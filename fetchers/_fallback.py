"""Cascade fallback wrapper for data fetchers.

Two entrypoints:

  fetch_with_fallback(...) -> dict
      Backward-compat. Tries sources in priority order. Returns first success.
      Raises DataFetchError on all-fail. No cache fallback.

  fetch_with_quality(...) -> FetchResult
      Modern. Same cascade PLUS cache layer (TTL-based) as final fallback.
      Always returns a FetchResult. Caller branches on .quality:
        OK        — primary source, fresh.
        WARNING   — secondary source used (data fresh but provenance weaker).
        DEGRADED  — cache used (data stale).
        CRITICAL  — every layer failed including cache (.success=False).
        VALIDATION_FAIL — value rejected by guards (treated as fail; tries next).

Configuração: config/sources_priority.yaml.
Cache TTL: config/sources_priority.yaml::cache.ttl_hours (override defaults).
Logs: logs/fetchers_fallback.log — JSON per attempt.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import yaml

from fetchers import _cache
from fetchers._errors import (
    CriticalError,
    DataError,
    DegradedError,
    RateLimitError,
    ValidationError,
    WarningError,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources_priority.yaml"
LOG_PATH = ROOT / "logs" / "fetchers_fallback.log"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


# ============================================================
# FetchResult — quality-aware return type
# ============================================================
@dataclass
class FetchResult:
    """Result of a fetch attempt with quality flag.

    Always inspectable; never raises (use .success). Callers read .quality
    to decide whether to halt, warn, or proceed silently.

    .value is the adapter's normalized dict on success (.success=True).
    On full failure (.success=False) value is None and .errors lists the
    cascade attempts ([(source, error_message), ...]).
    """
    success: bool
    value: Any
    market: str
    kind: str
    ticker: str
    source: str          # 'yfinance', 'massive', 'cache:yfinance', 'none'
    quality: str         # 'OK', 'WARNING', 'DEGRADED', 'CRITICAL'
    age_hours: float = 0.0
    message: str = ""
    errors: list[tuple[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def raise_if_critical(self) -> None:
        """Convenience for STRICT-mode callers."""
        if self.quality == "CRITICAL":
            raise CriticalError(self.message or f"Critical fetch fail for {self.ticker}")

    def raise_if_below(self, min_quality: str = "OK") -> None:
        """ULTRA-STRICT mode. Order: OK > WARNING > DEGRADED > CRITICAL."""
        order = ["CRITICAL", "DEGRADED", "WARNING", "OK"]
        if order.index(self.quality) < order.index(min_quality):
            mapping = {
                "OK": ValidationError,  # never raised but for completeness
                "WARNING": WarningError,
                "DEGRADED": DegradedError,
                "CRITICAL": CriticalError,
            }
            cls = mapping.get(self.quality, DataError)
            raise cls(f"{self.quality} quality below required {min_quality} for {self.ticker}: {self.message}")


# ============================================================
# Backward-compat error
# ============================================================
class DataFetchError(RuntimeError):
    """Raised by fetch_with_fallback when ALL sources fail.
    fetch_with_quality returns FetchResult(success=False) instead."""

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


# ============================================================
# Helpers
# ============================================================
def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False, default=str)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _record_provenance(result: "FetchResult") -> None:
    """Phase FF Bloco 3.1 — append a provenance row per successful FetchResult.

    Best-effort: DB write failures are logged but never break the fetch caller.
    Skips CRITICAL (no value to attest). Hash is sha1 over canonical JSON of
    the value so duplicate fetches collapse on the hash without comparing dicts.
    """
    if not result.success or result.value is None:
        return
    db_path = DB_BR if result.market == "br" else DB_US if result.market == "us" else None
    if db_path is None:
        return
    try:
        payload = json.dumps(result.value, sort_keys=True, default=str, ensure_ascii=False)
        value_hash = hashlib.sha1(payload.encode("utf-8")).hexdigest()
    except Exception:
        value_hash = None
    try:
        with sqlite3.connect(db_path, timeout=5.0) as conn:
            conn.execute(
                "INSERT INTO provenance "
                "(fetched_at, market, kind, ticker, source, quality, age_hours, value_hash, message) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (_now_iso(), result.market, result.kind, result.ticker,
                 result.source, result.quality, result.age_hours,
                 value_hash, (result.message or "")[:500]),
            )
            conn.commit()
    except sqlite3.OperationalError as e:
        _log({"market": result.market, "kind": result.kind, "ticker": result.ticker,
              "status": "provenance_write_fail", "error": str(e)[:200]})
    except Exception as e:  # noqa: BLE001
        _log({"market": result.market, "kind": result.kind, "ticker": result.ticker,
              "status": "provenance_write_fail", "error": str(e)[:200]})


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing {CONFIG_PATH}. Run from repo root.")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def get_priority(market: str, kind: str) -> list[str]:
    cfg = load_config()
    return list((cfg.get(market, {}) or {}).get(kind, []) or [])


def get_guards() -> dict:
    return load_config().get("guards", {}) or {}


# ============================================================
# Adapter REGISTRY — slug → callable(ticker, **kw) -> dict|Any
# ============================================================
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


def _adapter_yfinance_us_fundamentals(ticker: str, **kw) -> dict[str, Any]:
    import yfinance as yf
    tk = yf.Ticker(ticker)
    info = tk.info or {}
    if not info.get("symbol") and not info.get("shortName"):
        raise RuntimeError(f"yfinance .info empty for {ticker}")
    return {
        "ticker": ticker,
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "dy": info.get("dividendYield"),
        "roe": info.get("returnOnEquity"),
        "eps": info.get("trailingEps"),
        "bvps": info.get("bookValue"),
        "market_cap": info.get("marketCap"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "fcf_ttm": info.get("freeCashflow"),
        "source": "yfinance",
    }


def _adapter_yf_deep_us_fundamentals(ticker: str, **kw) -> dict[str, Any]:
    """Falls back to DataFrames financials/balance_sheet/cashflow when info dict is sparse."""
    import yfinance as yf
    tk = yf.Ticker(ticker)
    fin = getattr(tk, "financials", None)
    bs = getattr(tk, "balance_sheet", None)
    if fin is None or fin.empty:
        raise RuntimeError(f"yf_deep: financials empty for {ticker}")

    def _pick(df, keys):
        if df is None or df.empty:
            return None
        col = df.columns[0]
        for k in keys:
            if k in df.index:
                v = df.loc[k, col]
                try:
                    return float(v) if v == v else None
                except (TypeError, ValueError):
                    return None
        return None

    revenue = _pick(fin, ["Total Revenue", "Revenue"])
    net_income = _pick(fin, ["Net Income"])
    total_debt = _pick(bs, ["Total Debt", "Long Term Debt"])
    equity = _pick(bs, ["Stockholders Equity", "Total Stockholder Equity"])
    return {
        "ticker": ticker,
        "revenue": revenue,
        "net_income": net_income,
        "total_debt": total_debt,
        "equity": equity,
        "roe": (net_income / equity) if (net_income is not None and equity and equity > 0) else None,
        "source": "yf_deep",
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
    ts = r.get("t")
    date_str = (
        datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d")
        if ts else None
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


def _adapter_yfinance_br_fundamentals(ticker: str, **kw) -> dict[str, Any]:
    import yfinance as yf
    yf_ticker = ticker if ticker.endswith(".SA") else f"{ticker}.SA"
    tk = yf.Ticker(yf_ticker)
    info = tk.info or {}
    if not info.get("symbol") and not info.get("shortName"):
        raise RuntimeError(f"yfinance .info empty for {yf_ticker}")
    return {
        "ticker": ticker,
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "dy": info.get("dividendYield"),
        "roe": info.get("returnOnEquity"),
        "eps": info.get("trailingEps"),
        "bvps": info.get("bookValue"),
        "market_cap": info.get("marketCap"),
        "source": "yfinance",
    }


def _adapter_bcb_macro(series_name: str, **kw) -> dict[str, Any]:
    """series_name: 'SELIC_DAILY' | 'CDI_DAILY' | 'IPCA_MONTHLY' | 'USDBRL_PTAX' | 'SELIC_META'."""
    from datetime import datetime, timedelta
    from fetchers.bcb_fetcher import SGS_MAP, _parse_br_date, fetch_sgs
    info = SGS_MAP.get(series_name.upper())
    if not info:
        raise RuntimeError(f"bcb: unknown series {series_name} (try {list(SGS_MAP.keys())})")
    code, scale, _inception = info
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=14)  # 14d window catches latest published value
    rows = fetch_sgs(code, start_dt.strftime("%d/%m/%Y"), end_dt.strftime("%d/%m/%Y"))
    if not rows:
        raise RuntimeError(f"bcb: empty response for {series_name}")
    last = rows[-1]
    try:
        return {
            "series": series_name.upper(),
            "date": _parse_br_date(last["data"]),
            "value": float(last["valor"]) * scale,
            "source": "bcb_sgs",
        }
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"bcb: malformed row {last}: {e}") from e


def _adapter_fred_macro(series_name: str, **kw) -> dict[str, Any]:
    """FRED series: DFF, DGS10, DGS2, CPIAUCSL, UNRATE, FEDFUNDS, etc."""
    from fetchers.fred_fetcher import _fetch_csv
    rows = _fetch_csv(series_name.upper())
    if not rows:
        raise RuntimeError(f"fred: empty for {series_name}")
    date_str, value = rows[-1]
    return {
        "series": series_name.upper(),
        "date": date_str,
        "value": float(value) if value is not None else None,
        "source": "fred",
    }


def _adapter_fmp_us_fundamentals(ticker: str, **kw) -> dict[str, Any]:
    from fetchers._clients import fmp
    return fmp().get_fundamentals(ticker, years=kw.get("years", 5))


def _adapter_fmp_us_analyst(ticker: str, **kw) -> dict[str, Any]:
    from fetchers._clients import fmp
    return fmp().get_analyst_consensus(ticker)


def _adapter_eodhd_us_price(ticker: str, **kw) -> dict[str, Any]:
    from fetchers._clients import eodhd
    return eodhd().get_price(ticker, date=kw.get("date"))


def _adapter_benzinga_us_analyst(ticker: str, **kw) -> dict[str, Any]:
    from fetchers._clients import benzinga
    return benzinga().get_analyst_consensus(ticker)


REGISTRY: dict[tuple[str, str, str], Callable[..., Any]] = {
    # US prices
    ("us", "prices", "yfinance"): _adapter_yfinance_us_price,
    ("us", "prices", "massive"): _adapter_massive_us_price,
    ("us", "prices", "eodhd"): _adapter_eodhd_us_price,
    # US fundamentals
    ("us", "fundamentals", "yfinance"): _adapter_yfinance_us_fundamentals,
    ("us", "fundamentals", "yf_deep"): _adapter_yf_deep_us_fundamentals,
    ("us", "fundamentals", "fmp"): _adapter_fmp_us_fundamentals,
    # US analyst
    ("us", "analyst", "fmp"): _adapter_fmp_us_analyst,
    ("us", "analyst", "benzinga"): _adapter_benzinga_us_analyst,
    # US macro
    ("us", "macro", "fred"): _adapter_fred_macro,
    # BR prices
    ("br", "prices", "yfinance"): _adapter_yfinance_br_price,
    # BR fundamentals
    ("br", "fundamentals", "yfinance"): _adapter_yfinance_br_fundamentals,
    # BR macro
    ("br", "macro", "bcb_sgs"): _adapter_bcb_macro,
}


def register(market: str, kind: str, source: str, fn: Callable[..., Any]) -> None:
    """Permite adicionar adapter à mão (testes, plugins futuros)."""
    REGISTRY[(market, kind, source)] = fn


# ============================================================
# Public API
# ============================================================
def fetch_with_fallback(
    market: str, kind: str, ticker: str,
    *, sources: list[str] | None = None, **kwargs,
) -> dict[str, Any]:
    """Try sources in priority order. Return dict on first success.
    Raises DataFetchError on full failure. (Backward-compat; no cache fallback.)"""
    src_list = sources if sources is not None else get_priority(market, kind)
    if not src_list:
        raise DataFetchError(market, kind, ticker,
                             [("config", f"no sources for {market}/{kind}")])
    errors: list[tuple[str, str]] = []
    for src in src_list:
        adapter = REGISTRY.get((market, kind, src))
        if adapter is None:
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "skipped", "reason": "no adapter"})
            errors.append((src, "no adapter"))
            continue
        t0 = time.time()
        try:
            result = adapter(ticker, **kwargs)
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "ok",
                  "latency_ms": int((time.time() - t0) * 1000)})
            return result
        except Exception as e:  # noqa: BLE001
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "fail",
                  "error": str(e)[:300],
                  "latency_ms": int((time.time() - t0) * 1000)})
            errors.append((src, str(e)[:120]))
    raise DataFetchError(market, kind, ticker, errors)


def fetch_with_quality(
    market: str, kind: str, ticker: str,
    *, sources: list[str] | None = None,
    use_cache: bool = True,
    write_cache: bool = True,
    **kwargs,
) -> FetchResult:
    """Cascade with cache fallback. Always returns FetchResult; never raises.

    Quality logic:
      - First source successful → quality='OK', source=primary slug.
      - Second/Nth source successful → quality='WARNING', source=that slug.
      - All sources failed, fresh cache hit → quality='DEGRADED', source='cache:<slug>'.
      - All sources failed, stale cache hit → quality='DEGRADED' (age_hours>=ttl).
      - Everything failed → quality='CRITICAL', success=False.
    """
    src_list = sources if sources is not None else get_priority(market, kind)
    if not src_list:
        return FetchResult(
            success=False, value=None, market=market, kind=kind, ticker=ticker,
            source="none", quality="CRITICAL",
            message=f"No sources configured for {market}/{kind}",
            errors=[("config", "no sources")],
        )

    errors: list[tuple[str, str]] = []
    for idx, src in enumerate(src_list):
        adapter = REGISTRY.get((market, kind, src))
        if adapter is None:
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "skipped", "reason": "no adapter"})
            errors.append((src, "no adapter"))
            continue
        t0 = time.time()
        try:
            value = adapter(ticker, **kwargs)
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "ok",
                  "latency_ms": int((time.time() - t0) * 1000)})
            if write_cache:
                try:
                    _cache.put(market, kind, ticker, src, value)
                except Exception as e:  # noqa: BLE001
                    _log({"market": market, "kind": kind, "ticker": ticker,
                          "source": src, "status": "cache_write_fail",
                          "error": str(e)[:200]})
            quality = "OK" if idx == 0 else "WARNING"
            result = FetchResult(
                success=True, value=value,
                market=market, kind=kind, ticker=ticker,
                source=src, quality=quality, age_hours=0.0,
                message="" if quality == "OK" else f"Primary {src_list[0]} failed; using {src}",
                errors=errors,
            )
            _record_provenance(result)
            return result
        except Exception as e:  # noqa: BLE001
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": src, "status": "fail",
                  "error": str(e)[:300],
                  "latency_ms": int((time.time() - t0) * 1000)})
            errors.append((src, str(e)[:120]))

    # All live sources failed — try cache
    if use_cache:
        fresh = _cache.get_fresh(market, kind, ticker)
        if fresh:
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": f"cache:{fresh['source']}", "status": "cache_fresh",
                  "age_hours": round(fresh["age_hours"], 2)})
            result = FetchResult(
                success=True, value=fresh["value"],
                market=market, kind=kind, ticker=ticker,
                source=f"cache:{fresh['source']}", quality="DEGRADED",
                age_hours=fresh["age_hours"],
                message=f"All live sources failed; cache fresh ({fresh['age_hours']:.1f}h old)",
                errors=errors,
            )
            _record_provenance(result)
            return result
        stale = _cache.get_stale(market, kind, ticker)
        if stale:
            _log({"market": market, "kind": kind, "ticker": ticker,
                  "source": f"cache:{stale['source']}", "status": "cache_stale",
                  "age_hours": round(stale["age_hours"], 2)})
            result = FetchResult(
                success=True, value=stale["value"],
                market=market, kind=kind, ticker=ticker,
                source=f"cache:{stale['source']}", quality="DEGRADED",
                age_hours=stale["age_hours"],
                message=f"All live sources failed; stale cache ({stale['age_hours']:.1f}h old)",
                errors=errors,
            )
            _record_provenance(result)
            return result

    # Truly nothing worked
    return FetchResult(
        success=False, value=None,
        market=market, kind=kind, ticker=ticker,
        source="none", quality="CRITICAL",
        message=f"No data for {ticker}: every source + cache exhausted",
        errors=errors,
    )


# ============================================================
# Smoke test
# ============================================================
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Fallback wrapper smoke test")
    ap.add_argument("market", choices=["br", "us"])
    ap.add_argument("kind", choices=["prices", "fundamentals", "dividends", "macro", "analyst", "filings"])
    ap.add_argument("ticker")
    ap.add_argument("--sources", help="comma-separated override")
    ap.add_argument("--quality", action="store_true", help="use fetch_with_quality (FetchResult)")
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    overrides = args.sources.split(",") if args.sources else None
    if args.quality:
        result = fetch_with_quality(
            args.market, args.kind, args.ticker,
            sources=overrides, use_cache=not args.no_cache,
        )
        print(json.dumps(result.as_dict(), indent=2, default=str))
        raise SystemExit(0 if result.success else 1)
    try:
        out = fetch_with_fallback(args.market, args.kind, args.ticker, sources=overrides)
        print(json.dumps(out, indent=2, default=str))
    except DataFetchError as e:
        print(f"FAILED: {e}")
        raise SystemExit(1)
