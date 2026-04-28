---
type: midnight_work
date: 2026-04-28
session_focus: L2 vault hardening — playbooks-as-canonical-docs (token reduction)
deliverable: 9 vault playbooks + 5 CLAUDE.md drift fixes + 18 catalog adds + 1 code refactor
---

# 🌙 Midnight Work — 2026-04-28

> **Why**: User flagou que cada explicação de pipeline (YouTube, Library, Perpetuum, etc.) custava re-leitura de 5-15 módulos Python — token-bomb recorrente. Princípio: **L2 vault = escritório consultável** (Phase U.0 framework). Esta sessão materializa essa princípio para os 9 sistemas mais re-perguntáveis.

---

## 📊 Métricas before/after

| Métrica | Before | After | Δ |
|---|---|---:|---|
| `wiki/playbooks/*.md` count | 8 | **17** | +9 (+112%) |
| Memory entries com `verify against code` warning | 8 | 0 | -8 (apontam para vault) |
| CLAUDE.md script catalog drift count | 5 conhecidas | 0 | -5 |
| Mega Audit MA-UN-* (catalog gaps) | 20 | 0 | -20 |
| Vault L2 docs `❓ verify` markers | 11 | 4 (todos genuinamente abertos) | -7 |
| Code health CH005 (direct `requests.post`) violations | 5 reportadas (3 false-positive) | 4 reportadas (1 real fixed) | -1 real |

---

## 🎯 Token economics

**Cost típico de re-explicação antes**:
- "Explica o pipeline X" → leitura de ~5-15 módulos + DB inspection + memory cross-check
- Por sistema: ~10-20k tokens / re-pergunta

**Cost depois**:
- "Explica o pipeline X" → 1 Read da `wiki/playbooks/X.md` (~150-250 lines)
- Por sistema: ~1-2k tokens / re-pergunta

**ROI**: ~10× redução por re-pergunta. Investimento desta sessão (~600k tokens em agents + fixes) paga-se ao 4º-5º re-uso por playbook.

---

## ✅ O que foi feito

### Fase 1 — 9 novos playbooks (`wiki/playbooks/`)

Cada ficheiro segue o template `Youtube_Pipeline.md` (frontmatter + Princípio + Pipeline + Comandos + Schemas + Limitações + Integrações + Ver também):

| Playbook | Linhas | Cobertura |
|---|---:|---|
| [[Youtube_Pipeline]] | ~210 | yt-dlp + Whisper + Ollama Qwen → `video_insights/themes`; cache-first |
| [[Library_Pipeline]] | ~210 | book PDF → chunks → methods → matcher → `paper_trade_signals` |
| [[Perpetuum_Engine]] | ~280 | 12 perpetuums activos + T1-T5 tiers + action_run mecânica |
| [[Tavily_Integration]] | ~195 | L1 (autoresearch+wires, cron) + L2 (8 slash skills) |
| [[RI_Knowledge_Base]] | ~210 | CVM filings → `quarterly_history` + bank parser ds_conta-based |
| [[Critical_Thinking_Stack]] | ~280 | Synthetic IC + Variant + Decision Journal + Earnings Prep + Stress Test |
| [[Bibliotheca_v2]] | ~240 | Clippings RAG + Glossary tutor injector + Daily Digest + 12 Knowledge Cards |
| [[Verdict_Engine]] | ~200 | BUY/HOLD/SELL/AVOID aggregator + history + backtest |
| [[Daily_Orchestration]] | ~240 | sequência cron 23:30 (`daily_run.bat` 19 steps) |

**Total**: ~2,065 linhas de docs novas. Geradas em paralelo via 8 sub-agents (cada um isolado, ~70-100k tokens/agente).

### Fase 2 — Drift fixes em CLAUDE.md (script catalog)

Drifts entre catalog e argparse real:

| Script | Catalog dizia | Realidade |
|---|---|---|
| `variant_perception` | `[--write]` | flag não existe (writes by default); flags reais: `--market`, `--all-holdings`, `--no-weighting` |
| `portfolio_stress` | `--shock pe_compress\|recession` | positional `kind` ∈ {concentration, factor, drawdown, all} |
| `earnings_prep` | `--days 60` | `--upcoming N` |
| `compare_releases` | `--quarters 4` | não há flag (itera todos os quarters automaticamente) |
| `conviction_score` | `--top-n 20` | `--top N` (sem hífen) |

**Material finding**: catalog drift é sintoma sistémico — a `code_health` perpetuum não cobre catalog-vs-argparse alignment. **Recomendação**: adicionar **CH008** ao perpetuum (parse argparse + diff vs CLAUDE.md catalog).

### Fase 3 — 20 scripts adicionados ao catalog (Mega Audit MA-UN-*)

Sub-agent processou `Mega_Audit_2026-04-28.md` e adicionou 18 rows + 1 secção "Legacy migrations":
- **Helena**: `helena/report.py`
- **Bibliotheca**: `build_glossary.py`, `build_knowledge_cards.py`, `dossier_tutor.py`
- **RI / CVM**: `cvm_parser.py`, `cvm_parser_bank.py`, `quarterly_single.py`, `fii_filings.py`, `catalog_autopopulate.py`, `cvm_pdf_extractor.py`
- **Fetchers**: `fetch_kings_aristocrats.py`, `massive_fetcher.py`, `backfill_us_bank_tangibles.py`
- **Ops**: `export_macro_csv.py`, `notify_events.py`, `rotate_logs.py`, `telegram_loop.py`, `vault_clean_video_names.py`
- **Legacy migrations** (kept for disaster recovery): `migrate_fundamentals_extra.py`, `migrate_thesis_health.py`

### Fase 4 — Code refactor (CH005 cleanup)

`fetchers/subscriptions/_pdf_extract.py` — `requests.post(OLLAMA_URL, ...)` → `agents._llm.ollama_call(...)`. Removeu `import requests` + `OLLAMA_URL` constant. Smoke test: import OK.

**Material finding** (não corrigido — precisa decisão arquitectural):
- `code_health` perpetuum tem **3 false-positives** (paths de ficheiros já apagados continuam em `perpetuum_health` table). Ex: `scripts/overnight/populate_thesis.py`, `scripts/overnight/ab_qwen3_vs_14b.py`, `scripts/overnight/generate_methods_from_damodaran.py` — não existem mais (cemetery? deleted?), mas perpetuum reportou-os hoje. **Recomendação**: adicionar staleness gate ao `code_health` — se `not Path(file).exists()` → flag para limpeza, não score.

### Fase 5 — Memory pointers (8 ficheiros)

Cada uma das memory entries code-heavy agora abre com `**📚 Canonical doc**: …` apontando ao playbook L2:
- `library_and_paper_trade.md` → `[[Library_Pipeline]]`
- `phase_x_perpetuum_engine.md` → `[[Perpetuum_Engine]]`
- `phase_y_ri_knowledge_base.md` → `[[RI_Knowledge_Base]]`
- `bibliotheca_v2.md` → `[[Bibliotheca_v2]]`
- `phase_k_autoresearch_tavily.md` → `[[Tavily_Integration]]`
- `phase_k2_tavily_3_wires.md` → `[[Tavily_Integration]]`
- `phase_k3_tavily_skills_cli.md` → `[[Tavily_Integration]]`
- `phase_dd_bibliotheca.md` → `[[Bibliotheca_v2]]`

Plus o `phase_q_youtube_ingest_built.md` actualizado na sessão anterior.

### Fase 6 — Wiki Index reorganizado

`wiki/Index.md` Playbooks 8 → **17**. 3 categorias:
- **Meta + workflow**: Token_discipline, Agents_layer, Perpetuum_Engine, Daily_Orchestration, Analysis_workflow, Analyst_Tracking, Telegram_setup
- **Decisão / execução**: Verdict_Engine, Buy_checklist, Sell_triggers, Rebalance_cadence, Tax_lot_selection_practical, Critical_Thinking_Stack
- **Ingest pipelines (zero Claude tokens)**: Youtube_Pipeline, Library_Pipeline, Web_scraping_subscriptions, RI_Knowledge_Base, Bibliotheca_v2, Tavily_Integration

### Fase 7 — Background runs (idempotente)

- `research_digest.py` 2026-04-28 → confirmou 31 clippings sources / 303 chunks (validou minhas correcções de count)
- `conviction_score --universe --top 10` → **scored 0 tickers**. Open issue (ver abaixo).

---

## 🚨 Material findings (priority)

### HIGH

**M1. Conviction score retorna 0 tickers em universe-wide run**
- `python -m analytics.conviction_score --universe --top 10` corre OK mas reporta `Tickers scored: 0` e tabela vazia.
- Memory diz "33→184 subjects (5.6x), 86 high-conviction ≥70 (Phase J)" — descordância vs estado actual.
- Hipótese: talvez precisa flag adicional, ou DB não tem inputs (fundamentals stale?). Investigar amanhã.
- Action: `python -m analytics.conviction_score --universe --top 10 -v` (se há flag verbose) ou inspect manual.

**M2. Code health perpetuum tem 3 false-positive paths**
- 3 dos 5 ficheiros CH005 reportados hoje (`scripts/overnight/{populate_thesis, ab_qwen3_vs_14b, generate_methods_from_damodaran}.py`) **não existem** no filesystem.
- Perpetuum está scoring entries fantasma — ruído no signal.
- Action: adicionar `Path(file).exists()` gate ao code_health scanner; cleanup table ou flag stale rows.

### MEDIUM

**M3. CLAUDE.md catalog não tem auto-validation contra argparse**
- 5 drifts encontrados nesta sessão. Provavelmente há mais que não verifiquei sistematicamente.
- Action: adicionar **CH008** ao code_health perpetuum — parse argparse de cada `__main__` e diff vs catalog row. Reportar drifts.

**M4. Library matcher sem cooldown / unique-on-open**
- `library/matcher.py::apply_method` cria signal toda vez que rules passam. Mitigação actual: `library_signals` perpetuum frozen (`enabled=False`).
- Action: adicionar UNIQUE constraint em `paper_trade_signals(ticker, method, status='open')` ou cooldown timestamp.

### LOW

**M5. Library status string drift**
- `paper_trade.py` legacy escreve `'closed_win'`/`'closed_loss'`/`'closed_flat'`; `paper_trade_close.py` moderno escreve `'closed'` + `notes.win`. Convergente em rows novas mas legacy strings podem coexistir.
- Action: data audit script para count rows por status string; opcional migration to normalize.

**M6. `bank_quarterly_history` cobertura limitada**
- 5 bancos: ABCB4, BBAS3, BBDC4, BPAC11, ITUB4. Faltam: SANB11, BPAN4, SANTANDER (subsidiária), BMGB4, BIDI11, INBR32 (Inter).
- Action: estender `library/ri/catalog.yaml` + smoke run `bank_quarterly_single` para cada um.

---

## 📋 Recommendations (próxima sessão)

1. **Implementar CH008** (catalog-vs-argparse drift detector). Incremental — começar com top-20 scripts.
2. **Investigar conviction_score zero output** — bug ou stale state.
3. **Code_health staleness gate** — `Path(file).exists()` antes de score.
4. **Library matcher unique constraint** — destravar `library_signals` perpetuum (T0 → T1).
5. **Bank coverage extension** — +5 bancos no RI catalog.
6. **Periodic catalog audit** — Mega Audit + drift detector como cron mensal.

---

## 📦 Files changed (commit scope)

### Created (10)
- `obsidian_vault/wiki/playbooks/Youtube_Pipeline.md`
- `obsidian_vault/wiki/playbooks/Library_Pipeline.md`
- `obsidian_vault/wiki/playbooks/Perpetuum_Engine.md`
- `obsidian_vault/wiki/playbooks/Tavily_Integration.md`
- `obsidian_vault/wiki/playbooks/RI_Knowledge_Base.md`
- `obsidian_vault/wiki/playbooks/Critical_Thinking_Stack.md`
- `obsidian_vault/wiki/playbooks/Bibliotheca_v2.md`
- `obsidian_vault/wiki/playbooks/Verdict_Engine.md`
- `obsidian_vault/wiki/playbooks/Daily_Orchestration.md`
- `obsidian_vault/Bibliotheca/Midnight_Work_2026-04-28.md` (este ficheiro)

### Modified (3)
- `CLAUDE.md` — 5 drift fixes + 18 catalog rows added + legacy migrations subsection
- `obsidian_vault/wiki/Index.md` — Playbooks 8 → 17, reorganized into 3 categories
- `fetchers/subscriptions/_pdf_extract.py` — CH005 fix (canonical `ollama_call`)

### Memory updated (8 pointers, in `~/.claude/projects/.../memory/`)
- 8 memory files now point to canonical vault docs

---

## ⏱️ Stats

| Métrica | Valor |
|---|---|
| Wall time | ~2h |
| Sub-agents spawned | 8 (paralelos, cada um isolado) |
| Vault lines added | ~2,300 (incluindo este relatório) |
| CLAUDE.md lines added | +29 (catalog rows) |
| Lines removed (code) | -10 (CH005 refactor) |
| Tavily calls | 0 (toda a research foi cache + filesystem) |
| Ollama calls | 1 (research_digest perpetuum, idempotent re-run) |
| DB writes | 0 directos (só via approved scripts) |

---

## 🚪 Para retomar

Próxima sessão deve começar por:
1. Ler `obsidian_vault/CONSTITUTION.md` (✓ Voltamos secção)
2. Ler este relatório
3. Decidir: M1 (conviction zero) ou M3 (CH008 catalog drift detector) primeiro

Padrão estabelecido: **wiki/playbooks/ é a fonte canónica para "como funciona X"**. Memory entries só devem conter history + non-obvious gotchas + project state. Code é fonte da verdade para implementação; playbook é fonte da verdade para arquitectura + comandos.
