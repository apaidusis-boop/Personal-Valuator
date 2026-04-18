"""Testes de narrative/regime.py.

Testes unitários das funções puras (rate/growth/fx) com séries sintéticas,
mais um smoke test end-to-end contra a DB real (skip se ausente).

Corre com: python -m unittest tests.test_regime -v
"""
from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path

from narrative.regime import (
    BR_LOOKBACK_START,
    _classify_fx_br,
    _classify_growth_br,
    _classify_rate_br,
    _ipca_yoy,
    classify_br,
    current,
)

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"


class TestRateBR(unittest.TestCase):
    def test_tightening(self):
        series = [("2024-01-15", 10.0), ("2024-04-15", 11.0)]
        regime, details = _classify_rate_br(series, "2024-04-15")
        self.assertEqual(regime, "tightening")
        self.assertGreater(details["delta_pp"], 0)

    def test_easing(self):
        series = [("2024-01-15", 13.75), ("2024-04-15", 10.5)]
        regime, details = _classify_rate_br(series, "2024-04-15")
        self.assertEqual(regime, "easing")
        self.assertLess(details["delta_pp"], 0)

    def test_hold_small_delta(self):
        series = [("2024-01-15", 10.0), ("2024-04-15", 10.25)]
        regime, _ = _classify_rate_br(series, "2024-04-15")
        self.assertEqual(regime, "hold")

    def test_insufficient_data(self):
        series = [("2024-04-15", 10.0)]
        regime, details = _classify_rate_br(series, "2024-04-15")
        self.assertEqual(regime, "hold")
        self.assertEqual(details["reason"], "insufficient_data")


class TestIpcaYoY(unittest.TestCase):
    def test_simple_compound(self):
        # 12 meses de 0.5% a.m. → ~6.17% YoY
        series = [(f"2024-{m:02d}-01", 0.5) for m in range(1, 13)]
        yoy = _ipca_yoy(series, "2024-12-01")
        self.assertAlmostEqual(yoy, 6.17, places=1)

    def test_deflation(self):
        series = [(f"2024-{m:02d}-01", -0.1) for m in range(1, 13)]
        yoy = _ipca_yoy(series, "2024-12-01")
        self.assertLess(yoy, 0)

    def test_none_if_short(self):
        series = [("2024-01-01", 0.5)]
        self.assertIsNone(_ipca_yoy(series, "2024-06-01"))


class TestGrowthBR(unittest.TestCase):
    def test_high_inflation_slowdown(self):
        series = [(f"2024-{m:02d}-01", 0.7) for m in range(1, 13)]  # ~8.7% YoY
        regime, details = _classify_growth_br(series, "2024-12-01")
        self.assertEqual(regime, "slowdown")
        self.assertGreater(details["ipca_yoy_pct"], 6.0)

    def test_low_inflation_expansion(self):
        series = [(f"2024-{m:02d}-01", 0.15) for m in range(1, 13)]  # ~1.8% YoY
        regime, _ = _classify_growth_br(series, "2024-12-01")
        self.assertEqual(regime, "expansion")


class TestFxBR(unittest.TestCase):
    def _build_flat(self, value: float, n: int = 210):
        return [(f"2024-01-{i:02d}".replace("2024-01-32", "2024-02-01"), value)
                for i in range(1, n + 1)]

    def test_weak_local_when_above_ma(self):
        # MA 200 ~= 5.0, latest = 5.50 → +10% → weak_local
        series = [("2024-01-01", 5.0)] * 200 + [("2024-07-20", 5.50)]
        regime, details = _classify_fx_br(series, "2024-07-20")
        self.assertEqual(regime, "weak_local")
        self.assertGreater(details["deviation"], 0.05)

    def test_strong_local_when_below_ma(self):
        series = [("2024-01-01", 5.0)] * 200 + [("2024-07-20", 4.50)]
        regime, details = _classify_fx_br(series, "2024-07-20")
        self.assertEqual(regime, "strong_local")
        self.assertLess(details["deviation"], -0.05)

    def test_neutral_band(self):
        series = [("2024-01-01", 5.0)] * 200 + [("2024-07-20", 5.05)]
        regime, _ = _classify_fx_br(series, "2024-07-20")
        self.assertEqual(regime, "neutral")

    def test_insufficient_data(self):
        series = [("2024-01-01", 5.0)] * 50
        regime, details = _classify_fx_br(series, "2024-01-30")
        self.assertEqual(regime, "neutral")
        self.assertEqual(details["reason"], "insufficient_data")


@unittest.skipUnless(DB_BR.exists(), "DB BR não disponível")
class TestClassifyBREndToEnd(unittest.TestCase):
    """Smoke test contra a DB real. Verifica que:
      - classify_br corre sem erro
      - a última linha é consistente com a tabela series
      - é idempotente (corre 2x, mesmo número de linhas)
    """

    def test_idempotent(self):
        n1 = classify_br()
        n2 = classify_br()
        self.assertEqual(n1, n2)

    def test_current_reads_last_row(self):
        classify_br()
        latest = current(DB_BR, "br")
        self.assertIsNotNone(latest)
        self.assertEqual(latest.market, "br")
        self.assertIn(latest.rate, ("tightening", "easing", "hold"))

    def test_latest_date_matches_usdbrl(self):
        """A última data do macro_regime deve coincidir com a última data
        da série USDBRL_PTAX (é a grelha temporal usada)."""
        classify_br()
        with sqlite3.connect(DB_BR) as conn:
            last_regime = conn.execute(
                "SELECT MAX(date) FROM macro_regime WHERE market='br'"
            ).fetchone()[0]
            last_usd = conn.execute(
                "SELECT MAX(date) FROM series WHERE series_id='USDBRL_PTAX' AND date >= ?",
                (BR_LOOKBACK_START,),
            ).fetchone()[0]
        self.assertEqual(last_regime, last_usd)


if __name__ == "__main__":
    unittest.main()
