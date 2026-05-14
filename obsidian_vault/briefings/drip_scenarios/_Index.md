---
type: drip_scenarios_index
date: 2026-04-27
holdings: 33
tags: [drip, scenarios, index]
---

# 💰 DRIP Forward Scenarios — Índice

> Cenários de DRIP compounding (5/10/15/20y) por holding, com payback markers. 
Auto-gerados via `scripts/drip_projection.py`. **Refresh diário possível.**

## Ranking por DY-Percentil (entry-timing — NÃO stock-picker)

| Ticker | Kind | DY t12m | Streak | DY-pct (P/100) | Pos PnL | Detail |
|---|---|---:|---:|---|---:|---|
| `KLBN11  ` | fii | 9.12% | 12y | 🟢 P99 CHEAP | -2.2% | [[KLBN11|view]] |
| `HD      ` | equity | 2.75% | 40y | 🟢 P94 CHEAP | +15.0% | [[HD|view]] |
| `VGIR11  ` | fii | 15.63% | 5y | 🟢 P92 CHEAP | +0.7% | [[VGIR11|view]] |
| `GREK    ` | equity | 3.25% | 15y | 🟢 P81 CHEAP | +39.6% | [[GREK|view]] |
| `ITSA4   ` | equity | 8.63% | 20y | 🟢 P79 CHEAP | +83.5% | [[ITSA4|view]] |
| `O       ` | equity | 5.11% | 33y | 🟢 P77 CHEAP | -0.4% | [[O|view]] |
| `BBDC4   ` | equity | 7.56% | 19y | 🟢 P76 CHEAP | +23.9% | [[BBDC4|view]] |
| `RBRX11  ` | fii | 12.31% | 5y | 🔴 P18 EXPENSIVE | +4.0% | [[RBRX11|view]] |
| `TEN     ` | equity | 1.53% | 24y | 🔴 P17 EXPENSIVE | +64.1% | [[TEN|view]] |
| `PVBI11  ` | fii | 5.95% | 7y | 🔴 P16 EXPENSIVE | -0.1% | [[PVBI11|view]] |
| `JPM     ` | equity | 1.91% | 43y | 🔴 P12 EXPENSIVE | +0.6% | [[JPM|view]] |
| `BN      ` | equity | 0.55% | 40y | 🔴 P11 EXPENSIVE | +77.9% | [[BN|view]] |
| `KO      ` | equity | 2.69% | 65y | 🔴 P6 EXPENSIVE | +0.9% | [[KO|view]] |
| `XP      ` | equity | 0.91% | 8y | 🔴 P3 EXPENSIVE | +13.7% | [[XP|view]] |
| `AAPL    ` | equity | 0.38% | 15y | 🔴 P2 EXPENSIVE | +122.4% | [[AAPL|view]] |
| `JNJ     ` | equity | 2.29% | 65y | 🔴 P2 EXPENSIVE | -4.5% | [[JNJ|view]] |
| `TSM     ` | equity | 0.84% | 23y | 🔴 P1 EXPENSIVE | +292.8% | [[TSM|view]] |
| `ABBV    ` | equity | 3.39% | 14y | 🟡 P— — | -1.1% | [[ABBV|view]] |
| `ACN     ` | equity | 1.74% | 22y | 🟡 P— — | -16.5% | [[ACN|view]] |
| `BLK     ` | equity | 2.04% | 24y | 🟡 P— — | +16.4% | [[BLK|view]] |
| `BRK-B   ` | equity | 0.00% | 0y | 🟡 P— — | +12.3% | [[BRK-B|view]] |
| `BTLG11  ` | fii | 9.19% | 5y | 🟡 P— — | -0.1% | [[BTLG11|view]] |
| `GS      ` | equity | 1.67% | 28y | 🟡 P— — | +190.7% | [[GS|view]] |
| `IVVB11  ` | sp_etf | 0.00% | —y | 🟡 P— — | +176.9% | [[IVVB11|view]] |
| `LFTB11  ` | selic_etf | 0.00% | —y | 🟡 P— — | +0.4% | [[LFTB11|view]] |
| `NU      ` | equity | 0.00% | 0y | 🟡 P— — | +75.7% | [[NU|view]] |
| `PG      ` | equity | 2.87% | 65y | 🟡 P— — | +3.8% | [[PG|view]] |
| `PLD     ` | equity | 2.89% | 30y | 🟡 P— — | +30.1% | [[PLD|view]] |
| `PLTR    ` | equity | 0.00% | 0y | 🟡 P— — | +78.1% | [[PLTR|view]] |
| `PRIO3   ` | equity | 0.00% | 1y | 🟡 P— — | +57.2% | [[PRIO3|view]] |
| `TSLA    ` | equity | 0.00% | 0y | 🟡 P— — | +101.9% | [[TSLA|view]] |
| `VALE3   ` | equity | 6.38% | 18y | 🟡 P— — | +38.9% | [[VALE3|view]] |
| `XPML11  ` | fii | 9.94% | 5y | 🟡 P— — | +2.1% | [[XPML11|view]] |

## Como ler

- **DY-pct (P0-100)**: percentil do DY actual vs próprio histórico 10y. P>70 = CHEAP entry-timing (DY actual alto vs próprio); P<30 = EXPENSIVE.
- **Kind**: `equity` / `fii` / `compounder` (classificador interno).
- **Pos PnL**: ganho/perda actual da posição não-realizada.
- **Cenários full** (conservador/base/optimista, 5/10/15/20y): clique em [view] para detalhe.

Ver também: [[Glossary/DRIP|DRIP entry]] · [[Bibliotheca/Knowledge/drip_compounding_math]]

---
*Auto-build via `scripts/drip_projection.py` + index gen.*