# Catálogo de APIs US

Compilado a partir de `vendor/skill-financial-analyst/scripts/api_config.py`
e investigação em Abr 2026. Todas as APIs cobrem o mercado US; nenhuma cobre
BR (B3/CVM/brapi continuam a ser tratados pelo stack BR existente).

## Sem necessidade de chave (arranque imediato)

| Fonte | O que dá | Limite | Notas |
|---|---|---|---|
| **yfinance** | Preços diários, dividendos, splits, fundamentals básicos (info dict), earnings | Sem rate limit oficial, ~2 req/s seguro | Já usado no BR. Para US funciona igualmente bem. |
| **SEC EDGAR** | 10-K/10-Q/8-K filings, Form 4 (insider), Company Facts JSON (fundamentals autoritativos), full-text search | 10 req/s com User-Agent identificando app | **Ground truth US.** Usar para dividend streak (Form 10-K Cash Flow Statements) em vez de confiar só em yfinance. |
| **ApeWisdom** | Trends Reddit por ticker (232+ subreddits, incl. r/wallstreetbets, r/stocks, r/investing) | Público, ~1 req/s | Sinal de sentimento social barulhento mas acionável para detectar hype. |
| **StockTwits** | Bullish/bearish ratio, volume de messages por ticker | Público | Rápido proxy de sentimento retail. |
| **RSS feeds** (~20) | Seeking Alpha, CNBC, MarketWatch, Nasdaq, Benzinga, Yahoo Finance, Reuters, Bloomberg selectos | Sem limite real | Ver lista completa em `vendor/skill-financial-analyst/scripts/rss_feeds.py`. |
| **TradingView** (via `tradingview-ta` pip) | Consenso 26 indicadores técnicos por ticker (Strong Buy → Strong Sell) | Sem chave | Útil para overlay técnico, não compete com fundamentals Buffett. |

## Free tier com registo (chave gratuita)

| Fonte | O que dá | Free tier | URL de registo |
|---|---|---|---|
| **Finnhub** | Analyst ratings, price targets, earnings calendar, insider transactions, news por ticker | 60 req/min | https://finnhub.io |
| **Financial Modeling Prep (FMP)** | Fundamentals completos, DCF, key metrics, historical financials | 250 req/dia | https://financialmodelingprep.com |
| **Alpha Vantage** | Time series, fundamentals, news sentiment, indicadores técnicos server-side | 25 req/dia (apertado) | https://alphavantage.co |
| **Polygon.io** | Preços intraday, options, snapshots | Free tier limitado (~5 req/min) | https://polygon.io |
| **Mboum Finance** (via RapidAPI) | Congress trades, insider, analyst data agregados | Free tier via RapidAPI | https://rapidapi.com |

## Pagas (avaliar só se necessário)

| Fonte | O que dá | Custo |
|---|---|---|
| **Seeking Alpha RapidAPI** | Quant ratings + factor grades (valuation, growth, profitability, momentum, revisions) | Subscrição paga via RapidAPI |
| **Quiver Quant** | Congress trades detalhados, lobbying, patents | Tier pago |

## Fallback chains recomendadas (do `api_config.py` deles)

Quando se constroem fetchers US, a ordem de preferência deve ser:

| Categoria | Primary → ... → último recurso |
|---|---|
| **Preços** | yfinance → Polygon → Alpha Vantage → FMP |
| **Fundamentals** | yfinance + SEC EDGAR (canónico) → Finnhub → FMP |
| **Analyst ratings** | Finnhub → yfinance → Seeking Alpha → Mboum → FMP |
| **Insider trades** | SEC EDGAR Form 4 → Finnhub → Mboum → yfinance |
| **News** | Finnhub → Alpha Vantage → RSS feeds |
| **Congress trades** | Mboum → Quiver (pago) |

A implementação deles do pattern está em
`vendor/skill-financial-analyst/scripts/api_caller.py` (117 linhas) — ver
[`patterns_to_port.md`](patterns_to_port.md).

## Mínimo viável para arranque US

Para o screen Buffett (`scoring/engine.py score_us`), o que preciso:
- **Preço actual** — yfinance
- **EPS, P/E** — yfinance
- **P/B, ROE** — yfinance (via `.info`) ou SEC EDGAR CompanyFacts
- **Dividend yield** — yfinance
- **Dividend streak** — SEC EDGAR Form 10-K (autoritativo) ou yfinance histórico
- **Aristocrat flag** — manter lista manual no `config/universe.yaml` (S&P 500
  Dividend Aristocrats é uma lista pública conhecida)

**Tradução prática:** yfinance + SEC EDGAR cobrem 90% do screen Buffett **sem
nenhuma chave API**. Isso é o MVP para US.

## Sectores US (para futuro `sector_rotation.py`)

ETFs SPDR setoriais como proxies de rotação sectorial:

| ETF | Sector |
|---|---|
| XLK | Technology |
| XLF | Financials |
| XLE | Energy |
| XLV | Healthcare |
| XLI | Industrials |
| XLY | Consumer Discretionary |
| XLP | Consumer Staples |
| XLU | Utilities |
| XLRE | Real Estate |
| XLC | Communication Services |
| XLB | Materials |

Benchmark agregado: **SPY** (S&P 500) ou **VOO** (Vanguard S&P 500). yfinance
cobre todos. Análogo brasileiro: **IBOV** (já temos).

## Universo US para quando arrancar

S&P 500 Dividend Aristocrats é o ponto de partida natural para DRIP/Buffett.
Lista actualizada: https://www.spglobal.com/spdji/en/indices/dividends-factors/sp-500-dividend-aristocrats/

Alternativas que valem watchlist:
- **Dividend Kings** (50+ anos de aumentos) — ~50 tickers
- **Dividend Champions** (25+ anos) — superset dos Aristocrats
- Megacaps tech com dividendos emergentes: MSFT, AAPL, GOOGL (se DY ≥ 2.5%)
- Utilities (sector inteiro XLU tipicamente passa DY)
- REITs listados (tratamento especial, critérios diferentes — análogo aos FIIs)
