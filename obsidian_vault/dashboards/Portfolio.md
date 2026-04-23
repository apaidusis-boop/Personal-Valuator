---
tags: [dashboard, portfolio]
---
# 📊 Portfolio Dashboard (Dataview)

> Requer plugin **Dataview** habilitado. Para vista sem plugin, ver [[My Portfolio]].

## Holdings — live snapshot

```dataview
TABLE
  price AS "Preço",
  change_1d_pct AS "1d %",
  pnl_pct AS "P&L %",
  screen_score AS "Screen",
  altman_z AS "Altman",
  piotroski AS "Piot",
  div_safety AS "DivSaf"
FROM "tickers"
WHERE is_holding = true
SORT pnl_pct ASC
```

## Watchlist — screen passa

```dataview
TABLE
  price AS "Preço",
  pe AS "P/E",
  pb AS "P/B",
  dy_pct AS "DY%",
  screen_score AS "Screen",
  altman_z AS "Altman",
  piotroski AS "Piot"
FROM "tickers"
WHERE is_holding = false AND screen_pass = true
SORT screen_score DESC
```

## Screen falhas críticas (Altman < 3 ou Piotroski ≤ 3)

```dataview
TABLE altman_z, piotroski, screen_score, price
FROM "tickers"
WHERE (altman_z < 3 OR piotroski <= 3)
SORT altman_z ASC
```

## Quality high (Piotroski ≥ 7)

```dataview
TABLE piotroski, altman_z, pe, pb, dy_pct
FROM "tickers"
WHERE piotroski >= 7
SORT piotroski DESC
```

## Dividend stars (streak ≥ 15y)

```dataview
TABLE streak_years AS "Streak", dy_pct AS "DY%", div_safety AS "Safety", aristocrat
FROM "tickers"
WHERE streak_years >= 15
SORT streak_years DESC
```
