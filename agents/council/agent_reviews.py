"""Per-agent review writer.

When the Council debates a ticker, each contributing specialist gets ONE
review file in their personal folder. This makes the work visible per
specialist (cf. user request: "ITSA foi conversada entre Bancos e Macro,
fica ligada aos agentes").

Writes to:
  obsidian_vault/agents/<Employee Name>/reviews/<TICKER>_<DATE>.md

Each review:
  - Frontmatter: agent, employee, ticker, date, role, stance_round1, stance_round2
  - Round 1 statement (own opening)
  - Round 2 statement (response to peers, with names)
  - Backlinks: dossier, council transcript, other specialists in the room

The agent index is also updated automatically (a `_reviews_index.md` per agent).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from agents._schemas import CouncilOpening, CouncilResponse
from agents.council.roster import CouncilSeat

ROOT = Path(__file__).resolve().parents[2]
VAULT_AGENTS = ROOT / "obsidian_vault" / "agents"


def _agent_dir(employee_name: str) -> Path:
    """One folder per specialist. Folder name = employee_name as-is (matches persona MDs)."""
    p = VAULT_AGENTS / employee_name
    (p / "reviews").mkdir(parents=True, exist_ok=True)
    return p


def _stance_emoji(stance: str) -> str:
    return {"BUY": "🟢", "HOLD": "🟡", "AVOID": "🔴", "NEEDS_DATA": "⚪"}.get(stance, "?")


def write_review(
    seat: CouncilSeat,
    ticker: str,
    market: str,
    opening: CouncilOpening,
    response: CouncilResponse | None,
    other_seats: list[CouncilSeat],
    *,
    review_date: date | None = None,
) -> Path:
    review_date = review_date or date.today()
    agent_dir = _agent_dir(seat.employee_name)
    out = agent_dir / "reviews" / f"{ticker}_{review_date.isoformat()}.md"

    flip = ""
    if response and response.revised_stance != opening.stance:
        flip = f" *(R1 era {opening.stance})*"

    other_links = []
    for s in other_seats:
        if s.employee_name == seat.employee_name:
            continue
        other_links.append(f"[[{s.employee_name}]] ({s.title})")

    lines: list[str] = []
    lines += [
        "---",
        "type: agent_review",
        f"agent: {seat.agent_slug}",
        f"employee: {seat.employee_name}",
        f"role: {seat.role}",
        f"ticker: {ticker}",
        f"market: {market}",
        f"date: {review_date.isoformat()}",
        f"stance_round1: {opening.stance}",
        f"stance_round2: {response.revised_stance if response else 'N/A'}",
        f"flipped: {str(bool(response and response.revised_stance != opening.stance)).lower()}",
        "tags: [agent_review, council]",
        "---",
        "",
        f"# {seat.employee_name} sobre [[{ticker}_STORY|{ticker}]]",
        "",
        f"**Função no debate**: {seat.title} (`{seat.role}`)  ",
        f"**Data**: {review_date.isoformat()}  ",
        f"**Stance final**: {_stance_emoji(response.revised_stance if response else opening.stance)} **{response.revised_stance if response else opening.stance}**{flip}  ",
        "",
        "## Round 1 — Abertura (cega aos colegas)",
        "",
    ]
    if opening.headline:
        lines.append(f"> _{opening.headline}_")
        lines.append("")
    if opening.main_argument:
        lines.append(opening.main_argument)
        lines.append("")
    if opening.supporting_metrics:
        lines.append("**Métricas que invoquei**:")
        for m in opening.supporting_metrics:
            lines.append(f"- {m}")
        lines.append("")
    if opening.concerns:
        lines.append("**Preocupações**:")
        for c in opening.concerns:
            lines.append(f"- {c}")
        lines.append("")
    if opening.veto_signals:
        lines.append("**Veto signals**:")
        for v in opening.veto_signals:
            lines.append(f"- 🚫 {v}")
        lines.append("")

    if response:
        lines.append("## Round 2 — Resposta aos colegas")
        lines.append("")
        if response.agree_with:
            lines.append("**Concordei com**:")
            for a in response.agree_with:
                lines.append(f"- {a}")
            lines.append("")
        if response.challenge:
            lines.append("**Desafiei**:")
            for c in response.challenge:
                lines.append(f"- {c}")
            lines.append("")
        if response.new_evidence:
            lines.append(f"**Evidência nova**: {response.new_evidence}")
            lines.append("")
    else:
        lines.append("## Round 2")
        lines.append("")
        lines.append("_(Não respondi nesta ronda — falha na chamada do modelo.)_")
        lines.append("")

    lines.append("## Quem mais estava na sala")
    lines.append("")
    if other_links:
        for link in other_links:
            lines.append(f"- {link}")
    else:
        lines.append("_Estive sozinho neste debate._")
    lines.append("")

    lines.append("## Documentos relacionados")
    lines.append("")
    lines.append(f"- [[{ticker}_STORY|📖 Storytelling completo (8 actos)]]")
    lines.append(f"- [[{ticker}_COUNCIL|🏛️ Transcript do Council debate]]")
    lines.append(f"- [[{seat.employee_name}|👤 Minha página de persona]]")
    lines.append("")
    lines.append("---")
    lines.append(f"*Gerado pelo Council `{review_date.isoformat()}` — STORYT_2.0 Camada 5.5*")

    out.write_text("\n".join(lines), encoding="utf-8")

    # Update reviews index
    _update_reviews_index(seat.employee_name)
    return out


def _update_reviews_index(employee_name: str) -> None:
    """Write _reviews_index.md per specialist with Dataview-style table fallback."""
    agent_dir = VAULT_AGENTS / employee_name
    reviews_dir = agent_dir / "reviews"
    if not reviews_dir.exists():
        return

    review_files = sorted(reviews_dir.glob("*_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    lines = [
        "---",
        "type: agent_reviews_index",
        f"agent: {employee_name}",
        "tags: [moc, agent_reviews]",
        "---",
        "",
        f"# Revisões feitas por {employee_name}",
        "",
        f"_{len(review_files)} revisões registadas._",
        "",
        "## Lista (mais recentes primeiro)",
        "",
    ]

    if review_files:
        lines.append("| Data | Ticker | Stance R1 | Stance R2 | Flipped |")
        lines.append("|---|---|---|---|---|")
        for p in review_files:
            try:
                txt = p.read_text(encoding="utf-8")
            except Exception:
                continue
            r1 = "?"
            r2 = "?"
            flipped = "?"
            ticker = p.stem.split("_")[0]
            review_date_str = "_".join(p.stem.split("_")[1:])
            for line in txt.split("\n")[:20]:
                if line.startswith("stance_round1:"):
                    r1 = line.split(":", 1)[1].strip()
                elif line.startswith("stance_round2:"):
                    r2 = line.split(":", 1)[1].strip()
                elif line.startswith("flipped:"):
                    flipped = line.split(":", 1)[1].strip()
            lines.append(f"| {review_date_str} | [[{p.stem}\\|{ticker}]] | {r1} | {r2} | {flipped} |")
    else:
        lines.append("_Nenhuma revisão ainda._")

    lines.append("")
    lines.append("## Persona")
    lines.append("")
    lines.append(f"- [[personas/{employee_name}|👤 Página de persona]]")

    (agent_dir / "_reviews_index.md").write_text("\n".join(lines), encoding="utf-8")
