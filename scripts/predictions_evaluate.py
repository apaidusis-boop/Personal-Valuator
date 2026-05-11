"""predictions_evaluate — fecha predictions expiradas + computes outcome.

Counterpart de `scripts/paper_trade_close.py` mas para a tabela `predictions`
(analyst calls + YouTube channel predictions, ingested via Phase U + Phase Q).

Sem este eval, predictions ficam `outcome='pending'` para sempre →
track record de analysts undefined → variant_perception não consegue
calibrar source-weighting (mesmo bug estrutural que paper_trade pre-Phase F).

Outcome rules (per `predicted_stance`):
  bull / accumulate / buy:
    return >= +5%       → correct
    return <= -5%       → wrong
    -5% < return < +5%  → partial
  bear / sell / avoid:
    return <= -5%       → correct
    return >= +5%       → wrong
    else                → partial
  neutral / hold:
    abs(return) < 5%    → correct
    abs(return) >= 5%   → wrong (neutral was wrong; market moved)

WIN_THRESHOLD_PCT é tunável; 5% é o defeito (significant move 90d).

Uso:
  python scripts/predictions_evaluate.py
  python scripts/predictions_evaluate.py --dry-run
  python scripts/predictions_evaluate.py --report-only           # só track record sumário
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}

WIN_THRESHOLD_PCT = 5.0

BULL_STANCES = {"bull", "buy", "accumulate", "long", "positive", "outperform"}
BEAR_STANCES = {"bear", "sell", "avoid", "short", "negative", "underperform"}
NEUTRAL_STANCES = {"neutral", "hold", "market", "marketperform"}


@dataclass
class EvalResult:
    id: int
    source: str
    ticker: str
    stance: str
    horizon_days: int
    days_actual: int
    return_pct: float
    outcome: str  # correct | wrong | partial


def _classify(stance: str, return_pct: float) -> str:
    s = (stance or "").strip().lower()
    if s in BULL_STANCES:
        if return_pct >= WIN_THRESHOLD_PCT:
            return "correct"
        if return_pct <= -WIN_THRESHOLD_PCT:
            return "wrong"
        return "partial"
    if s in BEAR_STANCES:
        if return_pct <= -WIN_THRESHOLD_PCT:
            return "correct"
        if return_pct >= WIN_THRESHOLD_PCT:
            return "wrong"
        return "partial"
    if s in NEUTRAL_STANCES:
        return "correct" if abs(return_pct) < WIN_THRESHOLD_PCT else "wrong"
    # unknown stance
    return "partial"


def _price_at(c: sqlite3.Connection, ticker: str, on_date: str) -> tuple[float | None, str | None]:
    r = c.execute(
        "SELECT close, date FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, on_date),
    ).fetchone()
    if r and r[0] is not None:
        return float(r[0]), r[1]
    return None, None


def evaluate_market(market: str, dry_run: bool = False) -> list[EvalResult]:
    db = DBS[market]
    if not db.exists():
        return []
    today = date.today()
    today_iso = today.isoformat()
    out: list[EvalResult] = []
    skipped = {"no_horizon": 0, "no_price": 0, "not_due": 0}

    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT * FROM predictions WHERE outcome='pending' ORDER BY prediction_date"
        ).fetchall()

        for row in rows:
            sig_date_str = row["prediction_date"] or ""
            try:
                sig_date = date.fromisoformat(sig_date_str)
            except ValueError:
                continue
            horizon = row["horizon_days"]
            if horizon is None or horizon <= 0:
                skipped["no_horizon"] += 1
                continue
            target_date = sig_date.fromordinal(sig_date.toordinal() + int(horizon))
            if today < target_date:
                skipped["not_due"] += 1
                continue

            ticker = row["ticker"]
            target_iso = target_date.isoformat()
            cls_price, cls_date = _price_at(c, ticker, target_iso)
            if cls_price is None:
                cls_price, cls_date = _price_at(c, ticker, today_iso)
            if cls_price is None:
                skipped["no_price"] += 1
                continue

            entry = float(row["price_at_pred"] or 0)
            if entry <= 0:
                skipped["no_price"] += 1
                continue
            ret_pct = (cls_price - entry) / entry * 100.0
            outcome = _classify(row["predicted_stance"] or "", ret_pct)
            days_actual = (date.fromisoformat(cls_date) - sig_date).days if cls_date else int(horizon)

            if not dry_run:
                c.execute(
                    """UPDATE predictions
                       SET evaluated_at=?, price_at_eval=?, outcome=?
                       WHERE id=?""",
                    (cls_date, cls_price, outcome, row["id"]),
                )

            out.append(EvalResult(
                id=row["id"], source=row["source"] or "?", ticker=ticker,
                stance=row["predicted_stance"] or "?",
                horizon_days=int(horizon), days_actual=days_actual,
                return_pct=ret_pct, outcome=outcome,
            ))

        if not dry_run:
            c.commit()

    if any(skipped.values()):
        print(f"[{market}] skipped: {skipped}")
    return out


def track_record_summary(market: str, days_back: int = 365) -> list[dict]:
    """Win rate per source (1y rolling window por defeito)."""
    db = DBS[market]
    if not db.exists():
        return []
    cutoff = (date.today().toordinal() - days_back)
    cutoff_iso = date.fromordinal(cutoff).isoformat()
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """SELECT source,
                      COUNT(*) AS calls,
                      SUM(CASE WHEN outcome='correct' THEN 1 ELSE 0 END) AS correct,
                      SUM(CASE WHEN outcome='wrong' THEN 1 ELSE 0 END) AS wrong,
                      SUM(CASE WHEN outcome='partial' THEN 1 ELSE 0 END) AS partial,
                      SUM(CASE WHEN outcome='pending' THEN 1 ELSE 0 END) AS pending
               FROM predictions
               WHERE prediction_date >= ?
               GROUP BY source
               ORDER BY calls DESC""",
            (cutoff_iso,),
        ).fetchall()
    out: list[dict] = []
    for r in rows:
        d = dict(r)
        judged = d["calls"] - d["pending"]
        d["win_rate_pct"] = round(d["correct"] / judged * 100, 1) if judged else None
        out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--market", choices=["br", "us", "both"], default="both")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report-only", action="store_true",
                    help="skip eval, only print track record summary")
    ap.add_argument("--days-back", type=int, default=365,
                    help="track record rolling window (default 365)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    markets = ["br", "us"] if args.market == "both" else [args.market]
    all_results: list[EvalResult] = []

    if not args.report_only:
        for m in markets:
            results = evaluate_market(m, dry_run=args.dry_run)
            all_results.extend(results)
            n = len(results)
            print(f"\n=== {m.upper()} === closed={n}", end="")
            if n:
                wins = sum(1 for r in results if r.outcome == "correct")
                wrongs = sum(1 for r in results if r.outcome == "wrong")
                partials = sum(1 for r in results if r.outcome == "partial")
                print(f"  correct={wins} wrong={wrongs} partial={partials}")
                for r in results[:10]:
                    mark = {"correct": "✓", "wrong": "✗", "partial": "~"}.get(r.outcome, "?")
                    print(f"  [{r.id:>4}] {r.ticker:<8} {r.source[:18]:<18} "
                          f"{r.stance:<8} {r.days_actual}d  {r.return_pct:+.1f}%  {mark}")
            else:
                print(" (none due)")

    # Track record summary
    print("\n=== TRACK RECORD (rolling {}d) ===".format(args.days_back))
    for m in markets:
        rows = track_record_summary(m, days_back=args.days_back)
        if not rows:
            continue
        print(f"  [{m.upper()}]")
        print(f"  {'source':<22} {'calls':>5} {'correct':>7} {'wrong':>5} "
              f"{'partial':>7} {'pending':>7} {'win_rate':>8}")
        for r in rows:
            wr = f"{r['win_rate_pct']}%" if r['win_rate_pct'] is not None else "—"
            print(f"  {r['source'][:22]:<22} {r['calls']:>5} {r['correct']:>7} "
                  f"{r['wrong']:>5} {r['partial']:>7} {r['pending']:>7} {wr:>8}")

    if args.dry_run:
        print("\n(DRY RUN — no DB writes)")


if __name__ == "__main__":
    main()
