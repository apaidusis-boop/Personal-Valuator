---
type: skills_imported_index
tags: [skills, imported, plugins]
updated: 2026-05-13
---

# Imported Plugin Skills — Index

> Skills absorvidas de plugins de marketplace para o projecto local.
> Cópia invocável em `.claude/skills/<plugin>-<skill>/SKILL.md`.
> Re-absorver com `python scripts/absorb_plugins.py`.
> Manifest: `data/absorbed_plugins.json`.

## Porquê absorvemos

1. **Independência de marketplace** — updates upstream podem partir hooks (caso 2026-05-13, FSI plugins com `hooks.json = []`).
2. **Customização** — podemos editar localmente sem perder em refresh.
3. **Velocidade** — skills locais carregam sem rede.

A camada plugin original continua activa (MCP servers do FSI, hookify slash commands, etc.) — apenas as **skills e commands** vivem agora duplicadas localmente. Em caso de conflito, a cópia local ganha (Claude Code resolve por path de proximidade).

## Plugins absorvidos (17)

### Finance/Investment (mais relevantes ao projecto)

- [[equity-research/_|equity-research]] — 10 skills + 9 commands. **Catalysts/screen/morning-note/thesis/sector/initiate/earnings**. Sobreposição com `ii brief`, `ii decide`, `thesis_manager.py`.
- [[financial-analysis/_|financial-analysis]] — 14 skills + 7 commands. **DCF/LBO/3-statement/comps/debug-model**. Sobreposição com `analytics/fair_value.py`, `compare_tickers.py`.
- [[earnings-reviewer/_|earnings-reviewer]] — 6 skills. Earnings update reports + xlsx-author. Sobreposição com `ii react`, `library/earnings_prep.py`.
- [[model-builder/_|model-builder]] — 6 skills. DCF/LBO/3-statement/comps (versão headless de financial-analysis). Excel-focused.
- [[market-researcher/_|market-researcher]] — 5 skills. Competitive analysis + sector overview + idea generation. Subagent-flavour.
- [[wealth-management/_|wealth-management]] — 6 skills + 6 commands. **Rebalance/TLH/financial-plan/client-report**. Sobreposição com `ii rebalance`, `wealth-management:tlh`.
- [[private-equity/_|private-equity]] — 10 skills + 10 commands. IC memo, DD checklist, unit economics, value creation. **Menos relevante** ao nosso uso (Buffett/DRIP, não PE) mas útil como referência institucional.
- [[bigdata-com/_|bigdata-com]] — 1 skill + 10 commands. Bigdata.com MCP workflows (earnings-digest, sector-analysis, thematic). MCP server lado claude.ai.

### Engineering meta-skills

- [[superpowers/_|superpowers]] — 14 skills. **systematic-debugging, verification-before-completion, writing-plans, brainstorming, test-driven-development, dispatching-parallel-agents, using-git-worktrees, executing-plans, finishing-a-development-branch**. Reutilizadas no projecto (commands já existiam manualmente em `.claude/commands/`).
- [[claude-md-management/_|claude-md-management]] — 1 skill (claude-md-improver) + 1 command. Auditoria de CLAUDE.md.
- [[hookify/_|hookify]] — 1 skill (writing-rules) + 4 commands. Geração de hooks anti-padrão a partir de conversas.

### Dev tools

- [[chrome-devtools-mcp/_|chrome-devtools-mcp]] — 6 skills. A11y, LCP, memory-leak, performance debugging. Útil para Mission Control debug.
- [[figma/_|figma]] — 8 skills. Code Connect, implement-design, generate-library, generate-design. Para Phase MM design work.
- [[data/_|data]] (Astronomer) — 20 skills Airflow. Não relevante ao nosso uso actual mas absorvido.
- [[session-report/_|session-report]] — 1 skill. Gera HTML report de session usage.

### Web/AI search

- [[exa/_|exa]] — 1 skill (search). Já temos `fetchers/exa_fetcher.py` em produção. Skill é guia de uso do MCP.

### Outros

- [[legalzoom/_|legalzoom]] — 1 skill (attorney-assist) + 1 command (review-contract). **Não relevante** ao projecto investing mas absorvido (custou 1 ficheiro).

## Como invocar

As skills aparecem como **`<plugin>-<skill>`** no registo de skills (em vez de `<plugin>:<skill>`):

```
financial-analysis-dcf-model        # local (cópia absorvida)
financial-analysis:dcf-model         # original do plugin (continua disponível)
```

Ambas funcionam — a local sobrevive a problemas de marketplace.

## Manutenção

Re-correr após `/plugins update`:
```bash
python scripts/absorb_plugins.py
```

O script é idempotente — overwrites com a versão fresca do cache. Se quiseres preview antes:
```bash
python scripts/absorb_plugins.py --dry-run
```
