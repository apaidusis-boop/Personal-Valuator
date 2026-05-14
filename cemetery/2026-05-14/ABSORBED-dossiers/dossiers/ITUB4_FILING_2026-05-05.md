---
type: filing_dossier
ticker: ITUB4
market: br
event_date: 2026-05-05
event_kind: cvm:comunicado
action: SELL
confidence: disputed
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[ITUB4]] · 2026-05-05

**Trigger**: `cvm:comunicado` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516131&numSequencia=1040837&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 40.42

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `20.83` |
| HOLD entre | `20.83` — `28.54` (consensus) |
| TRIM entre | `28.54` — `32.82` |
| **SELL acima de** | `32.82` |

_Método: `br_bank_mult`. Consensus fair = R$28.54. Our fair (mais conservador) = R$20.83._

## 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.21816` | `None` | +100.0% |
| EPS | `4.12` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 102.9B (+53.6% QoQ, -0.4% YoY)
- PDD -24.9B (-47.0% QoQ)
- Lucro líquido 33.7B (+52.5% QoQ, +8.7% YoY)
- Eficiência 43.1% (vs 43.9% prior)

**BS / risco**
- Carteira de crédito 1.0T (+1.0% QoQ)
- Equity 224.7B (+2.9% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-13T18:35:07+00:00 | `br_bank_mult` | 28.54 | 20.83 | 40.42 | SELL | disputed | `filing:cvm:comunicado:2026-05-05` |
| 2026-05-09T13:08:34+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:06+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `post_fix_2026-05-09` |
| 2026-05-09T07:49:04+00:00 | `br_bank_mult` | 27.82 | 20.31 | 41.26 | SELL | disputed | `extend_2026-05-09` |
| 2026-05-08T19:20:37+00:00 | `br_bank_mult` | 27.82 | 20.31 | 40.79 | SELL | disputed | `filing:cvm:fato_relevante:2026-04-14` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._