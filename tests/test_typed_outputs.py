"""W.6.2 — offline tests para outputs typed (Pydantic) via Ollama local.

Cobertura: contrato `agents._llm.ollama_call_typed[T]` para os 3 schemas
introduzidos em W.6.1 (synthetic_ic, thesis_synthesizer, holding_wiki_synthesizer).

100% offline: chama Ollama em localhost:11434 com qwen2.5:14b. Skipa graciosamente
se Ollama não estiver up. Zero Claude tokens.

Run:
    pytest tests/ -v
    pytest tests/test_typed_outputs.py::test_persona_verdict_buffett_ko -v
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents._llm import ollama_call_typed  # noqa: E402
from agents._schemas import HoldingWikiStub, PersonaVerdict, ThesisDraft  # noqa: E402


OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"


def _ollama_up() -> bool:
    try:
        r = requests.get(OLLAMA_TAGS_URL, timeout=2)
        return r.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _ollama_up(),
    reason="Ollama not reachable at localhost:11434 — required for W.6.2",
)


# ──────────────────────────────────────────────────────────────────────
# PersonaVerdict — synthetic_ic.py output
# ──────────────────────────────────────────────────────────────────────

PERSONA_PROMPT_KO = """Você é Warren Buffett. Avalia Coca-Cola (KO) brevemente:
- P/E 24, Dividend Yield 3.0%, ROE 45%
- 60+ anos de dividendos crescentes (Aristocrat)
- Brand moat dominante, pricing power, free cash flow alta e estável
- Trading $58, net debt manejável

Devolve APENAS JSON válido nesta forma exacta:
{
  "verdict": "BUY",
  "conviction": 9,
  "rationale": ["razão 1", "razão 2", "razão 3"],
  "key_risk": "1 frase curta",
  "would_size": "large"
}

Constraints:
- verdict: exactamente "BUY", "HOLD" ou "AVOID"
- conviction: integer 1-10
- would_size: exactamente "small", "medium", "large" ou "none"
- rationale: lista de 2-4 strings
"""


def test_persona_verdict_schema_valid():
    """Buffett-vs-KO: schema parses, fields no domínio, conviction in range."""
    out = ollama_call_typed(
        PERSONA_PROMPT_KO, PersonaVerdict,
        seed=42, temperature=0.0, max_tokens=400,
    )
    assert out is not None, "ollama_call_typed returned None — JSON parse or schema validation failed"
    assert out.verdict in {"BUY", "HOLD", "AVOID"}, f"verdict out of domain: {out.verdict!r}"
    assert 1 <= out.conviction <= 10, f"conviction out of range: {out.conviction}"
    assert out.would_size in {"small", "medium", "large", "none"}, f"would_size out of domain: {out.would_size!r}"
    assert isinstance(out.rationale, list)


def test_persona_verdict_buffett_likes_ko():
    """Sanity check: KO + Buffett framework should not produce AVOID."""
    out = ollama_call_typed(
        PERSONA_PROMPT_KO, PersonaVerdict,
        seed=42, temperature=0.0, max_tokens=400,
    )
    assert out is not None
    assert out.verdict != "AVOID", (
        f"Buffett framework on KO with great fundamentals returned AVOID — "
        f"likely model or prompt regression. Got: {out.model_dump()}"
    )


def test_persona_verdict_seed_reproducible():
    """Same seed + temp=0 should give identical verdict (Ollama determinism)."""
    a = ollama_call_typed(
        PERSONA_PROMPT_KO, PersonaVerdict,
        seed=42, temperature=0.0, max_tokens=400,
    )
    b = ollama_call_typed(
        PERSONA_PROMPT_KO, PersonaVerdict,
        seed=42, temperature=0.0, max_tokens=400,
    )
    assert a is not None and b is not None
    assert a.verdict == b.verdict, (
        f"Same seed gave different verdicts: {a.verdict} vs {b.verdict}"
    )


# ──────────────────────────────────────────────────────────────────────
# ThesisDraft — thesis_synthesizer.py output
# ──────────────────────────────────────────────────────────────────────

THESIS_PROMPT_ITSA4 = """Escreve thesis de investimento curta para Itausa (ITSA4):
- Holding company brasileira, controla Itaú Unibanco + Alpargatas + Dexco
- DY ~6%, ROE ~12%, P/E ~8 (bancos BR ajuste)
- Long-horizon DRIP investor PT-BR, filosofia Buffett-Graham

Devolve APENAS JSON válido nesta forma exacta:
{
  "core_thesis": "1 parágrafo curto sobre porquê investir",
  "key_assumptions": ["assumption 1", "assumption 2", "assumption 3"],
  "disconfirmation_triggers": ["trigger que invalida 1", "trigger 2"],
  "intent": "DRIP"
}
"""


def test_thesis_draft_schema_valid():
    out = ollama_call_typed(
        THESIS_PROMPT_ITSA4, ThesisDraft,
        seed=42, temperature=0.0, max_tokens=600,
    )
    assert out is not None, "thesis ollama_call_typed returned None"
    assert out.core_thesis.strip(), "core_thesis is empty"
    assert len(out.key_assumptions) >= 1, f"key_assumptions empty: {out.key_assumptions}"
    assert len(out.disconfirmation_triggers) >= 1, f"triggers empty: {out.disconfirmation_triggers}"
    assert out.intent.strip(), "intent is empty"


def test_thesis_draft_assumptions_are_strings():
    out = ollama_call_typed(
        THESIS_PROMPT_ITSA4, ThesisDraft,
        seed=42, temperature=0.0, max_tokens=600,
    )
    assert out is not None
    for a in out.key_assumptions:
        assert isinstance(a, str) and a.strip(), f"non-string or empty assumption: {a!r}"
    for t in out.disconfirmation_triggers:
        assert isinstance(t, str) and t.strip(), f"non-string or empty trigger: {t!r}"


# ──────────────────────────────────────────────────────────────────────
# HoldingWikiStub — holding_wiki_synthesizer.py output
# ──────────────────────────────────────────────────────────────────────

WIKI_PROMPT_ACN = """Escreve nota wiki holding para Accenture (ACN):
- Consulting + IT services líder global
- ~735K colaboradores, presença 49 países
- Operating margin ~15%, ROE ~30%
- Dividend streak >10 anos (candidato Aristocrat)
- Switching cost moderado-alto + scale advantage

Devolve APENAS JSON válido nesta forma exacta:
{
  "intent_one_liner": "1 frase sobre intent na carteira",
  "business_snapshot": "1 parágrafo sobre o negócio",
  "why_we_hold": ["razão 1", "razão 2", "razão 3"],
  "moat": "1 parágrafo sobre o moat",
  "current_state": "1 parágrafo sobre estado actual",
  "invalidation_triggers": ["trigger 1", "trigger 2"],
  "sizing_drip_intent": "1 frase sobre sizing/DRIP"
}
"""


def test_holding_wiki_stub_schema_valid():
    out = ollama_call_typed(
        WIKI_PROMPT_ACN, HoldingWikiStub,
        seed=42, temperature=0.0, max_tokens=900,
    )
    assert out is not None, "wiki ollama_call_typed returned None"
    assert out.intent_one_liner.strip(), "intent_one_liner empty"
    assert out.business_snapshot.strip(), "business_snapshot empty"
    assert len(out.why_we_hold) >= 1, f"why_we_hold empty: {out.why_we_hold}"
    assert len(out.invalidation_triggers) >= 1, f"invalidation_triggers empty"
    assert out.sizing_drip_intent.strip(), "sizing_drip_intent empty"


def test_holding_wiki_stub_lists_are_strings():
    out = ollama_call_typed(
        WIKI_PROMPT_ACN, HoldingWikiStub,
        seed=42, temperature=0.0, max_tokens=900,
    )
    assert out is not None
    for r in out.why_we_hold:
        assert isinstance(r, str) and r.strip()
    for t in out.invalidation_triggers:
        assert isinstance(t, str) and t.strip()
