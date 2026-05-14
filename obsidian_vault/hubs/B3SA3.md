---
type: ticker_hub
ticker: B3SA3
market: br
sector: Financials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# B3SA3 — B3

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Financials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 5.98, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 18.09 · P/B 4.57 · DY 3.6% · ROE 26.7% · ND/EBITDA 0.08 · Dividend streak 19

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\B3SA3.md` (cemetery archive)_

#### B3SA3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ri.b3.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=17.59000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.26738 · DY=0.03444695820033037 · P/E=19.119566
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Conclusão de Venda de Par |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Cronograma de divulgação  |
| 2026-04-15 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - març |
| 2026-03-19 | fato_relevante | cvm | Alteração na Administração da B3 |
| 2026-03-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - feve |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\B3SA3_FILING_2026-05-07.md` (cemetery archive)_

#### Filing dossier — [[B3SA3]] · 2026-05-07

**Trigger**: `cvm:comunicado` no dia `2026-05-07`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1518305&numSequencia=1043011&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 17.28

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `6.51` |
| HOLD entre | `6.51` — `8.68` (consensus) |
| TRIM entre | `8.68` — `9.99` |
| **SELL acima de** | `9.99` |

_Método: `graham_number`. Consensus fair = R$8.68. Our fair (mais conservador) = R$6.51._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.26738` | `0.2532` | +5.3% |
| EPS | `0.92` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.8B (+0.8% QoQ, +2.0% YoY)
- EBIT 1.6B (-3.1% QoQ)
- Margem EBIT 59.5% vs 61.9% prior
- Lucro líquido 1.2B (-6.1% QoQ, +3.4% YoY)

**BS / cash**
- Equity 19.8B (+0.2% QoQ)
- Dívida total 14.5B (+0.0% QoQ)
- FCF proxy 1.5B (+24.0% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 8.68 | 6.51 | 17.28 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-07` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 8.04 | 6.03 | 17.93 | HOLD | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:05+00:00 | `graham_number` | 8.04 | 6.03 | 17.93 | HOLD | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:03+00:00 | `graham_number` | 8.04 | 6.03 | 17.93 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:35+00:00 | `graham_number` | 8.04 | 6.03 | 17.78 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Filing 2026-04-30
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\B3SA3_FILING_2026-04-30.md` (cemetery archive)_

#### Filing dossier — [[B3SA3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513515&numSequencia=1038221&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 17.78

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `6.03` |
| HOLD entre | `6.03` — `8.04` (consensus) |
| TRIM entre | `8.04` — `9.25` |
| **SELL acima de** | `9.25` |

_Método: `graham_number`. Consensus fair = R$8.04. Our fair (mais conservador) = R$6.03._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.25591` | `0.2532` | +1.1% |
| EPS | `0.83` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.8B (+0.8% QoQ, +2.0% YoY)
- EBIT 1.6B (-3.1% QoQ)
- Margem EBIT 59.5% vs 61.9% prior
- Lucro líquido 1.2B (-6.1% QoQ, +3.4% YoY)

**BS / cash**
- Equity 19.8B (+0.2% QoQ)
- Dívida total 14.5B (+0.0% QoQ)
- FCF proxy 1.5B (+24.0% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:35+00:00 | `graham_number` | 8.04 | 6.03 | 17.78 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\B3SA3.md` (cemetery archive)_

#### B3SA3 — B3SA3

#watchlist #br #financials

##### Links

- Sector: [[sectors/Financials|Financials]]
- Market: [[markets/BR|BR]]
- Peers: [[BRBI11]]
- Vídeos: [[videos/2026-04-22_virtual-asset_dividendo-r-1-bi-em-risco-na-sapr11-itsa4-mudou-o-plano-petr4-lucra-co|DIVIDENDO: R$ 1 BI EM RISCO NA SAPR11! I]] · [[videos/2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa|PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CH]] · [[videos/2026-04-14_o-primo-rico_por-que-o-dolar-esta-caindo-tanto-vai-cair-ainda-mais|POR QUE O DÓLAR ESTÁ CAINDO TANTO? (vai ]]

##### Snapshot

- **Preço**: R$17.78  (2026-05-07)    _-3.16% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 75.0/100 (WATCH)

##### Fundamentals

- P/E: 21.421688 | P/B: 5.132795 | DY: 3.41%
- ROE: 25.59% | EPS: 0.83 | BVPS: 3.464
- Streak div: 19y | Aristocrat: None

##### Dividendos recentes

- 2026-04-01: R$0.0743
- 2026-01-02: R$0.3805
- 2025-09-24: R$0.0783
- 2025-06-24: R$0.0728
- 2025-03-26: R$0.0628

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Conclusão de Venda de Par
- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Cronograma de divulgação 
- **2026-04-15** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - març
- **2026-03-19** `fato_relevante` — Alteração na Administração da B3
- **2026-03-16** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Dados Operacionais - feve

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A B3 está valorizada, com um preço de 61% acima do patrimonial nos últimos 12 meses. |
| 2026-04-22 | Virtual Asset | operational | 0.70 | A B3 continua envolvida nos processos preparatórios para a privatização da Copasa, mas não pode concluir a alienação do controle. |
| 2026-04-22 | Virtual Asset | risk | 0.60 | A B3 enfrenta riscos geopolíticos que podem afetar o preço do petróleo e a previsibilidade do setor. |
| 2026-04-20 | Virtual Asset | operational | 0.80 | A B3 registrou um volume financeiro negociado de R$ 37 bilhões no primeiro trimestre de 2026, superando expectativas. |
| 2026-04-20 | Virtual Asset | valuation | 0.80 | A B3 está negociando com múltiplos esticados, entre 16 e 17 vezes o lucro, mas os analistas reconhecem que a empresa tem fundamentos positi… |
| 2026-04-14 | O Primo Rico | operational | 0.80 | A B3 registrou entrada de mais de 53 bilhões de reais em capital estrangeiro até março de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Dividendos] B3SA3 — peso 10.0%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Renda Total] B3SA3 — peso 7.5%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] B3SA3 — peso 6.2% |
| 2026-04-14 | XP | rating | neutral | 16.00 | [XP Top Dividendos] B3SA3 — peso 12.5%, Neutro, PT R$16.0, setor Financeiro |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-22 | Virtual Asset | oil_cycle | neutral | A Petrobras admite que tensões geopolíticas podem impactar seus resultados, mas o preço do petróleo em alta é… |
| 2026-04-22 | Virtual Asset | real_estate_cycle | bullish | O fundo imobiliário BTLG11 está quitando galpões logísticos em São Paulo, aumentando sua exposição a áreas es… |
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-14 | O Primo Rico | fed_path | bearish | A incerteza política e econômica, incluindo a pressão sobre o presidente do Banco Central Americano e a guerr… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -10.38%
- **Drawdown 5y**: -10.38%
- **YTD**: +32.39%
- **YoY (1y)**: +35.21%
- **CAGR 3y**: +12.64%  |  **5y**: +0.00%  |  **10y**: +12.44%
- **Vol annual**: +34.03%
- **Sharpe 3y** (rf=4%): +0.26

###### Dividendos
- **DY 5y avg**: +4.06%
- **Div CAGR 5y**: -25.75%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$9.09B | R$4.23B | R$9.68B |
| 2023-12-31 | R$8.92B | R$4.13B | R$3.53B |
| 2024-12-31 | R$9.43B | R$4.58B | R$9.05B |
| 2025-12-31 | R$10.07B | R$4.59B | R$4.07B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "B3SA3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: B3SA3
    data: [14.25, 14.65, 14.95, 14.33, 13.95, 13.58, 13.24, 13.53, 13.52, 14.58, 14.71, 14.09, 13.68, 13.07, 12.7, 12.59, 12.91, 12.7, 12.53, 12.55, 12.98, 13.09, 12.97, 13.48, 13.5, 13.22, 12.84, 12.66, 12.55, 12.66, 12.5, 12.6, 13.2, 13.53, 14.16, 13.98, 14.96, 15.02, 14.21, 13.72, 13.24, 13.89, 14.28, 14.31, 15.1, 15.82, 16.68, 15.77, 17.45, 17.61, 18.22, 18.49, 17.24, 17.14, 17.12, 17.38, 17.04, 18.43, 19.51, 19.78, 19.03, 17.88, 18.36]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "B3SA3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.1679, 0.1509, 0.234, 0.2681, 0.6424, 0.9143, 0.4691, 0.382, 0.4016, 0.278, 0.4548]
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
    data: [21.66, 23.192772, 22.654764, 22.86747, 22.595238, 22.595238, 22.285715, 22.325302, 21.542168, 21.722893, 21.530123, 21.698795, 22.120483, 21.421688]
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
    data: [26.26, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59, 25.59]
  - title: DY %
    data: [3.08, 3.15, 3.18, 3.19, 3.19, 3.19, 3.24, 3.27, 3.39, 3.36, 3.39, 3.36, 3.3, 3.41]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\B3SA3_DOSSIE.md` (cemetery archive)_

#### 📑 B3SA3 — B3

> Generated **2026-04-26** by `ii dossier B3SA3`. Cross-links: [[B3SA3]] · [[B3SA3]] · [[CONSTITUTION]]

##### TL;DR

B3SA3 negocia a P/E 22.60 com DY 3.19% mas ROE excepcional de 25.59% e net_debt/EBITDA de apenas 0.16x — capital-light puro. Synthetic IC veredicto **BUY** (medium confidence, 60% consenso) e composite conviction 73 com 19 anos de streak de dividendos. Achado central: monopólio natural de exchange brasileira justifica P/B alto (5.48x); DY baixo é trade-off por capital-light, mas o factor decisivo é ADTV B3 — qualquer queda estrutural de volume colapsa earnings.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.84  |  **BVPS**: 3.46
- **ROE**: 25.59%  |  **P/E**: 22.60  |  **P/B**: 5.48
- **DY**: 3.19%  |  **Streak div**: 19y  |  **Market cap**: R$ 95.10B
- **Last price**: BRL 18.98 (2026-04-24)  |  **YoY**: +43.0%

##### 2. Synthetic IC

**🏛️ BUY** (medium confidence, 60.0% consensus)

→ Detalhe: [[B3SA3]]

##### 3. Thesis

**Core thesis (2026-04-25)**: B3SA3 é uma empresa financeira sólida com um histórico de pagamento de dividendos consistente por mais de uma década. Com um ROE elevado de 25,59% e uma relação dívida líquida/EBITDA extremamente baixa de apenas 0,16x, a empresa mantém-se como um valor atrativo apesar do P/E ligeiramente acima da média (22,87x) e P/B alto (5,48x).

**Key assumptions**:
1. A demanda por serviços financeiros continuará em crescimento no Brasil, beneficiando B3SA3.
2. B3SA3 manterá seu histórico de distribuição de dividendos acima dos 3%.
3. O cenário macroeconômico brasileiro não deteriorar-se-á significativamente nos próximos anos.
4. A empresa continuará a gerir efetivamente suas dívidas, mantendo o ROE acima do nível atual.

**Disconfirmation triggers**:
- ROE cair abaixo de

→ Vault: [[B3SA3]]

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

- **P/E = 22.60** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 22.60** fora do screen.
- **P/B = 5.48** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **5.48** — verificar consistência com ROE.
- **DY = 3.19%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **3.19%** abaixo do floor — DRIP não-óbvio.
- **ROE = 25.59%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **25.59%** compounder-grade.
- **Graham Number ≈ R$ 8.09** vs preço **R$ 18.98** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 19y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Volume B3 estrutural baixo** — Selic alta empurra capital para RF, contraindo ADTV equities. Trigger: ADTV B3 < R$15B/dia média trimestral (proxy via `events` macro ou snapshot externo).
- 🔴 **Fee compression regulatória** — CVM/B3 podem reduzir taxas para incentivar competição. Trigger: anúncio CVM/B3 de revisão de tabela tarifária (`events` kind=`fato_relevante`).
- 🟡 **P/B alto vulnerável a re-rating** — 5.48x deixa pouco buffer para erros operacionais. Trigger: `fundamentals.pb` > 6 sem aceleração de earnings.
- 🟡 **Concorrência (ATS / nova bolsa)** — entrada de ATS regulamentada poderia diluir monopólio. Trigger: aprovação CVM de ATS competitiva.
- 🟢 **DY sub-mínimo** — 3.19% < 6% típico do screen BR (mas justificado por capital-light). Trigger: `fundamentals.dy` < 2.5% por 4 trimestres.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: P/E < 18 (recompressão de múltiplo) **ou** sinal de Selic em tendência de queda sustentada (rotação de RF para equities aumenta ADTV). Weight prudente 4-6% do book BR como quality-compounder (não DRIP). Cash exclusivo BRL (BR isolation); pode complementar ITUB4 sem dupla-contar exposure financials operacional.

##### 7. Tracking triggers (auto-monitoring)

- **ADTV colapso** — ADTV B3 < R$15B/dia média trimestral (proxy macro).
- **ROE deterioração** — `fundamentals.roe` < 18% por 2 trimestres consecutivos.
- **P/E re-rating** — `fundamentals.pe` < 18 (entry técnico) ou > 30 (exit técnico).
- **Streak break** — `fundamentals.dividend_streak_years` regrida abaixo de 19.
- **Fato relevante regulatório** — `events WHERE source='cvm' AND kind LIKE '%fee%'` ou revisão de tabela tarifária.

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
*Generated by `ii dossier B3SA3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A B3 está valorizada, com um preço de 61% acima do patrimonial nos últimos 12 meses. |
| 2026-04-22 | Virtual Asset | operational | 0.70 | A B3 continua envolvida nos processos preparatórios para a privatização da Copasa, mas não pode concluir a alienação do controle. |
| 2026-04-22 | Virtual Asset | risk | 0.60 | A B3 enfrenta riscos geopolíticos que podem afetar o preço do petróleo e a previsibilidade do setor. |
| 2026-04-20 | Virtual Asset | operational | 0.80 | A B3 registrou um volume financeiro negociado de R$ 37 bilhões no primeiro trimestre de 2026, superando expectativas. |
| 2026-04-20 | Virtual Asset | valuation | 0.80 | A B3 está negociando com múltiplos esticados, entre 16 e 17 vezes o lucro, mas os analistas reconhecem que a empresa tem fundamentos positi… |
| 2026-04-14 | O Primo Rico | operational | 0.80 | A B3 registrou entrada de mais de 53 bilhões de reais em capital estrangeiro até março de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Dividendos] B3SA3 — peso 10.0%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Renda Total] B3SA3 — peso 7.5%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] B3SA3 — peso 6.2% |
| 2026-04-14 | XP | rating | neutral | 16.00 | [XP Top Dividendos] B3SA3 — peso 12.5%, Neutro, PT R$16.0, setor Financeiro |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-22 | Virtual Asset | oil_cycle | neutral | A Petrobras admite que tensões geopolíticas podem impactar seus resultados, mas o preço do petróleo em alta é… |
| 2026-04-22 | Virtual Asset | real_estate_cycle | bullish | O fundo imobiliário BTLG11 está quitando galpões logísticos em São Paulo, aumentando sua exposição a áreas es… |
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-14 | O Primo Rico | fed_path | bearish | A incerteza política e econômica, incluindo a pressão sobre o presidente do Banco Central Americano e a guerr… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\B3SA3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — B3SA3

**Committee verdict**: **MIXED** (low confidence, 40% consensus)  
**Votes**: BUY=2 | HOLD=2 | AVOID=1  
**Avg conviction majority**: 7.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- ROE alto e estável
- geração de FCF crescente
- baixa alavancagem

**Key risk**: deterioração macroeconômica no Brasil impactando demanda por serviços financeiros

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- ROE elevado e baixa dívida
- crescimento de serviços financeiros no Brasil
- dividendos consistentes

**Key risk**: deterioração significativa da economia brasileira nos próximos anos

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- Pe e Pb altos
- Intangíveis elevados
- Falta de anti-fragilidade

**Key risk**: Avaliação sobrevalorizada pode levar a perdas significativas se o mercado corrigir

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: small)

**Rationale**:
- ROE elevado
- dívida baixa
- dividendos consistentes

**Key risk**: deterioração macroeconômica brasileira impactando demanda serviços financeiros

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE elevado e baixa dívida
- Histórico de dividendos consistente
- Crescimento da demanda por serviços financeiros

**Key risk**: Deterioração significativa do cenário macroeconômico brasileiro

##### 📊 Context provided

```
TICKER: BR:B3SA3

FUNDAMENTALS LATEST:
  pe: 21.602411
  pb: 5.176097
  dy: 3.38%
  roe: 25.59%
  net_debt_ebitda: 0.16400602231528902
  intangible_pct_assets: 52.7%   (goodwill $24.4B + intangibles $1.2B)
  ⚠ HIGH intangibles — book value understates brand/franchise economic value (P/B + Buffett ceiling unreliable)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=2.8 ebit=1.6 ni=1.2 em%=59.5 debt=15 fcf=1.5
  2025-06-30: rev=2.7 ebit=1.7 ni=1.3 em%=61.9 debt=15 fcf=1.2
  2025-03-31: rev=2.7 ebit=1.6 ni=1.1 em%=58.7 debt=15 fcf=-0.7
  2024-12-31: rev=2.7 ebit=1.5 ni=1.2 em%=55.8 debt=13 fcf=2.3
  2024-09-30: rev=2.7 ebit=1.6 ni=1.2 em%=59.2 debt=13 fcf=1.2
  2024-06-30: rev=2.7 ebit=1.7 ni=1.2 em%=63.4 debt=13 fcf=4.1

VAULT THESIS:
**Core thesis (2026-04-25)**: B3SA3 é uma empresa financeira sólida com um histórico de pagamento de dividendos consistente por mais de uma década. Com um ROE elevado de 25,59% e uma relação dívida líquida/EBITDA extremamente baixa de apenas 0,16x, a empresa mantém-se como um valor atrativo apesar do P/E ligeiramente acima da média (22,87x) e P/B alto (5,48x).

**Key assumptions**:
1. A demanda por serviços financeiros continuará em crescimento no Brasil, beneficiando B3SA3.
2. B3SA3 manterá seu histórico de distribuição de dividendos acima dos 3%.
3. O cenário macroeconômico brasileiro não deteriorar-se-á significativamente nos próximos anos.
4. A empresa continuará a gerir efetivamente suas dívidas, mantendo o ROE acima do nível atual.

**Disconfirmation triggers**:
- ROE cair abaixo de
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=6 · analyst=4 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-22 | Virtual Asset | valuation | 0.80 | A B3 está valorizada, com um preço de 61% acima do patrimonial nos últimos 12 meses. |
| 2026-04-22 | Virtual Asset | operational | 0.70 | A B3 continua envolvida nos processos preparatórios para a privatização da Copasa, mas não pode concluir a alienação do controle. |
| 2026-04-22 | Virtual Asset | risk | 0.60 | A B3 enfrenta riscos geopolíticos que podem afetar o preço do petróleo e a previsibilidade do setor. |
| 2026-04-20 | Virtual Asset | operational | 0.80 | A B3 registrou um volume financeiro negociado de R$ 37 bilhões no primeiro trimestre de 2026, superando expectativas. |
| 2026-04-20 | Virtual Asset | valuation | 0.80 | A B3 está negociando com múltiplos esticados, entre 16 e 17 vezes o lucro, mas os analistas reconhecem que a empresa tem fundamentos positi… |
| 2026-04-14 | O Primo Rico | operational | 0.80 | A B3 registrou entrada de mais de 53 bilhões de reais em capital estrangeiro até março de 2026. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Dividendos] B3SA3 — peso 10.0%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | SUNO | rating | neutral | 16.90 | [Suno Renda Total] B3SA3 — peso 7.5%, rating Aguardar, PT R$16.9 |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] B3SA3 — peso 6.2% |
| 2026-04-14 | XP | rating | neutral | 16.00 | [XP Top Dividendos] B3SA3 — peso 12.5%, Neutro, PT R$16.0, setor Financeiro |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-22 | Virtual Asset | oil_cycle | neutral | A Petrobras admite que tensões geopolíticas podem impactar seus resultados, mas o preço do petróleo em alta é… |
| 2026-04-22 | Virtual Asset | real_estate_cycle | bullish | O fundo imobiliário BTLG11 está quitando galpões logísticos em São Paulo, aumentando sua exposição a áreas es… |
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |
| 2026-04-14 | O Primo Rico | fed_path | bearish | A incerteza política e econômica, incluindo a pressão sobre o presidente do Banco Central Americano e a guerr… |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\B3SA3_RI.md` (cemetery archive)_

#### B3SA3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `fco`: **+31.4%**
- ⬆️ **QOQ** `fcf_proxy`: **+24.0%**
- ⬆️ **YOY** `fco`: **+32.1%**
- ⬆️ **YOY** `fcf_proxy`: **+33.1%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.8 mi | R$ 2.7 mi | +0.8% |
| `ebit` | R$ 1.6 mi | R$ 1.7 mi | -3.1% |
| `net_income` | R$ 1.2 mi | R$ 1.3 mi | -6.1% |
| `debt_total` | R$ 14.5 mi | R$ 14.5 mi | +0.0% |
| `fco` | R$ 1.6 mi | R$ 1.2 mi | +31.4% |
| `fcf_proxy` | R$ 1.5 mi | R$ 1.2 mi | +24.0% |
| `gross_margin` | 89.8% | 92.6% | -2.7pp |
| `ebit_margin` | 59.5% | 61.9% | -2.4pp |
| `net_margin` | 45.0% | 48.3% | -3.3pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.8 mi | R$ 2.7 mi | +2.0% |
| `ebit` | R$ 1.6 mi | R$ 1.6 mi | +2.6% |
| `net_income` | R$ 1.2 mi | R$ 1.2 mi | +3.4% |
| `debt_total` | R$ 14.5 mi | R$ 12.9 mi | +12.9% |
| `fco` | R$ 1.6 mi | R$ 1.2 mi | +32.1% |
| `fcf_proxy` | R$ 1.5 mi | R$ 1.2 mi | +33.1% |
| `gross_margin` | 89.8% | 89.8% | +0.0pp |
| `ebit_margin` | 59.5% | 59.2% | +0.3pp |
| `net_margin` | 45.0% | 44.4% | +0.6pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 2.8 | 59.5% | 45.0% | 15 | 2 |
| 2025-06-30 | ITR | 2.7 | 61.9% | 48.3% | 15 | 1 |
| 2025-03-31 | ITR | 2.7 | 58.7% | 41.6% | 15 | -1 |
| 2024-12-31 | DFP-ITR | 2.7 | 55.8% | 44.2% | 13 | 2 |
| 2024-09-30 | ITR | 2.7 | 59.2% | 44.4% | 13 | 1 |
| 2024-06-30 | ITR | 2.7 | 63.4% | 45.6% | 13 | 4 |
| 2024-03-31 | ITR | 2.5 | 49.6% | 38.5% | 14 | 2 |
| 2023-12-31 | DFP-ITR | 2.5 | 47.0% | 36.7% | 14 | -1 |
| 2023-09-30 | ITR | 2.5 | 54.1% | 43.1% | 12 | 1 |
| 2023-06-30 | ITR | 2.5 | 55.5% | 42.5% | 11 | 2 |
| 2023-03-31 | ITR | 2.5 | 55.2% | 44.3% | 12 | 1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [2.5, 2.5, 2.5, 2.5, 2.5, 2.7, 2.7, 2.7, 2.7, 2.7, 2.8]
  - title: EBIT margin %
    data: [55.2, 55.5, 54.1, 47.0, 49.6, 63.4, 59.2, 55.8, 58.7, 61.9, 59.5]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama B3SA3 --write
ii deepdive B3SA3 --save-obsidian
ii verdict B3SA3 --narrate --write
ii fv B3SA3
python -m analytics.fair_value_forward --ticker B3SA3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
