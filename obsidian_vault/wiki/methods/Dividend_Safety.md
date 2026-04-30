---
type: method
name: Dividend Safety Score
category: income
author: nosso (inspired Simply Safe Dividends)
tags: [method, dividend, safety, income, drip]
applies_to: [equity, dividend_paying]
related: ["[[Piotroski_F]]", "[[Altman_Z]]", "[[Aristocrats_Kings]]", "[[DRIP_compounding]]", "[[Dividend_coverage]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Dividend Safety (nosso framework 0-100)

## Thesis

Não basta saber se uma empresa paga dividendo **agora** — interessa prever se vai **continuar a pagar** e idealmente **aumentar** nos próximos 5 anos. Score composto de 4 componentes avalia sustentabilidade forward.

## Componentes (100 pontos total)

| Componente | Peso | Threshold safe |
|---|---:|---|
| **Payout ratio** | 35 | Div/EPS ≤ 60% (ou Div/FCF ≤ 70%) |
| **Streak of payments** | 25 | ≥ 10y non-decreasing |
| **ROE level** | 20 | ≥ 15% (gera quality de pagar) |
| **Net Debt / EBITDA** | 20 | ≤ 2.5× (não compromete div em stress) |

## Scoring por componente

### Payout ratio (35)
- ≤ 30% → 35 (low payout + runway to increase)
- 30-45% → 30
- 45-60% → 20
- 60-80% → 10
- > 80% → 0 (stretched, próximo corte)

### Streak (25)
- ≥ 25y → 25 (Aristocrat / King)
- 15-25y → 18
- 10-15y → 12
- 5-10y → 6
- < 5y → 0

### ROE (20)
- ≥ 20% → 20
- 15-20% → 15
- 10-15% → 10
- 5-10% → 5
- < 5% → 0

### Net Debt/EBITDA (20)
- Net cash → 20
- 0-1.5× → 18
- 1.5-2.5× → 12
- 2.5-4× → 6
- > 4× → 0

## Verdict

| Score | Label | Interpretação |
|:-:|---|---|
| **80-100** | 🟢 SAFE | Forward cut risk < 10% |
| 60-80 | 🟡 MODERATE | Cut possível em stress extremo |
| 40-60 | 🟠 WEAK | Watch payout + FCF trends |
| < 40 | 🔴 DANGER | Cut provável nos próximos 2y |

## Exemplos no portfolio

| Ticker | Score | Breakdown |
|---|:-:|---|
| [[JNJ]] | ~95 | Payout 47%, streak 62y, ROE 24%, net cash |
| [[ACN]] | 95 | Payout 25%, streak 22y, ROE 25%, net cash |
| [[O]] | ~75 | Payout 72% (REIT — normal), streak 28y, ROE 4% |
| [[TEN]] | ~40 | Payout volátil, streak cortado 2025, Altman distress |
| [[PLTR]] | N/A | Não paga |

## Red flags que destroem score

1. **Payout > 100% em recessão** → corte eminente (GE 2017, BPS 2016)
2. **Debt refinancing wall + rates high** (BPS, XRX)
3. **Special dividend "one-time"** — sinaliza gestão não sabe o que fazer
4. **Dividend > FCF sistemático** — financiado por emissão/dívida

## Como interage com outros scores

- **Altman 1.81 (distress)** → Dividend Safety matters less (equity wipeout > cut)
- **Piotroski ≤ 3** → ΔROA caindo mais do que payout growth = watchlist
- **Aristocrat streak + Safety > 80** → core DRIP candidate

## No nosso código

`scoring/dividend_safety.py::compute` + em `scripts/verdict.py` (quality 35% weight) + em `obsidian_bridge` frontmatter `div_safety`.

---

> **Fontes**: Simply Safe Dividends (Brian Bollinger) methodology; S&P Aristocrats criteria (25y); Mergent's Dividend Achievers; nosso código em `scoring/dividend_safety.py`.
