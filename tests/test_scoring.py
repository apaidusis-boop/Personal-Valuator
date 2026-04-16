"""Testes do motor de scoring (scoring/engine.py).

Nunca toca na rede nem na DB real. Testa a lógica pura dos critérios.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scoring.engine import (  # noqa: E402
    score_br,
    score_br_fii,
    score_us,
    aggregate,
)


def _snap(*, sector="Banks", eps=2.0, bvps=10.0, roe=0.18, pe=8.0, pb=1.5,
          dy=0.07, net_debt_ebitda=2.0, dividend_streak_years=10,
          is_aristocrat=None, price=15.0):
    """Helper para criar um snapshot de teste."""
    return {
        "ticker": "TEST",
        "name": "Test Co",
        "sector": sector,
        "is_in_portfolio": True,
        "currency": "BRL",
        "fundamentals": {
            "period_end": "2026-01-01",
            "eps": eps, "bvps": bvps, "roe": roe,
            "pe": pe, "pb": pb, "dy": dy,
            "net_debt_ebitda": net_debt_ebitda,
            "dividend_streak_years": dividend_streak_years,
            "is_aristocrat": is_aristocrat,
        },
        "price": {"close": price, "date": "2026-04-15"},
    }


class TestScoreBR(unittest.TestCase):

    def test_all_pass(self):
        """Empresa saudável com todos os critérios a passar."""
        snap = _snap(eps=2.0, bvps=10.0, price=6.0, dy=0.08, roe=0.20,
                     net_debt_ebitda=1.5, dividend_streak_years=10)
        details = score_br(snap)
        score, passes = aggregate(details)
        self.assertTrue(passes)
        self.assertEqual(score, 1.0)
        for k, v in details.items():
            self.assertIn(v["verdict"], ("pass", "n/a"), msg=f"{k} should pass")

    def test_all_fail(self):
        """Empresa com todos os critérios a falhar."""
        snap = _snap(eps=0.5, bvps=2.0, price=100.0, dy=0.01, roe=0.05,
                     net_debt_ebitda=5.0, dividend_streak_years=2)
        details = score_br(snap)
        score, passes = aggregate(details)
        self.assertFalse(passes)
        self.assertEqual(score, 0.0)

    def test_holding_company_na(self):
        """Holdings (ITSA4) devem ter net_debt_ebitda como n/a."""
        snap = _snap(sector="Holding", net_debt_ebitda=2.5)
        details = score_br(snap)
        self.assertEqual(details["net_debt_ebitda"]["verdict"], "n/a")
        self.assertIn("holding company", details["net_debt_ebitda"]["reason"])

    def test_missing_eps_na(self):
        """EPS None → graham_number deve ser n/a."""
        snap = _snap(eps=None)
        details = score_br(snap)
        self.assertEqual(details["graham_number"]["verdict"], "n/a")

    def test_negative_eps_na(self):
        """EPS negativo → graham_number deve ser n/a."""
        snap = _snap(eps=-1.0)
        details = score_br(snap)
        self.assertEqual(details["graham_number"]["verdict"], "n/a")

    def test_graham_number_pass(self):
        """Graham Number deve passar quando preço <= sqrt(22.5 * EPS * BVPS)."""
        import math
        eps, bvps = 2.0, 10.0
        gn = math.sqrt(22.5 * eps * bvps)
        snap = _snap(eps=eps, bvps=bvps, price=gn - 1)
        details = score_br(snap)
        self.assertEqual(details["graham_number"]["verdict"], "pass")

    def test_graham_number_fail(self):
        """Graham Number deve falhar quando preço > sqrt(22.5 * EPS * BVPS)."""
        import math
        eps, bvps = 2.0, 10.0
        gn = math.sqrt(22.5 * eps * bvps)
        snap = _snap(eps=eps, bvps=bvps, price=gn + 10)
        details = score_br(snap)
        self.assertEqual(details["graham_number"]["verdict"], "fail")

    def test_mixed_pass_and_fail(self):
        """Score parcial com mix de pass e fail."""
        snap = _snap(dy=0.01, roe=0.05, net_debt_ebitda=1.0,
                     dividend_streak_years=10, eps=2.0, bvps=10.0, price=6.0)
        details = score_br(snap)
        score, passes = aggregate(details)
        self.assertFalse(passes)
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)


class TestScoreBRFII(unittest.TestCase):

    def _fii_snap(self, **kwargs):
        defaults = {
            "ticker": "TEST11", "name": "Test FII", "segment": "Shopping",
            "is_in_portfolio": True,
            "fundamentals": {
                "period_end": "2026-01-01",
                "price": 100.0, "vpa": 110.0, "pvp": 0.91,
                "dy_12m": 0.10,
                "avg_monthly_rendimento_24m": 0.90,
                "physical_vacancy": 0.05,
                "distribution_streak_months": 24,
                "adtv_daily": 1_000_000,
                "segment_anbima": "Shopping / Varejo",
            },
        }
        if kwargs:
            defaults["fundamentals"].update(kwargs)
        return defaults

    def test_all_pass(self):
        details = score_br_fii(self._fii_snap())
        score, passes = aggregate(details)
        self.assertTrue(passes)
        self.assertEqual(score, 1.0)

    def test_papel_fii_vacancy_na(self):
        """FIIs de papel devem ter vacância como n/a."""
        snap = self._fii_snap(segment_anbima="Títulos e Valores Imobiliários (CRI)")
        details = score_br_fii(snap)
        self.assertEqual(details["vacancy"]["verdict"], "n/a")

    def test_low_dy_fails(self):
        snap = self._fii_snap(dy_12m=0.05)
        details = score_br_fii(snap)
        self.assertEqual(details["dividend_yield"]["verdict"], "fail")

    def test_high_pvp_fails(self):
        snap = self._fii_snap(pvp=1.20)
        details = score_br_fii(snap)
        self.assertEqual(details["price_to_book"]["verdict"], "fail")

    def test_low_liquidity_fails(self):
        snap = self._fii_snap(adtv_daily=100_000)
        details = score_br_fii(snap)
        self.assertEqual(details["liquidity"]["verdict"], "fail")


class TestScoreUS(unittest.TestCase):

    def test_all_pass_aristocrat(self):
        snap = _snap(pe=15, pb=2.0, dy=0.03, roe=0.20,
                     is_aristocrat=True, dividend_streak_years=30)
        details = score_us(snap)
        score, passes = aggregate(details)
        self.assertTrue(passes)
        self.assertEqual(score, 1.0)

    def test_high_pe_fails(self):
        snap = _snap(pe=35, pb=2.0, dy=0.03, roe=0.20, is_aristocrat=True)
        details = score_us(snap)
        self.assertEqual(details["pe"]["verdict"], "fail")

    def test_non_aristocrat_with_streak(self):
        """Streak >= 10 sem ser aristocrat ainda passa."""
        snap = _snap(pe=15, pb=2.0, dy=0.03, roe=0.20,
                     is_aristocrat=False, dividend_streak_years=15)
        details = score_us(snap)
        self.assertEqual(details["aristocrat"]["verdict"], "pass")

    def test_short_streak_fails(self):
        snap = _snap(pe=15, pb=2.0, dy=0.03, roe=0.20,
                     is_aristocrat=False, dividend_streak_years=5)
        details = score_us(snap)
        self.assertEqual(details["aristocrat"]["verdict"], "fail")


class TestAggregate(unittest.TestCase):

    def test_empty_details(self):
        score, passes = aggregate({})
        self.assertEqual(score, 0.0)
        self.assertFalse(passes)

    def test_all_na(self):
        details = {
            "a": {"value": None, "threshold": 1, "verdict": "n/a"},
            "b": {"value": None, "threshold": 2, "verdict": "n/a"},
        }
        score, passes = aggregate(details)
        self.assertEqual(score, 0.0)
        self.assertFalse(passes)

    def test_mix_with_na_ignored(self):
        details = {
            "a": {"value": 1, "threshold": 1, "verdict": "pass"},
            "b": {"value": None, "threshold": 2, "verdict": "n/a"},
            "c": {"value": 3, "threshold": 1, "verdict": "pass"},
        }
        score, passes = aggregate(details)
        self.assertTrue(passes)
        self.assertEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
