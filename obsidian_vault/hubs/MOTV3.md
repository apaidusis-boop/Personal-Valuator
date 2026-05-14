---
type: ticker_hub
ticker: MOTV3
market: br
sector: Industrials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 8
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# MOTV3 — Motiva

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Industrials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `8 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 4.0, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 9.98 · P/B 1.81 · DY 2.6% · ROE 20.4% · ND/EBITDA 3.66 · Dividend streak 2

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\MOTV3.md` (cemetery archive)_

#### MOTV3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.motiva.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=15.449999809265137
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.20401 · DY=0.02507482231602866 · P/E=10.510203
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-29 | fato_relevante | cvm | ABERTURA DO 4º PROGRAMA DE RECOMPRA DE AÇÕES |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-27 | fato_relevante | cvm | Intenção de Alienação de Participação Acionária - Grupo Mover. |
| 2026-04-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Movimentação Mensal - Mar |

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

#### 2026-05-08 · Filing 2026-05-08
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\MOTV3_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[MOTV3]] · 2026-05-08

**Trigger**: `cvm:fato_relevante` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1519199&numSequencia=1043905&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 15.19

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `11.97` |
| HOLD entre | `11.97` — `16.39` (consensus) |
| TRIM entre | `16.39` — `18.85` |
| **SELL acima de** | `18.85` |

_Método: `graham_number`. Consensus fair = R$16.39. Our fair (mais conservador) = R$11.97._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20401` | `0.2066` | +1.3% |
| EPS | `1.47` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.3B (+36.1% QoQ, +13.6% YoY)
- EBIT 3.1B (+86.8% QoQ)
- Margem EBIT 48.5% vs 35.4% prior
- Lucro líquido 1.4B (+60.5% QoQ, +209.6% YoY)

**BS / cash**
- Equity 16.1B (+6.9% QoQ)
- Dívida total 40.3B (+3.3% QoQ)
- FCF proxy 1.1B (+227.6% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 16.39 | 11.97 | 15.19 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-05-08` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:40+00:00 | `graham_number` | 16.39 | 11.97 | 15.67 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-29 · Filing 2026-04-29
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\MOTV3_FILING_2026-04-29.md` (cemetery archive)_

#### Filing dossier — [[MOTV3]] · 2026-04-29

**Trigger**: `cvm:fato_relevante` no dia `2026-04-29`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1511580&numSequencia=1036286&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 15.67

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `11.97` |
| HOLD entre | `11.97` — `16.39` (consensus) |
| TRIM entre | `16.39` — `18.85` |
| **SELL acima de** | `18.85` |

_Método: `graham_number`. Consensus fair = R$16.39. Our fair (mais conservador) = R$11.97._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20401` | `0.2066` | +1.3% |
| EPS | `1.47` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.3B (+36.1% QoQ, +13.6% YoY)
- EBIT 3.1B (+86.8% QoQ)
- Margem EBIT 48.5% vs 35.4% prior
- Lucro líquido 1.4B (+60.5% QoQ, +209.6% YoY)

**BS / cash**
- Equity 16.1B (+6.9% QoQ)
- Dívida total 40.3B (+3.3% QoQ)
- FCF proxy 1.1B (+227.6% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:40+00:00 | `graham_number` | 16.39 | 11.97 | 15.67 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\MOTV3_COUNCIL.md` (cemetery archive)_

#### Council Dossier — MOTV3 (MOTV3)

**Final stance**: 🟡 **HOLD**  
**Confidence**: `medium`  
**Modo (auto)**: A (BR)  |  **Sector**: Industrials  |  **Held**: não  
**Elapsed**: 40.1s  |  **Failures**: 0

##### Síntese

**Consenso**:
- A relação dívida líquida/EBITDA está acima do limite ideal
- ROE acima de 15% e margens EBITDA sólidas sugerem potencial

**Dissenso (preservado)**:
- role RISK_OFFICER diz que o alto ROE pode ser temporário ou não indicar uma tendência sustentável se a relação dívida líquida/EBITDA continuar alta e sem mitigação clara
- role PORTFOLIO_OFFICER diz que embora a relação dívida líquida/EBITDA esteja alta, o ROE de 20.8% sugere que a empresa pode gerar lucros suficientes para reduzir essa alavancagem ao longo do tempo

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ CCC deteriorando >30% YoY sem explicação
- ⚠️ dividend yield baixo e relação dívida líquida/EBITDA acima de 3x

**Sizing**: size 1.5-2.5% se add, trim se peso > 5%, hold actual se watchlist

##### Round 1 — Opening Statements (blind)

###### Sector Specialist — 🟡 **HOLD**

**Headline**: _MOTV3 tem ROE forte mas preocupante ND/EBITDA e DY baixo_

A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial. No entanto, a relação ND/EBITDA está alta e o DY é insatisfatório.

**Supporting metrics**:
- ROE=20.8%
- ND/EBITDA=3.55
- DY=1.98%

**Concerns**:
- ND/EBITDA acima do limite ideal
- Dividend yield baixo

###### Risk Officer — 🔴 **AVOID**

**Headline**: _Risco de deterioração financeira e incerteza operacional_

A relação dívida líquida/EBITDA está acima do limite ideal, sem mitigação clara nos próximos dois anos. Além disso, a empresa quebrou recentemente seu histórico de dividendos.

**Supporting metrics**:
- ND/EBITDA=3.55
- DivStreak=2.00

**Concerns**:
- Deterioração da margem EBITDA nos últimos trimestres
- Possível falta de liquidez para manter o pagamento de dividendos

**Veto signals**:
- 🚫 CCC deteriorando >30% YoY sem explicação

###### Portfolio Officer — 🟡 **HOLD**

**Headline**: _MOTV3 tem potencial de valorização mas riscos financeiros_

ROE acima de 20% sugere crescimento futuro, porém dívida líquida/EBITDA elevada e DY baixo indicam cautela.

**Supporting metrics**:
- P/E=10.72
- ROE=20.8%
- ND/EBITDA=3.55

**Concerns**:
- dívida líquida/EBITDA acima de 3x
- dividend yield baixo

##### Round 2 — Responses (after seeing peers)

###### Sector Specialist — 🟡 **HOLD**

**Agreed with**:
- A relação dívida líquida/EBITDA está acima do limite ideal, sem mitigação clara nos próximos dois anos.
- risk_officer

###### Risk Officer — 🔴 **AVOID**

**Agreed with**:
- A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial.
- sector_specialist

**Challenged**:
- ROE acima de 20% sugere crescimento futuro
- O alto ROE pode ser temporário ou não indicar uma tendência sustentável se a relação dívida líquida/EBITDA continuar alta e sem mitigação clara.

###### Portfolio Officer — 🟡 **HOLD**

**Agreed with**:
- A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial.
- sector_specialist

**Challenged**:
- Concerns: ND/EBITDA acima do limite ideal
- Embora a relação dívida líquida/EBITDA esteja alta, o ROE de 20.8% sugere que a empresa pode gerar lucros suficientes para reduzir essa alavancagem ao longo do tempo.

##### Dossier (factual base — same input for all voices)

```
=== TICKER: BR:MOTV3 — MOTV3 ===
Sector: Industrials  |  Modo (auto): A  |  Held: False
Last price: 15.539999961853027 (2026-04-29)
Fundamentals: P/E=10.72 | P/B=1.98 | DY=2.5% | ROE=20.8% | ND/EBITDA=3.55 | DivStreak=2.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=    6.3  ebit=   3.1  ni=   1.4  ebit_margin= 48.5%
  2025-06-30: rev=    4.7  ebit=   1.6  ni=   0.9  ebit_margin= 35.4%
  2025-03-31: rev=    4.6  ebit=   1.9  ni=   0.5  ebit_margin= 41.3%
  2024-12-31: rev=    6.2  ebit=   1.2  ni=   0.2  ebit_margin= 19.3%
  2024-09-30: rev=    5.6  ebit=   1.5  ni=   0.5  ebit_margin= 26.6%
  2024-06-30: rev=    5.3  ebit=   1.3  ni=   0.3  ebit_margin= 24.7%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-25)**: A MOTV3 opera no setor industrial brasileiro, com um P/E de 11.36 e um ROE de 20.78%, indicando potencial valorização a longo prazo. No entanto, o dividend yield de apenas 1.98% e uma relação dívida líquida/EBITDA acima do limite ideal (3.55 vs 3x) sugerem cautela.

**Key assumptions**:
1. Mantendo-se a tendência atual de crescimento dos lucros, o ROE se manterá acima de 15% nos próximos anos
2. A empresa conseguirá reduzir sua dívida líquida/EBITDA para abaixo de 3x nos próximos dois anos
3. O dividend yield aumentará significativamente em decorrência de políticas de distribuição mais agressivas ou melhora na rentabilidade operacional
4. A empresa continuará a pagar dividendos ininterruptamente, mantendo o histórico de cinco anos

**Disconfirmation triggers**

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  Sector weight: 0.0%
```

---
*STORYT_2.0 Council prototype · 100% Ollama local · zero Claude tokens · 3 voices × 2 rounds*

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MOTV3.md` (cemetery archive)_

#### MOTV3 — MOTV3

#watchlist #br #industrials

##### Links

- Sector: [[sectors/Industrials|Industrials]]
- Market: [[markets/BR|BR]]
- Peers: [[POMO3]] · [[RAPT4]] · [[RENT3]] · [[SIMH3]] · [[TUPY3]]

##### Snapshot

- **Preço**: R$15.67  (2026-05-07)    _-1.69% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 60.0/100 (WATCH)

##### Fundamentals

- P/E: 10.659863 | P/B: 1.9288529 | DY: 2.47%
- ROE: 20.4% | EPS: 1.47 | BVPS: 8.124
- Streak div: 2y | Aristocrat: None

##### Dividendos recentes

- 2026-04-22: R$0.0617
- 2025-12-11: R$0.1464
- 2025-08-06: R$0.1793
- 2025-04-24: R$0.7833

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Divulgação 1T26
- **2026-04-29** `fato_relevante` — ABERTURA DO 4º PROGRAMA DE RECOMPRA DE AÇÕES
- **2026-04-29** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Divulgação 1T26
- **2026-04-27** `fato_relevante` — Intenção de Alienação de Participação Acionária - Grupo Mover.
- **2026-04-10** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Movimentação Mensal - Mar

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MOTV3 — peso 2.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MOTV3 — peso 2.0% |
| 2026-04-24 | XP | catalyst | bull | — | Motiva (MOTV3) ADICIONADA ao portfolio Value (2%) em abril — simplificação operacional, governança superior. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -11.02%
- **Drawdown 5y**: -11.02%
- **YTD**: +4.82%
- **YoY (1y)**: +17.64%
- **CAGR 3y**: n/a  |  **5y**: n/a  |  **10y**: n/a
- **Vol annual**: +27.44%
- **Sharpe 3y** (rf=4%): n/a

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: semiannual
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$19.18B | R$11.89B | R$4.13B |
| 2023-12-31 | R$18.93B | R$7.79B | R$1.70B |
| 2024-12-31 | R$18.12B | R$5.88B | R$1.25B |
| 2025-12-31 | R$18.85B | R$8.72B | R$3.28B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "MOTV3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: MOTV3
    data: [13.4, 13.42, 13.8, 13.56, 13.48, 13.5, 13.48, 13.7, 13.73, 13.79, 13.79, 13.2, 13.0, 12.34, 12.3, 12.5, 12.85, 13.09, 12.9, 13.78, 14.4, 14.78, 14.59, 14.74, 15.04, 14.74, 14.39, 13.97, 13.91, 14.86, 15.35, 15.5, 16.03, 16.25, 15.91, 15.94, 15.97, 16.57, 15.5, 15.12, 14.87, 15.06, 15.35, 14.99, 15.24, 17.02, 16.71, 16.73, 16.99, 16.2, 17.0, 16.51, 15.59, 15.08, 15.15, 15.36, 15.24, 16.08, 16.95, 17.28, 16.48, 15.54, 15.94]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "MOTV3 — dividend history"
labels: ['2025', '2026']
series:
  - title: Dividends
    data: [1.109, 0.0617]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-15', '2026-04-21', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: P/E
    data: [10.8, 12.034483, 11.365517, 11.365517, 11.365517, 11.365517, 11.089655, 11.027586, 10.717241, 11.034482, 10.639456, 10.612245, 10.843537, 10.659863]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-15', '2026-04-21', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: ROE %
    data: [20.14, 20.78, 20.78, 20.78, 20.78, 20.78, 20.78, 20.78, 20.78, 20.78, 20.4, 20.4, 20.4, 20.4]
  - title: DY %
    data: [2.77, 6.38, 6.76, 1.98, 2.35, 2.35, 2.41, 2.42, 2.49, 2.42, 2.48, 2.48, 2.43, 2.47]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MOTV3_DOSSIE.md` (cemetery archive)_

#### 📑 MOTV3 — Motiva

> Generated **2026-04-26** by `ii dossier MOTV3`. Cross-links: [[MOTV3]] · [[MOTV3]] · [[CONSTITUTION]]

##### TL;DR

MOTV3 negocia P/E 11.37 e P/B 2.10 com ROE forte de 20.78%, mas DY de apenas 2.35% e streak curta de 2y deixam-na fora do critério Graham clássico (DY ≥6%). IC consensus HOLD com high confidence (80%) — qualidade operacional reconhecida, mas não compensa o yield baixo num portefólio orientado a renda. Achado-chave: ND/EBITDA 3.55× já acima do limite 3× combinado com market cap R$33B sugere que o equity story aqui é growth-via-concessões, não DRIP defensivo.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.45  |  **BVPS**: 7.85
- **ROE**: 20.78%  |  **P/E**: 11.37  |  **P/B**: 2.10
- **DY**: 2.35%  |  **Streak div**: 2y  |  **Market cap**: R$ 33.14B
- **Last price**: BRL 16.48 (2026-04-24)  |  **YoY**: +26.1%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MOTV3]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A MOTV3 opera no setor industrial brasileiro, com um P/E de 11.36 e um ROE de 20.78%, indicando potencial valorização a longo prazo. No entanto, o dividend yield de apenas 1.98% e uma relação dívida líquida/EBITDA acima do limite ideal (3.55 vs 3x) sugerem cautela.

**Key assumptions**:
1. Mantendo-se a tendência atual de crescimento dos lucros, o ROE se manterá acima de 15% nos próximos anos
2. A empresa conseguirá reduzir sua dívida líquida/EBITDA para abaixo de 3x nos próximos dois anos
3. O dividend yield aumentará significativamente em decorrência de políticas de distribuição mais agressivas ou melhora na rentabilidade operacional
4. A empresa continuará a pagar dividendos ininterruptamente, mantendo o histórico de cinco anos

**Disconfirmation triggers**

→ Vault: [[MOTV3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **73** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 90 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 11.37** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 11.37** passa.
- **P/B = 2.10** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.10** — verificar consistência com ROE.
- **DY = 2.35%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **2.35%** abaixo do floor — DRIP não-óbvio.
- **ROE = 20.78%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **20.78%** compounder-grade.
- **Graham Number ≈ R$ 16.00** vs preço **R$ 16.48** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 2y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Alavancagem acima do limite** — ND/EBITDA 3.55× vs floor 3.0×; concessões CAPEX-intensive amplificam risco em ciclo de juros alto. Trigger: `fundamentals.net_debt_ebitda > 3.8` em qualquer release.
- 🟡 **Yield insuficiente para tese DRIP** — 2.35% vs floor 6%; tese só faz sentido como growth/total-return, não para reinvestimento de dividendos. Trigger: `fundamentals.dy < 2%` consolida desqualificação.
- 🟡 **Risco regulatório/concessão** — fim de prazos de concessão, repactuações tarifárias e ambiente político. Trigger: notícia/release sobre quebra ou renegociação contratual (events table).
- 🟡 **Streak curta (2y)** — sem histórico para qualificar como dividendeira fiável; possível corte em ciclo down. Trigger: dividendo trimestral abaixo da média móvel 4Q.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR (caixa BRL only). Entry só faz sentido se reframe como growth/compounder — não DRIP. Trigger: ND/EBITDA cair sustentadamente <3× e DY subir >4%. Weight prudente 3-4% como Tier-2 (industrial cíclico/concessões).

##### 7. Tracking triggers (auto-monitoring)

- **Deleverage success** — `fundamentals.net_debt_ebitda < 3.0` por 2 trimestres → reabrir tese.
- **ROE drop** — `fundamentals.roe < 15%` → invalidação do pilar de qualidade.
- **DY upgrade** — `fundamentals.dy > 4%` → começa a fazer sentido para income.
- **Selic shock** — `macro.selic_meta` delta >+50bp → CAPEX/refinancing pressure.
- **Thesis health** — `conviction_scores.composite_score < 60` → flag review.

##### 8. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier MOTV3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MOTV3 — peso 2.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MOTV3 — peso 2.0% |
| 2026-04-24 | XP | catalyst | bull | — | Motiva (MOTV3) ADICIONADA ao portfolio Value (2%) em abril — simplificação operacional, governança superior. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MOTV3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — MOTV3

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=0 | HOLD=4 | AVOID=1  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE acima de 15%
- EV/EBITDA atraente
- Tendência de crescimento dos lucros

**Key risk**: Dívida líquida/EBITDA elevada e geração de caixa irregular

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE acima de 20% indica solidez
- Potencial para redução da dívida líquida/EBITDA
- Tendência de crescimento dos lucros

**Key risk**: Dividend yield baixo e relação dívida líquida/EBITDA acima do ideal

###### 🔴 Nassim Taleb — **AVOID** (conv 10/10, size: none)

**Rationale**:
- Dívida líquida/EBITDA acima de 3x
- Volatilidade nos resultados financeiros
- Falta de anti-fragilidade

**Key risk**: Leverage e fragilidade operacional

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/E baixo e ROE forte
- Potencial de redução da dívida
- Histórico de dividendos

**Key risk**: Dívida líquida/EBITDA acima do ideal pode comprometer a solvência

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE acima de 20% indica solidez
- P/E baixo sugere valorização potencial
- Cautela com dívida líquida/EBITDA elevada

**Key risk**: Dívida líquida/EBITDA acima do ideal pode comprometer finanças

##### 📊 Context provided

```
TICKER: BR:MOTV3

FUNDAMENTALS LATEST:
  pe: 11.365517
  pb: 2.0982938
  dy: 2.35%
  roe: 20.78%
  net_debt_ebitda: 3.5524173031237063

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=6.3 ebit=3.1 ni=1.4 em%=48.5 debt=40 fcf=1.1
  2025-06-30: rev=4.7 ebit=1.6 ni=0.9 em%=35.4 debt=39 fcf=-0.8
  2025-03-31: rev=4.6 ebit=1.9 ni=0.5 em%=41.3 debt=38 fcf=-1.3
  2024-12-31: rev=6.2 ebit=1.2 ni=0.2 em%=19.3 debt=34 fcf=-0.7
  2024-09-30: rev=5.6 ebit=1.5 ni=0.5 em%=26.6 debt=34 fcf=0.3
  2024-06-30: rev=5.3 ebit=1.3 ni=0.3 em%=24.7 debt=31 fcf=0.9

VAULT THESIS:
**Core thesis (2026-04-25)**: A MOTV3 opera no setor industrial brasileiro, com um P/E de 11.36 e um ROE de 20.78%, indicando potencial valorização a longo prazo. No entanto, o dividend yield de apenas 1.98% e uma relação dívida líquida/EBITDA acima do limite ideal (3.55 vs 3x) sugerem cautela.

**Key assumptions**:
1. Mantendo-se a tendência atual de crescimento dos lucros, o ROE se manterá acima de 15% nos próximos anos
2. A empresa conseguirá reduzir sua dívida líquida/EBITDA para abaixo de 3x nos próximos dois anos
3. O dividend yield aumentará significativamente em decorrência de políticas de distribuição mais agressivas ou melhora na rentabilidade operacional
4. A empresa continuará a pagar dividendos ininterruptamente, mantendo o histórico de cinco anos

**Disconfirmation triggers**

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global minerals demand is strong enough 
  - 5 Of The Best Folding E-Bikes, According To Consumer Reports - Jalopnik [Mon, 20 Ap]
    Blix, headquartered in Santa Cruz, Calif., has been building e-bikes since 2014 and currently offers a full lineup that includes the folding Vika+ Flex — featuring basics like a 500-watt electr
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MOTV3 — peso 2.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MOTV3 — peso 2.0% |
| 2026-04-24 | XP | catalyst | bull | — | Motiva (MOTV3) ADICIONADA ao portfolio Value (2%) em abril — simplificação operacional, governança superior. |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MOTV3_RI.md` (cemetery archive)_

#### MOTV3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `revenue`: **+36.1%**
- ⬆️ **QOQ** `ebit`: **+86.8%**
- ⬆️ **QOQ** `net_income`: **+60.5%**
- ⬆️ **QOQ** `fco`: **+57.2%**
- ⬆️ **QOQ** `fcf_proxy`: **+227.6%**
- ⬆️ **QOQ** `ebit_margin`: **+13.2pp**
- ⬆️ **YOY** `revenue`: **+13.5%**
- ⬆️ **YOY** `ebit`: **+107.4%**
- ⬆️ **YOY** `net_income`: **+209.6%**
- ⬆️ **YOY** `fco`: **+38.5%**
- ⬆️ **YOY** `fcf_proxy`: **+215.3%**
- ⬆️ **YOY** `ebit_margin`: **+22.0pp**
- ⬆️ **YOY** `net_margin`: **+14.2pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 6.3 mi | R$ 4.7 mi | +36.1% |
| `ebit` | R$ 3.1 mi | R$ 1.6 mi | +86.8% |
| `net_income` | R$ 1.4 mi | R$ 0.9 mi | +60.5% |
| `debt_total` | R$ 40.3 mi | R$ 39.0 mi | +3.3% |
| `fco` | R$ 2.8 mi | R$ 1.8 mi | +57.2% |
| `fcf_proxy` | R$ 1.1 mi | R$ -0.8 mi | +227.6% |
| `gross_margin` | 54.1% | 43.9% | +10.2pp |
| `ebit_margin` | 48.5% | 35.4% | +13.2pp |
| `net_margin` | 22.4% | 19.0% | +3.4pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 6.3 mi | R$ 5.6 mi | +13.5% |
| `ebit` | R$ 3.1 mi | R$ 1.5 mi | +107.4% |
| `net_income` | R$ 1.4 mi | R$ 0.5 mi | +209.6% |
| `debt_total` | R$ 40.3 mi | R$ 34.4 mi | +17.1% |
| `fco` | R$ 2.8 mi | R$ 2.0 mi | +38.5% |
| `fcf_proxy` | R$ 1.1 mi | R$ 0.3 mi | +215.3% |
| `gross_margin` | 54.1% | 34.8% | +19.3pp |
| `ebit_margin` | 48.5% | 26.6% | +22.0pp |
| `net_margin` | 22.4% | 8.2% | +14.2pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 6.3 | 48.5% | 22.4% | 40 | 3 |
| 2025-06-30 | ITR | 4.7 | 35.4% | 19.0% | 39 | 2 |
| 2025-03-31 | ITR | 4.6 | 41.3% | 12.0% | 38 | 1 |
| 2024-12-31 | DFP-ITR | 6.2 | 19.3% | 3.7% | 34 | 2 |
| 2024-09-30 | ITR | 5.6 | 26.6% | 8.2% | 34 | 2 |
| 2024-06-30 | ITR | 5.3 | 24.7% | 5.4% | 31 | 2 |
| 2024-03-31 | ITR | 4.7 | 30.6% | 7.2% | 32 | 1 |
| 2023-12-31 | DFP-ITR | 6.2 | 29.7% | 11.5% | 31 | 2 |
| 2023-09-30 | ITR | 4.4 | 28.5% | 5.7% | 30 | 2 |
| 2023-06-30 | ITR | 3.9 | 33.6% | 6.7% | 33 | 2 |
| 2023-03-31 | ITR | 4.4 | 41.1% | 14.2% | 29 | 1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [4.4, 3.9, 4.4, 6.2, 4.7, 5.3, 5.6, 6.2, 4.6, 4.7, 6.3]
  - title: EBIT margin %
    data: [41.1, 33.6, 28.5, 29.7, 30.6, 24.7, 26.6, 19.3, 41.3, 35.4, 48.5]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama MOTV3 --write
ii deepdive MOTV3 --save-obsidian
ii verdict MOTV3 --narrate --write
ii fv MOTV3
python -m analytics.fair_value_forward --ticker MOTV3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
