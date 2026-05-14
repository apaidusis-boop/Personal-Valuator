---
type: filing_dossier
ticker: TSM
market: us
event_date: 2026-05-12
event_kind: sec:6-K
action: SELL
confidence: single_source
computed_at: 2026-05-13T18:35:08+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[TSM]] · 2026-05-12

**Trigger**: `sec:6-K` no dia `2026-05-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1046179/000104617926000274/tsm-boardx20260512.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 400.60

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `183.46` |
| HOLD entre | `183.46` — `235.20` (consensus) |
| TRIM entre | `235.20` — `270.48` |
| **SELL acima de** | `270.48` |

_Método: `modern_compounder_pe20`. Consensus fair = R$235.20. Our fair (mais conservador) = R$183.46._

## 🔍 Confidence

⚠️ **single_source** (score=0.40)
_(cvm_stale)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `modern_compounder_pe20` | 235.20 | 183.46 | 400.60 | SELL | single_source | `filing:sec:6-K:2026-05-12` |
| 2026-05-13T16:45:14+00:00 | `modern_compounder_pe20` | 235.20 | 183.46 | 400.60 | SELL | single_source | `manual` |
| 2026-05-11T20:40:44+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 404.54 | SELL | single_source | `manual` |
| 2026-05-11T12:53:42+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:19+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `manual` |
| 2026-05-09T20:37:09+00:00 | `modern_compounder_pe20` | 233.80 | 182.36 | 411.68 | SELL | single_source | `manual` |
| 2026-05-09T13:08:36+00:00 | `modern_compounder_pe20` | 232.80 | 181.58 | 411.68 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `buffett_ceiling` | 19.61 | 15.30 | 411.68 | SELL | single_source | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._