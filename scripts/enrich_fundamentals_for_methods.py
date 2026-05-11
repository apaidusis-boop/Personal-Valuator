"""Enrich fundamentals schema with columns needed by library methods.

Adds (idempotent):
    shares_outstanding   REAL
    market_cap_usd       REAL      -- price * shares * fx
    current_ratio        REAL      -- from yfinance if available
    ltd                  REAL      -- long-term debt
    working_capital      REAL
    beta_levered         REAL
    peg_ratio            REAL      -- forward PEG

Backfill fontes:
  - yfinance .info (get_info) — tem quotient of fields
  - brapi para BR (via token em .env)

Aplica a fundamentals row MAIS RECENTE de cada ticker holding/watchlist.
Non-destructive: se não consegue, deixa NULL.

Uso:
    python scripts/enrich_fundamentals_for_methods.py --schema       # só migration
    python scripts/enrich_fundamentals_for_methods.py --backfill     # fetch + update
    python scripts/enrich_fundamentals_for_methods.py --ticker ITSA4
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}

NEW_COLS = {
    "shares_outstanding": "REAL",
    "market_cap_usd": "REAL",
    "current_ratio": "REAL",
    "ltd": "REAL",
    "working_capital": "REAL",
    "beta_levered": "REAL",
    "peg_ratio": "REAL",
}


def apply_schema(db: Path) -> list[str]:
    added = []
    with sqlite3.connect(db) as c:
        cols = {row[1] for row in c.execute("PRAGMA table_info(fundamentals)").fetchall()}
        for col, typ in NEW_COLS.items():
            if col not in cols:
                c.execute(f"ALTER TABLE fundamentals ADD COLUMN {col} {typ}")
                added.append(col)
        c.commit()
    return added


def backfill_ticker(market: str, ticker: str) -> dict:
    """Fetch and apply enrichment for 1 ticker via yfinance (works for BR+US)."""
    try:
        import yfinance as yf
    except ImportError:
        return {"ticker": ticker, "status": "yfinance not installed"}

    yf_ticker = ticker + ".SA" if market == "br" else ticker
    try:
        info = yf.Ticker(yf_ticker).info
    except Exception as e:
        return {"ticker": ticker, "status": f"yf_error: {e}"}

    if not info or len(info) < 5:
        return {"ticker": ticker, "status": "no_info"}

    db = DBS[market]
    updates = {}
    for our, yf_key in [
        ("shares_outstanding", "sharesOutstanding"),
        ("current_ratio", "currentRatio"),
        ("beta_levered", "beta"),
        ("peg_ratio", "pegRatio"),
    ]:
        v = info.get(yf_key)
        if v is not None:
            try:
                updates[our] = float(v)
            except Exception:
                pass

    # compute market_cap_usd
    mc = info.get("marketCap")
    if mc:
        if market == "br":
            fx = info.get("currency") == "BRL"
            try:
                brl_usd = yf.Ticker("BRL=X").history(period="1d")["Close"].iloc[-1]
                if brl_usd and brl_usd > 0:
                    updates["market_cap_usd"] = float(mc) / float(brl_usd)
            except Exception:
                updates["market_cap_usd"] = None
        else:
            updates["market_cap_usd"] = float(mc)

    # ltd + working_capital — balance sheet
    try:
        bs = yf.Ticker(yf_ticker).balance_sheet
        if bs is not None and not bs.empty:
            latest = bs.columns[0]
            if "Long Term Debt" in bs.index:
                updates["ltd"] = float(bs.at["Long Term Debt", latest])
            if "Current Assets" in bs.index and "Current Liabilities" in bs.index:
                ca = float(bs.at["Current Assets", latest])
                cl = float(bs.at["Current Liabilities", latest])
                updates["working_capital"] = ca - cl
    except Exception:
        pass

    if not updates:
        return {"ticker": ticker, "status": "no_data", "updates": 0}

    # Find latest fundamentals row
    with sqlite3.connect(db) as c:
        row = c.execute(
            "SELECT period_end FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if not row:
            # create a row today
            c.execute(
                "INSERT INTO fundamentals (ticker, period_end) VALUES (?, ?)",
                (ticker, date.today().isoformat()),
            )
            period_end = date.today().isoformat()
        else:
            period_end = row[0]

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        c.execute(
            f"UPDATE fundamentals SET {set_clause} WHERE ticker=? AND period_end=?",
            (*updates.values(), ticker, period_end),
        )
        c.commit()

    return {"ticker": ticker, "status": "ok", "updates": len(updates), "fields": list(updates.keys())}


def holdings_list(market: str) -> list[str]:
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        rows = c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()
    return [r[0] for r in rows]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", action="store_true", help="Apply migration only")
    ap.add_argument("--backfill", action="store_true", help="Fetch + update all holdings")
    ap.add_argument("--ticker", help="Single ticker backfill")
    ap.add_argument("--market", choices=["br", "us"], help="Market for --ticker")
    args = ap.parse_args()

    # Always apply schema first
    for market, db in DBS.items():
        if db.exists():
            added = apply_schema(db)
            if added:
                print(f"[schema] {market}: added columns {added}")
            else:
                print(f"[schema] {market}: already up to date")

    if args.schema and not args.backfill and not args.ticker:
        return

    if args.ticker:
        m = args.market or "us"
        print(f"[backfill] {m}:{args.ticker}")
        r = backfill_ticker(m, args.ticker)
        print(f"  {r}")
        return

    if args.backfill:
        for market in ("br", "us"):
            tickers = holdings_list(market)
            print(f"\n[backfill] market={market}  tickers={len(tickers)}")
            for t in tickers:
                r = backfill_ticker(market, t)
                status = r["status"]
                fields = r.get("fields", [])
                print(f"  {t:<8} {status:<20} fields={fields}")


if __name__ == "__main__":
    main()
