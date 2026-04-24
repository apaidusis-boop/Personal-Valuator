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
        # Browser-like header set. Alguns sites (WSJ, XP) rejeitam requests
        # sem Sec-Fetch-* headers (Cloudflare/Akamai bot detection).
        self.session.headers.update({
            "User-Agent": DEFAULT_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            # `br` (brotli) requer `pip install brotli`; manter sem para robustez
            "Accept-Encoding": "gzip, deflate",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
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

    def get_bytes(self, url: str, extra_headers: dict | None = None, **kwargs) -> bytes:
        if extra_headers:
            kwargs.setdefault("headers", {}).update(extra_headers)
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


class _PWResponse:
    """requests.Response-compatible shim para resultados Playwright."""
    def __init__(self, text: str, status_code: int, url: str):
        self.text = text
        self.status_code = status_code
        self.url = url
        self.content = text.encode("utf-8", errors="replace")

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise RuntimeError(f"HTTP {self.status_code} @ {self.url}")


class PlaywrightSession:
    """Browser-real session para sites que bloqueiam requests (WAF, SPA, JWT).

    Usa `playwright.sync_api` com persistent context em
    `<project>/.playwright-profiles/<source>/`. Cookies Cookie-Editor são
    importadas na primeira run; subsequentes usam o storage persistente do
    Chromium.

    Interface compatível com `SessionManager` (get/get_text/get_bytes/is_logged_in)
    para os adapters não precisarem saber qual está por baixo.

    Install prerequisites:
        pip install playwright
        python -m playwright install chromium
    """

    def __init__(
        self,
        source: str,
        cookies_dir: Path,
        *,
        headless: bool = True,
        rate_limit_sec: float = 2.0,
    ):
        self.source = source
        self.cookies_path = cookies_dir / f"{source}.json"
        self.rate_limit_sec = rate_limit_sec
        self._last_request_at: float = 0.0
        self.headless = headless
        # persistent profile — Chromium guarda cookies+storage entre runs
        from pathlib import Path as _P
        root = _P(__file__).resolve().parents[2]
        self.profile_dir = root / ".playwright-profiles" / source
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._pw = None
        self._ctx = None
        self._page = None
        self._cookies_imported_file = self.profile_dir / ".cookies_imported"

    def _ensure_started(self) -> None:
        if self._ctx is not None:
            return
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:
            raise RuntimeError(
                "playwright não instalado. `pip install playwright && "
                "python -m playwright install chromium`"
            ) from e
        self._pw = sync_playwright().start()
        self._ctx = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=self.headless,
            user_agent=DEFAULT_UA,
            viewport={"width": 1440, "height": 900},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            # args para evitar bot detection comum
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        )
        self._page = self._ctx.new_page()
        # Import cookies 1× (depois persistent context guarda-as)
        if not self._cookies_imported_file.exists() and self.cookies_path.exists():
            self._import_cookies()
            self._cookies_imported_file.touch()
        # Restore session_state.json backup se existir — recovery path para
        # SPAs onde Chromium profile não fluiu localStorage correctamente.
        state_backup = self.profile_dir / "session_state.json"
        restore_marker = self.profile_dir / ".state_restored"
        if state_backup.exists() and not restore_marker.exists():
            try:
                self._restore_state(state_backup)
                restore_marker.touch()
                print(f"[pw:{self.source}] session_state.json restored from backup")
            except Exception as e:
                print(f"[pw:{self.source}] state restore failed: {e}")

    def _restore_state(self, state_path: "Path") -> None:
        """Re-injecta cookies + localStorage de um storage_state.json dump."""
        import json as _json
        state = _json.loads(state_path.read_text(encoding="utf-8"))
        # Cookies
        if state.get("cookies"):
            try:
                self._ctx.add_cookies(state["cookies"])
            except Exception as e:
                print(f"  cookie restore partial: {e}")
        # localStorage — requer navegar ao origin primeiro
        for origin_entry in state.get("origins", []):
            origin = origin_entry.get("origin")
            if not origin:
                continue
            try:
                self._page.goto(origin, wait_until="commit", timeout=15000)
                for item in origin_entry.get("localStorage", []):
                    k, v = item["name"], item["value"]
                    self._page.evaluate(
                        f"() => localStorage.setItem({k!r}, {v!r})"
                    )
            except Exception as e:
                print(f"  localStorage restore for {origin} failed: {e}")

    def _import_cookies(self) -> None:
        """Lê Cookie-Editor JSON e injecta no contexto Playwright."""
        import json as _json
        raw = _json.loads(self.cookies_path.read_text(encoding="utf-8"))
        pw_cookies = []
        for c in raw:
            ck = {
                "name": c["name"],
                "value": c["value"],
                "domain": c.get("domain", ""),
                "path": c.get("path", "/"),
                "secure": bool(c.get("secure", False)),
                "httpOnly": bool(c.get("httpOnly", False)),
            }
            if "expirationDate" in c and not c.get("session"):
                ck["expires"] = c["expirationDate"]
            ss = c.get("sameSite", "").lower()
            if ss in ("strict", "lax", "none"):
                ck["sameSite"] = ss.capitalize()
            pw_cookies.append(ck)
        try:
            self._ctx.add_cookies(pw_cookies)
        except Exception as e:
            print(f"[pw:{self.source}] cookie import partial: {e}")

    def _rate_limit(self) -> None:
        import time as _t
        elapsed = _t.time() - self._last_request_at
        if elapsed < self.rate_limit_sec:
            _t.sleep(self.rate_limit_sec - elapsed)
        self._last_request_at = _t.time()

    def get(self, url: str, timeout: int = 30, **kwargs) -> _PWResponse:
        self._ensure_started()
        self._rate_limit()
        # wait_until=domcontentloaded evita espera eterna em sites com trackers
        resp = self._page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        try:
            self._page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass  # networkidle timeout é OK — página usable
        status = resp.status if resp else 0
        content = self._page.content()
        return _PWResponse(content, status, url)

    def get_text(self, url: str, **kwargs) -> str:
        return self.get(url, **kwargs).text

    def get_bytes(self, url: str, extra_headers: dict | None = None, **kwargs) -> bytes:
        """Para downloads binários (PDF) — usa request context do Playwright.

        `extra_headers`: p.ex. `{"Referer": article_url}` — CDNs com WAF
        requerem Referer válido do article page.
        """
        self._ensure_started()
        self._rate_limit()
        api = self._ctx.request
        opts = {"timeout": kwargs.pop("timeout", 30) * 1000}
        if extra_headers:
            opts["headers"] = extra_headers
        r = api.get(url, **opts)
        if r.status >= 400:
            raise RuntimeError(f"HTTP {r.status} @ {url}")
        return r.body()

    def is_logged_in(self, probe_url: str, indicator: str) -> bool:
        try:
            return indicator.lower() in self.get_text(probe_url).lower()
        except Exception:
            return False

    def close(self) -> None:
        try:
            if self._ctx is not None:
                self._ctx.close()
        finally:
            if self._pw is not None:
                self._pw.stop()
            self._ctx = None
            self._pw = None
            self._page = None

    def __enter__(self):
        self._ensure_started()
        return self

    def __exit__(self, *exc):
        self.close()
