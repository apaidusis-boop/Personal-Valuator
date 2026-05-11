---
type: glossary
slug: DCF
title: DCF — Discounted Cash Flow
category: valuation
date: 2026-05-10
tags: [glossary, tutor, valuation]
---

# 📖 DCF — Discounted Cash Flow

> Categoria: **valuation**. Cross-links: [[CONSTITUTION]] · [[Glossary/_Index]]

## Fórmula

`Σ FCF_t / (1+WACC)^t + Terminal Value / (1+WACC)^N`

## Leitura

**Método de avaliação intrinsic** (Damodaran framework). Projecta FCF futuros + terminal value, desconta a presente value via WACC. Mais teórico que prático — sensible a assumptions.

## Thresholds

- **margin_safety**: Preço actual ≤ 70% do DCF = entrada Graham-style
- **sensitivity**: Sempre fazer ±2% no growth + ±1% no WACC para range
- **terminal**: Terminal value tipicamente 60-80% do DCF total — fragil

## Bom vs Mau

**DCF útil** para empresas estáveis com previsibilidade (Coca-Cola, JNJ). **DCF inútil** para growth high-uncertainty, cyclical, financials, REITs (use NAV/AFFO).

## Contraméricas (quando o sinal falha)

❌ Garbage in, garbage out — assumptions de growth + WACC dominam resultado.
❌ Terminal value > 60% do DCF = essencialmente apostando em perpetuidade.
❌ Buffett: 'preferir empresa boa a preço justo do que empresa medíocre a preço barato' — DCF muito sensível ignora isto.

---
*Auto-build via `scripts/build_glossary.py` em 2026-05-10.*
