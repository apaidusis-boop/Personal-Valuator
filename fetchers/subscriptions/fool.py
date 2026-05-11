"""Motley Fool adapter — fool.com.

Strategy:
1. RSS público para headlines + discovery (https://www.fool.com/a/feeds/foolwatch).
2. Login cookies para unlock Fool Premium / Stock Advisor / Rule Breakers articles.
3. Parse article HTML — Fool usa <article> com class .article-body.

Setup user:
- Login em fool.com.
- Cookie-Editor → `data/subscriptions/cookies/fool.json`.

Feeds RSS relevantes:
- https://www.fool.com/a/feeds/foolwatch                  (Stock Advisor watch)
- https://www.fool.com/feeds/foolwatch                     (free news)
- https://www.fool.com/investing-news/rss                  (investing news)

Priority: MÉDIA-ALTA (Stock Advisor = content premium caro, alto sinal).

TOS: uso pessoal. Não redistribuir.
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


class FoolAdapter(BaseAdapter):
    source = "fool"
    base_url = "https://www.fool.com"

    # Fool não tem RSS público. Scrape listing pages.
    LISTING_URLS = [
        "https://www.fool.com/investing-news/",
        "https://www.fool.com/investing/",
    ]
    # Artigos seguem padrão /investing/YYYY/MM/DD/<slug>/
    ARTICLE_RX = re.compile(r"/investing/(\d{4})/(\d{2})/(\d{2})/([^\"/]+)/?")

    # Default vazio — pegar tudo. User pode afinar passando `keywords=[...]`.
    DEFAULT_KEYWORDS: list[str] = []

    def __init__(self, session, storage_dir, keywords=None):
        super().__init__(session, storage_dir)
        self.keywords = keywords if keywords is not None else self.DEFAULT_KEYWORDS

    def test_access(self) -> tuple[bool, str]:
        # fool.com/my/ devolve 404 actualmente. Usar raiz + markers de UI.
        try:
            r = self.session.get("https://www.fool.com/", timeout=15)
            html = r.text.lower()
            # markers confirmados via probe (2026-04-24)
            has_ui = ("account" in html and "profile" in html)
            return (
                r.status_code == 200 and has_ui,
                f"fool: {'✓ access ok' if r.status_code == 200 and has_ui else f'✗ status {r.status_code}'}",
            )
        except Exception as e:
            return (False, f"fool test failed: {e}")

    def discover(self, since_days: int = 3) -> Iterator[Report]:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for fool adapter")
        cutoff = (datetime.now() - timedelta(days=since_days)).date()
        keywords_lc = [k.lower() for k in self.keywords] if self.keywords else []
        seen: set[str] = set()
        for listing_url in self.LISTING_URLS:
            try:
                html = self.session.get_text(listing_url)
            except Exception as e:
                print(f"  [fool] listing {listing_url} failed: {e}")
                continue
            soup = BeautifulSoup(html, "html.parser")
            for m in self.ARTICLE_RX.finditer(html):
                y, mo, d, slug = m.groups()
                url = f"{self.base_url}/investing/{y}/{mo}/{d}/{slug}/"
                if url in seen:
                    continue
                seen.add(url)
                try:
                    pub_date = datetime(int(y), int(mo), int(d)).date()
                    if pub_date < cutoff:
                        continue
                except ValueError:
                    continue
                # Titulo: procurar anchor que contém essa URL → usa seu texto
                a = soup.find("a", href=lambda h: h and slug in h)
                title = (a.get_text(strip=True) if a else slug.replace("-", " "))[:200]
                # keyword filter
                if keywords_lc and not any(k in title.lower() for k in keywords_lc):
                    continue
                sid = hashlib.sha1(url.encode()).hexdigest()[:16]
                yield Report(
                    source=self.source, source_id=sid, url=url, title=title,
                    published_at=pub_date.isoformat(),
                    content_type="html", language="en",
                    tags=["us-equity", "fool"],
                )

    def fetch_one(self, report: Report) -> Report:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for fool adapter")
        html = self.session.get_text(report.url)
        soup = BeautifulSoup(html, "html.parser")
        # Fool article body: .article-body é o container canónico (confirmado 2026-04-24)
        # `article` tag apanha primeiro sidebar cards, evitar.
        body = (
            soup.find("div", class_="article-body")
            or soup.find("div", class_="tailwind-article-body")
            or soup.find("main")
        )
        text = body.get_text(separator="\n", strip=True) if body else ""
        # Fool paywall indicator
        if "premium content" in html.lower() and len(text) < 800:
            report.tags.append("paywall_partial")
        # Tentar extrair title decente do h1 (o listing quase sempre devolve vazio
        # porque anchors de card são imagens sem texto).
        h1 = soup.find("h1")
        if h1:
            real_title = h1.get_text(strip=True)
            if real_title and (not report.title or len(report.title) < len(real_title)):
                report.title = real_title[:200]
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000]
        return report
