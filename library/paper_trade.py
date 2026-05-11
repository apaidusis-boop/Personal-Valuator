"""Paper trade log — toda signal de library entra aqui ANTES de qualquer capital real.

Schema:
    paper_trade_signals (
        id INTEGER PK AUTOINCREMENT,
        signal_date TEXT,              -- ISO when signal generated
        ticker TEXT,
        market TEXT,
        method_id TEXT,                -- ref to library/methods/<id>.yaml
        book_slug TEXT,                -- which book the method came from
        direction TEXT,                -- 'LONG' | 'SHORT' | 'NEUTRAL' | 'PAIR' | ...
        horizon TEXT,                  -- 'short' (<30d) | 'medium' (<180d) | 'long' (>180d)
        expected_move_pct REAL,        -- user target % move
        entry_price REAL,              -- price at signal generation
        thesis TEXT,                   -- why the method fired (narrative)
        status TEXT DEFAULT 'open',    -- 'open' | 'closed_win' | 'closed_loss' | 'closed_flat' | 'expired'
        closed_at TEXT,
        closed_price REAL,
        realized_return_pct REAL,
        notes TEXT
    )

Usage:
    from library.paper_trade import log_signal, resolve_signal, track_open

    log_signal(ticker='ITSA4', market='br', method_id='graham_defensive',
               book_slug='graham_intelligent_investor', direction='LONG',
               horizon='long', expected_move_pct=20, entry_price=14.17,
               thesis='passes Graham defensive at 8.91% DY')

CRITICAL: esta tabela é paper ONLY. Nenhum código neste repo deve ler daqui
para decidir real trades sem approval manual explícito por signal.
"""
from __future__ import annotations

import sqlite3
from datetime import date, datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BR_DB = ROOT / "data" / "br_investments.db"
US_DB = ROOT / "data" / "us_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS paper_trade_signals (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_date         TEXT NOT NULL,
    ticker              TEXT NOT NULL,
    market              TEXT NOT NULL,
    method_id           TEXT NOT NULL,
    book_slug           TEXT,
    direction           TEXT NOT NULL,
    horizon             TEXT,
    expected_move_pct   REAL,
    entry_price         REAL,
    thesis              TEXT,
    status              TEXT DEFAULT 'open',
    closed_at           TEXT,
    closed_price        REAL,
    realized_return_pct REAL,
    notes               TEXT
);

CREATE INDEX IF NOT EXISTS idx_paper_status ON paper_trade_signals(status);
CREATE INDEX IF NOT EXISTS idx_paper_ticker ON paper_trade_signals(ticker);
CREATE INDEX IF NOT EXISTS idx_paper_method ON paper_trade_signals(method_id);
"""


def _db(market: str) -> Path:
    return BR_DB if market == "br" else US_DB


def ensure_schema() -> None:
    for db in (BR_DB, US_DB):
        if db.exists():
            with sqlite3.connect(db) as c:
                c.executescript(SCHEMA)
                c.commit()


def log_signal(
    ticker: str,
    market: str,
    method_id: str,
    direction: str,
    book_slug: str | None = None,
    horizon: str = "medium",
    expected_move_pct: float | None = None,
    entry_price: float | None = None,
    thesis: str | None = None,
) -> int:
    ensure_schema()
    db = _db(market)
    with sqlite3.connect(db) as c:
        cur = c.execute(
            """
            INSERT INTO paper_trade_signals
                (signal_date, ticker, market, method_id, book_slug,
                 direction, horizon, expected_move_pct, entry_price, thesis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date.today().isoformat(), ticker, market, method_id, book_slug,
                direction, horizon, expected_move_pct, entry_price, thesis,
            ),
        )
        c.commit()
        return cur.lastrowid


def resolve_signal(
    signal_id: int,
    market: str,
    closed_price: float,
    status: str = "closed_win",
    notes: str = "",
) -> None:
    """Marca signal como resolvido. Calcula realized_return_pct vs entry."""
    db = _db(market)
    with sqlite3.connect(db) as c:
        row = c.execute(
            "SELECT entry_price, direction FROM paper_trade_signals WHERE id=?",
            (signal_id,),
        ).fetchone()
        if not row:
            print(f"signal {signal_id} not found in {market}")
            return
        entry, direction = row
        pct = None
        if entry and closed_price:
            raw = (closed_price - entry) / entry * 100
            pct = raw if direction == "LONG" else -raw
        c.execute(
            """
            UPDATE paper_trade_signals
            SET status=?, closed_at=?, closed_price=?,
                realized_return_pct=?, notes=?
            WHERE id=?
            """,
            (
                status, datetime.now(UTC).isoformat(timespec="seconds"),
                closed_price, pct, notes, signal_id,
            ),
        )
        c.commit()


def performance_by_method(min_closed: int = 5) -> list[dict]:
    """Aggregated paper-trade performance by method_id (requer ≥min_closed signals)."""
    ensure_schema()
    out = []
    for market, db in (("br", BR_DB), ("us", US_DB)):
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute("""
                SELECT method_id, COUNT(*) as total,
                       SUM(CASE WHEN status LIKE 'closed_win' THEN 1 ELSE 0 END) as wins,
                       AVG(CASE WHEN status LIKE 'closed%' THEN realized_return_pct ELSE NULL END) as avg_ret,
                       MIN(CASE WHEN status LIKE 'closed%' THEN realized_return_pct ELSE NULL END) as min_ret,
                       MAX(CASE WHEN status LIKE 'closed%' THEN realized_return_pct ELSE NULL END) as max_ret,
                       COUNT(CASE WHEN status LIKE 'closed%' THEN 1 ELSE NULL END) as closed_n
                FROM paper_trade_signals
                GROUP BY method_id
                HAVING closed_n >= ?
            """, (min_closed,)).fetchall()
            for r in rows:
                out.append({
                    "market": market,
                    "method": r["method_id"],
                    "total_signals": r["total"],
                    "closed": r["closed_n"],
                    "win_rate_pct": round(100 * r["wins"] / max(r["closed_n"], 1), 1),
                    "avg_return_pct": round(r["avg_ret"] or 0, 2),
                    "range": f"{r['min_ret']:.1f}% to {r['max_ret']:.1f}%",
                })
    return out


if __name__ == "__main__":
    ensure_schema()
    print("paper_trade_signals schema applied to both DBs.")
    print()
    print("Example:")
    print("  from library.paper_trade import log_signal")
    print("  log_signal(ticker='ITSA4', market='br', method_id='graham_defensive',")
    print("             direction='LONG', horizon='long', entry_price=14.17)")
