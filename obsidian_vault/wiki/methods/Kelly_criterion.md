---
type: method
name: Kelly Criterion
category: position_sizing
author: John L. Kelly Jr.
year: 1956
tags: [method, position_sizing, kelly, risk_management]
related: ["[[Position_sizing]]", "[[Risk_free_rate]]", "[[Moat_types]]"]
---

# Kelly Criterion

## Fórmula

$$
f^* = \frac{p \cdot b - q}{b}
$$

Onde:
- **f***: fracção óptima do capital a apostar
- **p**: probabilidade de ganhar
- **q = 1 - p**: probabilidade de perder
- **b**: odds (win amount / loss amount)

## Intuição

Kelly maximiza **log-return esperado** long-run. Apostar mais que Kelly → ruína matemática. Menos que Kelly → growth sub-óptimo mas seguro.

## Exemplo clássico (coin flip +2/-1)

- p = 0.5 (50% ganhar)
- b = 2 (ganhas 2, perdes 1)
- q = 0.5

f* = (0.5 × 2 - 0.5) / 2 = **0.25 (25% do capital)**

## Problema em investimentos reais

Kelly assumes **distribuição conhecida**. Em stocks:
- p é estimativa subjectiva (model risk)
- b depende de holding period + volatility
- Tail events não normalmente distribuídos

**Kelly puro leva a volatilidade extrema** — 50% drawdowns common em "full Kelly".

## Kelly-lite (nosso approach)

Usar **frac × Kelly** onde frac = 0.25-0.5 ("quarter Kelly" a "half Kelly"):

$$
f^* = 0.5 \times \frac{p \cdot b - q}{b}
$$

Com cap absoluto em **5% por ticker** (max concentration).

Ajustes no nosso `scripts/position_size.py`:
- **p** derivado de verdict score (5/10 = 0.5 win prob baseline, escalado)
- **b** ajustado por volatility 90d (high vol → penaliza edge)
- **Confidence haircut**: multiplica f* pela confidence do verdict

## Quando Kelly é útil

✅ **Decisões sizing relativas** entre múltiplas opções
✅ **Comparar "certeza" de 2 teses** (p=0.7 vs 0.55)
✅ **Risk budget** trimestral

✗ **Point prediction absolute** (nenhum modelo dá p verdadeiro)
✗ **Single-ticker decisions isoladas**
✗ **Assumes stationary distributions** (markets mudam regimes)

## Versões mais sofisticadas

### Kelly para carteiras
Maximizar Kelly sobre múltiplos assets simultaneamente → matriz de covariância + retornos esperados → **Markowitz + Kelly** fusion.

### Continuous-time Kelly (Thorpe)
$$
f^* = \frac{\mu - r}{\sigma^2}
$$

Onde:
- **μ**: expected return
- **r**: risk-free
- **σ**: volatility

Para SPY com μ=10%, r=4%, σ=16%:
f* = (0.10 - 0.04) / 0.16² = **2.34 (234%?!)**

Issue: Kelly diz usar **leverage 2.3×**. Na realidade quase ninguém faz isto porque:
- Historical σ underestima tail risk
- Leverage tem custos
- Drawdowns insuportáveis psicologicamente

## Recomendações práticas

1. **Half Kelly max** em carteiras diversificadas
2. **Quarter Kelly** para single-stock picks (muito model risk)
3. **Cap absoluto 5%** por ticker (independente do Kelly)
4. **Cap 25%** por sector
5. **Se Kelly diz > 10%, está errado** — p ou b foram sobre-estimados

## No nosso sistema

`scripts/position_size.py` usa Kelly-lite como sugestão. Ex:
- ACN verdict 6.15/10, confidence 80%, vol 3% daily
- p = 0.57, b = 1.5 - 3 = -1.5 (!) → Kelly negativo → **0 shares**

Kelly math says **don't add** em ACN atm — vol penalizes edge.

## Warren Buffett on Kelly

> *"Never risk what you have and need for something you don't have and don't need."*

Buffett usa Kelly intuitivamente — concentrou **40% em Amex 1964**, 50% em GEICO 1970s. Full-Kelly quando convicção altíssima + edge claro.

---

> **Fontes**: Kelly (1956) *A New Interpretation of Information Rate*; Ed Thorp *A Man for All Markets*; William Poundstone *Fortune's Formula*; Ole Peters ergodicity economics; nosso código em `scripts/position_size.py`.
