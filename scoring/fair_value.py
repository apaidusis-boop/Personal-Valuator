"""fair_value — compute consensus + our_fair (safety-margin) target prices.

Methods (per market × sector) — produces the *consensus* fair (Buffett/Graham
canonical reading):

  BR non-bank, non-FII  — Graham Number = sqrt(22.5 × EPS × BVPS)
  BR bank               — min(EPS × 10, BVPS × 1.5)   (both screen ceilings)
  US non-bank, non-REIT — min(EPS × 20, BVPS × 3)     (Buffett ceiling)
  US bank               — EPS × 12                     (mid-cycle multiple)
  US REIT               — BVPS × 2                     (proxy; AFFO/FFO later)
  BR FII                — VPA (NAV anchor)

The consensus is then narrowed by `scoring._safety.build_triplet()` into
(our_fair, buy_below, hold_low, hold_high, sell_above, action) using a
per-sector safety margin (config/safety_margins.yaml). Philosophy: 1-2%
*more* conservative than the canonical Buffett/Graham margin.

History: every `compute → persist` writes a NEW row keyed by
(ticker, method, computed_at) where computed_at is an ISO **timestamp**.
Same-day re-runs no longer overwrite; the full trajectory is queryable.
Mission Control's existing `MAX(computed_at)` query keeps surfacing the
latest correctly.

Confidence: each row carries `confidence_label` ∈ {cross_validated,
single_source, disputed} via `analytics.data_confidence`. Disputed inputs
still emit a number but flagged so the orchestrator / dossier can warn.

Uso:
    python -m scoring.fair_value ACN
    python -m scoring.fair_value --all
    python -m scoring.fair_value --holdings        (default)
    python -m scoring.fair_value --upside           (just print, no compute)
    python -m scoring.fair_value ACN --history     (print all rows for ticker)
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

# Columns added in v2 (2026-05-08). ALTER TABLE applied lazily via _ensure_v2_columns.
# Kept additive so existing INSERT OR REPLACE callers (none) don't break.
V2_COLUMNS = [
    ("our_fair",          "REAL"),
    ("buy_below",         "REAL"),
    ("hold_low",          "REAL"),
    ("hold_high",         "REAL"),
    ("sell_above",        "REAL"),
    ("action",            "TEXT"),
    ("margin_pct",        "REAL"),
    ("our_upside_pct",    "REAL"),
    ("confidence_label",  "TEXT"),
    ("confidence_score",  "REAL"),
    ("trigger",           "TEXT"),
]

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
        _ensure_v2_columns(c)


def _ensure_v2_columns(c: sqlite3.Connection) -> None:
    """Lazily add v2 columns. Idempotent: ignores 'duplicate column' errors."""
    existing = {r[1] for r in c.execute("PRAGMA table_info(fair_value)").fetchall()}
    for name, ctype in V2_COLUMNS:
        if name in existing:
            continue
        try:
            c.execute(f"ALTER TABLE fair_value ADD COLUMN {name} {ctype}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                raise
    c.commit()


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
    """Latest fundamentals snapshot. Prefers filings-derived (CVM/SEC) over
    yfinance — Phase LL Sprint 1.2 — because yfinance has documented bugs
    in BR coverage (PRIO3 ROE 9.7% yf vs 38.4% filings; BBDC4 EPS R$2.13 yf
    vs R$4.09 filings; the dual-share-class issue for BR banks).

    Fallback chain:
      1. fundamentals_from_filings   (CVM ITR/DFP, SEC XBRL when wired)
      2. fundamentals                (yfinance — last resort)

    Stamps `inputs.source` so dossier can show provenance ("filings" vs
    "yfinance_fallback").
    """
    # Try filings first
    try:
        fr = c.execute(
            """SELECT period_end, eps_ttm, bvps, roe_ttm, source, computed_at
               FROM fundamentals_from_filings WHERE ticker=?
               ORDER BY computed_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if fr and fr[1] is not None and fr[2] is not None:
            return {
                "period_end": fr[0],
                "eps": fr[1], "bvps": fr[2], "roe": fr[3],
                "pe": None, "pb": None, "dy": None,  # P/E P/B require price; not in filings
                "_source": fr[4],     # 'cvm_quarterly_single' | 'cvm_bank_quarterly' | 'sec_xbrl'
                "_provenance": "filings",
                "_computed_at": fr[5],
            }
    except sqlite3.OperationalError:
        pass  # table not yet created — fallback to yf
    # Fallback: yfinance fundamentals
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
        "_source": "yfinance",
        "_provenance": "yfinance_fallback",
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
    provenance = (f or {}).get("_provenance", "unknown")
    fund_source = (f or {}).get("_source", "unknown")

    method = None
    fair = None
    inputs = {"eps": eps, "bvps": bvps,
              "fundamentals_source": fund_source,
              "fundamentals_provenance": provenance}

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

    # Consensus upside (vs Buffett/Graham raw fair)
    upside = (fair / price - 1.0) * 100.0

    # Apply per-sector safety margin -> our_fair + action triplet
    from scoring._safety import build_triplet, resolve_margin
    margin_pct = resolve_margin(market, sector or None, ticker)
    triplet = build_triplet(consensus_fair=fair, price=price, margin_pct=margin_pct)
    our_upside = None
    if triplet["our_fair"] is not None:
        our_upside = (triplet["our_fair"] / price - 1.0) * 100.0

    # Confidence label (BR uses CVM cross-check; US is single-source today).
    confidence = _confidence_for(market, ticker)

    return {
        "ticker": ticker, "market": market, "sector": sector,
        "method": method,
        "fair_price": round(fair, 4),          # consensus
        "current_price": round(price, 4),
        "upside_pct": round(upside, 2),         # vs consensus
        "eps": eps, "bvps": bvps,
        "inputs": inputs,
        # v2 fields
        "our_fair": triplet["our_fair"],
        "buy_below": triplet["buy_below"],
        "hold_low": triplet["hold_low"],
        "hold_high": triplet["hold_high"],
        "sell_above": triplet["sell_above"],
        "action": triplet["action"],
        "margin_pct": triplet["margin_pct"],
        "our_upside_pct": round(our_upside, 2) if our_upside is not None else None,
        "confidence_label": confidence["label"],
        "confidence_score": confidence["score"],
        "confidence_detail": confidence.get("detail"),
    }


def _confidence_for(market: str, ticker: str) -> dict:
    """Lookup confidence from `analytics.data_confidence` if available; else
    default to 'single_source'. Lazy import to avoid hard dep at engine load."""
    try:
        from analytics.data_confidence import latest_label
        row = latest_label(market, ticker)
        if row:
            return row
    except Exception:
        pass
    return {"label": "single_source", "score": None, "detail": None}


def persist(result: dict, *, trigger: str | None = None) -> None:
    """Append-only persist. Uses ISO timestamp (not date) so same-day re-runs
    each get their own row — full history queryable via ORDER BY computed_at.
    `trigger` is optional context (e.g. "manual", "filing:BBDC4:2026-05-08",
    "cron:daily") for downstream filtering.
    """
    market = result["market"]
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    now_iso = datetime.now(UTC).isoformat(timespec="seconds")
    import json as _json
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT INTO fair_value
                 (ticker, method, fair_price, current_price, upside_pct,
                  eps, bvps, sector, inputs_json, computed_at,
                  our_fair, buy_below, hold_low, hold_high, sell_above,
                  action, margin_pct, our_upside_pct,
                  confidence_label, confidence_score, trigger)
               VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?, ?,?,?)""",
            (
                result["ticker"], result["method"], result["fair_price"],
                result["current_price"], result["upside_pct"],
                result.get("eps"), result.get("bvps"), result.get("sector"),
                _json.dumps(result.get("inputs") or {}, ensure_ascii=False),
                now_iso,
                result.get("our_fair"), result.get("buy_below"),
                result.get("hold_low"), result.get("hold_high"),
                result.get("sell_above"),
                result.get("action"), result.get("margin_pct"),
                result.get("our_upside_pct"),
                result.get("confidence_label"), result.get("confidence_score"),
                trigger or "manual",
            ),
        )
        c.commit()


def history(ticker: str, market: str, *, limit: int = 50) -> list[dict]:
    """Return historical fair_value rows for ticker, oldest→newest."""
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        rows = c.execute(
            """SELECT computed_at, method, fair_price, our_fair, current_price,
                      action, confidence_label, trigger
               FROM fair_value WHERE ticker=?
               ORDER BY computed_at DESC LIMIT ?""",
            (ticker, limit),
        ).fetchall()
    out = [
        {"computed_at": r[0], "method": r[1], "fair_price": r[2], "our_fair": r[3],
         "current_price": r[4], "action": r[5], "confidence_label": r[6],
         "trigger": r[7]}
        for r in rows
    ]
    out.reverse()  # oldest first
    return out


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
    ap.add_argument("--history", action="store_true",
                    help="(com --ticker) imprime trajectória histórica do ticker")
    ap.add_argument("--trigger", default="manual",
                    help="contexto persistido em fair_value.trigger (ex: 'filing:BBDC4:2026-05-08')")
    args = ap.parse_args()

    if args.ticker and args.history:
        tk = args.ticker.upper()
        for market, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                if not c.execute("SELECT 1 FROM companies WHERE ticker=?", (tk,)).fetchone():
                    continue
            print(f"\n=== {tk} fair value history ({market.upper()}) ===")
            for h in history(tk, market, limit=200):
                print(
                    f"  {h['computed_at']:<25} {h['method']:<18} "
                    f"fair={h['fair_price']:>9.2f} our={h['our_fair'] or 0:>9.2f} "
                    f"price={h['current_price']:>9.2f} {h['action'] or 'N/A':<11} "
                    f"[{h['confidence_label'] or '-'}] trig={h['trigger']}"
                )
            return 0
        print(f"{tk}: not found")
        return 1

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
            persist(r, trigger=args.trigger)
            ok += 1
            our = r.get("our_fair")
            our_str = f"{our:>10.2f}" if our is not None else "       N/A"
            act = r.get("action") or "—"
            conf = (r.get("confidence_label") or "-")[:6]
            print(
                f"  {tk:<8} {r['method']:<18} fair={r['fair_price']:>10.2f}"
                f"  our={our_str}  cur={r['current_price']:>10.2f}"
                f"  {act:<11}  [{conf}]"
            )
        except Exception as e:  # noqa: BLE001
            print(f"  {tk}: error — {e}")
            skipped += 1
    print(f"\nPersisted {ok} | skipped {skipped} (insufficient data).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
