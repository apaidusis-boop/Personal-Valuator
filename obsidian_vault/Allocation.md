---
tags: [allocation, portfolio]
---
# 📊 Alocação

_Total: **R$ 472,996.50** |  PTAX: 5.0083_

## Por mercado

| Mercado | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| 🇧🇷 BR | 12 | R$ 360,791 | 76.3% |
| 🇺🇸 US | 21 | R$ 112,206 | 23.7% |

## Por sector

| Sector | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| [[sectors/ETF-RF|ETF-RF]] | 1 | R$ 105,467 | 22.3% |
| [[sectors/Mining|Mining]] | 1 | R$ 42,935 | 9.1% |
| [[sectors/Holding|Holding]] | 2 | R$ 37,502 | 7.9% |
| [[sectors/Banks|Banks]] | 1 | R$ 36,414 | 7.7% |
| [[sectors/Oil_&_Gas|Oil & Gas]] | 1 | R$ 31,503 | 6.7% |
| [[sectors/Financials|Financials]] | 6 | R$ 30,433 | 6.4% |
| [[sectors/Technology|Technology]] | 4 | R$ 22,050 | 4.7% |
| [[sectors/Healthcare|Healthcare]] | 2 | R$ 18,824 | 4.0% |
| [[sectors/Materials|Materials]] | 1 | R$ 17,940 | 3.8% |
| [[sectors/Shopping|Shopping]] | 1 | R$ 17,649 | 3.7% |
| [[sectors/Híbrido|Híbrido]] | 1 | R$ 17,640 | 3.7% |
| [[sectors/Papel_(CRI)|Papel (CRI)]] | 1 | R$ 17,387 | 3.7% |
| [[sectors/Corporativo|Corporativo]] | 1 | R$ 17,143 | 3.6% |
| [[sectors/Logística|Logística]] | 1 | R$ 17,128 | 3.6% |
| [[sectors/Consumer_Staples|Consumer Staples]] | 2 | R$ 11,632 | 2.5% |
| [[sectors/REIT|REIT]] | 2 | R$ 10,939 | 2.3% |
| [[sectors/Consumer_Disc.|Consumer Disc.]] | 2 | R$ 7,336 | 1.6% |
| [[sectors/Energy|Energy]] | 1 | R$ 6,884 | 1.5% |
| [[sectors/ETF-US|ETF-US]] | 1 | R$ 4,433 | 0.9% |
| [[sectors/ETF|ETF]] | 1 | R$ 1,758 | 0.4% |

## Top 10 concentrações

| # | Ticker | MV (BRL) | % | Cumulative % |
|---:|---|---:|---:|---:|
| 1 | [[LFTB11]] | R$ 105,467 | 22.3% | 22.3% |
| 2 | [[VALE3]] | R$ 42,935 | 9.1% | 31.4% |
| 3 | [[BBDC4]] | R$ 36,414 | 7.7% | 39.1% |
| 4 | [[ITSA4]] | R$ 35,152 | 7.4% | 46.5% |
| 5 | [[PRIO3]] | R$ 31,503 | 6.7% | 53.2% |
| 6 | [[KLBN11]] | R$ 17,940 | 3.8% | 57.0% |
| 7 | [[XPML11]] | R$ 17,649 | 3.7% | 60.7% |
| 8 | [[RBRX11]] | R$ 17,640 | 3.7% | 64.4% |
| 9 | [[VGIR11]] | R$ 17,387 | 3.7% | 68.1% |
| 10 | [[PVBI11]] | R$ 17,143 | 3.6% | 71.7% |

## Por quality bucket (Dataview)

Altman Z ≥ 3 E Piotroski ≥ 6 = **Tier A**; Altman ≥ 1.8 E Piot ≥ 4 = **Tier B**; restante = **Tier C**.

```dataview
TABLE altman_z, piotroski, market_value, pnl_pct
FROM "tickers"
WHERE is_holding = true
SORT altman_z DESC
```