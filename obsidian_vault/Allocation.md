---
tags: [allocation, portfolio]
---
# 📊 Alocação

_Total: **R$ 466,419.37** |  PTAX: 4.9653_

## Por mercado

| Mercado | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| 🇧🇷 BR | 11 | R$ 355,338 | 76.2% |
| 🇺🇸 US | 21 | R$ 111,081 | 23.8% |

## Por sector

| Sector | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| [[sectors/ETF-RF|ETF-RF]] | 1 | R$ 123,951 | 26.6% |
| [[sectors/Mining|Mining]] | 1 | R$ 43,280 | 9.3% |
| [[sectors/Holding|Holding]] | 2 | R$ 37,545 | 8.0% |
| [[sectors/Banks|Banks]] | 1 | R$ 36,688 | 7.9% |
| [[sectors/Oil_&_Gas|Oil & Gas]] | 1 | R$ 31,835 | 6.8% |
| [[sectors/Financials|Financials]] | 6 | R$ 30,405 | 6.5% |
| [[sectors/Technology|Technology]] | 4 | R$ 21,385 | 4.6% |
| [[sectors/Healthcare|Healthcare]] | 2 | R$ 18,915 | 4.1% |
| [[sectors/Shopping|Shopping]] | 1 | R$ 16,244 | 3.5% |
| [[sectors/Papel_(CRI)|Papel (CRI)]] | 1 | R$ 16,052 | 3.4% |
| [[sectors/Híbrido|Híbrido]] | 1 | R$ 16,050 | 3.4% |
| [[sectors/Logística|Logística]] | 1 | R$ 15,939 | 3.4% |
| [[sectors/Corporativo|Corporativo]] | 1 | R$ 15,714 | 3.4% |
| [[sectors/Consumer_Staples|Consumer Staples]] | 2 | R$ 11,400 | 2.4% |
| [[sectors/REIT|REIT]] | 2 | R$ 10,947 | 2.3% |
| [[sectors/Consumer_Disc.|Consumer Disc.]] | 2 | R$ 7,247 | 1.6% |
| [[sectors/Energy|Energy]] | 1 | R$ 6,703 | 1.4% |
| [[sectors/ETF-US|ETF-US]] | 1 | R$ 4,384 | 0.9% |
| [[sectors/ETF|ETF]] | 1 | R$ 1,735 | 0.4% |

## Top 10 concentrações

| # | Ticker | MV (BRL) | % | Cumulative % |
|---:|---|---:|---:|---:|
| 1 | [[LFTB11]] | R$ 123,951 | 26.6% | 26.6% |
| 2 | [[VALE3]] | R$ 43,280 | 9.3% | 35.9% |
| 3 | [[BBDC4]] | R$ 36,688 | 7.9% | 43.7% |
| 4 | [[ITSA4]] | R$ 35,201 | 7.5% | 51.3% |
| 5 | [[PRIO3]] | R$ 31,835 | 6.8% | 58.1% |
| 6 | [[XPML11]] | R$ 16,244 | 3.5% | 61.6% |
| 7 | [[VGIR11]] | R$ 16,052 | 3.4% | 65.0% |
| 8 | [[RBRX11]] | R$ 16,050 | 3.4% | 68.5% |
| 9 | [[BTLG11]] | R$ 15,939 | 3.4% | 71.9% |
| 10 | [[PVBI11]] | R$ 15,714 | 3.4% | 75.2% |

## Por quality bucket (Dataview)

Altman Z ≥ 3 E Piotroski ≥ 6 = **Tier A**; Altman ≥ 1.8 E Piot ≥ 4 = **Tier B**; restante = **Tier C**.

```dataview
TABLE altman_z, piotroski, market_value, pnl_pct
FROM "tickers"
WHERE is_holding = true
SORT altman_z DESC
```