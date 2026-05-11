"""autoresearch — Tavily-based web research client com cache + rate-limit local.

Phase K (2026-04-26). Implementa W.5 do Roadmap (Autoresearch / "Heart of Gold").

Design:
  - 100% in-house pipeline. Zero Claude tokens.
  - Tavily API call → JSON cache local 7d → Ollama Qwen 14B sintetiza.
  - Rate-limit local: max 100 calls/dia (default), 50/h burst — protege quota.
  - Fallback gracioso: se Tavily down ou key missing, retorna estrutura vazia
    (não bloqueia perpetuums downstream).
  - Cache key = sha1(query|search_depth|topic). Hit ratio esperado: 30-50%
    (queries por ticker variam pouco entre runs).

Uso programático:
    from agents.autoresearch import search, search_ticker_news

    r = search("ITSA4 Itaúsa earnings 2025", max_results=5)
    if r.results:
        for hit in r.results:
            print(hit.title, hit.url, hit.score)

CLI:
    python -m agents.autoresearch query "ITSA4 dividendos 2025"
    python -m agents.autoresearch ticker ITSA4 --topic earnings
    python -m agents.autoresearch stats               # cache stats
    python -m agents.autoresearch test                # smoke test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "data" / "tavily_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

RATELIMIT_LOG = CACHE_DIR / "_ratelimit.json"
TAVILY_URL = "https://api.tavily.com/search"

CACHE_TTL_DAYS = 7
DAILY_LIMIT = 100        # max calls/day (protege quota mensal)
HOURLY_LIMIT = 50        # burst protection


# --- env loader (mirror notifiers/telegram._load_env pattern) ---

def _load_env() -> str | None:
    """Returns TAVILY_API_KEY from env or .env file. None se ausente."""
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("TAVILY_API_KEY") and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# --- result dataclasses ---

@dataclass
class TavilyHit:
    title: str
    url: str
    content: str
    score: float
    published_date: str | None = None


@dataclass
class TavilyResult:
    query: str
    answer: str | None
    results: list[TavilyHit]
    cached: bool = False
    cache_path: str | None = None
    error: str | None = None
    raw: dict = field(default_factory=dict)


# --- rate limit ---

def _read_ratelimit() -> dict:
    if not RATELIMIT_LOG.exists():
        return {"day": date.today().isoformat(), "day_count": 0,
                "hour": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H"),
                "hour_count": 0, "total": 0}
    try:
        return json.loads(RATELIMIT_LOG.read_text(encoding="utf-8"))
    except Exception:
        return {"day": date.today().isoformat(), "day_count": 0,
                "hour": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H"),
                "hour_count": 0, "total": 0}


def _bump_ratelimit() -> tuple[bool, str]:
    """Returns (allowed, reason)."""
    rl = _read_ratelimit()
    today = date.today().isoformat()
    this_hour = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
    if rl["day"] != today:
        rl["day"] = today
        rl["day_count"] = 0
    if rl["hour"] != this_hour:
        rl["hour"] = this_hour
        rl["hour_count"] = 0
    if rl["day_count"] >= DAILY_LIMIT:
        return False, f"daily_limit ({DAILY_LIMIT}) exceeded"
    if rl["hour_count"] >= HOURLY_LIMIT:
        return False, f"hourly_limit ({HOURLY_LIMIT}) exceeded"
    rl["day_count"] += 1
    rl["hour_count"] += 1
    rl["total"] = rl.get("total", 0) + 1
    rl["last_call"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    RATELIMIT_LOG.write_text(json.dumps(rl, indent=2), encoding="utf-8")
    return True, ""


# --- cache ---

def _cache_key(query: str, depth: str, topic: str | None) -> str:
    payload = f"{query}|{depth}|{topic or ''}".encode("utf-8")
    return hashlib.sha1(payload).hexdigest()[:16]


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}.json"


def _cache_load(key: str) -> dict | None:
    p = _cache_path(key)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    cached_at = data.get("_cached_at")
    if cached_at:
        try:
            ts = datetime.fromisoformat(cached_at)
            if datetime.now(timezone.utc) - ts.replace(tzinfo=timezone.utc) > timedelta(days=CACHE_TTL_DAYS):
                return None  # stale
        except Exception:
            pass
    return data


def _cache_save(key: str, data: dict) -> Path:
    p = _cache_path(key)
    data["_cached_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


# --- main API ---

def search(
    query: str,
    *,
    search_depth: Literal["basic", "advanced"] = "basic",
    topic: Literal["general", "news", "finance"] | None = None,
    max_results: int = 5,
    include_answer: bool = True,
    days_back: int | None = None,
    timeout: int = 30,
) -> TavilyResult:
    """Tavily search com cache + rate-limit. Devolve TavilyResult.

    Cache hit: zero Tavily quota gasta. Cache TTL 7d.
    Rate-limit: max 100/day, 50/hour (defaults).
    """
    key = _cache_key(query, search_depth, topic)
    cached = _cache_load(key)
    if cached:
        return _build_result(query, cached, cached=True, cache_path=str(_cache_path(key)))

    api_key = _load_env()
    if not api_key:
        return TavilyResult(
            query=query, answer=None, results=[],
            error="no_api_key (set TAVILY_API_KEY in .env)",
        )

    allowed, reason = _bump_ratelimit()
    if not allowed:
        return TavilyResult(
            query=query, answer=None, results=[],
            error=f"rate_limit: {reason}",
        )

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "max_results": max_results,
        "include_answer": include_answer,
    }
    if topic:
        payload["topic"] = topic
    if days_back is not None:
        payload["days"] = days_back

    try:
        import requests
        r = requests.post(TAVILY_URL, json=payload, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return TavilyResult(
            query=query, answer=None, results=[],
            error=f"tavily_call_failed: {type(e).__name__}: {e}",
        )

    cache_path = _cache_save(key, data)
    return _build_result(query, data, cached=False, cache_path=str(cache_path))


def _build_result(query: str, data: dict, *, cached: bool, cache_path: str) -> TavilyResult:
    hits = []
    for r in (data.get("results") or []):
        hits.append(TavilyHit(
            title=r.get("title", ""),
            url=r.get("url", ""),
            content=(r.get("content") or "")[:1000],
            score=float(r.get("score", 0) or 0),
            published_date=r.get("published_date"),
        ))
    return TavilyResult(
        query=query,
        answer=data.get("answer"),
        results=hits,
        cached=cached,
        cache_path=cache_path,
        raw=data,
    )


# --- convenience: ticker-targeted searches ---

TICKER_TOPICS = {
    "earnings": "{name} ({ticker}) earnings results last quarter beat miss guidance",
    "guidance": "{name} ({ticker}) forward guidance fy26 outlook",
    "news":     "{name} ({ticker}) news",
    "regime":   "{name} ({ticker}) regulatory macro risk",
    "downgrade":"{name} ({ticker}) analyst downgrade upgrade target",
    "scandal":  "{name} ({ticker}) fraud investigation scandal lawsuit",
}


def _company_name(ticker: str, market: str | None) -> str:
    """Resolve nome da empresa via companies table. Fallback para ticker."""
    import sqlite3
    candidates = [market] if market else ["us", "br"]
    for m in candidates:
        db = ROOT / "data" / f"{m}_investments.db"
        if not db.exists():
            continue
        try:
            with sqlite3.connect(db) as c:
                row = c.execute(
                    "SELECT name FROM companies WHERE ticker=?", (ticker,)
                ).fetchone()
                if row and row[0]:
                    name = (row[0] or "").strip()
                    # Strip common suffixes for cleaner Tavily query
                    for suf in [" S.A.", " SA", " Inc.", " Inc", " Corp.", " Corp",
                                " Ltd.", " Ltd", " Holdings", " Group", " Co.", " Co"]:
                        if name.endswith(suf):
                            name = name[:-len(suf)].strip()
                    return name
        except Exception:
            continue
    return ticker


def search_ticker(
    ticker: str,
    topic: Literal["earnings", "guidance", "news", "regime", "downgrade", "scandal"] = "news",
    market: str | None = None,
    days_back: int = 30,
    **kwargs,
) -> TavilyResult:
    """Curated ticker-specific search. Auto-injecta company name (improves
    Tavily relevance ~5x para US tickers) + market context se BR."""
    template = TICKER_TOPICS.get(topic, "{name} ({ticker})")
    name = _company_name(ticker, market)
    suffix = " B3 brazil" if market == "br" else ""
    query = template.format(ticker=ticker, name=name) + suffix
    return search(
        query,
        topic="news" if topic in ("news", "earnings", "guidance", "downgrade", "scandal") else "general",
        days_back=days_back,
        **kwargs,
    )


# --- CLI ---

def _stats() -> dict:
    rl = _read_ratelimit()
    cache_files = list(CACHE_DIR.glob("*.json"))
    cache_files = [p for p in cache_files if not p.name.startswith("_")]
    return {
        "ratelimit": rl,
        "cache_files": len(cache_files),
        "cache_size_kb": round(sum(p.stat().st_size for p in cache_files) / 1024, 1),
        "limits": {"daily": DAILY_LIMIT, "hourly": HOURLY_LIMIT, "ttl_days": CACHE_TTL_DAYS},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    p_q = sub.add_parser("query")
    p_q.add_argument("query")
    p_q.add_argument("--depth", choices=["basic", "advanced"], default="basic")
    p_q.add_argument("--topic", choices=["general", "news", "finance"])
    p_q.add_argument("--max", type=int, default=5)

    p_t = sub.add_parser("ticker")
    p_t.add_argument("ticker")
    p_t.add_argument("--topic", choices=list(TICKER_TOPICS.keys()), default="news")
    p_t.add_argument("--market", choices=["br", "us"])

    sub.add_parser("stats")
    sub.add_parser("test")

    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.cmd == "query":
        r = search(args.query, search_depth=args.depth, topic=args.topic, max_results=args.max)
    elif args.cmd == "ticker":
        r = search_ticker(args.ticker, topic=args.topic, market=args.market)
    elif args.cmd == "stats":
        print(json.dumps(_stats(), indent=2, ensure_ascii=False))
        return 0
    elif args.cmd == "test":
        r = search("Apple earnings Q4 2025 beat miss", topic="news", max_results=3)
    else:
        ap.print_help()
        return 1

    if r.error:
        print(f"ERROR: {r.error}")
        return 2

    print(f"Query: {r.query}")
    print(f"Cached: {r.cached} ({r.cache_path})")
    print()
    if r.answer:
        print("=== Tavily synth answer ===")
        print(r.answer[:1500])
        print()
    print(f"=== Top {len(r.results)} hits ===")
    for h in r.results:
        date_s = f" [{h.published_date}]" if h.published_date else ""
        print(f"  [{h.score:.2f}]{date_s} {h.title}")
        print(f"         {h.url}")
        print(f"         {h.content[:200]}...")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
