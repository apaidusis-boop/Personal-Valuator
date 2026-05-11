"""data_confidence — cross-source agreement label per ticker.

Today (2026-05-08) BR has two genuine sources we can triangulate:
  - fundamentals  (yfinance commercial)        — TTM EPS/BVPS/ROE snapshot
  - quarterly_history (CVM official ITR/DFP)   — actual filing periods

This module derives equivalent metrics from CVM (ROE_ttm, EPS_ttm) and
compares against yfinance, emitting a `data_confidence` row per ticker:

  cross_validated   metrics within tolerance (rel delta ≤ 25%)
  single_source     CVM data missing / too stale (>180d) / methodology gap
  disputed          metrics disagree by >50%; downstream consumers should warn

US is single-source today (no CVM equivalent yet). Returned label is always
'single_source' for market='us' until SEC EDGAR XBRL parser lands.

Why presence-based fallback first: even when the deltas are noisy, the *fact*
that two independent sources have data for a ticker is itself a signal. We
upgrade to numeric agreement when both ROE and EPS triangulate within tolerance.

CLI:
    python -m analytics.data_confidence BBDC4 [--market br]
    python -m analytics.data_confidence --holdings        (default)
    python -m analytics.data_confidence --all
    python -m analytics.data_confidence --json
"""
from __future__ import annotations

import argparse
import json
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

SCHEMA = """
CREATE TABLE IF NOT EXISTS data_confidence (
    ticker          TEXT NOT NULL,
    market          TEXT NOT NULL,
    label           TEXT NOT NULL,         -- cross_validated / single_source / disputed
    score           REAL,                  -- 0.0-1.0 (1.0 = full agreement)
    detail_json     TEXT,
    computed_at     TEXT NOT NULL,
    PRIMARY KEY (ticker, computed_at)
);
CREATE INDEX IF NOT EXISTS idx_dc_ticker ON data_confidence(ticker);
"""

# Tolerances (relative |a-b| / max(|a|,|b|))
ROE_OK = 0.25      # ≤25% delta -> agree
ROE_DISPUTED = 0.50
EPS_OK = 0.25
EPS_DISPUTED = 0.60   # EPS amplifies more given share count noise (treasury, splits)


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def _rel_delta(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    if a == 0 and b == 0:
        return 0.0
    denom = max(abs(a), abs(b))
    if denom == 0:
        return None
    return abs(a - b) / denom


def _yf_snapshot(c: sqlite3.Connection, ticker: str) -> dict | None:
    """Latest fundamentals row, but pull shares_outstanding from the most
    recent row that actually has it populated (ENRICH job runs less often
    than the daily snapshot, so latest snapshot rarely has shares)."""
    r = c.execute(
        """SELECT period_end, eps, bvps, roe
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    s = c.execute(
        """SELECT shares_outstanding FROM fundamentals
           WHERE ticker=? AND shares_outstanding IS NOT NULL
           ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    return {"period_end": r[0], "eps": r[1], "bvps": r[2], "roe": r[3],
            "shares_outstanding": (s[0] if s else None)}


def _cvm_ttm(c: sqlite3.Connection, ticker: str) -> dict | None:
    """Read the canonical filings-derived TTM. Phase LL upgrade (2026-05-08):
    delegate to fundamentals_from_filings, which already resolves YTD for
    banks (was a bug here before — banks live in bank_quarterly_history
    YTD-cumulative; this module used to read quarterly_single only and
    return None for banks → BBDC4 was wrongly flagged 'disputed' for
    that reason, not real disagreement).
    """
    try:
        r = c.execute(
            """SELECT period_end, net_income_ttm, equity, eps_ttm, roe_ttm,
                      n_quarters, source
               FROM fundamentals_from_filings WHERE ticker=?
               ORDER BY computed_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
    except sqlite3.OperationalError:
        r = None
    if r and r[1] is not None and r[2] is not None:
        return {
            "latest_period": r[0],
            "ni_ttm": r[1],
            "equity_avg": r[2],          # use latest equity (close to avg for stable companies)
            "eps_cvm_ready": r[3],       # may already have EPS_TTM with proper shares
            "roe_cvm_ready": r[4],
            "n_quarters": r[5] or 4,
            "source": r[6],
        }
    # Fallback: legacy direct read of quarterly_single (BR non-bank only).
    # Table doesn't exist on US DB — guard with try.
    try:
        rows = c.execute(
            """SELECT period_end, net_income, equity
               FROM quarterly_single
               WHERE ticker=? AND net_income IS NOT NULL
               ORDER BY period_end DESC LIMIT 4""",
            (ticker,),
        ).fetchall()
    except sqlite3.OperationalError:
        return None
    if not rows:
        return None
    nis = [rr[1] for rr in rows if rr[1] is not None]
    eqs = [rr[2] for rr in rows if rr[2] is not None]
    if not nis or not eqs:
        return None
    return {
        "latest_period": rows[0][0],
        "ni_ttm": sum(nis),
        "equity_avg": sum(eqs) / len(eqs),
        "n_quarters": len(rows),
        "source": "quarterly_single_legacy",
    }


def _staleness_days(latest_period_iso: str) -> int:
    try:
        d = date.fromisoformat(latest_period_iso[:10])
    except ValueError:
        return 9999
    return (date.today() - d).days


def evaluate(ticker: str, market: str) -> dict:
    """Compute confidence label for a single ticker.

    Returns dict: {ticker, market, label, score, detail{...}, computed_at}.
    Always returns a row (never None) — single_source is the floor.
    """
    now_iso = datetime.now(UTC).isoformat(timespec="seconds")
    out: dict = {"ticker": ticker, "market": market, "computed_at": now_iso}

    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        yf = _yf_snapshot(c, ticker)
        cvm = _cvm_ttm(c, ticker)   # for US: reads from fundamentals_from_filings (SEC XBRL)

    if yf is None and cvm is None:
        out.update({"label": "single_source", "score": 0.0,
                    "detail": {"reason": "no_data_either_source"}})
        return out
    if cvm is None:
        out.update({"label": "single_source", "score": 0.3,
                    "detail": {"reason": "no_cvm_quarterly_history",
                               "yf_period_end": yf["period_end"]}})
        return out
    if yf is None:
        out.update({"label": "single_source", "score": 0.3,
                    "detail": {"reason": "no_yf_fundamentals",
                               "cvm_latest_period": cvm["latest_period"]}})
        return out

    stale_days = _staleness_days(cvm["latest_period"])
    # 270d covers normal CVM filing lag: Q3 (Sep 30) is filed in mid-Nov;
    # DFP for prior FY (Dec 31) lands by end-Mar. So worst case "fresh enough"
    # is ~245d (Q3 from prior year if DFP not yet ingested).
    if stale_days > 270:
        out.update({"label": "single_source", "score": 0.4,
                    "detail": {"reason": "cvm_stale",
                               "cvm_latest_period": cvm["latest_period"],
                               "stale_days": stale_days}})
        return out
    # n_quarters check: BR quarterly_single needs 4 actual quarters; US
    # SEC XBRL via restitch_fy_minus_ytd uses 3 facts to compute TTM (1
    # quarter + 1 FY + 1 prior quarter) — that's still a valid TTM, just
    # different shape. Tolerate n_quarters >= 1 for sec_xbrl source.
    is_sec_xbrl = (cvm.get("source") == "sec_xbrl")
    min_q = 1 if is_sec_xbrl else 4
    if cvm["n_quarters"] < min_q:
        out.update({"label": "single_source", "score": 0.5,
                    "detail": {"reason": "filings_insufficient_quarters",
                               "n_quarters": cvm["n_quarters"]}})
        return out

    # --- Numeric cross-check ---
    # Prefer the canonical TTM values from fundamentals_from_filings when the
    # deriver has run; fallback to inline computation otherwise.
    roe_cvm = cvm.get("roe_cvm_ready")
    if roe_cvm is None and cvm.get("equity_avg"):
        roe_cvm = cvm["ni_ttm"] / cvm["equity_avg"]
    roe_yf = yf.get("roe")
    roe_delta = _rel_delta(roe_yf, roe_cvm)

    eps_cvm = cvm.get("eps_cvm_ready")
    if eps_cvm is None:
        shares = yf.get("shares_outstanding")
        eps_cvm = (cvm["ni_ttm"] * 1000.0 / shares) if (shares and shares > 0) else None
    eps_yf = yf.get("eps")
    eps_delta = _rel_delta(eps_yf, eps_cvm)

    # Phase LL Sprint 1.5 — 3-way voting with Fundamentus scrape.
    # When 2/3 sources agree and the 3rd is an outlier, flag the outlier
    # so future investigation surfaces it (VALE3 is the canonical case
    # we found: yf + Fundamentus both say EPS ~R$3.3; our CVM says R$6.86
    # because parser under-counts Q4'24 settlement loss).
    fund_eps = fund_roe = fund_delta_yf_eps = fund_delta_yf_roe = None
    fund_delta_cvm_eps = fund_delta_cvm_roe = None
    outlier_signal = None
    try:
        fr = c.execute(
            """SELECT eps, roe FROM fundamentals_scraped
               WHERE ticker=? AND source='fundamentus'
               ORDER BY scraped_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if fr:
            fund_eps, fund_roe = fr[0], fr[1]
            fund_delta_yf_eps = _rel_delta(eps_yf, fund_eps)
            fund_delta_yf_roe = _rel_delta(roe_yf, fund_roe)
            fund_delta_cvm_eps = _rel_delta(eps_cvm, fund_eps)
            fund_delta_cvm_roe = _rel_delta(roe_cvm, fund_roe)
            # Detect "2 vs 1" pattern: yf and Fundamentus agree, CVM disagrees.
            # Threshold for the outlier (CVM) is 1.5× the OK band — tighter than
            # full "disputed" (60%) because we have INDEPENDENT corroboration
            # from two sources, so we trust them sooner. VALE3 case: yf+Fund
            # both ~R$3.30 EPS, CVM R$6.86 (48% delta) → fires this rule.
            OUTLIER_CVM_THRESHOLD = 1.5 * EPS_OK   # 37.5%
            if (fund_delta_yf_eps is not None and fund_delta_yf_eps <= EPS_OK
                    and fund_delta_cvm_eps is not None
                    and fund_delta_cvm_eps >= OUTLIER_CVM_THRESHOLD):
                outlier_signal = "cvm_outlier_eps"
    except sqlite3.OperationalError:
        pass  # fundamentals_scraped may not exist yet

    # Aggregate: count metrics that triangulated within OK band
    metrics_checked = 0
    metrics_ok = 0
    metrics_dispute = 0
    if roe_delta is not None:
        metrics_checked += 1
        if roe_delta <= ROE_OK:
            metrics_ok += 1
        elif roe_delta >= ROE_DISPUTED:
            metrics_dispute += 1
    if eps_delta is not None:
        metrics_checked += 1
        if eps_delta <= EPS_OK:
            metrics_ok += 1
        elif eps_delta >= EPS_DISPUTED:
            metrics_dispute += 1

    if metrics_checked == 0:
        label, score = "single_source", 0.5
    elif metrics_dispute > 0:
        # Even one disputed metric flips us to disputed
        label, score = "disputed", round(metrics_ok / metrics_checked, 2)
    elif metrics_ok == metrics_checked:
        label, score = "cross_validated", 1.0
    else:
        # In tolerance "warn" zone — neither agree nor outright dispute
        label, score = "single_source", round(metrics_ok / metrics_checked, 2)

    detail = {
        "yf_period_end": yf["period_end"],
        "cvm_latest_period": cvm["latest_period"],
        "cvm_n_quarters": cvm["n_quarters"],
        "roe_yf": roe_yf, "roe_cvm": round(roe_cvm, 4) if roe_cvm else None,
        "roe_delta": round(roe_delta, 3) if roe_delta is not None else None,
        "eps_yf": eps_yf, "eps_cvm": round(eps_cvm, 4) if eps_cvm else None,
        "eps_delta": round(eps_delta, 3) if eps_delta is not None else None,
        "metrics_ok": metrics_ok, "metrics_checked": metrics_checked,
        "metrics_dispute": metrics_dispute,
    }
    if fund_eps is not None or fund_roe is not None:
        detail["fundamentus_eps"] = fund_eps
        detail["fundamentus_roe"] = fund_roe
        if fund_delta_yf_eps is not None:
            detail["yf_vs_fundamentus_eps_delta"] = round(fund_delta_yf_eps, 3)
        if fund_delta_cvm_eps is not None:
            detail["cvm_vs_fundamentus_eps_delta"] = round(fund_delta_cvm_eps, 3)
    if outlier_signal:
        detail["outlier_signal"] = outlier_signal
        # If 2 sources (yf+Fundamentus) agree and CVM is the outlier, downgrade
        # confidence to disputed — the canonical 2-vs-1 case.
        label, score = "disputed", 0.33

    out.update({"label": label, "score": score, "detail": detail})
    return out


def persist(row: dict) -> None:
    market = row["market"]
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO data_confidence
                 (ticker, market, label, score, detail_json, computed_at)
               VALUES (?,?,?,?,?,?)""",
            (row["ticker"], market, row["label"], row.get("score"),
             json.dumps(row.get("detail") or {}, ensure_ascii=False),
             row["computed_at"]),
        )
        c.commit()


def latest_label(market: str, ticker: str) -> dict | None:
    """Lookup most-recent label for ticker. Used by scoring.fair_value."""
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        r = c.execute(
            """SELECT label, score, detail_json, computed_at
               FROM data_confidence WHERE ticker=?
               ORDER BY computed_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
    if not r:
        return None
    try:
        detail = json.loads(r[2]) if r[2] else None
    except json.JSONDecodeError:
        detail = None
    return {"label": r[0], "score": r[1], "detail": detail, "computed_at": r[3]}


def _list_tickers(scope: str) -> list[tuple[str, str]]:
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
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--market", choices=["br", "us"], default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.ticker:
        tk = args.ticker.upper()
        market = args.market
        if not market:
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
        targets = _list_tickers("universe")
    else:
        targets = _list_tickers("holdings")
    if args.market:
        targets = [(t, m) for (t, m) in targets if m == args.market]

    results = []
    for tk, m in targets:
        row = evaluate(tk, m)
        persist(row)
        results.append(row)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    by_label = {"cross_validated": 0, "single_source": 0, "disputed": 0}
    print(f"Evaluated {len(results)} ticker(s):")
    for r in results:
        d = r.get("detail") or {}
        by_label[r["label"]] = by_label.get(r["label"], 0) + 1
        score = r.get("score")
        score_s = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
        extra = ""
        if d.get("roe_delta") is not None or d.get("eps_delta") is not None:
            parts = []
            if d.get("roe_delta") is not None:
                parts.append(f"roeΔ={d['roe_delta']*100:.1f}%")
            if d.get("eps_delta") is not None:
                parts.append(f"epsΔ={d['eps_delta']*100:.1f}%")
            else:
                parts.append("eps:no_shares")
            extra = " ".join(parts)
        elif d.get("reason"):
            extra = d["reason"]
        print(f"  {r['ticker']:<8} {r['market'].upper()} {r['label']:<16} score={score_s}  {extra}")
    print()
    print("Summary:", " ".join(f"{k}={v}" for k, v in by_label.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
