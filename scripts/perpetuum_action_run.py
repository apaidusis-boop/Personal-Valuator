"""Run an approved perpetuum action.

Uso:
    python scripts/perpetuum_action_run.py <action_id> [--market br|us]
    python scripts/perpetuum_action_run.py list-pending     # show T2 proposals
    python scripts/perpetuum_action_run.py list-open        # all open actions

Safety:
  - Only runs actions with `kind` starting "perpetuum:"
  - Only runs commands in a WHITELIST (extend cautiously)
  - Captures stdout/stderr into notes
  - Marks action 'resolved' (with exit code) or 'ignored' (if whitelist fail)
  - User must pass exact action_id — no batch run in T2

Future (T3+): worktree isolation, batch dry-run, auto-rollback.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}

# WHITELIST de commands que T2 perpetuum pode sugerir auto-run.
# Qualquer comando que não match estes patterns exige edit manual (fail-safe).
ACTION_WHITELIST = [
    re.compile(r"^python\s+fetchers/yf_deep_fundamentals\.py\s+[A-Z0-9.\-]+$"),
    re.compile(r"^python\s+scripts/refresh_ticker\.py\s+[A-Z0-9.\-]+$"),
    re.compile(r"^python\s+fetchers/fred_fetcher\.py(\s+--series\s+[A-Z0-9_]+)?$"),
    # Phase Y.8.5 — RI freshness perpetuum T2 actions
    re.compile(r"^python\s+-m\s+library\.ri\.cvm_filings\s+ingest\s+(dfp|itr|ipe)\s+--year\s+\d{4}(\s+--all-catalog|\s+--ticker\s+[A-Z0-9.\-]+)?$"),
    re.compile(r"^python\s+-m\s+library\.ri\.cvm_filings\s+download\s+(dfp|itr|ipe|fre|fca)\s+--year\s+\d{4}$"),
    re.compile(r"^python\s+-m\s+library\.ri\.cvm_parser\s+build$"),
    re.compile(r"^python\s+-m\s+library\.ri\.quarterly_single\s+build$"),
    re.compile(r"^python\s+-m\s+library\.ri\.compare_releases\s+(--all-catalog|[A-Z0-9.\-]+)$"),
    re.compile(r"^python\s+-m\s+library\.ri\.fii_filings\s+(download|ingest)\s+--year\s+\d{4}(\s+--ticker\s+[A-Z0-9]+)?$"),
]


def _find_action(action_id: int, market_hint: str | None = None) -> tuple[Path, dict] | None:
    markets = [market_hint] if market_hint else ["br", "us"]
    for m in markets:
        db = DBS[m]
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            row = c.execute(
                "SELECT * FROM watchlist_actions WHERE id = ? AND kind LIKE 'perpetuum:%'",
                (action_id,),
            ).fetchone()
            if row:
                return db, dict(row)
    return None


def _is_whitelisted(cmd: str) -> bool:
    cmd = cmd.strip()
    return any(p.match(cmd) for p in ACTION_WHITELIST)


def _mark(db: Path, action_id: int, status: str, note: str) -> None:
    with sqlite3.connect(db) as c:
        c.execute(
            "UPDATE watchlist_actions SET status=?, resolved_at=?, notes=? WHERE id=?",
            (status, datetime.now(UTC).isoformat(timespec="seconds"), note, action_id),
        )
        c.commit()


def run_action(action_id: int, market_hint: str | None = None) -> int:
    found = _find_action(action_id, market_hint)
    if not found:
        print(f"Action {action_id} not found (or not a perpetuum:* action)")
        return 2
    db, action = found

    if action["status"] != "open":
        print(f"Action {action_id} is already {action['status']!r}; nothing to do")
        return 3

    cmd = (action["action_hint"] or "").strip()
    if not cmd:
        print(f"Action {action_id} has no action_hint to execute")
        return 4

    if not _is_whitelisted(cmd):
        print(f"Action {action_id}: command NOT in whitelist")
        print(f"  cmd: {cmd}")
        print(f"  run manually if safe, then: python scripts/action_cli.py resolve {action_id} --note 'manual run: ok'")
        return 5

    print(f"=== Running action {action_id} (perpetuum={action['kind']}) ===")
    print(f"Subject: {action['market']}:{action['ticker']}")
    print(f"Cmd: {cmd}")
    print()

    proc = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, timeout=300)
    note = json.dumps({
        "exit_code": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-500:],
        "stderr_tail": (proc.stderr or "")[-500:],
        "ran_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }, ensure_ascii=False)

    status = "resolved" if proc.returncode == 0 else "ignored"
    _mark(db, action_id, status, note)

    print(f"Exit: {proc.returncode}")
    print(f"Status set: {status}")
    if proc.stdout:
        print(f"\n--- stdout ---\n{proc.stdout[-2000:]}")
    if proc.stderr:
        print(f"\n--- stderr ---\n{proc.stderr[-500:]}")

    return proc.returncode


def list_open(only_perpetuum: bool = True) -> None:
    from agents.perpetuum._actions import list_open_by_perpetuum
    rows = list_open_by_perpetuum() if only_perpetuum else []
    if not rows:
        print("(no open perpetuum actions)")
        return
    print(f"Open perpetuum actions ({len(rows)}):")
    print(f"{'ID':>4}  {'MKT':<3}  {'KIND':<25}  {'SCORE':>5}  {'TICKER':<12}  ACTION_HINT")
    print("-" * 120)
    for r in rows:
        snap = json.loads(r["trigger_snapshot_json"]) if r["trigger_snapshot_json"] else {}
        score = snap.get("score", "?")
        hint = (r["action_hint"] or "")[:60]
        print(f"{r['id']:>4}  {r['market']:<3}  {r['kind']:<25}  {score!s:>5}  {r['ticker'][:12]:<12}  {hint}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", nargs="?", help="action_id, or 'list-pending' / 'list-open'")
    ap.add_argument("--market", choices=["br", "us"])
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT))

    if not args.action or args.action in ("list-pending", "list-open"):
        list_open(only_perpetuum=True)
        return

    try:
        aid = int(args.action)
    except ValueError:
        print(f"Invalid action_id: {args.action}. Use number or 'list-open'.")
        sys.exit(1)

    sys.exit(run_action(aid, args.market))


if __name__ == "__main__":
    main()
