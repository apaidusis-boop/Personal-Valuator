"""CLI entry: python -m agents.council <TICKER> [--market br|us]"""
from __future__ import annotations

import argparse
import sys

from agents.council.coordinator import run_council
from agents.council.render import write_outputs


def main() -> int:
    ap = argparse.ArgumentParser(
        description="STORYT_2.0 Council — 3-voice debate before narrative",
    )
    ap.add_argument("ticker", help="Ticker (BR sem .SA, US como is)")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--quiet", action="store_true", help="suppress per-step prints")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

    run = run_council(args.ticker.upper(), args.market, verbose=not args.quiet)
    md_path, json_path = write_outputs(run)

    print(f"\nMD : {md_path}")
    print(f"JSON: {json_path}")
    if run.synthesis:
        print(f"Final: {run.synthesis.final_stance} ({run.synthesis.confidence})")
        if run.synthesis.pre_publication_flags:
            print("Pre-publication flags:")
            for f in run.synthesis.pre_publication_flags:
                print(f"  ⚠️  {f}")
    if run.failures:
        print(f"Failures: {', '.join(run.failures)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
