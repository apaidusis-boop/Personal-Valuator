# 🪦 Cemetery 2026-05-13 — manifest
## Burial @ 2026-05-13T22:42:25
_Audit IDs: MA-CD-001, MA-CD-002, MA-CD-003, MA-CD-004, MA-CD-005, MA-VE-001, MA-VE-002, MA-VE-003, MA-VE-004, MA-FE-001, MA-FE-002, MA-FE-003_


## Burial @ 2026-05-13T22:42:48
_Audit IDs: MA-CD-001, MA-CD-002, MA-CD-003, MA-CD-004, MA-CD-005, MA-VE-001, MA-VE-002, MA-VE-003, MA-VE-004, MA-FE-001, MA-FE-002, MA-FE-003_

- **MA-CD-001** `agents/roles/classification.py` → `cemetery/2026-05-13/CODE-DEAD/agents/roles/classification.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-05-13/CODE-DEAD/agents/roles/classification.py" "agents/roles/classification.py"` (or `mv` if not staged)
- **MA-CD-002** `agents/roles/critic.py` → `cemetery/2026-05-13/CODE-DEAD/agents/roles/critic.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-05-13/CODE-DEAD/agents/roles/critic.py" "agents/roles/critic.py"` (or `mv` if not staged)
- **MA-CD-003** `agents/roles/decision.py` → `cemetery/2026-05-13/CODE-DEAD/agents/roles/decision.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-05-13/CODE-DEAD/agents/roles/decision.py" "agents/roles/decision.py"` (or `mv` if not staged)
- **MA-CD-004** `agents/roles/extraction.py` → `cemetery/2026-05-13/CODE-DEAD/agents/roles/extraction.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-05-13/CODE-DEAD/agents/roles/extraction.py" "agents/roles/extraction.py"` (or `mv` if not staged)
- **MA-CD-005** `agents/roles/synthesis.py` → `cemetery/2026-05-13/CODE-DEAD/agents/roles/synthesis.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-05-13/CODE-DEAD/agents/roles/synthesis.py" "agents/roles/synthesis.py"` (or `mv` if not staged)
- **MA-VE-001** `obsidian_vault/Escrito por Evandro Medeiros em Ações.md` → `cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/Escrito por Evandro Medeiros em Ações.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/Escrito por Evandro Medeiros em Ações.md" "obsidian_vault/Escrito por Evandro Medeiros em Ações.md"` (or `mv` if not staged)
- **MA-VE-002** `obsidian_vault/data/_.md` → `cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/data/_.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/data/_.md" "obsidian_vault/data/_.md"` (or `mv` if not staged)
- **MA-VE-003** `obsidian_vault/market-researcher/_.md` → `cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/market-researcher/_.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/market-researcher/_.md" "obsidian_vault/market-researcher/_.md"` (or `mv` if not staged)
- **MA-VE-004** `obsidian_vault/reference/common-patterns.md` → `cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/reference/common-patterns.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-05-13/VAULT-EMPTY/obsidian_vault/reference/common-patterns.md" "obsidian_vault/reference/common-patterns.md"` (or `mv` if not staged)
- **MA-FE-001** `obsidian_vault/daily_logs` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "obsidian_vault/daily_logs"` (if needed)
- **MA-FE-002** `obsidian_vault/voice_notes` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "obsidian_vault/voice_notes"` (if needed)
- **MA-FE-003** `data/locks` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "data/locks"` (if needed)

## Burial @ 2026-05-13T22:43:57
_Audit IDs: MA-CO-001, MA-UN-014, MA-UN-018, MA-UN-019, MA-UN-020, MA-UN-023, MA-UN-024, MA-UN-033, MA-UN-034, MA-UN-035, MA-UN-036, MA-UN-038, MA-UN-044, MA-UN-045_

- **MA-CO-001** `scripts/morning_itsa4_check.py` → `cemetery/2026-05-13/CODE-ONESHOT/scripts/morning_itsa4_check.py`
  - Category: CODE-ONESHOT
  - Reason: filename contains ticker 'ITSA4' from universe.yaml; CLAUDE.md flags one-shot ticker scripts as anti-pattern
  - Restore: `git mv "cemetery/2026-05-13/CODE-ONESHOT/scripts/morning_itsa4_check.py" "scripts/morning_itsa4_check.py"` (or `mv` if not staged)
- **MA-UN-014** `scripts/extend_2026-05-09.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/extend_2026-05-09.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/extend_2026-05-09.py" "scripts/extend_2026-05-09.py"` (or `mv` if not staged)
- **MA-UN-018** `scripts/midnight_2026-05-09.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/midnight_2026-05-09.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/midnight_2026-05-09.py" "scripts/midnight_2026-05-09.py"` (or `mv` if not staged)
- **MA-UN-019** `scripts/migrate_decision_quality.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/migrate_decision_quality.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/migrate_decision_quality.py" "scripts/migrate_decision_quality.py"` (or `mv` if not staged)
- **MA-UN-020** `scripts/migrate_provenance.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/migrate_provenance.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/migrate_provenance.py" "scripts/migrate_provenance.py"` (or `mv` if not staged)
- **MA-UN-023** `scripts/night_shift_batch.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/night_shift_batch.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/night_shift_batch.py" "scripts/night_shift_batch.py"` (or `mv` if not staged)
- **MA-UN-024** `scripts/night_shift_report.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/night_shift_report.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/night_shift_report.py" "scripts/night_shift_report.py"` (or `mv` if not staged)
- **MA-UN-033** `scripts/seed_br_watchlist.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_br_watchlist.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_br_watchlist.py" "scripts/seed_br_watchlist.py"` (or `mv` if not staged)
- **MA-UN-034** `scripts/seed_holdings_yaml.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_holdings_yaml.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_holdings_yaml.py" "scripts/seed_holdings_yaml.py"` (or `mv` if not staged)
- **MA-UN-035** `scripts/seed_tier_a_us.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_tier_a_us.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_tier_a_us.py" "scripts/seed_tier_a_us.py"` (or `mv` if not staged)
- **MA-UN-036** `scripts/seed_us_watchlist.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_us_watchlist.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/seed_us_watchlist.py" "scripts/seed_us_watchlist.py"` (or `mv` if not staged)
- **MA-UN-038** `scripts/update_portfolio_may2026.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/update_portfolio_may2026.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/update_portfolio_may2026.py" "scripts/update_portfolio_may2026.py"` (or `mv` if not staged)
- **MA-UN-044** `scripts/overnight/nn4_backfill_orchestrator.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/overnight/nn4_backfill_orchestrator.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/overnight/nn4_backfill_orchestrator.py" "scripts/overnight/nn4_backfill_orchestrator.py"` (or `mv` if not staged)
- **MA-UN-045** `scripts/overnight/overnight_2026_05_09.py` → `cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/overnight/overnight_2026_05_09.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-05-13/CODE-UNDOCUMENTED/scripts/overnight/overnight_2026_05_09.py" "scripts/overnight/overnight_2026_05_09.py"` (or `mv` if not staged)