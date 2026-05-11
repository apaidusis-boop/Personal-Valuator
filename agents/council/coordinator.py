"""Coordinator — runs the 2-round debate with NAMED specialists.

Pipeline:
  1. Build dossier (factual layer)
  2. Roster.assemble_council(dossier) → list of CouncilSeats with named employees
  3. Round 1: each seat writes opening, blind to peers
  4. Round 2: each seat reads peers' Round 1, can challenge / revise stance
  5. Synthesis: deterministic majority vote + LLM-prose summary preserves dissent
  6. Per-agent reviews written to obsidian_vault/agents/<Employee>/reviews/

Two refactors vs v1:
  - Seats are NAMED (Diego Bancário, Mariana Macro, etc.) — not anonymous roles
  - Each contributing specialist gets ONE review file in their personal folder
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date

from agents._llm import ollama_call_typed
from agents._schemas import (
    CouncilOpening,
    CouncilResponse,
    CouncilSynthesis,
)
from agents.council.agent_reviews import write_review
from agents.council.dossier import CouncilDossier, build_dossier
from agents.council.personas import round1, round2
from agents.council.roster import CouncilSeat, assemble_council

MODEL = "qwen2.5:14b-instruct-q4_K_M"


@dataclass
class CouncilRun:
    ticker: str
    market: str
    dossier: CouncilDossier
    seats: list[CouncilSeat] = field(default_factory=list)
    openings: dict[str, CouncilOpening] = field(default_factory=dict)  # keyed by role_key
    responses: dict[str, CouncilResponse] = field(default_factory=dict)
    seat_by_role: dict[str, CouncilSeat] = field(default_factory=dict)  # role_key → seat
    synthesis: CouncilSynthesis | None = None
    review_paths: list[str] = field(default_factory=list)
    elapsed_sec: float = 0.0
    failures: list[str] = field(default_factory=list)


def _role_key(seat: CouncilSeat, idx: int) -> str:
    """Unique key per seat (handles duplicate roles like sector_specialist_secondary)."""
    return f"{seat.role}_{idx}" if seat.role.endswith("_secondary") else seat.role


def _vote_majority(stances: list[str]) -> tuple[str, str]:
    """Macro Strategist explicitly NEUTRAL on rating — exclude from vote.
    NEEDS_DATA from any voice forces low confidence."""
    voting_stances = [s for s in stances if s in ("BUY", "HOLD", "AVOID", "NEEDS_DATA")]
    if not voting_stances:
        return "HOLD", "low"
    if "NEEDS_DATA" in voting_stances:
        return "NEEDS_DATA", "low"
    counts = {s: voting_stances.count(s) for s in set(voting_stances)}
    winner, n = max(counts.items(), key=lambda x: x[1])
    pct = n / len(voting_stances)
    if pct >= 0.99:
        return winner, "high"
    if pct >= 0.66:
        return winner, "medium"
    return winner, "low"


def _llm_synthesis(
    dossier_text: str,
    run: CouncilRun,
    voted_stance: str,
    voted_confidence: str,
) -> CouncilSynthesis | None:
    transcript_lines = []
    for role_key, op in run.openings.items():
        seat = run.seat_by_role[role_key]
        transcript_lines.append(f"\n--- {seat.employee_name} ({seat.title}) R1 [{op.stance}] ---")
        transcript_lines.append(f"Headline: {op.headline}")
        transcript_lines.append(f"Argument: {op.main_argument}")
        if op.supporting_metrics:
            transcript_lines.append("Metrics: " + " | ".join(op.supporting_metrics))
        if op.concerns:
            transcript_lines.append("Concerns: " + " | ".join(op.concerns))
        if op.veto_signals:
            transcript_lines.append("VETO: " + " | ".join(op.veto_signals))
    for role_key, resp in run.responses.items():
        seat = run.seat_by_role[role_key]
        transcript_lines.append(f"\n--- {seat.employee_name} R2 [{resp.revised_stance}] ---")
        if resp.agree_with:
            transcript_lines.append("Agreed: " + " | ".join(resp.agree_with))
        if resp.challenge:
            transcript_lines.append("Challenged: " + " | ".join(resp.challenge))
        if resp.new_evidence:
            transcript_lines.append(f"New evidence: {resp.new_evidence}")
    transcript = "\n".join(transcript_lines)

    prompt = f"""És o Council Coordinator. Lês o transcript de N voices em 2 rounds e
extrais a síntese ESTRUTURADA. NÃO inventas — só reorganizas o que está dito.
SEMPRE cita os colegas pelo NOME (não por role) — eles são pessoas, não funções.

DOSSIER (factual base):
{dossier_text[:1500]}

DEBATE TRANSCRIPT:
{transcript}

Voto majoritário já calculado deterministicamente:
  Final stance: {voted_stance}
  Confidence: {voted_confidence}

TAREFA: produz JSON estrito com:

{{
  "consensus_points": ["pontos onde 2+ pessoas concordam — cita facto + métrica + nomes"],
  "dissent_points": ["onde discordam — formato 'X disse A, Y disse B'"],
  "final_stance": "{voted_stance}",
  "confidence": "{voted_confidence}",
  "pre_publication_flags": ["o que o user TEM que ver antes da narrativa imprimir — vetos, dados ausentes, sizing red flags — atribui a quem flagou"],
  "sizing_recommendation": "1 frase concreta com range (vem do Capital Allocator se ele estava na sala)"
}}

Lista vazia se não houver. Reply JSON ONLY — zero markdown."""

    return ollama_call_typed(
        prompt,
        CouncilSynthesis,
        model=MODEL,
        max_tokens=900,
        temperature=0.15,
        seed=42,
        timeout=180,
    )


def run_council(
    ticker: str,
    market: str = "br",
    *,
    verbose: bool = True,
) -> CouncilRun:
    t0 = time.time()
    dossier = build_dossier(ticker, market)
    seats = assemble_council(dossier)

    if verbose:
        print(f"\n=== Council: {market.upper()}:{ticker} ===")
        print(f"  Modo: {dossier.modo}-{market.upper()} | Sector: {dossier.sector or '?'} | Held: {dossier.is_holding}")
        print(f"  Seats convocados ({len(seats)}):")
        for seat in seats:
            print(f"    · {seat.employee_name} — {seat.title}")

    run = CouncilRun(ticker=ticker, market=market, dossier=dossier, seats=seats)
    dossier_text = dossier.render_facts_block()

    # Build role_key → seat mapping
    for idx, seat in enumerate(seats):
        rk = _role_key(seat, idx)
        run.seat_by_role[rk] = seat

    # ── Round 1 ─────────────────────────────────────────────────
    if verbose:
        print("  Round 1 (openings, blind):")
    for rk, seat in run.seat_by_role.items():
        if verbose:
            print(f"    {seat.employee_name}...", end=" ", flush=True)
        op = round1(seat, dossier_text, seed=42)
        if op is None:
            run.failures.append(f"R1:{seat.employee_name}")
            if verbose:
                print("FAIL")
            continue
        run.openings[rk] = op
        if verbose:
            print(f"{op.stance}")

    if not run.openings:
        run.elapsed_sec = time.time() - t0
        return run

    # ── Round 2 ─────────────────────────────────────────────────
    if verbose:
        print("  Round 2 (responses, peers visible):")
    for rk, seat in run.seat_by_role.items():
        if rk not in run.openings:
            continue
        peers = {
            other_rk: (run.seat_by_role[other_rk], run.openings[other_rk])
            for other_rk in run.openings
            if other_rk != rk
        }
        if not peers:
            continue
        if verbose:
            print(f"    {seat.employee_name}...", end=" ", flush=True)
        resp = round2(seat, dossier_text, run.openings[rk], peers, seed=42)
        if resp is None:
            run.failures.append(f"R2:{seat.employee_name}")
            if verbose:
                print("FAIL")
            continue
        run.responses[rk] = resp
        if verbose:
            print(f"{resp.revised_stance}")

    # ── Synthesis ────────────────────────────────────────────────
    # Macro strategist intentionally not voting on rating
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
            pre_publication_flags=["LLM synthesis failed — manual review of transcript needed"],
        )
    else:
        syn.final_stance = voted_stance  # type: ignore[assignment]
        syn.confidence = voted_conf  # type: ignore[assignment]
    run.synthesis = syn

    # ── Per-agent reviews ────────────────────────────────────────
    if verbose:
        print("  Writing per-agent reviews:")
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
            if verbose:
                print(f"    · {seat.employee_name} → {path.parent.parent.name}/{path.parent.name}/{path.name}")
        except Exception as e:
            run.failures.append(f"review:{seat.employee_name}: {type(e).__name__}")

    run.elapsed_sec = time.time() - t0
    if verbose:
        print(f"  Synthesis: {syn.final_stance} ({syn.confidence})  elapsed: {run.elapsed_sec:.1f}s")
    return run
