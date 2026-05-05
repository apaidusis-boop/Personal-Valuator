"""Moat Scoring Engine — composite 0-10 com 4 sub-scores.

Inspirado em Pat Dorsey ("The Little Book That Builds Wealth") e Buffett's
durable competitive advantage. As 5 dimensões clássicas (intangible assets,
switching costs, network effects, cost advantage, efficient scale) não são
todas extraíveis de financials. Aqui usamos *proxies financeiros* das 4
manifestações observáveis num P&L / BS / DFC com 5 anos de história:

    1. pricing_power        — gross margin LEVEL + STABILITY
       Empresa com brand / switching costs cobra prémio e mantém-no.
       GM volátil = empresa cíclica / commodity.

    2. capital_efficiency   — ROIC LEVEL + PERSISTÊNCIA
       Moat económico real = ROIC > custo de capital de forma persistente.
       Buffett: 15% como bar mínimo; 20%+ é wide moat.

    3. reinvestment_runway  — revenue growth DURABILIDADE + FCF/NI
       Compounder = cresce sem queimar caixa. FCF/NI ≥ 1 é earnings quality.
       Crescimento sem down-years sugere demanda inelástica.

    4. scale_durability     — operating margin TREND + share count TREND
       Operating leverage (margens subindo) confirma moat económico.
       Buybacks (shares caindo) confirma capital allocation disciplinada.

Cada sub-score é 0-10. Overall = média simples dos 4.

  overall ≥ 7   →  STRONG  (wide moat candidate)
  overall 5-7   →  NEUTRAL (narrow / unclear)
  overall < 5   →  WEAK    (no moat / commodity-like)

Requer ≥3 períodos anuais de deep_fundamentals. Exclui financials/REITs
(gross margin não significa o mesmo, ROIC requer ajuste BACEN).

Nota intencional: este score é **complementar** a Piotroski/Altman/Beneish.
Aqueles medem qualidade contábil e distress de curto prazo. Moat mede
**durabilidade** da vantagem económica. Empresa pode ter F=8 e moat=3
(execution boa numa indústria sem moat — Piotroski mede o jockey, moat
mede o cavalo).

CLI:
    python -m scoring.moat JNJ
    python -m scoring.moat ITSA4 --market br
    python -m scoring.moat KO --json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# Sectores onde o framework não faz sentido (mesma lógica que Piotroski/Altman)
EXCLUDED_SECTORS = {
    "Banks", "Financials", "Holding", "Insurance",
    "REIT", "FII", "Shopping", "Logística",
    "Papel (CRI)", "Híbrido", "Corporativo", "ETF-RF", "ETF-US",
}

# Tax rates para NOPAT (alinhado com scoring/roic.py)
TAX_RATES = {"us": 0.21, "br": 0.34}

# Mínimo de períodos anuais para correr o engine
MIN_YEARS = 3


@dataclass
class MoatScore:
    ticker: str
    applicable: bool
    reason_if_not_applicable: str | None = None
    overall: float | None = None              # 0-10
    pricing_power: float | None = None        # 0-10
    capital_efficiency: float | None = None   # 0-10
    reinvestment_runway: float | None = None  # 0-10
    scale_durability: float | None = None     # 0-10
    years_used: int | None = None
    period_first: str | None = None
    period_last: str | None = None
    details: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        if not self.applicable or self.overall is None:
            return "N/A"
        if self.overall >= 7:
            return "STRONG"
        if self.overall >= 5:
            return "NEUTRAL"
        return "WEAK"


# ─── DB helpers ───────────────────────────────────────────────────────────

def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        path = _db(mk)
        if not path.exists():
            continue
        with sqlite3.connect(path) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


def _fetch_history(conn: sqlite3.Connection, ticker: str) -> list[dict]:
    """Devolve até 5 anos de annual rows, ordem cronológica (oldest first)."""
    rows = conn.execute(
        """SELECT period_end, total_revenue, gross_profit, ebit, net_income,
                  free_cash_flow, stockholders_equity, total_debt,
                  shares_outstanding, diluted_avg_shares
           FROM deep_fundamentals
           WHERE ticker=? AND period_type='annual'
             AND total_revenue IS NOT NULL
           ORDER BY period_end DESC LIMIT 5""",
        (ticker,),
    ).fetchall()
    cols = ["period_end", "total_revenue", "gross_profit", "ebit", "net_income",
            "free_cash_flow", "stockholders_equity", "total_debt",
            "shares_outstanding", "diluted_avg_shares"]
    return list(reversed([dict(zip(cols, r)) for r in rows]))


# ─── Sub-score 1: Pricing Power (gross margin) ────────────────────────────

def _pricing_power(rows: list[dict], details: dict, notes: list[str]) -> float | None:
    """0-10 score from gross margin level + stability."""
    gms = []
    for r in rows:
        if r["gross_profit"] is None or not r["total_revenue"]:
            continue
        gms.append(r["gross_profit"] / r["total_revenue"])
    if len(gms) < MIN_YEARS:
        notes.append("pricing_power: gross_profit incompleto, ignorado")
        return None

    median_gm = statistics.median(gms)
    details["gm_median"] = round(median_gm, 4)

    # Level (0-6)
    if median_gm >= 0.50:
        level_pts = 6.0
    elif median_gm >= 0.40:
        level_pts = 5.0
    elif median_gm >= 0.30:
        level_pts = 4.0
    elif median_gm >= 0.20:
        level_pts = 2.0
    else:
        level_pts = 0.0

    # Stability via coefficient of variation (0-4)
    if len(gms) >= 2 and median_gm > 0:
        cv = statistics.stdev(gms) / median_gm
        details["gm_cv"] = round(cv, 4)
        if cv < 0.05:
            stab_pts = 4.0
        elif cv < 0.10:
            stab_pts = 3.0
        elif cv < 0.20:
            stab_pts = 2.0
        elif cv < 0.30:
            stab_pts = 1.0
        else:
            stab_pts = 0.0
    else:
        stab_pts = 2.0  # neutro se só há 1 ponto

    return round(level_pts + stab_pts, 2)


# ─── Sub-score 2: Capital Efficiency (ROIC level + persistence) ───────────

def _roic_for_row(row: dict, market: str) -> float | None:
    """ROIC simplificado: NOPAT / (equity + debt)."""
    ebit = row.get("ebit")
    equity = row.get("stockholders_equity")
    debt = row.get("total_debt") or 0.0
    if ebit is None or equity is None or equity <= 0:
        return None
    invested = equity + debt
    if invested <= 0:
        return None
    nopat = ebit * (1 - TAX_RATES.get(market, 0.21))
    return nopat / invested


def _capital_efficiency(rows: list[dict], market: str, details: dict, notes: list[str]) -> float | None:
    """0-10 from ROIC median level + persistence above 12%."""
    roics = [r for r in (_roic_for_row(row, market) for row in rows) if r is not None]
    if len(roics) < MIN_YEARS:
        notes.append("capital_efficiency: ROIC incomputável (equity ou ebit missing)")
        return None

    median_roic = statistics.median(roics)
    details["roic_median"] = round(median_roic, 4)

    # Level (0-6)
    if median_roic >= 0.20:
        level_pts = 6.0
    elif median_roic >= 0.15:
        level_pts = 5.0
    elif median_roic >= 0.10:
        level_pts = 3.0
    elif median_roic >= 0.05:
        level_pts = 1.0
    else:
        level_pts = 0.0

    # Persistence — fração de anos com ROIC >= 12% (0-4)
    above_bar = sum(1 for r in roics if r >= 0.12)
    fraction = above_bar / len(roics)
    details["roic_persistence"] = round(fraction, 2)
    if fraction >= 1.0:
        pers_pts = 4.0
    elif fraction >= 0.80:
        pers_pts = 3.0
    elif fraction >= 0.60:
        pers_pts = 2.0
    elif fraction >= 0.40:
        pers_pts = 1.0
    else:
        pers_pts = 0.0

    return round(level_pts + pers_pts, 2)


# ─── Sub-score 3: Reinvestment Runway (growth + FCF/NI) ───────────────────

def _reinvestment_runway(rows: list[dict], details: dict, notes: list[str]) -> float | None:
    """0-10 from revenue CAGR + down-year count + FCF/NI conversion."""
    revs = [r["total_revenue"] for r in rows if r.get("total_revenue") is not None]
    if len(revs) < MIN_YEARS:
        notes.append("reinvestment_runway: revenue history insuficiente")
        return None

    # CAGR (0-4 pts)
    n = len(revs) - 1
    if revs[0] > 0 and revs[-1] > 0:
        cagr = (revs[-1] / revs[0]) ** (1 / n) - 1
    else:
        cagr = 0.0
    details["revenue_cagr"] = round(cagr, 4)
    if cagr >= 0.10:
        cagr_pts = 4.0
    elif cagr >= 0.05:
        cagr_pts = 3.0
    elif cagr >= 0.02:
        cagr_pts = 2.0
    elif cagr >= 0.0:
        cagr_pts = 1.0
    else:
        cagr_pts = 0.0

    # Down-year count (0-3 pts)
    down_years = 0
    for i in range(1, len(revs)):
        if revs[i] < revs[i - 1]:
            down_years += 1
    details["down_years"] = down_years
    if down_years == 0:
        down_pts = 3.0
    elif down_years == 1:
        down_pts = 2.0
    elif down_years == 2:
        down_pts = 1.0
    else:
        down_pts = 0.0

    # FCF / NI conversion (0-3 pts)
    ratios = []
    for r in rows:
        fcf, ni = r.get("free_cash_flow"), r.get("net_income")
        if fcf is None or ni is None or ni <= 0:
            continue
        ratios.append(fcf / ni)
    if ratios:
        median_ratio = statistics.median(ratios)
        details["fcf_to_ni_median"] = round(median_ratio, 3)
        if median_ratio >= 1.0:
            fcf_pts = 3.0
        elif median_ratio >= 0.8:
            fcf_pts = 2.0
        elif median_ratio >= 0.6:
            fcf_pts = 1.0
        else:
            fcf_pts = 0.0
    else:
        fcf_pts = 1.5  # neutro se incomputável
        notes.append("reinvestment_runway: FCF/NI incomputável (NI≤0 ou missing)")

    return round(cagr_pts + down_pts + fcf_pts, 2)


# ─── Sub-score 4: Scale Durability (op margin + share count) ──────────────

def _scale_durability(rows: list[dict], details: dict, notes: list[str]) -> float | None:
    """0-10 from operating margin trend + share count trend + level."""
    op_margins = []
    for r in rows:
        if r.get("ebit") is None or not r.get("total_revenue"):
            continue
        op_margins.append(r["ebit"] / r["total_revenue"])
    if len(op_margins) < MIN_YEARS:
        notes.append("scale_durability: operating margin incomputável")
        return None

    # Trend: last vs first (0-4 pts)
    delta = op_margins[-1] - op_margins[0]
    details["op_margin_delta"] = round(delta, 4)
    if delta >= 0.03:
        trend_pts = 4.0
    elif delta >= 0.01:
        trend_pts = 3.0
    elif delta >= -0.01:
        trend_pts = 2.0
    elif delta >= -0.03:
        trend_pts = 1.0
    else:
        trend_pts = 0.0

    # Shares trend (0-4 pts)
    def _shares(r: dict) -> float | None:
        return r.get("diluted_avg_shares") or r.get("shares_outstanding")
    sh_first = _shares(rows[0])
    sh_last = _shares(rows[-1])
    if sh_first and sh_last and sh_first > 0:
        sh_delta = (sh_last / sh_first) - 1
        details["shares_delta_pct"] = round(sh_delta * 100, 2)
        if sh_delta <= -0.05:
            sh_pts = 4.0
        elif sh_delta <= 0.0:
            sh_pts = 3.0
        elif sh_delta <= 0.01:
            sh_pts = 2.0
        elif sh_delta <= 0.03:
            sh_pts = 1.0
        else:
            sh_pts = 0.0
    else:
        sh_pts = 2.0
        notes.append("scale_durability: shares outstanding incomputável, default 2pts")

    # Level (0-2 pts)
    median_om = statistics.median(op_margins)
    details["op_margin_median"] = round(median_om, 4)
    if median_om >= 0.20:
        level_pts = 2.0
    elif median_om >= 0.10:
        level_pts = 1.0
    else:
        level_pts = 0.0

    return round(trend_pts + sh_pts + level_pts, 2)


# ─── Public API ───────────────────────────────────────────────────────────

def compute(ticker: str, market: str | None = None) -> MoatScore:
    market = market or _detect_market(ticker)
    if market is None:
        return MoatScore(ticker=ticker, applicable=False,
                         reason_if_not_applicable="ticker não encontrado em nenhuma DB")

    with sqlite3.connect(_db(market)) as conn:
        sec_row = conn.execute(
            "SELECT sector FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        sector = sec_row[0] if sec_row else None
        if sector in EXCLUDED_SECTORS:
            return MoatScore(
                ticker=ticker, applicable=False,
                reason_if_not_applicable=f"moat framework não se aplica a sector '{sector}'",
            )
        rows = _fetch_history(conn, ticker)

    if len(rows) < MIN_YEARS:
        return MoatScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable=f"precisa >={MIN_YEARS} anos de deep_fundamentals (tem {len(rows)})",
        )

    details: dict = {}
    notes: list[str] = []
    pp = _pricing_power(rows, details, notes)
    ce = _capital_efficiency(rows, market, details, notes)
    rr = _reinvestment_runway(rows, details, notes)
    sd = _scale_durability(rows, details, notes)

    sub_scores = [s for s in (pp, ce, rr, sd) if s is not None]
    if len(sub_scores) < 3:
        return MoatScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable=">=2 sub-scores incomputaveis (data muito esparsa)",
            details=details, notes=notes,
        )

    overall = round(sum(sub_scores) / len(sub_scores), 2)

    return MoatScore(
        ticker=ticker, applicable=True,
        overall=overall,
        pricing_power=pp,
        capital_efficiency=ce,
        reinvestment_runway=rr,
        scale_durability=sd,
        years_used=len(rows),
        period_first=rows[0]["period_end"],
        period_last=rows[-1]["period_end"],
        details=details,
        notes=notes,
    )


# ─── CLI ──────────────────────────────────────────────────────────────────

def _print(score: MoatScore) -> None:
    print(f"\nMoat Score - {score.ticker}")
    print("=" * 62)
    if not score.applicable:
        print(f"  N/A: {score.reason_if_not_applicable}")
        return

    print(f"  Janela: {score.period_first} -> {score.period_last}  ({score.years_used} anos)")
    print()
    label_tag = {"STRONG":  "[+] STRONG (wide moat)",
                 "NEUTRAL": "[~] NEUTRAL (narrow / unclear)",
                 "WEAK":    "[-] WEAK (no moat / commodity)"}[score.label]
    print(f"  Overall: {score.overall:.2f}/10   ->{label_tag}")
    print("-" * 62)

    rows = [
        ("1. Pricing Power      ", score.pricing_power,
         f"GM med={score.details.get('gm_median', 0)*100:.1f}%, "
         f"CV={score.details.get('gm_cv', 0):.3f}"),
        ("2. Capital Efficiency ", score.capital_efficiency,
         f"ROIC med={score.details.get('roic_median', 0)*100:.1f}%, "
         f"persist={score.details.get('roic_persistence', 0)*100:.0f}%"),
        ("3. Reinvest Runway    ", score.reinvestment_runway,
         f"Rev CAGR={score.details.get('revenue_cagr', 0)*100:.1f}%, "
         f"down={int(score.details.get('down_years', 0))}, "
         f"FCF/NI={score.details.get('fcf_to_ni_median', 0):.2f}"),
        ("4. Scale Durability   ", score.scale_durability,
         f"OpM med={score.details.get('op_margin_median', 0)*100:.1f}%, "
         f"d={score.details.get('op_margin_delta', 0)*100:+.1f}pp, "
         f"shares d={score.details.get('shares_delta_pct', 0):+.1f}%"),
    ]
    for label, val, hint in rows:
        if val is None:
            print(f"  {label}    N/A    ({hint})")
        else:
            print(f"  {label}  {val:5.2f}/10  ({hint})")

    if score.notes:
        print("\n  notes:")
        for n in score.notes:
            print(f"    - {n}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Moat Score 0-10 (4 sub-scores)")
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--json", action="store_true", help="emit JSON instead of table")
    args = ap.parse_args()

    score = compute(args.ticker.upper(), args.market)
    if args.json:
        d = {k: v for k, v in asdict(score).items() if v is not None and v != []}
        d["label"] = score.label
        print(json.dumps(d, indent=2))
    else:
        _print(score)
    return 0 if score.applicable else 1


if __name__ == "__main__":
    raise SystemExit(main())
