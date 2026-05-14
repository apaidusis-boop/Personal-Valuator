---
type: ticker_hub
ticker: MULT3
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

# MULT3 — Multiplan

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Real Estate` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `WATCH` (score 6.7, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 11.87 · P/B 2.28 · DY 3.7% · ROE 20.0% · ND/EBITDA 2.40 · Dividend streak 18

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\MULT3.md` (now in cemetery)_

#### MULT3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://www.multri.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=31.010000228881836
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.20018 · DY=0.03493205391824209 · P/E=12.554656
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Data de eficácia da capit |
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência de Resultados - 1 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Participação de executivo |
| 2026-04-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Alienação de Participação |
| 2026-04-07 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Reunião Pública Multiplan 2026 -  |

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
_source: `dossiers\MULT3_FILING_2026-05-07.md` (now in cemetery)_

#### Filing dossier — [[MULT3]] · 2026-05-07

**Trigger**: `cvm:fato_relevante` no dia `2026-05-07`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1518048&numSequencia=1042754&numVersao=2>

##### 🎯 Acção sugerida

###### 🟠 **TRIM** &mdash; preço 30.15

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `23.27` |
| HOLD entre | `23.27` — `26.75` (consensus) |
| TRIM entre | `26.75` — `30.76` |
| **SELL acima de** | `30.76` |

_Método: `graham_number`. Consensus fair = R$26.75. Our fair (mais conservador) = R$23.27._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20018` | `0.2114` | +5.3% |
| EPS | `2.47` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 617.5M (-11.0% QoQ, +13.3% YoY)
- EBIT 403.7M (-5.4% QoQ)
- Margem EBIT 65.4% vs 61.5% prior
- Lucro líquido 221.2M (-16.4% QoQ, -20.9% YoY)

**BS / cash**
- Equity 6.0B (+1.9% QoQ)
- Dívida total 5.5B (+7.1% QoQ)
- FCF proxy -92.8M (-113.1% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 26.75 | 23.27 | 30.15 | TRIM | cross_validated | `filing:cvm:fato_relevante:2026-05-07` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 26.75 | 23.27 | 31.80 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 26.75 | 23.27 | 31.80 | SELL | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 26.75 | 23.27 | 31.80 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:42+00:00 | `graham_number` | 26.75 | 23.27 | 31.41 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Filing 2026-04-30
_source: `dossiers\MULT3_FILING_2026-04-30.md` (now in cemetery)_

#### Filing dossier — [[MULT3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513707&numSequencia=1038413&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 31.41

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `23.27` |
| HOLD entre | `23.27` — `26.75` (consensus) |
| TRIM entre | `26.75` — `30.76` |
| **SELL acima de** | `30.76` |

_Método: `graham_number`. Consensus fair = R$26.75. Our fair (mais conservador) = R$23.27._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20018` | `0.2114` | +5.3% |
| EPS | `2.47` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 617.5M (-11.0% QoQ, +13.3% YoY)
- EBIT 403.7M (-5.4% QoQ)
- Margem EBIT 65.4% vs 61.5% prior
- Lucro líquido 221.2M (-16.4% QoQ, -20.9% YoY)

**BS / cash**
- Equity 6.0B (+1.9% QoQ)
- Dívida total 5.5B (+7.1% QoQ)
- FCF proxy -92.8M (-113.1% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:42+00:00 | `graham_number` | 26.75 | 23.27 | 31.41 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `tickers\MULT3.md` (now in cemetery)_

#### MULT3 — MULT3

#watchlist #br #real_estate

##### Links

- Sector: [[sectors/Real_Estate|Real Estate]]
- Market: [[markets/BR|BR]]
- Peers: [[ALOS3]] · [[EZTC3]]

##### Snapshot

- **Preço**: R$31.41  (2026-05-07)    _-3.03% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 95.0/100 (SAFE)

##### Fundamentals

- P/E: 12.7165985 | P/B: 2.4399905 | DY: 3.45%
- ROE: 20.02% | EPS: 2.47 | BVPS: 12.873
- Streak div: 18y | Aristocrat: None

##### Dividendos recentes

- 2026-03-31: R$0.2855
- 2025-12-30: R$0.3065
- 2025-09-29: R$0.2456
- 2025-06-30: R$0.2456
- 2025-04-01: R$0.2252

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Data de eficácia da capit
- **2026-04-30** `comunicado` — Apresentações a analistas/agentes do mercado | Teleconferência de Resultados - 1
- **2026-04-29** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Participação de executivo
- **2026-04-20** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Alienação de Participação
- **2026-04-07** `comunicado` — Apresentações a analistas/agentes do mercado | Reunião Pública Multiplan 2026 - 

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=2 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-09 | Inter Invest | valuation | 0.90 | O analista recomenda comprar ações da Multiplan na quebra de R$32,5. |
| 2026-05-09 | Inter Invest | catalyst | 0.80 | O analista sugere que a Multiplan pode ter um potencial de alta, comparando com uma flâmula técnica. |
| 2026-05-09 | Inter Invest | operational | 0.70 | O analista menciona que o varejo está com dificuldades, mas ainda assim vê potencial na Multiplan. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MULT3 — peso 2.7% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MULT3 — peso 3.8% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-09 | Inter Invest | oil_cycle | bearish | O analista menciona preocupação com a queda do preço da Petrobras seguindo o petróleo, sugerindo um possível… |
| 2026-05-09 | Inter Invest | semis_cycle | bearish | O analista menciona a Aura 33 como um papel com potencial de queda, sugerindo uma tendência bearish. |
| 2026-05-09 | Inter Invest | usdbrl | bearish | O analista sugere que a tendência do dólar é de queda, indicando um momento não ideal para exposição em BDRs. |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -12.26%
- **Drawdown 5y**: -12.26%
- **YTD**: +16.16%
- **YoY (1y)**: +24.15%
- **CAGR 3y**: +5.32%  |  **5y**: +4.82%  |  **10y**: +5.20%
- **Vol annual**: +25.42%
- **Sharpe 3y** (rf=4%): +0.05

###### Dividendos
- **DY 5y avg**: +3.53%
- **Div CAGR 5y**: +30.17%
- **Frequency**: quarterly
- **Streak** (sem cortes): 1 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$1.80B | R$1.40B | R$769.3M |
| 2023-12-31 | R$2.03B | R$1.65B | R$1.02B |
| 2024-12-31 | R$2.54B | R$2.00B | R$1.34B |
| 2025-12-31 | R$2.74B | R$2.14B | R$1.14B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "MULT3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: MULT3
    data: [26.02, 25.67, 26.49, 26.08, 26.88, 26.25, 25.93, 26.23, 27.1, 27.21, 27.17, 26.25, 25.94, 25.09, 24.84, 25.65, 26.1, 26.52, 26.11, 26.77, 27.85, 27.69, 28.05, 28.72, 28.76, 28.9, 28.3, 27.53, 27.04, 27.49, 27.69, 27.86, 28.67, 29.37, 29.58, 29.35, 30.16, 30.71, 28.93, 27.66, 26.68, 27.25, 27.3, 28.69, 29.25, 31.28, 32.65, 32.91, 33.63, 33.14, 34.85, 34.11, 31.93, 30.97, 30.62, 31.24, 30.66, 31.77, 33.51, 34.41, 32.85, 31.56, 32.39]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "MULT3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.1683, 0.4013, 0.3192, 0.4365, 0.6059, 0.4989, 0.7169, 0.9963, 0.6238, 1.4322, 0.2855]
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
    data: [15.43, 14.969565, 14.282608, 14.230434, 14.230434, 14.230434, 14.126088, 14.017392, 13.721739, 13.791305, 13.573913, 12.7044525, 13.113359, 12.7165985]
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
    data: [18.11, 19.11, 19.11, 19.11, 19.11, 19.11, 19.11, 19.11, 19.11, 19.11, 19.11, 20.02, 20.02, 20.02]
  - title: DY %
    data: [2.32, 3.15, 3.3, 3.31, 3.31, 3.31, 3.33, 3.36, 3.43, 3.42, 3.47, 3.45, 3.34, 3.45]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\MULT3_DOSSIE.md` (now in cemetery)_

#### 📑 MULT3 — Multiplan

> Generated **2026-04-26** by `ii dossier MULT3`. Cross-links: [[MULT3]] · [[MULT3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

MULT3 negocia P/E 14.23 e P/B 2.54 com ROE 19.11% e streak excepcional de 18 anos, mas DY 3.31% fica abaixo do floor 6%. IC consensus HOLD (high, 80%) reflecte qualidade de operador líder de malls com track record longo, contrabalançada por valuation premium e yield baixo. Achado-chave: peer leader vs ALOS3 — ROE quase 3× superior (19% vs 7%), justificando P/B premium, mas o yield é metade.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.30  |  **BVPS**: 12.87
- **ROE**: 19.11%  |  **P/E**: 14.23  |  **P/B**: 2.54
- **DY**: 3.31%  |  **Streak div**: 18y  |  **Market cap**: R$ 16.05B
- **Last price**: BRL 32.73 (2026-04-24)  |  **YoY**: +30.1%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MULT3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: MULT3 é um fundo imobiliário focado em ativos de tijolo, com forte histórico de dividendos e ROE acima da média. Apesar do P/B estar ligeiramente alto (2.54), o DY de 3.31% ainda oferece uma vantagem relativa ao mercado brasileiro, embora esteja abaixo da faixa ideal para FIIs de 8-12%.

**Key assumptions**:
1. O P/VP manterá-se em um nível sustentável e não subirá acima do patamar atual
2. A taxa de vacância permanecerá estável ou diminuirá nos próximos trimestres, mantendo a geração de renda
3. Os ativos imobiliários continuarão gerando retornos superiores à média do setor, apoiados pelo ROE de 19.11%
4. A dívida líquida/EBITDA se manterá em um nível administrável (2.64), sem pressões significativas para aumentar

**Disconfirmation triggers**:
- ROE cai abai

→ Vault: [[MULT3]]

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

- **P/E = 14.23** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 14.23** passa.
- **P/B = 2.54** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.54** — verificar consistência com ROE.
- **DY = 3.31%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **3.31%** abaixo do floor — DRIP não-óbvio.
- **ROE = 19.11%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **19.11%** compounder-grade.
- **Graham Number ≈ R$ 25.81** vs preço **R$ 32.73** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🟡 **Valuation premium** — P/B 2.54× é o dobro de ALOS3; pouco margem de segurança. Trigger: `fundamentals.pb > 3.0` invalida ponto de entrada.
- 🟡 **Yield abaixo do critério** — DY 3.31% vs floor 6% impossibilita classificação como DRIP defensivo. Trigger: `fundamentals.dy < 3%` consolida desqualificação.
- 🟡 **Vacância em malls premium** — exposição a consumo discricionário e juros altos pode pressionar NOI. Trigger: NOI YoY <-3% em 2 trimestres consecutivos (release).
- 🟢 **ND/EBITDA controlado** — 2.64× dentro do limite, baixa pressão financeira; risco baixo. Trigger: `fundamentals.net_debt_ebitda > 3.5` para alarme.
- 🟡 **Compressão por juros** — yield baixo perde competitividade vs NTN-B em ciclo Selic alta. Trigger: `macro.selic_meta` delta >+50bp.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Entry trigger: pullback que leve P/B <2.0× combinado com DY ≥4.5%, ou tese reframe como compounder de qualidade em vez de DRIP. Weight prudente 3-5% como Tier-2 (mall premium, exposição cíclica).

##### 7. Tracking triggers (auto-monitoring)

- **Valuation pullback** — `fundamentals.pb < 2.0` → reabrir tese de entrada.
- **DY upgrade** — `fundamentals.dy > 4.5%` → começa a competir com peers/NTN-B.
- **ROE drop** — `fundamentals.roe < 12%` → perda do diferencial vs ALOS3.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 3.0` → alerta de pressão financeira.
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
*Generated by `ii dossier MULT3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=2 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-09 | Inter Invest | valuation | 0.90 | O analista recomenda comprar ações da Multiplan na quebra de R$32,5. |
| 2026-05-09 | Inter Invest | catalyst | 0.80 | O analista sugere que a Multiplan pode ter um potencial de alta, comparando com uma flâmula técnica. |
| 2026-05-09 | Inter Invest | operational | 0.70 | O analista menciona que o varejo está com dificuldades, mas ainda assim vê potencial na Multiplan. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MULT3 — peso 2.7% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MULT3 — peso 3.8% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-09 | Inter Invest | oil_cycle | bearish | O analista menciona preocupação com a queda do preço da Petrobras seguindo o petróleo, sugerindo um possível… |
| 2026-05-09 | Inter Invest | semis_cycle | bearish | O analista menciona a Aura 33 como um papel com potencial de queda, sugerindo uma tendência bearish. |
| 2026-05-09 | Inter Invest | usdbrl | bearish | O analista sugere que a tendência do dólar é de queda, indicando um momento não ideal para exposição em BDRs. |

#### — · IC Debate (synthetic)
_source: `tickers\MULT3_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — MULT3

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=1 | HOLD=4 | AVOID=0  
**Avg conviction majority**: 5.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE acima de 15%
- P/B ligeiramente alto
- DY abaixo da faixa ideal

**Key risk**: Possível queda no ROE e aumento na taxa de vacância

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- ROE acima da média
- Dividend yield atrativo
- Liquidez administrável

**Key risk**: Aumento significativo na taxa de vacância ou queda acentuada no ROE

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/B ligeiramente alto
- DY abaixo da faixa ideal para FIIs
- ROE acima média, mas volatilidade em resultados

**Key risk**: Flutuações significativas no ROE e geração de caixa livre

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: small)

**Rationale**:
- P/B ligeiramente alto
- ROE acima da média
- Dividend yield atrativo

**Key risk**: Aumento da taxa de vacância e pressão sobre o P/VP

###### 🟡 Ray Dalio — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- ROE acima da média
- Dividend yield atrativo
- Dívida administrável

**Key risk**: P/B alto e possibilidade de aumento na vacância imobiliária

##### 📊 Context provided

```
TICKER: BR:MULT3

FUNDAMENTALS LATEST:
  pe: 12.874494
  pb: 2.4702866
  dy: 3.41%
  roe: 20.02%
  net_debt_ebitda: 2.403232364628092
  intangible_pct_assets: 3.1%   (goodwill $0.3B + intangibles $0.1B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=0.6 ebit=0.4 ni=0.2 em%=65.4 debt=5 fcf=-0.1
  2025-06-30: rev=0.7 ebit=0.4 ni=0.3 em%=61.5 debt=5 fcf=0.7
  2025-03-31: rev=0.5 ebit=0.4 ni=0.2 em%=68.8 debt=5 fcf=0.3
  2024-12-31: rev=0.9 ebit=0.6 ni=0.5 em%=67.4 debt=5 fcf=0.5
  2024-09-30: rev=0.5 ebit=0.4 ni=0.3 em%=67.3 debt=4 fcf=-0.3
  2024-06-30: rev=0.5 ebit=0.4 ni=0.3 em%=65.9 debt=3 fcf=0.3

VAULT THESIS:
**Core thesis (2026-04-25)**: MULT3 é um fundo imobiliário focado em ativos de tijolo, com forte histórico de dividendos e ROE acima da média. Apesar do P/B estar ligeiramente alto (2.54), o DY de 3.31% ainda oferece uma vantagem relativa ao mercado brasileiro, embora esteja abaixo da faixa ideal para FIIs de 8-12%.

**Key assumptions**:
1. O P/VP manterá-se em um nível sustentável e não subirá acima do patamar atual
2. A taxa de vacância permanecerá estável ou diminuirá nos próximos trimestres, mantendo a geração de renda
3. Os ativos imobiliários continuarão gerando retornos superiores à média do setor, apoiados pelo ROE de 19.11%
4. A dívida líquida/EBITDA se manterá em um nível administrável (2.64), sem pressões significativas para aumentar

**Disconfirmation triggers**:
- ROE cai abai
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=3 · analyst=2 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-09 | Inter Invest | valuation | 0.90 | O analista recomenda comprar ações da Multiplan na quebra de R$32,5. |
| 2026-05-09 | Inter Invest | catalyst | 0.80 | O analista sugere que a Multiplan pode ter um potencial de alta, comparando com uma flâmula técnica. |
| 2026-05-09 | Inter Invest | operational | 0.70 | O analista menciona que o varejo está com dificuldades, mas ainda assim vê potencial na Multiplan. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] MULT3 — peso 2.7% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] MULT3 — peso 3.8% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-09 | Inter Invest | oil_cycle | bearish | O analista menciona preocupação com a queda do preço da Petrobras seguindo o petróleo, sugerindo um possível… |
| 2026-05-09 | Inter Invest | semis_cycle | bearish | O analista menciona a Aura 33 como um papel com potencial de queda, sugerindo uma tendência bearish. |
| 2026-05-09 | Inter Invest | usdbrl | bearish | O analista sugere que a tendência do dólar é de queda, indicando um momento não ideal para exposição em BDRs. |

#### — · RI / disclosure
_source: `tickers\MULT3_RI.md` (now in cemetery)_

#### MULT3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `revenue`: **-11.0%**
- ⬆️ **QOQ** `fco`: **+44.1%**
- ⬇️ **QOQ** `fcf_proxy`: **-113.1%**
- ⬆️ **YOY** `revenue`: **+13.3%**
- ⬇️ **YOY** `net_income`: **-20.9%**
- ⬆️ **YOY** `debt_total`: **+52.3%**
- ⬆️ **YOY** `fco`: **+30.4%**
- ⬆️ **YOY** `fcf_proxy`: **+68.9%**
- ⬇️ **YOY** `net_margin`: **-15.5pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 0.6 mi | R$ 0.7 mi | -11.0% |
| `ebit` | R$ 0.4 mi | R$ 0.4 mi | -5.4% |
| `net_income` | R$ 0.2 mi | R$ 0.3 mi | -16.3% |
| `debt_total` | R$ 5.5 mi | R$ 5.1 mi | +7.1% |
| `fco` | R$ 0.3 mi | R$ 0.2 mi | +44.1% |
| `fcf_proxy` | R$ -0.1 mi | R$ 0.7 mi | -113.1% |
| `gross_margin` | 80.3% | 77.3% | +3.0pp |
| `ebit_margin` | 65.4% | 61.5% | +3.9pp |
| `net_margin` | 35.8% | 38.1% | -2.3pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 0.6 mi | R$ 0.5 mi | +13.3% |
| `ebit` | R$ 0.4 mi | R$ 0.4 mi | +10.1% |
| `net_income` | R$ 0.2 mi | R$ 0.3 mi | -20.9% |
| `debt_total` | R$ 5.5 mi | R$ 3.6 mi | +52.3% |
| `fco` | R$ 0.3 mi | R$ 0.3 mi | +30.4% |
| `fcf_proxy` | R$ -0.1 mi | R$ -0.3 mi | +68.9% |
| `gross_margin` | 80.3% | 83.8% | -3.5pp |
| `ebit_margin` | 65.4% | 67.3% | -1.9pp |
| `net_margin` | 35.8% | 51.3% | -15.5pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 0.6 | 65.4% | 35.8% | 5 | 0 |
| 2025-06-30 | ITR | 0.7 | 61.5% | 38.1% | 5 | 0 |
| 2025-03-31 | ITR | 0.5 | 68.8% | 44.5% | 5 | 0 |
| 2024-12-31 | DFP-ITR | 0.9 | 67.4% | 54.7% | 5 | 1 |
| 2024-09-30 | ITR | 0.5 | 67.3% | 51.3% | 4 | 0 |
| 2024-06-30 | ITR | 0.5 | 65.9% | 52.2% | 3 | 0 |
| 2024-03-31 | ITR | 0.5 | 68.0% | 51.0% | 3 | 0 |
| 2023-12-31 | DFP-ITR | 0.6 | 63.0% | 53.0% | 3 | 0 |
| 2023-09-30 | ITR | 0.5 | 70.1% | 52.0% | 3 | 0 |
| 2023-06-30 | ITR | 0.5 | 68.4% | 50.7% | 3 | 0 |
| 2023-03-31 | ITR | 0.5 | 66.9% | 44.6% | 3 | 0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [0.5, 0.5, 0.5, 0.6, 0.5, 0.5, 0.5, 0.9, 0.5, 0.7, 0.6]
  - title: EBIT margin %
    data: [66.9, 68.4, 70.1, 63.0, 68.0, 65.9, 67.3, 67.4, 68.8, 61.5, 65.4]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama MULT3 --write
ii deepdive MULT3 --save-obsidian
ii verdict MULT3 --narrate --write
ii fv MULT3
python -m analytics.fair_value_forward --ticker MULT3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
