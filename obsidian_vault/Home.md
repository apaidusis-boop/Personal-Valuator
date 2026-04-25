# 🏠 Investment Intelligence — Morning Landing

> **Dashboard interactivo**: <http://localhost:8501> _(corre `ii dashboard` ou usa o launcher do Desktop)_

## 🔥 Decisões de hoje

> Para approve/ignore com clique → abre o **dashboard** → tab "🎯 Actions Queue".
> Para ler tese de cada decisão → clica nos tickers abaixo.

```dataview
TABLE
  market AS "Mkt",
  sector AS "Sector",
  round(price, 2) AS "Px",
  dy_pct + "%" AS "DY",
  altman_z AS "Altman Z",
  piotroski AS "Piotroski",
  screen_pass AS "Pass"
FROM "tickers"
WHERE is_holding = true AND (
  altman_z < 1.81
  OR piotroski <= 3
  OR dy_pct >= 8
  OR screen_pass = false
)
SORT altman_z ASC
LIMIT 15
```

---

## 📜 Read first

- [[CONSTITUTION|📜 The Constitution]] — master doc + 6 não-negociáveis + decision log
- [[../PHASE_Z_ROADMAP|🎨 Phase Z Roadmap (UI Layer)]] — current sprint

## 🌅 Today

- [[briefings/2026-04-23|🌅 Latest morning briefing]]
- [[briefings/metrics_2026-04-24|📊 Metrics report 2026-04-24]]
- [[briefings/overnight_research_2026-04-24/index|🦉 Overnight RAG research]]

## 💼 Portfolio at a glance

```dataview
TABLE WITHOUT ID
  file.link AS "Ticker",
  market AS "Mkt",
  sector AS "Sector",
  position_qty AS "Qty",
  round(market_value, 0) AS "MV",
  round(pnl_pct, 1) + "%" AS "P&L",
  dy_pct + "%" AS "DY"
FROM "tickers"
WHERE is_holding = true
SORT market_value DESC
LIMIT 15
```

## 🎯 Screen passers (top quality)

```dataview
TABLE WITHOUT ID
  file.link AS "Ticker",
  market AS "Mkt",
  sector AS "Sector",
  pe AS "P/E",
  dy_pct + "%" AS "DY",
  roe_pct + "%" AS "ROE",
  streak_years AS "Streak"
FROM "tickers"
WHERE screen_pass = true
SORT roe_pct DESC
LIMIT 20
```

## 🧰 Quick jump

| | | |
|---|---|---|
| [[My Portfolio\|💼 Portfolio]] | [[Holdings\|📋 Holdings]] | [[Allocation\|📊 Allocation]] |
| [[TaxLots\|📜 Tax Lots]] | [[Rebalance\|🔄 Rebalance]] | [[Transactions\|📜 Tx]] |
| [[wiki/Index\|📚 Wiki]] | [[skills/_MOC\|🧰 Skills]] | [[skills/Phase_X_Perpetuum_Engine\|🔁 Perpetuum]] |

## 📈 Markets & sectors

- [[markets/BR|🇧🇷 Brazil]] · [[markets/US|🇺🇸 United States]]
- Sectors: [[sectors/Banks|Banks]] · [[sectors/Financials|Financials]] · [[sectors/Technology|Technology]] · [[sectors/Healthcare|Healthcare]] · [[sectors/Consumer_Staples|Consumer Staples]] · [[sectors/REIT|REIT]] · [[sectors/Energy|Energy]] · [[sectors/Materials|Materials]] · [[sectors/Logística|Logística]] · [[sectors/Shopping|Shopping]] · [[sectors/Papel_(CRI)|Papel (CRI)]] · [[sectors/Híbrido|Híbrido]]

## 🩺 Perpetuum engine

> 9 perpetuums autónomos correm diariamente. Health visível no dashboard tab "🩺 Perpetuum Health".

```dataview
LIST
FROM "agents"
WHERE contains(file.name, "perpetuum") OR contains(file.name, "Perpetuum")
SORT file.name ASC
LIMIT 12
```

## 📚 Knowledge base

- [[skills/Library_First_Harvest_2026-04-24|📚 Library — books harvested]]
- 1704 chunks indexados (Damodaran + 3 Dalio) — RAG via dashboard tab "📚 Ask Library"
- 16 YAML methods activos → paper signals em "📈 Paper Signals" tab

## 🎬 YouTube digest

- 14 vídeos ingeridos — pasta [[videos/]]
- Insights por canal: dashboard tab "📺 YouTube Digest"

## 🗺️ Graph view

Abre o **graph view** (canto superior esquerdo, 3 bolas) — clusters emergem por sector + market + peers. Ticker → notes wiki, perpetuum logs, briefings.

---

_Last refresh: ver `python scripts/obsidian_bridge.py --refresh` (corre via dashboard tab Portfolio→Refresh ou cron 23:30)._
