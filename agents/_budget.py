"""Per-ticker daily budget rotation for paid-API buckets.

Phase HH-AOW shipped *bucket-level* quotas (Tavily 100/day split 30/30/25/15
across hourly_autoresearch / daily_wires / reactive / manual). What it didn't
solve: WHICH of the ~189 tickers gets a slot on any given day.

This module fills that gap. Given a bucket and a pool of candidate tickers,
it returns a deterministic per-day slice that:

1. **Prioritises holdings over watchlist** — every holding is touched at least
   every `holdings_cycle_days` (default 1, so daily). Watchlist rotates more
   slowly to fit the cap.
2. **Reserves headroom for reactive** — if `bucket="reactive"`, no rotation
   slice (pure event-driven; just checks bucket has capacity).
3. **Uses day-ordinal modulo** — fair distribution; same ticker won't be
   repeatedly picked while others starve.

Also adds FMP rate-limit ledger (250/day on /stable/ free tier; 5/sec burst).

Pure stdlib + sqlite + the existing `agents._health` bucket helpers.
No DB writes (only reads companies tables for universe).

CLI:
    python -m agents._budget today              # show per-bucket roster for today
    python -m agents._budget today reactive     # specific bucket
    python -m agents._budget status             # bucket usage + FMP usage
    python -m agents._budget simulate <bucket>  # show 7-day rotation preview
    python -m agents._budget fmp check          # can we make an FMP call?
    python -m agents._budget fmp record         # record an FMP call
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
HEALTH_DIR = ROOT / "data" / "health"
HEALTH_DIR.mkdir(parents=True, exist_ok=True)
FMP_LEDGER = HEALTH_DIR / "fmp_usage.json"

FMP_DAILY_LIMIT = 250  # free tier /stable/ endpoints
FMP_BURST_PER_SEC = 5

# Default per-bucket rotation policy. Reactive is pure event-driven so
# it doesn't have a daily roster (we just gate on bucket capacity).
ROTATION_POLICY = {
    "hourly_autoresearch": {
        "holdings_cycle_days": 2,   # every holding every 2 days
        "watchlist_cycle_days": 14, # every watchlist every 2 weeks
        "max_per_day": 30,           # matches tavily_buckets.yaml cap
    },
    "daily_wires": {
        "holdings_cycle_days": 1,    # every holding daily (variant + earnings)
        "watchlist_cycle_days": 7,
        "max_per_day": 30,
    },
    "manual": {
        "holdings_cycle_days": 30,   # rare; user invokes for specific ticker
        "watchlist_cycle_days": 30,
        "max_per_day": 15,
    },
    # reactive: no rotation; event-driven only. bucket_check still gates.
}


@dataclass(frozen=True)
class Candidate:
    ticker: str
    market: str           # 'br' or 'us'
    is_holding: bool


def _load_universe() -> list[Candidate]:
    """Read companies tables. Holdings flagged via is_holding=1."""
    out: list[Candidate] = []
    for db, mkt in ((DB_BR, "br"), (DB_US, "us")):
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            for row in c.execute("SELECT ticker, COALESCE(is_holding, 0) FROM companies"):
                out.append(Candidate(ticker=row[0], market=mkt, is_holding=bool(row[1])))
    return out


def _day_ordinal(today: date | None = None) -> int:
    today = today or date.today()
    return today.toordinal()


def _slice_for_day(items: list[Candidate], cycle_days: int, day: int) -> list[Candidate]:
    """Round-robin: split items into `cycle_days` buckets, return today's bucket.

    Determinism: same (items, cycle_days, day) always produces same slice.
    Order is preserved within the slice (caller sees ticker A before B if A < B).
    """
    if not items or cycle_days <= 0:
        return []
    if cycle_days == 1:
        return list(items)
    # Sort to make slicing deterministic across runs (if companies table reorders)
    sorted_items = sorted(items, key=lambda x: (not x.is_holding, x.market, x.ticker))
    bucket_idx = day % cycle_days
    # Spread items across buckets: item i goes to bucket i % cycle_days
    return [it for i, it in enumerate(sorted_items) if i % cycle_days == bucket_idx]


def tickers_for_today(
    bucket: str,
    *,
    universe: list[Candidate] | None = None,
    today: date | None = None,
) -> list[Candidate]:
    """Return the deterministic per-day roster for `bucket`.

    Reactive bucket returns empty (event-driven).
    Unknown buckets fall back to holdings-only.
    """
    if bucket == "reactive":
        return []
    universe = universe or _load_universe()
    holdings = [c for c in universe if c.is_holding]
    watchlist = [c for c in universe if not c.is_holding]
    policy = ROTATION_POLICY.get(bucket, ROTATION_POLICY["manual"])
    day = _day_ordinal(today)

    todays_holdings = _slice_for_day(holdings, policy["holdings_cycle_days"], day)
    todays_watchlist = _slice_for_day(watchlist, policy["watchlist_cycle_days"], day)
    combined = todays_holdings + todays_watchlist
    cap = policy["max_per_day"]
    return combined[:cap]


# ---- FMP rate-limit ledger ----

def _read_fmp_ledger() -> dict:
    if not FMP_LEDGER.exists():
        return {"day": date.today().isoformat(), "count": 0, "last_call_ts": 0.0}
    try:
        return json.loads(FMP_LEDGER.read_text(encoding="utf-8"))
    except Exception:
        return {"day": date.today().isoformat(), "count": 0, "last_call_ts": 0.0}


def _write_fmp_ledger(state: dict) -> None:
    FMP_LEDGER.write_text(json.dumps(state, indent=2), encoding="utf-8")


def fmp_can_call() -> tuple[bool, str]:
    """Return (allowed, reason). Enforces 250/day daily cap.

    Note: per-second burst (5/sec) is handled by FMPClient.THROTTLE_SEC
    inside fetchers/_clients.py — we don't double-throttle here.
    """
    state = _read_fmp_ledger()
    today_iso = date.today().isoformat()
    if state.get("day") != today_iso:
        state = {"day": today_iso, "count": 0, "last_call_ts": 0.0}
        _write_fmp_ledger(state)
    if state["count"] >= FMP_DAILY_LIMIT:
        return False, f"daily limit ({FMP_DAILY_LIMIT}) exhausted"
    return True, "ok"


def fmp_record_call() -> None:
    state = _read_fmp_ledger()
    today_iso = date.today().isoformat()
    if state.get("day") != today_iso:
        state = {"day": today_iso, "count": 0, "last_call_ts": 0.0}
    state["count"] = state.get("count", 0) + 1
    state["last_call_ts"] = time.time()
    state["last_call_iso"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    _write_fmp_ledger(state)


def fmp_status() -> dict:
    state = _read_fmp_ledger()
    today_iso = date.today().isoformat()
    if state.get("day") != today_iso:
        return {"day": today_iso, "count": 0, "remaining": FMP_DAILY_LIMIT, "limit": FMP_DAILY_LIMIT}
    used = state.get("count", 0)
    return {
        "day": state.get("day"),
        "count": used,
        "remaining": max(0, FMP_DAILY_LIMIT - used),
        "limit": FMP_DAILY_LIMIT,
        "last_call": state.get("last_call_iso"),
    }


# ---- Convenience: combined budget check ----

def check_bucket(bucket: str) -> tuple[bool, int, int]:
    """Pass-through to agents._health.tavily_bucket_check (backward compat)."""
    from agents._health import tavily_bucket_check
    return tavily_bucket_check(bucket)


def spend_bucket(bucket: str) -> None:
    """Pass-through to agents._health.tavily_bucket_record."""
    from agents._health import tavily_bucket_record
    tavily_bucket_record(bucket)


def _cli() -> int:
    ap = argparse.ArgumentParser(prog="agents._budget", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_today = sub.add_parser("today", help="Print per-day roster")
    p_today.add_argument("bucket", nargs="?", default=None,
                         help="If given, only this bucket; else all rotation buckets")

    sub.add_parser("status", help="Bucket usage + FMP usage")

    p_sim = sub.add_parser("simulate", help="Show 7-day rotation preview for a bucket")
    p_sim.add_argument("bucket")
    p_sim.add_argument("--days", type=int, default=7)

    p_fmp = sub.add_parser("fmp", help="FMP ledger CLI")
    fmp_sub = p_fmp.add_subparsers(dest="fcmd", required=True)
    fmp_sub.add_parser("check")
    fmp_sub.add_parser("record")
    fmp_sub.add_parser("status")

    args = ap.parse_args()

    if args.cmd == "today":
        universe = _load_universe()
        buckets = [args.bucket] if args.bucket else list(ROTATION_POLICY.keys())
        for b in buckets:
            roster = tickers_for_today(b, universe=universe)
            print(f"--- {b} ({len(roster)} tickers) ---")
            for c in roster:
                holding_mark = "*" if c.is_holding else " "
                print(f"  {holding_mark} [{c.market}] {c.ticker}")
        return 0

    if args.cmd == "status":
        from agents._health import _load_bucket_config, _read_bucket_state
        caps = _load_bucket_config()
        state = _read_bucket_state()
        buckets = state.get("buckets", {})
        print("=== Tavily buckets ===")
        for name, cap in caps.items():
            used = buckets.get(name, 0)
            pct = int(used / cap * 100) if cap else 0
            print(f"  {name:25s} {used:3d}/{cap:3d} ({pct:3d}%)")
        print("=== FMP ===")
        st = fmp_status()
        print(f"  count: {st['count']}/{st['limit']} (remaining {st['remaining']})")
        if st.get("last_call"):
            print(f"  last call: {st['last_call']}")
        return 0

    if args.cmd == "simulate":
        universe = _load_universe()
        today = date.today()
        seen_holdings: dict[str, list[int]] = {}
        seen_watchlist: dict[str, list[int]] = {}
        for offset in range(args.days):
            d = date.fromordinal(today.toordinal() + offset)
            roster = tickers_for_today(args.bucket, universe=universe, today=d)
            print(f"day +{offset} ({d.isoformat()}, ord={d.toordinal()}): {len(roster)} tickers")
            for c in roster:
                target = seen_holdings if c.is_holding else seen_watchlist
                target.setdefault(c.ticker, []).append(offset)
        print(f"\nholdings touched: {len(seen_holdings)}/{sum(1 for c in universe if c.is_holding)}")
        print(f"watchlist touched: {len(seen_watchlist)}/{sum(1 for c in universe if not c.is_holding)}")
        return 0

    if args.cmd == "fmp":
        if args.fcmd == "check":
            ok, reason = fmp_can_call()
            print(f"{'OK' if ok else 'BLOCKED'}: {reason}")
            return 0 if ok else 1
        if args.fcmd == "record":
            fmp_record_call()
            st = fmp_status()
            print(f"recorded -> {st['count']}/{st['limit']}")
            return 0
        if args.fcmd == "status":
            print(json.dumps(fmp_status(), indent=2))
            return 0

    return 2


if __name__ == "__main__":
    sys.exit(_cli())
