"""Matriz de decisão final — combina fundamentals × sentiment × regime macro.

NÃO é um score multiplicado. É uma matriz explícita que devolve uma `Action`
e uma justificação textual auditável.

Ordem de avaliação (early-exit):
    1. fundamentals_passes_screen?  Não → Action=AVOID (independente do resto)
    2. thesis_action == 'pause'?    Sim → Action=HOLD_REVIEW (esperar info nova)
    3. matriz (sentiment_bucket × macro_regime) → Action

Exemplo concreto (caso ABCB-style discutido em conversa):
    Banks BR, ITUB4 holding:
      - fundamentals_passes_screen = True (P/B<1.5, DY>6%, ROE>12%, streak>5y)
      - sector_sentiment 30d = -0.7 (very_neg)
      - thesis dominante = 'macro' → thesis_action = 'contrarian_ok'
      - macro_regime BR = {rate=easing, growth=recovery, fx=neutral, risk=neutral}
      - base_rate lookup: median +18% em 12m (n=11)
    → Action = REINFORCE com nota: "narrativa de pânico macro num sector com
       fundamentals OK e regime macro favorável; base rate histórica positiva".

Mesmo caso mas com thesis = 'credit_quality':
    → Action = HOLD_REVIEW, nota: "deterioração de carteira citada — aguardar
       próximo release de PDD antes de reforçar".
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Action = Literal[
    "REINFORCE",      # comprar/aumentar posição
    "ENTER",          # iniciar posição (watchlist)
    "HOLD",           # manter, sem acção
    "HOLD_REVIEW",    # manter, mas reavaliar com info nova (thesis 'pause')
    "TRIM",           # reduzir posição
    "AVOID",          # não tocar (fundamentals reprovam)
]


@dataclass(frozen=True)
class Decision:
    ticker: str
    sector: str
    subsector: str
    action: Action
    confidence: float        # [0, 1]
    rationale: str           # texto auditável
    inputs: dict             # snapshot dos sinais que produziram a decisão


def decide(
    db_path: Path,
    ticker: str,
    as_of_date: str | None = None,
) -> Decision:
    """Avalia um ticker. Lê:
        - fundamentals + scores (fundamentals_passes_screen)
        - sector_sentiment do sector/subsector do ticker
        - macro_regime do mercado do ticker
        - sector_base_rates para contextualizar

    Devolve uma `Decision` com rationale legível. Não escreve em DB —
    callers (relatórios, daily_update) decidem o que fazer com o output.
    """
    raise NotImplementedError


def decide_universe(db_path: Path, market: str) -> list[Decision]:
    """Avalia todos os tickers (holdings + watchlist) do mercado."""
    raise NotImplementedError
