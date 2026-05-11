"""Public-portal scraper — Playwright (JS rendering) + Markdownify (clean MD).

Use case: fetch JS-rendered pages that requests/BS4 can't see.
  - RI / Investor Relations sites with SPA frontends (Vue/React)
  - B3 calendar / company filings index
  - fiis.com.br property pages with lazy-loaded data
  - Status Invest / Fundamentus when raw HTML is incomplete
  - One-off due-diligence on any URL the user mentions

Combines:
  - PlaywrightSession (already used by subscriptions adapters) without
    cookies — public-only.
  - library._md_extract for HTML→Markdown via markitdown when --md flag set.

Idempotent cache in data/portal_cache/<sha1>.{html,md} keyed by URL+TTL.

CLI:
    # Render and save HTML
    python fetchers/portal_playwright.py https://www.fiis.com.br/knhf11/

    # Render and convert to Markdown via markitdown
    python fetchers/portal_playwright.py https://www.fiis.com.br/knhf11/ --md

    # Capture full-page screenshot too
    python fetchers/portal_playwright.py https://ri.itausa.com.br --md --screenshot

    # Set TTL (default 24h cache); 0 disables cache
    python fetchers/portal_playwright.py https://b3.com.br/... --ttl 0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Allow `python fetchers/portal_playwright.py ...` direct invocation to find
# sibling packages (library, agents, fetchers) without -m.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CACHE_DIR = ROOT / "data" / "portal_cache"
LOG_PATH = ROOT / "logs" / "portal_playwright.log"

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _cache_key(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def _cache_paths(url: str) -> dict[str, Path]:
    k = _cache_key(url)
    return {
        "html": CACHE_DIR / f"{k}.html",
        "md": CACHE_DIR / f"{k}.md",
        "png": CACHE_DIR / f"{k}.png",
        "meta": CACHE_DIR / f"{k}.meta.json",
    }


def _is_cache_fresh(meta_path: Path, ttl_hours: float) -> bool:
    if ttl_hours <= 0 or not meta_path.exists():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(meta["fetched_at"].replace("Z", "+00:00"))
        age_hours = (datetime.now(timezone.utc) - fetched_at).total_seconds() / 3600
        return age_hours < ttl_hours
    except Exception:
        return False


def fetch(
    url: str,
    *,
    md: bool = False,
    screenshot: bool = False,
    ttl_hours: float = 24.0,
    timeout: int = 30,
    wait_for_selector: str | None = None,
    headless: bool = True,
) -> dict:
    """Fetch a public URL through Playwright, optionally extract Markdown.

    Returns dict with keys: url, status, html_path, md_path (if md=True),
    png_path (if screenshot=True), cached (bool), html_chars, md_chars.

    wait_for_selector: optional CSS selector to wait for (SPA hydration).
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    paths = _cache_paths(url)

    if _is_cache_fresh(paths["meta"], ttl_hours):
        meta = json.loads(paths["meta"].read_text(encoding="utf-8"))
        _log({"event": "cache_hit", "url": url})
        return {
            "url": url,
            "status": meta.get("status", 200),
            "html_path": str(paths["html"]),
            "md_path": str(paths["md"]) if paths["md"].exists() else None,
            "png_path": str(paths["png"]) if paths["png"].exists() else None,
            "cached": True,
            "html_chars": len(paths["html"].read_text(encoding="utf-8", errors="replace")),
            "md_chars": len(paths["md"].read_text(encoding="utf-8")) if paths["md"].exists() else 0,
        }

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError(
            "playwright não instalado. `pip install playwright && "
            "python -m playwright install chromium`"
        ) from e

    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=DEFAULT_UA,
            viewport={"width": 1440, "height": 900},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        page = ctx.new_page()
        try:
            resp = page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            status = resp.status if resp else 0
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            if wait_for_selector:
                try:
                    page.wait_for_selector(wait_for_selector, timeout=8000)
                except Exception:
                    pass

            html = page.content()
            paths["html"].write_text(html, encoding="utf-8")

            if screenshot:
                page.screenshot(path=str(paths["png"]), full_page=True)
        finally:
            ctx.close()
            browser.close()

    md_chars = 0
    md_path = None
    if md:
        try:
            from library._md_extract import extract_text
            md_text = extract_text(paths["html"], engine="markitdown")
            paths["md"].write_text(md_text, encoding="utf-8")
            md_chars = len(md_text)
            md_path = str(paths["md"])
        except Exception as e:
            _log({"event": "md_extract_failed", "url": url, "error": str(e)})

    elapsed = round(time.time() - t0, 2)
    meta = {
        "url": url,
        "status": status,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": elapsed,
        "html_chars": len(html),
        "md_chars": md_chars,
    }
    paths["meta"].write_text(json.dumps(meta, indent=2), encoding="utf-8")
    _log({"event": "fetched", "url": url, "status": status,
          "html_chars": len(html), "md_chars": md_chars, "elapsed_s": elapsed})

    return {
        "url": url,
        "status": status,
        "html_path": str(paths["html"]),
        "md_path": md_path,
        "png_path": str(paths["png"]) if screenshot else None,
        "cached": False,
        "html_chars": len(html),
        "md_chars": md_chars,
        "elapsed_s": elapsed,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="URL to fetch")
    ap.add_argument("--md", action="store_true",
                    help="Convert rendered HTML to Markdown via markitdown")
    ap.add_argument("--screenshot", action="store_true",
                    help="Capture full-page PNG screenshot")
    ap.add_argument("--ttl", type=float, default=24.0,
                    help="Cache TTL hours. 0 disables. Default 24.")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--selector", default=None,
                    help="CSS selector to wait for (SPA hydration)")
    ap.add_argument("--no-headless", action="store_true",
                    help="Show browser window (debug)")
    args = ap.parse_args()

    result = fetch(
        args.url,
        md=args.md,
        screenshot=args.screenshot,
        ttl_hours=args.ttl,
        timeout=args.timeout,
        wait_for_selector=args.selector,
        headless=not args.no_headless,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
