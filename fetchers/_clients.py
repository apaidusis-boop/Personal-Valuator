"""Skeleton REST clients for paid data providers (FMP, EODHD, Benzinga).

Não-implementados ainda. Existem para:
  1. Documentar o contrato esperado (rate limits, endpoints, auth).
  2. Permitir registrar adapters em REGISTRY que falham com NotImplementedError
     em vez de ImportError silencioso quando a API key não está configurada.
  3. Quando o user adquirir uma key, basta substituir o corpo da classe.

Convenção: cada cliente expõe `is_available()` (verifica env var) e métodos
get_* que devolvem dict normalizado (não o JSON cru do provider).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _read_env_key(name: str) -> str | None:
    """Lê env var ou .env (mirror do pattern em massive_fetcher.py)."""
    val = os.environ.get(name)
    if val:
        return val.strip()
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(f"{name}=") or line.startswith(f"{name} ="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# ============================================================
# FMP (Financial Modeling Prep) — paid; fundamentals + analyst consensus
# ============================================================
class FMPClient:
    """Financial Modeling Prep — fundamentals primário pago.

    Tier Starter (~$15/mês): 250 req/dia, 5 anos history, US + 35 mercados.
    Tier Premium ($50/mês): 750 req/dia, 30 anos, real-time intraday.

    Endpoints planeados:
      - /api/v3/income-statement/{ticker}
      - /api/v3/balance-sheet-statement/{ticker}
      - /api/v3/cash-flow-statement/{ticker}
      - /api/v3/key-metrics/{ticker}
      - /api/v3/analyst-estimates/{ticker}
      - /api/v3/historical-price-full/{ticker}

    Env: FMP_API_KEY
    """
    BASE_URL = "https://financialmodelingprep.com"

    def __init__(self):
        self.api_key = _read_env_key("FMP_API_KEY")

    def is_available(self) -> bool:
        return self.api_key is not None

    def get_fundamentals(self, ticker: str, years: int = 5) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        raise NotImplementedError("FMPClient.get_fundamentals not implemented")

    def get_analyst_consensus(self, ticker: str) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        raise NotImplementedError("FMPClient.get_analyst_consensus not implemented")

    def get_price(self, ticker: str, date: str | None = None) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        raise NotImplementedError("FMPClient.get_price not implemented")


# ============================================================
# EODHD (End-of-Day Historical Data) — paid; reliable EOD prices
# ============================================================
class EODHDClient:
    """EOD Historical Data — preços EOD pagos, alternativa a yfinance.

    Tier All-in-One ($20/mês): unlimited symbols, EOD + intraday + fundamentals.
    Cobre 70+ exchanges incluindo B3 (com sufixo .SA).

    Endpoints planeados:
      - /api/eod/{ticker}
      - /api/real-time/{ticker}
      - /api/fundamentals/{ticker}

    Env: EODHD_API_KEY
    """
    BASE_URL = "https://eodhd.com"

    def __init__(self):
        self.api_key = _read_env_key("EODHD_API_KEY")

    def is_available(self) -> bool:
        return self.api_key is not None

    def get_price(self, ticker: str, date: str | None = None) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("EODHD_API_KEY not configured")
        raise NotImplementedError("EODHDClient.get_price not implemented")

    def get_eod_history(self, ticker: str, from_date: str, to_date: str) -> list[dict]:
        if not self.is_available():
            raise NotImplementedError("EODHD_API_KEY not configured")
        raise NotImplementedError("EODHDClient.get_eod_history not implemented")

    def get_fundamentals(self, ticker: str) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("EODHD_API_KEY not configured")
        raise NotImplementedError("EODHDClient.get_fundamentals not implemented")


# ============================================================
# Benzinga (analyst consensus + news) — via Massive ou directo
# ============================================================
class BenzingaClient:
    """Benzinga — consensus + news; via Massive subscription (futuro).

    Hoje acessível pela Polygon/Massive premium tier; standalone Benzinga
    Pro: $99/mês. Endpoints relevantes: /benzinga/v1/ratings,
    /benzinga/v1/calendar/earnings.

    Env: BENZINGA_API_KEY ou MASSIVE_API_KEY (com tier suficiente).
    """

    def __init__(self):
        self.api_key = _read_env_key("BENZINGA_API_KEY") or _read_env_key("MASSIVE_API_KEY")

    def is_available(self) -> bool:
        return self.api_key is not None

    def get_analyst_consensus(self, ticker: str) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("BENZINGA_API_KEY / MASSIVE_API_KEY not configured")
        raise NotImplementedError("BenzingaClient.get_analyst_consensus not implemented")


# ============================================================
# Singleton accessors (lazy)
# ============================================================
_singletons: dict[str, Any] = {}


def fmp() -> FMPClient:
    if "fmp" not in _singletons:
        _singletons["fmp"] = FMPClient()
    return _singletons["fmp"]


def eodhd() -> EODHDClient:
    if "eodhd" not in _singletons:
        _singletons["eodhd"] = EODHDClient()
    return _singletons["eodhd"]


def benzinga() -> BenzingaClient:
    if "benzinga" not in _singletons:
        _singletons["benzinga"] = BenzingaClient()
    return _singletons["benzinga"]


def availability_report() -> dict[str, bool]:
    """Diagnóstico: quais providers estão acessíveis com auth válida."""
    return {
        "fmp": fmp().is_available(),
        "eodhd": eodhd().is_available(),
        "benzinga": benzinga().is_available(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(availability_report(), indent=2))
