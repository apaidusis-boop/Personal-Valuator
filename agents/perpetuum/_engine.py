"""BasePerpetuum — contrato comum para self-improvement loops.

Each perpetuum is a self-improving loop that:
  1. enumerates subjects (tickers, notes, fetchers, ...)
  2. observes current state of each
  3. scores 0-100 against baseline expectations
  4. persists to perpetuum_health table (unified schema)
  5. emits signals when score drops ≥ drop_alert_threshold
  6. optionally writes action_hint for T2+ tiers

Subclasses implement:
  - name (class attribute)
  - autonomy_tier (T1..T5, default T1)
  - subjects() → list[PerpetuumSubject]
  - score(subject) → PerpetuumResult
"""
from __future__ import annotations

import json
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SHARED_DB = ROOT / "data" / "br_investments.db"  # perpetuum_health lives here

UNIFIED_SCHEMA = """
CREATE TABLE IF NOT EXISTS perpetuum_health (
    perpetuum_name TEXT    NOT NULL,
    subject_id     TEXT    NOT NULL,
    run_date       TEXT    NOT NULL,
    score          INTEGER NOT NULL,
    flag_count     INTEGER NOT NULL DEFAULT 0,
    tier           TEXT    NOT NULL DEFAULT 'T1',
    details_json   TEXT,
    action_hint    TEXT,
    PRIMARY KEY (perpetuum_name, subject_id, run_date)
);

CREATE INDEX IF NOT EXISTS idx_perp_health_date   ON perpetuum_health(run_date);
CREATE INDEX IF NOT EXISTS idx_perp_health_name   ON perpetuum_health(perpetuum_name);
CREATE INDEX IF NOT EXISTS idx_perp_health_score  ON perpetuum_health(score);

CREATE TABLE IF NOT EXISTS perpetuum_run_log (
    perpetuum_name TEXT    NOT NULL,
    run_date       TEXT    NOT NULL,
    started_at     TEXT    NOT NULL,
    finished_at    TEXT    NOT NULL,
    duration_sec   REAL    NOT NULL,
    subjects_count INTEGER NOT NULL,
    alerts_count   INTEGER NOT NULL,
    errors_count   INTEGER NOT NULL,
    summary        TEXT,
    PRIMARY KEY (perpetuum_name, run_date)
);
"""


def ensure_schema(db: Path | None = None) -> None:
    """Idempotent — safe to call multiple times."""
    db = db or SHARED_DB
    with sqlite3.connect(db) as c:
        c.executescript(UNIFIED_SCHEMA)
        c.commit()


@dataclass
class PerpetuumSubject:
    """Um subject a ser avaliado por um perpetuum."""
    id: str                        # unique key within perpetuum (ticker, path, etc.)
    label: str = ""                # human-readable
    metadata: dict = field(default_factory=dict)


@dataclass
class PerpetuumResult:
    """Output de score() para um subject."""
    subject_id: str
    score: int                     # 0-100 (or -1 for "not applicable")
    flag_count: int = 0
    flags: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
    action_hint: str | None = None


class BasePerpetuum(ABC):
    """Contrato base. Subclasses definem name + subjects() + score()."""

    name: str = ""                      # unique identifier
    description: str = ""
    autonomy_tier: str = "T1"           # T1 Observer | T2 Proposer | ... T5 Autonomous
    drop_alert_threshold: int = 10      # drop N points vs last run → alert
    action_score_threshold: int = 70    # scores below this get action row (T2+)
    db_path: Path | None = None         # override if perpetuum uses non-default DB
    enabled: bool = True                # T0: set False to freeze without removing

    def __init__(self):
        self._db = self.db_path or SHARED_DB
        ensure_schema(self._db)

    @abstractmethod
    def subjects(self) -> list[PerpetuumSubject]:
        """Enumerar all subjects to score."""

    @abstractmethod
    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        """Score um subject. Should be deterministic + idempotent."""

    # --- runner ---

    def run(self, run_date: str | None = None, dry_run: bool = False) -> dict:
        run_date = run_date or date.today().isoformat()
        started = datetime.now(timezone.utc)

        subjects = self.subjects()
        results: list[tuple[PerpetuumSubject, PerpetuumResult]] = []
        errors: list[str] = []

        for s in subjects:
            try:
                r = self.score(s)
                results.append((s, r))
            except Exception as e:
                errors.append(f"{s.id}: {type(e).__name__}: {e}")

        alerts = 0
        actions_written = 0
        is_t2_plus = self.autonomy_tier in ("T2", "T3", "T4", "T5")

        if not dry_run:
            for s, r in results:
                prev = self._last_score(s.id, run_date)
                if prev is not None and r.score >= 0 and prev - r.score >= self.drop_alert_threshold:
                    alerts += 1
                    r.details["alert_drop"] = prev - r.score
                    r.details["prev_score"] = prev
                self._persist(r, run_date)

                # T2+ autonomy: auto-propose action when score below threshold
                if (is_t2_plus and r.score >= 0
                        and r.score < self.action_score_threshold
                        and r.action_hint):
                    from ._actions import write_action_from_result
                    created, _ = write_action_from_result(
                        perpetuum_name=self.name,
                        subject_id=s.id,
                        score=r.score,
                        action_hint=r.action_hint,
                        flags=r.flags,
                        details=r.details,
                        run_date=run_date,
                    )
                    if created:
                        actions_written += 1

        finished = datetime.now(timezone.utc)
        duration = (finished - started).total_seconds()
        summary = (f"{self.name}: scored {len(results)}/{len(subjects)} subjects, "
                   f"{alerts} alerts, {len(errors)} errors")

        if not dry_run:
            self._log_run(run_date, started, finished, duration,
                          len(subjects), alerts, len(errors), summary)

        return {
            "perpetuum": self.name,
            "tier": self.autonomy_tier,
            "run_date": run_date,
            "subjects": len(subjects),
            "scored": len(results),
            "alerts": alerts,
            "actions_written": actions_written,
            "errors": errors,
            "duration_sec": duration,
            "summary": summary,
            "results": [{"subject": s.id, "score": r.score,
                         "flags": r.flag_count, "action_hint": r.action_hint}
                        for s, r in results],
        }

    # --- persistence helpers ---

    def _persist(self, r: PerpetuumResult, run_date: str) -> None:
        with sqlite3.connect(self._db) as c:
            c.execute(
                """
                INSERT OR REPLACE INTO perpetuum_health
                    (perpetuum_name, subject_id, run_date, score,
                     flag_count, tier, details_json, action_hint)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.name, r.subject_id, run_date, r.score,
                    r.flag_count, self.autonomy_tier,
                    json.dumps(r.details, ensure_ascii=False, default=str),
                    r.action_hint,
                ),
            )
            c.commit()

    def _last_score(self, subject_id: str, before_date: str) -> int | None:
        with sqlite3.connect(self._db) as c:
            row = c.execute(
                "SELECT score FROM perpetuum_health "
                "WHERE perpetuum_name=? AND subject_id=? AND run_date<? "
                "ORDER BY run_date DESC LIMIT 1",
                (self.name, subject_id, before_date),
            ).fetchone()
        return row[0] if row else None

    def _log_run(self, run_date, started, finished, duration,
                 subjects, alerts, errors, summary) -> None:
        with sqlite3.connect(self._db) as c:
            c.execute(
                """
                INSERT OR REPLACE INTO perpetuum_run_log
                    (perpetuum_name, run_date, started_at, finished_at,
                     duration_sec, subjects_count, alerts_count, errors_count, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.name, run_date,
                    started.isoformat(timespec="seconds"),
                    finished.isoformat(timespec="seconds"),
                    duration, subjects, alerts, errors, summary,
                ),
            )
            c.commit()
