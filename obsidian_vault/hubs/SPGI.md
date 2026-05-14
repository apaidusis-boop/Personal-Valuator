---
type: ticker_hub
ticker: SPGI
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

# SPGI — S&P Global

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: kings_aristocrats` · `3 sources merged`

## 🎯 Hoje

- **Fundamentals** (2026-05-13): P/E 25.70 · P/B 3.86 · DY 0.9% · ROE 13.9% · ND/EBITDA 1.54 · Dividend streak 42 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\SPGI.md` (cemetery archive)_

#### SPGI — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.spglobal.com/
- **Pilot rationale**: heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=421.0
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.13939999 · DY=0.009144893111638954 · P/E=26.645569
- Score (último run): score=0.2 · passes_screen=0

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
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\SPGI.md` (cemetery archive)_

#### SPGI — S&P Global

#watchlist #us #financials

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[GS]] · [[JPM]] · [[NU]]

##### Snapshot

- **Preço**: $423.57  (2026-05-06)    _-0.07% 1d_
- **Screen**: 0.2  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 90.0/100 (SAFE)

##### Fundamentals

- P/E: 26.791271 | P/B: 4.066025 | DY: 0.91%
- ROE: 13.94% | EPS: 15.81 | BVPS: 104.173
- Streak div: 42y | Aristocrat: True

##### Dividendos recentes

- 2026-02-25: $0.9700
- 2025-11-25: $0.9600
- 2025-08-26: $0.9600
- 2025-05-28: $0.9600
- 2025-02-26: $0.9600

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -24.92%
- **Drawdown 5y**: -24.92%
- **YTD**: -17.38%
- **YoY (1y)**: -15.59%
- **CAGR 3y**: +6.14%  |  **5y**: +1.63%  |  **10y**: +15.05%
- **Vol annual**: +29.32%
- **Sharpe 3y** (rf=4%): +0.09

###### Dividendos
- **DY 5y avg**: +0.79%
- **Div CAGR 5y**: +5.67%
- **Frequency**: quarterly
- **Streak** (sem cortes): 26 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "SPGI — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: SPGI
    data: [507.61, 511.94, 522.94, 516.7, 513.59, 519.36, 505.87, 502.63, 521.29, 529.32, 526.39, 530.12, 524.38, 530.85, 529.33, 563.02, 555.88, 556.47, 552.44, 549.87, 539.24, 547.71, 543.99, 507.16, 484.94, 481.67, 481.22, 479.34, 473.19, 482.7, 473.05, 499.21, 493.84, 493.9, 490.91, 495.61, 499.88, 490.73, 499.63, 512.6, 529.45, 512.66, 541.56, 545.0, 531.16, 526.67, 527.66, 439.28, 397.2, 416.67, 423.61, 443.99, 445.28, 422.49, 426.14, 408.48, 425.34, 430.06, 430.08, 442.57, 439.03, 433.19, 423.87]
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
    data: [30.352903, 29.79468, 29.754087, 29.754087, 29.783379, 29.588396, 27.382427, 27.275774, 26.865908, 26.827215, 26.791271]
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
    data: [13.09, 13.09, 13.09, 13.09, 13.09, 13.09, 13.94, 13.94, 13.94, 13.94, 13.94]
  - title: DY %
    data: [0.87, 0.88, 0.88, 0.88, 0.88, 0.89, 0.89, 0.89, 0.91, 0.91, 0.91]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\SPGI_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — SPGI

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=1 | HOLD=3 | AVOID=1  
**Avg conviction majority**: 6.3/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- Liderança no mercado de dados financeiros
- Histórico sólido de dividendos
- ROE acima de 13%

**Key risk**: P/E alto e P/B elevado, indicando possível sobreavaliação

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Líder de mercado com forte ROE
- Histórico sólido de dividendos
- Posicionamento defensivo em tempos voláteis

**Key risk**: Desaceleração significativa no crescimento das receitas e margens operacionais

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/E e P/B não atendem aos critérios
- Falta de anti-fragilidade em um ambiente volátil
- Nível de dívida é preocupante

**Key risk**: Leverage aumenta fragilidade diante de eventos tail risk

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E e P/B não atendem aos critérios de valuation
- ROE acima da média, mas não oferece margem significativa de segurança
- Histórico sólido de dividendos

**Key risk**: Caso o ROE caia abaixo de 12% por dois trimestres consecutivos

###### 🟡 Ray Dalio — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- P/E e P/B dentro dos limites
- ROE acima de 13%
- Histórico sólido de dividendos

**Key risk**: Desaceleração significativa do ROE abaixo de 12% por dois trimestres

##### 📊 Context provided

```
TICKER: US:SPGI

FUNDAMENTALS LATEST:
  pe: 29.754087
  pb: 4.1929293
  dy: 0.88%
  roe: 13.09%
  net_debt_ebitda: 1.55743067102273

VAULT THESIS:
**Core thesis (2026-04-26)**: S&P Global é líder em fornecimento de dados e análises para o mercado financeiro, com um histórico sólido de dividendos. Apesar de não atender completamente aos critérios de valuation da filosofia (P/E > 20 e P/B > 3), possui uma margem de segurança através do seu ROE acima de 13% e uma longa história de pagamentos de dividendos, sendo um Dividend Aristocrat.

**Key assumptions**:
1. S&P Global manterá sua posição dominante no mercado de dados financeiros
2. A companhia continuará a gerar lucros consistentes apesar da volatilidade do mercado
3. O crescimento sustentável de receita e margens operacionais será mantido
4. S&P Global manterá seu histórico de dividendos elevados

**Disconfirmation triggers**:
- ROE cai abaixo de 12% por dois trimestres consecutivos
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama SPGI --write
ii deepdive SPGI --save-obsidian
ii verdict SPGI --narrate --write
ii fv SPGI
python -m analytics.fair_value_forward --ticker SPGI
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
