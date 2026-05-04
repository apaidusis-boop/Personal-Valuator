"""Beneish M-Score — detector de manipulação contábil (Beneish 1999).

Fórmula:
  M = -4.84 + 0.920·DSRI + 0.528·GMI + 0.404·AQI + 0.892·SGI
        + 0.115·DEPI - 0.172·SGAI + 4.679·TATA - 0.327·LVGI

Onde os 8 índices comparam ano corrente (t) vs ano anterior (t-1):

  DSRI = (AR_t / Sales_t) / (AR_t-1 / Sales_t-1)        (Days Sales in Rec)
  GMI  = GM_t-1 / GM_t                                  (Gross Margin Index — invertido)
  AQI  = ((1-(CA+PPE)/TA)_t) / ((1-(CA+PPE)/TA)_t-1)    (Asset Quality)
  SGI  = Sales_t / Sales_t-1                            (Sales Growth)
  DEPI = (Dep_t-1 / (PPE_t-1+Dep_t-1)) / (Dep_t / (PPE_t+Dep_t))   (invertido)
  SGAI = (SGA_t / Sales_t) / (SGA_t-1 / Sales_t-1)
  TATA = (NI_t - OCF_t) / TA_t                          (Total Accruals)
  LVGI = ((LTD+CL)_t / TA_t) / ((LTD+CL)_t-1 / TA_t-1)  (Leverage Index)

Interpretação:
  M < -2.22  → clean (low manipulation risk)
  -2.22 ≤ M < -1.78 → grey zone (monitor)
  M ≥ -1.78  → high manipulation risk (red flag)

Fonte: yfinance live (mesmo approach do V10 Personal Equity Valuator). Alguns
campos podem faltar conforme o ticker (especialmente fora de US large-cap).
Quando faltam, o sub-índice cai a neutral (1.0) e confidence baixa.

Aplicabilidade: não se aplica a bancos, REITs, FIIs (estrutura de balanço
incompatível). Para esses, applicable=False.

CLI:
    python -m scoring.beneish JNJ
    python -m scoring.beneish ITSA4 --market br
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

EXCLUDED_SECTORS = {"Banks", "Financials", "REIT", "FII", "Shopping", "Logística",
                    "Papel (CRI)", "Híbrido", "Corporativo", "ETF-RF", "ETF-US"}


@dataclass
class BeneishScore:
    ticker: str
    applicable: bool
    reason_if_not_applicable: str | None = None
    m: float | None = None
    zone: str | None = None          # 'clean' | 'grey' | 'risk'
    confidence: str | None = None    # 'high' | 'medium' | 'low'
    indices: dict = field(default_factory=dict)
    period_end: str | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def is_risk(self) -> bool:
        return self.applicable and self.m is not None and self.m >= -1.78

    @property
    def is_clean(self) -> bool:
        return self.applicable and self.m is not None and self.m < -2.22


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        with sqlite3.connect(_db(mk)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


def _safe(df, row: str, col_idx: int = 0, default: float = 0.0) -> float:
    """Tolerant DataFrame[row, col] lookup."""
    try:
        if df is None or df.empty or row not in df.index:
            return default
        v = df.loc[row].iloc[col_idx]
        if v is None:
            return default
        try:
            import math
            if math.isnan(float(v)):
                return default
        except (TypeError, ValueError):
            return default
        return float(v)
    except (IndexError, KeyError, TypeError, AttributeError):
        return default


def _div(a: float, b: float, default: float = 1.0) -> float:
    """Safe division with neutral fallback (1.0 = no change for ratio indices)."""
    if not b:
        return default
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
        return default


# ─── ADR currency adjustment (mirror V10) ──────────────────────────────────
BR_ADR_TICKERS = {"PICS", "STNE", "PAGS", "NU", "VTEX", "ARCE", "BRFS", "VALE", "ITUB", "PBR"}


def _normalize_br_adr(ticker: str, *dfs):
    """Divide BS/IS/CF dataframes by USD/BRL if ADR. Returns adjusted dfs + rate (or 1.0)."""
    if ticker not in BR_ADR_TICKERS:
        return list(dfs) + [1.0]
    try:
        import yfinance as yf
        rate = float(yf.Ticker("USDBRL=X").history(period="1d")["Close"].iloc[-1])
    except Exception:
        return list(dfs) + [1.0]
    out = []
    for df in dfs:
        if df is not None and hasattr(df, "empty") and not df.empty:
            try:
                out.append(df / rate)
                continue
            except Exception:
                pass
        out.append(df)
    return out + [rate]


def compute(ticker: str, market: str | None = None) -> BeneishScore:
    """Compute Beneish M-Score for ticker. Auto-detects market if not given.
    Uses live yfinance fetch (same approach as V10). Tolerant to missing fields."""
    notes: list[str] = []
    market = market or _detect_market(ticker)

    # Sector exclusion check
    if market:
        try:
            with sqlite3.connect(_db(market)) as c:
                sec_row = c.execute(
                    "SELECT sector FROM companies WHERE ticker=?", (ticker,)
                ).fetchone()
                sector = sec_row[0] if sec_row else None
            if sector in EXCLUDED_SECTORS:
                return BeneishScore(
                    ticker=ticker, applicable=False,
                    reason_if_not_applicable=f"Beneish não se aplica a sector '{sector}'",
                )
        except sqlite3.OperationalError:
            pass

    # Fetch live via yfinance
    try:
        import yfinance as yf
    except ImportError:
        return BeneishScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable="yfinance não instalado",
        )

    yf_ticker = ticker
    if market == "br" and "." not in ticker and ticker not in BR_ADR_TICKERS:
        yf_ticker = f"{ticker}.SA"

    try:
        tk = yf.Ticker(yf_ticker)
        is_stmt = tk.income_stmt
        bs_stmt = tk.balance_sheet
        cf_stmt = tk.cashflow
    except Exception as e:
        return BeneishScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable=f"yfinance fetch falhou: {type(e).__name__}",
        )

    is_stmt, bs_stmt, cf_stmt, _rate = _normalize_br_adr(ticker, is_stmt, bs_stmt, cf_stmt)

    # Need at least 2 yearly periods
    if (bs_stmt is None or bs_stmt.empty or len(bs_stmt.columns) < 2 or
        is_stmt is None or is_stmt.empty or len(is_stmt.columns) < 2):
        return BeneishScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable="precisa 2+ anos de demonstrações no yfinance",
        )

    # Period end (most recent column)
    try:
        period_end = str(bs_stmt.columns[0].date()) if hasattr(bs_stmt.columns[0], "date") \
                     else str(bs_stmt.columns[0])
    except Exception:
        period_end = None

    confidence = "high"

    # Required core fields
    ta_0 = _safe(bs_stmt, "Total Assets", 0)
    ta_1 = _safe(bs_stmt, "Total Assets", 1)
    rev_0 = _safe(is_stmt, "Total Revenue", 0)
    rev_1 = _safe(is_stmt, "Total Revenue", 1)
    if not (ta_0 and ta_1 and rev_0 and rev_1):
        return BeneishScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable="campos essenciais (TA/Revenue 2y) ausentes",
        )

    # COGS — preferir explicit, derive from gross_profit if absent
    cogs_0 = _safe(is_stmt, "Cost Of Revenue", 0) or \
             (rev_0 - _safe(is_stmt, "Gross Profit", 0))
    cogs_1 = _safe(is_stmt, "Cost Of Revenue", 1) or \
             (rev_1 - _safe(is_stmt, "Gross Profit", 1))

    # AR (multiple naming conventions)
    ar_0 = (_safe(bs_stmt, "Receivables", 0) or
            _safe(bs_stmt, "Net Receivables", 0) or
            _safe(bs_stmt, "Accounts Receivable", 0))
    ar_1 = (_safe(bs_stmt, "Receivables", 1) or
            _safe(bs_stmt, "Net Receivables", 1) or
            _safe(bs_stmt, "Accounts Receivable", 1))
    if not ar_0 or not ar_1:
        notes.append("DSRI=1 (accounts receivable indisponível)")
        confidence = "low"

    # PPE
    ppe_0 = _safe(bs_stmt, "Net PPE", 0) or _safe(bs_stmt, "Property Plant Equipment Net", 0)
    ppe_1 = _safe(bs_stmt, "Net PPE", 1) or _safe(bs_stmt, "Property Plant Equipment Net", 1)
    if not ppe_0 or not ppe_1:
        notes.append("PPE indisponível — AQI/DEPI degradados")
        if confidence == "high":
            confidence = "medium"

    # Current items
    ca_0 = _safe(bs_stmt, "Current Assets", 0)
    ca_1 = _safe(bs_stmt, "Current Assets", 1)
    cl_0 = _safe(bs_stmt, "Current Liabilities", 0)
    cl_1 = _safe(bs_stmt, "Current Liabilities", 1)

    # Long-term debt (for LVGI)
    ltd_0 = _safe(bs_stmt, "Long Term Debt", 0)
    ltd_1 = _safe(bs_stmt, "Long Term Debt", 1)

    # Depreciation (cashflow)
    dep_0 = abs(_safe(cf_stmt, "Depreciation Amortization Depletion", 0) or
                _safe(cf_stmt, "Depreciation And Amortization", 0))
    dep_1 = abs(_safe(cf_stmt, "Depreciation Amortization Depletion", 1) or
                _safe(cf_stmt, "Depreciation And Amortization", 1))

    # SGA
    sga_0 = _safe(is_stmt, "Selling General Administrative", 0) or \
            _safe(is_stmt, "Selling General And Administration", 0)
    sga_1 = _safe(is_stmt, "Selling General Administrative", 1) or \
            _safe(is_stmt, "Selling General And Administration", 1)
    if not sga_0 or not sga_1:
        notes.append("SGAI=1 (SG&A indisponível)")
        if confidence == "high":
            confidence = "medium"

    # NI / OCF (for TATA)
    ni_0 = _safe(is_stmt, "Net Income", 0)
    ocf_0 = _safe(cf_stmt, "Operating Cash Flow", 0)

    # ── Compute 8 indices ─────────────────────────────────────────────────
    # DSRI: AR-to-sales ratio change. >1 = receivables growing faster than sales.
    dsri = _div(_div(ar_0, rev_0), _div(ar_1, rev_1)) if (ar_0 and ar_1) else 1.0

    # GMI: prior year GM / current year GM. >1 = margin contracting.
    gm_0 = _div(rev_0 - cogs_0, rev_0)
    gm_1 = _div(rev_1 - cogs_1, rev_1)
    gmi = _div(gm_1, gm_0)

    # AQI: non-current-assets-non-PPE share of TA. >1 = quality declining.
    aqi_0 = 1 - _div(ca_0 + ppe_0, ta_0) if (ca_0 and ppe_0) else 1.0
    aqi_1 = 1 - _div(ca_1 + ppe_1, ta_1) if (ca_1 and ppe_1) else 1.0
    aqi = _div(aqi_0, aqi_1)

    # SGI: sales growth. >1 = growing.
    sgi = _div(rev_0, rev_1)

    # DEPI: depreciation rate. >1 = depreciating slower (= overstating earnings).
    depi_n = _div(dep_1, ppe_1 + dep_1) if (dep_1 and ppe_1) else 1.0
    depi_d = _div(dep_0, ppe_0 + dep_0) if (dep_0 and ppe_0) else 1.0
    depi = _div(depi_n, depi_d) if (dep_0 and dep_1) else 1.0

    # SGAI: SG&A-to-sales ratio. >1 = expanding (negative for fraud — coefficient is negative).
    sgai = _div(_div(sga_0, rev_0), _div(sga_1, rev_1)) if (sga_0 and sga_1) else 1.0

    # TATA: total accruals. >0 = aggressive.
    tata = _div(ni_0 - ocf_0, ta_0) if (ni_0 is not None and ocf_0 is not None) else 0.0

    # LVGI: leverage growth.
    lvgi = _div(_div(ltd_0 + cl_0, ta_0), _div(ltd_1 + cl_1, ta_1)) if \
           (cl_0 and cl_1 and ta_0 and ta_1) else 1.0

    m = (-4.84
         + 0.920 * dsri
         + 0.528 * gmi
         + 0.404 * aqi
         + 0.892 * sgi
         + 0.115 * depi
         - 0.172 * sgai
         + 4.679 * tata
         - 0.327 * lvgi)

    if m < -2.22:
        zone = "clean"
    elif m < -1.78:
        zone = "grey"
    else:
        zone = "risk"

    return BeneishScore(
        ticker=ticker, applicable=True,
        m=m, zone=zone, confidence=confidence,
        indices={
            "DSRI": round(dsri, 3), "GMI": round(gmi, 3), "AQI": round(aqi, 3),
            "SGI": round(sgi, 3), "DEPI": round(depi, 3), "SGAI": round(sgai, 3),
            "TATA": round(tata, 4), "LVGI": round(lvgi, 3),
        },
        period_end=period_end, notes=notes,
    )


def _print(score: BeneishScore) -> None:
    print(f"\nBeneish M-Score — {score.ticker}")
    print("=" * 60)
    if not score.applicable:
        print(f"  NÃO APLICÁVEL: {score.reason_if_not_applicable}")
        return
    print(f"  Período: {score.period_end}   Confiança: {score.confidence}")
    print(f"  M = -4.84 + Σ(coef × index)")
    for k, v in score.indices.items():
        print(f"      {k:5} = {v:+.3f}")
    zone_tag = {"clean": "✓ CLEAN", "grey": "◦ GREY", "risk": "✗ RISK"}[score.zone]
    print(f"  M = {score.m:+.3f}  →  {zone_tag}")
    if score.is_risk:
        print(f"  ⚠ M ≥ -1.78 → red flag de manipulação contábil")
    for n in score.notes:
        print(f"  note: {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    args = ap.parse_args()
    score = compute(args.ticker.upper(), market=args.market)
    _print(score)


if __name__ == "__main__":
    main()
