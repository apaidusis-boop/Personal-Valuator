---
type: sector
name: Benchmark
count: 2
tags: [sector]
---

# 🏢 Benchmark

Total tickers: **2**
## Tabela live (Dataview)

```dataview
TABLE market, price, pnl_pct, screen_score, altman_z, piotroski
FROM "tickers"
WHERE sector = "Benchmark"
SORT is_holding DESC, pnl_pct ASC
```

## Tickers neste sector

- [[BOVA11]] _(br)_
- [[SPY]] _(us)_