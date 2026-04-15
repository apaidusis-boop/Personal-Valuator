"""yfinance fetcher para BR — preços unadjusted + eventos de dividendos.

Porquê: o plano free da brapi devolve histórico de 3 meses e não expõe
dividendos para a maioria dos tickers. yfinance é gratuito, sem token e
devolve histórico longo + Dividends por ticker.SA.

Persiste em data/br_investments.db:
  - prices (ticker, date, close unadjusted, volume)
  - dividends (ticker, ex_date, amount, kind, source, ...)

Não toca em fundamentals — isso fica com brapi/Status Invest. Isto é só
para análise de preço e total return.

Uso:
    python fetchers/yf_br_fetcher.py ITSA4
    python fetchers/yf_br_fetcher.py ITSA4 --period 5y
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "yf_br_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _yf_symbol(ticker: str) -> str:
    return ticker if ticker.endswith(".SA") else f"{ticker}.SA"


def _fetch_dividends_resilient(tk, ticker: str):
    """Obtém dividendos com cascata de estratégias, resiliente a versões do yfinance.

    Bug conhecido em yfinance ~0.2.40–0.2.55: `tk.dividends` pode levantar
    `'PriceHistory' object has no attribute '_dividends'` quando o estado
    interno do Ticker não foi inicializado. Solução: fallback em cascata.

    Devolve (series | None, strategy_name).
    """
    # Estratégia 1: API directa (caminho rápido quando funciona).
    try:
        d = tk.dividends
        if d is not None and len(d) > 0:
            return d, "tk.dividends"
    except Exception as exc:  # noqa: BLE001
        _log({"event": "yf_dividends_strategy_failed", "ticker": ticker,
              "strategy": "tk.dividends", "err": str(exc)})

    # Estratégia 2: history(max, actions=True) força lazy-load correcto
    # e devolve os dividendos como coluna.
    try:
        h = tk.history(period="max", actions=True, auto_adjust=False)
        if h is not None and "Dividends" in h.columns:
            d = h["Dividends"]
            d = d[d > 0]
            if len(d) > 0:
                return d, "history_actions"
    except Exception as exc:  # noqa: BLE001
        _log({"event": "yf_dividends_strategy_failed", "ticker": ticker,
              "strategy": "history_actions", "err": str(exc)})

    # Estratégia 3: tk.actions dataframe (última tentativa).
    try:
        a = tk.actions
        if a is not None and "Dividends" in a.columns:
            d = a["Dividends"]
            d = d[d > 0]
            if len(d) > 0:
                return d, "tk.actions"
    except Exception as exc:  # noqa: BLE001
        _log({"event": "yf_dividends_strategy_failed", "ticker": ticker,
              "strategy": "tk.actions", "err": str(exc)})

    return None, "none"


def fetch(ticker: str, period: str = "1y"):
    sym = _yf_symbol(ticker)
    tk = yf.Ticker(sym)
    # auto_adjust=False para preservar Close unadjusted; as colunas Dividends
    # e Stock Splits são os eventos que precisamos para computar TR nós.
    hist = tk.history(period=period, auto_adjust=False)
    divs_series, div_strategy = _fetch_dividends_resilient(tk, ticker)
    if divs_series is None:
        _log({"event": "yf_dividends_unavailable", "ticker": ticker,
              "reason": "all strategies failed"})
    else:
        _log({"event": "yf_dividends_strategy_ok", "ticker": ticker,
              "strategy": div_strategy, "count": len(divs_series)})
    return hist, divs_series


def upsert_prices(conn: sqlite3.Connection, ticker: str, hist) -> int:
    if hist is None or len(hist) == 0:
        return 0
    n = 0
    for idx, row in hist.iterrows():
        date = idx.strftime("%Y-%m-%d")
        close = row.get("Close")
        vol = row.get("Volume")
        if close is None or (isinstance(close, float) and close != close):  # NaN
            continue
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (ticker, date, float(close), int(vol) if vol is not None and vol == vol else None),
        )
        n += 1
    return n


def upsert_dividends(conn: sqlite3.Connection, ticker: str, divs) -> int:
    if divs is None or len(divs) == 0:
        return 0
    # yfinance pode devolver Series ou DataFrame conforme a versão.
    # Normalizar para (index, value).
    try:
        import pandas as pd
        if isinstance(divs, pd.DataFrame):
            col = "Dividends" if "Dividends" in divs.columns else divs.columns[0]
            divs = divs[col]
    except Exception:
        pass
    now = _now_iso()
    n = 0
    for idx, amount in divs.items():
        ex_date = idx.strftime("%Y-%m-%d")
        try:
            amt = float(amount)
        except (TypeError, ValueError):
            continue
        if amt <= 0:
            continue
        # yfinance não distingue dividend vs JCP; marcamos 'cash'.
        # Tarefa futura: cruzar com B3/CVM para taggar JCP.
        conn.execute(
            """INSERT INTO dividends
                 (ticker, ex_date, pay_date, amount, currency, kind, source, fetched_at)
               VALUES (?,?,?,?,?,?,?,?)
               ON CONFLICT(ticker, ex_date, kind) DO UPDATE SET
                 amount=excluded.amount, source=excluded.source,
                 fetched_at=excluded.fetched_at""",
            (ticker, ex_date, None, amt, "BRL", "cash", "yfinance", now),
        )
        n += 1
    return n


def run(ticker: str, period: str = "1y") -> dict:
    ticker = ticker.upper()
    _log({"event": "yf_br_fetch_start", "ticker": ticker, "period": period})
    hist, divs = fetch(ticker, period=period)

    with sqlite3.connect(DB_PATH) as conn:
        # garantir companies (não falha se já existir)
        conn.execute(
            """INSERT INTO companies (ticker, name, sector, is_holding, currency)
               VALUES (?, ?, NULL, 0, 'BRL')
               ON CONFLICT(ticker) DO NOTHING""",
            (ticker, ticker),
        )
        n_prices = upsert_prices(conn, ticker, hist)
        n_divs = upsert_dividends(conn, ticker, divs)
        conn.commit()

    result = {"ticker": ticker, "prices": n_prices, "dividends": n_divs,
              "price_range": [hist.index[0].strftime("%Y-%m-%d"),
                              hist.index[-1].strftime("%Y-%m-%d")] if len(hist) else None,
              "div_count_all_time": len(divs) if divs is not None else 0}
    _log({"event": "yf_br_persisted", **result})
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--period", default="1y",
                    help="yfinance period: 1mo,3mo,6mo,1y,2y,5y,10y,max")
    args = ap.parse_args()
    run(args.ticker, period=args.period)


if __name__ == "__main__":
    main()
