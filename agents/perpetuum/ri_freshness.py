"""RI Freshness Perpetuum — monitor releases CVM e flag overdue.

Subjects: cada stock do catalog (holdings + watchlist). FIIs têm pipeline
separado (fii_filings.py + fii_monthly schema) e não entram aqui.

Scoring:
  - has latest quarter ITR/DFP within reasonable window:
      Q1 expected by 2025-05-15 (45d after period end)
      Q2 expected by 2025-08-15
      Q3 expected by 2025-11-15
      Q4/DFP expected by following 2026-04-30
  - has IPE events nos last 30 days (proxy de actividade RI)
  - has IPE events nos last 7 days (urgent flag para fatos relevantes recentes)

Score 0-100. <70 → action_hint para refresh download.

T1 por defaut. Promote T2 quando estável (auto-trigger refresh via whitelisted command).
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject
from library.ri import catalog

DB = ROOT / "data" / "br_investments.db"


def _expected_latest_period(today: date) -> tuple[str, int]:
    """Given today, returns (expected_period_end_iso, days_after_period_for_publication)."""
    y = today.year
    candidates = [
        (date(y, 12, 31), 120),    # DFP delivery cutoff
        (date(y, 9, 30), 45),      # ITR Q3
        (date(y, 6, 30), 45),      # ITR Q2
        (date(y, 3, 31), 45),      # ITR Q1
        (date(y - 1, 12, 31), 120),
        (date(y - 1, 9, 30), 45),
    ]
    for period_end, deadline_days in candidates:
        if today >= period_end + timedelta(days=deadline_days):
            return period_end.isoformat(), deadline_days
    return (date(y - 1, 12, 31).isoformat(), 120)


class RIFreshnessPerpetuum(BasePerpetuum):
    name = "ri_freshness"
    description = "Monitora staleness de filings CVM (DFP/ITR/IPE) por ticker do catalog"
    autonomy_tier = "T2"           # Promoted Y.8.5 — propose actions auto via watchlist_actions
    drop_alert_threshold = 25
    action_score_threshold = 80    # any score < 80 emits actionable proposal

    def subjects(self) -> list[PerpetuumSubject]:
        out = []
        for entry in catalog.all_stocks(include_watchlist=True):
            out.append(PerpetuumSubject(
                id=f"ri:{entry['ticker']}",
                label=entry["ticker"],
                metadata={"ticker": entry["ticker"], "cnpj": entry.get("cnpj"),
                          "codigo_cvm": entry.get("codigo_cvm")},
            ))
        return out

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        ticker = subject.metadata["ticker"]
        today = date.today()
        flags: list[str] = []
        score = 100
        action_steps: list[str] = []

        with sqlite3.connect(DB) as c:
            c.row_factory = sqlite3.Row

            # Signal 1: latest period in quarterly_history vs expected
            row = c.execute(
                "SELECT MAX(period_end) FROM quarterly_history WHERE ticker=?",
                (ticker,),
            ).fetchone()
            latest_qh = row[0] if row and row[0] else None

            expected_period, _ = _expected_latest_period(today)
            if not latest_qh:
                score -= 50
                flags.append("no quarterly_history rows")
                action_steps.append(f"python -m library.ri.cvm_filings ingest itr --year {today.year} --ticker {ticker} && python -m library.ri.cvm_parser build")
            elif latest_qh < expected_period:
                # one quarter behind
                score -= 25
                flags.append(f"quarterly_history latest={latest_qh}, expected≥{expected_period}")
                action_steps.append(f"python -m library.ri.cvm_filings ingest itr --year {today.year} --all-catalog && python -m library.ri.cvm_parser build")

            # Signal 2: IPE events activity (last 30 days)
            cutoff_30 = (today - timedelta(days=30)).isoformat()
            ipe_30 = c.execute(
                "SELECT COUNT(*) FROM cvm_ipe WHERE ticker=? AND dt_referencia >= ?",
                (ticker, cutoff_30),
            ).fetchone()[0]
            if ipe_30 == 0:
                score -= 15
                flags.append("no IPE events in last 30 days (CVM data stale)")
                action_steps.append(f"python -m library.ri.cvm_filings ingest ipe --year {today.year} --all-catalog")

            # Signal 3: fato relevante recent (last 7 days)
            cutoff_7 = (today - timedelta(days=7)).isoformat()
            fr_7 = c.execute(
                """SELECT COUNT(*) FROM cvm_ipe
                   WHERE ticker=? AND dt_referencia >= ?
                     AND (categoria LIKE '%Fato Relevante%' OR tipo LIKE '%Fato Relevante%')""",
                (ticker, cutoff_7),
            ).fetchone()[0]
            # Not a flag, but bonus signal we add to details

            # Signal 4: DFP latest year (annual)
            dfp_periods = c.execute(
                "SELECT period_end FROM quarterly_history WHERE ticker=? AND source='DFP' ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            latest_dfp = dfp_periods[0] if dfp_periods else None
            if not latest_dfp or latest_dfp < f"{today.year - 1}-12-31":
                score -= 10
                flags.append(f"DFP latest={latest_dfp or 'none'}")

        score = max(0, min(100, score))
        action_hint = None
        if action_steps:
            action_hint = "RI_REFRESH: " + " ; ".join(action_steps[:2])

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "latest_quarterly_history": latest_qh,
                "latest_dfp": latest_dfp if 'latest_dfp' in locals() else None,
                "expected_period_min": expected_period,
                "ipe_events_last_30d": ipe_30,
                "fato_relevante_last_7d": fr_7,
                "action_steps": action_steps,
            },
            action_hint=action_hint,
        )
