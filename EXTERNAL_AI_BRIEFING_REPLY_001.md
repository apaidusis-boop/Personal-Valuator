# Reply 001 — Answers to 15 Surgical Questions

> **Context**: External AI agent read `EXTERNAL_AI_BRIEFING.md` and produced 15 surgical questions on agent architecture (perpetuum conflicts, tier drift, decision quality, validation paralysis, etc.). This document is the system owner's answers, structured to enable the external AI to produce a concrete Improvement Roadmap.
> **Date**: 2026-05-05
> **Format per answer**: Letter choice (or hybrid / "neither — here's why") + reasoning + concrete implementation note.

---

## P1 — Conflito entre perpetuums

**Resposta: D + nuance.** A premissa do exemplo está parcialmente errada. data_coverage propor um fetch + bibliotheca marcar o ticker como orphan **não é conflito** — são dois observadores correctamente a reportar factos independentes (tem dados ↔ não tem parent na taxonomia). A informação é aditiva, não destrutiva.

Conflito real só existe ao **executar**. Como hoje T3+ é vazio (nenhum perpetuum executa autonomamente decisões de capital), o problema é mais teórico que operacional. Onde já existe execução (vault auto-writes), o padrão é: escalation para `decision_journal` quando dois perpetuums emitem `action_hint` divergentes sobre o mesmo subject_id em <24h.

**Implementação concreta**: adicionar tabela `perpetuum_conflicts` com (subject_id, perpetuum_a, hint_a, perpetuum_b, hint_b, detected_at, resolution). Adicionar detector de **thrashing**: se A propõe X e B desfaz X >2 vezes num mesmo subject, T1 alert. Não construir Conflict Resolution Layer formal — overkill para o problema actual.

---

## P2 — T1→T5 Drift

**Resposta: D + E híbrido. Colapsar para 3 tiers + risco por acção.**

T1-T5 era over-engineering. Em prática só uso T1/T2/T3. Perpetuums **não devem ter tier** — *acções* têm tier. Um perpetuum pode emitir acções de risco variado.

Novo modelo:
- **Tier OBSERVE** — write-only para `signals` table. Zero side effects.
- **Tier PROPOSE** — write para `actions` (status=open). Requer human approval via `ii perpetuum-review`.
- **Tier EXECUTE** — só executa whitelist de acções marked `auto_safe=true` em `config/action_safety.yaml`. Whitelist começa minúscula (regenerate auto-draft wiki, refresh cache, rotate logs). Nunca expande sem human commit.

**Implementação concreta**: 1 commit migra os 12 perpetuums para o novo modelo (rename `tier=T1` → `tier=OBSERVE`). Criar `config/action_safety.yaml` com whitelist explícita. Audit pass: cada `action_hint` actual recebe `risk_class ∈ {fetch, vault_write, db_write, file_delete, network_paid}`.

---

## P3 — Perpetuum Granularidade

**Resposta: E. Manter 12 nomes, factorizar 2-3 base classes.**

Os 12 nomes mapeiam ao mental model do user — "thesis perpetuum", "bibliotheca perpetuum" são vocabulário operacional. Colapsar mata legibilidade.

Mas há duplicação: code_health, content_quality, ri_freshness, data_coverage, bibliotheca todos fazem "scan for staleness/missing → propose refresh". 5 implementações da mesma coisa.

**Implementação concreta**:
- `perpetuum/_base.py::Scanner` — para os 5 acima. Hook points: `find_subjects()`, `assess(subject)`, `propose_action(subject, finding)`.
- `perpetuum/_base.py::Synthesizer` — para thesis, autoresearch, methods (LLM-driven enrichment).
- `perpetuum/_base.py::Auditor` — para meta, code_health (read-only over codebase).

Goal: cada perpetuum fica em <80 linhas, lógica específica isolada do scaffolding.

---

## P4 — Evidence Ledger Automação

**Resposta: C + E. Provenance tracking automático + versioned.**

Hoje é manual no Council STORYT, semi-automático nos outros. Devia ser automático no fetcher layer.

**Implementação concreta**:
- Nova tabela `provenance` em ambas DBs: `(metric_id, ticker, metric_name, value, source, source_url, fetcher, fetched_at, cache_hit, confidence)`.
- Cada fetcher (yf, sec_edgar, cvm, bcb, fred, massive) escreve provenance ao escrever em `fundamentals`/`prices`/`events`.
- Dossier renderer query a `provenance` quando monta o appendix — zero trabalho manual.
- Snapshot do provenance vai em `data/dossier_snapshots/<TK>/<DATE>.json` junto com o dossier (versioned).

Custo: 1 migration + ~6 fetcher patches + helper `provenance.record(metric, value, source, url)`. ~1 dia de trabalho.

---

## P5 — Decision Quality Measurement

**Resposta: C + D + E (combinados). Esta é a maior dívida do sistema.**

A + B isolados são pobres. Brier exige outputs probabilísticos que não emitimos. Win-rate é grosso demais. O modelo certo:

- **D (outcome tracking)**: cada verdict (BUY/HOLD/AVOID) regista snapshot em `verdict_history` (já existe `ii vh`). Adicionar follow-up automático em 30/90/180/365 dias com return absoluto + return relativo a SPY/IBOV + return relativo a sector ETF.
- **C (calibration curve)**: x-axis = conviction score (0-100), y-axis = 1y forward IRR. Build trimestralmente. Idealmente monotónica. Se não-monotónica → score está a medir ruído.
- **E (post-mortem cadence)**: trimestral. "Das BUY 90 dias atrás, mediana de return? Top winner? Worst loser? Bias detection (concentração sectorial, tilt market-cap)?"

**Implementação concreta**: novo módulo `analytics/decision_quality.py`. Reusa `verdict_history` que já existe. Cron mensal: `ii decision-quality --report`. Output em `obsidian_vault/Bibliotheca/Decision_Quality_<DATE>.md`. Anti-overfit: **proibido** retreinar engines com base em hits — relatórios são lidos pelo humano, não realimentam scoring directamente.

---

## P6 — Synthetic IC Validation

**Resposta: D primeiro, A depois se D inconclusivo.**

D (ablation 3 vs 5) é barato e decisivo. Se 3 personas produzem o mesmo verdict que 5 em >85% dos casos, cortamos 2 personas (40% menos compute, zero quality loss). Se a divergência é alta, há diversidade real e mantemos 5.

A (embedding distance) só faz sentido se D mostra valor mas é unclear quais 3 manter. Aí calculamos pairwise embedding distance entre as 5 outputs ao longo de 50 backtests, mantemos as 3 mais distantes em média.

**Implementação concreta**:
- Backtest: rodar Synthetic IC sobre 50 tickers (33 holdings + 17 watchlist random). Capturar verdict + rationale por persona.
- Métricas: (a) verdict agreement rate por par de personas, (b) cosine similarity entre rationales (nomic embeddings, já temos), (c) ablation accuracy 3 vs 5.
- Output: `obsidian_vault/Bibliotheca/Synthetic_IC_Validation_<DATE>.md`. Decision: keep 5 / cut to 3 / replace 1.

Custo: ~250 LLM calls Qwen 14B local. ~30 min em RTX 5090. Zero tokens pagos.

---

## P7 — Variant Perception Self-Disagreement

**Resposta: A. Mostrar spread.**

Honestidade > falso consenso. Quando os 5 engines internos discordam, **isso é a informação** — não esconder atrás de mediana ou voto majoritário.

Output certo do Variant Perception:
```
Internal engines: graham=BUY (0.72) | buffett=HOLD (0.55) | drip=BUY (0.81) | macro=AVOID (0.30) | hedge=N/A
Internal spread: 0.51 (high)
Analyst consensus: HOLD (n=8 reports)
Variant signal: ambiguous-internally; consensus is HOLD; macro engine outlier (sector under regime headwind)
```

Spread alto + consenso firmado = **action: investigar porquê o macro engine é outlier antes de decidir**. Spread baixo + divergência vs consenso = **action: variant perception genuíno, dossier de defesa contrarian**.

**Implementação concreta**: refactor `agents/variant_perception.py::_internal_view()` para retornar `(median, spread, per_engine_dict)` em vez de só `median`. Renderer mostra os 3.

---

## P8 — Bibliotheca Validation Paralysis

**Resposta: D híbrido. Métodos academicamente backtested → backtest. Métodos novos → 30+ paper signals.**

A regra "30+ closed at 60% win rate" foi cautelar e está a produzir paralysis. Mas relaxar para "10+ closed at 50%" é injustificável — abre a porta a noise como sinal.

Modelo de duas-vias:
- **Tier-A methods** (Magic Formula, Net-Net, Buffett Quality, Piotroski high, Graham Number) — têm 10-50 anos de literatura académica + backtests publicados. Não preciso de re-validar conceito; preciso de validar **se funciona no meu universo**. Backtest walk-forward no universo BR/US 2010-2024. Aprovação se OOS Sharpe > 0.5 e drawdown max < 30%.
- **Tier-B methods** (extracções idiossincráticas dos books, regras compostas raras) — manter 30+ closed paper signals rule. Estes precisam de evidência empírica nossa.

Capital alocação: Tier-A pode receber capital pequeno (≤2% portfolio cada) sem paper validation. Tier-B continua paper-only até 30+ closed.

**Implementação concreta**: tag `tier ∈ {A, B}` na tabela `methods`. Novo módulo `library/backtest_method.py` que pega method definition + universo + datas + roda walk-forward. Output: `obsidian_vault/Bibliotheca/Methods/<method_slug>_Backtest.md`.

---

## P9 — yfinance SPOF

**Resposta: E (todos os 3 layers).**

- **Fallback**: já existe Massive.com para US. Re-adicionar brapi.dev como fallback BR (foi removido em c807140 nunca-wired; agora wired explicitamente como SPOF mitigation, não primary).
- **Spot-check**: cron mensal compara 5 random tickers BR contra CVM ITR + 5 random US contra SEC EDGAR XBRL. Métrica: % desvio em market_cap, eps, revenue. Alert Telegram se >5% em qualquer.
- **Cache agressivo**: TTL por tipo. Prices: 1 dia. Fundamentals: 7 dias. Dividendos histórico: 30 dias. Já temos `data/api_cache.db`; só precisa configurar TTLs por kind em `config/cache_ttl.yaml`.

**Implementação concreta**: 1 commit por layer (fallback re-wire + spot_check.py + ttl yaml). Spot-check é o único trabalho real (~1 dia). Os outros são re-arrange.

---

## P10 — CVM Bank Parser Fragility

**Resposta: D + B híbrido. Code-first com fallback ds_conta + per-bank mapping table.**

ds_conta-only é frágil porque CVM permite cada banco rebrand. cd_conta-only é frágil porque cada banco usa códigos diferentes. Real fix:

`config/bank_account_map.yaml`:
```yaml
BBDC4:
  net_interest_income: ['7.01.01.01', '7.01.01']
  loan_loss_provision: ['7.01.02']
  fees: ['7.01.04']
ITUB4:
  net_interest_income: ['7.01.01']
  ...
```

Parser: tenta cada code na ordem; se nenhum encontra → fuzzy match por ds_conta como último recurso. Log entry quando ds_conta foi usado (sinal de schema change).

**Implementação concreta**: ~1 dia. Bootstrap o YAML lendo 1 ITR de cada banco BR (BBDC4, ITUB4, BBAS3, SANB11, ABCB4) manualmente. Depois cron `library/ri/cvm_parser_bank.py --reconcile` testa monthly se os codes ainda funcionam.

---

## P11 — Thin History N/A

**Resposta: A com tweak. Manter N/A para <2 anos. ≥2 anos: emitir partial score com `confidence=low` flag.**

N/A é semanticamente correcto quando a métrica é matematicamente indefinida (Beneish exige 2 anos de comparáveis). Mas excluir do universo (E) é overcorreção — IPOs recentes podem ser tese válida com outros sinais.

Modelo:
- <2 anos history → score = NULL, screen excluído (Beneish/Piotroski/Altman não vetam nem aprovam)
- ≥2 anos mas <3 → score com `confidence=low`. Veto não dispara em low-confidence. Aparece no dossier com asterisco.
- ≥3 anos → score full confidence.

**Implementação concreta**: adicionar coluna `confidence ∈ {full, low, null}` em `scores` table. Tweak `scoring/beneish.py`, `scoring/piotroski.py`, `scoring/altman.py` para emitir confidence. Dossier renderer respeita confidence (asterisco + tooltip).

---

## P12 — Moat Engine Weighting

**Resposta: E. Validar empiricamente, mas com guard contra overfit.**

Equal weights (25% × 4) é defensável mas arbitrário. Não tunar em busca aberta — overfit garantido.

Plano:
- Pre-register 4 weighting schemes:
  1. Equal (status quo): 25/25/25/25
  2. Buffett-aligned: pricing 35 / capital 30 / reinvestment 20 / scale 15
  3. Munger-aligned: capital 35 / pricing 25 / reinvestment 25 / scale 15
  4. Greenblatt-aligned: capital 50 / pricing 30 / reinvestment 10 / scale 10
- Backtest cada scheme em US universe 2010-2020 (training) com OOS 2021-2024.
- Métrica: correlação entre Moat Score e 5y forward total return.
- Pick: melhor OOS, **não** melhor training. Se OOS empate <0.05 → manter Equal (Occam).

**Implementação concreta**: `scripts/moat_calibration.py`. Output: `obsidian_vault/Bibliotheca/Moat_Calibration_<DATE>.md`. Pre-registar os 4 schemes em commit ANTES de correr o backtest (evita p-hacking).

---

## P13 — Macro Regime Discrete vs Continuous

**Resposta: D. Probabilístico (P(expansion), P(late_cycle), P(recession), P(recovery), sum=1).**

Discreto esconde uncertainty exactamente nos momentos críticos (transições). Probabilístico permite blending suave do macro overlay.

Use case real: hoje em "late_cycle", hedge size = 5%. Amanhã threshold cruza para "recession", hedge salta a 10%. Discreto cria step function que produz trades artificiais. Probabilístico → P(late_cycle)=0.4, P(recession)=0.6 → hedge size = 0.4×5% + 0.6×10% = 8%. Suave.

**Implementação concreta**: `analytics/regime.py::classify()` actualmente retorna string. Alterar para retornar dict com 4 probabilidades. Manter helper `dominant_regime()` que retorna a label máxima para back-compat com UI. Hedge engine + macro engine consomem as 4 probs.

Modelo subjacente: logistic regression multi-class sobre features (yield curve slope, real fed funds rate, ISM PMI, unemployment delta, credit spread). Train em historical regimes labeled manualmente (NBER recessions + late-cycle definitions). ~200 linhas Python.

---

## P14 — Midnight Rollback

**Resposta: D + B. Sanity checks pre-commit + auto-revert em failure.**

Stage rollout (E) é overkill para single-user. Dry-run first (C) mata o midnight (não há human na hora de aprovar).

Modelo:
- `scripts/midnight_pre_commit_check.py` corre antes de cada `git commit` durante midnight session. Checks:
  - Nenhuma row deleted em `companies`, `prices`, `fundamentals`, `quarterly_history`, `portfolio_positions`.
  - Nenhum dossier em `obsidian_vault/dossiers/` perdeu >50% byte size.
  - Nenhum ticker hard-coded em `.py` files (CH001 anti-pattern).
  - Token spend (Tavily, Claude API) dentro do daily budget.
  - Provenance ledger não regrediu (count >= prior).
- Se algum check falha → midnight session aborta, `git stash` o que estava staged, push Telegram alert.
- Se midnight termina mas user de manhã detecta problema → `ii midnight rollback <DATE>` reverte todos os commits da session.

**Implementação concreta**: ~1 dia. Reusa `scripts/rotate_logs.py` pattern.

---

## P15 — 5 Surfaces

**Resposta honesta sobre uso real**:
- CLI `ii`: ~50% (arrancar, deepdive ad-hoc, queries SQL)
- Mission Control: ~25% (visual overview matinal, action buttons)
- Obsidian vault: ~15% (leitura de wikis, curate de teses, escrever notes humano)
- Telegram: ~8% (push diário Captain's Log, chat livre quando fora)
- Streamlit: ~2% (legacy, deprecate)

**Source of truth**: L1 SQLite (raw) + L3 Obsidian humano (curated). Tudo o resto são views.

**Decisão**: deprecar Streamlit. As 4 outras surfaces ganham o lugar:
- CLI = velocidade para acção
- MC = visual + write actions do browser (deepdive trigger, etc.)
- Obsidian = leitura humana + curadoria
- Telegram = mobile push + chat livre

**Implementação concreta**: 1 commit. Mover features únicas do Streamlit (Captain's Log page, paper_trade dashboard) para Mission Control panes existentes ou criar pane `/legacy`. Apagar `streamlit_app.py` + dependências em `requirements.txt`.

---

## Resumo do que o roadmap externo deve produzir

Top 5 prioridades em ordem (alinhadas com o user):
1. **Decision Quality Engine (P5)** — maior gap. Calibration curve + outcome tracking + post-mortem trimestral. ~3 dias.
2. **Synthetic IC Validation (P6)** — barato, decisivo. Ablation 3 vs 5 personas. ~1 dia.
3. **Provenance Tracking (P4)** — desbloquia evidence ledger automático em todos os dossiers. ~1 dia.
4. **Tier Clarification + Action Safety (P2)** — colapsar T1-T5 → OBSERVE/PROPOSE/EXECUTE + risk_class por acção. ~1 dia.
5. **yfinance SPOF Mitigation (P9)** — fallback re-wire + spot-check cron + cache TTL yaml. ~1 dia.

Total ~7-8 dias de trabalho focado. Tudo offline-capable, zero novos paid services.

Próximos do agente externo: Improvement Roadmap concreto + code change snippets para os 5 acima. Não pedir ainda os "New Agents" — primeiro consolidar o que existe.

---

*End of reply. Send back to external AI for Improvement Roadmap.*
