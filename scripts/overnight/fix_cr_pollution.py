"""Fix CR-suffix pollution from full backfill bug.

Bug: bash `read -r` on CRLF txt files preserved \r in ticker name. Each ticker
got written twice: clean version (older, less data) + dirty version (period=max).

Strategy: MERGE dirty INTO clean namespace, then DELETE dirty rows.
- INSERT OR IGNORE inserts dirty data using cleaned ticker name; only inserts
  rows where (clean_ticker, date) doesn't already exist.
- DELETE drops the dirty rows.

Safe: never deletes data without a clean equivalent existing first.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Tables and their columns (excluding ticker which we transform)
TABLES = {
    "prices":        None,   # use SELECT *
    "dividends":     None,
    "fundamentals":  None,
    "companies":     None,
}


def column_list(c: sqlite3.Connection, table: str) -> list[str]:
    return [row[1] for row in c.execute(f"PRAGMA table_info({table})").fetchall()]


def fix_db(db_path: Path) -> dict:
    print(f"\n=== {db_path.name} ===")
    counts = {}
    with sqlite3.connect(db_path) as c:
        for table in TABLES:
            cols = column_list(c, table)
            if "ticker" not in cols:
                print(f"  {table}: no ticker column, skipping")
                continue
            n_dirty = c.execute(
                f"SELECT COUNT(*) FROM {table} WHERE ticker LIKE '%' || char(13)"
            ).fetchone()[0]
            if not n_dirty:
                continue
            # Build column list with REPLACE on ticker
            select_cols = ", ".join(
                f"REPLACE({col}, char(13), '')" if col == "ticker" else col
                for col in cols
            )
            insert_cols = ", ".join(cols)
            # MERGE: insert clean version of dirty rows where not already present
            n_before_merge = c.execute(
                f"SELECT COUNT(*) FROM {table} WHERE ticker NOT LIKE '%' || char(13)"
            ).fetchone()[0]
            c.execute(
                f"INSERT OR IGNORE INTO {table} ({insert_cols}) "
                f"SELECT {select_cols} FROM {table} WHERE ticker LIKE '%' || char(13)"
            )
            n_after_merge = c.execute(
                f"SELECT COUNT(*) FROM {table} WHERE ticker NOT LIKE '%' || char(13)"
            ).fetchone()[0]
            n_inserted = n_after_merge - n_before_merge
            # DELETE dirty rows
            n_deleted = c.execute(
                f"DELETE FROM {table} WHERE ticker LIKE '%' || char(13)"
            ).rowcount
            c.commit()
            print(f"  {table}: dirty={n_dirty} merged_new={n_inserted} deleted={n_deleted}")
            counts[table] = {"dirty": n_dirty, "new": n_inserted, "deleted": n_deleted}
        # Vacuum to reclaim space (optional, can skip if expensive)
        # c.execute("VACUUM")
    return counts


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== CR-suffix pollution fix ===")
    print("Strategy: MERGE dirty (period=max) INTO clean namespace, then DELETE dirty.")
    for db in [ROOT / "data" / "br_investments.db",
               ROOT / "data" / "us_investments.db"]:
        fix_db(db)
    print("\n=== Verification ===")
    for db in [ROOT / "data" / "br_investments.db",
               ROOT / "data" / "us_investments.db"]:
        c = sqlite3.connect(db)
        for table in TABLES:
            try:
                n = c.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE ticker LIKE '%' || char(13)"
                ).fetchone()[0]
                if n:
                    print(f"  {db.name} {table}: STILL DIRTY ({n} rows)")
                else:
                    pass
            except sqlite3.OperationalError:
                pass
        c.close()
    print("Done.")


if __name__ == "__main__":
    main()
