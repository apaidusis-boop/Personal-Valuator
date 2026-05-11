---
type: skill
tier: Gold
skill_name: canvas-design
source: anthropics/skills
status: backlog
sprint: W.8
tags: [skill, gold, canvas, visual, briefing]
---

# 🎨 Canvas Design (Anthropic Skills)

**Repo**: https://github.com/anthropics/skills (subfolder `canvas-design`)
**Fit**: 🟡 médio, mas promovido a **Gold** por request do user (overkill is fine).

## O que faz
Skill para gerar visuais: diagramas, annotated charts, infográficos. Output SVG/PNG.

## Onde integra (uses reais para nós)

### 1. Briefings visuais diários
`obsidian_vault/briefings/YYYY-MM-DD.md` hoje é texto puro. Canvas geraria:
- **Allocation donut** — pie chart BR vs US vs RF (renovado diariamente)
- **Thesis health heatmap** — matriz 35 tickers × thesis score (feed do [[SKL_autoresearch_perpetuum|perpetuum validator]])
- **Regime dial** — BR regime + US regime em gauge visual
- **DRIP curve** — projecção 5/10/15y para cada holding

### 2. Obsidian Canvas nativos
Já temos `Untitled.canvas`, `Untitled 2.canvas` — vazios. Canvas Design skill poderia:
- Gerar canvas de **ticker deep-dive** (thesis + peers + catalysts + risks em layout)
- Canvas **Rebalance plan** (drift bars + target bars + sugestões visuais)
- Canvas **Earnings calendar** (timeline visual)

### 3. Weekly report (`scripts/weekly_report.py`)
Inject SVG charts em `reports/weekly_YYYY-MM-DD.md`:
- Portfolio performance curve vs IBOV / SPY
- Sector drift vs target
- Dividend reinvestment ladder

## Diff vs Streamlit dashboard
Streamlit é **on-demand** (user abre browser). Canvas é **pre-rendered** em Obsidian — consumido no fluxo vault. Complementares, não competem.

## Sprint W.8 — entregáveis
- [ ] Gerar 1 briefing visual piloto (2026-04-25) com 4 charts embedded
- [ ] Canvas de ticker (caso piloto: ACN — já tem deep notes)
- [ ] Template `obsidian_vault/templates/daily_briefing_visual.md`

## Blockers
Nenhum. Skill é Claude-side + filesystem output.
