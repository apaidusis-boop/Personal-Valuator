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

    # URLs confirmadas via probe Playwright (2026-04-24).
    # Requer PlaywrightSession com headless=False — Imperva bloqueia headless.
    LISTING_PATHS = [
        "/acoes/",
        "/acoes/relatorios/",
        "/fundos-imobiliarios/",
        "/fundos-imobiliarios/relatorios/",
        "/renda-fixa/",
        "/economia/",
    ]

    # Artigos seguem padrão /<categoria>/relatorios/<slug>/ ou /<categoria>/<slug>/
    ARTICLE_RX = re.compile(
        r"https?://conteudos\.xpi\.com\.br/(acoes|fundos-imobiliarios|renda-fixa|economia|cripto|internacional)/(?:relatorios/)?[^\"/]+/?$"
    )

    def test_access(self) -> tuple[bool, str]:
        # Probe página de acoes — é onde estão os reports. WAF bloqueia /feed/.
        try:
            r = self.session.get(self.base_url + "/acoes/", timeout=30)
            if r.status_code == 403 or "acesso bloqueado" in r.text.lower():
                return (False, "xp: ✗ WAF block — precisa PlaywrightSession headless=False")
            ok = r.status_code == 200 and len(r.text) > 50_000
            return (ok, f"xp: {'✓ access ok (Playwright)' if ok else f'✗ status {r.status_code}'}")
        except Exception as e:
            return (False, f"xp test failed: {e}")

    def discover(self, since_days: int = 7) -> Iterator[Report]:
        # XP via Playwright não tem acesso fiável a RSS (/feed/ é filtrado).
        # Listing scraping via HTML rendered pages funciona.
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for xp adapter")
        cutoff = (datetime.now() - timedelta(days=since_days)).date()
        seen: set[str] = set()
        for path in self.LISTING_PATHS:
            try:
                yield from self._discover_listing(path, cutoff, seen)
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

    def _discover_listing(self, path: str, cutoff, seen: set):
        """Scrape listing via Playwright-rendered page + regex sobre anchors."""
        html = self.session.get_text(self.base_url + path, timeout=30)
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith("http"):
                href = self.base_url + href
            # filtra só artigos (não category/tag pages)
            if not self.ARTICLE_RX.match(href.rstrip("/") + "/"):
                continue
            if href in seen:
                continue
            seen.add(href)
            title = a.get_text(strip=True)[:200]
            if not title or len(title) < 10:
                continue
            # data via <time> adjacente ou parent article
            parent_art = a.find_parent("article") or a.find_parent("div")
            t = parent_art.find("time") if parent_art else None
            pub_iso = datetime.now().date().isoformat()
            if t and t.get("datetime"):
                try:
                    pub_iso = t["datetime"][:10]
                    pub_date = datetime.fromisoformat(pub_iso).date()
                    if pub_date < cutoff:
                        continue
                except ValueError:
                    pass
            sid = hashlib.sha1(href.encode()).hexdigest()[:16]
            yield Report(
                source=self.source, source_id=sid, url=href, title=title,
                published_at=pub_iso, content_type="html", language="pt",
                tags=["br-equity", "xp"],
            )

    def fetch_one(self, report: Report) -> Report:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required")
        html = self.session.get_text(report.url, timeout=30)
        soup = BeautifulSoup(html, "html.parser")

        # Prefer title real do h1 do artigo (listing text é ruidoso com
        # "23 Abr • 14 mins de leitura..." prefixos).
        h1 = soup.find("h1")
        if h1:
            real_title = h1.get_text(strip=True)
            if real_title and len(real_title) > 10:
                report.title = real_title[:200]

        # PDF link dentro do artigo?
        pdf_link = None
        for a in soup.find_all("a", href=True):
            if a["href"].lower().endswith(".pdf"):
                pdf_link = a["href"]
                break
        if pdf_link:
            pdf_url = pdf_link if pdf_link.startswith("http") else self.base_url + pdf_link
            # XP CDN exige Referer do artigo (Imperva WAF). Playwright via
            # page-context shares cookies+referer; passar explicit headers.
            try:
                pdf_bytes = self.session.get_bytes(
                    pdf_url,
                    extra_headers={"Referer": report.url, "Accept": "application/pdf,*/*;q=0.9"},
                )
                local = self.storage_dir / f"{report.source_id}.pdf"
                local.write_bytes(pdf_bytes)
                report.raw_bytes = pdf_bytes
                report.local_path = local
                report.content_type = "pdf"
                # guardar HTML também (tem title + summary)
                article = soup.find("article") or soup.find("main")
                if article:
                    report.raw_text = article.get_text(separator="\n", strip=True)[:50_000]
                return report
            except Exception as e:
                print(f"  [xp] PDF failed: {e}")

        # HTML article
        article = (
            soup.find("article")
            or soup.find("div", class_="post-content")
            or soup.find("main")
            or soup.body
        )
        text = article.get_text(separator="\n", strip=True) if article else ""
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000]
        report.content_type = "html"
        return report
