"""derive_fundamentals_from_filings — compute TTM fundamentals direct from
CVM/SEC filings, **not** from yfinance.

KNOWN CALIBRATION ISSUES (2026-05-08, will be fixed in Sprint 1.x):
  - BR banks NI_TTM ~30% high vs IR-reported numbers (BBDC4 R$21.6B
    derived vs ~R$15-17B reported). Root cause: bank_quarterly_history
    captures total NI (controladora + minoritários); should split into
    NI_total / NI_atribuivel_controladora and use the latter for EPS_TTM.
    Sub-task: extend library/ri/cvm_parser_bank.py to capture both lines.
  - BR dual-class shares (ON+PN): yfinance.shares_outstanding for ticker
    BBDC4 may be PN-only or total — needs verification per-ticker. CVM
    cad_cia_aberta has shares-by-class but not consolidated.
  - All FII fundamentals path not yet wired (FIIs use VPA from
    fii_fundamentals which IS already filings-derived — separate route).


Philosophy (Phase LL): filings = primary source of truth. yfinance is the
cross-check, not the seed. yfinance has documented bugs in BR coverage:
  - BBDC4 ROE 13.75% (yf) vs 5.16% (CVM-derived) — ~62% delta
  - Many holding companies (ITSA4, etc) have minority-interest treatment
    that yf simplifies away

This module reads:
  BR non-bank: quarterly_single (CVM ITR/DFP, single-quarter resolved)
  BR bank:     bank_quarterly_history (CVM bank parser, ds_conta-based)
  US:          (TODO Sprint 1.3) sec_xbrl_fetcher → fundamentals_from_filings_us

Derives TTM:
  EPS_TTM   = sum(net_income last 4Q) × 1000 / shares_outstanding
  BVPS      = latest equity × 1000 / shares_outstanding
  ROE_TTM   = sum(net_income 4Q) / avg(equity 4Q)
  Net Debt  = latest debt_total − latest cash (cash via FCO/FCI proxy)
  D/E       = latest debt_total / latest equity
  Current   = latest current_assets / latest current_liab (non-bank only)
  FCF_TTM   = sum(fcf_proxy last 4Q)

Banks-only:
  CET1, NPL, cost_to_income — already native columns

P/E and P/B require price → joined at fair_value compute time, not here.

Schema: `fundamentals_from_filings` table parallel to `fundamentals`.
PK (ticker, period_end, source) — append-only over time.

CLI:
    python scripts/derive_fundamentals_from_filings.py BBDC4
    python scripts/derive_fundamentals_from_filings.py --holdings   (default)
    python scripts/derive_fundamentals_from_filings.py --all
    python scripts/derive_fundamentals_from_filings.py --backfill   (all periods)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# BR dual-class share pairs. yfinance.shares_outstanding for ticker BBDC4
# reports PN-only (~5.28B); but net_income from filings covers ON+PN
# combined. Dividing total NI by PN-only doubles the EPS. For these tickers,
# we look up the partner class and sum.
# Format: ticker -> partner_ticker (must exist in companies). Bidirectional.
BR_DUAL_CLASS = {
    "BBDC4": "BBDC3", "BBDC3": "BBDC4",
    "ITUB4": "ITUB3", "ITUB3": "ITUB4",
    "ITSA4": "ITSA3", "ITSA3": "ITSA4",
    "PETR4": "PETR3", "PETR3": "PETR4",
    "BBAS4": "BBAS3", "BBAS3": "BBAS4",  # Banco do Brasil rare PN
    "BRAP4": "BRAP3", "BRAP3": "BRAP4",  # Bradespar
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS fundamentals_from_filings (
    ticker              TEXT NOT NULL,
    period_end          TEXT NOT NULL,
    source              TEXT NOT NULL,
    eps_ttm             REAL,
    bvps                REAL,
    roe_ttm             REAL,
    net_income_ttm      REAL,
    revenue_ttm         REAL,
    ebit_ttm            REAL,
    fcf_ttm             REAL,
    equity              REAL,
    total_assets        REAL,
    debt_total          REAL,
    net_debt            REAL,
    debt_to_equity      REAL,
    current_ratio       REAL,
    nd_ebitda           REAL,
    -- bank-specific
    cet1_ratio          REAL,
    npl_ratio           REAL,
    cost_to_income      REAL,
    nii_ttm             REAL,
    -- provenance
    shares_outstanding  REAL,
    n_quarters          INTEGER,
    inputs_json         TEXT,
    computed_at         TEXT NOT NULL,
    PRIMARY KEY (ticker, period_end, source)
);
CREATE INDEX IF NOT EXISTS idx_fff_ticker ON fundamentals_from_filings(ticker);
CREATE INDEX IF NOT EXISTS idx_fff_period ON fundamentals_from_filings(period_end);
"""


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _shares_from_yf(c: sqlite3.Connection, ticker: str) -> float | None:
    r = c.execute(
        """SELECT shares_outstanding FROM fundamentals
           WHERE ticker=? AND shares_outstanding IS NOT NULL
           ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    return r[0] if r and r[0] else None


# In-memory cache for partner-ticker share counts (cleared per process)
_PARTNER_SHARES_CACHE: dict[str, float | None] = {}


def _fetch_partner_shares_live(partner_ticker: str) -> float | None:
    """Fetch shares_outstanding for a partner ticker not in our DB. Used for
    BBDC3/ITUB3/ITSA3 etc. that we don't track but need for total share count.
    """
    if partner_ticker in _PARTNER_SHARES_CACHE:
        return _PARTNER_SHARES_CACHE[partner_ticker]
    try:
        import yfinance as yf
        t = yf.Ticker(f"{partner_ticker}.SA")
        info = t.info
        shares = info.get("sharesOutstanding") or info.get("impliedSharesOutstanding")
        _PARTNER_SHARES_CACHE[partner_ticker] = shares
        return shares
    except Exception:
        _PARTNER_SHARES_CACHE[partner_ticker] = None
        return None


def _total_shares_dual_class(c: sqlite3.Connection, ticker: str) -> tuple[float | None, str]:
    """For dual-class BR tickers, sum ON + PN share counts so per-share
    metrics match the consolidated filings NI denominator.

    Lookup chain for partner shares:
      1. fundamentals table (if we track partner ticker)
      2. yfinance live (cached)

    Returns (total_shares, basis) where basis explains the path taken.
    """
    own = _shares_from_yf(c, ticker)
    partner = BR_DUAL_CLASS.get(ticker)
    if partner is None:
        return own, "single_class"
    # 1. DB lookup
    partner_shares = _shares_from_yf(c, partner)
    basis = "dual_sum_db"
    # 2. Live fallback for partners not tracked
    if partner_shares is None:
        partner_shares = _fetch_partner_shares_live(partner)
        basis = "dual_sum_live"
    if own and partner_shares:
        return own + partner_shares, basis
    return own, "pn_only_partner_unavailable"


def _is_bank(c: sqlite3.Connection, ticker: str) -> bool:
    r = c.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
    if not r or not r[0]:
        return False
    return any(tok in r[0].lower() for tok in ("bank", "banks", "banco", "bancos"))


def _ttm_window(rows: list[tuple], col_idx: int) -> tuple[float | None, int]:
    """Sum last 4 quarters for a column. Returns (sum, n_quarters_with_data).

    Assumes rows[col_idx] is already SINGLE-QUARTER values. Use
    _resolve_ytd_to_single first when the source is YTD-cumulative
    (bank_quarterly_history flow items are YTD; quarterly_single is
    already resolved).
    """
    vals = [r[col_idx] for r in rows[:4] if r[col_idx] is not None]
    if not vals:
        return None, 0
    return sum(vals), len(vals)


def _avg_window(rows: list[tuple], col_idx: int) -> float | None:
    """Average last 4 quarters for a column. Use for stock variables (equity)
    where YTD does not apply."""
    vals = [r[col_idx] for r in rows[:4] if r[col_idx] is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def _prior_period_same_year(period_end: str) -> str | None:
    """Return the prior fiscal-quarter period_end within the same calendar
    year. Q2 (Jun30) -> Q1 (Mar31), Q3 (Sep30) -> Q2 (Jun30), Q4 (Dec31) ->
    Q3 (Sep30). Q1 -> None (no prior in same year)."""
    try:
        year = period_end[:4]
        month_day = period_end[5:10]
    except (TypeError, IndexError):
        return None
    return {
        "06-30": f"{year}-03-31",
        "09-30": f"{year}-06-30",
        "12-31": f"{year}-09-30",
    }.get(month_day)


def _resolve_ytd_to_single(rows: list[tuple], flow_cols: tuple[int, ...]) -> list[tuple]:
    """Convert YTD-cumulative flow columns to single-quarter values.

    `rows` is period_end DESC ordered list of tuples. `flow_cols` are the
    column indices that need YTD resolution (e.g. net_income, NII for banks).
    Stock-variable columns (equity, total_assets) are left untouched.

    Q1 (Mar-31) stays as-is (YTD == single).
    Q2/Q3/Q4: subtract prior fiscal-quarter YTD within the same year.
    Returns rows with same shape but flow columns resolved.

    If prior period is missing from `rows`, that column for that row is set
    to None — caller deals with sparse coverage.
    """
    by_period: dict[str, tuple] = {r[0]: r for r in rows}
    out: list[tuple] = []
    for r in rows:
        period_end = r[0]
        if period_end[5:10] == "03-31":
            # Q1: YTD == single, no resolution needed
            out.append(r)
            continue
        prior_pe = _prior_period_same_year(period_end)
        prior = by_period.get(prior_pe) if prior_pe else None
        if prior is None:
            # Can't resolve → null out flow columns
            new_r = list(r)
            for ci in flow_cols:
                new_r[ci] = None
            out.append(tuple(new_r))
            continue
        new_r = list(r)
        for ci in flow_cols:
            cur, pri = r[ci], prior[ci]
            new_r[ci] = (cur - pri) if (cur is not None and pri is not None) else None
        out.append(tuple(new_r))
    return out


def derive_br_nonbank(c: sqlite3.Connection, ticker: str,
                      *, period_end: str | None = None) -> dict | None:
    """Derive TTM fundamentals for a BR non-bank ticker from quarterly_single.

    If `period_end` is given, derives TTM ending at that period (uses 4
    quarters ending at and including period_end). Otherwise uses latest 4Q.
    """
    if period_end:
        rows = c.execute(
            """SELECT period_end, net_income, equity, total_assets, total_liab,
                      debt_total, current_assets, current_liab, revenue, ebit,
                      fcf_proxy
               FROM quarterly_single
               WHERE ticker=? AND period_end <= ?
               ORDER BY period_end DESC LIMIT 4""",
            (ticker, period_end),
        ).fetchall()
    else:
        rows = c.execute(
            """SELECT period_end, net_income, equity, total_assets, total_liab,
                      debt_total, current_assets, current_liab, revenue, ebit,
                      fcf_proxy
               FROM quarterly_single WHERE ticker=?
               ORDER BY period_end DESC LIMIT 4""",
            (ticker,),
        ).fetchall()

    if not rows:
        return None
    if len(rows) < 4:
        # Partial coverage — emit but flag low n_quarters
        pass

    latest = rows[0]
    latest_period = latest[0]

    ni_ttm, n_q_ni = _ttm_window(rows, 1)
    revenue_ttm, _ = _ttm_window(rows, 8)
    ebit_ttm, _ = _ttm_window(rows, 9)
    fcf_ttm, _ = _ttm_window(rows, 10)
    avg_equity = _avg_window(rows, 2)

    latest_equity = latest[2]
    latest_assets = latest[3]
    latest_debt = latest[5]
    latest_ca = latest[6]
    latest_cl = latest[7]

    shares, shares_basis = _total_shares_dual_class(c, ticker)
    eps_ttm = (ni_ttm * 1000.0 / shares) if (ni_ttm and shares) else None
    bvps = (latest_equity * 1000.0 / shares) if (latest_equity and shares) else None
    roe_ttm = (ni_ttm / avg_equity) if (ni_ttm and avg_equity) else None

    debt_to_equity = (latest_debt / latest_equity) if (latest_debt and latest_equity) else None
    current_ratio = (latest_ca / latest_cl) if (latest_ca and latest_cl) else None
    nd_ebitda = None
    if ebit_ttm and latest_debt:
        # Crude proxy: net debt / TTM EBIT (safer than EBITDA when no D&A row)
        nd_ebitda = latest_debt / ebit_ttm if ebit_ttm > 0 else None

    return {
        "ticker": ticker, "period_end": latest_period,
        "source": "cvm_quarterly_single",
        "eps_ttm": eps_ttm, "bvps": bvps, "roe_ttm": roe_ttm,
        "net_income_ttm": ni_ttm,
        "revenue_ttm": revenue_ttm,
        "ebit_ttm": ebit_ttm,
        "fcf_ttm": fcf_ttm,
        "equity": latest_equity,
        "total_assets": latest_assets,
        "debt_total": latest_debt,
        "net_debt": latest_debt,  # without cash detail; refine when FCI parser exposes cash bucket
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio,
        "nd_ebitda": nd_ebitda,
        "cet1_ratio": None, "npl_ratio": None, "cost_to_income": None, "nii_ttm": None,
        "shares_outstanding": shares,
        "n_quarters": n_q_ni,
        "inputs": {
            "rows_used": [list(r) for r in rows[:4]],
            "rows_count": len(rows),
        },
        "computed_at": _now_iso(),
    }


def derive_br_bank(c: sqlite3.Connection, ticker: str,
                   *, period_end: str | None = None) -> dict | None:
    """Derive TTM fundamentals for a BR bank from bank_quarterly_history.

    bank_quarterly_history stores P&L items as YTD-cumulative (per CVM
    convention: ITR Q2 reports H1 cumulative, Q3 reports 9M, etc.). We
    must resolve YTD → single quarter before summing 4 to get TTM.
    Pulls 8 rows so we can resolve the latest 4 even if Q4 needs the
    prior Q3 (and Q3 needs prior Q2, etc.).
    """
    flow_cols = (1, 4)  # net_income (attributable preferred), nii — both YTD
    # Prefer net_income_attributable (3.11.01 — controladora, exclui minoritários);
    # fall back to total net_income via COALESCE if attribuível column NULL
    # (older parser runs before Sprint 1.1.x).
    if period_end:
        raw = c.execute(
            """SELECT period_end,
                      COALESCE(net_income_attributable, net_income),
                      equity, total_assets, nii,
                      cet1_ratio, npl_ratio, cost_to_income_ratio, loan_book,
                      pdd_reserve, net_income_attributable, net_income
               FROM bank_quarterly_history
               WHERE ticker=? AND period_end <= ? AND source != 'bacen_ifdata'
               ORDER BY period_end DESC LIMIT 8""",
            (ticker, period_end),
        ).fetchall()
    else:
        raw = c.execute(
            """SELECT period_end,
                      COALESCE(net_income_attributable, net_income),
                      equity, total_assets, nii,
                      cet1_ratio, npl_ratio, cost_to_income_ratio, loan_book,
                      pdd_reserve, net_income_attributable, net_income
               FROM bank_quarterly_history WHERE ticker=?
                 AND source != 'bacen_ifdata'
               ORDER BY period_end DESC LIMIT 8""",
            (ticker,),
        ).fetchall()
    if not raw:
        return None

    rows = _resolve_ytd_to_single(raw, flow_cols)
    latest = rows[0]
    latest_period = latest[0]

    ni_ttm, n_q = _ttm_window(rows, 1)
    nii_ttm, _ = _ttm_window(rows, 4)
    avg_equity = _avg_window(rows, 2)

    latest_equity = latest[2]
    latest_assets = latest[3]
    latest_cet1 = latest[5]
    latest_npl = latest[6]
    latest_c2i = latest[7]

    shares, shares_basis = _total_shares_dual_class(c, ticker)
    eps_ttm = (ni_ttm * 1000.0 / shares) if (ni_ttm and shares) else None
    bvps = (latest_equity * 1000.0 / shares) if (latest_equity and shares) else None
    roe_ttm = (ni_ttm / avg_equity) if (ni_ttm and avg_equity) else None

    return {
        "ticker": ticker, "period_end": latest_period,
        "source": "cvm_bank_quarterly",
        "eps_ttm": eps_ttm, "bvps": bvps, "roe_ttm": roe_ttm,
        "net_income_ttm": ni_ttm,
        "revenue_ttm": nii_ttm,  # NII as proxy for "revenue" in bank context
        "nii_ttm": nii_ttm,
        "ebit_ttm": None,         # not meaningful for banks
        "fcf_ttm": None,
        "equity": latest_equity,
        "total_assets": latest_assets,
        "debt_total": None,        # bank deposits ≠ debt; D/E doesn't apply
        "net_debt": None,
        "debt_to_equity": None,
        "current_ratio": None,
        "nd_ebitda": None,
        "cet1_ratio": latest_cet1,
        "npl_ratio": latest_npl,
        "cost_to_income": latest_c2i,
        "shares_outstanding": shares,
        "n_quarters": n_q,
        "inputs": {
            "rows_used": [list(r) for r in rows[:4]],
            "rows_count": len(rows),
        },
        "computed_at": _now_iso(),
    }


def derive_one(ticker: str, market: str = "br",
               *, period_end: str | None = None) -> dict | None:
    """Top-level: route to bank vs non-bank based on sector. US not yet wired."""
    if market != "br":
        return None  # US comes in Sprint 1.3
    db = DB_BR
    with sqlite3.connect(db) as c:
        if _is_bank(c, ticker):
            return derive_br_bank(c, ticker, period_end=period_end)
        return derive_br_nonbank(c, ticker, period_end=period_end)


def persist(row: dict, market: str = "br") -> None:
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO fundamentals_from_filings
                 (ticker, period_end, source,
                  eps_ttm, bvps, roe_ttm,
                  net_income_ttm, revenue_ttm, ebit_ttm, fcf_ttm,
                  equity, total_assets, debt_total, net_debt,
                  debt_to_equity, current_ratio, nd_ebitda,
                  cet1_ratio, npl_ratio, cost_to_income, nii_ttm,
                  shares_outstanding, n_quarters,
                  inputs_json, computed_at)
               VALUES (?,?,?, ?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?, ?,?,?,?, ?,?, ?,?)""",
            (
                row["ticker"], row["period_end"], row["source"],
                row.get("eps_ttm"), row.get("bvps"), row.get("roe_ttm"),
                row.get("net_income_ttm"), row.get("revenue_ttm"),
                row.get("ebit_ttm"), row.get("fcf_ttm"),
                row.get("equity"), row.get("total_assets"),
                row.get("debt_total"), row.get("net_debt"),
                row.get("debt_to_equity"), row.get("current_ratio"),
                row.get("nd_ebitda"),
                row.get("cet1_ratio"), row.get("npl_ratio"),
                row.get("cost_to_income"), row.get("nii_ttm"),
                row.get("shares_outstanding"), row.get("n_quarters"),
                json.dumps(row.get("inputs") or {}, ensure_ascii=False, default=str),
                row["computed_at"],
            ),
        )
        c.commit()


def derive_all_periods(ticker: str, market: str = "br") -> list[dict]:
    """Backfill: derive TTM for every period_end where we have ≥4 trailing quarters."""
    if market != "br":
        return []
    db = DB_BR
    out: list[dict] = []
    with sqlite3.connect(db) as c:
        is_bank = _is_bank(c, ticker)
        if is_bank:
            periods = c.execute(
                """SELECT DISTINCT period_end FROM bank_quarterly_history
                   WHERE ticker=? ORDER BY period_end DESC""",
                (ticker,),
            ).fetchall()
        else:
            periods = c.execute(
                """SELECT DISTINCT period_end FROM quarterly_single
                   WHERE ticker=? ORDER BY period_end DESC""",
                (ticker,),
            ).fetchall()
    for (p,) in periods:
        r = derive_one(ticker, market, period_end=p)
        if r:
            persist(r, market)
            out.append(r)
    return out


def _list_tickers(scope: str, market: str = "br") -> list[str]:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        if scope == "holdings":
            rows = c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ).fetchall()
        else:
            rows = c.execute("SELECT ticker FROM companies").fetchall()
    return sorted({r[0] for r in rows})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--backfill", action="store_true",
                    help="derive TTM for all historical periods (not just latest)")
    ap.add_argument("--show", action="store_true",
                    help="(with --ticker) print latest derived row + comparison vs yfinance")
    args = ap.parse_args()

    if args.show and args.ticker:
        return _show_compare(args.ticker.upper(), args.market)

    if args.ticker:
        targets = [args.ticker.upper()]
    elif args.all:
        targets = _list_tickers("all", args.market)
    else:
        targets = _list_tickers("holdings", args.market)

    print(f"Deriving fundamentals from filings for {len(targets)} ticker(s) (market={args.market})...")
    ok = skipped = 0
    for tk in targets:
        try:
            if args.backfill:
                rows = derive_all_periods(tk, args.market)
                if rows:
                    ok += len(rows)
                    print(f"  {tk:<8} backfilled {len(rows)} periods (latest {rows[0]['period_end']})")
                else:
                    skipped += 1
            else:
                r = derive_one(tk, args.market)
                if r is None:
                    skipped += 1
                    continue
                persist(r, args.market)
                ok += 1
                eps = f"{r.get('eps_ttm'):.4f}" if r.get('eps_ttm') is not None else "—"
                roe = f"{r.get('roe_ttm')*100:.1f}%" if r.get('roe_ttm') is not None else "—"
                src = r['source'].split('_')[1].upper()
                print(f"  {tk:<8} {r['period_end']} {src:<8} EPS_ttm={eps:<10} "
                      f"ROE_ttm={roe:<7} n_q={r.get('n_quarters', '?')}")
        except Exception as e:  # noqa: BLE001
            skipped += 1
            print(f"  {tk:<8} ERROR — {e}")
    print(f"\nPersisted {ok} | skipped {skipped}")
    return 0


def _show_compare(ticker: str, market: str) -> int:
    """Print latest filing-derived row side-by-side with yfinance equivalent."""
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        fr = c.execute(
            """SELECT period_end, source, eps_ttm, bvps, roe_ttm, n_quarters, computed_at
               FROM fundamentals_from_filings WHERE ticker=?
               ORDER BY computed_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        yf = c.execute(
            """SELECT period_end, eps, bvps, roe FROM fundamentals
               WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()

    print(f"\n=== {ticker} ({market.upper()}) — filings-derived vs yfinance ===")
    if fr:
        print(f"  FILINGS  ({fr[1]:<22}) period={fr[0]} computed={fr[6]}")
        print(f"           EPS_TTM={fr[2]}  BVPS={fr[3]}  ROE_TTM={fr[4]}  n_q={fr[5]}")
    else:
        print("  FILINGS  no row yet — run derive first")
    if yf:
        print(f"  YFINANCE              period={yf[0]}")
        print(f"           EPS    ={yf[1]}  BVPS={yf[2]}  ROE    ={yf[3]}")
    else:
        print("  YFINANCE no row")
    if fr and yf and fr[2] is not None and yf[1] is not None:
        delta = (fr[2] - yf[1]) / max(abs(fr[2]), abs(yf[1])) * 100
        print(f"\n  EPS delta (filings vs yf): {delta:+.1f}%")
    if fr and yf and fr[4] is not None and yf[3] is not None:
        delta = (fr[4] - yf[3]) / max(abs(fr[4]), abs(yf[3])) * 100
        print(f"  ROE delta (filings vs yf): {delta:+.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
