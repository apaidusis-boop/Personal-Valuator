"""Council transcript renderer — uses NAMED specialists with wikilinks.

Each contributor in the transcript is shown as `[[Employee Name]]` so the
Obsidian vault links the dossier back to their persona page and review folder.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from agents.council.coordinator import CouncilRun

ROOT = Path(__file__).resolve().parents[2]
DOSSIERS_DIR = ROOT / "obsidian_vault" / "dossiers"


_STANCE_EMOJI = {"BUY": "🟢", "HOLD": "🟡", "AVOID": "🔴", "NEEDS_DATA": "⚪"}


def _stance_pill(stance: str) -> str:
    return f"{_STANCE_EMOJI.get(stance, '?')} **{stance}**"


def _wikilink(employee_name: str) -> str:
    return f"[[{employee_name}]]"


def render_markdown(run: CouncilRun) -> str:
    d = run.dossier
    syn = run.synthesis
    today = date.today().isoformat()

    lines: list[str] = []
    lines += [
        "---",
        "type: council_dossier",
        f"ticker: {d.ticker}",
        f"market: {d.market}",
        f"modo: {d.modo}",
        f"is_holding: {str(d.is_holding).lower()}",
        f"date: {today}",
        f"final_stance: {syn.final_stance if syn else 'NEEDS_DATA'}",
        f"confidence: {syn.confidence if syn else 'low'}",
        f"specialists: [{', '.join(s.employee_name for s in run.seats)}]",
        f"elapsed_sec: {run.elapsed_sec:.1f}",
        "tags: [council, storyt2, debate]",
        "---",
        "",
        f"# Council Debate — [[{d.ticker}_STORY|{d.ticker}]] ({d.name or '?'})",
        "",
        f"**Final stance**: {_stance_pill(syn.final_stance if syn else 'NEEDS_DATA')}  ",
        f"**Confidence**: `{syn.confidence if syn else 'low'}`  ",
        f"**Modo (auto)**: {d.modo} ({d.market.upper()})  |  **Sector**: {d.sector or '?'}  |  **Held**: {'sim' if d.is_holding else 'não'}  ",
        f"**Elapsed**: {run.elapsed_sec:.1f}s  |  **Failures**: {len(run.failures)}",
        "",
        "## Quem esteve na sala",
        "",
    ]
    for seat in run.seats:
        bullet = f"- {_wikilink(seat.employee_name)} — _{seat.title}_ (`{seat.role}`)"
        lines.append(bullet)
    lines.append("")

    if syn:
        lines.append("## Síntese")
        lines.append("")
        if syn.consensus_points:
            lines.append("**Consenso**:")
            for p in syn.consensus_points:
                lines.append(f"- {p}")
            lines.append("")
        if syn.dissent_points:
            lines.append("**Dissenso (preservado)**:")
            for p in syn.dissent_points:
                lines.append(f"- {p}")
            lines.append("")
        if syn.pre_publication_flags:
            lines.append("**Pre-publication flags** (rever antes de qualquer narrativa imprimir):")
            for p in syn.pre_publication_flags:
                lines.append(f"- ⚠️ {p}")
            lines.append("")
        if syn.sizing_recommendation:
            lines.append(f"**Sizing**: {syn.sizing_recommendation}")
            lines.append("")

    lines.append("## Round 1 — Opening Statements (blind)")
    lines.append("")
    for rk, op in run.openings.items():
        seat = run.seat_by_role.get(rk)
        if not seat:
            continue
        lines.append(f"### {_wikilink(seat.employee_name)} — {_stance_pill(op.stance)}")
        lines.append(f"_{seat.title}_")
        lines.append("")
        if op.headline:
            lines.append(f"**Headline**: _{op.headline}_")
            lines.append("")
        if op.main_argument:
            lines.append(op.main_argument)
            lines.append("")
        if op.supporting_metrics:
            lines.append("**Métricas**:")
            for m in op.supporting_metrics:
                lines.append(f"- {m}")
            lines.append("")
        if op.concerns:
            lines.append("**Preocupações**:")
            for c in op.concerns:
                lines.append(f"- {c}")
            lines.append("")
        if op.veto_signals:
            lines.append("**Veto signals**:")
            for v in op.veto_signals:
                lines.append(f"- 🚫 {v}")
            lines.append("")

    lines.append("## Round 2 — Respostas (peers visíveis)")
    lines.append("")
    for rk, resp in run.responses.items():
        seat = run.seat_by_role.get(rk)
        op = run.openings.get(rk)
        if not seat:
            continue
        original = op.stance if op else "?"
        revised = resp.revised_stance
        flip = " *(stance flipped)*" if op and original != revised else ""
        lines.append(f"### {_wikilink(seat.employee_name)} — {_stance_pill(revised)}{flip}")
        lines.append(f"_{seat.title}_")
        lines.append("")
        if resp.agree_with:
            lines.append("**Concordou com**:")
            for a in resp.agree_with:
                lines.append(f"- {a}")
            lines.append("")
        if resp.challenge:
            lines.append("**Desafiou**:")
            for c in resp.challenge:
                lines.append(f"- {c}")
            lines.append("")
        if resp.new_evidence:
            lines.append(f"**Evidência nova**: {resp.new_evidence}")
            lines.append("")

    lines.append("## Documentos relacionados")
    lines.append("")
    lines.append(f"- [[{d.ticker}_STORY|📖 Storytelling completo (8 actos)]]")
    lines.append("- Reviews individuais por especialista:")
    for seat in run.seats:
        lines.append(f"  - [[{d.ticker}_{date.today().isoformat()}|{seat.employee_name}]] em [[{seat.employee_name}]]/reviews/")
    lines.append("")

    lines.append("## Dossier (factual base — same input para todos)")
    lines.append("")
    lines.append("```")
    lines.append(d.render_facts_block())
    lines.append("```")
    lines.append("")
    if run.failures:
        lines.append("## Failures")
        lines.append("")
        for f in run.failures:
            lines.append(f"- ❌ {f}")
        lines.append("")
    lines.append("---")
    lines.append("*STORYT_2.0 Council · 100% Ollama local · zero Claude tokens*")
    return "\n".join(lines)


def write_outputs(run: CouncilRun) -> tuple[Path, Path]:
    DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = DOSSIERS_DIR / f"{run.ticker}_COUNCIL.md"
    json_path = DOSSIERS_DIR / f"{run.ticker}_COUNCIL.json"

    md_path.write_text(render_markdown(run), encoding="utf-8")

    payload = {
        "ticker": run.ticker,
        "market": run.market,
        "modo": run.dossier.modo,
        "sector": run.dossier.sector,
        "is_holding": run.dossier.is_holding,
        "seats": [
            {
                "role": s.role,
                "employee_name": s.employee_name,
                "agent_slug": s.agent_slug,
                "title": s.title,
            }
            for s in run.seats
        ],
        "openings": {k: v.model_dump() for k, v in run.openings.items()},
        "responses": {k: v.model_dump() for k, v in run.responses.items()},
        "synthesis": run.synthesis.model_dump() if run.synthesis else None,
        "review_paths": run.review_paths,
        "failures": run.failures,
        "elapsed_sec": run.elapsed_sec,
        "date": date.today().isoformat(),
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return md_path, json_path
