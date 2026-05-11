"""ROIC calculator — Return on Invested Capital from deep_fundamentals.

Formula (simplified for available data):
    NOPAT       = EBIT × (1 - effective_tax_rate)
    Invested    = Stockholders Equity + Total Debt
    ROIC        = NOPAT / Invested

Tax rate fallback: 21% (post-TCJA US corp). For BR uses 34% (IRPJ+CSLL).
This is intentionally simplistic — purpose is screening, not corporate
finance. Buffett's bar is 15%; precision below 1pp doesn't change verdict.

Returns None when:
- ticker not in deep_fundamentals
- ebit / equity / debt missing
- equity + debt = 0 (would div by zero)
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

TAX_RATES = {"us": 0.21, "br": 0.34}


def compute(ticker: str, market: str = "us") -> float | None:
    """ROIC as fraction (0.18 = 18%). None if data missing."""
    db = DB_BR if market == "br" else DB_US
    if not db.exists():
        return None
    try:
        with sqlite3.connect(db) as conn:
            row = conn.execute(
                """SELECT ebit, stockholders_equity, total_debt
                   FROM deep_fundamentals
                   WHERE ticker=? AND period_type='annual'
                     AND ebit IS NOT NULL
                     AND stockholders_equity IS NOT NULL
                   ORDER BY period_end DESC LIMIT 1""",
                (ticker,),
            ).fetchone()
    except sqlite3.OperationalError:
        return None
    if not row:
        return None
    ebit, equity, debt = row
    if equity is None or equity <= 0:
        return None
    debt = debt or 0.0
    invested = equity + debt
    if invested <= 0:
        return None
    tax = TAX_RATES.get(market, 0.21)
    nopat = ebit * (1 - tax)
    return round(nopat / invested, 4)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Compute ROIC from deep_fundamentals")
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"], default="us")
    args = ap.parse_args()
    r = compute(args.ticker, args.market)
    if r is None:
        print(f"{args.ticker} ROIC: N/A (missing data)")
        return 1
    print(f"{args.ticker} ROIC ({args.market.upper()}): {r*100:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
