---
type: method
name: Piotroski F-Score
category: quality
author: Joseph Piotroski
year: 2000
tags: [method, quality, piotroski, veto, f_score]
applies_to: [equity, non_financial]
related: ["[[Altman_Z]]", "[[Dividend_Safety]]", "[[Graham_deep_value]]", "[[Quality_vs_deep_value]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Piotroski F-Score

## Thesis original (2000)

Joseph Piotroski estudou se era possível **melhorar retornos de value investing** (book-to-market alto) aplicando **quality screen simples**. Resultado: dentro de cesto top-20% B/M, os com F ≥ 7 outperformaram os com F ≤ 1 em **+7.5%/year** (1976-1996).

## Os 9 critérios (0 ou 1 cada)

Dividido em 3 categorias comparando **ano T vs T-1**:

### Profitability (4)
| # | Critério | 1 ponto se... |
|---:|---|---|
| 1 | ROA positivo | Net Income / Total Assets > 0 |
| 2 | FCF positivo | Operating CF - CapEx > 0 |
| 3 | ΔROA positivo | ROA_t > ROA_{t-1} |
| 4 | FCF > Net Income | **Quality of earnings** — acruais saudáveis |

### Leverage / Liquidity (3)
| # | Critério | 1 ponto se... |
|---:|---|---|
| 5 | Leverage não subiu | LTDebt/Assets ≤ ano anterior |
| 6 | Current ratio subiu | CA/CL_t > CA/CL_{t-1} |
| 7 | Sem dilution | Shares outstanding ≤ ano anterior |

### Operating efficiency (2)
| # | Critério | 1 ponto se... |
|---:|---|---|
| 8 | Gross margin subiu | GM_t > GM_{t-1} |
| 9 | Asset turnover subiu | Rev/Assets_t > Rev/Assets_{t-1} |

## Interpretação

| F-Score | Label | Acção |
|:-:|---|---|
| **8-9** | STRONG | Compounder com momentum fundamental |
| **5-7** | NEUTRAL | Normal, olhar restante screen |
| **3-4** | WEAK | Deteriorando — cautela |
| **0-2** | DISTRESS | Evitar ou cortar |

## No nosso sistema

`scoring/piotroski.py::compute` e usado como **veto estrutural** em:
- `config/triggers.yaml::quality/piotroski-weak` (threshold F ≤ 3)
- `scripts/research.py::_final_verdict` (veto AVOID)
- `scripts/verdict.py` (compontente Quality, weight 35%)

## Limitações

1. **Sector-agnostic** — banks/REITs não encaixam igual (leverage expected high)
2. **Requer 2 anos annual** — tickers novos (PLTR IPO 2020) só têm F recente
3. **Mechanical** — não capta mudança qualitativa (novo CEO, nova categoria)
4. **Não é timing signal** — empresa F=9 hoje pode crashar amanhã por razões externas

## Casos no nosso portfolio

| Ticker | F-Score | Interpretação |
|---|:-:|---|
| [[ABBV]] | 8/9 | STRONG — Rinvoq/Skyrizi ramp visible nos números |
| [[ACN]] | 5/9 | NEUTRAL — ROA flat, margem caindo, turnover down |
| [[TEN]] | 3/9 | WEAK — trigger veto; consistente com distress memo |

## Evolução da metodologia

Variantes propostas:
- **Piotroski F modified** (Mohanram G-Score) — para growth stocks
- **Trailing F** — usar TTM em vez de annual (reduz lag 6-9m)
- **Sector-adjusted F** — normalizar critérios 8, 9 por sector

---

> **Fontes**: Piotroski (2000) *Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers* (Journal of Accounting Research); AQR whitepapers sobre quality factor; nosso código em `scoring/piotroski.py`.
