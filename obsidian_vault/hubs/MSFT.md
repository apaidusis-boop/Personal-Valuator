---
type: ticker_hub
ticker: MSFT
market: us
sector: Technology
currency: USD
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 5
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# MSFT — Microsoft

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Technology` · `market: US` · `currency: USD` · `bucket: watchlist` · `5 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `SKIP` (score 5.39, 2026-05-09)
- **Fundamentals** (2026-05-13): P/E 24.12 · P/B 7.26 · DY 0.9% · ROE 34.0% · ND/EBITDA 0.26 · Dividend streak 24 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\MSFT.md` (cemetery archive)_

#### MSFT — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://www.microsoft.com/en-us/investor
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **98**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=412.6600036621094
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.34013999 · DY=0.008433092543782031 · P/E=24.607037
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-29 | 10-Q | sec | 10-Q |
| 2026-01-28 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-01-28 | 10-Q | sec | 10-Q |
| 2025-12-08 | 8-K | sec | 8-K \| 5.02,5.07 |

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


### 2019

#### 2019-12-05 · Filing 2019-12-05
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\MSFT_FILING_2019-12-05.md` (cemetery archive)_

#### Filing dossier — [[MSFT]] · 2019-12-05

**Trigger**: `sec:8-K` no dia `2019-12-05`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/789019/000119312519307138/d840134d8k.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 415.12

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `130.52` |
| HOLD entre | `130.52` — `167.33` (consensus) |
| TRIM entre | `167.33` — `192.43` |
| **SELL acima de** | `192.43` |

_Método: `buffett_ceiling`. Consensus fair = R$167.33. Our fair (mais conservador) = R$130.52._

##### 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:56+00:00 | `buffett_ceiling` | 167.33 | 130.52 | 415.12 | SELL | single_source | `filing:sec:8-K:2019-12-05` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MSFT.md` (cemetery archive)_

#### MSFT — Microsoft

#watchlist #us #technology

##### Links

- Sector: [[sectors/Technology|Technology]]
- Market: [[markets/US|US]]
- Peers: [[AAPL]] · [[ACN]] · [[PLTR]] · [[TSM]] · [[IBM]]
- Vídeos: [[videos/2026-04-10_btg-pactual_turbulencia-global-petroleo-e-oportunidades-em-tecnologia-radar-do-inv|Turbulência global, petróleo e oportunid]]

##### Snapshot

- **Preço**: $413.96  (2026-05-06)    _+0.63% 1d_
- **Screen**: 0.4  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 95.0/100 (SAFE)

##### Fundamentals

- P/E: 24.669844 | P/B: 7.8677177 | DY: 0.84%
- ROE: 34.01% | EPS: 16.78 | BVPS: 52.615
- Streak div: 24y | Aristocrat: False

##### Dividendos recentes

- 2026-02-19: $0.9100
- 2025-11-20: $0.9100
- 2025-08-21: $0.8300
- 2025-05-15: $0.8300
- 2025-02-20: $0.8300

##### Eventos (SEC/CVM)

- **2026-04-29** `8-K` — 8-K | 2.02,9.01
- **2026-04-29** `10-Q` — 10-Q
- **2026-01-28** `8-K` — 8-K | 2.02,9.01
- **2026-01-28** `10-Q` — 10-Q
- **2025-12-08** `8-K` — 8-K | 5.02,5.07

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O analista menciona a presença da Microsoft na corrida de inteligência artificial, embora ela tenha ficado para trás em comparação com outr… |
| 2026-05-10 | WSJ — What's News | operational | 1.00 | Microsoft assinou um contrato de 20 anos com a Constellation para comprar energia gerada no site do Three Mile Island. |
| 2026-05-10 | WSJ — What's News | catalyst | 0.90 | Microsoft está investindo em energia nuclear para atender às necessidades de energia crescentes dos seus data centers. |
| 2026-04-10 | BTG Pactual | valuation | 0.80 | A Microsoft é considerada uma empresa de alta qualidade com grande capacidade geradora de caixa, o que a torna menos arriscada em comparaçã… |
| 2026-04-10 | BTG Pactual | risk | 0.70 | Embora a Microsoft seja vista como menos arriscada em comparação com empresas menores no setor de inteligência artificial, ainda há risco a… |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | A nova era de inovação americana está impulsionando o interesse em energia nuclear, especialmente para atende… |
| 2026-05-10 | WSJ — What's News | semis_cycle | neutral | Apesar do interesse renovado em energia nuclear, há desafios significativos e custos elevados envolvidos na r… |
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | Empresas de tecnologia como Google, Meta e Microsoft estão investindo em usinas nucleares para atender às sua… |

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -23.63%
- **Drawdown 5y**: -23.63%
- **YTD**: -12.47%
- **YoY (1y)**: -4.47%
- **CAGR 3y**: +10.04%  |  **5y**: +10.40%  |  **10y**: +23.44%
- **Vol annual**: +26.93%
- **Sharpe 3y** (rf=4%): +0.25

###### Dividendos
- **DY 5y avg**: +0.78%
- **Div CAGR 5y**: +10.27%
- **Frequency**: quarterly
- **Streak** (sem cortes): 20 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "MSFT — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-29', '2026-05-05']
series:
  - title: MSFT
    data: [438.17, 452.94, 458.17, 460.69, 461.97, 470.38, 478.87, 480.24, 492.27, 492.05, 496.62, 503.02, 510.05, 510.88, 513.24, 527.75, 521.77, 520.17, 504.24, 506.74, 505.35, 498.41, 515.36, 517.93, 507.03, 519.71, 523.98, 514.05, 513.58, 520.56, 541.55, 514.33, 506.0, 510.18, 478.43, 485.5, 477.73, 492.02, 474.82, 485.92, 487.71, 472.94, 478.11, 459.38, 444.11, 480.58, 423.37, 401.14, 401.84, 398.46, 400.6, 403.93, 409.41, 395.55, 389.02, 371.04, 370.17, 372.29, 384.37, 422.79, 415.75, 424.46, 411.38]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: P/E
    data: [26.128437, 26.315592, 26.457449, 26.199312, 26.5598, 26.605263, 26.588602, 26.58735, 26.601128, 26.878521, 26.578585, 25.550125, 24.649582, 24.501488, 24.669844]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: ROE %
    data: [34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.39, 34.01, 34.01, 34.01]
  - title: DY %
    data: [89.0, 87.0, 86.0, 86.0, 0.82, 0.82, 0.82, 0.82, 0.82, 0.81, 0.82, 0.85, 0.84, 0.85, 0.84]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MSFT_DOSSIE.md` (cemetery archive)_

#### 📑 MSFT — Microsoft

> Generated **2026-04-26** by `ii dossier MSFT`. Cross-links: [[MSFT]] · [[MSFT_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

Microsoft transaciona a P/E 26.59 com DY apenas 0.82% e streak de 24y — falha screen US tanto em P/E (≤20) como em DY (≥2.5%). IC Synthetic verdica HOLD com high confidence (80% consenso, o mais robusto do grupo watchlist). Achado-chave: thesis é compounder/growth, não DRIP — entry justifica-se por moat (Azure + M365 + GitHub Copilot) e ROE 34.39% sustentado, não por yield; AI capex cycle é o swing variable.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 15.97  |  **BVPS**: 52.62
- **ROE**: 34.39%  |  **P/E**: 26.59  |  **P/B**: 8.07
- **DY**: 0.82%  |  **Streak div**: 24y  |  **Market cap**: USD 3155.94B
- **Last price**: USD 424.62 (2026-04-24)  |  **YoY**: +9.6%

##### 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MSFT_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-26)**: Microsoft é líder em tecnologia com forte ROE de 34.39%, embora apresente um P/E de 26.61 e um P/B de 8.07, que excedem os critérios da filosofia value-investor. A empresa mantém uma sólida tradição de dividendos por 24 anos consecutivos.

**Key assumptions**:
1. Microsoft continuará a expandir suas margens e lucratividade
2. A demanda por soluções em nuvem e inteligência artificial permanecerá robusta
3. A empresa manterá sua política de dividendos estável e crescente
4. O mercado reconhecerá o valor intrínseco da Microsoft, reavaliando suas métricas financeiras

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- P/E ultrapassa 30 por três trimestres seguidos
- A empresa reduz ou congela o dividendo após 24 anos de pagame

→ Vault: [[MSFT]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 26.59** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 26.59** esticado vs critério.
- **P/B = 8.07** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **8.07** esticado.
- **DY = 0.82%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.82%** fraco; verificar se é growth pick.
- **ROE = 34.39%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **34.39%** compounder-grade.
- **Graham Number ≈ R$ 137.51** vs preço **R$ 424.62** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 24y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🔴 **Azure growth deceleration** — segmento sustenta múltiplo; queda abaixo de 25% YoY constant currency é red flag. Trigger: revenue growth Azure YoY < 25% por 2Q em earnings transcripts (yt_digest).
- 🔴 **AI capex returns inadequados** — $80B+/ano capex requer ROIC>WACC; risco de overinvestment. Trigger: capex/revenue > 30% AND operating margin contracts > 200bps.
- 🟡 **OpenAI relationship complexity** — equity stake + IP rights + competitive overlap; qualquer ruptura é evento material. Trigger: events com kind='strategic' AND summary LIKE '%OpenAI%'.
- 🟡 **Antitrust EU/UK/FTC** — Activision deal sob scrutiny; bundling Teams já levou a unbundling forçado. Trigger: events com kind='regulatory' AND ticker='MSFT'.
- 🟢 **Múltiplo elevado vs screen** — DY 0.82% confirma entry não é DRIP. Trigger: P/E > 30 sustained reabre disconfirmation thesis.

##### 5. Position sizing

**Status atual**: watchlist

Watchlist — não é trade signal. Considerar entry inicial 3-5% da sleeve US apenas se P/E recuar para ≤22 com Azure growth ainda > 25% YoY (compounder thesis intact). DY 0.82% deixa MSFT fora do core DRIP — entry seria por compounder/quality, não por yield. Cash USD permanece em US (BR/US isolation); não converter BRL.

##### 6. Tracking triggers (auto-monitoring)

- `fundamentals.pe < 22` — entry condition compounder (DY screen ignorado dado thesis).
- `fundamentals.roe < 25%` por 2Q — quality compression alerta thesis.
- `events WHERE kind='earnings' AND summary LIKE '%Azure%' AND growth_pct < 25` por 2Q — disconfirmation core.
- `events WHERE kind='regulatory' AND ticker='MSFT'` — antitrust EU/FTC tracking.
- `scores.score > 75` AND macro 10y < 4% — promover de watchlist a entry.

##### 7. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier MSFT` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O analista menciona a presença da Microsoft na corrida de inteligência artificial, embora ela tenha ficado para trás em comparação com outr… |
| 2026-05-10 | WSJ — What's News | operational | 1.00 | Microsoft assinou um contrato de 20 anos com a Constellation para comprar energia gerada no site do Three Mile Island. |
| 2026-05-10 | WSJ — What's News | catalyst | 0.90 | Microsoft está investindo em energia nuclear para atender às necessidades de energia crescentes dos seus data centers. |
| 2026-04-10 | BTG Pactual | valuation | 0.80 | A Microsoft é considerada uma empresa de alta qualidade com grande capacidade geradora de caixa, o que a torna menos arriscada em comparaçã… |
| 2026-04-10 | BTG Pactual | risk | 0.70 | Embora a Microsoft seja vista como menos arriscada em comparação com empresas menores no setor de inteligência artificial, ainda há risco a… |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | A nova era de inovação americana está impulsionando o interesse em energia nuclear, especialmente para atende… |
| 2026-05-10 | WSJ — What's News | semis_cycle | neutral | Apesar do interesse renovado em energia nuclear, há desafios significativos e custos elevados envolvidos na r… |
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | Empresas de tecnologia como Google, Meta e Microsoft estão investindo em usinas nucleares para atender às sua… |

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\MSFT_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — MSFT

**Committee verdict**: **HOLD** (high confidence, 80% consensus)  
**Votes**: BUY=1 | HOLD=4 | AVOID=0  
**Avg conviction majority**: 6.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟡 Warren Buffett — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- ROE de 34.39% indica alta lucratividade
- Tradição de dividendos por 24 anos
- Demanda robusta por nuvem e IA

**Key risk**: P/E de 26.61 é alto, potencial sobreavaliação do mercado

###### 🟢 Stan Druckenmiller — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Fortes margens e ROE
- Demanda robusta por soluções em nuvem
- Política de dividendos estável

**Key risk**: P/E ultrapassa 30 por três trimestres seguidos

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE forte, mas P/E e P/B elevados
- Dividendos consistentes, mas alto dividendo não protege contra riscos sistêmicos
- Liderança em nuvem e IA

**Key risk**: Overvaluation pode levar a uma queda brusca se o mercado mudar de opinião

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- ROE forte
- tradição de dividendos
- demanda robusta

**Key risk**: P/E e P/B elevados podem indicar sobreavaliação do mercado

###### 🟡 Ray Dalio — **HOLD** (conv 7/10, size: medium)

**Rationale**:
- ROE forte
- expansão em nuvem e AI
- tradição de dividendos

**Key risk**: P/E e P/B elevados podem indicar sobreavaliação do mercado

##### 📊 Context provided

```
TICKER: US:MSFT

FUNDAMENTALS LATEST:
  pe: 26.588602
  pb: 8.070322
  dy: 0.82%
  roe: 34.39%
  net_debt_ebitda: 0.19294874431614215

VAULT THESIS:
**Core thesis (2026-04-26)**: Microsoft é líder em tecnologia com forte ROE de 34.39%, embora apresente um P/E de 26.61 e um P/B de 8.07, que excedem os critérios da filosofia value-investor. A empresa mantém uma sólida tradição de dividendos por 24 anos consecutivos.

**Key assumptions**:
1. Microsoft continuará a expandir suas margens e lucratividade
2. A demanda por soluções em nuvem e inteligência artificial permanecerá robusta
3. A empresa manterá sua política de dividendos estável e crescente
4. O mercado reconhecerá o valor intrínseco da Microsoft, reavaliando suas métricas financeiras

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- P/E ultrapassa 30 por três trimestres seguidos
- A empresa reduz ou congela o dividendo após 24 anos de pagame
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=5 · analyst=0 · themes=3_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-11 | Genial Investimentos | operational | 0.80 | O analista menciona a presença da Microsoft na corrida de inteligência artificial, embora ela tenha ficado para trás em comparação com outr… |
| 2026-05-10 | WSJ — What's News | operational | 1.00 | Microsoft assinou um contrato de 20 anos com a Constellation para comprar energia gerada no site do Three Mile Island. |
| 2026-05-10 | WSJ — What's News | catalyst | 0.90 | Microsoft está investindo em energia nuclear para atender às necessidades de energia crescentes dos seus data centers. |
| 2026-04-10 | BTG Pactual | valuation | 0.80 | A Microsoft é considerada uma empresa de alta qualidade com grande capacidade geradora de caixa, o que a torna menos arriscada em comparaçã… |
| 2026-04-10 | BTG Pactual | risk | 0.70 | Embora a Microsoft seja vista como menos arriscada em comparação com empresas menores no setor de inteligência artificial, ainda há risco a… |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | A nova era de inovação americana está impulsionando o interesse em energia nuclear, especialmente para atende… |
| 2026-05-10 | WSJ — What's News | semis_cycle | neutral | Apesar do interesse renovado em energia nuclear, há desafios significativos e custos elevados envolvidos na r… |
| 2026-05-10 | WSJ — What's News | semis_cycle | bullish | Empresas de tecnologia como Google, Meta e Microsoft estão investindo em usinas nucleares para atender às sua… |

## ⚙️ Refresh commands

```bash
ii panorama MSFT --write
ii deepdive MSFT --save-obsidian
ii verdict MSFT --narrate --write
ii fv MSFT
python -m analytics.fair_value_forward --ticker MSFT
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
