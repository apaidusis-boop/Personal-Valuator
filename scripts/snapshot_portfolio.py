"""snapshot_portfolio — grava snapshot diário de MV em portfolio_snapshots.

Correr diariamente (cron) após close BR. Computa por ticker:
  (date, ticker, qty, price_close, mv_native, mv_brl, fx_rate).

Base para charts de evolução em `scripts/dashboard_app.py` e Obsidian Charts.

Uso:
    python scripts/snapshot_portfolio.py
    python scripts/snapshot_portfolio.py --date 2026-04-23   # backfill
    python scripts/snapshot_portfolio.py --force             # overwrite
    python scripts/snapshot_portfolio.py --backfill 90       # últimos 90d
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _fx_for_date(iso_date: str) -> float:
    with sqlite3.connect(DB_BR) as c:
        r = c.execute(
            """SELECT value FROM series
               WHERE series_id='USDBRL_PTAX' AND date<=?
               ORDER BY date DESC LIMIT 1""",
            (iso_date,),
        ).fetchone()
    return float(r[0]) if r else 5.0


def _price_for(db: Path, ticker: str, iso_date: str) -> float | None:
    with sqlite3.connect(db) as c:
        r = c.execute(
            "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
            (ticker, iso_date),
        ).fetchone()
    return float(r[0]) if r else None


def snapshot_one(iso_date: str, force: bool = False) -> dict:
    """Grava snapshot de holdings activas para `iso_date`."""
    fx = _fx_for_date(iso_date)
    now = datetime.now(UTC).isoformat()
    stats = {"date": iso_date, "br": 0, "us": 0, "skipped_no_price": 0}

    for market, db in (("br", DB_BR), ("us", DB_US)):
        other_db = db  # snapshots stay per-market
        with sqlite3.connect(other_db) as c:
            holdings = c.execute(
                "SELECT ticker, quantity FROM portfolio_positions WHERE active=1"
            ).fetchall()
            for tk, qty in holdings:
                if force:
                    c.execute("DELETE FROM portfolio_snapshots WHERE date=? AND ticker=?",
                              (iso_date, tk))
                existing = c.execute(
                    "SELECT 1 FROM portfolio_snapshots WHERE date=? AND ticker=?",
                    (iso_date, tk),
                ).fetchone()
                if existing:
                    continue
                px = _price_for(db, tk, iso_date)
                if px is None:
                    stats["skipped_no_price"] += 1
                    continue
                mv_native = px * qty
                mv_brl = mv_native * (fx if market == "us" else 1.0)
                c.execute(
                    """INSERT INTO portfolio_snapshots
                         (date, ticker, quantity, price_close, mv_native, mv_brl, fx_rate, created_at)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (iso_date, tk, qty, px, mv_native, mv_brl, fx, now),
                )
                stats[market] += 1
            c.commit()
    return stats


def snapshot_backfill(days: int, force: bool = False) -> list[dict]:
    results = []
    start = date.today() - timedelta(days=days)
    for i in range(days + 1):
        d = (start + timedelta(days=i)).isoformat()
        results.append(snapshot_one(d, force=force))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", help="ISO (default hoje)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--backfill", type=int, help="Backfill últimos N dias")
    args = ap.parse_args()

    # Ensure schema
    from scripts.init_db import init
    init(DB_BR)
    init(DB_US)

    if args.backfill:
        print(f"Backfilling {args.backfill}d...")
        rs = snapshot_backfill(args.backfill, force=args.force)
        br_total = sum(r["br"] for r in rs)
        us_total = sum(r["us"] for r in rs)
        print(f"Done. BR rows: {br_total}, US rows: {us_total}")
    else:
        d = args.date or date.today().isoformat()
        r = snapshot_one(d, force=args.force)
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
