"""SessionManager — cookie-based HTTP session per subscription source.

Lê cookies exportados de `data/subscriptions/cookies/<source>.json`
(formato Cookie-Editor standard) e constrói um `requests.Session` auto-pronto
para falar com o site.

Playwright é upgrade opcional (classe `PlaywrightSession` stub — ativar só
quando requests+cookies bate em Cloudflare).

Format esperado do `<source>.json` (Cookie-Editor export):
    [
      {
        "domain": ".suno.com.br",
        "name": "__suno_session",
        "value": "...",
        "path": "/",
        "secure": true,
        "httpOnly": true,
        "sameSite": "Lax"
      },
      ...
    ]
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import requests

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


class SessionManager:
    """Wraps a requests.Session com cookies importados do browser."""

    def __init__(self, source: str, cookies_dir: Path, rate_limit_sec: float = 3.0):
        self.source = source
        self.cookies_path = cookies_dir / f"{source}.json"
        self.rate_limit_sec = rate_limit_sec
        self._last_request_at: float = 0.0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": DEFAULT_UA,
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        self._load_cookies()

    def _load_cookies(self) -> None:
        if not self.cookies_path.exists():
            raise FileNotFoundError(
                f"Cookies missing for {self.source}. "
                f"Export via Cookie-Editor → {self.cookies_path}"
            )
        cookies = json.loads(self.cookies_path.read_text(encoding="utf-8"))
        for c in cookies:
            # Cookie-Editor format → requests cookie
            self.session.cookies.set(
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", "").lstrip("."),
                path=c.get("path", "/"),
            )

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_at
        if elapsed < self.rate_limit_sec:
            time.sleep(self.rate_limit_sec - elapsed)
        self._last_request_at = time.time()

    def get(self, url: str, **kwargs) -> requests.Response:
        self._rate_limit()
        r = self.session.get(url, timeout=kwargs.pop("timeout", 30), **kwargs)
        return r

    def get_bytes(self, url: str, **kwargs) -> bytes:
        r = self.get(url, **kwargs)
        r.raise_for_status()
        return r.content

    def get_text(self, url: str, **kwargs) -> str:
        r = self.get(url, **kwargs)
        r.raise_for_status()
        r.encoding = r.encoding or "utf-8"
        return r.text

    def is_logged_in(self, probe_url: str, indicator: str) -> bool:
        """Checa se sessão autenticada fazendo GET + procurando `indicator` no HTML.
        `indicator` é string que só aparece quando logged in (ex: 'Logout', username).
        """
        try:
            html = self.get_text(probe_url)
            return indicator.lower() in html.lower()
        except Exception:
            return False


class PlaywrightSession:
    """Stub — upgrade path quando requests+cookies bate em Cloudflare challenge.

    Impl pendente: usar `playwright-python` com persistent context em
    `~/.config/ii-playwright-profile/<source>/`. Login manual 1×, depois
    scripts reusam.

    Install: `pip install playwright && playwright install chromium`
    """

    def __init__(self, source: str):
        raise NotImplementedError(
            "PlaywrightSession not yet implemented. "
            "For now use SessionManager with exported cookies."
        )
