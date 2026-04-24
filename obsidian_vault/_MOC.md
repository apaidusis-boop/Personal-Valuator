---
type: moc
name: Map of Content — root
tags: [moc, index, navigation]
---

# 🗺 Map of Content

Entry point único. Tudo navegável daqui.

## 🎯 Workflow diário

1. **Manhã**: [[briefings/2026-04-24|Briefing hoje]] → P&L, triggers, earnings próximos
2. **Análise ticker**: abrir [[tickers/]] direto ou ler [[wiki/playbooks/Analysis_workflow|fluxo]]
3. **Decisão**: [[wiki/playbooks/Buy_checklist]] / [[wiki/playbooks/Sell_triggers]]
4. **Após trade**: `ii notes add ...` → vault atualiza

## 📊 Portfolio

- [[My Portfolio]] — overview BR+US em BRL
- [[Holdings]] — tabela unificada
- [[Allocation]] — drift vs target
- [[Rebalance]] — ações sugeridas
- [[TaxLots]] — lots JPM (LT/ST)
- [[Transactions]] — log entries/exits
- [[Earnings Surprise]] — YT targets vs real

## 📚 Knowledge base

- [[wiki/Index|Wiki completa (53 notas)]]
- 🚨 [[wiki/playbooks/Token_discipline|REGRA #1 — in-house first]]

### Frameworks análise
- [[wiki/methods/Graham_Number]] · [[wiki/methods/Buffett_quality]] · [[wiki/methods/Altman_Z]] · [[wiki/methods/Piotroski_F]]

### Setores (8)
- [[wiki/sectors/BR_Banks]] · [[wiki/sectors/BR_Utilities]] · [[wiki/sectors/BR_FIIs_vs_US_REITs]]
- [[wiki/sectors/Consulting_IT_Services]] · [[wiki/sectors/Oil_and_Gas_cycle]]
- [[wiki/sectors/Semiconductors_cycle]] · [[wiki/sectors/Pulp_and_Paper_cycle]] · [[wiki/sectors/Consumer_Staples_moats]]

### Cycles (5)
- [[wiki/cycles/Oil_cycle]] · [[wiki/cycles/Semi_cycle]] · [[wiki/cycles/Pulp_cycle]] · [[wiki/cycles/Real_estate_cycle]] · [[wiki/cycles/Shipping_cycle]]

### Playbooks (5)
- 🚨 [[wiki/playbooks/Token_discipline]]
- [[wiki/playbooks/Buy_checklist]] · [[wiki/playbooks/Sell_triggers]]
- [[wiki/playbooks/Rebalance_cadence]] · [[wiki/playbooks/Tax_lot_selection_practical]]
- [[wiki/playbooks/Analysis_workflow]] (nova)
- [[wiki/playbooks/Web_scraping_subscriptions]] (nova)

### Tax & regulatory
- [[wiki/tax/BR_dividend_isencao]] · [[wiki/tax/US_LTCG_STCG]]
- [[wiki/tax/Dividend_withholding_BR_US]] · [[wiki/tax/CVM_vs_SEC]] · [[wiki/tax/Tax_lot_selection]]

## 🎬 Media & external

- [[wiki/macro/BR_vs_US_equity_culture]] — comparação estrutural
- Pasta: [[videos/]] — YouTube ingests (21)
- Pasta: [[briefings/]] — daily digests

## 🧭 Live screens (Dataview)

### Holdings em screen fail (alerta automático)

```dataview
TABLE market, sector, screen_score, altman_z, piotroski
FROM "tickers"
WHERE is_holding = true AND screen_pass = false
SORT screen_score ASC
```

### Próximos earnings (ordenados)

```dataview
TABLE next_earnings, market, sector
FROM "tickers"
WHERE is_holding = true AND next_earnings != null
SORT next_earnings ASC
LIMIT 10
```

### Watchlist passes

```dataview
TABLE market, sector, screen_score, dy_pct AS "DY%"
FROM "tickers"
WHERE is_holding = false AND screen_pass = true
SORT screen_score DESC
LIMIT 15
```

## 🔧 Dashboards & agg

- [[dashboards/Portfolio]] · [[dashboards/Sectors]] · [[dashboards/Briefing]]
- [[markets/BR]] · [[markets/US]]
- Pasta: [[sectors/]] — tag aggregates por sector

---

> _MOC é o ponto de entrada canónico. [[Home]] mantém-se como legado auto-gerado pelo `obsidian_bridge`._
