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

    RSS_FEEDS = [
        ("markets", "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"),
        ("tech", "https://feeds.a.dj.com/rss/RSSWSJD.xml"),
        ("world", "https://feeds.a.dj.com/rss/RSSWorldNews.xml"),
        ("business", "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml"),
        ("opinion", "https://feeds.a.dj.com/rss/RSSOpinion.xml"),
    ]

    # Default keywords para auto-filter; user pode override por CLI
    DEFAULT_KEYWORDS = [
        "Federal Reserve", "Treasury", "earnings", "Apple", "Microsoft",
        "Tesla", "Nvidia", "semiconductors", "OPEC", "dividend",
        "interest rates", "recession", "inflation",
    ]

    def __init__(self, session, storage_dir, keywords=None):
        super().__init__(session, storage_dir)
        self.keywords = keywords or self.DEFAULT_KEYWORDS

    def test_access(self) -> tuple[bool, str]:
        try:
            r = self.session.get("https://www.wsj.com/")
            html = r.text.lower()
            # WSJ mostra "sign in" quando logged out, "my wsj" ou username quando in
            signed_in = "my wsj" in html or "sign out" in html
            return (signed_in, f"wsj: {'✓ logged in' if signed_in else '✗ paywall active — refresh cookies'}")
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
                yield Report(
                    source=self.source, source_id=sid, url=link, title=title,
                    published_at=pub_iso, content_type="html", language="en",
                    tags=["us-equity", "wsj", f"section:{section}"],
                )

    def fetch_one(self, report: Report) -> Report:
        if not _HAS_BS4:
            raise RuntimeError("beautifulsoup4 required for wsj adapter")
        html = self.session.get_text(report.url)
        soup = BeautifulSoup(html, "html.parser")
        # WSJ: <section name="articleBody"> ou <article> com class articleBody
        body = (
            soup.find("section", attrs={"name": "articleBody"})
            or soup.find("article")
            or soup.find("main")
        )
        text = body.get_text(separator="\n", strip=True) if body else ""
        # detectar paywall (artigo truncado < 1000 chars sem sinais de completo)
        if len(text) < 1000 and "subscribe" in html.lower():
            report.tags.append("paywall_partial")
        local = self.storage_dir / f"{report.source_id}.html"
        local.write_text(html, encoding="utf-8")
        report.local_path = local
        report.raw_text = text[:50_000]
        return report
