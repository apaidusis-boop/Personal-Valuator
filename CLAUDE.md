# investment-intelligence

Sistema pessoal de inteligência de investimentos para um investidor pessoa física a operar em duas geografias: **Brasil (B3)** e **EUA (NYSE/NASDAQ)**. Estratégia de longo prazo: **DRIP** (reinvestimento de dividendos) com filosofia **Buffett / Graham** — qualidade, margem de segurança, dividendos consistentes.

## Filosofia

- O *universo* de empresas seguidas vive em `config/universe.yaml`. **Toda a edição de tickers é feita aí**, nunca em código Python.
- Dois mercados, duas bases de dados SQLite separadas: `data/br_investments.db` e `data/us_investments.db`. Schema idêntico para permitir relatórios consolidados, mas o isolamento evita confusão de moeda, fuso e fontes.
- Fetchers são *independentes* e *idempotentes*. Cada fetcher sabe falar com **uma** fonte. O motor de scoring nunca chama a rede.
- O motor de scoring é único, mas aplica critérios ajustados por mercado e tipo de ativo (BR stocks, BR FIIs, US stocks).
- Cache policy centralizada em `fetchers/cache_policy.py` — define TTLs por tipo de dado (preço passado = imutável, fundamental = 1 dia, etc.).

## Critérios de investimento

### Brasil — Acções (Graham clássico ajustado a juros locais)
- **Graham Number** ≤ 22.5  (`sqrt(22.5 × EPS × BVPS) ≥ preço`)
- **Dividend Yield** ≥ 6%
- **ROE** ≥ 15%
- **Dívida líquida / EBITDA** < 3× (n/a para holdings — `sector == 'Holding'`)
- **Histórico de dividendos** ininterrupto ≥ 5 anos

### Brasil — FIIs
- **DY 12 meses** ≥ 8%
- **P/VP** ≤ 1.05
- **Vacância física** < 15% (n/a para FIIs de papel/CRI)
- **Streak de distribuição** ≥ 12 meses consecutivos
- **Liquidez diária (ADTV)** > R$ 500k

### EUA (Buffett — qualidade sobre preço)
- **P/E** ≤ 20
- **P/B** ≤ 3
- **Dividend Yield** ≥ 2.5%
- **ROE** ≥ 15%
- **Dividend Aristocrat** *ou* mínimo 10 anos consecutivos de dividendos

### Veredictos do scoring
Cada critério devolve: `pass` / `fail` / `n/a`. Score = nº pass / nº aplicáveis. `passes_screen = True` sse todos os aplicáveis são `pass`.

## Valuation (Gordon DDM)

- `P = D0·(1+g) / (r−g)`, com cap duplo em g: `min(r − 0.04, cap_absoluto)`.
- r: BR=14% (SELIC+prémio), US=9% (10Y+prémio). Margem de segurança: 25%.
- Tese break: DY mínimo, ROE mínimo, corte de dividendos, quebra de streak.
- Output: `fair_value`, `entry_price`, `verdict` (BUY/HOLD/OVERVALUED).

## Fontes de dados

| Mercado | Fonte | Fetcher | Responsabilidade |
|---|---|---|---|
| BR | brapi.dev (token `.env`) | `brapi_fetcher.py` | EPS, P/E, cotação 3 meses |
| BR | Status Invest (scraping) | `statusinvest_scraper.py` | BVPS, ROE, DY, Dív/EBITDA, streak, P/B — fallback que completa brapi |
| BR | yfinance | `yfinance_fetcher.py` | Preços longos (10y), dividends_annual, DRE/BP/DFC anuais |
| BR | yfinance | `yf_br_fetcher.py` | Preços unadjusted + dividendos event-level (para total return) |
| BR FII | fiis.com.br | `fiis_fetcher.py` | Price, VPA, P/VP, DY 12m, rendimento, ADTV, segmento, streak |
| BR FII | Status Invest | `fii_statusinvest_scraper.py` | Fallback: avg rendimento 24m, P/VP, DY computado |
| BR macro | BCB SGS | `bcb_fetcher.py` | SELIC, CDI, IPCA, PTAX — tabela `series` |
| BR eventos | CVM IPE | `cvm_monitor.py` | Fatos relevantes + comunicados → tabela `events` |
| BR PDFs | CVM | `cvm_pdf_extractor.py` | Extrai full_text dos PDFs via pdfplumber |
| US | yfinance | `yfinance_fetcher.py` | Preços, dividends, statements (partilha o módulo com BR) |
| US eventos | SEC EDGAR | `sec_monitor.py` | 8-K, 10-K, 10-Q → tabela `events` |

**Nunca** commitar `.env`. O token brapi é pessoal e tem rate limit.

## Estrutura do projecto

```
investment-intelligence/
├── CLAUDE.md                    # este ficheiro
├── HANDOFF.md                   # notas de transição e plano do piloto ITSA4
├── config/
│   └── universe.yaml            # lista central de tickers (BR + US, holdings/watchlist/research_pool)
├── fetchers/
│   ├── brapi_fetcher.py         # B3 — fundamentals básicos (plano free)
│   ├── yfinance_fetcher.py      # BR+US — preços longos, dividendos anuais, statements
│   ├── yf_br_fetcher.py         # BR — preços unadjusted + dividendos event-level
│   ├── statusinvest_scraper.py  # fallback BR stocks — fundamentals detalhados
│   ├── fiis_fetcher.py          # BR FIIs — fiis.com.br + Status Invest fallback
│   ├── fii_statusinvest_scraper.py  # fallback BR FIIs
│   ├── bcb_fetcher.py           # séries macro BCB (SELIC, CDI, IPCA, PTAX)
│   └── cache_policy.py          # TTLs centralizados para todos os fetchers
├── scoring/
│   ├── engine.py                # scoring unificado (BR stocks, BR FIIs, US)
│   └── valuation.py             # Gordon DDM com tese break
├── analytics/
│   ├── loaders.py               # readers pandas (prices, dividends, series)
│   ├── total_return.py          # índice de retorno total com reinvestimento
│   └── compare.py               # comparativos multi-série (ticker vs macro)
├── monitors/
│   ├── cvm_monitor.py           # fatos relevantes CVM (lê cvm_name do yaml)
│   ├── cvm_pdf_extractor.py     # extrai texto de PDFs CVM via pdfplumber
│   └── sec_monitor.py           # 8-K / 10-K / 10-Q EDGAR (US)
├── scripts/
│   ├── init_db.py               # cria/migra ambas as DBs (idempotente)
│   ├── daily_update.py          # pipeline diário: BCB → yfinance → FIIs → streaks → scoring
│   ├── populate_br.py           # batch: yfinance → Status Invest → scoring → valuation
│   ├── weekly_report.py         # relatório consolidado BR + US (HTML dashboard)
│   ├── pilot_report.py          # deep-dive single ticker (HTML + Plotly)
│   ├── executive_report.py      # relatório de carteira multi-página (landscape PDF)
│   ├── compare_ibov.py          # ticker vs IBOV (via yfinance directo)
│   ├── compare_ticker_vs_macro.py  # ticker vs SELIC/CDI/IBOV (via DB)
│   ├── coverage_audit.py        # audit de NULLs e gaps por ticker
│   ├── seed_portfolio.py        # semeia portfolio_positions (equal-weight, Sprint 1)
│   └── recompute_fii_streaks.py # recalcula streak meses dos FIIs
├── data/
│   ├── br_investments.db        # SQLite — mercado BR
│   ├── us_investments.db        # SQLite — mercado US
│   └── cvm_pdfs/                # PDFs CVM descarregados
├── docs/references/             # PDFs research (Suno, XP, BTG) — uso pessoal
├── reports/                     # output HTML/MD/CSV dos reports
├── logs/                        # logs estruturados (1 linha JSON por evento)
└── tests/                       # unit tests (scoring, valuation, analytics)
```

## Schema SQLite (idêntico em ambas as DBs)

### Tabelas core
- **`companies`** — ticker, name, sector, is_holding (1=carteira, 0=watchlist), currency.
- **`prices`** — série diária: ticker, date, close, volume. PK `(ticker, date)`.
- **`fundamentals`** — snapshot: ticker, period_end, eps, bvps, roe, pe, pb, dy, net_debt_ebitda, dividend_streak_years, is_aristocrat.
- **`fii_fundamentals`** — FIIs: ticker, period_end, price, vpa, pvp, dy_12m, rendimento, vacância, ADTV, streak meses, segmento ANBIMA, source, fetched_at.
- **`dividends`** — eventos: ticker, ex_date, pay_date, amount, currency, kind (dividend/jcp/rendimento), source.
- **`dividends_annual`** — agregado: ticker, year, amount. Para DDM.
- **`scores`** — ticker, run_date, score, passes_screen, details_json.
- **`valuations`** — ticker, run_date, model, fair_value, entry_price, details_json.
- **`events`** — ticker, event_date, source (cvm/sec), kind, url, summary, full_text, pdf_path, classification_json.

### Tabelas de statements
- **`income_statements`** — DRE anual: ticker, period_end, revenue, gross_profit, ebit, ebitda, net_income.
- **`balance_sheets`** — BP anual: total_assets, current_assets, cash, liabilities, equity, etc.
- **`cash_flow_statements`** — DFC: operating/investing/financing cash flow, capex, FCF.

### Tabelas auxiliares
- **`series`** + **`series_meta`** — séries macro (SELIC, CDI, IPCA, IBOV, IFIX, USD/BRL).
- **`portfolio_positions`** — carteira: ticker, weight, entry_date, entry_price, active.

`scripts/init_db.py` aplica o schema a ambos os ficheiros.

## Comandos típicos

```bash
# Setup
python scripts/init_db.py                       # cria as DBs (idempotente)

# Pipeline diário
python scripts/daily_update.py                  # BCB + yfinance + FIIs + scoring
python scripts/daily_update.py --full           # mesmo com 5 anos de histórico

# Batch populate
python scripts/populate_br.py                   # stocks BR (yfinance + Status Invest + scoring + DDM)
python scripts/populate_br.py --fiis            # FIIs BR
python scripts/populate_br.py --all             # stocks + FIIs
python scripts/populate_br.py --only ITSA4 PRIO3  # subset

# Monitors
python monitors/cvm_monitor.py --all            # CVM para todos os tickers com cvm_name
python monitors/sec_monitor.py --all            # SEC EDGAR para tickers US

# Reports
python scripts/weekly_report.py                 # dashboard consolidado BR+US
python scripts/pilot_report.py ITSA4            # deep-dive single ticker
python scripts/executive_report.py              # relatório de carteira (landscape)

# Análise
python scripts/compare_ticker_vs_macro.py ITSA4 --months 6
python scripts/compare_ibov.py ITSA4 --period 10y

# Manutenção
python scripts/coverage_audit.py                # audit de gaps na DB
python scripts/coverage_audit.py --json         # output JSON
python scripts/recompute_fii_streaks.py         # recalcula streaks FIIs

# Testes
python -m unittest discover tests/ -v
```

## Convenções

- Datas em ISO 8601 (`YYYY-MM-DD`), UTC para timestamps de eventos.
- Moeda **nunca** convertida na DB — BRL na DB BR, USD na DB US. Conversão só na camada de relatório.
- Logs estruturados (1 linha JSON por evento) em `logs/`. Rotacionar manualmente.
- Tickers BR sem sufixo `.SA` na DB; o fetcher acrescenta-o ao falar com APIs externas.
- Fetchers devem usar `RuntimeError` (não `SystemExit`) para erros recuperáveis, de forma a não abortar callers em batch como `populate_br.py`.
- Scoring tem 3 estados: `pass` / `fail` / `n/a`. `n/a` é para dados em falta ou critérios inaplicáveis (holdings, FIIs de papel, etc.).
- `populate_br.py` apanha `(Exception, SystemExit)` para nunca abortar o batch num ticker problemático.
- `_fetch_dividends_resilient()` nos yf fetchers usa cascata de 3 estratégias para resiliência a versões do yfinance.
