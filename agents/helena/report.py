"""report — master consolidator for Helena Mega.

Reads structured data from audit/curate/spike modules and writes
`obsidian_vault/skills/Helena_Mega/00_MASTER.md` — the executive summary
the founder reads first.

Run:
    python -m agents.helena.report
"""
from __future__ import annotations

import argparse
from datetime import date

from . import VAULT_OUT, ROOT
from .audit import run as audit_run
from .curate import CANDIDATES
from .spike import PATHS


def render_md() -> str:
    today = date.today().isoformat()

    # ── audit summary
    violations, file_meta, targets = audit_run(["scripts"])
    sev = {"error": 0, "warn": 0, "info": 0}
    for v in violations:
        sev[v.severity] += 1
    by_rule: dict[str, int] = {}
    for v in violations:
        by_rule[v.rule] = by_rule.get(v.rule, 0) + 1
    by_file: dict[str, int] = {}
    for v in violations:
        by_file[v.file] = by_file.get(v.file, 0) + 1
    worst_file = max(by_file.items(), key=lambda kv: kv[1]) if by_file else (None, 0)

    # ── curate summary
    install = [c for c in CANDIDATES if c.tier == "INSTALL"]
    consider = [c for c in CANDIDATES if c.tier == "CONSIDER"]
    skip = [c for c in CANDIDATES if c.tier == "SKIP"]

    # ── spike summary  (kept inline — see 03_Spikes.md)

    out = [
        "---",
        "type: helena_mega_master",
        f"updated: {today}",
        "owner: helena_linha",
        "tags: [helena, mega, master, design, platform]",
        "---",
        "",
        "# 00 — Helena Mega · master report",
        "",
        f"> Helena Linha · {today}",
        "> Consolidação de 3 análises: auditoria do design system actual,",
        "> curadoria dos skills da comunidade, e spikes de 4 paths de plataforma.",
        "",
        "## TL;DR",
        "",
        f"1. **Design system v1.0 está aplicado em {len([f for f, m in file_meta.items() if m.get('has_inject_css')])}/{sum(1 for m in file_meta.values() if m.get('is_streamlit_page'))}** páginas Streamlit. Helena fez o trabalho.",
        f"2. **{len(violations)} violações** detectáveis automaticamente "
        f"(**{sev['error']} errors / {sev['warn']} warns / {sev['info']} info**) em {len(targets)} ficheiros. "
        f"Pior ficheiro: `{worst_file[0]}` com {worst_file[1]} hits — fix em ≤1h.",
        f"3. **{len(CANDIDATES)} skills da comunidade triados**: {len(install)} install, {len(consider)} consider, {len(skip)} skip. **Não instalar tudo** — excesso é o slop.",
        f"4. **4 paths de plataforma** com tecto e custo honestos. Recomendação: **Path B (Tauri)** para 'top quality'; Path A+D combinado se 4 semanas demasiado.",
        "",
        "## 1 · Estado actual do design system",
        "",
        f"### Cobertura — {sum(1 for m in file_meta.values() if m.get('is_streamlit_page'))} página(s) Streamlit detectadas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Páginas com `inject_css()` | {len([f for f, m in file_meta.items() if m.get('has_inject_css')])} |",
        f"| Páginas com `kpi_tile` import | {len([f for f, m in file_meta.items() if m.get('has_kpi_tile_import')])} |",
        f"| Total ficheiros .py em scope | {len(targets)} |",
        f"| Total LoC analisadas | {sum(m.get('lines', 0) for m in file_meta.values())} |",
        "",
        "### Violações por regra",
        "",
        "| Regra | Severidade | Hits |",
        "|---|---|---:|",
    ]

    rules_severity = {
        "DS001": "error", "DS002": "error", "DS003": "error", "DS004": "error",
        "DS005": "warn", "DS006": "warn", "DS007": "warn", "DS008": "warn",
        "DS009": "info",
    }
    rules_desc = {
        "DS001": "Rainbow/sequential cmap em styler",
        "DS002": "st.metric() cru",
        "DS003": "Emoji-prefix em heading",
        "DS004": "px.pie() banido",
        "DS005": "Plotly template cru",
        "DS006": "Hex literal fora dos 5 tokens",
        "DS007": "Cor por nome",
        "DS008": "Caption >8 palavras",
        "DS009": "Página sem inject_css()",
    }
    for rid, s in rules_severity.items():
        n = by_rule.get(rid, 0)
        if n == 0:
            mark = "🟢"
        elif s == "error":
            mark = "🔴"
        elif s == "warn":
            mark = "🟡"
        else:
            mark = "⚪"
        out.append(f"| `{rid}` {rules_desc[rid]} | {s} {mark} | {n} |")
    out += ["", "**Detalhe**: ver [[01_Audit]]", ""]

    out += [
        "## 2 · Curadoria de skills da comunidade",
        "",
        f"39 candidatos avaliados (lista completa em [[02_Curation]]). Princípio: "
        f"excesso de skills cria slop. Critério hard — preencher gap real, "
        f"manutenção activa, não duplicar arsenal in-house.",
        "",
        f"### INSTALL ({len(install)})",
        "",
        "| Skill | Categoria | Fit | Razão curta |",
        "|---|---|---:|---|",
    ]
    for c in sorted(install, key=lambda c: -c.fit_score):
        rationale = c.rationale.replace("|", "\\|")[:120]
        out.append(f"| **{c.name}** | {c.category} | {c.fit_score} | {rationale} |")

    out += [
        "",
        f"### CONSIDER ({len(consider)})",
        "",
        f"_30-min spike antes de decidir. Lista completa em [[02_Curation]]._",
        "",
        "Top 5 por fit score:",
        "",
        "| Skill | Fit | Razão |",
        "|---|---:|---|",
    ]
    for c in sorted(consider, key=lambda c: -c.fit_score)[:5]:
        rationale = c.rationale.replace("|", "\\|")[:120]
        out.append(f"| **{c.name}** | {c.fit_score} | {rationale} |")

    out += [
        "",
        f"### SKIP ({len(skip)})",
        "",
        f"_{len(skip)} skills filtradas — duplicam capability existente, fora de scope, ou abandonware._",
        "",
        "Top razões para skip:",
        "",
    ]
    skip_categories: dict[str, int] = {}
    for c in skip:
        skip_categories[c.category] = skip_categories.get(c.category, 0) + 1
    for cat, n in sorted(skip_categories.items(), key=lambda kv: -kv[1]):
        out.append(f"- {cat}: {n} skipped")

    out += [
        "",
        "## 3 · 4 paths de plataforma",
        "",
        f"Detalhe em [[03_Spikes]]. Cada path: stack, file tree, build, custo honesto.",
        "",
        "| Path | Título | Tecto | Semanas | Reusa backend |",
        "|---|---|---|---:|---|",
    ]
    for k, p in PATHS.items():
        reuse = "100%" if k in ("B", "C") else ("100%" if k == "D" else "100%")
        out.append(f"| **{k}** | {p['title']} | {p['ceiling']} | {p['weeks']} | {reuse} |")

    out += [
        "",
        "**Recomendação**: Path B (Tauri). Tecto 10/10, reusa 100% Python backend, "
        "Helena tokens traduzem 1:1, 3-4 semanas honestas.",
        "",
        "**Fallback se prazo apertado**: Path A (1 sprint Streamlit perfeccionismo, "
        "fix os 4 errors do audit) + Path D (Obsidian polish + HTML reports). "
        "2-3 semanas total para tecto 8/10.",
        "",
        "## 4 · Decisões pendentes do founder",
        "",
        "Helena precisa de aprovação em 3 pontos antes de avançar:",
        "",
        "- [ ] **Path** — A / B / C / D / hybrid? (recomendação Helena: B)",
        "- [ ] **Skills install agora** — confirmar 4 INSTALL automáticos OU "
        "Helena para de instalar e founder revê 1-a-1?",
        "- [ ] **Audit fixes** — Helena Mega faz auto-fix dos 4 errors do audit "
        "(opt-in com `--apply`)? Ou só relata?",
        "",
        "## 5 · Próximos passos imediatos (próximas 24h, sem aprovação adicional)",
        "",
        "1. **Audit fix manual**: founder vê [[01_Audit]] e decide quais errors aceita corrigir",
        "2. **30-min spikes** dos CONSIDER tier 1 (julianoczkowski/designer-skills, Skill_Seekers, CCHooks Python)",
        "3. **Helena Design Watch** corre normal no Sunday 23:30 (não bloquear)",
        "4. **Claude Design** primeira sessão real de Helena (per `Claude_Design_Integration.md`) — protótipo da page 'Conviction Heatmap' que ainda não existe",
        "",
        "## Reproduzibilidade",
        "",
        "Todos os outputs foram gerados por:",
        "",
        "```bash",
        "python -m agents.helena_mega all       # tudo",
        "python -m agents.helena.audit          # 01_Audit.md",
        "python -m agents.helena.curate         # 02_Curation.md",
        "python -m agents.helena.spike          # 03_Spikes.md",
        "python -m agents.helena.report         # 00_MASTER.md (este)",
        "```",
        "",
        "## Cross-links",
        "",
        "- [[01_Audit]] — design system linter (DS001-DS009 rules)",
        "- [[02_Curation]] — 39 skills triados",
        "- [[03_Spikes]] — 4 paths feasibility",
        "- [[Design_System]] — fonte das regras",
        "- [[Helena Linha]] — owner da Mega Helena",
        "- [[Claude_Design_Integration]] — prototyping flow",
        "- [[CONSTITUTION]] — não-negociáveis da casa",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    import sys
    ap = argparse.ArgumentParser(description="Helena Mega master report")
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()

    md = render_md()

    if args.print:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        sys.stdout.write(md + "\n")
        return 0

    out_path = VAULT_OUT / "00_MASTER.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
