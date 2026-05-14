# 🧹 Mega Audit — 2026-05-14

> **T1 Observer**. Audit-only — zero ficheiros tocados. User aprova batch-a-batch.
> Princípios Karpathy: Surgical changes + Simplicity first → candidatos a remoção/unificação.

## Resumo

| Categoria | Count | Severidade |
|---|---|---|
| CODE-DEAD | 0 | 🔴 high confidence (no main + no import + no catalog) |
| CODE-UNDOCUMENTED | 40 | 🟠 medium (catalog gap OR obsoleto) |
| CODE-ONESHOT | 0 | 🟠 medium-high (anti-pattern explícito) |
| CODE-MARK-OLD | 0 | 🟡 medium (autor marcou) |
| VAULT-EMPTY | 0 | 🟡 medium (verificar caso-a-caso) |
| VAULT-DEPRECATED | 0 | 🟡 medium (provavelmente safe) |
| MEM-STALE | 0 | 🟢 low (clean-up trivial) |
| FOLDER-EMPTY | 3 | 🟢 low (apagar safe) |

**Total candidatos**: 43

---

## CODE-DEAD

_Python files com **NO `__main__`**, NÃO importados por nada, NÃO no catalog. Alta confiança — provavelmente seguros para apagar._

✅ Nenhum candidato.

## CODE-UNDOCUMENTED

_Python files **com `__main__`** (entry points runnable) mas NÃO mencionados em `CLAUDE.md` catalog ou `ii.bat` dispatcher. Acção: ou adicionar ao catalog, ou apagar se obsoleto._

- **MA-UN-001** `agents/fiel_escudeiro.py` — 225 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-002** `agents/_lock.py` — 200 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-003** `agents/council/story.py` — 207 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-004** `fetchers/fiis_com_br_fetcher.py` — 333 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-005** `fetchers/fundamentus_fetcher.py` — 278 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-006** `fetchers/sec_xbrl_fetcher.py` — 692 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-007** `scripts/auto_import_taxlots.py` — 89 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-008** `scripts/auto_verdict_on_content.py` — 431 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-009** `scripts/backfill_intangibles.py` — 239 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-010** `scripts/backfill_strategy_tag.py` — 202 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-011** `scripts/bench_models.py` — 86 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-012** `scripts/build_tickers_index.py` — 129 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-013** `scripts/build_ticker_hubs.py` — 397 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-014** `scripts/cross_source_spotcheck.py` — 132 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-015** `scripts/derive_fundamentals_from_filings.py` — 625 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-016** `scripts/extract_user_profile.py` — 190 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-017** `scripts/final_overnight_trigger.py` — 123 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-018** `scripts/inject_ticker_insights.py` — 360 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-019** `scripts/morning_curated.py` — 160 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-020** `scripts/overnight_backfill.py` — 385 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-021** `scripts/overnight_code_health.py` — 206 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-022** `scripts/overnight_orchestrator.py` — 505 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-023** `scripts/overnight_preflight.py` — 105 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-024** `scripts/patch_failed_urls.py` — 82 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-025** `scripts/persona_handle_alias.py` — 86 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-026** `scripts/pilot_deep_dive.py` — 1487 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-027** `scripts/pod_poll.py` — 315 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-028** `scripts/refresh_benchmarks.py` — 115 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-029** `scripts/ri_url_resolver.py` — 830 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-030** `scripts/sws_buffett_drip_cross.py` — 330 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-031** `scripts/wiki_lint.py` — 237 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-032** `scripts/yt_poll.py` — 322 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-033** `scripts/_gemma_corruption_check.py` — 97 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-034** `scripts/_ollama_probe.py` — 59 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-035** `scripts/_retry.py` — 172 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-036** `scoring/consensus_target.py` — 303 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-037** `scoring/leap_of_faith.py` — 597 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-038** `analytics/cross_source_check.py` — 319 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-039** `analytics/decision_quality.py` — 557 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-040** `analytics/sector_tilt.py` — 194 LoC, has `__main__`
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

- **MA-FE-001** `obsidian_vault/data`
  - _directory contains no files (recursively)_
- **MA-FE-002** `obsidian_vault/market-researcher`
  - _directory contains no files (recursively)_
- **MA-FE-003** `obsidian_vault/reference`
  - _directory contains no files (recursively)_

---

## Workflow para apagar

1. Reviewer escolhe IDs específicos (ex: `MA-FE-001`, `MA-FE-003`)
2. Comanda: "apaga MA-FE-001..003 + MA-MS-001..005"
3. Execução manual ou via futuro `mega_auditor.py --apply --ids ...`
4. Commit em git ANTES de cada batch (rollback seguro)