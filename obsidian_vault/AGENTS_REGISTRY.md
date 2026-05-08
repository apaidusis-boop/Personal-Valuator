---
type: registry
purpose: canonical human-readable index of every agent in the system
updated: 2026-05-08
machine_source: config/agents.yaml + agents/perpetuum/_registry.py
edit: this file is human-curated; the YAML stays authoritative for the cron runner
---

# AGENTS_REGISTRY — fonte única humana

Convenção de nomes (renamed 2026-05-08): **`area.funcao`** (kebab-case CLI handle).
Adeus às personas (Antonio Carlos, Helena Linha, Tião Galpão...) — cada agente
agora é um substantivo do seu trabalho. Eles continuam tendo `employee_name` em
`config/agents.yaml` para narrative briefings, mas o **handle técnico** segue a
convenção nova.

> **Como ler a tabela**: cada linha é um agente activo no sistema. Coluna
> "Estado" reflecte o último ciclo conhecido (✅ rodando / ⚠️ adormecido /
> 🔴 partido / ⚪ on-demand). Reference é o ficheiro fonte. Modus é
> exactamente como o agente faz o seu trabalho — fonte de dados, modelo,
> cadência.

---

## Operations (5 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|---|
| `ops.briefing` | Aurora Matina | Briefing matinal Telegram | `agents/morning_briefing.py` | daily 07:00 → SQL aggregations + Ollama Qwen 14B narrative + Telegram push | ✅ |
| `ops.watchdog` | Wilson Vigil | Polling 15min — extrair pending + alertar triggers + earnings reminders + **cron failure detection** (novo 2026-05-08) | `agents/watchdog.py` | every:15m → SQL polling + PowerShell `Get-ScheduledTaskInfo` para detectar cron fails > 0 → emergency Telegram + HEARTBEAT.md replay entry | ✅ |
| `ops.telegram-bridge` | Zé Mensageiro | Long-poll Telegram → despacha comandos | `agents/telegram_controller.py` + `scripts/telegram_loop.py` | every:2m getUpdates timeout=25s; despacha texto livre para `ops.orchestrator` | ✅ |
| `ops.orchestrator` | Antonio Carlos / Fiel Escudeiro | Pergunta livre → tool-calling loop sobre 16 tools | `agents/chief_of_staff.py` (Qwen 32B) + `agents/fiel_escudeiro.py` (Claude CLI) | Manual; memória conversacional em `data/chief_memory.db` | ⚪ on-demand |
| `ops.janitor` | Noé Arquivista | Archive >180d, dedup, VACUUM SQLite | `agents/data_janitor.py` | weekly:sat:03:00; pure SQL | ✅ |

## Research (7 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|---|
| `research.scout` | Ulisses Navegador | Scout filings CVM/SEC + news + gaps | `agents/research_scout.py` | daily 08:30; yfinance + EDGAR + CVM IPE; dedup events table | ✅ |
| `research.thesis-refresh` | Teresa Tese | Re-injecta Live Snapshot em wiki/holdings | `agents/thesis_refresh.py` | weekly:sun:22:00; ler thesis_health → escrever vault | ✅ |
| `research.subscriptions` | Sofia Clippings | Fetch Suno/XP/WSJ/Finclass weekly | `agents/subscription_fetch.py` + `fetchers/subscriptions/` | weekly:mon:09:00; cookies em `data/subs_cookies.db`; rendering DOM scraping | ✅ |
| `research.autoresearch` | (perpetuum K) | Tavily web research top-30 conviction | `agents/autoresearch.py` + `agents/perpetuum/autoresearch.py` | Cache 7d + rate-limit bucket `hourly_autoresearch` (30/dia); cooldown 6d/ticker | ✅ |
| `research.ic-debate` | Synthetic IC | Debate 5 personas Buffett/Druck/Taleb/Klarman/Dalio | `agents/synthetic_ic.py` | Manual; Ollama 14B; majority N=3 | ⚪ on-demand |
| `research.variant` | Variant Perception | We vs analyst consensus | `agents/variant_perception.py` | Manual; word-boundary regex + Tavily wire | ⚪ on-demand |
| `research.journal` | Decision Journal Intel | Agrega P1-P5 patterns dos perpetuums | `agents/decision_journal_intel.py` | Manual; pure SQL aggregation | ⚪ on-demand |

## Risk & Compliance (5 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|---|
| `risk.drift-audit` | Valentina Prudente | Detecta drift de tese | `agents/risk_auditor.py` | daily:21:00; rules + Ollama narrative | ✅ |
| `risk.devils-advocate` | Diabo Silva | Bear case para cada bull case | `agents/devils_advocate.py` | weekly:wed:10:00; Ollama prompt invertido | ✅ |
| `risk.compliance` | Regina Ordem | Audita os auditores; auto-disable após 3 falhas | `agents/meta_agent.py` | daily:23:00; lê state files | ✅ |
| `risk.thesis-health` | Perpetuum Validator | Validator daily das theses | `agents/perpetuum_validator.py` | Daily; thesis_health table; rules deterministic | ✅ |
| `risk.security` | (perpetuum) | Read-only host hygiene | `agents/perpetuum/security_audit.py` | Diário; escreve `SECURITY_AUDIT.md` | ✅ |

## Performance & Allocation (2 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|---|
| `perf.backtest-analysts` | Aristóteles Backtest | Backtest predictions vs real moves | `agents/analyst_backtest.py` | weekly:fri:20:00; horizons 30/90/180d | ✅ |
| `perf.portfolio-matcher` | Clara Fit | Mapeia insights → holdings/watchlist | `agents/portfolio_matcher.py` | every:30m; relevance score | ✅ |

## Design (6 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|---|
| `design.lint` | Helena Linha (audit) | Linter DS001-DS010 sobre 94 .py + .md | `agents/helena/audit.py` | AST + regex; output `Helena_Mega/01_Audit.md` | ✅ (correu hoje) |
| `design.scout` | Helena Linha (scout) | GitHub + RSS + YouTube weekly scout | `scripts/design_research.py` | sun:23:30; **GitHub OK, RSS OK (Refactoring UI 404), YouTube OFF (sem API key), GitHub sem token (60/h)** | ⚠️ adormecido (fix wired 2026-05-08, próximo sun) |
| `design.curate` | Helena Mega curate | Tier INSTALL/CONSIDER/SKIP de skills externos | `agents/helena/curate.py` | **STATIC hoje** — precisa virar RAG sobre Design_Watch.md | ⚠️ static |
| `design.spike` | Helena Mega spike | Path A/B/C/D platform feasibility | `agents/helena/spike.py` | **STATIC hoje** | ⚠️ static |
| `design.cruft-detector` | Mega Audit | Detecta cruft de código/vault | `agents/mega_auditor.py` | Manual; 8 categorias; nunca apaga; quarantine via cemetery | ⚪ on-demand |
| `design.code-lint` | (perpetuum CH) | CH001-CH007 anti-patterns no Python | `agents/perpetuum/code_health.py` | Diário; AST scan 170 .py | ✅ |

## Specialists (Council — on-demand consultants, 9 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi |
|---|---|---|---|---|
| `council.banks-br` | Diego Bancário | Voice Modo B-BR (BBDC4, ITUB4, ITSA4...) | `agents/council/personas.py` | Convocado pelo coordinator quando ticker.modo=B & jurisdiction=BR; veta Graham/ND-EBITDA |
| `council.banks-us` | Hank Tier-One | Voice Modo B-US (JPM, BAC, GS...) | idem | Veta P/B sem tangible adjust; streak pre-2009 não conta |
| `council.industrials-br` | Tião Galpão | Modo A-BR não-banco | idem | Graham clássico ajustado; veta P/E sem sector anchor |
| `council.industrials-us` | Charlie Compounder | Modo A-US (Buffett) | idem | Aristocrats first; veta yield sem buyback layer |
| `council.commodities-br` | Aderbaldo Cíclico | Modo C-BR cíclicos | idem | Mid-cycle EBITDA only; veta valuation at peak earnings |
| `council.fiis-br` | Lourdes Aluguel | Modo D-BR FIIs | idem | Cap rate vs NTN-B; veta Piotroski/Altman em FII |
| `council.reits-us` | Walter Triple-Net | Modo D-US REITs | idem | AFFO over FFO; veta single-tenant concentration unflagged |
| `council.macro` | Mariana Macro | Cross-cutting macro voice | idem | Convocada quando macro_exposure ≥ 4 |
| `council.allocation` | Pedro Alocação | Sizing + correlação + currency isolation | idem | Veta concentração >10% sem tese explícita |

## Perpetuums (15 daemons já noun-by-area — sem rename)

| Handle | Faz | Reference | Modus operandi | Estado |
|---|---|---|---|---|
| `perp.thesis` | Backfill / refresh thesis universe-wide | `agents/perpetuum/thesis.py` | T2; Ollama Qwen 14B | ✅ |
| `perp.vault-health` | Drift, broken links, orphans no vault | `agents/perpetuum/vault_health.py` | T1; pure FS scan | ✅ |
| `perp.data-coverage` | Detecta gaps em fundamentals/prices | `agents/perpetuum/data_coverage.py` | T1; SQL coverage report | ✅ |
| `perp.content-quality` | Quality dos artefactos | `agents/perpetuum/content_quality.py` | T2 frozen | ⚠️ |
| `perp.method-discovery` | Books → methods extraction | `agents/perpetuum/method_discovery.py` | Ollama; library/extract_insights | ✅ |
| `perp.token-economy` | Token usage tracking | `agents/perpetuum/token_economy.py` | T2 frozen | ⚠️ |
| `perp.library-signals` | Signals de método-match | `agents/perpetuum/library_signals.py` | Frozen | ⚠️ |
| `perp.ri-freshness` | RI/CVM filing freshness | `agents/perpetuum/ri_freshness.py` | T1 | ✅ |
| `perp.code-health` | CH001-CH007 codebase | `agents/perpetuum/code_health.py` | T1 daily | ✅ |
| `perp.autoresearch` | Tavily top-30 conviction | `agents/perpetuum/autoresearch.py` | T2; rate-limit bucket | ✅ |
| `perp.bibliotheca` | Sector + name backfill | `agents/perpetuum/bibliotheca.py` | T1; BIB001-004 signals | ✅ |
| `perp.dreaming` | Consolida daily_logs → DREAMS.md | `agents/perpetuum/dreaming.py` | Manual trigger | ⚪ |
| `perp.security` | Host hygiene scan | `agents/perpetuum/security_audit.py` | T1 read-only | ✅ |
| `perp.daily-delight` | Topic-of-the-day | `agents/perpetuum/daily_delight.py` | Manual | ⚪ |
| `perp.meta` | Audita os outros perpetuums | `agents/perpetuum/meta.py` | Sempre last | ✅ |

## Discovery / Stubs (3 agentes)

| Handle novo | Persona (legacy) | Faz | Reference | Modus operandi |
|---|---|---|---|---|
| `discovery.skills` | skill_scout | Caça skills novos no GitHub | `agents/skill_scout.py` | Weekly; mesma engine que `design.scout` |
| `research.wiki-stub` | holding_wiki_synthesizer | Auto-gera stubs `wiki/holdings/*.md` | `agents/holding_wiki_synthesizer.py` | Ollama; auto_draft:true |
| `research.thesis-stub` | thesis_synthesizer | Auto-gera `## Thesis` sections | `agents/thesis_synthesizer.py` | Ollama Qwen 14B local |

---

## Heartbeat / never-stop infrastructure (Phase 2026-05-08)

Componentes que garantem que **nada pode parar em silêncio**:

| Componente | Reference | O que faz |
|---|---|---|
| Health probes + circuit breaker | `agents/_health.py` | 8 probes: ollama, yfinance, fmp, tavily, **cvm**, **sec**, **fred**, **bcb**. 3 fails consecutivos → TRIPPED 24h, auto-reset. |
| Retry wrapper | `scripts/_retry.py` | Wrap qualquer step com 3 attempts × backoff 1m/5m/15m. Final fail → HEARTBEAT.md row + Telegram alert. |
| Heartbeat checklist | `agents/_heartbeat.py` + `obsidian_vault/workspace/HEARTBEAT.md` | Replay de steps falhados na próxima run. |
| Cron failure detector | `agents.watchdog._cron_failures()` | A cada 15min: lê `Get-ScheduledTaskInfo`. Se LastTaskResult ≠ 0 → 🚨 Telegram + HEARTBEAT replay row. |
| Lock file | `agents/_lock.py` | Daily lock blocks hourly+q4h. Auto-recovery via PID OpenProcess. |

### Steps wrapped com retry no `daily_run.bat` (5/19)

- `BR-DAILY` (3×, network heavy)
- `US-DAILY` (3×, network heavy)
- `PERPETUUM` (2×, Ollama+Tavily heavy)
- `TELEGRAM-BRIEF` (3×, Telegram API)
- `DESIGN-SCOUT` (3×, Sunday only)

Os outros 14 steps são SQL puro / FS-only / Ollama local-only — falha rara,
re-run idempotente, retry desnecessário.

---

## Pending founder actions (HEARTBEAT.md / `~/.heartbeat-pending`)

| Acção | Comando | Por quê |
|---|---|---|
| Activar YouTube source no `design.scout` | adicionar `YOUTUBE_API_KEY=...` ao `.env` (Google Cloud Console → Data API v3, free 10k units/dia) | Sem API key, design scout só vê GitHub+RSS; perdemos Vibe Design / Refactoring UI / Pentagram tutorials |
| Aumentar rate limit GitHub | adicionar `GITHUB_TOKEN=...` ao `.env` (PAT scope `read:public_repo`) | 60/h → 5000/h, design.scout pode alargar queries |
| Registar hourly tier no Windows Scheduler | `schtasks /Create /SC HOURLY /TN "ii-hourly" /TR "C:\Users\paidu\investment-intelligence\scripts\hourly_run.bat" /F` | Phase EE-AOW pendente; sem isto hourly só corre quando alguém chama à mão |
| Registar q4h tier | `schtasks /Create /SC HOURLY /MO 4 /TN "ii-q4h" /TR "C:\Users\paidu\investment-intelligence\scripts\q4h_run.bat" /F` | idem |

---

## Cross-links

- `config/agents.yaml` — fonte máquina (cron runner)
- `agents/perpetuum/_registry.py` — registry dos 15 perpetuums
- `obsidian_vault/CONSTITUTION.md` — princípios não-negociáveis
- `agents/_health.py` — probes + circuit breaker
- `scripts/_retry.py` — retry wrapper
- `obsidian_vault/workspace/HEARTBEAT.md` — replay queue

## Changelog

- **2026-05-08**: Renomes área-noun + 4 probes novos (cvm/sec/fred/bcb) + retry wrapper + cron failure detector. Daily 2026-05-07 morreu em CVM SSL — root cause fixed.
