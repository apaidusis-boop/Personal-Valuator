"""paper_trade_close — fecha paper signals expirados.

Sem este script, paper_trade_signals nunca closes → win_rate undefined → real
capital nunca liberado. F1 do T0 cleanup (2026-04-26).

Fecha um signal quando:
  signal_date + HORIZON_DAYS[horizon] <= today.

Horizon mapping (conservador, alinhado com value/quality methods):
  short  →  30d  (earnings reaction window)
  medium →  90d  (1 quarter, ciclo Damodaran/Graham clássico)
  long   → 365d  (1 ano, Buffett/compounder)

Realized return:
  LONG:    (close - entry) / entry * 100
  SHORT:   (entry - close) / entry * 100   (profit when price drops)
  NEUTRAL: (close - entry) / entry * 100   (just the delta; no win/loss verdict)

Win/loss flag (notes JSON):
  LONG/SHORT: win = realized_return_pct >= expected_move_pct * 0.5
              (hit 50%+ of expected move = considerado win)
  NEUTRAL:    win = abs(realized_return_pct) < expected_move_pct
              (stayed within expected band)

Uso:
  python scripts/paper_trade_close.py                  # fecha tudo expirado
  python scripts/paper_trade_close.py --dry-run        # preview
  python scripts/paper_trade_close.py --all-now        # forçar close de todos
                                                       (debug; usa today price)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}

HORIZON_DAYS = {"short": 30, "medium": 90, "long": 365}
DEFAULT_HORIZON_DAYS = 90  # if horizon missing/unknown


@dataclass
class CloseResult:
    id: int
    ticker: str
    market: str
    direction: str
    days_held: int
    entry_price: float
    close_price: float
    realized_return_pct: float
    win: bool | None
    method_id: str
    horizon: str


def _get_latest_close(c: sqlite3.Connection, ticker: str) -> tuple[float | None, str | None]:
    r = c.execute(
        "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if r and r[0] is not None:
        return float(r[0]), r[1]
    return None, None


def _get_close_on_or_before(c: sqlite3.Connection, ticker: str, target_date: str
                             ) -> tuple[float | None, str | None]:
    r = c.execute(
        "SELECT close, date FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, target_date),
    ).fetchone()
    if r and r[0] is not None:
        return float(r[0]), r[1]
    return None, None


def _compute_return(direction: str, entry: float, close: float) -> float:
    if entry <= 0:
        return 0.0
    if direction == "SHORT":
        return (entry - close) / entry * 100
    # LONG, NEUTRAL, default → forward delta
    return (close - entry) / entry * 100


def _judge_win(direction: str, realized: float, expected_move: float | None) -> bool | None:
    if expected_move is None:
        return None
    target = abs(expected_move)
    if direction == "NEUTRAL":
        # win = stayed within expected band (low volatility thesis)
        return abs(realized) < target
    # LONG / SHORT: win if hit ≥ 50% of expected move (in profit direction)
    return realized >= target * 0.5


def close_expired(market: str, dry_run: bool = False, force_all: bool = False
                  ) -> list[CloseResult]:
    db = DBS[market]
    if not db.exists():
        return []
    today = date.today()
    today_iso = today.isoformat()
    closed: list[CloseResult] = []
    skipped_no_price = 0

    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT * FROM paper_trade_signals WHERE status='open' ORDER BY signal_date"
        ).fetchall()

        for row in rows:
            sig_date_str = row["signal_date"] or ""
            try:
                sig_date = date.fromisoformat(sig_date_str)
            except ValueError:
                continue
            horizon = (row["horizon"] or "").lower().strip()
            horizon_days = HORIZON_DAYS.get(horizon, DEFAULT_HORIZON_DAYS)
            target_close_date = sig_date.fromordinal(sig_date.toordinal() + horizon_days)
            if not force_all and today < target_close_date:
                continue

            ticker = row["ticker"]
            # Pick close price: prefer the price ON target_close_date if exists,
            # else fallback to latest close (used when force_all or no row that day).
            cls_target = target_close_date.isoformat()
            cls_price, cls_date = _get_close_on_or_before(c, ticker, cls_target)
            if cls_price is None:
                cls_price, cls_date = _get_latest_close(c, ticker)
            if cls_price is None:
                skipped_no_price += 1
                continue

            entry = float(row["entry_price"] or 0)
            if entry <= 0:
                continue

            direction = row["direction"] or "LONG"
            realized = _compute_return(direction, entry, cls_price)
            win = _judge_win(direction, realized,
                             float(row["expected_move_pct"]) if row["expected_move_pct"] is not None else None)

            note_payload = {
                "closed_by": "paper_trade_close.py",
                "closed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "horizon_days": horizon_days,
                "horizon_label": horizon or "default",
                "close_date": cls_date,
                "close_target_date": cls_target,
                "win": win,
                "expected_move_pct": row["expected_move_pct"],
                "method_id": row["method_id"],
            }

            if not dry_run:
                c.execute(
                    """UPDATE paper_trade_signals
                       SET status='closed', closed_at=?, closed_price=?,
                           realized_return_pct=?, notes=?
                       WHERE id=?""",
                    (cls_date, cls_price, realized,
                     json.dumps(note_payload, ensure_ascii=False),
                     row["id"]),
                )

            days_held = (date.fromisoformat(cls_date) - sig_date).days if cls_date else horizon_days
            closed.append(CloseResult(
                id=row["id"], ticker=ticker, market=market, direction=direction,
                days_held=days_held, entry_price=entry, close_price=cls_price,
                realized_return_pct=realized, win=win,
                method_id=row["method_id"] or "?", horizon=horizon or "default",
            ))

        if not dry_run:
            c.commit()

    if skipped_no_price:
        print(f"[{market}] WARN: skipped {skipped_no_price} signals (no price data for ticker)")
    return closed


def summarize(results: list[CloseResult]) -> dict:
    if not results:
        return {"closed": 0}
    n_long = sum(1 for r in results if r.direction == "LONG")
    n_short = sum(1 for r in results if r.direction == "SHORT")
    n_neutral = sum(1 for r in results if r.direction == "NEUTRAL")
    judgable = [r for r in results if r.win is not None]
    wins = sum(1 for r in judgable if r.win)
    avg_return = sum(r.realized_return_pct for r in results) / len(results)
    return {
        "closed": len(results),
        "long": n_long, "short": n_short, "neutral": n_neutral,
        "judgable": len(judgable),
        "wins": wins,
        "win_rate_pct": round(wins / len(judgable) * 100, 1) if judgable else None,
        "avg_realized_return_pct": round(avg_return, 2),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--market", choices=["br", "us", "both"], default="both")
    ap.add_argument("--dry-run", action="store_true", help="preview, no DB writes")
    ap.add_argument("--all-now", action="store_true",
                    help="force-close ALL open signals (uses latest price)")
    ap.add_argument("--limit", type=int, default=None, help="cap shown rows")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    markets = ["br", "us"] if args.market == "both" else [args.market]
    all_results: list[CloseResult] = []
    for m in markets:
        results = close_expired(m, dry_run=args.dry_run, force_all=args.all_now)
        all_results.extend(results)
        s = summarize(results)
        print(f"\n=== {m.upper()} ===  closed={s['closed']}", end="")
        if s["closed"]:
            print(f" | long={s['long']} short={s['short']} neutral={s['neutral']}"
                  f" | win_rate={s['win_rate_pct']}% (n_judgable={s['judgable']})"
                  f" | avg_return={s['avg_realized_return_pct']}%")
            shown = sorted(results, key=lambda r: r.realized_return_pct, reverse=True)
            if args.limit:
                shown = shown[:args.limit]
            for r in shown[:10]:
                w = "?" if r.win is None else ("✓" if r.win else "✗")
                print(f"  [{r.id:>4}] {r.market}:{r.ticker:<8} {r.direction:<7} "
                      f"{r.method_id[:32]:<32} {r.horizon:<6} "
                      f"{r.days_held}d  {r.entry_price:.2f}→{r.close_price:.2f}  "
                      f"{r.realized_return_pct:+.2f}%  win={w}")
        else:
            print(" (none expired)")

    overall = summarize(all_results)
    print(f"\n=== TOTAL ===  closed={overall.get('closed', 0)}", end="")
    if overall.get("closed"):
        print(f" | win_rate={overall.get('win_rate_pct')}% "
              f"(n_judgable={overall.get('judgable')}) | "
              f"avg_return={overall.get('avg_realized_return_pct')}%")
    else:
        print("")

    if args.dry_run:
        print("\n(DRY RUN — no DB writes)")


if __name__ == "__main__":
    main()
