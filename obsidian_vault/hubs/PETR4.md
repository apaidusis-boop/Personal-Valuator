---
type: ticker_hub
ticker: PETR4
market: br
sector: Oil & Gas
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 10
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# PETR4 — Petrobras

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Oil & Gas` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `10 sources merged`

## 🎯 Hoje

- **Verdict (DB)**: `BUY` (score 7.55, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 5.90 · P/B 1.38 · DY 7.1% · ROE 25.6% · ND/EBITDA 1.59 · Dividend streak 9

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas. Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13\PETR4.md` (now in cemetery)_

#### PETR4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Oil & Gas
- **RI URLs scraped** (1):
  - https://www.investidorpetrobras.com.br/
- **Pilot rationale**: known (watchlist)

##### Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **49**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=46.43000030517578
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.28176 · DY=0.06804753347476936 · P/E=6.174202
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Petrobras antecipa início |
| 2026-04-30 | fato_relevante | cvm | Relatório de Produção e Vendas 1T26 |
| 2026-04-28 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Investor Tour 2026 |
| 2026-04-27 | fato_relevante | cvm | Petrobras amplia presença na Bacia de Campos com a aquisição de parte do ring-fe |
| 2026-04-23 | fato_relevante | cvm | Petrobras assina novo Acordo de Acionistas da Braskem |

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

#### 2026-05-04 · Filing 2026-05-04
_source: `dossiers\PETR4_FILING_2026-05-04.md` (now in cemetery)_

#### Filing dossier — [[PETR4]] · 2026-05-04

**Trigger**: `cvm:comunicado` no dia `2026-05-04`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515529&numSequencia=1040235&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 45.17

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `42.96` |
| HOLD entre | `42.96` — `74.08` (consensus) |
| TRIM entre | `74.08` — `85.19` |
| **SELL acima de** | `85.19` |

_Método: `graham_number`. Consensus fair = R$74.08. Our fair (mais conservador) = R$42.96._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.25601` | `0.196` | +23.5% |
| EPS | `7.56` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 127.9B (+7.4% QoQ, -1.3% YoY)
- EBIT 43.6B (+43.2% QoQ)
- Margem EBIT 34.1% vs 25.6% prior
- Lucro líquido 32.8B (+22.7% QoQ, +0.5% YoY)

**BS / cash**
- Equity 425.0B (+5.8% QoQ)
- Dívida total 376.1B (+1.2% QoQ)
- FCF proxy 27.7B (-0.5% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 74.08 | 42.96 | 45.17 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-04` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `extend_2026-05-09` |
| 2026-05-08T19:20:28+00:00 | `graham_number` | 73.73 | 42.77 | 46.22 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-30 · Filing 2026-04-30
_source: `dossiers\PETR4_FILING_2026-04-30.md` (now in cemetery)_

#### Filing dossier — [[PETR4]] · 2026-04-30

**Trigger**: `cvm:fato_relevante` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513705&numSequencia=1038411&numVersao=1>

##### 🎯 Acção sugerida

###### 🟡 **HOLD** &mdash; preço 46.22

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `42.77` |
| HOLD entre | `42.77` — `73.73` (consensus) |
| TRIM entre | `73.73` — `84.79` |
| **SELL acima de** | `84.79` |

_Método: `graham_number`. Consensus fair = R$73.73. Our fair (mais conservador) = R$42.77._

##### 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.28176` | `0.196` | +30.4% |
| EPS | `7.49` | `None` | +0.0% |


##### 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 127.9B (+7.4% QoQ, -1.3% YoY)
- EBIT 43.6B (+43.2% QoQ)
- Margem EBIT 34.1% vs 25.6% prior
- Lucro líquido 32.8B (+22.7% QoQ, +0.5% YoY)

**BS / cash**
- Equity 425.0B (+5.8% QoQ)
- Dívida total 376.1B (+1.2% QoQ)
- FCF proxy 27.7B (-0.5% QoQ)

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 73.73 | 42.77 | 46.22 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._

#### 2026-04-22 · Other
_source: `videos\2026-04-22_virtual-asset_dividendo-r-1-bi-em-risco-na-sapr11-itsa4-mudou-o-plano-petr4-lucra-co.md` (now in cemetery)_

#### 🎬 DIVIDENDO: R$ 1 BI EM RISCO NA SAPR11! ITSA4 MUDOU O PLANO? PETR4 LUCRA COM CONFLITOS? +CSMG3 BTLG11

**Canal**: Virtual Asset | **Publicado**: 2026-04-22 | **Duração**: 22min

**URL**: [https://www.youtube.com/watch?v=eM1acX1fYb4](https://www.youtube.com/watch?v=eM1acX1fYb4)

##### Tickers mencionados

[[B3SA3]] · [[IRBR3]] · [[ITSA4]] · [[PETR4]] · [[SAPR11]]

##### Insights extraídos

###### [[B3SA3]]
- [0.80 valuation] A B3 está valorizada, com um preço de 61% acima do patrimonial nos últimos 12 meses.
- [0.70 operational] A B3 continua envolvida nos processos preparatórios para a privatização da Copasa, mas não pode concluir a alienação do controle.
- [0.60 risk] A B3 enfrenta riscos geopolíticos que podem afetar o preço do petróleo e a previsibilidade do setor.

###### [[ITSA4]]
- [0.80 thesis_bear] A crise contábil na AGEA postergou o IPO e aumenta a desconfiança do mercado sobre a capacidade da AGEA de sustentar uma trajetória limpa rumo ao mercado de capitais.
- [0.80 valuation] A Itaúsa é considerada um excelente ativo, com uma rentabilidade de 664,76% em 10 anos e um Dividend Yield atual de 8,44%, mesmo após a valorização recente.
- [0.70 risk] A Itaúsa sofreu um impacto de 700 milhões de reais com a revisão contábil da AGEA, mas considerou o efeito imaterial diante do seu patrimônio líquido.

###### [[PETR4]]
- [0.80 risk] A Petrobras alerta que a adaptação à nova legislação tributária pode causar efeitos adversos nos resultados.
- [0.80 risk] A Petrobras reconhece que as tensões geopolíticas podem impactar negativamente seus resultados.
- [0.70 guidance] A Petrobras confirmou a distribuição de R$8 bilhões em dividendos e reforçou a distribuição total de R$41,2 bilhões em 2025.

###### [[SAPR11]]
- [0.80 dividend] A Sanepar entrou na justiça para tentar barrar a decisão da Agepar, que determinou que 4 bilhões de reais em precatórios sejam destinados diretamente aos consumidores, o que poderia afetar os dividendos dos acionistas.
- [0.75 risk] A Sanepar enfrenta riscos regulatórios que podem afetar a previsibilidade da distribuição de dividendos, o que pode impactar negativamente o valor das ações.
- [0.70 valuation] A Sanepar está extremamente descontada no mercado, com um PL abaixo de seis vezes, o que é considerado um bom prêmio para investidores.

###### [[IRBR3]]
- [0.70 operational] É possível receber um dividendo sintético de até 1,19 centavos por ação com as ações da IRB Brasil (IRBR3) sem precisar comprar novas ações.

##### Temas macro

- **oil_cycle** neutral _(conf 0.85)_ — A Petrobras admite que tensões geopolíticas podem impactar seus resultados, mas o preço do petróleo em alta é positivo. A empresa continua a distribuir dividendos e enfrenta desafios com a adaptação à reforma tributária.
- **real_estate_cycle** bullish _(conf 0.85)_ — O fundo imobiliário BTLG11 está quitando galpões logísticos em São Paulo, aumentando sua exposição a áreas estratégicas da logística brasileira.

#### 2026-04-20 · Other
_source: `videos\2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa.md` (now in cemetery)_

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


### 2025

#### 2025-07-18 · Other
_source: `videos\2025-07-18_suno-noticias_petrobras-petr4-ja-tem-plano-b-asia-sera-a-nova-rota-se-trump-aplicar.md` (now in cemetery)_

#### 🎬 PETROBRAS (PETR4) JÁ TEM PLANO B: Ásia será a nova rota se Trump aplicar tarifas?

**Canal**: Suno Notícias | **Publicado**: 2025-07-18 | **Duração**: 5min

**URL**: [https://www.youtube.com/watch?v=MB0Wuzw6mhs](https://www.youtube.com/watch?v=MB0Wuzw6mhs)

##### Tickers mencionados

[[PETR4]]

##### Insights extraídos

###### [[PETR4]]
- [0.90 operational] As exportações de petróleo bruto da Petrobras para os EUA representam cerca de 4% do total das exportações da empresa.
- [0.80 risk] A Petrobras tem um plano B caso as tarifas de exportação dos EUA entrem em vigor, redirecionando parte do petróleo para a Ásia.
- [0.70 thesis_bear] Embora as tarifas possam afetar a Petrobras, os analistas acreditam que o impacto de médio e longo prazo será limitado.

##### Temas macro

- **oil_cycle** neutral _(conf 0.80)_ — As exportações de derivados de petróleo para os EUA são mais significativas, mas ainda assim representam uma parcela relativamente pequena das vendas da Petrobras.
- **oil_cycle** neutral _(conf 0.75)_ — Ainda há incerteza sobre a aplicação das tarifas, o que pode levar a uma renegociação ou isenção para combustíveis minerais brasileiros.


### (undated)

#### — · Panorama
_source: `tickers\PETR4.md` (now in cemetery)_

#### PETR4 — PETR4

#watchlist #br #oil_&_gas

##### Links

- Sector: [[sectors/Oil_&_Gas|Oil & Gas]]
- Market: [[markets/BR|BR]]
- Peers: [[PRIO3]]
- Vídeos: [[videos/2026-04-22_virtual-asset_dividendo-r-1-bi-em-risco-na-sapr11-itsa4-mudou-o-plano-petr4-lucra-co|DIVIDENDO: R$ 1 BI EM RISCO NA SAPR11! I]] · [[videos/2026-04-21_market-makers_risco-guerra-dolar-em-queda-e-petroleo-em-alta-onde-investir-agora-mar|RISCO GUERRA, DÓLAR EM QUEDA E PETRÓLEO ]] · [[videos/2026-04-21_o-primo-rico_se-voce-nao-entende-renda-fixa-voce-nao-entende-dinheiro|SE VOCÊ NÃO ENTENDE RENDA FIXA, VOCÊ NÃO]] · [[videos/2026-04-20_virtual-asset_petr4-e-cple3-dividendo-extra-e-novo-chegando-vale3-supera-expectativa|PETR4 e CPLE3: DIVIDENDO EXTRA E NOVO CH]] · [[videos/2026-04-18_stock-pickers_raizen-raiz4-mindset-mudou-para-investir-em-grandes-empresas-no-brasil|RAÍZEN (RAIZ4): MINDSET MUDOU PARA INVES]]

##### Snapshot

- **Preço**: R$46.22  (2026-05-07)    _-2.22% 1d_
- **Screen**: 1.0  ✓ PASS
- **Altman Z**: 4.02 (safe)
- **Piotroski**: 6/9
- **Div Safety**: 78.0/100 (WATCH)

##### Fundamentals

- P/E: 6.170895 | P/B: 1.4327341 | DY: 6.84%
- ROE: 28.18% | EPS: 7.49 | BVPS: 32.26
- Streak div: 9y | Aristocrat: None

##### Dividendos recentes

- 2026-04-23: R$0.6262
- 2025-12-23: R$0.9521
- 2025-08-22: R$0.6719
- 2025-06-03: R$0.9092
- 2025-04-17: R$0.7481

##### Eventos (SEC/CVM)

- **2026-05-01** `comunicado` — Outros Comunicados Não Considerados Fatos Relevantes | Petrobras antecipa início
- **2026-04-30** `fato_relevante` — Relatório de Produção e Vendas 1T26
- **2026-04-28** `comunicado` — Apresentações a analistas/agentes do mercado | Investor Tour 2026
- **2026-04-27** `fato_relevante` — Petrobras amplia presença na Bacia de Campos com a aquisição de parte do ring-fe
- **2026-04-23** `fato_relevante` — Petrobras assina novo Acordo de Acionistas da Braskem

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=6 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Genial Investimentos | valuation | 1.00 | O preço-alvo da Petrobras é de R$50, gerando potencial de valorização. |
| 2026-05-13 | Genial Investimentos | risk | 0.90 | A política de preços é o que mais gera volatilidade para a Petrobras. |
| 2026-05-13 | Virtual Asset | capex | 0.80 | A Petrobras está investindo cerca de 12 bilhões de reais na conclusão do trem 2 e manutenção do trem 1 da refinaria Abreu e Lima. |
| 2026-05-13 | Genial Investimentos | catalyst | 0.80 | A Petrobras pode ampliar sua forma de remuneração do acionista na forma de dividendos. |
| 2026-05-13 | Genial Investimentos | thesis_bull | 0.80 | A Petrobras precisa buscar fontes fora do pré-sal para manter a capacidade de entrega de resultados no longo prazo. |
| 2026-05-13 | Virtual Asset | valuation | 0.70 | As ações da Petrobras estão corrigindo na Bolsa de Valores, mas o PL (Preço/Lucro) é considerado baixo e pode subir em breve com novos divi… |
| 2026-05-13 | Genial Investimentos | catalyst | 0.70 | Aumento da gasolina pode ser um catalisador positivo para a Petrobras, embora possa haver medidas provisórias sobre subvenção à gasolina. |
| 2026-05-12 | Suno | capex | 0.90 | A Petrobras aumentou seu investimento em capital (CAPEX) no último trimestre, o que impactou negativamente a geração de caixa livre. |
| 2026-05-12 | Suno | operational | 0.90 | A receita líquida da Petrobras ficou estática em R$123 bilhões, apesar do aumento significativo no preço do petróleo. |
| 2026-05-12 | Suno | guidance | 0.80 | A Petrobras espera resultados mais fortes no segundo trimestre de 2026, devido ao atraso na negociação dos preços das exportações. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 38.00 | [Suno Valor] PETR4 — peso 7.5%, rating Aguardar, PT R$38.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PETR4 — peso 9.6%, setor Energy |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] PETR4 — peso 13.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PETR4 — peso 4.1% |
| 2026-04-24 | XP | catalyst | neutral | — | A Petrobras reajustou em 55% o preço do querosene de aviação, gerando apreensão no setor aéreo. |
| 2026-04-14 | XP | rating | bull | 47.00 | [XP Top Dividendos] PETR4 — peso 10.0%, Compra, PT R$47.0, setor Energia |

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
- **Drawdown 52w**: -7.15%
- **Drawdown 5y**: -7.15%
- **YTD**: +50.50%
- **YoY (1y)**: +52.59%
- **CAGR 3y**: +23.55%  |  **5y**: +13.65%  |  **10y**: +17.17%
- **Vol annual**: +26.48%
- **Sharpe 3y** (rf=4%): +0.68

###### Dividendos
- **DY 5y avg**: +26.81%
- **Div CAGR 5y**: +8.10%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-12-31 | n/a | n/a | n/a |
| 2022-12-31 | R$124.47B | R$36.62B | R$40.14B |
| 2023-12-31 | R$102.41B | R$24.88B | R$31.10B |
| 2024-12-31 | R$91.42B | R$7.53B | R$23.34B |
| 2025-12-31 | R$89.19B | R$19.63B | R$16.53B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "PETR4 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: PETR4
    data: [30.71, 31.91, 32.11, 31.3, 30.9, 29.36, 31.05, 32.94, 31.37, 31.38, 32.12, 32.24, 31.79, 31.35, 32.02, 32.21, 32.53, 30.57, 30.04, 30.65, 31.1, 31.06, 31.51, 31.53, 31.37, 32.25, 31.08, 30.65, 30.02, 29.75, 29.84, 29.89, 30.85, 33.2, 32.88, 32.54, 31.79, 32.52, 31.94, 30.74, 31.1, 30.82, 29.83, 31.14, 32.17, 35.04, 37.7, 37.52, 37.35, 37.19, 39.57, 41.13, 42.16, 45.0, 47.0, 47.27, 49.67, 48.94, 49.03, 48.58, 47.77, 48.96, 47.27]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "PETR4 — dividend history"
labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [0.9166, 0.9424, 0.0005, 5.6532, 15.1664, 7.3443, 7.9311, 3.2813, 0.6262]
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
    data: [5.6, 6.1787124, 6.269029, 6.221636, 6.1647058, 6.1647058, 6.192157, 6.277411, 6.4421053, 6.4664035, 6.4921055, 6.453581, 6.236148, 6.170895]
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
    data: [26.37, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18, 28.18]
  - title: DY %
    data: [6.87, 5.39, 6.67, 6.76, 6.76, 6.76, 6.73, 6.7, 6.51, 6.49, 6.4, 6.49, 6.68, 6.84]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `tickers\PETR4_DOSSIE.md` (now in cemetery)_

#### 📑 PETR4 — Petrobras

> Generated **2026-04-26** by `ii dossier PETR4`. Cross-links: [[PETR4]] · [[PETR4_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

PETR4 negocia a P/E 6.16 e DY 6.76% com ROE excepcional de 28.18% e dívida líq./EBITDA confortável em 1.60x. Synthetic IC veredicto **BUY** com consenso unânime (100%) e composite conviction 73. Achado central: combinação rara de earnings yield ~16% + payout sustentável, mas o risco de governança política (dividendos extraordinários, intervenção em preços) continua a ser o factor que pode colapsar a tese overnight.

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 7.65  |  **BVPS**: 32.26
- **ROE**: 28.18%  |  **P/E**: 6.16  |  **P/B**: 1.46
- **DY**: 6.76%  |  **Streak div**: 9y  |  **Market cap**: R$ 644.37B
- **Last price**: BRL 47.16 (2026-04-24)  |  **YoY**: +55.0%

##### 2. Synthetic IC

**🏛️ BUY** (high confidence, 100.0% consensus)

→ Detalhe: [[PETR4_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-25)**: A PETR4, com um P/E de 6.22 e um DY de 6.76%, oferece um valor atrativo para investidores em busca de retornos estáveis. A empresa atende aos critérios da filosofia value-investing ajustada à Selic alta, destacando-se pelo ROE de 28.18% e uma dívida líquida/EBITDA de 1.60.

**Key assumptions**:
1. A PETR4 manterá seu histórico de dividendos ininterrupto por mais dois anos
2. O preço da ação não subirá acima do Graham Number ajustado para o ambiente atual (22.5)
3. A empresa continuará gerando um ROE superior a 15%
4. As condições macroeconômicas globais não afetarão negativamente os lucros operacionais da PETR4

**Disconfirmation triggers**:
- ROE cair abaixo de 12% por dois trimestres consecutivos
- Dividendos serem cortados ou pausados
- A dívida líquida/EBI

→ Vault: [[PETR4]]

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

- **P/E = 6.16** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 6.16** passa.
- **P/B = 1.46** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.46** — verificar consistência com ROE.
- **DY = 6.76%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **6.76%** passa.
- **ROE = 28.18%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **28.18%** compounder-grade.
- **Graham Number ≈ R$ 74.52** vs preço **R$ 47.16** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 9y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 5. Riscos identificados

- 🔴 **Governança política** — interferência em pricing combustíveis ou redirecionamento de capex social compromete margens e payout. Trigger: anúncio de mudança em política de paridade de preços ou troca de CEO por indicação política.
- 🔴 **Brent estrutural baixo** — break-even de pre-sal e geração de FCF dependem de Brent ≥ $60. Trigger: Brent < $60/bbl por 2 trimestres consecutivos (`prices` proxy via correlated ETF ou macro).
- 🟡 **Dividendos extraordinários reset** — política actual de DY 6.76% pode ser cortada a qualquer assembleia. Trigger: payout TTM > 100% ou anúncio de revisão de política de dividendos (`fundamentals.dy` queda >2pp QoQ).
- 🟡 **Dívida líq./EBITDA degradação** — actual 1.60x; alavancagem para acquisitions ou capex E&P pode pressionar grau de investimento. Trigger: `fundamentals.net_debt_ebitda` > 2.5x.
- 🟢 **Royalties / nova MP** — mudança fiscal sobre exploração offshore. Trigger: aprovação de MP ou PL aumentando alíquota de royalties.

##### 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: pullback técnico para P/E < 5.5 (proxy: ~R$ 40) **com** confirmação de manutenção da política actual de dividendos pós-AGE. Weight prudente 3-5% do book BR (cap em estatal cíclica), uso exclusivo de cash BRL (BR isolation). Posição vs ITSA4/BBAS3 deve respeitar concentração sectorial — não somar +10% em estatais.

##### 7. Tracking triggers (auto-monitoring)

- **DY colapso** — `fundamentals.dy` < 5.0% (sinal de corte de payout ou rerating preço).
- **Leverage spike** — `fundamentals.net_debt_ebitda` > 2.5x (degradação balance sheet).
- **ROE deterioração** — `fundamentals.roe` < 15% por 2 trimestres consecutivos.
- **Streak break** — `fundamentals.dividend_streak_years` regrida (cancelamento de proventos).
- **Thesis health** — `scores.details_json::thesis_health` < 60 (Synthetic IC reset para HOLD/SELL).

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
*Generated by `ii dossier PETR4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=6 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Genial Investimentos | valuation | 1.00 | O preço-alvo da Petrobras é de R$50, gerando potencial de valorização. |
| 2026-05-13 | Genial Investimentos | risk | 0.90 | A política de preços é o que mais gera volatilidade para a Petrobras. |
| 2026-05-13 | Virtual Asset | capex | 0.80 | A Petrobras está investindo cerca de 12 bilhões de reais na conclusão do trem 2 e manutenção do trem 1 da refinaria Abreu e Lima. |
| 2026-05-13 | Genial Investimentos | catalyst | 0.80 | A Petrobras pode ampliar sua forma de remuneração do acionista na forma de dividendos. |
| 2026-05-13 | Genial Investimentos | thesis_bull | 0.80 | A Petrobras precisa buscar fontes fora do pré-sal para manter a capacidade de entrega de resultados no longo prazo. |
| 2026-05-13 | Virtual Asset | valuation | 0.70 | As ações da Petrobras estão corrigindo na Bolsa de Valores, mas o PL (Preço/Lucro) é considerado baixo e pode subir em breve com novos divi… |
| 2026-05-13 | Genial Investimentos | catalyst | 0.70 | Aumento da gasolina pode ser um catalisador positivo para a Petrobras, embora possa haver medidas provisórias sobre subvenção à gasolina. |
| 2026-05-12 | Suno | capex | 0.90 | A Petrobras aumentou seu investimento em capital (CAPEX) no último trimestre, o que impactou negativamente a geração de caixa livre. |
| 2026-05-12 | Suno | operational | 0.90 | A receita líquida da Petrobras ficou estática em R$123 bilhões, apesar do aumento significativo no preço do petróleo. |
| 2026-05-12 | Suno | guidance | 0.80 | A Petrobras espera resultados mais fortes no segundo trimestre de 2026, devido ao atraso na negociação dos preços das exportações. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 38.00 | [Suno Valor] PETR4 — peso 7.5%, rating Aguardar, PT R$38.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PETR4 — peso 9.6%, setor Energy |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] PETR4 — peso 13.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PETR4 — peso 4.1% |
| 2026-04-24 | XP | catalyst | neutral | — | A Petrobras reajustou em 55% o preço do querosene de aviação, gerando apreensão no setor aéreo. |
| 2026-04-14 | XP | rating | bull | 47.00 | [XP Top Dividendos] PETR4 — peso 10.0%, Compra, PT R$47.0, setor Energia |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · IC Debate (synthetic)
_source: `tickers\PETR4_IC_DEBATE.md` (now in cemetery)_

#### 🏛️ Synthetic IC Debate — PETR4

**Committee verdict**: **BUY** (high confidence, 80% consensus)  
**Votes**: BUY=4 | HOLD=1 | AVOID=0  
**Avg conviction majority**: 7.5/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- ROE de 28.18% muito alto
- P/E baixo e dividendos atrativos
- Geração de caixa forte

**Key risk**: Volatilidade dos preços do petróleo pode afetar resultados

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E baixo e DY atraente
- ROE forte e dívida controlada
- Histórico de dividendos

**Key risk**: Aumento significativo dos preços do petróleo impactando margens

###### 🟢 Nassim Taleb — **BUY** (conv 8/10, size: medium)

**Rationale**:
- P/E baixo e DY atraente
- ROE forte e dívida controlada
- Exposição ao petróleo com barbell strategy

**Key risk**: Flutuações bruscas nos preços do petróleo podem afetar significativamente os resultados

###### 🟡 Seth Klarman — **HOLD** (conv 6/10, size: medium)

**Rationale**:
- Valuation attractive with P/E of 6.08
- Strong dividend yield at 6.92%
- Solid ROE of 28.18%

**Key risk**: Volatility in commodity prices could impact earnings

###### 🟢 Ray Dalio — **BUY** (conv 7/10, size: medium)

**Rationale**:
- P/E baixo e DY atraente
- ROE forte
- FCF positivo

**Key risk**: Aumento da dívida líquida ou queda do ROE

##### 📊 Context provided

```
TICKER: BR:PETR4

FUNDAMENTALS LATEST:
  pe: 6.0812244
  pb: 1.415685
  dy: 6.92%
  roe: 28.18%
  net_debt_ebitda: 1.6018573174239312
  intangible_pct_assets: 1.1%   (goodwill $0.0B + intangibles $2.5B)

QUARTERLY TRAJECTORY (single-Q, R$ bi):
  2025-09-30: rev=127.9 ebit=43.6 ni=32.8 em%=34.1 debt=376 fcf=27.7
  2025-06-30: rev=119.1 ebit=30.5 ni=26.8 em%=25.6 debt=371 fcf=27.9
  2025-03-31: rev=123.1 ebit=43.0 ni=35.3 em%=35.0 debt=370 fcf=39.1
  2024-12-31: rev=121.3 ebit=13.2 ni=-17.0 em%=10.9 debt=373 fcf=28.5
  2024-09-30: rev=129.6 ebit=46.5 ni=32.7 em%=35.9 debt=322 fcf=36.4
  2024-06-30: rev=122.3 ebit=33.5 ni=-2.5 em%=27.4 debt=331 fcf=36.7

VAULT THESIS:
**Core thesis (2026-04-25)**: A PETR4, com um P/E de 6.22 e um DY de 6.76%, oferece um valor atrativo para investidores em busca de retornos estáveis. A empresa atende aos critérios da filosofia value-investing ajustada à Selic alta, destacando-se pelo ROE de 28.18% e uma dívida líquida/EBITDA de 1.60.

**Key assumptions**:
1. A PETR4 manterá seu histórico de dividendos ininterrupto por mais dois anos
2. O preço da ação não subirá acima do Graham Number ajustado para o ambiente atual (22.5)
3. A empresa continuará gerando um ROE superior a 15%
4. As condições macroeconômicas globais não afetarão negativamente os lucros operacionais da PETR4

**Disconfirmation triggers**:
- ROE cair abaixo de 12% por dois trimestres consecutivos
- Dividendos serem cortados ou pausados
- A dívida líquida/EBI

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Petro Victory reports stacked gas pay in SJ-12 well, offshore Brazil - World Oil [Tue, 28 Ap]
    World Oil Events Gulf Energy Information Excellence Awards Women's Global Leadership Conference World Oil Forecast Breakfast Deepwater Development Conference (MCEDD). # Petro Victory reports stacked g
  - Brazil's Petrobras raises natural gas prices by 19% after oil shock - Reuters [Sat, 02 Ma]
    REUTERS/Amanda Perobelli/File Photo Purchase Licensing Rights, opens new tab. 
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

##### 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=10 · analyst=6 · themes=5_

###### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-13 | Genial Investimentos | valuation | 1.00 | O preço-alvo da Petrobras é de R$50, gerando potencial de valorização. |
| 2026-05-13 | Genial Investimentos | risk | 0.90 | A política de preços é o que mais gera volatilidade para a Petrobras. |
| 2026-05-13 | Virtual Asset | capex | 0.80 | A Petrobras está investindo cerca de 12 bilhões de reais na conclusão do trem 2 e manutenção do trem 1 da refinaria Abreu e Lima. |
| 2026-05-13 | Genial Investimentos | catalyst | 0.80 | A Petrobras pode ampliar sua forma de remuneração do acionista na forma de dividendos. |
| 2026-05-13 | Genial Investimentos | thesis_bull | 0.80 | A Petrobras precisa buscar fontes fora do pré-sal para manter a capacidade de entrega de resultados no longo prazo. |
| 2026-05-13 | Virtual Asset | valuation | 0.70 | As ações da Petrobras estão corrigindo na Bolsa de Valores, mas o PL (Preço/Lucro) é considerado baixo e pode subir em breve com novos divi… |
| 2026-05-13 | Genial Investimentos | catalyst | 0.70 | Aumento da gasolina pode ser um catalisador positivo para a Petrobras, embora possa haver medidas provisórias sobre subvenção à gasolina. |
| 2026-05-12 | Suno | capex | 0.90 | A Petrobras aumentou seu investimento em capital (CAPEX) no último trimestre, o que impactou negativamente a geração de caixa livre. |
| 2026-05-12 | Suno | operational | 0.90 | A receita líquida da Petrobras ficou estática em R$123 bilhões, apesar do aumento significativo no preço do petróleo. |
| 2026-05-12 | Suno | guidance | 0.80 | A Petrobras espera resultados mais fortes no segundo trimestre de 2026, devido ao atraso na negociação dos preços das exportações. |

###### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 38.00 | [Suno Valor] PETR4 — peso 7.5%, rating Aguardar, PT R$38.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PETR4 — peso 9.6%, setor Energy |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] PETR4 — peso 13.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PETR4 — peso 4.1% |
| 2026-04-24 | XP | catalyst | neutral | — | A Petrobras reajustou em 55% o preço do querosene de aviação, gerando apreensão no setor aéreo. |
| 2026-04-14 | XP | rating | bull | 47.00 | [XP Top Dividendos] PETR4 — peso 10.0%, Compra, PT R$47.0, setor Energia |

###### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-13 | Virtual Asset | banking_br | bearish | Investidores estrangeiros estão saindo do Brasil devido ao rally de alta forte da Bolsa seguido por resultado… |
| 2026-05-13 | Virtual Asset | banking_br | bullish | O Itaú apresentou um balanço forte, com lucratividade de R$12,3 bilhões e ROE de 24,8%, apesar de ficar ligei… |
| 2026-05-13 | Virtual Asset | banking_br | neutral | O Itaú apresentou um controle de inadimplência invejável, com índice de apenas 1,9%, mas há riscos a monitora… |
| 2026-05-13 | Virtual Asset | ipca_inflacao | bullish | Aumento na produção de diesel pela Petrobras pode ajudar a controlar a inflação no Brasil. |
| 2026-05-13 | Virtual Asset | oil_cycle | bullish | A Petrobras alcançou um novo recorde de produção de diesel, o que melhora a segurança energética do Brasil e… |

#### — · RI / disclosure
_source: `tickers\PETR4_RI.md` (now in cemetery)_

#### PETR4 — RI Quarterly Compare

**Latest period**: 2025-09-30  
**Q-o-Q vs**: 2025-06-30  
**YoY vs**: 2024-09-30  

##### 🚨 Material changes

- ⬆️ **QOQ** `ebit`: **+43.2%**
- ⬆️ **QOQ** `net_income`: **+22.7%**
- ⬆️ **QOQ** `ebit_margin`: **+8.5pp**
- ⬇️ **YOY** `fcf_proxy`: **-23.9%**

##### Q-o-Q (2025-09-30 vs 2025-06-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 127.9 mi | R$ 119.1 mi | +7.4% |
| `ebit` | R$ 43.6 mi | R$ 30.5 mi | +43.2% |
| `net_income` | R$ 32.8 mi | R$ 26.8 mi | +22.7% |
| `debt_total` | R$ 376.1 mi | R$ 371.4 mi | +1.3% |
| `fco` | R$ 53.7 mi | R$ 42.4 mi | +26.5% |
| `fcf_proxy` | R$ 27.7 mi | R$ 27.9 mi | -0.5% |
| `gross_margin` | 47.8% | 47.6% | +0.2pp |
| `ebit_margin` | 34.1% | 25.6% | +8.5pp |
| `net_margin` | 25.7% | 22.5% | +3.2pp |

##### YoY (2025-09-30 vs 2024-09-30)

| Metric | Current | Prior | Change |
|---|---:|---:|---:|
| `revenue` | R$ 127.9 mi | R$ 129.6 mi | -1.3% |
| `ebit` | R$ 43.6 mi | R$ 46.5 mi | -6.1% |
| `net_income` | R$ 32.8 mi | R$ 32.7 mi | +0.5% |
| `debt_total` | R$ 376.1 mi | R$ 322.2 mi | +16.7% |
| `fco` | R$ 53.7 mi | R$ 62.7 mi | -14.5% |
| `fcf_proxy` | R$ 27.7 mi | R$ 36.4 mi | -23.9% |
| `gross_margin` | 47.8% | 51.4% | -3.6pp |
| `ebit_margin` | 34.1% | 35.9% | -1.7pp |
| `net_margin` | 25.7% | 25.2% | +0.5pp |

##### 📊 Trajetória 11Q

| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |
|---|---|---:|---:|---:|---:|---:|
| 2025-09-30 | ITR | 127.9 | 34.1% | 25.7% | 376 | 54 |
| 2025-06-30 | ITR | 119.1 | 25.6% | 22.5% | 371 | 42 |
| 2025-03-31 | ITR | 123.1 | 35.0% | 28.7% | 370 | 49 |
| 2024-12-31 | DFP-ITR | 121.3 | 10.9% | -14.0% | 373 | 48 |
| 2024-09-30 | ITR | 129.6 | 35.9% | 25.2% | 322 | 63 |
| 2024-06-30 | ITR | 122.3 | 27.4% | -2.1% | 331 | 47 |
| 2024-03-31 | ITR | 117.7 | 37.4% | 20.2% | 309 | 46 |
| 2023-12-31 | DFP-ITR | 134.3 | 29.5% | 23.2% | 303 | 58 |
| 2023-09-30 | ITR | 124.8 | 38.1% | 21.4% | 305 | 57 |
| 2023-06-30 | ITR | 113.8 | 36.9% | 25.4% | 279 | 48 |
| 2023-03-31 | ITR | 139.1 | 43.3% | 27.5% | 271 | 54 |

##### Chart: Revenue + EBIT margin trend

```chart
type: line
title: "Revenue (R$bi) + EBIT margin %"
labels: ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30']
series:
  - title: Revenue
    data: [139.1, 113.8, 124.8, 134.3, 117.7, 122.3, 129.6, 121.3, 123.1, 119.1, 127.9]
  - title: EBIT margin %
    data: [43.3, 36.9, 38.1, 29.5, 37.4, 27.4, 35.9, 10.9, 35.0, 25.6, 34.1]
width: 90%
beginAtZero: false
tension: 0.3
```

---
*Auto-generated by `library.ri.compare_releases` from CVM official data.*

## ⚙️ Refresh commands

```bash
ii panorama PETR4 --write
ii deepdive PETR4 --save-obsidian
ii verdict PETR4 --narrate --write
ii fv PETR4
python -m analytics.fair_value_forward --ticker PETR4
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
