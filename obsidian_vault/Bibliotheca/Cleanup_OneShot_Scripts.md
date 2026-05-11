# Cleanup: One-Shot Scripts — 2026-04-27 (overnight)

Audit driven by CLAUDE.md anti-pattern rule:
> "Scripts one-shot específicos de um ticker (ex: `itsa4_drip_scenario.py`) são anti-padrão — generalizar e apagar o one-shot."

Scope: `scripts/`, `agents/`, `analytics/`, `fetchers/`. Sacred dirs left alone:
`library/`, `obsidian_vault/`, `data/`, `logs/`, `.git/`, `.venv/`.

## Summary
- Files scanned: 124 .py files (scripts=80, agents=29, analytics=15, fetchers=13)
- Files deleted: 2
- Files investigated and kept: 8
- Files flagged for human review: 1
- LoC removed: ~974 (153 + 821)

## Deleted (with reasons)

| File | LoC | Reason |
|---|---|---|
| `scripts/_info_power_audit.py` | 153 | One-shot dated audit (`print("INFORMATION POWER AUDIT — 2026-04-26")` hardcoded). Zero references in repo, zero imports, not in any `.bat`. Untracked in git. Was clearly run-once for the Phase U.0 audit moment. |
| `scripts/render_home_html.py` | 821 | Generates a static `home.html` for the deprecated React desktop. Per memory `phase_u0_unification_sweep`: "React desktop deprecated. helena.css unifica Streamlit ↔ Obsidian." Not in `daily_run.bat`, not in `ii.bat`, not imported anywhere. Untracked in git. Output path `obsidian_vault/_assets/home.html` superseded by Streamlit dashboard + Obsidian Home.md. |

## Investigated, kept

| File | Reason kept |
|---|---|
| `scripts/migrate_fundamentals_extra.py` | DB schema migration (idempotent ALTER TABLE). Safe to rerun after fresh init_db; cheap to keep, risk of confusion if dropped. |
| `scripts/migrate_thesis_health.py` | Same — creates `thesis_health` table; supports Ad Perpetuum Validator (still wrapped by perpetuum.thesis). |
| `scripts/recompute_fii_streaks.py` | Idempotent recompute of `distribution_streak_months` from `dividends`. Useful when FII data backfills come in; not a one-shot, just rarely-run. |
| `scripts/vault_clean_video_names.py` | Renames `videos/<id>.md` → readable filenames with alias preservation. Idempotent. May be re-run as new YouTube ingests land. |
| `scripts/backfill_us_bank_tangibles.py` | Backfill TBVPS/ROTCE for US banks. Re-runnable with new bank tickers; not single-ticker. |
| `scripts/build_glossary.py` | Generates `obsidian_vault/Glossary/` (15+ files exist). Vault content producer — explicitly protected. |
| `scripts/dossier_tutor.py` | Injects `## Tutor` section into all `_DOSSIE.md` files. Vault content producer for 30+ dossiers. |
| `scripts/_terminal.py` | Streamlit CSS module. Currently no `import` references (potentially orphaned post-Phase U.0 helena.css unification), BUT docstring claims active use in 7 dashboard pages. See "Suspicious" below. |

## Suspicious (flag for human review)

| File | Issue |
|---|---|
| `scripts/_terminal.py` (10.6KB, ~280 LoC) | Bloomberg-inspired CSS/Plotly template module. **Zero imports across codebase** (`grep` for `from scripts._terminal` and `import _terminal` returned nothing), but its docstring says "Usado em: Home, Portfolio, Triggers, Signals, Screener, Paper Signals, Perpetuum Health". Either (a) the dashboard pages it claims to back never wired it up, or (b) it was wired then ripped during Phase U.0 helena.css unification. **Recommendation**: open `dashboard_app.py` page-by-page and confirm — if helena.css fully replaced it, delete; otherwise wire it back. Conservatively kept this round. |

## Patterns observed

1. **No ticker-named one-shots present** — `grep` for files matching `^(itsa4|vale3|petr|bbas|abcb|aapl|msft|googl|axia|btg)*` returned zero across all four target dirs. Either the rule is being respected, or past one-shots were already cleaned. Good.
2. **No `_test_/_tmp_/_scratch_/_one_off_/_backup_/_old_/_deprecated_` files** in any of the four dirs. Discipline holding.
3. **The two deletions both had `2026-04-26` artefacts** in their content/intent — born during the heavy Phase U.0/AA/BB/CC/DD/F/G/H/I/J/K/K.2/K.3 burst yesterday. They served their moment then went stale within 24h. Worth watching: rapid sprint phases tend to leave behind one-shots.
4. **Dashboard `_*.py` private modules** (`_theme`, `_components`, `_editorial`, `_carteiras`, `_captains_log`) are all properly imported by `dashboard_app.py` or `captains_log_telegram.py`. Only `_terminal` is the odd one out.

## Verification
- `git status` shows the two deleted files were untracked (never committed) — no destructive removal of versioned work.
- All 8 "kept" files were checked for `.bat` references and `import` references before deciding.
