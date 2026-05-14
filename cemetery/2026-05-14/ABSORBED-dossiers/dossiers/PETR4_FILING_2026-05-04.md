---
type: filing_dossier
ticker: PETR4
market: br
event_date: 2026-05-04
event_kind: cvm:comunicado
action: HOLD
confidence: cross_validated
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PETR4]] · 2026-05-04

**Trigger**: `cvm:comunicado` no dia `2026-05-04`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1515529&numSequencia=1040235&numVersao=1>

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 45.17

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `42.96` |
| HOLD entre | `42.96` — `74.08` (consensus) |
| TRIM entre | `74.08` — `85.19` |
| **SELL acima de** | `85.19` |

_Método: `graham_number`. Consensus fair = R$74.08. Our fair (mais conservador) = R$42.96._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.25601` | `0.196` | +23.5% |
| EPS | `7.56` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 127.9B (+7.4% QoQ, -1.3% YoY)
- EBIT 43.6B (+43.2% QoQ)
- Margem EBIT 34.1% vs 25.6% prior
- Lucro líquido 32.8B (+22.7% QoQ, +0.5% YoY)

**BS / cash**
- Equity 425.0B (+5.8% QoQ)
- Dívida total 376.1B (+1.2% QoQ)
- FCF proxy 27.7B (-0.5% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `graham_number` | 74.08 | 42.96 | 45.17 | HOLD | cross_validated | `filing:cvm:comunicado:2026-05-04` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 73.83 | 42.82 | 45.67 | HOLD | single_source | `extend_2026-05-09` |
| 2026-05-08T19:20:28+00:00 | `graham_number` | 73.73 | 42.77 | 46.22 | HOLD | single_source | `filing:cvm:fato_relevante:2026-04-30` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._