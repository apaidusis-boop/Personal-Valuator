---
tags: [allocation, portfolio]
---
# 📊 Alocação

_Total: **R$ 465,208.46** |  PTAX: 4.9539_

## Por mercado

| Mercado | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| 🇧🇷 BR | 11 | R$ 354,382 | 76.2% |
| 🇺🇸 US | 21 | R$ 110,826 | 23.8% |

## Por sector

| Sector | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| [[sectors/ETF-RF|ETF-RF]] | 1 | R$ 123,951 | 26.6% |
| [[sectors/Mining|Mining]] | 1 | R$ 42,985 | 9.2% |
| [[sectors/Holding|Holding]] | 2 | R$ 37,342 | 8.0% |
| [[sectors/Banks|Banks]] | 1 | R$ 36,505 | 7.8% |
| [[sectors/Oil_&_Gas|Oil & Gas]] | 1 | R$ 31,548 | 6.8% |
| [[sectors/Financials|Financials]] | 6 | R$ 30,335 | 6.5% |
| [[sectors/Technology|Technology]] | 4 | R$ 21,336 | 4.6% |
| [[sectors/Healthcare|Healthcare]] | 2 | R$ 18,871 | 4.1% |
| [[sectors/Shopping|Shopping]] | 1 | R$ 16,208 | 3.5% |
| [[sectors/Híbrido|Híbrido]] | 1 | R$ 16,106 | 3.5% |
| [[sectors/Papel_(CRI)|Papel (CRI)]] | 1 | R$ 16,052 | 3.5% |
| [[sectors/Logística|Logística]] | 1 | R$ 15,931 | 3.4% |
| [[sectors/Corporativo|Corporativo]] | 1 | R$ 15,708 | 3.4% |
| [[sectors/Consumer_Staples|Consumer Staples]] | 2 | R$ 11,374 | 2.4% |
| [[sectors/REIT|REIT]] | 2 | R$ 10,922 | 2.3% |
| [[sectors/Consumer_Disc.|Consumer Disc.]] | 2 | R$ 7,231 | 1.6% |
| [[sectors/Energy|Energy]] | 1 | R$ 6,688 | 1.4% |
| [[sectors/ETF-US|ETF-US]] | 1 | R$ 4,384 | 0.9% |
| [[sectors/ETF|ETF]] | 1 | R$ 1,731 | 0.4% |

## Top 10 concentrações

| # | Ticker | MV (BRL) | % | Cumulative % |
|---:|---|---:|---:|---:|
| 1 | [[LFTB11]] | R$ 123,951 | 26.6% | 26.6% |
| 2 | [[VALE3]] | R$ 42,985 | 9.2% | 35.9% |
| 3 | [[BBDC4]] | R$ 36,505 | 7.8% | 43.7% |
| 4 | [[ITSA4]] | R$ 35,004 | 7.5% | 51.3% |
| 5 | [[PRIO3]] | R$ 31,548 | 6.8% | 58.0% |
| 6 | [[XPML11]] | R$ 16,208 | 3.5% | 61.5% |
| 7 | [[RBRX11]] | R$ 16,106 | 3.5% | 65.0% |
| 8 | [[VGIR11]] | R$ 16,052 | 3.5% | 68.4% |
| 9 | [[BTLG11]] | R$ 15,931 | 3.4% | 71.9% |
| 10 | [[PVBI11]] | R$ 15,708 | 3.4% | 75.2% |

## Por quality bucket (Dataview)

Altman Z ≥ 3 E Piotroski ≥ 6 = **Tier A**; Altman ≥ 1.8 E Piot ≥ 4 = **Tier B**; restante = **Tier C**.

```dataview
TABLE altman_z, piotroski, market_value, pnl_pct
FROM "tickers"
WHERE is_holding = true
SORT altman_z DESC
```