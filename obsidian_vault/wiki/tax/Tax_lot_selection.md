---
type: tax
name: Tax Lot Selection
region: US
tags: [tax, lot_selection, fifo, spec_id, optimization]
related: ["[[US_LTCG_STCG]]", "[[Dividend_withholding_BR_US]]", "[[BR_dividend_isencao]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 📋 Tax Lot Selection — método prático JPM/Fidelity

## O problema

Compraste AAPL em 3 momentos:
- 2023-02-01: 100 shares @ $140
- 2024-06-15: 100 shares @ $180
- 2025-11-10: 100 shares @ $230

Preço hoje: $250. Queres vender 100 shares.

**Qual lote vender** determina ganho capital + tax.

## Métodos disponíveis

### 1. FIFO (First In First Out) — default na maioria dos brokers
Vende a compra mais antiga primeiro.
- Vende 2023-02 lot: 100 @ $140 → ganho $110 × 100 = **$11,000** LTCG.

### 2. LIFO (Last In First Out)
Vende a compra mais recente primeiro.
- Vende 2025-11 lot: 100 @ $230 → ganho $20 × 100 = **$2,000 STCG** (< 1y).
- Menor ganho MAS STCG rate (ordinary, e.g. 32-37%).

### 3. Highest Cost (HIFO)
Vende o lote com menor ganho.
- Vende 2025-11 lot (highest basis $230).
- Ganho $2,000.
- **Se > 1 ano**: STCG. Se esperar até 2026-11 para vender: LTCG.

### 4. Specific Identification (Spec ID)
Investidor escolhe exatamente qual lot.
- Pode ser minha 2024-06 lot (100 @ $180).
- Ganho $70 × 100 = $7,000 **LTCG** (> 1 ano).
- Menor tax que FIFO ($7k × 20% = $1,400) vs FIFO ($11k × 20% = $2,200) = **savings $800**.

### 5. Minimum Tax (broker algorithm)
Broker calculates optimal combination para minimizar tax liability. Fidelity "Auto Tax Smart" e JPM versão disponível.

## JPM — como usar Spec ID

1. **Antes da venda**:
   - Settings → Cost Basis → Default method = **Specific Lot Identification**.
   - Ou escolher por trade.

2. **Durante a venda**:
   - Select "Sell" → ticker → quantity.
   - Menu "Cost Basis Method" → escolher **Specific lots**.
   - Modal exibe todos os lots → seleccionar manualmente.

3. **Fechamento T+1**: broker confirma selection.

4. **1099-B** reflete selection (basis reported vs not reported).

**Importante**: Se não configurar antes, JPM usa FIFO por default.

## Fidelity — same UI + automation

- **Tax Smart** algoritmo sugere optimal lot.
- Pode definir "Tax-sensitive minimized" a default account level.
- Reports granulares pós-venda.

## Strategy por situação

### Situação 1: Tax-loss harvesting
**Goal**: realizar perda para deduzir $3k + carry forward.
- Select **HIFO** → vende o lot mais caro (maior loss vs current price).
- Recompra NÃO-idêntica 31 days depois (wash sale rule).

### Situação 2: Minimizar tax em LTCG realization
**Goal**: realizar ganho but minimize tax.
- Select **Spec ID → lowest ganho AGE > 1 ano**.
- Prefere lots onde basis está perto do preço atual E holding > 1 ano.

### Situação 3: STCG avoidance
**Goal**: nunca realizar STCG se evitável.
- Select **FIFO** geralmente protege older lots (> 1y) from touch.
- Em position com compras recentes: **esperar > 1 ano** antes vender se possível.

### Situação 4: Partial position exit
**Goal**: vender metade, manter resto.
- Select **Spec ID → highest-gain long-term lots first** → maximize step-up (quase).
- Mantém lots de basis menor para herdeiros (step-up at death).

### Situação 5: Gift / charity
**Goal**: doar stocks em vez de cash.
- **Donate o lot com maior ganho** → evita realizing + donor writes off full market value.
- Don't sell first!

## Exemplo específico — Charity contribution

Paciencia:
- Compra JNJ 100 @ $50 em 2018.
- Hoje vale $160.
- Ganho $110/share × 100 = $11,000 LTCG se vender.
- Tax: $2,200 (20% LTCG).

Alternative: **doar directamente para charity**:
- Transfer stock to 501(c)(3) — charity receives $16,000 (100 × $160).
- Donor deducts $16,000 from AGI (up to 30% AGI limit).
- **Zero tax realized**.
- **Net benefit**: $16k deduction (at 32% marginal) = $5,120 saved + $2,200 tax avoided = **$7,320 benefit**.

## Step-up at death

- Heir inherits basis **= price at date of death** (FMV).
- Todos os ganhos pre-death são **erased**.
- **Massive planning tool**: HNW famílias mantêm compounders até morte, heir recebe basis alto, zero tax.

**Exemplo**: basis $10, atual $100, morre. Heir's basis = $100. Se heir sell imediato @ $100: $0 ganho, $0 tax.

Daí a estratégia **"buy and die"** para Aristocrat holdings.

## Red flags

- Broker default FIFO sem saber → sold oldest lowest-basis unecessarily.
- Partial exit sem Spec ID → algorítmo aleatório broker.
- Wash sale across accounts (taxable + IRA) — perda perdida permanentemente.
- DRIP automatic reinvest creates dozens of small lots → track tedium.

## Automation tools

- **Fidelity Full View** — aggregates cost basis.
- **Cost Basis Reporter** built-in JPM.
- **Sharesight** (paid, third-party) — tracks multiple brokers.
- Our own `sqlite3 data/us_investments.db "SELECT * FROM tax_lots WHERE ticker='AAPL'"` se estiver populated.

## BR — nota para residente BR

- **BR PF** usa **custo médio** para ações BR (mandatory, não escolha).
- Cada compra atualiza o custo médio da carteira.
- Não há Spec ID BR — diferente estrutura.
- **Ganho capital BR** = (preço venda - custo médio) × qty.
- **Mas se holding US via corretora US**: aplicam regras US (Spec ID available) + tax compliance BR (convert to BRL).

## Our tools

```bash
sqlite3 data/us_investments.db "SELECT * FROM tax_lots WHERE ticker='JNJ'"
# displays lots by date + basis
```

Ver memória `portfolio_loaded.md` — tax_lots table was loaded Phase S.

---

> Ver [[US_LTCG_STCG]] para underlying rules. [[Dividend_withholding_BR_US]] para cross-border. Dashboard `TaxLots.md` no vault mostra breakdown.
