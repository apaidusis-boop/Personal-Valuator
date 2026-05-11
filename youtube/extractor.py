"""Extractor LLM local (Ollama + Qwen2.5-32B-Instruct, JSON mode).

Recebe as windows do router por ticker/tema e devolve `ExtractorOutput`
validado por pydantic. Se o parse falhar ou o modelo devolver 0 factos
onde claramente havia match, tenta fallback para o 14B.

Design anti-alucinação:
  1. System prompt insiste em `evidence_quote` como substring literal.
  2. Pydantic valida comprimento/tipos/ranges.
  3. `validator.py` confirma substring antes de persistir.
  4. Confidence gate (≥0.5) aplicado em `validator.py`.

Temperature=0.1 (determinístico mas não zero — ajuda com JSON tricky).
"""
from __future__ import annotations

import json
import logging

import ollama
from pydantic import ValidationError

from youtube.models import ExtractorOutput, InsightKind

log = logging.getLogger(__name__)

# 2026-05-08: swapped 32B↔14B priority. 14B é ~3× mais rápido e produz JSON
# valido em 95%+ dos casos para o nosso schema. 32B fica como fallback para
# transcripts difíceis (CIO interviews longos, jargão técnico denso).
# Empirical: 5min episódio 14B = ~30s; 32B = ~2-3min. Para 38 vídeos
# backlog, swap reduz ~2h GPU work.
PRIMARY_MODEL = "qwen2.5:14b-instruct-q4_K_M"
FALLBACK_MODEL = "qwen2.5:32b-instruct-q4_K_M"

ALLOWED_KINDS = [
    "guidance", "capex", "dividend", "balance_sheet",
    "thesis_bull", "thesis_bear", "catalyst", "risk",
    "operational", "management", "valuation",
]


SYSTEM_PROMPT = """És um analista financeiro. Lês excertos de um vídeo (PT ou EN)
e extrais factos estruturados sobre UMA empresa específica — o TICKER ALVO.

Devolves **apenas JSON válido** com este schema exacto:
{
  "insights": [
    {
      "ticker": "<TICKER_ALVO>",
      "kind": "<uma de: guidance|capex|dividend|balance_sheet|thesis_bull|thesis_bear|catalyst|risk|operational|management|valuation>",
      "claim": "<afirmação em 1-2 frases, em português>",
      "evidence_quote": "<trecho VERBATIM do transcript, ≤400 chars>",
      "ts_seconds": <inteiro ou null>,
      "confidence": <float 0.0-1.0>
    }
  ],
  "themes": []
}

REGRAS OBRIGATÓRIAS — LER COM ATENÇÃO:
1. **SUJEITO do facto**: cada insight tem de descrever o TICKER ALVO **como sujeito principal**. Se o texto apenas menciona o TICKER ALVO de passagem (ex: "a B3 recebeu os documentos da Copasa" — o facto é sobre Copasa, não sobre B3), **NÃO extrair**. Devolver array vazio.
2. **Teste de substituição**: para cada insight, pergunta "este facto deixa de fazer sentido se eu remover o TICKER ALVO da história?". Se NÃO deixa de fazer sentido (o facto era de outra empresa), **rejeitar**.
3. **BROKERS/ANALISTAS como sujeito proibido**: se o TICKER ALVO é um banco/broker (ex: Goldman Sachs, JP Morgan, BB Investimentos, Bradesco BBI, XP Inc, Itaú BBA) e o texto diz "<broker> recomenda/cobre/tem price-target para <outra empresa>", o facto é sobre a OUTRA EMPRESA, **não sobre o broker**. Nesse caso **devolver array vazio** para o TICKER ALVO. Exemplos de rejeição:
   - TICKER_ALVO=GS, texto="Goldman Sachs recomenda Klabin com preço-alvo R$18" → REJEITAR (facto é sobre Klabin).
   - TICKER_ALVO=BBAS3, texto="BB Investimentos, ou seja, o Banco do Brasil, manteve recomendação de compra para a Klabin" → REJEITAR (facto é sobre Klabin).
   - TICKER_ALVO=JPM, texto="JP Morgan elevou preço-alvo da Petrobras" → REJEITAR (facto é sobre Petrobras).
   Só aceitar factos sobre o broker se forem sobre o **próprio broker** (ex: "Goldman Sachs reportou lucro trimestral de X", "JP Morgan teve redução de dividendo").
4. `evidence_quote` TEM de ser uma substring LITERAL do transcript. **NÃO parafrasear, NÃO resumir, NÃO corrigir gramática**. Copiar caracteres exactos, incluindo disfluências ("é é é", "tipo assim", etc.).
5. Se o trecho VERBATIM passar os 400 caracteres, escolher a parte nuclear do facto — nunca inventar conteúdo para "completar".
6. Confidence: >0.7 para número/declaração explícita da empresa; 0.5-0.7 para inferência razoável; <0.5 para opinião sem suporte numérico.
7. Se não houver facto confiável onde o TICKER ALVO é sujeito, devolver {"insights": [], "themes": []}.
8. Máximo 5 insights por request. Preferir poucos factos sólidos a muitos fracos.
9. Para este request, `themes` é sempre [].
"""

THEME_SYSTEM_PROMPT = """És um analista macro. Lês excertos de um vídeo sobre
um tema macro/sector específico e extrais factos estruturados.

Devolves **apenas JSON válido** com este schema exacto:
{
  "insights": [],
  "themes": [
    {
      "theme": "<TEMA_DADO>",
      "stance": "<bullish|bearish|neutral>",
      "summary": "<resumo em 1-2 frases, em português>",
      "evidence_quote": "<trecho VERBATIM do transcript, ≤300 chars>",
      "ts_seconds": <inteiro ou null>,
      "confidence": <float 0.0-1.0>
    }
  ]
}

REGRAS OBRIGATÓRIAS:
1. `evidence_quote` TEM de ser uma substring LITERAL do transcript. Copiar verbatim.
2. Se não houver facto claro sobre o tema, devolver {"insights": [], "themes": []}.
3. Máximo 3 themes por request.
4. Para este request, `insights` é sempre [].
"""


def _call_ollama(system: str, user: str, model: str) -> dict:
    resp = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        format="json",
        options={"temperature": 0.1, "num_ctx": 8192},
    )
    content = resp["message"]["content"]
    return json.loads(content)


MAX_QUOTE_CHARS = 400
MAX_CLAIM_CHARS = 500


def _sanitize_raw(raw: dict) -> dict:
    """Trunca quotes/claims muito longos *antes* de pydantic validar +
    filtra items com estrutura malformada.

    O LLM às vezes excede limites OU inventa schema (ex: devolve strings
    em vez de dicts, ou campos com nomes diferentes). Filtramos defensivamente
    para que o parse pydantic só veja items potencialmente válidos.
    """
    if not isinstance(raw, dict):
        return {"insights": [], "themes": []}
    for key in ("insights", "themes"):
        arr = raw.get(key)
        if not isinstance(arr, list):
            raw[key] = []
            continue
        clean: list[dict] = []
        for item in arr:
            if not isinstance(item, dict):
                continue
            q = item.get("evidence_quote")
            if isinstance(q, str) and len(q) > MAX_QUOTE_CHARS:
                item["evidence_quote"] = q[:MAX_QUOTE_CHARS].rstrip()
            c = item.get("claim") if key == "insights" else item.get("summary")
            if isinstance(c, str) and len(c) > MAX_CLAIM_CHARS:
                field = "claim" if key == "insights" else "summary"
                item[field] = c[:MAX_CLAIM_CHARS].rstrip()
            clean.append(item)
        raw[key] = clean
    return raw


def _try_parse(raw: dict) -> ExtractorOutput | None:
    raw = _sanitize_raw(raw)
    try:
        return ExtractorOutput.model_validate(raw)
    except ValidationError as e:
        log.warning("extractor_parse_fail err=%s raw=%s", e, str(raw)[:500])
        return None


def extract_for_ticker(
    ticker: str,
    windows_text: str,
    model: str = PRIMARY_MODEL,
    fallback_model: str = FALLBACK_MODEL,
) -> ExtractorOutput:
    """Extrai insights para UM ticker a partir das suas windows concatenadas."""
    user = (
        f"TICKER ALVO: {ticker}\n\n"
        f"KINDS PERMITIDOS: {', '.join(ALLOWED_KINDS)}\n\n"
        f"TRANSCRIPT (excertos relevantes):\n{windows_text}\n\n"
        "Devolve o JSON com insights sobre este ticker (ou array vazio)."
    )

    try:
        raw = _call_ollama(SYSTEM_PROMPT, user, model)
    except Exception as e:  # noqa: BLE001
        log.error("ollama_error ticker=%s model=%s err=%s", ticker, model, e)
        return ExtractorOutput()

    parsed = _try_parse(raw)
    if parsed is None and model != fallback_model:
        log.info("extractor_retry_fallback ticker=%s", ticker)
        try:
            raw = _call_ollama(SYSTEM_PROMPT, user, fallback_model)
            parsed = _try_parse(raw)
        except Exception as e:  # noqa: BLE001
            log.error("fallback_error ticker=%s err=%s", ticker, e)

    if parsed is None:
        return ExtractorOutput()

    # Força todos os insights ao ticker pedido (o LLM às vezes re-mapeia)
    for ins in parsed.insights:
        ins.ticker = ticker
    return parsed


def extract_for_theme(
    theme: str,
    windows_text: str,
    model: str = PRIMARY_MODEL,
    fallback_model: str = FALLBACK_MODEL,
) -> ExtractorOutput:
    user = (
        f"TEMA ALVO: {theme}\n\n"
        f"TRANSCRIPT (excertos relevantes):\n{windows_text}\n\n"
        "Devolve o JSON com themes sobre este tema (ou array vazio)."
    )
    try:
        raw = _call_ollama(THEME_SYSTEM_PROMPT, user, model)
    except Exception as e:  # noqa: BLE001
        log.error("ollama_error theme=%s err=%s", theme, e)
        return ExtractorOutput()
    parsed = _try_parse(raw)
    if parsed is None and model != fallback_model:
        try:
            raw = _call_ollama(THEME_SYSTEM_PROMPT, user, fallback_model)
            parsed = _try_parse(raw)
        except Exception as e:  # noqa: BLE001
            log.error("fallback_theme_error theme=%s err=%s", theme, e)
    if parsed is None:
        return ExtractorOutput()
    for th in parsed.themes:
        th.theme = theme  # force
    return parsed
