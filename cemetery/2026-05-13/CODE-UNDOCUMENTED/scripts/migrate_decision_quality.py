"""Migration Phase FF Bloco 1.1 — Decision Quality outcome columns + engine breakdown.

Estende `verdict_history` (existente, PK composta `(ticker, date)`) com 8 colunas
de outcome para closed-loop validation contra benchmark. Cria tabela nova
`verdict_engine_breakdown` para registar contribuição de cada engine
(graham/buffett/drip/macro/hedge) ao verdict combinado.

Idempotente — usa PRAGMA table_info para verificar colunas antes de ALTER, e
CREATE TABLE IF NOT EXISTS para o breakdown. Pode correr múltiplas vezes sem
erro.

Uso:
    python scripts/migrate_decision_quality.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = [ROOT / "data" / "br_investments.db", ROOT / "data" / "us_investments.db"]

NEW_COLUMNS: list[tuple[str, str]] = [
    ("outcome_price",         "REAL"),
    ("outcome_date",          "TEXT"),
    ("outcome_return",        "REAL"),
    ("benchmark_symbol",      "TEXT"),
    ("benchmark_return",      "REAL"),
    ("return_vs_benchmark",   "REAL"),
    ("sector_etf",            "TEXT"),
    ("return_vs_sector",      "REAL"),
    ("accuracy",              "INTEGER"),
    ("outperformed_benchmark","INTEGER"),
    ("outperformed_sector",   "INTEGER"),
]

BREAKDOWN_SCHEMA = """
CREATE TABLE IF NOT EXISTS verdict_engine_breakdown (
    ticker        TEXT NOT NULL,
    date          TEXT NOT NULL,
    engine        TEXT NOT NULL,
    score         REAL,
    verdict       TEXT,
    weight        REAL,
    rationale     TEXT,
    PRIMARY KEY (ticker, date, engine)
);

CREATE INDEX IF NOT EXISTS idx_veb_engine ON verdict_engine_breakdown(engine);
CREATE INDEX IF NOT EXISTS idx_veb_date   ON verdict_engine_breakdown(date);
"""


def _existing_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def migrate(db_path: Path) -> None:
    print(f"[migrate] {db_path.name}")
    conn = sqlite3.connect(db_path)
    try:
        existing = _existing_columns(conn, "verdict_history")
        if not existing:
            print(f"  warn: verdict_history table missing in {db_path.name}; skipping ALTERs")
        else:
            for col, sqltype in NEW_COLUMNS:
                if col in existing:
                    continue
                conn.execute(f"ALTER TABLE verdict_history ADD COLUMN {col} {sqltype}")
                print(f"  + verdict_history.{col} ({sqltype})")
        conn.executescript(BREAKDOWN_SCHEMA)
        conn.commit()
        print("  ok")
    finally:
        conn.close()


def main() -> int:
    for db in DBS:
        if db.exists():
            migrate(db)
        else:
            print(f"[migrate] skip {db.name} (missing)")
    print("[migrate] done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
