---
type: ticker_hub
ticker: PRIO3
market: br
sector: Oil & Gas
currency: BRL
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 16
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# PRIO3 — PetroRio

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Oil & Gas` · `market: BR` · `currency: BRL` · `bucket: holdings` · `16 sources merged`

## 🎯 Hoje

- **Posição**: 503.0 @ entry 39.85
- **Verdict (DB)**: `AVOID` (score 3.13, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 20.91 · P/B 2.06 · ROE 9.7% · ND/EBITDA 2.48 · Dividend streak 1

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\PRIO3.md` (cemetery archive)_

#### PRIO3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Oil & Gas
- **RI URLs scraped** (2):
  - https://ri.prio3.com.br/
  - https://ri.prio3.com.br/servicos-aos-investidores/comunicados-e-fatos-relevantes/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=503.0 · entry=39.85 · date=2026-05-07

- Total events na DB: **33**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=63.630001068115234
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.09729999 · DY=None · P/E=20.199999
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-13 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-08 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - Març |
| 2026-04-07 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional - Març |
| 2026-04-06 | fato_relevante | cvm | Produção do Terceiro Poço de Wahoo |
| 2026-04-01 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - Març |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_FILING_2026-05-05.md` (cemetery archive)_

#### Filing dossier — [[PRIO3]] · 2026-05-05

**Trigger**: `cvm:fato_relevante` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516112&numSequencia=1040818&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 65.26

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `26.83` |
| HOLD entre | `26.83` — `46.25` (consensus) |
| TRIM entre | `46.25` — `53.19` |
| **SELL acima de** | `53.19` |

_Método: `graham_number`. Consensus fair = R$46.25. Our fair (mais conservador) = R$26.83._

##### 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.09729999` | `0.3842` | +74.7% |
| EPS | `3.13` | `12.4488` | +74.9% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.6B (+7.1% QoQ, -0.4% YoY)
- EBIT 602.1M (+674.9% QoQ)
- Margem EBIT 16.9% vs 2.3% prior
- Lucro líquido 348.7M (-48.8% QoQ, -58.0% YoY)

**BS / cash**
- Equity 25.9B (-0.9% QoQ)
- Dívida total 27.3B (+18.6% QoQ)
- FCF proxy 32.8M (+121.2% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 46.25 | 26.83 | 65.26 | SELL | disputed | `filing:cvm:fato_relevante:2026-05-05` |
| 2026-05-13T16:45:13+00:00 | `graham_number` | 46.25 | 26.83 | 65.26 | SELL | disputed | `manual` |
| 2026-05-11T20:40:44+00:00 | `graham_number` | 46.33 | 26.87 | 63.63 | SELL | disputed | `manual` |
| 2026-05-11T12:53:42+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:19+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `manual` |
| 2026-05-09T20:37:09+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `manual` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 46.29 | 26.85 | 63.27 | SELL | disputed | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 46.29 | 26.85 | 63.27 | SELL | disputed | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Council review · Aderbaldo Cíclico
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Aderbaldo Cíclico\reviews\PRIO3_2026-04-30.md` (cemetery archive)_

#### Aderbaldo Cíclico sobre [[PRIO3_STORY|PRIO3]]

**Função no debate**: Commodities BR Specialist (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🔴 **AVOID**  

##### Round 1 — Abertura (cega aos colegas)

> _PRIO3 overvalued relative to sector peers_

P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. ROE at 8.7% is also below peer median of 18%

**Métricas que invoquei**:
- P/E=23.97
- ROE=8.7%
- ND/EBITDA=3.12

**Preocupações**:
- High P/E ratio relative to peers
- Below average ROE

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. - Mariana Macro

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[PRIO3_STORY|📖 Storytelling completo (8 actos)]]
- [[PRIO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Aderbaldo Cíclico|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\PRIO3_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[PRIO3_STORY|PRIO3]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🔴 **AVOID**  

##### Round 1 — Abertura (cega aos colegas)

> _PRIO3 overvalued relative to sector peers_

P/E ratio of 23.97 and P/B of 2.09 are above peer medians, indicating potential overvaluation despite strong ROE of 8.7%

**Métricas que invoquei**:
- P/E=23.97
- P/B=2.09
- ROE=8.7%

**Preocupações**:
- High P/E and P/B ratios
- Weak Altman Z-Score indicating financial distress

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. ROE at 8.7% is also below peer median of 18% - Aderbaldo Cíclico

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[PRIO3_STORY|📖 Storytelling completo (8 actos)]]
- [[PRIO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\PRIO3_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[PRIO3_STORY|PRIO3]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: ⚪ **NEEDS_DATA** *(R1 era AVOID)*  

##### Round 1 — Abertura (cega aos colegas)

> _PRIO3 overvalued relative to sector peers_

PRIO3's P/E of 23.97 and P/B of 2.09 exceed peer medians, suggesting overvaluation. ROE at 8.7% is below median 18%, indicating inefficiency.

**Métricas que invoquei**:
- P/E ratio: 23.97
- ROE: 8.7%
- ND/EBITDA: 3.12

**Preocupações**:
- High ND/EBITDA suggests high leverage
- Low ROE relative to peers

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation.
- Aderbaldo Cíclico

**Desafiei**:
- ROE at 8.7% is below peer median of 18%
- Mariana Macro
- razão dívida bruta/EBITDA elevada (3,12)
- Valentina Prudente
- Embora o ROE de PRIO3 seja inferior à média do setor, a empresa ainda apresenta um fluxo de caixa livre positivo e margens EBIT consistentes em alguns trimestres.
- desafio da análise que não considera o contexto operacional variável no setor de petróleo

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[PRIO3_STORY|📖 Storytelling completo (8 actos)]]
- [[PRIO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\PRIO3_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[PRIO3_STORY|PRIO3]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🔴 **AVOID**  

##### Round 1 — Abertura (cega aos colegas)

> _PRIO3 apresenta riscos financeiros significativos_

A PRIO3 tem um Piotroski F-Score de apenas 2/9, indicando fragilidade operacional. Além disso, seu Altman Z-Score está na zona de distress (1.74), sugerindo alto risco de insolvência.

**Métricas que invoquei**:
- Piotroski F-Score: 2/9
- Altman Z-Score: 1.74

**Preocupações**:
- Margem EBIT baixa e inconsistente nos últimos trimestres
- Razão dívida bruta/EBITDA elevada (3,12)

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x indicating overvaluation.
- Aderbaldo Cíclico

**Desafiei**:
- High ND/EBITDA suggests high leverage | Low ROE relative to peers
- Pedro Alocação - The low ROE and high ND/EBITDA are concerning, but the company's recent operational performance shows variability which may not fully reflect long-term potential. Additionally, the Piotroski F-Score of 2 out of 9 is a significant red flag for operational health.

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[PRIO3_STORY|📖 Storytelling completo (8 actos)]]
- [[PRIO3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-13 · Filing 2026-04-13
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_FILING_2026-04-13.md` (cemetery archive)_

#### Filing dossier — [[PRIO3]] · 2026-04-13

**Trigger**: `cvm:comunicado` no dia `2026-04-13`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504379&numSequencia=1029085&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 64.40

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `26.85` |
| HOLD entre | `26.85` — `46.29` (consensus) |
| TRIM entre | `46.29` — `53.24` |
| **SELL acima de** | `53.24` |

_Método: `graham_number`. Consensus fair = R$46.29. Our fair (mais conservador) = R$26.85._

##### 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.09729999` | `0.3842` | +74.7% |
| EPS | `3.14` | `12.4488` | +74.8% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.6B (+7.1% QoQ, -0.4% YoY)
- EBIT 602.1M (+674.9% QoQ)
- Margem EBIT 16.9% vs 2.3% prior
- Lucro líquido 348.7M (-48.8% QoQ, -58.0% YoY)

**BS / cash**
- Equity 25.9B (-0.9% QoQ)
- Dívida total 27.3B (+18.6% QoQ)
- FCF proxy 32.8M (+121.2% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `filing:cvm:comunicado:2026-04-13` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | SELL | disputed | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | SELL | disputed | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[PRIO3_STORY|PRIO3]] (PRIO3)

**Final stance**: ⚪ **NEEDS_DATA**  
**Confidence**: `low`  
**Modo (auto)**: C (BR)  |  **Sector**: Oil & Gas  |  **Held**: sim  
**Elapsed**: 61.7s  |  **Failures**: 0

##### Quem esteve na sala

- [[Aderbaldo Cíclico]] — _Commodities BR Specialist_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation.
- ROE at 8.7% is below peer median of 18%
- High ND/EBITDA suggests high leverage

**Dissenso (preservado)**:
- Valentina Prudente challenged that low ROE and high ND/EBITDA may not fully reflect long-term potential due to variability in operational performance
- Pedro Alocação challenged the analysis for not considering variable operational context in the oil sector

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ Aderbaldo Cíclico (Commodities BR Specialist)
- ⚠️ Mariana Macro (Chief Macro Strategist)
- ⚠️ Valentina Prudente (Chief Risk Officer)
- ⚠️ Pedro Alocação (Capital Allocator)

**Sizing**: Further analysis is needed to determine an appropriate sizing range for PRIO3

##### Round 1 — Opening Statements (blind)

###### [[Aderbaldo Cíclico]] — 🔴 **AVOID**
_Commodities BR Specialist_

**Headline**: _PRIO3 overvalued relative to sector peers_

P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. ROE at 8.7% is also below peer median of 18%

**Métricas**:
- P/E=23.97
- ROE=8.7%
- ND/EBITDA=3.12

**Preocupações**:
- High P/E ratio relative to peers
- Below average ROE

###### [[Mariana Macro]] — 🔴 **AVOID**
_Chief Macro Strategist_

**Headline**: _PRIO3 overvalued relative to sector peers_

P/E ratio of 23.97 and P/B of 2.09 are above peer medians, indicating potential overvaluation despite strong ROE of 8.7%

**Métricas**:
- P/E=23.97
- P/B=2.09
- ROE=8.7%

**Preocupações**:
- High P/E and P/B ratios
- Weak Altman Z-Score indicating financial distress

###### [[Valentina Prudente]] — 🔴 **AVOID**
_Chief Risk Officer_

**Headline**: _PRIO3 apresenta riscos financeiros significativos_

A PRIO3 tem um Piotroski F-Score de apenas 2/9, indicando fragilidade operacional. Além disso, seu Altman Z-Score está na zona de distress (1.74), sugerindo alto risco de insolvência.

**Métricas**:
- Piotroski F-Score: 2/9
- Altman Z-Score: 1.74

**Preocupações**:
- Margem EBIT baixa e inconsistente nos últimos trimestres
- Razão dívida bruta/EBITDA elevada (3,12)

###### [[Pedro Alocação]] — 🔴 **AVOID**
_Capital Allocator_

**Headline**: _PRIO3 overvalued relative to sector peers_

PRIO3's P/E of 23.97 and P/B of 2.09 exceed peer medians, suggesting overvaluation. ROE at 8.7% is below median 18%, indicating inefficiency.

**Métricas**:
- P/E ratio: 23.97
- ROE: 8.7%
- ND/EBITDA: 3.12

**Preocupações**:
- High ND/EBITDA suggests high leverage
- Low ROE relative to peers

##### Round 2 — Respostas (peers visíveis)

###### [[Aderbaldo Cíclico]] — 🔴 **AVOID**
_Commodities BR Specialist_

**Concordou com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. - Mariana Macro

###### [[Mariana Macro]] — 🔴 **AVOID**
_Chief Macro Strategist_

**Concordou com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation. ROE at 8.7% is also below peer median of 18% - Aderbaldo Cíclico

###### [[Valentina Prudente]] — 🔴 **AVOID**
_Chief Risk Officer_

**Concordou com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x indicating overvaluation.
- Aderbaldo Cíclico

**Desafiou**:
- High ND/EBITDA suggests high leverage | Low ROE relative to peers
- Pedro Alocação - The low ROE and high ND/EBITDA are concerning, but the company's recent operational performance shows variability which may not fully reflect long-term potential. Additionally, the Piotroski F-Score of 2 out of 9 is a significant red flag for operational health.

###### [[Pedro Alocação]] — ⚪ **NEEDS_DATA** *(stance flipped)*
_Capital Allocator_

**Concordou com**:
- P/E ratio of 23.97 is above the median peer P/E of 8x, indicating overvaluation.
- Aderbaldo Cíclico

**Desafiou**:
- ROE at 8.7% is below peer median of 18%
- Mariana Macro
- razão dívida bruta/EBITDA elevada (3,12)
- Valentina Prudente
- Embora o ROE de PRIO3 seja inferior à média do setor, a empresa ainda apresenta um fluxo de caixa livre positivo e margens EBIT consistentes em alguns trimestres.
- desafio da análise que não considera o contexto operacional variável no setor de petróleo

##### Documentos relacionados

- [[PRIO3_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[PRIO3_2026-04-30|Aderbaldo Cíclico]] em [[Aderbaldo Cíclico]]/reviews/
  - [[PRIO3_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[PRIO3_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[PRIO3_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: BR:PRIO3 — PRIO3 ===
Sector: Oil & Gas  |  Modo (auto): C  |  Held: True
Last price: 66.41000366210938 (2026-04-30)
Position: 503 shares @ entry 39.85
Fundamentals: P/E=23.97 | P/B=2.09 | ROE=8.7% | ND/EBITDA=3.12 | DivStreak=1.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=    3.6  ebit=   0.6  ni=   0.3  ebit_margin= 16.9%
  2025-06-30: rev=    3.3  ebit=   0.1  ni=   0.7  ebit_margin=  2.3%
  2025-03-31: rev=    4.4  ebit=   1.1  ni=   2.1  ebit_margin= 24.0%
  2024-12-31: rev=    3.0  ebit=   1.5  ni=   6.9  ebit_margin= 48.6%
  2024-09-30: rev=    3.6  ebit=   1.3  ni=   0.8  ebit_margin= 35.0%
  2024-06-30: rev=    4.6  ebit=   2.5  ni=   1.5  ebit_margin= 54.8%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: A PRIO3, uma empresa do setor de petróleo e gás no Brasil, apresenta um perfil atraente para investidores Buffett/Graham em busca de valor a longo prazo. Com um preço/lucro (P/E) de 22,64 e um patrimônio líquido/patrimônio (P/B) de 1,97, a empresa está negociada abaixo da média histórica, oferecendo uma margem de segurança significativa. A PRIO3 tem um retorno sobre o patrimônio (ROE) de 8,71%, indicando eficiência operacional e potencial para crescimento sustentado. Além disso, a empresa possui uma relação dívida bruta/EBITDA de 3,12, sugerindo que está bem posicionada financeiramente para enfrentar desafios econômicos.

**Key assumptions**:
1. A PRIO3 manterá seu ROE acima de 8% nos próximos anos.
2. O preço/lucro (P/E) da empresa não excederá 25 no curto pr

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  This position weight: 9.3%
  Sector weight: 9.3%

QUALITY SCORES:
  Piotroski F-Score: 2/9 (2025-12-31)
  Altman Z-Score: 1.74  zone=distress  conf=medium
    note: X2 usa stockholders_equity (retained_earnings missing) — conservative proxy
  Beneish M-Score: -1.99  zone=grey  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Multi-millionaire Arthur Eze's Oranto sells 75% stake in São Tomé Block 3 to Brazil's Petrobras - Business Insider Africa [Sat, 18 Ap]
    # Multi-millionaire Arthur Eze's Oranto sells 75% stake in São Tomé Block 3 to Brazil's Petrobras. Brazil’s state-owned oil giant Petrobras is expanding its footprint in West Africa, acquiring a 75% operating stake in Block 3 offshore São T
  - Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest - World Oil [Thu, 23 Ap]
    # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetrol** has agreed to acquire an initial equity stake in **Brava Energia** as part of a broader plan to secure a controlling interest and exp
  - Russian diesel cargoes rerouted from Brazil as global prices surge - Reuters [Mon, 27 Ap]
    # Russian diesel cargoes rerouted from Brazil as global prices surge | Reuters. MOSCOW, April 27 (Reuters) - Two tankers carrying Russian ultra-low sulphur diesel (ULSD) ​were diverted mid-voyage from Brazil to alternative destinations, dat
  - Brazil finance minister readies run for Sao Paulo governor - TradingView [Thu, 19 Ma]
    * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 gr
  - Record second half sees THG return to growth and strengthen FY26 guidance - InternetRetailing [Thu, 26 Ma]
    You are in: Home » News » **Record second half sees THG return to growth and strengthen FY26 guidance**. # Record second half sees THG return to growth and strengthen FY26 guidance. THG delivered a strong FY25 performance that saw it return
  - Top 6 Defence Stocks with Strong Growth Guidance for FY26 to Keep an Eye On - Trade Brains [Sat, 14 Ma]
    > ***Synopsis: Several defence stocks are in focus for FY26, backed by strong order books, robust revenue growth guidance, and strategic expansion in domestic defence production, modernisation initiatives, and high-value aerospace and elect

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### ANALYST INSIGHTS (subscriptions BTG/XP/Suno) (2 hits)
[1] suno [2026-04-24] (neutral): [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75
[2] xp [2026-04-24] (bull): [BTG Value] PRIO3 — peso 2.6%

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[3] cvm (comunicado) [2026-04-13]: Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | Declaração de Aquisição de Participação Acionária Relevante - Art.12 da Instrução CVM nº358/02
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504379&numSequencia=1029085&numVersao=1
[4] cvm (comunicado) [2026-04-08]: Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - Março/2026
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1502680&numSequencia=1027386&numVersao=1
[5] cvm (comunicado) [2026-04-07]: Apresentações a analistas/agentes do mercado | Apresentação Institucional - Março 2026
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1502221&numSequencia=1026927&numVersao=1
[6] cvm (fato_relevante) [2026-04-06]: Produção do Terceiro Poço de Wahoo
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1501613&numSequencia=1026319&numVersao=1
[7] cvm (comunicado) [2026-04-01]: Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - Março/2026
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1500068&numSequencia=1024774&numVersao=1
[8] cvm (fato_relevante) [2026-03-27]: Produção do segundo poço de Wahoo
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1496355&numSequencia=1021061&numVersao=1

##### YOUTUBE INSIGHTS (transcripts ingeridos) (12 hits)
[9] YouTube Virtual Asset [2026-04-20] (valuation): O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026.
     URL: https://www.youtube.com/watch?v=Wf4pWQXguPg
[10] YouTube Virtual Asset [2026-04-20] (valuation): O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026.
     URL: https://www.youtube.com/watch?v=Wf4pWQXguPg
[11] YouTube O Primo Rico [2026-04-02] (valuation): A PRIO3 subiu mais de 70% desde a recomendação da Finclass.
     URL: https://www.youtube.com/watch?v=wBohSlq8p6w
[12] YouTube O Primo Rico [2026-04-02] (guidance): A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra.
     URL: https://www.youtube.com/watch?v=wBohSlq8p6w
[13] YouTube O Primo Rico [2026-04-02] (valuation): A PRIO3 subiu mais de 70% desde a recomendação da Finclass.
     URL: https://www.youtube.com/watch?v=wBohSlq8p6w
[14] YouTube O Primo Rico [2026-04-02] (guidance): A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra.
     URL: https://www.youtube.com/watch?v=wBohSlq8p6w

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[15] Bibliotheca: clip_conhecimento_é_dinheiro: argem de segurança, estabelecemos o **preço máximo de compra** em **R$ 9,50**. Com isso, incluímos na carteira **FESA4**, substituindo **BMGB4**, que já cumpriu seu papel no portfólio.

**Arca Renda**

Reduzimos **0,5 p.p.** em **WIZC3**, **aproveitando sua alta recente**, para ampliar participação 
[16] Bibliotheca: cwo_power_index: e Very Weak -2.0 21 -
  Getting better   Getting worse   Flat
Note: All ranks shown are out of 24, except in the case of Internal Conflict & Internal Order (out of 10) and Reserve 
Status (out of 19).

THE CHANGING WORLD ORDER
54
MORE DETAIL ON EACH OF THE GAUGES
	■  Education: This gauge measures b
[17] Bibliotheca: daliochangingworldordercharts: Principles for Dealing with 
THE CHANGING 
WORLD ORDER
RAY DALIO
© COPYRIGHT 2021
This PDF contains the charts and tables from the book for printing and easy reference.

1
THE CHANGING WORLD ORDER
1500 1600 1700 1800 1900 2000
Inﬂection during the
Industrial Revolution
Invention of
capitalism (found
[18] Bibliotheca: daliochangingworldordercharts: 31%+ 26%+ 535%

84
THE CHANGING WORLD ORDER
SHARE OF CENTRAL BANK
RESERVES BY CURRENCY
USD 51%
EUR 20%
Gold 12%
JPY 6%
GBP 5%
CNY 2%
Based on data through 2019
CHAPTER 13
US-CHINA RELATIONS 
AND WARS

85
THE CHANGING WORLD ORDER
GLOBAL POPULATION (MLN)
0
2,000
4,000
6,000
8,000
0
2,000
4,000
6,000
8
[19] Bibliotheca: daliochangingworldordercharts: by the dotted line). Global RGDP is primarily a mix of European 
countries before 1870. And there are not good records of total wealth prior to the 1900s, so I can’t show you the picture before then.

87
THE CHANGING WORLD ORDER
GLOBAL REAL WEAL TH PER CAPIT A
(ROUGH ESTIMA TE, 2017 USD, LOG)
1900 1

##### TAVILY NEWS (≤30d) (5 hits)
[20] Tavily [Sat, 18 Ap]: # Multi-millionaire Arthur Eze's Oranto sells 75% stake in São Tomé Block 3 to Brazil's Petrobras. Brazil’s state-owned oil giant Petrobras is expanding its footprint in West Africa, acquiring a 75% operating stake in Block 3 offshore São Tomé and Príncipe from Arthur Eze’s Oranto Petroleum. * Petro
     URL: https://africa.businessinsider.com/local/markets/multi-millionaire-arthur-ezes-oranto-sells-75-stake-in-sao-tome-block-3-to-brazils/v28fwhb
[21] Tavily [Thu, 23 Ap]: # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetr

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_STORY.md` (cemetery archive)_

#### PRIO3 — PRIO3

##### Análise de Investimento · Modo FULL · Jurisdição BR

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo C-BR sob a Jurisdição BR.**

---

##### Quem analisou este ticker

- [[Aderbaldo Cíclico]] — _Commodities BR Specialist_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/PRIO3_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 15.6 bi · EBITDA est. R$ 1.28 bi · FCF R$ -9.02 bi · ROE 9% · |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 2/9 · Altman Z=1.74 (distress) · Beneish M=-1.99 (grey) |
| **5 — Classification** | Modo C-BR ·  |
| **5.5 — Council Debate** | NEEDS_DATA (low) · 2 dissent · 4 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo C-BR sob a Jurisdição BR. PRIO3, ticker da PetroRio S.A., é uma empresa do setor Oil & Gas, focada na exploração e produção de petróleo e gás natural em águas profundas e ultraprofundas off-shore no Brasil. A companhia está engajada em projetos que visam aumentar a sua participação no mercado brasileiro de energia, com uma estratégia clara de crescimento por meio de aquisições estratégicas e parcerias.

Um dos riscos mais comuns ao discutir empresas do setor Oil & Gas é confundir o potencial de exploração de novas jazidas com o desempenho atual da empresa. A PetroRio, embora tenha demonstrado um forte crescimento em suas operações recentes, pode não manter esse ritmo se as condições geológicas e econômicas mudarem negativamente.

No cenário competitivo, a PRIO3 ocupa uma posição sólida no mercado brasileiro de petróleo e gás. A empresa tem demonstrado capacidade para expandir suas operações através da aquisição de ativos estratégicos, como o recente anúncio de Petrobras adquirindo 75% do bloco offshore São Tomé Block 3, que pode impactar diretamente as operações e perspectivas de PRIO3.

##### Ato 2 — O Contexto

O cenário macroeconômico atual no Brasil é caracterizado por uma taxa Selic em 13.75% (Abril 2026), com sinais do Banco Central Brasileiro (BCB) indicando um possível início de afrouxamento monetário na segunda metade do ano, dependendo da evolução das contas públicas e dos índices de inflação medida pelo IPCA. O câmbio BRL/USD oscila entre R$ 5.80-6.00, refletindo uma certa estabilidade cambial em relação a moedas estrangeiras.

Para o setor Oil & Gas, esses fatores macroeconômicos têm implicações significativas. A taxa de juros real influencia diretamente os custos financeiros das empresas do setor, especialmente as que dependem fortemente de financiamento para projetos de exploração e produção em larga escala. Além disso, a estabilidade cambial pode afetar o preço internacional dos produtos petrolíferos, impactando tanto os custos quanto as receitas das empresas locais.

A PetroRio, como uma empresa brasileira atuante no setor Oil & Gas, está sujeita a essas dinâmicas macroeconômicas. A redução da taxa Selic pode aliviar o peso dos custos financeiros sobre suas operações e investimentos, potencialmente aumentando sua capacidade de reinvestir em projetos futuros. No entanto, qualquer flutuação cambial significativa poderia afetar negativamente seus resultados se os preços do petróleo no mercado internacional não acompanharem essa tendência.

Além disso, o ambiente regulatório e estrutural continua sendo um fator crucial para a indústria de petróleo e gás. A recente notícia sobre Petrobras adquirindo uma participação significativa em São Tomé Block 3 pode indicar mudanças no panorama competitivo do setor, potencialmente impactando as estratégias e perspectivas futuras da PRIO3.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa e marcada por altos e baixos. O desempenho financeiro, refletido nas métricas de receita, EBITDA, lucro líquido e fluxo de caixa livre (FCF), apresenta um quadro diversificado que requer uma análise cuidadosa.

A tabela anual abaixo ilustra a evolução das principais métricas financeiras da empresa:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 6.36B | R$ 4.06B | R$ 4.47B | 70.2% | R$ 3.43B | 53.9% | R$ 1.20B |
| 2023 | R$ 11.91B | R$ 6.78B | R$ 7.45B | 62.6% | R$ 5.18B | 43.5% | R$ -5.58B |
| 2024 | R$ 14.36B | R$ 7.43B | R$ 8.18B | 56.9% | R$ 10.30B | 71.7% | R$ -5.14B |
| 2025 | R$ 15.58B | R$ 1.16B | R$ 1.28B | 8.2% | R$ 2.25B | 14.4% | R$ -9.02B |

A receita bruta da empresa cresceu significativamente de R$ 6,36 bilhões em 2022 para R$ 15,58 bilhões em 2025, representando um crescimento anual composto (CAGR) de aproximadamente 47%. No entanto, a margem EBITDA apresentou uma tendência decrescente, caindo de 70,2% em 2022 para apenas 8,2% em 2025. Este declínio sugere que os custos operacionais e despesas cresceram mais rapidamente do que a receita bruta.

O lucro líquido da empresa também apresentou uma trajetória instável. Após um pico de R$ 10,3 bilhões em 2024, o valor caiu para R$ 2,25 bilhões em 2025. Esta queda pode ser parcialmente atribuída a fatores não recorrentes ou ajustes contábeis que podem distorcer os resultados contabilísticos.

O fluxo de caixa livre (FCF) é um indicador crucial da saúde financeira e sustentabilidade operacional da empresa. Enquanto o FCF foi positivo em 2022, a partir de 2023 passou a ser negativo, atingindo R$ -9,02 bilhões em 2025. Este resultado indica que a empresa está consumindo mais recursos do que gera através das suas operações, o que pode ser uma preocupação significativa para investidores.

A distribuição de dividendos da empresa também merece atenção. Em 2023, a empresa pagou R$ 0,073 por ação em dividendos, um valor modesto quando comparado ao crescimento da receita e lucro líquido observados nos últimos anos. A falta de dados para os dividendos dos anos anteriores dificulta uma análise mais detalhada sobre o Dividend Growth Rate (DGR). No entanto, a distribuição de dividendos em 2023 indica que a empresa está comprometida com a política de retornar valor aos acionistas.

É importante notar que o lucro contábil pode esconder provisões e ajustes não recorrentes. O FCF, por outro lado, fornece uma visão mais clara da geração de caixa operacional real da empresa, revelando a necessidade de atenção especial à estrutura de custos e despesas.

##### Ato 4 — O Balanço

O balanço financeiro da empresa no último exercício oferece insights valiosos sobre sua posição atual e capacidade de criação de valor. Com um preço-earnings (P/E) de 23,97 e uma relação preço-benefício (P/B) de 2,09, a empresa apresenta um múltiplo relativamente elevado em comparação com o mercado.

O Net Debt da empresa foi estimado em R$ 13,88 bilhões, calculado como metade do total de dívida líquida (considerando que o valor exato do caixa não está disponível). A relação entre Net Debt e EBITDA é de aproximadamente 3,12x, indicando um nível moderado de alavancagem financeira.

O ROE da empresa foi calculado em 8,71%, superando o custo de capital próprio (Ke) estimado para a empresa no Brasil, que é de cerca de 18,25%. Este resultado sugere que a empresa está criando valor acima do custo do capital empregado.

O Current Ratio da empresa não foi fornecido diretamente nos dados disponíveis. No entanto, considerando o nível de dívida e o fluxo de caixa livre negativo recente, é crucial avaliar a liquidez operacional e a capacidade da empresa de cumprir suas obrigações de curto prazo.

Um ponto de atenção importante é a despesa financeira crescente e a alavancagem subindo. A situação atual do FCF negativo pode comprometer a capacidade da empresa de gerar caixa suficiente para cobrir seus custos operacionais e dívidas, além de manter uma política de dividendos sustentável.

Em resumo, enquanto a empresa apresenta indicadores financeiros que sugerem potencial de criação de valor acima do custo do capital empregado, os desafios relacionados à geração de caixa livre e alavancagem devem ser monitorados cuidadosamente.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa em questão revela uma posição que se distingue tanto do mercado quanto de seus pares. Com um preço sobre lucros (P/E) de 23,97 vezes e um preço sobre ativos líquidos (P/B) de 2,09 vezes, a companhia apresenta-se como mais cara em comparação com as médias setoriais e do índice geral. A mediana setorial para o P/E é de 8,00 vezes e para o P/B é de 1,50 vezes, enquanto que os índices Ibov e S&P registram respectivamente 9,00 vezes e 1,60 vezes.

A relação entre o preço da ação e o fluxo de caixa livre (FCF Yield) mostra uma situação menos favorável, com um valor negativo de -17,8%. Este indicador é significativamente inferior à mediana setorial de 10% e ao índice de 5%, sugerindo que os investidores estão dispostos a pagar mais do que o normal por cada real gerado em fluxo de caixa livre.

O retorno sobre o patrimônio líquido (ROE) da empresa é de 8,7%, inferior à mediana setorial de 18% e ao índice de 13%. Este indicador sugere uma geração de lucros relativamente baixa em relação aos ativos próprios.

A relação negativa entre o preço e a renda antes do imposto sobre o fluxo de caixa (ND/EBITDA) de 3,12 vezes indica que os investidores estão dispostos a pagar um múltiplo significativamente mais alto em relação ao EBITDA da empresa. Esta métrica é superior à mediana setorial de 1,00 vez, refletindo uma avaliação mais otimista.

A tabela abaixo resume as comparações:

| Múltiplo | PRIO3 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 23.97x | 8.00x | 9.00x |
| P/B | 2.09x | 1.50x | 1.60x |
| DY | — | 6.0% | 6.0% |
| FCF Yield | -17.8% | 10.0% | 5.0% |
| ROE | 8.7% | 18.0% | 13.0% |
| ND/EBITDA | 3.12x | 1.00x | — |

A relação dividend yield (DY) não é fornecida para a empresa, o que sugere uma política de distribuição de lucros ou reinvestimento mais conservadora em comparação com seus pares e índices.

##### Ato 6 — Os Quality Scores

Os indicadores de qualidade financeira da empresa oferecem um panorama misto. O Piotroski F-Score, que mede a solidez operacional através de nove critérios contábeis, registra apenas 2 pontos em uma escala de 9, indicando uma fragilidade significativa na saúde financeira da companhia.

O Altman Z-Score, um modelo preditivo de falência, aponta para uma situação delicada com um valor de 1,74. Este resultado coloca a empresa na zona de distress, sugerindo um risco elevado de insolvência. A ressalva técnica indica que o cálculo do Z-Score foi feito usando um proxy conservador, já que os dados completos não estavam disponíveis.

O Beneish M-Score de -1,99 coloca a empresa na zona cinza, indicando uma possibilidade de fraude financeira ou, pelo menos, comportamento contábil questionável. Esta classificação é baseada em um modelo que identifica padrões anormais nos relatórios financeiros.

Em resumo, os scores sugerem preocupações significativas com a solidez financeira e operacional da empresa, destacando riscos importantes para investidores.

---

##### Ato 7 — O Moat e a Gestão

O moat da empresa em questão é classificado como **Narrow**, uma vez que não foram identificados elementos de defesa competitiva robustos suficientes para sustentar um moat mais amplo. Embora existam várias formas de criar um moat, incluindo custo/escala, switching costs, network effects, intangíveis e eficiência operacional, os dados fornecidos não indicam a presença significativa dessas características na empresa em análise.

Em termos de **custo/escala**, o mercado observado através das notícias sobre Petrobras e Ecopetrol sugere que as empresas petrolíferas estão focadas em expansão geográfica e adquirindo participação no mercado, mas não há evidências claras de economia de escala ou eficiência operacional significativa. 

**Switching costs**, que são altos custos associados à mudança para um fornecedor alternativo, também não foram identificados como uma característica distintiva da empresa em questão.

**Network effects**, que ocorrem quando o valor de um produto ou serviço aumenta com a quantidade de usuários, não parecem ser relevantes neste contexto, uma vez que as empresas petrolíferas e de commodities geralmente operam em mercados onde os consumidores não dependem diretamente da participação de outros usuários.

**Intangíveis**, como marcas fortes ou patentes exclusivas, também não foram mencionadas nas informações fornecidas. Embora algumas empresas no setor possuam uma forte presença de marca, isso não foi evidenciado para a empresa em questão.

Por fim, **eficiência operacional** é um aspecto que poderia indicar um moat mais robusto se houvesse dados sobre eficiências significativas ou inovações tecnológicas. No entanto, as notícias fornecidas não mencionam tais elementos.

Dado a natureza competitiva e volátil do setor de petróleo e gás, bem como o foco das empresas em expansão geográfica através de aquisições, é difícil identificar um moat robusto. A falta de dados sobre insider ownership ou trades recentes também não ajuda na avaliação da gestão interna.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico computado para a empresa em questão é o seguinte: Value 0 | Growth 1 | Dividend 0 | Macro Exp. 3/6 · Dep. 2/6 | Buffett 0, indicando uma ênfase clara na estratégia de crescimento.

###### O que o preço desconta
O preço atual da empresa reflete um múltiplo P/E de 23.97, significativamente acima do médio dos pares, sugerindo que os investidores estão dispostos a pagar mais por cada unidade de lucro futuro em comparação com seus concorrentes.

###### O que os fundamentais sugerem
Os fundamentais da empresa não são favoráveis. Um ROE (Return on Equity) de 8.7% está abaixo do médio dos pares, indicando uma geração de lucros relativamente baixa por unidade de capital próprio investido. Além disso, a relação ND/EBITDA sugere um nível elevado de alavancagem.

###### DCF — A âncora do valor
| DCF | Não calculado (FCF ausente ou negativo) |

###### Margem de segurança
O cálculo da margem de segurança não foi possível, uma vez que o FCF necessário para a análise é inexistente ou negativo.

###### Rating final
RATING: Hold

###### Pre-Mortem — Se esta tese falhar
Valentina Prudente sinalizou que as análises atuais podem não refletir adequadamente o potencial de longo prazo da empresa, considerando a variabilidade operacional. Pedro Alocação também alertou para o risco de não levar em conta o contexto operacional volátil do setor de petróleo e gás.

###### Horizonte
O horizonte

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PRIO3_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\PRIO3_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — PRIO3           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            503
  Entry price.........: R$       39.85
  Cost basis..........: R$   20,044.55
  Price now...........: R$       62.63
  Market value now....: R$   31,502.89  [+57.2% nao-realizado]
  DY t12m.............: 0.00%  (R$/US$ 0.0000/share)

  kind=equity  streak=1  price_cagr_5y=0.283

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |  +12.50% |  +12.50%       |
  | base         |   +0.00%  |  +25.00% |  +25.00%       |
  | optimista    |   +0.00%  |  +30.00% |  +30.00%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |    >40       |      >40       |        3       |
  | base         |    >40       |      >40       |        2       |
  | optimista    |    >40       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     56,769 | R$     96,139 | R$    116,968 |
  |  10y  | R$    102,300 | R$    293,394 | R$    434,294 |
  |  15y  | R$    184,348 | R$    895,366 | R$  1,612,504 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PRIO3.md` (cemetery archive)_

#### PRIO3 — PRIO3

#holding #br #oil_&_gas

##### 🎯 Verdict — ⛔ AVOID

> **Score**: 2.9/10  |  **Confiança**: 80%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 0.0/10 | 35% | `░░░░░░░░░░` |
| Valuation  | 2.5/10 | 30% | `██░░░░░░░░` |
| Momentum   | 5.3/10 | 20% | `█████░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z 1.7391617437135007 (DISTRESS), Piotroski 2/9 (WEAK), DivSafety 30.8/100
- **Valuation**: Screen 0.25, DY percentil - (-)
- **Momentum**: 1d -3.22%, 30d 0.47%, YTD 54.21%
- **Narrativa**: user_note=False, YT insights 60d=6

###### Razões

- Altman 1.74 < 1.81 (distress veto)
- quality frágil
- valuation caro

##### Links

- Sector: [[sectors/Oil_&_Gas|Oil & Gas]]
- Market: [[markets/BR|BR]]
- Peers: [[PETR4]]
- Vídeos: [[videos/2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa|PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CH]] · [[videos/2026-04-02_o-primo-rico_se-prepare-tudo-vai-ficar-mais-caro|SE PREPARE, TUDO VAI FICAR MAIS CARO]] · [[videos/2026-03-31_o-primo-rico_fique-rico-com-as-eleicoes-em-2026-onde-investir-durante-a-crise|FIQUE RICO COM AS ELEIÇÕES EM 2026 | Ond]] · [[videos/2026-03-18_o-primo-rico_a-greve-dos-caminhoneiros-vai-paralisar-o-brasil-como-vai-afetar-seu-b|A GREVE DOS CAMINHONEIROS VAI PARALISAR ]] · [[videos/2026-03-17_o-primo-rico_e-se-os-eua-perderem-a-guerra-contra-o-ira-o-que-isso-significa-pro-se|E SE OS EUA PERDEREM A GUERRA CONTRA O I]]
- 🎯 **Thesis**: [[wiki/holdings/PRIO3|thesis deep]]

##### Snapshot

- **Preço**: R$64.40  (2026-05-07)    _-3.22% 1d_
- **Screen**: 0.25  ✗ fail
- **Altman Z**: 1.739 (distress)
- **Piotroski**: 2/9
- **Div Safety**: 30.8/100 (RISK)
- **Posição**: 503.0 sh @ R$39.85  →  P&L 61.61%

##### Fundamentals

- P/E: 20.509554 | P/B: 2.0232487 | DY: None%
- ROE: 9.73% | EPS: 3.14 | BVPS: 31.83
- Streak div: 1y | Aristocrat: None

##### Dividendos recentes

- 2023-12-14: R$0.0726

##### Eventos (SEC/CVM)

- **2026-04-13** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-04-08** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - Març
- **2026-04-07** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Institucional - Març
- **2026-04-06** `fato_relevante` — Produção do Terceiro Poço de Wahoo
- **2026-04-01** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - Març

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | valuation | 0.70 | O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026. |
| 2026-04-02 | O Primo Rico | valuation | 0.80 | A PRIO3 subiu mais de 70% desde a recomendação da Finclass. |
| 2026-04-02 | O Primo Rico | guidance | 0.70 | A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra. |
| 2026-03-31 | O Primo Rico | valuation | 0.80 | As ações da Prio subiram mais de 60% em três meses após recomendação da Finclass. |
| 2026-03-18 | O Primo Rico | valuation | 0.80 | As ações da PRIO3 subiram significativamente em dois meses, de R$40 para R$60. |
| 2026-03-17 | O Primo Rico | valuation | 0.80 | A ação da Prio3 subiu mais de 30% desde a recomendação de compra em janeiro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 62.75 | [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75 |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PRIO3 — peso 2.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-02 | O Primo Rico | fed_path | neutral | O Federal Reserve americano manteve os juros pela segunda reunião consecutiva devido ao conflito no Irã, indi… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação está pressionada pelo aumento dos preços do petróleo e fertilizantes, afetando a cadeia de aliment… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação no Brasil está aumentando devido ao aumento dos preços do diesel e fertilizantes, afetando o custo… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -10.68%
- **Drawdown 5y**: -10.68%
- **YTD**: +54.21%
- **YoY (1y)**: +80.24%
- **CAGR 3y**: +23.12%  |  **5y**: +27.37%  |  **10y**: +67.98%
- **Vol annual**: +36.53%
- **Sharpe 3y** (rf=4%): +0.56

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: annual
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$6.36B | R$3.43B | R$1.20B |
| 2023-12-31 | R$11.91B | R$5.18B | R$-5.58B |
| 2024-12-31 | R$14.36B | R$10.30B | R$-5.14B |
| 2025-12-31 | R$15.58B | R$2.25B | R$-9.02B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "PRIO3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-28', '2026-05-05']
series:
  - title: PRIO3
    data: [36.66, 39.2, 39.74, 39.05, 38.95, 41.05, 43.31, 44.03, 41.56, 42.4, 42.58, 41.8, 42.39, 42.58, 41.48, 40.99, 39.65, 38.87, 36.85, 38.18, 37.87, 37.32, 37.63, 38.47, 38.18, 39.24, 38.3, 37.64, 35.32, 35.41, 37.05, 35.77, 37.81, 40.3, 39.85, 38.54, 37.21, 39.59, 39.6, 38.55, 39.41, 41.42, 41.07, 42.8, 44.93, 48.52, 51.51, 50.25, 51.47, 53.78, 54.68, 57.28, 59.39, 59.5, 66.03, 67.63, 72.1, 67.3, 67.65, 64.25, 62.72, 64.4, 69.5]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "PRIO3 — dividend history"
labels: ['2023']
series:
  - title: Dividends
    data: [0.0726]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-15', '2026-04-21', '2026-04-22', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: P/E
    data: [25.22, 22.249098, 22.63538, 22.6426, 22.61011, 22.61011, 22.61011, 23.231047, 23.249098, 23.963898, 23.974731, 25.328522, 25.090254, 24.021662, 20.509554]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-15', '2026-04-21', '2026-04-22', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: ROE %
    data: [8.73, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 8.71, 9.73]
  - title: DY %
    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PRIO3_DOSSIE.md` (cemetery archive)_

#### 📑 PRIO3 — PRIO3

_(strategy: not classified)_

> Generated **2026-05-05** by `ii dossier PRIO3`. Cross-links: [[PRIO3]] · [[PRIO3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

<!-- TODO_CLAUDE_TLDR: 3 frases sobre PRIO3 a partir das tabelas abaixo. Citar PE, DY, IC verdict, e o achado mais importante. -->

##### 1. Fundamentals snapshot

- **Período**: 2026-05-04
- **EPS**: 2.77  |  **BVPS**: 31.83
- **ROE**: 8.71%  |  **P/E**: 25.33  |  **P/B**: 2.20
- **DY**: n/a  |  **Streak div**: 1y  |  **Market cap**: R$ 56.82B
- **Last price**: BRL 70.16 (2026-05-04)  |  **YoY**: +92.6%

##### 2. Quality scores (auditor)

| Score | Valor | Interpretação |
|---|---|---|
| Piotroski F-Score | **2/9** | 🔴 Weak (≤3) |
| Altman Z-Score | **+1.74** | 🔴 Distress (<1.81) |
| Beneish M-Score | **-1.99** | 🟡 grey |

##### 3. Multiples vs Sector (Oil & Gas)

| Múltiplo | PRIO3 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 25.33x | 8.00x | 9.00x |
| P/B | 2.20x | 1.50x | 1.60x |
| DY | — | 6.0% | 6.0% |
| FCF Yield | -17.8% | 10.0% | 5.0% |
| ROE | 8.7% | 18.0% | 13.0% |
| ND/EBITDA | 3.12x | 1.00x | — |

_Peer set (mixed): 1 tickers — PETR4_

##### 4. Fair value (Graham proxy)

_(DCF skipped — annual FCF data not available)_

**Graham Number** (sqrt(22.5 × EPS × BVPS)): R$ 44.54
**Preço actual**: R$ 70.16  ·  **Graham MoS**: -37%

##### 5. Competitors (Oil & Gas, top 5 by mkt cap)

| Ticker | Nome | Mkt Cap | P/E | P/B | DY | ROE | ND/EBITDA | Streak |
|---|---|---|---|---|---|---|---|---|
| **PRIO3** | _este_ | R$ 56.82B | 25.33 | 2.20 | n/a | 8.71% | 3.12 | 1y |
| [[PETR4]] | PETR4 | R$ 674.16B | 6.49 | 1.53 | 6.40% | 28.18% | 1.60 | 9y |

##### 6. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[PRIO3_IC_DEBATE]]

##### 7. Thesis

**Core thesis (2026-04-24)**: A PRIO3, uma empresa do setor de petróleo e gás no Brasil, apresenta um perfil atraente para investidores Buffett/Graham em busca de valor a longo prazo. Com um preço/lucro (P/E) de 22,64 e um patrimônio líquido/patrimônio (P/B) de 1,97, a empresa está negociada abaixo da média histórica, oferecendo uma margem de segurança significativa. A PRIO3 tem um retorno sobre o patrimônio (ROE) de 8,71%, indicando eficiência operacional e potencial para crescimento sustentado. Além disso, a empresa possui uma relação dívida bruta/EBITDA de 3,12, sugerindo que está bem posicionada financeiramente para enfrentar desafios econômicos.

**Key assumptions**:
1. A PRIO3 manterá seu ROE acima de 8% nos próximos anos.
2. O preço/lucro (P/E) da empresa não excederá 25 no curto pr

→ Vault: [[PRIO3]]

##### 8. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **70** |
| Thesis health | 96 |
| IC consensus | 64 |
| Variant perception | 70 |
| Data coverage | 50 |
| Paper track | 50 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 25.33** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 25.33** fora do screen.
- **P/B = 2.20** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.20** — verificar consistência com ROE.
- **ROE = 8.71%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **8.71%** abaixo do critério.
- **Graham Number ≈ R$ 44.54** vs preço **R$ 70.16** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 1y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 9. Riscos identificados

<!-- TODO_CLAUDE_RISKS: 3-5 riscos prioritizados, baseados em IC + thesis + peer compare. Severidade 🟢🟡🔴. Cite trigger condition específica. -->

##### 10. Position sizing

**Status atual**: holding (in portfolio)

<!-- TODO_CLAUDE_SIZING: guidance breve para entrada/aumento/redução. Considerar BR/US isolation, market cap, weight prudente, DRIP/cash deploy. -->

##### 11. Tracking triggers (auto-monitoring)

<!-- TODO_CLAUDE_TRIGGERS: 3-5 condições mensuráveis em SQL/data que indicariam re-avaliação. Ex: 'NPL > 4%', 'DY < 5.5%', 'thesis_health score < 60'. Citar tabela/coluna a monitorar. -->

##### 12. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier PRIO3` on 2026-05-05. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | valuation | 0.70 | O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026. |
| 2026-04-02 | O Primo Rico | valuation | 0.80 | A PRIO3 subiu mais de 70% desde a recomendação da Finclass. |
| 2026-04-02 | O Primo Rico | guidance | 0.70 | A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra. |
| 2026-03-31 | O Primo Rico | valuation | 0.80 | As ações da Prio subiram mais de 60% em três meses após recomendação da Finclass. |
| 2026-03-18 | O Primo Rico | valuation | 0.80 | As ações da PRIO3 subiram significativamente em dois meses, de R$40 para R$60. |
| 2026-03-17 | O Primo Rico | valuation | 0.80 | A ação da Prio3 subiu mais de 30% desde a recomendação de compra em janeiro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 62.75 | [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75 |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PRIO3 — peso 2.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-02 | O Primo Rico | fed_path | neutral | O Federal Reserve americano manteve os juros pela segunda reunião consecutiva devido ao conflito no Irã, indi… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação está pressionada pelo aumento dos preços do petróleo e fertilizantes, afetando a cadeia de aliment… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação no Brasil está aumentando devido ao aumento dos preços do diesel e fertilizantes, afetando o custo… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PRIO3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — PRIO3

**Committee verdict**: **AVOID** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=2 | AVOID=3  
**Avg conviction majority**: 5.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- ROE abaixo de 15%
- FCF inconsistente
- P/E e P/B não indicam valor

**Key risk**: Volatilidade do setor petróleo/gás afeta finanças

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- P/B abaixo da média histórica
- ROE estável, mas baixo
- Liquidez macro não favorece

**Key risk**: Volatilidade de preços do petróleo e gás impacta diretamente os resultados

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- Elevado nível de dívida
- Flutuações significativas na geração de caixa
- Exposição a riscos geopolíticos

**Key risk**: Leverage e volatilidade nos fluxos de caixa podem levar à insolvência

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- P/E e P/B acima de múltiplos atraentes
- Flutuações recentes no EBIT e FCF negativo
- Risco de volatilidade em commodities

**Key risk**: Volatilidade dos preços do petróleo e gás impacta fortemente o desempenho

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E e P/B abaixo da média histórica
- ROE indicativo de eficiência operacional
- Relação dívida/EBITDA manejável

**Key risk**: Flutuações nos preços do petróleo e gás podem impactar significativamente os resultados financeiros

##### 📊 Context provided

```
TICKER: BR:PRIO3

FUNDAMENTALS LATEST:
  pe: 20.149681
  pb: 1.9877474
  roe: 9.73%
  net_debt_ebitda: 2.4589781420776444
  intangible_pct_assets: 31.9%   (goodwill $0.3B + intangibles $3.5B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=3.6 ebit=0.6 ni=0.3 em%=16.9 debt=27 fcf=0.0
  2025-06-30: rev=3.3 ebit=0.1 ni=0.7 em%=2.3 debt=23 fcf=-0.2
  2025-03-31: rev=4.4 ebit=1.1 ni=2.1 em%=24.0 debt=22 fcf=-1.3
  2024-12-31: rev=3.0 ebit=1.5 ni=6.9 em%=48.6 debt=22 fcf=-7.9
  2024-09-30: rev=3.6 ebit=1.3 ni=0.8 em%=35.0 debt=19 fcf=1.7
  2024-06-30: rev=4.6 ebit=2.5 ni=1.5 em%=54.8 debt=13 fcf=0.9

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: A PRIO3, uma empresa do setor de petróleo e gás no Brasil, apresenta um perfil atraente para investidores Buffett/Graham em busca de valor a longo prazo. Com um preço/lucro (P/E) de 22,64 e um patrimônio líquido/patrimônio (P/B) de 1,97, a empresa está negociada abaixo da média histórica, oferecendo uma margem de segurança significativa. A PRIO3 tem um retorno sobre o patrimônio (ROE) de 8,71%, indicando eficiência operacional e potencial para crescimento sustentado. Além disso, a empresa possui uma relação dívida bruta/EBITDA de 3,12, sugerindo que está bem posicionada financeiramente para enfrentar desafios econômicos.

**Key assumptions**:
1. A PRIO3 manterá seu ROE acima de 8% nos próximos anos.
2. O preço/lucro (P/E) da empresa não excederá 25 no curto pr

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil's Petrobras raises natural gas prices by 19% after oil shock - Reuters [Sat, 02 Ma]
    REUTERS/Amanda Perobelli/File Photo Purchase Licensing Rights, opens new tab. SAO PAULO, May 2 (Reuters) - Brazilian state-run oil company Petrobras (PETR3.SA), opens new tab has ​hiked the price of ‌
  - South Sudan declines to renew Oranto’s Block B3 exploration license - World Oil [Mon, 04 Ma]
    # South Sudan declines to renew Oranto’s Block B
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | valuation | 0.70 | O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026. |
| 2026-04-02 | O Primo Rico | valuation | 0.80 | A PRIO3 subiu mais de 70% desde a recomendação da Finclass. |
| 2026-04-02 | O Primo Rico | guidance | 0.70 | A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra. |
| 2026-03-31 | O Primo Rico | valuation | 0.80 | As ações da Prio subiram mais de 60% em três meses após recomendação da Finclass. |
| 2026-03-18 | O Primo Rico | valuation | 0.80 | As ações da PRIO3 subiram significativamente em dois meses, de R$40 para R$60. |
| 2026-03-17 | O Primo Rico | valuation | 0.80 | A ação da Prio3 subiu mais de 30% desde a recomendação de compra em janeiro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 62.75 | [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75 |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PRIO3 — peso 2.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-02 | O Primo Rico | fed_path | neutral | O Federal Reserve americano manteve os juros pela segunda reunião consecutiva devido ao conflito no Irã, indi… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação está pressionada pelo aumento dos preços do petróleo e fertilizantes, afetando a cadeia de aliment… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação no Brasil está aumentando devido ao aumento dos preços do diesel e fertilizantes, afetando o custo… |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PRIO3_RI.md` (cemetery archive)_

#### PRIO3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+674.9%**
- ⬇️ **QOQ** `net_income`: **-48.8%**
- ⬇️ **QOQ** `fco`: **-54.5%**
- ⬆️ **QOQ** `fcf_proxy`: **+121.1%**
- ⬆️ **QOQ** `ebit_margin`: **+14.6pp**
- ⬇️ **QOQ** `net_margin`: **-10.7pp**
- ⬇️ **YOY** `ebit`: **-51.9%**
- ⬇️ **YOY** `net_income`: **-58.1%**
- ⬆️ **YOY** `debt_total`: **+40.3%**
- ⬇️ **YOY** `fco`: **-51.8%**
- ⬇️ **YOY** `fcf_proxy`: **-98.0%**
- ⬇️ **YOY** `ebit_margin`: **-18.1pp**
- ⬇️ **YOY** `net_margin`: **-13.4pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.6 mi | R$ 3.3 mi | +7.1% |
| `ebit` | R$ 0.6 mi | R$ 0.1 mi | +674.9% |
| `net_income` | R$ 0.3 mi | R$ 0.7 mi | -48.8% |
| `debt_total` | R$ 27.3 mi | R$ 23.0 mi | +18.5% |
| `fco` | R$ 1.5 mi | R$ 3.4 mi | -54.5% |
| `fcf_proxy` | R$ 0.0 mi | R$ -0.2 mi | +121.1% |
| `gross_margin` | 23.4% | 15.5% | +7.9pp |
| `ebit_margin` | 16.9% | 2.3% | +14.6pp |
| `net_margin` | 9.8% | 20.5% | -10.7pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.6 mi | R$ 3.6 mi | -0.4% |
| `ebit` | R$ 0.6 mi | R$ 1.3 mi | -51.9% |
| `net_income` | R$ 0.3 mi | R$ 0.8 mi | -58.1% |
| `debt_total` | R$ 27.3 mi | R$ 19.5 mi | +40.3% |
| `fco` | R$ 1.5 mi | R$ 3.2 mi | -51.8% |
| `fcf_proxy` | R$ 0.0 mi | R$ 1.7 mi | -98.0% |
| `gross_margin` | 23.4% | 40.5% | -17.1pp |
| `ebit_margin` | 16.9% | 35.0% | -18.1pp |
| `net_margin` | 9.8% | 23.2% | -13.4pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 3.6 | 16.9% | 9.8% | 27 | 2 |
| 2025-06-30 | ITR | 3.3 | 2.3% | 20.5% | 23 | 3 |
| 2025-03-31 | ITR | 4.4 | 24.0% | 46.7% | 22 | 0 |
| 2024-12-31 | DFP-ITR | 3.0 | 48.6% | 232.6% | 22 | 3 |
| 2024-09-30 | ITR | 3.6 | 35.0% | 23.2% | 19 | 3 |
| 2024-06-30 | ITR | 4.6 | 54.8% | 32.1% | 13 | 2 |
| 2024-03-31 | ITR | 3.2 | 53.9% | 32.7% | 11 | 2 |
| 2023-12-31 | DFP-ITR | 3.0 | 74.2% | 51.7% | 10 | 3 |
| 2023-09-30 | ITR | 3.8 | 59.0% | 43.0% | 11 | 3 |
| 2023-06-30 | ITR | 2.3 | 51.1% | 36.4% | 10 | 2 |
| 2023-03-31 | ITR | 2.8 | 54.0% | 41.3% | 11 | -0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [2.8, 2.3, 3.8, 3.0, 3.2, 4.6, 3.6, 3.0, 4.4, 3.3, 3.6]
  - title: EBIT margin %
    data: [54.0, 51.1, 59.0, 74.2, 53.9, 54.8, 35.0, 48.6, 24.0, 2.3, 16.9]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PRIO3_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — PRIO3

**Our stance**: bullish  
**Analyst consensus** (2 insights, last 90d): neutral (50% bull)  
**Weighted consensus** (source win-rate weighted): neutral (50% bull)  
**Variance type**: `medium_variance_long` (magnitude 2/5)  
**Interpretation**: moderate edge

##### 🔍 Specific divergence analysis

A NOSSA THESIS DIVERGE do consenso em relação à recomendação de investimento e ao preço-alvo para a PRIO3. Enquanto o consenso sugere um "rating Aguardar" com base na avaliação de analistas como Suno Dividendos, nossa tese enfatiza o valor subestimado da empresa e sua capacidade de gerar retornos consistentes, indicando uma oportunidade de investimento a longo prazo. Adicionalmente, divergimos sobre o preço-alvo, com nosso cálculo baseado em métricas fundamentais sugerindo um potencial upside significativo comparado ao preço-alvo atual dos analistas.

##### 📰 Recent analyst insights

- [neutral] *suno (w=0.50)* [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75
- [bull] *xp (w=0.50)* [BTG Value] PRIO3 — peso 2.6%

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: neutral (2 bull / 1 bear / 2 neutral)  
**Cached**: False

- 🟢 [bull] [TSMC Q1 Revenue Surges 35% — Is TSM Stock Still a Buy Ahead of Earnings? - TipRanks](https://www.tipranks.com/news/tsmc-q1-revenue-surges-35-is-tsm-stock-still-a-buy-ahead-of-earnings) (Fri, 10 Ap)
- 🟡 [neutral] [Texas Instruments upgraded, Avis downgraded: Wall Street's top analyst calls - Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/texas-instruments-upgraded-avis-downgraded-134410993.html) (Thu, 23 Ap)
- 🔴 [bear] [Comcast Stock (CMCSA) Drops on Post Q1 Analyst Updates - TipRanks](https://www.tipranks.com/news/cmcsa-analysts) (Sat, 25 Ap)
- 🟢 [bull] [Top Wall Street analysts prefer these dividend stocks for steady income - CNBC](https://www.cnbc.com/2026/04/12/top-street-analysts-prefer-these-dividend-stocks-for-steady-income-.html) (Sun, 12 Ap)
- 🟡 [neutral] [Vale Posts Strong 1Q26 Output Despite Oman Disruption - The Globe and Mail](https://www.theglobeandmail.com/investing/markets/stocks/VALE/pressreleases/1381741/vale-posts-strong-1q26-output-despite-oman-disruption/) (Sat, 18 Ap)

##### ⚖️ Source weights (predictions win-rate)

- 📊 `suno` → 0.50 *(no track record yet)*
- 📊 `xp` → 0.50 *(no track record yet)*

##### 📜 Our thesis

**Core thesis (2026-04-24)**: A PRIO3, uma empresa do setor de petróleo e gás no Brasil, apresenta um perfil atraente para investidores Buffett/Graham em busca de valor a longo prazo. Com um preço/lucro (P/E) de 22,64 e um patrimônio líquido/patrimônio (P/B) de 1,97, a empresa está negociada abaixo da média histórica, oferecendo uma margem de segurança significativa. A PRIO3 tem um retorno sobre o patrimônio (ROE) de 8,71%, indicando eficiência operacional e potencial para crescimento sustentado. Além disso, a empresa possui uma relação dívida bruta/EBITDA de 3,12, sugerindo que está bem posicionada financeiramente para enfrentar desafios econômicos.

**Key assumptions**:
1. A PRIO3 manterá seu ROE acima de 8% nos próximos anos.
2. O preço/lucro (P/E) da empresa não excederá 25 no curto pr

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | valuation | 0.70 | O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026. |
| 2026-04-02 | O Primo Rico | valuation | 0.80 | A PRIO3 subiu mais de 70% desde a recomendação da Finclass. |
| 2026-04-02 | O Primo Rico | guidance | 0.70 | A PRIO3 ainda é uma recomendação da Finclass, mas pode sair dependendo do preço do barril de petróleo ou da guerra. |
| 2026-03-31 | O Primo Rico | valuation | 0.80 | As ações da Prio subiram mais de 60% em três meses após recomendação da Finclass. |
| 2026-03-18 | O Primo Rico | valuation | 0.80 | As ações da PRIO3 subiram significativamente em dois meses, de R$40 para R$60. |
| 2026-03-17 | O Primo Rico | valuation | 0.80 | A ação da Prio3 subiu mais de 30% desde a recomendação de compra em janeiro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 62.75 | [Suno Dividendos] PRIO3 — peso 10.0%, rating Aguardar, PT R$62.75 |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PRIO3 — peso 2.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-02 | O Primo Rico | fed_path | neutral | O Federal Reserve americano manteve os juros pela segunda reunião consecutiva devido ao conflito no Irã, indi… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação está pressionada pelo aumento dos preços do petróleo e fertilizantes, afetando a cadeia de aliment… |
| 2026-04-02 | O Primo Rico | ipca_inflacao | bullish | A inflação no Brasil está aumentando devido ao aumento dos preços do diesel e fertilizantes, afetando o custo… |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\PRIO3.md` (cemetery archive)_

#### 🎯 Thesis: [[PRIO3]] — PetroRio

> E&P independente BR, puro play em **brownfield revitalization**. Breakeven ~$20-25/bbl dos mais baixos do mundo. Growth play, não DRIP.

##### Intent
**Compounder** (growth-primary, DY irrelevante). Capital gain driver = produção crescendo + preço Brent + execução M&A.

##### Business snapshot
- E&P pure-play offshore BR.
- Activos: Polvo, Tubarão Martelo, Frade, Wahoo (2025+), Albacora Leste (eventual).
- **Filosofia**: comprar campos maduros Majors abandonaram → reactivar com capex baixo → extrair upside operacional.
- Produção objectivo 2026: 120-140 Kboe/d (era ~30 Kboe/d em 2019).

##### Por que detemos

1. **Breakeven ultra-baixo** $20-25 — sobrevive Brent $40 com margem.
2. **Management best-in-class BR E&P** (Roberto Monteiro vendido IR prof + execução comprovada).
3. **Cash flow explosivo** em Brent > $70 — FCF margin 50%+ em good years.
4. **Zero state risk** (≠ [[PETR4]] interferência política Prates-era).
5. **Consolidação secular**: majors (Shell, Chevron) saindo offshore BR maduro → pipeline M&A.

##### Moat

- **Operational moat** — capacidade única de reactivar campos maduros sub-custo.
- **Relationship com ANP + Petrobras** (deal flow privilegiado).
- **Tax structure** (lucro reduzido via depreciação acelerada campos maduros).
- **Weak moat sobre preço Brent** — commodity price taker.

##### Cycle context

Ver [[Oil_cycle]]:
- **Fase actual (2026-04)**: discipline late → shortage setup.
- PRIO3 é **beta alto ao Brent** — amplifica movimentos.
- Brent $75-85 atual = comfort zone PRIO.
- Risk: Brent break < $60 sustained → FCF comprimido mas ainda positivo.
- Opportunity: Brent > $95 → special dividends + buyback aggressive.

##### Current state (2026-04)

- Production ramp Wahoo on-track 2H 2026.
- Debt/EBITDA ~1.2× (confortável para cycle).
- Buyback program activo.
- Optionality: Albacora Leste deal (TBD).

##### Invalidation triggers

- [ ] Brent < $50 sustained > 12m (cycle collapse)
- [ ] CEO/CTO departure sem sucessão clara (Roberto Monteiro é crítico)
- [ ] Major operational incident (blowout tipo Macondo, perda unidade)
- [ ] Políticas ANP/royalties adversas (hoje benignas)
- [ ] Debt/EBITDA > 2.5× pré-peak cycle (over-levering for M&A)
- [ ] Production guidance cut > 20%

##### Sizing

- Posição actual: 503 shares
- Position volátil por design — position size smaller que DRIP core holdings
- Target 5-7% sleeve BR equity
- **Não reinvest dividendos automaticamente** — capital gain é o driver; hold se tese intacta


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -13.01%
- **Drawdown 5y**: -13.01%
- **YTD**: +50.19%
- **YoY (1y)**: +88.63%
- **CAGR 3y**: +21.43%  |  **5y**: +27.84%  |  **10y**: +66.63%
- **Vol annual**: +35.83%
- **Sharpe 3y** (rf=4%): +0.51

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: annual
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Oil_and_Gas_cycle]] — sector framework (E&P vs majors)
- [[Oil_cycle]] — timing framework
- [[Brent_WTI]] — benchmark macro
- [[VALE3]] — outro commodity BR holding (diversifier)
- [[wiki/playbooks/Sell_triggers]] — regras exit

##### Memory refs

- `user_investment_intents.md` — PRIO3 classificada como Compounder growth

## ⚙️ Refresh commands

```bash
ii panorama PRIO3 --write
ii deepdive PRIO3 --save-obsidian
ii verdict PRIO3 --narrate --write
ii fv PRIO3
python -m analytics.fair_value_forward --ticker PRIO3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
