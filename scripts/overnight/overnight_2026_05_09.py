"""Overnight 2026-05-09 — audit + research + synthesis.

Sequential, idempotent, read-only writes only to obsidian_vault/Bibliotheca/.
Memory rule: zero writes to data/ (user authorized for enrichment + audit only;
backfill of missing fundamentals/prices needs explicit user approval).

Blocks:
    A · Data coverage audit (10y per ticker, holdings + watchlist)
    B · Bloomberg/Voila terminal research (Tavily ~15 q)
    C · Compact widget research (Tavily ~10 q)
    D · Synthesis brief (Qwen 14B local — descriptive, no calls)

Run:
    python scripts/overnight/overnight_2026_05_09.py [--block A|B|C|D|all]

Outputs:
    obsidian_vault/Bibliotheca/Data_Coverage_Audit_2026-05-09.md
    obsidian_vault/Bibliotheca/Bloomberg_Terminal_Patterns_2026-05-09.md
    obsidian_vault/Bibliotheca/Compact_Widgets_Patterns_2026-05-09.md
    obsidian_vault/Bibliotheca/Phase_NN_Mission_Control_Roadmap_2026-05-09.md
    obsidian_vault/Bibliotheca/Overnight_Plan_2026-05-09.md (run log)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
import traceback
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
VAULT = ROOT / "obsidian_vault" / "Bibliotheca"
LOG = ROOT / "logs" / "overnight_2026-05-09.log"

DATE_TAG = "2026-05-09"
TODAY = date.today()
TEN_YEARS_AGO = date(TODAY.year - 10, TODAY.month, TODAY.day)


def log(msg: str) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ======================================================================
# BLOCK A · Data coverage audit
# ======================================================================

def _load_universe() -> dict[str, list[dict]]:
    """Returns {br: [...], us: [...]} of {ticker, name, is_holding, kind}."""
    import yaml
    universe_yaml = ROOT / "config" / "universe.yaml"
    kings_yaml = ROOT / "config" / "kings_aristocrats.yaml"
    out = {"br": [], "us": []}

    try:
        u = yaml.safe_load(universe_yaml.read_text(encoding="utf-8"))
        for market in ("br", "us"):
            section = u.get(market, {}) or {}
            holdings = section.get("holdings", {}) or {}
            for kind in ("stocks", "fiis", "etfs"):
                for entry in holdings.get(kind, []) or []:
                    out[market].append({
                        "ticker": entry["ticker"],
                        "name": entry.get("name", entry["ticker"]),
                        "is_holding": True,
                        "kind": kind,
                    })
            wl = section.get("watchlist", {}) or {}
            for kind in ("stocks", "fiis", "etfs"):
                for entry in wl.get(kind, []) or []:
                    out[market].append({
                        "ticker": entry["ticker"],
                        "name": entry.get("name", entry["ticker"]),
                        "is_holding": False,
                        "kind": kind,
                    })
    except Exception as e:
        log(f"WARN universe.yaml load failed: {e}")

    # Kings/Aristocrats — usually all US.
    # Schema: top-level `tickers: [...]` with each entry {ticker, name, kind, ...}
    try:
        if kings_yaml.exists():
            k = yaml.safe_load(kings_yaml.read_text(encoding="utf-8"))
            entries = k.get("tickers", []) or []
            seen = {e["ticker"] for e in out["us"]}
            for entry in entries:
                tk = entry.get("ticker")
                if not tk or tk in seen:
                    continue
                out["us"].append({
                    "ticker": tk,
                    "name": entry.get("name", tk),
                    "is_holding": False,
                    "kind": entry.get("kind", "king_aristocrat"),
                })
                seen.add(tk)
    except Exception as e:
        log(f"WARN kings_aristocrats load failed: {e}")

    return out


def _coverage_for_ticker(conn: sqlite3.Connection, ticker: str) -> dict:
    """Return coverage stats per category × year (last 10y)."""
    out = {"prices": {}, "dividends": {}, "fundamentals": {}, "events": {}}

    for yr in range(TEN_YEARS_AGO.year, TODAY.year + 1):
        start = f"{yr}-01-01"
        end = f"{yr}-12-31"

        # Prices — daily count (target ~252/yr)
        try:
            c = conn.execute(
                "SELECT COUNT(*) FROM prices WHERE ticker=? AND date BETWEEN ? AND ?",
                (ticker, start, end),
            ).fetchone()
            out["prices"][yr] = c[0] if c else 0
        except sqlite3.OperationalError:
            out["prices"][yr] = None

        # Dividends — count of payments
        try:
            c = conn.execute(
                "SELECT COUNT(*) FROM dividends WHERE ticker=? AND ex_date BETWEEN ? AND ?",
                (ticker, start, end),
            ).fetchone()
            out["dividends"][yr] = c[0] if c else 0
        except sqlite3.OperationalError:
            out["dividends"][yr] = None

        # Fundamentals — quarterly snapshots (target 4/yr)
        try:
            c = conn.execute(
                "SELECT COUNT(*) FROM fundamentals WHERE ticker=? AND period_end BETWEEN ? AND ?",
                (ticker, start, end),
            ).fetchone()
            out["fundamentals"][yr] = c[0] if c else 0
        except sqlite3.OperationalError:
            out["fundamentals"][yr] = None

        # Events / filings (8-K, 10-K, fato_relevante etc.)
        try:
            c = conn.execute(
                "SELECT COUNT(*) FROM events WHERE ticker=? AND event_date BETWEEN ? AND ?",
                (ticker, start, end),
            ).fetchone()
            out["events"][yr] = c[0] if c else 0
        except sqlite3.OperationalError:
            out["events"][yr] = None

    # Income statement / balance sheet — check deep_fundamentals if present
    has_deep = False
    try:
        r = conn.execute(
            "SELECT COUNT(*) FROM deep_fundamentals WHERE ticker=?",
            (ticker,),
        ).fetchone()
        has_deep = bool(r and r[0] > 0)
        out["deep_rows_total"] = r[0] if r else 0
    except sqlite3.OperationalError:
        out["deep_rows_total"] = None

    out["has_deep_fundamentals"] = has_deep
    return out


def _grade(count: int | None, target: int) -> str:
    if count is None: return "—"
    if count == 0: return "🔴"
    if count >= target * 0.85: return "🟢"
    if count >= target * 0.4: return "🟡"
    return "🔴"


def block_a_data_audit():
    log("BLOCK A · Data coverage audit — START")
    universe = _load_universe()
    total_tk = len(universe["br"]) + len(universe["us"])
    log(f"  universe: {len(universe['br'])} BR + {len(universe['us'])} US = {total_tk}")

    out_lines: list[str] = []
    out_lines.append("---")
    out_lines.append("type: data_coverage_audit")
    out_lines.append(f"date: {DATE_TAG}")
    out_lines.append(f"window: {TEN_YEARS_AGO.year}–{TODAY.year}")
    out_lines.append(f"universe_total: {total_tk}")
    out_lines.append("status: read_only_audit")
    out_lines.append("tags: [data_coverage, audit, phase_nn]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append("# Data Coverage Audit — 10 anos")
    out_lines.append("")
    out_lines.append(f"> Janela: {TEN_YEARS_AGO} → {TODAY}. Universe completo: holdings + watchlist + Kings/Aristocrats.")
    out_lines.append("")
    out_lines.append("## Legenda")
    out_lines.append("")
    out_lines.append("- 🟢 cobertura ≥ 85% do target")
    out_lines.append("- 🟡 cobertura 40–85%")
    out_lines.append("- 🔴 cobertura < 40% ou sem dados")
    out_lines.append("- — tabela ausente")
    out_lines.append("")
    out_lines.append("## Targets por categoria (anuais)")
    out_lines.append("")
    out_lines.append("| Categoria | Target/ano | Notas |")
    out_lines.append("|---|---|---|")
    out_lines.append("| Prices | 252 | dias úteis |")
    out_lines.append("| Dividends | 1–4 | varia por ticker; 0 é OK para growth |")
    out_lines.append("| Fundamentals | 4 | quarterly snapshots |")
    out_lines.append("| Events / Filings | 4–12 | 10-K + 4×10-Q + 8-Ks |")
    out_lines.append("")

    # Aggregate stats per market
    summary: dict[str, dict[str, dict]] = {"br": {}, "us": {}}
    gaps: list[dict] = []

    for market, db_path in [("br", DB_BR), ("us", DB_US)]:
        if not db_path.exists():
            log(f"  {market}: DB missing")
            continue
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        out_lines.append(f"## {market.upper()} · {len(universe[market])} tickers")
        out_lines.append("")
        out_lines.append("| Ticker | Holding | Kind | Prices 10y | Divs 10y | Fund 10y | Events 10y | Deep | Status |")
        out_lines.append("|---|---|---|---|---|---|---|---|---|")

        for entry in sorted(universe[market], key=lambda e: (not e["is_holding"], e["ticker"])):
            tk = entry["ticker"]
            try:
                cov = _coverage_for_ticker(conn, tk)
            except Exception as e:
                log(f"    {tk}: ERROR {e}")
                continue

            prices_total = sum(v for v in cov["prices"].values() if v is not None)
            divs_total = sum(v for v in cov["dividends"].values() if v is not None)
            fund_total = sum(v for v in cov["fundamentals"].values() if v is not None)
            events_total = sum(v for v in cov["events"].values() if v is not None)

            # Grade overall: green if all categories are green
            target_prices = 10 * 252
            grade_prices = _grade(prices_total, target_prices)
            grade_fund = _grade(fund_total, 10 * 4)  # 4 quarters/yr
            grade_events = _grade(events_total, 10 * 4)
            grade_divs = "🟢" if divs_total > 0 else ("—" if divs_total == 0 and not entry["is_holding"] else "🔴")
            deep = "🟢" if cov["has_deep_fundamentals"] else "🔴"

            # Overall status
            if grade_prices == "🟢" and grade_fund != "🔴":
                overall = "🟢 OK"
            elif grade_prices == "🔴":
                overall = "🔴 NO_PRICES"
            elif grade_fund == "🔴":
                overall = "🟡 NO_FUNDAMENTALS"
            else:
                overall = "🟡 PARTIAL"

            holding_mark = "✓" if entry["is_holding"] else ""
            out_lines.append(
                f"| {tk} | {holding_mark} | {entry['kind']} | {grade_prices} {prices_total} | "
                f"{grade_divs} {divs_total} | {grade_fund} {fund_total} | "
                f"{grade_events} {events_total} | {deep} | {overall} |",
            )

            summary[market][tk] = {
                "is_holding": entry["is_holding"],
                "kind": entry["kind"],
                "prices_total": prices_total,
                "divs_total": divs_total,
                "fund_total": fund_total,
                "events_total": events_total,
                "has_deep": cov["has_deep_fundamentals"],
                "overall": overall,
            }

            # Track gaps for summary
            if grade_prices == "🔴":
                gaps.append({"ticker": tk, "market": market, "kind": "prices_missing"})
            if grade_fund == "🔴":
                gaps.append({"ticker": tk, "market": market, "kind": "fundamentals_missing"})
            if entry["is_holding"] and grade_divs == "🔴":
                gaps.append({"ticker": tk, "market": market, "kind": "dividends_missing_holding"})

        conn.close()
        out_lines.append("")

    # Gaps summary
    out_lines.append("## Gaps detectados")
    out_lines.append("")
    if not gaps:
        out_lines.append("Nenhum gap crítico detectado. ✨")
    else:
        # Bucket
        by_kind: dict[str, list[str]] = {}
        for g in gaps:
            key = g["kind"]
            by_kind.setdefault(key, []).append(f"{g['ticker']} ({g['market']})")
        for kind, items in by_kind.items():
            out_lines.append(f"### {kind} ({len(items)} tickers)")
            out_lines.append("")
            out_lines.append(", ".join(items))
            out_lines.append("")

    out_lines.append("## Sugestões de backfill (carecem de aprovação do user)")
    out_lines.append("")
    out_lines.append("| Gap | Fetcher sugerido | Custo estimado |")
    out_lines.append("|---|---|---|")
    out_lines.append("| prices_missing (BR) | `python fetchers/yfinance_fetcher.py --tickers ... --period max` | ~10s/ticker |")
    out_lines.append("| prices_missing (US) | `python fetchers/yfinance_fetcher.py --tickers ... --period max` | ~10s/ticker |")
    out_lines.append("| fundamentals_missing | `python fetchers/yf_deep_fundamentals.py --ticker X` | ~30s/ticker, yfinance.info |")
    out_lines.append("| events_missing (BR) | `python -m monitors.cvm_monitor --backfill` | tem rate limit |")
    out_lines.append("| events_missing (US) | `python -m monitors.sec_monitor --ticker X` | EDGAR rate-limited |")
    out_lines.append("")

    # Write JSON sidecar for downstream block D
    json_path = VAULT / f"data_coverage_summary_{DATE_TAG}.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Write report
    out_path = VAULT / f"Data_Coverage_Audit_{DATE_TAG}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    log(f"BLOCK A · OK · wrote {out_path}")
    log(f"  {len(gaps)} gaps tracked. JSON sidecar: {json_path}")


# ======================================================================
# BLOCK B · Bloomberg / Voila terminal research (Tavily-driven)
# ======================================================================

BLOOMBERG_QUERIES = [
    "Bloomberg Terminal layout principles screen panels grid design",
    "Bloomberg Terminal monitor configuration multi-pane workflow",
    "Bloomberg Terminal command shortcuts function panels",
    "FactSet vs Bloomberg Terminal user interface comparison",
    "Refinitiv Eikon Workspace layout pattern screen",
    "S&P Capital IQ dashboard layout pattern",
    "Bloomberg Terminal heatmap watchlist mini chart",
    "Bloomberg Anywhere mobile app condensed UI patterns",
    "trader workstation multiple panel arrangement best practices",
    "Voila Jupyter notebook dashboard layout pattern",
    "professional financial dashboard micro-station design",
    "fintech dashboard density Bloomberg-style data table",
    "Bloomberg orange black color palette data visualization",
    "real-time financial dashboard tile layout pattern",
    "Hedge fund analyst desktop layout workflow",
]


def _tavily_search_safe(query: str) -> dict | None:
    """Wrap autoresearch.search with try/except so one bad query doesn't kill the block."""
    try:
        sys.path.insert(0, str(ROOT))
        from agents.autoresearch import search
        r = search(query, max_results=5, search_depth="basic")
        return {
            "query": query,
            "answer": r.answer,
            # TavilyHit fields: title, url, content, score, published_date
            "results": [{"title": h.title, "url": h.url, "snippet": (h.content or "")[:300]} for h in r.results],
            "error": r.error,
        }
    except Exception as e:
        return {"query": query, "answer": None, "results": [], "error": f"exception: {e}"}


def block_b_bloomberg_research():
    log("BLOCK B · Bloomberg/Voila research — START")
    out_lines: list[str] = []
    out_lines.append("---")
    out_lines.append("type: design_research")
    out_lines.append(f"date: {DATE_TAG}")
    out_lines.append("topic: bloomberg_terminal_voila_micro_station_patterns")
    out_lines.append("source: tavily")
    out_lines.append("tags: [research, design, mission_control, phase_nn, layout_patterns]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append("# Bloomberg / Voila Terminal — Research Patterns")
    out_lines.append("")
    out_lines.append("> Discovery para informar a evolução do Workbench do Mission Control. ")
    out_lines.append("> Foco: como Bloomberg Terminal e ferramentas profissionais organizam ")
    out_lines.append("> múltiplos painéis num mesmo workspace ('micro-station').")
    out_lines.append("")
    out_lines.append("## Queries executadas")
    out_lines.append("")
    out_lines.append(f"Total: {len(BLOOMBERG_QUERIES)} queries Tavily.")
    out_lines.append("")

    all_hits: list[dict] = []
    for i, q in enumerate(BLOOMBERG_QUERIES, 1):
        log(f"  Q{i}/{len(BLOOMBERG_QUERIES)}: {q[:60]}...")
        r = _tavily_search_safe(q)
        if r:
            all_hits.append(r)
        time.sleep(2)  # gentle rate-limiting

    out_lines.append("## Resultados por query")
    out_lines.append("")

    for r in all_hits:
        out_lines.append(f"### `{r['query']}`")
        out_lines.append("")
        if r.get("error"):
            out_lines.append(f"> ⚠️ {r['error']}")
            out_lines.append("")
            continue
        if r.get("answer"):
            out_lines.append("**Tavily synthesis**:")
            out_lines.append("")
            out_lines.append(f"> {r['answer']}")
            out_lines.append("")
        out_lines.append("**Top results**:")
        out_lines.append("")
        for hit in r.get("results", [])[:5]:
            out_lines.append(f"- [{hit['title']}]({hit['url']})")
            out_lines.append(f"  > {hit['snippet']}")
        out_lines.append("")

    out_lines.append("## Padrões a remixar (preliminar — afinar no brief D)")
    out_lines.append("")
    out_lines.append("- Multi-pane com tab-strip por painel (Bloomberg)")
    out_lines.append("- Header bar com command line / global search (Bloomberg cmd)")
    out_lines.append("- Watchlist mini-chart inline em vez de cell number (sparkline)")
    out_lines.append("- Click-to-zoom: pane minimizado expande full-screen")
    out_lines.append("- Synced focus: 1 ticker → 4 panes simultâneos (price, fundamentals, news, peers)")
    out_lines.append("")

    out_path = VAULT / f"Bloomberg_Terminal_Patterns_{DATE_TAG}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    log(f"BLOCK B · OK · wrote {out_path}")

    # Sidecar JSON for D
    json_path = VAULT / f"bloomberg_research_{DATE_TAG}.json"
    json_path.write_text(json.dumps(all_hits, indent=2), encoding="utf-8")


# ======================================================================
# BLOCK C · Compact widget research (Tavily-driven)
# ======================================================================

WIDGET_QUERIES = [
    "Charles Schwab next dividends widget design dashboard",
    "JPMorgan Chase Self-Directed dashboard upcoming dividends panel",
    "Robinhood dividend calendar mini card design",
    "Interactive Brokers IBKR dividend events widget",
    "compact dashboard widget upcoming events small card design",
    "Schwab personal banking filings notifications panel",
    "broker app upcoming earnings card design pattern",
    "fintech dashboard mini calendar component design",
    "Apple Stocks app dividend history compact display",
    "Yahoo Finance ETF dashboard upcoming events tile",
]


def block_c_widget_research():
    log("BLOCK C · Compact widget research — START")
    out_lines: list[str] = []
    out_lines.append("---")
    out_lines.append("type: design_research")
    out_lines.append(f"date: {DATE_TAG}")
    out_lines.append("topic: compact_dividend_filing_widgets")
    out_lines.append("source: tavily")
    out_lines.append("tags: [research, design, mission_control, phase_nn, widgets]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append("# Compact Widgets — Dividend & Filings Mini-Cards")
    out_lines.append("")
    out_lines.append("> Como Schwab / JPM / Robinhood / IB / Apple Stocks / Yahoo Finance ")
    out_lines.append("> mostram 'próximos dividendos' e 'próximos filings' em pouco espaço, ")
    out_lines.append("> sem perder utilidade.")
    out_lines.append("")
    out_lines.append(f"Total queries: {len(WIDGET_QUERIES)}.")
    out_lines.append("")

    all_hits: list[dict] = []
    for i, q in enumerate(WIDGET_QUERIES, 1):
        log(f"  Q{i}/{len(WIDGET_QUERIES)}: {q[:60]}...")
        r = _tavily_search_safe(q)
        if r:
            all_hits.append(r)
        time.sleep(2)

    out_lines.append("## Resultados")
    out_lines.append("")

    for r in all_hits:
        out_lines.append(f"### `{r['query']}`")
        out_lines.append("")
        if r.get("error"):
            out_lines.append(f"> ⚠️ {r['error']}")
            out_lines.append("")
            continue
        if r.get("answer"):
            out_lines.append(f"> {r['answer']}")
            out_lines.append("")
        for hit in r.get("results", [])[:5]:
            out_lines.append(f"- [{hit['title']}]({hit['url']})")
            out_lines.append(f"  > {hit['snippet']}")
        out_lines.append("")

    out_lines.append("## Variants preliminares (a explorar amanhã)")
    out_lines.append("")
    out_lines.append("- **V1: Mini-card timeline** — 5 próximos dividendos como linha horizontal compacta")
    out_lines.append("- **V2: Stacked rows** — lista vertical com data + ticker + amount, similar Schwab")
    out_lines.append("- **V3: Hexagonal grid** — 1 ticker por hex, dia do mês como label")
    out_lines.append("")

    out_path = VAULT / f"Compact_Widgets_Patterns_{DATE_TAG}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    log(f"BLOCK C · OK · wrote {out_path}")

    json_path = VAULT / f"widgets_research_{DATE_TAG}.json"
    json_path.write_text(json.dumps(all_hits, indent=2), encoding="utf-8")


# ======================================================================
# BLOCK D · Synthesis brief
# ======================================================================

def block_d_synthesis():
    log("BLOCK D · Synthesis brief — START")

    summary_path = VAULT / f"data_coverage_summary_{DATE_TAG}.json"
    bloomberg_path = VAULT / f"bloomberg_research_{DATE_TAG}.json"
    widgets_path = VAULT / f"widgets_research_{DATE_TAG}.json"

    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    bloomberg = json.loads(bloomberg_path.read_text(encoding="utf-8")) if bloomberg_path.exists() else []
    widgets = json.loads(widgets_path.read_text(encoding="utf-8")) if widgets_path.exists() else []

    # Aggregate audit stats
    n_tickers = sum(len(s) for s in summary.values()) if summary else 0
    n_holdings = sum(1 for m in summary.values() for v in m.values() if v.get("is_holding"))
    n_red_prices = sum(1 for m in summary.values() for v in m.values() if "NO_PRICES" in v.get("overall", ""))
    n_red_fund = sum(1 for m in summary.values() for v in m.values() if "NO_FUNDAMENTALS" in v.get("overall", ""))

    out_lines: list[str] = []
    out_lines.append("---")
    out_lines.append("type: design_brief")
    out_lines.append(f"date: {DATE_TAG}")
    out_lines.append("phase: NN")
    out_lines.append("status: draft_overnight_synthesis")
    out_lines.append("tags: [phase_nn, mission_control, roadmap, design_brief]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append("# Phase NN · Mission Control Roadmap (overnight synthesis)")
    out_lines.append("")
    out_lines.append("> Junta os 3 outputs da noite (audit + Bloomberg research + widget research) ")
    out_lines.append("> num roadmap concreto. Assina-se tudo amanhã com o user antes de codar.")
    out_lines.append("")
    out_lines.append("## Estado do mundo (audit)")
    out_lines.append("")
    out_lines.append(f"- Universe seguido: **{n_tickers}** tickers")
    out_lines.append(f"- Holdings activas: **{n_holdings}**")
    out_lines.append(f"- Tickers sem prices 10y: **{n_red_prices}**")
    out_lines.append(f"- Tickers sem fundamentals 10y: **{n_red_fund}**")
    out_lines.append("")
    out_lines.append("Detalhe completo: `Data_Coverage_Audit_2026-05-09.md`")
    out_lines.append("")

    out_lines.append("## Insights research (Bloomberg + Widgets)")
    out_lines.append("")
    out_lines.append(f"- Queries Bloomberg/Voila: **{len(bloomberg)}**")
    out_lines.append(f"- Queries widgets: **{len(widgets)}**")
    out_lines.append("")
    out_lines.append("Detalhes:")
    out_lines.append("- `Bloomberg_Terminal_Patterns_2026-05-09.md`")
    out_lines.append("- `Compact_Widgets_Patterns_2026-05-09.md`")
    out_lines.append("")

    out_lines.append("## Próximos sprints propostos")
    out_lines.append("")
    out_lines.append("### Sprint NN.1 · Chart system v2")
    out_lines.append("")
    out_lines.append("- Substituir SVG raw por Recharts (já em package.json)")
    out_lines.append("- Hover crosshair vertical + tooltip flutuante com valores de todos os tickers")
    out_lines.append("- Período zoom + pan")
    out_lines.append("- Responsive verdadeiro via `<ResponsiveContainer>`")
    out_lines.append("- Aplicar a: Compare tab + DRIP charts + ticker tearsheet price line")
    out_lines.append("")
    out_lines.append("### Sprint NN.2 · Micro-station layout")
    out_lines.append("")
    out_lines.append("- Reorganizar o Workbench em 4 panes simultâneos sincronizados pelo focus-ticker")
    out_lines.append("- Top: big chart")
    out_lines.append("- Middle: positions table compacta")
    out_lines.append("- Right rail: mini-cards 'next dividends' + 'next filings'")
    out_lines.append("- Inspirado em padrões Bloomberg detectados na noite (ver research)")
    out_lines.append("")
    out_lines.append("### Sprint NN.3 · /stocks watchlist expansion")
    out_lines.append("")
    out_lines.append("- Mostrar TODA a watchlist (~108 tickers) e Kings/Aristocrats (~87)")
    out_lines.append("- Não só holdings activas")
    out_lines.append("- Filter chip 'Holdings only / Watchlist / All'")
    out_lines.append("")
    out_lines.append("### Sprint NN.4 · Data backfill (carece tua aprovação)")
    out_lines.append("")
    out_lines.append("Baseado nos gaps do audit:")
    out_lines.append(f"- Backfill prices p/ {n_red_prices} tickers via yfinance --period max")
    out_lines.append(f"- Backfill fundamentals p/ {n_red_fund} tickers via yf_deep_fundamentals")
    out_lines.append("- CVM/SEC events para holdings sem cobertura events")
    out_lines.append("")
    out_lines.append("**Custo estimado**: 30–60 min de runtime, write ao `data/`. **Precisa tua aprovação.**")
    out_lines.append("")

    out_lines.append("## Decisões pendentes para o user")
    out_lines.append("")
    out_lines.append("- [ ] Aprovar chart system v2 com Recharts? (alternativa: Visx, Plotly)")
    out_lines.append("- [ ] Aprovar layout micro-station 4-pane? (vou trazer 3 mockups ASCII)")
    out_lines.append("- [ ] Aprovar /stocks watchlist expansion?")
    out_lines.append("- [ ] Aprovar backfill priorities (decidir quais gaps fechar)?")
    out_lines.append("")

    out_path = VAULT / f"Phase_NN_Mission_Control_Roadmap_{DATE_TAG}.md"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    log(f"BLOCK D · OK · wrote {out_path}")


# ======================================================================
# Run-log writer
# ======================================================================

def write_run_log(blocks_run: list[str], started: datetime, finished: datetime, errors: list[str]):
    out_lines: list[str] = []
    out_lines.append("---")
    out_lines.append("type: overnight_run_log")
    out_lines.append(f"date: {DATE_TAG}")
    out_lines.append(f"started: {started.isoformat(timespec='seconds')}")
    out_lines.append(f"finished: {finished.isoformat(timespec='seconds')}")
    out_lines.append(f"duration_min: {round((finished-started).total_seconds()/60, 1)}")
    out_lines.append(f"blocks: {','.join(blocks_run)}")
    out_lines.append(f"errors: {len(errors)}")
    out_lines.append("tags: [overnight, run_log]")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append(f"# Overnight Run Log · {DATE_TAG}")
    out_lines.append("")
    out_lines.append(f"Iniciado: {started}")
    out_lines.append(f"Terminado: {finished}")
    out_lines.append(f"Duração: {round((finished-started).total_seconds()/60, 1)} min")
    out_lines.append(f"Blocos corridos: {', '.join(blocks_run)}")
    out_lines.append("")
    out_lines.append("## Outputs gerados")
    out_lines.append("")
    for f in sorted(VAULT.glob(f"*{DATE_TAG}*")):
        if f.suffix == ".md":
            out_lines.append(f"- [[{f.stem}]]")
    out_lines.append("")
    if errors:
        out_lines.append("## Erros")
        out_lines.append("")
        for e in errors:
            out_lines.append(f"```")
            out_lines.append(e)
            out_lines.append(f"```")
        out_lines.append("")
    out_lines.append(f"Log completo: `{LOG.relative_to(ROOT)}`")
    (VAULT / f"Overnight_Plan_{DATE_TAG}.md").write_text("\n".join(out_lines), encoding="utf-8")


# ======================================================================
# Main
# ======================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", choices=["A", "B", "C", "D", "all"], default="all")
    args = parser.parse_args()

    started = datetime.now()
    blocks_run: list[str] = []
    errors: list[str] = []

    blocks = ["A", "B", "C", "D"] if args.block == "all" else [args.block]

    for b in blocks:
        try:
            if b == "A": block_a_data_audit(); blocks_run.append("A")
            elif b == "B": block_b_bloomberg_research(); blocks_run.append("B")
            elif b == "C": block_c_widget_research(); blocks_run.append("C")
            elif b == "D": block_d_synthesis(); blocks_run.append("D")
        except Exception as e:
            tb = traceback.format_exc()
            log(f"BLOCK {b} FAILED: {e}\n{tb}")
            errors.append(f"BLOCK {b}:\n{tb}")

    finished = datetime.now()
    write_run_log(blocks_run, started, finished, errors)
    log(f"OVERNIGHT DONE · blocks={blocks_run} · errors={len(errors)} · duration={round((finished-started).total_seconds()/60,1)}min")


if __name__ == "__main__":
    main()
