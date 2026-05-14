---
type: ticker_hub
ticker: JPM
market: us
sector: Financials
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 16
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# JPM — JPMorgan Chase

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: holdings` · `16 sources merged`

## 🎯 Hoje

- **Posição**: 7.0 @ entry 306.55571428571426
- **Verdict (DB)**: `HOLD` (score 5.98, 2026-05-13)
- **Último deepdive**: `JPM_deepdive_20260509_1437.json` (2026-05-09 14:37)
- **Fundamentals** (2026-05-13): P/E 14.38 · P/B 2.34 · DY 2.0% · ROE 16.5% · Dividend streak 43 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\JPM.md` (cemetery archive)_

#### JPM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (2):
  - https://www.jpmorganchase.com/ir
  - https://www.jpmorganchase.com/ir/quarterly-earnings
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=7.0 · entry=306.55571428571426 · date=2025-09-25

- Total events na DB: **28**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=300.0
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.16465001 · DY=0.01966666666666667 · P/E=14.367817
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 3.03,5.03,8.01,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-24 | 8-K | sec | 8-K \| 5.03 |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,9.01 |

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
_generated 2026-05-09 14:37 · source: `reports/deepdive/JPM_deepdive_20260509_1437.json`_

> Sector: ? · Country: ? · Price: ? 

**Quality scores**

| Score | Valor | Zona |
|---|---|---|
| Piotroski | -/9 | - |
| Altman Z | - | - |
| Beneish M | - | - |
| Moat | -/10 | N/A |


**Fundamentals**: P/E - · P/B - · EV/EBITDA - · DY - · ROE -

**Delta vs análise anterior**

```
Delta Report — JPM | hoje vs run anterior (2026-05-08)
```

**Strategist dossier**

# 1. Executive Summary
- **Rating:** EVITAR
- **Preço justo estimado e upside/downside %:** Não possível calcular devido à falta de dados quantitativos.
- **Risk Score:** 10 (Altíssimo)
- **Alerta vermelho:** Dados insuficientes para avaliar o Beneish M-Score ou Altman Z-Score, impossibilitando uma análise completa do risco.

# 2. O Negócio
- **Modelo de receita e fontes de caixa:** Não disponível.
- **Moat (Network Effect / Switching Costs / Intangibles / Cost Adv):** Não possível avaliar sem dados específicos sobre o negócio da empresa.

# 3. Decomposição DuPont
- **ROE = Margem × Giro × Alavancagem:** Dados insuficientes para calcular.
- **Identificar a alavanca dominante:** Não disponível devido à falta de dados financeiros.

# 4. Valuation Multinível
- **Graham Number:** Não aplicável sem informações específicas sobre o lucro por ação e P/B da empresa.
- **DCF com 3 cenários (Bear / Base / Bull):** Impossível realizar sem dados financeiros futuros, incluindo fluxo de caixa livre projetado.
- **EV/EBITDA vs mediana setor:** Não possível comparar sem informações sobre o múltiplo EV/EBITDA da empresa e do setor.

# 5. Bear Case (mais agressivo se Piotroski < 5)
- **3 maiores riscos com prob × impacto:**
    - Risco de mercado em geral: Probabilidade alta, impacto significativo.
    - Dados insuficientes para análise financeira detalhada: Probabilidade alta, impacto crítico na tomada de decisão.
    - Possível fraude contábil ou irregularidades não detectadas: Probabilidade média-alta, impacto severo.
- **Cenário de -40%:** Sem dados específicos sobre o negócio e a situação financeira da empresa, é impossível prever com precisão as consequências de uma queda de 40%. No entanto, considerando os riscos mencionados acima, seria razoável esperar um impacto significativo na liquidez e na capacidade operacional da empresa.

# 6. Bull Case
- **Catalisadores específicos com prazo:** Não disponível devido à falta de dados sobre o negócio.
- **O que precisa acontecer para o preço dobrar em 3 anos?** Sem informações financeiras, não é possível identificar fatores específicos.

# 7. Classificação Lynch
- **Slow / Stalwart / Fast / Cyclical / Turnaround / Asset Play:** Não possível classificar sem dados sobre a natureza do negócio e desempenho histórico.
- **2-3 argumentos objetivos:** Impossível fornecer devido à falta de informações.

# 8. Veredicto Final
- **Decisão com 3 critérios mensuráveis:**
    - Dados financeiros insuficientes para avaliação.
    - Risco elevado devido a incertezas e possíveis irregularidades contábeis.
    - Não atende aos princípios básicos do value investing (Graham, Buffett, Klarman, Dalio).
- **Position sizing:** Evitar. A falta de dados financeiros confiáveis e a alta probabilidade de riscos significativos indicam que esta é uma oportunidade de investimento inaceitável sob os critérios estabelecidos para value investing.

#### 2026-05-07 · Filing 2026-05-07
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM_FILING_2026-05-07.md` (cemetery archive)_

#### Filing dossier — [[JPM]] · 2026-05-07

**Trigger**: `sec:8-K` no dia `2026-05-07`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/19617/000119312526211978/d903351d8k.htm>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 314.90

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `306.26` |
| HOLD entre | `306.26` — `392.63` (consensus) |
| TRIM entre | `392.63` — `451.53` |
| **SELL acima de** | `451.53` |

_Método: `buffett_ceiling`. Consensus fair = R$392.63. Our fair (mais conservador) = R$306.26._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.16465001` | `0.1639` | +0.4% |
| EPS | `20.88` | `21.1753` | +1.4% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `filing:sec:8-K:2026-05-07` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-01 · Council review · Hank Tier-One
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Hank Tier-One\reviews\JPM_2026-05-01.md` (cemetery archive)_

#### Hank Tier-One sobre [[JPM|JPM]]

**Função no debate**: Banks US Specialist (`sector_specialist`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _JPMorgan mantém posição de longo prazo com sólidos dividendos e P/E abaixo do setor_

JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos.

**Métricas que invoquei**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- P/B de 2.44, acima do setor (2.21x)
- NII outlook trimmed recentemente

##### Round 2 — Resposta aos colegas

**Concordei com**:
- JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização. - Mariana Macro

**Desafiei**:
- redução no outlook NII | Private credit lending restrictions - Valentina Prudente; Essa redução pode ser temporária ou uma correção necessária que não afeta a sustentabilidade a longo prazo da empresa.

##### Quem mais estava na sala

- [[council.macro]] (Chief Macro Strategist)
- [[risk.drift-audit]] (Chief Risk Officer)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[JPM|📖 Storytelling completo (8 actos)]]
- [[JPM|🏛️ Transcript do Council debate]]
- [[council.banks-us|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\JPM_2026-05-01.md` (cemetery archive)_

#### Mariana Macro sobre [[JPM|JPM]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _JPMorgan mantém posição atraente com sólidos fundamentos financeiros_

JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos robusto, indicando valorização.

**Métricas que invoquei**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- redução da perspectiva NII
- impacto potencial de crises de crédito

##### Round 2 — Resposta aos colegas

**Concordei com**:
- JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização. - Valentina Prudente

**Desafiei**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - Hank Tier-One | A elevação no P/B pode ser atribuída a fatores específicos da empresa que não refletem necessariamente uma sobrevalorização, como investimentos em ativos intangíveis ou crescimento projetado

##### Quem mais estava na sala

- [[council.banks-us]] (Banks US Specialist)
- [[risk.drift-audit]] (Chief Risk Officer)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[JPM|📖 Storytelling completo (8 actos)]]
- [[JPM|🏛️ Transcript do Council debate]]
- [[council.macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\JPM_2026-05-01.md` (cemetery archive)_

#### Pedro Alocação sobre [[JPM|JPM]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _JPMorgan mantém sólida performance financeira_

JPM tem P/E abaixo do setor (14.98 vs mediana de 15.75x), ROE acima da média (16.5% vs mediana de 15.4%) e histórico consistente de dividendos.

**Métricas que invoquei**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- redução no outlook NII
- peso na carteira acima do recomendado (9.7%)

##### Round 2 — Resposta aos colegas

**Concordei com**:
- JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos - Hank Tier-One

**Desafiei**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - Concerns: P/B de 2.44, acima do setor (2.21x), mas o P/E está abaixo da média e sugere valorização; a redução do NII é um risco, mas não invalida a posição atualmente

##### Quem mais estava na sala

- [[council.banks-us]] (Banks US Specialist)
- [[council.macro]] (Chief Macro Strategist)
- [[risk.drift-audit]] (Chief Risk Officer)

##### Documentos relacionados

- [[JPM|📖 Storytelling completo (8 actos)]]
- [[JPM|🏛️ Transcript do Council debate]]
- [[council.allocation|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\JPM_2026-05-01.md` (cemetery archive)_

#### Valentina Prudente sobre [[JPM|JPM]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _JPMorgan mantém posição atraente com sólidos fundamentos_

JPM tem P/E abaixo da média do setor (14.98 vs 15.75), ROE acima (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização.

**Métricas que invoquei**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- NII outlook trimmed
- Private credit lending restrictions

##### Round 2 — Resposta aos colegas

**Concordei com**:
- JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos - Hank Tier-One

**Desafiei**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - redução no outlook NII é um risco que precisa ser monitorado de perto mas não invalida a posição atualmente bem fundamentada
- redução no outlook NII | impacto potencial de crises de crédito - enquanto o cenário macro é preocupante, os fundamentos atuais da JPM mantêm a posição atrativa

##### Quem mais estava na sala

- [[council.banks-us]] (Banks US Specialist)
- [[council.macro]] (Chief Macro Strategist)
- [[council.allocation]] (Capital Allocator)

##### Documentos relacionados

- [[JPM|📖 Storytelling completo (8 actos)]]
- [[JPM|🏛️ Transcript do Council debate]]
- [[risk.drift-audit|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*


### (undated)

#### — · Other
_source: `Clippings\JPM & Fool.md`_

JPM Research, aqui onde teremos as nossas researches e comparações nosso potênciais e tudo mais. algo a se considerar a integrar com os prints que eu coloquei antes.

![[Pasted image 20260507215233.png]]

**US OVERVIEW**

Podemos fazer igual para o Brazil. Subdividir FIIs x Stocks (?)

![[Pasted image 20260507215318.png]]

**Events**

![[Pasted image 20260507215438.png]]


**ALERTS**

Aqui tem como colocar alerta para como, isso em si, o sistema já deve monitorar e pensar "possível preço justo de entrada como sugerido, alerta, ou algo assim"

![[Pasted image 20260507215910.png]]



**AQUI ESTÁ TODA PARTE DO FOOL.COM E O POTENCIAL DE IDEIAS**

**Main Dashboard**

![[Pasted image 20260507220518.png]]

**Reccomendations**


![[Pasted image 20260507220555.png]]

Agora todo o code de um recomendation e como é estruturado

title: "Stock Advisor | The Motley Fool"
source: "https://www.fool.com/premium/18/coverage/updates/2026/05/07/buy-krystal-biotech-a-gene-therapy-pioneer"

---
**Price at publication: $281.40**  
as of 12:48 p.m. on May 7

##### Foolish Thesis

- Krystal Biotech has developed a differentiated method for gene therapy that could transform the emerging field of medicine.
- The company is achieving strong profitability with its one commercialized treatment, Vyjuvek.
- Co-founders Krish and Suma Krishnan have decades of experience in developing and commercializing novel treatments.
- Despite early successes, there is still plenty of growth remaining at this emerging biotech.

###### Analyst Projections

**Aggressive**  
Investing Type

**15+%**  
Est. annualized return

**\-40%**  
Est. max drawdown

These estimates reflect the Hidden Gems team’s opinion at the time of this recommendation.

***Prefer a video?*** This recommendation is accompanied by a live chat in which the team talks more about the company and takes questions. Click [here](https://www.fool.com/premium/18/coverage/updates/2026/05/07/our-next-recommendation-is) to watch!

##### What Krystal Biotech Does

**Krystal Biotech** [(NASDAQ: KRYS)](https://www.fool.com/premium/company/341337) is a commercial stage biotechnology company specializing in gene therapy for rare diseases. It has one commercial treatment at present, Vyjuvek, which treats a rare genetic condition known as dystrophic epidermolysis bullosa (DEB, also colloquially called butterfly skin disease). The condition affects a person's ability to build the right types of collagen that binds layers of skin together, which results in severe blistering and scarring. Vyjuvek delivers genetic material to the affected cells such that they can build the right type of collagen.

The FDA approved Vyjuvek in 2023 and is generating approximately $115 million in quarterly revenue (as of the most recent quarter). Vyjuvek has received approval from Germany, France, and Japan recently and management anticipates other European countries to approve the treatment by the end of the year. Over the past 12 months, the company has reported a 53% net income margin and sales growth of 25% year over year.

Beyond Vyjuvek, Krystal Biotech also has several potential treatments in various stages of development and clinical trials. Its current portfolio of care focuses on genetic conditions related to skin, eyes, lungs, and some solid tumor cancer treatments.

Additionally, it is developing an aesthetics business, Jeune, that uses gene therapy to address some of the core causes of aging and wrinkles in skin (collagen formation).

Krystal Biotech was co-founded by CEO Krish Krishnan and President of Research and Development Suma Krishnan. The biotech power couple founded Krystal after long tenured careers at other biotech companies to develop new methods for gene therapy based on Suma's work.

##### Why Krystal Biotech Is a Buy

###### Substantial Profitability Now and Deep Pipeline for the Future

Not all new treatments become a profit engine immediately. They often require a certain volume of sales to reach critical mass for profitability, and those sales often ramp slowly. What is surprising is how quickly Vyjuvek has become a profit engine. As a treatment for a rare disease without alternative treatments and high ongoing care costs for DEB patients, Krystal is able to charge a rather high price on a per unit basis.

This also bodes well for the company's growth. Management estimates that unique prescriptions for Vyjuvek are less than half of the U.S. population, with even lower penetration rates in its current European markets. High usage rates in existing markets and growth in not-yet-approved markets provide ample growth in the near term.

Further down the road, Krystal has a robust development and clinical trial pipeline that's attacking much larger patient groups than DEB. Management's goal for 2030 is to have four marketed rare disease medicines treating 10,000 patients (for reference, the current patient count is 710).

###### Groundbreaking Gene Therapy Technology

For certain diseases caused by a single faulty gene, we understand the genetic defect well enough that the main challenge is no longer finding it, but delivering the fix to the right cells. d. One of the biggest challenges for gene therapy is getting the right genetic material to the cell nucleus. That’s accomplished using a virus that naturally infiltrates cells, also called a vector.

What makes Krystal Biotech so unique in this space is the work it has done on improved vectors for delivering genetic material (the payload) to affected cells. Suma Krishnan's team has designed a genetically modified herpes simplex virus (HSV-1) that they believe is a major advancement in gene therapy.

Compared to other viral vectors for gene therapy, Krystal Biotech says its modified HSV-1 virus is superior because it can carry a larger genetic payload to treat more complex genetic mutations, it has a much lower immune response, and allows for multiple treatments without the body building immunity to the virus. Krystal’s patents for using HSV-1 viruses as vectors coupled with its ability to manufacture them–a tricky area they have mastered–create an additional moat.

###### Why Now?

Even though Vyjuvek has so far been a resounding success and shares are up $2,500% since the IPO in 2017, there is still an immense amount of growth potential in Vyjuvek and any contributions from its treatment pipeline. There are also some longshots like its Jeune aesthetics business taking off and any potential licensing opportunities for its HSV-1 viral vector technology in the burgeoning gene therapy industry.

##### What Could Go Wrong

###### Advancements or Alternative DEB Treatments

Krystal has developed a strong position in treating DEB, but other treatments have come to market and more are on their way. Zevaskyn, a surgical gene therapy option for recessive DEB, received approval in April of 2025.

Zevaskyn is slightly different from Krystal's offering because it treats recessive DEB (RDEB), a more severe condition. Therefore, there isn't much competition or overlap for the two treatments. However, other gene therapy companies are working on solutions for DEB that could compete with Vyjuvek.

###### Development Pipeline Treatments Aren't Guaranteed Success

Krish and Suma Krishnan have stellar track records at shepherding potential treatments from the development phase all the way through FDA approval. Prior to Krystal, they were pivotal in the development of several ADHD treatments and treatments for specific conditions related to end stage kidney disease.

Even with decades of success, there is no guarantee that all (or even some) of its development pipeline gets through the clinical trial and FDA approval process. According to the National Institutes of Health, the overall success rate for all treatments in phase 2 trials getting to commercialization is in the 16% to 21% range.

Some of the valuation for Krystal Biotech's stock is likely tied to the pending success of several treatments in its pipeline. Should the clinical trials for those treatments not meet critical end points, then it would likely have a profound impact on the stock.

[\[ See how you can tell if this investment is going right -- or wrong. \]](https://www.fool.com/premium/18/coverage/updates/2026/05/07/krystal-biotech-bull-and-bear)

##### Who Else to Watch

- **Abenoa Pharmaceuticals** [(NASDAQ: ABEO)](https://www.fool.com/premium/company/335340), maker of Zevaskyn
- LEO Pharma (private)
- Chiesi Farmaceutici (private)

##### Bottom Line

Krystal Biotech has developed a groundbreaking method to deliver gene therapy through a new viral vector technology. It has one smashing commercial success (Vyjuvek) and several promising gene therapy treatments in the pipeline. We believe Krish and Suma Krishnan have built an incredible business and expect more great things to come.

##### Portfolio Fit

###### Might Be For

Krystal Biotech is a great option for investors looking for stocks with high growth potential in the healthcare industry.

###### Might Not Be For

We won't likely be getting a dividend from Krystal Biotech anytime soon, so income investors may not be interested. Also, those with high exposure to healthcare already may want to consider something else for portfolio diversification.

###### Not the Right Stock?

If Krystal Biotech isn't to your liking, consider **Moog** ([NYSE: MOGA](http://fool.com/premium/company/206462)) as an alternative. It was [recommended in *Stock Advisor* last month](https://www.fool.com/premium/18/coverage/updates/2026/04/16/buy-moog-mission-critical-components-and-more) and is a key component supplier to the aerospace and defense industry. It also has strong growth tailwinds behind it thanks to both increased defense budgets and commercial airplane production rates.

##### What Team Rule Breakers Thinks

Gene therapy has been a scientific tour-de-force over the past decade, but more often than not a commercial bust. Krystal Biotech is an exception, and it mostly comes down to one thing: their HSV-1 vector. (A vector in this context is a virus that acts as a Trojan horse, carrying genetic material into cells.) There are different vectors for different jobs, and HSV-1 is particularly useful for skin and surface tissue. Herpes has evolved to enter cells from their exposed outer surface—that's precisely why it spreads so easily through skin contact!

One seeming drawback of this vector turns out to be its sneaky superpower: Because HSV doesn’t incorporate into the genome, Vyjuvek’s effectiveness fades away as cells divide. That’s bad if you want a “one and done” treatment. But in our healthcare system, it makes for a re-dosable drug, much more in line with how drugs are currently reimbursed–and as we can see, that has made for rapid commercial success.

Krystal can’t really use this platform to target organs like liver, muscle, heart, and bone marrow, where other vectors work better. But they are being smart about its advantages. One exciting program is KB407, which is going after cystic fibrosis. Other gene therapies have failed in CF, because it’s hard to gain access to the epithelial cells (that is, the surface membrane) of the lungs. This is a perfect application for HSV, and while clinical results are limited to date, they look promising. The success of V **ertex Pharmaceuticals** [(NASDAQ: VRTX)](https://www.fool.com/premium/company/206020) is an indication of the market size here. -- Karl Thiel

*Tyler Crowe contributed to this report.*

#### — · Dossier
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM.md` (cemetery archive)_

#### [[JPM]] — Dossier Deepdive (2026-05-09)

> Sector: ? · Country: ? · Price: ? 

##### Quality Scores

| Score | Valor | Zona |
|---|---|---|
| Piotroski | -/9 | - |
| Altman Z | - | - |
| Beneish M | - | - |
| Moat | -/10 | N/A |


##### Delta Report

```
Delta Report — JPM | hoje vs run anterior (2026-05-08)
```

##### Strategist Dossier

#### 1. Executive Summary
- **Rating:** EVITAR
- **Preço justo estimado e upside/downside %:** Não possível calcular devido à falta de dados quantitativos.
- **Risk Score:** 10 (Altíssimo)
- **Alerta vermelho:** Dados insuficientes para avaliar o Beneish M-Score ou Altman Z-Score, impossibilitando uma análise completa do risco.

#### 2. O Negócio
- **Modelo de receita e fontes de caixa:** Não disponível.
- **Moat (Network Effect / Switching Costs / Intangibles / Cost Adv):** Não possível avaliar sem dados específicos sobre o negócio da empresa.

#### 3. Decomposição DuPont
- **ROE = Margem × Giro × Alavancagem:** Dados insuficientes para calcular.
- **Identificar a alavanca dominante:** Não disponível devido à falta de dados financeiros.

#### 4. Valuation Multinível
- **Graham Number:** Não aplicável sem informações específicas sobre o lucro por ação e P/B da empresa.
- **DCF com 3 cenários (Bear / Base / Bull):** Impossível realizar sem dados financeiros futuros, incluindo fluxo de caixa livre projetado.
- **EV/EBITDA vs mediana setor:** Não possível comparar sem informações sobre o múltiplo EV/EBITDA da empresa e do setor.

#### 5. Bear Case (mais agressivo se Piotroski < 5)
- **3 maiores riscos com prob × impacto:**
    - Risco de mercado em geral: Probabilidade alta, impacto significativo.
    - Dados insuficientes para análise financeira detalhada: Probabilidade alta, impacto crítico na tomada de decisão.
    - Possível fraude contábil ou irregularidades não detectadas: Probabilidade média-alta, impacto severo.
- **Cenário de -40%:** Sem dados específicos sobre o negócio e a situação financeira da empresa, é impossível prever com precisão as consequências de uma queda de 40%. No entanto, considerando os riscos mencionados acima, seria razoável esperar um impacto significativo na liquidez e na capacidade operacional da empresa.

#### 6. Bull Case
- **Catalisadores específicos com prazo:** Não disponível devido à falta de dados sobre o negócio.
- **O que precisa acontecer para o preço dobrar em 3 anos?** Sem informações financeiras, não é possível identificar fatores específicos.

#### 7. Classificação Lynch
- **Slow / Stalwart / Fast / Cyclical / Turnaround / Asset Play:** Não possível classificar sem dados sobre a natureza do negócio e desempenho histórico.
- **2-3 argumentos objetivos:** Impossível fornecer devido à falta de informações.

#### 8. Veredicto Final
- **Decisão com 3 critérios mensuráveis:**
    - Dados financeiros insuficientes para avaliação.
    - Risco elevado devido a incertezas e possíveis irregularidades contábeis.
    - Não atende aos princípios básicos do value investing (Graham, Buffett, Klarman, Dalio).
- **Position sizing:** Evitar. A falta de dados financeiros confiáveis e a alta probabilidade de riscos significativos indicam que esta é uma oportunidade de investimento inaceitável sob os critérios estabelecidos para value investing.

---
*Generated by `ii deepdive JPM` em 2026-05-09T14:37:58.*

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[JPM|JPM]] (JPMorgan Chase)

**Final stance**: 🟢 **BUY**  
**Confidence**: `high`  
**Modo (auto)**: B (US)  |  **Sector**: Financials  |  **Held**: sim  
**Elapsed**: 66.7s  |  **Failures**: 0

##### Quem esteve na sala

- [[council.banks-us]] — _Banks US Specialist_ (`sector_specialist`)
- [[council.macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[risk.drift-audit]] — _Chief Risk Officer_ (`risk_officer`)
- [[council.allocation]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos - Hank Tier-One
- P/B de 2.44, acima do setor (2.21x) pode ser atribuído a fatores específicos da empresa que não refletem necessariamente uma sobrevalorização, como investimentos em ativos intangíveis ou crescimento projetado - Mariana Macro

**Dissenso (preservado)**:
- Hank Tier-One disse que a redução no outlook NII pode ser temporária ou uma correção necessária que não afeta a sustentabilidade a longo prazo da empresa, enquanto Valentina Prudente e Pedro Alocação disseram que é um risco que precisa ser monitorado de perto

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ redução no outlook NII - Pedro Alocação
- ⚠️ impacto potencial de crises de crédito - Valentina Prudente

**Sizing**: Considerar reduzir a posição para um peso na carteira abaixo do recomendado (9.7%) - Pedro Alocação

##### Round 1 — Opening Statements (blind)

###### [[council.banks-us]] — 🟢 **BUY**
_Banks US Specialist_

**Headline**: _JPMorgan mantém posição de longo prazo com sólidos dividendos e P/E abaixo do setor_

JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos.

**Métricas**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- P/B de 2.44, acima do setor (2.21x)
- NII outlook trimmed recentemente

###### [[council.macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _JPMorgan mantém posição atraente com sólidos fundamentos financeiros_

JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos robusto, indicando valorização.

**Métricas**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- redução da perspectiva NII
- impacto potencial de crises de crédito

###### [[risk.drift-audit]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _JPMorgan mantém posição atraente com sólidos fundamentos_

JPM tem P/E abaixo da média do setor (14.98 vs 15.75), ROE acima (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização.

**Métricas**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- NII outlook trimmed
- Private credit lending restrictions

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _JPMorgan mantém sólida performance financeira_

JPM tem P/E abaixo do setor (14.98 vs mediana de 15.75x), ROE acima da média (16.5% vs mediana de 15.4%) e histórico consistente de dividendos.

**Métricas**:
- P/E=14.98
- ROE=16.5%
- DivStreak=43

**Preocupações**:
- redução no outlook NII
- peso na carteira acima do recomendado (9.7%)

##### Round 2 — Respostas (peers visíveis)

###### [[council.banks-us]] — 🟢 **BUY**
_Banks US Specialist_

**Concordou com**:
- JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização. - Mariana Macro

**Desafiou**:
- redução no outlook NII | Private credit lending restrictions - Valentina Prudente; Essa redução pode ser temporária ou uma correção necessária que não afeta a sustentabilidade a longo prazo da empresa.

###### [[council.macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- JPM tem P/E abaixo do setor (14.98 vs 15.75), ROE acima da média (16.5% vs 15.4%) e histórico de dividendos consistente, indicando valorização. - Valentina Prudente

**Desafiou**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - Hank Tier-One | A elevação no P/B pode ser atribuída a fatores específicos da empresa que não refletem necessariamente uma sobrevalorização, como investimentos em ativos intangíveis ou crescimento projetado

###### [[risk.drift-audit]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos - Hank Tier-One

**Desafiou**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - redução no outlook NII é um risco que precisa ser monitorado de perto mas não invalida a posição atualmente bem fundamentada
- redução no outlook NII | impacto potencial de crises de crédito - enquanto o cenário macro é preocupante, os fundamentos atuais da JPM mantêm a posição atrativa

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- JPM tem um P/E de 14.98, inferior ao setor (15.75x), e ROE de 16.5%, acima da média (15.4%). Dividendos crescem há 43 anos - Hank Tier-One

**Desafiou**:
- P/B de 2.44, acima do setor (2.21x) | NII outlook trimmed recentemente - Concerns: P/B de 2.44, acima do setor (2.21x), mas o P/E está abaixo da média e sugere valorização; a redução do NII é um risco, mas não invalida a posição atualmente

##### Documentos relacionados

- [[JPM|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[JPM|Hank Tier-One]] em [[council.banks-us]]/reviews/
  - [[JPM|Mariana Macro]] em [[council.macro]]/reviews/
  - [[JPM|Valentina Prudente]] em [[risk.drift-audit]]/reviews/
  - [[JPM|Pedro Alocação]] em [[council.allocation]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:JPM — JPMorgan Chase ===
Sector: Financials  |  Modo (auto): B  |  Held: True
Last price: 313.2300109863281 (2026-04-30)
Position: 7 shares @ entry 306.55571428571426
Fundamentals: P/E=14.98 | P/B=2.44 | DY=1.9% | ROE=16.5% | DivStreak=43.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: JPMorgan Chase é uma excelente posição long-term para um investidor Buffett/Graham devido à sua sólida história de dividendos, com 43 anos consecutivos de aumentos e uma taxa de crescimento anual média de dividendos de 10%. A empresa possui um P/E de 14.98, que é inferior ao do setor financeiro em geral, indicando um preço justo ou subvalorizado. Além disso, o ROE de 16.47% sugere uma eficiência operacional superior e a capacidade sustentável de gerar lucros acima da média.

**Key assumptions**:
1. A taxa de dividendos (DY) permanecerá estável em torno de 1.88%.
2. O P/E continuarão abaixo do setor financeiro, mantendo o preço justo ou subvalorizado.
3. O ROE se manterá acima dos 16%, indicando eficiência operacional sustentável.
4. A empresa continuará a aume

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 9.7%
  Sector weight: 27.1%

WEB CONTEXT (qualitative research, last 30-90d):
  - JPMorgan Chase Q1 earnings beat, but NII outlook trimmed (JPM:NYSE) - Seeking Alpha [Tue, 14 Ap]
    # JPMorgan Chase Q1 earnings beat, but NII outlook trimmed. Follow us on Google for the latest stock newsFollow Seeking Alpha on Google for the latest stock news. JPMorgan Chase (JPM) stock slipped 0.9% in Tuesday premarket trading after th
  - JPMorgan Marks Down Private Credit Portfolios, FT Reports - Bloomberg [Wed, 11 Ma]
    # JPMorgan Limits Private Credit Lending After Loan Markdowns. Provide news feedback or report an error. Send a tip to our reporters. JPMorgan Chase & Co. is restricting some lending to private credit funds after marking down the value of c
  - JPMorgan Makes Bold Push to Offload Huge LBO Debt - Bloomberg.com [Sat, 14 Ma]
    # JPMorgan Makes Bold Push to Offload Huge LBO Debt. Provide news feedback or report an error. ### **Takeaways** by Bloomberg AISubscribe. Jamie Dimon has been warning for weeks — months, even — that the credit cycle will eventually sour. J
  - JPMorgan Chase is set to report first-quarter earnings – here’s what the Street expects - CNBC [Tue, 14 Ap]
    # JPMorgan Chase is set to report first-quarter earnings – here’s what the Street expects. * JPMorgan Chase reports first-quarter earnings before the bell on Tuesday. * Wall Street expects earnings of $5.45 per share and revenue of $49.17 b
  - Earnings playbook: JPMorgan Chase and Netflix kick off the reporting season - CNBC [Sun, 12 Ap]
    This quarter: The investment bank is forecast to report double-digit earnings and revenue growth from the year-earlier period, LSEG data shows. Tuesday Johnson & Johnson is set to report earnings before the bell, followed by a conference ca

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[1] sec (8-K) [2026-04-24]: 8-K | 5.03
     URL: https://www.sec.gov/Archives/edgar/data/19617/000001961726000119/jpm-20260421.htm
[2] sec (8-K) [2026-04-23]: 8-K | 8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/19617/000119312526173739/d235028d8k.htm
[3] sec (8-K) [2026-04-14]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/19617/000162828026024990/jpm-20260414.htm
[4] sec (8-K) [2026-04-14]: 8-K | 7.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/19617/000162828026025013/jpm-20260414.htm
[5] sec (proxy) [2026-04-06]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/19617/000001961726000096/jpm-20260402.htm
[6] sec (8-K) [2026-02-23]: 8-K | 7.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/19617/000162828026010693/jpm-20260223.htm

##### YOUTUBE INSIGHTS (transcripts ingeridos) (6 hits)
[7] YouTube BTG Pactual [2026-04-10] (operational): O JP Morgan irá reportar seus resultados na terça-feira, dia 14.
     URL: https://www.youtube.com/watch?v=WIRWPyYNJzE
[8] YouTube BTG Pactual [2026-04-10] (operational): O JP Morgan irá reportar seus resultados na terça-feira, dia 14.
     URL: https://www.youtube.com/watch?v=WIRWPyYNJzE
[9] YouTube O Primo Rico [2026-03-17] (thesis_bull): O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação aos EUA.
     URL: https://www.youtube.com/watch?v=7EBNjOuA-mI
[10] YouTube O Primo Rico [2026-03-17] (management): O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente.
     URL: https://www.youtube.com/watch?v=7EBNjOuA-mI
[11] YouTube O Primo Rico [2026-03-17] (thesis_bull): O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação aos EUA.
     URL: https://www.youtube.com/watch?v=7EBNjOuA-mI
[12] YouTube O Primo Rico [2026-03-17] (management): O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente.
     URL: https://www.youtube.com/watch?v=7EBNjOuA-mI

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[13] Bibliotheca: investment_valuation_3rd_edition: undamentals (analysts' estimates of expected growth
in EPS over the next five years, payout, return on equity, and beta) for U.S. insurance companies with a market
capitalization exceeding $1 billion.

Looking at the PE ratio, CNO Financial and Hartford look cheap, but they are also extremely risky 
[14] Bibliotheca: investment_valuation_3rd_edition: ed. In contrast, the predicted PE ratio for Aon Corporation is:
At 21.94 times earnings, Aon looks overvalued.
ILLUSTRATION 21.6: Valuing a Company Based on
Business Units: JP Morgan Chase in May 2011

JP Morgan Chase is in multiple businesses and breaks down its net profit by business. The followin
[15] Bibliotheca: investment_valuation_3rd_edition: R)
International financial reporting standards (IFRS)
acquisition accounting and
explanation of
Internet service providers/retailers
Internet stocks
Inventory, approaches to valuing
Inventory turnover

Inventory valuation
Investment announcements
Investments
income from
majority active
minority acti
[16] Bibliotheca: principles_for_navigating_big_debt_crises_by_ray_d: ittee late this evening 
dispatched a note to the German Chancellor 
informing him that it was prepared to grant the 
partial moratorium on this year’s reparations 
payments which had been scheduled.”

Part 2: German Debt Crisis and Hyperinflation (1918–1924)
28
June 1922–December 1922:  
Hyperinfla
[17] Bibliotheca: principles_for_navigating_big_debt_crises_by_ray_d: orning. Policemen 
were posted throughout the financial district in the event of trouble. New York 
Stock Exchange Superintendent William R. Crawford later described 
News & 
Federal Reserve Bulletin 

October 13, 1929
Mortgage Returns Show Good Values; Give 
Higher Investment Results Than Stocks an

##### TAVILY NEWS (≤30d) (5 hits)
[18] Tavily [Tue, 14 Ap]: # JPMorgan Chase Q1 earnings beat, but NII outlook trimmed. Follow us on Google for the latest stock newsFollow Seeking Alpha on Google for the latest stock news. JPMorgan Chase (JPM) stock slipped 0.9% in Tuesday premarket trading after the Wall Street giant trimmed its guidance for 2026 firmwide n
     URL: https://seekingalpha.com/news/4574690-jpmorgan-chase-q1-earnings-beat-but-nii-outlook-trimmed
[19] Tavily [Wed, 11 Ma]: # JPMorgan Limits Private Credit Lending After Loan Markdowns. Provide news feedback or report an error. Send a tip to our reporters. JPMorgan Chase & Co. is restricting some lending to private credit funds after marking down the value of certain loans in their portfolios, according to a person fami
     URL: https://www.bloomberg.com/news/articles/2026-03-11/jpmorgan-marks-down-private-credit-portfolios-ft-reports
[20] Tavily [Sat, 14 Ma]: # JPMorgan Makes Bold Push to Offload Huge LBO Debt. Provide news feedback or report an error. ### **Takeaways** by Bloomberg AISubscribe. Jamie Dimon has been warning for weeks — months, even — that the credit cycle will eventually sour. JPMorgan Chase & Co. is gearing up to help issuers sell billi
     URL: https://www.bloomberg.com/news/articles/2026-03-14/jpmorgan-makes-bold-push-to-offload-huge-lbo-debt-credit-weekly
[21] Tavily [Wed, 11 Ma]: REUTERS/Dado Ruvic/Illustration/File Photo Purchase Licensing Rights, opens new tab. March 11 (Reuters) - JPMorgan Chase (JPM.N), opens new tab has ​marked down ‌the value of ​certain loans ​held by private-credit ⁠groups ​and is tightening ​its lending to the sector, ​the ​Financial Times reported 
     URL: https://www.reuters.com/business/finance/jpmorgan-marks-down-loan-portfolios-private-credit-groups-ft-reports-2026-03-11/
[22] Tavily [Tue, 14 Ap]: REUTERS/Eduardo Munoz/File Photo Purchase Licensing Rights, opens new tab. April 14 (Reuters) - JPMorgan Chase (JPM.N), opens new tab reported a rise in first

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM_STORY.md` (cemetery archive)_

#### JPMorgan Chase — JPM

##### Análise de Investimento · Modo FULL · Jurisdição US

*1 de Maio de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo B-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[council.banks-us]] — _Banks US Specialist_
- [[council.macro]] — _Chief Macro Strategist_
- [[risk.drift-audit]] — _Chief Risk Officer_
- [[council.allocation]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/JPM_2026-05-01.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (5 hits) |
| **2 — Metric Engine** | Receita R$ 181.8 bi · FCF R$ -147.78 bi · ROE 16% · DGR 25.3% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** |  |
| **5 — Classification** | Modo B-US ·  |
| **5.5 — Council Debate** | BUY (high) · 1 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo B-US sob a Jurisdição US. JPMorgan Chase, com ticker JPM, é uma das instituições financeiras mais influentes e diversificadas dos Estados Unidos, operando em múltiplos segmentos do setor financeiro incluindo bancário comercial, banco de investimento, gestão de ativos e serviços privados. A empresa tem sido notável por sua capacidade de gerir riscos complexos e aproveitar oportunidades no mercado global, mantendo-se como uma referência em termos de inovação tecnológica e práticas éticas.

A armadilha típica que os investidores podem cair ao analisar JPMorgan Chase é a confusão entre o alcance da marca e as suas capacidades operacionais reais. A empresa é frequentemente associada à sua reputação de prestígio e solidez, mas isso pode ocultar desafios mais específicos em segmentos como o crédito privado ou a gestão de ativos. Além disso, a diversificação geográfica recomendada pelo JP Morgan Private Bank (indicando que a Europa e os mercados emergentes estão descontados em relação aos EUA) pode ser vista como uma oportunidade estratégica para expansão, mas também como um risco se não for gerida adequadamente.

No contexto competitivo, JPMorgan Chase mantém-se como líder no mercado americano de serviços financeiros, com forte presença global. A empresa enfrenta competição significativa de outras instituições bancárias e empresas de investimento, mas sua diversificação estratégica e capacidade de inovação tecnológica a distinguem do resto da indústria.

##### Ato 2 — O Contexto

O panorama macroeconômico atual é caracterizado por taxas de juros elevadas nos Estados Unidos, com o Fed Funds Rate estabelecido entre 4.25% e 4.50%, enquanto a taxa de juro do Tesouro dos EUA a dez anos se mantém em torno de 4.2%. O custo de capital próprio (Ke) é estimado em cerca de 10%. A economia está transitando para uma fase tardia de expansão, com sinais emergentes de enfraquecimento econômico.

Para o setor financeiro e JPMorgan Chase especificamente, essas condições desafiam a rentabilidade dos produtos baseados em juros, como depósitos e empréstimos. A elevação das taxas de juro pode reduzir a demanda por crédito e aumentar os custos operacionais para as instituições financeiras. No entanto, também oferece oportunidades para gerar lucros através da gestão eficaz dos riscos e investimentos em produtos mais rentáveis.

A recente decisão de JPMorgan Chase de limitar o financiamento a fundos de crédito privado após uma diminuição no valor de certas carteiras de empréstimos ilustra como a empresa está respondendo às condições atuais. Esta medida reflete um ajuste estratégico para mitigar riscos e preservar a solidez financeira, enquanto continua a procurar oportunidades lucrativas.

Em termos regulatórios, não foram identificadas mudanças significativas que afetem diretamente JPMorgan Chase nos dados fornecidos. No entanto, o ambiente de regulação financeira permanece em constante evolução, e a empresa deve continuar monitorando cuidadosamente as tendências para se manter competitiva e em conformidade com as normas estabelecidas.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória de crescimento sustentado na receita e no lucro líquido, embora com algumas preocupações emergentes em relação à geração de fluxo de caixa livre (FCF). A tabela a seguir detalha os principais indicadores financeiros anuais:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 127.73B | — | — | — | R$ 37.68B | 29.5% | R$ 107.12B |
| 2023 | R$ 154.95B | — | — | — | R$ 49.55B | 32.0% | R$ 12.97B |
| 2024 | R$ 169.44B | — | — | — | R$ 58.47B | 34.5% | R$ -42.01B |
| 2025 | R$ 181.85B | — | — | — | R$ 57.05B | 31.4% | R$ -147.78B |

A receita da empresa cresceu de forma consistente, com um CAGR (Compound Annual Growth Rate) de aproximadamente 12% entre 2022 e 2025. O lucro líquido também demonstrou uma tendência de crescimento, embora tenha apresentado uma ligeira queda em 2025 comparativamente ao ano anterior. A margem líquida aumentou significativamente de 29,5% em 2022 para 34,5% em 2024 antes de recuar um pouco em 2025.

No entanto, o fluxo de caixa livre (FCF) apresenta uma situação preocupante. Após ter atingido R$107 bilhões em 2022 e R$12,97 bilhões em 2023, a empresa registrou um FCF negativo de R$42 bilhões em 2024 e um ainda mais alarmante de R$-147,78 bilhões em 2025. Este declínio dramático no FCF sugere que a empresa pode estar enfrentando desafios significativos na geração de caixa operacional ou investindo pesadamente em projetos que não geram retorno imediato.

A tabela abaixo mostra o histórico dos dividendos pagos pela empresa:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 1.800 |
| 2021 | 3.700 |
| 2022 | 4.000 |
| 2023 | 4.050 |
| 2024 | 4.600 |
| 2025 | 5.550 |
| 2026 | 3.000 |

O Dividend Growth Rate (DGR) calculado, sem considerar dividendos extraordinários, é de 25,3% ao ano. Este DGR robusto sugere um compromisso contínuo da empresa em distribuir lucros aos acionistas e pode ser uma característica atraente para investidores que buscam dividendos sustentáveis.

É importante notar que o DY total reportado de 1,88% deve ser interpretado com cautela. Dada a queda nos dividendos projetados para 2026 (de R$5.550 em 2025 para R$3.000), pode indicar uma possível reavaliação da política de distribuição de lucros ou um ajuste estratégico na alocação de capital.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A deterioração no fluxo de caixa livre é particularmente preocupante, pois indica que a empresa está gastando mais do que gera em termos de caixa operacional, o que pode ser um sinal de problemas subjacentes na gestão financeira ou na eficiência operacional.

##### Ato 4 — O Balanço

O balanço da empresa no final de 2026 apresenta uma série de indicadores importantes para avaliar a saúde financeira e o desempenho. Com um preço atual de R$313,23 por ação, os principais indicadores são:

- **P/E (Price to Earnings Ratio)**: 14,98
- **P/B (Price to Book Value Ratio)**: 2,44
- **DY (Dividend Yield)**: 1,88%
- **ROE (Return on Equity)**: 16,47%

A relação de endividamento líquido (Net Debt) é estimada em R$249,99 bilhões, com uma razão Net Debt/EBITDA de aproximadamente 5,3x (considerando o EBITDA mais recente disponível). Esta alavancagem elevada pode ser um ponto de atenção, especialmente considerando a deterioração no fluxo de caixa livre.

O Current Ratio da empresa é de 1,2x, indicando que a empresa tem recursos líquidos suficientes para cobrir suas dívidas a curto prazo. No entanto, este valor está abaixo do ideal e pode sugerir algum risco associado à liquidez.

A relação ROE (Return on Equity) de 16,47% supera o custo de capital próprio estimado para o Brasil (~18,25%), o que indica que a empresa cria valor para os acionistas. No entanto, é crucial observar que esta vantagem pode ser temporária dada a situação atual do fluxo de caixa livre e da alavancagem.

Em resumo, enquanto a empresa apresenta um histórico sólido em termos de dividendos e lucratividade contábil, os desafios emergentes no fluxo de caixa livre e na gestão da dívida podem representar riscos significativos para o futuro.

---

##### Ato 5 — Os Múltiplos

O banco JPM mantém uma posição sólida em termos de múltiplos financeiros quando comparado a seus pares e ao índice geral, embora com algumas nuances que merecem destaque. O preço-earnings (P/E) do JPM está ligeiramente abaixo da média setorial e do índice, situando-se em 14,98x contra uma mediana de 15,75x para seus pares e 21,00x para o índice. Este múltiplo sugere que os investidores estão atribuindo um valor mais baixo à empresa comparativamente a outros bancos e ao mercado em geral.

A relação preço-balanço (P/B) do JPM é de 2,44x, ligeiramente superior à mediana setorial de 2,21x, mas significativamente inferior aos 3,50x do índice. Este múltiplo indica que o ativo líquido da empresa está sendo avaliado com um desconto em relação ao mercado geral e a média dos seus pares.

O dividend yield (DY) reportado pelo JPM é de 1,88%, ligeiramente inferior à mediana setorial de 2,0% e superior aos 1,5% do índice. É importante notar que o DY pode incluir dividendos extraordinários ou não refletir a tendência estrutural da empresa. No caso do JPM, este valor sugere uma distribuição de lucros aos acionistas em um nível confortável para a empresa.

O retorno sobre o patrimônio (ROE) do JPM é de 16,47%, ligeiramente superior à mediana setorial de 15,4% e ao índice que se situa em 16,0%. Este indicador reflete efetivamente a capacidade da empresa em gerar lucros com relação ao capital próprio investido.

A rendibilidade do fluxo de caixa livre (FCF Yield) é negativa para o JPM no último ano, apresentando um valor de -17,7%, muito inferior à mediana setorial de 3,3% e ao índice que se situa em 4,0%. Este resultado sugere que a empresa está utilizando mais recursos do que gera em fluxo de caixa livre, o que pode ser uma preocupação para investidores focados neste indicador.

A tabela abaixo resume os múltiplos financeiros comparativos:

| Múltiplo | JPM | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 14.98x | 15.75x | 21.00x |
| P/B | 2.44x | 2.21x | 3.50x |
| DY | 1.9% | 2.0% | 1.5% |
| FCF Yield | -17.7% | 3.3% | 4.0% |
| ROE | 16.5% | 15.4% | 16.0% |
| ND/EBITDA | — | 0.48x | — |

##### Ato 6 — Os Quality Scores

Os indicadores de qualidade financeira do JPM não estão disponíveis para análise detalhada, o que implica a inaplicabilidade dos scores de Piotroski, Altman e Beneish neste contexto. Sem os dados necessários para calcular estes indicadores, é impossível fornecer uma avaliação precisa da saúde financeira e solidez operacional da empresa.

A falta destas métricas limita significativamente a capacidade de avaliar aspectos fundamentais como a probabilidade de falência (Altman Z-Score), a detecção de manipulação contábil (Beneish M-Score) ou a robustez financeira geral (Piotroski F-Score). Sem esses dados, qualquer recomendação baseada em análise fundamental deve ser tratada com cautela e consideração adicional para outros indicadores disponíveis.

A ressalva técnica X2 do Altman para o Brasil não é aplicável neste caso devido à ausência dos dados necessários.

---

##### Ato 7 — O Moat e a Gestão

O moat de JPMorgan Chase é classificado como Wide. Este reconhecimento baseia-se em múltiplos aspectos da empresa que lhe conferem uma vantagem competitiva sustentável no longo prazo, incluindo eficiência operacional, custos de escala e ativos intangíveis.

Primeiramente, a JPMorgan Chase beneficia significativamente dos custos de escala. Como um dos maiores bancos do mundo, a empresa é capaz de distribuir seus gastos fixos entre uma base muito ampla de clientes e transações, o que lhe permite oferecer serviços financeiros com eficiência incomparável. Esta vantagem é especialmente evidente em áreas como tecnologia e infraestrutura, onde os investimentos iniciais são altos mas os custos subsequentes relativamente baixos.

A empresa também possui uma forte presença de switching costs entre seus clientes corporativos e institucionais. A complexidade das transações financeiras e a necessidade de confiança estabelecida tornam difícil para essas entidades trocarem fornecedores, especialmente quando se trata de um banco com a reputação e o histórico operacional da JPMorgan.

Outro aspecto do moat é a eficiência operacional. A JPMorgan Chase tem demonstrado habilidade em gerir seus ativos e passivos de maneira eficiente, minimizando custos e maximizando rendimentos. Isso inclui estratégias como o refinanciamento de dívidas a taxas mais baixas e otimização das carteiras de investimento.

Em relação aos intangíveis, JPMorgan Chase possui uma marca extremamente valiosa que é reconhecida globalmente. Esta reputação lhe permite atrair e reter talentos de alta qualidade, além de facilitar a entrada em novos mercados ou negócios.

Por fim, o moat da empresa também se beneficia dos network effects. A JPMorgan Chase opera uma rede extensa de clientes que interagem uns com os outros através de seus produtos e serviços financeiros, criando um ecossistema valioso que é difícil para concorrentes replicarem.

Quanto ao insider ownership, o dado não está disponível nas informações fornecidas. Da mesma forma, não há menção a insider trades nos últimos seis meses na web facts.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico da JPMorgan Chase é predominantemente de valor, com pontuações específicas refletindo essa orientação. A empresa recebeu um score de +2 em Value, baseado em seu P/E de 15.0, que está abaixo da média setorial (18). O Growth score é de +1, indicando uma tendência de reinvestimento elevada apesar do rendimento dividendo baixo (<3%). A empresa também recebeu um score de +2 no Dividend, com um histórico ininterrupto de pagamentos por 43 anos. Finalmente, o Buffett score é de +3, refletindo um ROE de 16.5%, acima da média (15.4%), e uma consistência de crescimento dividendo que dura mais de uma década.

###### O que o preço desconta
O preço atual do JPMorgan Chase parece incorporar expectativas moderadas em relação ao seu desempenho futuro, refletindo a estabilidade e solidez da empresa. A redução no outlook NII para 2026 é um fator importante que já está parcialmente descontado pelos mercados.

###### O que os fundamentos sugerem
Os fundamentais atuais de JPMorgan Chase são robustos, com indicadores como o P/E e ROE superando as médias setoriais. A empresa também tem uma história consistente de crescimento dividendo ao longo dos anos, o que é um sinal positivo para investidores em busca de rendimentos sustentáveis.

###### DCF — A âncora do valor
| DCF | Não calculado 

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\JPM_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\JPM_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — JPM             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              7
  Entry price.........: US$      306.56
  Cost basis..........: US$    2,145.89
  Price now...........: US$      308.28
  Market value now....: US$    2,157.96  [+0.6% nao-realizado]
  DY t12m.............: 1.91%  (R$/US$ 5.9000/share)
  DY vs own 10y.......: P12 [EXPENSIVE]  (actual 1.91% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=43  hist_g_5y=0.107  hist_g_raw=0.107  gordon_g=0.118  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +6.75%  |   -1.00% |   +7.66%       |
  | base         |  +11.24%  |   +0.00% |  +13.16%       |
  | optimista    |  +15.18%  |   +1.00% |  +18.09%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     23       |       32       |       10       |
  | base         |     18       |       37       |        6       |
  | optimista    |     15       |      >40       |        5       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      3,146 | US$      4,042 | US$      5,009 |
  |  10y  | US$      4,606 | US$      7,570 | US$     11,583 |
  |  15y  | US$      6,779 | US$     14,178 | US$     26,685 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\JPM.md` (cemetery archive)_

#### JPM — JPMorgan Chase

#holding #us #financials

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 6.2/10  |  **Confiança**: 60%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 6.7/10 | 35% | `███████░░░` |
| Valuation  | 6.0/10 | 30% | `██████░░░░` |
| Momentum   | 5.3/10 | 20% | `█████░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski None/9 (N/A), DivSafety 100.0/100
- **Valuation**: Screen 0.80, DY percentil P10 (EXPENSIVE)
- **Momentum**: 1d 1.78%, 30d 1.47%, YTD -3.25%
- **Narrativa**: user_note=False, YT insights 60d=3

###### Razões

- total 6.2 na zona neutra

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[GS]] · [[NU]] · [[TFC]]
- Vídeos: [[videos/2026-04-10_btg-pactual_turbulencia-global-petroleo-e-oportunidades-em-tecnologia-radar-do-inv|Turbulência global, petróleo e oportunid]] · [[videos/2026-03-17_o-primo-rico_e-se-os-eua-perderem-a-guerra-contra-o-ira-o-que-isso-significa-pro-se|E SE OS EUA PERDEREM A GUERRA CONTRA O I]]
- 🎯 **Thesis**: [[JPM|thesis deep]]

##### Snapshot

- **Preço**: $314.90  (2026-05-06)    _+1.78% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 100.0/100 (SAFE)
- **Posição**: 7.0 sh @ $306.55571428571426  →  P&L 2.72%

##### Fundamentals

- P/E: 15.081418 | P/B: 2.4528935 | DY: 1.87%
- ROE: 16.47% | EPS: 20.88 | BVPS: 128.379
- Streak div: 43y | Aristocrat: True

##### Dividendos recentes

- 2026-04-06: $1.5000
- 2026-01-06: $1.5000
- 2025-10-06: $1.5000
- 2025-07-03: $1.4000
- 2025-04-04: $1.4000

##### Eventos (SEC/CVM)

- **2026-05-07** `8-K` — 8-K | 3.03,5.03,8.01,9.01
- **2026-05-01** `10-Q` — 10-Q
- **2026-04-24** `8-K` — 8-K | 5.03
- **2026-04-23** `8-K` — 8-K | 8.01,9.01
- **2026-04-14** `8-K` — 8-K | 2.02,9.01

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Bloomberg Television | management | 0.90 | JP Morgan está reorganizando sua liderança em banco de investimentos para melhorar a colaboração entre diferentes áreas. |
| 2026-05-11 | Bloomberg Television | valuation | 0.90 | JP Morgan aumentou a meta do índice KOSPI para um cenário otimista de 10.000 pontos. |
| 2026-04-10 | BTG Pactual | operational | 0.80 | O JP Morgan irá reportar seus resultados na terça-feira, dia 14. |
| 2026-03-17 | O Primo Rico | thesis_bull | 0.80 | O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação… |
| 2026-03-17 | O Primo Rico | management | 0.70 | O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A alta inflação e os preços elevados de energia estão pressionando o Fed a manter as taxas de juros mais alta… |
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A pressão inflacionária continua alta, o que sugere que o Fed pode precisar manter as taxas de juros elevadas… |
| 2026-05-13 | Bloomberg Television | fed_path | neutral | O novo presidente do Fed, Kevin Warsh, pode mudar a forma como o Fed comunica suas decisões, mas não há indic… |
| 2026-05-13 | Bloomberg Television | oil_cycle | neutral | O preço do petróleo Brent está em torno de $107,44 e não há indicação clara sobre uma tendência bullish ou be… |
| 2026-05-13 | Bloomberg Television | real_estate_cycle | neutral | Apesar da incerteza política e econômica, Brookfield Real Estate continua ativo no mercado londrino, buscando… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -5.89%
- **Drawdown 5y**: -5.89%
- **YTD**: -3.25%
- **YoY (1y)**: +26.34%
- **CAGR 3y**: +32.06%  |  **5y**: +14.32%  |  **10y**: +17.72%
- **Vol annual**: +24.99%
- **Sharpe 3y** (rf=4%): +1.20

###### Dividendos
- **DY 5y avg**: +2.27%
- **Div CAGR 5y**: +10.67%
- **Frequency**: quarterly
- **Streak** (sem cortes): 16 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $127.73B | $37.68B | $107.12B |
| 2023-12-31 | $154.95B | $49.55B | $12.97B |
| 2024-12-31 | $169.44B | $58.47B | $-42.01B |
| 2025-12-31 | $181.85B | $57.05B | $-147.78B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "JPM — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: JPM
    data: [253.47, 265.64, 265.68, 265.29, 264.66, 265.73, 268.24, 273.96, 284.06, 290.41, 282.78, 288.7, 291.27, 296.55, 299.63, 291.37, 289.56, 290.49, 291.47, 299.28, 299.51, 297.85, 308.9, 314.78, 313.45, 310.71, 307.69, 307.97, 297.56, 294.54, 305.51, 309.25, 316.89, 303.61, 298.38, 307.64, 312.13, 300.51, 320.02, 317.21, 327.91, 325.48, 329.79, 307.87, 302.04, 300.31, 308.14, 322.4, 302.64, 308.05, 303.3, 300.26, 289.92, 283.44, 287.97, 295.42, 294.16, 297.4, 313.68, 310.29, 311.69, 311.45, 307.65]
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
    data: [14.64272, 14.758852, 14.837244, 14.860633, 15.101054, 14.983246, 14.764368, 14.750239, 14.750239, 14.910527, 14.916189, 14.796651, 14.979915, 14.720096, 14.810914, 15.081418]
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
    data: [16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47, 16.47]
  - title: DY %
    data: [1.93, 1.96, 1.94, 1.93, 1.93, 1.88, 1.91, 1.91, 1.91, 1.89, 1.89, 1.91, 1.88, 1.92, 1.91, 1.87]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\JPM_DOSSIE.md` (cemetery archive)_

#### 📑 JPM — JPMorgan Chase

> Generated **2026-04-26** by `ii dossier JPM`. Cross-links: [[JPM]] · [[JPM]] · [[CONSTITUTION]]

##### TL;DR

JPM negoceia a P/E 14.75 e P/B 2.40 com DY 1.91% e ROE 16.5%, IC HOLD com **alta confiança e 100% consenso**. Achado-chave: 43 anos de dividendos consecutivos com ROE acima do screen US (≥15%) — fortaleza de capital best-in-class entre os money-center banks. Subida YoY +26.6% sugere preço esticado para um sector cíclico — não é momento para acelerar entrada.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 20.90  |  **BVPS**: 128.38
- **ROE**: 16.47%  |  **P/E**: 14.75  |  **P/B**: 2.40
- **DY**: 1.91%  |  **Streak div**: 43y  |  **Market cap**: USD 826.04B
- **Last price**: USD 308.28 (2026-04-26)  |  **YoY**: +26.6%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 100.0% consensus)

→ Detalhe: [[JPM]]

##### 3. Thesis

**Core thesis (2026-04-24)**: JPMorgan Chase é uma excelente posição long-term para um investidor Buffett/Graham devido à sua sólida história de dividendos, com 43 anos consecutivos de aumentos e uma taxa de crescimento anual média de dividendos de 10%. A empresa possui um P/E de 14.98, que é inferior ao do setor financeiro em geral, indicando um preço justo ou subvalorizado. Além disso, o ROE de 16.47% sugere uma eficiência operacional superior e a capacidade sustentável de gerar lucros acima da média.

**Key assumptions**:
1. A taxa de dividendos (DY) permanecerá estável em torno de 1.88%.
2. O P/E continuarão abaixo do setor financeiro, mantendo o preço justo ou subvalorizado.
3. O ROE se manterá acima dos 16%, indicando eficiência operacional sustentável.
4. A empresa continuará a aume

→ Vault: [[JPM]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 14.75** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 14.75** passa.
- **P/B = 2.40** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **2.40** OK.
- **DY = 1.91%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **1.91%** fraco; verificar se é growth pick.
- **ROE = 16.47%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **16.47%** compounder-grade.
- **Graham Number ≈ R$ 245.70** vs preço **R$ 308.28** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 43y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🟡 **Sensibilidade a taxas (Fed pivot)** — NIM comprime se Fed cortar agressivamente. Trigger: `fundamentals` NII trimestral YoY < -5%.
- 🟡 **Ciclo de crédito** — provisões PDD podem disparar em recessão (consumer + IB). Trigger: charge-offs / loan book > 0.8% nos quarterlies.
- 🟡 **Pressão regulatória (Basel III endgame, capital buffer)** — pode forçar buyback freeze. Trigger: `events` table novo regulatory action.
- 🟢 **Concentração executive risk (Dimon succession)** — sucessão pendente, mercado precifica prémio Dimon.

##### 5. Position sizing

**Status atual**: holding (in portfolio)

**Manter DRIP ligado** — core financials holding, qualidade superior aos peers. P/B 2.40 é alto para banco; aguardar dips ou preferir reforçar peers em desconto. USD em conta US, sem conversão para BR.

##### 6. Tracking triggers (auto-monitoring)

- **ROE quebra screen** — `fundamentals.roe < 0.15` por 2 trimestres → degradação fundamental.
- **PE expansion** — `fundamentals.pe > 18` → premium banco difícil de justificar.
- **Dividend freeze/cut** — qualquer corte interrompe streak de 43y → tese DRIP comprometida.
- **Earnings miss** — `events.kind='earnings'` surprise < -10% → reavaliação.
- **Conviction drop** — `conviction_scores.composite_score < 60` → trim.

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
*Generated by `ii dossier JPM` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Bloomberg Television | management | 0.90 | JP Morgan está reorganizando sua liderança em banco de investimentos para melhorar a colaboração entre diferentes áreas. |
| 2026-05-11 | Bloomberg Television | valuation | 0.90 | JP Morgan aumentou a meta do índice KOSPI para um cenário otimista de 10.000 pontos. |
| 2026-04-10 | BTG Pactual | operational | 0.80 | O JP Morgan irá reportar seus resultados na terça-feira, dia 14. |
| 2026-03-17 | O Primo Rico | thesis_bull | 0.80 | O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação… |
| 2026-03-17 | O Primo Rico | management | 0.70 | O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A alta inflação e os preços elevados de energia estão pressionando o Fed a manter as taxas de juros mais alta… |
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A pressão inflacionária continua alta, o que sugere que o Fed pode precisar manter as taxas de juros elevadas… |
| 2026-05-13 | Bloomberg Television | fed_path | neutral | O novo presidente do Fed, Kevin Warsh, pode mudar a forma como o Fed comunica suas decisões, mas não há indic… |
| 2026-05-13 | Bloomberg Television | oil_cycle | neutral | O preço do petróleo Brent está em torno de $107,44 e não há indicação clara sobre uma tendência bullish ou be… |
| 2026-05-13 | Bloomberg Television | real_estate_cycle | neutral | Apesar da incerteza política e econômica, Brookfield Real Estate continua ativo no mercado londrino, buscando… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\JPM_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — JPM

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=1 | HOLD=4 | AVOID=0  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE acima de 15%
- Histórico confiável de dividendos
- Preço justo comparado ao setor

**Key risk**: Riscos regulatórios e operacionais no setor bancário

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E abaixo da média setorial
- ROE forte indicando eficiência operacional
- Histórico de dividendos robusto

**Key risk**: Ameaças regulatórias e crises no mercado de títulos podem impactar significativamente o desempenho

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável e ROE forte
- História de dividendos sólida
- Exposição a riscos sistêmicos

**Key risk**: Volatilidade do mercado de títulos pode afetar significativamente o desempenho da empresa

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- História sólida de dividendos
- ROE acima da média
- P/E abaixo do setor

**Key risk**: Riscos operacionais e regulatórios no setor financeiro

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/E abaixo da média setorial
- ROE forte indicando eficiência operacional
- Histórico de dividendos robusto

**Key risk**: Risco sistêmico em mercado de títulos conforme alertado por Jamie Dimon

##### 📊 Context provided

```
TICKER: US:JPM

FUNDAMENTALS LATEST:
  pe: 14.461466
  pb: 2.3531888
  dy: 1.95%
  roe: 16.47%
  intangible_pct_assets: 1.5%   (goodwill $52.7B + intangibles $11.7B)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: JPMorgan Chase é uma excelente posição long-term para um investidor Buffett/Graham devido à sua sólida história de dividendos, com 43 anos consecutivos de aumentos e uma taxa de crescimento anual média de dividendos de 10%. A empresa possui um P/E de 14.98, que é inferior ao do setor financeiro em geral, indicando um preço justo ou subvalorizado. Além disso, o ROE de 16.47% sugere uma eficiência operacional superior e a capacidade sustentável de gerar lucros acima da média.

**Key assumptions**:
1. A taxa de dividendos (DY) permanecerá estável em torno de 1.88%.
2. O P/E continuarão abaixo do setor financeiro, mantendo o preço justo ou subvalorizado.
3. O ROE se manterá acima dos 16%, indicando eficiência operacional sustentável.
4. A empresa continuará a aume

RECENT MATERIAL NEWS (last 14d via Tavily):
  - JP Morgan's Jamie Dimon warns of looming bond market crisis (JPM:NYSE) - Seeking Alpha [Tue, 28 Ap]
    Home page Seeking Alpha - Power to Investors. Search for Symbols, analysts, keywords. # JP Morgan's Jamie Dimon warns of looming bond market crisis. Apr 28, 2026, 3:19 PM ETJPMorgan Chase & Co. (JPM) 
  - JPMorgan Tried to Settle Sexual-Assault Claims That Went Viral - WSJ [Wed, 06 Ma]
    # JPMorgan Tried to Settle Sexual-Assault Claims, Iran and U.S. Move Closer to Talks, and Mistakes Yield Beloved Innovations | What’s News for May 6 - WSJ. S&P GSCI Index Spot 735.10 -3.93%. https://w
  - JPMorgan to become global partner of 2028 Olympics, 2030 Winter Games - Reuters [Tue, 28 Ap]
    REUTERS/Eduardo Munoz/File Photo Purchase Licensing Rights, opens new tab. NEW YORK, April 28 (Reuters) - JPMorgan Chase (JPM.N), opens new tab on Tuesday announced a partnership with ​the Intern
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Bloomberg Television | management | 0.90 | JP Morgan está reorganizando sua liderança em banco de investimentos para melhorar a colaboração entre diferentes áreas. |
| 2026-05-11 | Bloomberg Television | valuation | 0.90 | JP Morgan aumentou a meta do índice KOSPI para um cenário otimista de 10.000 pontos. |
| 2026-04-10 | BTG Pactual | operational | 0.80 | O JP Morgan irá reportar seus resultados na terça-feira, dia 14. |
| 2026-03-17 | O Primo Rico | thesis_bull | 0.80 | O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação… |
| 2026-03-17 | O Primo Rico | management | 0.70 | O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A alta inflação e os preços elevados de energia estão pressionando o Fed a manter as taxas de juros mais alta… |
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A pressão inflacionária continua alta, o que sugere que o Fed pode precisar manter as taxas de juros elevadas… |
| 2026-05-13 | Bloomberg Television | fed_path | neutral | O novo presidente do Fed, Kevin Warsh, pode mudar a forma como o Fed comunica suas decisões, mas não há indic… |
| 2026-05-13 | Bloomberg Television | oil_cycle | neutral | O preço do petróleo Brent está em torno de $107,44 e não há indicação clara sobre uma tendência bullish ou be… |
| 2026-05-13 | Bloomberg Television | real_estate_cycle | neutral | Apesar da incerteza política e econômica, Brookfield Real Estate continua ativo no mercado londrino, buscando… |

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\JPM_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — JPM

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `low_consensus_long` (magnitude 1/5)  
**Interpretation**: consensus pick — no edge

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: bullish (4 bull / 1 bear / 0 neutral)  
**Cached**: True

- 🔴 [bear] [JPMorgan has stark message for investors on Meta stock - thestreet.com](https://www.thestreet.com/investing/stocks/jpmorgan-has-stark-message-for-investors-on-meta-stock) (Fri, 01 Ma)
- 🟢 [bull] [JPMorgan just boosted its S&P 500 target on fresh AI excitement and big earnings expectations - Business Insider](https://www.businessinsider.com/stock-market-today-earnings-ai-trade-investing-bull-price-target-2026-4) (Tue, 21 Ap)
- 🟢 [bull] [TSMC Q1 Revenue Surges 35% — Is TSM Stock Still a Buy Ahead of Earnings? - TipRanks](https://www.tipranks.com/news/tsmc-q1-revenue-surges-35-is-tsm-stock-still-a-buy-ahead-of-earnings) (Fri, 10 Ap)
- 🟢 [bull] [JPMorgan's best stock ideas heading into May - CNBC](https://www.cnbc.com/2026/05/02/jpmorgans-best-stock-ideas-heading-into-may.html) (Sat, 02 Ma)
- 🟢 [bull] [JPMorgan Chase Q1 earnings beat, but NII outlook trimmed (JPM:NYSE) - Seeking Alpha](https://seekingalpha.com/news/4574690-jpmorgan-chase-q1-earnings-beat-but-nii-outlook-trimmed) (Tue, 14 Ap)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: JPMorgan Chase é uma excelente posição long-term para um investidor Buffett/Graham devido à sua sólida história de dividendos, com 43 anos consecutivos de aumentos e uma taxa de crescimento anual média de dividendos de 10%. A empresa possui um P/E de 14.98, que é inferior ao do setor financeiro em geral, indicando um preço justo ou subvalorizado. Além disso, o ROE de 16.47% sugere uma eficiência operacional superior e a capacidade sustentável de gerar lucros acima da média.

**Key assumptions**:
1. A taxa de dividendos (DY) permanecerá estável em torno de 1.88%.
2. O P/E continuarão abaixo do setor financeiro, mantendo o preço justo ou subvalorizado.
3. O ROE se manterá acima dos 16%, indicando eficiência operacional sustentável.
4. A empresa continuará a aume

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Bloomberg Television | management | 0.90 | JP Morgan está reorganizando sua liderança em banco de investimentos para melhorar a colaboração entre diferentes áreas. |
| 2026-05-11 | Bloomberg Television | valuation | 0.90 | JP Morgan aumentou a meta do índice KOSPI para um cenário otimista de 10.000 pontos. |
| 2026-04-10 | BTG Pactual | operational | 0.80 | O JP Morgan irá reportar seus resultados na terça-feira, dia 14. |
| 2026-03-17 | O Primo Rico | thesis_bull | 0.80 | O JP Morgan recomenda diversificação geográfica de carteiras, indicando que a Europa e os mercados emergentes estão descontados em relação… |
| 2026-03-17 | O Primo Rico | management | 0.70 | O JP Morgan Private Bank recomenda aos clientes que saiam da dependência total de um único mercado e diversifiquem geograficamente. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A alta inflação e os preços elevados de energia estão pressionando o Fed a manter as taxas de juros mais alta… |
| 2026-05-13 | Bloomberg Television | fed_path | bearish | A pressão inflacionária continua alta, o que sugere que o Fed pode precisar manter as taxas de juros elevadas… |
| 2026-05-13 | Bloomberg Television | fed_path | neutral | O novo presidente do Fed, Kevin Warsh, pode mudar a forma como o Fed comunica suas decisões, mas não há indic… |
| 2026-05-13 | Bloomberg Television | oil_cycle | neutral | O preço do petróleo Brent está em torno de $107,44 e não há indicação clara sobre uma tendência bullish ou be… |
| 2026-05-13 | Bloomberg Television | real_estate_cycle | neutral | Apesar da incerteza política e econômica, Brookfield Real Estate continua ativo no mercado londrino, buscando… |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\JPM.md` (cemetery archive)_

#### 🎯 Thesis: [[JPM]] — JPMorgan Chase

> Best-in-class US bank — Dimon leadership 20+ years. Core DRIP US financials.

##### Intent
**DRIP core US** — US bank pilar. Combined with [[JNJ]], [[KO]], [[PG]] foundation.

##### Business snapshot
- **Consumer & Community Banking** (Chase retail + cards)
- **Corporate & Investment Bank** (#1 or #2 globally most segments)
- **Commercial Banking**
- **Asset & Wealth Management** ($4T+ AUM)

US market cap ranking: top-3 always. Often #1 by revenue + profit among banks.

##### Por que detemos

1. **Dimon leadership** (CEO 2006-present) — navegou GFC + COVID + 2023 bank crisis sem drama.
2. **Best-in-class ROE** 17-20% (industry avg 12-14%).
3. **Scale moat** — trading volumes + IB deal flow + deposit base impossible replicate.
4. **Fortress balance sheet** — over-capitalised post-GFC.
5. **Dividend 15y+ streak** (broken briefly in 2020 Fed stress test halt).

##### Moat

- **Deposit franchise** — $2.4T+ deposits, sticky (retail + corporate cash management).
- **Network effects IB** — clients go to JPM because JPM has liquidity; liquidity is there because clients are.
- **Technology moat** — $15B+/y IT spend, proprietary risk systems.
- **Regulatory relationships** decades-deep.
- **Weak moat**: regulatory environment variável (capital requirements flip-flop).

##### Current state (2026-04)

- Net Interest Income benefitting Fed hikes cycle + careful ALM.
- Credit quality excellent — NPLs < 0.6%.
- Buyback + dividend increases recent cycles.
- First Republic acquisition 2023 = accretive bargain.
- Wealth management growing organically.

##### Invalidation triggers

- [ ] Dimon departure sem succession plan executed (key-person risk moderate)
- [ ] ROE < 12% 2 years (structural decline signal)
- [ ] Major trading loss > $5B single quarter (risk management fail)
- [ ] Major regulatory fine > $10B systemic
- [ ] Fed stress test fail → buyback/dividend halt (as 2020 COVID)
- [ ] Accounting restatement

##### Sizing

- Posição actual: 7 shares
- Target 3-5% sleeve US
- Reinvest dividends DRIP auto

##### US bank peer comparison

| Ticker | ROE | P/B | Trait |
|---|---|---|---|
| **JPM** | 18% | 2.0× | Best-in-class diversified |
| BAC | 12% | 1.2× | Rate-sensitive Main Street |
| C | 8% | 0.6× | Turnaround troubled |
| WFC | 11% | 1.2× | Account scandals legacy |
| [[GS]] | 14% | 1.3× | Pure IB + trading |
| MS | 14% | 1.8× | Wealth management pivot |
| [[BLK]] | N/A (asset manager) | 4× P/B-like | Fee-based |

JPM vs others = premium justified by ROE + diversification + leadership.


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -6.91%
- **Drawdown 5y**: -6.91%
- **YTD**: -4.30%
- **YoY (1y)**: +29.31%
- **CAGR 3y**: +30.32%  |  **5y**: +15.71%  |  **10y**: +17.22%
- **Vol annual**: +25.20%
- **Sharpe 3y** (rf=4%): +1.13

###### Dividendos
- **DY 5y avg**: +2.27%
- **Div CAGR 5y**: +10.67%
- **Frequency**: quarterly
- **Streak** (sem cortes): 16 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[BR_Banks]] — comparativo BR vs US banks (structural differences)
- [[BLK]] — peer US financial (asset manager, not bank)
- [[GS]] — peer IB-heavy
- [[Buffett_quality]] — JPM canonical Buffett pick (post-2020)
- [[Dividend_withholding_BR_US]] — tax 30% US withhold para PF BR

## ⚙️ Refresh commands

```bash
ii panorama JPM --write
ii deepdive JPM --save-obsidian
ii verdict JPM --narrate --write
ii fv JPM
python -m analytics.fair_value_forward --ticker JPM
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
