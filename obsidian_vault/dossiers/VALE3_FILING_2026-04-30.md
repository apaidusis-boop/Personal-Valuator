---
type: filing_dossier
ticker: VALE3
market: br
event_date: 2026-04-30
event_kind: cvm:comunicado
action: SELL
confidence: disputed
computed_at: 2026-05-08T19:20:28+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[VALE3]] · 2026-04-30

**Trigger**: `cvm:comunicado` no dia `2026-04-30`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1513231&numSequencia=1037937&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 80.07

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `33.24` |
| HOLD entre | `33.24` — `57.31` (consensus) |
| TRIM entre | `57.31` — `65.90` |
| **SELL acima de** | `65.90` |

_Método: `graham_number`. Consensus fair = R$57.31. Our fair (mais conservador) = R$33.24._

## 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.068390004` | `0.1349` | +49.3% |
| EPS | `3.26` | `6.8643` | +52.5% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 56.7B (+13.8% QoQ, +7.0% YoY)
- EBIT 16.1B (+46.4% QoQ)
- Margem EBIT 28.4% vs 22.1% prior
- Lucro líquido 14.7B (+20.4% QoQ, +10.6% YoY)

**BS / cash**
- Equity 224.7B (+1.7% QoQ)
- Dívida total 98.6B (+1.3% QoQ)
- FCF proxy 6.9B (+959.2% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `filing:cvm:comunicado:2026-04-30` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:46+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll2_macro_overlay` |
| 2026-05-08T16:39:50+00:00 | `graham_number` | 57.31 | 33.24 | 80.07 | SELL | disputed | `phase_ll_outlier_median` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | disputed | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:27:07+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | disputed | `phase_ll_3way_outlier` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | single_source | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 90.22 | 52.33 | 80.07 | HOLD | single_source | `phase_ll_dualclass_v2` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._