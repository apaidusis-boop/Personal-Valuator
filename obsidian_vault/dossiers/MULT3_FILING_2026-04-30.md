---
type: filing_dossier
ticker: MULT3
market: br
event_date: 2026-04-30
event_kind: cvm:comunicado
action: SELL
confidence: cross_validated
computed_at: 2026-05-08T19:20:42+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[MULT3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513707&numSequencia=1038413&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 31.41

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 13% margem) | `23.27` |
| HOLD entre | `23.27` — `26.75` (consensus) |
| TRIM entre | `26.75` — `30.76` |
| **SELL acima de** | `30.76` |

_Método: `graham_number`. Consensus fair = R$26.75. Our fair (mais conservador) = R$23.27._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.20018` | `0.2114` | +5.3% |
| EPS | `2.47` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 617.5M (-11.0% QoQ, +13.3% YoY)
- EBIT 403.7M (-5.4% QoQ)
- Margem EBIT 65.4% vs 61.5% prior
- Lucro líquido 221.2M (-16.4% QoQ, -20.9% YoY)

**BS / cash**
- Equity 6.0B (+1.9% QoQ)
- Dívida total 5.5B (+7.1% QoQ)
- FCF proxy -92.8M (-113.1% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:42+00:00 | `graham_number` | 26.75 | 23.27 | 31.41 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._