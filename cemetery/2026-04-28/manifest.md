# 🪦 Cemetery 2026-04-28 — manifest
## Burial @ 2026-04-28T21:44:56
_Audit IDs: MA-CD-001, MA-CD-002, MA-VE-001, MA-VE-002, MA-VE-003, MA-VE-004, MA-VE-005, MA-VE-006, MA-VE-007, MA-VD-001, MA-FE-001, MA-FE-002, MA-FE-003, MA-FE-004_


## Burial @ 2026-04-28T21:45:07
_Audit IDs: MA-CD-001, MA-CD-002, MA-VE-001, MA-VE-002, MA-VE-003, MA-VE-004, MA-VE-005, MA-VE-006, MA-VE-007, MA-VD-001, MA-FE-001, MA-FE-002, MA-FE-003, MA-FE-004_


## Burial @ 2026-04-28T21:46:17
_Audit IDs: MA-CD-001, MA-CD-002, MA-VE-001, MA-VE-002, MA-VE-003, MA-VE-004, MA-VE-005, MA-VE-006, MA-VD-001, MA-FE-001, MA-FE-002, MA-FE-003, MA-FE-004_

- **MA-CD-001** `agents/_telegram.py` → `cemetery/2026-04-28/CODE-DEAD/agents/_telegram.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-04-28/CODE-DEAD/agents/_telegram.py" "agents/_telegram.py"` (or `mv` if not staged)
- **MA-CD-002** `scripts/_terminal.py` → `cemetery/2026-04-28/CODE-DEAD/scripts/_terminal.py`
  - Category: CODE-DEAD
  - Reason: no `__main__`, not imported anywhere, not in catalog — likely dead
  - Restore: `git mv "cemetery/2026-04-28/CODE-DEAD/scripts/_terminal.py" "scripts/_terminal.py"` (or `mv` if not staged)
- **MA-VE-001** `obsidian_vault/2026-04-23.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/2026-04-23.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/2026-04-23.md" "obsidian_vault/2026-04-23.md"` (or `mv` if not staged)
- **MA-VE-002** `obsidian_vault/Joshua Kennedy.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Joshua Kennedy.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Joshua Kennedy.md" "obsidian_vault/Joshua Kennedy.md"` (or `mv` if not staged)
- **MA-VE-003** `obsidian_vault/Obsidian AI plugins.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Obsidian AI plugins.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Obsidian AI plugins.md" "obsidian_vault/Obsidian AI plugins.md"` (or `mv` if not staged)
- **MA-VE-004** `obsidian_vault/tickers.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/tickers.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/tickers.md" "obsidian_vault/tickers.md"` (or `mv` if not staged)
- **MA-VE-005** `obsidian_vault/Tobi Opeyemi Amure.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Tobi Opeyemi Amure.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/Tobi Opeyemi Amure.md" "obsidian_vault/Tobi Opeyemi Amure.md"` (or `mv` if not staged)
- **MA-VE-006** `obsidian_vault/briefings/2026-04-24.md` → `cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/briefings/2026-04-24.md`
  - Category: VAULT-EMPTY
  - Reason: body has 0 meaningful chars (threshold 100)
  - Restore: `git mv "cemetery/2026-04-28/VAULT-EMPTY/obsidian_vault/briefings/2026-04-24.md" "obsidian_vault/briefings/2026-04-24.md"` (or `mv` if not staged)
- **MA-VD-001** `reports/_phases/HANDOFF_PHASE_Z_UI.md` → `cemetery/2026-04-28/VAULT-DEPRECATED/reports/_phases/HANDOFF_PHASE_Z_UI.md`
  - Category: VAULT-DEPRECATED
  - Reason: filename matches stale pattern 'HANDOFF_PHASE_[A-Z]+'
  - Restore: `git mv "cemetery/2026-04-28/VAULT-DEPRECATED/reports/_phases/HANDOFF_PHASE_Z_UI.md" "reports/_phases/HANDOFF_PHASE_Z_UI.md"` (or `mv` if not staged)
- **MA-FE-001** `scripts/agents` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "scripts/agents"` (if needed)
- **MA-FE-002** `library/methods/drafts` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "library/methods/drafts"` (if needed)
- **MA-FE-003** `data/subscriptions/pdfs/finclass` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "data/subscriptions/pdfs/finclass"` (if needed)
- **MA-FE-004** `reports/_archive` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "reports/_archive"` (if needed)

## Burial @ 2026-04-28T21:57:47
_Audit IDs: MA-UN-025, MA-UN-026, MA-UN-027, MA-UN-028, MA-UN-029, MA-UN-030_

- **MA-UN-025** `scripts/overnight/ab_qwen3_vs_14b.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/ab_qwen3_vs_14b.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/ab_qwen3_vs_14b.py" "scripts/overnight/ab_qwen3_vs_14b.py"` (or `mv` if not staged)
- **MA-UN-026** `scripts/overnight/fix_cr_pollution.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/fix_cr_pollution.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/fix_cr_pollution.py" "scripts/overnight/fix_cr_pollution.py"` (or `mv` if not staged)
- **MA-UN-027** `scripts/overnight/generate_methods_from_damodaran.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/generate_methods_from_damodaran.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/generate_methods_from_damodaran.py" "scripts/overnight/generate_methods_from_damodaran.py"` (or `mv` if not staged)
- **MA-UN-028** `scripts/overnight/orchestrator.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/orchestrator.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/orchestrator.py" "scripts/overnight/orchestrator.py"` (or `mv` if not staged)
- **MA-UN-029** `scripts/overnight/populate_thesis.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/populate_thesis.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/populate_thesis.py" "scripts/overnight/populate_thesis.py"` (or `mv` if not staged)
- **MA-UN-030** `scripts/overnight/rag_research_batch.py` → `cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/rag_research_batch.py`
  - Category: CODE-UNDOCUMENTED
  - Reason: has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete
  - Restore: `git mv "cemetery/2026-04-28/CODE-UNDOCUMENTED/scripts/overnight/rag_research_batch.py" "scripts/overnight/rag_research_batch.py"` (or `mv` if not staged)