---
type: method
name: Altman Z-Score
category: distress
author: Edward I. Altman
year: 1968
tags: [method, distress, altman, z_score, bankruptcy, veto]
applies_to: [equity, non_financial, industrial]
related: ["[[Piotroski_F]]", "[[Dividend_Safety]]", "[[Net_debt_EBITDA]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Altman Z-Score

## Thesis (1968)

Modelo de **5 rácios financeiros** que prevê falência com **~72-80% accuracy** a 1-2 anos. Construído por Altman (NYU) sobre 66 empresas manufactureiras.

## Fórmula original (Public Manufacturing)

$$
Z = 1.2 \cdot X_1 + 1.4 \cdot X_2 + 3.3 \cdot X_3 + 0.6 \cdot X_4 + 1.0 \cdot X_5
$$

| X | Definição | Proxy |
|---|---|---|
| X₁ | Working Capital / Total Assets | Liquidez curto prazo |
| X₂ | Retained Earnings / Total Assets | Rentabilidade acumulada |
| X₃ | **EBIT / Total Assets** | Produtividade dos assets |
| X₄ | Market Cap / Total Liabilities | Leverage + mercado |
| X₅ | Revenue / Total Assets | Turnover |

## Zonas

| Z-Score | Zona | Interpretação |
|:-:|---|---|
| Z > 2.99 | 🟢 **SAFE** | Baixa prob. falência 2y |
| 1.81 ≤ Z ≤ 2.99 | 🟡 GREY | Zona de indefinição |
| Z < 1.81 | 🔴 **DISTRESS** | Alta prob. falência — **veto** |

## Variantes

### Z'-Score (Private manufacturing)
$$
Z' = 0.717 X_1 + 0.847 X_2 + 3.107 X_3 + 0.420 X_4 + 0.998 X_5
$$
X₄ usa book value em vez de market cap. Threshold: Z' < 1.23 distress.

### Z''-Score (Emerging markets / non-manufacturing)
$$
Z'' = 6.56 X_1 + 3.26 X_2 + 6.72 X_3 + 1.05 X_4
$$
**Exclui X₅** (turnover) — útil para serviços, tech, BR. Threshold: Z'' < 1.1.

## Quando NÃO usar

✗ **Bancos e financeiras** — balance sheet estruturalmente diferente (Basel III ratios, Texas ratio, CET1 mais apropriados)
✗ **REITs/FIIs** — leverage expected high, diferente interpretação
✗ **Empresas pre-revenue** ou early-stage growth (PLTR pré-2020)
✗ **Utilities reguladas** — debt alto é feature, não bug

## No nosso sistema

`scoring/altman.py::compute` em `scripts/verdict.py` (peso quality 35%) + `config/triggers.yaml::quality/altman-distress` (threshold 1.81).

Usa deep_fundamentals anual + market cap × shares.

## Interpretação moderna (Altman 2000 update)

Altman reviu em 2000 e 2017:
- Threshold SAFE subiu para **~3.0** (inflation in ratios)
- Z < 1.1 é o novo "distress" real (1.81 era 1968)
- **Z-score de empresas listadas subiu em média** (survivorship + contabilidade mais conservadora)

## Casos no nosso portfolio

| Ticker | Z | Zone | Nota |
|---|:-:|---|---|
| [[ACN]] | 4.38 | SAFE | Net cash + FCF robusto |
| [[ABBV]] | 1.99 | GREY | Debt alto pós-aquisições (Allergan), watch |
| [[TEN]] | 1.02 | **DISTRESS** | Consistente com memo SELL + dividend cut |
| [[BRK-B]] | N/A | Bank-like | Altman não aplicável a holding com muita seg. |

## Limitações

1. **Score estático** — Z-score de 3 hoje pode ser 1.5 em 6 meses (auto manufacturers)
2. **Não captura off-balance-sheet debt** (operating leases pré-2019, SPVs)
3. **EPS one-time items** inflam X₃ artificialmente
4. **Pós-crisis tail risk** — Z funcionou mal em 2008 para bancos

---

> **Fontes**: Altman (1968) *Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy* (Journal of Finance); Altman (2000, 2017) updates; nosso código em `scoring/altman.py`.
