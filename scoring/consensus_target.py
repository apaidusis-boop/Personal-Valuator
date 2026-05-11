"""consensus_target — aggregate price targets from multiple analyst houses.

Phase LL.3 Sprint 2. Builds the "blended fair price" the user described
in the dashboard vision:

    Nossa $14.50 | BTG $15 | XP $17 | Suno $14 | WS $16 | Consensus $15.30

Sources (in priority of authority for blend weight):
  our_fair       — scoring.fair_value.our_fair (filings-grounded)
  Suno           — analyst_insights kind=rating where source LIKE '%suno%'
  XP             — analyst_insights ... LIKE '%xp%'
  BTG            — analyst_insights ... LIKE '%btg%'
  Wall Street    — fundamentals.priceTarget (FMP if populated) — US only
  FMP analyst    — alternative US source if priceTarget missing

Today, BR has 58 tickers with at least 1 PT (42 Suno, 21 XP). BTG covered
in analyst_reports as 'BTG' but may not have explicit price_target on the
insight row — defer to extract_targets re-pass when needed.

Output (return dict):
  ticker, market, our_fair, current_price,
  houses: [{source, target, recency_days, stance, confidence}],
  blended:
    median: median of all targets including our_fair
    mean: equal-weight mean
    weighted: weighted by track-record × recency (decay 90d) × confidence
  dispersion: stddev / mean (volatility of targets)

CLI:
    python -m scoring.consensus_target ITSA4
    python -m scoring.consensus_target --holdings  (default)
    python -m scoring.consensus_target ITSA4 --json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from statistics import median, mean, stdev

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _detect_market(ticker: str) -> str | None:
    for m, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return m
    return None


def _our_fair(c: sqlite3.Connection, ticker: str) -> tuple[float | None, float | None, float | None]:
    """Returns (our_fair, consensus_fair, current_price)."""
    r = c.execute(
        """SELECT our_fair, fair_price, current_price
           FROM fair_value WHERE ticker=?
           ORDER BY computed_at DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    return (r[0], r[1], r[2]) if r else (None, None, None)


def _house_targets(c: sqlite3.Connection, ticker: str, *, days_window: int = 365) -> list[dict]:
    """Return latest non-null price_target per house (ai source LIKE)."""
    cutoff = (datetime.now(UTC).date().isoformat()[:10])
    # Window: rough — published_at < days_window
    rows = c.execute(
        """SELECT ar.source, ar.published_at, ai.price_target, ai.stance, ai.confidence
           FROM analyst_insights ai
           LEFT JOIN analyst_reports ar ON ar.id = ai.report_id
           WHERE ai.ticker=? AND ai.price_target IS NOT NULL
             AND ar.published_at IS NOT NULL
           ORDER BY ar.published_at DESC""",
        (ticker,),
    ).fetchall()
    if not rows:
        return []
    # Group by source (latest wins)
    by_source: dict[str, dict] = {}
    today = date.today()
    for src, pub, pt, stance, conf in rows:
        if not src:
            continue
        # Already sorted desc — first hit per source wins
        if src in by_source:
            continue
        try:
            pub_d = date.fromisoformat(pub[:10])
            recency_days = (today - pub_d).days
        except (ValueError, TypeError):
            recency_days = 9999
        if recency_days > days_window:
            continue
        by_source[src] = {
            "source": src, "target": float(pt),
            "recency_days": recency_days,
            "stance": stance, "confidence": conf,
            "published_at": pub,
        }
    return list(by_source.values())


def _wallstreet_target(c: sqlite3.Connection, ticker: str) -> dict | None:
    """US only: pull FMP analyst price target if persisted in fundamentals."""
    try:
        r = c.execute(
            """SELECT period_end FROM fundamentals
               WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
    except sqlite3.OperationalError:
        return None
    if not r:
        return None
    # Check if there's a 'analyst' table or similar
    try:
        wt = c.execute(
            """SELECT target_consensus, last_updated FROM analyst_targets_fmp
               WHERE ticker=? ORDER BY last_updated DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if wt and wt[0]:
            today = date.today()
            try:
                d = date.fromisoformat(wt[1][:10])
                rec = (today - d).days
            except (ValueError, TypeError):
                rec = 9999
            return {"source": "wallstreet_fmp", "target": float(wt[0]),
                    "recency_days": rec, "stance": None, "confidence": None}
    except sqlite3.OperationalError:
        pass
    return None


def compute(ticker: str, market: str | None = None,
            *, days_window: int = 365) -> dict | None:
    """Compose consensus from our_fair + house targets + WS.

    Returns full breakdown dict or None if no data.
    """
    if market is None:
        market = _detect_market(ticker)
    if market is None:
        return None
    db = DB_BR if market == "br" else DB_US

    with sqlite3.connect(db) as c:
        our_fair, consensus_fair, current_price = _our_fair(c, ticker)
        houses = _house_targets(c, ticker, days_window=days_window)
        ws = _wallstreet_target(c, ticker) if market == "us" else None

    sources_used: list[dict] = []
    if our_fair is not None:
        sources_used.append({
            "source": "our_fair", "target": our_fair,
            "recency_days": 0, "stance": None, "confidence": 1.0,
        })
    sources_used.extend(houses)
    if ws:
        sources_used.append(ws)

    if not sources_used:
        return None

    targets = [s["target"] for s in sources_used if s.get("target") is not None]
    if not targets:
        return None

    blended_median = median(targets)
    blended_mean = mean(targets)
    dispersion = (stdev(targets) / blended_mean) if (len(targets) > 1 and blended_mean > 0) else 0.0

    # Recency-weighted mean: weight = exp(-recency_days/90) * confidence
    import math as _math
    weights = []
    for s in sources_used:
        recency = s.get("recency_days") or 0
        conf = s.get("confidence") or 0.7  # default if not set
        w = _math.exp(-recency / 90.0) * conf
        weights.append(w)
    if sum(weights) > 0:
        weighted = sum(s["target"] * w for s, w in zip(sources_used, weights, strict=True)) / sum(weights)
    else:
        weighted = blended_mean

    return {
        "ticker": ticker, "market": market,
        "our_fair": our_fair,
        "consensus_fair": consensus_fair,
        "current_price": current_price,
        "n_sources": len(sources_used),
        "houses": [{k: v for k, v in s.items() if k != "_internal"} for s in sources_used],
        "blended": {
            "median": round(blended_median, 4),
            "mean": round(blended_mean, 4),
            "weighted": round(weighted, 4),
        },
        "dispersion": round(dispersion, 3),
        "upside_blended_pct": (
            round((blended_median / current_price - 1) * 100, 2)
            if current_price else None
        ),
        "computed_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def _print_report(r: dict) -> None:
    print(f"\n=== {r['ticker']} ({r['market'].upper()}) — Consensus Target ===")
    cur = r.get("current_price")
    cur_s = f"R${cur:.2f}" if r["market"] == "br" and cur else (f"${cur:.2f}" if cur else "—")
    print(f"  Current price: {cur_s}")
    print(f"  N sources: {r['n_sources']}")
    print()
    print(f"  {'Source':<22} {'Target':>10} {'Recency':>10} {'Stance':<10}")
    print(f"  {'-' * 56}")
    for h in r["houses"]:
        rec = h.get("recency_days")
        rec_s = f"{rec}d" if rec is not None else "—"
        stance = h.get("stance") or "—"
        target = h.get("target")
        target_s = f"{target:.2f}" if target else "—"
        print(f"  {h['source']:<22} {target_s:>10} {rec_s:>10} {stance:<10}")
    print()
    b = r["blended"]
    print(f"  Blended median:   {b['median']:.2f}")
    print(f"  Blended mean:     {b['mean']:.2f}")
    print(f"  Weighted (recency × conf):  {b['weighted']:.2f}")
    print(f"  Dispersion (σ/μ): {r['dispersion']:.2%}")
    if r.get("upside_blended_pct") is not None:
        sign = "+" if r["upside_blended_pct"] >= 0 else ""
        print(f"  Upside vs median: {sign}{r['upside_blended_pct']:.1f}%")


def _list_holdings() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ).fetchall()
        for (t,) in rows:
            out.append((t, market))
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--days-window", type=int, default=365)
    args = ap.parse_args()

    if args.ticker:
        r = compute(args.ticker.upper(), days_window=args.days_window)
        if r is None:
            print(f"{args.ticker}: no consensus data — no fair_value or no analyst targets")
            return 1
        if args.json:
            print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        else:
            _print_report(r)
        return 0

    targets = _list_holdings()
    print(f"Computing consensus for {len(targets)} holdings...")
    print()
    print(f"  {'Ticker':<8} {'Sources':<8} {'Median':>10} {'Weighted':>10} {'Cur':>10} {'Upside':>8}")
    print(f"  {'-' * 64}")
    found = 0
    for tk, mk in targets:
        try:
            r = compute(tk, mk, days_window=args.days_window)
            if r is None:
                continue
            cur = r.get("current_price") or 0
            up = r.get("upside_blended_pct") or 0
            up_s = f"{up:+.1f}%"
            print(f"  {tk:<8} {r['n_sources']:<8} {r['blended']['median']:>10.2f} "
                  f"{r['blended']['weighted']:>10.2f} {cur:>10.2f} {up_s:>8}")
            found += 1
        except Exception as e:  # noqa: BLE001
            print(f"  {tk:<8} ERROR — {e}")
    print(f"\n{found} tickers with consensus data; {len(targets) - found} skipped (no fair_value or no targets).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
