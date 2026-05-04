"""TTL-based API result cache backed by SQLite.

Schema lives in `data/api_cache.db`. Separate file from market DBs so:
- It can be safely wiped without losing fundamentals/prices time series.
- Backup strategies differ (cache is regenerable, market DBs are not).

Used by `_fallback.py::fetch_with_quality` as the tertiary fallback when
all live sources fail. Also serves as a sliding-window deduplication layer
to spare quota on repeated identical queries within the TTL window.

Cache hit semantics:
    1. Look for non-expired entry first (status=fresh).
    2. If none, fall back to ANY entry regardless of age (status=stale).
       Caller decides via quality flag whether to use it.

TTL defaults (from sources_priority.yaml::cache.ttl_hours when present;
fallback to module defaults below):
    prices:        24h
    fundamentals:  72h  (quarterlies update infrequently)
    dividends:     168h (weekly is fine)
    macro:         168h (weekly central bank publication cycle)
    filings:       24h
    analyst:       24h  (consensus shifts daily on earnings)

Idempotent: schema is created on first import.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CACHE_DB = ROOT / "data" / "api_cache.db"
CONFIG_PATH = ROOT / "config" / "sources_priority.yaml"

DEFAULT_TTL_HOURS = {
    "prices": 24,
    "fundamentals": 72,
    "dividends": 168,
    "macro": 168,
    "filings": 24,
    "analyst": 24,
}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")


@lru_cache(maxsize=1)
def _ttl_hours() -> dict[str, int]:
    """Read TTLs from config if defined, else defaults."""
    if not CONFIG_PATH.exists():
        return dict(DEFAULT_TTL_HOURS)
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    overrides = (cfg.get("cache") or {}).get("ttl_hours") or {}
    merged = dict(DEFAULT_TTL_HOURS)
    merged.update(overrides)
    return merged


def _ttl(kind: str) -> int:
    return int(_ttl_hours().get(kind, 24))


def _conn() -> sqlite3.Connection:
    CACHE_DB.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(CACHE_DB, timeout=10.0)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS api_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market TEXT NOT NULL,
            kind TEXT NOT NULL,
            ticker TEXT NOT NULL,
            source TEXT NOT NULL,
            value_json TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            UNIQUE(market, kind, ticker, source)
        )"""
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_cache_lookup "
        "ON api_cache(market, kind, ticker, expires_at)"
    )
    conn.commit()
    return conn


def put(market: str, kind: str, ticker: str, source: str,
        value: dict[str, Any]) -> None:
    """Insert/replace cache entry with TTL derived from `kind`."""
    ttl_h = _ttl(kind)
    fetched = _now_utc()
    expires = fetched + timedelta(hours=ttl_h)
    payload = json.dumps(value, ensure_ascii=False, default=str)
    with _conn() as c:
        c.execute(
            """INSERT INTO api_cache
                 (market, kind, ticker, source, value_json, fetched_at, expires_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(market, kind, ticker, source) DO UPDATE SET
                 value_json=excluded.value_json,
                 fetched_at=excluded.fetched_at,
                 expires_at=excluded.expires_at""",
            (market, kind, ticker, source,
             payload, fetched.isoformat(), expires.isoformat()),
        )


def get_fresh(market: str, kind: str, ticker: str) -> dict | None:
    """Return cache entry if any source has it AND it's not expired.

    Picks the most recently fetched, then any-source.
    Returns dict with keys: value, source, fetched_at (datetime), age_hours.
    """
    with _conn() as c:
        row = c.execute(
            """SELECT value_json, source, fetched_at FROM api_cache
               WHERE market=? AND kind=? AND ticker=?
                 AND datetime(expires_at) > datetime('now')
               ORDER BY fetched_at DESC LIMIT 1""",
            (market, kind, ticker),
        ).fetchone()
    if not row:
        return None
    fetched_at = datetime.fromisoformat(row[1] if False else row[2])
    return {
        "value": json.loads(row[0]),
        "source": row[1],
        "fetched_at": fetched_at,
        "age_hours": (_now_utc() - fetched_at.replace(tzinfo=fetched_at.tzinfo or timezone.utc)).total_seconds() / 3600,
        "stale": False,
    }


def get_stale(market: str, kind: str, ticker: str) -> dict | None:
    """Return ANY cache entry regardless of age (last-resort fallback)."""
    with _conn() as c:
        row = c.execute(
            """SELECT value_json, source, fetched_at FROM api_cache
               WHERE market=? AND kind=? AND ticker=?
               ORDER BY fetched_at DESC LIMIT 1""",
            (market, kind, ticker),
        ).fetchone()
    if not row:
        return None
    fetched_at = datetime.fromisoformat(row[2])
    age = (_now_utc() - fetched_at.replace(tzinfo=fetched_at.tzinfo or timezone.utc))
    return {
        "value": json.loads(row[0]),
        "source": row[1],
        "fetched_at": fetched_at,
        "age_hours": age.total_seconds() / 3600,
        "stale": True,
    }


def stats() -> dict[str, Any]:
    """Aggregate stats for the data_health monitor."""
    with _conn() as c:
        total = c.execute("SELECT COUNT(*) FROM api_cache").fetchone()[0]
        fresh = c.execute(
            "SELECT COUNT(*) FROM api_cache "
            "WHERE datetime(expires_at) > datetime('now')"
        ).fetchone()[0]
        per_kind = c.execute(
            "SELECT kind, COUNT(*) FROM api_cache GROUP BY kind"
        ).fetchall()
        per_source = c.execute(
            "SELECT source, COUNT(*) FROM api_cache GROUP BY source"
        ).fetchall()
    return {
        "entries_total": total,
        "entries_fresh": fresh,
        "entries_stale": total - fresh,
        "by_kind": dict(per_kind),
        "by_source": dict(per_source),
    }


def purge_expired() -> int:
    """Delete expired entries. Returns count deleted. Idempotent."""
    with _conn() as c:
        cur = c.execute(
            "DELETE FROM api_cache "
            "WHERE datetime(expires_at) < datetime('now', '-7 days')"
        )
        return cur.rowcount


if __name__ == "__main__":
    print(json.dumps(stats(), indent=2, default=str))
