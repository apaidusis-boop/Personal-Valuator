"""Validação anti-alucinação, fuzzy evidence e filtro anti cross-contamination.

Regras por insight (ordem de aplicação):
  1. `evidence_quote` presente no transcript. Primeiro match exacto com
     whitespace-norm + lowercase; fallback para match após normalização
     agressiva (accent strip + punct strip); último recurso fuzzy substring
     com overlap ≥ FUZZY_OVERLAP.
  2. Evidence não pode mencionar outro ticker/empresa do universe *sem*
     também mencionar o ticker alvo → cross-contamination (ex: insight
     marcado B3SA3 com evidence a falar só de "Copasa" → reject).
  3. Confidence >= threshold (default 0.5).
  4. Dedup por (video_id, ticker, kind, claim_norm).

Themes: regras 1,3,4 aplicam (cross-contamination não se aplica — theme é
sobre macro, não empresa).
"""
from __future__ import annotations

import logging
import re
import unicodedata

from youtube.models import ExtractorOutput, Insight, Theme

log = logging.getLogger(__name__)

DEFAULT_CONFIDENCE_THRESHOLD = 0.5
FUZZY_OVERLAP = 0.85      # 85% dos tokens do quote têm de aparecer em ordem
_WHITESPACE = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]")


def _normalize_ws(s: str) -> str:
    return _WHITESPACE.sub(" ", s).strip()


def _strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def _norm_aggressive(s: str) -> str:
    """Lowercase + strip accents + strip punct + collapse whitespace."""
    s = _strip_accents(s).lower()
    s = _PUNCT.sub(" ", s)
    return _normalize_ws(s)


def _longest_consecutive_overlap_ratio(needle: str, haystack: str) -> float:
    """Proporção dos tokens do needle que aparecem em ordem consecutiva no haystack.

    Usado como último recurso quando substring directo falha (paraphrasing
    leve). Janela deslizante sobre haystack em tamanho = len(needle_tokens).
    """
    n_toks = needle.split()
    h_toks = haystack.split()
    if not n_toks:
        return 0.0
    window = len(n_toks)
    if window > len(h_toks):
        return 0.0
    best = 0
    for start in range(len(h_toks) - window + 1):
        chunk = h_toks[start : start + window]
        matches = sum(1 for a, b in zip(n_toks, chunk) if a == b)
        if matches > best:
            best = matches
    return best / window


def _quote_in_transcript(quote: str, transcript_norm_ws: str, transcript_norm_agg: str) -> bool:
    """3-tier: exact → accent-strip → fuzzy overlap ≥85%."""
    q_ws = _normalize_ws(quote).lower()
    if q_ws in transcript_norm_ws:
        return True
    q_agg = _norm_aggressive(quote)
    if q_agg in transcript_norm_agg:
        return True
    ratio = _longest_consecutive_overlap_ratio(q_agg, transcript_norm_agg)
    return ratio >= FUZZY_OVERLAP


def normalize_claim(s: str) -> str:
    """Lowercase + strip acentos + strip pontuação para dedup."""
    return _norm_aggressive(s)


def _build_other_ticker_patterns(
    target_ticker: str,
    aliases: dict,
) -> tuple[re.Pattern | None, re.Pattern | None]:
    """(pattern para alias do target, pattern para aliases de outros tickers)."""
    ticker_defs = aliases.get("tickers", {}) or {}
    target_names: list[str] = []
    other_names: list[str] = []
    for tk, entry in ticker_defs.items():
        names = entry.get("names", []) or []
        products = entry.get("products", []) or []
        if tk == target_ticker:
            target_names.extend(names)
        else:
            # Só nomes de empresa, não produtos/people — demasiado genérico
            other_names.extend(names)
    target_pat = None
    if target_names:
        target_pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in target_names if n) + r")\b", re.IGNORECASE)
    other_pat = None
    if other_names:
        other_pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in other_names if n) + r")\b", re.IGNORECASE)
    return target_pat, other_pat


def _is_cross_contaminated(
    evidence: str,
    claim: str,
    target_pat: re.Pattern | None,
    other_pat: re.Pattern | None,
) -> bool:
    """Três falhas de sanidade:
    (A) evidence menciona outra empresa E NÃO menciona o alvo em claim+evidence;
    (B) claim menciona outra empresa E NÃO menciona o alvo no claim — LLM
        atribuiu um claim de Y ao ticker X só porque o alvo apareceu numa
        janela de contexto vizinha. (ex: claim sobre Klabin atribuído a BBAS3
        porque "Banco do Brasil" foi citado como broker.)
    (C) evidence não menciona o alvo E claim não menciona o alvo — pura
        pronome/elipse, sem âncora verbatim em lado nenhum.
    """
    if target_pat is None:
        return False  # sem aliases conhecidos, não há como verificar

    target_in_evidence = bool(target_pat.search(evidence))
    target_in_claim = bool(target_pat.search(claim))

    # (A) menção literal a outra empresa no evidence sem alvo em lado nenhum
    if other_pat is not None and other_pat.search(evidence):
        if not target_in_evidence and not target_in_claim:
            return True

    # (B) claim fala de outra empresa e o alvo não está no claim → subject confusion
    if other_pat is not None and other_pat.search(claim):
        if not target_in_claim:
            return True

    # (C) alvo ausente em ambos → sem âncora
    if not target_in_evidence and not target_in_claim:
        return True

    return False


def validate(
    out: ExtractorOutput,
    full_transcript: str,
    aliases: dict | None = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> tuple[list[Insight], list[Theme], dict]:
    """Filtra insights/themes que passam validação. Devolve também stats."""
    stats = {
        "insights_in": len(out.insights),
        "themes_in": len(out.themes),
        "dropped_evidence": 0,
        "dropped_cross_contamination": 0,
        "dropped_confidence": 0,
        "dropped_dedup": 0,
    }

    transcript_norm_ws = _normalize_ws(full_transcript).lower()
    transcript_norm_agg = _norm_aggressive(full_transcript)

    # Cross-contamination patterns por ticker alvo (cached)
    patterns_cache: dict[str, tuple[re.Pattern | None, re.Pattern | None]] = {}

    def get_patterns(ticker: str):
        if aliases is None:
            return None, None
        if ticker not in patterns_cache:
            patterns_cache[ticker] = _build_other_ticker_patterns(ticker, aliases)
        return patterns_cache[ticker]

    kept_insights: list[Insight] = []
    seen_insights: set[tuple[str, str, str]] = set()
    for ins in out.insights:
        if not _quote_in_transcript(ins.evidence_quote, transcript_norm_ws, transcript_norm_agg):
            stats["dropped_evidence"] += 1
            log.debug("drop_evidence ticker=%s quote=%s", ins.ticker, ins.evidence_quote[:80])
            continue
        target_pat, other_pat = get_patterns(ins.ticker)
        if _is_cross_contaminated(ins.evidence_quote, ins.claim, target_pat, other_pat):
            stats["dropped_cross_contamination"] += 1
            log.info("drop_cross_contam ticker=%s claim=%s", ins.ticker, ins.claim[:80])
            continue
        if ins.confidence < confidence_threshold:
            stats["dropped_confidence"] += 1
            continue
        key = (ins.ticker, ins.kind, normalize_claim(ins.claim))
        if key in seen_insights:
            stats["dropped_dedup"] += 1
            continue
        seen_insights.add(key)
        kept_insights.append(ins)

    kept_themes: list[Theme] = []
    seen_themes: set[tuple[str, str]] = set()
    for th in out.themes:
        if not _quote_in_transcript(th.evidence_quote, transcript_norm_ws, transcript_norm_agg):
            stats["dropped_evidence"] += 1
            continue
        if th.confidence < confidence_threshold:
            stats["dropped_confidence"] += 1
            continue
        key2 = (th.theme, normalize_claim(th.summary))
        if key2 in seen_themes:
            stats["dropped_dedup"] += 1
            continue
        seen_themes.add(key2)
        kept_themes.append(th)

    stats["insights_out"] = len(kept_insights)
    stats["themes_out"] = len(kept_themes)
    return kept_insights, kept_themes, stats
