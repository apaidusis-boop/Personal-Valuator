"""Scraper RSS — fonte primária de narrativa.

Feeds-alvo (a definir em config/narrative_sources.yaml — ainda não criado):
    BR:  InfoMoney, Valor Econômico, Brazil Journal, Money Times, Suno
    US:  Reuters Business, Bloomberg Markets, WSJ Markets, Seeking Alpha,
         Yahoo Finance

Saída: insere em `narrative_items` com source='rss:<canal>', classified_at=NULL.
A classificação por sector/tese é feita posteriormente por classifier.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RssFeed:
    name: str            # ex: 'infomoney'
    url: str
    market: str          # 'br' | 'us' | 'global'
    lang: str            # 'pt' | 'en'


def load_feeds(config_path: Path) -> list[RssFeed]:
    """Lê config/narrative_sources.yaml. TODO: definir formato."""
    raise NotImplementedError


def fetch_feed(feed: RssFeed, since: str | None = None) -> list[dict]:
    """Faz parse do RSS e devolve items novos desde `since` (ISO date).

    Cada dict contém: source, source_url, published_at, raw_title, raw_text,
    lang, market. Sem classificação (campos sector/direction etc ficam None).
    """
    raise NotImplementedError


def persist(items: list[dict], db_path: Path) -> int:
    """Insere em narrative_items. Devolve nº de novos. Idempotente por
    (source, source_url)."""
    raise NotImplementedError


def run(db_path: Path, config_path: Path) -> None:
    """Entry-point: lê config, varre todos os feeds, persiste novos items."""
    raise NotImplementedError
