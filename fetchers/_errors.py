"""Typed exception hierarchy for the data layer.

Quality flags map 1:1 to exception types so callers can branch on severity:

    OK        — Primary source returned fresh data.
    WARNING   — Secondary source used; data is fresh but provenance is weaker.
    DEGRADED  — Cache used; data is stale but within sane bounds.
    CRITICAL  — All sources failed AND no usable cache. Analysis cannot proceed.

Patterns:
    try:
        result = fetch_with_quality("us", "prices", "AAPL")
    except CriticalError as e:
        # halt analysis
    except DegradedError as e:
        # proceed but flag in report

Most callers don't need to raise these — the wrapper attaches them via
FetchResult.quality. Exceptions are reserved for: (a) when caller explicitly
needs to halt on degraded data; (b) tests asserting on cascade behaviour.
"""
from __future__ import annotations


class DataError(Exception):
    """Base class for all data-layer errors."""
    quality: str = "UNKNOWN"


class CriticalError(DataError):
    """No source produced usable data — primary, secondary, OR cache.

    Caller should halt and surface to user. Common causes:
      - Ticker invalid / delisted
      - All APIs down simultaneously (rare)
      - Cache empty (first run for new ticker, all APIs down)
    """
    quality = "CRITICAL"


class DegradedError(DataError):
    """Live sources failed but cache rescued the call.

    Quality flag should propagate to the report ("data is N days old").
    Not raised by default — wrapper returns a FetchResult with quality=DEGRADED.
    Use this when caller wants STRICT mode (no stale data tolerated).
    """
    quality = "DEGRADED"


class WarningError(DataError):
    """Primary source failed, secondary succeeded.

    Data is fresh but provenance is weaker (e.g. yfinance vs EODHD).
    Not raised by default — wrapper returns a FetchResult with quality=WARNING.
    Use this when caller wants ULTRA-STRICT mode (only primary tolerated).
    """
    quality = "WARNING"


class RateLimitError(DataError):
    """Specific subtype of source failure: quota exhausted.

    Catchable separately for callers who want to back off rather than fall through.
    Adapters raise this when an API returns 429 or equivalent.
    """
    quality = "WARNING"


class ValidationError(DataError):
    """Data was returned but failed sanity guards (e.g. P/E > 1000, DY < 0).

    Reject reason logged but next source attempted. If all sources reject:
    CriticalError raised by wrapper.
    """
    quality = "WARNING"
