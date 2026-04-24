"""XP Conteúdos adapter — conteudos.xpi.com.br research reports.

Strategy:
1. RSS feed primário (WordPress-style `/feed/`) para discovery leve.
2. Fallback: fetch listing pages por categoria.
3. Full article HTML com cookies autenticados (PRO content).
4. PDFs quando disponíveis (<a href=".pdf">).

Setup user:
- Login em conteudos.xpi.com.br (ou xpi.com.br → redireciona).
- Cookie-Editor → Export → `data/subscriptions/cookies/xp.json`.

Categorias alvo:
- /categoria/renda-variavel/
- /categoria/fundos-imobiliarios/
- /categoria/top-picks/
- /categoria/morning-call/

TOS: cliente XP only, uso pessoal.
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


class XPAdapter(BaseAdapter):
    source = "xp"
    base_url = "https://conteudos.xpi.com.br"
    rss_url = "https://conteudos.xpi.com.br/feed/"

    LISTING_PATHS = [
        "/categoria/renda-variavel/",
        "/categoria/fundos-imobiliarios/",
        "/categoria/morning-call/",
        "/categoria/top-picks/",
    ]

    def test_access(self) -> tuple[bool, str]:
        # NOTA (2026-04-24): conteudos.xpi.com.br bloqueia requests com WAF
        # "Acesso Bloqueado" (Imperva/Akamai). Mesmo com browser headers +
        # cookies válidas, retorna 403. **Requer Playwright** para bypass.
        try:
            r = self.session.get(self.rss_url, timeout=15)
            if r.status_code == 403 or "acesso bloqueado" in r.text.lower():
                return (False, "xp: ✗ WAF block (403) — requer Playwright upgrade")
            ok = r.status_code == 200 and ("<rss" in r.text or "<feed" in r.text)
            return (ok, f"xp rss: {'✓ ok' if ok else f'✗ status {r.status_code}'}")
        except Exception as e:
            return (False, f"xp test failed: {e}")

    def discover(self, since_days: int = 7) -> Iterator[Report]:
        cutoff = (datetime.now() - timedelta(days=since_days)).date()
        # Primeiro RSS (rápido, ~20 items últimos)
        try:
            yield from self._discover_rss(cutoff)
        except Exception as e:
            print(f"  [xp] rss failed: {e}")
        # Fallback: HTML listings (se BS4 disponível)
        if _HAS_BS4:
            for path in self.LISTING_PATHS:
                try:
                    yield from self._discover_listing(path, cutoff)
                except Exception as e:
                    print(f"  [xp] listing {path} failed: {e}")

    def _discover_rss(self, cutoff):
        import xml.etree.ElementTree as ET
        xml = self.session.get_text(self.rss_url)
        root = ET.fromstring(xml)
        # RSS 2.0 channel/item
        for item in root.iter("item"):
            link = item.findtext("link") or ""
            title = (item.findtext("title") or "")[:200]
            pub = item.findtext("pubDate") or ""
            try:
                pub_dt = datetime.strptime(pub[:25], "%a, %d %b %Y %H:%M:%S")
                pub_iso = pub_dt.date().isoformat()
                if pub_dt.date() < cutoff:
                    continue
            except ValueError:
                pub_iso = datetime.now().date().isoformat()
            sid = hashlib.sha1(link.encode()).hexdigest()[:16]
            yield Report(
                source=self.source,
                source_id=sid,
                url=link,
                title=title,
                published_at=pub_iso,
                content_type="rss_item",
                language="pt",
                tags=["br-equity", "xp"],
            )

    def _discover_listing(self, path: str, cutoff):
        html = self.session.get_text(self.base_url + path)
        soup = BeautifulSoup(html, "html.parser")
        for art in soup.find_all("article"):
            a = art.find("a", href=True)
            if not a:
                continue
            url = a["href"] if a["href"].startswith("http") else self.base_url + a["href"]
            title = (a.get_text(strip=True) or art.get_text(strip=True))[:200]
            sid = hashlib.sha1(url.encode()).hexdigest()[:16]
            # extrair data de <time datetime="...">
            t = art.find("time")
            pub_iso = datetime.now().date().isoformat()
            if t and t.get("datetime"):
                try:
                    pub_iso = t["datetime"][:10]
                except Exception:
                    pass
            yield Report(
                source=self.source, source_id=sid, url=url, title=title,
                published_at=pub_iso, content_type="html", language="pt",
                tags=["br-equity", "xp"],
            )

    def fetch_one(self, report: Report) -> Report:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required")
        html = self.session.get_text(report.url)
        soup = BeautifulSoup(html, "html.parser")
        # PDF link dentro do artigo?
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
                print(f"  [xp] PDF failed: {e}")
        # HTML article
        article = soup.find("article") or soup.find("main") or soup.body
        text = article.get_text(separator="\n", strip=True) if article else ""
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000]
        report.content_type = "html"
        return report
