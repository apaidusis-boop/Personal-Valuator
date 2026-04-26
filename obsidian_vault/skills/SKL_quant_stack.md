---
type: skill_group
tier: Gold
skill_name: quant-stack
status: backlog
sprint: W.11
tags: [skill, gold, quant, backtest, pyfolio, vectorbt]
---

# 📊 Quant Stack — Gold extras

Libraries Python para profissionalizar análise quantitativa. Vamos elevar `analytics/` para level production.

## 1. pyfolio — Portfolio performance analytics 🎯
**Repo**: https://github.com/quantopian/pyfolio
**O que faz**: comprehensive tear sheet de performance do portfolio. Sharpe, Sortino, drawdown, rolling beta, VaR, stress tests.

**Onde integra**:
- Novo script `scripts/pyfolio_tearsheet.py` — gera relatório HTML/PNG com ~20 charts professional-grade
- Input: `portfolio_positions` + `prices` histórico
- Output: `reports/tearsheets/YYYY-QN.html`
- **Include no quarterly PPTX deck** ([[SKL_pptx]]) como embedded pages

**Dor resolve**: hoje `scripts/portfolio_report.py` tem métricas básicas. pyfolio tem o standard institutional.

## 2. empyrical — Financial risk metrics 📐
**Repo**: https://github.com/quantopian/empyrical
**O que faz**: biblioteca de métricas (sibling da pyfolio). Sharpe, Sortino, Calmar, omega, tail ratio, VaR, CVaR, alpha, beta.

**Onde integra**:
- `analytics/` module — novo `analytics/risk_metrics.py`
- Feed para thesis health (perpetuum validator): se `portfolio.max_drawdown` > threshold, alert
- Weekly report inclui tabela com estas métricas

## 3. vectorbt — Vectorized backtesting ⚡
**Repo**: https://github.com/polakowo/vectorbt
**O que faz**: backtest engine 100x-1000x mais rápido que Backtrader via numpy vectorization.

**Onde integra**:
- Hoje temos `analytics/backtest_yield.py` e `backtest_regime.py` (custom, lentos)
- Refactor para vectorbt:
  - Rodar backtest de 20 anos em segundos (vs minutos)
  - Parameter sweeps (ex: top-N de 3 a 10) em paralelo
  - Equity curves, drawdowns, Sharpe em 1 linha

**Use case killer**: "Qual era o melhor valor de top_n para a estratégia Buffett US de 2010-2025?" → vectorbt responde em 5s.

## 4. Zipline / Backtrader — alternativas
**Decisão**: vectorbt >> Zipline/Backtrader para nosso uso (personal, não HFT). Só voltar se vectorbt tiver limitação real.

## 5. Riskfolio-Lib — Portfolio optimization 📈
**Repo**: https://github.com/dcajasn/Riskfolio-Lib
**O que faz**: modern portfolio theory solver — mean-variance, risk parity, Black-Litterman, HRP.

**Onde integra**:
- `scripts/position_size.py` hoje é Kelly-lite. Riskfolio-Lib adiciona:
  - **Risk parity**: aloca para igualar risk contribution (vs equal weight)
  - **HRP** (Hierarchical Risk Parity): não requires covariance invertível
  - **Black-Litterman**: incorpora views subjetivos (ex: "acredito que VALE3 vai ter +15% retorno") em optimization

**Use case**: `ii rebalance --optimize hrp --cash-add 5000` → sugere exact weights para balancear risk.

## 6. Alphalens — Factor analysis
**Repo**: https://github.com/quantopian/alphalens
**O que faz**: analisa factores (ex: DY, ROE, P/B) — são preditivos de retorno? IC (information coefficient), quintile returns, turnover.

**Onde integra**:
- Validar se **nosso scoring** (BR/US criteria) é realmente preditivo
- Input: histórico de scores (`scores` table) + retornos subsequentes
- Output: "Score > 80 ganha 7% em 12m vs 2% baseline → engine funciona"

**Meta-fit**: isto é **validation do nosso core IP** (scoring engine). Deveria ser prioridade alta — prova se nosso método funciona.

## Sprint W.11 — entregáveis

Ordem:
1. **pyfolio** — tearsheet pronta em 2 dias (setup simples, high impact visual)
2. **empyrical** — usar standalone em scripts novos
3. **vectorbt** — refactor backtests existentes (3-5 dias)
4. **Alphalens** — valida scoring engine IP (crítico para saber se estamos certos)
5. **Riskfolio-Lib** — avançado, só depois de ter baseline

## Links cruzados
- [[SKL_openbb]] — OpenBB inclui algumas destas libs; evitar duplicate install
- [[Metrics]] — estas libs geram KPIs para before/after comparison
- [[SKL_pptx]] — pyfolio tearsheets embebidas no quarterly deck

## Blockers
- pyfolio/empyrical/alphalens são **unmaintained** (Quantopian closed 2020). Funcionam mas podem quebrar em numpy/pandas futuros. Pinar versions.
- vectorbt tem versão free + pro. Free suficiente.
