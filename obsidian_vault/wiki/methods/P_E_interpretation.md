---
type: method
name: P/E Ratio — interpretation
category: valuation
tags: [method, valuation, pe_ratio, multiples]
related: ["[[P_B_interpretation]]", "[[FCF_yield]]", "[[Graham_Number]]", "[[Equity_risk_premium]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# P/E Ratio — quando faz sense, quando engana

## Fórmula

$$
P/E = \frac{\text{Price per share}}{\text{EPS (TTM)}}
$$

Ou em termos de firma: Market Cap / Net Income.

## Interpretação intuitiva

P/E = **anos que demorarias a pagar o preço** da acção com lucros actuais (assumindo lucro constante).

Exemplo: P/E 20 = 20 anos de lucros "compram" a empresa.

## Inverso: earnings yield

$$
\text{Earnings Yield} = \frac{1}{P/E} \times 100\%
$$

P/E 20 → EY 5%. Comparar com 10Y UST (say 4.5%) → equity premium 0.5pp (pequeno, caro).

## Thresholds historicos

| P/E | Zona | Contexto |
|:-:|---|---|
| < 10 | Deep value / distress | Cyclicals bottom, dinos, BR value |
| 10-15 | Value | Graham zone, mature industrials |
| 15-20 | Fair | S&P500 média histórica |
| 20-30 | Growth premium | Aristocrats + growth modest |
| 30-50 | High growth | Tech qualities (MSFT, V) |
| > 50 | Speculative growth | Priced to perfection |

## Variantes importantes

### Trailing P/E (TTM)
Usa lucros últimos 12m. Mais objectivo mas **lagged** (pode estar desactualizado em cyclicals).

### Forward P/E
Usa EPS **previsto** próximos 12m (consensus). Mais útil mas depende de accuracy dos analistas (± erráticos).

### Cyclically Adjusted P/E (CAPE / Shiller)
$$
CAPE = \frac{\text{Price}}{\text{10y average EPS inflation-adjusted}}
$$

Para **index level** (S&P500). CAPE > 30 historicamente → decadas futuras decepcionantes.

Current S&P500 CAPE ~33 (elevado, mas não bolha 1999 onde foi 44).

## Quando P/E engana

### 1. One-time items
Write-offs, restructuring, tax benefits inflam/desinflam EPS.
- Ajuste: **Normalized earnings** (média 3-5y)

### 2. Cyclicals em peak
PRIO3 em Brent $100: EPS cresceu 5× → P/E "colapsou" para 4 → parece barato
- Na realidade: earnings mean-revert → P/E real ~10-15 on normalized

**Regra**: para cyclicals, comprar quando P/E é **alto** (earnings depressed).

### 3. Crescimento descontinuado
Empresas sem lucro (PLTR 2018-2019) têm P/E infinite/NMF.

### 4. Banks / financeiros
Banks EPS é **artificial** por provisions (PCLD). Usar **P/TBV** e **ROTE** complementar.

### 5. Goodwill / intangibles
Tech com muito amortization masca EPS baixo. Usar **EV/FCF** ou **P/FCF**.

### 6. Stock-based comp (SBC)
Tech **ignora SBC** no EPS em muitos casos. EPS GAAP vs **EPS ajustado SBC** pode ser 30-50% diferente.
- Ajuste: **P/FCF** ou use EPS com SBC subtraído.

### 7. Buybacks mascarando
Empresa encolhe share count → EPS sobe mesmo com lucro flat. Olhar **absolute earnings growth** não per-share.

## Relação P/E com crescimento

**PEG ratio** (Peter Lynch):
$$
PEG = \frac{P/E}{\text{Earnings Growth Rate (\%)}}
$$

- PEG < 1 = cheap vs growth
- PEG ~ 1 = fair
- PEG > 2 = expensive

Exemplo: MSFT P/E 30, growth 15% → PEG 2.0 (priced fairly for growth).

## Comparações úteis

**P/E vs sector average**: ACN P/E 15.95 vs Tech sector mediano ~25 → **P0 percentil** (cheapest in sector — ver `ii peers ACN`).

**P/E vs own historical**: JPM P/E atual vs JPM 10y histórico. Útil para detectar re-rating.

**P/E vs country yield**: BR P/E 12 fair se NTN-B 10Y é 6%. US P/E 20 fair se UST 10Y é 4.5%.

## No nosso sistema

- `scoring/engine.py::score_us`: P/E ≤ 20 threshold
- `scoring/engine.py::score_br`: usado em `score_br_bank` (P/E ≤ 10)
- `scripts/verdict.py::valuation_score`: componente screen_score

## Regras rápidas

✅ **P/E baixo em growth sustainable** = interesse
✅ **P/E alto em cyclicals em low** = earnings will recover
✅ **CAPE index level** = long-run return proxy

✗ **P/E baixo em cyclicals em high** = trap
✗ **P/E "cheap" por write-off one-time** = artifact
✗ **Forward P/E based on hyped consensus** = wishful

---

> **Fontes**: Robert Shiller *Irrational Exuberance* (CAPE); Peter Lynch *One Up on Wall Street* (PEG); McKinsey *Valuation*; Damodaran lectures.
