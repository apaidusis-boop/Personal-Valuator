---
type: filing_dossier
ticker: AXIA7
market: br
event_date: 2026-05-06
event_kind: cvm:fato_relevante
confidence: disputed
computed_at: 2026-05-13T18:35:07+00:00
tags: [filing, fair_value, dossier]
---

# Filing dossier — [[AXIA7]] · 2026-05-06

**Trigger**: `cvm:fato_relevante` no dia `2026-05-06`
**Filing URL**: <https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1517234&numSequencia=1041940&numVersao=1>

## 🎯 Acção sugerida

_Fair value engine devolveu None — fundamentals insuficientes._

## 🔍 Confidence

❌ **disputed** (score=0.00)

| Métrica | yfinance | CVM derivada | Δ |
|---|---|---|---|
| ROE | `0.07862` | `-0.0304` | +138.7% |

> ⚠️ **Methodology gap detected** — fair value emitido a partir de yfinance pode não bater com CVM oficial. Tipicamente: consolidação minority interest (bancos/holdings) ou one-off items (cyclicals). Reler antes de mover capital.

## 📊 Quarter delta

**Filing período**: `2025-09-30` vs prior `2025-06-30` | YoY: `2024-09-30`

**P&L**
- Receita 2.3B (+7.3% QoQ, -59.0% YoY)
- EBIT 850.4M (+10977.8% QoQ)
- Margem EBIT 36.4% vs -0.4% prior
- Lucro líquido 190.5M (+156.1% QoQ, -93.6% YoY)

**BS / cash**
- Equity 33.7B (+0.6% QoQ)
- Dívida total 8.7B (-0.3% QoQ)
- FCF proxy -157.9M (-144.2% QoQ)

## 📈 Fair value history (últimas runs)

_(sem histórico — primeira run)_

---

_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. Engines: `analytics.data_confidence`, `analytics.quarter_delta`, `scoring.fair_value` (com `scoring._safety` per-sector margins)._