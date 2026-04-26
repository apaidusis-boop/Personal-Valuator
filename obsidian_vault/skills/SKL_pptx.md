---
type: skill
tier: Gold
skill_name: pptx
source: anthropics/skills
status: backlog
sprint: W.8
tags: [skill, gold, pptx, slides, reports]
---

# 🎬 PPTX Skill (Anthropic Skills)

**Repo**: https://github.com/anthropics/skills (subfolder `document-skills/pptx`)
**Fit**: 🟡 médio, promovido a **Gold** por request do user.

## O que faz
Skill para gerar/editar apresentações `.pptx`: slides, layouts, charts, tabelas, animações. Respeita templates.

## Onde integra (uses reais)

### 1. Quarterly State-of-Portfolio deck 📊
Novo deliverable **trimestral** (Mar/Jun/Set/Dez):
- Slide 1: Capa "Portfolio Q1 2026"
- Slide 2: Overview BR+US+RF totals em BRL
- Slide 3: Top 5 winners / losers
- Slide 4: Sector allocation vs target
- Slide 5-10: Deep-dive nas 5 holdings maiores (thesis + catalysts + risks)
- Slide 11: Regime macro BR + US
- Slide 12: Thesis health heatmap (feed perpetuum validator)
- Slide 13: Action plan próximo trimestre

### 2. Annual review deck 🏆
End-of-year comprehensive review:
- Performance vs benchmarks (IBOV, SPY, CDI)
- Dividends received + DRIP effectiveness
- Rebalance history + drift control
- Winners/losers postmortem
- Strategic adjustments para próximo ano

### 3. Ad-hoc thesis deck 🎯
Quando ingerir "Carteira Recomendada" (ex: Suno Top Div) — skill gera PPTX com comparison:
- Carteira do analista vs minha carteira
- Overlap / gaps
- Pesos relativos
- Insights

## Automação
Script `scripts/generate_quarterly_deck.py`:
```
Inputs: quarter (Q1/Q2/Q3/Q4), year
↓
1. Pull snapshot mv + portfolio_positions
2. Pull thesis_health history (novo, do perpetuum validator)
3. Gerar charts (pode pedir Canvas skill para SVG)
4. PPTX skill assembla slides com layout template
Output: reports/quarterly_YYYYQN.pptx
```

Depois: upload automático para **Google Drive** (usar `mcp__claude_ai_Google_Drive__create_file` que já está no harness!) em folder "Investment Intelligence > Quarterly".

## Sprint W.8 — entregáveis
- [ ] Template `reports/templates/quarterly_template.pptx` (design limpo, 13 slides)
- [ ] Script `scripts/generate_quarterly_deck.py`
- [ ] Primeiro deck: Q1 2026 (retroactivo, 2026-04-24 é fim Q1 logical cutoff)
- [ ] Auto-upload para Google Drive

## Blockers
Nenhum. python-pptx disponível; skill oficial Anthropic.
