---
type: market
name: br
tags: [market]
---

# 🌐 Market: BR

## Holdings — P&L sorted

```dataview
TABLE sector, price, pnl_pct AS "P&L %", screen_score, altman_z, piotroski
FROM "tickers"
WHERE market = "br" AND is_holding = true
SORT pnl_pct ASC
```

## Watchlist screen passes

```dataview
TABLE sector, price, screen_score, dy_pct AS "DY%"
FROM "tickers"
WHERE market = "br" AND is_holding = false AND screen_pass = true
SORT screen_score DESC
```

## Por sector neste mercado

```dataview
TABLE length(rows) AS Total, sum(rows.is_holding) AS Holdings
FROM "tickers"
WHERE market = "br"
GROUP BY sector
SORT length(rows) DESC
```
