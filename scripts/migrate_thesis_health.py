"""Migration: criar tabela thesis_health nas 2 DBs (BR + US).

Heart of Gold: suporta o Ad Perpetuum Validator (agents/perpetuum_validator.py).
Cada run diário deixa uma linha por ticker com score 0-100 + evidence counts.

Idempotente — pode correr múltiplas vezes.

Uso:
    python scripts/migrate_thesis_health.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = [ROOT / "data" / "br_investments.db", ROOT / "data" / "us_investments.db"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS thesis_health (
    ticker           TEXT    NOT NULL,
    run_date         TEXT    NOT NULL,
    thesis_score     INTEGER NOT NULL,
    new_evidence     INTEGER NOT NULL DEFAULT 0,
    contradictions   INTEGER NOT NULL DEFAULT 0,
    regime_shift     INTEGER NOT NULL DEFAULT 0,
    devils_flags     INTEGER NOT NULL DEFAULT 0,
    risk_flags       INTEGER NOT NULL DEFAULT 0,
    details_json     TEXT,
    PRIMARY KEY (ticker, run_date)
);

CREATE INDEX IF NOT EXISTS idx_thesis_health_date   ON thesis_health(run_date);
CREATE INDEX IF NOT EXISTS idx_thesis_health_ticker ON thesis_health(ticker);
CREATE INDEX IF NOT EXISTS idx_thesis_health_score  ON thesis_health(thesis_score);
"""


def migrate(db_path: Path) -> None:
    print(f"[migrate] {db_path.name} ...", end=" ")
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
        print("ok")
    finally:
        conn.close()


if __name__ == "__main__":
    for db in DBS:
        if db.exists():
            migrate(db)
        else:
            print(f"[migrate] skip {db.name} (missing)")
    print("[migrate] done.")
