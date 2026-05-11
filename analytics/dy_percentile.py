"""DY vs own history — entry-timing context.

Computes current dividend yield percentile against a ticker's own trailing
history. Uses a monthly series of trailing-12m DY vs month-end price.

    percentile ≥ 75  → DY historically high → price historically depressed → CHEAP
    percentile ≤ 25  → DY historically low  → price historically elevated → EXPENSIVE

Phase F (2026-04) empirical caveat — see config/triggers.yaml:
O sinal NÃO gera alpha como stock-picker standalone. Uso correcto é contexto
observacional / entry-timing em posições já decididas por outras razões.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class DyPercentile:
    dy_now_pct: float       # DY trailing-12m actual em %
    percentile: float       # 0-100 onde dy_now se situa no histórico
    obs: int                # nº de observações mensais usadas
    lookback_years: int

    @property
    def label(self) -> str:
        if self.percentile >= 75:
            return "CHEAP"
        if self.percentile >= 50:
            return "fair-cheap"
        if self.percentile >= 25:
            return "fair-rich"
        return "EXPENSIVE"

    @property
    def short(self) -> str:
        """Símbolo compacto para tabelas densas."""
        if self.percentile >= 75:
            return "$"   # cheap
        if self.percentile <= 25:
            return "!"   # expensive
        return "·"


def _monthly_dy_series(
    conn: sqlite3.Connection, ticker: str, lookback_years: int
) -> list[float]:
    end_row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker=?", (ticker,)
    ).fetchone()
    if not end_row or not end_row[0]:
        return []
    end_dt = date.fromisoformat(end_row[0])
    start_dt = date(end_dt.year - lookback_years, end_dt.month, 1)

    out: list[float] = []
    cur = start_dt
    while cur <= end_dt:
        next_month = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)
        month_end = (next_month - timedelta(days=1)).isoformat()
        pr = conn.execute(
            "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
            (ticker, month_end),
        ).fetchone()
        if pr and pr[0] and pr[0] > 0:
            since = (date.fromisoformat(month_end) - timedelta(days=365)).isoformat()
            div_row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM dividends "
                "WHERE ticker=? AND ex_date<=? AND ex_date>? AND amount>0",
                (ticker, month_end, since),
            ).fetchone()
            div = (div_row[0] if div_row else 0) or 0
            if div > 0:
                out.append(100.0 * div / pr[0])
        cur = next_month
    return out


def compute(
    conn: sqlite3.Connection, ticker: str, lookback_years: int = 10, min_obs: int = 24
) -> DyPercentile | None:
    """Devolve DyPercentile ou None se histórico insuficiente."""
    hist = _monthly_dy_series(conn, ticker, lookback_years)
    if len(hist) < min_obs:
        return None
    dy_now = hist[-1]
    sorted_hist = sorted(hist)
    rank = sum(1 for v in sorted_hist if v < dy_now)
    pct = 100.0 * rank / len(sorted_hist)
    return DyPercentile(
        dy_now_pct=dy_now,
        percentile=pct,
        obs=len(hist),
        lookback_years=lookback_years,
    )
