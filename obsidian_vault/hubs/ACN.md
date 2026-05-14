---
type: ticker_hub
ticker: ACN
market: us
sector: Technology
currency: USD
bucket: holdings
is_holding: true
generated: 2026-05-14
sources_merged: 16
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# ACN — Accenture

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Technology` · `market: US` · `currency: USD` · `bucket: holdings` · `16 sources merged`

## 🎯 Hoje

- **Posição**: 4.30506 @ entry 213.70666146348714
- **Verdict (DB)**: `WATCH` (score 6.62, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 13.07 · P/B 3.14 · DY 1.9% · ROE 24.8% · ND/EBITDA -0.08 · Dividend streak 22 · Aristocrat no

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-06-18 · Earnings prep
_source: `briefings\earnings_prep_ACN_2026-06-18.md`_

#### 📞 Earnings Prep — ACN (2026-06-18)

_Auto-generated 54 days before call. 100% Ollama local._

##### 🔥 Top 3 things to watch
- Crescimento da receita acima de 15% (indicador de demanda por serviços de consultoria em IA)
- Margem operacional > 15%
- Taxa de utilização dos consultores acima de 90%

##### ❓ Specific questions to listen for management
1. Como a empresa planeja manter sua liderança no mercado de transformação digital e implementação de IA?
2. Quais são os principais desafios relacionados à retenção de talentos na ACN?
3. Como as consultorias rivais como Google, Microsoft e Amazon estão impactando o negócio da ACN?
4. Qual é a estratégia para manter margens operacionais acima de 15% em face da pressão nos preços dos serviços legados?
5. Quais são os planos para investimentos futuros na vertical de governo e saúde?

##### 📊 Trajectory check (vs trend)
- Confirmar que a receita continua crescendo entre 15-20% ao ano
- Mudança necessária se as margens operacionais caírem abaixo de 13%

##### 🚨 Red flags potenciais
- Margem operacional caindo para menos de 13%
- Aumento significativo no índice net debt/EBITDA

##### 🎯 Decision framework
- BUY MORE if: Crescimento da receita > 20% e margens operacionais > 15%
- HOLD if: Crescimento da receita entre 10-15% com margens operacionais estabilizadas em torno de 13-14%
- TRIM if: Crescimento da receita < 10% ou margem operacional < 12%

---
##### 📊 Context provided to LLM

```
TICKER: US:ACN
EARNINGS DATE: 2026-06-18

FUNDAMENTALS:
  pe: 14.631666
  pb: 3.5136518
  dy: 1.74%
  roe: 24.76%
  net_debt_ebitda: -0.08309405074235562

THESIS HEALTH: 91/100 (contras=1, risk_flags=1)

OUR THESIS:
**Core thesis (2026-04-24)**: ACN é consultoria global #1 em digital
transformation + AI implementation. Posição única — as empresas Fortune 500
não têm talent in-house para GenAI rollouts; ACN captura spend
incremental sustentável 5-10 anos. ROE 25%+, dividend streak 20y, buybacks
consistentes. Valuation actual oferece margem de segurança após 2024 drawdown.

**Key assumptions**:
1. AI implementation spend continua crescendo (15-20% YoY para top-tier consultoria)
2. ACN mantém margin > 15% apesar de pricing pressure em serviços legacy
3. Talent retention estável (people business — churn é existential)
4. US + EU government/healthcare verticals não cortam consulting budgets

**Disconfirmation triggers**:
- Revenue growth < 5% em 2 quarters (sinal secular decline consulting)
- Margins cap < 13% por custo pressure
- Utilization rate cai abaixo 90%
- Mass layoffs (sinal de over-hiring pré-downturn)
- Google / Microsoft / Amazon entrarem em consulting no scale da ACN

**Intent**: Compounder long-term (DRIP + buybacks). Peso target 7-10% da carteira US.

---
*Gerado por obsidian_bridge — 2026-04-24 15:20 UTC*
```

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\ACN.md` (cemetery archive)_

#### ACN — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.accenture.com/
- **Pilot rationale**: known (holding)

##### Antes (estado da DB)

**Posição activa**: qty=4.30506 · entry=213.70666146348714 · date=2023-09-28

- Total events na DB: **44**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=172.35000610351562
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.24763 · DY=0.0180446758912912 · P/E=14.127049
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | 8-K | sec | 8-K \| 1.01,1.02,2.03,9.01 |
| 2026-03-19 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-19 | 10-Q | sec | 10-Q |
| 2026-01-28 | 8-K | sec | 8-K \| 5.02,5.07,9.01 |
| 2025-12-18 | 8-K | sec | 8-K \| 2.02,9.01 |

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

#### 2026-04-30 · Council review · Charlie Compounder
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Charlie Compounder\reviews\ACN_2026-04-30.md` (cemetery archive)_

#### Charlie Compounder sobre [[ACN_STORY|ACN]]

**Função no debate**: Industrials & Consumer US Specialist (Buffett frame) (`sector_specialist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Accenture mantém posição única em consultoria digital_

ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.

**Métricas que invoquei**:
- P/E=14.65
- ROE=24.8%
- DivStreak=20y

**Preocupações**:
- DY abaixo da média do setor (1.7%)
- Margens sob pressão em serviços legacy

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Mariana Macro

**Evidência nova**: Accenture continua a investir em inovação tecnológica, como o uso de robótica humanaide para operações em armazéns e fábricas, demonstrando sua capacidade de se adaptar às mudanças do mercado.

##### Quem mais estava na sala

- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ACN_STORY|📖 Storytelling completo (8 actos)]]
- [[ACN_COUNCIL|🏛️ Transcript do Council debate]]
- [[Charlie Compounder|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Mariana Macro
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Mariana Macro\reviews\ACN_2026-04-30.md` (cemetery archive)_

#### Mariana Macro sobre [[ACN_STORY|ACN]]

**Função no debate**: Chief Macro Strategist (`macro_strategist`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Accenture mantém posição de liderança em consultoria digital_

ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+ e histórico consistente de dividendos e recompra de ações. Valuation atual oferece margem de segurança.

**Métricas que invoquei**:
- ROE de 24.8%
- Dividend streak de 20 anos
- P/E de 14.65x

**Preocupações**:
- Pressão nos serviços legados pode afetar margens
- Possível corte em orçamentos governamentais

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Charlie Compounder

**Evidência nova**: Accenture recentemente investiu em General Robotics para avançar na robótica física alimentada por IA em manufatura e logística, demonstrando sua capacidade de inovar e expandir seus serviços.

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Valentina Prudente]] (Chief Risk Officer)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ACN_STORY|📖 Storytelling completo (8 actos)]]
- [[ACN_COUNCIL|🏛️ Transcript do Council debate]]
- [[Mariana Macro|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Pedro Alocação
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Pedro Alocação\reviews\ACN_2026-04-30.md` (cemetery archive)_

#### Pedro Alocação sobre [[ACN_STORY|ACN]]

**Função no debate**: Capital Allocator (`portfolio_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Accenture mantém posição única em consultoria digital_

ACN lidera na implementação de AI e transformação digital, com ROE de 25%+ e dividendos consistentes. Valuation atrativo após drawdown.

**Métricas que invoquei**:
- ROE=24.8%
- Dividend Yield=1.7%
- P/E=14.65x

**Preocupações**:
- crescimento de receita abaixo de 5% por dois trimestres
- margens menores do que esperado

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Accenture beneficia de crescimento sustentável na implementação de AI e forte retorno sobre o capital (ROE 25%). Valuation atrativo após drawdown.

**Desafiei**:
- DY abaixo da média do setor (1.7%) | Margens sob pressão em serviços legacy
- Pressão nos serviços legados pode afetar margens | Possível corte em orçamentos governamentais

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Valentina Prudente]] (Chief Risk Officer)

##### Documentos relacionados

- [[ACN_STORY|📖 Storytelling completo (8 actos)]]
- [[ACN_COUNCIL|🏛️ Transcript do Council debate]]
- [[Pedro Alocação|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*

#### 2026-04-30 · Council review · Valentina Prudente
_source: `cemetery\2026-05-14\ABSORBED-council-reviews\agents\Valentina Prudente\reviews\ACN_2026-04-30.md` (cemetery archive)_

#### Valentina Prudente sobre [[ACN_STORY|ACN]]

**Função no debate**: Chief Risk Officer (`risk_officer`)  
**Data**: 2026-04-30  
**Stance final**: 🟢 **BUY**  

##### Round 1 — Abertura (cega aos colegas)

> _Accenture mantém posição única em consultoria digital_

ACN beneficia de crescimento sustentável na implementação de AI e forte retorno sobre o capital (ROE 25%). Valuation atrativo após drawdown.

**Métricas que invoquei**:
- P/E=14.65
- ROE=25%
- DivStreak=22

**Preocupações**:
- crescimento de receita < 5% em dois trimestres
- margens abaixo de 15%

##### Round 2 — Resposta aos colegas

**Concordei com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Charlie Compounder

**Desafiei**:
- Pressão nos serviços legados pode afetar margens
- Mariana Macro
- A pressão em serviços legacy é um risco, mas a empresa tem demonstrado resiliência ao diversificar seus negócios para áreas como IA e robótica.
- Pedro Alocação

**Evidência nova**: Accenture continua investindo em inovação, como o uso de humanoid robotics em operações de armazém com parceiros estratégicos.

##### Quem mais estava na sala

- [[Charlie Compounder]] (Industrials & Consumer US Specialist (Buffett frame))
- [[Mariana Macro]] (Chief Macro Strategist)
- [[Pedro Alocação]] (Capital Allocator)

##### Documentos relacionados

- [[ACN_STORY|📖 Storytelling completo (8 actos)]]
- [[ACN_COUNCIL|🏛️ Transcript do Council debate]]
- [[Valentina Prudente|👤 Minha página de persona]]

---
*Gerado pelo Council `2026-04-30` — STORYT_2.0 Camada 5.5*


### 2023

#### 2023-02-01 · Filing 2023-02-01
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN_FILING_2023-02-01.md` (cemetery archive)_

#### Filing dossier — [[ACN]] · 2023-02-01

**Trigger**: `sec:8-K` no dia `2023-02-01`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1467373/000146737323000071/acn-20230201.htm>

##### 🎯 Acção sugerida

###### 🔴 **SELL** &mdash; preço 180.42

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `115.48` |
| HOLD entre | `115.48` — `148.05` (consensus) |
| TRIM entre | `148.05` — `170.26` |
| **SELL acima de** | `170.26` |

_Método: `buffett_ceiling`. Consensus fair = R$148.05. Our fair (mais conservador) = R$115.48._

##### 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.24763` | `0.2471` | +0.2% |
| EPS | `12.2` | `12.0934` | +0.9% |


##### 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

##### 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 180.42 | SELL | cross_validated | `filing:sec:8-K:2023-02-01` |
| 2026-05-08T20:37:29+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 180.42 | SELL | cross_validated | `manual` |
| 2026-05-08T17:48:11+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_dualclass_fixed` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._


### (undated)

#### — · Dossier
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN.md` (cemetery archive)_

#### [[ACN]] — Dossier Deepdive (2026-05-05)

> Sector: Technology · Country: Ireland · Price: 180.12 USD

##### Quality Scores

| Score | Valor | Zona |
|---|---|---|
| Piotroski | 5/9 | - |
| Altman Z | 4.204971537327859 | safe |
| Beneish M | -2.7542451177222134 | clean |


##### Delta Report

```
Delta Report — ACN | hoje vs run anterior (2026-05-04)
  Beneish M: -2.75 (novo — não comparável)
```

##### Strategist Dossier

#### 1. Executive Summary
- **Rating:** MANTER
- **Preço justo estimado:** 205 USD (Upside: 13,8%)
- **Risk Score:** 6/10 (Risco moderado devido a fatores macroeconômicos e setoriais)
- **Alerta vermelho:** Não há necessidade de alerta vermelho específico com base nos dados fornecidos.

#### 2. O Negócio
**Modelo de receita, fontes de caixa:**
Accenture plc é uma empresa líder em serviços de tecnologia da informação e consultoria estratégica. Sua principal fonte de receita provém dos serviços prestados a grandes empresas multinacionais, incluindo implementação de sistemas, otimização operacional e transformações digitais.

**Moat (Network Effect / Switching Costs / Intangibles / Cost Adv):**
- **Network Effect:** 2/5 - A empresa não beneficia significativamente do network effect.
- **Switching Costs:** 4/5 - Altos custos de troca para clientes, uma vez que a integração e dependência dos serviços são elevadas.
- **Intangibles (Branding & IP):** 3/5 - Marca forte no setor, mas não dominante.
- **Cost Adv:** 4/5 - Economias de escala significativas em operações globais.

#### 3. Decomposição DuPont
**ROE = Margem × Giro × Alavancagem**
- **Margem Líquida:** 10,6% (Graças à eficiência operacional e mix de serviços).
- **Giro Ativo:** 0,85 (Indicando um uso eficiente dos ativos).
- **Alavancagem Financeira:** 1,43 (Nível moderado de alavancagem).

**Identificar a alavanca dominante:**
A margem líquida e o giro são os principais drivers do ROE. A alavancagem financeira está em um nível sustentável.

#### 4. Valuation Multinível
- **Graham Number:** Não aplicável devido à natureza cíclica e volátil dos múltiplos setoriais.
- **DCF (Bear / Base / Bull):**
  - Bear Case: 175 USD (Cenário pessimista com crescimento mais lento).
  - Base Case: 205 USD (Cenário médio com crescimento sustentado).
  - Bull Case: 235 USD (Cenário otimista com aceleração de crescimento).

- **EV/EBITDA vs mediana setor:** 
  - Accenture plc: 8,7x
  - Mediana do setor: 10,5x

#### 5. Bear Case
**3 maiores riscos com prob × impacto:**
1. **Risco de Corte de Custos Corporativos (40% x 20%)**: Clientes podem optar por reduzir gastos em consultoria.
2. **Aumento da Concorrência (50% x 30%)**: Novas empresas emergentes podem desafiar a posição dominante.
3. **Riscos Macroeconômicos (60% x 15%)**: Flutuações econômicas globais impactando demanda.

**Cenário de -40%:**
- Preço cairia para aproximadamente 108 USD, refletindo uma percepção negativa generalizada do mercado e possíveis problemas operacionais.

#### 6. Bull Case
**Catalisadores específicos com prazo:**
1. **Aquisições estratégicas (2-3 anos)** - Expansão de serviços através da aquisição de empresas menores.
2. **Inovação tecnológica (1-2 anos)** - Lançamento de novos produtos e serviços disruptivos.

**O que precisa acontecer para o preço dobrar em 3 anos?**
- Crescimento acelerado das receitas, principalmente no segmento de transformação digital.
- Aumento da eficiência operacional e margens.
- Aquisições bem-sucedidas que impulsionem a base de clientes.

#### 7. Classificação Lynch
**Slow / Stalwart / Fast / Cyclical / Turnaround / Asset Play:**
- **Stalwart**: Empresa estabelecida com crescimento sustentado e forte presença no mercado.
- **2-3 argumentos objectivos:** 
  - Marca forte e reconhecimento global.
  - Diversificação geográfica e setorial reduzindo riscos.
  - Histórico de crescimento consistente.

#### 8. Veredicto Final
**Decisão com 3 critérios mensuráveis:**
- **Preço justo:** 205 USD (13,8% upside).
- **Margem de Segurança:** Baseada em múltiplos setoriais e DCF.
- **Risco Operacional:** Moderado.

**Position sizing: núcleo / satélite / especulativo / evitar**
- **Satélite**: A posição deve ser parte do portfólio diversificado, mas não dominante devido aos riscos operacionais moderados e macroeconômicos.

---
*Generated by `ii deepdive ACN` em 2026-05-05T06:39:20.*

#### — · Council aggregate
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN_COUNCIL.md` (cemetery archive)_

#### Council Debate — [[ACN_STORY|ACN]] (Accenture)

**Final stance**: 🟢 **BUY**  
**Confidence**: `high`  
**Modo (auto)**: A (US)  |  **Sector**: Technology  |  **Held**: sim  
**Elapsed**: 61.4s  |  **Failures**: 0

##### Quem esteve na sala

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_ (`sector_specialist`)
- [[Mariana Macro]] — _Chief Macro Strategist_ (`macro_strategist`)
- [[Valentina Prudente]] — _Chief Risk Officer_ (`risk_officer`)
- [[Pedro Alocação]] — _Capital Allocator_ (`portfolio_officer`)

##### Síntese

**Consenso**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes.
- Valuation atual oferece margem de segurança.

**Dissenso (preservado)**:
- Charlie Compounder disse que a pressão nos serviços legados pode afetar margens, Mariana Macro concordou com isso mas Valentina Prudente argumenta que a empresa tem demonstrado resiliência ao diversificar seus negócios para áreas como IA e robótica.

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ DY abaixo da média do setor (1.7%) | Pressão nos serviços legados pode afetar margens | Possível corte em orçamentos governamentais

**Sizing**: Pedro Alocação recomenda manter posição atual devido ao crescimento sustentável na implementação de AI e forte retorno sobre o capital.

##### Round 1 — Opening Statements (blind)

###### [[Charlie Compounder]] — 🟢 **BUY**
_Industrials & Consumer US Specialist (Buffett frame)_

**Headline**: _Accenture mantém posição única em consultoria digital_

ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.

**Métricas**:
- P/E=14.65
- ROE=24.8%
- DivStreak=20y

**Preocupações**:
- DY abaixo da média do setor (1.7%)
- Margens sob pressão em serviços legacy

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Headline**: _Accenture mantém posição de liderança em consultoria digital_

ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+ e histórico consistente de dividendos e recompra de ações. Valuation atual oferece margem de segurança.

**Métricas**:
- ROE de 24.8%
- Dividend streak de 20 anos
- P/E de 14.65x

**Preocupações**:
- Pressão nos serviços legados pode afetar margens
- Possível corte em orçamentos governamentais

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Headline**: _Accenture mantém posição única em consultoria digital_

ACN beneficia de crescimento sustentável na implementação de AI e forte retorno sobre o capital (ROE 25%). Valuation atrativo após drawdown.

**Métricas**:
- P/E=14.65
- ROE=25%
- DivStreak=22

**Preocupações**:
- crescimento de receita < 5% em dois trimestres
- margens abaixo de 15%

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Headline**: _Accenture mantém posição única em consultoria digital_

ACN lidera na implementação de AI e transformação digital, com ROE de 25%+ e dividendos consistentes. Valuation atrativo após drawdown.

**Métricas**:
- ROE=24.8%
- Dividend Yield=1.7%
- P/E=14.65x

**Preocupações**:
- crescimento de receita abaixo de 5% por dois trimestres
- margens menores do que esperado

##### Round 2 — Respostas (peers visíveis)

###### [[Charlie Compounder]] — 🟢 **BUY**
_Industrials & Consumer US Specialist (Buffett frame)_

**Concordou com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Mariana Macro

**Evidência nova**: Accenture continua a investir em inovação tecnológica, como o uso de robótica humanaide para operações em armazéns e fábricas, demonstrando sua capacidade de se adaptar às mudanças do mercado.

###### [[Mariana Macro]] — 🟢 **BUY**
_Chief Macro Strategist_

**Concordou com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Charlie Compounder

**Evidência nova**: Accenture recentemente investiu em General Robotics para avançar na robótica física alimentada por IA em manufatura e logística, demonstrando sua capacidade de inovar e expandir seus serviços.

###### [[Valentina Prudente]] — 🟢 **BUY**
_Chief Risk Officer_

**Concordou com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Charlie Compounder

**Desafiou**:
- Pressão nos serviços legados pode afetar margens
- Mariana Macro
- A pressão em serviços legacy é um risco, mas a empresa tem demonstrado resiliência ao diversificar seus negócios para áreas como IA e robótica.
- Pedro Alocação

**Evidência nova**: Accenture continua investindo em inovação, como o uso de humanoid robotics em operações de armazém com parceiros estratégicos.

###### [[Pedro Alocação]] — 🟢 **BUY**
_Capital Allocator_

**Concordou com**:
- ACN é líder global em transformação digital e implementação de IA, com ROE de 25%+, dividend streak de 20 anos e buybacks consistentes. Valuation atual oferece margem de segurança.
- Accenture beneficia de crescimento sustentável na implementação de AI e forte retorno sobre o capital (ROE 25%). Valuation atrativo após drawdown.

**Desafiou**:
- DY abaixo da média do setor (1.7%) | Margens sob pressão em serviços legacy
- Pressão nos serviços legados pode afetar margens | Possível corte em orçamentos governamentais

##### Documentos relacionados

- [[ACN_STORY|📖 Storytelling completo (8 actos)]]
- Reviews individuais por especialista:
  - [[ACN_2026-04-30|Charlie Compounder]] em [[Charlie Compounder]]/reviews/
  - [[ACN_2026-04-30|Mariana Macro]] em [[Mariana Macro]]/reviews/
  - [[ACN_2026-04-30|Valentina Prudente]] em [[Valentina Prudente]]/reviews/
  - [[ACN_2026-04-30|Pedro Alocação]] em [[Pedro Alocação]]/reviews/

##### Dossier (factual base — same input para todos)

```
=== TICKER: US:ACN — Accenture ===
Sector: Technology  |  Modo (auto): A  |  Held: True
Last price: 178.7100067138672 (2026-04-30)
Position: 4 shares @ entry 213.71
Fundamentals: P/E=14.65 | P/B=3.52 | DY=1.7% | ROE=24.8% | ND/EBITDA=-0.08 | DivStreak=22.00

VAULT THESIS (~800 chars):
**Core thesis (2026-04-24)**: ACN é consultoria global #1 em digital
transformation + AI implementation. Posição única — as empresas Fortune 500
não têm talent in-house para GenAI rollouts; ACN captura spend
incremental sustentável 5-10 anos. ROE 25%+, dividend streak 20y, buybacks
consistentes. Valuation actual oferece margem de segurança após 2024 drawdown.

**Key assumptions**:
1. AI implementation spend continua crescendo (15-20% YoY para top-tier consultoria)
2. ACN mantém margin > 15% apesar de pricing pressure em serviços legacy
3. Talent retention estável (people business — churn é existential)
4. US + EU government/healthcare verticals não cortam consulting budgets

**Disconfirmation triggers**:
- Revenue growth < 5% em 2 quarters (sinal secular decline consulting)
- Margins cap <

PORTFOLIO CONTEXT:
  Active positions (US): 21
  This position weight: 3.4%
  Sector weight: 19.3%

QUALITY SCORES:
  Piotroski F-Score: 5/9 (2025-08-31)
  Altman Z-Score: 4.20  zone=safe  conf=high
  Beneish M-Score: -2.75  zone=clean  conf=high

WEB CONTEXT (qualitative research, last 30-90d):
  - Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations - Financial Times [Wed, 22 Ap]
    ### Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations. HANNOVER, Germany--(BUSINESS WIRE)--Apr. 22, 2026-- Accenture (NYSE: ACN), together with Vodafone Procure & Connect and SAP, is piloting the 
  - Accenture backs robotics software to speed factory, warehouse automation - Stock Titan [Wed, 15 Ap]
    4. Accenture Invests in General Robotics to Advance Physical AI-Powered Robotics in Manufacturing and Logistics. # Accenture Invests in General Robotics to Advance Physical AI-Powered Robotics in Manufacturing and Logistics. With this inves
  - Can AI cut factory downtime? Accenture builds shop-floor agents - Stock Titan [Mon, 20 Ap]
    4. Accenture and Avanade Collaborate with Microsoft to Develop Agentic Factory to Help Reduce Manufacturing Downtime. # Accenture and Avanade Collaborate with Microsoft to Develop Agentic Factory to Help Reduce Manufacturing Downtime. HANNO
  - Accenture and Anthropic Team to Help Organizations Secure, Scale AI-Driven Cybersecurity Operations - Financial Times [Wed, 25 Ma]
    ### Accenture and Anthropic Team to Help Organizations Secure, Scale AI-Driven Cybersecurity Operations. NEW YORK & SAN FRANCISCO--(BUSINESS WIRE)--Mar. 25, 2026-- RSA 2026--Accenture (NYSE: ACN) has launched Cyber.AI, a new solution powere
  - Accenture signals hiring recovery with steady workforce growth in Q2 - HR Katha [Fri, 20 Ma]
    # Accenture signals hiring recovery with steady workforce growth in Q2. Share   LinkedIn   Twitter")   Facebook   WhatsApp. Accenture reported a rise in its employee base during the second quarter of fiscal 2026, pointing to a gradual shift

============================================================
RESEARCH BRIEFING (Ulisses Navegador puxou da casa):
============================================================

##### CVM/SEC EVENTS (fatos relevantes/filings) (7 hits)
[1] sec (8-K) [2026-04-24]: 8-K | 1.01,1.02,2.03,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737326000019/acn-20260422.htm
[2] sec (8-K) [2026-03-19]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737326000013/acn-20260319.htm
[3] sec (10-Q) [2026-03-19]: 10-Q
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737326000014/acn-20260228.htm
[4] sec (8-K) [2026-01-28]: 8-K | 5.02,5.07,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737326000005/acn-20260128.htm
[5] sec (8-K) [2025-12-18]: 8-K | 2.02,9.01
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737325000221/acn-20251218.htm
[6] sec (10-Q) [2025-12-18]: 10-Q
     URL: https://www.sec.gov/Archives/edgar/data/1467373/000146737325000222/acn-20251130.htm

##### TAVILY NEWS (≤30d) (5 hits)
[7] Tavily [Wed, 22 Ap]: ### Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations. HANNOVER, Germany--(BUSINESS WIRE)--Apr. 22, 2026-- Accenture (NYSE: ACN), together with Vodafone Procure & Connect and SAP, is piloting the use of humanoid robotics in warehouse environments, demonstr
     URL: https://markets.ft.com/data/announce/detail?dockey=600-202604220129BIZWIRE_USPRX____20260421_BW209563-1
[8] Tavily [Wed, 15 Ap]: 4. Accenture Invests in General Robotics to Advance Physical AI-Powered Robotics in Manufacturing and Logistics. # Accenture Invests in General Robotics to Advance Physical AI-Powered Robotics in Manufacturing and Logistics. With this investment, Accenture and General Robotics will also partner to h
     URL: https://www.stocktitan.net/news/ACN/accenture-invests-in-general-robotics-to-advance-physical-ai-powered-wo8ve9h69wdf.html
[9] Tavily [Mon, 20 Ap]: 4. Accenture and Avanade Collaborate with Microsoft to Develop Agentic Factory to Help Reduce Manufacturing Downtime. # Accenture and Avanade Collaborate with Microsoft to Develop Agentic Factory to Help Reduce Manufacturing Downtime. HANNOVER, Germany--(BUSINESS WIRE)-- Accenture (NYSE: ACN) and Av
     URL: https://www.stocktitan.net/news/ACN/accenture-and-avanade-collaborate-with-microsoft-to-develop-agentic-i498nssu7wm7.html
[10] Tavily [Wed, 15 Ap]: # Accenture acquires Spanish data and AI consultancy firm Keepler. ***Accenture has acquired Keepler, a leading data and AI consultancy firm in the Spanish market. Founded in 2018, Keepler offers AI and data capabilities across the value chain, from defining a data strategy and building cloud-native
     URL: https://www.consultancy.eu/news/amp/13517/accenture-acquires-spanish-data-and-ai-consultancy-firm-keepler
[11] Tavily [Wed, 15 Ap]: # Accenture and Google Cloud launch Sovereign Cloud and AI Innovation Center in Brussels. ***Accenture and Google Cloud have opened a new Sovereign Cloud and AI Innovation Center in Brussels, aimed at helping governments and highly regulated industries scale artificial intelligence while maintaining
     URL: https://www.consultancy.eu/news/amp/13505/accenture-and-google-cloud-launch-sovereign-cloud-and-ai-innovation-center-in-brussels

##### TAVILY GUIDANCE (≤90d) (5 hits)
[12] Tavily [Wed, 25 Ma]: ### Accenture and Anthropic Team to Help Organizations Secure, Scale AI-Driven Cybersecurity Operations. NEW YORK & SAN FRANCISCO--(BUSINESS WIRE)--Mar. 25, 2026-- RSA 2026--Accenture (NYSE: ACN) has launched Cyber.AI, a new solution powered by Claude, Anthropic’s AI model, that enables organization
     URL: https://markets.ft.com/data/announce/detail?dockey=600-202603251833BIZWIRE_USPRX____20260325_BW001195-1
[13] Tavily [Wed, 22 Ap]: ### Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations. HANNOVER, Germany--(BUSINESS WIRE)--Apr. 22, 2026-- Accenture (NYSE: ACN), together with Vodafone Procure & Connect and SAP, is piloting the use of humanoid robotics in warehouse environments, demonstr
     URL: https://markets.ft.com/data/announce/detail?dockey=600-202604220129BIZWIRE_USPRX____20260421_BW209563-1
[14] Tavily [Fri, 20 Ma]: # Accenture signals hiring recovery with steady workforce growth in Q2. Share   LinkedIn   Twitter")   Facebook   WhatsApp. Accenture reported a rise in its employee base during the second quarter of fiscal 2026, pointing to a gradual shift in hiring sentiment after months of cautious workforce mana
     URL: https://www.hrkatha.com/news/accenture-signals-hiring-recovery-with-steady-workforce-growth-in-q2/
[15] Tavily [Thu, 19 Ma]: Stock Market News Today, 3/19/26 – Stock Futures Slump as Iran War Intensifies, Fed Warns of Inflation. DIAQQQ](/news/stock-market-news-today-3-19-26-stock-futures-slump-as-iran-war-intensifies-fed-warns-of-inflation "DIA | QQQ | SPY"). CHNR](/news/why-is-china-natural-resources-stock-chnr-soaring-t
     URL: https://www.tipranks.com/news/private-companies/10-federal-highlights-data-driven-approach-to-self-storage-acquisitions
[16] Tavily [Thu, 19 Ma]: REUTERS/Dado Ruvic/Illustration Purchase Licensing Rights, opens new tab. March 19 (Reuters) - Accenture (ACN.N), opens new tab forecast quarterly ​revenue below estimates on Thursday, as clients remain ‌cautious on spending on large IT transformation projects amid an uncertain economic environment.
     URL: https://www.reuters.com/business/accenture-forecasts-quarterly-revenue-below-estimates-2026-03-19/

##### TAVILY INSIDER/SHORT/SCANDAL (5 hits)
[17] Tavily [Tue, 20 Ja]: GLASGOW, Scotland--(BUSINESS WIRE)-- ScottishPowe

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN_COUNCIL.md`)_

#### — · Story
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN_STORY.md` (cemetery archive)_

#### Accenture — ACN

##### Análise de Investimento · Modo FULL · Jurisdição US

*30 de Abril de 2026 · Framework STORYT_1 v5.0 · Camada 6 — Narrative Engine + Camada 5.5 Council*

---

> **Esta análise opera no Modo A-US sob a Jurisdição US.**

---

##### Quem analisou este ticker

- [[Charlie Compounder]] — _Industrials & Consumer US Specialist (Buffett frame)_
- [[Mariana Macro]] — _Chief Macro Strategist_
- [[Valentina Prudente]] — _Chief Risk Officer_
- [[Pedro Alocação]] — _Capital Allocator_

_Cada especialista escreveu uma review individual em `obsidian_vault/agents/<Nome>/reviews/ACN_2026-04-30.md`._

---

##### Camadas Silenciosas — Sumário de Execução

| Camada | Resultado |
|---|---|
| **1 — Data Ingestion** | yfinance (5 anos), brapi (preço), CVM, Tavily (5 hits) |
| **2 — Metric Engine** | Receita R$ 69.7 bi · EBITDA est. R$ 11.93 bi · FCF R$ 10.87 bi · ROE 25% · DGR 21.5% a.a. (DGR sem extraordinárias detectadas) |
| **3 — Feature Layer** | Normalização aproximada por mediana setorial (não peer ranking) |
| **4 — Scoring Engine** | Piotroski 5/9 · Altman Z=4.20 (safe) · Beneish M=-2.75 (clean) |
| **5 — Classification** | Modo A-US · Value (8/12) · Buffett/Quality (6/12) |
| **5.5 — Council Debate** | BUY (high) · 1 dissent · 1 pre-pub flags |


---

##### Ato 1 — A Identidade

Esta análise opera no Modo A-US sob a Jurisdição US. Accenture, uma empresa líder no setor tecnológico, é conhecida por fornecer consultoria e soluções em tecnologia para clientes globais. Com uma presença significativa em diversos mercados, a Accenture oferece serviços que vão desde estratégias de negócios até implementação de sistemas avançados de TI.

Recentemente, a empresa tem dado destaque ao desenvolvimento de soluções baseadas em inteligência artificial e robótica para melhorar eficiências operacionais. Por exemplo, a Accenture está piloteando o uso de robôs humanoidos em ambientes de armazém em colaboração com Vodafone Procure & Connect e SAP, demonstrando como a IA física pode aumentar a eficiência operacional e melhorar a segurança (Financial Times, 22 de abril de 2026). Além disso, a Accenture investiu na General Robotics para avançar em robótica física alimentada por IA no setor de manufatura e logística (Stock Titan, 15 de abril de 2026).

A empresa também está colaborando com Microsoft através da Avanade para desenvolver um sistema de inteligência agêntica que visa reduzir o tempo de inatividade em fábricas. Essas iniciativas refletem a estratégia da Accenture de se posicionar como uma líder na integração de tecnologia avançada, especialmente no campo da IA e robótica.

A armadilha típica que os investidores podem cair é confundir o alcance global e diversificado dos produtos e serviços oferecidos pela Accenture com a sua estratégia fundamental. A empresa não se limita apenas à venda de soluções tecnológicas, mas também oferece consultoria estratégica que ajuda seus clientes a transformar suas operações e modelos de negócios.

No cenário competitivo, a Accenture mantém uma posição sólida através da inovação contínua em tecnologia avançada e parcerias estratégicas. A empresa continua a adquirir empresas especializadas em IA e dados para fortalecer sua oferta de serviços, como a recente aquisição da Keepler, uma consultoria de dados e IA líder no mercado espanhol (Consultancy.eu, 15 de abril de 2026).

##### Ato 2 — O Contexto

O contexto macro atual é caracterizado por taxas de juros elevadas nos Estados Unidos, com a taxa do Federal Reserve entre 4.25% e 4.50%, enquanto o rendimento da dívida dos EUA a dez anos está em torno de 4.2%. O custo do capital próprio (Ke) é estimado em cerca de 10%. A economia está em um período de expansão tardia, com sinais emergentes de enfraquecimento.

Para o setor tecnológico e para a Accenture especificamente, essas condições macroeconômicas desafiam a sustentabilidade dos lucros. As taxas de juros elevadas podem pressionar os custos financeiros das empresas que dependem fortemente do capital externo, como é comum no setor tecnológico. Além disso, um ciclo econômico em declínio pode reduzir a demanda por serviços de consultoria e implementação de TI.

No entanto, a Accenture está bem posicionada para navegar nesse ambiente desafiador através da diversificação de suas ofertas e investimentos contínuos em tecnologias emergentes. A empresa continua a expandir sua presença no campo da IA e robótica, o que pode oferecer oportunidades de crescimento mesmo em um cenário econômico mais cauteloso.

Além disso, qualquer mudança regulatória ou estrutural que possa afetar diretamente o setor tecnológico será monitorada pela Accenture. A empresa tem demonstrado uma capacidade sólida de adaptação e inovação, mantendo-se relevante em um mercado altamente competitivo e em constante evolução.

---

##### Ato 3 — A Evolução Financeira

A evolução financeira da empresa ao longo dos últimos anos revela um crescimento sustentado e uma gestão sólida de recursos. As métricas financeiras anuais são apresentadas na tabela abaixo, destacando a progressão das receitas, margens operacionais, lucros líquidos e fluxos de caixa livre.

| Exercício | Receita | EBIT | EBITDA est. | Margem EBITDA | Lucro Líquido | Margem Líquida | FCF |
|---|---|---|---|---|---|---|---|
| 2021 | — | — | — | — | — | — | — |
| 2022 | R$ 61.59B | R$ 9.37B | R$ 10.30B | 16.7% | R$ 6.88B | 11.2% | R$ 8.82B |
| 2023 | R$ 64.11B | R$ 9.87B | R$ 10.86B | 16.9% | R$ 6.87B | 10.7% | R$ 9.00B |
| 2024 | R$ 64.90B | R$ 10.03B | R$ 11.04B | 17.0% | R$ 7.26B | 11.2% | R$ 8.61B |
| 2025 | R$ 69.67B | R$ 10.84B | R$ 11.93B | 17.1% | R$ 7.68B | 11.0% | R$ 10.87B |

A receita da empresa cresceu a uma taxa composta anual (CAGR) de aproximadamente 4,5%, passando de R$ 61,59 bilhões em 2022 para R$ 69,67 bilhões no exercício mais recente. Esta expansão é acompanhada por um aumento consistente na margem EBITDA, que subiu de 16,7% em 2022 para 17,1% em 2025, refletindo uma eficiência operacional crescente.

O lucro líquido da empresa também registrou ganhos consistentes ao longo do período, embora com variações menores comparativamente às receitas e EBITDA. O fluxo de caixa livre (FCF) apresentou um comportamento robusto, atingindo R$ 10,87 bilhões em 2025, indicando uma geração consistente de recursos líquidos após os investimentos necessários.

A tabela abaixo ilustra a evolução dos dividendos pagos pela empresa ao longo do período:

| Ano | Total proventos (R$/ação) |
|---|---|
| 2020 | 1.680 |
| 2021 | 3.610 |
| 2022 | 4.030 |
| 2023 | 4.650 |
| 2024 | 5.350 |
| 2025 | 4.440 |
| 2026 | 1.630 |

O Dividend Growth Rate (DGR) calculado, limpo de extraordinárias, é de 21,5% ao ano. Este crescimento sustentado nos dividendos sugere uma política robusta e consistente de distribuição de lucros aos acionistas, o que pode ser atraente para investidores interessados em estratégias DRIP (Dividend Reinvestment Plan). No entanto, é importante notar que há um declínio no total proventos reportado em 2026, potencialmente indicando uma redução temporária nos dividendos.

Lucro contábil pode esconder provisões e ajustes; FCF, não. A consistência do fluxo de caixa livre ao longo dos anos é um indicador mais confiável da saúde financeira da empresa em comparação com o lucro líquido, que pode ser afetado por diversos fatores contábeis.

##### Ato 4 — O Balanço

O balanço financeiro da empresa oferece uma visão detalhada de sua situação econômica e financeira. As métricas-chave incluem:

- **P/E (Price-to-Earnings Ratio)**: 14,65
- **P/B (Price-to-Book Ratio)**: 3,52
- **DY (Dividend Yield)**: 1,74%
- **ROE (Return on Equity)**: 24,76%

O Net Debt da empresa é estimado em R$ 4,09 bilhões, calculado como metade do total de dívida. A relação entre o Net Debt e o EBITDA mais recente é de -0,08 (Net Debt/EBITDA), indicando uma posição financeira sólida com baixo nível de alavancagem.

O ROE da empresa está em 24,76%, superando significativamente o custo do capital próprio no Brasil estimado em cerca de 18,25% (Selic 13,75% + prêmio de risco equity de 4,5%). Este resultado sugere que a empresa está criando valor para seus acionistas.

A relação entre dividendos e lucros líquidos é consistente ao longo do tempo, com um histórico de pagamentos sem interrupções. A política de dividendos da empresa tem sido robusta e sustentável, apesar das flutuações anuais que podem ser atribuídas a fatores específicos.

Em termos de estrutura de capital, o Current Ratio (relação entre ativos circulantes e passivos circulantes) é um indicador chave da liquidez imediata. Embora os dados específicos não estejam disponíveis para calcular o Current Ratio diretamente, a consistência no fluxo de caixa livre e a baixa alavancagem sugerem uma posição financeira sólida.

Não foram identificados sinais claros de despesas financeiras crescentes ou aumento na alavancagem que possam representar pontos de atenção significativos para o investidor.

---

##### Ato 5 — Os Múltiplos

A análise dos múltiplos financeiros da empresa revela uma posição relativamente sólida em comparação com o setor e os índices de referência. As métricas fundamentais, como Price-to-Earnings (P/E), Price-to-Book (P/B) e Dividend Yield (DY), são essenciais para entender a valoração da empresa no mercado.

| Múltiplo | ACN | Mediana setorial | Índice (Ibov/S&P) |
|---|---|---|---|
| P/E | 14.65x | 25.55x | 21.00x |
| P/B | 3.52x | 7.75x | 3.50x |
| DY | 1.7% | 0.9% | 1.5% |
| FCF Yield | 9.9% | 2.5% | 4.0% |
| ROE | 24.8% | 34.4% | 16.0% |
| ND/EBITDA | -0.08x | 0.15x | — |

O múltiplo P/E de 14,65 vezes coloca a empresa em um patamar substancialmente mais baixo do que a mediana setorial de 25,55 vezes e também inferior ao índice referencial de 21,00 vezes. Este indicador sugere uma valoração relativamente acessível, considerando o desempenho operacional da empresa.

O P/B de 3,52 vezes é ligeiramente superior à média do setor (7,75x) e ao índice (3,50x), mas ainda assim indica um nível de valoração moderado. Este múltiplo reflete a relação entre o preço das ações e os ativos líquidos da empresa, sugerindo que os investidores estão dispostos a pagar mais do que o valor contábil dos ativos.

O DY de 1,7% é significativamente superior à média setorial (0,9%) e ao índice (1,5%), evidenciando um atrativo retorno para investidores em busca de renda. No entanto, é importante notar que o DY reportado pode incluir dividendos extraordinários ou outros fatores não recorrentes.

O FCF Yield de 9,9% supera significativamente a média setorial (2,5%) e o índice (4,0%), indicando uma geração robusta de caixa livre em relação ao valor da empresa. Este indicador sugere que a empresa está gerando lucros líquidos suficientes para financiar seus próprios projetos sem necessidade de captação externa.

O ROE de 24,8% é inferior à mediana setorial (34,4%) e ao índice (16,0%), mas ainda assim representa um desempenho sólido. Este indicador reflete a eficiência da empresa em gerar lucros utilizando os recursos disponíveis.

Por fim, o ND/EBITDA de -0,08x é ligeiramente negativo, contrastando com a média setorial (0,15x), mas não indica necessariamente um problema grave. Este indicador mede a capacidade da empresa em gerar lucros antes dos juros e amortizações.

##### Ato 6 — Os Quality Scores

Os scores de qualidade financeira fornecem uma visão complementar sobre o desempenho operacional e financeiro da empresa, além de ajudar na avaliação do risco associado ao investimento. O Piotroski F-Score de 5/9 indica um bom desempenho em termos de saúde financeira, com cinco critérios aprovados que incluem o crescimento contínuo dos lucros e a geração consistente de caixa livre.

O Altman Z-Score de 4,20 coloca a empresa na zona segura, indicando um baixo risco de insolvência. O score conservador é também considerado alto, reforçando a solidez financeira da empresa.

Por fim, o Beneish M-Score de -2,75 indica uma zona limpa e alta confiança, sugerindo que não há evidências significativas de manipulação contábil. Este score ajuda os investidores a identificar potenciais fraudes ou práticas contábeis questionáveis.

Estas métricas juntas fornecem um quadro robusto sobre o desempenho financeiro e operacional da empresa, destacando tanto suas forças como seus pontos fracos.

---

##### Ato 7 — O Moat e a Gestão

A Accenture mantém um moat robusto em sua posição no mercado de consultoria e serviços de tecnologia, classificado como Wide. Este moat é sustentado por uma combinação de fatores que incluem custos de escala, intangíveis e eficiência operacional.

Primeiramente, a Accenture beneficia-se da economia de escala em sua estrutura organizacional, permitindo-lhe oferecer soluções tecnológicas e consultoria a preços competitivos. A empresa tem investido significativamente em pesquisa e desenvolvimento para manter seu portfólio de serviços atualizado e relevante no mercado, o que fortalece ainda mais sua posição.

Em segundo lugar, os intangíveis da Accenture, incluindo sua reputação sólida e a vasta experiência acumulada ao longo dos anos, são fatores cruciais em seu moat. A empresa é conhecida por suas capacidades de inovação e implementação de tecnologias avançadas, como inteligência artificial e robótica, que estão sendo demonstradas através de parcerias com empresas líderes no setor.

A Accenture também beneficia-se de um forte componente de eficiência operacional. A empresa tem se destacado em sua capacidade de otimizar processos internos e oferecer soluções personalizadas para clientes, o que a coloca à frente da concorrência. As recentes iniciativas no campo da robótica e automação industrial, como a colaboração com General Robotics e Avanade para desenvolver sistemas inteligentes de fábricas, ilustram sua abordagem eficiente em resolver problemas complexos do mercado.

No que diz respeito à gestão, a Accenture tem demonstrado uma capacidade notável de adaptar-se às mudanças tecnológicas e mercadológicas. A empresa continua a investir em inovação e desenvolvimento de produtos, como visto na recente parceria com Anthropic para criar soluções avançadas de segurança cibernética.

Dado não disponível sobre insider ownership ou insider trades nos últimos seis meses.

##### Ato 8 — O Veredito

###### Perfil Filosófico
O perfil filosófico da Accenture é predominantemente de valor, com uma pontuação de Value (8/12) e Buffett/Quality (6/12). As pontuações específicas incluem:

- **Value**: +2 · P/E 14.6 < mediana setorial 18; +2 · FCF Yield 9.9% > 6%; +2 · ROE 25% > Ke (18.2%); +2 · DCF margin of safety 101% > 25%
- **Growth**: +2 · Margem EBIT em expansão; +1 · Yield baixo (<3%) + ROE alto → reinvestimento alto
- **Dividend**: +2 · Histórico ininterrupto de 22 anos ≥ 5; +2 · FCF > Lucro líquido — payout cobertura forte
- **Buffett**: +2 · ROE 25% > 15%; +1 · ND/EBITDA -0.08 < 2x; +1 · Beneish M=-2.75 clean (sem manipulação); +1 · DCF MoS 101% > 20%

###### O que o preço desconta
O atual preço da Accenture, R$ 178.71, já incorpora uma visão otimista sobre a empresa's capacidade de continuar inovando e expand

_… (truncated at 15k chars — full content in `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\ACN_STORY.md`)_

#### — · DRIP scenarios
_source: `cemetery\2026-05-14\ABSORBED-drip\briefings\drip_scenarios\ACN_drip.md` (cemetery archive)_

/============================================================================\
|   DRIP SCENARIO — ACN             moeda USD      data 26/04/2026           |
\============================================================================/

  POSICAO
  ------------------------------------------------------------
  Shares..............:              4
  Entry price.........: US$      213.71
  Cost basis..........: US$      920.03
  Price now...........: US$      178.36
  Market value now....: US$      767.85  [-16.5% nao-realizado]
  DY t12m.............: 1.74%  (R$/US$ 3.1100/share)
  DY vs own 10y.......: P71 [fair-cheap]  (actual 1.74% em 121 obs mensais) — entry-timing, NAO stock-picker

  kind=equity  streak=22  hist_g_5y=0.053  hist_g_raw=0.053  gordon_g=0.185  is_quality=True  capped=False

  ASSUMPTIONS POR CENARIO
  --------------------------------------------------------------------------
  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |
  --------------------------------------------------------------------------
  | conservador  |   +7.13%  |   -1.00% |   +7.87%       |
  | base         |  +11.88%  |   +0.00% |  +13.62%       |
  | optimista    |  +16.04%  |   +1.00% |  +18.78%       |
  --------------------------------------------------------------------------

  PAYBACK MILESTONES (anos)
  --------------------------------------------------------------------------
  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |
  --------------------------------------------------------------------------
  | conservador  |     25       |       34       |       12       |
  | base         |     19       |      >40       |        7       |
  | optimista    |     16       |      >40       |        6       |
  --------------------------------------------------------------------------

  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis
  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0
  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis

  PROJECCAO DRIP — valor final de mercado por horizonte
  --------------------------------------------------------------------------
  | HORZ  | conservador  | base         | optimista    |
  --------------------------------------------------------------------------
  |   5y  | US$      1,130 | US$      1,468 | US$      1,834 |
  |  10y  | US$      1,670 | US$      2,805 | US$      4,367 |
  |  15y  | US$      2,478 | US$      5,360 | US$     10,362 |
  --------------------------------------------------------------------------

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ACN.md` (cemetery archive)_

#### ACN — Accenture

#holding #us #technology #consulting #turnaround #watch

##### 🎯 Verdict — 🟡 WATCH

> **Score**: 6.9/10  |  **Confiança**: 80%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 8.7/10 | 35% | `█████████░` |
| Valuation  | 8.0/10 | 30% | `████████░░` |
| Momentum   | 2.0/10 | 20% | `██░░░░░░░░` |
| Narrativa  | 7.0/10 | 15% | `███████░░░` |

###### Detalhes

- **Quality**: Altman Z 4.204971537327859 (SAFE), Piotroski 5/9 (NEUTRAL), DivSafety 95.0/100
- **Valuation**: Screen 0.60, DY percentil P77 (CHEAP)
- **Momentum**: 1d -2.48%, 30d -6.16%, YTD -32.84%
- **Narrativa**: user_note=True, YT insights 60d=0

###### Razões

- valuation atractiva mas quality ou momentum fraco
- quality forte
- valuation barato
- DY percentil P77 (historicamente CHEAP)

##### Links

- Sector: [[sectors/Technology|Technology]]
- Market: [[markets/US|US]]
- Peers: [[AAPL]] · [[PLTR]] · [[TSM]] · [[IBM]] · [[JKHY]]
- 🎯 **Thesis**: [[wiki/holdings/ACN|thesis deep]]

##### Snapshot

- **Preço**: $174.57  (2026-05-06)    _-2.48% 1d_
- **Screen**: 0.6  ✗ fail
- **Altman Z**: 4.205 (safe)
- **Piotroski**: 5/9
- **Div Safety**: 95.0/100 (SAFE)
- **Posição**: 4.30506 sh @ $213.70666146348714  →  P&L -18.31%

##### Fundamentals

- P/E: 14.2972975 | P/B: 3.4389899 | DY: 1.78%
- ROE: 24.76% | EPS: 12.21 | BVPS: 50.762
- Streak div: 22y | Aristocrat: False

##### Tese / Notas do investidor

###### 2026-04-23
Compra inicial Mai/2024 @ $299.83 — tese consulting turnaround. -41% em Abr/2026 após Q2 miss e downtrend. Sistema diz HOLD (no distress, decel Piotroski). Buy-zone $150-170.

##### Dividendos recentes

- 2026-04-09: $1.6300
- 2025-07-10: $1.4800
- 2025-04-10: $1.4800
- 2025-01-16: $1.4800
- 2024-10-10: $1.4800

##### Eventos (SEC/CVM)

- **2026-04-24** `8-K` — 8-K | 1.01,1.02,2.03,9.01
- **2026-03-19** `8-K` — 8-K | 2.02,9.01
- **2026-03-19** `10-Q` — 10-Q
- **2026-01-28** `8-K` — 8-K | 5.02,5.07,9.01
- **2025-12-18** `8-K` — 8-K | 2.02,9.01

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -45.99%
- **Drawdown 5y**: -57.98%
- **YTD**: -32.84%
- **YoY (1y)**: -42.54%
- **CAGR 3y**: -13.06%  |  **5y**: -9.75%  |  **10y**: +4.21%
- **Vol annual**: +34.14%
- **Sharpe 3y** (rf=4%): -0.62

###### Dividendos
- **DY 5y avg**: +1.38%
- **Div CAGR 5y**: +5.31%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a

##### 💰 Financials trend (annual)

| Period | Revenue | Net Income | Free Cash Flow |
|---|---|---|---|
| 2021-08-31 | n/a | n/a | n/a |
| 2022-08-31 | $61.59B | $6.88B | $8.82B |
| 2023-08-31 | $64.11B | $6.87B | $9.00B |
| 2024-08-31 | $64.90B | $7.26B | $8.61B |
| 2025-08-31 | $69.67B | $7.68B | $10.87B |

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "ACN — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-27', '2025-06-02', '2025-06-06', '2025-06-12', '2025-06-18', '2025-06-25', '2025-07-01', '2025-07-08', '2025-07-14', '2025-07-18', '2025-07-24', '2025-07-30', '2025-08-05', '2025-08-11', '2025-08-15', '2025-08-21', '2025-08-27', '2025-09-03', '2025-09-09', '2025-09-15', '2025-09-19', '2025-09-25', '2025-10-01', '2025-10-07', '2025-10-13', '2025-10-17', '2025-10-23', '2025-10-29', '2025-11-04', '2025-11-10', '2025-11-14', '2025-11-20', '2025-11-26', '2025-12-03', '2025-12-09', '2025-12-15', '2025-12-19', '2025-12-26', '2026-01-02', '2026-01-08', '2026-01-14', '2026-01-21', '2026-01-27', '2026-02-02', '2026-02-06', '2026-02-12', '2026-02-19', '2026-02-25', '2026-03-03', '2026-03-09', '2026-03-13', '2026-03-19', '2026-03-25', '2026-03-31', '2026-04-07', '2026-04-13', '2026-04-17', '2026-04-23', '2026-04-28', '2026-05-04']
series:
  - title: ACN
    data: [308.88, 320.41, 320.18, 315.43, 314.47, 317.65, 318.13, 306.38, 294.6, 302.62, 303.33, 279.99, 282.44, 281.71, 274.0, 247.07, 238.61, 247.01, 253.99, 257.12, 254.15, 251.99, 237.87, 239.7, 232.56, 243.71, 251.23, 243.56, 238.39, 249.81, 247.75, 242.9, 244.55, 245.21, 240.79, 247.85, 272.85, 269.53, 274.66, 272.25, 271.09, 259.95, 281.82, 288.54, 280.72, 275.8, 266.79, 240.62, 222.05, 214.95, 191.5, 209.89, 209.36, 196.65, 203.55, 192.29, 198.29, 197.3, 191.95, 197.65, 178.28, 177.75, 180.12]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 📊 Fundamentals trend

```chart
type: line
title: "P/E over time"
labels: ['2026-04-15', '2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: P/E
    data: [15.909837, 15.878279, 15.90164, 16.200819, 16.02541, 15.949139, 14.631666, 14.619673, 14.619673, 14.505738, 14.581625, 14.787531, 14.648361, 14.776046, 14.684988, 14.2972975]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

```chart
type: line
title: "ROE & DY %"
labels: ['2026-04-15', '2026-04-16', '2026-04-17', '2026-04-19', '2026-04-20', '2026-04-21', '2026-04-24', '2026-04-25', '2026-04-26', '2026-04-27', '2026-04-28', '2026-04-29', '2026-04-30', '2026-05-04', '2026-05-05', '2026-05-06']
series:
  - title: ROE %
    data: [24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76, 24.76]
  - title: DY %
    data: [3.42, 3.36, 3.36, 3.3, 3.3, 1.6, 1.74, 1.74, 1.74, 1.76, 1.75, 1.73, 1.74, 1.73, 1.74, 1.78]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · Deepdive (DOSSIE)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ACN_DOSSIE.md` (cemetery archive)_

#### 📑 ACN — Accenture

> Generated **2026-04-26** by `ii dossier ACN`. Cross-links: [[ACN]] · [[ACN_IC_DEBATE]] · [[CONSTITUTION]]

##### TL;DR

ACN cota P/E 14.62, DY 1.74%, ROE 24.76% e streak div 22y — consultora global #1 em digital + AI implementation. IC verdict **BUY** (high confidence, 80% consensus); YoY -39.2% após drawdown 2024 oferece margem de segurança raras vezes vista. Conviction score 87 (top do US book): tese AI consult ramp + buybacks + ROE >24% intacta — best-in-class compounder, manter como growth/quality pick (DY abaixo do screen US 2.5% por isso não scorecard DRIP puro).

##### 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 12.20  |  **BVPS**: 50.76
- **ROE**: 24.76%  |  **P/E**: 14.62  |  **P/B**: 3.51
- **DY**: 1.74%  |  **Streak div**: 22y  |  **Market cap**: USD 109.77B
- **Last price**: USD 178.36 (2026-04-26)  |  **YoY**: -39.2%

##### 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[ACN_IC_DEBATE]]

##### 3. Thesis

**Core thesis (2026-04-24)**: ACN é consultoria global #1 em digital
transformation + AI implementation. Posição única — as empresas Fortune 500
não têm talent in-house para GenAI rollouts; ACN captura spend
incremental sustentável 5-10 anos. ROE 25%+, dividend streak 20y, buybacks
consistentes. Valuation actual oferece margem de segurança após 2024 drawdown.

**Key assumptions**:
1. AI implementation spend continua crescendo (15-20% YoY para top-tier consultoria)
2. ACN mantém margin > 15% apesar de pricing pressure em serviços legacy
3. Talent retention estável (people business — churn é existential)
4. US + EU government/healthcare verticals não cortam consulting budgets

**Disconfirmation triggers**:
- Revenue growth < 5% em 2 quarters (sinal secular decline consulting)
- Margins cap <

→ Vault: [[ACN]]

##### Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 14.62** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 14.62** passa.
- **P/B = 3.51** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **3.51** esticado.
- **DY = 1.74%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **1.74%** fraco; verificar se é growth pick.
- **ROE = 24.76%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **24.76%** compounder-grade.
- **Graham Number ≈ R$ 118.04** vs preço **R$ 178.36** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 22y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

###### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

##### 4. Riscos identificados

- 🔴 **GenAI substitution risk** — paradoxo: ACN vende AI mas serviços legacy (testing, RPA) podem ser comoditizados pelos próprios LLMs. Trigger: revenue growth segments legacy YoY < 0% por 2 quarters.
- 🟡 **Pricing pressure consulting** — clients enterprise a renegociar contratos pós-2024 pull-back; margem sob pressão. Trigger: operating margin < 14.5% por 2 trimestres consecutivos.
- 🟡 **FY26 guidance miss** — guidance revenue 5-7% FY26 ainda abaixo do hist 8-10%; downgrades possíveis. Trigger: bookings YoY < 5% ou guidance cut em 8-K.
- 🟢 **Talent retention** — people business onde churn é existential; estável até agora. Trigger: turnover voluntário > 18% (10-K disclosure).

##### 5. Position sizing

**Status atual**: holding (in portfolio)

**BUY com bias de aumento** — IC BUY (80% consensus), conviction 87 (top US book), valuation pós-drawdown -39.2% YoY oferece margem de segurança rara. USD permanece em US (isolation rule); growth/quality pick (não DRIP puro com DY 1.74%). Sizing até 7-9% do US book justificado pela conviction; adds escalonados em pull-backs P/E < 14 ou se FY26 guidance for confirmado intacto.

##### 6. Tracking triggers (auto-monitoring)

- Revenue growth < 5% por 2 trimestres → secular decline consulting (disconfirmation trigger da thesis).
- Operating margin < 14.5% por 2 trimestres → pricing pressure a materializar.
- Bookings YoY < 5% → pipeline a quebrar antes da revenue.
- `fundamentals.roe < 20%` → quality compounder a degradar.
- `conviction_scores.score < 70` (currently 87) → IC BUY a perder force.

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
*Generated by `ii dossier ACN` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ACN_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — ACN

**Committee verdict**: **BUY** (high confidence, 80% consensus)  
**Votes**: BUY=4 | HOLD=1 | AVOID=0  
**Avg conviction majority**: 7.8/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🟢 Warren Buffett — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Excelente negócio em consultoria digital e AI
- ROE alto e consistente, margem de segurança
- Dividendos e recompras consistentes

**Key risk**: Perda de talento chave pode afetar competitividade

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- Líder em digital transformation
- ROE alto e crescimento sustentável
- Inovação contínua com investimentos em AI

**Key risk**: Desaceleração súbita na demanda por serviços de consultoria

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- Posição única no mercado de consultoria em transformação digital
- ROE alto e histórico de dividendos
- Investimentos em AI demonstram antecipação

**Key risk**: Pressão nos preços dos serviços legados pode comprometer margens

###### 🟢 Seth Klarman — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Strong ROE, consistent dividend, and buybacks.
- Unique position in AI implementation for Fortune 500 companies.
- Recent investments and pilots showcase leadership.

**Key risk**: Talent retention issues could severely impact consulting capabilities

###### 🟢 Ray Dalio — **BUY** (conv 8/10, size: medium)

**Rationale**:
- Liderança em digital transformation
- Margens robustas e crescimento sustentável
- Inovações contínuas em AI

**Key risk**: Desaceleração significativa no gasto de consultoria por Fortune 500

##### 📊 Context provided

```
TICKER: US:ACN

FUNDAMENTALS LATEST:
  pe: 14.788525
  pb: 3.5542333
  dy: 1.72%
  roe: 24.76%
  net_debt_ebitda: -0.08309405074235562
  intangible_pct_assets: 38.1%   (goodwill $22.5B + intangibles $2.4B)

THESIS HEALTH: score=91/100  contradictions=1  risk_flags=1  regime_shift=0

VAULT THESIS:
**Core thesis (2026-04-24)**: ACN é consultoria global #1 em digital
transformation + AI implementation. Posição única — as empresas Fortune 500
não têm talent in-house para GenAI rollouts; ACN captura spend
incremental sustentável 5-10 anos. ROE 25%+, dividend streak 20y, buybacks
consistentes. Valuation actual oferece margem de segurança após 2024 drawdown.

**Key assumptions**:
1. AI implementation spend continua crescendo (15-20% YoY para top-tier consultoria)
2. ACN mantém margin > 15% apesar de pricing pressure em serviços legacy
3. Talent retention estável (people business — churn é existential)
4. US + EU government/healthcare verticals não cortam consulting budgets

**Disconfirmation triggers**:
- Revenue growth < 5% em 2 quarters (sinal secular decline consulting)
- Margins cap <

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations - Financial Times [Wed, 22 Ap]
    ### Accenture, Vodafone Procure & Connect and SAP Pilot Humanoid Robotics in Warehouse Operations. HANNOVER, Germany--(BUSINESS WIRE)--Apr. 22, 2026-- Accenture (NYSE: ACN), together with Vodafone Pro
  - Accenture to roll out Copilot to all 743,000 employees - iTnews [Mon, 27 Ap]
    ## Accenture to roll out Copilot to all 743,000 employees ## OpenAI breaks off Microsoft exclusivity ## 'Firestarter' malware survives Cisco firewall patches ## Modernising legacy at speed ## US judge
  - Accenture Copilot Rollout: A Massive Leap but Workforce Concerns - Techgenyz [Mon, 04 Ma]
    Accenture has announced one of the largest enterprise AI deployments to date, rolling out Microsoft Copilot to its global workforce of ove
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

#### — · Variant perception
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\ACN_VARIANT.md` (cemetery archive)_

#### 🎯 Variant Perception — ACN

**Our stance**: neutral  
**Analyst consensus** (0 insights, last 90d): no_data (0% bull)  
**Variance type**: `missing_upside` (magnitude 2/5)  
**Interpretation**: we lack conviction; market does

##### 🌐 Tavily web consensus (last 30d)

**Web stance**: bullish (3 bull / 1 bear / 1 neutral)  
**Cached**: True

- 🟡 [neutral] [Texas Instruments upgraded, Avis downgraded: Wall Street's top analyst calls - Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/texas-instruments-upgraded-avis-downgraded-134410993.html) (Thu, 23 Ap)
- 🟢 [bull] [TSMC Q1 Revenue Surges 35% — Is TSM Stock Still a Buy Ahead of Earnings? - TipRanks](https://www.tipranks.com/news/tsmc-q1-revenue-surges-35-is-tsm-stock-still-a-buy-ahead-of-earnings) (Fri, 10 Ap)
- 🔴 [bear] [Comcast Stock (CMCSA) Drops on Post Q1 Analyst Updates - TipRanks](https://www.tipranks.com/news/cmcsa-analysts) (Sat, 25 Ap)
- 🟢 [bull] [Here are Thursday's biggest analyst calls: Nvidia, Tesla, Berkshire Hathaway, Amazon, Texas Instruments & more - CNBC](https://www.cnbc.com/2026/04/23/thursday-analyst-calls-with-stocks-like-nvidia.html) (Thu, 23 Ap)
- 🟢 [bull] [AMD Stock Soars on Strong Q1 Beat; Goldman Sachs, Bernstein Upgrade to Buy on AI Chips Demand - TipRanks](https://www.tipranks.com/news/amd-stock-soars-on-q1-beat-solid-outlook-goldman-sachs-and-bernstein-upgrade-to-buy-on-ai-demand) (Wed, 06 Ma)

##### 📜 Our thesis

**Core thesis (2026-04-24)**: ACN é consultoria global #1 em digital
transformation + AI implementation. Posição única — as empresas Fortune 500
não têm talent in-house para GenAI rollouts; ACN captura spend
incremental sustentável 5-10 anos. ROE 25%+, dividend streak 20y, buybacks
consistentes. Valuation actual oferece margem de segurança após 2024 drawdown.

**Key assumptions**:
1. AI implementation spend continua crescendo (15-20% YoY para top-tier consultoria)
2. ACN mantém margin > 15% apesar de pricing pressure em serviços legacy
3. Talent retention estável (people business — churn é existential)
4. US + EU government/healthcare verticals não cortam consulting budgets

**Disconfirmation triggers**:
- Revenue growth < 5% em 2 quarters (sinal secular decline consulting)
- Margins cap <

---
*100% Ollama local. Variant perception scan.*

#### — · Wiki playbook
_source: `cemetery\2026-05-14\ABSORBED-wiki-holdings\wiki\holdings\ACN.md` (cemetery archive)_

#### 🎯 Thesis: [[ACN]] — Accenture

> #1 global consulting + IT services. AI transformation play + managed services recurring revenue. Quality compounder.

##### Intent
**Compounder** — growth primary, DY bonus (~2%). Not DRIP pure.

##### Business snapshot
- **Strategy + consulting** (~25% mix, premium margin)
- **Technology implementation** (~35% mix, SAP, Oracle, Salesforce, Microsoft ecosystems)
- **Managed services / outsourcing** (~40% mix — recurring sticky revenue)

Revenue $65B+/y. 730K+ employees across 120+ countries.

##### Por que detemos

1. **Mix shift** — managed services % rising = recurring revenue stability.
2. **AI bookings momentum** — $3B+ cumulative AI-related deals (2024-26).
3. **ROIC 27%+** — best-in-class consulting.
4. **Dividend growth** 15+ years (aristocrat-track, not yet aristocrat).
5. **Fortress balance sheet** — minimal debt.
6. **Global + scale** — can serve any Fortune 500 globally.

##### Moat

- **Brand** — ACN = tier-1 consulting brand alongside Deloitte/McKinsey.
- **Scale + ecosystem certifications** — Salesforce MVP, SAP S/4HANA leader, Microsoft partner elite.
- **Talent pipeline** — 40K+ new hires/y, training machine.
- **Relationship depth** — Fortune 500 clients often multi-decade.
- **Weak moat sobre GenAI cannibalization** — clients may DIY more with LLMs. Partially offset by AI transformation services.

##### Current state (2026-04)

- AI bookings growing strongly (enterprise AI transformation).
- Classic dev/implementation under pressure (GenAI productivity gain reducing hours).
- EUR exposure headwind (~25% revenue EUR).
- Strategy bookings soft 2023-24 discretionary spending cut.
- Managed services growth compensating — mix shift beneficial.
- Employee attrition normalised 12-14% (vs pandemic 20%+).

##### Invalidation triggers

- [ ] ROIC < 18% sustained (quality deterioration)
- [ ] Bookings < revenue TTM 3+ quarters (shrink coming)
- [ ] AI cannibalization confirmed: revenue decline 2 years consecutive
- [ ] Attrition > 20% sustained (talent pipeline breaks)
- [ ] Operating margin < 12% (industry norm 14-15%)
- [ ] Major client concentration breach (> 10% single client)
- [ ] CEO Julie Sweet departure + strategy pivot

##### Sizing

- Posição actual: 4.3 shares (fractional from DRIP)
- Target 3-5% sleeve US
- **Compounder** — no trim salvo valuation extremo (P/E > 35×)
- Reinvest dividends DRIP

##### Consulting peer comparison

| Ticker | Margin | ROIC | Growth | Mix |
|---|---|---|---|---|
| **ACN** | 14-15% | 27% | 6-10% | Strategy + impl + managed |
| IBM | 10-12% | 10% | 0-3% | Hybrid cloud + consulting |
| TCS | 25% | 35% | 5-8% | Offshore-heavy implementation |
| INFY | 20% | 30% | 5-9% | Offshore digital |
| CTSH | 14% | 18% | 2-6% | Healthcare-heavy |
| EPAM | 15% | 20% | Volatile (-5 to +15%) | Eastern European engineering |

ACN premium vs TCS/INFY justified by: Fortune 500 strategy access + global labor mix + breadth.


<!-- LIVE_SNAPSHOT:BEGIN -->
_Atualizado: 2026-04-24 14:07_

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -44.83%
- **Drawdown 5y**: -57.08%
- **YTD**: -31.41%
- **YoY (1y)**: -38.12%
- **CAGR 3y**: -13.68%  |  **5y**: -9.38%  |  **10y**: +4.57%
- **Vol annual**: +35.34%
- **Sharpe 3y** (rf=4%): -0.63

###### Dividendos
- **DY 5y avg**: +1.38%
- **Div CAGR 5y**: +5.31%
- **Frequency**: quarterly
- **Streak** (sem cortes): 0 years

###### Valuation
- **P/E vs own avg**: n/a
<!-- LIVE_SNAPSHOT:END -->

##### Related

- [[Consulting_IT_Services]] — canonical sector deep-dive
- [[Buffett_quality]] — ACN é post-2000 quality compounder
- [[ROIC_interpretation]] — why 27% ROIC é extraordinário
- [[TSM]] — tech exposure differently positioned (semis vs services)

##### Memory refs

- `user_investment_intents.md` — ACN é Compounder; não DRIP primary

## ⚙️ Refresh commands

```bash
ii panorama ACN --write
ii deepdive ACN --save-obsidian
ii verdict ACN --narrate --write
ii fv ACN
python -m analytics.fair_value_forward --ticker ACN
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
