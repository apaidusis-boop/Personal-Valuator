"""Round 1 / Round 2 prompts for council seats.

Each seat is a NAMED specialist (see `agents/council/roster.py::CouncilSeat`).
The prompt embeds:
  - Persona identity (employee_name + title)
  - Framework brief (what this specialist defends + their veto rules)
  - Dossier (factual layer, same for all)
  - In Round 2: peers' Round 1 statements, so each can challenge specific points

Same Pydantic schemas (CouncilOpening, CouncilResponse) as before — what
changed is *who* sits in the seat, not the shape of their output.
"""
from __future__ import annotations

from agents._llm import ollama_call_typed
from agents._schemas import CouncilOpening, CouncilResponse
from agents.council.roster import CouncilSeat

MODEL = "qwen2.5:14b-instruct-q4_K_M"


# ─────────────────────────────────────────────────────────────────────
# Round 1 — opening statement, blind to peers
# ─────────────────────────────────────────────────────────────────────

ROUND1_TASK = """TAREFA — Round 1 (opening statement, blind aos outros membros do council):

Lê o dossier. Produz a tua avaliação inicial NO TEU FRAME (não no frame deles).
Output JSON estrito:

{
  "headline": "1 frase (max 20 palavras) que captura a tua posição",
  "stance": "BUY" | "HOLD" | "AVOID" | "NEEDS_DATA",
  "main_argument": "2-3 frases de raciocínio (max 80 palavras) — cita números do dossier",
  "supporting_metrics": ["métrica 1 com número", "métrica 2", "métrica 3"],
  "concerns": ["o que me preocupa 1", "o que me preocupa 2"],
  "veto_signals": ["dado/método inválido — caso contrário lista vazia"]
}

Reply JSON ONLY — sem markdown, sem prose antes/depois."""


def _identity_block(seat: CouncilSeat) -> str:
    return f"""És **{seat.employee_name}** — {seat.title}.

Framework e regras que defendes:
{seat.framework_brief}

Tom: factual, denso, sem hype. Se os números não sustentam a tese, dizes isso
explicitamente. Se um colega aplica a métrica errada (ex: P/B em banco com
goodwill grande), levantas veto signal."""


def round1(seat: CouncilSeat, dossier_text: str, *, seed: int = 42) -> CouncilOpening | None:
    prompt = f"""{_identity_block(seat)}

DOSSIER (factual, mesmo para todos os membros do council):
{dossier_text}

{ROUND1_TASK}"""
    return ollama_call_typed(
        prompt,
        CouncilOpening,
        model=MODEL,
        max_tokens=600,
        temperature=0.2,
        seed=seed,
        timeout=180,
    )


# ─────────────────────────────────────────────────────────────────────
# Round 2 — response to peers, can revise stance
# ─────────────────────────────────────────────────────────────────────

ROUND2_TASK = """TAREFA — Round 2 (resposta aos outros membros do council):

Lês as opening statements deles abaixo. Agora podes:
- Concordar com pontos específicos (cite o membro pelo NOME)
- Desafiar pontos específicos (cite o membro + razão)
- Adicionar evidência nova que os outros não consideraram
- Rever a tua stance se a evidência deles te convencer (ou manter)

Output JSON estrito:

{
  "agree_with": ["citação curta + nome do colega que disse"],
  "challenge": ["citação + razão de discordância + nome do colega"],
  "new_evidence": "1 frase com algo que ninguém referiu (ou string vazia)",
  "revised_stance": "BUY" | "HOLD" | "AVOID" | "NEEDS_DATA"
}

Se não tens nada a adicionar a um campo, devolve lista vazia ou string vazia.
Reply JSON ONLY."""


def round2(
    seat: CouncilSeat,
    dossier_text: str,
    my_round1: CouncilOpening,
    peers: dict[str, tuple[CouncilSeat, CouncilOpening]],
    *,
    seed: int = 42,
) -> CouncilResponse | None:
    """peers: {role_key: (seat, opening)}"""
    peer_lines = []
    for role_key, (peer_seat, peer_op) in peers.items():
        peer_lines.append(f"--- **{peer_seat.employee_name}** ({peer_seat.title}) — {peer_op.stance} ---")
        peer_lines.append(f"Headline: {peer_op.headline}")
        peer_lines.append(f"Argument: {peer_op.main_argument}")
        if peer_op.concerns:
            peer_lines.append("Concerns: " + " | ".join(peer_op.concerns))
        if peer_op.veto_signals:
            peer_lines.append("VETO: " + " | ".join(peer_op.veto_signals))
        peer_lines.append("")
    peers_block = "\n".join(peer_lines)

    prompt = f"""{_identity_block(seat)}

DOSSIER (factual, mesmo de antes):
{dossier_text}

A TUA OPENING (Round 1):
Stance: {my_round1.stance}  |  Headline: {my_round1.headline}
Argument: {my_round1.main_argument}

OUTROS MEMBROS DO COUNCIL (Round 1):
{peers_block}

{ROUND2_TASK}"""
    return ollama_call_typed(
        prompt,
        CouncilResponse,
        model=MODEL,
        max_tokens=600,
        temperature=0.25,
        seed=seed,
        timeout=180,
    )
