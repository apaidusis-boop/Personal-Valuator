---
type: ticker_hub
ticker: EQTL3
market: br
sector: Utilities
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# EQTL3 — Equatorial

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Utilities` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 3.3, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 40.89 · P/B 1.92 · DY 4.0% · ROE 7.0% · ND/EBITDA 3.87 · Dividend streak 18

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\EQTL3.md` (now in cemetery)_

#### EQTL3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.equatorialenergia.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **24**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=41.52000045776367
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.06985 · DY=0.03813326065857366 · P/E=43.25
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Resultado sobre proposta  |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Release Operacional - 1t2 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reajuste Tarifário - Equa |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-15 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional 4T25 |

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
_source: `dossiers\EQTL3_FILING_2026-05-08.md` (now in cemetery)_

#### Filing dossier — [[EQTL3]] · 2026-05-08

**Trigger**: `cvm:fato_relevante` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1519278&numSequencia=1043984&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 40.43

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `16.40` |
| HOLD entre | `16.40` — `21.03` (consensus) |
| TRIM entre | `21.03` — `24.18` |
| **SELL acima de** | `24.18` |

_Método: `graham_number`. Consensus fair = R$21.03. Our fair (mais conservador) = R$16.40._

##### 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06985` | `0.1309` | +46.6% |
| EPS | `0.96` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.1B (+10.6% QoQ, +14.4% YoY)
- EBIT 2.4B (-19.3% QoQ)
- Margem EBIT 16.9% vs 23.2% prior
- Lucro líquido 609.8M (-52.7% QoQ, -38.4% YoY)

**BS / cash**
- Equity 32.8B (+2.1% QoQ)
- Dívida total 62.4B (+13.2% QoQ)
- FCF proxy -4.7B (-784.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 21.03 | 16.40 | 40.43 | SELL | single_source | `filing:cvm:fato_relevante:2026-05-08` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 21.03 | 16.40 | 42.31 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 21.03 | 16.40 | 42.31 | SELL | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `graham_number` | 21.03 | 16.40 | 42.31 | SELL | single_source | `extend_2026-05-09` |
| 2026-05-08T19:20:39+00:00 | `graham_number` | 21.03 | 16.40 | 42.20 | SELL | single_source | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Filing 2026-04-30
_source: `dossiers\EQTL3_FILING_2026-04-30.md` (now in cemetery)_

#### Filing dossier — [[EQTL3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513370&numSequencia=1038076&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 42.20

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `16.40` |
| HOLD entre | `16.40` — `21.03` (consensus) |
| TRIM entre | `21.03` — `24.18` |
| **SELL acima de** | `24.18` |

_Método: `graham_number`. Consensus fair = R$21.03. Our fair (mais conservador) = R$16.40._

##### 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06985` | `0.1309` | +46.6% |
| EPS | `0.96` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.1B (+10.6% QoQ, +14.4% YoY)
- EBIT 2.4B (-19.3% QoQ)
- Margem EBIT 16.9% vs 23.2% prior
- Lucro líquido 609.8M (-52.7% QoQ, -38.4% YoY)

**BS / cash**
- Equity 32.8B (+2.1% QoQ)
- Dívida total 62.4B (+13.2% QoQ)
- FCF proxy -4.7B (-784.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:39+00:00 | `graham_number` | 21.03 | 16.40 | 42.20 | SELL | single_source | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `tickers\EQTL3.md` (now in cemetery)_

#### EQTL3 — EQTL3

#watchlist #br #utilities

##### Links

- Sector: [[sectors/Utilities|Utilities]]
- Market: [[markets/BR|BR]]
- Peers: [[ALUP11]] · [[AXIA7]] · [[CMIG4]] · [[CPLE3]] · [[CSMG3]]

##### Snapshot

- **Preço**: R$42.20  (2026-05-07)    _-3.39% 1d_
- **Screen**: 0.2  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 35.0/100 (RISK)

##### Fundamentals

- P/E: 43.958336 | P/B: 2.061755 | DY: 3.75%
- ROE: 6.98% | EPS: 0.96 | BVPS: 20.468
- Streak div: 18y | Aristocrat: None

##### Dividendos recentes

- 2025-12-30: R$0.1333
- 2025-11-06: R$1.4500
- 2025-05-02: R$0.7002
- 2025-01-14: R$0.0891
- 2024-05-02: R$0.4472

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Resultado sobre proposta 
- **2026-04-29** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Release Operacional - 1t2
- **2026-04-29** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Reajuste Tarifário - Equa
- **2026-04-22** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-04-15** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Institucional 4T25

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] EQTL3 — peso 6.0% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] EQTL3 — peso 8.0% |
| 2026-04-24 | XP | catalyst | bull | — | Equatorial aumentada +2% no Equity Brazil (mais descontada que Sabesp). |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -6.95%
- **Drawdown 5y**: -6.95%
- **YTD**: +10.18%
- **YoY (1y)**: +17.78%
- **CAGR 3y**: +15.39%  |  **5y**: +11.51%  |  **10y**: +16.99%
- **Vol annual**: +24.21%
- **Sharpe 3y** (rf=4%): +0.46

###### Dividendos
- **DY 5y avg**: +2.86%
- **Div CAGR 5y**: +6.61%
- **Frequency**: irregular
- **Streak** (sem cortes): 2 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$26.22B | R$7.17B | R$1.37B |
| 2023-12-31 | R$39.49B | R$9.72B | R$2.08B |
| 2024-12-31 | R$41.56B | R$9.52B | R$2.81B |
| 2025-12-31 | R$49.25B | R$10.57B | R$1.68B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "EQTL3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: EQTL3
    data: [36.81, 37.18, 37.31, 36.47, 36.59, 36.68, 36.4, 36.64, 36.0, 35.96, 36.07, 34.44, 34.36, 33.93, 33.5, 34.33, 35.14, 35.68, 35.03, 35.65, 36.57, 35.84, 36.45, 36.25, 36.58, 36.73, 36.25, 35.29, 35.26, 36.5, 37.1, 36.81, 38.55, 39.12, 39.26, 38.75, 39.76, 41.25, 38.5, 38.98, 37.6, 38.5, 38.25, 37.33, 37.47, 40.91, 40.82, 40.26, 41.38, 40.85, 42.36, 41.7, 40.47, 40.15, 40.13, 41.17, 39.6, 40.46, 44.77, 45.26, 43.92, 41.7, 43.68]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "EQTL3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
series:
  - title: Dividends
    data: [0.1845, 0.1206, 0.2403, 0.1885, 0.3174, 0.7143, 0.6349, 0.3476, 0.4472, 2.3726]
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
    data: [33.79, 46.937504, 45.75, 45.947918, 45.947918, 45.947918, 45.197918, 44.416668, 43.4375, 44.083336, 43.802082, 44.71875, 45.5, 43.958336]
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
    data: [5.92, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98, 6.98]
  - title: DY %
    data: [5.07, 5.07, 5.2, 5.18, 5.18, 5.18, 5.26, 5.36, 5.48, 5.4, 3.77, 3.69, 3.62, 3.75]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\EQTL3_DOSSIE.md` (now in cemetery)_

#### 📑 EQTL3 — Equatorial

> Generated **2026-04-26** by `ii dossier EQTL3`. Cross-links: [[EQTL3]] · [[EQTL3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

EQTL3 negocia a P/E esticado de 45.95 com DY apenas 5.18% e ROE fraco de 6.98%, apesar de streak impressionante de 18 anos. Synthetic IC veredicto **AVOID** (high confidence, 80% consenso) e composite conviction 65. Achado central: histórico de excelência em M&A de distribuidoras já não está reflectido em retorno actual sobre capital — múltiplos premium sem justificativa em ROE, classic value trap em utility growth.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.96  |  **BVPS**: 20.47
- **ROE**: 6.98%  |  **P/E**: 45.95  |  **P/B**: 2.16
- **DY**: 5.18%  |  **Streak div**: 18y  |  **Market cap**: R$ 55.50B
- **Last price**: BRL 44.11 (2026-04-24)  |  **YoY**: +24.4%

##### 2. Synthetic IC

**🏛️ AVOID** (high confidence, 80.0% consensus)

→ Detalhe: [[EQTL3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A EQTL3 opera no setor de utilities e apresenta um histórico sólido de dividendos, com 18 anos ininterruptos. Apesar disso, a empresa não atende aos critérios estritos da filosofia de investimento value, especialmente em relação ao ROE (6.98%) e ao Dividend Yield (5.18%), que estão abaixo dos requisitos mínimos.

**Key assumptions**:
1. A taxa Selic permanecerá elevada por um período prolongado, mantendo o ambiente desafiador para empresas com baixos retornos sobre capital empregado e dividendos mais baixos
2. A empresa não será capaz de aumentar significativamente seu ROE nos próximos 12-24 meses
3. O Dividend Yield permanecerá abaixo dos 6% por um período prolongado, refletindo a política atual da companhia em relação aos dividendos e à alocação do capital
4

→ Vault: [[EQTL3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **65** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 50 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 45.95** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 45.95** fora do screen.
- **P/B = 2.16** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.16** — verificar consistência com ROE.
- **DY = 5.18%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **5.18%** abaixo do floor — DRIP não-óbvio.
- **ROE = 6.98%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **6.98%** abaixo do critério.
- **Graham Number ≈ R$ 21.03** vs preço **R$ 44.11** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **P/E premium injustificado** — 45.95 contra ROE 6.98% sinaliza overvaluation severa. Trigger: `fundamentals.pe` > 30 mantém-se enquanto `roe` < 10%.
- 🔴 **ROE estrutural baixo** — bem abaixo do mínimo 15% para utility BR. Trigger: `fundamentals.roe` < 10% por 4 trimestres consecutivos.
- 🟡 **DY abaixo do mínimo** — 5.18% < 6% requerido. Trigger: `fundamentals.dy` < 6% (já actual; manter sob watch).
- 🟡 **Revisão tarifária ANEEL** — múltiplas distribuidoras (CEMAR, CELPA, CEPISA, EQTL Goiás) entram em ciclos diferentes. Trigger: anúncio ANEEL de revisão tarifária com WACC reduzido.
- 🟡 **Capex M&A intensivo** — modelo de roll-up de distribuidoras requer alavancagem contínua. Trigger: `fundamentals.net_debt_ebitda` > 4x.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira; veredicto **AVOID** torna entry trigger restritivo. Re-entry só se P/E < 18 **e** ROE recuperar para ≥ 12% **e** DY ≥ 6% (combinação simultânea). Weight prudente máximo 3-4% se as condições convergirem. Cash exclusivo BRL (BR isolation), sem deploy DRIP enquanto múltiplos forem premium.

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe` ≥ 12% por 2 trimestres consecutivos.
- **P/E re-rating** — `fundamentals.pe` < 18 (sai de zona AVOID).
- **DY ≥ 6%** — `fundamentals.dy` ≥ 6% sustentado 2 trimestres.
- **Streak preservado** — `fundamentals.dividend_streak_years` < 18 sinaliza corte (red flag imediato).
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 4x.

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
*Generated by `ii dossier EQTL3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] EQTL3 — peso 6.0% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] EQTL3 — peso 8.0% |
| 2026-04-24 | XP | catalyst | bull | — | Equatorial aumentada +2% no Equity Brazil (mais descontada que Sabesp). |

#### — · IC Debate (synthetic)
_source: `tickers\EQTL3_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — EQTL3

**Committee verdict**: **AVOID** (high confidence, 80% consensus)  
**Votes**: BUY=0 | HOLD=1 | AVOID=4  
**Avg conviction majority**: 9.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 10/10, size: none)

**Rationale**:
- ROE abaixo dos padrões desejados
- Geração de caixa livre instável e negativa recentemente
- Ambiente macroeconômico desafiador para utilities

**Key risk**: Taxa Selic elevada impactando significativamente os retornos sobre capital empregado

###### 🔴 Stan Druckenmiller — **AVOID** (conv 8/10, size: none)

**Rationale**:
- ROE baixo e não deve melhorar nos próximos 12-24 meses
- Dividend yield abaixo dos requisitos mínimos
- Ambiente macro desafiador com taxas Selic elevadas

**Key risk**: Taxa Selic permanece alta por mais tempo do que o esperado, afetando a rentabilidade

###### 🔴 Nassim Taleb — **AVOID** (conv 10/10, size: none)

**Rationale**:
- ROE abaixo dos requisitos
- Dividend yield não atrativo
- Falta de anti-fragilidade

**Key risk**: Leverage e baixo retorno sobre capital empregado

###### 🔴 Seth Klarman — **AVOID** (conv 10/10, size: none)

**Rationale**:
- ROE baixo e PE alto
- Dividend yield abaixo do desejado
- FCF negativo

**Key risk**: Perda permanente de capital devido a FCF negativo e dívida elevada

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Dividend yield abaixo dos requisitos mínimos
- ROE fraco e não deve melhorar nos próximos 12-24 meses
- Ambiente desafiador com taxas Selic elevadas

**Key risk**: Taxa Selic permanece alta por mais tempo do que o esperado, pressionando os lucros

##### 📊 Context provided

```
TICKER: BR:EQTL3

FUNDAMENTALS LATEST:
  pe: 45.947918
  pb: 2.1550713
  dy: 5.18%
  roe: 6.98%
  net_debt_ebitda: 3.873966854708453

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=14.1 ebit=2.4 ni=0.6 em%=16.9 debt=62 fcf=-4.7
  2025-06-30: rev=12.8 ebit=3.0 ni=1.3 em%=23.2 debt=55 fcf=0.7
  2025-03-31: rev=11.7 ebit=2.4 ni=0.7 em%=20.5 debt=54 fcf=-0.4
  2024-12-31: rev=12.6 ebit=2.2 ni=1.5 em%=17.2 debt=56 fcf=-1.4
  2024-09-30: rev=12.4 ebit=2.5 ni=1.0 em%=20.6 debt=52 fcf=-6.4
  2024-06-30: rev=10.5 ebit=1.9 ni=0.7 em%=18.5 debt=48 fcf=-3.7

VAULT THESIS:
**Core thesis (2026-04-25)**: A EQTL3 opera no setor de utilities e apresenta um histórico sólido de dividendos, com 18 anos ininterruptos. Apesar disso, a empresa não atende aos critérios estritos da filosofia de investimento value, especialmente em relação ao ROE (6.98%) e ao Dividend Yield (5.18%), que estão abaixo dos requisitos mínimos.

**Key assumptions**:
1. A taxa Selic permanecerá elevada por um período prolongado, mantendo o ambiente desafiador para empresas com baixos retornos sobre capital empregado e dividendos mais baixos
2. A empresa não será capaz de aumentar significativamente seu ROE nos próximos 12-24 meses
3. O Dividend Yield permanecerá abaixo dos 6% por um período prolongado, refletindo a política atual da companhia em relação aos dividendos e à alocação do capital
4

RECENT MATERIAL NEWS (last 14d via Tavily):
  - EQT and data center builder EdgeConneX launch AI investing strategy - PitchBook [Tue, 21 Ap]
    # EQT and data center builder EdgeConneX launch AI investing strategy. EQT is partnering with one of its portfolio companies to launch a digital infrastructure investing platform, adding to the mounta
  - EQT launches AI infrastructure strategy - Private Equity Wire [Wed, 22 Ap]
    ## FORWARD FEATURES CALENDAR. ## NEWSLETTER. Sign up to our free newsletter. ## SIGN UP NOW. ***EQT has unveiled a dedicated AI Infrastructure strategy aimed at investing in the physical back
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=3 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] EQTL3 — peso 6.0% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] EQTL3 — peso 8.0% |
| 2026-04-24 | XP | catalyst | bull | — | Equatorial aumentada +2% no Equity Brazil (mais descontada que Sabesp). |

#### — · RI / disclosure
_source: `tickers\EQTL3_RI.md` (now in cemetery)_

#### EQTL3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `revenue`: **+10.5%**
- ⬇️ **QOQ** `net_income`: **-52.7%**
- ⬇️ **QOQ** `fcf_proxy`: **-784.3%**
- ⬇️ **QOQ** `ebit_margin`: **-6.3pp**
- ⬇️ **QOQ** `net_margin`: **-5.8pp**
- ⬆️ **YOY** `revenue`: **+14.4%**
- ⬇️ **YOY** `net_income`: **-38.4%**
- ⬇️ **YOY** `fco`: **-31.1%**
- ⬆️ **YOY** `fcf_proxy`: **+26.8%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 14.1 mi | R$ 12.8 mi | +10.5% |
| `ebit` | R$ 2.4 mi | R$ 3.0 mi | -19.3% |
| `net_income` | R$ 0.6 mi | R$ 1.3 mi | -52.7% |
| `debt_total` | R$ 62.4 mi | R$ 55.1 mi | +13.2% |
| `fco` | R$ 1.0 mi | R$ 0.9 mi | +14.8% |
| `fcf_proxy` | R$ -4.7 mi | R$ 0.7 mi | -784.3% |
| `gross_margin` | 24.6% | 26.5% | -1.8pp |
| `ebit_margin` | 16.9% | 23.2% | -6.3pp |
| `net_margin` | 4.3% | 10.1% | -5.8pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 14.1 mi | R$ 12.4 mi | +14.4% |
| `ebit` | R$ 2.4 mi | R$ 2.5 mi | -5.9% |
| `net_income` | R$ 0.6 mi | R$ 1.0 mi | -38.4% |
| `debt_total` | R$ 62.4 mi | R$ 51.7 mi | +20.6% |
| `fco` | R$ 1.0 mi | R$ 1.5 mi | -31.1% |
| `fcf_proxy` | R$ -4.7 mi | R$ -6.4 mi | +26.8% |
| `gross_margin` | 24.6% | 28.0% | -3.3pp |
| `ebit_margin` | 16.9% | 20.6% | -3.6pp |
| `net_margin` | 4.3% | 8.0% | -3.7pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 14.1 | 16.9% | 4.3% | 62 | 1 |
| 2025-06-30 | ITR | 12.8 | 23.2% | 10.1% | 55 | 1 |
| 2025-03-31 | ITR | 11.7 | 20.5% | 6.0% | 54 | 1 |
| 2024-12-31 | DFP-ITR | 12.6 | 17.2% | 11.9% | 56 | 1 |
| 2024-09-30 | ITR | 12.4 | 20.6% | 8.0% | 52 | 1 |
| 2024-06-30 | ITR | 10.5 | 18.5% | 6.6% | 48 | 1 |
| 2024-03-31 | ITR | 9.9 | 20.1% | 5.9% | 44 | 1 |
| 2023-12-31 | DFP-ITR | 11.2 | 15.7% | 8.8% | 46 | 1 |
| 2023-09-30 | ITR | 10.4 | 21.2% | 9.0% | 45 | 1 |
| 2023-06-30 | ITR | 9.2 | 19.6% | 7.3% | 43 | 1 |
| 2023-03-31 | ITR | 10.2 | 18.4% | 2.8% | 42 | 1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [10.2, 9.2, 10.4, 11.2, 9.9, 10.5, 12.4, 12.6, 11.7, 12.8, 14.1]
  - title: EBIT margin %
    data: [18.4, 19.6, 21.2, 15.7, 20.1, 18.5, 20.6, 17.2, 20.5, 23.2, 16.9]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama EQTL3 --write
ii deepdive EQTL3 --save-obsidian
ii verdict EQTL3 --narrate --write
ii fv EQTL3
python -m analytics.fair_value_forward --ticker EQTL3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
