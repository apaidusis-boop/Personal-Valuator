---
tags: [allocation, portfolio]
---
# Alocação

> [!info] Resumo
> **Total:** R$ 466,204.43  
> **PTAX:** 4.9170  
> **Holdings:** 33

---

## Por mercado

| Mercado | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| **BR** | 12 | R$ 353,478 | 75.8% |
| **US** | 21 | R$ 112,726 | 24.2% |

---

## Por sector

| Sector | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| [[sectors/ETF-RF|ETF-RF]] | 1 | R$ 105,589 | 22.6% |
| [[sectors/Mining|Mining]] | 1 | R$ 40,115 | 8.6% |
| [[sectors/Holding|Holding]] | 2 | R$ 35,361 | 7.6% |
| [[sectors/Banks|Banks]] | 1 | R$ 34,021 | 7.3% |
| [[sectors/Oil_&_Gas|Oil & Gas]] | 1 | R$ 32,393 | 6.9% |
| [[sectors/Financials|Financials]] | 6 | R$ 30,454 | 6.5% |
| [[sectors/Technology|Technology]] | 4 | R$ 22,306 | 4.8% |
| [[sectors/Healthcare|Healthcare]] | 2 | R$ 18,571 | 4.0% |
| [[sectors/Materials|Materials]] | 1 | R$ 18,024 | 3.9% |
| [[sectors/Shopping|Shopping]] | 1 | R$ 17,582 | 3.8% |
| [[sectors/Papel_(CRI)|Papel (CRI)]] | 1 | R$ 17,565 | 3.8% |
| [[sectors/Híbrido|Híbrido]] | 1 | R$ 17,218 | 3.7% |
| [[sectors/Logística|Logística]] | 1 | R$ 17,106 | 3.7% |
| [[sectors/Corporativo|Corporativo]] | 1 | R$ 16,384 | 3.5% |
| [[sectors/Consumer_Staples|Consumer Staples]] | 2 | R$ 11,546 | 2.5% |
| [[sectors/REIT|REIT]] | 2 | R$ 10,847 | 2.3% |
| [[sectors/Consumer_Disc.|Consumer Disc.]] | 2 | R$ 7,470 | 1.6% |
| [[sectors/Energy|Energy]] | 1 | R$ 7,429 | 1.6% |
| [[sectors/ETF-US|ETF-US]] | 1 | R$ 4,429 | 1.0% |
| [[sectors/ETF|ETF]] | 1 | R$ 1,792 | 0.4% |

---

## Top 10 concentrações

| # | Ticker | MV (BRL) | % | Cumulative % |
|---:|---|---:|---:|---:|
| 1 | [[LFTB11]] | R$ 105,589 | 22.6% | 22.6% |
| 2 | [[VALE3]] | R$ 40,115 | 8.6% | 31.3% |
| 3 | [[BBDC4]] | R$ 34,021 | 7.3% | 38.6% |
| 4 | [[ITSA4]] | R$ 33,051 | 7.1% | 45.6% |
| 5 | [[PRIO3]] | R$ 32,393 | 6.9% | 52.6% |
| 6 | [[KLBN11]] | R$ 18,024 | 3.9% | 56.5% |
| 7 | [[XPML11]] | R$ 17,582 | 3.8% | 60.2% |
| 8 | [[VGIR11]] | R$ 17,565 | 3.8% | 64.0% |
| 9 | [[KNHF11]] | R$ 17,218 | 3.7% | 67.7% |
| 10 | [[BTLG11]] | R$ 17,106 | 3.7% | 71.4% |

---

## Por quality bucket

> [!note] Tiers
> **Tier A:** Altman Z ≥ 3 **e** Piotroski ≥ 6  
> **Tier B:** Altman Z ≥ 1.8 **e** Piotroski ≥ 4  
> **Tier C:** restante

```dataview
TABLE altman_z, piotroski, market_value, pnl_pct
FROM "tickers"
WHERE is_holding = true
SORT altman_z DESC
```