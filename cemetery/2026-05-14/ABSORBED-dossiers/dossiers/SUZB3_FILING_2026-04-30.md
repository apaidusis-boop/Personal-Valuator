---
type: filing_dossier
ticker: SUZB3
market: br
event_date: 2026-04-30
event_kind: cvm:comunicado
action: SELL
confidence: single_source
computed_at: 2026-05-08T19:20:59+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[SUZB3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1511860&numSequencia=1036566&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 43.30

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 38% margem) | `53.08` |
| HOLD entre | `53.08` — `85.62` (consensus) |
| TRIM entre | `85.62` — `98.46` |
| **SELL acima de** | `98.46` |

_Método: `graham_number`. Consensus fair = R$85.62. Our fair (mais conservador) = R$53.08._

## 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.26295` | `0.1652` | +37.2% |
| EPS | `9.19` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 12.2B (-8.6% QoQ, -1.0% YoY)
- EBIT 2.0B (-31.5% QoQ)
- Margem EBIT 16.2% vs 21.6% prior
- Lucro líquido 2.0B (-60.9% QoQ, -39.4% YoY)

**BS / cash**
- Equity 45.3B (+4.6% QoQ)
- Dívida total 93.0B (+1.5% QoQ)
- FCF proxy 762.1M (+247.6% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:59+00:00 | `graham_number` | 85.62 | 53.08 | 43.30 | SELL | single_source | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._