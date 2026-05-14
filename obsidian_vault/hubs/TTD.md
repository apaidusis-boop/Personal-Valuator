---
type: ticker_hub
ticker: TTD
market: us
sector: Communication
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 5
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# TTD — The Trade Desk

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Communication` · `market: US` · `currency: USD` · `bucket: holdings` · `5 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `HOLD` (score 4.13, 2026-05-08)
- **Fundamentals** (2026-05-13): P/E 23.28 · P/B 3.93 · ROE 16.7% · ND/EBITDA -1.38 · Dividend streak 0 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\TTD.md` (cemetery archive)_

#### TTD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Communication
- **RI URLs scraped** (1):
  - https://investors.thetradedesk.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **134**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=21.520000457763672
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.16735001 · DY=None · P/E=24.454546
- Score (último run): score=0.25 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 5.02 |
| 2026-05-08 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-05-07 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 1.01,2.03 |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\TTD_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[TTD]] · 2026-05-08

**Trigger**: `sec:8-K` no dia `2026-05-08`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1671933/000167193326000055/ttd-20260504.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 24.01

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `11.74` |
| HOLD entre | `11.74` — `15.66` (consensus) |
| TRIM entre | `15.66` — `18.01` |
| **SELL acima de** | `18.01` |

_Método: `buffett_ceiling`. Consensus fair = R$15.66. Our fair (mais conservador) = R$11.74._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 15.66 | 11.74 | 24.01 | SELL | single_source | `filing:sec:8-K:2026-05-08` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TTD.md` (cemetery archive)_

#### TTD — The Trade Desk

#holding #us #communication

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 4.1/10  |  **Confiança**: 70%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 5.7/10 | 35% | `██████░░░░` |
| Valuation  | 2.5/10 | 30% | `██░░░░░░░░` |
| Momentum   | 4.0/10 | 20% | `████░░░░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z 2.7931866436948565 (GREY), Piotroski 6/9 (NEUTRAL), DivSafety 61.5/100
- **Valuation**: Screen 0.25, DY percentil - (-)
- **Momentum**: 1d -2.44%, 30d 18.57%, YTD -36.28%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- total 4.1 na zona neutra
- valuation caro

##### Links

- Sector: [[sectors/Communication|Communication]]
- Market: [[markets/US|US]]
- Peers: [[TDS]]

##### Snapshot

- **Preço**: $24.01  (2026-05-06)    _-2.44% 1d_
- **Screen**: 0.25  ✗ fail
- **Altman Z**: 2.793 (grey)
- **Piotroski**: 6/9
- **Div Safety**: 61.5/100 (WATCH)

##### Fundamentals

- P/E: 26.677778 | P/B: 4.599617 | DY: None%
- ROE: 16.32% | EPS: 0.9 | BVPS: 5.22
- Streak div: 0y | Aristocrat: False

##### Eventos (SEC/CVM)

- **2026-05-07** `8-K` — 8-K | 2.02,9.01
- **2026-05-07** `10-Q` — 10-Q
- **2026-04-20** `8-K` — 8-K | 1.01,2.03
- **2026-04-09** `proxy` — DEF 14A
- **2026-04-06** `8-K` — 8-K | 5.02

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -73.25%
- **Drawdown 5y**: -82.79%
- **YTD**: -36.28%
- **YoY (1y)**: -56.84%
- **CAGR 3y**: -27.38%  |  **5y**: -18.35%  |  **10y**: n/a
- **Vol annual**: +73.73%
- **Sharpe 3y** (rf=4%): -0.50

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
| 2022-12-31 | $1.58B | $53.4M | $456.8M |
| 2023-12-31 | $1.95B | $178.9M | $543.3M |
| 2024-12-31 | $2.44B | $393.1M | $632.4M |
| 2025-12-31 | $2.90B | $443.3M | $783.0M |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "TTD — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: TTD
    data: [59.9, 79.14, 77.06, 76.06, 74.77, 71.46, 70.57, 68.66, 69.8, 73.49, 74.03, 75.43, 80.21, 85.0, 86.42, 87.7, 53.17, 52.12, 52.3, 52.65, 53.77, 52.4, 45.54, 44.47, 46.76, 49.32, 53.49, 51.28, 49.98, 54.13, 49.96, 47.24, 43.26, 41.93, 38.35, 39.11, 38.61, 39.4, 36.19, 37.26, 38.31, 37.68, 37.3, 37.13, 35.33, 32.19, 29.75, 27.04, 26.14, 25.24, 25.16, 25.0, 28.56, 27.34, 23.51, 21.97, 22.69, 20.7, 21.22, 22.47, 22.62, 24.37, 24.61]
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
    data: [24.627779, 25.522112, 25.288889, 24.966667, 26.083334, 25.777779, 26.633333, 26.633333, 26.633333, 25.711111, 25.811111, 27.07778, 26.211111, 26.777779, 27.344446, 26.677778]
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
    data: [16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32, 16.32]
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
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TTD_DOSSIE.md` (cemetery archive)_

#### 📑 TTD — The Trade Desk

> Generated **2026-04-26** by `ii dossier TTD`. Cross-links: [[TTD]] · _(no IC yet)_ · [[CONSTITUTION]]

##### TL;DR

TTD negoceia P/E 26.63, sem dividendo, ROE 16.32% — DSP independente líder em Connected TV / programmatic. IC ainda não gerado (correr `python -m agents.synthetic_ic TTD`); YoY -55.0% reflecte sell-off severo após guidance miss e tese cookie-deprecation comprometida. Growth pick puro, NÃO DRIP — drawdown coloca tese em teste; reavaliar com synthetic IC antes de aumentar.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.90  |  **BVPS**: 5.22
- **ROE**: 16.32%  |  **P/E**: 26.63  |  **P/B**: 4.59
- **DY**: n/a  |  **Streak div**: n/ay  |  **Market cap**: USD 11.41B
- **Last price**: USD 23.97 (2026-04-24)  |  **YoY**: -55.0%

##### 2. Synthetic IC

_(IC ainda não gerado para TTD. Execute `python -m agents.synthetic_ic TTD` para popular antes do dossier ser refinado.)_

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 26.63** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 26.63** esticado vs critério.
- **P/B = 4.59** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **4.59** esticado.
- **ROE = 16.32%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **16.32%** compounder-grade.
- **Graham Number ≈ R$ 10.28** vs preço **R$ 23.97** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 3. Riscos identificados

- 🔴 **Connected TV growth deceleração** — vector central da tese; ramp da CTV abaixo do esperado pesou no -55% YoY. Trigger: CTV revenue YoY < 25% ou guidance cut adicional em earnings call.
- 🔴 **Google ad cookies / privacy shift** — Google deprecation timeline e Privacy Sandbox impactam open-internet thesis directamente. Trigger: anúncio Chrome cookie deprecation date concrete + UID2 adoption < 50% top 100 advertisers.
- 🟡 **Customer concentration** — top 100 advertisers respondem por bulk da revenue; perda de 1-2 grandes accounts material. Trigger: customer retention < 95% ou anúncio de churn em 8-K.
- 🟡 **Sem IC ainda** — verdict por gerar; não tomar decisões grandes antes de sintetizar. Trigger: rodar `python -m agents.synthetic_ic TTD`.

##### 4. Position sizing

**Status atual**: holding (in portfolio)

**HOLD — pausa para reavaliar** — growth pick adtech sem dividendo (NÃO DRIP); USD permanece em US (isolation rule). Drawdown -55% YoY coloca a tese sob escrutínio severo; NÃO aumentar antes de gerar synthetic IC e confirmar conviction. Sizing máximo 3-4% do US book; considerar trim parcial se thesis_health degradar abaixo de 50.

##### 5. Tracking triggers (auto-monitoring)

- CTV revenue YoY < 25% → core driver da tese a quebrar.
- Customer retention < 95% (10-K disclosure) → concentração risk a materializar.
- Revenue YoY < 15% por 2 trimestres → growth premium injustificado.
- `fundamentals.pe > 35` mesmo com -55% YoY → re-rating optimista sem fundamentos.
- `conviction_scores.score < 50` (após gerar IC) → trim signal forte.

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
*Generated by `ii dossier TTD` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\TTD_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — TTD

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 4.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E alto, mas ROE positivo
- Dívida baixa em relação a EBITDA
- Necessidade de análise adicional sobre moat e gestão

**Key risk**: Valuation elevado pode não refletir um negócio excelente ou uma vantagem competitiva duradoura

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- P/E razoável, mas P/B alto
- ROE positivo, mas não impressionante
- Dívida baixa, mas crescimento potencial incerto

**Key risk**: Preço atual pode estar refletindo otimismo excessivo sobre o crescimento futuro

###### 🔴 Nassim Taleb — **AVOID** (conv 9/10, size: none)

**Rationale**:
- PE alto
- Leverage potencial em negócios de crescimento
- Falta de antifragilidade

**Key risk**: Overvaluation e fragilidade a mudanças abruptas no mercado

###### 🔴 Seth Klarman — **AVOID** (conv 10/10, size: none)

**Rationale**:
- P/E alto
- PB elevado
- Debt/EBITDA negativo não indica valor

**Key risk**: Perda permanente de capital com preço acima do valor intrínseco

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: small)

**Rationale**:
- PE elevado
- ROE positivo, mas não impressionante
- Net debt/EBITDA negativo sugerindo liquidez

**Key risk**: Ciclo de dívida e condições macroeconômicas podem afetar ações

##### 📊 Context provided

```
TICKER: US:TTD

FUNDAMENTALS LATEST:
  pe: 26.633333
  pb: 4.591954
  roe: 16.32%
  net_debt_ebitda: -1.2559349807022997
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama TTD --write
ii deepdive TTD --save-obsidian
ii verdict TTD --narrate --write
ii fv TTD
python -m analytics.fair_value_forward --ticker TTD
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
