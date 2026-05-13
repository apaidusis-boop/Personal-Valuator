---
type: agents_review
tags: [agents, review, audit]
date: 2026-05-13
status: aligned_with_AGENTS_REGISTRY
---

# Agents Review

> **Versão alinhada** com handles canónicos do [[AGENTS_REGISTRY]] (era a fonte que devia estar a usar desde o início).
> Tabela de TODOS os agents (~80). Colunas: **handle** · **persona alias** · **o que faz** · **estado**.
>
> **Legenda estado**:
> - ✅ usado (cron / CLI regular / Telegram)
> - 🟡 ocasional / on-demand
> - ⚪ adormecido / frozen
> - ❌ legacy (substituído)

---

## Decisões executadas (2026-05-13 overnight cleanup)
- ✂️ **Bigdata** removido (skills locais + deny-list)
- 🔒 **figma** + **private-equity** mantidos (revertido)
- ✂️ **26 items buried** via mega_auditor → `cemetery/2026-05-13/`
- ✂️ **7 pre-LL deepdives** buried (ACN, JNJ duplicados, KO, XPML11)
- ✅ **Council personas aliased** com handles canónicos (front-matter `handle:` injectado)
- 📊 **JNJ deepdive A/B** comparison gerada — ver [[Sessions/JNJ_Deepdive_Comparison_PreLL_vs_Now]]

---

## 1. Ops (5 agentes) — operações diárias

| Handle | Persona (alias) | O que faz | Estado |
|---|---|---|:---:|
| `ops.briefing` | Aurora Matina | Briefing matinal Telegram (07:00) | ✅ |
| `ops.watchdog` | Wilson Vigil | Polling 15min — triggers + earnings + cron failures | ✅ |
| `ops.telegram-bridge` | Zé Mensageiro | Long-poll Telegram (`scripts/telegram_loop.py`) | ✅ |
| `ops.orchestrator` | Antonio Carlos / Fiel Escudeiro | Tool-calling 16 tools | 🟡 on-demand |
| `ops.janitor` | Noé Arquivista | Archive >180d, VACUUM SQLite (weekly sat 03:00) | ✅ |

## 2. Research (10 agentes)

| Handle | Persona (alias) | O que faz | Estado |
|---|---|---|:---:|
| `research.scout` | Ulisses Navegador | Scout filings CVM/SEC + news (daily 08:30) | ✅ |
| `research.thesis-refresh` | Teresa Tese | Re-injecta Live Snapshot em wiki (sun 22:00) | ✅ |
| `research.subscriptions` | Sofia Clippings | Fetch Suno/XP/WSJ (mon 09:00) | ✅ |
| `research.autoresearch` | (perpetuum K) | Tavily top-30 conviction; cache 7d | ✅ |
| `research.ic-debate` | Synthetic IC | Debate 5 personas Buffett/Druck/Taleb/... | 🟡 |
| `research.variant` | Variant Perception | We vs analyst consensus | 🟡 |
| `research.journal` | Decision Journal Intel | Pattern mining P1-P5 perpetuums | 🟡 |
| `research.wiki-stub` | Holding Wiki Synthesizer | Auto stubs `wiki/holdings/*.md` | 🟡 |
| `research.thesis-stub` | Thesis Synthesizer | Auto `## Thesis` sections | ✅ |
| `discovery.skills` | Skill Scout | Caça skills novos no GitHub (weekly) | 🟡 |

## 3. Risk & Compliance (5 agentes)

| Handle | Persona (alias) | O que faz | Estado |
|---|---|---|:---:|
| `risk.drift-audit` | Valentina Prudente | Detecta drift de tese (daily 21:00) | ✅ |
| `risk.devils-advocate` | Diabo Silva | Bear case (wed 10:00) | ✅ |
| `risk.compliance` | Regina Ordem | Audita auditores (daily 23:00) | ✅ |
| `risk.thesis-health` | (perpetuum) | Validator daily das theses | ✅ |
| `risk.security` | (perpetuum) | Read-only host hygiene | ✅ |

## 4. Performance & Allocation (2 agentes)

| Handle | Persona (alias) | O que faz | Estado |
|---|---|---|:---:|
| `perf.backtest-analysts` | Aristóteles Backtest | Backtest predictions (fri 20:00) | ✅ |
| `perf.portfolio-matcher` | Clara Fit | Mapeia insights → holdings (every 30m) | ✅ |

## 5. Design (6 agentes)

| Handle | Persona (alias) | O que faz | Estado |
|---|---|---|:---:|
| `design.lint` | Helena Linha (audit) | Linter DS001-DS010 | ✅ |
| `design.scout` | Helena Linha (scout) | GitHub+RSS+YouTube (sun 23:30) | ⚪ (YouTube key missing) |
| `design.curate` | Helena Mega curate | Tier INSTALL/CONSIDER/SKIP skills | ⚪ static |
| `design.spike` | Helena Mega spike | Path A/B/C/D feasibility | ⚪ static |
| `design.cruft-detector` | Mega Auditor | T1 cruft detector | 🟡 (corri agora) |
| `design.code-lint` | (perpetuum CH) | CH001-CH007 anti-patterns | ✅ |

## 6. Council Specialists (9 agentes — on-demand, multi-persona debate)

| Handle | Persona (alias) | Foco | Reviews | Estado |
|---|---|---|---:|:---:|
| `council.macro` | Mariana Macro | Macro overlay BR+US | 32 | ✅ |
| `council.allocation` | Pedro Alocação | Sizing + correlação | 32 | ✅ |
| `council.industrials-us` | Charlie Compounder | Modo A-US Buffett | 12 | ✅ |
| `council.fiis-br` | Lourdes Aluguel | Modo D-BR FIIs | 7 | ✅ |
| `council.banks-us` | Hank Tier-One | Modo B-US bancos | 6 | 🟡 |
| `council.banks-br` | Diego Bancário | Modo B-BR bancos | 2 | 🟡 |
| `council.commodities-br` | Aderbaldo Cíclico | Modo C-BR cíclicos | 2 | ⚪ |
| `council.industrials-br` | Tião Galpão | Modo A-BR não-banco | 2 | ⚪ |
| `council.reits-us` | Walter Triple-Net | Modo D-US REITs | 2 | ⚪ |

**Nota** `council.risk` = `risk.drift-audit` (Valentina Prudente) — overlap, considerar consolidar nomenclatura.

## 7. Perpetuums (15 daemons — background validation diária)

Todos correm via `perpetuum.master` no cron 23:30.

| Handle | O que faz | Estado |
|---|---|:---:|
| `perp.thesis` ⭐ | Backfill / refresh thesis universe-wide | ✅ |
| `perp.vault-health` | Drift, broken links, orphans (1610 notes scanned) | ✅ |
| `perp.data-coverage` | Detecta gaps em fundamentals/prices | ✅ |
| `perp.bibliotheca` | Sector + name backfill | ✅ |
| `perp.ri-freshness` | RI/CVM filing freshness | ✅ |
| `perp.code-health` | CH001-CH007 codebase | ✅ |
| `perp.autoresearch` | Tavily top-30 conviction | ✅ |
| `perp.method-discovery` | Books → methods extraction | ✅ |
| `perp.security` | Host hygiene scan | ✅ |
| `perp.meta` | Audita os outros perpetuums | ✅ |
| `perp.content-quality` | Quality dos artefactos | ⚪ frozen |
| `perp.token-economy` | Token usage tracking | ⚪ frozen |
| `perp.library-signals` | Method-match signals | ⚪ frozen |
| `perp.dreaming` | Consolida daily_logs → DREAMS.md | ⚪ manual |
| `perp.daily-delight` | Topic-of-the-day | ⚪ manual |

## 8. Built-in Claude Code subagents (5)

Via Task tool com `subagent_type=...`.

| Handle | O que faz | Estado |
|---|---|:---:|
| `general-purpose` | Pesquisa multi-step | ✅ |
| `Explore` | Read-only Glob + Grep | ✅ |
| `Plan` | Architect strategy | 🟡 |
| `claude-code-guide` | Q&A sobre Claude Code | 🟡 |
| `statusline-setup` | Configurar statusline | ⚪ |

## 9. Plugin subagents (4) + cópias absorvidas (4)

| Handle (plugin) | Cópia local | Estado |
|---|---|:---:|
| `earnings-reviewer:earnings-reviewer` | `.claude/agents/earnings-reviewer-earnings-reviewer.md` | ⚪ |
| `market-researcher:market-researcher` | `.claude/agents/market-researcher-market-researcher.md` | ⚪ |
| `model-builder:model-builder` | `.claude/agents/model-builder-model-builder.md` | ⚪ |
| `hookify:conversation-analyzer` | `.claude/agents/hookify-conversation-analyzer.md` | ⚪ |

---

## 10. Heartbeat / never-stop infra (5)

Não são "agents" mas garantem continuidade.

| Componente | Reference | O que faz |
|---|---|---|
| Health probes + circuit breaker | `agents/_health.py` | 8 probes; 3 fails → TRIPPED 24h |
| Retry wrapper | `scripts/_retry.py` | 3 attempts × backoff 1m/5m/15m |
| Heartbeat checklist | `agents/_heartbeat.py` | Replay de steps falhados |
| Cron failure detector | `agents.watchdog._cron_failures()` | Telegram alert em LastTaskResult ≠ 0 |
| Lock file | `agents/_lock.py` | Daily lock blocks hourly+q4h |

---

## Decisões pendentes (para a tua revisão matinal)

### 🟢 Manter / promover
- ⭐ `perp.thesis` (Heart of Phase W) — core
- ⭐ `ops.briefing` + `ops.watchdog` — cron quotidianos
- ⭐ `research.subscriptions` (Sofia Clippings) — base do clipping auto-tag futuro
- ⭐ Council top-4 (`council.macro`, `council.allocation`, `council.industrials-us`, `risk.drift-audit/Valentina`) — 108 reviews acumulados

### 🟡 Investigar (não actuar overnight)
- ❓ `council.commodities-br` (Aderbaldo) / `council.industrials-br` (Tião) / `council.reits-us` (Walter) — só 2 reviews cada. Spawn na watchlist amanhã para validar relevância.
- ❓ `perp.content-quality`, `perp.token-economy`, `perp.library-signals` — todos frozen. Descongelar ou bury?
- ❓ `perp.dreaming` + `perp.daily-delight` — OpenClaw-era. Mantemos?
- ❓ `research.scout` (Ulisses) vs `research.autoresearch` — overlap? Confirmar.
- ❓ `risk.compliance` vs `risk.drift-audit` — overlap? Confirmar.

### 🔴 Já buried tonight
- ✂️ 5 ficheiros `agents/roles/*.py` (CODE-DEAD, dummy stubs)
- ✂️ 4 vault notes vazias
- ✂️ 3 pastas vazias
- ✂️ 14 scripts one-shot datados (`extend_2026-05-09.py`, `midnight_2026-05-09.py`, migrações, seeds, etc.)
- ✂️ 7 pre-LL deepdives (mantido só `JNJ_20260429_2105` para A/B reference)

---

## Cross-links
- Source canónica: [[AGENTS_REGISTRY]]
- Manual operacional: [[Manual_do_Sistema]]
- Filosofia: [[CONSTITUTION]] · [[CONSTITUTION_Pessoal]]
- Cemetery: `cemetery/2026-05-13/manifest.md` (26 + 7 = 33 items)
- A/B comparison: [[Sessions/JNJ_Deepdive_Comparison_PreLL_vs_Now]]
- Memory rules: [[feedback_agent_function_names]] · [[feedback_inhouse_first]]
