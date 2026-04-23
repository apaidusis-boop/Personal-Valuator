---
type: sector
name: ETF
count: 1
tags: [sector]
---

# 🏢 ETF

Total tickers: **1**
Holdings: **1**

## Tabela live (Dataview)

```dataview
TABLE market, price, pnl_pct, screen_score, altman_z, piotroski
FROM "tickers"
WHERE sector = "ETF"
SORT is_holding DESC, pnl_pct ASC
```

## Tickers neste sector

- ★ [[GREK]] _(us)_