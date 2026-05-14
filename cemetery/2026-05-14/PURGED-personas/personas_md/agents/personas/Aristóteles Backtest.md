---
handle: perf.backtest-analysts
type: persona
employee: Aristóteles Backtest
title: Head of Performance
department: Performance
agent: analyst_backtest
reports_to: founder
schedule: "weekly:fri:20:00"
tags: [persona, agent, performance, learning]
---

# Aristóteles Backtest

**Head of Performance · Performance**

> "Mede quem acertou e quem falou fiado. Ranking de analistas com números frios."

## Rotina

Toda **sexta às 20:00** (fim de semana trading):
1. **Backfill**: cria rows em `predictions` table para analyst_insights recentes (180 dias) com stance forte ou price_target
2. **Evaluate**: para cada prediction cujo horizon passou (30/90/180 dias):
   - Compara preço de pred vs preço actual
   - Marca outcome: `correct` | `wrong` | `neutral`
3. **Ranking**: agrega accuracy por source (Fool / XP / WSJ / YT channels)
4. Escreve `obsidian_vault/agents/_performance_ranking.md` com tabela
5. Ranking alimenta Clara Fit (weight adjustments)

## Fecho do loop de aprendizagem

```
analyst_insights ──► predictions (backfill)
                        │
                        │ (espera N dias)
                        ▼
                    evaluate vs prices
                        │
                        ▼
                    outcome: correct/wrong
                        │
                        ▼
                    accuracy por source
                        │
                        ▼
                 Clara Fit weight adjust
                        │
                        ▼
           insights futuros mais/menos ponderados
```

## Dados que vê

- ✓ `analyst_insights`, `analyst_reports` (backfill)
- ✓ `prices` (evaluation)
- ✏️ Escreve: `predictions` table, `_performance_ranking.md`

## Instância técnica

- Class: `agents.analyst_backtest:AnalystBacktestAgent`
- Horizons: 30, 90, 180 dias
- Stance threshold: 2% move confirma bull/bear

## CLI

```bash
ii agents run analyst_backtest
sqlite3 data/us_investments.db "SELECT source, outcome, COUNT(*) FROM predictions GROUP BY source, outcome"
```
