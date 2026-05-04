"""Data-quality guards shared by US/BR fetchers.

Thresholds are read from config/sources_priority.yaml::guards. This lets
analysts ajustar limites sem deploy. Guards return True when the value is
suspect (caller skips the row + logs).

API:
    is_suspicious_close(conn, ticker, date, close) -> bool
    is_suspicious_volume(conn, ticker, date, volume) -> bool
    is_extreme_metric(metric_name, value) -> bool
        metric_name ∈ {pe, pb, roe, dy}
"""
from __future__ import annotations

import sqlite3
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources_priority.yaml"


@lru_cache(maxsize=1)
def _guards() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    return cfg.get("guards", {}) or {}


def _price_guards() -> dict:
    return _guards().get("prices", {}) or {}


def _fund_guards() -> dict:
    return _guards().get("fundamentals", {}) or {}


def is_suspicious_close(conn: sqlite3.Connection, ticker: str,
                        date_iso: str, close: float) -> bool:
    """>50% intraday move vs previous close → reject. Catches Yahoo glitches."""
    if close is None or close <= 0:
        return True
    g = _price_guards()
    jump_max = float(g.get("intraday_jump_max_ratio", 2.0))
    drop_min = float(g.get("intraday_drop_min_ratio", 0.5))
    row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<? "
        "ORDER BY date DESC LIMIT 1", (ticker, date_iso),
    ).fetchone()
    if not row or not row[0] or row[0] <= 0:
        return False
    prev = float(row[0])
    ratio = close / prev
    return ratio < drop_min or ratio > jump_max


def is_suspicious_volume(conn: sqlite3.Connection, ticker: str,
                         date_iso: str, volume: int | None) -> bool:
    """Volume > N× the trailing 30-session median → suspect (data artifact / glitch).
    Returns False if no baseline (e.g. new ticker).
    """
    if volume is None or volume <= 0:
        return False
    g = _price_guards()
    spike_max = float(g.get("volume_spike_max_x_median", 10.0))
    rows = conn.execute(
        "SELECT volume FROM prices WHERE ticker=? AND date<? AND volume IS NOT NULL "
        "AND volume>0 ORDER BY date DESC LIMIT 30",
        (ticker, date_iso),
    ).fetchall()
    if len(rows) < 10:
        return False
    vols = sorted(int(r[0]) for r in rows)
    median = vols[len(vols) // 2]
    if median <= 0:
        return False
    return volume > median * spike_max


def is_extreme_metric(metric_name: str, value: float | None) -> bool:
    """Reject implausible fundamentals values (likely yfinance bugs).
    metric_name ∈ {pe, pb, roe, dy}.
    """
    if value is None:
        return False
    g = _fund_guards()
    try:
        v = float(value)
    except (TypeError, ValueError):
        return True
    if v != v:  # NaN
        return True
    if metric_name == "pe":
        return abs(v) > float(g.get("pe_max_sane", 1000))
    if metric_name == "pb":
        return abs(v) > float(g.get("pb_max_sane", 100))
    if metric_name == "roe":
        return abs(v) > float(g.get("roe_max_sane", 5.0))
    if metric_name == "dy":
        dy_max = float(g.get("dy_max_sane", 0.25))
        dy_min = float(g.get("dy_min_sane", 0.0))
        return v > dy_max or v < dy_min
    return False
