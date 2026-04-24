---
type: wiki_index
tags: [wiki, index]
---

# 📚 Wiki — Finance Map

> Fundações conceptuais. Cada nota é um nó do grafo. Links aggressivos cross-wiki.
>
> **Status**: Fases A + B.1 + C.1 + D + E concluídas → **53 notas**.
> Fase C.2 (analyst tracking infra) + Fase B.2 (holdings/watchlist deep) pendentes.

## 🧪 Methodology (16)

Frameworks e ferramentas de análise.

### Valuation
- [[Graham_Number]] — fórmula margem segurança Graham
- [[Graham_deep_value]] — filosofia Graham complete
- [[Buffett_quality]] — evolução para moats + quality
- [[DCF_simplified]] — intrinsic value determinístico
- [[DDM_Gordon]] — dividend discount model
- [[P_E_interpretation]] — P/E quando faz sense
- [[P_B_interpretation]] — P/B + quando engana
- [[FCF_yield]] — Free Cash Flow yield

### Quality
- [[Piotroski_F]] — 9-point quality score
- [[Altman_Z]] — distress predictor
- [[ROIC_interpretation]] — Return on Invested Capital
- [[Moat_types]] — 5 moats Dorsey + 7 Powers Helmer

### Income / DRIP
- [[Dividend_Safety]] — nosso score 0-100
- [[Aristocrats_Kings]] — 25y+ / 50y+ streak
- [[DRIP_compounding]] — math do reinvest

### Risk management
- [[Kelly_criterion]] — position sizing optimal

## 🌐 Macro indicators (11)

Séries que drivam valuation + regime.

### Brasil
- [[Selic]] — taxa básica BR
- [[CDI]] — benchmark renda fixa
- [[IPCA]] — inflação oficial
- [[USDBRL_PTAX]] — câmbio

### US
- [[Fed_funds]] — taxa básica US
- [[10Y_Treasury]] — risk-free global
- [[2s10s]] — yield curve + recession signal
- [[VIX]] — volatility / fear index

### Commodities
- [[Brent_WTI]] — oil benchmarks
- [[Iron_ore]] — VALE3 driver

### Cross-market
- [[BR_vs_US_equity_culture]] — **comparação estrutural tax/retail/governance/currency**

## 📜 Historical context (5)

Como interest rates + crises evolved.

- [[Selic_history]] — 1999-2026 completo
- [[Fed_funds_history]] — 1954-2026 (Volcker → Powell)
- [[Brazilian_inflation_hist]] — hyperinflation → Plano Real → sticky era
- [[2008_GFC]] — Global Financial Crisis
- [[2020_COVID_crash]] — fastest bear ever

## 🏢 Setores (8)

Deep-dives com framework + peer tables + links para tickers.

- [[BR_Banks]] — por que bancos precisam scoring separado; Big 5 + boutique + digital + seguradora
- [[BR_Utilities]] — transmissão vs distribuição vs geração; RAP, PLD, hidrologia
- [[BR_FIIs_vs_US_REITs]] — structural diff (tax, mandate, cadência); tijolo/papel vs REIT types
- [[Consulting_IT_Services]] — ACN/IBM/TCS/INFY; strategy/implement/managed mix
- [[Oil_and_Gas_cycle]] — upstream/midstream/downstream; majors vs E&P vs PETR4
- [[Semiconductors_cycle]] — fabless/foundry/IDM; NVDA/TSM/ASML/AVGO; AI supercycle
- [[Pulp_and_Paper_cycle]] — BEKP cash cost; SUZB3 + KLBN4 + FX lever
- [[Consumer_Staples_moats]] — PG/KO/CL; brand + DSD + private label threat + GLP-1

## 🔄 Cycles (5)

Frameworks para timing de entrada/saída cyclical.

- [[Oil_cycle]] — 4 fases (Discovery → Oversupply → Discipline → Shortage); indicators
- [[Semi_cycle]] — 3-4y cycle; memory/logic/equipment desincronizados; AI supercycle
- [[Pulp_cycle]] — BEKP spot + port inventory; BR structural low-cost advantage
- [[Real_estate_cycle]] — 6-10y long cycle; sector-specific (office decline, industrial bull, DC secular)
- [[Shipping_cycle]] — 4-6y; tanker peak 2026 ([[TEN]] distress case)

## 💰 Tax & Regulatory (5)

Compliance + optimization cross-jurisdiction.

- [[BR_dividend_isencao]] — 0% IR residente PF; JCP trick; PL 1.087/2025 watch
- [[US_LTCG_STCG]] — LT/ST holding periods; brackets; wash sale; state tax
- [[Dividend_withholding_BR_US]] — BR resident holding US stocks; W-8BEN; Irish UCITS alternative
- [[CVM_vs_SEC]] — Fato Relevante vs 8-K; Form 4 vs FR; BDR vs ADR
- [[Tax_lot_selection]] — FIFO vs LIFO vs Spec ID vs HIFO strategies

## 📋 Playbooks (7)

Checklists operacionais destilados do código/scoring.

- 🚨 [[Token_discipline]] — **REGRA #1** — in-house first, tokens last. Meta-regra que governa todas as outras.
- [[Analysis_workflow]] — fluxo canónico por caso de uso (panorama → decisão → journal); anti-padrões
- [[Buy_checklist]] — 7-step pipeline (screen → quality → safety → intent → timing → size → journal)
- [[Sell_triggers]] — 5 categorias (thesis-broken / quality / valuation / drift / personal)
- [[Rebalance_cadence]] — trimestral drift check; semestral execution; rebalance-by-contribution
- [[Tax_lot_selection_practical]] — JPM UI steps + scenarios (TLH, partial exit, charitable)
- [[Web_scraping_subscriptions]] — ingest Suno/XP/WSJ/Finclass via cookies + Ollama extract (0 tokens)

## 💼 Holdings thesis (Fase B.2 — 20 notas)

Ver [[wiki/holdings/_README|secção README + índice completo]].

### BR (8)
- [[ITSA4]] · [[BBDC4]] · [[PRIO3]] · [[VALE3]] · [[PVBI11]] (turnaround) · [[BTLG11]] · [[VGIR11]] · [[XPML11]]

### US (12)
- [[JNJ]] · [[KO]] · [[PG]] · [[JPM]] · [[BLK]] · [[BN]] · [[BRK-B]] · [[ACN]] · [[O]] · [[TSM]] · [[AAPL]] · [[PLD]] · [[HD]] · [[NU]] · [[TEN]] ⚠️

## 🗺 Próximas fases (roadmap)

### Fase B.3 — Watchlist deep (pending)
- 50 priority watchlist names expanded com thesis light.
- Holdings sem thesis ainda: ABBV, GS, PLTR, TSLA, XP, GREK.

### Fase C.2 — Analyst tracking infra (pending)
- DB schema novo: `analyst_calls` + `yt_predictions`.
- Track record de firms (Bradesco BBI, XP, BTG, Goldman, JPM).
- YouTube channel accuracy tracking (leverage phase Q pipeline).
- Integration com `ii surprise` (earnings targets vs real).

### Fase F — Trade journal reflexivo (ideia)
- Journal estruturado de entries/exits com 6-month lookback.
- "O que acertei / errei" — lição aprendida.
- Link para teses específicas.

## 🔗 Como usar

1. **Entry point**: abrir qualquer nota → seguir backlinks + forwardlinks.
2. **Search**: `Ctrl+O` → procurar conceito.
3. **Graph view** (ícone canto esquerdo) — visualizar conexões.
4. **Dataview queries** em `dashboards/*` — filtrar por tag/type.
5. **Smart Chat** (Smart Connections plugin + Ollama) — pergunta livre sobre vault.

## 💡 Convenção

- `type: method | macro | history | sector | cycle | tax | playbook | company | analyst | wiki_index`
- Frontmatter YAML estruturado (Dataview-friendly).
- Links internos sempre: `[[Note_name]]`.
- Tags taxonomia: `#method/valuation`, `#macro/br`, `#sector/banks`, `#cycle/oil`, `#playbook/buy`.

## 📊 Vault stats (2026-04-24)

- **Wiki notes**: 76 (16 methods + 11 macro + 5 history + 8 sectors + 5 cycles + 5 tax + 6 playbooks + **20 holdings thesis** + 1 section index)
- **Ticker notes**: 34 (auto-generated via `obsidian_bridge.py`)
- **Video notes**: 21 (Phase Q YouTube pipeline)
- **Analyst reports**: 125 ingeridos (Fool 18 + WSJ/MW 20 + XP 87) — Phase U
- **Dashboards**: 3 (Portfolio, Sectors, Briefing)
- **Total**: ~130+ markdown notes + 125 analyst reports em SQLite

---

*Phase A: 2026-04-23 — 31 notas initial.*
*Phase B.1+C.1+D+E: 2026-04-24 — +22 notas (sectors + cycles + tax + playbooks).*
*Phase U: 2026-04-24 — Token discipline + scraping infra + Playwright + 125 analyst reports.*
*Phase B.2: 2026-04-24 — +20 holdings thesis deep (BR 8 + US 12).*
*Continuous expansion.*
