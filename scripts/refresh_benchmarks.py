"""Refresh benchmark prices (SPY US / BOVA11 BR / 11 sector ETFs US).

Wired into daily_run.bat após `daily_update_us.py` (Phase FF Bloco 1.1
follow-up). Mantém SPY + BOVA11 + sector ETFs frescos para feed do
`analytics.decision_quality.update_outcomes` que cruza verdicts com benchmarks.

Modos:
  - default: fetch últimos 5 dias úteis (cobre fins-de-semana, idempotente)
  - --backfill: fetch 2 anos (re-correr só se DB perdeu dados)

100% local (yfinance, sem auth). Idempotente (INSERT OR REPLACE).

Uso:
    python scripts/refresh_benchmarks.py             # diário (5d)
    python scripts/refresh_benchmarks.py --backfill  # re-seed 2y
    python scripts/refresh_benchmarks.py --quiet
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

US_BENCHMARKS = ["SPY", "XLK", "XLV", "XLF", "XLE", "XLI", "XLY", "XLP", "XLB", "XLRE", "XLU", "XLC"]
BR_BENCHMARKS_YF = [("BOVA11.SA", "BOVA11")]


def _flatten_columns(df) -> None:
    """yfinance pode devolver multi-index; achata in-place."""
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)


def _fetch(symbol_yf: str, symbol_db: str, db_path: Path, period: str, quiet: bool) -> int:
    import yfinance as yf

    df = yf.download(symbol_yf, period=period, auto_adjust=False, progress=False, group_by="column")
    if df.empty:
        if not quiet:
            print(f"  {symbol_yf}: empty")
        return 0
    _flatten_columns(df)

    rows: list[tuple[str, str, float, int]] = []
    for d, row in df.iterrows():
        date_str = d.date().isoformat() if hasattr(d, "date") else str(d)[:10]
        try:
            close = float(row["Close"])
        except (ValueError, TypeError):
            continue
        try:
            vol_raw = row["Volume"]
            vol = int(vol_raw) if vol_raw == vol_raw else 0  # NaN check
        except (ValueError, TypeError):
            vol = 0
        rows.append((symbol_db, date_str, close, vol))

    if not rows:
        return 0

    with sqlite3.connect(db_path) as c:
        c.executemany(
            "INSERT OR REPLACE INTO prices(ticker, date, close, volume) VALUES (?,?,?,?)",
            rows,
        )
        c.commit()
    if not quiet:
        print(f"  {symbol_db} -> {db_path.name}: {len(rows)} rows ({rows[0][1]} to {rows[-1][1]})")
    return len(rows)


def refresh(backfill: bool, quiet: bool) -> dict:
    period = "2y" if backfill else "5d"
    stats = {"us_rows": 0, "br_rows": 0}

    if not quiet:
        print(f"[refresh-benchmarks] period={period}")
        print(f"  US ({len(US_BENCHMARKS)} symbols)")
    for sym in US_BENCHMARKS:
        stats["us_rows"] += _fetch(sym, sym, DB_US, period, quiet)

    if not quiet:
        print(f"  BR ({len(BR_BENCHMARKS_YF)} symbols)")
    for yf_sym, db_sym in BR_BENCHMARKS_YF:
        stats["br_rows"] += _fetch(yf_sym, db_sym, DB_BR, period, quiet)

    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backfill", action="store_true", help="fetch 2y em vez de 5d")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    stats = refresh(args.backfill, args.quiet)
    if not args.quiet:
        print(f"[done] us_rows={stats['us_rows']} br_rows={stats['br_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
