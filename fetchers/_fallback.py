"""Cascade fallback wrapper for data fetchers.

Lê config/sources_priority.yaml e orquestra a tentativa em ordem.
Não substitui os fetchers — coordena-os.

Uso típico (caller):

    from fetchers._fallback import fetch_with_fallback

    # Preço US — tenta yfinance, se falhar tenta massive
    price = fetch_with_fallback("us", "prices", "AAPL")

    # Macro BR — só BCB (single source, mas ainda passa pelo wrapper para
    # uniformizar logs)
    selic = fetch_with_fallback("br", "macro", "SELIC")

Cada fetcher registado em REGISTRY recebe (ticker_or_series, **kwargs) e
devolve um dict normalizado OU lança qualquer Exception. Wrapper apanha
e tenta a próxima fonte.

Logs: 1 linha JSON por tentativa em logs/fetchers_fallback.log com
{ts, market, kind, ticker, source, status: ok|fail|skipped, error?, latency_ms}.
Útil para auditoria post-mortem (quais fontes falharam mais nesta semana?).
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources_priority.yaml"
LOG_PATH = ROOT / "logs" / "fetchers_fallback.log"


class DataFetchError(RuntimeError):
    """Raised when ALL sources for (market, kind) failed."""

    def __init__(self, market: str, kind: str, ticker: str, errors: list[tuple[str, str]]):
        self.market = market
        self.kind = kind
        self.ticker = ticker
        self.errors = errors
        msg = (
            f"All sources exhausted for {market}/{kind}/{ticker}: "
            + "; ".join(f"{src}={err}" for src, err in errors)
        )
        super().__init__(msg)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False, default=str)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing {CONFIG_PATH}. Run from repo root.")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def get_priority(market: str, kind: str) -> list[str]:
    """Return ordered list of source slugs for (market, kind), or empty if unconfigured."""
    cfg = load_config()
    return list((cfg.get(market, {}) or {}).get(kind, []) or [])


def get_guards() -> dict:
    """Return the `guards` section verbatim. Callers apply thresholds locally."""
    return load_config().get("guards", {}) or {}


# ============================================================
# Fetcher REGISTRY — slug → callable(ticker, **kw) -> dict|Any
# ============================================================
# Each entry is registered lazily to avoid import cycles. Adapter functions
# normalize the heterogeneous fetcher APIs to one signature: (ticker, **kw).

def _adapter_yfinance_us_price(ticker: str, **kw) -> dict[str, Any]:
    import yfinance as yf

    period = kw.get("period", "1d")
    tk = yf.Ticker(ticker)
    hist = tk.history(period=period, auto_adjust=False)
    if hist is None or len(hist) == 0:
        raise RuntimeError(f"yfinance returned empty history for {ticker}")
    last = hist.iloc[-1]
    return {
        "ticker": ticker,
        "date": hist.index[-1].strftime("%Y-%m-%d"),
        "close": float(last["Close"]),
        "volume": int(last["Volume"]) if last["Volume"] == last["Volume"] else None,
        "source": "yfinance",
    }


def _adapter_massive_us_price(ticker: str, **kw) -> dict[str, Any]:
    from fetchers.massive_fetcher import MassiveError, get_previous_close

    try:
        data = get_previous_close(ticker)
    except MassiveError as e:
        raise RuntimeError(f"massive: {e}") from e
    results = data.get("results") or []
    if not results:
        raise RuntimeError(f"massive: empty results for {ticker}")
    r = results[0]
    # massive returns timestamp `t` in millis
    ts = r.get("t")
    date_str = (
        datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d")
        if ts
        else None
    )
    return {
        "ticker": ticker,
        "date": date_str,
        "close": float(r.get("c")) if r.get("c") is not None else None,
        "volume": int(r.get("v")) if r.get("v") is not None else None,
        "source": "massive",
    }


def _adapter_yfinance_br_price(ticker: str, **kw) -> dict[str, Any]:
    import yfinance as yf

    yf_ticker = ticker if ticker.endswith(".SA") else f"{ticker}.SA"
    period = kw.get("period", "1d")
    tk = yf.Ticker(yf_ticker)
    hist = tk.history(period=period, auto_adjust=False)
    if hist is None or len(hist) == 0:
        raise RuntimeError(f"yfinance returned empty history for {yf_ticker}")
    last = hist.iloc[-1]
    return {
        "ticker": ticker,
        "date": hist.index[-1].strftime("%Y-%m-%d"),
        "close": float(last["Close"]),
        "volume": int(last["Volume"]) if last["Volume"] == last["Volume"] else None,
        "source": "yfinance",
    }


REGISTRY: dict[tuple[str, str, str], Callable[..., Any]] = {
    ("us", "prices", "yfinance"): _adapter_yfinance_us_price,
    ("us", "prices", "massive"): _adapter_massive_us_price,
    ("br", "prices", "yfinance"): _adapter_yfinance_br_price,
    # Fundamentals/dividendos/macro: adicionar adapters quando o caller precisar.
    # Não pré-registar tudo para evitar import cycles e chamar dependências
    # opcionais sem necessidade.
}


def register(market: str, kind: str, source: str, fn: Callable[..., Any]) -> None:
    """Permite adicionar adapter à mão sem editar este ficheiro (ex: testes)."""
    REGISTRY[(market, kind, source)] = fn


def fetch_with_fallback(
    market: str,
    kind: str,
    ticker: str,
    *,
    sources: list[str] | None = None,
    **kwargs,
) -> dict[str, Any]:
    """Try sources in priority order. Return dict of first success.

    Args:
        market: 'br' or 'us'
        kind: 'prices', 'fundamentals', 'dividends', 'macro', 'filings'
        ticker: e.g. 'AAPL', 'PETR4', 'SELIC' (for macro series)
        sources: override priority list (rare; mostly for tests)
        **kwargs: passed to each adapter (e.g. period='5y')

    Raises DataFetchError if every source fails.
    """
    src_list = sources if sources is not None else get_priority(market, kind)
    if not src_list:
        raise DataFetchError(
            market, kind, ticker,
            [("config", f"no sources configured for {market}/{kind}")],
        )

    errors: list[tuple[str, str]] = []
    for src in src_list:
        adapter = REGISTRY.get((market, kind, src))
        if adapter is None:
            _log({
                "market": market, "kind": kind, "ticker": ticker,
                "source": src, "status": "skipped",
                "reason": "no adapter registered",
            })
            errors.append((src, "no adapter"))
            continue

        t0 = time.time()
        try:
            result = adapter(ticker, **kwargs)
            _log({
                "market": market, "kind": kind, "ticker": ticker,
                "source": src, "status": "ok",
                "latency_ms": int((time.time() - t0) * 1000),
            })
            return result
        except Exception as e:  # noqa: BLE001 — caught + logged + retry next
            _log({
                "market": market, "kind": kind, "ticker": ticker,
                "source": src, "status": "fail",
                "error": str(e)[:300],
                "latency_ms": int((time.time() - t0) * 1000),
            })
            errors.append((src, str(e)[:120]))

    raise DataFetchError(market, kind, ticker, errors)


# ============================================================
# Standalone smoke test
# ============================================================
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Fallback wrapper smoke test")
    ap.add_argument("market", choices=["br", "us"])
    ap.add_argument("kind", choices=["prices", "fundamentals", "dividends", "macro"])
    ap.add_argument("ticker")
    ap.add_argument("--sources", help="comma-separated override")
    args = ap.parse_args()

    overrides = args.sources.split(",") if args.sources else None
    try:
        out = fetch_with_fallback(args.market, args.kind, args.ticker, sources=overrides)
        print(json.dumps(out, indent=2, default=str))
    except DataFetchError as e:
        print(f"FAILED: {e}")
        raise SystemExit(1)
