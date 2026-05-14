# 🪦 Cemetery 2026-05-14 — manifest

Morning cleanup session (Wave 2 — biggest sweep yet).

User feedback from morning 2026-05-14: "33 items isn't enough — there's still much duplicated/triplicated old info scattered". 
Goal: per-ticker hubs are now the entry point; everything older/duplicated/superseded goes here (reversible).

All restores via `git mv` since renames are tracked.

---

## Burial @ 2026-05-14 morning


### Wave 1 — Superseded overnight scrapes (2 dirs, 142 files)
- **W1-001** `obsidian_vault/Overnight_2026-05-11/` (140 files) → `cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Overnight_2026-05-11/`
  - Reason: superseded by Overnight_2026-05-13/ (newer scrape of same universe)
  - Per-ticker links remain in `obsidian_vault/hubs/<TK>.md` history journal
  - Restore: `git mv "cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Overnight_2026-05-11" "obsidian_vault/Overnight_2026-05-11"`
- **W1-002** `obsidian_vault/Pilot_Deep_Dive_2026-05-10/` (7 files) → `cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Pilot_Deep_Dive_2026-05-10/`
  - Reason: pilot mission complete (5 tickers proof-of-concept of Playwright+markitdown pipeline)
  - Restore: `git mv "cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Pilot_Deep_Dive_2026-05-10" "obsidian_vault/Pilot_Deep_Dive_2026-05-10"`
- **W1-003** `obsidian_vault/Pilot_Deep_Dive_2026-05-11/` (2 untracked files) → `cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Pilot_Deep_Dive_2026-05-11/`
  - Reason: tiny pilot, missions done; untracked = never committed
  - Restore: `mv "cemetery/2026-05-14/SUPERSEDED-obsidian_vault-Pilot_Deep_Dive_2026-05-11" "obsidian_vault/Pilot_Deep_Dive_2026-05-11"`


## Burial @ 2026-05-14T06:49:17
_Audit IDs: MA-FE-001, MA-FE-002, MA-FE-003_

- **MA-FE-001** `obsidian_vault/data` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "obsidian_vault/data"` (if needed)
- **MA-FE-002** `obsidian_vault/market-researcher` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "obsidian_vault/market-researcher"` (if needed)
- **MA-FE-003** `obsidian_vault/reference` (FOLDER-EMPTY) — directory was empty, removed.
  - Restore: `mkdir -p "obsidian_vault/reference"` (if needed)