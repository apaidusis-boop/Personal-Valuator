"""Base rates históricas: retorno forward por (sector, regime macro, regime narrativa).

Pergunta que responde:
    "Historicamente, quando o sector Banks BR esteve com narrative_regime='very_neg'
     em macro {rate=hold, growth=slowdown}, qual foi o retorno mediano nos
     próximos 12m? Em quantos episódios?"

Procedimento:
    1. Para cada dia D em [start, today - horizon]:
       a. Para cada (market, sector, subsector):
          - regime macro de D (macro_regime)
          - sentiment de D, janela 30d (sector_sentiment)
          - bucket narrative via aggregator.narrative_regime_bucket
          - retorno forward do sector (média ponderada por market cap dos
            tickers do sector na carteira/watchlist)  ⚠ aproximação inicial:
            equal-weighted sobre tickers em universe.yaml
       b. Insere observação numa tabela temporária
    2. GROUP BY (market, sector, subsector, rate_regime, growth_regime,
                narrative_regime, forward_horizon)
       → median, p25, p75, n_obs
    3. UPSERT em sector_base_rates

Filtros de confiança:
    - n_obs < 5  →  não inserir (insuficiente)
    - BR: lookback >= 2010-01-01
    - US: lookback >= 2000-01-01

Limitação assumida:
    Sentiment histórico só existe a partir do dia em que começamos a scrapear.
    Ou seja, a primeira versão das base rates terá apenas alguns meses de obs
    para 'very_neg'/'very_pos' (raros). Aceitar — base rates ganham massa
    com o tempo. Para bootstrap, podemos aproximar sentiment histórico via
    proxy: drawdown >X% do sector vs IBOV/SP500 ⇒ assumir 'neg' nesse período.
    Implementar proxy em `bootstrap_historical_sentiment`.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

FORWARD_HORIZONS = ("3m", "6m", "12m")
MIN_OBS = 5

LOOKBACK_START = {
    "br": "2010-01-01",
    "us": "2000-01-01",
}


@dataclass(frozen=True)
class BaseRate:
    market: str
    sector: str
    subsector: str
    rate_regime: str
    growth_regime: str
    narrative_regime: str
    forward_horizon: str
    median_return: float
    p25_return: float
    p75_return: float
    n_obs: int


def compute(db_path: Path, market: str) -> int:
    """Recomputa todas as base rates para o mercado indicado.

    Idempotente. UPSERT em sector_base_rates. Devolve nº de combinações
    inseridas/actualizadas.
    """
    raise NotImplementedError


def bootstrap_historical_sentiment(db_path: Path, market: str) -> int:
    """Proxy para sentiment pré-scraper: drawdown do sector como sinal negativo.

    Apenas para preencher histórico antes do go-live do scraper. Usa
    sector_sentiment com source flag 'proxy' em extra_json. Conservador:
    só marca 'neg'/'very_neg', nunca positivo (não há proxy razoável).
    """
    raise NotImplementedError


def lookup(
    db_path: Path,
    market: str,
    sector: str,
    rate_regime: str,
    growth_regime: str,
    narrative_regime: str,
    horizon: str = "12m",
    subsector: str = "",
) -> BaseRate | None:
    """Consulta a base rate. Fallback: se subsector tem n_obs<MIN_OBS,
    cai para subsector='' (rollup do sector)."""
    raise NotImplementedError
