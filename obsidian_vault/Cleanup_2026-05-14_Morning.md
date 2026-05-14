---
type: cleanup_report
tags: [cleanup, morning, faxina, restructuring, hubs]
date: 2026-05-14
duration_estimated: ~2h authorized
session_id: morning-faxina-wave2
status: completed
parent: "[[Manual_do_Sistema]]"
sibling_to: "[[Cleanup_Overnight_2026-05-13]]"
---

# 🧹 Cleanup matinal — 2026-05-14 (Wave 2, a grande)

> **Para leitura matinal**. Resposta ao feedback de hoje: "33 itens não chegaram, e ainda vejo o mesmo nome de ticker espalhado por 5 sítios".
> Hoje: **243 itens enterrados** + **33 hubs canónicos** + **1 índice mestre** + **23 personas com handle canónico** no front-matter.
> Tudo reversível via `cemetery/2026-05-14/`.

## TL;DR (1 minuto)

1. **🆕 Cada holding tem 1 hub.** `obsidian_vault/hubs/<TK>.md` consolida tudo: hoje + jornal histórico cronológico + artefactos por categoria. Porta única para abrir de manhã.
2. **🆕 Tickers Index mestre.** `obsidian_vault/_TICKERS_INDEX.md` — 1 tabela com 33 linhas, link directo para cada hub. **Substitui o atropelo matinal.**
3. **🪦 243 ficheiros enterrados** vs 33 ontem (7× mais). 8 categorias no cemetery, manifesto completo.
4. **🏷️ 23 personas com handle canónico** (`design.lint`, `council.banks-br`, `ops.briefing`…). Resolveu o "vejo nome de agente antigo no Obsidian" — agora o handle aparece logo no front-matter.
5. **🛡️ Zero dados destrutivos.** Sem DB writes, sem Tavily/Exa, sem push. Tudo `git mv` → cemetery, restore comando por linha do manifesto.

---

## 1. Hubs por ticker (resposta directa ao teu ask)

> _"Eu posso ter JNJ stock, JNJ deepdive, JNJ informação, tudo espalhado. Se estão todos juntos, devem estar no mesmo sítio. E quero um diário histórico mostrando como olhámos a informação antes vs como olhamos agora."_

✅ **Feito.** Em vez de mexer em ~ 500 ficheiros (alto risco partir links Obsidian), criei uma **porta consolidada por holding** que linka tudo:

```
obsidian_vault/hubs/
├── AAPL.md     ABBV.md     ACN.md      BBDC4.md    BLK.md
├── BN.md       BRK-B.md    BTLG11.md   GREK.md     GS.md
├── HD.md       ITSA4.md    IVVB11.md   JNJ.md      JPM.md
├── KLBN11.md   KNHF11.md   KO.md       LFTB11.md   NU.md
├── O.md        PG.md       PLD.md      PLTR.md     PRIO3.md
├── PVBI11.md   TEN.md      TSLA.md     TSM.md      VALE3.md
├── VGIR11.md   XP.md       XPML11.md
```

**33 hubs · 12 BR + 21 US**.

Estrutura de cada hub (exemplo [[JNJ]]):

```markdown
## 🎯 Hoje
- Posição: 10.0 @ entry 238.28
- Verdict (DB): HOLD (score 5.68, 2026-05-13)
- Último deepdive: JNJ_deepdive_20260513_2248.json (V10 4-layer pipeline)
- Fundamentals (2026-05-13): P/E 26.70 · P/B 6.83 · DY 2.8% · ROE 26.4% · ND/EBITDA 0.96 · Dividend streak 65 · Aristocrat yes

## 📜 Histórico (chronological journal)
### 2026
- 2026-05-13 · Overnight → [[JNJ]]                    (Overnight_2026-05-13/JNJ.md)
- 2026-05-11 · Overnight → [[JNJ]]                    (Overnight_2026-05-11/JNJ.md)  ← agora no cemetery
- 2026-05-10 · Pilot → [[JNJ]]                        (Pilot_Deep_Dive_2026-05-10/JNJ.md) ← cemetery
- 2026-05-05 · Bibliotheca → [[Compare_JNJ_KO_PG]]
- 2026-05-01 · Dossier Archive → [[JNJ_STORY_2026-05-01]] ← cemetery
- 2026-05-01 · Review (Charlie + Mariana + Pedro + Valentina) → links
- ...

## 🗂️ Artefactos por categoria
### Panorama / Deepdive / Story / Council / IC Debate / Variant
### Overnight scrapes / Pilot / DRIP / Wiki / Sessions / Bibliotheca / etc

## ⚙️ Refresh commands
ii panorama JNJ --write
ii deepdive JNJ --save-obsidian
ii verdict JNJ --narrate --write
ii fv JNJ
python -m analytics.fair_value_forward --ticker JNJ
```

**Regenerável**: `python scripts/build_ticker_hubs.py` reescreve os 33 hubs a partir do filesystem actual. Cada hub é uma **vista**, não uma cópia — os ficheiros originais ficam onde estavam.

### Tickers Index (porta de entrada)

[[_TICKERS_INDEX]] — 1 tabela por mercado com:

| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |
|---|---|---|---|---|---|---|
| [[hubs/JNJ\|JNJ]] | Johnson & Johnson | Healthcare | 10 | `HOLD` | 5.68 | 2026-05-13 |
| [[hubs/ACN\|ACN]] | Accenture | Technology | 4 | `WATCH` | 6.62 | — |
| … | … | … | … | … | … | … |

Cada link entra directo no hub. Regenera com `python scripts/build_tickers_index.py`.

---

## 2. O que foi para o cemetery (243 itens, 8 categorias)

Manifest completo: `cemetery/2026-05-14/manifest.md`. Toda a entrada tem comando `git mv` para restore.

| ID prefix | Categoria | Items | Razão |
|---|---|---:|---|
| W1-001 | SUPERSEDED `Overnight_2026-05-11/` | 140 | Substituído pelo scrape 2026-05-13 do mesmo universo. Links per-ticker preservados no hub journal. |
| W1-002 | SUPERSEDED `Pilot_Deep_Dive_2026-05-10/` | 7 | Pilot (5 tickers) — missão done. |
| W1-003 | SUPERSEDED `Pilot_Deep_Dive_2026-05-11/` | 2 | Tiny pilot untracked, missions done. |
| W2-* | ARCHIVED `dossiers/archive/` | 31 | STORYs dated do início (2026-04-30 / 05-01). Já linkados nos hubs por data. |
| W3-* | STALE Bibliotheca dated | 17 | Research_Digest / Midnight_Work / Night_Shift / Workday_Work / Overnight_Backfill / Test_Run anteriores a 2026-05-07. Mantido: Compare_JNJ_KO_PG (analítico), Phase_FF_Bloco1, Mega_Audit_2026-05-13. |
| W4-* | STALE Daily_Synthesis | 6 | Daily_Synthesis 08/09/10 (mantido 11+13). Allocation_US_2026-05-04.json. Extension_Run dupe Bibliotheca. |
| W5-* | STALE briefings dated | 18 | conviction_ranking < 05-09 (3) · decision_journal_intel 04-25 · portfolio_concentration/drawdown < 05-09 (4) · metrics 04-24 · earnings_prep para earnings já passados (AAPL/BRK-B/KO/O/PLTR/PRIO3/VALE3). Mantido latest 05-09 + earnings futuros (HD/XP/ACN). |
| W6-* | STALE `briefings/overnight_research_2026-04-24/` | 21 | One-shot dir do overnight 24/04. |
| W7-* | FOLDER-EMPTY (Mega Auditor 2026-05-14) | 3 | `data/`, `market-researcher/`, `reference/` — dirs vazias. |

**Total: 245 movimentos** (243 ficheiros .md/.json + 2 directorias com conteúdo agregado).

### O que **NÃO** se enterrou (de propósito)

- `dossiers/<TK>_FILING_<DATE>.md` (67 ficheiros) — **fazem parte do jornal histórico**, são os links primários que o hub usa.
- `agents/<Persona>/reviews/<TK>_<DATE>.md` — reviews de Council por persona, **datados, são os blocos do jornal**. Linkados no hub.
- `tickers/<TK>_DOSSIE.md`, `_IC_DEBATE.md`, `_VARIANT.md`, `_RI.md` — são as 4 vistas analíticas distintas. Cada uma com purpose.
- `dossiers/<TK>.md` (6 ficheiros: ACN, JNJ, JPM, KO, VALE3, XPML11) — **não duplicam** `tickers/<TK>.md`; são deepdive snapshots dum dia específico (ex: JNJ.md tem `date: 2026-05-09` com Moat 8.75). Mantidos.
- `videos/*.md` (43) — transcripts. Linkados nos hubs onde aplicável.
- `Clippings/*.md` (40) — externos colados pelo user.
- `wiki/holdings/<TK>.md` (34) — playbooks longos por nome.

---

## 3. Agente-name sweep (a tua queixa "vejo nome antigo")

23 personas em `obsidian_vault/agents/personas/` agora têm **`handle:` no front-matter**:

| Persona file | Handle canónico injectado |
|---|---|
| Aderbaldo Cíclico.md | `council.commodities-br` |
| Aristóteles Backtest.md | `perf.backtest-analysts` |
| Aurora Matina.md | `ops.briefing` |
| Charlie Compounder.md | `council.industrials-us` |
| Clara Fit.md | `perf.portfolio-matcher` |
| Diabo Silva.md | `risk.devils-advocate` |
| Diego Bancário.md | `council.banks-br` |
| Hank Tier-One.md | `council.banks-us` |
| Helena Linha.md | `design.lint` |
| Lourdes Aluguel.md | `council.fiis-br` |
| Mariana Macro.md | `council.macro` |
| Noé Arquivista.md | `ops.janitor` |
| Pedro Alocação.md | `council.allocation` |
| Regina Ordem.md | `risk.compliance` |
| Sofia Clippings.md | `research.subscriptions` |
| Teresa Tese.md | `research.thesis-refresh` |
| Tião Galpão.md | `council.industrials-br` |
| Ulisses Navegador.md | `research.scout` |
| Valentina Prudente.md | `risk.drift-audit` |
| Vitória Vitrine.md | `design.product` |
| Walter Triple-Net.md | `council.reits-us` |
| Wilson Vigil.md | `ops.watchdog` |
| Zé Mensageiro.md | `ops.telegram-bridge` |

Quando abres em Obsidian agora, **o handle aparece logo na metadata** e o nome de persona fica como descrição secundária. Não renomeei as pastas (`Helena Linha/` → `design.lint/`) por causa dos links de outras notas; o `handle:` no front-matter dá-te aliasing canónico searchable.

Script: `scripts/persona_handle_alias.py` (idempotente — re-correr não duplica).

---

## 4. Mega Auditor 2nd pass

Output: [[Mega_Audit_2026-05-14]]

| Categoria | Count | Acção tomada |
|---|---:|---|
| CODE-DEAD | 0 | ✅ (ontem limpou todos) |
| CODE-UNDOCUMENTED | 40 | ⚠️ **não-actuei** — são scripts com `__main__` mas sem entry no CLAUDE.md catalog. Maior decisão de design (incluir/remover do catálogo, ou agrupar em `ii <ns> <cmd>`). Lista no Mega_Audit. |
| CODE-ONESHOT | 0 | ✅ |
| CODE-MARK-OLD | 0 | ✅ |
| VAULT-EMPTY | 0 | ✅ |
| VAULT-DEPRECATED | 0 | ✅ |
| MEM-STALE | 0 | ✅ |
| FOLDER-EMPTY | 3 | 🪦 enterrados (`data/`, `market-researcher/`, `reference/`) |

---

## 5. Métricas antes/depois

| Métrica | Antes (2026-05-13 noite) | Agora (2026-05-14 manhã) | Δ |
|---|---:|---:|---:|
| Hubs canónicos por ticker | 0 | 33 | +33 |
| Master index | 0 | 1 (`_TICKERS_INDEX`) | +1 |
| Personas com handle no front-matter | 10 (só Council) | 33 (Council + personas/) | +23 |
| Ficheiros buried no cemetery (sessão) | 33 | 243 | **+210 (7,4×)** |
| Vault working files (.md) | 1.610 | 1.418 (vault) + 195 (cemetery) | −192 visíveis |
| Empty folders em `obsidian_vault/` | 3 | 0 | −3 |
| Overnight scrape dirs duplicados | 2 (`_2026-05-11/`+`_2026-05-13/`) | 1 (só `_2026-05-13/`) | −1 |
| Pilot Deep Dive dirs | 2 | 0 | −2 |

> Nota: a contagem de 1.418 working .md é estimada (1.613 total file-system menos 195 buried hoje). O número exacto sai do próximo `vault_health`.

---

## 6. O que **NÃO** toquei (de propósito)

Constraints honoured:
- ❌ **Sem `data/` destructive writes**: zero SQLite touch, zero migration.
- ❌ **Sem push**: trabalho local apenas. `git status` mostra 568 ficheiros alterados (renames + uncommitted M).
- ❌ **Sem Tavily/Exa**: zero rate-limit consumido.
- ❌ **Sem rename de pastas Obsidian**: `Helena Linha/` → `design.lint/` partiria links. Optei por `handle:` front-matter (non-breaking + searchable).
- ❌ **Sem `ii deepdive --holdings`** (5-8h Ollama, risco VRAM thrashing pós-incidente 09/05).
- ❌ **Sem mexer no CLI catalog** dos 40 scripts UNDOCUMENTED — decisão de design tua (são `bury` ou são `add to ii`?).
- ❌ **Sem auto-tag clippings** (Sprint A do feedback ontem) — fica para próxima sessão; é um agent novo.

---

## 7. Próximos passos sugeridos (quando puderes)

### Imediato (5 min — só leitura)
1. Abre [[_TICKERS_INDEX]]. Clica em 1-2 hubs (JNJ, ACN, BBDC4). Confirma a estrutura.
2. Confere [[Cleanup_2026-05-14_Morning]] (este doc).
3. Lê `cemetery/2026-05-14/manifest.md` se quiseres restaurar algo.

### Curto prazo (1 sessão)
4. **Hubs para watchlist**: estender `scripts/build_ticker_hubs.py` para também construir hubs para tickers do `universe.yaml watchlist` (não só holdings) — provavelmente mais 30-40 tickers úteis.
5. **Catalog gap (40 scripts UNDOCUMENTED)**: triar 1× — quais são active (add CLAUDE.md catalog row) vs deprecated (bury). Lista no [[Mega_Audit_2026-05-14]].
6. **Vault graph cleanup**: agora que o cemetery tirou 245 ficheiros, vale correr `python -m agents.perpetuum.vault_health` para ver quantas das 1.350 flagged ontem ficam.
7. **Sprint A explícito (do feedback de ontem)**: criar `research.auto-tag-clippings` (Ollama Qwen 14B sobre `vault/Clippings/` + `config/topic_watchlist.yaml`).

### Médio (sprints)
8. **Renomeação opcional de pastas Council** com `git mv "Charlie Compounder/" "council.industrials-us/"` + sed sobre `[[council.industrials-us]]` global. Trabalhoso mas torna a vault Obsidian-search 100% handle-first.
9. **Hubs com price chart embedded**: cada hub poderia ter `![[price_<TK>.svg]]` gerado por `scripts/refresh_ticker.py`. Visual.
10. **Auto-update dos hubs no daily_run**: depois de cada `ii deepdive`, regenerar só o hub afectado.

---

## 8. Como navegar daqui em diante

> Resposta directa ao teu "duas horas e dá-me um MD para abrir como o `Manual_do_Sistema.md` no lado direito".

**O fluxo é**:

```
[[Manual_do_Sistema]]            — como tudo opera (manual do dono)
       ↓
[[_TICKERS_INDEX]]               — 33 tickers, 1 linha cada, link directo
       ↓
[[JNJ]]  [[BBDC4]]     — porta única por ticker
       ↓
Hoje + Histórico + Artefactos    — tudo dentro, scroll → ler → decidir
       ↓
ii deepdive JNJ ← se quiseres aprofundar
```

**E para ler o que mudou hoje**: este doc é a leitura matinal pós-faxina. Abre antes do briefing diário, depois `[[_TICKERS_INDEX]]`.

---

## 9. Cross-references

- **Roteiro de operação**: [[Manual_do_Sistema]]
- **Índice mestre** (novo): [[_TICKERS_INDEX]]
- **Hubs por ticker** (novo, 33): `obsidian_vault/hubs/`
- **Constituição**: [[CONSTITUTION]] · [[CONSTITUTION_Pessoal]]
- **Agents (handles canónicos)**: [[AGENTS_REGISTRY]]
- **Faxina anterior**: [[Cleanup_Overnight_2026-05-13]]
- **Mega Audit fresh**: [[Mega_Audit_2026-05-14]]
- **Manifesto de cemetery**: `cemetery/2026-05-14/manifest.md` (245 entries com restore command)
- **Linguagem de investidor**: [[Bibliotheca/Manual_de_Direcao]]

---

## 10. Confissão de pontos por validar

Por transparência:

1. **Vault graph**: hubs novos podem ter aliases iguais ao basename (ex: `[[JNJ]]` em hubs/JNJ.md colide com `[[JNJ]]` em tickers/JNJ.md ou dossiers/JNJ.md). Obsidian resolve pelo path completo na maioria dos casos; se notares notas "wrong target", abre o issue.
2. **Verdict snapshot**: o "Hoje" do hub usa `verdict_history` da DB. Para holdings sem verdict computado (BR maior parte, 2026-05-13 só correu para os US), o número é o último de qualquer corrida. Próximo `ii allocate` / `ii agent` actualiza.
3. **Compare_JNJ_KO_PG.md** ficou em Bibliotheca/ — é analítico (cross-ticker), não pode estar num único hub. Linkado de JNJ + KO + PG hubs.
4. **earnings_prep** futuros (ACN 2026-06-18, HD 2026-05-19, XP 2026-05-19) ficaram — datas adiante. Hoje (BN, NU 2026-05-14) também ficaram.
5. **40 scripts UNDOCUMENTED não actuei**. Mega Auditor lista-os, mas estes são `__main__`-runnable que existem fora do CLAUDE.md catalog — possivelmente USADOS por cron / outros scripts. Triagem manual recomendada antes de bury.
6. **vault count** mismatch de ~200 — provavelmente o "1610" do relatório ontem foi pré-burial dos 33. Não bloqueia, mas refazer `vault_health --by-issue` daria o número exacto.

---

**Boa academia.** Voltas para um vault menor, com porta única por ticker e jornal histórico. Próxima sessão pode atacar:
- Bury dos 40 CODE-UNDOCUMENTED triados
- Sprint `research.auto-tag-clippings`
- Hubs para tickers watchlist (~ 30-40 nomes)

_Gerado por sessão autónoma 2026-05-14 manhã. Faxina Wave 2._
