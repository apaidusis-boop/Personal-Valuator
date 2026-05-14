---
type: ticker_hub
ticker: RDOR3
market: br
sector: Healthcare
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# RDOR3 — Rede D'Or

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Healthcare` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 5.63, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 16.64 · P/B 3.97 · DY 12.3% · ROE 19.2% · ND/EBITDA 1.10 · Dividend streak 6

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\RDOR3.md` (cemetery archive)_

#### RDOR3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://ri.rededorsaoluiz.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **5**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=35.970001220703125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.19188 · DY=0.11873116083026136 · P/E=17.128572
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-16 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-23 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Distribuição de Juros Sob |
| 2026-03-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Habilitação Medicina |
| 2026-02-26 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação da Teleconferência d |
| 2026-01-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Fechamento do Acordo Atlâ |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RDOR3_FILING_2026-05-07.md` (cemetery archive)_

#### Filing dossier — [[RDOR3]] · 2026-05-07

**Trigger**: `cvm:comunicado` no dia `2026-05-07`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517476&numSequencia=1042182&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 35.72

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `16.65` |
| HOLD entre | `16.65` — `20.31` (consensus) |
| TRIM entre | `20.31` — `23.36` |
| **SELL acima de** | `23.36` |

_Método: `graham_number`. Consensus fair = R$20.31. Our fair (mais conservador) = R$16.65._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.19188` | `0.1654` | +13.8% |
| EPS | `2.09` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.4B (+3.3% QoQ, +10.7% YoY)
- EBIT 2.7B (+21.0% QoQ)
- Margem EBIT 19.1% vs 16.3% prior
- Lucro líquido 1.5B (+46.8% QoQ, +31.6% YoY)

**BS / cash**
- Equity 28.8B (+3.2% QoQ)
- Dívida total 42.9B (+12.9% QoQ)
- FCF proxy -4.2B (-105.0% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `graham_number` | 20.31 | 16.65 | 35.72 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-07` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:48+00:00 | `graham_number` | 20.31 | 16.65 | 37.74 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-16` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-16 · Filing 2026-04-16
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RDOR3_FILING_2026-04-16.md` (cemetery archive)_

#### Filing dossier — [[RDOR3]] · 2026-04-16

**Trigger**: `cvm:comunicado` no dia `2026-04-16`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505499&numSequencia=1030205&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 37.74

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `16.65` |
| HOLD entre | `16.65` — `20.31` (consensus) |
| TRIM entre | `20.31` — `23.36` |
| **SELL acima de** | `23.36` |

_Método: `graham_number`. Consensus fair = R$20.31. Our fair (mais conservador) = R$16.65._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20047002` | `0.1654` | +17.5% |
| EPS | `2.09` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.4B (+3.3% QoQ, +10.7% YoY)
- EBIT 2.7B (+21.0% QoQ)
- Margem EBIT 19.1% vs 16.3% prior
- Lucro líquido 1.5B (+46.8% QoQ, +31.6% YoY)

**BS / cash**
- Equity 28.8B (+3.2% QoQ)
- Dívida total 42.9B (+12.9% QoQ)
- FCF proxy -4.2B (-105.0% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:48+00:00 | `graham_number` | 20.31 | 16.65 | 37.74 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-16` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RDOR3.md` (cemetery archive)_

#### RDOR3 — RDOR3

#watchlist #br #healthcare

##### Links

- Sector: [[sectors/Healthcare|Healthcare]]
- Market: [[markets/BR|BR]]

##### Snapshot

- **Preço**: R$37.74  (2026-05-07)    _-6.47% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 43.0/100 (RISK)

##### Fundamentals

- P/E: 18.057417 | P/B: 4.3028164 | DY: 11.32%
- ROE: 20.05% | EPS: 2.09 | BVPS: 8.771
- Streak div: 6y | Aristocrat: None

##### Dividendos recentes

- 2026-03-27: R$0.1591
- 2025-12-19: R$3.6811
- 2025-09-24: R$0.2266
- 2025-06-17: R$0.2039
- 2025-03-27: R$0.1811

##### Eventos (SEC/CVM)

- **2026-04-16** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-03-23** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Distribuição de Juros Sob
- **2026-03-06** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Habilitação Medicina
- **2026-02-26** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação da Teleconferência d
- **2026-01-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Fechamento do Acordo Atlâ

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RDOR3 — peso 2.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RDOR3 — peso 1.7% |
| 2026-04-24 | XP | thesis | neutral | — | Visões mistas sobre RD devido ao ceticismo em relação aos riscos estruturais. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -20.45%
- **Drawdown 5y**: -41.01%
- **YTD**: -6.75%
- **YoY (1y)**: +19.81%
- **CAGR 3y**: +22.50%  |  **5y**: -8.84%  |  **10y**: n/a
- **Vol annual**: +30.87%
- **Sharpe 3y** (rf=4%): +0.54

###### Dividendos
- **DY 5y avg**: +4.07%
- **Div CAGR 5y**: +12.66%
- **Frequency**: semiannual
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$22.99B | R$6.08B | R$1.19B |
| 2023-12-31 | R$46.51B | R$7.39B | R$2.04B |
| 2024-12-31 | R$50.57B | R$9.90B | R$3.85B |
| 2025-12-31 | R$55.73B | R$12.12B | R$4.69B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "RDOR3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: RDOR3
    data: [33.7, 34.34, 36.74, 37.07, 37.78, 36.24, 35.32, 35.49, 35.38, 35.42, 34.93, 33.81, 33.61, 32.72, 32.44, 32.4, 35.9, 36.83, 37.32, 37.55, 39.36, 39.04, 39.1, 40.3, 41.71, 41.22, 41.54, 40.99, 40.21, 41.07, 42.26, 42.8, 43.78, 45.83, 45.19, 45.48, 46.63, 47.42, 44.12, 46.19, 40.43, 40.61, 40.99, 40.22, 40.45, 43.95, 42.73, 41.66, 41.3, 42.83, 43.47, 39.7, 38.41, 37.26, 37.02, 38.82, 37.85, 39.73, 41.4, 39.25, 37.86, 37.74, 40.35]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "RDOR3 — dividend history"
labels: ['2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [1.4595, 0.5038, 0.3693, 0.6477, 4.2927, 0.1591]
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
    data: [20.71, 18.51643, 17.774647, 18.259434, 18.173708, 18.173708, 18.042253, 18.042253, 17.71831, 18.099056, 17.793427, 18.183098, 18.94366, 18.057417]
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
    data: [21.68, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05, 20.05]
  - title: DY %
    data: [10.07, 10.83, 11.28, 11.03, 11.03, 11.03, 11.11, 11.11, 11.32, 11.13, 11.27, 11.03, 10.58, 11.32]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RDOR3_DOSSIE.md` (cemetery archive)_

#### 📑 RDOR3 — Rede D'Or

> Generated **2026-04-26** by `ii dossier RDOR3`. Cross-links: [[RDOR3]] · [[RDOR3]] · [[CONSTITUTION]]

##### TL;DR

RDOR3 negocia P/E 18.17 e P/B 4.41 com ROE 20.05% e DY excepcional de 11.03% (acima do floor 6%) com streak 6y. IC consensus BUY (high, 80%) — qualidade de líder hospitalar combinada com yield e ND/EBITDA controlado em 1.01× passa todos os critérios Graham excepto P/B. Achado-chave: DY 11% num healthcare é anómalo — provavelmente dividendo extraordinário pós-integração Sul América; validar que é recorrente antes de assumir como base DRIP.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.13  |  **BVPS**: 8.77
- **ROE**: 20.05%  |  **P/E**: 18.17  |  **P/B**: 4.41
- **DY**: 11.03%  |  **Streak div**: 6y  |  **Market cap**: R$ 85.26B
- **Last price**: BRL 38.71 (2026-04-24)  |  **YoY**: +25.2%

##### 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[RDOR3]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A RDOR3 é uma empresa de saúde que atende aos critérios clássicos de investimento de valor ajustados para a Selic alta, com um DY de 11.03%, ROE de 20.05% e dívida líquida/EBITDA de apenas 1.01x, além de ter mantido dividendos consistentes por seis anos.

**Key assumptions**:
1. A empresa continuará a gerar lucros acima da média do setor
2. Os níveis atuais de endividamento permanecerão estáveis ou diminuirão
3. O mercado de saúde no Brasil continuará crescendo e demandando serviços especializados oferecidos pela RDOR3
4. A empresa manterá seu histórico de pagamento de dividendos

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- Dividend streak interrompido
- P/B aumenta para mais de 6x
- Net Debt/EBITDA sobe acima de 3×

→ Vault: [[RDOR3]]

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

- **P/E = 18.17** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 18.17** passa.
- **P/B = 4.41** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **4.41** — verificar consistência com ROE.
- **DY = 11.03%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **11.03%** passa.
- **ROE = 20.05%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **20.05%** compounder-grade.
- **Graham Number ≈ R$ 20.50** vs preço **R$ 38.71** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 6y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **DY 11% pode ser não-recorrente** — provável evento extraordinário (M&A Sul América); base sustentável é provavelmente 4-6%. Trigger: dividendo trimestral próximo ano <60% do anualizado actual.
- 🟡 **Regulação operadoras de saúde / ANS** — pressão tarifária, judicialização e tetos podem comprimir margem. Trigger: notícia/release ANS sobre reajuste/limite (events table).
- 🟡 **Integração Sul América** — risco de execução do M&A; sinergias podem demorar. Trigger: gross margin YoY <-200bp em 2 trimestres.
- 🟡 **P/B 4.41 esticado** — único critério Graham falhado; pouca margem de segurança patrimonial. Trigger: `fundamentals.pb > 5.5` para alerta.
- 🟢 **Alavancagem baixa** — ND/EBITDA 1.01× dá flexibilidade financeira. Trigger: `fundamentals.net_debt_ebitda > 2.5` para alarme.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. IC BUY mas validar primeiro recorrência do DY 11% (pode ser one-off pós-Sul América). Entry weight prudente 4-5% como Tier-2 (líder healthcare, M&A risk). Pode chegar a 6-7% após confirmação de yield base sustentável >5%.

##### 7. Tracking triggers (auto-monitoring)

- **DY normalization** — `fundamentals.dy < 5%` em release seguinte → confirma yield 11% foi one-off.
- **ROE drop** — `fundamentals.roe < 15%` por 2 trimestres → invalida pilar qualidade.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 2.5` → integração mais cara que esperado.
- **Regulatory hit** — `events` com kind='fato_relevante' + ANS/regulatório → review imediato.
- **Conviction drop** — `conviction_scores.composite_score < 65` → flag review.

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
*Generated by `ii dossier RDOR3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RDOR3 — peso 2.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RDOR3 — peso 1.7% |
| 2026-04-24 | XP | thesis | neutral | — | Visões mistas sobre RD devido ao ceticismo em relação aos riscos estruturais. |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RDOR3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — RDOR3

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=2 | HOLD=3 | AVOID=0  
**Avg conviction majority**: 6.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: small)

**Rationale**:
- ROE acima de 15%
- Dividendos consistentes
- P/B moderado

**Key risk**: Possível aumento da dívida e queda na geração de caixa livre

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- DY de 11.03% atrativo
- ROE acima da média
- Net Debt/EBITDA estável e baixo

**Key risk**: Aumento significativo dos custos operacionais ou queda na geração de caixa

###### 🟡 Nassim Taleb — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- DY atrativo
- ROE forte
- Net Debt/EBITDA saudável

**Key risk**: Aumento da dívida ou interrupção dos dividendos

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: small)

**Rationale**:
- DY de 11.03% e ROE sólido
- Dívida controlada com PB baixo
- Histórico consistente de dividendos

**Key risk**: Aumento da dívida ou queda acentuada no fluxo de caixa

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- DY de 11.03% atrativo
- ROE acima da média
- Net Debt/EBITDA estável e baixo

**Key risk**: Aumento significativo do endividamento ou interrupção dos dividendos

##### 📊 Context provided

```
TICKER: BR:RDOR3

FUNDAMENTALS LATEST:
  pe: 18.330145
  pb: 4.367803
  dy: 11.15%
  roe: 20.05%
  net_debt_ebitda: 1.0080974194282264
  intangible_pct_assets: 14.8%   (goodwill $12.5B + intangibles $3.3B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=14.4 ebit=2.7 ni=1.5 em%=19.1 debt=43 fcf=-4.2
  2025-06-30: rev=14.0 ebit=2.3 ni=1.0 em%=16.3 debt=38 fcf=-2.0
  2025-03-31: rev=13.0 ebit=2.2 ni=1.1 em%=17.0 debt=38 fcf=2.7
  2024-12-31: rev=12.8 ebit=1.8 ni=0.9 em%=13.7 debt=39 fcf=-0.4
  2024-09-30: rev=13.0 ebit=2.2 ni=1.2 em%=16.8 debt=36 fcf=3.5
  2024-06-30: rev=12.5 ebit=1.8 ni=1.0 em%=14.5 debt=36 fcf=-0.2

VAULT THESIS:
**Core thesis (2026-04-25)**: A RDOR3 é uma empresa de saúde que atende aos critérios clássicos de investimento de valor ajustados para a Selic alta, com um DY de 11.03%, ROE de 20.05% e dívida líquida/EBITDA de apenas 1.01x, além de ter mantido dividendos consistentes por seis anos.

**Key assumptions**:
1. A empresa continuará a gerar lucros acima da média do setor
2. Os níveis atuais de endividamento permanecerão estáveis ou diminuirão
3. O mercado de saúde no Brasil continuará crescendo e demandando serviços especializados oferecidos pela RDOR3
4. A empresa manterá seu histórico de pagamento de dividendos

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- Dividend streak interrompido
- P/B aumenta para mais de 6x
- Net Debt/EBITDA sobe acima de 3×

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil party asks court to halt rare earths miner’s sale - Mining.com [Sat, 25 Ap]
    Brent Crude Oil $ 104.4 / bbl  -4.21%. Palladium $ 1496.5 / ozt  5.39%. Crude Oil $ 101.85 / bbl  -3.06%. Aluminum Futures $ 3314.25 / ton  -1.21%. Micro Silver Futures $ 75.48 / ozt  7.54%. Platinum 
  - Brazil party asks court to halt rare earths miner’s sale - Bitget [Sat, 25 Ap]
    Brazil party asks court to halt rare earths miner’s sale. # Brazil party asks court to halt rare earths miner’s sale. Left-wi
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RDOR3 — peso 2.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RDOR3 — peso 1.7% |
| 2026-04-24 | XP | thesis | neutral | — | Visões mistas sobre RD devido ao ceticismo em relação aos riscos estruturais. |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RDOR3_RI.md` (cemetery archive)_

#### RDOR3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+21.0%**
- ⬆️ **QOQ** `net_income`: **+46.8%**
- ⬇️ **QOQ** `fco`: **-450.8%**
- ⬇️ **QOQ** `fcf_proxy`: **-105.0%**
- ⬆️ **YOY** `revenue`: **+10.7%**
- ⬆️ **YOY** `ebit`: **+25.7%**
- ⬆️ **YOY** `net_income`: **+31.7%**
- ⬇️ **YOY** `fco`: **-180.9%**
- ⬇️ **YOY** `fcf_proxy`: **-218.6%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 14.4 mi | R$ 14.0 mi | +3.3% |
| `ebit` | R$ 2.7 mi | R$ 2.3 mi | +21.0% |
| `net_income` | R$ 1.5 mi | R$ 1.0 mi | +46.8% |
| `debt_total` | R$ 42.9 mi | R$ 38.0 mi | +12.9% |
| `fco` | R$ -2.3 mi | R$ 0.6 mi | -450.8% |
| `fcf_proxy` | R$ -4.2 mi | R$ -2.0 mi | -105.0% |
| `gross_margin` | 23.3% | 20.9% | +2.4pp |
| `ebit_margin` | 19.1% | 16.3% | +2.8pp |
| `net_margin` | 10.7% | 7.5% | +3.2pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 14.4 mi | R$ 13.0 mi | +10.7% |
| `ebit` | R$ 2.7 mi | R$ 2.2 mi | +25.7% |
| `net_income` | R$ 1.5 mi | R$ 1.2 mi | +31.7% |
| `debt_total` | R$ 42.9 mi | R$ 35.7 mi | +20.1% |
| `fco` | R$ -2.3 mi | R$ 2.8 mi | -180.9% |
| `fcf_proxy` | R$ -4.2 mi | R$ 3.5 mi | -218.6% |
| `gross_margin` | 23.3% | 18.8% | +4.6pp |
| `ebit_margin` | 19.1% | 16.8% | +2.3pp |
| `net_margin` | 10.7% | 9.0% | +1.7pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 14.4 | 19.1% | 10.7% | 43 | -2 |
| 2025-06-30 | ITR | 14.0 | 16.3% | 7.5% | 38 | 1 |
| 2025-03-31 | ITR | 13.0 | 17.0% | 8.2% | 38 | 2 |
| 2024-12-31 | DFP-ITR | 12.8 | 13.7% | 7.3% | 39 | 2 |
| 2024-09-30 | ITR | 13.0 | 16.8% | 9.0% | 36 | 3 |
| 2024-06-30 | ITR | 12.5 | 14.5% | 8.0% | 36 | 1 |
| 2024-03-31 | ITR | 12.2 | 13.8% | 6.9% | 34 | 1 |
| 2023-12-31 | DFP-ITR | 11.8 | 13.2% | 6.7% | 35 | -0 |
| 2023-09-30 | ITR | 11.8 | 12.6% | 5.8% | 34 | 1 |
| 2023-06-30 | ITR | 11.6 | 12.0% | 2.7% | 32 | -0 |
| 2023-03-31 | ITR | 11.2 | 10.0% | 2.8% | 33 | 0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [11.2, 11.6, 11.8, 11.8, 12.2, 12.5, 13.0, 12.8, 13.0, 14.0, 14.4]
  - title: EBIT margin %
    data: [10.0, 12.0, 12.6, 13.2, 13.8, 14.5, 16.8, 13.7, 17.0, 16.3, 19.1]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama RDOR3 --write
ii deepdive RDOR3 --save-obsidian
ii verdict RDOR3 --narrate --write
ii fv RDOR3
python -m analytics.fair_value_forward --ticker RDOR3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
