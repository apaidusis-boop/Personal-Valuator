---
name: rebalance-advisor
description: Use this skill when the user asks about rebalancing, allocation
  drift, new cash deployment, or "onde adicionar/reduzir" in their portfolio.
  Examples - "tenho R$5000 onde aplicar", "rebalance a carteira", "minha
  alocação está desequilibrada", "drift vs target", "where should I add cash",
  "trim which position". Reads portfolio_positions + target weights + macro
  regime + thesis_health to suggest concrete trades. Respects BR/US currency
  isolation (memory rule).
---

# Rebalance Advisor Skill

Data-driven rebalance recommendations using existing infrastructure.

## When to trigger

- "Onde aplicar R$X?" / "tenho Y em cash"
- "Rebalance a carteira"
- "Que posições reduzir?"
- "Allocation drift"
- "Novo aporte"
- "Trim / add to X"

## Workflow

1. **Identify market + amount**: from prompt or default (ask if ambiguous)
   - **Critical rule**: BR cash → BR positions only. US cash → US positions only.
     NEVER suggest cross-market conversion.
2. **Pull current state**:
   ```bash
   # Portfolio
   sqlite3 data/<market>_investments.db "
     SELECT p.ticker, p.quantity, p.entry_price,
            (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) as last_price
     FROM portfolio_positions p WHERE active=1
   "

   # Macro regime
   python -m analytics.regime --market <br|us>

   # Thesis health (latest for each holding)
   # Query thesis_health with latest per ticker
   ```
3. **Compute drift**:
   - Current weight = (qty * last_price) / total
   - Target weight = from config or infer (equal-weight, or intent-based from [[user_investment_intents]])
   - Drift = current - target
4. **Apply decision rules**:
   - **ADD to**: underweight + thesis_score ≥ 70 + regime compatible
   - **TRIM from**: overweight + thesis_score < 70 OR R4 euphoria trigger
   - **HOLD**: otherwise
5. **Respect memory rules**:
   - `feedback_honest_projections` — no optimistic assumptions
   - `user_investment_intents` — differentiate DRIP vs growth picks
   - `carteiras_isoladas` — NEVER cross BR/US
   - `ten_distress_signal` — NEVER add TEN
   - `grek_irregular_dividends` — NEVER add GREK by DRIP logic
6. **Output**: concrete trade list in PT:

```markdown
## Rebalance suggestion — <R$/US$ X amount>

**Market**: <BR|US>
**Regime**: <expansion/late_cycle/...>  (weight: X% vs baseline)
**Portfolio total**: R$ X,XXX

### Actions
| Action | Ticker | Qty | Amount | Reason |
|---|---|---|---|---|
| ADD | ITSA4 | 50 | R$ 708 | Underweight 1.5pp + thesis 100/100 |
| ADD | TFC | 10 | R$ 350 | Underweight 2pp + thesis 82 + regime compatible |
| HOLD | ACN | — | — | Thesis 91 but R3 DD flag; wait 1 week |
| TRIM | — | — | — | No overweight triggering sell |

### Reasoning
<3-5 bullets explaining regime/thesis considerations>

### What NOT to do
<Specific anti-recommendations based on memory rules>
```

## Critical rules

- **NEVER suggest a trade without checking thesis_health**
- **NEVER exceed portfolio concentration limit** (configure: max 15% single ticker)
- **ALWAYS show math**: user sees current%, target%, delta
- **Currency lock**: BR only BR, US only US. Explicit warning if user mixes.
- **TEN/GREK blacklist**: hardcoded rules from memory

## Files reference

- `scripts/ii` → `ii rebalance` CLI (prefer if available)
- `config/targets.yaml` — if exists, target weights
- `data/{br,us}_investments.db` — portfolio_positions
- `agents/perpetuum_validator.py` — thesis_health
- `analytics/regime.py` — regime classifier
- memory: `user_investment_intents`, `carteiras_isoladas`, `ten_distress_signal`
