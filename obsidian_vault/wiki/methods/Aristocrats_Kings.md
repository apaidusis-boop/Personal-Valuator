---
type: method
name: Dividend Aristocrats & Kings
category: income
tags: [method, dividend, aristocrats, kings, drip]
related: ["[[Dividend_Safety]]", "[[DRIP_compounding]]", "[[Buffett_quality]]", "[[Kings_aristocrats_trap]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Dividend Aristocrats e Kings

## Definições oficiais

### S&P 500 Dividend Aristocrats
- Membro do **S&P 500**
- **≥ 25 anos consecutivos** aumentando dividendo (não apenas pagando)
- Market cap ≥ $3B
- Liquidez mínima ($5M daily trade)
- Rebalance trimestral pelo S&P

**~67 empresas em 2024** (varia).

### Dividend Kings
- **≥ 50 anos consecutivos** aumentando dividendo
- Sem requisito S&P 500 (pode ser mid-cap)
- ~50 empresas

### Dividend Aristocrats vs Kings vs Champions
| Designação | Anos | Coverage |
|---|---|---|
| **Challengers** | 5-9y | Early stage |
| **Contenders** | 10-24y | Proven |
| **Aristocrats** | ≥ 25y (S&P500) | Blue-chip |
| **Kings** | ≥ 50y | Legends |

## Por que a streak importa

**1. Proxy de cultura corporativa**: management que priorisa shareholder return a longo prazo.

**2. Business model moat**: só empresas com **pricing power estável** e **FCF resiliente** sobrevivem 25+ anos aumentando div — muitas recessões no meio (1990, 2001, 2008, 2020).

**3. Psicologia da gestão**: cortar streak é **tabu** no board — cria discipline de capital allocation.

**4. Evidência empírica**: S&P Aristocrats outperformed S&P 500 com menor vol em períodos longos (2000-2020).

## Armadilhas ([[Kings_aristocrats_trap]])

### Streak a ponto de quebrar
- **T (AT&T)** cortou em 2022 após 37y (fusion WBD → dividend diluído)
- **GE** cortou 2009 durante GFC
- **Wells Fargo** cortou 2020 COVID

Sinal cedo: payout > 80% + growth estagnou + debt refinancing iminente.

### "Streak artificial"
Alguns mantêm streak aumentando 1-2c por ano (simbólico) — KMB, 3M fazem isto em stress.

### Setor em decline estrutural
- **Consumer staples** anos 2010-2020: KO, PEP, MCD, PG bateram inflação apenas
- **Tobacco**: MO dividend subiu mas stock caiu 50% — total return negativo

## No nosso sistema

`config/kings_aristocrats.yaml` tem **87 tickers** canonical list. Loaders automáticos em `fetchers/yf_us_fetcher.py` + `scripts/daily_update_us.py`.

Memória: [[Kings & Aristocrats yaml]]

## Critério relaxado no nosso scoring

`scoring/engine.py::score_us` aceita **10y streak** (não 25y) para não excluir:
- Companies que pararam aumento mas continuam pagar (PFE, OXY)
- Spin-offs recentes (WBD, KDP)
- BDCs / REITs com streak reset por merger

Aristocrat **tag** usada como **tiebreaker** em decisões de allocation, não como hard screen.

## Lista-tier do nosso vault

- **Tier S** (Kings 50+): KO, PG, JNJ, MCD, CINF, LANC, HRL, LOW, MKC, ADP
- **Tier A** (Aristocrats 25-50): PEP, CL, CLX, EMR, ABBV, WMT, TGT, CVX, ABT
- **Tier B** (Contenders 10-25): V, MA, AVGO, COST

## Como investir em Aristocrats

### ETF: NOBL (ProShares S&P Aristocrats)
- Expense ratio 0.35%
- Rebalance trimestral, equal-weight
- Under-performs single-picks se escolheres bem

### Single-picks (nosso approach)
- Screen Buffett/Graham + aristocrat + DY decente
- DCA trimestral sobre bearish news (ACN 2026-04 exemplo)
- [[DRIP_compounding]]

## Total return ao longo do tempo

1990-2020 benchmark:
- S&P 500: ~10.2%/y
- Aristocrats: ~11.8%/y (menor drawdown -34% vs -51% em 2008)
- Kings: ~12-13%/y

Fonte: ProShares NOBL factsheet + Wisdom Tree.

---

> **Fontes**: S&P Dividend Aristocrats methodology; Daniel Peris *The Strategic Dividend Investor*; SureDividend.com; nosso [[Kings_aristocrats_trap]] para armadilhas.
