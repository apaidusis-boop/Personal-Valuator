---
type: filing_dossier
ticker: TTD
market: us
event_date: 2026-05-08
event_kind: sec:8-K
action: SELL
confidence: single_source
computed_at: 2026-05-08T19:21:01+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[TTD]] · 2026-05-08

**Trigger**: `sec:8-K` no dia `2026-05-08`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/1671933/000167193326000055/ttd-20260504.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 24.01

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `11.74` |
| HOLD entre | `11.74` — `15.66` (consensus) |
| TRIM entre | `15.66` — `18.01` |
| **SELL acima de** | `18.01` |

_Método: `buffett_ceiling`. Consensus fair = R$15.66. Our fair (mais conservador) = R$11.74._

## 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `buffett_ceiling` | 15.66 | 11.74 | 24.01 | SELL | single_source | `filing:sec:8-K:2026-05-08` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._