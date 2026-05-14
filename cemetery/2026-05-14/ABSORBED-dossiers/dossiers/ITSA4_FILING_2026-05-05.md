---
type: filing_dossier
ticker: ITSA4
market: br
event_date: 2026-05-05
event_kind: cvm:comunicado
action: HOLD
confidence: cross_validated
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ITSA4]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516131&numSequencia=1040837&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 13.10

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
| EPS | `1.52` | `1.4272` | +6.1% |


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
| 2026-05-13T18:35:07+00:00 | `graham_number` | 16.66 | 12.99 | 13.10 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-13T16:45:13+00:00 | `graham_number` | 16.66 | 12.99 | 13.10 | HOLD | cross_validated | `manual` |
| 2026-05-11T20:40:44+00:00 | `graham_number` | 16.66 | 12.99 | 13.25 | HOLD | cross_validated | `manual` |
| 2026-05-11T12:53:42+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:18+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `manual` |
| 2026-05-09T20:37:09+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `manual` |
| 2026-05-09T13:08:34+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 16.66 | 12.99 | 13.50 | HOLD | cross_validated | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._