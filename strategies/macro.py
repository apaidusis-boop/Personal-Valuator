"""Macro Engine — top-down regime overlay applied to per-ticker tilt.

Wraps analytics.regime.classify() to get current regime per market,
then config/macro_overlays.yaml to map regime+sector → multiplier.

Per-ticker output:
  score = multiplier (0.5 / 1.0 / 1.5) normalized to 0-1 via /1.5
  verdict: BUY if multiplier 1.5, HOLD if 1.0, AVOID if 0.5.

This is NOT a fundamental signal — it's a TILT. The Portfolio Engine
weights the macro engine smaller (~15%) than fundamental engines.
"""
from __future__ import annotations

import sqlite3
from functools import lru_cache
from pathlib import Path

import yaml

from analytics.regime import classify
from scoring.engine import DB_BR, DB_US
from strategies._base import StrategyOutput

ROOT = Path(__file__).resolve().parents[1]
OVERLAY_PATH = ROOT / "config" / "macro_overlays.yaml"

name = "macro"


@lru_cache(maxsize=1)
def _overlays() -> dict:
    if not OVERLAY_PATH.exists():
        return {}
    return yaml.safe_load(OVERLAY_PATH.read_text(encoding="utf-8")) or {}


@lru_cache(maxsize=2)
def _regime_for(market: str) -> tuple[str, str]:
    """Returns (regime_name, confidence) — cached per session."""
    r = classify(market)
    return (r.regime, r.confidence)


def _ticker_sector(ticker: str, market: str) -> str | None:
    db = DB_BR if market == "br" else DB_US
    try:
        with sqlite3.connect(db) as conn:
            row = conn.execute(
                "SELECT sector FROM companies WHERE ticker=?", (ticker,)
            ).fetchone()
            return (row[0] or "").lower() if row else None
    except sqlite3.OperationalError:
        return None


def _multiplier(market: str, regime: str, sector: str | None) -> tuple[float, str]:
    """Resolve sector tilt for current regime. Returns (multiplier, label)."""
    cfg = _overlays()
    rmap = ((cfg.get("regimes") or {}).get(market) or {}).get(regime) or {}
    mults = cfg.get("multipliers") or {"tilt_up": 1.5, "neutral": 1.0, "tilt_down": 0.5}
    if not sector:
        return (mults["neutral"], "neutral")
    sl = sector.lower()
    for tilt_sector in (rmap.get("tilt_up") or []):
        if tilt_sector.lower() in sl or sl in tilt_sector.lower():
            return (mults["tilt_up"], "tilt_up")
    for tilt_sector in (rmap.get("tilt_down") or []):
        if tilt_sector.lower() in sl or sl in tilt_sector.lower():
            return (mults["tilt_down"], "tilt_down")
    return (mults["neutral"], "neutral")


def evaluate(ticker: str, market: str = "us") -> StrategyOutput:
    market = market.lower()
    sector = _ticker_sector(ticker, market)
    regime, confidence = _regime_for(market)
    mult, label = _multiplier(market, regime, sector)
    score = round(mult / 1.5, 4)  # normalize to 0-1
    if label == "tilt_up":
        verdict = "BUY"
        weight = score
    elif label == "neutral":
        verdict = "HOLD"
        weight = 0.0
    else:
        verdict = "AVOID"
        weight = 0.0
    cfg = _overlays()
    rcfg = ((cfg.get("regimes") or {}).get(market) or {}).get(regime) or {}
    return StrategyOutput(
        ticker=ticker, market=market, engine=name,
        score=score, verdict=verdict, weight_suggestion=weight,
        rationale={
            "regime": regime,
            "regime_confidence": confidence,
            "sector": sector,
            "tilt": label,
            "multiplier": mult,
            "regime_notes": rcfg.get("notes"),
        },
    )


def rank_universe(market: str = "us",
                  tickers: list[str] | None = None) -> list[StrategyOutput]:
    if tickers is None:
        # Macro engine doesn't enumerate; wraps universes from elsewhere.
        return []
    outs = [evaluate(t, market) for t in tickers]
    rankable = [o for o in outs if o.verdict in ("BUY", "HOLD")]
    rankable.sort(key=lambda o: o.score, reverse=True)
    for i, o in enumerate(rankable, 1):
        o.rank = i
    rest = [o for o in outs if o not in rankable]
    return rankable + rest


def current_regime(market: str) -> dict:
    """Helper for callers that just want the regime metadata."""
    regime, confidence = _regime_for(market)
    cfg = _overlays()
    rcfg = ((cfg.get("regimes") or {}).get(market) or {}).get(regime) or {}
    return {
        "market": market,
        "regime": regime,
        "confidence": confidence,
        "tilt_up": rcfg.get("tilt_up", []),
        "tilt_down": rcfg.get("tilt_down", []),
        "notes": rcfg.get("notes"),
    }
