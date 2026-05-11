---
type: filing_dossier
ticker: RENT3
market: br
event_date: 2026-04-29
event_kind: cvm:comunicado
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T19:20:49+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[RENT3]] · 2026-04-29

**Trigger**: `cvm:comunicado` no dia `2026-04-29`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1511170&numSequencia=1035876&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 46.35

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `22.18` |
| HOLD entre | `22.18` — `30.39` (consensus) |
| TRIM entre | `30.39` — `34.95` |
| **SELL acima de** | `34.95` |

_Método: `graham_number`. Consensus fair = R$30.39. Our fair (mais conservador) = R$22.18._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.07211` | `0.0684` | +5.1% |
| EPS | `1.76` | `None` | +0.0% |


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
| 2026-05-08T19:20:49+00:00 | `graham_number` | 30.39 | 22.18 | 46.35 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-29` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._