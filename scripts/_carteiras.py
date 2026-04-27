"""_carteiras — leitor de config/carteiras_recomendadas.yaml + helpers.

Pure data layer (no Streamlit imports).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "config" / "carteiras_recomendadas.yaml"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


@dataclass
class Holding:
    ticker: str
    peso: float


@dataclass
class Carteira:
    id: str
    name: str
    fonte: str
    data_base: str
    type: str
    holdings: list[Holding]

    @property
    def tickers(self) -> list[str]:
        return [h.ticker for h in self.holdings if h.peso > 0]

    @property
    def n_holdings(self) -> int:
        return len([h for h in self.holdings if h.peso > 0])


@lru_cache(maxsize=1)
def load_carteiras() -> list[Carteira]:
    """Load all carteiras from YAML."""
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    out = []
    for c in data["carteiras"]:
        holdings = [Holding(**h) for h in c["holdings"]]
        out.append(Carteira(
            id=c["id"], name=c["name"], fonte=c["fonte"],
            data_base=c["data_base"], type=c["type"], holdings=holdings,
        ))
    return out


def get_carteira(carteira_id: str) -> Carteira | None:
    for c in load_carteiras():
        if c.id == carteira_id:
            return c
    return None


def fetch_prices(tickers: list[str], market: str = "br", years: int = 5) -> pd.DataFrame:
    """Fetch close prices for a list of tickers from the appropriate DB.

    Returns wide DataFrame (date index, ticker columns). NaN where missing.
    """
    db = DB_BR if market == "br" else DB_US
    if not tickers:
        return pd.DataFrame()
    cutoff = (date.today() - timedelta(days=years * 366)).isoformat()
    placeholders = ",".join("?" for _ in tickers)
    q = (
        f"SELECT ticker, date, close FROM prices "
        f"WHERE ticker IN ({placeholders}) AND date >= ? "
        f"ORDER BY date"
    )
    with sqlite3.connect(db) as c:
        df = pd.read_sql_query(q, c, params=[*tickers, cutoff], parse_dates=["date"])
    if df.empty:
        return pd.DataFrame()
    return df.pivot(index="date", columns="ticker", values="close").sort_index()


def normalize_to_100(prices: pd.DataFrame) -> pd.DataFrame:
    """Re-base each column to 100 at the first non-null observation."""
    out = pd.DataFrame(index=prices.index)
    for col in prices.columns:
        s = prices[col].dropna()
        if s.empty:
            continue
        out[col] = (prices[col] / s.iloc[0]) * 100
    return out


def compute_basket(prices: pd.DataFrame, weights: dict[str, float] | None = None) -> pd.Series:
    """Compute weighted basket return series, normalized to 100.

    If weights is None, equal-weighted.
    """
    if prices.empty:
        return pd.Series(dtype=float)
    if weights:
        w = pd.Series(weights)
        w = w[w.index.intersection(prices.columns)]
        w = w / w.sum()
        normalized = normalize_to_100(prices[w.index])
        return (normalized * w).sum(axis=1, min_count=1)
    normalized = normalize_to_100(prices)
    return normalized.mean(axis=1)


def fetch_index(index_ticker: str = "^BVSP", years: int = 5) -> pd.Series:
    """Fetch index series. Tries DB first; if missing, falls back to yfinance."""
    cutoff = (date.today() - timedelta(days=years * 366)).isoformat()
    for db in (DB_BR, DB_US):
        try:
            with sqlite3.connect(db) as c:
                r = pd.read_sql_query(
                    "SELECT date, close FROM prices WHERE ticker = ? AND date >= ? ORDER BY date",
                    c, params=[index_ticker, cutoff], parse_dates=["date"],
                )
                if not r.empty:
                    return r.set_index("date")["close"]
        except Exception:
            continue
    # Fallback to yfinance live
    try:
        import yfinance as yf
        df = yf.Ticker(index_ticker).history(period=f"{years}y")
        if not df.empty:
            df.index = df.index.tz_localize(None) if df.index.tz else df.index
            return df["Close"]
    except Exception:
        pass
    return pd.Series(dtype=float)


def latest_close(ticker: str, market: str = "br") -> float | None:
    db = DB_BR if market == "br" else DB_US
    try:
        with sqlite3.connect(db) as c:
            r = c.execute(
                "SELECT close FROM prices WHERE ticker = ? ORDER BY date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            return float(r[0]) if r else None
    except Exception:
        return None


def return_5y(ticker: str, market: str = "br") -> float | None:
    """5-year total return % (price-only, no dividends)."""
    db = DB_BR if market == "br" else DB_US
    cutoff = (date.today() - timedelta(days=5 * 365)).isoformat()
    try:
        with sqlite3.connect(db) as c:
            first = c.execute(
                "SELECT close FROM prices WHERE ticker = ? AND date >= ? ORDER BY date LIMIT 1",
                (ticker, cutoff),
            ).fetchone()
            last = c.execute(
                "SELECT close FROM prices WHERE ticker = ? ORDER BY date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if first and last and first[0] > 0:
                return (last[0] / first[0] - 1) * 100
    except Exception:
        pass
    return None
