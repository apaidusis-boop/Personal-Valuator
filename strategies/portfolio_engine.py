"""Portfolio Engine — combines outputs across 5 strategy engines.

Pipeline:
  1. For each (engine, ticker) in scope, call engine.evaluate(ticker).
  2. Aggregate per-ticker score = SUM(bucket_weight × engine_score).
  3. Apply macro overlay (multiplier 0.5 / 1.0 / 1.5).
  4. Resolve conflicts (e.g. Graham BUY + DRIP AVOID).
  5. Layer hedge proposal (separate from per-ticker allocation).
  6. Output AllocationProposal.

Bucket weights (default — override via call):
  graham   25%  (deep value, BR-leaning)
  buffett  30%  (quality, US-leaning)
  drip     20%  (income safety)
  macro    15%  (top-down tilt)
  hedge    10%  (reserved for tactical hedge size, NOT per-ticker)
"""
from __future__ import annotations

import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from scoring.engine import DB_BR, DB_US
from strategies import buffett, drip, graham, hedge, macro
from strategies._base import AllocationProposal, StrategyOutput

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "config" / "universe.yaml"

DEFAULT_BUCKET_WEIGHTS = {
    "graham":  0.25,
    "buffett": 0.30,
    "drip":    0.20,
    "macro":   0.15,
    "hedge":   0.10,
}


def _ticker_universe(market: str) -> list[str]:
    if not UNIVERSE.exists():
        return []
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8")) or {}
    m = data.get(market, {}) or {}
    out: list[str] = []
    for bucket in ("holdings", "watchlist"):
        group = m.get(bucket) or {}
        if isinstance(group, list):
            for entry in group:
                if isinstance(entry, dict) and entry.get("ticker"):
                    out.append(entry["ticker"])
        else:
            for sublist in (group or {}).values():
                for entry in sublist or []:
                    if isinstance(entry, dict) and entry.get("ticker"):
                        out.append(entry["ticker"])
    return sorted(set(out))


def _engine_for_market(market: str) -> list:
    """Which engines apply per market.
    Graham only BR. Buffett only US. DRIP/Macro/Hedge both."""
    if market == "br":
        return [graham, drip, macro, hedge]
    return [buffett, drip, macro, hedge]


def _collect_scores(market: str, tickers: list[str]
                    ) -> dict[str, list[StrategyOutput]]:
    """For each engine applicable to market, evaluate every ticker.
    Returns {engine_name: [StrategyOutput, ...]}."""
    out: dict[str, list[StrategyOutput]] = {}
    for engine_mod in _engine_for_market(market):
        results = [engine_mod.evaluate(t, market) for t in tickers]
        out[engine_mod.name] = results
    return out


def _detect_conflicts(per_ticker: dict[str, list[StrategyOutput]]
                      ) -> list[dict[str, Any]]:
    """Surface tickers where engines strongly disagree (BUY vs AVOID)."""
    conflicts = []
    for ticker, outs in per_ticker.items():
        verdicts = {o.engine: o.verdict for o in outs}
        has_buy = any(v == "BUY" for v in verdicts.values())
        has_avoid = any(v == "AVOID" for v in verdicts.values())
        if has_buy and has_avoid:
            conflicts.append({
                "ticker": ticker,
                "verdicts": verdicts,
                "resolution": "averaged via bucket weights",
            })
    return conflicts


def combine(market: str = "us",
            tickers: list[str] | None = None,
            bucket_weights: dict[str, float] | None = None,
            apply_macro_overlay: bool = True,
            hedge_overlay: bool = True,
            top_n: int | None = None,
            ) -> AllocationProposal:
    """Run all engines for `market`, aggregate, and propose allocations.

    Args:
        market: 'br' or 'us'.
        tickers: override universe.
        bucket_weights: per-engine bucket; default DEFAULT_BUCKET_WEIGHTS.
        apply_macro_overlay: multiply target_weight by macro multiplier.
        hedge_overlay: include hedge proposal in output (does NOT subtract
            from target_weights — hedge is on top of equity allocation).
        top_n: keep only top N tickers (after macro overlay) in target_weights.
    """
    market = market.lower()
    weights = dict(bucket_weights or DEFAULT_BUCKET_WEIGHTS)
    # `tickers` may be explicitly [] (no universe) — distinguish from None.
    universe = tickers if tickers is not None else _ticker_universe(market)
    if not universe:
        return AllocationProposal(
            target_weights={}, per_engine={}, bucket_weights=weights,
            notes=[f"No tickers in universe for market={market}"],
        )

    per_engine_outputs = _collect_scores(market, universe)
    # build per-ticker lookup
    by_ticker: dict[str, list[StrategyOutput]] = defaultdict(list)
    for engine_name, outs in per_engine_outputs.items():
        for o in outs:
            by_ticker[o.ticker].append(o)

    # 1. raw composite score per ticker = sum(bucket_w × engine_score)
    raw_scores: dict[str, float] = {}
    for ticker, outs in by_ticker.items():
        s = 0.0
        for o in outs:
            # hedge engine doesn't contribute per-ticker score
            if o.engine == "hedge":
                continue
            bw = weights.get(o.engine, 0.0)
            s += bw * o.score
        raw_scores[ticker] = s

    # 2. apply macro overlay (multiplier 0.5/1.0/1.5)
    composite: dict[str, float] = {}
    for ticker, raw in raw_scores.items():
        mult = 1.0
        if apply_macro_overlay:
            macro_out = next(
                (o for o in by_ticker[ticker] if o.engine == "macro"), None
            )
            if macro_out is not None:
                mult = macro_out.rationale.get("multiplier", 1.0)
        composite[ticker] = round(raw * mult, 4)

    # 3. normalize to weights summing to 1.0 across BUY/HOLD candidates
    # candidates = those with composite > 0 AND not AVOID majority
    candidates: dict[str, float] = {}
    for ticker, score in composite.items():
        outs = by_ticker[ticker]
        avoid_count = sum(1 for o in outs if o.verdict == "AVOID")
        buy_count = sum(1 for o in outs if o.verdict == "BUY")
        # require at least one BUY across engines (avoids weight to all-AVOID tickers)
        if buy_count > 0 and score > 0:
            candidates[ticker] = score

    # rank + optional top_n
    ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    if top_n is not None:
        ranked = ranked[:top_n]

    total = sum(s for _, s in ranked) or 1.0
    target_weights = {t: round(s / total, 4) for t, s in ranked}

    # 4. conflicts surfaced for inspection
    conflicts = _detect_conflicts(by_ticker)

    # 5. macro + hedge overlays attached
    macro_meta = macro.current_regime(market)
    hedge_proposal = hedge.propose_hedge(market) if hedge_overlay else {}

    notes = [
        f"Universe size: {len(universe)} | candidates: {len(candidates)}",
        f"Bucket weights: {weights}",
        f"Macro regime: {macro_meta['regime']} ({macro_meta['confidence']})",
    ]
    if hedge_proposal.get("active"):
        notes.append(
            f"Tactical hedge active: {hedge_proposal['hedge_size_pct']:.0%} "
            f"via {', '.join(hedge_proposal['instruments'])} "
            "(applied on top of equity allocation, not subtracted)"
        )

    return AllocationProposal(
        target_weights=target_weights,
        per_engine=per_engine_outputs,
        bucket_weights=weights,
        conflicts=conflicts,
        macro_overlay=macro_meta,
        hedge_overlay=hedge_proposal,
        notes=notes,
    )


def main() -> int:
    import argparse
    import json
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--tickers", help="comma-separated override")
    ap.add_argument("--top", type=int, help="keep top N")
    ap.add_argument("--no-hedge", action="store_true")
    ap.add_argument("--no-macro", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    tickers = args.tickers.split(",") if args.tickers else None
    proposal = combine(
        market=args.market,
        tickers=tickers,
        top_n=args.top,
        apply_macro_overlay=not args.no_macro,
        hedge_overlay=not args.no_hedge,
    )
    if args.json:
        print(json.dumps(proposal.as_dict(), indent=2, default=str))
        return 0
    print(f"\n=== Allocation Proposal | market={args.market.upper()} ===")
    for note in proposal.notes:
        print(f"  {note}")
    print("\nTarget weights (top):")
    for t, w in sorted(proposal.target_weights.items(),
                       key=lambda x: x[1], reverse=True):
        print(f"  {t:<10} {w*100:>5.1f}%")
    if proposal.conflicts:
        print(f"\nConflicts ({len(proposal.conflicts)}):")
        for c in proposal.conflicts[:5]:
            print(f"  {c['ticker']}: {c['verdicts']}")
    if proposal.hedge_overlay.get("active"):
        h = proposal.hedge_overlay
        print(f"\nHedge: {h['hedge_size_pct']:.0%} via {', '.join(h['instruments'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
