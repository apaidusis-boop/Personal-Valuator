"""Wiki lint — enforce memory-wiki bridge schema (source_class, confidence, freshness_check).

Read-only by default. With --apply-defaults, bulk-adds missing fields with
conservative defaults (idempotent, never overwrites existing values).

Cadence defaults (per type) for staleness check:
  macro/cycle/method/playbook : 90d
  holding                      : 30d
  sector                       : 60d
  default                      : 90d

Usage:
  python scripts/wiki_lint.py                   # full report
  python scripts/wiki_lint.py --stale           # only stale-freshness items
  python scripts/wiki_lint.py --missing-source  # only no source_class
  python scripts/wiki_lint.py --apply-defaults  # bulk-add defaults (write)
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "obsidian_vault" / "wiki"

CADENCE_DAYS = {
    "macro": 90, "cycle": 90, "method": 90, "playbook": 180,
    "holding": 30, "sector": 60, "tax": 180, "history": 365,
}
DEFAULT_CADENCE = 90

REQUIRED = ["type", "name"]
RECOMMENDED = ["source_class", "confidence", "freshness_check"]

DEFAULT_SOURCE_CLASS_BY_TYPE = {
    "macro": "derived",
    "cycle": "derived",
    "method": "founder",  # frameworks são curados pelo founder
    "playbook": "founder",
    "sector": "derived",
    "holding": "yfinance",
    "tax": "founder",
    "history": "derived",
}


def _parse_frontmatter(text: str) -> tuple[dict, int, int]:
    """Return (parsed_dict, frontmatter_start_line, frontmatter_end_line).
    Returns ({}, -1, -1) if no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, -1, -1
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end == -1:
        return {}, -1, -1
    fm: dict = {}
    for line in lines[1:end]:
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            fm[k] = v
    return fm, 0, end


def _is_stale(freshness: str, note_type: str) -> tuple[bool, int]:
    cadence = CADENCE_DAYS.get(note_type, DEFAULT_CADENCE)
    try:
        d = date.fromisoformat(freshness)
    except ValueError:
        return True, -1
    age_days = (date.today() - d).days
    return age_days > cadence, age_days


def lint_one(path: Path, opts: argparse.Namespace) -> dict:
    out = {
        "path": str(path.relative_to(ROOT)),
        "missing_required": [],
        "missing_recommended": [],
        "stale": False,
        "stale_age_days": None,
        "notes": [],
    }
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        out["notes"].append(f"read_error: {e}")
        return out

    fm, _, _ = _parse_frontmatter(text)
    if not fm:
        out["notes"].append("no_frontmatter")
        return out

    for k in REQUIRED:
        if not fm.get(k):
            out["missing_required"].append(k)
    for k in RECOMMENDED:
        if not fm.get(k):
            out["missing_recommended"].append(k)

    if fm.get("freshness_check"):
        note_type = fm.get("type", "")
        stale, age = _is_stale(fm["freshness_check"], note_type)
        out["stale"] = stale
        out["stale_age_days"] = age

    out["fm"] = fm
    return out


def apply_defaults_one(path: Path, lint_result: dict) -> bool:
    """Add default source_class / confidence / freshness_check (today) and
    derive missing `name` from filename if needed. Never overwrites existing.
    Returns True if file modified."""
    needs_recommended = bool(lint_result["missing_recommended"])
    needs_name = "name" in lint_result["missing_required"]
    if not needs_recommended and not needs_name:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False
    fm, _, end = _parse_frontmatter(text)
    if end == -1:
        return False

    note_type = fm.get("type", "")
    additions: list[str] = []
    if needs_name:
        # Filename → human-readable: "Pulp_cycle" → "Pulp cycle"
        derived_name = path.stem.replace("_", " ").replace("-", " ")
        additions.append(f"name: {derived_name}")
    if "source_class" in lint_result["missing_recommended"]:
        default_src = DEFAULT_SOURCE_CLASS_BY_TYPE.get(note_type, "derived")
        additions.append(f"source_class: {default_src}")
    if "confidence" in lint_result["missing_recommended"]:
        # Conservative default: 0.7 = secondary-source confidence
        additions.append("confidence: 0.7")
    if "freshness_check" in lint_result["missing_recommended"]:
        additions.append(f"freshness_check: {date.today().isoformat()}")

    if not additions:
        return False

    lines = text.splitlines()
    # Insert before closing --- of frontmatter
    new_lines = lines[:end] + additions + lines[end:]
    path.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale", action="store_true",
                    help="Only report notes with stale freshness_check")
    ap.add_argument("--missing-source", action="store_true",
                    help="Only report notes missing source_class")
    ap.add_argument("--apply-defaults", action="store_true",
                    help="Bulk-add missing recommended fields (writes files)")
    args = ap.parse_args()

    if not WIKI_DIR.exists():
        print(f"wiki dir not found: {WIKI_DIR}")
        return 1

    files = sorted(WIKI_DIR.rglob("*.md"))
    files = [f for f in files if not f.name.startswith("_")]  # skip _SCHEMA, _LAYER, etc

    total = len(files)
    n_missing_req = 0
    n_missing_rec = 0
    n_stale = 0
    n_modified = 0

    print(f"Scanning {total} wiki notes in {WIKI_DIR}\n")
    for f in files:
        r = lint_one(f, args)
        if r["missing_required"]:
            n_missing_req += 1
        if r["missing_recommended"]:
            n_missing_rec += 1
        if r["stale"]:
            n_stale += 1

        # Filter output
        if args.stale and not r["stale"]:
            continue
        if args.missing_source and "source_class" not in r["missing_recommended"]:
            continue

        flags = []
        if r["missing_required"]:
            flags.append(f"required-missing:{r['missing_required']}")
        if r["missing_recommended"]:
            flags.append(f"recommended-missing:{r['missing_recommended']}")
        if r["stale"]:
            flags.append(f"stale:{r['stale_age_days']}d")
        if r["notes"]:
            flags.append(f"notes:{r['notes']}")
        if flags:
            print(f"  - {r['path']}: {' | '.join(flags)}")

        if args.apply_defaults:
            if apply_defaults_one(f, r):
                n_modified += 1
                print(f"      ↳ patched")

    print()
    print(f"=== Summary ===")
    print(f"Total notes: {total}")
    print(f"Missing required fields: {n_missing_req}")
    print(f"Missing recommended fields: {n_missing_rec}")
    print(f"Stale freshness_check: {n_stale}")
    if args.apply_defaults:
        print(f"Modified: {n_modified}")
    return 0 if n_missing_req == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
