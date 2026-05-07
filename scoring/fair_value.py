"""fair_value — compute target price + upside % from latest fundamentals.

Methods (per market × sector):
  BR non-bank, non-FII  — Graham Number = sqrt(22.5 × EPS × BVPS)
  BR bank               — min(EPS × 10, BVPS × 1.5)   (passes both screen ceilings)
  US non-bank, non-REIT — min(EPS × 20, BVPS × 3)     (Buffett ceiling)
  US bank               — EPS × 12                     (mid-cycle multiple)
  US REIT               — BVPS × 2  (proxy; AFFO/FFO when available later)

Store: `fair_value` table (auto-created). Idempotent (PK ticker, method, computed_at_date).
The Mission Control surfaces the latest row per ticker via lib/db.ts.

Uso:
    python -m scoring.fair_value ACN
    python -m scoring.fair_value --all
    python -m scoring.fair_value --holdings        (default)
    python -m scoring.fair_value --upside           (just print, no compute)
"""
from __future__ import annotations

import argparse
import math
import sqlite3
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS fair_value (
    ticker          TEXT NOT NULL,
    method          TEXT NOT NULL,
    fair_price      REAL,
    current_price   REAL,
    upside_pct      REAL,
    eps             REAL,
    bvps            REAL,
    sector          TEXT,
    inputs_json     TEXT,
    computed_at     TEXT NOT NULL,
    PRIMARY KEY (ticker, method, computed_at)
);
CREATE INDEX IF NOT EXISTS idx_fv_ticker ON fair_value(ticker);
"""

# Sector keys (lowercase) that are FIIs / REITs / Banks
_BANK_TOKENS = {"bank", "banks", "banco", "bancos"}
_FII_SECTORS = {
    "logística", "logistica", "shopping", "papel (cri)", "híbrido", "hibrido",
    "corporativo", "tijolo", "residencial", "agro", "fundo de fundos", "ffii",
}
_REIT_TOKENS = {"reit", "reits"}


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def _is_bank(sector: str | None) -> bool:
    if not sector:
        return False
    s = sector.strip().lower()
    return any(tok in s for tok in _BANK_TOKENS)


def _is_fii(sector: str | None) -> bool:
    if not sector:
        return False
    return sector.strip().lower() in _FII_SECTORS


def _is_reit(sector: str | None) -> bool:
    if not sector:
        return False
    s = sector.strip().lower()
    return any(tok in s for tok in _REIT_TOKENS)


def _latest_price(c: sqlite3.Connection, ticker: str) -> float | None:
    r = c.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return r[0] if r else None


def _latest_fundamentals(c: sqlite3.Connection, ticker: str) -> dict | None:
    r = c.execute(
        """SELECT period_end, eps, bvps, roe, pe, pb, dy
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    return {
        "period_end": r[0], "eps": r[1], "bvps": r[2],
        "roe": r[3], "pe": r[4], "pb": r[5], "dy": r[6],
    }


def _company(c: sqlite3.Connection, ticker: str) -> dict | None:
    r = c.execute(
        "SELECT ticker, name, sector, is_holding FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    return {"ticker": r[0], "name": r[1], "sector": r[2], "is_holding": bool(r[3])}


def compute(ticker: str, market: str) -> dict | None:
    """Returns {method, fair_price, current_price, upside_pct, eps, bvps, sector, inputs}.
    Returns None if data insufficient."""
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        co = _company(c, ticker)
        if not co:
            return None
        f = _latest_fundamentals(c, ticker)
        price = _latest_price(c, ticker)

    sector = co.get("sector") or ""
    eps = (f or {}).get("eps")
    bvps = (f or {}).get("bvps")

    method = None
    fair = None
    inputs = {"eps": eps, "bvps": bvps}

    if market == "br":
        if _is_fii(sector):
            # FII fair value = NAV (VPA). Read fii_fundamentals if available.
            with sqlite3.connect(db) as c:
                r = c.execute(
                    "SELECT vpa FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                    (ticker,),
                ).fetchone()
            vpa = r[0] if r else None
            if vpa and vpa > 0:
                method, fair = "fii_nav", float(vpa)
                inputs = {"vpa": vpa}
        elif _is_bank(sector):
            if eps and bvps and eps > 0 and bvps > 0:
                method = "br_bank_mult"
                fair = min(eps * 10.0, bvps * 1.5)
        else:
            if eps and bvps and eps > 0 and bvps > 0:
                method = "graham_number"
                fair = math.sqrt(22.5 * eps * bvps)
    else:  # us
        if _is_reit(sector):
            if bvps and bvps > 0:
                method, fair = "reit_pb_proxy", bvps * 2.0
        elif _is_bank(sector):
            if eps and eps > 0:
                method, fair = "us_bank_pe12", eps * 12.0
        else:
            if eps and bvps and eps > 0 and bvps > 0:
                method = "buffett_ceiling"
                fair = min(eps * 20.0, bvps * 3.0)

    if method is None or fair is None or price is None or price <= 0:
        return None

    upside = (fair / price - 1.0) * 100.0
    return {
        "ticker": ticker, "market": market, "sector": sector,
        "method": method,
        "fair_price": round(fair, 4),
        "current_price": round(price, 4),
        "upside_pct": round(upside, 2),
        "eps": eps, "bvps": bvps,
        "inputs": inputs,
    }


def persist(result: dict) -> None:
    market = result["market"]
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    today = date.today().isoformat()
    import json as _json
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO fair_value
                 (ticker, method, fair_price, current_price, upside_pct,
                  eps, bvps, sector, inputs_json, computed_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (result["ticker"], result["method"], result["fair_price"],
             result["current_price"], result["upside_pct"],
             result.get("eps"), result.get("bvps"), result.get("sector"),
             _json.dumps(result.get("inputs") or {}, ensure_ascii=False),
             today),
        )
        c.commit()


def _load_tickers(scope: str) -> list[tuple[str, str]]:
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
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--upside", action="store_true",
                    help="apenas listar último fair value persistido")
    args = ap.parse_args()

    if args.upside:
        for market, db in (("br", DB_BR), ("us", DB_US)):
            _ensure_schema(db)
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    """SELECT fv.ticker, fv.method, fv.fair_price, fv.current_price,
                              fv.upside_pct, fv.computed_at, c.is_holding
                       FROM fair_value fv LEFT JOIN companies c ON c.ticker=fv.ticker
                       WHERE fv.computed_at = (
                         SELECT MAX(computed_at) FROM fair_value f2
                         WHERE f2.ticker=fv.ticker AND f2.method=fv.method
                       )
                       ORDER BY fv.upside_pct DESC""",
                ).fetchall()
            if rows:
                print(f"\n=== {market.upper()} fair value (most recent) ===")
                for tk, m, fair, cur, up, dt, h in rows:
                    mark = "★" if h else " "
                    print(f"  {mark} {tk:<8} {m:<18} fair={fair:>10.2f}  cur={cur:>10.2f}  upside={up:>+6.1f}%  ({dt})")
        return 0

    if args.ticker:
        tk = args.ticker.upper()
        # detect market
        market = None
        for m, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                if c.execute("SELECT 1 FROM companies WHERE ticker=?", (tk,)).fetchone():
                    market = m
                    break
        if not market:
            print(f"{tk}: not found")
            return 1
        targets = [(tk, market)]
    elif args.all:
        targets = _load_tickers("universe")
    else:
        targets = _load_tickers("holdings")

    print(f"Computing fair value for {len(targets)} ticker(s)...")
    ok = skipped = 0
    for tk, market in targets:
        try:
            r = compute(tk, market)
            if r is None:
                skipped += 1
                continue
            persist(r)
            ok += 1
            print(f"  {tk:<8} {r['method']:<18} fair={r['fair_price']:>10.2f}"
                  f"  cur={r['current_price']:>10.2f}  upside={r['upside_pct']:>+6.1f}%")
        except Exception as e:  # noqa: BLE001
            print(f"  {tk}: error — {e}")
            skipped += 1
    print(f"\nPersisted {ok} | skipped {skipped} (insufficient data).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
