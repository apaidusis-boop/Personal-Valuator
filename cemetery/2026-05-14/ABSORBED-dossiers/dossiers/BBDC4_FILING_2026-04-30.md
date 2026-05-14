---
type: filing_dossier
ticker: BBDC4
market: br
event_date: 2026-04-30
event_kind: cvm:comunicado
action: HOLD
confidence: cross_validated
computed_at: 2026-05-08T19:20:28+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[BBDC4]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1514205&numSequencia=1038911&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 18.52

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `14.72` |
| HOLD entre | `14.72` — `20.17` (consensus) |
| TRIM entre | `20.17` — `23.19` |
| **SELL acima de** | `23.19` |

_Método: `br_bank_mult`. Consensus fair = R$20.17. Our fair (mais conservador) = R$14.72._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.13754` | `0.1235` | +10.2% |
| EPS | `2.13` | `2.0167` | +5.3% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 56.8B (+45.2% QoQ, +15.9% YoY)
- PDD -21.7B (-45.5% QoQ)
- Lucro líquido 17.4B (+47.1% QoQ, +30.4% YoY)
- Eficiência 37.1% (vs 35.7% prior)

**BS / risco**
- Carteira de crédito 747.8B (+2.3% QoQ)
- Equity 176.1B (+0.9% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `filing:cvm:comunicado:2026-04-30` |
| 2026-05-08T17:48:11+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.52 | HOLD | cross_validated | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `br_bank_mult` | 40.91 | 29.87 | 18.52 | BUY | single_source | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._