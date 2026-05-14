---
type: ticker_hub
ticker: PGMN3
market: br
sector: Consumer Staples
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# PGMN3 — Pague Menos

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Consumer Staples` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 2.63, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 9.63 · P/B 1.01 · DY 5.4% · ROE 9.0% · ND/EBITDA 3.46 · Dividend streak 3

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\PGMN3.md` (cemetery archive)_

#### PGMN3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://ri.paguemenos.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **9**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.019999980926514
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.089729995 · DY=0.051099203381402385 · P/E=10.244898
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-03-23 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional (PT/EN |
| 2026-03-18 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-16 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-10 | fato_relevante | cvm | Aprovação do Preço por Ação no âmbito da Oferta Pública de Distribuição Primária |
| 2026-03-03 | fato_relevante | cvm | Oferta Pública de Distribuição Primária e Secundária de Ações Ordinárias de Emis |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PGMN3_FILING_2026-05-05.md` (cemetery archive)_

#### Filing dossier — [[PGMN3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515665&numSequencia=1040371&numVersao=1>

##### 🎯 Acção sugerida

###### 🟢🟢 **STRONG_BUY** &mdash; preço 4.89

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `5.89` |
| HOLD entre | `5.89` — `7.18` (consensus) |
| TRIM entre | `7.18` — `8.26` |
| **SELL acima de** | `8.26` |

_Método: `graham_number`. Consensus fair = R$7.18. Our fair (mais conservador) = R$5.89._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.089729995` | `0.0714` | +20.5% |
| EPS | `0.49` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.9B (+4.3% QoQ, +17.8% YoY)
- EBIT 251.0M (+9.3% QoQ)
- Margem EBIT 6.5% vs 6.2% prior
- Lucro líquido 76.0M (+50.9% QoQ, +85.5% YoY)

**BS / cash**
- Equity 2.9B (+2.6% QoQ)
- Dívida total 1.7B (+2.8% QoQ)
- FCF proxy -40.9M (+66.8% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 7.18 | 5.89 | 4.89 | STRONG_BUY | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 7.18 | 5.89 | 5.10 | STRONG_BUY | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 7.18 | 5.89 | 5.10 | STRONG_BUY | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 7.18 | 5.89 | 5.10 | STRONG_BUY | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:44+00:00 | `graham_number` | 7.18 | 5.89 | 5.01 | STRONG_BUY | cross_validated | `filing:cvm:fato_relevante:2026-03-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-03-10 · Filing 2026-03-10
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\PGMN3_FILING_2026-03-10.md` (cemetery archive)_

#### Filing dossier — [[PGMN3]] · 2026-03-10

**Trigger**: `cvm:fato_relevante` no dia `2026-03-10`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1488644&numSequencia=1013350&numVersao=1>

##### 🎯 Acção sugerida

###### 🟢🟢 **STRONG_BUY** &mdash; preço 5.01

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `5.89` |
| HOLD entre | `5.89` — `7.18` (consensus) |
| TRIM entre | `7.18` — `8.26` |
| **SELL acima de** | `8.26` |

_Método: `graham_number`. Consensus fair = R$7.18. Our fair (mais conservador) = R$5.89._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.089729995` | `0.0714` | +20.5% |
| EPS | `0.49` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.9B (+4.3% QoQ, +17.8% YoY)
- EBIT 251.0M (+9.3% QoQ)
- Margem EBIT 6.5% vs 6.2% prior
- Lucro líquido 76.0M (+50.9% QoQ, +85.5% YoY)

**BS / cash**
- Equity 2.9B (+2.6% QoQ)
- Dívida total 1.7B (+2.8% QoQ)
- FCF proxy -40.9M (+66.8% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:44+00:00 | `graham_number` | 7.18 | 5.89 | 5.01 | STRONG_BUY | cross_validated | `filing:cvm:fato_relevante:2026-03-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PGMN3.md` (cemetery archive)_

#### PGMN3 — PGMN3

#watchlist #br #consumer_staples

##### Links

- Sector: [[sectors/Consumer_Staples|Consumer Staples]]
- Market: [[markets/BR|BR]]
- Peers: [[ABEV3]] · [[GMAT3]] · [[PNVL3]] · [[SLCE3]] · [[TTEN3]]

##### Snapshot

- **Preço**: R$5.01  (2026-05-07)    _-4.93% 1d_
- **Screen**: 0.2  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 40.0/100 (RISK)

##### Fundamentals

- P/E: 10.22449 | P/B: 1.0711995 | DY: 5.12%
- ROE: 8.97% | EPS: 0.49 | BVPS: 4.677
- Streak div: 3y | Aristocrat: None

##### Dividendos recentes

- 2025-12-26: R$0.2565
- 2025-01-21: R$0.2509
- 2024-01-29: R$0.2919
- 2023-01-30: R$0.1781

##### Eventos (SEC/CVM)

- **2026-03-23** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Institucional (PT/EN
- **2026-03-18** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-03-16** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-03-10** `fato_relevante` — Aprovação do Preço por Ação no âmbito da Oferta Pública de Distribuição Primária
- **2026-03-03** `fato_relevante` — Oferta Pública de Distribuição Primária e Secundária de Ações Ordinárias de Emis

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | 8.50 | Recomendação de compra para PGMN3 com preço-alvo de R$8,5/ação até o final de 2026. |
| 2026-04-24 | XP | thesis | bull | — | A produtividade das lojas da PGMN deve melhorar continuamente até atingir ~R$965 mil por loja no final de 2026. |
| 2026-04-24 | XP | numerical | neutral | — | O valuation atual é atrativo, negociado a ~10,5x P/L 2026. |
| 2026-04-24 | XP | catalyst | bull | — | Os genéricos de semaglutida devem começar a ser vendidos no segundo semestre de 2026, com um mercado endereçável que pode surpree… |
| 2026-04-24 | XP | numerical | bull | — | O GLP-1 deve responder por cerca de ~1/3 do crescimento da PGMN em 2026. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PGMN3 — peso 9.6%, setor Consumer Staples |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PGMN3 — peso 1.8% |
| 2026-04-24 | XP | catalyst | bull | — | A PGMN deve se beneficiar da tendência estrutural de GLP-1, com aceleração prevista à frente. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -33.55%
- **Drawdown 5y**: -61.60%
- **YTD**: -19.84%
- **YoY (1y)**: +43.14%
- **CAGR 3y**: +18.73%  |  **5y**: -13.06%  |  **10y**: n/a
- **Vol annual**: +42.94%
- **Sharpe 3y** (rf=4%): +0.32

###### Dividendos
- **DY 5y avg**: +7.40%
- **Div CAGR 5y**: +68.78%
- **Frequency**: annual
- **Streak** (sem cortes): 2 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$9.19B | R$1.11B | R$263.7M |
| 2023-12-31 | R$11.20B | R$797.9M | R$2.5M |
| 2024-12-31 | R$12.64B | R$957.5M | R$103.1M |
| 2025-12-31 | R$14.91B | R$1.21B | R$260.3M |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "PGMN3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: PGMN3
    data: [3.47, 3.34, 3.34, 3.38, 3.48, 3.45, 3.37, 3.44, 3.49, 3.45, 3.39, 3.38, 3.44, 3.53, 3.5, 3.92, 3.91, 3.68, 3.58, 3.65, 3.62, 3.78, 3.88, 3.57, 3.57, 3.61, 3.6, 3.62, 3.55, 3.83, 3.87, 3.84, 4.02, 4.45, 4.86, 4.85, 5.89, 6.28, 5.7, 6.02, 5.88, 6.09, 6.44, 6.45, 6.34, 6.43, 6.56, 6.56, 6.61, 7.25, 7.4, 6.82, 6.2, 6.11, 6.1, 6.3, 6.13, 5.69, 5.86, 5.67, 5.59, 5.44, 5.27]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "PGMN3 — dividend history"
labels: ['2023', '2024', '2025']
series:
  - title: Dividends
    data: [0.1781, 0.2919, 0.5074]
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
    data: [16.33, 13.785714, 13.309525, 13.571428, 13.571428, 13.571428, 13.476191, 13.166668, 12.952381, 13.238095, 12.833333, 12.690476, 10.755102, 10.22449]
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
    data: [8.41, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97, 8.97]
  - title: DY %
    data: [4.39, 4.43, 4.59, 4.5, 4.5, 4.5, 4.53, 4.64, 4.72, 4.61, 4.76, 4.81, 4.87, 5.12]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PGMN3_DOSSIE.md` (cemetery archive)_

#### 📑 PGMN3 — Pague Menos

> Generated **2026-04-26** by `ii dossier PGMN3`. Cross-links: [[PGMN3]] · [[PGMN3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

PGMN3 negocia P/E 13.57 e P/B 1.22 (perto do livro) com DY 4.50% e ROE 8.97% — abaixo do critério Graham (DY 6%, ROE 15%). IC consensus HOLD com confiança máxima (100%) — ninguém diverge: empresa em fase de turnaround com fundamentos médios. Achado-chave: subida de +66.2% YoY já reprecificou a tese contrarian; entrada nova precisa de prova de melhoria de margem retalho ou expansão da clínica.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.42  |  **BVPS**: 4.68
- **ROE**: 8.97%  |  **P/E**: 13.57  |  **P/B**: 1.22
- **DY**: 4.50%  |  **Streak div**: 3y  |  **Market cap**: R$ 4.30B
- **Last price**: BRL 5.70 (2026-04-24)  |  **YoY**: +66.2%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 100.0% consensus)

→ Detalhe: [[PGMN3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A PGMN3, uma empresa do setor de Consumer Staples, apresenta um valuation atrativo com P/E de 13.57 e P/B de 1.22, embora não atenda aos critérios rigorosos da filosofia value-investimento ajustada à Selic alta (Graham clássico). A empresa tem uma taxa de dividendos de 4.50% e um ROE de 8.97%, indicando potencial para melhorias em eficiência operacional.

**Key assumptions**:
1. A PGMN3 manterá sua posição no mercado brasileiro, mantendo margens estáveis
2. O cenário macroeconômico do Brasil continuará a suportar o consumo de bens essenciais
3. A empresa aumentará seus esforços para melhorar seu ROE e reduzir sua dívida líquida/EBITDA
4. Os dividendos continuarão sendo pagos, mesmo com a atual crise econômica

**Disconfirmation triggers**:
- ROE cai abaixo de

→ Vault: [[PGMN3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **67** |
| Thesis health | 92 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 70 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 13.57** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 13.57** passa.
- **P/B = 1.22** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.22** — verificar consistência com ROE.
- **DY = 4.50%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.50%** abaixo do floor — DRIP não-óbvio.
- **ROE = 8.97%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **8.97%** abaixo do critério.
- **Graham Number ≈ R$ 6.65** vs preço **R$ 5.70** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 3y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Margem retalho farma sob pressão** — sector altamente competitivo (RaiaDrogasil, Pague Menos, redes regionais); ROE 8.97% reflecte essa compressão. Trigger: `fundamentals.roe < 7%` em 2 trimestres.
- 🟡 **Streak div curta (3y)** — sem track record para sustentar tese DRIP. Trigger: dividendo trimestral abaixo da média móvel 4Q.
- 🟡 **Competição RD/Drogasil** — peer maior tem economias de escala; risco de perda de share. Trigger: gross margin YoY <-100bp em release.
- 🟡 **Reprecificação esticada** — +66% YoY pode ter consumido upside; reversão rápida possível. Trigger: `prices.close` queda >-15% em 30d.
- 🟢 **Valuation moderado** — P/B 1.22 dá floor parcial; risco de mark-down limitado. Trigger: `fundamentals.pb > 1.8` para alerta.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR (caixa BRL only). Entry trigger: ROE recovery >12% em 2 trimestres OU pullback significativo (>-20%) que recoloque DY próximo a 6%. Weight prudente 2-3% como Tier-2 (mid-cap consumer staples, tese turnaround não consolidada).

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → confirma turnaround.
- **DY upgrade** — `fundamentals.dy > 6%` → entra critério Graham.
- **Margin compression** — `fundamentals.eps` YoY <-15% → sector pressure confirmada.
- **Pullback técnico** — `prices.close` queda >-20% em 60d com fundamentos intactos → entry zone.
- **Thesis health** — `conviction_scores.composite_score < 55` → flag review.

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
*Generated by `ii dossier PGMN3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | 8.50 | Recomendação de compra para PGMN3 com preço-alvo de R$8,5/ação até o final de 2026. |
| 2026-04-24 | XP | thesis | bull | — | A produtividade das lojas da PGMN deve melhorar continuamente até atingir ~R$965 mil por loja no final de 2026. |
| 2026-04-24 | XP | numerical | neutral | — | O valuation atual é atrativo, negociado a ~10,5x P/L 2026. |
| 2026-04-24 | XP | catalyst | bull | — | Os genéricos de semaglutida devem começar a ser vendidos no segundo semestre de 2026, com um mercado endereçável que pode surpree… |
| 2026-04-24 | XP | numerical | bull | — | O GLP-1 deve responder por cerca de ~1/3 do crescimento da PGMN em 2026. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PGMN3 — peso 9.6%, setor Consumer Staples |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PGMN3 — peso 1.8% |
| 2026-04-24 | XP | catalyst | bull | — | A PGMN deve se beneficiar da tendência estrutural de GLP-1, com aceleração prevista à frente. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PGMN3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — PGMN3

**Committee verdict**: **HOLD** (high confidence, 100% consensus)  
**Votes**: BUY=0 | HOLD=5 | AVOID=0  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: small)

**Rationale**:
- Valuation atraente com P/E e P/B baixos
- Dividendos consistentes
- Posição sólida no mercado brasileiro

**Key risk**: ROE abaixo do desejado e geração de caixa negativa recentemente

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Valuation atrativo
- Dividendos consistentes
- Potencial para melhorar ROE

**Key risk**: Desaceleração econômica no Brasil pode afetar margens e consumo de bens essenciais

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Valuation atrativo, mas não oferece convexidade
- Dividendos atraentes, porém ROE fraco
- Não apresenta barbell strategy

**Key risk**: Fragilidade financeira com dívida elevada e FCF negativa

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E e P/B razoáveis, mas não oferecem margem de segurança significativa
- Dividendos atraentes, mas ROE baixo
- Necessidade de melhorias operacionais

**Key risk**: Possível deterioração das margens devido a fatores macroeconômicos

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Valuation atrativo
- Potencial para melhorias operacionais
- Dividendos consistentes

**Key risk**: Dívida líquida/EBITDA elevada pode comprometer a capacidade de geração de caixa

##### 📊 Context provided

```
TICKER: BR:PGMN3

FUNDAMENTALS LATEST:
  pe: 13.571428
  pb: 1.2187299
  dy: 4.50%
  roe: 8.97%
  net_debt_ebitda: 3.4583879614556476

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=3.9 ebit=0.3 ni=0.1 em%=6.5 debt=2 fcf=-0.0
  2025-06-30: rev=3.7 ebit=0.2 ni=0.1 em%=6.2 debt=2 fcf=-0.1
  2025-03-31: rev=3.4 ebit=0.1 ni=0.0 em%=4.2 debt=1 fcf=0.0
  2024-12-31: rev=3.3 ebit=0.1 ni=0.1 em%=4.4 debt=1 fcf=0.1
  2024-09-30: rev=3.3 ebit=0.2 ni=0.0 em%=5.3 debt=1 fcf=0.1
  2024-06-30: rev=3.1 ebit=0.2 ni=0.0 em%=5.3 debt=1 fcf=0.1

VAULT THESIS:
**Core thesis (2026-04-25)**: A PGMN3, uma empresa do setor de Consumer Staples, apresenta um valuation atrativo com P/E de 13.57 e P/B de 1.22, embora não atenda aos critérios rigorosos da filosofia value-investimento ajustada à Selic alta (Graham clássico). A empresa tem uma taxa de dividendos de 4.50% e um ROE de 8.97%, indicando potencial para melhorias em eficiência operacional.

**Key assumptions**:
1. A PGMN3 manterá sua posição no mercado brasileiro, mantendo margens estáveis
2. O cenário macroeconômico do Brasil continuará a suportar o consumo de bens essenciais
3. A empresa aumentará seus esforços para melhorar seu ROE e reduzir sua dívida líquida/EBITDA
4. Os dividendos continuarão sendo pagos, mesmo com a atual crise econômica

**Disconfirmation triggers**:
- ROE cai abaixo de 

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Petrobras takes FID on SEAP FPSO development in Brazil basin - World Oil [Tue, 14 Ap]
    World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petrobras takes FID on SEAP FPS
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global minerals demand is strong enough 
  - B
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=8 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | 8.50 | Recomendação de compra para PGMN3 com preço-alvo de R$8,5/ação até o final de 2026. |
| 2026-04-24 | XP | thesis | bull | — | A produtividade das lojas da PGMN deve melhorar continuamente até atingir ~R$965 mil por loja no final de 2026. |
| 2026-04-24 | XP | numerical | neutral | — | O valuation atual é atrativo, negociado a ~10,5x P/L 2026. |
| 2026-04-24 | XP | catalyst | bull | — | Os genéricos de semaglutida devem começar a ser vendidos no segundo semestre de 2026, com um mercado endereçável que pode surpree… |
| 2026-04-24 | XP | numerical | bull | — | O GLP-1 deve responder por cerca de ~1/3 do crescimento da PGMN em 2026. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PGMN3 — peso 9.6%, setor Consumer Staples |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PGMN3 — peso 1.8% |
| 2026-04-24 | XP | catalyst | bull | — | A PGMN deve se beneficiar da tendência estrutural de GLP-1, com aceleração prevista à frente. |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\PGMN3_RI.md` (cemetery archive)_

#### PGMN3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `net_income`: **+50.9%**
- ⬆️ **QOQ** `fco`: **+133.8%**
- ⬆️ **QOQ** `fcf_proxy`: **+66.8%**
- ⬆️ **YOY** `revenue`: **+17.8%**
- ⬆️ **YOY** `ebit`: **+44.9%**
- ⬆️ **YOY** `net_income`: **+85.5%**
- ⬇️ **YOY** `fco`: **-83.9%**
- ⬇️ **YOY** `fcf_proxy`: **-127.3%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.9 mi | R$ 3.7 mi | +4.3% |
| `ebit` | R$ 0.3 mi | R$ 0.2 mi | +9.3% |
| `net_income` | R$ 0.1 mi | R$ 0.1 mi | +50.9% |
| `debt_total` | R$ 1.7 mi | R$ 1.7 mi | +2.8% |
| `fco` | R$ 0.0 mi | R$ -0.1 mi | +133.8% |
| `fcf_proxy` | R$ -0.0 mi | R$ -0.1 mi | +66.8% |
| `gross_margin` | 32.1% | 33.0% | -0.9pp |
| `ebit_margin` | 6.5% | 6.2% | +0.3pp |
| `net_margin` | 2.0% | 1.4% | +0.6pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.9 mi | R$ 3.3 mi | +17.8% |
| `ebit` | R$ 0.3 mi | R$ 0.2 mi | +44.9% |
| `net_income` | R$ 0.1 mi | R$ 0.0 mi | +85.5% |
| `debt_total` | R$ 1.7 mi | R$ 1.5 mi | +19.3% |
| `fco` | R$ 0.0 mi | R$ 0.2 mi | -83.9% |
| `fcf_proxy` | R$ -0.0 mi | R$ 0.1 mi | -127.3% |
| `gross_margin` | 32.1% | 31.6% | +0.6pp |
| `ebit_margin` | 6.5% | 5.3% | +1.2pp |
| `net_margin` | 2.0% | 1.3% | +0.7pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 3.9 | 6.5% | 2.0% | 2 | 0 |
| 2025-06-30 | ITR | 3.7 | 6.2% | 1.4% | 2 | -0 |
| 2025-03-31 | ITR | 3.4 | 4.2% | 0.2% | 1 | 0 |
| 2024-12-31 | DFP-ITR | 3.3 | 4.4% | 2.0% | 1 | 0 |
| 2024-09-30 | ITR | 3.3 | 5.3% | 1.3% | 1 | 0 |
| 2024-06-30 | ITR | 3.1 | 5.3% | 1.0% | 1 | 0 |
| 2024-03-31 | ITR | 2.9 | 3.0% | -1.3% | 2 | -0 |
| 2023-12-31 | DFP-ITR | 2.9 | 4.9% | 4.4% | 2 | 0 |
| 2023-09-30 | ITR | 2.9 | 4.1% | -0.8% | 2 | 0 |
| 2023-06-30 | ITR | 2.8 | 4.2% | -1.3% | 2 | 0 |
| 2023-03-31 | ITR | 2.6 | 1.4% | -2.4% | 2 | 0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [2.6, 2.8, 2.9, 2.9, 2.9, 3.1, 3.3, 3.3, 3.4, 3.7, 3.9]
  - title: EBIT margin %
    data: [1.4, 4.2, 4.1, 4.9, 3.0, 5.3, 5.3, 4.4, 4.2, 6.2, 6.5]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama PGMN3 --write
ii deepdive PGMN3 --save-obsidian
ii verdict PGMN3 --narrate --write
ii fv PGMN3
python -m analytics.fair_value_forward --ticker PGMN3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
