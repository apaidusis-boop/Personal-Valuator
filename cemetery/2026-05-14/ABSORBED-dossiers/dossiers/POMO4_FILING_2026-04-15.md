---
type: filing_dossier
ticker: POMO4
market: br
event_date: 2026-04-15
event_kind: cvm:fato_relevante
action: HOLD
confidence: single_source
computed_at: 2026-05-08T19:21:01+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[POMO4]] · 2026-04-15

**Trigger**: `cvm:fato_relevante` no dia `2026-04-15`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1505167&numSequencia=1029873&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 6.37

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 25% margem) | `6.25` |
| HOLD entre | `6.25` — `8.34` (consensus) |
| TRIM entre | `8.34` — `9.59` |
| **SELL acima de** | `9.59` |

_Método: `graham_number`. Consensus fair = R$8.34. Our fair (mais conservador) = R$6.25._

## 🔍 Confidence

⚠️ **single_source** (score=0.30)
_(no_cvm_quarterly_history)_

## 📊 Quarter delta

_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:21:01+00:00 | `graham_number` | 8.34 | 6.25 | 6.37 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-15` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._