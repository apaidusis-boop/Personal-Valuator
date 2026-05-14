---
type: decision_journal_intelligence
date: 2026-04-25
tags: [decision_journal, meta, autocrítica, patterns]
---

# 🧠 Decision Journal Intelligence

> Pattern mining em past decisions, actions, paper signals, e thesis decay. 100% local SQL.

## 🔁 Pattern 1+2 — Action resolution patterns

| Kind | n | Open | Resolved | Ignored | Ignore% | Avg days |
|---|---:|---:|---:|---:|---:|---:|
| dy_above_pct | 4 | 4 | 0 | 0 | 0.0% | — |
| altman_distress | 4 | 4 | 0 | 0 | 0.0% | — |
| piotroski_weak | 4 | 4 | 0 | 0 | 0.0% | — |
| perpetuum:data_coverage | 3 | 2 | 1 | 0 | 0.0% | — |
| perpetuum:vault | 4 | 4 | 0 | 0 | 0.0% | — |
| dy_percentile_vs_own_history | 2 | 2 | 0 | 0 | 0.0% | — |

## 📉 Pattern 3 — Thesis decay leaders

_No thesis_health history with decay yet (sistema novo)._

## 🎯 Pattern 4 — Paper trade method performance

| Method | Open | Closed | Win | Loss | Win% | Avg ret% |
|---|---:|---:|---:|---:|---:|---:|
| damodaran_implied_equity_premium | 132 | 0 | 0 | 0 | — | — |
| damodaran_unlevered_beta_quality | 108 | 0 | 0 | 0 | — | — |
| damodaran_auto_geometric_mean_growth | 296 | 0 | 0 | 0 | — | — |
| damodaran_auto_h_model | 46 | 0 | 0 | 0 | — | — |
| damodaran_auto_roe_calculation | 138 | 0 | 0 | 0 | — | — |
| damodaran_auto_valuation_method | 144 | 0 | 0 | 0 | — | — |
| dalio_bubble_4_criteria | 68 | 0 | 0 | 0 | — | — |

> ⚠️ **Sistema novo — quase tudo open. Real intelligence emerge depois de 30+ closed signals/method.**

## 🚨 Pattern 5 — Dominant concerns (most-flagged)

### Top 15 tickers by flag count (perpetuums)

| Ticker | Total flags |
|---|---:|
| PRIO3 | 5 |
| IVVB11 | 4 |
| LFTB11 | 4 |
| NU | 4 |
| PLTR | 4 |
| TSLA | 4 |
| KLBN11 | 3 |
| BRK-B | 3 |
| TSM | 3 |
| PVBI11 | 2 |
| RBRX11 | 2 |
| VGIR11 | 2 |
| XPML11 | 2 |
| GREK | 2 |
| AAPL | 2 |

### Sectors com mais flags

| Sector | Flags |
|---|---:|
| Technology | 11 |
| Financials | 9 |
| Oil & Gas | 6 |
| ETF-US | 4 |
| ETF-RF | 4 |
| Holding | 4 |
| Consumer Disc. | 4 |
| Materials | 3 |
| Corporativo | 2 |
| Híbrido | 2 |

## 💡 Insights actionable

- **Sector Technology** concentra 11 flags — concentration risk a observar

## 🪞 Auto-crítica do próprio sistema

- Decision journal só fica útil após **30+ days de operação** com action resolutions
- Paper signals win-rate só significant após **30+ closed signals/method**
- Thesis decay dataset é tiny (sistema só corre desde 2026-04-24)
- Pattern detection é honesto sobre amostra pequena
