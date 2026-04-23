"""verdict_history — persiste verdicts diários para backtest forward-only.

Grava em tabela `verdict_history` em AMBAS as DBs (BR e US) para permitir
cross-market analysis. Idempotente por (ticker, date).

Uso:
    python scripts/verdict_history.py record            # regista hoje todos holdings
    python scripts/verdict_history.py record --all      # universe inteiro (lento)
    python scripts/verdict_history.py backtest          # mede accuracy +30/+90d
    python scripts/verdict_history.py show ACN          # histórico ACN
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from dataclasses import asdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def record_verdict(ticker: str, replace: bool = False) -> dict:
    from scripts.verdict import compute_verdict
    from scripts.refresh_ticker import _market_of
    market = _market_of(ticker)
    v = compute_verdict(ticker)
    today = date.today().isoformat()
    now = datetime.now(UTC).isoformat()

    price = v.momentum_detail.get("price_latest")
    with sqlite3.connect(_db(market)) as c:
        if replace:
            c.execute("DELETE FROM verdict_history WHERE ticker=? AND date=?", (ticker, today))
        try:
            c.execute(
                """INSERT INTO verdict_history
                     (ticker, date, action, total_score, confidence_pct,
                      quality_score, valuation_score, momentum_score, narrative_score,
                      price_at_verdict, recorded_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (ticker, today, v.action, v.total_score, v.confidence_pct,
                 v.quality_score, v.valuation_score, v.momentum_score, v.narrative_score,
                 price, now),
            )
            c.commit()
            return {"ticker": ticker, "status": "inserted", "action": v.action, "score": v.total_score}
        except sqlite3.IntegrityError:
            return {"ticker": ticker, "status": "already_recorded_today"}


def record_all(include_watchlist: bool = False) -> dict:
    """Regista verdicts para holdings (default) ou universo completo."""
    tickers: list[tuple[str, str]] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if include_watchlist:
                rows = c.execute("SELECT ticker FROM companies").fetchall()
            else:
                rows = c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ).fetchall()
            for (t,) in rows:
                tickers.append((t, market))

    stats = {"inserted": 0, "skipped": 0, "error": 0}
    for tk, mk in tickers:
        try:
            r = record_verdict(tk)
            if r["status"] == "inserted":
                stats["inserted"] += 1
                print(f"  {tk:<8} {r['action']:<6} score={r['score']:.1f}")
            else:
                stats["skipped"] += 1
        except Exception as e:  # noqa: BLE001
            stats["error"] += 1
            print(f"  {tk:<8} ERROR: {e}")
    return stats


def _forward_return(conn: sqlite3.Connection, ticker: str, base_date: str, days: int) -> float | None:
    base = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date=?", (ticker, base_date)
    ).fetchone()
    if not base:
        return None
    target = (date.fromisoformat(base_date) + timedelta(days=days)).isoformat()
    fwd = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date>=? ORDER BY date LIMIT 1",
        (ticker, target),
    ).fetchone()
    if not fwd:
        return None
    return (fwd[0] / base[0] - 1) * 100


def backtest() -> dict:
    """Mede forward-return dos verdicts gravados vs acção."""
    from collections import defaultdict
    buckets: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"30d": [], "90d": [], "180d": []}
    )

    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute(
                """SELECT ticker, date, action, total_score FROM verdict_history
                   ORDER BY date, ticker"""
            ).fetchall()
            for tk, d, action, _score in rows:
                for w_name, w_days in (("30d", 30), ("90d", 90), ("180d", 180)):
                    r = _forward_return(c, tk, d, w_days)
                    if r is not None:
                        buckets[action][w_name].append(r)

    out: dict = {}
    for action, wins in buckets.items():
        out[action] = {}
        for window, vals in wins.items():
            if not vals:
                out[action][window] = None
                continue
            vals = sorted(vals)
            out[action][window] = {
                "n": len(vals),
                "mean": round(sum(vals) / len(vals), 2),
                "median": round(vals[len(vals) // 2], 2),
                "win_rate": round(sum(1 for v in vals if v > 0) / len(vals) * 100, 1),
                "min": round(vals[0], 2),
                "max": round(vals[-1], 2),
            }
    return out


def show_history(ticker: str) -> None:
    from scripts.refresh_ticker import _market_of
    market = _market_of(ticker)
    with sqlite3.connect(_db(market)) as c:
        rows = c.execute(
            """SELECT date, action, total_score, confidence_pct,
                      quality_score, valuation_score, momentum_score, price_at_verdict
               FROM verdict_history WHERE ticker=? ORDER BY date DESC""",
            (ticker,),
        ).fetchall()
    if not rows:
        print(f"(sem histórico para {ticker})")
        return
    print(f"{'Date':<12}{'Action':<8}{'Score':<8}{'Conf':<6}{'Qual':<6}{'Val':<6}{'Mom':<6}{'Price':<10}")
    for r in rows:
        print(f"{r[0]:<12}{r[1]:<8}{r[2]:<8.1f}{r[3]:<6}{r[4]:<6.1f}{r[5]:<6.1f}{r[6]:<6.1f}{r[7] or 0:<10.2f}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--all", action="store_true", help="Universo inteiro (lento)")
    sub.add_parser("backtest")
    sh = sub.add_parser("show"); sh.add_argument("ticker")
    args = ap.parse_args()

    from scripts.init_db import init
    init(DB_BR); init(DB_US)

    if args.cmd == "record":
        print(f"[record] holdings{'+watchlist' if args.all else ''}, {date.today()}")
        stats = record_all(include_watchlist=args.all)
        print(f"\n[done] inserted={stats['inserted']} skipped={stats['skipped']} errors={stats['error']}")
    elif args.cmd == "backtest":
        r = backtest()
        if not r:
            print("(sem verdicts gravados — correr 'record' primeiro, aguardar 30d, depois backtest)")
            return 0
        print("Backtest accuracy por action\n")
        print(f"{'Action':<8}{'Window':<8}{'N':<6}{'Mean %':<10}{'Med %':<10}{'Win %':<8}")
        for action, wins in r.items():
            for window, stats in wins.items():
                if stats is None:
                    continue
                print(f"{action:<8}{window:<8}{stats['n']:<6}"
                      f"{stats['mean']:<10}{stats['median']:<10}{stats['win_rate']:<8}")
    elif args.cmd == "show":
        show_history(args.ticker.upper())
    return 0


if __name__ == "__main__":
    sys.exit(main())
