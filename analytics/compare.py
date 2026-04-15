"""Comparação de séries heterogéneas — tickers, macro, benchmarks.

Aceita uma lista de "specs" e devolve um DataFrame alinhado por data útil,
opcionalmente normalizado a 100 na data-base. Especificações:

    "ITSA4"          → total return do ticker (inclui dividendos + JCP)
    "ITSA4:price"    → preço unadjusted (sem reinvestimento)
    "SELIC_DAILY"    → série macro, acumulada daily
    "IBOV"           → série (preço do índice)
    "CDI_DAILY"      → análogo a SELIC

Séries "rate" (SELIC_DAILY, CDI_DAILY) são tratadas como taxa diária e
convertidas em índice cumulativo: idx_t = Π (1 + r_k) para k ≤ t.

Séries "level" (IBOV, USDBRL, prices) são usadas directamente.
"""
from __future__ import annotations

import pandas as pd

from .loaders import load_prices, load_series
from .total_return import total_return_series

RATE_SERIES = {"SELIC_DAILY", "CDI_DAILY"}


def _load_spec(spec: str, start: str, end: str) -> pd.Series:
    if ":" in spec:
        ticker, kind = spec.split(":", 1)
    else:
        ticker, kind = spec, None

    # macro / benchmark séries
    if ticker.isupper() and ticker in RATE_SERIES:
        df = load_series(ticker, start=start, end=end)
        if df.empty:
            raise ValueError(f"série {ticker} vazia em [{start}, {end}]")
        rates = df["value"]
        idx = (1.0 + rates).cumprod()
        return idx.rename(spec)

    if ticker.isupper() and ticker in {"IBOV", "IFIX", "SELIC_META", "USDBRL_PTAX", "IPCA_MONTHLY"}:
        df = load_series(ticker, start=start, end=end)
        if df.empty:
            raise ValueError(f"série {ticker} vazia em [{start}, {end}]")
        return df["value"].rename(spec)

    # ticker: preço puro ou total return
    if kind == "price":
        df = load_prices(ticker, start=start, end=end)
        if df.empty:
            raise ValueError(f"sem preços para {ticker} em [{start}, {end}]")
        return df["close"].rename(spec)

    # default: total return
    df = total_return_series(ticker, start=start, end=end)
    if df.empty:
        raise ValueError(f"sem total return para {ticker} em [{start}, {end}]")
    return df["tr_close"].rename(spec)


def compare(specs: list[str], start: str, end: str,
            normalize: bool = True) -> pd.DataFrame:
    """Alinha as séries pelo dia útil e opcionalmente normaliza a 100
    na primeira data comum."""
    series = [_load_spec(s, start, end) for s in specs]
    # join outer e forward-fill para alinhar dias úteis (cada série tem calendário próprio)
    df = pd.concat(series, axis=1).sort_index().ffill().dropna()
    if normalize and not df.empty:
        df = df / df.iloc[0] * 100.0
    return df


def growth_pct(df: pd.DataFrame) -> pd.Series:
    """Retorno total entre a primeira e a última linha, em %."""
    if df.empty:
        return pd.Series(dtype=float)
    return (df.iloc[-1] / df.iloc[0] - 1.0) * 100.0
