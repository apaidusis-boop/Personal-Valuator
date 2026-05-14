---
type: ticker_hub
ticker: CINF
market: us
sector: Financials
currency: USD
bucket: kings_aristocrats
is_holding: false
generated: 2026-05-14
sources_merged: 3
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# CINF — Cincinnati Financial

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: kings_aristocrats` · `3 sources merged`

## 🎯 Hoje

- **Fundamentals** (2026-05-13): P/E 9.33 · P/B 1.61 · DY 2.2% · ROE 18.7% · ND/EBITDA -0.10 · Dividend streak 41 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\CINF.md` (cemetery archive)_

#### CINF — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.cincinnati.com/
- **Pilot rationale**: heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=163.3300018310547
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.18735 · DY=0.021735137208117154 · P/E=9.338479
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

##### Agora (RI scrape live)

- Scrape: ❌ FALHOU — Traceback (most recent call last):
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 233, in <module>
    main()
    ~~~~^^
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 220, in main
    result = fetch(
        args.url,
    ...<5 lines>...
        headless=not args.no_headless,
    )
  File "C:\Users\paidu\investment-intellig


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CINF.md` (cemetery archive)_

#### CINF — Cincinnati Financial

#watchlist #us #financials

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[GS]] · [[JPM]] · [[NU]]

##### Snapshot

- **Preço**: $160.43  (2026-05-06)    _+0.05% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 100.0/100 (SAFE)

##### Fundamentals

- P/E: 9.172669 | P/B: 1.5783674 | DY: 2.21%
- ROE: 18.73% | EPS: 17.49 | BVPS: 101.643
- Streak div: 41y | Aristocrat: True

##### Dividendos recentes

- 2026-03-24: $0.9400
- 2025-12-22: $0.8700
- 2025-09-22: $0.8700
- 2025-06-23: $0.8700
- 2025-03-24: $0.8700

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -7.08%
- **Drawdown 5y**: -7.08%
- **YTD**: -0.66%
- **YoY (1y)**: +10.70%
- **CAGR 3y**: +15.09%  |  **5y**: +5.92%  |  **10y**: +9.16%
- **Vol annual**: +23.21%
- **Sharpe 3y** (rf=4%): +0.47

###### Dividendos
- **DY 5y avg**: +2.44%
- **Div CAGR 5y**: +8.40%
- **Frequency**: quarterly
- **Streak** (sem cortes): 7 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "CINF — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: CINF
    data: [146.67, 146.3, 150.17, 149.47, 151.6, 151.03, 148.25, 145.7, 143.72, 149.38, 146.09, 149.26, 150.73, 147.87, 149.51, 150.43, 149.88, 151.06, 152.96, 154.01, 153.53, 153.69, 155.13, 156.11, 154.42, 159.79, 165.69, 157.88, 153.02, 155.72, 151.83, 157.39, 166.4, 163.9, 163.66, 168.48, 162.83, 161.49, 167.07, 167.29, 164.79, 161.49, 165.19, 163.68, 161.78, 157.86, 162.48, 172.65, 165.11, 162.4, 163.75, 168.53, 163.32, 163.82, 157.86, 155.45, 157.35, 160.18, 163.68, 166.82, 168.18, 163.22, 160.35]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: P/E
    data: [10.972974, 10.842452, 10.842452, 10.842452, 10.918919, 10.874094, 9.33219, 9.353917, 9.118286, 9.168097, 9.172669]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: ROE %
    data: [16.04, 16.04, 16.04, 16.04, 16.04, 18.73, 18.73, 18.73, 18.73, 18.73, 18.73]
  - title: DY %
    data: [2.13, 2.16, 2.16, 2.16, 2.14, 2.15, 2.17, 2.17, 2.22, 2.21, 2.21]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CINF_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — CINF

**Committee verdict**: **BUY** (high confidence, 100% consensus)  
**Votes**: BUY=5 | HOLD=0 | AVOID=0  
**Avg conviction majority**: 7.4/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE de 18,73% é sólido e acima de 15%
- P/L baixo (9,23) indica possível subavaliação
- Dividend yield de 2,20% sugere geração de caixa

**Key risk**: Volatilidade do mercado de seguros pode afetar resultados

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- PE baixo e ROE alto sugerem valor
- Forecast positivo da Keefe, Bruyette & Woods
- Dividend yield atraente

**Key risk**: Aumento de impostos locais pode afetar lucratividade

###### 🟢 Nassim Taleb — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE baixo e ROE alto
- Dividendos atraentes
- Baixa alavancagem

**Key risk**: Dependência do mercado de seguros, potencial aumento de taxas governamentais

###### 🟢 Seth Klarman — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE e PB abaixo da média
- ROE sólido
- dividend yield atrativo

**Key risk**: volatilidade do setor de seguros e condições econômicas adversas

###### 🟢 Ray Dalio — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE baixo e ROE alto
- Dividend yield atraente
- Analistas positivos

**Key risk**: Possível aumento de impostos locais pode afetar resultados financeiros

##### 📊 Context provided

```
TICKER: US:CINF

FUNDAMENTALS LATEST:
  pe: 9.233848
  pb: 1.5888945
  dy: 2.20%
  roe: 18.73%
  net_debt_ebitda: -0.1027960701754386

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Keefe, Bruyette & Woods Issues Positive Forecast for Cincinnati Financial (NASDAQ:CINF) Stock Price - InsuranceNewsNet [Wed, 29 Ap]
    # Keefe, Bruyette & Woods Issues Positive Forecast for Cincinnati Financial (NASDAQ:CINF) Stock Price - Insurance News | InsuranceNewsNet. HomeNow reading INN Insider News. INN Insider News RSSGet our
  - City of Beavercreek will put a 1% income tax on November ballot - WYSO [Tue, 28 Ap]
    # City of Beavercreek will put a 1% income tax on November ballot. Beavercreek city council members on Monday unanimously approved putting a 1% earned income tax on the Nov. 3 ballot. “Your company is
  - Bengals News (5/6): Cincy offense gets little respect in new ranking - Cincy Jungle [Wed, 06 Ma]
    # Bengals News (5/6): Cincy offense gets little respect in new ranking. ## Bengals News. Ranking Every NFL Offense After the 2026 Draft. Welcome to the “tweak” phase of the NFL calendar. According to 
  - Cincinnati Reds vs. Colorado Rockies - April 29, 2026 | Live Scores, Updates, Odds, Injury News and Recaps - Bleacher Re [Wed, 29 Ap]
    Image 3: Cincinnati Reds logo. Image 9: Cincinnati Reds logo. Image 11: Cincinnati Reds logo. Image 13: Cincinnati Reds logo. Image 22: tag-logo MLB Network 11m Image 23 Coming up next on MLB Network,
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama CINF --write
ii deepdive CINF --save-obsidian
ii verdict CINF --narrate --write
ii fv CINF
python -m analytics.fair_value_forward --ticker CINF
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
