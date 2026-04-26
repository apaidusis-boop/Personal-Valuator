---
type: skill
tier: S
skill_name: xlsx
source: anthropics/skills
status: backlog
sprint: W.1
tags: [skill, tier_s, xlsx, document, portfolio_import]
---

# 📊 XLSX Skill (Anthropic Skills)

**Repo**: https://github.com/anthropics/skills (subfolder `document-skills/xlsx`)
**Fit**: 🎯 **Alto** — XP e JPM entregam extracts em xlsx; importação hoje é frágil.

## O que faz
Skill oficial para ler/escrever `.xlsx` preservando formatação, fórmulas, múltiplas sheets. Retorna DataFrame-like.

## Onde integra
- **Primário**: `scripts/import_portfolio.py` — hoje usa `openpyxl` cru, quebra quando XP muda layout
- **Secundário**: `scripts/import_taxlots.py` — JPM tax lots vêm em xlsx multi-sheet
- **Terciário**: export de reports (`reports/weekly_*.md`) poderia ter versão xlsx para análise offline

## Decisão de adopção
O valor aqui é **menor que PDF** porque `openpyxl` já resolve 80%. Skill só vale se:
1. XP/JPM mudam layout e precisamos de detecção automática de colunas (Claude lê headers + infere mapping)
2. Quisermos exportar xlsx rico (condicional formatting, sparklines) — relevant se user quer dashboard Excel

**Recomendação**: adoptar só se W.1 benchmark mostrar regressões no `import_portfolio.py`. Caso contrário, backlog.

## Instalação
```bash
cp -r ~/.claude/anthropic-skills/document-skills/xlsx ~/.claude/skills/
```

## Blockers
Nenhum. Decisão arquitetural: substituir openpyxl ou só fallback?
