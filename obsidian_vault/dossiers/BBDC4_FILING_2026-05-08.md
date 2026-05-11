---
type: filing_dossier
ticker: BBDC4
market: br
event_date: 2026-05-08
event_kind: manual
action: HOLD
confidence: disputed
computed_at: 2026-05-08T13:34:56+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[BBDC4]] · 2026-05-08

**Trigger**: `manual` no dia `2026-05-08`

## 🎯 Acção sugerida

### 🟡 **HOLD** &mdash; preço 18.52

| Banda | Preço |
|---|---|
| **BUY abaixo de** (our_fair, 27% margem) | `15.55` |
| HOLD entre | `15.55` — `21.30` (consensus) |
| TRIM entre | `21.30` — `24.50` |
| **SELL acima de** | `24.50` |

_Método: `br_bank_mult`. Consensus fair = R$21.30. Our fair (mais conservador) = R$15.55._

## 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.13754` | `0.0516` | +62.5% |
| EPS | `2.13` | `4.0913` | +47.9% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- NII 56.8B (+45.2% QoQ, +15.9% YoY)
- PDD -21.7B (-45.5% QoQ)
- Lucro líquido 17.4B (+47.1% QoQ, +30.4% YoY)
- Eficiência 37.1% (vs 35.7% prior)

**BS / risco**
- Carteira de crédito 747.8B (+2.3% QoQ)
- CET1 11.39% (vs 11.06% prior)
- Equity 176.1B (+0.9% QoQ)

## 📈 Fair value history (últimas runs)

| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |
|---|---|---|---|---|---|---|---|
| 2026-05-08T13:34:56+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual:dossier` |
| 2026-05-08T13:34:47+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual:dossier` |
| 2026-05-08T13:34:26+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `manual` |
| 2026-05-08T13:21:27+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | disputed | `smoke_v3_with_confidence` |
| 2026-05-08T13:16:03+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | single_source | `smoke_v2_run2` |
| 2026-05-08T13:15:45+00:00 | `br_bank_mult` | 21.30 | 15.55 | 18.52 | HOLD | single_source | `smoke_v2` |
| 2026-05-07 | `br_bank_mult` | 21.30 | — | 19.27 | — | — | `—` |

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._