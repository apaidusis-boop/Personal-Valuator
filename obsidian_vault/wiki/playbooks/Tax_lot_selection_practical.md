---
type: playbook
name: Tax Lot Selection — Practical JPM Steps
tags: [playbook, tax, jpm, spec_id, execution]
related: ["[[Tax_lot_selection]]", "[[US_LTCG_STCG]]", "[[Sell_triggers]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 📋 Tax Lot Selection — JPM UI steps

> Operational playbook para aplicar [[Tax_lot_selection]] na prática via JPM (Chase Wealth Management).

## One-time setup

### 1. Configurar default cost basis method

JPM Chase website:
1. **Log in** → Investments tab.
2. **Account settings** → "Cost Basis".
3. **Default method**: change from "FIFO" (default) to **"Specific Lot Identification"**.
4. Confirm.

Mobile app: Settings → Investments → Cost Basis → Select method.

Fidelity equivalent: Account Features → Lot Depletion Method → "Specific Shares".

### 2. View holdings with lot detail

JPM:
1. Investments → Holdings.
2. Click ticker → "Cost Basis" tab.
3. Table shows lots: date, qty, basis, current value, unrealized gain, holding period (short/long).

### 3. Export for records

JPM → Statements & Documents → Tax Forms → Year-end 1099-B → CSV download.

Import para nosso tracking:
```bash
python scripts/import_tax_lots.py --file 1099-B-2025.csv   # se implementado
sqlite3 data/us_investments.db "SELECT * FROM tax_lots WHERE ticker='JNJ'"
```

## Execution — sell with specific lots

### Step 1 — Open trade ticket

1. JPM → Trade → Sell.
2. Select account + ticker.
3. Enter quantity.

### Step 2 — Before confirming, click "Cost Basis Method"

- If you didn't set default, selector appears.
- Choose **"Specific Lots"**.

### Step 3 — Lot selection modal

Tabela aparece com:
- ✅ checkbox
- Date acquired
- Qty
- Basis / share
- Current gain/loss
- Holding period (LT / ST)

**Select strategy based on goal**:

### Strategy A — Tax-loss harvesting

Goal: realize maximum loss deductible.

Select: **highest-basis lots** (maior unrealized loss).

Example:
```
Lot 1: 2023-02 — 100 @ $50 (basis $5,000) — LT — current $3,000 — loss $2,000 ⬅ select
Lot 2: 2024-06 — 50 @ $40 (basis $2,000) — LT — current $1,500 — loss $500
Lot 3: 2025-03 — 30 @ $35 (basis $1,050) — ST — current $900 — loss $150
```

Select Lot 1 = realize $2,000 loss. Max deduction.

### Strategy B — Minimum LTCG on partial exit

Goal: realize small gain para raise cash.

Select: **lowest-gain LT lots** (> 1 year).

Example:
```
Lot 1: 2020-05 — 100 @ $30 — LT — current $90 — gain $60/share ($6,000)
Lot 2: 2022-11 — 100 @ $75 — LT — current $90 — gain $15/share ($1,500) ⬅ select
Lot 3: 2024-09 — 50 @ $85 — ST — current $90 — gain $5/share ($250)
```

Select Lot 2 = $1,500 LTCG (15% tax = $225). Much better than FIFO selling Lot 1 ($6k gain → $900-1200 tax).

### Strategy C — STCG avoidance

Goal: partial exit without touching short-term lots.

Select: **LT lots only**, skip any < 1 year.

Algorithm: sort by holding date ASC, fill qty from oldest LT until quota met, skip ST.

### Strategy D — Maximum step-up for heirs (advanced)

Goal: retain lowest-basis lots para heir step-up at death.

Select: **highest-basis lots** first for selling (keep deep-in-money old lots untouched).

Rare: only if estate planning is meaningful for teu situation.

### Step 4 — Confirm total

Modal totals:
- Qty sold
- Total basis
- Realized gain/loss
- Tax estimate (LTCG @ 15/20% + state)

**Double check** before click confirm.

### Step 5 — Execute + journal

Click "Place Order". Trade confirms T+1.

Journal immediately:
```bash
python scripts/notes_cli.py add AAPL "SELL 100 @ $250 — Spec ID Lot 2022-11 = $1,500 LTCG" --tags sell,tax
```

## Common JPM gotchas

### Gotcha 1 — Market order defaults to FIFO
If you use "Market Order" and don't click Cost Basis first, JPM uses default (FIFO unless changed in account settings).
**Fix**: set default in account settings Step 1 above.

### Gotcha 2 — Fractional shares auto-washed
If you sell "100 shares" but lot has "99.76" and DRIP added "0.24" later:
- JPM may split across lots.
- Verify sale confirmation 1099-B carefully.

### Gotcha 3 — Dividend reinvestment creates many tiny lots
Every DRIP creates new lot (1.2 shares @ $X, 0.8 shares @ $Y, etc).
After 3 years: 12 quarterly lots for 1 ticker. Tedium to select manually.

**Fix**:
- Pause DRIP on positions not being trimmed frequently.
- Or: consolidate lots via "Move to long-term" annually.

### Gotcha 4 — Transfer in-kind preserves basis
If transferring JNJ from Schwab → JPM, basis + holding period preserved (if broker reports correctly).
- Confirm 1099-B next year reflects pre-transfer basis.
- If "Cost basis: Not reported" flag: need Schwab cost basis report + upload.

### Gotcha 5 — Wash sale across accounts
If sell AAPL loss in JPM + buy AAPL in IRA within 30 days → wash rule applies **across accounts**.
- Loss disallowed AND basis in IRA steps up by disallowed amount.
- **But IRA has no basis** (tax-deferred) → loss **permanently lost**.

**Fix**: coordinate accounts. Don't buy back in IRA after taxable loss sell.

## Estratégias por situação real

### Situação: year-end TLH

**December 20-29**:
1. Review unrealized losses > $500 across all holdings (both accounts).
2. For each: select HIFO lots → sell.
3. Immediately buy non-identical substitute (not VOO for SPY; different fund/sector).
4. 31+ days later: can repurchase original if desired.
5. Total loss harvest: $3k off ordinary income + carry forward excess.

### Situação: partial trim for rebalance

**Any time**:
1. `ii rebalance` shows ACN 12% vs 8% target.
2. Need sell ~30 shares ACN (=4% trim).
3. In JPM: sell 30, Spec ID → pick lowest-gain LT lots.
4. Minimize tax friction.

### Situação: charitable donation

Never sell first. Instead:
1. Transfer stock directly to 501(c)(3) charity.
2. Lot selection: **highest-gain lots** → donor gets FMV deduction + charity gets full value + **zero realize**.
3. Paperwork: Form 8283 if > $500 annual charitable stock donation.

### Situação: inheritance planning

Multi-decade Aristocrat hold strategy:
1. Never sell — hold till death.
2. Heir inherits with step-up basis.
3. Zero capital gains tax on all historical gains.

This requires **discipline not to sell in volatility**.

## Annual review (December)

Each December, do:
1. **Cost basis report** — download all 1099-B projections.
2. **Realized gains/losses YTD** — tally.
3. **TLH opportunities** — scan unrealized losses.
4. **Forward plan** — identify lots becoming LT in next 12m (avoid selling before).
5. **Export records** to local archive for safety.

## Our DB integration

Nossa `tax_lots` table armazena:
- ticker, lot_date, qty, basis_usd, holding_period_class, source ("jpm" | "fidelity")

Update via:
```bash
python scripts/update_tax_lots.py --file 1099-B-2025.csv
python scripts/tax_lot_report.py --ticker AAPL
```

Vault `TaxLots.md` dashboard auto-populates from this.

## BR — nota residente

PF BR trading US via JPM:
- Usar Spec ID JPM lado.
- Converter para BRL usando PTAX data cada lot (compra + venda).
- Registrar em DARF mensal se ganho > R$ 35k/mês.
- Aplicar [[Dividend_withholding_BR_US]] para div income.

## Related

- [[Tax_lot_selection]] — theory
- [[US_LTCG_STCG]] — underlying law
- [[Sell_triggers]] — when to use
