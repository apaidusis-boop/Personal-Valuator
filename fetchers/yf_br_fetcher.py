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
COMPOUNDERS = ROOT / "config" / "br_dividend_compounders.yaml"


def _lookup_compounder(ticker: str) -> dict | None:
    if not COMPOUNDERS.exists():
        return None
    try:
        import yaml as _yaml
        data = _yaml.safe_load(COMPOUNDERS.read_text(encoding="utf-8")) or {}
        for e in (data.get("tickers") or []):
            if e.get("ticker") == ticker:
                return e
    except Exception:
        pass
    return None


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


def fetch(ticker: str, period: str = "1y"):
    sym = _yf_symbol(ticker)
    tk = yf.Ticker(sym)
    # auto_adjust=False para preservar Close unadjusted; as colunas Dividends
    # e Stock Splits são os eventos que precisamos para computar TR nós.
    hist = tk.history(period=period, auto_adjust=False)
    divs_series = tk.dividends  # série completa histórica
    return hist, divs_series, tk


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


def _compute_streak(divs) -> int | None:
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


def _compute_dy_from_divs(conn: sqlite3.Connection, ticker: str, current_price: float,
                          months: int = 12) -> float | None:
    """DY = soma dividendos trailing-N-months / current_price.
    Ground truth baseado nos nossos dados, evita bugs yfinance.info."""
    if not current_price or current_price <= 0:
        return None
    from datetime import date, timedelta
    since = (date.today() - timedelta(days=int(30.4 * months))).isoformat()
    r = conn.execute(
        "SELECT SUM(amount) FROM dividends WHERE ticker=? AND amount>0 AND ex_date>=?",
        (ticker, since),
    ).fetchone()
    tot = r[0] if r and r[0] else None
    if tot and tot > 0:
        return tot / current_price
    return None


def upsert_fundamentals_br(conn: sqlite3.Connection, ticker: str, info: dict, divs) -> None:
    """Persiste fundamentals básicos vindos do yfinance.info para ticker BR.
    Serve como fallback/complemento ao brapi_fetcher — especialmente útil
    para compounders recém-adicionados que ainda não foram ao brapi."""
    if not info:
        return
    pe = _f(info.get("trailingPE"))
    pb = _f(info.get("priceToBook"))
    # DY: sempre re-computar dos nossos dividendos vs price actual (evita bugs
    # yfinance.info — ex: ABEV3 retornava 15.59% quando real é ~10%).
    px_row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)
    ).fetchone()
    current_price = px_row[0] if px_row else None
    dy = _compute_dy_from_divs(conn, ticker, current_price)
    if dy is None:  # fallback para yfinance se dividends table vazia
        dy = _f(info.get("dividendYield"))
        if dy is not None and dy > 1:
            dy = dy / 100.0
        if dy is not None and dy > 0.25:
            dy = None
    roe = _f(info.get("returnOnEquity"))
    eps = _f(info.get("trailingEps") or info.get("earningsPerShare"))
    bvps = _f(info.get("bookValue"))
    total_debt = _f(info.get("totalDebt"))
    total_cash = _f(info.get("totalCash"))
    ebitda = _f(info.get("ebitda"))
    nd_ebitda = None
    if total_debt is not None and ebitda and ebitda > 0:
        nd_ebitda = (total_debt - (total_cash or 0.0)) / ebitda
    streak = _compute_streak(divs)
    pe_forward = _f(info.get("forwardPE"))
    ev_ebitda = _f(info.get("enterpriseToEbitda"))
    market_cap = _f(info.get("marketCap"))

    period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO fundamentals
             (ticker, period_end, eps, bvps, roe, pe, pb, dy,
              net_debt_ebitda, dividend_streak_years, is_aristocrat,
              pe_forward, ev_ebitda, market_cap)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             eps=excluded.eps, bvps=excluded.bvps, roe=excluded.roe,
             pe=excluded.pe, pb=excluded.pb, dy=excluded.dy,
             net_debt_ebitda=excluded.net_debt_ebitda,
             dividend_streak_years=excluded.dividend_streak_years,
             pe_forward=excluded.pe_forward,
             ev_ebitda=excluded.ev_ebitda,
             market_cap=excluded.market_cap""",
        (ticker, period, eps, bvps, roe, pe, pb, dy,
         nd_ebitda, streak, None, pe_forward, ev_ebitda, market_cap),
    )


def _is_suspicious_close(conn: sqlite3.Connection, ticker: str,
                         date_iso: str, close: float) -> bool:
    """Reject obviously corrupt prices: >50% drop/jump vs previous close
    when no split is on file. Catches Yahoo glitches like XPML11 Jan 2026
    (close went R$110 → R$1.07 → R$110 over 3 days; no corporate action).
    """
    if close <= 0:
        return True
    row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<? "
        "ORDER BY date DESC LIMIT 1", (ticker, date_iso),
    ).fetchone()
    if not row or not row[0] or row[0] <= 0:
        return False  # no previous close to compare; accept
    prev = float(row[0])
    ratio = close / prev
    # Suspicious if dropped to less than half or jumped to more than double in one session.
    return ratio < 0.5 or ratio > 2.0


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
        close_f = float(close)
        if _is_suspicious_close(conn, ticker, date, close_f):
            # Skip suspect row; do not poison the time series.
            # If it really is a 50%+ legit move, downstream tooling will surface
            # the gap and a manual override can re-insert.
            continue
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET
                 close=excluded.close, volume=excluded.volume""",
            (ticker, date, close_f, int(vol) if vol is not None and vol == vol else None),
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
    hist, divs, tk = fetch(ticker, period=period)

    meta = _lookup_compounder(ticker) or {}
    with sqlite3.connect(DB_PATH) as conn:
        # garantir companies (não falha se já existir; actualiza name/sector
        # se metadata disponível via br_dividend_compounders.yaml)
        conn.execute(
            """INSERT INTO companies (ticker, name, sector, is_holding, currency)
               VALUES (?, ?, ?, 0, 'BRL')
               ON CONFLICT(ticker) DO UPDATE SET
                 name=COALESCE(excluded.name, companies.name),
                 sector=COALESCE(excluded.sector, companies.sector)""",
            (ticker, meta.get("name") or ticker, meta.get("sector")),
        )
        n_prices = upsert_prices(conn, ticker, hist)
        n_divs = upsert_dividends(conn, ticker, divs)
        # fundamentals via yfinance.info (fallback/complemento ao brapi)
        try:
            info = tk.info or {}
            upsert_fundamentals_br(conn, ticker, info, divs)
        except Exception as e:  # noqa: BLE001
            _log({"event": "yf_br_fundamentals_skip", "ticker": ticker, "err": str(e)[:120]})
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
