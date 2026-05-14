---
type: ticker_hub
ticker: VALE3
market: br
sector: Mining
currency: BRL
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 18
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# VALE3 — Vale

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Mining` · `market: BR` · `currency: BRL` · `bucket: holdings` · `18 sources merged`

## 🎯 Hoje

- **Posição**: 501.0 @ entry 61.84
- **Verdict (DB)**: `HOLD` (score 6.13, 2026-05-13)
- **Último deepdive**: `VALE3_deepdive_20260509_1611.json` (2026-05-09 16:11)
- **Fundamentals** (2026-05-13): P/E 26.02 · P/B 1.95 · DY 6.5% · ROE 6.8% · ND/EBITDA 1.08 · Dividend streak 18

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\VALE3.md` (cemetery archive)_

#### VALE3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Mining
- **RI URLs scraped** (1):
  - https://vale.com/pt/investidores
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=501.0 · entry=61.84 · date=2026-05-07

- Total events na DB: **42**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=83.44999694824219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.068390004 · DY=0.06563401078848538 · P/E=25.598158
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Vale esclarece sobre notí |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Desempenho da Vale no 1T26 |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Relatório de produção e v |

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

#### 2026-05-09 · Deepdive (V10 4-layer)
_generated 2026-05-09 16:11 · source: `reports/deepdive/VALE3_deepdive_20260509_1611.json`_

> Sector: ? · Country: ? · Price: ? 

**Quality scores**

| Score | Valor | Zona |
|---|---|---|
| Piotroski | 5/9 | - |
| Altman Z | 4.82333528110067 | safe |
| Beneish M | - | - |
| Moat | 4.5/10 | WEAK |


**Fundamentals**: P/E - · P/B - · EV/EBITDA - · DY - · ROE -

**Delta vs análise anterior**

```
Delta Report — VALE3 | hoje vs run anterior (2026-05-08)
```

**Strategist dossier**

# 1. Executive Summary
- **Rating:** EVITAR
- **Preço justo estimado e upside/downside %:** Não é possível calcular devido à falta de dados quantitativos.
- **Risk Score:** 8 (Risco moderadamente alto)
- **Alerta vermelho:** Sem análise Beneish, mas o Moat Score fraco e a necessidade de um Bear Case mais agressivo indicam riscos significativos.

# 2. O Negócio
O negócio em questão não foi especificado, impossibilitando uma avaliação detalhada do modelo de receita e fontes de caixa. No entanto, com base nos dados disponíveis:
- **Network Effect:** Não aplicável (não informado)
- **Switching Costs:** 4/5 (baseado na pontuação Moat)
- **Intangibles:** 6/10 (baseado na pontuação Moat)
- **Cost Advantages:** 2/5 (baseado na pontuação Moat)

# 3. Decomposição DuPont
Sem dados específicos sobre margem, giro e alavancagem, não é possível realizar uma análise detalhada da decomposição DuPont.

# 4. Valuation Multinível
- **Graham Number:** Não aplicável devido à falta de dados.
- **DCF com 3 cenários:**
    - Bear Case: Não calculado (falta de dados).
    - Base Case: Não calculado (falta de dados).
    - Bull Case: Não calculado (falta de dados).
- **EV/EBITDA vs mediana setor:** Não comparável sem dados.

# 5. Bear Case
Dada a pontuação Piotroski de 5, o Bear Case deve ser mais agressivo:
1. **Risco Operacional** (Probabilidade: Alta) - A empresa pode enfrentar desafios operacionais que afetem negativamente sua rentabilidade.
2. **Condições Econômicas Adversas** (Probabilidade: Média) - Uma recessão ou condições econômicas adversas podem impactar negativamente a demanda e os preços dos produtos da empresa.
3. **Riscos de Mercado** (Probabilidade: Baixa) - Flutuações significativas no mercado podem afetar o preço das ações.

**Cenário de -40%:** A empresa enfrentaria dificuldades financeiras, potencialmente resultando em cortes de custos e redução de investimentos. Se as condições persistirem, pode haver risco de falência ou reestruturação significativa.

# 6. Bull Case
- **Catalisadores específicos com prazo:** Não identificados devido à falta de dados.
- **O que precisa acontecer para o preço dobrar em 3 anos?** A empresa precisaria apresentar crescimento excepcional, melhoria na eficiência operacional e condições macroeconômicas favoráveis.

# 7. Classificação Lynch
- **Classificação:** Não aplicável devido à falta de dados específicos sobre o negócio.
- **Argumentos objetivos:**
    - A empresa não apresenta características claras para classificação.
    - Falta de dados impede uma análise detalhada.

# 8. Veredicto Final
- **Decisão com 3 critérios mensuráveis:** 
    - Piotroski F-Score: 5/9 (razoável, mas não excelente).
    - Moat Score: 4.5/10 (fraco).
    - Falta de dados quantitativos específicos.
- **Position sizing:** Evitar
- **Justificativa final:** A falta de dados quantitativos e a pontuação fraca do moat, combinada com um Piotroski F-Score apenas razoável, indicam riscos significativos sem uma justificativa clara para recomendar uma posição.

#### 2026-04-30 · Council review · Aderbaldo Cíclico
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Aderbaldo Cíclico\reviews\VALE3_2026-04-30.md` (cemetery archive)_

#### Aderbaldo Cíclico sobre [[VALE3_STORY|VALE3]]

**Função no debate**: Commodities BR Specialist (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _VALE3 mantém posição de longo prazo com geração de caixa sólida_

A Vale S.A. sustenta uma posição financeira robusta, com payout ratio sustentável e histórico de dividendos consistente. A relação P/E elevada é compensada por um ROE baixo mas gerenciado eficientemente.

**Métricas que invoquei**:
- P/E=24.60
- ROE=5.9%
- ND/EBITDA=0.97

**Preocupações**:
- Payout ratio elevado pode comprometer investimentos futuros
- Dependência do preço do minério de ferro

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor.
- Valentina Prudente

**Desafiei**:
- Seu múltiplo P/E está acima da média do setor (24.60 vs mediana de 8.00x).
- A relação entre a geração de caixa sólida e o payout ratio sustentável compensa o múltiplo elevado.
- Pedro Alocação

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[VALE3_STORY|📖 Storytelling completo (8 actos)]]
- [[VALE3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Aderbaldo Cíclico|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\VALE3_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[VALE3_STORY|VALE3]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Vale mantém posição sólida com geração de caixa robusta_

A Vale S.A. apresenta uma consistência em dividendos e uma gestão eficiente dos ativos, apesar do múltiplo P/E ligeiramente elevado.

**Métricas que invoquei**:
- P/B=1.88
- ROE=5.9%
- ND/EBITDA=0.97

**Preocupações**:
- múltiplo P/E acima do setor
- volatilidade de preços do minério de ferro

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor. - Valentina Prudente

**Desafiei**:
- Payout ratio elevado pode comprometer investimentos futuros | Dependência do preço do minério de ferro - Aderbaldo Cíclico; Essa dependência é uma preocupação, mas a Vale tem demonstrado resiliência e capacidade de gerir seus ativos mesmo em condições desafiadoras.

**Evidência nova**: A Vale continua a expandir suas reservas minerais tanto no Brasil quanto no Canadá, o que pode fortalecer sua posição futura.

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[VALE3_STORY|📖 Storytelling completo (8 actos)]]
- [[VALE3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\VALE3_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[VALE3_STORY|VALE3]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _VALE3 mantém posição de HOLD com risco elevado_

A Vale apresenta um histórico sólido em dividendos e geração de caixa, mas seu múltiplo P/E está acima da média do setor (24.60 vs mediana de 8.00x).

**Métricas que invoquei**:
- P/E=24.60
- DY=6.7%
- ROE=5.9%

**Preocupações**:
- P/E elevado em relação ao setor
- vulnerabilidade a flutuações de preços do minério de ferro

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Vale apresenta uma consistência em dividendos e uma gestão eficiente dos ativos, apesar do múltiplo P/E ligeiramente elevado. - Mariana Macro

**Desafiei**:
- A relação P/E elevada é compensada por um ROE baixo mas gerenciado eficientemente. - Aderbaldo Cíclico | O ROE de 5,9% é significativamente abaixo da média do setor (18%) e pode indicar que a empresa está enfrentando desafios em sua geração de lucros por unidade de capital empregado.

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[VALE3_STORY|📖 Storytelling completo (8 actos)]]
- [[VALE3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\VALE3_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[VALE3_STORY|VALE3]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Vale mantém posição financeira sólida e geração de caixa consistente_

A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor.

**Métricas que invoquei**:
- Piotroski F-Score: 5/9
- Altman Z-Score: 5.05 (safe)
- Beneish M-Score: -2.81 (clean)

**Preocupações**:
- P/E ligeiramente elevado em comparação com o setor
- Dependência do preço do minério de ferro

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Vale S.A. sustenta uma posição financeira robusta, com payout ratio sustentável e histórico de dividendos consistente. - Aderbaldo Cíclico

**Desafiei**:
- múltiplo P/E acima do setor | volatilidade de preços do minério de ferro - Mariana Macro; O múltiplo P/E elevado é um reflexo da expectativa de crescimento futuro e não necessariamente indica uma posição financeira fraca, especialmente com a geração de caixa sólida que a Vale tem demonstrado consistentemente.

##### Quem mais estava na sala

- [[Aderbaldo Cíclico]] (Commodities BR Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[VALE3_STORY|📖 Storytelling completo (8 actos)]]
- [[VALE3_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Filing 2026-04-30
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3_FILING_2026-04-30.md` (cemetery archive)_

#### Filing dossier — [[VALE3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513231&numSequencia=1037937&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 80.07

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `33.24` |
| HOLD entre | `33.24` — `57.31` (consensus) |
| TRIM entre | `57.31` — `65.90` |
| **SELL acima de** | `65.90` |

_Método: `graham_number`. Consensus fair = R$57.31. Our fair (mais conservador) = R$33.24._

##### 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.068390004` | `0.1349` | +49.3% |
| EPS | `3.26` | `6.8643` | +52.5% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 56.7B (+13.8% QoQ, +7.0% YoY)
- EBIT 16.1B (+46.4% QoQ)
- Margem EBIT 28.4% vs 22.1% prior
- Lucro líquido 14.7B (+20.4% QoQ, +10.6% YoY)

**BS / cash**
- Equity 224.7B (+1.7% QoQ)
- Dívida total 98.6B (+1.3% QoQ)
- FCF proxy 6.9B (+959.2% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `filing:cvm:comunicado:2026-04-30` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:46+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll2_macro_overlay` |
| 2026-05-08T16:39:50+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll_outlier_median` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | disputed | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:27:07+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | disputed | `phase_ll_3way_outlier` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | single_source | `phase_ll_dualclass_v2` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-20 · Other
_source: `videos\2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa.md`_

#### 🎬 PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CHEGANDO? VALE3 SUPERA EXPECTATIVA! B3SA3 +46% e EGIE3 2,7BI

**Canal**: Virtual Asset | **Publicado**: 2026-04-20 | **Duração**: 20min

**URL**: [https://www.youtube.com/watch?v=Wf4pWQXguPg](https://www.youtube.com/watch?v=Wf4pWQXguPg)

##### Tickers mencionados

[[B3SA3]] · [[CPLE3]] · [[EGIE3]] · [[PETR4]] · [[PRIO3]] · [[TAEE11]] · [[VALE3]]

##### Insights extraídos

###### [[VALE3]]
- [0.90 operational] A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma geração de caixa mais robusta.
- [0.70 risk] A volatilidade das commodities e a execução de projetos são fatores de atenção para os investidores na Vale.

###### [[B3SA3]]
- [0.80 operational] A B3 registrou um volume financeiro negociado de R$ 37 bilhões no primeiro trimestre de 2026, superando expectativas.
- [0.80 valuation] A B3 está negociando com múltiplos esticados, entre 16 e 17 vezes o lucro, mas os analistas reconhecem que a empresa tem fundamentos positivos.

###### [[CPLE3]]
- [0.80 dividend] A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária.
- [0.70 valuation] A Copel está negociando com múltiplos elevados, refletindo a expectativa do mercado para o futuro.

###### [[EGIE3]]
- [0.80 balance_sheet] A Engie Brasil reduziu seu saldo contábil de obrigações do balanço, passando de R$4,44 bilhões para R$2,36 bilhões.
- [0.70 operational] A Engie Brasil aprovou a repactuação de R$2,3 bilhões em concessões de suas usinas.
- [0.70 valuation] As ações da Engie Brasil (EGIE3) estão valorizando significativamente, com um PVP de 242% acima do valor patrimonial.

###### [[PETR4]]
- [0.80 guidance] A alta do barril de petróleo está impulsionando a Petrobras e outras petroleiras da bolsa.
- [0.80 valuation] A Petrobras tem um dividendo yield estimado de 6,5% para 2026 e é vista como bem posicionada no mercado.
- [0.70 valuation] A Petrobras está sendo valorizada no mercado devido à alta do barril de petróleo e sua capacidade de geração de caixa.

###### [[PRIO3]]
- [0.70 valuation] O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026.

###### [[TAEE11]]
- [0.70 valuation] TAEE11 está sendo negociada com um dividend yield de 6,20%, que é considerado enorme.

##### Temas macro

- **oil_cycle** bullish _(conf 0.90)_ — A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando a rondar os 100 dólares.
- **oil_cycle** neutral _(conf 0.80)_ — Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos anos.


### 2025

#### 2025-07-27 · Other
_source: `videos\2025-07-27_suno-noticias_vale-a-pena-investir-em-vale-vale3-apos-resultados-operacionais.md`_

#### 🎬 Vale a pena INVESTIR EM VALE (VALE3) após RESULTADOS operacionais?

**Canal**: Suno Notícias | **Publicado**: 2025-07-27 | **Duração**: 5min

**URL**: [https://www.youtube.com/watch?v=ZHRmPOdCBqo](https://www.youtube.com/watch?v=ZHRmPOdCBqo)

##### Tickers mencionados

[[VALE3]]

##### Insights extraídos

###### [[VALE3]]
- [0.80 operational] A Vale registrou queda nas vendas de minério de ferro no segundo trimestre de 2025.
- [0.80 operational] A Vale teve um crescimento de 3,7% na produção de minério de ferro no segundo trimestre de 2025.
- [0.70 valuation] O BTG Pactual manteve uma recomendação neutra para as ações da Vale com preço-alvo de R$ 65,00.
- [0.70 valuation] O JP Morgan manteve a recomendação de compra para as ações da Vale com preço-alvo de R$ 86,00.


### (undated)

#### — · Dossier
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3.md` (cemetery archive)_

#### [[VALE3]] — Dossier Deepdive (2026-05-09)

> Sector: ? · Country: ? · Price: ? 

##### Quality Scores

| Score | Valor | Zona |
|---|---|---|
| Piotroski | 5/9 | - |
| Altman Z | 4.82333528110067 | safe |
| Beneish M | - | - |
| Moat | 4.5/10 | WEAK |


##### Delta Report

```
Delta Report — VALE3 | hoje vs run anterior (2026-05-08)
```

##### Strategist Dossier

#### 1. Executive Summary
- **Rating:** EVITAR
- **Preço justo estimado e upside/downside %:** Não é possível calcular devido à falta de dados quantitativos.
- **Risk Score:** 8 (Risco moderadamente alto)
- **Alerta vermelho:** Sem análise Beneish, mas o Moat Score fraco e a necessidade de um Bear Case mais agressivo indicam riscos significativos.

#### 2. O Negócio
O negócio em questão não foi especificado, impossibilitando uma avaliação detalhada do modelo de receita e fontes de caixa. No entanto, com base nos dados disponíveis:
- **Network Effect:** Não aplicável (não informado)
- **Switching Costs:** 4/5 (baseado na pontuação Moat)
- **Intangibles:** 6/10 (baseado na pontuação Moat)
- **Cost Advantages:** 2/5 (baseado na pontuação Moat)

#### 3. Decomposição DuPont
Sem dados específicos sobre margem, giro e alavancagem, não é possível realizar uma análise detalhada da decomposição DuPont.

#### 4. Valuation Multinível
- **Graham Number:** Não aplicável devido à falta de dados.
- **DCF com 3 cenários:**
    - Bear Case: Não calculado (falta de dados).
    - Base Case: Não calculado (falta de dados).
    - Bull Case: Não calculado (falta de dados).
- **EV/EBITDA vs mediana setor:** Não comparável sem dados.

#### 5. Bear Case
Dada a pontuação Piotroski de 5, o Bear Case deve ser mais agressivo:
1. **Risco Operacional** (Probabilidade: Alta) - A empresa pode enfrentar desafios operacionais que afetem negativamente sua rentabilidade.
2. **Condições Econômicas Adversas** (Probabilidade: Média) - Uma recessão ou condições econômicas adversas podem impactar negativamente a demanda e os preços dos produtos da empresa.
3. **Riscos de Mercado** (Probabilidade: Baixa) - Flutuações significativas no mercado podem afetar o preço das ações.

**Cenário de -40%:** A empresa enfrentaria dificuldades financeiras, potencialmente resultando em cortes de custos e redução de investimentos. Se as condições persistirem, pode haver risco de falência ou reestruturação significativa.

#### 6. Bull Case
- **Catalisadores específicos com prazo:** Não identificados devido à falta de dados.
- **O que precisa acontecer para o preço dobrar em 3 anos?** A empresa precisaria apresentar crescimento excepcional, melhoria na eficiência operacional e condições macroeconômicas favoráveis.

#### 7. Classificação Lynch
- **Classificação:** Não aplicável devido à falta de dados específicos sobre o negócio.
- **Argumentos objetivos:**
    - A empresa não apresenta características claras para classificação.
    - Falta de dados impede uma análise detalhada.

#### 8. Veredicto Final
- **Decisão com 3 critérios mensuráveis:** 
    - Piotroski F-Score: 5/9 (razoável, mas não excelente).
    - Moat Score: 4.5/10 (fraco).
    - Falta de dados quantitativos específicos.
- **Position sizing:** Evitar
- **Justificativa final:** A falta de dados quantitativos e a pontuação fraca do moat, combinada com um Piotroski F-Score apenas razoável, indicam riscos significativos sem uma justificativa clara para recomendar uma posição.

---
*Generated by `ii deepdive VALE3` em 2026-05-09T16:11:31.*

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[VALE3_STORY|VALE3]] (VALE3)

**Final stance**: 🟢 **BUY**  
**Confidence**: `medium`  
**Modo (auto)**: C (BR)  |  **Sector**: Mining  |  **Held**: sim  
**Elapsed**: 63.9s  |  **Failures**: 0

##### Quem esteve na sala

- [[Aderbaldo Cíclico]] — _Commodities BR Specialist_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor.
- Valentina Prudente
- Mariana Macro

**Dissenso (preservado)**:
- X disse A, Y disse B

**Sizing**: Pedro Alocação recomenda uma alocação moderada devido ao múltiplo P/E elevado e riscos associados à volatilidade do preço do minério de ferro.

##### Round 1 — Opening Statements (blind)

###### [[Aderbaldo Cíclico]] — 🟢 **BUY**
_Commodities BR Specialist_

**Headline**: _VALE3 mantém posição de longo prazo com geração de caixa sólida_

A Vale S.A. sustenta uma posição financeira robusta, com payout ratio sustentável e histórico de dividendos consistente. A relação P/E elevada é compensada por um ROE baixo mas gerenciado eficientemente.

**Métricas**:
- P/E=24.60
- ROE=5.9%
- ND/EBITDA=0.97

**Preocupações**:
- Payout ratio elevado pode comprometer investimentos futuros
- Dependência do preço do minério de ferro

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _Vale mantém posição sólida com geração de caixa robusta_

A Vale S.A. apresenta uma consistência em dividendos e uma gestão eficiente dos ativos, apesar do múltiplo P/E ligeiramente elevado.

**Métricas**:
- P/B=1.88
- ROE=5.9%
- ND/EBITDA=0.97

**Preocupações**:
- múltiplo P/E acima do setor
- volatilidade de preços do minério de ferro

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Vale mantém posição financeira sólida e geração de caixa consistente_

A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor.

**Métricas**:
- Piotroski F-Score: 5/9
- Altman Z-Score: 5.05 (safe)
- Beneish M-Score: -2.81 (clean)

**Preocupações**:
- P/E ligeiramente elevado em comparação com o setor
- Dependência do preço do minério de ferro

###### [[Pedro Alocação]] — 🟡 **HOLD**
_Capital Allocator_

**Headline**: _VALE3 mantém posição de HOLD com risco elevado_

A Vale apresenta um histórico sólido em dividendos e geração de caixa, mas seu múltiplo P/E está acima da média do setor (24.60 vs mediana de 8.00x).

**Métricas**:
- P/E=24.60
- DY=6.7%
- ROE=5.9%

**Preocupações**:
- P/E elevado em relação ao setor
- vulnerabilidade a flutuações de preços do minério de ferro

##### Round 2 — Respostas (peers visíveis)

###### [[Aderbaldo Cíclico]] — 🟢 **BUY**
_Commodities BR Specialist_

**Concordou com**:
- A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor.
- Valentina Prudente

**Desafiou**:
- Seu múltiplo P/E está acima da média do setor (24.60 vs mediana de 8.00x).
- A relação entre a geração de caixa sólida e o payout ratio sustentável compensa o múltiplo elevado.
- Pedro Alocação

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- A Vale apresenta uma geração de caixa robusta e um histórico de dividendos estáveis, com múltiplos P/E e P/B dentro do esperado para o setor. - Valentina Prudente

**Desafiou**:
- Payout ratio elevado pode comprometer investimentos futuros | Dependência do preço do minério de ferro - Aderbaldo Cíclico; Essa dependência é uma preocupação, mas a Vale tem demonstrado resiliência e capacidade de gerir seus ativos mesmo em condições desafiadoras.

**Evidência nova**: A Vale continua a expandir suas reservas minerais tanto no Brasil quanto no Canadá, o que pode fortalecer sua posição futura.

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- A Vale S.A. sustenta uma posição financeira robusta, com payout ratio sustentável e histórico de dividendos consistente. - Aderbaldo Cíclico

**Desafiou**:
- múltiplo P/E acima do setor | volatilidade de preços do minério de ferro - Mariana Macro; O múltiplo P/E elevado é um reflexo da expectativa de crescimento futuro e não necessariamente indica uma posição financeira fraca, especialmente com a geração de caixa sólida que a Vale tem demonstrado consistentemente.

###### [[Pedro Alocação]] — 🟡 **HOLD**
_Capital Allocator_

**Concordou com**:
- A Vale apresenta uma consistência em dividendos e uma gestão eficiente dos ativos, apesar do múltiplo P/E ligeiramente elevado. - Mariana Macro

**Desafiou**:
- A relação P/E elevada é compensada por um ROE baixo mas gerenciado eficientemente. - Aderbaldo Cíclico | O ROE de 5,9% é significativamente abaixo da média do setor (18%) e pode indicar que a empresa está enfrentando desafios em sua geração de lucros por unidade de capital empregado.

##### Documentos relacionados

- [[VALE3_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[VALE3_2026-04-30|Aderbaldo Cíclico]] em [[Aderbaldo Cíclico]]/reviews/
  - [[VALE3_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[VALE3_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[VALE3_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: BR:VALE3 — VALE3 ===
Sector: Mining  |  Modo (auto): C  |  Held: True
Last price: 81.18000030517578 (2026-04-30)
Position: 500 shares @ entry 61.81
Fundamentals: P/E=24.60 | P/B=1.88 | DY=6.7% | ROE=5.9% | ND/EBITDA=0.97 | DivStreak=18.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=   56.7  ebit=  16.1  ni=  14.7  ebit_margin= 28.4%
  2025-06-30: rev=   49.8  ebit=  11.0  ni=  12.2  ebit_margin= 22.1%
  2025-03-31: rev=   47.4  ebit=  10.9  ni=   8.2  ebit_margin= 23.0%
  2024-12-31: rev=   59.4  ebit=   4.6  ni=  -5.8  ebit_margin=  7.7%
  2024-09-30: rev=   53.0  ebit=  17.2  ni=  13.3  ebit_margin= 32.5%
  2024-06-30: rev=   51.7  ebit=  21.0  ni=  14.6  ebit_margin= 40.5%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: A Vale S.A. (VALE3) é uma excelente posição de longo prazo para um investidor do tipo Buffett/Graham, dada sua sólida geração de caixa e consistência em dividendos. Com um payout ratio sustentável de 50%, a empresa tem mantido um histórico de 18 anos consecutivos de pagamentos de dividendos, oferecendo uma renda estável aos acionistas. A relação P/E de 31,15 é ligeiramente elevada em comparação com o setor, mas compensada pelo baixo múltiplo P/B de 1,99 e um ROE de 5,87%, indicando que a empresa está gerindo bem seus ativos. A relação dívida EBITDA de 0,97 sugere uma posição financeira sólida.

**Key assumptions**:
1. O preço do minério de ferro permanecerá acima dos níveis mínimos históricos.
2. A Vale continuará a manter um payout ratio sustentável entre 50%

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  This position weight: 11.4%
  Sector weight: 11.4%

QUALITY SCORES:
  Piotroski F-Score: 5/9 (2025-12-31)
  Altman Z-Score: 5.05  zone=safe  conf=high
  Beneish M-Score: -2.81  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Vale Posts Strong 1Q26 Output Despite Oman Disruption - The Globe and Mail [Sat, 18 Ap]
    While Oman pellet operations were temporarily halted from mid-March amid Middle East conflict-related logistical constraints, Vale plans to redirect pellet feed to Brazilian plants and fines sales, keeping 2026 agglomerates guidance unchang
  - Brazil mining sector posts higher Q1 revenue, association says - Mining.com [Wed, 15 Ap]
    Brent Crude Oil $ 104.4 / bbl  -4.21%. Palladium $ 1496.5 / ozt  5.39%. Crude Oil $ 101.85 / bbl  -3.06%. Silver Futures $ 75.495 / ozt  7.47%. Micro Gold Futures $ 4713.1 / ozt  3.80%. Micro Silver Futures $ 75.48 / ozt  7.54%. Platinum $ 
  - Vale Indonesia signs $750 million loan deal with global lenders - Mining.com [Thu, 23 Ap]
    Silver Futures $ 75.495 / ozt  7.47%. Micro Gold Futures $ 4713.1 / ozt  3.80%. Micro Silver Futures $ 75.48 / ozt  7.54%. Gold Futures $ 4713.3 / ozt  3.84%. # Vale Indonesia signs $750 million loan deal with global lenders. Nickel miner P
  - Brazil finance minister readies run for Sao Paulo governor - TradingView [Thu, 19 Ma]
    * Image 5 Quartr VLE: Robust 2025 results: high production, strong cash flow, and strategic growth initiatives. * Image 6 Quartr Marfrig Global Foods: Record revenue, robust margins, and synergy gains position the company for strong 2026 gr
  - Vale Base Metals grows resources across Brazil and Canada - Mining.com.au [Wed, 01 Ap]
    * Vale Base Metals grows resources across Brazil and Canada. # Vale Base Metals grows resources across Brazil and Canada. Vale Base Metals, a subsidiary of Vale S.A. (NYSE:VALE) is set to increase its total minerals reserves and resources i

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### ANALYST INSIGHTS (subscriptions BTG/XP/Suno) (5 hits)
[1] suno [2026-04-24] (neutral): [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0
[2] xp [2026-04-24] (bull): [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials
[3] xp [2026-04-24] (bull): [BTG Equity Brazil] VALE3 — peso 9.0%
[4] xp [2026-04-24] (bull): Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes.
[5] xp [2026-04-14] (neutral): [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[6] cvm (comunicado) [2026-04-22]: Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre negociações de contratos de concessão ferroviária
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1506995&numSequencia=1031701&numVersao=2
[7] cvm (comunicado) [2026-04-16]: Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre negociações de contratos de concessão ferroviária
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505854&numSequencia=1030560&numVersao=1
[8] cvm (comunicado) [2026-04-16]: Outros Comunicados Não Considerados Fatos Relevantes | Relatório de produção e vendas da Vale no 1T256
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505852&numSequencia=1030558&numVersao=1
[9] cvm (comunicado) [2026-04-06]: Outros Comunicados Não Considerados Fatos Relevantes | Datas de divulgação do desempenho no 1T26
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1501510&numSequencia=1026216&numVersao=1
[10] cvm (comunicado) [2026-04-02]: Outros Comunicados Não Considerados Fatos Relevantes | Ação de Rating
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1501041&numSequencia=1025747&numVersao=2
[11] cvm (fato_relevante) [2026-03-31]: Atualização de projeções do negócio de Metais Básicos
     URL: https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1498645&numSequencia=1023351&numVersao=1

##### YOUTUBE INSIGHTS (transcripts ingeridos) (15 hits)
[12] YouTube Market Makers [2026-04-21] (operational): O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0
[13] YouTube Market Makers [2026-04-21] (risk): A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção pode mudar.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0
[14] YouTube Market Makers [2026-04-21] (valuation): A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0
[15] YouTube Market Makers [2026-04-21] (operational): O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0
[16] YouTube Market Makers [2026-04-21] (risk): A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção pode mudar.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0
[17] YouTube Market Makers [2026-04-21] (valuation): A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante.
     URL: https://www.youtube.com/watch?v=VS-8e2uZJH0

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[18] Bibliotheca: clip_carteira_dividendos_suno_research: .

| rank | ativo | ticker / empresa | DY esperado | entrada (R$) | preço atual (R$) | preço-teto (R$) | alocação | rentabilidade | viés |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1  0 |  |  | 8,8% | 7,56  06.02.2017 | 9,26  1,20% | 10,00 | 10,0% | 22,49% | Comprar |
| --- | 
[19] Bibliotheca: clip_carteira_dividendos_suno_research: 7 | 17,82 | 20.09.2017 | 23,20 | 30,19% |

|rank|ativo|ticker / empresa|DY esperado|entrada (R$)|preço atual (R$)|preço-teto (R$)|alocação|rentabilidade|viés|
|---|---|---|---|---|---|---|---|---|---|

|             |                                                                                   
[20] Bibliotheca: cwo_power_index: n exporter a country is. It looks at the absolute level of a 
country’s exports as a share of the world. China scores highest (being the largest exporter in the world), 
followed by Europe and the US.

COUNTRY POWER INDEX 2022
55
	■  Military Strength:  This gauge is driven mostly by the absolute sh
[21] Bibliotheca: investment_valuation_3rd_edition: asset 
CF to firm
t
 = Expected cash flow to firm in period t 
WACC = Weighted average cost of capital
While these approaches use different definitions of cash flow and discount rates, they will yield

consistent estimates of value for equity as long as you are consistent in your assumptions in valu
[22] Bibliotheca: investment_valuation_3rd_edition: nd principal payments, they are usually cash flows to the firm. Needless to say,
there are other items that need to be considered when estimating these cash flows, and they are considered in extensive

detail in the coming chapters.
We then add the present value of these excess returns to the invest

##### TAVILY NEWS (≤30d) (5 hits)
[23] Tavily [Sat, 18 Ap]: While Oman pellet o

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3_STORY.md` (cemetery archive)_

#### VALE3 — VALE3

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

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/VALE3_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (5 hits) |
| **2 — Metric Engine** | Receita R$ 38.4 bi · EBITDA est. R$ 7.36 bi · FCF R$ 2.79 bi · ROE 6% · DGR 22.1% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 5/9 · Altman Z=5.05 (safe) · Beneish M=-2.81 (clean) |
| **5 — Classification** | Modo C-BR · Dividend/DRIP (7/12) |
| **5.5 — Council Debate** | BUY (medium) · 1 dissent · 0 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo C-BR sob a Jurisdição BR. VALE3, uma empresa do setor de mineração, é conhecida por sua produção e venda extensiva de minério de ferro, além de outras commodities metálicas como cobre e níquel. A Vale atua em diversos países, com destaque para o Brasil, onde opera algumas das maiores jazidas de minérios do mundo. Além disso, a empresa é reconhecida por seu compromisso com práticas ESG (Ambiental, Social e de Governança), que têm se tornado cada vez mais importantes no cenário global.

A armadilha típica para investidores ao analisar empresas como a Vale é confundir o valor intrínseco do produto mineral com o desempenho sustentável da empresa. O minério de ferro, por exemplo, pode ter preços voláteis devido às flutuações globais na demanda e oferta, mas isso não reflete necessariamente a capacidade operacional ou estratégica da Vale em gerir essas incertezas.

Competitivamente, a Vale ocupa uma posição dominante no mercado global de minério de ferro. A empresa é líder em produção e exportação, beneficiando-se de uma infraestrutura logística robusta que inclui portos e ferrovias próprios. No entanto, a concorrência na exploração de níquel e cobre está se intensificando, especialmente com o aumento da demanda por metais utilizados em tecnologias verdes.

##### Ato 2 — O Contexto

O cenário macroeconômico atual é caracterizado por uma taxa Selic (taxa básica de juros) de 13.75% no mês de abril de 2026, com sinais do Banco Central Brasileiro (BCB) indicando um possível afrouxamento monetário no segundo semestre deste ano, dependendo da evolução do IPCA e das contas públicas. O câmbio BRL/USD oscila na faixa de R$ 5.80 a R$ 6.00, enquanto o custo de capital próprio (Ke) é estimado em aproximadamente 18% (Selic + prêmio de 4.5%). Além disso, os títulos públicos Tesouro IPCA+ 2035 oferecem um retorno real na casa dos 6-7%.

Para o setor de mineração e a Vale especificamente, essas condições macroeconômicas têm implicações significativas. A taxa Selic elevada pode aumentar os custos financeiros para empresas que dependem de financiamento externo ou internamente gerenciado. No entanto, um possível afrouxamento monetário no futuro poderia aliviar essa pressão e melhorar o acesso ao crédito a taxas mais favoráveis.

O câmbio forte pode beneficiar as exportações da Vale, já que os preços das commodities são geralmente negociados em dólares. Isso significa que receitas em moeda estrangeira podem ser convertidas em reais a um valor mais alto, potencialmente aumentando o lucro operacional da empresa.

Em termos regulatórios e estruturais, a Vale enfrenta desafios relacionados à sustentabilidade e segurança ambiental. Recentemente, houve interrupções temporárias nas operações devido a questões logísticas ligadas ao conflito no Oriente Médio (Oman), mas a empresa tem demonstrado resiliência em manter suas metas de produção e vendas através desses desafios.

Essa combinação de fatores macroeconômicos e regulatórios cria um ambiente complexo para a Vale, exigindo uma abordagem estratégica cuidadosa para navegar pelas incertezas globais enquanto busca maximizar o valor dos seus ativos minerais.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa de crescimento e ajustes. As métricas financeiras anuais, apresentadas na tabela a seguir, ilustram essa dinâmica:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 43.84B | R$ 20.73B | R$ 22.80B | 52.0% | R$ 18.79B | 42.9% | R$ 6.04B |
| 2023 | R$ 41.78B | R$ 12.52B | R$ 13.77B | 33.0% | R$ 7.98B | 19.1% | R$ 7.25B |
| 2024 | R$ 38.06B | R$ 8.03B | R$ 8.84B | 23.2% | R$ 6.17B | 16.2% | R$ 2.92B |
| 2025 | R$ 38.40B | R$ 6.69B | R$ 7.36B | 19.2% | R$ 2.35B | 6.1% | R$ 2.79B |

A receita da empresa apresentou um crescimento anual composto (CAGR) de -4,0% entre 2022 e 2025, refletindo uma desaceleração gradual no ritmo de expansão das vendas. A margem EBITDA, que atingiu o auge em 2022 com 52%, declinou para 19% em 2025, indicando um enfraquecimento da eficiência operacional e uma possível pressão sobre os custos fixos. O fluxo de caixa livre (FCF) também mostrou uma trajetória decrescente, passando de R$6,04 bilhões em 2022 para apenas R$2,79 bilhões em 2025.

O lucro contábil pode esconder provisões e ajustes; FCF, não. O fluxo de caixa livre é uma medida mais robusta da geração de valor pela empresa, pois exclui os efeitos das políticas contabilísticas e dos investimentos em ativos intangíveis.

A tabela abaixo apresenta o histórico de dividendos pagos:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 2.408 |
| 2021 | 14.649 |
| 2022 | 7.583 |
| 2023 | 6.078 |
| 2024 | 5.353 |
| 2025 | 7.619 |

A distribuição de dividendos demonstra uma tendência decrescente, com exceções pontuais que podem ser atribuídas a ajustes extraordinários ou políticas temporárias da administração. O Dividend Growth Rate (DGR) calculado é de 22,1% ao ano, mas este valor inclui possíveis dividendos extraordinários e não reflete uma tendência estrutural consistente.

O DGR sem dividendos extraordinários sugere que a empresa tem mantido um compromisso com o retorno aos acionistas, embora haja sinais de compressão na distribuição de lucros. Isso é crucial para investidores interessados em estratégias DRIP (Dividend Reinvestment Plan), pois indica uma consistência no pagamento de dividendos ao longo do tempo.

##### Ato 4 — O Balanço

O balanço financeiro da empresa oferece uma visão detalhada de sua posição atual e sustentabilidade futura. Com um preço de mercado de R$81,18 (2026-04-30), a empresa apresenta indicadores que refletem tanto forças como desafios.

O P/E de 24,60 sugere uma avaliação moderada em relação ao lucro projetado. O P/B de 1,88 indica que o preço das ações está ligeiramente acima do valor contábil por ação, sugerindo um potencial de crescimento ou reconhecimento da qualidade dos ativos da empresa.

O DY (Dividend Yield) de 6,75% é atrativo para investidores em busca de renda. No entanto, o ROE (Return on Equity) de apenas 5,87% indica que a empresa está gerando retornos menores do que o custo médio ponderado de capital (Ke), estimado em cerca de 18,25%.

A relação Net Debt/EBITDA é calculada como R$10,9 bilhões / R$7,36 bilhões = 1,48x. Este valor sugere um nível moderado de alavancagem financeira, mas não indica uma situação crítica.

O Current Ratio (relação entre ativos circulantes e passivos circulantes) é crucial para avaliar a solidez da empresa no curto prazo. Infelizmente, este dado não está disponível nos dados fornecidos.

A relação ROE vs Ke de 5,87% vs ~18,25% sugere que a empresa está criando valor abaixo do custo médio ponderado de capital, o que pode indicar uma necessidade de reavaliação das estratégias operacionais e financeiras. Além disso, não há sinais claros de despesa financeira crescente ou alavancagem excessiva no período analisado.

Em resumo, a empresa apresenta um balanço que reflete tanto oportunidades quanto riscos, com uma necessidade clara de melhorar sua eficiência operacional e gerenciamento de capital para sustentar o crescimento futuro.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa VALE3 oferece uma visão detalhada do seu desempenho relativo ao setor e aos índices de referência. A tabela abaixo resume os principais indicadores, destacando a relação entre o preço das ações e as métricas fundamentais:

| Múltiplo | VALE3 | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 24.60x | 8.00x | 9.00x |
| P/B | 1.88x | 1.50x | 1.60x |
| DY | 6.7% | 7.0% | 6.0% |
| FCF Yield | 0.7% | 10.0% | 5.0% |
| ROE | 5.9% | 18.0% | 13.0% |
| ND/EBITDA | 0.97x | 1.00x | — |

O múltiplo P/E de 24,60 vezes indica que os investidores estão dispostos a pagar um preço significativamente alto em relação ao lucro por ação da empresa, quando comparado à média setorial (8,00x) e aos índices de referência (9,00x). Este valor sugere uma expectativa elevada de crescimento futuro ou um risco percebido menor na comparação com o setor.

O P/B de 1,88 vezes é ligeiramente superior à média do setor (1,50x) e ao índice (1,60x), indicando que os investidores estão dispostos a pagar um prêmio pelo ativo líquido da empresa. Isso pode refletir uma avaliação favorável das perspectivas de valorização patrimonial.

O dividend yield (DY) de 6,7% é ligeiramente inferior à médiana setorial (7,0%) e ao índice (6,0%), indicando que a VALE3 oferece um retorno atrativo em termos de rendimentos, embora não seja o mais generoso do setor. É importante notar que este DY pode incluir dividendos extraordinários, o que pode distorcer ligeiramente a percepção estrutural da remuneração dos acionistas.

O FCF Yield (rendimento de fluxo de caixa livre) é significativamente mais baixo do que tanto a média setorial quanto os índices de referência, com apenas 0,7% contra uma mediana de 10,0% e um índice de 5,0%. Isso sugere que a empresa está gerando fluxo de caixa livre em níveis relativamente baixos comparados ao preço das ações.

O retorno sobre o patrimônio líquido (ROE) da VALE3 é de apenas 5,9%, muito abaixo tanto da média setorial (18,0%) quanto dos índices de referência (13,0%). Este indicador sugere que a empresa está gerando um retorno relativamente baixo sobre o capital investido.

Por fim, o múltiplo ND/EBITDA de 0,97x é ligeiramente inferior à médiana setorial (1,00x), sugerindo que os investidores estão dispostos a pagar um pouco menos em relação ao EBITDA ajustado da empresa. Este valor indica uma avaliação moderada do desempenho operacional.

##### Ato 6 — Os Quality Scores

A análise dos scores de qualidade financeira ajuda a avaliar a solidez e a sustentabilidade das finanças da VALE3. O Piotroski F-Score, que varia entre 0 e 9 pontos, é um indicador robusto do desempenho operacional da empresa. Com um score de 5/9 no final de 2025, a VALE3 mostra uma performance mista, com metade dos critérios analisados sendo favoráveis à saúde financeira e a outra metade não.

O Altman Z-Score de 5,05 coloca a empresa na zona segura (safe), indicando um baixo risco de insolvência. A confiança no cálculo é alta, sugerindo que os dados utilizados são robustos e refletem uma situação financeira estável.

O Beneish M-Score de -2,81 coloca a empresa na zona clean (limpa), indicando baixo risco de manipulação contábil. A confiança no cálculo é alta, o que reforça a credibilidade das demonstrações financeiras da VALE3.

Estes scores sugerem uma situação financeira sólida e transparente, com um desempenho operacional misto mas sustentável em termos de solvência e integridade contábil.

---

##### Ato 7 — O Moat e a Gestão

Vale S.A., uma das maiores empresas minerais do mundo, apresenta um moat (barreira de entrada) que pode ser classificado como moderado. Embora não seja tão robusto quanto o de algumas outras gigantes globais, Vale possui várias características que lhe conferem vantagens competitivas significativas.

###### Custo e Escala
Vale opera em uma escala incomparável, com ativos distribuídos por todo o mundo, incluindo operações na Austrália, Brasil e Indonésia. Esta vasta rede de minas permite que a empresa obtenha economias de escala significativas ao reduzir custos de produção e logística. Além disso, a diversificação geográfica ajuda a mitigar riscos associados a eventos locais.

###### Custos de Mudança
A complexidade das operações minerais torna difícil para novas entradas competirem com Vale sem um investimento significativo em infraestrutura e conhecimento técnico. A empresa também possui contratos de longo prazo com clientes, o que dificulta a mudança para fornecedores alternativos.

###### Efeitos de Rede
Embora não seja uma característica típica das empresas minerais, Vale beneficia-se de um tipo de efeito de rede indireto. A empresa mantém relações estreitas com bancos e instituições financeiras globais para financiamento de longo prazo, o que fortalece sua posição no mercado.

###### Intangíveis
Vale possui uma sólida reputação no setor minério, construída ao longo de décadas. Esta marca forte é um ativo intangível significativo, permitindo à empresa atrair e reter clientes em mercados competitivos.

###### Eficiência Operacional
A empresa demonstra eficiência operacional através da implementação de tecnologias avançadas e práticas sustentáveis na mineração. Isso não apenas reduz os custos de produção, mas também melhora a percepção ambiental do público e dos stakeholders.

###### Gestão
Vale tem uma gestão sólida com um histórico consistente de geração de caixa e distribuição de dividendos. A empresa anunciou recentemente planos para expandir suas operações no Brasil e na Indonésia, demonstrando sua capacidade estratégica de crescimento sustentável.

###### Propriedade Interna
Dado não disponível.

###### Transações Internas dos Últimos 6 Meses
Dado não disponível.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico de Vale S.A. é fortemente orientado para dividendos e pagamentos recorrentes, com um score de Dividend/DRIP de 7 em uma escala de 12. A empresa mantém um histórico ininterrupto de pagamento de dividendos por mais de 18 anos, além de demonstrar consistência na geração de caixa livre (FCF) que supera o lucro líquido, indicando uma cobertura forte do payout.

###### O que o preço desconta
O atual preço da ação de Vale S.A. sugere um cenário otimista para os próximos anos, com crescimento anual esperado em torno de 8% e uma taxa de crescimento perpetuamente estabilizada em 4%. No entanto, o valor intrínseco calculado através do modelo DCF indica que a empresa está atualmente sobreavaliada.

###### O que os fundamen

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\VALE3_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\VALE3_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — VALE3           moeda BRL      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:            500
  Entry price.........: R$       61.81
  Cost basis..........: R$   30,905.00
  Price now...........: R$       85.87
  Market value now....: R$   42,935.00  [+38.9% nao-realizado]
  DY t12m.............: 6.38%  (R$/US$ 5.4772/share)
  DY vs own 10y.......: P50 [fair-rich]  (actual 6.38% em 115 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=18  hist_g_5y=0.221  hist_g_raw=0.221  gordon_g=0.000  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +6.63%  |   -1.00% |  +12.01%       |
  | base         |  +11.06%  |   +0.00% |  +17.43%       |
  | optimista    |  +14.92%  |   +1.00% |  +22.30%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |      9       |       11       |        4       |
  | base         |      8       |       12       |        3       |
  | optimista    |      7       |       12       |        2       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | R$     77,593 | R$     98,805 | R$    121,515 |
  |  10y  | R$    142,324 | R$    227,378 | R$    339,667 |
  |  15y  | R$    265,132 | R$    523,258 | R$    938,212 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\VALE3.md` (cemetery archive)_

#### VALE3 — VALE3

#holding #br #mining

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 6.0/10  |  **Confiança**: 80%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 6.3/10 | 35% | `██████░░░░` |
| Valuation  | 6.0/10 | 30% | `██████░░░░` |
| Momentum   | 4.7/10 | 20% | `█████░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z 5.048221672575513 (SAFE), Piotroski 5/9 (NEUTRAL), DivSafety 45.0/100
- **Valuation**: Screen 0.60, DY percentil P53 (fair-cheap)
- **Momentum**: 1d -1.43%, 30d -6.45%, YTD 10.62%
- **Narrativa**: user_note=False, YT insights 60d=9

###### Razões

- total 6.0 na zona neutra

##### Links

- Sector: [[sectors/Mining|Mining]]
- Market: [[markets/BR|BR]]
- Vídeos: [[videos/2026-04-21_market-makers_risco-guerra-dolar-em-queda-e-petroleo-em-alta-onde-investir-agora-mar|RISCO GUERRA, DÓLAR EM QUEDA E PETRÓLEO ]] · [[videos/2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa|PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CH]] · [[videos/2025-07-27_suno-noticias_vale-a-pena-investir-em-vale-vale3-apos-resultados-operacionais|Vale a pena INVESTIR EM VALE (VALE3) apó]]
- 🎯 **Thesis**: [[wiki/holdings/VALE3|thesis deep]]

##### Snapshot

- **Preço**: R$80.07  (2026-05-07)    _-1.43% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: 5.048 (safe)
- **Piotroski**: 5/9
- **Div Safety**: 45.0/100 (RISK)
- **Posição**: 501.0 sh @ R$61.84  →  P&L 29.48%

##### Fundamentals

- P/E: 24.56135 | P/B: 1.8545884 | DY: 6.84%
- ROE: 6.84% | EPS: 3.26 | BVPS: 43.174
- Streak div: 18y | Aristocrat: None

##### Dividendos recentes

- 2025-12-12: R$3.5818
- 2025-08-13: R$1.8954
- 2025-03-10: R$2.1418
- 2024-12-12: R$0.5205
- 2024-08-05: R$2.0938

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Vale esclarece sobre notí
- **2026-04-29** `comunicado` — Apresentações a analistas/agentes do mercado | Desempenho da Vale no 1T26
- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre negocia
- **2026-04-16** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Atualização sobre negocia
- **2026-04-16** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Relatório de produção e v

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=5 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Morning Call XP | valuation | 0.80 | O futuro do minério de ferro está subindo, indicando potencial positivo para a Vale. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A Vale teve um lucro líquido de quase 2 bilhões de dólares em apenas um trimestre, com alta de 36%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção de minério de ferro da Vale subiu 3%, enquanto as vendas aumentaram 4%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção da Vale Base Metals cresceu 13%, com aumento significativo na produção de cobre e níquel. |
| 2026-05-12 | Virtual Asset | balance_sheet | 1.00 | O EBITDA da Vale aumentou 21% no primeiro trimestre de 2026. |
| 2026-05-12 | Virtual Asset | valuation | 1.00 | O preço das ações da Vale está atualmente em R$81,40 e valoriza 66,47% nos últimos 12 meses. |
| 2026-04-21 | Market Makers | risk | 0.70 | A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção po… |
| 2026-04-21 | Market Makers | operational | 0.70 | O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global. |
| 2026-04-21 | Market Makers | valuation | 0.60 | A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante. |
| 2026-04-20 | Virtual Asset | operational | 0.90 | A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 78.00 | [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] VALE3 — peso 9.0% |
| 2026-04-24 | XP | catalyst | bull | — | Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes. |
| 2026-04-14 | XP | rating | neutral | 71.00 | [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Morning Call XP | fed_path | bearish | O mercado está precificando que o Fed não deve cortar juros no curto prazo e há alguma probabilidade de alta… |
| 2026-05-13 | Morning Call XP | ipca_inflacao | bearish | O IPCA de abril veio acima do esperado, especialmente nos núcleos e serviços subjacentes. |
| 2026-05-13 | Morning Call XP | oil_cycle | bullish | O petróleo subiu 3% no dia anterior, contribuindo para a precificação de que o Fed não deve cortar os juros n… |
| 2026-05-13 | Morning Call XP | us_inflation | bearish | O CPI de abril nos EUA veio acima do esperado, aumentando a probabilidade de que o Fed não corte os juros no… |
| 2026-05-13 | Morning Call XP | usdbrl | bearish | O real ficou estável em relação ao dólar, mas a tendência é de apreciação do dólar contra as moedas emergente… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -11.12%
- **Drawdown 5y**: -32.56%
- **YTD**: +10.62%
- **YoY (1y)**: +51.36%
- **CAGR 3y**: +4.60%  |  **5y**: -7.06%  |  **10y**: +18.05%
- **Vol annual**: +26.34%
- **Sharpe 3y** (rf=4%): +0.02

###### Dividendos
- **DY 5y avg**: +11.12%
- **Div CAGR 5y**: -15.08%
- **Frequency**: semiannual
- **Streak** (sem cortes): 1 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$43.84B | R$18.79B | R$6.04B |
| 2023-12-31 | R$41.78B | R$7.98B | R$7.25B |
| 2024-12-31 | R$38.06B | R$6.17B | R$2.92B |
| 2025-12-31 | R$38.40B | R$2.35B | R$2.79B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "VALE3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-28', '2026-05-05']
series:
  - title: VALE3
    data: [52.74, 54.9, 55.35, 54.01, 52.1, 52.91, 53.18, 51.41, 50.54, 52.65, 55.2, 55.28, 54.4, 57.5, 55.16, 53.75, 54.16, 54.09, 53.24, 54.92, 55.56, 55.71, 56.58, 57.7, 58.0, 57.09, 58.7, 59.2, 59.75, 60.9, 61.73, 63.81, 65.73, 65.04, 65.22, 65.09, 67.4, 71.92, 71.06, 69.29, 72.92, 71.96, 76.32, 75.35, 78.57, 85.02, 87.41, 89.43, 87.05, 83.92, 87.73, 88.16, 78.86, 79.24, 77.13, 78.1, 79.5, 83.09, 85.59, 87.44, 85.97, 84.39, 78.39]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "VALE3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
series:
  - title: Dividends
    data: [0.1663, 1.3255, 1.9689, 1.4144, 2.4075, 14.6486, 7.5833, 6.0778, 5.3529, 7.619]
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
    data: [28.38, 32.148552, 31.148552, 31.339417, 31.000002, 31.000002, 30.866426, 30.79927, 28.887274, 24.6, 23.836365, 23.972477, 24.68997, 24.56135]
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
    data: [7.31, 5.87, 5.87, 5.87, 5.87, 5.87, 5.87, 5.87, 5.87, 5.87, 6.84, 6.84, 6.84, 6.84]
  - title: DY %
    data: [6.2, 6.17, 6.37, 6.38, 6.38, 6.38, 6.41, 6.49, 6.89, 6.75, 6.96, 6.99, 6.74, 6.84]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\VALE3_DOSSIE.md` (cemetery archive)_

#### 📑 VALE3 — Vale

> Generated **2026-04-26** by `ii dossier VALE3`. Cross-links: [[VALE3]] · [[VALE3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

VALE3 negocia P/E 31.0 com ROE de apenas 5.87% e DY 6.38% sustentado por streak de 18 anos — múltiplo esticado para um ROE single-digit. IC HOLD (high confidence, 80% consensus); composite conviction 75. Achado material da Phase Y RI: deteriorating quality YoY com EBIT -25%, exigindo monitorização próxima do ciclo de minério após rally YoY +59.5%.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.77  |  **BVPS**: 43.17
- **ROE**: 5.87%  |  **P/E**: 31.00  |  **P/B**: 1.99
- **DY**: 6.38%  |  **Streak div**: 18y  |  **Market cap**: R$ 366.62B
- **Last price**: BRL 85.87 (2026-04-26)  |  **YoY**: +59.5%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[VALE3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-24)**: A Vale S.A. (VALE3) é uma excelente posição de longo prazo para um investidor do tipo Buffett/Graham, dada sua sólida geração de caixa e consistência em dividendos. Com um payout ratio sustentável de 50%, a empresa tem mantido um histórico de 18 anos consecutivos de pagamentos de dividendos, oferecendo uma renda estável aos acionistas. A relação P/E de 31,15 é ligeiramente elevada em comparação com o setor, mas compensada pelo baixo múltiplo P/B de 1,99 e um ROE de 5,87%, indicando que a empresa está gerindo bem seus ativos. A relação dívida EBITDA de 0,97 sugere uma posição financeira sólida.

**Key assumptions**:
1. O preço do minério de ferro permanecerá acima dos níveis mínimos históricos.
2. A Vale continuará a manter um payout ratio sustentável entre 50%

→ Vault: [[VALE3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **75** |
| Thesis health | 100 |
| IC consensus | 64 |
| Variant perception | 60 |
| Data coverage | 100 |
| Paper track | 50 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 31.00** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 31.00** fora do screen.
- **P/B = 1.99** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.99** — verificar consistência com ROE.
- **DY = 6.38%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **6.38%** passa.
- **ROE = 5.87%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **5.87%** abaixo do critério.
- **Graham Number ≈ R$ 51.87** vs preço **R$ 85.87** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Deteriorating quality (Phase Y RI)** — YoY EBIT -25% sinaliza compressão de margens; ROE caiu para 5.87%. Trigger: `quarterly_history` EBIT YoY < -10% no próximo Q.
- 🔴 **Ciclo do minério de ferro** — receita ultra-correlacionada com preço China spot. Trigger: minério < 80 USD/t sustentado 30d.
- 🟡 **Múltiplo esticado** — P/E 31 com ROE 5.87% implica re-rating só justificável se margens normalizarem. Trigger: `fundamentals.pe > 35` AND `roe < 0.07`.
- 🟡 **Risco regulatório/ESG (Brumadinho/Mariana)** — passivos ambientais e fiscais residuais. Trigger: novo provisionamento >R$5B em earnings.
- 🟢 **Yield trap risk** — DY 6.38% pode comprimir se payout 50% encolhe com lucros. Trigger: `fundamentals.dy < 0.04` próximo trimestre.

##### 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold** sem reforçar a este nível — combinação YoY +59.5% + EBIT -25% YoY + P/E 31 com ROE 5.87% sinaliza ciclo perto do topo. VALE3 é commodity-cyclical (não DRIP puro apesar do streak de 18 anos), pelo que peso prudente <7% da sleeve BR. Cash em BRL fica em BR (não converter); considerar trim parcial se EBIT continuar a deteriorar dois trimestres seguidos ou se minério cair abaixo de 80 USD/t. Reforço só com P/E < 8 e estabilização da margem operacional.

##### 7. Tracking triggers (auto-monitoring)

- **EBIT YoY duplo digit drop** — `SELECT ebit FROM quarterly_history WHERE ticker='VALE3' ORDER BY period_end DESC LIMIT 5` — comparar Q vs Q-4 < -10%
- **ROE colapsa abaixo de 5%** — `SELECT roe FROM fundamentals WHERE ticker='VALE3' ORDER BY period_end DESC LIMIT 1` < 0.05
- **DY corta abaixo de 4%** — `fundamentals.dy < 0.04` (sinal de payout reduction)
- **P/E expande sem ROE** — `fundamentals.pe > 35 AND fundamentals.roe < 0.07`
- **Thesis health degrada** — `SELECT thesis_health FROM conviction_scores WHERE ticker='VALE3'` < 60

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
*Generated by `ii dossier VALE3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=5 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Morning Call XP | valuation | 0.80 | O futuro do minério de ferro está subindo, indicando potencial positivo para a Vale. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A Vale teve um lucro líquido de quase 2 bilhões de dólares em apenas um trimestre, com alta de 36%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção de minério de ferro da Vale subiu 3%, enquanto as vendas aumentaram 4%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção da Vale Base Metals cresceu 13%, com aumento significativo na produção de cobre e níquel. |
| 2026-05-12 | Virtual Asset | balance_sheet | 1.00 | O EBITDA da Vale aumentou 21% no primeiro trimestre de 2026. |
| 2026-05-12 | Virtual Asset | valuation | 1.00 | O preço das ações da Vale está atualmente em R$81,40 e valoriza 66,47% nos últimos 12 meses. |
| 2026-04-21 | Market Makers | risk | 0.70 | A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção po… |
| 2026-04-21 | Market Makers | operational | 0.70 | O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global. |
| 2026-04-21 | Market Makers | valuation | 0.60 | A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante. |
| 2026-04-20 | Virtual Asset | operational | 0.90 | A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 78.00 | [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] VALE3 — peso 9.0% |
| 2026-04-24 | XP | catalyst | bull | — | Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes. |
| 2026-04-14 | XP | rating | neutral | 71.00 | [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Morning Call XP | fed_path | bearish | O mercado está precificando que o Fed não deve cortar juros no curto prazo e há alguma probabilidade de alta… |
| 2026-05-13 | Morning Call XP | ipca_inflacao | bearish | O IPCA de abril veio acima do esperado, especialmente nos núcleos e serviços subjacentes. |
| 2026-05-13 | Morning Call XP | oil_cycle | bullish | O petróleo subiu 3% no dia anterior, contribuindo para a precificação de que o Fed não deve cortar os juros n… |
| 2026-05-13 | Morning Call XP | us_inflation | bearish | O CPI de abril nos EUA veio acima do esperado, aumentando a probabilidade de que o Fed não corte os juros no… |
| 2026-05-13 | Morning Call XP | usdbrl | bearish | O real ficou estável em relação ao dólar, mas a tendência é de apreciação do dólar contra as moedas emergente… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\VALE3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — VALE3

**Committee verdict**: **HOLD** (high confidence, 100% consensus)  
**Votes**: BUY=0 | HOLD=5 | AVOID=0  
**Avg conviction majority**: 5.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- Geração de caixa crescente
- Histórico de dividendos estáveis
- Baixo múltiplo P/B

**Key risk**: Volatilidade dos preços do minério de ferro afeta resultados

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E elevado
- ROE baixo
- FCF inconsistente

**Key risk**: Preço do minério de ferro cair abaixo dos níveis mínimos históricos

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Geração de caixa sólida
- Dividendos consistentes
- Posição financeira estável

**Key risk**: Volatilidade do preço do minério de ferro e exposição a riscos geológicos

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: none)

**Rationale**:
- P/E elevado
- Geração de caixa inconsistente
- Preço do minério volátil

**Key risk**: Volatilidade no preço do minério de ferro pode afetar lucros significativamente

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- Geração de caixa sólida
- Dividendos consistentes
- Posição financeira estável

**Key risk**: Dependência do preço do minério de ferro e volatilidade dos mercados

##### 📊 Context provided

```
TICKER: BR:VALE3

FUNDAMENTALS LATEST:
  pe: 24.996931
  pb: 1.8874786
  dy: 6.72%
  roe: 6.84%
  net_debt_ebitda: 1.0835868739540464
  intangible_pct_assets: 10.3%   (goodwill $1.3B + intangibles $7.7B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=56.7 ebit=16.1 ni=14.7 em%=28.4 debt=99 fcf=6.9
  2025-06-30: rev=49.8 ebit=11.0 ni=12.2 em%=22.1 debt=97 fcf=-0.8
  2025-03-31: rev=47.4 ebit=10.9 ni=8.2 em%=23.0 debt=93 fcf=1.7
  2024-12-31: rev=59.4 ebit=4.6 ni=-5.8 em%=7.7 debt=96 fcf=-5.2
  2024-09-30: rev=53.0 ebit=17.2 ni=13.3 em%=32.5 debt=77 fcf=1.8
  2024-06-30: rev=51.7 ebit=21.0 ni=14.6 em%=40.5 debt=84 fcf=12.5

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: A Vale S.A. (VALE3) é uma excelente posição de longo prazo para um investidor do tipo Buffett/Graham, dada sua sólida geração de caixa e consistência em dividendos. Com um payout ratio sustentável de 50%, a empresa tem mantido um histórico de 18 anos consecutivos de pagamentos de dividendos, oferecendo uma renda estável aos acionistas. A relação P/E de 31,15 é ligeiramente elevada em comparação com o setor, mas compensada pelo baixo múltiplo P/B de 1,99 e um ROE de 5,87%, indicando que a empresa está gerindo bem seus ativos. A relação dívida EBITDA de 0,97 sugere uma posição financeira sólida.

**Key assumptions**:
1. O preço do minério de ferro permanecerá acima dos níveis mínimos históricos.
2. A Vale continuará a manter um payout ratio sustentável entre 50%

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil's Vale posts $1.9 billion net profit in first quarter - Reuters [Tue, 28 Ap]
    REUTERS/Washington Alves Purchase Licensing Rights, opens new tab. SAO PAULO, April 28 (Reuters) - Brazilian ‌miner (VALE3.SA), opens new tab ​on ​Tuesday posted ⁠a $1.89 ​billion ​net profit for ​the
  - Vale posts 36% rise in Q1 profit on more sales, higher prices - Bitget [Wed, 29 Ap]
    Vale posts 36% rise in Q1 profit on 
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=5 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Morning Call XP | valuation | 0.80 | O futuro do minério de ferro está subindo, indicando potencial positivo para a Vale. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A Vale teve um lucro líquido de quase 2 bilhões de dólares em apenas um trimestre, com alta de 36%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção de minério de ferro da Vale subiu 3%, enquanto as vendas aumentaram 4%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção da Vale Base Metals cresceu 13%, com aumento significativo na produção de cobre e níquel. |
| 2026-05-12 | Virtual Asset | balance_sheet | 1.00 | O EBITDA da Vale aumentou 21% no primeiro trimestre de 2026. |
| 2026-05-12 | Virtual Asset | valuation | 1.00 | O preço das ações da Vale está atualmente em R$81,40 e valoriza 66,47% nos últimos 12 meses. |
| 2026-04-21 | Market Makers | risk | 0.70 | A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção po… |
| 2026-04-21 | Market Makers | operational | 0.70 | O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global. |
| 2026-04-21 | Market Makers | valuation | 0.60 | A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante. |
| 2026-04-20 | Virtual Asset | operational | 0.90 | A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 78.00 | [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] VALE3 — peso 9.0% |
| 2026-04-24 | XP | catalyst | bull | — | Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes. |
| 2026-04-14 | XP | rating | neutral | 71.00 | [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Morning Call XP | fed_path | bearish | O mercado está precificando que o Fed não deve cortar juros no curto prazo e há alguma probabilidade de alta… |
| 2026-05-13 | Morning Call XP | ipca_inflacao | bearish | O IPCA de abril veio acima do esperado, especialmente nos núcleos e serviços subjacentes. |
| 2026-05-13 | Morning Call XP | oil_cycle | bullish | O petróleo subiu 3% no dia anterior, contribuindo para a precificação de que o Fed não deve cortar os juros n… |
| 2026-05-13 | Morning Call XP | us_inflation | bearish | O CPI de abril nos EUA veio acima do esperado, aumentando a probabilidade de que o Fed não corte os juros no… |
| 2026-05-13 | Morning Call XP | usdbrl | bearish | O real ficou estável em relação ao dólar, mas a tendência é de apreciação do dólar contra as moedas emergente… |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\VALE3_RI.md` (cemetery archive)_

#### VALE3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `revenue`: **+13.8%**
- ⬆️ **QOQ** `ebit`: **+46.4%**
- ⬆️ **QOQ** `net_income`: **+20.4%**
- ⬆️ **QOQ** `fcf_proxy`: **+959.2%**
- ⬆️ **QOQ** `ebit_margin`: **+6.3pp**
- ⬆️ **YOY** `debt_total`: **+27.6%**
- ⬆️ **YOY** `fco`: **+50.1%**
- ⬆️ **YOY** `fcf_proxy`: **+294.2%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 56.7 mi | R$ 49.8 mi | +13.8% |
| `ebit` | R$ 16.1 mi | R$ 11.0 mi | +46.4% |
| `net_income` | R$ 14.7 mi | R$ 12.2 mi | +20.4% |
| `debt_total` | R$ 98.6 mi | R$ 97.4 mi | +1.3% |
| `fco` | R$ 13.7 mi | R$ 10.6 mi | +29.9% |
| `fcf_proxy` | R$ 6.9 mi | R$ -0.8 mi | +959.2% |
| `gross_margin` | 36.4% | 30.9% | +5.5pp |
| `ebit_margin` | 28.4% | 22.1% | +6.3pp |
| `net_margin` | 25.9% | 24.5% | +1.4pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 56.7 mi | R$ 53.0 mi | +7.0% |
| `ebit` | R$ 16.1 mi | R$ 17.2 mi | -6.6% |
| `net_income` | R$ 14.7 mi | R$ 13.3 mi | +10.5% |
| `debt_total` | R$ 98.6 mi | R$ 77.3 mi | +27.6% |
| `fco` | R$ 13.7 mi | R$ 9.1 mi | +50.1% |
| `fcf_proxy` | R$ 6.9 mi | R$ 1.8 mi | +294.2% |
| `gross_margin` | 36.4% | 34.3% | +2.1pp |
| `ebit_margin` | 28.4% | 32.5% | -4.1pp |
| `net_margin` | 25.9% | 25.1% | +0.8pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 56.7 | 28.4% | 25.9% | 99 | 14 |
| 2025-06-30 | ITR | 49.8 | 22.1% | 24.5% | 97 | 11 |
| 2025-03-31 | ITR | 47.4 | 23.0% | 17.2% | 93 | 10 |
| 2024-12-31 | DFP-ITR | 59.4 | 7.7% | -9.7% | 96 | 17 |
| 2024-09-30 | ITR | 53.0 | 32.5% | 25.1% | 77 | 9 |
| 2024-06-30 | ITR | 51.7 | 40.5% | 28.2% | 84 | 6 |
| 2024-03-31 | ITR | 41.9 | 30.4% | 19.9% | 73 | 18 |
| 2023-12-31 | DFP-ITR | 64.5 | 30.8% | 18.8% | 67 | 24 |
| 2023-09-30 | ITR | 52.0 | 31.8% | 26.9% | 70 | 14 |
| 2023-06-30 | ITR | 47.8 | 29.7% | 10.0% | 67 | 9 |
| 2023-03-31 | ITR | 43.8 | 33.5% | 22.2% | 66 | 19 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [43.8, 47.8, 52.0, 64.5, 41.9, 51.7, 53.0, 59.4, 47.4, 49.8, 56.7]
  - title: EBIT margin %
    data: [33.5, 29.7, 31.8, 30.8, 30.4, 40.5, 32.5, 7.7, 23.0, 22.1, 28.4]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\VALE3_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — VALE3

**Our stance**: bullish  
**Analyst consensus** (5 insights, last 90d): bullish (60% bull)  
**Weighted consensus** (source win-rate weighted): bullish (60% bull)  
**Variance type**: `low_consensus_long` (magnitude 1/5)  
**Interpretation**: consensus pick — no edge

##### 📰 Recent analyst insights

- [neutral] *suno (w=0.50)* [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0
- [neutral] *xp (w=0.50)* [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais
- [bull] *xp (w=0.50)* [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials
- [bull] *xp (w=0.50)* [BTG Equity Brazil] VALE3 — peso 9.0%
- [bull] *xp (w=0.50)* Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes.

##### ⚖️ Source weights (predictions win-rate)

- 📊 `suno` → 0.50 *(no track record yet)*
- 📊 `xp` → 0.50 *(no track record yet)*

##### 📜 Our thesis

**Core thesis (2026-04-24)**: A Vale S.A. (VALE3) é uma excelente posição de longo prazo para um investidor do tipo Buffett/Graham, dada sua sólida geração de caixa e consistência em dividendos. Com um payout ratio sustentável de 50%, a empresa tem mantido um histórico de 18 anos consecutivos de pagamentos de dividendos, oferecendo uma renda estável aos acionistas. A relação P/E de 31,15 é ligeiramente elevada em comparação com o setor, mas compensada pelo baixo múltiplo P/B de 1,99 e um ROE de 5,87%, indicando que a empresa está gerindo bem seus ativos. A relação dívida EBITDA de 0,97 sugere uma posição financeira sólida.

**Key assumptions**:
1. O preço do minério de ferro permanecerá acima dos níveis mínimos históricos.
2. A Vale continuará a manter um payout ratio sustentável entre 50%

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=5 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Morning Call XP | valuation | 0.80 | O futuro do minério de ferro está subindo, indicando potencial positivo para a Vale. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A Vale teve um lucro líquido de quase 2 bilhões de dólares em apenas um trimestre, com alta de 36%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção de minério de ferro da Vale subiu 3%, enquanto as vendas aumentaram 4%. |
| 2026-05-12 | Virtual Asset | operational | 1.00 | A produção da Vale Base Metals cresceu 13%, com aumento significativo na produção de cobre e níquel. |
| 2026-05-12 | Virtual Asset | balance_sheet | 1.00 | O EBITDA da Vale aumentou 21% no primeiro trimestre de 2026. |
| 2026-05-12 | Virtual Asset | valuation | 1.00 | O preço das ações da Vale está atualmente em R$81,40 e valoriza 66,47% nos últimos 12 meses. |
| 2026-04-21 | Market Makers | risk | 0.70 | A Vale sofreu durante a guerra devido à antecipação de uma desaceleração global, mas com a diminuição do risco da guerra, essa percepção po… |
| 2026-04-21 | Market Makers | operational | 0.70 | O preço do minério de ferro subiu durante o período da guerra, mas a Vale caiu devido à antecipação de uma desaceleração global. |
| 2026-04-21 | Market Makers | valuation | 0.60 | A Vale é vista como uma oportunidade de investimento, pois a tese de hard assets e commodities continua relevante. |
| 2026-04-20 | Virtual Asset | operational | 0.90 | A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 78.00 | [Suno Valor] VALE3 — peso 5.0%, rating Aguardar, PT R$78.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] VALE3 — peso 9.0%, setor Materials |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] VALE3 — peso 9.0% |
| 2026-04-24 | XP | catalyst | bull | — | Vale (VALE3) ADICIONADA ao portfolio Dividendos (substituindo GGBR4) — preços minério resilientes. |
| 2026-04-14 | XP | rating | neutral | 71.00 | [XP Top Dividendos] VALE3 — peso 12.5%, Neutro, PT R$71.0, setor Materiais |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Morning Call XP | fed_path | bearish | O mercado está precificando que o Fed não deve cortar juros no curto prazo e há alguma probabilidade de alta… |
| 2026-05-13 | Morning Call XP | ipca_inflacao | bearish | O IPCA de abril veio acima do esperado, especialmente nos núcleos e serviços subjacentes. |
| 2026-05-13 | Morning Call XP | oil_cycle | bullish | O petróleo subiu 3% no dia anterior, contribuindo para a precificação de que o Fed não deve cortar os juros n… |
| 2026-05-13 | Morning Call XP | us_inflation | bearish | O CPI de abril nos EUA veio acima do esperado, aumentando a probabilidade de que o Fed não corte os juros no… |
| 2026-05-13 | Morning Call XP | usdbrl | bearish | O real ficou estável em relação ao dólar, mas a tendência é de apreciação do dólar contra as moedas emergente… |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\VALE3.md` (cemetery archive)_

#### 🎯 Thesis: [[VALE3]] — Vale

> #1-2 global producer iron ore + nickel + cobre. Tese híbrida: income cíclico + USD-exposure natural via export. Não é DRIP "safe" — é DRIP de **commodity cycle**.

##### Intent
**DRIP cyclical** — reinvestir dividendos em trough (Brent / ferro barato); trim em peak. NÃO é DRIP tipo JNJ (steady state).

##### Business snapshot
- **Ferro** ~70% EBITDA (operações Carajás, Minas Centrais, Sudeste).
- **Nickel** ~15% (Canadá, Indonésia — strategic EV metal).
- **Cobre** ~10% (Salobo, Sossego — growth segment).
- **Others**: coal (divesting), manganese, logistics (VLI minority).
- Custo ferro caixa ~$25-35/t (lowest tier global com Rio Tinto Pilbara).

##### Por que detemos

1. **Low-cost moat ferro** — sobrevive China demand softness $80/t.
2. **China absorbente #1** (60%+ demanda marginal). Infra + housing + EV chips.
3. **USD exposure natural** — receita 100% USD + custo BRL → BRL fraco = windfall.
4. **Payout alto** — 30-50% FCF em years favoráveis, DY peaks 12-20%.
5. **Cobre optionality** — pipeline Alemão + Salobo expansão = EV metal exposure.

##### Moat

- **Carajás** reserva ferro alta lei (68% Fe) — prémio vs Pilbara padrão.
- **Scale** — produção 300+ Mt/y ferro = economias escala logísticas (rail + port).
- **Relationship China** — Vale's iron ore premium chegou até ao governo chinês como supply strategic.
- **Weak moat sobre preço** — spot IODEX dicta revenue.

##### Current state (2026-04)

- Ferro spot IODEX $100-110/t (soft vs 2021 peak $200, acima do distress $80).
- China real estate stress persistente → demanda ferro flat-declining.
- Nickel weak (Indonésia oversupply).
- Cobre firme (EV + grid build-out tailwinds).
- Samarco resolução (provisões pesadas finalmente resolvendo).
- BRL fraco R$5.80 = tailwind EBITDA.

##### Cycle context

Cenário ferro 3-5y:
- **Bull**: China stimulus agressivo + India steel growth + infra global.
- **Bear**: China deflation deep → ferro < $80 sustained → Vale FCF 50% menor.
- **Base**: ferro $90-110 sideways → VALE3 DY 8-10% comfortable.

##### Invalidation triggers

- [ ] Ferro IODEX < $80 sustained > 12m (structural demand break)
- [ ] Dividend cut para proteger balance sheet sem guidance clara
- [ ] Acidente operacional severo (pós-Brumadinho, Samarco) → multa > 10% MV
- [ ] Governance interferência estatal (Previ stakeholder activismo)
- [ ] Net debt / EBITDA > 2× peak cycle (historicamente ficam < 1.5)
- [ ] Perda maior executiva estratégica sem replacement

##### Sizing

- Posição actual: 500 shares
- Target 6-8% sleeve BR (cycle-aware — cap em peaks)
- Trim em DY < 3% (cycle peak) → redeploy [[ITSA4]] / [[BBDC4]]
- Accumulate em DY > 12% (cycle trough) → capital gain ready se ciclo reverte


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -4.57%
- **Drawdown 5y**: -27.59%
- **YTD**: +18.78%
- **YoY (1y)**: +57.86%
- **CAGR 3y**: +6.11%  |  **5y**: -4.46%  |  **10y**: +16.89%
- **Vol annual**: +25.19%
- **Sharpe 3y** (rf=4%): +0.08

###### Dividendos
- **DY 5y avg**: +11.12%
- **Div CAGR 5y**: -15.08%
- **Frequency**: semiannual
- **Streak** (sem cortes): 1 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Iron_ore]] — benchmark + drivers (China demand sub-60% marginal)
- [[USDBRL_PTAX]] — FX motor lateral
- [[PRIO3]] — outro commodity BR cíclico (diversifier oil vs metal)
- [[SUZB3]] — wiki/sectors/Pulp_and_Paper_cycle (comparable cycle mechanic)
- [[wiki/sectors/Pulp_and_Paper_cycle]] — pulp BR-specific advantage template

##### Memory refs

- Cycle-aware DRIP: reinvest trough only, trim peak

## ⚙️ Refresh commands

```bash
ii panorama VALE3 --write
ii deepdive VALE3 --save-obsidian
ii verdict VALE3 --narrate --write
ii fv VALE3
python -m analytics.fair_value_forward --ticker VALE3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
