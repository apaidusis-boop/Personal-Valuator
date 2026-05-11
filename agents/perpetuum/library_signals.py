"""Library Signals Perpetuum — daily run dos métodos da library contra carteira.

Subjects: cada (method, ticker) pair com fundamentals recent.
Score: % rules passed (0-100).
Action: se score==100, log paper-trade signal (in T2 tier).

Autonomy: T1 por agora. Promoção para T2 requer:
  - ≥30 signals gerados
  - ≥3 closed_win com positive realized_return
  - No false positive em methods com `caveats` longos
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject


class LibrarySignalsPerpetuum(BasePerpetuum):
    name = "library_signals"
    description = "Aplica library/methods/*.yaml a holdings + watchlist; log paper signals"
    autonomy_tier = "T1"
    drop_alert_threshold = 25
    # FROZEN 2026-04-26 (T0 cleanup): 2511/2912 subjects below threshold = pure noise
    # while paper_trade_close.py has zero closed signals (no win_rate trackable yet).
    # Re-enable once ≥30 signals closed with win_rate measurable.
    enabled = False

    def subjects(self) -> list[PerpetuumSubject]:
        try:
            from library.matcher import load_methods, _holdings_and_watchlist
        except Exception as e:
            return []

        methods = load_methods()
        if not methods:
            return []

        subjects = []
        for method in methods:
            for market in ("br", "us"):
                for ticker in _holdings_and_watchlist(market):
                    subjects.append(PerpetuumSubject(
                        id=f"{method['id']}:{market}:{ticker}",
                        label=f"{method['id']} vs {ticker}",
                        metadata={
                            "method": method,
                            "market": market,
                            "ticker": ticker,
                        },
                    ))
        return subjects

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        from library.matcher import apply_method

        m = subject.metadata["method"]
        market = subject.metadata["market"]
        ticker = subject.metadata["ticker"]

        r = apply_method(m, ticker, market, dry_run=False)

        if r["status"] == "no_fundamentals":
            return PerpetuumResult(
                subject_id=subject.id, score=-1,
                flags=["no_fundamentals"],
                details=r,
            )

        if r["rules_total"] == 0:
            return PerpetuumResult(
                subject_id=subject.id, score=-1,
                flags=["method has 0 evaluable rules"],
                details=r,
            )

        score_pct = int(100 * r["rules_passed"] / r["rules_total"])
        flags = [f"{r['rules_passed']}/{r['rules_total']} rules passed"]

        action_hint = None
        if r["status"] == "SIGNAL":
            action_hint = f"PAPER_SIGNAL logged id={r['signal_id']} — review & track"
        elif score_pct >= 80:
            action_hint = f"NEAR_MISS ({score_pct}%) — verify remaining rules"

        return PerpetuumResult(
            subject_id=subject.id,
            score=score_pct,
            flag_count=1 if r["status"] == "SIGNAL" else 0,
            flags=flags,
            details={
                "rules_passed": r["rules_passed"],
                "rules_total": r["rules_total"],
                "failed_reasons": r["failed_reasons"],
                "signal_id": r["signal_id"],
            },
            action_hint=action_hint,
        )
