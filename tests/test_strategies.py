"""Tests for strategies/* — focus on contract conformance + edge cases.

Cobertura:
  - StrategyOutput shape uniform across engines
  - verdict_from_pass_ratio thresholds
  - details_to_pass_count ignores 'n/a'
  - Each engine handles missing-ticker gracefully (verdict='N/A')
  - Hedge engine emits correct status string per regime
  - Portfolio engine combines + detects conflicts
  - Macro overlay applies multipliers correctly

Não testamos contra DBs reais (depende de estado mutável). Usa mocks
quando tem que tocar persistência.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategies._base import (
    StrategyOutput,
    Verdict,
    details_to_pass_count,
    verdict_from_pass_ratio,
)


# ============================================================
# Foundation
# ============================================================
def test_strategy_output_serializes():
    o = StrategyOutput(
        ticker="X", market="us", engine="t",
        score=0.5, verdict="HOLD",
    )
    d = o.as_dict()
    assert d["score"] == 0.5
    assert d["verdict"] == "HOLD"
    assert d["weight_suggestion"] == 0.0


def test_verdict_from_pass_ratio():
    assert verdict_from_pass_ratio(5, 5) == "BUY"      # 100% >= 0.85
    assert verdict_from_pass_ratio(4, 5) == "HOLD"     # 80% < 0.85, >= 0.60
    assert verdict_from_pass_ratio(3, 5) == "HOLD"     # 60% == 0.60
    assert verdict_from_pass_ratio(2, 5) == "AVOID"    # 40% < 0.60
    assert verdict_from_pass_ratio(0, 0) == "N/A"


def test_details_to_pass_count_ignores_na():
    details = {
        "a": {"verdict": "pass"},
        "b": {"verdict": "pass"},
        "c": {"verdict": "fail"},
        "d": {"verdict": "n/a"},
        "e": "not a dict",  # ignored
    }
    p, app = details_to_pass_count(details)
    assert p == 2
    assert app == 3   # n/a + non-dict ignored


# ============================================================
# Hedge — pure logic, no DB needed (mocks classify)
# ============================================================
def test_hedge_off_in_expansion():
    from analytics.regime import Regime
    from strategies import hedge as hedge_mod

    fake = Regime(market="us", regime="expansion", confidence="high")
    with patch("strategies.hedge.classify", return_value=fake):
        # Clear LRU cache from earlier tests
        hedge_mod._triggers.cache_clear()
        p = hedge_mod.propose_hedge("us")
        assert p["active"] is False
        assert p["hedge_size_pct"] == 0.0
        assert p["regime"] == "expansion"


def test_hedge_on_in_recession():
    from analytics.regime import Regime
    from strategies import hedge as hedge_mod

    fake = Regime(market="us", regime="recession", confidence="high")
    with patch("strategies.hedge.classify", return_value=fake):
        p = hedge_mod.propose_hedge("us", portfolio_value=100_000)
        assert p["active"] is True
        assert p["hedge_size_pct"] == 0.10
        assert p["notional"] == 10_000
        assert "SH" in p["instruments"]


def test_hedge_late_cycle_partial():
    from analytics.regime import Regime
    from strategies import hedge as hedge_mod

    fake = Regime(market="us", regime="late_cycle", confidence="medium")
    with patch("strategies.hedge.classify", return_value=fake):
        p = hedge_mod.propose_hedge("us")
        assert p["active"] is True
        assert p["hedge_size_pct"] == 0.05


def test_hedge_status_string():
    from analytics.regime import Regime
    from strategies import hedge as hedge_mod

    fake = Regime(market="us", regime="expansion", confidence="high")
    with patch("strategies.hedge.classify", return_value=fake):
        s = hedge_mod.status("us")
        assert "HEDGE OFF" in s
        assert "expansion" in s


# ============================================================
# Macro — overlay logic with mocked regime + sector
# ============================================================
def test_macro_tilt_up_returns_buy():
    from analytics.regime import Regime
    from strategies import macro as macro_mod

    fake = Regime(market="us", regime="expansion", confidence="high")
    with patch("strategies.macro.classify", return_value=fake), \
         patch("strategies.macro._ticker_sector", return_value="technology"):
        macro_mod._regime_for.cache_clear()
        macro_mod._overlays.cache_clear()
        out = macro_mod.evaluate("AAPL", "us")
        assert out.verdict == "BUY"
        assert out.score == round(1.5 / 1.5, 4)
        assert out.rationale["tilt"] == "tilt_up"


def test_macro_tilt_down_returns_avoid():
    from analytics.regime import Regime
    from strategies import macro as macro_mod

    fake = Regime(market="us", regime="expansion", confidence="high")
    with patch("strategies.macro.classify", return_value=fake), \
         patch("strategies.macro._ticker_sector", return_value="staples"):
        macro_mod._regime_for.cache_clear()
        out = macro_mod.evaluate("PG", "us")
        assert out.verdict == "AVOID"
        assert out.rationale["tilt"] == "tilt_down"


def test_macro_neutral_when_no_sector():
    from analytics.regime import Regime
    from strategies import macro as macro_mod

    fake = Regime(market="us", regime="expansion", confidence="medium")
    with patch("strategies.macro.classify", return_value=fake), \
         patch("strategies.macro._ticker_sector", return_value=None):
        macro_mod._regime_for.cache_clear()
        out = macro_mod.evaluate("XYZ", "us")
        assert out.verdict == "HOLD"
        assert out.rationale["tilt"] == "neutral"


# ============================================================
# Portfolio Engine — uses mocked engines for deterministic test
# ============================================================
def test_portfolio_engine_combines():
    from strategies import portfolio_engine

    def fake_eval(engine_name, scores: dict):
        def _f(ticker, market):
            score = scores.get(ticker, 0.0)
            verdict = "BUY" if score >= 0.85 else ("HOLD" if score >= 0.6 else "AVOID")
            return StrategyOutput(
                ticker=ticker, market=market, engine=engine_name,
                score=score, verdict=verdict,
                rationale={"multiplier": 1.0} if engine_name == "macro" else {},
            )
        return _f

    with patch("strategies.portfolio_engine.graham") as g, \
         patch("strategies.portfolio_engine.buffett") as b, \
         patch("strategies.portfolio_engine.drip") as d, \
         patch("strategies.portfolio_engine.macro") as m, \
         patch("strategies.portfolio_engine.hedge") as h:
        g.name = "graham"
        b.name = "buffett"
        d.name = "drip"
        m.name = "macro"
        h.name = "hedge"
        b.evaluate.side_effect = fake_eval("buffett", {"AAPL": 0.9, "JNJ": 0.4})
        d.evaluate.side_effect = fake_eval("drip", {"AAPL": 0.5, "JNJ": 0.9})
        m.evaluate.side_effect = fake_eval("macro", {"AAPL": 1.0, "JNJ": 1.0})
        h.evaluate.side_effect = fake_eval("hedge", {"AAPL": 0.5, "JNJ": 0.5})
        m.current_regime.return_value = {"regime": "expansion", "confidence": "high"}
        h.propose_hedge.return_value = {"active": False, "hedge_size_pct": 0.0,
                                         "instruments": [], "regime": "expansion"}
        proposal = portfolio_engine.combine(
            market="us", tickers=["AAPL", "JNJ"],
        )
    # AAPL has more BUY signals → should rank first
    assert "AAPL" in proposal.target_weights
    weights = proposal.target_weights
    assert weights.get("AAPL", 0) >= weights.get("JNJ", 0)


def test_portfolio_engine_empty_universe():
    from strategies import portfolio_engine
    proposal = portfolio_engine.combine(market="us", tickers=[])
    assert proposal.target_weights == {}
    assert "No tickers" in proposal.notes[0]


# ============================================================
# ROIC
# ============================================================
def test_roic_computes_when_data_present(tmp_path):
    """Build a tiny fake DB with one annual row and assert ROIC math."""
    import sqlite3
    db = tmp_path / "fake.db"
    with sqlite3.connect(db) as c:
        c.execute("""CREATE TABLE deep_fundamentals (
            ticker TEXT, period_type TEXT, period_end TEXT,
            ebit REAL, stockholders_equity REAL, total_debt REAL
        )""")
        c.execute(
            "INSERT INTO deep_fundamentals VALUES (?, ?, ?, ?, ?, ?)",
            ("X", "annual", "2024-12-31", 1000.0, 5000.0, 2000.0),
        )
    from scoring import roic as roic_mod
    with patch.object(roic_mod, "DB_US", db):
        r = roic_mod.compute("X", "us")
    # ROIC = 1000 * 0.79 / (5000 + 2000) = 790 / 7000 ≈ 0.1129
    assert r == pytest.approx(0.1129, abs=0.01)


def test_roic_returns_none_on_missing():
    from scoring import roic as roic_mod
    r = roic_mod.compute("NONEXISTENT_TICKER_XYZ", "us")
    assert r is None
