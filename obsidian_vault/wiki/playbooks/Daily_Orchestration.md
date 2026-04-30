---
type: playbook
name: Daily Orchestration — cron 23:30 sequence
tags: [playbook, orchestration, cron, daily]
related: ["[[Perpetuum_Engine]]", "[[Telegram_setup]]", "[[Token_discipline]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🕰️ Daily Orchestration — uma corrida, três camadas

> Tudo o que acontece **automaticamente** no projecto às **23:30 local** corre por uma única entrada: `scripts/daily_run.bat`. Este playbook é o mapa: que step, em que ordem, o que produz, e o que falha quando algo está em sleep.

## Princípio

**Uma cron, três camadas, zero tokens Claude.**
1. **Data refresh** (fetchers + scoring + conviction) — fonte primária da DB.
2. **Decision close** (paper trade + predictions) — fecha o ciclo de cada call.
3. **Reporting + self-improvement** (digest, telegram, perpetuums) — gera o briefing matinal e mexe-se a si mesmo.

Cumpre [[Token_discipline]] (REGRA #1): tudo Ollama + SQL + scripts locais. Claude nunca é chamado durante o cron.

## Cron entry

| Item | Valor |
|---|---|
| Task name | `investment-intelligence-daily` |
| Schedule | Daily, **23:30 local** |
| Action | `C:\Users\paidu\investment-intelligence\scripts\daily_run.bat` |
| Install | `scripts/_schtasks_install.bat` (idempotente, `/F` reescreve) |
| Verify | `scripts/_schtasks_verify.bat` (`schtasks /Query`) |
| Remove | `schtasks /Delete /TN "investment-intelligence-daily" /F` |
| Log | `logs/daily_run_YYYY-MM-DD.log` (rotativo) |

> ⚠️ **REGRA SAGRADA**: o PC tem de estar **acordado** às 23:30. Sleep/hibernate = cron skip silencioso. Em `Power Options` → desligar sleep antes das 23:30 ou colocar wake timer. Se o PC dorme à noite, mover schedule para horário em que está aberto.

## Sequência completa (ordem actual)

`daily_run.bat` corre 19 steps em série. Cada step append ao mesmo log diário, captura `errorlevel` e **não aborta** se falhar — colecciona e prossegue.

### Camada 1 — Data refresh (BR + US)

| # | Step | Comando | Produz | Runtime | Falha-modo |
|---|---|---|---|---|---|
| 1 | `[BR]` | `python scripts/daily_update.py` | `prices`, `dividends`, `fundamentals`, `scores` (BR DB) | ~3-6min | brapi rate-limit, yfinance 429 → ticker individual marca BAD, prossegue |
| 2 | `[CVM]` | `python monitors/cvm_monitor.py` | `events` (BR fatos relevantes) | ~30-90s | CVM scrape flaky → exit ≠0 mas não bloqueia |
| 3 | `[CVM-PDF]` | `python monitors/cvm_pdf_extractor.py --limit 20` | PDFs CVM RAD parsed | ~1-3min | RAD frequentemente em 503 → exit code **ignorado** by design |
| 4 | `[US]` | `python scripts/daily_update_us.py` | `prices`, `dividends`, `fundamentals`, `scores` (US DB) | ~5-10min | yfinance throttle, SEC EDGAR rate-limit |
| 5 | `[SEC]` | `python monitors/sec_monitor.py --lookback-days 30` | `events` (US 8-K/10-K/divs) | ~1-2min | SEC EDGAR 429 (User-Agent obrigatório) |

**Step 1 (BR)** corre 5 sub-steps internos (ver docstring `daily_update.py`):
   1. BCB SGS macro (SELIC/CDI/IPCA/PTAX, 30d window)
   2. yfinance BR (preços + dividendos para holdings + watchlist + `br_dividend_compounders.yaml`)
   3. fiis.com.br + Status Invest fallback (FII fundamentals)
   4. `recompute_fii_streaks` (recalcula streaks do dividend history)
   5. scoring BR (`scoring/engine.py` aplicado a todo o universe)

**Step 4 (US)** corre 3 sub-steps:
   1. `yf_us_fetcher` para `us.holdings + us.watchlist + kings_aristocrats.yaml`
   2. SEC EDGAR cross-validation do streak + flag `is_aristocrat`
   3. scoring US (critérios Buffett — `score_us` / `score_us_bank`)

### Camada 2 — Decision close

| # | Step | Comando | Produz | Runtime | Falha-modo |
|---|---|---|---|---|---|
| 11 | `[PAPER-CLOSE]` | `python scripts/paper_trade_close.py` | Fecha `paper_trade_signals` expirados (30/90/365d) | ~10-30s | DB lock se outro processo a escrever; idempotent retry OK |
| 12 | `[PRED-EVAL]` | `python scripts/predictions_evaluate.py` | Closes `predictions` (analyst + YouTube channel calls) com outcome correct/wrong/partial | ~5-15s | Sem preço hoje → mantém pending |

**Por que ordem 11 → 12 importa**: ambos lêem `prices` actualizadas pelo step 1/4. Sem data refresh primeiro, fechariam com preço stale.

### Camada 3 — Reporting + self-improvement

| # | Step | Comando | Produz | Runtime | Falha-modo |
|---|---|---|---|---|---|
| 6 | `[REPORT-US]` | `python scripts/us_portfolio_report.py` | `reports/us_briefing_<DATE>.md` | ~5s | DB read-only |
| 7 | `[WEEKLY]` | `python scripts/weekly_report.py --days 7` | `reports/weekly_<DATE>.md` | ~10s | (corre todo o dia, mesmo conteúdo) |
| 8 | `[BRIEFING]` | `python scripts/portfolio_report.py --md` | Briefing consolidado BR+US+RF | ~5s | — |
| 9 | `[TRIGGERS]` | `python scripts/trigger_monitor.py` | Open triggers (buy/sell signals declarativos) | ~30s | — |
| 10 | `[PERPETUUM]` | `python agents/perpetuum_master.py` | `perpetuum_health` + `perpetuum_run_log` (12 perpetuums) | ~5-15min | Ollama down → perpetuums LLM-dependentes (autoresearch, librarian) marcam errors mas seguem |
| 13 | `[CLIPPINGS-INGEST]` | `python -m library.clippings_ingest --rag-build` | Novos clippings → `chunks_index.db` + RAG rebuild | ~1-5min | Nomic embed model fail |
| 14 | `[GLOSSARY]` | `python scripts/build_glossary.py --backlinks --quiet` | Glossary 29 entries idempotent rebuild | ~10s | — |
| 15 | `[TUTOR]` | `python scripts/dossier_tutor.py --quiet` | Re-injecta tutor sections em ~72 dossiers | ~30-60s | — |
| 16 | `[KNOWLEDGE-CARDS]` | `python scripts/build_knowledge_cards.py --quiet` | Skip-existing, only new | ~30s | — |
| 17 | `[RESEARCH-DIGEST]` | `python scripts/research_digest.py --quiet` | `Bibliotheca/Research_Digest_<DATE>.md` | ~10s | — |
| 18 | `[TELEGRAM-BRIEF]` | `python scripts/captains_log_telegram.py --silent` | Push Telegram (~1160 chars) | ~5s | Telegram bot offline / network down → silently skips |
| 19 | `[NOTIFY]` | `python scripts/notify_events.py --hours 48` | Notify_state.json delta push | ~5s | — |
| 20 | `[CSV]` | `python scripts/export_macro_csv.py` | `data/macro_exports/*.csv` | ~5s | — |
| 21 | `[ROTATE]` | `python scripts/rotate_logs.py --days 30` | Apaga logs > 30d | ~1s | — |

### Domingo — extra step

```
[WEEKLY-SUNDAY] python scripts/design_research.py
```
Helena Linha continuous scout (GitHub + RSS + YouTube design sources). Só corre quando `(Get-Date).DayOfWeek.value__ == 0`.

> ✓ Confirmado: perpetuum_master corre **antes** de research_digest e telegram-brief no `daily_run.bat`. Alerts BIB001-004 + autoresearch findings deste run aparecem no digest e push de hoje.

## Os 12 perpetuums (step 10)

`perpetuum_master.py` itera o registry em `agents/perpetuum/`. Cada perpetuum tem `name`, `description`, `enabled`, `tier (T1-T5)`. Detalhe arquitectural em [[Perpetuum_Engine]].

Ordem de execução determinística (registry-order):
1. `thesis` — thesis_health daily (Phase W.5)
2. `vault` — frontmatter drift + missing wiki notes
3. `data_coverage` — DB completeness checks
4. `content_quality` — Bibliotheca clippings quality (T2)
5. `methods` — library/methods/*.yaml health
6. `tokens` — Tavily quota / Ollama uptime (T2)
7. `library` — chunks_index integrity
8. `meta` — perpetuum-of-perpetuums (errors aggregator)
9. `ri_freshness` — quarterly_history staleness (Phase Y)
10. `code_health` — codebase anti-patterns CH001-CH004 (Phase BB, T1)
11. `bibliotheca` — librarian quality BIB001-004 (Phase DD, T1)
12. `autoresearch` — Tavily web research top-30 conviction (Phase K, T1)

Frozen perpetuums (`enabled=False`) são puladas com mensagem `FROZEN`. Promoção T1→T2+ é decisão humana (Constitution decision log).

## Manual triggers (re-run individual)

| Caso | Comando |
|---|---|
| Re-run pipeline inteiro (force, fora do cron) | `scripts\daily_run.bat` |
| Só BR refresh | `python scripts/daily_update.py` |
| Só US refresh | `python scripts/daily_update_us.py` |
| Só fetcher yf | `python scripts/daily_update.py --only yf` |
| Salta FIIs | `python scripts/daily_update.py --skip-fii` |
| Histórico 5y completo | `python scripts/daily_update_us.py --full` |
| Salta SEC | `python scripts/daily_update_us.py --skip-sec` |
| Só fechar paper trades (dry-run) | `python scripts/paper_trade_close.py --dry-run` |
| Só evaluar predictions | `python scripts/predictions_evaluate.py --report-only` |
| Só perpetuum vault | `python agents/perpetuum_master.py --only vault` |
| Perpetuum dry-run (no DB writes) | `python agents/perpetuum_master.py --dry-run` |
| Só Telegram brief (preview) | `python scripts/captains_log_telegram.py --dry-run` |
| Só research digest 7d | `python scripts/research_digest.py --days 7` |
| Verificar cron registado | `scripts\_schtasks_verify.bat` |

## Failure modes — diagnóstico rápido

| Sintoma | Causa provável | Fix |
|---|---|---|
| Log do dia não existe em `logs/daily_run_<DATE>.log` | PC em sleep/hibernate às 23:30 | Wake timer + power plan ajustado; ou re-run manual `daily_run.bat` |
| `BR exit code: 1` no log mas seguiu | brapi rate-limit ou yfinance 429 | Tickers individuais marcam BAD; benigno se 1-2; investigar se 5+ |
| `PERPETUUM` step muito rápido (<1s) | Ollama down → todos LLM-perps falham fast | `ollama list` para checar; daemon `ollama serve` |
| `TELEGRAM-BRIEF exit code: 0` mas não recebi push | `.env` `TELEGRAM_TOKEN`/`CHAT_ID` errado | `python -m notifiers.telegram --setup`; ver [[Telegram_setup]] |
| `[CVM-PDF]` exit ≠0 todos os dias | CVM RAD em 503 (sistema deles) | **Ignorado by design** — extractor é best-effort |
| Tavily quota exhausted (autoresearch perp errors) | 100/dia ou 50/hora budget gasto | Reset 24h; cache 7d evita re-spend; ver [[Tavily_Integration]] |
| `[CLIPPINGS-INGEST]` muito lento (>10min) | nomic-embed model não cached / disco lento | Pre-pull com `ollama pull nomic-embed-text` |
| DB locked errors em vários steps | Streamlit dashboard aberto a escrever, ou outro `daily_run.bat` em paralelo | Fechar dashboard, esperar; só **uma** instance do cron por dia |
| Logs a crescer sem limite | rotate_logs.py falhou ou não correu | Run manual `python scripts/rotate_logs.py --days 30` |

## Token economics

| Step | Custo Claude | Custo Ollama | Custo rede |
|---|---|---|---|
| Data refresh (1-5) | **0** | 0 | yfinance + brapi + BCB + SEC EDGAR (free APIs) |
| Decision close (11-12) | **0** | 0 | 0 (lê DB) |
| Reporting (6-9, 17-21) | **0** | 0 | 0 |
| Perpetuum (10) | **0** | ~5-10min Qwen 14B (autoresearch + thesis quality + librarian) | Tavily (gating: top 30 conviction, cooldown 6d, cache 7d) |
| Clippings ingest (13) | **0** | nomic-embed (per chunk, fast) | 0 |

**Total Claude tokens por dia: 0.** Toda a cadeia roda em compute local + DB. Claude (eu) só é chamado quando user faz pergunta interactiva — **fora** do cron.

## Logs — onde cada step escreve

Top-level log: `logs/daily_run_YYYY-MM-DD.log` (catch-all stdout+stderr de cada step).

Logs estruturados por fetcher (1 linha JSON por evento), append-only:
- `logs/yf_br_fetcher.log`
- `logs/yf_us_fetcher.log`
- `logs/yf_deep_fundamentals.log`
- `logs/bcb_fetcher.log`
- `logs/fiis_fetcher.log`
- `logs/sec_edgar_fetcher.log`
- `logs/cvm_monitor.log`
- `logs/cvm_pdf_extractor.log`
- `logs/sec_monitor.log`
- `logs/yt_ingest.log` (não no cron, mas mesma rotação)

Rotação: `rotate_logs.py --days 30` (step 21) apaga `.log` files > 30d. Não compacta — apaga.

## Ordem mental de leitura ao acordar

Quando user volta de manhã, **ordem natural**:
1. **Telegram push** (recebido durante a noite) — pulse 1-line.
2. `obsidian_vault/Bibliotheca/Research_Digest_<DATE>.md` — o que aconteceu nas últimas 24h.
3. `reports/weekly_<DATE>.md` ou `portfolio_report.md` — briefing carteira.
4. Streamlit dashboard (`ii dashboard`) — Captain's Log page primeiro.
5. Se algo cheirar mal → `logs/daily_run_<DATE>.log` (raw).

## Ver também

- [[Perpetuum_Engine]] — anatomia dos 12 perpetuums (step 10)
- [[Telegram_setup]] — configuração do bot Jarbas (step 18)
- [[Token_discipline]] — porque tudo é local
- [[Bibliotheca_v2]] — o que research_digest agrega (step 17)
- [[Library_Pipeline]] — clippings ingest detail (step 13)
- [[Tavily_Integration]] — autoresearch perpetuum (step 10 sub-12)
- [[RI_Knowledge_Base]] — ri_freshness perpetuum (step 10 sub-9)
