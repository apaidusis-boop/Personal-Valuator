"""Hedge Engine — tactical defensive overlays for risk-off regimes.

Filosofia: este sistema é Buy & Hold + DRIP. Hedging activo contradiz a
filosofia. PORÉM, em janelas tácticas (regime=recession ou late_cycle com
sinal forte de drawdown), uma alocação pequena (5-10%) a instrumentos
defensivos amortece a volatilidade sem trair o core.

Este engine:
  - NÃO emite signal por ticker individual da carteira
  - Emite um HedgeProposal quando o regime + sinais técnicos justificam
  - Output structured como rationale; portfolio engine decide se aplica

Triggers (config/hedge_triggers.yaml — ver seguir abaixo se precisar override):
  recession (US ou BR)              → hedge_size = 10% notional
  late_cycle + curve inverted ≥ 6m  → hedge_size = 5% notional
  expansion + late_cycle (default)  → hedge_size = 0%
  recovery                          → hedge_size = 0% (de-hedge)

Instruments suggested (não comprados automaticamente):
  US:
    - SH (ProShares Short S&P 500) — beta hedge passivo, sem decay puts
    - SQQQ (3x inverse Nasdaq) — só em curtas janelas; high decay
    - SPY 30-delta puts 90-day — tail risk hedge, premium 1-2%
  BR:
    - BOVA11 short via empréstimo (BTC) — beta hedge; custo carry
    - SMAL11 short — small cap hedge
    - USDBRL futures long — proxy stress hedge (BRL fraqueja em risk-off)
  Cross-asset:
    - GLD / IAU — uncorrelated tail hedge (medium-term)
    - TLT — duration; bom em deflação, mau em stagflation

A "evaluate(ticker)" devolve um HOLD genérico — o ticker não é avaliado
individualmente. Para obter o hedge tactical use propose_hedge(market).
"""
from __future__ import annotations

import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from analytics.regime import classify
from strategies._base import StrategyOutput

ROOT = Path(__file__).resolve().parents[1]

name = "hedge"

DEFAULT_TRIGGERS = {
    "us": {
        "recession": {"hedge_size_pct": 0.10, "instruments": ["SH", "SPY_PUT_30D"]},
        "late_cycle": {"hedge_size_pct": 0.05, "instruments": ["SH"]},
        "expansion": {"hedge_size_pct": 0.0, "instruments": []},
        "recovery": {"hedge_size_pct": 0.0, "instruments": []},
        "unknown": {"hedge_size_pct": 0.02, "instruments": ["SH"]},
    },
    "br": {
        "recession": {"hedge_size_pct": 0.10, "instruments": ["USDBRL_LONG", "BOVA11_SHORT"]},
        "late_cycle": {"hedge_size_pct": 0.05, "instruments": ["USDBRL_LONG"]},
        "expansion": {"hedge_size_pct": 0.0, "instruments": []},
        "recovery": {"hedge_size_pct": 0.0, "instruments": []},
        "unknown": {"hedge_size_pct": 0.02, "instruments": ["USDBRL_LONG"]},
    },
    "cross": ["GLD", "TLT"],
}


@lru_cache(maxsize=1)
def _triggers() -> dict:
    p = ROOT / "config" / "hedge_triggers.yaml"
    if p.exists():
        cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return cfg or DEFAULT_TRIGGERS
    return DEFAULT_TRIGGERS


def propose_hedge(market: str = "us",
                  portfolio_value: float | None = None) -> dict[str, Any]:
    """Compute a tactical hedge proposal for the current regime.

    Args:
        market: 'us' or 'br'
        portfolio_value: optional, used to materialise notional sizes
    Returns dict with: regime, hedge_size_pct, instruments, notional,
    rationale, confidence.
    """
    market = market.lower()
    r = classify(market)
    cfg = _triggers().get(market, {})
    bucket = cfg.get(r.regime) or cfg.get("unknown") or {"hedge_size_pct": 0.0, "instruments": []}
    proposal = {
        "market": market,
        "regime": r.regime,
        "confidence": r.confidence,
        "hedge_size_pct": bucket["hedge_size_pct"],
        "instruments": list(bucket["instruments"]),
        "notional": (portfolio_value * bucket["hedge_size_pct"])
                     if portfolio_value is not None else None,
        "rationale": r.notes,
        "cross_asset_alternatives": _triggers().get("cross", []),
        "active": bucket["hedge_size_pct"] > 0,
    }
    return proposal


def evaluate(ticker: str, market: str = "us") -> StrategyOutput:
    """Per-ticker: this engine does NOT individually rank tickers.
    Returns a HOLD with the current hedge proposal in rationale."""
    proposal = propose_hedge(market)
    if proposal["active"]:
        # When the hedge is active, every long position has implicit
        # "AVOID more exposure" recommendation; weight_suggestion stays
        # 0 because hedge is at the portfolio level, not per-ticker.
        verdict = "HOLD"
        score = 0.5
        msg = (f"Tactical hedge active: {proposal['hedge_size_pct']:.0%} of NAV via "
               f"{', '.join(proposal['instruments'])}")
    else:
        verdict = "HOLD"
        score = 1.0
        msg = "No tactical hedge active in current regime"
    return StrategyOutput(
        ticker=ticker, market=market, engine=name,
        score=score, verdict=verdict, weight_suggestion=0.0,
        rationale=proposal, message=msg,
    )


def rank_universe(market: str = "us",
                  tickers: list[str] | None = None) -> list[StrategyOutput]:
    """Hedge engine doesn't rank individuals — returns empty list."""
    return []


def status(market: str = "us") -> str:
    """Quick CLI summary."""
    p = propose_hedge(market)
    if not p["active"]:
        return f"HEDGE OFF | {market.upper()} regime={p['regime']} (confidence={p['confidence']})"
    return (f"HEDGE ON | {market.upper()} regime={p['regime']} "
            f"size={p['hedge_size_pct']:.0%} via {', '.join(p['instruments'])}")
