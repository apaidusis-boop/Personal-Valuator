"""Backtest: regime overlay vs buy-and-hold.

Hipótese a validar (Phase H): usar o classificador de regime (analytics/regime.py)
como filtro de timing adiciona alpha? Especificamente, ir a cash durante fases
de late_cycle/recession preserva capital sem sacrificar o upside.

Metodologia (ano-a-ano, zero look-ahead):
  1. Para cada anchor Dec-31 do ano T em [start, end-1]:
     a. Classifica o regime a essa data usando analytics.regime.classify(as_of=...)
        — o classifier já foi refactorado p/ aceitar as_of.
     b. Define universe = tickers elegíveis (dividendos + prices) desde T-min_history.
     c. Computa EW forward 1y return (média de total return de cada ticker).
     d. Baseline  : portfolio sempre em EW universe (alpha target).
     e. Overlay   : em cash (taxa rf = FEDFUNDS ou SELIC no anchor) quando regime
                    ∈ {late_cycle, recession}; caso contrário em EW universe.
  2. Summary: CAGR baseline vs overlay, hit-rate (anos em que overlay > baseline),
     volatilidade, drawdown máximo.

Zero rede. Só DB local.

CLI:
    python -m analytics.backtest_regime --market us --start 2005
    python -m analytics.backtest_regime --market br --start 2010 --rf-mode flat --rf-rate 0.05
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# regimes em que o overlay vai a cash
RISK_OFF_REGIMES = {"late_cycle", "recession"}


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


# --- reusa helpers mínimos de data (sem depender do outro módulo) -----------

def _eligible_tickers(conn: sqlite3.Connection, earliest_iso: str) -> list[str]:
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


def _total_return_1y(conn: sqlite3.Connection, ticker: str, start_iso: str) -> float | None:
    p0 = _price_at_or_before(conn, ticker, start_iso)
    end_dt = (date.fromisoformat(start_iso) + timedelta(days=365)).isoformat()
    p1 = _price_at_or_before(conn, ticker, end_dt)
    if not p0 or not p1 or p0 <= 0:
        return None
    divs = _div_sum_between(conn, ticker, start_iso, end_dt)
    return (p1 + divs) / p0 - 1


def _risk_free_rate_at(conn: sqlite3.Connection, market: str, anchor_iso: str) -> float:
    """Taxa livre-de-risco anualizada em anchor_iso. Fallback 0%."""
    series_id = "FRED_FEDFUNDS" if market == "us" else "SELIC_META"
    r = conn.execute(
        "SELECT value FROM series WHERE series_id=? AND date<=? ORDER BY date DESC LIMIT 1",
        (series_id, anchor_iso),
    ).fetchone()
    if r and r[0] is not None:
        # valores já vêm em % anualizado (FEDFUNDS, SELIC_META)
        return float(r[0]) / 100.0
    return 0.0


# --- core ------------------------------------------------------------------

@dataclass
class YearResult:
    year: int
    anchor: str
    regime: str
    regime_confidence: str
    n_universe: int
    ew_return: float | None           # buy-and-hold EW (baseline)
    rf_rate: float                    # taxa de cash usada se risk-off
    overlay_return: float | None      # overlay: ew_return se risk_on, rf_rate se risk_off
    risk_off: bool


def run_backtest(market: str, *, start_year: int, end_year: int,
                 min_history_years: int = 10,
                 custom_risk_off: set[str] | None = None) -> list[YearResult]:
    """Corre o backtest. Usa classify(as_of=...) do analytics.regime."""
    from analytics.regime import classify
    risk_off = custom_risk_off or RISK_OFF_REGIMES
    out: list[YearResult] = []
    with sqlite3.connect(_db(market)) as conn:
        for year in range(start_year, end_year):
            anchor = f"{year}-12-31"
            earliest = f"{year - min_history_years}-01-01"
            universe = _eligible_tickers(conn, earliest)
            if len(universe) < 3:
                out.append(YearResult(
                    year=year, anchor=anchor, regime="insufficient_universe",
                    regime_confidence="-", n_universe=len(universe),
                    ew_return=None, rf_rate=0.0, overlay_return=None, risk_off=False,
                ))
                continue

            rets = [_total_return_1y(conn, t, anchor) for t in universe]
            rets = [r for r in rets if r is not None]
            ew = mean(rets) if rets else None

            # classifica regime no anchor
            reg = classify(market, as_of=anchor)
            rf = _risk_free_rate_at(conn, market, anchor)
            in_risk_off = reg.regime in risk_off
            overlay = rf if in_risk_off else ew

            out.append(YearResult(
                year=year, anchor=anchor, regime=reg.regime,
                regime_confidence=reg.confidence, n_universe=len(rets),
                ew_return=ew, rf_rate=rf, overlay_return=overlay,
                risk_off=in_risk_off,
            ))
    return out


# --- summary & print -------------------------------------------------------

def _cagr(returns: Iterable[float]) -> float | None:
    rs = [r for r in returns if r is not None]
    if not rs:
        return None
    acc = 1.0
    for r in rs:
        acc *= (1 + r)
    return acc ** (1 / len(rs)) - 1


def _max_drawdown(returns: Iterable[float]) -> float:
    """MDD como % de peak-to-trough num cumulative compounding."""
    rs = [r for r in returns if r is not None]
    if not rs:
        return 0.0
    curve = [1.0]
    for r in rs:
        curve.append(curve[-1] * (1 + r))
    peak = curve[0]
    mdd = 0.0
    for v in curve:
        if v > peak:
            peak = v
        dd = (v / peak) - 1
        if dd < mdd:
            mdd = dd
    return mdd


def summarize(results: list[YearResult]) -> dict:
    valid = [r for r in results if r.ew_return is not None and r.overlay_return is not None]
    if not valid:
        return {"n_years": 0}
    baseline_rets = [r.ew_return for r in valid]
    overlay_rets = [r.overlay_return for r in valid]
    excess = [o - b for o, b in zip(overlay_rets, baseline_rets)]
    n_risk_off = sum(1 for r in valid if r.risk_off)
    return {
        "n_years": len(valid),
        "n_risk_off_years": n_risk_off,
        "baseline_cagr": _cagr(baseline_rets),
        "overlay_cagr": _cagr(overlay_rets),
        "cagr_edge": _cagr(overlay_rets) - _cagr(baseline_rets),
        "baseline_mdd": _max_drawdown(baseline_rets),
        "overlay_mdd": _max_drawdown(overlay_rets),
        "baseline_stdev": stdev(baseline_rets) if len(baseline_rets) > 1 else 0,
        "overlay_stdev": stdev(overlay_rets) if len(overlay_rets) > 1 else 0,
        "mean_excess": mean(excess) if excess else 0,
        "hit_rate_overlay_beats": sum(1 for e in excess if e > 0) / len(excess),
    }


def _print(market: str, results: list[YearResult], summary: dict) -> None:
    print(f"\nBACKTEST regime overlay  market={market.upper()}  rule='cash when regime in {RISK_OFF_REGIMES}'")
    print("=" * 100)
    print(f"{'YEAR':<6}{'REGIME':<13}{'CONF':<7}{'RF%':>6}  {'EW_ret':>9}  {'OVRLY_ret':>10}  {'EDGE':>9}  {'N':>4}")
    print("-" * 100)
    for r in results:
        ew = f"{r.ew_return*100:+.2f}%" if r.ew_return is not None else "    —"
        ov = f"{r.overlay_return*100:+.2f}%" if r.overlay_return is not None else "    —"
        edge = (r.overlay_return - r.ew_return) if (r.ew_return is not None and r.overlay_return is not None) else None
        edge_s = f"{edge*100:+.2f}%" if edge is not None else "    —"
        tag = " *" if r.risk_off else "  "
        print(f"{r.year:<6}{r.regime:<13}{r.regime_confidence:<7}{r.rf_rate*100:>5.2f}{tag}{ew:>9}  {ov:>10}  {edge_s:>9}  {r.n_universe:>4}")
    print("-" * 100)
    if summary.get("n_years"):
        print(f"\nSUMMARY ({summary['n_years']} anos, {summary['n_risk_off_years']} risk-off):")
        print(f"  CAGR baseline (always in EW): {summary['baseline_cagr']*100:+.2f}%/y")
        print(f"  CAGR overlay  (cash on risk-off): {summary['overlay_cagr']*100:+.2f}%/y")
        print(f"  EDGE (overlay - baseline):        {summary['cagr_edge']*100:+.2f}%/y")
        print(f"  MDD baseline: {summary['baseline_mdd']*100:+.2f}%   MDD overlay: {summary['overlay_mdd']*100:+.2f}%")
        print(f"  Vol baseline: {summary['baseline_stdev']*100:.2f}%   Vol overlay: {summary['overlay_stdev']*100:.2f}%")
        print(f"  Mean excess: {summary['mean_excess']*100:+.2f}%  Hit rate (overlay > baseline): {summary['hit_rate_overlay_beats']*100:.0f}%")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--start", type=int, default=2005)
    ap.add_argument("--end", type=int, default=date.today().year)
    ap.add_argument("--min-history-years", type=int, default=10)
    ap.add_argument("--risk-off", default=",".join(sorted(RISK_OFF_REGIMES)),
                    help="Regimes em que o overlay vai a cash (CSV)")
    args = ap.parse_args()

    custom = set(args.risk_off.split(",")) if args.risk_off else None
    results = run_backtest(
        args.market,
        start_year=args.start, end_year=args.end,
        min_history_years=args.min_history_years,
        custom_risk_off=custom,
    )
    summary = summarize(results)
    _print(args.market, results, summary)


if __name__ == "__main__":
    main()
