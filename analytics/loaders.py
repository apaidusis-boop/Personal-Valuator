"""Leitores puros de data/br_investments.db. Nenhum I/O de rede."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"


def load_prices(ticker: str, start: str | None = None, end: str | None = None,
                db: Path = DB_BR) -> pd.DataFrame:
    """DataFrame indexado por data (DatetimeIndex) com coluna `close`."""
    q = "SELECT date, close FROM prices WHERE ticker=?"
    params: list = [ticker]
    if start:
        q += " AND date >= ?"; params.append(start)
    if end:
        q += " AND date <= ?"; params.append(end)
    q += " ORDER BY date"
    with sqlite3.connect(db) as conn:
        df = pd.read_sql_query(q, conn, params=params, parse_dates=["date"])
    return df.set_index("date")


def load_dividends(ticker: str, start: str | None = None, end: str | None = None,
                   db: Path = DB_BR) -> pd.DataFrame:
    """Eventos de dividendos entre ex_date ∈ [start, end].

    Colunas: `amount`, `kind`. Index = ex_date (DatetimeIndex).
    Inclui JCP e rendimentos — todos contam para total return.
    """
    q = "SELECT ex_date, amount, kind FROM dividends WHERE ticker=?"
    params: list = [ticker]
    if start:
        q += " AND ex_date >= ?"; params.append(start)
    if end:
        q += " AND ex_date <= ?"; params.append(end)
    q += " ORDER BY ex_date"
    with sqlite3.connect(db) as conn:
        df = pd.read_sql_query(q, conn, params=params, parse_dates=["ex_date"])
    return df.set_index("ex_date")


def load_series(series_id: str, start: str | None = None, end: str | None = None,
                db: Path = DB_BR) -> pd.DataFrame:
    """Série temporal de `series` (SELIC, CDI, IPCA, IBOV, ...).

    Coluna única `value`. Index = data (DatetimeIndex).
    """
    q = "SELECT date, value FROM series WHERE series_id=?"
    params: list = [series_id]
    if start:
        q += " AND date >= ?"; params.append(start)
    if end:
        q += " AND date <= ?"; params.append(end)
    q += " ORDER BY date"
    with sqlite3.connect(db) as conn:
        df = pd.read_sql_query(q, conn, params=params, parse_dates=["date"])
    return df.set_index("date")
