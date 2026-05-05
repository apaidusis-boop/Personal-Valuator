"""Data anomaly detector | scan BR+US DBs for suspicious data.

Three classes of anomaly, all derivable purely from SQL (zero network):

  PRICE_JUMP — daily abs(return) > pct threshold (default 20%)
  PRICE_STALE — no `prices` row for ticker in last N business days
  FUND_STALE — `fundamentals` snapshot older than X days for a holding

Holdings (companies.is_holding=1) are scrutinized stricter than watchlist:
they MUST have fresh fundamentals; watchlist tolerates a longer window.

Output:
  - data/data_anomalies.json  (single source of truth, latest scan)
  - stdout summary

Idempotent: each scan rewrites the JSON file. The JSON has a `generated_at`
field; consumers (Mission Control, captain's log) can compare to detect drift.

Uso:
    python -m analytics.data_anomalies                        # scan + write JSON
    python -m analytics.data_anomalies --json                 # scan + print JSON
    python -m analytics.data_anomalies --price-pct 25         # tweak threshold
    python -m analytics.data_anomalies --no-write             # don't touch JSON file
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
OUT_PATH = ROOT / "data" / "data_anomalies.json"


# ============================================================
# Data structures
# ============================================================
@dataclass
class Anomaly:
    market: str
    ticker: str
    kind: str            # PRICE_JUMP | PRICE_STALE | FUND_STALE
    severity: str        # warn | alert
    detected_at: str
    detail: dict[str, Any] = field(default_factory=dict)


# ============================================================
# Detectors — each returns list[Anomaly]
# ============================================================
def detect_price_jumps(conn: sqlite3.Connection, market: str,
                       pct_threshold: float, lookback_days: int = 7) -> list[Anomaly]:
    """Find tickers with abs(daily return) > pct_threshold in the last lookback_days.

    A 20% one-day move on a holding usually means a corp action (split, spin)
    OR a real price shock. Either way, surface for review.
    """
    since = (datetime.now(UTC).date() - timedelta(days=lookback_days)).isoformat()
    rows = conn.execute(
        """
        WITH ranked AS (
          SELECT ticker, date, close,
                 LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
          FROM prices
          WHERE date >= ?
        )
        SELECT ticker, date, close, prev_close
        FROM ranked
        WHERE prev_close IS NOT NULL AND prev_close > 0
          AND ABS((close - prev_close) / prev_close) >= ?
        ORDER BY date DESC, ticker
        """,
        (since, pct_threshold / 100.0),
    ).fetchall()
    out: list[Anomaly] = []
    for ticker, date, close, prev in rows:
        ret = (close - prev) / prev * 100
        out.append(Anomaly(
            market=market, ticker=ticker, kind="PRICE_JUMP",
            severity="alert" if abs(ret) >= 30 else "warn",
            detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
            detail={
                "date": date,
                "close": round(close, 4),
                "prev_close": round(prev, 4),
                "return_pct": round(ret, 2),
            },
        ))
    return out


def detect_price_stale(conn: sqlite3.Connection, market: str,
                       max_days: int = 5) -> list[Anomaly]:
    """Holdings without a prices row in the last `max_days`."""
    cutoff = (datetime.now(UTC).date() - timedelta(days=max_days)).isoformat()
    rows = conn.execute(
        """
        SELECT c.ticker, MAX(p.date) AS last_date, COUNT(p.date) AS n
        FROM companies c
        LEFT JOIN prices p ON p.ticker = c.ticker
        WHERE c.is_holding = 1
        GROUP BY c.ticker
        HAVING last_date IS NULL OR last_date < ?
        ORDER BY last_date
        """,
        (cutoff,),
    ).fetchall()
    out: list[Anomaly] = []
    for ticker, last_date, n in rows:
        out.append(Anomaly(
            market=market, ticker=ticker, kind="PRICE_STALE",
            severity="alert" if last_date is None else "warn",
            detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
            detail={
                "last_price_date": last_date,
                "rows_total": n,
                "max_age_days": max_days,
            },
        ))
    return out


def detect_fundamentals_stale(conn: sqlite3.Connection, market: str,
                              holdings_max_days: int = 100,
                              watchlist_max_days: int = 200) -> list[Anomaly]:
    """Tickers whose latest fundamentals snapshot is older than threshold."""
    today = datetime.now(UTC).date()
    cutoff_holdings = (today - timedelta(days=holdings_max_days)).isoformat()
    cutoff_watchlist = (today - timedelta(days=watchlist_max_days)).isoformat()
    rows = conn.execute(
        """
        SELECT c.ticker, c.is_holding, MAX(f.period_end) AS last_pe
        FROM companies c
        LEFT JOIN fundamentals f ON f.ticker = c.ticker
        GROUP BY c.ticker
        """,
    ).fetchall()
    out: list[Anomaly] = []
    for ticker, is_holding, last_pe in rows:
        cutoff = cutoff_holdings if is_holding else cutoff_watchlist
        is_holding_bool = bool(is_holding)
        if last_pe is None:
            # Watchlist with NO fundamentals is a slower-burn issue; only flag holdings.
            if not is_holding_bool:
                continue
            out.append(Anomaly(
                market=market, ticker=ticker, kind="FUND_STALE",
                severity="alert",
                detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
                detail={
                    "last_period_end": None,
                    "is_holding": True,
                    "max_age_days": holdings_max_days,
                },
            ))
            continue
        if last_pe < cutoff:
            try:
                age = (today - datetime.fromisoformat(last_pe).date()).days
            except (ValueError, TypeError):
                age = None
            out.append(Anomaly(
                market=market, ticker=ticker, kind="FUND_STALE",
                severity="alert" if is_holding_bool else "warn",
                detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
                detail={
                    "last_period_end": last_pe,
                    "age_days": age,
                    "is_holding": is_holding_bool,
                    "max_age_days": holdings_max_days if is_holding_bool else watchlist_max_days,
                },
            ))
    return out


# ============================================================
# Orchestrator
# ============================================================
def scan(price_pct: float = 20.0,
         price_stale_days: int = 5,
         fund_holdings_days: int = 100,
         fund_watchlist_days: int = 200) -> dict[str, Any]:
    anomalies: list[Anomaly] = []
    for db, market in [(DB_BR, "br"), (DB_US, "us")]:
        if not db.exists():
            continue
        with sqlite3.connect(db) as conn:
            anomalies += detect_price_jumps(conn, market, price_pct)
            anomalies += detect_price_stale(conn, market, price_stale_days)
            anomalies += detect_fundamentals_stale(
                conn, market, fund_holdings_days, fund_watchlist_days
            )

    by_kind: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for a in anomalies:
        by_kind[a.kind] = by_kind.get(a.kind, 0) + 1
        by_severity[a.severity] = by_severity.get(a.severity, 0) + 1

    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "thresholds": {
            "price_pct": price_pct,
            "price_stale_days": price_stale_days,
            "fund_holdings_days": fund_holdings_days,
            "fund_watchlist_days": fund_watchlist_days,
        },
        "totals": {
            "all": len(anomalies),
            "by_kind": by_kind,
            "by_severity": by_severity,
        },
        "anomalies": [asdict(a) for a in anomalies],
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Data anomalies | generated_at={report['generated_at']}",
        f"thresholds: {report['thresholds']}",
        f"totals: {report['totals']['all']} (by_kind={report['totals']['by_kind']} "
        f"by_severity={report['totals']['by_severity']})",
        "",
    ]
    if not report["anomalies"]:
        lines.append("(no anomalies)")
        return "\n".join(lines)
    for kind in ("PRICE_JUMP", "PRICE_STALE", "FUND_STALE"):
        rows = [a for a in report["anomalies"] if a["kind"] == kind]
        if not rows:
            continue
        lines.append(f"## {kind}  ({len(rows)})")
        for a in rows[:30]:
            d = a["detail"]
            ref = f"{a['market']}/{a['ticker']}"
            sev = a["severity"]
            if kind == "PRICE_JUMP":
                lines.append(f"  [{sev:5}] {ref:<10} {d['date']}  ret={d['return_pct']:+.2f}% "
                             f"(close={d['close']} ← {d['prev_close']})")
            elif kind == "PRICE_STALE":
                lines.append(f"  [{sev:5}] {ref:<10} last={d['last_price_date']}  rows={d['rows_total']}")
            else:  # FUND_STALE
                age = d.get("age_days")
                age_str = f"{age}d" if age is not None else "—"
                hold = "HOLD" if d.get("is_holding") else "wtch"
                lines.append(f"  [{sev:5}] {ref:<10} last_pe={d['last_period_end']}  "
                             f"age={age_str}  ({hold})")
        if len(rows) > 30:
            lines.append(f"  ... +{len(rows) - 30} more")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--price-pct", type=float, default=20.0,
                    help="Daily |return| threshold (default 20%%)")
    ap.add_argument("--price-stale-days", type=int, default=5)
    ap.add_argument("--fund-holdings-days", type=int, default=100)
    ap.add_argument("--fund-watchlist-days", type=int, default=200)
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--no-write", action="store_true", help="don't write data_anomalies.json")
    args = ap.parse_args()

    report = scan(
        price_pct=args.price_pct,
        price_stale_days=args.price_stale_days,
        fund_holdings_days=args.fund_holdings_days,
        fund_watchlist_days=args.fund_watchlist_days,
    )

    if not args.no_write:
        OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))
        if not args.no_write:
            print(f"\nwrote: {OUT_PATH.relative_to(ROOT)}")
    return 0 if report["totals"]["by_severity"].get("alert", 0) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
