---
type: ticker_hub
ticker: TFC
market: us
sector: Financials
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 5
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# TFC — Truist Financial

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: US` · `currency: USD` · `bucket: holdings` · `5 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `HOLD` (score 5.67, 2026-05-09)
- **Fundamentals** (2026-05-13): P/E 11.52 · P/B 0.97 · DY 4.5% · ROE 8.6% · Dividend streak 40 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\TFC.md` (cemetery archive)_

#### TFC — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ir.truist.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **117**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=47.970001220703125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.08579001 · DY=0.0433604325009336 · P/E=11.873763
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.02,5.07,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-17 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-16 | proxy | sec | DEF 14A |

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


### 2020

#### 2020-05-27 · Filing 2020-05-27
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TFC_FILING_2020-05-27.md` (cemetery archive)_

#### Filing dossier — [[TFC]] · 2020-05-27

**Trigger**: `sec:8-K` no dia `2020-05-27`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/92230/000119312520153120/d863084d8k.htm>

##### 🎯 Acção sugerida

###### 🟢 **BUY** &mdash; preço 49.11

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `63.02` |
| HOLD entre | `63.02` — `80.80` (consensus) |
| TRIM entre | `80.80` — `92.92` |
| **SELL acima de** | `92.92` |

_Método: `buffett_ceiling`. Consensus fair = R$80.80. Our fair (mais conservador) = R$63.02._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 80.80 | 63.02 | 49.11 | BUY | single_source | `filing:sec:8-K:2020-05-27` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TFC.md` (cemetery archive)_

#### TFC — Truist Financial

#holding #us #financials

##### 🎯 Verdict — 🟡 WATCH

> **Score**: 6.2/10  |  **Confiança**: 50%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 5.3/10 | 35% | `█████░░░░░` |
| Valuation  | 8.0/10 | 30% | `████████░░` |
| Momentum   | 6.7/10 | 20% | `███████░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski None/9 (N/A), DivSafety 75.0/100
- **Valuation**: Screen 0.80, DY percentil P31 (fair-rich)
- **Momentum**: 1d 1.7%, 30d 3.06%, YTD 2.13%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- valuation atractiva mas quality ou momentum fraco
- valuation barato

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/US|US]]
- Peers: [[BLK]] · [[BN]] · [[GS]] · [[JPM]] · [[NU]]

##### Snapshot

- **Preço**: $50.80  (2026-05-06)    _+1.70% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 75.0/100 (WATCH)

##### Fundamentals

- P/E: 12.574257 | P/B: 1.0640526 | DY: 4.09%
- ROE: 8.58% | EPS: 4.04 | BVPS: 47.742
- Streak div: 40y | Aristocrat: True

##### Dividendos recentes

- 2026-02-13: $0.5200
- 2025-11-14: $0.5200
- 2025-08-08: $0.5200
- 2025-05-09: $0.5200
- 2025-02-14: $0.5200

##### Eventos (SEC/CVM)

- **2026-05-01** `8-K` — 8-K | 5.02,5.07,9.01
- **2026-05-01** `10-Q` — 10-Q
- **2026-04-23** `8-K` — 8-K | 8.01,9.01
- **2026-04-17** `8-K` — 8-K | 2.02,9.01
- **2026-03-16** `proxy` — DEF 14A

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -8.98%
- **Drawdown 5y**: -24.64%
- **YTD**: +2.13%
- **YoY (1y)**: +30.36%
- **CAGR 3y**: +20.98%  |  **5y**: -3.77%  |  **10y**: +4.09%
- **Vol annual**: +28.27%
- **Sharpe 3y** (rf=4%): +0.51

###### Dividendos
- **DY 5y avg**: +4.50%
- **Div CAGR 5y**: +2.83%
- **Frequency**: quarterly
- **Streak** (sem cortes): 11 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | $19.97B | $6.26B | $11.08B |
| 2023-12-31 | $20.02B | $-1.09B | $8.63B |
| 2024-12-31 | $13.28B | $4.82B | $2.16B |
| 2025-12-31 | $20.32B | $5.31B | $5.74B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "TFC — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: TFC
    data: [39.56, 41.23, 40.68, 40.03, 39.23, 40.66, 39.94, 39.81, 41.4, 44.2, 45.4, 45.67, 44.25, 45.48, 44.26, 43.42, 42.83, 44.42, 44.07, 46.78, 46.41, 45.29, 44.78, 45.99, 45.74, 45.57, 45.2, 42.95, 42.6, 43.61, 43.91, 43.73, 45.12, 44.86, 44.4, 46.24, 47.42, 47.92, 49.74, 50.08, 50.61, 49.74, 50.95, 49.83, 50.02, 50.89, 52.66, 55.81, 52.07, 51.78, 50.57, 49.3, 46.75, 43.83, 43.88, 45.39, 45.97, 47.83, 50.01, 50.57, 51.4, 50.65, 49.95]
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
    data: [13.060158, 12.929319, 12.939791, 13.23822, 13.2421465, 12.641089, 12.556931, 12.556931, 12.556931, 12.680693, 12.660892, 12.537129, 12.747525, 12.247525, 12.363862, 12.574257]
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
    data: [8.24, 8.24, 8.24, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58, 8.58]
  - title: DY %
    data: [4.2, 4.19, 4.21, 4.11, 4.11, 4.07, 4.1, 4.1, 4.1, 4.06, 4.07, 4.11, 4.04, 4.2, 4.16, 4.09]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TFC_DOSSIE.md` (cemetery archive)_

#### 📑 TFC — Truist Financial

> Generated **2026-04-26** by `ii dossier TFC`. Cross-links: [[TFC]] · _(no IC yet)_ · [[CONSTITUTION]]

##### TL;DR

TFC negoceia P/E 12.56, P/B 1.06, DY 4.10% e ROE 8.58% com streak dividendos 40y — regional bank southeast US, trading próximo do book. IC ainda não gerado (correr `python -m agents.synthetic_ic TFC`); YoY +33.9% reflecte recovery do banking sector pós sell-off SVB 2023. DRIP candidate forte: DY 4.10% + 40y streak qualificam screen US, manter para reinvestimento atento à NIM e qualidade de crédito.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 4.04  |  **BVPS**: 47.74
- **ROE**: 8.58%  |  **P/E**: 12.56  |  **P/B**: 1.06
- **DY**: 4.10%  |  **Streak div**: 40y  |  **Market cap**: USD 63.20B
- **Last price**: USD 50.73 (2026-04-24)  |  **YoY**: +33.9%

##### 2. Synthetic IC

_(IC ainda não gerado para TFC. Execute `python -m agents.synthetic_ic TFC` para popular antes do dossier ser refinado.)_

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 12.56** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 12.56** passa.
- **P/B = 1.06** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **1.06** OK.
- **DY = 4.10%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **4.10%** OK.
- **ROE = 8.58%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **8.58%** abaixo do critério.
- **Graham Number ≈ R$ 65.88** vs preço **R$ 50.73** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 40y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

###### Conceitos relacionados

- 💰 **Status DRIP-friendly** (US holding com DY ≥ 2.5%) — ver [[Glossary/DRIP]] para mecanismo + [[Glossary/Aristocrat]] para membership formal.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 3. Riscos identificados

- 🔴 **Credit quality regional bank** — exposure CRE / commercial loans southeast US; NPL spike afecta materialmente. Trigger: NPL ratio > 1.2% ou charge-offs YoY > +25%.
- 🔴 **NIM compression** — Fed corte rápido pode comprimir NIM antes de re-pricing dos depósitos. Trigger: NIM < 2.7% por 2 trimestres.
- 🟡 **CRE office concentration** — exposição a commercial RE office em metros US; writedowns continuam. Trigger: CRE office reserves > 8% do portfolio.
- 🟡 **ROE 8.58% abaixo do screen US** — ROE < 15% screen Buffett; aceitável para banco regional mas vigiar tendência. Trigger: `fundamentals.roe < 7%` por 2 trimestres consecutivos.

##### 4. Position sizing

**Status atual**: holding (in portfolio)

**HOLD com bias DRIP** — DY 4.10% + streak 40y + P/B 1.06 qualifica para reinvestimento; USD permanece em US (isolation rule). Sizing prudente até 4-5% do US book dado o risco regional bank concentrated. Adds em pull-backs (P/B < 0.95 ou DY > 4.5%); priority de DRIP para os dividendos vs cash deploy adicional.

##### 5. Tracking triggers (auto-monitoring)

- `fundamentals.dy < 3.0%` → quebra DRIP thesis (Aristocrat-like yield).
- NPL ratio > 1.2% (10-Q risk metrics) → credit cycle a virar.
- NIM < 2.7% por 2 trimestres → spread compression material.
- `fundamentals.pb > 1.4` → premium injustificado vs hist regional banks.
- `conviction_scores.score < 55` → tese DRIP regional bank a degradar.

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
*Generated by `ii dossier TFC` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TFC_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — TFC

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=0 | HOLD=4 | AVOID=1  
**Avg conviction majority**: 5.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- ROE abaixo de 15%
- Notícias recentes não relevantes para o negócio
- Baixo retorno sobre capital investido

**Key risk**: Risco de deterioração contínua do ROIC e pressão competitiva

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- PE razoável, mas ROE baixo
- Intangíveis significativos sugerem riscos de goodwill
- Notícias irrelevantes para valuation

**Key risk**: Risco associado a intangibilidades e goodwill pode afetar o valor contábil

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E razoável
- Dividendos atraentes
- Baixo risco devido à natureza conservadora

**Key risk**: Potencial aumento da intangibilidade e endividamento pode comprometer o valor

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: none)

**Rationale**:
- Valuation not compelling
- Lack of margin of safety
- No special situations present

**Key risk**: Permanent loss due to overvaluation and lack of intrinsic value discount

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E razoável
- Dividendos atraentes
- Intangíveis significativos

**Key risk**: Vulnerabilidade a ciclos de dívida macroeconômicos e volatilidade do setor bancário

##### 📊 Context provided

```
TICKER: US:TFC

FUNDAMENTALS LATEST:
  pe: 12.155941
  pb: 1.028654
  dy: 3.18%
  roe: 8.58%
  intangible_pct_assets: 4.1%   (goodwill $17.1B + intangibles $5.2B)

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Huntington Bancshares Incorporated $HBAN Shares Sold by Truist Financial Corp - InsuranceNewsNet [Thu, 07 Ma]
    # Huntington Bancshares Incorporated $HBAN Shares Sold by Truist Financial Corp - Insurance News | InsuranceNewsNet. HomeNow reading INN Insider News. Sign in or register to be an INNsider. INN Inside
  - 2026 Truist Championship Preview! + Cam Young's Doral dominance & Jon Rahm's deal with DP World Tour | Scorecard Stream  [Fri, 08 Ma]
    ## Golf News & Highlights. # 2026 Truist Championship Preview! + Cam Young's Doral dominance & Jon Rahm's deal with DP World Tour | Scorecard. ## Patrick McDonald and Johnson Wagner are back on Scorec
  - 2026 Truist Championship longshot picks, odds, PGA props: This golf parlay could return almost $70,000 - CBS Sports [Wed, 06 Ma]
    # 2026 Truist Championship longshot picks, odds, PGA props: This golf parlay could return almost $70,000. ## SportsLine's model simulated the 2026 Truist Championship 10,000 times and revealed a PGA l
  - PGA Tour Abruptly Announces Additional Weather Delay News at Truist Championship - heavy.com [Thu, 07 Ma]
    Share on Facebook   Share on Twitter   Share via E-mail   Share on Pinterest   Share on Flipboard   Share on Reddit   Share on WhatsApp. The start of the Truist Championship has been delayed. Things a
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama TFC --write
ii deepdive TFC --save-obsidian
ii verdict TFC --narrate --write
ii fv TFC
python -m analytics.fair_value_forward --ticker TFC
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
