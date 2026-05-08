"""Phase FF Bloco 3.1 — provenance table migration (BR + US).

One-shot, idempotent. Adds:
  - provenance(id, fetched_at, market, kind, ticker, source, quality,
               age_hours, value_hash, message)
  - idx_provenance_ticker_kind_date

Reseed-safe: re-running is a no-op (CREATE TABLE IF NOT EXISTS).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DBS = [ROOT / "data" / "br_investments.db", ROOT / "data" / "us_investments.db"]

DDL = """
CREATE TABLE IF NOT EXISTS provenance (
    id          INTEGER PRIMARY KEY,
    fetched_at  TEXT NOT NULL,
    market      TEXT NOT NULL,
    kind        TEXT NOT NULL,
    ticker      TEXT NOT NULL,
    source      TEXT NOT NULL,
    quality     TEXT NOT NULL,
    age_hours   REAL DEFAULT 0,
    value_hash  TEXT,
    message     TEXT
);

CREATE INDEX IF NOT EXISTS idx_provenance_ticker_kind_date
    ON provenance(ticker, kind, fetched_at DESC);

CREATE INDEX IF NOT EXISTS idx_provenance_quality_date
    ON provenance(quality, fetched_at DESC);
"""


def main() -> None:
    for db in DBS:
        with sqlite3.connect(db) as conn:
            conn.executescript(DDL)
            conn.commit()
            n = conn.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
            print(f"{db.name}: provenance ready ({n} rows)")


if __name__ == "__main__":
    main()
