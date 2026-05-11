# Framework de decisão — $1.5k US + Sells

> Anexo para `_BOM_DIA.md`. Cobre como pensar a decisão de capital esta semana.

## Step 1 — Onde colocar $1,500 USD

### Critérios qualitativos (em ordem de peso)

1. **Score nosso ≥ 0.6 + passa screen Buffett** — primeiro filtro. Se score baixo, pular.
2. **Aristocrat / Streak ≥ 25 anos** — qualidade comprovada de pagar dividendos. Para DRIP de longo prazo, isto é critical.
3. **Sem 🚨 sinais críticos negativos** — verificar a secção 'Critical signals' do `_LEITURA_DA_MANHA.md`. Se houver mudança executiva contestada, M&A material, downgrade, etc → pause antes de adicionar.
4. **P/L da posição actual** — para REINVESTMENT, preferir tickers ainda em desconto vs entry (ou ligeiramente acima). Adicionar a posições com +50% lucro implicit chases price.
5. **Concentração sectorial** — se já tens 30%+ em Financials, evita reforçar o sector. Diversificar.
6. **Ex-dividend timing** — se há ex-dividend nos próximos 30 dias, capturar. Vê secção "Próximos eventos" por ticker.

### Critérios quantitativos (composite score do _LEITURA_DA_MANHA.md)

A tabela "Top 8 candidatos" usa esta fórmula:

```
composite =
  + (score nosso × 30)            # peso máximo (0-30)
  + (10 if passes_screen)         # bonus binary
  + (5 if aristocrat)             # bonus dividend quality
  + (min(streak/50 × 5, 5))       # streak years cap 5
  + (max(0, dy - 2.5%) × 100)     # extra DY value
  + (max(0, 18 - PE/100) × 30)    # cheap valuation
  + (signals × 2)                 # critical signals (positive)
  + (novel × 0.5)                 # filings novos
```

**Limitações conhecidas**:
- Não considera FCF yield ou ROIC explicitamente (proxied por score)
- Não pondera tax bracket / wash sale rules
- Não diferencia BR market sentiment vs US fundamentals
- "novel filings" não distingue positive de negative news

### Decision matrix

| Cenário | Recomendação |
|---|---|
| Top 1 candidate (composite) > 50 + você confia | Concentrar $1.5k em 1 ticker |
| Top 3 dispersos (composite 30-50) | Distribuir $500 cada — diversifica |
| Top picks são todos REITs/Financials (sector dominance) | Adicionar fora do sector dominante (mesmo se composite menor) |
| Posição actual já tem +50% em alguma top pick | Considerar 2nd/3rd ranked em vez de adicionar mais à 1st |

## Step 2 — 2 sells para realocar

### Critérios para flagar SELL

1. **Score < 0.4 E não passa screen** — fundamentais deteriorando
2. **🚨 Mudança material de tese** (ex: change of CEO, M&A controversa, ofício CVM significativo)
3. **P/L > +50%** — realizar parte do ganho (rebalancing tactical)
4. **Sector concentration > 35%** — reduzir overweight
5. **Tese original já realizada** — você comprou por X razão, X aconteceu, agora está overpriced

### Para pares específicos que vais decidir vender

Quando me disseres os 2 tickers, vou correr:
1. **Cross-section vs replacement** — comparar sell candidate a top 3 picks do composite
2. **Tax-impact estimate** — capital gains se vendido agora vs hold
3. **Sector swap** — se vendes 1 Financial, sugiro replacement em outro sector ou outro Financial?
4. **Verdict consensus** — agregar score + dossier signals + recent news para confirmar

### Comandos para executar

```powershell
# Ver dossier completo de 1 ticker antes de decidir
notepad obsidian_vault/Overnight_2026-05-11/<TICKER>.md

# Dar-me os 2 tickers para sell análise
# (na conversa Claude amanhã)

# Re-scrape um ticker se quiser dado fresco
.venv\Scripts\python.exe scripts/pilot_deep_dive.py --tickers <TICKER> --force-fresh --deep
```

## Step 3 — Considerações tácticas

### Timing

- **Esta semana** (11-15 maio): 1T26 earnings season BR + alguns US Q1 reports. Re-scrape mais críticos no dia.
- **Mid-month** (15-20 maio): geralmente menor volatilidade — bom para entries.
- **End-month** (28-31 maio): rebalancing institucional pode mover preços. Cuidado com chase.

### Wash sale (US tax)

Se vendeste $X em ticker Y nos últimos 30 dias com loss, NÃO recomprar Y nos próximos 30 dias (wash sale rule). Verifica histórico antes.

### Para BR

Como tu disseste antes ("USD fica em US, BRL em BR"), o $1,500 só vai para US holdings/watchlist. Ignorar BR para esta decisão.

## Step 4 — Após decisão

1. Comprar shares (broker próprio)
2. Atualizar `data/us_investments.db` portfolio_positions com novas qty/entry_price
3. Re-correr `ii overnight --quick` ou `pilot_deep_dive.py` para snapshot pós-trade
4. Registar a decisão no Decision Journal (`obsidian_vault/decision_journal/2026-05/`)

---
_Framework escrito durante overnight 2026-05-10 → 2026-05-11._
_Ajustar se houver feedback do user amanhã._
