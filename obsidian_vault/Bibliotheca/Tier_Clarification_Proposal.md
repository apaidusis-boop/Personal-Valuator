---
type: proposal
phase: FF Bloco 3.2
status: AWAITING_REVIEW
created: 2026-05-08
tags: [phase_ff, perpetuum, governance, proposal]
---

# Tier Clarification — Phase FF Bloco 3.2 (PROPOSAL)

> **Status: aguarda review do user antes de implementação.** O yaml em
> `config/action_safety.yaml` está committed mas é dormant — nenhum perpetuum
> consulta-o ainda.

## O problema

Os 16 perpetuums activos usam um identificador `autonomy_tier` ∈ T1..T5 mas a
semântica é informal:

- `T1 Observer | T2 Proposer | ... T5 Autonomous` (comentário em `_engine.py:93`)
- Quando um T2 acciona, fica claro? E um T3 hipotético?
- Que **gating** existe entre tiers? Resposta hoje: depende do código de cada
  perpetuum + `_actions.py::run_action` + whitelist em `perpetuum_action_run.py`.

External AI critique 2026-05-05 chamou isto de **"Decorator Macro Engine"**:
classificação que sugere autonomia mas não constrange comportamento.

## A proposta

Mapear T1..T5 → semântica explícita de blast radius:

| Tier | Semantic | Pode ler | Escrever reports | Propor actions | Executar | Approval |
|---|---|---|---|---|---|---|
| **T1** | OBSERVE | ✅ | ✅ | ❌ | ❌ | n/a |
| **T2** | PROPOSE | ✅ | ✅ | ✅ (status=open) | ❌ | human |
| **T3** | EXECUTE_WHITELIST | ✅ | ✅ | ✅ | ✅ whitelist | schema match |
| **T4** | EXECUTE_BROAD | ✅ | ✅ | ✅ | ✅ derivado | cmd validation + reversible |
| **T5** | AUTONOMOUS | ✅ | ✅ | ✅ | ✅ | none (must_be_internal) |

A whitelist (T3) está formalizada em `config/action_safety.yaml::execute_whitelist`
com 4 entries iniciais:
- `data_coverage_refetch` (5s, network)
- `bibliotheca_autofix` (30s, idempotent)
- `vault_health_clean_orphan` (10s, reversible)
- `ri_freshness_refetch_quarter` (60s, db write)

## Estado actual (snapshot 2026-05-08)

**T1 Observer (10):** autoresearch, bibliotheca, code_health, daily_delight,
dreaming, library_signals, meta, method_discovery, security_audit, thesis.

**T2 Proposer (5):** content_quality, data_coverage, ri_freshness, token_economy,
vault_health.

**T3+ (0):** nenhum hoje. Promoção candidatos abaixo.

## Plano de implementação (4 sub-sprints)

### 3.2.1 — `BasePerpetuum.action_safety()` (no-op)
Adiciona método que lê `action_safety.yaml` e retorna o dict de gates do tier
actual. **Nenhum perpetuum consulta-o ainda.** Sprint pequeno (≤30min), zero
risco. Entrega: instrumentação + 1 unit test que confirma mapping T1→OBSERVE.

### 3.2.2 — Gate enforcement em `_actions.py::run_action()`
Patch ao `run_action` para consultar `gates[tier_semantics[perpetuum.autonomy_tier]]`
antes de executar. Se gate.can_execute=False → refuse + log. Se gate.requires_approval='human'
→ confirma row com status='open' (já é o comportamento). **Mudança comportamental:
T1+T2 ficam mais defensivamente bloqueados** (refuses se algo tentar executar
directly). Deve ser no-op para o estado actual (nenhum T1/T2 chama run_action
para si).

### 3.2.3 — Promoções candidatas a T3
Após 3.2.1 + 3.2.2 estáveis (≥7 dias):

- **`bibliotheca`** T1 → T3. Justificação: `bibliotheca_autofix` é completamente
  idempotente (re-running = no-op via `--apply` clauses CASE WHEN), zero side
  effects fora da `companies` table, comprovado clean em produção desde
  2026-04-26 (Phase DD). Whitelist entry já existe.
- **`data_coverage`** T2 → T3. Justificação: refetch via `fetch_with_quality` é
  network-only com cache TTL configurado, falhas são absorvidas (Phase FF Bloco
  3.1 provenance writer + cache cascade). Whitelist entry já existe.

**NÃO promover ainda**: thesis (Ollama LLM call, custoso), code_health (acções
implicam edits ao código), vault_health (renames de ficheiros — reversível mas
visível).

### 3.2.4 — T4/T5 deferred
Sem candidatos hoje. Reservar T5 para housekeeping perpetuums futuros
(log rotation, cache eviction) que ainda não existem.

## Por que **não tocar nos 16 perpetuums hoje**

CLAUDE.md regra: actions de blast radius alta requerem confirmação. Tocar 16
perpetuums num único PR concorrente com 9 outras sprints arrisca regression
silenciosa. Esta proposta escreve o yaml + documentação **sem alterar comportamento**;
implementação fica para sprint dedicada após user OK.

## O que pedimos hoje

- ✅ Aprovas a taxonomia OBSERVE/PROPOSE/EXECUTE_WHITELIST/EXECUTE_BROAD/AUTONOMOUS?
- ✅ Aprovas as 4 whitelist entries iniciais?
- ✅ Aprovas o plano de promoção bibliotheca + data_coverage para T3 após
   3.2.1/3.2.2 estáveis ≥7 dias?

Quando responderes "vai" + qualquer ajuste, abro Phase FF Bloco 3.2 sub-sprints
3.2.1-3.2.3 numa sessão dedicada (estimo 2h).
