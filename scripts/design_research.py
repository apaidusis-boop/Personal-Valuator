"""design_research.py — Helena Linha continuous design scout.

Pesquisa GitHub semanalmente por novos Claude Code skills/agents focados em
design, UX, design systems, dashboard polish. Rankia por stars + recency,
filtra contra inventory já instalado, escreve em
`obsidian_vault/skills/Design_Watch.md` (overwrite, prepend new finds).

Uso:
    python scripts/design_research.py                   # full run
    python scripts/design_research.py --dry-run         # print only
    python scripts/design_research.py --since-days 30   # widen window

Cron:
    Weekly Sunday 23:00 (add to existing scheduled task)

Depends:
    - urllib (stdlib)  — no external deps, GitHub API unauth (rate-limited 60/h)
    - GITHUB_TOKEN env var (optional, raises to 5000/h)
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


def collect(since_days: int = 30) -> list[dict]:
    """Run all queries, dedupe, filter, classify."""
    seen: dict[str, dict] = {}
    cutoff = (date.today() - timedelta(days=since_days)).isoformat()
    for q in SEARCH_QUERIES:
        items = _gh_search(q)
        _log(f"query={q[:60]!r} returned={len(items)}")
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


def render(rows: list[dict]) -> str:
    today = date.today().isoformat()
    installed = _list_installed()
    install_rows = [r for r in rows if r["tier"] == "install"]
    consider_rows = [r for r in rows if r["tier"] == "consider"]

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
        f"> Auto-refreshed weekly. Last run: **{today}**. Total finds: **{len(rows)}** ({len(install_rows)} install / {len(consider_rows)} consider).",
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
        "## New: install tier",
        "",
        "Stars ≥1000, design-relevant description, pushed in window.",
        "",
    ]
    if install_rows:
        out.append("| Repo | Stars | Pushed | Description |")
        out.append("|---|---:|---|---|")
        for r in install_rows:
            desc = r["description"][:120].replace("|", "\\|")
            out.append(f"| [{r['full_name']}]({r['url']}) | {r['stars']} | {r['pushed_at']} | {desc} |")
    else:
        out.append("_(no new install-tier finds this week)_")

    out += ["", "## New: consider tier", "", "Stars ≥100 (or ≥5 with strong design keyword). Helena triages.", ""]
    if consider_rows:
        out.append("| Repo | Stars | Pushed | Description |")
        out.append("|---|---:|---|---|")
        for r in consider_rows[:30]:  # cap
            desc = r["description"][:100].replace("|", "\\|")
            out.append(f"| [{r['full_name']}]({r['url']}) | {r['stars']} | {r['pushed_at']} | {desc} |")
    else:
        out.append("_(no new consider-tier finds this week)_")

    out += [
        "",
        "## Helena's recommendation this week",
        "",
        "_(Auto-generated stub — Helena writes here on review)_",
        "",
        "## Notes",
        "",
        "- Source: GitHub search API. Queries in `scripts/design_research.py::SEARCH_QUERIES`.",
        "- Adicionar repo à blacklist: editar `KNOWN` no script.",
        "- Rate limit 60/h sem token; 5000/h com `GITHUB_TOKEN`.",
        f"- Log: `logs/design_research.log`",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--since-days", type=int, default=30)
    args = ap.parse_args()

    rows = collect(since_days=args.since_days)
    md = render(rows)

    if args.dry_run:
        print(md)
        return 0

    VAULT.mkdir(parents=True, exist_ok=True)
    WATCH_FILE.write_text(md, encoding="utf-8")
    install_n = sum(1 for r in rows if r["tier"] == "install")
    consider_n = sum(1 for r in rows if r["tier"] == "consider")
    msg = f"wrote {WATCH_FILE.relative_to(ROOT)} · {len(rows)} finds ({install_n} install / {consider_n} consider)"
    _log(msg)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
