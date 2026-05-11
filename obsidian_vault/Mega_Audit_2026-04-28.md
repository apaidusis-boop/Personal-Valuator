# 🧹 Mega Audit — 2026-04-28

> **T1 Observer**. Audit-only — zero ficheiros tocados. User aprova batch-a-batch.
> Princípios Karpathy: Surgical changes + Simplicity first → candidatos a remoção/unificação.

## Resumo

| Categoria | Count | Severidade |
|---|---|---|
| CODE-DEAD | 0 | 🔴 high confidence (no main + no import + no catalog) |
| CODE-UNDOCUMENTED | 20 | 🟠 medium (catalog gap OR obsoleto) |
| CODE-ONESHOT | 0 | 🟠 medium-high (anti-pattern explícito) |
| CODE-MARK-OLD | 0 | 🟡 medium (autor marcou) |
| VAULT-EMPTY | 0 | 🟡 medium (verificar caso-a-caso) |
| VAULT-DEPRECATED | 0 | 🟡 medium (provavelmente safe) |
| MEM-STALE | 0 | 🟢 low (clean-up trivial) |
| FOLDER-EMPTY | 0 | 🟢 low (apagar safe) |

**Total candidatos**: 20

---

## CODE-DEAD

_Python files com **NO `__main__`**, NÃO importados por nada, NÃO no catalog. Alta confiança — provavelmente seguros para apagar._

✅ Nenhum candidato.

## CODE-UNDOCUMENTED

_Python files **com `__main__`** (entry points runnable) mas NÃO mencionados em `CLAUDE.md` catalog ou `ii.bat` dispatcher. Acção: ou adicionar ao catalog, ou apagar se obsoleto._

- **MA-UN-001** `agents/helena/report.py` — 247 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-002** `fetchers/massive_fetcher.py` — 174 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-003** `scripts/backfill_us_bank_tangibles.py` — 179 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-004** `scripts/build_glossary.py` — 945 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-005** `scripts/build_knowledge_cards.py` — 244 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-006** `scripts/dossier_tutor.py` — 323 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-007** `scripts/export_macro_csv.py` — 50 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-008** `scripts/fetch_kings_aristocrats.py` — 74 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-009** `scripts/migrate_fundamentals_extra.py` — 56 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-010** `scripts/migrate_thesis_health.py` — 56 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-011** `scripts/notify_events.py` — 193 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-012** `scripts/rotate_logs.py` — 86 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-013** `scripts/telegram_loop.py` — 112 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-014** `scripts/vault_clean_video_names.py` — 159 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-015** `monitors/cvm_pdf_extractor.py` — 154 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-016** `library/ri/catalog_autopopulate.py` — 152 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-017** `library/ri/cvm_parser.py` — 259 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-018** `library/ri/cvm_parser_bank.py` — 343 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-019** `library/ri/fii_filings.py` — 327 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-020** `library/ri/quarterly_single.py` — 267 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_

## CODE-ONESHOT

_Scripts com nome contendo ticker real do `universe.yaml` (anti-pattern CLAUDE.md). Generalizar para `--ticker X` e apagar one-shot._

✅ Nenhum candidato.

## CODE-MARK-OLD

_Files com markers `# DEPRECATED` / `# LEGACY` / `# TODO REMOVE` em código. Hint deixado pelo autor._

✅ Nenhum candidato.

## VAULT-EMPTY

_Markdown files com <100 meaningful chars no body. Provavelmente stub esquecido ou rascunho abandonado._

✅ Nenhum candidato.

## VAULT-DEPRECATED

_Markdown com filename pattern `HANDOFF_*` / `_DEPRECATED.md` / `PROPOSED_*`. Phase docs antigos._

✅ Nenhum candidato.

## MEM-STALE

_MEMORY.md aponta para .md file inexistente. Clean-up trivial._

✅ Nenhum candidato.

## FOLDER-EMPTY

_Directorias sem ficheiros (recursivo). Apagar é seguro._

✅ Nenhum candidato.

---

## Workflow para apagar

1. Reviewer escolhe IDs específicos (ex: `MA-FE-001`, `MA-FE-003`)
2. Comanda: "apaga MA-FE-001..003 + MA-MS-001..005"
3. Execução manual ou via futuro `mega_auditor.py --apply --ids ...`
4. Commit em git ANTES de cada batch (rollback seguro)