---
type: macro
name: Brent + WTI — Crude oil benchmarks
category: commodity
tags: [macro, oil, brent, wti, crude, commodity]
related: ["[[USDBRL_PTAX]]", "[[Oil_cycles_decades]]", "[[Oil_Gas_integrated]]", "[[Shipping_tankers]]"]
---

# Brent + WTI — Benchmarks do Petróleo

## Os 2 principais

### Brent (global benchmark)
- Crude **leve-suave** do Mar do Norte
- Preço de **referência global** para ~60% do petróleo mundial
- Usado para petróleo brasileiro (PRIO3, PETR4), angolano, saudita
- Contratos: **ICE Brent** (Londres)

### WTI (US benchmark)
- West Texas Intermediate, **crude americano**
- Preço "domestic US" — permanece $2-5 abaixo de Brent tipicamente
- Usado para produção shale US
- Contratos: **NYMEX** (Nova York)

## Spread Brent-WTI

Historicamente **Brent premium ~$2-5**. Causes:
1. WTI é **landlocked** (Cushing OK delivery point) — storage pressure
2. US export ban até 2015 comprimiu WTI
3. Transport costs Cushing → coast

Post-2015 ban lift: spread narrower (~$1-3).

## Drivers de preço

### Supply
- **OPEC+ quotas** (Saudi + Russia coordination)
- **US shale production** (DUC inventory, rig count)
- **Non-OPEC growth** (Brazil, Guyana, Norway)
- **Geopolitical disruptions** (Middle East, Russia sanctions)

### Demand
- **China growth** (biggest marginal importer)
- **Global GDP**
- **Aviation demand** (jet fuel 8% of barrel)
- **Petrochemicals** (15-20% of barrel)
- **EV penetration** (slowly eroding gasoline demand)

### Macro
- **USD strength** (oil priced in USD — strong USD = lower oil)
- **Inflation regime** (oil often inflation hedge)
- **Interest rates** (inventory finance costs)

## Faixas históricas

| Ano | Brent médio | Contexto |
|---|:-:|---|
| 1998 | **$11** | Asian crisis low |
| 2008 (Jul) | **$147** | Peak bubble |
| 2008 (Dec) | $40 | Post-crash |
| 2014-2016 | $30-100 | Oil price war (Saudi vs shale) |
| 2020 (Apr) | **$-37 WTI (!!)** | COVID demand destruction |
| 2022 (Jun) | $125 | Russia invasion spike |
| 2023-2025 | $75-90 | Post-war normalisation |
| 2026 (now) | $70-80 | OPEC+ managing supply |

## Impacto nos nossos holdings

### [[PRIO3]] (oil E&P small-cap BR)
- **Break-even** ~$35-40 Brent
- **FCF leverage** ~$15 FCF/barrel above break-even
- Brent $90 → PRIO3 ~$60 historically
- Brent $50 → PRIO3 ~$30

### [[PETR4]] (oil integrated major BR)
- **Break-even** ~$30-35 (deep-water pre-sal efficiency)
- **Dividend policy** explicit tied to Brent: $40 floor + 60% FCF payout above
- Brent $90+ → dividend extraordinary
- Brent $60-70 → dividend baseline

### [[TEN]] (tanker shipping)
- **Rates** (VLCC, Suezmax) **correlated** com oil price oscilation (não level)
- High oil → traders store on ships (contango floating storage)
- Cycle peak ≠ oil peak — usually lags by 6-12m
- 2023-2025 tanker boom: oil moderate but geopolitical uncertainty = rate boom

### Outras exposições indirectas
- **EMBR3**: jet fuel costs (negative)
- **VALE3**: unit costs (iron ore extraction uses diesel)
- **Airlines BR** (AZUL4, GOLL4): cost huge
- **Chemicals** (BRKM5): naphtha input

## OPEC+ cheat sheet

### Members principais (2024)
- Saudi Arabia (core OPEC)
- Russia (OPEC+ cooperation)
- UAE, Iraq, Kuwait, Kazakhstan, Iran (sanctions)
- Venezuela (declining)

### Output cuts decision framework
- **Saudi stated**: target Brent $80-90 "fair" range
- Cut when prices < $70
- Hold/increase when > $90

### Compliance monitoring
- Saudi strict; Russia historically cheats
- Secondary source reporting (Reuters, Platts)

## Quotes fundamental trade-offs

### Cost curve
| Source | Break-even |
|---|:-:|
| Saudi (traditional) | $15-25 |
| Russia Urals | $35-40 |
| US shale Permian | $40-50 (new wells) |
| US shale tier-2 | $55-65 |
| Deepwater Brazil | $30-40 (pre-sal) |
| Canadian oil sands | $55-70 |
| UK North Sea mature | $45-55 |

$50 Brent destrói shale marginal. $80 pays everyone.

## Cycles previews

Ciclos históricos (~7-15 anos):
- 1980s oil bust (post-Volcker)
- 1998 Asian crisis bottom
- 2000-2008 China boom
- 2014 shale flood / Saudi price war
- 2020 COVID demand destruction
- 2022-2023 Russia-Ukraine spike
- 2024-? moderation phase

## No nosso sistema

Pendente fetcher explicit para oil — actualmente só indirecto via ticker correlations.

**Add to roadmap**: `fetchers/commodities_fetcher.py` via EIA API ou yfinance (BZ=F, CL=F).

## Para consultar

- **EIA**: eia.gov/petroleum/
- **OilPrice.com**
- **Platts / S&P Global Commodity Insights**
- **Bloomberg**: `CO1 Comdty` (Brent continuous), `CL1 Comdty` (WTI)

---

> **Fontes**: IEA World Energy Outlook; EIA STEO (Short-Term Energy Outlook); Daniel Yergin *The Prize*; OPEC Monthly Market Report; nosso monitoring via YouTube macro themes.
