"""Phase W.7 — Skill Scout (Catalog Monitoring, passive).

Monthly cron that audits skills arsenal vs. actual implementation activity.
Reads ``obsidian_vault/skills/SKL_*.md``, parses frontmatter, finds linked
implementation files, queries ``git log`` for last-touched dates, then
classifies each skill into:

- **Active** — implementation file touched in last 30 days
- **Stable** — touched 30-90 days ago (no concern)
- **Decay candidate** — 90+ days untouched (review whether still useful)
- **Backlog** — status:backlog in frontmatter, no impl found yet
- **Skipped** — tier_B/tier_C/skip notes (informational only)

Output: ``obsidian_vault/skills/Skill_Scout_YYYY-MM-DD.md`` with backlinks
to each SKL note + git commits for context.

Read-only. No DB writes. No LLM calls. Pure stdlib + git.

Usage:
    python -m agents.skill_scout            # write report for today
    python -m agents.skill_scout --dry-run  # print summary, no file write
    python -m agents.skill_scout --json     # machine-readable output

Cron: monthly (first day of month). User wires schtasks externally; until
then, run manually after major skill rollouts.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "obsidian_vault" / "skills"
OUT_PATTERN = "Skill_Scout_{date}.md"

ACTIVE_DAYS = 30
STABLE_DAYS = 90

# Heuristic: scan SKL note body for path references like `agents/foo.py`,
# `scripts/bar.py`, `library/x/y.py`, etc. Only paths that resolve to an
# existing file are kept.
PATH_RE = re.compile(
    r"`?([a-z_][a-z0-9_/\-]*?/[a-z0-9_/\-\.]+\.py)`?",
    re.IGNORECASE,
)


@dataclass
class SkillRecord:
    name: str
    note_path: str
    status: str | None
    sprint: str | None
    tier: str | None
    impl_files: list[str]
    last_commit_iso: str | None
    days_since_last: int | None
    bucket: str  # active | stable | decay | backlog | skipped


def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip("'\"")
    return fm


def _find_impl_files(text: str) -> list[str]:
    """Return existing repo-relative .py paths mentioned in the note."""
    seen: set[str] = set()
    for m in PATH_RE.finditer(text):
        path = m.group(1).replace("\\", "/")
        if path in seen:
            continue
        # Skip obvious doc paths
        if path.startswith(("obsidian_vault/", "data/", "logs/", "tests/")):
            continue
        if (ROOT / path).is_file():
            seen.add(path)
    return sorted(seen)


def _git_last_touched(path: str) -> tuple[str | None, int | None]:
    """Return (ISO date of last commit, days since today). None if never."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", path],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
        ).strip()
    except (subprocess.SubprocessError, OSError):
        return None, None
    if not out:
        return None, None
    try:
        ts = datetime.fromisoformat(out)
    except ValueError:
        return None, None
    days = (datetime.now(ts.tzinfo) - ts).days
    return ts.date().isoformat(), days


def _classify(rec_data: dict) -> str:
    name = rec_data["name"]
    status = (rec_data.get("status") or "").lower()
    tier = (rec_data.get("tier") or "").lower()
    if "tier_B" in name or "tier_C" in name or tier in ("b", "c"):
        return "skipped"
    if status == "backlog" and not rec_data["impl_files"]:
        return "backlog"
    days = rec_data["days_since_last"]
    if days is None:
        # No impl found and not explicitly backlog -> treat as backlog
        return "backlog"
    if days <= ACTIVE_DAYS:
        return "active"
    if days <= STABLE_DAYS:
        return "stable"
    return "decay"


def scan_skills() -> list[SkillRecord]:
    records: list[SkillRecord] = []
    for note in sorted(SKILLS_DIR.glob("SKL_*.md")):
        text = note.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        impl_files = _find_impl_files(text)
        # Pick the most recently touched impl file as the skill's pulse
        last_iso: str | None = None
        last_days: int | None = None
        for path in impl_files:
            iso, days = _git_last_touched(path)
            if days is None:
                continue
            if last_days is None or days < last_days:
                last_iso = iso
                last_days = days
        rec_data = {
            "name": note.stem,
            "note_path": note.relative_to(ROOT).as_posix(),
            "status": fm.get("status"),
            "sprint": fm.get("sprint"),
            "tier": fm.get("tier"),
            "impl_files": impl_files,
            "last_commit_iso": last_iso,
            "days_since_last": last_days,
        }
        rec_data["bucket"] = _classify(rec_data)
        records.append(SkillRecord(**rec_data))
    return records


def render_md(records: list[SkillRecord], today: str) -> str:
    by_bucket: dict[str, list[SkillRecord]] = {}
    for r in records:
        by_bucket.setdefault(r.bucket, []).append(r)
    counts = {k: len(v) for k, v in by_bucket.items()}

    lines: list[str] = []
    lines.append("---")
    lines.append("type: skill_scout_report")
    lines.append(f"date: {today}")
    lines.append(f"total: {len(records)}")
    lines.append(f"active: {counts.get('active', 0)}")
    lines.append(f"stable: {counts.get('stable', 0)}")
    lines.append(f"decay: {counts.get('decay', 0)}")
    lines.append(f"backlog: {counts.get('backlog', 0)}")
    lines.append(f"skipped: {counts.get('skipped', 0)}")
    lines.append("tags: [skill_scout, monthly, w_7]")
    lines.append("---")
    lines.append("")
    lines.append(f"# 🛰️ Skill Scout — {today}")
    lines.append("")
    lines.append(f"Auditoria mensal de **{len(records)} skill notes** vs. actividade no codebase.")
    lines.append(
        f"Active = touched ≤{ACTIVE_DAYS}d · Stable = {ACTIVE_DAYS+1}–{STABLE_DAYS}d · "
        f"Decay = >{STABLE_DAYS}d · Backlog = no impl found."
    )
    lines.append("")
    lines.append(
        f"**Snapshot**: 🟢 {counts.get('active',0)} active · "
        f"🟡 {counts.get('stable',0)} stable · "
        f"🔴 {counts.get('decay',0)} decay · "
        f"⏳ {counts.get('backlog',0)} backlog · "
        f"⚪ {counts.get('skipped',0)} skipped."
    )
    lines.append("")

    section_order = [
        ("decay", "🔴 Decay candidates (>90d untouched — review)"),
        ("backlog", "⏳ Backlog (no impl yet)"),
        ("active", "🟢 Active (≤30d)"),
        ("stable", "🟡 Stable (30–90d)"),
        ("skipped", "⚪ Skipped (Tier B/C — informational)"),
    ]
    for key, header in section_order:
        items = by_bucket.get(key, [])
        if not items:
            continue
        lines.append(f"## {header}")
        lines.append("")
        for r in sorted(items, key=lambda x: (x.days_since_last or 9999, x.name), reverse=(key == "decay")):
            note_link = f"[[{r.name}]]"
            sprint = f" · sprint {r.sprint}" if r.sprint else ""
            tier_tag = f" · tier {r.tier}" if r.tier else ""
            if r.days_since_last is not None:
                meta = f"last touched {r.last_commit_iso} ({r.days_since_last}d ago)"
            else:
                meta = f"status: {r.status or '—'}"
            lines.append(f"- {note_link}{sprint}{tier_tag} — {meta}")
            if r.impl_files:
                files_str = ", ".join(f"`{f}`" for f in r.impl_files[:4])
                more = f" (+{len(r.impl_files)-4})" if len(r.impl_files) > 4 else ""
                lines.append(f"    - impl: {files_str}{more}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🔁 Manutenção")
    lines.append("")
    lines.append(
        "1. **Decay candidates**: abrir SKL note + git blame impl. Decidir "
        "`status: deprecated` no frontmatter ou re-investir.\n"
        "2. **Backlog antigos** (>60d): demote para `tier_C` ou archive.\n"
        "3. **Active sem decay tracking**: nada a fazer."
    )
    lines.append("")
    lines.append(f"Gerado por `python -m agents.skill_scout` em {datetime.now().isoformat(timespec='seconds')}.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(prog="agents.skill_scout", description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Print summary, no file write")
    ap.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = ap.parse_args()

    records = scan_skills()
    today = date.today().isoformat()

    if args.json:
        print(json.dumps([asdict(r) for r in records], indent=2, ensure_ascii=False))
        return 0

    md = render_md(records, today)

    if args.dry_run:
        counts: dict[str, int] = {}
        for r in records:
            counts[r.bucket] = counts.get(r.bucket, 0) + 1
        print(f"[dry-run] {len(records)} skills scanned")
        for k, v in sorted(counts.items()):
            print(f"  {k}: {v}")
        return 0

    out_path = SKILLS_DIR / OUT_PATTERN.format(date=today)
    out_path.write_text(md, encoding="utf-8")
    print(f"[OK] wrote {out_path.relative_to(ROOT).as_posix()} ({len(records)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
