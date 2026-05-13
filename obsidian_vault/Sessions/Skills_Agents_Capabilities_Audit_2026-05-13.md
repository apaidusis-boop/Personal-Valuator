---
type: audit
tags: [audit, skills, agents, capabilities, organization]
date: 2026-05-13
---

# Skills / Agents / Capabilities — Audit 2026-05-13

> Sentido do user: "tenho muitos skills que não estão a ser usados". Este doc é o
> inventário completo + sinal de uso (cron / código / CLAUDE.md), para decidir
> o que cortar, consolidar ou promover.

---

## Resumo executivo

| Categoria | Total | Usados (sinal claro) | Decorativos / candidatos a purga |
|---|---:|---:|---:|
| **Skills `.claude/skills/`** | 124 | 13 (project-native) + ~15 imported-relevantes | ~96 imported sem sinal de uso |
| **Slash commands `.claude/commands/`** | 52 | 4 native + ~10 imported relevantes | ~38 |
| **Subagents `.claude/agents/`** | 4 | 1 (earnings-reviewer wrapper) | 3 |
| **Python agents `agents/`** | 28 .py + 4 packages | ~10 em cron/CLI | ~18 (one-shots e legacy) |
| **Council personas (vault)** | 10 | 6 com reviews recentes | 4 sem reviews |
| **`ii` command catalog** | 133 entradas | ~60 em uso quotidiano | ~73 raras / experimentais |
| **Plugins activos** | 17 | 5 (financial-analysis, equity-research, exa, bigdata-com, superpowers) | 12 (data Airflow, legalzoom, figma, hookify, etc.) |
| **MCP servers loaded** | 18 | 8 (yfinance via fetcher, Bigdata, FMP, Status Invest, Tavily) | 10 (Gmail/Calendar/Drive raramente) |

**O que está MESMO a correr** (cron + CLI quotidiana):
- `daily_run.bat` (cron diário 23:30): 20 scripts — universos BR+US, perpetuum, paper-trade, briefing, telegram
- `hourly_run.bat`: SEC + CVM monitors, news fetch, notify
- `q4h_run.bat`: PDF extractor, dividend/earnings calendar, triggers, yt_poll, pod_poll
- CLI: `ii brief`, `ii deepdive`, `ii panorama`, `ii decide`, `ii fv`, `ii verdict`

---

## 1. Skills — `.claude/skills/` (124 dirs)

### 1a. Project-native (13) — todos têm uso documentado

| Skill | Wired em | Sinal |
|---|---|---|
| `drip-analyst` | manual / piloto | Phase W skill creator piloto |
| `macro-regime` | `analytics/regime.py` chama | ✓ cron |
| `panorama-ticker` | `ii panorama` | ✓ CLI |
| `perpetuum-review` | `scripts/perpetuum_action_run.py` | ✓ workflow |
| `rebalance-advisor` | `ii rebalance` | ✓ CLI |
| `tavily-best-practices` / `cli` / `crawl` / `dynamic-search` / `extract` / `map` / `research` / `search` (8) | `fetchers/tavily_*.py` + agents/autoresearch.py | ✓ amplamente usado |

**Decisão**: manter todos. Núcleo do projecto.

### 1b. Imported (111) — agrupados por plugin de origem com tier de relevância

#### Tier A — alta relevância investing (manter, consultar quando preciso)

- **equity-research** (10 skills): catalyst-calendar, earnings-analysis, earnings-preview, idea-generation, initiating-coverage, model-update, morning-note, sector-overview, thesis-tracker
  - **Sobrepõem**: `ii brief`, `ii decide`, `thesis_manager.py`, `library/earnings_prep.py`
  - **Valor adicional**: framework sell-side formal (5-task initiation, 8-12 page earnings report). Útil para nivelar o nosso template.
- **financial-analysis** (14 skills): 3-statement-model, audit-xls, clean-data-xls, comps-analysis, competitive-analysis, dcf-model, deck-refresh, ib-check-deck, lbo-model, ppt-template-creator, pptx-author, skill-creator, xlsx-author
  - **Sobrepõem**: `analytics/fair_value.py`, `analytics/fair_value_forward.py`, `compare_tickers.py`
  - **Valor adicional**: tooling Excel/PPT formal. Usar para deck quarterly se chegar a tier B4 do Comercial.
- **earnings-reviewer** (6 skills): audit-xls, earnings-analysis, earnings-preview, model-update, morning-note, xlsx-author
  - **Sobrepõem**: `ii react`, `earnings_prep.py`
  - Quase duplicado de equity-research mas focado em update pós-earnings.
- **wealth-management** (6 skills): client-report, client-review, financial-plan, investment-proposal, portfolio-rebalance, tax-loss-harvesting
  - **Sobrepõem**: `ii rebalance` (nosso é mais simples)
  - **Valor adicional**: TLH e financial-plan são gaps reais nossos.

#### Tier B — útil para engenharia (manter como referência)

- **superpowers** (14 skills): brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving/requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills
  - **Sobrepõem**: 4 já estão como `.claude/commands/` manualmente (security-review, systematic-debugging, verification-before-completion, writing-plans).
  - **Acção**: dedup. Manter `superpowers-*` ou os manuais, não ambos. Decisão pendente.
- **chrome-devtools-mcp** (6 skills): a11y-debugging, chrome-devtools, chrome-devtools-cli, debug-optimize-lcp, memory-leak-debugging, troubleshooting
  - **Uso**: debug do Mission Control Next.js. Pertinente quando há work UI.
- **claude-md-management** (1): claude-md-improver. ✓ útil para CLAUDE.md hygiene.

#### Tier C — relevância marginal (candidatos a remover)

- **private-equity** (10 skills): ai-readiness, dd-checklist, dd-meeting-prep, deal-screening/sourcing, ic-memo, portfolio-monitoring, returns-analysis, unit-economics, value-creation-plan
  - **Razão para skip**: nós fazemos Buffett/DRIP de empresas listadas, não PE de privadas. Frameworks são quase ortogonais. ICs e DD checklists são reutilizáveis em conceito mas o LLM já sabe.
- **data** (Astronomer Airflow, 20 skills): airflow, airflow-hitl, analyzing-data, annotating-task-lineage, authoring-dags, checking-freshness, cosmos-dbt-{core,fusion}, creating-openlineage-extractors, debugging-dags, deploying-airflow, managing-astro-{deployments,local-env}, migrating-airflow-2-to-3, profiling-tables, setting-up-astro-{deployments,project}, testing-dags, tracing-{up,down}stream-lineage, troubleshooting-astro-deployments, warehouse-init
  - **Razão para skip**: não usamos Airflow nem Astronomer. SQLite + scheduled tasks chega.
- **figma** (8 skills): figma-{use, use-figjam, create-design-system-rules, create-new-file, generate-design, generate-diagram, generate-library, implement-design, code-connect}
  - **Razão para skip**: não usamos Figma. Mission Control é Next.js artesanal + Helena audit interno.
- **bigdata-com** (1 skill, 10 commands): financial-research-analyst + company-brief, country-analysis, country-sector-analysis, cross-sector, earnings-{digest,preview}, regional-comparison, risk-assessment, sector-analysis, thematic-research
  - **Razão para manter**: MCP server activo e útil; skill é tour-guide do MCP. ✓ manter.
- **market-researcher** (5 skills): competitive-analysis, comps-analysis, idea-generation, pptx-author, sector-overview
  - Quase duplicado de financial-analysis. Manter referência via Agent tool (subagent_type).
- **model-builder** (6 skills): 3-statement-model, audit-xls, comps-analysis, dcf-model, lbo-model, xlsx-author
  - Subset headless de financial-analysis. Manter ou consolidar — decisão.
- **legalzoom** (1 skill, 1 command): attorney-assist, review-contract
  - **Razão para skip**: irrelevante ao escopo investing.
- **hookify** (1 skill, 4 commands): writing-rules, configure, help, hookify, list
  - **Manter** apenas o plugin (não os locais absorvidos) — os locais são duplicados sem valor adicional.
- **exa** (1 skill): search
  - **Manter** — referência ao fetcher que já temos (`fetchers/exa_fetcher.py`).
- **session-report** (1 skill): session-report
  - **Manter** — útil para auditoria de uso de tokens em sessões longas.

---

## 2. Slash commands — `.claude/commands/` (52)

### 2a. Project-native (4)
- `/security-review` — eng meta
- `/systematic-debugging` — eng meta (duplicado de superpowers-*)
- `/verification-before-completion` — eng meta (duplicado de superpowers-*)
- `/writing-plans` — eng meta (duplicado de superpowers-*)

### 2b. Imported (48) — espelham as imports do Tier A/B/C acima.

**Duplicação real**: 3 commands native são exactamente os superpowers absorvidos. Devias **escolher uma das duas vias** e apagar a outra.

---

## 3. Subagents (Claude Code Task tool)

### 3a. `.claude/agents/` locais (4 .md)
- `earnings-reviewer-earnings-reviewer.md` — sell-side post-earnings note
- `hookify-conversation-analyzer.md` — gera hooks anti-padrão de conversas
- `market-researcher-market-researcher.md` — sector primer + comps
- `model-builder-model-builder.md` — Excel-headless DCF/LBO/3-statement

**Uso real**: subagent types `earnings-reviewer:earnings-reviewer`, `market-researcher:market-researcher`, `model-builder:model-builder` aparecem na tool definition mas raramente disparados pela minha lado (Tier A para earnings prep, Tier C para os outros).

### 3b. Subagent types loaded (Claude Code built-in + plugin-provided)
- `claude-code-guide`, `Explore`, `general-purpose`, `Plan`, `statusline-setup` — built-in, todos usados
- `hookify:conversation-analyzer` — único do hookify plugin
- `earnings-reviewer:earnings-reviewer`, `market-researcher:market-researcher`, `model-builder:model-builder` — só os do FSI subagents

---

## 4. Python agents — `agents/` (28 .py + 4 sub-packages)

### 4a. Produção (cron / wired) — ~10
- `perpetuum_master.py` ✓ daily_run
- `chief_of_staff.py` ✓ Telegram + `ii agent`
- `holding_wiki_synthesizer.py` ✓ Phase I (stubs auto)
- `helena_mega.py` + pacote `helena/` (audit/curate/spike/report) ✓ on-demand
- `mega_auditor.py` ✓ Tier-1 cruft detector
- `morning_briefing.py` ✓ `ii brief`
- `daily_synthesizer.py` ✓
- `subscription_fetch.py` ✓ XP/Suno fetcher
- `voice_input.py` + `voice_output.py` ✓ Telegram audio
- `telegram_controller.py` (substituído por `telegram_loop.py`?)

### 4b. CLI on-demand — ~8
- `synthetic_ic.py` ✓ `python -m agents.synthetic_ic`
- `variant_perception.py` ✓
- `decision_journal_intel.py` ✓
- `devils_advocate.py` ✓ (chama-se via Antonio Carlos?)
- `risk_auditor.py` — verificar uso
- `research_scout.py` — verificar uso
- `data_janitor.py` — verificar uso
- `meta_agent.py` — verificar uso

### 4c. Sub-packages (verificar inventário)
- `agents/perpetuum/` — 11 perpetuum modules (autoresearch, bibliotheca, code_health, content_quality, daily_delight, data_coverage, dreaming, library_signals, meta, method_discovery, ri_freshness, security_audit, thesis, token_economy, vault_health, vault_health). Tudo wired via `perpetuum_master.py`.
- `agents/council/` — Council v3 (Story / Personas / Evidence / Versioning / etc.). Wired via `python -m agents.council.story <TK>`.
- `agents/helena/` — Helena Mega (audit / curate / spike / report). Wired via `helena_mega.py`.

### 4d. Possivelmente unused (verificar antes de remover)
- `autoresearch.py` — wrappado em `perpetuum.autoresearch`?
- `analyst_backtest.py` — ainda chamado?
- `fiel_escudeiro.py` — `agents/fiel_escudeiro.py` (Phase EE handoff) — usado pelo MC chat
- `perpetuum_validator.py` — legacy Phase W.5, agora em `perpetuum.thesis`. **Candidato a remover.**
- `portfolio_matcher.py` — verificar uso
- `thesis_refresh.py` vs `thesis_synthesizer.py` — possíveis duplicados
- `skill_scout.py` — Phase W.7 catalogue watcher
- `watchdog.py` — `perpetuum._cron_failures` (Phase EE-AOW)

**Acção sugerida**: correr `python -m agents.mega_auditor` para Tier-1 detect.

---

## 5. Council personas (`obsidian_vault/agents/`) — 10

| Persona | Foco | Reviews recentes |
|---|---|---|
| Aderbaldo Cíclico | commodities/cycles | 2 (PRIO3, VALE3) |
| Charlie Compounder | quality compounders | 11 (AAPL, ABBV, ACN, BRK-B, HD, JNJ, KO, PG, PLTR, TEN, TSLA, TSM) |
| Diego Bancário | bancos BR | 2 (BBDC4, ITSA4) |
| Hank Tier-One | bancos US/global | 6 (BLK, BN, GS, JPM, NU, XP) |
| Lourdes Aluguel | FIIs tijolo | verificar |
| Mariana Macro | macro overlay | verificar |
| Pedro Alocação | allocator | verificar |
| Tião Galpão | FIIs logística | verificar |
| Valentina Prudente | risk/diligence | verificar |
| Walter Triple-Net | NNN REITs (O, etc.) | verificar |

**Acção**: as 4 sem reviews documentados podem ser dummies. Spawn `python -m agents.council.story <TK>` numa watchlist sample e ver se todas disparam.

---

## 6. `ii` command catalog — 133 entradas em CLAUDE.md

Demasiadas para listar uma a uma aqui. **Métrica de saúde**: 60 em uso quotidiano (cron + CLI manual) + 73 raras (one-shot / experimental / debug).

**Top candidates a auditar**:
- Comandos com flag "EXPERIMENTAL" ou "deferred" (ex: `fair_value_forward`, vault_clean_video_names)
- Scripts one-shot identificados como anti-padrão (ex: `itsa4_drip_scenario.py` se ainda existir)
- Comandos com `--all-holdings` que ninguém corre em batch

**Acção**: correr `python -m agents.mega_auditor` (CH008/CH009 categories) para detectar:
- Scripts não importados por ninguém
- Scripts não modificados há >60 dias
- Scripts sem entry em CLAUDE.md mas existentes

---

## 7. Plugins activos + MCPs

### Plugins (17, todos absorvidos para `.claude/` em 2026-05-13)
- **claude-for-financial-services** (7): earnings-reviewer, equity-research, financial-analysis, market-researcher, model-builder, private-equity, wealth-management
- **claude-plugins-official** (10): bigdata-com, chrome-devtools-mcp, claude-md-management, data, exa, figma, hookify, legalzoom, pyright-lsp, playwright, session-report, superpowers, typescript-lsp

### MCP servers loaded (de system reminders desta sessão)
- **claude.ai-hosted** (sempre on): Bigdata.com, FMP, Gmail, Google Calendar, Google Drive, LSEG
- **Plugin-provided**: financial-analysis (aiera, chronograph, daloopa, egnyte, factset, lseg, moodys, morningstar, pitchbook, sp-global — OAuth-gated), figma, playwright
- **Local config**: status-invest, context7, task-master-ai

**Acção**: muitas LSEG/Moodys/S&P-global requerem OAuth e provavelmente não usamos. Verificar quais respondem `authenticate` vs estão a consumir slots.

---

## 8. Recomendações concretas (em ordem de impacto)

### Tier 1 — quick wins (1-2h, zero risco)
1. **Apagar duplicados de superpowers**: escolher entre `.claude/commands/{security-review,systematic-debugging,verification-before-completion,writing-plans}.md` OU os 4 absorvidos `.claude/skills/superpowers-*`. Manter um só.
2. **Reverter absorção do tier C**: rever `scripts/absorb_plugins.py` com lista de exclusão (`data-*`, `figma-*`, `legalzoom-*`, `private-equity-*`). Re-correr → -45 skills.
3. **Remover `agents/perpetuum_validator.py`** (legacy, wrappado em `perpetuum.thesis`).

### Tier 2 — investigar e decidir (3-5h)
4. **Auditoria de scripts órfãos**: `python -m agents.mega_auditor` → identificar scripts sem chamadas. Aprovar individualmente antes de bury.
5. **Consolidar `thesis_refresh.py` vs `thesis_synthesizer.py`**: ler ambos, decidir o canónico.
6. **Auditar Council personas sem reviews**: spawn na watchlist, ver se disparam.
7. **MCPs OAuth não usados**: desligar Pitchbook/Moodys/etc. se não houver workflow real.

### Tier 3 — política de manutenção (estabelecer regra)
8. **Editar `scripts/absorb_plugins.py`** para aceitar `--allow-list` ou `--deny-list` por plugin, evitando re-absorver lixo no próximo refresh.
9. **Criar `scripts/skills_audit.py`** (auto-regenerar este doc após mudanças).
10. **Memory rule nova**: antes de instalar plugin novo, perguntar "que ii ou agent já cobre isto?" — anti-padrão é absorber primeiro e auditar depois.

---

## Próximo passo proposto

Quando voltares, escolhe ordem:

**Opção A — corte cirúrgico agora** (30 min):
- Editar `absorb_plugins.py` com deny-list `data,figma,legalzoom,private-equity` (-45 skills, -21 commands)
- Apagar duplicados superpowers
- Re-correr `absorb_plugins.py`

**Opção B — auditoria sistemática primeiro** (~2h):
- Correr mega_auditor sobre scripts/agents
- Listar candidatos
- Decidir item-a-item

**Opção C — política nova** (~1h):
- Memory rule "consultar antes de absorber"
- `--deny-list` no script
- Cleanup ad-hoc ao longo da semana

A minha sugestão: **A primeiro** (quick wins arrumam o ruído visual no /doctor e nos skill lists) **depois B** (decisões mais informadas sobre o que mantém valor).
