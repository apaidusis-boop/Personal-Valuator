---
tags: [dashboard, briefing]
---
# 📰 Daily Briefing

## Preço móveis — últimas 24h

```dataview
TABLE price, change_1d_pct AS "1d %", pnl_pct AS "P&L %"
FROM "tickers"
WHERE is_holding = true
SORT abs(change_1d_pct) DESC
LIMIT 20
```

## Holdings com eventos recentes (≤ 7d)

Manual ingest quando briefing correr. Ver ficheiro individual do ticker para eventos SEC/CVM.

## YouTube — últimos insights por canal

Ver `yt_digest.py --channel "X" --days 7` + importar manualmente.
