"""Data health monitor | derives availability + cache stats from logs/fetchers_fallback.log.

Lê a log JSON line-by-line (1 linha = 1 attempt do wrapper) e cruza com cache stats.
Output:
  - API availability % por (market, kind, source) na janela de tempo.
  - Cache hit rate global e por kind.
  - Top failing sources (>20% fail rate).
  - Latency p50/p95/p99 por source.
  - Stale ratio (entries_stale / entries_total).

Sem dependências externas (lê só log + SQLite cache).

Uso:
    python -m analytics.data_health [--days 7] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "logs" / "fetchers_fallback.log"


def _percentile(sorted_vals: list[float], p: float) -> float | None:
    if not sorted_vals:
        return None
    idx = max(0, min(len(sorted_vals) - 1, int(p / 100 * len(sorted_vals))))
    return sorted_vals[idx]


def parse_log(days: int = 7) -> list[dict]:
    """Read last N days of fetchers_fallback log."""
    if not LOG_PATH.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    rows: list[dict] = []
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = rec.get("ts")
            if ts:
                try:
                    rec_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if rec_dt < cutoff:
                        continue
                    rec["_ts_dt"] = rec_dt
                except ValueError:
                    pass
            rows.append(rec)
    return rows


def availability_by_source(rows: list[dict]) -> dict[str, dict[str, Any]]:
    """Per (market/kind/source): {attempts, ok, fail, ok_rate, p50_ms, p95_ms}."""
    buckets: dict[tuple[str, str, str], dict[str, list]] = defaultdict(
        lambda: {"ok": [], "fail": [], "skipped": []}
    )
    for r in rows:
        market = r.get("market", "?")
        kind = r.get("kind", "?")
        source = r.get("source", "?")
        status = r.get("status", "?")
        latency = r.get("latency_ms")
        key = (market, kind, source)
        if status in ("ok", "cache_fresh", "cache_stale"):
            buckets[key]["ok"].append(latency or 0)
        elif status == "fail":
            buckets[key]["fail"].append(latency or 0)
        elif status == "skipped":
            buckets[key]["skipped"].append(latency or 0)
    out: dict[str, dict[str, Any]] = {}
    for (m, k, s), bag in buckets.items():
        ok_n, fail_n, skip_n = len(bag["ok"]), len(bag["fail"]), len(bag["skipped"])
        attempts = ok_n + fail_n + skip_n
        all_lat = sorted(bag["ok"] + bag["fail"])
        out[f"{m}/{k}/{s}"] = {
            "attempts": attempts,
            "ok": ok_n,
            "fail": fail_n,
            "skipped": skip_n,
            "ok_rate": round(ok_n / attempts * 100, 1) if attempts else 0,
            "p50_ms": _percentile(all_lat, 50),
            "p95_ms": _percentile(all_lat, 95),
            "p99_ms": _percentile(all_lat, 99),
        }
    return dict(sorted(out.items()))


def cache_metrics(rows: list[dict]) -> dict[str, Any]:
    """Cache hit rate from cache_fresh/cache_stale events vs total fetches."""
    cache_fresh = sum(1 for r in rows if r.get("status") == "cache_fresh")
    cache_stale = sum(1 for r in rows if r.get("status") == "cache_stale")
    api_ok = sum(1 for r in rows if r.get("status") == "ok")
    api_fail = sum(1 for r in rows if r.get("status") == "fail")
    total = cache_fresh + cache_stale + api_ok + api_fail
    return {
        "api_ok": api_ok,
        "api_fail": api_fail,
        "cache_fresh_hits": cache_fresh,
        "cache_stale_hits": cache_stale,
        "total_resolutions": total,
        "cache_hit_rate_pct": round(
            (cache_fresh + cache_stale) / total * 100, 1
        ) if total else 0,
        "api_success_rate_pct": round(api_ok / (api_ok + api_fail) * 100, 1)
        if (api_ok + api_fail) else 0,
    }


def top_errors(rows: list[dict], n: int = 10) -> list[dict]:
    """Most common error messages."""
    counts: dict[tuple[str, str, str, str], int] = defaultdict(int)
    for r in rows:
        if r.get("status") == "fail":
            key = (
                r.get("market", "?"),
                r.get("kind", "?"),
                r.get("source", "?"),
                (r.get("error") or "")[:80],
            )
            counts[key] += 1
    sorted_errs = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return [
        {"market": k[0], "kind": k[1], "source": k[2], "error": k[3], "count": v}
        for k, v in sorted_errs
    ]


def cache_db_stats() -> dict[str, Any]:
    try:
        from fetchers import _cache as cache_mod
        return cache_mod.stats()
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def alerts(report: dict[str, Any]) -> list[str]:
    """Surface anomalies. Return list of human-readable warning strings."""
    out: list[str] = []
    for name, stats in report["availability"].items():
        if stats["attempts"] >= 5 and stats["ok_rate"] < 80:
            out.append(
                f"[!] {name}: ok_rate={stats['ok_rate']}% (attempts={stats['attempts']})"
            )
        if stats.get("p95_ms") and stats["p95_ms"] > 10000:
            out.append(f"[!] {name}: p95 latency {stats['p95_ms']}ms (>10s)")
    cache = report["cache"]
    if cache["total_resolutions"] >= 20 and cache["cache_hit_rate_pct"] > 50:
        out.append(
            f"[i] Cache hit rate elevado ({cache['cache_hit_rate_pct']}%) | APIs falham muito"
        )
    return out


def report(days: int = 7) -> dict[str, Any]:
    rows = parse_log(days=days)
    out = {
        "window_days": days,
        "log_events": len(rows),
        "availability": availability_by_source(rows),
        "cache": cache_metrics(rows),
        "top_errors": top_errors(rows),
        "cache_db": cache_db_stats(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    out["alerts"] = alerts(out)
    return out


def render_text(rep: dict[str, Any]) -> str:
    lines = [
        f"Data Health Report | last {rep['window_days']}d ({rep['log_events']} events)",
        "",
        "## API availability",
    ]
    for name, s in rep["availability"].items():
        lat = (
            f"p50={s['p50_ms']}ms p95={s['p95_ms']}ms"
            if s.get("p50_ms") is not None else "no latency data"
        )
        lines.append(
            f"  {name}: {s['ok']}/{s['attempts']} ok "
            f"({s['ok_rate']}%) | {lat}"
        )
    lines += ["", "## Cache"]
    c = rep["cache"]
    lines += [
        f"  api_ok={c['api_ok']}  api_fail={c['api_fail']}  "
        f"cache_fresh={c['cache_fresh_hits']}  cache_stale={c['cache_stale_hits']}",
        f"  api_success_rate={c['api_success_rate_pct']}%  "
        f"cache_hit_rate={c['cache_hit_rate_pct']}%",
    ]
    cdb = rep["cache_db"]
    if "error" not in cdb:
        lines += [
            f"  cache_db: total={cdb.get('entries_total')} "
            f"fresh={cdb.get('entries_fresh')} stale={cdb.get('entries_stale')}",
            f"  by_kind: {cdb.get('by_kind')}",
        ]
    lines += ["", "## Top errors"]
    for e in rep["top_errors"]:
        lines.append(
            f"  x{e['count']:>3}  {e['market']}/{e['kind']}/{e['source']}: {e['error']}"
        )
    if rep["alerts"]:
        lines += ["", "## Alerts"]
        lines.extend(f"  {a}" for a in rep["alerts"])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true", help="raw JSON output")
    args = ap.parse_args()
    rep = report(days=args.days)
    if args.json:
        print(json.dumps(rep, indent=2, default=str))
    else:
        print(render_text(rep))
    return 0 if not rep["alerts"] else 1


if __name__ == "__main__":
    sys.exit(main())
