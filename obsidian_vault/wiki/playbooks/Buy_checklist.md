---
type: playbook
name: Buy Checklist
tags: [playbook, buy, checklist, process]
related: ["[[Graham_Number]]", "[[Buffett_quality]]", "[[Altman_Z]]", "[[Piotroski_F]]", "[[Dividend_Safety]]", "[[Kelly_criterion]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# ✅ Buy Checklist

> **Princípio**: nunca comprar em impulso. Sempre passar por este gate.

## Pipeline completo

```
1. Screen (passes critérios?)
   ↓ yes
2. Quality veto (Altman + Piotroski ok?)
   ↓ yes
3. Dividend safety (score ≥ 60?)
   ↓ yes
4. Intent alignment (DRIP / Growth / Compounder?)
   ↓ yes
5. Timing (DY percentile / drawdown ok?)
   ↓ yes
6. Position size (Kelly-lite, max %)
   ↓ sized
7. Execute + journal entry
```

## Step 1 — Screen (scoring/engine.py)

### BR não-financeiras
- [ ] Graham Number ≥ preço (`sqrt(22.5 × EPS × BVPS) ≥ price`)
- [ ] DY ≥ 6%
- [ ] ROE ≥ 15%
- [ ] Net Debt / EBITDA < 3×
- [ ] Dividend streak ≥ 5 anos

### BR bancos (sector == "Banks")
- [ ] P/E ≤ 10
- [ ] P/B ≤ 1.5
- [ ] DY ≥ 6%
- [ ] ROE ≥ 12%
- [ ] Dividend streak ≥ 5 anos

### US
- [ ] P/E ≤ 20
- [ ] P/B ≤ 3
- [ ] DY ≥ 2.5%
- [ ] ROE ≥ 15%
- [ ] Dividend Aristocrat **ou** ≥ 10 anos consecutivos dividendo

```bash
python scoring/engine.py <TICKER> --market br|us
```

**Se falha screen**: NÃO compra (exceção thesis contrarian — requires explicit `notes_cli` entry + justificação).

## Step 2 — Quality veto ([[Altman_Z]] + [[Piotroski_F]])

- [ ] Altman Z > 1.81 (se não-financeira, não-REIT, não-FII)
- [ ] Piotroski F ≥ 4

```bash
python -m scoring.altman <TICKER>
python -m scoring.piotroski <TICKER>
```

**Se Z < 1.81**: distress. Compra vetada. (Excepção: tese turnaround com capital burn runway > 24m e catalyst data definida.)

**Se F ≤ 3**: quality deterioration. Compra vetada. (Excepção: single-quarter flyer documentado.)

Sectores **excluídos** do veto (ratios não aplicáveis):
- Banks, Insurance, REITs, FIIs, BDCs, Mortgage REITs.

## Step 3 — Dividend safety

- [ ] Dividend Safety score ≥ 60 (se tese DRIP)

```bash
python -m scoring.dividend_safety <TICKER>
```

Componentes (0-100):
- Payout ratio health
- FCF coverage
- Net debt / EBITDA
- Streak length
- Moat (via ROIC)
- Earnings stability (variance 5y)

**Se score < 40**: dividend em risco. Compra vetada para intent DRIP.
**Se 40-59**: proceed com caução; reforço escalonado.

## Step 4 — Intent alignment

Antes compra, definir **explicitamente** intent:

| Intent | Expectativa | DY requerido | Growth requerido | Exemplo |
|---|---|---|---|---|
| **DRIP core** | Income compounder 10+y | ≥ 3% US / ≥ 6% BR | 2-5%/y EPS | [[TAEE11]], [[PG]] |
| **DRIP plus** | Mix income + modest growth | 2-4% | 5-8% | [[ACN]]-border, [[ITUB4]] |
| **Compounder** | Growth primary, DY bonus | 1-2% | 8-15% | [[MSFT]], [[ACN]] |
| **Growth** | Appreciation only | Nul | 15%+ | [[NVDA]]-era, [[BN]] |
| **Tactical** | Evento/ciclo catalyst | N/A | N/A | [[PVBI11]] turnaround |

Rule: **um ticker não tem 2 intents**. Se tese muda (e.g., growth → DRIP), registar em notes_cli.

```bash
python scripts/notes_cli.py add ACN "Intent: compounder — DY bonus não primary"
```

Ver memória `user_investment_intents.md`.

## Step 5 — Timing ([[DY_percentile]] / drawdown)

Não confunde timing com screen. Timing é **só se já passa Steps 1-4**.

Context checks:
- [ ] Drawdown de 52w high > -15%? (entrada melhor que neutral)
- [ ] DY atual > percentil 75 histórico 10y? (relative yield entry — útil mas no alpha per backtest)
- [ ] Regime macro favorável ao sector? (use `analytics.regime`)
- [ ] Earnings announcement próximos 5 dias? (espera pós-reaction)

```bash
python scripts/compare_ticker_vs_macro.py <TICKER>
python -m analytics.regime --market us
ii peers <TICKER>
```

**Empírico** (ver backtest_yield phase F): DY-percentile sozinho não gera alpha mas funciona como **entry context** — prefere drawdowns para reforços vs peak euphoria.

## Step 6 — Position sizing

Usar Kelly-lite:

```bash
ii size <TICKER> --cash 10000
```

Regras teu portfolio:
- Max por ticker: **8%** do total (BR+US em BRL).
- Max por sector: **20%** do total.
- Max por country (BR ou US): **60%** do total.
- Single-name core holdings: min **2%** (senão muita friction DRIP).

Se Kelly calc > max cap: usa max cap (prudence over math).

```bash
ii peers <TICKER>                # confirma não over-exposed sector
ii rebalance                     # drift vs target
```

## Step 7 — Execute + Journal

### Execute
- BR: XP / corretora teu. Limit order recommended (evita spread wide).
- US: JPM / Fidelity. MKT order OK para large caps; LIMIT para small/mid cap.

### Journal imediatamente:

```bash
python scripts/notes_cli.py add <TICKER> "BUY X shares @ Y — thesis: ..." --tags buy,entry
```

Entry must include:
- Date, price paid, qty
- Thesis em 1-2 linhas
- What would invalidate (exit trigger)
- Intent category

### Update system
- Se nova holding (primeira compra), adicionar em `config/universe.yaml` → `is_holding: 1`.
- Se reforço, update `portfolio_positions` na DB.
- Rodar `python scripts/daily_update.py` para re-score.

## Common pitfalls

1. **Anchoring na entry**: compraste a $50, agora vale $70, recusas reforçar. Re-avalie a partir de $70 fresh — passa screen **agora**? Se sim, reforço válido.
2. **FOMO compounder peak**: comprar NVDA a 50× P/E porque "é qualidade" — quality filter não substitui valuation filter.
3. **Yield trap**: DY alto por preço caindo → checa Altman/Piotroski primeiro.
4. **Forced diversification**: comprar 2º-tier porque "já tenho muito do tier-1" → prefira over-allocate tier-1 se convictions warrant.
5. **Ignorar macro regime**: comprar homebuilder em Selic alta → headwind estrutural.

## Templates

### DRIP core entry journal
```
[2026-04-XX] BUY TAEE11 200 @ R$ 35.50 = R$ 7,100
Thesis: transmissão pura, DY 8.5%, Selic cycle peak superado
Intent: DRIP core (BR utilities backbone)
Invalidation: dividend cut OR ND/EBITDA > 3.5× OR nova RTP hostile
Next review: 90 dias ou earnings release
```

### Compounder entry journal
```
[2026-04-XX] BUY ACN 5 @ $178 = $890
Thesis: AI services bookings $3B+, ROIC 27%, managed services 50%+ mix
Intent: Compounder (not DRIP primary)
Invalidation: Bookings < revenue TTM 3 quarters, CEO change, AI cannibalization accelerating
Next review: FY guidance release
```

## Related

- [[Sell_triggers]] — inverse (when to exit)
- [[Rebalance_cadence]] — periodic drift checks
- [[Kelly_criterion]] — sizing math
