"""STORYT_1 v5.0 — Camada de Filosofia de Investimento.

Deterministic scoring engine for the 5 philosophy lenses:
  - Value (0-12)
  - Growth (0-12)
  - Dividend / DRIP (0-12)
  - Macro Exposure (0-6) + Macro Dependency (0-6)
  - Buffett / Quality (0-12)

Outputs feed Acto 8 of the narrative (filed as `philosophy_scores` on dossier).
The deterministic computation here is what stops the narrative engine from
guessing "Value (8/12)" — it makes the LLM cite the actual computation.

Each criterion that fires is recorded in `breakdown` so the narrative can show
WHY (e.g. "P/E 6.4 < mediana setorial 12 → +2 pts Value").
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PhilosophyScores:
    value: int = 0
    growth: int = 0
    dividend: int = 0
    macro_exposure: int = 0
    macro_dependency: int = 0
    buffett: int = 0
    breakdown: dict[str, list[str]] = field(default_factory=dict)
    primary: str = ""
    secondary: str = ""

    def declare(self) -> str:
        primary = self.primary
        secondary = f" | {self.secondary} " if self.secondary else ""
        return (
            f"PERFIL FILOSÓFICO: {primary}{secondary}\n"
            f"Scores: Value {self.value} | Growth {self.growth} | "
            f"Dividend {self.dividend} | Macro Exp. {self.macro_exposure}/6 · "
            f"Dep. {self.macro_dependency}/6 | Buffett {self.buffett}"
        )


# Sector medians for BR (rough — published mid-cap industrials)
# Used only when peer-level normalization is unavailable. STORYT_1 v5.0
# acknowledges this fallback explicitly.
SECTOR_MEDIAN_PE_BR = {
    "Industrials": 12.0, "Consumer Staples": 14.0, "Consumer Disc.": 13.0,
    "Healthcare": 16.0, "Utilities": 11.0, "Materials": 10.0,
    "Real Estate": 14.0, "Holding": 9.0, "Banks": 8.0,
    "Oil & Gas": 8.0, "Mining": 8.0,
}
IBOV_MEDIAN_PE = 9.0
SELIC_2026 = 0.1375  # April 2026 reference
KE_BR = SELIC_2026 + 0.045  # 18.25% premium of 4.5% over Selic for equity


def _median_pe(sector: str, market: str) -> float:
    if market == "br":
        return SECTOR_MEDIAN_PE_BR.get(sector or "", 12.0)
    return 18.0  # US generic mid


def _add(scores: PhilosophyScores, lens: str, pts: int, reason: str) -> None:
    setattr(scores, lens, getattr(scores, lens) + pts)
    scores.breakdown.setdefault(lens, []).append(f"+{pts} · {reason}")


def compute(dossier_dict: dict[str, Any], annual_evolution: list[dict] | None = None,
            dcf: dict | None = None) -> PhilosophyScores:
    """Compute all 5 philosophy scores from the dossier.

    Args:
      dossier_dict: must include fundamentals (pe, pb, dy, roe, net_debt_ebitda),
                    sector, market, quality_scores (piotroski, altman, beneish).
      annual_evolution: list of annual rows with revenue, ebit, net_income (for growth + DGR proxies)
      dcf: dict with margin_of_safety_pct (for value/buffett bonus).
    """
    s = PhilosophyScores()
    f = dossier_dict.get("fundamentals", {}) or {}
    qs = dossier_dict.get("quality_scores", {}) or {}
    sector = dossier_dict.get("sector") or ""
    market = dossier_dict.get("market") or "br"
    held = bool(dossier_dict.get("is_holding"))

    pe = f.get("pe")
    pb = f.get("pb")
    dy = f.get("dy")
    roe = f.get("roe")
    nde = f.get("net_debt_ebitda")
    streak = f.get("dividend_streak_years") or 0

    median_pe = _median_pe(sector, market)
    mos = (dcf or {}).get("margin_of_safety_pct", 0.0)

    # ── Value (0-12) ───────────────────────────────────────────
    if pe and pe > 0 and pe < median_pe:
        _add(s, "value", 2, f"P/E {pe:.1f} < mediana setorial {median_pe:.0f}")
    if pb and pb < 1.5:
        _add(s, "value", 2, f"P/B {pb:.2f} < 1.5x")
    # FCF Yield > 6% — needs market_cap + FCF
    fcf_yield = None
    mc = f.get("market_cap") or f.get("market_cap_brl") or f.get("market_cap_usd")
    if annual_evolution and mc:
        latest_fcf = annual_evolution[0].get("free_cash_flow") if annual_evolution else None
        if latest_fcf and mc > 0:
            fcf_yield = latest_fcf / mc
            if fcf_yield > 0.06:
                _add(s, "value", 2, f"FCF Yield {fcf_yield*100:.1f}% > 6%")
    if roe and KE_BR and roe > KE_BR:
        _add(s, "value", 2, f"ROE {roe*100:.0f}% > Ke ({KE_BR*100:.1f}%)")
    if mos and mos > 0.25:
        _add(s, "value", 2, f"DCF margin of safety {mos*100:.0f}% > 25%")
    pio_score = qs.get("piotroski", {}).get("f_score") if qs else None
    if pio_score is not None and pio_score >= 7:
        _add(s, "value", 1, f"Piotroski F={pio_score} ≥ 7")

    # ── Growth (0-12) ──────────────────────────────────────────
    # FIX 2026-05-01: revs/nis/margins are filtered (drop None/0 values), so
    # len(annual_evolution) does NOT guarantee len(revs). Index against revs.
    if annual_evolution and len(annual_evolution) >= 2:
        revs = [r.get("total_revenue") for r in annual_evolution[:3] if r.get("total_revenue")]
        if len(revs) >= 2 and revs[1] > 0:
            yoy_rev = (revs[0] / revs[1]) - 1
            if yoy_rev > 0.15:
                _add(s, "growth", 2, f"Receita YoY +{yoy_rev*100:.0f}% > 15%")
            if len(revs) >= 3 and revs[2] > 0:
                yoy_rev_prev = (revs[1] / revs[2]) - 1
                if yoy_rev_prev > 0.15:
                    _add(s, "growth", 1, "Receita prior YoY também > 15%")
        nis = [r.get("net_income") for r in annual_evolution[:3] if r.get("net_income")]
        if len(nis) >= 2 and nis[1] > 0 and (nis[0] / nis[1] - 1) > 0.15:
            _add(s, "growth", 2, f"EPS YoY +{(nis[0]/nis[1]-1)*100:.0f}% > 15%")
        # Margin expansion
        ebits = [(r.get("ebit"), r.get("total_revenue")) for r in annual_evolution[:4]]
        margins = [(e/r) for e, r in ebits if e and r and r > 0]
        if len(margins) >= 3 and margins[0] > margins[2]:
            _add(s, "growth", 2, f"Margem EBIT em expansão {margins[2]*100:.1f}% → {margins[0]*100:.1f}%")
    if pe and roe:
        # PEG ratio rough: PE / (ROE * retention rate ≈ ROE * (1 - payout))
        # Use simpler: PE < 1.5 × growth proxy. Skip if not enough data.
        pass
    # Payout < 30% suggests growth retention — needs payout. Use roe + dy proxy:
    if dy is not None and dy < 0.03 and roe and roe > 0.15:
        _add(s, "growth", 1, "Yield baixo (<3%) + ROE alto → reinvestimento alto")

    # ── Dividend / DRIP (0-12) ─────────────────────────────────
    dy_min = 0.05 if market == "br" else 0.03
    if dy and dy > dy_min:
        _add(s, "dividend", 2, f"DY {dy*100:.1f}% > {dy_min*100:.0f}%")
    if streak >= 5:
        _add(s, "dividend", 2, f"Histórico ininterrupto {int(streak)} anos ≥ 5")
    # DGR > 5% will be fed via annual_evolution side computation in narrative
    # Payout sustainability: FCF cobre dividendo. Need dividend total + FCF.
    if annual_evolution and annual_evolution[0].get("free_cash_flow"):
        # If FCF > 1.5x net income, payout very safe.
        fcf = annual_evolution[0].get("free_cash_flow") or 0
        ni = annual_evolution[0].get("net_income") or 0
        if fcf > 0 and ni > 0 and fcf > ni:
            _add(s, "dividend", 2, "FCF > Lucro líquido — payout cobertura forte")
    # JCP (BR)
    if market == "br" and dy and dy > 0.04:
        _add(s, "dividend", 1, "JCP+Dividendo recurring BR market")

    # ── Macro Exposure (0-6) ──────────────────────────────────
    cyclical_sectors = ("Mining", "Oil & Gas", "Steel", "Materials", "Pulp & Paper", "Aluminum")
    if any(c in sector for c in cyclical_sectors):
        _add(s, "macro_exposure", 2, f"Sector cíclico ({sector})")
    # FX exposure: industrial exporter or commodity
    if "Industrials" in sector and market == "br":
        # Conservative — assume some FX exposure in Brazilian industrials
        _add(s, "macro_exposure", 1, "Industrial BR — exposure cambial parcial")
    # Rate sensitivity
    if nde and nde > 3.0:
        _add(s, "macro_exposure", 1, f"Alavancagem alta (ND/EBITDA {nde:.1f}) → sensível a juros")

    # ── Macro Dependency (0-6) ────────────────────────────────
    if any(c in sector for c in cyclical_sectors):
        _add(s, "macro_dependency", 2, "Receita atrelada a commodity global")
    # If the thesis depends explicitly on a Selic cut etc — placeholder, would need thesis parsing

    # ── Buffett / Quality (0-12) ──────────────────────────────
    if roe and roe > 0.15:
        _add(s, "buffett", 2, f"ROE {roe*100:.0f}% > 15% (proxy ROIC alto)")
    if nde is not None and nde < 2:
        _add(s, "buffett", 1, f"ND/EBITDA {nde:.2f} < 2x")
    bn = qs.get("beneish", {}) if qs else {}
    if bn.get("zone") == "clean":
        _add(s, "buffett", 1, f"Beneish M={bn.get('m', 0):.2f} clean (sem manipulação)")
    if mos and mos > 0.20:
        _add(s, "buffett", 1, f"DCF MoS {mos*100:.0f}% > 20%")
    if streak >= 10:
        _add(s, "buffett", 1, f"Streak {int(streak)} anos ≥ 10 (consistência)")
    # Narrow moat default for industrials with long history
    if "Industrials" in sector and streak >= 10:
        _add(s, "buffett", 1, "Narrow moat (escala industrial + histórico)")

    # ── Primary / Secondary classification ────────────────────
    candidates: list[tuple[str, int]] = [
        ("Value", s.value),
        ("Growth", s.growth),
        ("Dividend/DRIP", s.dividend),
        ("Buffett/Quality", s.buffett),
    ]
    macro_combined = s.macro_exposure + s.macro_dependency
    if macro_combined >= 8:
        candidates.append(("Macro", macro_combined))

    candidates.sort(key=lambda x: -x[1])
    if candidates and candidates[0][1] >= 4:
        s.primary = f"{candidates[0][0]} ({candidates[0][1]}/12)"
    if len(candidates) >= 2 and candidates[1][1] >= 4 and (candidates[0][1] - candidates[1][1]) <= 2:
        s.secondary = f"{candidates[1][0]} ({candidates[1][1]}/12)"

    return s
