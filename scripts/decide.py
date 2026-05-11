"""Decision Orchestrator | unified tier-gated action surface.

Consolidates three previously-separate flows into one CLI:

  * `scripts/trigger_monitor.py` — opens rows in watchlist_actions when
    declarative triggers (config/triggers.yaml) fire (T0-T1 user signals).
  * `scripts/action_cli.py` — user marks open rows resolved/ignored/notes.
  * `scripts/perpetuum_action_run.py` — runs whitelisted perpetuum:* commands.

All three drive the SAME table (watchlist_actions in BR+US DBs). This wrapper
adds:

  - **tier**: every open action gets a tier label (T0..T3) computed from kind:
      T0  user_trigger:*           (price/DY trigger — needs human review)
      T1  perpetuum:* observer     (logged only — no action)
      T2  perpetuum:* with hint    (proposes whitelisted command; user approves)
      T3  perpetuum:* auto-runnable (whitelisted + low-risk; can `--auto`)
  - **safety gate**: `approve <ref>` runs the action_hint only if T2/T3 +
    whitelist match; else falls back to manual resolve flow.
  - **scan**: optional first step that runs trigger_monitor before listing.

Uso:
    ii decide                              # list open (default)
    ii decide list [--all] [--tier T2]     # list with filters
    ii decide scan                         # run trigger_monitor + list
    ii decide approve <ref> [--note "..."] # T0=resolve / T2-3=run+resolve
    ii decide ignore <ref> [--note "..."]
    ii decide run <ref>                    # explicit run (T2/T3 only)
    ii decide tier <ref>                   # explain tier + what approve does

Done criterion: `ii decide list` shows tier per row; `ii decide approve <ref>`
either runs the action (T2/T3 whitelisted) OR marks resolved (T0/T1) with a
single command, and the row reflects the new status.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Reuse — never duplicate
from scripts import action_cli  # noqa: E402
from scripts import perpetuum_action_run as par  # noqa: E402
from analytics.format import br_date  # noqa: E402

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


# ============================================================
# Tier classifier — single source of truth
# ============================================================
def classify_tier(kind: str, action_hint: str | None) -> str:
    """Return one of {T0, T1, T2, T3}.

    T0: user-triggered (price/DY) — always needs human review
    T1: perpetuum observer — logged, no hint, nothing to do
    T2: perpetuum with hint, whitelisted — user approves, then runs
    T3: perpetuum with hint NOT whitelisted — manual run only (safer label)
    """
    if not kind:
        return "T0"
    if not kind.startswith("perpetuum:"):
        return "T0"
    hint = (action_hint or "").strip()
    if not hint:
        return "T1"
    if par._is_whitelisted(hint):
        return "T2"
    return "T3"


def tier_explanation(tier: str) -> str:
    return {
        "T0": "user trigger — `approve` resolves with note; no command runs",
        "T1": "perpetuum observer — `approve` resolves; nothing else to run",
        "T2": "perpetuum proposal (whitelisted) — `approve` RUNS the command + marks resolved",
        "T3": "perpetuum proposal (NOT whitelisted) — `approve` will only resolve; run command manually",
    }.get(tier, "unknown")


# ============================================================
# List / display
# ============================================================
def _fetch_open(ticker: str | None = None, kind: str | None = None) -> list[dict]:
    return action_cli._fetch_all(
        status_filter="open", ticker_filter=ticker, kind_filter=kind
    )


def cmd_list(args: argparse.Namespace) -> int:
    rows = action_cli._fetch_all(
        status_filter=None if args.all else "open",
        ticker_filter=args.ticker,
        kind_filter=args.kind,
    )
    if args.tier:
        rows = [r for r in rows
                if classify_tier(r["kind"], r["action_hint"]) == args.tier.upper()]
    if not rows:
        print("[nenhuma action]")
        return 0
    print(f"\n{'REF':<8}  {'TIER':<4}  {'TICKER':<7}  {'STATUS':<9}  "
          f"{'OPENED':<12}  KIND / DETAIL")
    print("-" * 100)
    by_tier: dict[str, int] = {}
    for r in rows:
        tier = classify_tier(r["kind"], r["action_hint"])
        by_tier[tier] = by_tier.get(tier, 0) + 1
        opened = br_date(r["opened_at"])
        ref = f"{r['market']}/{r['id']}"
        detail = action_cli._summarize_snapshot(r["kind"], r["snapshot"])
        print(f"{ref:<8}  {tier:<4}  {r['ticker']:<7}  {r['status']:<9}  "
              f"{opened:<12}  {r['kind']}  ::  {detail}")
        if r["action_hint"] and tier in ("T2", "T3"):
            print(f"           hint: {r['action_hint']}")
        if r["notes"]:
            print(f"           note: {r['notes']}")
    print("-" * 100)
    summary = " · ".join(f"{t}={n}" for t, n in sorted(by_tier.items()))
    print(f"{len(rows)} action(s)  [{summary}]")
    return 0


def cmd_tier(args: argparse.Namespace) -> int:
    mkt, aid = action_cli._parse_ref(args.ref)
    rows = action_cli._fetch_all(status_filter=None, ticker_filter=None, kind_filter=None)
    match = next((r for r in rows
                  if r["id"] == aid and (mkt is None or r["market"] == mkt)), None)
    if not match:
        print(f"[erro] action #{args.ref} não existe")
        return 1
    t = classify_tier(match["kind"], match["action_hint"])
    print(f"ref:    {match['market']}/{match['id']}")
    print(f"kind:   {match['kind']}")
    print(f"tier:   {t}")
    print(f"hint:   {match['action_hint'] or '(none)'}")
    if match["action_hint"]:
        wl = par._is_whitelisted(match["action_hint"])
        print(f"whitelisted: {wl}")
    print(f"behaviour: {tier_explanation(t)}")
    return 0


# ============================================================
# Scan — run trigger_monitor first
# ============================================================
def cmd_scan(args: argparse.Namespace) -> int:
    """Run trigger_monitor (idempotent) then list."""
    import subprocess
    py = sys.executable
    cmd = [py, str(ROOT / "scripts" / "trigger_monitor.py")]
    if args.market:
        cmd += ["--market", args.market]
    if args.dry_run:
        cmd += ["--dry-run"]
    print(f"[scan] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=False)
    if proc.returncode != 0:
        print(f"[scan] trigger_monitor exit={proc.returncode}", file=sys.stderr)
        return proc.returncode
    print()
    list_args = argparse.Namespace(all=False, ticker=None, kind=None, tier=None)
    return cmd_list(list_args)


# ============================================================
# Approve / ignore / run — tier-gated
# ============================================================
def _find_row(ref: str) -> dict | None:
    mkt, aid = action_cli._parse_ref(ref)
    rows = action_cli._fetch_all(status_filter=None, ticker_filter=None, kind_filter=None)
    return next(
        (r for r in rows if r["id"] == aid and (mkt is None or r["market"] == mkt)),
        None,
    )


def cmd_approve(args: argparse.Namespace) -> int:
    """Tier-gated approval.

    T0/T1 → resolve with note (no command runs)
    T2    → run whitelisted command, then resolve
    T3    → reject (manual run required); print exact command for the user
    """
    row = _find_row(args.ref)
    if not row:
        print(f"[erro] action #{args.ref} não existe")
        return 1
    tier = classify_tier(row["kind"], row["action_hint"])
    print(f"[decide] {row['market']}/{row['id']}  tier={tier}  kind={row['kind']}")
    if tier in ("T0", "T1"):
        return action_cli._update(
            args.ref, new_status="resolved",
            note=args.note or f"approved (tier={tier})",
            market_hint=args.market,
        )
    if tier == "T2":
        if args.dry_run:
            print(f"[dry-run] would execute: {row['action_hint']}")
            return 0
        # Delegate to perpetuum_action_run which already does whitelist + capture.
        rc = par.run_action(row["id"], market_hint=row["market"])
        return rc
    # T3: don't auto-run an unwhitelisted command
    print(f"[T3] command not in whitelist; run manually:")
    print(f"   {row['action_hint']}")
    print(f"then: ii decide resolve {args.ref} --note 'manual run ok'")
    return 2


def cmd_ignore(args: argparse.Namespace) -> int:
    return action_cli._update(
        args.ref, new_status="ignored", note=args.note, market_hint=args.market
    )


def cmd_resolve(args: argparse.Namespace) -> int:
    return action_cli._update(
        args.ref, new_status="resolved", note=args.note, market_hint=args.market
    )


def cmd_run(args: argparse.Namespace) -> int:
    """Explicit run for T2/T3 — bypasses tier check beyond whitelist."""
    row = _find_row(args.ref)
    if not row:
        print(f"[erro] action #{args.ref} não existe")
        return 1
    tier = classify_tier(row["kind"], row["action_hint"])
    if tier in ("T0", "T1"):
        print(f"[erro] tier={tier} não tem command para correr; use `decide approve`")
        return 1
    return par.run_action(row["id"], market_hint=row["market"])


# ============================================================
# CLI
# ============================================================
def main() -> int:
    ap = argparse.ArgumentParser(
        prog="ii decide",
        description="Tier-gated action orchestrator (triggers + perpetuum)",
    )
    sub = ap.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="list open actions (default)")
    p_list.add_argument("--all", action="store_true")
    p_list.add_argument("--ticker")
    p_list.add_argument("--kind")
    p_list.add_argument("--tier", choices=["T0", "T1", "T2", "T3", "t0", "t1", "t2", "t3"])
    p_list.set_defaults(func=cmd_list)

    p_scan = sub.add_parser("scan", help="run trigger_monitor then list")
    p_scan.add_argument("--market", choices=["br", "us"])
    p_scan.add_argument("--dry-run", action="store_true")
    p_scan.set_defaults(func=cmd_scan)

    p_t = sub.add_parser("tier", help="explain tier of a ref")
    p_t.add_argument("ref")
    p_t.set_defaults(func=cmd_tier)

    p_app = sub.add_parser("approve", help="approve action (tier-gated)")
    p_app.add_argument("ref")
    p_app.add_argument("--market", choices=["br", "us"])
    p_app.add_argument("--note", default="")
    p_app.add_argument("--dry-run", action="store_true")
    p_app.set_defaults(func=cmd_approve)

    p_ig = sub.add_parser("ignore", help="mark ignored")
    p_ig.add_argument("ref")
    p_ig.add_argument("--market", choices=["br", "us"])
    p_ig.add_argument("--note", default="")
    p_ig.set_defaults(func=cmd_ignore)

    p_res = sub.add_parser("resolve", help="mark resolved (no command run)")
    p_res.add_argument("ref")
    p_res.add_argument("--market", choices=["br", "us"])
    p_res.add_argument("--note", default="")
    p_res.set_defaults(func=cmd_resolve)

    p_run = sub.add_parser("run", help="run T2/T3 command (whitelist still applies)")
    p_run.add_argument("ref")
    p_run.set_defaults(func=cmd_run)

    args = ap.parse_args()
    if args.cmd is None:
        list_args = argparse.Namespace(all=False, ticker=None, kind=None, tier=None)
        return cmd_list(list_args)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
