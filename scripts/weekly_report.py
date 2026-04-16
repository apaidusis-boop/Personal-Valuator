"""Relatório semanal consolidado BR + US.

Lê `data/br_investments.db` e `data/us_investments.db`. Produz:
  - reports/weekly_YYYY-MM-DD.md   (estilo Fallout terminal)
  - reports/weekly_YYYY-MM-DD.html (render do md)

Secções:
  1. HEADER (contagens, últimas runs)
  2. EVENTOS DA SEMANA (events source=cvm/sec, últimos 7 dias)
  3. SCORING — quem passou/falhou nos critérios (último run)
  4. HOLDINGS — preço, variação, yield

Uso:
    python scripts/weekly_report.py                  # semana corrente
    python scripts/weekly_report.py --days 14        # últimos 14 dias
    python scripts/weekly_report.py --no-html        # só markdown
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORT_DIR = ROOT / "reports"

# 8-K items que queremos destacar como "prioritários" no digest
PRIORITY_8K_ITEMS = {"5.02", "8.01", "2.01", "1.01", "3.03"}


def _rows(db: Path, sql: str, params: tuple = ()) -> list[tuple]:
    with sqlite3.connect(db) as c:
        return c.execute(sql, params).fetchall()


def _is_priority_sec(summary: str | None) -> bool:
    if not summary:
        return False
    return any(f"{it}" in summary for it in PRIORITY_8K_ITEMS)


def header_block(today: date, days: int) -> list[str]:
    br_tickers = _rows(DB_BR, "SELECT COUNT(*) FROM companies")[0][0]
    us_tickers = _rows(DB_US, "SELECT COUNT(*) FROM companies")[0][0]
    br_scores = _rows(DB_BR, "SELECT run_date, COUNT(*) FROM scores GROUP BY run_date ORDER BY run_date DESC LIMIT 1")
    us_scores = _rows(DB_US, "SELECT run_date, COUNT(*) FROM scores GROUP BY run_date ORDER BY run_date DESC LIMIT 1")
    br_events = _rows(DB_BR, "SELECT COUNT(*) FROM events")[0][0]
    us_events = _rows(DB_US, "SELECT COUNT(*) FROM events")[0][0]

    br_run = f"{br_scores[0][0]}  ({br_scores[0][1]} tickers)" if br_scores else "NENHUM"
    us_run = f"{us_scores[0][0]}  ({us_scores[0][1]} tickers)" if us_scores else "NENHUM"

    return [
        "```",
        ">ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL",
        ">COPYRIGHT 2075-2077 ROBCO(R)",
        ">LOADER V1.1",
        ">EXEC VERSION 41.10",
        ">LOADING ARCHIVE...",
        "",
        "================================================================",
        "            INVESTMENT-INTELLIGENCE // WEEKLY DIGEST",
        f"            DATA ESTELAR: {today.isoformat()}  (JANELA: {days}D)",
        "================================================================",
        "",
        f"  ARCHIVE B3    : {br_tickers:>3} TICKERS   |  EVENTS: {br_events:>4}",
        f"  ARCHIVE NYSE  : {us_tickers:>3} TICKERS   |  EVENTS: {us_events:>4}",
        f"  LAST BR RUN   : {br_run}",
        f"  LAST US RUN   : {us_run}",
        "",
        "================================================================",
        "```",
        "",
    ]


def events_block(today: date, days: int) -> list[str]:
    since = (today - timedelta(days=days)).isoformat()
    lines = ["## EVENTOS DA SEMANA", "", "```"]

    # BR: fatos relevantes primeiro, depois comunicados
    br_fr = _rows(
        DB_BR,
        """SELECT e.event_date, e.ticker, e.summary, c.is_holding
           FROM events e LEFT JOIN companies c ON e.ticker=c.ticker
           WHERE e.source='cvm' AND e.kind='fato_relevante' AND e.event_date >= ?
           ORDER BY e.event_date DESC, c.is_holding DESC, e.ticker""",
        (since,),
    )
    if br_fr:
        lines.append(">BR FATOS RELEVANTES:")
        for d, tk, summ, is_h in br_fr[:15]:
            flag = "*" if is_h else " "
            summ_short = (summ or "")[:60].replace("\n", " ")
            lines.append(f" {flag} {d}  {tk:<6} | {summ_short}")
        if len(br_fr) > 15:
            lines.append(f"   (+{len(br_fr) - 15} mais)")
        lines.append("")

    # US: 8-K prioritários
    us_8k = _rows(
        DB_US,
        """SELECT e.event_date, e.ticker, e.summary, c.is_holding
           FROM events e LEFT JOIN companies c ON e.ticker=c.ticker
           WHERE e.source='sec' AND e.kind='8-K' AND e.event_date >= ?
           ORDER BY e.event_date DESC, c.is_holding DESC, e.ticker""",
        (since,),
    )
    us_prio = [r for r in us_8k if _is_priority_sec(r[2])]
    if us_prio:
        lines.append(">US 8-K PRIORITARIOS (itens 1.01, 2.01, 3.03, 5.02, 8.01):")
        for d, tk, summ, is_h in us_prio[:15]:
            flag = "*" if is_h else " "
            summ_short = (summ or "").replace("8-K | ", "")[:60]
            lines.append(f" {flag} {d}  {tk:<6} | {summ_short}")
        if len(us_prio) > 15:
            lines.append(f"   (+{len(us_prio) - 15} mais)")
        lines.append("")

    # US: 10-K / 10-Q recentes
    us_annual = _rows(
        DB_US,
        """SELECT e.event_date, e.ticker, e.kind, c.is_holding
           FROM events e LEFT JOIN companies c ON e.ticker=c.ticker
           WHERE e.source='sec' AND e.kind IN ('10-K','10-Q','20-F') AND e.event_date >= ?
           ORDER BY e.event_date DESC, c.is_holding DESC, e.ticker""",
        (since,),
    )
    if us_annual:
        lines.append(">US RESULTADOS (10-K / 10-Q / 20-F):")
        for d, tk, kind, is_h in us_annual[:10]:
            flag = "*" if is_h else " "
            lines.append(f" {flag} {d}  {tk:<6} | {kind}")
        lines.append("")

    if not (br_fr or us_prio or us_annual):
        lines.append(">NENHUM EVENTO DE INTERESSE NA JANELA.")
        lines.append("")

    lines.append("  * = ticker nas tuas holdings")
    lines.append("```")
    lines.append("")
    return lines


def scoring_block() -> list[str]:
    lines = ["## SCORING — ULTIMO RUN", "", "```"]

    for db_path, market in ((DB_BR, "BR"), (DB_US, "US")):
        with sqlite3.connect(db_path) as c:
            last = c.execute("SELECT MAX(run_date) FROM scores").fetchone()[0]
            if not last:
                continue
            rows = c.execute(
                """SELECT s.ticker, s.score, s.passes_screen, c.is_holding, c.name
                   FROM scores s LEFT JOIN companies c ON s.ticker=c.ticker
                   WHERE s.run_date=? ORDER BY s.score DESC, s.ticker""",
                (last,),
            ).fetchall()
        if not rows:
            continue

        passes = [r for r in rows if r[2]]
        top_fails = [r for r in rows if not r[2]][:5]

        lines.append(f">{market}  RUN_DATE: {last}")
        if passes:
            lines.append(f"  PASSES SCREEN ({len(passes)}):")
            for tk, sc, _, is_h, _ in passes:
                flag = "*" if is_h else " "
                lines.append(f"   {flag} {tk:<7} score={sc:.2f}")
        else:
            lines.append("  NENHUM TICKER PASSA SCREEN COMPLETO.")
        if top_fails:
            lines.append(f"  TOP 5 NEAR-MISS:")
            for tk, sc, _, is_h, _ in top_fails:
                flag = "*" if is_h else " "
                lines.append(f"   {flag} {tk:<7} score={sc:.2f}")
        lines.append("")

    lines.append("```")
    lines.append("")
    return lines


def holdings_block() -> list[str]:
    lines = ["## HOLDINGS — SNAPSHOT", "", "```"]

    for db_path, market, ccy in ((DB_BR, "BR", "R$"), (DB_US, "US", "US$")):
        with sqlite3.connect(db_path) as c:
            rows = c.execute(
                """SELECT c.ticker, c.name,
                          (SELECT close FROM prices p WHERE p.ticker=c.ticker ORDER BY date DESC LIMIT 1) AS px,
                          (SELECT date  FROM prices p WHERE p.ticker=c.ticker ORDER BY date DESC LIMIT 1) AS dt
                   FROM companies c
                   WHERE c.is_holding=1
                   ORDER BY c.ticker""",
            ).fetchall()
        if not rows:
            continue
        lines.append(f">{market}  HOLDINGS:")
        lines.append(f"  {'TICKER':<7} {'PRICE':>10}  {'DATE':<10}  NAME")
        for tk, name, px, dt in rows:
            px_s = f"{px:>10.2f}" if px is not None else f"{'--':>10}"
            dt_s = dt or "--"
            nm = (name or "")[:28]
            lines.append(f"  {tk:<7} {px_s}  {dt_s:<10}  {nm}")
        lines.append("")

    lines.append("```")
    lines.append("")
    return lines


def footer_block() -> list[str]:
    return [
        "```",
        "================================================================",
        "  * = ticker nas holdings",
        "  SOURCES  : B3 (yfinance + brapi + Status Invest)",
        "             NYSE (yfinance) + SEC EDGAR",
        "             BCB SGS (macro)  |  CVM IPE (fatos relevantes)",
        ">END OF TRANSMISSION.",
        "================================================================",
        "```",
    ]


def md_to_html(md: str, title: str) -> str:
    """Render minimalista: envolve em <pre> com CSS Fallout. Não parseia
    markdown a sério, só aplica style global e deixa o texto cru."""
    import html as html_mod
    escaped = html_mod.escape(md)
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{
    background: #000;
    color: #20ff20;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
    padding: 24px;
    text-shadow: 0 0 2px #20ff20;
  }}
  pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
  }}
  h1, h2, h3 {{
    color: #39ff14;
    border-bottom: 1px solid #155;
    padding-bottom: 2px;
    text-shadow: 0 0 4px #39ff14;
  }}
  a {{ color: #7fff7f; }}
  a:visited {{ color: #4faf4f; }}
</style>
</head>
<body>
<pre>{escaped}</pre>
</body>
</html>
"""


def run(days: int = 7, write_html: bool = True) -> Path:
    today = date.today()
    lines: list[str] = []
    lines.extend(header_block(today, days))
    lines.extend(events_block(today, days))
    lines.extend(scoring_block())
    lines.extend(holdings_block())
    lines.extend(footer_block())
    md = "\n".join(lines)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    md_path = REPORT_DIR / f"weekly_{today.isoformat()}.md"
    md_path.write_text(md, encoding="utf-8")

    html_path = None
    if write_html:
        html_path = REPORT_DIR / f"weekly_{today.isoformat()}.html"
        html_path.write_text(md_to_html(md, f"Weekly {today.isoformat()}"), encoding="utf-8")

    print(f"[ok] {md_path}")
    if html_path:
        print(f"[ok] {html_path}")
    return md_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--no-html", action="store_true")
    args = ap.parse_args()
    run(days=args.days, write_html=not args.no_html)


if __name__ == "__main__":
    main()
