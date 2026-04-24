"""WSJ adapter — wsj.com (Wall Street Journal).

Strategy:
1. RSS público para discovery (headlines + URLs) — NÃO precisa login.
   https://feeds.a.dj.com/rss/RSSMarketsMain.xml
   https://feeds.a.dj.com/rss/RSSWSJD.xml  (tech)
   https://feeds.a.dj.com/rss/RSSWorldNews.xml
2. Filter por keyword/ticker (user preferences).
3. Fetch full article HTML com cookies autenticados (senão: paywall).
4. Parse article body (WSJ usa <article id="articleBody"> ou similar).

Setup user:
- Login em wsj.com.
- Cookie-Editor → `data/subscriptions/cookies/wsj.json`.
- IMPORTANTE: WSJ tem bot detection — respeitar rate limit ≥ 3s entre requests.

TOS: WSJ proíbe explicitamente scraping. Uso pessoal (não-redistribuição,
não-automação mass) geralmente tolerado mas não garantido. Baixo volume.
"""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Iterator

try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

from ._base import BaseAdapter, Report


class WSJAdapter(BaseAdapter):
    source = "wsj"
    base_url = "https://www.wsj.com"

    # NOTA (2026-04-24): feeds.a.dj.com/rss/* devolve items de 2025-01 (stale!).
    # O feed actual que funciona é MarketWatch (Dow Jones sibling, freemium):
    # feeds.content.dowjones.io/public/rss/mw_topstories retorna items do próprio dia.
    # WSJ puro (pay-walled) não tem RSS fresh público — requer Playwright para
    # discover. Este adapter usa MarketWatch como proxy + fetch de WSJ article
    # individual via cookies para content premium.
    RSS_FEEDS = [
        ("mw_topstories", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
        ("mw_marketpulse", "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"),
        ("mw_bulletins", "https://feeds.content.dowjones.io/public/rss/mw_bulletins"),
    ]

    # Default vazio — WSJ RSS é high-volume, user afina keywords se quiser.
    # Para já, aceitar tudo; filtro pode ir em extract stage.
    DEFAULT_KEYWORDS: list[str] = []

    def __init__(self, session, storage_dir, keywords=None):
        super().__init__(session, storage_dir)
        self.keywords = keywords if keywords is not None else self.DEFAULT_KEYWORDS

    def test_access(self) -> tuple[bool, str]:
        # Markers confirmados via probe (2026-04-24): "logout", "customer center"
        try:
            r = self.session.get("https://www.wsj.com/", timeout=20)
            if r.status_code != 200:
                return (False, f"wsj: ✗ status {r.status_code}")
            html = r.text.lower()
            signed_in = "logout" in html or "customer center" in html
            return (signed_in, f"wsj: {'✓ logged in' if signed_in else '✗ not logged in — refresh cookies'}")
        except Exception as e:
            return (False, f"wsj test: {e}")

    def discover(self, since_days: int = 3) -> Iterator[Report]:
        cutoff = (datetime.now() - timedelta(days=since_days)).date()
        keywords_lc = [k.lower() for k in self.keywords]
        for section, feed_url in self.RSS_FEEDS:
            try:
                xml = self.session.get_text(feed_url)
                root = ET.fromstring(xml)
            except Exception as e:
                print(f"  [wsj] rss {section} failed: {e}")
                continue
            for item in root.iter("item"):
                link = item.findtext("link") or ""
                title = (item.findtext("title") or "")[:200]
                desc = (item.findtext("description") or "")[:500]
                pub = item.findtext("pubDate") or ""
                try:
                    pub_dt = datetime.strptime(pub[:25], "%a, %d %b %Y %H:%M:%S")
                    pub_iso = pub_dt.date().isoformat()
                    if pub_dt.date() < cutoff:
                        continue
                except ValueError:
                    pub_iso = datetime.now().date().isoformat()
                # keyword filter
                hay = (title + " " + desc).lower()
                if keywords_lc and not any(k in hay for k in keywords_lc):
                    continue
                sid = hashlib.sha1(link.encode()).hexdigest()[:16]
                # Guardar description do RSS como raw_text — fallback se o
                # artigo estiver behind paywall MarketWatch (cookies WSJ não
                # autenticam em marketwatch.com).
                clean_desc = re.sub(r"<[^>]+>", " ", desc).strip() if desc else ""
                yield Report(
                    source=self.source, source_id=sid, url=link, title=title,
                    published_at=pub_iso, content_type="html", language="en",
                    raw_text=clean_desc[:5000] if clean_desc else None,
                    tags=["us-equity", "wsj", f"section:{section}"],
                )

    def fetch_one(self, report: Report) -> Report:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for wsj adapter")
        rss_desc = report.raw_text  # preserva fallback já set em discover
        try:
            html = self.session.get_text(report.url)
        except Exception as e:
            # MarketWatch articles retornam 401 com WSJ cookies — usar RSS desc
            report.tags.append("paywall_cross_domain")
            if not rss_desc:
                report.raw_text = f"(fetch failed: {e})"
            return report
        soup = BeautifulSoup(html, "html.parser")
        # WSJ: <section name="articleBody"> / MarketWatch: <div class="article__body">
        body = (
            soup.find("section", attrs={"name": "articleBody"})
            or soup.find("div", class_="article__body")
            or soup.find("article")
            or soup.find("main")
        )
        text = body.get_text(separator="\n", strip=True) if body else ""
        # Se não encontrou corpo decente, fica com RSS description.
        if len(text) < 500 and rss_desc:
            text = rss_desc
            report.tags.append("rss_description_only")
        if "subscribe to continue" in html.lower() and len(text) < 1000:
            report.tags.append("paywall_partial")
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000] if text else rss_desc
        return report
