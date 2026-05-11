# Cleanup: Orphans Audit — 2026-04-27 (overnight)

Companion to `Cleanup_OneShot_Scripts.md`. Inventory only — nothing was deleted, no perpetuum was disabled.

## Summary
- Perpetuums registered: **12** (in `agents/perpetuum/_registry.py`)
- Perpetuums actively running last 7d: **11** (the 12th, `autoresearch`, has never logged a row in `perpetuum_run_log` despite being registered and wired into `perpetuum_master.py`)
- Perpetuums with 0 alerts in 7d: **9** (silent — see table)
- Scripts with no caller in any `.bat`, no Python import, no doc reference: **3**
- Modules (agents/analytics) without any importer in code: **5**
- Untracked-by-git suspect files at root: **1** (`_scan_dead_code.py`)

## Perpetuum status (last 7 days)

| Name             | Last run    | Subjects (last) | Alerts (7d) | Status |
|------------------|-------------|-----------------|-------------|--------|
| autoresearch     | **never**   | 0               | 0           | **NEVER LOGGED** — registered, wired in master + daily_run.bat, but no row in `perpetuum_run_log`. Either it errored on every run, or its logging hook is disconnected. Investigate. |
| bibliotheca      | 2026-04-26  | 184             | 0           | T1 observer; expected silent |
| code_health      | 2026-04-26  | 176             | 0           | T1 observer; ran once in 7d (added late) |
| content_quality  | 2026-04-26  | 93              | 0           | Silent — promoted to T2 per Phase F but no signals firing |
| data_coverage    | 2026-04-26  | 99              | 0           | Silent (data backfilled; signals quiet) |
| library_signals  | 2026-04-25  | 5,840           | 16          | **FROZEN** (`enabled=False` in code) yet last run 2 days ago shows alerts. Conflict between code freeze + cron history. |
| meta             | 2026-04-26  | 24              | 1           | Active — only perpetuum producing alerts in last 24h |
| method_discovery | 2026-04-26  | 24              | 0           | Silent |
| ri_freshness     | 2026-04-26  | 25              | 0           | Silent (Phase BB raised it 5→20 subjects but still 0 alerts) |
| thesis           | 2026-04-26  | 401             | 0           | Silent — universe-wide thesis coverage 100% (Phase J) so no missing-thesis alerts to fire; consider new signals |
| token_economy    | 2026-04-26  | 387             | 0           | Silent — promoted T2 per Phase F |
| vault            | 2026-04-26  | 1,379           | 0           | Silent — Phase F bulk-ignored 80 drift signals; now nothing firing |

**Net**: 11/12 perpetuums actually run. **9/12 produced zero alerts in the last 7 days** — the perpetuum layer is mostly observing nothing. Only `meta` and `library_signals` (frozen) generated alerts.

## Orphaned scripts (zero callers in any .bat / .py / .md inside the repo)

| Script                            | LoC | Last git mod | Recommendation |
|-----------------------------------|-----|--------------|----------------|
| `scripts/telegram_loop.py`        | 112 | untracked    | Predates `agents/telegram_controller.py` (registered in `config/agents.yaml` as Zé Mensageiro, schedule `every:2m`). Functional duplicate. **Drop after diff vs telegram_controller.** |
| `scripts/_terminal.py`            | 337 | untracked    | Already flagged in `Cleanup_OneShot_Scripts.md`. Bloomberg-style CSS module not imported by `dashboard_app.py` (which uses `_theme + _editorial + _components`). Helena `editorial` CSS replaced it during Phase U.0. **Drop unless wiring intent exists.** |
| `scripts/fetch_kings_aristocrats.py` | 74 | 2026-04-21   | Memory rule says `config/kings_aristocrats.yaml` is the canonical source and loaders in `yf_us_fetcher` + `daily_update_us` read it automatically — confirmed grep. The fetcher script is legacy. **Drop or convert into a yaml-bootstrapper one-shot, then drop.** |

(`_captains_log.py`, `_carteiras.py`, `_editorial.py` were initially false positives — they ARE imported by `dashboard_app.py` / `captains_log_telegram.py` via the `from scripts import X as Y` pattern, which the first sweep missed.)

## Orphaned modules (zero importers in code; only doc/persona files mention them)

| Module                                | LoC | Where it should plug in | Recommendation |
|---------------------------------------|-----|-------------------------|----------------|
| `agents/decision_journal_intel.py`    | 311 | Captain's Log Streamlit page or daily run | Built in Phase AA but never wired. Only the Phase AA report doc references it. Either wire into `_captains_log.py` story_cards or `daily_run.bat`, or freeze. |
| `analytics/portfolio_stress.py`       | 395 | `dashboard_app.py` (Risk page) or `morning_briefing` | Built in Phase AA (concentration / factor / drawdown). Zero importers. Should at minimum surface in dashboard "Captain's Log" or daily brief. |
| `analytics/backtest_triggers.py`      | 204 | `ii backtest-triggers` CLI subcommand | CLAUDE.md catalogs `python -m analytics.backtest_triggers ...` but `ii.bat` only wires `backtest-yield`. Add the subcommand or document it as `python -m` only. |
| `analytics/quant_smoke.py`            | 245 | manual quant sanity-check tool | Last modified 2026-04-26, never imported. Likely a sprint scratch — confirm intent then either wire into a periodic check or move to `tests/`. |
| `scripts/build_knowledge_cards.py`    | 244 | dossier build pipeline | Imported by nothing. Generates "knowledge cards" — likely intended for vault but never wired into `obsidian_bridge.py` or the dossier flow. Confirm and wire or freeze. |

Plus a stray top-level file:

| File                                | LoC | Status |
|-------------------------------------|-----|--------|
| `_scan_dead_code.py` (repo root)    | 219 | Sibling of one-shot audit scripts that lived in `scripts/` and were deleted yesterday. Probably the scaffold of the dead-code scanner used during Phase BB. Not in `.bat`, not imported. **Likely safe to delete after a 1-shot review.** |

## Patterns

1. **Perpetuum signal exhaustion** — 9/12 perpetuums produced zero alerts in the last 7 days. After Phase F bulk-ignore (vault drift), Phase J thesis 100%, Phase BB code-health auto-fix, the existing signal sets have largely been silenced. Either (a) write new signals for the silent ones, (b) lower their cadence (cron weekly, not daily), or (c) demote to T0 frozen.

2. **`autoresearch` perpetuum has no run history** — registered, wired into `daily_run.bat`, but `perpetuum_run_log` has zero rows. Worth tailing today's `daily_run` log to see if it errors silently, or if its logging path bypasses `perpetuum_run_log`.

3. **`library_signals` enabled=False but last run shows 16 alerts** — the freeze in code (`agents/perpetuum/library_signals.py:31 enabled = False`) didn't land before the last cron, OR the master skipped it but a stale row remains. Cross-check Phase F freeze date vs run_log timestamps.

4. **Agents declared in `config/agents.yaml` count toward "wired" even without code-grep hits** — the registry uses dynamic dotted-path import (`agents.X:ClassName`), so `data_janitor`, `portfolio_matcher`, `analyst_backtest`, `meta_agent`, `risk_auditor`, `devils_advocate`, `research_scout`, `subscription_fetch`, `thesis_refresh`, `holding_wiki_synthesizer` are all live agents — not orphans even though static grep shows few callers.

## Suggested actions

1. **Diagnose `autoresearch` perpetuum logging gap** — `grep "PERPETUUM" logs/daily_run_*.log | grep autoresearch` to confirm whether it even gets invoked. If yes → log-write bug. If no → master skips it.
2. **Clarify `library_signals` freeze state** — either re-enable (and accept its alerts) or stop scheduling it in the master loop entirely.
3. **Decide fate of the 5 orphaned modules** above. Path A: wire each into a visible surface (dashboard / daily brief / ii subcommand). Path B: move them to a `agents/_attic/` and `analytics/_attic/` graveyard, freeing import surface.
4. **Drop the 3 orphaned scripts** (`telegram_loop`, `_terminal`, `fetch_kings_aristocrats`) and the root-level `_scan_dead_code.py` after 1-shot review — none have any caller and the functional successor exists in each case.
5. **Promote zero-alert perpetuums to weekly cadence** — daily runs that always emit `alerts=0` for 7d straight are pure subject-counting noise; weekly cron + on-demand `--only X` covers them.
