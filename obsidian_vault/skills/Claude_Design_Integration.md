---
type: integration_plan
owner: helena_linha
status: proposed
created: 2026-04-25
tags: [design, claude, integration, helena, anthropic_labs]
---

# Claude Design — integration plan

> Helena Linha · 2026-04-25
> Como incorporar [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) (Anthropic Labs research preview) ao nosso fluxo de design.

## TL;DR

Claude Design é **web-only** (claude.ai), Pro/Max/Team/Enterprise. Não há API.

Não substitui o nosso `_theme.py` / `_components.py` / Streamlit — substitui o **whiteboard** onde a Helena prototipa antes de codar. O fluxo é:

> **Helena prototipa em Claude Design → exporta HTML/screenshot → handoff para Claude Code (esta CLI) → implementação em Streamlit reusando `_components.py`**.

A nossa vantagem específica: o [[Design_System]] v1.0 já existe em markdown estruturado. Podemos **cola­r o Design_System.md inteiro como contexto de Claude Design**, e ele respeita os 5 tokens, 5 princípios, 8 anti-padrões. Saída fica conforme antes de chegar a Streamlit.

## O que é Claude Design (síntese)

| Capacidade | Detalhe |
|---|---|
| Interface | Chat à esquerda + canvas à direita |
| Powered by | Claude Opus 4.7 |
| Outputs | HTML standalone, PDF, PPTX, ZIP, link partilhável (view/comment/edit), Canva |
| Inputs | Prompt, screenshots, link a repo (GitHub), brand assets, design system existente |
| Pode ler | "code repository so Claude understands your existing components, architecture, and styling patterns" |
| Pode produzir | Wireframes, prototypes, slide decks, landing pages, mobile apps, design systems, animações |
| Handoff | "Handoff to Claude Code" (local agent ou web) |
| API | **Não** — só web UI |
| Auth | Pro/Max/Team/Enterprise; usage conta contra os limites do plano |

**Limitação crítica**: link de repos muito grandes pode causar lag. Anthropic recomenda apontar a sub-directorias específicas, não monorepos inteiros.

## Onde encaixa no nosso fluxo

### O que o Claude Design faz BEM para nós

1. **Prototipar pages novas antes de codar** — Helena descreve "uma page de Sector Drilldown com top-3 holdings, EV/EBITDA distribution, e correlation matrix"; Claude Design devolve HTML mockup; Helena critica/itera no canvas; só depois manda para implementação.
2. **Slide decks "Quarterly review"** — output PPTX directo, sem ter que abrir PowerPoint. Casamento natural com `morning_briefing.py` / `weekly_report.py`.
3. **Landing page externa** — se algum dia tivermos page pública para o sistema (recruitment? showcase?), Claude Design entrega em 1 prompt.
4. **A/B visual rápido** — gerar 3 variantes de uma KPI tile e escolher; muito mais rápido que mexer em CSS no Streamlit e refresh.
5. **Design system audit** — apontá-lo a `obsidian_vault/skills/Design_System.md` + screenshots actuais do dashboard, pedir gaps/inconsistências.

### O que NÃO faz (importante)

1. **Não modifica o nosso código directamente** — não há API. É sempre human-in-the-loop: copy-paste do export para Claude Code (esta CLI).
2. **Não substitui Streamlit** — o output é HTML/CSS standalone; não conhece os widgets do Streamlit nem o nosso `_components.py`. Helena/Claude Code traduz.
3. **Não vê o estado real dos dados** — gera com placeholders. Para ver com dados reais, ainda precisas do dashboard local.
4. **Não respeita automaticamente o `_theme.py`** — temos que dar-lhe o Design_System.md como contexto inicial em **cada nova sessão**.

## Workflow proposto

### Sessão típica de página nova

1. **Brief no Obsidian**: founder ou Vitória escreve 1 nota `obsidian_vault/skills/Brief_<page>.md` com objectivo, audiência, dados-chave (≤200 palavras).
2. **Helena entra em Claude Design** (claude.ai → Labs → Design):
   - Cola o conteúdo de `Design_System.md` como contexto inicial.
   - Cola o brief.
   - Opcional: linka https://github.com/<user>/investment-intelligence (sub-dir `scripts/`).
   - Itera no canvas até estar satisfeita.
3. **Export**: HTML standalone + screenshot → guarda em `obsidian_vault/_assets/proto_<page>_v1.html` + `.png`.
4. **Handoff para Claude Code** (esta CLI): "Helena aprovou este protótipo `proto_<page>_v1.html`. Implementa como `scripts/dashboard_app.py` page nova, reusando `_components.py`. Anti-padrão: introduzir cores fora dos tokens".
5. **Claude Code implementa** em Streamlit, regista no `_components.py` se gerou helpers reusáveis novos.
6. **Helena review** → commit.

### Sessão típica de slide deck (briefing trimestral)

1. **Vitória escreve outline** + key insights do trimestre (já temos em `morning_briefing.py`).
2. **Helena cola** Design_System + outline em Claude Design, pede "10-slide deck, paleta nossa, Helvetica/Inter, dark mode".
3. **Export PPTX** → guarda em `reports/Q<n>_<year>.pptx`.
4. Para a próxima vez, pode ser scriptado via `python-pptx` se virar recurring (ver Phase Z follow-up).

## O que muda no nosso código

**Nada por agora.** Claude Design é uma ferramenta consultiva da Helena, não uma dependência runtime.

**Adicionar ao roadmap**:

- [ ] Helena cria 1 brief de teste em Claude Design para validar fluxo (page candidata: "Conviction Heatmap" — não existe ainda).
- [ ] Se export HTML for útil, criar `scripts/_proto_to_streamlit.py` (Helena + Claude Code) — ferramenta que lê HTML de Claude Design e sugere mapeamento para `kpi_tile`/`status_pill`/etc. (deferred até validar fluxo).
- [ ] Se PPTX output for útil para `weekly_report.py`, integrar como output alternativo (`--format pptx`).

## Política de uso

1. **Toda export do Claude Design fica em `obsidian_vault/_assets/proto_*`** com versionamento manual (v1, v2, ...). Não substitui o source-of-truth no Streamlit.
2. **Helena nunca leva um Claude Design HTML directamente para produção.** Sempre passa por handoff a Claude Code, que respeita `_components.py` e tokens.
3. **Brand spec sempre injectado**: o `Design_System.md` é o contexto inicial de qualquer sessão — caso contrário, Claude Design inventa cores fora da paleta.
4. **Custos**: usage do Claude Design conta contra plano pessoal. Para sessões de 30+ minutos, limitar a 1-2 por dia.
5. **Repository link**: apontar só a `scripts/` ou só a `obsidian_vault/skills/`, nunca o repo todo (lag).

## Quando NÃO usar Claude Design

- Para mexer em **uma única CSS rule** ou **um helper já existente**: Helena edita directamente em `_theme.py` ou `_components.py`. Claude Design tem overhead de browser.
- Para **dados reais com interactividade complexa** (filtros, drill-downs ligados a SQLite): isto é Streamlit territory. Claude Design só protótipa o esqueleto.
- Para **visualizações Plotly específicas**: o nosso template `ii_dark` está afinado; Claude Design não conhece Plotly Python.

## Cross-links

- [[Design_System]] — paleta + princípios; injectar como contexto em cada sessão de Claude Design
- [[Helena Linha]] — owner do fluxo
- [[Design_Watch]] — Claude Design entra como **source #4** (após GitHub + RSS + YouTube) na próxima iteração da scout, com query "claude design design system export pattern"

## Status

**Proposed (2026-04-25)**. Proxima sessão real de Claude Design + reporte de Helena depois → promover a `accepted` ou `deferred`.
