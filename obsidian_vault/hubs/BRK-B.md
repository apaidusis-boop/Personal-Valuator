---
type: ticker_hub
ticker: BRK-B
market: us
sector: Holding
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 10
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# BRK-B — Berkshire Hathaway B

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Holding` · `market: US` · `currency: USD` · `bucket: holdings` · `10 sources merged`

## 🎯 Hoje

- **Posição**: 1.0 @ entry 417.99
- **Verdict (DB)**: `HOLD` (score 4.42, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 14.45 · P/B 0.00 · ROE 10.5% · ND/EBITDA -2.28 · Dividend streak 0 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\BRK-B.md` (cemetery archive)_

#### BRK-B — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Holding
- **RI URLs scraped** (1):
  - https://www.berkshirehathaway.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=417.99 · date=2024-03-28

- Total events na DB: **124**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=479.54998779296875
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.10499 · DY=None · P/E=14.272322
- Score (último run): score=0.5 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,5.02,5.03,5.07,9.01 |
| 2026-05-04 | 10-Q | sec | 10-Q |
| 2026-04-16 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-03-13 | proxy | sec | DEF 14A |
| 2026-03-05 | 8-K | sec | 8-K \| 8.01,9.01 |

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

#### 2026-05-07 · Filing 2026-05-07
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\BRK-B_FILING_2026-05-07.md` (cemetery archive)_

#### Filing dossier — [[BRK-B]] · 2026-05-07

**Trigger**: `sec:8-K` no dia `2026-05-07`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1067983/000119312526212148/d74313d8k.htm>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 469.83

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `524.32` |
| HOLD entre | `524.32` — `672.20` (consensus) |
| TRIM entre | `672.20` — `773.03` |
| **SELL acima de** | `773.03` |

_Método: `buffett_ceiling`. Consensus fair = R$672.20. Our fair (mais conservador) = R$524.32._

##### 🔍 Confidence

❌ **disputed** (score=0.50)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.10499` | `0.1036` | +1.3% |
| EPS | `33.61` | `51827.6123` | +99.9% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | HOLD | disputed | `filing:sec:8-K:2026-05-07` |
| 2026-05-08T17:48:11+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | HOLD | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\BRK-B_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[BRK-B|BRK-B]] (Berkshire Hathaway B)

**Final stance**: 🟢 **BUY**  
**Confidence**: `high`  
**Modo (auto)**: A (US)  |  **Sector**: Holding  |  **Held**: sim  
**Elapsed**: 66.5s  |  **Failures**: 0

##### Quem esteve na sala

- [[council.industrials-us]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[council.macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[risk.drift-audit]] — _Chief Risk Officer_ (`risk_officer`)
- [[council.allocation]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- A Berkshire Hathaway B oferece uma relação preço-benefício atrativa, com um P/E de 15.26 e um ROE sustentado de 9.8%
- O Piotroski F-Score de 4/9 e Beneish M-Score de -2.42 indicam uma situação financeira estável
- A relação dívida bruta/EBITDA negativa (-2.15) é preocupante, mas não reflete a solidez financeira ou o potencial de crescimento da empresa

**Dissenso (preservado)**:
- Mariana Macro disse que o DY baixo (46.2%) é um indicador relevante para investidores que buscam dividendos
- Pedro Alocação e Valentina Prudente disseram que a relação dívida bruta/EBITDA negativa pode sugerir desafios financeiros

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ O DY baixo de 46.2% é um ponto de preocupação para investidores que buscam dividendos (Mariana Macro)
- ⚠️ A relação dívida bruta/EBITDA negativa (-2.15) pode sugerir desafios financeiros, mas não reflete a solidez geral da empresa (Pedro Alocação)

**Sizing**: Considerar uma alocação de 1-3% do portfólio para Berkshire Hathaway B, dada sua natureza defensiva e relação preço-benefício atrativa

##### Round 1 — Opening Statements (blind)

###### [[council.industrials-us]] — 🟢 **BUY**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _Berkshire Hathaway B mantém posição atraente com PE de 15 e ROE de 9.8%_

A Berkshire Hathaway B oferece uma relação preço-benefício atrativa, com um P/E de 15.26 e um ROE sustentado de 9.8%. A empresa mantém solidez financeira.

**Métricas**:
- P/E=15.26
- ROE=9.8%
- Liquidez corrente=7.07

**Preocupações**:
- Dividend yield baixo de 46.2%
- Relação dívida bruta/EBITDA negativa (-2.15)

###### [[council.macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Headline**: _Berkshire Hathaway B mantém posição defensiva com PE razoável_

A Berkshire Hathaway B oferece um PE de 15.08 e ROE de 9.8%, indicando uma relação preço-benefício atraente, apesar do DY baixo.

**Métricas**:
- PE=15.26
- ROE=9.8%
- Liquidez corrente=7.07

**Preocupações**:
- Relação dívida bruta/EBITDA negativa (-2.15)
- DY baixo de 46.2%

###### [[risk.drift-audit]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Berkshire Hathaway B mantém posição de valor com solidez financeira_

A Berkshire Hathaway B oferece uma relação preço-benefício atrativa (PE=15.26) e um ROE de 9.8%, indicando potencial de crescimento sustentável.

**Métricas**:
- Piotroski F-Score: 4/9
- Beneish M-Score: -2.42
- Liquidez corrente: 7.07

**Preocupações**:
- Relação dívida bruta/EBITDA negativa (-2.15)
- Dividend yield baixo (DY=46.2%)

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Berkshire Hathaway B mantém posição defensiva com PE razoável_

A Berkshire Hathaway B oferece uma relação preço-benefício atraente (PE de 15.26) e um ROE de 9.8%, além de baixa volatilidade (beta de 0.699), apoiando uma estratégia defensiva.

**Métricas**:
- P/E=15.26
- ROE=9.8%
- Beta=0.699

**Preocupações**:
- Dividend Yield baixo (46.2%)
- Relação dívida bruta/EBITDA negativa (-2.15)

##### Round 2 — Respostas (peers visíveis)

###### [[council.industrials-us]] — 🟢 **BUY**
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- A relação preço-benefício atrativa mantém-se como uma forte vantagem para BRK-B
- Mariana Macro

**Desafiou**:
- Relação dívida bruta/EBITDA negativa (-2.15) | DY baixo de 46.2%
- Concordo que a relação dívida bruta/EBITDA é preocupante, mas o Piotroski F-Score de 4/9 e Beneish M-Score de -2.42 indicam uma situação financeira estável.
- Mariana Macro
- Pedro Alocação

###### [[council.macro]] — 🟡 **HOLD**
_Chief Macro Strategist_

**Concordou com**:
- A Berkshire Hathaway B oferece uma relação preço-benefício atrativa (PE=15.26) e um ROE de 9.8%, indicando potencial de crescimento sustentável.
- Valentina Prudente

**Desafiou**:
- Dividend yield baixo de 46.2% | Dividend Yield baixo (46.2%)
- Charlie Compounder, Pedro Alocação e Valentina Prudente - O DY é um indicador relevante para investidores que buscam dividendos, mas não reflete a solidez financeira ou o potencial de crescimento da empresa

###### [[risk.drift-audit]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- A Berkshire Hathaway B oferece uma relação preço-benefício atrativa, com um P/E de 15.26 e um ROE sustentado de 9.8%. - Charlie Compounder

**Desafiou**:
- Dividend yield baixo de 46.2% | DY baixo de 46.2% - Mariana Macro & Pedro Alocação | O valor do dividendo não é o único indicador de valor para uma empresa como Berkshire Hathaway, que foca em crescimento e liquidez a longo prazo.

###### [[council.allocation]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- A Berkshire Hathaway B oferece uma relação preço-benefício atrativa, com um P/E de 15.26 e um ROE sustentado de 9.8%. - Charlie Compounder

**Desafiou**:
- Relação dívida bruta/EBITDA negativa (-2.15) | DY baixo de 46.2% - Mariana Macro | A relação dívida bruta/EBITDA negativa pode sugerir que a empresa está enfrentando desafios financeiros, mas é importante considerar o contexto geral da solidez financeira e liquidez corrente de 7.07.

##### Documentos relacionados

- [[BRK-B|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[BRK-B|Charlie Compounder]] em [[council.industrials-us]]/reviews/
  - [[BRK-B|Mariana Macro]] em [[council.macro]]/reviews/
  - [[BRK-B|Valentina Prudente]] em [[risk.drift-audit]]/reviews/
  - [[BRK-B|Pedro Alocação]] em [[council.allocation]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:BRK-B — Berkshire Hathaway B ===
Sector: Holding  |  Modo (auto): A  |  Held: True
Last price: 473.6000061035156 (2026-04-30)
Position: 1 shares @ entry 417.99
Fundamentals: P/E=15.26 | P/B=0.00 | ROE=9.8% | ND/EBITDA=-2.15 | DivStreak=0.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: A Berkshire Hathaway B é uma excelente posição de longo prazo para um investidor Buffett/Graham, oferecendo uma relação preço-benefício atrativa com um PE de 15.08 e um ROE de 9.81%. Apesar do dividendo não ser significativo (DY de 46.2%), a empresa mantém um alto índice de liquidez corrente de 7.07, indicando solidez financeira. A posição também beneficia-se da baixa volatilidade relativa ao mercado (beta de 0.699), contribuindo para uma estratégia defensiva.

**Key assumptions**:
1. O preço-benefício (PE) de 15.08 continuará a ser considerado razoável em comparação com o crescimento esperado da empresa.
2. A relação dívida bruta/EBITDA negativa (-2.15) indicará que a Berkshire Hathaway B continua gerindo sua posição de capital de forma eficaz, sem endividame

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 2.1%
  Sector weight: 2.1%

QUALITY SCORES:
  Piotroski F-Score: 4/9 (2025-12-31)
  Beneish M-Score: -2.42  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Watch the 2026 Berkshire Hathaway annual shareholders meeting on Saturday, May 2 - CNBC [Fri, 24 Ap]
    2026 Berkshire Hathaway Annual Shareholder Meeting. # Watch the 2026 Berkshire Hathaway annual shareholders meeting on Saturday, May 2. It's a new day in Omaha, Nebraska, as Greg Abel takes center stage at the 2026 Berkshire Hathaway annual
  - Exclusive | Greg Abel Has Been Leading Berkshire for 100 Days. Things Are Already Changing. - WSJ [Sat, 18 Ap]
    # Exclusive | Greg Abel Has Been Leading Berkshire Hathaway for 100 Days. Greg Abel Has Been Leading Berkshire for 100 Days. This copy is for your personal, non-commercial use only. For non-personal use or to order multiple copies, please c
  - CNBC to Exclusively Host Virtual Livestream of 2026 Berkshire Hathaway Annual Shareholders Meeting on May 2 - CNBC [Mon, 27 Ap]
    # CNBC to Exclusively Host Virtual Livestream of 2026 Berkshire Hathaway Annual Shareholders Meeting on May 2. **ENGLEWOOD CLIFFS, N.J., April 27, 2026 –** CNBC, First in Business Worldwide, will host the annual Berkshire Hathaway Sharehold
  - Berkshire Hathaway Q4 2025: Buffett’s Finale, Abel’s Debut - Forbes [Sun, 01 Ma]
    Berkshire Hathaway (BRK/A, BRK/B) reported fourth-quarter earnings of almost $19.2 billion, below the $19.7 billion in the same quarter of 2024, due to lower operating profits and an impairment of Berkshire’s Occidental Petroleum investment
  - Berkshire Hathaway’s Earnings Are Nearly Here. Greg Abel’s Letter Will Be Top of Mind for Investors. - Barron's [Sat, 28 Fe]
    This copy is for your personal, non-commercial use only. Distribution and use of this material are governed by our Subscriber Agreement and by copyright law. For non-personal use or to order multiple copies, please contact Dow Jones Reprint
  - Berkshire Hathaway reports drop in quarterly profit on insurance operations weakness - CNN [Sat, 28 Fe]
    Berkshire Vice Chairman Greg Abel speaks with shareholders during the Berkshire Hathaway Inc. annual shareholders' meeting, in Omaha, Nebraska, on May 2, 2025. Berkshire Hathaway (BRK.B), which wrapped up its final year under Warren Buffett

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (9 hits)
[1] sec (8-K) [2026-04-16]: 8-K | 8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312526159326/d903301d8k.htm
[2] sec (proxy) [2026-03-13]: DEF 14A
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312526106253/d882687ddef14a.htm
[3] sec (8-K) [2026-03-05]: 8-K | 8.01,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312526092557/d82599d8k.htm
[4] sec (10-K) [2026-03-02]: 10-K
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312526083899/brka-20251231.htm
[5] sec (8-K) [2026-03-02]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312526085801/d117283d8k.htm
[6] sec (8-K) [2025-12-11]: 8-K | 5.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1067983/000119312525314935/d10933d8k.htm

##### BIBLIOTHECA (livros/clippings RAG) (5 hits)
[7] Bibliotheca: investment_valuation_3rd_edition: ent is flawed because:
a.
 Value is determined by earnings and cash flows, and investor perceptions do not matter.
b.
 Perceptions do matter, but they can change. Value must be based on something more

substantial.
c.
 Investors are irrational. Therefore, their perceptions should not determine value
[8] Bibliotheca: investment_valuation_3rd_edition: icient markets are and how good the managers of the firm are at finding undervalued securities. In
unique cases, a firm may be more adept at finding good investments in financial markets than it is at

competing in product markets. Consider the case of Berkshire Hathaway, a firm that has been a
vehi
[9] Bibliotheca: investment_valuation_3rd_edition: ntegrated moving average (ARIMA) models
Avatek Corporation
Averages
Averaging, in beta calculation
Avonex
Balance sheets
accounting vs. financial
explanation of
BancorpSouth (BXS)
Bank of Hawaii (BOH)

Bankruptcy
costs of
overlevered firms and probability of
Barnes & Noble
Barra
Barrier options
Barr
[10] Bibliotheca: clip_berkshire_hathaway_inc_13f_filings: ## Berkshire Hathaway Inc

##### 13F Portfolio Filings

Most recent 13F

[Q4 2025](https://13f.info/13f/000119312526054580-berkshire-hathaway-inc-q4-2025)

Notable people

Warren Buffett

Location

Omaha, NE

CIK

0001067983

All SEC filings

[View on sec.gov](https://www.sec.gov/cgi-bin/browse-edgar?C
[11] Bibliotheca: clip_berkshire_hathaway_inc_13f_filings: 5012315002961-berkshire-hathaway-inc-q4-2014">Q4 2014</a></td><td>47</td><td>109,365,274</td><td>WFC, KO, AXP, IBM</td><td>13F-HR</td><td>2/17/2015</td><td>000095012315002961</td></tr></tbody></table>

Showing 1 to 50 of 55 entries

1 2 Next

Additional filings from Berkshire Hathaway Inc that have 

##### TAVILY NEWS (≤30d) (5 hits)
[12] Tavily [Fri, 24 Ap]: 2026 Berkshire Hathaway Annual Shareholder Meeting. # Watch the 2026 Berkshire Hathaway annual shareholders meeting on Saturday, May 2. It's a new day in Omaha, Nebraska, as Greg Abel takes center stage at the 2026 Berkshire Hathaway annual meeting. Iran foreign minister says no meeting is planned b
     URL: https://www.cnbc.com/video/2026/04/24/watch-the-2026-berkshire-hathaway-annual-shareholders-meeting-on-saturday-may-2.html
[13] Tavily [Sat, 18 Ap]: # Exclusive | Greg Abel Has Been Leading Berkshire Hathaway for 100 Days. Greg Abel Has Been Leading Berkshire for 100 Days. This copy is for your personal, non-commercial use only. For non-personal use or to order multiple copies, please contact Dow Jones Reprints at 1-800-843-0008 or visit www.djr
     URL: https://www.wsj.com/finance/berkshire-hathaway-ceo-greg-abel-first-100-days-a42fcf27
[14] Tavily [Mon, 27 Ap]: # CNBC to Exclusively Host Virtual Livestream of 2026 Berkshire Hathaway Annual Shareholders Meeting on May 2. **ENGLEWOOD CLIFFS, N.J., April 27, 2026 –** CNBC, First in Business Worldwide, will host the annual Berkshire Hathaway Shareholders Meeting taking place on Saturday, May 2. CNBC's livestre
     URL: https://www.cnbc.com/2026/04/27/cnbc-to-exclusively-host-virtual-livestream-of-2026-berkshire-hathaway-annual-shareholders-meeting-on-may-2.html
[15] Tavily [Sat, 25 Ap]: He will have a chance to do that in one week at the Berkshire shareholders meeting, live on CNBC.com. Apple CEO Tim Cook arrives for the 2024 Berkshire annual shareholders' meeting. Even though Berkshire's stake in Apple has been cut by 75% since the summer of 2023 through the end of this year's fir
     URL: https://www.cnbc.com/2026/04/25/berkshire-attracts-interest-as-it-slips-further-behind-the-sp-500.html
[16] Tavily [Sat, 18 Ap]: *(This is the Warren Buffett Watch newsletter, news and analysis on all things Warren Buffett and Berkshire Hathaway. On their own terms, Berkshire shares have not been performing well since they closed at record highs on May 2, 2025, just before Warren Buffett announced he would be stepping down as
     URL: https://www.cnbc.com/2026/04/18/berkshire-shares-left-behind-as-sp-500-rallies-to-record-high.html

##### TAVILY GUIDANCE (≤90d) (5 hits)
[17] Tavily [Sun, 01 Ma]: Berkshire Hathaway (BRK/A, BRK/B) reported fourth-quarter earnings of almost $19.2 billion, below the $19.7 billion in the same quarter of 2024, due to lower operating profits and an impairment of Berkshire’s Occident

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\BRK-B_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\BRK-B_STORY.md` (cemetery archive)_

#### Berkshire Hathaway B — BRK-B

##### Análise de Investimento · Modo FULL · Jurisdição US

*1 de Maio de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[council.industrials-us]] — _Industrials & Consumer US Specialist (Buffett frame)_
- [[council.macro]] — _Chief Macro Strategist_
- [[risk.drift-audit]] — _Chief Risk Officer_
- [[council.allocation]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/BRK-B_2026-05-01.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (6 hits) |
| **2 — Metric Engine** | Receita R$ 410.5 bi · EBITDA est. R$ 96.28 bi · FCF R$ 25.04 bi · ROE 10% · |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 4/9 · Beneish M=-2.42 (clean) |
| **5 — Classification** | Modo A-US · Value (6/12) |
| **5.5 — Council Debate** | BUY (high) · 2 dissent · 2 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. Berkshire Hathaway B (BRK-B) é uma empresa de holding que detém participações em diversas empresas, sendo um dos maiores conglomerados do mundo. Sua estratégia tem sido liderada por Warren Buffett durante décadas e agora está sob a direção de Greg Abel desde o início de 2026. A Berkshire Hathaway é conhecida por suas estratégias de investimento em longo prazo e sua capacidade de identificar oportunidades de valor no mercado financeiro, muitas vezes superando seu desempenho nos mercados de produtos.

A armadilha típica que os investidores podem cair ao falar sobre Berkshire Hathaway é confundir o valor das empresas detidas com a própria estratégia e capacidade operacional da empresa. Muitos analistas tendem a focar nas participações individuais, como Apple ou Geico, em vez de entender a visão estratégica global que Warren Buffett e agora Greg Abel aplicam ao conglomerado.

O posicionamento competitivo de Berkshire Hathaway é único no mercado financeiro por sua abordagem diversificada e conservadora. A empresa tem sido capaz de navegar através de diversos ciclos econômicos, mantendo-se como uma referência em termos de valorização a longo prazo e gestão de risco.

##### Ato 2 — O Contexto

O cenário macroeconómico atual apresenta um ambiente desafiador para muitas empresas. As taxas do Federal Reserve estão fixadas entre os 4,25% e 4,50%, enquanto a taxa dos títulos do Tesouro de dez anos está em torno dos 4,2%. O custo do capital próprio (Ke) é estimado em cerca de 10%, refletindo um ambiente onde o acesso ao crédito tornou-se mais caro. Em termos do ciclo económico, estamos no fim da expansão e no início de uma fase de acomodação.

Para o sector de holdings, como Berkshire Hathaway, este cenário apresenta tanto desafios quanto oportunidades. A elevada taxa de juros pode pressionar os preços das ações, especialmente para empresas que dependem fortemente do financiamento através da dívida. No entanto, também cria um ambiente propício para aquisições estratégicas e investimentos em ativos subavaliados.

Recentemente, Berkshire Hathaway tem enfrentado desafios específicos relacionados à sua exposição ao mercado de seguros, que é o maior contribuinte para suas receitas operacionais. A queda nas receitas do segmento de seguros no quarto trimestre de 2025 reflete a pressão sobre este setor em um ambiente macroeconomicamente desafiador.

Em termos regulatórios e estruturais, não há mudanças significativas mencionadas nos web facts que afetem diretamente Berkshire Hathaway. No entanto, o cenário geral de taxas elevadas e incerteza econômica continua a moldar as estratégias da empresa para os próximos trimestres.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa é um retrato de transformação e crescimento que se desdobra ao longo dos últimos anos. A tabela abaixo ilustra a trajetória financeira da companhia desde 2022 até as previsões para 2025, destacando os principais indicadores econômicos:

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 234.12B | R$ -26.15B | R$ -28.76B | -12.3% | R$ -22.76B | -9.7% | R$ 21.89B |
| 2023 | R$ 439.34B | R$ 125.17B | R$ 137.69B | 31.3% | R$ 96.22B | 21.9% | R$ 29.79B |
| 2024 | R$ 424.23B | R$ 115.58B | R$ 127.13B | 30.0% | R$ 89.00B | 21.0% | R$ 11.62B |
| 2025 | R$ 410.52B | R$ 87.53B | R$ 96.28B | 23.5% | R$ 66.97B | 16.3% | R$ 25.04B |

A receita da empresa registrou um crescimento significativo de 87,3% entre 2022 e 2023, seguido por uma ligeira contração em 2024 (-3.1%). Em 2025, a receita estabilizou-se, mantendo o mesmo nível do ano anterior.

A expansão da margem EBITDA é notável: após um prejuízo operacional de -12.3% em 2022, a empresa alcançou uma margem positiva de 31.3% em 2023 e manteve-se acima dos 20% nos anos seguintes. Este progresso reflete melhorias significativas na eficiência operacional.

O fluxo de caixa livre (FCF) da empresa também apresentou uma trajetória notável, passando de R$ 21.89B em 2022 para um pico de R$ 29.79B em 2023 e voltando a R$ 25.04B no último ano analisado. Este indicador é crucial para avaliar a capacidade da empresa de gerar caixa livre, o que é fundamental para sustentar investimentos futuros.

Em relação aos dividendos, não há um histórico disponível, o que implica que a empresa ainda está em uma fase de reinvestimento ou não tem uma política consistente de distribuição de lucros. Dado esse cenário, não é possível calcular um Dividend Growth Rate (DGR) significativo ou avaliar a tese DRIP (Dividend Reinvestment Plan).

É importante notar que o FCF fornece uma visão mais precisa da geração de caixa do que os lucros contábeis, pois pode esconder provisões e ajustes. O fluxo de caixa livre é um indicador crucial para avaliar a sustentabilidade financeira da empresa.

##### Ato 4 — O Balanço

O balanço da empresa no final de 2026 apresenta uma série de indicadores que permitem uma análise mais detalhada do seu desempenho e posição financeira. Com um preço atual de R$ 473.60, a relação P/E é de 15.26, sugerindo um valor relativamente acessível em comparação com os lucros da empresa.

A relação P/B (Price to Book Ratio) está ausente devido à falta de dados sobre o patrimônio líquido da empresa. O ROE (Return on Equity), no entanto, é de 9.81%, indicando que a empresa gera um retorno de quase 10% para cada real investido em capital próprio.

A relação Net Debt/EBITDA, calculada com base nos dados disponíveis, é de -2.15 (considerando o net debt estimado de R$ 64.54B e o EBITDA mais recente de R$ 96.28B). Este valor negativo sugere que a empresa tem um fluxo de caixa operacional robusto, capaz de cobrir suas obrigações financeiras.

O Current Ratio (relação entre ativos correntes e passivos correntes) não está disponível para análise direta, mas o FCF positivo indica uma posição líquida sólida. O ROE de 9.81% supera o custo do capital próprio (Ke) estimado em cerca de 18.25%, sugerindo que a empresa cria valor.

Não há sinais claros de despesas financeiras crescentes ou alavancagem excessiva no período analisado, o que é um ponto positivo para a sustentabilidade financeira da empresa. No entanto, a ausência de uma política consistente de dividendos pode ser vista como um possível ponto de atenção para investidores em busca de rendimentos regulares.

Em resumo, os indicadores sugerem que a empresa está bem posicionada financeiramente e tem potencial para continuar gerando valor para seus acionistas.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa em questão revela uma posição complexa no mercado. O preço-earnings (P/E) de 15,26 vezes é significativamente menor que a média do índice S&P, indicando potencialmente um desconto frente ao mercado geral. No entanto, o múltiplo price-to-book (P/B) está em zero, sugerindo que o valor contábil da empresa não é positivo ou pode estar sendo seriamente penalizado por fatores como endividamento elevado ou ativos depreciados.

O retorno sobre o patrimônio líquido (ROE) de 9,81% é inferior à média setorial e do índice S&P, que registra cerca de 16%. Este indicador sugere uma eficiência operacional menor em relação ao capital próprio investido. O múltiplo net-debt-to-EBITDA (ND/EBITDA) de -2,15 vezes indica um endividamento líquido negativo ou que a empresa tem mais recursos financeiros do que compromissos de dívida, o que é incomum e pode ser interpretado como uma posição financeira particularmente forte ou como resultado de práticas contábeis específicas.

O fluxo de caixa livre (FCF) yield de 2,5% indica um retorno sobre a capitalização da empresa relativamente baixo em comparação com o índice S&P, que registra cerca de 4%. Este indicador sugere que a geração de caixa está abaixo do esperado para uma companhia de seu porte e setor.

A tabela comparativa detalha estes múltiplos:

| Múltiplo | BRK-B | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 15.26x | — | 21.00x |
| P/B | 0.00x | — | 3.50x |
| DY | — | — | 1.5% |
| FCF Yield | 2.5% | — | 4.0% |
| ROE | 9.8% | — | 16.0% |
| ND/EBITDA | -2.15x | — | — |

É importante notar que a falta de dados comparáveis para peers específicos levou à utilização da mediana setorial como referência, o que pode limitar a precisão das comparações.

##### Ato 6 — Os Quality Scores

A análise dos scores de qualidade financeira revela uma posição mista. O Piotroski F-Score de 4/9 indica um desempenho moderado na manutenção da solidez financeira e operacional da empresa, com quatro critérios aprovados em nove possíveis. Isso sugere que enquanto a empresa mantém certa estabilidade financeira, há áreas onde o desempenho é menos robusto.

O Beneish M-Score de -2,42 coloca a empresa na zona "clean", indicando um baixo risco de manipulação contábil. Esta classificação é apoiada por uma alta confiança no resultado, sugerindo que os números apresentados são provavelmente precisos e não distorcidos.

No entanto, dados específicos sobre o Altman Z-Score (conservador ou ajustado) para a empresa BRK-B não foram fornecidos, limitando nossa capacidade de avaliar o risco de insolvência com base nesse indicador. Em geral, os scores sugerem que enquanto há certas preocupações financeiras, a empresa parece estar em uma posição sólida e confiável no momento.

A análise destes indicadores é crucial para entender não apenas as métricas financeiras da empresa, mas também o contexto operacional e estratégico por trás desses números.

---

##### Ato 7 — O Moat e a Gestão

A Berkshire Hathaway, sob a liderança de Greg Abel desde o início de 2026, tem demonstrado sinais claros de uma estratégia sólida e um moat robusto. Com mais de cem dias à frente da empresa, Abel já implementou mudanças significativas que indicam sua determinação em manter a posição competitiva da Berkshire no mercado.

###### Moat

A classificação do moat da Berkshire Hathaway é amplamente considerada como "Wide". Esta avaliação baseia-se principalmente nos seguintes aspectos:

1. **Custo/Escala**: A empresa possui uma vasta gama de negócios, desde seguros até energia e manufatura, o que lhe permite beneficiar de economias de escala em várias frentes.
2. **Switching Costs**: Os clientes de longo prazo da Berkshire, especialmente os segurados corporativos e individuais, enfrentam altos custos para mudar de fornecedor, uma vez que a empresa oferece serviços personalizados e confiáveis.
3. **Intangíveis**: A marca Berkshire Hathaway é um ativo intangível significativo, reconhecida pela sua estabilidade financeira e capacidade de gerir riscos complexos.
4. **Eficiência Operacional**: Sob a gestão de Greg Abel, a empresa tem demonstrado uma eficácia crescente em otimizar seus negócios, reduzindo custos e aumentando a produtividade.

###### Gestão

A transição para o novo CEO, Greg Abel, foi suave e já mostrou resultados tangíveis. O evento mais notável é o anúncio de que o próximo encontro anual dos acionistas será transmitido virtualmente pela CNBC em 2 de maio de 2026, marcando uma nova era para a empresa.

###### Insider Ownership

Dado não disponível.

###### Insider Trades

Dado não disponível.

##### Ato 8 — O Veredito

###### Perfil Filosófico

A Berkshire Hathaway exibe um perfil filosófico de Value (6/12), com ênfase no valor e na estabilidade financeira. As pontuações específicas incluem:

- **Value**: +2 por P/E abaixo da média setorial, +2 por P/B baixo e +2 pela margem de segurança do DCF.
- **Buffett**: +1 por ND/EBITDA negativo, +1 pelo M-Score Beneish indicando ausência de manipulação financeira e +1 pela margem de segurança do DCF.

###### O que o preço desconta

O preço atual da Berkshire Hathaway reflete a transição bem-sucedida para uma nova liderança e a consolidação dos negócios existentes. A empresa é valorizada por sua capacidade de gerir riscos e manter lucratividade em diferentes setores.

###### O que os fundamentos sugerem

Os fundamentos da Berkshire Hathaway indicam um negócio resiliente, com uma estrutura financeira sólida apesar dos desafios recentes. A relação dívida bruta/EBITDA negativa é preocupante, mas não reflete a solidez geral da empresa.

###### DCF — A âncora do valor

| Cenário | Crescimento 5y | Perpetuidade | Valor por ação |
|---|---|---|---|
| Pessimista | 5% a.a. | 3% | R$ 278914.83 |
| **Base** | **8% a.a.** | **4%** | **R$ 357770.64** |
| Optimista | 11% a.a. | 5% | R$ 472034.45 |

###### Margem de segurança

A margem de segurança da Berkshire Hathaway, calculada com base no DCF, é de +75443%.

###### Rating final

RATING: Buy

###### Pre-Mortem — Se esta tese falhar

Foi este o ponto onde Mariana Macro divergiu de Diego Bancário: a baixa taxa de dividendos (DY) de 46.2% pode ser um indicador relevante para investidores que buscam rendimentos regulares. Além disso, Valentina Prudente sinalizou que a relação dívida bruta/EBITDA negativa (-2.15) pode sugerir desafios financeiros no curto prazo.

###### Horizonte

O horizonte de investimento para Berkshire Hathaway é de 24-36 meses, com expectativas de continuidade na implementação da estratégia sob a liderança de Greg Abel.

###### Nota divergente do Council

Foi este o ponto onde Mariana Macro divergiu de Diego Bancário: "A baixa taxa de dividendos (DY) é um indicador relevante para investidores que buscam rendimentos regulares, e deve ser considerado ao tomar decisões de investimento."

---

##### Evidence Ledger — fontes de cada métrica e claim

> 19 entradas · 15 com URL · confiança: {'reported': 9, 'computed': 3, 'extracted': 7}

| # | Claim | Valor | Fonte | URL | Confiança | Fetched |
|---|---|---|---|---|---|---|
| [1] | P/E ratio (TTM) | 15.26x | yfinance Ticker.info → fundamentals table | [link](https://finance.yahoo.com/quote/BRK-B) | `reported

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\BRK-B_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\BRK-B_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — BRK-B           moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              1
  Entry price.........: US$      417.99
  Cost basis..........: US$      417.99
  Price now...........: US$      469.32
  Market value now....: US$      469.32  [+12.3% nao-realizado]
  DY t12m.............: 0.00%  (R$/US$ 0.0000/share)

  kind=equity  streak=0  price_cagr_5y=0.114

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +0.00%  |   +5.70% |   +5.70%       |
  | base         |   +0.00%  |  +11.40% |  +11.40%       |
  | optimista    |   +0.00%  |  +14.82% |  +14.82%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |    >40       |      >40       |       11       |
  | base         |    >40       |      >40       |        6       |
  | optimista    |    >40       |      >40       |        5       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$        619 | US$        805 | US$        937 |
  |  10y  | US$        817 | US$      1,381 | US$      1,869 |
  |  15y  | US$      1,078 | US$      2,370 | US$      3,730 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\BRK-B.md` (cemetery archive)_

#### BRK-B — Berkshire Hathaway B

#holding #us #holding

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 4.2/10  |  **Confiança**: 60%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 3.7/10 | 35% | `████░░░░░░` |
| Valuation  | 5.0/10 | 30% | `█████░░░░░` |
| Momentum   | 4.0/10 | 20% | `████░░░░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski 4/9 (NEUTRAL), DivSafety 53.8/100
- **Valuation**: Screen 0.50, DY percentil - (-)
- **Momentum**: 1d 0.93%, 30d -3.17%, YTD -5.44%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- total 4.2 na zona neutra
- quality frágil

##### Links

- Sector: [[sectors/Holding|Holding]]
- Market: [[markets/US|US]]
- 🎯 **Thesis**: [[BRK-B|thesis deep]]

##### Snapshot

- **Preço**: $469.83  (2026-05-06)    _+0.93% 1d_
- **Screen**: 0.5  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: 4/9
- **Div Safety**: 53.8/100 (RISK)
- **Posição**: 1.0 sh @ $417.99  →  P&L 12.4%

##### Fundamentals

- P/E: 13.978874 | P/B: 0.00094217935 | DY: None%
- ROE: 10.5% | EPS: 33.61 | BVPS: 498663.0
- Streak div: 0y | Aristocrat: False

##### Eventos (SEC/CVM)

- **2026-05-07** `8-K` — 8-K | 2.02,5.02,5.03,5.07,9.01
- **2026-05-04** `10-Q` — 10-Q
- **2026-04-16** `8-K` — 8-K | 8.01,9.01
- **2026-03-13** `proxy` — DEF 14A
- **2026-03-05** `8-K` — 8-K | 8.01,9.01

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Fernando Ulrich | balance_sheet | 1.00 | A Berkshire Hathaway possui quase 400 bilhões em caixa. |
| 2026-05-11 | Fernando Ulrich | thesis_bull | 0.80 | A Berkshire Hathaway está posicionada para aproveitar oportunidades assimétricas em cenários de incerteza. |
| 2026-05-11 | Fernando Ulrich | operational | 0.70 | A Berkshire Hathaway pode enfrentar desafios em investir simultaneamente em CAPEX e buybacks devido à falta de dinheiro. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -9.34%
- **Drawdown 5y**: -12.96%
- **YTD**: -5.44%
- **YoY (1y)**: -8.30%
- **CAGR 3y**: +13.20%  |  **5y**: +10.06%  |  **10y**: +12.50%
- **Vol annual**: +17.83%
- **Sharpe 3y** (rf=4%): +0.58

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: none
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $234.12B | $-22.76B | $21.89B |
| 2023-12-31 | $439.34B | $96.22B | $29.79B |
| 2024-12-31 | $424.23B | $89.00B | $11.62B |
| 2025-12-31 | $410.52B | $66.97B | $25.04B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "BRK-B — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: BRK-B
    data: [513.25, 503.4, 508.74, 509.16, 502.81, 493.53, 490.34, 485.14, 486.21, 489.61, 477.47, 476.31, 473.8, 480.6, 476.0, 464.19, 464.73, 477.2, 488.59, 495.72, 501.49, 492.72, 491.54, 492.85, 494.96, 498.2, 502.3, 491.93, 492.42, 490.16, 475.76, 487.66, 496.98, 508.94, 501.12, 511.23, 503.6, 491.43, 506.38, 494.53, 498.3, 496.85, 499.77, 493.15, 483.83, 474.67, 487.29, 508.09, 500.01, 496.94, 493.99, 481.36, 497.2, 490.03, 481.48, 476.19, 479.2, 478.08, 480.19, 474.58, 470.55, 478.16, 468.52]
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
    data: [15.316526, 15.228342, 15.311633, 15.289303, 15.2348585, 15.083709, 15.11011, 15.129594, 15.129594, 15.242102, 15.39472, 15.320013, 15.257731, 15.098936, 13.858886, 13.978874]
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
    data: [9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 9.81, 10.5, 10.5, 10.5]
  - title: DY %
    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\BRK-B_DOSSIE.md` (cemetery archive)_

#### 📑 BRK-B — Berkshire Hathaway B

> Generated **2026-04-26** by `ii dossier BRK-B`. Cross-links: [[BRK-B]] · [[BRK-B]] · [[CONSTITUTION]]

##### TL;DR

BRK-B negoceia a P/E 15.13 com market cap USD 1.01T e ROE modesto 9.81%, reflexo do cash-drag estrutural (>USD 300B em treasuries) e da ausência de dividendo por desenho Buffett. IC verdict **HOLD** (high confidence, 100% consensus) — compounder defensivo com beta 0.7 mas YoY -11.6% sinaliza descompressão pós-Buffett (sucessão Greg Abel). Posição growth/holding pura: NÃO aplicar scorecard DRIP — não há dividendo para reinvestir e a tese é compounding via book value retido.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 31.02  |  **BVPS**: 498663.00
- **ROE**: 9.81%  |  **P/E**: 15.13  |  **P/B**: 0.00
- **DY**: n/a  |  **Streak div**: n/ay  |  **Market cap**: USD 1012.26B
- **Last price**: USD 469.32 (2026-04-26)  |  **YoY**: -11.6%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 100.0% consensus)

→ Detalhe: [[BRK-B]]

##### 3. Thesis

**Core thesis (2026-04-24)**: A Berkshire Hathaway B é uma excelente posição de longo prazo para um investidor Buffett/Graham, oferecendo uma relação preço-benefício atrativa com um PE de 15.08 e um ROE de 9.81%. Apesar do dividendo não ser significativo (DY de 46.2%), a empresa mantém um alto índice de liquidez corrente de 7.07, indicando solidez financeira. A posição também beneficia-se da baixa volatilidade relativa ao mercado (beta de 0.699), contribuindo para uma estratégia defensiva.

**Key assumptions**:
1. O preço-benefício (PE) de 15.08 continuará a ser considerado razoável em comparação com o crescimento esperado da empresa.
2. A relação dívida bruta/EBITDA negativa (-2.15) indicará que a Berkshire Hathaway B continua gerindo sua posição de capital de forma eficaz, sem endividame

→ Vault: [[BRK-B]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 15.13** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 15.13** passa.
- **P/B = 0.00** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **0.00** OK.
- **ROE = 9.81%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **9.81%** abaixo do critério.
- **Graham Number ≈ R$ 18655.88** vs preço **R$ 469.32** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🔴 **Sucessão Buffett/Munger** — transição executiva para Greg Abel + Ajit Jain; risco de re-rating se mercado perceber perda do "Buffett premium". Trigger: `events` com kind='8-K' e summary contendo 'CEO' ou 'leadership transition'.
- 🟡 **Cash drag estrutural** — pilha de USD 300B+ em treasuries diluindo ROE para 9.81% (abaixo do screen US 15%). Trigger: `fundamentals.roe < 8%` por 2 trimestres consecutivos.
- 🟡 **Concentração Apple** — equity portfolio com >40% em AAPL; correlação não-trivial com tech. Trigger: 13F filing mostrando AAPL >35% do equity book.
- 🟢 **Sem dividendo by design** — não é risco em si mas remove qualquer pretensão de DRIP; alinhar expectativas. Trigger: n/a (política conhecida).

##### 5. Position sizing

**Status atual**: holding (in portfolio)

**HOLD** — posição growth/compounder dentro do bucket US (USD permanece em US, regra de isolation). Não usar para deploy de cash destinado a DRIP — sem dividendo. Sizing prudente até 6-8% do US book; aumentar apenas em drawdowns >15% vs all-time high (margem de segurança Buffett-style sobre o próprio Buffett).

##### 6. Tracking triggers (auto-monitoring)

- `fundamentals.pe > 22` por 2 trimestres → premium injustificado vs hist 15-18.
- `fundamentals.roe < 8%` → cash drag a corroer compounding.
- `events.kind = '8-K'` com 'leadership' / 'succession' → news driver imediato.
- `prices.close` drawdown > 20% vs ATH → janela de aumento (Buffett-style on Buffett).
- `conviction_scores.score < 60` → tese a degradar; reavaliar.

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
*Generated by `ii dossier BRK-B` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Fernando Ulrich | balance_sheet | 1.00 | A Berkshire Hathaway possui quase 400 bilhões em caixa. |
| 2026-05-11 | Fernando Ulrich | thesis_bull | 0.80 | A Berkshire Hathaway está posicionada para aproveitar oportunidades assimétricas em cenários de incerteza. |
| 2026-05-11 | Fernando Ulrich | operational | 0.70 | A Berkshire Hathaway pode enfrentar desafios em investir simultaneamente em CAPEX e buybacks devido à falta de dinheiro. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\BRK-B_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — BRK-B

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=1 | HOLD=3 | AVOID=1  
**Avg conviction majority**: 5.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE abaixo de expectativa
- Baixo payout ratio
- Liquidez e solidez financeira

**Key risk**: Possível subavaliação do crescimento futuro das operações

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE razoável
- ROE sólido
- baixa volatilidade

**Key risk**: Dependência de Warren Buffett e Greg Abel; mudança na gestão pode afetar a governança corporativa.

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- Baixo PE e PB sugerem valorização
- Liquidez corrente alta indica solidez financeira
- Gestão eficiente da dívida

**Key risk**: Volatilidade do mercado de seguros e exposição a ativos intangíveis

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: none)

**Rationale**:
- Preço-benefício não oferece desconto significativo
- Margem de segurança insuficiente (<30%)
- Complexidade e tamanho da empresa

**Key risk**: Risco de subavaliação do valor intrínseco devido à complexidade

###### 🟡 Ray Dalio — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- PE razoável
- ROE sólido
- Baixa volatilidade

**Key risk**: Endividamento negativo pode ser temporário, mas monitorar é crucial

##### 📊 Context provided

```
TICKER: US:BRK-B

FUNDAMENTALS LATEST:
  pe: 14.169098
  pb: 0.0009414126
  roe: 10.50%
  net_debt_ebitda: -2.2753212908071867
  intangible_pct_assets: 9.6%   (goodwill $83.1B + intangibles $33.8B)

THESIS HEALTH: score=-1/100  contradictions=0  risk_flags=0  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: A Berkshire Hathaway B é uma excelente posição de longo prazo para um investidor Buffett/Graham, oferecendo uma relação preço-benefício atrativa com um PE de 15.08 e um ROE de 9.81%. Apesar do dividendo não ser significativo (DY de 46.2%), a empresa mantém um alto índice de liquidez corrente de 7.07, indicando solidez financeira. A posição também beneficia-se da baixa volatilidade relativa ao mercado (beta de 0.699), contribuindo para uma estratégia defensiva.

**Key assumptions**:
1. O preço-benefício (PE) de 15.08 continuará a ser considerado razoável em comparação com o crescimento esperado da empresa.
2. A relação dívida bruta/EBITDA negativa (-2.15) indicará que a Berkshire Hathaway B continua gerindo sua posição de capital de forma eficaz, sem endividame

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Berkshire Profits More Than Double on Gains in Insurance, Railroad, Energy Businesses - WSJ [Sat, 02 Ma]
    Image 1: President and CEO Greg Abel greets shareholders in front of a red "Pilot" truck with cardboard cutouts of Warren Buffett and Charlie Munger in the windshield. Berkshire Hathaway’sBRK.B-0.12%d
  - Berkshire Hathaway Q1 Earnings & Revenues Increase Year Over Year - TradingView [Mon, 04 Ma]
    # Berkshire Hathaway Q1 Earnings & Revenues Increase Year Over Year. **Berkshire Hathaway Inc.** BRK.B delivered first-quarter 2026 operating earnings of $11.3 billion, which increased 17.7% year over
  - Warren Buffett says it's important to know which deals not to take (BRK.B:NYSE) - Seeking Alpha [Sat, 02 Ma]
    Entering text into the input field will update the search result below. Entering text into the input field will update the search r
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Fernando Ulrich | balance_sheet | 1.00 | A Berkshire Hathaway possui quase 400 bilhões em caixa. |
| 2026-05-11 | Fernando Ulrich | thesis_bull | 0.80 | A Berkshire Hathaway está posicionada para aproveitar oportunidades assimétricas em cenários de incerteza. |
| 2026-05-11 | Fernando Ulrich | operational | 0.70 | A Berkshire Hathaway pode enfrentar desafios em investir simultaneamente em CAPEX e buybacks devido à falta de dinheiro. |

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\BRK-B_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — BRK-B

**Our stance**: bullish  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `medium_variance_long` (magnitude 2/5)  
**Interpretation**: moderate edge

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: neutral (1 bull / 1 bear / 3 neutral)  
**Cached**: True

- 🟢 [bull] [Here are Thursday's biggest analyst calls: Nvidia, Tesla, Berkshire Hathaway, Amazon, Texas Instruments & more - CNBC](https://www.cnbc.com/2026/04/23/thursday-analyst-calls-with-stocks-like-nvidia.html) (Thu, 23 Ap)
- 🟡 [neutral] [Berkshire Hathaway Q1 Earnings & Revenues Increase Year Over Year - TradingView](https://www.tradingview.com/news/zacks:e70b463c3094b:0-berkshire-hathaway-q1-earnings-revenues-increase-year-over-year/) (Mon, 04 Ma)
- 🔴 [bear] [Comcast Stock (CMCSA) Drops on Post Q1 Analyst Updates - TipRanks](https://www.tipranks.com/news/cmcsa-analysts) (Sat, 25 Ap)
- 🟡 [neutral] [Berkshire shares trade higher as Buffett successor Abel scores good marks at meeting, earnings jump - CNBC](https://www.cnbc.com/2026/05/04/berkshire-shares-trade-higher-as-buffett-successor-abel-scores-good-marks-at-meeting-earnings-jump.html) (Mon, 04 Ma)
- 🟡 [neutral] [Investment firm Telsey Advisory Group announced that it has downgraded Vital Farms, Inc.'s stock rating from "Outperform](https://www.bitget.com/asia/amp/news/detail/12560605403062) (Fri, 08 Ma)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: A Berkshire Hathaway B é uma excelente posição de longo prazo para um investidor Buffett/Graham, oferecendo uma relação preço-benefício atrativa com um PE de 15.08 e um ROE de 9.81%. Apesar do dividendo não ser significativo (DY de 46.2%), a empresa mantém um alto índice de liquidez corrente de 7.07, indicando solidez financeira. A posição também beneficia-se da baixa volatilidade relativa ao mercado (beta de 0.699), contribuindo para uma estratégia defensiva.

**Key assumptions**:
1. O preço-benefício (PE) de 15.08 continuará a ser considerado razoável em comparação com o crescimento esperado da empresa.
2. A relação dívida bruta/EBITDA negativa (-2.15) indicará que a Berkshire Hathaway B continua gerindo sua posição de capital de forma eficaz, sem endividame

---
*100% Ollama local. Variant perception scan.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=0 · themes=0_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Fernando Ulrich | balance_sheet | 1.00 | A Berkshire Hathaway possui quase 400 bilhões em caixa. |
| 2026-05-11 | Fernando Ulrich | thesis_bull | 0.80 | A Berkshire Hathaway está posicionada para aproveitar oportunidades assimétricas em cenários de incerteza. |
| 2026-05-11 | Fernando Ulrich | operational | 0.70 | A Berkshire Hathaway pode enfrentar desafios em investir simultaneamente em CAPEX e buybacks devido à falta de dinheiro. |

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\BRK-B.md` (cemetery archive)_

#### 🎯 Thesis: [[BRK-B]] — Berkshire Hathaway Class B

> Warren Buffett + Greg Abel (heir apparent) + $300B+ cash pile + wholly-owned operating businesses + $300B+ public equity portfolio. Core compounder position US.

##### Intent
**Compounder** — no dividend (Berkshire famously doesn't pay), pure reinvestment via book value growth + buybacks.

##### Business snapshot

Structure:
- **Insurance** (GEICO, Gen Re, BHRG, Alleghany) — float $170B+, no-cost leverage
- **Railroads** (BNSF) — largest US freight
- **Energy** (BHE — utilities + renewables)
- **Manufacturing** (Precision Castparts, Lubrizol, Marmon, etc)
- **Services + retail** (See's Candy, Nebraska Furniture Mart, Pampered Chef, Dairy Queen)
- **Investment portfolio**: AAPL $120B+, BAC, AXP, KO, CVX, OXY, KHC, etc ($300B+ total)
- **Cash + short-term Treasury**: $300B+ (historic high, waiting for bargains)

Market cap ~$900B+ (2026).

##### Por que detemos

1. **Quality proxy** — diversified across economies, sectors, risk factors.
2. **Buffett + Munger (RIP 2023) + Abel** — disciplined capital allocators.
3. **Float-leveraged** — $170B insurance float = negative-cost capital for investments.
4. **Buyback program** — disciplined below IV.
5. **Recession-resilient** — cash buffer absurd (300B).
6. **AAA-like balance sheet** — credit rating trumps many governments.

##### Moat

- **Capital allocation culture** — unique institutional memory.
- **Reputation premium** — distressed sellers prefer Berkshire (rep for not meddling).
- **Scale of capital** — only 3-4 entities globally can write $20B+ M&A cheque instantly.
- **Insurance underwriting discipline** — multi-decade track record.

##### Current state (2026-04)

- Cash pile $300B+ — either Buffett sees no bargains OR preparing mega-deal.
- Apple position trimmed 2024 (65% cut) — capital deployment path open.
- Energy (BHE) growing (renewables capex).
- BNSF solid freight volumes.
- Post-Munger governance transition smooth (Abel + Jain running operations day-to-day).

##### Invalidation triggers

- [ ] Buffett health crisis severe + Abel transition rocky (succession uncertainty priced but still risk)
- [ ] Major catastrophic insurance event ($50B+ write-down single event)
- [ ] Book value growth < 5%/y 3 years consecutive (compound breaking)
- [ ] Major capital mis-allocation (post-Buffett era)
- [ ] Cash pile deployment into quasi-dilutive mega-deal (unlikely given discipline)

##### Sizing

- Posição actual: 1 share (price ~$450+, so decent dollar value)
- Target 3-5% sleeve US
- **Buy-and-die candidate**

##### Why BRK vs other holdco / asset managers

| Holding type | Example | Profile |
|---|---|---|
| **Classic holdco** | BRK-B, BN | Capital allocator focus |
| **Asset manager** | BLK, TROW | Fee-based |
| **PE manager** | BX, KKR | Fund-cycle driven |
| **Wealth manager** | MS (post-Smith Barney) | Advisory fees |

BRK unique combo: holdco + insurance float + stock portfolio + operating businesses. No peer exact.


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -12.55%
- **Drawdown 5y**: -12.55%
- **YTD**: -4.99%
- **YoY (1y)**: -10.40%
- **CAGR 3y**: +13.13%  |  **5y**: +11.66%  |  **10y**: +12.44%
- **Vol annual**: +17.92%
- **Sharpe 3y** (rf=4%): +0.58

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: none
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Buffett_quality]] — the framework named after BRK's approach
- [[Moat_types]] — BRK portfolio é moat-curated
- [[BN]] — similar holdco model (Brookfield)
- [[KO]] / [[AAPL]] — BRK major holdings (we own directly + via BRK)

## ⚙️ Refresh commands

```bash
ii panorama BRK-B --write
ii deepdive BRK-B --save-obsidian
ii verdict BRK-B --narrate --write
ii fv BRK-B
python -m analytics.fair_value_forward --ticker BRK-B
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
