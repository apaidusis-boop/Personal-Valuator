---
type: ticker_hub
ticker: RAPT4
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

# RAPT4 — Randoncorp

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Industrials` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `AVOID` (score 2.15, 2026-05-13)
- **Fundamentals** (2026-05-13): P/B 0.53 · ROE -1.3% · ND/EBITDA 3.55 · Dividend streak 9

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\RAPT4.md` (cemetery archive)_

#### RAPT4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.randoncorp.com/
- **Pilot rationale**: heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.25
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=-0.0129700005 · DY=None · P/E=None
- Score (último run): score=0.3333 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Mar/20 |
| 2026-03-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Fev/20 |
| 2026-03-13 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Videoconferência de  |
| 2026-03-12 | fato_relevante | cvm | Guidance 2026 - Projeções |
| 2026-02-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Jan/20 |

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
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RAPT4_FILING_2026-05-08.md` (cemetery archive)_

#### Filing dossier — [[RAPT4]] · 2026-05-08

**Trigger**: `cvm:comunicado` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1518456&numSequencia=1043162&numVersao=1>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `-0.0129700005` | `0.075` | +117.3% |
| EPS | `-0.72` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.4B (+4.4% QoQ, +9.9% YoY)
- EBIT 363.2M (+54.6% QoQ)
- Margem EBIT 10.5% vs 7.1% prior
- Lucro líquido 90.0M (+8302.6% QoQ, -54.1% YoY)

**BS / cash**
- Equity 4.7B (+8.6% QoQ)
- Dívida total 9.3B (+4.1% QoQ)
- FCF proxy 505.0M (+515.8% QoQ)

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-20 · Filing 2026-04-20
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RAPT4_FILING_2026-04-20.md` (cemetery archive)_

#### Filing dossier — [[RAPT4]] · 2026-04-20

**Trigger**: `cvm:comunicado` no dia `2026-04-20`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1506453&numSequencia=1031159&numVersao=1>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `-0.0129700005` | `0.075` | +117.3% |
| EPS | `-0.72` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.4B (+4.4% QoQ, +9.9% YoY)
- EBIT 363.2M (+54.6% QoQ)
- Margem EBIT 10.5% vs 7.1% prior
- Lucro líquido 90.0M (+8302.6% QoQ, -54.1% YoY)

**BS / cash**
- Equity 4.7B (+8.6% QoQ)
- Dívida total 9.3B (+4.1% QoQ)
- FCF proxy 505.0M (+515.8% QoQ)

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RAPT4.md` (cemetery archive)_

#### RAPT4 — RAPT4

#watchlist #br #industrials

##### Links

- Sector: [[sectors/Industrials|Industrials]]
- Market: [[markets/BR|BR]]
- Peers: [[MOTV3]] · [[POMO3]] · [[RENT3]] · [[SIMH3]] · [[TUPY3]]

##### Snapshot

- **Preço**: R$5.28  (2026-05-07)    _-1.49% 1d_
- **Screen**: 0.3333  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 20.0/100 (RISK)

##### Fundamentals

- P/E: None | P/B: 0.56945646 | DY: None%
- ROE: -1.3% | EPS: -0.72 | BVPS: 9.272
- Streak div: 9y | Aristocrat: None

##### Dividendos recentes

- 2025-05-02: R$0.0467
- 2024-12-20: R$0.2094
- 2024-07-23: R$0.1543
- 2023-12-21: R$0.3594
- 2023-07-24: R$0.2224

##### Eventos (SEC/CVM)

- **2026-04-20** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Divulgação Receita Mar/20
- **2026-03-20** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Divulgação Receita Fev/20
- **2026-03-13** `comunicado` — Apresentações a analistas/agentes do mercado | Apresentação Videoconferência de 
- **2026-03-12** `fato_relevante` — Guidance 2026 - Projeções
- **2026-02-20** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Divulgação Receita Jan/20

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RAPT4 — peso 1.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RAPT4 — peso 2.0% |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -43.10%
- **Drawdown 5y**: -65.17%
- **YTD**: -3.30%
- **YoY (1y)**: -37.29%
- **CAGR 3y**: -16.35%  |  **5y**: -18.17%  |  **10y**: +6.51%
- **Vol annual**: +40.64%
- **Sharpe 3y** (rf=4%): -0.57

###### Dividendos
- **DY 5y avg**: +5.11%
- **Div CAGR 5y**: -36.48%
- **Frequency**: semiannual
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$11.15B | R$1.78B | R$471.7M |
| 2023-12-31 | R$10.89B | R$1.92B | R$381.7M |
| 2024-12-31 | R$11.92B | R$2.02B | R$408.5M |
| 2025-12-31 | R$13.14B | R$1.58B | R$-250.7M |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "RAPT4 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: RAPT4
    data: [8.52, 8.05, 8.59, 8.32, 9.07, 8.98, 8.78, 9.12, 8.71, 8.91, 8.77, 8.38, 8.04, 7.13, 6.93, 7.15, 6.98, 6.28, 6.49, 6.63, 6.75, 6.7, 6.72, 6.67, 6.45, 6.18, 5.84, 5.64, 5.29, 5.71, 5.98, 5.96, 6.1, 6.21, 6.12, 5.94, 6.62, 6.8, 6.12, 5.92, 5.32, 5.65, 6.14, 6.33, 6.58, 6.81, 6.71, 6.32, 6.42, 6.42, 6.71, 6.56, 6.0, 5.53, 4.72, 5.1, 5.32, 5.15, 5.56, 5.46, 5.46, 5.19, 5.36]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "RAPT4 — dividend history"
labels: ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
series:
  - title: Dividends
    data: [0.0438, 0.102, 0.3589, 0.2419, 0.6528, 0.86, 0.5818, 0.3636, 0.0467]
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
    data: [-7.77, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    data: [-5.28, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3]
  - title: DY %
    data: [0.84, 0.84, 0.86, 0.88, 0.88, 0.88, 0.89, 0.89, 0.9, 0.88, 0, 0, 0, 0]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RAPT4_DOSSIE.md` (cemetery archive)_

#### 📑 RAPT4 — Randoncorp

> Generated **2026-04-26** by `ii dossier RAPT4`. Cross-links: [[RAPT4]] · [[RAPT4_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

RAPT4 está em prejuízo (EPS -0.72, ROE -1.30%, P/E n/a) com DY 0.88% e P/B 0.57 (50% abaixo do livro). IC consensus HOLD (medium, 60%) — divergência reflecte trade-off entre tese contrarian de turnaround (P/B baixo, streak 9y) e fundamentos actualmente negativos. Achado-chave: queda de -41% YoY mais ROE negativo coloca a empresa em zona de distress; entrada pré-virada de ciclo automotivo só faz sentido com sinal de recuperação operacional, não baseada apenas em valuation.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: -0.72  |  **BVPS**: 9.27
- **ROE**: -1.30%  |  **P/E**: n/a  |  **P/B**: 0.57
- **DY**: 0.88%  |  **Streak div**: 9y  |  **Market cap**: R$ 1.86B
- **Last price**: BRL 5.32 (2026-04-24)  |  **YoY**: -41.0%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[RAPT4_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A RAPT4 opera no setor industrial brasileiro e, apesar de apresentar um ROE negativo recentemente (-1.30%), possui um P/B baixo (0.57) indicando potencial valor oculto. No entanto, a empresa não atende aos critérios do Graham Number ajustado à Selic alta, pois seu DY é muito abaixo da meta de 6% (apenas 0.88%).

**Key assumptions**:
1. A RAPT4 melhorará sua margem operacional e aumentará seus lucros em breve, revertendo o ROE negativo.
2. O mercado industrial no Brasil continuará a se recuperar, impulsionando as receitas da empresa.
3. A dívida líquida/EBITDA (3.55) permanecerá estável ou melhorará com novas medidas de gestão financeira.
4. Apesar do DY baixo atualmente, a RAPT4 aumentará significativamente seus dividendos nos próximos anos.

**Disconfirmation

→ Vault: [[RAPT4]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **58** |
| Thesis health | 91 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 30 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **DY = 0.88%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **0.88%** abaixo do floor — DRIP não-óbvio.
- **Streak div = 9y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Prejuízo operacional actual** — ROE -1.30% e EPS -0.72; risco de continuar a queimar equity. Trigger: `fundamentals.roe < 0` em mais 1 trimestre → distress confirmado.
- 🔴 **Alavancagem alta com prejuízo** — ND/EBITDA 3.55× combinada com EBIT em queda amplifica risco financeiro. Trigger: `fundamentals.net_debt_ebitda > 4.0` ou cobertura juros <2×.
- 🔴 **Ciclo autopeças/caminhões** — exposição a transporte rodoviário e venda de caminhões pesados; sensível a Selic alta e safra agrícola. Trigger: produção ANFAVEA caminhões YoY <-15%.
- 🟡 **Streak div em risco** — 9y de streak ameaçados por prejuízo; corte iminente. Trigger: dividendo trimestral = 0 num release.
- 🟢 **Floor por P/B** — 0.57× dá margem de segurança patrimonial parcial, mas não protege contra burn. Trigger: `fundamentals.pb > 0.9` para reabrir tese.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist BR (caixa BRL only). NÃO entrar enquanto ROE negativo persistir — paciência paga em distress. Entry trigger: 2 trimestres consecutivos de ROE >5% + EBIT YoY positivo. Weight pequeno 1-2% como Tier-3 (cycle play, não DRIP).

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 5%` por 2 trimestres → sinal de virada de ciclo.
- **Deleverage** — `fundamentals.net_debt_ebitda < 3.0` → pressão financeira reduz.
- **Distress confirm** — `fundamentals.roe < -3%` ou Altman Z <1.8 → exit consideration.
- **Dividend cut** — dividendo trimestral = 0 → streak quebrada, tese DRIP morta.
- **Conviction drop** — `conviction_scores.composite_score < 50` → flag review.

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
*Generated by `ii dossier RAPT4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RAPT4 — peso 1.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RAPT4 — peso 2.0% |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RAPT4_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — RAPT4

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 4.3/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 1/10, size: none)

**Rationale**:
- ROE negativo
- FCF inconsistente
- DY baixo

**Key risk**: Margem operacional e lucratividade podem não se recuperar conforme esperado

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- P/B baixo indica valor oculto
- Margem operacional em recuperação
- Setor industrial brasileiro em melhora

**Key risk**: DY muito baixo e ROE negativo recentemente

###### 🔴 Nassim Taleb — **AVOID** (conv 10/10, size: none)

**Rationale**:
- ROE negativo
- DY baixo
- FCF instável

**Key risk**: Leverage e fragilidade financeira com FCF variando entre positivo e negativo

###### 🟡 Seth Klarman — **HOLD** (conv 4/10, size: small)

**Rationale**:
- P/B baixo indica valor oculto
- Melhora esperada na margem operacional
- Dívida líquida/EBITDA estável

**Key risk**: Possível atraso ou interrupção de projetos industriais por questões políticas

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/B baixo indica valor oculto
- Margem operacional em recuperação
- Dívida/EBITDA estável

**Key risk**: Possível interrupção de vendas por intervenção política

##### 📊 Context provided

```
TICKER: BR:RAPT4

FUNDAMENTALS LATEST:
  pb: 0.57377046
  dy: 0.88%
  roe: -1.30%
  net_debt_ebitda: 3.5491276068687663

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=3.4 ebit=0.4 ni=0.1 em%=10.5 debt=9 fcf=0.5
  2025-06-30: rev=3.3 ebit=0.2 ni=-0.0 em%=7.1 debt=9 fcf=-0.1
  2025-03-31: rev=3.2 ebit=0.2 ni=0.0 em%=7.1 debt=9 fcf=-2.0
  2024-12-31: rev=3.3 ebit=0.3 ni=0.2 em%=9.9 debt=7 fcf=0.0
  2024-09-30: rev=3.1 ebit=0.4 ni=0.2 em%=12.4 debt=6 fcf=-0.5
  2024-06-30: rev=3.0 ebit=0.3 ni=0.1 em%=10.1 debt=6 fcf=0.2

VAULT THESIS:
**Core thesis (2026-04-25)**: A RAPT4 opera no setor industrial brasileiro e, apesar de apresentar um ROE negativo recentemente (-1.30%), possui um P/B baixo (0.57) indicando potencial valor oculto. No entanto, a empresa não atende aos critérios do Graham Number ajustado à Selic alta, pois seu DY é muito abaixo da meta de 6% (apenas 0.88%).

**Key assumptions**:
1. A RAPT4 melhorará sua margem operacional e aumentará seus lucros em breve, revertendo o ROE negativo.
2. O mercado industrial no Brasil continuará a se recuperar, impulsionando as receitas da empresa.
3. A dívida líquida/EBITDA (3.55) permanecerá estável ou melhorará com novas medidas de gestão financeira.
4. Apesar do DY baixo atualmente, a RAPT4 aumentará significativamente seus dividendos nos próximos anos.

**Disconfirmation

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Brazil Party Asks Court to Halt Rare Earths Miner’s Sale - Bloomberg.com [Sat, 25 Ap]
    # Brazil Party Asks Court to Halt Rare Earths Miner’s Sale. Provide news feedback or report an error. Left-wing Brazilian political party Rede Sustentabilidade asked the country’s Supreme Court to sus
  - Rare Earths Americas announces IPO - Bitget [Wed, 15 Ap]
    Rare Earths Americas, a company advancing a portfolio of prospective heavy rare earths projects in the US and Brazil, announced Tuesday it has filed a registration statement with the Securities and Ex
  - Brazil party asks court to halt rare ear
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=2 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] RAPT4 — peso 1.9% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] RAPT4 — peso 2.0% |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\RAPT4_RI.md` (cemetery archive)_

#### RAPT4 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+54.6%**
- ⬆️ **QOQ** `net_income`: **+8302.6%**
- ⬆️ **QOQ** `fco`: **+224.5%**
- ⬆️ **QOQ** `fcf_proxy`: **+515.8%**
- ⬇️ **YOY** `net_income`: **-54.1%**
- ⬆️ **YOY** `debt_total`: **+55.9%**
- ⬆️ **YOY** `fco`: **+342.7%**
- ⬆️ **YOY** `fcf_proxy`: **+193.7%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.4 mi | R$ 3.3 mi | +4.4% |
| `ebit` | R$ 0.4 mi | R$ 0.2 mi | +54.6% |
| `net_income` | R$ 0.1 mi | R$ -0.0 mi | +8302.6% |
| `debt_total` | R$ 9.3 mi | R$ 9.0 mi | +4.1% |
| `fco` | R$ 0.6 mi | R$ 0.2 mi | +224.5% |
| `fcf_proxy` | R$ 0.5 mi | R$ -0.1 mi | +515.8% |
| `gross_margin` | 26.3% | 24.2% | +2.1pp |
| `ebit_margin` | 10.5% | 7.1% | +3.4pp |
| `net_margin` | 2.6% | -0.0% | +2.6pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 3.4 mi | R$ 3.1 mi | +9.9% |
| `ebit` | R$ 0.4 mi | R$ 0.4 mi | -6.6% |
| `net_income` | R$ 0.1 mi | R$ 0.2 mi | -54.1% |
| `debt_total` | R$ 9.3 mi | R$ 6.0 mi | +55.9% |
| `fco` | R$ 0.6 mi | R$ -0.3 mi | +342.7% |
| `fcf_proxy` | R$ 0.5 mi | R$ -0.5 mi | +193.7% |
| `gross_margin` | 26.3% | 26.3% | +0.0pp |
| `ebit_margin` | 10.5% | 12.4% | -1.9pp |
| `net_margin` | 2.6% | 6.3% | -3.6pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 3.4 | 10.5% | 2.6% | 9 | 1 |
| 2025-06-30 | ITR | 3.3 | 7.1% | -0.0% | 9 | 0 |
| 2025-03-31 | ITR | 3.2 | 7.1% | 1.5% | 9 | 0 |
| 2024-12-31 | DFP-ITR | 3.3 | 9.9% | 6.1% | 7 | 1 |
| 2024-09-30 | ITR | 3.1 | 12.4% | 6.3% | 6 | -0 |
| 2024-06-30 | ITR | 3.0 | 10.1% | 4.6% | 6 | 0 |
| 2024-03-31 | ITR | 2.5 | 10.5% | 6.3% | 6 | -0 |
| 2023-12-31 | DFP-ITR | 2.6 | 8.0% | 4.8% | 5 | 1 |
| 2023-09-30 | ITR | 2.9 | 11.3% | 5.7% | 5 | 1 |
| 2023-06-30 | ITR | 2.8 | 13.6% | 6.7% | 5 | 1 |
| 2023-03-31 | ITR | 2.7 | 14.2% | 7.0% | 5 | -0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [2.7, 2.8, 2.9, 2.6, 2.5, 3.0, 3.1, 3.3, 3.2, 3.3, 3.4]
  - title: EBIT margin %
    data: [14.2, 13.6, 11.3, 8.0, 10.5, 10.1, 12.4, 9.9, 7.1, 7.1, 10.5]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama RAPT4 --write
ii deepdive RAPT4 --save-obsidian
ii verdict RAPT4 --narrate --write
ii fv RAPT4
python -m analytics.fair_value_forward --ticker RAPT4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
