"""dividend_calendar — fetch upcoming dividend ex-dates / pay-dates.

Sources:
  - yfinance `t.calendar` ("Ex-Dividend Date", "Dividend Date")
  - yfinance `t.info` ("exDividendDate", "dividendDate", "dividendRate")

Persists to the existing `dividends` table in each market DB. Idempotent
(PK ticker, ex_date, kind). Existing historical rows are not touched —
INSERT OR IGNORE.

The Mission Control front-end reads upcoming rows via `upcomingDividends()`
in lib/db.ts (filters `ex_date BETWEEN today AND today+45`).

Uso:
    python fetchers/dividend_calendar.py                 # holdings BR + US
    python fetchers/dividend_calendar.py --all           # universe completo
    python fetchers/dividend_calendar.py ITSA4           # 1 ticker
    python fetchers/dividend_calendar.py --upcoming 60   # listar próximos 60d (sem fetch)
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _market_of(ticker: str) -> str | None:
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return market
    return None


def _yf_sym(ticker: str, market: str) -> str:
    return f"{ticker}.SA" if market == "br" else ticker


def _to_iso(d) -> str | None:
    if d is None:
        return None
    if hasattr(d, "isoformat"):
        return d.isoformat()[:10]
    s = str(d)[:10]
    return s if len(s) == 10 and s[4] == "-" else None


def _fetch_one(ticker: str, market: str) -> list[dict]:
    """Returns list of {ex_date, pay_date, amount, currency, source} for forward
    dividends. May return 0–2 rows depending on yfinance coverage."""
    import yfinance as yf

    sym = _yf_sym(ticker, market)
    t = yf.Ticker(sym)
    out: list[dict] = []
    today = date.today().isoformat()

    # Path 1: t.calendar — modern yfinance returns dict
    try:
        cal = t.calendar
        if isinstance(cal, dict):
            ex = cal.get("Ex-Dividend Date")
            pay = cal.get("Dividend Date")
            ex_iso = _to_iso(ex)
            pay_iso = _to_iso(pay)
            if ex_iso and ex_iso >= today:
                out.append({
                    "ex_date": ex_iso,
                    "pay_date": pay_iso,
                    "amount": None,
                    "currency": "BRL" if market == "br" else "USD",
                    "source": "yfinance_calendar",
                })
    except Exception:  # noqa: BLE001
        pass

    # Path 2: t.info — fallback / amount enrichment
    try:
        info = t.info or {}
        ex_ts = info.get("exDividendDate")
        pay_ts = info.get("dividendDate")
        amt = info.get("lastDividendValue") or info.get("dividendRate")
        # yfinance returns Unix timestamps
        ex_iso = pay_iso = None
        if isinstance(ex_ts, (int, float)) and ex_ts > 0:
            ex_iso = datetime.fromtimestamp(ex_ts, UTC).date().isoformat()
        if isinstance(pay_ts, (int, float)) and pay_ts > 0:
            pay_iso = datetime.fromtimestamp(pay_ts, UTC).date().isoformat()
        if ex_iso and ex_iso >= today:
            # If we already have this ex_date from path 1, enrich amount
            existing = next((r for r in out if r["ex_date"] == ex_iso), None)
            if existing:
                if existing["amount"] is None and amt:
                    existing["amount"] = float(amt)
                if existing["pay_date"] is None and pay_iso:
                    existing["pay_date"] = pay_iso
            else:
                out.append({
                    "ex_date": ex_iso,
                    "pay_date": pay_iso,
                    "amount": float(amt) if amt else None,
                    "currency": "BRL" if market == "br" else "USD",
                    "source": "yfinance_info",
                })
    except Exception:  # noqa: BLE001
        pass

    return out


def _persist(market: str, ticker: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    db = DB_BR if market == "br" else DB_US
    now_iso = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    inserted = 0
    with sqlite3.connect(db) as c:
        for r in rows:
            # amount may be None — `dividends.amount` is NOT NULL, so default to 0 placeholder
            amount = r.get("amount") if r.get("amount") is not None else 0.0
            try:
                cur = c.execute(
                    """INSERT INTO dividends
                         (ticker, ex_date, pay_date, amount, currency, kind, source, fetched_at)
                       VALUES (?,?,?,?,?,?,?,?)
                       ON CONFLICT(ticker, ex_date, kind) DO UPDATE SET
                         pay_date=COALESCE(excluded.pay_date, dividends.pay_date),
                         amount=CASE WHEN dividends.amount=0 AND excluded.amount<>0
                                     THEN excluded.amount ELSE dividends.amount END,
                         source=excluded.source,
                         fetched_at=excluded.fetched_at""",
                    (ticker, r["ex_date"], r.get("pay_date"), amount,
                     r["currency"], "dividend", r["source"], now_iso),
                )
                if cur.rowcount > 0:
                    inserted += 1
            except sqlite3.Error as e:
                print(f"  persist error {ticker} {r['ex_date']}: {e}")
        c.commit()
    return inserted


def _list_upcoming(days: int) -> list[tuple]:
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    out: list[tuple] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            for r in c.execute(
                """SELECT d.ticker, d.ex_date, d.pay_date, d.amount, d.currency,
                          c.name, c.is_holding
                   FROM dividends d LEFT JOIN companies c ON c.ticker=d.ticker
                   WHERE d.ex_date BETWEEN ? AND ?
                   ORDER BY d.ex_date ASC""",
                (today, cutoff),
            ):
                out.append((market, *r))
    return out


def _load_tickers(scope: str) -> list[tuple[str, str]]:
    """Returns list of (ticker, market). scope = holdings | universe."""
    out: list[tuple[str, str]] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if scope == "holdings":
                rows = c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ).fetchall()
            else:
                rows = c.execute("SELECT ticker FROM companies").fetchall()
            for (t,) in rows:
                out.append((t, market))
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=False)
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="default scope")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--upcoming", type=int, metavar="N",
                    help="lista próximos N dias (sem fetch)")
    args = ap.parse_args()

    if args.upcoming is not None:
        rows = _list_upcoming(args.upcoming)
        if not rows:
            print(f"(zero ex-dividends nos próximos {args.upcoming}d)")
            return 0
        print(f"Upcoming ex-dividends (≤ {args.upcoming}d):")
        for market, tk, ex, pay, amt, currency, name, is_h in rows:
            mark = "★" if is_h else " "
            sym = "R$" if market == "br" else "$"
            amt_s = f"{sym}{amt:.4f}" if amt else "(amount?)"
            print(f"  {ex}  {mark} {tk:<8} ({market})  ex={ex} pay={pay or '?'}  {amt_s}  {name or ''}")
        return 0

    if args.ticker:
        tk = args.ticker.upper()
        market = _market_of(tk)
        if not market:
            print(f"{tk}: not found in any DB")
            return 1
        targets = [(tk, market)]
    elif args.all:
        targets = _load_tickers("universe")
    else:
        targets = _load_tickers("holdings")

    print(f"Fetching dividend calendar for {len(targets)} ticker(s)...")
    total = 0
    for i, (tk, market) in enumerate(targets, 1):
        try:
            rows = _fetch_one(tk, market)
            n = _persist(market, tk, rows)
            total += n
            if rows:
                first = rows[0]
                amt_s = f"{first.get('amount'):.4f}" if first.get("amount") else "?"
                print(f"  [{i}/{len(targets)}] {tk}: ex={first['ex_date']} amt={amt_s} (+{n})")
        except Exception as e:  # noqa: BLE001
            print(f"  [{i}/{len(targets)}] {tk}: error — {e}")
    print(f"Persisted {total} new/updated row(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
