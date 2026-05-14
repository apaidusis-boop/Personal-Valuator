---
type: filing_dossier
ticker: ALOS3
market: br
event_date: 2026-05-05
event_kind: cvm:comunicado
action: HOLD
confidence: cross_validated
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ALOS3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516128&numSequencia=1040834&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 29.02

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `27.29` |
| HOLD entre | `27.29` — `31.36` (consensus) |
| TRIM entre | `31.36` — `36.07` |
| **SELL acima de** | `36.07` |

_Método: `graham_number`. Consensus fair = R$31.36. Our fair (mais conservador) = R$27.29._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.068569995` | `0.061` | +11.0% |
| EPS | `1.66` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 678.3M (-2.8% QoQ, +3.2% YoY)
- EBIT 345.8M (+0.1% QoQ)
- Margem EBIT 51.0% vs 49.5% prior
- Lucro líquido 155.9M (-32.2% QoQ, +15.4% YoY)

**BS / cash**
- Equity 14.2B (-0.3% QoQ)
- FCF proxy 400.3M (-41.1% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 31.36 | 27.29 | 29.02 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:05+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:03+00:00 | `graham_number` | 31.36 | 27.29 | 30.35 | HOLD | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:35+00:00 | `graham_number` | 31.17 | 27.12 | 30.29 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._