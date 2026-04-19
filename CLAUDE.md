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
| Quantas ações tenho de X / posição actual     | `sqlite3 data/<mkt>_investments.db "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE ticker='X' AND active=1"` |
| Deep-dive em ticker X                         | `python scripts/analyze_ticker.py X` |
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
| **Comparar tickers** side-by-side             | `python scripts/compare_tickers.py JNJ PG KO [--vs SPY]` |
| **Quality drift** (screen a degradar/melhorar)| `python -m analytics.screen_trend [--market br\|us] [--ticker X]` |
| **Backtest yield strategy**                   | `python -m analytics.backtest_yield --market br --start 2019 --top-n 5` |
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
