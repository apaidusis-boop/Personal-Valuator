# Research Memo — KLBN4 2026-04-22

```
==============================================================================
  RESEARCH MEMO — KLBN4  (KLBN4)
  Gerado: 2026-04-22   Mercado: BR   Sector: -
==============================================================================

  VEREDITO: ✗ AVOID   Confiança: 85%
    • Altman Z=1.07 < 1.81 (distress zone) → veto estrutural

[1] IDENTIFICAÇÃO & PREÇO
------------------------------------------------------------------------------
  Preço actual ............: R$3.76  (2026-04-20)
  DY t12m .................: 8.70%  (div t12m R$0.3272/share)
  DY vs own 10y ...........: P88  [CHEAP]  (25 obs mensais) — entry-timing, NÃO stock-picker

[2] SCREEN VERDICT (Buffett/Graham sector-aware)
------------------------------------------------------------------------------
  Score composto ..........: 0.60  →  ≈ NEAR
    ✓  graham_number               5.767  (threshold 3.759999990463257)
    ✓  dividend_yield              0.087  (threshold 0.06)
    ✗  roe                         0.146  (threshold 0.15)
    ✗  net_debt_ebitda             3.804  (threshold 3.0)
    ✓  dividend_streak              16.0  (threshold 5)

[3] QUALITY COMPOSITE (Altman + Piotroski)
------------------------------------------------------------------------------
  Altman Z-Score ..........: +1.066  →  ✗ DISTRESS  (confiança high)
    X1 WC/TA=+0.145  X2 RE/TA=+0.000  X3 EBIT/TA=+0.087  X4 MC/TL=+0.468  X5 Rev/TA=+0.324
  Piotroski F-Score .......: 5/9  →  ◦ NEUTRAL  (2025-12-31 vs 2024-12-31)
    passou: roa_positive, fcf_positive, fcf_gt_netincome, leverage_not_up, liquidity_up
    falhou: delta_roa_positive, no_dilution, margin_up, turnover_up

[4] DIVIDEND SAFETY
------------------------------------------------------------------------------
  Safety score ............: 40/100  →  RISK

[5] DRIP FORWARD — cenário Base (apenas contexto, não forecast)
------------------------------------------------------------------------------
  g (div growth base) .....: +18.00%/y
  md (multiple drift) .....: +0.00%/y
  TR fwd base (DY+g+md) ...: +26.70%/y
  kind ....................: equity

[7] REGIME MACRO
------------------------------------------------------------------------------
  BR: expansion (conf low) — sinais mistos — default expansion
  NOTA: classifier é descritivo, não timing signal (ver Phase H null).

==============================================================================
  Fontes: deep_fundamentals, scores, prices, dividends, series (FRED/BCB), thesis_book, dy_percentile
  Memo determinístico — sem LLM. Regras em scripts/research.py::_final_verdict.
==============================================================================
```
