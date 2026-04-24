"""Finclass adapter — app.finclass.com (SKELETON, deprioritized).

Finclass é SPA (React/Next) com API backend. Scraping via requests+cookies
**não funciona** directamente — precisa Playwright + network interception.

Strategy (não implementada neste skeleton):
1. Playwright com `localStorage` persisted (JWT bearer token).
2. Interceptar chamadas para `/api/courses/<id>/lessons/<id>` e similar.
3. Extrair video captions (se existe) → Whisper para transcrever.
4. Parse course notes PDFs se exportáveis.

**Priority: BAIXA**. Education platform, não investment intel direto.
Activar apenas se user pedir indexar curso específico.

Para activar:
1. `pip install playwright && playwright install chromium`
2. Implementar `PlaywrightSession` em `_session.py`.
3. Substituir `raise NotImplementedError` aqui pelo fluxo real.
"""
from __future__ import annotations

from typing import Iterator

from ._base import BaseAdapter, Report


class FinclassAdapter(BaseAdapter):
    source = "finclass"
    base_url = "https://app.finclass.com"

    def test_access(self) -> tuple[bool, str]:
        return (False, "finclass: SKELETON — requer Playwright (não implementado). Ver docstring.")

    def discover(self, since_days: int = 30) -> Iterator[Report]:
        raise NotImplementedError(
            "FinclassAdapter é skeleton. SPA requer Playwright + JWT interception. "
            "Ver docstring do módulo. Uso Suno / XP / WSJ em vez."
        )
        yield  # pragma: no cover (torna generator)

    def fetch_one(self, report: Report) -> Report:
        raise NotImplementedError
