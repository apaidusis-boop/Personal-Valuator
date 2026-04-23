---
type: macro
name: 10Y Treasury Yield
category: interest_rates
country: US
source: FRED DGS10
tags: [macro, treasury, 10y, yield, benchmark]
related: ["[[Fed_funds]]", "[[2s10s]]", "[[CPI]]", "[[Risk_free_rate]]", "[[Equity_risk_premium]]"]
---

# 10-Year Treasury Yield

## O que é

**Yield-to-maturity** do título do Tesouro americano com 10 anos de duração — é o **"risk-free rate"** global de referência.

Publicado diariamente em **FRED: DGS10**.

## Por que é tão importante

1. **Discount rate** default em modelos DCF global
2. **Benchmark hipotecas** (30y fixed) — housing market depende disto
3. **Pricing mundial** de sovereign debt emergente (spread vs Treasury)
4. **Stock valuation**: equity risk premium = ERP = Equity yield - 10Y
5. **Corporate bond spreads**: IG/HY mede como "treasury + X bp"

## Decomposição

$$
\text{10Y Yield} = \text{Expected Real Rate} + \text{Inflation Expectations} + \text{Term Premium}
$$

### Expected real rate
Mercado expectativa de **juros reais** ao longo de 10 anos.
- Proxy: **TIPS** (Treasury Inflation-Protected Securities) 10Y yield
- Current TIPS ~2% = **real rate** esperado

### Inflation expectations
Diferença entre Nominal 10Y e TIPS 10Y = **breakeven inflation**.
- Current ~2.3% = mercado espera CPI médio 2.3% próximos 10y
- Meta Fed: PCE 2% (CPI ~2.2% implícito)

### Term premium
Compensação por **uncertainty** sobre inflação + duration risk.
- Historicamente 1-2%
- Era 2010-2019: **negativo** (QE distorceu)
- 2022+: back to positive (~0.5-1%)

## Drivers (curto prazo)

- **Fed decisions** (especialmente QE/QT)
- **CPI surprises** (hot CPI → yields up)
- **NFP** (strong jobs → hawkish → yields up)
- **Budget deficit / supply** (mais emissão → yields up)
- **Global risk-off** (flight to safety → yields DOWN)

## Drivers (longo prazo)

- **Demographics** (aging developed = savings glut = yields low)
- **Productivity growth**
- **Debt/GDP** (high debt = eventual inflation / repression = yields up long-run)
- **Reserve currency status** (US benefit unique)

## Histórico

| Período | 10Y yield | Contexto |
|---|:-:|---|
| 1981 | **15.8%** | Volcker inflation fight peak |
| 1990s | 6-8% | Goldilocks era |
| 2000 | 6% | Dot-com peak |
| 2008 | 2% | GFC cuts |
| 2012 | **1.4%** | Historic LOW |
| 2018 | 3.2% | Trump tax cut bounce |
| 2020 | **0.52%** | **COVID extreme** |
| 2022 | 4.2% | Fed hike aggressivo |
| 2023-2024 | 4-5% | Normalisation |
| 2025-2026 | 4-4.5% | Plateau |

## Como investidor equity deve pensar

### Regra DCF
Discount rate tipico equity = **10Y + 5-6% ERP** = 9-10.5%.

Se 10Y sobe 1pp → discount rate +1pp → fair multiple -10 a -20% (!!!).

É por isso que **rate spikes crash equity** (2022: 10Y 1.5%→4.5%, Nasdaq -35%).

### Regra DY
DY competitivo vs 10Y:
- 10Y 4%: DY equity > 4-5% = atractivo
- 10Y 6%: DY equity > 6-7% = atractivo

### Regra relative valuation sectors
- **Utilities / REITs / FIIs**: -1 correlation com 10Y (bond proxies)
- **Banks**: +0.3 correlation (NIM)
- **Growth tech**: -0.5 correlation (duration-like)
- **Consumer staples**: mild negative
- **Commodities**: independent

## Comparação com outros sovereigns

| País | 10Y (Abril 2026) |
|---|:-:|
| US | 4.4% |
| UK | 4.1% |
| Germany | 2.3% |
| Japan | 1.2% |
| China | 1.7% |
| **Brasil NTN-B 10y** | ~7% real + inflação |

**Spread BR-US** em bonds de 10y: ~2-3pp + inflação differential. Valor em carry trade histórico.

## No nosso sistema

- `data/us_investments.db` → `fetchers/fred_fetcher.py` puxa DGS10
- `analytics/regime.py`: componente importante do classificador US
- `scripts/research.py` [7] Regime macro: cita 10Y

## Como consultar

- **FRED**: `fred.stlouisfed.org/series/DGS10`
- **Real-time**: Bloomberg, tradingeconomics.com
- **Curve**: Bloomberg / CNBC yield curve page

---

> **Fontes**: Federal Reserve St. Louis (FRED); US Treasury publications; Andrew Chen *The Yield Curve and Recession*; Cam Harvey research; Hull *Options, Futures and Other Derivatives*.
