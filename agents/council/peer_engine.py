"""Peer Comparison Engine — Sprint 2 of STORYT_3.0.

Computes sector medians from the actual DB instead of the hardcoded
SECTOR_MEDIAN_PE_BR table. Fixes "Dado não disponível" in the multiples
comparison act of the storytelling.

For each sector × market, pull all tickers in the same sector with non-null
fundamentals (latest period_end) and compute robust medians for:
  - P/E
  - P/B
  - DY
  - ROE
  - ND/EBITDA
  - FCF Yield (computed from market_cap + free_cash_flow when available)

Falls back to published-mediana table only when DB has < 3 peers.
"""
from __future__ import annotations

import sqlite3
import statistics
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}

# Fallback medianas published — used when DB has < 3 peers in same sector
PUBLISHED_FALLBACK: dict[tuple[str, str], dict[str, float]] = {
    # (sector, market): {metric: median}
    ("Industrials", "br"): {"pe": 12.0, "pb": 1.8, "dy": 0.04, "roe": 0.13, "net_debt_ebitda": 2.5, "fcf_yield": 0.05},
    ("Consumer Staples", "br"): {"pe": 14.0, "pb": 2.5, "dy": 0.04, "roe": 0.16, "net_debt_ebitda": 2.0, "fcf_yield": 0.05},
    ("Consumer Disc.", "br"): {"pe": 13.0, "pb": 2.0, "dy": 0.03, "roe": 0.14, "net_debt_ebitda": 2.5, "fcf_yield": 0.04},
    ("Healthcare", "br"): {"pe": 16.0, "pb": 2.5, "dy": 0.03, "roe": 0.15, "net_debt_ebitda": 2.5, "fcf_yield": 0.04},
    ("Utilities", "br"): {"pe": 11.0, "pb": 2.0, "dy": 0.06, "roe": 0.13, "net_debt_ebitda": 3.0, "fcf_yield": 0.06},
    ("Materials", "br"): {"pe": 10.0, "pb": 1.5, "dy": 0.05, "roe": 0.15, "net_debt_ebitda": 1.5, "fcf_yield": 0.07},
    ("Real Estate", "br"): {"pe": 14.0, "pb": 1.5, "dy": 0.05, "roe": 0.10, "net_debt_ebitda": 4.0, "fcf_yield": 0.05},
    ("Holding", "br"): {"pe": 9.0, "pb": 1.5, "dy": 0.06, "roe": 0.15, "net_debt_ebitda": 2.5, "fcf_yield": 0.06},
    ("Banks", "br"): {"pe": 8.0, "pb": 1.3, "dy": 0.07, "roe": 0.18, "net_debt_ebitda": None, "fcf_yield": None},
    ("Oil & Gas", "br"): {"pe": 8.0, "pb": 1.5, "dy": 0.06, "roe": 0.18, "net_debt_ebitda": 1.0, "fcf_yield": 0.10},
    ("Mining", "br"): {"pe": 8.0, "pb": 1.5, "dy": 0.07, "roe": 0.18, "net_debt_ebitda": 1.0, "fcf_yield": 0.10},
    # US fallbacks
    ("Industrials", "us"): {"pe": 18.0, "pb": 3.0, "dy": 0.02, "roe": 0.18, "net_debt_ebitda": 2.0, "fcf_yield": 0.04},
    ("Consumer Staples", "us"): {"pe": 22.0, "pb": 5.0, "dy": 0.025, "roe": 0.25, "net_debt_ebitda": 2.5, "fcf_yield": 0.04},
    ("Healthcare", "us"): {"pe": 18.0, "pb": 4.0, "dy": 0.02, "roe": 0.20, "net_debt_ebitda": 2.0, "fcf_yield": 0.05},
    ("Banks", "us"): {"pe": 11.0, "pb": 1.4, "dy": 0.025, "roe": 0.13, "net_debt_ebitda": None, "fcf_yield": None},
}

# Index proxies (Ibovespa / S&P) — broad market median
INDEX_MEDIANS = {
    "br": {"pe": 9.0, "pb": 1.6, "dy": 0.06, "roe": 0.13, "fcf_yield": 0.05},
    "us": {"pe": 21.0, "pb": 3.5, "dy": 0.015, "roe": 0.16, "fcf_yield": 0.04},
}


@dataclass
class SectorBenchmark:
    sector: str
    market: str
    n_peers: int
    peers_used: list[str] = field(default_factory=list)
    median_pe: float | None = None
    median_pb: float | None = None
    median_dy: float | None = None
    median_roe: float | None = None
    median_nde: float | None = None
    median_fcf_yield: float | None = None
    source: str = "db"  # 'db' | 'published_fallback' | 'mixed'

    def render_comparison_table(self, ticker: str, ticker_metrics: dict) -> str:
        """Render the multiples comparison table for Acto 5."""
        idx_med = INDEX_MEDIANS.get(self.market.lower(), {})

        def fmt_pe(v): return f"{v:.2f}x" if v is not None else "—"
        def fmt_pct(v): return f"{v*100:.1f}%" if v is not None else "—"

        rows = [
            "| Múltiplo | " + ticker + " | Mediana setorial | Índice (Ibov/S&P) |",
            "|---|---|---|---|",
            f"| P/E | {fmt_pe(ticker_metrics.get('pe'))} | {fmt_pe(self.median_pe)} | {fmt_pe(idx_med.get('pe'))} |",
            f"| P/B | {fmt_pe(ticker_metrics.get('pb'))} | {fmt_pe(self.median_pb)} | {fmt_pe(idx_med.get('pb'))} |",
            f"| DY | {fmt_pct(ticker_metrics.get('dy'))} | {fmt_pct(self.median_dy)} | {fmt_pct(idx_med.get('dy'))} |",
            f"| FCF Yield | {fmt_pct(ticker_metrics.get('fcf_yield'))} | {fmt_pct(self.median_fcf_yield)} | {fmt_pct(idx_med.get('fcf_yield'))} |",
            f"| ROE | {fmt_pct(ticker_metrics.get('roe'))} | {fmt_pct(self.median_roe)} | {fmt_pct(idx_med.get('roe'))} |",
            f"| ND/EBITDA | {fmt_pe(ticker_metrics.get('net_debt_ebitda'))} | {fmt_pe(self.median_nde)} | — |",
        ]
        return "\n".join(rows)


def _safe_median(values: list[float | None]) -> float | None:
    clean = [v for v in values if v is not None and v == v]  # filter None and NaN
    if len(clean) < 3:
        return None
    return statistics.median(clean)


def compute_sector_benchmark(ticker: str, market: str, sector: str) -> SectorBenchmark:
    """Pull peers in the same sector and compute robust medians."""
    db = DBS.get(market)
    if not db or not db.exists():
        return _fallback_benchmark(sector, market)

    bench = SectorBenchmark(sector=sector or "?", market=market, n_peers=0)
    if not sector:
        return _fallback_benchmark(sector, market)

    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        # Get latest fundamentals per peer in same sector (excluding the ticker itself)
        try:
            rows = c.execute("""
                SELECT c.ticker, f.pe, f.pb, f.dy, f.roe, f.net_debt_ebitda
                FROM companies c
                JOIN fundamentals f ON f.ticker = c.ticker
                WHERE c.sector = ?
                  AND c.ticker != ?
                  AND f.period_end = (
                      SELECT MAX(period_end) FROM fundamentals
                      WHERE ticker = c.ticker
                  )
            """, (sector, ticker)).fetchall()
        except sqlite3.OperationalError:
            return _fallback_benchmark(sector, market)

        if not rows:
            return _fallback_benchmark(sector, market)

        bench.peers_used = [r["ticker"] for r in rows]
        bench.n_peers = len(rows)
        bench.median_pe = _safe_median([r["pe"] for r in rows if r["pe"] and r["pe"] > 0])
        bench.median_pb = _safe_median([r["pb"] for r in rows if r["pb"] and r["pb"] > 0])
        bench.median_dy = _safe_median([r["dy"] for r in rows if r["dy"] and r["dy"] > 0])
        bench.median_roe = _safe_median([r["roe"] for r in rows if r["roe"] is not None])
        bench.median_nde = _safe_median([r["net_debt_ebitda"] for r in rows if r["net_debt_ebitda"] is not None])

        # FCF Yield from deep_fundamentals + market_cap_at_fetch
        try:
            fcf_rows = c.execute("""
                SELECT df.free_cash_flow, df.market_cap_at_fetch
                FROM deep_fundamentals df
                WHERE df.ticker IN ({})
                  AND df.period_type = 'annual'
                  AND df.period_end = (
                      SELECT MAX(period_end) FROM deep_fundamentals
                      WHERE ticker = df.ticker AND period_type = 'annual'
                  )
            """.format(",".join("?" * len(bench.peers_used))), bench.peers_used).fetchall()
            yields = [
                r["free_cash_flow"] / r["market_cap_at_fetch"]
                for r in fcf_rows
                if r["free_cash_flow"] and r["market_cap_at_fetch"] and r["market_cap_at_fetch"] > 0
            ]
            bench.median_fcf_yield = _safe_median(yields)
        except sqlite3.OperationalError:
            pass

    bench.source = "db"

    # If many medians are None, fill from published fallback
    fallback = PUBLISHED_FALLBACK.get((sector, market.lower())) or {}
    filled_from_fallback = False
    if bench.median_pe is None and fallback.get("pe") is not None:
        bench.median_pe = fallback["pe"]; filled_from_fallback = True
    if bench.median_pb is None and fallback.get("pb") is not None:
        bench.median_pb = fallback["pb"]; filled_from_fallback = True
    if bench.median_dy is None and fallback.get("dy") is not None:
        bench.median_dy = fallback["dy"]; filled_from_fallback = True
    if bench.median_roe is None and fallback.get("roe") is not None:
        bench.median_roe = fallback["roe"]; filled_from_fallback = True
    if bench.median_nde is None and fallback.get("net_debt_ebitda") is not None:
        bench.median_nde = fallback["net_debt_ebitda"]; filled_from_fallback = True
    if bench.median_fcf_yield is None and fallback.get("fcf_yield") is not None:
        bench.median_fcf_yield = fallback["fcf_yield"]; filled_from_fallback = True

    if filled_from_fallback and bench.n_peers > 0:
        bench.source = "mixed"
    elif filled_from_fallback:
        bench.source = "published_fallback"

    return bench


def _fallback_benchmark(sector: str, market: str) -> SectorBenchmark:
    fb = PUBLISHED_FALLBACK.get((sector, market.lower())) or {}
    return SectorBenchmark(
        sector=sector or "?",
        market=market,
        n_peers=0,
        peers_used=[],
        median_pe=fb.get("pe"),
        median_pb=fb.get("pb"),
        median_dy=fb.get("dy"),
        median_roe=fb.get("roe"),
        median_nde=fb.get("net_debt_ebitda"),
        median_fcf_yield=fb.get("fcf_yield"),
        source="published_fallback",
    )


def compute_ticker_fcf_yield(ticker: str, market: str) -> float | None:
    """Compute FCF Yield = FCF / Market Cap from deep_fundamentals."""
    db = DBS.get(market)
    if not db or not db.exists():
        return None
    with sqlite3.connect(db) as c:
        try:
            row = c.execute("""
                SELECT free_cash_flow, market_cap_at_fetch
                FROM deep_fundamentals
                WHERE ticker = ? AND period_type = 'annual'
                ORDER BY period_end DESC LIMIT 1
            """, (ticker,)).fetchone()
            if row and row[0] and row[1] and row[1] > 0:
                return float(row[0]) / float(row[1])
        except sqlite3.OperationalError:
            return None
    return None
