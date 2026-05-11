"""sec_xbrl_fetcher — pull US fundamentals from SEC EDGAR XBRL companyfacts API.

Phase LL Sprint 1.3. Brings US to BR parity: filings as primary source of
truth, yfinance becomes the cross-check.

API: https://data.sec.gov/api/xbrl/companyfacts/CIK{10d}.json
  - Free, official, no rate limits in practice (SEC fair-use UA required)
  - Returns ALL XBRL facts ever filed for that issuer (10-K, 10-Q, 8-K, etc.)
  - 10+ years of history available for most large issuers

We harvest US-GAAP concepts and compute TTM (last 4 quarters):
  NetIncomeLoss            → net_income_ttm
  StockholdersEquity       → equity (latest instant)
  Assets                   → total_assets (latest instant)
  Revenues / RevenuesNetOf… → revenue_ttm
  OperatingIncomeLoss      → ebit_ttm
  LongTermDebt + ShortTermBorrowings → debt_total
  EarningsPerShareDiluted  → eps_diluted (sanity-check vs computed)
  WeightedAvg…SharesDiluted → shares_diluted

Edge cases:
  - Foreign private issuers (TSM, NU, XP) file 20-F annually instead of 10-K.
    Some have XBRL coverage; if 'us-gaap' empty we try 'ifrs-full'.
  - REITs (O, PLD) report FFO outside us-gaap as concept; we still capture
    NetIncomeLoss + equity for fair_value compute.
  - Banks (JPM, GS) report InterestIncome / InterestExpense separately;
    NetIncomeLoss still works for our use.
  - ETFs and complex holdings (BN, BRK-B, PLTR with class shares) flagged
    in `inputs.notes` so dossier can warn.

CLI:
    python -m fetchers.sec_xbrl_fetcher JNJ
    python -m fetchers.sec_xbrl_fetcher --holdings   (default)
    python -m fetchers.sec_xbrl_fetcher --all
    python -m fetchers.sec_xbrl_fetcher JNJ --show
    python -m fetchers.sec_xbrl_fetcher --backfill   (all historical periods)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_US = ROOT / "data" / "us_investments.db"
CACHE_DIR = ROOT / "data" / "sec_cache"
COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
USER_AGENT = "investment-intelligence apaidusis@gmail.com"

# US-GAAP concept → our column. Order matters: first match wins per concept.
# Some companies use newer ASU concepts; fallback chain handles legacy/IFRS.
CONCEPT_FALLBACKS = {
    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",  # IFRS / some foreign filers
        "NetIncomeLossAvailableToCommonStockholdersBasic",
    ],
    "equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        "Equity",  # IFRS
    ],
    "total_assets": ["Assets"],
    "total_liab": ["Liabilities"],
    "revenue": [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "Revenue",  # IFRS
        "SalesRevenueNet",
    ],
    "ebit": [
        "OperatingIncomeLoss",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
    ],
    "debt_lt": ["LongTermDebt", "LongTermDebtNoncurrent"],
    "debt_st": ["ShortTermBorrowings", "DebtCurrent"],
    "fco": ["NetCashProvidedByUsedInOperatingActivities"],
    "eps_diluted": ["EarningsPerShareDiluted", "IncomeLossFromContinuingOperationsPerDilutedShare"],
    "eps_basic": ["EarningsPerShareBasic"],
    "shares_diluted": [
        "WeightedAverageNumberOfDilutedSharesOutstanding",
        "WeightedAverageNumberOfSharesOutstandingDiluted",
    ],
}

SCHEMA_FFF_AUGMENT = """
-- Idempotent: only adds columns if missing. Schema base lives in
-- scripts/derive_fundamentals_from_filings.py
"""


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=5, backoff_factor=2,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET",))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov",
    })
    return s


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _ensure_schema() -> None:
    """Reuse existing fundamentals_from_filings schema (created by
    scripts/derive_fundamentals_from_filings.py). Idempotent CREATE if
    that hasn't run yet on US DB."""
    schema = """
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
        cet1_ratio          REAL,
        npl_ratio           REAL,
        cost_to_income      REAL,
        nii_ttm             REAL,
        shares_outstanding  REAL,
        n_quarters          INTEGER,
        inputs_json         TEXT,
        computed_at         TEXT NOT NULL,
        PRIMARY KEY (ticker, period_end, source)
    );
    CREATE INDEX IF NOT EXISTS idx_fff_ticker ON fundamentals_from_filings(ticker);
    """
    with sqlite3.connect(DB_US) as c:
        c.executescript(schema)


def _ticker_map_from_sec(sess: requests.Session) -> dict[str, str]:
    """Reuse SEC ticker→CIK lookup. 7-day cached locally."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / "company_tickers.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 7 * 86400:
        data = json.loads(cache.read_text(encoding="utf-8"))
    else:
        sess.headers["Host"] = "www.sec.gov"
        r = sess.get("https://www.sec.gov/files/company_tickers.json", timeout=30)
        r.raise_for_status()
        data = r.json()
        cache.write_text(json.dumps(data), encoding="utf-8")
    return {str(e["ticker"]).upper(): str(e["cik_str"]).zfill(10)
            for e in data.values()}


def fetch_companyfacts(sess: requests.Session, cik10: str) -> dict | None:
    """Pull full XBRL companyfacts JSON. Cached 1 day per ticker."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"facts_{cik10}.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 86400:
        return json.loads(cache.read_text(encoding="utf-8"))
    sess.headers["Host"] = "data.sec.gov"
    url = COMPANYFACTS_URL.format(cik10=cik10)
    try:
        r = sess.get(url, timeout=30)
        if r.status_code == 404:
            return None  # foreign issuer w/o XBRL coverage
        r.raise_for_status()
        data = r.json()
        cache.write_text(json.dumps(data), encoding="utf-8")
        return data
    except (requests.RequestException, ValueError):
        return None


def _extract_facts(facts: dict, concept_keys: list[str]) -> list[dict]:
    """Return list of fact dicts {end, start, val, fy, fp, form, frame, accn}
    for the first concept that has data. Tries us-gaap first, then ifrs-full.

    Always returns a flat list ordered by end date (latest first).
    """
    for taxonomy in ("us-gaap", "ifrs-full"):
        tax = facts.get(taxonomy, {})
        for concept in concept_keys:
            entry = tax.get(concept)
            if not entry:
                continue
            units = entry.get("units", {})
            # Prefer USD; fall back to first unit found
            unit_key = "USD" if "USD" in units else (next(iter(units), None))
            if not unit_key:
                continue
            arr = units[unit_key]
            # Flatten + sort
            for item in arr:
                item["_taxonomy"] = taxonomy
                item["_concept"] = concept
                item["_unit"] = unit_key
            arr.sort(key=lambda x: x.get("end", ""), reverse=True)
            if arr:
                return arr
    return []


def _is_quarterly(fact: dict) -> bool:
    """Detect 3-month duration. SEC XBRL facts have `start` + `end` for
    duration items (P&L) and only `end` for instant items (BS).
    Quarterly P&L: end - start ≈ 90 days.
    """
    s, e = fact.get("start"), fact.get("end")
    if not s or not e:
        return False
    try:
        sd = date.fromisoformat(s)
        ed = date.fromisoformat(e)
    except ValueError:
        return False
    days = (ed - sd).days
    return 80 <= days <= 100


def _is_annual(fact: dict) -> bool:
    """360-380 day duration ≈ annual."""
    s, e = fact.get("start"), fact.get("end")
    if not s or not e:
        return False
    try:
        sd = date.fromisoformat(s)
        ed = date.fromisoformat(e)
    except ValueError:
        return False
    days = (ed - sd).days
    return 350 <= days <= 380


def _instant_latest(facts_list: list[dict]) -> dict | None:
    """Return latest instant fact (no `start` key, only `end`).
    BS items: equity, total_assets, debt.
    """
    for f in facts_list:  # already sorted desc by end
        if not f.get("start") and f.get("end"):
            return f
        # Some filings include both start and end with same date for instants
        if f.get("start") == f.get("end"):
            return f
    return None


def _ttm_quarterly(facts_list: list[dict], *, as_of: str | None = None) -> tuple[float | None, list[dict]]:
    """Sum 4 contiguous QUARTERLY (3-month) facts ending ≤ as_of.

    The contiguity check matters: US issuers don't file Q4 standalone (it's
    implicit in 10-K FY minus 9M YTD). A naive 'latest 4 distinct ends' picks
    Q1 2026 + Q3 2025 + Q2 2025 + Q1 2025 — wrong, skips Q4 2025, double-
    weights Q1.

    Strategy:
      1. Filter to 3-month duration, dedupe by end (latest accession wins).
      2. Walk DESC. Keep a fact only if its `start` is within 100d after the
         previous fact's `start` minus a quarter (i.e. truly contiguous).
      3. Once 4 contiguous picked, return sum. Otherwise return None — caller
         falls back to annual (preferred) or restitch via FY - 9M.
    """
    qs = [f for f in facts_list if _is_quarterly(f)]
    if as_of:
        qs = [f for f in qs if f.get("end", "") <= as_of]
    if len(qs) < 4:
        return None, []
    seen_ends: set[str] = set()
    deduped: list[dict] = []
    for f in sorted(qs, key=lambda x: x.get("end", ""), reverse=True):
        e = f.get("end", "")
        if e in seen_ends:
            continue
        seen_ends.add(e)
        deduped.append(f)

    # Walk for contiguity: each fact's `end` must be ≈90d before the previous
    # fact's `start` (or equivalently, current `start` ≈ previous `start`-3mo)
    contiguous: list[dict] = [deduped[0]]
    for i in range(1, len(deduped)):
        prev_start = date.fromisoformat(contiguous[-1]["start"])
        curr_end = date.fromisoformat(deduped[i]["end"])
        gap = (prev_start - curr_end).days
        # Allowed gap: -3 (overlap, restated) to +5 days (filing rounding)
        if -5 <= gap <= 5:
            contiguous.append(deduped[i])
            if len(contiguous) == 4:
                break

    if len(contiguous) < 4:
        return None, contiguous  # caller falls back

    total = sum(f.get("val", 0) for f in contiguous if f.get("val") is not None)
    return total, contiguous


def _restitch_ttm_from_fy_minus_ytd(facts_list: list[dict], *, as_of: str | None = None) -> tuple[float | None, list[dict]]:
    """When 4 contiguous quarters aren't available (Q4 standalone missing —
    typical for US issuers), restitch TTM via:

        TTM_ending_QN = QN_current_year + (FY_prior_year - YTD_prior_year_at_QN_position)

    Where QN_current is the standalone quarter (3-month duration) and YTD
    prior is the cumulative same-position figure from prior year (e.g. for
    TTM ending Q1 2026: TTM = Q1_2026 + FY_2025 - Q1_2025).

    Returns (sum, [facts_used]) or (None, []) if can't restitch.
    """
    if not facts_list:
        return None, []

    # Find latest standalone quarter ending ≤ as_of
    quarters = [f for f in facts_list if _is_quarterly(f)]
    if as_of:
        quarters = [f for f in quarters if f.get("end", "") <= as_of]
    if not quarters:
        return None, []
    latest_q = sorted(quarters, key=lambda x: x.get("end", ""), reverse=True)[0]

    # Find latest FY annual ≤ as_of and ≤ latest_q.end
    annuals = [f for f in facts_list if _is_annual(f)]
    if as_of:
        annuals = [f for f in annuals if f.get("end", "") <= as_of]
    annuals = [a for a in annuals if a.get("end", "") < latest_q.get("end", "9999")]
    if not annuals:
        return None, []
    fy_prior = sorted(annuals, key=lambda x: x.get("end", ""), reverse=True)[0]

    # Find prior-year quarter at same fiscal position (start month aligned)
    latest_q_start = latest_q.get("start", "")
    if len(latest_q_start) < 7:
        return None, []
    target_month = latest_q_start[5:7]
    target_day = latest_q_start[8:10] or "01"
    prior_year = str(int(latest_q_start[:4]) - 1)
    target_start = f"{prior_year}-{target_month}-{target_day}"

    prior_q = next(
        (q for q in quarters
         if q.get("start", "")[:7] == target_start[:7]),
        None,
    )
    if prior_q is None:
        return None, []

    val = (latest_q.get("val", 0) + fy_prior.get("val", 0) - prior_q.get("val", 0))
    return val, [latest_q, fy_prior, prior_q]


def _annual_latest(facts_list: list[dict], *, as_of: str | None = None) -> dict | None:
    """Latest 12-month duration fact (10-K annual figure)."""
    annuals = [f for f in facts_list if _is_annual(f)]
    if as_of:
        annuals = [f for f in annuals if f.get("end", "") <= as_of]
    return annuals[0] if annuals else None


def derive_us_from_xbrl(ticker: str, facts: dict, *, as_of: str | None = None) -> dict | None:
    """Build fundamentals_from_filings row from SEC companyfacts JSON.

    `as_of` allows backfill: derive TTM ending at this date instead of latest.
    """
    if "facts" not in facts:
        return None
    f = facts["facts"]

    # P&L: TTM via 4 contiguous quarters; fallback restitch FY-9M when
    # Q4 standalone missing (always for US issuers).
    def _ttm_with_fallback(facts_list):
        v, used = _ttm_quarterly(facts_list, as_of=as_of)
        if v is not None:
            return v, used, "4q_contiguous"
        v, used = _restitch_ttm_from_fy_minus_ytd(facts_list, as_of=as_of)
        if v is not None:
            return v, used, "restitch_fy_minus_ytd"
        # Final fallback: latest annual figure (FY EPS as proxy for TTM)
        annual = _annual_latest(facts_list, as_of=as_of)
        if annual is not None:
            return annual.get("val"), [annual], "annual_fy"
        return None, [], "no_data"

    ni_facts = _extract_facts(f, CONCEPT_FALLBACKS["net_income"])
    ni_ttm, ni_used, ni_method = _ttm_with_fallback(ni_facts)

    rev_facts = _extract_facts(f, CONCEPT_FALLBACKS["revenue"])
    rev_ttm, _, rev_method = _ttm_with_fallback(rev_facts)

    ebit_facts = _extract_facts(f, CONCEPT_FALLBACKS["ebit"])
    ebit_ttm, _, _ = _ttm_with_fallback(ebit_facts)

    fco_facts = _extract_facts(f, CONCEPT_FALLBACKS["fco"])
    fco_ttm, _, _ = _ttm_with_fallback(fco_facts)

    # BS: instant items (latest)
    eq_facts = _extract_facts(f, CONCEPT_FALLBACKS["equity"])
    eq_latest = _instant_latest(eq_facts)
    if as_of and eq_latest and eq_latest.get("end", "") > as_of:
        eq_latest = next((x for x in eq_facts if not x.get("start") and x.get("end", "") <= as_of), None)
    equity = eq_latest.get("val") if eq_latest else None

    ta_facts = _extract_facts(f, CONCEPT_FALLBACKS["total_assets"])
    ta_latest = _instant_latest(ta_facts)
    if as_of and ta_latest and ta_latest.get("end", "") > as_of:
        ta_latest = next((x for x in ta_facts if not x.get("start") and x.get("end", "") <= as_of), None)
    total_assets = ta_latest.get("val") if ta_latest else None

    debt_lt_facts = _extract_facts(f, CONCEPT_FALLBACKS["debt_lt"])
    debt_st_facts = _extract_facts(f, CONCEPT_FALLBACKS["debt_st"])
    debt_lt = (_instant_latest(debt_lt_facts) or {}).get("val")
    debt_st = (_instant_latest(debt_st_facts) or {}).get("val")
    debt_total = None
    if debt_lt is not None or debt_st is not None:
        debt_total = (debt_lt or 0) + (debt_st or 0)

    # Average equity for ROE: average over the 4 quarter-end equity values
    # (XBRL gives equity at each period_end; pick those matching the 4 quarters)
    avg_equity = equity  # fallback: use latest
    if ni_used and eq_facts:
        per_q_equity = []
        for q in ni_used:
            qe = q.get("end")
            match = next((x for x in eq_facts if x.get("end") == qe and not x.get("start")), None)
            if match and match.get("val"):
                per_q_equity.append(match["val"])
        if per_q_equity:
            avg_equity = sum(per_q_equity) / len(per_q_equity)

    # Shares: prefer weighted avg diluted from latest 10-K (annual is more stable
    # than quarterly because 10-Q reports quarterly avg only). Fallback to 10-Q.
    shares_facts = _extract_facts(f, CONCEPT_FALLBACKS["shares_diluted"])
    shares_annual = _annual_latest(shares_facts, as_of=as_of)
    shares = (shares_annual.get("val") if shares_annual else None)
    if shares is None and shares_facts:
        # Latest quarterly shares value
        qs = [x for x in shares_facts if _is_quarterly(x)]
        if as_of:
            qs = [x for x in qs if x.get("end", "") <= as_of]
        if qs:
            shares = qs[0].get("val")

    # Per-share metrics
    eps_ttm = (ni_ttm / shares) if (ni_ttm is not None and shares) else None
    bvps = (equity / shares) if (equity is not None and shares) else None
    roe_ttm = (ni_ttm / avg_equity) if (ni_ttm is not None and avg_equity) else None

    # Cross-check: company-reported diluted EPS (sum 4 quarters)
    eps_facts = _extract_facts(f, CONCEPT_FALLBACKS["eps_diluted"])
    eps_reported_ttm, _ = _ttm_quarterly(eps_facts, as_of=as_of)

    # Period_end: latest quarter end we used
    period_end = (ni_used[0].get("end") if ni_used else
                  (eq_latest.get("end") if eq_latest else None))

    if period_end is None:
        return None

    # Debt-to-equity, ND/EBITDA proxies
    dte = (debt_total / equity) if (debt_total and equity) else None
    nd_ebitda = None
    if debt_total and ebit_ttm and ebit_ttm > 0:
        nd_ebitda = debt_total / ebit_ttm

    notes = []
    if abs((eps_ttm or 0) - (eps_reported_ttm or 0)) > 0.05 * max(abs(eps_ttm or 0), 1):
        notes.append(
            f"computed_eps_ttm={eps_ttm:.4f} vs reported_diluted_sum={eps_reported_ttm:.4f}"
            if eps_ttm and eps_reported_ttm else None
        )
    if shares is None:
        notes.append("shares_outstanding_unavailable_from_xbrl")

    return {
        "ticker": ticker, "period_end": period_end,
        "source": "sec_xbrl",
        "eps_ttm": eps_ttm, "bvps": bvps, "roe_ttm": roe_ttm,
        "net_income_ttm": ni_ttm,
        "revenue_ttm": rev_ttm,
        "ebit_ttm": ebit_ttm,
        "fcf_ttm": fco_ttm,  # FCO as proxy; capex needed for true FCF
        "equity": equity,
        "total_assets": total_assets,
        "debt_total": debt_total,
        "net_debt": debt_total,  # without cash detail
        "debt_to_equity": dte,
        "current_ratio": None,  # need current_assets/current_liab — separate call
        "nd_ebitda": nd_ebitda,
        "cet1_ratio": None, "npl_ratio": None, "cost_to_income": None, "nii_ttm": None,
        "shares_outstanding": shares,
        "n_quarters": len(ni_used) if ni_used else 0,
        "inputs": {
            "ni_periods_used": [q.get("end") for q in ni_used] if ni_used else [],
            "ni_method": ni_method,         # 4q_contiguous | restitch_fy_minus_ytd | annual_fy
            "rev_method": rev_method,
            "ni_concept": ni_facts[0].get("_concept") if ni_facts else None,
            "ni_taxonomy": ni_facts[0].get("_taxonomy") if ni_facts else None,
            "equity_period": eq_latest.get("end") if eq_latest else None,
            "shares_source": "10-K_annual_avg" if shares_annual else "10-Q_quarterly",
            "eps_reported_ttm": eps_reported_ttm,
            "eps_computed_ttm": eps_ttm,
            "notes": [n for n in notes if n],
        },
        "computed_at": _now_iso(),
    }


def persist(row: dict) -> None:
    _ensure_schema()
    with sqlite3.connect(DB_US) as c:
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


def fetch_one(sess: requests.Session, cik_map: dict[str, str], ticker: str,
              *, as_of: str | None = None) -> dict | None:
    """Top-level: ticker → CIK → companyfacts → derived row."""
    tk = ticker.upper()
    cik10 = cik_map.get(tk)
    if not cik10:
        return {"ticker": tk, "_error": f"no_cik_for_ticker"}
    facts = fetch_companyfacts(sess, cik10)
    if not facts:
        return {"ticker": tk, "_error": "no_companyfacts_404_or_error"}
    derived = derive_us_from_xbrl(tk, facts, as_of=as_of)
    if not derived:
        return {"ticker": tk, "_error": "no_derivable_facts_in_xbrl"}
    return derived


def _list_us_tickers(scope: str) -> list[str]:
    with sqlite3.connect(DB_US) as c:
        if scope == "holdings":
            rows = c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ).fetchall()
        else:
            rows = c.execute("SELECT ticker FROM companies").fetchall()
    return sorted({r[0] for r in rows})


def show_compare(ticker: str) -> int:
    """Side-by-side filings vs yfinance for a single US ticker."""
    _ensure_schema()
    with sqlite3.connect(DB_US) as c:
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
    print(f"\n=== {ticker} (US) — SEC XBRL filings vs yfinance ===")
    if fr:
        print(f"  FILINGS  ({fr[1]:<10}) period={fr[0]} computed={fr[6]}")
        print(f"           EPS_TTM={fr[2]}  BVPS={fr[3]}  ROE_TTM={fr[4]}  n_q={fr[5]}")
    else:
        print("  FILINGS  no row yet")
    if yf:
        print(f"  YFINANCE              period={yf[0]}")
        print(f"           EPS    ={yf[1]}  BVPS={yf[2]}  ROE    ={yf[3]}")
    if fr and yf and fr[2] is not None and yf[1] is not None:
        delta = (fr[2] - yf[1]) / max(abs(fr[2]), abs(yf[1])) * 100
        print(f"\n  EPS delta: {delta:+.1f}%")
    if fr and yf and fr[4] is not None and yf[3] is not None:
        delta = (fr[4] - yf[3]) / max(abs(fr[4]), abs(yf[3])) * 100
        print(f"  ROE delta: {delta:+.1f}%")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--show", action="store_true",
                    help="(with ticker) print derived vs yfinance comparison")
    ap.add_argument("--backfill", action="store_true",
                    help="derive TTM for every fiscal-quarter end available "
                         "(builds 5-10y trajectory for fair_value history)")
    args = ap.parse_args()

    if args.show and args.ticker:
        return show_compare(args.ticker.upper())

    if args.ticker:
        targets = [args.ticker.upper()]
    elif args.all:
        targets = _list_us_tickers("all")
    else:
        targets = _list_us_tickers("holdings")

    sess = _session()
    cik_map = _ticker_map_from_sec(sess)
    print(f"SEC XBRL — fetching {len(targets)} ticker(s) (cik_map_size={len(cik_map)})")

    ok = err = 0
    for tk in targets:
        try:
            r = fetch_one(sess, cik_map, tk)
            if r is None or "_error" in r:
                err += 1
                why = r.get("_error", "unknown") if r else "none"
                print(f"  {tk:<8} ERROR — {why}")
                continue
            if args.backfill:
                # Walk all available quarter-end dates and persist each
                cik10 = cik_map[tk]
                facts = fetch_companyfacts(sess, cik10)
                ni_facts = _extract_facts(facts.get("facts", {}), CONCEPT_FALLBACKS["net_income"])
                quarters = sorted({f.get("end") for f in ni_facts if _is_quarterly(f) and f.get("end")},
                                  reverse=True)
                bf_count = 0
                for q_end in quarters:
                    bf = derive_us_from_xbrl(tk, facts, as_of=q_end)
                    if bf:
                        persist(bf)
                        bf_count += 1
                ok += 1
                print(f"  {tk:<8} backfilled {bf_count} periods (latest {quarters[0] if quarters else 'N/A'})")
            else:
                persist(r)
                ok += 1
                eps = f"{r.get('eps_ttm'):.4f}" if r.get('eps_ttm') is not None else "—"
                roe = f"{r.get('roe_ttm')*100:.1f}%" if r.get('roe_ttm') is not None else "—"
                print(f"  {tk:<8} {r['period_end']} EPS_ttm={eps:<10} ROE_ttm={roe:<7} "
                      f"n_q={r.get('n_quarters', '?')}")
        except Exception as e:  # noqa: BLE001
            err += 1
            print(f"  {tk:<8} ERROR — {e}")

    print(f"\nPersisted {ok} | errors {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
