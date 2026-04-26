"""backtest_triggers — replay triggers em série histórica de preços.

Mede, para cada trigger que *teria disparado* no passado, o return forward
em 30d, 90d e 180d. Permite avaliar se as regras declarativas produzem
timing útil (entrada) ou se são ruído.

Estratégia simplificada: para cada ticker × cada dia t, avalia condição
`price_drop_from_high` e `dy_above_pct` usando dados até t. Se passa, marca
como "trigger hipotético" e regista return t→t+30/90/180.

Limitações:
- Não recorre aos triggers exactos em yaml; usa parametrização embebida.
- Não replays quality triggers (Altman/Piotroski) — demasiado pesado sem
  snapshot trimestral reindex.

Uso:
    python -m analytics.backtest_triggers --market us --start 2020
    python -m analytics.backtest_triggers --market br --kind dy_above_pct --threshold 6
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _fetch_prices(conn: sqlite3.Connection, ticker: str, start: str) -> list[tuple[str, float]]:
    return list(conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? AND date >= ? ORDER BY date ASC",
        (ticker, start),
    ))


def _forward_return(prices: list[tuple], idx: int, offset_days: int) -> float | None:
    if idx >= len(prices):
        return None
    base_date = date.fromisoformat(prices[idx][0])
    target = (base_date + timedelta(days=offset_days)).isoformat()
    # find closest price on/after target
    for d, c in prices[idx + 1 :]:
        if d >= target:
            return (c / prices[idx][1] - 1) * 100
    return None


def _max_since(prices: list[tuple], idx: int, lookback_days: int) -> float | None:
    base_date = date.fromisoformat(prices[idx][0])
    cutoff = (base_date - timedelta(days=lookback_days)).isoformat()
    hi = 0.0
    for d, c in prices[:idx + 1]:
        if d >= cutoff and c > hi:
            hi = c
    return hi if hi > 0 else None


def _trailing_12m_div(conn: sqlite3.Connection, ticker: str, as_of: str) -> float:
    """Sum of ex_date dividends na janela (as_of-365d, as_of]."""
    start = (date.fromisoformat(as_of) - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT SUM(amount) FROM dividends WHERE ticker=? AND ex_date>? AND ex_date<=?",
        (ticker, start, as_of),
    ).fetchone()
    return (r[0] or 0.0)


def backtest_drop(market: str, start: str, threshold_pct: float, lookback_days: int,
                  forward_windows: list[int]) -> dict:
    """Para cada ticker, cada dia t: se price ≤ max(lookback)*(1+threshold_pct/100),
    regista t como evento e mede return forward."""
    db = DB_BR if market == "br" else DB_US
    events: list[dict] = []
    with sqlite3.connect(db) as c:
        tickers = [r[0] for r in c.execute("SELECT DISTINCT ticker FROM prices")]
        for tk in tickers:
            prices = _fetch_prices(c, tk, start)
            last_event_idx = -1_000
            for i, (d, px) in enumerate(prices):
                hi = _max_since(prices, i, lookback_days)
                if hi is None:
                    continue
                drop = (px / hi - 1) * 100
                if drop <= threshold_pct:
                    # evita "trigger-spam" diário — impõe cooldown de lookback/2 dias
                    if i - last_event_idx < lookback_days // 2:
                        continue
                    last_event_idx = i
                    ev = {"ticker": tk, "date": d, "price": px, "drop_pct": drop}
                    for w in forward_windows:
                        ev[f"ret_{w}d_pct"] = _forward_return(prices, i, w)
                    events.append(ev)
    return _summarize(events, forward_windows, f"price_drop≤{threshold_pct}% lb={lookback_days}d")


def backtest_dy(market: str, start: str, threshold_pct: float,
                forward_windows: list[int]) -> dict:
    db = DB_BR if market == "br" else DB_US
    events: list[dict] = []
    with sqlite3.connect(db) as c:
        tickers = [r[0] for r in c.execute("SELECT DISTINCT ticker FROM prices")]
        for tk in tickers:
            prices = _fetch_prices(c, tk, start)
            last_event_idx = -1_000
            for i, (d, px) in enumerate(prices):
                if px <= 0:
                    continue
                # cooldown 30d
                if i - last_event_idx < 30:
                    continue
                div = _trailing_12m_div(c, tk, d)
                if div <= 0:
                    continue
                dy = div / px * 100
                if dy >= threshold_pct:
                    last_event_idx = i
                    ev = {"ticker": tk, "date": d, "price": px, "dy_pct": dy}
                    for w in forward_windows:
                        ev[f"ret_{w}d_pct"] = _forward_return(prices, i, w)
                    events.append(ev)
    return _summarize(events, forward_windows, f"dy≥{threshold_pct}%")


def _summarize(events: list[dict], windows: list[int], name: str) -> dict:
    def mean(xs): return (sum(xs) / len(xs)) if xs else None
    def median(xs):
        s = sorted(x for x in xs if x is not None)
        return s[len(s) // 2] if s else None

    per_window: dict[int, dict] = {}
    for w in windows:
        key = f"ret_{w}d_pct"
        vals = [e[key] for e in events if e.get(key) is not None]
        per_window[w] = {
            "n": len(vals),
            "mean": round(mean(vals), 2) if vals else None,
            "median": round(median(vals), 2) if vals else None,
            "win_rate": round(sum(1 for v in vals if v > 0) / len(vals) * 100, 1) if vals else None,
            "p25": round(sorted(vals)[len(vals) // 4], 2) if vals else None,
            "p75": round(sorted(vals)[3 * len(vals) // 4], 2) if vals else None,
        }
    by_ticker: dict[str, int] = defaultdict(int)
    for e in events:
        by_ticker[e["ticker"]] += 1

    return {
        "name": name,
        "total_events": len(events),
        "unique_tickers": len(by_ticker),
        "per_window": per_window,
        "top_triggered": sorted(by_ticker.items(), key=lambda x: -x[1])[:10],
    }


def _print_report(r: dict) -> None:
    print(f"\n=== {r['name']} ===")
    print(f"Eventos totais: {r['total_events']}  |  Tickers únicos: {r['unique_tickers']}")
    print(f"{'Window':<10}{'N':<6}{'Mean %':<10}{'Median %':<12}{'Win %':<8}{'P25 %':<8}{'P75 %':<8}")
    for w, s in r["per_window"].items():
        print(f"{w:<10}{s['n']:<6}"
              f"{str(s['mean'] or '-'):<10}"
              f"{str(s['median'] or '-'):<12}"
              f"{str(s['win_rate'] or '-'):<8}"
              f"{str(s['p25'] or '-'):<8}"
              f"{str(s['p75'] or '-'):<8}")
    if r["top_triggered"]:
        print("Top triggered:", ", ".join(f"{t}({n})" for t, n in r["top_triggered"][:8]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--start", default="2018-01-01")
    ap.add_argument("--kind", choices=["price_drop", "dy_above"], default="price_drop")
    ap.add_argument("--threshold", type=float, help="% (negativo para drop, positivo para dy)")
    ap.add_argument("--lookback", type=int, default=90, help="para price_drop")
    ap.add_argument("--windows", default="30,90,180")
    args = ap.parse_args()

    windows = [int(w) for w in args.windows.split(",")]

    if args.kind == "price_drop":
        thr = args.threshold if args.threshold is not None else -15.0
        r = backtest_drop(args.market, args.start, thr, args.lookback, windows)
    else:
        thr = args.threshold if args.threshold is not None else 5.0
        r = backtest_dy(args.market, args.start, thr, windows)
    _print_report(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
