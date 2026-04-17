"""Scraper YouTube — narrativa de canais selecionados.

Trade-off: alto sinal mas alto custo (transcript + LLM por vídeo). Usar com
parcimónia. Canais-alvo definidos em config/narrative_sources.yaml.

Estratégia:
    1. Listar vídeos novos do canal (RSS do YouTube: per channel feed)
    2. yt-dlp --write-auto-sub --skip-download para captar transcript
    3. Inserir em narrative_items com source='youtube:<channel_handle>',
       raw_text = transcript completo, classified_at = NULL.
    4. Classificação por classifier.py (LLM extrai múltiplas opiniões por
       vídeo: um vídeo do Nigro pode falar de 5 sectores diferentes).

Importante:
    - 1 vídeo pode gerar N entradas em narrative_items pós-classificação
      (uma por sector mencionado). O scraper insere 1; o classifier replica.
    - Respeitar ToS do YouTube. yt-dlp + transcripts públicos apenas.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class YouTubeChannel:
    handle: str          # ex: '@thiagonigro'
    channel_id: str      # UC...
    market_focus: str    # 'br' | 'us' | 'global'
    lang: str


def list_recent_videos(channel: YouTubeChannel, since: str | None = None) -> list[dict]:
    """Devolve metadados de vídeos novos (id, title, published_at)."""
    raise NotImplementedError


def fetch_transcript(video_id: str) -> str | None:
    """yt-dlp --write-auto-sub. Devolve transcript ou None se indisponível."""
    raise NotImplementedError


def persist(items: list[dict], db_path: Path) -> int:
    """Idempotente por (source, source_url=youtube_url)."""
    raise NotImplementedError


def run(db_path: Path, config_path: Path) -> None:
    raise NotImplementedError
