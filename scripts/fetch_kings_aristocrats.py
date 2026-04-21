"""Batch fetch: popula companies+prices+dividends+fundamentals para os tickers
Kings/Aristocrats que ainda não estão na DB US.

Uso:
    python scripts/fetch_kings_aristocrats.py          # roda sobre os que faltam
    python scripts/fetch_kings_aristocrats.py --all    # força re-fetch de todos
    python scripts/fetch_kings_aristocrats.py --period 5y
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_US = ROOT / "data" / "us_investments.db"
KA = ROOT / "config" / "kings_aristocrats.yaml"


def _missing_tickers() -> list[str]:
    ka = yaml.safe_load(KA.read_text(encoding="utf-8"))
    all_tickers = [e["ticker"] for e in ka["tickers"]]
    with sqlite3.connect(DB_US) as c:
        existing = {r[0] for r in c.execute("SELECT ticker FROM companies").fetchall()}
    return [t for t in all_tickers if t not in existing]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="força re-fetch de todos")
    ap.add_argument("--period", default="5y", help="período yfinance (default 5y)")
    ap.add_argument("--sleep", type=float, default=0.3, help="sleep entre tickers")
    args = ap.parse_args()

    ka = yaml.safe_load(KA.read_text(encoding="utf-8"))
    if args.all:
        tickers = [e["ticker"] for e in ka["tickers"]]
    else:
        tickers = _missing_tickers()

    print(f"[batch] vai fazer fetch de {len(tickers)} tickers (period={args.period})")

    from fetchers.yf_us_fetcher import run as yf_run

    ok: list[tuple[str, int, int]] = []
    bad: list[tuple[str, str]] = []
    for i, t in enumerate(tickers, 1):
        try:
            r = yf_run(t, period=args.period)
            ok.append((t, r["prices"], r["dividends"]))
            print(f"[{i}/{len(tickers)}] OK  {t:6s} prices={r['prices']:4d} div={r['dividends']:3d}")
        except Exception as e:
            bad.append((t, str(e)[:100]))
            print(f"[{i}/{len(tickers)}] ERR {t:6s} {str(e)[:80]}")
        if args.sleep:
            time.sleep(args.sleep)

    print(f"\n=== RESUMO ===")
    print(f"OK:  {len(ok)}")
    print(f"BAD: {len(bad)}")
    if bad:
        print("\nFalhas:")
        for t, err in bad:
            print(f"  {t:6s} {err}")


if __name__ == "__main__":
    main()
