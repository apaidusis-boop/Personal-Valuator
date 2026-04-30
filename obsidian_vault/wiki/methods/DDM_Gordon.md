---
type: method
name: Dividend Discount Model (Gordon Growth)
category: valuation
author: Myron J. Gordon
year: 1959
tags: [method, valuation, ddm, gordon, dividend, drip]
applies_to: [dividend_paying, mature]
related: ["[[DCF_simplified]]", "[[Dividend_Safety]]", "[[DRIP_compounding]]", "[[Aristocrats_Kings]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Dividend Discount Model (Gordon)

## Fórmula

$$
P_0 = \frac{D_1}{r - g}
$$

- **P₀**: fair value por acção hoje
- **D₁**: dividendo esperado próximo ano
- **r**: required rate of return
- **g**: growth rate dos dividendos (perpétuo)

Condição: **r > g** sempre. Se g ≥ r, modelo diverge (valor infinito = inconsistente).

## Quando aplicar

✅ **Empresas maduras** com dividendo previsível (Aristocrats, Kings):
- KO, JNJ, PG, MCD, O, T
- BR: VALE3, BBDC4, ITSA4 (com ajuste), TAEE11

✗ **Não aplicar**:
- Empresas sem dividendo (TSLA, GOOGL, META)
- Early-stage growth
- Cyclicals com div volátil (PRIO3, tankers)

## Reverse DDM — mais útil

Em vez de calcular fair value, **inverter** para descobrir o **g implícito** no preço actual:

$$
g_{\text{implicit}} = r - \frac{D_1}{P_0}
$$

Se g_implicit > growth realista (say > 6% para mature) → acção **overvalued**.

### Exemplo: KO
- Preço $76
- Div 2026 esperado ~$2.04
- r = 8.5% (US RF 4.5% + equity prem 4%)
- g_implicit = 8.5% - (2.04/76) = **5.8%**

KO growth histórico dividendos 5y CAGR ≈ 5% → g_implicit próximo do real → **fair**.

### Exemplo: JNJ (hoje $230)
- Div 2026 ~$5.36 (estimativa)
- r = 8%
- g_implicit = 8% - (5.36/230) = **5.7%**

JNJ 5y CAGR = 5.8% → **fair value**.

## DDM de 2 estágios (mais flexível)

Empresas transicionando de growth → mature:
$$
P_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r)^t} + \frac{D_{n+1}/(r-g_{\infty})}{(1+r)^n}
$$

Onde:
- Fase 1 (anos 1-n): growth alto g₁ (say 10%)
- Fase 2 (terminal): growth sustentável g_∞ (say 4%)

## Required return (r) — como escolher

| Tipo | r sugerido |
|---|---|
| **Utility blue-chip** (O, UTES) | 7-8% (baixo risco) |
| **Aristocrat Staples** (KO, PG) | 8-9% |
| **Banks mature** (JPM) | 9-10% |
| **Cyclicals** (VALE) | 12-14% |
| **BR tickers** | +3-4% sobre US equivalentes (country premium) |

## Growth (g) — como estimar

### Histórico
- 5y dividend CAGR (trimmed, excluir one-offs)
- 10y preferível para Aristocrats

### Forward
- Management guidance (se houver)
- ROE × (1 - payout) = sustainable g
- Revenue growth × profit margin × (1 - payout)

### Realista
- US Staples: 4-7%/y
- US Banks: 5-8%/y
- US Utilities: 4-5%/y
- US Aristocrats generic: 5-8%
- BR dividend payers: 3-7%/y (inflação dilui)

## No nosso sistema

`scripts/drip_projection.py::derive_scenarios` usa DDM-inspired para:
- Base scenario: g = histórico CAGR (damped)
- Optimistic: g + 50%
- Conservative: g - 50% OR Gordon-derived floor

## Limitações

1. **Sensibilidade g → r**: mudança 1pp em g muda preço 20-30%
2. **Ignora buybacks** — hoje muitos substituem div por buyback (AAPL, MSFT, ORCL)
3. **Ignora special dividends**
4. **Empresas que cortam** (GE 2018, T 2022): modelo puro nunca antecipa

---

> **Fontes**: Gordon & Shapiro (1956) *Capital Equipment Analysis*; Damodaran *Investment Valuation* (cap. 13); Fisher Black critique "DDM é toy model" mas útil como sanity check; nosso código em `scripts/drip_projection.py`.
