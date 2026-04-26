# Cleanup: Dead Code — 2026-04-27 (overnight)

## Summary
- Files scanned: 196
- Files modified: 62 (59 auto + 3 manual function-local imports)
- Unused imports removed: 88
- Dead function candidates flagged (NOT removed): 16
- Smoke tests passed: 62/62 (`py_compile` for all; 13 critical modules also passed real `import`)

Methodology: AST-based scan (no `pyflakes`/`ruff` available). Each file parsed with `ast`, top-level imports cross-checked against `ast.Name` / `ast.Attribute` references plus string-constant occurrences (to avoid false positives from `getattr` / forward refs / typing strings). `__future__` imports ignored. Names listed in `__all__` preserved. Top-level functions cross-referenced via word-boundary regex across every `.py` in scope.

Skip rules respected: `library/clippings_ingest.py`, `scripts/research_digest.py`, `scripts/build_glossary.py`, `scripts/dossier_tutor.py`, `agents/variant_perception.py` were marked do-not-touch and not modified. `library/chunks/`, `library/insights/`, `library/methods/`, `data/`, `obsidian_vault/`, `.git/`, `.venv/`, `__pycache__/`, `library/books/`, `library/ri/cache/` excluded from scan.

## Files modified — auto-fix (top-level imports)

| File | Imports removed |
|---|---|
| `scripts/dashboard_app.py` | 9 (inject_css, brand_sidebar, section_header, story_card, status_pill, verdict_pill, divider, hero, ask_box) |
| `scripts/_captains_log.py` | 3 (field, datetime, timedelta) |
| `scripts/weekly_report.py` | 3 (json, datetime, timezone) |
| `agents/research_scout.py` | 3 (datetime, timedelta, timezone) |
| `scripts/br_drip_optimizer.py` | 2 (derive_scenarios, project_drip) |
| `scripts/compare_tickers.py` | 2 (timedelta, _ptax) |
| `scripts/daily_diff.py` | 2 (UTC, datetime) |
| `scripts/metrics_baseline.py` | 2 (subprocess, sys) |
| `scripts/notify_events.py` | 2 (datetime, timezone) |
| `scripts/predictions_evaluate.py` | 2 (datetime, timezone) |
| `scripts/trigger_monitor.py` | 2 (quantiles, Any) |
| `agents/decision_journal_intel.py` | 2 (json, timedelta) |
| `agents/perpetuum_validator.py` | 2 (datetime, timezone) |
| `agents/perpetuum/autoresearch.py` | 2 (timezone, _stats) |
| `fetchers/cache_policy.py` | 2 (sqlite3, Path) |
| `library/ri/cvm_filings.py` | 2 (hashlib, CATALOG_PATH) |
| `scripts/agent_morning.py` | 1 (timedelta) |
| `scripts/analyze_ticker.py` | 1 (json) |
| `scripts/daily_update.py` | 1 (datetime) |
| `scripts/dossier.py` | 1 (Iterator) |
| `scripts/earnings_surprise.py` | 1 (timedelta) |
| `scripts/import_portfolio.py` | 1 (Iterable) |
| `scripts/migrate_fundamentals_extra.py` | 1 (sys) |
| `scripts/panorama.py` | 1 (json) |
| `scripts/peer_compare.py` | 1 (median) |
| `scripts/refresh_ticker.py` | 1 (datetime) |
| `scripts/thesis_manager.py` | 1 (sys) |
| `scripts/vault_ask.py` | 1 (sqlite3) |
| `scripts/verdict_history.py` | 1 (asdict) |
| `agents/_base.py` | 1 (Any) |
| `agents/autoresearch.py` | 1 (time) |
| `agents/data_janitor.py` | 1 (timezone) |
| `agents/meta_agent.py` | 1 (timedelta) |
| `agents/portfolio_matcher.py` | 1 (json) |
| `agents/thesis_refresh.py` | 1 (Path) |
| `agents/thesis_synthesizer.py` | 1 (textwrap) |
| `agents/watchdog.py` | 1 (timezone) |
| `agents/perpetuum/method_discovery.py` | 1 (json) |
| `agents/perpetuum/ri_freshness.py` | 1 (datetime) |
| `agents/perpetuum/vault_health.py` | 1 (timedelta) |
| `agents/helena/curate.py` | 1 (field) |
| `analytics/backtest_regime.py` | 1 (field) |
| `analytics/backtest_triggers.py` | 1 (datetime) |
| `analytics/portfolio_stress.py` | 1 (json) |
| `fetchers/bacen_ifdata_fetcher.py` | 1 (Iterator) |
| `fetchers/bcb_fetcher.py` | 1 (sys) |
| `fetchers/sec_edgar_fetcher.py` | 1 (sys) |
| `fetchers/status_invest_mcp_fetcher.py` | 1 (Any) |
| `fetchers/yf_us_fetcher.py` | 1 (sys) |
| `fetchers/subscriptions/suno.py` | 1 (Path) |
| `library/extract_insights.py` | 1 (sys) |
| `library/ingest.py` | 1 (sys) |
| `library/paper_trade.py` | 1 (sys) |
| `library/rag.py` | 1 (json) |
| `library/ri/catalog.py` | 1 (Iterable) |
| `library/ri/cvm_codes.py` | 1 (CATALOG_PATH) |
| `library/ri/fii_filings.py` | 1 (date) |
| `monitors/cvm_monitor.py` | 1 (sys) |
| `monitors/sec_monitor.py` | 1 (sys) |

## Files modified — manual (function-local imports)

The auto-scanner only inspects module-level `import` statements. These three files
had unused names inside `def`-scoped imports; trimmed by hand:

| File | Imports removed |
|---|---|
| `scripts/research.py` | 1 (`project_drip` inside `_drip_summary`) |
| `scripts/obsidian_bridge.py` | 1 (`fx_rate` inside `_portfolio_live_snapshot`) |
| `scripts/subscriptions_cli.py` | 1 (`extract_html_text` inside `cmd_extract`) |

## Large files (LOC > 500) — extra-care confirmation

All passed `py_compile` after edit; spot-checked with real `import`:

| File | LOC | Removed | Status |
|---|---|---|---|
| `scripts/dashboard_app.py` | 1456 | 9 | py_compile OK (full import needs `plotly`, unrelated) |
| `scripts/obsidian_bridge.py` | 1387 | 1 (manual) | py_compile OK |
| `scripts/research.py` | 725 | 1 (manual) | py_compile OK |
| `scripts/dossier.py` | 719 | 1 | real import OK |
| `agents/helena/curate.py` | 584 | 1 | py_compile OK |
| `scripts/import_portfolio.py` | 559 | 1 | py_compile OK |

## Dead function candidates (NOT removed — needs human review)

Top-level functions whose names appear ZERO times across the whole codebase
(outside their own definition line). Excluded: `main`, `cli*`, dunder, decorated
functions, `_handler`/`_callback`/`_hook`/`_cmd`/`_command` suffixes, anything
mentioned in a string constant.

| Function | File | Reason flagged | Confidence |
|---|---|---|---|
| `compute_basket` | `scripts/_carteiras.py:101` | No callers found | Medium — `_carteiras.py` is a helper module; check if planned for an unfinished CLI (Path A baskets). |
| `inject_terminal_css` | `scripts/_terminal.py:255` | No callers found | Medium — sibling of `_theme.inject_css`; possibly orphaned after Helena CSS unification. |
| `_ago` | `scripts/dashboard_app.py:283` | Local helper never invoked | High — safe to drop, but file >500 LoC; verify no Streamlit `eval` magic. |
| `_resample_norm` | `scripts/render_home_html.py:33` | No callers | Medium — render_home_html may be in flux (Phase U.0/U.1 home minimal). |
| `build_payload` | `scripts/render_home_html.py:46` | No callers | Medium — same as above; could be the intended public entry point that nothing yet calls. |
| `save_theses` | `scripts/thesis_manager.py:40` | No callers | High — counterpart to a `load_theses` pattern; if thesis flow now writes through `agents.thesis_synthesizer`, this is dead. |
| `by_department` | `agents/_personas.py:61` | No callers | Medium — persona registry helper; might be intended for future agent routing. |
| `push_founder_alert` | `agents/_telegram.py:64` | No callers | Low — Telegram channel-aware push; likely reserved for upcoming alerting tier (Jarbas). Keep. |
| `statement_policy_for` | `fetchers/cache_policy.py:74` | No callers | Medium — cache_policy is a small policy module; check `subscriptions/_session` and `_pdf_extract`. |
| `fmt_date_br` | `fetchers/cache_policy.py:99` | No callers | Medium — duplicates `analytics.format.br_date`; likely dead, replaced by analytics helper. |
| `parse_date_br` | `fetchers/cache_policy.py:111` | No callers | Medium — same story; remove together with `fmt_date_br`. |
| `cache_payload` | `fetchers/status_invest_mcp_fetcher.py:107` | No callers | Medium — MCP fetcher is partially activated per memory note; defer until status_invest MCP wiring done. |
| `passes_graham_br_bank` | `fetchers/status_invest_mcp_fetcher.py:169` | No callers | Medium — duplicates logic in `scoring.engine`; dead unless MCP path goes live. |
| `performance_by_method` | `library/paper_trade.py:150` | No callers | High — counterpart of paper_trade closing; ought to feed the matcher / dashboard but currently unused. Consider wiring into Captain's Log instead of deleting. |
| `find_by_ticker` | `library/ri/catalog.py:94` | No callers | Medium — `catalog.all_tickers` is the hot path (recurring "watchlist not in catalog loop" bug). `find_by_ticker` may be intended for the planned `library/ri/catalog.py::all_tickers()` refactor. Keep. |
| `__ack_legacy` | `library/ri/catalog.py:106` | No callers | High — name suggests one-off legacy ack; safe to drop after grep across vault for any reference. |

Recommendation: do a focused PR per cluster — `cache_policy.py` (3 funcs), `status_invest_mcp_fetcher.py` (2 funcs), `library/ri/catalog.py` (1 func) — once you confirm no Phase X/Y plan reactivates them.

## Skipped (too risky / per-instruction)

| File | Reason |
|---|---|
| `library/clippings_ingest.py` | User instruction: just shipped, leave alone. |
| `scripts/research_digest.py` | User instruction: just shipped, leave alone. |
| `scripts/build_glossary.py` | User instruction: just shipped, leave alone. |
| `scripts/dossier_tutor.py` | User instruction: just shipped, leave alone. |
| `agents/variant_perception.py` | User instruction: just patched, leave alone. |

## Artefacts (gitignored helpers, can be deleted post-review)

- `_scan_dead_code.py` — AST scanner
- `_scan_dead_funcs.py` — function cross-reference
- `_apply_dead_imports.py` — surgical fixer (uses `ast.unparse`, preserves trailing `# noqa` comments)
- `_scan_dead_code_results.json`, `_scan_dead_funcs_results.json`, `_apply_dead_imports.log` — raw outputs

Suggested commit message:
> chore(cleanup): remove 88 unused imports across 62 files (overnight DC sweep)
