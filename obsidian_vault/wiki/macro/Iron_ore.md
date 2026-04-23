---
type: macro
name: Iron Ore — Commodity driver VALE3
category: commodity
tags: [macro, commodity, iron_ore, vale, mining]
related: ["[[USDBRL_PTAX]]", "[[Mining_iron_ore]]", "[[Brent_WTI]]"]
---

# Iron Ore — "Minério de ferro"

## O que é

Commodity **bulk** (não tradada em bolsa com contratos líquidos como oil/copper). Principais contratos:
- **SGX 62% Fe (Singapore)** — benchmark global
- **DCE (Dalian Commodity Exchange)** — benchmark China
- **Platts 62% CFR China**

Preço em **USD/ton**. Entrega em **China ports** (Qingdao, Tianjin).

## Key grades

| Grade | Fe content | Premium |
|---|:-:|---|
| **Fines 62%** | 62% | Baseline |
| **Fines 65%** | 65% | +$10-20 premium (high-grade, produtividade) |
| **Lump** | 62% | +$5-10 (no sintering needed) |
| **Pellet** | 66%+ | +$30-60 (processed, DR-ready) |

## Supply concentrado

**Big 3** = ~70% seaborne supply:
- **Vale (Brazil)** — ~300 Mt/year
- **BHP (Australia)** — ~290 Mt
- **Rio Tinto (Australia)** — ~330 Mt
- **FMG (Fortescue Australia)** — ~180 Mt

BR é **#2 exporter** global após Australia.

## Demand — dominada por China

- **China = 60-70%** seaborne demand (70% world steel)
- Outros: Japan (HY steel), Korea (POSCO), Europa (ArcelorMittal)
- India growing mas infrastructure bottleneck

### China steel drivers
- **Real estate** ~30% domestic steel
- **Infrastructure** (high-speed rail, ponts) ~25%
- **Auto** 10-15%
- **Machinery** 15-20%
- **Shipbuilding, appliances** remainder

## Ciclo típico

### Boom phase
- China stimulus (2008-2011, 2015-2016, 2020)
- Credit expansion → real estate starts ↑
- Steel mills restock
- **Iron ore spikes $100+ → $200+**

### Bust phase
- China property crunch (2021-2024 Evergrande/Country Garden)
- Mills de-stock
- Iron ore drops $60-80

## Faixas históricas

| Ano | Iron ore (62% CFR China) | Contexto |
|---|:-:|---|
| 2008 | $85→$60 | GFC collapse |
| 2011 | **$190** | China stimulus peak |
| 2015 | **$38** | China slowdown low |
| 2019 | $70-90 | Vale Brumadinho disaster → spike |
| 2021 (Jul) | **$230** | Post-COVID China stimulus |
| 2021 (Dec) | $90 | China property turn |
| 2022-2024 | $100-140 range | Moderate |
| 2025-2026 | $95-110 | Property crunch weighing |

## Impact em [[VALE3]]

**VALE3** é super-sensível. EBITDA leverage to iron ore:
- **Cost base**: ~$25/ton full break-even (best-in-class)
- **$60 price** → modest profit
- **$100 price** → robust FCF, dividends extraordinary
- **$150+ price** → all-time high profits

### Historical correlations
- Iron ore up 10% → VALE3 up ~12-15% (with 2-3 week lag)
- China PMI up → iron ore + VALE3 up
- USDBRL depreciate → VALE3 up (revenue USD)

## Brumadinho aftermath (2019+)

Jan 2019: tailings dam collapse killed 270+ em Brumadinho.
- VALE3 production cut ~90 Mt
- Iron ore spiked to $125 (previous $70)
- VALE3 stock: dropped 25% then recovered, ultimately boost earnings
- Lessons: regulatory scrutiny + operational discipline key for VALE3 thesis

## Cross-commodity signals

### Copper ↗ = Steel ↗ = Iron ore ↗
"Dr. Copper" often leads iron ore 3-6m.

### Coking coal (met coal)
Input for blast furnace. Spiked 2021-2022 with Australia-China geopolitics. Afeta steel margins (não directly iron ore demand).

### USD ↘ = commodities ↑
Classic relationship; 2022-2023 weak USD helped iron ore recover.

## Green steel thesis (long-term)

DR (Direct Reduction) processes need **high-grade iron ore (>66%)** + hydrogen. Traditional 62% fines won't fit.

Premium for **pellet / high-grade**:
- Vale's **Mariana + S11D** pellet operations strategically positioned
- CVRD / Anglo American pellet competition

Este é um **structural bull** para high-grade producers 2030+.

## No nosso sistema

Actualmente **não puxamos iron ore explicitly** — captado via VALE3 price + analyst commentary.

**Pendente roadmap**: `fetchers/commodities_fetcher.py` com iron ore, copper, oil, gold.

**No theme tracking** (YouTube): quando BTG/Virtual Asset mencionar "minério", "iron ore", tema 'mining_iron_ore' triggers.

## Consulta

- **Platts**: spglobal.com/commodities (paywall)
- **Reuters Commodities**: free digest
- **YCharts**, **TradingView**: TIOc1 (iron ore 62% Fe CFR China)
- **Vale IR**: presentations mostram realized prices

## Para ver o trend

| Indicador | Fonte | Sinal |
|---|---|---|
| Iron ore 62% spot | Platts | Price level |
| China real estate starts | NBS China | Lead 3-6m |
| China steel production | NBS China | Demand proxy |
| Port inventory China | Platts | Supply slack |
| Vale production guidance | Vale IR | Supply BR |

---

> **Fontes**: S&P Global Commodity Insights (Platts); Vale IR materials; BHP Operational Review; Iron Ore Market Weekly (Wood Mackenzie); Bloomberg.
