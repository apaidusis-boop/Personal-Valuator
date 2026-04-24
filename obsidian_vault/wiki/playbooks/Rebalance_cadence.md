---
type: playbook
name: Rebalance Cadence
tags: [playbook, rebalance, allocation, drift]
related: ["[[Buy_checklist]]", "[[Sell_triggers]]", "[[Kelly_criterion]]"]
---

# 🔄 Rebalance Cadence

> **Princípio**: rebalance é **disciplina mecânica**, não market timing.

## Cadência recomendada

| Frequência | O quê |
|---|---|
| **Mensal** | Log of net cash flow + DRIP + nova entrada cash |
| **Trimestral** | Drift check vs target (relatório automático) |
| **Semestral** | Real rebalance execution (acting on drift) |
| **Anual** | Target weights review (macro / life changes) |

Trading rebalances monthly = **over-trading** (friction + tax drag).
Rebalancing uma vez/ano apenas = drift muito grande entre execuções.
**Sweet spot**: 6 meses + ad-hoc se drift > 3pp.

## Target weights framework (exemplo teu perfil)

```
Target      Banda de tolerância
─────────────────────────────────
BR equity    45%    (40-50%)
US equity    40%    (35-45%)
BR RF        10%    ( 5-15%)
Cash USD      3%    ( 1- 5%)
Cash BRL      2%    ( 1- 5%)
─────────────────────────────
Total       100%
```

**Single ticker max**: 8% (12% hard cap).
**Sector max**: 20%.
**Currency**: ~60/40 BRL/USD (flex +/- 10pp tolerated).

## Rebalance checklist

### Step 1 — Snapshot

```bash
ii rebalance              # current vs target drift
ii fx --total             # BR+US em BRL
python scripts/portfolio_report.py
```

Anotar:
- Total portfolio (BRL equivalent)
- Drift per major category (> 3pp = acting)
- Concentration violations (single > 10%, sector > 25%)

### Step 2 — Classify drift source

Drift pode vir de:

1. **Price appreciation** (good problem)
2. **New cash flows** (DRIP + externo)
3. **Scheduled buys/sells**
4. **Currency movement** (BRL/USD change)

**Impact**: trim "up-drifted" para pay lucros (se LTCG), reinvest em "down-drifted" para mean revert.

### Step 3 — Consideração tax

Antes de trim:
- [ ] Qual é o tax cost? (realize LTCG = 15-20% US, zero BR dividendo retornados)
- [ ] Há loss harvest opportunities para offset?
- [ ] A posição tem lots > 1 ano (LTCG) vs < 1 ano (STCG)?

Ver [[Tax_lot_selection]] — **Spec ID** para trim específicos.

Rebalance **pode ser via new cash primariamente** — evita realize tax:
- Se BR drift abaixo 5pp: alocar 100% new cash para BR until back em target.
- Se US drift acima 5pp: pause US buys até BR catch up.
- **"Rebalance by addition" > "rebalance by subtraction"** sempre que cash flow permite.

### Step 4 — Execute

Priority rules:
1. **Concentrations violations** (> 12% hard cap) — imediato sem discussão
2. **Sector drift > 7pp**
3. **Currency drift > 10pp**
4. **Overall equity/RF drift > 5pp**

Execute via:
- BR: corretora (XP, Clear).
- US: JPM / Fidelity — use Spec ID tax lot method.

### Step 5 — Journal

```bash
python scripts/notes_cli.py add PORTFOLIO "Rebalance 2026-Q2: ..." --tags rebalance
```

Estructure:
```
[2026-04-XX] Quarterly rebalance
Pre-state:
- BR 48%, US 45%, RF 7% (drift US +5pp)
- Violation: ACN 11% (target 8%)

Actions:
- TRIM ACN 20 @ $182 = $3,640 (Spec ID lots 2024)
- Redirected to BBSE3 (BR under-weight, DY 9.5%, intent DRIP core)
- Result: BR 49%, US 40%, ACN 8.2%

Tax:
- LTCG $1,100 @ 20% US = $220 tax (acceptable vs drift risk)
```

## Rebalance-by-contribution (preferred)

Se houver cash flow mensal (salário, dividendos):

1. Calculate current allocation vs target.
2. Apply **100% new cash to under-weight category** até se alinhar.
3. **Zero selling** → zero tax, zero friction.
4. Revisit após 3 meses.

**Exemplo**: drift mostra US 45% vs 40% target. BRL dividendos recebidos R$ 5k/mês:
- Alocar 100% dos R$ 5k em BR equities até US drift abaixar naturalmente (por BR grow + US flat or DRIP).
- 6 meses depois: reavaliar.

## DRIP integration

**DRIP auto-reinvest NÃO deve alterar allocation conscious**:
- BR FIIs: dividendo BRL → reinveste no próprio FII (manual usually).
- US stocks: DRIP program broker (JPM/Fidelity auto).
- **Risk**: concentração silenciosa. Ex: TAEE11 pagando 8% DY auto-reinvested = +8% position year-1. Em 5y: +40% original (compounding).

**Fix**: override DRIP auto para tickers già em target. Usar dividendo cash para **under-weight** em vez.

## Indicators de "bad drift"

- [ ] Category drifted via single ticker appreciation (concentration)
- [ ] Currency drifted > 10pp from target (FX move)
- [ ] Sector dominated by 1 ticker (VALE3 → Mining 100%)
- [ ] RF too low in bear market (emergency liquidity)
- [ ] RF too high in bull market (opportunity cost)

## Currency rebalance (BRL ↔ USD)

**Never rebalance BRL → USD via FX trade directly**. Brokerage FX spreads matam.

Vias validas:
1. **BDR compra** (US stock equivalent em B3) — usa BRL.
2. **USD-inflow allocation** — salary USD, dividends US → vai para US buys.
3. **Longer horizon rebalance natural** via asymmetric growth.
4. **Worst case**: transferência via Wise/IB com spread mínimo (0.3-0.5%).

Ver memória `feedback_carteiras_isoladas.md` — **não misturar** BRL+USD activamente.

## Red flags

- Rebalance every month → over-trading.
- Never rebalance → drift 15pp+ = uncontrolled exposure.
- Always rebalance at year-end → tax bunched into Q4.
- Ignoring concentration violations hoping "it'll normalize" → crash dangerous.
- Rebalancing DURING panic (selling low, buying high against reversion).

## Tools

```bash
ii rebalance [--cash-add 5000]       # diff + suggestion
ii rebalance --md                    # export markdown
python scripts/portfolio_report.py   # full briefing
ii peers <TICKER>                    # percentil vs sector holdings
```

## Annual review (January)

Uma vez por ano, revisita target weights:
- [ ] Life change? (job, kids, home purchase)
- [ ] Income stability change?
- [ ] Risk tolerance? (market volatility tolerance)
- [ ] Tax situation changes? (PL 1.087 if approved)
- [ ] Currency view change? (BRL secular weakening/strengthening outlook)

Adjust targets em config mental + document reasoning.

## Related

- [[Buy_checklist]] — new positions
- [[Sell_triggers]] — exit mechanics
- [[Kelly_criterion]] — size math
- [[Tax_lot_selection]] — execute optimization
