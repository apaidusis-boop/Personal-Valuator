---
type: macro
name: Fed Funds Rate — Taxa básica US
category: interest_rates
country: US
source: FRED (fred.stlouisfed.org) DFEDTARU
tags: [macro, fed_funds, fomc, us, interest_rates]
related: ["[[10Y_Treasury]]", "[[2s10s]]", "[[Selic]]", "[[CPI]]", "[[Core_CPI]]", "[[Fed_funds_history]]"]
source_class: derived
confidence: 0.7
freshness_check: 2026-04-30
---

# Fed Funds Rate — Benchmark US

## O que é

Taxa **overnight** à qual bancos com excesso de reservas **emprestam a bancos com deficit** de reservas no Federal Reserve. É a ferramenta principal do **FOMC** (Federal Open Market Committee) para gerir política monetária.

## Estrutura do FOMC

### Composição
- 7 membros do **Board of Governors** (indicados presidente, ratificados Senado, 14y)
- 5 presidentes de **Federal Reserve Banks regionais** (NY permanente; outros 4 rotam)
- Total: **12 voting members**

### Reuniões
**8 por ano** (~6 semanas entre cada). Typical months: Jan, Mar, Apr/May, Jun, Jul, Sep, Oct/Nov, Dec.

### Outputs
- **FOMC statement** (2:00pm ET) — decisão + comunicação
- **Dot plot** (trimestral) — projeções individuais de cada membro para fed funds
- **SEP** (Summary of Economic Projections) — GDP, unemployment, inflation, rates
- **Press conference** (30m depois) com Powell

## Alvo (target range)

Desde 2008, Fed usa **range de 25bp** (não single rate):
- Ex: **5.00%-5.25%** (upper bound = o que media escreve)

## Mandate — dual (vs BCB single)

Congressional Federal Reserve Act dual mandate:
1. **Maximum employment** (unemployment ~4-5% natural rate)
2. **Price stability** (PCE 2% target)

E implícito:
3. **Moderate long-term interest rates**
4. **Financial stability**

## Ferramentas além da Fed funds

### QE / QT
- **Quantitative Easing** (2008-2014, 2020-2022): compra de títulos long-term → inflow liquidez + dovish signal
- **Quantitative Tightening** (2017-2019, 2022+): balance sheet reduction → tightening implícito

Balance sheet peak: **$9 trillion** (2022). Runoff rate: ~$95B/month.

### Interest on Reserve Balances (IORB)
Fed paga juros sobre reservas bancárias — piso para fed funds corridor.

### Overnight Reverse Repo (ON RRP)
Money market funds park cash aqui — outro piso para taxa.

## Como lê-se o Fed

### Hawkish (pro-tightening)
- "Inflation remains elevated"
- "Further rate increases may be appropriate"
- "Continuing QT"
- Dot plot: rates higher than market expects

### Dovish (pro-cutting)
- "Progress on inflation"
- "Softening labor market"
- "Closer to neutral"
- Dot plot: cuts proximos

### Neutral
- "Data-dependent"
- "On hold"
- "Wait and see"

## Histórico rápido (ver [[Fed_funds_history]])

| Ano | Fed funds | Contexto |
|---|:-:|---|
| 1981 | **20%** | **Volcker peak** vs inflação 14% |
| 2001-2003 | 6→1% | dot-com + 9/11 cuts |
| 2007-2008 | 5.25→0% | GFC cuts aggressive |
| 2008-2015 | **0-0.25%** | **Zero-bound década** + QE |
| 2015-2019 | 0→2.5% | Gradual normalisation |
| 2020 | 0% + QE massivo | COVID emergency |
| 2022-2023 | 0→5.5% | **525bp hike em 18m** — fastest hiking cycle ever |
| 2024-2026 | 4.5-5.25% | Moderation, higher-for-longer |

## Efeito em ações

### Rate up (hiking cycle)
- **Bad for**: growth tech (discount rate higher devalues future cash flows), REITs, utilities, unprofitable
- **Good for**: banks (NIM expansion), insurance (float earns more), cash-rich staples
- **Historical**: S&P multiples compress ~15-25% during fast hike cycles

### Rate down (cutting cycle)
- **Bad for**: banks (NIM compression), cash-rich companies (less yield)
- **Good for**: REITs, growth tech, unprofitable
- **Historical**: Soft-landing cuts bull; recessionary cuts bear

## Yield curve (ver [[2s10s]])

Fed funds control short-end. **10Y yield** controlled por mercado (expectations + term premium). When:
- **2s10s positive** (normal): expansion
- **2s10s inverted**: recession warning (6 of 7 inversions preceded recessions since 1970)

## Fed vs BCB — diferenças

| Aspecto | Fed (US) | BCB (BR) |
|---|---|---|
| **Mandato** | Dual (employment + prices) | Single (inflation target) |
| **Meta inflação** | PCE 2% | IPCA 3% (± 1.5pp) |
| **Frequency** | 8/y | 8/y (Copom) |
| **Balance sheet tool** | QE/QT | Sem QE tradicional |
| **Independence** | Strong | Desde 2021 (Lei Complementar 179) |

## No nosso sistema

- `data.series` tabela (BR DB)? Não — temos FRED fetcher em `fetchers/fred_fetcher.py`
- Series comumente usadas: DFEDTARU (upper bound), DGS10 (10Y)
- `analytics/regime.py` usa Fed path como input regime US

## Onde consultar

- **FRED**: `fred.stlouisfed.org/series/DFEDTARU` (upper bound)
- **Fed Calendar**: `federalreserve.gov/monetarypolicy/fomccalendars.htm`
- **Dot plot**: página do SEP, após cada reunião trimestral
- **Minutes**: ~3 semanas após reunião

---

> **Fontes**: Federal Reserve Board (federalreserve.gov); FRED economic data; FOMC statements arquivo; Alan Blinder *The Quiet Revolution*; Ben Bernanke *21st Century Monetary Policy*; nosso fetcher `fetchers/fred_fetcher.py`.
