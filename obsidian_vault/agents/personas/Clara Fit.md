---
handle: perf.portfolio-matcher
type: persona
employee: Clara Fit
title: Portfolio Analyst
department: Performance
agent: portfolio_matcher
reports_to: clara_fit
schedule: "every:30m"
tags: [persona, agent, portfolio, triage]
---

# Clara Fit

**Portfolio Analyst · Performance**

> "Cada insight novo é atribuído ao lugar certo: holding / watchlist / macro / noise."

## Rotina

A cada **30 minutos**:
1. Pega analyst_insights criados nas últimas 6h
2. Para cada, classifica:
   - **HOLDING** — ticker é posição activa
   - **WATCHLIST** — ticker segue mas sem posição
   - **MACRO** — sem ticker específico
   - **NOISE** — ticker desconhecido (descartado)
3. Para HOLDING + WATCHLIST:
   - Carrega source credibility (Aristóteles Backtest ranking)
   - Computa `relevance = source_weight × confidence × min(pos_weight × 5, 1)`
4. Se `relevance ≥ 0.7` E HOLDING → cria `watchlist_action` kind='portfolio_matcher_high_rel' com action_hint=REVIEW
5. Dedup 24h por ticker

## Fórmula relevance

```
relevance = source_credibility × insight_confidence × position_sizing_factor

  source_credibility ∈ [0.3, 1.0]   (vem de _performance_ranking.md)
  insight_confidence ∈ [0, 1]       (Ollama self-report no extract)
  position_sizing_factor = min(pos_mv / total_mv × 5, 1.0)
```

## Dados que vê

- ✓ `analyst_insights` (recentes)
- ✓ `portfolio_positions` (para classificar holding)
- ✓ `companies` (watchlist)
- ✓ `prices` (market value)
- ✓ `predictions` (source credibility via accuracy)
- ✏️ Escreve: `watchlist_actions`

## Loop de aprendizagem
Clara usa credibility de Aristóteles. Se XP é 70% correct → insights XP pesam mais. Se YT channel X é 30% correct → contrarian signal.

## Instância técnica

- Class: `agents.portfolio_matcher:PortfolioMatcherAgent`
- Schedule: `every:30m`

## CLI

```bash
ii agents run portfolio_matcher
sqlite3 data/br_investments.db "SELECT * FROM watchlist_actions WHERE kind='portfolio_matcher_high_rel'"
```
