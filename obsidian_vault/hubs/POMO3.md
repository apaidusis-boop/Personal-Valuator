---
type: ticker_hub
ticker: POMO3
market: br
sector: Industrials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 11
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# POMO3 — Marcopolo ON

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Industrials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `11 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `WATCH` (score 6.97, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 5.71 · P/B 1.85 · DY 16.5% · ROE 31.0% · ND/EBITDA 0.99 · Dividend streak 19

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\POMO3.md` (now in cemetery)_

#### POMO3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.marcopolo.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.920000076293945
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.30973 · DY=0.1594748290258507 · P/E=5.92
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
_source: `dossiers\POMO3_FILING_2026-05-05.md` (now in cemetery)_

#### Filing dossier — [[POMO3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515775&numSequencia=1040481&numVersao=1>

##### 🎯 Acção sugerida

###### 🟢 **BUY** &mdash; preço 5.87

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
| 2026-05-13T18:35:07+00:00 | `graham_number` | 8.34 | 6.09 | 5.87 | BUY | single_source | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 8.34 | 6.09 | 6.00 | BUY | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 8.34 | 6.09 | 6.00 | BUY | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 8.34 | 6.09 | 6.00 | BUY | single_source | `extend_2026-05-09` |
| 2026-05-08T19:20:59+00:00 | `graham_number` | 8.34 | 6.09 | 6.01 | BUY | single_source | `filing:cvm:fato_relevante:2026-04-15` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Council review · Mariana Macro
_source: `agents\Mariana Macro\reviews\POMO3_2026-04-30.md` (now in cemetery)_

#### Mariana Macro sobre [[POMO3_STORY|POMO3]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _POMO3 apresenta DY atraente e ROE forte_

A empresa oferece um dividendo anual de 15.9% (DY) e um ROE de 31%, superando significativamente as médias do setor.

**Métricas que invoquei**:
- DY=15.9%
- ROE=31.0%
- P/B=2.08

**Preocupações**:
- P/E ligeiramente elevado em relação ao setor
- ND/EBITDA próximo da média do setor

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.
- Tião Galpão

**Desafiei**:
- P/B de 2,08x está acima da mediana setorial (1,35x)
- A alta relação P/B pode indicar que a empresa já foi precificada pelo mercado ou que há preocupações sobre o valor contábil do ativo. É importante investigar se os fundamentos financeiros sustentam essa avaliação.
- Tião Galpão

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[POMO3_STORY|📖 Storytelling completo (8 actos)]]
- [[POMO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `agents\Pedro Alocação\reviews\POMO3_2026-04-30.md` (now in cemetery)_

#### Pedro Alocação sobre [[POMO3_STORY|POMO3]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _POMO3 apresenta DY atraente e ROE forte_

DY de 15.9% e ROE de 31.0% superam setor, mas P/E de 6.57x é baixo comparado à média do setor (19.43x)

**Métricas que invoquei**:
- P/E=6.57
- DY=15.9%
- ROE=31.0%

**Preocupações**:
- P/B de 2.08x acima da média do setor (1.35x)
- ND/EBITDA próximo a 1, sugerindo margem estreita

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização. - Tião Galpão

**Desafiei**:
- P/B de 2,08x está acima da mediana setorial (1,35x) | Falta de informações relevantes sobre o impacto macroeconômico na empresa - Tião Galpão | Ainda que o P/B esteja elevado, é importante notar que a companhia tem um histórico sólido de geração de caixa e retorno aos acionistas, indicando que o valor pode ser sustentável

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[POMO3_STORY|📖 Storytelling completo (8 actos)]]
- [[POMO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Tião Galpão
_source: `agents\Tião Galpão\reviews\POMO3_2026-04-30.md` (now in cemetery)_

#### Tião Galpão sobre [[POMO3_STORY|POMO3]]

**Função no debate**: Industrials & Consumer BR Specialist (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _POMO3 apresenta ROE elevado e DY atrativo_

ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.

**Métricas que invoquei**:
- P/E=6.57
- ND/EBITDA=0.99x
- DivStreak=19y

**Preocupações**:
- P/B de 2,08x está acima da mediana setorial (1,35x)
- Falta de informações relevantes sobre o impacto macroeconômico na empresa

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Mariana Macro

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[POMO3_STORY|📖 Storytelling completo (8 actos)]]
- [[POMO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Tião Galpão|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `agents\Valentina Prudente\reviews\POMO3_2026-04-30.md` (now in cemetery)_

#### Valentina Prudente sobre [[POMO3_STORY|POMO3]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _POMO3 apresenta DY atraente e indicadores financeiros sólidos_

A empresa oferece um dividendo anual de 15.9%, com ROE de 31% e P/B de 2.08, sugerindo valorização potencial.

**Métricas que invoquei**:
- DY=15.9%
- ROE=31.0%
- Piotroski F-Score: 6/9

**Preocupações**:
- P/E baixo em comparação com o setor
- P/B acima da média do setor

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.
- Tião Galpão

**Desafiei**:
- P/B de 2,08x está acima da mediana setorial (1,35x) | Falta de informações relevantes sobre o impacto macroeconômico na empresa
- Informações limitadas sobre o impacto macroeconômico podem não refletir completamente os riscos associados à posição. É necessário mais detalhamento para avaliar a exposição da empresa a fatores econômicos.
- Tião Galpão

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[POMO3_STORY|📖 Storytelling completo (8 actos)]]
- [[POMO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-15 · Filing 2026-04-15
_source: `dossiers\POMO3_FILING_2026-04-15.md` (now in cemetery)_

#### Filing dossier — [[POMO3]] · 2026-04-15

**Trigger**: `cvm:fato_relevante` no dia `2026-04-15`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505167&numSequencia=1029873&numVersao=1>

##### 🎯 Acção sugerida

###### 🟢 **BUY** &mdash; preço 6.01

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
| 2026-05-08T19:20:59+00:00 | `graham_number` | 8.34 | 6.09 | 6.01 | BUY | single_source | `filing:cvm:fato_relevante:2026-04-15` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Council aggregate
_source: `dossiers\POMO3_COUNCIL.md` (now in cemetery)_

#### Council Debate — [[POMO3_STORY|POMO3]] (POMO3)

**Final stance**: 🟢 **BUY**  
**Confidence**: `high`  
**Modo (auto)**: A (BR)  |  **Sector**: Industrials  |  **Held**: não  
**Elapsed**: 61.4s  |  **Failures**: 0

##### Quem esteve na sala

- [[Tião Galpão]] — _Industrials & Consumer BR Specialist_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- ROE de 31% supera significativamente a média setorial (5,2%).
- Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.

**Dissenso (preservado)**:
- Mariana Macro disse que o P/B de 2,08x está acima da média setorial (1,35x), Tião Galpão concordou.
- Valentina Prudente mencionou a falta de informações relevantes sobre o impacto macroeconômico na empresa, Tião Galpão concordou.

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ P/B acima da média do setor
- ⚠️ Falta de informações relevantes sobre o impacto macroeconômico

**Sizing**: Alocar entre 2% e 3% do portfólio, considerando os riscos mencionados.

##### Round 1 — Opening Statements (blind)

###### [[Tião Galpão]] — 🟢 **BUY**
_Industrials & Consumer BR Specialist_

**Headline**: _POMO3 apresenta ROE elevado e DY atrativo_

ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.

**Métricas**:
- P/E=6.57
- ND/EBITDA=0.99x
- DivStreak=19y

**Preocupações**:
- P/B de 2,08x está acima da mediana setorial (1,35x)
- Falta de informações relevantes sobre o impacto macroeconômico na empresa

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _POMO3 apresenta DY atraente e ROE forte_

A empresa oferece um dividendo anual de 15.9% (DY) e um ROE de 31%, superando significativamente as médias do setor.

**Métricas**:
- DY=15.9%
- ROE=31.0%
- P/B=2.08

**Preocupações**:
- P/E ligeiramente elevado em relação ao setor
- ND/EBITDA próximo da média do setor

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _POMO3 apresenta DY atraente e indicadores financeiros sólidos_

A empresa oferece um dividendo anual de 15.9%, com ROE de 31% e P/B de 2.08, sugerindo valorização potencial.

**Métricas**:
- DY=15.9%
- ROE=31.0%
- Piotroski F-Score: 6/9

**Preocupações**:
- P/E baixo em comparação com o setor
- P/B acima da média do setor

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _POMO3 apresenta DY atraente e ROE forte_

DY de 15.9% e ROE de 31.0% superam setor, mas P/E de 6.57x é baixo comparado à média do setor (19.43x)

**Métricas**:
- P/E=6.57
- DY=15.9%
- ROE=31.0%

**Preocupações**:
- P/B de 2.08x acima da média do setor (1.35x)
- ND/EBITDA próximo a 1, sugerindo margem estreita

##### Round 2 — Respostas (peers visíveis)

###### [[Tião Galpão]] — 🟢 **BUY**
_Industrials & Consumer BR Specialist_

**Concordou com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Mariana Macro

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.
- Tião Galpão

**Desafiou**:
- P/B de 2,08x está acima da mediana setorial (1,35x)
- A alta relação P/B pode indicar que a empresa já foi precificada pelo mercado ou que há preocupações sobre o valor contábil do ativo. É importante investigar se os fundamentos financeiros sustentam essa avaliação.
- Tião Galpão

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização.
- Tião Galpão

**Desafiou**:
- P/B de 2,08x está acima da mediana setorial (1,35x) | Falta de informações relevantes sobre o impacto macroeconômico na empresa
- Informações limitadas sobre o impacto macroeconômico podem não refletir completamente os riscos associados à posição. É necessário mais detalhamento para avaliar a exposição da empresa a fatores econômicos.
- Tião Galpão

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- ROE de 31% supera significativamente a média setorial (5,2%). Dividend yield de 15,9% é muito acima da mediana do setor (3%) e sugere valorização. - Tião Galpão

**Desafiou**:
- P/B de 2,08x está acima da mediana setorial (1,35x) | Falta de informações relevantes sobre o impacto macroeconômico na empresa - Tião Galpão | Ainda que o P/B esteja elevado, é importante notar que a companhia tem um histórico sólido de geração de caixa e retorno aos acionistas, indicando que o valor pode ser sustentável

##### Documentos relacionados

- [[POMO3_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[POMO3_2026-04-30|Tião Galpão]] em [[Tião Galpão]]/reviews/
  - [[POMO3_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[POMO3_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[POMO3_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: BR:POMO3 — POMO3 ===
Sector: Industrials  |  Modo (auto): A  |  Held: False
Last price: 6.440000057220459 (2026-04-30)
Fundamentals: P/E=6.57 | P/B=2.08 | DY=15.9% | ROE=31.0% | ND/EBITDA=0.99 | DivStreak=19.00

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  Sector weight: 0.0%

QUALITY SCORES:
  Piotroski F-Score: 6/9 (2025-12-31)
  Altman Z-Score: 3.27  zone=safe  conf=medium
    note: X2 usa stockholders_equity (retained_earnings missing) — conservative proxy
  Beneish M-Score: -2.58  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Popular Supplement May Be Helping Cancer Survive, Scientists Warn - Newsweek [Wed, 08 Ap]
    Vitamin B3, however, might have a surprising side effect: According to researchers at Case Western Reserve School, the popular supplement could also help cancer survive. The researchers found that pancreatic cancer cells can use derivatives
  - Popular Vitamin B3 Supplements May Help Cancer Cells Survive, Scientists Warn - SciTechDaily [Sat, 04 Ap]
    **A new study raises important questions about widely used NAD+ supplements, suggesting that compounds often taken to boost energy and support healthy aging may have unintended consequences in cancer treatment.**. A study from Case Western 
  - Petrobras takes FID on SEAP FPSO development in Brazil basin - World Oil [Tue, 14 Ap]
    World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petrobras takes FID on SEAP FPSO development in Brazil basin. (WO) — **
  - Brazil finance minister readies run for Sao Paulo governor - TradingView [Thu, 19 Ma]
    * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 gr
  - Top 6 Defence Stocks with Strong Growth Guidance for FY26 to Keep an Eye On - Trade Brains [Sat, 14 Ma]
    > ***Synopsis: Several defence stocks are in focus for FY26, backed by strong order books, robust revenue growth guidance, and strategic expansion in domestic defence production, modernisation initiatives, and high-value aerospace and elect
  - Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround - InternetRetailing [Tue, 31 Ma]
    You are in: Home » Marketplaces » **Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround**. # Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround. The Group’s trading statement for 

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### ANALYST INSIGHTS (subscriptions BTG/XP/Suno) (1 hits)
[1] xp [2026-04-24] (bull): [BTG Portfolio Dividendos] POMO4 — peso 9.6%, setor Industrials

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[2] cvm (fato_relevante) [2026-04-15]: Pagamento de Juros Sobre o Capital Próprio
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505167&numSequencia=1029873&numVersao=1
[3] cvm (fato_relevante) [2026-04-15]: Pagamento de Juros Sobre o Capital Próprio
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505167&numSequencia=1029873&numVersao=1
[4] cvm (fato_relevante) [2026-03-24]: Alteração dos portais de publicação
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1494409&numSequencia=1019115&numVersao=1
[5] cvm (fato_relevante) [2026-03-24]: Alteração dos portais de publicação
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1494409&numSequencia=1019115&numVersao=1
[6] cvm (comunicado) [2026-03-03]: Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | Declaração de Aquisição de Participação Acionária Relevante - Art.12 da Instrução CVM nº358/02
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1484369&numSequencia=1009075&numVersao=1
[7] cvm (comunicado) [2026-03-03]: Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | Declaração de Aquisição de Participação Acionária Relevante - Art.12 da Instrução CVM nº358/02
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1484369&numSequencia=1009075&numVersao=1

##### TAVILY NEWS (≤30d) (5 hits)
[8] Tavily [Wed, 08 Ap]: Vitamin B3, however, might have a surprising side effect: According to researchers at Case Western Reserve School, the popular supplement could also help cancer survive. The researchers found that pancreatic cancer cells can use derivatives of vitamin B3 to survive treatment that might have otherwis
     URL: https://www.newsweek.com/popular-supplement-help-cancer-survive-11798948
[9] Tavily [Sat, 04 Ap]: **A new study raises important questions about widely used NAD+ supplements, suggesting that compounds often taken to boost energy and support healthy aging may have unintended consequences in cancer treatment.**. A study from Case Western Reserve University’s School of Medicine, published in *Cance
     URL: https://scitechdaily.com/popular-vitamin-b3-supplements-may-help-cancer-cells-survive-scientists-warn/
[10] Tavily [Tue, 14 Ap]: World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petrobras takes FID on SEAP FPSO development in Brazil basin. (WO) — **Petrobras** has approved the final investment decision (FID)
     URL: https://www.worldoil.com/news/2026/4/14/petrobras-takes-fid-on-seap-fpso-development-in-brazil-basin/
[11] Tavily [Mon, 02 Ma]: # Petro-Victory spuds SJ-12 gas well at São João field, Brazil. (WO) - **Petro-Victory Energy Corp.** has commenced drilling operations on the SJ-12 well at its 100%-owned São João field in Brazil’s Barreirinhas basin, Maranhão state. According to the company, drilling and testing of SJ-12 are inten
     URL: https://worldoil.com/news/2026/3/2/petro-victory-spuds-sj-12-gas-well-at-sao-joao-field-brazil/
[12] Tavily [Thu, 16 Ap]: World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petrobras board vote comes amid oil price surge, fuel policy pressure in Brazil. (Bloomberg) – Petroleo Brasileiro SA investors wil
     URL: https://worldoil.com/news/2026/4/16/petrobras-board-vote-comes-amid-oil-price-surge-fuel-policy-pressure-in-brazil/

##### TAVILY GUIDANCE (≤90d) (5 hits)
[13] Tavily [Thu, 19 Ma]: * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 growth. * Image 7 Quartr IMP: Strong PGM prices, ESG leadershi
     URL: https://www.tradingview.com/news/reuters.com,2026:newsml_L1N4061A6:0-brazil-finance-minister-readies-run-for-sao-paulo-governor/
[14] Tavily [Sat, 14 Ma]: > ***Synopsis: Several defence stocks are in focus for FY26, backed by strong order books, robust revenue growth guidance, and strategic expansion in domestic defence production, modernisation initiatives, and high-value aerospace and electronics segments.***. For FY26, the company maintains revenue
     URL: https://tradebrains.in/top-6-defence-stocks-with-strong-growth-guidance-for-fy26-to-keep-an-eye-on/
[15] Tavily [Tue, 31 Ma]: You are in: Home » Marketplaces » **Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround**. # Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround. The Group’s trading statement for the financial year ending 28 February 2026 shows £53m in adj
     URL: https://internetretailing.net/debenhams-group-smashes-fy26-guidance-as-marketplace-model-accelerates-turnaround/
[16] Tavily [Thu, 26 Ma]: You are in: Home » News » **Record second half sees THG return to growth and strengthen FY26 guidance**. # Record second half sees THG return to growth and strengthen FY26 guidance. THG delivered a strong FY25 performance that saw it return to growth after a shaky H1, with a record H2 and renewed mo
     URL: https://internetretailing.net/record-second-half-sees-thg-return-to-growth-and-strengthen-fy26-guidance/
[17] Tavily [Thu, 23 Ap]: |  | Q1 2026 and 2025 adjusted earnings from continuing operations exclude after-tax purchase accounting expenses, restructuring and other costs, and gain on dispositions. Adjusted earnings from continuing operations, adjusted diluted earnings per share from continuing operations, total segment earn
     URL: https://markets.ft.com/data/announce/detail?dockey=600-202604230655PR_NEWS_USPRX____NY41627-1

##### TAVILY INSIDER/SHORT/SCANDAL (5 hits)
[18] Tavily [Tue, 17 Fe]: # **HUBG Investors Have Opportunity to Join Hub Group, Inc. Fraud Investigation with the Schall Law Firm**. LOS ANGELES--(BUSINESS WIRE)--The Schall Law Firm, a national shareholder rights litigation firm, announces that it is investigating claims on behalf of investors of Hub Group, Inc. HUBG Inves
     URL: https://www.businesswire.com/news/home/20260216168257/en/HUBG-Investors-

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\POMO3_COUNCIL.md`)_

#### — · Story
_source: `dossiers\POMO3_STORY.md` (now in cemetery)_

#### POMO3 — POMO3

##### Análise de Investimento · Modo FULL · Jurisdição BR

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-BR sob a Jurisdição BR.**

---

##### Quem analisou este ticker

- [[Tião Galpão]] — _Industrials & Consumer BR Specialist_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/POMO3_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 9.1 bi · EBITDA est. R$ 1.94 bi · FCF R$ 1.12 bi · ROE 31% · DGR 75.4% a.a. (DGR limpo de extraordinária) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 6/9 · Altman Z=3.27 (safe) · Beneish M=-2.58 (clean) |
| **5 — Classification** | Modo A-BR · Buffett/Quality (7/12) · Value (6/12) |
| **5.5 — Council Debate** | AVOID (medium) · 1 dissent · 1 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-BR sob a Jurisdição BR. POMO3, com ticker POMO3 e pertencente ao sector Industrials, é uma empresa cuja identificação precisa requer um exame cuidadoso dos dados disponíveis sem suposições adicionais. Segundo o briefing analítico da XP, o papel de POMO4 no portfólio BTG Portfolio Dividendos destaca a relevância desta companhia no setor industriais, embora detalhes específicos sobre sua atividade operacional não estejam disponíveis nas informações fornecidas.

Uma armadilha comum ao discutir empresas deste tipo é confundir o produto ou serviço que oferecem com o modelo de negócio subjacente. É crucial distinguir entre a oferta de produtos e serviços da empresa e as estratégias comerciais e operacionais que sustentam sua posição no mercado.

A análise não fornece detalhes sobre o posicionamento competitivo específico de POMO3, mas dados do sector indicam uma tendência para empresas industriais em expansão estratégica e investimentos significativos. A falta de informações específicas sobre a empresa limita a capacidade de avaliar seu papel no mercado industrial brasileiro.

##### Ato 2 — O Contexto

A macroeconomia brasileira, como refletida nos dados atualizados do Banco Central do Brasil (BCB), apresenta uma taxa Selic de 13.75% em abril de 2026, com sinais emergentes de um possível afrouxamento monetário no segundo semestre desse ano, dependendo da evolução do IPCA e das contas públicas. O câmbio BRL/USD oscila na faixa entre R$5.80 e R$6.00, enquanto o custo de capital próprio (Ke) é estimado em cerca de 18%, refletindo um prêmio adicional de 4.5% sobre a taxa Selic.

Para empresas industriais como POMO3, essas condições macroeconômicas têm implicações significativas. A taxa de juros real oferecida pelo Tesouro IPCA+ 2035 está na faixa dos 6-7%, o que sugere um ambiente desafiador para financiamento e investimento em comparação com rendimentos alternativos disponíveis no mercado.

No contexto específico do sector industriais, a tendência de expansão estratégica e investimentos significativos continua sendo uma característica predominante. No entanto, as condições macroeconômicas atuais podem desencorajar ou restringir tais iniciativas, especialmente se o custo do capital permanecer elevado.

Não foram identificadas mudanças regulatórias específicas que afetem diretamente POMO3 nas informações fornecidas. No entanto, a evolução da política monetária e cambial continua sendo um fator crucial para determinar as condições de financiamento e crescimento futuras para empresas industriais no Brasil.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela um crescimento sólido e sustentável. O desempenho financeiro, conforme apresentado na tabela abaixo, demonstra uma trajetória ascendente em vários indicadores-chave.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 5.42B | R$ 0.55B | R$ 0.61B | 11.2% | R$ 0.45B | 8.3% | R$ -0.05B |
| 2023 | R$ 6.68B | R$ 1.00B | R$ 1.10B | 16.4% | R$ 0.82B | 12.2% | R$ 0.91B |
| 2024 | R$ 8.59B | R$ 1.67B | R$ 1.84B | 21.4% | R$ 1.20B | 14.0% | R$ 0.90B |
| 2025 | R$ 9.06B | R$ 1.76B | R$ 1.94B | 21.4% | R$ 1.22B | 13.5% | R$ 1.12B |

A receita da empresa cresceu a uma taxa composta anual (CAGR) de aproximadamente 20,7% entre 2022 e 2025. Este crescimento robusto reflete tanto o aumento do volume de negócios quanto a eficiência operacional, como evidenciado pela expansão da margem EBITDA de 11,2% em 2022 para 21,4% em 2025.

A empresa também melhorou significativamente seu fluxo de caixa livre (FCF), passando de um déficit de R$ -0.05B em 2022 para um superávit de R$ 1.12B em 2025, o que indica uma gestão financeira cada vez mais eficaz e a capacidade crescente da empresa de gerar caixa livre após investimentos necessários.

A tabela abaixo ilustra os dividendos pagos pela empresa ao longo dos anos:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 0.015 |
| 2021 | 0.081 |
| 2022 | 0.108 |
| 2023 | 0.252 |
| 2024 | 0.502 |
| 2025 | 1.145 |
| 2026 | 0.085 |

O crescimento dos dividendos, com um DGR (Dividend Growth Rate) de 75,4% ao ano, é uma indicação clara da capacidade da empresa de gerar lucros e distribuir retornos aos acionistas. No entanto, o significativo salto no dividendo em 2025 sugere a possibilidade de dividendos extraordinários ou ajustes contábeis que não refletem uma tendência estrutural.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A empresa tem demonstrado consistência na geração de caixa livre, um indicador mais confiável da saúde financeira do que o lucro líquido.

##### Ato 4 — O Balanço

O balanço da empresa apresenta uma série de métricas importantes para avaliar a solidez e a sustentabilidade financeira. Com um P/E (Preço sobre Lucro) de 6,57 e um P/B (Preço sobre Patrimônio Líquido) de 2,08, a empresa parece estar sendo negociada em múltiplos relativamente baixos comparados com as médias do setor.

A taxa de dividend yield (DY) da empresa é de 15,86%, um indicador atrativo para investidores em busca de rendimentos. O ROE (Return on Equity), que mede a eficiência na geração de lucros por parte dos acionistas, está em 30,97%. Este valor supera o custo do capital próprio (Ke) estimado no Brasil de aproximadamente 18,25%, indicando que a empresa cria valor para seus acionistas.

A relação Net Debt/EBITDA é calculada como R$ 1.88B / R$ 1.94B = 0,97x, um nível considerado saudável e que sugere uma boa capacidade de endividamento. No entanto, o Current Ratio (relação entre ativos circulantes e passivos circulantes) não foi fornecido, sendo necessário para uma análise mais detalhada da liquidez.

O ponto de atenção reside no fato de a empresa ter um histórico de distribuição de dividendos extraordinários, o que pode indicar alguma volatilidade na geração de caixa ou na gestão do endividamento. No entanto, com um DGR consistente e uma trajetória crescente em termos de FCF, os riscos parecem mitigados.

Em resumo, a empresa apresenta um perfil financeiro sólido, com indicadores que sugerem tanto valorização intrínseca como potencial para distribuição de dividendos sustentável.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa POMO3 revela uma posição distintiva em relação à sua base de comparação, que inclui peers setoriais e índices como o Ibov e S&P. Com um preço-earnings (P/E) de 6.57x, a companhia apresenta-se significativamente mais barata do que tanto seus pares setoriais quanto os índices de referência, cujas médias são respectivamente de 19.43x e 9.00x. Esta diferença é ainda mais evidente quando consideramos o múltiplo preço-benefício (P/B), com POMO3 cotada a um valor de 2.08x contra uma mediana setorial de 1.35x e índice de 1.60x.

A rendibilidade do dividendo (DY) da empresa é notável, atingindo 15.86%, muito acima tanto dos peers quanto dos índices de referência, que registram médias de 3% e 6%. Este DY elevado pode ser um indicador de uma política de distribuição de dividendos robusta ou de uma situação temporária de baixo preço das ações.

Quando avaliamos o fluxo de caixa livre (FCF) em relação ao valor de mercado, o FCF Yield da POMO3 é de 13.7%, bem acima dos níveis médios setoriais e do índice, que são de aproximadamente 5%. Este indicador sugere uma geração de caixa muito sólida comparativamente.

A margem de lucro antes de juros, impostos, depreciação e amortização (EBITDA) estimada para o último ano foi de R$ 1.94 bilhão, com um fluxo de caixa livre (FCF) de R$ 1.12 bilhão e uma receita total de R$ 9.06 bilhões.

A relação entre a dívida neta e o EBITDA da empresa é de 0.99x, significativamente mais baixa do que os valores médios setoriais (3.55x), indicando um perfil de endividamento controlado em comparação com seus pares.

| Múltiplo | POMO3 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 6.57x | 19.43x | 9.00x |
| P/B | 2.08x | 1.35x | 1.60x |
| DY | 15.9% | 3.0% | 6.0% |
| FCF Yield | 13.7% | 5.0% | 5.0% |
| ROE | 31.0% | 5.2% | 13.0% |
| ND/EBITDA | 0.99x | 3.55x | — |

A relação entre o retorno sobre o patrimônio líquido (ROE) da empresa é de 30.97%, muito acima tanto dos peers quanto do índice, que registram médias de 5.2% e 13.0%. Este indicador reflete uma eficiência operacional significativamente superior em relação ao capital próprio investido.

##### Ato 6 — Os Quality Scores

A avaliação da qualidade financeira da POMO3 através dos scores de qualidade revela um quadro robusto, embora com algumas nuances importantes. O score F-Score de Piotroski é de 6/9, indicando uma empresa que está em boa forma operacional e financeira, com seis critérios aprovados nos últimos três anos.

O Z-Score de Altman para a empresa é de 3.27, classificado como "safe", embora tenha sido calculado usando um proxy conservador (stockholders_equity) devido à falta de dados específicos sobre retained earnings. Este score sugere que a empresa está em uma situação financeira sólida e está longe do risco de insolvência.

O M-Score de Beneish é -2.58, indicando um baixo risco de manipulação contábil ("clean"), com alta confiança no resultado. Este score sugere que a empresa mantém práticas contábeis transparentes e não há indícios de manipulações financeiras.

Em resumo, os scores sugerem uma empresa em boa saúde operacional e financeira, embora seja necessário manter um olhar atento às limitações dos dados disponíveis para o cálculo do Z-Score.

---

##### Ato 7 — O Moat e a Gestão

O moat da empresa em questão é classificado como **Narrow**, refletindo um conjunto de características que oferecem uma vantagem competitiva, mas não são suficientemente robustas para proteger contra ameaças duradouras. Este moat se baseia principalmente na eficiência operacional e no histórico de gestão sólida.

###### Eficiência Operacional
A empresa demonstra um forte ROE (Retorno sobre o Patrimônio Líquido) de 31%, indicando uma alta capacidade de gerar lucros a partir do capital investido. Este desempenho é sustentado por margens EBIT em expansão, passando de 14,9% para 19,4%. A eficiência operacional também se reflete no FCF Yield (Yield de Fluxo de Caixa Livre) de 13,4%, que supera o limiar de 6%.

###### Gestão
A gestão da empresa tem uma reputação sólida, com um histórico ininterrupto de dividendos por 19 anos e um DY (Dividend Yield) de 15,9%. Esses indicadores sugerem uma governança corporativa robusta e a capacidade de gerir efetivamente os fluxos de caixa para beneficiar os acionistas.

###### Dados Internos
Dado não disponível. Não há informações sobre propriedade interna ou transações recentes de insiders nas web facts fornecidas.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico da empresa é predominantemente Buffett/Quality (7/12) e Value (6/12). As pontuações específicas são:
- **Value**: +2 P/E < mediana setorial, +2 FCF Yield > 6%, +2 ROE > Ke
- **Growth**: +1 Receita YoY > 15%, +2 Margem EBIT em expansão
- **Dividend**: +2 DY > 5%, +2 Histórico ininterrupto de dividendos, +1 JCP+Dividendo BR market
- **Buffett**: +2 ROE > 15%, +1 ND/EBITDA < 2x, +1 Beneish M=-2.58 clean, +1 DCF MoS > 20%, +1 Streak ≥ 10 anos, +1 Narrow moat

###### O que o preço desconta
O preço atual da empresa de R$6,44 sugere um nível de otimismo significativo em relação ao crescimento futuro. A margem de segurança do modelo DCF indica uma sobreavaliação potencial, considerando a comparação com os múltiplos setoriais e o histórico de dividendos.

###### O que os fundamentos sugerem
Os fundamentos da empresa indicam um desempenho sólido em termos de eficiência operacional e gestão. No entanto, a relação P/E alta (6,57x) e o DY elevado (15,9%) levantam questões sobre a sustentabilidade desses níveis de dividendos.

###### DCF — A âncora do valor
| Cenário | Crescimento 5y | Perpetuidade | Valor por ação |
|---|---|---|---|
| Pessimista | 5% a.a. | 3% | R$ 6,67 |
| **Base** | **8% a.a.** | **4%** | **R$ 7,78** |
| Optimista | 11% a.a. | 5% | R$ 9,13 |

###### Margem de segurança
A margem de segurança em relação ao preço atual é de +21%, indicando que o valor intrínseco calculado está significativamente acima do preço atual.

###### Rating final
RATING: Sell

###### Pre-Mortem — Se esta tese falhar
Se a empresa não conseguir sustentar os níveis atuais de dividendos ou se enfrentar uma deterioração nas margens EBIT, isso poderia levar a um reajuste significativo nos preços das ações. Valentina Prudente sinalizou que o alto dividendo anual e ROE de 31% indicam solidez financeira, mas Pedro Alocação argumentou que a alta taxa de dividendos pode não ser sustentável dada a relação P/E elevada e o FCF Yield baixo.

###### Horizonte
O horizonte para este veredito é de 24-36 meses, permitindo tempo suficiente para avaliar as tendências operacionais e financeiras da empresa.

###### Nota divergente do Council
Foi neste ponto que Valentina Prudente divergiu de Pedro Alocação: enquanto a primeira viu o alto dividendo anual como um indicador de solidez financeira, o segundo argumentou que a relação P/E elevada e o FCF Yield baixo sugerem riscos significativos para a sustentabilidade dos dividendos.

---

##### Evidence Ledger — fontes de cada métrica e claim

> 19 entradas · 11 com URL · confiança: {'reported': 6, 'computed': 6, 'extracted': 7}

| # | Claim | Valor | Fonte | URL | Confiança | Fetched |
|---|---|---|---|---|---|---|
| [1] | P/E ratio (TTM) | 6.57x | yfinance Ticker.info → fundamentals table | [link](https://finance.yahoo.com/quote/POMO3.SA) | `reported` | 2026-04-30 |
| [2] | P/B ratio | 2.08x | yfinance Ticker.info | [link](https://finance.yahoo.com/quote/POMO3.SA) | `reported` | 2026-04-30 |
| [3] | Div

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\POMO3_STORY.md`)_

#### — · Panorama
_source: `tickers\POMO3.md` (now in cemetery)_

#### POMO3 — POMO3

#watchlist #br #industrials

##### Links

- Sector: [[sectors/Industrials|Industrials]]
- Market: [[markets/BR|BR]]
- Peers: [[MOTV3]] · [[RAPT4]] · [[RENT3]] · [[SIMH3]] · [[TUPY3]]

##### Snapshot

- **Preço**: R$6.01  (2026-05-07)    _+0.00% 1d_
- **Screen**: 1.0  ✓ PASS
- **Altman Z**: 3.266 (safe)
- **Piotroski**: 6/9
- **Div Safety**: 75.0/100 (WATCH)

##### Fundamentals

- P/E: 6.01 | P/B: 1.9456135 | DY: 15.71%
- ROE: 30.97% | EPS: 1.0 | BVPS: 3.089
- Streak div: 19y | Aristocrat: None

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

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -21.39%
- **Drawdown 5y**: -21.39%
- **YTD**: +8.29%
- **YoY (1y)**: +24.97%
- **CAGR 3y**: +32.63%  |  **5y**: +25.88%  |  **10y**: n/a
- **Vol annual**: +36.60%
- **Sharpe 3y** (rf=4%): +0.76

###### Dividendos
- **DY 5y avg**: +9.18%
- **Div CAGR 5y**: +52.32%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$5.42B | R$449.1M | R$-52.1M |
| 2023-12-31 | R$6.68B | R$816.2M | R$907.2M |
| 2024-12-31 | R$8.59B | R$1.20B | R$899.6M |
| 2025-12-31 | R$9.06B | R$1.22B | R$1.12B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "POMO3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: POMO3
    data: [4.85, 5.04, 5.24, 5.04, 5.31, 5.34, 5.43, 5.68, 5.69, 5.91, 5.94, 5.94, 5.95, 5.95, 5.99, 6.37, 6.55, 6.42, 6.37, 6.64, 6.73, 6.73, 7.01, 7.32, 7.27, 6.99, 6.71, 6.64, 6.54, 6.67, 6.83, 6.93, 5.98, 5.91, 5.75, 6.25, 5.5, 5.55, 5.37, 5.24, 5.55, 5.74, 5.58, 5.54, 5.56, 6.04, 6.12, 5.85, 6.04, 6.2, 6.49, 6.33, 6.0, 5.65, 5.56, 5.77, 5.66, 5.86, 6.28, 6.5, 6.33, 6.2, 6.01]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "POMO3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.0992, 0.014, 0.0841, 0.0455, 0.0705, 0.0811, 0.1076, 0.2515, 0.5015, 1.1455, 0.085]
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
    data: [6.5714283, 6.3265305, 6.0408163, 6.01, 6.01]
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
    data: [15.86, 15.23, 15.95, 15.71, 15.71]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `tickers\POMO3_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — POMO3

**Committee verdict**: **BUY** (high confidence, 100% consensus)  
**Votes**: BUY=5 | HOLD=0 | AVOID=0  
**Avg conviction majority**: 7.8/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE alto e estável
- P/B baixo, geração de cash forte
- Dividend yield atrativo

**Key risk**: Dependência excessiva de um único mercado ou cliente

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- PE baixo e DY alto sugerem valor
- ROE forte indica solidez financeira
- Net debt/EBITDA saudável

**Key risk**: Possível reversão da tendência macroeconômica que sustenta o atual regime de liquidez

###### 🟢 Nassim Taleb — **BUY** (conv 8/10, size: medium)

**Rationale**:
- PE baixo e DY alto
- ROE forte
- Net debt/EBITDA positivo

**Key risk**: Dependência de um setor específico pode levar a fragilidade

###### 🟢 Seth Klarman — **BUY** (conv 8/10, size: medium)

**Rationale**:
- P/E baixo, ROE alto
- Dividend yield atrativo
- Dívida controlada

**Key risk**: Volatilidade setorial e econômica pode afetar negativamente o valor intrínseco

###### 🟢 Ray Dalio — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE baixo e dividendos atraentes
- ROE forte
- Net debt/EBITDA positivo

**Key risk**: Possível aumento da taxa de juros impactando o valor do ativo

##### 📊 Context provided

```
TICKER: BR:POMO3

FUNDAMENTALS LATEST:
  pe: 6.0
  pb: 1.9423761
  dy: 15.73%
  roe: 30.97%
  net_debt_ebitda: 0.9931406677389282
  intangible_pct_assets: 3.1%   (goodwill $0.2B + intangibles $0.1B)
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama POMO3 --write
ii deepdive POMO3 --save-obsidian
ii verdict POMO3 --narrate --write
ii fv POMO3
python -m analytics.fair_value_forward --ticker POMO3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
