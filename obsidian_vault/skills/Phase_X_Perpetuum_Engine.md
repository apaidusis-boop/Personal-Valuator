---
type: phase_design
phase: X
tags: [phase_x, perpetuum, engine, autonomy]
status: scaffolded
date: 2026-04-24
---

# 🔁 Phase X — The Perpetuum Engine

> **Context**: Phase W Gold introduziu `perpetuum_validator` para thesis de tickers. User expandiu visão — perpetuum é pattern arquitectural, não feature única. Phase X generaliza.

## 🎯 A tese

**Thesis validation** foi caso particular. O pattern real é:

> _Qualquer processo que melhore por observação repetida + scoring contra baseline é candidato a perpetuum._

Domínios onde aplicamos:

1. **Thesis de tickers** ✅ (Phase W.5, já activo)
2. **Saúde de vault notes** ✅ (Phase X, activo)
3. **Cobertura de dados** ✅ (Phase X, activo)
4. **Content quality** (futuro) — briefings decay, signal-to-noise
5. **Workflow efficiency** (futuro) — exec logs, bottlenecks, wasted LLM calls
6. **Method discovery** (futuro) — autoresearch descobre novos papers/repos aplicáveis
7. **Assumption challenging** (futuro) — periodically questions CLAUDE.md thresholds

O sistema vai **aprendendo sobre si mesmo** todos os dias.

## 🏗️ Arquitectura

```
agents/perpetuum/
├── __init__.py            # public API
├── _engine.py             # BasePerpetuum + PerpetuumResult + shared schema
├── _registry.py           # REGISTRY of perpetuums
├── thesis.py              # [T1] thesis por ticker
├── vault_health.py        # [T1] saúde de notas (orphans, stale, broken links)
├── data_coverage.py       # [T1] data completeness por holding
├── content_quality.py     # (futuro) signal-to-noise de briefings
├── workflow.py            # (futuro) exec log analysis
└── method_discovery.py    # (futuro) autoresearch sobre novos métodos

agents/perpetuum_master.py  # runner unificado
```

Shared DB schema:
- `perpetuum_health` — unified (perpetuum_name, subject_id, run_date, score, flags, tier, action_hint)
- `perpetuum_run_log` — exec metadata per run

Cada perpetuum declara `autonomy_tier` (T1..T5) que governa quanto pode actuar sozinho.

## 📶 Autonomy Tiers

| Tier | Nome | Agent faz... | User faz... | Exemplo |
|---|---|---|---|---|
| **T1** | Observer | detecta + regista | revê alertas Telegram | perpetuums actuais |
| **T2** | Proposer | detecta + **propõe action** escrita em `open_actions` | one-click approve | próximo passo vault_health |
| **T3** | Sandboxed | actua em **dry-run branch/worktree** | revê diff depois | data_coverage pode auto-fetch |
| **T4** | Guarded | actua em produção com **hard limits** | auditoria semanal | rebalance com cap diário |
| **T5** | Autonomous | actua livremente | sample audits | só após 6m sem falso positivo |

**Promoção de tier requer**: (a) 30d estabilidade T-1, (b) 0 falsos positivos críticos, (c) backtest explicitamente validado.

## 🔬 Autoresearch como backbone dos perpetuums externos

Para perpetuums futuros que dependem de **evidência externa**:

- `perpetuum_method` — autoresearch queries: "new dividend safety metric 2026", "Piotroski F-score improvements", "Graham criteria in high-rate regimes"
- `perpetuum_thesis` (ganha braço externo) — queries: "contradicting evidence for <thesis>", "recent analyst downgrades"
- `perpetuum_assumptions` — queries: "is DY >6% BR threshold still valid with Selic 11%?" → evidence summary → suggested CLAUDE.md update

Backend: **GPT Researcher** (Sprint W.5) ou **autoresearch Karpathy**, conforme A/B test.

## 📊 Estado live (2026-04-24)

Após execução inicial de `agents/perpetuum_master.py`:

```
=== Perpetuum Master ===
Running 3 perpetuum(s): ['thesis', 'vault', 'data_coverage']

[thesis]        subjects=33   alerts=0  errors=0  2/33 scored (thesis explícita)
[vault]         subjects=376  alerts=0  errors=0  376/376 scored
[data_coverage] subjects=33   alerts=0  errors=0  33/33 scored

=== Summary ===
Total subjects scored: 442
Total decay alerts: 0
Total errors: 0
```

### Insights imediatos gerados por perpetuums

**vault_health** detectou órfãs + stale:
- `2026-04-23.md` (briefing antigo) score=35 — precisa backlinks
- `tickers.md` (index list) score=35 — thin
- `agents/watchdog.md` score=35 — nota de agent desatualizada
- `Earnings Surprise.md` score=50 — precisa refresh

**data_coverage** detectou holdings com fundamentals incompletos:
- IVVB11, KLBN11, LFTB11 — score **33/100** (4 flags cada)
- Action hint automático: `python fetchers/yf_deep_fundamentals.py IVVB11`

Este é valor **sem Claude reasoning envolvido** — 100% SQL + filesystem deterministic.

## 🚀 Roadmap Phase X

### X.1 — Perpetuum Content Quality (próximo)
- Input: briefings históricos + outcomes (ex: prev alerts vs price moves)
- Output: score signal-to-noise por briefing
- Meta: descobrir quais formatos de briefing produziram insights úteis vs noise

### X.2 — Perpetuum Workflow Efficiency
- Input: exec logs de todos os scripts (latency, token usage, retry count)
- Output: score efficiency por workflow; flag redundâncias
- Meta: sistema auto-refactor de pipelines

### X.3 — Perpetuum Method Discovery (autoresearch)
- Input: lista de métodos nossos (CLAUDE.md critérios, scoring rules)
- Output: para cada método, evidência recente que contradiz/reforça
- Meta: **CLAUDE.md evolui sozinho** com evidence-based updates propostos

### X.4 — Perpetuum Assumption Challenger
- Input: assumptions hardcoded no código (thresholds, weights)
- Output: teste contra dados mais recentes + alternativas da literatura
- Meta: nossos critérios nunca ficam stale

### X.5 — T2 Promotion (1-click actions) ✅ **LIVE 2026-04-24**
- ✅ Skill `.claude/skills/perpetuum-review/SKILL.md` criado
- ✅ Infra: reutiliza `watchlist_actions` table (já existia)
- ✅ `agents/perpetuum/_actions.py` writer com dedup via trigger_id
- ✅ `scripts/perpetuum_action_run.py` runner com WHITELIST de comandos safe
- ✅ `data_coverage` promovido para T2 — produziu 3 actions reais (IVVB11/KLBN11/LFTB11 score 33)
- ✅ Action #6 executada end-to-end (exit 0, status=resolved)
- 📍 Discovery interessante: IVVB11 fetch correu mas fetcher reportou FAIL (yfinance não cobre BDR-ETF) — exactly o tipo de meta-sinal que auto-learning deve captar

### X.6 — T3 Promotion (sandboxed writes)
- Infra: worktree isolation (Claude Code nativo) para actions de data_coverage
- Test: data_coverage faz auto-fetch em worktree; user revê diff

### X.7 — Meta-perpetuum
- `perpetuum_perpetuums` — valida os perpetuums entre si
- Detecta: um perpetuum com 30d sem alert é útil? um com 100% alerts é ruído?

## 📏 Métricas que Phase X adiciona

| Métrica | Hoje | Target |
|---|---|---|
| Perpetuums activos | 3 | 7 |
| Subjects scored / dia | 442 | >1000 |
| Action hints gerados / semana | ~20 | >100 |
| Actions T2 executadas pelo user | 0 | >50/mo |
| CLAUDE.md updates evidence-based | 0 | ≥1/quarter |
| Self-audit catches (vault orfãs resolved) | 0 | 100% de orphans detectadas → resolved em 30d |

## 🔗 Comando central

```bash
# Corre tudo
python agents/perpetuum_master.py

# Só um perpetuum
python agents/perpetuum_master.py --only vault

# Dry-run (sem persist)
python agents/perpetuum_master.py --dry-run
```

## Links

- [[SKL_autoresearch_perpetuum]] — design original da Phase W.5 (agora caso particular)
- [[Roadmap]] — sprints W.x actuais
- [[Demo]] — demo execução Phase W inicial
- [[Metrics]] — KPIs before/after
