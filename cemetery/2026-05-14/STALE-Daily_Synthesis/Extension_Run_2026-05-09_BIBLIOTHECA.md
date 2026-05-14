# Extension Run 2026-05-09 — Final Report

_Generated: 2026-05-09T12:18:29_

## Mission recap

3 fixes shipped earlier today, then this orchestrator extended:
- Recomputed fair_value for full universe (now with intangibles in inputs)
- Recomputed dividend_safety (REIT-aware ROE fix)
- synthetic_ic on holdings + watchlist top-N

## Calibration: predicted vs actual

| Phase | Predicted | Actual | Δ | Δ% |
|---|---:|---:|---:|---:|
| 1.backfill_br_intangibles | 90s | 42s | -48s | -53% |
| 2.recompute_fair_value | 180s | 3s | -177s | -98% |
| 3.recompute_safety | 60s | 0s | -60s | -100% |
| 4.multi_agent_holdings | 2520s | 1771s | -749s | -30% |
| 5.multi_agent_watchlist | 5400s | 3592s | -1808s | -34% |
| **TOTAL** | **8250s (138min)** | **5408s (90min)** | **-2842s** | **-34%** |

## Fair value confidence (after recompute)

- **US**: {'cross_validated': 13, 'disputed': 1, 'single_source': 85}
- **BR**: {'cross_validated': 11, 'disputed': 3, 'single_source': 59}

## IC debates produced

- Total IC_DEBATE.md files in vault: **188**
- Run output dir: `obsidian_vault/tickers/<TK>_IC_DEBATE.md`

## How to use this run

1. Compare any single dossier to its earlier version — does intangible context appear in fundamentals?
2. Re-ask 'should I add to KO/PG/JNJ?' — system can now cite intangible_pct_assets and warn re: brand-off-balance-sheet
3. Re-ask 'is O safe?' — dividend_safety should now show REIT-aware re-score (75 instead of 60)
4. Open A_FAZER.md to see what's still pending (CET1 parser, fair-zones engine, litigation flags, CVM upstream fix)

## Files

- Live status: `obsidian_vault\Extension_Run_2026-05-09.md`
- Log: `logs\extend_2026-05-09.log`
- Calibration: `data\calibration_2026-05-09.json`
