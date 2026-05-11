---
type: roadmap
status: proposal
phase: pre-EE
date: 2026-04-29
horizon: 4-6 weeks
author: claude (overnight planning)
tags: [roadmap, workforce, cron, perpetuum, always-on]
---

# 🌙→☀️ Roadmap: Always-On Workforce

> **Briefing para o teu regresso (saíste 29/04 ~01:30, voltas ~09:30)**
>
> Pediste: *"deveriam trabalhar no background de maneira geral, sempre vendo conteúdos. Ouy a cada hora."*
>
> Hoje: 1 cron diário às 23:30 (~2h) faz tudo de uma vez. Resto do dia, **silêncio total**.
> Ambição: workforce com cadência tier-1 (1h) + tier-2 (4h) + tier-3 (1d) + reactiva (event-driven).
> Restrição-mãe: **zero tokens Claude**. Tudo Ollama/SQL/scripts. Tavily 100/dia.

---

## 1. Estado actual (factual, não diagnóstico)

| Camada | O que existe | Cadência | Gap |
|---|---|---|---|
| **Scheduled Task** | `investment-intelligence-daily` → `daily_run.bat` | 23:30 (1×/dia, 2h) | Sem hourly/4h tasks |
| **Fetchers** | yf_br/us, brapi, fred, bcb, sec_edgar, fiis, news_fetch | 1×/dia dentro do cron | News+earnings poderiam ser hourly |
| **Monitors** | cvm_monitor, sec_monitor (lookback 30d), cvm_pdf_extractor | 1×/dia | SEC 8-K real-time → 22h de delay máx |
| **Perpetuums (12)** | thesis, vault, data_coverage, content_quality, method_discovery, token_economy, library_signals (frozen), ri_freshness, code_health, autoresearch, bibliotheca, meta | Todos rodam juntos 1×/dia | Tier de cadência inexistente |
| **Reactive** | earnings_react, trigger_monitor, notify_events | Apenas como steps do cron | Não dispara quando filing chega |
| **Tavily** | autoresearch + 3 wires (variant/earnings/IC) | Sob demanda + perpetuum diário | Budget 100/dia mal distribuído (15 used yesterday, gasta tudo às 23:45) |
| **Telegram** | captains_log push diário ~23:45 | 1×/dia | Sem severity tiers, sem batching reactivo |
| **YouTube** | yt_ingest manual + yt_ingest_batch | Sob demanda | Channels podiam fazer poll RSS |

**Quota Tavily real (28/Apr)**: 15/100 daily, 162 lifetime, 7d cache cooldown. **80% de budget desperdiçado**.
**Telegram**: 1 push/dia, sem urgência diferenciada (toast de O downgrade ontem foi via `notify_events`, não Telegram).

---

## 2. Mirabolar — 5 designs candidatos

> Listados do mais simples ao mais ambicioso. **Recomendação no fim.**

### A. Tiered Cron (multi-task scheduler) ⭐ recomendado
- **3 Scheduled Tasks** em paralelo:
  - `*-hourly` (a cada hora, ~2-5min): SEC poll, CVM poll, RSS news, autoresearch quota check
  - `*-4h` (a cada 4h, ~10-15min): perpetuums leves (data_coverage, vault, token_economy), YT channel RSS poll
  - `*-daily` (23:30, ~2h): tudo o resto (full perpetuum master, RAG embed, telegram brief)
- **Mecânica**: lockfile por tier (`data/locks/hourly.lock`), evita overlap.
- **Custo**: 0 (já temos Task Scheduler).
- **Risco**: baixo. Só adiciona linhas ao schtasks.
- **Reversibilidade**: alta. Apagar task volta ao estado actual.

### B. Daemon Process (Python loop)
- 1 processo Python permanente com `schedule` lib ou asyncio loop.
- Roda 24/7, dispara funções no horário próprio.
- **Pró**: Estado in-memory entre runs (caches quentes), control flow rico.
- **Contra**: Single point of failure (se cair, ninguém repõe). Precisa supervisor (NSSM/pm2). Memory leak ao longo de dias.
- **Veredito**: overkill para o tamanho do projecto.

### C. Event-Driven (file/DB watchers)
- `watchdog` em `data/cvm_pdfs/` → quando download novo, dispara extractor.
- SEC RSS via webhook (não existe, teria que poll).
- **Pró**: latência mínima.
- **Contra**: complexo, sem ganho material vs poll 1h.
- **Veredito**: só faz sentido se fôssemos competir com terminal Bloomberg.

### D. Hybrid Cron + Long-Poll (já parcialmente)
- Tiered cron (A) + Telegram bot Jarbas continua long-poll para comandos.
- **Pró**: Poll para inputs do user (já está) + cron para outputs proactivos.
- **Veredito**: É o que A já implica de facto. Equivalente a A.

### E. Cloud worker (GCP/AWS Lambda)
- Roadmap longe — out of scope. Custos + secrets + latência sync com SQLite local. Reject.

**📌 Recomendado: A (Tiered Cron).** Simples, reversível, alinhado com cultura "in-house first".

---

## 3. Stress test — 8 modos de falha

| # | Failure mode | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | **Cron overlap** (daily 23:30 ainda corre quando hourly 00:00 dispara) | Média | DB lock, scoring meio-feito | Lockfile per-tier; hourly checa lock daily, abort se busy |
| 2 | **PC sleep** (Windows entra em sleep às 02:00) | Alta | 0 runs até user acordar PC | Power plan: never sleep; ou wake timer no schtasks |
| 3 | **Ollama 500** (saw last night, 2 embed errors) | Recorrente | Embed/thesis falha silenciosa | Health check antes do run + retry com backoff (já temos parcial) |
| 4 | **Tavily quota burst** (reactive 8-K → 5 calls × 3 holdings = 15 num dia agitado) | Média | Quota exhausta, autoresearch falla resto do dia | Budget allocation: 30 daily, 50 hourly-tier, 20 reactive-reserve. `_ratelimit.json` já tem mecânica, falta enforcement por bucket |
| 5 | **brapi token expira / rate-limit** | Baixa | BR fundamentals stale | Status check no início do hourly; flag em meta perpetuum |
| 6 | **Telegram spam** (10 alerts/dia tier P2 → user muta bot) | Alta se sem tier | Perde-se sinal real | Severity P0/P1/P2 + batching: P0 imediato, P1 hourly digest, P2 daily brief |
| 7 | **SQLite WAL crescer sem checkpoint** (hourly writes acumulam WAL, performance degrada) | Média | Dashboard lento | `PRAGMA wal_checkpoint(TRUNCATE)` no fim de cada cron tier |
| 8 | **Disk growth** (logs/yt_ingest.log já 200MB; tavily_cache 163 entries) | Baixa | Nenhum até 100GB | rotate_logs já wired; adicionar tavily_cache TTL 30d |

**Falha não coberta hoje**: nenhum dashboard em tempo real do "estado da workforce". Captain's Log mostra resultados, não health da máquina.

---

## 4. Best practices (aplicáveis a este projecto)

### 4.1 Princípios
1. **Idempotência > correctness**: cada job pode ser re-rodado sem efeito colateral. Já maioria está aí.
2. **Single-writer por DB**: hourly job que escreve em `br_investments.db` não pode coexistir com daily. Lock + tier separation.
3. **Budget por job**: cada perpetuum declara `max_duration_s`, `max_llm_calls`, `max_tavily_calls`. Engine enforce.
4. **Severity-aware notifications**: P0 (broken thesis, dividend cut) → Telegram imediato; P1 (screen drift, downgrade) → hourly digest; P2 (style drift, glossary gap) → daily brief.
5. **Circuit breaker**: 3 erros consecutivos = pausa 24h + alert P1. Já existe esqueleto no perpetuum engine, falta wiring.
6. **Health-first**: cada cron tier começa com `health_check()` (Ollama? brapi? Tavily quota?). Se vermelho, abort + alert.
7. **Observabilidade**: structured JSON logs com `run_id`, `tier`, `job_name`. Já parcial em `logs/`.

### 4.2 Como não queimar Tavily
| Bucket | Daily cap | Quem usa |
|---|---|---|
| Hourly autoresearch | 30 | perpetuum top-30 conviction (cooldown 6d) |
| Daily wire calls | 30 | variant_perception batch + earnings_prep |
| Reactive (event-driven) | 25 | 8-K react, fato_relevante react, paper_trade signal |
| Manual (`ii panorama`, slash commands) | 15 | user-invoked |
| **Total cap** | **100** | hard limit no `_ratelimit.json` |

Hoje: **15 usados, 85 desperdiçados todos os dias**. Reserva total > consumo.

### 4.3 Padrões a copiar (industry)
- **Airflow tier model**: `@hourly`/`@daily`/`@weekly` decorators. Não vamos importar Airflow, mas adoptar a mentalidade.
- **Sentry-style breadcrumbs**: cada perpetuum loga 1 JSON por subject avaliado. Já temos parcialmente.
- **Honeycomb tracing**: `run_id` propagado entre fetcher → monitor → perpetuum. Falta — adicionar.
- **Datadog SLO mindset**: "perpetuum X tem 99% success rate ou pausamos". Captado pelo meta perpetuum, falta SLO threshold formal.

---

## 5. Roadmap fasiado (4-6 semanas)

### Phase EE — Tiered Scheduler ⏱ 1-2 dias
**Objectivo**: separar cron em 3 tiers (hourly/4h/daily).
- [ ] Criar `scripts/hourly_run.bat` + `scripts/q4h_run.bat`
- [ ] Adicionar 2 Scheduled Tasks (`*-hourly`, `*-4h`) com lockfile
- [ ] Refactor `daily_run.bat`: tirar steps que vão para hourly/4h, garantir idempotência
- [ ] `agents/_lock.py` — context manager para lockfile per-tier
- [ ] Smoke test: correr os 3 tiers em série local; verificar não há lock contention

**Critério de done**: 3 tasks no schtasks, 0 overlap em 24h de observação.

### Phase FF — Stream Layer ⏱ 2-3 dias
**Objectivo**: feeds de conteúdo continuamente vistos.
- [ ] **SEC 8-K poll hourly** (substituir `--lookback-days 30` daily por `--since-last-poll` hourly)
- [ ] **CVM fatos relevantes hourly** (10:00-18:00 BRT, fora desse range skip)
- [ ] **News RSS hourly** (`fetchers/news_fetch.py --classify` hourly, classifier Qwen local)
- [ ] **YouTube channels RSS** (4h tier; quando vídeo novo dropa, queue para `yt_ingest`)
- [ ] **earnings_calendar refresh** 4h (próximas 30d)
- [ ] **Bigdata.com events_calendar** (4h tier para holdings + watchlist top-50)

**Critério de done**: 24h de observação → SEC/CVM/News/YT events arrived sem perder nenhum (cross-check vs RSS manual).

### Phase GG — Reactive Engine ⏱ 2-3 dias
**Objectivo**: quando algo material chega, perpetuum dispara em segundos, não 22h depois.
- [ ] Tabela `event_queue` em ambas DBs (eventos pending de processar)
- [ ] Hourly: scan event_queue → invoca handler apropriado (`react_8k`, `react_fato`, `react_div_cut`)
- [ ] `react_8k` (US): autoresearch + dossier update + Telegram P1
- [ ] `react_fato_relevante` (BR): cvm_pdf_extractor + autoresearch + Telegram P1
- [ ] `react_screen_break`: quando trigger_monitor flag holding screen broke (como O ontem) → P0 Telegram + auto-sized open action
- [ ] Severity-aware Telegram (P0 imediato / P1 hourly digest / P2 daily)

**Critério de done**: simular 8-K via test fixture → dossier actualizado + Telegram P1 enviado em < 5min.

### Phase HH — Budget & Health ⏱ 1-2 dias
**Objectivo**: não rebentar quotas, não rodar em ambiente partido.
- [ ] `agents/_health.py` — `check_ollama()`, `check_brapi()`, `check_tavily_quota()` (boolean + reason)
- [ ] Cada cron tier: health-first, abort com alert se vermelho
- [ ] Tavily budget allocation por bucket (ver §4.2) — wire em `_ratelimit.json` com keys `bucket`
- [ ] Circuit breaker: `meta` perpetuum pausa job com 3 erros consecutivos por 24h

**Critério de done**: simular Ollama down → hourly tier aborta com Telegram P0 "infra fora", retoma quando volta.

### Phase II — Live Workforce Page ⏱ 1 dia
**Objectivo**: 1 click vê o estado da máquina.
- [ ] Streamlit page nova `pages/Workforce.py`:
  - Próximos 3 jobs agendados (de schtasks)
  - Últimos 10 runs (tier, duration, status, errors)
  - Tavily quota meter (hourly + daily) com colour-coded progress bar
  - Ollama up/down + última latência
  - Event queue depth
- [ ] Adicionar à nav do dashboard (segunda página depois do Captain's Log)

**Critério de done**: page renderiza com dados reais; posso ver de manhã sem CLI.

### Phase JJ — Tuning & Telegram Refinement ⏱ ongoing
- [ ] Calibrar severity thresholds depois de 1 semana de observação real
- [ ] Telegram inline buttons (`/approve`, `/snooze`, `/dossier <TK>`) — usa Jarbas long-poll já existente
- [ ] Weekly digest aos domingos 20:00: roll-up das 168h passadas

---

## 6. Decisões abertas (preciso de teu input ao acordar)

1. **PC awake policy**: posso alterar power plan para "never sleep when AC", ou queres manter sleep? Sem isto, hourly só roda quando estás em frente.
2. **Telegram severity P0**: quais eventos? Sugiro: `dividend cut announced`, `holding screen broke ≥2 dias seguidos`, `8-K item 5.02 (CEO/CFO change)`, `8-K item 4.01 (auditor change)`.
3. **YouTube channels** a fazer poll: existem 442 subjects/dia mencionados em Phase X mas não sei quais channels específicos estão tracked. Listar os top-10 para começar.
4. **Bigdata.com events_calendar wiring**: invocar via MCP custa Claude tokens (a forma como acessas o Bigdata é via Anthropic-managed MCP). Confirma — talvez fica fora do "in-house first" e não inclua.
5. **Phase EE.1 vs EE.2 tradeoff**: começar hourly só com SEC/CVM (evidence-driven, alta valor) ou full broadcast (RSS+news+YT) de uma só vez?

---

## 7. O que **não** vou mexer sem ordem explícita

- ❌ Nada que escreva em produção sem dry-run primeiro (regra mãe).
- ❌ `data/` writes em batch >100 rows.
- ❌ `git push --force` (nunca, ever).
- ❌ Phase BB-DD existing perpetuums — refactor virá no fim, depois de tier scheduler estabilizar.
- ❌ Subscription cookies — esses são teus.

---

## 8. Atalho de retoma quando voltares

```bash
# 1. Ver este roadmap (já abriste se estás a ler)

# 2. Verificar que daily cron rodou enquanto estavas fora (vai correr hoje 23:30)
ls -lt logs/daily_run_*.log | head -3

# 3. Status workforce actual
sqlite3 data/us_investments.db "SELECT COUNT(*) FROM events WHERE event_date >= date('now','-1 day')"

# 4. Aprovar Phase EE para arrancar
# Diz-me: "go EE" → eu monto tiered cron + lockfile + dry-run smoke test
```

---

## 9. ETA total

- **Phase EE+FF+GG (core)**: 5-8 dias de trabalho dedicado, ou 2-3 semanas em background
- **Phase HH+II**: +2 dias
- **Phase JJ ongoing**: indefinido, melhora com observação

**Quick win possível em 1h** (se aprovares ao acordar): apenas Phase EE.1 — adicionar 1 hourly task que corre `sec_monitor` + `cvm_monitor` + `news_fetch --classify`. Isto sozinho leva-nos de **22h delay** para **<1h delay** em filings críticos. 80/20.

---

*Gerado em 2026-04-29 ~02:00 enquanto dormias. Sem implementação até "go".*
