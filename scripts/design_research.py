"""design_research.py — Helena Linha continuous design scout.

Multi-source weekly scout: GitHub + design blog RSS + (deferred) YouTube.
Filtra contra inventory já instalado, escreve em
`obsidian_vault/skills/Design_Watch.md` (overwrite).

Uso:
    python scripts/design_research.py                   # full run all sources
    python scripts/design_research.py --dry-run         # print only
    python scripts/design_research.py --since-days 30   # widen window
    python scripts/design_research.py --source github   # single source

Cron:
    Weekly Sunday 23:30 (wired in scripts/daily_run.bat).

Depends:
    - urllib (stdlib)
    - GITHUB_TOKEN env var (optional, raises GitHub to 5000/h)
    - YOUTUBE_API_KEY env var (optional, enables YouTube source)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load .env so YOUTUBE_API_KEY / GITHUB_TOKEN are picked up when run from cron.
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass
VAULT = ROOT / "obsidian_vault" / "skills"
WATCH_FILE = VAULT / "Design_Watch.md"
LOG_FILE = ROOT / "logs" / "design_research.log"
INSTALLED_DIR = Path.home() / ".claude" / "skills"

# Search queries — each returns a list of repos. Helena tunes these over time.
SEARCH_QUERIES = [
    # Topic-based
    'topic:claude-code-skill design',
    'topic:claude-skill design',
    'topic:claude-code-skill ui',
    'topic:claude-code-skill ux',
    # Keyword-based, scoped to recent + relevant
    '"claude code" design skill in:name,description,readme',
    '"claude code" "design system" in:name,description,readme',
    '"claude code skill" "design review" in:name,description,readme',
    '"claude code" dashboard polish in:description,readme',
    'claude-code design tokens in:name,description,readme',
]

# Repos we already evaluated — won't show up as "new" again
KNOWN = {
    "nextlevelbuilder/ui-ux-pro-max-skill",
    "dominikmartn/hue",
    "alchaincyf/huashu-design",
    "travisvn/awesome-claude-skills",
    "rohitg00/awesome-claude-design",
    "joeseesun/qiaomu-design-advisor",
    "gregorymm/design-review-plugin",
    "airowe/claude-a11y-skill",
    "kylezantos/design-motion-principles",
    "dominikmartn/nothing-design-skill",
    "hamen/material-3-skill",
    "designagentlab/skills",
}

# Min stars to surface as "consider" tier
MIN_STARS = 5


def _gh_search(query: str, per_page: int = 30) -> list[dict]:
    """Hit GitHub search/repositories endpoint. Returns items list."""
    qs = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": per_page})
    url = f"https://api.github.com/search/repositories?{qs}"
    headers = {
        "User-Agent": "design-research-helena",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("items", [])
    except urllib.error.HTTPError as e:
        _log(f"HTTP {e.code} on query: {query[:60]} — {e.reason}")
        return []
    except Exception as e:
        _log(f"ERR on query: {query[:60]} — {type(e).__name__}: {e}")
        return []


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        ts = datetime.now(UTC).isoformat(timespec="seconds")
        f.write(f"{ts} {msg}\n")


def _list_installed() -> set[str]:
    """Return set of skill folder names already installed under ~/.claude/skills."""
    if not INSTALLED_DIR.exists():
        return set()
    return {p.name for p in INSTALLED_DIR.iterdir() if p.is_dir()}


def _classify(repo: dict) -> str:
    """Tier the repo: install / consider / skip — Helena heuristics, strict."""
    stars = repo.get("stargazers_count", 0)
    desc = (repo.get("description") or "").lower()
    name = repo.get("name", "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    pushed = repo.get("pushed_at", "")[:10]
    text = f"{name} {desc}"

    try:
        days_stale = (date.today() - date.fromisoformat(pushed)).days
    except Exception:
        days_stale = 9999
    if days_stale > 180:
        return "skip"

    # Off-topic guards
    bad_keywords = ["crypto", "mev", "trading bot", "telegram bot", "minecraft",
                    "career", "job search", "resume", "playwright", "browser-use"]
    if any(b in text for b in bad_keywords):
        return "skip"

    # Generic curated lists — usually 50k+ stars, not actionable
    generic_list_signals = ["awesome lists about all kinds", "curated list of awesome",
                            "interactive roadmaps", "anthropics/skills"]
    if any(s in desc for s in generic_list_signals) and "design" not in name:
        return "skip"

    # Strong design signals (need ≥1 of these)
    design_strong = ["design system", "design language", "design review",
                     "design tokens", "color palette", "typography", "ui style",
                     "design intelligence", "design skill", "ux audit",
                     "accessibility", "dashboard polish", "visual hierarchy"]
    has_strong = any(s in text for s in design_strong) or any("design" in t for t in topics)

    # Weak design signals
    design_weak = ["design", "ui", "ux", "frontend", "dashboard"]
    weak_count = sum(1 for k in design_weak if k in text)

    # Claude-Code specificity (raises confidence)
    is_claude = any(k in text for k in ["claude code", "claude-code", "claude skill",
                                          "claude agent", "agent skill"]) \
                or any(t in topics for t in ["claude-code", "claude-code-skill", "claude-skill"])

    # Tier rules
    if has_strong and is_claude and stars >= 50:
        return "install"
    if has_strong and stars >= 500:
        return "install"
    if has_strong and stars >= 50:
        return "consider"
    if is_claude and weak_count >= 2 and stars >= 100:
        return "consider"
    if weak_count >= 2 and stars >= MIN_STARS and is_claude:
        return "consider"
    return "skip"


# ─────────────── source: design blog RSS feeds ───────────────

RSS_FEEDS = [
    ("Smashing Magazine",   "https://www.smashingmagazine.com/feed/"),
    ("CSS-Tricks",          "https://css-tricks.com/feed/"),
    ("A List Apart",        "https://alistapart.com/main/feed/"),
    ("Nielsen Norman",      "https://www.nngroup.com/feed/rss/"),
    ("Refactoring UI blog", "https://www.refactoringui.com/blog/feed.xml"),
]


def _fetch_rss(name: str, url: str, cutoff_iso: str) -> list[dict]:
    """Minimal RSS/Atom parser (no external deps). Returns recent items."""
    import re as _re
    headers = {"User-Agent": "design-research-helena/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        _log(f"rss FAIL {name}: {type(e).__name__}: {e}")
        return []

    items = []
    item_re = _re.compile(r"<item>(.*?)</item>|<entry>(.*?)</entry>", _re.DOTALL)
    title_re = _re.compile(r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", _re.DOTALL)
    link_re = _re.compile(r'<link[^>]*?href="([^"]+)"|<link>(.*?)</link>', _re.DOTALL)
    date_re = _re.compile(r"<(?:pubDate|published|updated|dc:date)>(.*?)</", _re.DOTALL)

    for m in item_re.finditer(xml):
        block = m.group(1) or m.group(2) or ""
        t = title_re.search(block)
        l = link_re.search(block)
        d = date_re.search(block)
        title = (t.group(1) if t else "").strip()
        link = ""
        if l:
            link = (l.group(1) or l.group(2) or "").strip()
        date_str = (d.group(1) if d else "").strip()[:10]
        if not title or not link:
            continue
        if date_str and date_str < cutoff_iso:
            continue
        items.append({"source": name, "title": title[:200], "url": link, "date": date_str or "—"})
    _log(f"rss {name}: {len(items)} items in window")
    return items


# ─────────────── source: YouTube (deferred — needs API key) ───────────────

def _fetch_youtube(cutoff_iso: str) -> list[dict]:
    """YouTube Data API search for design tutorials. Stub if no API key."""
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        _log("youtube SKIP: no YOUTUBE_API_KEY env var")
        return []
    queries = ["claude code design skill", "claude code dashboard", "design system tutorial 2026"]
    out = []
    for q in queries:
        qs = urllib.parse.urlencode({
            "part": "snippet", "q": q, "type": "video", "order": "date",
            "maxResults": 5, "key": api_key,
            "publishedAfter": f"{cutoff_iso}T00:00:00Z",
        })
        try:
            with urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/search?{qs}", timeout=10) as r:
                data = json.loads(r.read())
            for it in data.get("items", []):
                sn = it["snippet"]
                out.append({
                    "source": f"YouTube · {sn['channelTitle']}",
                    "title": sn["title"][:200],
                    "url": f"https://youtu.be/{it['id']['videoId']}",
                    "date": sn["publishedAt"][:10],
                })
        except Exception as e:
            _log(f"youtube FAIL {q!r}: {e}")
    return out


# ─────────────── orchestration ───────────────

def collect_github(since_days: int) -> list[dict]:
    """GitHub source — repos with design relevance."""
    seen: dict[str, dict] = {}
    cutoff = (date.today() - timedelta(days=since_days)).isoformat()
    for q in SEARCH_QUERIES:
        items = _gh_search(q)
        _log(f"gh query={q[:60]!r} returned={len(items)}")
        for it in items:
            full = it["full_name"]
            if full in KNOWN:
                continue
            if it.get("pushed_at", "")[:10] < cutoff:
                continue
            tier = _classify(it)
            if tier == "skip":
                continue
            if full not in seen:
                seen[full] = {
                    "full_name": full,
                    "url": it["html_url"],
                    "description": (it.get("description") or "").strip(),
                    "stars": it.get("stargazers_count", 0),
                    "pushed_at": it.get("pushed_at", "")[:10],
                    "language": it.get("language") or "—",
                    "topics": it.get("topics", []),
                    "tier": tier,
                    "matched_query": q,
                }
    return sorted(seen.values(), key=lambda r: (r["tier"] != "install", -r["stars"]))


def collect_blogs(since_days: int) -> list[dict]:
    cutoff = (date.today() - timedelta(days=since_days)).isoformat()
    out = []
    for name, url in RSS_FEEDS:
        out.extend(_fetch_rss(name, url, cutoff))
    return sorted(out, key=lambda x: x.get("date", ""), reverse=True)


def collect_youtube(since_days: int) -> list[dict]:
    cutoff = (date.today() - timedelta(days=since_days)).isoformat()
    return _fetch_youtube(cutoff)


# Backward-compat alias used by old callers
def collect(since_days: int = 30) -> list[dict]:
    return collect_github(since_days)


def render(gh_rows: list[dict], blog_rows: list[dict], yt_rows: list[dict]) -> str:
    today = date.today().isoformat()
    installed = _list_installed()
    install_rows = [r for r in gh_rows if r["tier"] == "install"]
    consider_rows = [r for r in gh_rows if r["tier"] == "consider"]

    out = [
        "---",
        "type: design_watch",
        f"updated: {today}",
        "owner: helena_linha",
        "tags: [design, watch, research, helena]",
        "---",
        "",
        "# Design Watch — Helena Linha continuous scout",
        "",
        f"> Auto-refreshed weekly. Last run: **{today}**. ",
        f"> GitHub: **{len(gh_rows)}** ({len(install_rows)} install / {len(consider_rows)} consider) · "
        f"Blogs: **{len(blog_rows)}** · YouTube: **{len(yt_rows)}**",
        "",
        "## Currently installed (`~/.claude/skills/`)",
        "",
    ]
    if installed:
        for s in sorted(installed):
            out.append(f"- `{s}`")
    else:
        out.append("- _(empty)_")
    out += [
        "",
        "## GitHub · install tier",
        "",
        "Stars ≥1000 com design-keyword forte, pushed em window.",
        "",
    ]
    if install_rows:
        out.append("| Repo | Stars | Pushed | Description |")
        out.append("|---|---:|---|---|")
        for r in install_rows:
            desc = r["description"][:120].replace("|", "\\|")
            out.append(f"| [{r['full_name']}]({r['url']}) | {r['stars']} | {r['pushed_at']} | {desc} |")
    else:
        out.append("_(no new install-tier finds)_")

    out += ["", "## GitHub · consider tier", "", "Stars ≥50 com design strong, ou ≥100 + Claude-Code spec.", ""]
    if consider_rows:
        out.append("| Repo | Stars | Pushed | Description |")
        out.append("|---|---:|---|---|")
        for r in consider_rows[:30]:
            desc = r["description"][:100].replace("|", "\\|")
            out.append(f"| [{r['full_name']}]({r['url']}) | {r['stars']} | {r['pushed_at']} | {desc} |")
    else:
        out.append("_(no new consider-tier finds)_")

    out += ["", "## Design blogs · latest posts", "", "RSS feeds in window — Helena triages para padrões emergentes.", ""]
    if blog_rows:
        out.append("| Source | Date | Title |")
        out.append("|---|---|---|")
        for r in blog_rows[:25]:
            t = r["title"].replace("|", "\\|")
            out.append(f"| {r['source']} | {r.get('date','—')} | [{t}]({r['url']}) |")
    else:
        out.append("_(blogs offline ou sem posts em window)_")

    out += ["", "## YouTube · latest videos", ""]
    if yt_rows:
        out.append("| Source | Date | Title |")
        out.append("|---|---|---|")
        for r in yt_rows[:15]:
            t = r["title"].replace("|", "\\|")
            out.append(f"| {r['source']} | {r['date']} | [{t}]({r['url']}) |")
    else:
        out.append("_(YouTube source desactivado — exporta `YOUTUBE_API_KEY` para activar)_")

    out += [
        "",
        "## Helena's recommendation this week",
        "",
        "_(Helena reescreve esta secção semanalmente após review)_",
        "",
        "## Sources & tuning",
        "",
        "- **GitHub** — 9 queries em `SEARCH_QUERIES`. Inventory: `KNOWN` set.",
        "- **RSS** — Smashing Mag, CSS-Tricks, A List Apart, NN/g, Refactoring UI.",
        "- **YouTube** — opt-in via `YOUTUBE_API_KEY` env. 3 queries.",
        "- Rate limits: GitHub 60/h sem token; 5000/h com `GITHUB_TOKEN`. YouTube 10k units/dia free tier.",
        "- Log: `logs/design_research.log`",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--since-days", type=int, default=30)
    ap.add_argument("--source", choices=["github", "blogs", "youtube", "all"], default="all")
    args = ap.parse_args()

    gh_rows = collect_github(args.since_days) if args.source in ("github", "all") else []
    blog_rows = collect_blogs(args.since_days) if args.source in ("blogs", "all") else []
    yt_rows = collect_youtube(args.since_days) if args.source in ("youtube", "all") else []

    md = render(gh_rows, blog_rows, yt_rows)

    if args.dry_run:
        print(md)
        return 0

    VAULT.mkdir(parents=True, exist_ok=True)
    WATCH_FILE.write_text(md, encoding="utf-8")
    install_n = sum(1 for r in gh_rows if r["tier"] == "install")
    msg = (f"wrote {WATCH_FILE.relative_to(ROOT)} · "
           f"gh={len(gh_rows)} ({install_n} install) blogs={len(blog_rows)} yt={len(yt_rows)}")
    _log(msg)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
