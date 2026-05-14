---
type: ticker_hub
ticker: FDS
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

# FDS — FactSet

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: kings_aristocrats` · `3 sources merged`

## 🎯 Hoje

- **Fundamentals** (2026-05-13): P/E 12.98 · P/B 3.47 · DY 2.2% · ROE 28.1% · ND/EBITDA 1.39 · Dividend streak 28 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\FDS.md` (now in cemetery)_

#### FDS — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.factset.com/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=219.19000244140625
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.28084 · DY=0.020073908257636913 · P/E=14.104891
- Score (último run): score=0.6 · passes_screen=0

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
_source: `tickers\FDS.md` (now in cemetery)_

#### FDS — FactSet

#watchlist #us #financials

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[GS]] · [[JPM]] · [[NU]]

##### Snapshot

- **Preço**: $211.79  (2026-05-06)    _-3.48% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 95.0/100 (SAFE)

##### Fundamentals

- P/E: 13.637476 | P/B: 3.6447647 | DY: 2.08%
- ROE: 28.08% | EPS: 15.53 | BVPS: 58.108
- Streak div: 28y | Aristocrat: True

##### Dividendos recentes

- 2026-02-27: $1.1000
- 2025-11-28: $1.1000
- 2025-08-29: $1.1000
- 2025-05-30: $1.1000
- 2025-02-28: $1.0400

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -55.25%
- **Drawdown 5y**: -57.28%
- **YTD**: -25.66%
- **YoY (1y)**: -50.73%
- **CAGR 3y**: -19.49%  |  **5y**: -8.87%  |  **10y**: +3.47%
- **Vol annual**: +37.79%
- **Sharpe 3y** (rf=4%): -0.85

###### Dividendos
- **DY 5y avg**: +0.94%
- **Div CAGR 5y**: +7.66%
- **Frequency**: quarterly
- **Streak** (sem cortes): 20 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "FDS — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: FDS
    data: [448.49, 459.87, 470.16, 462.99, 456.56, 432.35, 424.17, 425.04, 439.87, 450.3, 444.57, 440.01, 432.32, 421.46, 409.16, 387.51, 377.57, 369.62, 376.96, 380.22, 370.8, 372.86, 344.43, 289.15, 283.86, 286.73, 276.93, 285.99, 286.67, 286.84, 266.89, 264.58, 265.09, 273.91, 273.05, 277.41, 279.15, 287.56, 292.03, 288.54, 292.13, 284.9, 294.17, 295.27, 284.13, 268.66, 248.76, 207.32, 201.95, 198.88, 206.62, 222.87, 221.04, 205.65, 208.84, 193.88, 216.99, 227.6, 226.42, 232.73, 228.08, 232.32, 219.42]
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
    data: [15.464608, 14.431423, 14.431423, 14.431423, 14.509337, 14.762701, 14.949807, 14.644788, 14.442729, 14.128783, 13.637476]
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
    data: [28.08, 28.08, 28.08, 28.08, 28.08, 28.08, 28.08, 28.08, 28.08, 28.08, 28.08]
  - title: DY %
    data: [1.83, 1.96, 1.96, 1.96, 1.95, 1.92, 1.89, 1.93, 1.96, 2.01, 2.08]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `tickers\FDS_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — FDS

**Committee verdict**: **BUY** (medium confidence, 60% consensus)  
**Votes**: BUY=3 | HOLD=2 | AVOID=0  
**Avg conviction majority**: 7.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE de 28% indicativo de alto retorno sobre investimento
- Histórico consistente de dividendos e crescimento
- Pequeno múltiplo P/E sugerindo preço justo ou abaixo

**Key risk**: Dependência excessiva da indústria financeira pode afetar receitas

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- ROE de 28% indica eficiência operacional
- Histórico consistente de dividendos
- Crescimento contínuo em um mercado em expansão

**Key risk**: Aumento da concorrência pode ameaçar margens e crescimento

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE forte e dividendos consistentes
- expansão de serviços e software
- mercado financeiro investindo em tecnologia

**Key risk**: Leverage e complexidade operacional podem criar riscos ocultos

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E razoável
- ROE forte
- Histórico de dividendos

**Key risk**: Avaliação preço-balanço alta pode refletir expectativas elevadas

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Fortes indicadores fundamentais
- Histórico de crescimento e dividendos
- Demanda crescente por tecnologia financeira

**Key risk**: Aumento da concorrência e mudanças regulatórias no setor financeiro

##### 📊 Context provided

```
TICKER: US:FDS

FUNDAMENTALS LATEST:
  pe: 14.431423
  pb: 3.8569558
  dy: 1.96%
  roe: 28.08%
  net_debt_ebitda: 1.3936023345551072

VAULT THESIS:
**Core thesis (2026-04-25)**: FactSet é um fornecedor líder de dados e software para a indústria financeira, com forte histórico de crescimento contínuo e retorno sobre o patrimônio (ROE) de 28%. A empresa atende aos critérios do Dividend Aristocrat, oferecendo dividendos consistentes por mais de duas décadas.

**Key assumptions**:
1. FactSet continuará a expandir suas ofertas de software e serviços para atender às demandas crescentes dos clientes em um ambiente competitivo
2. A empresa manterá sua política de dividendos robusta, com pagamentos consistentes ao acionista nos próximos anos
3. O mercado financeiro continuará a investir em tecnologia avançada para análise e gerenciamento de portfólios
4. FactSet terá sucesso na integração de novas aquisições, mantendo seu ritmo atual de cresci
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama FDS --write
ii deepdive FDS --save-obsidian
ii verdict FDS --narrate --write
ii fv FDS
python -m analytics.fair_value_forward --ticker FDS
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
