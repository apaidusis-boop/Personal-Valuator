"""Topic Watchlist scorer (Phase EE.8 — reproduce Tina OpenClaw watchlist).

Reads `config/topic_watchlist.yaml` + scans the vault for evidence per topic,
producing a 0-100 score with a "tier" tag (Make Now / Rising / Watch / Background).

Score components:
  freshness  (40%) — last mention recency: <3d=40, 3-7d=30, 7-14d=20, 14-30d=10, else 0
  frequency  (35%) — mentions in last 14d: 0=0, 1=10, 2-3=20, 4-7=30, 8+=35
  breadth    (15%) — distinct holdings tracked AND mentioning the topic
  trigger    (10%) — open watchlist_actions on tracked tickers (recency+count)

Tiers:
  ≥75  → Make Now    (red, action item)
  ≥55  → Rising      (yellow)
  ≥35  → Watch       (purple)
  else → Background  (zinc)

Output:
  data/topic_scores.json — keyed by topic id
  Stdout summary table.
  Optional --vault flag writes a daily snapshot to obsidian.

CLI:
    python -m analytics.topic_scorer
    python -m analytics.topic_scorer --vault
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS_YAML = ROOT / "config" / "topic_watchlist.yaml"
VAULT_DIR = ROOT / "obsidian_vault"
SCORES_OUT = ROOT / "data" / "topic_scores.json"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _load_topics() -> list[dict]:
    try:
        import yaml  # type: ignore
    except ImportError:
        print("PyYAML not installed", file=sys.stderr)
        return []
    if not TOPICS_YAML.exists():
        return []
    raw = yaml.safe_load(TOPICS_YAML.read_text(encoding="utf-8")) or {}
    return raw.get("topics", [])


def _all_vault_files() -> list[tuple[Path, float, str]]:
    """Walk vault — return (path, mtime, content) for each .md file."""
    out: list[tuple[Path, float, str]] = []
    if not VAULT_DIR.exists():
        return out
    for p in VAULT_DIR.rglob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            out.append((p, p.stat().st_mtime, text))
        except Exception:
            continue
    return out


def _score_topic(topic: dict, vault: list[tuple[Path, float, str]]) -> dict:
    """Compute components + total score for one topic."""
    keywords = [k.lower() for k in topic.get("keywords", [])]
    tickers = [t.upper() for t in topic.get("track_for", [])]
    name_terms = topic.get("name", "").lower().split() + keywords

    now = datetime.now().timestamp()
    cutoff_3d = now - 3 * 86400
    cutoff_7d = now - 7 * 86400
    cutoff_14d = now - 14 * 86400
    cutoff_30d = now - 30 * 86400

    mentions: list[tuple[float, str]] = []  # (mtime, file)
    holdings_hit = set()

    for path, mtime, content in vault:
        if mtime < cutoff_30d:
            continue
        text_lower = content.lower()
        # Match if any keyword appears (whole-word for short keywords)
        matched = False
        for kw in keywords:
            if len(kw) >= 4 and kw in text_lower:
                matched = True
                break
            if len(kw) < 4 and re.search(rf"\b{re.escape(kw)}\b", text_lower):
                matched = True
                break
        if not matched:
            continue
        mentions.append((mtime, str(path.relative_to(VAULT_DIR))))
        # Holdings present in this file?
        for t in tickers:
            if re.search(rf"\b{re.escape(t)}\b", content):
                holdings_hit.add(t)

    last_mention = max((m[0] for m in mentions), default=0)
    n_recent = sum(1 for m, _ in mentions if m >= cutoff_14d)

    # Freshness
    if last_mention >= cutoff_3d:
        freshness = 40
    elif last_mention >= cutoff_7d:
        freshness = 30
    elif last_mention >= cutoff_14d:
        freshness = 20
    elif last_mention >= cutoff_30d:
        freshness = 10
    else:
        freshness = 0

    # Frequency
    if n_recent >= 8:
        frequency = 35
    elif n_recent >= 4:
        frequency = 30
    elif n_recent >= 2:
        frequency = 20
    elif n_recent >= 1:
        frequency = 10
    else:
        frequency = 0

    # Breadth
    breadth = min(15, len(holdings_hit) * 3)

    # Trigger boost — count open actions on tracked tickers
    open_triggers = 0
    for db in (DB_BR, DB_US):
        if not db.exists():
            continue
        try:
            with sqlite3.connect(db) as c:
                placeholders = ",".join("?" for _ in tickers) if tickers else "?"
                params = tickers if tickers else [""]
                row = c.execute(
                    f"SELECT COUNT(*) FROM watchlist_actions "
                    f"WHERE status='open' AND ticker IN ({placeholders})",
                    params,
                ).fetchone()
                open_triggers += row[0] if row else 0
        except sqlite3.OperationalError:
            pass
    trigger_score = min(10, open_triggers * 2)

    total = freshness + frequency + breadth + trigger_score

    if total >= 75:
        tier = "make_now"
    elif total >= 55:
        tier = "rising"
    elif total >= 35:
        tier = "watch"
    else:
        tier = "background"

    weeks_tracked = max(
        1, int(((now - min((m[0] for m in mentions), default=now)) // 86400) // 7)
    )

    return {
        "id": topic["id"],
        "name": topic["name"],
        "summary": topic.get("summary", ""),
        "tags": topic.get("tags", []),
        "tickers": tickers,
        "score": total,
        "tier": tier,
        "weeks_tracked": weeks_tracked,
        "mentions_recent": n_recent,
        "holdings_hit": sorted(holdings_hit),
        "open_triggers": open_triggers,
        "last_mention_iso": (
            datetime.fromtimestamp(last_mention).isoformat(timespec="seconds")
            if last_mention
            else None
        ),
        "components": {
            "freshness": freshness,
            "frequency": frequency,
            "breadth": breadth,
            "trigger": trigger_score,
        },
        "evidence_files": [f for _, f in sorted(mentions, reverse=True)[:5]],
    }


def score_all() -> dict:
    topics = _load_topics()
    if not topics:
        return {"computed_at": datetime.now().isoformat(), "topics": []}
    vault = _all_vault_files()
    scored = [_score_topic(t, vault) for t in topics]
    scored.sort(key=lambda s: s["score"], reverse=True)
    return {
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        "n_topics": len(scored),
        "topics": scored,
    }


def _print_summary(out: dict) -> None:
    sep = "═" * 72
    print(f"\n{sep}\n  Topic Watchlist — {out['n_topics']} topics  ·  {out['computed_at']}\n{sep}")
    tier_icon = {"make_now": "🔴", "rising": "🟡", "watch": "🟣", "background": "⚪"}
    for t in out["topics"]:
        print(
            f"{tier_icon.get(t['tier'],'?')} {t['score']:>3} {t['tier']:<10} "
            f"{t['name'][:50]:<50} {t['mentions_recent']:>3}m {len(t['holdings_hit']):>2}t"
        )
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Topic Watchlist scorer")
    ap.add_argument("--vault", action="store_true",
                    help="Snapshot to obsidian_vault/dashboards/Topic_Watchlist.md")
    args = ap.parse_args()

    out = score_all()
    SCORES_OUT.parent.mkdir(parents=True, exist_ok=True)
    SCORES_OUT.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"💾 {SCORES_OUT}")
    _print_summary(out)

    if args.vault:
        dash = ROOT / "obsidian_vault" / "dashboards" / "Topic_Watchlist.md"
        dash.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "---",
            f"type: topic_watchlist",
            f"computed_at: {out['computed_at']}",
            "tags: [topics, watchlist, dashboard]",
            "---",
            "",
            f"# Topic Watchlist — {out['n_topics']} themes",
            "",
            "| Tier | Score | Topic | Recent | Holdings | Triggers |",
            "|---|---|---|---|---|---|",
        ]
        for t in out["topics"]:
            tier_emoji = {"make_now": "🔴 Make Now", "rising": "🟡 Rising",
                          "watch": "🟣 Watch", "background": "⚪ BG"}[t["tier"]]
            lines.append(
                f"| {tier_emoji} | {t['score']} | {t['name']} | "
                f"{t['mentions_recent']}m / {t['weeks_tracked']}w | "
                f"{len(t['holdings_hit'])} ({', '.join(t['holdings_hit'][:3])}{'…' if len(t['holdings_hit'])>3 else ''}) | "
                f"{t['open_triggers']} |"
            )
        dash.write_text("\n".join(lines), encoding="utf-8")
        print(f"📝 vault: {dash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
