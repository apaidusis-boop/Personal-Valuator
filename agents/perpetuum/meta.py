"""Meta Perpetuum — valida os perpetuums entre si.

User insight: "processos estarão em perpétuo autoconhecimento". Este é isso.

Subjects: cada perpetuum registado (incluindo ele próprio — exclui-se em score()).

Scoring signals (observados de perpetuum_health + perpetuum_run_log + watchlist_actions):

  - signal_to_noise: % de flags that led to resolved actions / total flags
  - score_distribution_health: not all 100 (trivial), not all 0 (broken)
  - actionability: % de actions com action_hint != null
  - alert_density: alerts / subjects — 0 = stale, >50% = noise
  - runtime_cost: duration_sec vs subjects (efficiency)
  - uniqueness: does it surface what other perpetuums don't?

Score 0-100. < 60 → propor retirement / retune.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

DB = ROOT / "data" / "br_investments.db"


class MetaPerpetuum(BasePerpetuum):
    name = "meta"
    description = "Meta-audit: valida os outros perpetuums (signal-to-noise, useful flags, cost)"
    autonomy_tier = "T1"
    drop_alert_threshold = 20

    def subjects(self) -> list[PerpetuumSubject]:
        if not DB.exists():
            return []
        with sqlite3.connect(DB) as c:
            names = [r[0] for r in c.execute(
                "SELECT DISTINCT perpetuum_name FROM perpetuum_health"
            ).fetchall()]
        # Exclude self to avoid recursion paradox
        return [
            PerpetuumSubject(id=f"perpetuum:{n}", label=n, metadata={"perpetuum_name": n})
            for n in names if n != self.name
        ]

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        name = subject.metadata["perpetuum_name"]
        flags: list[str] = []
        score = 100

        with sqlite3.connect(DB) as c:
            c.row_factory = sqlite3.Row

            # Latest run stats
            last_runs = c.execute(
                "SELECT subjects_count, alerts_count, errors_count, duration_sec "
                "FROM perpetuum_run_log WHERE perpetuum_name=? "
                "ORDER BY run_date DESC LIMIT 7",
                (name,),
            ).fetchall()

            # Score distribution (last run)
            scores = [r[0] for r in c.execute(
                "SELECT score FROM perpetuum_health "
                "WHERE perpetuum_name=? AND score >= 0 AND run_date = ("
                "  SELECT MAX(run_date) FROM perpetuum_health WHERE perpetuum_name=?)",
                (name, name),
            ).fetchall()]

            # Action quality
            action_counts = c.execute(
                "SELECT "
                "  SUM(CASE WHEN status='open' THEN 1 ELSE 0 END) as open_n, "
                "  SUM(CASE WHEN status='resolved' THEN 1 ELSE 0 END) as resolved_n, "
                "  SUM(CASE WHEN status='ignored' THEN 1 ELSE 0 END) as ignored_n "
                "FROM watchlist_actions WHERE kind = ?",
                (f"perpetuum:{name}",),
            ).fetchone()

            # action_hint coverage
            hint_coverage = c.execute(
                "SELECT "
                "  SUM(CASE WHEN action_hint IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) "
                "FROM perpetuum_health "
                "WHERE perpetuum_name=? AND score >= 0 AND run_date = ("
                "  SELECT MAX(run_date) FROM perpetuum_health WHERE perpetuum_name=?)",
                (name, name),
            ).fetchone()

        # --- signal 1: score distribution
        if scores:
            avg = mean(scores)
            sd = stdev(scores) if len(scores) > 1 else 0

            if avg > 98:
                score -= 20
                flags.append(f"trivial pass ratio (avg={avg:.0f})")
            elif avg < 20:
                score -= 15
                flags.append(f"everyone failing (avg={avg:.0f}) — broken?")

            if sd < 2 and len(scores) > 5:
                score -= 15
                flags.append(f"no discrimination (sd={sd:.1f})")
        else:
            score -= 30
            flags.append("no scored subjects")

        # --- signal 2: action quality
        open_n = action_counts["open_n"] or 0
        resolved_n = action_counts["resolved_n"] or 0
        ignored_n = action_counts["ignored_n"] or 0
        total_actions = open_n + resolved_n + ignored_n

        if total_actions > 0:
            ignore_rate = ignored_n / total_actions
            if ignore_rate > 0.7:
                score -= 20
                flags.append(f"high ignore rate ({ignore_rate*100:.0f}%) — noisy actions")

            if open_n > 10 and resolved_n == 0:
                score -= 15
                flags.append(f"{open_n} open actions, 0 resolved — friction or noise")

        # --- signal 3: hint coverage for T2+ perpetuums
        coverage = (hint_coverage[0] if hint_coverage and hint_coverage[0] else 0)
        if coverage < 50 and scores:
            low_scorers = sum(1 for s in scores if s < 70)
            if low_scorers > 5:
                score -= 10
                flags.append(f"only {coverage:.0f}% of flagged have action_hint")

        # --- signal 4: runtime cost
        if last_runs:
            costs = [(r["duration_sec"] / max(r["subjects_count"], 1)) for r in last_runs]
            avg_cost = mean(costs) if costs else 0
            if avg_cost > 1.0:
                score -= 10
                flags.append(f"slow per subject ({avg_cost*1000:.0f}ms avg)")

        # --- signal 5: alert density
        if last_runs:
            densities = [r["alerts_count"] / max(r["subjects_count"], 1) for r in last_runs]
            d = mean(densities)
            if d > 0.5:
                score -= 15
                flags.append(f"alert storm ({d*100:.0f}% of subjects alerted)")

        score = max(0, min(100, score))

        action_hint = None
        if score < 50:
            action_hint = f"RETIRE_or_RETUNE — perpetuum {name} is not pulling weight"
        elif score < 70:
            action_hint = f"CALIBRATE thresholds for perpetuum {name}"

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "scored_subjects": len(scores),
                "avg_score": round(mean(scores), 1) if scores else None,
                "score_sd": round(stdev(scores), 2) if len(scores) > 1 else 0,
                "open_actions": open_n,
                "resolved_actions": resolved_n,
                "ignored_actions": ignored_n,
                "hint_coverage_pct": round(coverage, 1),
                "runs_observed": len(last_runs),
            },
            action_hint=action_hint,
        )
