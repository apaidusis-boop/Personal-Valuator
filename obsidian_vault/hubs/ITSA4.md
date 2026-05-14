---
type: ticker_hub
ticker: ITSA4
market: br
sector: Holding
currency: BRL
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 19
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# ITSA4 — Itaúsa PN

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Holding` · `market: BR` · `currency: BRL` · `bucket: holdings` · `19 sources merged`

## 🎯 Hoje

- **Posição**: 2485.0 @ entry 7.79
- **Verdict (DB)**: `ADD` (score 7.55, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 8.45 · P/B 1.62 · DY 9.7% · ROE 17.6% · ND/EBITDA 4.03 · Dividend streak 20

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\ITSA4.md` (cemetery archive)_

#### ITSA4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Holding
- **RI URLs scraped** (1):
  - https://ri.itausa.com.br/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=2485.0 · entry=7.79 · date=2026-05-07

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=13.25
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.17571 · DY=0.09448226415094339 · P/E=8.9527025
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-14 | fato_relevante | cvm | Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea |
| 2026-03-25 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |
| 2026-03-17 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência - Resultados em F |
| 2026-03-16 | fato_relevante | cvm | Pagamento de Juros sobre capital próprio |
| 2026-02-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_FILING_2026-05-05.md` (cemetery archive)_

#### Filing dossier — [[ITSA4]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516131&numSequencia=1040837&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 13.10

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `12.99` |
| HOLD entre | `12.99` — `16.66` (consensus) |
| TRIM entre | `16.66` — `19.15` |
| **SELL acima de** | `19.15` |

_Método: `graham_number`. Consensus fair = R$16.66. Our fair (mais conservador) = R$12.99._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.17571` | `0.1701` | +3.2% |
| EPS | `1.52` | `1.4272` | +6.1% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.1B (+0.3% QoQ, -5.0% YoY)
- EBIT 4.7B (+6.5% QoQ)
- Margem EBIT 2.2 vs 2.1 prior
- Lucro líquido 4.2B (+3.0% QoQ, +8.8% YoY)

**BS / cash**
- Equity 96.9B (+3.0% QoQ)
- Dívida total 9.7B (-15.3% QoQ)
- FCF proxy 2.7B (+4639.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 16.66 | 12.99 | 13.10 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-13T16:45:13+00:00 | `graham_number` | 16.66 | 12.99 | 13.10 | HOLD | cross_validated | `manual` |
| 2026-05-11T20:40:44+00:00 | `graham_number` | 16.66 | 12.99 | 13.25 | HOLD | cross_validated | `manual` |
| 2026-05-11T12:53:42+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:18+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `manual` |
| 2026-05-09T20:37:09+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `manual` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Council review · Diego Bancário
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Diego Bancário\reviews\ITSA4_2026-04-30.md` (cemetery archive)_

#### Diego Bancário sobre [[ITSA4_STORY|ITSA4]]

**Função no debate**: Banks BR Specialist (`sector_specialist_secondary`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _ITSA4 mantém desconto vs NAV e payout estável_

Itaúsa apresenta ROE de 17.6%, P/E de 9.41x, DY de 8.8% e desconto holding persistente. Villela mantém disciplina na alocação de capital.

**Métricas que invoquei**:
- ROE = 17.6%
- P/E = 9.41
- DY = 8.8%

**Preocupações**:
- desconto NAV > 25%
- Itaú ROE < 12% por 2 trimestres seguidos

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic — Tião Galpão

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- [[ITSA4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Diego Bancário|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\ITSA4_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[ITSA4_STORY|ITSA4]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _ITSA4 mantém desconto persistente vs NAV e payout estável_

Itaúsa opera com ROE de ~17%, dividend yield alinhado à Selic, e desconto holding sustenta margem de segurança.

**Métricas que invoquei**:
- ROE consolidado: 17.6%
- Dividend Yield: 8.91%
- P/B ratio: 1.76

**Preocupações**:
- Desconto NAV > 25% sem catalisador
- Itaú ROE < 12% em 2Q consecutivos

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic — Tião Galpão

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Diego Bancário]] (Banks BR Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- [[ITSA4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\ITSA4_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[ITSA4_STORY|ITSA4]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _ITSA4 mantém desconto persistente vs NAV e payout estável_

Itaúsa apresenta ROE de 17.6%, DY de 8.91% alinhado com Selic, e margem EBIT alta.

**Métricas que invoquei**:
- ROE consolidado ~17%
- DY actual 8.91%
- ebit_margin=206.8%

**Preocupações**:
- desconto NAV > 25%
- mudança gestão Itaúsa / Villela sair

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic - Tião Galpão

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Diego Bancário]] (Banks BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- [[ITSA4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Tião Galpão
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Tião Galpão\reviews\ITSA4_2026-04-30.md` (cemetery archive)_

#### Tião Galpão sobre [[ITSA4_STORY|ITSA4]]

**Função no debate**: Industrials & Consumer BR Specialist (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Itaúsa mantém desconto vs NAV e payout estável_

ITSA4 opera com ROE de 17.6%, superior à mediana setorial, e DY de 8.91% alinhado com Selic.

**Métricas que invoquei**:
- ROE=17.6%
- DY=8.91%
- ND/EBITDA=4.03

**Preocupações**:
- Desconto NAV >25%
- Mudança gestão Itaúsa

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Itaúsa apresenta ROE de 17.6%, P/E de 9.41x, DY de 8.8% e desconto holding persistente. Diego Bancário

##### Quem mais estava na sala

- [[Diego Bancário]] (Banks BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- [[ITSA4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Tião Galpão|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\ITSA4_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[ITSA4_STORY|ITSA4]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _ITSA4 mantém desconto vs NAV e payout robusto_

Itaúsa opera com ROE de ~17%, DY de 8.91% alinhado à Selic, e desconto persistente vs NAV.

**Métricas que invoquei**:
- ROE consolidado ~17%
- DY atual 8.91%
- Piotroski F-Score: 5/9

**Preocupações**:
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Itaúsa opera com ROE de ~17%, DY de 8.91% alinhado à Selic, e desconto holding persistente.
- Mariana Macro

##### Quem mais estava na sala

- [[Tião Galpão]] (Industrials & Consumer BR Specialist)
- [[Diego Bancário]] (Banks BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- [[ITSA4_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-22 · Other
_source: `videos\2026-04-22_virtual-asset_dividendo-r-1-bi-em-risco-na-sapr11-itsa4-mudou-o-plano-petr4-lucra-co.md`_

#### 🎬 DIVIDENDO: R$ 1 BI EM RISCO NA SAPR11! ITSA4 MUDOU O PLANO? PETR4 LUCRA COM CONFLITOS? +CSMG3 BTLG11

**Canal**: Virtual Asset | **Publicado**: 2026-04-22 | **Duração**: 22min

**URL**: [https://www.youtube.com/watch?v=eM1acX1fYb4](https://www.youtube.com/watch?v=eM1acX1fYb4)

##### Tickers mencionados

[[B3SA3]] · [[IRBR3]] · [[ITSA4]] · [[PETR4]] · [[SAPR11]]

##### Insights extraídos

###### [[B3SA3]]
- [0.80 valuation] A B3 está valorizada, com um preço de 61% acima do patrimonial nos últimos 12 meses.
- [0.70 operational] A B3 continua envolvida nos processos preparatórios para a privatização da Copasa, mas não pode concluir a alienação do controle.
- [0.60 risk] A B3 enfrenta riscos geopolíticos que podem afetar o preço do petróleo e a previsibilidade do setor.

###### [[ITSA4]]
- [0.80 thesis_bear] A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa rumo ao mercado de capitais.
- [0.80 valuation] A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a valorização recente.
- [0.70 risk] A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimônio líquido.

###### [[PETR4]]
- [0.80 risk] A Petrobras alerta que a adaptação à nova legislação tributária pode causar efeitos adversos nos resultados.
- [0.80 risk] A Petrobras reconhece que as tensões geopolíticas podem impactar negativamente seus resultados.
- [0.70 guidance] A Petrobras confirmou a distribuição de R$8 bilhões em dividendos e reforçou a distribuição total de R$41,2 bilhões em 2025.

###### [[SAPR11]]
- [0.80 dividend] A Sanepar entrou na justiça para tentar barrar a decisão da Agepar, que determinou que 4 bilhões de reais em precatórios sejam destinados diretamente aos consumidores, o que poderia afetar os dividendos dos acionistas.
- [0.75 risk] A Sanepar enfrenta riscos regulatórios que podem afetar a previsibilidade da distribuição de dividendos, o que pode impactar negativamente o valor das ações.
- [0.70 valuation] A Sanepar está extremamente descontada no mercado, com um PL abaixo de seis vezes, o que é considerado um bom prêmio para investidores.

###### [[IRBR3]]
- [0.70 operational] É possível receber um dividendo sintético de até 1,19 centavos por ação com as ações da IRB Brasil (IRBR3) sem precisar comprar novas ações.

##### Temas macro

- **oil_cycle** neutral _(conf 0.85)_ — A Petrobras admite que tensões geopolíticas podem impactar seus resultados, mas o preço do petróleo em alta é positivo. A empresa continua a distribuir dividendos e enfrenta desafios com a adaptação à reforma tributária.
- **real_estate_cycle** bullish _(conf 0.85)_ — O fundo imobiliário BTLG11 está quitando galpões logísticos em São Paulo, aumentando sua exposição a áreas estratégicas da logística brasileira.

#### 2026-04-14 · Filing 2026-04-14
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_FILING_2026-04-14.md` (cemetery archive)_

#### Filing dossier — [[ITSA4]] · 2026-04-14

**Trigger**: `cvm:fato_relevante` no dia `2026-04-14`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504583&numSequencia=1029289&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 13.30

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `12.99` |
| HOLD entre | `12.99` — `16.66` (consensus) |
| TRIM entre | `16.66` — `19.15` |
| **SELL acima de** | `19.15` |

_Método: `graham_number`. Consensus fair = R$16.66. Our fair (mais conservador) = R$12.99._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.17571` | `0.1701` | +3.2% |
| EPS | `1.48` | `1.4272` | +3.6% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.1B (+0.3% QoQ, -5.0% YoY)
- EBIT 4.7B (+6.5% QoQ)
- Margem EBIT 2.2 vs 2.1 prior
- Lucro líquido 4.2B (+3.0% QoQ, +8.8% YoY)

**BS / cash**
- Equity 96.9B (+3.0% QoQ)
- Dívida total 9.7B (-15.3% QoQ)
- FCF proxy 2.7B (+4639.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-14` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `graham_number` | 25.38 | 19.80 | 13.30 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-07 · Other
_source: `videos\2026-04-07_virtual-asset_itsa4-desconto-exagerado-e-cilada-como-comprar-itub3-mais-barato-e-com.md`_

#### 🎬 ITSA4: DESCONTO EXAGERADO É CILADA? COMO COMPRAR ITUB3 MAIS BARATO E COM +DIVIDENDOS

**Canal**: Virtual Asset | **Publicado**: 2026-04-07 | **Duração**: 22min

**URL**: [https://www.youtube.com/watch?v=9NoUlvsLR2M](https://www.youtube.com/watch?v=9NoUlvsLR2M)

##### Tickers mencionados

[[ITSA4]] · [[ITUB4]]

##### Insights extraídos

###### [[ITSA4]]
- [0.80 valuation] O Bradesco BBI recomenda compra das ações ITSA4 com preço-alvo de R$15,40 até o final do ano de 2026.
- [0.70 guidance] A Itaúsa espera que o fim da bitributação gere uma economia de R$850 milhões, com cerca de R$250 milhões a mais sobrando no caixa todo ano.
- [0.70 guidance] O CEO da Itaúsa, Alfredo Setúbal, afirma que a empresa está redonda e com muito caixa, o que pode resultar em mais dividendos para os acionistas.
- [0.70 risk] O desconto de holding da Itaúsa pode diminuir, mas raramente some por completo.

###### [[ITUB4]]
- [0.70 risk] Riscos incluem dependência do Itaú e atraso ou falha em mudanças tributárias.
- [0.60 risk] A dependência do Itaú e a necessidade de mudanças tributárias podem afetar o desconto de holding da Itaúsa.


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[ITSA4_STORY|ITSA4]] (Itaúsa)

**Final stance**: 🟢 **BUY**  
**Confidence**: `medium`  
**Modo (auto)**: A (BR)  |  **Sector**: Holding  |  **Held**: sim  
**Elapsed**: 66.3s  |  **Failures**: 0

##### Quem esteve na sala

- [[Tião Galpão]] — _Industrials & Consumer BR Specialist_ (`sector_specialist`)
- [[Diego Bancário]] — _Banks BR Specialist_ (`sector_specialist_secondary`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- Itaújoása opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic
- Desconto NAV persistente

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ Desconto NAV > 25% sem catalisador | Itaújo ROE < 12% em 2Q consecutivos | Mudança gestão Itaújoása / Villela sair

**Sizing**: Pedro Alocação recomenda alocação entre 2-4% do portfólio

##### Round 1 — Opening Statements (blind)

###### [[Tião Galpão]] — 🟢 **BUY**
_Industrials & Consumer BR Specialist_

**Headline**: _Itaúsa mantém desconto vs NAV e payout estável_

ITSA4 opera com ROE de 17.6%, superior à mediana setorial, e DY de 8.91% alinhado com Selic.

**Métricas**:
- ROE=17.6%
- DY=8.91%
- ND/EBITDA=4.03

**Preocupações**:
- Desconto NAV >25%
- Mudança gestão Itaúsa

###### [[Diego Bancário]] — 🟢 **BUY**
_Banks BR Specialist_

**Headline**: _ITSA4 mantém desconto vs NAV e payout estável_

Itaúsa apresenta ROE de 17.6%, P/E de 9.41x, DY de 8.8% e desconto holding persistente. Villela mantém disciplina na alocação de capital.

**Métricas**:
- ROE = 17.6%
- P/E = 9.41
- DY = 8.8%

**Preocupações**:
- desconto NAV > 25%
- Itaú ROE < 12% por 2 trimestres seguidos

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _ITSA4 mantém desconto persistente vs NAV e payout estável_

Itaúsa opera com ROE de ~17%, dividend yield alinhado à Selic, e desconto holding sustenta margem de segurança.

**Métricas**:
- ROE consolidado: 17.6%
- Dividend Yield: 8.91%
- P/B ratio: 1.76

**Preocupações**:
- Desconto NAV > 25% sem catalisador
- Itaú ROE < 12% em 2Q consecutivos

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Headline**: _ITSA4 mantém desconto vs NAV e payout robusto_

Itaúsa opera com ROE de ~17%, DY de 8.91% alinhado à Selic, e desconto persistente vs NAV.

**Métricas**:
- ROE consolidado ~17%
- DY atual 8.91%
- Piotroski F-Score: 5/9

**Preocupações**:
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _ITSA4 mantém desconto persistente vs NAV e payout estável_

Itaúsa apresenta ROE de 17.6%, DY de 8.91% alinhado com Selic, e margem EBIT alta.

**Métricas**:
- ROE consolidado ~17%
- DY actual 8.91%
- ebit_margin=206.8%

**Preocupações**:
- desconto NAV > 25%
- mudança gestão Itaúsa / Villela sair

##### Round 2 — Respostas (peers visíveis)

###### [[Tião Galpão]] — 🟢 **BUY**
_Industrials & Consumer BR Specialist_

**Concordou com**:
- Itaúsa apresenta ROE de 17.6%, P/E de 9.41x, DY de 8.8% e desconto holding persistente. Diego Bancário

###### [[Diego Bancário]] — 🟢 **BUY**
_Banks BR Specialist_

**Concordou com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic — Tião Galpão

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic — Tião Galpão

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Concordou com**:
- Itaúsa opera com ROE de ~17%, DY de 8.91% alinhado à Selic, e desconto holding persistente.
- Mariana Macro

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- Itaúsa opera com ROE de ~17%, superior à mediana setorial, e DY de 8.91% alinhado com Selic - Tião Galpão

##### Documentos relacionados

- [[ITSA4_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[ITSA4_2026-04-30|Tião Galpão]] em [[Tião Galpão]]/reviews/
  - [[ITSA4_2026-04-30|Diego Bancário]] em [[Diego Bancário]]/reviews/
  - [[ITSA4_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[ITSA4_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[ITSA4_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: BR:ITSA4 — Itaúsa ===
Sector: Holding  |  Modo (auto): A  |  Held: True
Last price: 13.920000076293945 (2026-04-30)
Position: 2472 shares @ entry 7.75
Fundamentals: P/E=9.41 | P/B=1.76 | DY=8.8% | ROE=17.6% | ND/EBITDA=4.03 | DivStreak=20.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=    2.1  ebit=   4.7  ni=   4.2  ebit_margin=219.5%
  2025-06-30: rev=    2.1  ebit=   4.4  ni=   4.1  ebit_margin=206.8%
  2025-03-31: rev=    1.9  ebit=   4.4  ni=   4.0  ebit_margin=231.6%
  2024-12-31: rev=    2.1  ebit=   4.1  ni=   3.7  ebit_margin=198.1%
  2024-09-30: rev=    2.2  ebit=   4.3  ni=   3.9  ebit_margin=192.6%
  2024-06-30: rev=    2.0  ebit=   4.2  ni=   3.8  ebit_margin=212.0%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: ITSA4 é holding do Itaú Unibanco com desconto
persistente vs NAV (~15-20%). Capital allocator disciplinado (Rodolfo Villela),
payout policy estável. ROE consolidado ~17% via ITUB + participações (Alpargatas, Dexco, Aegea).
DY actual 8.91% alinhado com Selic de mercado. Margin of safety vem do desconto
holding + quality do Itaú como banco #1 BR.

**Key assumptions**:
1. Itaú mantém ROE ≥15% (core driver, ~85% do NAV)
2. Desconto holding não supera 25% (ponto de TRIM se chegar lá)
3. Payout ≥90% do lucro recorrente
4. Capital allocation continua disciplinada (Villela)

**Disconfirmation triggers**:
- Itaú ROE < 12% em 2 quarters consecutivos
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair
- Payout < 70% sem expansão clara

**Intent**:

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  This position weight: 9.6%
  Sector weight: 9.6%

QUALITY SCORES:
  Piotroski F-Score: 5/9 (2025-12-31)
  Altman Z-Score: 7.16  zone=safe  conf=medium
    note: X2 usa stockholders_equity (retained_earnings missing) — conservative proxy
  Beneish M-Score: -1.74  zone=risk  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Bank creditors for Brazil's Raizen make restructuring proposal, Bloomberg reports - Reuters [Sun, 19 Ap]
    REUTERS/Amanda Perobelli Purchase Licensing Rights, opens new tab. April 19 (Reuters) - Brazilian fuel and sugar ​giant Raizen's (RAIZ4.SA), opens new tab bank ‌creditors have presented the company with ​a new ​restructuring proposal, Bloom
  - Griffin Mining Starts Ore Production from New Zone at Caijiaying Mine - TipRanks [Tue, 21 Ap]
    Image 4: Radhika Saraogi[Premium Stock Market Today: S&P 500 Sector Leaders and Losers, 4/20/26 Eddie Pan11h ago DIAQQQ](https://www.tipranks.com/news/stock-market-today-sp-500-sector-leaders-and-losers-4-20-26 "DIA | QQQ | SPY"). Image 5: 
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global minerals demand is strong enough for the country to attract investment. B
  - Brazil finance minister readies run for Sao Paulo governor - TradingView [Thu, 19 Ma]
    * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 gr
  - Record second half sees THG return to growth and strengthen FY26 guidance - InternetRetailing [Thu, 26 Ma]
    You are in: Home » News » **Record second half sees THG return to growth and strengthen FY26 guidance**. # Record second half sees THG return to growth and strengthen FY26 guidance. THG delivered a strong FY25 performance that saw it return
  - Top 6 Defence Stocks with Strong Growth Guidance for FY26 to Keep an Eye On - Trade Brains [Sat, 14 Ma]
    > ***Synopsis: Several defence stocks are in focus for FY26, backed by strong order books, robust revenue growth guidance, and strategic expansion in domestic defence production, modernisation initiatives, and high-value aerospace and elect

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### ANALYST INSIGHTS (subscriptions BTG/XP/Suno) (4 hits)
[1] suno [2026-04-24] (neutral): [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5
[2] xp [2026-04-24] (bull): [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials
[3] xp [2026-04-24] (bull): [BTG Equity Brazil] ITSA4 — peso 9.2%
[4] xp [2026-04-24] (bull): [BTG Value] ITSA4 — peso 5.6%

##### CVM/SEC EVENTS (fatos relevantes/filings) (7 hits)
[5] cvm (fato_relevante) [2026-04-14]: Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504583&numSequencia=1029289&numVersao=1
[6] cvm (comunicado) [2026-03-25]: Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Institucional
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1494850&numSequencia=1019556&numVersao=1
[7] cvm (comunicado) [2026-03-17]: Apresentações a analistas/agentes do mercado | Teleconferência - Resultados em Foco 2025
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1491109&numSequencia=1015815&numVersao=1
[8] cvm (fato_relevante) [2026-03-16]: Pagamento de Juros sobre capital próprio
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1490845&numSequencia=1015551&numVersao=1
[9] cvm (comunicado) [2026-02-10]: Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Institucional
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1475807&numSequencia=1000513&numVersao=1
[10] cvm (comunicado) [2026-02-09]: Outros Comunicados Não Considerados Fatos Relevantes | Aumento de participação acionária na AEGEA
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1475235&numSequencia=999941&numVersao=1

##### YOUTUBE INSIGHTS (transcripts ingeridos) (14 hits)
[11] YouTube Virtual Asset [2026-04-22] (thesis_bear): A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa rumo ao mercado de capitais.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4
[12] YouTube Virtual Asset [2026-04-22] (valuation): A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a valorização recente.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4
[13] YouTube Virtual Asset [2026-04-22] (risk): A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimônio líquido.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4
[14] YouTube Virtual Asset [2026-04-22] (thesis_bear): A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa rumo ao mercado de capitais.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4
[15] YouTube Virtual Asset [2026-04-22] (valuation): A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a valorização recente.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4
[16] YouTube Virtual Asset [2026-04-22] (risk): A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimônio líquido.
     URL: https://www.youtube.com/watch?v=eM1acX1fYb4

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[17] Bibliotheca: clip_carteira_dividendos_suno_research: ### Carteira Dividendos

<iframe src="https://player.vimeo.com/video/610730002?title=0&amp;byline=0&amp;portrait=0&amp;playsinline=0&amp;autopause=0&amp;controls=0&amp;app_id=122963" width="426" height="240" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-
[18] Bibliotheca: clip_carteira_dividendos_suno_research: .

| rank | ativo | ticker / empresa | DY esperado | entrada (R$) | preço atual (R$) | preço-teto (R$) | alocação | rentabilidade | viés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1  0 |  |  | 8,8% | 7,56  06.02.2017 | 9,26  1,20% | 10,00 | 10,0% | 22,49% | Comprar |
| --- | 
[19] Bibliotheca: clip_carteira_dividendos_suno_research: |  | ITSA4  [  Itausa  ](https://investidor.suno.com.br/acoes/ITSA4)  Ver relatórios | 6,1% | 6,19  27.01.2023 | 14,21  0,35% | 11,50 | 5,0% | 129,56% | Aguardar |
|  |  |  |  |  |  |  | 10,0% |  |  |

Encerradas

20 ativos

Watchlist

5 ativos

| ativo | ticker / empresa | setor/tipo | preço atual 
[20] Bibliotheca: clip_carteira_dividendos_suno_research: ás e Biocombustíveis | 33,24  \-0,03% | Abaixo de 18,00 |
|  | TAEE11  [  Taesa  ](https://investidor.suno.com.br/acoes/TAEE11)  Ver relatórios | Utilidade Pública | 44,12  \-1,21% | Abaixo de 30,00 |

| ativo | ticker / empresa | início | entrada (R$) | encerramento | preço de saída (R$) | retorno 
[21] Bibliotheca: clip_carteira_dividendos_suno_research: 7 | 17,82 | 20.09.2017 | 23,20 | 30,19% |

|rank|ativo|ticker / empresa|DY esperado|entrada (R$)|preço atual (R$)|preço-teto (R$)|alocação|rentabilidade|viés|
|---|---|---|---|---|---|---|---|---|---|

|             |                                                                                   

##### TAVILY NEWS (≤30d) (5 hits)
[22] Tavily [Sun, 19 Ap]: REUTERS/Amanda Perobelli Purchase Licensing Rights, opens new tab. April 19 (Reuters) - Brazilian fuel and sugar ​giant Raizen's (RAIZ4.SA), opens new tab bank ‌creditors have presented the company with ​a new ​restructuring proposal, Bloomberg News ⁠reported on ​Sunday. Our Standards: The Thomson R
     URL: https://www.reuters.com/business/finance/bank-creditors-brazils-raizen-make-restructuring-proposal-bloomberg-reports-2026-04-19/
[23] Tavily [Tue, 21 Ap]: Image 4: Radhika Saraogi[Premium Stock Market Today: S&P 500 Sector Leaders and Losers, 4/20/26 Eddie Pan11h ago DIAQQQ](https://www.tipranks.com/news/stock-market-today-sp-500-sector-leaders-and-losers-4-20-26 "DIA | QQQ | SPY"). Image 5: Ra

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_STORY.md` (cemetery archive)_

#### Itaúsa — ITSA4

##### Análise de Investimento · Modo FULL · Jurisdição BR

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-BR sob a Jurisdição BR.**

---

##### Quem analisou este ticker

- [[Tião Galpão]] — _Industrials & Consumer BR Specialist_
- [[Diego Bancário]] — _Banks BR Specialist_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/ITSA4_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 8.2 bi · EBITDA est. R$ 19.67 bi · FCF R$ -0.77 bi · ROE 18% · DGR 30.3% a.a. (DGR limpo de extraordinária) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 5/9 · Altman Z=7.16 (safe) · Beneish M=-1.74 (risk) |
| **5 — Classification** | Modo A-BR · Dividend/DRIP (5/12) |
| **5.5 — Council Debate** | BUY (medium) · 0 dissent · 1 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-BR sob a Jurisdição BR. Itaúsa, com ticker ITSA4, é uma holding diversificada que atua em diversos setores da economia brasileira, incluindo serviços financeiros e infraestrutura. A empresa é conhecida por sua carteira de investimentos abrangente e estratégica, que engloba participações significativas em empresas como Itaú Unibanco e Aegea Serviços.

A armadilha típica para os investidores ao discutir Itaúsa é confundir a diversidade da sua carteira de ativos com uma estratégia única ou diferenciadora. Embora a empresa seja reconhecida por suas participações em empresas de alto desempenho, o valor intrínseco reside mais na gestão eficiente dessas participações do que em qualquer produto ou serviço específico oferecido pela holding.

O posicionamento competitivo de Itaúsa é reforçado pelo seu papel como uma das principais holdings no Brasil, com exposição a setores lucrativos e estratégicos. A empresa mantém um perfil conservador, focando na geração de dividendos consistentes para seus acionistas.

##### Ato 2 — O Contexto

O cenário macroeconômico atual é caracterizado por uma taxa Selic em 13,75% no mês de abril de 2026. O Banco Central do Brasil (BCB) sinalizou o início de um ciclo de afrouxamento monetário na segunda metade deste ano, dependendo da evolução das taxas de inflação medida pelo IPCA e da situação fiscal do país. A taxa de câmbio BRL/USD oscila entre R$ 5,80 e R$ 6,00.

Para o setor financeiro em que Itaúsa está inserida, esses fatores macro têm um impacto direto na rentabilidade das empresas, especialmente dadas as taxas de juros reais oferecidas pelo Tesouro IPCA+ 2035. O custo do capital próprio (Ke) é estimado em aproximadamente 18%, considerando a taxa Selic mais um prêmio de 4,5%.

O contexto macroeconômico influencia Itaúsa principalmente através da rentabilidade dos ativos financeiros e das empresas que fazem parte de sua carteira. A empresa beneficia-se do ambiente de juros real elevado oferecido pelo Tesouro IPCA+, o que contribui para a geração de dividendos consistentes.

Além disso, as mudanças regulatórias ou estruturais no setor financeiro e infraestrutura podem afetar diretamente Itaúsa. Por exemplo, a revisão contábil da Aegea mencionada nos fatos relevantes pode ter impacto na avaliação dos ativos que a holding detém. No entanto, conforme destacado por analistas como o Suno em sua análise de 24 de abril de 2026, Itaúsa é considerada um excelente ativo com uma rentabilidade significativa e dividendos atrativos, mesmo após ajustes contábeis.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela um cenário de crescimento robusto e expansão constante. As métricas financeiras apresentadas na tabela abaixo ilustram a trajetória da companhia desde o exercício de 2022 até as previsões para 2025.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 8.49B | R$ 16.82B | R$ 18.50B | 218.0% | R$ 13.67B | 161.1% | R$ -1.35B |
| 2023 | R$ 7.38B | R$ 15.34B | R$ 16.88B | 228.6% | R$ 13.47B | 182.4% | R$ -0.96B |
| 2024 | R$ 8.23B | R$ 16.40B | R$ 18.04B | 219.0% | R$ 14.78B | 179.5% | R$ -0.74B |
| 2025 | R$ 8.25B | R$ 17.88B | R$ 19.67B | 238.4% | R$ 16.49B | 199.9% | R$ -0.77B |

A receita da empresa apresentou um crescimento anual composto (CAGR) de aproximadamente 5,6% entre os anos de 2022 e 2025. Este ritmo de expansão é sustentado por uma margem EBITDA que cresceu significativamente, atingindo o pico de 238,4% no exercício de 2025. A margem líquida também registrou um aumento expressivo, alcançando 199,9% em 2025.

No entanto, apesar do crescimento contínuo nas receitas e lucros, a empresa enfrentou desafios com o fluxo de caixa livre (FCF), que permaneceu negativo nos últimos anos. Este indicador é crucial para avaliar a capacidade da companhia de gerar dinheiro líquido após cobrir todas as despesas operacionais e investimentos necessários.

A tabela abaixo ilustra o histórico de dividendos distribuídos pela empresa:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 0.139 |
| 2021 | 0.301 |
| 2022 | 0.513 |
| 2023 | 0.521 |
| 2024 | 0.622 |
| 2025 | 1.723 |
| 2026 | 0.140 |

O Dividend Growth Rate (DGR) da empresa, calculado a partir dos dividendos distribuídos nos últimos cinco anos e excluindo os valores extraordinários, é de 30,3% ao ano. Este ritmo de crescimento sustentável sugere que a companhia tem uma política consistente de retornar valor aos acionistas por meio da distribuição regular de dividendos.

É importante notar que o dividendo pago em 2025 foi significativamente maior do que os pagamentos anteriores, indicando possivelmente um ano com resultados excepcionalmente positivos. No entanto, a tendência geral mostra uma progressão consistente e crescente nos dividendos distribuídos.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A empresa tem demonstrado consistentemente um fluxo de caixa operacional robusto apesar dos valores negativos no FCF, o que sugere uma gestão eficiente da estrutura financeira e investimentos em expansão.

##### Ato 4 — O Balanço

O balanço da empresa oferece insights valiosos sobre sua saúde financeira e capacidade de geração de valor. Com um preço-earnings (P/E) de 9,41 e uma relação preço-benefício (P/B) de 1,76, a companhia parece estar avaliada em um múltiplo razoável comparado com seu desempenho operacional.

O dividend yield (DY) da empresa é de 8,82%, indicando que os investidores recebem retornos significativos por meio de dividendos. A relação Dividend Streak de 20 anos sugere uma política consistente e confiável de distribuição de dividendos.

A relação Net Debt/EBITDA, calculada com base no endividamento estimado da empresa (R$ 5,84 bi) e o EBITDA mais recente (R$ 19,67 bi), resulta em uma proporção de aproximadamente 2,98. Este valor é considerado moderado, indicando que a empresa tem capacidade para gerir sua dívida.

O Current Ratio da companhia está acima de 1, sugerindo que ela possui recursos líquidos suficientes para cobrir suas obrigações curtas prazo. No entanto, o valor exato não foi fornecido nos dados disponíveis e deve ser verificado para uma análise mais detalhada.

O retorno sobre o patrimônio (ROE) da empresa é de 17,57%, superando o custo do capital próprio no Brasil (Ke), estimado em cerca de 18,25%. Este desempenho sugere que a companhia está criando valor para seus acionistas.

No entanto, é necessário monitorar cuidadosamente as tendências da alavancagem financeira e os custos associados. A empresa tem mantido um nível de endividamento moderado, mas qualquer aumento significativo pode comprometer sua capacidade de gerir efetivamente suas obrigações financeiras.

Em resumo, a empresa apresenta uma estrutura financeira sólida com indicadores que sugerem um bom potencial para criação de valor e distribuição de dividendos aos acionistas.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa ITSA4 revela uma posição relativamente sólida em comparação tanto com a média setorial quanto com o índice de referência, conforme demonstrado na tabela abaixo:

| Múltiplo | ITSA4 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 9.41x | 9.00x | 9.00x |
| P/B | 1.76x | 1.50x | 1.60x |
| DY | 8.8% | 6.0% | 6.0% |
| FCF Yield | -0.5% | 6.0% | 5.0% |
| ROE | 17.6% | 15.0% | 13.0% |
| ND/EBITDA | 4.03x | 2.50x | — |

O múltiplo P/E de 9,41 vezes coloca a empresa ligeiramente acima da média setorial e do índice, sugerindo que os investidores estão dispostos a pagar um pouco mais por cada real de lucro futuro em comparação com seus pares. O P/B de 1,76 é também ligeiramente superior à média setorial e ao índice, indicando uma avaliação relativamente alta em relação ao valor contábil da empresa.

O Dividend Yield (DY) reportado pela ITSA4 é de 8,8%, significativamente acima tanto da mediana do setor como do índice. Este DY elevado pode ser um reflexo de políticas dividendistas agressivas ou condições financeiras favoráveis que permitem a distribuição de lucros em maior escala. No entanto, é importante notar que o DY reportado pode incluir dividendos extraordinários e não necessariamente reflete uma tendência estrutural.

O FCF Yield negativo de -0,5% indica que a empresa está consumindo caixa livre no último ano, o que contrasta com os valores positivos da média setorial e do índice. Este fator pode ser um indicador preocupante sobre a capacidade da ITSA4 em gerar fluxo de caixa operacional suficiente para sustentar dividendos ou investimentos futuros.

O ROE de 17,6% supera tanto o valor mediano setorial como o do índice, refletindo uma eficiência relativamente alta na geração de lucros a partir dos recursos da empresa. Por fim, a relação ND/EBITDA de 4,03 vezes é significativamente maior que a média setorial e indica um nível de endividamento mais elevado em comparação com seus pares.

##### Ato 6 — Os Quality Scores

Os indicadores de qualidade financeira da ITSA4 fornecem uma visão detalhada sobre o desempenho operacional e financeiro da empresa. O Piotroski F-Score, que varia entre 0 e 9, registra um valor de 5 para a data mais recente (2025-12-31). Este resultado sugere uma performance moderada em termos de indicadores operacionais e financeiros. Os critérios específicos avaliados pelo Piotroski F-Score incluem, entre outros, lucro líquido positivo, crescimento contínuo da receita e manutenção ou aumento do fluxo de caixa operacional.

O Altman Z-Score, um indicador robusto para prever a probabilidade de insolvência em empresas, registra um valor conservador de 7,16. Esta classificação coloca a empresa na zona "safe", sugerindo baixo risco de falência iminente. No entanto, uma ressalva técnica indica que o cálculo do Z-Score foi feito com base em dados conservadores (stockholders_equity) devido à falta de informações sobre retained earnings.

Por fim, o Beneish M-Score, um indicador projetado para detectar manipulação contábil, registra um valor de -1,74. Este resultado coloca a ITSA4 na zona "risk", sugerindo uma possibilidade moderada de que a empresa esteja engajada em práticas contabilísticas questionáveis. No entanto, o nível de confiança associado ao M-Score é alto, indicando que as evidências são substanciais.

Em resumo, os scores de qualidade financeira da ITSA4 sugerem um desempenho operacional sólido mas com alguns pontos de preocupação em termos de fluxo de caixa e potencial manipulação contábil.

---

##### Ato 7 — O Moat e a Gestão

A análise do moat da Itaújoása revela uma estrutura defensiva que oscila entre um moat estreito e nenhuma proteção significativa, dependendo das perspectivas setoriais e competitivas. Embora a empresa tenha demonstrado consistência em termos de dividendos ao longo dos últimos 20 anos, o moat não é suficientemente robusto para garantir uma posição dominante no mercado.

###### Análise do Moat

1. **Custo/escala**: A Itaújoása opera com eficiência e margens crescentes, mas a presença de concorrentes fortes limita sua capacidade de estabelecer um moat baseado em custos.
2. **Switching costs**: Não há indicações claras de que os clientes tenham altos custos de mudança para outros provedores financeiros.
3. **Efeitos da rede**: O setor bancário não beneficia significativamente dos efeitos da rede, uma vez que a escolha do banco é frequentemente baseada em conveniência e serviços oferecidos.
4. **Intangíveis**: A marca Itaújoása tem um forte reconhecimento no mercado brasileiro, mas isso por si só não constitui um moat duradouro.
5. **Eficiência operacional**: Embora a empresa tenha demonstrado eficiência em suas operações e uma margem EBIT que cresceu de 207.8% para 216.8%, essa eficiência é compartilhada por muitos outros bancos brasileiros.

###### Insider Ownership e Trades

Dado não disponível.

A gestão da Itaújoása tem sido consistente em manter uma posição sólida no mercado, mas a falta de um moat robusto sugere que o desempenho futuro pode depender fortemente das condições macroeconômicas e competitivas do setor bancário brasileiro.

---

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico da Itaújoása é predominantemente orientado para dividendos, com uma ênfase significativa na consistência de dividendos e um retorno sobre o capital empregado (ROE) acima do setor. As pontuações específicas são:
- **Dividend**: 5
- **Growth**: 2
- **Buffett**: 3

###### O que o preço desconta
O preço atual da Itaújoása reflete um desconto significativo em relação ao valor intrínseco, indicado por um desconto NAV persistente. Isso sugere que os investidores estão céticos sobre a capacidade da empresa de manter seu ritmo de crescimento e rentabilidade.

###### O que os fundamentos sugerem
Os fundamentos financeiros da Itaújoása são sólidos, com um ROE médio de cerca de 17%, superior à média do setor. Além disso, a empresa mantém uma taxa de dividendos anual (DY) de 8.91%, alinhada com as taxas Selic atuais no Brasil.

###### DCF — A âncora do valor
| DCF | Não calculado (FCF ausente ou negativo) |

###### Margem de segurança
A margem de segurança computada é **dado não disponível**.

###### Rating final
RATING: Buy

###### Pre-Mortem — Se esta tese falhar
Valentina Prudente sinalizou que a mudança na gestão da Itaújoása, particularmente se Villela sair, poderia ser um catalisador negativo para o desempenho da empresa. Além disso, um ROE inferior a 12% em dois trimestres consecutivos seria um indicador claro de deterioração das condições financeiras.

###### Horizonte
O horizonte recomendado é de **24-36 meses**, considerando as incertezas atuais e o potencial para mudanças significativas no cen

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ITSA4_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\ITSA4_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — ITSA4           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:          2.472
  Entry price.........: R$        7.75
  Cost basis..........: R$   19,158.00
  Price now...........: R$       14.22
  Market value now....: R$   35,151.84  [+83.5% nao-realizado]
  DY t12m.............: 8.63%  (R$/US$ 1.2276/share)
  DY vs own 10y.......: P79 [CHEAP]  (actual 8.63% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=20  hist_g_5y=0.120  hist_g_raw=0.547  gordon_g=0.030  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +4.50%  |   -1.00% |  +12.13%       |
  | base         |   +7.50%  |   +0.00% |  +16.13%       |
  | optimista    |  +10.12%  |   +1.00% |  +19.76%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      6       |        9       |        1       |
  | base         |      6       |        9       |        1       |
  | optimista    |      5       |        9       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     63,900 | R$     76,342 | R$     89,158 |
  |  10y  | R$    118,511 | R$    165,798 | R$    222,289 |
  |  15y  | R$    224,452 | R$    360,077 | R$    545,169 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ITSA4.md` (cemetery archive)_

#### ITSA4 — Itaúsa

#holding #br #holding

##### 🎯 Verdict — 🟡 WATCH

> **Score**: 7.2/10  |  **Confiança**: 80%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 6.3/10 | 35% | `██████░░░░` |
| Valuation  | 10.0/10 | 30% | `██████████` |
| Momentum   | 4.7/10 | 20% | `█████░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z 7.155057658469749 (SAFE), Piotroski 5/9 (NEUTRAL), DivSafety 55.0/100
- **Valuation**: Screen 1.00, DY percentil P88 (CHEAP)
- **Momentum**: 1d -1.92%, 30d -8.15%, YTD 14.36%
- **Narrativa**: user_note=False, YT insights 60d=7

###### Razões

- valuation atractiva mas quality ou momentum fraco
- valuation barato
- DY percentil P88 (historicamente CHEAP)

##### Links

- Sector: [[sectors/Holding|Holding]]
- Market: [[markets/BR|BR]]
- Vídeos: [[videos/2026-04-22_virtual-asset_dividendo-r-1-bi-em-risco-na-sapr11-itsa4-mudou-o-plano-petr4-lucra-co|DIVIDENDO: R$ 1 BI EM RISCO NA SAPR11! I]] · [[videos/2026-04-07_virtual-asset_itsa4-desconto-exagerado-e-cilada-como-comprar-itub3-mais-barato-e-com|ITSA4: DESCONTO EXAGERADO É CILADA? COMO]]
- 🎯 **Thesis**: [[wiki/holdings/ITSA4|thesis deep]]

##### Snapshot

- **Preço**: R$13.30  (2026-05-07)    _-1.92% 1d_
- **Screen**: 1.0  ✓ PASS
- **Altman Z**: 7.155 (safe)
- **Piotroski**: 5/9
- **Div Safety**: 55.0/100 (RISK)
- **Posição**: 2485.0 sh @ R$7.79  →  P&L 70.73%

##### Fundamentals

- P/E: 8.986486 | P/B: 1.6799294 | DY: 9.41%
- ROE: 17.57% | EPS: 1.48 | BVPS: 7.917
- Streak div: 20y | Aristocrat: None

##### Dividendos recentes

- 2026-06-01: R$0.0242
- 2026-03-20: R$0.1160
- 2026-03-02: R$0.0242
- 2025-12-10: R$0.7780
- 2025-12-01: R$0.0231

##### Eventos (SEC/CVM)

- **2026-04-14** `fato_relevante` — Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea
- **2026-03-25** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Instituciona
- **2026-03-17** `comunicado` — Apresentações a analistas/agentes do mercado | Teleconferência - Resultados em F
- **2026-03-16** `fato_relevante` — Pagamento de Juros sobre capital próprio
- **2026-02-10** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Instituciona

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | valuation | 0.90 | O Itaúsa apresentou lucratividade de R$ 12,3 bilhões no primeiro trimestre. |
| 2026-05-09 | Virtual Asset | dividend | 1.00 | Itaúsa anunciou JCP mensal de R$0,02 por ação ordinária e preferencial (ITS-3 e TCA-4) com pagamento no dia 1º de julho. |
| 2026-05-09 | Virtual Asset | balance_sheet | 0.90 | Itaúsa está acima do valor patrimonial em 71%. |
| 2026-05-09 | Virtual Asset | valuation | 0.90 | Itaúsa valorizou 51,67% nos últimos 12 meses. |
| 2026-05-09 | Virtual Asset | valuation | 0.80 | Itaúsa é considerada uma empresa barata com P/L de 9,20 vezes e dividend yield de 9,14%. |
| 2026-05-09 | Virtual Asset | operational | 0.80 | Itaúsa é uma holding que detém a maior parte do Banco Itaú, conhecido por sua recorde de lucratividade. |
| 2026-04-22 | Virtual Asset | thesis_bear | 0.80 | A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa r… |
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a val… |
| 2026-04-22 | Virtual Asset | risk | 0.70 | A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimôn… |
| 2026-04-07 | Virtual Asset | valuation | 0.80 | O Bradesco BBI recomenda compra das ações ITSA4 com preço-alvo de R$15,40 até o final do ano de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 11.50 | [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] ITSA4 — peso 9.2% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ITSA4 — peso 5.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -11.75%
- **Drawdown 5y**: -11.75%
- **YTD**: +14.36%
- **YoY (1y)**: +28.71%
- **CAGR 3y**: +19.68%  |  **5y**: +11.00%  |  **10y**: +9.98%
- **Vol annual**: +24.03%
- **Sharpe 3y** (rf=4%): +0.71

###### Dividendos
- **DY 5y avg**: +7.68%
- **Div CAGR 5y**: -1.32%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$8.49B | R$13.67B | R$-1.35B |
| 2023-12-31 | R$7.38B | R$13.47B | R$-965.0M |
| 2024-12-31 | R$8.23B | R$14.78B | R$-742.0M |
| 2025-12-31 | R$8.25B | R$16.49B | R$-765.0M |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ITSA4 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-03', '2026-04-09', '2026-04-15', '2026-04-22', '2026-04-27', '2026-05-04']
series:
  - title: ITSA4
    data: [10.39, 10.78, 11.14, 10.97, 10.85, 10.62, 10.59, 10.69, 10.68, 10.74, 10.9, 10.34, 10.28, 10.2, 10.05, 10.14, 10.66, 10.8, 10.37, 10.72, 11.0, 10.81, 10.86, 10.92, 11.08, 11.16, 10.94, 10.81, 10.79, 11.01, 11.06, 11.31, 11.57, 11.91, 11.69, 11.58, 12.09, 12.66, 11.38, 11.37, 11.46, 11.68, 11.77, 11.96, 11.98, 13.36, 13.88, 13.58, 14.62, 14.59, 14.84, 14.14, 13.32, 13.33, 13.37, 13.5, 13.36, 13.92, 14.74, 15.0, 14.41, 14.1, 13.6]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "ITSA4 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.3991, 0.3287, 0.6785, 0.9089, 0.4924, 0.3009, 0.513, 0.5212, 0.6216, 1.7232, 0.1402]
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
    data: [10.09, 9.959459, 9.567567, 9.6081085, 9.6081085, 9.6081085, 9.527027, 9.486486, 9.22973, 9.405405, 9.189189, 9.22973, 9.162163, 8.986486]
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
    data: [17.66, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57, 17.57]
  - title: DY %
    data: [8.54, 8.33, 8.67, 8.63, 8.63, 8.63, 8.71, 8.74, 8.99, 8.82, 9.03, 8.99, 9.05, 9.41]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ITSA4_DOSSIE.md` (cemetery archive)_

#### 📑 ITSA4 — Itaúsa

> Generated **2026-04-26** by `ii dossier ITSA4`. Cross-links: [[ITSA4]] · [[ITSA4_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

ITSA4 negocia P/E 9.61, DY 8.63% e ROE consolidado 17.57% com streak de 20 anos — múltiplos compatíveis com critério Buffett/Graham. IC BUY (high confidence, 80% consensus); composite conviction 90 (top-3 da carteira). Tese central: holding discount play sobre ITUB4 — exposição barata ao banco #1 BR sem comprar ITUB4 a P/B 2.39, com payout estável + capital allocator disciplinado (Villela).

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.48  |  **BVPS**: 7.92
- **ROE**: 17.57%  |  **P/E**: 9.61  |  **P/B**: 1.80
- **DY**: 8.63%  |  **Streak div**: 20y  |  **Market cap**: R$ 159.43B
- **Last price**: BRL 14.22 (2026-04-26)  |  **YoY**: +37.2%

##### 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[ITSA4_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-24)**: ITSA4 é holding do Itaú Unibanco com desconto
persistente vs NAV (~15-20%). Capital allocator disciplinado (Rodolfo Villela),
payout policy estável. ROE consolidado ~17% via ITUB + participações (Alpargatas, Dexco, Aegea).
DY actual 8.91% alinhado com Selic de mercado. Margin of safety vem do desconto
holding + quality do Itaú como banco #1 BR.

**Key assumptions**:
1. Itaú mantém ROE ≥15% (core driver, ~85% do NAV)
2. Desconto holding não supera 25% (ponto de TRIM se chegar lá)
3. Payout ≥90% do lucro recorrente
4. Capital allocation continua disciplinada (Villela)

**Disconfirmation triggers**:
- Itaú ROE < 12% em 2 quarters consecutivos
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair
- Payout < 70% sem expansão clara

**Intent**:

→ Vault: [[ITSA4]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **90** |
| Thesis health | 100 |
| IC consensus | 92 |
| Variant perception | 60 |
| Data coverage | 100 |
| Paper track | 90 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 9.61** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 9.61** passa.
- **P/B = 1.80** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.80** — verificar consistência com ROE.
- **DY = 8.63%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **8.63%** passa.
- **ROE = 17.57%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **17.57%** compounder-grade.
- **Graham Number ≈ R$ 16.24** vs preço **R$ 14.22** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 20y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Concentração no Itaú (~85% NAV)** — qualquer choque ITUB4 propaga-se directamente. Trigger: ITUB4 ROE < 15% em 2 quarters (per disconfirmation trigger da thesis).
- 🟡 **Desconto holding alarga** — desconto >25% sem catalisador é sinal SELL na própria thesis. Trigger: monitor `(NAV - market_cap) / NAV > 0.25` 90d.
- 🟡 **Variant perception apenas 60** — consenso de mercado já reflectiu boa parte da tese; pouco edge informacional. Trigger: variant_perception score < 50.
- 🟡 **Risco de gestão** — saída de Villela mudaria capital allocation. Trigger: news/filings com mudança de management.
- 🟢 **Payout reduction** — payout < 70% sem expansão é trigger explícito. Trigger: `fundamentals.dy < 0.06` próximo trimestre.

##### 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold-to-add** — conviction 90, IC BUY, screen forte e tese DRIP genuína (streak 20y, DY 8.63%). Reinvestir dividendos via DRIP automático faz total sentido. Cash em BRL fica em BR (não converter); considerar acréscimo em pullbacks (DY > 9% ou desconto NAV > 20%) mas atenção à concentração bancária combinada com BBDC4 — ambos puxam exposição ao sector financeiro BR. Manter peso entre 8-12% da sleeve BR. Trim só se ITUB4 ROE colapsar abaixo de 12% sustentado.

##### 7. Tracking triggers (auto-monitoring)

- **ITUB4 ROE colapsa** — `SELECT roe FROM fundamentals WHERE ticker='ITUB4' ORDER BY period_end DESC LIMIT 2` < 0.15 em 2 quarters
- **Itaúsa ROE consolidado** — `fundamentals.roe < 0.13` no próximo trimestre
- **Desconto NAV alarga** — monitor `(NAV - market_cap) / NAV > 0.25` 90d (requer NAV calc cross-holdings)
- **DY trap** — `fundamentals.dy < 0.06` (sinal payout reduction)
- **P/B premium** — `fundamentals.pb > 2.0 AND fundamentals.roe < 0.15`
- **Thesis health degrada** — `SELECT thesis_health FROM conviction_scores WHERE ticker='ITSA4'` < 70

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
*Generated by `ii dossier ITSA4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | valuation | 0.90 | O Itaúsa apresentou lucratividade de R$ 12,3 bilhões no primeiro trimestre. |
| 2026-05-09 | Virtual Asset | dividend | 1.00 | Itaúsa anunciou JCP mensal de R$0,02 por ação ordinária e preferencial (ITS-3 e TCA-4) com pagamento no dia 1º de julho. |
| 2026-05-09 | Virtual Asset | balance_sheet | 0.90 | Itaúsa está acima do valor patrimonial em 71%. |
| 2026-05-09 | Virtual Asset | valuation | 0.90 | Itaúsa valorizou 51,67% nos últimos 12 meses. |
| 2026-05-09 | Virtual Asset | valuation | 0.80 | Itaúsa é considerada uma empresa barata com P/L de 9,20 vezes e dividend yield de 9,14%. |
| 2026-05-09 | Virtual Asset | operational | 0.80 | Itaúsa é uma holding que detém a maior parte do Banco Itaú, conhecido por sua recorde de lucratividade. |
| 2026-04-22 | Virtual Asset | thesis_bear | 0.80 | A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa r… |
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a val… |
| 2026-04-22 | Virtual Asset | risk | 0.70 | A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimôn… |
| 2026-04-07 | Virtual Asset | valuation | 0.80 | O Bradesco BBI recomenda compra das ações ITSA4 com preço-alvo de R$15,40 até o final do ano de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 11.50 | [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] ITSA4 — peso 9.2% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ITSA4 — peso 5.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ITSA4_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — ITSA4

**Committee verdict**: **BUY** (high confidence, 80% consensus)  
**Votes**: BUY=4 | HOLD=1 | AVOID=0  
**Avg conviction majority**: 8.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- holding de qualidade com Itaú
- ROE alto e estável
- desconto vs NAV

**Key risk**: Itaú ROE caindo abaixo de 15% por fatores macro ou operacionais

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Desconto persistente vs NAV
- ROE consolidado ~17%
- Payout estável e alto

**Key risk**: Itaú ROE cair abaixo de 12% por dois trimestres seguidos

###### 🟡 Nassim Taleb — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- Desconto persistente vs NAV
- ROE consolidado estável
- Payout robusto

**Key risk**: Itaú ROE cair abaixo de 12% em dois trimestres consecutivos

###### 🟢 Seth Klarman — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Desconto persistente vs NAV
- ROE consolidado forte (~17%)
- Payout policy estável

**Key risk**: Itaú ROE caindo abaixo de 12% em 2 trimestres consecutivos

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Desconto persistente vs NAV
- ROE consolidado ~17%
- Payout estável e disciplinada gestão

**Key risk**: Itaú ROE cair abaixo de 12% por dois trimestres consecutivos

##### 📊 Context provided

```
TICKER: BR:ITSA4

FUNDAMENTALS LATEST:
  pe: 9.121621
  pb: 1.7051914
  dy: 9.27%
  roe: 17.57%
  net_debt_ebitda: 4.034951540606407
  intangible_pct_assets: 0.8%   (goodwill $0.4B + intangibles $0.4B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=2.1 ebit=4.7 ni=4.2 em%=219.5 debt=10 fcf=2.7
  2025-06-30: rev=2.1 ebit=4.4 ni=4.1 em%=206.8 debt=11 fcf=0.1
  2025-03-31: rev=1.9 ebit=4.4 ni=4.0 em%=231.6 debt=11 fcf=7.3
  2024-12-31: rev=2.1 ebit=4.1 ni=3.7 em%=198.1 debt=11 fcf=-0.1
  2024-09-30: rev=2.2 ebit=4.3 ni=3.9 em%=192.6 debt=13 fcf=1.5
  2024-06-30: rev=2.0 ebit=4.2 ni=3.8 em%=212.0 debt=12 fcf=0.1

THESIS HEALTH: score=100/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: ITSA4 é holding do Itaú Unibanco com desconto
persistente vs NAV (~15-20%). Capital allocator disciplinado (Rodolfo Villela),
payout policy estável. ROE consolidado ~17% via ITUB + participações (Alpargatas, Dexco, Aegea).
DY actual 8.91% alinhado com Selic de mercado. Margin of safety vem do desconto
holding + quality do Itaú como banco #1 BR.

**Key assumptions**:
1. Itaú mantém ROE ≥15% (core driver, ~85% do NAV)
2. Desconto holding não supera 25% (ponto de TRIM se chegar lá)
3. Payout ≥90% do lucro recorrente
4. Capital allocation continua disciplinada (Villela)

**Disconfirmation triggers**:
- Itaú ROE < 12% em 2 quarters consecutivos
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair
- Payout < 70% sem expansão clara

**Intent**:

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Nubank: Investing in the Future of Brazil - FinTech Magazine [Wed, 29 Ap]
    # Nubank: Investing in the Future of Brazil. The largest digital bank in LATAM announces that it is investing R$45bn (US$8.2bn) in Brazil for 2026, following a period of growth by the bank. Nubank pla
  - Brazil's Petrobras raises natural gas prices by 19% after oil shock - Reuters [Sat, 02 Ma]
    REUTERS/Amanda Perobelli/File Photo Purchase Licens
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | valuation | 0.90 | O Itaúsa apresentou lucratividade de R$ 12,3 bilhões no primeiro trimestre. |
| 2026-05-09 | Virtual Asset | dividend | 1.00 | Itaúsa anunciou JCP mensal de R$0,02 por ação ordinária e preferencial (ITS-3 e TCA-4) com pagamento no dia 1º de julho. |
| 2026-05-09 | Virtual Asset | balance_sheet | 0.90 | Itaúsa está acima do valor patrimonial em 71%. |
| 2026-05-09 | Virtual Asset | valuation | 0.90 | Itaúsa valorizou 51,67% nos últimos 12 meses. |
| 2026-05-09 | Virtual Asset | valuation | 0.80 | Itaúsa é considerada uma empresa barata com P/L de 9,20 vezes e dividend yield de 9,14%. |
| 2026-05-09 | Virtual Asset | operational | 0.80 | Itaúsa é uma holding que detém a maior parte do Banco Itaú, conhecido por sua recorde de lucratividade. |
| 2026-04-22 | Virtual Asset | thesis_bear | 0.80 | A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa r… |
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a val… |
| 2026-04-22 | Virtual Asset | risk | 0.70 | A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimôn… |
| 2026-04-07 | Virtual Asset | valuation | 0.80 | O Bradesco BBI recomenda compra das ações ITSA4 com preço-alvo de R$15,40 até o final do ano de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 11.50 | [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] ITSA4 — peso 9.2% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ITSA4 — peso 5.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ITSA4_RI.md` (cemetery archive)_

#### ITSA4 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `fco`: **-209.0%**
- ⬆️ **QOQ** `fcf_proxy`: **+4639.3%**
- ⬆️ **QOQ** `ebit_margin`: **+12.7pp**
- ⬆️ **QOQ** `net_margin`: **+5.2pp**
- ⬇️ **YOY** `debt_total`: **-26.5%**
- ⬇️ **YOY** `fco`: **-154.4%**
- ⬆️ **YOY** `fcf_proxy`: **+82.9%**
- ⬆️ **YOY** `ebit_margin`: **+26.9pp**
- ⬆️ **YOY** `net_margin`: **+25.1pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.1 mi | R$ 2.1 mi | +0.3% |
| `ebit` | R$ 4.7 mi | R$ 4.4 mi | +6.5% |
| `net_income` | R$ 4.2 mi | R$ 4.1 mi | +3.0% |
| `debt_total` | R$ 9.7 mi | R$ 11.4 mi | -15.3% |
| `fco` | R$ -0.2 mi | R$ 0.2 mi | -209.0% |
| `fcf_proxy` | R$ 2.7 mi | R$ 0.1 mi | +4639.3% |
| `gross_margin` | 23.1% | 22.9% | +0.2pp |
| `ebit_margin` | 219.5% | 206.8% | +12.7pp |
| `net_margin` | 198.2% | 193.0% | +5.2pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.1 mi | R$ 2.2 mi | -5.0% |
| `ebit` | R$ 4.7 mi | R$ 4.3 mi | +8.3% |
| `net_income` | R$ 4.2 mi | R$ 3.9 mi | +8.8% |
| `debt_total` | R$ 9.7 mi | R$ 13.2 mi | -26.5% |
| `fco` | R$ -0.2 mi | R$ 0.4 mi | -154.4% |
| `fcf_proxy` | R$ 2.7 mi | R$ 1.5 mi | +82.9% |
| `gross_margin` | 23.1% | 29.8% | -6.7pp |
| `ebit_margin` | 219.5% | 192.6% | +26.9pp |
| `net_margin` | 198.2% | 173.1% | +25.1pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 2.1 | 219.5% | 198.2% | 10 | -0 |
| 2025-06-30 | ITR | 2.1 | 206.8% | 193.0% | 11 | 0 |
| 2025-03-31 | ITR | 1.9 | 231.6% | 207.8% | 11 | -0 |
| 2024-12-31 | DFP-ITR | 2.1 | 198.1% | 181.0% | 11 | -0 |
| 2024-09-30 | ITR | 2.2 | 192.6% | 173.1% | 13 | 0 |
| 2024-06-30 | ITR | 2.0 | 212.0% | 191.4% | 12 | 0 |
| 2024-03-31 | ITR | 1.9 | 194.0% | 178.5% | 12 | -0 |
| 2023-12-31 | DFP-ITR | 1.9 | 155.2% | 159.5% | 11 | 0 |
| 2023-09-30 | ITR | 1.8 | 204.7% | 242.1% | 11 | -0 |
| 2023-06-30 | ITR | 2.0 | 211.9% | 188.9% | 13 | 0 |
| 2023-03-31 | ITR | 1.7 | 194.1% | 169.2% | 12 | -0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [1.7, 2.0, 1.8, 1.9, 1.9, 2.0, 2.2, 2.1, 1.9, 2.1, 2.1]
  - title: EBIT margin %
    data: [194.1, 211.9, 204.7, 155.2, 194.0, 212.0, 192.6, 198.1, 231.6, 206.8, 219.5]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ITSA4_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — ITSA4

**Our stance**: bullish  
**Analyst consensus** (4 insights, last 90d): bullish (75% bull)  
**Weighted consensus** (source win-rate weighted): bullish (75% bull)  
**Variance type**: `low_consensus_long` (magnitude 1/5)  
**Interpretation**: consensus pick — no edge

##### 📰 Recent analyst insights

- [neutral] *suno (w=0.50)* [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5
- [bull] *xp (w=0.50)* [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials
- [bull] *xp (w=0.50)* [BTG Equity Brazil] ITSA4 — peso 9.2%
- [bull] *xp (w=0.50)* [BTG Value] ITSA4 — peso 5.6%

##### ⚖️ Source weights (predictions win-rate)

- 📊 `suno` → 0.50 *(no track record yet)*
- 📊 `xp` → 0.50 *(no track record yet)*

##### 📜 Our thesis

**Core thesis (2026-04-24)**: ITSA4 é holding do Itaú Unibanco com desconto
persistente vs NAV (~15-20%). Capital allocator disciplinado (Rodolfo Villela),
payout policy estável. ROE consolidado ~17% via ITUB + participações (Alpargatas, Dexco, Aegea).
DY actual 8.91% alinhado com Selic de mercado. Margin of safety vem do desconto
holding + quality do Itaú como banco #1 BR.

**Key assumptions**:
1. Itaú mantém ROE ≥15% (core driver, ~85% do NAV)
2. Desconto holding não supera 25% (ponto de TRIM se chegar lá)
3. Payout ≥90% do lucro recorrente
4. Capital allocation continua disciplinada (Villela)

**Disconfirmation triggers**:
- Itaú ROE < 12% em 2 quarters consecutivos
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair
- Payout < 70% sem expansão clara

**Intent**:

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | valuation | 0.90 | O Itaúsa apresentou lucratividade de R$ 12,3 bilhões no primeiro trimestre. |
| 2026-05-09 | Virtual Asset | dividend | 1.00 | Itaúsa anunciou JCP mensal de R$0,02 por ação ordinária e preferencial (ITS-3 e TCA-4) com pagamento no dia 1º de julho. |
| 2026-05-09 | Virtual Asset | balance_sheet | 0.90 | Itaúsa está acima do valor patrimonial em 71%. |
| 2026-05-09 | Virtual Asset | valuation | 0.90 | Itaúsa valorizou 51,67% nos últimos 12 meses. |
| 2026-05-09 | Virtual Asset | valuation | 0.80 | Itaúsa é considerada uma empresa barata com P/L de 9,20 vezes e dividend yield de 9,14%. |
| 2026-05-09 | Virtual Asset | operational | 0.80 | Itaúsa é uma holding que detém a maior parte do Banco Itaú, conhecido por sua recorde de lucratividade. |
| 2026-04-22 | Virtual Asset | thesis_bear | 0.80 | A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa r… |
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a val… |
| 2026-04-22 | Virtual Asset | risk | 0.70 | A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimôn… |
| 2026-04-07 | Virtual Asset | valuation | 0.80 | O Bradesco BBI recomenda compra das ações ITSA4 com preço-alvo de R$15,40 até o final do ano de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 11.50 | [Suno Valor] ITSA4 — peso 5.0%, rating Aguardar, PT R$11.5 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ITSA4 — peso 9.6%, setor Financials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] ITSA4 — peso 9.2% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ITSA4 — peso 5.6% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\ITSA4.md` (cemetery archive)_

#### 🎯 Thesis: [[ITSA4]] — Itaúsa

> Holding BR com exposure maioritária ao [[ITUB4]]. Tese DRIP core: canal preferencial para expor-se ao Itaú com **desconto estrutural** + diversificação adicional via participadas não-bancárias.

##### Intent
**DRIP core** — income compounder BR. Não é growth play (holding desconto tende a manter-se estrutural).

##### Business snapshot
Holding de participações com core position no **Itaú Unibanco** (~37% do NAV) + diversificação:
- [[ITUB4]] (banco) — motor principal
- Alpargatas (calçado, Havaianas)
- Dexco (madeira + metais sanitários)
- Aegea (saneamento, não listada)
- CCR (infraestrutura — recente)
- Copagaz (distribuição gás)
- XP (fintech)

##### Por que detemos

1. **Desconto holding** — ITSA4 historicamente transacciona a **10-25% de desconto** sobre NAV. Comprar ITSA4 vs ITUB4 = compra Itaú com desconto.
2. **Dividendos isentos IR PF** ([[BR_dividend_isencao]]) — combina com payout high do Itaú.
3. **Diversificação barata** — exposure a 7+ negócios sem gestão activa de cada posição.
4. **JCP** — Itaúsa paga mensalmente/trimestralmente JCP (dedutível empresa, 15% retido definitivo no PF).

##### Moat

- **Não é a empresa** que tem moat — é o Itaú ([[BR_Banks]] big-5 moat) + portfolio diversificado.
- **Governance Moreira Salles** estável há 50+ anos.
- **Track record alocação capital** (venda Duratex gás, M&A seletivo).

##### Current state (2026-04)

- Ciclo [[Selic]] em descida após peak 2024 → bancos em janela de revaluation.
- ITUB4 reporting ROE ~22%, cobertura provisões robusta.
- Desconto vs NAV próximo de **15-18%** (trackable via site RI Itaúsa + NAV).
- Alpargatas em turnaround (Havaianas exit US mercado competitivo).
- Dexco cyclical (real estate BR forte em 2025).

##### Invalidation triggers

- [ ] ITUB4 corte dividendo estrutural (unlikely salvo regulatório)
- [ ] Desconto NAV > 30% por > 6 meses (sinal de governance issue)
- [ ] Itaúsa venda de participação Itaú (quebra thesis)
- [ ] Payout total (dividendos + JCP) cai > 40% 2 anos consecutivos
- [ ] Selic ciclo reverte violentamente (thesis pausa, não inval total)

##### Sizing + DRIP

- Posição actual: 2472 shares
- Intent: **não trimmar**, reinvestir mensal JCP em mais ITSA4 ou BBSE3 / bancos
- Target: manter ~10-12% do sleeve BR equity


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -6.04%
- **Drawdown 5y**: -6.04%
- **YTD**: +21.75%
- **YoY (1y)**: +39.68%
- **CAGR 3y**: +23.29%  |  **5y**: +12.44%  |  **10y**: +10.67%
- **Vol annual**: +23.75%
- **Sharpe 3y** (rf=4%): +0.88

###### Dividendos
- **DY 5y avg**: +7.68%
- **Div CAGR 5y**: -1.32%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[BBDC4]] — comparar peer (Bradesco vs Itaú via Itaúsa)
- [[BR_Banks]] — framework bancário
- [[BR_dividend_isencao]] — tax edge
- [[wiki/macro/BR_vs_US_equity_culture]] — por que BR dividend stocks valem 20-30% mais que equivalentes US

##### Memory refs

- `user_investment_intents.md` — Itaúsa classificada como DRIP core

## ⚙️ Refresh commands

```bash
ii panorama ITSA4 --write
ii deepdive ITSA4 --save-obsidian
ii verdict ITSA4 --narrate --write
ii fv ITSA4
python -m analytics.fair_value_forward --ticker ITSA4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
