---
type: filing_dossier
ticker: CPLE3
market: br
event_date: 2026-04-22
event_kind: cvm:comunicado
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T19:20:33+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[CPLE3]] · 2026-04-22

**Trigger**: `cvm:comunicado` no dia `2026-04-22`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1506999&numSequencia=1031705&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 15.29

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `9.85` |
| HOLD entre | `9.85` — `12.63` (consensus) |
| TRIM entre | `12.63` — `14.52` |
| **SELL acima de** | `14.52` |

_Método: `graham_number`. Consensus fair = R$12.63. Our fair (mais conservador) = R$9.85._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.10787` | `0.085` | +21.2% |
| EPS | `0.91` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 6.8B (+9.4% QoQ, +18.8% YoY)
- EBIT 982.2M (-19.6% QoQ)
- Margem EBIT 14.4% vs 19.6% prior
- Lucro líquido 383.1M (-33.2% QoQ, -68.5% YoY)

**BS / cash**
- Equity 25.9B (+1.5% QoQ)
- Dívida total 20.9B (+5.2% QoQ)
- FCF proxy 269.3M (+122.2% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:33+00:00 | `graham_number` | 12.63 | 9.85 | 15.29 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-22` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._