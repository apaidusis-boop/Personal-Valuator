"""Métricas computadas a partir da DB — sem tocar na rede.

Agrupa derivações que a MegaWatchlist consome:

  - drawdown_52w     — % abaixo do high de 52 semanas
  - drawdown_5y      — % abaixo do máximo em 5 anos
  - ytd_return       — retorno desde 1 Jan do ano corrente (só preço, sem divs)
  - yoy_return       — retorno últimos 365 dias (só preço)
  - dy_5y_avg        — média do DY anual observado últimos 5 anos
  - div_cagr_5y      — CAGR da soma anual de dividendos últimos 5y
  - div_frequency    — quarterly / semiannual / annual / irregular / none
  - pe_vs_own_avg    — P/E actual comparado com média dos snapshots próprios

Todas funções: (conn, ticker) → float | None | dataclass.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# price-derived
# ---------------------------------------------------------------------------

def _latest_close(conn: sqlite3.Connection, ticker: str) -> tuple[str, float] | None:
    r = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return (r[0], r[1]) if r and r[1] else None


def drawdown_52w(conn: sqlite3.Connection, ticker: str) -> float | None:
    """% abaixo do máximo nos últimos 365 dias. Negativo (-25.0 = -25%)."""
    latest = _latest_close(conn, ticker)
    if not latest:
        return None
    end_date, close = latest
    start_iso = (date.fromisoformat(end_date) - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT MAX(close) FROM prices WHERE ticker=? AND date>=? AND date<=?",
        (ticker, start_iso, end_date),
    ).fetchone()
    high = r[0] if r and r[0] else None
    if not high or high <= 0:
        return None
    return 100.0 * (close - high) / high


def drawdown_5y(conn: sqlite3.Connection, ticker: str) -> float | None:
    latest = _latest_close(conn, ticker)
    if not latest:
        return None
    end_date, close = latest
    start_iso = (date.fromisoformat(end_date) - timedelta(days=365 * 5)).isoformat()
    r = conn.execute(
        "SELECT MAX(close) FROM prices WHERE ticker=? AND date>=? AND date<=?",
        (ticker, start_iso, end_date),
    ).fetchone()
    high = r[0] if r and r[0] else None
    if not high or high <= 0:
        return None
    return 100.0 * (close - high) / high


def ytd_return(conn: sqlite3.Connection, ticker: str) -> float | None:
    """% de variação do preço desde o 1º preço do ano corrente."""
    latest = _latest_close(conn, ticker)
    if not latest:
        return None
    end_date, close = latest
    year_start = date.fromisoformat(end_date).replace(month=1, day=1).isoformat()
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date>=? ORDER BY date ASC LIMIT 1",
        (ticker, year_start),
    ).fetchone()
    p0 = r[0] if r and r[0] else None
    if not p0 or p0 <= 0:
        return None
    return 100.0 * (close - p0) / p0


def yoy_return(conn: sqlite3.Connection, ticker: str) -> float | None:
    """% preço últimos 365 dias (não-total-return, só capital)."""
    latest = _latest_close(conn, ticker)
    if not latest:
        return None
    end_date, close = latest
    ref = (date.fromisoformat(end_date) - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, ref),
    ).fetchone()
    p0 = r[0] if r and r[0] else None
    if not p0 or p0 <= 0:
        return None
    return 100.0 * (close - p0) / p0


# ---------------------------------------------------------------------------
# dividend-derived
# ---------------------------------------------------------------------------

def _annual_dividends(
    conn: sqlite3.Connection, ticker: str, years: int
) -> list[tuple[int, float]]:
    """Lista [(year, total_amount)] dos últimos N anos completos (inclui ano corrente parcial)."""
    r = conn.execute(
        "SELECT MAX(ex_date) FROM dividends WHERE ticker=? AND amount>0",
        (ticker,),
    ).fetchone()
    if not r or not r[0]:
        return []
    end = date.fromisoformat(r[0])
    start_year = end.year - years
    rows = conn.execute(
        """SELECT substr(ex_date, 1, 4) AS y, SUM(amount)
           FROM dividends WHERE ticker=? AND amount>0
             AND substr(ex_date, 1, 4) >= ?
           GROUP BY y ORDER BY y ASC""",
        (ticker, str(start_year)),
    ).fetchall()
    return [(int(y), float(tot)) for y, tot in rows if y]


def dy_5y_avg(conn: sqlite3.Connection, ticker: str) -> float | None:
    """Média do (dividendos anuais / preço médio anual) últimos 5 anos completos.
    Usa dividendos soma-anual e preço de fim de ano."""
    hist = _annual_dividends(conn, ticker, 6)  # 6 para descartar ano corrente parcial
    if len(hist) < 3:
        return None
    today_year = date.today().year
    full_years = [(y, tot) for y, tot in hist if y < today_year][-5:]
    if not full_years:
        return None
    dys = []
    for y, tot in full_years:
        r = conn.execute(
            "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
            (ticker, f"{y}-12-31"),
        ).fetchone()
        px = r[0] if r and r[0] else None
        if px and px > 0 and tot > 0:
            dys.append(100.0 * tot / px)
    return sum(dys) / len(dys) if dys else None


def _annual_regular_dividends(
    conn: sqlite3.Connection, ticker: str, years: int
) -> list[tuple[int, float]]:
    """Como _annual_dividends mas exclui special dividends.
    Heurística: payment individual > 2× mediana do ano é considerado special
    e descartado. Preserva sum normal quarterly/annual.
    Evita distorções tipo TROW 2021 ($3.00 special + 4 × $1.08 regulares)."""
    r = conn.execute(
        "SELECT MAX(ex_date) FROM dividends WHERE ticker=? AND amount>0",
        (ticker,),
    ).fetchone()
    if not r or not r[0]:
        return []
    end = date.fromisoformat(r[0])
    start_year = end.year - years
    rows = conn.execute(
        """SELECT substr(ex_date,1,4) y, amount
           FROM dividends WHERE ticker=? AND amount>0
             AND substr(ex_date,1,4) >= ?
           ORDER BY ex_date""",
        (ticker, str(start_year)),
    ).fetchall()
    by_year: dict[int, list[float]] = {}
    for y, a in rows:
        if not y:
            continue
        by_year.setdefault(int(y), []).append(float(a))
    out = []
    for y in sorted(by_year):
        amounts = by_year[y]
        if len(amounts) <= 1:
            out.append((y, sum(amounts)))
            continue
        sorted_a = sorted(amounts)
        median = sorted_a[len(sorted_a) // 2]
        regular = [a for a in amounts if a <= 2.0 * median]  # exclui outliers >2× mediana
        out.append((y, sum(regular) if regular else sum(amounts)))
    return out


def div_cagr_5y(conn: sqlite3.Connection, ticker: str) -> float | None:
    """CAGR dos dividendos regulares (excluindo specials) nos últimos 5 anos.
    Retorna percentagem (ex: 5.3 = +5.3%/ano)."""
    hist = _annual_regular_dividends(conn, ticker, 6)
    today_year = date.today().year
    full_years = [(y, tot) for y, tot in hist if y < today_year and tot > 0]
    if len(full_years) < 3:
        return None
    full_years = full_years[-5:]
    y0, v0 = full_years[0]
    y1, v1 = full_years[-1]
    n = y1 - y0
    if n <= 0 or v0 <= 0 or v1 <= 0:
        return None
    return 100.0 * ((v1 / v0) ** (1.0 / n) - 1.0)


def div_frequency(conn: sqlite3.Connection, ticker: str) -> str:
    """Classifica regularidade: quarterly|semiannual|annual|irregular|none.
    Usa últimos 3 anos completos."""
    hist = _annual_dividends(conn, ticker, 4)
    today_year = date.today().year
    full_years = [(y, tot) for y, tot in hist if y < today_year][-3:]
    if not full_years:
        return "none"
    # contar eventos por ano (não soma)
    counts = []
    for y, _ in full_years:
        n = conn.execute(
            "SELECT COUNT(*) FROM dividends WHERE ticker=? AND amount>0 AND substr(ex_date,1,4)=?",
            (ticker, str(y)),
        ).fetchone()[0]
        counts.append(n)
    if not counts:
        return "none"
    avg = sum(counts) / len(counts)
    # tolerância: rejeita se desvio for grande
    spread = max(counts) - min(counts)
    if spread > 2:
        return "irregular"
    if avg >= 3.5:
        return "quarterly"
    if avg >= 1.5:
        return "semiannual"
    if avg >= 0.7:
        return "annual"
    return "irregular"


# ---------------------------------------------------------------------------
# fundamentals-derived
# ---------------------------------------------------------------------------

def pe_vs_own_avg(
    conn: sqlite3.Connection, ticker: str, min_obs: int = 20
) -> float | None:
    """% actual vs média histórica dos snapshots de P/E.
    Exige >= min_obs snapshots. Negativo = actualmente abaixo da média (cheap)."""
    rows = conn.execute(
        "SELECT pe FROM fundamentals WHERE ticker=? AND pe>0 ORDER BY period_end ASC",
        (ticker,),
    ).fetchall()
    vals = [r[0] for r in rows if r and r[0]]
    if len(vals) < min_obs:
        return None
    pe_now = vals[-1]
    hist_avg = sum(vals[:-1]) / len(vals[:-1])
    if hist_avg <= 0:
        return None
    return 100.0 * (pe_now - hist_avg) / hist_avg


# ---------------------------------------------------------------------------
# aggregator — um dict completo por ticker
# ---------------------------------------------------------------------------

@dataclass
class TickerMetrics:
    ticker: str
    drawdown_52w: float | None
    drawdown_5y: float | None
    ytd: float | None
    yoy: float | None
    dy_5y_avg_pct: float | None
    div_cagr_5y_pct: float | None
    div_frequency: str
    pe_vs_own_avg_pct: float | None


def compute_all(conn: sqlite3.Connection, ticker: str) -> TickerMetrics:
    return TickerMetrics(
        ticker=ticker,
        drawdown_52w=drawdown_52w(conn, ticker),
        drawdown_5y=drawdown_5y(conn, ticker),
        ytd=ytd_return(conn, ticker),
        yoy=yoy_return(conn, ticker),
        dy_5y_avg_pct=dy_5y_avg(conn, ticker),
        div_cagr_5y_pct=div_cagr_5y(conn, ticker),
        div_frequency=div_frequency(conn, ticker),
        pe_vs_own_avg_pct=pe_vs_own_avg(conn, ticker),
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"], default="us")
    args = ap.parse_args()
    db = ROOT / "data" / f"{args.market}_investments.db"
    with sqlite3.connect(db) as c:
        m = compute_all(c, args.ticker.upper())
    print(f"\n=== metrics {args.ticker.upper()} ({args.market}) ===")
    for field_name, v in m.__dict__.items():
        if field_name == "ticker":
            continue
        if isinstance(v, float):
            print(f"  {field_name:22s}  {v:+.2f}")
        else:
            print(f"  {field_name:22s}  {v}")
