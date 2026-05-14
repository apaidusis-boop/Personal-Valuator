---
type: ticker_hub
ticker: ALOS3
market: br
sector: Real Estate
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# ALOS3 — Allos

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Real Estate` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 5.77, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 17.14 · P/B 1.08 · DY 8.0% · ROE 6.9% · ND/EBITDA 3.05 · Dividend streak 6

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\ALOS3.md` (cemetery archive)_

#### ALOS3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://ri.allos.com.br/
- **Pilot rationale**: heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **11**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=29.799999237060547
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.068569995 · DY=0.07605765295393907 · P/E=17.951807
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-10 | fato_relevante | cvm | Celebração de Memorando de Entendimento para constituição de Fundo de  Investime |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reestruturações societári |
| 2026-04-02 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Encerramento da Oferta Pú |
| 2026-03-19 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atribuição de Rating AAA. |
| 2026-03-12 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ALOS3_FILING_2026-05-05.md` (cemetery archive)_

#### Filing dossier — [[ALOS3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516128&numSequencia=1040834&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 29.02

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `27.29` |
| HOLD entre | `27.29` — `31.36` (consensus) |
| TRIM entre | `31.36` — `36.07` |
| **SELL acima de** | `36.07` |

_Método: `graham_number`. Consensus fair = R$31.36. Our fair (mais conservador) = R$27.29._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.068569995` | `0.061` | +11.0% |
| EPS | `1.66` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 678.3M (-2.8% QoQ, +3.2% YoY)
- EBIT 345.8M (+0.1% QoQ)
- Margem EBIT 51.0% vs 49.5% prior
- Lucro líquido 155.9M (-32.2% QoQ, +15.4% YoY)

**BS / cash**
- Equity 14.2B (-0.3% QoQ)
- FCF proxy 400.3M (-41.1% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 31.36 | 27.29 | 29.02 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:05+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:03+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:35+00:00 | `graham_number` | 31.17 | 27.12 | 30.29 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-10 · Filing 2026-04-10
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ALOS3_FILING_2026-04-10.md` (cemetery archive)_

#### Filing dossier — [[ALOS3]] · 2026-04-10

**Trigger**: `cvm:fato_relevante` no dia `2026-04-10`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1503340&numSequencia=1028046&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 30.29

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `27.12` |
| HOLD entre | `27.12` — `31.17` (consensus) |
| TRIM entre | `31.17` — `35.85` |
| **SELL acima de** | `35.85` |

_Método: `graham_number`. Consensus fair = R$31.17. Our fair (mais conservador) = R$27.12._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06744` | `0.061` | +9.5% |
| EPS | `1.64` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 678.3M (-2.8% QoQ, +3.2% YoY)
- EBIT 345.8M (+0.1% QoQ)
- Margem EBIT 51.0% vs 49.5% prior
- Lucro líquido 155.9M (-32.2% QoQ, +15.4% YoY)

**BS / cash**
- Equity 14.2B (-0.3% QoQ)
- FCF proxy 400.3M (-41.1% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:35+00:00 | `graham_number` | 31.17 | 27.12 | 30.29 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ALOS3.md` (cemetery archive)_

#### ALOS3 — ALOS3

#watchlist #br #real_estate

##### Links

- Sector: [[sectors/Real_Estate|Real Estate]]
- Market: [[markets/BR|BR]]
- Peers: [[EZTC3]] · [[MULT3]]

##### Snapshot

- **Preço**: R$30.29  (2026-05-07)    _-2.95% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 38.0/100 (RISK)

##### Fundamentals

- P/E: 18.469513 | P/B: 1.1501367 | DY: 7.48%
- ROE: 6.74% | EPS: 1.64 | BVPS: 26.336
- Streak div: 6y | Aristocrat: None

##### Dividendos recentes

- 2026-04-23: R$0.2919
- 2026-03-30: R$0.2925
- 2026-02-20: R$0.2925
- 2026-01-22: R$0.2925
- 2025-12-22: R$0.2925

##### Eventos (SEC/CVM)

- **2026-04-10** `fato_relevante` — Celebração de Memorando de Entendimento para constituição de Fundo de  Investime
- **2026-04-06** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Reestruturações societári
- **2026-04-02** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Encerramento da Oferta Pú
- **2026-03-19** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Atribuição de Rating AAA.
- **2026-03-12** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | A concessão da Autopista Litoral Sul se estende até 2033. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ALOS3 — peso 9.6%, setor Real Estate |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados a refinanciamentos, passivos intragrupo e investimentos programados. |
| 2026-04-24 | XP | thesis | bull | — | A Oncoclínicas apresenta um modelo de negócios integrado com crescimento sustentável nos últimos anos. |
| 2026-04-24 | XP | sector_view | neutral | — | O setor de tratamento do câncer tem fundamentos sólidos de longo prazo, impulsionado pelo envelhecimento da população e avanços n… |
| 2026-04-24 | XP | thesis | neutral | — | A concessão da Autopista Litoral Sul é madura e geradora de caixa, mas apresenta pontos de atenção relacionados à rentabilidade e… |
| 2026-04-24 | XP | risk | bear | — | Há riscos regulatórios e métricas de crédito da Arteris que podem impactar a Autopista Litoral Sul. |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados à continuidade operacional e descumprimento de covenants. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -10.38%
- **Drawdown 5y**: -10.38%
- **YTD**: +6.09%
- **YoY (1y)**: +44.38%
- **CAGR 3y**: +17.09%  |  **5y**: +1.57%  |  **10y**: n/a
- **Vol annual**: +24.48%
- **Sharpe 3y** (rf=4%): +0.52

###### Dividendos
- **DY 5y avg**: +3.78%
- **Div CAGR 5y**: +41.03%
- **Frequency**: irregular
- **Streak** (sem cortes): 1 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$1.11B | R$763.9M | R$155.9M |
| 2023-12-31 | R$2.71B | R$6.35B | R$3.39B |
| 2024-12-31 | R$2.74B | R$2.21B | R$698.5M |
| 2025-12-31 | R$2.86B | R$2.48B | R$834.2M |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ALOS3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: ALOS3
    data: [21.55, 21.5, 22.19, 21.78, 22.22, 21.95, 21.62, 21.86, 22.26, 22.72, 22.85, 21.85, 22.03, 21.26, 21.05, 21.54, 22.23, 22.73, 22.69, 22.99, 23.96, 24.2, 24.22, 24.84, 25.09, 25.51, 25.22, 24.42, 23.79, 24.27, 24.53, 24.73, 25.95, 26.82, 27.99, 27.76, 28.35, 29.7, 28.36, 28.32, 27.38, 28.37, 28.77, 28.93, 28.44, 29.77, 30.78, 31.01, 31.29, 30.93, 32.04, 32.23, 30.68, 29.47, 29.73, 29.85, 29.01, 30.47, 32.91, 33.27, 31.89, 30.12, 31.21]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "ALOS3 — dividend history"
labels: ['2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.2264, 0.3839, 0.519, 1.5274, 1.4825, 1.1694]
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
    data: [20.13, 20.42683, 19.327272, 19.157576, 19.274391, 19.274391, 19.067074, 18.896341, 18.254547, 18.689024, 18.321213, 18.5, 19.030487, 18.469513]
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
    data: [6.0, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74, 6.74]
  - title: DY %
    data: [6.54, 6.2, 7.11, 7.17, 7.17, 7.17, 7.25, 7.32, 7.53, 7.4, 7.5, 7.47, 7.26, 7.48]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ALOS3_DOSSIE.md` (cemetery archive)_

#### 📑 ALOS3 — Allos

> Generated **2026-04-26** by `ii dossier ALOS3`. Cross-links: [[ALOS3]] · [[ALOS3]] · [[CONSTITUTION]]

##### TL;DR

ALOS3 negocia a P/E 19.27 e P/B 1.20 com DY 7.17% (acima do floor 6%) e streak 6y, mas ROE 6.74% fica muito abaixo do exigido (15%). IC consensus HOLD (60%, medium) reflecte o trade-off: yield decente e P/B perto de 1× dão margem de segurança, mas a rentabilidade do equity é fraca para um operador de malls. Achado-chave: yield FII-like a 7%+ depois de subida de +49.9% YoY sugere que o mercado já reprecificou a tese de queda de juros — entrada nova exige confirmação de NOI/ABL.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.64  |  **BVPS**: 26.34
- **ROE**: 6.74%  |  **P/E**: 19.27  |  **P/B**: 1.20
- **DY**: 7.17%  |  **Streak div**: 6y  |  **Market cap**: R$ 15.78B
- **Last price**: BRL 31.61 (2026-04-24)  |  **YoY**: +49.9%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[ALOS3]]

##### 3. Thesis

**Core thesis (2026-04-25)**: ALOS3 é um fundo imobiliário focado em ativos de tijolo, com um DY anualizado de 7.17%, ligeiramente abaixo da faixa ideal de 8-12% para FIIs no Brasil. Apresenta uma relação P/B de 1.20x, oferecendo margem de segurança considerável em comparação com a média do setor e um histórico consistente de pagamentos de dividendos por seis anos consecutivos.

**Key assumptions**:
1. Dividendos continuarão sendo pagos consistentemente nos próximos três anos
2. Taxa de vacância permanecerá estável ou diminuirá, mantendo a receita operacional
3. Net Debt/EBITDA se manterá abaixo dos 3.0x para garantir liquidez e capacidade de refinanciamento
4. A categoria tijolo (shoppings, lajes, logística) continuará sendo atrativa em termos de demanda imobiliária

**Disconfirmation tri

→ Vault: [[ALOS3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **73** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 90 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 19.27** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 19.27** passa.
- **P/B = 1.20** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.20** — verificar consistência com ROE.
- **DY = 7.17%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **7.17%** passa.
- **ROE = 6.74%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **6.74%** abaixo do critério.
- **Graham Number ≈ R$ 31.18** vs preço **R$ 31.61** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 6y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **ROE estruturalmente baixo** — 6.74% vs critério 15%; sustenta tese de que valuation a 1.2× P/B já é fair value. Trigger: `fundamentals.roe < 8%` em 2 trimestres consecutivos.
- 🟡 **Vacância em malls** — ciclo macro (juros, consumo) pressiona ABL ocupada e renovação de aluguel. Trigger: NOI YoY negativo nos releases trimestrais (vault releases note).
- 🟡 **Compressão de valuation por juros** — DY 7.17% compete directamente com NTN-B; corte da Selic é tailwind, mas alta surpresa é veneno. Trigger: `macro.selic_meta` subir >25bp vs assumption.
- 🟡 **Streak div curto (6y)** — não atinge floor histórico de aristocratas; risco de corte se NOI cair. Trigger: dividendo trimestral abaixo dos últimos 4Q médios.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada (não consumir caixa USD). Entry trigger: ROE >12% em 2 trimestres consecutivos OU pullback que leve P/B < 1.0× com DY ainda ≥7%. Weight prudente 3-5% como Tier-2 (real estate cíclico, não DRIP defensivo).

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → reavaliar BUY.
- **DY floor break** — `fundamentals.dy < 6%` → tese DRIP enfraquece.
- **P/B inflation** — `fundamentals.pb > 1.6` → margem de segurança evaporou.
- **Selic shock** — `macro.selic_meta` delta >+50bp vs último snapshot → revalidar valuation.
- **Conviction drop** — `conviction_scores.composite_score < 60` → flag review.

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
*Generated by `ii dossier ALOS3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | A concessão da Autopista Litoral Sul se estende até 2033. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ALOS3 — peso 9.6%, setor Real Estate |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados a refinanciamentos, passivos intragrupo e investimentos programados. |
| 2026-04-24 | XP | thesis | bull | — | A Oncoclínicas apresenta um modelo de negócios integrado com crescimento sustentável nos últimos anos. |
| 2026-04-24 | XP | sector_view | neutral | — | O setor de tratamento do câncer tem fundamentos sólidos de longo prazo, impulsionado pelo envelhecimento da população e avanços n… |
| 2026-04-24 | XP | thesis | neutral | — | A concessão da Autopista Litoral Sul é madura e geradora de caixa, mas apresenta pontos de atenção relacionados à rentabilidade e… |
| 2026-04-24 | XP | risk | bear | — | Há riscos regulatórios e métricas de crédito da Arteris que podem impactar a Autopista Litoral Sul. |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados à continuidade operacional e descumprimento de covenants. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ALOS3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — ALOS3

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=1 | HOLD=4 | AVOID=0  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE baixo
- DY abaixo da faixa ideal
- FCF variável

**Key risk**: Possível aumento na taxa de vacância impactando receita operacional

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- DY atrativo e consistente
- P/B oferece margem de segurança
- Histórico positivo de FCF

**Key risk**: Taxa de vacância aumentando ou desaceleração econômica afetando demanda imobiliária

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- DY atrativo, mas abaixo da faixa ideal
- Histórico consistente de dividendos
- Margem de segurança P/B

**Key risk**: Taxa de vacância aumentando ou aumento significativo na dívida

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: small)

**Rationale**:
- Margem de segurança limitada
- DY abaixo da faixa ideal
- Liquidez e refinanciamento garantidos

**Key risk**: Aumento da taxa de vacância impactando receita operacional

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/B razoável e consistência de dividendos
- Taxa de vacância estável
- Net Debt/EBITDA controlado

**Key risk**: Possível aumento da taxa de vacância impactando receita operacional

##### 📊 Context provided

```
TICKER: BR:ALOS3

FUNDAMENTALS LATEST:
  pe: 18.283133
  pb: 1.1524149
  dy: 7.47%
  roe: 6.74%
  net_debt_ebitda: 2.998148242344636
  intangible_pct_assets: 3.1%   (goodwill $0.3B + intangibles $0.5B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=0.7 ebit=0.3 ni=0.2 em%=51.0 debt=0 fcf=0.4
  2025-06-30: rev=0.7 ebit=0.3 ni=0.2 em%=49.5 debt=0 fcf=0.7
  2025-03-31: rev=0.6 ebit=0.4 ni=0.3 em%=68.9 debt=0 fcf=1.0
  2024-12-31: rev=0.8 ebit=0.4 ni=0.2 em%=56.3 debt=0 fcf=2.9
  2024-09-30: rev=0.7 ebit=0.3 ni=0.1 em%=47.7 debt=0 fcf=-1.8
  2024-06-30: rev=0.6 ebit=0.4 ni=0.3 em%=64.2 debt=0 fcf=0.1

VAULT THESIS:
**Core thesis (2026-04-25)**: ALOS3 é um fundo imobiliário focado em ativos de tijolo, com um DY anualizado de 7.17%, ligeiramente abaixo da faixa ideal de 8-12% para FIIs no Brasil. Apresenta uma relação P/B de 1.20x, oferecendo margem de segurança considerável em comparação com a média do setor e um histórico consistente de pagamentos de dividendos por seis anos consecutivos.

**Key assumptions**:
1. Dividendos continuarão sendo pagos consistentemente nos próximos três anos
2. Taxa de vacância permanecerá estável ou diminuirá, mantendo a receita operacional
3. Net Debt/EBITDA se manterá abaixo dos 3.0x para garantir liquidez e capacidade de refinanciamento
4. A categoria tijolo (shoppings, lajes, logística) continuará sendo atrativa em termos de demanda imobiliária

**Disconfirmation tri

RECENT MATERIAL NEWS (last 14d via Tavily):
  - SES satellites to support Brazil’s offshore oil production - Developing Telecoms [Tue, 05 Ma]
    ## SES satellites to support Brazil’s offshore oil production. Space solutions company SES has announced that it will provide service on its high-capacity medium-Earth orbit (MEO) satellite network O3
  - SES to connect seven Petrobras FPSOs with O3b mPOWER network - World Oil [Tue, 05 Ma]
    # SES to connect seven Petrobras FPSOs with O3b mPOWER network. (WO) - SES S.A. will provide satellite connectivity for seven 
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | A concessão da Autopista Litoral Sul se estende até 2033. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ALOS3 — peso 9.6%, setor Real Estate |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados a refinanciamentos, passivos intragrupo e investimentos programados. |
| 2026-04-24 | XP | thesis | bull | — | A Oncoclínicas apresenta um modelo de negócios integrado com crescimento sustentável nos últimos anos. |
| 2026-04-24 | XP | sector_view | neutral | — | O setor de tratamento do câncer tem fundamentos sólidos de longo prazo, impulsionado pelo envelhecimento da população e avanços n… |
| 2026-04-24 | XP | thesis | neutral | — | A concessão da Autopista Litoral Sul é madura e geradora de caixa, mas apresenta pontos de atenção relacionados à rentabilidade e… |
| 2026-04-24 | XP | risk | bear | — | Há riscos regulatórios e métricas de crédito da Arteris que podem impactar a Autopista Litoral Sul. |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados à continuidade operacional e descumprimento de covenants. |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ALOS3_RI.md` (cemetery archive)_

#### ALOS3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `net_income`: **-32.2%**
- ⬇️ **QOQ** `fcf_proxy`: **-41.1%**
- ⬇️ **QOQ** `net_margin`: **-10.0pp**
- ⬆️ **YOY** `fcf_proxy`: **+122.5%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 0.7 mi | R$ 0.7 mi | -2.8% |
| `ebit` | R$ 0.3 mi | R$ 0.3 mi | +0.0% |
| `net_income` | R$ 0.2 mi | R$ 0.2 mi | -32.2% |
| `debt_total` | R$ 0.0 mi | R$ 0.0 mi | — |
| `fco` | R$ 0.4 mi | R$ 0.5 mi | -28.2% |
| `fcf_proxy` | R$ 0.4 mi | R$ 0.7 mi | -41.1% |
| `gross_margin` | 76.3% | 74.1% | +2.2pp |
| `ebit_margin` | 51.0% | 49.5% | +1.5pp |
| `net_margin` | 23.0% | 32.9% | -10.0pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 0.7 mi | R$ 0.7 mi | +3.2% |
| `ebit` | R$ 0.3 mi | R$ 0.3 mi | +10.3% |
| `net_income` | R$ 0.2 mi | R$ 0.1 mi | +15.4% |
| `debt_total` | R$ 0.0 mi | R$ 0.0 mi | — |
| `fco` | R$ 0.4 mi | R$ 0.4 mi | -10.1% |
| `fcf_proxy` | R$ 0.4 mi | R$ -1.8 mi | +122.5% |
| `gross_margin` | 76.3% | 72.9% | +3.4pp |
| `ebit_margin` | 51.0% | 47.7% | +3.3pp |
| `net_margin` | 23.0% | 20.5% | +2.4pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 0.7 | 51.0% | 23.0% | 0 | 0 |
| 2025-06-30 | ITR | 0.7 | 49.5% | 32.9% | 0 | 0 |
| 2025-03-31 | ITR | 0.6 | 68.9% | 42.8% | 0 | 0 |
| 2024-12-31 | DFP-ITR | 0.8 | 56.3% | 25.3% | 0 | 0 |
| 2024-09-30 | ITR | 0.7 | 47.7% | 20.5% | 0 | 0 |
| 2024-06-30 | ITR | 0.6 | 64.2% | 54.3% | 0 | 0 |
| 2024-03-31 | ITR | 0.6 | 43.4% | 19.8% | 0 | 0 |
| 2023-12-31 | DFP-ITR | 0.8 | 23.2% | 33.5% | 0 | 1 |
| 2023-09-30 | ITR | 0.7 | 33.3% | 7.9% | 0 | 0 |
| 2023-06-30 | ITR | 0.7 | 49.0% | 27.6% | 0 | 0 |
| 2023-03-31 | ITR | 0.6 | 755.3% | 482.6% | 0 | 0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [0.6, 0.7, 0.7, 0.8, 0.6, 0.6, 0.7, 0.8, 0.6, 0.7, 0.7]
  - title: EBIT margin %
    data: [755.3, 49.0, 33.3, 23.2, 43.4, 64.2, 47.7, 56.3, 68.9, 49.5, 51.0]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama ALOS3 --write
ii deepdive ALOS3 --save-obsidian
ii verdict ALOS3 --narrate --write
ii fv ALOS3
python -m analytics.fair_value_forward --ticker ALOS3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
