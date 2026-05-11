"""ii crew — multi-agent crew designer (EE.9 / OpenClaw "Multi Agent Framework").

Audita o estado actual:
  - Quem já está em config/agents.yaml (12 perpetuums + Antonio Carlos)
  - Que modelos Ollama estão instalados
  - Schedules + reports_to (org chart)
  - Que gaps existem no fluxo (no editor de conteúdo, no security check, etc.)

Propõe:
  - Crew dimensionado (3-7 specialists adicionais OU consolidação dos existentes)
  - Para cada novo agente: name / role / model_tier / model_recommendation /
    local_or_cloud / cadence / monthly_cost_estimate / rationale
  - Privacy gates: o que tem de ficar local
  - Output: vault/skills/Crew_Design.md

Uso:
    ii crew                  # imprime + escreve vault
    ii crew --dry-run        # imprime só
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CREW_OUT = ROOT / "obsidian_vault" / "skills" / "Crew_Design.md"


@dataclass
class CrewMember:
    name: str
    role: str
    model_tier: str            # flagship / mid / lightweight
    model: str                 # specific model id
    local_or_cloud: str        # local / cloud / hybrid
    cadence: str               # daily:HH:MM / weekly:DOW:HH / every:Nm / manual
    monthly_cost_usd: float    # estimate
    rationale: str
    why_now: str = ""
    privacy_required: bool = False


def _ollama_models() -> list[str]:
    try:
        r = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
        if r.returncode != 0:
            return []
        lines = (r.stdout or "").strip().split("\n")[1:]
        return [line.split()[0] for line in lines if line.strip()]
    except Exception:
        return []


def _existing_agents() -> list[dict]:
    """Read existing agents.yaml — minimal parser (mirror lib/agents.ts)."""
    p = ROOT / "config" / "agents.yaml"
    if not p.exists():
        return []
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        return data.get("agents", [])
    except ImportError:
        return []


def design_crew() -> list[CrewMember]:
    """Propose new crew members based on existing gaps."""
    existing = {a.get("name"): a for a in _existing_agents()}
    have_models = _ollama_models()
    has_32b = any("qwen2.5:32b" in m for m in have_models)
    has_70b = any(("llama3.3:70b" in m) or ("qwen2.5:72b" in m) for m in have_models)

    crew: list[CrewMember] = []

    # 1. Security Auditor — daily 11pm, log to alerts file (OpenClaw video has this)
    if "security_auditor" not in existing:
        crew.append(CrewMember(
            name="security_auditor",
            role="Security Officer — daily audit",
            model_tier="lightweight",
            model="qwen2.5:14b-instruct-q4_K_M",
            local_or_cloud="local",
            cadence="daily:23:00",
            monthly_cost_usd=0.0,
            rationale=(
                "Audita o stack: secrets em git history, perms .env, "
                ".gitignore coverage, API keys em logs. Posta para Telegram "
                "se houver issue."
            ),
            why_now=(
                "OpenClaw setup video flagged como passo crítico. Damos "
                "Tavily key + Telegram token + Polygon — qualquer leak é grave."
            ),
            privacy_required=True,
        ))

    # 2. Earnings Producer — orchestrate ii deepdive on upcoming earnings tickers
    if "earnings_producer" not in existing:
        crew.append(CrewMember(
            name="earnings_producer",
            role="Earnings Pre-Call Producer",
            model_tier="mid",
            model="qwen2.5:32b-instruct-q4_K_M" if has_32b else "qwen2.5:14b-instruct-q4_K_M",
            local_or_cloud="local",
            cadence="daily:18:00",
            monthly_cost_usd=0.0,
            rationale=(
                "Lê earnings_calendar holdings; qualquer ticker com ER em "
                "<7 dias dispara: ii deepdive --no-llm + variant_perception. "
                "Output em vault/dashboards/Earnings_Pipeline.md."
            ),
            why_now=(
                "Phase AA earnings_prep existe mas é manual. Producer fecha o loop."
            ),
            privacy_required=False,
        ))

    # 3. Content Curator — gera Topic Watchlist + Bibliotheca digest semanal
    if "content_curator" not in existing:
        crew.append(CrewMember(
            name="content_curator",
            role="Content Curator — Topic Watchlist scorer",
            model_tier="lightweight",
            model="qwen2.5:14b-instruct-q4_K_M",
            local_or_cloud="local",
            cadence="every:6h",
            monthly_cost_usd=0.0,
            rationale=(
                "Re-corre analytics.topic_scorer + gera markdown vault para "
                "topics 'Make Now'. Cross-references holdings em Topic Watchlist."
            ),
            why_now=(
                "EE.8 criou topic_scorer mas falta scheduler. Sem isto, "
                "scores ficam stale e Mission Control mente."
            ),
            privacy_required=False,
        ))

    # 4. Strategist Premium — só se 70B instalado
    if "strategist_premium" not in existing and has_70b:
        crew.append(CrewMember(
            name="strategist_premium",
            role="Senior Equity Analyst — Llama 70B dossier",
            model_tier="flagship",
            model="llama3.3:70b",
            local_or_cloud="local",
            cadence="manual",
            monthly_cost_usd=0.0,
            rationale=(
                "Quando o founder pede 'ii deepdive X --save-obsidian', usa "
                "70B para o dossier 5k palavras (DuPont + bear/bull + Lynch). "
                "32B para o resto."
            ),
            why_now="Llama 3.3 70B detectado em Ollama.",
            privacy_required=True,
        ))
    elif "strategist_premium" not in existing:
        crew.append(CrewMember(
            name="strategist_premium",
            role="Senior Equity Analyst (PENDING — pull 70B)",
            model_tier="flagship",
            model="llama3.3:70b (não instalado)",
            local_or_cloud="local",
            cadence="manual",
            monthly_cost_usd=0.0,
            rationale=(
                "Pull do modelo: ollama pull llama3.3:70b (~40GB). Antes disso "
                "o ii deepdive cai-back para 32B. Strategist fica desactivado."
            ),
            why_now="Hardware (5090) suporta. 32B é OK, 70B é melhor.",
            privacy_required=True,
        ))

    # 5. Dossier Reviewer — Synthetic IC critic on auto_draft theses
    if "dossier_reviewer" not in existing:
        crew.append(CrewMember(
            name="dossier_reviewer",
            role="Dossier Reviewer — auto_draft critic",
            model_tier="mid",
            model="qwen2.5:32b-instruct-q4_K_M" if has_32b else "qwen2.5:14b-instruct-q4_K_M",
            local_or_cloud="local",
            cadence="weekly:wed:10:00",
            monthly_cost_usd=0.0,
            rationale=(
                "Lê wiki/holdings com auto_draft:true (Phase I); aplica "
                "synthetic_ic compressed (3 personas) para flagar dossiers fracos. "
                "Output: lista de quem precisa rewrite humano."
            ),
            why_now=(
                "Phase I gerou 10 stubs; ainda não foram revistos. Sem reviewer, "
                "auto_draft acumula tecnical debt."
            ),
            privacy_required=False,
        ))

    return crew


def _print_table(crew: list[CrewMember]) -> None:
    sep = "═" * 92
    print(f"\n{sep}\n  Crew Designer — {len(crew)} novos specialists propostos\n{sep}\n")
    headers = ["NAME", "ROLE", "TIER", "MODEL", "CADENCE", "$/mo"]
    widths = [22, 38, 12, 30, 18, 6]
    print("  " + "  ".join(f"{h:<{w}}" for h, w in zip(headers, widths)))
    print("  " + "  ".join("-" * w for w in widths))
    total_cost = 0.0
    for m in crew:
        row = [
            m.name[:22], m.role[:38], m.model_tier[:12],
            m.model[:30], m.cadence[:18], f"${m.monthly_cost_usd:.0f}"
        ]
        print("  " + "  ".join(f"{c:<{w}}" for c, w in zip(row, widths)))
        total_cost += m.monthly_cost_usd
    print(f"\n  Total estimated monthly cost: ${total_cost:.0f}")
    print(f"  Privacy-locked agents: {sum(1 for m in crew if m.privacy_required)}")
    print()


def _write_vault(crew: list[CrewMember]) -> Path:
    CREW_OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "type: crew_design",
        f"computed_at: {datetime.now().isoformat(timespec='seconds')}",
        f"n_proposals: {len(crew)}",
        "tags: [crew, agents, design]",
        "---",
        "",
        "# Crew Design — Multi-Agent Framework",
        "",
        "Auditoria do org chart actual + propostas de novos specialists. ",
        "Reproduce o pattern OpenClaw: cada agente tem role + model tier + ",
        "cadence + cost estimate. Privacy-sensitive ficam local.",
        "",
        "## Org chart actual (já em produção)",
        "",
        "Founder",
        "  └─ Antonio Carlos (Chief of Staff)",
        "      ├─ Aurora Matina · Morning Analyst",
        "      ├─ Wilson Vigil · Floor Trader",
        "      ├─ Zé Mensageiro · Telegram Desk",
        "      ├─ Teresa Tese · Research Coordinator",
        "      ├─ Sofia Clippings · Research Intern",
        "      ├─ Ulisses Navegador · Head of Research",
        "      ├─ Valentina Prudente · Chief Risk Officer",
        "      │   └─ Diabo Silva · Chief Contrarian",
        "      ├─ Regina Ordem · Compliance Officer",
        "      │   └─ Noé Arquivista · Data Steward",
        "      ├─ Aristóteles Backtest · Head of Performance",
        "      ├─ Clara Fit · Portfolio Analyst",
        "      └─ Helena Linha (Mega) · Head of Design",
        "",
        f"## Propostas ({len(crew)})",
        "",
        "| Name | Role | Tier | Model | Local | Cadence | $/mo | Privacy |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m in crew:
        lines.append(
            f"| {m.name} | {m.role} | {m.model_tier} | {m.model} | "
            f"{m.local_or_cloud} | {m.cadence} | ${m.monthly_cost_usd:.0f} | "
            f"{'🔒' if m.privacy_required else '—'} |"
        )

    lines += ["", "## Detalhes", ""]
    for m in crew:
        lines += [
            f"### {m.name} — {m.role}",
            "",
            f"- **Model**: `{m.model}` ({m.model_tier} tier)",
            f"- **Localização**: {m.local_or_cloud}",
            f"- **Cadência**: `{m.cadence}`",
            f"- **Custo mensal estimado**: ${m.monthly_cost_usd:.2f}",
            f"- **Privacy-required**: {'sim 🔒' if m.privacy_required else 'não'}",
            "",
            f"**Rationale.** {m.rationale}",
            "",
            f"**Why now.** {m.why_now or '—'}",
            "",
        ]

    lines += [
        "",
        "## Próximos passos (manual)",
        "",
        "1. Decidir quais propostas aceitar/rejeitar.",
        "2. Para cada accepted, copiar template de `agents/` (e.g. `agents/morning_briefing.py`)",
        "   e adaptar.",
        "3. Adicionar persona em `config/agents.yaml`.",
        "4. Smoke test em manual mode antes de activar schedule.",
        "5. Re-correr `ii crew` para refresh.",
        "",
        "_Gerado por `ii crew` — analytics/topic_scorer + scripts/crew_designer.py_",
    ]
    CREW_OUT.write_text("\n".join(lines), encoding="utf-8")
    return CREW_OUT


def main() -> int:
    ap = argparse.ArgumentParser(description="Crew designer (EE.9)")
    ap.add_argument("--dry-run", action="store_true", help="só imprime, não escreve vault")
    args = ap.parse_args()

    crew = design_crew()
    _print_table(crew)
    if not args.dry_run:
        out = _write_vault(crew)
        print(f"📝 vault: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
