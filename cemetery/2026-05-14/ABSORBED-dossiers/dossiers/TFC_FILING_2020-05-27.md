---
type: filing_dossier
ticker: TFC
market: us
event_date: 2020-05-27
event_kind: sec:8-K
action: BUY
confidence: single_source
computed_at: 2026-05-08T22:39:51+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[TFC]] · 2020-05-27

**Trigger**: `sec:8-K` no dia `2020-05-27`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/92230/000119312520153120/d863084d8k.htm>

## 🎯 Acção sugerida

### 🟢 **BUY** &mdash; preço 49.11

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `63.02` |
| HOLD entre | `63.02` — `80.80` (consensus) |
| TRIM entre | `80.80` — `92.92` |
| **SELL acima de** | `92.92` |

_Método: `buffett_ceiling`. Consensus fair = R$80.80. Our fair (mais conservador) = R$63.02._

## 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:51+00:00 | `buffett_ceiling` | 80.80 | 63.02 | 49.11 | BUY | single_source | `filing:sec:8-K:2020-05-27` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._