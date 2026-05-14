---
type: ticker_hub
ticker: RENT3
market: br
sector: Industrials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# RENT3 — Localiza

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Industrials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 4.7, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 20.84 · P/B 1.85 · DY 4.8% · ROE 8.5% · ND/EBITDA 3.98 · Dividend streak 20

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\RENT3.md` (cemetery archive)_

#### RENT3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.localiza.com/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **14**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=47.02000045776367
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.0853 · DY=0.04379319395901885 · P/E=22.714977
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-28 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Juros sobre o capital pró |
| 2026-03-25 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-24 | fato_relevante | cvm | Juros sobre o Capital Próprio |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RENT3_FILING_2026-05-05.md` (cemetery archive)_

#### Filing dossier — [[RENT3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515858&numSequencia=1040564&numVersao=2>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 44.88

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `24.06` |
| HOLD entre | `24.06` — `32.96` (consensus) |
| TRIM entre | `32.96` — `37.90` |
| **SELL acima de** | `37.90` |

_Método: `graham_number`. Consensus fair = R$32.96. Our fair (mais conservador) = R$24.06._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.0853` | `0.0684` | +19.8% |
| EPS | `2.07` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 10.7B (+8.4% QoQ, +10.8% YoY)
- EBIT 1.3B (-34.0% QoQ)
- Margem EBIT 12.4% vs 20.4% prior
- Lucro líquido 258.1M (+253.1% QoQ, -68.2% YoY)

**BS / cash**
- Equity 25.1B (-1.4% QoQ)
- Dívida total 43.9B (+5.7% QoQ)
- FCF proxy -298.6M (-119.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `graham_number` | 32.96 | 24.06 | 44.88 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:49+00:00 | `graham_number` | 30.39 | 22.18 | 46.35 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-29 · Filing 2026-04-29
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RENT3_FILING_2026-04-29.md` (cemetery archive)_

#### Filing dossier — [[RENT3]] · 2026-04-29

**Trigger**: `cvm:comunicado` no dia `2026-04-29`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1511170&numSequencia=1035876&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 46.35

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `22.18` |
| HOLD entre | `22.18` — `30.39` (consensus) |
| TRIM entre | `30.39` — `34.95` |
| **SELL acima de** | `34.95` |

_Método: `graham_number`. Consensus fair = R$30.39. Our fair (mais conservador) = R$22.18._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.07211` | `0.0684` | +5.1% |
| EPS | `1.76` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 10.7B (+8.4% QoQ, +10.8% YoY)
- EBIT 1.3B (-34.0% QoQ)
- Margem EBIT 12.4% vs 20.4% prior
- Lucro líquido 258.1M (+253.1% QoQ, -68.2% YoY)

**BS / cash**
- Equity 25.1B (-1.4% QoQ)
- Dívida total 43.9B (+5.7% QoQ)
- FCF proxy -298.6M (-119.3% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:49+00:00 | `graham_number` | 30.39 | 22.18 | 46.35 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RENT3.md` (cemetery archive)_

#### RENT3 — RENT3

#watchlist #br #industrials

##### Links

- Sector: [[sectors/Industrials|Industrials]]
- Market: [[markets/BR|BR]]
- Peers: [[MOTV3]] · [[POMO3]] · [[RAPT4]] · [[SIMH3]] · [[TUPY3]]

##### Snapshot

- **Preço**: R$46.35  (2026-05-07)    _-2.73% 1d_
- **Screen**: 0.2  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 30.0/100 (RISK)

##### Fundamentals

- P/E: 26.335226 | P/B: 1.9876494 | DY: 4.44%
- ROE: 7.21% | EPS: 1.76 | BVPS: 23.319
- Streak div: 20y | Aristocrat: None

##### Dividendos recentes

- 2026-03-30: R$0.5221
- 2025-12-18: R$0.5155
- 2025-09-26: R$0.5154
- 2025-06-30: R$0.5062
- 2025-03-27: R$0.4564

##### Eventos (SEC/CVM)

- **2026-04-29** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-04-22** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-03-28** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Juros sobre o capital pró
- **2026-03-25** `comunicado` — Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) | D
- **2026-03-24** `fato_relevante` — Juros sobre o Capital Próprio

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RENT3 — peso 3.4% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RENT3 — peso 6.2% |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -12.27%
- **Drawdown 5y**: -36.73%
- **YTD**: +6.70%
- **YoY (1y)**: +10.12%
- **CAGR 3y**: -7.23%  |  **5y**: -5.93%  |  **10y**: +16.05%
- **Vol annual**: +36.95%
- **Sharpe 3y** (rf=4%): -0.30

###### Dividendos
- **DY 5y avg**: +3.03%
- **Div CAGR 5y**: +45.86%
- **Frequency**: quarterly
- **Streak** (sem cortes): 5 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$17.78B | R$7.54B | R$1.84B |
| 2023-12-31 | R$28.90B | R$11.62B | R$1.81B |
| 2024-12-31 | R$37.27B | R$13.32B | R$1.81B |
| 2025-12-31 | R$41.78B | R$15.34B | R$1.88B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "RENT3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: RENT3
    data: [43.9, 39.71, 41.7, 40.85, 42.96, 44.2, 44.0, 44.6, 43.51, 40.52, 39.18, 38.25, 37.0, 35.8, 35.17, 34.37, 35.65, 34.8, 33.8, 34.62, 35.84, 37.0, 37.34, 39.1, 39.13, 40.08, 38.78, 36.77, 35.87, 36.97, 38.75, 39.24, 41.57, 43.25, 43.17, 42.97, 45.25, 49.6, 45.99, 45.3, 43.43, 43.57, 43.96, 41.87, 40.81, 44.75, 48.13, 50.06, 50.49, 51.3, 52.05, 51.73, 45.83, 45.17, 44.11, 46.44, 45.02, 47.14, 49.0, 50.78, 49.39, 45.2, 47.65]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "RENT3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.2686, 0.2339, 0.2558, 0.3925, 0.3451, 0.4405, 1.3086, 1.5026, 1.5849, 1.9934, 0.5221]
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
    data: [30.57, 29.53409, 28.0625, 28.005682, 28.005682, 28.005682, 27.454546, 26.880682, 25.681818, 26.085228, 25.556818, 26.079546, 27.073864, 26.335226]
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
    data: [7.34, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21, 7.21]
  - title: DY %
    data: [4.04, 3.96, 4.17, 4.18, 4.18, 4.18, 4.26, 4.35, 4.56, 4.49, 4.58, 4.49, 4.32, 4.44]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RENT3_DOSSIE.md` (cemetery archive)_

#### 📑 RENT3 — Localiza

> Generated **2026-04-26** by `ii dossier RENT3`. Cross-links: [[RENT3]] · [[RENT3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

RENT3 negocia P/E elevado de 28.01 e P/B 2.11 com ROE apenas 7.21% (abaixo dos 15% requeridos), DY 4.18% e streak excepcional de 20 anos. IC consensus HOLD (medium, 60%) — divergência reflecte trade-off entre track record DRIP impecável e ROE actualmente comprimido pelo ciclo de juros (custo de carry da frota). Achado-chave: Localiza é classic compounder de longo prazo mas a janela actual (Selic alta + CAPEX renovação frota) pressiona ROE; entrada deve esperar ROE >12%.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.76  |  **BVPS**: 23.32
- **ROE**: 7.21%  |  **P/E**: 28.01  |  **P/B**: 2.11
- **DY**: 4.18%  |  **Streak div**: 20y  |  **Market cap**: R$ 51.98B
- **Last price**: BRL 49.29 (2026-04-24)  |  **YoY**: +18.5%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[RENT3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A RENT3 é uma empresa de capital intensivo no setor industrial com um histórico robusto de pagamento de dividendos por mais de duas décadas. Apesar do P/E alto e ROE abaixo da meta, a relação P/B está dentro de limites aceitáveis e o DY oferece atratividade para investidores em busca de renda.

**Key assumptions**:
1. A empresa mantém seu histórico de dividendos por mais dois anos consecutivos
2. O ROE se recupera acima dos 15% nos próximos quatro trimestres
3. A relação dívida líquida/EBITDA permanece abaixo de 3× no próximo ano
4. A Selic mantém-se estável ou em queda, facilitando a gestão da dívida

**Disconfirmation triggers**:
- ROE cai abaixo de 7% por dois trimestres consecutivos
- Dividendos não são pagos nos próximos dois trimestres
- A relação dívida

→ Vault: [[RENT3]]

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

- **P/E = 28.01** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 28.01** fora do screen.
- **P/B = 2.11** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.11** — verificar consistência com ROE.
- **DY = 4.18%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.18%** abaixo do floor — DRIP não-óbvio.
- **ROE = 7.21%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **7.21%** abaixo do critério.
- **Graham Number ≈ R$ 30.39** vs preço **R$ 49.29** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 20y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **ROE comprimido pelo ciclo** — 7.21% vs floor 15%; carry de frota com Selic alta e CAPEX renovação destroem retorno. Trigger: `fundamentals.roe < 6%` em release seguinte → erosão estrutural.
- 🟡 **CAPEX frota intensivo** — modelo capital-intensive amplifica sensibilidade a juros e preços de carros. Trigger: dívida líquida YoY >+25% em 2 trimestres.
- 🟡 **Ciclo automotivo / preço de carros usados** — desvalorização da frota afecta resultado. Trigger: receita de seminovos YoY <-15% em release.
- 🟡 **P/E 28 esticado para ROE 7%** — múltiplo precifica recuperação de margem; risco se demora. Trigger: `fundamentals.pe > 35` para alerta de overvaluation.
- 🟢 **Streak 20y impecável** — track record DRIP class A; risco de corte muito baixo. Trigger: dividendo zero em qualquer trimestre = sinal estrutural grave.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Compounder de qualidade mas valuation actual desfavorável (P/E 28 / ROE 7%). Entry trigger: ROE recovery >12% em 2 trimestres OU pullback que normalize P/E <20×. Weight prudente 4-5% como Tier-2 pela qualidade do business e streak DRIP.

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → entry zone activa.
- **PE compression** — `fundamentals.pe < 18` → valuation razoável.
- **Selic shock** — `macro.selic_meta` delta >+50bp → CAPEX/refinancing pressure agrava.
- **DY drop** — `fundamentals.dy < 3%` → afasta-se do critério renda.
- **Conviction drop** — `conviction_scores.composite_score < 55` → flag review.

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
*Generated by `ii dossier RENT3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RENT3 — peso 3.4% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RENT3 — peso 6.2% |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RENT3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — RENT3

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 5.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/B aceitável
- DY atrativo
- Potencial de recuperação ROE

**Key risk**: Possível instabilidade financeira com queda nos dividendos e aumento da dívida

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E alto e ROE fraco
- Histórico de dividendos atrativo
- Liquidez macro positiva

**Key risk**: Desaceleração econômica ou aumento da Selic impactando a dívida

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/E alto
- ROE fraco
- FCF negativo

**Key risk**: Leverage e volatilidade de resultados financeiros (max 30 palavras)

###### 🔴 Seth Klarman — **AVOID** (conv 8/10, size: small)

**Rationale**:
- P/E alto e ROE fraco
- Fluxo de caixa negativo recente
- Risco político envolvendo mineradora

**Key risk**: Dividendos não pagos nos próximos dois trimestres

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/E alto e ROE abaixo meta
- Histórico de dividendos positivo
- Relação dívida/EBITDA dentro do limite

**Key risk**: Possível interrupção da venda pela justiça brasileira impactando negativamente a empresa

##### 📊 Context provided

```
TICKER: BR:RENT3

FUNDAMENTALS LATEST:
  pe: 28.005682
  pb: 2.113727
  dy: 4.18%
  roe: 7.21%
  net_debt_ebitda: 4.265023692200826

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=10.7 ebit=1.3 ni=0.3 em%=12.4 debt=44 fcf=-0.3
  2025-06-30: rev=9.9 ebit=2.0 ni=-0.2 em%=20.4 debt=42 fcf=1.5
  2025-03-31: rev=10.1 ebit=2.1 ni=0.8 em%=20.4 debt=43 fcf=0.9
  2024-12-31: rev=9.9 ebit=2.0 ni=0.8 em%=20.6 debt=45 fcf=1.2
  2024-09-30: rev=9.7 ebit=2.0 ni=0.8 em%=21.0 debt=43 fcf=1.9
  2024-06-30: rev=9.0 ebit=-0.1 ni=-0.6 em%=-1.2 debt=44 fcf=-1.2

VAULT THESIS:
**Core thesis (2026-04-25)**: A RENT3 é uma empresa de capital intensivo no setor industrial com um histórico robusto de pagamento de dividendos por mais de duas décadas. Apesar do P/E alto e ROE abaixo da meta, a relação P/B está dentro de limites aceitáveis e o DY oferece atratividade para investidores em busca de renda.

**Key assumptions**:
1. A empresa mantém seu histórico de dividendos por mais dois anos consecutivos
2. O ROE se recupera acima dos 15% nos próximos quatro trimestres
3. A relação dívida líquida/EBITDA permanece abaixo de 3× no próximo ano
4. A Selic mantém-se estável ou em queda, facilitando a gestão da dívida

**Disconfirmation triggers**:
- ROE cai abaixo de 7% por dois trimestres consecutivos
- Dividendos não são pagos nos próximos dois trimestres
- A relação dívida

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil Party Asks Court to Halt Rare Earths Miner’s Sale - Bloomberg.com [Sat, 25 Ap]
    # Brazil Party Asks Court to Halt Rare Earths Miner’s Sale. Provide news feedback or report an error. Left-wing Brazilian political party Rede Sustentabilidade asked the country’s Supreme Court to sus
  - Brazil party asks court to halt rare earths miner’s sale - Mining.com [Sat, 25 Ap]
    Brent Crude Oil $ 104.4 / bbl  -4.21%. Palladium $ 1496.5 / ozt  5.39%. Crude Oil $ 101.85 / bbl  -3.06%. Aluminum Futures $ 3314.25 / ton  -1.21%. Micro Silver Futures $ 75.48 / ozt  7.54%. Plat
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RENT3 — peso 3.4% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RENT3 — peso 6.2% |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RENT3_RI.md` (cemetery archive)_

#### RENT3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `ebit`: **-34.1%**
- ⬆️ **QOQ** `net_income`: **+253.1%**
- ⬇️ **QOQ** `fco`: **-111.6%**
- ⬇️ **QOQ** `fcf_proxy`: **-119.3%**
- ⬇️ **QOQ** `ebit_margin`: **-8.0pp**
- ⬆️ **YOY** `revenue`: **+10.8%**
- ⬇️ **YOY** `ebit`: **-34.5%**
- ⬇️ **YOY** `net_income`: **-68.2%**
- ⬇️ **YOY** `fco`: **-109.4%**
- ⬇️ **YOY** `fcf_proxy`: **-115.5%**
- ⬇️ **YOY** `ebit_margin`: **-8.6pp**
- ⬇️ **YOY** `net_margin`: **-6.0pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 10.7 mi | R$ 9.9 mi | +8.4% |
| `ebit` | R$ 1.3 mi | R$ 2.0 mi | -34.1% |
| `net_income` | R$ 0.3 mi | R$ -0.2 mi | +253.1% |
| `debt_total` | R$ 43.9 mi | R$ 41.6 mi | +5.7% |
| `fco` | R$ -0.2 mi | R$ 1.6 mi | -111.6% |
| `fcf_proxy` | R$ -0.3 mi | R$ 1.5 mi | -119.3% |
| `gross_margin` | 19.9% | 28.7% | -8.8pp |
| `ebit_margin` | 12.4% | 20.4% | -8.0pp |
| `net_margin` | 2.4% | -1.7% | +4.1pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 10.7 mi | R$ 9.7 mi | +10.8% |
| `ebit` | R$ 1.3 mi | R$ 2.0 mi | -34.5% |
| `net_income` | R$ 0.3 mi | R$ 0.8 mi | -68.2% |
| `debt_total` | R$ 43.9 mi | R$ 43.2 mi | +1.8% |
| `fco` | R$ -0.2 mi | R$ 2.0 mi | -109.4% |
| `fcf_proxy` | R$ -0.3 mi | R$ 1.9 mi | -115.5% |
| `gross_margin` | 19.9% | 28.5% | -8.6pp |
| `ebit_margin` | 12.4% | 21.0% | -8.6pp |
| `net_margin` | 2.4% | 8.4% | -6.0pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 10.7 | 12.4% | 2.4% | 44 | -0 |
| 2025-06-30 | ITR | 9.9 | 20.4% | -1.7% | 42 | 2 |
| 2025-03-31 | ITR | 10.1 | 20.4% | 8.3% | 43 | 1 |
| 2024-12-31 | DFP-ITR | 9.9 | 20.6% | 8.5% | 45 | 1 |
| 2024-09-30 | ITR | 9.7 | 21.0% | 8.4% | 43 | 2 |
| 2024-06-30 | ITR | 9.0 | -1.2% | -6.3% | 44 | -1 |
| 2024-03-31 | ITR | 8.7 | 21.3% | 8.4% | 42 | -2 |
| 2023-12-31 | DFP-ITR | 7.9 | 22.8% | 8.9% | 41 | -2 |
| 2023-09-30 | ITR | 7.3 | 22.3% | 9.1% | 37 | -2 |
| 2023-06-30 | ITR | 6.8 | 12.0% | -1.3% | 37 | -5 |
| 2023-03-31 | ITR | 6.8 | 24.0% | 7.6% | 36 | -1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [6.8, 6.8, 7.3, 7.9, 8.7, 9.0, 9.7, 9.9, 10.1, 9.9, 10.7]
  - title: EBIT margin %
    data: [24.0, 12.0, 22.3, 22.8, 21.3, -1.2, 21.0, 20.6, 20.4, 20.4, 12.4]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama RENT3 --write
ii deepdive RENT3 --save-obsidian
ii verdict RENT3 --narrate --write
ii fv RENT3
python -m analytics.fair_value_forward --ticker RENT3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
