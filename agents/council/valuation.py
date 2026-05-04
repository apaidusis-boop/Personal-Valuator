"""DCF + multiples + financial evolution — deterministic numbers for narrative.

The narrative engine should never compute DCF in prose. Compute here, pass the
numbers in, the LLM only writes the rationale around them.

Conservative DCF: FCF base × growth annuity (5y) + perpetuity / (WACC - g_inf).
WACC for BR = Selic + 4.5% equity premium ~ 18% (matches STORYT_1 v5.0 reference).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}

WACC_BR = 0.18  # Selic 13.75% + 4.5% equity premium, conservative
WACC_US = 0.10  # 10Y Treasury + 5.5% premium
EBITDA_DA_UPLIFT = 0.10  # D&A typically 8-12% on EBIT for industrials


@dataclass
class FinancialRow:
    period_end: str
    revenue: float | None
    ebit: float | None
    net_income: float | None
    fcf: float | None
    total_debt: float | None
    equity: float | None
    op_cashflow: float | None

    @property
    def ebitda_estimate(self) -> float | None:
        if self.ebit is None:
            return None
        return self.ebit * (1 + EBITDA_DA_UPLIFT)

    @property
    def ebit_margin(self) -> float | None:
        if not self.revenue or not self.ebit or self.revenue == 0:
            return None
        return self.ebit / self.revenue

    @property
    def ebitda_margin(self) -> float | None:
        ebitda = self.ebitda_estimate
        if not self.revenue or not ebitda or self.revenue == 0:
            return None
        return ebitda / self.revenue

    @property
    def net_margin(self) -> float | None:
        if not self.revenue or not self.net_income or self.revenue == 0:
            return None
        return self.net_income / self.revenue


@dataclass
class DCFResult:
    pessimistic_value: float | None
    base_value: float | None
    optimistic_value: float | None
    base_growth: float
    base_perpetuity: float
    base_wacc: float
    margin_of_safety_pct: float | None
    current_price: float | None


def fetch_annual_evolution(ticker: str, market: str, n: int = 5) -> list[FinancialRow]:
    """Pull annual deep_fundamentals as FinancialRow objects, newest first."""
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        try:
            rows = c.execute("""
                SELECT period_end, total_revenue, ebit, net_income, free_cash_flow,
                       total_debt, stockholders_equity, operating_cashflow
                FROM deep_fundamentals
                WHERE ticker = ? AND period_type = 'annual'
                ORDER BY period_end DESC
                LIMIT ?
            """, (ticker, n)).fetchall()
        except sqlite3.OperationalError:
            return []
    out: list[FinancialRow] = []
    for r in rows:
        out.append(FinancialRow(
            period_end=r["period_end"],
            revenue=r["total_revenue"],
            ebit=r["ebit"],
            net_income=r["net_income"],
            fcf=r["free_cash_flow"],
            total_debt=r["total_debt"],
            equity=r["stockholders_equity"],
            op_cashflow=r["operating_cashflow"],
        ))
    return out


def render_evolution_table(rows: list[FinancialRow], scale: float = 1e9, suffix: str = "B") -> str:
    """Markdown table — Receita | EBIT | EBITDA est | Net Income | FCF | margens."""
    if not rows:
        return "| Sem dados anuais disponíveis |\n|---|"
    lines = [
        "| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in reversed(rows):  # oldest first
        rev = f"R$ {r.revenue/scale:.2f}{suffix}" if r.revenue else "—"
        ebit = f"R$ {r.ebit/scale:.2f}{suffix}" if r.ebit else "—"
        ebitda = f"R$ {r.ebitda_estimate/scale:.2f}{suffix}" if r.ebitda_estimate else "—"
        eb_m = f"{r.ebitda_margin*100:.1f}%" if r.ebitda_margin else "—"
        ni = f"R$ {r.net_income/scale:.2f}{suffix}" if r.net_income else "—"
        nm = f"{r.net_margin*100:.1f}%" if r.net_margin else "—"
        fcf = f"R$ {r.fcf/scale:.2f}{suffix}" if r.fcf is not None else "—"
        year = r.period_end[:4] if r.period_end else "?"
        lines.append(f"| {year} | {rev} | {ebit} | {ebitda} | {eb_m} | {ni} | {nm} | {fcf} |")
    return "\n".join(lines)


def compute_net_debt(fundamentals: dict, ev: list[FinancialRow]) -> float | None:
    """Approximate Net Debt from total_debt minus cash proxy.
    Cash proxy: working capital × 0.4 (rough industrial benchmark)."""
    if not ev:
        return None
    latest = ev[0]
    if latest.total_debt is None:
        return None
    # If we have a market_cap and equity, can derive cash proxy
    # Rough: industrial cash ratio ~25% of current_assets, but we don't have CA here
    # Conservative: assume 30% of total debt is offset by cash
    return latest.total_debt * 0.5


def compute_dcf(ev: list[FinancialRow], current_price: float | None, shares_out: float | None,
                market: str = "br") -> DCFResult:
    """3-scenario DCF on FCF base. Scenarios: pessimistic 5%g/3%∞, base 8%g/4%∞, optimistic 11%g/5%∞.
    WACC fixed by jurisdiction."""
    wacc = WACC_BR if market == "br" else WACC_US

    if not ev or not ev[0].fcf or ev[0].fcf <= 0:
        return DCFResult(None, None, None, 0.08, 0.04, wacc, None, current_price)

    fcf0 = ev[0].fcf

    def _intrinsic(growth: float, g_inf: float) -> float:
        # 5y growth annuity + perpetuity
        total = 0.0
        for t in range(1, 6):
            total += fcf0 * ((1 + growth) ** t) / ((1 + wacc) ** t)
        terminal_fcf = fcf0 * ((1 + growth) ** 5) * (1 + g_inf)
        terminal_value = terminal_fcf / (wacc - g_inf)
        total += terminal_value / ((1 + wacc) ** 5)
        return total

    pess_ev = _intrinsic(0.05, 0.03)
    base_ev = _intrinsic(0.08, 0.04)
    opt_ev = _intrinsic(0.11, 0.05)

    if shares_out and shares_out > 0:
        pess_v = pess_ev / shares_out
        base_v = base_ev / shares_out
        opt_v = opt_ev / shares_out
    else:
        pess_v = pess_ev
        base_v = base_ev
        opt_v = opt_ev

    mos = None
    if current_price and base_v and current_price > 0:
        mos = (base_v - current_price) / current_price

    return DCFResult(
        pessimistic_value=pess_v,
        base_value=base_v,
        optimistic_value=opt_v,
        base_growth=0.08,
        base_perpetuity=0.04,
        base_wacc=wacc,
        margin_of_safety_pct=mos,
        current_price=current_price,
    )


def render_dcf_table(dcf: DCFResult) -> str:
    if dcf.base_value is None:
        return "| DCF | Não calculado (FCF ausente ou negativo) |"
    lines = [
        "| Cenário | Crescimento 5y | Perpetuidade | Valor por ação |",
        "|---|---|---|---|",
        f"| Pessimista | 5% a.a. | 3% | R$ {dcf.pessimistic_value:.2f} |",
        f"| **Base** | **8% a.a.** | **4%** | **R$ {dcf.base_value:.2f}** |",
        f"| Optimista | 11% a.a. | 5% | R$ {dcf.optimistic_value:.2f} |",
    ]
    if dcf.current_price and dcf.margin_of_safety_pct is not None:
        lines.append("")
        lines.append(
            f"**Preço actual**: R$ {dcf.current_price:.2f}  ·  "
            f"**Margem de segurança (vs base)**: {dcf.margin_of_safety_pct*100:+.0f}%  ·  "
            f"**WACC**: {dcf.base_wacc*100:.0f}%"
        )
    return "\n".join(lines)


def get_shares_outstanding(ticker: str, market: str) -> float | None:
    db = DBS[market]
    if not db.exists():
        return None
    with sqlite3.connect(db) as c:
        try:
            row = c.execute("""
                SELECT shares_outstanding FROM deep_fundamentals
                WHERE ticker = ? AND period_type = 'annual'
                ORDER BY period_end DESC LIMIT 1
            """, (ticker,)).fetchone()
            return row[0] if row and row[0] else None
        except sqlite3.OperationalError:
            return None
