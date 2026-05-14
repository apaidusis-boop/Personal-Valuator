---
type: filing_dossier
ticker: PRIO3
market: br
event_date: 2026-05-05
event_kind: cvm:fato_relevante
action: SELL
confidence: disputed
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[PRIO3]] · 2026-05-05

**Trigger**: `cvm:fato_relevante` no dia `2026-05-05`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516112&numSequencia=1040818&numVersao=1>

## 🎯 Acção sugerida

### 🔴 **SELL** &mdash; preço 65.26

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 42% margem) | `26.83` |
| HOLD entre | `26.83` — `46.25` (consensus) |
| TRIM entre | `46.25` — `53.19` |
| **SELL acima de** | `53.19` |

_Método: `graham_number`. Consensus fair = R$46.25. Our fair (mais conservador) = R$26.83._

## 🔍 Confidence

❌ **disputed** (score=0.33)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.09729999` | `0.3842` | +74.7% |
| EPS | `3.13` | `12.4488` | +74.9% |

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
| 2026-05-13T18:35:07+00:00 | `graham_number` | 46.25 | 26.83 | 65.26 | SELL | disputed | `filing:cvm:fato_relevante:2026-05-05` |
| 2026-05-13T16:45:13+00:00 | `graham_number` | 46.25 | 26.83 | 65.26 | SELL | disputed | `manual` |
| 2026-05-11T20:40:44+00:00 | `graham_number` | 46.33 | 26.87 | 63.63 | SELL | disputed | `manual` |
| 2026-05-11T12:53:42+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `session:2026-05-11:intangible-gate-fix` |
| 2026-05-10T20:38:19+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `manual` |
| 2026-05-09T20:37:09+00:00 | `graham_number` | 46.33 | 26.87 | 63.27 | SELL | disputed | `manual` |
| 2026-05-09T13:08:35+00:00 | `graham_number` | 46.29 | 26.85 | 63.27 | SELL | disputed | `modern_compounder_2026-05-09` |
| 2026-05-09T12:50:07+00:00 | `graham_number` | 46.29 | 26.85 | 63.27 | SELL | disputed | `post_fix_2026-05-09` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._