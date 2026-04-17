"""Classificação de items de narrativa via LLM.

Input:  narrative_items WHERE classified_at IS NULL
Output: actualiza sector, subsector, direction, magnitude, thesis_tag,
        thesis_action, confidence, classified_at.

Um único item bruto pode produzir múltiplas linhas classificadas — ex: vídeo
do Nigro de 30min fala de Banks BR, Tech US, Selic, e dólar. A função
`classify_item` devolve uma lista de `Classification`, e o caller insere
uma linha por sector mencionado (mantendo o item bruto original como pai
via narrative_items.id replicado em extra_json).

Taxonomia de tese (decide se a narrativa negativa é oportunidade ou armadilha):

    Tese                 thesis_action     Significado
    -------------------  ----------------  -------------------------------------
    macro                contrarian_ok     Selic, juros, recessão geral, pânico
    panic                contrarian_ok     "vende tudo", manchete sensacionalista
    rotation             contrarian_ok     Saída de capital do sector por moda
    earnings_miss        neutral           Resultado fraco, mas público
    guidance_cut         neutral           Mas releva — fundamentals próximos
    credit_quality       pause             Deterioração da carteira (banco)
    governance           pause             Conselho, CEO, conflito de interesse
    fraud                pause             Suspeita de manipulação contábil
    regulatory           pause             Multa, mudança de regra, intervenção
    accounting           pause             Restatement, auditoria qualificada

Action 'contrarian_ok' = se fundamentals OK + preço caiu, é candidato a reforço.
Action 'pause'         = ignorar fundamentals trimestrais, esperar mais info.
Action 'neutral'       = sem leitura clara, contar para sentiment mas sem regra.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ThesisTag = Literal[
    "macro", "panic", "rotation",
    "earnings_miss", "guidance_cut",
    "credit_quality", "governance", "fraud", "regulatory", "accounting",
]
ThesisAction = Literal["contrarian_ok", "pause", "neutral"]

THESIS_ACTION: dict[str, ThesisAction] = {
    "macro":          "contrarian_ok",
    "panic":          "contrarian_ok",
    "rotation":       "contrarian_ok",
    "earnings_miss":  "neutral",
    "guidance_cut":   "neutral",
    "credit_quality": "pause",
    "governance":     "pause",
    "fraud":          "pause",
    "regulatory":     "pause",
    "accounting":     "pause",
}


@dataclass(frozen=True)
class Classification:
    sector: str
    subsector: str | None
    market: str           # 'br' | 'us' | 'global'
    direction: float      # [-1, +1]
    magnitude: int        # 1..3
    thesis_tag: ThesisTag
    confidence: float     # [0, 1]


def classify_item(raw_title: str, raw_text: str, lang: str) -> list[Classification]:
    """Chama LLM (Claude via anthropic SDK) com prompt estruturado.

    Prompt deve forçar JSON: lista de objects, cada um com os campos do dataclass.
    Um vídeo longo pode produzir 5+ classifications; uma manchete curta produz 1.
    """
    raise NotImplementedError


def classify_pending(db_path: Path, batch_size: int = 50) -> int:
    """Processa items com classified_at IS NULL. Devolve nº processados."""
    raise NotImplementedError
