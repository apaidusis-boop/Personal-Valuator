---
type: filing_dossier
ticker: RENT3
market: br
event_date: 2026-05-05
event_kind: cvm:comunicado
action: SELL
confidence: cross_validated
computed_at: 2026-05-13T18:35:08+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[RENT3]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515858&numSequencia=1040564&numVersao=2>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 44.88

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `24.06` |
| HOLD entre | `24.06` — `32.96` (consensus) |
| TRIM entre | `32.96` — `37.90` |
| **SELL acima de** | `37.90` |

_Método: `graham_number`. Consensus fair = R$32.96. Our fair (mais conservador) = R$24.06._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.0853` | `0.0684` | +19.8% |
| EPS | `2.07` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 10.7B (+8.4% QoQ, +10.8% YoY)
- EBIT 1.3B (-34.0% QoQ)
- Margem EBIT 12.4% vs 20.4% prior
- Lucro líquido 258.1M (+253.1% QoQ, -68.2% YoY)

**BS / cash**
- Equity 25.1B (-1.4% QoQ)
- Dívida total 43.9B (+5.7% QoQ)
- FCF proxy -298.6M (-119.3% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `graham_number` | 32.96 | 24.06 | 44.88 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 30.39 | 22.18 | 49.88 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:49+00:00 | `graham_number` | 30.39 | 22.18 | 46.35 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._