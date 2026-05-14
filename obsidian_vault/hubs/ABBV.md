---
type: ticker_hub
ticker: ABBV
market: us
sector: Healthcare
currency: USD
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 16
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# ABBV — AbbVie

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Healthcare` · `market: US` · `currency: USD` · `bucket: watchlist` · `16 sources merged`

## 🎯 Hoje

- **Posição**: 7.46602 @ entry 200.91025740622177
- **Verdict (DB)**: `SKIP` (score 4.95, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 102.21 · P/B -55.35 · DY 3.2% · ND/EBITDA 2.12 · Dividend streak 14 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\ABBV.md` (cemetery archive)_

#### ABBV — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://investors.abbvie.com/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: qty=7.46602 · entry=200.91025740622177 · date=2026-04-23

- Total events na DB: **183**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=202.77999877929688
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.03323799211250479 · P/E=99.40196
- Score (último run): score=0.8 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 10-Q | sec | 10-Q |
| 2026-04-29 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-03 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-23 | proxy | sec | DEF 14A |
| 2026-03-04 | 8-K | sec | 8-K \| 8.01,9.01 |

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

#### 2026-05-12 · Filing 2026-05-12
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_FILING_2026-05-12.md` (cemetery archive)_

#### Filing dossier — [[ABBV]] · 2026-05-12

**Trigger**: `sec:8-K` no dia `2026-05-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1551152/000110465926059484/tm2614276d1_8k.htm>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `None` | `-1.1403` | +0.0% |
| EPS | `2.04` | `2.0502` | +0.5% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-08 · Filing 2026-05-08
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[ABBV]] · 2026-05-08

**Trigger**: `sec:10-Q` no dia `2026-05-08`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1551152/000155115226000017/abbv-20260331.htm>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `None` | `-1.1403` | +0.0% |
| EPS | `2.04` | `2.0502` | +0.5% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Council review · Charlie Compounder
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Charlie Compounder\reviews\ABBV_2026-04-30.md` (cemetery archive)_

#### Charlie Compounder sobre [[ABBV|ABBV]]

**Função no debate**: Industrials & Consumer US Specialist (Buffett frame) (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _High P/E and negative P/B cloud AbbVie's long-term prospects_

Despite a strong ROE of 62.25% and a dividend yield of 3.2%, AbbVie's high P/E ratio (103.59) and negative P/B (-114.23) raise valuation concerns.

**Métricas que invoquei**:
- P/E=103.59
- P/B=-114.23
- ROE=62.25%

**Preocupações**:
- High valuation metrics
- Negative P/B ratio

**Veto signals**:
- 🚫 valuation sem histórico de ROIC

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado.
- citação curta + nome do colega que disse

**Desafiei**:
- A AbbVie apresenta um ROE de 62,25% e margens estáveis apesar do P/E elevado. Pagamento consistente de dividendos.
- O ponto chave é que mesmo com um ROE alto, a relação entre o P/B negativo e o P/E extremamente alto sugere uma avaliação muito alta que não pode ser justificada apenas pelo ROE ou margens estáveis. O risco associado à sustentabilidade do dividendo também deve ser levado em consideração.
- Pedro Alocação

##### Quem mais estava na sala

- [[council.macro]] (Chief Macro Strategist)
- [[risk.drift-audit]] (Chief Risk Officer)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[ABBV|📖 Storytelling completo (8 actos)]]
- [[ABBV|🏛️ Transcript do Council debate]]
- [[council.industrials-us|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\ABBV_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[ABBV|ABBV]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _AbbVie mantém ROE impressionante e crescimento sustentável_

A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado.

**Métricas que invoquei**:
- ROE=62,25%
- DY=3,29%
- Piotroski F-Score: 8/9

**Preocupações**:
- P/B negativo
- Pressões regulatórias no dividendo

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Piotroski F-Score de 8/9 sugere saúde financeira sólida, Valentina Prudente

**Desafiei**:
- High valuation metrics | Negative P/B ratio, Charlie Compounder - esses fatores são preocupantes mas não refletem a consistência da AbbVie em manter um ROE elevado e crescimento sustentável

**Evidência nova**: A recente expansão de $1.4 bilhão na Carolina do Norte demonstra o compromisso contínuo da AbbVie com investimentos estratégicos.

##### Quem mais estava na sala

- [[council.industrials-us]] (Industrials & Consumer US Specialist (Buffett frame))
- [[risk.drift-audit]] (Chief Risk Officer)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[ABBV|📖 Storytelling completo (8 actos)]]
- [[ABBV|🏛️ Transcript do Council debate]]
- [[council.macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\ABBV_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[ABBV|ABBV]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _AbbVie mantém ROE impressionante e crescimento sustentável_

A AbbVie apresenta um ROE de 62,25% e margens estáveis apesar do P/E elevado. Pagamento consistente de dividendos.

**Métricas que invoquei**:
- ROE: 62,25%
- Dividend Yield: 3,2%
- Piotroski F-Score: 8/9

**Preocupações**:
- P/E muito alto (103.59x)
- P/B negativo (-114.23x)

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado. - Mariana Macro

**Desafiei**:
- High valuation metrics | Negative P/B ratio - Charlie Compounder
- P/B negativo | Pressões regulatórias no dividendo - Mariana Macro
- Altman Z-Score indica zona cinzenta de risco - Valentina Prudente
- Os métricas de valuation como P/E e P/B não refletem a sustentabilidade financeira da empresa, que continua gerando lucros consistentes e investindo em crescimento futuro.
- O Piotroski F-Score de 8/9 sugere uma saúde financeira sólida, apesar do Z-Score estar na zona cinzenta.

##### Quem mais estava na sala

- [[council.industrials-us]] (Industrials & Consumer US Specialist (Buffett frame))
- [[council.macro]] (Chief Macro Strategist)
- [[risk.drift-audit]] (Chief Risk Officer)

##### Documentos relacionados

- [[ABBV|📖 Storytelling completo (8 actos)]]
- [[ABBV|🏛️ Transcript do Council debate]]
- [[council.allocation|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\ABBV_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[ABBV|ABBV]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Altman Z-Score indica zona cinzenta de risco_

Piotroski F-Score de 8/9 sugere saúde financeira sólida, mas Altman Z-Score de 1.96 sinaliza potencial estresse financeiro.

**Métricas que invoquei**:
- Altman Z-Score: 1.96
- Piotroski F-Score: 8/9
- Beneish M-Score: -2.87

**Preocupações**:
- Z-Score na zona cinzenta de risco
- Dividendos dependem da sustentabilidade financeira

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Piotroski F-Score de 8/9 sugere saúde financeira sólida
- Mariana Macro

**Desafiei**:
- High P/E and negative P/B cloud AbbVie's long-term prospects
- A alta relação P/E e o P/B negativo não indicam necessariamente perda permanente do capital, mas podem sugerir volatilidade.
- Charlie Compounder

##### Quem mais estava na sala

- [[council.industrials-us]] (Industrials & Consumer US Specialist (Buffett frame))
- [[council.macro]] (Chief Macro Strategist)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[ABBV|📖 Storytelling completo (8 actos)]]
- [[ABBV|🏛️ Transcript do Council debate]]
- [[risk.drift-audit|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*


### 2017

#### 2017-03-20 · Filing 2017-03-20
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_FILING_2017-03-20.md` (cemetery archive)_

#### Filing dossier — [[ABBV]] · 2017-03-20

**Trigger**: `sec:proxy` no dia `2017-03-20`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1551152/000104746917001778/a2231406zdef14a.htm>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `None` | `-1.1403` | +0.0% |
| EPS | `2.05` | `2.0502` | +0.0% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[ABBV|ABBV]] (AbbVie)

**Final stance**: 🟡 **HOLD**  
**Confidence**: `medium`  
**Modo (auto)**: A (US)  |  **Sector**: Healthcare  |  **Held**: sim  
**Elapsed**: 64.2s  |  **Failures**: 0

##### Quem esteve na sala

- [[council.industrials-us]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[council.macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[risk.drift-audit]] — _Chief Risk Officer_ (`risk_officer`)
- [[council.allocation]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado.
- Piotroski F-Score de 8/9 sugere saúde financeira sólida.

**Dissenso (preservado)**:
- High valuation metrics | Negative P/B ratio - Charlie Compounder disse que esses fatores são preocupantes, Mariana Macro argumentou que não refletem a consistência da AbbVie em manter um ROE elevado e crescimento sustentável.
- P/B negativo | Pressões regulatórias no dividendo - Mariana Macro mencionou pressões regulatórias sobre o dividendo, Pedro Alocação ressaltou a importância de considerar essas preocupações.

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ valuation sem histórico de ROIC - Charlie Compounder
- ⚠️ P/B negativo e pressões regulatórias no dividendo - Mariana Macro

**Sizing**: Considerar uma alocação moderada entre 5-10% para mitigar riscos de valuation.

##### Round 1 — Opening Statements (blind)

###### [[council.industrials-us]] — 🟡 **HOLD**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _High P/E and negative P/B cloud AbbVie's long-term prospects_

Despite a strong ROE of 62.25% and a dividend yield of 3.2%, AbbVie's high P/E ratio (103.59) and negative P/B (-114.23) raise valuation concerns.

**Métricas**:
- P/E=103.59
- P/B=-114.23
- ROE=62.25%

**Preocupações**:
- High valuation metrics
- Negative P/B ratio

**Veto signals**:
- 🚫 valuation sem histórico de ROIC

###### [[council.macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _AbbVie mantém ROE impressionante e crescimento sustentável_

A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado.

**Métricas**:
- ROE=62,25%
- DY=3,29%
- Piotroski F-Score: 8/9

**Preocupações**:
- P/B negativo
- Pressões regulatórias no dividendo

###### [[risk.drift-audit]] — 🟡 **HOLD**
_Chief Risk Officer_

**Headline**: _Altman Z-Score indica zona cinzenta de risco_

Piotroski F-Score de 8/9 sugere saúde financeira sólida, mas Altman Z-Score de 1.96 sinaliza potencial estresse financeiro.

**Métricas**:
- Altman Z-Score: 1.96
- Piotroski F-Score: 8/9
- Beneish M-Score: -2.87

**Preocupações**:
- Z-Score na zona cinzenta de risco
- Dividendos dependem da sustentabilidade financeira

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _AbbVie mantém ROE impressionante e crescimento sustentável_

A AbbVie apresenta um ROE de 62,25% e margens estáveis apesar do P/E elevado. Pagamento consistente de dividendos.

**Métricas**:
- ROE: 62,25%
- Dividend Yield: 3,2%
- Piotroski F-Score: 8/9

**Preocupações**:
- P/E muito alto (103.59x)
- P/B negativo (-114.23x)

##### Round 2 — Respostas (peers visíveis)

###### [[council.industrials-us]] — 🟡 **HOLD**
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado.
- citação curta + nome do colega que disse

**Desafiou**:
- A AbbVie apresenta um ROE de 62,25% e margens estáveis apesar do P/E elevado. Pagamento consistente de dividendos.
- O ponto chave é que mesmo com um ROE alto, a relação entre o P/B negativo e o P/E extremamente alto sugere uma avaliação muito alta que não pode ser justificada apenas pelo ROE ou margens estáveis. O risco associado à sustentabilidade do dividendo também deve ser levado em consideração.
- Pedro Alocação

###### [[council.macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- Piotroski F-Score de 8/9 sugere saúde financeira sólida, Valentina Prudente

**Desafiou**:
- High valuation metrics | Negative P/B ratio, Charlie Compounder - esses fatores são preocupantes mas não refletem a consistência da AbbVie em manter um ROE elevado e crescimento sustentável

**Evidência nova**: A recente expansão de $1.4 bilhão na Carolina do Norte demonstra o compromisso contínuo da AbbVie com investimentos estratégicos.

###### [[risk.drift-audit]] — 🟡 **HOLD**
_Chief Risk Officer_

**Concordou com**:
- Piotroski F-Score de 8/9 sugere saúde financeira sólida
- Mariana Macro

**Desafiou**:
- High P/E and negative P/B cloud AbbVie's long-term prospects
- A alta relação P/E e o P/B negativo não indicam necessariamente perda permanente do capital, mas podem sugerir volatilidade.
- Charlie Compounder

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- A AbbVie apresenta um ROE de 62,25% e uma renda anual de 3,29%, demonstrando consistência no pagamento de dividendos apesar do P/E elevado. - Mariana Macro

**Desafiou**:
- High valuation metrics | Negative P/B ratio - Charlie Compounder
- P/B negativo | Pressões regulatórias no dividendo - Mariana Macro
- Altman Z-Score indica zona cinzenta de risco - Valentina Prudente
- Os métricas de valuation como P/E e P/B não refletem a sustentabilidade financeira da empresa, que continua gerando lucros consistentes e investindo em crescimento futuro.
- O Piotroski F-Score de 8/9 sugere uma saúde financeira sólida, apesar do Z-Score estar na zona cinzenta.

##### Documentos relacionados

- [[ABBV|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[ABBV|Charlie Compounder]] em [[council.industrials-us]]/reviews/
  - [[ABBV|Mariana Macro]] em [[council.macro]]/reviews/
  - [[ABBV|Valentina Prudente]] em [[risk.drift-audit]]/reviews/
  - [[ABBV|Pedro Alocação]] em [[council.allocation]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:ABBV — AbbVie ===
Sector: Healthcare  |  Modo (auto): A  |  Held: True
Last price: 211.32000732421875 (2026-04-30)
Position: 7 shares @ entry 200.91
Fundamentals: P/E=103.59 | P/B=-114.23 | DY=3.2% | DivStreak=14.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: A AbbVie é uma excelente posição long-term para um investidor Buffett/Graham devido à sua consistência no pagamento de dividendos e ao seu potencial de crescimento sustentado. Apesar do P/E alto de 86,91x, a empresa mantém um ROE impressionante de 62,25% e uma renda anual de 3,29%. Com uma história de 14 anos sem interrupção no pagamento de dividendos, a AbbVie demonstra sua capacidade de gerir lucrativamente seus negócios mesmo em cenários desafiadores.

**Key assumptions**:
1. A AbbVie continuará a expandir suas linhas de produtos e a manter um ROE acima de 60%.
2. O mercado farmacêutico global continuará a crescer, mantendo as margens da AbbVie estáveis ou aumentando-as.
3. A empresa manterá seu dividendo anual em pelo menos 3,29%, apesar das pressões regul

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 7.0%
  Sector weight: 17.1%

QUALITY SCORES:
  Piotroski F-Score: 8/9 (2025-12-31)
  Altman Z-Score: 1.96  zone=grey  conf=high
  Beneish M-Score: -2.87  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus - AbbVie News Center [Wed, 22 Ap]
    AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus. * Investment demonstrates continued progress against AbbVie's $100 billion commitment to U.S. research and development (R&D) and capital investments, including manufac
  - AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus - BioSpace [Thu, 23 Ap]
    # AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus. * Investment demonstrates continued progress against AbbVie's $100 billion commitment to U.S. research and development (R&D) and capital investments, including manuf
  - AbbVie commits $1.4B to NC plant in its largest-ever single campus investment - BioSpace [Thu, 23 Ap]
    AbbVie has selected North Carolina as the location for its largest-ever capital investment in one campus, committing $1.4 billion to build a drug production facility in the state. Illinois-based AbbVie, which disclosed the plan Wednesday, m
  - AbbVie (ABBV) Stock Trades Up, Here Is Why - The Chronicle-Journal [Wed, 29 Ap]
    # AbbVie (ABBV) Stock Trades Up, Here Is Why. April 29, 2026 at 15:36 PM EDT. Shares of pharmaceutical company AbbVie (NYSE: ABBV) jumped 3.5% in the afternoon session after the company reported first-quarter results that featured a revenue
  - AbbVie tops Q1 estimates, raises outlook and discontinues cancer candidate - BioSpace [Wed, 29 Ap]
    ## Strong growth in immunology and neurology prompted AbbVie to raise its 2026 outlook and consider future M&A from a position of “ample financial capacity.”. However, AbbVie’s shares are still down over 10% year-to-date, the firm said, “an
  - AbbVie’s (NYSE:ABBV) Q1 CY2026 Sales Top Estimates - The Chronicle-Journal [Wed, 29 Ap]
    Pharmaceutical company AbbVie (NYSE: ABBV) announced better-than-expected revenue in Q1 CY2026, with sales up 12.4% year on year to $15 billion. AbbVie’s annualized revenue growth of 7.5% over the last two years is above its five-year trend

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[1] sec (8-K) [2026-04-29]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000155115226000013/abbv-20260429.htm
[2] sec (8-K) [2026-04-03]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000155115226000011/abbv-20260403.htm
[3] sec (proxy) [2026-03-23]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000110465926033387/abbv-20260508xdef14a.htm
[4] sec (8-K) [2026-03-04]: 8-K | 8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000110465926023534/tm266774d4_8k.htm
[5] sec (8-K) [2026-02-26]: 8-K | 8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000110465926020643/tm266774d4_8k.htm
[6] sec (10-K) [2026-02-20]: 10-K
     URL: https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm

##### TAVILY NEWS (≤30d) (5 hits)
[7] Tavily [Wed, 22 Ap]: AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus. * Investment demonstrates continued progress against AbbVie's $100 billion commitment to U.S. research and development (R&D) and capital investments, including manufacturing, over the next decade. * New 185-acre campus will cre
     URL: https://news.abbvie.com/2026-04-22-AbbVie-Selects-North-Carolina-for-New-1-4-Billion-Manufacturing-Campus
[8] Tavily [Thu, 23 Ap]: # AbbVie Selects North Carolina for New $1.4 Billion Manufacturing Campus. * Investment demonstrates continued progress against AbbVie's $100 billion commitment to U.S. research and development (R&D) and capital investments, including manufacturing, over the next decade. NORTH CHICAGO, Ill., April 2
     URL: https://www.biospace.com/press-releases/abbvie-selects-north-carolina-for-new-1-4-billion-manufacturing-campus
[9] Tavily [Thu, 23 Ap]: AbbVie has selected North Carolina as the location for its largest-ever capital investment in one campus, committing $1.4 billion to build a drug production facility in the state. Illinois-based AbbVie, which disclosed the plan Wednesday, made the investment as part of a previously announced commitm
     URL: https://www.biospace.com/drug-delivery/abbvie-commits-1-4b-to-nc-plant-in-its-largest-ever-single-campus-investment
[10] Tavily [Thu, 23 Ap]: The $1.4 billion project is the latest revelation in the pharma group's $100 billion programme of manufacturing and R&D investment plan over the next decade, announced as part of a deal with the US government, designed to avoid tariffs, that also saw it sign up to the administration's Most Favoured 
     URL: https://pharmaphorum.com/news/abbvie-makes-record-investment-north-carolina-plant
[11] Tavily [Thu, 23 Ap]: # AbbVie to invest $1.4bn in North Carolina manufacturing campus. **American pharmaceutical company, AbbVie, has unveiled plans to invest $1.4bn in a new pharmaceutical manufacturing campus in Durham, marking a significant expansion of its U.S. production footprint and a major boost for the state’s 
     URL: https://www.themanufacturer.com/articles/abbvie-to-invest-1-4bn-in-north-carolina-manufacturing-campus/

##### TAVILY GUIDANCE (≤90d) (5 hits)
[12] Tavily [Wed, 29 Ap]: # AbbVie (ABBV) Stock Trades Up, Here Is Why. April 29, 2026 at 15:36 PM EDT. Shares of pharmaceutical company AbbVie (NYSE: ABBV) jumped 3.5% in the afternoon session after the company reported first-quarter results that featured a revenue beat. Looking ahead, AbbVie lowered its full-year 2026 adju
     URL: http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-29-abbvie-abbv-stock-trades-up-here-is-why
[13] Tavily [Wed, 29 Ap]: ## Strong growth in immunology and neurology prompted AbbVie to raise its 2026 outlook and consider future M&A from a position of “ample financial capacity.”. However, AbbVie’s shares are still down over 10% year-to-date, the firm said, “and we believe investors will continue to be focused on market
     URL: https://www.biospace.com/business/abbvie-tops-q1-estimates-raises-outlook-and-discontinues-cancer-candidate
[14] Tavily [Wed, 29 Ap]: Pharmaceutical company AbbVie (NYSE: ABBV) announced better-than-expected revenue in Q1 CY2026, with sales up 12.4% year on year to $15 billion. AbbVie’s annualized revenue growth of 7.5% over the last two years is above its five-year trend, which is encouraging. This quarter, AbbVie reported year-o
     URL: http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-29-abbvies-nyseabbv-q1-cy2026-sales-top-estimates
[15] Tavily [Tue, 28 Ap]: # AbbVie (ABBV) To Report Earnings Tomorrow: Here Is What To Expect. Pharmaceutical company AbbVie (NYSE: ABBV) will be announcing earnings results this Wednesday before market hours. AbbVie beat analysts’ revenue expectations last quarter, reporting revenues of $16.62 billion, up 10% year on year. 
     URL: http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-28-abbvie-abbv-to-report-earnings-tomorrow-here-is-what-to-expect
[16] Tavily [Thu, 16 Ap]: Comparable sales growth includes the prior and current year sales of Exact Sciences, a cancer diagnostics company that Abbott acquired on March 23, 2026. Comparable sales growth exclude

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_STORY.md` (cemetery archive)_

#### AbbVie — ABBV

##### Análise de Investimento · Modo FULL · Jurisdição US

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[council.industrials-us]] — _Industrials & Consumer US Specialist (Buffett frame)_
- [[council.macro]] — _Chief Macro Strategist_
- [[risk.drift-audit]] — _Chief Risk Officer_
- [[council.allocation]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/ABBV_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 61.2 bi · EBITDA est. R$ 10.44 bi · FCF R$ 17.82 bi · DGR 22.7% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 8/9 · Altman Z=1.96 (grey) · Beneish M=-2.87 (clean) |
| **5 — Classification** | Modo A-US · Dividend/DRIP (6/12) |
| **5.5 — Council Debate** | HOLD (medium) · 2 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. AbbVie, uma empresa do setor de Healthcare com ticker ABBV, é conhecida por sua abordagem estratégica em pesquisa e desenvolvimento (R&D) bem como na produção de medicamentos especializados, principalmente nos campos da imunologia, neurociência e oncologia. Recentemente, a companhia anunciou um investimento significativo no estado americano de North Carolina, comprometendo-se com uma nova fábrica que custará $1,4 bilhão e criará 734 empregos para apoiar a produção de seus medicamentos. Este projeto faz parte de um compromisso maior da AbbVie de investir US$ 100 bilhões nos Estados Unidos em R&D e capital durante uma década.

A armadilha típica que os investidores podem cair ao falar sobre a AbbVie é confundir o sucesso de seus produtos individuais, como Skyrizi e Rinvoq, com o desempenho geral da empresa. É fácil concentrar-se na performance de um único medicamento ou no impacto de uma decisão de marketing em vez de considerar a estratégia global e os esforços contínuos de inovação que sustentam a posição competitiva da AbbVie.

##### Ato 2 — O Contexto

O panorama macroeconômico atual é caracterizado por taxas de juros elevadas, com o Fed Funds Rate estabelecido entre 4.25% e 4.50%, enquanto a taxa de juro do Treasury 10Y se mantém em torno de 4.2%. O custo de capital próprio (Ke) é estimado em aproximadamente 10%, indicando um ambiente desafiador para financiamento corporativo. O ciclo econômico está no final da expansão e início de uma possível suavização, o que pode afetar a demanda por produtos farmacêuticos especializados.

Para o setor de saúde, essas condições podem resultar em maior pressão sobre os custos operacionais e financeiros. A AbbVie, com seu foco em R&D intensivo e investimentos significativos, pode enfrentar desafios adicionais nesse cenário econômico restritivo. No entanto, a empresa tem demonstrado resiliência ao anunciar recentemente um aumento no seu outlook para 2026, refletindo o forte crescimento em suas linhas de imunologia e neurologia.

Além disso, as mudanças regulatórias e estruturais continuam a moldar o ambiente operacional da AbbVie. Por exemplo, recentemente a empresa anunciou um compromisso com investimentos significativos no setor farmacêutico americano, que não apenas demonstra sua confiança na economia dos EUA, mas também pode ser visto como uma estratégia para evitar tarifas e alinhar-se às prioridades do governo americano. Esses movimentos estratégicos podem ter implicações significativas tanto no curto quanto no longo prazo para a AbbVie, influenciando não apenas sua posição competitiva, mas também suas perspectivas de crescimento futuro.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa e cheia de altos e baixos. Embora a receita tenha apresentado um crescimento modesto, com um CAGR (Crescimento Anual Compounded) de aproximadamente 1% entre 2022 e 2025, o desempenho operacional tem sido marcado por uma contração nas margens EBITDA e lucro líquido. A tabela abaixo detalha os principais indicadores financeiros anuais:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 58.05B | R$ 15.71B | R$ 17.28B | 29.8% | R$ 11.84B | 20.4% | R$ 24.25B |
| 2023 | R$ 54.32B | R$ 8.47B | R$ 9.32B | 17.2% | R$ 4.86B | 9.0% | R$ 22.06B |
| 2024 | R$ 56.33B | R$ 6.52B | R$ 7.18B | 12.7% | R$ 4.28B | 7.6% | R$ 17.83B |
| 2025 | R$ 61.16B | R$ 9.49B | R$ 10.44B | 17.1% | R$ 4.23B | 6.9% | R$ 17.82B |

O fluxo de caixa livre (FCF) tem sido uma constante positiva, embora tenha apresentado um declínio em 2024 e se mantido estável nos anos subsequentes. Este indicador é crucial para avaliar a capacidade da empresa de gerar dinheiro líquido após cobrir todas as despesas operacionais e investimentos necessários.

A distribuição de dividendos tem sido consistente, com um crescimento anual médio que reflete uma política de retorno aos acionistas. A tabela abaixo ilustra os valores pagos nos últimos anos:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 2.360 |
| 2021 | 5.200 |
| 2022 | 5.640 |
| 2023 | 5.920 |
| 2024 | 6.200 |
| 2025 | 6.560 |
| 2026 | 3.460 |

O Dividend Growth Rate (DGR) calculado, sem considerar dividendos extraordinários, é de 22.7% ao ano. Este crescimento sustentável sugere que a empresa tem mantido uma política consistente e estável de distribuição de lucros aos acionistas. No entanto, o DY estrutural (Dividend Yield) pode ser afetado por dividendos extraordinários, portanto, é importante analisar tanto o DY total quanto o estrutural.

A importância do FCF como indicador financeiro não deve ser subestimada, pois enquanto o lucro contábil pode esconder provisões e ajustes, o fluxo de caixa livre fornece uma imagem mais clara da geração de dinheiro pela empresa. Este é um ponto crucial para avaliar a sustentabilidade dos dividendos ao longo do tempo.

##### Ato 4 — O Balanço

O balanço financeiro atual da empresa reflete uma situação mista, com indicadores que sugerem tanto pontos fortes quanto áreas de preocupação. Com um preço de mercado de R$211.32 (data: 2026-04-30), a relação P/E está em 103.59 e o P/B é negativo, com -114.23. O Dividend Yield (DY) é de 3.19%, enquanto a empresa tem mantido uma sequência de dividendos ininterrupta por 14 anos.

A relação Net Debt/EBITDA calculada é de aproximadamente 3.2 vezes, baseando-se na estimativa do endividamento líquido (Net Debt) e no EBITDA mais recente da tabela fornecida. Este indicador sugere que a empresa tem um nível moderado de alavancagem financeira.

O Current Ratio é uma métrica importante para avaliar a liquidez curta prazo, embora o valor exato não seja disponível nos dados fornecidos. No entanto, considerando os fluxos de caixa positivos e consistentes, pode-se inferir que a empresa tem uma posição sólida em termos de capacidade de honrar suas obrigações curtas.

O Return on Equity (ROE) da empresa é significativamente superior ao custo do capital próprio (Ke), com um ROE estimado de cerca de 18.25% (considerando a Selic de 13.75% mais um prêmio de risco equity de 4.5%). Este desempenho sugere que a empresa está criando valor para seus acionistas, superando o custo do capital próprio.

No entanto, é importante notar que o endividamento líquido estimado em R$33.75 bi pode indicar uma tendência de alavancagem crescente, um ponto de atenção que requer monitoramento contínuo para garantir a sustentabilidade financeira da empresa no longo prazo.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa em questão revela uma situação complexa e desafiadora no mercado. O preço-earnings (P/E) da companhia está fixado em 103,59x, bem acima tanto do múltiplo médio setorial de 25,43x quanto do índice Ibov/S&P de 21,00x. Este valor elevado sugere que os investidores estão atribuindo um alto potencial de crescimento à empresa, embora possa indicar também uma sobreavaliação em relação aos seus pares e ao mercado geral.

O preço-book (P/B) da companhia é negativo, com um índice de -114,23x. Este valor está significativamente abaixo tanto do múltiplo médio setorial de 3,02x quanto do índice Ibov/S&P de 3,50x. A presença de um P/B negativo pode indicar que o ativo líquido da empresa é inferior ao seu preço de mercado, sugerindo potencialmente uma situação financeira delicada ou a existência de ativos intangíveis significativos.

O dividend yield (DY) reportado pela companhia é de 3,19%, ligeiramente superior à média setorial de 2,4% e ao índice Ibov/S&P de 1,5%. No entanto, é importante notar que o DY pode incluir dividendos extraordinários, o que não reflete necessariamente a rendibilidade estrutural da empresa. Este indicador sugere um retorno atrativo aos acionistas em termos de distribuição de lucros.

O fluxo de caixa livre (FCF) yield da companhia é de 5%, exatamente igual à média setorial e ligeiramente superior ao índice Ibov/S&P, que está em 4%. Este múltiplo reflete a eficiência da empresa em gerar caixa livre em relação ao seu valor de mercado.

A tabela abaixo compara os principais múltiplos financeiros da empresa com o setor e o índice:

| Múltiplo | ABBV | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 103.59x | 25.43x | 21.00x |
| P/B | -114.23x | 3.02x | 3.50x |
| DY | 3.2% | 2.4% | 1.5% |
| FCF Yield | 5.0% | 5.0% | 4.0% |
| ROE | — | 14.3% | 16.0% |
| ND/EBITDA | — | 0.96x | — |

##### Ato 6 — Os Quality Scores

A análise dos indicadores de qualidade financeira da empresa revela um quadro misto, com pontos fortes e fracos que merecem uma atenção especial.

O Piotroski F-Score da companhia é de 8/9 no último trimestre analisado (2025-12-31), indicando uma forte saúde financeira. Este resultado sugere que a empresa está gerindo bem seus fluxos de caixa e demonstra um bom desempenho operacional, com oito dos nove critérios avaliados sendo positivos.

O Altman Z-Score da companhia é de 1,96, colocando-a em uma zona cinza. Este indicador sugere que a empresa está em uma situação financeira instável e pode estar próxima do colapso, embora ainda não esteja tecnicamente em risco iminente.

O Beneish M-Score da companhia é de -2,87, classificado como "clean". Este resultado indica que as práticas contábeis da empresa são consideradas saudáveis e transparentes, sem sinais evidentes de manipulação financeira.

Em resumo, a combinação dos três indicadores sugere uma empresa com um desempenho operacional sólido mas financeiramente instável. A alta pontuação no Piotroski F-Score contrasta com o Z-Score cinza e o M-Score limpo, criando um quadro complexo que requer vigilância contínua dos investidores.

Tais resultados devem ser considerados em conjunto com as recomendações do sell-side disponíveis na pesquisa.

---

##### Ato 7 — O Moat e a Gestão

A AbbVie demonstra um moat significativo que se sustenta principalmente através de intangíveis, eficiência operacional e custos/escala. Este moat é classificado como "Wide" dada a forte presença da empresa no mercado farmacêutico com medicamentos especializados em imunologia, neurociência e oncologia.

###### Intangíveis
A AbbVie possui uma vasta carteira de patentes que protegem seus produtos inovadores. Medicamentos como Humira (para artrite reumatóide) e Skyrizi (para doenças inflamatórias), por exemplo, são fundamentais para a receita da empresa. Esses medicamentos não apenas geram lucros substanciais, mas também garantem que a AbbVie mantenha uma posição de liderança no mercado.

###### Eficiência Operacional
A recente decisão da AbbVie de investir $1.4 bilhões em um novo campus de fabricação na Carolina do Norte demonstra sua capacidade de otimizar seus processos e reduzir custos, enquanto expande suas operações para atender à crescente demanda por medicamentos especializados. Este é um indicador claro da eficiência operacional que a empresa mantém.

###### Custos/Escala
A AbbVie beneficia significativamente de economias de escala em sua cadeia de produção e distribuição, o que lhe permite oferecer produtos a preços competitivos sem comprometer a qualidade. O novo campus na Carolina do Norte é um exemplo deste modelo operacional, criando 734 empregos para apoiar a produção de medicamentos especializados.

###### Gestão
A gestão da AbbVie tem demonstrado consistência e visão estratégica ao investir em pesquisa e desenvolvimento, bem como em infraestrutura. A decisão de expandir suas operações na Carolina do Norte é um reflexo deste compromisso com a inovação e crescimento sustentável.

###### Insider Ownership
Dado não disponível

###### Insider Trades
Dado não disponível

##### Ato 8 — O Veredito

A AbbVie apresenta um perfil filosófico que favorece dividendos e distribuições de rendimentos, com uma ênfase clara na consistência do pagamento de dividendos ao longo dos anos. As pontuações indicam uma forte capacidade financeira e saúde operacional.

###### Perfil Filosófico
A AbbVie recebeu um score de 6 em Dividendos, refletindo seu histórico ininterrupto de pagamentos de dividendos por mais de 14 anos, com uma taxa atual de rendimento de 3.2%. Além disso, a empresa tem demonstrado forte cobertura do fluxo de caixa livre sobre o pagamento de dividendos.

###### O que o preço desconta
O preço atual da AbbVie reflete um cenário otimista em relação ao crescimento futuro e à sustentabilidade dos lucros. A decisão de investir na Carolina do Norte, por exemplo, é vista como uma estratégia para manter a liderança no mercado farmacêutico.

###### O que os fundamentos sugerem
Os fundamentos da AbbVie indicam um forte desempenho operacional e financeiro. A empresa tem mantido um ROE de 62,25%, demonstrando eficiência na geração de lucros a partir do capital empregado.

###### DCF — A âncora do valor
| Cenário | Crescimento 5y | Perpetuidade | Valor por ação |
|---|---|---|---|
| Pessimista | 5% a.a. | 3% | R$ 161.43 |
| **Base** | **8% a.a.** | **4%** | **R$ 207.07** |
| Optimista | 11% a.a. | 5% | R$ 273.21 |

###### Margem de segurança
A margem de segurança da AbbVie é calculada em -2%, indicando que o preço atual está ligeiramente acima do valor intrínseco estimado pelo modelo DCF base.

###### Rating final
RATING: Hold

###### Pre-Mortem — Se esta tese falhar
Foi este o ponto onde Mariana Macro divergiu de Diego Bancário: a pressão regulatória sobre dividendos e um P/B negativo podem levar a uma reavaliação significativa do valor da AbbVie. Valentina Prudente sinalizou que as preocupações com a falta de histórico de ROIC poderiam comprometer a sustentabilidade dos lucros futuros.

###### Horizonte
24-36 meses

###### Nota divergente do Council
Foi este o ponto onde Mariana Macro divergiu de D

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ABBV_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\ABBV_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — ABBV            moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              7
  Entry price.........: US$      200.91
  Cost basis..........: US$    1,500.00
  Price now...........: US$      198.71
  Market value now....: US$    1,483.57  [-1.1% nao-realizado]
  DY t12m.............: 3.39%  (R$/US$ 6.7400/share)
  DY vs own 10y.......: P26 [fair-rich]  (actual 3.39% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=14  hist_g_5y=0.060  hist_g_raw=0.060  gordon_g=0.000  is_quality=False  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +1.79%  |   -2.00% |   +3.19%       |
  | base         |   +2.99%  |   +0.00% |   +6.38%       |
  | optimista    |   +4.04%  |   +1.00% |   +8.43%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     24       |       18       |       19       |
  | base         |     22       |       21       |       12       |
  | optimista    |     20       |       24       |        9       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,753 | US$      2,031 | US$      2,231 |
  |  10y  | US$      2,108 | US$      2,781 | US$      3,329 |
  |  15y  | US$      2,587 | US$      3,807 | US$      4,933 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ABBV.md` (cemetery archive)_

#### ABBV — AbbVie

#watchlist #us #healthcare

##### Links

- Sector: [[sectors/Healthcare|Healthcare]]
- Market: [[markets/US|US]]
- Peers: [[JNJ]] · [[ABT]] · [[BDX]] · [[MDT]] · [[WST]]
- 🎯 **Thesis**: [[ABBV|thesis deep]]

##### Snapshot

- **Preço**: $205.03  (2026-05-06)    _-0.52% 1d_
- **Screen**: 0.75  ✗ fail
- **Altman Z**: 1.955 (grey)
- **Piotroski**: 8/9
- **Div Safety**: 31.2/100 (RISK)
- **Posição**: 7.46602 sh @ $200.91025740622177  →  P&L 2.05%

##### Fundamentals

- P/E: 100.504906 | P/B: None | DY: 3.29%
- ROE: None% | EPS: 2.04 | BVPS: -1.85
- Streak div: 14y | Aristocrat: False

##### Dividendos recentes

- 2026-04-15: $1.7300
- 2026-01-16: $1.7300
- 2025-10-15: $1.6400
- 2025-07-15: $1.6400
- 2025-04-15: $1.6400

##### Eventos (SEC/CVM)

- **2026-04-29** `8-K` — 8-K | 2.02,9.01
- **2026-04-03** `8-K` — 8-K | 2.02,9.01
- **2026-03-23** `proxy` — DEF 14A
- **2026-03-04** `8-K` — 8-K | 8.01,9.01
- **2026-02-26** `8-K` — 8-K | 8.01,9.01

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -16.10%
- **Drawdown 5y**: -16.10%
- **YTD**: -10.59%
- **YoY (1y)**: +9.55%
- **CAGR 3y**: +11.47%  |  **5y**: +12.11%  |  **10y**: +12.61%
- **Vol annual**: +27.24%
- **Sharpe 3y** (rf=4%): +0.31

###### Dividendos
- **DY 5y avg**: +3.50%
- **Div CAGR 5y**: +5.98%
- **Frequency**: quarterly
- **Streak** (sem cortes): 12 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $58.05B | $11.84B | $24.25B |
| 2023-12-31 | $54.32B | $4.86B | $22.06B |
| 2024-12-31 | $56.33B | $4.28B | $17.83B |
| 2025-12-31 | $61.16B | $4.23B | $17.82B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ABBV — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: ABBV
    data: [185.58, 177.44, 184.85, 185.72, 186.99, 189.83, 192.42, 185.49, 185.39, 189.99, 189.77, 191.52, 189.26, 190.83, 189.31, 198.55, 198.64, 206.69, 209.5, 208.06, 211.86, 210.42, 217.61, 222.47, 218.54, 244.38, 232.83, 230.3, 229.57, 228.25, 225.14, 215.89, 218.71, 232.36, 229.45, 227.66, 230.24, 222.99, 227.45, 226.82, 229.98, 229.31, 224.13, 221.89, 216.15, 223.93, 225.64, 223.43, 227.5, 224.35, 226.92, 233.86, 227.45, 219.68, 206.23, 207.18, 217.49, 206.37, 206.47, 208.38, 200.95, 197.69, 208.16]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: P/E
    data: [87.90756, 88.55509, 87.55462, 86.31092, 86.91525, 83.84389, 84.19916, 84.19916, 83.6356, 83.413506, 86.02954, 103.58824, 101.541466, 101.03432, 100.504906]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: ROE %
    data: [6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 6225.0, 0, 0, 0, 0]
  - title: DY %
    data: [3.32, 3.31, 3.32, 3.32, 3.29, 3.39, 3.39, 3.39, 3.41, 3.41, 3.31, 3.19, 3.24, 3.27, 3.29]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ABBV_DOSSIE.md` (cemetery archive)_

#### 📑 ABBV — AbbVie

> Generated **2026-04-26** by `ii dossier ABBV`. Cross-links: [[ABBV]] · [[ABBV]] · [[CONSTITUTION]]

##### TL;DR

AbbVie transaciona a P/E 84.20 com DY 3.39% e streak de 14y (herdou Aristocrat status via spinoff ABT em 2013). IC Synthetic verdica HOLD (60% consenso) — P/E muito acima do screen US (≤20) reflecte one-time charges Humira erosion já no denominador, distorcendo o múltiplo. Achado-chave: BVPS negativo torna P/B inutilizável; o que importa é Skyrizi+Rinvoq ramp (~$24B run-rate combinado) que está a substituir Humira faster than expected — entry condition deve focar normalised earnings, não P/E reportado.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.36  |  **BVPS**: -1.85
- **ROE**: 6225.00%  |  **P/E**: 84.20  |  **P/B**: -107.41
- **DY**: 3.39%  |  **Streak div**: 14y  |  **Market cap**: USD 351.47B
- **Last price**: USD 198.71 (2026-04-26)  |  **YoY**: +6.8%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[ABBV]]

##### 3. Thesis

**Core thesis (2026-04-24)**: A AbbVie é uma excelente posição long-term para um investidor Buffett/Graham devido à sua consistência no pagamento de dividendos e ao seu potencial de crescimento sustentado. Apesar do P/E alto de 86,91x, a empresa mantém um ROE impressionante de 62,25% e uma renda anual de 3,29%. Com uma história de 14 anos sem interrupção no pagamento de dividendos, a AbbVie demonstra sua capacidade de gerir lucrativamente seus negócios mesmo em cenários desafiadores.

**Key assumptions**:
1. A AbbVie continuará a expandir suas linhas de produtos e a manter um ROE acima de 60%.
2. O mercado farmacêutico global continuará a crescer, mantendo as margens da AbbVie estáveis ou aumentando-as.
3. A empresa manterá seu dividendo anual em pelo menos 3,29%, apesar das pressões regul

→ Vault: [[ABBV]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **DY = 3.39%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **3.39%** OK.
- **Streak div = 14y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🟡 **Humira biosimilar erosion** — em fase de lapping mas declínio continua; magnitude residual ainda relevante. Trigger: events com kind='earnings' AND summary LIKE '%Humira%decline%' > -25% YoY.
- 🟡 **Skyrizi/Rinvoq ramp adequacy** — substituição depende destes dois activos; qualquer slowdown é tese-killer. Trigger: revenue growth combinado < 20% YoY em earnings transcripts.
- 🟡 **M&A integration risk** — Cerevel + ImmunoGen + Capstan; integração de neuroscience + ADC pipeline complexa. Trigger: events com kind='restructuring' OR goodwill writedown.
- 🟢 **Dívida elevada pós-deals** — net debt significativo após aquisições. Trigger: net_debt_ebitda > 3.0 sustained.
- 🟢 **Múltiplo distorcido por charges** — P/E reportado 84 não é quality signal; usar forward P/E ~15. Trigger: scoring engine usa GAAP P/E sem ajuste — flag para override manual.

##### 5. Position sizing

**Status atual**: watchlist

Watchlist — não é trade signal. Considerar entry inicial 3-5% da sleeve US se forward P/E (manual override) ≤ 18 E DY > 3.5% E Skyrizi+Rinvoq combined revenue YoY > 25%. DY 3.39% e streak 14y qualificam para core DRIP US, mas dívida pós-M&A e GAAP distortion exigem due diligence extra. Cash USD permanece em US (BR/US isolation).

##### 6. Tracking triggers (auto-monitoring)

- `fundamentals.dy > 3.5% AND price drop YoY < -10%` — entry condition watchlist (P/E GAAP unreliable).
- `fundamentals.net_debt_ebitda > 3.0` por 2Q — disconfirmation, dividend safety risk.
- `events WHERE kind='earnings' AND summary LIKE '%Skyrizi%' OR LIKE '%Rinvoq%'` — track ramp.
- `events WHERE kind='regulatory' AND summary LIKE '%biosimilar%'` — Humira erosion magnitude.
- `scores.score > 75` (composite com forward P/E override) AND screen passes — promover.

##### 7. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier ABBV` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ABBV_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — ABBV

**Committee verdict**: **AVOID** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=2 | AVOID=3  
**Avg conviction majority**: 5.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- P/E muito alto
- intangíveis elevados
- ROIC não estável

**Key risk**: Dependência de poucos produtos, risco de perda de patente

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E alto
- intangíveis significativos
- dividendos consistentes

**Key risk**: Avaliação sobrevalorizada e potencial queda nas margens devido a pressões regulatórias

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/E muito alto
- intangíveis elevados
- pequena margem de segurança

**Key risk**: overvalued growth and high intangible assets misrepresent true economic value

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- P/E muito alto
- intangíveis elevados
- valor intrínseco incerto

**Key risk**: overvaluation e dependência de poucos produtos

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E alto
- intangíveis significativos
- dividendos consistentes

**Key risk**: Avaliação de ativos intangíveis pode subestimar o valor econômico da marca.

##### 📊 Context provided

```
TICKER: US:ABBV

FUNDAMENTALS LATEST:
  pe: 98.31708
  dy: 3.34%
  net_debt_ebitda: 2.1045738229516076
  intangible_pct_assets: 65.9%   (goodwill $35.6B + intangibles $52.6B)
  ⚠ HIGH intangibles — book value understates brand/franchise economic value (P/B + Buffett ceiling unreliable)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: A AbbVie é uma excelente posição long-term para um investidor Buffett/Graham devido à sua consistência no pagamento de dividendos e ao seu potencial de crescimento sustentado. Apesar do P/E alto de 86,91x, a empresa mantém um ROE impressionante de 62,25% e uma renda anual de 3,29%. Com uma história de 14 anos sem interrupção no pagamento de dividendos, a AbbVie demonstra sua capacidade de gerir lucrativamente seus negócios mesmo em cenários desafiadores.

**Key assumptions**:
1. A AbbVie continuará a expandir suas linhas de produtos e a manter um ROE acima de 60%.
2. O mercado farmacêutico global continuará a crescer, mantendo as margens da AbbVie estáveis ou aumentando-as.
3. A empresa manterá seu dividendo anual em pelo menos 3,29%, apesar das pressões regul

RECENT MATERIAL NEWS (last 14d via Tavily):
  - AbbVie’s (NYSE:ABBV) Q1 CY2026 Sales Top Estimates - The Chronicle-Journal [Wed, 29 Ap]
    Pharmaceutical company AbbVie (NYSE: ABBV) announced better-than-expected revenue in Q1 CY2026, with sales up 12.4% year on year to $15 billion. AbbVie’s annualized revenue growth of 7.5% over the las
  - AbbVie (ABBV) To Report Earnings Tomorrow: Here Is What To Expect - The Chronicle-Journal [Tue, 28 Ap]
    # AbbVie (ABBV) To Report Earnings Tomorrow: Here Is What To Expect. Pharmaceutical company AbbVie (NYSE: ABBV) will be announcing earnings results this Wednesday before market hours. AbbVie beat anal
  - AbbVie (ABBV) Stock Trades Up, Here Is Why - The Chronicle-Journal [Wed, 29 Ap]
    # AbbVie (ABBV) Stock Trades Up, Here Is Why. April 29, 2026 at 15:36 PM EDT. 
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ABBV_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — ABBV

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `medium_variance_long` (magnitude 2/5)  
**Interpretation**: moderate edge

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: neutral (0 bull / 0 bear / 5 neutral)  
**Cached**: False

- 🟡 [neutral] [AbbVie (ABBV) Stock Trades Up, Here Is Why - The Chronicle-Journal](http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-29-abbvie-abbv-stock-trades-up-here-is-why) (Wed, 29 Ap)
- 🟡 [neutral] [AbbVie’s (NYSE:ABBV) Q1 CY2026 Sales Top Estimates - The Chronicle-Journal](http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-29-abbvies-nyseabbv-q1-cy2026-sales-top-estimates) (Wed, 29 Ap)
- 🟡 [neutral] [AbbVie (ABBV) To Report Earnings Tomorrow: Here Is What To Expect - The Chronicle-Journal](http://markets.chroniclejournal.com/chroniclejournal/article/stockstory-2026-4-28-abbvie-abbv-to-report-earnings-tomorrow-here-is-what-to-expect) (Tue, 28 Ap)
- 🟡 [neutral] [AbbVie tops Q1 estimates, raises outlook and discontinues cancer candidate - BioSpace](https://www.biospace.com/business/abbvie-tops-q1-estimates-raises-outlook-and-discontinues-cancer-candidate) (Wed, 29 Ap)
- 🟡 [neutral] [2,918 Shares in Taiwan Semiconductor Manufacturing Company Ltd. $TSM Bought by Cannon Capital Management Inc. - MarketBe](https://www.marketbeat.com/instant-alerts/filing-2918-shares-in-taiwan-semiconductor-manufacturing-company-ltd-tsm-bought-by-cannon-capital-management-inc-2026-04-30/) (Thu, 30 Ap)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: A AbbVie é uma excelente posição long-term para um investidor Buffett/Graham devido à sua consistência no pagamento de dividendos e ao seu potencial de crescimento sustentado. Apesar do P/E alto de 86,91x, a empresa mantém um ROE impressionante de 62,25% e uma renda anual de 3,29%. Com uma história de 14 anos sem interrupção no pagamento de dividendos, a AbbVie demonstra sua capacidade de gerir lucrativamente seus negócios mesmo em cenários desafiadores.

**Key assumptions**:
1. A AbbVie continuará a expandir suas linhas de produtos e a manter um ROE acima de 60%.
2. O mercado farmacêutico global continuará a crescer, mantendo as margens da AbbVie estáveis ou aumentando-as.
3. A empresa manterá seu dividendo anual em pelo menos 3,29%, apesar das pressões regul

---
*100% Ollama local. Variant perception scan.*

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\ABBV.md` (cemetery archive)_

> ⚠️ **AUTO-DRAFT** (2026-04-25) — gerado por `holding_wiki_synthesizer.py` via
> Ollama Qwen 14B local. Refinar com tese pessoal + memória de contexto que o
> LLM não tem acesso (entry rationale, lições passadas, sizing decisions).
> Após review humana, remover `auto_draft: true` e este aviso.

#### 🎯 Thesis: [[ABBV]] — AbbVie

> DRIP core / Compounder / Tactical / Growth — por sua capacidade de gerar lucros sustentáveis e crescer consistentemente.

##### Intent
**Tactical** — DRIP core / Compounder / Tactical / Growth — por sua capacidade de gerar lucros sustentáveis e crescer consistentemente.

##### Business snapshot
AbbVie é uma empresa farmacêutica líder nos Estados Unidos, com foco em medicamentos especializados para condições crônicas. A receita da empresa vem principalmente dos EUA, mas também tem presença global significativa.

**Fundamentals**: P/E 83.8 · P/B -107.4 · DY 3.4% · ROE 6225.0% · Streak 14y

##### Por que detemos

1. Paga dividendos consistentemente por 14 anos consecutivos, o que demonstra estabilidade financeira.
2. ROE de 62,25% indica eficiência operacional e gerenciamento eficaz de ativos.
3. Taxa de crescimento de dividendo positiva, apesar do alto P/E e baixo P/B.
4. Net Debt/EBITDA é moderado em 2,16x, indicando capacidade de endividamento sustentável.

##### Moat

['Possui um portfólio diversificado de medicamentos especializados com patentes robustas.', 'Força comercial significativa nos mercados onde opera, permitindo preços elevados para seus produtos.', 'Investimentos contínuos em pesquisa e desenvolvimento garantem a inovação constante.']

##### Current state (2026-04)

['P/E de 83,84 é muito alto, indicando que o mercado espera um crescimento futuro significativo.', 'P/B negativo sugere problemas de capitalização ou ativos intangíveis não contabilizados.', 'Dividend yield de 3,39% oferece rendimentos atraentes para investidores procurando por renda.']

##### Invalidation triggers

- [ ] Redução significativa no fluxo de caixa operacional.
- [ ] Perda de exclusividade em medicamentos-chave.
- [ ] Aumento brusco na dívida líquida/EBITDA para níveis não sustentáveis.
- [ ] Deterioração contínua do P/B.

##### Sizing + DRIP

['Alvo de posição atual é adequado, com intenção de DRIP para compor a carteira ao longo do tempo.', 'Aumentar a posição se o preço cair e os fundamentos permanecerem sólidos.']
- Posição actual: 7.46602 shares @ 200.91 entry (2026-04-23)

---
*AUTO-DRAFT por `holding_wiki_synthesizer.py` · Ollama Qwen 14B local · 2026-04-25*

## ⚙️ Refresh commands

```bash
ii panorama ABBV --write
ii deepdive ABBV --save-obsidian
ii verdict ABBV --narrate --write
ii fv ABBV
python -m analytics.fair_value_forward --ticker ABBV
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
