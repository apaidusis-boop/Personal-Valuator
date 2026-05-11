---
type: macro
name: VIX — Volatility Index
category: sentiment
tags: [macro, vix, volatility, fear_index, sentiment]
country: US (primary)
source: CBOE
related: ["[[Fed_funds]]", "[[10Y_Treasury]]", "[[Short_interest]]"]
source_class: derived
confidence: 0.7
freshness_check: 2026-04-30
---

# VIX — "Fear Index"

## O que é

CBOE Volatility Index — mede **volatilidade implícita** de opções sobre S&P 500 dos **próximos 30 dias**. Expressado como **standard deviation anualizada**.

Alcunha: **"fear gauge"** (Wall Street Journal 2003).

## Cálculo simplificado

Média ponderada de opções SPX calls e puts em múltiplos strikes, prazo 23-37 dias. Formula CBOE detalhada incorpora variance swap pricing.

Output: **valor 10-80** tipicamente, expresso em **annualized volatility %**.

## Zonas

| VIX | Regime | Exemplo |
|:-:|---|---|
| < 12 | Extreme complacency | 2017, early 2020 |
| 12-18 | Low vol bull | 2019 |
| 18-25 | Normal | Média long-run |
| 25-35 | Elevated / correction | 2022 bear start |
| 35-50 | Panic / crisis | 2008 Oct, 2011 Aug |
| > 50 | **Black swan** | 2008 Lehman (80), 2020 COVID (82) |

## O que VIX mede (e não mede)

### Mede:
- Options dealers' **demand for hedge**
- Market's 30-day ahead variance expectation

### **NÃO** mede:
- Directional expectation (up or down)
- Long-term volatility
- Specific event risk (earnings, Fed)

## Reversion characteristics

VIX é **mean-reverting** — 2 regimes:
1. **Low vol**: 12-20, sticky (meses/anos)
2. **High vol spike**: 40+, rarely sustained > 2-3 meses

**Média long-run**: ~19-20.

**Half-life** de spikes: ~20 dias.

## Como usar em equity investing

### Como **signal de medo extremo** (contrarian buy)
- **VIX > 35** historicamente = **within 3-6m bottom** em 75% casos
- Nassim Taleb insight: buy stocks quando VIX alto (cheap)
- Buffett: *"Be greedy when others are fearful"*

**Anti-pattern**: trying to time exactly o topo do VIX spike. Melhor: DCA durante panic.

### Como **signal de complacency**
- **VIX < 12** = "things are too quiet"
- Setup for surprise crash (2018 Feb, 2020 Feb)
- Trim ou hedge neste regime

### Como **regime classifier**
- Persistent VIX > 20 → regime "volatile" (bear market, crisis)
- Persistent VIX < 16 → regime "calm" (bull)

## Correlação com equity

**Correlação VIX vs S&P 500**: **-0.75** (strong negative)
- S&P up 1% → VIX down ~5%
- S&P down 1% → VIX up ~7% (asymmetric — skewness)

**Não é simétrico** — panic pull is stronger than calm drift.

## VIX futures e VXX

- **VIX futures** tradam diferentes maturities (M1, M2, ...)
- **Contango** típico (M2 > M1 > spot): custo de roll destrói long-only positions
- **VXX ETN**: perde ~40%/y em contango mesmo em mercado calmo
- Só hedging tactical (dias/semanas), não long-term

## Brazilian equivalent (quase-)

**VINDEX** ou **IBOVESPA volatility** — não é tão padronizado quanto VIX. **Mais útil** usar:
- IBOV realized vol últimos 30d (via `prices` table)
- Credit spreads BR (CDS 5Y)
- Implied vol de opções IBOV (via B3 se disponível)

## Histórico de picos extremos

| Data | VIX close | Evento |
|:-:|:-:|---|
| 2008-10-24 | 80 | Lehman aftermath |
| 2015-08-24 | 40 | China devaluation shock |
| 2018-02-05 | 37 | "Vol-mageddon" (XIV ETN crashed) |
| 2020-03-16 | **82** | **COVID panic peak** |
| 2022-06-13 | 35 | Inflation shock |

## No nosso sistema

Actualmente **não puxamos VIX** — pendente adicionar ao `fetchers/fred_fetcher.py` (series VIXCLS).

Benefício: input de regime + alerta em ticker note "mercado em pânico, avaliar DCA".

## Como usar em decisions

### Daily workflow
1. Check VIX em `ii brief` (se integrated)
2. Se VIX > 30 e verdicts BUY piled up → opportunity
3. Se VIX < 12 por semanas → avaliar reduzir risk

### Event-driven
- **Pre-earnings**: VIX subir = implied vol alta = **opção short-strategies** (covered call)
- **Pre-FOMC**: VIX frequently spike + reverse pós-meeting

### Portfolio sizing
- VIX > 30: reduz Kelly sizing (edge blur, costs increase)
- VIX < 15: normal sizing

---

> **Fontes**: CBOE VIX methodology (cboe.com/tradable_products/vix); Nassim Taleb *The Black Swan*; Edward Chancellor *Devil Take the Hindmost*; VIX FAQs por CFA Institute.
