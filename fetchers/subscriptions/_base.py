"""BaseAdapter — contrato comum para todos os subscription adapters.

Cada site (WSJ, Suno, XP, Finclass) implementa `discover()` + `fetch_one()`
retornando objectos `Report`. O orchestrator persiste em `analyst_reports`.

Design:
- Adapter é **stateless** salvo cookies/session.
- Não fala com DB directamente — devolve `Report` + raw bytes.
- Ollama extract é feito por `_pdf_extract.py` ou `_text_extract.py` num passo
  separado (idempotente, re-runnable).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


@dataclass
class Report:
    """Um documento (artigo ou PDF) descoberto/fetched de um site."""
    source: str                  # 'suno' | 'xp' | 'wsj' | 'finclass'
    source_id: str               # site-specific stable ID (slug, url hash)
    url: str
    title: str
    published_at: str            # ISO YYYY-MM-DD
    content_type: str            # 'html' | 'pdf' | 'rss_item'
    author: str | None = None
    language: str = "pt"
    tags: list[str] = field(default_factory=list)
    # Payload
    raw_bytes: bytes | None = None        # PDF binário ou HTML se fetched
    raw_text: str | None = None            # texto extraído (se disponível)
    local_path: Path | None = None         # path se já gravado em disco


@dataclass
class AdapterResult:
    """Resultado agregado de uma run."""
    source: str
    discovered: int = 0
    fetched: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)


class BaseAdapter(ABC):
    """Contrato para subscription adapters."""
    source: str = ""  # override em subclasses
    base_url: str = ""

    def __init__(self, session, storage_dir: Path):
        self.session = session           # SessionManager instance
        self.storage_dir = storage_dir   # data/subscriptions/<source>/
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def discover(self, since_days: int = 7) -> Iterator[Report]:
        """Itera reports disponíveis nos últimos `since_days`.

        Devolve Report com metadados (title, url, published_at) mas **sem**
        raw_bytes ainda — é lightweight para permitir filter/dedup antes de
        fetch pesado.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_one(self, report: Report) -> Report:
        """Faz download do conteúdo full (PDF bytes ou HTML body).

        Popula `report.raw_bytes` / `report.raw_text` e `report.local_path`.
        """
        raise NotImplementedError

    def test_access(self) -> tuple[bool, str]:
        """Verifica que cookies estão válidos. Override se precisar.
        Devolve (ok, message).
        """
        return (True, f"{self.source}: no test implemented — assuming ok")
