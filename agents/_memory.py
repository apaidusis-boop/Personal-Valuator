"""Operational memory — record every agent_call decision.

Schema (data/agent_decisions.db):
  agent_decisions(
      id INTEGER PK,
      ts TEXT,                  -- ISO UTC
      role TEXT,                -- 'classification' | 'extraction' | ...
      task TEXT,                -- short label of the task
      ticker TEXT,              -- optional
      market TEXT,              -- optional
      model TEXT,               -- modelo usado
      input_hash TEXT,          -- SHA1 do input para dedup
      output_summary TEXT,      -- 200 chars do output (full em output_json)
      output_json TEXT,         -- output completo serializado
      success INTEGER,          -- 1=ok, 0=fail
      attempts INTEGER,         -- quantas tentativas até sucesso
      latency_ms INTEGER,
      cost_tokens INTEGER,      -- estimado, se aplicável
      escalated INTEGER,        -- 1 se subiu para 32B
      run_id TEXT,              -- correlação com batch run
      notes TEXT
  )

API:
    record(decision: dict) -> int     # inserts row, returns id
    recent(role, ticker?, limit=10)   # SELECT recent matching
    last_for_input(hash, max_age_hours=1)  # cache lookup; None if expired
    purge_old(retention_days=90)

Usage by _agent.py:
    - Before call: lookup last_for_input(hash) — if recent and successful,
      skip the LLM call entirely and return cached output.
    - After call: record(...) regardless of success/fail.

Idempotent schema creation on import.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "agent_decisions.db"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=10.0)
    c.execute(
        """CREATE TABLE IF NOT EXISTS agent_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            role TEXT NOT NULL,
            task TEXT,
            ticker TEXT,
            market TEXT,
            model TEXT,
            input_hash TEXT,
            output_summary TEXT,
            output_json TEXT,
            success INTEGER,
            attempts INTEGER,
            latency_ms INTEGER,
            cost_tokens INTEGER,
            escalated INTEGER DEFAULT 0,
            run_id TEXT,
            notes TEXT
        )"""
    )
    c.execute(
        "CREATE INDEX IF NOT EXISTS idx_role_ticker_ts "
        "ON agent_decisions(role, ticker, ts)"
    )
    c.execute(
        "CREATE INDEX IF NOT EXISTS idx_input_hash "
        "ON agent_decisions(input_hash, ts)"
    )
    c.commit()
    return c


def hash_input(payload: Any) -> str:
    """Stable SHA1 of input — used for dedup cache lookups."""
    s = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def record(decision: dict[str, Any]) -> int:
    """Insert a decision record. Returns the new id."""
    fields = {
        "ts": _now_iso(),
        "role": decision.get("role", "?"),
        "task": decision.get("task"),
        "ticker": decision.get("ticker"),
        "market": decision.get("market"),
        "model": decision.get("model"),
        "input_hash": decision.get("input_hash"),
        "output_summary": (decision.get("output_summary") or "")[:200],
        "output_json": json.dumps(decision.get("output"), default=str, ensure_ascii=False),
        "success": 1 if decision.get("success") else 0,
        "attempts": decision.get("attempts", 1),
        "latency_ms": decision.get("latency_ms"),
        "cost_tokens": decision.get("cost_tokens"),
        "escalated": 1 if decision.get("escalated") else 0,
        "run_id": decision.get("run_id"),
        "notes": decision.get("notes"),
    }
    cols = ", ".join(fields.keys())
    placeholders = ", ".join("?" * len(fields))
    with _conn() as c:
        cur = c.execute(
            f"INSERT INTO agent_decisions ({cols}) VALUES ({placeholders})",
            tuple(fields.values()),
        )
        return cur.lastrowid or 0


def last_for_input(input_hash: str, *, max_age_hours: int = 1
                   ) -> dict | None:
    """Find a successful recent decision for the same input — used for dedup.
    Returns dict with parsed output_json, or None if no cache hit."""
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=max_age_hours)).isoformat()
    with _conn() as c:
        row = c.execute(
            """SELECT id, ts, role, output_json, model, attempts FROM agent_decisions
               WHERE input_hash=? AND success=1 AND ts > ?
               ORDER BY ts DESC LIMIT 1""",
            (input_hash, cutoff),
        ).fetchone()
    if not row:
        return None
    try:
        out = json.loads(row[3]) if row[3] else None
    except json.JSONDecodeError:
        out = None
    return {
        "id": row[0],
        "ts": row[1],
        "role": row[2],
        "output": out,
        "model": row[4],
        "attempts": row[5],
    }


def recent(role: str | None = None, *, ticker: str | None = None,
           limit: int = 10) -> list[dict]:
    """Recent decisions matching filters; useful for audit + UI."""
    where = []
    params: list[Any] = []
    if role:
        where.append("role=?")
        params.append(role)
    if ticker:
        where.append("ticker=?")
        params.append(ticker)
    sql = "SELECT id, ts, role, ticker, market, model, success, attempts, " \
          "escalated, output_summary FROM agent_decisions"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY ts DESC LIMIT ?"
    params.append(limit)
    with _conn() as c:
        rows = c.execute(sql, tuple(params)).fetchall()
    return [
        {
            "id": r[0], "ts": r[1], "role": r[2], "ticker": r[3],
            "market": r[4], "model": r[5], "success": bool(r[6]),
            "attempts": r[7], "escalated": bool(r[8]),
            "summary": r[9],
        }
        for r in rows
    ]


def stats(days: int = 7) -> dict:
    """Aggregate counts for monitoring."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    with _conn() as c:
        total = c.execute(
            "SELECT COUNT(*) FROM agent_decisions WHERE ts > ?", (cutoff,)
        ).fetchone()[0]
        ok = c.execute(
            "SELECT COUNT(*) FROM agent_decisions WHERE ts > ? AND success=1",
            (cutoff,),
        ).fetchone()[0]
        per_role = c.execute(
            """SELECT role, COUNT(*), SUM(success), AVG(attempts), SUM(escalated)
               FROM agent_decisions WHERE ts > ? GROUP BY role""", (cutoff,),
        ).fetchall()
        per_model = c.execute(
            "SELECT model, COUNT(*) FROM agent_decisions WHERE ts > ? GROUP BY model",
            (cutoff,),
        ).fetchall()
    return {
        "window_days": days,
        "total": total,
        "ok": ok,
        "fail": total - ok,
        "success_rate_pct": round(ok / total * 100, 1) if total else 0,
        "by_role": [
            {"role": r[0], "count": r[1], "ok": r[2],
             "avg_attempts": round(r[3], 2) if r[3] else None,
             "escalations": r[4] or 0}
            for r in per_role
        ],
        "by_model": dict(per_model),
    }


def purge_old(retention_days: int = 90) -> int:
    """Delete entries older than N days. Returns rowcount."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()
    with _conn() as c:
        cur = c.execute("DELETE FROM agent_decisions WHERE ts < ?", (cutoff,))
        return cur.rowcount


if __name__ == "__main__":
    print(json.dumps(stats(), indent=2, default=str))
