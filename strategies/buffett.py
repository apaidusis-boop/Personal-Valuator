"""Buffett Engine — quality compounding, durable advantage, fair price.

Wraps scoring/engine.py::score_us + score_us_bank + score_us_reit.
US criteria in this codebase ARE Buffett-style (low P/E, low P/B, ROE,
Aristocrat). Adds optional ROIC criterion when fundamentals.roic populated
(via roic ALTER TABLE migration).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

from scoring.engine import (
    DB_US,
    _is_reit,
    _is_us_bank,
    load_snapshot,
    score_us,
    score_us_bank,
    score_us_reit,
)
from strategies._base import (
    StrategyOutput,
    details_to_pass_count,
    verdict_from_pass_ratio,
)

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "config" / "universe.yaml"
KINGS_ARISTO = ROOT / "config" / "kings_aristocrats.yaml"

name = "buffett"


def _us_universe() -> list[str]:
    out: list[str] = []
    if UNIVERSE.exists():
        data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8")) or {}
        us = data.get("us", {}) or {}
        for bucket in ("holdings", "watchlist", "research_pool"):
            group = us.get(bucket) or {}
            if isinstance(group, list):
                for entry in group:
                    if isinstance(entry, dict) and entry.get("ticker"):
                        out.append(entry["ticker"])
            else:
                for sublist in (group or {}).values():
                    for entry in sublist or []:
                        if isinstance(entry, dict) and entry.get("ticker"):
                            out.append(entry["ticker"])
    if KINGS_ARISTO.exists():
        ka = yaml.safe_load(KINGS_ARISTO.read_text(encoding="utf-8")) or {}
        for entry in ka.get("tickers") or []:
            if entry.get("ticker"):
                out.append(entry["ticker"])
    return sorted(set(out))


def _score_one_with_roic(snap: dict, base_details: dict, ticker: str) -> dict:
    """Compute ROIC from deep_fundamentals on-the-fly. If unavailable, leaves
    base_details unchanged. ROIC ≥ 15% (Buffett's quality bar)."""
    from scoring.roic import compute as roic_compute
    roic = roic_compute(ticker, "us")
    if roic is None:
        return base_details
    out = dict(base_details)
    out["roic"] = {
        "value": roic,
        "threshold": 0.15,
        "verdict": "pass" if roic >= 0.15 else "fail",
    }
    return out


def _score_one(ticker: str, market: str = "us") -> StrategyOutput:
    if market != "us":
        return StrategyOutput(
            ticker=ticker, market=market, engine=name,
            score=0.0, verdict="N/A",
            rationale={"reason": "Buffett engine only handles US; for BR use Graham"},
        )
    try:
        with sqlite3.connect(DB_US) as conn:
            snap = load_snapshot(conn, ticker)
            if snap is None:
                return StrategyOutput(
                    ticker=ticker, market=market, engine=name,
                    score=0.0, verdict="N/A",
                    rationale={"reason": "ticker not in DB"},
                )
            if _is_reit(snap):
                base = score_us_reit(snap)
                kind = "us_reit"
            elif _is_us_bank(snap):
                base = score_us_bank(snap)
                kind = "us_bank"
            else:
                base = score_us(snap)
                kind = "us_company"
            details = _score_one_with_roic(snap, base, ticker)
    except sqlite3.OperationalError as e:
        return StrategyOutput(
            ticker=ticker, market=market, engine=name,
            score=0.0, verdict="N/A",
            rationale={"reason": f"DB error: {e}"},
        )

    passes, applicable = details_to_pass_count(details)
    score = passes / applicable if applicable else 0.0
    verdict = verdict_from_pass_ratio(passes, applicable)
    return StrategyOutput(
        ticker=ticker, market=market, engine=name,
        score=round(score, 4),
        verdict=verdict,
        weight_suggestion=score if verdict == "BUY" else 0.0,
        rationale={"kind": kind, "details": details,
                   "passes": passes, "applicable": applicable},
    )


def evaluate(ticker: str, market: str = "us") -> StrategyOutput:
    return _score_one(ticker, market)


def rank_universe(market: str = "us",
                  tickers: list[str] | None = None) -> list[StrategyOutput]:
    if market != "us":
        return []
    universe = tickers or _us_universe()
    outputs = [_score_one(t, market) for t in universe]
    rankable = [o for o in outputs if o.verdict in ("BUY", "HOLD")]
    rankable.sort(key=lambda o: o.score, reverse=True)
    for i, o in enumerate(rankable, 1):
        o.rank = i
    rest = [o for o in outputs if o not in rankable]
    return rankable + rest
