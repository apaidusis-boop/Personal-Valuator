"""actions — /api/actions/open, /api/actions/{id}/resolve|ignore.

Surface for `watchlist_actions` table (perpetuum + trigger proposals).
Replaces CLI: `python scripts/perpetuum_action_run.py list-open`.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Body, HTTPException

ROOT = Path(__file__).resolve().parents[3]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

router = APIRouter()


def _db_for(market: str) -> Path:
    if market.lower() == "br":
        return DB_BR
    if market.lower() == "us":
        return DB_US
    raise HTTPException(400, f"unknown market {market!r}")


@router.get("/actions/open")
def actions_open() -> list[dict]:
    """Return all open watchlist_actions across BR + US, newest first."""
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT id, ticker, market, kind, trigger_id, action_hint,
                       trigger_snapshot_json, status, opened_at, notes
                FROM watchlist_actions
                WHERE status='open'
                ORDER BY opened_at DESC
            """)
            for r in cur:
                d = dict(r)
                if d.get("trigger_snapshot_json"):
                    try:
                        d["snapshot"] = json.loads(d["trigger_snapshot_json"])
                    except Exception:
                        d["snapshot"] = None
                d.pop("trigger_snapshot_json", None)
                d["market"] = market
                rows.append(d)
    return rows


@router.get("/actions/recent")
def actions_recent(limit: int = 30) -> list[dict]:
    """Last N actions (any status), newest first."""
    rows: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("""
                SELECT id, ticker, market, kind, trigger_id, action_hint,
                       status, opened_at, resolved_at, notes
                FROM watchlist_actions
                ORDER BY opened_at DESC
                LIMIT ?
            """, (limit,))
            for r in cur:
                d = dict(r)
                d["market"] = market
                rows.append(d)
    rows.sort(key=lambda r: r.get("opened_at") or "", reverse=True)
    return rows[:limit]


def _update_status(action_id: int, market: str, status: str,
                   note: str | None = None) -> dict:
    db = _db_for(market)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(db) as c:
        cur = c.execute(
            "SELECT id, ticker, status FROM watchlist_actions WHERE id=?",
            (action_id,),
        )
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(404, f"action {action_id} not found in {market}")
        prev_notes = c.execute(
            "SELECT notes FROM watchlist_actions WHERE id=?",
            (action_id,),
        ).fetchone()[0] or ""
        new_notes = (prev_notes + (" | " if prev_notes and note else "") +
                     (note or "")) if note else prev_notes
        c.execute(
            "UPDATE watchlist_actions SET status=?, resolved_at=?, notes=? WHERE id=?",
            (status, now, new_notes, action_id),
        )
        c.commit()
    return {"id": action_id, "market": market, "status": status, "resolved_at": now}


@router.post("/actions/{market}/{action_id}/resolve")
def action_resolve(market: str, action_id: int,
                   payload: dict | None = Body(None)) -> dict:
    note = (payload or {}).get("note")
    return _update_status(action_id, market, "resolved", note)


@router.post("/actions/{market}/{action_id}/ignore")
def action_ignore(market: str, action_id: int,
                  payload: dict | None = Body(None)) -> dict:
    note = (payload or {}).get("note")
    return _update_status(action_id, market, "ignored", note)
