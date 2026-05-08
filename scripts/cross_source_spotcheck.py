"""Phase FF Bloco 3.3 — yfinance SPOF mitigation via cross-source spot check.

Picks N US holdings per run, fetches today's close from BOTH yfinance and
massive, flags divergences > tolerance. Persists each fetch as a `provenance`
row (free; the fallback wrapper already does this) and writes any divergence
as a row in `data_anomalies.json` so the daily MC alerts pick it up.

Why US only:
    BR has only yfinance configured for prices in sources_priority.yaml — no
    second source to cross-check against. BR SPOF mitigation lives in the
    existing analytics/data_anomalies.py detectors (PRICE_JUMP/STALE).

Cron: wired in scripts/daily_run.bat right after refresh_benchmarks.

Usage:
    python scripts/cross_source_spotcheck.py [--n 5] [--tolerance 0.02] [--quiet]
"""
from __future__ import annotations

import argparse
import json
import random
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fetchers._fallback import fetch_with_quality

DB_US = ROOT / "data" / "us_investments.db"
ANOMALIES_PATH = ROOT / "data" / "data_anomalies.json"


def _holdings(n: int) -> list[str]:
    with sqlite3.connect(DB_US) as conn:
        rows = conn.execute(
            "SELECT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()
    tickers = sorted({r[0] for r in rows if r[0]})
    if len(tickers) <= n:
        return tickers
    return random.sample(tickers, n)


def _close(value: dict) -> float | None:
    if not isinstance(value, dict):
        return None
    for key in ("close", "previous_close", "regularMarketPreviousClose", "price"):
        v = value.get(key)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def _append_anomaly(record: dict) -> None:
    payload = {"runs": []}
    if ANOMALIES_PATH.exists():
        try:
            payload = json.loads(ANOMALIES_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {"runs": []}
    payload.setdefault("runs", []).append(record)
    ANOMALIES_PATH.write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--tolerance", type=float, default=0.02,
                    help="Max acceptable relative diff (default 2%)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    holdings = _holdings(args.n)
    if not holdings:
        if not args.quiet:
            print("No active US holdings — nothing to check")
        return 0

    divergences = []
    checked = []
    for ticker in holdings:
        yf = fetch_with_quality("us", "prices", ticker, sources=["yfinance"])
        ms = fetch_with_quality("us", "prices", ticker, sources=["massive"])
        yf_close = _close(yf.value) if yf.success else None
        ms_close = _close(ms.value) if ms.success else None
        checked.append({
            "ticker": ticker,
            "yfinance_close": yf_close,
            "massive_close": ms_close,
            "yfinance_status": yf.quality if yf.success else "FAIL",
            "massive_status": ms.quality if ms.success else "FAIL",
        })
        if yf_close is None or ms_close is None or ms_close == 0:
            continue
        diff = abs(yf_close - ms_close) / ms_close
        if diff > args.tolerance:
            divergences.append({
                "ticker": ticker,
                "yfinance_close": yf_close,
                "massive_close": ms_close,
                "abs_pct_diff": round(diff * 100, 3),
            })

    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": "CROSS_SOURCE_SPOTCHECK",
        "tolerance_pct": args.tolerance * 100,
        "checked": checked,
        "divergences": divergences,
    }
    _append_anomaly(record)

    if not args.quiet:
        print(f"Spot-check {len(holdings)} tickers — divergences: {len(divergences)}")
        for d in divergences:
            print(f"  ⚠ {d['ticker']}: yf={d['yfinance_close']} vs ms={d['massive_close']} "
                  f"({d['abs_pct_diff']}%)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
