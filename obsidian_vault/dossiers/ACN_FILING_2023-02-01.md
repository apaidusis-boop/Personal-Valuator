---
type: filing_dossier
ticker: ACN
market: us
event_date: 2023-02-01
event_kind: sec:8-K
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T22:39:51+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ACN]] · 2023-02-01

**Trigger**: `sec:8-K` no dia `2023-02-01`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1467373/000146737323000071/acn-20230201.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 180.42

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `115.48` |
| HOLD entre | `115.48` — `148.05` (consensus) |
| TRIM entre | `148.05` — `170.26` |
| **SELL acima de** | `170.26` |

_Método: `buffett_ceiling`. Consensus fair = R$148.05. Our fair (mais conservador) = R$115.48._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.24763` | `0.2471` | +0.2% |
| EPS | `12.2` | `12.0934` | +0.9% |


## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 180.42 | SELL | cross_validated | `filing:sec:8-K:2023-02-01` |
| 2026-05-08T20:37:29+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 180.42 | SELL | cross_validated | `manual` |
| 2026-05-08T17:48:11+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `buffett_ceiling` | 148.05 | 115.48 | 174.57 | SELL | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `buffett_ceiling` | 152.29 | 118.78 | 174.57 | TRIM | single_source | `phase_ll_dualclass_fixed` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._