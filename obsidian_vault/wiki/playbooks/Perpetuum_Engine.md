---
type: playbook
name: Perpetuum Engine — autonomous self-improvement loops
tags: [playbook, perpetuum, autonomy, agents]
related: ["[[Agents_layer]]", "[[Token_discipline]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🔁 Perpetuum Engine — observação repetida → score → action

> Pattern arquitectural do projecto para **auto-melhoria contínua**. Cada perpetuum varre um domínio (tickers, vault, dados, código, vault, library, RI, bibliografia, tokens, autoresearch, meta), pontua 0-100 cada *subject* e — conforme o seu **autonomy tier** — apenas observa, ou propõe acções com `action_hint` executável. 12 perpetuums activos hoje (2026-04-28).

## Princípio

**Sistema aprende sobre si próprio todos os dias.** Cada loop é determinístico e idempotente: re-correr o mesmo dia sobrescreve a mesma row (`PRIMARY KEY (perpetuum_name, subject_id, run_date)`). Custo marginal: SQL + filesystem + opcional Ollama local. Zero tokens Claude no caminho crítico (cumpre [[Token_discipline]]).

> _Qualquer processo que melhore por observação repetida + scoring contra baseline é candidato a perpetuum._

## O ciclo (5 fases)

```
subjects() → score() → drift detect → persist → action_hint (T2+)
   ↓           ↓            ↓             ↓            ↓
enumerar   0-100/sub   delta vs      perpetuum_   watchlist_actions
 (SQL +    + flags     last run       health      (kind=perpetuum:<n>,
  files)                ≥ 10 = alert  + run_log    status=open)
```

| # | Fase | Onde | Output |
|---|---|---|---|
| 1 | Enumerar subjects | `subjects()` em cada perpetuum | `list[PerpetuumSubject]` |
| 2 | Score | `score(subject)` determinístico | `PerpetuumResult(score, flags, action_hint)` |
| 3 | Drift detect | `_engine.run()` | `prev - now ≥ drop_alert_threshold` |
| 4 | Persist | `_engine._persist()` | row em `perpetuum_health` (BR DB, shared) |
| 5 | Action propose | `_actions.write_action_from_result()` | row em `watchlist_actions` (T2+ only) |

Schema central em `data/br_investments.db` (mesmo p/ subjects US — storage centralizado, `_split_subject_id` divide `br:TICKER` vs `us:TICKER`):

- `perpetuum_health` — `(perpetuum_name, subject_id, run_date)` PK, score, flag_count, tier, details_json, action_hint
- `perpetuum_run_log` — exec metadata por run (duration, alerts, errors, summary)
- `watchlist_actions` — partilhada com trigger system; perpetuum rows têm `kind = "perpetuum:<name>"`, `trigger_id = "perpetuum:<name>:<subject_id>:<run_date>"` (dedup natural)

## 📶 Autonomy Tiers (T1-T5)

| Tier | Nome | Agent faz... | User faz... | Promoção requer |
|---|---|---|---|---|
| **T1** | Observer | detecta + regista em `perpetuum_health` | revê alertas Telegram / Captain's Log | baseline |
| **T2** | Proposer | tudo do T1 + escreve `action_hint` em `watchlist_actions` (`status=open`) | one-click approve via `perpetuum_action_run.py` ou skill `perpetuum-review` | 30d estável + 0 falsos positivos críticos |
| **T3** | Sandboxed | actua em **dry-run worktree** | revê diff antes de merge | T2 ≥ 30d + backtest validado |
| **T4** | Guarded | actua em produção com **hard limits** (ex: cap diário) | auditoria semanal | T3 com boundaries provadas |
| **T5** | Autonomous | actua livremente | sample audits | só após 6 meses sem falso positivo crítico |

**Promoção** é uma edição na linha `autonomy_tier = "Tx"` do perpetuum + commit explícito (não auto). O `_engine.run()` lê o atributo e escreve actions só quando tier in `{T2, T3, T4, T5}`.

## Tabela dos perpetuums activos (2026-04-28)

| # | Nome | Tier | Observa | Sinais / códigos | Action whitelisted? |
|---|---|---|---|---|---|
| 1 | `thesis` | T1 | thesis explícita por ticker (holdings + watchlist universe, ~184 subjects) | 5y streak, ROE, NetDebt/EBITDA, regime fit | ❌ MANUAL_REVIEW |
| 2 | `vault` | T2 | saúde de notas .md (orphan, stale, broken links, no_thesis) | orphan -40, stale gradient, short -25, no_thesis -20, broken -5 each | ❌ MANUAL_REVIEW |
| 3 | `data_coverage` | T2 | completeness de dados por holding | price_fresh, fundamentals_fresh, complete, dy_history, streak, sector | ✅ `yf_deep_fundamentals` / `refresh_ticker` |
| 4 | `content_quality` | T2 | signal-to-noise de briefings + ticker notes | specificity, actionability, uniqueness vs prev, boilerplate, generic, age | ❌ MANUAL_REVIEW |
| 5 | `method_discovery` | T1 | métodos do CLAUDE.md (Graham, Buffett, Piotroski) | last_validated_days, evidence_citations, backtest_age, regime_covered | ❌ stub queries |
| 6 | `token_economy` | T2 | static analysis de scripts/agents (AST + regex) p/ Claude vs Ollama | claude_direct, no_cache, long_prompt, hardcoded_model, dup_prompt | ❌ MANUAL_REVIEW |
| 7 | `library_signals` | T1 (**FROZEN**) | (method × ticker) pairs c/ fundamentals; gera paper signals | % rules passed | ❌ enabled=False até paper_trade_close ter ≥30 closed signals |
| 8 | `ri_freshness` | T2 | releases CVM (ITR/DFP/IPE) por stock do catalog | latest quarter overdue, IPE stale 30d/7d | ✅ `library.ri.cvm_filings` (ingest/download) |
| 9 | `code_health` | T1 | anti-patterns no codebase (170+ .py) | CH001 yaml.safe_load directo, CH002/3 catalog miss watchlist, CH004 dead CATALOG, CH005 hardcoded Ollama URL, CH006 silent except, CH007 banner ad-hoc | ❌ MANUAL_REVIEW (refactor proposal) |
| 10 | `autoresearch` | T1 | top-conviction holdings (≥70) vs Tavily news 14d | material_news_uncovered (penalty per item not in vault) | ❌ alert-only (cooldown 6d) |
| 11 | `bibliotheca` | T1 | catalog itself — `companies` rows, holdings ou não | BIB001 sector_null, BIB002 sector_noncanonical, BIB003 name_generic (== ticker), BIB004 orphan (DB-only) | ✅ `bibliotheca_autofix.py --apply` (manual run) |
| 12 | `meta` | T1 | os outros perpetuums entre si | signal_to_noise, score_distribution_health, actionability, alert_density, runtime_cost, uniqueness | ❌ retire/retune proposals |

> Detalhe: `meta` corre **sempre por último** no `_registry._build()` — precisa que os outros já tenham escrito `perpetuum_health` rows hoje para se auto-auditar.

> Tier definitivo verificável em runtime via `getattr(perp, "autonomy_tier")` ou direct grep `autonomy_tier = "T?"` em `agents/perpetuum/<name>.py`.

## Action lifecycle

```
   T2+ score < 70           user decides
        │                       │
        ▼                       ▼
  watchlist_actions ──► open ──► resolved | ignored
   (kind=perpetuum:*,             ↑              ↑
    trigger_id dedup)              │              │
                       perpetuum_action_run.py    ├─ exit 0 (whitelisted, ran)
                       (or perpetuum-review skill)│  → status=resolved
                                                  └─ exit ≠ 0 OR not whitelisted
                                                    → status=ignored (manual fix)
```

Estados:

- `open` — perpetuum propôs, user ainda não decidiu.
- `resolved` — comando whitelisted correu com `exit 0`. `notes` field tem JSON com `exit_code, stdout_tail, stderr_tail, ran_at`.
- `ignored` — comando não-whitelisted **ou** falhou. User pode também marcar manual via `action_cli.py ignore <id> --note '...'`.
- `defer` — sem state machine; basta deixar `open` que volta a aparecer no próximo `list-open`.

Idempotência via `trigger_id = "perpetuum:<name>:<subject_id>:<run_date>"` — re-corridas do mesmo perpetuum no mesmo dia **não** criam duplicados (`_actions.py::write_action_from_result` faz `SELECT … WHERE trigger_id = ?` antes de inserir). Dia novo + score ainda baixo = nova row.

## Whitelist mechanism (`perpetuum_action_run.py`)

Apenas comandos que casam um `re.compile` na lista `ACTION_WHITELIST` correm automaticamente. Tudo o resto cai em "command NOT in whitelist" e o user vê instruções para correr à mão.

Whitelist actual:

```python
^python\s+fetchers/yf_deep_fundamentals\.py\s+[A-Z0-9.\-]+$
^python\s+scripts/refresh_ticker\.py\s+[A-Z0-9.\-]+$
^python\s+fetchers/fred_fetcher\.py(\s+--series\s+[A-Z0-9_]+)?$
^python\s+-m\s+library\.ri\.cvm_filings\s+(ingest|download)\s+(dfp|itr|ipe|fre|fca)\s+--year\s+\d{4}…$
^python\s+-m\s+library\.ri\.cvm_parser\s+build$
^python\s+-m\s+library\.ri\.quarterly_single\s+build$
^python\s+-m\s+library\.ri\.compare_releases\s+(--all-catalog|[A-Z0-9.\-]+)$
^python\s+-m\s+library\.ri\.fii_filings\s+(download|ingest)\s+--year\s+\d{4}…$
```

Regra: **estender com cuidado**. Tudo que escreve em `data/`, faz force-push, ou consome quotas externas pagas = não entra. Comandos read-mostly + idempotentes + escritos só em DBs locais = candidatos.

Failure modes:

- `cmd` não match whitelist → exit 5, status `ignored`, user vê o cmd e corre manual.
- `cmd` corre, exit ≠ 0 → status `ignored`, stderr_tail no `notes`.
- `cmd` corre, exit 0 → status `resolved`, stdout_tail no `notes`.
- Action `id` não existe ou `kind` não começa com `perpetuum:` → exit 2.
- Action já `resolved`/`ignored` → exit 3 (não re-corre).

## Daily cron

`scripts/daily_run.bat` (Windows Task Scheduler — tarefa `investment-intelligence-daily`, 23:30 local):

```bat
[PERPETUUM] perpetuum_master.py  (12 perpetuums incl. autoresearch K)
%PY% agents\perpetuum_master.py >> %LOG% 2>&1
```

Corre depois dos fetchers + monitors + briefings + triggers. Output integral vai para `logs/daily_run_YYYY-MM-DD.log`. Captain's Log Telegram (`captains_log_telegram.py` no mesmo .bat) pesca counters do `perpetuum_run_log` e empacota em push diário.

## Decision journal output

T2+ actions geram trail auditável (3 layers):

1. **`perpetuum_health`** — score histórico do subject (drift visível).
2. **`watchlist_actions`** — proposta + decisão + execução output (no `notes` JSON).
3. **`perpetuum_run_log`** — meta-resumo por dia (subjects, alerts, errors, duration).

Para retomada de contexto após pausa: `agents/decision_journal_intel.py` (Phase AA) agrega P1-P5 patterns por perpetuum. Captain's Log page (`scripts/_captains_log.py`) mostra perpetuum alerts em story_cards.

## Comandos

| Caso | Comando |
|---|---|
| Correr todos os perpetuums | `python agents/perpetuum_master.py` |
| Correr só um | `python agents/perpetuum_master.py --only data_coverage` |
| Dry-run (sem persist) | `python agents/perpetuum_master.py --dry-run` |
| Verbose (errors detail) | `python agents/perpetuum_master.py --verbose` |
| Listar open actions T2+ | `python scripts/perpetuum_action_run.py list-open` |
| Listar pending (alias) | `python scripts/perpetuum_action_run.py list-pending` |
| Aprovar 1 action (whitelisted) | `python scripts/perpetuum_action_run.py 47` |
| Aprovar restrita por mercado | `python scripts/perpetuum_action_run.py 47 --market br` |
| Ignorar / annotar | `python scripts/action_cli.py ignore 47 --note 'reason'` |
| **Skill review interactiva** | invocar skill `perpetuum-review` (triggers: "revisar ações", "perpetuum review", "approve X", "ignore Y") |
| Ver últimas runs | `sqlite3 data/br_investments.db "SELECT perpetuum_name, run_date, alerts_count, duration_sec FROM perpetuum_run_log ORDER BY run_date DESC, perpetuum_name LIMIT 30"` |
| Ver worst subjects de hoje | `sqlite3 data/br_investments.db "SELECT subject_id, score, flag_count FROM perpetuum_health WHERE perpetuum_name='data_coverage' AND run_date=(SELECT MAX(run_date) FROM perpetuum_health) AND score<70 ORDER BY score"` |

## Adicionar novo perpetuum (how-to)

1. **Criar ficheiro** `agents/perpetuum/<name>.py`:
   ```python
   from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

   class MyPerpetuum(BasePerpetuum):
       name = "my_perp"
       description = "What I observe"
       autonomy_tier = "T1"           # NUNCA começar > T1
       drop_alert_threshold = 10
       action_score_threshold = 70    # só relevante se subir para T2+

       def subjects(self) -> list[PerpetuumSubject]: ...
       def score(self, s) -> PerpetuumResult: ...
   ```
2. **Registar** em `agents/perpetuum/_registry.py` na lista `instances` (antes de `MetaPerpetuum`, que tem de ficar last).
3. **Smoke test**: `python agents/perpetuum_master.py --only my_perp --dry-run --verbose`.
4. **Garantir idempotência**: re-correr mesmo dia → mesmas rows actualizadas, não duplicadas.
5. **Wire ao cron**: já está — `daily_run.bat` corre `perpetuum_master` sem flags.
6. **Tier graduation**:
   - T1 → T2 quando: 30d sem alerts ruidosos, action_hint sempre executável (whitelist OR claro MANUAL_REVIEW), score distribution não-trivial (não é all-100 nem all-0).
   - T2 → T3 quando: ≥30d em T2 com >50% das actions resolved (não ignored), backtest do action effect é mensurável, infra de worktree pronta.
   - **User decide a promoção**, não auto-promote. Edit do `autonomy_tier` é commit explícito.

## Limitações conhecidas

- **`library_signals` FROZEN desde 2026-04-26** (`enabled = False`): 2511/2912 subjects below threshold = pure noise enquanto `paper_trade_close.py` não tinha closed signals trackable. Re-enable depois de ≥30 closed signals com `win_rate` mensurável.
- **Storage central na BR DB** (`data/br_investments.db`) — subjects US (`us:TICKER`) também aterram lá. Convenção, não bug; simplifica queries de meta-audit.
- **CRLF poison nos tickers** (Windows ingest) — `thesis.py::subjects()` faz `(ticker or "").strip()`. Outras `subjects()` similares devem replicar.
- **Whitelist é narrow por design** — ampliar custa rever cada padrão; preferível MANUAL_REVIEW first, whitelist depois de 5-10 successful manual runs.
- **`meta` ainda não promove/retira** automaticamente — só score-flag. T1 puro.
- **Drop alert threshold default = 10**, individual perpetuums podem subir (ex: `data_coverage = 20`, `library_signals = 25`) para reduzir noise.

## Estado actual (2026-04-28)

- **12 perpetuums registados** (1 frozen `library_signals`).
- **5 em T2** — `vault`, `data_coverage`, `content_quality`, `token_economy`, `ri_freshness`.
- **6 em T1** — `thesis`, `method_discovery`, `code_health`, `autoresearch`, `bibliotheca`, `meta`.
- Cron daily 23:30 wired em `scripts/daily_run.bat`.
- Captain's Log + Telegram brief consomem `perpetuum_run_log`.

## Workflow recomendado

1. **Antes** de criar script novo para detectar drift / staleness / coverage gaps → ver se cabe num perpetuum existente ou justifica um novo. Pattern já tem schema, scheduling, action lifecycle, dedup.
2. Para rever proposals: invocar skill `perpetuum-review` (não correr ad-hoc — skill enforça whitelist visual + delta after).
3. Para iterar prompt/scoring sem poluir DB: `--dry-run`.
4. Para promover tier: editar `autonomy_tier` no ficheiro, commit explícito com critério verificável de done na mensagem.

## Ver também

- [[Token_discipline]] — porque scoring é todo SQL/regex/AST (zero Claude no path crítico)
- [[Agents_layer]] — perpetuums são agents tier 1 do framework `agents/`
- [[Analyst_Tracking]] — `predictions_evaluate.py` é counterpart (closes analyst predictions; perpetuums fecham coverage gaps)
- [[Buy_checklist]] — `data_coverage` perpetuum garante que checklist tem dados
- [[Sell_triggers]] — trigger engine partilha tabela `watchlist_actions` com perpetuums (kind diferente)
