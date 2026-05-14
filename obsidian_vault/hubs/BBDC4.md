---
type: ticker_hub
ticker: BBDC4
market: br
sector: Banks
currency: BRL
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 19
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# BBDC4 — Bradesco PN

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Banks` · `market: BR` · `currency: BRL` · `bucket: holdings` · `19 sources merged`

## 🎯 Hoje

- **Posição**: 1837.0 @ entry 16.1
- **Verdict (DB)**: `WATCH` (score 6.58, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 8.40 · P/B 1.04 · DY 8.6% · ROE 13.4% · Dividend streak 19

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\BBDC4.md` (now in cemetery)_

#### BBDC4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (2):
  - https://www.bradescori.com.br/
  - https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fatos-relevantes/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=1837.0 · entry=16.1 · date=2026-05-07

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=18.09000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.13366 · DY=0.08428114909561732 · P/E=8.614286
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Fechamento da Consolidaçã |
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Publicação dos Relatórios |
| 2026-04-15 | comunicado | cvm | Esclarecimentos sobre questionamentos da CVM/B3 \| Notícia Divulgada na Mídia |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre a Reorg |
| 2026-03-25 | fato_relevante | cvm | Pagamento de Juros sobre o Capital Próprio Intermediários |

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
_source: `dossiers\BBDC4_FILING_2026-05-08.md` (now in cemetery)_

#### Filing dossier — [[BBDC4]] · 2026-05-08

**Trigger**: `manual` no dia `2026-05-08`

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 18.52

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `15.55` |
| HOLD entre | `15.55` — `21.30` (consensus) |
| TRIM entre | `21.30` — `24.50` |
| **SELL acima de** | `24.50` |

_Método: `br_bank_mult`. Consensus fair = R$21.30. Our fair (mais conservador) = R$15.55._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.13754` | `0.0516` | +62.5% |
| EPS | `2.13` | `4.0913` | +47.9% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 56.8B (+45.2% QoQ, +15.9% YoY)
- PDD -21.7B (-45.5% QoQ)
- Lucro líquido 17.4B (+47.1% QoQ, +30.4% YoY)
- Eficiência 37.1% (vs 35.7% prior)

**BS / risco**
- Carteira de crédito 747.8B (+2.3% QoQ)
- CET1 11.39% (vs 11.06% prior)
- Equity 176.1B (+0.9% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T13:34:56+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual:dossier` |
| 2026-05-08T13:34:47+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual:dossier` |
| 2026-05-08T13:34:26+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual` |
| 2026-05-08T13:21:27+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `smoke_v3_with_confidence` |
| 2026-05-08T13:16:03+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | single_source | `smoke_v2_run2` |
| 2026-05-08T13:15:45+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | single_source | `smoke_v2` |
| 2026-05-07 | `br_bank_mult` | 21.30 | — | 19.27 | — | — | `—` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-06 · Filing 2026-05-06
_source: `dossiers\BBDC4_FILING_2026-05-06.md` (now in cemetery)_

#### Filing dossier — [[BBDC4]] · 2026-05-06

**Trigger**: `cvm:comunicado` no dia `2026-05-06`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517345&numSequencia=1042051&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 18.21

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `14.72` |
| HOLD entre | `14.72` — `20.17` (consensus) |
| TRIM entre | `20.17` — `23.19` |
| **SELL acima de** | `23.19` |

_Método: `br_bank_mult`. Consensus fair = R$20.17. Our fair (mais conservador) = R$14.72._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.13366` | `0.1235` | +7.6% |
| EPS | `2.1` | `2.0167` | +4.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 56.8B (+45.2% QoQ, +15.9% YoY)
- PDD -21.7B (-45.5% QoQ)
- Lucro líquido 17.4B (+47.1% QoQ, +30.4% YoY)
- Eficiência 37.1% (vs 35.7% prior)

**BS / risco**
- Carteira de crédito 747.8B (+2.3% QoQ)
- Equity 176.1B (+0.9% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.21 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-06` |
| 2026-05-13T16:45:13+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.21 | HOLD | cross_validated | `manual` |
| 2026-05-11T20:40:44+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.09 | HOLD | cross_validated | `manual` |
| 2026-05-11T12:53:42+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:18+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `manual` |
| 2026-05-09T20:37:09+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `manual` |
| 2026-05-09T13:08:34+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:05+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Council review · Diego Bancário
_source: `agents\Diego Bancário\reviews\BBDC4_2026-04-30.md` (now in cemetery)_

#### Diego Bancário sobre [[BBDC4_STORY|BBDC4]]

**Função no debate**: Banks BR Specialist (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Bradesco mantém sólidos indicadores financeiros_

A Bradesco oferece P/E de 9.07 e P/B de 1.15, abaixo dos benchmarks do setor, com ROE de 13.8% acima da Selic-era.

**Métricas que invoquei**:
- P/E=9.07
- ROE=13.8%
- DivStreak=19

**Preocupações**:
- ambiente macroeconômico desafiador
- pressão sobre a qualidade dos ativos

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Bradesco opera com um P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor. — Mariana Macro

**Desafiei**:
- Ambiente macroeconômico desafiador | Pressão sobre a qualidade dos ativos — Valentina Prudente | A pressão macroeconômica é um risco, mas os resultados recentes mostram que o Bradesco tem se mantido resiliente em ciclos anteriores

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[BBDC4_STORY|📖 Storytelling completo (8 actos)]]
- [[BBDC4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Diego Bancário|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `agents\Mariana Macro\reviews\BBDC4_2026-04-30.md` (now in cemetery)_

#### Mariana Macro sobre [[BBDC4_STORY|BBDC4]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Bradesco oferece valor atraente com sólidos dividendos_

A Bradesco opera com um P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor.

**Métricas que invoquei**:
- P/E=9.07
- ROE=13.8%
- DY=7.54%

**Preocupações**:
- Ambiente macroeconômico desafiador
- Pressão sobre a qualidade dos ativos

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital. - Valentina Prudente

**Desafiei**:
- Margem EBIT baixa nos últimos trimestres | Possível pressão macroeconômica - Valentina Prudente | A margem EBIT tem oscilado, mas é importante notar que o Bradesco está diversificando seus negócios além do segmento bancário para mitigar riscos

**Evidência nova**: O ambiente regulatório favorável e a dinâmica do setor fintech no Brasil podem oferecer oportunidades de crescimento adicionais para o Bradesco.

##### Quem mais estava na sala

- [[Diego Bancário]] (Banks BR Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[BBDC4_STORY|📖 Storytelling completo (8 actos)]]
- [[BBDC4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `agents\Pedro Alocação\reviews\BBDC4_2026-04-30.md` (now in cemetery)_

#### Pedro Alocação sobre [[BBDC4_STORY|BBDC4]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Bradesco apresenta valorização atraente com sólidos dividendos_

A Bradesco oferece uma P/E de 9.07 e um DY de 7.8%, abaixo da média do setor, indicando potencial de valorização.

**Métricas que invoquei**:
- P/E=9.07
- DY=7.8%
- ROE=13.8%

**Preocupações**:
- peso atual na carteira (9.9%)
- ambiente macroeconômico desafiador

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor. - Mariana Macro

**Desafiei**:
- Ambiente macroeconômico desafiador | pressão sobre a qualidade dos ativos - Diego Bancário
- A preocupação com o ambiente macroeconômico e a qualidade dos ativos é válida, mas não deve ser um impedimento único para uma posição de compra considerando os indicadores financeiros sólidos da empresa.

##### Quem mais estava na sala

- [[Diego Bancário]] (Banks BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[BBDC4_STORY|📖 Storytelling completo (8 actos)]]
- [[BBDC4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `agents\Valentina Prudente\reviews\BBDC4_2026-04-30.md` (now in cemetery)_

#### Valentina Prudente sobre [[BBDC4_STORY|BBDC4]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Bradesco apresenta valorização atraente com sólidos dividendos_

A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital.

**Métricas que invoquei**:
- P/E=9.07
- ROE=13.8%
- DY=7.54%

**Preocupações**:
- Margem EBIT baixa nos últimos trimestres
- Possível pressão macroeconômica

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital.
- Mariana Macro

**Desafiei**:
- Ambiente macroeconômico desafiador | Pressão sobre a qualidade dos ativos
- Diego Bancário, Mariana Macro, Pedro Alocação — A pressão macroeconômica é um risco conhecido, mas não há evidências concretas de deterioração na qualidade dos ativos da Bradesco que justifiquem uma mudança na posição

##### Quem mais estava na sala

- [[Diego Bancário]] (Banks BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[BBDC4_STORY|📖 Storytelling completo (8 actos)]]
- [[BBDC4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Filing 2026-04-30
_source: `dossiers\BBDC4_FILING_2026-04-30.md` (now in cemetery)_

#### Filing dossier — [[BBDC4]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1514205&numSequencia=1038911&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 18.52

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `14.72` |
| HOLD entre | `14.72` — `20.17` (consensus) |
| TRIM entre | `20.17` — `23.19` |
| **SELL acima de** | `23.19` |

_Método: `br_bank_mult`. Consensus fair = R$20.17. Our fair (mais conservador) = R$14.72._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.13754` | `0.1235` | +10.2% |
| EPS | `2.13` | `2.0167` | +5.3% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 56.8B (+45.2% QoQ, +15.9% YoY)
- PDD -21.7B (-45.5% QoQ)
- Lucro líquido 17.4B (+47.1% QoQ, +30.4% YoY)
- Eficiência 37.1% (vs 35.7% prior)

**BS / risco**
- Carteira de crédito 747.8B (+2.3% QoQ)
- Equity 176.1B (+0.9% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `filing:cvm:comunicado:2026-04-30` |
| 2026-05-08T17:48:11+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `br_bank_mult` | 40.91 | 29.87 | 18.52 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-16 · Other
_source: `videos\2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al.md` (now in cemetery)_

#### 🎬 BBDC3 OU BBDC4? O BANCO MAIS BARATO COM 14,5 BI DE DIVIDENDOS E +70% DE ALTA? +PREÇO TETO

**Canal**: Virtual Asset | **Publicado**: 2026-04-16 | **Duração**: 20min

**URL**: [https://www.youtube.com/watch?v=yS2rb3Ksu18](https://www.youtube.com/watch?v=yS2rb3Ksu18)

##### Tickers mencionados

[[BBAS3]] · [[BBDC4]] · [[SUZB3]]

##### Insights extraídos

###### [[BBDC4]]
- [0.90 guidance] O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026.
- [0.80 thesis_bull] O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotação atual.
- [0.80 valuation] O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado.
- [0.70 dividend] O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025.
- [0.70 thesis_bull] O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro.

###### [[BBAS3]]
- [0.70 operational] O BBAS3 participou de uma estratégia de dividendo sintético com o BBDC4, gerando receitas adicionais para os investidores.

###### [[SUZB3]]
- [0.70 operational] É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$1,18 por ação.
- [0.70 valuation] É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$1,18 por ação.

##### Temas macro

- **banking_br** bullish _(conf 0.90)_ — O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026.
- **banking_br** bullish _(conf 0.80)_ — O Bradesco apresenta resultados positivos, com crescimento na carteira de crédito e margem financeira líquida, além de aumento nos dividendos pagos aos acionistas.
- **banking_br** bullish _(conf 0.80)_ — O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026, indicando otimismo para o futuro.
- **banking_br** neutral _(conf 0.70)_ — A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as despesas com PDDs aumentaram.
- **banking_br** neutral _(conf 0.70)_ — A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado.


### (undated)

#### — · DRIP scenarios
_source: `briefings\drip_scenarios\BBDC4_drip.md` (now in cemetery)_

/============================================================================\
|   DRIP SCENARIO — BBDC4           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:          1.828
  Entry price.........: R$       16.08
  Cost basis..........: R$   29,394.24
  Price now...........: R$       19.92
  Market value now....: R$   36,413.76  [+23.9% nao-realizado]
  DY t12m.............: 7.56%  (R$/US$ 1.5057/share)
  DY vs own 10y.......: P76 [CHEAP]  (actual 7.56% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=19  hist_g_5y=0.120  hist_g_raw=0.169  gordon_g=0.040  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +4.81%  |   -1.00% |  +11.37%       |
  | base         |   +8.02%  |   +0.00% |  +15.57%       |
  | optimista    |  +10.82%  |   +1.00% |  +19.38%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      9       |       10       |        5       |
  | base         |      8       |       10       |        4       |
  | optimista    |      7       |       10       |        3       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     63,846 | R$     77,077 | R$     90,795 |
  |  10y  | R$    113,944 | R$    163,150 | R$    223,004 |
  |  15y  | R$    207,145 | R$    345,340 | R$    539,865 |
  --------------------------------------------------------------------------

#### — · Council aggregate
_source: `dossiers\BBDC4_COUNCIL.md` (now in cemetery)_

#### Council Debate — [[BBDC4_STORY|BBDC4]] (Bradesco)

**Final stance**: 🟢 **BUY**  
**Confidence**: `high`  
**Modo (auto)**: B (BR)  |  **Sector**: Banks  |  **Held**: sim  
**Elapsed**: 65.1s  |  **Failures**: 0

##### Quem esteve na sala

- [[Diego Bancário]] — _Banks BR Specialist_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor.
- O histórico de dividendos da Bradesco é sólido, com um DY de 7.54% mantido por 19 anos consecutivos.

**Dissenso (preservado)**:
- Valentina Prudente disse que a margem EBIT tem sido baixa nos últimos trimestres e há pressão macroeconômica.
- Diego Bancário, Mariana Macro e Pedro Alocação mencionaram preocupações com o ambiente macroeconômico desafiador e a qualidade dos ativos.

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ Ambiente regulatório favorável e dinâmica do setor fintech no Brasil podem oferecer oportunidades de crescimento adicionais para o Bradesco - Mariana Macro
- ⚠️ A pressão macroeconômica é um risco conhecido, mas não há evidências concretas de deterioração na qualidade dos ativos da Bradesco que justifiquem uma mudança na posição - Valentina Prudente

**Sizing**: Considerar a redução do peso atual na carteira (9.9%) em função das preocupações com o ambiente macroeconômico e a qualidade dos ativos.

##### Round 1 — Opening Statements (blind)

###### [[Diego Bancário]] — 🟢 **BUY**
_Banks BR Specialist_

**Headline**: _Bradesco mantém sólidos indicadores financeiros_

A Bradesco oferece P/E de 9.07 e P/B de 1.15, abaixo dos benchmarks do setor, com ROE de 13.8% acima da Selic-era.

**Métricas**:
- P/E=9.07
- ROE=13.8%
- DivStreak=19

**Preocupações**:
- ambiente macroeconômico desafiador
- pressão sobre a qualidade dos ativos

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _Bradesco oferece valor atraente com sólidos dividendos_

A Bradesco opera com um P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor.

**Métricas**:
- P/E=9.07
- ROE=13.8%
- DY=7.54%

**Preocupações**:
- Ambiente macroeconômico desafiador
- Pressão sobre a qualidade dos ativos

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Bradesco apresenta valorização atraente com sólidos dividendos_

A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital.

**Métricas**:
- P/E=9.07
- ROE=13.8%
- DY=7.54%

**Preocupações**:
- Margem EBIT baixa nos últimos trimestres
- Possível pressão macroeconômica

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Bradesco apresenta valorização atraente com sólidos dividendos_

A Bradesco oferece uma P/E de 9.07 e um DY de 7.8%, abaixo da média do setor, indicando potencial de valorização.

**Métricas**:
- P/E=9.07
- DY=7.8%
- ROE=13.8%

**Preocupações**:
- peso atual na carteira (9.9%)
- ambiente macroeconômico desafiador

##### Round 2 — Respostas (peers visíveis)

###### [[Diego Bancário]] — 🟢 **BUY**
_Banks BR Specialist_

**Concordou com**:
- A Bradesco opera com um P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor. — Mariana Macro

**Desafiou**:
- Ambiente macroeconômico desafiador | Pressão sobre a qualidade dos ativos — Valentina Prudente | A pressão macroeconômica é um risco, mas os resultados recentes mostram que o Bradesco tem se mantido resiliente em ciclos anteriores

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital. - Valentina Prudente

**Desafiou**:
- Margem EBIT baixa nos últimos trimestres | Possível pressão macroeconômica - Valentina Prudente | A margem EBIT tem oscilado, mas é importante notar que o Bradesco está diversificando seus negócios além do segmento bancário para mitigar riscos

**Evidência nova**: O ambiente regulatório favorável e a dinâmica do setor fintech no Brasil podem oferecer oportunidades de crescimento adicionais para o Bradesco.

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando avaliação atrativa e gestão eficiente do capital.
- Mariana Macro

**Desafiou**:
- Ambiente macroeconômico desafiador | Pressão sobre a qualidade dos ativos
- Diego Bancário, Mariana Macro, Pedro Alocação — A pressão macroeconômica é um risco conhecido, mas não há evidências concretas de deterioração na qualidade dos ativos da Bradesco que justifiquem uma mudança na posição

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- A Bradesco oferece P/E de 9.07 e ROE de 13.8%, indicando uma avaliação atrativa em comparação à média do setor. - Mariana Macro

**Desafiou**:
- Ambiente macroeconômico desafiador | pressão sobre a qualidade dos ativos - Diego Bancário
- A preocupação com o ambiente macroeconômico e a qualidade dos ativos é válida, mas não deve ser um impedimento único para uma posição de compra considerando os indicadores financeiros sólidos da empresa.

##### Documentos relacionados

- [[BBDC4_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[BBDC4_2026-04-30|Diego Bancário]] em [[Diego Bancário]]/reviews/
  - [[BBDC4_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[BBDC4_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[BBDC4_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: BR:BBDC4 — Bradesco ===
Sector: Banks  |  Modo (auto): B  |  Held: True
Last price: 19.31999969482422 (2026-04-30)
Position: 1828 shares @ entry 16.08
Fundamentals: P/E=9.07 | P/B=1.15 | DY=7.8% | ROE=13.8% | DivStreak=19.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=   70.4  ebit=   4.9  ni=   5.6  ebit_margin=  6.9%
  2025-06-30: rev=   65.3  ebit=   4.3  ni=   6.1  ebit_margin=  6.6%
  2025-03-31: rev=   60.1  ebit=   6.1  ni=   5.7  ebit_margin= 10.1%
  2024-12-31: rev=   56.5  ebit=   3.3  ni=   4.2  ebit_margin=  5.8%
  2024-09-30: rev=   52.5  ebit=   5.6  ni=   4.9  ebit_margin= 10.6%
  2024-06-30: rev=   51.5  ebit=   3.7  ni=   4.2  ebit_margin=  7.2%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: A Bradesco, com seu preço atual de R$19.96 e um P/E de 9.38, oferece uma oportunidade única para investidores Buffett/Graham em busca de valor a longo prazo. A empresa possui um sólido histórico de dividendos, mantendo-o por 19 anos consecutivos, com um rendimento atual de 7.54%. Além disso, o ROE de 13.75% e a relação Patrimônio Líquido/Patrimônio (PB) de 1.18 indicam uma gestão eficiente e sustentável do capital.

**Key assumptions**:
1. A Bradesco continuará a manter seu histórico de dividendos por mais pelo menos os próximos cinco anos.
2. O P/E da empresa permanecerá abaixo de 10 nos próximos três anos, refletindo uma avaliação justa ou subavaliada em relação ao mercado.
3. A taxa ROE se mantém acima de 12% durante o mesmo período, indicando eficiência op

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  This position weight: 9.9%
  Sector weight: 9.9%

WEB CONTEXT (qualitative research, last 30-90d):
  - The Fintech Ecosystem of Brazil in 2026 - The Fintech Times [Mon, 13 Ap]
    #### *Public infrastructure, regulatory foresight and private-sector dynamism have converged to create one of the most sophisticated and inclusive financial ecosystems in the emerging world. Speaking of financial services, the financial gra
  - Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest - World Oil [Thu, 23 Ap]
    # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetrol** has agreed to acquire an initial equity stake in **Brava Energia** as part of a broader plan to secure a controlling interest and exp
  - Petrobras board vote comes amid oil price surge, fuel policy pressure in Brazil - World Oil [Thu, 16 Ap]
    World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petrobras board vote comes amid oil price surge, fuel policy pressure i
  - Brazil finance minister readies run for Sao Paulo governor - TradingView [Thu, 19 Ma]
    * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 gr
  - Top 6 Defence Stocks with Strong Growth Guidance for FY26 to Keep an Eye On - Trade Brains [Sat, 14 Ma]
    > ***Synopsis: Several defence stocks are in focus for FY26, backed by strong order books, robust revenue growth guidance, and strategic expansion in domestic defence production, modernisation initiatives, and high-value aerospace and elect
  - Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround - InternetRetailing [Tue, 31 Ma]
    You are in: Home » Marketplaces » **Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround**. # Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround. The Group’s trading statement for 

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### ANALYST INSIGHTS (subscriptions BTG/XP/Suno) (8 hits)
[1] xp [2026-04-24] (bull): [BTG Equity Brazil] BBDC4 — peso 3.1%
[2] xp [2026-04-24] (neutral): O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores.
     URL: https://conteudos.xpi.com.br/acoes/relatorios/bradesco-bbdc4-recuperacao-gradual-upside-limitado/
[3] xp [2026-04-24] (neutral): O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios.
     URL: https://conteudos.xpi.com.br/acoes/relatorios/bradesco-bbdc4-recuperacao-gradual-upside-limitado/
[4] xp [2026-04-24] (bear): Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco.
     URL: https://conteudos.xpi.com.br/acoes/relatorios/bradesco-bbdc4-recuperacao-gradual-upside-limitado/
[5] xp [2026-04-24] (neutral): As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E.
     URL: https://conteudos.xpi.com.br/acoes/relatorios/bradesco-bbdc4-recuperacao-gradual-upside-limitado/
[6] xp [2026-04-24] (neutral): A recomendação para o Bradesco é Neutra.
     URL: https://conteudos.xpi.com.br/acoes/relatorios/bradesco-bbdc4-recuperacao-gradual-upside-limitado/

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[7] cvm (comunicado) [2026-04-15]: Esclarecimentos sobre questionamentos da CVM/B3 | Notícia Divulgada na Mídia
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505365&numSequencia=1030071&numVersao=1
[8] cvm (comunicado) [2026-04-06]: Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre a Reorganização Societária para Consolidar os Negócios de Saúde da Organização Bradesco na Odontoprev
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1501628&numSequencia=1026334&numVersao=1
[9] cvm (fato_relevante) [2026-03-25]: Pagamento de Juros sobre o Capital Próprio Intermediários
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1495078&numSequencia=1019784&numVersao=1
[10] cvm (comunicado) [2026-03-25]: Outros Comunicados Não Considerados Fatos Relevantes
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1495256&numSequencia=1019962&numVersao=2
[11] cvm (comunicado) [2026-03-06]: Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre a Reorganização Societária para Consolidar os Negócios de Saúde da Organização Bradesco na Odontoprev
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1487022&numSequencia=1011728&numVersao=1
[12] cvm (comunicado) [2026-03-01]: Apresentações a analistas/agentes do mercado | Apresentação ROADSHOW Bradsaúde
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1483661&numSequencia=1008367&numVersao=1

##### YOUTUBE INSIGHTS (transcripts ingeridos) (10 hits)
[13] YouTube Virtual Asset [2026-04-16] (guidance): O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18
[14] YouTube Virtual Asset [2026-04-16] (thesis_bull): O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotação atual.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18
[15] YouTube Virtual Asset [2026-04-16] (valuation): O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18
[16] YouTube Virtual Asset [2026-04-16] (dividend): O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18
[17] YouTube Virtual Asset [2026-04-16] (thesis_bull): O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18
[18] YouTube Virtual Asset [2026-04-16] (guidance): O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026.
     URL: https://www.youtube.com/watch?v=yS2rb3Ksu18

##### TAVILY NEWS (≤30d) (5 hits)
[19] Tavily [Mon, 13 Ap]: #### *Public infrastructure, regulatory foresight and private-sector dynamism have converged to create one of the most sophisticated and inclusive financial ecosystems in the emerging world. Speaking of financial services, the financial gravity is centred in São Paulo, Brazil’s largest city by popul
     URL: https://thefintechtimes.com/the-fintech-landscape-of-brazil-in-2026/
[20] Tavily [Thu, 23 Ap]: # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetrol** has agreed to acquire an initial equity stake in **Brava Energia** as part of a broader plan to secure a controlling interest and expand i

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\BBDC4_COUNCIL.md`)_

#### — · Story
_source: `dossiers\BBDC4_STORY.md` (now in cemetery)_

#### Bradesco — BBDC4

##### Análise de Investimento · Modo FULL · Jurisdição BR

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo B-BR sob a Jurisdição BR.**

---

##### Quem analisou este ticker

- [[Diego Bancário]] — _Banks BR Specialist_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/BBDC4_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 117.8 bi · FCF R$ -74.16 bi · ROE 14% · DGR 29.9% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** |  |
| **5 — Classification** | Modo B-BR · Dividend/DRIP (5/12) |
| **5.5 — Council Debate** | BUY (high) · 2 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo B-BR sob a Jurisdição BR. O Bradesco, representado pelo ticker BBDC4 na bolsa brasileira, é uma das principais instituições financeiras do país, com presença significativa em diversos setores além de sua atividade bancária tradicional. A empresa oferece um leque abrangente de serviços que incluem seguros e consórcios, estratégias que lhe conferem opcionalidades importantes no mercado.

O Bradesco tem se destacado por executar melhor do que inicialmente esperava em ciclos anteriores, segundo análise neutral da XP. Essa resiliência é um ponto-chave para investidores ao avaliarem o potencial de retorno e riscos associados à ação BBDC4. No entanto, uma armadilha comum é confundir a marca Bradesco como sinônimo do seu diferencial competitivo, que vai além da mera reputação estabelecida no mercado financeiro brasileiro.

O posicionamento competitivo do Bradesco é robusto, refletindo sua capacidade de adaptar-se e expandir seus negócios não core. No entanto, o ambiente macroeconômico desafiador e a pressão sobre a qualidade dos ativos podem impactar negativamente os resultados da empresa, conforme alerta um relatório bear do XP.

##### Ato 2 — O Contexto

O cenário econômico atual é marcado por uma taxa Selic de 13.75% em abril de 2026, com o Banco Central do Brasil (BCB) sinalizando um início gradual de afrouxamento monetário no segundo semestre do mesmo ano, dependendo da evolução do IPCA e das contas públicas. O câmbio BRL/USD oscila na faixa dos R$ 5,80 a R$ 6,00, enquanto o custo de capital próprio (Ke) é estimado em cerca de 18%, considerando um prêmio adicional de 4,5% sobre a taxa Selic.

Neste contexto macroeconômico, os bancos enfrentam desafios significativos relacionados à liquidez e ao crédito. A pressão sobre as taxas de juros e o câmbio pode afetar diretamente o custo do capital para instituições financeiras como o Bradesco, impactando sua rentabilidade e capacidade de expansão. Além disso, a incerteza regulatória continua sendo um fator relevante, com possíveis mudanças nas políticas governamentais que podem afetar diretamente os negócios do setor bancário.

Para o Bradesco, essas condições exigem uma estratégia flexível e adaptativa. A empresa deve continuar a buscar oportunidades de crescimento em seus negócios não core, como seguros e consórcios, para diversificar suas receitas e mitigar os riscos associados às flutuações do mercado bancário tradicional.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa e desafiadora. As cifras apresentadas na tabela abaixo ilustram tanto períodos de crescimento como momentos de declínio, retratando a dinâmica do mercado em que a companhia opera.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 108.85B | — | — | — | R$ 21.22B | 19.5% | R$ 40.36B |
| 2023 | R$ 98.33B | — | — | — | R$ 14.25B | 14.5% | R$ -9.32B |
| 2024 | R$ 105.33B | — | — | — | R$ 17.25B | 16.4% | R$ 42.18B |
| 2025 | R$ 117.81B | — | — | — | R$ 23.67B | 20.1% | R$ -74.16B |

A receita da empresa apresentou um crescimento anual composto (CAGR) de aproximadamente 5,9%, passando de R$ 108,85 bilhões em 2022 para R$ 117,81 bilhões em 2025. No entanto, este aumento não foi acompanhado por uma expansão consistente das margens EBITDA e lucro líquido, o que sugere desafios operacionais e potenciais pressões de custos.

O fluxo de caixa livre (FCF) da empresa exibe um comportamento volátil. Após atingir R$ 40,36 bilhões em 2022, houve uma queda significativa para R$ -9,32 bilhões no ano seguinte e um retorno a números positivos em 2024 com R$ 42,18 bilhões. No entanto, o último exercício registrou novamente um fluxo de caixa negativo de R$ 74,16 bilhões, indicando potenciais desafios na gestão de capital e investimentos.

A distribuição de dividendos também apresenta uma variação notável ao longo do período. A tabela abaixo detalha os valores pagos anualmente:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 0.469 |
| 2021 | 0.925 |
| 2022 | 0.417 |
| 2023 | 1.697 |
| 2024 | 0.820 |
| 2025 | 1.730 |
| 2026 | 0.373 |

O Dividend Growth Rate (DGR) calculado, sem considerar dividendos extraordinários, é de 29,9% ao ano. Este crescimento sustentado sugere uma política de distribuição de lucros consistente e um potencial atrativo para investidores interessados em renda através da estratégia DRIP (Dividend Reinvestment Plan).

É importante notar que o DY total reportado pode não refletir completamente a estrutura de dividendos, especialmente se houver pagamentos extraordinários. No entanto, a consistência e o crescimento dos dividendos ao longo do tempo indicam uma política sólida e confiável.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A volatilidade do fluxo de caixa livre destaca as dificuldades da empresa em gerir seus investimentos e despesas operacionais de forma consistente.

##### Ato 4 — O Balanço

O balanço financeiro da empresa no exercício mais recente (2025) revela uma estrutura de capital que, embora apresentar alguns pontos fortes, também traz preocupações significativas. Com um preço-earnings (P/E) de 9,07 e um price-to-book (P/B) de 1,15, a empresa parece estar avaliada em níveis moderados comparativamente ao seu potencial de lucro e ativos.

O dividend yield (DY) da companhia é de 7,79%, o que representa uma atratividade considerável para investidores interessados em renda. O retorno sobre o patrimônio líquido (ROE) está em 13,75%, superando a taxa de custo do capital próprio (Ke) estimada no Brasil de aproximadamente 18,25%. Este resultado positivo indica que a empresa cria valor para seus acionistas.

A dívida líquida (Net Debt), calculada com base na proporção de dívida total e caixa disponível, é estimada em R$ 224,34 bilhões. A relação Net Debt/EBITDA, considerando o EBITDA mais recente da tabela anual, resulta em aproximadamente 10,7 vezes, sugerindo um nível de alavancagem significativo.

O Current Ratio, que mede a capacidade da empresa de cobrir suas dívidas curtas com ativos líquidos imediatamente disponíveis, não está especificado nos dados fornecidos. No entanto, considerando o elevado nível de dívida e os fluxos de caixa livres recentemente negativos, é possível que a empresa esteja enfrentando desafios na gestão de sua liquidez.

A política de dividendos consistente, com 19 anos sem interrupções (Dividend Streak), continua sendo um ponto forte da empresa. No entanto, o fluxo de caixa livre negativo no último exercício e a alavancagem crescente são sinais preocupantes que podem indicar desafios futuros na sustentabilidade dos dividendos e na gestão do endividamento.

Em resumo, enquanto a empresa apresenta um balanço financeiro com pontos positivos como o ROE acima da taxa de custo do capital próprio e uma política de dividendos sólida, os riscos associados à alavancagem elevada e ao fluxo de caixa negativo devem ser monitorados cuidadosamente.

---

##### Ato 5 — Os Múltiplos

No panorama financeiro atual, a análise dos múltiplos é crucial para entender o valor intrínseco e a posição relativa de uma empresa no mercado. O Banco do Brasil S.A. (BBDC4) oferece um caso interessante ao exibir múltiplos que refletem tanto oportunidades como desafios.

###### Valoração Relativa

A tabela abaixo apresenta os principais múltiplos financeiros da BBDC4, comparados com a média setorial e o índice de referência (Ibov/S&P):

| Múltiplo | BBDC4 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 9.07x | 10.77x | 9.00x |
| P/B | 1.15x | 0.90x | 1.60x |
| DY | 7.8% | 7.9% | 6.0% |
| FCF Yield | -35.1% | 5.7% | 5.0% |
| ROE | 13.8% | 15.5% | 13.0% |

O múltiplo P/E de 9.07x para BBDC4 é ligeiramente inferior à média setorial (10.77x) e ao índice (9.00x), sugerindo que o mercado pode estar avaliando a empresa com um desconto em relação aos seus pares e ao índice geral. Este múltiplo reflete uma expectativa de crescimento mais baixa ou maior incerteza sobre as perspectivas futuras da companhia.

O P/B (Preço/Patrimônio) de 1.15x é ligeiramente superior à média setorial (0.90x), mas inferior ao índice (1.60x). Este indicador sugere que o mercado está atribuindo um valor mais baixo aos ativos tangíveis da BBDC4 em comparação com seus pares, embora ainda seja considerado razoável quando comparado ao índice.

A taxa de dividendos (DY) de 7.8% é ligeiramente inferior à médiana setorial (7.9%) e significativamente superior ao índice (6.0%). Este DY elevado pode ser atraente para investidores em busca de renda, mas deve ser analisado com cautela, pois pode incluir dividendos extraordinários.

O FCF Yield negativo (-35.1%) é um indicador preocupante e está significativamente abaixo da média setorial (5.7%) e do índice (5.0%). Este resultado reflete a dificuldade atual da empresa em gerar fluxo de caixa livre positivo, o que pode ser atribuído à sua recente expansão ou investimentos pesados.

O retorno sobre o equity (ROE) de 13.8% está ligeiramente abaixo do setor (15.5%) e um pouco acima do índice (13.0%). Este indicador sugere que a empresa está gerando retornos adequados em relação ao capital investido, mas pode haver espaço para melhorias.

###### Análise de Recomendações

As recomendações do sell-side variam amplamente, com alguns analistas destacando o potencial de crescimento e outros alertando sobre os riscos associados à geração de fluxo de caixa negativo. A análise dos múltiplos oferece uma base sólida para entender as perspectivas divergentes do mercado.

##### Ato 6 — Os Quality Scores

A avaliação da qualidade financeira é crucial para identificar empresas com solidez e potencial de crescimento sustentável. No caso da BBDC4, a análise dos scores de qualidade revela tanto pontos fortes quanto áreas que requerem atenção.

###### Piotroski F-Score

O F-Score do Piotrosoki não foi computado para esta empresa, o que implica uma falta de dados suficientes ou relevância limitada para este modelo específico. Este score é baseado em nove critérios financeiros e serve como um indicador da solidez operacional e financeira.

###### Altman Z-Score

O Z-Score conservador (Z) e o Z-Score ajustado não foram calculados para a BBDC4, o que pode ser atribuído à natureza específica do modelo de classificação ou à falta de dados necessários. O Z-Score é um indicador robusto da solidez financeira e da probabilidade de insolvência.

###### Beneish M-Score

O M-Score da Beneish também não foi calculado para a BBDC4, o que sugere uma ausência de dados ou relevância limitada. Este score é projetado para identificar empresas com potencial de manipulação financeira e serve como um indicador adicional da integridade das finanças.

###### Conclusão

A falta de scores específicos indica a necessidade de uma análise mais detalhada dos fundamentos financeiros da BBDC4. A avaliação dos múltiplos oferece insights valiosos sobre o valor relativo e as perspectivas do mercado, mas a ausência de indicadores de qualidade financeira sugere que um estudo mais profundo é necessário para uma compreensão completa da saúde financeira da empresa.

---

##### Ato 7 — O Moat e a Gestão

A Bradesco, uma das maiores instituições financeiras do Brasil, possui um moat significativo que lhe confere vantagens competitivas sustentáveis no mercado. Este moat é classificado como "Wide", devido à combinação de fatores que incluem escala e eficiência operacional, custos reduzidos para clientes e investidores, e uma sólida presença regulatória.

###### Escala e Eficiência Operacional

A Bradesco beneficia-se da economia de escala derivada do seu tamanho e diversificação geográfica. A instituição opera em todo o território brasileiro, com uma rede extensa de agências físicas e plataformas digitais que permitem atender a um vasto espectro de clientes, desde pequenas empresas até grandes corporações. Esta presença abrangente não apenas aumenta a visibilidade da marca, mas também reduz os custos operacionais por cliente, tornando-a mais competitiva em comparação com seus concorrentes menores.

###### Custos Reduzidos para Clientes e Investidores

A Bradesco mantém uma relação sólida com seus clientes através de um portfólio diversificado de produtos financeiros que incluem seguros, serviços bancários e investimentos. A instituição oferece soluções personalizadas e competitivas em termos de taxas e tarifas, o que contribui para a fidelização dos clientes e aumenta sua participação no mercado.

###### Presença Regulatória

A Bradesco tem uma forte presença regulatória no Brasil, refletida na sua capacidade de navegar com eficácia através do complexo cenário legal e normativo da indústria financeira. A instituição mantém um diálogo constante com os órgãos reguladores para garantir que suas práticas comerciais estejam em conformidade com as leis e regulamentos vigentes, o que lhe confere uma vantagem competitiva.

###### Dados Internos

Infelizmente, não foram fornecidos dados específicos sobre a propriedade interna ou negócios recentes de insiders na Bradesco. Portanto, declaro "dado não disponível" para essas informações.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico da Bradesco é predominantemente orientado para dividendos e distribuição de rendimentos recorrentes (DRIP). As pontuações indicam um forte compromisso com o pagamento de dividendos, refletido em um DY de 7.8% mantido por 19 anos consecutivos. O valor e crescimento são moderados, mas a consistência do histórico de dividendos é notável.

###### O que o preço desconta
O atual preço da Bradesco já incorpora uma avaliação atrativa em relação à média do setor financeiro brasileiro, refletida no P/E de 9.07 e ROE de 13.8%. Além disso, a pressão macroeconômica é um fator conhecido que o mercado já considera na precifica

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\BBDC4_STORY.md`)_

#### — · Other
_source: `hubs\BBDC4.md` (now in cemetery)_

#### BBDC4 — Bradesco

> **Hub consolidado**. Tudo o que existe no vault sobre BBDC4, em ordem cronológica. Cada link aponta para o ficheiro original que ficou na sua pasta — esta é a porta de entrada matinal.

`sector: Banks` · `market: BR` · `currency: BRL`

##### 🎯 Hoje

- **Posição**: 1837.0 @ entry 16.1
- **Verdict (DB)**: `WATCH` (score 6.58, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 8.40 · P/B 1.04 · DY 8.6% · ROE 13.4% · Dividend streak 19

##### 📜 Histórico (chronological journal)

> Como a vista sobre este nome evoluiu — do primeiro screen ao deepdive mais recente. Útil para perceber **o que sabíamos antes vs o que sabemos agora**.


###### 2026

- **2026-05-13** · Overnight → [[BBDC4]] _(`Overnight_2026-05-13/BBDC4.md`)_
- **2026-05-11** · Overnight → [[BBDC4]] _(`Overnight_2026-05-11/BBDC4.md`)_
- **2026-05-10** · Pilot → [[BBDC4]] _(`Pilot_Deep_Dive_2026-05-10/BBDC4.md`)_
- **2026-05-08** · Filing → [[BBDC4_FILING_2026-05-08]] _(`dossiers/BBDC4_FILING_2026-05-08.md`)_
- **2026-05-06** · Filing → [[BBDC4_FILING_2026-05-06]] _(`dossiers/BBDC4_FILING_2026-05-06.md`)_
- **2026-04-30** · Filing → [[BBDC4_FILING_2026-04-30]] _(`dossiers/BBDC4_FILING_2026-04-30.md`)_
- **2026-04-30** · Dossier Archive → [[BBDC4_STORY_2026-04-30]] _(`dossiers/archive/BBDC4_STORY_2026-04-30.md`)_
- **2026-04-30** · Review · Valentina Prudente → [[BBDC4_2026-04-30]] _(`agents/Valentina Prudente/reviews/BBDC4_2026-04-30.md`)_
- **2026-04-30** · Review · Pedro Alocação → [[BBDC4_2026-04-30]] _(`agents/Pedro Alocação/reviews/BBDC4_2026-04-30.md`)_
- **2026-04-30** · Review · Mariana Macro → [[BBDC4_2026-04-30]] _(`agents/Mariana Macro/reviews/BBDC4_2026-04-30.md`)_
- **2026-04-30** · Review · Diego Bancário → [[BBDC4_2026-04-30]] _(`agents/Diego Bancário/reviews/BBDC4_2026-04-30.md`)_
- **2026-04-16** · Video → [[2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al]] _(`videos/2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al.md`)_

###### (undated)

- **—** · Wiki → [[BBDC4]] _(`wiki/holdings/BBDC4.md`)_
- **—** · Variant → [[BBDC4_VARIANT]] _(`tickers/BBDC4_VARIANT.md`)_
- **—** · Story → [[BBDC4_STORY]] _(`dossiers/BBDC4_STORY.md`)_
- **—** · Ri → [[BBDC4_RI]] _(`tickers/BBDC4_RI.md`)_
- **—** · Panorama → [[BBDC4]] _(`tickers/BBDC4.md`)_
- **—** · Other → [[BBDC4]] _(`hubs/BBDC4.md`)_
- **—** · Ic Debate → [[BBDC4_IC_DEBATE]] _(`tickers/BBDC4_IC_DEBATE.md`)_
- **—** · Drip → [[BBDC4_drip]] _(`briefings/drip_scenarios/BBDC4_drip.md`)_
- **—** · Deepdive → [[BBDC4_DOSSIE]] _(`tickers/BBDC4_DOSSIE.md`)_
- **—** · Council → [[BBDC4_COUNCIL]] _(`dossiers/BBDC4_COUNCIL.md`)_

##### 🗂️ Artefactos por categoria

###### Panorama
- [[BBDC4]] _(`tickers/BBDC4.md`)_

###### Deepdive (DOSSIE)
- [[BBDC4_DOSSIE]] _(`tickers/BBDC4_DOSSIE.md`)_

###### Story
- [[BBDC4_STORY]] _(`dossiers/BBDC4_STORY.md`)_

###### Council aggregate
- [[BBDC4_COUNCIL]] _(`dossiers/BBDC4_COUNCIL.md`)_

###### Council reviews por persona

_Diego Bancário_:
- [[BBDC4_2026-04-30]] _(`agents/Diego Bancário/reviews/BBDC4_2026-04-30.md`)_

_Mariana Macro_:
- [[BBDC4_2026-04-30]] _(`agents/Mariana Macro/reviews/BBDC4_2026-04-30.md`)_

_Pedro Alocação_:
- [[BBDC4_2026-04-30]] _(`agents/Pedro Alocação/reviews/BBDC4_2026-04-30.md`)_

_Valentina Prudente_:
- [[BBDC4_2026-04-30]] _(`agents/Valentina Prudente/reviews/BBDC4_2026-04-30.md`)_

###### IC Debate (synthetic)
- [[BBDC4_IC_DEBATE]] _(`tickers/BBDC4_IC_DEBATE.md`)_

###### Variant perception
- [[BBDC4_VARIANT]] _(`tickers/BBDC4_VARIANT.md`)_

###### RI / official disclosures
- [[BBDC4_RI]] _(`tickers/BBDC4_RI.md`)_

###### Filings individuais
- [[BBDC4_FILING_2026-05-08]] _(`dossiers/BBDC4_FILING_2026-05-08.md`)_
- [[BBDC4_FILING_2026-05-06]] _(`dossiers/BBDC4_FILING_2026-05-06.md`)_
- [[BBDC4_FILING_2026-04-30]] _(`dossiers/BBDC4_FILING_2026-04-30.md`)_

###### Overnight scrapes
- [[BBDC4]] _(`Overnight_2026-05-13/BBDC4.md`)_
- [[BBDC4]] _(`Overnight_2026-05-11/BBDC4.md`)_

###### Pilot deep dives
- [[BBDC4]] _(`Pilot_Deep_Dive_2026-05-10/BBDC4.md`)_

###### DRIP scenarios
- [[BBDC4_drip]] _(`briefings/drip_scenarios/BBDC4_drip.md`)_

###### Wiki / playbooks
- [[BBDC4]] _(`wiki/holdings/BBDC4.md`)_

###### Video transcripts
- [[2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al]] _(`videos/2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al.md`)_

###### Archived stories
- [[BBDC4_STORY_2026-04-30]] _(`dossiers/archive/BBDC4_STORY_2026-04-30.md`)_

###### Other
- [[BBDC4]] _(`hubs/BBDC4.md`)_

##### ⚙️ Refresh commands

```bash
ii panorama BBDC4 --write       # aggregator (verdict+peers+notes+videos)
ii deepdive BBDC4 --save-obsidian # V10 4-layer pipeline
ii verdict BBDC4 --narrate --write
ii fv BBDC4                      # fair value (Buffett-Graham conservative)
python -m analytics.fair_value_forward --ticker BBDC4 # quality-aware forward
```

---

_Regenerado por `scripts/build_ticker_hubs.py`. Run novamente para refresh._

#### — · Panorama
_source: `tickers\BBDC4.md` (now in cemetery)_

#### BBDC4 — Bradesco

#holding #br #banks

##### 🎯 Verdict — 🟡 WATCH

> **Score**: 6.6/10  |  **Confiança**: 60%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 5.3/10 | 35% | `█████░░░░░` |
| Valuation  | 10.0/10 | 30% | `██████████` |
| Momentum   | 3.3/10 | 20% | `███░░░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski None/9 (N/A), DivSafety 62.5/100
- **Valuation**: Screen 1.00, DY percentil P82 (CHEAP)
- **Momentum**: 1d -3.89%, 30d -8.18%, YTD 1.65%
- **Narrativa**: user_note=False, YT insights 60d=5

###### Razões

- valuation atractiva mas quality ou momentum fraco
- valuation barato
- DY percentil P82 (historicamente CHEAP)

##### Links

- Sector: [[sectors/Banks|Banks]]
- Market: [[markets/BR|BR]]
- Peers: [[ABCB4]] · [[BBAS3]] · [[BPAC11]] · [[ITUB4]] · [[SANB11]]
- Vídeos: [[videos/2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al|BBDC3 OU BBDC4? O BANCO MAIS BARATO COM ]]
- 🎯 **Thesis**: [[wiki/holdings/BBDC4|thesis deep]]

##### Snapshot

- **Preço**: R$18.52  (2026-05-07)    _-3.89% 1d_
- **Screen**: 1.0  ✓ PASS
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 62.5/100 (WATCH)
- **Posição**: 1837.0 sh @ R$16.1  →  P&L 15.03%

##### Fundamentals

- P/E: 8.694836 | P/B: 1.097937 | DY: 8.23%
- ROE: 13.75% | EPS: 2.13 | BVPS: 16.868
- Streak div: 19y | Aristocrat: None

##### Dividendos recentes

- 2026-06-02: R$0.0190
- 2026-05-05: R$0.0190
- 2026-04-07: R$0.2973
- 2026-04-02: R$0.0190
- 2026-03-03: R$0.0190

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Fechamento da Consolidaçã
- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Publicação dos Relatórios
- **2026-04-15** `comunicado` — Esclarecimentos sobre questionamentos da CVM/B3 | Notícia Divulgada na Mídia
- **2026-04-06** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre a Reorg
- **2026-03-25** `fato_relevante` — Pagamento de Juros sobre o Capital Próprio Intermediários

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=8 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Virtual Asset | dividend | 0.90 | O Bradesco anunciou um lucro líquido de 6,8 bilhões de reais no primeiro trimestre e está distribuindo dividendos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção para quem busca dividendos sintéticos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção barata para investidores. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | O Bradesco ainda enfrenta riscos devido à inadimplência e competição com outros bancos. |
| 2026-05-11 | Virtual Asset | operational | 0.80 | O Bradesco está mostrando recuperação gradual na rentabilidade e margem financeira. |
| 2026-04-16 | Virtual Asset | guidance | 0.90 | O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.80 | O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotaç… |
| 2026-04-16 | Virtual Asset | valuation | 0.80 | O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado. |
| 2026-04-16 | Virtual Asset | dividend | 0.70 | O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.70 | O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E. |
| 2026-04-24 | XP | rating | — | — | A recomendação para o Bradesco é Neutra. |
| 2026-04-24 | XP | sector_view | — | — | O ambiente macroeconômico desafiador e expectativas de cortes da Selic pioraram no 1T26. |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] BBDC4 — peso 3.1% |
| 2026-04-24 | XP | thesis | neutral | 24.00 | O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores. |
| 2026-04-24 | XP | risk | bear | — | Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco. |
| 2026-04-24 | XP | catalyst | neutral | — | O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios. |
| 2026-04-24 | XP | thesis | neutral | — | O Bradesco está em uma recuperação gradual, mas o upside é limitado. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-11 | Virtual Asset | banking_br | bearish | Apesar do lucro forte, o Bradesco ainda enfrenta preocupações com sinais de pressão na carteira e consumo de… |
| 2026-05-11 | Virtual Asset | banking_br | neutral | O Bradesco ainda está atrás do Itaú em termos de rentabilidade, com um ROE de 15,8% contra 24-25% do Itaú, in… |
| 2026-05-11 | Virtual Asset | banking_br | bullish | O Bradesco apresentou um lucro líquido recorrente de R$6,8 bilhões no primeiro trimestre, com uma alta de 16,… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -14.89%
- **Drawdown 5y**: -28.37%
- **YTD**: +1.65%
- **YoY (1y)**: +42.02%
- **CAGR 3y**: +6.53%  |  **5y**: -3.27%  |  **10y**: +3.44%
- **Vol annual**: +28.52%
- **Sharpe 3y** (rf=4%): +0.09

###### Dividendos
- **DY 5y avg**: +6.92%
- **Div CAGR 5y**: +1.01%
- **Frequency**: irregular
- **Streak** (sem cortes): 11 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$108.85B | R$21.22B | R$40.36B |
| 2023-12-31 | R$98.33B | R$14.25B | R$-9.32B |
| 2024-12-31 | R$105.33B | R$17.25B | R$42.18B |
| 2025-12-31 | R$117.81B | R$23.67B | R$-74.16B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "BBDC4 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-28', '2026-05-05']
series:
  - title: BBDC4
    data: [15.08, 15.2, 15.69, 15.72, 16.2, 15.97, 16.32, 16.89, 16.54, 16.83, 16.67, 16.14, 16.06, 15.63, 15.44, 15.56, 15.79, 16.13, 15.79, 16.35, 16.83, 16.83, 16.87, 16.99, 17.74, 17.66, 17.09, 16.99, 17.16, 18.01, 18.08, 18.1, 18.79, 19.49, 19.32, 18.8, 19.65, 19.27, 18.33, 18.4, 18.24, 18.19, 18.84, 18.19, 18.9, 20.79, 21.44, 20.98, 20.92, 20.91, 21.4, 21.23, 19.55, 19.39, 18.63, 18.94, 18.47, 19.33, 20.44, 20.85, 19.97, 19.57, 19.19]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "BBDC4 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.6836, 0.706, 0.5965, 1.5066, 0.5738, 0.925, 0.4174, 1.6969, 0.8203, 1.7301, 0.3922]
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
    data: [9.2, 9.8732395, 9.375586, 9.352112, 9.352112, 9.352112, 9.26291, 9.187793, 8.97183, 9.070422, 8.8779335, 9.00939, 9.046948, 8.694836]
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
    data: [13.37, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75, 13.75]
  - title: DY %
    data: [5.98, 7.16, 7.54, 7.56, 7.56, 7.56, 7.63, 7.69, 7.88, 7.79, 7.96, 7.85, 7.81, 8.23]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\BBDC4_DOSSIE.md` (now in cemetery)_

#### 📑 BBDC4 — Bradesco

_Strategy: **Dividend/DRIP (5/12)**_

> Generated **2026-05-05** by `ii dossier BBDC4`. Cross-links: [[BBDC4]] · [[BBDC4_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

<!-- TODO_CLAUDE_TLDR: 3 frases sobre BBDC4 a partir das tabelas abaixo. Citar PE, DY, IC verdict, e o achado mais importante. -->

##### 1. Fundamentals snapshot

- **Período**: 2026-05-04
- **EPS**: 2.13  |  **BVPS**: 16.87
- **ROE**: 13.75%  |  **P/E**: 8.88  |  **P/B**: 1.12
- **DY**: 7.96%  |  **Streak div**: 19y  |  **Market cap**: R$ 199.89B
- **Last price**: BRL 18.91 (2026-05-04)  |  **YoY**: +40.7%

##### 2. Strategy classification

**Primary**: Dividend/DRIP (5/12)

| Lente | Score | Sinais |
|---|---|---|
| Value (Graham) | **2/12** | +2 · P/B 1.12 < 1.5x |
| Growth | **0/12** | — |
| Dividend/DRIP | **5/12** | +2 · DY 8.0% > 5% · +2 · Histórico ininterrupto 19 anos ≥ 5 · +1 · JCP+Dividendo recurring BR market |
| Buffett/Quality | **1/12** | +1 · Streak 19 anos ≥ 10 (consistência) |
| Macro (Exp/Dep) | 0/6 + 0/6 = 0/12 | — |

##### 3. Multiples vs Sector (Banks)

| Múltiplo | BBDC4 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 8.88x | 10.57x | 9.00x |
| P/B | 1.12x | 0.90x | 1.60x |
| DY | 8.0% | 8.0% | 6.0% |
| FCF Yield | -35.1% | 5.7% | 5.0% |
| ROE | 13.8% | 15.5% | 13.0% |
| ND/EBITDA | — | — | — |

_Peer set (db): 5 tickers — ITUB4, BBAS3, BPAC11, ABCB4, SANB11_

##### 4. Screen — BR Banks (CLAUDE.md)

| Critério | Threshold | Valor | OK? |
|---|---|---|---|
| P/E ≤ 10 | ≤ 10 | **8.88** | ✅ |
| P/B ≤ 1.5 | ≤ 1.5 | **1.12** | ✅ |
| DY ≥ 6% | ≥ 6% | **7.96%** | ✅ |
| ROE ≥ 12% | ≥ 12% | **13.75%** | ✅ |
| Streak div ≥ 5y | ≥ 5 | **19y** | ✅ |

→ **5/5 critérios** passam.

##### 5. Peer comparison

###### Fundamentals

| Métrica | BBDC4 | ABCB4 | ITUB4 |
|---|---|---|---|
| Market cap | R$ 199.89B | R$ 6.52B | R$ 467.31B |
| P/E | 8.88 | 4.73 | 10.57 |
| P/B | 1.12 | 0.90 | 2.29 |
| ROE | 13.75% | 15.46% | 21.01% |
| DY | 7.96% | 10.30% | 8.04% |
| Streak div | 19y | 16y | 19y |
| YoY price | +40.7% | +21.0% | +23.1% |

###### BACEN regulatório (latest non-NULL)

| Métrica | BBDC4 | ABCB4 | ITUB4 |
|---|---|---|---|
| Período | 2025-09-30 | 2025-09-30 | 2025-09-30 |
| Basel | 15.85% | 16.71% | 16.40% |
| CET1 | 11.39% | 11.88% | 13.47% |
| NPL E-H | n/a | n/a | n/a |

##### 6. BACEN timeline — capital + crédito

| Período | Basel | CET1 | NPL E-H |
|---|---|---|---|
| 2018-03-31 | 15.87% | 11.58% | 7.70% |
| 2018-06-30 | 14.86% | 10.58% | 6.75% |
| 2018-09-30 | 16.78% | 11.43% | 6.63% |
| 2019-03-31 | 18.08% | 13.03% | 6.29% |
| 2019-06-30 | 18.64% | 13.66% | 6.14% |
| 2019-09-30 | 18.15% | 13.38% | 6.01% |
| 2019-12-31 | 16.50% | 12.02% | 6.10% |
| 2020-03-31 | 13.93% | 10.33% | 5.72% |
| 2020-06-30 | 15.04% | 11.47% | 6.16% |
| 2020-09-30 | 15.15% | 11.85% | 6.32% |
| 2020-12-31 | 15.81% | 12.69% | 6.23% |
| 2021-03-31 | 15.37% | 12.56% | 5.97% |
| 2021-06-30 | 15.95% | 13.07% | 5.73% |
| 2021-09-30 | 15.18% | 12.68% | 5.63% |
| 2021-12-31 | 15.76% | 12.49% | 5.80% |
| 2022-03-31 | 15.68% | 12.47% | 6.50% |
| 2022-06-30 | 15.65% | 11.88% | 7.05% |
| 2022-09-30 | 15.82% | 12.13% | 7.28% |
| 2022-12-31 | 14.85% | 10.96% | 8.49% |
| 2023-03-31 | 15.09% | 11.07% | 9.57% |
| 2023-06-30 | 15.54% | 11.43% | 10.13% |
| 2023-09-30 | 15.99% | 11.85% | 10.14% |
| 2023-12-31 | 15.82% | 11.68% | 9.17% |
| 2024-03-31 | 15.38% | 11.21% | 8.35% |
| 2024-06-30 | 15.19% | 11.11% | 7.91% |
| 2024-09-30 | 15.10% | 11.23% | 7.44% |
| 2024-12-31 | 14.78% | 10.51% | 6.98% |
| 2025-03-31 | 15.45% | 11.08% | pending |
| 2025-06-30 | 15.47% | 11.06% | pending |
| 2025-09-30 | 15.85% | 11.39% | pending |

<!-- TODO_CLAUDE_BACEN_INSIGHT: 3-4 bullets sobre tendência Basel/NPL + comparação peer. Identificar peak ciclo + recovery. -->

##### 7. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[BBDC4_IC_DEBATE]]

##### 8. Thesis

**Core thesis (2026-04-24)**: A Bradesco, com seu preço atual de R$19.96 e um P/E de 9.38, oferece uma oportunidade única para investidores Buffett/Graham em busca de valor a longo prazo. A empresa possui um sólido histórico de dividendos, mantendo-o por 19 anos consecutivos, com um rendimento atual de 7.54%. Além disso, o ROE de 13.75% e a relação Patrimônio Líquido/Patrimônio (PB) de 1.18 indicam uma gestão eficiente e sustentável do capital.

**Key assumptions**:
1. A Bradesco continuará a manter seu histórico de dividendos por mais pelo menos os próximos cinco anos.
2. O P/E da empresa permanecerá abaixo de 10 nos próximos três anos, refletindo uma avaliação justa ou subavaliada em relação ao mercado.
3. A taxa ROE se mantém acima de 12% durante o mesmo período, indicando eficiência op

→ Vault: [[BBDC4]]

##### 9. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **92** |
| Thesis health | 100 |
| IC consensus | 92 |
| Variant perception | 70 |
| Data coverage | 100 |
| Paper track | 90 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 8.88** → [[Glossary/PE|porquê isto importa?]]. Bancos BR têm spread alto e múltiplos comprimidos — target ≤ 10. **Actual 8.88** passa.
- **P/B = 1.12** → [[Glossary/PB|leitura completa]]. Bancos: P/B ≤ 1.5 = margem sobre equity. **1.12** OK.
- **DY = 7.96%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **7.96%** passa.
- **ROE = 13.75%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Bancos BR (Selic alta): target ≥ 12%. **13.75%** OK.
- **Streak div = 19y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.
- **Basel = 15.85%** → [[Glossary/Basel_Ratio|capital regulatório]]. Tier **saudável** (mín BCB ~10.5%; saudável ≥14%; premium ≥16%).
- **CET1 = 11.39%** → [[Glossary/CET1|capital high-quality]]. Tier **saudável** (≥11% médio peer BR; ≥13% leadership tipo ITUB4).

###### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.

##### 10. Riscos identificados

<!-- TODO_CLAUDE_RISKS: 3-5 riscos prioritizados, baseados em IC + thesis + peer compare. Severidade 🟢🟡🔴. Cite trigger condition específica. -->

##### 11. Position sizing

**Status atual**: holding (in portfolio)

<!-- TODO_CLAUDE_SIZING: guidance breve para entrada/aumento/redução. Considerar BR/US isolation, market cap, weight prudente, DRIP/cash deploy. -->

##### 12. Tracking triggers (auto-monitoring)

<!-- TODO_CLAUDE_TRIGGERS: 3-5 condições mensuráveis em SQL/data que indicariam re-avaliação. Ex: 'NPL > 4%', 'DY < 5.5%', 'thesis_health score < 60'. Citar tabela/coluna a monitorar. -->

##### 13. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| BACEN backfill | Olinda OData | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier BBDC4` on 2026-05-05. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=8 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Virtual Asset | dividend | 0.90 | O Bradesco anunciou um lucro líquido de 6,8 bilhões de reais no primeiro trimestre e está distribuindo dividendos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção para quem busca dividendos sintéticos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção barata para investidores. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | O Bradesco ainda enfrenta riscos devido à inadimplência e competição com outros bancos. |
| 2026-05-11 | Virtual Asset | operational | 0.80 | O Bradesco está mostrando recuperação gradual na rentabilidade e margem financeira. |
| 2026-04-16 | Virtual Asset | guidance | 0.90 | O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.80 | O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotaç… |
| 2026-04-16 | Virtual Asset | valuation | 0.80 | O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado. |
| 2026-04-16 | Virtual Asset | dividend | 0.70 | O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.70 | O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E. |
| 2026-04-24 | XP | rating | — | — | A recomendação para o Bradesco é Neutra. |
| 2026-04-24 | XP | sector_view | — | — | O ambiente macroeconômico desafiador e expectativas de cortes da Selic pioraram no 1T26. |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] BBDC4 — peso 3.1% |
| 2026-04-24 | XP | thesis | neutral | 24.00 | O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores. |
| 2026-04-24 | XP | risk | bear | — | Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco. |
| 2026-04-24 | XP | catalyst | neutral | — | O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios. |
| 2026-04-24 | XP | thesis | neutral | — | O Bradesco está em uma recuperação gradual, mas o upside é limitado. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-11 | Virtual Asset | banking_br | bearish | Apesar do lucro forte, o Bradesco ainda enfrenta preocupações com sinais de pressão na carteira e consumo de… |
| 2026-05-11 | Virtual Asset | banking_br | neutral | O Bradesco ainda está atrás do Itaú em termos de rentabilidade, com um ROE de 15,8% contra 24-25% do Itaú, in… |
| 2026-05-11 | Virtual Asset | banking_br | bullish | O Bradesco apresentou um lucro líquido recorrente de R$6,8 bilhões no primeiro trimestre, com uma alta de 16,… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |

#### — · IC Debate (synthetic)
_source: `tickers\BBDC4_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — BBDC4

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=2 | HOLD=3 | AVOID=0  
**Avg conviction majority**: 5.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE abaixo de 15%
- FCF inconsistente
- P/E razoável

**Key risk**: Incerteza macroeconômica afetando lucratividade e geração de caixa

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E baixo e dividendos atraentes
- Histórico de pagamento de dividendos forte
- ROE sustentável

**Key risk**: Competição intensa do setor financeiro digital pode afetar margens

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável, dividendos sólidos
- PB ligeiramente acima da média
- Histórico de ROE forte

**Key risk**: Volatilidade do mercado financeiro e concorrência digital

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E baixo, mas não oferece margem de segurança significativa
- ROE estável, mas não excepcional
- Histórico de dividendos positivo

**Key risk**: Possível subavaliação do risco em um ambiente econômico incerto

###### 🟢 Ray Dalio — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E baixo e dividendos atraentes
- Histórico de pagamento de dividendos forte
- ROE sustentável

**Key risk**: Aumento da concorrência digital no setor bancário brasileiro

##### 📊 Context provided

```
TICKER: BR:BBDC4

FUNDAMENTALS LATEST:
  pe: 8.852382
  pb: 1.1020868
  dy: 8.20%
  intangible_pct_assets: 1.1%   (goodwill $6.6B + intangibles $19.1B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=70.4 ebit=4.9 ni=5.6 em%=6.9 debt=667 fcf=11.7
  2025-06-30: rev=65.3 ebit=4.3 ni=6.1 em%=6.6 debt=642 fcf=45.7
  2025-03-31: rev=60.1 ebit=6.1 ni=5.7 em%=10.1 debt=623 fcf=-31.3
  2024-12-31: rev=56.5 ebit=3.3 ni=4.2 em%=5.8 debt=649 fcf=0.5
  2024-09-30: rev=52.5 ebit=5.6 ni=4.9 em%=10.6 debt=617 fcf=2.2
  2024-06-30: rev=51.5 ebit=3.7 ni=4.2 em%=7.2 debt=619 fcf=22.0

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: A Bradesco, com seu preço atual de R$19.96 e um P/E de 9.38, oferece uma oportunidade única para investidores Buffett/Graham em busca de valor a longo prazo. A empresa possui um sólido histórico de dividendos, mantendo-o por 19 anos consecutivos, com um rendimento atual de 7.54%. Além disso, o ROE de 13.75% e a relação Patrimônio Líquido/Patrimônio (PB) de 1.18 indicam uma gestão eficiente e sustentável do capital.

**Key assumptions**:
1. A Bradesco continuará a manter seu histórico de dividendos por mais pelo menos os próximos cinco anos.
2. O P/E da empresa permanecerá abaixo de 10 nos próximos três anos, refletindo uma avaliação justa ou subavaliada em relação ao mercado.
3. A taxa ROE se mantém acima de 12% durante o mesmo período, indicando eficiência op

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest - World Oil [Thu, 23 Ap]
    # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetrol** has agreed to acquire an initial equity stake in **Brava Energia** as part of a broader plan 
  - Nubank: Investing in the Future of Brazil - FinTech Magazine [Wed, 29 Ap]
    # Nubank: Investing in the Future of Brazil. The largest digital bank in LATAM 
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=8 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Virtual Asset | dividend | 0.90 | O Bradesco anunciou um lucro líquido de 6,8 bilhões de reais no primeiro trimestre e está distribuindo dividendos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção para quem busca dividendos sintéticos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção barata para investidores. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | O Bradesco ainda enfrenta riscos devido à inadimplência e competição com outros bancos. |
| 2026-05-11 | Virtual Asset | operational | 0.80 | O Bradesco está mostrando recuperação gradual na rentabilidade e margem financeira. |
| 2026-04-16 | Virtual Asset | guidance | 0.90 | O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.80 | O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotaç… |
| 2026-04-16 | Virtual Asset | valuation | 0.80 | O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado. |
| 2026-04-16 | Virtual Asset | dividend | 0.70 | O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.70 | O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E. |
| 2026-04-24 | XP | rating | — | — | A recomendação para o Bradesco é Neutra. |
| 2026-04-24 | XP | sector_view | — | — | O ambiente macroeconômico desafiador e expectativas de cortes da Selic pioraram no 1T26. |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] BBDC4 — peso 3.1% |
| 2026-04-24 | XP | thesis | neutral | 24.00 | O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores. |
| 2026-04-24 | XP | risk | bear | — | Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco. |
| 2026-04-24 | XP | catalyst | neutral | — | O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios. |
| 2026-04-24 | XP | thesis | neutral | — | O Bradesco está em uma recuperação gradual, mas o upside é limitado. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-11 | Virtual Asset | banking_br | bearish | Apesar do lucro forte, o Bradesco ainda enfrenta preocupações com sinais de pressão na carteira e consumo de… |
| 2026-05-11 | Virtual Asset | banking_br | neutral | O Bradesco ainda está atrás do Itaú em termos de rentabilidade, com um ROE de 15,8% contra 24-25% do Itaú, in… |
| 2026-05-11 | Virtual Asset | banking_br | bullish | O Bradesco apresentou um lucro líquido recorrente de R$6,8 bilhões no primeiro trimestre, com uma alta de 16,… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |

#### — · RI / disclosure
_source: `tickers\BBDC4_RI.md` (now in cemetery)_

#### BBDC4 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `fco`: **-97.9%**
- ⬇️ **QOQ** `fcf_proxy`: **-74.3%**
- ⬆️ **YOY** `revenue`: **+34.0%**
- ⬆️ **YOY** `fco`: **+113.0%**
- ⬆️ **YOY** `fcf_proxy`: **+429.0%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 70.4 mi | R$ 65.3 mi | +7.7% |
| `ebit` | R$ 4.9 mi | R$ 4.3 mi | +12.7% |
| `net_income` | R$ 5.6 mi | R$ 6.1 mi | -9.3% |
| `debt_total` | R$ 667.1 mi | R$ 642.2 mi | +3.9% |
| `fco` | R$ 0.8 mi | R$ 39.8 mi | -97.9% |
| `fcf_proxy` | R$ 11.7 mi | R$ 45.7 mi | -74.3% |
| `gross_margin` | 25.1% | 29.2% | -4.1pp |
| `ebit_margin` | 6.9% | 6.6% | +0.3pp |
| `net_margin` | 7.9% | 9.4% | -1.5pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 70.4 mi | R$ 52.5 mi | +34.0% |
| `ebit` | R$ 4.9 mi | R$ 5.6 mi | -12.5% |
| `net_income` | R$ 5.6 mi | R$ 4.9 mi | +12.6% |
| `debt_total` | R$ 667.1 mi | R$ 616.7 mi | +8.2% |
| `fco` | R$ 0.8 mi | R$ -6.3 mi | +113.0% |
| `fcf_proxy` | R$ 11.7 mi | R$ 2.2 mi | +429.0% |
| `gross_margin` | 25.1% | 29.0% | -3.8pp |
| `ebit_margin` | 6.9% | 10.6% | -3.7pp |
| `net_margin` | 7.9% | 9.4% | -1.5pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 70.4 | 6.9% | 7.9% | 667 | 1 |
| 2025-06-30 | ITR | 65.3 | 6.6% | 9.4% | 642 | 40 |
| 2025-03-31 | ITR | 60.1 | 10.1% | 9.4% | 623 | -83 |
| 2024-12-31 | DFP-ITR | 56.5 | 5.8% | 7.5% | 649 | 10 |
| 2024-09-30 | ITR | 52.5 | 10.6% | 9.4% | 617 | -6 |
| 2024-06-30 | ITR | 51.5 | 7.2% | 8.1% | 619 | 29 |
| 2024-03-31 | ITR | 52.8 | 8.2% | 8.0% | 610 | 18 |
| 2023-12-31 | DFP-ITR | 54.1 | -2.2% | 2.7% | 626 | -81 |
| 2023-09-30 | ITR | 56.1 | 3.7% | 6.2% | 614 | 80 |
| 2023-06-30 | ITR | 56.9 | 5.4% | 7.2% | 594 | -20 |
| 2023-03-31 | ITR | 57.4 | 10.9% | 9.5% | 589 | 21 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [57.4, 56.9, 56.1, 54.1, 52.8, 51.5, 52.5, 56.5, 60.1, 65.3, 70.4]
  - title: EBIT margin %
    data: [10.9, 5.4, 3.7, -2.2, 8.2, 7.2, 10.6, 5.8, 10.1, 6.6, 6.9]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

#### — · Variant perception
_source: `tickers\BBDC4_VARIANT.md` (now in cemetery)_

#### 🎯 Variant Perception — BBDC4

**Our stance**: bullish  
**Analyst consensus** (8 insights, last 90d): neutral (20% bull)  
**Weighted consensus** (source win-rate weighted): neutral (20% bull)  
**Variance type**: `medium_variance_long` (magnitude 2/5)  
**Interpretation**: moderate edge

##### 🔍 Specific divergence analysis

Diverge: A NOSSA thesis prevê que o P/E da Bradesco permanecerá abaixo de 10 nos próximos três anos, enquanto o consenso analista aponta uma projeção de cerca de 7,8x P/L em 2026E. O consenso parece mais conservador nesse aspecto.

Alinhado: Ambos reconhecem a resiliência do Bradesco em ciclos econômicos anteriores e o potencial dos negócios não core para agregar valor à empresa, embora nossa tese enfatize mais a sustentabilidade de dividendos e ROE elevados.

Diverge: Enquanto nosso conselho foca nas métricas atuais que sugerem uma avaliação subavaliada (P/E de 9.38), o consenso analista considera um cenário macroeconômico mais desafiador potencialmente negativo para a empresa, indicando maior cautela em relação ao valor atual das ações.

##### 📰 Recent analyst insights

- [bull] *xp (w=0.50)* [BTG Equity Brazil] BBDC4 — peso 3.1%
- [neutral] *xp (w=0.50)* O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores.
- [neutral] *xp (w=0.50)* O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios.
- [bear] *xp (w=0.50)* Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco.
- [?] *xp (w=0.50)* As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E.
- [?] *xp (w=0.50)* A recomendação para o Bradesco é Neutra.
- [?] *xp (w=0.50)* O ambiente macroeconômico desafiador e expectativas de cortes da Selic pioraram no 1T26.
- [neutral] *xp (w=0.50)* O Bradesco está em uma recuperação gradual, mas o upside é limitado.

##### ⚖️ Source weights (predictions win-rate)

- 📊 `xp` → 0.50 *(no track record yet)*

##### 📜 Our thesis

**Core thesis (2026-04-24)**: A Bradesco, com seu preço atual de R$19.96 e um P/E de 9.38, oferece uma oportunidade única para investidores Buffett/Graham em busca de valor a longo prazo. A empresa possui um sólido histórico de dividendos, mantendo-o por 19 anos consecutivos, com um rendimento atual de 7.54%. Além disso, o ROE de 13.75% e a relação Patrimônio Líquido/Patrimônio (PB) de 1.18 indicam uma gestão eficiente e sustentável do capital.

**Key assumptions**:
1. A Bradesco continuará a manter seu histórico de dividendos por mais pelo menos os próximos cinco anos.
2. O P/E da empresa permanecerá abaixo de 10 nos próximos três anos, refletindo uma avaliação justa ou subavaliada em relação ao mercado.
3. A taxa ROE se mantém acima de 12% durante o mesmo período, indicando eficiência op

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=8 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Virtual Asset | dividend | 0.90 | O Bradesco anunciou um lucro líquido de 6,8 bilhões de reais no primeiro trimestre e está distribuindo dividendos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção para quem busca dividendos sintéticos. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações BBDC4 estão sendo vistas como uma opção barata para investidores. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | O Bradesco ainda enfrenta riscos devido à inadimplência e competição com outros bancos. |
| 2026-05-11 | Virtual Asset | operational | 0.80 | O Bradesco está mostrando recuperação gradual na rentabilidade e margem financeira. |
| 2026-04-16 | Virtual Asset | guidance | 0.90 | O Bradesco espera aumentar sua carteira de crédito expandida entre 8,5% a 10,5% em 2026. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.80 | O Bradesco tem um potencial de valorização com o preço-alvo ajustado para R$27, representando uma alta de cerca de 29,5% em relação à cotaç… |
| 2026-04-16 | Virtual Asset | valuation | 0.80 | O Bradesco está sendo negociado com um P/L de 8 vezes, considerado baixo em comparação ao benchmark do mercado. |
| 2026-04-16 | Virtual Asset | dividend | 0.70 | O Bradesco pagou dividendos crescentes, aumentando de R$9,2 bilhões em 2021 para R$14,5 bilhões em 2025. |
| 2026-04-16 | Virtual Asset | thesis_bull | 0.70 | O Bradesco tem uma carteira de crédito trilionária e cresceu 11% no ano, indicando um bom desempenho para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | As ações do Bradesco negociam atualmente a cerca de 7,8x P/L 2026E e 1,2x P/VP 2026E. |
| 2026-04-24 | XP | rating | — | — | A recomendação para o Bradesco é Neutra. |
| 2026-04-24 | XP | sector_view | — | — | O ambiente macroeconômico desafiador e expectativas de cortes da Selic pioraram no 1T26. |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] BBDC4 — peso 3.1% |
| 2026-04-24 | XP | thesis | neutral | 24.00 | O Bradesco tem executado melhor do que inicialmente esperávamos e se mostra mais resiliente em ciclos anteriores. |
| 2026-04-24 | XP | risk | bear | — | Um ambiente macroeconômico desafiador e pressão sobre a qualidade dos ativos podem impactar negativamente o Bradesco. |
| 2026-04-24 | XP | catalyst | neutral | — | O Bradesco apresenta opcionalidades estratégicas por meio de negócios não core, como seguros e consórcios. |
| 2026-04-24 | XP | thesis | neutral | — | O Bradesco está em uma recuperação gradual, mas o upside é limitado. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-11 | Virtual Asset | banking_br | bearish | Apesar do lucro forte, o Bradesco ainda enfrenta preocupações com sinais de pressão na carteira e consumo de… |
| 2026-05-11 | Virtual Asset | banking_br | neutral | O Bradesco ainda está atrás do Itaú em termos de rentabilidade, com um ROE de 15,8% contra 24-25% do Itaú, in… |
| 2026-05-11 | Virtual Asset | banking_br | bullish | O Bradesco apresentou um lucro líquido recorrente de R$6,8 bilhões no primeiro trimestre, com uma alta de 16,… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |

#### — · Wiki playbook
_source: `wiki\holdings\BBDC4.md` (now in cemetery)_

#### 🎯 Thesis: [[BBDC4]] — Bradesco

> Big-4 BR bank. Tese DRIP core. Em turnaround pós-2023 (ciclo inadimplência).

##### Intent
**DRIP core** — income + deep-value relative play vs Itaú.

##### Business snapshot
- Big-4 BR retail + corporate + seguridade (Bradesco Seguros, BBSE3 minority).
- Carteira crédito ~R$ 900B+ (top-3 BR).
- Rede agência + digital (Next, Ágora).
- **Sector class**: [[BR_Banks]] → scoring especial `score_br_bank` (não Graham).

##### Por que detemos

1. **Valuation deep-value** — P/B 0.9-1.1× vs ITUB4 1.7-1.9×. Desconto reflecte 2023 cycle pain.
2. **Dividend streak** consistente 10y+, pagou até no pior 2023.
3. **Seguros sub (BBSE)** = crown jewel — ROE 40%+ , low-capital business.
4. **Turnaround play** — novo CEO Marcelo Noronha 2024+; cost discipline + tech refocus.

##### Moat

- Big-4 scale → cost-to-income 40-45% stable.
- Bradesco Seguros dominância nicho.
- Corporate lending franchise profunda (décadas de relationship).
- **Weakness vs Itaú**: tech gap maior; retail market share eroded pelas fintechs.

##### Current state (2026-04)

- Post-2023: provisões peak, NPL estabilizando.
- ROE recovery path 14% → 17-18% target 2026.
- [[Selic]] descendo → NIM compressão LEVE mas inadimplência melhora.
- Guidance 2026 conservador — upside se executarem.
- BBSE valuation spin-off debate (create value se acontecer).

##### Invalidation triggers

- [ ] ROE < 12% por 2 anos consecutivos (vs target 17%)
- [ ] Dividend streak break (corte/suspensão)
- [ ] NPL 90d > 4.5% consistente (hoje ~4%)
- [ ] Perda CEO sem plano sucessão
- [ ] Basel ratio < 11%
- [ ] Agressiva regulação CVM sobre seguros (BBSE impact)

##### Sizing

- Posição actual: 1828 shares
- Target ~8% sleeve BR equity
- Reinvest dividendos + JCP → mais BBDC4 ou diversificar para [[ITSA4]] / TAEE11

##### Comparação peer BR bancos

| Ticker | P/B | ROE | Trait |
|---|---|---|---|
| [[ITUB4]] | 1.8× | 22% | quality premium |
| BBDC4 | 1.0× | 15% (recovering) | deep value |
| [[BBAS3]] | 0.8× | 20% | estatal desconto |
| [[SANB11]] | 1.1× | 15% | Santander BR |
| [[BPAC11]] | 3.0× | 25% | wealth growth |


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -8.23%
- **Drawdown 5y**: -22.76%
- **YTD**: +9.60%
- **YoY (1y)**: +51.86%
- **CAGR 3y**: +14.22%  |  **5y**: -1.37%  |  **10y**: +4.45%
- **Vol annual**: +28.17%
- **Sharpe 3y** (rf=4%): +0.35

###### Dividendos
- **DY 5y avg**: +6.92%
- **Div CAGR 5y**: +1.01%
- **Frequency**: irregular
- **Streak** (sem cortes): 11 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[BR_Banks]] — framework bancário + por que scoring especial
- [[ITSA4]] — comparação (Itaú via holding)
- [[Dividend_Safety]] — scoring income
- [[Selic]] — sensibilidade macro

## ⚙️ Refresh commands

```bash
ii panorama BBDC4 --write
ii deepdive BBDC4 --save-obsidian
ii verdict BBDC4 --narrate --write
ii fv BBDC4
python -m analytics.fair_value_forward --ticker BBDC4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
