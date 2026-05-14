---
type: ticker_hub
ticker: AXIA7
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

# AXIA7 — Axia Energia

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Utilities` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `7 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 2.68, 2026-05-13)
- **Fundamentals** (2026-05-13): P/B 1.24 · ROE 7.9% · ND/EBITDA 4.23

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\AXIA7.md` (cemetery archive)_

#### AXIA7 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (2):
  - https://ri.axiaenergia.com.br/
  - https://ri.light.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **33**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=55.09000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.07862 · DY=None · P/E=None
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Arquivamento do Form 20-F |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado - A |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reapresentação de BVD |
| 2026-04-01 | fato_relevante | cvm | Aprovação de Migração para o Novo Mercado |
| 2026-04-01 | fato_relevante | cvm | Deslistagem dos Americans Depositary Recepits - ADRs |

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

#### 2026-05-06 · Filing 2026-05-06
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AXIA7_FILING_2026-05-06.md` (cemetery archive)_

#### Filing dossier — [[AXIA7]] · 2026-05-06

**Trigger**: `cvm:fato_relevante` no dia `2026-05-06`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517234&numSequencia=1041940&numVersao=1>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.07862` | `-0.0304` | +138.7% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.3B (+7.3% QoQ, -59.0% YoY)
- EBIT 850.4M (+10977.8% QoQ)
- Margem EBIT 36.4% vs -0.4% prior
- Lucro líquido 190.5M (+156.1% QoQ, -93.6% YoY)

**BS / cash**
- Equity 33.7B (+0.6% QoQ)
- Dívida total 8.7B (-0.3% QoQ)
- FCF proxy -157.9M (-144.2% QoQ)

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-24 · Filing 2026-04-24
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\AXIA7_FILING_2026-04-24.md` (cemetery archive)_

#### Filing dossier — [[AXIA7]] · 2026-04-24

**Trigger**: `cvm:comunicado` no dia `2026-04-24`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1508583&numSequencia=1033289&numVersao=1>

##### 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

##### 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.05455` | `-0.0304` | +155.7% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.3B (+7.3% QoQ, -59.0% YoY)
- EBIT 850.4M (+10977.8% QoQ)
- Margem EBIT 36.4% vs -0.4% prior
- Lucro líquido 190.5M (+156.1% QoQ, -93.6% YoY)

**BS / cash**
- Equity 33.7B (+0.6% QoQ)
- Dívida total 8.7B (-0.3% QoQ)
- FCF proxy -157.9M (-144.2% QoQ)

##### 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AXIA7.md` (cemetery archive)_

#### AXIA7 — AXIA7

#watchlist #br #utilities

##### Links

- Sector: [[sectors/Utilities|Utilities]]
- Market: [[markets/BR|BR]]
- Peers: [[ALUP11]] · [[CMIG4]] · [[CPLE3]] · [[CSMG3]] · [[EGIE3]]

##### Snapshot

- **Preço**: R$55.80  (2026-05-07)    _-5.76% 1d_
- **Screen**: 0.0  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 25.0/100 (RISK)

##### Fundamentals

- P/E: None | P/B: 1.3452915 | DY: None%
- ROE: 5.46% | EPS: None | BVPS: 41.478
- Streak div: Noney | Aristocrat: None

##### Eventos (SEC/CVM)

- **2026-04-24** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Arquivamento do Form 20-F
- **2026-04-16** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Comunicado ao Mercado - A
- **2026-04-06** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Reapresentação de BVD
- **2026-04-01** `fato_relevante` — Aprovação de Migração para o Novo Mercado
- **2026-04-01** `fato_relevante` — Deslistagem dos Americans Depositary Recepits - ADRs

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=5 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] AXIA7 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] AXIA7 — peso 8.3% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] AXIA7 — peso 4.9% |
| 2026-04-24 | XP | catalyst | neutral | — | Troca AXIA6 por AXIA7 no Equity Brazil — AXIA7 cerca de 1.5 por cento mais barato mesmo considerando diferencial de dividendos. |
| 2026-04-14 | XP | rating | bull | 48.80 | [XP Top Dividendos] AXIA7 — peso 5.0%, Compra, PT R$48.8, setor Elétricas |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -14.07%
- **Drawdown 5y**: -14.07%
- **YTD**: +16.25%
- **YoY (1y)**: n/a
- **CAGR 3y**: n/a  |  **5y**: n/a  |  **10y**: n/a
- **Vol annual**: +38.42%
- **Sharpe 3y** (rf=4%): n/a

###### Dividendos
- **DY 5y avg**: n/a
- **Div CAGR 5y**: n/a
- **Frequency**: none
- **Streak** (sem cortes): n/a years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$34.07B | R$10.74B | R$3.64B |
| 2023-12-31 | R$37.16B | R$11.81B | R$4.55B |
| 2024-12-31 | R$40.18B | R$20.73B | R$10.38B |
| 2025-12-31 | R$41.28B | R$3.61B | R$6.56B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "AXIA7 — 1y close"
labels: ['2025-12-22', '2025-12-23', '2025-12-26', '2025-12-29', '2025-12-30', '2026-01-02', '2026-01-05', '2026-01-06', '2026-01-07', '2026-01-08', '2026-01-09', '2026-01-12', '2026-01-13', '2026-01-14', '2026-01-15', '2026-01-16', '2026-01-19', '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23', '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29', '2026-01-30', '2026-02-02', '2026-02-03', '2026-02-04', '2026-02-05', '2026-02-06', '2026-02-09', '2026-02-10', '2026-02-11', '2026-02-12', '2026-02-13', '2026-02-18', '2026-02-19', '2026-02-20', '2026-02-23', '2026-02-24', '2026-02-25', '2026-02-26', '2026-02-27', '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-05', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-16', '2026-03-17', '2026-03-18', '2026-03-19', '2026-03-20', '2026-03-23', '2026-03-24', '2026-03-25', '2026-03-26', '2026-03-27', '2026-03-30', '2026-03-31', '2026-04-01', '2026-04-02', '2026-04-06', '2026-04-07', '2026-04-08', '2026-04-09', '2026-04-10', '2026-04-13', '2026-04-14', '2026-04-15', '2026-04-16', '2026-04-17', '2026-04-20', '2026-04-22', '2026-04-23', '2026-04-24', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06', '2026-05-07']
series:
  - title: AXIA7
    data: [48.2, 48.52, 49.0, 48.78, 49.12, 48.0, 48.3, 49.89, 47.62, 49.43, 49.3, 49.03, 47.84, 49.0, 49.75, 48.65, 49.09, 49.32, 51.1, 52.89, 52.8, 51.62, 52.47, 54.18, 53.05, 52.8, 54.0, 55.0, 53.08, 54.9, 55.64, 56.58, 56.8, 57.59, 56.62, 56.46, 56.32, 59.19, 59.42, 58.65, 59.34, 60.22, 61.01, 59.04, 60.36, 57.58, 59.33, 57.02, 57.2, 57.63, 58.53, 58.73, 56.06, 55.93, 56.91, 55.6, 55.47, 55.84, 53.3, 56.5, 55.56, 56.94, 54.62, 53.97, 54.2, 56.64, 57.44, 57.33, 56.99, 57.35, 60.08, 62.09, 63.07, 63.33, 64.94, 64.06, 62.89, 61.2, 61.2, 60.2, 60.44, 60.11, 59.83, 59.3, 57.63, 59.95, 58.9, 59.11, 59.21, 55.8]
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
    data: [28.87, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    data: [5.53, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46, 5.46]
  - title: DY %
    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AXIA7_DOSSIE.md` (cemetery archive)_

#### 📑 AXIA7 — Axia Energia

> Generated **2026-04-26** by `ii dossier AXIA7`. Cross-links: [[AXIA7]] · [[AXIA7]] · [[CONSTITUTION]]

##### TL;DR

AXIA7 (CVM 2437) negocia a P/B 1.45 com ROE fraco de 5.46%; P/E e DY ainda n/a no snapshot, sinalizando lacuna de earnings recorrentes ou cobertura de dados. Synthetic IC veredicto **HOLD** (medium confidence, 60% consenso) e composite conviction 61. Achado central: tese de turnaround/value sem fundamentos comprovados ainda — ROE precisa duplicar para a tese converter, é binária e não DRIP.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: n/a  |  **BVPS**: 41.48
- **ROE**: 5.46%  |  **P/E**: n/a  |  **P/B**: 1.45
- **DY**: n/a  |  **Streak div**: n/ay  |  **Market cap**: n/a
- **Last price**: BRL 60.11 (2026-04-24)  |  **YoY**: +0.0%

##### 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[AXIA7]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A AXIA7, atuando no setor de Utilities, apresenta um P/B de 1.45 e ROE de 5.46%, indicando potencial valor por estar abaixo do seu patrimônio líquido. Entretanto, não atende aos critérios estritos da filosofia de investimento ajustada a Selic alta.

**Key assumptions**:
1. A empresa manterá sua capacidade operacional e financeira atual
2. Taxas de juros no Brasil permanecem estáveis ou declinam
3. Histórico de dividendos continua ininterrupto por mais 5 anos
4. Dívida líquida/EBITDA reduz para menos de 3x nos próximos trimestres

**Disconfirmation triggers**:
- ROE cai abaixo de 12% por dois quarters consecutivos
- Dividend Yield cair abaixo de 6%
- Dívida líquida/EBITDA aumenta para mais que 5x
- P/B sobe acima de 2.0

**Intent**: Value/turnaround

→ Vault: [[AXIA7]]

##### 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **61** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 30 |

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/B = 1.45** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.45** — verificar consistência com ROE.
- **ROE = 5.46%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **5.46%** abaixo do critério.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **ROE persistentemente baixo** — actual 5.46% bem abaixo do mínimo de 15% (utilities). Trigger: `fundamentals.roe` < 8% por 4 trimestres consecutivos invalida turnaround.
- 🔴 **Cobertura de dados incompleta** — EPS, DY e market cap n/a; não permite Graham nem screen full. Trigger: ausência de `fundamentals.eps` no próximo update da CVM (CVM 2437).
- 🟡 **Risco regulatório ANEEL** — revisão tarifária periódica pode comprimir WACC regulatório. Trigger: anúncio ANEEL de revisão tarifária extraordinária.
- 🟡 **Hidrologia / GSF** — exposição a geração hidrelétrica vulnerável a estiagem. Trigger: ONS reportar GSF < 0.85 por trimestre.
- 🟡 **Leverage opaco** — sem net_debt/EBITDA disponível, não há visibilidade de capacidade de payout. Trigger: divulgação ITR com net_debt/EBITDA > 4x.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: ROE recuperar para ≥ 12% com EPS positivo divulgado em 2 ITRs consecutivos **e** divulgação de DY ≥ 6%. Weight prudente máximo 3% por ser tese contrarian/turnaround binária. Cash exclusivo BRL (BR isolation). Não enquadrar como DRIP — perfil é value/special situation.

##### 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe` ≥ 12% por 2 trimestres consecutivos (sinal de turnaround).
- **EPS reaparece** — `fundamentals.eps IS NOT NULL` e positivo no próximo ITR.
- **DY divulgado** — `fundamentals.dy` ≥ 6% (banco de dados deixa de retornar n/a).
- **P/B re-rating** — `fundamentals.pb` < 1.0 (ponto de máxima margem de segurança).
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 5x (invalida tese).

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
*Generated by `ii dossier AXIA7` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=5 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] AXIA7 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] AXIA7 — peso 8.3% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] AXIA7 — peso 4.9% |
| 2026-04-24 | XP | catalyst | neutral | — | Troca AXIA6 por AXIA7 no Equity Brazil — AXIA7 cerca de 1.5 por cento mais barato mesmo considerando diferencial de dividendos. |
| 2026-04-14 | XP | rating | bull | 48.80 | [XP Top Dividendos] AXIA7 — peso 5.0%, Compra, PT R$48.8, setor Elétricas |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AXIA7_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — AXIA7

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=0 | HOLD=3 | AVOID=2  
**Avg conviction majority**: 4.7/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 1/10, size: none)

**Rationale**:
- ROE baixo
- FCF inconsistente
- Dívida líquida/EBITDA alta

**Key risk**: Possível deterioração da situação financeira e redução do dividendo

###### 🟡 Stan Druckenmiller — **HOLD** (conv 4/10, size: small)

**Rationale**:
- P/B abaixo de 2, indicando potencial valor
- ROE baixo mas estável
- Dívida líquida/EBITDA alta mas em trajetória descendente

**Key risk**: Taxas de juros elevadas e estagnação econômica podem prejudicar a capacidade da empresa de gerir sua dívida

###### 🔴 Nassim Taleb — **AVOID** (conv 10/10, size: none)

**Rationale**:
- EBIT margem inconsistente
- FCF negativo recente
- ROE fraco

**Key risk**: Aumento da dívida líquida/EBITDA para mais de 5x

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/B próximo ao patrimônio líquido, mas não oferece margem significativa de segurança
- ROE baixo e incerteza operacional nos últimos trimestres
- Dívida elevada em relação a EBITDA

**Key risk**: Aumento da dívida líquida/EBITDA para mais que 5x

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/B abaixo de 2, mas ROE fraco.
- Dívida líquida/EBITDA elevada e inconsistência trimestral nas margens.
- Potencial valor se taxas declinarem conforme esperado.

**Key risk**: Aumento da dívida líquida/EBITDA para mais de 5x.

##### 📊 Context provided

```
TICKER: BR:AXIA7

FUNDAMENTALS LATEST:
  pb: 1.449202
  roe: 5.46%
  net_debt_ebitda: 5.110410552910357

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=2.3 ebit=0.9 ni=0.2 em%=36.4 debt=9 fcf=-0.2
  2025-06-30: rev=2.2 ebit=-0.0 ni=-0.3 em%=-0.4 debt=9 fcf=0.4
  2025-03-31: rev=2.2 ebit=-0.2 ni=-0.8 em%=-10.5 debt=9 fcf=0.1
  2024-12-31: rev=2.4 ebit=0.8 ni=-0.1 em%=31.9 debt=9 fcf=1.9
  2024-09-30: rev=5.7 ebit=5.1 ni=3.0 em%=89.5 debt=9 fcf=-1.0
  2024-06-30: rev=0.0 ebit=0.0 ni=0.0 em%=0.0 debt=9 fcf=0.0

VAULT THESIS:
**Core thesis (2026-04-25)**: A AXIA7, atuando no setor de Utilities, apresenta um P/B de 1.45 e ROE de 5.46%, indicando potencial valor por estar abaixo do seu patrimônio líquido. Entretanto, não atende aos critérios estritos da filosofia de investimento ajustada a Selic alta.

**Key assumptions**:
1. A empresa manterá sua capacidade operacional e financeira atual
2. Taxas de juros no Brasil permanecem estáveis ou declinam
3. Histórico de dividendos continua ininterrupto por mais 5 anos
4. Dívida líquida/EBITDA reduz para menos de 3x nos próximos trimestres

**Disconfirmation triggers**:
- ROE cai abaixo de 12% por dois quarters consecutivos
- Dividend Yield cair abaixo de 6%
- Dívida líquida/EBITDA aumenta para mais que 5x
- P/B sobe acima de 2.0

**Intent**: Value/turnaround

---
*Gerad

RECENT MATERIAL NEWS (last 14d via Tavily):
  - 5 Of The Best Folding E-Bikes, According To Consumer Reports - Jalopnik [Mon, 20 Ap]
    Blix, headquartered in Santa Cruz, Calif., has been building e-bikes since 2014 and currently offers a full lineup that includes the folding Vika+ Flex — featuring basics like a 500-watt electric moto
  - Brazil rejects state miner concept as US deal stalls - The Northern Miner [Fri, 24 Ap]
    * April 24, 2026 | Brazil rejects state miner concept as US deal stalls. # Brazil rejects state miner concept as US deal stalls. Brazil's finance minister says global minerals demand is strong enough 
  - Bank creditors for Br
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=5 · themes=0_

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] AXIA7 — peso 9.6%, setor Utilities |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] AXIA7 — peso 8.3% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] AXIA7 — peso 4.9% |
| 2026-04-24 | XP | catalyst | neutral | — | Troca AXIA6 por AXIA7 no Equity Brazil — AXIA7 cerca de 1.5 por cento mais barato mesmo considerando diferencial de dividendos. |
| 2026-04-14 | XP | rating | bull | 48.80 | [XP Top Dividendos] AXIA7 — peso 5.0%, Compra, PT R$48.8, setor Elétricas |

#### — · RI / disclosure
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\AXIA7_RI.md` (cemetery archive)_

#### AXIA7 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+10977.8%**
- ⬆️ **QOQ** `net_income`: **+156.1%**
- ⬇️ **QOQ** `fcf_proxy`: **-144.2%**
- ⬆️ **QOQ** `ebit_margin`: **+36.8pp**
- ⬆️ **QOQ** `net_margin`: **+23.8pp**
- ⬇️ **YOY** `revenue`: **-59.0%**
- ⬇️ **YOY** `ebit`: **-83.3%**
- ⬇️ **YOY** `net_income`: **-93.6%**
- ⬆️ **YOY** `fco`: **+156.4%**
- ⬆️ **YOY** `fcf_proxy`: **+83.5%**
- ⬇️ **YOY** `ebit_margin`: **-53.1pp**
- ⬇️ **YOY** `net_margin`: **-44.4pp**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.3 mi | R$ 2.2 mi | +7.3% |
| `ebit` | R$ 0.9 mi | R$ -0.0 mi | +10977.8% |
| `net_income` | R$ 0.2 mi | R$ -0.3 mi | +156.1% |
| `debt_total` | R$ 8.7 mi | R$ 8.8 mi | -0.3% |
| `fco` | R$ 1.2 mi | R$ 1.2 mi | -0.6% |
| `fcf_proxy` | R$ -0.2 mi | R$ 0.4 mi | -144.2% |
| `gross_margin` | 54.7% | 58.3% | -3.7pp |
| `ebit_margin` | 36.4% | -0.4% | +36.8pp |
| `net_margin` | 8.2% | -15.6% | +23.8pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 2.3 mi | R$ 5.7 mi | -59.0% |
| `ebit` | R$ 0.9 mi | R$ 5.1 mi | -83.3% |
| `net_income` | R$ 0.2 mi | R$ 3.0 mi | -93.6% |
| `debt_total` | R$ 8.7 mi | R$ 8.9 mi | -2.3% |
| `fco` | R$ 1.2 mi | R$ 0.5 mi | +156.4% |
| `fcf_proxy` | R$ -0.2 mi | R$ -1.0 mi | +83.5% |
| `gross_margin` | 54.7% | 51.7% | +2.9pp |
| `ebit_margin` | 36.4% | 89.5% | -53.1pp |
| `net_margin` | 8.2% | 52.6% | -44.4pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 2.3 | 36.4% | 8.2% | 9 | 1 |
| 2025-06-30 | ITR | 2.2 | -0.4% | -15.6% | 9 | 1 |
| 2025-03-31 | ITR | 2.2 | -10.5% | -37.5% | 9 | 1 |
| 2024-12-31 | DFP-ITR | 2.4 | 31.9% | -3.1% | 9 | 3 |
| 2024-09-30 | ITR | 5.7 | 89.5% | 52.6% | 9 | 0 |
| 2024-06-30 | ITR | 0.0 | 0.0% | 0.0% | 9 | 0 |
| 2024-03-31 | ITR | 0.0 | 0.0% | 0.0% | 3 | 0 |
| 2023-12-31 | DFP-ITR | -6.1 | 60.4% | 34.7% | 0 | -2 |
| 2023-09-30 | ITR | 1.9 | 83.7% | 63.4% | 3 | 1 |
| 2023-06-30 | ITR | 2.1 | 56.6% | 29.1% | 3 | 1 |
| 2023-03-31 | ITR | 2.2 | 43.8% | 15.3% | 1 | 0 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [2.2, 2.1, 1.9, -6.1, 0.0, 0.0, 5.7, 2.4, 2.2, 2.2, 2.3]
  - title: EBIT margin %
    data: [43.8, 56.6, 83.7, 60.4, 0, 0, 89.5, 31.9, -10.5, -0.4, 36.4]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama AXIA7 --write
ii deepdive AXIA7 --save-obsidian
ii verdict AXIA7 --narrate --write
ii fv AXIA7
python -m analytics.fair_value_forward --ticker AXIA7
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
