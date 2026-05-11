"""Decision Quality Engine — Phase FF Bloco 1.1.

Closed-loop validation infra para `verdict_history`. Mede:

  - Outcome (forward return absoluto em N dias após verdict)
  - Benchmark return (SPY US / BOVA11 BR no mesmo intervalo)
  - Sector ETF return (XLK/XLV/... US; sector ETF BR onde existir)
  - Outperformance vs benchmark + vs sector
  - Accuracy direccional. Vocabulário oficial das actions (Phase FF Bloco 3):
      bullish: BUY (not held, score≥7) | ADD (held, score≥7)
      neutral: HOLD (held, mid score)  | WATCH (not held, mid score)
      bearish: AVOID (not held, low)   | SELL (held, low)
      no-op  : SKIP (not held, mid-low; "no opinion" — returns None from _accuracy)
    Hit definitions:
      bullish: return>0; outperformed_benchmark: vs_bench>0
      bearish: return<0; outperformed_benchmark: vs_bench<0
      neutral: |return|<HOLD_BAND_PCT (5%); outperformed: |vs_bench|<HOLD_BAND_VS_BENCH_PCT (2%)
      SKIP   : intentionally None — represents absence of verdict, not a calibratable call

Persiste tudo em `verdict_history` (colunas adicionadas pelo migrate). A diferença
crítica vs `scripts/verdict_history.py::backtest()` (que computava on-the-fly):
guardamos o outcome para análise cumulativa + calibration curve estável.

Calibration curve: bina por `confidence_pct` (0-20, 20-40, ...) e mede mediana
de `return_vs_benchmark`. Idealmente monotónica (mais confidence → mais
outperformance). Se não-monotónica, o score está a medir ruído.

100% local. Pure SQL + filesystem. Zero LLM calls.

Uso:
    python -m analytics.decision_quality update                  # actualiza outcomes em verdicts ≥30d
    python -m analytics.decision_quality update --window 90      # forçar window específico
    python -m analytics.decision_quality calibration --market us # imprime calibration curve
    python -m analytics.decision_quality post-mortem 2026-Q1     # post-mortem trimestral
    python -m analytics.decision_quality engine-attribution      # qual engine arrasta hits
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}

# Benchmark per market
BENCHMARK = {"us": "SPY", "br": "BOVA11"}

# Sector ETF map (US only — BR sector ETFs scarce/illiquid; default a benchmark)
SECTOR_ETF_US = {
    "Technology":             "XLK",
    "Healthcare":             "XLV",
    "Financials":             "XLF",
    "Financial Services":     "XLF",
    "Energy":                 "XLE",
    "Industrials":            "XLI",
    "Consumer Discretionary": "XLY",
    "Consumer Cyclical":      "XLY",
    "Consumer Staples":       "XLP",
    "Consumer Defensive":     "XLP",
    "Materials":              "XLB",
    "Basic Materials":        "XLB",
    "Real Estate":            "XLRE",
    "Utilities":              "XLU",
    "Communication Services": "XLC",
}

# HOLD acceptance band: |return| < this => "correctly held"
HOLD_BAND_PCT = 5.0
HOLD_BAND_VS_BENCH_PCT = 2.0


# ============================================================
# Helpers
# ============================================================
def _price_at_or_after(conn: sqlite3.Connection, ticker: str, target_date: str) -> tuple[str, float] | None:
    """First close price for ticker on or after target_date. Returns (date, close) or None."""
    row = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? AND date>=? ORDER BY date LIMIT 1",
        (ticker, target_date),
    ).fetchone()
    return (row[0], row[1]) if row else None


def _price_on_or_before(conn: sqlite3.Connection, ticker: str, target_date: str) -> tuple[str, float] | None:
    """Last close price for ticker on or before target_date."""
    row = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, target_date),
    ).fetchone()
    return (row[0], row[1]) if row else None


def _pct_return(start: float, end: float) -> float:
    if start <= 0:
        return 0.0
    return (end / start - 1.0) * 100.0


def _sector_etf(conn: sqlite3.Connection, ticker: str, market: str) -> str | None:
    """Resolve sector ETF for a ticker. Returns None if no mapping or BR."""
    if market != "us":
        return None
    row = conn.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
    if not row:
        return None
    return SECTOR_ETF_US.get(row[0])


BULLISH_ACTIONS = frozenset({"BUY", "ADD"})
BEARISH_ACTIONS = frozenset({"AVOID", "SELL"})
NEUTRAL_ACTIONS = frozenset({"HOLD", "WATCH"})
NULL_ACTIONS    = frozenset({"SKIP"})


def _accuracy(action: str, return_pct: float, return_vs_bench_pct: float) -> tuple[int | None, int | None]:
    """Returns (accuracy, outperformed_benchmark) as 0/1/None.

    Action vocabulary aligned com `scripts/verdict.py`:
      BUY, ADD       → bullish (hit if return_pct > 0; outperformed if vs_bench > 0)
      AVOID, SELL    → bearish (hit if return_pct < 0; outperformed if vs_bench < 0)
      HOLD, WATCH    → neutral cautious (hit if |return_pct| < HOLD_BAND_PCT;
                       outperformed if |vs_bench| < HOLD_BAND_VS_BENCH_PCT)
      SKIP           → null (não emite julgamento, fica fora da calibration)
    """
    a = (action or "").upper()
    if a in BULLISH_ACTIONS:
        accuracy = 1 if return_pct > 0 else 0
        outperf = 1 if return_vs_bench_pct > 0 else 0
    elif a in BEARISH_ACTIONS:
        accuracy = 1 if return_pct < 0 else 0
        outperf = 1 if return_vs_bench_pct < 0 else 0
    elif a in NEUTRAL_ACTIONS:
        accuracy = 1 if abs(return_pct) < HOLD_BAND_PCT else 0
        outperf = 1 if abs(return_vs_bench_pct) < HOLD_BAND_VS_BENCH_PCT else 0
    elif a in NULL_ACTIONS:
        return None, None
    else:
        # Unknown action — treat as neutral to avoid false-positive metrics
        accuracy = 1 if abs(return_pct) < HOLD_BAND_PCT else 0
        outperf = 1 if abs(return_vs_bench_pct) < HOLD_BAND_VS_BENCH_PCT else 0
    return accuracy, outperf


# ============================================================
# Update outcomes
# ============================================================
def reset_accuracy(market: str) -> dict[str, Any]:
    """Recomputa `accuracy`/`outperformed_*` para rows já preenchidas, sem
    re-fetch de prices. Necessário depois de mudar o vocabulário em `_accuracy()`.
    """
    db = DBS[market]
    stats = {"updated": 0}
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT ticker, date, action, outcome_return, return_vs_benchmark, return_vs_sector
                 FROM verdict_history WHERE outcome_price IS NOT NULL"""
        ).fetchall()
        for ticker, vdate, action, ret, vs_b, vs_s in rows:
            acc, op_b = _accuracy(action, ret, vs_b if vs_b is not None else 0.0)
            _, op_s = _accuracy(action, ret, vs_s) if vs_s is not None else (None, None)
            conn.execute(
                """UPDATE verdict_history
                      SET accuracy=?, outperformed_benchmark=?, outperformed_sector=?
                    WHERE ticker=? AND date=?""",
                (acc, op_b if vs_b is not None else None, op_s, ticker, vdate),
            )
            stats["updated"] += 1
        conn.commit()
    return stats


def update_outcomes(market: str, window_days: int = 30, dry_run: bool = False) -> dict[str, Any]:
    """Cruza verdicts com idade >= window_days contra forward return + benchmarks.

    Idempotente: só processa rows com `outcome_price IS NULL`. Re-correr depois
    de window maior preenche os mais antigos.
    """
    db = DBS[market]
    bench_sym = BENCHMARK[market]
    today = date.today().isoformat()
    cutoff = (date.today() - timedelta(days=window_days)).isoformat()

    stats = {"considered": 0, "filled": 0, "skipped_no_price": 0, "skipped_no_bench": 0, "errors": 0}

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT ticker, date, action, confidence_pct, price_at_verdict
                 FROM verdict_history
                WHERE outcome_price IS NULL
                  AND date <= ?
                  AND price_at_verdict IS NOT NULL
                ORDER BY date""",
            (cutoff,),
        ).fetchall()

        for ticker, vdate, action, conf, issued_price in rows:
            stats["considered"] += 1
            target = (date.fromisoformat(vdate) + timedelta(days=window_days)).isoformat()
            if target > today:
                continue

            outcome = _price_at_or_after(conn, ticker, target)
            if not outcome:
                stats["skipped_no_price"] += 1
                continue
            outcome_date, outcome_price = outcome
            return_pct = _pct_return(issued_price, outcome_price)

            # Benchmark (price at issued_date and at outcome_date)
            bench_start = _price_on_or_before(conn, bench_sym, vdate)
            bench_end = _price_at_or_after(conn, bench_sym, outcome_date)
            if not bench_start or not bench_end:
                stats["skipped_no_bench"] += 1
                bench_return = None
                vs_bench = None
                outperf_bench = None
            else:
                bench_return = _pct_return(bench_start[1], bench_end[1])
                vs_bench = return_pct - bench_return
                _, outperf_bench = _accuracy(action, return_pct, vs_bench)

            # Sector ETF (US only)
            sec_etf = _sector_etf(conn, ticker, market)
            sec_return = None
            vs_sector = None
            outperf_sector = None
            if sec_etf:
                sec_start = _price_on_or_before(conn, sec_etf, vdate)
                sec_end = _price_at_or_after(conn, sec_etf, outcome_date)
                if sec_start and sec_end:
                    sec_return = _pct_return(sec_start[1], sec_end[1])
                    vs_sector = return_pct - sec_return
                    _, outperf_sector = _accuracy(action, return_pct, vs_sector)

            # Directional accuracy uses absolute return (independent of benchmark)
            accuracy_int, _ = _accuracy(action, return_pct, vs_bench if vs_bench is not None else 0.0)

            if dry_run:
                print(f"  [dry] {ticker} {vdate} {action:<5} ret={return_pct:+.2f}% "
                      f"vs_{bench_sym}={vs_bench if vs_bench is not None else 'na':>7} "
                      f"vs_sec={vs_sector if vs_sector is not None else 'na':>7}")
                continue

            conn.execute(
                """UPDATE verdict_history
                      SET outcome_price=?, outcome_date=?, outcome_return=?,
                          benchmark_symbol=?, benchmark_return=?, return_vs_benchmark=?,
                          sector_etf=?, return_vs_sector=?,
                          accuracy=?, outperformed_benchmark=?, outperformed_sector=?
                    WHERE ticker=? AND date=?""",
                (outcome_price, outcome_date, return_pct,
                 bench_sym, bench_return, vs_bench,
                 sec_etf, vs_sector,
                 accuracy_int, outperf_bench, outperf_sector,
                 ticker, vdate),
            )
            stats["filled"] += 1

        if not dry_run:
            conn.commit()

    return stats


# ============================================================
# Calibration curve
# ============================================================
def calibration_curve(market: str, lookback_days: int = 365) -> dict[str, Any]:
    """Conviction (`confidence_pct`) vs realised outperformance vs benchmark.

    Bins: 0-20, 20-40, 40-60, 60-80, 80-100. Reports n + median vs_benchmark +
    median vs_sector + hit rate (fraction outperformed_benchmark=1).
    """
    db = DBS[market]
    cutoff = (date.today() - timedelta(days=lookback_days)).isoformat()
    bins: dict[str, list[dict[str, Any]]] = {f"{i}-{i+20}": [] for i in range(0, 100, 20)}

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT confidence_pct, return_vs_benchmark, return_vs_sector,
                      outperformed_benchmark, action
                 FROM verdict_history
                WHERE outcome_price IS NOT NULL
                  AND return_vs_benchmark IS NOT NULL
                  AND date >= ?
                ORDER BY confidence_pct""",
            (cutoff,),
        ).fetchall()

    for conf, vs_bench, vs_sec, outperf, action in rows:
        if conf is None:
            continue
        bin_start = min(int(conf // 20) * 20, 80)
        key = f"{bin_start}-{bin_start+20}"
        bins[key].append({
            "vs_bench": vs_bench,
            "vs_sec":   vs_sec,
            "outperf":  outperf,
            "action":   action,
        })

    curve: dict[str, Any] = {}
    for key in sorted(bins.keys(), key=lambda k: int(k.split("-")[0])):
        items = bins[key]
        if not items:
            curve[key] = None
            continue
        vs_bench_vals = sorted([it["vs_bench"] for it in items if it["vs_bench"] is not None])
        vs_sec_vals = sorted([it["vs_sec"] for it in items if it["vs_sec"] is not None])
        outperf_count = sum(1 for it in items if it["outperf"] == 1)
        curve[key] = {
            "n":               len(items),
            "median_vs_bench": round(vs_bench_vals[len(vs_bench_vals)//2], 2) if vs_bench_vals else None,
            "median_vs_sec":   round(vs_sec_vals[len(vs_sec_vals)//2], 2) if vs_sec_vals else None,
            "hit_rate_bench":  round(outperf_count / len(items) * 100, 1),
        }
    return curve


# ============================================================
# Engine attribution
# ============================================================
def engine_attribution(market: str) -> dict[str, Any]:
    """Por engine: hit rate baseado no verdict *individual do engine* (não no global).

    Cada engine tem um verdict per-row em `verdict_engine_breakdown`
    (BUY se score≥7, HOLD se ≥4, AVOID se <4). Para cada (engine, verdict),
    medimos:
      - n: quantas rows
      - bullish_hit: BUY/HOLD/AVOID match com return realizado (independente do
        verdict global do verdict_history)
      - avg_outcome_return / avg_vs_bench

    Isto é informativo porque permite ver, ex: "valuation engine emitiu BUY 12x
    e em 7 acertou (58%) — mas o engine de momentum acertou 9/12 (75%)".
    """
    db = DBS[market]
    out: dict[str, dict[str, Any]] = {}
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT veb.engine, veb.verdict,
                      vh.outcome_return, vh.return_vs_benchmark
                 FROM verdict_engine_breakdown veb
                 JOIN verdict_history vh
                   ON vh.ticker = veb.ticker AND vh.date = veb.date
                WHERE vh.outcome_price IS NOT NULL""",
        ).fetchall()

    # Aggregate per engine
    agg: dict[str, dict[str, Any]] = {}
    for engine, e_verdict, ret, vs_b in rows:
        if engine not in agg:
            agg[engine] = {"n": 0, "hits": 0, "rets": [], "vs_bench": [],
                           "by_verdict": {"BUY": [0,0], "HOLD": [0,0], "AVOID": [0,0], "N/A": [0,0]}}
        d = agg[engine]
        d["n"] += 1
        d["rets"].append(ret)
        if vs_b is not None:
            d["vs_bench"].append(vs_b)

        # Hit logic per-engine verdict
        ev = (e_verdict or "N/A").upper()
        if ev not in d["by_verdict"]:
            d["by_verdict"][ev] = [0, 0]
        d["by_verdict"][ev][0] += 1
        # bullish (BUY) -> hit if ret>0; bearish (AVOID) -> hit if ret<0;
        # neutral (HOLD) -> hit if |ret|<HOLD_BAND_PCT
        if ev == "BUY" and ret > 0:
            d["hits"] += 1
            d["by_verdict"][ev][1] += 1
        elif ev == "AVOID" and ret < 0:
            d["hits"] += 1
            d["by_verdict"][ev][1] += 1
        elif ev == "HOLD" and abs(ret) < HOLD_BAND_PCT:
            d["hits"] += 1
            d["by_verdict"][ev][1] += 1

    for engine, d in agg.items():
        rets = d["rets"]
        vs_b = d["vs_bench"]
        out[engine] = {
            "n":             d["n"],
            "hit_rate":      round(d["hits"] / d["n"] * 100, 1) if d["n"] else 0.0,
            "avg_return":    round(sum(rets) / len(rets), 2) if rets else None,
            "avg_vs_bench":  round(sum(vs_b) / len(vs_b), 2) if vs_b else None,
            "by_verdict":    {k: {"n": v[0], "hits": v[1],
                                  "hit_rate": round(v[1]/v[0]*100, 1) if v[0] else 0.0}
                              for k, v in d["by_verdict"].items() if v[0] > 0},
        }
    return out


# ============================================================
# Post-mortem
# ============================================================
def post_mortem(market: str, year: int, quarter: int) -> dict[str, Any]:
    """Trimestral: das verdicts emitidas no Qx do ano Y, como foram?"""
    db = DBS[market]
    month_start = (quarter - 1) * 3 + 1
    months = [month_start, month_start + 1, month_start + 2]

    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT action,
                      COUNT(*) AS n,
                      AVG(outcome_return) AS avg_ret,
                      AVG(return_vs_benchmark) AS avg_vs_bench,
                      SUM(CASE WHEN accuracy=1 THEN 1 ELSE 0 END) AS hits,
                      SUM(CASE WHEN outperformed_benchmark=1 THEN 1 ELSE 0 END) AS bench_hits,
                      MIN(outcome_return) AS worst,
                      MAX(outcome_return) AS best
                 FROM verdict_history
                WHERE strftime('%Y', date) = ?
                  AND CAST(strftime('%m', date) AS INTEGER) IN (?, ?, ?)
                  AND outcome_price IS NOT NULL
                GROUP BY action""",
            (str(year), *months),
        ).fetchall()

    out: dict[str, Any] = {"market": market, "year": year, "quarter": quarter, "actions": {}}
    for action, n, avg_ret, avg_vb, hits, bh, worst, best in rows:
        out["actions"][action] = {
            "n":              n,
            "avg_return":     round(avg_ret, 2) if avg_ret is not None else None,
            "avg_vs_bench":   round(avg_vb, 2) if avg_vb is not None else None,
            "hit_rate":       round((hits or 0) / n * 100, 1) if n else 0.0,
            "bench_hit_rate": round((bh or 0) / n * 100, 1) if n else 0.0,
            "worst":          round(worst, 2) if worst is not None else None,
            "best":           round(best, 2) if best is not None else None,
        }
    return out


# ============================================================
# CLI
# ============================================================
def _print_calibration(market: str, curve: dict[str, Any]) -> None:
    print(f"\nCalibration curve — {market.upper()} (last 365d)")
    print(f"{'Bin':<10}{'N':>6}{'med vs bench':>15}{'med vs sec':>14}{'hit % bench':>14}")
    for bin_key, data in curve.items():
        if data is None:
            print(f"{bin_key:<10}{'--':>6}{'--':>15}{'--':>14}{'--':>14}")
            continue
        mvb = f"{data['median_vs_bench']:+.2f}" if data["median_vs_bench"] is not None else "n/a"
        mvs = f"{data['median_vs_sec']:+.2f}" if data["median_vs_sec"] is not None else "n/a"
        print(f"{bin_key:<10}{data['n']:>6}{mvb:>15}{mvs:>14}{data['hit_rate_bench']:>13.1f}%")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    upd = sub.add_parser("update", help="Cruza verdicts ≥window_days antigos com forward return + benchmarks")
    upd.add_argument("--market", choices=("br", "us", "both"), default="both")
    upd.add_argument("--window", type=int, default=30, help="dias forward (default 30)")
    upd.add_argument("--dry-run", action="store_true")

    rst = sub.add_parser("reset-accuracy", help="Recomputa accuracy nas rows já fechadas (sem re-fetch)")
    rst.add_argument("--market", choices=("br", "us", "both"), default="both")

    cal = sub.add_parser("calibration", help="Imprime calibration curve")
    cal.add_argument("--market", choices=("br", "us"), default="us")
    cal.add_argument("--lookback", type=int, default=365)
    cal.add_argument("--json", action="store_true")

    pm = sub.add_parser("post-mortem", help="Trimestral: 'YYYY-Qn'")
    pm.add_argument("quarter", help="ex: 2026-Q1")
    pm.add_argument("--market", choices=("br", "us"), default="us")
    pm.add_argument("--json", action="store_true")

    eng = sub.add_parser("engine-attribution", help="Hit rate por engine (precisa Bloco 1.2)")
    eng.add_argument("--market", choices=("br", "us"), default="us")
    eng.add_argument("--json", action="store_true")

    args = ap.parse_args()

    if args.cmd == "update":
        markets = ("br", "us") if args.market == "both" else (args.market,)
        for m in markets:
            print(f"[update] market={m} window={args.window}d{' (dry-run)' if args.dry_run else ''}")
            stats = update_outcomes(m, args.window, args.dry_run)
            print(f"  considered={stats['considered']} filled={stats['filled']} "
                  f"skipped_no_price={stats['skipped_no_price']} "
                  f"skipped_no_bench={stats['skipped_no_bench']}")
        return 0

    if args.cmd == "reset-accuracy":
        markets = ("br", "us") if args.market == "both" else (args.market,)
        for m in markets:
            stats = reset_accuracy(m)
            print(f"[reset-accuracy] market={m} updated={stats['updated']}")
        return 0

    if args.cmd == "calibration":
        curve = calibration_curve(args.market, args.lookback)
        if args.json:
            print(json.dumps(curve, indent=2))
        else:
            _print_calibration(args.market, curve)
        return 0

    if args.cmd == "post-mortem":
        try:
            year_s, q_s = args.quarter.split("-Q")
            year, quarter = int(year_s), int(q_s)
        except (ValueError, IndexError):
            print(f"erro: quarter deve ter formato YYYY-Qn, recebido {args.quarter!r}")
            return 1
        report = post_mortem(args.market, year, quarter)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"\nPost-mortem {args.market.upper()} {year}-Q{quarter}\n")
            for action, d in report["actions"].items():
                print(f"  {action}: n={d['n']} avg_ret={d['avg_return']:+.2f}% "
                      f"avg_vs_bench={d['avg_vs_bench']:+.2f}% "
                      f"hit={d['hit_rate']:.1f}% bench_hit={d['bench_hit_rate']:.1f}%")
        return 0

    if args.cmd == "engine-attribution":
        attr = engine_attribution(args.market)
        if args.json:
            print(json.dumps(attr, indent=2))
            return 0
        if not attr:
            print("(sem dados — Bloco 1.2 ainda não populou verdict_engine_breakdown)")
            return 0
        print(f"\nEngine attribution — {args.market.upper()}")
        print(f"{'Engine':<12}{'N':>6}{'hit %':>10}{'avg ret':>10}{'avg vs bench':>15}")
        for engine, d in attr.items():
            ar = f"{d['avg_return']:+.2f}" if d["avg_return"] is not None else "n/a"
            avb = f"{d['avg_vs_bench']:+.2f}" if d["avg_vs_bench"] is not None else "n/a"
            print(f"{engine:<12}{d['n']:>6}{d['hit_rate']:>9.1f}%{ar:>10}{avb:>15}")
        # Per-verdict breakdown
        print(f"\n  By per-engine verdict (BUY=score>=7, HOLD=>=4, AVOID=<4):")
        print(f"  {'engine':<12}{'verdict':<8}{'n':>5}{'hits':>6}{'hit %':>8}")
        for engine, d in attr.items():
            for ev, sub in d["by_verdict"].items():
                print(f"  {engine:<12}{ev:<8}{sub['n']:>5}{sub['hits']:>6}{sub['hit_rate']:>7.1f}%")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
