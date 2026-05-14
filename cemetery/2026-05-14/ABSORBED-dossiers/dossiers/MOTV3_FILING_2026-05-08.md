---
type: filing_dossier
ticker: MOTV3
market: br
event_date: 2026-05-08
event_kind: cvm:fato_relevante
action: SELL
confidence: cross_validated
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[MOTV3]] · 2026-05-08

**Trigger**: `cvm:fato_relevante` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1519199&numSequencia=1043905&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 15.19

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `11.97` |
| HOLD entre | `11.97` — `16.39` (consensus) |
| TRIM entre | `16.39` — `18.85` |
| **SELL acima de** | `18.85` |

_Método: `graham_number`. Consensus fair = R$16.39. Our fair (mais conservador) = R$11.97._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20401` | `0.2066` | +1.3% |
| EPS | `1.47` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.3B (+36.1% QoQ, +13.6% YoY)
- EBIT 3.1B (+86.8% QoQ)
- Margem EBIT 48.5% vs 35.4% prior
- Lucro líquido 1.4B (+60.5% QoQ, +209.6% YoY)

**BS / cash**
- Equity 16.1B (+6.9% QoQ)
- Dívida total 40.3B (+3.3% QoQ)
- FCF proxy 1.1B (+227.6% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 16.39 | 11.97 | 15.19 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-05-08` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `graham_number` | 16.39 | 11.97 | 15.87 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:40+00:00 | `graham_number` | 16.39 | 11.97 | 15.67 | SELL | cross_validated | `filing:cvm:fato_relevante:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._