"""Graham Engine — deep value, statistical cheapness, balance sheet strength.

Wraps scoring/engine.py::score_br + score_br_bank + score_br_fii.
The BR criteria in this codebase ARE Graham-style (Graham number, low P/E,
P/B, ROE, balance sheet ratios), so this engine is BR-native. Optional
extension: applies same logic to US small-caps if requested (NCAV-style),
but defaults to BR universe.

Output:
  StrategyOutput.score in [0.0, 1.0] = passes / applicable_criteria.
  Verdict: BUY if score >= 0.85, HOLD 0.60-0.85, AVOID < 0.60.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

from scoring.engine import (
    DB_BR,
    DB_US,
    _is_bank,
    _is_fii_ticker,
    _is_reit,
    _is_us_bank,
    _selic_real_bcb,
    load_fii_snapshot,
    load_snapshot,
    score_br,
    score_br_bank,
    score_br_fii,
)
from strategies._base import (
    StrategyOutput,
    details_to_pass_count,
    verdict_from_pass_ratio,
)

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "config" / "universe.yaml"

name = "graham"


def _br_universe() -> list[str]:
    """Read all BR tickers from universe.yaml."""
    if not UNIVERSE.exists():
        return []
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8")) or {}
    br = data.get("br", {}) or {}
    out: list[str] = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        group = br.get(bucket) or {}
        if isinstance(group, list):
            for entry in group:
                if isinstance(entry, dict) and entry.get("ticker"):
                    out.append(entry["ticker"])
        else:
            for sublist in (group or {}).values():
                for entry in sublist or []:
                    if isinstance(entry, dict) and entry.get("ticker"):
                        out.append(entry["ticker"])
    return sorted(set(out))


def _score_one(ticker: str, market: str = "br") -> StrategyOutput:
    db = DB_BR if market == "br" else DB_US
    is_fii = market == "br" and _is_fii_ticker(ticker)
    try:
        with sqlite3.connect(db) as conn:
            if is_fii:
                snap = load_fii_snapshot(conn, ticker)
                if snap is None:
                    return _na_output(ticker, market, "ticker not in DB")
                selic_real = _selic_real_bcb(conn)
                details = score_br_fii(snap, selic_real=selic_real)
                kind = "br_fii"
            else:
                snap = load_snapshot(conn, ticker)
                if snap is None:
                    return _na_output(ticker, market, "ticker not in DB")
                if market == "br" and _is_bank(snap):
                    details = score_br_bank(snap)
                    kind = "br_bank"
                elif market == "br":
                    details = score_br(snap)
                    kind = "br_company"
                else:
                    return _na_output(ticker, market,
                                      "Graham engine only handles BR; for US use Buffett")
    except sqlite3.OperationalError as e:
        return _na_output(ticker, market, f"DB error: {e}")

    passes, applicable = details_to_pass_count(details)
    score = passes / applicable if applicable else 0.0
    verdict = verdict_from_pass_ratio(passes, applicable)
    return StrategyOutput(
        ticker=ticker,
        market=market,
        engine=name,
        score=round(score, 4),
        verdict=verdict,
        weight_suggestion=score if verdict == "BUY" else 0.0,
        rationale={"kind": kind, "details": details,
                   "passes": passes, "applicable": applicable},
    )


def _na_output(ticker: str, market: str, msg: str) -> StrategyOutput:
    return StrategyOutput(
        ticker=ticker, market=market, engine=name,
        score=0.0, verdict="N/A",
        rationale={"reason": msg}, message=msg,
    )


def evaluate(ticker: str, market: str = "br") -> StrategyOutput:
    return _score_one(ticker, market)


def rank_universe(market: str = "br",
                  tickers: list[str] | None = None) -> list[StrategyOutput]:
    if market != "br":
        return []
    universe = tickers or _br_universe()
    outputs = [_score_one(t, market) for t in universe]
    # Filter to BUY/HOLD only for ranking purposes
    rankable = [o for o in outputs if o.verdict in ("BUY", "HOLD")]
    rankable.sort(key=lambda o: o.score, reverse=True)
    for i, o in enumerate(rankable, 1):
        o.rank = i
    rest = [o for o in outputs if o not in rankable]
    return rankable + rest
