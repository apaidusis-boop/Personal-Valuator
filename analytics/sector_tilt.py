"""Sector-tilt analyzer — Phase FF Bloco 4.1.

Computes how the active portfolio's sector weights diverge from a benchmark
(SPY US / BOVA11 BR or sector ETF mix). Surfaces structural over/under-
exposure relative to the index.

Why this matters for Phase FF: confirmation-bias detection. A system that
always recommends Buffett-favored sectors will mechanically tilt toward
Tech/Financials/Staples relative to SPY. Measuring the tilt makes the bias
*visible* — it doesn't tell you the tilt is wrong, but it makes the case
that you're choosing it.

Data sources:
  - Active positions: portfolio_positions WHERE active=1
  - Sector mapping: companies.sector
  - Benchmark sector weights: hard-coded reference (SPY/BOVA11 sector splits
    as of 2026-04). These shift over years; refresh from SPDR factsheets.

Output:
  JSON record persisted to data/sector_tilt_history.parquet (or fallback
  data/sector_tilt_history.json if pyarrow not installed).

Usage:
    python -m analytics.sector_tilt run [--market us|br|both]
    python -m analytics.sector_tilt show [--market us]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
HISTORY_JSON = ROOT / "data" / "sector_tilt_history.json"

# SPY sector weights — approximate (SPDR factsheet 2026-Q1 aliased to
# investment-intelligence sector taxonomy used in companies.sector). Rebalance
# this from the live SPDR holdings doc when material drift suspected.
SPY_BENCHMARK = {
    "Technology": 0.295,
    "Financials": 0.135,
    "Healthcare": 0.115,
    "Consumer Disc.": 0.105,
    "Communication": 0.085,
    "Industrials": 0.080,
    "Consumer Staples": 0.060,
    "Energy": 0.040,
    "Materials": 0.025,
    "REIT": 0.025,
    "Utilities": 0.025,
    "Holding": 0.010,  # BRK-B included in SPY but classified separately by us
    "ETF": 0.000,
}

# BOVA11 sector weights — IBOV index composition Q1 2026 (B3 official factsheet
# aliased to our sector taxonomy). Heavy commodity/financials tilt is structural.
BOVA11_BENCHMARK = {
    "Banks": 0.225,
    "Mining": 0.115,
    "Oil & Gas": 0.110,
    "Materials": 0.080,
    "Industrials": 0.075,
    "Utilities": 0.075,
    "Consumer Disc.": 0.065,
    "Consumer Staples": 0.060,
    "Telecom": 0.050,
    "Healthcare": 0.045,
    "Financials": 0.045,        # ex-banks (insurance, brokerage)
    "Holding": 0.030,
    "Real Estate": 0.025,        # FIIs aren't in BOVA11 directly
}


def _portfolio_weights(market: str) -> dict[str, float]:
    """Equal-weight across active holdings (sector frequency, not market cap)."""
    db = DB_US if market == "us" else DB_BR
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """
            SELECT c.sector, COUNT(*) AS n
            FROM portfolio_positions p
            JOIN companies c ON c.ticker = p.ticker
            WHERE p.active=1 AND c.sector IS NOT NULL AND c.sector != ''
            GROUP BY c.sector
            """
        ).fetchall()
    total = sum(r[1] for r in rows) or 1
    return {sector: count / total for sector, count in rows}


def _tilts(weights: dict[str, float], benchmark: dict[str, float]) -> list[dict]:
    sectors = sorted(set(weights) | set(benchmark))
    rows = []
    for s in sectors:
        w = weights.get(s, 0.0)
        b = benchmark.get(s, 0.0)
        rows.append({
            "sector": s,
            "portfolio_weight": round(w, 4),
            "benchmark_weight": round(b, 4),
            "tilt_pp": round((w - b) * 100, 2),  # percentage points
        })
    rows.sort(key=lambda r: abs(r["tilt_pp"]), reverse=True)
    return rows


def run(market: str) -> dict:
    if market == "us":
        weights = _portfolio_weights("us")
        bench = SPY_BENCHMARK
        bench_label = "SPY"
    elif market == "br":
        weights = _portfolio_weights("br")
        bench = BOVA11_BENCHMARK
        bench_label = "BOVA11"
    else:
        raise ValueError(f"unknown market {market!r}")
    tilts = _tilts(weights, bench)
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "market": market,
        "benchmark": bench_label,
        "n_holdings": sum(1 for v in weights.values() if v > 0),
        "tilts": tilts,
    }
    return record


def append_history(record: dict) -> None:
    payload = {"runs": []}
    if HISTORY_JSON.exists():
        try:
            payload = json.loads(HISTORY_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {"runs": []}
    payload.setdefault("runs", []).append(record)
    HISTORY_JSON.write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )


def cmd_run(args) -> int:
    markets = ["us", "br"] if args.market == "both" else [args.market]
    for m in markets:
        record = run(m)
        append_history(record)
        print(f"\n=== {m.upper()} sector tilt vs {record['benchmark']} ===")
        print(f"{'Sector':<22} {'Portfolio':>10} {'Bench':>10} {'Tilt (pp)':>11}")
        print("-" * 56)
        for t in record["tilts"]:
            mark = "+" if t["tilt_pp"] > 0 else "-" if t["tilt_pp"] < 0 else " "
            print(f"  {t['sector']:<20} {t['portfolio_weight']*100:>9.1f}% "
                  f"{t['benchmark_weight']*100:>9.1f}% {mark} {t['tilt_pp']:>+8.2f}")
    return 0


def cmd_show(args) -> int:
    if not HISTORY_JSON.exists():
        print("No history yet. Run `run` first.")
        return 1
    payload = json.loads(HISTORY_JSON.read_text(encoding="utf-8"))
    runs = [r for r in payload.get("runs", []) if r.get("market") == args.market]
    if not runs:
        print(f"No runs for market={args.market}")
        return 1
    last = runs[-1]
    print(f"\n=== Latest tilt — {args.market.upper()} {last['ts']} ===")
    for t in last["tilts"][:10]:
        print(f"  {t['sector']:<22} portfolio={t['portfolio_weight']*100:.1f}% "
              f"bench={t['benchmark_weight']*100:.1f}% tilt={t['tilt_pp']:+.2f}pp")
    print(f"... {len(last['tilts'])-10} more sectors" if len(last["tilts"]) > 10 else "")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run")
    p_run.add_argument("--market", choices=["us", "br", "both"], default="both")
    p_run.set_defaults(func=cmd_run)
    p_show = sub.add_parser("show")
    p_show.add_argument("--market", choices=["us", "br"], required=True)
    p_show.set_defaults(func=cmd_show)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
