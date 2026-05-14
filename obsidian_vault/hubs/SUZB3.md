---
type: ticker_hub
ticker: SUZB3
market: br
sector: Materials
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 7
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# SUZB3 — Suzano

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Materials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 5.16, 2026-05-08)
- **Fundamentals** (2026-05-13): P/E 4.68 · P/B 1.21 · DY 2.6% · ROE 26.3% · ND/EBITDA 3.63 · Dividend streak 5

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\SUZB3.md` (now in cemetery)_

#### SUZB3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://ri.suzano.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **11**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=43.130001068115234
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.26295 · DY=0.025994411598306812 · P/E=4.6931453
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação de Resultados 1T26 |
| 2026-04-02 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| L |
| 2026-03-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| 1 |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Termo de Emissão (CPR-F) |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aprovação da 2° Oferta pú |

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
_source: `dossiers\SUZB3_CONTENT_TRIGGER_2026-05-08.md` (now in cemetery)_

#### SUZB3 — Content Trigger 2026-05-08

##### 🚨 Disagreement detectado

O verdict actual `AVOID` (score 5.16, polaridade -0.70) contradiz o consenso recente de 2 fontes profissionais.

- **Direcção do conflito**: 🟢 mais bullish
- **Gap de polaridade**: `1.36` (threshold 0.8)
- **Confiança média insights**: 0.83
- **Insights opostos**: 3 (de 2 fontes distintas)

##### 🎙️ Insights opostos (últimas 24h)

| Fonte | Tipo | Kind | Conf | Claim |
|---|---|---|---:|---|
| XP | analyst | rating | 0.90 | [BTG Equity Brazil] SUZB3 — peso 4.1% |
| XP | analyst | rating | 0.90 | [BTG Value] SUZB3 — peso 3.0% |
| Virtual Asset | video | operational | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$1 |

##### 📊 Recomendação

**Status**: REVIEW — não acção automática.

Sugestão de fluxo:
1. Lê os insights opostos acima e o verdict actual em `tickers/SUZB3.md`.
2. Se concordas com o consenso recente → `ii decide SUZB3` para re-rodar engines.
3. Se discordas (e tens conviction) → `ii actions ignore SUZB3 --note 'reason'`.
4. Se quiseres mais sinal antes de decidir → adiciona pergunta a Antonio Carlos via Telegram.

##### Cross-links

- [[tickers/SUZB3|Ticker page]]
- [[CONSTITUTION#decision-log]]
- Triggered by `auto_verdict_on_content.py` em 2026-05-08 19:50 UTC

#### 2026-04-30 · Filing 2026-04-30
_source: `dossiers\SUZB3_FILING_2026-04-30.md` (now in cemetery)_

#### Filing dossier — [[SUZB3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1511860&numSequencia=1036566&numVersao=1>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 43.30

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 38% margem) | `53.08` |
| HOLD entre | `53.08` — `85.62` (consensus) |
| TRIM entre | `85.62` — `98.46` |
| **SELL acima de** | `98.46` |

_Método: `graham_number`. Consensus fair = R$85.62. Our fair (mais conservador) = R$53.08._

##### 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.26295` | `0.1652` | +37.2% |
| EPS | `9.19` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 12.2B (-8.6% QoQ, -1.0% YoY)
- EBIT 2.0B (-31.5% QoQ)
- Margem EBIT 16.2% vs 21.6% prior
- Lucro líquido 2.0B (-60.9% QoQ, -39.4% YoY)

**BS / cash**
- Equity 45.3B (+4.6% QoQ)
- Dívida total 93.0B (+1.5% QoQ)
- FCF proxy 762.1M (+247.6% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:59+00:00 | `graham_number` | 85.62 | 53.08 | 43.30 | SELL | single_source | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `tickers\SUZB3.md` (now in cemetery)_

#### SUZB3 — SUZB3

#watchlist #br #materials

##### Links

- Sector: [[sectors/Materials|Materials]]
- Market: [[markets/BR|BR]]
- Peers: [[KLBN11]] · [[BRKM5]] · [[KLBN4]] · [[UNIP6]]
- Vídeos: [[videos/2026-04-16_virtual-asset_bbdc3-ou-bbdc4-o-banco-mais-barato-com-145-bi-de-dividendos-e-70-de-al|BBDC3 OU BBDC4? O BANCO MAIS BARATO COM ]]

##### Snapshot

- **Preço**: R$43.30  (2026-05-07)    _+0.67% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 68.0/100 (WATCH)

##### Fundamentals

- P/E: 4.711643 | P/B: 1.221473 | DY: 2.59%
- ROE: 26.3% | EPS: 9.19 | BVPS: 35.449
- Streak div: 5y | Aristocrat: None

##### Dividendos recentes

- 2026-04-30: R$0.0046
- 2025-12-19: R$1.1166
- 2024-12-17: R$2.0174
- 2023-12-08: R$1.1634
- 2022-12-19: R$1.7948

##### Eventos (SEC/CVM)

- **2026-04-30** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação de Resultados 1T26
- **2026-04-02** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Comunicado ao Mercado | L
- **2026-03-10** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Comunicado ao Mercado | 1
- **2026-03-09** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Termo de Emissão (CPR-F)
- **2026-03-09** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Aprovação da 2° Oferta pú

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-16 | Virtual Asset | valuation | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |
| 2026-04-16 | Virtual Asset | operational | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] SUZB3 — peso 4.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] SUZB3 — peso 3.0% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco apresenta resultados positivos, com crescimento na carteira de crédito e margem financeira líquida… |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026, indicando… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -26.59%
- **Drawdown 5y**: -36.76%
- **YTD**: -16.52%
- **YoY (1y)**: -15.50%
- **CAGR 3y**: +1.13%  |  **5y**: -8.47%  |  **10y**: +8.02%
- **Vol annual**: +26.36%
- **Sharpe 3y** (rf=4%): -0.11

###### Dividendos
- **DY 5y avg**: +3.50%
- **Div CAGR 5y**: -5.76%
- **Frequency**: annual
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$49.83B | R$40.18B | R$23.38B |
| 2023-12-31 | R$39.76B | R$29.40B | R$14.08B |
| 2024-12-31 | R$47.40B | R$1.02B | R$-7.07B |
| 2025-12-31 | R$50.12B | R$37.86B | R$13.41B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "SUZB3 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: SUZB3
    data: [51.47, 53.01, 53.02, 52.76, 49.65, 52.9, 52.98, 52.64, 51.85, 51.21, 51.95, 49.85, 50.52, 51.26, 52.15, 51.74, 54.14, 53.86, 53.01, 53.41, 52.45, 51.67, 50.8, 50.68, 50.35, 49.45, 50.1, 47.83, 47.99, 47.71, 49.1, 48.69, 48.9, 46.55, 48.5, 47.98, 47.58, 49.54, 51.67, 48.92, 51.2, 51.45, 49.94, 51.51, 51.85, 52.25, 49.36, 49.6, 51.12, 57.2, 58.58, 58.06, 54.92, 53.47, 52.56, 51.17, 50.56, 49.6, 47.16, 47.53, 46.69, 44.82, 43.01]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "SUZB3 — dividend history"
labels: ['2016', '2017', '2018', '2019', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.258, 0.183, 0.1922, 0.4447, 3.1288, 1.1634, 2.0174, 1.1166, 0.0046]
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
    data: [4.57, 4.417745, 4.3191485, 4.2220163, 4.218115, 4.218115, 4.1866913, 4.200555, 4.142329, 4.051756, 4.6383443, 4.6187363, 4.680087, 4.711643]
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
    data: [30.51, 35.19, 35.19, 35.19, 35.19, 35.19, 35.19, 35.19, 35.19, 35.19, 26.3, 26.3, 26.3, 26.3]
  - title: DY %
    data: [2.3, 2.34, 2.39, 2.45, 2.45, 2.45, 2.46, 2.46, 2.49, 2.56, 2.63, 2.64, 2.61, 2.59]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\SUZB3_DOSSIE.md` (now in cemetery)_

#### 📑 SUZB3 — Suzano

> Generated **2026-04-26** by `ii dossier SUZB3`. Cross-links: [[SUZB3]] · [[SUZB3_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

SUZB3 negocia P/E baixíssimo de 4.22 e P/B 1.29 com ROE robusto de 35.19%, mas DY apenas 2.45% e streak curta de 4y. IC consensus HOLD (medium, 60%) — divergência típica de cíclica de commodity: lucros actuais elevados (FX favorável + preço BHKP) com risco evidente de mean-reversion. Achado-chave: P/E 4 num ROE 35% é o mercado a precificar pico de ciclo da celulose; entrada exige convicção sobre cenário USD/BRL e demanda China — não tese DRIP.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 10.82  |  **BVPS**: 35.45
- **ROE**: 35.19%  |  **P/E**: 4.22  |  **P/B**: 1.29
- **DY**: 2.45%  |  **Streak div**: 4y  |  **Market cap**: R$ 56.42B
- **Last price**: BRL 45.64 (2026-04-24)  |  **YoY**: -12.7%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[SUZB3_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A Suzano (SUZB3) é uma empresa de materiais com um P/E baixo de 4.22, indicando que o preço da ação está abaixo do valor intrínseco comparado à sua lucratividade. Apesar de ter um ROE robusto de 35.19%, a empresa não atende aos critérios de dividend yield e Net Debt/EBITDA estabelecidos na filosofia de investimento.

**Key assumptions**:
1. A demanda por papelão ondulado continuará crescendo, mantendo os preços das commodities em níveis elevados
2. O cenário macroeconômico brasileiro permitirá que a empresa reduza sua dívida líquida de forma sustentável
3. Os dividendos continuarão sendo pagos e o histórico de pagamento será estendido para mais de 5 anos
4. A Selic permanecerá em níveis elevados, mantendo a atratividade das ações com P/E baixo

**Disconfirmati

→ Vault: [[SUZB3]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **72** |
| Thesis health | 96 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 90 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 4.22** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 4.22** passa.
- **P/B = 1.29** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.29** — verificar consistência com ROE.
- **DY = 2.45%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **2.45%** abaixo do floor — DRIP não-óbvio.
- **ROE = 35.19%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **35.19%** compounder-grade.
- **Graham Number ≈ R$ 92.90** vs preço **R$ 45.64** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 4y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Preço BHKP / ciclo celulose** — receita altamente sensível a preço FOB China; queda de 20% destrói lucro. Trigger: BHKP spot China YoY <-15% (vault commodity note ou release).
- 🔴 **Exposição USD/BRL** — receita exportadora; BRL forte comprime EBITDA mesmo com volume estável. Trigger: `macro.usdbrl` <5.0 sustentado.
- 🟡 **Demanda China** — papel/celulose dependente de consumo asiático; risco macro chinês. Trigger: imports China celulose YoY <-10%.
- 🟡 **Streak curta + DY baixo** — 4y de pagamento e DY 2.45% afastam-se totalmente do critério DRIP. Trigger: `fundamentals.dy < 2%` consolida desqualificação.
- 🟢 **Custo cash competitivo** — Suzano é low-cost producer global; floor parcial em ciclos baixos. Trigger: gross margin YoY <-500bp em 2 trimestres → competitividade erodida.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Tese só faz sentido como tactical (cycle play / FX hedge), não como DRIP. Entry trigger: pullback >-25% combinado com BHKP a recuperar OU USD/BRL >5.5 sustentado. Weight prudente 2-3% como Tier-3 (cíclica de commodity).

##### 7. Tracking triggers (auto-monitoring)

- **ROE mean-revert** — `fundamentals.roe < 18%` em release → tese de pico confirmada.
- **FX shock** — `macro.usdbrl` < 5.0 sustentado >60d → comprime EBITDA exportador.
- **PE inflation** — `fundamentals.pe > 12` → mercado já reprecificou ciclo, downside.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 3.5` → risco financeiro com lucro a normalizar.
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
*Generated by `ii dossier SUZB3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-16 | Virtual Asset | valuation | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |
| 2026-04-16 | Virtual Asset | operational | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] SUZB3 — peso 4.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] SUZB3 — peso 3.0% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco apresenta resultados positivos, com crescimento na carteira de crédito e margem financeira líquida… |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026, indicando… |

#### — · IC Debate (synthetic)
_source: `tickers\SUZB3_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — SUZB3

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=1 | HOLD=3 | AVOID=1  
**Avg conviction majority**: 5.3/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE robusto
- P/E baixo
- Demanda por papelão ondulado

**Key risk**: Flutuações macroeconômicas e de commodities afetam lucratividade

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E baixo e ROE forte
- Potencial de redução da dívida
- Atratividade com Selic alta

**Key risk**: Flutuações nos preços das commodities podem afetar significativamente os resultados

###### 🔴 Nassim Taleb — **AVOID** (conv 10/10, size: none)

**Rationale**:
- Net Debt/EBITDA alto
- Intangíveis significativos
- Fluxo de caixa volátil

**Key risk**: Leverage e fragilidade financeira em um cenário macro incerto

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: small)

**Rationale**:
- P/E baixo, ROE robusto
- Demanda por papelão ondulado crescente
- Selic elevada

**Key risk**: Risco de redução da dívida líquida em cenário macroeconômico desfavorável

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E baixo sugere valorização
- ROE forte indica solidez financeira
- CF livre oscila significativamente

**Key risk**: Flutuações nos fluxos de caixa podem comprometer a sustentabilidade da dívida

##### 📊 Context provided

```
TICKER: BR:SUZB3

FUNDAMENTALS LATEST:
  pe: 4.755169
  pb: 1.2327569
  dy: 2.57%
  roe: 26.30%
  net_debt_ebitda: 3.627541230396124
  intangible_pct_assets: 7.7%   (goodwill $8.2B + intangibles $4.8B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=12.2 ebit=2.0 ni=2.0 em%=16.2 debt=93 fcf=0.8
  2025-06-30: rev=13.3 ebit=2.9 ni=5.0 em%=21.6 debt=92 fcf=-0.5
  2025-03-31: rev=11.6 ebit=2.3 ni=6.3 em%=19.6 debt=91 fcf=7.7
  2024-12-31: rev=14.2 ebit=4.4 ni=-6.7 em%=31.1 debt=101 fcf=0.4
  2024-09-30: rev=12.3 ebit=4.1 ni=3.2 em%=33.5 debt=88 fcf=0.1
  2024-06-30: rev=11.5 ebit=4.6 ni=-3.8 em%=40.1 debt=89 fcf=2.5

VAULT THESIS:
**Core thesis (2026-04-25)**: A Suzano (SUZB3) é uma empresa de materiais com um P/E baixo de 4.22, indicando que o preço da ação está abaixo do valor intrínseco comparado à sua lucratividade. Apesar de ter um ROE robusto de 35.19%, a empresa não atende aos critérios de dividend yield e Net Debt/EBITDA estabelecidos na filosofia de investimento.

**Key assumptions**:
1. A demanda por papelão ondulado continuará crescendo, mantendo os preços das commodities em níveis elevados
2. O cenário macroeconômico brasileiro permitirá que a empresa reduza sua dívida líquida de forma sustentável
3. Os dividendos continuarão sendo pagos e o histórico de pagamento será estendido para mais de 5 anos
4. A Selic permanecerá em níveis elevados, mantendo a atratividade das ações com P/E baixo

**Disconfirmati
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=2 · analyst=2 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-04-16 | Virtual Asset | valuation | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |
| 2026-04-16 | Virtual Asset | operational | 0.70 | É possível comprar ações SUZB3 por R$45,63 se o preço estiver em R$15,63 ou abaixo no dia 15 de maio, recebendo um prêmio entre R$1,10 e R$… |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] SUZB3 — peso 4.1% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] SUZB3 — peso 3.0% |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência das pessoas físicas piorou ligeiramente, mas a carteira de crédito continua crescendo e as de… |
| 2026-04-16 | Virtual Asset | banking_br | neutral | A inadimplência e as despesas com PDDs aumentaram, o que causou preocupação no mercado. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco apresenta resultados positivos, com crescimento na carteira de crédito e margem financeira líquida… |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026. |
| 2026-04-16 | Virtual Asset | banking_br | bullish | O Bradesco espera um crescimento maior na carteira de crédito e margem financeira líquida em 2026, indicando… |

#### — · RI / disclosure
_source: `tickers\SUZB3_RI.md` (now in cemetery)_

#### SUZB3 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬇️ **QOQ** `ebit`: **-31.5%**
- ⬇️ **QOQ** `net_income`: **-60.9%**
- ⬆️ **QOQ** `fcf_proxy`: **+247.6%**
- ⬇️ **QOQ** `ebit_margin`: **-5.4pp**
- ⬇️ **QOQ** `net_margin`: **-21.6pp**
- ⬇️ **YOY** `ebit`: **-52.1%**
- ⬇️ **YOY** `net_income`: **-39.4%**
- ⬆️ **YOY** `fcf_proxy`: **+450.2%**
- ⬇️ **YOY** `ebit_margin`: **-17.3pp**
- ⬇️ **YOY** `net_margin`: **-10.2pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 12.2 mi | R$ 13.3 mi | -8.6% |
| `ebit` | R$ 2.0 mi | R$ 2.9 mi | -31.5% |
| `net_income` | R$ 2.0 mi | R$ 5.0 mi | -60.9% |
| `debt_total` | R$ 93.0 mi | R$ 91.6 mi | +1.5% |
| `fco` | R$ 4.0 mi | R$ 4.3 mi | -7.1% |
| `fcf_proxy` | R$ 0.8 mi | R$ -0.5 mi | +247.6% |
| `gross_margin` | 30.4% | 35.3% | -4.8pp |
| `ebit_margin` | 16.2% | 21.6% | -5.4pp |
| `net_margin` | 16.1% | 37.7% | -21.6pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 12.2 mi | R$ 12.3 mi | -1.0% |
| `ebit` | R$ 2.0 mi | R$ 4.1 mi | -52.1% |
| `net_income` | R$ 2.0 mi | R$ 3.2 mi | -39.4% |
| `debt_total` | R$ 93.0 mi | R$ 87.8 mi | +5.9% |
| `fco` | R$ 4.0 mi | R$ 5.3 mi | -23.6% |
| `fcf_proxy` | R$ 0.8 mi | R$ 0.1 mi | +450.2% |
| `gross_margin` | 30.4% | 44.2% | -13.8pp |
| `ebit_margin` | 16.2% | 33.5% | -17.3pp |
| `net_margin` | 16.1% | 26.4% | -10.2pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 12.2 | 16.2% | 16.1% | 93 | 4 |
| 2025-06-30 | ITR | 13.3 | 21.6% | 37.7% | 92 | 4 |
| 2025-03-31 | ITR | 11.6 | 19.6% | 54.9% | 91 | 4 |
| 2024-12-31 | DFP-ITR | 14.2 | 31.1% | -47.5% | 101 | 6 |
| 2024-09-30 | ITR | 12.3 | 33.5% | 26.4% | 88 | 5 |
| 2024-06-30 | ITR | 11.5 | 40.1% | -32.8% | 89 | 6 |
| 2024-03-31 | ITR | 9.5 | 27.0% | 2.3% | 79 | 3 |
| 2023-12-31 | DFP-ITR | 10.4 | 30.4% | 43.5% | 77 | 5 |
| 2023-09-30 | ITR | 8.9 | 18.8% | -8.1% | 79 | 2 |
| 2023-06-30 | ITR | 9.2 | 33.5% | 55.4% | 75 | 6 |
| 2023-03-31 | ITR | 11.3 | 38.2% | 46.5% | 73 | 4 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [11.3, 9.2, 8.9, 10.4, 9.5, 11.5, 12.3, 14.2, 11.6, 13.3, 12.2]
  - title: EBIT margin %
    data: [38.2, 33.5, 18.8, 30.4, 27.0, 40.1, 33.5, 31.1, 19.6, 21.6, 16.2]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama SUZB3 --write
ii deepdive SUZB3 --save-obsidian
ii verdict SUZB3 --narrate --write
ii fv SUZB3
python -m analytics.fair_value_forward --ticker SUZB3
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
