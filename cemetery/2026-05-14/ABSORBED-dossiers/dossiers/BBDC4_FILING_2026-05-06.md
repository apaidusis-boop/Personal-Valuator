---
type: filing_dossier
ticker: BBDC4
market: br
event_date: 2026-05-06
event_kind: cvm:comunicado
action: HOLD
confidence: cross_validated
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[BBDC4]] · 2026-05-06

**Trigger**: `cvm:comunicado` no dia `2026-05-06`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517345&numSequencia=1042051&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 18.21

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
| ROE | `0.13366` | `0.1235` | +7.6% |
| EPS | `2.1` | `2.0167` | +4.0% |


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
| 2026-05-13T18:35:07+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.21 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-06` |
| 2026-05-13T16:45:13+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.21 | HOLD | cross_validated | `manual` |
| 2026-05-11T20:40:44+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.09 | HOLD | cross_validated | `manual` |
| 2026-05-11T12:53:42+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:18+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `manual` |
| 2026-05-09T20:37:09+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `manual` |
| 2026-05-09T13:08:34+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:05+00:00 | `br_bank_mult` | 20.17 | 14.72 | 18.59 | HOLD | cross_validated | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._