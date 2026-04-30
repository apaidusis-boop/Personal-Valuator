"""Heartbeat checklist executor — reads HEARTBEAT.md, runs `>>` prefixed shell items, marks done.

OpenClaw pattern: vault file `obsidian_vault/workspace/HEARTBEAT.md` is the human-editable
checklist of ad-hoc tasks beyond the static schedule in config/agents.yaml.

Format:
    - [ ] >> python scripts/foo.py        ← runs as subprocess
    - [ ] verificar X                     ← logged, not executed
    - nota: ...                           ← ignored (no checkbox)

Done items get `- [x]` and a trailing `<!-- ran ISO_TS, exit=N -->` comment.
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEARTBEAT_PATH = ROOT / "obsidian_vault" / "workspace" / "HEARTBEAT.md"
DEFAULT_TIMEOUT_SEC = 300

PENDING_PATTERN = re.compile(r"^(\s*)- \[ \] (.+?)\s*$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_heartbeat(*, dry_run: bool = False, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> dict:
    """Execute pending checklist items in HEARTBEAT.md.

    Returns dict with counts: {file_exists, total_pending, executed, ok, failed, logged_only}.
    Mutates HEARTBEAT.md in place (idempotent — re-runs skip already-checked items).
    """
    summary = {
        "file_exists": HEARTBEAT_PATH.exists(),
        "total_pending": 0,
        "executed": 0,
        "ok": 0,
        "failed": 0,
        "logged_only": 0,
        "items": [],
    }
    if not HEARTBEAT_PATH.exists():
        return summary

    try:
        original = HEARTBEAT_PATH.read_text(encoding="utf-8")
    except Exception as e:
        summary["error"] = f"read: {e}"
        return summary

    lines = original.splitlines()
    new_lines: list[str] = []
    changed = False
    in_fence = False  # skip pending items inside ``` fenced blocks

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            new_lines.append(line)
            continue
        if in_fence:
            new_lines.append(line)
            continue
        m = PENDING_PATTERN.match(line)
        if not m:
            new_lines.append(line)
            continue

        indent, body = m.group(1), m.group(2).strip()
        summary["total_pending"] += 1

        if not body.startswith(">>"):
            summary["logged_only"] += 1
            summary["items"].append({"body": body, "kind": "note", "ok": None})
            new_lines.append(line)
            continue

        cmd = body[2:].strip()
        if not cmd:
            new_lines.append(line)
            continue

        if dry_run:
            summary["items"].append({"body": cmd, "kind": "shell", "ok": "dry-run"})
            new_lines.append(line)
            continue

        try:
            r = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=timeout_sec, cwd=str(ROOT),
            )
            exit_code = r.returncode
            ok = (exit_code == 0)
        except subprocess.TimeoutExpired:
            exit_code = -1
            ok = False
        except Exception:
            exit_code = -2
            ok = False

        summary["executed"] += 1
        if ok:
            summary["ok"] += 1
        else:
            summary["failed"] += 1
        summary["items"].append({
            "body": cmd, "kind": "shell", "ok": ok, "exit": exit_code,
        })

        marker = "x" if ok else " "  # leave failed unchecked so user retries
        ts = _now_iso()
        new_line = f"{indent}- [{marker}] >> {cmd}  <!-- ran {ts}, exit={exit_code} -->"
        new_lines.append(new_line)
        changed = True

    if changed and not dry_run:
        HEARTBEAT_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return summary


def format_summary(s: dict) -> str:
    if not s.get("file_exists"):
        return "heartbeat: HEARTBEAT.md not found (skipped)"
    if s["total_pending"] == 0:
        return "heartbeat: no pending items"
    return (f"heartbeat: {s['total_pending']} pending "
            f"({s['executed']} executed: {s['ok']} ok, {s['failed']} failed, "
            f"{s['logged_only']} notes)")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SEC)
    args = ap.parse_args()
    s = run_heartbeat(dry_run=args.dry_run, timeout_sec=args.timeout)
    print(format_summary(s))
    for item in s.get("items", []):
        print(f"  - {item}")
