---
name: macro-regime
description: Use this skill when the user asks about macro regime, economic
  environment, rate cycle, inflation trend, or which sectors to favor in
  current conditions. Examples - "em que regime estamos", "o Fed vai cortar",
  "como está Selic", "macro BR agora", "should I be defensive", "risk-on ou
  risk-off". Invokes analytics/regime.py classifier + layers in sector
  implications from CLAUDE.md + vault wiki macro notes.
---

# Macro Regime Skill

Classify current macro regime (BR + US) and translate to sector-level
implications for the portfolio.

## When to trigger

- "Que regime macro?" / "expansion ou recession?"
- "Selic a subir vai doer quais sectors?"
- "Should I be defensive now?"
- "Como está o cenário"
- "Risk-on ou risk-off"

DO NOT trigger for:
- Ticker-specific analysis (use panorama-ticker)
- Rebalance decisions (use rebalance-advisor — though this skill feeds it)

## Workflow

1. **Classify current regime**:
   ```bash
   python -m analytics.regime          # both markets
   python -m analytics.regime --market br
   python -m analytics.regime --market us
   ```
   Output: `expansion | late_cycle | recession | recovery` + confidence

2. **Pull historical context** — last 4 weeks of regime changes:
   ```sql
   -- regime_history if exists, otherwise run classify_at past dates
   SELECT run_date, regime_br, regime_us FROM regime_history
   WHERE run_date >= date('now','-30 days')
   ORDER BY run_date
   ```

3. **Translate to sector implications** using CLAUDE.md + wiki rules:

   | Regime | Favor | Underweight | Why |
   |---|---|---|---|
   | expansion | Tech, Discretionary, Industrials | Utilities, REITs | Earnings growth cycle |
   | late_cycle | Healthcare, Staples, Utilities | Tech, Discretionary | Defensive rotation |
   | recession | Staples, Healthcare, Treasuries | Financials, Energy, Discretionary | Cash flow resilience |
   | recovery | Financials, Industrials, Discretionary | Defensives | Rate cuts + demand rebound |

4. **Empirical caveat** (from `analytics/regime.py` docstring — CRITICAL):
   - Overlay "cash when late_cycle/recession" **DESTRÓI valor** (backtested -2-3%/y)
   - Classifier is trigger-happy on late_cycle (chamou 2022, 2023 US + 2021, 2024 BR)
   - **Use DESCRITIVO, NÃO accionável standalone**
   - When regime flips, suggest **tilt ±3pp** max, not wholesale rotation

5. **Check thesis_health for regime-sensitive holdings**:
   - If regime shifted and any holding has regime_shift=1 in thesis_health, flag
6. **Narrate in PT**:

```markdown
## Macro Regime — <YYYY-MM-DD>

### BR
- **Regime**: late_cycle (confidence: medium ▓▓░)
- Signals: Selic 11.5% (a subir 6m), IPCA 4.2% YoY, IBOV 6m flat
- Driver: Selic hiking + IPCA above target → restrictive

### US
- **Regime**: expansion (confidence: high ▓▓▓)
- Signals: Fed funds 4.25% cutting, T10Y-T2Y +0.4, VIX 14, unemployment 4.1% falling
- Driver: Fed cutting + labor strong = textbook expansion

### Sector implications (tilts, não rotation massiva)
- BR: favor financials (juros altos ainda beneficiam bancos), underweight REITs (cap rate compressed)
- US: favor tech + discretionary (earnings cycle), hold defensive allocation (VIX baixo = complacência)

### Regime-sensitive holdings to review
- ACN (US, thesis=91): regime compatible, hold
- ITSA4 (BR, thesis=100): bancos beneficiam Selic alta, hold+

### Empirical warning
Regime classifier é DESCRITIVO. Não fazer rotation >3pp baseado só nisto.
Tilts pequenos + re-avaliar em 30 dias.
```

## Critical rules

- **Sempre citar "empirical caveat"** — previne o user de usar regime como timing signal
- **Confidence matters**: se confidence=low, dar peso menor às implications
- **Never recommend cash position >5%** based on regime alone (backtested destructive)
- **Cross-reference vault wiki**: `[[wiki/macro/Selic]]`, `[[wiki/macro/Fed_funds]]`, etc.

## Files reference

- `analytics/regime.py` — classifier
- `analytics/backtest_regime.py` — empirical validation (null overlay!)
- `obsidian_vault/wiki/macro/` — 11 macro notes
- `data/{br,us}_investments.db` — regime_history if exists
- `fetchers/bcb_fetcher.py` + `fetchers/fred_fetcher.py` — série macro
