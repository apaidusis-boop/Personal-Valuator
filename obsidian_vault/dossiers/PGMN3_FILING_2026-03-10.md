---
type: filing_dossier
ticker: PGMN3
market: br
event_date: 2026-03-10
event_kind: cvm:fato_relevante
action: STRONG_BUY
confidence: cross_validated
computed_at: 2026-05-08T19:20:44+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PGMN3]] · 2026-03-10

**Trigger**: `cvm:fato_relevante` no dia `2026-03-10`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1488644&numSequencia=1013350&numVersao=1>

## 🎯 Acção sugerida

### 🟢🟢 **STRONG_BUY** &mdash; preço 5.01

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `5.89` |
| HOLD entre | `5.89` — `7.18` (consensus) |
| TRIM entre | `7.18` — `8.26` |
| **SELL acima de** | `8.26` |

_Método: `graham_number`. Consensus fair = R$7.18. Our fair (mais conservador) = R$5.89._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.089729995` | `0.0714` | +20.5% |
| EPS | `0.49` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.9B (+4.3% QoQ, +17.8% YoY)
- EBIT 251.0M (+9.3% QoQ)
- Margem EBIT 6.5% vs 6.2% prior
- Lucro líquido 76.0M (+50.9% QoQ, +85.5% YoY)

**BS / cash**
- Equity 2.9B (+2.6% QoQ)
- Dívida total 1.7B (+2.8% QoQ)
- FCF proxy -40.9M (+66.8% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:44+00:00 | `graham_number` | 7.18 | 5.89 | 5.01 | STRONG_BUY | cross_validated | `filing:cvm:fato_relevante:2026-03-10` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._