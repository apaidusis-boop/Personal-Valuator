---
type: ticker_hub
ticker: POMO4
market: br
sector: Industrials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 5
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# POMO4 — Marcopolo PN

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Industrials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `5 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `WATCH` (score 6.97, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 5.92 · P/B 1.92 · DY 15.9% · ROE 31.0% · ND/EBITDA 0.99 · Dividend streak 17

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\POMO4.md` (now in cemetery)_

#### POMO4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.marcopolo.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=6.170000076293945
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.30973 · DY=0.1530131261468436 · P/E=6.17
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-15 | fato_relevante | cvm | Pagamento de Juros Sobre o Capital Próprio |
| 2026-03-24 | fato_relevante | cvm | Alteração dos portais de publicação |
| 2026-03-03 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-02-27 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação de Resultados 4T25 e |
| 2026-02-17 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |

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

#### 2026-05-05 · Filing 2026-05-05
_source: `dossiers\POMO4_FILING_2026-05-05.md` (now in cemetery)_

#### Filing dossier — [[POMO4]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515775&numSequencia=1040481&numVersao=1>

##### 🎯 Acção sugerida

###### 🟢 **BUY** &mdash; preço 6.08

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `6.09` |
| HOLD entre | `6.09` — `8.34` (consensus) |
| TRIM entre | `8.34` — `9.59` |
| **SELL acima de** | `9.59` |

_Método: `graham_number`. Consensus fair = R$8.34. Our fair (mais conservador) = R$6.09._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 8.34 | 6.09 | 6.08 | BUY | single_source | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 8.34 | 6.25 | 6.44 | HOLD | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 8.34 | 6.25 | 6.44 | HOLD | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 8.34 | 6.25 | 6.44 | HOLD | single_source | `extend_2026-05-09` |
| 2026-05-08T19:21:01+00:00 | `graham_number` | 8.34 | 6.25 | 6.37 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-15` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-15 · Filing 2026-04-15
_source: `dossiers\POMO4_FILING_2026-04-15.md` (now in cemetery)_

#### Filing dossier — [[POMO4]] · 2026-04-15

**Trigger**: `cvm:fato_relevante` no dia `2026-04-15`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505167&numSequencia=1029873&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 6.37

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `6.25` |
| HOLD entre | `6.25` — `8.34` (consensus) |
| TRIM entre | `8.34` — `9.59` |
| **SELL acima de** | `9.59` |

_Método: `graham_number`. Consensus fair = R$8.34. Our fair (mais conservador) = R$6.25._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `graham_number` | 8.34 | 6.25 | 6.37 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-15` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `tickers\POMO4.md` (now in cemetery)_

#### POMO4 — POMO4

#watchlist #br

##### Links

- Sector: [[sectors/Uncategorized|None]]
- Market: [[markets/BR|BR]]

##### Snapshot

- **Preço**: R$6.37  (2026-05-07)    _-0.16% 1d_
- **Screen**: 1.0  ✓ PASS
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 75.0/100 (WATCH)

##### Fundamentals

- P/E: 6.37 | P/B: 2.062156 | DY: 14.82%
- ROE: 30.97% | EPS: 1.0 | BVPS: 3.089
- Streak div: 17y | Aristocrat: None

##### Dividendos recentes

- 2026-04-27: R$0.0850
- 2025-11-25: R$0.7091
- 2025-08-27: R$0.1500
- 2025-05-02: R$0.0773
- 2025-02-27: R$0.2091

##### Eventos (SEC/CVM)

- **2026-04-15** `fato_relevante` — Pagamento de Juros Sobre o Capital Próprio
- **2026-03-24** `fato_relevante` — Alteração dos portais de publicação
- **2026-03-03** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-02-27** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação de Resultados 4T25 e
- **2026-02-17** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=1 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] POMO4 — peso 9.6%, setor Industrials |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -10.28%
- **Drawdown 5y**: -10.28%
- **YTD**: -1.24%
- **YoY (1y)**: n/a
- **CAGR 3y**: n/a  |  **5y**: n/a  |  **10y**: n/a
- **Vol annual**: +33.37%
- **Sharpe 3y** (rf=4%): n/a

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: +52.32%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "POMO4 — 1y close"
labels: ['2026-01-30', '2026-02-02', '2026-02-03', '2026-02-04', '2026-02-05', '2026-02-06', '2026-02-09', '2026-02-10', '2026-02-11', '2026-02-12', '2026-02-13', '2026-02-18', '2026-02-19', '2026-02-20', '2026-02-23', '2026-02-24', '2026-02-25', '2026-02-26', '2026-02-27', '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-05', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-16', '2026-03-17', '2026-03-18', '2026-03-19', '2026-03-20', '2026-03-23', '2026-03-24', '2026-03-25', '2026-03-26', '2026-03-27', '2026-03-30', '2026-03-31', '2026-04-01', '2026-04-02', '2026-04-06', '2026-04-07', '2026-04-08', '2026-04-09', '2026-04-10', '2026-04-13', '2026-04-14', '2026-04-15', '2026-04-16', '2026-04-17', '2026-04-20', '2026-04-22', '2026-04-23', '2026-04-24', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: POMO4
    data: [6.45, 6.57, 6.5, 6.22, 6.24, 6.35, 6.44, 6.47, 6.52, 6.36, 6.36, 6.51, 6.53, 6.54, 6.62, 6.79, 6.66, 7.03, 6.88, 6.68, 6.6, 6.69, 6.57, 6.34, 6.34, 6.31, 6.23, 6.07, 5.89, 5.93, 5.96, 5.86, 5.9, 5.77, 6.13, 6.12, 6.22, 6.12, 6.02, 6.02, 6.2, 6.23, 6.2, 6.23, 6.19, 6.4, 6.62, 6.76, 6.69, 6.94, 6.85, 6.86, 7.01, 7.1, 6.88, 6.75, 6.69, 6.63, 6.45, 6.4, 6.48, 6.35, 6.28, 6.38, 6.37]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "POMO4 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.0985, 0.0139, 0.084, 0.0455, 0.0705, 0.0811, 0.1076, 0.2742, 0.5015, 1.1455, 0.085]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: P/E
    data: [6.6122446, 6.479592, 6.4081635, 6.38, 6.37]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: ROE %
    data: [30.97, 30.97, 30.97, 30.97, 30.97]
  - title: DY %
    data: [15.76, 14.87, 15.03, 14.8, 14.82]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `tickers\POMO4_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — POMO4

**Committee verdict**: **BUY** (high confidence, 100% consensus)  
**Votes**: BUY=5 | HOLD=0 | AVOID=0  
**Avg conviction majority**: 8.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE alto e estável
- P/B baixo, geração de caixa forte
- Dividend yield atrativo

**Key risk**: Dependência de um setor específico pode levar a volatilidade

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- PE baixo e DY alto
- ROE forte
- Net debt/EBITDA saudável

**Key risk**: Flutuações cambiais negativas para exportações

###### 🟢 Nassim Taleb — **BUY** (conv 8/10, size: medium)

**Rationale**:
- PE baixo e DY alto
- ROE forte
- Nível de dívida controlado

**Key risk**: Potencial queda súbita no preço das ações (black swan)

###### 🟢 Seth Klarman — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE de 30.97% indica eficiência operacional
- DY de 14.66% é atrativo para investidores
- P/L baixo sugere desconto do valor intrínseco

**Key risk**: Risco de perda permanente se a indústria sofrer um choque sistêmico

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- P/E baixo
- Dividendos atrativos
- Baixa alavancagem

**Key risk**: Possível desaceleração econômica global impactando lucros

##### 📊 Context provided

```
TICKER: BR:POMO4

FUNDAMENTALS LATEST:
  pe: 6.44
  pb: 2.0848172
  dy: 14.66%
  roe: 30.97%
  net_debt_ebitda: 0.9931406677389282
  intangible_pct_assets: 3.1%   (goodwill $0.2B + intangibles $0.1B)
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=1 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] POMO4 — peso 9.6%, setor Industrials |

## ⚙️ Refresh commands

```bash
ii panorama POMO4 --write
ii deepdive POMO4 --save-obsidian
ii verdict POMO4 --narrate --write
ii fv POMO4
python -m analytics.fair_value_forward --ticker POMO4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
