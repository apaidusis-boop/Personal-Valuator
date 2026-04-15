"""Fetcher yfinance — histórico longo de preços e dividendos (BR+US).

Passa a ser a fonte primária de histórico longo em ambos os mercados.
O brapi free só dá 3 meses; o Status Invest não tem API de preços.
yfinance é gratuito, sem auth, e aceita tickers BR com sufixo .SA e
índices como ^BVSP / ^GSPC.

Responsabilidades:
  - prices (série diária, até 10y)
  - dividends_annual (agregados por ano a partir do calendário de pagamentos)
  - companies (upsert a partir de universe.yaml)

NÃO toca em fundamentals — fundamentals BR continuam a vir do
Status Invest (mais detalhado), fundamentals US virão de yfinance
na próxima fase (Sprint 3).

Uso:
    python fetchers/yfinance_fetcher.py                 # ITSA4 (BR)
    python fetchers/yfinance_fetcher.py PRIO3
    python fetchers/yfinance_fetcher.py AAPL --market us
    python fetchers/yfinance_fetcher.py ITSA4 --period 5y
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
import yfinance as yf

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fetchers.cache_policy import is_fresh, now_iso, statement_policy_for  # noqa: E402

ROOT = _ROOT
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "yfinance_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def load_universe_entry(ticker: str, market: str) -> dict | None:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    node = data.get(market, {}) or {}
    pools: list[dict] = []
    # holdings.* (dict de sections)
    for section in (node.get("holdings") or {}).values():
        pools.extend(section or [])
    # watchlist.* (dict de sections — stocks, fiis)
    wl = node.get("watchlist") or {}
    if isinstance(wl, dict):
        for section in wl.values():
            pools.extend(section or [])
    elif isinstance(wl, list):
        pools.extend(wl)  # backwards compat
    # research_pool — também aceita mas só se explicitamente pedido
    rp = node.get("research_pool") or {}
    if isinstance(rp, dict):
        for section in rp.values():
            pools.extend(section or [])
    for entry in pools:
        if entry["ticker"] == ticker:
            return entry
    return None


def yf_symbol(ticker: str, market: str) -> str:
    if market == "br" and not ticker.endswith(".SA") and not ticker.startswith("^"):
        return f"{ticker}.SA"
    return ticker


# ---------- persistência ----------

def upsert_company(conn: sqlite3.Connection, entry: dict, currency: str) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(ticker) DO UPDATE SET
             name=excluded.name, sector=excluded.sector,
             is_holding=excluded.is_holding, currency=excluded.currency""",
        (
            entry["ticker"],
            entry["name"],
            entry.get("sector"),
            1 if entry.get("is_holding") else 0,
            currency,
        ),
    )


def upsert_prices(conn: sqlite3.Connection, ticker: str, history) -> int:
    n = 0
    for ts, row in history.iterrows():
        date = ts.strftime("%Y-%m-%d")
        close = row.get("Close")
        volume = row.get("Volume")
        if close is None or close != close:  # NaN check
            continue
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (ticker, date, float(close), int(volume) if volume == volume else None),
        )
        n += 1
    return n


# ---------- statements (DRE / BP / DFC) ----------

# Mapeamento de nomes de linha do yfinance para os nossos campos.
# yfinance varia entre versões; tentamos múltiplas variantes e usamos o
# primeiro hit. None se nenhum casar.
INCOME_MAP = {
    "revenue":      ["Total Revenue", "Revenue", "TotalRevenue"],
    "gross_profit": ["Gross Profit", "GrossProfit"],
    "ebit":         ["EBIT", "Operating Income", "OperatingIncome"],
    "ebitda":       ["EBITDA", "Normalized EBITDA"],
    "net_income":   ["Net Income", "NetIncome", "Net Income Common Stockholders"],
}
BALANCE_MAP = {
    "total_assets":        ["Total Assets", "TotalAssets"],
    "current_assets":      ["Current Assets", "Total Current Assets"],
    "cash_equivalents":    ["Cash And Cash Equivalents", "CashAndCashEquivalents", "Cash"],
    "total_liabilities":   ["Total Liabilities Net Minority Interest", "Total Liab", "TotalLiabilities"],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"],
    "long_term_debt":      ["Long Term Debt", "LongTermDebt"],
    "total_equity":        ["Stockholders Equity", "Total Stockholder Equity", "TotalEquityGrossMinorityInterest"],
}
CASHFLOW_MAP = {
    "operating_cash_flow": ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities", "Total Cash From Operating Activities"],
    "investing_cash_flow": ["Investing Cash Flow", "Cash Flow From Continuing Investing Activities", "Total Cashflows From Investing Activities"],
    "financing_cash_flow": ["Financing Cash Flow", "Cash Flow From Continuing Financing Activities", "Total Cash From Financing Activities"],
    "capex":               ["Capital Expenditure", "CapitalExpenditures"],
    "free_cash_flow":      ["Free Cash Flow", "FreeCashFlow"],
}


def _pick(df, candidates: list[str]):
    """Devolve a Series da primeira linha que casar, ou None."""
    if df is None or df.empty:
        return None
    for name in candidates:
        if name in df.index:
            return df.loc[name]
    return None


def _series_to_dict(df, field_map: dict[str, list[str]]) -> dict[str, dict]:
    """Converte um DataFrame do yfinance (colunas = períodos) num dict
    {period_end_iso: {field: value, ...}}."""
    if df is None or df.empty:
        return {}
    out: dict[str, dict] = {}
    for col in df.columns:
        period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)[:10]
        row: dict[str, float | None] = {}
        for field, candidates in field_map.items():
            series = _pick(df, candidates)
            if series is None or col not in series.index:
                row[field] = None
                continue
            val = series[col]
            row[field] = float(val) if val == val else None  # NaN guard
        out[period] = row
    return out


def upsert_statements(conn: sqlite3.Connection, ticker: str, tk: "yf.Ticker") -> dict:
    """Busca DRE/BP/DFC anuais do yfinance e persiste. Respeita a política
    de cache: períodos já imutáveis em DB não são sobrescritos."""
    result = {"income": 0, "balance": 0, "cashflow": 0, "skipped": 0}
    try:
        income = tk.income_stmt
        balance = tk.balance_sheet
        cashflow = tk.cash_flow
    except Exception as exc:  # noqa: BLE001
        _log({"event": "yf_statements_error", "ticker": ticker, "err": str(exc)})
        return result

    now = now_iso()
    for table, field_map, df, counter in (
        ("income_statements",      INCOME_MAP,   income,   "income"),
        ("balance_sheets",         BALANCE_MAP,  balance,  "balance"),
        ("cash_flow_statements",   CASHFLOW_MAP, cashflow, "cashflow"),
    ):
        parsed = _series_to_dict(df, field_map)
        for period_end, fields in parsed.items():
            # cache check: se já temos e é imutável, skip
            existing = conn.execute(
                f"SELECT fetched_at FROM {table} WHERE ticker=? AND period_end=? AND period_type='annual'",
                (ticker, period_end),
            ).fetchone()
            policy_key = statement_policy_for(period_end, "annual")
            if existing and is_fresh(existing[0], policy_key):
                result["skipped"] += 1
                continue
            cols = ["ticker", "period_end", "period_type"] + list(fields.keys()) + ["source", "fetched_at"]
            placeholders = ",".join("?" * len(cols))
            updates = ",".join(f"{c}=excluded.{c}" for c in cols[3:])
            values = [ticker, period_end, "annual"] + list(fields.values()) + ["yfinance", now]
            conn.execute(
                f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders}) "
                f"ON CONFLICT(ticker, period_end, period_type) DO UPDATE SET {updates}",
                values,
            )
            result[counter] += 1
    return result


def upsert_dividends_annual(conn: sqlite3.Connection, ticker: str, dividends) -> int:
    """yfinance devolve Series indexed by payment date. Agregamos por ano."""
    if dividends is None or len(dividends) == 0:
        return 0
    import pandas as pd
    # yfinance pode devolver Series ou DataFrame — normalizar para Series.
    if isinstance(dividends, pd.DataFrame):
        col = "Dividends" if "Dividends" in dividends.columns else dividends.columns[0]
        series = dividends[col]
    else:
        series = dividends
    totals: dict[int, float] = {}
    for ts, amt in series.items():
        year = pd.Timestamp(ts).year
        totals[year] = totals.get(year, 0.0) + float(amt)
    n = 0
    for year, amount in totals.items():
        conn.execute(
            """INSERT INTO dividends_annual (ticker, year, amount) VALUES (?,?,?)
               ON CONFLICT(ticker, year) DO UPDATE SET amount=excluded.amount""",
            (ticker, year, amount),
        )
        n += 1
    return n


# ---------- pipeline ----------

def run(ticker: str, market: str = "br", period: str = "10y") -> None:
    entry = load_universe_entry(ticker, market)
    if entry is None:
        raise SystemExit(f"{ticker} não está em config/universe.yaml ({market})")

    symbol = yf_symbol(ticker, market)
    currency = "BRL" if market == "br" else "USD"
    db = DB_BR if market == "br" else DB_US

    _log({"event": "yf_fetch_start", "ticker": ticker, "symbol": symbol, "period": period})

    tk = yf.Ticker(symbol)
    hist = tk.history(period=period, auto_adjust=True)
    try:
        divs = tk.dividends  # pode vir vazia ou levantar AttributeError para alguns tickers
    except (AttributeError, Exception) as exc:  # noqa: BLE001
        _log({"event": "yf_dividends_unavailable", "ticker": ticker, "err": str(exc)})
        divs = None

    if hist is None or len(hist) == 0:
        raise SystemExit(f"yfinance devolveu histórico vazio para {symbol}")

    with sqlite3.connect(db) as conn:
        upsert_company(conn, entry, currency)
        n_prices = upsert_prices(conn, ticker, hist)
        n_divs = upsert_dividends_annual(conn, ticker, divs)
        statements = upsert_statements(conn, ticker, tk)
        conn.commit()

    _log({
        "event": "yf_persisted",
        "ticker": ticker,
        "prices_rows": n_prices,
        "prices_from": hist.index[0].strftime("%Y-%m-%d"),
        "prices_to": hist.index[-1].strftime("%Y-%m-%d"),
        "dividend_years": n_divs,
        "statements": statements,
    })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--period", default="10y",
                    help="1y, 2y, 5y, 10y, max (default 10y)")
    args = ap.parse_args()
    run(args.ticker, args.market, args.period)


if __name__ == "__main__":
    main()
