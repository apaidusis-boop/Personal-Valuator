# Overnight Backfill — 2026-05-04

**Run ID**: `overnight_2026-05-04`  
**Generated**: 2026-05-04T19:11:38Z  

## Pre-fetch summary (live cache hits + DB writes)

### US
- Universe size: 28
- Prices fetched OK: 0
- Fundamentals fetched OK: 0
- Macro series OK: 0 / fail: 0
- Strategy outputs persisted: 112 / fail: 0

**Hedge US**: OFF  
- regime: expansion (confidence: medium)  
- size: 0%  
- instruments: —  

**Top 10 allocation US**:
- ACN: 12.3%
- TSM: 11.2%
- IBM: 11.0%
- MSFT: 10.5%
- AAPL: 10.3%
- TTD: 9.0%
- GREK: 8.5%
- PLTR: 7.6%
- HD: 7.0%
- PLD: 6.1%

**8 conflicts** detected (BUY+AVOID disagreement):
- AAPL: {'buffett': 'AVOID', 'drip': 'HOLD', 'macro': 'BUY', 'hedge': 'HOLD'}
- KO: {'buffett': 'HOLD', 'drip': 'BUY', 'macro': 'AVOID', 'hedge': 'HOLD'}
- MSFT: {'buffett': 'AVOID', 'drip': 'HOLD', 'macro': 'BUY', 'hedge': 'HOLD'}
- PG: {'buffett': 'HOLD', 'drip': 'BUY', 'macro': 'AVOID', 'hedge': 'HOLD'}
- PLD: {'buffett': 'AVOID', 'drip': 'BUY', 'macro': 'HOLD', 'hedge': 'HOLD'}

## How to consume

- Strategy outputs in `data/{br,us}_investments.db::strategy_runs`
- Allocation proposals in `obsidian_vault/Bibliotheca/Allocation_*.json`
- Cache fully primed in `data/api_cache.db` (TTL 24h prices, 72h fund, 168h macro)
- Agent decisions log in `data/agent_decisions.db` (90d retention)
