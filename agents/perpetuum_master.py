"""Perpetuum Master — runner that executes all registered perpetuums.

Uso:
    python agents/perpetuum_master.py              # all perpetuums
    python agents/perpetuum_master.py --only vault # só um
    python agents/perpetuum_master.py --dry-run    # simula, não grava

Output:
  - perpetuum_health table populated
  - perpetuum_run_log updated
  - Human-readable summary to stdout
  - (future) Telegram digest when alerts > 0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Force stdout/stderr to UTF-8 — Windows console default cp1252 chokes on emoji/arrows.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum import get_all, get_by_name
from agents._heartbeat import run_heartbeat, format_summary as fmt_heartbeat


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="Run só o perpetuum com este nome")
    ap.add_argument("--date", help="ISO date (default: today)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--skip-heartbeat", action="store_true",
                    help="Skip HEARTBEAT.md checklist execution")
    args = ap.parse_args()

    # Heartbeat first — ad-hoc tasks before scheduled perpetuums.
    if not args.skip_heartbeat:
        hb = run_heartbeat(dry_run=args.dry_run)
        print(fmt_heartbeat(hb))
        if hb.get("failed", 0) > 0 and args.verbose:
            for item in hb.get("items", []):
                if item.get("ok") is False:
                    print(f"  FAIL: {item.get('body')} (exit={item.get('exit')})")
        print()

    registry = get_all()
    if args.only:
        p = get_by_name(args.only)
        if p is None:
            print(f"Unknown perpetuum: {args.only}")
            print(f"Available: {list(registry.keys())}")
            sys.exit(1)
        targets = {args.only: p}
    else:
        targets = registry

    print(f"=== Perpetuum Master ===")
    print(f"Running {len(targets)} perpetuum(s): {list(targets.keys())}")
    if args.dry_run:
        print("(DRY RUN — no DB writes)")
    print()

    total_subjects = 0
    total_alerts = 0
    total_errors = 0

    for name, perp in targets.items():
        if not getattr(perp, "enabled", True):
            print(f"--- [{name}] FROZEN (enabled=False) — skipping")
            print()
            continue
        print(f"--- [{name}] {perp.description}")
        summary = perp.run(run_date=args.date, dry_run=args.dry_run)
        print(f"    subjects={summary['subjects']} alerts={summary['alerts']} "
              f"errors={len(summary['errors'])} duration={summary['duration_sec']:.2f}s")

        # Show worst-5 per perpetuum
        results = summary["results"]
        scored = [r for r in results if r["score"] >= 0]
        if scored:
            worst = sorted(scored, key=lambda r: r["score"])[:5]
            print(f"    worst-5:")
            for r in worst:
                hint = f" | hint: {r['action_hint']}" if r.get("action_hint") else ""
                print(f"      {r['subject']:<40}  score={r['score']:>3}  flags={r['flags']}{hint}")

        if args.verbose and summary["errors"]:
            print(f"    errors:")
            for e in summary["errors"][:3]:
                print(f"      - {e}")

        total_subjects += summary["subjects"]
        total_alerts += summary["alerts"]
        total_errors += len(summary["errors"])
        print()

    print(f"=== Summary ===")
    print(f"Perpetuums run: {len(targets)}")
    print(f"Total subjects scored: {total_subjects}")
    print(f"Total decay alerts: {total_alerts}")
    print(f"Total errors: {total_errors}")


if __name__ == "__main__":
    main()
