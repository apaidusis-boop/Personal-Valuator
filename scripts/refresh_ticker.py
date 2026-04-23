"""refresh_ticker — fetch intraday quote + UPSERT em prices.

Motivo: daily cron 23:30 só apanha fechos. Análise intraday (hoje cedo, ou
ticker em movimento) precisa do último quote *agora*. Este script vai buscar
o quote atual via yfinance (funciona para US + BR com sufixo .SA) e persiste.

Uso:
    python scripts/refresh_ticker.py ACN
    python scripts/refresh_ticker.py --all-holdings
    python scripts/refresh_ticker.py --tickers ACN,ITSA4,JNJ
    python scripts/refresh_ticker.py --watchlist
    python scripts/refresh_ticker.py --all-holdings --quiet   # silent mode
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _market_of(ticker: str) -> str:
    """Heurística: ticker BR termina em número (4, 3, 11, etc.) e tem 4+letras+numbers.
    Refina consultando DB primeiro."""
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            row = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if row:
                return "br" if db == DB_BR else "us"
    # fallback: BR tickers têm número no fim
    return "br" if ticker and ticker[-1].isdigit() else "us"


def _yf_symbol(ticker: str, market: str) -> str:
    if market == "br" and not ticker.endswith(".SA"):
        return f"{ticker}.SA"
    return ticker


def fetch_quote(ticker: str) -> dict | None:
    """Devolve dict {ticker, price, date, volume, market, stale_close}.
    `price` é o último tick conhecido (pode ser pre-market/post-market).
    """
    import yfinance as yf

    market = _market_of(ticker)
    sym = _yf_symbol(ticker, market)
    tk = yf.Ticker(sym)

    # Tenta fast_info primeiro (mais rápido, dá quote actual)
    price = None
    volume = None
    try:
        fi = tk.fast_info
        price = float(fi.last_price) if fi.last_price else None
        volume = int(fi.last_volume) if fi.last_volume else None
    except Exception:  # noqa: BLE001
        pass

    # Fallback: history 1d intraday
    if price is None:
        try:
            hist = tk.history(period="1d", interval="1m")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
                volume = int(hist["Volume"].sum()) if "Volume" in hist else None
        except Exception:  # noqa: BLE001
            pass

    # Último recurso: daily
    if price is None:
        try:
            hist = tk.history(period="5d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
                volume = int(hist["Volume"].iloc[-1]) if "Volume" in hist else None
        except Exception:  # noqa: BLE001
            pass

    if price is None:
        return None

    return {
        "ticker": ticker,
        "price": price,
        "date": date.today().isoformat(),
        "volume": volume,
        "market": market,
    }


def _persist(q: dict) -> tuple[str, float | None]:
    """UPSERT no DB correcto. Devolve (status, prev_close) — status in {inserted,updated,same}."""
    db = DB_BR if q["market"] == "br" else DB_US
    with sqlite3.connect(db) as c:
        prev = c.execute(
            "SELECT close FROM prices WHERE ticker=? AND date<? ORDER BY date DESC LIMIT 1",
            (q["ticker"], q["date"]),
        ).fetchone()
        prev_close = prev[0] if prev else None

        existing = c.execute(
            "SELECT close FROM prices WHERE ticker=? AND date=?",
            (q["ticker"], q["date"]),
        ).fetchone()

        c.execute(
            """INSERT INTO prices (ticker, date, close, volume)
               VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (q["ticker"], q["date"], q["price"], q["volume"]),
        )
        c.commit()

        if existing is None:
            return "inserted", prev_close
        if abs(existing[0] - q["price"]) < 1e-6:
            return "same", prev_close
        return "updated", prev_close


def refresh(tickers: list[str], quiet: bool = False) -> list[dict]:
    results = []
    for tk in tickers:
        q = fetch_quote(tk)
        if q is None:
            if not quiet:
                print(f"  {tk:<8}  FAILED (no quote)")
            results.append({"ticker": tk, "status": "failed"})
            continue
        status, prev = _persist(q)
        change = None
        if prev and q["price"]:
            change = (q["price"] / prev - 1) * 100
        if not quiet:
            chg_str = f"{change:+.2f}%" if change is not None else "    -    "
            cur = "R$" if q["market"] == "br" else "$"
            print(f"  {tk:<8}  {cur}{q['price']:>9.2f}  {chg_str}   ({status})")
        results.append({**q, "status": status, "change_pct": change, "prev_close": prev})
    return results


def _load_tickers(scope: str) -> list[str]:
    tickers: set[str] = set()
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                if scope == "holdings":
                    for (t,) in c.execute(
                        "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                    ):
                        tickers.add(t)
                elif scope == "watchlist":
                    for (t,) in c.execute(
                        "SELECT ticker FROM companies WHERE is_holding=0"
                    ):
                        tickers.add(t)
                elif scope == "universe":
                    for (t,) in c.execute("SELECT ticker FROM companies"):
                        tickers.add(t)
            except sqlite3.OperationalError:
                pass
    return sorted(tickers)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("ticker", nargs="?", help="Single ticker")
    g.add_argument("--tickers", help="Comma-separated list")
    g.add_argument("--all-holdings", action="store_true")
    g.add_argument("--watchlist", action="store_true")
    g.add_argument("--universe", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.ticker:
        tickers = [args.ticker.upper()]
    elif args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    elif args.all_holdings:
        tickers = _load_tickers("holdings")
    elif args.watchlist:
        tickers = _load_tickers("watchlist")
    elif args.universe:
        tickers = _load_tickers("universe")
    else:
        ap.print_help()
        return 1

    if not args.quiet:
        print(f"Refreshing {len(tickers)} ticker(s)...")
    results = refresh(tickers, quiet=args.quiet)

    ok = sum(1 for r in results if r.get("status") in ("inserted", "updated", "same"))
    failed = sum(1 for r in results if r.get("status") == "failed")
    if not args.quiet:
        print(f"Done: {ok} ok, {failed} failed")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
