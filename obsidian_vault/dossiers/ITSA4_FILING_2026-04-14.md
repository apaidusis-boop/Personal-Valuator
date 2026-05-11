---
type: filing_dossier
ticker: ITSA4
market: br
event_date: 2026-04-14
event_kind: cvm:fato_relevante
action: HOLD
confidence: cross_validated
computed_at: 2026-05-08T19:20:28+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ITSA4]] · 2026-04-14

**Trigger**: `cvm:fato_relevante` no dia `2026-04-14`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504583&numSequencia=1029289&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 13.30

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `12.99` |
| HOLD entre | `12.99` — `16.66` (consensus) |
| TRIM entre | `16.66` — `19.15` |
| **SELL acima de** | `19.15` |

_Método: `graham_number`. Consensus fair = R$16.66. Our fair (mais conservador) = R$12.99._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.17571` | `0.1701` | +3.2% |
| EPS | `1.48` | `1.4272` | +3.6% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.1B (+0.3% QoQ, -5.0% YoY)
- EBIT 4.7B (+6.5% QoQ)
- Margem EBIT 2.2 vs 2.1 prior
- Lucro líquido 4.2B (+3.0% QoQ, +8.8% YoY)

**BS / cash**
- Equity 96.9B (+3.0% QoQ)
- Dívida total 9.7B (-15.3% QoQ)
- FCF proxy 2.7B (+4639.3% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-14` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `graham_number` | 16.66 | 12.99 | 13.30 | HOLD | cross_validated | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `graham_number` | 25.38 | 19.80 | 13.30 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._