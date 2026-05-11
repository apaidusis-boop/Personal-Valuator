"""earnings_calendar — fetch próximas datas de earnings via yfinance.

Persiste em tabela `earnings_calendar` (criada on-demand).
Schema: ticker, market, earnings_date (ISO), period_type, fetched_at, source.

Uso:
    python fetchers/earnings_calendar.py --holdings
    python fetchers/earnings_calendar.py ACN
    python fetchers/earnings_calendar.py --all
    python fetchers/earnings_calendar.py --upcoming 30   # lista próximas 30d
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS earnings_calendar (
    ticker         TEXT NOT NULL,
    earnings_date  TEXT NOT NULL,
    period_type    TEXT,
    estimate_eps   REAL,
    fetched_at     TEXT NOT NULL,
    source         TEXT NOT NULL DEFAULT 'yfinance',
    PRIMARY KEY (ticker, earnings_date)
);
CREATE INDEX IF NOT EXISTS idx_earnings_date ON earnings_calendar(earnings_date);
"""


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def _market_of(ticker: str) -> str:
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            row = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if row:
                return market
    return "us"


def _yf_sym(ticker: str, market: str) -> str:
    return f"{ticker}.SA" if market == "br" else ticker


def _fetch_one(ticker: str) -> list[dict]:
    import yfinance as yf
    market = _market_of(ticker)
    sym = _yf_sym(ticker, market)
    t = yf.Ticker(sym)
    out: list[dict] = []
    try:
        cal = t.calendar
        if cal is None:
            return []
        if isinstance(cal, dict):
            # recent yfinance returns a dict with "Earnings Date" as list of dates
            ed = cal.get("Earnings Date")
            if isinstance(ed, list):
                for d in ed:
                    if d is None:
                        continue
                    ds = d.isoformat() if hasattr(d, "isoformat") else str(d)
                    out.append({"ticker": ticker, "market": market,
                                "earnings_date": ds[:10], "period_type": "estimated"})
            elif ed is not None:
                ds = ed.isoformat() if hasattr(ed, "isoformat") else str(ed)
                out.append({"ticker": ticker, "market": market,
                            "earnings_date": ds[:10], "period_type": "estimated"})
        else:
            # DataFrame legacy
            try:
                ed_col = cal.loc["Earnings Date"]
                for val in ed_col.values:
                    if val is None:
                        continue
                    ds = val.isoformat() if hasattr(val, "isoformat") else str(val)
                    out.append({"ticker": ticker, "market": market,
                                "earnings_date": ds[:10], "period_type": "estimated"})
            except Exception:  # noqa: BLE001
                pass
    except Exception as e:  # noqa: BLE001
        print(f"  {ticker}: error fetching calendar — {e}")
    return out


def _persist(rows: list[dict]) -> int:
    if not rows:
        return 0
    count = 0
    now_iso = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_market: dict[str, list[dict]] = {"br": [], "us": []}
    for r in rows:
        by_market.setdefault(r["market"], []).append(r)

    for market, items in by_market.items():
        if not items:
            continue
        db = DB_BR if market == "br" else DB_US
        _ensure_schema(db)
        with sqlite3.connect(db) as c:
            for r in items:
                try:
                    c.execute(
                        """INSERT INTO earnings_calendar
                             (ticker, earnings_date, period_type, fetched_at, source)
                           VALUES (?,?,?,?,?)
                           ON CONFLICT(ticker, earnings_date) DO UPDATE SET
                             period_type=excluded.period_type,
                             fetched_at=excluded.fetched_at""",
                        (r["ticker"], r["earnings_date"], r.get("period_type", "estimated"),
                         now_iso, "yfinance"),
                    )
                    count += 1
                except sqlite3.Error as e:
                    print(f"  persist error {r['ticker']}: {e}")
            c.commit()
    return count


def _list_upcoming(days: int) -> list[tuple]:
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    today = date.today().isoformat()
    out: list[tuple] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        _ensure_schema(db)
        with sqlite3.connect(db) as c:
            for r in c.execute(
                """SELECT e.ticker, e.earnings_date, c.name, c.is_holding
                   FROM earnings_calendar e LEFT JOIN companies c ON e.ticker=c.ticker
                   WHERE e.earnings_date >= ? AND e.earnings_date <= ?
                   ORDER BY e.earnings_date ASC""",
                (today, cutoff),
            ):
                out.append((r[0], r[1], r[2] or "", bool(r[3]), market))
    return out


def _load_tickers(scope: str) -> list[str]:
    tickers: set[str] = set()
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            if scope == "holdings":
                for (t,) in c.execute("SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"):
                    tickers.add(t)
            elif scope == "all":
                for (t,) in c.execute("SELECT ticker FROM companies"):
                    tickers.add(t)
    return sorted(tickers)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=False)
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--upcoming", type=int, help="Só lista próximos N dias (sem fetch)")
    args = ap.parse_args()

    if args.upcoming is not None:
        rows = _list_upcoming(args.upcoming)
        if not rows:
            print(f"(sem earnings nos próximos {args.upcoming}d)")
            return 0
        print(f"Upcoming earnings (≤ {args.upcoming}d):")
        for tk, dt, name, is_h, market in rows:
            mark = "★" if is_h else " "
            print(f"  {dt}  {mark} {tk:<8} ({market})  {name}")
        return 0

    if args.ticker:
        tickers = [args.ticker.upper()]
    elif args.all:
        tickers = _load_tickers("all")
    else:
        tickers = _load_tickers("holdings")

    print(f"Fetching earnings calendar for {len(tickers)} ticker(s)...")
    all_rows: list[dict] = []
    for i, tk in enumerate(tickers, 1):
        rows = _fetch_one(tk)
        if rows:
            print(f"  [{i}/{len(tickers)}] {tk}: {len(rows)} date(s) → {rows[0]['earnings_date']}")
        all_rows.extend(rows)
    n = _persist(all_rows)
    print(f"Persisted {n} row(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
