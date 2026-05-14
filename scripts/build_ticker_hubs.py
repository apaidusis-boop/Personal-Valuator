"""Build per-ticker consolidation hubs at obsidian_vault/hubs/<TK>.md.

Each hub is a single morning-read file that:
- shows current verdict + fundamentals
- has a chronological "Historical Journal" linking every per-ticker artifact in the vault
- groups artifacts by type (overnight, council, filing, deepdive, story, drip, wiki, ic_debate, variant, ri, pilot)

The hub is regenerable - running this script again rebuilds from scratch.
"""
from __future__ import annotations
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path("obsidian_vault")
HUBS = VAULT / "hubs"
HUBS.mkdir(exist_ok=True)

# Match a ticker followed by a non-alphanumeric boundary
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def holdings_from_dbs() -> list[tuple[str, str]]:
    out = []
    for market, db in [("br", "data/br_investments.db"), ("us", "data/us_investments.db")]:
        try:
            con = sqlite3.connect(db)
            for (tk,) in con.execute(
                "SELECT ticker FROM portfolio_positions WHERE active=1 ORDER BY ticker"
            ):
                out.append((tk, market))
            con.close()
        except sqlite3.Error:
            pass
    return out


def categorize(rel_path: Path, ticker: str) -> tuple[str, str | None]:
    """Return (category, iso_date) for an artifact path."""
    s = str(rel_path).replace("\\", "/")
    name = rel_path.name
    date_match = DATE_RE.search(s)
    iso = date_match.group(1) if date_match else None

    if s.startswith(f"Overnight_"):
        return ("overnight", iso or s[len("Overnight_"):len("Overnight_") + 10])
    if s.startswith("Pilot_Deep_Dive_"):
        return ("pilot", iso or s[len("Pilot_Deep_Dive_"):len("Pilot_Deep_Dive_") + 10])
    if s.startswith("agents/") and "/reviews/" in s:
        persona = s.split("/")[1]
        return ("council_review:" + persona, iso)
    if s.startswith("briefings/drip_scenarios/"):
        return ("drip", iso)
    if "earnings_prep_" in name:
        return ("earnings_prep", iso)
    if s.startswith("dossiers/archive/"):
        return ("dossier_archive", iso)
    if s.startswith("dossiers/") and "_STORY" in name:
        return ("story", iso)
    if s.startswith("dossiers/") and "_COUNCIL" in name:
        return ("council", iso)
    if s.startswith("dossiers/") and "_FILING_" in name:
        return ("filing", iso)
    if s.startswith("dossiers/") and "_CONTENT_TRIGGER_" in name:
        return ("content_trigger", iso)
    if s.startswith("dossiers/") and "_MIGRATION" in name:
        return ("migration", iso)
    if s.startswith("dossiers/") and "_PATRIA_TRANSITION" in name:
        return ("migration", iso)
    if s.startswith("tickers/") and "_DOSSIE" in name:
        return ("deepdive", iso)
    if s.startswith("tickers/") and "_IC_DEBATE" in name:
        return ("ic_debate", iso)
    if s.startswith("tickers/") and "_VARIANT" in name:
        return ("variant", iso)
    if s.startswith("tickers/") and "_RI" in name:
        return ("ri", iso)
    if s.startswith("tickers/"):
        return ("panorama", iso)
    if s.startswith("wiki/"):
        return ("wiki", iso)
    if s.startswith("Sessions/"):
        return ("session", iso)
    if s.startswith("Bibliotheca/"):
        return ("bibliotheca", iso)
    if s.startswith("Clippings/"):
        return ("clipping", iso)
    if s.startswith("videos/"):
        return ("video", iso)
    return ("other", iso)


def collect_artifacts(ticker: str) -> dict[str, list[tuple[str, str | None]]]:
    """Return dict[category] -> list of (rel_path, iso_date)."""
    out: dict[str, list[tuple[str, str | None]]] = defaultdict(list)
    tk_upper = ticker.upper()
    # Strict ticker filename matcher: name must contain ticker as a token
    tok = re.compile(rf"(?:^|[_\-\.\s/]){re.escape(tk_upper)}(?:[_\-\.\s/]|$)")
    for p in VAULT.rglob("*.md"):
        # skip hubs folder itself
        if p.parts and p.parts[0] == "hubs":
            continue
        rel = p.relative_to(VAULT)
        # Match name OR any path segment; we want stem-level match primarily
        if tok.search(rel.name.upper()) or tok.search(str(rel).upper().replace("\\", "/")):
            cat, iso = categorize(rel, tk_upper)
            out[cat].append((str(rel).replace("\\", "/"), iso))
    # Also include JSON deepdives (reports/deepdive/<TK>_deepdive_*.json) — referenced from hub
    for p in Path("reports/deepdive").glob(f"{tk_upper}_deepdive_*.json"):
        out["deepdive_json"].append((str(p).replace("\\", "/"), None))
    return out


def latest_deepdive_json(ticker: str) -> Path | None:
    candidates = sorted(Path("reports/deepdive").glob(f"{ticker}_deepdive_*.json"))
    return candidates[-1] if candidates else None


def load_verdict(ticker: str) -> dict:
    """Pull current verdict + key fundamentals."""
    out: dict = {}
    dd = latest_deepdive_json(ticker)
    if dd:
        try:
            data = json.loads(dd.read_text(encoding="utf-8", errors="ignore"))
            out["deepdive_file"] = dd.name
            out["deepdive_dt"] = datetime.fromtimestamp(dd.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            # extract a few common keys defensively
            for k in ("ticker", "market", "verdict", "score", "moat", "altman", "piotroski", "beneish", "fair_value", "thesis_health"):
                if isinstance(data, dict) and k in data:
                    out[k] = data[k]
            # nested verdict patterns
            audit = data.get("auditor", {}) if isinstance(data, dict) else {}
            if audit:
                out["audit"] = {k: audit.get(k) for k in ("piotroski", "altman", "beneish", "moat") if k in audit}
        except Exception:
            pass
    # Try sqlite verdict_history (correct schema: action + total_score + date)
    for db in ("data/br_investments.db", "data/us_investments.db"):
        try:
            con = sqlite3.connect(db)
            cur = con.execute(
                "SELECT action, total_score, date FROM verdict_history WHERE ticker=? ORDER BY date DESC LIMIT 1",
                (ticker,),
            )
            row = cur.fetchone()
            if row:
                out["db_verdict"] = row[0]
                out["db_score"] = row[1]
                out["db_date"] = row[2]
                break
            con.close()
        except sqlite3.Error:
            try:
                con.close()
            except Exception:
                pass
    return out


def load_fundamentals(ticker: str, market: str) -> dict:
    db = f"data/{market}_investments.db"
    out: dict = {}
    try:
        con = sqlite3.connect(db)
        row = con.execute(
            """SELECT period_end, pe, pb, dy, roe, net_debt_ebitda, dividend_streak_years, is_aristocrat
               FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if row:
            keys = ["period_end", "pe", "pb", "dy", "roe", "nd_ebitda", "streak", "aristocrat"]
            out = dict(zip(keys, row))
        # holding intent / sector
        row = con.execute(
            "SELECT name, sector, currency FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        if row:
            out["name"] = row[0]
            out["sector"] = row[1]
            out["currency"] = row[2]
        # position
        row = con.execute(
            "SELECT quantity, entry_price FROM portfolio_positions WHERE ticker=? AND active=1",
            (ticker,),
        ).fetchone()
        if row:
            out["quantity"] = row[0]
            out["entry_price"] = row[1]
        con.close()
    except sqlite3.Error:
        pass
    return out


def build_hub(ticker: str, market: str) -> str:
    arts = collect_artifacts(ticker)
    v = load_verdict(ticker)
    f = load_fundamentals(ticker, market)
    today = datetime.now().strftime("%Y-%m-%d")

    name = f.get("name") or ticker
    sector = f.get("sector") or "—"
    currency = f.get("currency") or ("BRL" if market == "br" else "USD")

    lines = []
    lines.append("---")
    lines.append("type: ticker_hub")
    lines.append(f"ticker: {ticker}")
    lines.append(f"market: {market}")
    lines.append(f"sector: {sector}")
    lines.append(f"currency: {currency}")
    lines.append(f"generated: {today}")
    lines.append("tags: [hub, ticker, consolidated]")
    lines.append(f'parent: "[[_TICKERS_INDEX]]"')
    lines.append("---")
    lines.append("")
    lines.append(f"# {ticker} — {name}")
    lines.append("")
    lines.append(f"> **Hub consolidado**. Tudo o que existe no vault sobre {ticker}, em ordem cronológica. Cada link aponta para o ficheiro original que ficou na sua pasta — esta é a porta de entrada matinal.")
    lines.append("")
    lines.append(f"`sector: {sector}` · `market: {market.upper()}` · `currency: {currency}`")
    lines.append("")

    # ── HOJE ────────────────────────────────────────────────────
    lines.append("## 🎯 Hoje")
    lines.append("")
    if f.get("quantity") is not None:
        lines.append(f"- **Posição**: {f['quantity']} @ entry {f.get('entry_price', '—')}")
    if v.get("db_verdict"):
        lines.append(f"- **Verdict (DB)**: `{v['db_verdict']}` (score {v.get('db_score', '—')}, {v.get('db_date', '—')})")
    if v.get("deepdive_file"):
        lines.append(f"- **Último deepdive**: `{v['deepdive_file']}` ({v.get('deepdive_dt', '—')})")
        if v.get("audit"):
            audit = v["audit"]
            audit_str = " · ".join(f"{k}={audit[k]}" for k in audit if audit[k] is not None)
            if audit_str:
                lines.append(f"- **Auditor**: {audit_str}")
    if f.get("period_end"):
        fund_parts = []
        def _fmt(k, val):
            if val is None or val == "":
                return None
            if k in ("dy", "roe"):
                try:
                    return f"{float(val) * 100:.1f}%"
                except (TypeError, ValueError):
                    return str(val)
            if k in ("pe", "pb", "nd_ebitda"):
                try:
                    return f"{float(val):.2f}"
                except (TypeError, ValueError):
                    return str(val)
            if k == "aristocrat":
                try:
                    return "yes" if int(val) == 1 else "no"
                except (TypeError, ValueError):
                    return str(val)
            return str(val)
        for k, label in [("pe", "P/E"), ("pb", "P/B"), ("dy", "DY"), ("roe", "ROE"), ("nd_ebitda", "ND/EBITDA"), ("streak", "Dividend streak"), ("aristocrat", "Aristocrat")]:
            val = _fmt(k, f.get(k))
            if val is not None:
                fund_parts.append(f"{label} {val}")
        if fund_parts:
            lines.append(f"- **Fundamentals** ({f['period_end']}): " + " · ".join(fund_parts))
    if not any([f.get("quantity") is not None, v.get("db_verdict"), v.get("deepdive_file"), f.get("period_end")]):
        lines.append("_(sem dados na DB)_")
    lines.append("")

    # ── HISTÓRICO ─────────────────────────────────────────────
    lines.append("## 📜 Histórico (chronological journal)")
    lines.append("")
    lines.append("> Como a vista sobre este nome evoluiu — do primeiro screen ao deepdive mais recente. Útil para perceber **o que sabíamos antes vs o que sabemos agora**.")
    lines.append("")

    # collect every artifact with date, sort desc
    rows = []
    for cat, items in arts.items():
        for path, iso in items:
            rows.append((iso or "0000-00-00", cat, path))
    rows.sort(reverse=True)

    if not rows:
        lines.append("_(sem artefactos cronológicos)_")
    else:
        last_year = None
        for iso, cat, path in rows:
            year = iso[:4] if iso != "0000-00-00" else "(undated)"
            if year != last_year:
                lines.append(f"\n### {year}\n")
                last_year = year
            # human label
            label = cat.replace("council_review:", "Review · ").replace("_", " ").title()
            # obsidian link by basename, but include path for clarity
            stem = Path(path).stem
            date_display = iso if iso != "0000-00-00" else "—"
            lines.append(f"- **{date_display}** · {label} → [[{stem}]] _(`{path}`)_")
    lines.append("")

    # ── ARTEFACTOS POR CATEGORIA ──────────────────────────────
    lines.append("## 🗂️ Artefactos por categoria")
    lines.append("")
    cat_order = [
        ("panorama", "Panorama"),
        ("deepdive", "Deepdive (DOSSIE)"),
        ("deepdive_json", "Deepdive JSON snapshots"),
        ("story", "Story"),
        ("council", "Council aggregate"),
        ("council_review:", "Council reviews por persona"),
        ("ic_debate", "IC Debate (synthetic)"),
        ("variant", "Variant perception"),
        ("ri", "RI / official disclosures"),
        ("filing", "Filings individuais"),
        ("overnight", "Overnight scrapes"),
        ("pilot", "Pilot deep dives"),
        ("drip", "DRIP scenarios"),
        ("earnings_prep", "Earnings prep briefs"),
        ("wiki", "Wiki / playbooks"),
        ("session", "Session notes"),
        ("bibliotheca", "Bibliotheca / clippings"),
        ("clipping", "Clippings"),
        ("video", "Video transcripts"),
        ("content_trigger", "Content trigger"),
        ("migration", "Migration / transition"),
        ("dossier_archive", "Archived stories"),
        ("other", "Other"),
    ]
    for key, label in cat_order:
        if key.endswith(":"):
            # gather all council_review:* persona buckets
            keys = [k for k in arts.keys() if k.startswith(key)]
            if not keys:
                continue
            lines.append(f"### {label}")
            for k in sorted(keys):
                persona = k.split(":", 1)[1]
                lines.append(f"\n_{persona}_:")
                for path, iso in sorted(arts[k], key=lambda x: x[1] or ""):
                    stem = Path(path).stem
                    lines.append(f"- [[{stem}]] _(`{path}`)_")
            lines.append("")
        else:
            if key not in arts:
                continue
            lines.append(f"### {label}")
            for path, iso in sorted(arts[key], key=lambda x: (x[1] or ""), reverse=True):
                stem = Path(path).stem
                lines.append(f"- [[{stem}]] _(`{path}`)_")
            lines.append("")

    # ── BUTTONS / COMMANDS ────────────────────────────────────
    lines.append("## ⚙️ Refresh commands")
    lines.append("")
    lines.append("```bash")
    lines.append(f"ii panorama {ticker} --write       # aggregator (verdict+peers+notes+videos)")
    lines.append(f"ii deepdive {ticker} --save-obsidian # V10 4-layer pipeline")
    lines.append(f"ii verdict {ticker} --narrate --write")
    lines.append(f"ii fv {ticker}                      # fair value (Buffett-Graham conservative)")
    lines.append(f"python -m analytics.fair_value_forward --ticker {ticker} # quality-aware forward")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Regenerado por `scripts/build_ticker_hubs.py`. Run novamente para refresh._")
    return "\n".join(lines) + "\n"


def main() -> None:
    holdings = holdings_from_dbs()
    if not holdings:
        print("No holdings found")
        return
    print(f"Building hubs for {len(holdings)} holdings…")
    written = 0
    for tk, market in holdings:
        content = build_hub(tk, market)
        out = HUBS / f"{tk}.md"
        out.write_text(content, encoding="utf-8")
        size = len(content)
        # count artifacts
        n_arts = sum(len(v) for v in collect_artifacts(tk).values())
        print(f"  {tk} ({market}): {n_arts} artefactos · {size:,} bytes → {out}")
        written += 1
    print(f"\nDone: {written} hubs at obsidian_vault/hubs/")


if __name__ == "__main__":
    main()
