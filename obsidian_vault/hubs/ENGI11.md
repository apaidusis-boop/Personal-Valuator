---
type: ticker_hub
ticker: ENGI11
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

# ENGI11 — Energisa

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Utilities` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 1.62, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 35.54 · P/B 0.89 · DY 3.2% · ROE 12.1% · ND/EBITDA 4.05 · Dividend streak 16

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\ENGI11.md` (cemetery archive)_

#### ENGI11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.energisa.com.br/
- **Pilot rationale**: heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **21**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=51.79999923706055
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.14495 · DY=0.02985530932003462 · P/E=37.536232
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Boletim de Relações com I |
| 2026-04-22 | fato_relevante | cvm | Assinatura de memorando de entendimentos para subscrição e integralização de açõ |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aneel homologa reajuste t |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aneel homologa reajuste t |
| 2026-04-22 | fato_relevante | cvm | Assinatura de memorando de entendimentos para subscrição e integralização de açõ |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ENGI11_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[ENGI11]] · 2026-05-08

**Trigger**: `cvm:fato_relevante` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1518979&numSequencia=1043685&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 49.98

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `32.30` |
| HOLD entre | `32.30` — `41.41` (consensus) |
| TRIM entre | `41.41` — `47.63` |
| **SELL acima de** | `47.63` |

_Método: `graham_number`. Consensus fair = R$41.41. Our fair (mais conservador) = R$32.30._

##### 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.12091` | `0.1893` | +36.1% |
| EPS | `1.38` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 9.2B (+7.2% QoQ, +7.0% YoY)
- EBIT 1.7B (+0.4% QoQ)
- Margem EBIT 18.3% vs 19.6% prior
- Lucro líquido 648.4M (+32.4% QoQ, -10.8% YoY)

**BS / cash**
- Equity 22.6B (-1.2% QoQ)
- Dívida total 41.0B (+8.6% QoQ)
- FCF proxy -763.7M (-445.7% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 41.41 | 32.30 | 49.98 | SELL | single_source | `filing:cvm:fato_relevante:2026-05-08` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 41.41 | 32.30 | 52.73 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 41.41 | 32.30 | 52.73 | SELL | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `graham_number` | 41.41 | 32.30 | 52.73 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:37+00:00 | `graham_number` | 41.41 | 32.30 | 52.20 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-04-22` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-22 · Filing 2026-04-22
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ENGI11_FILING_2026-04-22.md` (cemetery archive)_

#### Filing dossier — [[ENGI11]] · 2026-04-22

**Trigger**: `cvm:fato_relevante` no dia `2026-04-22`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1507402&numSequencia=1032108&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 52.20

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `32.30` |
| HOLD entre | `32.30` — `41.41` (consensus) |
| TRIM entre | `41.41` — `47.63` |
| **SELL acima de** | `47.63` |

_Método: `graham_number`. Consensus fair = R$41.41. Our fair (mais conservador) = R$32.30._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.14495` | `0.1893` | +23.4% |
| EPS | `1.38` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 9.2B (+7.2% QoQ, +7.0% YoY)
- EBIT 1.7B (+0.4% QoQ)
- Margem EBIT 18.3% vs 19.6% prior
- Lucro líquido 648.4M (+32.4% QoQ, -10.8% YoY)

**BS / cash**
- Equity 22.6B (-1.2% QoQ)
- Dívida total 41.0B (+8.6% QoQ)
- FCF proxy -763.7M (-445.7% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:37+00:00 | `graham_number` | 41.41 | 32.30 | 52.20 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-04-22` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ENGI11.md` (cemetery archive)_

#### ENGI11 — ENGI11

#watchlist #br #utilities

##### Links

- Sector: [[sectors/Utilities|Utilities]]
- Market: [[markets/BR|BR]]
- Peers: [[ALUP11]] · [[AXIA7]] · [[CMIG4]] · [[CPLE3]] · [[CSMG3]]

##### Snapshot

- **Preço**: R$52.20  (2026-05-07)    _-3.42% 1d_
- **Screen**: 0.0  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 35.0/100 (RISK)

##### Fundamentals

- P/E: 37.826088 | P/B: 0.94498456 | DY: 2.96%
- ROE: 14.49% | EPS: 1.38 | BVPS: 55.239
- Streak div: 16y | Aristocrat: None

##### Dividendos recentes

- 2025-11-27: R$0.6374
- 2025-08-13: R$0.9091
- 2025-02-26: R$1.7273
- 2024-08-13: R$0.9091
- 2024-01-02: R$0.9091

##### Eventos (SEC/CVM)

- **2026-04-24** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Boletim de Relações com I
- **2026-04-22** `fato_relevante` — Assinatura de memorando de entendimentos para subscrição e integralização de açõ
- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Aneel homologa reajuste t
- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Aneel homologa reajuste t
- **2026-04-22** `fato_relevante` — Assinatura de memorando de entendimentos para subscrição e integralização de açõ

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ENGI11 — peso 4.8% |
| 2026-04-14 | XP | rating | bull | 84.86 | [XP Top Dividendos] ENGI11 — peso 5.0%, Compra, PT R$84.86, setor Elétricas |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -10.23%
- **Drawdown 5y**: -10.23%
- **YTD**: +10.85%
- **YoY (1y)**: +28.63%
- **CAGR 3y**: +9.83%  |  **5y**: +5.22%  |  **10y**: +15.61%
- **Vol annual**: +26.20%
- **Sharpe 3y** (rf=4%): +0.22

###### Dividendos
- **DY 5y avg**: +5.36%
- **Div CAGR 5y**: +19.77%
- **Frequency**: semiannual
- **Streak** (sem cortes): 2 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$26.50B | R$6.84B | R$2.14B |
| 2023-12-31 | R$28.53B | R$7.93B | R$1.89B |
| 2024-12-31 | R$33.72B | R$9.19B | R$3.79B |
| 2025-12-31 | R$35.44B | R$9.24B | R$2.21B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ENGI11 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: ENGI11
    data: [42.05, 42.15, 43.81, 43.21, 43.18, 43.05, 42.14, 42.89, 42.78, 43.93, 43.89, 41.93, 41.65, 41.05, 40.65, 41.82, 43.95, 42.54, 41.64, 43.01, 44.37, 43.98, 44.64, 45.14, 45.32, 45.77, 45.36, 43.89, 43.67, 45.93, 47.25, 47.05, 49.01, 49.37, 48.75, 48.79, 49.32, 51.06, 47.94, 47.69, 46.1, 47.16, 46.72, 46.91, 46.65, 51.8, 51.42, 50.08, 51.49, 51.34, 54.43, 53.54, 52.9, 53.25, 50.51, 50.3, 50.28, 53.01, 57.35, 57.7, 55.5, 51.98, 54.05]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "ENGI11 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
series:
  - title: Dividends
    data: [0.3634, 0.513, 0.7069, 0.9818, 0.5455, 1.5909, 3.0545, 1.3636, 1.8182, 3.2738]
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
    data: [13.23, 41.644928, 40.217392, 40.06522, 40.06522, 40.06522, 39.347824, 38.934784, 37.666668, 38.275364, 38.028984, 38.434784, 39.166668, 37.826088]
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
    data: [10.45, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49, 14.49]
  - title: DY %
    data: [2.93, 2.69, 2.79, 2.8, 2.8, 2.8, 2.85, 2.88, 2.98, 2.93, 2.95, 2.92, 2.86, 2.96]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ENGI11_DOSSIE.md` (cemetery archive)_

#### 📑 ENGI11 — Energisa

> Generated **2026-04-26** by `ii dossier ENGI11`. Cross-links: [[ENGI11]] · [[ENGI11]] · [[CONSTITUTION]]

##### TL;DR

ENGI11 negocia a P/E elevado de 40.07 mas P/B exactamente 1.00 e ROE de 14.49%, com DY apenas 2.80% após 16 anos consecutivos de dividendos. Synthetic IC veredicto **HOLD** (high confidence, 80% consenso) e composite conviction 65. Achado central: P/B colado em 1x oferece floor estrutural, mas DY abaixo de 3% e P/E premium tornam ENGI11 não-DRIP — preço já incorpora execução perfeita das concessões.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.38  |  **BVPS**: 55.24
- **ROE**: 14.49%  |  **P/E**: 40.07  |  **P/B**: 1.00
- **DY**: 2.80%  |  **Streak div**: 16y  |  **Market cap**: R$ 25.27B
- **Last price**: BRL 55.29 (2026-04-24)  |  **YoY**: +35.0%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[ENGI11]]

##### 3. Thesis

**Core thesis (2026-04-25)**: ENGI11, com um P/B de 1.0009233 e ROE de 14.49%, oferece valor potencial devido ao seu baixo múltiplo em relação ao patrimônio líquido e uma história consistente de dividendos por 16 anos, apesar do DY ser inferior à média esperada para FIIs.

**Key assumptions**:
1. Dividendos continuarão a ser pagos consistentemente nos próximos anos
2. A relação Net Debt/EBITDA melhorará gradualmente ao longo dos próximos trimestres
3. O P/B permanecerá estável ou diminuirá, mantendo o desconto sobre o patrimônio líquido
4. O ROE se manterá acima de 14% para sustentar a valorização do ativo

**Disconfirmation triggers**:
- ROE cair abaixo de 12% por dois trimestres consecutivos
- Net Debt/EBITDA aumentar para mais de 5.0
- Dividend streak interrompido após 16 anos
- P/B sub

→ Vault: [[ENGI11]]

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

- **P/E = 40.07** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 40.07** fora do screen.
- **P/B = 1.00** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.00** — verificar consistência com ROE.
- **DY = 2.80%** → [[Glossary/DY|leitura + contraméricas]]. FIIs: target DY ≥ 8%. **2.80%** baixo para FII; verificar reset/cycle.
- **ROE = 14.49%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **14.49%** abaixo do critério.
- **Streak div = 16y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

##### 5. Riscos identificados

- 🔴 **DY estruturalmente baixo** — 2.80% bem abaixo do mínimo 6% para utility BR. Trigger: `fundamentals.dy` < 4% mantém-se 4 trimestres consecutivos.
- 🟡 **P/E esticado** — 40.07 indica preço incorpora crescimento agressivo. Trigger: `fundamentals.pe` > 30 com `roe` < 14%.
- 🟡 **Revisão tarifária ANEEL** — múltiplas distribuidoras (Energisa MS/MT/Sergipe etc.). Trigger: anúncio ANEEL de revisão tarifária com WACC reduzido.
- 🟡 **Hidrologia / GSF** — exposição a geração. Trigger: ONS GSF < 0.85 trimestral.
- 🟢 **Capex elevado expansão** — concessões nordestinas exigem investimento. Trigger: `fundamentals.net_debt_ebitda` > 5x.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: DY recuperar para ≥ 5% (preço cair ou payout subir) **e** P/E < 20. Weight prudente 3-5% se entrada acontecer; perfil mais quality-compounder do que DRIP devido ao DY baixo. Cash exclusivo BRL (BR isolation), competindo com TAEE11/CMIG4 no slot utility.

##### 7. Tracking triggers (auto-monitoring)

- **DY recovery** — `fundamentals.dy` ≥ 5% sustentado 2 trimestres.
- **P/E re-rating** — `fundamentals.pe` < 20 abre ponto de entrada.
- **ROE preservado** — `fundamentals.roe` ≥ 14% por 2 trimestres consecutivos.
- **Streak break** — `fundamentals.dividend_streak_years` regrida abaixo de 16 (red flag).
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 5x.

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
*Generated by `ii dossier ENGI11` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ENGI11 — peso 4.8% |
| 2026-04-14 | XP | rating | bull | 84.86 | [XP Top Dividendos] ENGI11 — peso 5.0%, Compra, PT R$84.86, setor Elétricas |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ENGI11_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — ENGI11

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=0 | HOLD=4 | AVOID=1  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/B baixo e ROE estável
- Dividendos consistentes por 16 anos
- Net Debt/EBITDA em melhora

**Key risk**: Possibilidade de deterioração da relação Net Debt/EBITDA ou interrupção do pagamento de dividendos

###### 🟡 Stan Druckenmiller — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/B estável e baixo oferece valor
- Dividendos consistentes há 16 anos
- ROE acima de 14% mantido

**Key risk**: Aumento do Net Debt/EBITDA para mais de 5.0 ou interrupção da sequência de dividendos

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- P/B está próximo a 1, indicando pouca margem de segurança
- ROE é baixo para o setor e não mostra robustez contra incertezas

**Key risk**: Risco sistêmico associado a ativos brasileiros e potencial aumento da dívida

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/B próximo a 1, ROE estável
- Dividendos consistentes por 16 anos
- Melhora gradual na relação dívida/EBITDA

**Key risk**: Possível deterioração da situação financeira devido ao risco regulatório no Brasil

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/B baixo e ROE sólido
- Dividendos consistentes por 16 anos
- Relação dívida/EBITDA sob controle

**Key risk**: Potencial perda de concessão no Brasil pode afetar negativamente a empresa

##### 📊 Context provided

```
TICKER: BR:ENGI11

FUNDAMENTALS LATEST:
  pe: 40.06522
  pb: 1.0009233
  dy: 2.80%
  roe: 14.49%
  net_debt_ebitda: 4.224792861839163

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=9.2 ebit=1.7 ni=0.6 em%=18.3 debt=41 fcf=-0.8
  2025-06-30: rev=8.6 ebit=1.7 ni=0.5 em%=19.6 debt=38 fcf=0.2
  2025-03-31: rev=8.4 ebit=1.9 ni=1.0 em%=22.7 debt=37 fcf=0.4
  2024-12-31: rev=9.6 ebit=1.3 ni=2.1 em%=13.6 debt=35 fcf=-0.6
  2024-09-30: rev=8.6 ebit=1.4 ni=0.7 em%=16.4 debt=33 fcf=2.3
  2024-06-30: rev=7.6 ebit=1.3 ni=0.7 em%=17.2 debt=35 fcf=-1.2

VAULT THESIS:
**Core thesis (2026-04-25)**: ENGI11, com um P/B de 1.0009233 e ROE de 14.49%, oferece valor potencial devido ao seu baixo múltiplo em relação ao patrimônio líquido e uma história consistente de dividendos por 16 anos, apesar do DY ser inferior à média esperada para FIIs.

**Key assumptions**:
1. Dividendos continuarão a ser pagos consistentemente nos próximos anos
2. A relação Net Debt/EBITDA melhorará gradualmente ao longo dos próximos trimestres
3. O P/B permanecerá estável ou diminuirá, mantendo o desconto sobre o patrimônio líquido
4. O ROE se manterá acima de 14% para sustentar a valorização do ativo

**Disconfirmation triggers**:
- ROE cair abaixo de 12% por dois trimestres consecutivos
- Net Debt/EBITDA aumentar para mais de 5.0
- Dividend streak interrompido após 16 anos
- P/B sub

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Enel assets worth nearly $4 billion at risk over Brazil concession, auditors say - Reuters [Thu, 16 Ap]
    REUTERS/Amanda Perobelli/File Photo Purchase Licensing Rights, opens new tab. MILAN, April 16 (Reuters) - Enel (ENEI.MI), opens new tab may lose its power concession in the Brazilian city ​of Sao Paul
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global minerals
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Value] ENGI11 — peso 4.8% |
| 2026-04-14 | XP | rating | bull | 84.86 | [XP Top Dividendos] ENGI11 — peso 5.0%, Compra, PT R$84.86, setor Elétricas |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ENGI11_RI.md` (cemetery archive)_

#### ENGI11 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `net_income`: **+32.4%**
- ⬇️ **QOQ** `fcf_proxy`: **-445.7%**
- ⬇️ **YOY** `fcf_proxy`: **-133.3%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 9.2 mi | R$ 8.6 mi | +7.2% |
| `ebit` | R$ 1.7 mi | R$ 1.7 mi | +0.4% |
| `net_income` | R$ 0.6 mi | R$ 0.5 mi | +32.4% |
| `debt_total` | R$ 41.0 mi | R$ 37.8 mi | +8.5% |
| `fco` | R$ 1.3 mi | R$ 1.4 mi | -8.9% |
| `fcf_proxy` | R$ -0.8 mi | R$ 0.2 mi | -445.7% |
| `gross_margin` | 23.6% | 25.5% | -1.9pp |
| `ebit_margin` | 18.3% | 19.6% | -1.2pp |
| `net_margin` | 7.1% | 5.7% | +1.3pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 9.2 mi | R$ 8.6 mi | +7.0% |
| `ebit` | R$ 1.7 mi | R$ 1.4 mi | +19.5% |
| `net_income` | R$ 0.6 mi | R$ 0.7 mi | -10.8% |
| `debt_total` | R$ 41.0 mi | R$ 33.4 mi | +23.0% |
| `fco` | R$ 1.3 mi | R$ 1.5 mi | -13.3% |
| `fcf_proxy` | R$ -0.8 mi | R$ 2.3 mi | -133.3% |
| `gross_margin` | 23.6% | 23.6% | +0.0pp |
| `ebit_margin` | 18.3% | 16.4% | +1.9pp |
| `net_margin` | 7.1% | 8.5% | -1.4pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 9.2 | 18.3% | 7.1% | 41 | 1 |
| 2025-06-30 | ITR | 8.6 | 19.6% | 5.7% | 38 | 1 |
| 2025-03-31 | ITR | 8.4 | 22.7% | 12.2% | 37 | 1 |
| 2024-12-31 | DFP-ITR | 9.6 | 13.6% | 22.2% | 35 | 2 |
| 2024-09-30 | ITR | 8.6 | 16.4% | 8.5% | 33 | 1 |
| 2024-06-30 | ITR | 7.6 | 17.2% | 8.6% | 35 | 2 |
| 2024-03-31 | ITR | 8.0 | 26.2% | 14.2% | 32 | 2 |
| 2023-12-31 | DFP-ITR | 8.1 | 19.2% | 9.0% | 32 | 2 |
| 2023-09-30 | ITR | 7.3 | 22.2% | 9.4% | 31 | 1 |
| 2023-06-30 | ITR | 6.6 | 21.0% | 10.0% | 31 | 1 |
| 2023-03-31 | ITR | 6.5 | 22.8% | 7.8% | 29 | 1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [6.5, 6.6, 7.3, 8.1, 8.0, 7.6, 8.6, 9.6, 8.4, 8.6, 9.2]
  - title: EBIT margin %
    data: [22.8, 21.0, 22.2, 19.2, 26.2, 17.2, 16.4, 13.6, 22.7, 19.6, 18.3]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama ENGI11 --write
ii deepdive ENGI11 --save-obsidian
ii verdict ENGI11 --narrate --write
ii fv ENGI11
python -m analytics.fair_value_forward --ticker ENGI11
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
