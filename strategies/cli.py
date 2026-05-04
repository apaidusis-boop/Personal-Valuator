"""Unified strategy CLI: ii strategy <engine> <ticker> [--market X]

Examples:
    ii strategy graham PETR4
    ii strategy buffett JNJ --market us
    ii strategy drip KO
    ii strategy macro AAPL
    ii strategy hedge --market us         # no ticker, just status
    ii strategy all KO                    # run every applicable engine
"""
from __future__ import annotations

import argparse
import json
import sys

from strategies import buffett, drip, graham, hedge, macro
from strategies._base import StrategyOutput

ENGINES = {
    "graham": graham,
    "buffett": buffett,
    "drip": drip,
    "macro": macro,
    "hedge": hedge,
}


def _print_output(o: StrategyOutput) -> None:
    print(f"\n[{o.engine.upper()}] {o.ticker} ({o.market}):")
    print(f"  verdict: {o.verdict}    score: {o.score}")
    if o.weight_suggestion:
        print(f"  weight_suggestion: {o.weight_suggestion}")
    if o.message:
        print(f"  msg: {o.message}")
    if o.rationale:
        rat_str = json.dumps(o.rationale, default=str, indent=2, ensure_ascii=False)
        for line in rat_str.split("\n")[:30]:
            print(f"    {line}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("engine", choices=list(ENGINES.keys()) + ["all"],
                    help="strategy engine name")
    ap.add_argument("ticker", nargs="?", help="ticker (optional for hedge)")
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.engine == "hedge" and not args.ticker:
        # Hedge engine + no ticker = just status
        print(hedge.status(args.market))
        return 0

    if not args.ticker:
        ap.error("ticker required (except for 'hedge' standalone)")

    if args.engine == "all":
        results = []
        for name, mod in ENGINES.items():
            r = mod.evaluate(args.ticker, args.market)
            results.append(r)
        if args.json:
            print(json.dumps([r.as_dict() for r in results], indent=2, default=str))
        else:
            for r in results:
                _print_output(r)
        return 0

    mod = ENGINES[args.engine]
    out = mod.evaluate(args.ticker, args.market)
    if args.json:
        print(json.dumps(out.as_dict(), indent=2, default=str))
    else:
        _print_output(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
