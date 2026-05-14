---
type: cleanup_report
tags: [cleanup, deep_merge, faxina, restructuring, hubs]
date: 2026-05-14
session: deep-merge-wave-3
status: completed
parent: "[[Manual_do_Sistema]]"
sibling: "[[Cleanup_2026-05-14_Morning]]"
---

# 🧹🔥 Cleanup Wave 3 — Deep Merge (2026-05-14 tarde)

> Resposta à tua queixa: _"continuo a ver `_DOSSIE`, `_COUNCIL`, `_<DATE>` por todo o lado, e Charlie Compounder/Mariana Macro continuam visíveis. Não estás a apagar suficiente."_
>
> Resultado: **1.002 ficheiros per-ticker absorvidos** + **23 personas eliminadas** + **10 folders renomeadas para handles**. Total **1.291 itens no cemetery hoje**. Vault visível: **1.613 → 720 .md** (−893, −55%).

## TL;DR (1 minuto)

1. **🎯 1 ficheiro por ticker. 187 hubs, conteúdo absorvido inline.**
   `obsidian_vault/hubs/<TK>.md` agora contém o conteúdo absorvido de TODAS as fontes per-ticker (não só links). Cada hub: Hoje + Histórico embedded section-by-section + Refresh commands.
2. **🪦 1.002 ficheiros per-ticker enterrados.**
   `<TK>_DOSSIE`, `<TK>_STORY`, `<TK>_COUNCIL`, `<TK>_FILING_*`, `<TK>_IC_DEBATE`, `<TK>_VARIANT`, `<TK>_RI`, `<TK>_drip`, `<TK>_<DATE>` reviews, `Overnight_*/<TK>.md`, `wiki/holdings/<TK>.md`, `Sessions/<TK>_*.md` — tudo para o cemetery, conteúdo preservado nos hubs.
3. **🏷️ Personas eliminadas.**
   - 23 `.md` files em `agents/personas/` → cemetery.
   - 10 pastas `agents/<Persona>/` → renomeadas para `agents/<handle>/`:
     - `Charlie Compounder/` → `council.industrials-us/`
     - `Mariana Macro/` → `council.macro/`
     - `Walter Triple-Net/` → `council.reits-us/`
     - `Valentina Prudente/` → `risk.drift-audit/`
     - ... e mais 6.
4. **📋 Index expandido.** `_TICKERS_INDEX.md` agora cobre os 187 hubs em 6 secções (BR/US × holdings/watchlist/research_pool + Kings & Aristocrats US).
5. **🛡️ Reversível.** Tudo via `git mv` para `cemetery/2026-05-14/`. Manifesto completo no folder cemetery.

---

## 1. O modelo agora — uma porta por ticker

### Antes (o que viste nos screenshots)

```
JNJ_DOSSIE                    PG_DOSSIE          ACN_DOSSIE
JNJ_STORY        JNJ_IC_DEBATE   ACN_STORY    Charlie Compounder ←   nodes massivos
JNJ_COUNCIL      ACN_COUNCIL     PG_COUNCIL   Mariana Macro
JNJ_2026-05-01   ACN_2026-04-30  PG_2026-05-01 Valentina Prudente
JNJ_VARIANT      ACN_VARIANT     PG_VARIANT    Pedro Alocação
...
```

Cada ticker = 4-15 nós no graph. Personas = nós centrais com 30+ ligações cada.

### Agora

```
hubs/JNJ.md          ← 1 nó por ticker (conteúdo absorvido inline)
hubs/ACN.md
hubs/PG.md
agents/council.industrials-us/   ← handles, não pessoas
agents/council.macro/
agents/risk.drift-audit/
```

### Estrutura de cada hub

```markdown
---
type: ticker_hub
ticker: JNJ
market: us
sector: Healthcare
sources_merged: 14
bucket: holdings
---

# JNJ — Johnson & Johnson

## 🎯 Hoje
- Posição: 10.0 @ entry 238.28
- Verdict: HOLD (score 5.68, 2026-05-13)
- Último deepdive: JNJ_deepdive_20260513_2248.json
- Auditor: moat=8.75 STRONG · piotroski · altman · beneish
- Fundamentals (2026-05-13): P/E 26.70 · P/B 6.83 · DY 2.8% · ROE 26.4% · ND/EBITDA 0.96 · Dividend streak 65 · Aristocrat yes

## 📜 Histórico (conteúdo absorvido)

### 2026

#### 2026-05-13 · Overnight scrape
_source: `Overnight_2026-05-13/JNJ.md` (now in cemetery)_

[CONTEÚDO REAL DO OVERNIGHT EMBEDDED AQUI, headings demoted h1→h4]

#### 2026-05-05 · Bibliotheca cross-ref (Compare_JNJ_KO_PG)
[CONTEÚDO]

#### 2026-05-01 · Council review · council.industrials-us
[CONTEÚDO DA REVIEW]

#### 2026-05-01 · Council review · council.macro
[CONTEÚDO]

#### 2026-05-01 · Story
[STORY EMBEDDED]

### Filings históricos
#### (todos os FILING_*.md absorvidos)

## ⚙️ Refresh commands
ii panorama JNJ --write
ii deepdive JNJ --save-obsidian
...
```

**Tamanhos típicos**:
- Holdings com história rica (JNJ, ACN, BBDC4): 40-70 KB
- Watchlist tier 1-2: 15-25 KB
- Kings/Aristocrats sem coverage profunda: 8-10 KB

---

## 2. Burials de hoje (1.291 itens, 18 categorias)

| Categoria | Items | Razão |
|---|---:|---|
| **ABSORBED-tickers** | 494 | `tickers/<TK>*.md` (panorama, _DOSSIE, _IC_DEBATE, _VARIANT, _RI) — conteúdo nos hubs |
| **ABSORBED-overnight-per-ticker** | 182 | `Overnight_2026-05-13/<TK>.md` — absorvido |
| **ABSORBED-dossiers** | 136 | `dossiers/<TK>_STORY/_COUNCIL/_FILING_*` — absorvido |
| **ABSORBED-council-reviews** | 125 | `agents/<Persona>/reviews/<TK>_<DATE>.md` — absorvido por persona-handle |
| **ABSORBED-drip** | 32 | `briefings/drip_scenarios/<TK>_drip.md` — absorvido |
| **ABSORBED-wiki-holdings** | 32 | `wiki/holdings/<TK>.md` — absorvido (playbook nos hubs) |
| **PURGED-personas** | 23 | `agents/personas/*.md` — descrições eliminadas (handle é tudo) |
| **ABSORBED-council-reviews-stragglers** | 4 | BRK-B reviews (hyphen matched 2nd pass) |
| **ABSORBED-sessions-per-ticker** | 1 | `Sessions/JNJ_Deepdive_Comparison.md` |
| ↓ (já do morning cleanup) | ↓ | ↓ |
| SUPERSEDED Overnight_2026-05-11 | 140 | morning cleanup |
| ARCHIVED dossiers/archive | 31 | morning |
| STALE briefings/overnight_research | 21 | morning |
| STALE briefings dated | 18 | morning |
| STALE Bibliotheca dated | 17 | morning |
| SUPERSEDED Pilot_2026-05-10 + 11 | 9 | morning |
| STALE Daily_Synthesis | 6 | morning |
| FOLDER-EMPTY (mega_auditor) | 3 | morning |
| **TOTAL hoje** | **1.291** | |

### Folders renomeadas (10 personas → handles)

| Old folder | New folder (canonical handle) |
|---|---|
| `agents/Aderbaldo Cíclico/` | `agents/council.commodities-br/` |
| `agents/Charlie Compounder/` | `agents/council.industrials-us/` |
| `agents/Diego Bancário/` | `agents/council.banks-br/` |
| `agents/Hank Tier-One/` | `agents/council.banks-us/` |
| `agents/Lourdes Aluguel/` | `agents/council.fiis-br/` |
| `agents/Mariana Macro/` | `agents/council.macro/` |
| `agents/Pedro Alocação/` | `agents/council.allocation/` |
| `agents/Tião Galpão/` | `agents/council.industrials-br/` |
| `agents/Valentina Prudente/` | `agents/risk.drift-audit/` |
| `agents/Walter Triple-Net/` | `agents/council.reits-us/` |

---

## 3. Métricas antes/depois

| Métrica | Morning (após Wave 2) | Deep Merge (após Wave 3) | Δ |
|---|---:|---:|---:|
| `.md` no vault (visíveis) | ~1.418 | **720** | **−698 (−49%)** |
| `.md` no cemetery (acumulado hoje) | 243 | 1.291 | +1.048 |
| Hubs por ticker | 33 (holdings only) | **187** (universo completo) | +154 |
| Hubs com conteúdo absorvido inline | 0 (linking model) | **187** | +187 |
| Personas .md visíveis | 23 | **0** | −23 |
| Pastas com nome de persona | 10 | **0** | −10 |
| Folders `agents/` com handle canónico | 0 | **10** | +10 |

### Vault em 1614 → 720 .md
Detalhe da redução:
- `tickers/`: 507 → 1 (`_LAYER.md` only)
- `dossiers/`: 170 → 0 (subfolder vazio agora)
- `agents/personas/`: 23 → 0 (folder removed)
- `Overnight_2026-05-13/`: 186 → 4 (só hubs `_MASTER`, `_LEITURA_DA_MANHA`)
- `briefings/drip_scenarios/`: 33 → 1 (`_Index.md`)
- `wiki/holdings/`: 34 → 1 (`_README.md`)
- `agents/<Persona>/reviews/`: 125 → 0

Sobreviventes:
- `hubs/` (NOVO): 187 .md
- `Glossary/`: 30 — métricas (Graham_Number, Moat, ROE, etc.) **keep, cross-ticker**
- `agents/<handle>/`: 10 pastas com `_reviews_index.md` cada
- `Bibliotheca/`, `Clippings/`, `videos/`: cross-ref / external (não tocadas)
- `wiki/sectors/`, `wiki/methods/`, `wiki/macro/`, `wiki/playbooks/`, `wiki/tax/`, `wiki/cycles/`, `wiki/history/`: non-ticker knowledge **keep**
- `Sessions/`: 6 files non-ticker (audits, overhauls)
- `Comercial/`, `dashboards/`, `skills/`, `specs/`, `workspace/`: out of scope

---

## 4. Como mudou o graph view

**Antes**: nodes massivos `Charlie Compounder` / `Mariana Macro` / `Valentina Prudente` no centro, conectados a 30-50 reviews per ticker dated. Tickers com 4-15 _DOSSIE/_STORY/_COUNCIL/_VARIANT satellite nodes.

**Agora**: cada ticker = **1 node** (`hubs/JNJ`). Glossary terms (Graham_Number, Moat, ROE) ficam como nodes legítimos centrais — esses **devem ficar**, são os conceitos canónicos. Personas desaparecem.

---

## 5. O que se passa quando abres Obsidian agora

1. **Graph view**: deve ficar muito mais limpo. 187 ticker nodes (1 por ticker) + Glossary central + Bibliotheca + Sessions + Comercial. Sem `_DOSSIE`/`_STORY`/`_COUNCIL`/`_<DATE>`/`Charlie Compounder`/etc.
2. **Sidebar files**: pasta `tickers/` praticamente vazia (só `_LAYER.md`). `dossiers/` vazio. `agents/personas/` foi-se.
3. **Search**: pesquisar `[[JNJ]]` resolve para `hubs/JNJ.md` (porta única). Pesquisar `council.industrials-us` encontra a pasta.
4. **Backlinks**: links externos para `JNJ_DOSSIE` etc. ficam quebrados; ao clicar, Obsidian sugere `JNJ` (que é o hub) — bom o suficiente, ou pode resolver-se com vault search-and-replace.

---

## 6. Constraints honoured

- ❌ **Sem `data/` writes**: zero SQLite touch.
- ❌ **Sem push**: tudo local.
- ❌ **Sem Tavily/Exa**: zero rate-limit.
- ✅ **Reversível**: cada move é `git mv`. Cemetery preserva o original. Restore command pattern: `git mv cemetery/2026-05-14/<SUBDIR>/<PATH> <ORIGINAL_PATH>`.

---

## 7. Trade-offs explícitos (transparência)

### O que ficou mais difícil
1. **Hubs longos** — alguns hubs (TEN, VALE3, TSM, XPML11) têm 60-100 KB. Scrollable em Obsidian, mas grande para leitura linear. Mitigação: cada secção começa com `#### <date> · <type>` então TOC vertical funciona.
2. **Links partidos**: notas Bibliotheca/Clippings que apontavam para `[[JNJ]]` agora não resolvem. Obsidian sugere `[[JNJ]]` (o hub) — mostly OK mas é fricção visual.
3. **Council reviews só por handle**: `council.industrials-us/reviews/` ficou vazio (todos os reviews foram absorvidos). Pasta sobrevive com `_reviews_index.md`. Quando o Council correr novamente, escreve aí.

### O que melhorou objectivamente
1. **1 ficheiro por ticker** = leitura linear matinal.
2. **Histórico contínuo embedded** = "antes vs agora" visível no mesmo scroll.
3. **Personas eliminadas** = handles canónicos consistentes.
4. **Graph 4x mais limpo** (estimativa: era ~1500 ticker-related nodes, agora ~187).

---

## 8. Próximos passos (para a tua decisão)

### Imediato (2 min)
1. Abre [[_TICKERS_INDEX]] e clica em 2-3 hubs (JNJ, ACN, ITSA4). Confirma que está tudo lá.
2. Verifica o graph view do Obsidian (deve estar drasticamente reduzido).
3. Lê `cemetery/2026-05-14/manifest.md` (~1.300 entries) se quiseres restaurar algo.

### Pendente
1. **Rebuild Mission Control**: se o MC frontend lia `tickers/*.md` directamente, precisa apontar para `hubs/<TK>.md` agora.
2. **`ii deepdive` output path**: ainda escreve `reports/deepdive/<TK>_*.json` e `obsidian_vault/dossiers/<TK>.md`? Se sim, próximo deepdive ressuscita conteúdo no `dossiers/`. Solução: mudar `--save-obsidian` para escrever `hubs/<TK>.md` (append section).
3. **Daily run hook**: o `daily_run.bat` faz `python scripts/build_merged_hubs.py` no fim para refrescar? Sugiro adicionar.
4. **Obsidian search-and-replace** `[[JNJ]]` → `[[JNJ]]` global? Posso fazer numa próxima sessão.

### Stragglers conhecidos
- SPY, VOO, BOVA11, BTLG12, MCRF11 — buried mas sem hub (não estavam no universe.yaml). Conteúdo recuperável do cemetery. Se quiseres, adiciono ao universe e crio hubs.

---

## 9. Cross-references

- **Manual operacional**: [[Manual_do_Sistema]]
- **Índice mestre** (refresh): [[_TICKERS_INDEX]] (187 hubs)
- **Hubs por ticker**: `obsidian_vault/hubs/<TK>.md`
- **Cleanup anterior (Wave 2)**: [[Cleanup_2026-05-14_Morning]]
- **Cleanup ontem (Wave 1)**: [[Cleanup_Overnight_2026-05-13]]
- **AGENTS_REGISTRY (handles)**: [[AGENTS_REGISTRY]]
- **Cemetery**: `cemetery/2026-05-14/manifest.md`

---

## 10. Scripts adicionados

| Script | Propósito |
|---|---|
| `scripts/build_merged_hubs.py` | Builder dos 187 hubs com absorção inline de conteúdo. Idempotente. |
| `scripts/bury_per_ticker_sources.py` | Move 1002 ficheiros per-ticker source para cemetery. Idempotente. |
| `scripts/persona_purge.py` | Bury das 23 personas .md + rename de 10 folders → handles. |
| `scripts/build_tickers_index.py` (refresh) | Master index com todos os 187 hubs em 6 secções. |

Todos commitados nesta sessão.

---

**Próximo turno**: tu abres Obsidian, vês o graph limpo, navegas o `_TICKERS_INDEX` e dizes:
- "Falta isto" → restauro do cemetery
- "Está OK, ataca X" → próxima fase
- "Há um link partido em Y" → search-and-replace

_Gerado por sessão autónoma Wave 3 (deep merge). 2026-05-14._
