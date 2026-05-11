"""Backfill goodwill, intangibles, total_assets, tangible book value into
`fundamentals` for US (and BR where yfinance has data).

Why this exists: the canonical Buffett-ceiling formula `min(EPS×20, BVPS×3)`
unfairly destroys consumer staples / consumer discretionary names whose brand
equity is OFF balance sheet. KO trades at P/B 10 because its $98B brand value
(Interbrand) is not in BVPS — only goodwill from acquisitions is. PG and JNJ
are NEGATIVE tangible book ($-12B and $-18B respectively) because intangibles
+ goodwill exceed shareholders' equity.

This script doesn't change fair_value DECISIONS. It enriches the dossier
context so the LLM personas (synthetic_ic) can reason about intangible
context. Future: a sector-specific brand premium adjustment can use these.

Idempotent: ALTER TABLE guarded by 'duplicate column' check; UPDATE SET
keyed on (ticker, period_end) writes to the latest row.

Uso:
    python scripts/backfill_intangibles.py                      # all US + BR holdings
    python scripts/backfill_intangibles.py --us-only
    python scripts/backfill_intangibles.py --ticker KO          # single
    python scripts/backfill_intangibles.py --schema-only        # ALTER TABLE then exit
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

NEW_COLS = [
    ("goodwill", "REAL"),
    ("other_intangibles", "REAL"),
    ("total_assets", "REAL"),
    ("tangible_book_value", "REAL"),
    ("intangible_pct_assets", "REAL"),
]


def _ensure_columns(db: Path) -> None:
    with sqlite3.connect(db) as c:
        existing = {r[1] for r in c.execute("PRAGMA table_info(fundamentals)").fetchall()}
        for name, ctype in NEW_COLS:
            if name in existing:
                continue
            try:
                c.execute(f"ALTER TABLE fundamentals ADD COLUMN {name} {ctype}")
                print(f"  [{db.name}] added column: {name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e).lower():
                    raise
        c.commit()


def _ensure_all_schemas() -> None:
    print("Ensuring schema for both DBs...")
    for db in (DB_BR, DB_US):
        if db.exists():
            _ensure_columns(db)


def _yfinance_intangibles(ticker: str) -> dict | None:
    """Fetch goodwill + intangibles + total assets + tangible BV from yfinance.
    Returns dict with these keys or None if not available."""
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance not installed; aborting")
        return None

    yf_ticker = ticker
    # BR tickers need .SA suffix on yfinance
    if "." not in ticker and not ticker.startswith("$") and len(ticker) <= 7 and ticker[-1].isdigit():
        yf_ticker = ticker + ".SA"

    try:
        t = yf.Ticker(yf_ticker)
        bs = t.balance_sheet
        if bs is None or bs.empty:
            return None
        latest = bs.columns[0]

        def _get(key):
            try:
                return float(bs.loc[key, latest]) if key in bs.index else None
            except Exception:
                return None

        goodwill = _get("Goodwill") or 0.0
        intangibles = _get("Other Intangible Assets") or 0.0
        total_assets = _get("Total Assets")
        tangible_bv = _get("Tangible Book Value")
        if tangible_bv is None:
            tangible_bv = _get("Net Tangible Assets")

        out = {
            "goodwill": goodwill if goodwill else None,
            "other_intangibles": intangibles if intangibles else None,
            "total_assets": total_assets,
            "tangible_book_value": tangible_bv,
        }
        # Compute intangible_pct_assets if both numerator and denominator available
        denom = total_assets
        numer = (goodwill or 0) + (intangibles or 0)
        if denom and denom > 0 and numer > 0:
            out["intangible_pct_assets"] = round(numer / denom, 4)
        else:
            out["intangible_pct_assets"] = None

        return out
    except Exception as e:
        print(f"  [{ticker}] yfinance error: {type(e).__name__}: {e}")
        return None


def _persist(db: Path, ticker: str, data: dict) -> bool:
    """Write to latest fundamentals row for the ticker. Returns True if written."""
    if not db.exists():
        return False
    if not any(data.get(k) is not None for k, _ in NEW_COLS):
        return False
    with sqlite3.connect(db) as c:
        # Find latest period_end for the ticker
        r = c.execute(
            "SELECT period_end FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if not r:
            return False
        period_end = r[0]
        sets = []
        vals = []
        for col, _ in NEW_COLS:
            if data.get(col) is not None:
                sets.append(f"{col}=?")
                vals.append(data[col])
        if not sets:
            return False
        vals.extend([ticker, period_end])
        c.execute(
            f"UPDATE fundamentals SET {', '.join(sets)} WHERE ticker=? AND period_end=?",
            vals,
        )
        c.commit()
        return True


def _list_targets(market: str | None, ticker: str | None) -> list[tuple[str, str]]:
    if ticker:
        # Detect which DB has it
        for mkt, db in (("us", DB_US), ("br", DB_BR)):
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                    return [(ticker, mkt)]
        return [(ticker, "us")]  # default

    out: list[tuple[str, str]] = []
    for mkt, db in (("us", DB_US), ("br", DB_BR)):
        if market and market != mkt:
            continue
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            rows = c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ).fetchall()
            holdings = [r[0] for r in rows]
            # Also include companies (watchlist) — but limit BR FIIs are skipped (no balance sheet)
            rows = c.execute("SELECT ticker, sector FROM companies").fetchall()
            for tk, sector in rows:
                if mkt == "br" and sector and any(s in sector.lower() for s in ("logística", "logistica", "shopping", "papel (cri)", "híbrido", "hibrido", "corporativo", "tijolo", "residencial")):
                    continue  # FIIs — no traditional balance sheet
                out.append((tk, mkt))
            # Also ensure holdings are in
            for tk in holdings:
                if (tk, mkt) not in out:
                    out.append((tk, mkt))
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", help="Backfill single ticker only")
    ap.add_argument("--us-only", action="store_true")
    ap.add_argument("--br-only", action="store_true")
    ap.add_argument("--schema-only", action="store_true",
                    help="Apply ALTER TABLE and exit (no fetch)")
    ap.add_argument("--limit", type=int, default=None, help="Cap number of tickers")
    ap.add_argument("--sleep", type=float, default=0.5,
                    help="Sleep between yfinance calls to respect rate limits")
    args = ap.parse_args()

    _ensure_all_schemas()
    if args.schema_only:
        print("schema-only mode — done.")
        return 0

    market_filter = "us" if args.us_only else ("br" if args.br_only else None)
    targets = _list_targets(market_filter, args.ticker)
    if args.limit:
        targets = targets[: args.limit]

    print(f"\nBackfilling {len(targets)} ticker(s)...")
    written = skipped = errored = 0
    t0 = time.time()
    for i, (tk, mkt) in enumerate(targets, 1):
        try:
            data = _yfinance_intangibles(tk)
            if data is None:
                skipped += 1
                continue
            db = DB_BR if mkt == "br" else DB_US
            if _persist(db, tk, data):
                ipa = data.get("intangible_pct_assets")
                ipa_s = f"{ipa*100:.1f}%" if ipa is not None else "—"
                print(f"  [{i:>3}/{len(targets)}] {mkt}/{tk:<8} intangible_pct_assets={ipa_s}  goodwill=${(data.get('goodwill') or 0)/1e9:.1f}B")
                written += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  [{i:>3}/{len(targets)}] {mkt}/{tk:<8} ERROR: {type(e).__name__}: {e}")
            errored += 1
        if args.sleep:
            time.sleep(args.sleep)

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.0f}s. Written: {written} | Skipped: {skipped} | Errored: {errored}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
