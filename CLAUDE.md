# investment-intelligence

Sistema pessoal de inteligência de investimentos para um investidor pessoa física a operar em duas geografias: **Brasil (B3)** e **EUA (NYSE/NASDAQ)**. Estratégia de longo prazo: **DRIP** (reinvestimento de dividendos) com filosofia **Buffett / Graham** — qualidade, margem de segurança, dividendos consistentes.

## Filosofia

- O *universo* de empresas seguidas vive em `config/universe.yaml`. **Toda a edição de tickers é feita aí**, nunca em código Python.
- Dois mercados, duas bases de dados SQLite separadas: `data/br_investments.db` e `data/us_investments.db`. Schemas idênticos para permitir relatórios consolidados, mas o isolamento evita confusão de moeda, fuso e fontes.
- Fetchers são *independentes* e *idempotentes*. Cada fetcher sabe falar com **uma** fonte. O motor de scoring nunca chama a rede.
- O motor de scoring é único, mas aplica critérios ajustados por mercado (BR vs US — ver abaixo).

## Critérios de investimento

### Brasil (Graham clássico ajustado a juros locais)
- **Graham Number** ≤ 22.5  (`sqrt(22.5 × EPS × BVPS) ≥ preço`)
- **Dividend Yield** ≥ 6%
- **ROE** ≥ 15%
- **Dívida líquida / EBITDA** < 3×
- **Histórico de dividendos** ininterrupto ≥ 5 anos

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

## Convenções

- Datas em ISO 8601 (`YYYY-MM-DD`), UTC para timestamps de eventos.
- Moeda **nunca** convertida na DB — BRL na DB BR, USD na DB US. Conversão só na camada de relatório, se necessário.
- Logs estruturados (1 linha JSON por evento) em `logs/`. Rotacionar manualmente.
- Tickers BR sem sufixo `.SA` na DB; o fetcher acrescenta-o ao falar com APIs externas se preciso.
