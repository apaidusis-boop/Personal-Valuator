"""Piotroski F-Score — quality composite 0-9 (binário por critério).

Referência: Piotroski, J. (2000). "Value Investing: The Use of Historical
Financial Statement Information to Separate Winners from Losers from Losers."

Nove critérios, 1 ponto cada se cumpre:

  Rentabilidade (4):
    1. ROA > 0                    (year t)
    2. FCF > 0                    (year t)
    3. ΔROA > 0                   (ROA_t > ROA_{t-1})
    4. FCF > Net Income           (quality of earnings)

  Alavancagem / Liquidez (3):
    5. Δ Long-Term Debt ≤ 0       (debt não subiu)
    6. Δ Current Ratio > 0        (liquidez melhorou)
    7. Shares não subiram         (sem dilution)

  Eficiência (2):
    8. Δ Gross Margin > 0         (margem bruta subiu)
    9. Δ Asset Turnover > 0       (Rev/TA subiu)

Leitura:
  F ≥ 7  →  strong quality (top decile histórico outperforma em 7%/y)
  F = 4-6 → neutro
  F ≤ 3  →  avoid (red flag; veto forte)

Requer 2 períodos anuais consecutivos na deep_fundamentals. Se só há 1, devolve
applicable=False.

CLI:
    python -m scoring.piotroski JNJ
    python -m scoring.piotroski ITSA4 --market br
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# Mesmos sectores excluídos do Altman (financials têm contabilidade distinta)
EXCLUDED_SECTORS = {"Banks", "Financials", "REIT", "FII", "Shopping", "Logística",
                    "Papel (CRI)", "Híbrido", "Corporativo", "ETF-RF", "ETF-US"}


@dataclass
class PiotroskiScore:
    ticker: str
    applicable: bool
    reason_if_not_applicable: str | None = None
    f_score: int | None = None
    period_t: str | None = None
    period_t_minus_1: str | None = None
    criteria: dict[str, bool] = field(default_factory=dict)
    details: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def is_strong(self) -> bool:
        return self.applicable and self.f_score is not None and self.f_score >= 7

    @property
    def is_weak(self) -> bool:
        return self.applicable and self.f_score is not None and self.f_score <= 3

    @property
    def label(self) -> str:
        if not self.applicable:
            return "N/A"
        if self.is_strong:
            return "STRONG"
        if self.is_weak:
            return "WEAK"
        return "NEUTRAL"


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        with sqlite3.connect(_db(mk)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


def _fetch_two_periods(conn: sqlite3.Connection, ticker: str) -> list[dict] | None:
    """Devolve lista com 2 rows (mais recente primeiro), ou None se insuficiente.

    Exige total_assets e net_income não-null em ambos. Ignora rows stub (só RE
    preenchido, como o ano mais antigo de yfinance tipicamente).
    """
    rows = conn.execute(
        """SELECT period_end, total_assets, current_assets, current_liabilities,
                  long_term_debt, net_income, total_revenue, gross_profit,
                  free_cash_flow, operating_cashflow, capital_expenditure,
                  diluted_avg_shares, shares_outstanding
           FROM deep_fundamentals
           WHERE ticker=? AND period_type='annual'
             AND total_assets IS NOT NULL AND net_income IS NOT NULL
           ORDER BY period_end DESC LIMIT 2""",
        (ticker,),
    ).fetchall()
    if len(rows) < 2:
        return None
    cols = ["period_end", "total_assets", "current_assets", "current_liabilities",
            "long_term_debt", "net_income", "total_revenue", "gross_profit",
            "free_cash_flow", "operating_cashflow", "capital_expenditure",
            "diluted_avg_shares", "shares_outstanding"]
    return [dict(zip(cols, r)) for r in rows]


def compute(ticker: str, market: str | None = None) -> PiotroskiScore:
    notes: list[str] = []
    market = market or _detect_market(ticker)
    if market is None:
        return PiotroskiScore(ticker=ticker, applicable=False,
                              reason_if_not_applicable="ticker não encontrado em nenhuma DB")

    with sqlite3.connect(_db(market)) as conn:
        sec_row = conn.execute(
            "SELECT sector FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        sector = sec_row[0] if sec_row else None
        if sector in EXCLUDED_SECTORS:
            return PiotroskiScore(
                ticker=ticker, applicable=False,
                reason_if_not_applicable=f"Piotroski não se aplica a sector '{sector}'",
            )
        periods = _fetch_two_periods(conn, ticker)

    if not periods:
        return PiotroskiScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable="precisa 2 períodos anuais completos em deep_fundamentals",
        )
    t, tm1 = periods[0], periods[1]

    # computa rácios derivados
    def _roa(row: dict) -> float | None:
        if row["net_income"] is None or not row["total_assets"]:
            return None
        return row["net_income"] / row["total_assets"]

    def _cr(row: dict) -> float | None:
        if row["current_assets"] is None or not row["current_liabilities"]:
            return None
        return row["current_assets"] / row["current_liabilities"]

    def _gm(row: dict) -> float | None:
        if row["gross_profit"] is None or not row["total_revenue"]:
            return None
        return row["gross_profit"] / row["total_revenue"]

    def _at(row: dict) -> float | None:
        if row["total_revenue"] is None or not row["total_assets"]:
            return None
        return row["total_revenue"] / row["total_assets"]

    def _shares(row: dict) -> float | None:
        return row["diluted_avg_shares"] or row["shares_outstanding"]

    roa_t, roa_tm1 = _roa(t), _roa(tm1)
    cr_t, cr_tm1 = _cr(t), _cr(tm1)
    gm_t, gm_tm1 = _gm(t), _gm(tm1)
    at_t, at_tm1 = _at(t), _at(tm1)
    sh_t, sh_tm1 = _shares(t), _shares(tm1)
    fcf_t = t["free_cash_flow"]
    ni_t = t["net_income"]
    ltd_t, ltd_tm1 = t["long_term_debt"], tm1["long_term_debt"]

    criteria: dict[str, bool] = {}
    details: dict[str, float] = {}

    # 1. ROA > 0
    criteria["roa_positive"] = (roa_t is not None and roa_t > 0)
    details["roa_t"] = roa_t if roa_t is not None else float("nan")

    # 2. FCF > 0
    criteria["fcf_positive"] = (fcf_t is not None and fcf_t > 0)
    details["fcf_t"] = fcf_t if fcf_t is not None else float("nan")

    # 3. ΔROA > 0
    criteria["delta_roa_positive"] = (
        roa_t is not None and roa_tm1 is not None and roa_t > roa_tm1
    )
    details["delta_roa"] = (roa_t - roa_tm1) if (roa_t is not None and roa_tm1 is not None) else float("nan")

    # 4. FCF > Net Income (quality of earnings)
    criteria["fcf_gt_netincome"] = (fcf_t is not None and ni_t is not None and fcf_t > ni_t)

    # 5. ΔLong-Term Debt ≤ 0 (debt não subiu; nota: usar / TA evita false alarms de crescimento)
    if ltd_t is not None and ltd_tm1 is not None and t["total_assets"] and tm1["total_assets"]:
        ltd_ratio_t = ltd_t / t["total_assets"]
        ltd_ratio_tm1 = ltd_tm1 / tm1["total_assets"]
        criteria["leverage_not_up"] = ltd_ratio_t <= ltd_ratio_tm1
        details["delta_ltd_ratio"] = ltd_ratio_t - ltd_ratio_tm1
    else:
        # Se LTD ausente em qualquer ano, assume OK (empresas sem LT debt são comuns)
        criteria["leverage_not_up"] = True
        notes.append("leverage_not_up default=True (long_term_debt missing)")

    # 6. Δ Current Ratio > 0
    if cr_t is not None and cr_tm1 is not None:
        criteria["liquidity_up"] = cr_t > cr_tm1
        details["delta_current_ratio"] = cr_t - cr_tm1
    else:
        criteria["liquidity_up"] = False
        notes.append("liquidity_up = False (current ratio incomputável)")

    # 7. Sem dilution (shares flat ou caindo)
    if sh_t is not None and sh_tm1 is not None:
        # tolerância 1% para buyback pequeno ou accretion não conta como dilution
        criteria["no_dilution"] = sh_t <= sh_tm1 * 1.01
        details["shares_delta_pct"] = (sh_t / sh_tm1 - 1) * 100 if sh_tm1 > 0 else 0
    else:
        criteria["no_dilution"] = False
        notes.append("no_dilution = False (shares incomputável)")

    # 8. Δ Gross Margin > 0
    if gm_t is not None and gm_tm1 is not None:
        criteria["margin_up"] = gm_t > gm_tm1
        details["delta_gross_margin"] = gm_t - gm_tm1
    else:
        criteria["margin_up"] = False
        notes.append("margin_up = False (gross profit incomputável)")

    # 9. Δ Asset Turnover > 0
    if at_t is not None and at_tm1 is not None:
        criteria["turnover_up"] = at_t > at_tm1
        details["delta_turnover"] = at_t - at_tm1
    else:
        criteria["turnover_up"] = False
        notes.append("turnover_up = False (asset turnover incomputável)")

    f_score = sum(1 for v in criteria.values() if v)

    return PiotroskiScore(
        ticker=ticker, applicable=True,
        f_score=f_score,
        period_t=t["period_end"], period_t_minus_1=tm1["period_end"],
        criteria=criteria, details=details, notes=notes,
    )


def _print(score: PiotroskiScore) -> None:
    print(f"\nPiotroski F-Score — {score.ticker}")
    print("=" * 62)
    if not score.applicable:
        print(f"  NÃO APLICÁVEL: {score.reason_if_not_applicable}")
        return
    print(f"  Períodos: {score.period_t}  vs  {score.period_t_minus_1}")
    order = ["roa_positive", "fcf_positive", "delta_roa_positive", "fcf_gt_netincome",
             "leverage_not_up", "liquidity_up", "no_dilution", "margin_up", "turnover_up"]
    labels = {
        "roa_positive":       "1. ROA > 0",
        "fcf_positive":       "2. FCF > 0",
        "delta_roa_positive": "3. ΔROA > 0",
        "fcf_gt_netincome":   "4. FCF > Net Income (quality)",
        "leverage_not_up":    "5. Leverage ratio não subiu",
        "liquidity_up":       "6. Current ratio subiu",
        "no_dilution":        "7. Sem dilution (shares ≤ prior)",
        "margin_up":          "8. Gross margin subiu",
        "turnover_up":        "9. Asset turnover subiu",
    }
    for k in order:
        tag = "✓" if score.criteria.get(k) else "✗"
        print(f"  {tag}  {labels[k]}")
    print("-" * 62)
    verdict_tag = {"STRONG": "✓ STRONG", "WEAK": "✗ WEAK", "NEUTRAL": "◦ NEUTRAL"}[score.label]
    print(f"  F-Score = {score.f_score}/9   →  {verdict_tag}")
    if score.is_weak:
        print(f"  ⚠ F ≤ 3 → veto forte sobre BUY")
    if score.notes:
        print("  notes:")
        for n in score.notes:
            print(f"    • {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    args = ap.parse_args()
    score = compute(args.ticker.upper(), args.market)
    _print(score)


if __name__ == "__main__":
    main()
