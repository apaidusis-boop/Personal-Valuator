---
type: method
name: ROIC — Return on Invested Capital
category: quality
tags: [method, quality, roic, returns]
related: ["[[Moat_types]]", "[[Buffett_quality]]", "[[WACC_calculation]]"]
---

# ROIC — Return on Invested Capital

## Fórmula

$$
ROIC = \frac{NOPAT}{\text{Invested Capital}}
$$

Onde:
- **NOPAT** = EBIT × (1 - Tax rate)
- **Invested Capital** = Equity + Debt − Cash (ou Total Assets − non-interest liabilities)

## Por que ROIC > ROE

**ROE** inflate com leverage (e.g., banks ROE 15% mas equity é 10× assets).

**ROIC** neutraliza estrutura de capital — compara **produtividade do capital total** independent of debt/equity mix.

## Threshold

| ROIC | Quality |
|:-:|---|
| > 20% | 🟢 Excelente — compounder monster (MSFT, V, ADBE) |
| 15-20% | 🟢 Strong — Buffett quality bar |
| 10-15% | 🟡 Fair — acima WACC típico |
| 5-10% | 🟠 Average — marginal value creation |
| < 5% / < WACC | 🔴 Value destruction (ICL em minerais, muitas utilities over-levered) |

## Regra fundamental

$$
\text{Value creation} = ROIC - WACC
$$

- **ROIC > WACC** → empresa cria valor para shareholders
- **ROIC = WACC** → empresa neutra (break-even economicamente)
- **ROIC < WACC** → **destrói valor** — dinheiro melhor em bonds

## WACC típico (para comparação)

| Tipo de empresa | WACC aprox |
|---|---|
| **Banks blue-chip** (JPM) | 9-10% |
| **Utility regulada** | 6-8% |
| **Consumer staples** | 7-8% |
| **Tech quality** | 9-11% |
| **Cyclical BR** (VALE3) | 11-13% |
| **High-yield / junk** | 12-16% |

## Evolução ROIC — sinal crítico

**ROIC trend importa mais que level**:
- ROIC crescendo 10y → **moat strengthening** (AMZN 2015-2020)
- ROIC declining → **moat eroding** (IBM 2010-2020; GE 2000s)

Buffett exemplo positivo: COST ROIC subiu de 11% (2000) para 25% (2023) — moat strengthening.

## Top ROIC companies (benchmarks)

| Ticker | ROIC 5y avg |
|---|:-:|
| **V** (Visa) | 30%+ |
| **MA** (Mastercard) | 55%+ |
| **MSFT** | 25%+ |
| **AAPL** | 40%+ (unusual high) |
| **LULU** | 35%+ |
| **ADBE** | 30%+ |
| **ACN** | 25%+ |

## Medição prática

### Invested Capital
$$
IC = \text{Total Debt} + \text{Equity} - \text{Cash} - \text{Goodwill optional}
$$

Subtrair goodwill (ROIC excl goodwill) = **produtividade dos assets reais** (ignora M&A premium).

### NOPAT approximation
$$
NOPAT \approx EBIT \times (1 - \text{Effective Tax Rate})
$$

Tax rate = Taxes Paid / Pre-tax Income (últimos 3y average).

### Average vs beginning/ending IC
Usar **average(BoY, EoY)** para ROIC anual. Empresas growing → ending IC > beginning → usar beginning pode inflate ROIC.

## Casos especiais

### Banks
ROIC doesn't really apply — usar **ROTE (Return on Tangible Equity)** ou **ROA**.

### REITs
ROIC pouco informativo — usar **FFO yield** e **dividend coverage**.

### Early-stage growth
Negative NOPAT → ROIC negativo. Useless até chegar a break-even.

### Empresas com much goodwill
- **Including goodwill**: ROIC mais conservador, reflecte M&A cost
- **Excluding goodwill**: ROIC "underlying business"
- Ambos úteis; prefiro **including** por default (realidade financeira)

## No nosso sistema

Actualmente **não computamos ROIC** — usamos **ROE** como proxy (thresholds: US ≥15%, BR ≥15% non-banks, BR banks ≥12%).

**Pendente**: adicionar ROIC em `scoring/roic.py` + verdict component.

## Cross-check ROIC

1. **ROIC estável ou subindo 5y?** → moat real
2. **ROIC > WACC consistentemente?** → value creation
3. **ROIC varies enormously year-to-year?** → cyclical business
4. **Gross margin + ROIC moving same direction?** → moat signal
5. **ROE >> ROIC?** → leverage-driven (bank-like), ROIC mais honesto

---

> **Fontes**: McKinsey *Valuation* (Koller/Goedhart/Wessels) — bíblia do ROIC; Charlie Munger 1994 speech "A Lesson on Elementary, Worldly Wisdom"; Mauboussin *Expectations Investing*; Morningstar moat research.
