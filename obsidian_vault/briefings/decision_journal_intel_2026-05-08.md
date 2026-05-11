---
type: decision_journal_intelligence
date: 2026-05-08
tags: [decision_journal, meta, autocrítica, patterns]
---

# 🧠 Decision Journal Intelligence

> Pattern mining em past decisions, actions, paper signals, e thesis decay. 100% local SQL.

## 🔁 Pattern 1+2 — Action resolution patterns (last 90d)

> Window 90d: action conta se foi aberta OU resolvida no período. Exclui bulk-ignores históricos para que ignore-rate reflicta comportamento actual.

| Kind | n | Open | Resolved | Ignored | Bulk | Ignore% | Avg days |
|---|---:|---:|---:|---:|---:|---:|---:|
| perpetuum:content_quality | 3 | 1 | 0 | 2 | 0 | 66.7% | 2.4d |
| perpetuum:token_economy | 3 | 1 | 0 | 2 | 0 | 66.7% | 2.4d |
| perpetuum:ri_freshness | 50 | 20 | 0 | 30 | 0 | 60.0% | 2.4d |
| perpetuum:vault | 80 | 0 | 0 | 0 | 80 | — | — |
| altman_distress | 22 | 22 | 0 | 0 | 0 | 0.0% | — |
| piotroski_weak | 22 | 22 | 0 | 0 | 0 | 0.0% | — |
| dy_above_pct | 13 | 13 | 0 | 0 | 0 | 0.0% | — |
| dy_percentile_vs_own_history | 11 | 11 | 0 | 0 | 0 | 0.0% | — |
| perpetuum:data_coverage | 7 | 6 | 0 | 0 | 1 | 0.0% | — |

> **Bulk** = one-time sweep (notes starts with `bulk-` ou resolução <60s). Excluído de Ignore% para preservar signal de comportamento real.

## 📉 Pattern 3 — Thesis decay leaders

_No thesis_health history with decay yet (sistema novo)._

## 🎯 Pattern 4 — Paper trade method performance

| Method | Open | Closed | Win | Loss | Win% | Avg ret% |
|---|---:|---:|---:|---:|---:|---:|
| damodaran_implied_equity_premium | 196 | 0 | 0 | 0 | — | — |
| damodaran_unlevered_beta_quality | 182 | 0 | 0 | 0 | — | — |
| damodaran_auto_geometric_mean_growth | 594 | 0 | 0 | 0 | — | — |
| damodaran_auto_h_model | 98 | 0 | 0 | 0 | — | — |
| damodaran_auto_roe_calculation | 274 | 0 | 0 | 0 | — | — |
| damodaran_auto_valuation_method | 294 | 0 | 0 | 0 | — | — |
| dalio_bubble_4_criteria | 98 | 0 | 0 | 0 | — | — |

> ⚠️ **Sistema novo — quase tudo open. Real intelligence emerge depois de 30+ closed signals/method.**

## 🚨 Pattern 5 — Dominant concerns (latest run only)

> Snapshot da run mais recente por perpetuum (thesis/data_coverage/ri_freshness). Exclui acumulação ao longo do tempo — só sinal actual.

### Top 15 tickers by flag count (latest run, sum across perpetuums)

| Ticker | Total flags |
|---|---:|
| BTLG12 | 5 |
| PRIO3 | 5 |
| IVVB11 | 4 |
| LFTB11 | 4 |
| BRK-B | 3 |
| NU | 3 |
| PLTR | 3 |
| TSLA | 3 |
| AXIA7 | 3 |
| CPLE3 | 3 |
| ALOS3 | 3 |
| B3SA3 | 3 |
| ENGI11 | 3 |
| ITUB4 | 3 |
| EQTL3 | 3 |

### Sectors com mais flags

| Sector | Flags |
|---|---:|
| Utilities | 12 |
| Industrials | 9 |
| Oil & Gas | 7 |
| Financials | 7 |
| Real Estate | 6 |
| Consumer Staples | 6 |
| Logística | 5 |
| Banks | 5 |
| Holding | 5 |
| ETF-US | 4 |

## 💡 Insights actionable

- **BTLG12** lidera com 5 flags na última run — drill-down em thesis/data/RI signals
- **Sector Utilities** concentra 12 flags (latest run) — concentration risk a observar

## 🪞 Auto-crítica do próprio sistema

- Decision journal só fica útil após **30+ days de operação** com action resolutions
- Paper signals win-rate só significant após **30+ closed signals/method**
- Thesis decay dataset é tiny (sistema só corre desde 2026-04-24)
- Pattern detection é honesto sobre amostra pequena
