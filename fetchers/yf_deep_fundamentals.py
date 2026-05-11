"""Fetcher: yfinance balance sheet + income + cash flow → deep_fundamentals.

Pull-on-demand (não no batch diário). Usado por research.py, Altman e Piotroski
quando o ticker ainda não tem histórico persistido.

yfinance expõe estes DataFrames em Ticker(t):
  .balance_sheet         (annual; colunas = períodos, linhas = contas)
  .financials            (annual income statement)
  .cashflow              (annual cash flow)
  .quarterly_balance_sheet / .quarterly_financials / .quarterly_cashflow

Usa-se o ANUAL por defeito (Altman + Piotroski precisam de 1-2 anos).

CLI:
    python fetchers/yf_deep_fundamentals.py JNJ              # 1 ticker, ambas DBs
    python fetchers/yf_deep_fundamentals.py ITSA4 --market br
    python fetchers/yf_deep_fundamentals.py --holdings       # todos os holdings
"""
from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"

# Mapeamento row-name (yfinance) → coluna DB. yfinance varia rótulos entre
# empresas; incluímos aliases razoáveis. Ordem importa: primeiro hit vence.
BS_MAP: dict[str, list[str]] = {
    "total_assets":          ["Total Assets"],
    "current_assets":        ["Current Assets", "Total Current Assets"],
    "current_liabilities":   ["Current Liabilities", "Total Current Liabilities"],
    "total_liabilities":     ["Total Liabilities Net Minority Interest", "Total Liab"],
    "long_term_debt":        ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"],
    "total_debt":            ["Total Debt"],
    "stockholders_equity":   ["Stockholders Equity", "Common Stock Equity", "Total Stockholder Equity"],
    "retained_earnings":     ["Retained Earnings"],
    "working_capital":       ["Working Capital"],
    "shares_outstanding":    ["Ordinary Shares Number", "Share Issued"],
}
IS_MAP: dict[str, list[str]] = {
    "total_revenue":         ["Total Revenue", "Operating Revenue"],
    "gross_profit":          ["Gross Profit"],
    "ebit":                  ["EBIT", "Operating Income"],
    "net_income":            ["Net Income", "Net Income Common Stockholders"],
    "diluted_avg_shares":    ["Diluted Average Shares", "Basic Average Shares"],
}
CF_MAP: dict[str, list[str]] = {
    "operating_cashflow":    ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"],
    "capital_expenditure":   ["Capital Expenditure"],
    "free_cash_flow":        ["Free Cash Flow"],
}


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / "yf_deep_fundamentals.log"
    logger = logging.getLogger("yf_deep_fundamentals")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    h = logging.FileHandler(log_path, encoding="utf-8")
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(h)
    return logger


def _first_match(df, candidates: list[str], column):
    """Devolve o valor float da primeira row em `candidates` presente em df, ou None."""
    if df is None or df.empty:
        return None
    for name in candidates:
        if name in df.index:
            try:
                v = df.loc[name, column]
                if v is None:
                    continue
                fv = float(v)
                if fv != fv:  # NaN
                    continue
                return fv
            except (KeyError, TypeError, ValueError):
                continue
    return None


def _yf_symbol(ticker: str, market: str) -> str:
    """BR → acrescenta .SA; US → mantém."""
    if market == "br" and not ticker.endswith(".SA"):
        return f"{ticker}.SA"
    return ticker


def fetch_one(ticker: str, market: str, period_type: str = "annual") -> list[dict]:
    """Busca fundamentos e devolve lista de dicts (um por período).

    Não escreve na DB — apenas retorna. Caller decide persistência.
    """
    sym = _yf_symbol(ticker, market)
    t = yf.Ticker(sym)

    if period_type == "annual":
        bs = t.balance_sheet
        inc = t.financials
        cf = t.cashflow
    else:
        bs = t.quarterly_balance_sheet
        inc = t.quarterly_financials
        cf = t.quarterly_cashflow

    # Union of all period columns across the three DFs
    periods = set()
    for df in (bs, inc, cf):
        if df is not None and not df.empty:
            periods.update(df.columns)
    periods = sorted(periods, reverse=True)[:5]  # top-5 mais recentes

    market_cap = None
    try:
        info = t.info
        market_cap = info.get("marketCap")
    except Exception:
        pass

    rows = []
    for i, p in enumerate(periods):
        row = {
            "ticker": ticker,
            "period_end": p.date().isoformat() if hasattr(p, "date") else str(p)[:10],
            "period_type": period_type,
        }
        for col, aliases in BS_MAP.items():
            row[col] = _first_match(bs, aliases, p)
        for col, aliases in IS_MAP.items():
            row[col] = _first_match(inc, aliases, p)
        for col, aliases in CF_MAP.items():
            row[col] = _first_match(cf, aliases, p)
        # derived: working capital se não veio explícito
        if row.get("working_capital") is None:
            ca, cl = row.get("current_assets"), row.get("current_liabilities")
            if ca is not None and cl is not None:
                row["working_capital"] = ca - cl
        # derived: FCF se não veio explícito
        if row.get("free_cash_flow") is None:
            ocf, capex = row.get("operating_cashflow"), row.get("capital_expenditure")
            if ocf is not None and capex is not None:
                # capex em yfinance vem negativo → FCF = OCF + capex
                row["free_cash_flow"] = ocf + capex
        # market_cap só na row mais recente
        row["market_cap_at_fetch"] = market_cap if i == 0 else None
        row["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        row["source"] = "yfinance"
        rows.append(row)
    return rows


def persist(conn: sqlite3.Connection, rows: list[dict]) -> int:
    """UPSERT nas rows. Devolve nº de rows afectadas."""
    if not rows:
        return 0
    cols = list(rows[0].keys())
    placeholders = ",".join("?" * len(cols))
    col_list = ",".join(cols)
    updates = ",".join(f"{c}=excluded.{c}" for c in cols if c not in ("ticker", "period_end", "period_type"))
    sql = (
        f"INSERT INTO deep_fundamentals ({col_list}) VALUES ({placeholders}) "
        f"ON CONFLICT(ticker, period_end, period_type) DO UPDATE SET {updates}"
    )
    n = 0
    for r in rows:
        conn.execute(sql, [r[c] for c in cols])
        n += 1
    conn.commit()
    return n


def fetch_and_persist(ticker: str, market: str, period_type: str = "annual") -> int:
    """Conveniência: fetch + persist numa só chamada. Devolve nº de rows escritas."""
    logger = _setup_logging()
    db = DB_BR if market == "br" else DB_US
    try:
        rows = fetch_one(ticker, market, period_type)
        with sqlite3.connect(db) as conn:
            n = persist(conn, rows)
        logger.info(f"OK {ticker} ({market}) — {n} rows persistidas")
        return n
    except Exception as e:
        logger.error(f"FAIL {ticker} ({market}) — {type(e).__name__}: {e}")
        logger.debug(traceback.format_exc())
        return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", help="Tickers para fetch (ex: JNJ ITSA4)")
    ap.add_argument("--market", choices=["br", "us"], help="Força mercado; senão tenta ambos")
    ap.add_argument("--holdings", action="store_true", help="Fetch todos os holdings activos (ambos mercados)")
    ap.add_argument("--quarterly", action="store_true", help="Quarterly em vez de annual")
    args = ap.parse_args()

    period_type = "quarterly" if args.quarterly else "annual"
    targets: list[tuple[str, str]] = []

    if args.holdings:
        for mk, db in [("br", DB_BR), ("us", DB_US)]:
            with sqlite3.connect(db) as c:
                tks = [r[0] for r in c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1 AND quantity>0"
                ).fetchall()]
            for t in tks:
                targets.append((t, mk))
    else:
        if not args.tickers:
            ap.error("passa tickers ou --holdings")
        for t in args.tickers:
            t = t.upper()
            if args.market:
                targets.append((t, args.market))
            else:
                # auto-detecta: procura o ticker em ambas as DBs
                found = False
                for mk, db in [("br", DB_BR), ("us", DB_US)]:
                    with sqlite3.connect(db) as c:
                        r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (t,)).fetchone()
                    if r:
                        targets.append((t, mk))
                        found = True
                        break
                if not found:
                    print(f"[warn] {t}: não encontrado em nenhuma DB, pulando.")

    print(f"Fetching deep fundamentals ({period_type}) para {len(targets)} ticker(s)...")
    ok = bad = 0
    for t, mk in targets:
        n = fetch_and_persist(t, mk, period_type)
        if n > 0:
            ok += 1
            print(f"  ✓ {t:<8} ({mk})  {n} periods")
        else:
            bad += 1
            print(f"  ✗ {t:<8} ({mk})  FAIL")
    print(f"\nDone: {ok} OK, {bad} bad")


if __name__ == "__main__":
    main()
