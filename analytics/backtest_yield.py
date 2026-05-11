"""Backtest: "compra ao DY percentile alto vs comprar tudo equal-weight".

Valida empiricamente o sinal que os triggers usam (dy_percentile_vs_own_history):
se historicamente este sinal picked winners, ganhamos confiança; se não,
repensamos a tese.

Metodologia (ano-a-ano):
  1. Para cada ano T de start_year a end_year-1:
     a. Para cada ticker elegível (dividend history desde antes de T-10):
        - Computa DY trailing-12m no fim de Dezembro de T
        - Computa percentile do DY actual vs próprio histórico até T
          (apenas dados disponíveis NAQUELE momento, sem look-ahead bias)
     b. Constrói duas carteiras de 1 ano:
        - HIGH_PCTL  : top N tickers por DY percentile (actual no P75+)
        - EQUAL_WT   : todos os tickers elegíveis igual peso
     c. Forward 1y total return de cada carteira (inclui divs recebidos + reinvest)
  2. Agregados: CAGR, hit rate (anos em que HIGH bate EW), excess return médio.

Zero rede. Apenas prices + dividends.

CLI:
    python -m analytics.backtest_yield --market us
    python -m analytics.backtest_yield --market us --top-n 5 --start 2012
    python -m analytics.backtest_yield --market br --top-n 3
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


# --- helpers de dados -------------------------------------------------------

def _eligible_tickers(conn: sqlite3.Connection, earliest_iso: str) -> list[str]:
    """Tickers com dividendos e prices desde antes de earliest_iso.

    earliest_iso é a data máxima permitida para o primeiro datapoint — i.e. o
    ticker tem de já existir e pagar dividendos nessa altura para ser elegível.
    """
    div_ok = {r[0] for r in conn.execute(
        "SELECT ticker FROM dividends GROUP BY ticker HAVING MIN(ex_date) <= ?",
        (earliest_iso,),
    ).fetchall()}
    px_ok = {r[0] for r in conn.execute(
        "SELECT ticker FROM prices GROUP BY ticker HAVING MIN(date) <= ?",
        (earliest_iso,),
    ).fetchall()}
    return sorted(div_ok & px_ok)


def _price_at_or_before(conn: sqlite3.Connection, ticker: str, iso: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, iso),
    ).fetchone()
    return r[0] if r and r[0] else None


def _div_sum_between(conn: sqlite3.Connection, ticker: str, start: str, end: str) -> float:
    r = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM dividends "
        "WHERE ticker=? AND ex_date>? AND ex_date<=? AND amount>0",
        (ticker, start, end),
    ).fetchone()
    return float(r[0] or 0.0)


def _dy_at(conn: sqlite3.Connection, ticker: str, anchor: str) -> float | None:
    """DY t12m no ponto anchor (iso date)."""
    px = _price_at_or_before(conn, ticker, anchor)
    if not px or px <= 0:
        return None
    since = (date.fromisoformat(anchor) - timedelta(days=365)).isoformat()
    dv = _div_sum_between(conn, ticker, since, anchor)
    if dv <= 0:
        return None
    return 100.0 * dv / px


def _dy_history_until(conn: sqlite3.Connection, ticker: str, end_iso: str,
                      lookback_years: int = 10) -> list[float]:
    """Série mensal de DY t12m, usando dados até end_iso (sem look-ahead).
    Devolve valores em %."""
    end_dt = date.fromisoformat(end_iso)
    start_dt = date(max(1970, end_dt.year - lookback_years), end_dt.month, 1)
    cur = start_dt
    out: list[float] = []
    while cur < end_dt:
        next_m = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)
        month_end = min(next_m - timedelta(days=1), end_dt).isoformat()
        dy = _dy_at(conn, ticker, month_end)
        if dy is not None:
            out.append(dy)
        cur = next_m
    return out


def _percentile_of_last(series: list[float]) -> float | None:
    """Percentile (0-100) do último elemento face aos anteriores."""
    if len(series) < 12:                    # pelo menos 1 ano de mensais
        return None
    current = series[-1]
    prior = series[:-1]
    rank = sum(1 for v in prior if v < current)
    return 100.0 * rank / len(prior)


def _total_return_1y(conn: sqlite3.Connection, ticker: str, start_iso: str) -> float | None:
    """TR 1y aproximado: (P_end + divs pagos no período) / P_start - 1."""
    p0 = _price_at_or_before(conn, ticker, start_iso)
    end_dt = (date.fromisoformat(start_iso) + timedelta(days=365)).isoformat()
    p1 = _price_at_or_before(conn, ticker, end_dt)
    if not p0 or not p1 or p0 <= 0:
        return None
    divs = _div_sum_between(conn, ticker, start_iso, end_dt)
    return (p1 + divs) / p0 - 1


# --- Core --------------------------------------------------------------------

@dataclass
class YearResult:
    year: int
    n_eligible: int
    high_pctl_tickers: list[str]
    high_pctl_return: float | None
    equal_wt_return: float | None
    excess: float | None       # high - equal


def _quality_tickers(conn: sqlite3.Connection, min_score: float = 0.6) -> set[str]:
    """Tickers com score de screen >= min_score na última run.

    min_score default 0.6 = pelo menos 3 de 5 critérios passam. Pragmático:
    passes_screen=1 (todos critérios) é demasiado restritivo (só 1 ticker US).

    Caveat: isto usa o screen ACTUAL (não ponto no tempo) — aproximação
    honesta dado que fundamentals históricos não estão disponíveis.
    Interpretação: filtro de qualidade ex-post atenua o viés do trigger puro.
    """
    rows = conn.execute(
        "SELECT ticker FROM scores WHERE score >= ? AND "
        "run_date=(SELECT MAX(run_date) FROM scores)",
        (min_score,),
    ).fetchall()
    return {r[0] for r in rows}


def run_backtest(market: str, *, start_year: int, end_year: int,
                 top_n: int = 5, min_percentile: float = 75.0,
                 min_history_years: int = 10,
                 quality_only: bool = False,
                 quality_min_score: float = 0.6) -> list[YearResult]:
    out: list[YearResult] = []
    with sqlite3.connect(_db(market)) as conn:
        quality = _quality_tickers(conn, quality_min_score) if quality_only else None
        for year in range(start_year, end_year):
            anchor = f"{year}-12-31"
            # elegibilidade muda a cada ano: ticker precisa ter history até antes de year-min_history
            earliest = f"{year - min_history_years}-01-01"
            universe = _eligible_tickers(conn, earliest)
            if quality is not None:
                universe = [t for t in universe if t in quality]
            candidates: list[tuple[str, float, float]] = []  # (tk, dy, pctl)
            for tk in universe:
                hist = _dy_history_until(conn, tk, anchor, lookback_years=min_history_years)
                pct = _percentile_of_last(hist)
                if pct is None:
                    continue
                candidates.append((tk, hist[-1], pct))
            if len(candidates) < top_n + 2:
                out.append(YearResult(year, len(candidates), [], None, None, None))
                continue

            # HIGH_PCTL: top-N por percentile actual ≥ min_percentile
            ranked = sorted(candidates, key=lambda x: x[2], reverse=True)
            high_picks = [t for t, _, p in ranked if p >= min_percentile][:top_n]
            if len(high_picks) < top_n:
                # fallback: top N por percentile mesmo abaixo do threshold
                high_picks = [t for t, _, _ in ranked[:top_n]]

            high_rets: list[float] = []
            for tk in high_picks:
                r = _total_return_1y(conn, tk, anchor)
                if r is not None:
                    high_rets.append(r)
            ew_rets: list[float] = []
            for tk, _, _ in candidates:
                r = _total_return_1y(conn, tk, anchor)
                if r is not None:
                    ew_rets.append(r)

            high_ret = mean(high_rets) if high_rets else None
            ew_ret = mean(ew_rets) if ew_rets else None
            excess = (high_ret - ew_ret) if (high_ret is not None and ew_ret is not None) else None
            out.append(YearResult(year, len(candidates), high_picks, high_ret, ew_ret, excess))
    return out


# --- Summary & print --------------------------------------------------------

def _cagr(returns: Iterable[float]) -> float | None:
    rs = [r for r in returns if r is not None]
    if not rs:
        return None
    acc = 1.0
    for r in rs:
        acc *= (1 + r)
    return acc ** (1 / len(rs)) - 1


def summarize(results: list[YearResult]) -> dict:
    valid = [r for r in results if r.high_pctl_return is not None and r.equal_wt_return is not None]
    if not valid:
        return {"n_years": 0}
    high_cagr = _cagr(r.high_pctl_return for r in valid)
    ew_cagr = _cagr(r.equal_wt_return for r in valid)
    excesses = [r.excess for r in valid]
    hit_rate = sum(1 for e in excesses if e > 0) / len(excesses)
    return {
        "n_years": len(valid),
        "high_pctl_cagr": high_cagr,
        "equal_wt_cagr": ew_cagr,
        "cagr_edge": high_cagr - ew_cagr if high_cagr is not None and ew_cagr is not None else None,
        "mean_excess": mean(excesses),
        "stdev_excess": stdev(excesses) if len(excesses) > 1 else 0,
        "hit_rate": hit_rate,
    }


def _print(market: str, results: list[YearResult], summary: dict,
           top_n: int, min_pctl: float) -> None:
    print(f"\nBACKTEST  market={market.upper()}  strategy='top-{top_n} DY percentile ≥ {min_pctl:.0f}'")
    print("=" * 88)
    print(f"{'YEAR':<6}{'N':>4} {'PICKS':<36} {'HIGH':>8} {'EW':>8} {'EXCESS':>9}")
    print("-" * 88)
    for r in results:
        picks_str = ",".join(r.high_pctl_tickers[:5])
        if len(picks_str) > 35:
            picks_str = picks_str[:32] + "..."
        hr = f"{r.high_pctl_return*100:+.2f}%" if r.high_pctl_return is not None else "    —"
        ew = f"{r.equal_wt_return*100:+.2f}%" if r.equal_wt_return is not None else "    —"
        ex = f"{r.excess*100:+.2f}%" if r.excess is not None else "    —"
        print(f"{r.year:<6}{r.n_eligible:>4} {picks_str:<36} {hr:>8} {ew:>8} {ex:>9}")
    print("-" * 88)
    if summary.get("n_years"):
        print(f"\nSUMMARY ({summary['n_years']} anos):")
        print(f"  CAGR HIGH_PCTL   : {summary['high_pctl_cagr']*100:+.2f}%/y")
        print(f"  CAGR EQUAL_WT    : {summary['equal_wt_cagr']*100:+.2f}%/y")
        print(f"  EDGE (CAGR diff) : {summary['cagr_edge']*100:+.2f}%/y")
        print(f"  Excess médio/ano : {summary['mean_excess']*100:+.2f}%  (stdev {summary['stdev_excess']*100:.2f}%)")
        print(f"  Hit rate         : {summary['hit_rate']*100:.0f}% dos anos HIGH bate EW")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--start", type=int, default=2012)
    ap.add_argument("--end", type=int, default=date.today().year)
    ap.add_argument("--top-n", type=int, default=5)
    ap.add_argument("--min-percentile", type=float, default=75.0)
    ap.add_argument("--min-history-years", type=int, default=10)
    ap.add_argument("--quality-only", action="store_true",
                    help="Restringe universe a tickers que passam o screen actual")
    ap.add_argument("--quality-min-score", type=float, default=0.6,
                    help="Threshold do screen score p/ quality-only (default 0.6)")
    args = ap.parse_args()

    results = run_backtest(
        args.market,
        start_year=args.start, end_year=args.end,
        top_n=args.top_n, min_percentile=args.min_percentile,
        min_history_years=args.min_history_years,
        quality_only=args.quality_only,
        quality_min_score=args.quality_min_score,
    )
    summary = summarize(results)
    _print(args.market, results, summary, args.top_n, args.min_percentile)


if __name__ == "__main__":
    main()
