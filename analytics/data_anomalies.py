"""Data anomaly detector | scan BR+US DBs for suspicious data.

Five classes of anomaly, all derivable purely from SQL (zero network):

  PRICE_JUMP            — daily abs(return) > pct threshold (default 20%)
  PRICE_STALE           — no `prices` row for ticker in last N business days
  FUND_STALE            — `fundamentals` snapshot older than X days for holding
  BENFORD_DEVIATION     — first-digit distribution of a metric deviates from
                          Benford's Law (chi-square > critical at p<0.05).
                          Aggregate per-metric, not per-ticker. (Phase FF Bloco 2.2)
  CROSS_SECTIONAL_OUTLIER — ticker's log(P/E) is >MAD_THRESHOLD modified
                          z-scores from the sector median (heavy-tailed safe
                          via Median Absolute Deviation). (Phase FF Bloco 2.2)

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
# Phase FF Bloco 2.2 — Benford's Law (aggregated chi-square)
# ============================================================

# Benford's Law: P(first digit = d) = log10(1 + 1/d)
import math
BENFORD_EXPECTED = {d: math.log10(1 + 1/d) for d in range(1, 10)}
# Chi-square critical value @ df=8, p=0.05 -> 15.507; p=0.01 -> 20.090
BENFORD_CHI2_WARN = 15.507
BENFORD_CHI2_ALERT = 20.090
BENFORD_MIN_SAMPLE = 30

# Metrics suitable for Benford (large dynamic range, multiplicative process)
BENFORD_METRICS = ("market_cap", "market_cap_usd", "shares_outstanding")


def _first_digit(value: float | int) -> int | None:
    """Returns first non-zero digit of |value|, or None if not extractable."""
    if value is None:
        return None
    try:
        v = abs(float(value))
    except (ValueError, TypeError):
        return None
    if v == 0 or v != v:  # zero or NaN
        return None
    # scientific notation safe — log10 path
    try:
        exp = math.floor(math.log10(v))
        first = int(v / (10 ** exp))
        return first if 1 <= first <= 9 else None
    except (ValueError, OverflowError):
        return None


def detect_benford_violations(conn: sqlite3.Connection, market: str) -> list[Anomaly]:
    """For each numeric metric in BENFORD_METRICS, compute first-digit distribution
    over latest fundamentals across the universe, run chi-square vs Benford expected.

    Emits ONE Anomaly per metric that violates (ticker = "*ALL*"). This is the
    *correct* way to apply Benford's Law: aggregate distribution, not per-row flag.
    """
    out: list[Anomaly] = []

    # Get latest fundamentals row per ticker
    cols = [r[1] for r in conn.execute("PRAGMA table_info(fundamentals)").fetchall()]
    avail = [c for c in BENFORD_METRICS if c in cols]
    if not avail:
        return out

    select_cols = ", ".join(avail)
    rows = conn.execute(
        f"""
        SELECT ticker, {select_cols}
        FROM fundamentals f
        WHERE (ticker, period_end) IN (
            SELECT ticker, MAX(period_end) FROM fundamentals GROUP BY ticker
        )
        """
    ).fetchall()

    for idx, metric in enumerate(avail):
        digits: list[int] = []
        for row in rows:
            d = _first_digit(row[idx + 1])
            if d is not None:
                digits.append(d)
        n = len(digits)
        if n < BENFORD_MIN_SAMPLE:
            continue
        observed = {d: digits.count(d) / n for d in range(1, 10)}
        chi2 = sum(
            ((observed[d] - BENFORD_EXPECTED[d]) ** 2) / BENFORD_EXPECTED[d]
            for d in range(1, 10)
        ) * n  # multiply by n: standard chi-square form on counts
        if chi2 < BENFORD_CHI2_WARN:
            continue
        sev = "alert" if chi2 >= BENFORD_CHI2_ALERT else "warn"
        out.append(Anomaly(
            market=market, ticker="*ALL*", kind="BENFORD_DEVIATION", severity=sev,
            detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
            detail={
                "metric": metric,
                "sample_size": n,
                "chi_square": round(chi2, 2),
                "critical_warn": BENFORD_CHI2_WARN,
                "critical_alert": BENFORD_CHI2_ALERT,
                "observed_freq": {d: round(observed[d], 4) for d in range(1, 10)},
                "expected_freq": {d: round(BENFORD_EXPECTED[d], 4) for d in range(1, 10)},
            },
        ))
    return out


# ============================================================
# Phase FF Bloco 2.2 — Cross-sectional outliers via MAD on log(metric)
# ============================================================

MAD_CONSTANT = 1.4826  # makes MAD a consistent estimator of std for normal dist
MAD_THRESHOLD_WARN = 3.5
MAD_THRESHOLD_ALERT = 5.0
MAD_MIN_PEERS = 5


def _median(xs: list[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2


def detect_cross_sectional_outliers(conn: sqlite3.Connection, market: str,
                                    threshold: float = MAD_THRESHOLD_WARN) -> list[Anomaly]:
    """Within each sector, flag tickers whose log(P/E) is > threshold modified
    z-scores from the sector median.

    Uses MAD (not std) because P/E distributions are heavy-tailed and lognormal.
    Tests on log(P/E) to handle multiplicative scale.
    """
    rows = conn.execute(
        """
        SELECT c.ticker, c.sector, f.pe
          FROM companies c
          JOIN fundamentals f ON f.ticker = c.ticker
         WHERE (f.ticker, f.period_end) IN (
                 SELECT ticker, MAX(period_end) FROM fundamentals GROUP BY ticker
               )
           AND c.sector IS NOT NULL AND c.sector != ''
           AND f.pe IS NOT NULL AND f.pe > 0
        """
    ).fetchall()

    by_sector: dict[str, list[tuple[str, float]]] = {}
    for ticker, sector, pe in rows:
        by_sector.setdefault(sector, []).append((ticker, pe))

    out: list[Anomaly] = []
    for sector, items in by_sector.items():
        if len(items) < MAD_MIN_PEERS:
            continue
        log_pes = [math.log(pe) for _, pe in items]
        med = _median(log_pes)
        deviations = [abs(x - med) for x in log_pes]
        mad = _median(deviations)
        if mad == 0:
            continue
        for (ticker, pe), log_pe in zip(items, log_pes):
            mod_z = abs(log_pe - med) / (MAD_CONSTANT * mad)
            if mod_z < threshold:
                continue
            sev = "alert" if mod_z >= MAD_THRESHOLD_ALERT else "warn"
            out.append(Anomaly(
                market=market, ticker=ticker, kind="CROSS_SECTIONAL_OUTLIER",
                severity=sev,
                detected_at=datetime.now(UTC).isoformat(timespec="seconds"),
                detail={
                    "metric": "pe",
                    "sector": sector,
                    "ticker_pe": round(pe, 2),
                    "sector_median_pe": round(math.exp(med), 2),
                    "log_modified_z": round(mod_z, 2),
                    "threshold": threshold,
                    "n_peers": len(items),
                },
            ))
    return out


# ============================================================
# Orchestrator
# ============================================================
def scan(price_pct: float = 20.0,
         price_stale_days: int = 5,
         fund_holdings_days: int = 100,
         fund_watchlist_days: int = 200,
         mad_threshold: float = MAD_THRESHOLD_WARN) -> dict[str, Any]:
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
            anomalies += detect_benford_violations(conn, market)
            anomalies += detect_cross_sectional_outliers(conn, market, mad_threshold)

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
    for kind in ("PRICE_JUMP", "PRICE_STALE", "FUND_STALE", "BENFORD_DEVIATION", "CROSS_SECTIONAL_OUTLIER"):
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
                             f"(close={d['close']} <- {d['prev_close']})")
            elif kind == "PRICE_STALE":
                lines.append(f"  [{sev:5}] {ref:<10} last={d['last_price_date']}  rows={d['rows_total']}")
            elif kind == "FUND_STALE":
                age = d.get("age_days")
                age_str = f"{age}d" if age is not None else "-"
                hold = "HOLD" if d.get("is_holding") else "wtch"
                lines.append(f"  [{sev:5}] {ref:<10} last_pe={d['last_period_end']}  "
                             f"age={age_str}  ({hold})")
            elif kind == "BENFORD_DEVIATION":
                lines.append(f"  [{sev:5}] {ref:<10} metric={d['metric']:<20} "
                             f"chi2={d['chi_square']:.2f} (n={d['sample_size']}, "
                             f"warn>{d['critical_warn']:.1f} alert>{d['critical_alert']:.1f})")
            else:  # CROSS_SECTIONAL_OUTLIER
                lines.append(f"  [{sev:5}] {ref:<10} {d['metric']}={d['ticker_pe']:.2f} "
                             f"(sector {d['sector']}: median {d['sector_median_pe']:.2f}, "
                             f"log-MAD-z={d['log_modified_z']:.2f})")
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
    ap.add_argument("--mad-threshold", type=float, default=MAD_THRESHOLD_WARN,
                    help="modified-z threshold for CROSS_SECTIONAL_OUTLIER (default 3.5)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--no-write", action="store_true", help="don't write data_anomalies.json")
    args = ap.parse_args()

    report = scan(
        price_pct=args.price_pct,
        price_stale_days=args.price_stale_days,
        fund_holdings_days=args.fund_holdings_days,
        fund_watchlist_days=args.fund_watchlist_days,
        mad_threshold=args.mad_threshold,
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
