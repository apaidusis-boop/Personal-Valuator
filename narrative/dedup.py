"""Deduplicação de items de narrativa.

Problema: Reuters → Yahoo Finance → CNBC → MarketWatch replicam a mesma
manchete ("Fed holds rates steady"). Sem dedup, uma única história inflaciona
o sector_sentiment por contagem repetida.

Estratégia:
    1. Normalizar título (lowercase, sem pontuação, sem stopwords, tokens
       ordenados) para absorver variações superficiais.
    2. SHA1 dos primeiros 16 chars → dedup_group_id.
    3. Janela de 24h: items com mesmo hash e published_at dentro de 24h são
       agrupados. Fora da janela conta como nova notícia (um CPI novo).

Limitações assumidas:
    - Não apanha paráfrases ("Fed keeps rates unchanged" vs "Fed holds rates
      steady"). Para isso seria preciso embeddings + similaridade cosseno —
      está reservado como próximo passo (coluna embedding_blob já existe).
    - Stopwords são uma lista curta bilingue. Não é NLTK, intencionalmente.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta, timezone

# Stopwords curtas pt+en — artigo, conjunções, aux verbais, prep comuns.
# Intencionalmente enxuto; perder uma stopword cria falsos negativos mas não
# falsos positivos. Falsos positivos são o problema, não o inverso.
_STOPWORDS: frozenset[str] = frozenset({
    # en
    "a", "an", "the", "of", "to", "in", "on", "at", "for", "by", "from",
    "with", "and", "or", "but", "is", "are", "was", "were", "be", "been",
    "being", "has", "have", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "may", "might", "must", "as", "that", "this",
    "these", "those", "it", "its", "after", "before", "over", "under",
    # pt
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da",
    "dos", "das", "em", "no", "na", "nos", "nas", "para", "por", "com",
    "sem", "sob", "sobre", "entre", "que", "e", "ou", "mas", "é", "são",
    "foi", "foram", "ser", "está", "estão", "tem", "têm", "ter", "teve",
    "vai", "vão", "pode", "podem", "ao", "à", "aos", "às",
})

_WINDOW = timedelta(hours=24)

_TOKEN_RE = re.compile(r"[a-z0-9áéíóúâêîôûãõàèìòùäëïöüç]+", re.IGNORECASE)


def normalize(title: str) -> str:
    """lowercase + remove pontuação + remove stopwords + ordena tokens.

    Ordenação alfabética absorve ordem diferente de palavras-chave
    ("Fed holds rates steady" ≡ "rates steady: Fed holds").
    """
    tokens = _TOKEN_RE.findall(title.lower())
    keep = [t for t in tokens if t not in _STOPWORDS and len(t) > 1]
    keep.sort()
    return " ".join(keep)


def dedup_hash(title: str) -> str:
    """SHA1(normalize(title))[:16] — 16 hex chars = 64 bits, colisão
    desprezável para o volume em causa (6k/mês)."""
    normed = normalize(title)
    return hashlib.sha1(normed.encode("utf-8")).hexdigest()[:16]


def _parse_dt(s: str | datetime) -> datetime:
    if isinstance(s, datetime):
        return s if s.tzinfo else s.replace(tzinfo=timezone.utc)
    # Aceita ISO 8601 com ou sem Z
    s = s.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def same_group(
    title_a: str, published_a: str | datetime,
    title_b: str, published_b: str | datetime,
) -> bool:
    """True se os dois items devem ser agrupados como a mesma notícia."""
    if dedup_hash(title_a) != dedup_hash(title_b):
        return False
    da = _parse_dt(published_a)
    db = _parse_dt(published_b)
    return abs(da - db) < _WINDOW


def group_id(title: str, published_at: str | datetime) -> str:
    """ID estável para um item, incluindo bucket temporal.

    Forma: `{hash16}_{YYYYMMDD}`. A parte temporal garante que versões da
    mesma manchete em dias diferentes NÃO são agrupadas. Para bucketing por
    janela fina (24h deslizante) usar `same_group` directamente.
    """
    h = dedup_hash(title)
    dt = _parse_dt(published_at)
    return f"{h}_{dt.strftime('%Y%m%d')}"
