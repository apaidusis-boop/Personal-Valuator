---
type: playbook
name: Sell Triggers
tags: [playbook, sell, triggers, exit]
related: ["[[Buy_checklist]]", "[[Altman_Z]]", "[[Piotroski_F]]", "[[Dividend_Safety]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🚪 Sell Triggers — quando sair

> **Princípio**: venda deve ser regra-baseada. Emotional selling = wealth destruction.

## Categorias de venda

| Categoria | Velocidade | Exemplos |
|---|---|---|
| **Thesis-broken** | Imediato (D+1) | Dividend cut, CEO scandal, covenant breach |
| **Quality deterioration** | Ponderado (2-4 semanas) | Altman < 1.81, Piotroski ≤ 3, earnings miss pattern |
| **Valuation extreme** | Gradual (trim) | P/E 2-3× histórico, parabolic run |
| **Allocation drift** | Agendado | Ticker > 12% portfolio, sector > 25% |
| **Personal** | Planned | Liquidity need, tax optimization |

## 1. Thesis-broken (immediate sell)

**Critério**: o motivo pelo qual compraste **deixou de ser verdadeiro**.

### Dividend cut (para intent DRIP)
- [ ] Corte ou suspensão de dividendo pela empresa
- [ ] Ação: **SELL imediato** se intent era DRIP
- Exceção: cut temporário anunciado (e.g., INTC 2023) — pode valer esperar se tese turnaround ainda ativa

### Fraud / governance scandal
- [ ] SEC/CVM investigation aberta
- [ ] CEO/CFO departure sem replacement
- [ ] Auditor resignation
- [ ] Restatement 10-K/DFP
- Ação: **SELL imediato** — capital preservation > gain recovery

### Covenant breach
- [ ] ND/EBITDA > covenant trigger
- [ ] Interest coverage < 2×
- Ação: **SELL** dentro de 1-2 semanas (observar se renegotiation anunciada)

### Moat break evidence
- [ ] Perda de cliente top-3 com > 10% receita
- [ ] Preço concorrente destroi pricing power (KO vs Coca-Cola Kirkland)
- [ ] Regulatório revert moat (farma patente expirando + nenhum pipeline)
- Ação: **SELL / trim** 50% + re-avaliar

## 2. Quality deterioration (medium-speed)

### Altman Z-Score veto (para não-financeiros)
- [ ] Z < 1.81 (distress zone) por 2 quarters
- Ação: **SELL 50-75%** — preservar capital em risco insolvência
- `python -m scoring.altman <TICKER>`

### Piotroski F-Score veto
- [ ] F ≤ 3 por 2 quarters
- Ação: **SELL 50%** — fundamentals compounding negative
- `python -m scoring.piotroski <TICKER>`

### Dividend Safety < 40
- [ ] Score < 40 (eg payout > 90% + FCF < dividend + streak broken)
- Ação: **TRIM 50%** para intent DRIP
- `python -m scoring.dividend_safety <TICKER>`

### Earnings miss pattern
- [ ] 3 consecutive quarterly earnings misses vs consensus
- [ ] Guidance cut > 15%
- Ação: **TRIM 33%**, re-avaliar FY guidance reset

## 3. Valuation extremes (gradual sell)

### P/E histórico
- [ ] P/E > 150% do 10y avg → TRIM 25%
- [ ] P/E > 200% do 10y avg → TRIM 50%

### Parabolic move
- [ ] Preço +50% em 3 meses sem fundamental change (capital gain realization)
- Ação: **TRIM 25%** para gestão risco, não exit

### DY suppressed (DRIP-focused)
- [ ] DY atual < 50% DY histórico 5y avg
- Ação: **TRIM 20-30%** em growth/quality rotation

### Peer relative
- [ ] P/E 2× peer group median sem growth differential justifier
- Ação: **TRIM + rotate** para peer cheaper

## 4. Allocation drift (scheduled)

### Concentration limits
- [ ] Single ticker > 10% → TRIM down to 8%
- [ ] Sector > 25% → TRIM ou pausar reforços
- [ ] Single country > 65% → diversify ou pausar

```bash
ii rebalance                     # detecta drift
ii peers <TICKER>                # confirma over-weight
```

### Target weight deviation
- Define target weights em `config/allocations.yaml` (ou carteira ideal mental)
- TRIM se +50% acima target, ADD se -50% below

## 5. Personal / practical

### Tax loss harvesting (US)
- [ ] Position unrealized loss > $500 near year-end
- Ação: **SELL + repurpose** (compra substitute non-identical) para TLH
- 31 days later: recompra se ainda desejar
- Ver [[Tax_lot_selection]]

### Liquidity need
- [ ] Emergency expense
- Ação: SELL **lowest-gain LTCG lots first** (minimize tax)

### Tax optimization pre-PL 1.087 (BR)
- Se [[BR_dividend_isencao]] PL aprovar: antecipate realization
- TRIM winners em 2026 pre-deadline

## Our trigger system — automated signals

`config/triggers.yaml` + `scripts/trigger_monitor.py` dispara automáticamente:

| kind | Descrição | Action hint |
|---|---|---|
| `price_drop_from_high` | Preço caiu X% de máx lookback | BUY / ADD (contrarian) |
| `dy_above_pct` | DY acima absoluto threshold | BUY |
| `dy_percentile_vs_own_history` | DY no top percentile histórico | BUY (entry context) |
| `altman_distress` | Z < 1.81 | SELL / TRIM / REVIEW |
| `piotroski_weak` | F ≤ 3 | SELL / TRIM / REVIEW |

```bash
python scripts/trigger_monitor.py --market us     # corre todos
python scripts/action_cli.py list                 # lista abertos
python scripts/action_cli.py resolve <id> --note "sold 50 @ $X"
python scripts/action_cli.py ignore <id> --note "thesis intact"
```

## Execution checklist (antes de clicar SELL)

- [ ] Trigger identificado e classificado (thesis-broken / quality / valuation / drift / personal)
- [ ] Tax implication verificada ([[Tax_lot_selection]] método Spec ID se US taxable)
- [ ] Size calculado (total vs partial — 25/50/75/100%)
- [ ] Alternative confirmed (if rotation, where does cash go?)
- [ ] Journal entry draft pronto

## Journal template SELL

```bash
python scripts/notes_cli.py add <TICKER> "SELL X @ Y = $Z — reason: ..." --tags sell,exit
```

```
[2026-04-XX] SELL TAEE11 500 @ R$ 42.00 = R$ 21,000
Reason: Allocation drift (8.5% → 12% após rally)
Tax lot: older 200 @ R$ 32, newer 300 @ R$ 38 (Spec ID Q1 2023 mais tarde)
Gain: R$ 5,000 LTCG 
Redeploy: R$ 10k para ITUB4 (sub-allocated, DY 8%)
Journal: triggered by ii rebalance
```

## Common pitfalls

1. **Hope-holding**: "quando voltar ao breakeven eu vendo" → sunk cost fallacy. Evaluate fresh.
2. **Selling winners too soon**: reg to mean bias. Compounders destroying "expensive" = erro. Use **trim 20-25%** para lock some gain sem forfeit full upside.
3. **Panic in drawdown**: drawdown -30% sem thesis break = **add not sell**. Trigger `price_drop_from_high` é BUY hint, not SELL.
4. **Ignoring quality signals**: Altman/Piotroski deterioration waiting "mais 1 quarter" → posição colapsa.
5. **Tax procrastination**: evitando realize loss → capital bleeding ongoing vs tax deduction $3k + carry forward.

## Related

- [[Buy_checklist]] — mirror de entry
- [[Rebalance_cadence]] — when scheduled sells happen
- [[Dividend_Safety]] — quant signal pré-cut
- [[Tax_lot_selection]] — execution optimization
