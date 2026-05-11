---
type: method
name: Buffett Quality
category: valuation
author: Warren Buffett
year: 1965-present
tags: [method, valuation, buffett, quality, moat]
related: ["[[Graham_deep_value]]", "[[Moat_types]]", "[[ROIC_interpretation]]", "[[Aristocrats_Kings]]", "[[Economic_moats_Damodaran]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Buffett Quality Investing

## Evolução Graham → Fisher → Munger → Buffett

Buffett começou **Graham puro** (deep value). A transição para quality veio via Philip Fisher (*Common Stocks and Uncommon Profits*) e Charlie Munger. A frase-chave:

> *"It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."*

## Os 4 pilares

### 1. Business que entendas (Circle of Competence)
Se não percebes o modelo de negócio em 5 minutos, **passa**. Buffett ignorou tech durante 40 anos por isto.

### 2. Moat económico durável ([[Moat_types]])
- **Brand** (KO, AAPL, MCD)
- **Switching costs** (V, MA, MSFT Azure)
- **Network effects** (V, MA, META)
- **Cost advantage** (WMT, COST, GEICO)
- **Scale** (AMZN, JPM)

### 3. Management honesto e racional
- Capital allocation: reinvestir só se ROIC > WACC
- Buybacks **só** quando stock < intrinsic value
- Dividend policy consistent
- CEO letters legíveis (Berkshire, Markel)

### 4. Preço razoável (não obrigatoriamente barato)
- P/E pode ser 20-30× se quality extrema (MCO, MSFT)
- ROIC ≥ 15% consistente justifica premium
- FCF yield ≥ 5% preferível

## Métricas proxy Buffett

| Métrica | Threshold | Porquê |
|---|---|---|
| **ROE** | ≥ 15% consistente 10y | Retorno sobre equity reinvestido |
| **ROIC** | ≥ 12% | Better que ROE (ignora alavancagem) |
| **Gross margin** | Estável ou crescente | Pricing power = moat |
| **Debt/Equity** | ≤ 0.5 | Sobrevive recessões |
| **FCF conversion** | > 90% NI | Lucro "real" |
| **Insider ownership** | High + no selling | Skin in the game |
| **Capex/Revenue** | Low (< 5%) preferível | Asset-light compounders |

## O teste definitivo

> *"Se o mercado fechasse por 10 anos, continuarias confortável com esta empresa?"*

Se resposta **sim** → candidato Buffett.

## Casos clássicos

| Empresa | Quando comprou | Lição |
|---|---|---|
| Coca-Cola ([[KO]]) | 1988 após crash 87 | Brand global, rarely sold |
| American Express | 1964 post-salad oil crisis | Franchise + oportunismo |
| See's Candies | 1972 | Pricing power pura |
| Apple ([[AAPL]]) | 2016 (tardio) | Evoluiu do anti-tech para "consumer brand com hardware" |
| Bank of America | 2011 crisis | Preferred shares + warrants |

## No nosso sistema

- `score_us`: P/E ≤ 20, P/B ≤ 3, DY ≥ 2.5%, ROE ≥ 15%, aristocrat OR streak ≥ 10
- Intencionalmente menos restritivo que Graham em P/E — permite pagar quality
- `scoring.piotroski` captura deterioração de quality (veto F ≤ 3)

## Crítica honesta

Quality compounders têm **sobrevalorização** em regimes optimistas (2010-2021). Pós-2022 rates hike, muitos caíram 30-50% (MSFT, ADBE, MA). Quality ≠ imune a drawdowns.

---

> **Fontes**: Berkshire letters (buffett.com archives); Buffett biography *The Snowball* (Schroeder); Robert Hagstrom *The Warren Buffett Way*; Pat Dorsey *The Little Book That Builds Wealth* (moats).
