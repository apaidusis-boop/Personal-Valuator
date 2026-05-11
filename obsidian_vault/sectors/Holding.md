---
type: sector
name: Holding
count: 2
tags: [sector]
---

# 🏢 Holding

Total tickers: **2**
Holdings: **2**

## Tabela live (Dataview)

```dataview
TABLE market, price, pnl_pct, screen_score, altman_z, piotroski
FROM "tickers"
WHERE sector = "Holding"
SORT is_holding DESC, pnl_pct ASC
```

## Tickers neste sector

- ★ [[BRK-B]] _(us)_
- ★ [[ITSA4]] _(br)_