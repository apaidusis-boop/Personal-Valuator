"""Backfill TBVPS + ROTCE para bancos US.

Fecha task #7 (gap detectado quando codifiquei score_us_bank em 2026-04-26):
schema us_investments.db.fundamentals não tinha tbvps/rotce/cet1/efficiency,
forçando score_us_bank a usar BVPS/ROE como proxies.

Este script:
  1. ALTER TABLE fundamentals ADD COLUMN tbvps REAL, rotce REAL, cet1_ratio REAL, efficiency_ratio REAL
     (idempotente — ignora "duplicate column name").
  2. Para cada US bank ticker fornecido, fetch annual balance_sheet + financials da yfinance.
     yfinance expõe 'Tangible Book Value' directamente — não precisamos derivar.
     ROTCE = Net Income Common Stockholders / TBV (preferred dividends excluídos).
  3. UPDATE fundamentals SET tbvps=?, rotce=? WHERE ticker=? AND period_end=(MAX).

CET1 e efficiency_ratio ficam NULL — exigem 10-Q XBRL parsing (próxima iteração).

Uso:
    python scripts/backfill_us_bank_tangibles.py                 # default banks
    python scripts/backfill_us_bank_tangibles.py JPM GS TFC      # só estes
    python scripts/backfill_us_bank_tangibles.py --schema-only   # só ALTER
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DB_US = ROOT / "data" / "us_investments.db"

# Default cohort: holdings + Buffett-watched US banks
DEFAULT_BANKS = ["JPM", "GS", "TFC", "BAC", "USB", "WFC"]

NEW_COLS = [
    ("tbvps", "REAL"),
    ("rotce", "REAL"),
    ("cet1_ratio", "REAL"),
    ("efficiency_ratio", "REAL"),
]


def ensure_schema(conn: sqlite3.Connection) -> list[str]:
    """ALTER TABLE — idempotente. Devolve colunas adicionadas nesta corrida."""
    added = []
    for col, typ in NEW_COLS:
        try:
            conn.execute(f"ALTER TABLE fundamentals ADD COLUMN {col} {typ}")
            added.append(col)
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
    conn.commit()
    return added


def _row_value(df, candidates: list[str], col):
    """Devolve o primeiro valor float não-NaN para os candidates."""
    if df is None or df.empty:
        return None
    for name in candidates:
        if name in df.index:
            try:
                v = df.loc[name, col]
                fv = float(v)
                if fv == fv:  # not NaN
                    return fv
            except (KeyError, TypeError, ValueError):
                continue
    return None


def fetch_metrics(ticker: str) -> dict | None:
    """Fetch yfinance annual BS + IS, devolve dict com tbvps + rotce.

    Devolve None se ticker não tem dados ou shares_outstanding/TBV estão em falta.
    """
    t = yf.Ticker(ticker)
    bs = t.balance_sheet
    inc = t.financials
    if bs is None or bs.empty:
        return None

    period = bs.columns[0]  # mais recente
    period_end = period.date().isoformat() if hasattr(period, "date") else str(period)[:10]

    tbv = _row_value(bs, ["Tangible Book Value", "Net Tangible Assets"], period)
    if tbv is None:
        # fallback: derivar de equity - goodwill - intangibles
        equity = _row_value(bs, ["Common Stock Equity", "Stockholders Equity"], period)
        goodwill = _row_value(bs, ["Goodwill"], period) or 0.0
        intang = _row_value(bs, ["Other Intangible Assets"], period) or 0.0
        if equity is not None:
            tbv = equity - goodwill - intang

    shares = _row_value(bs, ["Ordinary Shares Number", "Share Issued"], period)
    if shares is None:
        try:
            info = t.info
            shares = info.get("sharesOutstanding")
        except Exception:
            pass

    tbvps = (tbv / shares) if (tbv is not None and shares) else None

    # ROTCE = NI Common / Tangible Common Equity. Usar TBV período corrente
    # (ideal seria avg de 2 períodos, mas simplificamos — banco é estável).
    ni_common = _row_value(inc, ["Net Income Common Stockholders", "Net Income"], period)
    rotce = (ni_common / tbv) if (ni_common is not None and tbv and tbv > 0) else None

    return {
        "ticker": ticker,
        "period_end": period_end,
        "tbv": tbv,
        "tbvps": tbvps,
        "ni_common": ni_common,
        "rotce": rotce,
        "shares": shares,
    }


def update_fundamentals(conn: sqlite3.Connection, ticker: str, tbvps: float | None,
                        rotce: float | None) -> int:
    """Aplica tbvps/rotce na row mais recente de fundamentals para o ticker.
    yfinance dá metric anual; aplicamos à row "snapshot" mais recente
    (que tem period_end ~= hoje porque o fetcher diário escreve uma snapshot por dia).
    """
    most_recent = conn.execute(
        "SELECT period_end FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if not most_recent:
        return 0
    period = most_recent[0]
    cur = conn.execute(
        "UPDATE fundamentals SET tbvps=?, rotce=? WHERE ticker=? AND period_end=?",
        (tbvps, rotce, ticker, period),
    )
    return cur.rowcount


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tickers", nargs="*", default=DEFAULT_BANKS,
                    help=f"US bank tickers (default: {' '.join(DEFAULT_BANKS)})")
    ap.add_argument("--schema-only", action="store_true",
                    help="só corre ALTER TABLE, não fetcha")
    args = ap.parse_args()

    with sqlite3.connect(DB_US) as conn:
        added = ensure_schema(conn)
        if added:
            print(f"[schema] colunas adicionadas: {', '.join(added)}")
        else:
            print("[schema] já existente — nada a fazer")

        if args.schema_only:
            return

        for tk in args.tickers:
            try:
                m = fetch_metrics(tk)
            except Exception as e:
                print(f"[{tk}] ERRO fetch: {e}", file=sys.stderr)
                continue
            if m is None or m["tbvps"] is None:
                print(f"[{tk}] dados insuficientes (TBV/shares em falta)")
                continue
            n = update_fundamentals(conn, tk, m["tbvps"], m["rotce"])
            tbvps_s = f"${m['tbvps']:.2f}"
            rotce_s = f"{m['rotce']*100:.1f}%" if m["rotce"] is not None else "n/a"
            print(f"[{tk}] period={m['period_end']} TBVPS={tbvps_s} ROTCE={rotce_s} rows_updated={n}")
        conn.commit()


if __name__ == "__main__":
    main()
