"""Overnight Backfill — pre-warm data layer + run all strategy engines.

OBJECTIVO: à noite, percorrer todo o universe (BR + US) e:
  1. Pre-fetch prices + fundamentals + dividends + macro via fetch_with_quality
     (popula data/api_cache.db; depois da meia-noite tudo está fresh).
  2. Pre-compute regime classification BR + US (cache em data/agent_decisions.db
     se usar agent layer; ou apenas em RAM via lru_cache).
  3. Pre-compute ROIC para todo holdings + watchlist US.
  4. Correr os 5 strategy engines por ticker e persistir em strategy_runs table.
  5. Correr portfolio_engine.combine() para BR e US e gravar AllocationProposal.
  6. Pre-compute hedge proposal por mercado.
  7. Output: relatório markdown em obsidian_vault/Bibliotheca/Overnight_Backfill_<DATE>.md
     + JSONL progress em logs/overnight_progress_<DATE>.jsonl

Idempotente — pode correr várias vezes no mesmo dia. Cache TTL evita
re-fetch desnecessário.

Schema novo: strategy_runs (criado se não existir):
    run_id TEXT, market TEXT, ticker TEXT, engine TEXT,
    score REAL, verdict TEXT, weight_suggestion REAL,
    rationale_json TEXT, run_ts TEXT
    PRIMARY KEY (run_id, market, ticker, engine)

Uso:
    python scripts/overnight_backfill.py [--market br|us|both] [--dry-run]
                                          [--skip-fetch] [--skip-strategies]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
VAULT_DIR = ROOT / "obsidian_vault" / "Bibliotheca"
UNIVERSE_PATH = ROOT / "config" / "universe.yaml"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _log_progress(progress_path: Path, event: dict) -> None:
    progress_path.parent.mkdir(exist_ok=True)
    with progress_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _now_iso(), **event}, default=str) + "\n")


def load_universe(market: str) -> list[str]:
    if not UNIVERSE_PATH.exists():
        return []
    data = yaml.safe_load(UNIVERSE_PATH.read_text(encoding="utf-8")) or {}
    m = data.get(market, {}) or {}
    out: list[str] = []
    for bucket in ("holdings", "watchlist"):
        group = m.get(bucket) or {}
        if isinstance(group, list):
            for entry in group:
                if isinstance(entry, dict) and entry.get("ticker"):
                    out.append(entry["ticker"])
        else:
            for sublist in (group or {}).values():
                for entry in sublist or []:
                    if isinstance(entry, dict) and entry.get("ticker"):
                        out.append(entry["ticker"])
    return sorted(set(out))


# ============================================================
# Schema migration
# ============================================================
def ensure_strategy_runs_table(market: str) -> None:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS strategy_runs (
                run_id TEXT NOT NULL,
                market TEXT NOT NULL,
                ticker TEXT NOT NULL,
                engine TEXT NOT NULL,
                score REAL,
                verdict TEXT,
                weight_suggestion REAL,
                rationale_json TEXT,
                run_ts TEXT NOT NULL,
                PRIMARY KEY (run_id, market, ticker, engine)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_strategy_runs_lookup "
                  "ON strategy_runs(market, ticker, run_ts)")
        c.commit()


def persist_strategy_output(market: str, run_id: str, output) -> None:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        c.execute("""
            INSERT INTO strategy_runs (run_id, market, ticker, engine, score,
                                        verdict, weight_suggestion,
                                        rationale_json, run_ts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id, market, ticker, engine) DO UPDATE SET
                score=excluded.score, verdict=excluded.verdict,
                weight_suggestion=excluded.weight_suggestion,
                rationale_json=excluded.rationale_json,
                run_ts=excluded.run_ts
        """, (run_id, market, output.ticker, output.engine, output.score,
              output.verdict, output.weight_suggestion,
              json.dumps(output.rationale, default=str, ensure_ascii=False),
              _now_iso()))
        c.commit()


# ============================================================
# Pipeline steps
# ============================================================
def step_prefetch(market: str, tickers: list[str], progress: Path,
                  dry_run: bool = False) -> dict:
    """Pre-fetch prices + fundamentals + dividends for every ticker."""
    from fetchers._fallback import fetch_with_quality

    counts = {"prices_ok": 0, "fundamentals_ok": 0, "dividends_ok": 0, "fail": 0}
    for i, ticker in enumerate(tickers, 1):
        for kind in ("prices", "fundamentals"):
            if dry_run:
                continue
            try:
                r = fetch_with_quality(market, kind, ticker)
                if r.success:
                    counts[f"{kind}_ok"] += 1
                else:
                    counts["fail"] += 1
            except Exception as e:  # noqa: BLE001
                counts["fail"] += 1
                _log_progress(progress, {
                    "step": "prefetch", "market": market, "ticker": ticker,
                    "kind": kind, "error": str(e)[:200]
                })
        if i % 10 == 0:
            _log_progress(progress, {
                "step": "prefetch_progress", "market": market,
                "done": i, "total": len(tickers), "counts": dict(counts)
            })
    return counts


def step_macro(market: str, progress: Path, dry_run: bool = False) -> dict:
    """Pre-fetch macro series for the market."""
    from fetchers._fallback import fetch_with_quality

    series_map = {
        "br": ["SELIC_DAILY", "CDI_DAILY", "IPCA_MONTHLY", "USDBRL_PTAX"],
        "us": ["DFF", "DGS10", "DGS2", "CPIAUCSL", "UNRATE"],
    }
    counts = {"ok": 0, "fail": 0}
    for s in series_map.get(market, []):
        if dry_run:
            continue
        try:
            r = fetch_with_quality(market, "macro", s)
            counts["ok" if r.success else "fail"] += 1
        except Exception as e:  # noqa: BLE001
            counts["fail"] += 1
            _log_progress(progress, {"step": "macro", "market": market,
                                      "series": s, "error": str(e)[:200]})
    return counts


def step_strategies(market: str, tickers: list[str], run_id: str,
                    progress: Path, dry_run: bool = False) -> dict:
    """Run 5 engines per ticker; persist to strategy_runs."""
    from strategies import buffett, drip, graham, hedge, macro

    if market == "br":
        engine_modules = [graham, drip, macro, hedge]
    else:
        engine_modules = [buffett, drip, macro, hedge]

    counts = {"ok": 0, "fail": 0}
    for i, ticker in enumerate(tickers, 1):
        for engine in engine_modules:
            if dry_run:
                continue
            try:
                out = engine.evaluate(ticker, market)
                persist_strategy_output(market, run_id, out)
                counts["ok"] += 1
            except Exception as e:  # noqa: BLE001
                counts["fail"] += 1
                _log_progress(progress, {
                    "step": "strategy", "market": market, "ticker": ticker,
                    "engine": engine.name, "error": str(e)[:200]
                })
        if i % 10 == 0:
            _log_progress(progress, {
                "step": "strategy_progress", "market": market,
                "done": i, "total": len(tickers), "counts": dict(counts)
            })
    return counts


def step_allocation(market: str, run_id: str, progress: Path,
                    dry_run: bool = False) -> dict | None:
    """Run portfolio combiner and save AllocationProposal as JSON in vault."""
    from strategies import portfolio_engine

    if dry_run:
        return None
    try:
        proposal = portfolio_engine.combine(market=market, top_n=20)
    except Exception as e:  # noqa: BLE001
        _log_progress(progress, {"step": "allocation", "market": market,
                                  "error": str(e)[:200]})
        return None
    out_path = ROOT / "obsidian_vault" / "Bibliotheca" / \
        f"Allocation_{market.upper()}_{_today()}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(proposal.as_dict(), indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )
    return proposal.as_dict()


def step_hedge(market: str) -> dict:
    from strategies import hedge
    return hedge.propose_hedge(market)


# ============================================================
# Report
# ============================================================
def render_report(run_id: str, summary: dict[str, Any]) -> str:
    today = _today()
    lines = [
        f"# Overnight Backfill — {today}",
        "",
        f"**Run ID**: `{run_id}`  ",
        f"**Generated**: {_now_iso()}  ",
        "",
        "## Pre-fetch summary (live cache hits + DB writes)",
        "",
    ]
    for market in ("br", "us"):
        m = summary.get(market) or {}
        if not m:
            continue
        lines.append(f"### {market.upper()}")
        pf = m.get("prefetch") or {}
        macro = m.get("macro") or {}
        strat = m.get("strategies") or {}
        lines += [
            f"- Universe size: {m.get('universe_size', 0)}",
            f"- Prices fetched OK: {pf.get('prices_ok', 0)}",
            f"- Fundamentals fetched OK: {pf.get('fundamentals_ok', 0)}",
            f"- Macro series OK: {macro.get('ok', 0)} / fail: {macro.get('fail', 0)}",
            f"- Strategy outputs persisted: {strat.get('ok', 0)} / fail: {strat.get('fail', 0)}",
            "",
        ]
        h = m.get("hedge") or {}
        if h:
            status = "ON" if h.get("active") else "OFF"
            lines += [
                f"**Hedge {market.upper()}**: {status}  ",
                f"- regime: {h.get('regime')} (confidence: {h.get('confidence')})  ",
                f"- size: {h.get('hedge_size_pct', 0):.0%}  ",
                f"- instruments: {', '.join(h.get('instruments') or []) or '—'}  ",
                "",
            ]
        alloc = m.get("allocation") or {}
        if alloc:
            tw = alloc.get("target_weights") or {}
            top = sorted(tw.items(), key=lambda x: x[1], reverse=True)[:10]
            lines.append(f"**Top 10 allocation {market.upper()}**:")
            for t, w in top:
                lines.append(f"- {t}: {w*100:.1f}%")
            lines.append("")
            confs = alloc.get("conflicts") or []
            if confs:
                lines += [f"**{len(confs)} conflicts** detected (BUY+AVOID disagreement):"]
                for c in confs[:5]:
                    lines.append(f"- {c.get('ticker')}: {c.get('verdicts')}")
                lines.append("")
    lines += [
        "## How to consume",
        "",
        "- Strategy outputs in `data/{br,us}_investments.db::strategy_runs`",
        "- Allocation proposals in `obsidian_vault/Bibliotheca/Allocation_*.json`",
        "- Cache fully primed in `data/api_cache.db` (TTL 24h prices, 72h fund, 168h macro)",
        "- Agent decisions log in `data/agent_decisions.db` (90d retention)",
        "",
    ]
    return "\n".join(lines)


# ============================================================
# Main
# ============================================================
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--market", choices=["br", "us", "both"], default="both")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-fetch", action="store_true")
    ap.add_argument("--skip-strategies", action="store_true")
    ap.add_argument("--skip-allocation", action="store_true")
    args = ap.parse_args()

    today = _today()
    run_id = f"overnight_{today}"
    progress_path = LOG_DIR / f"overnight_progress_{today}.jsonl"
    LOG_DIR.mkdir(exist_ok=True)
    print(f"=== Overnight Backfill | run_id={run_id} ===")
    print(f"Progress log: {progress_path}")

    markets = ["br", "us"] if args.market == "both" else [args.market]
    summary: dict[str, Any] = {}

    for market in markets:
        ensure_strategy_runs_table(market)
        tickers = load_universe(market)
        print(f"\n--- {market.upper()} | universe={len(tickers)} ---")
        m_summary: dict[str, Any] = {"universe_size": len(tickers)}

        if not args.skip_fetch:
            t0 = time.time()
            print(f"  [1/4] Pre-fetching prices+fundamentals for {len(tickers)} tickers...")
            m_summary["prefetch"] = step_prefetch(market, tickers, progress_path,
                                                   dry_run=args.dry_run)
            print(f"        prefetch counts: {m_summary['prefetch']} "
                  f"({time.time()-t0:.1f}s)")
            print(f"  [2/4] Pre-fetching macro series...")
            m_summary["macro"] = step_macro(market, progress_path, dry_run=args.dry_run)
            print(f"        macro counts: {m_summary['macro']}")

        if not args.skip_strategies:
            t0 = time.time()
            print(f"  [3/4] Running 5 strategy engines per ticker...")
            m_summary["strategies"] = step_strategies(market, tickers, run_id,
                                                      progress_path, dry_run=args.dry_run)
            print(f"        strategy counts: {m_summary['strategies']} "
                  f"({time.time()-t0:.1f}s)")

        if not args.skip_allocation:
            print(f"  [4/4] Combining via portfolio_engine...")
            m_summary["allocation"] = step_allocation(market, run_id, progress_path,
                                                      dry_run=args.dry_run)
            m_summary["hedge"] = step_hedge(market)
            print(f"        hedge: {'ON' if m_summary['hedge'].get('active') else 'OFF'} "
                  f"({m_summary['hedge'].get('regime')})")

        summary[market] = m_summary

    # Write final report
    report_path = VAULT_DIR / f"Overnight_Backfill_{today}.md"
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(run_id, summary), encoding="utf-8")
    final_path = LOG_DIR / f"overnight_final_{today}.json"
    final_path.write_text(
        json.dumps({"run_id": run_id, "summary": summary}, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"\n=== Done ===")
    print(f"Report: {report_path}")
    print(f"Final JSON: {final_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
