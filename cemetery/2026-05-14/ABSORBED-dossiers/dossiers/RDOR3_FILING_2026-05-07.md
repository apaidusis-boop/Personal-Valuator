---
type: filing_dossier
ticker: RDOR3
market: br
event_date: 2026-05-07
event_kind: cvm:comunicado
action: SELL
confidence: cross_validated
computed_at: 2026-05-13T18:35:08+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[RDOR3]] · 2026-05-07

**Trigger**: `cvm:comunicado` no dia `2026-05-07`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517476&numSequencia=1042182&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 35.72

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 18% margem) | `16.65` |
| HOLD entre | `16.65` — `20.31` (consensus) |
| TRIM entre | `20.31` — `23.36` |
| **SELL acima de** | `23.36` |

_Método: `graham_number`. Consensus fair = R$20.31. Our fair (mais conservador) = R$16.65._

## 🔍 Confidence

✅ **cross_validated** (score=1.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.19188` | `0.1654` | +13.8% |
| EPS | `2.09` | `None` | +0.0% |


## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 14.4B (+3.3% QoQ, +10.7% YoY)
- EBIT 2.7B (+21.0% QoQ)
- Margem EBIT 19.1% vs 16.3% prior
- Lucro líquido 1.5B (+46.8% QoQ, +31.6% YoY)

**BS / cash**
- Equity 28.8B (+3.2% QoQ)
- Dívida total 42.9B (+12.9% QoQ)
- FCF proxy -4.2B (-105.0% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:08+00:00 | `graham_number` | 20.31 | 16.65 | 35.72 | SELL | cross_validated | `filing:cvm:comunicado:2026-05-07` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `post_fix_2026-05-09` |
| 2026-05-09T07:49:05+00:00 | `graham_number` | 20.31 | 16.65 | 38.31 | SELL | cross_validated | `extend_2026-05-09` |
| 2026-05-08T19:20:48+00:00 | `graham_number` | 20.31 | 16.65 | 37.74 | SELL | cross_validated | `filing:cvm:comunicado:2026-04-16` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._