"""Suno adapter — suno.com.br research reports.

Strategy:
1. Fetch listing pages (relatórios) → parse HTML para cards.
2. Para cada card: extrair URL do PDF (usualmente via link /download/ ou similar).
3. Download PDF binário → guardar em storage_dir.

Setup user:
- Login em suno.com.br.
- Cookie-Editor → Export → guardar em `data/subscriptions/cookies/suno.json`.
- `ii subs test --source suno` para validar acesso.

URLs típicas (ajustar se mudarem):
- Lista: https://www.suno.com.br/relatorios/
- Artigo: https://www.suno.com.br/artigos/<slug>/
- PDF: variável — procurar <a href="...pdf"> dentro do artigo.

TOS: uso pessoal. Não redistribuir.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

from ._base import BaseAdapter, Report


class SunoAdapter(BaseAdapter):
    source = "suno"
    base_url = "https://www.suno.com.br"
    probe_url = "https://www.suno.com.br/conta/"
    login_indicator = "sair"  # "Sair" link aparece quando logged

    LISTING_PATHS = [
        "/relatorios/",
        "/materiais/",
    ]

    def test_access(self) -> tuple[bool, str]:
        ok = self.session.is_logged_in(self.probe_url, self.login_indicator)
        return (ok, f"suno login: {'✓ ok' if ok else '✗ not logged in — refresh cookies'}")

    def discover(self, since_days: int = 7) -> Iterator[Report]:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for suno adapter")
        cutoff = (datetime.now() - timedelta(days=since_days)).date()
        seen: set[str] = set()
        for path in self.LISTING_PATHS:
            try:
                html = self.session.get_text(self.base_url + path)
            except Exception as e:
                print(f"  [suno] failed listing {path}: {e}")
                continue
            soup = BeautifulSoup(html, "html.parser")
            # Suno usa cards com classe variable — catch-all: links para /artigos/
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/artigos/" not in href and "/relatorios/" not in href:
                    continue
                url = href if href.startswith("http") else self.base_url + href
                sid = hashlib.sha1(url.encode()).hexdigest()[:16]
                if sid in seen:
                    continue
                seen.add(sid)
                title = (a.get_text(strip=True) or "")[:200]
                if not title or len(title) < 10:
                    continue
                # data de publicação: Suno embebe em <time> ou no próprio slug /YYYY-MM-DD/
                pub = self._extract_date_from_url(url) or datetime.now().date().isoformat()
                try:
                    pub_date = datetime.fromisoformat(pub).date()
                    if pub_date < cutoff:
                        continue
                except ValueError:
                    pass
                yield Report(
                    source=self.source,
                    source_id=sid,
                    url=url,
                    title=title,
                    published_at=pub,
                    content_type="html",  # será upgraded para pdf se encontrarmos link
                    language="pt",
                    tags=["br-equity"],
                )

    @staticmethod
    def _extract_date_from_url(url: str) -> str | None:
        m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        return None

    def fetch_one(self, report: Report) -> Report:
        """Fetch article HTML e tenta encontrar PDF link dentro. Se encontra, baixa PDF."""
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required")
        html = self.session.get_text(report.url)
        soup = BeautifulSoup(html, "html.parser")
        # 1. procurar PDF link
        pdf_link = None
        for a in soup.find_all("a", href=True):
            if a["href"].lower().endswith(".pdf"):
                pdf_link = a["href"]
                break
        if pdf_link:
            pdf_url = pdf_link if pdf_link.startswith("http") else self.base_url + pdf_link
            try:
                pdf_bytes = self.session.get_bytes(pdf_url)
                local = self.storage_dir / f"{report.source_id}.pdf"
                local.write_bytes(pdf_bytes)
                report.raw_bytes = pdf_bytes
                report.local_path = local
                report.content_type = "pdf"
                return report
            except Exception as e:
                print(f"  [suno] PDF download failed for {report.source_id}: {e}")
        # 2. fallback: guardar HTML do artigo
        article = soup.find("article") or soup.find("main")
        text = article.get_text(separator="\n", strip=True) if article else ""
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000]
        return report
