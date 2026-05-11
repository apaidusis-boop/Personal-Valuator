---
type: method
name: Graham Number
category: valuation
author: Benjamin Graham
year: 1934
tags: [method, valuation, graham, deep_value]
applies_to: [equity, non_financial]
related: ["[[Graham_deep_value]]", "[[P_E_interpretation]]", "[[P_B_interpretation]]", "[[Buffett_quality]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Graham Number

## O que é
Preço **máximo** que um value investor conservador deve pagar por uma acção, segundo Benjamin Graham em *The Intelligent Investor* (1949).

## Fórmula
$$
\text{Graham Number} = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}
$$

O factor 22.5 = 15 × 1.5 (P/E máximo × P/B máximo).

## Quando aplicar

✅ **Empresas maduras, rentáveis, com BV positivo** (industriais, consumo, saúde)

✗ **NÃO aplicar em**:
- **Bancos** (P/B lógica diferente; equity altamente alavancado — usar P/B ≤ 1.5 directo)
- **REITs/FIIs** (NAV-driven, FFO em vez de EPS)
- **Empresas com BV negativo** (PG, HD, CLX — buybacks pesados)
- **Growth puro** (ACN era borderline; META/GOOGL não se encaixam)
- **Cyclicals em peak earnings** (PRIO3 em Brent alto mascara)

## Interpretação

| Relação | Leitura |
|---|---|
| Preço ≤ Graham Number | 🟢 Margem de segurança Graham |
| Preço > Graham Number × 1.5 | 🔴 Caro |
| Preço < Graham × 0.7 | 🟢🟢 Deep value — verificar distress (Altman) |

## No nosso sistema

`scoring/engine.py::score_br` aplica como critério #1 (≥ preço × 22.5). Também em `scripts/research.py`. Bancos usam `score_br_bank` que ignora este critério.

## Limitações

- EPS pode ser massajado (extraordinários, impostos diferidos)
- BVPS históricos distorcem (intangíveis, goodwill enorme)
- Não captura quality (Piotroski) nem distress (Altman)
- Ignora growth (um Kings Aristocrat com 53y streak pode ter Graham ≠ real value)

## Exemplo prático

**ACN** (2026-04-23): EPS 12.19, BVPS 50.76
- Graham Number = √(22.5 × 12.19 × 50.76) = **√13,917** = **$118**
- Preço actual $178 → **acima do Graham** mas não astronómico
- Margem só se preço ≤ $118 (seria −34% adicional)

---

> **Fontes**: Graham, *The Intelligent Investor* (1949/revised 1973); *Security Analysis* (1934); [[Aristocrats_Kings]] framework; [[Piotroski_F]] + [[Altman_Z]] complementam.
