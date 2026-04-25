"""signals — /api/signals/open, /api/signals/by-ticker/{sym}.

Surface for `paper_trade_signals` table — book methods × portfolio matches.
"""
from __future__ import annotations

import sqlite3
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Query

ROOT = Path(__file__).resolve().parents[3]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

router = APIRouter()


@router.get("/signals/open")
def signals_open(limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    """Open paper trade signals across BR + US, newest first."""
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT id, signal_date, ticker, market, method_id, book_slug,
                       direction, horizon, expected_move_pct, entry_price,
                       thesis, status, notes
                FROM paper_trade_signals
                WHERE status='open'
                ORDER BY signal_date DESC, id DESC
                LIMIT ?
            """, (limit,))
            for r in cur:
                d = dict(r)
                d["market"] = market
                rows.append(d)
    rows.sort(key=lambda r: r.get("signal_date") or "", reverse=True)
    return rows[:limit]


@router.get("/signals/summary")
def signals_summary() -> dict:
    """Aggregates: by direction, by method, total open."""
    by_direction: Counter[str] = Counter()
    by_method: Counter[str] = Counter()
    total_open = 0
    total_closed = 0
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            for r in c.execute(
                "SELECT status, direction, method_id FROM paper_trade_signals"
            ):
                status, direction, method = r
                if status == "open":
                    total_open += 1
                    by_direction[direction or "?"] += 1
                    by_method[method or "?"] += 1
                elif status == "closed":
                    total_closed += 1
    return {
        "total_open": total_open,
        "total_closed": total_closed,
        "by_direction": dict(by_direction.most_common()),
        "by_method_top10": dict(by_method.most_common(10)),
    }


@router.get("/signals/by-ticker/{ticker}")
def signals_by_ticker(ticker: str) -> list[dict]:
    """All paper signals for a single ticker, both markets."""
    ticker = ticker.upper()
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT id, signal_date, method_id, direction, horizon,
                       expected_move_pct, entry_price, thesis, status,
                       closed_at, closed_price, realized_return_pct
                FROM paper_trade_signals
                WHERE ticker=?
                ORDER BY signal_date DESC, id DESC
            """, (ticker,))
            for r in cur:
                d = dict(r)
                d["market"] = market
                rows.append(d)
    return rows


@router.get("/verdicts/{ticker}/history")
def verdict_history(ticker: str, limit: int = Query(20, ge=1, le=200)) -> list[dict]:
    """Past verdicts for a ticker, newest first."""
    ticker = ticker.upper()
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT date, action, total_score, confidence_pct,
                       quality_score, valuation_score, momentum_score,
                       narrative_score, price_at_verdict, recorded_at
                FROM verdict_history
                WHERE ticker=?
                ORDER BY date DESC
                LIMIT ?
            """, (ticker, limit))
            for r in cur:
                d = dict(r)
                d["market"] = market
                rows.append(d)
    rows.sort(key=lambda r: r.get("date") or "", reverse=True)
    return rows[:limit]
