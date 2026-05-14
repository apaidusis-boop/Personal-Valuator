---
type: ticker_hub
ticker: ITUB4
market: br
sector: Banks
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# ITUB4 — Itaú Unibanco

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Banks` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `WATCH` (score 6.72, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 9.62 · P/B 2.08 · DY 8.6% · ROE 21.8% · Dividend streak 19

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\ITUB4.md` (now in cemetery)_

#### ITUB4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (1):
  - https://www.itau.com.br/relacoes-com-investidores/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=40.33000183105469
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.21816 · DY=0.0845453966078045 · P/E=9.788836
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-14 | fato_relevante | cvm | Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea |
| 2026-03-25 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |
| 2026-03-17 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência - Resultados em F |
| 2026-03-16 | fato_relevante | cvm | Pagamento de Juros sobre capital próprio |
| 2026-02-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |

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
_source: `dossiers\ITUB4_FILING_2026-05-05.md` (now in cemetery)_

#### Filing dossier — [[ITUB4]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516131&numSequencia=1040837&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 40.42

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `20.83` |
| HOLD entre | `20.83` — `28.54` (consensus) |
| TRIM entre | `28.54` — `32.82` |
| **SELL acima de** | `32.82` |

_Método: `br_bank_mult`. Consensus fair = R$28.54. Our fair (mais conservador) = R$20.83._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.21816` | `None` | +100.0% |
| EPS | `4.12` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 102.9B (+53.6% QoQ, -0.4% YoY)
- PDD -24.9B (-47.0% QoQ)
- Lucro líquido 33.7B (+52.5% QoQ, +8.7% YoY)
- Eficiência 43.1% (vs 43.9% prior)

**BS / risco**
- Carteira de crédito 1.0T (+1.0% QoQ)
- Equity 224.7B (+2.9% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `br_bank_mult` | 28.54 | 20.83 | 40.42 | SELL | disputed | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:34+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `extend_2026-05-09` |
| 2026-05-08T19:20:37+00:00 | `br_bank_mult` | 27.82 | 20.31 | 40.79 | SELL | disputed | `filing:cvm:fato_relevante:2026-04-14` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-14 · Filing 2026-04-14
_source: `dossiers\ITUB4_FILING_2026-04-14.md` (now in cemetery)_

#### Filing dossier — [[ITUB4]] · 2026-04-14

**Trigger**: `cvm:fato_relevante` no dia `2026-04-14`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504583&numSequencia=1029289&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 40.79

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `20.31` |
| HOLD entre | `20.31` — `27.82` (consensus) |
| TRIM entre | `27.82` — `31.99` |
| **SELL acima de** | `31.99` |

_Método: `br_bank_mult`. Consensus fair = R$27.82. Our fair (mais conservador) = R$20.31._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.21816` | `None` | +100.0% |
| EPS | `4.12` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 102.9B (+53.6% QoQ, -0.4% YoY)
- PDD -24.9B (-47.0% QoQ)
- Lucro líquido 33.7B (+52.5% QoQ, +8.7% YoY)
- Eficiência 43.1% (vs 43.9% prior)

**BS / risco**
- Carteira de crédito 1.0T (+1.0% QoQ)
- Equity 224.7B (+2.9% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:37+00:00 | `br_bank_mult` | 27.82 | 20.31 | 40.79 | SELL | disputed | `filing:cvm:fato_relevante:2026-04-14` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `tickers\ITUB4.md` (now in cemetery)_

#### ITUB4 — Itaú Unibanco

#watchlist #br #banks

##### Links

- Sector: [[sectors/Banks|Banks]]
- Market: [[markets/BR|BR]]
- Peers: [[BBDC4]] · [[ABCB4]] · [[BBAS3]] · [[BPAC11]] · [[SANB11]]
- Vídeos: [[videos/2026-04-21_market-makers_risco-guerra-dolar-em-queda-e-petroleo-em-alta-onde-investir-agora-mar|RISCO GUERRA, DÓLAR EM QUEDA E PETRÓLEO ]] · [[videos/2026-04-21_virtual-asset_taee11-novos-dividendos-chegando-com-100-dos-lucros-comprar-taesa-agor|TAEE11: NOVOS DIVIDENDOS CHEGANDO COM 10]] · [[videos/2026-04-07_virtual-asset_itsa4-desconto-exagerado-e-cilada-como-comprar-itub3-mais-barato-e-com|ITSA4: DESCONTO EXAGERADO É CILADA? COMO]] · [[videos/2026-03-29_o-primo-rico_o-fim-do-brasil-a-bomba-relogio-das-empresas-brasileiras-chegamos-no-l|O FIM DO BRASIL | A BOMBA-RELÓGIO DAS EM]] · [[videos/2025-08-01_suno-noticias_banco-do-brasil-bbas3-vai-decepcionar-projecoes-para-grandes-bancos|BANCO DO BRASIL (BBAS3) vai DECEPCIONAR?]]

##### Snapshot

- **Preço**: R$40.79  (2026-05-07)    _-2.37% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 68.8/100 (WATCH)

##### Fundamentals

- P/E: 9.900486 | P/B: 2.1993961 | DY: 8.36%
- ROE: 21.82% | EPS: 4.12 | BVPS: 18.546
- Streak div: 19y | Aristocrat: None

##### Dividendos recentes

- 2026-05-04: R$0.0182
- 2026-04-01: R$0.0182
- 2026-03-20: R$0.3489
- 2026-03-02: R$0.0182
- 2026-02-02: R$0.0182

##### Eventos (SEC/CVM)

- **2026-04-14** `fato_relevante` — Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea
- **2026-03-25** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Instituciona
- **2026-03-17** `comunicado` — Apresentações a analistas/agentes do mercado | Teleconferência - Resultados em F
- **2026-03-16** `fato_relevante` — Pagamento de Juros sobre capital próprio
- **2026-02-10** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Apresentação Instituciona

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=3 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | balance_sheet | 0.90 | O Itaú teve lucro líquido de R$12,3 bilhões no primeiro trimestre, um crescimento de 10,4%. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um múltiplo P/L de 5,34 vezes, considerado baixo em comparação com os padrões internacionais. |
| 2026-05-13 | Virtual Asset | operational | 0.80 | O índice de inadimplência do Itaú ficou em apenas 1,9% no primeiro trimestre. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um dividend yield de 6,90% e pode anunciar novos pagamentos de dividendos em breve. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | O Itaú tem um ROE de quase 25%, destacando-se na rentabilidade entre os bancos brasileiros. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações do Itaú (ITUB4) estão sendo vistas como uma opção barata, com dividend yield de 8,5%. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A inadimplência do Itaú está em torno de 4,2%, o que ainda exige cuidado. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A competição acirrada no setor bancário pode ser um risco para o Itaú, com outros bancos e fintechs disputando mercado. |
| 2026-05-11 | Virtual Asset | thesis_bull | 0.80 | O Itaú está isolado na liderança em termos de rentabilidade e lucratividade, o que pode continuar atraíndo investidores. |
| 2026-05-08 | Genial Investimentos | operational | 0.80 | O analista recomenda Itaú para swing trade devido ao movimento consolidado e possibilidade de pullback. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bear | — | [BTG Value] ITUB4 — peso -2.1% (SHORT) |
| 2026-04-14 | XP | rating | bull | 51.00 | [XP Top Dividendos] ITUB4 — peso 10.0%, Compra, PT R$51.0, setor Bancos |
| 2026-04-14 | XP | catalyst | neutral | — | ITUB4 reduzido de 15 para 10 por cento em abril/2026 para abrir espaço à inclusão de ROXO34 (NU). |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -17.38%
- **Drawdown 5y**: -17.38%
- **YTD**: +4.19%
- **YoY (1y)**: +19.90%
- **CAGR 3y**: +20.60%  |  **5y**: +10.84%  |  **10y**: +9.56%
- **Vol annual**: +23.52%
- **Sharpe 3y** (rf=4%): +0.75

###### Dividendos
- **DY 5y avg**: +6.26%
- **Div CAGR 5y**: +5.28%
- **Frequency**: quarterly
- **Streak** (sem cortes): 2 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$136.38B | R$29.21B | R$121.14B |
| 2023-12-31 | R$148.38B | R$33.10B | R$68.63B |
| 2024-12-31 | R$158.57B | R$41.09B | R$546.0M |
| 2025-12-31 | R$165.24B | R$44.86B | R$27.35B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ITUB4 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: ITUB4
    data: [34.29, 36.1, 37.18, 36.7, 36.34, 35.43, 35.27, 35.97, 36.17, 35.87, 36.63, 34.22, 34.17, 33.98, 33.47, 33.91, 35.71, 36.57, 35.25, 36.12, 37.37, 36.83, 36.78, 36.8, 37.32, 37.54, 36.83, 36.16, 36.36, 37.05, 36.92, 38.15, 38.96, 40.02, 39.13, 38.66, 40.43, 42.0, 38.29, 38.17, 38.46, 39.23, 39.32, 39.17, 39.55, 43.57, 46.15, 44.62, 48.42, 47.99, 48.17, 45.92, 42.93, 42.69, 42.28, 42.54, 41.6, 43.49, 46.07, 46.98, 44.18, 42.87, 41.78]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "ITUB4 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.9387, 0.882, 1.8803, 2.4753, 1.1505, 0.8003, 0.8986, 1.1091, 2.13, 4.4493, 0.4398]
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
    data: [11.44, 11.56359, 11.017456, 11.064837, 11.064837, 11.064837, 10.970075, 10.997505, 10.690772, 10.770573, 10.5735655, 10.588528, 10.418952, 9.900486]
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
    data: [20.86, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.01, 21.82]
  - title: DY %
    data: [6.77, 7.35, 7.72, 7.68, 7.68, 7.68, 7.75, 7.73, 7.95, 7.89, 8.04, 8.03, 8.16, 8.36]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\ITUB4_DOSSIE.md` (now in cemetery)_

#### 📑 ITUB4 — Itaú Unibanco

> Generated **2026-04-26** by `ii dossier ITUB4`. Cross-links: [[ITUB4]] · [[ITUB4_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

ITUB4 negocia a P/E 11.06 (acima do limite 10) e P/B 2.39 (acima do limite 1.5), mas com DY 7.68% e ROE excepcional de 21.01% com 19 anos de streak. Synthetic IC veredicto **HOLD** (medium confidence, 60% consenso) e composite conviction 73, passando 3/5 critérios do screen BR Banks. Achado central: melhor ROE do trio (21% vs 13.75% BBDC4 e 15.46% ABCB4), mas P/B premium torna a entry pouco atractiva versus BBDC4 (P/B 1.18) ou ABCB4 (P/B 0.90) com DY similar.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 4.01  |  **BVPS**: 18.55
- **ROE**: 21.01%  |  **P/E**: 11.06  |  **P/B**: 2.39
- **DY**: 7.68%  |  **Streak div**: 19y  |  **Market cap**: R$ 489.02B
- **Last price**: BRL 44.37 (2026-04-24)  |  **YoY**: +31.5%

##### 2. Screen — BR Banks (CLAUDE.md)

| Critério | Threshold | Valor | OK? |
|---|---|---|---|
| P/E ≤ 10 | ≤ 10 | **11.06** | ❌ |
| P/B ≤ 1.5 | ≤ 1.5 | **2.39** | ❌ |
| DY ≥ 6% | ≥ 6% | **7.68%** | ✅ |
| ROE ≥ 12% | ≥ 12% | **21.01%** | ✅ |
| Streak div ≥ 5y | ≥ 5 | **19y** | ✅ |

→ **3/5 critérios** passam.

##### 3. Peer comparison

###### Fundamentals

| Métrica | ITUB4 | ABCB4 | BBDC4 |
|---|---|---|---|
| Market cap | R$ 489.02B | R$ 6.52B | R$ 210.57B |
| P/E | 11.06 | 4.73 | 9.35 |
| P/B | 2.39 | 0.90 | 1.18 |
| ROE | 21.01% | 15.46% | 13.75% |
| DY | 7.68% | 10.30% | 7.56% |
| Streak div | 19y | 16y | 19y |
| YoY price | +31.5% | +21.0% | +48.9% |

###### BACEN regulatório (latest non-NULL)

| Métrica | ITUB4 | ABCB4 | BBDC4 |
|---|---|---|---|
| Período | 2025-09-30 | 2025-09-30 | 2025-09-30 |
| Basel | 16.40% | 16.71% | 15.85% |
| CET1 | 13.47% | 11.88% | 11.39% |
| NPL E-H | n/a | n/a | n/a |

##### 4. BACEN timeline — capital + crédito

| Período | Basel | CET1 | NPL E-H |
|---|---|---|---|
| 2018-03-31 | 16.61% | 14.52% | 4.67% |
| 2018-06-30 | 17.17% | 14.15% | 4.42% |
| 2018-09-30 | 16.89% | 13.94% | 4.36% |
| 2019-03-31 | 16.03% | 13.25% | 4.10% |
| 2019-06-30 | 16.32% | 13.64% | 3.89% |
| 2019-09-30 | 15.41% | 12.76% | 3.81% |
| 2020-03-31 | 13.34% | 10.32% | 3.84% |
| 2020-06-30 | 13.52% | 10.39% | 3.79% |
| 2020-09-30 | 13.75% | 10.66% | 3.36% |
| 2021-03-31 | 14.47% | 11.28% | 2.99% |
| 2021-06-30 | 14.93% | 11.92% | 3.20% |
| 2021-09-30 | 14.71% | 11.28% | 3.12% |
| 2022-03-31 | 13.93% | 11.08% | 3.57% |
| 2022-06-30 | 14.06% | 11.12% | 3.69% |
| 2022-09-30 | 14.72% | 11.65% | 3.93% |
| 2023-03-31 | 14.98% | 11.97% | 4.28% |
| 2023-06-30 | 15.13% | 12.19% | 4.37% |
| 2023-09-30 | 16.27% | 13.11% | 4.32% |
| 2023-12-31 | 17.03% | 13.69% | 4.16% |
| 2024-03-31 | 16.40% | 12.97% | 4.03% |
| 2024-06-30 | 16.56% | 13.06% | 3.80% |
| 2024-09-30 | 17.42% | 13.67% | 3.31% |
| 2024-12-31 | 16.51% | 13.66% | 3.09% |
| 2025-03-31 | 15.64% | 12.61% | pending |
| 2025-06-30 | 16.53% | 13.12% | pending |
| 2025-09-30 | 16.40% | 13.47% | pending |

- **Basel cycle peak** — pico em 2024-09-30 (17.42%) após recovery do trough COVID 2020-03 (13.34%); actual 16.40% mantém-se acima da média histórica (~15.5%) com folga regulatória confortável.
- **CET1 estabilidade** — recuperação de 10.32% (2020-Q1) para 13.47% (2025-Q3), em níveis pré-COVID; trajectória de capital orgânico saudável e suporta payout actual de DY 7.68%.
- **NPL E-H em queda** — pico ciclo recente em 2023-06 (4.37%), descendo para 3.09% (2024-Q4) antes de entrar em pending; tendência alinhada com normalização pós-Selic peak. Aguardar releases 2025 para confirmar continuação.
- **Posição peer** — Basel ITUB4 16.40% praticamente colado a ABCB4 (16.71%) e ligeiramente acima de BBDC4 (15.85%); CET1 ITUB4 13.47% lidera o trio (vs ABCB4 11.88% e BBDC4 11.39%), confirmando ITUB4 como o banco mais bem capitalizado entre os pares acompanhados.

##### 5. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[ITUB4_IC_DEBATE]]

##### 6. Thesis

**Core thesis (2026-04-25)**: Itaú Unibanco, com um ROE de 21.01% e um dividendo anual de 7.68%, oferece um retorno atrativo para investidores em busca de rendimentos estáveis. Apesar de não atender integralmente aos critérios de valor da nossa filosofia (P/E acima de 10 e P/B acima de 1,5), o banco apresenta uma história consistente de pagamentos de dividendos por 19 anos consecutivos.

**Key assumptions**:
1. Itaú Unibanco continuará a manter um ROE acima de 12% nos próximos trimestres
2. A taxa de crescimento do banco em termos de receitas e lucros mantém-se estável ou crescente
3. O nível atual da dívida a longo prazo não compromete a capacidade do banco de pagar dividendos consistentemente
4. As condições econômicas brasileiras continuam favoráveis para o setor bancário

**Disconfirma

→ Vault: [[ITUB4]]

##### 7. Conviction breakdown

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

- **P/E = 11.06** → [[Glossary/PE|porquê isto importa?]]. Bancos BR têm spread alto e múltiplos comprimidos — target ≤ 10. **Actual 11.06** NÃO passa.
- **P/B = 2.39** → [[Glossary/PB|leitura completa]]. Bancos: P/B ≤ 1.5 = margem sobre equity. **2.39** caro vs equity (mas verificar ROE).
- **DY = 7.68%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **7.68%** passa.
- **ROE = 21.01%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Bancos BR (Selic alta): target ≥ 12%. **21.01%** OK.
- **Streak div = 19y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.
- **Basel = 16.40%** → [[Glossary/Basel_Ratio|capital regulatório]]. Tier **premium** (mín BCB ~10.5%; saudável ≥14%; premium ≥16%).
- **CET1 = 13.47%** → [[Glossary/CET1|capital high-quality]]. Tier **premium** (≥11% médio peer BR; ≥13% leadership tipo ITUB4).

##### 8. Riscos identificados

- 🔴 **P/B premium vs peers** — 2.39 contra BBDC4 1.18 e ABCB4 0.90; pouco margem de segurança. Trigger: `fundamentals.pb` > 2.5 sem expansão proporcional de ROE.
- 🟡 **NPL ciclo crédito** — Selic alta historicamente eleva inadimplência com lag de 4-6 trimestres. Trigger: `bacen_quarterly.npl_eh` > 4.5% (acima do peak recente 4.37%).
- 🟡 **CET1 erosão** — actual 13.47% confortável, mas payout agressivo + crescimento book pode pressionar. Trigger: `bacen_quarterly.cet1` < 11% por 2 trimestres consecutivos.
- 🟡 **Regulamentação BACEN** — circulares sobre PDD, CMN sobre payout/dividend, ou Basel IV reforms. Trigger: `events WHERE source='cvm' AND kind LIKE '%BACEN%' OR LIKE '%CMN%'`.
- 🟢 **DY abaixo de ABCB4** — 7.68% vs 10.30% ABCB4; competitividade relativa para DRIP. Trigger: `fundamentals.dy` < 6%.

##### 9. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: P/B < 2.0 (re-rating) **e** P/E < 10 simultaneamente; preferir BBDC4 ou ABCB4 enquanto P/B premium persistir. Weight prudente 4-6% como core banking holding (qualidade de balance sheet inquestionável). Cash exclusivo BRL (BR isolation); evitar dupla-contar exposure financials se já houver BBDC4 + ABCB4 — escolher 2 dos 3.

##### 10. Tracking triggers (auto-monitoring)

- **NPL deterioração** — `bacen_quarterly.npl_eh` > 4.5% (acima do peak recente 4.37%).
- **CET1 erosão** — `bacen_quarterly.cet1` < 11% por 2 trimestres consecutivos.
- **P/B re-rating** — `fundamentals.pb` < 2.0 (entry técnico) ou > 2.7 (red flag overvaluation).
- **DY corrosão** — `fundamentals.dy` < 6% (sai do screen BR Banks).
- **ROE deterioração** — `fundamentals.roe` < 15% por 2 trimestres consecutivos.

##### 11. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| BACEN backfill | Olinda OData | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier ITUB4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=3 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | balance_sheet | 0.90 | O Itaú teve lucro líquido de R$12,3 bilhões no primeiro trimestre, um crescimento de 10,4%. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um múltiplo P/L de 5,34 vezes, considerado baixo em comparação com os padrões internacionais. |
| 2026-05-13 | Virtual Asset | operational | 0.80 | O índice de inadimplência do Itaú ficou em apenas 1,9% no primeiro trimestre. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um dividend yield de 6,90% e pode anunciar novos pagamentos de dividendos em breve. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | O Itaú tem um ROE de quase 25%, destacando-se na rentabilidade entre os bancos brasileiros. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações do Itaú (ITUB4) estão sendo vistas como uma opção barata, com dividend yield de 8,5%. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A inadimplência do Itaú está em torno de 4,2%, o que ainda exige cuidado. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A competição acirrada no setor bancário pode ser um risco para o Itaú, com outros bancos e fintechs disputando mercado. |
| 2026-05-11 | Virtual Asset | thesis_bull | 0.80 | O Itaú está isolado na liderança em termos de rentabilidade e lucratividade, o que pode continuar atraíndo investidores. |
| 2026-05-08 | Genial Investimentos | operational | 0.80 | O analista recomenda Itaú para swing trade devido ao movimento consolidado e possibilidade de pullback. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bear | — | [BTG Value] ITUB4 — peso -2.1% (SHORT) |
| 2026-04-14 | XP | rating | bull | 51.00 | [XP Top Dividendos] ITUB4 — peso 10.0%, Compra, PT R$51.0, setor Bancos |
| 2026-04-14 | XP | catalyst | neutral | — | ITUB4 reduzido de 15 para 10 por cento em abril/2026 para abrir espaço à inclusão de ROXO34 (NU). |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · IC Debate (synthetic)
_source: `tickers\ITUB4_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — ITUB4

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=1 | HOLD=4 | AVOID=0  
**Avg conviction majority**: 5.2/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- ROE alto e consistente
- História de dividendos sólida
- P/B moderado

**Key risk**: Condições econômicas brasileiras podem afetar o setor bancário

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- ROE acima de 20%
- Dividend yield atrativo
- Histórico consistente de pagamentos

**Key risk**: Volatilidade das condições econômicas brasileiras pode afetar o desempenho do banco

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Dividendos atraentes
- ROE forte
- Histórico de pagamentos

**Key risk**: Volatilidade macroeconômica e endividamento recente podem comprometer o fluxo de caixa

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE acima de 20%
- Histórico consistente de dividendos
- Setor bancário resiliente

**Key risk**: Condições econômicas adversas no Brasil podem afetar lucros

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- ROE acima de 20%
- Dividend yield atrativo
- Histórico consistente de pagamentos

**Key risk**: Dependência das condições econômicas brasileiras e gestão da dívida

##### 📊 Context provided

```
TICKER: BR:ITUB4

FUNDAMENTALS LATEST:
  pe: 10.014563
  pb: 2.2247384
  dy: 8.26%
  roe: 21.82%
  intangible_pct_assets: 0.8%   (goodwill $8.3B + intangibles $15.8B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=97.4 ebit=13.7 ni=0.0 em%=14.1 debt=74 fcf=70.4
  2025-06-30: rev=102.8 ebit=9.7 ni=0.0 em%=9.4 debt=75 fcf=23.9
  2025-03-31: rev=97.5 ebit=12.9 ni=0.0 em%=13.2 debt=72 fcf=7.9
  2024-12-31: rev=91.2 ebit=13.1 ni=0.0 em%=14.3 debt=0 fcf=-17.8
  2024-09-30: rev=77.9 ebit=10.0 ni=0.0 em%=12.8 debt=60 fcf=6.9
  2024-06-30: rev=86.2 ebit=12.3 ni=0.0 em%=14.2 debt=146 fcf=-16.6

VAULT THESIS:
**Core thesis (2026-04-25)**: Itaú Unibanco, com um ROE de 21.01% e um dividendo anual de 7.68%, oferece um retorno atrativo para investidores em busca de rendimentos estáveis. Apesar de não atender integralmente aos critérios de valor da nossa filosofia (P/E acima de 10 e P/B acima de 1,5), o banco apresenta uma história consistente de pagamentos de dividendos por 19 anos consecutivos.

**Key assumptions**:
1. Itaú Unibanco continuará a manter um ROE acima de 12% nos próximos trimestres
2. A taxa de crescimento do banco em termos de receitas e lucros mantém-se estável ou crescente
3. O nível atual da dívida a longo prazo não compromete a capacidade do banco de pagar dividendos consistentemente
4. As condições econômicas brasileiras continuam favoráveis para o setor bancário

**Disconfirma
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=3 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Virtual Asset | balance_sheet | 0.90 | O Itaú teve lucro líquido de R$12,3 bilhões no primeiro trimestre, um crescimento de 10,4%. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um múltiplo P/L de 5,34 vezes, considerado baixo em comparação com os padrões internacionais. |
| 2026-05-13 | Virtual Asset | operational | 0.80 | O índice de inadimplência do Itaú ficou em apenas 1,9% no primeiro trimestre. |
| 2026-05-13 | Virtual Asset | valuation | 0.80 | O Itaú tem um dividend yield de 6,90% e pode anunciar novos pagamentos de dividendos em breve. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | O Itaú tem um ROE de quase 25%, destacando-se na rentabilidade entre os bancos brasileiros. |
| 2026-05-11 | Virtual Asset | valuation | 0.90 | As ações do Itaú (ITUB4) estão sendo vistas como uma opção barata, com dividend yield de 8,5%. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A inadimplência do Itaú está em torno de 4,2%, o que ainda exige cuidado. |
| 2026-05-11 | Virtual Asset | risk | 0.80 | A competição acirrada no setor bancário pode ser um risco para o Itaú, com outros bancos e fintechs disputando mercado. |
| 2026-05-11 | Virtual Asset | thesis_bull | 0.80 | O Itaú está isolado na liderança em termos de rentabilidade e lucratividade, o que pode continuar atraíndo investidores. |
| 2026-05-08 | Genial Investimentos | operational | 0.80 | O analista recomenda Itaú para swing trade devido ao movimento consolidado e possibilidade de pullback. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bear | — | [BTG Value] ITUB4 — peso -2.1% (SHORT) |
| 2026-04-14 | XP | rating | bull | 51.00 | [XP Top Dividendos] ITUB4 — peso 10.0%, Compra, PT R$51.0, setor Bancos |
| 2026-04-14 | XP | catalyst | neutral | — | ITUB4 reduzido de 15 para 10 por cento em abril/2026 para abrir espaço à inclusão de ROXO34 (NU). |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · RI / disclosure
_source: `tickers\ITUB4_RI.md` (now in cemetery)_

#### ITUB4 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+42.0%**
- ⬆️ **QOQ** `fco`: **+444.7%**
- ⬆️ **QOQ** `fcf_proxy`: **+194.6%**
- ⬆️ **YOY** `revenue`: **+25.0%**
- ⬆️ **YOY** `ebit`: **+37.1%**
- ⬆️ **YOY** `fco`: **+310.8%**
- ⬆️ **YOY** `fcf_proxy`: **+914.4%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 97.4 mi | R$ 102.8 mi | -5.2% |
| `ebit` | R$ 13.7 mi | R$ 9.7 mi | +42.0% |
| `net_income` | R$ 0.0 mi | R$ 0.0 mi | — |
| `debt_total` | R$ 73.8 mi | R$ 75.5 mi | -2.3% |
| `fco` | R$ 75.7 mi | R$ 13.9 mi | +444.7% |
| `fcf_proxy` | R$ 70.4 mi | R$ 23.9 mi | +194.6% |
| `gross_margin` | 36.9% | 30.7% | +6.2pp |
| `ebit_margin` | 14.1% | 9.4% | +4.7pp |
| `net_margin` | 0.0% | 0.0% | +0.0pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 97.4 mi | R$ 77.9 mi | +25.0% |
| `ebit` | R$ 13.7 mi | R$ 10.0 mi | +37.1% |
| `net_income` | R$ 0.0 mi | R$ 0.0 mi | — |
| `debt_total` | R$ 73.8 mi | R$ 59.6 mi | +23.8% |
| `fco` | R$ 75.7 mi | R$ -35.9 mi | +310.8% |
| `fcf_proxy` | R$ 70.4 mi | R$ 6.9 mi | +914.4% |
| `gross_margin` | 36.9% | 45.3% | -8.4pp |
| `ebit_margin` | 14.1% | 12.8% | +1.2pp |
| `net_margin` | 0.0% | 0.0% | +0.0pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 97.4 | 14.1% | 0.0% | 74 | 76 |
| 2025-06-30 | ITR | 102.8 | 9.4% | 0.0% | 75 | 14 |
| 2025-03-31 | ITR | 97.5 | 13.2% | 0.0% | 72 | -12 |
| 2024-12-31 | DFP-ITR | 91.2 | 14.3% | 0.0% | 0 | -4 |
| 2024-09-30 | ITR | 77.9 | 12.8% | 0.0% | 60 | -36 |
| 2024-06-30 | ITR | 86.2 | 14.2% | 0.0% | 146 | -1 |
| 2024-03-31 | ITR | 80.0 | 15.3% | 0.0% | 58 | 48 |
| 2023-12-31 | DFP-ITR | 75.1 | 13.4% | 0.0% | 59 | -15 |
| 2023-09-30 | ITR | 80.4 | 13.0% | 0.0% | 116 | 34 |
| 2023-06-30 | ITR | 82.0 | 13.3% | 0.0% | 118 | 13 |
| 2023-03-31 | ITR | 75.7 | 10.9% | 0.0% | 134 | 45 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [75.7, 82.0, 80.4, 75.1, 80.0, 86.2, 77.9, 91.2, 97.5, 102.8, 97.4]
  - title: EBIT margin %
    data: [10.9, 13.3, 13.0, 13.4, 15.3, 14.2, 12.8, 14.3, 13.2, 9.4, 14.1]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama ITUB4 --write
ii deepdive ITUB4 --save-obsidian
ii verdict ITUB4 --narrate --write
ii fv ITUB4
python -m analytics.fair_value_forward --ticker ITUB4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
