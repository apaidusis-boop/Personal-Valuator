---
type: ticker_hub
ticker: GS
market: us
sector: Financials
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 15
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# GS — Goldman Sachs

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: holdings` · `15 sources merged`

## 🎯 Hoje

- **Posição**: 1.0 @ entry 318.83
- **Verdict (DB)**: `HOLD` (score 5.92, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 17.44 · P/B 2.68 · DY 2.1% · ROE 14.5% · Dividend streak 28 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\GS.md` (now in cemetery)_

#### GS — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://www.goldmansachs.com/investor-relations/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=318.83 · date=2023-07-11

- Total events na DB: **20**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=944.8599853515625
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.14548 · DY=0.021167157367298628 · P/E=17.248266
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 9.01 |
| 2026-04-13 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-03-20 | proxy | sec | DEF 14A |

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
_source: `dossiers\GS_FILING_2026-05-12.md` (now in cemetery)_

#### Filing dossier — [[GS]] · 2026-05-12

**Trigger**: `sec:8-K` no dia `2026-05-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/886982/000119312526219511/d142159d8k.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 953.40

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `532.48` |
| HOLD entre | `532.48` — `682.67` (consensus) |
| TRIM entre | `682.67` — `785.07` |
| **SELL acima de** | `785.07` |

_Método: `us_bank_pe12`. Consensus fair = R$682.67. Our fair (mais conservador) = R$532.48._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.14548` | `0.1457` | +0.1% |
| EPS | `54.77` | `56.8892` | +3.7% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 953.40 | SELL | cross_validated | `filing:sec:8-K:2026-05-12` |
| 2026-05-13T16:45:13+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 953.40 | SELL | cross_validated | `manual` |
| 2026-05-11T20:40:44+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 944.86 | SELL | cross_validated | `manual` |
| 2026-05-11T12:53:42+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 936.48 | SELL | cross_validated | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:18+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 936.48 | SELL | cross_validated | `manual` |
| 2026-05-09T20:37:09+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 936.48 | SELL | cross_validated | `manual` |
| 2026-05-09T13:08:34+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 936.48 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `us_bank_pe12` | 682.67 | 532.48 | 936.48 | SELL | cross_validated | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-05-01 · Council review · Hank Tier-One
_source: `agents\Hank Tier-One\reviews\GS_2026-05-01.md` (now in cemetery)_

#### Hank Tier-One sobre [[GS_STORY|GS]]

**Função no debate**: Banks US Specialist (`sector_specialist`)  
**Data**: 2026-05-01  
**Stance final**: 🔴 **AVOID**  

##### Round 1 — Abertura (cega aos colegas)

> _P/E e P/B acima do limite; ROE abaixo da média setorial_

GS tem um P/E de 16.86x, acima do limite de 12x, e um P/B de 2.57x, além do limite de 1.8x. O ROE está abaixo da média setorial (14.6% vs 16.5%).

**Métricas que invoquei**:
- P/E=16.86
- P/B=2.57
- ROE=14.6%

**Preocupações**:
- Volatilidade do negócio de taxas devido à guerra do Irã
- Dividend yield baixo (1.7%)

**Veto signals**:
- 🚫 P/B simples sobrestima o valor real

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 19.8% no Q1 é forte
- Mariana Macro

**Desafiei**:
- P/E e P/B acima do limite não são aceitáveis mesmo com ROE forte
- Pedro Alocação

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[GS_STORY|📖 Storytelling completo (8 actos)]]
- [[GS_COUNCIL|🏛️ Transcript do Council debate]]
- [[Hank Tier-One|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Mariana Macro
_source: `agents\Mariana Macro\reviews\GS_2026-05-01.md` (now in cemetery)_

#### Mariana Macro sobre [[GS_STORY|GS]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Strong earnings growth but geopolitical risks persist_

Goldman Sachs reports robust Q1 earnings with ROE of 19.8%, yet faces volatility from Iran war impacting fixed-income business.

**Métricas que invoquei**:
- ROE=14.6%
- P/E=16.86
- DY=1.7%

**Preocupações**:
- Iran war volatility affecting rates business
- Geopolitical risks to global trade and finance

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média - Valentina Prudente

**Desafiei**:
- P/B simples sobrestima o valor real - Hank Tier-One; razão: O uso de métricas simplistas como P/B pode não capturar completamente a complexidade dos ativos intangíveis e goodwill em empresas financeiras, especialmente quando enfrentam volatilidades geopolíticas

##### Quem mais estava na sala

- [[Hank Tier-One]] (Banks US Specialist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[GS_STORY|📖 Storytelling completo (8 actos)]]
- [[GS_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Pedro Alocação
_source: `agents\Pedro Alocação\reviews\GS_2026-05-01.md` (now in cemetery)_

#### Pedro Alocação sobre [[GS_STORY|GS]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Goldman Sachs mantém-se atraente com sólidos fundamentos financeiros_

A empresa apresenta um ROE de 14.6% e P/E de 16.86, acima da média do setor, refletindo uma posição forte no mercado.

**Métricas que invoquei**:
- ROE=14.6%
- P/E=16.86
- DivStreak=28

**Preocupações**:
- impacto potencial de volatilidade geopolítica
- peso na carteira acima do recomendado

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média - Mariana Macro

**Desafiei**:
- GS tem um P/E de 16.86x, acima do limite de 12x, e um P/B de 2.57x, além do limite de 1.8x - Hank Tier-One | Estes limites são rígidos demais para uma instituição financeira líder como GS

##### Quem mais estava na sala

- [[Hank Tier-One]] (Banks US Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[GS_STORY|📖 Storytelling completo (8 actos)]]
- [[GS_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*

#### 2026-05-01 · Council review · Valentina Prudente
_source: `agents\Valentina Prudente\reviews\GS_2026-05-01.md` (now in cemetery)_

#### Valentina Prudente sobre [[GS_STORY|GS]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-05-01  
**Stance final**: 🟡 **HOLD**  

##### Round 1 — Abertura (cega aos colegas)

> _Goldman Sachs mantém posição de HOLD com riscos geopolíticos_

ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média. Riscos geopolíticos impactam negativamente.

**Métricas que invoquei**:
- ROE: 14,6%
- P/E: 16,86
- DY: 1,7%

**Preocupações**:
- Impacto de conflitos geopolíticos no negócio da empresa
- Desempenho abaixo da média do setor em termos de ROE

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ROE de 19.8% é forte - Mariana Macro

**Desafiei**:
- P/E e P/B acima do limite; ROE abaixo da média setorial - Veto: a métrica P/B sobrestima o valor real por não considerar goodwill significativo
- Volatilidade do negócio de taxas devido à guerra do Irã - A volatilidade é temporária e não indica perda permanente de capital

##### Quem mais estava na sala

- [[Hank Tier-One]] (Banks US Specialist)
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[GS_STORY|📖 Storytelling completo (8 actos)]]
- [[GS_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-05-01` — STORYT_2.0 Camada 5.5*


### (undated)

#### — · DRIP scenarios
_source: `briefings\drip_scenarios\GS_drip.md` (now in cemetery)_

/============================================================================\
|   DRIP SCENARIO — GS              moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              1
  Entry price.........: US$      318.83
  Cost basis..........: US$      318.83
  Price now...........: US$      926.91
  Market value now....: US$      926.91  [+190.7% nao-realizado]
  DY t12m.............: 1.67%  (R$/US$ 15.5000/share)
  DY vs own 10y.......: P46 [fair-rich]  (actual 1.67% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=28  hist_g_5y=0.209  hist_g_raw=0.211  gordon_g=0.105  is_quality=True  capped=True

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +9.42%  |   -1.00% |  +10.09%       |
  | base         |  +15.69%  |   +0.00% |  +17.37%       |
  | optimista    |  +21.19%  |   +1.00% |  +23.86%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     12       |       36       |        1       |
  | base         |     10       |      >40       |        1       |
  | optimista    |      8       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,512 | US$      2,087 | US$      2,737 |
  |  10y  | US$      2,476 | US$      4,701 | US$      8,057 |
  |  15y  | US$      4,071 | US$     10,586 | US$     23,641 |
  --------------------------------------------------------------------------

#### — · Council aggregate
_source: `dossiers\GS_COUNCIL.md` (now in cemetery)_

#### Council Debate — [[GS_STORY|GS]] (Goldman Sachs)

**Final stance**: 🔴 **AVOID**  
**Confidence**: `low`  
**Modo (auto)**: B (US)  |  **Sector**: Financials  |  **Held**: sim  
**Elapsed**: 59.2s  |  **Failures**: 0

##### Quem esteve na sala

- [[Hank Tier-One]] — _Banks US Specialist_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- ROE de 14,6% está abaixo da mediana do setor (16,5%) - Mariana Macro, Valentina Prudente
- P/E de 16,86 é ligeiramente acima da média - Mariana Macro, Pedro Alocação

**Dissenso (preservado)**:
- Hank Tier-One disse que P/B simples sobrestima o valor real, enquanto Mariana Macro concorda com a avaliação de risco geopolítico
- Pedro Alocação disse que os limites são rígidos demais para uma instituição financeira líder como GS, enquanto Hank Tier-One discorda

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ P/B simples sobrestima o valor real - Hank Tier-One
- ⚠️ Limites de P/E e P/B são rígidos demais para uma instituição financeira líder como GS - Pedro Alocação

**Sizing**: Considerar reduzir a posição na carteira, mantendo entre 2-3% do total

##### Round 1 — Opening Statements (blind)

###### [[Hank Tier-One]] — 🔴 **AVOID**
_Banks US Specialist_

**Headline**: _P/E e P/B acima do limite; ROE abaixo da média setorial_

GS tem um P/E de 16.86x, acima do limite de 12x, e um P/B de 2.57x, além do limite de 1.8x. O ROE está abaixo da média setorial (14.6% vs 16.5%).

**Métricas**:
- P/E=16.86
- P/B=2.57
- ROE=14.6%

**Preocupações**:
- Volatilidade do negócio de taxas devido à guerra do Irã
- Dividend yield baixo (1.7%)

**Veto signals**:
- 🚫 P/B simples sobrestima o valor real

###### [[Mariana Macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Headline**: _Strong earnings growth but geopolitical risks persist_

Goldman Sachs reports robust Q1 earnings with ROE of 19.8%, yet faces volatility from Iran war impacting fixed-income business.

**Métricas**:
- ROE=14.6%
- P/E=16.86
- DY=1.7%

**Preocupações**:
- Iran war volatility affecting rates business
- Geopolitical risks to global trade and finance

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Headline**: _Goldman Sachs mantém posição de HOLD com riscos geopolíticos_

ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média. Riscos geopolíticos impactam negativamente.

**Métricas**:
- ROE: 14,6%
- P/E: 16,86
- DY: 1,7%

**Preocupações**:
- Impacto de conflitos geopolíticos no negócio da empresa
- Desempenho abaixo da média do setor em termos de ROE

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Goldman Sachs mantém-se atraente com sólidos fundamentos financeiros_

A empresa apresenta um ROE de 14.6% e P/E de 16.86, acima da média do setor, refletindo uma posição forte no mercado.

**Métricas**:
- ROE=14.6%
- P/E=16.86
- DivStreak=28

**Preocupações**:
- impacto potencial de volatilidade geopolítica
- peso na carteira acima do recomendado

##### Round 2 — Respostas (peers visíveis)

###### [[Hank Tier-One]] — 🔴 **AVOID**
_Banks US Specialist_

**Concordou com**:
- ROE de 19.8% no Q1 é forte
- Mariana Macro

**Desafiou**:
- P/E e P/B acima do limite não são aceitáveis mesmo com ROE forte
- Pedro Alocação

###### [[Mariana Macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Concordou com**:
- ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média - Valentina Prudente

**Desafiou**:
- P/B simples sobrestima o valor real - Hank Tier-One; razão: O uso de métricas simplistas como P/B pode não capturar completamente a complexidade dos ativos intangíveis e goodwill em empresas financeiras, especialmente quando enfrentam volatilidades geopolíticas

###### [[Valentina Prudente]] — 🟡 **HOLD**
_Chief Risk Officer_

**Concordou com**:
- ROE de 19.8% é forte - Mariana Macro

**Desafiou**:
- P/E e P/B acima do limite; ROE abaixo da média setorial - Veto: a métrica P/B sobrestima o valor real por não considerar goodwill significativo
- Volatilidade do negócio de taxas devido à guerra do Irã - A volatilidade é temporária e não indica perda permanente de capital

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- ROE de 14,6% está abaixo da mediana do setor (16,5%), enquanto P/E de 16,86 é ligeiramente acima da média - Mariana Macro

**Desafiou**:
- GS tem um P/E de 16.86x, acima do limite de 12x, e um P/B de 2.57x, além do limite de 1.8x - Hank Tier-One | Estes limites são rígidos demais para uma instituição financeira líder como GS

##### Documentos relacionados

- [[GS_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[GS_2026-05-01|Hank Tier-One]] em [[Hank Tier-One]]/reviews/
  - [[GS_2026-05-01|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[GS_2026-05-01|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[GS_2026-05-01|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:GS — Goldman Sachs ===
Sector: Financials  |  Modo (auto): B  |  Held: True
Last price: 923.77001953125 (2026-04-30)
Position: 1 shares @ entry 318.83
Fundamentals: P/E=16.86 | P/B=2.57 | DY=1.7% | ROE=14.6% | DivStreak=28.00

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 4.1%
  Sector weight: 27.1%

WEB CONTEXT (qualitative research, last 30-90d):
  - Goldman Sachs rates business hit by Iran war volatility, sources say - Reuters [Thu, 16 Ap]
    # Goldman Sachs rates business hit by Iran war volatility, sources say | Reuters. NEW YORK, April 15 (Reuters) - Goldman Sachs' (GS.N), opens new tab rates business suffered losses on some positions towards the end of the ‌last quarter as f
  - Short Squeeze Fuels Market Rally as Bears Rush to Cover - TipRanks [Sat, 18 Ap]
    # Short Squeeze Fuels Market Rally as Bears Rush to Cover. * One of the biggest drivers of the market’s recent rally appears to be short covering. * A basket of heavily shorted stocks tracked by Goldman Sachs jumped by more than 13% this we
  - Here are Friday's biggest analyst calls: Nvidia, Apple, Netflix, JPMorgan, Affirm, UnitedHealth, WeRide & more - CNBC [Fri, 17 Ap]
    GS remains Buy-rated." RBC initiates Woodward at outperform RBC said the aerospace and defense company is best positioned. "We are initiating coverage of Woodward ( WWD) at Outperform and a $450 price target." Bank of America reiterates Net
  - Goldman Sachs sees prolonged Iran War hurting China's export growth this year - CNBC [Mon, 20 Ap]
    Monday - Friday, 10:00 - 11:00 SIN/HK | 0400 - 05:00 CET. # Goldman Sachs sees prolonged Iran War hurting China's export growth this year. Hui Shan, Chief China Economist at Goldman Sachs, provides an outlook for China's economy for the rem
  - Healthy earnings backdrop remains due to AI investment and hyperscalers: Goldman Sachs AM - CNBC [Thu, 23 Ap]
    # Healthy earnings backdrop remains due to AI investment and hyperscalers: Goldman Sachs AM. Luke Barrs, Chief Business Officer, Fundamental Equity at Goldman Sachs Asset Management, thinks that earnings expectations continue to remain high
  - Goldman Sachs Reports 2026 First Quarter Earnings Per Common Share of $17.55 and Annualized Return on Common Equity of 19.8% - Goldman Sachs [Mon, 13 Ap]
    # Goldman Sachs Reports 2026 First Quarter Earnings Per Common Share of $17.55 and Annualized Return on Common Equity of 19.8%. Diluted earnings per common share (EPS) was $17.55 and annualized return on average common shareholders’ equity 

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[1] sec (8-K) [2026-04-20]: 8-K | 9.01
     URL: https://www.sec.gov/Archives/edgar/data/886982/000119312526164058/d122102d8k.htm
[2] sec (8-K) [2026-04-13]: 8-K | 2.02,7.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/886982/000088698226000096/gs-20260413.htm
[3] sec (proxy) [2026-03-20]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/886982/000119312526117433/gs-20260319.htm
[4] sec (8-K) [2026-03-13]: 8-K | 5.02
     URL: https://www.sec.gov/Archives/edgar/data/886982/000119312526105328/gs-20260309.htm
[5] sec (8-K) [2026-03-05]: 8-K | 9.01
     URL: https://www.sec.gov/Archives/edgar/data/886982/000119312526094047/d926033d8k.htm
[6] sec (10-K) [2026-02-25]: 10-K
     URL: https://www.sec.gov/Archives/edgar/data/886982/000088698226000091/gs-20251231.htm

##### YOUTUBE INSIGHTS (transcripts ingeridos) (8 hits)
[7] YouTube Virtual Asset [2026-04-14] (valuation): Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00.
     URL: https://www.youtube.com/watch?v=UZHTffhDF8Y
[8] YouTube O Primo Rico [2026-04-14] (guidance): O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável.
     URL: https://www.youtube.com/watch?v=dgqAHfvcPYs
[9] YouTube Virtual Asset [2026-04-14] (valuation): Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00.
     URL: https://www.youtube.com/watch?v=UZHTffhDF8Y
[10] YouTube O Primo Rico [2026-04-14] (guidance): O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável.
     URL: https://www.youtube.com/watch?v=dgqAHfvcPYs
[11] YouTube Suno Notícias [2025-08-01] (guidance): Goldman Sachs reduziu a estimativa de lucro líquido para o Banco do Brasil, agora projetando R$4,9 bilhões.
     URL: https://www.youtube.com/watch?v=6_On_fZLA_E
[12] YouTube Suno Notícias [2025-08-01] (guidance): Goldman Sachs tem uma avaliação mais conservadora para os resultados do Itaú, estimando um lucro líquido de R$11,3 bilhões.
     URL: https://www.youtube.com/watch?v=6_On_fZLA_E

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[13] Bibliotheca: investment_valuation_3rd_edition: estments and the expected excess returns to equity investors from these and future investments.
The most interesting aspect of this model is its focus on excess returns. A firm that invests its equity

and earns just the fair-market rate of return on these investments should see the market value of 
[14] Bibliotheca: investment_valuation_3rd_edition: . Using the average beta of 1.20, reported by investment
banks in 2010, in conjunction with a Treasury bond rate of 3.5% and an equity risk premium of 5%, yields a cost of equity of
9.5% for the firm:

In 2010, Goldman earned net income of $8,354 million, which in conjunction with the book value of 
[15] Bibliotheca: investment_valuation_3rd_edition: uity (FCFE)
dividend discount model valuation and
dividends and
earnings and
estimating growth in
explanation of
FCFF model compared with
financial service firms and
firm payout and
growth in
negative

separate valuation and
Free cash flow to equity (FCFE) valuation models
constant growth
E (three-s
[16] Bibliotheca: principles_for_navigating_big_debt_crises_by_ray_d: -Pound Total 
–New York Times 
October 30, 1929
Reserve Board Finds Action Unnecessary: 
Six-Hour Session Brings No Change in the 
New York Rediscount Rate, Officials Are 
Optimistic 
–New York Times 

Part 2: US Debt Crisis and Adjustment (1928–1937)
58
from brokers whose loans from corporations we
[17] Bibliotheca: principles_for_navigating_big_debt_crises_by_ray_d: mid 
2001 to 2006
Inﬂation
Short Rate
0%
2%
4%
6%
8%
00 02 04 06
Long term interest
rates ﬂat even as
short term rates rise
Inﬂation
Long Rate
-4%
-3%
-2%
-1%
0%
1%
2%
00 02 04 06
Short Rate–Long Rate

News & 
Bridgewater Daily Observations 
(BDO)
April 19, 2006
Fed Signals Policy Shift on Rates
“Th

##### TAVILY NEWS (≤30d) (5 hits)
[18] Tavily [Thu, 16 Ap]: # Goldman Sachs rates business hit by Iran war volatility, sources say | Reuters. NEW YORK, April 15 (Reuters) - Goldman Sachs' (GS.N), opens new tab rates business suffered losses on some positions towards the end of the ‌last quarter as fixed-income market volatility due to the Iran war forced it 
     URL: https://www.reuters.com/business/goldman-sachs-rates-business-hit-by-iran-war-volatility-sources-say-2026-04-16/
[19] Tavily [Sat, 18 Ap]: # Short Squeeze Fuels Market Rally as Bears Rush to Cover. * One of the biggest drivers of the market’s recent rally appears to be short covering. * A basket of heavily shorted stocks tracked by Goldman Sachs jumped by more than 13% this week. One of the biggest drivers of the market’s recent rally 
     URL: https://www.tipranks.com/news/short-squeeze-fuels-market-rally-as-bears-rush-to-cover
[20] Tavily [Fri, 17 Ap]: GS remains Buy-rated." RBC initiates Woodward at outperform RBC said the aerospace and defense company is best positioned. "We are initiating coverage of Woodward ( WWD) at Outperform and a $450 price target." Bank of America reiterates Netflix as buy Bank of America said it's sticking with Netflix 
     URL: https://www.cnbc.com/2026/04/17/friday-stock-calls-by-analyst-include-nvidia-apple-netflix-affirm.html
[21] Tavily [Thu, 23 Ap]: # Healthy earnings backdrop remains due to AI investment and hyperscalers: Goldman Sachs AM. Luke Barrs, Chief Business Officer, Fundamental Equity at Goldman Sachs Asset Management, thinks that earnings expectations continue to remain high, but there will be a differentiation among firms that can o
     URL: https://www.cnbc.com/video/2026/04/23/healthy-earnings-backdrop-ai-investment-hyperscalers-goldman-sachs.html
[22] Tavily [Wed, 15 Ap]: US banks from Goldman Sachs to JPMorgan, Bank of America and Citi have reported first quarter results this week and they are fine indeed. First quarter M&A revenues rose nearly 90% year-on-year at Goldman Sachs and over 80% at JPMorgan. Barnum said M&A deals benefitted from "accelerated timing" than
     URL: https://www.efinancialcareers.com/news/banking-jobs-2026

##### TAVILY GUIDANCE (≤90d) (5 hits)
[23] Tavily [Mon, 20 Ap]: Monday - Friday, 10:00 - 11:00 SIN/HK | 0400 - 05:00 CET. # Goldman Sachs sees prolonged Iran War hurting China's export growth this year. Hui Shan, Chief China Economist at Goldman Sachs, provides an outlook for China's economy for the remainder of 2026. She discusses the contrast between domestic 
     URL: https://www.cnbc.com/video/2026/04/20/prolonged-iran-war-hurt-chinas-export-growth-goldman-sachs.html
[24] Tavily [Thu, 23 Ap]: # Healthy earnings backdrop remains due to AI investment and hyperscalers: Goldman Sachs AM. Luke Barrs, Chief Business Officer, Fundamental Equity at Goldman Sachs Asset Management, thinks that earnings expectations continue to remain high, but there will be a differentiation among firms that can o
     URL: https://www.cnbc.com/video/2026/04/23/healthy-earnings-bac

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\GS_COUNCIL.md`)_

#### — · Story
_source: `dossiers\GS_STORY.md` (now in cemetery)_

#### Goldman Sachs — GS

##### Análise de Investimento · Modo FULL · Jurisdição US

*1 de Maio de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo B-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[Hank Tier-One]] — _Banks US Specialist_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/GS_2026-05-01.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 58.3 bi · FCF R$ -47.22 bi · ROE 15% · DGR 30.1% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** |  |
| **5 — Classification** | Modo B-US ·  |
| **5.5 — Council Debate** | AVOID (low) · 2 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo B-US sob a Jurisdição US. Goldman Sachs, com ticker GS e pertencente ao sector Financials, é uma das instituições financeiras mais prestigiadas do mundo. Fundada em Nova Iorque, a empresa oferece uma gama de serviços financeiros que incluem investimento bancário, gestão de ativos, finanças corporativas e serviços para clientes privados. A Goldman Sachs tem um papel significativo no mercado global, sendo conhecida não apenas pela sua robusta presença nas operações de investimento e banca de investimentos, mas também por suas capacidades em gestão de riscos e análise macroeconómica.

Uma armadilha comum para os investidores ao avaliar a Goldman Sachs é confundir o seu prestígio e alcance global com uma vantagem competitiva inata. Embora seja verdade que a empresa possui um histórico sólido e uma reputação estabelecida, sua posição no mercado depende em grande parte de suas capacidades operacionais, estratégias de investimento e adaptação às mudanças regulatórias e económicas globais.

Competitivamente, a Goldman Sachs enfrenta desafios significativos de outros grandes bancos de investimentos como Morgan Stanley e JPMorgan Chase. No entanto, sua especialização em certas áreas, como a gestão de ativos para clientes institucionais e privados, lhe confere uma posição distintiva no mercado financeiro.

##### Ato 2 — O Contexto

O cenário macroeconómico atual é caracterizado por um fundo interbancário (Fed Funds) entre 4.25% e 4.50%, com a taxa de juros do Tesouro dos EUA para o prazo de dez anos em torno de 4,2%. O custo de capital próprio (Ke) está estimado em cerca de 10%, indicando um ambiente desafiador para as empresas financeiras que buscam maximizar seus retornos sobre o capital investido. Além disso, a economia global encontra-se no final do ciclo de expansão e início da fase de enfraquecimento.

Para Goldman Sachs, este contexto macroeconómico apresenta tanto desafios quanto oportunidades. A volatilidade nos mercados financeiros, especialmente em decorrência das tensões geopolíticas associadas à guerra entre o Irã e outros países, tem impactado negativamente a performance da empresa em certas áreas de negócio. Por exemplo, a divisão de taxas da Goldman Sachs sofreu perdas significativas no último trimestre devido ao aumento da volatilidade nos mercados de renda fixa.

No entanto, o ambiente macro também oferece oportunidades para investimentos estratégicos e inovação tecnológica. A empresa tem destacado a importância do investimento em inteligência artificial (IA) e na eficiência operacional como fatores críticos para manter um bom desempenho nos próximos trimestres. Além disso, o crescimento das empresas de nuvem escaláveis (hyperscalers) continua a ser uma fonte importante de lucros para Goldman Sachs.

Em termos regulatórios, não foram identificadas mudanças significativas que afetariam diretamente a operação da empresa. No entanto, o ambiente geopolítico instável e as incertezas econômicas continuam a ser fatores importantes a monitorar para Goldman Sachs e outros players no mercado financeiro global.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória complexa e marcada por altos e baixos. Com base nos dados fornecidos, é possível traçar um panorama que inclui tanto períodos de crescimento robusto quanto outros caracterizados por desafios significativos.

###### Tabela Anual

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 47.37B | — | — | — | R$ 11.26B | 23.8% | R$ 4.96B |
| 2023 | R$ 46.25B | — | — | — | R$ 8.52B | 18.4% | R$ -14.90B |
| 2024 | R$ 53.51B | — | — | — | R$ 14.28B | 26.7% | R$ -15.30B |
| 2025 | R$ 58.28B | — | — | — | R$ 17.18B | 29.5% | R$ -47.22B |

###### Análise da Trajetória Financeira

A receita bruta da empresa apresentou um crescimento composto anual (CAGR) de aproximadamente 3,6% entre 2022 e 2025, com picos notáveis em 2024 e 2025. No entanto, a margem EBITDA não foi fornecida nos dados disponíveis, o que dificulta uma análise mais detalhada sobre os custos operacionais.

O lucro líquido da empresa oscilou significativamente ao longo do período analisado. Em 2022, a companhia registrou um lucro líquido de R$11,26 bilhões, com uma margem líquida de 23,8%. No ano seguinte, essa margem caiu para 18,4%, com o lucro líquido diminuindo para R$8,52 bilhões. Em 2024 e 2025, a empresa voltou a apresentar um crescimento no lucro líquido, alcançando respectivamente R$14,28 bilhões e R$17,18 bilhões.

No entanto, uma das principais preocupações reside na evolução do fluxo de caixa livre (FCF). Enquanto em 2022 a empresa registrou um FCF positivo de R$4,96 bilhões, nos anos seguintes esse indicador sofreu uma queda significativa. Em 2023 e 2024, o FCF foi negativo em R$14,90 bilhões e R$15,30 bilhões respectivamente, culminando em um déficit de R$47,22 bilhões no ano de 2025. Essa tendência negativa do FCF pode ser indicativa de desafios significativos na gestão de capital operacional e investimentos.

###### Dividendos

A empresa tem mantido uma política consistente de pagamento de dividendos ao longo dos anos, com um crescimento contínuo no valor total proventos por ação. A tabela abaixo ilustra essa evolução:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 3.750 |
| 2021 | 6.500 |
| 2022 | 9.000 |
| 2023 | 10.500 |
| 2024 | 11.500 |
| 2025 | 14.000 |
| 2026 | 4.500 |

A distribuição de dividendos tem sido um ponto importante para os acionistas, com a empresa apresentando uma Dividend Growth Rate (DGR) de 30,1% ao ano, calculada sem considerar eventuais dividendos extraordinários. Essa taxa de crescimento robusta sugere que a empresa mantém uma política consistente e atrativa em termos de retorno aos acionistas.

###### Lucro Contábil vs FCF

É importante notar que enquanto o lucro contábil pode ser influenciado por ajustes e provisões, o fluxo de caixa livre (FCF) oferece uma visão mais clara da geração de valor operacional. A queda acentuada do FCF em 2023 e 2024, seguida pelo déficit significativo em 2025, indica que os ajustes contábeis podem estar mascarando desafios financeiros reais.

##### Ato 4 — O Balanço

O balanço da empresa no ano de 2026 revela uma série de indicadores importantes para avaliar o seu desempenho e sustentabilidade financeira. 

###### Indicadores Financeiros Principais
- **P/E (Price to Earnings Ratio)**: 16,86
- **P/B (Price to Book Ratio)**: 2,57
- **DY (Dividend Yield)**: 1,68%
- **ROE (Return on Equity)**: 14,59%

###### Análise do Balanço

###### Estrutura de Capital e Alavancagem Financeira
A empresa apresenta uma estrutura de capital com um nível significativo de endividamento. O Net Debt estimado é de R$193,07 bilhões (estimativa: total_debt × 0,5 — caixa não disponível directamente), resultando em uma relação Net Debt/EBITDA de aproximadamente 4,2 vezes com base no EBITDA mais recente da tabela. Este nível de alavancagem é considerado alto e pode comprometer a capacidade da empresa de gerenciar despesas financeiras crescentes.

###### Liquidez
O Current Ratio (relação entre ativos circulantes e passivos circulantes) não foi fornecido diretamente, mas com base nos dados disponíveis, é possível inferir que a empresa enfrenta um risco líquido moderado devido ao nível elevado de endividamento.

###### Retorno sobre o Capital Próprio (ROE)
O ROE da empresa está em 14,59%, superando o custo do capital próprio (Ke) estimado para a companhia no Brasil, que é de aproximadamente 18,25% (Selic 13,75% + prémio de risco equity de 4,5%). Embora o ROE seja inferior ao Ke, ainda indica que a empresa está criando valor acima do custo do capital próprio.

###### Pontos de Atualização
Um ponto de atenção importante é a tendência crescente da despesa financeira e alavancagem. A empresa deve monitorar cuidadosamente esses indicadores para evitar um aumento excessivo na carga de dívida, o que poderia comprometer sua capacidade de gerir futuros ciclos econômicos adversos.

Em resumo, a análise do balanço da empresa em 2026 sugere uma posição financeira complexa, com indicadores mistos que refletem tanto oportunidades quanto desafios significativos.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa em questão revela uma série de indicadores que permitem avaliar sua posição relativa no mercado e compará-la com pares setoriais e índices gerais. Para o cálculo do múltiplo PER (Preço/Ebitda), a empresa apresenta um valor de 16,86x, ligeiramente superior à média setorial de 14,81x, mas inferior ao índice S&P 500 que registra uma média de 21,00x. Este múltiplo sugere que a empresa está avaliada um pouco acima da média do seu setor, embora ainda esteja dentro dos parâmetros considerados normais.

O múltiplo P/B (Preço/Patrimônio Líquido) é de 2,57x para a empresa em questão, ligeiramente superior à mediana setorial de 2,21x e significativamente abaixo do índice Ibov que apresenta uma média de 3,50x. Este indicador sugere um nível de valorização moderado da empresa comparada aos seus pares, mas ainda dentro dos limites aceitáveis.

O Dividend Yield (DY) reportado pela empresa é de 1,68%, ligeiramente inferior à média setorial que se situa em 2,0% e também abaixo do índice S&P 500 com uma média de 1,5%. É importante notar que o DY pode ser influenciado por fatores extraordinários ou temporários. No entanto, a empresa tem um histórico consistente de pagamentos de dividendos ao longo dos últimos 28 trimestres consecutivos, indicando uma política de dividendos sólida e estruturalmente sustentável.

O retorno sobre o patrimônio líquido (ROE) da empresa é de 14,59%, ligeiramente inferior à médiana setorial que se situa em 16,5% e também abaixo do índice S&P 500 com uma média de 16,0%. Este indicador sugere que a empresa está gerando um retorno sobre o patrimônio líquido ligeiramente inferior à média setorial, embora ainda dentro dos limites aceitáveis.

Por fim, o fluxo de caixa livre (FCF) da empresa no último ano foi negativo em R$ 47,22 bilhões. Este valor é significativamente inferior ao yield médio do setor que se situa em 3,3% e também abaixo do índice S&P 500 com uma média de 4,0%. Este indicador sugere que a empresa está enfrentando desafios na geração de caixa livre no momento.

A tabela abaixo resume os múltiplos analisados para a empresa em questão, comparados aos seus pares setoriais e ao índice S&P 500:

| Múltiplo | GS | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 16.86x | 14.81x | 21.00x |
| P/B | 2.57x | 2.21x | 3.50x |
| DY | 1.68% | 2.0% | 1.5% |
| FCF Yield | -17.1% | 3.3% | 4.0% |
| ROE | 14.59% | 16.5% | 16.0% |
| ND/EBITDA | — | 0.48x | — |

##### Ato 6 — Os Quality Scores

A análise dos indicadores de qualidade financeira da empresa revela uma série de métricas que permitem avaliar a solidez e a sustentabilidade do seu desempenho operacional e financeiro.

O índice de qualidade financeira de Piotroski, embora não seja fornecido neste relatório, é um indicador importante para medir a saúde financeira da empresa. Este índice varia entre 0 e 9 pontos e considera uma série de critérios como lucro operacional positivo, crescimento em ativos circulantes líquidos, cobertura de dividendos por lucros, entre outros.

O modelo de risco financeiro de Altman apresenta dois indicadores: o Z-score conservador (Z) e o Z-score ajustado (Z'). No caso da empresa em questão, os valores do Z-score não foram fornecidos. Este índice é um indicador robusto que permite classificar empresas como baixo risco, médio risco ou alto risco de insolvência.

O modelo M-Score de Beneish é outro indicador importante para medir a probabilidade de manipulação contábil. No entanto, o valor do M-score não foi fornecido neste relatório. Este índice varia entre -5 e +5 pontos e permite classificar empresas como limpas (M < -2,2), cinzentas (M > -2,2 e M < -1,78) ou de risco (M > -1,78).

É importante ressaltar que a ausência destes indicadores pode ser interpretada como uma limitação na análise financeira da empresa. Recomenda-se a obtenção dessas métricas para uma avaliação mais completa e precisa do desempenho da empresa.

A falta de dados específicos sobre os scores de qualidade financeira impede uma análise detalhada, mas é fundamental considerar esses indicadores ao avaliar o perfil de risco e sustentabilidade da empresa.

---

##### Ato 7 — O Moat e a Gestão

O moat de Goldman Sachs é classificado como Wide. Este reconhecimento baseia-se em várias dimensões da empresa que lhe conferem uma vantagem competitiva duradoura, incluindo custos de escala significativos, elevados custos de troca para clientes institucionais e um forte portfólio intangível.

A primeira dimensão do moat é a economia de escala. Como um dos maiores bancos de investimento globalmente, Goldman Sachs beneficia de uma infraestrutura tecnológica robusta e eficiente que permite operar com custos relativamente baixos em comparação com seus concorrentes menores. Este fator lhe confere uma vantagem competitiva significativa ao permitir a empresa oferecer serviços financeiros complexos a um preço mais acessível.

A segunda dimensão é o alto custo de troca para clientes institucionais, que são frequentemente vinculados por contratos longos e complexas relações comerciais. A mudança para outro banco pode ser dispendiosa em termos de tempo e recursos, além do potencial impacto negativo na reputação e no desempenho financeiro.

A terceira dimensão é a força intangível da marca Goldman Sachs. Com uma história rica e reconhecida globalmente, a empresa possui um portfólio significativo de ativos intangíveis que incluem marcas fortes, relações com clientes estabelecidas e conhecimento especializado.

Quanto à gestão, o perfil filosófico computado indica que a estratégia da Goldman Sachs é

_… (truncated at 15k chars — full content in cemetery copy of `dossiers\GS_STORY.md`)_

#### — · Other
_source: `hubs\GS.md` (now in cemetery)_

#### GS — Goldman Sachs

> **Hub consolidado**. Tudo o que existe no vault sobre GS, em ordem cronológica. Cada link aponta para o ficheiro original que ficou na sua pasta — esta é a porta de entrada matinal.

`sector: Financials` · `market: US` · `currency: USD`

##### 🎯 Hoje

- **Posição**: 1.0 @ entry 318.83
- **Verdict (DB)**: `HOLD` (score 5.92, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 17.44 · P/B 2.68 · DY 2.1% · ROE 14.5% · Dividend streak 28 · Aristocrat yes

##### 📜 Histórico (chronological journal)

> Como a vista sobre este nome evoluiu — do primeiro screen ao deepdive mais recente. Útil para perceber **o que sabíamos antes vs o que sabemos agora**.


###### 2026

- **2026-05-13** · Overnight → [[GS]] _(`Overnight_2026-05-13/GS.md`)_
- **2026-05-12** · Filing → [[GS_FILING_2026-05-12]] _(`dossiers/GS_FILING_2026-05-12.md`)_
- **2026-05-11** · Overnight → [[GS]] _(`Overnight_2026-05-11/GS.md`)_
- **2026-05-01** · Dossier Archive → [[GS_STORY_2026-05-01]] _(`dossiers/archive/GS_STORY_2026-05-01.md`)_
- **2026-05-01** · Review · Valentina Prudente → [[GS_2026-05-01]] _(`agents/Valentina Prudente/reviews/GS_2026-05-01.md`)_
- **2026-05-01** · Review · Pedro Alocação → [[GS_2026-05-01]] _(`agents/Pedro Alocação/reviews/GS_2026-05-01.md`)_
- **2026-05-01** · Review · Mariana Macro → [[GS_2026-05-01]] _(`agents/Mariana Macro/reviews/GS_2026-05-01.md`)_
- **2026-05-01** · Review · Hank Tier-One → [[GS_2026-05-01]] _(`agents/Hank Tier-One/reviews/GS_2026-05-01.md`)_

###### (undated)

- **—** · Wiki → [[GS]] _(`wiki/holdings/GS.md`)_
- **—** · Variant → [[GS_VARIANT]] _(`tickers/GS_VARIANT.md`)_
- **—** · Story → [[GS_STORY]] _(`dossiers/GS_STORY.md`)_
- **—** · Panorama → [[GS]] _(`tickers/GS.md`)_
- **—** · Other → [[GS]] _(`hubs/GS.md`)_
- **—** · Ic Debate → [[GS_IC_DEBATE]] _(`tickers/GS_IC_DEBATE.md`)_
- **—** · Drip → [[GS_drip]] _(`briefings/drip_scenarios/GS_drip.md`)_
- **—** · Deepdive → [[GS_DOSSIE]] _(`tickers/GS_DOSSIE.md`)_
- **—** · Council → [[GS_COUNCIL]] _(`dossiers/GS_COUNCIL.md`)_

##### 🗂️ Artefactos por categoria

###### Panorama
- [[GS]] _(`tickers/GS.md`)_

###### Deepdive (DOSSIE)
- [[GS_DOSSIE]] _(`tickers/GS_DOSSIE.md`)_

###### Story
- [[GS_STORY]] _(`dossiers/GS_STORY.md`)_

###### Council aggregate
- [[GS_COUNCIL]] _(`dossiers/GS_COUNCIL.md`)_

###### Council reviews por persona

_Hank Tier-One_:
- [[GS_2026-05-01]] _(`agents/Hank Tier-One/reviews/GS_2026-05-01.md`)_

_Mariana Macro_:
- [[GS_2026-05-01]] _(`agents/Mariana Macro/reviews/GS_2026-05-01.md`)_

_Pedro Alocação_:
- [[GS_2026-05-01]] _(`agents/Pedro Alocação/reviews/GS_2026-05-01.md`)_

_Valentina Prudente_:
- [[GS_2026-05-01]] _(`agents/Valentina Prudente/reviews/GS_2026-05-01.md`)_

###### IC Debate (synthetic)
- [[GS_IC_DEBATE]] _(`tickers/GS_IC_DEBATE.md`)_

###### Variant perception
- [[GS_VARIANT]] _(`tickers/GS_VARIANT.md`)_

###### Filings individuais
- [[GS_FILING_2026-05-12]] _(`dossiers/GS_FILING_2026-05-12.md`)_

###### Overnight scrapes
- [[GS]] _(`Overnight_2026-05-13/GS.md`)_
- [[GS]] _(`Overnight_2026-05-11/GS.md`)_

###### DRIP scenarios
- [[GS_drip]] _(`briefings/drip_scenarios/GS_drip.md`)_

###### Wiki / playbooks
- [[GS]] _(`wiki/holdings/GS.md`)_

###### Archived stories
- [[GS_STORY_2026-05-01]] _(`dossiers/archive/GS_STORY_2026-05-01.md`)_

###### Other
- [[GS]] _(`hubs/GS.md`)_

##### ⚙️ Refresh commands

```bash
ii panorama GS --write       # aggregator (verdict+peers+notes+videos)
ii deepdive GS --save-obsidian # V10 4-layer pipeline
ii verdict GS --narrate --write
ii fv GS                      # fair value (Buffett-Graham conservative)
python -m analytics.fair_value_forward --ticker GS # quality-aware forward
```

---

_Regenerado por `scripts/build_ticker_hubs.py`. Run novamente para refresh._

#### — · Panorama
_source: `tickers\GS.md` (now in cemetery)_

#### GS — Goldman Sachs

#holding #us #financials

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 5.9/10  |  **Confiança**: 60%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 6.7/10 | 35% | `███████░░░` |
| Valuation  | 4.0/10 | 30% | `████░░░░░░` |
| Momentum   | 6.7/10 | 20% | `███████░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski None/9 (N/A), DivSafety 93.8/100
- **Valuation**: Screen 0.60, DY percentil P19 (EXPENSIVE)
- **Momentum**: 1d 2.01%, 30d 3.72%, YTD 2.52%
- **Narrativa**: user_note=False, YT insights 60d=4

###### Razões

- total 5.9 na zona neutra

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[JPM]] · [[NU]] · [[TFC]]
- Vídeos: [[videos/2026-04-14_virtual-asset_klabin-mudou-o-plano-nova-ordem-de-dividendos-e-lucros-klbn11-ou-klbn4|KLABIN MUDOU O PLANO? NOVA ORDEM DE DIVI]] · [[videos/2026-04-14_o-primo-rico_por-que-o-dolar-esta-caindo-tanto-vai-cair-ainda-mais|POR QUE O DÓLAR ESTÁ CAINDO TANTO? (vai ]] · [[videos/2025-08-01_suno-noticias_banco-do-brasil-bbas3-vai-decepcionar-projecoes-para-grandes-bancos|BANCO DO BRASIL (BBAS3) vai DECEPCIONAR?]]
- 🎯 **Thesis**: [[wiki/holdings/GS|thesis deep]]

##### Snapshot

- **Preço**: $937.35  (2026-05-06)    _+2.01% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 93.8/100 (SAFE)
- **Posição**: 1.0 sh @ $318.83  →  P&L 194.0%

##### Fundamentals

- P/E: 17.114296 | P/B: 2.6054435 | DY: 1.65%
- ROE: 14.55% | EPS: 54.77 | BVPS: 359.766
- Streak div: 28y | Aristocrat: True

##### Dividendos recentes

- 2026-06-01: $4.5000
- 2026-03-02: $4.5000
- 2025-12-02: $4.0000
- 2025-08-29: $4.0000
- 2025-05-30: $3.0000

##### Eventos (SEC/CVM)

- **2026-05-01** `8-K` — 8-K | 5.07
- **2026-05-01** `10-Q` — 10-Q
- **2026-04-20** `8-K` — 8-K | 9.01
- **2026-04-13** `8-K` — 8-K | 2.02,7.01,9.01
- **2026-03-20** `proxy` — DEF 14A

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O Goldman Sachs está atuando como um grande vendedor no mercado, sugerindo uma posição bearish. |
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O Goldman Sachs está utilizando robôs de negociação para vender ações. |
| 2026-05-11 | Genial Investimentos | operational | 0.70 | O Goldman Sachs está parando de vender e começando a comprar, indicando uma possível mudança na estratégia. |
| 2026-04-14 | Virtual Asset | valuation | 0.90 | Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00. |
| 2026-04-14 | O Primo Rico | guidance | 0.60 | O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -3.95%
- **Drawdown 5y**: -3.95%
- **YTD**: +2.52%
- **YoY (1y)**: +70.63%
- **CAGR 3y**: +42.05%  |  **5y**: +20.37%  |  **10y**: +19.42%
- **Vol annual**: +31.68%
- **Sharpe 3y** (rf=4%): +1.37

###### Dividendos
- **DY 5y avg**: +2.13%
- **Div CAGR 5y**: +21.14%
- **Frequency**: quarterly
- **Streak** (sem cortes): 15 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $47.37B | $11.26B | $4.96B |
| 2023-12-31 | $46.25B | $8.52B | $-14.90B |
| 2024-12-31 | $53.51B | $14.28B | $-15.30B |
| 2025-12-31 | $58.28B | $17.18B | $-47.22B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "GS — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: GS
    data: [565.7, 611.6, 606.52, 615.73, 598.72, 614.0, 625.11, 635.24, 669.87, 706.46, 697.28, 713.3, 708.26, 719.18, 730.75, 720.91, 719.24, 730.72, 715.95, 749.67, 730.56, 763.92, 786.76, 805.0, 794.76, 785.51, 789.65, 786.78, 750.77, 750.78, 783.06, 790.83, 797.2, 790.91, 773.7, 816.01, 836.57, 876.58, 889.59, 893.48, 907.04, 914.34, 934.83, 932.67, 953.01, 929.72, 946.33, 928.75, 904.55, 916.65, 921.38, 862.58, 832.03, 782.21, 809.5, 841.84, 845.99, 864.15, 890.79, 925.95, 931.3, 926.55, 903.27]
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
    data: [16.426132, 16.513508, 16.447369, 16.9216, 17.079678, 16.932566, 16.926771, 16.920591, 16.920591, 17.11957, 16.917107, 16.537619, 16.860193, 16.489048, 16.786446, 17.114296]
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
    data: [13.86, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.59, 14.55, 14.55, 14.55]
  - title: DY %
    data: [1.98, 2.0, 2.0, 1.94, 1.94, 1.67, 1.67, 1.67, 1.67, 1.65, 1.67, 1.71, 1.68, 1.72, 1.69, 1.65]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\GS_DOSSIE.md` (now in cemetery)_

#### 📑 GS — Goldman Sachs

> Generated **2026-04-26** by `ii dossier GS`. Cross-links: [[GS]] · [[GS_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

GS negoceia a P/E 16.92 com DY 1.67% e ROE 14.59%, IC HOLD com alta confiança (80% consenso). Achado-chave: 28 anos de dividendos consecutivos e franchise IB/Trading top-tier — YoY +70.1% reflecte recovery dealmaking + IPO window reabrindo. ROE 14.59% ligeiramente abaixo do screen US ≥15%; manter para compounding mas vigiar deterioração.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 54.78  |  **BVPS**: 359.77
- **ROE**: 14.59%  |  **P/E**: 16.92  |  **P/B**: 2.58
- **DY**: 1.67%  |  **Streak div**: 28y  |  **Market cap**: USD 275.06B
- **Last price**: USD 926.91 (2026-04-26)  |  **YoY**: +70.1%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[GS_IC_DEBATE]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 16.92** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 16.92** passa.
- **P/B = 2.58** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **2.58** OK.
- **DY = 1.67%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **1.67%** fraco; verificar se é growth pick.
- **ROE = 14.59%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **14.59%** abaixo do critério.
- **Graham Number ≈ R$ 665.91** vs preço **R$ 926.91** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 28y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 3. Riscos identificados

- 🟡 **Sensibilidade a ciclo capital markets** — IB/M&A volátil; recessão fecha pipeline. Trigger: IB revenue YoY < -15%.
- 🟡 **Trading volatility (FICC + Equities)** — receita imprevisível; tail risk em quiet markets. Trigger: trading revenue stddev > 25% over 4 quarters.
- 🟡 **Regulatory cap (Basel III endgame)** — capital requirements pressão sobre buybacks. Trigger: `events` table novo regulatory action.
- 🟢 **Consumer pivot wind-down (Marcus/Apple Card)** — execução decente mas ainda overhang.

##### 4. Position sizing

**Status atual**: holding (in portfolio)

**Manter para compounding** — sleeve growth/financials, não pure DRIP. Após +70% YoY não acelerar reforços; aguardar consolidação ou pullback. USD em conta US.

##### 5. Tracking triggers (auto-monitoring)

- **ROE quebra** — `fundamentals.roe < 0.12` por 2 trimestres → degradação severa.
- **PE expansion** — `fundamentals.pe > 20` → premium banco difícil de sustentar.
- **IB revenue collapse** — IB revenue YoY < -20% por 2 quarters → ciclo capital markets em rollover.
- **Earnings miss** — `events.kind='earnings'` surprise < -10% → reavaliar.
- **Conviction drop** — `conviction_scores.composite_score < 60` → reduce.

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
*Generated by `ii dossier GS` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O Goldman Sachs está atuando como um grande vendedor no mercado, sugerindo uma posição bearish. |
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O Goldman Sachs está utilizando robôs de negociação para vender ações. |
| 2026-05-11 | Genial Investimentos | operational | 0.70 | O Goldman Sachs está parando de vender e começando a comprar, indicando uma possível mudança na estratégia. |
| 2026-04-14 | Virtual Asset | valuation | 0.90 | Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00. |
| 2026-04-14 | O Primo Rico | guidance | 0.60 | O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável. |

#### — · IC Debate (synthetic)
_source: `tickers\GS_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — GS

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 5.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- ROE abaixo de 15%
- Complexidade do negócio
- Leverage cíclica

**Key risk**: Ciclos econômicos afetam fortemente o desempenho da empresa

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável
- ROE sólido
- Notícias positivas recentes

**Key risk**: Volatilidade do mercado financeiro pode afetar significativamente o desempenho da Goldman Sachs

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável
- Dividendos atraentes
- Exposição a fintech

**Key risk**: Volatilidade do mercado financeiro pode afetar significativamente o desempenho da empresa

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Preço não oferece desconto significativo
- Indicadores fundamentais são razoáveis, mas não atraentes
- Ausência de oportunidades especiais ou situações complexas

**Key risk**: Risco de perda permanente de capital por sobrevalorização

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável
- Dívida/GDP estável
- Inflação transitoria na Asia

**Key risk**: Bubbles e ciclo de dívidas globais podem afetar Goldman Sachs

##### 📊 Context provided

```
TICKER: US:GS

FUNDAMENTALS LATEST:
  pe: 17.114035
  pb: 2.6030252
  dy: 2.14%
  roe: 14.55%
  intangible_pct_assets: 0.4%   (goodwill $5.9B + intangibles $0.8B)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

RECENT MATERIAL NEWS (last 14d via Tavily):
  - We're trimming a big winner and buying the dip in a stock that shouldn't be down - CNBC [Wed, 06 Ma]
    # We're trimming a big winner and buying the dip in a stock that shouldn't be down. We are making two trades Wednesday: Selling 15 shares of Goldman Sachs at roughly $938 each, which leaves Jim Cramer
  - Goldman Sachs leads Kashable's $60m funding round - Finextra Research [Tue, 28 Ap]
    # Goldman Sachs leads Kashable's $60m funding round. Image 2: Download Finextra Pro. *   Image 3: Download Finextra Pro. 4.   Goldman Sachs leads Kashable's $60m funding round. Image 5: NextGen FinCri
  - Import price inflation in Asia is likely to be transitory this time: GS economist - CNBC [Mon, 04 Ma]
    # Import price inflation in Asia is likely to be transitory this time: GS economist. Goldman Sachs Goohoon Kwon says Asia’s import price shock should be far milder than in 2021–22, with pressures larg
  - Goldman Sachs Alternatives Announces Strategic Investment in Kashable, Leading the Company’s Series C Equity Round - Fin [Mon, 27 Ap]
    # Goldman Sachs Alternatives Announces Strategic Investment in Kashable, Leading the Company’s Series C Equity Round. NEW YORK, April 27, 2026 (GLOBE NEWSWIRE) -- Kashable, a mission-driven fintech pl
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O Goldman Sachs está atuando como um grande vendedor no mercado, sugerindo uma posição bearish. |
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O Goldman Sachs está utilizando robôs de negociação para vender ações. |
| 2026-05-11 | Genial Investimentos | operational | 0.70 | O Goldman Sachs está parando de vender e começando a comprar, indicando uma possível mudança na estratégia. |
| 2026-04-14 | Virtual Asset | valuation | 0.90 | Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00. |
| 2026-04-14 | O Primo Rico | guidance | 0.60 | O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável. |

#### — · Variant perception
_source: `tickers\GS_VARIANT.md` (now in cemetery)_

#### 🎯 Variant Perception — GS

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `unmeasurable` (magnitude 0/5)  
**Interpretation**: missing thesis or no analyst data

##### 📜 Our thesis

**Core thesis (2026-04-25)**: Goldman Sachs é um líder global em serviços financeiros com solidez histórica de dividendos e uma forte posição no mercado. Apesar do ROE estar ligeiramente abaixo da barreira estabelecida (14.59% vs. 15%), a empresa mantém um P/E razoável (16.93), um sólido P/B (2.58) e uma longa história de pagamentos de dividendos (28 anos consecutivos).

**Key assumptions**:
1. O setor financeiro continuará a oferecer oportunidades lucrativas para Goldman Sachs nos próximos anos.
2. A empresa manterá sua capacidade de gerir dívida e capital com eficiência, mantendo o ROE acima do mínimo da estratégia.
3. As condições econômicas globais não deteriorarão drasticamente, impactando negativamente os resultados financeiros da Goldman Sachs.
4. O histórico de pagamentos de divide

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.90 | O Goldman Sachs está atuando como um grande vendedor no mercado, sugerindo uma posição bearish. |
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O Goldman Sachs está utilizando robôs de negociação para vender ações. |
| 2026-05-11 | Genial Investimentos | operational | 0.70 | O Goldman Sachs está parando de vender e começando a comprar, indicando uma possível mudança na estratégia. |
| 2026-04-14 | Virtual Asset | valuation | 0.90 | Goldman Sachs tem uma recomendação neutra para as ações da Klabin, com preço-alvo de R$ 18,00. |
| 2026-04-14 | O Primo Rico | guidance | 0.60 | O Goldman Sachs previu que o dólar continuaria enfraquecendo em 2026, mas a previsão pode não ser confiável. |

#### — · Wiki playbook
_source: `wiki\holdings\GS.md` (now in cemetery)_

> ⚠️ **AUTO-DRAFT** (2026-04-25) — gerado por `holding_wiki_synthesizer.py` via
> Ollama Qwen 14B local. Refinar com tese pessoal + memória de contexto que o
> LLM não tem acesso (entry rationale, lições passadas, sizing decisions).
> Após review humana, remover `auto_draft: true` e este aviso.

#### 🎯 Thesis: [[GS]] — Goldman Sachs

> Goldman Sachs como DRIP core, compounding growth e tactical hold — por sua consistência e dividendos sustentáveis.

##### Intent
**Tactical** — Goldman Sachs como DRIP core, compounding growth e tactical hold — por sua consistência e dividendos sustentáveis.

##### Business snapshot
Goldman Sachs é uma instituição financeira líder global com forte presença nos EUA. Seu negócio se baseia principalmente em serviços de investimento e banca comercial, gerando receita diversificada a longo prazo.

**Fundamentals**: P/E 16.9 · P/B 2.6 · DY 1.7% · ROE 14.6% · Streak 28y

##### Por que detemos

1. Satisfação dos critérios de qualidade sobre preço da filosofia value investing, com exceção do DY (1.67% < 2.5%)
2. Dividend Aristocrat e histórico de pagamentos de dividendos por 28 anos consecutivos.
3. ROE acima de 14%, indicando eficiência operacional.
4. P/B de apenas 2.58, sugerindo valor potencial.

##### Moat

Goldman Sachs mantém uma vantagem competitiva através de sua rede global de clientes, marca reconhecida e capacidade de inovação em serviços financeiros.

##### Current state (2026-04)

Em 2026, Goldman Sachs continua a ser um líder no setor financeiro com métricas sólidas: P/E de 16.93, ROE de 14.59%, e uma relação P/B de 2.58.

##### Invalidation triggers

- [ ] DY cair abaixo de 1% ou não aumentar durante ações de dividendos futuras
- [ ] ROE cair significativamente para menos que 10%
- [ ] P/E subir acima de 30, indicando sobreavaliação.
- [ ] Aumento significativo da dívida líquida (long_term_debt) sem crescimento correspondente.

##### Sizing + DRIP

Tamanho atual é adequado para DRIP e acumulação adicional quando condições favoráveis surgirem, mantendo a posição como um core holding.
- Posição actual: 1.0 shares @ 318.83 entry (2023-07-11)

---
*AUTO-DRAFT por `holding_wiki_synthesizer.py` · Ollama Qwen 14B local · 2026-04-25*

## ⚙️ Refresh commands

```bash
ii panorama GS --write
ii deepdive GS --save-obsidian
ii verdict GS --narrate --write
ii fv GS
python -m analytics.fair_value_forward --ticker GS
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
