"""Migração idempotente: adiciona colunas novas à tabela `fundamentals`.

Novos campos extraídos do yfinance.info que ainda não estávamos a persistir:
  - pe_forward           (forward P/E consenso)
  - ev_ebitda            (EV/EBITDA)
  - market_cap           (market cap USD)
  - fcf_ttm              (free cash flow TTM)
  - shares_outstanding   (shares outstanding)
  - next_ex_date         (próxima ex-dividend — ISO)
  - next_earnings_date   (próximo earnings — ISO)

Uso:
    python scripts/migrate_fundamentals_extra.py

Aplica a ambas as DBs (BR + US).
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_COLUMNS = [
    ("pe_forward", "REAL"),
    ("ev_ebitda", "REAL"),
    ("market_cap", "REAL"),
    ("fcf_ttm", "REAL"),
    ("shares_outstanding", "REAL"),
    ("next_ex_date", "TEXT"),
    ("next_earnings_date", "TEXT"),
]


def migrate(db_path: Path) -> None:
    if not db_path.exists():
        print(f"  [skip] {db_path.name} não existe")
        return
    con = sqlite3.connect(db_path)
    existing = {r[1] for r in con.execute("PRAGMA table_info(fundamentals)").fetchall()}
    added = 0
    for col, typ in NEW_COLUMNS:
        if col not in existing:
            con.execute(f"ALTER TABLE fundamentals ADD COLUMN {col} {typ}")
            print(f"  + {db_path.name}:{col} ({typ})")
            added += 1
    con.commit()
    con.close()
    print(f"  [{db_path.name}] {added} colunas adicionadas, {len(NEW_COLUMNS) - added} já existiam")


if __name__ == "__main__":
    for name in ("br_investments.db", "us_investments.db"):
        print(f"--- {name} ---")
        migrate(ROOT / "data" / name)
    print("\nOK")
