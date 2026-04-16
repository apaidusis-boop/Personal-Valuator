"""Testes do motor de valuation (scoring/valuation.py).

Testa a lógica pura do DDM Gordon sem tocar na rede nem na DB.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scoring.valuation import (  # noqa: E402
    compute_cagr,
    gordon_fair_value,
    DISCOUNT_RATE,
    SAFETY_SPREAD,
    ABSOLUTE_G_CAP,
    MARGIN_OF_SAFETY,
)


class TestComputeCAGR(unittest.TestCase):

    def test_steady_growth(self):
        """5 anos de dividendos crescentes."""
        divs = [
            {"year": 2020, "amount": 1.00},
            {"year": 2021, "amount": 1.10},
            {"year": 2022, "amount": 1.21},
            {"year": 2023, "amount": 1.331},
            {"year": 2024, "amount": 1.4641},
            {"year": 2025, "amount": 1.61051},
        ]
        cagr, years, start = compute_cagr(divs, window=5)
        self.assertIsNotNone(cagr)
        self.assertAlmostEqual(cagr, 0.10, places=2)
        self.assertEqual(years, 5)
        self.assertEqual(start, 2020)

    def test_flat_dividends(self):
        """Dividendos iguais → CAGR = 0."""
        divs = [{"year": y, "amount": 1.0} for y in range(2020, 2026)]
        cagr, years, start = compute_cagr(divs)
        self.assertIsNotNone(cagr)
        self.assertAlmostEqual(cagr, 0.0, places=4)

    def test_single_year(self):
        """Menos de 2 anos → CAGR indisponível."""
        divs = [{"year": 2024, "amount": 1.0}]
        cagr, years, start = compute_cagr(divs)
        self.assertIsNone(cagr)

    def test_empty(self):
        cagr, years, start = compute_cagr([])
        self.assertIsNone(cagr)
        self.assertEqual(years, 0)

    def test_ignores_current_year(self):
        """O ano corrente é ignorado (pode estar incompleto)."""
        from datetime import datetime
        current = datetime.now().year
        divs = [
            {"year": current - 2, "amount": 1.0},
            {"year": current - 1, "amount": 1.1},
            {"year": current, "amount": 0.3},  # parcial
        ]
        cagr, years, start = compute_cagr(divs)
        self.assertIsNotNone(cagr)
        self.assertAlmostEqual(cagr, 0.10, places=2)

    def test_zero_amount_ignored(self):
        """Anos com amount=0 são ignorados."""
        divs = [
            {"year": 2022, "amount": 1.0},
            {"year": 2023, "amount": 0},
            {"year": 2024, "amount": 1.21},
        ]
        cagr, years, start = compute_cagr(divs)
        self.assertIsNotNone(cagr)
        self.assertEqual(years, 2)


class TestGordonFairValue(unittest.TestCase):

    def test_basic(self):
        """Gordon: P = D1 / (r - g) = D0*(1+g) / (r - g)."""
        d0, g, r = 1.0, 0.05, 0.10
        expected = d0 * (1 + g) / (r - g)  # 1.05 / 0.05 = 21.0
        self.assertAlmostEqual(gordon_fair_value(d0, g, r), expected, places=4)

    def test_higher_growth(self):
        """Maior crescimento → maior fair value."""
        fv_low = gordon_fair_value(1.0, 0.03, 0.10)
        fv_high = gordon_fair_value(1.0, 0.06, 0.10)
        self.assertGreater(fv_high, fv_low)

    def test_higher_discount_rate(self):
        """Maior taxa de desconto → menor fair value."""
        fv_low_r = gordon_fair_value(1.0, 0.05, 0.08)
        fv_high_r = gordon_fair_value(1.0, 0.05, 0.12)
        self.assertGreater(fv_low_r, fv_high_r)


class TestDiscountRateConstants(unittest.TestCase):

    def test_br_rate(self):
        self.assertEqual(DISCOUNT_RATE["br"], 0.14)

    def test_us_rate(self):
        self.assertEqual(DISCOUNT_RATE["us"], 0.09)

    def test_safety_spread(self):
        self.assertEqual(SAFETY_SPREAD, 0.04)

    def test_margin_of_safety(self):
        self.assertEqual(MARGIN_OF_SAFETY, 0.25)

    def test_g_cap_br(self):
        self.assertEqual(ABSOLUTE_G_CAP["br"], 0.06)

    def test_g_cap_us(self):
        self.assertEqual(ABSOLUTE_G_CAP["us"], 0.05)

    def test_g_cap_below_rate(self):
        """Cap de g deve ser inferior a r para o denominador não explodir."""
        for market in ("br", "us"):
            r = DISCOUNT_RATE[market]
            cap = min(r - SAFETY_SPREAD, ABSOLUTE_G_CAP[market])
            self.assertGreater(r - cap, 0, msg=f"{market}: r-g_cap deve ser positivo")


if __name__ == "__main__":
    unittest.main()
