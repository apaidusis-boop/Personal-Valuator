---
type: filing_dossier
ticker: IBM
market: us
event_date: 2019-11-12
event_kind: sec:8-K
action: SELL
confidence: single_source
computed_at: 2026-05-08T22:39:57+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[IBM]] · 2019-11-12

**Trigger**: `sec:8-K` no dia `2019-11-12`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/51143/000110465919062171/tm1922448d1_8k.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 229.76

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `82.09` |
| HOLD entre | `82.09` — `105.25` (consensus) |
| TRIM entre | `105.25` — `121.04` |
| **SELL acima de** | `121.04` |

_Método: `buffett_ceiling`. Consensus fair = R$105.25. Our fair (mais conservador) = R$82.09._

## 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:57+00:00 | `buffett_ceiling` | 105.25 | 82.09 | 229.76 | SELL | single_source | `filing:sec:8-K:2019-11-12` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._