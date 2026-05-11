---
type: skill
tier: Gold
skill_name: openbb
source: OpenBB-finance/OpenBB
status: backlog
sprint: W.10
priority: high
tags: [skill, gold, openbb, research_platform, opensource]
---

# 📈 OpenBB — Open Source Investment Research Platform

**Repo**: https://github.com/OpenBB-finance/OpenBB
**Homepage**: https://openbb.co
**Fit**: 🎯 **MASSIVO** — é literalmente o que estamos a construir, já pronto e open source.

## Por que esta descoberta é crítica
Investment-intelligence tem 100+ scripts custom. OpenBB tem **~5 anos de investimento em research tooling open source** que cobre muito do que temos:

- 100+ data providers (vs nossos 8)
- CLI + SDK + Workspace (dashboard)
- Macro indicators, fundamentals, technicals, economy, crypto, forex
- Backtesting integrations
- Research agents nativos

**NÃO** é substituir investment-intelligence (nossa lógica DRIP Buffett/Graham BR+US é o differentiator).
**É** usar OpenBB como **platform layer** para data fetching + UX tooling, deixando nosso código focar em scoring/thesis logic.

## Integração pragmática

### Fase 1 — OpenBB como data source fallback
- `fetchers/openbb_fetcher.py` — wrapper sobre `openbb` Python SDK
- Quando brapi falha OR yfinance inconsistente → tentar OpenBB
- Registar em `fetchers/_registry.py` como `priority=3` (depois de primary + fallback)

### Fase 2 — OpenBB Terminal integration
- Aprender a usar `openbb` CLI localmente
- Substituir alguns nossos scripts quando OpenBB equivalente é melhor:
  - `compare_ibov.py` → OpenBB já tem `economy compare` nativo
  - `compare_ticker_vs_macro.py` → OpenBB `stocks.fa` + `economy`
  - `br_drip_optimizer.py` → nossa lógica fica; mas data fetch via OpenBB

### Fase 3 — OpenBB Workspace como secundário dashboard
- Streamlit (`ii dashboard`) continua primário
- OpenBB Workspace para research exploratory ad-hoc
- Paridade de data: ambos leem as mesmas DBs

## O que NÃO mover para OpenBB
- **CLAUDE.md critérios BR/US** — nosso IP conceitual
- **Bancos BR scoring** — lógica específica Graham adjusted
- **DRIP projection damper** — custom
- **Agents framework** — Phase V
- **Thesis health** — perpetuum validator
- **Obsidian vault** — conventions próprias
- **Subscriptions ingestion** — Suno/XP/BTG são mercado BR específico

## Sprint W.10 — entregáveis
- [ ] `pip install openbb` em env paralelo (sanity test deps)
- [ ] `fetchers/openbb_fetcher.py` wrapper básico
- [ ] A/B test: 5 tickers BR + 5 US, compare OpenBB vs brapi/yfinance
- [ ] Documentar em CLAUDE.md quais scripts foram aposentados/refactored
- [ ] Decision memo: quais 5 scripts nossos ficam vs 5 que movemos para OpenBB

## Riscos
- **Dependency hell**: OpenBB pesa (30+ deps); isolar em venv
- **API stability**: OpenBB tem breaking changes entre versions
- **LLM-first design** do OpenBB — muitos outputs orientados para LLM consumption; pode conflitar com nosso Ollama in-house

## Decisão estratégica
OpenBB é **peer, não replacement**. Adoptar gradualmente. W.10 é avaliação; se passar, outras features.

## Blockers
Instalação (pesado mas direto).
