---
type: filing_dossier
ticker: JPM
market: us
event_date: 2026-05-07
event_kind: sec:8-K
action: HOLD
confidence: cross_validated
computed_at: 2026-05-08T19:21:01+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[JPM]] · 2026-05-07

**Trigger**: `sec:8-K` no dia `2026-05-07`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/19617/000119312526211978/d903351d8k.htm>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 314.90

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `306.26` |
| HOLD entre | `306.26` — `392.63` (consensus) |
| TRIM entre | `392.63` — `451.53` |
| **SELL acima de** | `451.53` |

_Método: `buffett_ceiling`. Consensus fair = R$392.63. Our fair (mais conservador) = R$306.26._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.16465001` | `0.1639` | +0.4% |
| EPS | `20.88` | `21.1753` | +1.4% |


## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `filing:sec:8-K:2026-05-07` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 392.63 | 306.26 | 314.90 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 385.14 | 300.41 | 314.90 | HOLD | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._