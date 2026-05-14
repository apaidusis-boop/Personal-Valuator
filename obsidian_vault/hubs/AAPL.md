---
type: ticker_hub
ticker: AAPL
market: us
sector: Technology
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 13
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# AAPL — Apple

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Technology` · `market: US` · `currency: USD` · `bucket: holdings` · `13 sources merged`

## 🎯 Hoje

- **Posição**: 5.0 @ entry 121.89000000000001
- **Verdict (DB)**: `HOLD` (score 6.62, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 36.23 · P/B 41.17 · DY 0.4% · ROE 141.5% · ND/EBITDA 0.10 · Dividend streak 15 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\AAPL.md` (cemetery archive)_

#### AAPL — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.apple.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=5.0 · entry=121.89000000000001 · date=2020-11-16

- Total events na DB: **160**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=292.67999267578125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=1.4147099 · DY=0.004441711194929836 · P/E=35.390564
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-30 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-20 | 8-K | sec | 8-K \| 5.02 |
| 2026-02-24 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-01-30 | 10-Q | sec | 10-Q |

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

#### 2026-04-30 · Council review · Charlie Compounder
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Charlie Compounder\reviews\AAPL_2026-04-30.md` (cemetery archive)_

#### Charlie Compounder sobre [[AAPL_STORY|AAPL]]

**Função no debate**: Industrials & Consumer US Specialist (Buffett frame) (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: ⚪ **NEEDS_DATA** *(R1 era HOLD)*  

##### Round 1 — Abertura (cega aos colegas)

> _Apple mantém forte ROE e crescimento, mas múltiplos elevados são preocupantes_

A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos. No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados.

**Métricas que invoquei**:
- ROE = 152%
- Dividend Yield = 0,4%
- P/E = 34,39

**Preocupações**:
- Múltiplos de valuation muito altos
- Baixo dividend yield isolado

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Apple continua gerando lucros consistentes com um ROE de 152% e uma relação P/B de 45,24x - Valentina Prudente

**Desafiei**:
- A relação P/E está acima da média setorial, mas reflete a solidez operacional - Mariana Macro | Discordo pois o múltiplo elevado não é justificado pelo crescimento atual e pode indicar sobreavaliação

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[AAPL_STORY|📖 Storytelling completo (8 actos)]]
- [[AAPL_COUNCIL|🏛️ Transcript do Council debate]]
- [[Charlie Compounder|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\AAPL_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[AAPL_STORY|AAPL]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Apple mantém posição de liderança com forte geração de lucros_

A Apple continua gerando ROE excepcionalmente alto (152%) e tem um histórico consistente de dividendos, apesar do baixo DY. A relação P/E está acima da média setorial, mas reflete a solidez operacional.

**Métricas que invoquei**:
- ROE=152%
- P/E=34.39
- DivStreak=15

**Preocupações**:
- P/B elevado (45.24x)
- Dependência macro crescente

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiei**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem a solidez operacional da empresa e não são necessariamente preocupantes

**Evidência nova**: Apple continua a ver um crescimento significativo em suas divisões de serviços, mantendo o momentum financeiro da empresa

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[AAPL_STORY|📖 Storytelling completo (8 actos)]]
- [[AAPL_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\AAPL_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[AAPL_STORY|AAPL]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Apple mantém posição de destaque com forte geração de lucros_

A Apple continua a gerar ROE superior a 150% e um histórico consistente de dividendos, apesar do P/E elevado de 34.39.

**Métricas que invoquei**:
- ROE=152%
- P/E=34.39
- DivStreak=15

**Preocupações**:
- P/B alto de 45.24
- peso na carteira de 6%

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiei**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem o desempenho operacional excepcional da empresa

**Evidência nova**: A Apple continua a registrar crescimento significativo em suas divisões de serviços e dispositivos, mantendo o momentum financeiro da empresa

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[AAPL_STORY|📖 Storytelling completo (8 actos)]]
- [[AAPL_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\AAPL_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[AAPL_STORY|AAPL]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Apple mantém robusta geração de lucros e ROE elevado_

A Apple continua gerando lucros consistentes com um ROE de 152% e uma relação P/B de 45,24x. A empresa tem histórico de dividendos por 15 anos.

**Métricas que invoquei**:
- ROE=152%
- P/B=45,24
- DivStreak=15

**Preocupações**:
- P/E elevado de 34,39x
- alta dependência do mercado chinês

##### Round 2 — Resposta aos colegas

**Concordei com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiei**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem o desempenho operacional excepcional da empresa e não necessariamente sugerem um risco permanente de capital

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[AAPL_STORY|📖 Storytelling completo (8 actos)]]
- [[AAPL_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AAPL_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[AAPL_STORY|AAPL]] (Apple)

**Final stance**: ⚪ **NEEDS_DATA**  
**Confidence**: `low`  
**Modo (auto)**: A (US)  |  **Sector**: Technology  |  **Held**: sim  
**Elapsed**: 60.3s  |  **Failures**: 0

##### Quem esteve na sala

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos
- Metrics: ROE=152%
- Nomes: Charlie Compounder, Mariana Macro, Valentina Prudente, Pedro Alocação

**Dissenso (preservado)**:
- Charlie Compounder disse que a relação P/E está acima da média setorial e indica sobreavaliação; Mariana Macro e outros disseram que esses múltiplos refletem o desempenho operacional excepcional da empresa e não são necessariamente preocupantes

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ Dados de crescimento futuro ausentes
- ⚠️ Valentina Prudente

**Sizing**: Considerar reduzir a posição para até 5% da carteira, dado o peso atual de 6%

##### Round 1 — Opening Statements (blind)

###### [[Charlie Compounder]] — 🟡 **HOLD**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _Apple mantém forte ROE e crescimento, mas múltiplos elevados são preocupantes_

A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos. No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados.

**Métricas**:
- ROE = 152%
- Dividend Yield = 0,4%
- P/E = 34,39

**Preocupações**:
- Múltiplos de valuation muito altos
- Baixo dividend yield isolado

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _Apple mantém posição de liderança com forte geração de lucros_

A Apple continua gerando ROE excepcionalmente alto (152%) e tem um histórico consistente de dividendos, apesar do baixo DY. A relação P/E está acima da média setorial, mas reflete a solidez operacional.

**Métricas**:
- ROE=152%
- P/E=34.39
- DivStreak=15

**Preocupações**:
- P/B elevado (45.24x)
- Dependência macro crescente

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Apple mantém robusta geração de lucros e ROE elevado_

A Apple continua gerando lucros consistentes com um ROE de 152% e uma relação P/B de 45,24x. A empresa tem histórico de dividendos por 15 anos.

**Métricas**:
- ROE=152%
- P/B=45,24
- DivStreak=15

**Preocupações**:
- P/E elevado de 34,39x
- alta dependência do mercado chinês

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Apple mantém posição de destaque com forte geração de lucros_

A Apple continua a gerar ROE superior a 150% e um histórico consistente de dividendos, apesar do P/E elevado de 34.39.

**Métricas**:
- ROE=152%
- P/E=34.39
- DivStreak=15

**Preocupações**:
- P/B alto de 45.24
- peso na carteira de 6%

##### Round 2 — Respostas (peers visíveis)

###### [[Charlie Compounder]] — ⚪ **NEEDS_DATA** *(stance flipped)*
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- A Apple continua gerando lucros consistentes com um ROE de 152% e uma relação P/B de 45,24x - Valentina Prudente

**Desafiou**:
- A relação P/E está acima da média setorial, mas reflete a solidez operacional - Mariana Macro | Discordo pois o múltiplo elevado não é justificado pelo crescimento atual e pode indicar sobreavaliação

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiou**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem a solidez operacional da empresa e não são necessariamente preocupantes

**Evidência nova**: Apple continua a ver um crescimento significativo em suas divisões de serviços, mantendo o momentum financeiro da empresa

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiou**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem o desempenho operacional excepcional da empresa e não necessariamente sugerem um risco permanente de capital

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- A Apple apresenta um sólido retorno sobre o patrimônio líquido de 152% e uma história consistente de dividendos — Charlie Compounder

**Desafiou**:
- No entanto, a relação P/E de 34,39 e P/B de 45,24 indicam que os múltiplos estão elevados — Charlie Compounder | Esses múltiplos refletem o desempenho operacional excepcional da empresa

**Evidência nova**: A Apple continua a registrar crescimento significativo em suas divisões de serviços e dispositivos, mantendo o momentum financeiro da empresa

##### Documentos relacionados

- [[AAPL_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[AAPL_2026-04-30|Charlie Compounder]] em [[Charlie Compounder]]/reviews/
  - [[AAPL_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[AAPL_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[AAPL_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:AAPL — Apple ===
Sector: Technology  |  Modo (auto): A  |  Held: True
Last price: 271.3500061035156 (2026-04-30)
Position: 5 shares @ entry 121.89000000000001
Fundamentals: P/E=34.39 | P/B=45.24 | DY=0.4% | ROE=152.0% | ND/EBITDA=0.15 | DivStreak=15.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: Apple é uma excelente posição long-term para um investidor Buffett/Graham devido à sua robusta geração de lucros e retorno sobre o patrimônio líquido (ROE) de 152,02%. A empresa mantém um histórico consistente de dividendos por 15 anos consecutivos, apesar do rendimento anual de dividendos baixo de apenas 0,39%. Com uma relação P/E de 33,74 e uma relação P/B de 44,38, a empresa ainda oferece um potencial significativo para valorização acionária.

**Key assumptions**:
1. A Apple continuará a gerar lucros consistentes com ROE superior a 150%.
2. O crescimento contínuo em suas divisões de serviços e dispositivos mantém o momentum financeiro da empresa.
3. A relação P/E permanecerá estável ou cairá, refletindo um múltiplo mais justo para o desempenho operacional.

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 6.0%
  Sector weight: 19.3%

QUALITY SCORES:
  Piotroski F-Score: 8/9 (2025-09-30)
  Altman Z-Score: 10.70  zone=safe  conf=high
  Beneish M-Score: -2.37  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Apple Stock Rose on New Security Shield that Destroys the FBI’s Hidden Peephole into Private Messages - TipRanks [Thu, 23 Ap]
    # Apple Stock Rose on New Security Shield that Destroys the FBI’s Hidden Peephole into Private Messages. * Apple stock rose 2.6% on Wednesday as the firm successfully shut down a secret way for the FBI to spy on private messages. * The late
  - Stock market today: Dow, S&P 500, and Nasdaq turn negative amid Warsh hearing, Apple CEO change, Iran uncertainty - Yahoo Finance [Tue, 21 Ap]
    # Stock market today: Dow, S&P 500, and Nasdaq turn negative amid Warsh hearing, Apple CEO change, Iran uncertainty. US stocks turned negative on Tuesday as investors assessed Fed chair appointee Kevin Warsh’s confirmation hearing and weigh
  - NZME Investors Back Board-Endorsed Directors, Reject Self-Nominated Candidate - TipRanks [Wed, 22 Ap]
    * Investors overwhelmingly rejected self-nominated director candidate Benedict Ong, affirming confidence in NZME’s current board direction. * Looking for the best stocks to buy? * Discover top-performing stock ideas and upgrade to a portfol
  - Geospace announces 20% reduction in global workforce - TipRanks [Mon, 06 Ap]
    **See today’s best-performing stocks on TipRanks >>**. ### UnitedHealth (UNH) or Humana (HUM): Which Stock Is the Better Buy After CMS’ Surprise Rate Hike. HUMUNH](/news/unitedhealth-unh-or-humana-hum-which-stock-is-the-better-buy-after-cms
  - NVDA vs. AVGO: Why Investors Liked Broadcom’s Earnings More Than Nvidia’s - TipRanks [Fri, 06 Ma]
    DIAQQQ](/news/stock-market-today-review-spy-qqq-lose-steam-on-labor-market-woes-as-trump-calls-for-irans-unconditional-surrender "DIA | QQQ | SPY"). Top Gainers/losers/active ETFs. Best High Yield Dividend Stocks. Five-star-rated analyst Co
  - Apple’s (AAPL) iPhone Sales Continue to Surge Worldwide - TipRanks [Wed, 08 Ap]
    # Apple’s (AAPL) iPhone Sales Continue to Surge Worldwide. – China continues to be a key market for iPhone sales. Data shows that Apple’s (AAPL) newest iPhone 17 continues to sell at a brisk pace. Analysts at Wall Street brokerage Bernstein

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (10 hits)
[1] sec (8-K) [2026-04-30]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/320193/000032019326000011/aapl-20260430.htm
[2] sec (8-K) [2026-04-20]: 8-K | 5.02
     URL: https://www.sec.gov/Archives/edgar/data/320193/000114036126015711/ef20071035_8k.htm
[3] sec (8-K) [2026-02-24]: 8-K | 5.07,9.01
     URL: https://www.sec.gov/Archives/edgar/data/320193/000114036126006577/ef20060722_8k.htm
[4] sec (10-Q) [2026-01-30]: 10-Q
     URL: https://www.sec.gov/Archives/edgar/data/320193/000032019326000006/aapl-20251227.htm
[5] sec (8-K) [2026-01-29]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/320193/000032019326000005/aapl-20260129.htm
[6] sec (proxy) [2026-01-08]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/320193/000130817926000008/aapl014016-def14a.htm

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[7] Bibliotheca: clip_warren_buffetts_investing_rule_that_could_change_your_financ: ional price, a part interest in an easily understandable business whose earnings are virtually certain to be materially higher five, 10, and 20 years from now,” Buffett wrote in the same 1996 letter.1

In practice, that means focusing less on hot trends or complex strategies and more on how a busine
[8] Bibliotheca: clip_warren_buffetts_value_investing_strategy_explained: rnings, revenues, and assets. A company's intrinsic value is usually higher and more complicated than its liquidation value, which is what a company would be worth if it were broken up and sold today.

The liquidation value doesn't include intangibles that aren't directly stated on the financial sta
[9] Bibliotheca: clip_warren_buffetts_value_investing_strategy_how_patience_and_di: ut trillions while Berkshire kept growing. This principle—staying within your ""—protects against the biggest investment killer: buying into hype because you don't understand the business being sold.1

Instead of chasing the latest trends, Buffett, who is [still making investment decisions](https://
[10] Bibliotheca: clip_investors_cautiously_lean_into_a_tenuous_stock_market: ’s no surprise that inflation and a recession are also among the top five of respondents’ concerns. Over one-third of respondents believe there is a 50-50 chance of a recession in the next six months.

<iframe allow="encrypted-media 'src'" data-src="https://datawrapper.dwcdn.net/1EY9I/1/" allowfulls
[11] Bibliotheca: clip_investors_cautiously_lean_into_a_tenuous_stock_market: hind them. The most widely bought stocks among individual investors throughout March include popular holdings like Apple and Nvidia, as well as Microsoft, Micron (MU), and Nvidia, according to Schwab.

Conversely, individual investors have been selling chipmakers like Broadcom (AVG), and AMD (AMD), 

##### TAVILY NEWS (≤30d) (5 hits)
[12] Tavily [Thu, 23 Ap]: # Apple Stock Rose on New Security Shield that Destroys the FBI’s Hidden Peephole into Private Messages. * Apple stock rose 2.6% on Wednesday as the firm successfully shut down a secret way for the FBI to spy on private messages. * The latest security fix ensures that “notifications marked for delet
     URL: https://www.tipranks.com/news/apple-stock-jumps-as-new-security-shield-destroys-the-fbis-hidden-peephole-into-private-messages
[13] Tavily [Tue, 21 Ap]: # Stock market today: Dow, S&P 500, and Nasdaq turn negative amid Warsh hearing, Apple CEO change, Iran uncertainty. US stocks turned negative on Tuesday as investors assessed Fed chair appointee Kevin Warsh’s confirmation hearing and weighed Tim Cook’s exit as Apple (AAPL) CEO. Federal Reserve chai
     URL: https://finance.yahoo.com/markets/stocks/live/stock-market-today-dow-sp-500-and-nasdaq-turn-negative-amid-warsh-hearing-apple-ceo-change-iran-uncertainty-231748783.html
[14] Tavily [Wed, 22 Ap]: * Investors overwhelmingly rejected self-nominated director candidate Benedict Ong, affirming confidence in NZME’s current board direction. * Looking for the best stocks to buy? * Discover top-performing stock ideas and upgrade to a portfolio of market leaders with  Smart Investor Picks. Learn more 
     URL: https://www.tipranks.com/news/company-announcements/nzme-investors-back-board-endorsed-directors-reject-self-nominated-candidate
[15] Tavily [Tue, 14 Ap]: # Apple Launches New All-in-One Apple Business Platform for Device Management, Email, and Customer Engagement. Apple today launched its new all-in-one Apple Business platform, debuting the refreshed Apple Business web portal and accompanying app. The Apple Business companion app and email, calendar,
     URL: https://www.macrumors.com/2026/04/14/apple-business-platform-launches/
[16] Tavily [Tue, 21 Ap]: Image 4: Radhika Saraogi[Premium Stock Market Today: S&P 500 Sector Leaders and Losers, 4/20/26 Eddie Pan11h ago DIAQQQ](https://www.tipranks.com/news/stock-market-today-sp-500-sector-leaders-and-losers-4-20-26 "DIA | QQQ | SPY"). Image 5: Radhika Saraogi[Premium SoundHound AI Stock (SOUN) Rises des
     URL: https://www.tipranks.com/news/company-announcements/rc-fornax-hosts-investor-webinar-to-outline-strategy-and-engage-shareholders

##### TAVILY GUIDANCE (≤90d) (5 hits)
[17] Tavily [Mon, 06 Ap]: **See today’s best-performing stocks on TipRanks >>**. ### UnitedHealth (UNH) or Humana (HUM): Which Stock Is the Better Buy After CMS’ Surprise Rate Hike. HUMUNH](/news/unitedhealth-unh-or-humana-hum-which-stock-is-the-better-buy-after-cms-surprise-rate-hike "HUM | UNH"). ### Stock Market Futures M
     URL: https://www.tipranks.

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AAPL_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AAPL_STORY.md` (cemetery archive)_

#### Apple — AAPL

##### Análise de Investimento · Modo FULL · Jurisdição US

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/AAPL_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 416.2 bi · EBITDA est. R$ 146.35 bi · FCF R$ 98.77 bi · ROE 152% · DGR 10.9% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 8/9 · Altman Z=10.70 (safe) · Beneish M=-2.37 (clean) |
| **5 — Classification** | Modo A-US · Growth (5/12) · Buffett/Quality (5/12) |
| **5.5 — Council Debate** | NEEDS_DATA (low) · 1 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. Apple, com ticker AAPL, é uma empresa líder no setor tecnológico, conhecida por sua variedade de produtos e serviços que incluem smartphones (iPhone), computadores pessoais (Mac), tablets (iPad), wearables (Apple Watch) e sistemas operacionais (iOS, macOS). A empresa também oferece um ecossistema de serviços digitais como a App Store, Apple Music, iCloud e o Apple Pay. Além disso, recentemente lançou uma plataforma empresarial integrada que abrange gerenciamento de dispositivos, email e engajamento com clientes.

A armadilha típica para investidores ao analisar empresas como a Apple é confundir a força da marca e do produto com o verdadeiro diferencial competitivo. Embora a empresa seja reconhecida globalmente por seus produtos inovadores, seu sucesso real reside em sua capacidade de criar um ecossistema interconectado que mantém os usuários engajados e fidelizados. A Apple não é apenas uma fabricante de hardware; ela oferece soluções completas baseadas em software e serviços que complementam seus dispositivos.

No cenário competitivo, a Apple enfrenta desafios significativos de empresas como Samsung e Huawei no mercado global, mas mantém sua posição dominante através da integração perfeita entre hardware e software. A recente notícia sobre uma atualização de segurança que impede o acesso secreto do FBI às mensagens privadas dos usuários demonstra a capacidade da empresa em proteger a confidencialidade e a segurança dos dados dos clientes, um ponto forte competitivo.

##### Ato 2 — O Contexto

O cenário macroeconômico atual é caracterizado por uma taxa de juros federal nos Estados Unidos (Fed Funds) entre 4.25% e 4.50%, enquanto a taxa de juro dos títulos do Tesouro americano a dez anos está em aproximadamente 4.2%. O custo de capital próprio (Ke) é estimado em cerca de 10%. A economia está atualmente no final da expansão, com sinais emergentes de enfraquecimento.

Para o setor tecnológico e para a Apple especificamente, este ambiente macroeconômico cria um desafio significativo. As taxas de juros mais altas aumentam os custos de capital, tornando mais caro financiar novos projetos ou expansões. Além disso, a possibilidade de uma recessão no horizonte curto pode reduzir o gasto dos consumidores em produtos não essenciais e tecnológicos premium.

Recentemente, houve notícias sobre um potencial aumento na tensão geopolítica relacionada à situação do Irã, que poderia afetar as cadeias de suprimentos globais. Para a Apple, essa incerteza pode aumentar os custos operacionais e criar instabilidade nos mercados financeiros em que opera.

Além disso, a empresa enfrenta desafios regulatórios crescentes em vários países, incluindo uma ação judicial na Califórnia relacionada à contaminação por PFAS em Apple Watch Bands. Essas questões podem aumentar os custos legais e operacionais da empresa e potencialmente afetar sua reputação global.

Em suma, embora o cenário macroeconômico apresente desafios significativos para a Apple, a empresa continua a demonstrar resiliência através de seu forte ecossistema integrado e foco em segurança e privacidade dos usuários.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela uma trajetória de crescimento sustentável e lucratividade crescente. As métricas financeiras anuais fornecem um retrato detalhado desta jornada, destacando tanto os pontos fortes quanto as áreas que requerem atenção.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 394.33B | R$ 119.44B | R$ 131.38B | 33.3% | R$ 99.80B | 25.3% | R$ 111.44B |
| 2023 | R$ 383.29B | R$ 114.30B | R$ 125.73B | 32.8% | R$ 97.00B | 25.3% | R$ 99.58B |
| 2024 | R$ 391.04B | R$ 123.22B | R$ 135.54B | 34.7% | R$ 93.74B | 24.0% | R$ 108.81B |
| 2025 | R$ 416.16B | R$ 133.05B | R$ 146.35B | 35.2% | R$ 112.01B | 26.9% | R$ 98.77B |

A receita da empresa apresentou um crescimento anual composto (CAGR) de aproximadamente 3,4% entre os anos de 2022 e 2025, com uma ligeira queda em 2023 seguida por um aumento significativo em 2025. Este padrão reflete a capacidade da empresa de navegar através das flutuações do mercado sem comprometer sua posição financeira.

A margem EBITDA aumentou consistentemente, passando de 33,3% em 2022 para 35,2% em 2025. Esta expansão é um indicador forte da eficiência operacional e do controle de custos que a empresa tem demonstrado ao longo dos anos.

O fluxo de caixa livre (FCF) também mostrou uma trajetória positiva, com picos em 2022 e 2024, embora tenha diminuído ligeiramente em 2025. Este comportamento do FCF é particularmente relevante quando se considera que o lucro contábil pode esconder provisões e ajustes; o FCF, por outro lado, fornece uma visão mais clara da geração de caixa operacional.

A empresa tem mantido um histórico consistente de distribuição de dividendos, com um crescimento anual médio de aproximadamente 4,5% entre 2021 e 2026. No entanto, o dividendo total reportado em 2026 apresenta uma queda significativa para R$ 0,26 por ação, sugerindo que este valor pode não ser estrutural e poderia refletir ajustes temporários.

A taxa de crescimento dos dividendos (DGR) calculada é de 10,9% ao ano, excluindo eventuais pagamentos extraordinários. Este DGR sustentado por quinze anos consecutivos fornece uma tese sólida para a estratégia de reinvestimento em dividendos (DRIP).

##### Ato 4 — O Balanço

O balanço financeiro da empresa no final de 2026 revela um perfil robusto, embora com alguns pontos que merecem atenção. Com uma relação preço-lucro (P/E) de 34,39 e uma relação preço-ativos líquidos (P/B) de 45,24, a empresa é avaliada como premium no mercado.

A taxa de dividendos (DY) da empresa é de apenas 0,38%, o que pode ser visto como um indicador de que os investidores estão dispostos a pagar um prêmio por uma exposição à marca e ao potencial de crescimento futuro. O retorno sobre o patrimônio líquido (ROE) da empresa é impressionante, com 152,02%, superando significativamente o custo do capital próprio (Ke) estimado em cerca de 18,25% no Brasil.

A relação dívida bruta/EBITDA ajustada, calculada como R$ 49,33 bi dividido por R$ 146,35 bi, resulta em uma alavancagem financeira de aproximadamente 0,34 vezes. Este nível é considerado moderado e indica que a empresa tem espaço para aumentar sua alavancagem sem comprometer sua solidez financeira.

O Current Ratio da empresa está acima de 1, sugerindo um bom grau de liquidez curta prazo. No entanto, é importante monitorar o crescimento da despesa financeira e a tendência de alavancagem para garantir que estes não comprometam a sustentabilidade financeira a longo prazo.

Em resumo, embora a empresa apresente um balanço sólido com indicadores robustos, é crucial manter uma vigilância constante sobre as tendências emergentes de alavancagem e despesas financeiras para garantir que o crescimento contínuo seja sustentável.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa revela uma posição distintiva no mercado, refletindo tanto a sua valoração intrínseca quanto a percepção do setor e do índice geral. Com um preço-valor de vendas (P/E) de 34.39x, a companhia está significativamente acima da média setorial de 22.15x e do índice Ibov/S&P de 21.00x. Este múltiplo elevado sugere que os investidores atribuem um valor futuro substancial à empresa, possivelmente refletindo expectativas de crescimento acelerado ou vantagens competitivas sustentáveis.

A relação preço-benefício (P/B) da companhia é ainda mais notável, com 45.24x contra uma média setorial de 6.58x e um índice Ibov/S&P de 3.50x. Este indicador elevado pode ser interpretado como uma confiança na solidez do ativo da empresa ou em sua capacidade de gerar lucros futuros consistentes, apesar de representar um risco significativo se as expectativas não forem alcançadas.

O dividendo yield (DY) da companhia é de 0.38%, inferior à média setorial de 1.3% e ao índice Ibov/S&P de 1.5%. Este DY baixo pode indicar que a empresa está reinvestindo lucros em expansão, inovação ou outros projetos estratégicos, em vez de distribuir dividendos aos acionistas.

O fluxo de caixa livre (FCF) yield da companhia é de 2.5%, muito abaixo do setor e do índice geral, que são respectivamente de 9.9% e 4.0%. Este indicador sugere que a empresa está gerando um retorno sobre o capital investido menor em comparação com as médias setoriais e do mercado.

O retorno sobre o patrimônio líquido (ROE) da companhia é de 152.0%, bem acima da média setorial de 26% e do índice geral de 16%. Este alto ROE pode indicar uma eficiência operacional excepcional ou um uso estratégico de dívida para alavancagem financeira.

Finalmente, a relação negativo de dívidas sobre EBITDA (ND/EBITDA) da companhia é de 0.15x, significativamente inferior à média setorial de 0.06x e ao índice geral não disponível. Este indicador sugere que a empresa tem uma posição financeira sólida com baixo nível de endividamento.

| Múltiplo | AAPL | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 34.39x | 22.15x | 21.00x |
| P/B | 45.24x | 6.58x | 3.50x |
| DY | 0.4% | 1.3% | 1.5% |
| FCF Yield | 2.5% | 9.9% | 4.0% |
| ROE | 152.0% | 26.0% | 16.0% |
| ND/EBITDA | 0.15x | 0.06x | — |

##### Ato 6 — Os Quality Scores

Os indicadores de qualidade financeira da empresa, conhecidos como "Quality Scores", fornecem uma visão aprofundada sobre as práticas contábeis e o desempenho operacional. O Piotroski F-Score da companhia é de 8/9 (2025-09-30), indicando um excelente nível de qualidade financeira, com apenas uma das nove categorias não sendo atendida.

O Altman Z-Score da empresa é de 10.70, classificado na zona segura e com confiança alta. Este resultado sugere que a companhia tem baixo risco de insolvência, refletindo práticas financeiras sólidas e uma posição forte no mercado.

O Beneish M-Score da empresa é -2.37, indicando uma zona limpa com alta confiança. Isto sugere que não há evidências significativas de manipulação contábil ou distorções nos relatórios financeiros da companhia.

Em resumo, os "Quality Scores" da empresa sugerem um desempenho sólido e práticas financeiras robustas, reforçando a confiança dos investidores na sustentabilidade do negócio.

---

##### Ato 7 — O Moat e a Gestão

A Apple Inc. (AAPL) tem um moat extremamente robusto que se classifica como Wide, fundamentado em múltiplos aspectos de sua estratégia empresarial e inovação contínua. As barreiras à entrada criadas pela empresa são notáveis, incluindo a escala de produção e distribuição, os custos de troca significativos para os usuários da plataforma iOS, os efeitos de rede através do App Store e o portfólio intangível de patentes e marcas registradas.

###### Escala e Custo

A Apple beneficia grandemente da economia de escala em sua cadeia de fornecimento global. A capacidade da empresa para negociar com fornecedores de componentes, bem como a eficiência operacional resultante dessa escala, cria uma barreira significativa para novos entrantes no mercado.

###### Custos de Troca

Os custos de troca são altos para os usuários que desejam mudar de plataforma iOS para concorrentes. A integração profunda entre dispositivos Apple e serviços como o iCloud, a App Store e outros recursos exclusivos cria uma forte aderência ao ecossistema da empresa.

###### Efeitos de Rede

A vasta comunidade de desenvolvedores que criam aplicativos para a plataforma iOS contribui para os efeitos de rede. Quanto mais usuários e desenvolvedores existem, maior o valor percebido do sistema para novos participantes, aumentando ainda mais a aderência ao ecossistema.

###### Ativos Intangíveis

A marca Apple é um ativo intangível extremamente valioso que serve como uma barreira à entrada. Além disso, as patentes e os direitos autorais protegem inovações tecnológicas cruciais da empresa de serem copiadas por concorrentes.

###### Eficiência Operacional

A eficiência operacional da Apple é notável, refletida em seus altos retornos sobre o capital empregado (ROE) e margens EBIT consistentemente elevadas. Essa eficiência cria uma barreira de custo para concorrentes que não conseguem replicar a mesma estrutura operacional.

###### Gestão

A gestão da Apple, sob liderança de Tim Cook desde 2011, tem sido notável em sua capacidade de manter o crescimento e inovação contínuos. A recente notícia sobre a renúncia de Cook como CEO não foi mencionada nas web facts fornecidas, portanto, consideraremos que os dados estão ausentes para este aspecto.

###### Propriedade Interna

Dado não disponível.

###### Transações Internas dos Últimos 6 Meses

Dado não disponível.

##### Ato 8 — O Veredito

###### Perfil Filosófico
A Apple apresenta um perfil filosófico que combina forças de crescimento e qualidade, com uma ênfase notável na qualidade. As pontuações detalhadas são as seguintes:
- **Growth:** 5 (ROE alto, expansão da margem EBIT)
- **Buffett/Quality:** 5 (ROE acima do padrão, ND/EBITDA baixo e consistência histórica)

###### O que o preço desconta
O atual preço de mercado da Apple reflete uma expectativa elevada em relação ao crescimento futuro e à sustentabilidade dos lucros. A empresa tem demonstrado um histórico consistente de inovação e expansão, o que sugere que os investidores estão otimistas quanto às capacidades futuras da companhia.

###### O que os fundamentos sugerem
Os fundamentais atuais da Apple são robustos, com retornos sobre o patrimônio líquido (ROE) de 152% e uma história consistente de dividendos ao longo dos últimos 15 anos. A empresa mantém um forte equilíbrio entre crescimento e qualidade operacional.

###### DCF — A ân

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AAPL_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\AAPL_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — AAPL            moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              5
  Entry price.........: US$      121.89
  Cost basis..........: US$      609.45
  Price now...........: US$      271.06
  Market value now....: US$    1,355.30  [+122.4% nao-realizado]
  DY t12m.............: 0.38%  (R$/US$ 1.0400/share)
  DY vs own 10y.......: P 2 [EXPENSIVE]  (actual 0.38% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=15  hist_g_5y=0.045  hist_g_raw=0.045  gordon_g=1.320  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |  +10.80%  |   -1.00% |  +10.18%       |
  | base         |  +18.00%  |   +0.00% |  +18.38%       |
  | optimista    |  +22.00%  |   +1.00% |  +23.38%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     25       |      >40       |        1       |
  | base         |     18       |      >40       |        1       |
  | optimista    |     16       |      >40       |        1       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      2,206 | US$      3,161 | US$      3,888 |
  |  10y  | US$      3,594 | US$      7,370 | US$     11,143 |
  |  15y  | US$      5,860 | US$     17,187 | US$     31,915 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AAPL.md` (cemetery archive)_

#### AAPL — Apple

#holding #us #technology

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 6.0/10  |  **Confiança**: 70%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 10.0/10 | 35% | `██████████` |
| Valuation  | 2.0/10 | 30% | `██░░░░░░░░` |
| Momentum   | 6.7/10 | 20% | `███████░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z 10.702066138022928 (SAFE), Piotroski 8/9 (STRONG), DivSafety 95.0/100
- **Valuation**: Screen 0.40, DY percentil P0 (EXPENSIVE)
- **Momentum**: 1d 1.17%, 30d 10.37%, YTD 6.09%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- total 6.0 na zona neutra
- quality forte
- valuation caro

##### Links

- Sector: [[sectors/Technology|Technology]]
- Market: [[markets/US|US]]
- Peers: [[ACN]] · [[PLTR]] · [[TSM]] · [[IBM]] · [[JKHY]]
- 🎯 **Thesis**: [[wiki/holdings/AAPL|thesis deep]]

##### Snapshot

- **Preço**: $287.51  (2026-05-06)    _+1.17% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: 10.702 (safe)
- **Piotroski**: 8/9
- **Div Safety**: 95.0/100 (SAFE)
- **Posição**: 5.0 sh @ $121.89000000000001  →  P&L 135.88%

##### Fundamentals

- P/E: 34.765415 | P/B: 47.93431 | DY: 0.36%
- ROE: 141.47% | EPS: 8.27 | BVPS: 5.998
- Streak div: 15y | Aristocrat: False

##### Dividendos recentes

- 2026-05-11: $0.2600
- 2026-02-09: $0.2600
- 2025-11-10: $0.2600
- 2025-08-11: $0.2600
- 2025-05-12: $0.2600

##### Eventos (SEC/CVM)

- **2026-05-01** `10-Q` — 10-Q
- **2026-04-30** `8-K` — 8-K | 2.02,9.01
- **2026-04-20** `8-K` — 8-K | 5.02
- **2026-02-24** `8-K` — 8-K | 5.07,9.01
- **2026-01-30** `10-Q` — 10-Q

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=9 · analyst=0 · themes=1_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-10 | WSJ Podcasts | risk | 0.90 | Tim Cook alertou que os gastos de capital da Apple aumentarão devido aos custos crescentes de memória. |
| 2026-05-10 | WSJ Podcasts | valuation | 0.80 | A Apple, apesar de sua capacidade de compra em massa de chips e outros componentes, não está desempenhando tão bem quanto as empresas que f… |
| 2026-05-05 | Invest Like the Best | management | 0.90 | O CEO da Apple está focado em reinventar a empresa e adaptá-la à era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.85 | O CEO da Apple acredita que o modo de fundador é crucial para lidar com a era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple aprendeu com Hiroki Asai, ex-diretor criativo de Steve Jobs na Apple. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple enfatiza a importância de simplicidade e detalhes na gestão da empresa. |
| 2026-05-05 | Invest Like the Best | management | 0.75 | O CEO da Apple acredita que o sucesso de uma empresa depende muito das pessoas que ela contrata. |
| 2026-05-03 | Stock Pickers | management | 0.90 | Warren Buffett elogiou Tim Cook da Apple durante a apresentação da Berkshire Hathaway. |
| 2026-05-03 | Stock Pickers | valuation | 0.80 | Warren Buffett vendeu grande parte da posição em Apple, mas ainda mantém uma porção significativa. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ Podcasts | semis_cycle | bullish | O ciclo de semicondutores está em um superciclo devido a contratos mais longos e previsibilidade nas vendas,… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: +0.00%
- **Drawdown 5y**: +0.00%
- **YTD**: +6.09%
- **YoY (1y)**: +44.83%
- **CAGR 3y**: +18.32%  |  **5y**: +17.17%  |  **10y**: +28.63%
- **Vol annual**: +30.77%
- **Sharpe 3y** (rf=4%): +0.56

###### Dividendos
- **DY 5y avg**: +0.49%
- **Div CAGR 5y**: +4.46%
- **Frequency**: quarterly
- **Streak** (sem cortes): 13 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-09-30 | n/a | n/a | n/a |
| 2022-09-30 | $394.33B | $99.80B | $111.44B |
| 2023-09-30 | $383.29B | $97.00B | $99.58B |
| 2024-09-30 | $391.04B | $93.74B | $108.81B |
| 2025-09-30 | $416.16B | $112.01B | $98.77B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "AAPL — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: AAPL
    data: [197.49, 212.33, 206.86, 200.21, 201.7, 203.92, 199.2, 196.58, 201.56, 207.82, 210.01, 208.62, 211.18, 213.76, 209.05, 202.92, 227.18, 231.59, 224.9, 230.49, 238.47, 234.35, 236.7, 245.5, 256.87, 255.45, 256.48, 247.66, 252.29, 259.58, 269.7, 270.04, 269.43, 272.41, 266.25, 277.55, 284.15, 277.18, 274.11, 273.67, 273.4, 271.01, 259.04, 259.96, 247.65, 258.27, 270.01, 278.12, 261.73, 260.58, 274.23, 263.75, 259.88, 250.12, 248.96, 252.62, 253.79, 253.5, 259.2, 270.23, 273.43, 270.71, 276.83]
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
    data: [33.642586, 33.34071, 33.34177, 34.249683, 34.543724, 33.73511, 34.31139, 34.35488, 34.35488, 33.917618, 34.31052, 34.198734, 34.391636, 33.514526, 34.44606, 34.765415]
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
    data: [152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 152.02, 141.47, 141.47, 141.47]
  - title: DY %
    data: [40.0, 39.0, 39.0, 38.0, 38.0, 0.39, 0.38, 0.38, 0.38, 0.39, 0.38, 0.38, 0.38, 0.38, 0.37, 0.36]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AAPL_DOSSIE.md` (cemetery archive)_

#### 📑 AAPL — Apple

> Generated **2026-04-26** by `ii dossier AAPL`. Cross-links: [[AAPL]] · [[AAPL_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

AAPL negoceia a P/E 34.35 com DY 0.38% e ROE 152.02% (alavancado por buybacks), IC MIXED com baixa confiança (40% consenso). Achado-chave: **valuation stretch** — P/E acima do screen Buffett (≤20) e Services growth a desacelerar; a tese de moat ecossistema iOS continua intacta mas o múltiplo precifica perfeição. Posição growth/tech (não DRIP) — manter para compounding sem acelerar reforços.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 7.89  |  **BVPS**: 6.00
- **ROE**: 152.02%  |  **P/E**: 34.35  |  **P/B**: 45.19
- **DY**: 0.38%  |  **Streak div**: 15y  |  **Market cap**: USD 3979.47B
- **Last price**: USD 271.06 (2026-04-26)  |  **YoY**: +29.5%

##### 2. Synthetic IC

**🏛️ MIXED** (low confidence, 40.0% consensus)

→ Detalhe: [[AAPL_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-24)**: Apple é uma excelente posição long-term para um investidor Buffett/Graham devido à sua robusta geração de lucros e retorno sobre o patrimônio líquido (ROE) de 152,02%. A empresa mantém um histórico consistente de dividendos por 15 anos consecutivos, apesar do rendimento anual de dividendos baixo de apenas 0,39%. Com uma relação P/E de 33,74 e uma relação P/B de 44,38, a empresa ainda oferece um potencial significativo para valorização acionária.

**Key assumptions**:
1. A Apple continuará a gerar lucros consistentes com ROE superior a 150%.
2. O crescimento contínuo em suas divisões de serviços e dispositivos mantém o momentum financeiro da empresa.
3. A relação P/E permanecerá estável ou cairá, refletindo um múltiplo mais justo para o desempenho operacional.

→ Vault: [[AAPL]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 34.35** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 34.35** esticado vs critério.
- **P/B = 45.19** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **45.19** esticado.
- **DY = 0.38%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.38%** fraco; verificar se é growth pick.
- **ROE = 152.02%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **152.02%** compounder-grade.
- **Graham Number ≈ R$ 32.64** vs preço **R$ 271.06** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 15y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🟡 **Services growth deceleration** — Services tem sido o multiple-driver; uma queda <10% YoY pressiona o múltiplo. Trigger: Services revenue YoY < 10%.
- 🟡 **China demand (iPhone)** — Greater China receita -5/-10% por trimestres consecutivos é material. Trigger: Greater China revenue YoY < -5% por 2 quarters.
- 🟡 **AI catch-up (Apple Intelligence)** — atraso vs MSFT/GOOGL/META em GenAI pode erodir Services premium. Trigger: GenAI capex YoY < peers' avg.
- 🟡 **Valuation stretch** — P/E 34 vs screen Buffett ≤20. Trigger: `fundamentals.pe > 38`.
- 🟢 **Antitrust (DoJ/EU/App Store)** — overhang persistente mas slow-burn.

##### 5. Position sizing

**Status atual**: holding (in portfolio)

**Manter para compounding** — posição growth/tech (não DRIP, DY 0.38% irrelevante). Não acelerar reforços com P/E 34; aguardar pullback -15%+ ou correcção do múltiplo. USD em conta US.

##### 6. Tracking triggers (auto-monitoring)

- **PE overstretch** — `fundamentals.pe > 38` → trim candidate.
- **Services deceleration** — Services revenue YoY < 10% por 2 quarters → tese rota.
- **China revenue collapse** — Greater China YoY < -5% por 2 quarters → reavaliação.
- **Earnings miss** — `events.kind='earnings'` surprise < -10% → reavaliar.
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
*Generated by `ii dossier AAPL` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=9 · analyst=0 · themes=1_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-10 | WSJ Podcasts | risk | 0.90 | Tim Cook alertou que os gastos de capital da Apple aumentarão devido aos custos crescentes de memória. |
| 2026-05-10 | WSJ Podcasts | valuation | 0.80 | A Apple, apesar de sua capacidade de compra em massa de chips e outros componentes, não está desempenhando tão bem quanto as empresas que f… |
| 2026-05-05 | Invest Like the Best | management | 0.90 | O CEO da Apple está focado em reinventar a empresa e adaptá-la à era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.85 | O CEO da Apple acredita que o modo de fundador é crucial para lidar com a era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple aprendeu com Hiroki Asai, ex-diretor criativo de Steve Jobs na Apple. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple enfatiza a importância de simplicidade e detalhes na gestão da empresa. |
| 2026-05-05 | Invest Like the Best | management | 0.75 | O CEO da Apple acredita que o sucesso de uma empresa depende muito das pessoas que ela contrata. |
| 2026-05-03 | Stock Pickers | management | 0.90 | Warren Buffett elogiou Tim Cook da Apple durante a apresentação da Berkshire Hathaway. |
| 2026-05-03 | Stock Pickers | valuation | 0.80 | Warren Buffett vendeu grande parte da posição em Apple, mas ainda mantém uma porção significativa. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ Podcasts | semis_cycle | bullish | O ciclo de semicondutores está em um superciclo devido a contratos mais longos e previsibilidade nas vendas,… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AAPL_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — AAPL

**Committee verdict**: **MIXED** (low confidence, 40% consensus)  
**Votes**: BUY=1 | HOLD=2 | AVOID=2  
**Avg conviction majority**: 6.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- Excelente negócio, ROE alto
- Geração de lucros consistente
- Inovações contínuas

**Key risk**: Multiplos altos, potencial correção significativa se múltiplo cair

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE superior a 150%
- crescimento contínuo em serviços e dispositivos
- resultados financeiros superam expectativas

**Key risk**: potencial reversão do regime de liquidez favorável

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/E e P/B extremamente elevados
- Baixo dividend yield
- Falta de anti-fragilidade

**Key risk**: Overvaluation and lack of convex payoffs expose to hidden risks

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Valuation múltiplos elevados
- Margem de segurança insuficiente
- Risco de overvaluation

**Key risk**: Overvaluation e potencial correção significativa nos preços

###### 🟡 Ray Dalio — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- Excelente ROE e geração de lucros
- Dividendos consistentes por 15 anos
- Crescimento contínuo em serviços

**Key risk**: P/E muito elevado (35,55) pode indicar sobreavaliação

##### 📊 Context provided

```
TICKER: US:AAPL

FUNDAMENTALS LATEST:
  pe: 35.55394
  pb: 40.402203
  dy: 0.44%
  roe: 141.47%
  net_debt_ebitda: 0.10129017754727493

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: Apple é uma excelente posição long-term para um investidor Buffett/Graham devido à sua robusta geração de lucros e retorno sobre o patrimônio líquido (ROE) de 152,02%. A empresa mantém um histórico consistente de dividendos por 15 anos consecutivos, apesar do rendimento anual de dividendos baixo de apenas 0,39%. Com uma relação P/E de 33,74 e uma relação P/B de 44,38, a empresa ainda oferece um potencial significativo para valorização acionária.

**Key assumptions**:
1. A Apple continuará a gerar lucros consistentes com ROE superior a 150%.
2. O crescimento contínuo em suas divisões de serviços e dispositivos mantém o momentum financeiro da empresa.
3. A relação P/E permanecerá estável ou cairá, refletindo um múltiplo mais justo para o desempenho operacional.

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Apple (AAPL) Stock Pops on Q2 Beat – Top Analysts Raise Price Targets - TipRanks [Sat, 02 Ma]
    # Apple (AAPL) Stock Pops on Q2 Beat – Top Analysts Raise Price Targets. • Several analysts reacted to Apple’s earnings report with raised price targets. The upbeat results boosted investor confidence
  - How Apple (AAPL) Plans to Turn the iPhone Camera into an AI Tool - TipRanks [Wed, 29 Ap]
    # How Apple (AAPL) Plans to Turn the iPhone Camera into an AI Tool. * Apple is planning to bring more artificial intelligence into the iPhone’s camera app as part of its upcoming iOS 27 update. Tech g
  - Apple Inc. $AAPL Shares Acquired by Brookwood Investment Group LLC - InsuranceNewsNet [Thu, 30 Ap]
    $AAPL Shares Acquired by Brookwood Investment Group LLC - Insurance News | InsuranceNewsNet. HomeNow reading INN Insider News. INN Insider News RSSGet our newsletter. 55 seconds ago INN Insider News. 
  - Apple tops Q2 e
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=9 · analyst=0 · themes=1_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-10 | WSJ Podcasts | risk | 0.90 | Tim Cook alertou que os gastos de capital da Apple aumentarão devido aos custos crescentes de memória. |
| 2026-05-10 | WSJ Podcasts | valuation | 0.80 | A Apple, apesar de sua capacidade de compra em massa de chips e outros componentes, não está desempenhando tão bem quanto as empresas que f… |
| 2026-05-05 | Invest Like the Best | management | 0.90 | O CEO da Apple está focado em reinventar a empresa e adaptá-la à era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.85 | O CEO da Apple acredita que o modo de fundador é crucial para lidar com a era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple aprendeu com Hiroki Asai, ex-diretor criativo de Steve Jobs na Apple. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple enfatiza a importância de simplicidade e detalhes na gestão da empresa. |
| 2026-05-05 | Invest Like the Best | management | 0.75 | O CEO da Apple acredita que o sucesso de uma empresa depende muito das pessoas que ela contrata. |
| 2026-05-03 | Stock Pickers | management | 0.90 | Warren Buffett elogiou Tim Cook da Apple durante a apresentação da Berkshire Hathaway. |
| 2026-05-03 | Stock Pickers | valuation | 0.80 | Warren Buffett vendeu grande parte da posição em Apple, mas ainda mantém uma porção significativa. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ Podcasts | semis_cycle | bullish | O ciclo de semicondutores está em um superciclo devido a contratos mais longos e previsibilidade nas vendas,… |

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AAPL_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — AAPL

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `medium_variance_long` (magnitude 2/5)  
**Interpretation**: moderate edge

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: neutral (2 bull / 0 bear / 3 neutral)  
**Cached**: True

- 🟡 [neutral] [Here are Thursday's biggest analyst calls: Nvidia, Apple, Tesla, CoreWeave, Meta, Dick's, ResMed & more - CNBC](https://www.cnbc.com/2026/04/16/thursday-street-analyst-calls-stocks-include-nvidia-apple-tesla-meta.html) (Thu, 16 Ap)
- 🟢 [bull] [Apple (AAPL) Stock Pops on Q2 Beat – Top Analysts Raise Price Targets - TipRanks](https://www.tipranks.com/news/apple-aapl-stock-pops-on-q2-beat-top-analysts-raise-price-targets) (Sat, 02 Ma)
- 🟡 [neutral] [‘That Was an Impressive Quarter’: Morgan Stanley Hikes Apple (AAPL) Stock’s Price Target Following Strong Earnings - Tip](https://www.tipranks.com/news/article/that-was-an-impressive-quarter-morgan-stanley-hikes-apple-aapl-stocks-price-target-following-strong-earnings) (Fri, 01 Ma)
- 🟡 [neutral] [‘Scoop Up,’ Says Morgan Stanley on UnitedHealth Stock (UNH) Ahead of Earnings - TipRanks](https://www.tipranks.com/news/scoop-up-says-morgan-stanley-on-unitedhealth-stock-unh-ahead-of-earnings) (Mon, 20 Ap)
- 🟢 [bull] [Wall Street is bullish ahead of Apple earnings, but is looking for answers about the post-Tim Cook era - Business Inside](https://www.businessinsider.com/apple-earnings-preview-q2-wall-street-analysts-john-ternus-aapl-2026-4) (Wed, 29 Ap)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: Apple é uma excelente posição long-term para um investidor Buffett/Graham devido à sua robusta geração de lucros e retorno sobre o patrimônio líquido (ROE) de 152,02%. A empresa mantém um histórico consistente de dividendos por 15 anos consecutivos, apesar do rendimento anual de dividendos baixo de apenas 0,39%. Com uma relação P/E de 33,74 e uma relação P/B de 44,38, a empresa ainda oferece um potencial significativo para valorização acionária.

**Key assumptions**:
1. A Apple continuará a gerar lucros consistentes com ROE superior a 150%.
2. O crescimento contínuo em suas divisões de serviços e dispositivos mantém o momentum financeiro da empresa.
3. A relação P/E permanecerá estável ou cairá, refletindo um múltiplo mais justo para o desempenho operacional.

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=9 · analyst=0 · themes=1_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-10 | WSJ Podcasts | risk | 0.90 | Tim Cook alertou que os gastos de capital da Apple aumentarão devido aos custos crescentes de memória. |
| 2026-05-10 | WSJ Podcasts | valuation | 0.80 | A Apple, apesar de sua capacidade de compra em massa de chips e outros componentes, não está desempenhando tão bem quanto as empresas que f… |
| 2026-05-05 | Invest Like the Best | management | 0.90 | O CEO da Apple está focado em reinventar a empresa e adaptá-la à era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.85 | O CEO da Apple acredita que o modo de fundador é crucial para lidar com a era da IA. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple aprendeu com Hiroki Asai, ex-diretor criativo de Steve Jobs na Apple. |
| 2026-05-05 | Invest Like the Best | management | 0.80 | O CEO da Apple enfatiza a importância de simplicidade e detalhes na gestão da empresa. |
| 2026-05-05 | Invest Like the Best | management | 0.75 | O CEO da Apple acredita que o sucesso de uma empresa depende muito das pessoas que ela contrata. |
| 2026-05-03 | Stock Pickers | management | 0.90 | Warren Buffett elogiou Tim Cook da Apple durante a apresentação da Berkshire Hathaway. |
| 2026-05-03 | Stock Pickers | valuation | 0.80 | Warren Buffett vendeu grande parte da posição em Apple, mas ainda mantém uma porção significativa. |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ Podcasts | semis_cycle | bullish | O ciclo de semicondutores está em um superciclo devido a contratos mais longos e previsibilidade nas vendas,… |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\AAPL.md` (cemetery archive)_

#### 🎯 Thesis: [[AAPL]] — Apple

> World's largest consumer electronics + services company. Ecosystem moat + installed base monetization. Warren Buffett's largest single stock position. Core quality compounder.

##### Intent
**Compounder** — growth + capital return (buyback-heavy). DY ~0.5% secundário.

##### Business snapshot

Segments:
- **iPhone** ~55% revenue — installed base 1.5B+ active
- **Services** ~25% revenue — App Store, iCloud, Apple Music, Apple TV+, Apple Pay, Apple Care
- **Wearables** (Watch, AirPods) ~10%
- **iPad** ~6%
- **Mac** ~8%

Services growing 15-20%/y, offsetting iPhone saturation.

##### Por que detemos

1. **Ecosystem moat** — iPhone + Watch + Mac + AirPods + Services = switching costs high.
2. **Installed base monetization** — 2B+ active devices generating Services revenue.
3. **Buyback aggressive** — $100B+/y, reducing share count 3-5%/y.
4. **Supply chain mastery** — Tim Cook's legacy, margins resilient.
5. **Cash hoard $160B+** — optionality for M&A or accelerated buyback.
6. **Brand premium** — willingness to pay 20-50% over Android equivalent.

##### Moat

- **Ecosystem switching cost** — iMessage lock-in, photos, contacts, subscriptions.
- **Brand premium** globally.
- **Supply chain scale** — Foxconn + suppliers dependent on Apple volumes.
- **App Store tax** (15-30% of digital purchases) — high margin recurring.
- **Weak moat**: China revenue (15-20%) exposed to geopolitics + local competition (Huawei comeback); Services revenue faces regulatory pressure (Epic v Apple, EU DMA).

##### Current state (2026-04)

- iPhone 17 cycle modest.
- Apple Intelligence (AI) rollout — slow but positioning for iPhone 18+ upgrade cycle.
- Services growth strong.
- China revenue declining (Huawei Mate pro resurgence, Xi regulatory pressure).
- India market emerging ($10B+ manufacturing).
- Vision Pro - weak sales, R&D pay-off long-term.
- FTC antitrust cases + DOJ suit ongoing.

##### Invalidation triggers

- [ ] iPhone installed base declining (currently 1.5B, -5% 2 years = thesis crack)
- [ ] Services growth < 8%/y sustained
- [ ] Operating margin < 28% structural (currently 31%)
- [ ] China revenue collapse > 50% (combined geopol + local competition)
- [ ] Antitrust break-up executed (unlikely near-term)
- [ ] Tim Cook departure + strategy pivot sem successor proven (John Ternus?)
- [ ] ROIC < 30% sustained

##### Sizing

- Posição actual: 5 shares
- Target 3-5% sleeve US
- **Compounder buy-and-hold** — don't trim salvo valuation extremo (P/E > 35×)
- Note: Indirect additional exposure via [[BRK-B]] (~40% of BRK equity portfolio).

##### AAPL valuation context

Historical P/E range 15-30×. Current 30-35× premium vs historic.
- **Bull**: services + AI monetization justifies premium.
- **Bear**: iPhone saturation + China erosion + regulation = derating.

Base case: hold, expect 8-12% TSR long-term (EPS growth + buyback + small dividend).


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -4.25%
- **Drawdown 5y**: -4.25%
- **YTD**: +1.11%
- **YoY (1y)**: +33.93%
- **CAGR 3y**: +18.34%  |  **5y**: +15.33%  |  **10y**: +26.43%
- **Vol annual**: +30.83%
- **Sharpe 3y** (rf=4%): +0.56

###### Dividendos
- **DY 5y avg**: +0.49%
- **Div CAGR 5y**: +4.46%
- **Frequency**: quarterly
- **Streak** (sem cortes): 13 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Moat_types]] — ecosystem + switching cost + brand = triple moat
- [[Buffett_quality]] — Apple é pick #1 Buffett moderno
- [[TSM]] — primary chip supplier (indirect AAPL exposure)
- [[BRK-B]] — overlap via BRK stake

## ⚙️ Refresh commands

```bash
ii panorama AAPL --write
ii deepdive AAPL --save-obsidian
ii verdict AAPL --narrate --write
ii fv AAPL
python -m analytics.fair_value_forward --ticker AAPL
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
