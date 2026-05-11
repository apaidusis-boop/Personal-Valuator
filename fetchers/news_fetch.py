"""news_fetch — RSS feeds (InfoMoney, Valor, Reuters) → classifica ticker + stance via Qwen.

Persiste em tabela `news` em ambas DBs (BR primeiro — fontes PT).

Uso:
    python fetchers/news_fetch.py                    # latest
    python fetchers/news_fetch.py --classify         # + Qwen stance/ticker
    python fetchers/news_fetch.py --digest --days 7  # resumo
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

FEEDS = [
    ("InfoMoney",   "https://www.infomoney.com.br/feed/"),
    ("Valor",       "https://valor.globo.com/rss/"),
    ("Reuters-BR",  "https://www.reuters.com/world/americas/brazil/rss"),
    ("SeekingAlpha","https://seekingalpha.com/feed.xml"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS news (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT NOT NULL,
    url         TEXT NOT NULL UNIQUE,
    title       TEXT NOT NULL,
    summary     TEXT,
    published   TEXT,
    classified  INTEGER NOT NULL DEFAULT 0,
    ticker      TEXT,           -- matched ticker if any
    stance      TEXT,           -- bullish|bearish|neutral (after classify)
    fetched_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_news_published ON news(published);
CREATE INDEX IF NOT EXISTS idx_news_ticker ON news(ticker);
"""


def _ensure(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def fetch_feeds() -> list[dict]:
    try:
        import feedparser
    except ImportError:
        print("feedparser não instalado. pip install feedparser")
        return []
    out = []
    for src, url in FEEDS:
        try:
            p = feedparser.parse(url)
            for e in p.entries[:30]:
                out.append({
                    "source": src,
                    "url": e.get("link", ""),
                    "title": e.get("title", "")[:300],
                    "summary": (e.get("summary", "") or e.get("description", ""))[:600],
                    "published": e.get("published", "") or e.get("updated", ""),
                })
        except Exception as exc:  # noqa: BLE001
            print(f"  {src}: {exc}")
    return out


def persist(items: list[dict]) -> int:
    n = 0
    now = datetime.now(UTC).isoformat()
    # Persist BR feeds in BR db, SeekingAlpha/Reuters in US db
    for item in items:
        db = DB_BR if item["source"] in ("InfoMoney", "Valor") else DB_US
        _ensure(db)
        with sqlite3.connect(db) as c:
            try:
                c.execute(
                    """INSERT OR IGNORE INTO news
                         (source, url, title, summary, published, fetched_at)
                       VALUES (?,?,?,?,?,?)""",
                    (item["source"], item["url"], item["title"],
                     item["summary"], item["published"], now),
                )
                if c.total_changes > 0:
                    n += 1
                c.commit()
            except sqlite3.Error:
                pass
    return n


def _classify_one(title: str, summary: str, universe: list[str]) -> dict:
    """Qwen 14B classifica: ticker match + stance."""
    import requests
    sys_prompt = (
        "Classifica uma notícia sobre mercado. Saída JSON estrito:\n"
        '{"ticker": "<TICKER ou null>", "stance": "bullish|bearish|neutral"}\n'
        f"Universo de tickers permitido: {', '.join(universe[:60])}. Se nenhum "
        "tickermencionado, ticker=null."
    )
    user = f"TITLE: {title}\nSUMMARY: {summary[:400]}"
    try:
        r = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:14b-instruct-q4_K_M",
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user},
                ],
                "format": "json",
                "options": {"temperature": 0.1, "num_ctx": 2048},
                "stream": False,
            },
            timeout=60,
        )
        r.raise_for_status()
        content = r.json()["message"]["content"]
        d = json.loads(content)
        return {
            "ticker": (d.get("ticker") or "").upper() if d.get("ticker") else None,
            "stance": d.get("stance", "neutral"),
        }
    except Exception:  # noqa: BLE001
        return {"ticker": None, "stance": "neutral"}


def classify_unclassified(limit: int = 50) -> int:
    n = 0
    for db in (DB_BR, DB_US):
        _ensure(db)
        with sqlite3.connect(db) as c:
            universe = [r[0] for r in c.execute("SELECT ticker FROM companies")]
            rows = c.execute(
                "SELECT id, title, summary FROM news WHERE classified=0 LIMIT ?",
                (limit,),
            ).fetchall()
            for rid, title, summary in rows:
                cls = _classify_one(title, summary or "", universe)
                c.execute(
                    """UPDATE news SET classified=1, ticker=?, stance=? WHERE id=?""",
                    (cls["ticker"], cls["stance"], rid),
                )
                n += 1
            c.commit()
    return n


def digest(days: int = 7) -> None:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    from collections import defaultdict
    by_tk = defaultdict(list)
    for db in (DB_BR, DB_US):
        _ensure(db)
        with sqlite3.connect(db) as c:
            for row in c.execute(
                """SELECT ticker, stance, title, source, published
                   FROM news WHERE classified=1 AND ticker IS NOT NULL
                     AND published >= ?
                   ORDER BY published DESC""",
                (cutoff,),
            ):
                by_tk[row[0]].append(row)

    if not by_tk:
        print("(sem news classificadas)")
        return
    print(f"News digest — últimos {days}d, {sum(len(v) for v in by_tk.values())} items\n")
    for tk in sorted(by_tk, key=lambda x: -len(by_tk[x])):
        rows = by_tk[tk]
        bull = sum(1 for r in rows if r[1] == "bullish")
        bear = sum(1 for r in rows if r[1] == "bearish")
        print(f"{tk:<8} {len(rows)} items  (🟢 {bull} bull, 🔴 {bear} bear)")
        for r in rows[:3]:
            icon = "🟢" if r[1] == "bullish" else "🔴" if r[1] == "bearish" else "⚪"
            print(f"  {icon} [{r[3]}] {r[2][:100]}")
        print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--classify", action="store_true")
    ap.add_argument("--digest", action="store_true")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--fetch-limit", type=int, default=100)
    args = ap.parse_args()

    if args.digest:
        digest(args.days)
        return 0

    items = fetch_feeds()
    n = persist(items)
    print(f"Fetched {len(items)} items, persisted {n} new")

    if args.classify:
        c = classify_unclassified(limit=args.fetch_limit)
        print(f"Classified {c} unclassified items via Qwen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
