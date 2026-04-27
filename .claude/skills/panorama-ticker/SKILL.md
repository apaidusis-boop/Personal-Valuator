---
name: panorama-ticker
description: Use this skill when the user wants a comprehensive 360-degree
  view of a specific ticker — asks for "panorama", "visão completa", "deep
  dive", or "me diga tudo sobre X". Orchestrates `ii panorama X --write` which
  aggregates verdict + peers + triggers + notes + videos + analyst reports +
  thesis_health + perpetuum validator output, then narrates in PT.
  DO NOT use for: DRIP projection (drip-analyst), rebalance advice
  (rebalance-advisor), macro-only questions (macro-regime).
---

# Panorama Ticker Skill

Comprehensive 360° view of a ticker using the existing `ii panorama` command.

## When to trigger

- "Panorama de X" / "visão completa de X"
- "Deep dive em Y"
- "Tudo que sabemos sobre Z"
- "Mostra-me TFC" / "analisa ACN"

Do NOT trigger for:
- Pure DRIP questions (use drip-analyst)
- Rebalance / portfolio allocation (use rebalance-advisor)
- Macro regime questions (use macro-regime)

## Workflow

1. **Identify ticker + market**: extract from user prompt or CLAUDE.md portfolio context
2. **Run super-command**:
   ```bash
   ii panorama <TICKER> --write
   ```
   This generates:
   - Verdict (BUY/HOLD/SELL aggregated)
   - Peer comparison (sector percentile)
   - Active triggers (price drops, DY spikes)
   - Notes history (user-added context)
   - YouTube videos referencing ticker
   - Analyst report views (Suno/XP/WSJ via `ii subs query`)
   - `--write` flag saves output to `obsidian_vault/tickers/<TICKER>.md`
3. **Pull latest thesis_health** from DB:
   ```sql
   SELECT thesis_score, contradictions, risk_flags, regime_shift, details_json
   FROM thesis_health WHERE ticker='<TICKER>' ORDER BY run_date DESC LIMIT 1
   ```
4. **Pull 7-day thesis trend** (detect decay):
   ```sql
   SELECT run_date, thesis_score FROM thesis_health
   WHERE ticker='<TICKER>' AND run_date >= date('now','-7 days')
   ORDER BY run_date
   ```
5. **Narrate in PT** with structure:
   - 1-line verdict
   - Thesis health status + trend
   - Key flags from perpetuum (risk_reasons, contradictions)
   - Peer rank
   - Active triggers
   - Recent analyst views (last 90d)
   - Suggested next action

## Output format

```markdown
## Panorama — <TICKER> (<MARKET>)

**Verdict**: BUY/HOLD/SELL (confidence) | Price R$X.XX | 52w range $X-$Y

### Thesis Health
- Score: **82/100** ↘ (was 89 5 days ago)
- Regime: expansion
- Flags: 1 risk (R3 DD -46% from 52w), 0 contradictions

### Peer rank (sector: Technology US)
... (table from ii peers)

### Active triggers
- 🔴 price_drop -20% (2026-04-18) — auto-generated
- 🟡 earnings_approaching (2026-05-02)

### Analyst views (last 90d)
- WSJ 2026-04-15: "BUY, PT $380" (Morgan Stanley upgrade)
- Suno 2026-04-10: "HOLD — risk/reward balanced"

### Recent vault notes
... (last 3 notes)

### Suggested next action
<1-2 sentences actionable>
```

## Critical rules

- **ALWAYS use `ii panorama`** — don't reimplement logic. Respect in-house first.
- **Check thesis_health**: if score < 50, WARN loudly before proceeding
- **Cite sources**: Suno/WSJ/XP reports with date
- **Conservative**: if regime shift detected, mention it even if user didn't ask
- **Language**: default PT; switch to EN only if user wrote in EN

## Files reference

- `CLAUDE.md` — portfolio philosophy + commands
- `scripts/panorama.py` — super-command logic
- `agents/perpetuum_validator.py` — thesis_health source
- `data/{br,us}_investments.db` — main data
- `obsidian_vault/tickers/<X>.md` — vault notes for cross-reference
