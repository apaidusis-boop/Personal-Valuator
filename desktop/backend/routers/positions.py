"""positions — /api/positions, /api/snapshot endpoints."""
from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path

from fastapi import APIRouter, Query

ROOT = Path(__file__).resolve().parents[3]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

router = APIRouter()


@router.get("/positions")
def positions() -> list[dict]:
    """Active holdings BR + US, latest close, MV in native currency."""
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT p.ticker, p.quantity, p.entry_price, p.entry_date, p.notes,
                       c.name, c.sector, c.currency,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS price,
                       (SELECT date  FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS price_date,
                       (SELECT score FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS screen_score,
                       (SELECT passes_screen FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS screen_pass
                FROM portfolio_positions p LEFT JOIN companies c ON c.ticker=p.ticker
                WHERE p.active=1
            """)
            for r in cur:
                d = dict(r)
                d["market"] = market
                qty = d.get("quantity") or 0
                price = d.get("price") or 0
                entry = d.get("entry_price") or 0
                d["mv_native"] = round(qty * price, 2)
                d["cost_native"] = round(qty * entry, 2)
                d["pnl_pct"] = round(((price / entry) - 1) * 100, 2) if entry else None
                rows.append(d)
    return rows


@router.get("/snapshot")
def snapshot(days: int = Query(180, ge=7, le=730)) -> list[dict]:
    """Daily portfolio snapshots, last `days` days, BR+US in BRL."""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            try:
                cur = c.execute(
                    "SELECT date, ticker, mv_brl, mv_native FROM portfolio_snapshots "
                    "WHERE date >= ? ORDER BY date",
                    (cutoff,),
                )
                for r in cur:
                    d = dict(r)
                    d["market"] = market
                    out.append(d)
            except sqlite3.OperationalError:
                pass
    return out


@router.get("/sectors")
def sectors() -> list[dict]:
    """Sector exposure — sum of MV in BRL by sector across BR+US."""
    fx = 5.0
    with sqlite3.connect(DB_BR) as c:
        r = c.execute(
            "SELECT value FROM series WHERE series_id='USDBRL_PTAX' "
            "ORDER BY date DESC LIMIT 1"
        ).fetchone()
        if r:
            fx = float(r[0])
    agg: dict[str, float] = {}
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            cur = c.execute("""
                SELECT c.sector,
                       SUM(p.quantity *
                           COALESCE((SELECT close FROM prices
                                     WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1), 0)) AS mv_native
                FROM portfolio_positions p LEFT JOIN companies c ON c.ticker=p.ticker
                WHERE p.active=1
                GROUP BY c.sector
            """)
            for sector, mv in cur:
                if not sector:
                    continue
                mv_brl = (mv or 0) * (fx if market == "us" else 1.0)
                agg[sector] = agg.get(sector, 0.0) + mv_brl
    rows = [{"sector": s, "mv_brl": round(v, 2)} for s, v in agg.items()]
    rows.sort(key=lambda r: -r["mv_brl"])
    return rows
