"""Massive.com (ex-Polygon.io) thin REST client.

Massive.com adquiriu/rebrandou a Polygon.io em 2025; o domínio legado
`api.polygon.io` continua a responder mas a base canónica é agora
`api.massive.com`. SDK Go: github.com/massive-com/client-go.

No nosso pipeline serve como fonte alternativa/fallback ao yfinance para US:
  - intraday real-time (yfinance tem 15min delay)
  - options chains (yfinance não cobre)
  - forex / futures (yfinance limitado)
  - aggregates com controlo adjusted/unadjusted (yfinance só ajustado)

Free tier histórico do Polygon: ~5 req/min, end-of-day apenas. Adicionei
rate-limiter conservador. Tier real do user é desconhecido — o smoke-test
abaixo deteta 401/429 e reporta.

Uso:
    python fetchers/massive_fetcher.py AAPL                     # smoke test
    python fetchers/massive_fetcher.py AAPL --previous-close
    python fetchers/massive_fetcher.py AAPL --aggregates --from 2026-04-01 --to 2026-04-25
"""
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"

BASE_URL = "https://api.massive.com"
DEFAULT_TIMEOUT = 15
MIN_INTERVAL_SEC = 13.0  # ~5 req/min ceiling (free tier safety)


def _load_api_key() -> str | None:
    """MASSIVE_API_KEY do env ou .env. Mirror do pattern em autoresearch.py."""
    key = os.environ.get("MASSIVE_API_KEY")
    if key:
        return key.strip()
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("MASSIVE_API_KEY") and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


@dataclass
class _Throttle:
    last_call: float = 0.0

    def wait(self) -> None:
        delta = time.time() - self.last_call
        if delta < MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC - delta)
        self.last_call = time.time()


_throttle = _Throttle()


class MassiveError(RuntimeError):
    pass


def _get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    api_key = _load_api_key()
    if not api_key:
        raise MassiveError("MASSIVE_API_KEY ausente em env e .env")
    _throttle.wait()
    full_params = dict(params or {})
    full_params["apiKey"] = api_key
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=full_params, timeout=DEFAULT_TIMEOUT)
    if resp.status_code == 401:
        raise MassiveError(f"401 Unauthorized — chave inválida ou expirada ({path})")
    if resp.status_code == 403:
        raise MassiveError(f"403 Forbidden — endpoint fora do tier actual ({path})")
    if resp.status_code == 429:
        raise MassiveError(f"429 Rate limited — abrandar ou upgrade tier ({path})")
    resp.raise_for_status()
    return resp.json()


def get_previous_close(ticker: str, adjusted: bool = True) -> dict[str, Any]:
    """Last completed trading day OHLCV. Endpoint mais barato — bom para health check."""
    return _get(
        f"/v2/aggs/ticker/{ticker.upper()}/prev",
        {"adjusted": "true" if adjusted else "false"},
    )


def get_aggregates(
    ticker: str,
    from_date: str,
    to_date: str,
    timespan: str = "day",
    multiplier: int = 1,
    adjusted: bool = True,
) -> dict[str, Any]:
    """Bars OHLCV. timespan: minute|hour|day|week|month|quarter|year."""
    return _get(
        f"/v2/aggs/ticker/{ticker.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}",
        {"adjusted": "true" if adjusted else "false", "sort": "asc"},
    )


def get_snapshot(ticker: str) -> dict[str, Any]:
    """Real-time snapshot (todays trade, day OHLCV, prev close, ...). Tier-gated."""
    return _get(f"/v2/snapshot/locale/us/markets/stocks/tickers/{ticker.upper()}")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    from datetime import UTC, datetime
    line = json.dumps(
        {"ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), **event},
        ensure_ascii=False,
        default=str,
    )
    with (LOG_DIR / "massive_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def main() -> int:
    ap = argparse.ArgumentParser(description="Massive.com (ex-Polygon) smoke test")
    ap.add_argument("ticker")
    ap.add_argument("--previous-close", action="store_true", help="prev day OHLCV (default)")
    ap.add_argument("--aggregates", action="store_true", help="bars range")
    ap.add_argument("--snapshot", action="store_true", help="real-time snapshot (tier-gated)")
    ap.add_argument("--from", dest="from_date", help="YYYY-MM-DD (aggregates)")
    ap.add_argument("--to", dest="to_date", help="YYYY-MM-DD (aggregates)")
    ap.add_argument("--timespan", default="day", choices=["minute", "hour", "day", "week", "month"])
    args = ap.parse_args()

    if not (args.previous_close or args.aggregates or args.snapshot):
        args.previous_close = True

    try:
        if args.aggregates:
            if not (args.from_date and args.to_date):
                ap.error("--aggregates requer --from YYYY-MM-DD --to YYYY-MM-DD")
            data = get_aggregates(args.ticker, args.from_date, args.to_date, timespan=args.timespan)
            _log({"endpoint": "aggregates", "ticker": args.ticker, "results": len(data.get("results") or [])})
        elif args.snapshot:
            data = get_snapshot(args.ticker)
            _log({"endpoint": "snapshot", "ticker": args.ticker, "ok": data.get("status") == "OK"})
        else:
            data = get_previous_close(args.ticker)
            results = data.get("results") or []
            _log({
                "endpoint": "previous_close",
                "ticker": args.ticker,
                "close": results[0].get("c") if results else None,
                "volume": results[0].get("v") if results else None,
            })
        print(json.dumps(data, indent=2, default=str)[:2000])
        return 0
    except MassiveError as e:
        _log({"error": str(e), "ticker": args.ticker})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
