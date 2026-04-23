---
type: method
name: DCF Simplified
category: valuation
tags: [method, valuation, dcf, intrinsic_value]
related: ["[[DDM_Gordon]]", "[[WACC_calculation]]", "[[FCF_yield]]", "[[Risk_free_rate]]", "[[Equity_risk_premium]]"]
---

# DCF Simplificado

## O que é
Cálculo do **intrinsic value** baseado em valor presente dos Free Cash Flows futuros + terminal value. É o **ground truth** de value investing segundo Buffett/Damodaran.

## Fórmula base

$$
\text{Intrinsic Value} = \sum_{t=1}^{n} \frac{FCF_t}{(1+r)^t} + \frac{TV}{(1+r)^n}
$$

com Terminal Value (Gordon):

$$
TV = \frac{FCF_{n+1}}{r - g_{\text{terminal}}}
$$

## Inputs críticos (4)

### 1. FCF base (ano 0)
- **FCF = CFO - CapEx** dos últimos 12m (TTM preferível)
- Normalizar se cyclical (média 5 anos) ou se one-time items

### 2. Growth rate (g)
**Decaying 3 fases**:
- Anos 1-5: growth robusto (histórico CAGR, cap em 15%)
- Anos 6-10: fade to GDP-like (3-5%)
- Terminal: 2-3% (GDP long-run real + inflation)

Nunca g terminal > r (modelo diverge).

### 3. Discount rate (r = WACC)
$$
r = \text{Risk-free} + \beta \times \text{Equity Risk Premium}
$$

Para o **nosso uso**:
- **US tickers**: r = 10Y UST + 1.0 × 5.5% ≈ **9-10%**
- **BR tickers**: r = NTN-B 10y + 1.0 × 7.5% ≈ **13-15%**

### 4. Terminal growth (g_∞)
- **US**: 2.5% (Fed target + GDP real)
- **BR**: 4-5% (GDP nominal BR higher)
- Nunca > 4% US ou > 6% BR (irrealista long-run)

## Versão prática "simplified" (nosso sistema)

```
FCF_0 = TTM FCF
g_5y = min(historical_cagr, 15%)
discount = RF_10y + 5.5%  (US); +7.5% (BR)
g_term = 2.5% (US); 4% (BR)
horizon = 10y

PV = Σ FCF_0*(1+g_5y)^t / (1+r)^t for t=1..5
   + Σ FCF_5*(1+g_fade)^(t-5) / (1+r)^t for t=6..10
   + TV/(1+r)^10
```

## Margin of Safety

$$
\text{MoS} = 1 - \frac{\text{Market Cap}}{\text{Intrinsic Value}}
$$

| MoS | Decisão |
|---|---|
| > 40% | 🟢 BUY strong |
| 20-40% | 🟡 Good entry |
| 0-20% | 🟠 Fair value |
| < 0 | 🔴 Overpriced vs DCF |

## Armadilhas comuns

### 1. Growth rate muito alto
TSLA 2021 assumia 30%/y perpétuo — impossivel. Hoje mais perto 15%.

### 2. Terminal muito grande
Terminal value tipicamente = **60-75% do PV total**. Pequena mudança em g_∞ ou r destabiliza tudo.

### 3. FCF base volátil
Cyclicals (oil, semis, mining): usar média 5-7y, não TTM no pico.

### 4. Capex de crescimento ≠ manutenção
- Maintenance CapEx + SBC (stock-based comp) — **true FCF**
- Ignorar SBC em tech (GOOGL, MSFT) infla FCF ~10%

### 5. Taxes
Usar effective rate, não statutory. Especial BR: empresas com lucro no exterior (TSMC para US).

## Quando NÃO fazer DCF

- **Banks/insurers**: use P/TBV, ROTE, embedded value
- **REITs**: use P/NAV, FFO multiples
- **Growth hyper-early**: pre-revenue → DCF irrelevante
- **Cyclicals peak**: FCF normalized é mais honesto

## Comparação com outros frameworks

| Framework | Quando prefiro |
|---|---|
| **DCF** | Maduras com FCF estável e previsível |
| **DDM** ([[DDM_Gordon]]) | Utilities, FIIs, aristocrats dividendeiros |
| **P/E relativo** | Cyclicals, bancos |
| **Graham Number** ([[Graham_Number]]) | Deep value simples |
| **Sum-of-parts** | Holdings (ITSA4, Brookfield) |

## No nosso roadmap

Pendente implementar `scoring/dcf.py` (Sprint futuro). Até lá, uso aproximação manual + [[DDM_Gordon]] para dividendeiros.

---

> **Fontes**: Damodaran *Investment Valuation* (3rd ed); McKinsey *Valuation* (Koller); Greenwald *Value Investing*; prof. Damodaran's website tem templates + betas + ERP histórico.
