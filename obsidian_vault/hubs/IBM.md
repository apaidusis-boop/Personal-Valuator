---
type: ticker_hub
ticker: IBM
market: us
sector: Technology
currency: USD
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 4
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# IBM — International Business Machines

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Technology` · `market: US` · `currency: USD` · `bucket: watchlist` · `4 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 4.43, 2026-05-09)
- **Fundamentals** (2026-05-13): P/E 19.01 · P/B 6.12 · DY 3.1% · ROE 35.8% · ND/EBITDA 3.49 · Dividend streak 65 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\IBM.md` (cemetery archive)_

#### IBM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://www.ibm.com/investor
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **148**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=223.5500030517578
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.35772 · DY=0.030105121485692058 · P/E=19.783186
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.02,5.03,5.07 |
| 2026-04-23 | 10-Q | sec | 10-Q |
| 2026-04-22 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-10 | proxy | sec | DEF 14A |
| 2026-03-03 | 8-K | sec | 8-K \| 5.03,9.01 |

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


### 2019

#### 2019-11-12 · Filing 2019-11-12
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\IBM_FILING_2019-11-12.md` (cemetery archive)_

#### Filing dossier — [[IBM]] · 2019-11-12

**Trigger**: `sec:8-K` no dia `2019-11-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/51143/000110465919062171/tm1922448d1_8k.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 229.76

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `82.09` |
| HOLD entre | `82.09` — `105.25` (consensus) |
| TRIM entre | `105.25` — `121.04` |
| **SELL acima de** | `121.04` |

_Método: `buffett_ceiling`. Consensus fair = R$105.25. Our fair (mais conservador) = R$82.09._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:57+00:00 | `buffett_ceiling` | 105.25 | 82.09 | 229.76 | SELL | single_source | `filing:sec:8-K:2019-11-12` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\IBM.md` (cemetery archive)_

#### IBM — International Business Machines

#watchlist #us #technology

##### Links

- Sector: [[sectors/Technology|Technology]]
- Market: [[markets/US|US]]
- Peers: [[AAPL]] · [[ACN]] · [[PLTR]] · [[TSM]] · [[JKHY]]

##### Snapshot

- **Preço**: $225.74  (2026-05-06)    _-1.44% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 75.0/100 (WATCH)

##### Fundamentals

- P/E: 19.994686 | P/B: 6.4344554 | DY: 2.98%
- ROE: 35.77% | EPS: 11.29 | BVPS: 35.083
- Streak div: 65y | Aristocrat: True

##### Dividendos recentes

- 2026-02-10: $1.6800
- 2025-11-10: $1.6800
- 2025-08-08: $1.6800
- 2025-05-09: $1.6800
- 2025-02-10: $1.6700

##### Eventos (SEC/CVM)

- **2026-05-01** `8-K` — 8-K | 5.02,5.03,5.07
- **2026-04-23** `10-Q` — 10-Q
- **2026-04-22** `8-K` — 8-K | 2.02,9.01

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -28.33%
- **Drawdown 5y**: -28.33%
- **YTD**: -22.56%
- **YoY (1y)**: -9.39%
- **CAGR 3y**: +22.22%  |  **5y**: +10.17%  |  **10y**: +4.83%
- **Vol annual**: +34.57%
- **Sharpe 3y** (rf=4%): +0.68

###### Dividendos
- **DY 5y avg**: +3.75%
- **Div CAGR 5y**: +1.45%
- **Frequency**: quarterly
- **Streak** (sem cortes): 29 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "IBM — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: IBM
    data: [254.14, 257.82, 266.95, 263.23, 263.9, 268.87, 281.03, 283.21, 291.06, 291.2, 290.42, 283.79, 285.87, 260.51, 260.26, 250.67, 236.3, 239.72, 239.4, 244.84, 244.1, 259.11, 256.24, 266.4, 281.44, 286.49, 293.87, 277.22, 281.28, 285.0, 308.21, 300.85, 309.13, 305.69, 290.4, 303.21, 302.62, 310.48, 308.66, 300.98, 305.09, 291.5, 302.72, 309.03, 297.54, 293.86, 314.73, 298.93, 259.52, 256.28, 237.54, 245.28, 253.33, 246.28, 250.37, 241.39, 242.39, 245.07, 237.82, 253.47, 231.08, 227.1, 229.03]
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
    data: [22.951525, 20.529203, 20.529203, 20.529203, 20.181416, 20.604773, 20.097345, 20.422634, 20.290009, 20.286095, 19.994686]
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
    data: [35.16, 35.77, 35.77, 35.77, 35.77, 35.77, 35.77, 35.77, 35.77, 35.77, 35.77]
  - title: DY %
    data: [2.63, 2.9, 2.9, 2.9, 2.95, 2.88, 2.96, 2.91, 2.93, 2.93, 2.98]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\IBM_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — IBM

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=2 | HOLD=3 | AVOID=0  
**Avg conviction majority**: 6.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE superior a 35%
- P/B reflete forte geração de caixa
- Histórico de dividendos

**Key risk**: Possível queda do ROE abaixo de 15% por dois trimestres consecutivos

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE superior a 35%
- P/B elevado reflete geração de caixa forte
- expansão em IA e cloud computing

**Key risk**: cenário macro adverso pode aumentar endividamento

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E ligeiramente alto
- ROE forte e consistente dividendos
- Potencial de crescimento em IA

**Key risk**: Endividamento pode aumentar com expansão agressiva em novas tecnologias

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/B elevado reflete forte geração de caixa
- ROE superior a 35% indica eficiência operacional
- Histórico de dividendos e crescimento sustentado

**Key risk**: Subida do P/B acima de 7, indicando sobreavaliação

###### 🟡 Ray Dalio — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- P/E ligeiramente alto
- ROE forte e consistente
- expansão em IA

**Key risk**: Aumento significativo do endividamento ou deterioração da geração de caixa

##### 📊 Context provided

```
TICKER: US:IBM

FUNDAMENTALS LATEST:
  pe: 20.529203
  pb: 6.6574826
  dy: 2.90%
  roe: 35.77%
  net_debt_ebitda: 3.4928059239240326

VAULT THESIS:
**Core thesis (2026-04-25)**: IBM é um gigante da tecnologia com uma longa história de distribuição de dividendos e crescimento sustentado. Apesar do P/E ligeiramente acima dos critérios recomendados, o P/B elevado reflete a forte geração de caixa e ROE superior a 35%, além de um DY de 2.90%.

**Key assumptions**:
1. IBM manterá sua posição dominante no mercado de serviços gerenciados e cloud computing
2. A empresa continuará a expandir suas operações em IA e aprendizado de máquina, impulsionando o crescimento futuro
3. O cenário macroeconômico permitirá que IBM mantenha seus níveis atuais de endividamento sob controle
4. IBM manterá seu histórico de dividendos sem interrupções

**Disconfirmation triggers**:
- ROE cair abaixo de 15% por dois trimestres consecutivos
- P/B subir acima de 7 p
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama IBM --write
ii deepdive IBM --save-obsidian
ii verdict IBM --narrate --write
ii fv IBM
python -m analytics.fair_value_forward --ticker IBM
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
