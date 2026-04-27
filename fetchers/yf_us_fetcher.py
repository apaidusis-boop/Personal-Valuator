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
from datetime import datetime, timezone
from pathlib import Path

import yaml
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"
KINGS_ARISTOCRATS = ROOT / "config" / "kings_aristocrats.yaml"


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
    if KINGS_ARISTOCRATS.exists():
        ka = yaml.safe_load(KINGS_ARISTOCRATS.read_text(encoding="utf-8")) or {}
        for entry in (ka.get("tickers") or []):
            if entry.get("ticker") == ticker:
                return {
                    "ticker": entry["ticker"],
                    "name": entry.get("name", entry["ticker"]),
                    "sector": entry.get("sector"),
                    "is_holding": entry.get("is_holding", False),
                    "sources": ["kings_aristocrats"],
                    "kind": entry.get("kind"),
                }
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


def _is_suspicious_close(conn: sqlite3.Connection, ticker: str,
                         date_iso: str, close: float) -> bool:
    """Reject obvious data-feed glitches (>50% intraday move with no split).
    Mirrors the BR fetcher guard added 2026-04-27.
    """
    if close <= 0:
        return True
    row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<? "
        "ORDER BY date DESC LIMIT 1", (ticker, date_iso),
    ).fetchone()
    if not row or not row[0] or row[0] <= 0:
        return False
    prev = float(row[0])
    ratio = close / prev
    return ratio < 0.5 or ratio > 2.0


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
        close_f = float(close)
        if _is_suspicious_close(conn, ticker, date, close_f):
            continue
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (ticker, date, close_f,
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


def _ts_to_iso(ts) -> str | None:
    """yfinance devolve timestamps unix ou strings ISO conforme versão.
    Normaliza para 'YYYY-MM-DD' ou None."""
    if ts is None:
        return None
    try:
        if isinstance(ts, (int, float)):
            from datetime import datetime, timezone as _tz
            return datetime.fromtimestamp(float(ts), tz=_tz.utc).strftime("%Y-%m-%d")
        if isinstance(ts, str):
            return ts[:10] if len(ts) >= 10 else None
        if isinstance(ts, (list, tuple)) and ts:
            return _ts_to_iso(ts[0])
    except Exception:
        return None
    return None


def _compute_dy_from_db(conn: sqlite3.Connection, ticker: str, months: int = 12) -> float | None:
    """DY = soma dividendos trailing-N-months / current_price (nossos dados)."""
    px_row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)
    ).fetchone()
    if not px_row or not px_row[0] or px_row[0] <= 0:
        return None
    from datetime import date, timedelta
    since = (date.today() - timedelta(days=int(30.4 * months))).isoformat()
    r = conn.execute(
        "SELECT SUM(amount) FROM dividends WHERE ticker=? AND amount>0 AND ex_date>=?",
        (ticker, since),
    ).fetchone()
    tot = r[0] if r and r[0] else None
    if tot and tot > 0:
        return tot / px_row[0]
    return None


def extract_fundamentals(info: dict, divs, tk=None, conn: sqlite3.Connection = None,
                         ticker: str = None) -> dict:
    """Lê yfinance .info e normaliza para o schema `fundamentals`.
    Se tk (yf.Ticker) for fornecido, inclui métricas REIT (FFO, cobertura).
    Se conn+ticker forem fornecidos, prefere DY computado dos nossos dividendos."""
    pe = _f(info.get("trailingPE"))
    pb = _f(info.get("priceToBook"))
    dy = None
    if conn is not None and ticker:
        dy = _compute_dy_from_db(conn, ticker)
    if dy is None:
        dy = _f(info.get("dividendYield"))
        if dy is not None and dy > 1:
            dy = dy / 100.0
        # sanity: DY > 25% é quase certamente bug yfinance (ex: XP=86%, TSM=96%)
        if dy is not None and dy > 0.25:
            _log({"event": "yf_us_dy_sanity_reject", "ticker": ticker, "raw": dy})
            dy = None
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

    # novos campos (Sessão 1 MegaWatchlist)
    pe_forward = _f(info.get("forwardPE"))
    ev_ebitda = _f(info.get("enterpriseToEbitda"))
    market_cap = _f(info.get("marketCap"))
    fcf_ttm = _f(info.get("freeCashflow"))
    shares_outstanding = _f(info.get("sharesOutstanding"))
    next_ex_date = _ts_to_iso(info.get("exDividendDate"))
    # earningsDate pode ser lista [start,end]; earningsTimestamp é o start
    next_earnings_date = _ts_to_iso(info.get("earningsTimestamp") or info.get("earningsDate"))

    reit_fields = {"ffo_per_share": None, "interest_coverage": None, "debt_to_assets": None}
    if tk is not None:
        try:
            reit_fields = extract_reit_metrics(
                getattr(tk, "cashflow", None),
                getattr(tk, "financials", None),
                getattr(tk, "balance_sheet", None),
                shares_outstanding,
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
        "pe_forward": pe_forward,
        "ev_ebitda": ev_ebitda,
        "market_cap": market_cap,
        "fcf_ttm": fcf_ttm,
        "shares_outstanding": shares_outstanding,
        "next_ex_date": next_ex_date,
        "next_earnings_date": next_earnings_date,
        **reit_fields,
    }


def upsert_fundamentals(conn: sqlite3.Connection, ticker: str, fields: dict) -> str:
    period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO fundamentals
             (ticker, period_end, eps, bvps, roe, pe, pb, dy,
              net_debt_ebitda, dividend_streak_years, is_aristocrat,
              ffo_per_share, interest_coverage, debt_to_assets,
              pe_forward, ev_ebitda, market_cap, fcf_ttm,
              shares_outstanding, next_ex_date, next_earnings_date)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             eps=excluded.eps, bvps=excluded.bvps, roe=excluded.roe,
             pe=excluded.pe, pb=excluded.pb, dy=excluded.dy,
             net_debt_ebitda=excluded.net_debt_ebitda,
             dividend_streak_years=excluded.dividend_streak_years,
             is_aristocrat=COALESCE(excluded.is_aristocrat, fundamentals.is_aristocrat),
             ffo_per_share=excluded.ffo_per_share,
             interest_coverage=excluded.interest_coverage,
             debt_to_assets=excluded.debt_to_assets,
             pe_forward=excluded.pe_forward,
             ev_ebitda=excluded.ev_ebitda,
             market_cap=excluded.market_cap,
             fcf_ttm=excluded.fcf_ttm,
             shares_outstanding=excluded.shares_outstanding,
             next_ex_date=excluded.next_ex_date,
             next_earnings_date=excluded.next_earnings_date""",
        (ticker, period,
         fields["eps"], fields["bvps"], fields["roe"],
         fields["pe"], fields["pb"], fields["dy"],
         fields["net_debt_ebitda"], fields["dividend_streak_years"],
         fields["is_aristocrat"],
         fields.get("ffo_per_share"), fields.get("interest_coverage"),
         fields.get("debt_to_assets"),
         fields.get("pe_forward"), fields.get("ev_ebitda"),
         fields.get("market_cap"), fields.get("fcf_ttm"),
         fields.get("shares_outstanding"),
         fields.get("next_ex_date"), fields.get("next_earnings_date")),
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

    with sqlite3.connect(DB_PATH) as conn:
        upsert_company(conn, entry)
        n_prices = upsert_prices(conn, ticker, hist)
        n_divs = upsert_dividends(conn, ticker, divs)
        # extract precisa de conn para computar DY dos nossos dividendos
        fields = extract_fundamentals(info, divs, tk=tk, conn=conn, ticker=ticker)
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
