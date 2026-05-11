---
type: filing_dossier
ticker: EQTL3
market: br
event_date: 2026-04-30
event_kind: cvm:comunicado
action: SELL
confidence: single_source
computed_at: 2026-05-08T19:20:39+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[EQTL3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513370&numSequencia=1038076&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 42.20

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 22% margem) | `16.40` |
| HOLD entre | `16.40` — `21.03` (consensus) |
| TRIM entre | `21.03` — `24.18` |
| **SELL acima de** | `24.18` |

_Método: `graham_number`. Consensus fair = R$21.03. Our fair (mais conservador) = R$16.40._

## 🔍 Confidence

⚠️ **single_source** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.06985` | `0.1309` | +46.6% |
| EPS | `0.96` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.1B (+10.6% QoQ, +14.4% YoY)
- EBIT 2.4B (-19.3% QoQ)
- Margem EBIT 16.9% vs 23.2% prior
- Lucro líquido 609.8M (-52.7% QoQ, -38.4% YoY)

**BS / cash**
- Equity 32.8B (+2.1% QoQ)
- Dívida total 62.4B (+13.2% QoQ)
- FCF proxy -4.7B (-784.3% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:39+00:00 | `graham_number` | 21.03 | 16.40 | 42.20 | SELL | single_source | `filing:cvm:comunicado:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._