---
type: filing_dossier
ticker: PRIO3
market: br
event_date: 2026-04-13
event_kind: cvm:comunicado
action: SELL
confidence: disputed
computed_at: 2026-05-08T19:20:28+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PRIO3]] · 2026-04-13

**Trigger**: `cvm:comunicado` no dia `2026-04-13`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1504379&numSequencia=1029085&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 64.40

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `26.85` |
| HOLD entre | `26.85` — `46.29` (consensus) |
| TRIM entre | `46.29` — `53.24` |
| **SELL acima de** | `53.24` |

_Método: `graham_number`. Consensus fair = R$46.29. Our fair (mais conservador) = R$26.85._

## 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.09729999` | `0.3842` | +74.7% |
| EPS | `3.14` | `12.4488` | +74.8% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.6B (+7.1% QoQ, -0.4% YoY)
- EBIT 602.1M (+674.9% QoQ)
- Margem EBIT 16.9% vs 2.3% prior
- Lucro líquido 348.7M (-48.8% QoQ, -58.0% YoY)

**BS / cash**
- Equity 25.9B (-0.9% QoQ)
- Dívida total 27.3B (+18.6% QoQ)
- FCF proxy 32.8M (+121.2% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T19:20:28+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `filing:cvm:comunicado:2026-04-13` |
| 2026-05-08T17:48:12+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `phase_ll_full_run_validation` |
| 2026-05-08T16:46:45+00:00 | `graham_number` | 46.29 | 26.85 | 64.40 | SELL | disputed | `phase_ll2_macro_overlay` |
| 2026-05-08T16:38:11+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | SELL | disputed | `phase_ll_sec_xbrl_live` |
| 2026-05-08T15:09:06+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | SELL | disputed | `phase_ll_full_v3` |
| 2026-05-08T15:06:19+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_dualclass_v2` |
| 2026-05-08T15:06:02+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_dualclass_fixed` |
| 2026-05-08T14:25:04+00:00 | `graham_number` | 94.88 | 55.03 | 64.40 | HOLD | disputed | `phase_ll_full_pipeline` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._