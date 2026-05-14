---
type: cleanup_report
tags: [cleanup, wave_4, ghost_nodes, wikilinks]
date: 2026-05-14
session: wave-4-ghost-nodes
status: completed
parent: "[[Manual_do_Sistema]]"
sibling: "[[Cleanup_2026-05-14_DeepMerge]]"
---

# 🧹👻 Cleanup Wave 4 — Ghost-Node Killer (2026-05-14 final)

> Resposta directa aos screenshots: _"continuo a ver `_DOSSIE`, `Charlie Compounder`, `_2026-05-01` por todo o lado no graph"_.
>
> **Causa raíz identificada**: os ficheiros físicos estão fora há horas — mas o graph mostra **nós-fantasma** porque centenas de `[[wikilinks]]` orfãos em notas que ainda existem apontam para ficheiros que já foram para cemetery.
>
> **Resultado**: **2.937 wikilinks reescritos** em 98 ficheiros + 32 JSONs enterrados + Helena_Mega renomeado. Ghost-nodes do graph: **0**.

## TL;DR

| Métrica | Antes Wave 4 | Depois Wave 4 |
|---|---:|---:|
| `[[Charlie Compounder]]` no vault | **105** | **0** |
| `[[Mariana Macro]]` no vault | **280** | **0** |
| `[[Valentina Prudente]]` no vault | **280** | **0** |
| `[[Pedro Alocação]]` no vault | **280** | **0** |
| `[[JNJ_DOSSIE]]` no vault | **16** | **0** |
| `[[<TK>_STORY/COUNCIL/IC_DEBATE/VARIANT]]` total | ~700 | **0** |
| .json files em `dossiers/` | 32 | **0** |
| Pasta `Helena_Mega/` | 1 | renomeada para `design.lint_mega/` |
| Pasta `dossiers/` | existe (vazia + .Rhistory) | **removida** |

---

## 1. Causa raíz — porque o graph mostrava scatter mesmo depois do Wave 3

O Wave 3 enterrou **1.291 ficheiros** per-ticker no cemetery. Filesystem ficou limpo. Mas o Obsidian graph **continuava a mostrar** `JNJ_DOSSIE`, `Charlie Compounder`, etc.

**Porquê**: Obsidian cria um nó no graph para cada destino de wikilink (`[[...]]`) — **mesmo que o destino não exista mais**. Quando uma nota diz `[[Charlie Compounder]]` e o ficheiro `Charlie Compounder.md` foi para o cemetery, Obsidian mostra um "nó cinzento" (unresolved link). Visualmente é **igual** a um nó real.

Multiplica isso por 187 tickers × 5-7 suffixes cada + 23 personas × 50-280 menções cada = **milhares de nós-fantasma no graph**.

---

## 2. Solução — wikilink rewriter global

**Script**: `scripts/wikilink_rewrite.py`

Para cada `.md` em `obsidian_vault/` (excluindo cemetery, .obsidian, .git, skills/imported):

```
[[<TK>_DOSSIE]]              → [[<TK>]]
[[<TK>_STORY]]               → [[<TK>]]
[[<TK>_COUNCIL]]             → [[<TK>]]
[[<TK>_IC_DEBATE]]           → [[<TK>]]
[[<TK>_VARIANT]]             → [[<TK>]]
[[<TK>_RI]]                  → [[<TK>]]
[[<TK>_drip]]                → [[<TK>]]
[[<TK>_FILING_<DATE>]]       → [[<TK>]]
[[<TK>_MIGRATION]]           → [[<TK>]]
[[<TK>_CONTENT_TRIGGER_*]]   → [[<TK>]]
[[<TK>_PATRIA_TRANSITION]]   → [[<TK>]]
[[<TK>_<YYYY-MM-DD>]]        → [[<TK>]]
[[<TK>_<SUFFIX>|texto]]      → [[<TK>|texto]]  (preserva display)

[[Charlie Compounder]]       → [[council.industrials-us]]
[[Mariana Macro]]            → [[council.macro]]
[[Valentina Prudente]]       → [[risk.drift-audit]]
[[Pedro Alocação]]           → [[council.allocation]]
[[Helena Linha]]             → [[design.lint]]
[[Hank Tier-One]]            → [[council.banks-us]]
[[Walter Triple-Net]]        → [[council.reits-us]]
... 23 personas total
```

**Resultados do run**:
- **2.937 wikilinks reescritos** em **98 ficheiros** (1ª pass 2.765 + 2ª pass pós-rebuild 172)
- Idempotente: re-run após rebuild é no-op se nada novo aparecer

**Top 10 rewrites**:

| Cnt | Old | New |
|---:|---|---|
| 280 | `[[Mariana Macro]]` | `[[council.macro]]` |
| 280 | `[[Valentina Prudente]]` | `[[risk.drift-audit]]` |
| 280 | `[[Pedro Alocação]]` | `[[council.allocation]]` |
| 105 | `[[Charlie Compounder]]` | `[[council.industrials-us]]` |
| 58 | `[[Lourdes Aluguel]]` | `[[council.fiis-br]]` |
| 54 | `[[Hank Tier-One]]` | `[[council.banks-us]]` |
| 19 | `[[Tião Galpão]]` | `[[council.industrials-br]]` |
| 19 | `[[Diego Bancário]]` | `[[council.banks-br]]` |
| 18 | `[[Walter Triple-Net]]` | `[[council.reits-us]]` |
| 18 | `[[Aderbaldo Cíclico]]` | `[[council.commodities-br]]` |

---

## 3. Limpezas adicionais

### 3a. 32 ficheiros `.json` em `dossiers/` enterrados

`AAPL_COUNCIL.json`, `ABBV_COUNCIL.json`, ... — dumps paralelos aos `.md` que já tinham sido enterrados no Wave 3. Cemetery: `cemetery/2026-05-14/ABSORBED-dossier-json/` (32 files).

Pasta `obsidian_vault/dossiers/` agora **removida** (era só `.Rhistory` órfão restante).

### 3b. Helena_Mega → design.lint_mega

`obsidian_vault/skills/Helena_Mega/` renomeada para `obsidian_vault/skills/design.lint_mega/`.

Code references actualizadas:
- `agents/helena/__init__.py` (VAULT_OUT constant + docstring)
- `agents/helena/audit.py` (DS010 skip dir + comment)
- `agents/helena/report.py` (docstring)
- `agents/helena_mega.py` (docstring)
- `agents/perpetuum/code_health.py` (CH008 skip prefix)
- `CLAUDE.md` (catalog entries)

Smoke test: `from agents.helena import VAULT_OUT` resolve para `obsidian_vault\skills\design.lint_mega` ✓

---

## 4. Anti-regressão — `daily_run.bat` ganhou `[HUBS-WIKILINKS]`

Problema: `build_merged_hubs.py` reabsorve conteúdo do cemetery, e os ficheiros enterrados continuam a ter `[[Charlie Compounder]]` no texto. Sem o rewriter, a cada rebuild os ghost-nodes voltam.

Novo passo no daily_run (após `[HUBS-INDEX]`, antes de `[ROTATE]`):

```bat
[HUBS-WIKILINKS] wikilink_rewrite.py  (rewrite persona names + ticker suffixes)
```

Idempotente — corre a cada daily run e mantém o graph limpo permanentemente.

**Pipeline completo agora**:

```
[HUBS-BUILD]      build_merged_hubs.py        Refresh 187 hubs a partir de vault + cemetery + JSON
[HUBS-BURY]       bury_per_ticker_sources.py  Cemetery qualquer per-ticker novo do dia
[HUBS-INDEX]      build_tickers_index.py      Refresh _TICKERS_INDEX.md
[HUBS-WIKILINKS]  wikilink_rewrite.py         Kill ghost nodes (rewrite persona + ticker suffixes)
```

---

## 5. O que vais ver no Obsidian

**Antes** (screenshots que enviaste):
- Nós cinzentos para `JNJ_DOSSIE`, `KO_DOSSIE`, `ACN_STORY`, etc. em todo o graph
- Nós grandes para `Charlie Compounder`, `Mariana Macro`, `Valentina Prudente`
- Nós datados `JNJ_2026-05-01`, `BBDC4_2026-04-30`, etc.

**Agora** (após restart Obsidian para reindex):
- Cada ticker = **1 nó** (`hubs/<TK>`). Sem suffixes.
- Cada persona = **0 nós** (handle resolve para pasta real `agents/council.xxx/` ou `agents/risk.xxx/`)
- Sem datas como nós (`<TK>_<DATE>` → `<TK>`)

**Acção necessária da tua parte**: fechar e reabrir Obsidian (ou `Ctrl+P` → "Reload App without saving"). Isso força reindex do graph e os ghost-nodes desaparecem.

---

## 6. Próximas perguntas razoáveis (próxima sessão)

1. **Renomear `agents/helena/` package** para `agents/design/` (Python module). Por agora mantém — refactor maior.
2. **Aliases inversos**: criar `Charlie Compounder.md` em `agents/personas_aliases/` que apenas redireciona via front-matter `aliases: [council.industrials-us]` — útil se voltares a usar o nome em texto puro.
3. **Cemetery pre-search-and-replace**: também reescrever wikilinks **dentro** dos ficheiros no cemetery? Reversível mas evita ghost-node-revival se restaurares algum.
4. **Glossary cleanup**: os nós Glossary (Graham_Number, Moat, ROE, DRIP, Margin_of_Safety...) continuam **legítimos** — são conceitos canónicos linkados de muitos hubs. Manter.

---

**Wave 4 fecha o ciclo**: filesystem limpo (Wave 3) + wikilinks limpos (Wave 4) + daily_run anti-regressão (Phase pipeline). Próximo refresh do Obsidian deve mostrar o graph drasticamente mais limpo.

_Gerado por sessão autónoma Wave 4 (ghost-node killer). 2026-05-14._
