# investment-intelligence

Sistema pessoal de inteligência de investimentos para um investidor pessoa física a operar em duas geografias: **Brasil (B3)** e **EUA (NYSE/NASDAQ)**. Estratégia de longo prazo: **DRIP** (reinvestimento de dividendos) com filosofia **Buffett / Graham** — qualidade, margem de segurança, dividendos consistentes.

## Filosofia

- O *universo* de empresas seguidas vive em `config/universe.yaml`. **Toda a edição de tickers é feita aí**, nunca em código Python.
- Dois mercados, duas bases de dados SQLite separadas: `data/br_investments.db` e `data/us_investments.db`. Schemas idênticos para permitir relatórios consolidados, mas o isolamento evita confusão de moeda, fuso e fontes.
- Fetchers são *independentes* e *idempotentes*. Cada fetcher sabe falar com **uma** fonte. O motor de scoring nunca chama a rede.
- O motor de scoring é único, mas aplica critérios ajustados por mercado (BR vs US — ver abaixo).

## Critérios de investimento

### Brasil — empresas não-financeiras (Graham clássico ajustado a juros locais)
- **Graham Number** ≤ 22.5  (`sqrt(22.5 × EPS × BVPS) ≥ preço`)
- **Dividend Yield** ≥ 6%
- **ROE** ≥ 15%
- **Dívida líquida / EBITDA** < 3×
- **Histórico de dividendos** ininterrupto ≥ 5 anos

### Brasil — bancos (sector == "Banks" em universe.yaml)
Bancos têm estrutura de capital e receita incomparáveis com empresas operacionais.
Graham Number e Dív. líq./EBITDA não se aplicam.
- **P/E** ≤ 10 (multiplos baixos típicos do sector)
- **P/B** ≤ 1.5 (margem de segurança sobre o equity)
- **Dividend Yield** ≥ 6%
- **ROE** ≥ 12% (relaxado vs 15% para refletir era Selic alta)
- **Histórico de dividendos** ≥ 5 anos

### EUA (Buffett — qualidade sobre preço)
- **P/E** ≤ 20
- **P/B** ≤ 3
- **Dividend Yield** ≥ 2.5%
- **ROE** ≥ 15%
- **Dividend Aristocrat** *ou* mínimo 10 anos consecutivos de dividendos

### EUA — bancos (sector == "Banks", market == us)
Bancos US têm dinâmica diferente dos bancos BR e das empresas operacionais.
ROTCE > ROE como métrica primária (intangíveis grandes pós-aquisições);
P/TBV é a referência de avaliação; CET1 substitui Basel ratio; o streak
pós-GFC é o que conta (vários cortaram em 2009 — JPM, BAC, WFC, C).

- **P/E** ≤ 12 (mid-cycle típico de top-tier US bank, mais conservador que Buffett genérico)
- **P/TBV** ≤ 1.8 (Tangible Book; P/B simples sobrestima banco com goodwill)
- **ROTCE** ≥ 15% (Return on Tangible Common Equity; ROE ≥ 12% é fallback se ROTCE indisponível)
- **Dividend Yield** ≥ 2.5%
- **CET1 ratio** ≥ 11% (Basel III mínimo regulatório + buffer)
- **Efficiency ratio** ≤ 60% (cost-to-income; lower is better)
- **Dividend streak pós-2009** ≥ 10 anos (GFC reset clock — Aristocrat strict não aplica a maioria dos bancos)

Engine: `scoring/engine.py::score_us_bank` (paralelo a `score_br_bank`).
Playbook narrativo: `obsidian_vault/wiki/sectors/US_Banks.md`.
Method YAML: `library/methods/us_buffett_bank_screen.yaml`.

## Fontes de dados

| Mercado | Fonte primária | Fallback | Notas |
|---|---|---|---|
| BR | [brapi.dev](https://brapi.dev) (token em `.env` como `BRAPI_TOKEN`) | scraping Status Invest | CVM API pública para fatos relevantes |
| US | `yfinance` (sem auth) | — | SEC EDGAR para 8-K / 10-K / dividend declarations |

**Nunca** commitar `.env`. O token brapi é pessoal e tem rate limit.

## Estrutura do projecto

```
investment-intelligence/
├── CLAUDE.md                    # este ficheiro
├── config/
│   └── universe.yaml            # lista central de tickers (BR + US + watchlists)
├── fetchers/
│   ├── brapi_fetcher.py         # B3 — fundamentals + cotações
│   ├── yfinance_fetcher.py      # NYSE/NASDAQ — fundamentals + cotações
│   └── statusinvest_scraper.py  # fallback BR para dividend history
├── scoring/
│   └── engine.py                # scoring unificado, critérios por mercado
├── monitors/
│   ├── cvm_monitor.py           # fatos relevantes CVM (BR)
│   └── sec_monitor.py           # 8-K / 10-K / div EDGAR (US)
├── scripts/
│   ├── daily_update.py          # cron diário — preços + scores
│   ├── weekly_report.py         # relatório consolidado BR + US
│   └── init_db.py               # cria/migra ambas as DBs
├── data/
│   ├── br_investments.db        # SQLite — mercado BR
│   └── us_investments.db        # SQLite — mercado US
├── reports/                     # output markdown/HTML do weekly_report
├── logs/                        # logs estruturados dos fetchers e monitors
└── tests/
```

## Schema SQLite (idêntico em ambas as DBs)

- **`companies`** — uma linha por ticker. `ticker`, `name`, `sector`, `is_holding` (1 = na carteira, 0 = watchlist), `currency`.
- **`prices`** — série temporal diária. `ticker`, `date`, `close`, `volume`. PK `(ticker, date)`.
- **`fundamentals`** — snapshot trimestral. `ticker`, `period_end`, `eps`, `bvps`, `roe`, `pe`, `pb`, `dy`, `net_debt_ebitda`, `dividend_streak_years`, `is_aristocrat`. PK `(ticker, period_end)`.
- **`scores`** — output do motor de scoring, uma linha por (ticker, run). `ticker`, `run_date`, `score`, `passes_screen` (bool), `details_json`.
- **`events`** — fatos relevantes/filings. `ticker`, `event_date`, `source` (`cvm`/`sec`), `kind` (`8-K`, `10-K`, `dividend`, `fato_relevante`...), `url`, `summary`.

`scripts/init_db.py` aplica o schema a ambos os ficheiros.

## Comandos típicos

```bash
python scripts/init_db.py                # cria as DBs (idempotente)
python scripts/daily_update.py           # corre fetchers + scoring para BR e US
python scripts/weekly_report.py          # gera reports/weekly_YYYY-MM-DD.md
```

## Script catalog — consultar ANTES de criar novo

**Política anti-queima-tokens**: antes de escrever um script novo para responder
uma pergunta, verificar se já existe um que resolve (ou que possa ser estendido
com uma flag). Reescrever do zero queima tokens e duplica lógica de derivação
de assumptions que tem subtilezas (damper, Gordon, quality flag, etc.).

| Pergunta                                      | Comando existente |
|---|---|
| **Mega Helena** (design audit + skill curate + 4-path spikes) | `python agents/helena_mega.py [audit\|curate\|spike\|report\|all] [--dry-run]` — outputs em `obsidian_vault/skills/Helena_Mega/` |
| **Helena audit** (design system linter, DS001-DS009) | `python -m agents.helena.audit` |
| **Helena Linha scout** (weekly, GitHub+RSS+YouTube) | `python scripts/design_research.py [--source github\|blogs\|youtube\|all]` |
| **Panorama completo de ticker** (super-command) | `ii panorama X [--write]` — agrega verdict+peers+triggers+notes+videos+analyst |
| **Perpetuum Master** (Phase X — 3 perpetuums) | `python agents/perpetuum_master.py [--only NAME] [--dry-run]` — thesis + vault + data_coverage, 442 subjects/dia |
| **Perpetuum individual** | `python agents/perpetuum_master.py --only {thesis\|vault\|data_coverage\|bibliotheca\|...}` |
| **Bibliotheca autofix** (sector + name backfill) | `python scripts/bibliotheca_autofix.py [--apply]` — universe.yaml → companies; idempotente |
| **Perpetuum review** (T2 actions open) | `python scripts/perpetuum_action_run.py list-open` |
| **Perpetuum run action** (whitelisted) | `python scripts/perpetuum_action_run.py <id> [--market br\|us]` |
| **Library ingest books** (PDF→chunks) | `python -m library.ingest` (processa library/books/) |
| **Library extract methods** (Ollama) | `python -m library.extract_insights --book <slug> --max 40` |
| **Library matcher** (methods vs portfolio) | `python -m library.matcher [--method X] [--dry-run]` |
| **Library RAG build** (nomic-embed local) | `python -m library.rag build` |
| **Library RAG query** (semantic search) | `python -m library.rag query "texto" --k 5` |
| **Library RAG ask** (RAG + Qwen synth) | `python -m library.rag ask "pergunta PT" --k 6` |
| **Paper trade signals** | `sqlite3 data/us_investments.db 'SELECT * FROM paper_trade_signals WHERE status="open"'` |
| **Enrich fundamentals** (market_cap, cur_ratio, ltd, wc) | `python scripts/enrich_fundamentals_for_methods.py [--schema\|--backfill\|--ticker X]` |
| **Ad Perpetuum Validator** (legacy, Phase W.5) | `python -c "from agents.perpetuum_validator import PerpetuumValidator; ..."` — thesis_health daily (agora wrappado em perpetuum.thesis) |
| **Metrics baseline freeze** (Phase W before) | `python scripts/metrics_baseline.py --freeze` — uma vez |
| **Metrics daily report** (tracking contínuo) | `python scripts/metrics_report.py --compare` — delta vs baseline |
| **Phase W Roadmap** | `obsidian_vault/skills/Roadmap.md` — 11 sprints W.1–W.11 |
| **Skills arsenal index** | `obsidian_vault/skills/_MOC.md` — 33 skills avaliadas + Gold extras |
| **Ingest relatórios subscriptions** (Suno/XP/WSJ) | `ii subs fetch --source all && ii subs extract` |
| **Views de analistas sobre ticker**           | `ii subs query X --days 90` |
| Quantas ações tenho de X / posição actual     | `sqlite3 data/<mkt>_investments.db "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE ticker='X' AND active=1"` |
| Deep-dive em ticker X                         | `python scripts/analyze_ticker.py X` |
| **Research memo unificado** (Phase J, PT/EN)  | `python scripts/research.py X [--md]` |
| **Batch research scan** (todas holdings, BR+US) | `python scripts/research.py --holdings [--md]` |
| **Payback DRIP de X** (quantos anos p/ 2× shares, cash payback) | `python scripts/drip_projection.py --ticker X --payback` |
| Projecção DRIP 5/10/15y single-ticker         | `python scripts/drip_projection.py --ticker X` |
| Projecção DRIP agregada da carteira           | `python scripts/drip_projection.py --horizons 5,10,15,20` |
| Briefing consolidado BR+US+RF                 | `python scripts/portfolio_report.py` |
| Comparar ticker vs IBOV                       | `python scripts/compare_ibov.py X` |
| Comparar ticker vs macro (Selic/CDI/USD)      | `python scripts/compare_ticker_vs_macro.py X` |
| Tese qualitativa (macro / sector / ticker)    | `python scripts/thesis_manager.py X` |
| Ranking DRIP quality BR                       | `python scripts/br_drip_optimizer.py` |
| Trigger engine (buy/sell signals declarativos)| `python scripts/trigger_monitor.py [--dry-run] [--market br\|us]` |
| **Gerir open triggers** (list/resolve/ignore) | `python scripts/action_cli.py [list\|resolve\|ignore\|note] [ref] [--note '...']` |
| **Dividend safety score** (0-100, forward)    | `python -m scoring.dividend_safety X` ou `--all` |
| **Altman Z-Score** (distress, veto R5)        | `python -m scoring.altman X` |
| **Piotroski F-Score** (quality 0-9, veto F≤3) | `python -m scoring.piotroski X` |
| **Fetch deep fundamentals** (yfinance)        | `python fetchers/yf_deep_fundamentals.py X` ou `--holdings` |
| **Comparar tickers** side-by-side             | `python scripts/compare_tickers.py JNJ PG KO [--vs SPY]` |
| **Quality drift** (screen a degradar/melhorar)| `python -m analytics.screen_trend [--market br\|us] [--ticker X]` |
| **Backtest yield strategy**                   | `python -m analytics.backtest_yield --market br --start 2019 --top-n 5 [--quality-only]` |
| **Backtest regime overlay** (Phase H, null)   | `python -m analytics.backtest_regime --market us --start 2013 --min-history-years 1` |
| **Regime macro classifier** (BR + US)         | `python -m analytics.regime [--market br\|us] [--as-of YYYY-MM-DD]` |
| **Atualizar FRED macro (US)**                 | `python fetchers/fred_fetcher.py [--series DGS10]` |
| **YouTube ingest** 1 vídeo (cache-first)      | `python scripts/yt_ingest.py <url>` |
| **YouTube batch** (lista/canal)               | `python scripts/yt_ingest_batch.py --channel-last <id> --count N` |
| **YouTube re-extract** (só Ollama, 0 rede)    | `python scripts/yt_reextract.py --all` ou `--video X` |
| **YouTube digest** (SQL-only, 0 LLM)          | `python scripts/yt_digest.py --channel "X" --days 30` |
| **Refresh preço intraday** (yfinance live)    | `python scripts/refresh_ticker.py X` ou `--all-holdings` |
| **Notes por ticker** (tese, observações)      | `python scripts/notes_cli.py add X "texto" --tags a,b` |
| **Obsidian vault export**                     | `python scripts/obsidian_bridge.py [--refresh] [--holdings-only]` |
| **Research memo com preço live**              | `python scripts/research.py X --intraday` |
| **Verdict engine** (BUY/HOLD/SELL aggregado)  | `ii verdict ACN [--narrate] [--write]` |
| **Streamlit dashboard** (localhost:8501)      | `ii dashboard` |
| **Agent matinal** (cron 09:30)                | `ii agent [--quick] [--dry-run]` |
| **Snapshot MV diário**                        | `ii snapshot [--backfill 90]` |
| **Earnings react** (refetch on new filing)    | `ii react [--dry-run]` |
| **Telegram push**                             | `ii telegram --setup`  depois  `ii telegram "msg"` |
| **Peer compare** (percentil vs sector)        | `ii peers ACN [--write]` |
| **Rebalance assistant**                       | `ii rebalance [--cash-add 5000] [--md]` |
| **Position size Kelly-lite**                  | `ii size ACN --cash 10000 [--force]` |
| **Verdict history + backtest**                | `ii vh record` (daily) / `ii vh backtest` / `ii vh show ACN` |
| **Earnings surprise** (YT targets vs real)    | `ii surprise [--ticker X] [--md]` |
| **News fetch + classify**                     | `ii news [--classify]` / `ii news --digest --days 7` |
| **Morning briefing consolidado**              | `python scripts/morning_briefing.py` ou `ii brief` (legacy) |
| **Daily diff** (o que mudou vs ontem)         | `python scripts/daily_diff.py --since 1` |
| **Vault semantic ask** (Qwen 14B sobre vault) | `ii vault "pergunta em PT"` |
| **Earnings calendar** (yfinance)              | `python fetchers/earnings_calendar.py --holdings` + `--upcoming 30` |
| **FX total BR+US em BRL**                     | `ii fx --total` |
| **Backtest triggers históricos**              | `python -m analytics.backtest_triggers --market us --start 2020 --kind price_drop --threshold -20` |
| **Memory cleanup** (stale/broken/orphan)      | `python scripts/memory_cleanup.py [--fix]` |
| **CLI unificada (tudo)**                      | `ii help` |
| Importar nova carteira (XP/JPM)               | `python scripts/import_portfolio.py --br <x.xlsx> --us <y.csv>` |
| Scoring ad-hoc                                | `python scoring/engine.py X [--market br\|us]` |

**Regras de extensão**:
1. Se existe o script mas falta um ângulo (ex: single-ticker, formato payback),
   **adicionar flag/modo** em vez de criar script novo.
2. Scripts one-shot específicos de um ticker (ex: `itsa4_drip_scenario.py`) são
   anti-padrão — generalizar e apagar o one-shot.
3. Toda a lógica de *derivação de assumptions* (damper, Gordon, classify
   equity/fii/compounder) vive em `scripts/drip_projection.py::derive_scenarios`
   e é reutilizada. NÃO reimplementar à mão.

## Convenções

- Datas em ISO 8601 (`YYYY-MM-DD`) na DB e nos logs (machine-readable).
  Na camada de apresentação ao utilizador, **dd/mm/yyyy** via helpers
  `analytics.format.br_date(iso)` / `br_datetime(iso)`.
- Moeda **nunca** convertida na DB — BRL na DB BR, USD na DB US. Conversão só na camada de relatório, se necessário.
- Logs estruturados (1 linha JSON por evento) em `logs/`. Rotacionar manualmente.
- Tickers BR sem sufixo `.SA` na DB; o fetcher acrescenta-o ao falar com APIs externas se preciso.
