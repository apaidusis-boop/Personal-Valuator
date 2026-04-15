"""Total return para tickers BR.

Dado preço diário unadjusted (tabela `prices`) e eventos de dividendos
(tabela `dividends`), calcula um factor cumulativo que representa o
retorno de alguém que reinveste cada provento no dia ex.

Fórmula clássica do ajuste dividend-paid:
    ratio_t = (close_{t-1} + D_t) / close_{t-1}   para cada dia t com dividendo
    ratio_t = 1                                    caso contrário
    tr_factor_t = Π ratio_k (k ≤ t) × (close_t / close_0)

Equivalentemente: construímos uma série `tr_close` reinvestindo proventos
em cotas adicionais e reportamos o valor do "portfólio de 1 cota inicial".

Puro: não faz I/O de rede, só lê da DB.
"""
from __future__ import annotations

import pandas as pd

from .loaders import load_dividends, load_prices


def total_return_series(ticker: str, start: str | None = None,
                        end: str | None = None) -> pd.DataFrame:
    """Devolve DataFrame com colunas:
        close       — preço unadjusted do dia
        dividend    — proventos do dia (0 se nenhum)
        tr_close    — preço total-return reinvestido (começa = close[0])
        tr_factor   — tr_close / close[0] (crescimento normalizado a 1.0)
    """
    prices = load_prices(ticker, start=start, end=end)
    if prices.empty:
        return prices.assign(dividend=[], tr_close=[], tr_factor=[])

    divs = load_dividends(ticker,
                          start=prices.index.min().strftime("%Y-%m-%d"),
                          end=prices.index.max().strftime("%Y-%m-%d"))
    # agregar por dia caso haja múltiplos eventos no mesmo ex_date
    if not divs.empty:
        div_daily = divs.groupby(divs.index)["amount"].sum()
    else:
        div_daily = pd.Series(dtype=float)

    df = prices.copy()
    df["dividend"] = div_daily.reindex(df.index).fillna(0.0)

    # ratio por dia: 1 + D_t / close_{t-1}. No dia 0 é 1.
    prev_close = df["close"].shift(1)
    ratio = 1.0 + (df["dividend"] / prev_close).fillna(0.0)
    # growth por preço: close_t / close_{t-1}
    price_growth = (df["close"] / prev_close).fillna(1.0)
    # retorno total diário = crescimento de preço × ratio de reinvestimento
    daily_tr = price_growth * ratio
    daily_tr.iloc[0] = 1.0  # âncora

    df["tr_factor"] = daily_tr.cumprod()
    df["tr_close"] = df["tr_factor"] * df["close"].iloc[0]
    return df[["close", "dividend", "tr_close", "tr_factor"]]
