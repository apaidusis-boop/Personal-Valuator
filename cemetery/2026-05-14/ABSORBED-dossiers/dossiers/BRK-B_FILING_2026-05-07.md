---
type: filing_dossier
ticker: BRK-B
market: us
event_date: 2026-05-07
event_kind: sec:8-K
action: HOLD
confidence: disputed
computed_at: 2026-05-08T19:21:01+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[BRK-B]] · 2026-05-07

**Trigger**: `sec:8-K` no dia `2026-05-07`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1067983/000119312526212148/d74313d8k.htm>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 469.83

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `524.32` |
| HOLD entre | `524.32` — `672.20` (consensus) |
| TRIM entre | `672.20` — `773.03` |
| **SELL acima de** | `773.03` |

_Método: `buffett_ceiling`. Consensus fair = R$672.20. Our fair (mais conservador) = R$524.32._

## 🔍 Confidence

❌ **disputed** (score=0.50)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.10499` | `0.1036` | +1.3% |
| EPS | `33.61` | `51827.6123` | +99.9% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | HOLD | disputed | `filing:sec:8-K:2026-05-07` |
| 2026-05-08T17:48:11+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | HOLD | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 672.20 | 524.32 | 469.83 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._