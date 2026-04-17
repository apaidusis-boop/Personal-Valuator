"""Agregação de narrative_items em sector_sentiment (rolling).

Para cada (market, sector, subsector) e janela ∈ {7, 30, 90} dias:
    score      = sum(direction_i * magnitude_i * confidence_i) /
                 sum(magnitude_i * confidence_i)
    n_items    = nº de items na janela
    confidence = mean(confidence_i) * tanh(n_items / 10)
                 (atenuado quando há poucos items)
    top_theses_json = contagem de thesis_tag mais frequentes

Também produz rollup por sector (subsector='') além de cada subsector.

Decisão: sentiment do subsector pesa mais para empresas desse subsector;
o rollup do sector serve de fallback quando subsector tem n_obs baixo
(ver `effective_sentiment` em rules.py).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

WINDOWS_DAYS = (7, 30, 90)


@dataclass(frozen=True)
class SectorAggregate:
    as_of_date: str
    market: str
    sector: str
    subsector: str       # '' para rollup
    window_days: int
    score: float
    n_items: int
    confidence: float
    top_theses: dict[str, int]


def aggregate(db_path: Path, as_of_date: str | None = None) -> int:
    """Recalcula sector_sentiment para a data indicada (default: hoje).

    Idempotente — UPSERT na PK (as_of_date, market, sector, subsector,
    window_days).
    """
    raise NotImplementedError


def narrative_regime_bucket(score: float, confidence: float) -> str:
    """Mapeia score contínuo para bucket discreto usado em base_rates.

    Threshold conservador — um sentiment de -0.2 é apenas 'neg', não 'very_neg'.
    Com baixa confidence (<0.3) força 'neutral'.
    """
    if confidence < 0.3:
        return "neutral"
    if score <= -0.6:
        return "very_neg"
    if score <= -0.2:
        return "neg"
    if score >= 0.6:
        return "very_pos"
    if score >= 0.2:
        return "pos"
    return "neutral"
