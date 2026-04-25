---
type: helena_mega_master
updated: 2026-04-25
owner: helena_linha
tags: [helena, mega, master, design, platform]
---

# 00 — Helena Mega · master report

> Helena Linha · 2026-04-25
> Consolidação de 3 análises: auditoria do design system actual,
> curadoria dos skills da comunidade, e spikes de 4 paths de plataforma.

## TL;DR

1. **Design system v1.0 está aplicado em 1/1** páginas Streamlit. Helena fez o trabalho.
2. **16 violações** detectáveis automaticamente (**4 errors / 12 warns / 0 info**) em 67 ficheiros. Pior ficheiro: `scripts/dashboard_app.py` com 6 hits — fix em ≤1h.
3. **39 skills da comunidade triados**: 4 install, 16 consider, 19 skip. **Não instalar tudo** — excesso é o slop.
4. **4 paths de plataforma** com tecto e custo honestos. Recomendação: **Path B (Tauri)** para 'top quality'; Path A+D combinado se 4 semanas demasiado.

## 1 · Estado actual do design system

### Cobertura — 1 página(s) Streamlit detectadas

| Métrica | Valor |
|---|---:|
| Páginas com `inject_css()` | 1 |
| Páginas com `kpi_tile` import | 1 |
| Total ficheiros .py em scope | 67 |
| Total LoC analisadas | 18465 |

### Violações por regra

| Regra | Severidade | Hits |
|---|---|---:|
| `DS001` Rainbow/sequential cmap em styler | error 🔴 | 2 |
| `DS002` st.metric() cru | error 🟢 | 0 |
| `DS003` Emoji-prefix em heading | error 🟢 | 0 |
| `DS004` px.pie() banido | error 🔴 | 2 |
| `DS005` Plotly template cru | warn 🟡 | 5 |
| `DS006` Hex literal fora dos 5 tokens | warn 🟡 | 5 |
| `DS007` Cor por nome | warn 🟢 | 0 |
| `DS008` Caption >8 palavras | warn 🟡 | 2 |
| `DS009` Página sem inject_css() | info 🟢 | 0 |

**Detalhe**: ver [[01_Audit]]

## 2 · Curadoria de skills da comunidade

39 candidatos avaliados (lista completa em [[02_Curation]]). Princípio: excesso de skills cria slop. Critério hard — preencher gap real, manutenção activa, não duplicar arsenal in-house.

### INSTALL (4)

| Skill | Categoria | Fit | Razão curta |
|---|---|---:|---|
| **hue (dominikmartn)** | design | 100 | Already in ~/.claude/skills/. Confirm it's the latest version. Generates design language skills from references. |
| **huashu-design** | design | 100 | Already installed. Hi-fi prototyping + 5 streams × 20 philosophies + video export. Underused — should be Helena's go-to  |
| **ui-ux-pro-max-skill** | design | 100 | Already installed. 67 UI styles + 161 palettes + 57 font pairs. Use as reference DB when picking variants for new pages. |
| **designer-skills (julianoczkowski)** | design | 88 | 7 skills mapping a real design process (research → wireframe → high-fi → handoff). Helena flow currently jumps from brie |

### CONSIDER (16)

_30-min spike antes de decidir. Lista completa em [[02_Curation]]._

Top 5 por fit score:

| Skill | Fit | Razão |
|---|---:|---|
| **CCHooks (GowayLee)** | 72 | Python equivalent of johnlindquist. Better fit for our stack; could trigger `python -m agents.helena.audit` on PreToolUs |
| **Skill Seekers (yusufkaraaslan)** | 68 | Auto-generates a skill from any docs site/PDF. Concrete use: feed it Bigdata.com docs + yfinance docs + brapi.dev docs t |
| **awesome-claude-skills (BehiSecc)** | 60 | Curated index. Use as discovery, not install. Re-scan monthly via Helena scout. |
| **interface-design (Dammyjay93)** | 58 | Scope claims 'interface design'. Need to read SKILL.md before deciding — risk of overlap with huashu-design prototyping  |
| **OneDrive/Claude/Skills/design-system** | 55 | Local copy with components/layouts/showcase/themes/tokens. Audit overlap with our Helena Design System v1.0 — keep best. |

### SKIP (19)

_19 skills filtradas — duplicam capability existente, fora de scope, ou abandonware._

Top razões para skip:

- dev: 6 skipped
- research: 5 skipped
- hooks: 4 skipped
- security: 2 skipped
- finance: 1 skipped
- productivity: 1 skipped

## 3 · 4 paths de plataforma

Detalhe em [[03_Spikes]]. Cada path: stack, file tree, build, custo honesto.

| Path | Título | Tecto | Semanas | Reusa backend |
|---|---|---|---:|---|
| **A** | Streamlit perfectionism | Tasteful internal tool (8/10) | 1 | 100% |
| **B** | Tauri desktop app  (RECOMMENDED) | Native product feel (10/10) | 3-4 | 100% |
| **C** | Next.js + FastAPI (web app, PWA) | Real web product (9/10) | 3-4 | 100% |
| **D** | Obsidian-native + static HTML reports | Polished knowledge worker setup (8/10 in different dimension) | 1-2 | 100% |

**Recomendação**: Path B (Tauri). Tecto 10/10, reusa 100% Python backend, Helena tokens traduzem 1:1, 3-4 semanas honestas.

**Fallback se prazo apertado**: Path A (1 sprint Streamlit perfeccionismo, fix os 4 errors do audit) + Path D (Obsidian polish + HTML reports). 2-3 semanas total para tecto 8/10.

## 4 · Decisões pendentes do founder

Helena precisa de aprovação em 3 pontos antes de avançar:

- [x] **Path** — A / B / C / D / hybrid? (recomendação Helena: B)
- [x] **Skills install agora** — confirmar 4 INSTALL automáticos OU Helena para de instalar e founder revê 1-a-1?
- [x] **Audit fixes** — Helena Mega faz auto-fix dos 4 errors do audit (opt-in com `--apply`)? Ou só relata?

## 5 · Próximos passos imediatos (próximas 24h, sem aprovação adicional)

1. **Audit fix manual**: founder vê [[01_Audit]] e decide quais errors aceita corrigir
2. **30-min spikes** dos CONSIDER tier 1 (julianoczkowski/designer-skills, Skill_Seekers, CCHooks Python)
3. **Helena Design Watch** corre normal no Sunday 23:30 (não bloquear)
4. **Claude Design** primeira sessão real de Helena (per `Claude_Design_Integration.md`) — protótipo da page 'Conviction Heatmap' que ainda não existe

## Reproduzibilidade

Todos os outputs foram gerados por:

```bash
python -m agents.helena_mega all       # tudo
python -m agents.helena.audit          # 01_Audit.md
python -m agents.helena.curate         # 02_Curation.md
python -m agents.helena.spike          # 03_Spikes.md
python -m agents.helena.report         # 00_MASTER.md (este)
```

## Cross-links

- [[01_Audit]] — design system linter (DS001-DS009 rules)
- [[02_Curation]] — 39 skills triados
- [[03_Spikes]] — 4 paths feasibility
- [[Design_System]] — fonte das regras
- [[Helena Linha]] — owner da Mega Helena
- [[Claude_Design_Integration]] — prototyping flow
- [[CONSTITUTION]] — não-negociáveis da casa
