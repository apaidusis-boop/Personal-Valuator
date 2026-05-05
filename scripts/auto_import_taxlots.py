"""auto_import_taxlots — corre import_taxlots se o CSV em Downloads for mais recente.

Idempotente. Safe to run from cron (daily_run.bat) ou ad-hoc.
Compara file mtime vs MAX(imported_at) em tax_lots WHERE source='jpm_import'.
Se ficheiro inexistente ou mais antigo, é no-op silencioso.

Uso:
    python scripts/auto_import_taxlots.py            # default ~/Downloads/taxlots.csv
    python scripts/auto_import_taxlots.py --file X   # path custom
    python scripts/auto_import_taxlots.py --quiet    # cron-friendly
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_US = ROOT / "data" / "us_investments.db"
DEFAULT_CSV = Path.home() / "Downloads" / "taxlots.csv"


def _last_imported_at() -> datetime | None:
    if not DB_US.exists():
        return None
    with sqlite3.connect(DB_US) as c:
        row = c.execute(
            "SELECT MAX(imported_at) FROM tax_lots WHERE source='jpm_import'"
        ).fetchone()
    if not row or not row[0]:
        return None
    try:
        dt = datetime.fromisoformat(row[0])
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", default=str(DEFAULT_CSV))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    csv_path = Path(args.file).expanduser()
    if not csv_path.exists():
        if not args.quiet:
            print(f"[auto-import] no file at {csv_path}, skipping")
        return 0

    file_mtime = datetime.fromtimestamp(csv_path.stat().st_mtime, tz=timezone.utc)
    last = _last_imported_at()
    if last and file_mtime <= last:
        if not args.quiet:
            print(f"[auto-import] CSV mtime {file_mtime.isoformat()} <= last import {last.isoformat()}, skipping")
        return 0

    if not args.quiet:
        print(f"[auto-import] CSV updated ({file_mtime.isoformat()}); running import_taxlots")

    from scripts.import_taxlots import (
        aggregate_to_positions,
        parse_csv,
        persist_cash,
        persist_lots,
    )
    lots, cash, _meta = parse_csv(csv_path)
    persist_lots(lots, dry_run=False)
    persist_cash(cash, dry_run=False)
    agg = aggregate_to_positions(dry_run=False)
    if not args.quiet:
        print(
            f"[auto-import] done. lots={len(lots)} tickers={agg['tickers']} "
            f"cash={cash.get('amount', 0)} {cash.get('currency', '')}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
