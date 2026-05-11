"""Thesis Perpetuum — valida thesis por ticker.

Wraps existing `agents/perpetuum_validator.py::score_ticker` to fit in the
generic PerpetuumEngine framework. Preserves the thesis_health table
(backwards compat) while also writing to unified perpetuum_health.
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


class ThesisPerpetuum(BasePerpetuum):
    name = "thesis"
    description = "Valida thesis explícita de cada holding contra fundamentals + regime + risk rules"
    autonomy_tier = "T1"
    drop_alert_threshold = 10

    def subjects(self) -> list[PerpetuumSubject]:
        """Holdings + watchlist do universo (companies table).

        2026-04-26: expandido de portfolio_positions only para companies (full
        universe). score_ticker é deterministic + zero LLM, então custo é
        marginal. Watchlist tickers sem thesis devolvem score=-1 (sentinel
        "no_thesis_in_vault") — útil porque expõe quais notas precisam thesis.

        Strip whitespace de ticker — companies table tem CRLF (Windows ingest)
        que polui subject_id e quebra file lookup em obsidian_vault/tickers/.
        """
        subjects = []
        seen: set[str] = set()
        for market, db in DBS.items():
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                rows = c.execute("""
                    SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1
                    UNION
                    SELECT DISTINCT ticker FROM companies
                     WHERE ticker IS NOT NULL AND ticker != ''
                """).fetchall()
            for (ticker,) in rows:
                ticker = (ticker or "").strip()  # strip CRLF / whitespace
                if not ticker:
                    continue
                key = f"{market}:{ticker}"
                if key in seen:
                    continue
                seen.add(key)
                subjects.append(PerpetuumSubject(
                    id=key,
                    label=ticker,
                    metadata={"market": market, "ticker": ticker},
                ))
        return subjects

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        from agents.perpetuum_validator import score_ticker

        ticker = subject.metadata["ticker"]
        market = subject.metadata["market"]
        health = score_ticker(ticker, market)

        action_hint = None
        if health.thesis_score >= 0:
            if health.thesis_score < 30:
                action_hint = f"EXIT — thesis broken, capital preservation ({health.thesis_score})"
            elif health.thesis_score < 50:
                action_hint = f"REBALANCE — thesis materially drifted ({health.thesis_score})"
            elif health.thesis_score < 70:
                action_hint = f"REVIEW — minor drift, re-examine this week ({health.thesis_score})"

        return PerpetuumResult(
            subject_id=subject.id,
            score=health.thesis_score,
            flag_count=health.risk_flags + health.contradictions + health.devils_flags,
            flags=[*health.details.get("risk_reasons", []),
                   *health.details.get("contradiction_reasons", [])],
            details=health.details,
            action_hint=action_hint,
        )
