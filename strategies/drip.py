"""DRIP Engine — dividend compounding (yield + safety + reinvestment friendliness).

Wraps scoring/dividend_safety.compute() and overlays:
  - Yield floor (BR ≥ 6%, US ≥ 2.5%) — uses fundamentals.dy from same DB
  - Safety verdict (SAFE / WATCH / RISK from dividend_safety)
  - Optional: payout coverage (payout_ratio < 0.7 ideally)

A ticker is BUY-DRIP if:
  - safety verdict in {SAFE}
  - dy >= floor for market
A ticker is HOLD-DRIP if:
  - safety in {WATCH} OR
  - safety SAFE but yield below floor (still a quality compounder, just lean)
A ticker is AVOID-DRIP if:
  - safety RISK OR
  - dy is None or 0 and no aristocrat flag
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from scoring.dividend_safety import compute as ds_compute
from scoring.engine import DB_BR, DB_US, _is_fii_ticker, load_fii_snapshot, load_snapshot
from strategies._base import StrategyOutput

ROOT = Path(__file__).resolve().parents[1]

name = "drip"

DY_FLOOR = {"br": 0.06, "us": 0.025}


def _ticker_dy(ticker: str, market: str) -> float | None:
    db = DB_BR if market == "br" else DB_US
    try:
        with sqlite3.connect(db) as conn:
            if market == "br" and _is_fii_ticker(ticker):
                snap = load_fii_snapshot(conn, ticker)
                return (snap or {}).get("fundamentals", {}).get("dy_12m")
            snap = load_snapshot(conn, ticker)
            return (snap or {}).get("fundamentals", {}).get("dy")
    except sqlite3.OperationalError:
        return None


def evaluate(ticker: str, market: str = "us") -> StrategyOutput:
    market = market.lower()
    safety = ds_compute(ticker, market=market)
    if safety is None:
        return StrategyOutput(
            ticker=ticker, market=market, engine=name,
            score=0.0, verdict="N/A",
            rationale={"reason": "ticker not found in DB"},
        )
    dy = _ticker_dy(ticker, market)
    floor = DY_FLOOR.get(market, 0.025)
    score = (safety.total or 0) / 100.0
    has_yield = dy is not None and dy >= floor

    if safety.verdict == "SAFE" and has_yield:
        verdict = "BUY"
        weight = score
    elif safety.verdict == "SAFE":
        verdict = "HOLD"
        weight = 0.0
    elif safety.verdict == "WATCH":
        verdict = "HOLD"
        weight = 0.0
    elif safety.verdict == "RISK":
        verdict = "AVOID"
        weight = 0.0
    else:  # N/A
        verdict = "N/A"
        weight = 0.0
    return StrategyOutput(
        ticker=ticker, market=market, engine=name,
        score=round(score, 4),
        verdict=verdict,
        weight_suggestion=round(weight, 4),
        rationale={
            "safety_score": safety.total,
            "safety_verdict": safety.verdict,
            "components": [
                {"name": c.name, "score": c.score, "weight": c.weight,
                 "value": c.raw_value, "verdict": c.verdict}
                for c in (safety.components or [])
            ],
            "dy": dy,
            "dy_floor": floor,
            "has_yield_above_floor": has_yield,
        },
    )


def rank_universe(market: str = "us",
                  tickers: list[str] | None = None) -> list[StrategyOutput]:
    import yaml
    UNIVERSE = ROOT / "config" / "universe.yaml"
    if tickers is None and UNIVERSE.exists():
        data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8")) or {}
        m = (data.get(market) or {})
        out: list[str] = []
        for bucket in ("holdings", "watchlist", "research_pool"):
            group = m.get(bucket) or {}
            if isinstance(group, list):
                for entry in group:
                    if isinstance(entry, dict) and entry.get("ticker"):
                        out.append(entry["ticker"])
            else:
                for sublist in (group or {}).values():
                    for entry in sublist or []:
                        if isinstance(entry, dict) and entry.get("ticker"):
                            out.append(entry["ticker"])
        tickers = sorted(set(out))
    outputs = [evaluate(t, market) for t in (tickers or [])]
    rankable = [o for o in outputs if o.verdict in ("BUY", "HOLD")]
    rankable.sort(key=lambda o: o.score, reverse=True)
    for i, o in enumerate(rankable, 1):
        o.rank = i
    rest = [o for o in outputs if o not in rankable]
    return rankable + rest
