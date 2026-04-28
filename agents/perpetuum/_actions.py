"""Perpetuum → watchlist_actions writer (T2+ autonomy).

Quando um perpetuum tem tier T2+, resultados com score baixo + action_hint
são auto-escritos em `watchlist_actions` table para user rever via action_cli
ou skill `perpetuum-review`.

Dedup (2 níveis):
  1. trigger_id = `perpetuum:<name>:<subject_id>:<run_date>` — re-runs no
     mesmo dia são idempotent (same trigger_id → skip).
  2. (kind, ticker_or_id, status='open') — runs em dias diferentes que
     escolheriam piling up new rows quando já há uma open são skipped.
     Mantém o queue limpo: uma open action por (perpetuum, subject) até
     user resolver/ignorar.

Safety: action_hint é escrito but NOT executed. User approves via CLI/skill.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}


def _split_subject_id(subject_id: str) -> tuple[str, str]:
    """Parse 'br:TICKER' or 'us:TICKER' or 'relative/path.md' → (market, identifier).

    Non-market subjects go to BR db as default (perpetuum_vault notes etc).
    """
    if subject_id.startswith("br:") or subject_id.startswith("us:"):
        market, ticker = subject_id.split(":", 1)
        return market, ticker
    # vault notes, workflow paths, etc. — default to BR db for central storage
    return "br", subject_id


def write_action_from_result(
    perpetuum_name: str,
    subject_id: str,
    score: int,
    action_hint: str,
    flags: list[str],
    details: dict,
    run_date: str,
) -> tuple[bool, int | None]:
    """Insert into watchlist_actions. Returns (created, row_id).

    If trigger_id already exists → skip (idempotent). Else insert with status=open.
    """
    if not action_hint or score < 0:
        return False, None

    market, identifier = _split_subject_id(subject_id)
    db = DBS[market]

    trigger_id = f"perpetuum:{perpetuum_name}:{subject_id}:{run_date}"
    kind = f"perpetuum:{perpetuum_name}"
    snapshot = {
        "perpetuum": perpetuum_name,
        "subject_id": subject_id,
        "score": score,
        "flags": flags,
        "details": details,
        "run_date": run_date,
    }
    opened_at = datetime.now(UTC).isoformat(timespec="seconds")

    with sqlite3.connect(db) as c:
        exists = c.execute(
            "SELECT id FROM watchlist_actions WHERE trigger_id = ?",
            (trigger_id,),
        ).fetchone()
        if exists:
            return False, exists[0]

        ticker_or_id = identifier if market in ("br", "us") and ":" not in identifier else identifier[:32]

        already_open = c.execute(
            "SELECT id FROM watchlist_actions WHERE kind = ? AND ticker = ? AND status = 'open'",
            (kind, ticker_or_id),
        ).fetchone()
        if already_open:
            return False, already_open[0]

        cur = c.execute(
            """
            INSERT INTO watchlist_actions
                (ticker, market, kind, trigger_id, action_hint,
                 trigger_snapshot_json, status, opened_at)
            VALUES (?, ?, ?, ?, ?, ?, 'open', ?)
            """,
            (
                ticker_or_id, market, kind, trigger_id,
                action_hint, json.dumps(snapshot, ensure_ascii=False, default=str),
                opened_at,
            ),
        )
        c.commit()
        return True, cur.lastrowid


def list_open_by_perpetuum(perpetuum_name: str | None = None) -> list[dict]:
    """List open actions, optionally filtered by perpetuum_name."""
    out = []
    for market, db in DBS.items():
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            if perpetuum_name:
                rows = c.execute(
                    "SELECT * FROM watchlist_actions WHERE status='open' AND kind = ? ORDER BY opened_at DESC",
                    (f"perpetuum:{perpetuum_name}",),
                ).fetchall()
            else:
                rows = c.execute(
                    "SELECT * FROM watchlist_actions WHERE status='open' AND kind LIKE 'perpetuum:%' ORDER BY opened_at DESC"
                ).fetchall()
            for r in rows:
                d = dict(r)
                d["_db_market"] = market
                out.append(d)
    return out
