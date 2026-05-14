---
type: filing_dossier
ticker: ALOS3
market: br
event_date: 2026-04-10
event_kind: cvm:fato_relevante
action: HOLD
confidence: cross_validated
computed_at: 2026-05-08T19:20:35+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ALOS3]] · 2026-04-10

**Trigger**: `cvm:fato_relevante` no dia `2026-04-10`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1503340&numSequencia=1028046&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 30.29

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `27.12` |
| HOLD entre | `27.12` — `31.17` (consensus) |
| TRIM entre | `31.17` — `35.85` |
| **SELL acima de** | `35.85` |

_Método: `graham_number`. Consensus fair = R$31.17. Our fair (mais conservador) = R$27.12._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06744` | `0.061` | +9.5% |
| EPS | `1.64` | `None` | +0.0% |


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
| 2026-05-08T19:20:35+00:00 | `graham_number` | 31.17 | 27.12 | 30.29 | HOLD | cross_validated | `filing:cvm:fato_relevante:2026-04-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._