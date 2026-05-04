---
tags: [allocation, portfolio]
---
# Alocação

> [!info] Resumo
> **Total:** R$ 471,485.64  
> **PTAX:** 4.9700  
> **Holdings:** 33

---

## Por mercado

| Mercado | Holdings | MV (BRL) | % |
|---|---:|---:|---:|
| **BR** | 12 | R$ 360,126 | 76.4% |
| **US** | 21 | R$ 111,360 | 23.6% |

---

## Por sector

| Sector                     |           Holdings | MV (BRL) |          % |       |
| -------------------------- | -----------------: | -------: | ---------: | ----- |
| [[sectors/ETF-RF           |           ETF-RF]] |        1 | R$ 105,467 | 22.4% |
| [[sectors/Mining           |           Mining]] |        1 |  R$ 42,750 | 9.1%  |
| [[sectors/Holding          |          Holding]] |        2 |  R$ 37,205 | 7.9%  |
| [[sectors/Banks            |            Banks]] |        1 |  R$ 36,066 | 7.6%  |
| [[sectors/Oil_&_Gas        |        Oil & Gas]] |        1 |  R$ 32,368 | 6.9%  |
| [[sectors/Financials       |       Financials]] |        6 |  R$ 30,459 | 6.5%  |
| [[sectors/Technology       |       Technology]] |        4 |  R$ 21,828 | 4.6%  |
| [[sectors/Healthcare       |       Healthcare]] |        2 |  R$ 18,523 | 3.9%  |
| [[sectors/Materials        |        Materials]] |        1 |  R$ 17,870 | 3.8%  |
| [[sectors/Shopping         |         Shopping]] |        1 |  R$ 17,542 | 3.7%  |
| [[sectors/Híbrido          |          Híbrido]] |        1 |  R$ 17,440 | 3.7%  |
| [[sectors/Papel_(CRI)      |      Papel (CRI)]] |        1 |  R$ 17,352 | 3.7%  |
| [[sectors/Logística        |        Logística]] |        1 |  R$ 17,186 | 3.6%  |
| [[sectors/Corporativo      |      Corporativo]] |        1 |  R$ 16,796 | 3.6%  |
| [[sectors/Consumer_Staples | Consumer Staples]] |        2 |  R$ 11,489 | 2.4%  |
| [[sectors/REIT             |             REIT]] |        2 |  R$ 10,748 | 2.3%  |
| [[sectors/Consumer_Disc.   |   Consumer Disc.]] |        2 |   R$ 7,298 | 1.5%  |
| [[sectors/Energy           |           Energy]] |        1 |   R$ 6,923 | 1.5%  |
| [[sectors/ETF-US           |           ETF-US]] |        1 |   R$ 4,433 | 0.9%  |
| [[sectors/ETF              |              ETF]] |        1 |   R$ 1,742 | 0.4%  |

---

## Top 10 concentrações

| # | Ticker | MV (BRL) | % | Cumulative % |
|---:|---|---:|---:|---:|
| 1 | [[LFTB11]] | R$ 105,467 | 22.4% | 22.4% |
| 2 | [[VALE3]] | R$ 42,750 | 9.1% | 31.4% |
| 3 | [[BBDC4]] | R$ 36,066 | 7.6% | 39.1% |
| 4 | [[ITSA4]] | R$ 34,855 | 7.4% | 46.5% |
| 5 | [[PRIO3]] | R$ 32,368 | 6.9% | 53.3% |
| 6 | [[KLBN11]] | R$ 17,870 | 3.8% | 57.1% |
| 7 | [[XPML11]] | R$ 17,542 | 3.7% | 60.9% |
| 8 | [[RBRX11]] | R$ 17,440 | 3.7% | 64.6% |
| 9 | [[VGIR11]] | R$ 17,352 | 3.7% | 68.2% |
| 10 | [[BTLG11]] | R$ 17,186 | 3.6% | 71.9% |

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