"""yfinance fetcher para US — preços, dividendos e fundamentals.

Persiste em data/us_investments.db:
  - companies  (upsert a partir de universe.yaml)
  - prices     (unadjusted close + volume)
  - dividends  (eventos por ex_date, para total_return)
  - fundamentals (pe, pb, dy, roe, net_debt_ebitda, streak, aristocrat)

Os fundamentals são extraídos do dict `Ticker.info` do yfinance. Para US este
endpoint é razoavelmente fiável (ao contrário do BR, onde usamos brapi/SI).
A flag `is_aristocrat` não é devolvida pelo yfinance — fica NULL e pode ser
preenchida manualmente via universe.yaml se necessário.

Uso:
    python fetchers/yf_us_fetcher.py JNJ
    python fetchers/yf_us_fetcher.py JNJ --period 5y
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

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False, default=str)
    with (LOG_DIR / "yf_us_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def load_us_entry(ticker: str) -> dict | None:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    us = data.get("us", {}) or {}
    pools: list[dict] = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        group = us.get(bucket) or {}
        if isinstance(group, list):
            pools.extend(group)
        else:
            for v in (group or {}).values():
                pools.extend(v or [])
    for entry in pools:
        if entry.get("ticker") == ticker:
            return entry
    return None


def upsert_company(conn: sqlite3.Connection, entry: dict) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, ?, 'USD')
           ON CONFLICT(ticker) DO UPDATE SET
             name=excluded.name, sector=excluded.sector,
             is_holding=excluded.is_holding""",
        (
            entry["ticker"],
            entry.get("name", entry["ticker"]),
            entry.get("sector"),
            1 if entry.get("is_holding") else 0,
        ),
    )


def upsert_prices(conn: sqlite3.Connection, ticker: str, hist) -> int:
    if hist is None or len(hist) == 0:
        return 0
    n = 0
    for idx, row in hist.iterrows():
        date = idx.strftime("%Y-%m-%d")
        close = row.get("Close")
        vol = row.get("Volume")
        if close is None or (isinstance(close, float) and close != close):
            continue
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (ticker, date, float(close),
             int(vol) if vol is not None and vol == vol else None),
        )
        n += 1
    return n


def upsert_dividends(conn: sqlite3.Connection, ticker: str, divs) -> int:
    if divs is None or len(divs) == 0:
        return 0
    import pandas as pd
    if isinstance(divs, pd.DataFrame):
        col = "Dividends" if "Dividends" in divs.columns else divs.columns[0]
        divs = divs[col]
    now = _now_iso()
    n = 0
    for idx, amount in divs.items():
        try:
            ex_date = idx.strftime("%Y-%m-%d")
            amt = float(amount)
        except (TypeError, ValueError, AttributeError):
            continue
        if amt <= 0:
            continue
        conn.execute(
            """INSERT INTO dividends
                 (ticker, ex_date, pay_date, amount, currency, kind, source, fetched_at)
               VALUES (?,?,?,?,?,?,?,?)
               ON CONFLICT(ticker, ex_date, kind) DO UPDATE SET
                 amount=excluded.amount, fetched_at=excluded.fetched_at""",
            (ticker, ex_date, None, amt, "USD", "dividend", "yfinance", now),
        )
        n += 1
    return n


def compute_dividend_streak_years(divs) -> int | None:
    """Anos consecutivos com pelo menos um dividendo, a contar do mais
    recente. Um ano vazio interrompe o streak."""
    if divs is None or len(divs) == 0:
        return None
    import pandas as pd
    if isinstance(divs, pd.DataFrame):
        col = "Dividends" if "Dividends" in divs.columns else divs.columns[0]
        divs = divs[col]
    years = sorted({pd.Timestamp(ts).year for ts in divs.index}, reverse=True)
    if not years:
        return None
    streak = 1
    for i in range(1, len(years)):
        if years[i - 1] - years[i] == 1:
            streak += 1
        else:
            break
    return streak


def _f(v):
    if v is None:
        return None
    try:
        val = float(v)
        if val != val:
            return None
        return val
    except (TypeError, ValueError):
        return None


def _pick(df, keys: list[str]):
    """Devolve o primeiro valor encontrado para qualquer key em df.index
    na coluna mais recente (index[0]). yfinance renomeia campos entre versões."""
    if df is None or df.empty:
        return None
    col = df.columns[0]
    for k in keys:
        if k in df.index:
            v = df.loc[k, col]
            return _f(v)
    return None


def extract_reit_metrics(cashflow, financials, balance_sheet, shares_out):
    """FFO estimado, interest coverage, debt-to-assets.
    FFO = Net Income + D&A imobiliária. Aproximação (ignora gains on sales)."""
    net_income = _pick(cashflow, ["Net Income"]) or _pick(financials, ["Net Income"])
    da = _pick(cashflow, ["Depreciation And Amortization",
                          "Depreciation Amortization Depletion",
                          "Depreciation"])
    interest_exp = _pick(financials, ["Interest Expense"])
    ebitda = _pick(financials, ["EBITDA", "Normalized EBITDA"])
    total_debt = _pick(balance_sheet, ["Total Debt"])
    total_assets = _pick(balance_sheet, ["Total Assets"])

    ffo_per_share = None
    if net_income is not None and da is not None and shares_out and shares_out > 0:
        ffo_per_share = (net_income + da) / shares_out

    interest_coverage = None
    if ebitda is not None and interest_exp and interest_exp > 0:
        interest_coverage = ebitda / interest_exp

    debt_to_assets = None
    if total_debt is not None and total_assets and total_assets > 0:
        debt_to_assets = total_debt / total_assets

    return {
        "ffo_per_share": ffo_per_share,
        "interest_coverage": interest_coverage,
        "debt_to_assets": debt_to_assets,
    }


def extract_fundamentals(info: dict, divs, tk=None) -> dict:
    """Lê yfinance .info e normaliza para o schema `fundamentals`.
    Se tk (yf.Ticker) for fornecido, inclui métricas REIT (FFO, cobertura)."""
    pe = _f(info.get("trailingPE"))
    pb = _f(info.get("priceToBook"))
    dy = _f(info.get("dividendYield"))
    if dy is not None and dy > 1:
        dy = dy / 100.0
    roe = _f(info.get("returnOnEquity"))
    eps = _f(info.get("trailingEps") or info.get("earningsPerShare"))
    bvps = _f(info.get("bookValue"))

    total_debt = _f(info.get("totalDebt"))
    total_cash = _f(info.get("totalCash"))
    ebitda = _f(info.get("ebitda"))
    net_debt_ebitda = None
    if total_debt is not None and ebitda and ebitda > 0:
        net_debt = total_debt - (total_cash or 0.0)
        net_debt_ebitda = net_debt / ebitda

    streak = compute_dividend_streak_years(divs)

    reit_fields = {"ffo_per_share": None, "interest_coverage": None, "debt_to_assets": None}
    if tk is not None:
        try:
            shares = _f(info.get("sharesOutstanding"))
            reit_fields = extract_reit_metrics(
                getattr(tk, "cashflow", None),
                getattr(tk, "financials", None),
                getattr(tk, "balance_sheet", None),
                shares,
            )
        except Exception as e:  # noqa: BLE001
            _log({"event": "yf_us_reit_metrics_error", "err": str(e)[:120]})

    return {
        "eps": eps,
        "bvps": bvps,
        "roe": roe,
        "pe": pe,
        "pb": pb,
        "dy": dy,
        "net_debt_ebitda": net_debt_ebitda,
        "dividend_streak_years": streak,
        "is_aristocrat": None,
        **reit_fields,
    }


def upsert_fundamentals(conn: sqlite3.Connection, ticker: str, fields: dict) -> str:
    period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO fundamentals
             (ticker, period_end, eps, bvps, roe, pe, pb, dy,
              net_debt_ebitda, dividend_streak_years, is_aristocrat,
              ffo_per_share, interest_coverage, debt_to_assets)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             eps=excluded.eps, bvps=excluded.bvps, roe=excluded.roe,
             pe=excluded.pe, pb=excluded.pb, dy=excluded.dy,
             net_debt_ebitda=excluded.net_debt_ebitda,
             dividend_streak_years=excluded.dividend_streak_years,
             is_aristocrat=COALESCE(excluded.is_aristocrat, fundamentals.is_aristocrat),
             ffo_per_share=excluded.ffo_per_share,
             interest_coverage=excluded.interest_coverage,
             debt_to_assets=excluded.debt_to_assets""",
        (ticker, period,
         fields["eps"], fields["bvps"], fields["roe"],
         fields["pe"], fields["pb"], fields["dy"],
         fields["net_debt_ebitda"], fields["dividend_streak_years"],
         fields["is_aristocrat"],
         fields.get("ffo_per_share"), fields.get("interest_coverage"),
         fields.get("debt_to_assets")),
    )
    return period


def run(ticker: str, period: str = "5y") -> dict:
    ticker = ticker.upper()
    entry = load_us_entry(ticker)
    if entry is None:
        # fallback: cria entry mínima; o fetcher é tolerante a tickers novos.
        entry = {"ticker": ticker, "name": ticker, "is_holding": False}

    _log({"event": "yf_us_fetch_start", "ticker": ticker, "period": period})
    tk = yf.Ticker(ticker)
    hist = tk.history(period=period, auto_adjust=False)
    try:
        divs = tk.dividends
    except Exception as e:  # noqa: BLE001
        _log({"event": "yf_us_dividends_error", "ticker": ticker, "err": str(e)[:100]})
        divs = None
    try:
        info = tk.info or {}
    except Exception as e:  # noqa: BLE001
        _log({"event": "yf_us_info_error", "ticker": ticker, "err": str(e)[:100]})
        info = {}

    if hist is None or len(hist) == 0:
        _log({"event": "yf_us_empty_history", "ticker": ticker})
        return {"ticker": ticker, "prices": 0, "dividends": 0, "fundamentals": None}

    fields = extract_fundamentals(info, divs, tk=tk)

    with sqlite3.connect(DB_PATH) as conn:
        upsert_company(conn, entry)
        n_prices = upsert_prices(conn, ticker, hist)
        n_divs = upsert_dividends(conn, ticker, divs)
        period_end = upsert_fundamentals(conn, ticker, fields)
        conn.commit()

    result = {
        "ticker": ticker,
        "prices": n_prices,
        "dividends": n_divs,
        "period_end": period_end,
        "fundamentals": fields,
    }
    _log({"event": "yf_us_persisted", **{k: v for k, v in result.items() if k != "fundamentals"},
          "pe": fields["pe"], "pb": fields["pb"], "dy": fields["dy"],
          "roe": fields["roe"], "streak": fields["dividend_streak_years"]})
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="JNJ")
    ap.add_argument("--period", default="5y")
    args = ap.parse_args()
    run(args.ticker, period=args.period)


if __name__ == "__main__":
    main()
