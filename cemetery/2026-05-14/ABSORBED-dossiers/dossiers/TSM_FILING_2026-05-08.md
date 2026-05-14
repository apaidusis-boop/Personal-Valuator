---
type: filing_dossier
ticker: TSM
market: us
event_date: 2026-05-08
event_kind: sec:6-K
action: SELL
confidence: single_source
computed_at: 2026-05-08T19:21:03+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[TSM]] · 2026-05-08

**Trigger**: `sec:6-K` no dia `2026-05-08`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1046179/000104617926000213/tsm-revenue20260508.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 419.50

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `10.55` |
| HOLD entre | `10.55` — `13.52` (consensus) |
| TRIM entre | `13.52` — `15.55` |
| **SELL acima de** | `15.55` |

_Método: `buffett_ceiling`. Consensus fair = R$13.52. Our fair (mais conservador) = R$10.55._

## 🔍 Confidence

⚠️ **single_source** (score=0.40)
_(cvm_stale)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:03+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `filing:sec:6-K:2026-05-08` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:46+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `buffett_ceiling` | 13.52 | 10.55 | 419.50 | SELL | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._