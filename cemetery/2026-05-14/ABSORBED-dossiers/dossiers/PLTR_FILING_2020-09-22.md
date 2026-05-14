---
type: filing_dossier
ticker: PLTR
market: us
event_date: 2020-09-22
event_kind: sec:8-K
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T22:39:51+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PLTR]] · 2020-09-22

**Trigger**: `sec:8-K` no dia `2020-09-22`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1321655/000119312520251414/d11024d8k.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 137.80

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `7.71` |
| HOLD entre | `7.71` — `9.88` (consensus) |
| TRIM entre | `9.88` — `11.36` |
| **SELL acima de** | `11.36` |

_Método: `buffett_ceiling`. Consensus fair = R$9.88. Our fair (mais conservador) = R$7.71._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.32587` | `0.3219` | +1.2% |
| EPS | `0.89` | `0.8894` | +0.1% |


## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 9.88 | 7.71 | 137.80 | SELL | cross_validated | `filing:sec:8-K:2020-09-22` |
| 2026-05-08T20:37:29+00:00 | `buffett_ceiling` | 9.88 | 7.71 | 137.80 | SELL | cross_validated | `manual` |
| 2026-05-08T17:48:12+00:00 | `buffett_ceiling` | 9.88 | 7.71 | 133.79 | SELL | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 9.88 | 7.71 | 133.79 | SELL | single_source | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 9.88 | 7.71 | 133.79 | SELL | single_source | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 9.27 | 7.23 | 133.79 | SELL | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 9.27 | 7.23 | 133.79 | SELL | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 9.27 | 7.23 | 133.79 | SELL | single_source | `phase_ll_dualclass_fixed` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._