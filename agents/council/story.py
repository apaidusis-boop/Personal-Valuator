"""End-to-end pipeline: Council debate → Narrative Engine.

Smart cache (STORYT_3.0 follow-up):
  - Builds dossier first (cheap — DB queries + cached APIs).
  - Computes fingerprint of materially-significant features.
  - If matches latest prior snapshot → SKIP full pipeline, emit minimal delta.
  - Otherwise → run full council + narrative.

Usage:
    python -m agents.council.story POMO3 --market br
    python -m agents.council.story POMO3 --market br --no-cache  # force full run

Produces:
  obsidian_vault/dossiers/<TICKER>_COUNCIL.{md,json}   (Camada 5.5)
  obsidian_vault/dossiers/<TICKER>_STORY.md            (Camada 6 — 8-act)
  obsidian_vault/dossiers/archive/<TICKER>_STORY_<DATE>.md
  obsidian_vault/dossiers/<TICKER>_DELTA_<DATE>.md     (if prior exists)
  data/dossier_snapshots/<TICKER>/<DATE>.json
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import date

from agents.council.cache_policy import compute_fingerprint, decide, emit_no_change_delta
from agents.council.coordinator import run_council
from agents.council.dossier import build_dossier
from agents.council.narrative import render_story
from agents.council.render import write_outputs


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Council + Narrative end-to-end (STORYT_3.0 with smart cache)",
    )
    ap.add_argument("ticker", help="Ticker (BR sem .SA, US como is)")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-cache", action="store_true",
                    help="Bypass smart cache; always do full council + narrative")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

    ticker = args.ticker.upper()
    market = args.market
    verbose = not args.quiet
    t0 = time.time()

    # Step 1 — Build dossier (cheap; ~5-25s depending on cache state)
    if verbose:
        print(f"\n=== {market.upper()}:{ticker} ===")
        print("[1/3] Building dossier (research brief + peer benchmark + scores)...")
    dossier = build_dossier(ticker, market)
    dossier_time = time.time() - t0
    if verbose:
        print(f"    Dossier ready in {dossier_time:.1f}s")
        if dossier.research_brief:
            print(f"    Research hits: analyst={len(dossier.research_brief.analyst_hits)} "
                  f"event={len(dossier.research_brief.event_hits)} "
                  f"video={len(dossier.research_brief.video_hits)} "
                  f"biblio={len(dossier.research_brief.bibliotheca_hits)} "
                  f"tavily_news={len(dossier.research_brief.tavily_news_hits)}")

    # Step 2 — Smart cache decision
    if not args.no_cache:
        if verbose:
            print("[2/3] Checking smart cache...")
        decision = decide(dossier, run_date=date.today())
        if verbose:
            print(f"    Decision: {decision.action} — {decision.reason}")

        if decision.action == "skip":
            delta_path = emit_no_change_delta(
                ticker, market, decision.fingerprint, decision.prior_date,
            )
            total = time.time() - t0
            if verbose:
                print(f"\n[SKIP] No material change since {decision.prior_date}.")
                print(f"       Delta: {delta_path.name}")
                print(f"       Total: {total:.1f}s (saved ~95s vs full run)")
            return 0

        if decision.action == "partial":
            if verbose:
                print(f"    (Partial mode not yet implemented — falling through to full)")
            # TODO: implement partial mode (Risk Officer only refresh)
            # For now, partial → full
    else:
        if verbose:
            print("[2/3] Smart cache bypassed (--no-cache)")

    # Step 3 — Full council + narrative
    if verbose:
        print("[3/3] Running council + narrative...")

    # Inject existing dossier into run_council (avoids rebuilding)
    from agents.council.coordinator import CouncilRun
    from agents.council.coordinator import _role_key, _vote_majority, _llm_synthesis
    from agents.council.personas import round1, round2
    from agents.council.roster import assemble_council
    from agents.council.agent_reviews import write_review
    from agents._schemas import CouncilSynthesis

    seats = assemble_council(dossier)
    if verbose:
        print(f"    Seats convocados ({len(seats)}):")
        for seat in seats:
            print(f"      · {seat.employee_name} — {seat.title}")

    run = CouncilRun(ticker=ticker, market=market, dossier=dossier, seats=seats)
    dossier_text = dossier.render_facts_block()
    for idx, seat in enumerate(seats):
        rk = _role_key(seat, idx)
        run.seat_by_role[rk] = seat

    if verbose:
        print("    Round 1 (openings, blind):")
    for rk, seat in run.seat_by_role.items():
        if verbose:
            print(f"      {seat.employee_name}...", end=" ", flush=True)
        op = round1(seat, dossier_text, seed=42)
        if op is None:
            run.failures.append(f"R1:{seat.employee_name}")
            if verbose: print("FAIL")
            continue
        run.openings[rk] = op
        if verbose: print(f"{op.stance}")

    if verbose:
        print("    Round 2 (responses):")
    for rk, seat in run.seat_by_role.items():
        if rk not in run.openings:
            continue
        peers = {
            other_rk: (run.seat_by_role[other_rk], run.openings[other_rk])
            for other_rk in run.openings if other_rk != rk
        }
        if not peers:
            continue
        if verbose:
            print(f"      {seat.employee_name}...", end=" ", flush=True)
        resp = round2(seat, dossier_text, run.openings[rk], peers, seed=42)
        if resp is None:
            run.failures.append(f"R2:{seat.employee_name}")
            if verbose: print("FAIL")
            continue
        run.responses[rk] = resp
        if verbose: print(f"{resp.revised_stance}")

    voting_responses = [
        (rk, resp) for rk, resp in run.responses.items()
        if run.seat_by_role[rk].role != "macro_strategist"
    ]
    final_stances = [resp.revised_stance for _, resp in voting_responses]
    voted_stance, voted_conf = _vote_majority(final_stances)

    syn = _llm_synthesis(dossier_text, run, voted_stance, voted_conf)
    if syn is None:
        syn = CouncilSynthesis(
            final_stance=voted_stance,  # type: ignore[arg-type]
            confidence=voted_conf,  # type: ignore[arg-type]
            pre_publication_flags=["LLM synthesis failed — manual review needed"],
        )
    else:
        syn.final_stance = voted_stance  # type: ignore[assignment]
        syn.confidence = voted_conf  # type: ignore[assignment]
    run.synthesis = syn

    if verbose:
        print("    Writing per-agent reviews:")
    today = date.today()
    for rk, seat in run.seat_by_role.items():
        opening = run.openings.get(rk)
        if opening is None:
            continue
        response = run.responses.get(rk)
        other_seats = [s for k, s in run.seat_by_role.items() if k != rk]
        try:
            path = write_review(seat, ticker, market, opening, response, other_seats, review_date=today)
            run.review_paths.append(str(path))
        except Exception as e:
            run.failures.append(f"review:{seat.employee_name}: {type(e).__name__}")

    run.elapsed_sec = time.time() - t0
    council_md, council_json = write_outputs(run)
    if verbose:
        print(f"    Council: {syn.final_stance} ({syn.confidence})")
        print(f"    Council outputs: {council_md.name}, {council_json.name}")

    if not run.synthesis:
        if verbose: print("[council] No synthesis — narrative skipped.")
        return 1

    narrative = render_story(run, verbose=verbose)
    total = time.time() - t0
    if verbose:
        print()
        print(f"[narrative] {narrative.md_path.name}  ({narrative.elapsed_sec:.1f}s)")
        print(f"[total] {total:.1f}s end-to-end")
        print(f"\nFull dossier: {narrative.md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
