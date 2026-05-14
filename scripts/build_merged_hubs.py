"""Build per-ticker MERGE-TOTAL hubs at obsidian_vault/hubs/<TK>.md.

This is the deep-cleanup version: instead of linking to scattered sources,
it absorbs each source file's content as an inline section. After running:
the hub is a single long file containing all per-ticker history, and the
source files can be safely buried (their content is preserved here).

Sources merged per ticker (when present):
  - tickers/<TK>.md             -> 'Panorama'
  - tickers/<TK>_DOSSIE.md      -> 'Deepdive (DOSSIE)'
  - tickers/<TK>_IC_DEBATE.md   -> 'IC Debate'
  - tickers/<TK>_VARIANT.md     -> 'Variant perception'
  - tickers/<TK>_RI.md          -> 'RI'
  - dossiers/<TK>.md            -> 'Dossier'
  - dossiers/<TK>_STORY.md      -> 'Story'
  - dossiers/<TK>_COUNCIL.md    -> 'Council aggregate'
  - dossiers/<TK>_FILING_<D>.md -> per-date filing
  - dossiers/<TK>_CONTENT_TRIGGER_*.md
  - dossiers/<TK>_MIGRATION*.md
  - agents/<Persona>/reviews/<TK>_<D>.md -> council review by persona
  - briefings/drip_scenarios/<TK>_drip.md -> 'DRIP scenarios'
  - briefings/earnings_prep_<TK>_<D>.md   -> 'Earnings prep'
  - wiki/holdings/<TK>.md       -> 'Wiki playbook'
  - Overnight_<DATE>/<TK>.md    -> 'Overnight scrape'
  - Pilot_Deep_Dive_<DATE>/<TK>.md -> 'Pilot deepdive'
  - Sessions/<TK>_*.md          -> 'Session notes'
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import re
import json
import sqlite3
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path("obsidian_vault")
HUBS = VAULT / "hubs"
HUBS.mkdir(exist_ok=True)
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
FRONTMATTER_RE = re.compile(r"^---\s*\n(?:.*?\n)?---\s*\n", re.DOTALL)


def universe_tickers() -> dict[str, dict]:
    """Return dict[ticker] -> {market, bucket, name, sector}."""
    out: dict[str, dict] = {}
    with open("config/universe.yaml", "r", encoding="utf-8") as f:
        u = yaml.safe_load(f)
    for market in ("br", "us"):
        m = u.get(market, {})
        for bucket in ("holdings", "watchlist", "research_pool"):
            node = m.get(bucket, {})
            stack = [node]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    stack.extend(cur.values())
                elif isinstance(cur, list):
                    for item in cur:
                        if isinstance(item, dict) and "ticker" in item:
                            tk = item["ticker"]
                            if tk not in out:
                                out[tk] = {
                                    "market": market,
                                    "bucket": bucket,
                                    "name": item.get("name", ""),
                                    "sector": item.get("sector") or item.get("segment", ""),
                                }
                        else:
                            stack.append(item)
    # Kings & Aristocrats
    if Path("config/kings_aristocrats.yaml").exists():
        with open("config/kings_aristocrats.yaml", "r", encoding="utf-8") as f:
            k = yaml.safe_load(f)
        for item in k.get("tickers", []):
            tk = item["ticker"]
            if tk not in out:
                out[tk] = {
                    "market": "us",
                    "bucket": "kings_aristocrats",
                    "name": item.get("name", ""),
                    "sector": item.get("sector", ""),
                }
    return out


def categorize(rel: Path, ticker: str) -> tuple[str, str | None, str]:
    """Return (category, iso_date, section_label)."""
    s = str(rel).replace("\\", "/")
    name = rel.name
    iso = (DATE_RE.search(s) or [None])[0] if DATE_RE.search(s) else None

    if s.startswith("Overnight_"):
        return ("overnight", iso or s[10:20], "Overnight scrape")
    if s.startswith("Pilot_Deep_Dive_"):
        return ("pilot", iso or s[16:26], "Pilot deepdive")
    if "/reviews/" in s and s.startswith("agents/"):
        persona = s.split("/")[1]
        return (f"council_review:{persona}", iso, f"Council review · {persona}")
    if s.startswith("briefings/drip_scenarios/"):
        return ("drip", iso, "DRIP scenarios")
    if "earnings_prep_" in name:
        return ("earnings_prep", iso, "Earnings prep")
    if s.startswith("dossiers/") and "_STORY" in name:
        return ("story", iso, "Story")
    if s.startswith("dossiers/") and "_COUNCIL" in name:
        return ("council", iso, "Council aggregate")
    if s.startswith("dossiers/") and "_FILING_" in name:
        return ("filing", iso, f"Filing {iso or '—'}")
    if s.startswith("dossiers/") and "_CONTENT_TRIGGER_" in name:
        return ("content_trigger", iso, "Content trigger")
    if s.startswith("dossiers/") and ("_MIGRATION" in name or "_PATRIA" in name or "_vs_" in name):
        return ("migration", iso, "Migration / transition")
    if s.startswith("dossiers/"):
        return ("dossier", iso, "Dossier")
    if s.startswith("tickers/") and "_DOSSIE" in name:
        return ("deepdive", iso, "Deepdive (DOSSIE)")
    if s.startswith("tickers/") and "_IC_DEBATE" in name:
        return ("ic_debate", iso, "IC Debate (synthetic)")
    if s.startswith("tickers/") and "_VARIANT" in name:
        return ("variant", iso, "Variant perception")
    if s.startswith("tickers/") and "_RI" in name:
        return ("ri", iso, "RI / disclosure")
    if s.startswith("tickers/"):
        return ("panorama", iso, "Panorama")
    if s.startswith("wiki/"):
        return ("wiki", iso, "Wiki playbook")
    if s.startswith("Sessions/"):
        return ("session", iso, "Session notes")
    if s.startswith("Bibliotheca/"):
        return ("bibliotheca", iso, "Bibliotheca cross-ref")
    return ("other", iso, "Other")


def file_matches_ticker(path: Path, ticker: str) -> bool:
    """Strict match: ticker must be a token in the filename or in a path segment."""
    tk = ticker.upper()
    stem_upper = path.stem.upper()
    # tokenize by separator
    parts = re.split(r"[_\-\.\s]", stem_upper)
    if tk in parts:
        return True
    # path segment match (e.g., dossiers/archive/JNJ_STORY_<DATE>.md)
    path_upper = str(path).upper().replace("\\", "/")
    return bool(re.search(rf"(?:^|/){re.escape(tk)}(?:[_\-\.\s/]|$)", path_upper))


def collect_artifacts(ticker: str) -> list[tuple[Path, str, str | None, str]]:
    """Return list of (path, category, iso_date, label)."""
    items: list[tuple[Path, str, str | None, str]] = []
    for p in VAULT.rglob("*.md"):
        if "cemetery" in p.parts:
            continue
        if p.parts and p.parts[0] == "hubs":
            continue
        rel = p.relative_to(VAULT)
        if file_matches_ticker(rel, ticker):
            cat, iso, label = categorize(rel, ticker.upper())
            items.append((p, cat, iso, label))
    return items


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Extract front-matter as dict + return body."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = text[: m.end()]
    # crude key:value
    fm: dict = {}
    for line in fm_text.split("\n")[1:-2]:
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    body = text[m.end():]
    return fm, body


def demote_headings(body: str, levels: int = 3) -> str:
    """Demote markdown headings by `levels` to nest inside an outer heading."""
    out_lines = []
    for line in body.split("\n"):
        m = re.match(r"^(#+)\s", line)
        if m:
            new_level = min(6, len(m.group(1)) + levels)
            line = "#" * new_level + line[m.end(1):]
        out_lines.append(line)
    return "\n".join(out_lines)


def load_db_meta(ticker: str, market: str) -> dict:
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
            out.update(dict(zip(["period_end", "pe", "pb", "dy", "roe", "nd_ebitda", "streak", "aristocrat"], row)))
        row = con.execute("SELECT name, sector, currency FROM companies WHERE ticker=?", (ticker,)).fetchone()
        if row:
            out["name"], out["sector"], out["currency"] = row
        row = con.execute(
            "SELECT quantity, entry_price FROM portfolio_positions WHERE ticker=? AND active=1",
            (ticker,),
        ).fetchone()
        if row:
            out["quantity"], out["entry_price"] = row
        row = con.execute(
            "SELECT action, total_score, date FROM verdict_history WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if row:
            out["verdict"], out["score"], out["verdict_date"] = row
        con.close()
    except sqlite3.Error:
        pass
    # Latest deepdive json
    dd = sorted(Path("reports/deepdive").glob(f"{ticker}_deepdive_*.json"))
    if dd:
        try:
            data = json.loads(dd[-1].read_text(encoding="utf-8", errors="ignore"))
            out["deepdive_file"] = dd[-1].name
            out["deepdive_dt"] = datetime.fromtimestamp(dd[-1].stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            if isinstance(data, dict):
                audit = data.get("auditor", {})
                if audit:
                    out["audit"] = {k: audit.get(k) for k in ("piotroski", "altman", "beneish", "moat") if k in audit}
        except Exception:
            pass
    return out


def fmt_num(k, v):
    if v is None or v == "":
        return None
    if k in ("dy", "roe"):
        try: return f"{float(v) * 100:.1f}%"
        except: return str(v)
    if k in ("pe", "pb", "nd_ebitda"):
        try: return f"{float(v):.2f}"
        except: return str(v)
    if k == "aristocrat":
        try: return "yes" if int(v) == 1 else "no"
        except: return str(v)
    return str(v)


def build_hub(ticker: str, meta_yaml: dict) -> str:
    market = meta_yaml["market"]
    bucket = meta_yaml["bucket"]
    name = meta_yaml.get("name") or ticker
    sector = meta_yaml.get("sector") or "—"

    db_meta = load_db_meta(ticker, market)
    currency = db_meta.get("currency") or ("BRL" if market == "br" else "USD")
    today = datetime.now().strftime("%Y-%m-%d")

    arts = collect_artifacts(ticker)
    # sort newest-first by date; undated to end
    arts.sort(key=lambda x: (x[2] or "0000-00-00"), reverse=True)

    lines: list[str] = []
    lines.append("---")
    lines.append("type: ticker_hub")
    lines.append(f"ticker: {ticker}")
    lines.append(f"market: {market}")
    lines.append(f"sector: {sector}")
    lines.append(f"currency: {currency}")
    lines.append(f"bucket: {bucket}")
    lines.append(f"is_holding: {'true' if bucket == 'holdings' else 'false'}")
    lines.append(f"generated: {today}")
    lines.append(f"sources_merged: {len(arts)}")
    lines.append("tags: [hub, ticker, merged]")
    lines.append('parent: "[[_TICKERS_INDEX]]"')
    lines.append("---")
    lines.append("")
    lines.append(f"# {ticker} — {name or ticker}")
    lines.append("")
    lines.append(f"> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.")
    lines.append("")
    lines.append(f"`sector: {sector}` · `market: {market.upper()}` · `currency: {currency}` · `bucket: {bucket}` · `{len(arts)} sources merged`")
    lines.append("")

    # ── HOJE ────────────────────────────────────────────────────
    lines.append("## 🎯 Hoje")
    lines.append("")
    if db_meta.get("quantity") is not None:
        lines.append(f"- **Posição**: {db_meta['quantity']} @ entry {db_meta.get('entry_price', '—')}")
    if db_meta.get("verdict"):
        lines.append(f"- **Verdict (DB)**: `{db_meta['verdict']}` (score {db_meta.get('score', '—')}, {db_meta.get('verdict_date', '—')})")
    if db_meta.get("deepdive_file"):
        lines.append(f"- **Último deepdive**: `{db_meta['deepdive_file']}` ({db_meta.get('deepdive_dt', '—')})")
        if db_meta.get("audit"):
            au = db_meta["audit"]
            au_str = " · ".join(f"{k}={au[k]}" for k in au if au[k] is not None)
            if au_str:
                lines.append(f"- **Auditor**: {au_str}")
    if db_meta.get("period_end"):
        parts = []
        for k, label in [("pe", "P/E"), ("pb", "P/B"), ("dy", "DY"), ("roe", "ROE"), ("nd_ebitda", "ND/EBITDA"), ("streak", "Dividend streak"), ("aristocrat", "Aristocrat")]:
            v = fmt_num(k, db_meta.get(k))
            if v is not None:
                parts.append(f"{label} {v}")
        if parts:
            lines.append(f"- **Fundamentals** ({db_meta['period_end']}): " + " · ".join(parts))
    if not any([db_meta.get("quantity") is not None, db_meta.get("verdict"), db_meta.get("deepdive_file"), db_meta.get("period_end")]):
        lines.append("_(sem dados na DB)_")
    lines.append("")

    # ── HISTÓRICO ─────────────────────────────────────────────
    lines.append("## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)")
    lines.append("")
    lines.append("> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.")
    lines.append("")

    if not arts:
        lines.append("_(sem fontes para absorver)_")
    else:
        last_year = None
        for path, cat, iso, label in arts:
            year = iso[:4] if iso else "(undated)"
            if year != last_year:
                lines.append(f"\n### {year}\n")
                last_year = year
            date_display = iso or "—"
            rel = path.relative_to(VAULT)
            lines.append(f"#### {date_display} · {label}")
            lines.append(f"_source: `{rel}` (now in cemetery)_")
            lines.append("")
            try:
                raw = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                raw = ""
            _, body = strip_frontmatter(raw)
            body = body.strip()
            # Skip body if essentially empty
            if len(body) < 30:
                lines.append("_(stub vazio ou quase vazio — sem conteúdo a absorver)_")
                lines.append("")
                continue
            # Truncate giant files (>15k chars) to keep hub readable
            truncated = False
            if len(body) > 15000:
                body = body[:15000]
                truncated = True
            demoted = demote_headings(body, levels=3)
            lines.append(demoted)
            if truncated:
                lines.append("")
                lines.append(f"_… (truncated at 15k chars — full content in cemetery copy of `{rel}`)_")
            lines.append("")

    # ── REFRESH ─────────────────────────────────────────────
    lines.append("## ⚙️ Refresh commands")
    lines.append("")
    lines.append("```bash")
    lines.append(f"ii panorama {ticker} --write")
    lines.append(f"ii deepdive {ticker} --save-obsidian")
    lines.append(f"ii verdict {ticker} --narrate --write")
    lines.append(f"ii fv {ticker}")
    lines.append(f"python -m analytics.fair_value_forward --ticker {ticker}")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append(f"_Gerado por `scripts/build_merged_hubs.py` em {today}. Run again to refresh._")
    return "\n".join(lines) + "\n"


def main() -> None:
    universe = universe_tickers()
    print(f"Universe size: {len(universe)} tickers")

    # Limit to tickers actually present in vault (any per-ticker file)
    present = set()
    for tk in universe:
        for p in VAULT.rglob("*.md"):
            if "cemetery" in p.parts:
                continue
            if p.parts and p.parts[0] == "hubs":
                continue
            rel = p.relative_to(VAULT)
            if file_matches_ticker(rel, tk):
                present.add(tk)
                break
    print(f"Tickers with vault content: {len(present)}")

    # Build hubs
    written = 0
    skipped = 0
    for tk in sorted(present):
        meta = universe[tk]
        content = build_hub(tk, meta)
        n_arts = content.count("#### ")
        out = HUBS / f"{tk}.md"
        try:
            out.write_text(content, encoding="utf-8")
            print(f"  {tk:8s} ({meta['market']}/{meta['bucket']:<18s}): {n_arts:3d} sources merged · {len(content):,} bytes")
            written += 1
        except Exception as e:
            print(f"  {tk}: WRITE FAILED ({e})")
            skipped += 1
    print(f"\nDone: {written} hubs written, {skipped} skipped → obsidian_vault/hubs/")


if __name__ == "__main__":
    main()
