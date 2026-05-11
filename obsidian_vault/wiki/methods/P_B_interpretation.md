---
type: method
name: P/B Ratio — interpretation
category: valuation
tags: [method, valuation, pb_ratio, book_value, multiples]
related: ["[[P_E_interpretation]]", "[[Graham_Number]]", "[[ROIC_interpretation]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# P/B Ratio — quando importa, quando não

## Fórmula

$$
P/B = \frac{\text{Price per share}}{\text{Book Value per share (BVPS)}}
$$

BVPS = (Total Equity - Preferred) / Shares outstanding.

## Intuição

P/B = quanto o mercado paga por **R$1 de equity contábil**.

- P/B 1.0 = preço = equity
- P/B 2.0 = paga 2× equity (justifica-se por ROE > cost of equity)
- P/B 0.5 = distress / mercado descrente

## Thresholds

| Tipo empresa | P/B fair |
|---|---|
| **Banks sólidos** (JPM, ITUB4) | 1.0-2.0 |
| **REITs** | 0.9-1.3 (close to NAV) |
| **Industrial maduro** | 1.5-3.0 |
| **Growth quality** (MSFT) | 5-15 |
| **Asset-light services** (ACN, V) | 3-10 |
| **Tech early-stage** | 10-50+ (BV negativo irrelevante) |

## Relação P/B ↔ ROE

**Equação fundamental** (Warren Buffett):
$$
\text{Sustainable P/B} = \frac{ROE - g}{r - g}
$$

Onde:
- ROE = retorno sobre equity
- g = growth rate
- r = cost of equity

Exemplo: ROE 20%, g 5%, r 10%:
- Sustainable P/B = (20 - 5) / (10 - 5) = **3.0×**

Se ROE ≤ r, P/B deve ser ≤ 1.0 (empresa destrói valor).

## Casos onde P/B FALHA

### 1. Buybacks agressivos → BV negativo
Empresas comprando ações a preço alto, amortizam equity:
- **HD**: BVPS negativo
- **PG, CLX, AZO, YUM**: BV deprimido ou negativo
- P/B "gigantesco" ou negativo — **irrelevante** nestes casos

### 2. Write-offs / impairments
Empresa reconhece goodwill write-off → BV cai → P/B "parece caro"
- **GE** em 2018 após write-offs — P/B parecia maior que real

### 3. Intangíveis pesados
Software (MSFT, ORCL), pharma (ABBV goodwill Allergan):
- BV é **metade real value** — P/B inflate artificially
- Usar **P/TBV** (tangible book value) ou **P/FCF**

### 4. Mark-to-market variability
Banks: bond portfolios marked to market (AFS bonds) → BV oscila com rates
- 2022 banks: BV caiu 20% com rates up → P/B subiu artificially
- Long-run mean-reversão OK

## P/B baixo = oportunidade?

### SIM quando
- ROE ≥ r (equity productive)
- Sector em recessão temporária (banks 2009, 2016, 2020)
- Management racional (não dilui)

### NÃO quando (P/B trap)
- ROE < r sistemático (value destruction)
- Secular decline (newspapers, coal)
- Hidden liabilities (off-balance-sheet, pensions, environmental)

**Regra**: P/B 0.5 pode ser deep value OR distress. Cross-check com [[Altman_Z]] + [[Piotroski_F]].

## P/B sector-specific

### Bancos
P/B 1.0 = NAV. Comprar abaixo de 1.0 em banks tier-1 (JPM, BAC) é historicamente lucrativo.

### REITs / FIIs
P/B ~ P/NAV. Usar **P/NAV** directly melhor (external appraisal).

### Insurance
Life insurers: usar **P/Embedded Value** (EV). P&C: usar P/B book direct.

### Shipping / tankers
Very cyclical. P/B 0.5 em bottom = grande edge; P/B 2.0 em peak = sell.

### Tech
P/B mostly useless. Use **EV/Revenue** + **Rule of 40** (growth + FCF margin ≥ 40).

## P/TBV (Tangible Book Value)

$$
P/TBV = \frac{\text{Price}}{\text{Equity} - \text{Goodwill} - \text{Intangibles}}
$$

Crucial para banks (regulators olham TBV), M&A-heavy companies.

## No nosso sistema

- `scoring/engine.py::score_us`: P/B ≤ 3 threshold
- `scoring/engine.py::score_br_bank`: P/B ≤ 1.5 (bancos)
- `scripts/verdict.py`: parte do screen_score

## Exemplos no portfolio

| Ticker | P/B | Interpretação |
|---|:-:|---|
| [[ACN]] | 3.83 | Ligeiramente cara (threshold 3.0) — mas ROE 25% justifica |
| [[BBDC4]] | ~1.0 | **NAV** — banks fair |
| [[JPM]] | ~2.2 | Premium — JPM é best-in-class |
| [[AAPL]] | 44× | Intangible-heavy — P/B irrelevante, usar P/FCF |
| [[O]] | ~1.1 | REIT próximo NAV |
| [[PG]] | -97 (!) | **Ignorar** — buybacks drained equity |

---

> **Fontes**: Damodaran lectures on multiples; Aswath Damodaran *Investment Valuation*; Pinto *Equity Asset Valuation*; McKinsey *Valuation*.
