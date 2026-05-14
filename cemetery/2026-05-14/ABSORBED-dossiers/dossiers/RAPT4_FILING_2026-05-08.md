---
type: filing_dossier
ticker: RAPT4
market: br
event_date: 2026-05-08
event_kind: cvm:comunicado
confidence: disputed
computed_at: 2026-05-13T18:35:08+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[RAPT4]] · 2026-05-08

**Trigger**: `cvm:comunicado` no dia `2026-05-08`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1518456&numSequencia=1043162&numVersao=1>

## 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

## 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `-0.0129700005` | `0.075` | +117.3% |
| EPS | `-0.72` | `None` | +0.0% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 3.4B (+4.4% QoQ, +9.9% YoY)
- EBIT 363.2M (+54.6% QoQ)
- Margem EBIT 10.5% vs 7.1% prior
- Lucro líquido 90.0M (+8302.6% QoQ, -54.1% YoY)

**BS / cash**
- Equity 4.7B (+8.6% QoQ)
- Dívida total 9.3B (+4.1% QoQ)
- FCF proxy 505.0M (+515.8% QoQ)

## 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._