"""Cross-source fundamentals validator (Block B).

Compares yfinance vs FMP fundamentals for US tickers and flags discrepancies
exceeding tolerance. Persists as anomalies (kind=CROSS_SOURCE_FUND).

Why: yfinance has known systematic bugs in some metrics (DY occasionally
inflated, ROE occasionally negative-then-positive across reload). FMP is a
genuine second source for the same numbers. When they agree -> high
confidence. When they disagree -> we surface the question, don't silently
trust either.

KNOWN LIMITATION (2026-05-08): FMP free tier returns 402 Payment Required on
`/stable/ratios-ttm` and `/stable/key-metrics-ttm` (paid endpoints). The free
tier only covers analyst consensus + profile. So in current state, this
detector emits warnings ("fmp fetch failed: 402") for every US ticker —
correct behaviour, but not actionable until either:
  - FMP plan upgraded to Starter (~$15/mo, unlocks ratios + key-metrics), OR
  - A different free fundamentals source is wired (investidor10 scrape,
    finnhub free tier ~60/min, brapi re-evaluation).
The detector is shipped now so the integration is ready when a source lands.

Scope:
- US: yfinance vs FMP. Today: gated by FMP plan tier. Future: any /fundamentals
  source registered in fetchers/_clients.py.
- BR: yfinance is the only fundamentals source today. --br-note flag emits
  informational entries; default off (avoids polluting daily anomalies feed).

Budget:
- FMP free tier 250/day. This module calls 2 endpoints per ticker.
- Default: holdings only (~22 US holdings -> ~44 calls/run).
- Opt-in --watchlist roughly doubles cost (~218 calls).
- Gates on agents._budget.fmp_can_call() before each call; aborts gracefully
  if quota exhausted (records partial result + logs).

Tolerances (relative deltas vs the larger of the two values):
- PE ratio: 25% warn, 50% alert
- ROE: 30% warn, 60% alert
- DY: 40% warn, 80% alert (tiny absolute values amplify noise)
- Either side null/zero -> skip metric (not a discrepancy, just missing data)

Output: same Anomaly shape as analytics.data_anomalies. Run via:
    python -m analytics.cross_source_check                # holdings only
    python -m analytics.cross_source_check --watchlist    # include watchlist
    python -m analytics.cross_source_check --json         # machine-readable
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_US = ROOT / "data" / "us_investments.db"
DB_BR = ROOT / "data" / "br_investments.db"
OUT_PATH = ROOT / "data" / "cross_source_anomalies.json"

UTC = timezone.utc

PE_WARN = 0.25
PE_ALERT = 0.50
ROE_WARN = 0.30
ROE_ALERT = 0.60
DY_WARN = 0.40
DY_ALERT = 0.80


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _rel_delta(a: float | None, b: float | None) -> float | None:
    """Relative absolute delta = |a-b| / max(|a|, |b|). None if either invalid."""
    if a is None or b is None:
        return None
    if a == 0 and b == 0:
        return 0.0
    denom = max(abs(a), abs(b))
    if denom == 0:
        return None
    return abs(a - b) / denom


def _classify(delta: float | None, warn: float, alert: float) -> str | None:
    if delta is None:
        return None
    if delta >= alert:
        return "alert"
    if delta >= warn:
        return "warn"
    return None


def _list_us_tickers(conn: sqlite3.Connection, *, holdings_only: bool) -> list[str]:
    where = "WHERE is_holding = 1" if holdings_only else ""
    rows = conn.execute(f"SELECT ticker FROM companies {where} ORDER BY ticker").fetchall()
    return [r[0] for r in rows]


def _yf_fundamentals(conn: sqlite3.Connection, ticker: str) -> dict | None:
    """Latest row from `fundamentals` table for this ticker."""
    row = conn.execute(
        """SELECT period_end, pe, pb, dy, roe, eps, bvps
           FROM fundamentals
           WHERE ticker = ?
           ORDER BY period_end DESC
           LIMIT 1""",
        (ticker,),
    ).fetchone()
    if not row:
        return None
    return {
        "period_end": row[0],
        "pe": row[1],
        "pb": row[2],
        "dy": row[3],
        "roe": row[4],
        "eps": row[5],
        "bvps": row[6],
    }


def detect_cross_source_us(*, holdings_only: bool = True,
                           max_calls: int = 220) -> list[dict]:
    """Compare yfinance vs FMP for each US ticker. Returns list of anomaly dicts.

    max_calls is a hard ceiling on FMP API calls per run (~2 calls per ticker).
    Default 220 keeps us under the 250/day FMP free-tier cap with headroom.
    """
    from agents._budget import fmp_can_call, fmp_record_call
    from fetchers._clients import fmp as get_fmp_client

    fmp = get_fmp_client()
    if not fmp.is_available():
        return [{
            "market": "us", "ticker": "*ALL*", "kind": "CROSS_SOURCE_FUND",
            "severity": "warn", "detected_at": _now_iso(),
            "detail": {"reason": "FMP_API_KEY not configured; cross-source check skipped"},
        }]

    anomalies: list[dict] = []
    calls_made = 0
    if not DB_US.exists():
        return anomalies
    with sqlite3.connect(DB_US) as conn:
        tickers = _list_us_tickers(conn, holdings_only=holdings_only)
        for ticker in tickers:
            yf = _yf_fundamentals(conn, ticker)
            if not yf:
                continue
            # Each FMP call to get_fundamentals is 2 underlying HTTP calls
            if calls_made + 2 > max_calls:
                anomalies.append({
                    "market": "us", "ticker": ticker, "kind": "CROSS_SOURCE_FUND",
                    "severity": "warn", "detected_at": _now_iso(),
                    "detail": {"reason": f"max_calls cap ({max_calls}) reached; remaining tickers skipped"},
                })
                break
            ok, why = fmp_can_call()
            if not ok:
                anomalies.append({
                    "market": "us", "ticker": ticker, "kind": "CROSS_SOURCE_FUND",
                    "severity": "warn", "detected_at": _now_iso(),
                    "detail": {"reason": f"fmp budget gated: {why}"},
                })
                break
            try:
                fmp_data = fmp.get_fundamentals(ticker)
                fmp_record_call()
                calls_made += 2  # ratios + key-metrics
            except Exception as e:
                anomalies.append({
                    "market": "us", "ticker": ticker, "kind": "CROSS_SOURCE_FUND",
                    "severity": "warn", "detected_at": _now_iso(),
                    "detail": {"reason": f"fmp fetch failed: {e}"},
                })
                fmp_record_call()  # still costs quota even on partial fail
                calls_made += 1
                continue

            for metric, warn_t, alert_t in (
                ("pe", PE_WARN, PE_ALERT),
                ("roe", ROE_WARN, ROE_ALERT),
                ("dy", DY_WARN, DY_ALERT),
            ):
                yf_v = yf.get(metric)
                fmp_v = fmp_data.get(metric)
                # FMP DY is a fraction (0.018 = 1.8%); yfinance may be too. Both
                # are "expected fraction" by our convention. If fmp returns >1
                # it's percent format -> normalise.
                if metric == "dy" and isinstance(fmp_v, (int, float)) and fmp_v > 1.5:
                    fmp_v = fmp_v / 100.0
                delta = _rel_delta(yf_v, fmp_v)
                sev = _classify(delta, warn_t, alert_t)
                if sev is None:
                    continue
                anomalies.append({
                    "market": "us", "ticker": ticker, "kind": "CROSS_SOURCE_FUND",
                    "severity": sev, "detected_at": _now_iso(),
                    "detail": {
                        "metric": metric,
                        "yfinance": yf_v,
                        "fmp": fmp_v,
                        "rel_delta": round(delta, 4),
                        "yf_period_end": yf.get("period_end"),
                    },
                })
    return anomalies


def detect_cross_source_br() -> list[dict]:
    """BR cross-source: today, no second public source for fundamentals.

    Emits a single informational note per BR ticker held that we are
    single-source (so calibration tooling can tag confidence accordingly).
    """
    if not DB_BR.exists():
        return []
    out: list[dict] = []
    with sqlite3.connect(DB_BR) as conn:
        tickers = _list_us_tickers(conn, holdings_only=True)  # function works for both
    for ticker in tickers:
        out.append({
            "market": "br", "ticker": ticker, "kind": "CROSS_SOURCE_FUND",
            "severity": "info", "detected_at": _now_iso(),
            "detail": {
                "reason": "single-source: only yfinance covers BR fundamentals today",
                "todo": "wire investidor10 (Playwright) or re-evaluate brapi to triangulate",
            },
        })
    return out


def scan(*, holdings_only: bool = True, max_calls: int = 220, include_br_note: bool = True) -> dict:
    anomalies: list[dict] = detect_cross_source_us(
        holdings_only=holdings_only, max_calls=max_calls,
    )
    if include_br_note:
        anomalies += detect_cross_source_br()
    by_severity: dict[str, int] = {}
    by_metric: dict[str, int] = {}
    for a in anomalies:
        by_severity[a["severity"]] = by_severity.get(a["severity"], 0) + 1
        m = a["detail"].get("metric")
        if m:
            by_metric[m] = by_metric.get(m, 0) + 1
    return {
        "generated_at": _now_iso(),
        "params": {"holdings_only": holdings_only, "max_calls": max_calls},
        "totals": {
            "all": len(anomalies),
            "by_severity": by_severity,
            "by_metric": by_metric,
        },
        "anomalies": anomalies,
    }


def render_text(report: dict) -> str:
    lines = [
        f"Cross-source fundamentals | generated_at={report['generated_at']}",
        f"params: {report['params']}",
        f"totals: {report['totals']}",
        "",
    ]
    if not report["anomalies"]:
        lines.append("(no anomalies)")
        return "\n".join(lines)
    # Order: critical alerts first, then warns, then infos
    sev_order = {"alert": 0, "warn": 1, "info": 2}
    for a in sorted(report["anomalies"], key=lambda x: sev_order.get(x["severity"], 9)):
        d = a["detail"]
        ref = f"{a['market']}/{a['ticker']}"
        sev = a["severity"]
        if "metric" in d:
            lines.append(
                f"  [{sev:5}] {ref:<10} {d['metric']:<4} "
                f"yf={d['yfinance']}  fmp={d['fmp']}  rel={d['rel_delta']*100:.1f}%"
            )
        else:
            lines.append(f"  [{sev:5}] {ref:<10} {d.get('reason', '?')}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(prog="analytics.cross_source_check", description=__doc__.splitlines()[0])
    ap.add_argument("--watchlist", action="store_true",
                    help="Include US watchlist (default holdings only). Costs ~5x more FMP budget.")
    ap.add_argument("--max-calls", type=int, default=220,
                    help="Hard ceiling on FMP calls per run (default 220 = ~110 tickers).")
    ap.add_argument("--no-br-note", action="store_true",
                    help="Skip the BR single-source informational notes.")
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    ap.add_argument("--write", action="store_true",
                    help=f"Write report JSON to {OUT_PATH.relative_to(ROOT)}.")
    args = ap.parse_args()

    report = scan(
        holdings_only=not args.watchlist,
        max_calls=args.max_calls,
        include_br_note=not args.no_br_note,
    )

    if args.write:
        OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"[OK] wrote {OUT_PATH.relative_to(ROOT).as_posix()}")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
