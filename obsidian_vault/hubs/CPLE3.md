---
type: ticker_hub
ticker: CPLE3
market: br
sector: Utilities
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 9
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# CPLE3 — Copel

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Utilities` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `9 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 3.53, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 16.00 · P/B 1.87 · DY 7.3% · ROE 10.8% · ND/EBITDA 2.88 · Dividend streak 1

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\CPLE3.md` (cemetery archive)_

#### CPLE3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.copel.com/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=15.069999694824219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.10787 · DY=0.07051088397599298 · P/E=16.560438
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 08/ |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 02/ |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Arquivamento Relatório An |
| 2026-03-18 | fato_relevante | cvm | FR 01/26 - Copel vence leilão de reserva de capacidade com duas usinas hidrelétr |
| 2026-03-18 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação - Leilão de Reserva  |

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

#### 2026-05-08 · Content trigger
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\CPLE3_CONTENT_TRIGGER_2026-05-08.md` (cemetery archive)_

#### CPLE3 — Content Trigger 2026-05-08

##### 🚨 Disagreement detectado

O verdict actual `AVOID` (score 3.66, polaridade -0.70) contradiz o consenso recente de 2 fontes profissionais.

- **Direcção do conflito**: 🟢 mais bullish
- **Gap de polaridade**: `1.43` (threshold 0.8)
- **Confiança média insights**: 0.89
- **Insights opostos**: 5 (de 2 fontes distintas)

##### 🎙️ Insights opostos (últimas 24h)

| Fonte | Tipo | Kind | Conf | Claim |
|---|---|---|---:|---|
| XP | analyst | rating | 0.95 | [XP Top Dividendos] CPLE3 — peso 15.0%, Compra, PT R$13.5, setor Elétricas |
| XP | analyst | rating | 0.90 | [BTG Portfolio Dividendos] CPLE3 — peso 9.6%, setor Utilities |
| XP | analyst | rating | 0.90 | [BTG Equity Brazil] CPLE3 — peso 5.1% |
| XP | analyst | rating | 0.90 | [BTG Value] CPLE3 — peso 4.3% |
| Virtual Asset | video | dividend | 0.80 | A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária. |

##### 📊 Recomendação

**Status**: REVIEW — não acção automática.

Sugestão de fluxo:
1. Lê os insights opostos acima e o verdict actual em `tickers/CPLE3.md`.
2. Se concordas com o consenso recente → `ii decide CPLE3` para re-rodar engines.
3. Se discordas (e tens conviction) → `ii actions ignore CPLE3 --note 'reason'`.
4. Se quiseres mais sinal antes de decidir → adiciona pergunta a Antonio Carlos via Telegram.

##### Cross-links

- [[tickers/CPLE3|Ticker page]]
- [[CONSTITUTION#decision-log]]
- Triggered by `auto_verdict_on_content.py` em 2026-05-08 19:50 UTC

#### 2026-05-06 · Filing 2026-05-06
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\CPLE3_FILING_2026-05-06.md` (cemetery archive)_

#### Filing dossier — [[CPLE3]] · 2026-05-06

**Trigger**: `cvm:comunicado` no dia `2026-05-06`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516536&numSequencia=1041242&numVersao=2>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 14.87

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `9.85` |
| HOLD entre | `9.85` — `12.63` (consensus) |
| TRIM entre | `12.63` — `14.52` |
| **SELL acima de** | `14.52` |

_Método: `graham_number`. Consensus fair = R$12.63. Our fair (mais conservador) = R$9.85._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.10787` | `0.085` | +21.2% |
| EPS | `0.91` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.8B (+9.4% QoQ, +18.8% YoY)
- EBIT 982.2M (-19.6% QoQ)
- Margem EBIT 14.4% vs 19.6% prior
- Lucro líquido 383.1M (-33.2% QoQ, -68.5% YoY)

**BS / cash**
- Equity 25.9B (+1.5% QoQ)
- Dívida total 20.9B (+5.2% QoQ)
- FCF proxy 269.3M (+122.2% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 12.63 | 9.85 | 14.87 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-06` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 12.63 | 9.85 | 15.47 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 12.63 | 9.85 | 15.47 | SELL | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `graham_number` | 12.63 | 9.85 | 15.47 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:33+00:00 | `graham_number` | 12.63 | 9.85 | 15.29 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-22` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-22 · Filing 2026-04-22
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\CPLE3_FILING_2026-04-22.md` (cemetery archive)_

#### Filing dossier — [[CPLE3]] · 2026-04-22

**Trigger**: `cvm:comunicado` no dia `2026-04-22`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1506999&numSequencia=1031705&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 15.29

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `9.85` |
| HOLD entre | `9.85` — `12.63` (consensus) |
| TRIM entre | `12.63` — `14.52` |
| **SELL acima de** | `14.52` |

_Método: `graham_number`. Consensus fair = R$12.63. Our fair (mais conservador) = R$9.85._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.10787` | `0.085` | +21.2% |
| EPS | `0.91` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.8B (+9.4% QoQ, +18.8% YoY)
- EBIT 982.2M (-19.6% QoQ)
- Margem EBIT 14.4% vs 19.6% prior
- Lucro líquido 383.1M (-33.2% QoQ, -68.5% YoY)

**BS / cash**
- Equity 25.9B (+1.5% QoQ)
- Dívida total 20.9B (+5.2% QoQ)
- FCF proxy 269.3M (+122.2% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:33+00:00 | `graham_number` | 12.63 | 9.85 | 15.29 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-22` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-20 · Other
_source: `videos\2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa.md`_

#### 🎬 PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CHEGANDO? VALE3 SUPERA EXPECTATIVA! B3SA3 +46% e EGIE3 2,7BI

**Canal**: Virtual Asset | **Publicado**: 2026-04-20 | **Duração**: 20min

**URL**: [https://www.youtube.com/watch?v=Wf4pWQXguPg](https://www.youtube.com/watch?v=Wf4pWQXguPg)

##### Tickers mencionados

[[B3SA3]] · [[CPLE3]] · [[EGIE3]] · [[PETR4]] · [[PRIO3]] · [[TAEE11]] · [[VALE3]]

##### Insights extraídos

###### [[VALE3]]
- [0.90 operational] A Vale aumentou a produção de minério de ferro em 3% e as vendas totais cresceram 3,9%. O preço do cobre subiu 47,8%, contribuindo para uma geração de caixa mais robusta.
- [0.70 risk] A volatilidade das commodities e a execução de projetos são fatores de atenção para os investidores na Vale.

###### [[B3SA3]]
- [0.80 operational] A B3 registrou um volume financeiro negociado de R$ 37 bilhões no primeiro trimestre de 2026, superando expectativas.
- [0.80 valuation] A B3 está negociando com múltiplos esticados, entre 16 e 17 vezes o lucro, mas os analistas reconhecem que a empresa tem fundamentos positivos.

###### [[CPLE3]]
- [0.80 dividend] A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária.
- [0.70 valuation] A Copel está negociando com múltiplos elevados, refletindo a expectativa do mercado para o futuro.

###### [[EGIE3]]
- [0.80 balance_sheet] A Engie Brasil reduziu seu saldo contábil de obrigações do balanço, passando de R$4,44 bilhões para R$2,36 bilhões.
- [0.70 operational] A Engie Brasil aprovou a repactuação de R$2,3 bilhões em concessões de suas usinas.
- [0.70 valuation] As ações da Engie Brasil (EGIE3) estão valorizando significativamente, com um PVP de 242% acima do valor patrimonial.

###### [[PETR4]]
- [0.80 guidance] A alta do barril de petróleo está impulsionando a Petrobras e outras petroleiras da bolsa.
- [0.80 valuation] A Petrobras tem um dividendo yield estimado de 6,5% para 2026 e é vista como bem posicionada no mercado.
- [0.70 valuation] A Petrobras está sendo valorizada no mercado devido à alta do barril de petróleo e sua capacidade de geração de caixa.

###### [[PRIO3]]
- [0.70 valuation] O preço-alvo da Prio foi elevado pelo Bradesco BBI de R$58,00 para R$69,00 até o final do ano de 2026.

###### [[TAEE11]]
- [0.70 valuation] TAEE11 está sendo negociada com um dividend yield de 6,20%, que é considerado enorme.

##### Temas macro

- **oil_cycle** bullish _(conf 0.90)_ — A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando a rondar os 100 dólares.
- **oil_cycle** neutral _(conf 0.80)_ — Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos anos.


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CPLE3.md` (cemetery archive)_

#### CPLE3 — Copel

#watchlist #br #utilities

##### Links

- Sector: [[sectors/Utilities|Utilities]]
- Market: [[markets/BR|BR]]
- Peers: [[ALUP11]] · [[AXIA7]] · [[CMIG4]] · [[CSMG3]] · [[EGIE3]]
- Vídeos: [[videos/2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa|PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CH]]

##### Snapshot

- **Preço**: R$15.29  (2026-05-07)    _-2.92% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 25.0/100 (RISK)

##### Fundamentals

- P/E: 16.802197 | P/B: 1.9632769 | DY: 6.95%
- ROE: 10.79% | EPS: 0.91 | BVPS: 7.788
- Streak div: 1y | Aristocrat: None

##### Dividendos recentes

- 2026-04-30: R$0.2377
- 2026-01-02: R$0.8249
- 2024-12-12: R$0.1904
- 2024-10-01: R$0.1540
- 2024-04-23: R$0.0415

##### Eventos (SEC/CVM)

- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Comunicado ao Mercado 08/
- **2026-04-22** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Comunicado ao Mercado 02/
- **2026-04-16** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Arquivamento Relatório An
- **2026-03-18** `fato_relevante` — FR 01/26 - Copel vence leilão de reserva de capacidade com duas usinas hidrelétr
- **2026-03-18** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação - Leilão de Reserva 

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=4 · themes=2_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | dividend | 0.80 | A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária. |
| 2026-04-20 | Virtual Asset | valuation | 0.70 | A Copel está negociando com múltiplos elevados, refletindo a expectativa do mercado para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] CPLE3 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] CPLE3 — peso 5.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] CPLE3 — peso 4.3% |
| 2026-04-14 | XP | rating | bull | 13.50 | [XP Top Dividendos] CPLE3 — peso 15.0%, Compra, PT R$13.5, setor Elétricas |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -9.69%
- **Drawdown 5y**: -9.69%
- **YTD**: +25.95%
- **YoY (1y)**: +42.76%
- **CAGR 3y**: +30.69%  |  **5y**: +22.82%  |  **10y**: +24.21%
- **Vol annual**: +25.45%
- **Sharpe 3y** (rf=4%): +1.12

###### Dividendos
- **DY 5y avg**: +7.16%
- **Div CAGR 5y**: +8.17%
- **Frequency**: semiannual
- **Streak** (sem cortes): 1 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "CPLE3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: CPLE3
    data: [10.99, 11.48, 11.58, 11.53, 11.66, 11.47, 11.49, 11.84, 11.75, 11.66, 11.55, 11.15, 11.29, 10.91, 10.78, 11.18, 11.52, 11.32, 11.01, 11.29, 11.2, 11.28, 11.52, 11.8, 12.01, 11.83, 11.84, 11.5, 11.69, 12.4, 12.84, 12.95, 13.61, 13.58, 13.66, 13.15, 13.62, 13.93, 13.29, 13.22, 12.71, 13.08, 12.12, 12.46, 12.27, 13.52, 13.09, 13.17, 13.99, 14.08, 14.87, 14.73, 14.45, 14.17, 15.2, 15.27, 15.02, 15.82, 16.66, 16.8, 16.81, 15.77, 15.75]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "CPLE3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2026']
series:
  - title: Dividends
    data: [0.1137, 0.1765, 0.1983, 0.2587, 0.2818, 0.6567, 0.9026, 0.304, 0.3859, 1.0626]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-21', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: P/E
    data: [18.777779, 18.677778, 18.433334, 18.433334, 18.433334, 18.11111, 17.922222, 17.522223, 17.666666, 17.633333, 17.666666, 17.5, 16.802197]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-21', '2026-04-23', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: ROE %
    data: [10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.96, 10.79]
  - title: DY %
    data: [4.88, 4.91, 4.97, 4.97, 4.97, 5.06, 5.11, 5.23, 6.68, 6.7, 6.68, 6.75, 6.95]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CPLE3_DOSSIE.md` (cemetery archive)_

#### 📑 CPLE3 — Copel

> Generated **2026-04-26** by `ii dossier CPLE3`. Cross-links: [[CPLE3]] · [[CPLE3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

CPLE3 negocia a P/E 18.43 e DY 4.97% com ROE moderado de 10.96%; preço subiu +57.3% YoY, comprimindo entry attractiveness. Synthetic IC veredicto **HOLD** (high confidence, 80% consenso) e composite conviction 68. Achado central: streak de dividendos de apenas 1 ano após a privatização — falta histórico para qualificar como DRIP, e a re-rating já consumiu o desconto pré-privatização.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.90  |  **BVPS**: 7.79
- **ROE**: 10.96%  |  **P/E**: 18.43  |  **P/B**: 2.13
- **DY**: 4.97%  |  **Streak div**: 1y  |  **Market cap**: R$ 49.27B
- **Last price**: BRL 16.59 (2026-04-24)  |  **YoY**: +57.3%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[CPLE3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: Copel, uma empresa de utilidade pública no Brasil, apresenta um P/E de 18.43 e um DY de 4.97%, com um ROE de 10.96%. Apesar do potencial valor, Copel não atende aos critérios rigorosos da filosofia investidora clássica ajustada à Selic alta.

**Key assumptions**:
1. A taxa Selic permanecerá estável ou cairá nos próximos anos
2. Copel manterá sua posição competitiva no mercado de energia elétrica e serviços relacionados
3. O fluxo de caixa operacional melhorará, permitindo um aumento sustentável dos dividendos em breve
4. A dívida líquida/EBITDA se aproximará do limite aceitável de 3x nos próximos trimestres

**Disconfirmation triggers**:
- ROE cai abaixo de 10% por dois quarters consecutivos
- Dividendos são cortados ou não aumentam após um período prolongado

→ Vault: [[CPLE3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **68** |
| Thesis health | 96 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 70 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 18.43** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 18.43** passa.
- **P/B = 2.13** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.13** — verificar consistência com ROE.
- **DY = 4.97%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.97%** abaixo do floor — DRIP não-óbvio.
- **ROE = 10.96%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **10.96%** abaixo do critério.
- **Graham Number ≈ R$ 12.56** vs preço **R$ 16.59** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 1y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Dividend streak imaturo** — apenas 1 ano pós-privatização; tese DRIP não qualificada (mínimo 5y). Trigger: `fundamentals.dividend_streak_years` < 3 mantém-se como veto.
- 🟡 **Revisão tarifária ANEEL** — distribuição (Copel DIS) entra em ciclo de revisão; WACC regulatório pode contrair. Trigger: anúncio ANEEL com mudança de WACC base.
- 🟡 **DY abaixo do mínimo** — 4.97% < 6% requerido para utility BR. Trigger: `fundamentals.dy` permanecer < 6% por 4 trimestres.
- 🟡 **Hidrologia / Copel GeT** — geração hidrelétrica exposta a GSF. Trigger: ONS GSF < 0.85.
- 🟢 **Execução pós-privatização** — sinergias prometidas no IPO podem demorar; capex elevado pode pressionar FCF. Trigger: `fundamentals.net_debt_ebitda` > 3x.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: P/E < 13 **e** DY ≥ 6% sustentado por 2 ITRs após maturação do streak (≥ 3y). Weight prudente 3-5% do book BR; só faz sentido como complemento defensivo se já tiver low exposure a utilities. Cash exclusivo BRL (BR isolation), sem deploy DRIP enquanto streak < 5y.

##### 7. Tracking triggers (auto-monitoring)

- **DY ≥ 6%** — `fundamentals.dy` ≥ 6% sustentado 2 trimestres (qualifica para screen utility BR).
- **Streak amadurece** — `fundamentals.dividend_streak_years` ≥ 3 (parcial DRIP) ou ≥ 5 (full DRIP).
- **ROE deterioração** — `fundamentals.roe` < 10% por 2 trimestres consecutivos invalida tese.
- **P/E re-rating** — `fundamentals.pe` < 13 abre ponto de entrada técnico.
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 3x.

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
*Generated by `ii dossier CPLE3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=4 · themes=2_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | dividend | 0.80 | A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária. |
| 2026-04-20 | Virtual Asset | valuation | 0.70 | A Copel está negociando com múltiplos elevados, refletindo a expectativa do mercado para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] CPLE3 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] CPLE3 — peso 5.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] CPLE3 — peso 4.3% |
| 2026-04-14 | XP | rating | bull | 13.50 | [XP Top Dividendos] CPLE3 — peso 15.0%, Compra, PT R$13.5, setor Elétricas |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CPLE3_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — CPLE3

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=0 | HOLD=4 | AVOID=1  
**Avg conviction majority**: 5.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 6/10, size: small)

**Rationale**:
- ROE abaixo da meta
- FCF inconsistente
- Dívida líquida alta

**Key risk**: Redução do ROE e falta de crescimento sustentável dos dividendos

###### 🟡 Stan Druckenmiller — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E e DY dentro da média
- ROE satisfatório, mas não excepcional
- Fluxo de caixa operacional em melhora

**Key risk**: Taxa Selic mais alta do que previsto pode pressionar margens

###### 🔴 Nassim Taleb — **AVOID** (conv 1/10, size: none)

**Rationale**:
- Taxa Selic alta
- Dívida elevada
- Falta de anti-fragilidade

**Key risk**: Leverage e fragilidade financeira em um ambiente macro incerto

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E acima da média
- ROE abaixo das expectativas
- Fluxo de caixa instável

**Key risk**: Corte ou estagnação dos dividendos em meio a volatilidade nos fluxos de caixa

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- P/E e DY dentro da média
- ROE estável mas abaixo de 15%
- Fluxo de caixa operacional instável

**Key risk**: Dívida líquida/EBITDA próximo ao limite aceitável, potencial aumento dos custos financeiros

##### 📊 Context provided

```
TICKER: BR:CPLE3

FUNDAMENTALS LATEST:
  pe: 18.433334
  pb: 2.1302004
  dy: 4.97%
  roe: 10.96%
  net_debt_ebitda: 2.7659527640877264

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=6.8 ebit=1.0 ni=0.4 em%=14.4 debt=21 fcf=0.3
  2025-06-30: rev=6.2 ebit=1.2 ni=0.6 em%=19.6 debt=20 fcf=-1.2
  2025-03-31: rev=5.9 ebit=1.4 ni=0.7 em%=23.4 debt=19 fcf=0.7
  2024-12-31: rev=6.0 ebit=0.9 ni=0.6 em%=15.3 debt=17 fcf=-3.9
  2024-09-30: rev=5.7 ebit=1.2 ni=1.2 em%=20.2 debt=16 fcf=0.8
  2024-06-30: rev=5.5 ebit=0.9 ni=0.5 em%=17.3 debt=17 fcf=0.5

VAULT THESIS:
**Core thesis (2026-04-25)**: Copel, uma empresa de utilidade pública no Brasil, apresenta um P/E de 18.43 e um DY de 4.97%, com um ROE de 10.96%. Apesar do potencial valor, Copel não atende aos critérios rigorosos da filosofia investidora clássica ajustada à Selic alta.

**Key assumptions**:
1. A taxa Selic permanecerá estável ou cairá nos próximos anos
2. Copel manterá sua posição competitiva no mercado de energia elétrica e serviços relacionados
3. O fluxo de caixa operacional melhorará, permitindo um aumento sustentável dos dividendos em breve
4. A dívida líquida/EBITDA se aproximará do limite aceitável de 3x nos próximos trimestres

**Disconfirmation triggers**:
- ROE cai abaixo de 10% por dois quarters consecutivos
- Dividendos são cortados ou não aumentam após um período prolongado 

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest - World Oil [Thu, 23 Ap]
    # Ecopetrol to acquire stake in Brazil’s Brava Energia, targets controlling interest. (WO) - **Ecopetrol** has agreed to acquire an initial equity stake in **Brava Energia** as part of a broader plan 
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global mine
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=4 · themes=2_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-20 | Virtual Asset | dividend | 0.80 | A Copel anunciou R$ 700 milhões em dividendos sob a forma de JCP, pagando R$ 0,24 por ação ordinária. |
| 2026-04-20 | Virtual Asset | valuation | 0.70 | A Copel está negociando com múltiplos elevados, refletindo a expectativa do mercado para o futuro. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] CPLE3 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] CPLE3 — peso 5.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] CPLE3 — peso 4.3% |
| 2026-04-14 | XP | rating | bull | 13.50 | [XP Top Dividendos] CPLE3 — peso 15.0%, Compra, PT R$13.5, setor Elétricas |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-20 | Virtual Asset | oil_cycle | bullish | A alta do barril de petróleo está impulsionando a Petrobras e outras empresas do setor, com o Brent voltando… |
| 2026-04-20 | Virtual Asset | oil_cycle | neutral | Embora o Brent esteja subindo, os analistas projetam uma queda gradual dos preços do petróleo nos próximos an… |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\CPLE3_RI.md` (cemetery archive)_

#### CPLE3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `net_income`: **-33.2%**
- ⬆️ **QOQ** `fcf_proxy`: **+122.2%**
- ⬇️ **QOQ** `ebit_margin`: **-5.2pp**
- ⬆️ **YOY** `revenue`: **+18.8%**
- ⬇️ **YOY** `net_income`: **-68.5%**
- ⬆️ **YOY** `debt_total`: **+29.0%**
- ⬇️ **YOY** `fcf_proxy`: **-66.7%**
- ⬇️ **YOY** `ebit_margin`: **-5.8pp**
- ⬇️ **YOY** `net_margin`: **-15.6pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 6.8 mi | R$ 6.2 mi | +9.4% |
| `ebit` | R$ 1.0 mi | R$ 1.2 mi | -19.6% |
| `net_income` | R$ 0.4 mi | R$ 0.6 mi | -33.2% |
| `debt_total` | R$ 20.9 mi | R$ 19.9 mi | +5.2% |
| `fco` | R$ 0.8 mi | R$ 0.7 mi | +3.3% |
| `fcf_proxy` | R$ 0.3 mi | R$ -1.2 mi | +122.2% |
| `gross_margin` | 18.7% | 20.9% | -2.2pp |
| `ebit_margin` | 14.4% | 19.6% | -5.2pp |
| `net_margin` | 5.6% | 9.2% | -3.6pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 6.8 mi | R$ 5.7 mi | +18.8% |
| `ebit` | R$ 1.0 mi | R$ 1.2 mi | -15.2% |
| `net_income` | R$ 0.4 mi | R$ 1.2 mi | -68.5% |
| `debt_total` | R$ 20.9 mi | R$ 16.2 mi | +29.0% |
| `fco` | R$ 0.8 mi | R$ 0.8 mi | +1.8% |
| `fcf_proxy` | R$ 0.3 mi | R$ 0.8 mi | -66.7% |
| `gross_margin` | 18.7% | 20.4% | -1.7pp |
| `ebit_margin` | 14.4% | 20.2% | -5.8pp |
| `net_margin` | 5.6% | 21.2% | -15.6pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 6.8 | 14.4% | 5.6% | 21 | 1 |
| 2025-06-30 | ITR | 6.2 | 19.6% | 9.2% | 20 | 1 |
| 2025-03-31 | ITR | 5.9 | 23.4% | 11.3% | 19 | 1 |
| 2024-12-31 | DFP-ITR | 6.0 | 15.3% | 9.6% | 17 | 1 |
| 2024-09-30 | ITR | 5.7 | 20.2% | 21.2% | 16 | 1 |
| 2024-06-30 | ITR | 5.5 | 17.3% | 8.6% | 17 | 1 |
| 2024-03-31 | ITR | 5.4 | 19.1% | 9.8% | 15 | 1 |
| 2023-12-31 | DFP-ITR | 5.6 | 21.3% | 16.9% | 15 | 1 |
| 2023-09-30 | ITR | 5.5 | 8.1% | 8.0% | 15 | 1 |
| 2023-06-30 | ITR | 5.1 | 17.0% | 6.0% | 16 | 1 |
| 2023-03-31 | ITR | 5.3 | 22.6% | 12.1% | 15 | 1 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [5.3, 5.1, 5.5, 5.6, 5.4, 5.5, 5.7, 6.0, 5.9, 6.2, 6.8]
  - title: EBIT margin %
    data: [22.6, 17.0, 8.1, 21.3, 19.1, 17.3, 20.2, 15.3, 23.4, 19.6, 14.4]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama CPLE3 --write
ii deepdive CPLE3 --save-obsidian
ii verdict CPLE3 --narrate --write
ii fv CPLE3
python -m analytics.fair_value_forward --ticker CPLE3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
