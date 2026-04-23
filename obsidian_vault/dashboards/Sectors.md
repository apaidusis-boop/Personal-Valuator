---
tags: [dashboard, sector]
---
# 🏢 Cobertura por Sector

```dataview
TABLE length(rows) AS "N", sum(rows.is_holding) AS "Holdings"
FROM "tickers"
GROUP BY sector
SORT length(rows) DESC
```

## Por mercado

```dataview
TABLE length(rows) AS "N", sum(rows.is_holding) AS "Holdings"
FROM "tickers"
GROUP BY market
```
