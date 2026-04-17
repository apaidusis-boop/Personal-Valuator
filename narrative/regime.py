"""Classificação do regime macro (4 dimensões independentes).

Consome `series` já populada por fetchers/bcb_fetcher.py (BR) e equivalente US
(a definir — FRED via fredapi). NÃO chama rede.

Dimensões:
    rate_regime    : 'tightening' | 'easing' | 'hold'
                     BR: derivada de SELIC_META (delta 90d)
                     US: derivada de Fed Funds (FRED:FEDFUNDS, delta 90d)
    growth_regime  : 'expansion' | 'slowdown' | 'recession' | 'recovery'
                     BR: IBC-Br YoY + IPCA + desemprego (composite)
                     US: GDP growth + unemployment + ISM PMI
    fx_regime      : 'strong_local' | 'weak_local' | 'neutral'
                     BR: USDBRL_PTAX vs média móvel 200d (banda ±5%)
                     US: DXY vs MM200d
    risk_regime    : 'risk_on' | 'risk_off' | 'neutral'
                     Global: VIX (<15 risk-on, >25 risk-off) +
                             credit spread HY-IG +
                             curva 2y-10y

Regras são heurísticas conservadoras — preferir 'hold'/'neutral' quando
sinal ambíguo. Histórico inteiro é recomputado de cada vez (idempotente,
permite refinar regras sem migration).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

RateRegime = Literal["tightening", "easing", "hold"]
GrowthRegime = Literal["expansion", "slowdown", "recession", "recovery"]
FxRegime = Literal["strong_local", "weak_local", "neutral"]
RiskRegime = Literal["risk_on", "risk_off", "neutral"]


@dataclass(frozen=True)
class MacroRegime:
    date: str
    market: str          # 'br' | 'us'
    rate: RateRegime
    growth: GrowthRegime
    fx: FxRegime
    risk: RiskRegime
    details: dict        # valores numéricos brutos que justificam a classificação


def classify_br(db_path: Path, since: str | None = None) -> int:
    """Recomputa macro_regime para market='br'. Idempotente.

    Restrição: BR limitar lookback a 2010-01-01 para evitar quebras
    estruturais (era de Selic 14%→2%→13% em 5 anos distorce base rates).
    """
    raise NotImplementedError


def classify_us(db_path: Path, since: str | None = None) -> int:
    """Recomputa macro_regime para market='us'. Idempotente."""
    raise NotImplementedError


def current(db_path: Path, market: str) -> MacroRegime | None:
    """Devolve o regime mais recente para o mercado indicado."""
    raise NotImplementedError
