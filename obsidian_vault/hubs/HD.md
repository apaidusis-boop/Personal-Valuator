---
type: ticker_hub
ticker: HD
market: us
sector: Consumer Disc.
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 16
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# HD — Home Depot

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Consumer Disc.` · `market: US` · `currency: USD` · `bucket: holdings` · `16 sources merged`

## 🎯 Hoje

- **Posição**: 1.0 @ entry 292.02
- **Verdict (DB)**: `HOLD` (score 5.95, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 21.28 · P/B 23.52 · DY 3.1% · ROE 145.5% · ND/EBITDA 2.58 · Dividend streak 40 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-19 · Earnings prep
_source: `briefings\earnings_prep_HD_2026-05-19.md` (now in cemetery)_

#### 📞 Earnings Prep — HD (2026-05-19)

_Auto-generated 22 days before call. 100% Ollama local._

##### 🔥 Top 3 things to watch
- Crescimento das vendas comparáveis (0% a 2%) e impacto na margem operacional (max 30 palavras)
- Fluxo de caixa livre e nível de dívida líquida (vs EBITDA: 2.58x)
- Perspectivas de lucros por ação para o ano fiscal de 2026

##### ❓ Specific questions to listen for management
1. Como os aumentos nos preços das casas e a baixa rotação no mercado residencial afetam as vendas futuras?
2. Qual é o plano da Home Depot para mitigar preocupações dos clientes sobre a habitação e empregabilidade?
3. Quais são as expectativas de Home Depot em relação ao crescimento nas categorias profissionais versus DIY?
4. Como a empresa planeja lidar com a desaceleração na demanda por produtos de reparo e manutenção?
5. Qual é o impacto esperado da inflação nos custos operacionais?

##### 📊 Trajectory check (vs trend)
- Confirmar se as vendas comparáveis continuarão em tendência de crescimento lenta
- Mudança na orientação financeira para indicar uma reversão na desaceleração das vendas

##### 🚨 Red flags potenciais
- Dívida líquida/EBITDA aumentando significativamente (atualmente 2.58x)
- Margens operacionais caindo abaixo do esperado devido a pressões nos custos

##### 🎯 Decision framework
- BUY MORE if: Crescimento das vendas comparáveis acima de 2% e melhora na margem operacional
- HOLD if: Vendas dentro da faixa projetada (0%-2%) com estabilidade nas margens
- TRIM if: Perspectivas de crescimento abaixo do esperado ou sinais de pressão nos custos

---
##### 📊 Context provided to LLM

```
TICKER: US:HD
EARNINGS DATE: 2026-05-19

FUNDAMENTALS:
  pe: 23.587782
  pb: 26.110853
  dy: 2.75%
  roe: 145.54%
  net_debt_ebitda: 2.579664948386075

THESIS HEALTH: -1/100 (contras=0, risk_flags=0)

WEB EARNINGS CONTEXT (Tavily synth, last 90d):
  Home Depot's earnings results for the last quarter surpassed Wall Street's expectations, despite a decline in sales. The company reported a net income of $2.57 billion, or $2.58 per share, down from $3.0 billion, or $3.02 per share, in the same period last year. However, comparable sales increased by 0.4% and average ticket rose by 2.4%. Home Depot's CFO noted that customers are concerned about housing affordability and job losses, which have influenced the company's outlook for the year. The company anticipates flat to a 2% increase in comparable sales for 2026 due to ongoing affordability pr

WEB GUIDANCE CONTEXT (Tavily synth, last 60d):
  Home Depot's forward guidance for fiscal year 2026 anticipates sales to range from flat to a 2% gain, influenced by the ongoing struggles in the housing market, including significant increases in home prices and low housing turnover since 2023.

WEB EARNINGS HEADLINES:
  - Home Depot beats Wall Street’s expectations, even as sales decline - CNBC
  - Home Depot beats quarterly sales estimates on demand from professional customers - Reuters
  - Home Depot tops expectations in the fourth quarter, but customers pull back on spending - Greenwich 

WEB GUIDANCE HEADLINES:
  - DIY Doldrums Overshadow Home Depot, Lowe's 02/26/2026 - MediaPost
  - Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround - InternetRetailin
  - Bitcoin Stands Strong at $71,000 as Trump Warns of Attacks on Iran’s ‘Crown Jewel’ - TipRanks
```

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\HD.md` (now in cemetery)_

#### HD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ir.homedepot.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=292.02 · date=2023-10-12

- Total events na DB: **140**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=311.3999938964844
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=1.45541 · DY=0.029640334556551847 · P/E=21.898733
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-07 | proxy | sec | DEF 14A |
| 2026-03-18 | 10-K | sec | 10-K |
| 2026-02-24 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2025-11-25 | 10-Q | sec | 10-Q |
| 2025-11-24 | 8-K | sec | 8-K \| 5.03,8.01,9.01 |

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

#### 2026-05-01 · Council review · Charlie Compounder
_source: `agents\Charlie Compounder\reviews\HD_2026-05-01.md` (now in cemetery)_

#### Charlie Compounder sobre [[HD_STORY|HD]]

**Função no debate**: Industrials & Consumer US Specialist (Buffett frame) (`sector_specialist`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Home Depot mantém sólida posição de mercado, mas valuation está esticado_

HD possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett.

**Métricas que invoquei**:
- ROE=145.5%
- DivStreak=40y
- P/E=23.09x

**Preocupações**:
- P/E > 20
- P/B > 3

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Home Depot has a high ROE and safe Altman Z-Score, yet recent unauthorized discounting incidents raise red flags.
- Valentina Prudente

**Desafiei**:
- P/E e P/B acima da média do setor indicam sobreavaliação
- Pedro Alocação
- razão: Embora o P/E esteja ligeiramente acima do frame Buffett, a empresa mantém um histórico consistente de dividendos e buybacks que sustentam uma avaliação mais alta. O P/B é significativamente maior, mas deve-se considerar a natureza do negócio da Home Depot com ativos intangíveis significativos que podem distorcer o cálculo.

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[HD_STORY|📖 Storytelling completo (8 actos)]]
- [[HD_COUNCIL|🏛️ Transcript do Council debate]]
- [[Charlie Compounder|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Mariana Macro
_source: `agents\Mariana Macro\reviews\HD_2026-05-01.md` (now in cemetery)_

#### Mariana Macro sobre [[HD_STORY|HD]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Home Depot mantém posição de liderança apesar dos desafios operacionais_

P/E e P/B acima da média do setor sugerem valorização atual, com ROE elevado indicando eficiência na geração de lucros. No entanto, recentes escândalos operacionais podem afetar a reputação.

**Métricas que invoquei**:
- P/E=23.09x
- P/B=25.56x
- ROE=145.5%

**Preocupações**:
- escândalos de fraude interna
- declínio nas vendas do último trimestre

##### Round 2 — Resposta aos colegas

**Concordei com**:
- Home Depot possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett.
- Valentina Prudente

**Desafiei**:
- P/E > 20 | P/B > 3
- A relação entre P/E e P/B deve ser analisada em contexto macro. Com taxas de juros baixas, múltiplos mais altos podem ser sustentáveis.
- Charlie Compounder

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[HD_STORY|📖 Storytelling completo (8 actos)]]
- [[HD_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Pedro Alocação
_source: `agents\Pedro Alocação\reviews\HD_2026-05-01.md` (now in cemetery)_

#### Pedro Alocação sobre [[HD_STORY|HD]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Home Depot mantém posição de liderança apesar dos desafios operacionais_

P/E e P/B acima da média do setor indicam sobreavaliação, mas Z-Score alto sugere solidez financeira. Dívidas elevadas são preocupantes.

**Métricas que invoquei**:
- P/E=23.09x
- P/B=25.56x
- Z-Score=5.71

**Preocupações**:
- Fraudes internas afetam reputação e custos operacionais
- Dívida líquida alta pode comprometer flexibilidade financeira

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E e P/B acima da média do setor indicam sobreavaliação, Charlie Compounder

**Desafiei**:
- HD possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett. - Esses múltiplos elevados podem ser justificados por sua posição de liderança no mercado, mas a sobrevalorização é um risco significativo.
- citação + razão de discordância + Charlie Compounder

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[HD_STORY|📖 Storytelling completo (8 actos)]]
- [[HD_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Valentina Prudente
_source: `agents\Valentina Prudente\reviews\HD_2026-05-01.md` (now in cemetery)_

#### Valentina Prudente sobre [[HD_STORY|HD]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Strong fundamentals but fraud concerns_

Home Depot has a high ROE and safe Altman Z-Score, yet recent unauthorized discounting incidents raise red flags.

**Métricas que invoquei**:
- ROE=145.5%
- Altman Z-Score: 5.71
- Piotroski F-Score: 4/9

**Preocupações**:
- Unauthorized discounts fraud
- Negative press on sales decline

##### Round 2 — Resposta aos colegas

**Concordei com**:
- P/E e P/B acima da média do setor indicam sobreavaliação
- Charlie Compounder

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[HD_STORY|📖 Storytelling completo (8 actos)]]
- [[HD_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*


### 2017

#### 2017-08-22 · Filing 2017-08-22
_source: `dossiers\HD_FILING_2017-08-22.md` (now in cemetery)_

#### Filing dossier — [[HD]] · 2017-08-22

**Trigger**: `sec:10-Q` no dia `2017-08-22`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/354950/000035495017000032/hd_10qx07302017.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 317.45

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `28.97` |
| HOLD entre | `28.97` — `38.63` (consensus) |
| TRIM entre | `38.63` — `44.43` |
| **SELL acima de** | `44.43` |

_Método: `buffett_ceiling`. Consensus fair = R$38.63. Our fair (mais conservador) = R$28.97._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `1.45541` | `1.1048` | +24.1% |
| EPS | `14.23` | `14.2271` | +0.0% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 38.63 | 28.97 | 317.45 | SELL | cross_validated | `filing:sec:10-Q:2017-08-22` |
| 2026-05-08T20:37:29+00:00 | `buffett_ceiling` | 38.63 | 28.97 | 317.45 | SELL | cross_validated | `manual` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 38.63 | 28.97 | 323.05 | SELL | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 38.63 | 28.97 | 323.05 | SELL | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 38.63 | 28.97 | 323.05 | SELL | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 38.59 | 28.94 | 323.05 | SELL | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 38.59 | 28.94 | 323.05 | SELL | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 38.59 | 28.94 | 323.05 | SELL | single_source | `phase_ll_dualclass_fixed` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · DRIP scenarios
_source: `briefings\drip_scenarios\HD_drip.md` (now in cemetery)_

/============================================================================\
|   DRIP SCENARIO — HD              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              1
  Entry price.........: US$      292.02
  Cost basis..........: US$      292.02
  Price now...........: US$      335.89
  Market value now....: US$      335.89  [+15.0% nao-realizado]
  DY t12m.............: 2.75%  (R$/US$ 9.2300/share)
  DY vs own 10y.......: P94 [CHEAP]  (actual 2.75% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=40  hist_g_5y=0.087  hist_g_raw=0.087  gordon_g=0.512  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +12.55%       |
  | base         |  +18.00%  |   +0.00% |  +20.75%       |
  | optimista    |  +22.00%  |   +1.00% |  +25.75%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     14       |       23       |        5       |
  | base         |     11       |       26       |        3       |
  | optimista    |     10       |       29       |        3       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        616 | US$        880 | US$      1,079 |
  |  10y  | US$      1,137 | US$      2,305 | US$      3,451 |
  |  15y  | US$      2,114 | US$      6,040 | US$     10,976 |
  --------------------------------------------------------------------------

#### — · Council aggregate
_source: `dossiers\HD_COUNCIL.md` (now in cemetery)_

#### Council Debate — [[HD_STORY|HD]] (Home Depot)

**Final stance**: 🟡 **HOLD**  
**Confidence**: `high`  
**Modo (auto)**: A (US)  |  **Sector**: Consumer Disc.  |  **Held**: sim  
**Elapsed**: 59.0s  |  **Failures**: 0

##### Quem esteve na sala

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- Home Depot tem um ROE elevado e uma história consistente de dividendos; P/E e P/B acima da média do setor indicam sobreavaliação; escândalos operacionais podem afetar a reputação
- Metrics: ROE=145.5%, DivStreak=40y, P/E=23.09x, P/B=25.56x

**Dissenso (preservado)**:
- Charlie Compounder disse que o P/E acima do frame Buffett pode ser justificado por dividendos e buybacks consistentes; Mariana Macro disse que a relação entre P/E e P/B deve ser analisada em contexto macro com taxas de juros baixas
- Pedro Alocação disse que múltiplos elevados podem ser justificados pela posição de liderança no mercado, mas é um risco significativo

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ escândalos operacionais afetam a reputação e custos operacionais
- ⚠️ dúvida sobre a sustentabilidade dos múltiplos elevados em um contexto macro de taxas de juros baixas

**Sizing**: Considerar reduzir posição para até 1% do portfolio dada a sobreavaliação e riscos operacionais

##### Round 1 — Opening Statements (blind)

###### [[Charlie Compounder]] — 🟡 **HOLD**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _Home Depot mantém sólida posição de mercado, mas valuation está esticado_

HD possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett.

**Métricas**:
- ROE=145.5%
- DivStreak=40y
- P/E=23.09x

**Preocupações**:
- P/E > 20
- P/B > 3

###### [[Mariana Macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Headline**: _Home Depot mantém posição de liderança apesar dos desafios operacionais_

P/E e P/B acima da média do setor sugerem valorização atual, com ROE elevado indicando eficiência na geração de lucros. No entanto, recentes escândalos operacionais podem afetar a reputação.

**Métricas**:
- P/E=23.09x
- P/B=25.56x
- ROE=145.5%

**Preocupações**:
- escândalos de fraude interna
- declínio nas vendas do último trimestre

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Headline**: _Strong fundamentals but fraud concerns_

Home Depot has a high ROE and safe Altman Z-Score, yet recent unauthorized discounting incidents raise red flags.

**Métricas**:
- ROE=145.5%
- Altman Z-Score: 5.71
- Piotroski F-Score: 4/9

**Preocupações**:
- Unauthorized discounts fraud
- Negative press on sales decline

###### [[Pedro Alocação]] — 🟡 **HOLD**
_Capital Allocator_

**Headline**: _Home Depot mantém posição de liderança apesar dos desafios operacionais_

P/E e P/B acima da média do setor indicam sobreavaliação, mas Z-Score alto sugere solidez financeira. Dívidas elevadas são preocupantes.

**Métricas**:
- P/E=23.09x
- P/B=25.56x
- Z-Score=5.71

**Preocupações**:
- Fraudes internas afetam reputação e custos operacionais
- Dívida líquida alta pode comprometer flexibilidade financeira

##### Round 2 — Respostas (peers visíveis)

###### [[Charlie Compounder]] — 🟡 **HOLD**
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- Home Depot has a high ROE and safe Altman Z-Score, yet recent unauthorized discounting incidents raise red flags.
- Valentina Prudente

**Desafiou**:
- P/E e P/B acima da média do setor indicam sobreavaliação
- Pedro Alocação
- razão: Embora o P/E esteja ligeiramente acima do frame Buffett, a empresa mantém um histórico consistente de dividendos e buybacks que sustentam uma avaliação mais alta. O P/B é significativamente maior, mas deve-se considerar a natureza do negócio da Home Depot com ativos intangíveis significativos que podem distorcer o cálculo.

###### [[Mariana Macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Concordou com**:
- Home Depot possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett.
- Valentina Prudente

**Desafiou**:
- P/E > 20 | P/B > 3
- A relação entre P/E e P/B deve ser analisada em contexto macro. Com taxas de juros baixas, múltiplos mais altos podem ser sustentáveis.
- Charlie Compounder

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Concordou com**:
- P/E e P/B acima da média do setor indicam sobreavaliação
- Charlie Compounder

###### [[Pedro Alocação]] — 🟡 **HOLD**
_Capital Allocator_

**Concordou com**:
- P/E e P/B acima da média do setor indicam sobreavaliação, Charlie Compounder

**Desafiou**:
- HD possui forte ROE e longa história de dividendos, porém P/E e P/B estão acima do frame Buffett. - Esses múltiplos elevados podem ser justificados por sua posição de liderança no mercado, mas a sobrevalorização é um risco significativo.
- citação + razão de discordância + Charlie Compounder

##### Documentos relacionados

- [[HD_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[HD_2026-05-01|Charlie Compounder]] em [[Charlie Compounder]]/reviews/
  - [[HD_2026-05-01|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[HD_2026-05-01|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[HD_2026-05-01|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:HD — Home Depot ===
Sector: Consumer Disc.  |  Modo (auto): A  |  Held: True
Last price: 328.79998779296875 (2026-04-30)
Position: 1 shares @ entry 292.02
Fundamentals: P/E=23.09 | P/B=25.56 | DY=2.8% | ROE=145.5% | ND/EBITDA=2.58 | DivStreak=40.00

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 1.5%
  Sector weight: 6.5%

QUALITY SCORES:
  Piotroski F-Score: 4/9 (2026-01-31)
  Altman Z-Score: 5.71  zone=safe  conf=high
  Beneish M-Score: -2.42  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Florida Home Depot manager arrested for allegedly dishing out $4M in ‘unauthorized’ discounts to boost his sales - New York Post [Sat, 25 Ap]
    # Florida Home Depot manager arrested for allegedly dishing out $4M in ‘unauthorized’ discounts to boost his sales. A Florida Home Depot manager was arrested on felony charges after allegedly dishing out $4.3 million in “unauthorized” disco
  - Home Depot eyes same-day, next-day delivery site in New York - Retail Dive [Mon, 20 Ap]
    # Home Depot eyes same-day, next-day delivery site in New York. * The Home Depot is exploring the construction of a distribution center providing same-day and next-day delivery of bulky goods in Yaphank, New York, per an application filed w
  - Home Depot manager accused of giving millions in fraudulent discounts - USA Today [Fri, 24 Ap]
    A Home Depot manager in Florida is accused of running a "deliberate" and "systematic" fraud scheme at stores where he worked, leading the company to lose more than $4 million through unauthorized discounts, arrest documents show. Mauricio J
  - DIY Doldrums Overshadow Home Depot, Lowe's 02/26/2026 - MediaPost [Sun, 08 Ma]
    # DIY Doldrums Overshadow Home Depot, Lowe's. overstretched budgets, and Home Depot and Lowe’s are feeling the pinch. At Home Depot, sales for the fiscal fourth quarter fell 3.8% to $38.2 billion, with some of that decline. And it reiterate
  - Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround - InternetRetailing [Tue, 31 Ma]
    You are in: Home » Marketplaces » **Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround**. # Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround. The Group’s trading statement for 
  - Bitcoin Stands Strong at $71,000 as Trump Warns of Attacks on Iran’s ‘Crown Jewel’ - TipRanks [Sat, 14 Ma]
    “Focus on Improving Customer Experience”: Home Depot Stock (NYSE:HD) Notches Up as Live Tracking Gets Fleshed Out. HD](/news/focus-on-improving-customer-experience-home-depot-stock-nysehd-notches-up-as-live-tracking-gets-fleshed-out "HD"). 

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (7 hits)
[1] sec (proxy) [2026-04-07]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/354950/000035495026000090/hd-20260406.htm
[2] sec (10-K) [2026-03-18]: 10-K
     URL: https://www.sec.gov/Archives/edgar/data/354950/000162828026019436/hd-20260201.htm
[3] sec (8-K) [2026-02-24]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/354950/000035495026000026/hd-20260224.htm
[4] sec (10-Q) [2025-11-25]: 10-Q
     URL: https://www.sec.gov/Archives/edgar/data/354950/000162828025053868/hd-20251102.htm
[5] sec (8-K) [2025-11-24]: 8-K | 5.03,8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/354950/000035495025000247/hd-20251120.htm
[6] sec (8-K) [2025-11-18]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/354950/000035495025000238/hd-20251118.htm

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[7] Bibliotheca: investment_valuation_3rd_edition: r countries often use
accelerated depreciation for both tax and financial reporting purposes, leading to reported income
that is understated relative to that of their U.S. counterparts.
Current Assets

Current assets include inventory, cash, and accounts receivable. It is in this category that accou
[8] Bibliotheca: investment_valuation_3rd_edition: firm. In
contrast, when an intangible asset is acquired from an external party, it is treated as an asset.
Intangible assets have to be amortized over their expected lives, with a maximum amortization

period of 40 years. The standard practice is to use straight-line amortization. For tax purposes,

[9] Bibliotheca: investment_valuation_3rd_edition: 0
Inventories
$ 8,349
$ 4,293
Other current assets
$         0
$    109
Total current assets
$16,375
$ 4,933
Total assets
$36,672
$13,465
There are five points worth noting about these asset values:

1.

Goodwill.
 Boeing, which acquired Rockwell in 1996 and McDonnell Douglas in 1997, used purchase 
[10] Bibliotheca: investment_valuation_3rd_edition: records them at market
value. The Home Depot has a mix of trading, available-for-sale, and held-to-maturity investments and therefore uses a mix
of book and market value to value these investments.
5.

Prepaid pension expense.
 Boeing records the excess of its pension fund assets over its expected p
[11] Bibliotheca: investment_valuation_3rd_edition: te:
1.
 When companies buy back stock for short periods, with the intent of reissuing the stock or using
it to cover option exercises, they are allowed to show the repurchased stock as treasury stock,

which reduces the book value of equity. Firms are not allowed to keep treasury stock on the books


##### TAVILY NEWS (≤30d) (5 hits)
[12] Tavily [Sat, 25 Ap]: # Florida Home Depot manager arrested for allegedly dishing out $4M in ‘unauthorized’ discounts to boost his sales. A Florida Home Depot manager was arrested on felony charges after allegedly dishing out $4.3 million in “unauthorized” discounts to repeat clients to boost his sales and get higher bon
     URL: https://nypost.com/2026/04/25/us-news/florida-home-depot-manager-arrested-for-allegedly-dishing-out-4m-in-unauthorized-discounts/
[13] Tavily [Mon, 20 Ap]: # Home Depot eyes same-day, next-day delivery site in New York. * The Home Depot is exploring the construction of a distribution center providing same-day and next-day delivery of bulky goods in Yaphank, New York, per an application filed with the Brookhaven Industrial Development Agency last month.
     URL: https://www.retaildive.com/news/home-depot-same-next-day-delivery-new-york/817918/
[14] Tavily [Fri, 24 Ap]: A Home Depot manager in Florida is accused of running a "deliberate" and "systematic" fraud scheme at stores where he worked, leading the company to lose more than $4 million through unauthorized discounts, arrest documents show. Mauricio Jimenez, 48, faces organized fraud and first-degree grand the
     URL: https://www.usatoday.com/story/news/nation/2026/04/23/home-depot-manager-arrested-fraudulent-discount-scheme-florida/89755375007/
[15] Tavily [Thu, 23 Ap]: # Home Depot says ‘bye’ to a traditional customer service feature in favor of AI. Home Depot is letting go of a traditional store feature and introducing a new customer support system. The retailer is replacing their old-school phone menus with an AI-powered voice agent to provide support for custom
     URL: https://nypost.com/2026/04/23/lifestyle/home-depot-says-bye-to-a-traditional-customer-service-feature/
[16] Tavily [Tue, 14 Ap]: # Spruce Up Your Space for Up to 40% Off With Home Depot’s Spring Black Friday Sale. See at The Home Depot"). Home Depot is having a Spring Black Friday sale") running until **April 22**. For one, Home Depot is offering select appliances for up to 40% off"). Save up to 40% at Home Depot") See at Hom
     URL: https://www.cnet.com/deals/home-depot-spring-black-friday-deals/

##### TAVILY GUIDANCE (≤90d) (5 hits)
[17] Tavily [Sun, 08 Ma]: # DIY Doldrums Overshadow Home Depot, Lowe's. overstretched budgets, and Home Depot and Lowe’s are feeling the pinch. At Home Depot, sales for the fiscal fourth quarter fell 3.8% to $38.2 billion, with some of that decline. And it reiterated its forecast for the full year ahead, expecting sales to r
     URL: https://www.mediapost.com/publications/article/413074/diy-doldrums-overshadow-home-depot-lowes.html?edition=141804
[18] Tavily [Tue, 31 Ma]: You are in: Home » Marketplaces » **Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround**. # Debenhams Group smashes FY26 guidance as marketplace model accelerates turnaround. The Group’s trading statement for the financial year ending 28 February 2026 shows £53m in adj
     URL: https://internetretailing.net/debenhams-group-smashes-fy26-guidance-as-marketplace-model-accelerates-turnaround/
[19] Tavily [Sat, 14 Ma]: “Focus on Improving Customer Experience”: Home Depot Stock (NYSE:HD) Notches Up as Live Tracking Gets Fleshed Out. HD](/news/focus-on-improving-customer-experience-home-depot-stock-nysehd-notches-up-as-live-tracking-gets-fleshed-out "HD"). # “Focus on Improving Customer Experience”: Home Depot Stock
     URL: https://www.tipranks.com/news/bitcoin-stands-strong-at-71000-as-trump-warns-of-attacks-on-irans-crown-jewel
[20] Tavily [Thu, 26 Ma]: You are in: Home » News » **Record second half sees THG return to growth and strengthen FY26 guidance**. # Record second half sees THG return to growth and strengthen FY26 guidance. THG delivered a strong FY25 performance that saw it return to growth after a shaky H1, with a re

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\HD_COUNCIL.md`)_

#### — · Story
_source: `dossiers\HD_STORY.md` (now in cemetery)_

#### Home Depot — HD

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

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/HD_2026-05-01.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 164.7 bi · EBITDA est. R$ 23.12 bi · FCF R$ 12.65 bi · ROE 146% · DGR 15.4% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 4/9 · Altman Z=5.71 (safe) · Beneish M=-2.42 (clean) |
| **5 — Classification** | Modo A-US · Buffett/Quality (4/12) |
| **5.5 — Council Debate** | HOLD (high) · 2 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. O Home Depot, uma empresa líder no setor de varejo de materiais para construção e ferramentas domésticas, é conhecida por seu amplo catálogo que atende tanto aos profissionais do setor quanto ao consumidor final. Com lojas espalhadas pelos Estados Unidos e Canadá, a empresa oferece uma variedade de produtos, desde madeira e ferragens até equipamentos para jardinagem e manutenção residencial.

Um dos principais desafios que o Home Depot enfrenta é evitar que os investidores confundam sua marca com seu negócio. A reputação da empresa como um fornecedor líder não deve obscurecer a necessidade de inovação constante em termos de serviços ao cliente e eficiência operacional para manter-se competitiva frente às mudanças no comportamento do consumidor e à crescente concorrência online.

Recentemente, o Home Depot tem se destacado por iniciativas como a construção de um centro de distribuição que oferecerá entregas no mesmo dia e no dia seguinte em Yaphank, Nova York. Essa medida reflete uma resposta estratégica às demandas do mercado moderno por conveniência e rapidez na entrega.

No entanto, o Home Depot também enfrentou desafios operacionais, como a prisão de um gerente da loja em Florida acusado de conceder descontos não autorizados no valor de mais de 4 milhões de dólares para aumentar suas vendas. Esses incidentes podem afetar a confiança dos consumidores e criar custos adicionais relacionados à recuperação desses erros.

##### Ato 2 — O Contexto

O cenário macroeconômico atual é caracterizado por taxas de juros elevadas, com o Fed Funds entre 4.25% e 4.50%, e a taxa do Tesouro dos EUA de 10 anos em torno de 4.2%. O custo do capital próprio (Ke) está estimado em aproximadamente 10%. A economia encontra-se no final da expansão, com sinais de enfraquecimento emergindo.

Para o setor de varejo de materiais para construção e ferramentas domésticas, essas condições desafiadoras podem resultar em uma diminuição do gasto dos consumidores, especialmente aqueles que estão sobrecarregados financeiramente. Isso é particularmente relevante para empresas como o Home Depot, cujas vendas no quarto trimestre de 2025 caíram 3.8% para US$ 38.2 bilhões, refletindo a pressão sobre os orçamentos domésticos.

A pressão sobre as vendas do Home Depot é um reflexo direto das dificuldades enfrentadas pelo setor de construção residencial e reforma domiciliar. A falta de atividade na construção residencial, combinada com o aumento dos custos de vida, tem limitado a demanda por produtos da empresa.

Além disso, as recentes notícias sobre fraudes internas podem ter um impacto negativo adicional nos resultados financeiros e na reputação da empresa. A necessidade de lidar com esses problemas enquanto se adapta às mudanças no comportamento do consumidor e à concorrência online torna o cenário ainda mais desafiador para a Home Depot.

Em suma, o contexto macroeconômico atual apresenta um ambiente hostil para empresas como o Home Depot. A necessidade de inovação contínua em serviços ao cliente, eficiência operacional e adaptação às mudanças no comportamento do consumidor é crucial para a sobrevivência e sucesso da empresa neste ciclo econômico incerto.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa de crescimento e desafios. A tabela anual abaixo ilustra as principais métricas financeiras do período:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2022 | — | — | — | — | — | — | — |
| 2023 | R$ 157.40B | R$ 24.09B | R$ 26.50B | 16.8% | R$ 17.11B | 10.9% | R$ 11.50B |
| 2024 | R$ 152.67B | R$ 21.87B | R$ 24.05B | 15.8% | R$ 15.14B | 9.9% | R$ 17.95B |
| 2025 | R$ 159.51B | R$ 21.73B | R$ 23.90B | 15.0% | R$ 14.81B | 9.3% | R$ 16.32B |
| 2026 | R$ 164.68B | R$ 21.01B | R$ 23.12B | 14.0% | R$ 14.16B | 8.6% | R$ 12.65B |

A receita da empresa apresentou um crescimento anual composto (CAGR) de aproximadamente 1,7% entre os anos de 2023 e 2026, com picos em 2025 e 2026. No entanto, a margem EBITDA da empresa diminuiu ligeiramente ao longo do período, refletindo um aumento nas despesas operacionais ou uma redução na eficiência operacional.

O fluxo de caixa livre (FCF) demonstrou variações significativas. Em 2023 e 2024, o FCF foi positivo e crescente, mas em 2025 houve um declínio moderado que se acentuou em 2026. Este comportamento sugere uma maior necessidade de reinvestimento ou despesas não operacionais.

A distribuição de dividendos tem sido consistente ao longo dos anos, com o total proventos por ação aumentando gradualmente desde 2023 até 2025, mas caindo significativamente em 2026. A tabela abaixo ilustra essa evolução:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 4.500 |
| 2021 | 6.600 |
| 2022 | 7.600 |
| 2023 | 8.360 |
| 2024 | 9.000 |
| 2025 | 9.200 |
| 2026 | 2.330 |

O Dividend Growth Rate (DGR) da empresa, calculado a partir dos dividendos reportados e ajustado para extraordinários, foi de 15,4% ao ano. No entanto, o declínio significativo em 2026 indica que os dividendos podem não ser estruturalmente sustentáveis no longo prazo.

A relação entre dividend yield (DY) total reportado e DY estrutural é crucial para avaliar a consistência dos dividendos. Dada a queda abrupta em 2026, é evidente que o DY total reportado não reflete uma tendência estrutural de distribuição de lucros.

Lucro contábil pode esconder provisões e ajustes; FCF, não. O fluxo de caixa livre (FCF) fornece um indicador mais preciso da geração de valor operacional da empresa e é crucial para sustentar a política de dividendos em longo prazo.

##### Ato 4 — O Balanço

O balanço financeiro da empresa no final de 2026 apresenta uma série de métricas que ajudam a entender o estado atual do negócio. Com um preço de mercado de R$ 328,80 por ação e um EBITDA estimado de R$ 23,12 bilhões para o último ano, as principais métricas são:

- **P/E:** 23,09
- **P/B:** 25,56
- **DY:** 2,81%
- **ROE:** 145,54%
- **ND/EBITDA:** 1,41 (Net Debt estimado: R$ 32,67 bilhões / EBITDA mais recente de R$ 23,12 bilhões)
- **DivStreak:** 40 anos
- **Receita (último ano):** R$ 164,68 bilhões

O ROE da empresa, que atingiu 145,54%, supera significativamente o custo de capital próprio estimado no Brasil (~18,25%), indicando que a empresa está criando valor para os acionistas. No entanto, é importante notar que a alavancagem da dívida (Net Debt/EBITDA) aumentou ligeiramente em 2026, o que pode ser um ponto de atenção se continuar a crescer.

A relação entre dividend yield e dividend growth rate sugere uma consistência na política de distribuição de lucros, mas é crucial monitorar os níveis de alavancagem financeira para garantir que não comprometam a sustentabilidade dos dividendos no longo prazo.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa em questão revela uma posição distinta no mercado tanto em termos de valorização relativa quanto de rendimento. O preço-lucro (P/E) atualmente está em 23,09x, um pouco acima do múltiplo médio setorial de 22,37x e da média do índice Ibov/S&P de 21,00x. Este indicador sugere que os investidores estão dispostos a pagar mais por cada real de lucro futuro em relação ao consenso do mercado.

O preço-benefício (P/B) é ainda mais notável, com uma avaliação de 25,56x contra a média setorial de 3,47x e o índice Ibov/S&P de 3,50x. Este múltiplo elevado pode indicar que os investidores atribuem um alto valor à marca ou ao potencial de crescimento futuro da empresa em relação aos seus ativos líquidos.

O dividendo yield (DY) reportado é de 2,8%, ligeiramente superior à média setorial de 2,5% e significativamente acima do índice Ibov/S&P que registra 1,5%. No entanto, é importante notar que o DY pode incluir dividendos extraordinários ou não refletir a tendência estrutural da política de distribuição de rendimentos. Uma análise mais detalhada revela que este yield elevado pode ser temporário e não necessariamente indicativo do potencial futuro de geração de lucros.

O retorno sobre o patrimônio líquido (ROE) é impressionante, com uma taxa de 145,5%, muito acima da média setorial de 14,5% e do índice Ibov/S&P que registra 16,0%. Este indicador sugere uma eficiência operacional excepcional na geração de lucros em relação ao capital próprio.

A relação negócios/disponibilidade de caixa (ND/EBITDA) é de 2,58x, ligeiramente inferior à média setorial de 2,99x. Este indicador sugere que a empresa está gerando caixa operacional mais eficientemente em comparação com seus pares.

A tabela abaixo resume estes múltiplos e fornece uma base para comparações mais detalhadas:

| Múltiplo | HD | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 23.09x | 22.37x | 21.00x |
| P/B | 25.56x | 3.47x | 3.50x |
| DY | 2.8% | 2.5% | 1.5% |
| FCF Yield | 3.7% | — | 4.0% |
| ROE | 145.5% | 14.5% | 16.0% |
| ND/EBITDA | 2.58x | 2.99x | — |

##### Ato 6 — Os Quality Scores

A avaliação dos scores de qualidade da empresa oferece uma perspectiva complementar sobre a solidez financeira e operacional. O Piotroski F-Score, que mede a saúde financeira baseada em nove critérios contábeis, registra um score de 4/9 para o período encerrado em 2026-01-31. Este resultado sugere uma situação mista: enquanto alguns indicadores sugerem fortalecimento financeiro, outros apontam para fraquezas operacionais.

O Altman Z-Score, que é um modelo preditivo de falência, registra um valor de 5,71, classificado na zona segura com alta confiança. Este indicador sugere uma baixa probabilidade de insolvência nos próximos dois anos, embora seja importante notar que o Z-Score conservador e ajustado para Brasil (BR) possa oferecer insights adicionais.

O M-score do Beneish, um modelo utilizado para detectar manipulação contábil, registra -2,42, indicando uma zona de "clean" com alta confiança. Este resultado sugere que não há evidências significativas de manipulação financeira na empresa.

Em resumo, os scores de qualidade apontam para um perfil sólido e transparente da empresa, embora algumas áreas operacionais possam requerer atenção adicional conforme indicado pelo Piotroski F-Score.

---

##### Ato 7 — O Moat e a Gestão

A Home Depot é uma empresa que opera em um setor altamente competitivo, mas possui um moat substancial devido à sua escala operacional, eficiência logística e forte reputação no mercado. Este moat permite que a companhia mantenha margens superiores às da concorrência e gere retornos sobre o capital empregado (ROE) consistentemente elevados.

###### Moat

O moat da Home Depot é classificado como **Wide**. A empresa possui um conjunto diversificado de barreiras competitivas que incluem:

1. **Custo/escala**: Com uma presença geográfica extensa e uma base de clientes sólida, a Home Depot beneficia de economias de escala significativas em suas operações logísticas e compras.
2. **Switching costs**: A Home Depot oferece um amplo catálogo de produtos e serviços personalizados que criam altos custos de mudança para os consumidores que buscam alternativas.
3. **Eficiência**: A empresa tem investido pesadamente em tecnologia para melhorar a eficiência operacional, incluindo sistemas avançados de gerenciamento de estoque e entrega rápida.
4. **Intangíveis**: A marca Home Depot é reconhecida internacionalmente como sinônimo de qualidade e confiabilidade no setor de materiais de construção.

###### Gestão

A gestão da Home Depot tem sido consistente ao longo dos anos, com uma história ininterrupta de dividendos que remonta a quarenta anos. No entanto, recentes escândalos operacionais têm levantado preocupações sobre a governança interna e a cultura corporativa.

Em relação à posse interna (insider ownership), os dados não estão disponíveis para esta análise. Além disso, as transações internas dos últimos seis meses também não foram mencionadas nos fatos web fornecidos.

###### Escândalos Operacionais

Recentemente, um gerente da Home Depot em Florida foi acusado de conceder descontos não autorizados no valor de quatro milhões de dólares para aumentar suas vendas e receber bônus mais altos. Este tipo de comportamento ilícito pode ter impacto negativo na reputação da empresa e nos custos operacionais, além de potencialmente comprometer a confiança dos investidores.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico computado para a Home Depot é Buffett/Quality (4/12), com as seguintes pontuações:
- **VALUE**: +2 · ROE 146% > Ke (18.2%)
- **GROWTH**: +1 · Yield baixo (<3%) + ROE alto → reinvestimento alto
- **DIVIDEND**: +2 · Histórico ininterrupto de 40 anos ≥ 5
- **BUFFETT**: +2 · ROE 146% > 15% (proxy ROIC alto) +1 · Beneish M=-2.42 clean (sem manipulação) +1 · Streak 40 anos ≥ 10 (consistência)

###### O que o preço desconta
O preço atual da Home Depot, de R$328.80 por ação, reflete uma avaliação acima da média do setor, com um P/E de 23.09x e um P/B de 25.56x. Isso sugere que os investidores estão descontando um crescimento sustentável e robusto nos próximos anos.

###### O que os fundamentos sugerem
Os fundamentos da Home Depot são fortes, com um ROE elevado e uma história consistente de dividendos. No entanto, a sobreavaliação dos múltiplos P/E e P/B em comparação com o setor pode indicar riscos associados à sustentabilidade desses níveis.

###### DCF — A âncora do valor
A avaliação através da metodologia de fluxo descontado (DCF) indica que a Home Depot está atualmente sobreavaliada, com uma margem de segurança negativa em relação ao cenário base. A tabela abaixo resume os resultados:

| Cenário | Crescimento 5y | Perpetuidade | Valor por ação |
|---|---|---|---|
| Pessimista | 5% a.a. | 3% | R$ 203.49 

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\HD_STORY.md`)_

#### — · Other
_source: `hubs\HD.md` (now in cemetery)_

#### HD — Home Depot

> **Hub consolidado**. Tudo o que existe no vault sobre HD, em ordem cronológica. Cada link aponta para o ficheiro original que ficou na sua pasta — esta é a porta de entrada matinal.

`sector: Consumer Disc.` · `market: US` · `currency: USD`

##### 🎯 Hoje

- **Posição**: 1.0 @ entry 292.02
- **Verdict (DB)**: `HOLD` (score 5.95, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 21.28 · P/B 23.52 · DY 3.1% · ROE 145.5% · ND/EBITDA 2.58 · Dividend streak 40 · Aristocrat yes

##### 📜 Histórico (chronological journal)

> Como a vista sobre este nome evoluiu — do primeiro screen ao deepdive mais recente. Útil para perceber **o que sabíamos antes vs o que sabemos agora**.


###### 2026

- **2026-05-19** · Earnings Prep → [[earnings_prep_HD_2026-05-19]] _(`briefings/earnings_prep_HD_2026-05-19.md`)_
- **2026-05-13** · Overnight → [[HD]] _(`Overnight_2026-05-13/HD.md`)_
- **2026-05-11** · Overnight → [[HD]] _(`Overnight_2026-05-11/HD.md`)_
- **2026-05-01** · Dossier Archive → [[HD_STORY_2026-05-01]] _(`dossiers/archive/HD_STORY_2026-05-01.md`)_
- **2026-05-01** · Review · Valentina Prudente → [[HD_2026-05-01]] _(`agents/Valentina Prudente/reviews/HD_2026-05-01.md`)_
- **2026-05-01** · Review · Pedro Alocação → [[HD_2026-05-01]] _(`agents/Pedro Alocação/reviews/HD_2026-05-01.md`)_
- **2026-05-01** · Review · Mariana Macro → [[HD_2026-05-01]] _(`agents/Mariana Macro/reviews/HD_2026-05-01.md`)_
- **2026-05-01** · Review · Charlie Compounder → [[HD_2026-05-01]] _(`agents/Charlie Compounder/reviews/HD_2026-05-01.md`)_

###### 2017

- **2017-08-22** · Filing → [[HD_FILING_2017-08-22]] _(`dossiers/HD_FILING_2017-08-22.md`)_

###### (undated)

- **—** · Wiki → [[HD]] _(`wiki/holdings/HD.md`)_
- **—** · Variant → [[HD_VARIANT]] _(`tickers/HD_VARIANT.md`)_
- **—** · Story → [[HD_STORY]] _(`dossiers/HD_STORY.md`)_
- **—** · Panorama → [[HD]] _(`tickers/HD.md`)_
- **—** · Other → [[HD]] _(`hubs/HD.md`)_
- **—** · Ic Debate → [[HD_IC_DEBATE]] _(`tickers/HD_IC_DEBATE.md`)_
- **—** · Drip → [[HD_drip]] _(`briefings/drip_scenarios/HD_drip.md`)_
- **—** · Deepdive → [[HD_DOSSIE]] _(`tickers/HD_DOSSIE.md`)_
- **—** · Council → [[HD_COUNCIL]] _(`dossiers/HD_COUNCIL.md`)_

##### 🗂️ Artefactos por categoria

###### Panorama
- [[HD]] _(`tickers/HD.md`)_

###### Deepdive (DOSSIE)
- [[HD_DOSSIE]] _(`tickers/HD_DOSSIE.md`)_

###### Story
- [[HD_STORY]] _(`dossiers/HD_STORY.md`)_

###### Council aggregate
- [[HD_COUNCIL]] _(`dossiers/HD_COUNCIL.md`)_

###### Council reviews por persona

_Charlie Compounder_:
- [[HD_2026-05-01]] _(`agents/Charlie Compounder/reviews/HD_2026-05-01.md`)_

_Mariana Macro_:
- [[HD_2026-05-01]] _(`agents/Mariana Macro/reviews/HD_2026-05-01.md`)_

_Pedro Alocação_:
- [[HD_2026-05-01]] _(`agents/Pedro Alocação/reviews/HD_2026-05-01.md`)_

_Valentina Prudente_:
- [[HD_2026-05-01]] _(`agents/Valentina Prudente/reviews/HD_2026-05-01.md`)_

###### IC Debate (synthetic)
- [[HD_IC_DEBATE]] _(`tickers/HD_IC_DEBATE.md`)_

###### Variant perception
- [[HD_VARIANT]] _(`tickers/HD_VARIANT.md`)_

###### Filings individuais
- [[HD_FILING_2017-08-22]] _(`dossiers/HD_FILING_2017-08-22.md`)_

###### Overnight scrapes
- [[HD]] _(`Overnight_2026-05-13/HD.md`)_
- [[HD]] _(`Overnight_2026-05-11/HD.md`)_

###### DRIP scenarios
- [[HD_drip]] _(`briefings/drip_scenarios/HD_drip.md`)_

###### Earnings prep briefs
- [[earnings_prep_HD_2026-05-19]] _(`briefings/earnings_prep_HD_2026-05-19.md`)_

###### Wiki / playbooks
- [[HD]] _(`wiki/holdings/HD.md`)_

###### Archived stories
- [[HD_STORY_2026-05-01]] _(`dossiers/archive/HD_STORY_2026-05-01.md`)_

###### Other
- [[HD]] _(`hubs/HD.md`)_

##### ⚙️ Refresh commands

```bash
ii panorama HD --write       # aggregator (verdict+peers+notes+videos)
ii deepdive HD --save-obsidian # V10 4-layer pipeline
ii verdict HD --narrate --write
ii fv HD                      # fair value (Buffett-Graham conservative)
python -m analytics.fair_value_forward --ticker HD # quality-aware forward
```

---

_Regenerado por `scripts/build_ticker_hubs.py`. Run novamente para refresh._

#### — · Panorama
_source: `tickers\HD.md` (now in cemetery)_

#### HD — Home Depot

#holding #us #consumer_disc.

##### 🎯 Verdict — 🟡 WATCH

> **Score**: 6.5/10  |  **Confiança**: 70%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 7.7/10 | 35% | `████████░░` |
| Valuation  | 8.0/10 | 30% | `████████░░` |
| Momentum   | 4.0/10 | 20% | `████░░░░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z 5.711518479962093 (SAFE), Piotroski 4/9 (NEUTRAL), DivSafety 80.0/100
- **Valuation**: Screen 0.60, DY percentil P96 (CHEAP)
- **Momentum**: 1d 2.42%, 30d -4.87%, YTD -6.58%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- valuation atractiva mas quality ou momentum fraco
- valuation barato
- DY percentil P96 (historicamente CHEAP)

##### Links

- Sector: [[sectors/Consumer_Disc.|Consumer Disc.]]
- Market: [[markets/US|US]]
- Peers: [[TSLA]] · [[GPC]] · [[LEG]] · [[LOW]] · [[MCD]]
- 🎯 **Thesis**: [[wiki/holdings/HD|thesis deep]]

##### Snapshot

- **Preço**: $323.05  (2026-05-06)    _+2.42% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: 5.712 (safe)
- **Piotroski**: 4/9
- **Div Safety**: 80.0/100 (SAFE)
- **Posição**: 1.0 sh @ $292.02  →  P&L 10.63%

##### Fundamentals

- P/E: 22.702038 | P/B: 25.112717 | DY: 2.86%
- ROE: 145.54% | EPS: 14.23 | BVPS: 12.864
- Streak div: 40y | Aristocrat: True

##### Dividendos recentes

- 2026-03-12: $2.3300
- 2025-12-04: $2.3000
- 2025-09-04: $2.3000
- 2025-06-05: $2.3000
- 2025-03-13: $2.3000

##### Eventos (SEC/CVM)

- **2026-04-07** `proxy` — DEF 14A
- **2026-03-18** `10-K` — 10-K
- **2026-02-24** `8-K` — 8-K | 2.02,9.01
- **2025-11-25** `10-Q` — 10-Q
- **2025-11-24** `8-K` — 8-K | 5.03,8.01,9.01

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -23.70%
- **Drawdown 5y**: -25.11%
- **YTD**: -6.58%
- **YoY (1y)**: -10.11%
- **CAGR 3y**: +3.71%  |  **5y**: -0.97%  |  **10y**: +9.06%
- **Vol annual**: +24.19%
- **Sharpe 3y** (rf=4%): -0.01

###### Dividendos
- **DY 5y avg**: +2.28%
- **Div CAGR 5y**: +8.66%
- **Frequency**: quarterly
- **Streak** (sem cortes): 29 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2022-01-31 | n/a | n/a | n/a |
| 2023-01-31 | $157.40B | $17.11B | $11.50B |
| 2024-01-31 | $152.67B | $15.14B | $17.95B |
| 2025-01-31 | $159.51B | $14.81B | $16.32B |
| 2026-01-31 | $164.68B | $14.16B | $12.65B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "HD — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: HD
    data: [364.86, 372.81, 377.05, 370.4, 367.96, 367.33, 363.16, 347.03, 361.86, 373.16, 367.5, 370.11, 359.4, 373.09, 372.08, 385.41, 387.53, 399.38, 397.7, 408.24, 407.71, 415.34, 422.71, 415.69, 407.45, 397.02, 386.81, 379.37, 391.9, 385.03, 378.04, 383.08, 370.43, 362.36, 332.38, 355.47, 357.91, 345.27, 356.99, 345.0, 349.78, 345.82, 359.56, 375.95, 384.64, 380.36, 378.12, 385.15, 390.22, 378.58, 375.57, 366.92, 353.56, 339.03, 328.21, 332.51, 328.89, 318.77, 341.16, 349.4, 340.16, 329.06, 312.42]
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
    data: [23.780943, 23.800774, 23.692904, 24.571026, 24.460688, 24.185654, 23.620956, 23.587782, 23.587782, 23.335674, 23.140646, 22.701124, 23.089888, 21.970465, 22.181435, 22.702038]
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
    data: [145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54, 145.54]
  - title: DY %
    data: [2.72, 2.75, 2.76, 2.67, 2.67, 2.68, 2.75, 2.75, 2.75, 2.78, 2.8, 2.86, 2.81, 2.95, 2.93, 2.86]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\HD_DOSSIE.md` (now in cemetery)_

#### 📑 HD — Home Depot

> Generated **2026-04-26** by `ii dossier HD`. Cross-links: [[HD]] · [[HD_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

HD negoceia P/E 23.59, DY 2.75% e ROE 145.5% (alavancado pelo buyback agressivo a comprimir equity) com streak dividendos 40y — Aristocrat genuíno. IC verdict **HOLD** (medium confidence, 60% consensus); YoY -6.1% reflecte housing turnover deprimido pelo ciclo de juros US. DRIP candidate sólido: Aristocrat + DY 2.75% qualifica screen US, manter para reinvestimento em weakness.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 14.24  |  **BVPS**: 12.86
- **ROE**: 145.54%  |  **P/E**: 23.59  |  **P/B**: 26.11
- **DY**: 2.75%  |  **Streak div**: 40y  |  **Market cap**: USD 334.56B
- **Last price**: USD 335.89 (2026-04-26)  |  **YoY**: -6.1%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[HD_IC_DEBATE]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 23.59** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 23.59** esticado vs critério.
- **P/B = 26.11** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **26.11** esticado.
- **DY = 2.75%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **2.75%** OK.
- **ROE = 145.54%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **145.54%** compounder-grade.
- **Graham Number ≈ R$ 64.19** vs preço **R$ 335.89** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 40y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

###### Conceitos relacionados

- 💰 **Status DRIP-friendly** (US holding com DY ≥ 2.5%) — ver [[Glossary/DRIP]] para mecanismo + [[Glossary/Aristocrat]] para membership formal.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 3. Riscos identificados

- 🔴 **Housing turnover deprimido** — existing home sales em mínimos multi-anos pesa em remodels e Pro mix. Trigger: NAR existing home sales < 4M annualized por 6m.
- 🟡 **Lumber / commodity inflation** — comprime gross margin se input prices não puderem ser repassados. Trigger: lumber futures > +30% YoY + GM < 33%.
- 🟡 **Pro vs DIY mix** — Pro segment é mais cíclico mas higher-ticket; perda de share para Lowe's. Trigger: comp sales Pro < DIY por 2 quarters.
- 🟢 **Aristocrat streak (40y)** — robusto mas qualquer corte seria evento gigante; P/E 23 acima do screen US (≤20). Trigger: `fundamentals.dy < 2.0%` ou anúncio de freeze de dividendo em 8-K.

##### 4. Position sizing

**Status atual**: holding (in portfolio)

**HOLD com bias de DRIP** — Aristocrat 40y + DY 2.75% qualifica para reinvestimento automático (USD permanece em US). P/E 23.59 ligeiramente acima do screen US (≤20), por isso evitar aumentos agressivos a estes níveis; preferir adds em pull-backs (P/E < 20 ou DY > 3%). Sizing prudente até 6-8% do US book.

##### 5. Tracking triggers (auto-monitoring)

- `fundamentals.dy < 2.0%` → quebra screen US (DY ≥ 2.5%), reavaliar.
- `fundamentals.pe > 27` → premium injustificado vs hist 20-23.
- Comp sales YoY < -3% por 2 trimestres → housing turnover a romper.
- Streak break (`fundamentals.dividend_streak_years` reset) → Aristocrat status perdido, exit imediato.
- `conviction_scores.score < 60` → tese DRIP a degradar.

##### 6. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier HD` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

#### — · IC Debate (synthetic)
_source: `tickers\HD_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — HD

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 4.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Preço elevado (PE, PB)
- ROE alto mas dependente de goodwill
- Recentes notícias negativas

**Key risk**: Gestão e controles internos questionáveis após escândalos recentes

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- PE e PB elevados
- Notícias negativas recentes sobre gerenciamento
- Parceria em risco

**Key risk**: Gerente de Home Depot acusado de desconto ilegal pode indicar gestão fraca

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E e P/B elevados sugerem sobreavaliação
- Renda fixa atrativa, mas não compensa o risco
- Parceiros em falência indicam fragilidade

**Key risk**: Exposição a parceiros frágeis e potencial de fraudes internas

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Valuation too high (PE, PB)
- Recent negative news impacts perception
- High intangibles suggest potential write-downs

**Key risk**: Permanent loss of capital due to overvaluation and operational risks

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- Fundamentos mistos
- Notícias recentes negativas
- Parceria com The Weather Company positiva

**Key risk**: Gerenciamento de risco e integridade operacional em questão após incidente do gerente

##### 📊 Context provided

```
TICKER: US:HD

FUNDAMENTALS LATEST:
  pe: 22.308504
  pb: 24.677395
  dy: 2.91%
  roe: 145.54%
  net_debt_ebitda: 2.579664948386075
  intangible_pct_assets: 31.1%   (goodwill $22.3B + intangibles $10.3B)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Florida Home Depot manager arrested for allegedly dishing out $4M in ‘unauthorized’ discounts to boost his sales - New Y [Sat, 25 Ap]
    # Florida Home Depot manager arrested for allegedly dishing out $4M in ‘unauthorized’ discounts to boost his sales. A Florida Home Depot manager was arrested on felony charges after allegedly dishing 
  - Home Depot partner files for bankruptcy and closes US stores — leaving customers with thousands of dollars at stake - Ne [Tue, 28 Ap]
    # Home Depot partner files for bankruptcy and closes US stores — leaving customers with thousands of dollars at stake. Wren Kitchens, a Home Depot partner brand, filed for bankruptcy and abruptly clos
  - Home Depot helps advertisers reach DIY audiences on Reddit and Pinterest - Retail Dive [Wed, 29 Ap]
    * Home Depot is bringing several new advertising capabilities to its retail media network, including what the home-improvement retailer bills as an industry-first integration with Reddit, according to
  - Why Home Depot built its marketing around the forecast - The Drum [Tue, 05 Ma]
    **A partnership with The Weather Company is replacing the retail calendar with real-time atmospheric signals, driving conversion rates six times higher than standard seasonal pushes.**. That’s the pre
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

#### — · Variant perception
_source: `tickers\HD_VARIANT.md` (now in cemetery)_

#### 🎯 Variant Perception — HD

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `unmeasurable` (magnitude 0/5)  
**Interpretation**: missing thesis or no analyst data

##### 📜 Our thesis

**Core thesis (2026-04-25)**: Home Depot é um líder estabelecido no setor de varejo de materiais para construção, com uma sólida história de crescimento e distribuição de dividendos. Apesar do P/E (23.62) estar ligeiramente acima da média recomendada pela filosofia de investimento, a empresa mantém um ROE elevado de 145.54%, além de ser uma Dividend Aristocrat com 40 anos consecutivos de dividendos.

**Key assumptions**:
1. Home Depot continuará a crescer organicamente e expandir sua presença no mercado, especialmente em mercados suburbanos emergentes
2. A empresa manterá seu forte histórico de distribuição de dividendos e potencial para aumentar os dividendos futuros
3. O setor de materiais para construção continuará a se beneficiar da recuperação econômica e do crescimento populacional n

---
*100% Ollama local. Variant perception scan.*

#### — · Wiki playbook
_source: `wiki\holdings\HD.md` (now in cemetery)_

#### 🎯 Thesis: [[HD]] — Home Depot

> #1 US home improvement retail. Secular housing + DIY + Pro customer tailwinds. Dividend growth 14y+.

##### Intent
**DRIP core** (borderline staple for consumer disc sector). Reinvest dividends.

##### Business snapshot
- #1 US home improvement (#2 Lowe's).
- 2,300+ big-box stores US + Canada + Mexico.
- Revenue ~$160B/y.
- **Two customers**:
  - **DIY** (~55% revenue) — homeowners doing projects
  - **Pro** (~45%) — contractors, tradespeople (high-frequency, sticky)

##### Por que detemos

1. **#1 market share** — scale advantages vs Lowe's distant #2.
2. **Pro customer growing** — stickier + higher basket.
3. **Dividend growth 14y+** consistent.
4. **Operating margin 14-15%** — industry-leading.
5. **Buyback aggressive** reducing share count.
6. **Secular housing** — US housing under-built 5-7M homes vs need.
7. **Ageing housing stock** — maintenance demand steady.

##### Moat

- **Scale** — purchasing power + distribution.
- **Real estate** — locked-in prime big-box locations.
- **Pro customer ecosystem** — HD account, credit terms, bulk delivery.
- **Brand + trust** — category default.
- **Weak moat**: Amazon + DTC players nibbling small-ticket items.

##### Current state (2026-04)

- **Housing slowdown** — high mortgage rates → turnover down → repairs + renovations down marginally.
- DIY softer (post-COVID normalization).
- Pro resilient.
- Digital platform growing (HD Supply reintegrated).
- SRS Distribution acquisition 2024 — roofing/landscaping Pro channel boost.
- Margin pressure from mix (Pro = lower margin than DIY).

##### Invalidation triggers

- [ ] Same-store sales (comps) declining > 5% 2 years
- [ ] Market share losing > 100bp to Lowe's
- [ ] Operating margin < 12%
- [ ] Dividend growth < 5%/y sustained (slowdown signal)
- [ ] Major housing crisis (-30% housing starts 2 years)
- [ ] CEO Ted Decker departure + strategy pivot

##### Sizing

- Posição actual: 1 share
- Target 2-4% sleeve US
- Reinvest dividends

##### HD vs LOW

| Trait | HD | LOW |
|---|---|---|
| Market share | #1 (~30%) | #2 (~20%) |
| Pro mix | ~45% | ~25% |
| Op margin | 14-15% | 12-13% |
| ROIC | 40%+ | 30%+ |
| DY | 2.5% | 2.0% |
| Streak | 14y | 61y (aristocrat!) |

LOW has longer streak (aristocrat) despite smaller; HD has better economics. Trade-off.


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -19.87%
- **Drawdown 5y**: -21.34%
- **YTD**: -1.89%
- **YoY (1y)**: -4.80%
- **CAGR 3y**: +4.00%  |  **5y**: +0.93%  |  **10y**: +9.60%
- **Vol annual**: +24.10%
- **Sharpe 3y** (rf=4%): -0.00

###### Dividendos
- **DY 5y avg**: +2.28%
- **Div CAGR 5y**: +8.66%
- **Frequency**: quarterly
- **Streak** (sem cortes): 29 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Moat_types]] — scale + network (Pro customer stickiness)
- [[wiki/tax/Dividend_withholding_BR_US]] — tax 30% US withhold

## ⚙️ Refresh commands

```bash
ii panorama HD --write
ii deepdive HD --save-obsidian
ii verdict HD --narrate --write
ii fv HD
python -m analytics.fair_value_forward --ticker HD
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
