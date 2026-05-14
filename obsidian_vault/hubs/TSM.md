---
type: ticker_hub
ticker: TSM
market: us
sector: Technology
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 15
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# TSM — Taiwan Semiconductor

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Technology` · `market: US` · `currency: USD` · `bucket: holdings` · `15 sources merged`

## 🎯 Hoje

- **Posição**: 5.0 @ entry 102.47
- **Verdict (DB)**: `HOLD` (score 6.39, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 34.00 · P/B 61.16 · DY 1.1% · ROE 36.2% · ND/EBITDA -0.83 · Dividend streak 23 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\TSM.md` (cemetery archive)_

#### TSM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.tsmc.com/english
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=5.0 · entry=102.47 · date=2020-11-16

- Total events na DB: **864**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=404.5400085449219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.3621 · DY=0.010750481801893442 · P/E=34.605648
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 6-K | sec | 6-K |
| 2026-05-08 | 6-K | sec | 6-K |
| 2026-04-24 | 6-K | sec | 6-K |
| 2026-04-17 | 6-K | sec | 6-K |
| 2026-04-16 | 20-F | sec | 20-F |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_FILING_2026-05-12.md` (cemetery archive)_

#### Filing dossier — [[TSM]] · 2026-05-12

**Trigger**: `sec:6-K` no dia `2026-05-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1046179/000104617926000274/tsm-boardx20260512.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 400.60

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `183.46` |
| HOLD entre | `183.46` — `235.20` (consensus) |
| TRIM entre | `235.20` — `270.48` |
| **SELL acima de** | `270.48` |

_Método: `modern_compounder_pe20`. Consensus fair = R$235.20. Our fair (mais conservador) = R$183.46._

##### 🔍 Confidence

⚠️ **single_source** (score=0.40)
_(cvm_stale)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `modern_compounder_pe20` | 235.20 | 183.46 | 400.60 | SELL | single_source | `filing:sec:6-K:2026-05-12` |
| 2026-05-13T16:45:14+00:00 | `modern_compounder_pe20` | 235.20 | 183.46 | 400.60 | SELL | single_source | `manual` |
| 2026-05-11T20:40:44+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 404.54 | SELL | single_source | `manual` |
| 2026-05-11T12:53:42+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:19+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `manual` |
| 2026-05-09T20:37:09+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `manual` |
| 2026-05-09T13:08:36+00:00 | `modern_compounder_pe20` | 232.80 | 181.58 | 411.68 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `buffett_ceiling` | 19.61 | 15.30 | 411.68 | SELL | single_source | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-08 · Filing 2026-05-08
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[TSM]] · 2026-05-08

**Trigger**: `sec:6-K` no dia `2026-05-08`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1046179/000104617926000213/tsm-revenue20260508.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 419.50

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `10.55` |
| HOLD entre | `10.55` — `13.52` (consensus) |
| TRIM entre | `13.52` — `15.55` |
| **SELL acima de** | `15.55` |

_Método: `buffett_ceiling`. Consensus fair = R$13.52. Our fair (mais conservador) = R$10.55._

##### 🔍 Confidence

⚠️ **single_source** (score=0.40)
_(cvm_stale)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:03+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `filing:sec:6-K:2026-05-08` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:46+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-01 · Council review · Charlie Compounder
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Charlie Compounder\reviews\TSM_2026-05-01.md` (cemetery archive)_

#### Charlie Compounder sobre [[TSM_STORY|TSM]]

**Função no debate**: Industrials & Consumer US Specialist (Buffett frame) (`sector_specialist`)  
**Data**: 2026-05-01  
**Stance final**: ⚪ **NEEDS_DATA** *(R1 era BUY)*  

##### Round 1 — Abertura (cega aos colegas)

> _Taiwan Semiconductor mantém forte ROE e pagamentos de dividendos_

TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos. No entanto, o P/E de 33,85 é acima do limite.

**Métricas que invoquei**:
- ROE=36,2%
- DivStreak=23
- P/E=33,85

**Preocupações**:
- P/E acima da meta
- P/B muito elevado

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Taiwan Semiconductor apresenta um ROE de 36,21% e 23 anos consecutivos de dividendos, indicando solidez financeira - Mariana Macro

**Desafiei**:
- P/B de 87,86 sugere valorização do ativo líquido - Valentina Prudente | Este P/B elevado pode sugerir que o mercado está sobreavaliando os ativos líquidos da empresa, potencialmente indicando um risco de correção

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[TSM_STORY|📖 Storytelling completo (8 actos)]]
- [[TSM_COUNCIL|🏛️ Transcript do Council debate]]
- [[Charlie Compounder|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\TSM_2026-05-01.md` (cemetery archive)_

#### Mariana Macro sobre [[TSM_STORY|TSM]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _TSM mantém posição de compra com forte ROE e crescimento sustentável_

Taiwan Semiconductor apresenta um ROE de 36,21% e 23 anos consecutivos de dividendos, indicando solidez financeira. P/B de 87,86 sugere valorização do ativo líquido.

**Métricas que invoquei**:
- ROE=36,2%
- P/B=87,86
- DivStreak=23

**Preocupações**:
- ND/EBITDA=-0,83
- P/E=33,85

##### Round 2 — Resposta aos colegas

**Concordei com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiei**:
- P/E acima da meta | P/B muito elevado - Razão: Embora o P/E esteja alto, a empresa tem um histórico comprovado de crescimento sustentável. O P/B alto pode ser justificado pela valorização do mercado dos ativos líquidos da TSM - Charlie Compounder

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[TSM_STORY|📖 Storytelling completo (8 actos)]]
- [[TSM_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\TSM_2026-05-01.md` (cemetery archive)_

#### Pedro Alocação sobre [[TSM_STORY|TSM]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Taiwan Semiconductor mantém posição BUY com forte ROE e crescimento sustentável_

TSM apresenta um ROE de 36,21% e uma média de 23 anos de pagamentos de dividendos, indicando solidez financeira. A relação P/B de 87,86 sugere valorização do mercado.

**Métricas que invoquei**:
- ROE=36,2%
- P/B=87,86
- DivStreak=23

**Preocupações**:
- peso na carteira acima da média (8,7%)
- ND/EBITDA negativo (-0,83)

##### Round 2 — Resposta aos colegas

**Concordei com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiei**:
- P/E acima da meta | P/B muito elevado - Charlie Compounder: Embora o P/E esteja alto (33,85), a empresa tem um histórico comprovado de crescimento e lucratividade que pode justificar essa avaliação. O mesmo se aplica ao P/B, onde a valorização do mercado sugere confiança na solidez financeira da TSM

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[TSM_STORY|📖 Storytelling completo (8 actos)]]
- [[TSM_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\TSM_2026-05-01.md` (cemetery archive)_

#### Valentina Prudente sobre [[TSM_STORY|TSM]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Strong fundamentals and consistent dividend payments support long-term investment_

Taiwan Semiconductor demonstrates robust financial health with a high ROE of 36.2% and 23 consecutive years of dividend payments, indicating stability and growth potential.

**Métricas que invoquei**:
- ROE=36.2%
- Piotroski F-Score=8/9
- Altman Z-Score=3.04

**Preocupações**:
- High P/B ratio of 87.86 may indicate overvaluation
- Recent insider activity and legal issues could impact reputation

##### Round 2 — Resposta aos colegas

**Concordei com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiei**:
- P/E acima da meta | P/B muito elevado - Charlie Compounder; Esses são indicadores de valorização do mercado, não necessariamente um sinal de risco permanente de perda de capital.

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[TSM_STORY|📖 Storytelling completo (8 actos)]]
- [[TSM_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[TSM_STORY|TSM]] (Taiwan Semiconductor)

**Final stance**: ⚪ **NEEDS_DATA**  
**Confidence**: `low`  
**Modo (auto)**: A (US)  |  **Sector**: Technology  |  **Held**: sim  
**Elapsed**: 62.8s  |  **Failures**: 0

##### Quem esteve na sala

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- Taiwan Semiconductor apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Dissenso (preservado)**:
- Charlie Compounder disse que o P/B de 87,86 sugere valorização do ativo líquido pode indicar risco de correção; Mariana Macro, Valentina Prudente e Pedro Alocação disseram que embora o P/E esteja alto (33,85) e o P/B muito elevado (87,86), esses são indicadores da valorização do mercado que podem ser justificados pela solidez financeira e crescimento sustentável de TSM

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ P/B muito elevado pode sugerir sobreavaliação - Valentina Prudente
- ⚠️ ND/EBITDA negativo (-0,83) e peso na carteira acima da média (8,7%) - Pedro Alocação

**Sizing**: Considerar reduzir a posição para um nível mais confortável entre 2-4% do portfólio dada a sobreavaliação potencial indicada pelo P/B e ND/EBITDA negativo

##### Round 1 — Opening Statements (blind)

###### [[Charlie Compounder]] — 🟢 **BUY**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _Taiwan Semiconductor mantém forte ROE e pagamentos de dividendos_

TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos. No entanto, o P/E de 33,85 é acima do limite.

**Métricas**:
- ROE=36,2%
- DivStreak=23
- P/E=33,85

**Preocupações**:
- P/E acima da meta
- P/B muito elevado

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _TSM mantém posição de compra com forte ROE e crescimento sustentável_

Taiwan Semiconductor apresenta um ROE de 36,21% e 23 anos consecutivos de dividendos, indicando solidez financeira. P/B de 87,86 sugere valorização do ativo líquido.

**Métricas**:
- ROE=36,2%
- P/B=87,86
- DivStreak=23

**Preocupações**:
- ND/EBITDA=-0,83
- P/E=33,85

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Strong fundamentals and consistent dividend payments support long-term investment_

Taiwan Semiconductor demonstrates robust financial health with a high ROE of 36.2% and 23 consecutive years of dividend payments, indicating stability and growth potential.

**Métricas**:
- ROE=36.2%
- Piotroski F-Score=8/9
- Altman Z-Score=3.04

**Preocupações**:
- High P/B ratio of 87.86 may indicate overvaluation
- Recent insider activity and legal issues could impact reputation

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Taiwan Semiconductor mantém posição BUY com forte ROE e crescimento sustentável_

TSM apresenta um ROE de 36,21% e uma média de 23 anos de pagamentos de dividendos, indicando solidez financeira. A relação P/B de 87,86 sugere valorização do mercado.

**Métricas**:
- ROE=36,2%
- P/B=87,86
- DivStreak=23

**Preocupações**:
- peso na carteira acima da média (8,7%)
- ND/EBITDA negativo (-0,83)

##### Round 2 — Respostas (peers visíveis)

###### [[Charlie Compounder]] — ⚪ **NEEDS_DATA** *(stance flipped)*
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- Taiwan Semiconductor apresenta um ROE de 36,21% e 23 anos consecutivos de dividendos, indicando solidez financeira - Mariana Macro

**Desafiou**:
- P/B de 87,86 sugere valorização do ativo líquido - Valentina Prudente | Este P/B elevado pode sugerir que o mercado está sobreavaliando os ativos líquidos da empresa, potencialmente indicando um risco de correção

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiou**:
- P/E acima da meta | P/B muito elevado - Razão: Embora o P/E esteja alto, a empresa tem um histórico comprovado de crescimento sustentável. O P/B alto pode ser justificado pela valorização do mercado dos ativos líquidos da TSM - Charlie Compounder

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiou**:
- P/E acima da meta | P/B muito elevado - Charlie Compounder; Esses são indicadores de valorização do mercado, não necessariamente um sinal de risco permanente de perda de capital.

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- TSM apresenta um ROE sustentável de 36,21% e uma história consistente de dividendos por 23 anos - Charlie Compounder

**Desafiou**:
- P/E acima da meta | P/B muito elevado - Charlie Compounder: Embora o P/E esteja alto (33,85), a empresa tem um histórico comprovado de crescimento e lucratividade que pode justificar essa avaliação. O mesmo se aplica ao P/B, onde a valorização do mercado sugere confiança na solidez financeira da TSM

##### Documentos relacionados

- [[TSM_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[TSM_2026-05-01|Charlie Compounder]] em [[Charlie Compounder]]/reviews/
  - [[TSM_2026-05-01|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[TSM_2026-05-01|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[TSM_2026-05-01|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:TSM — Taiwan Semiconductor ===
Sector: Technology  |  Modo (auto): A  |  Held: True
Last price: 396.05999755859375 (2026-04-30)
Position: 5 shares @ entry 102.47
Fundamentals: P/E=33.85 | P/B=87.86 | DY=0.9% | ROE=36.2% | ND/EBITDA=-0.83 | DivStreak=23.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: Taiwan Semiconductor é uma excelente posição long-term para um investidor Buffett/Graham, devido à sua consistência em dividendos e forte retorno sobre o patrimônio líquido. Com 23 anos consecutivos de pagamentos de dividendos e um ROE de 36,21%, a empresa demonstra uma solidez financeira sólida e sustentável. A relação P/B de 56,30 indica que o mercado valoriza significativamente seu ativo líquido, sugerindo potencial para reavaliação positiva no futuro.

**Key assumptions**:
1. Taiwan Semiconductor continuará a aumentar seus lucros por ação (EPS) em um ritmo superior à média do setor.
2. A empresa manterá sua política de dividendos e ampliará o pagamento de dividendos nos próximos anos.
3. O mercado continuará a valorizar positivamente os ativos líquidos da

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 8.7%
  Sector weight: 19.3%

QUALITY SCORES:
  Piotroski F-Score: 8/9 (2025-12-31)
  Altman Z-Score: 3.04  zone=safe  conf=high
  Beneish M-Score: -2.70  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Taiwan Semiconductor Manufacturing (NYSE:TSM) Shares Up 2% on Analyst Upgrade - MarketBeat [Fri, 17 Ap]
    Image 1: MarketBeat - Stock Market News and Research Tools. +Shares+Up+2%25+on+Analyst+Upgrade%20https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-nysetsm-shares-up-2-on-analyst-upgrade-2026-04-17/ "Share on Twitt
  - Taiwan Semiconductor Manufacturing Company Ltd. $TSM Shares Sold by KBC Group NV - MarketBeat [Fri, 17 Ap]
    Image 7: MarketBeat - Stock Market News and Research Tools. The fund owned 212,124 shares of the semiconductor company's stock after selling 17,775 shares during the quarter. In other Taiwan Semiconductor Manufacturing news, VP Bor-Zen Tien
  - Taiwan Semiconductor Manufacturing Company Limited Reports Earnings Results for the First Quarter Ended March 31, 2026 - marketscreener.com [Thu, 16 Ap]
    © S&P Capital IQ - 2026  Share      Latest news about TSMC (Taiwan Semiconductor Manufacturing Company)  |  |  |  | | --- | --- | --- | | 08:04am | Hopes for Middle East Peace Nudge US Equity Futures Slightly Higher Pre-Bell | MT | | 07:23a
  - TSMC (NYSE: TSM) March revenue jumps 45% year over year - Stock Titan [Fri, 10 Ap]
    **Taiwan Semiconductor Manufacturing Company Limited** reported strong March 2026 results, with consolidated net revenue of **NT$415.19 billion**, up **30.7%** from February 2026 and **45.2%** from March 2025. TSMC and its subsidiaries deta
  - Taiwan Semiconductor Manufacturing Q1 Earnings, Net Revenue Rise; Q2 Revenue Outlook Set - marketscreener.com [Thu, 16 Ap]
    Employees  76,907  Sector  Semiconductors  Calendar  Jun. 11 -  Ex-dividend date - 6 TWD  More about the company  Income Statement and Estimates  More financial data  Analysis / Opinion  **What could shake TSMC?**  January 20, 2026 at 02:25

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[1] sec (6-K) [2026-04-24]: 6-K
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000104617926000205/tsm-monthend6kx20260424.htm
[2] sec (6-K) [2026-04-17]: 6-K
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000104617926000203/tsm-boardx20260417x6k.htm
[3] sec (20-F) [2026-04-16]: 20-F
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm
[4] sec (6-K) [2026-04-16]: 6-K
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000104617926000199/tsm-20260416x6k.htm
[5] sec (6-K) [2026-04-16]: 6-K
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000104617926000201/tsm_20260416.htm
[6] sec (6-K) [2026-04-10]: 6-K
     URL: https://www.sec.gov/Archives/edgar/data/1046179/000104617926000136/tsm-revenue20260410.htm

##### BIBLIOTHECA (livros/clippings RAG) (1 hits)
[7] Bibliotheca: clip_investments_chasecom: Self-Directed (...0231)

As of 10:42 AM ET 04/26/2026

Self-Directed (...0231)

##### Account value

$22,903.99

$0.00

Day's gain/loss

Day's gain/loss

$0.00

Gain of +$4,691.82

Total gain/loss

Total gain/loss

Gain of +$4,691.82

$492.26

Estimated annual income

Estimated annual income

$492.26



##### TAVILY NEWS (≤30d) (5 hits)
[8] Tavily [Fri, 17 Ap]: Image 1: MarketBeat - Stock Market News and Research Tools. +Shares+Up+2%25+on+Analyst+Upgrade%20https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-nysetsm-shares-up-2-on-analyst-upgrade-2026-04-17/ "Share on Twitter")+Shares+Up+2%25+on+Analyst+Upgrade%20https://www.marketb
     URL: https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-nysetsm-shares-up-2-on-analyst-upgrade-2026-04-17/
[9] Tavily [Fri, 17 Ap]: Image 7: MarketBeat - Stock Market News and Research Tools. The fund owned 212,124 shares of the semiconductor company's stock after selling 17,775 shares during the quarter. In other Taiwan Semiconductor Manufacturing news, VP Bor-Zen Tien purchased 1,000 shares of Taiwan Semiconductor Manufacturin
     URL: https://www.marketbeat.com/instant-alerts/filing-taiwan-semiconductor-manufacturing-company-ltd-tsm-shares-sold-by-kbc-group-nv-2026-04-17/
[10] Tavily [Thu, 16 Ap]: © S&P Capital IQ - 2026  Share      Latest news about TSMC (Taiwan Semiconductor Manufacturing Company)  |  |  |  | | --- | --- | --- | | 08:04am | Hopes for Middle East Peace Nudge US Equity Futures Slightly Higher Pre-Bell | MT | | 07:23am | Corporate Earnings, Geopolitics Undergird Wall Street Pr
     URL: https://www.marketscreener.com/news/taiwan-semiconductor-manufacturing-company-limited-reports-earnings-results-for-the-first-quarter-en-ce7e50dddd8fff24
[11] Tavily [Sun, 26 Ap]: # Verdence Capital Advisors LLC Increases Stock Position in Taiwan Semiconductor Manufacturing Company Ltd. Image 20: Taiwan Semiconductor Manufacturing logo with Computer and Technology background. # Verdence Capital Advisors LLC Increases Stock Position in Taiwan Semiconductor Manufacturing Compan
     URL: https://www.marketbeat.com/instant-alerts/filing-verdence-capital-advisors-llc-increases-stock-position-in-taiwan-semiconductor-manufacturing-company-ltd-tsm-2026-04-26/
[12] Tavily [Fri, 17 Ap]: Image 1: MarketBeat - Stock Market News and Research Tools. %20%24TSM%20%23TSM%20https://www.marketbeat.com/instant-alerts/da-davidson-reaffirms-buy-rating-for-taiwan-semiconductor-manufacturing-nysetsm-2026-04-17/ "Share on Twitter")%20https://www.marketbeat.com/instant-alerts/da-davidson-reaffirms
     URL: https://www.marketbeat.com/instant-alerts/da-davidson-reaffirms-buy-rating-for-taiwan-semiconductor-manufacturing-nysetsm-2026-04-17/

##### TAVILY GUIDANCE (≤90d) (5 hits)
[13] Tavily [Fri, 10 Ap]: **Taiwan Semiconductor Manufacturing Company Limited** reported strong March 2026 results, with consolidated net revenue of **NT$415.19 billion**, up **30.7%** from February 2026 and **45.2%** from March 2025. TSMC and its subsidiaries detailed foreign-exchange derivative positions, largely forwards
     URL: https://www.stocktitan.net/sec-filings/TSM/6-k-taiwan-semiconductor-manufacturing-co-ltd-current-report-foreign--ad634bdd2780.html
[14] Tavily [Thu, 16 Ap]: © S&P Capital IQ - 2026  Share      Latest news about TSMC (Taiwan Semiconductor Manufacturing Company)  |  |  |  | | --- | --- | --- | | 08:04am | Hopes for Middle East Peace Nudge US Equity Futures Slightly Higher Pre-Bell | MT | | 07:23am | Corporate Earnings, Geopolitics Undergird Wall Street Pr
     URL: https://www.marketscreener.com/news/taiwan-semiconductor-manufacturing-company-limited-reports-earnings-results-for-the-first-quarter-en-ce7e50dddd8fff24
[15] Tavily [Thu, 16 Ap]: Employees  76,907  Sector  Semiconductors  Calendar  Jun. 11 -  Ex-dividend date - 6 TWD  More about the company  Income Statement and Estimates  More financial data  Analysis / Opinion  **What could shake TSMC?**  January 20, 2026 at 02:25 am EST  **TSMC Eyes Smaller Gap Between US, Taiwan Chipmaki
     URL: https://www.marketscreener.com/news/taiwan-semiconductor-manufacturing-q1-earnings-net-revenue-rise-q2-revenue-outlook-set-ce7e50ddda8ef426
[16] Tavily [Mon, 06 Ap]: # Taiwan Semiconductor Manufacturing Company Limited (TSM). Is TSM a buy now? This price reflects trading activity during the overnight session on the Blue Ocean ATS, available 8 PM to 4 AM ET, Sunday through Thursday, when regular markets are closed. Is TSM a buy now? Chart does not reflect overnig
     URL: https://ca.finance.yahoo.com/quote/TSM/
[17] Tavily [Tue, 17 Ma]: The company notifies holders of its American Depositary Shares that they may submit proposed resolutions for the 2026 Annual Shareholders’ Meeting during a defined submission window. Pursuant to the Depository Agreement for the Taiwan Semiconductor 

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_STORY.md` (cemetery archive)_

#### Taiwan Semiconductor — TSM

##### Análise de Investimento · Modo FULL · Jurisdição US

*1 de Maio de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/TSM_2026-05-01.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (5 hits) |
| **2 — Metric Engine** | Receita R$ 3809.1 bi · EBITDA est. R$ 2259.43 bi · FCF R$ 992.38 bi · ROE 36% · DGR 19.3% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 8/9 · Altman Z=3.04 (safe) · Beneish M=-2.70 (clean) |
| **5 — Classification** | Modo A-US · Growth (8/12) · Value (7/12) |
| **5.5 — Council Debate** | NEEDS_DATA (low) · 1 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. Taiwan Semiconductor Manufacturing (NYSE: TSM), uma empresa líder global no setor de tecnologia, é conhecida por sua capacidade excepcional na fabricação de semicondutores para clientes em todo o mundo. Com sede não especificada nas fontes consultadas, a companhia opera um modelo de negócio que se concentra fortemente na produção e desenvolvimento de chips avançados, essenciais para uma ampla gama de aplicações tecnológicas, desde smartphones até supercomputadores.

A empresa enfrenta frequentemente a armadilha do investidor que confunde sua marca com seu diferencial competitivo. Enquanto Taiwan Semiconductor é reconhecida globalmente por seus produtos de alta qualidade e eficiência, o verdadeiro valor da companhia reside em suas capacidades únicas de fabricação e inovação tecnológica contínua. Esta distinção é crucial para entender que a empresa não se limita apenas à produção de semicondutores, mas também ao desenvolvimento de processos avançados que permitem a criação de chips cada vez mais eficientes e compactos.

Competitivamente, Taiwan Semiconductor posiciona-se como um líder incontestável no mercado de fabricação de semicondutores. A empresa mantém uma vantagem significativa sobre seus concorrentes através da sua capacidade técnica avançada e investimentos contínuos em pesquisa e desenvolvimento, o que lhe permite manter a liderança na produção de chips de última geração.

##### Ato 2 — O Contexto

O panorama macroeconômico atual apresenta um cenário complexo para Taiwan Semiconductor Manufacturing. Com uma taxa do Federal Funds entre 4,25% e 4,50%, juros mais altos pressionam os custos de capital, enquanto a taxa dos títulos do Tesouro dos EUA a dez anos se mantém em cerca de 4,2%. Este ambiente financeiro desafiador é ainda mais acentuado pelo custo de capital próprio (Ke) estimado em aproximadamente 10%, indicando um nível significativo de exigência para retornos acima do mercado.

O ciclo econômico atual está no final da expansão e início do amaciamento, o que sugere uma desaceleração gradual das atividades econômicas. Este cenário macroeconômico tem implicações diretas para o setor de semicondutores, já que a demanda por produtos tecnológicos pode diminuir em um ambiente de crescimento mais lento.

Para Taiwan Semiconductor Manufacturing, este contexto exige uma abordagem cautelosa e estratégica. A empresa precisa continuar investindo em inovação e eficiência operacional para manter sua liderança no mercado, mesmo diante das pressões econômicas. Além disso, a estabilidade geopolítica continua sendo um fator crucial, com tensões comerciais e disputas de propriedade intelectual potencialmente afetando os negócios da empresa.

As notícias recentes sobre ações judiciais envolvendo ex-executivos que supostamente violaram acordos de confidencialidade destacam o ambiente competitivo e litigioso no qual Taiwan Semiconductor opera. Estas disputas podem ter implicações significativas para a reputação da empresa e suas relações com parceiros estratégicos, como Intel.

Em resumo, enquanto Taiwan Semiconductor enfrenta desafios econômicos e regulatórios, sua posição de liderança e foco em inovação tecnológica continuam sendo seus principais ativos.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa e dinâmica, marcada por altos e baixos que refletem tanto desafios quanto oportunidades no mercado. As métricas financeiras fornecidas permitem traçar um panorama detalhado do desempenho da empresa desde 2022 até as previsões para 2025, com destaque para o ano de 2026.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 2263.89B | R$ 1155.82B | R$ 1271.40B | 56.2% | R$ 992.92B | 43.9% | R$ 520.97B |
| 2023 | R$ 2161.74B | R$ 991.32B | R$ 1090.45B | 50.4% | R$ 851.74B | 39.4% | R$ 286.57B |
| 2024 | R$ 2894.31B | R$ 1416.34B | R$ 1557.97B | 53.8% | R$ 1158.38B | 40.0% | R$ 861.20B |
| 2025 | R$ 3809.05B | R$ 2054.03B | R$ 2259.43B | 59.3% | R$ 1697.60B | 44.6% | R$ 992.38B |

A receita da empresa registrou um crescimento anual composto (CAGR) de aproximadamente 17,5% entre 2022 e 2025, com uma recuperação significativa em 2024 após o declínio observado em 2023. A expansão da margem EBITDA de 56,2% para 59,3% no período reflete a eficiência operacional e a capacidade da empresa de gerir custos em um cenário desafiador.

O fluxo de caixa livre (FCF) demonstrou uma trajetória instável, com picos e vales que podem ser atribuídos a fatores como investimentos em capital de giro e expansão de ativos. Em 2023, o FCF diminuiu para R$ 286,57 bilhões, mas recuperou-se significativamente no ano seguinte, alcançando R$ 861,20 bilhões em 2024.

Em relação aos dividendos, a empresa manteve uma política consistente de distribuição de proventos ao longo dos anos. A tabela abaixo ilustra o histórico de dividendos:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 1.289 |
| 2021 | 1.892 |
| 2022 | 1.856 |
| 2023 | 1.847 |
| 2024 | 2.340 |
| 2025 | 3.121 |
| 2026 | 0.956 |

O Dividend Growth Ratio (DGR) da empresa, calculado a partir de dividendos regulares e sem considerar ajustes extraordinários, é de 19,3% ao ano. Este crescimento constante reforça a tese de reinvestimento em dividendos (DRIP), incentivando os acionistas a manter suas participações na empresa.

É importante notar que o Dividend Yield (DY) total reportado pode ser influenciado por ajustes extraordinários, enquanto o DY estrutural reflete um rendimento mais consistente e sustentável. No caso da empresa em questão, o DY estrutural é de 0,86%, indicando uma distribuição de dividendos moderada.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A análise do fluxo de caixa livre oferece um retrato mais preciso da geração de valor pela empresa, destacando a importância deste indicador para avaliar o desempenho financeiro real.

##### Ato 4 — O Balanço

O balanço atual da empresa apresenta uma série de métricas que permitem avaliar sua saúde financeira e capacidade de criação de valor. Com um preço-earnings (P/E) de 33,85 e um preço-book (P/B) de 87,86, a empresa é considerada carregada em comparação com o mercado, sugerindo que os investidores atribuem um alto potencial de crescimento futuro.

O Dividend Yield (DY) da empresa é de apenas 0.86%, indicando uma distribuição de dividendos moderada e refletindo a prioridade da empresa em reinvestir lucros para impulsionar o crescimento orgânico.

A relação Net Debt/EBITDA, calculada com base no endividamento líquido estimado (R$ 532.29 bilhões) e na margem EBITDA mais recente (59,3%), é de aproximadamente 0,47x, indicando uma posição financeira sólida e um nível moderado de alavancagem.

O Return on Equity (ROE) da empresa é de 36,21%, superando o custo do capital próprio estimado no Brasil de cerca de 18,25%. Este desempenho robusto sugere que a empresa está criando valor significativo para seus acionistas.

O Current Ratio da empresa não foi fornecido diretamente nos dados disponíveis. No entanto, é fundamental avaliar esta métrica para entender a capacidade da empresa de honrar suas obrigações curtas prazo com base em ativos líquidos circulantes. 

Não foram identificados sinais claros de despesa financeira crescente ou alavancagem excessiva que possam representar riscos imediatamente prementes para a empresa, embora seja sempre recomendável monitorar estes indicadores ao longo do tempo.

Em resumo, o balanço da empresa reflete um cenário promissor de criação de valor e sustentabilidade financeira, apesar dos desafios enfrentados no mercado.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa revela uma posição distintiva no mercado tanto em comparação com seus pares como com os índices de referência. O preço-lucro (P/E) da empresa está atualmente em 33,85x, significativamente acima do múltiplo médio setorial de 22,15x e do índice S&P 500 que se situa em 21,00x. Este elevado múltiplo reflete uma avaliação mais otimista dos investidores quanto ao potencial futuro da empresa.

No que diz respeito à relação preço-benefício (P/B), a empresa apresenta um valor de 87,86x, muito superior não apenas aos seus pares setoriais com média de 6,58x, mas também ao índice Ibovespa, cujo múltiplo é de 3,50x. Este indicador sugere que os investidores estão dispostos a pagar um preço significativamente maior em relação aos ativos tangíveis da empresa comparado com outros players do setor.

A taxa de dividend yield (DY) da empresa é de 0,86%, inferior à média setorial de 1,3% e ao índice S&P 500 que registra 1,5%. Este DY pode incluir dividendos extraordinários ou não ser estruturalmente representativo do payout da companhia. É importante notar que a empresa tem uma sequência de pagamentos consecutivos de dividendos sem interrupções por 23 anos, o que indica consistência na política de distribuição de lucros.

O fluxo de caixa livre (FCF) yield da empresa é de 50%, um valor muito superior à média setorial de 2,5% e ao índice S&P 500 com 4%. Este indicador destaca a capacidade da empresa em gerar fluxos de caixa líquidos consideravelmente maiores do que seus pares.

O retorno sobre o patrimônio (ROE) da empresa é de 36,21%, superior à média setorial de 26% e ao índice S&P 500 com 16%. Este resultado reflete a eficiência na geração de lucros por parte da empresa em relação aos seus ativos totais.

Por último, o múltiplo negativo de dívida sobre EBITDA (ND/EBITDA) da empresa é de -0,83x, indicando que a empresa tem um fluxo de caixa operacional suficiente para cobrir suas obrigações de dívida. Este valor contrasta com o múltiplo médio setorial de 0,15x.

| Múltiplo | TSM | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 33.85x | 22.15x | 21.00x |
| P/B | 87.86x | 6.58x | 3.50x |
| DY | 0.9% | 1.3% | 1.5% |
| FCF Yield | 50.0% | 2.5% | 4.0% |
| ROE | 36.2% | 26.0% | 16.0% |
| ND/EBITDA | -0,83x | 0.15x | — |

##### Ato 6 — Os Quality Scores

Os indicadores de qualidade financeira da empresa destacam um desempenho sólido e consistente ao longo do tempo. O Piotroski F-Score da companhia é de 8/9, o que indica uma forte saúde operacional e financeira. Este resultado reflete a presença de oito dos nove critérios positivos estabelecidos pelo modelo, indicando um desempenho robusto em termos de lucratividade, crescimento do caixa e gestão da dívida.

O Altman Z-Score da empresa é de 3.04, situado na zona segura com uma confiança alta. Este resultado sugere que a companhia tem um baixo risco de insolvência em comparação com outros players do setor e o mercado geral. Além disso, o Z-Score conservador da empresa é igual ao ajustado (ambos 3.04), indicando uma consistência na avaliação.

O M-score de Beneish da companhia é -2,70, posicionando-a na zona limpa com alta confiança. Este resultado sugere que a empresa não está manipulando seus resultados financeiros e apresenta um comportamento contábil transparente e honesto.

Em resumo, os indicadores de qualidade financeira da empresa apontam para uma posição sólida em termos de saúde operacional, gestão de risco e transparência contábil.

---

##### Ato 7 — O Moat e a Gestão

A Taiwan Semiconductor Manufacturing Company (TSMC) é uma empresa que tem demonstrado um moat significativo no setor de semicondutores, classificado como "Wide" por sua capacidade de manter liderança em tecnologia avançada e eficiência operacional. Este moat se deve a vários fatores:

1. **Custo/Escala**: TSMC opera na escala mais elevada do setor, permitindo que a empresa obtenha economias significativas através da produção em massa de semicondutores avançados. A capacidade de investir massivamente em tecnologia e infraestrutura para manter-se à frente dos concorrentes é um forte indicador deste moat.

2. **Switching Costs**: As empresas que dependem de TSMC para a produção de seus chips enfrentam altos custos de mudança se decidirem migrar para fornecedores alternativos, especialmente em tecnologias avançadas como 5nm e abaixo. Esses custos incluem tempo de desenvolvimento adicional e perda de competitividade no mercado.

3. **Intangíveis**: TSMC possui uma forte reputação e marca estabelecida na indústria, além de um portfólio significativo de patentes e direitos autorais que protegem suas tecnologias avançadas. Esses ativos intangíveis criam uma barreira à entrada para novos competidores.

4. **Eficiência Operacional**: A empresa tem demonstrado consistente eficiência operacional através da otimização de seus processos e investimentos em automação, mantendo um ritmo constante de inovação tecnológica que lhe permite manter a liderança no setor.

5. **Network Effects**: Embora menos evidente neste segmento do mercado, TSMC beneficia-se de uma rede de clientes satisfeitos e fornecedores confiáveis que contribuem para sua posição dominante. A integração profunda com grandes fabricantes de semicondutores como Apple e NVIDIA cria um efeito em cascata positivo.

Quanto à gestão, o envolvimento ativo dos insiders demonstra a confiança na direção da empresa. No último relatório, foi mencionado que KBC Group NV vendeu 17.775 ações durante o trimestre, reduzindo sua posição para 212.124 ações. Por outro lado, Bor-Zen Tien, Vice-Presidente, adquiriu 1.000 ações recentemente, indicando uma visão positiva sobre o futuro da empresa.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico de Taiwan Semiconductor Manufacturing Company (TSMC) é classificado como Growth com um score de 8 e Value com um score de 7. As pontuações detalhadas são as seguintes

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TSM_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\TSM_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — TSM             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              5
  Entry price.........: US$      102.47
  Cost basis..........: US$      512.35
  Price now...........: US$      402.46
  Market value now....: US$    2,012.30  [+292.8% nao-realizado]
  DY t12m.............: 0.84%  (R$/US$ 3.3930/share)
  DY vs own 10y.......: P 1 [EXPENSIVE]  (actual 0.84% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=23  hist_g_5y=0.133  hist_g_raw=0.133  gordon_g=0.257  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +10.64%       |
  | base         |  +18.00%  |   +0.00% |  +18.84%       |
  | optimista    |  +22.00%  |   +1.00% |  +23.84%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     14       |      >40       |        1       |
  | base         |     11       |      >40       |        1       |
  | optimista    |     10       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      3,353 | US$      4,801 | US$      5,902 |
  |  10y  | US$      5,598 | US$     11,454 | US$     17,283 |
  |  15y  | US$      9,366 | US$     27,328 | US$     50,530 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TSM.md` (cemetery archive)_

#### TSM — Taiwan Semiconductor

#holding #us #technology

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 6.3/10  |  **Confiança**: 70%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 10.0/10 | 35% | `██████████` |
| Valuation  | 2.0/10 | 30% | `██░░░░░░░░` |
| Momentum   | 8.0/10 | 20% | `████████░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z 3.040456662709355 (SAFE), Piotroski 8/9 (STRONG), DivSafety 95.0/100
- **Valuation**: Screen 0.40, DY percentil P0 (EXPENSIVE)
- **Momentum**: 1d 6.36%, 30d 14.78%, YTD 31.25%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- total 6.3 na zona neutra
- quality forte
- valuation caro

##### Links

- Sector: [[sectors/Technology|Technology]]
- Market: [[markets/US|US]]
- Peers: [[AAPL]] · [[ACN]] · [[PLTR]] · [[IBM]] · [[JKHY]]
- 🎯 **Thesis**: [[wiki/holdings/TSM|thesis deep]]

##### Snapshot

- **Preço**: $419.50  (2026-05-06)    _+6.36% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: 3.04 (safe)
- **Piotroski**: 8/9
- **Div Safety**: 95.0/100 (SAFE)
- **Posição**: 5.0 sh @ $102.47  →  P&L 309.39%

##### Fundamentals

- P/E: 36.16379 | P/B: 93.05788 | DY: 0.81%
- ROE: 36.21% | EPS: 11.6 | BVPS: 4.5079474
- Streak div: 23y | Aristocrat: False

##### Dividendos recentes

- 2026-06-11: $0.9560
- 2026-03-17: $0.9560
- 2025-12-11: $0.8350
- 2025-09-16: $0.8220
- 2025-06-12: $0.7800

##### Eventos (SEC/CVM)

- **2026-04-24** `6-K` — 6-K
- **2026-04-17** `6-K` — 6-K
- **2026-04-16** `20-F` — 20-F
- **2026-04-16** `6-K` — 6-K
- **2026-04-16** `6-K` — 6-K

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=1 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O apresentador menciona ter vendido TSMC recentemente. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: +0.00%
- **Drawdown 5y**: +0.00%
- **YTD**: +31.25%
- **YoY (1y)**: +143.50%
- **CAGR 3y**: +70.28%  |  **5y**: +29.13%  |  **10y**: +33.45%
- **Vol annual**: +38.54%
- **Sharpe 3y** (rf=4%): +1.75

###### Dividendos
- **DY 5y avg**: +1.61%
- **Div CAGR 5y**: +13.33%
- **Frequency**: quarterly
- **Streak** (sem cortes): 6 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $2263.89B | $992.92B | $520.97B |
| 2023-12-31 | $2161.74B | $851.74B | $286.57B |
| 2024-12-31 | $2894.31B | $1158.38B | $861.20B |
| 2025-12-31 | $3809.05B | $1697.60B | $992.38B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "TSM — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: TSM
    data: [175.22, 194.76, 193.45, 197.68, 194.84, 205.18, 215.43, 213.5, 222.74, 224.68, 227.86, 228.67, 240.4, 241.6, 242.91, 232.47, 242.09, 238.88, 227.33, 239.29, 231.39, 250.92, 261.38, 264.87, 276.66, 288.47, 294.03, 302.89, 295.08, 290.73, 305.09, 294.05, 295.27, 284.82, 277.5, 289.96, 295.45, 303.41, 287.74, 288.95, 302.84, 319.61, 318.01, 327.11, 326.12, 338.34, 341.36, 348.85, 368.1, 360.39, 387.73, 353.13, 348.7, 338.31, 338.79, 347.75, 337.95, 345.32, 369.57, 370.5, 382.66, 392.34, 401.61]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-15', '2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: P/E
    data: [36.119118, 34.69532, 31.162094, 31.857265, 31.628117, 31.513697, 34.486717, 34.486717, 34.486717, 34.702656, 33.64837, 33.68948, 33.851284, 34.47296, 33.85494, 36.16379]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-15', '2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: ROE %
    data: [35.06, 35.06, 36.6, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21, 36.21]
  - title: DY %
    data: [92.0, 93.0, 97.0, 95.0, 95.0, 0.92, 0.84, 0.84, 0.84, 0.84, 0.86, 0.86, 0.86, 0.84, 0.86, 0.81]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TSM_DOSSIE.md` (cemetery archive)_

#### 📑 TSM — Taiwan Semiconductor

> Generated **2026-04-26** by `ii dossier TSM`. Cross-links: [[TSM]] · [[TSM_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

TSM negoceia a P/E 34.49 com DY 0.84% e ROE 36.21%, IC HOLD com confiança média (60% consenso). Achado-chave: **YoY +143.8%** após onda AI/Nvidia — múltiplos esticados mas moat técnico (3nm/2nm) é dos mais defensáveis em tech. Posição growth/tech (não pure DRIP) — manter para compounding mas sem reforçar nos níveis actuais.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 11.67  |  **BVPS**: 4.51
- **ROE**: 36.21%  |  **P/E**: 34.49  |  **P/B**: 89.28
- **DY**: 0.84%  |  **Streak div**: 23y  |  **Market cap**: USD 2087.32B
- **Last price**: USD 402.46 (2026-04-26)  |  **YoY**: +143.8%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[TSM_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-24)**: Taiwan Semiconductor é uma excelente posição long-term para um investidor Buffett/Graham, devido à sua consistência em dividendos e forte retorno sobre o patrimônio líquido. Com 23 anos consecutivos de pagamentos de dividendos e um ROE de 36,21%, a empresa demonstra uma solidez financeira sólida e sustentável. A relação P/B de 56,30 indica que o mercado valoriza significativamente seu ativo líquido, sugerindo potencial para reavaliação positiva no futuro.

**Key assumptions**:
1. Taiwan Semiconductor continuará a aumentar seus lucros por ação (EPS) em um ritmo superior à média do setor.
2. A empresa manterá sua política de dividendos e ampliará o pagamento de dividendos nos próximos anos.
3. O mercado continuará a valorizar positivamente os ativos líquidos da

→ Vault: [[TSM]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 34.49** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 34.49** esticado vs critério.
- **P/B = 89.28** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **89.28** esticado.
- **DY = 0.84%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.84%** fraco; verificar se é growth pick.
- **ROE = 36.21%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **36.21%** compounder-grade.
- **Graham Number ≈ R$ 34.41** vs preço **R$ 402.46** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 23y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🔴 **Geopolítica China/Taiwan** — risco existencial; uma escalada militar invalida a tese. Trigger: `events` table tagged geopolitical action; Pentagon/MOFA escalation.
- 🟡 **Concentração de clientes (Apple + Nvidia)** — top-2 ~35% receita; perda de socket é material. Trigger: customer concentration disclosed > 30% single client.
- 🟡 **Capex cycle (2nm/3nm + Arizona/Japan fabs)** — capex elevado pressiona FCF se demand AI desacelerar. Trigger: FCF YoY < -20% por 2 trimestres.
- 🟡 **Valuation stretch após onda AI** — P/E 34 vs histórico 18-22; mean-reversion possível. Trigger: `fundamentals.pe > 40`.

##### 5. Position sizing

**Status atual**: holding (in portfolio)

**Manter para compounding** — posição growth/tech (não DRIP). Após +143.8% YoY, não acelerar reforços; usar pullbacks de -15%+ para adicionar selectivamente. Pesar limit ≤ 7-8% portfolio devido ao risco geopolítico binário. USD em conta US.

##### 6. Tracking triggers (auto-monitoring)

- **PE overstretch** — `fundamentals.pe > 40` → trim candidate.
- **Geopolitical event** — `events` flagged Taiwan/China escalation → emergency review.
- **Earnings miss** — `events.kind='earnings'` surprise < -10% → reavaliar.
- **ROE quebra** — `fundamentals.roe < 0.20` → moat erosion sinal.
- **Conviction drop** — `conviction_scores.composite_score < 60` → reduce.

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
*Generated by `ii dossier TSM` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=1 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O apresentador menciona ter vendido TSMC recentemente. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TSM_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — TSM

**Committee verdict**: **AVOID** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=2 | AVOID=3  
**Avg conviction majority**: 5.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Preço muito alto (PE 35, PB 62)
- Risco geopolítico e regulatório
- Complexidade do negócio
- Leverage cíclica

**Key risk**: Exposição a riscos geopolíticos e regulatórios na indústria de semicondutores

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/B elevado indica sobreavaliação
- ROE forte, mas dividendos baixos
- Mercado institucional reduz exposição

**Key risk**: Sobrea valorização do ativo líquido pode levar a reavaliação negativa

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/E muito alto
- Falta de anti-fragilidade
- Risco geopolítico significativo

**Key risk**: Geopolitical instability and high valuation risks outweigh potential long-term benefits.

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Preço muito acima do valor intrínseco
- Margem de segurança insuficiente
- Risco de reversão de múltiplos

**Key risk**: Reavaliação negativa dos múltiplos devido a condições macroeconômicas

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/B alto indica valorização significativa
- ROE forte e dividendos consistentes
- Aumento de posições por alguns gestores

**Key risk**: Mercado pode reavaliar o múltiplo P/B em um cenário de desaceleração econômica

##### 📊 Context provided

```
TICKER: US:TSM

FUNDAMENTALS LATEST:
  pe: 35.367695
  pb: 62.973495
  dy: 1.06%
  roe: 36.21%
  net_debt_ebitda: -0.8287645168907426
  intangible_pct_assets: 0.3%   (goodwill $5.9B + intangibles $19.1B)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: Taiwan Semiconductor é uma excelente posição long-term para um investidor Buffett/Graham, devido à sua consistência em dividendos e forte retorno sobre o patrimônio líquido. Com 23 anos consecutivos de pagamentos de dividendos e um ROE de 36,21%, a empresa demonstra uma solidez financeira sólida e sustentável. A relação P/B de 56,30 indica que o mercado valoriza significativamente seu ativo líquido, sugerindo potencial para reavaliação positiva no futuro.

**Key assumptions**:
1. Taiwan Semiconductor continuará a aumentar seus lucros por ação (EPS) em um ritmo superior à média do setor.
2. A empresa manterá sua política de dividendos e ampliará o pagamento de dividendos nos próximos anos.
3. O mercado continuará a valorizar positivamente os ativos líquidos da

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Taiwan Semiconductor Manufacturing Company Ltd. $TSM Shares Sold by Matthews International Capital Management LLC - Mark [Sat, 25 Ap]
    Image 7: MarketBeat - Stock Market News and Research Tools. Taiwan Semiconductor Manufacturing makes up approximately 3.0% of Matthews International Capital Management LLC's portfolio, making the stoc
  - Boyer Financial Services Inc. Invests $648,000 in Taiwan Semiconductor Manufacturing Company Ltd. $TSM - MarketBeat [Tue, 28 Ap]
    # Boyer Financial Services Inc. Invests $648,000 in Taiwan Semiconductor Manufacturing Company Ltd. Image 20: Taiwan Semiconductor Manufacturing logo with Computer and Technology background. Image 7: 
  - Verdence Capital Advisors LLC Increases Stock Position in Taiwan Semiconductor Manufacturing Company Ltd. $TSM - MarketB [Sun, 26 Ap]
    # Verdence Capital Advisors LLC Incr
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=1 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O apresentador menciona ter vendido TSMC recentemente. |

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TSM_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — TSM

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `low_consensus_long` (magnitude 1/5)  
**Interpretation**: consensus pick — no edge

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: bullish (4 bull / 0 bear / 1 neutral)  
**Cached**: True

- 🟢 [bull] [Taiwan Semiconductor Manufacturing (NYSE:TSM) Shares Up 2% on Analyst Upgrade - MarketBeat](https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-nysetsm-shares-up-2-on-analyst-upgrade-2026-04-17/) (Fri, 17 Ap)
- 🟡 [neutral] [Taiwan Semiconductor Manufacturing (NYSE:TSM) Stock Price Down 1.3% - What's Next? - MarketBeat](https://www.marketbeat.com/instant-alerts/taiwan-semiconductor-manufacturing-nysetsm-stock-price-down-13-whats-next-2026-04-23/) (Thu, 23 Ap)
- 🟢 [bull] [Mivtachim The Workers Social Insurance Fund Ltd. Under Special Management Sells 24,000 Shares of Taiwan Semiconductor Ma](https://www.marketbeat.com/instant-alerts/filing-mivtachim-the-workers-social-insurance-fund-ltd-under-special-management-sells-24000-shares-of-taiwan-semiconductor-manufacturing-company-ltd-tsm-2026-04-25/) (Sat, 25 Ap)
- 🟢 [bull] [1,419 Shares in Taiwan Semiconductor Manufacturing Company Ltd. $TSM Acquired by Watershed Private Wealth LLC - MarketBe](https://www.marketbeat.com/instant-alerts/filing-1419-shares-in-taiwan-semiconductor-manufacturing-company-ltd-tsm-acquired-by-watershed-private-wealth-llc-2026-04-13/) (Mon, 13 Ap)
- 🟢 [bull] [Taiwan Semiconductor Manufacturing (TSM) – Among the Best Global Stocks to Buy According to Wall Street Analysts - Insid](https://www.insidermonkey.com/blog/taiwan-semiconductor-manufacturing-tsm-among-the-best-global-stocks-to-buy-according-to-wall-street-analysts-1745092/) (Thu, 23 Ap)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: Taiwan Semiconductor é uma excelente posição long-term para um investidor Buffett/Graham, devido à sua consistência em dividendos e forte retorno sobre o patrimônio líquido. Com 23 anos consecutivos de pagamentos de dividendos e um ROE de 36,21%, a empresa demonstra uma solidez financeira sólida e sustentável. A relação P/B de 56,30 indica que o mercado valoriza significativamente seu ativo líquido, sugerindo potencial para reavaliação positiva no futuro.

**Key assumptions**:
1. Taiwan Semiconductor continuará a aumentar seus lucros por ação (EPS) em um ritmo superior à média do setor.
2. A empresa manterá sua política de dividendos e ampliará o pagamento de dividendos nos próximos anos.
3. O mercado continuará a valorizar positivamente os ativos líquidos da

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=1 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O apresentador menciona ter vendido TSMC recentemente. |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\TSM.md` (cemetery archive)_

#### 🎯 Thesis: [[TSM]] — Taiwan Semiconductor (ADR)

> #1 foundry globally. 55%+ world foundry share. **3nm + 2nm monopoly** leading-edge. Beneficiário AI supercycle.

##### Intent
**Compounder** — growth primary. DY ~1.5% secundário.

##### Business snapshot

Pure-play foundry (fabrica para fabless clients):
- **Clients**: Apple (20%+), NVIDIA (15-20%), AMD, MediaTek, Qualcomm, Broadcom, Marvell, Sony.
- **Nodes**:
  - 3nm (N3) — current leading
  - 2nm (N2) — 2025 ramp
  - 1.4nm (A14) — 2027 roadmap
- **Global expansion**: Arizona, Japan (Kumamoto), Germany (Dresden) — but Taiwan remains core.

Revenue ~$70B+/y, growing 20%+/y in AI upcycle.

##### Por que detemos

1. **Foundry moat** — TSMC >55% share, 90%+ leading-edge.
2. **Capital intensity moat** — 3nm fab $20-30B, 2nm $30-40B. Only TSMC + Samsung + Intel can afford. TSMC execution class separates.
3. **AI demand explosion** — NVIDIA + Apple + AMD AI chips all on TSMC nodes.
4. **ROIC 25%+** consistently.
5. **Dividend growth** (modest but consistent).
6. **Morris Chang legacy** — now CEO C.C. Wei, disciplined.

##### Moat

- **Process technology** — years ahead of Samsung/Intel foundry.
- **Ecosystem** — EDA tools (Synopsys, Cadence) optimize FIRST for TSMC nodes.
- **Customer stickiness** — design for 3nm takes years, can't switch mid-cycle.
- **Scale** — $30B+ annual capex only sustainable at TSMC volume.
- **Weak moat**: **Taiwan geopolitical risk** — single-point of failure for global chip supply.

##### Current state (2026-04)

- N3 capacity fully booked through 2026, allocating customers.
- N2 2025 ramp on schedule.
- AZ fab first 4nm wafers 2025 (smaller scale vs Taiwan).
- Advanced packaging (CoWoS) a new bottleneck for NVIDIA datacenter GPUs.
- Customer concentration: Apple + NVIDIA ~40% revenue (AI concentration risk).

##### Taiwan geopolitical risk

**The single biggest hidden risk**:
- China-Taiwan tensions → could escalate (peaceful unification pressure → blockade → worst-case invasion).
- TSMC ~92% of world leading-edge logic. Disruption = global chip supply chain paralysis.
- US CHIPS Act ($52B) diversification helps multi-year but NOT quick fix.
- **Probability estimate**: low single-digit per year but consequences catastrophic.

**Portfolio implication**: TSM position sized SMALLER than equivalent-quality non-Taiwan name would be. Tax loss harvest if held long-term and thesis pivots.

##### Invalidation triggers

- [ ] **Taiwan crisis** (blockade, invasion, even elevated tension) — potential 50%+ drawdown
- [ ] Foundry technology leadership lost (Samsung 2nm catches up meaningfully)
- [ ] Major customer loss (Apple moves to own/different foundry — unlikely short-term)
- [ ] Capital intensity exceeds cash flow (capex > FCF sustained > 2y)
- [ ] ROIC < 15% structural
- [ ] Accounting/governance scandal

##### Sizing

- Posição actual: 5 shares
- Target 2-4% sleeve US (smaller than equivalent-quality non-Taiwan name)
- **Compounder** — hold, don't trim unless Taiwan risk materializes

##### Semi peer comparison (focus foundry + equipment)

| Ticker | Profile | Moat |
|---|---|---|
| **TSM** | Pure foundry #1 | Process tech + ecosystem + scale |
| Samsung Foundry | #2 foundry (closer) | Captive customers (Samsung) + memory cross |
| Intel Foundry (IFS) | Turnaround play | US gov support + domestic chip backup |
| GFS (GlobalFoundries) | Mature node specialist | Military/auto contracts |
| ASML | EUV lithography | Monopoly |
| AMAT, LRCX, KLA | Wafer fab equipment | High switching cost |


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -1.81%
- **Drawdown 5y**: -1.81%
- **YTD**: +19.12%
- **YoY (1y)**: +141.26%
- **CAGR 3y**: +65.07%  |  **5y**: +26.26%  |  **10y**: +31.30%
- **Vol annual**: +38.11%
- **Sharpe 3y** (rf=4%): +1.61

###### Dividendos
- **DY 5y avg**: +1.61%
- **Div CAGR 5y**: +13.33%
- **Frequency**: quarterly
- **Streak** (sem cortes): 6 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Semiconductors_cycle]] — sector deep-dive (stack + AI supercycle)
- [[Semi_cycle]] — cycle timing framework
- [[Moat_types]] — TSM é multi-moat (process + ecosystem + scale)
- [[ACN]] — tech sector peer with very different profile (services not silicon)

## ⚙️ Refresh commands

```bash
ii panorama TSM --write
ii deepdive TSM --save-obsidian
ii verdict TSM --narrate --write
ii fv TSM
python -m analytics.fair_value_forward --ticker TSM
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
