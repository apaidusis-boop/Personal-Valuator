---
type: manual
tags: [manual, sistema, walkthrough, overhaul]
date: 2026-05-13
status: working_draft
parent: "[[CONSTITUTION]]"
sibling: "[[Bibliotheca/Manual_de_Direcao]]"
---

# 🛠️ Manual do Sistema — Como tudo opera

> **Propósito**: este doc é o **mapa passo-a-passo** de como o sistema funciona hoje. Para cada workflow declara: **trigger · agents (handle do [[AGENTS_REGISTRY]]) · fluxo de dados · falhas observadas · porquê construído assim · cleanup proposto**.
>
> **Companion docs**:
> - [[CONSTITUTION]] — filosofia mãe (lê primeiro)
> - [[CONSTITUTION_Pessoal]] — regras só do mundo pessoal
> - [[AGENTS_REGISTRY]] — handles canónicos `area.funcao`
> - [[Bibliotheca/Manual_de_Direcao]] — linguagem de investidor (output)
> - [[Agents Review]] — inventário com status/decisão
>
> **Pretende substituir**: a sensação de "circles" — esse doc é a régua única.

---

## 📜 Parte I — Filosofia

### O que queremos alcançar
- **Investidor pessoa física** a operar em **BR (B3) + US (NYSE/NASDAQ)**.
- **Horizonte: anos**. Não traders.
- **Estratégia core**: **DRIP** (reinvestimento de dividendos) + **Buffett/Graham** (qualidade + margem de segurança).
- **Decisões claras e rápidas** — output bruto na CLI, output polido no Obsidian/dashboard ("Escritório").
- **Validação antes de capital** — Phase GG (deploy) só arranca depois de ≥90d de verdicts validados (~Ago/2026).

### Os 7 não-negociáveis do mundo Pessoal (de [[CONSTITUTION_Pessoal]])
1. **A carteira real é sagrada** — consultar `portfolio_positions` na DB; nunca pedir quantidades; nunca writes destrutivos em `data/`.
2. **Blacklist viva** — TEN não-adicionar, GREK não-DRIP, RBRX11→KNHF11, PVBI11 contrarian-keep.
3. **Intenção por posição** — DRIP vs Growth vs Compounder difere por ticker. XP=growth. BN=post-split.
4. **CLI = sala do chefe; Obsidian = Escritório** — bruto vs polido.
5. **Trabalho autónomo OK** — overnight/midnight enrichment+cleanup; proibido data/ destrutivo + force-push + Tavily over-quota.
6. **Output = verdade comprimida** — meia página + 1 gráfico > relatório de 10 páginas.
7. **Direcção, não micro-aprovação** — "Avança com X" = ação total, leio no Escritório depois.

### Filosofia "in-house first" (regra-mãe acima de tudo)
**Ollama + SQL + scripts locais ANTES de Claude API**. Claude API é último recurso. Ver [[feedback_inhouse_first]].

---

## 🏗️ Parte II — Estrutura física

### Bases de dados (2, isoladas)
- `data/br_investments.db` — SQLite BR. Schema: companies, prices, fundamentals, scores, events, portfolio_positions, paper_trade_signals, watchlist_actions, thesis_health, verdict_history, fair_value, bank_quarterly_history, quarterly_history, perpetuum_health, etc.
- `data/us_investments.db` — Schema idêntico. **Nunca misturar moeda** (BRL fica em BR, USD em US).

### Vault Obsidian (`obsidian_vault/`)
Hubs centrais (visíveis no graph view):
- **`_LEITURA_DA_MANHA`** — daily reading hub; linka todos os tickers mencionados no briefing matinal. Diário, gerado pelo `ops.briefing`.
- **`_MASTER`** — master hub de tickers; cada wiki/holding linka aqui.
- **`CONSTITUTION`** + **`CONSTITUTION_Pessoal`** + **`CONSTITUTION_Comercial`** — filosofia.
- **`agents/`** — Council personas (10 pastas com reviews por ticker).
- **`Bibliotheca/`** — Knowledge Cards + Manual_de_Direcao + Disciplina_de_Investidor + clippings.
- **`Glossary/`** — métricas (Graham_Number, ROE, Moat, DRIP, etc.) que ligam aos DOSSIES.
- **`dossiers/`** — `<TICKER>_DOSSIE.md` + `<TICKER>_FILING_<DATE>.md` + `<TICKER>_IC_DEBATE.md` + `<TICKER>_COUNCIL.md` + `<TICKER>_STORY.md`.
- **`wiki/holdings/`** — wiki pages por holding.
- **`Sessions/`** — handoff notes por sessão.
- **`skills/`** — skills MOC + Roadmap + skills custom.
- **`Comercial/`** — mundo comercial (blueprint).

### Agents (do [[AGENTS_REGISTRY]], 7 áreas)
| Área | Handles | Cadência |
|---|---|---|
| **`ops.*`** (5) | briefing, watchdog, telegram-bridge, orchestrator, janitor | daily / every:15m / every:2m / on-demand / weekly |
| **`research.*`** (7+3 stubs) | scout, thesis-refresh, subscriptions, autoresearch, ic-debate, variant, journal, wiki-stub, thesis-stub | daily / weekly / on-demand |
| **`risk.*`** (5) | drift-audit, devils-advocate, compliance, thesis-health, security | daily / weekly |
| **`perf.*`** (2) | backtest-analysts, portfolio-matcher | weekly / every:30m |
| **`design.*`** (6) | lint, scout, curate, spike, cruft-detector, code-lint | on-demand / weekly / daily |
| **`council.*`** (9) | banks-br/us, industrials-br/us, commodities-br, fiis-br, reits-us, macro, allocation | on-demand (per ticker debate) |
| **`perp.*`** (15) | thesis, vault-health, data-coverage, content-quality, method-discovery, token-economy, library-signals, ri-freshness, code-health, autoresearch, bibliotheca, dreaming, security, daily-delight, meta | daily via `perpetuum.master` |

### Fontes de dados (cascade)
| Mercado | Primária | Fallback | Notas |
|---|---|---|---|
| BR | CVM filings + fiis.com.br + yfinance (.SA) | Fundamentus + Status Invest MCP + BACEN IF.Data | brapi.dev removido c807140 |
| US | SEC EDGAR XBRL + FMP | Massive (ex-Polygon) + yfinance (último recurso) | **yfinance NÃO é primary para US** ([[feedback_avoid_yfinance_us]]) |
| Macro | FRED (US) + BCB SGS (BR) | — | Selic, CDI, USDBRL, DGS10 |
| News | SEC + CVM monitors + Exa + Tavily | yt_poll + pod_poll | Hourly + q4h |

---

## 🔄 Parte III — Workflows passo-a-passo

> Cada workflow tem 6 campos. Falhas marcadas com 🐛. Cleanups marcados com ✂️.

---

### A. Briefing matinal (06:00 → 09:30)

🎯 **Trigger**: `scripts/daily_run.bat` (cron 23:30 noite anterior) + `ops.briefing` (cron 07:00) + `ii agent` (CLI 09:30).

🧑‍🤝‍🧑 **Handles**:
- `ops.briefing` (`agents/morning_briefing.py`) — compila briefing matinal via Ollama Qwen 14B.
- `ops.watchdog` (`agents/watchdog.py`) — every:15m, detecta filings novos + cron failures.
- `risk.thesis-health` — corre via `perpetuum.master`, gera thesis_health table.
- `ops.telegram-bridge` (`scripts/telegram_loop.py`) — push final para Telegram.

📊 **Fluxo de dados**:
1. (23:30 noite anterior) `daily_run.bat` corre 20 scripts: prices/fundamentals BR+US + perpetuum_master + paper_trade_close + glossary build + dossier tutor + telegram brief.
2. (07:00) `ops.briefing` lê `verdict_history`, `thesis_health`, `events` (filings novos 24h), `fair_value` (action mudou?), `data_confidence` (alerts).
3. Output: Markdown narrativo + push Telegram via `captains_log_telegram.py`.
4. Linka para `_LEITURA_DA_MANHA.md` no vault — cada ticker mencionado vira aresta.

🐛 **Falhas observadas**:
- Briefing às vezes traz tickers da watchlist sem distinção clara das holdings (cleanup needed).
- Hierarquia de prioridade não está clara — qual ticker é "urgente hoje" vs "context"?
- Quando perpetuum.master falha à noite, briefing da manhã usa thesis_health stale.

🤔 **Porquê construído assim**:
- Cron noite anterior porque BR+US fechados + 8h de Ollama heavy work disponíveis sem conflito com user.
- Briefing matinal só roda agregações + narrative — evita refazer trabalho pesado de noite.
- Telegram push para user ver antes mesmo de abrir o PC.

✂️ **Cleanup proposto**:
- Definir **camada de prioridade** clara no briefing: 🔥 Action-needed > ⚠️ Watchlist > 📌 Context.
- Ligar `_LEITURA_DA_MANHA` ao **Manual_de_Direcao** (linguagem de investidor) para output ser sempre "fosso/margem/o que mata a tese", não "score=0.42".
- Remover briefings antigos com info errada (pré-Phase LL multi-source — anteriores a 2026-05-08).

---

### B. Filing Reactor (real-time)

🎯 **Trigger**: `hourly_run.bat` (SEC+CVM monitors) → `q4h_run.bat` (auto_verdict_on_filing).

🧑‍🤝‍🧑 **Handles**:
- `research.scout` (`agents/research_scout.py`) — scout filings (CVM IPE + EDGAR).
- `monitors/sec_monitor.py` + `monitors/cvm_monitor.py` — escrevem events table.
- `monitors/cvm_pdf_extractor.py` — q4h: PDFs → events.full_text (pdfplumber).
- `scripts/auto_verdict_on_filing.py` — q4h: re-corre fair_value sobre filing → escreve `dossiers/<TK>_FILING_<DATE>.md`.
- `scripts/auto_verdict_on_content.py` — content mismatch detection.
- `scripts/notify_events.py` — hourly: Windows Toast para holdings críticos.

📊 **Fluxo de dados**:
```
SEC EDGAR / CVM IPE
  → sec_monitor / cvm_monitor (hourly)
    → events table (ticker, kind, date, url)
      → cvm_pdf_extractor (q4h, only pending)
        → events.full_text (Qwen-ready)
          → auto_verdict_on_filing (q4h)
            → re-roda fair_value v2 + data_confidence
              → dossiers/<TK>_FILING_<DATE>.md
                → Mission Control alerts ribbon
                → notify_events (Toast)
                → ops.briefing pega na próxima run
```

🐛 **Falhas observadas**:
- 41 URLs CVM com `verified:false` ([[ri_resolver_overhaul_2026-05-11]]) — fonte de filings partidos.
- yfinance ainda no primary cascade para US — viola [[feedback_avoid_yfinance_us]]. **Reparar `config/sources_priority.yaml`**.
- Filings antigos no events table podem disparar verdict re-runs desnecessários (cleanup do events.full_text > 180d).

🤔 **Porquê construído assim**:
- Hourly+q4h em vez de single daily porque earnings/8-K podem chegar em qualquer hora.
- PDFs extraídos em batch q4h porque pdfplumber é lento (~5s/PDF) — não bloqueia hourly.
- `auto_verdict_on_filing` escreve markdown porque é o tier de leitura (Escritório).

✂️ **Cleanup proposto**:
- ✅ Reordenar `config/sources_priority.yaml` (US: FMP + SEC primary; yfinance último).
- ✅ Adicionar guard `WARN if yfinance_used_as_primary_for_us`.
- ✂️ Apagar `dossiers/<TK>_FILING_<DATE>.md` anteriores a 2026-05-08 (Phase LL closeout — antes disso eram single-source unreliable).

---

### C. Deepdive — ticker on-demand

🎯 **Trigger**: `ii deepdive <TK>` (CLI) ou via Antonio Carlos no Telegram.

🧑‍🤝‍🧑 **Handles**:
- `ii deepdive <TK>` — 4 layers: Auditor + Scout + Historian + Strategist.
- **Auditor**: Piotroski + Altman + Beneish + **Moat** (`scoring/moat.py`).
- **Scout**: yfinance news/insider/short/consensus.
- **Historian**: delta vs last deepdive.
- **Strategist**: Llama dossier 5k palavras (Ollama).

📊 **Fluxo de dados**:
```
ii deepdive ACN
  → Auditor (Piotroski 0-9 + Altman Z + Beneish M + Moat 0-10)
  → Scout (news + insider + short + consensus)
  → Historian (delta vs reports/deepdive/ACN_*.json mais recente)
  → Strategist (Llama 5k-word dossier OU --no-llm para skip)
  → reports/deepdive/ACN_YYYYMMDD.json
  → (--save-obsidian) obsidian_vault/dossiers/ACN.md
```

🐛 **Falhas observadas**:
- Antigos deepdives feitos antes de Phase LL multi-source — métricas potencialmente erradas (yfinance-only fundamentals).
- Strategist Llama 5k palavras pode ter "AI slop" sem ser challenged (devils-advocate não está wired no pipeline).
- Beneish M-Score exclui banks/REITs — mas pipeline não flagga claramente.

🤔 **Porquê construído assim**:
- 4 layers paralelas porque cada faz coisa diferente; Auditor é deterministic, Strategist é generative (precisa Ollama).
- JSON + Obsidian para ter tier raw + tier polido.
- `--no-llm` flag porque Llama é caro em VRAM e às vezes só queres os números do Auditor.

✂️ **Cleanup proposto**:
- ✂️ **Apagar deepdives anteriores a 2026-05-08** (`reports/deepdive/*_pre_LL.json`) — antes da Phase LL multi-source eram unreliable. Reproduzir só os 33 holdings + watchlist prioritária com pipeline atual.
- 🔗 Wire `risk.devils-advocate` antes do Strategist para reduzir slop.
- 🔗 Wire `risk.thesis-health` no Historian para sinalizar drift.

---

### D. Verdict + Decision Aggregation

🎯 **Trigger**: `ii verdict <TK>` (CLI) ou auto-trigger via `auto_verdict_on_filing`.

🧑‍🤝‍🧑 **Handles**:
- `scoring/fair_value.py` (v2, com banda + 6-stance action + history).
- `scoring/_safety.py` (per-sector margins).
- `analytics/data_confidence.py` (3-way voting yf↔filings↔scrape).
- `analytics/conviction_score.py` (0-100 composite).
- `scripts/predictions_evaluate.py` (closes analyst predictions; tracks win_rate).
- `scripts/verdict_history_*.py` — `ii vh record`, `ii vh backtest`, `ii vh show`.

📊 **Fluxo de dados**:
```
fair_value (v2)         → our_fair + banda + action (BUY/HOLD/AVOID/SELL)
  + data_confidence     → confidence_label (HIGH/MED/LOW + disputed?)
  + safety_margins      → per-sector adjust
  + conviction_score    → composite 0-100
  → verdict_history table (append-only)
  → ii verdict ACN output: action + reasoning + 1-line
  → vault/dossiers/ACN_DOSSIE.md update
```

🐛 **Falhas observadas**:
- Phase FF closed-loop validation: BUY hit rate **0% US (n=3) / 16.7% BR (n=6)** — n é pequeno, precisamos 30/90d (~Ago/2026).
- Algumas verdicts antigas no `verdict_history` antes da Phase KK eram single-source — devem ser flagged como `legacy_single_source` na DB.
- `predictions_evaluate.py` corre mas predictions só fecham a partir de Jul/2026 (horizons 30/90/180d).

🤔 **Porquê construído assim**:
- 6-stance action (não só BUY/SELL) porque "AVOID" e "TRIM" são acionáveis distintos.
- Append-only history porque queremos backtest do nosso próprio engine.
- Data confidence porque yfinance + filings discordam às vezes (VALE3 R$90 vs R$57).

✂️ **Cleanup proposto**:
- ✂️ **Migration**: marcar `verdict_history` rows pre-Phase-KK (anteriores a 2026-05-08) como `data_source='legacy_single'`. Excluir do backtest. Não apagar (precisamos para track record histórico).
- 📊 Quando ≥90d verdicts validados, **Phase GG** activa capital deployment engine.

---

### E. Library + Clippings + Bibliotheca (knowledge accumulation)

🎯 **Trigger**: `ii subs fetch --source all` (weekly), `python -m library.ingest` (when adding book), `library.clippings_ingest` (when user drops content in `obsidian_vault/Clippings/`).

🧑‍🤝‍🧑 **Handles**:
- `research.subscriptions` (`agents/subscription_fetch.py`) — Sofia Clippings: fetch Suno/XP/WSJ/Finclass weekly.
- `library.ingest` — PDF → chunks (markitdown ou pypdf).
- `library.clippings_ingest` — vault/Clippings → chunks_index.
- `library.extract_insights` — book → methods.yaml via Ollama.
- `library.matcher` — methods vs portfolio.
- `library.rag.{build,query,ask}` — RAG sobre chunks.
- `scripts/build_glossary.py` — métricas Glossary.
- `scripts/build_knowledge_cards.py` — synthesis filosofia.
- `scripts/dossier_tutor.py` — injecta `## Tutor` em DOSSIE.md.
- `scripts/research_digest.py` — daily Bibliotheca digest.

📊 **Fluxo de dados**:
```
PDF/EPUB book              → library.ingest (chunks via markitdown)
news/research clipping     → vault/Clippings/*.md
weekly Suno/XP/WSJ pull    → research.subscriptions → subscriptions table
                                ↓
                          library.clippings_ingest → chunks_index
                                ↓
                          library.rag.build (nomic-embed local)
                                ↓
                      ii vault "pergunta" → library.rag.ask (Qwen synth PT)
                                ↓
                       Knowledge Cards + Glossary + Tutor (daily refresh)
```

🐛 **Falhas observadas**:
- **User pediu explicitamente nesta sessão**: muitos news lidos por dia → agente devia identificar clipping + auto-tag por tópico do artigo. **Hoje a tagging é manual** ou ausente.
- Knowledge Cards antigos podem ter info defasada (pre-Phase LL).
- Clippings sem schema consistente — alguns têm front-matter, outros não.
- Library books sem nada de comecial pode aparecer (Maybe-OK, but user prefers focused).

🤔 **Porquê construído assim**:
- RAG local (nomic-embed + Qwen 14B) por `feedback_inhouse_first` — não queimar Claude API por query.
- Glossary + Tutor + Knowledge Cards = 3 níveis: definição → contexto narrativo → aplicação no DOSSIE.
- Subscriptions weekly porque é o ritmo dos providers (Suno semanal, XP mensal).

✂️ **Cleanup + 🌱 promoção**:
- 🌱 **Novo agent**: `research.auto-tag-clippings` — observa `vault/Clippings/`, classifica artigo por sector/tema/ticker mentioned, escreve YAML front-matter tags. Ollama Qwen 14B + lista de tags canónicas de `config/topic_watchlist.yaml`. **Promover** para sprint imediato (user explicit ask).
- ✂️ Re-build `Knowledge Cards` (`scripts/build_knowledge_cards.py --force`) com fontes pós-LL.
- 🔧 Adicionar front-matter schema obrigatório em `vault/Clippings/` (date + source + tickers + topics).

---

### F. Council Debate (multi-persona on-demand)

🎯 **Trigger**: `python -m agents.council.story <TK>` (CLI) ou via Antonio Carlos.

🧑‍🤝‍🧑 **Handles** (do [[AGENTS_REGISTRY]]):
- `council.coordinator` — orquestra debate 2-round.
- `council.banks-br` / `council.banks-us` — bancos.
- `council.industrials-br` / `council.industrials-us` — empresas operacionais.
- `council.commodities-br` — cíclicos.
- `council.fiis-br` / `council.reits-us` — REITs/FIIs.
- `council.macro` — overlay macro (chamada quando macro_exposure ≥ 4).
- `council.allocation` — sizing + correlação.
- `council.dossier` — factual layer (sem opiniões).
- `council.evidence` — Evidence Ledger (Sprint 3 STORYT_3.0).
- `council.peer-engine` — peer comparison (Sprint 2).
- `council.valuation` — DCF + múltiplos deterministic.
- `council.narrative` — Narrative Engine (chunked).
- `council.render` — transcript com wikilinks.
- `council.versioning` — Delta Engine (Sprint 4).
- `council.cache-policy` — smart re-run.
- `council.agent-reviews` — escreve `vault/agents/<persona>/reviews/<TK>_<DATE>.md`.

📊 **Fluxo de dados**:
```
ii deepdive ACN ... OU ... user pede council ACN
  → council.coordinator
    → council.roster (modo ACN = A-US Buffett → Charlie Compounder / industrials-us)
    → council.dossier (lê DB: prices, fundamentals, events, scores)
    → council.research-brief (fetch news + analyst views)
    → council.peer-engine (comps spread)
    → council.valuation (DCF + múltiplos)
    → Round 1: persona principal escreve verdict
    → Round 2: council.macro + council.allocation overlay
    → council.evidence (ledger)
    → council.narrative (deterministic-numbers narrative)
    → council.render → vault/dossiers/ACN_COUNCIL.md + ACN_STORY.md
    → council.agent-reviews → vault/agents/Charlie Compounder/reviews/ACN_2026-05-13.md
```

🐛 **Falhas observadas** (image 3 mostra):
- **Mesh denso de COUNCIL/STORY/IC_DEBATE files por ticker** — 4-5 ficheiros por ticker × 33 holdings = ~150 ficheiros no grafo. Visualmente ruidoso.
- Personas com **poucos reviews** (Tião Galpão 2, Walter Triple-Net 2, Aderbaldo Cíclico 2) — provavelmente spawned em watchlist e depois nunca mais. **Cleanup ou promoção.**
- Pastas `vault/agents/<persona>/` continuam com nome de persona (não handle `area.funcao`). Memory rule diz handle.
- IC_DEBATE files (do `research.ic-debate`) e COUNCIL files (do `council.coordinator`) **sobrepõem-se conceptualmente** — ambos são "multi-persona view". User pode confundir.

🤔 **Porquê construído assim**:
- Personas nomeadas (Charlie, Mariana, ...) porque narrative briefings funcionam melhor com nomes humanos do que com handles técnicos.
- Mas: handle técnico (`council.industrials-us`) ainda é o identificador canónico no [[AGENTS_REGISTRY]].
- 2-round debate porque round 1 captura o principal-specialist verdict + round 2 challenges com macro/allocation.

✂️ **Cleanup proposto**:
- ✂️ **Consolidar IC_DEBATE vs COUNCIL** — escolher um único formato. Recomendo manter **COUNCIL** (mais completo, multi-persona com macro/allocation overlay) e deprecar **IC_DEBATE** (era da Phase AA original synthetic_ic, mais antigo).
- ✂️ Renomear pastas `vault/agents/<persona>/` para `vault/agents/<handle>/` (ex: `vault/agents/council.industrials-us/`) e deixar `<persona>` como alias front-matter.
- ✂️ Apagar reviews COUNCIL/STORY/IC_DEBATE anteriores a 2026-05-08 (Phase LL closeout). Re-correr `council.story` para 33 holdings com pipeline current.
- ⭐ Promover uso: depois do cleanup, correr `council.story` sobre **toda a watchlist priority** + spawn nas personas pouco-usadas (Tião/Walter/Aderbaldo) para validar relevância.

---

### G. Perpetuums (background validation, 15 daemons)

🎯 **Trigger**: `perpetuum.master` no cron diário (23:30 noite, parte de `daily_run.bat`).

🧑‍🤝‍🧑 **Handles** (15, em [[AGENTS_REGISTRY]]):
- `perp.thesis` ⭐ (Heart of Phase W) — valida thesis por ticker.
- `perp.vault-health`, `perp.data-coverage`, `perp.bibliotheca`, `perp.ri-freshness`, `perp.autoresearch`, `perp.code-health`, `perp.security`, `perp.method-discovery` — todos active.
- `perp.content-quality`, `perp.token-economy`, `perp.library-signals` — frozen ⚠️.
- `perp.dreaming`, `perp.daily-delight` — manual ⚪.
- `perp.meta` — audita os outros perpetuums.

📊 **Fluxo de dados**:
```
23:30 daily_run.bat
  → perpetuum.master
    → para cada perp.*:
        → score 0-100 por subject (ticker/file/etc)
        → escreve perpetuum_health table (BR + US)
        → propõe T1 (audit-only) ou T2+ (action needs approval)
    → ações T2+ visíveis via `python scripts/perpetuum_action_run.py list-open`
    → user revisa: ii perpetuum-review (skill)
    → approve → executa whitelist command
    → reject/defer → marca closed
```

🐛 **Falhas observadas**:
- 3 perpetuums frozen (`content-quality`, `token-economy`, `library-signals`) — provavelmente desactualizados, **investigar e remover OU descongelar**.
- Volume de T2 actions altas (~10-30/dia) — user não revisa todas, fica backlog.
- `perp.dreaming` e `perp.daily-delight` são OpenClaw-era ideas que talvez não se apliquem aqui (user mencionou isto).

🤔 **Porquê construído assim**:
- Background validation continua mesmo sem user input — captura drift entre runs.
- T1/T2 tier porque audit-only é safe automatic; T2+ precisa human-in-the-loop.
- `perp.meta` no fim porque audita os outros (compliance officer).

✂️ **Cleanup proposto**:
- ❓ **Investigar cada frozen**: `perp.content-quality` / `perp.token-economy` / `perp.library-signals`. Se sem uso real, **remover do `_registry.py`**.
- ❓ **Avaliar OpenClaw-era**: `perp.dreaming` (memory consolidation) e `perp.daily-delight` (wake-up gift) — user duvida da relevância. **Decisão: manter se gerou algo útil últimos 30 dias; senão remover.**
- 🔧 **Backlog management**: criar `ii perpetuum-review --priority high` para filtrar só ações urgentes.

---

### H. Vault hubs (_MASTER, _LEITURA_DA_MANHA, Glossary↔DOSSIE)

🎯 **Trigger**: vivem como notas estáticas, actualizadas por scripts.

🧑‍🤝‍🧑 **Handles + scripts**:
- `_LEITURA_DA_MANHA.md` — actualizado por `ops.briefing` (linka tickers mencionados).
- `_MASTER.md` — master index; actualizado por `scripts/obsidian_bridge.py`.
- `Glossary/*.md` (Graham_Number, ROE, Moat, DRIP, etc.) — gerados/refresh por `scripts/build_glossary.py` (diário).
- `dossiers/<TK>_DOSSIE.md` — base ticker note; injectada por `scripts/dossier_tutor.py` com secção `## Tutor` + links para Glossary.
- `wiki/holdings/<TK>.md` — wiki autorada (alguns auto_draft via `research.wiki-stub`).

📊 **Fluxo visual** (do graph view nas imagens):
```
CONSTITUTION ─┬─ Glossary/* (Graham_Number, ROE, Moat, ...)
              │     ↕ (backlinks bidirectional)
              │   dossiers/<TK>_DOSSIE.md ←──→ wiki/holdings/<TK>.md
              │     ↕
              ├─ _LEITURA_DA_MANHA (daily) ──→ tickers mencionados
              ├─ _MASTER (always) ──→ all tickers
              └─ agents/<persona>/reviews/<TK>_<DATE>.md
```

🐛 **Falhas observadas**:
- Image 7 mostra **`_INDEX` órfão** — note vazia ou sem linkagem real. **Apagar ou popular**.
- Image 8 mostra pasta `data/_` ou similar vazia. **Investigar**.
- Alguns DOSSIES antigos não têm secção Tutor / Glossary links porque `dossier_tutor.py` foi adicionado depois.
- Vault graph denso (image 5/6) — pode ser sinal de "demasiado linking", ou pode ser sinal de "knowledge graph rico". User decide.

🤔 **Porquê construído assim**:
- _LEITURA_DA_MANHA + _MASTER como hubs porque dão um "ponto de entrada único" no vault.
- Glossary↔DOSSIE bidirectional porque user lê DOSSIE → quer entender métrica → vai ao Glossary; ou lê Glossary → quer exemplos → vai aos DOSSIES.
- Constitution como root porque é o "porquê" de todas as decisões.

✂️ **Cleanup proposto**:
- ✂️ Apagar `_INDEX` órfão (image 7).
- ✂️ Identificar e apagar pastas vazias (image 8 — `data/_`).
- 🔧 Correr `python -m agents.perpetuum.vault_health` para listar broken links + orphans, depois bulk-fix.
- 🌱 **Conexão promovida**: cada DOSSIE deve linkar pelo menos para 1 Knowledge Card da Bibliotheca (filosofia aplicada ao ticker).

---

### I. Mission Control + Telegram (interfaces)

🎯 **Trigger**: `ii missioncontrol` (Next.js, localhost:3000) + Telegram bot Jarbas (long-poll).

🧑‍🤝‍🧑 **Handles**:
- `ops.orchestrator` (`agents/chief_of_staff.py` Qwen 32B + `agents/fiel_escudeiro.py` Claude CLI) — Antonio Carlos / Fiel Escudeiro tool-calling.
- `ops.telegram-bridge` (`agents/telegram_controller.py` + `scripts/telegram_loop.py`) — Zé Mensageiro long-poll.
- 16 tools accessible: verdict/deepdive/posição/regime/portfolio/IC/variant/web/etc.
- `agents/voice_input.py` + `agents/voice_output.py` — Telegram audio.
- Mission Control panes: Home / Tasks / Content / Calendar / Projects / Memory / Docs / Team / Visual.

📊 **Fluxo de dados**:
```
Telegram user msg (text or audio)
  → telegram_loop.py getUpdates
    → (if audio) voice_input → Whisper + Qwen intent
    → ops.orchestrator (Antonio Carlos OR Fiel Escudeiro)
      → tool-calling loop (16 tools)
        → SQL queries / agent calls / vault reads
        → resposta narrativa Qwen
    → (if requested) voice_output → TTS pyttsx3
    → Telegram push

Mission Control (localhost:3000)
  → React/Next.js reads SQLite + vault directo (no API layer)
  → chat widget bottom-right → spawn ops.orchestrator
  → action buttons → /api/actions/<id> → spawn Python
```

🐛 **Falhas observadas**:
- Mission Control dashboard ainda tem "AI slop" em alguns componentes (Phase MM design overhaul em curso).
- Tools loop ocasionalmente trava em loops longos sem yield.
- Voice input em PT às vezes erra ticker (BBAS3 vira "B-B-A-S três").

🤔 **Porquê construído assim**:
- Antonio Carlos para Telegram conversational; Fiel Escudeiro para acesso elevado via MC.
- Tool-calling loop porque queries do user são open-ended; um dispatcher rígido não cobre tudo.
- MC reads SQLite directo (no API layer) porque é localhost single-user — não precisa REST overhead.

✂️ **Cleanup proposto**:
- 🌱 **Aplicar Manual_de_Direcao** — tools que devolvem texto devolvem em linguagem de investidor (fosso, margem, o que mata a tese), não jargão de código.
- 🔧 Yield + timeout em tool-calling loops longos.
- ✂️ Apagar Mission Control pages não-usadas (verificar quais panes têm zero visitas).

---

## 🧹 Parte IV — Cleanup list concreto

### Fase 1 — apagar lixo antigo (1-2h)
1. ✂️ `reports/deepdive/*` anteriores a 2026-05-08 (Phase LL closeout — single-source unreliable).
2. ✂️ `dossiers/<TK>_FILING_*.md` anteriores a 2026-05-08 (mesmo motivo).
3. ✂️ `dossiers/<TK>_IC_DEBATE.md` (deprecar; consolidar em `_COUNCIL.md`).
4. ✂️ `vault/_INDEX.md` órfão (image 7).
5. ✂️ Pastas vazias tipo `data/_` (image 8).
6. ✂️ Markdown files em `data_anomalies.json` etc — verificar se são lixo de runs antigas.

### Fase 2 — consolidar (2-3h)
7. 🔄 Renomear `vault/agents/<persona>/` para `vault/agents/<handle>/` (ex: `council.industrials-us/`) — manter `<persona>` como alias no front-matter.
8. 🔄 Consolidar IC_DEBATE → COUNCIL.
9. 🔄 Re-correr `council.story` sobre 33 holdings com pipeline current.
10. 🔄 Re-correr `ii deepdive --holdings` para refresh dossiers com pipeline Phase LL.
11. 🔄 `verdict_history`: marcar rows pre-Phase-KK como `data_source='legacy_single'`.

### Fase 3 — remover OpenClaw-era se não relevante (1h)
12. ❓ Investigar `perp.dreaming` — útil? Se não, remover.
13. ❓ Investigar `perp.daily-delight` — útil? Se não, remover.
14. ❓ Investigar `perp.content-quality`, `perp.token-economy`, `perp.library-signals` (todos frozen) — descongelar ou apagar.

### Fase 4 — promover ⭐ (3-5h)
15. 🌱 **Novo**: `research.auto-tag-clippings` — agent que observa `vault/Clippings/`, auto-tagga por sector/tema/ticker. Ollama 14B + `config/topic_watchlist.yaml`. **User explicit ask nesta sessão.**
16. 🌱 Wire `risk.devils-advocate` no pipeline Deepdive Strategist (reduzir AI slop).
17. 🌱 Wire `risk.thesis-health` no Historian do Deepdive.
18. 🌱 Linkar cada DOSSIE a 1 Knowledge Card da Bibliotheca.

### Fase 5 — alinhamento de linguagem (1-2h)
19. 🔄 Re-build `Knowledge Cards` com fontes pós-LL.
20. 🔄 Briefing matinal sempre em linguagem de investidor (Manual_de_Direcao).
21. 🔄 Tools no Antonio Carlos devolvem narrative investidor, não jargão de código.

### Fase 6 — fontes / fix pendente (1h)
22. ✅ `feedback_avoid_yfinance_us` — reordenar `config/sources_priority.yaml` (US: FMP + SEC primary; yfinance último).
23. ✅ Adicionar guard `WARN if yfinance_used_as_primary_for_us`.
24. ✅ Audit scripts: validar que cascade está a usar a ordem certa.

---

## 🗺️ Parte V — Plano de ataque (próximas sessões)

**Sessão A (esta? ou próxima)** — Fase 1 (limpeza visual + arquivos antigos).
**Sessão B** — Fase 2 (consolidação COUNCIL + renomes de pastas).
**Sessão C** — Fase 3 (OpenClaw-era audit + decisão).
**Sessão D** — Fase 4 (novo agent `research.auto-tag-clippings` + wires).
**Sessão E** — Fase 5+6 (linguagem de investidor + cascade US fix).

A ordem é deliberada: limpa primeiro, depois consolida, depois remove velho, depois adiciona novo.

---

## 🔗 Cross-references

- **Filosofia**: [[CONSTITUTION]] · [[CONSTITUTION_Pessoal]] · [[CONSTITUTION_Comercial]] · [[Bibliotheca/Disciplina_de_Investidor]]
- **Inventários**: [[AGENTS_REGISTRY]] · [[Agents Review]] · [[Sessions/Full_Inventory_2026-05-13]]
- **Linguagem**: [[Bibliotheca/Manual_de_Direcao]]
- **Roadmap master**: [[ROADMAP]]
- **Memory rules críticos**: [[feedback_inhouse_first]] · [[feedback_agent_function_names]] · [[feedback_avoid_yfinance_us]] · [[feedback_investor_language]] · [[feedback_dont_block_on_approval]]
- **Phase history**: ver topo de [[CONSTITUTION]] (Voltamos sintetizador) — Phase LL/KK/FF/EE-AOW/HH/II foram as últimas grandes.

---

## 📝 Notas finais

**Este doc é vivo**. Quando completas uma fase de cleanup, marca aqui ✅. Quando descobres um workflow que faltou, adiciona uma secção. O objectivo é **ter UMA referência única para "como o sistema opera hoje"** — não múltiplos docs fragmentados.

**Não fazer**:
- Não tentar overhaul tudo numa única sessão (~410 items na inventory).
- Não apagar coisas sem confirmar com `mega_auditor --bury` (reversível via cemetery).
- Não adicionar features antes de limpar — anti-padrão "build more on top of mess".

**Quando voltares depois de pausa**:
1. Lê [[CONSTITUTION]] (Voltamos sintetizador no topo).
2. Lê este Manual (parte III workflows + parte IV cleanup list).
3. Continua na próxima fase pendente da Parte V.
