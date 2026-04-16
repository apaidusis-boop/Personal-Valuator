"""Testes do módulo analytics (loaders, total_return, compare).

Usa uma DB em memória populada com dados de teste. Não toca na rede.
Requer pandas — skip automático se não estiver instalado.
"""
from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import pandas  # noqa: F401
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def _create_test_db() -> sqlite3.Connection:
    """Cria DB em memória com schema e dados de teste."""
    conn = sqlite3.connect(":memory:")
    schema_path = ROOT / "scripts" / "init_db.py"
    # Extrair schema do init_db.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("init_db", schema_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    conn.executescript(mod.SCHEMA)

    # Seed: empresa + preços + dividendos
    conn.execute(
        "INSERT INTO companies (ticker, name, sector, is_holding, currency) VALUES (?,?,?,?,?)",
        ("TEST", "Test Corp", "Tech", 0, "BRL"),
    )
    # 5 dias de preços
    prices = [
        ("TEST", "2026-04-10", 10.00, 1000),
        ("TEST", "2026-04-11", 10.50, 1100),
        ("TEST", "2026-04-12", 10.20, 900),
        ("TEST", "2026-04-13", 10.80, 1200),
        ("TEST", "2026-04-14", 11.00, 1000),
    ]
    conn.executemany(
        "INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)", prices
    )
    # Dividendo no dia 12
    conn.execute(
        "INSERT INTO dividends (ticker, ex_date, pay_date, amount, currency, kind, source, fetched_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        ("TEST", "2026-04-12", "2026-04-15", 0.50, "BRL", "cash", "test", "2026-04-15T00:00:00Z"),
    )
    # Série macro (SELIC daily — 3 dias)
    conn.execute(
        "INSERT INTO series_meta (series_id, description, unit, frequency, source_primary) "
        "VALUES (?,?,?,?,?)",
        ("SELIC_DAILY", "SELIC diária", "pct_daily", "daily", "test"),
    )
    for date, val in [("2026-04-10", 0.000489), ("2026-04-11", 0.000489), ("2026-04-14", 0.000489)]:
        conn.execute(
            "INSERT INTO series (series_id, date, value, source, fetched_at) VALUES (?,?,?,?,?)",
            ("SELIC_DAILY", date, val, "test", "2026-04-15T00:00:00Z"),
        )
    conn.commit()
    return conn


@unittest.skipUnless(HAS_PANDAS, "pandas not installed")
class TestLoaders(unittest.TestCase):

    def setUp(self):
        self.conn = _create_test_db()
        # Patch analytics.loaders para usar a nossa DB em memória
        import analytics.loaders as loaders
        self._orig_connect = sqlite3.connect
        self.loaders = loaders

    def test_load_prices(self):
        with patch.object(sqlite3, "connect", return_value=self.conn):
            df = self.loaders.load_prices("TEST", "2026-04-10", "2026-04-14")
        self.assertEqual(len(df), 5)
        self.assertAlmostEqual(df.iloc[0]["close"], 10.00)
        self.assertAlmostEqual(df.iloc[-1]["close"], 11.00)

    def test_load_dividends(self):
        with patch.object(sqlite3, "connect", return_value=self.conn):
            df = self.loaders.load_dividends("TEST", "2026-04-10", "2026-04-15")
        self.assertEqual(len(df), 1)
        self.assertAlmostEqual(df.iloc[0]["amount"], 0.50)

    def test_load_series(self):
        with patch.object(sqlite3, "connect", return_value=self.conn):
            df = self.loaders.load_series("SELIC_DAILY", "2026-04-10", "2026-04-14")
        self.assertEqual(len(df), 3)

    def tearDown(self):
        self.conn.close()


@unittest.skipUnless(HAS_PANDAS, "pandas not installed")
class TestTotalReturn(unittest.TestCase):

    def setUp(self):
        self.conn = _create_test_db()

    def test_total_return_includes_dividend(self):
        """TR deve ser maior que price return quando há dividendos."""
        with patch.object(sqlite3, "connect", return_value=self.conn):
            from analytics.total_return import total_return_series
            df = total_return_series("TEST", "2026-04-10", "2026-04-14")
        # Price return: 11.00 / 10.00 - 1 = 10%
        price_return = df.iloc[-1]["close"] / df.iloc[0]["close"] - 1
        # TR return deve ser > price return por causa do dividendo
        tr_return = df.iloc[-1]["tr_factor"] - 1
        self.assertGreater(tr_return, price_return)

    def test_no_dividend_tr_equals_price(self):
        """Sem dividendos, TR factor segue apenas variação de preço."""
        # Remover dividendo
        self.conn.execute("DELETE FROM dividends WHERE ticker='TEST'")
        self.conn.commit()
        with patch.object(sqlite3, "connect", return_value=self.conn):
            from analytics.total_return import total_return_series
            df = total_return_series("TEST", "2026-04-10", "2026-04-14")
        price_return = df.iloc[-1]["close"] / df.iloc[0]["close"] - 1
        tr_return = df.iloc[-1]["tr_factor"] - 1
        self.assertAlmostEqual(tr_return, price_return, places=4)

    def tearDown(self):
        self.conn.close()


if __name__ == "__main__":
    unittest.main()
