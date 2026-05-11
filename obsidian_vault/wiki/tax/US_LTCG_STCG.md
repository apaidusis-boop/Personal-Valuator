---
type: tax
name: US Capital Gains — LTCG vs STCG
region: US
tags: [tax, us, capital_gains, wash_sale, regulatory]
related: ["[[Tax_lot_selection]]", "[[Dividend_withholding_BR_US]]", "[[BR_dividend_isencao]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🇺🇸 US — Long-term vs Short-term Capital Gains

## Holding period define everything

| Holding | Nome | Taxa |
|---|---|---|
| ≤ 1 ano | **Short-term (STCG)** | Ordinary income (10-37% federal) |
| > 1 ano e 1 dia | **Long-term (LTCG)** | 0%, 15% ou 20% federal |

**O dia exacto**: comprou 2026-01-15 → venda elegível LTCG a partir de 2027-01-16.

## LTCG brackets (2025, ajustam CPI)

Single filer:
| AGI | LTCG |
|---|---|
| ≤ $47,025 | **0%** |
| $47,025–$518,900 | **15%** |
| > $518,900 | **20%** |

Married filing jointly:
| AGI | LTCG |
|---|---|
| ≤ $94,050 | **0%** |
| $94,050–$583,750 | **15%** |
| > $583,750 | **20%** |

**Plus**: 3.8% Net Investment Income Tax (NIIT) para single > $200k / MFJ > $250k.

Total topo: 20% + 3.8% NIIT = **23.8%** federal.

## State tax variation

Estados sem state income tax (bons para LTCG):
- Texas, Florida, Nevada, Tennessee, Washington (sem LTCG tax excepto Washington 7% > $250k), Wyoming, South Dakota, New Hampshire.

Estados com state LTCG tax alta:
- California: **13.3% top** (no LTCG distinction — same as ordinary).
- New York: 10.9% top.
- Hawaii: 11%.
- New Jersey: 10.75%.

**California total top**: 20% federal + 3.8% NIIT + 13.3% state = **37.1%** em LTCG.

## Short-term = ordinary income

STCG é tratado como salário:
- 2025 top federal bracket: 37% (single > $609,350; MFJ > $731,200).
- + 3.8% NIIT.
- + state.
- **California + federal + NIIT**: **53.1%** STCG top.

## Implicações estratégicas

### 1. Hold > 1 year SEMPRE se possível
- Passar de STCG 37% → LTCG 20% = savings 17pp absolut.
- Em $10,000 ganho: $1,700 extra se LTCG.

### 2. Holding period tracking
- JPM/Fidelity mostra "Tax lot status: long term / short term".
- **Gift / inheritance resets** holding period de herança (starts over at step-up basis).

### 3. Investor-residente BR holding US stocks
- **0% US federal capital gain** para não-residente (IRS treaty + foreign investor exemption).
- **Pagar IR BR** sobre ganho: 15% comum, até 22.5% se ganho > R$ 5M.
- Aplicar **tax credit** se houver treaty — **mas BR não tem treaty US ativa** (assinado 1967 nunca ratificado).
- Na prática: BR PF trader US paga 0% US + 15% BR = 15% total.
- Registro BR via DAA e DARF mensal se > R$ 35k/mês (mesmo raciocínio BR stocks).

## Wash Sale Rule (IRC 1091)

**Proíbe**: vender perda + recomprar "substantially identical" dentro de 30 dias (antes+depois).

**Efeito**: perda **disallowed** e added to basis da nova compra.

**Aplica**:
- Mesma ação (óbvio).
- Mesma ETF (óbvio).
- **Substantially identical**: SPY vs IVV (S&P 500) — sim, washed. VOO vs IVV também. SPY vs RSP (equal weight) — não, estrategia diferente.
- ETF sector vs 1 stock do sector — NÃO é washed geralmente.
- Call option vs underlying — YES if deep-in-money, ambigous otherwise.

**Strategy tax-loss harvest (TLH)**:
- Sell AAPL loss → buy MSFT imediatamente → wait 31 days → buy AAPL de volta se ainda quiser.
- Sell SPY loss → buy VOO imediatamente (**ERRO** — substantially identical).
- Sell VTI loss → buy ITOT (iShares total market) — **borderline**, muitos fiscal advisors evitam.

**Multiple accounts**: wash sale aplica **across** accounts (individual + IRA combinado). Comprar em IRA depois de vender perda taxable = wash → perda **perdida permanentemente** (IRA basis não step up).

## Tax-loss harvesting strategy

1. Final de ano: review positions unrealized loss > $500.
2. Sell losses → imediato switch para similar-but-not-identical (ex: VTI → ITOT cuidado).
3. 31 days later: switch back se desejar original.
4. **Deduct $3,000/y contra ordinary income** + carry forward excess.
5. Ganhos (LTCG) paired against losses → reduce taxable.

**Efeito**: +1-2%/y boost em after-tax return em taxable accounts de high earners.

## Qualified vs non-qualified dividends

### Qualified (15-20%+3.8% NIIT)
- US corp stocks held > 60 days around ex-div.
- Also: certain foreign ADRs (qualified foreign corp + treaty).

### Non-qualified (ordinary 10-37%)
- REITs distributions (majority).
- BDCs.
- Foreign stocks no-treaty.
- Mutual funds de income type.

**Implicação REITs**: O, SPG, AVB, etc pagam **ordinary income tax**. Em CA top bracket: 37% + 3.8% + 13.3% = **~54%** em REIT dividends para holder residente CA.

→ REITs vantagem **menor em taxable** account; coloque em IRA/401k idealmente.

## Tools + Reporting

- **Form 8949** + **Schedule D** para sales.
- **1099-B** brokerage gera automaticamente (JPM, Fidelity).
- Software: TurboTax, HR Block, FreeTaxUSA importa 1099-B.

## Red flags

- Broker mark "Cost basis not reported" → responsabilidade investidor reconstruir.
- ETF distribution 100% ordinary = REIT/BDC focused (not qualified).
- Wash sale losses "disallowed" em 1099-B — adicionam à base da nova compra.

---

> Ver [[Tax_lot_selection]] para optimização FIFO vs Spec ID. [[Dividend_withholding_BR_US]] para holders BR no US.
