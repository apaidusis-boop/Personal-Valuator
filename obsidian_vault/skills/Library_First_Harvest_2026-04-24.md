---
type: library_harvest
tags: [library, books, dalio, damodaran, insights]
date: 2026-04-24
pipeline: ollama_local
tokens_claude_used: 0
---

# 📚 Primeira colheita — 4 livros ingeridos e extraídos

> **User adicionou 4 PDFs hoje. O pipeline processou 1,704 chunks e extraiu 97 methods + 252 heuristics + 468 concepts em ~8 minutos totais, 100% Ollama local, zero tokens Claude.**

## 📊 Resumo quantitativo

| Livro | Páginas | Chunks | Sample | Methods | Heuristics | Concepts |
|---|---|---|---|---|---|---|
| **Damodaran — Investment Valuation 3rd ed** | ~1,000 | 1,043 | 60 | **67** | 113 | 192 |
| **Dalio — Principles for Navigating Big Debt Crises** | ~500 | 550 | 40 | **20** | 66 | 117 |
| **Dalio — Changing World Order Charts** | ~150 | 52 | 30 | 7 | 47 | 114 |
| **Dalio — CWO Power Index** | ~60 | 59 | 15 | 3 | 26 | 45 |
| **TOTAL** | — | 1,704 | 145 | **97** | 252 | 468 |

## 🎯 Methods mais accionáveis (Damodaran — valuation direct use)

Estes são fórmulas concretas que podemos ligar aos nossos fetchers/scoring:

### Valuation core
- **Firm DCF**: `Value = Σ(CF_firm_t / (1 + WACC)^t)` + Terminal Value
- **Equity DCF**: `Value = Σ(CF_equity_t / (1 + k_e)^t)`
- **Gordon DDM**: `V = D₁ / (k - g)` — já usamos no `drip_projection.py`
- **Put-Call Parity**: `P + S = C + Ke^(-rt)` — útil para sanity check options

### Risk / cost of capital
- **Beta Estimation**: `Beta = Cov(R_stock, R_market) / Var(R_market)`
- **Unlevered Beta**: `β_u = β_L / (1 + (D/E)(1-T))` — comparar firms c/ capital diferente
- **Implied Equity Premium**: `r = (D₁ + g·P₀)/P₀ - g` — quando não há histórico
- **Risk-free Rate build-up**: `RFR = Expected Inflation + Real Rate` — útil para BR (Selic real)
- **Local Bond Method**: `RFR_local = Bond Yield - Default Spread` — aplicação direta para BR

### Factor awareness
- **January Effect**: small-cap premium concentrado nas primeiras 2 semanas de Janeiro
- **Survival Bias**: backtests sem tickers delistados inflam retornos
- **Transaction Cost Consideration**: strategies ignorando custos são ficção

## 🌊 Methods Dalio macro (diretamente wirable ao regime classifier)

### Frameworks principais
- **Debt Growth Management**: "Maintain debt growth at level income can service"
- **Deleveraging Cycle Analysis**: track debt/GDP ratio over time → identify bubble + depression phases
- **Inflationary Deleveraging Cycle**: pre-crisis signals = high fx-denominated debts + foreign financing dependence
- **Capital Flow Analysis**: monitor foreign investment + currency + export prices + borrowing costs
- **Hyperinflation Spiral Analysis**: logarithmic charts to see exponential money supply growth

### Bubble detection (usable tomorrow)
> "Defining characteristics of a bubble:
> 1. Prices are high relative to traditional measures
> 2. Prices are discounting future rapid price appreciation from these high levels
> 3. There is broad bullish sentiment
> 4. Purchases are being financed by debt..."

### Policy response signals
- **Reflation Phase**: Fed cutting + M0 increasing + lowering rates + managing banks = expansion coming
- **Policy Response to Capital Flow Adversity**: currency peg abandonment → current account improves ≥7% GDP within short period
- **Pushing on a String**: late-cycle central bank limits — QE with diminishing effectiveness

## 📜 Top heuristics regravadas (para acção)

### Damodaran (valuation discipline)
- "Beware single-point estimates — always do scenario analysis with reasonable ranges"
- "Survival bias is not benign; it's systematic"
- "Transaction costs kill 'theoretical' alpha — include in backtest"
- "For DCF validity, require 3 conditions: positive CFs growing at g < WACC, finite terminal period, g ≤ economy growth"

### Dalio (macro discipline)
- "Weakening capital flows precede balance of payments crises"
- "Central banks focusing on inflation and growth may overlook bubble formation"
- "Countries without reserve currency are more prone to inflationary depressions"
- "Watch central bank actions BEFORE taking long position in a currency"
- "Currency depreciation provides short-term stimulation but is harmful when overused"
- "Losers of wars experience deeper depressions + higher inflation + more reliance on..."

## 🔗 Tickers/assets mencionados (para cross-reference)

Do Damodaran: AT&T, Amgen, Boeing, Cisco, Coca-Cola, Deutsche Bank, Disney, Eurotunnel, Exxon Mobil, Home Depot, MGM Resorts (convertibles), S&P 500, Tata Motors, Xerox.

Valor: quando falamos de Disney/Boeing etc. em panorama, podemos referenciar casos do Damodaran.

## 🚀 Como usar isto AGORA

### Caminho 1 — Enriquecer CLAUDE.md com heuristics validadas
- Sample 20 heuristics Dalio + 20 Damodaran
- Revisitar critérios BR/US contra estas heuristics
- `perpetuum_method_discovery` já identificou métodos staleness 35/100

### Caminho 2 — Novos YAML methods em library/methods/
Já temos `graham_defensive` + `dalio_all_weather_tilt`. Candidatos novos:
- `damodaran_dcf_basic` — baseado no Firm Valuation method
- `damodaran_implied_premium` — equity premium quando dividend yield approach
- `dalio_debt_bubble_check` — formalizar os 4 critérios de bubble
- `dalio_capital_flow_signal` — pre-crisis indicator

### Caminho 3 — RAG sobre chunks (futuro, W.6 stack)
- LlamaIndex + Ollama embeddings (nomic-embed-text já está local!)
- "Pergunta em português sobre Dalio → resposta cita páginas relevantes"
- Implementação: ~200 LOC extra se user quiser

## ⚠️ Limitações honestas

1. **Qwen 14B pode errar** em fórmulas complexas — sample manual dos top 10 methods antes de codificar. **Revisitei 5 top Damodaran acima: corretas**.
2. **Chunks samplam livro** (60 de 1043 = 5.7% do Damodaran). Perdemos 94% mas cobrimos book com stride. Para coverage completa, correr com `--max 1000` (1 hora).
3. **Heuristics genéricas** — algumas repetem (ex: "diversificação importa"). Dedup futuro pode aplicar embeddings similarity.
4. **Method rules às vezes vazias** (`None provided`) — o LLM não inventou quando chunk não tinha detalhe. Honesto.

## 💰 Custo desta sessão

- **Tokens Claude**: **0**. Tudo Ollama local (Qwen 14B).
- **Tempo wall-clock**: ~8 min para 4 livros.
- **Energia**: compute local. Zero API calls.
- **Resultado tangível**: 97 methods + 252 heuristics + 468 concepts indexed.

Este é **exactamente** o spirit [[../_MOC|in-house first]] materializado.

## 📁 Output files

```
library/insights/
├── cwo_power_index.json                                   11 KB
├── daliochangingworldordercharts.json                     17 KB
├── investment_valuation_3rd_edition.json                  64 KB
└── principles_for_navigating_big_debt_crises_by_ray_d.json  30 KB
```

Plus `library/chunks/<book>/*.txt` (1,704 files ≈ 4 MB).

## Links

- [[Library_Books_and_Options]] — strategy document + paper-trade pipeline
- [[Phase_X_Perpetuum_Engine]] — the engine que pode correr isto diariamente
- `library/extract_insights.py` — extractor shipped today
- `library/insights/*.json` — raw structured outputs
