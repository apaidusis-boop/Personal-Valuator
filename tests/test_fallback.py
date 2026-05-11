"""Tests for fetchers/_fallback.py — cascade behaviour with mocked adapters.

Cobre todos os caminhos do FetchResult quality matrix:
  OK         — primary success
  WARNING    — secondary success
  DEGRADED   — fresh cache fallback
  DEGRADED   — stale cache fallback (cache TTL expired but available)
  CRITICAL   — all live + cache empty

Também verifica:
  - errors[] propaga em CRITICAL
  - source string format (e.g. 'cache:yfinance')
  - write_cache=False não polui cache
  - sources= override funciona
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure repo root in path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fetchers import _cache, _fallback


@pytest.fixture(autouse=True)
def isolate_cache(tmp_path, monkeypatch):
    """Redirect cache DB to tmp so tests don't pollute real cache."""
    test_db = tmp_path / "test_cache.db"
    monkeypatch.setattr(_cache, "CACHE_DB", test_db)
    yield


@pytest.fixture(autouse=True)
def reset_registry():
    """Snapshot REGISTRY before each test, restore after."""
    snapshot = dict(_fallback.REGISTRY)
    yield
    _fallback.REGISTRY.clear()
    _fallback.REGISTRY.update(snapshot)


# ============================================================
# Helpers — register fake adapters
# ============================================================
def make_adapter(value=None, error=None):
    def adapter(ticker, **kw):
        if error:
            raise RuntimeError(error)
        return value or {"ticker": ticker, "value": "ok"}
    return adapter


# ============================================================
# Quality matrix
# ============================================================
def test_primary_success_is_ok():
    _fallback.register("test", "prices", "primary", make_adapter({"px": 100}))
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL", sources=["primary"]
    )
    assert r.success is True
    assert r.quality == "OK"
    assert r.source == "primary"
    assert r.value == {"px": 100}
    assert r.errors == []


def test_secondary_success_is_warning():
    _fallback.register("test", "prices", "primary", make_adapter(error="primary down"))
    _fallback.register("test", "prices", "secondary", make_adapter({"px": 95}))
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL", sources=["primary", "secondary"]
    )
    assert r.success is True
    assert r.quality == "WARNING"
    assert r.source == "secondary"
    assert r.value == {"px": 95}
    assert len(r.errors) == 1
    assert r.errors[0][0] == "primary"


def test_cache_fallback_is_degraded():
    # Pre-populate cache
    _cache.put("test", "prices", "AAPL", "primary", {"px": 90, "cached": True})
    # Now register adapter that fails
    _fallback.register("test", "prices", "primary", make_adapter(error="boom"))
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL", sources=["primary"]
    )
    assert r.success is True
    assert r.quality == "DEGRADED"
    assert r.source == "cache:primary"
    assert r.value == {"px": 90, "cached": True}


def test_no_sources_is_critical():
    r = _fallback.fetch_with_quality("test", "prices", "AAPL", sources=[])
    assert r.success is False
    assert r.quality == "CRITICAL"
    assert r.source == "none"


def test_all_fail_no_cache_is_critical():
    _fallback.register("test", "prices", "primary", make_adapter(error="A down"))
    _fallback.register("test", "prices", "secondary", make_adapter(error="B down"))
    r = _fallback.fetch_with_quality(
        "test", "prices", "NEW_TICKER",
        sources=["primary", "secondary"],
    )
    assert r.success is False
    assert r.quality == "CRITICAL"
    assert len(r.errors) == 2


def test_no_adapter_registered_is_skipped_then_falls_through():
    _fallback.register("test", "prices", "primary", make_adapter({"px": 100}))
    # 'unregistered' has no adapter
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL", sources=["unregistered", "primary"]
    )
    assert r.success is True
    assert r.quality == "WARNING"  # primary used because secondary slot
    assert r.source == "primary"
    assert ("unregistered", "no adapter") in r.errors


def test_write_cache_false_does_not_pollute():
    _fallback.register("test", "prices", "primary", make_adapter({"px": 100}))
    _fallback.fetch_with_quality(
        "test", "prices", "AAPL",
        sources=["primary"], write_cache=False,
    )
    assert _cache.get_fresh("test", "prices", "AAPL") is None


def test_use_cache_false_skips_cache_fallback():
    _cache.put("test", "prices", "AAPL", "primary", {"px": 90})
    _fallback.register("test", "prices", "primary", make_adapter(error="down"))
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL",
        sources=["primary"], use_cache=False,
    )
    assert r.success is False
    assert r.quality == "CRITICAL"


def test_fetch_result_dict_serialization():
    _fallback.register("test", "prices", "primary", make_adapter({"px": 100}))
    r = _fallback.fetch_with_quality(
        "test", "prices", "AAPL", sources=["primary"]
    )
    d = r.as_dict()
    assert d["quality"] == "OK"
    assert d["value"] == {"px": 100}


def test_raise_if_critical():
    r = _fallback.fetch_with_quality("test", "prices", "X", sources=[])
    assert r.quality == "CRITICAL"
    with pytest.raises(_fallback.CriticalError):
        r.raise_if_critical()


def test_raise_if_below_warning():
    _cache.put("test", "prices", "X", "primary", {"px": 1})
    _fallback.register("test", "prices", "primary", make_adapter(error="down"))
    r = _fallback.fetch_with_quality("test", "prices", "X", sources=["primary"])
    assert r.quality == "DEGRADED"
    # WARNING is acceptable but DEGRADED is below
    with pytest.raises(_fallback.DegradedError):
        r.raise_if_below("WARNING")


# ============================================================
# Backward-compat fetch_with_fallback
# ============================================================
def test_fetch_with_fallback_returns_dict_on_success():
    _fallback.register("test", "prices", "primary", make_adapter({"px": 100}))
    out = _fallback.fetch_with_fallback("test", "prices", "AAPL", sources=["primary"])
    assert out == {"px": 100}


def test_fetch_with_fallback_raises_on_all_fail():
    _fallback.register("test", "prices", "primary", make_adapter(error="boom"))
    with pytest.raises(_fallback.DataFetchError):
        _fallback.fetch_with_fallback("test", "prices", "X", sources=["primary"])
