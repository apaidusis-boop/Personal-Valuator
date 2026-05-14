---
type: ticker_hub
ticker: KNHF11
market: br
sector: Híbrido
currency: BRL
bucket: watchlist
is_holding: false
generated: 2026-05-14
sources_merged: 4
tags: [hub, ticker, merged]
parent: "[[_TICKERS_INDEX]]"
---

# KNHF11 — Kinea Hedge Fund FII

> **Hub mergeado**. Todo o conteúdo per-ticker do vault foi absorvido aqui (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews por persona, sessions). Ficheiros-fonte estão no `cemetery/2026-05-14/`.

`sector: Híbrido` · `market: BR` · `currency: BRL` · `bucket: watchlist` · `4 sources merged`

## 🎯 Hoje

- **Posição**: 175.0 @ entry 98.56
- **Verdict (DB)**: `SKIP` (score 5.1, 2026-05-13)
- **Fundamentals** (2026-05-13): P/E 7.52 · DY 11.5% · Dividend streak 4

## 📜 Histórico (conteúdo absorvido, ordem cronológica desc)

> Todas as fontes consolidadas (vault + JSON deepdives). Cada bloco mantém o título original e foi rebaixado 3 níveis (h1→h4) para encaixar.


### 2026

#### 2026-05-13 · Overnight scrape
_source: `cemetery\2026-05-14\ABSORBED-overnight-per-ticker\Overnight_2026-05-13\KNHF11.md` (cemetery archive)_

#### KNHF11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Híbrido
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/knhf11/
- **Pilot rationale**: fii_heuristic (watchlist)

##### Antes (estado da DB)

**Posição activa**: qty=175.0 · entry=98.56 · date=2026-05-08

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **2**
- Última cotação DB: 2026-05-11 → close=97.25
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.11311053984575835 · P/E=7.6214733
- Score (último run): score=0.8 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

_(zero events em DB)_

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


### (undated)

#### — · Migration / transition
_source: `cemetery\2026-05-14\ABSORBED-dossiers\dossiers\RBRX11_vs_KNHF11_MIGRATION.md` (cemetery archive)_

#### RBRX11 (Pátria) → KNHF11 (Kinea) — migração EXECUTADA

**Status**: ✅ **EXECUTADA** — 2026-05-08 10h48 (full swap, não faseado)
**Decisão do user**: full migration em vez do faseamento 50/50 que eu havia recomendado
**Confiança ex-ante**: média (LEAN MIGRATE) — registado para retrospectiva

##### Execução real (broker print)

| | Operação | Preço | Qty | Total |
|---|---|---|---|---|
| RBRX11 | **Venda** | R$ 8.70 | 2,000 | R$ 17,400.40 |
| KNHF11 | **Compra** | R$ 98.56 | 175 | R$ 17,247.62 |
| **Cash residual** | | | | **R$ 152.78** (pre-IR) |

###### Realized P&L RBRX11 (após 2026-04-24 entry @ R$8.48)

- Cost basis: R$ 16,960.00 (2,000 × R$8.48)
- Proceeds:   R$ 17,400.00 (2,000 × R$8.70)
- Gross gain: **+R$ 440.00**
- IR FII 20%: R$ 88.00 (devida — FII tributa ganho de capital a 20%)
- **Net gain: +R$ 352.00**
- Cash net (após IR): R$ 152.78 − R$ 88.00 = **R$ 64.78**

> Plus 12 meses × R$0.09 × 2,000 = R$ 2,160 de proventos isentos colhidos durante o holding period (não entram no cálculo de P&L de capital).

###### DB updates aplicados (`data/br_investments.db`)

- `portfolio_positions` RBRX11 (entry 2026-05-07): `active=0, exit_date=2026-05-08, exit_price=8.70`
- `portfolio_positions` KNHF11: nova linha `entry_date=2026-05-08, entry_price=98.56, qty=175, active=1`
- `companies.is_holding`: KNHF11 → 1, RBRX11 → 0

---

##### Análise ex-ante (preservada para retrospectiva)

**Stance que dei**: 🟢 **LEAN MIGRATE faseado** (50% agora, 50% em 8 semanas)
**O que o user fez**: full migration imediata
**Diff**: o user removeu optionality que eu sugeri preservar. Razoável se a convicção era alta — no extremo o faseamento é só uma regra de "não vendas no fundo" que pesa pouco quando a tese qualitativa é forte. Registar e medir nos próximos 8 semanas qual foi a melhor escolha.

---

##### Resumo executivo (1 parágrafo)

Mantemos RBRX11 desde antes da venda da divisão FIIs da RBR à Pátria (Dez/2025). O fundo já foi formalmente renomeado **Pátria Plus Multiestratégia Real Estate FII**, e a Pátria comunicou um *reposicionamento estratégico* — redução de tijolo performado, prioridade a CRIs. O fundo passa portanto a competir, na prática, num espaço onde o **KNHF11 (Kinea Hedge Fund)** já está estabelecido, com gestor mais sénior, *track record* mais longo, e mandato híbrido análogo (CRI + tijolo + cotas FII). Para mesmo capital deployed, ambos pagam DY ~12% mensal isento; a renda mensal ficaria praticamente igual (~R$2,124 vs R$2,160). **A migração troca risco de transição de gestor por exposição a um fundo já estabilizado**, com modesto sacrifício de yield.

---

##### Side-by-side

| | **RBRX11** (held) | **KNHF11** (candidate) |
|---|---|---|
| Nome legal (2026) | Pátria Plus Multiestratégia Real Estate FII | Kinea Hedge Fund FII |
| Gestor | **Pátria Investments** (post-Dez/25) | **Kinea** (Itaú Unibanco) |
| Mandato | Híbrido — pivotando p/ CRI | Híbrido multi-strategy |
| Sector na DB | Híbrido | Híbrido |
| Preço (2026-05-07) | R$ 8.70 | R$ 98.39 |
| Market cap | R$ 989M | R$ 1,935M (~2× maior) |
| DY trailing 12m | ~12.5% | ~11.2–12.0% |
| Distribuição | R$ 0.09/cota/mês (9 meses estável) | R$ 1.00/cota/mês (12 meses estável) |
| Carry alvo | ~1.05% mensal | ~91–99% CDI bruto isento |
| P/VP | n/d (DB sem book) | ~0.93–0.94 (~6–8% deságio) |
| Streak dividendos | 5 anos | 4 anos |
| Alocação CRI | em transição (subindo) | 63.6% (Jun/25) |
| Alocação tijolo | em redução | 29.2% (prime SP) |
| Alocação FII | parte mantida | 13.5% |
| Duration crédito | n/d | ~2.9 anos (positivo p/ ciclo de corte Selic) |
| Risco material 2026 | mudança regulamento, possível troca ticker, integração Pátria; cotistas −8% Jul→Dez/25 | resgates secundário; CRI inadimplência idiossincrática |

> Fontes: `companies` + `fundamentals` + `prices` + `dividends` (DB local), Kinea, fiis.pro, Funds Explorer, statusinvest, Patria Real Estate, Visão do Mercado (Substack), XP Investimentos. Detalhe nas _Sources_ ao fundo.

---

##### Renda anual equivalente (mesmo capital)

Migrar R$17,400 (2,000 cotas RBRX11) → ~177 cotas KNHF11 @ R$98.39:

| Cenário | Renda anual | Yield efectivo |
|---|---|---|
| **Manter RBRX11** | R$ 2,160 | 12.41% |
| **Migrar para KNHF11** | R$ 2,124 | 12.20% |
| Δ | **−R$ 36/ano (−1.7%)** | −0.21 pp |

**Custo da migração em renda é ruído**. Decisão é qualitativa, não numérica.

---

##### Argumentos a favor da migração (LEAN MIGRATE)

1. **Gestor superior**. Kinea tem track record de 15+ anos em FIIs (KNRI11, KNCR11, KNHY11), todos referência no segmento. Pátria assume os FIIs RBR em fase de M&A integration onde "consolidar fundos" e "possível troca de ticker" estão em cima da mesa (memory `rbrx11_patria_acquisition.md`).
2. **Cotistas a fugir**. RBRX11 perdeu **−8% de cotistas Jul→Dez/2025** (62.7k → 57.8k segundo CVM `fii_monthly`). Mercado já está votando com os pés. Não é o sinal que se quer estar do lado errado.
3. **KNHF11 tem opcionalidade**. Carteira hoje 63% CRI + 29% tijolo prime SP + 13.5% FII. Kinea pode rotacionar de crédito para tijolo conforme cap rates comprimem no ciclo de corte de Selic — captura ganho de capital além do carry. Pátria está a fazer o movimento *contrário* (saindo de tijolo, entrando em CRI), o que é razoável mas perde a optionality dos dois lados.
4. **Mandato declarado vs em transição**. KNHF11 já está estabilizado na sua estratégia. RBRX11/Pátria está a meio da transição — assembleia, possível regulamento novo, possível troca de ticker. *Risco operacional ≠ zero*.
5. **DY similar, escala 2×**. KNHF11 R$1.93B vs RBRX11 R$989M — fundo maior com mais liquidez, menor risco de bid/ask spread alargado em momentos de stress.

##### Argumentos contra (HOLD position)

1. **DY ligeiramente maior em RBRX11** (12.5% vs 12.2%). Marginal mas real.
2. **Streak maior** — RBRX11 com 5 anos de pagamento ininterrupto vs 4 de KNHF11.
3. **Custo fiscal e operacional**. Vender 2,000 RBRX11 e comprar ~177 KNHF11 implica corretagem (provavelmente zero na XP), mas há efeito spread de mercado e o spread bid/ask tende a estar alargado em RBRX11 dado o fluxo de saídas.
4. **A transição já foi precificada**. Cotação RBRX11 caiu durante Jul-Dez/2025; em R$8.70 hoje pode já reflectir maior parte do risco. Migrar agora é "vender no fundo".
5. **Pátria não é gestor mau**. R$38B em real estate AuM pós-aquisição → maior gestora de FIIs do Brasil. A integração pode até melhorar processos.

---

##### Sinais para reforçar a decisão (data-driven)

Para virar *LEAN MIGRATE → MIGRATE*, vigiar:
- [ ] Fato relevante CVM RBRX11 com convocatória de assembleia para mudança de regulamento ou troca de ticker → migração imediata.
- [ ] Cotistas RBRX11 continuar caindo no `fii_monthly` Jan-Mai/2026 → tendência confirmada.
- [ ] DY KNHF11 manter R$1.00/cota/mês por +3 meses (até Ago/2026) → carry comprovadamente sustentável no novo regime.
- [ ] P/VP KNHF11 ≤0.95 mantido → entry com colchão de valor.

Para virar *LEAN MIGRATE → HOLD*, vigiar:
- [ ] Pátria publicar carta com plano de gestão claro e *não* mexer em ticker/regulamento.
- [ ] Cotistas RBRX11 estabilizarem ou recuperarem.
- [ ] DY RBRX11 subir acima de R$0.10/cota (sinalizando reposicionamento eficaz).

---

##### Open questions (não resolvidas neste documento)

1. **Posso vender RBRX11 sem prejuízo fiscal material?** R$8.70 vs entry R$8.48 → ganho de R$440 (R$0.22 × 2000). Como FII, ganho é tributado a 20%, mas se vender em prejuízo (não é o caso) seria carry-forward. Verificar no `portfolio_positions` o histórico exacto de aquisições antes de executar.
2. **KNHF11 está em janela de subscrição em 2026?** Algumas Kineas abrem novas emissões periodicamente. Comprar via primária com desconto vs secundária pode mudar o cálculo.
3. **Existe peer melhor que ambos?** KNHY11 (Kinea High Yield) entregou DY 13.43% últimos 12m e R$1.10/cota Mar/2026 — yield superior a ambos. Worth considering como terceira via, mas mandato é só CRI (sem optionality de tijolo/FII).
4. **Concentração Kinea**. User já tem outras posições Kinea? Verificar no portfolio para evitar concentração no mesmo gestor.

---

##### Recomendação operacional (ex-ante, NÃO seguida)

**LEAN MIGRATE com execução faseada**, _não all-in num dia_:

- Sprint 1 (próximas 2 semanas): vender 50% da posição RBRX11 (1,000 cotas → ~R$8,700). Comprar ~88 cotas KNHF11. Manter outras 1,000 RBRX11 para observar a integração Pátria.
- Sprint 2 (8 semanas depois): se sinais de reforço migração persistirem (ver _Sinais_ acima), liquidar restante. Se Pátria estabilizar e dividends manterem, parar e re-avaliar.

Este faseamento limita o risco de "vender no fundo" e dá optionality. Se tudo correr bem com a Pátria, perdemos só ~R$18/ano em renda da metade migrada — perfeitamente comportável.

> **Decisão real do user**: full swap imediato em 2026-05-08 10h48. Ver topo do dossier — registado para retrospectiva.

##### Acompanhamento pós-trade (next 8 semanas)

Para validar/invalidar a decisão de full swap:

- [ ] **Renda KNHF11 mantém R$1.00/cota/mês** (Mai/Jun/Jul/Ago) → tese carry confirmada.
- [ ] **Cotação RBRX11 NÃO sobe muito** (>R$9.20) → "vender no fundo" não se materializou.
- [ ] **Pátria publica fato relevante de mudança regulamento/ticker** → migração foi a leitura certa.
- [ ] **KNHF11 P/VP comprime mais** (<0.92) → entrámos um pouco caros, registar para próximas oportunidades.
- [ ] **DY KNHF11 12m mantém ≥11.5%** → carry sustentável no novo regime de Selic.

---

##### Sources

- [KNHF11 — Kinea Hedge Fund (página oficial)](https://www.kinea.com.br/fundos/fundo-imobiliario-kinea-hedge-fund-knhf11/)
- [KNHF11 dividendos · statusinvest](https://statusinvest.com.br/fundos-imobiliarios/knhf11)
- [KNHF11 · Investidor10](https://investidor10.com.br/fiis/knhf11/)
- [KNHF11 · Funds Explorer](https://www.fundsexplorer.com.br/funds/knhf11)
- [KNHF11 · fiis.pro](https://www.fiis.pro/funds/KNHF11)
- [KNHF11 · Expert XP](https://conteudos.xpi.com.br/fundos-imobiliarios/kinea-hedge-fund-fii-knhf11/)
- [KNHF11: por que ele é um cavalo certo para o ciclo de queda de juros · Visão do Mercado](https://visaodomercado.substack.com/p/knhf11-kinea-hedge-fund-fii-por-que)
- [Patria assume FIIs RBRX11, RBRY11 e RBRP11 · statusinvest](https://statusinvest.com.br/noticias/patria-assume-gestao-fiis-rbrx11-rbry11-rbrp11/)
- [RBRX11 (Pátria Plus Multiestratégia Real Estate FII) · Patria Real Estate](https://realestate.patria.com/papel/rbrx11/)
- [Próximos passos na incorporação do RBRF11 pelo RBRX11 · XP](https://conteudos.xpi.com.br/fundos-imobiliarios/relatorios/proximos-passos-na-incorporacao-do-rbrf11-pelo-rbrx11/)
- [RBRX11 paga R$ 0,09 e foca CRIs · statusinvest](https://statusinvest.com.br/noticias/rbrx11-paga-0-09-e-foca-cris-abril-2026/)
- Local: `data/br_investments.db` (companies, fundamentals, prices, dividends)
- Memory: `rbrx11_patria_acquisition.md` (timeline canónico Pátria-RBR Dez/2025)

#### — · Panorama
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\KNHF11.md` (cemetery archive)_

#### KNHF11 — KNHF11

#holding #br #híbrido

##### 🎯 Verdict — 🟠 HOLD

> **Score**: 4.8/10  |  **Confiança**: 50%  |  _2026-05-08 18:30_

| Dimensão | Score | Peso | Bar |
|---|---:|---:|---|
| Quality    | 3.3/10 | 35% | `███░░░░░░░` |
| Valuation  | 6.0/10 | 30% | `██████░░░░` |
| Momentum   | 6.0/10 | 20% | `██████░░░░` |
| Narrativa  | 4.0/10 | 15% | `████░░░░░░` |

###### Detalhes

- **Quality**: Altman Z None (N/A), Piotroski None/9 (N/A), DivSafety 25.0/100
- **Valuation**: Screen 0.80, DY percentil P24 (EXPENSIVE)
- **Momentum**: 1d 0.6%, 30d 0.04%, YTD 3.51%
- **Narrativa**: user_note=False, YT insights 60d=0

###### Razões

- total 4.8 na zona neutra
- quality frágil

##### Links

- Sector: [[sectors/Híbrido|Híbrido]]
- Market: [[markets/BR|BR]]
- Peers: [[GARE11]] · [[HGRU11]] · [[KNRI11]] · [[RBRX11]] · [[TRXF11]]

##### Snapshot

- **Preço**: R$98.39  (2026-05-07)    _+0.60% 1d_
- **Screen**: 0.8  ✗ fail
- **Altman Z**: n/a ()
- **Piotroski**: None/9
- **Div Safety**: 25.0/100 (RISK)
- **Posição**: 175.0 sh @ R$98.56  →  P&L -0.17%

##### Fundamentals

- P/E: 7.710815 | P/B: None | DY: 11.18%
- ROE: None% | EPS: 12.76 | BVPS: None
- Streak div: 4y | Aristocrat: None

##### Dividendos recentes

- 2026-05-04: R$1.0000
- 2026-03-02: R$1.0000
- 2026-02-02: R$1.0000
- 2026-01-02: R$1.0000
- 2025-12-01: R$1.0000

##### 📈 Live snapshot (auto-gerado)

###### Preço
- **Drawdown 52w**: -1.60%
- **Drawdown 5y**: -1.81%
- **YTD**: +3.51%
- **YoY (1y)**: +8.22%
- **CAGR 3y**: n/a  |  **5y**: n/a  |  **10y**: n/a
- **Vol annual**: +10.91%
- **Sharpe 3y** (rf=4%): n/a

###### Dividendos
- **DY 5y avg**: +12.46%
- **Div CAGR 5y**: +93.02%
- **Frequency**: irregular
- **Streak** (sem cortes): 2 years

###### Valuation
- **P/E vs own avg**: n/a

##### 📈 Price history 1y

_Charts plugin requerido. Se não vês o gráfico: Settings → Community plugins → instalar **Charts** (phibr0)._

```chart
type: line
title: "KNHF11 — 1y close"
labels: ['2025-05-08', '2025-05-14', '2025-05-20', '2025-05-26', '2025-05-30', '2025-06-05', '2025-06-11', '2025-06-17', '2025-06-24', '2025-06-30', '2025-07-04', '2025-07-10', '2025-07-16', '2025-07-22', '2025-07-28', '2025-08-01', '2025-08-07', '2025-08-13', '2025-08-19', '2025-08-25', '2025-08-29', '2025-09-04', '2025-09-10', '2025-09-16', '2025-09-22', '2025-09-26', '2025-10-02', '2025-10-08', '2025-10-14', '2025-10-20', '2025-10-24', '2025-10-30', '2025-11-05', '2025-11-11', '2025-11-17', '2025-11-24', '2025-11-28', '2025-12-04', '2025-12-10', '2025-12-16', '2025-12-22', '2025-12-30', '2026-01-07', '2026-01-13', '2026-01-19', '2026-01-23', '2026-01-29', '2026-02-04', '2026-02-10', '2026-02-18', '2026-02-24', '2026-03-02', '2026-03-06', '2026-03-12', '2026-03-18', '2026-03-24', '2026-03-30', '2026-04-06', '2026-04-10', '2026-04-16', '2026-04-23', '2026-04-29', '2026-05-06']
series:
  - title: KNHF11
    data: [91.24, 90.24, 91.29, 91.39, 91.25, 90.89, 89.52, 90.3, 90.81, 93.98, 91.6, 92.51, 92.75, 91.77, 90.8, 88.9, 89.61, 90.45, 90.15, 89.89, 91.58, 90.23, 91.38, 93.38, 92.72, 93.75, 93.38, 92.77, 92.57, 92.83, 92.99, 92.89, 92.1, 91.69, 91.7, 91.76, 93.0, 93.48, 93.17, 93.5, 93.37, 96.11, 95.73, 96.4, 96.5, 97.75, 98.25, 97.95, 97.51, 98.45, 98.47, 98.0, 98.22, 98.45, 99.5, 98.73, 98.9, 99.02, 99.02, 99.49, 99.29, 99.57, 97.8]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

##### 💰 Dividendos anuais (10y)

```chart
type: bar
title: "KNHF11 — dividend history"
labels: ['2023', '2024', '2025', '2026']
series:
  - title: Dividends
    data: [3.1, 10.81, 11.55, 4.0]
width: 80%
beginAtZero: false
fill: false
tension: 0.3
```

---
*Gerado por obsidian_bridge — 2026-05-08 15:30 UTC*

#### — · IC Debate (synthetic)
_source: `cemetery\2026-05-14\ABSORBED-tickers\tickers\KNHF11_IC_DEBATE.md` (cemetery archive)_

#### 🏛️ Synthetic IC Debate — KNHF11

**Committee verdict**: **HOLD** (medium confidence, 60% consensus)  
**Votes**: BUY=1 | HOLD=3 | AVOID=1  
**Avg conviction majority**: 5.0/10  
**Panel**: 5 personas (failed: 0)

##### 🗣️ Each persona's verdict

###### 🔴 Warren Buffett — **AVOID** (conv 8/10, size: none)

**Rationale**:
- IPO risk
- Complexity in rare earth projects
- Leverage cíclica

**Key risk**: Risco de IPO e incertezas no mercado de terras raras

###### 🟢 Stan Druckenmiller — **BUY** (conv 7/10, size: medium)

**Rationale**:
- PE baixo e dividendos atraentes
- Possível interesse de fundo ativista
- Projetos de terras raras em expansão

**Key risk**: Mercado pode reagir negativamente à oferta do fundo ativista

###### 🟡 Nassim Taleb — **HOLD** (conv 5/10, size: small)

**Rationale**:
- P/E razoável
- Dividendos atraentes
- Notícias de mercado neutras

**Key risk**: Possível intervenção de hedge funds que pode afetar volatilidade e preço

###### 🟡 Seth Klarman — **HOLD** (conv 5/10, size: small)

**Rationale**:
- Valuation seems reasonable with PE of 7.7
- Dividend yield is attractive at 11.19%
- Recent news not directly impacting KNHF11

**Key risk**: Uncertainty in the market for rare earth projects

###### 🟡 Ray Dalio — **HOLD** (conv 5/10, size: medium)

**Rationale**:
- P/E baixo e dividendos atraentes
- Notícias de mercado mistas
- Falta de informações sobre dívida cíclica

**Key risk**: Possível oferta hostil ou mudança no setor que afete o valor da empresa

##### 📊 Context provided

```
TICKER: BR:KNHF11

FUNDAMENTALS LATEST:
  pe: 7.702194
  dy: 11.19%

RECENT MATERIAL NEWS (last 14d via Tavily):
  - Activist Hedge Fund Makes Nearly $3 Billion Offer to Buy Meineke Owner - WSJ [Thu, 30 Ap]
    # Activist Hedge Fund Makes Nearly $3 Billion Offer to Buy Meineke Owner - WSJ. https://www.wsj.com/business/deals/activist-hedge-fund-makes-nearly-3-billion-offer-to-buy-meineke-owner-b3b265d5. # Act
  - US company to carry out IPO of up to US$60.8 million to finance rare earth projects in Brazil - BNamericas [Mon, 04 Ma]
    # US company to carry out IPO of up to US$60.8 million to finance rare earth projects in Brazil. (REA) will carry out an initial public offering (IPO), with part of the proceeds allocated to rare eart
  - Brazil project lifts Meridian London debut - marketscreener.com [Tue, 05 Ma]
    © 2026 bne IntelliNews, source Magazine © Acquiremedia - 2026 Share Latest news about Meridian Mining Plc | | | | | --- | --- | --- | | May. 01 | Meridian Mining raises GBP25.0 million, begins trading
  - Hedge funds seek an edge by using AI’s speed - Financial Times [Mon, 04 Ma]
    * Hedge funds seek an edge by using AI’s speed on x (opens in a new window). * Hedge funds seek an edge by using AI’s speed on facebook (opens in a new window). * Hedge funds seek an edge by using AI’
```

---
*100% Ollama local (qwen2.5:14b-instruct-q4_K_M). Zero Claude tokens. 5 personas debated.*

## ⚙️ Refresh commands

```bash
ii panorama KNHF11 --write
ii deepdive KNHF11 --save-obsidian
ii verdict KNHF11 --narrate --write
ii fv KNHF11
python -m analytics.fair_value_forward --ticker KNHF11
```

---
_Gerado por `scripts/build_merged_hubs.py` em 2026-05-14. Run again to refresh._
