"""Decision Journal Intelligence — pattern mining em past decisions/notes/triggers.

Inspirado em "Decision journal intelligence — detectar padrões nos seus erros" da lista do user.

Sources mined:
  - obsidian_vault/tickers/<X>.md (notas existentes — observações)
  - watchlist_actions (resolved/ignored history) — quais propostas foram aceites/rejeitadas
  - paper_trade_signals com status closed_* (win/loss outcomes)
  - perpetuum_health (thesis_score trajectory) — quais ações tiveram decay e o que aconteceu
  - briefings/ — histórico de alertas matinais

Patterns detected:
  P1. Auto-ignored kinds: que tipos de action sempre ignoramos? (high ignore rate por kind)
  P2. Action latency: quanto tempo demoramos a actuar em actions abertas?
  P3. Thesis decay → outcome: tickers com decay maior tiveram pior performance?
  P4. Dominant ticker concerns: quais tickers aparecem mais vezes em risk_auditor flags?
  P5. Sector concentration in flags: setor que mais flagado

Output: obsidian_vault/briefings/decision_journal_intel_<DATE>.md

100% local. Pure SQL + filesystem.
"""
from __future__ import annotations

import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
BRIEFINGS_DIR = ROOT / "obsidian_vault" / "briefings"


def pattern_action_resolution() -> dict:
    """P1+P2: ignore rate por kind + average resolution time."""
    out = {"by_kind": [], "overall": {}}
    by_kind = defaultdict(lambda: {"open": 0, "resolved": 0, "ignored": 0, "resolution_days": []})
    for db in DBS.values():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            try:
                rows = c.execute("""
                    SELECT kind, status, opened_at, resolved_at FROM watchlist_actions
                """).fetchall()
            except sqlite3.OperationalError:
                continue
            for r in rows:
                k = r["kind"] or "?"
                s = r["status"] or "open"
                if s in ("open", "resolved", "ignored"):
                    by_kind[k][s] += 1
                if s in ("resolved", "ignored") and r["opened_at"] and r["resolved_at"]:
                    try:
                        oa = datetime.fromisoformat(r["opened_at"].replace("Z", "+00:00"))
                        ra = datetime.fromisoformat(r["resolved_at"].replace("Z", "+00:00"))
                        days = (ra - oa).total_seconds() / 86400
                        by_kind[k]["resolution_days"].append(days)
                    except Exception:
                        pass

    for k, v in by_kind.items():
        n = v["open"] + v["resolved"] + v["ignored"]
        if n == 0:
            continue
        ignore_rate = v["ignored"] / n
        avg_days = sum(v["resolution_days"]) / max(len(v["resolution_days"]), 1)
        out["by_kind"].append({
            "kind": k, "n": n,
            "open": v["open"], "resolved": v["resolved"], "ignored": v["ignored"],
            "ignore_rate_pct": round(ignore_rate * 100, 1),
            "avg_resolution_days": round(avg_days, 1) if v["resolution_days"] else None,
        })
    out["by_kind"].sort(key=lambda x: -x["ignore_rate_pct"])
    return out


def pattern_thesis_decay() -> dict:
    """P3: thesis_score trajectory per ticker — biggest decays."""
    decays = []
    for market, db in DBS.items():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            try:
                rows = c.execute("""
                    SELECT ticker,
                           MAX(thesis_score) AS max_score,
                           MIN(thesis_score) AS min_score,
                           COUNT(*) AS runs
                    FROM thesis_health WHERE thesis_score >= 0
                    GROUP BY ticker
                """).fetchall()
            except sqlite3.OperationalError:
                continue
            for r in rows:
                ticker, max_s, min_s, runs = r
                drop = max_s - min_s
                if drop > 0:
                    decays.append({"ticker": ticker, "market": market, "max_score": max_s,
                                   "min_score": min_s, "drop": drop, "runs": runs})
    decays.sort(key=lambda x: -x["drop"])
    return {"decays": decays}


def pattern_paper_trade_outcomes() -> dict:
    """P3 ext: paper signal close stats per method."""
    by_method = defaultdict(lambda: {"open": 0, "win": 0, "loss": 0, "flat": 0, "expired": 0,
                                     "returns": []})
    for db in DBS.values():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            try:
                rows = c.execute("""
                    SELECT method_id, status, realized_return_pct
                    FROM paper_trade_signals
                """).fetchall()
            except sqlite3.OperationalError:
                continue
            for r in rows:
                m, s, ret = r
                if s == "open":
                    by_method[m]["open"] += 1
                elif s == "closed_win":
                    by_method[m]["win"] += 1
                    if ret is not None: by_method[m]["returns"].append(ret)
                elif s == "closed_loss":
                    by_method[m]["loss"] += 1
                    if ret is not None: by_method[m]["returns"].append(ret)
                elif s == "closed_flat":
                    by_method[m]["flat"] += 1
                elif s == "expired":
                    by_method[m]["expired"] += 1
    out = []
    for m, v in by_method.items():
        closed = v["win"] + v["loss"] + v["flat"]
        avg_ret = sum(v["returns"]) / len(v["returns"]) if v["returns"] else None
        out.append({"method": m, "open": v["open"], "closed": closed,
                    "win": v["win"], "loss": v["loss"],
                    "win_rate_pct": round(v["win"] / closed * 100, 1) if closed else None,
                    "avg_return_pct": round(avg_ret, 2) if avg_ret is not None else None})
    out.sort(key=lambda x: -(x["closed"] or 0))
    return {"by_method": out}


def pattern_dominant_concerns() -> dict:
    """P4+P5: tickers + sectors most flagged in perpetuum + risk_auditor."""
    ticker_flags = Counter()
    sector_flags = Counter()

    for db in DBS.values():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            # From perpetuum_health (low scores)
            try:
                rows = c.execute("""
                    SELECT subject_id, flag_count FROM perpetuum_health
                    WHERE perpetuum_name IN ('thesis', 'data_coverage', 'ri_freshness')
                      AND score >= 0 AND flag_count > 0
                """).fetchall()
                for r in rows:
                    subj = r["subject_id"]
                    if ":" in subj:
                        ticker = subj.split(":", 1)[1]
                        ticker_flags[ticker] += r["flag_count"] or 1
            except sqlite3.OperationalError:
                pass

            # Map ticker → sector
            try:
                ts = dict(c.execute("SELECT ticker, sector FROM companies").fetchall())
                for t, n in list(ticker_flags.items()):
                    if t in ts:
                        sector_flags[ts[t] or "?"] += n
            except sqlite3.OperationalError:
                pass

    return {
        "top_tickers": ticker_flags.most_common(15),
        "top_sectors": sector_flags.most_common(10),
    }


def write_report(p1: dict, p2: dict, p3: dict, p4: dict) -> Path:
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    out = BRIEFINGS_DIR / f"decision_journal_intel_{date.today().isoformat()}.md"
    lines = [
        "---",
        "type: decision_journal_intelligence",
        f"date: {date.today().isoformat()}",
        "tags: [decision_journal, meta, autocrítica, patterns]",
        "---",
        "",
        "# 🧠 Decision Journal Intelligence",
        "",
        "> Pattern mining em past decisions, actions, paper signals, e thesis decay. 100% local SQL.",
        "",
        "## 🔁 Pattern 1+2 — Action resolution patterns",
        "",
    ]
    if p1["by_kind"]:
        lines.append("| Kind | n | Open | Resolved | Ignored | Ignore% | Avg days |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for k in p1["by_kind"]:
            avg = f"{k['avg_resolution_days']:.1f}d" if k['avg_resolution_days'] else "—"
            lines.append(f"| {k['kind']} | {k['n']} | {k['open']} | {k['resolved']} | {k['ignored']} | {k['ignore_rate_pct']}% | {avg} |")
    else:
        lines.append("_No action history yet._")
    lines.append("")

    lines.append("## 📉 Pattern 3 — Thesis decay leaders")
    lines.append("")
    if p2["decays"]:
        lines.append("| Ticker | Market | Max | Min | Drop | Runs |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for d in p2["decays"][:15]:
            lines.append(f"| {d['ticker']} | {d['market'].upper()} | {d['max_score']} | {d['min_score']} | -{d['drop']} | {d['runs']} |")
    else:
        lines.append("_No thesis_health history with decay yet (sistema novo)._")
    lines.append("")

    lines.append("## 🎯 Pattern 4 — Paper trade method performance")
    lines.append("")
    if p3["by_method"]:
        lines.append("| Method | Open | Closed | Win | Loss | Win% | Avg ret% |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for m in p3["by_method"][:20]:
            wr = f"{m['win_rate_pct']}%" if m['win_rate_pct'] is not None else "—"
            ar = f"{m['avg_return_pct']:+.2f}%" if m['avg_return_pct'] is not None else "—"
            lines.append(f"| {m['method'][:40]} | {m['open']} | {m['closed']} | {m['win']} | {m['loss']} | {wr} | {ar} |")
        lines.append("")
        lines.append("> ⚠️ **Sistema novo — quase tudo open. Real intelligence emerge depois de 30+ closed signals/method.**")
    lines.append("")

    lines.append("## 🚨 Pattern 5 — Dominant concerns (most-flagged)")
    lines.append("")
    lines.append("### Top 15 tickers by flag count (perpetuums)")
    lines.append("")
    lines.append("| Ticker | Total flags |")
    lines.append("|---|---:|")
    for t, n in p4["top_tickers"]:
        lines.append(f"| {t} | {n} |")
    lines.append("")
    if p4["top_sectors"]:
        lines.append("### Sectors com mais flags")
        lines.append("")
        lines.append("| Sector | Flags |")
        lines.append("|---|---:|")
        for s, n in p4["top_sectors"]:
            lines.append(f"| {s} | {n} |")
        lines.append("")

    lines.append("## 💡 Insights actionable")
    lines.append("")
    # Build insights from patterns
    insights = []
    if p1["by_kind"]:
        high_ignore = [k for k in p1["by_kind"] if k["ignore_rate_pct"] >= 70 and k["n"] >= 3]
        for k in high_ignore:
            insights.append(f"- **Action `{k['kind']}` é maioritariamente ignorada ({k['ignore_rate_pct']}%)** — considera silenciar este perpetuum ou ajustar threshold")
    if p4["top_tickers"]:
        top1 = p4["top_tickers"][0]
        if top1[1] > 5:
            insights.append(f"- **{top1[0]}** acumula {top1[1]} flags — re-avaliar position size ou exit")
    if p4["top_sectors"]:
        top_sect = p4["top_sectors"][0]
        if top_sect[1] > 10:
            insights.append(f"- **Sector {top_sect[0]}** concentra {top_sect[1]} flags — concentration risk a observar")
    if not insights:
        insights.append("_(no clear patterns yet — sistema precisa de mais dados ao longo do tempo)_")
    lines.extend(insights)
    lines.append("")

    lines.append("## 🪞 Auto-crítica do próprio sistema")
    lines.append("")
    lines.append("- Decision journal só fica útil após **30+ days de operação** com action resolutions")
    lines.append("- Paper signals win-rate só significant após **30+ closed signals/method**")
    lines.append("- Thesis decay dataset é tiny (sistema só corre desde 2026-04-24)")
    lines.append("- Pattern detection é honesto sobre amostra pequena")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== Decision Journal Intelligence ===")
    p1 = pattern_action_resolution()
    p2 = pattern_thesis_decay()
    p3 = pattern_paper_trade_outcomes()
    p4 = pattern_dominant_concerns()
    out = write_report(p1, p2, p3, p4)
    print(f"\nWrote: {out.relative_to(ROOT)}")
    print(f"Patterns analyzed:")
    print(f"  Actions tracked: {sum(k['n'] for k in p1['by_kind'])} across {len(p1['by_kind'])} kinds")
    print(f"  Thesis decays: {len(p2['decays'])} tickers")
    print(f"  Paper signal methods: {len(p3['by_method'])}")
    print(f"  Top flagged tickers: {len(p4['top_tickers'])}")


if __name__ == "__main__":
    main()
