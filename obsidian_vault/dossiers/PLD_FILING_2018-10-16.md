---
type: filing_dossier
ticker: PLD
market: us
event_date: 2018-10-16
event_kind: sec:8-K
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T22:39:51+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PLD]] · 2018-10-16

**Trigger**: `sec:8-K` no dia `2018-10-16`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1045609/000156459018024299/pld-8k_20181016.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 144.09

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 16% margem) | `93.94` |
| HOLD entre | `93.94` — `111.83` (consensus) |
| TRIM entre | `111.83` — `128.61` |
| **SELL acima de** | `128.61` |

_Método: `reit_pb_proxy`. Consensus fair = R$111.83. Our fair (mais conservador) = R$93.94._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06844` | `0.0696` | +1.7% |
| EPS | `3.98` | `3.885` | +2.4% |


## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `reit_pb_proxy` | 111.83 | 93.94 | 144.09 | SELL | cross_validated | `filing:sec:8-K:2018-10-16` |
| 2026-05-08T20:37:29+00:00 | `reit_pb_proxy` | 111.83 | 93.94 | 144.09 | SELL | cross_validated | `manual` |
| 2026-05-08T17:48:12+00:00 | `reit_pb_proxy` | 111.83 | 93.94 | 142.90 | SELL | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `reit_pb_proxy` | 111.83 | 93.94 | 142.90 | SELL | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `reit_pb_proxy` | 111.83 | 93.94 | 142.90 | SELL | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `reit_pb_proxy` | 114.91 | 96.52 | 142.90 | SELL | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `reit_pb_proxy` | 114.91 | 96.52 | 142.90 | SELL | single_source | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `reit_pb_proxy` | 114.91 | 96.52 | 142.90 | SELL | single_source | `phase_ll_dualclass_fixed` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._