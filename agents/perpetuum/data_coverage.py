"""Data Coverage Perpetuum — score 0-100 de completeness por holding.

Sinais medidos para cada ticker:
  - price_fresh: última price em prices table ≤ 3 days old
  - fundamentals_fresh: último period_end ≤ 180 days
  - fundamentals_complete: eps, bvps, roe, pe, pb, dy todos ≠ null
  - dy_history: ≥ 3 pontos distintos de DY em fundamentals (permite CAGR)
  - dividend_streak: streak_years >= 3 OR is_aristocrat
  - sector_tagged: companies.sector ≠ null

Score: 100 - 15 per missing signal (6 signals → min 10).

Zero LLM. Pure SQL.

Output: action_hint concreto por missing signal:
  "fetch_price" → run `python scripts/refresh_ticker.py X`
  "fetch_fundamentals" → run `python fetchers/yf_deep_fundamentals.py X`
  etc.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

DBS = {
    "br": ROOT / "data" / "br_investments.db",
    "us": ROOT / "data" / "us_investments.db",
}


class DataCoveragePerpetuum(BasePerpetuum):
    name = "data_coverage"
    description = "Coverage/quality de dados por holding (price, fundamentals, dividends, sector)"
    autonomy_tier = "T2"                   # Promoted 2026-04-24: proposes approvable actions
    drop_alert_threshold = 20
    action_score_threshold = 70            # scores < 70 → action row created

    def subjects(self) -> list[PerpetuumSubject]:
        subjects = []
        for market, db in DBS.items():
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ).fetchall()
            for (ticker,) in rows:
                subjects.append(PerpetuumSubject(
                    id=f"{market}:{ticker}",
                    label=ticker,
                    metadata={"market": market, "ticker": ticker},
                ))
        return subjects

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        market = subject.metadata["market"]
        ticker = subject.metadata["ticker"]
        db = DBS[market]

        signals_checked = 0
        signals_passed = 0
        missing: list[str] = []
        action_hints: list[str] = []

        with sqlite3.connect(db) as c:
            # 1. price_fresh
            signals_checked += 1
            row = c.execute(
                "SELECT date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if row and row[0] >= _n_days_ago(3):
                signals_passed += 1
            else:
                missing.append(f"price stale (last={row[0] if row else 'none'})")
                action_hints.append(f"python scripts/refresh_ticker.py {ticker}")

            # 2. fundamentals_fresh
            signals_checked += 1
            row = c.execute(
                "SELECT period_end FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if row and row[0] >= _n_days_ago(180):
                signals_passed += 1
            else:
                missing.append(f"fundamentals stale (last={row[0] if row else 'none'})")
                action_hints.append(f"python fetchers/yf_deep_fundamentals.py {ticker}")

            # 3. fundamentals_complete
            signals_checked += 1
            row = c.execute(
                "SELECT eps, bvps, roe, pe, pb, dy FROM fundamentals "
                "WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if row and all(v is not None for v in row):
                signals_passed += 1
            else:
                nulls = sum(1 for v in (row or [None]*6) if v is None)
                missing.append(f"fundamentals incomplete ({nulls}/6 nulls)")

            # 4. dy_history
            signals_checked += 1
            row = c.execute(
                "SELECT COUNT(DISTINCT dy) FROM fundamentals WHERE ticker=? AND dy > 0",
                (ticker,),
            ).fetchone()
            if row and row[0] >= 3:
                signals_passed += 1
            else:
                missing.append(f"DY history thin ({row[0] if row else 0} distinct values)")

            # 5. dividend_streak
            signals_checked += 1
            row = c.execute(
                "SELECT MAX(dividend_streak_years), MAX(is_aristocrat) FROM fundamentals WHERE ticker=?",
                (ticker,),
            ).fetchone()
            if row and ((row[0] or 0) >= 3 or row[1]):
                signals_passed += 1
            else:
                missing.append(f"no dividend streak (streak={row[0] if row else None})")

            # 6. sector_tagged
            signals_checked += 1
            row = c.execute(
                "SELECT sector FROM companies WHERE ticker=?",
                (ticker,),
            ).fetchone()
            if row and row[0]:
                signals_passed += 1
            else:
                missing.append("no sector tagged")
                action_hints.append(f"UPDATE companies SET sector='?' WHERE ticker='{ticker}'")

        score = int(100 * signals_passed / signals_checked) if signals_checked else 0
        action_hint = "; ".join(action_hints[:2]) if action_hints else None

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(missing),
            flags=missing,
            details={
                "passed": signals_passed,
                "checked": signals_checked,
                "missing": missing,
                "action_hints": action_hints,
            },
            action_hint=action_hint,
        )


def _n_days_ago(n: int) -> str:
    from datetime import date, timedelta
    return (date.today() - timedelta(days=n)).isoformat()
