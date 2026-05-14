---
type: filing_dossier
ticker: MSFT
market: us
event_date: 2019-12-05
event_kind: sec:8-K
action: SELL
confidence: single_source
computed_at: 2026-05-08T22:39:56+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[MSFT]] · 2019-12-05

**Trigger**: `sec:8-K` no dia `2019-12-05`
**Filing URL**: <https://www.sec.gov/Archives/edgar/data/789019/000119312519307138/d840134d8k.htm>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 415.12

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `130.52` |
| HOLD entre | `130.52` — `167.33` (consensus) |
| TRIM entre | `167.33` — `192.43` |
| **SELL acima de** | `192.43` |

_Método: `buffett_ceiling`. Consensus fair = R$167.33. Our fair (mais conservador) = R$130.52._

## 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T22:39:56+00:00 | `buffett_ceiling` | 167.33 | 130.52 | 415.12 | SELL | single_source | `filing:sec:8-K:2019-12-05` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._