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

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"


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


def _log(provider: str, event: dict) -> None:
    """JSON line em logs/<provider>_fetcher.log (mirror do pattern em massive_fetcher)."""
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps(
        {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **event},
        ensure_ascii=False,
        default=str,
    )
    with (LOG_DIR / f"{provider}_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ============================================================
# FMP (Financial Modeling Prep) — paid; fundamentals + analyst consensus
# ============================================================
class FMPClient:
    """Financial Modeling Prep — fundamentals + analyst consensus.

    Tier Free (registo simples): 250 req/dia, US apenas.
    Tier Starter (~$15/mês): 750 req/dia, 35 mercados.
    Tier Premium ($50/mês): real-time intraday + 30 anos.

    Endpoints usados (namespace /stable/, novo desde 2024):
      - /stable/ratios-ttm?symbol=X        — pe/pb/dy/bvps/eps TTM
      - /stable/key-metrics-ttm?symbol=X   — marketCap/ev_ebitda/roe/fcf TTM
      - /stable/price-target-consensus     — analyst targets (high/low/median)
      - /stable/analyst-estimates?symbol=X — eps/revenue forward estimates

    Env: FMP_API_KEY (em .env ou env var).
    """
    BASE_URL = "https://financialmodelingprep.com"
    TIMEOUT = 15
    THROTTLE_SEC = 0.25  # 4 req/s ceiling — conservador, todos os tiers cabem

    def __init__(self):
        self.api_key = _read_env_key("FMP_API_KEY")
        self._last_call = 0.0

    def is_available(self) -> bool:
        return self.api_key is not None

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.api_key:
            raise NotImplementedError("FMP_API_KEY not configured")
        delta = time.time() - self._last_call
        if delta < self.THROTTLE_SEC:
            time.sleep(self.THROTTLE_SEC - delta)
        full_params = dict(params or {})
        full_params["apikey"] = self.api_key
        url = f"{self.BASE_URL}{path}"
        try:
            resp = requests.get(url, params=full_params, timeout=self.TIMEOUT)
        except requests.RequestException as e:
            _log("fmp", {"path": path, "error": f"network: {e}"})
            raise RuntimeError(f"fmp: network error for {path}: {e}") from e
        finally:
            self._last_call = time.time()
        if resp.status_code == 401:
            _log("fmp", {"path": path, "error": "401 unauthorized"})
            raise RuntimeError("fmp: 401 — FMP_API_KEY inválida ou expirada")
        if resp.status_code == 403:
            _log("fmp", {"path": path, "error": "403 forbidden"})
            raise RuntimeError(f"fmp: 403 — endpoint fora do tier ({path})")
        if resp.status_code == 429:
            _log("fmp", {"path": path, "error": "429 rate-limited"})
            raise RuntimeError("fmp: 429 — quota diária excedida")
        if resp.status_code == 404:
            _log("fmp", {"path": path, "error": "404 not found"})
            raise RuntimeError(f"fmp: 404 — recurso desconhecido ({path})")
        resp.raise_for_status()
        data = resp.json()
        _log("fmp", {"path": path, "ok": True, "rows": len(data) if isinstance(data, list) else 1})
        return data

    @staticmethod
    def _first(payload: Any) -> dict[str, Any]:
        if isinstance(payload, list) and payload:
            return payload[0] or {}
        if isinstance(payload, dict):
            return payload
        return {}

    def get_fundamentals(self, ticker: str, years: int = 5) -> dict[str, Any]:
        """TTM ratios + market cap. Output shape compatível com `_adapter_yfinance_us_fundamentals`."""
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        ticker = ticker.upper()
        ratios = self._first(self._get("/stable/ratios-ttm", {"symbol": ticker}))
        km = self._first(self._get("/stable/key-metrics-ttm", {"symbol": ticker}))
        if not ratios and not km:
            raise RuntimeError(f"fmp: empty payload for {ticker}")
        return {
            "ticker": ticker,
            "pe": ratios.get("priceToEarningsRatioTTM"),
            "pb": ratios.get("priceToBookRatioTTM"),
            "dy": ratios.get("dividendYieldTTM"),
            "roe": km.get("returnOnEquityTTM"),
            "eps": ratios.get("netIncomePerShareTTM"),
            "bvps": ratios.get("bookValuePerShareTTM"),
            "market_cap": km.get("marketCap"),
            "ev_ebitda": km.get("evToEBITDATTM"),
            "fcf_ttm": km.get("freeCashFlowToFirmTTM"),
            "source": "fmp",
        }

    def get_analyst_consensus(self, ticker: str) -> dict[str, Any]:
        """Price targets + forward estimates (escolhe o ano fiscal mais próximo no futuro)."""
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        ticker = ticker.upper()
        target = self._first(self._get("/stable/price-target-consensus", {"symbol": ticker}))
        est_list = self._get(
            "/stable/analyst-estimates",
            {"symbol": ticker, "period": "annual", "limit": 10},
        )
        est = self._pick_nearest_forward(est_list)
        if not target and not est:
            raise RuntimeError(f"fmp: no analyst data for {ticker}")
        return {
            "ticker": ticker,
            "target_high": target.get("targetHigh"),
            "target_low": target.get("targetLow"),
            "target_median": target.get("targetMedian"),
            "target_consensus": target.get("targetConsensus"),
            "estimate_eps_avg": est.get("epsAvg"),
            "estimate_eps_high": est.get("epsHigh"),
            "estimate_eps_low": est.get("epsLow"),
            "estimate_revenue_avg": est.get("revenueAvg"),
            "estimate_net_income_avg": est.get("netIncomeAvg"),
            "estimate_num_analysts": est.get("numAnalystsEps"),
            "estimate_date": est.get("date"),
            "source": "fmp",
        }

    @staticmethod
    def _pick_nearest_forward(rows: Any) -> dict[str, Any]:
        """Dada lista de estimates anuais com `date` ISO, devolve a mais próxima ≥ hoje.
        Fallback à mais recente se todas forem passadas (raro).
        """
        if not isinstance(rows, list) or not rows:
            return {}
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        forward = [r for r in rows if r.get("date") and r["date"] >= today]
        if forward:
            return min(forward, key=lambda r: r["date"])
        return max(rows, key=lambda r: r.get("date") or "")

    def get_price(self, ticker: str, date: str | None = None) -> dict[str, Any]:
        if not self.is_available():
            raise NotImplementedError("FMP_API_KEY not configured")
        raise NotImplementedError("FMPClient.get_price não implementado (yfinance + Massive cobrem prices)")


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
