# 🧹 Mega Audit — 2026-05-13

> **T1 Observer**. Audit-only — zero ficheiros tocados. User aprova batch-a-batch.
> Princípios Karpathy: Surgical changes + Simplicity first → candidatos a remoção/unificação.

## Resumo

| Categoria | Count | Severidade |
|---|---|---|
| CODE-DEAD | 5 | 🔴 high confidence (no main + no import + no catalog) |
| CODE-UNDOCUMENTED | 50 | 🟠 medium (catalog gap OR obsoleto) |
| CODE-ONESHOT | 1 | 🟠 medium-high (anti-pattern explícito) |
| CODE-MARK-OLD | 0 | 🟡 medium (autor marcou) |
| VAULT-EMPTY | 4 | 🟡 medium (verificar caso-a-caso) |
| VAULT-DEPRECATED | 0 | 🟡 medium (provavelmente safe) |
| MEM-STALE | 0 | 🟢 low (clean-up trivial) |
| FOLDER-EMPTY | 3 | 🟢 low (apagar safe) |

**Total candidatos**: 63

---

## CODE-DEAD

_Python files com **NO `__main__`**, NÃO importados por nada, NÃO no catalog. Alta confiança — provavelmente seguros para apagar._

- **MA-CD-001** `agents/roles/classification.py` — 61 LoC
  - _no `__main__`, not imported anywhere, not in catalog — likely dead_
- **MA-CD-002** `agents/roles/critic.py` — 71 LoC
  - _no `__main__`, not imported anywhere, not in catalog — likely dead_
- **MA-CD-003** `agents/roles/decision.py` — 80 LoC
  - _no `__main__`, not imported anywhere, not in catalog — likely dead_
- **MA-CD-004** `agents/roles/extraction.py` — 56 LoC
  - _no `__main__`, not imported anywhere, not in catalog — likely dead_
- **MA-CD-005** `agents/roles/synthesis.py` — 56 LoC
  - _no `__main__`, not imported anywhere, not in catalog — likely dead_

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
- **MA-UN-012** `scripts/cross_source_spotcheck.py` — 132 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-013** `scripts/derive_fundamentals_from_filings.py` — 625 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-014** `scripts/extend_2026-05-09.py` — 425 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-015** `scripts/extract_user_profile.py` — 190 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-016** `scripts/final_overnight_trigger.py` — 123 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-017** `scripts/inject_ticker_insights.py` — 360 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-018** `scripts/midnight_2026-05-09.py` — 650 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-019** `scripts/migrate_decision_quality.py` — 90 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-020** `scripts/migrate_provenance.py` — 50 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-021** `scripts/morning_curated.py` — 160 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-022** `scripts/morning_itsa4_check.py` — 61 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-023** `scripts/night_shift_batch.py` — 158 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-024** `scripts/night_shift_report.py` — 272 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-025** `scripts/overnight_backfill.py` — 385 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-026** `scripts/overnight_code_health.py` — 206 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-027** `scripts/overnight_orchestrator.py` — 505 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-028** `scripts/overnight_preflight.py` — 105 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-029** `scripts/patch_failed_urls.py` — 82 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-030** `scripts/pilot_deep_dive.py` — 1487 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-031** `scripts/pod_poll.py` — 315 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-032** `scripts/refresh_benchmarks.py` — 115 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-033** `scripts/seed_br_watchlist.py` — 52 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-034** `scripts/seed_holdings_yaml.py` — 83 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-035** `scripts/seed_tier_a_us.py` — 53 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-036** `scripts/seed_us_watchlist.py` — 45 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-037** `scripts/sws_buffett_drip_cross.py` — 330 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-038** `scripts/update_portfolio_may2026.py` — 188 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-039** `scripts/wiki_lint.py` — 237 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-040** `scripts/yt_poll.py` — 322 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-041** `scripts/_gemma_corruption_check.py` — 97 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-042** `scripts/_ollama_probe.py` — 59 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-043** `scripts/_retry.py` — 172 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-044** `scripts/overnight/nn4_backfill_orchestrator.py` — 320 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-045** `scripts/overnight/overnight_2026_05_09.py` — 702 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-046** `scoring/consensus_target.py` — 303 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-047** `scoring/leap_of_faith.py` — 597 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-048** `analytics/cross_source_check.py` — 319 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-049** `analytics/decision_quality.py` — 557 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_
- **MA-UN-050** `analytics/sector_tilt.py` — 194 LoC, has `__main__`
  - _has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete_

## CODE-ONESHOT

_Scripts com nome contendo ticker real do `universe.yaml` (anti-pattern CLAUDE.md). Generalizar para `--ticker X` e apagar one-shot._

- **MA-CO-001** `scripts/morning_itsa4_check.py`
  - _filename contains ticker 'ITSA4' from universe.yaml; CLAUDE.md flags one-shot ticker scripts as anti-pattern_

## CODE-MARK-OLD

_Files com markers `# DEPRECATED` / `# LEGACY` / `# TODO REMOVE` em código. Hint deixado pelo autor._

✅ Nenhum candidato.

## VAULT-EMPTY

_Markdown files com <100 meaningful chars no body. Provavelmente stub esquecido ou rascunho abandonado._

- **MA-VE-001** `obsidian_vault/Escrito por Evandro Medeiros em Ações.md` — body=0c
  - _body has 0 meaningful chars (threshold 100)_
- **MA-VE-002** `obsidian_vault/data/_.md` — body=0c
  - _body has 0 meaningful chars (threshold 100)_
- **MA-VE-003** `obsidian_vault/market-researcher/_.md` — body=0c
  - _body has 0 meaningful chars (threshold 100)_
- **MA-VE-004** `obsidian_vault/reference/common-patterns.md` — body=0c
  - _body has 0 meaningful chars (threshold 100)_

## VAULT-DEPRECATED

_Markdown com filename pattern `HANDOFF_*` / `_DEPRECATED.md` / `PROPOSED_*`. Phase docs antigos._

✅ Nenhum candidato.

## MEM-STALE

_MEMORY.md aponta para .md file inexistente. Clean-up trivial._

✅ Nenhum candidato.

## FOLDER-EMPTY

_Directorias sem ficheiros (recursivo). Apagar é seguro._

- **MA-FE-001** `obsidian_vault/daily_logs`
  - _directory contains no files (recursively)_
- **MA-FE-002** `obsidian_vault/voice_notes`
  - _directory contains no files (recursively)_
- **MA-FE-003** `data/locks`
  - _directory contains no files (recursively)_

---

## Workflow para apagar

1. Reviewer escolhe IDs específicos (ex: `MA-FE-001`, `MA-FE-003`)
2. Comanda: "apaga MA-FE-001..003 + MA-MS-001..005"
3. Execução manual ou via futuro `mega_auditor.py --apply --ids ...`
4. Commit em git ANTES de cada batch (rollback seguro)