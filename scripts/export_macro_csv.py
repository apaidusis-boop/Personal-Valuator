"""Exporta séries macro (BCB SGS) para CSV em data/macro_exports/.

Objectivos:
  - Diffs legíveis em git (CSV é texto; .db é binário)
  - Portabilidade: qualquer ferramenta lê o CSV sem SQLite
  - Reseeding: permite reconstruir a DB a partir dos CSVs + fetchers

Um ficheiro por série. Append-only (dados históricos não mudam).
Idempotente: reescreve o CSV inteiro cada run — delta é só as linhas novas.

Uso:
    python scripts/export_macro_csv.py
"""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "br_investments.db"
OUT = ROOT / "data" / "macro_exports"

SERIES = ["SELIC_DAILY", "SELIC_META", "CDI_DAILY", "IPCA_MONTHLY", "USDBRL_PTAX"]


def export_series(conn: sqlite3.Connection, series_id: str) -> tuple[Path, int]:
    rows = conn.execute(
        "SELECT date, value FROM series WHERE series_id=? ORDER BY date ASC",
        (series_id,),
    ).fetchall()
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{series_id}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "value"])
        for date, value in rows:
            w.writerow([date, value])
    return path, len(rows)


def main() -> None:
    with sqlite3.connect(DB) as conn:
        for sid in SERIES:
            path, n = export_series(conn, sid)
            print(f"[ok] {sid:15} {n:>6} linhas  →  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
