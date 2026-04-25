"""ticker — /api/ticker/{symbol}, /api/verdict/{symbol}, /api/prices/{symbol}."""
from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

ROOT = Path(__file__).resolve().parents[3]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

router = APIRouter()


def _market_of(ticker: str) -> str:
    """Detect market by checking which DB has the ticker registered."""
    with sqlite3.connect(DB_BR) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?",
                     (ticker,)).fetchone():
            return "br"
    with sqlite3.connect(DB_US) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?",
                     (ticker,)).fetchone():
            return "us"
    raise HTTPException(404, f"ticker {ticker} not found")


@router.get("/ticker/{symbol}")
def ticker_summary(symbol: str) -> dict:
    """Static metadata + latest snapshot."""
    symbol = symbol.upper()
    market = _market_of(symbol)
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        company = c.execute(
            "SELECT ticker, name, sector, currency FROM companies WHERE ticker=?",
            (symbol,),
        ).fetchone()
        if not company:
            raise HTTPException(404, f"company {symbol} not found")
        last_price = c.execute(
            "SELECT date, close, volume FROM prices WHERE ticker=? "
            "ORDER BY date DESC LIMIT 1",
            (symbol,),
        ).fetchone()
        latest_score = c.execute(
            "SELECT run_date, score, passes_screen, details_json "
            "FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (symbol,),
        ).fetchone()

    return {
        "ticker": symbol,
        "market": market,
        "company": dict(company),
        "last_price": dict(last_price) if last_price else None,
        "latest_score": dict(latest_score) if latest_score else None,
    }


@router.get("/prices/{symbol}")
def prices(symbol: str, days: int = Query(365, ge=7, le=3650)) -> list[dict]:
    """OHLC time series. Default 1y."""
    symbol = symbol.upper()
    market = _market_of(symbol)
    db = DB_BR if market == "br" else DB_US
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        cur = c.execute(
            "SELECT date, close, volume FROM prices "
            "WHERE ticker=? AND date>=? ORDER BY date",
            (symbol, cutoff),
        )
        return [dict(r) for r in cur]


@router.get("/verdict/{symbol}")
def verdict(symbol: str) -> dict:
    """Compute on-demand. Reuses scoring.verdict (existing engine)."""
    symbol = symbol.upper()
    try:
        from scoring.verdict import compute_verdict  # type: ignore
    except Exception:
        # Engine not yet wired here — return a stub so frontend can detect.
        return {"ticker": symbol, "error": "verdict engine not yet exposed"}
    try:
        return compute_verdict(symbol)
    except Exception as e:
        return {"ticker": symbol, "error": f"{type(e).__name__}: {e}"}
