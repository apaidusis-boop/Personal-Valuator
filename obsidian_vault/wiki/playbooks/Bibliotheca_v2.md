---
type: playbook
name: Bibliotheca v2 — clippings RAG + glossary tutor + research digest + perpetuum
tags: [playbook, bibliotheca, clippings, rag, glossary]
related: ["[[Library_Pipeline]]", "[[Perpetuum_Engine]]", "[[Token_discipline]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 📚 Bibliotheca v2 — arquitectura

> Hub vault: [[Bibliotheca/_Index]] (catálogo + stats actualizados). Este playbook documenta **como as peças encaixam**, para futuro Claude não ter de re-tracejar o pipeline.

## Princípio

Tudo que entra no sistema vindo de fora — clippings web, livros, papers, glossário, research diário — vive sob `obsidian_vault/Bibliotheca/` (vault humano) e/ou `library/chunks_index.db` (RAG embedded localmente). Ollama `nomic-embed-text` faz os embeddings, Qwen 2.5 14B faz a síntese RAG. **Zero tokens Claude** — cumpre [[Token_discipline]] (REGRA #1).

## 5 componentes (e como interlocam)

```
                    ┌─────────────────────────────────┐
       Clippings ──►│ 1. clippings_ingest.py          │── chunks ──┐
                    └─────────────────────────────────┘            │
                                                                    ▼
                    ┌─────────────────────────────────┐    ┌──────────────────┐
       Books ──────►│   library/ingest.py             │───►│ chunks_index.db  │
                    └─────────────────────────────────┘    │ (Ollama 768-dim) │
                                                            └──────────────────┘
                                                                    │
       ┌─ build_glossary.py ──► Glossary/ (29 entries) ──┐          │
       │                                                  │          │
       │  ┌── dossier_tutor.py ──► injecta `## Tutor` ────┤          │
       │  │   em 72 dossiers tickers/*.md                 │          │
       │  │                                               │          │
       └──┴── build_knowledge_cards.py ──► Knowledge/ ────┤          │
          (12 cards Ollama-synthed via RAG)               │          │
                                                          ▼          ▼
       ┌─ scripts/research_digest.py ──► Bibliotheca/Research_Digest_<DATE>.md
       │  (Daily Digest — clippings novos + Tavily + perpetuum + gaps + alerts)
       │
       └─ agents/perpetuum/bibliotheca.py (12º perpetuum, T1)
          BIB001-004 → bibliotheca_autofix.py + sector_taxonomy.py
```

### 1. Clippings RAG

**O que**: vault `obsidian_vault/Clippings/*.md` → chunks → embedded localmente (Ollama nomic-embed). Estado actual (verificado 2026-04-28): **31 sources clippings → 303 chunks**; total geral em `library/chunks_index.db` é **2,007 chunks** (4 books + 31 clippings). Tabela única `chunk_index` (cols: `book_slug`, `chunk_file`, `text`, `embedding`, `n_tokens`); clippings têm `book_slug` com prefix `clip_*`.

**Pipeline** (`library/clippings_ingest.py`):
1. Lê cada `.md` em `obsidian_vault/Clippings/` (skip files que começam por `_`).
2. Parse frontmatter (title/source/author/published/tags).
3. Strip markdown image refs + whitespace.
4. Chunk via `library._common.chunk_text` (CHUNK_SIZE=2000, OVERLAP=200).
5. Slug = `clip_<slugify(stem)>` — namespace separado dos books (`book_slug LIKE 'clip_%'`).
6. Idempotente: `meta.json` por clip; skip se `file_hash` inalterado.
7. `--rag-build` → embed chunks novos via `library.rag.embed()` → SQLite BLOB em `chunk_index`.

**Storage**:
- Chunks raw text: `library/chunks/clip_<slug>/*.txt`
- Embeddings: `library/chunks_index.db` (table `chunk_index`, BLOB column 768f)
- Metadata: `library/chunks/clip_<slug>/meta.json`

**Query**: `python -m library.rag query "texto" --k 5` (semantic search) ou `python -m library.rag ask "pergunta PT" --k 6` (RAG + Qwen 14B synth, cita `[book:chunk]`).

### 2. Glossary tutor injector

**O que**: 29 entradas em `obsidian_vault/Glossary/` (PE, PB, DY, ROE, EBITDA, EPS, FCF, BVPS, NAV, NPL, CET1, Basel_Ratio, Cap_Rate, Coverage_Ratio, DCF, DRIP, Dividend_Streak, Aristocrat, Beta, CDI, IPCA, Selic, Graham_Number, Margin_of_Safety, Moat, Net_Debt_EBITDA, Payout_Ratio, Total_Shareholder_Yield, WACC ❓ verify completeness vs dir listing). Cada entry tem **fórmula + leitura + thresholds (BR equity / BR banks / US / fii) + good_bad + contraméricas + sources (links a Clippings) + back-links**.

**Build**: `scripts/build_glossary.py` — `ENTRIES` dict é a fonte canónica. `--backlinks` adiciona secção "Usado em" (≈72 dossiers que referenciam a métrica).

**Tutor injector** (`scripts/dossier_tutor.py`):
- Lê cada `obsidian_vault/tickers/*_DOSSIE.md` (~72 dossiers).
- `_parse_fundamentals` — regex sobre o texto do dossier extrai PE/PB/DY/ROE/EPS/BVPS/streak/preço/YoY/Basel/CET1/NPL.
- `_parse_meta` — extrai market/sector/is_holding do frontmatter.
- `_build_tutor` — para cada métrica presente, gera bullet com:
  - Valor actual (`**P/E = 12.34**`)
  - Link a `[[Glossary/PE|porquê isto importa?]]` (deep-link Obsidian)
  - Verdict vs threshold do CLAUDE.md ajustado por mercado/sector (**bank vs equity vs FII vs US**).
  - Edge cases: DY > 15% → "frequentemente sinaliza distress".
- **Decisão de quando injectar uma entry**: não escolhe semanticamente — injecta **toda métrica que `_parse_fundamentals` apanhar** no dossier (presença literal). Se o dossier não tem `**ROE**: X%` no formato esperado, não há link a `[[Glossary/ROE]]`. Se tem, link aparece deterministicamente. Bank-specific (Basel/CET1/NPL) só aparece se `is_bank` (sector match `banks`/`bancos`).
- Idempotente: regex `_TUTOR_PATTERN` strip-and-replace da secção `## Tutor` existente. Insere antes de `## Riscos identificados` (ou `## N. Riscos`); fallback: antes de `---\n*Generated`.

**Cron** (per `_Index.md` "Pipeline daily"):
```
[GLOSSARY]   rebuild entries + index (idempotente)
[TUTOR]      re-inject ## Tutor section em todos os DOSSIE.md
```

### 3. Daily Research Digest

**O que**: `scripts/research_digest.py` corre como perpetuum diário e gera `obsidian_vault/Bibliotheca/Research_Digest_<DATE>.md` — vista única do que aconteceu nas últimas 24h.

**8 secções fixas**:
1. **Clippings novos** ingested (mtime ≥ cutoff)
2. **Tavily web searches** (perpetuum autoresearch + dossier wires; cache em `data/tavily_cache/`)
3. **Methods extraídos** (`library/methods/*.yaml` novos)
4. **Books processados** (`library/books/` mtime ≥ cutoff)
5. **Perpetuum runs hoje** (lê `perpetuum_run_log` em `br_investments.db`)
6. **Coverage gaps surfaced** (banks sem BACEN, holdings BR sem fundamentals, conviction stale > 7d)
7. **Bibliotheca alerts** (BIB001-004 do `perpetuum_health` table, score < 100, top 25)
8. **RAG ready-to-ask** (6 prompts curados para `ii vault` / `library.rag ask`)

**Idempotente**: re-run mesmo dia sobrescreve `Research_Digest_<DATE>.md`. `--days N` alarga janela; `--since YYYY-MM-DD` força data alvo.

### 4. 12 Knowledge Cards

Cards conceptuais sintetizados via RAG sobre books + clippings (Ollama Qwen, zero tokens Claude). Cada card é resposta durável a uma pergunta-chave de filosofia:

| Categoria | Card |
|---|---|
| **fii** | `fii_paper_vs_brick` — quando preferir cada |
| **income** | `aristocrat_quality_signal` — o que sustenta status 25y+ |
| **macro** | `dalio_bubble_framework` — 4 critérios para identificar bolha |
| **macro** | `dalio_debt_crisis_signals` — sinais precoces antes de crise dívida |
| **philosophy** | `buffett_moat_detection` — detectar vantagem sustentável |
| **philosophy** | `graham_margin_of_safety` — princípio fundamental |
| **process** | `variant_perception_edge` — onde divergimos do consenso com edge real |
| **process** | `value_trap_signals` — evitar comprar barato pelas razões erradas |
| **sector** | `bank_screening_checklist` — checklist antes de comprar banco |
| **strategy** | `drip_vs_cash_dividends` — quando cada faz sentido |
| **strategy** | `drip_compounding_math` — matemática real 10–20 anos |
| **valuation** | `dcf_practical_pitfalls` — quando faz sentido vs quando engana |

**Build**: `scripts/build_knowledge_cards.py` — `CARDS` list é fonte; skip-if-exists default; `--force` regenera (custo ≈30s × N via Ollama). Index: [[Bibliotheca/Knowledge/_Index]].

### 5. Bibliotheca Perpetuum (12º)

**O que**: `agents/perpetuum/bibliotheca.py` — pure SQL + YAML, **zero LLM**. Counterpart de `data_coverage` (que pontua HOLDINGS coverage); este audita o **catálogo inteiro** (`companies` table, holding ou não) por qualidade de bibliotecário.

**Subjects**: cada `(market, ticker)` em `data/br_investments.db` + `data/us_investments.db`.

**Signals (cada -25 pts; min score 0)**:

| Code | O que | Action hint |
|---|---|---|
| **BIB001 SECTOR_NULL** | `companies.sector IS NULL` | `python scripts/bibliotheca_autofix.py --apply` |
| **BIB002 SECTOR_NONCANONICAL** | sector não está em `CANONICAL_SECTORS` e não tem alias mapeado | extender `library/sector_taxonomy.py::SECTOR_ALIASES` ou corrigir em `universe.yaml` |
| **BIB003 NAME_GENERIC** | `name == ticker` (placeholder de auto-onboard) | adicionar real name em `config/universe.yaml`, depois `bibliotheca_autofix.py --apply` |
| **BIB004 ORPHAN** | em DB mas NÃO em `universe.yaml` E NÃO é holding | adicionar a watchlist OU `DELETE FROM companies WHERE ticker='X'` (triage humana) |

**Sector taxonomy** (`library/sector_taxonomy.py`):
- `CANONICAL_SECTORS` frozenset: 28 buckets (Banks, Financials, Insurance, Healthcare, Technology, Communication, Consumer Disc., Consumer Staples, Energy, Oil & Gas, Industrials, Materials, Mining, Utilities, Telecom, Real Estate, Holding, REIT, Shopping, Logística, Híbrido, Papel (CRI), Corporativo, ETF, ETF-RF, ETF-US…).
- `SECTOR_ALIASES` map case-insensitive (`"chemicals" → "Materials"`, `"financial services" → "Financials"`, mojibake `"h?brido" → "Híbrido"`, etc.).
- `normalize(raw)` → canonical bucket OR original (deixa Bibliotheca surface non-canonical para human review).

**Autofix** (`scripts/bibliotheca_autofix.py`):
- Fix 1: `SECTOR_NULL` → backfill from `universe.yaml` (com `normalize()`), só se canonical.
- Fix 2: alias non-canonical → canonical (mojibake repair incluído).
- Fix 3: `name == ticker` → real name from `universe.yaml`.
- `HARDCODED_FALLBACKS` minimal: `ABCB4 → Banco ABC Brasil/Banks`, `BPAC11 → BTG Pactual/Banks`. Tudo o resto **deve** ir para `universe.yaml`.
- Default dry-run; `--apply` executa writes. Idempotente — re-run não faz nada se já corrigido.

**Estado as of memory write 2026-04-26 (Phase DD)**:
- BR sectors NULL: **17 → 0**
- 35 fixes (sectors + names) aplicados
- 94 orphans surfaced para triage humana

T1 Observer; promove a T2 quando autofix está confiável em cron.

## Comandos

```bash
# Clippings RAG
python -m library.clippings_ingest                 # ingere novos
python -m library.clippings_ingest --rag-build     # ingest + embed
python -m library.clippings_ingest --list          # inventory + embed status
python -m library.rag query "margem de segurança" --k 5
python -m library.rag ask "como o Buffett define moat?" --k 6
python -m library.rag status                       # cobertura do índice

# Glossary + Tutor injector
python scripts/build_glossary.py --backlinks      # rebuild Glossary/ + who-uses
python scripts/dossier_tutor.py                   # re-inject ## Tutor em todos
python scripts/dossier_tutor.py --ticker ITSA4    # single-ticker

# Knowledge Cards
python scripts/build_knowledge_cards.py           # skip-if-exists
python scripts/build_knowledge_cards.py --force   # regenera tudo

# Daily Research Digest
python scripts/research_digest.py                 # hoje (1d window)
python scripts/research_digest.py --days 7        # window 7d
python scripts/research_digest.py --since 2026-04-26

# Bibliotheca Perpetuum + autofix
python -m agents.perpetuum.bibliotheca            # T1 audit (read-only)
python scripts/bibliotheca_autofix.py             # dry-run
python scripts/bibliotheca_autofix.py --apply     # executa writes
```

## Storage

| Asset | Path |
|---|---|
| Clippings vault | `obsidian_vault/Clippings/*.md` |
| Knowledge Cards | `obsidian_vault/Bibliotheca/Knowledge/*.md` (12 cards + `_Index.md`) |
| Glossary | `obsidian_vault/Glossary/*.md` (29 entries + `_Index.md`) |
| Daily Digests | `obsidian_vault/Bibliotheca/Research_Digest_<DATE>.md` |
| RAG chunks (raw) | `library/chunks/clip_*/*.txt` + `library/chunks/<book_slug>/*.txt` |
| RAG embeddings | `library/chunks_index.db` (`chunk_index` table, BLOB column) |
| Tavily cache | `data/tavily_cache/*.json` (TTL 7d) |
| Methods | `library/methods/*.yaml` |
| Books raw | `library/books/*.{pdf,epub}` |
| Hub | `obsidian_vault/Bibliotheca/_Index.md` |

## Pipeline daily (cron 23:30)

```
[CLIPPINGS-INGEST]  novos clippings → RAG (Ollama embed)
[GLOSSARY]          rebuild entries + index (idempotente)
[TUTOR]             re-inject ## Tutor section em todos os DOSSIE.md
[KNOWLEDGE-CARDS]   skip-if-exists; gera só novas perguntas
[RESEARCH-DIGEST]   gera Research_Digest_<DATE>.md
[BIBLIOTHECA-PERP]  audit catalog (BIB001-004)
```

Synthetic IC, variant_perception, earnings_prep correm manualmente / weekly (não no cron Bibliotheca).

## Limitações / open items

- **94 orphans** surfaced 2026-04-26 esperam triage humana (delete vs add to `universe.yaml`).
- Tutor injector é **regex-based** sobre o texto formatado do dossier — se um dossier muda formato (ex: `**ROE**:` vira `**Return on Equity**:`), métrica deixa de ser apanhada. ❓ verify se algum dossier diverge.
- Tutor não tenta semantic match de quando uma métrica importa — se está no dossier no formato esperado, link é injectado. Sectors onde uma métrica é irrelevante (ex: P/E para FII paper) ainda recebem bullet, com texto contextualizando "fora do screen".
- `_parse_fundamentals` para banks lê **última coluna** das tabelas Basel/CET1/NPL (assume formato peer-table com ticker alvo no final).
- `clippings_ingest` skip se `len(body) < 200` chars (filter ruído de Web Clipper meta-only docs).
- `build_knowledge_cards.py` é Ollama-based (Qwen 14B local); ≈30s/card. `--force` re-gera todos = custo significativo.
- RAG `library.rag.ask` usa `qwen2.5:14b-instruct-q4_K_M`; se Ollama down, devolve `(generation failed: …)`. Fallback: `query` (busca pura) sempre funciona offline contra DB local.
- Hardcoded fallbacks no autofix são **minimal por design** — extender `universe.yaml` é o caminho correcto.

## Workflow recomendado

1. **Antes** de pedir Claude para "explicar métrica X" → seguir link `[[Glossary/X]]` no dossier (já tem fórmula + contraméricas + sources). Zero tokens.
2. **Antes** de pedir "o que aconteceu hoje" → ler `Bibliotheca/Research_Digest_<TODAY>.md` (gerado às 23:30).
3. **Antes** de pedir Claude para "explicar conceito Buffett/Dalio/Graham" → tentar `python -m library.rag ask "pergunta PT"` (RAG local, cita chunks de books). Knowledge Cards são a versão durável das 12 perguntas mais frequentes.
4. **Antes** de adicionar nova métrica a dossiers → adicionar entry em `build_glossary.py::ENTRIES` PRIMEIRO; depois actualizar `dossier_tutor.py::_build_tutor` para parse + bullet.
5. **Antes** de criar novo sector ad-hoc → ver `library/sector_taxonomy.py::CANONICAL_SECTORS`. Adicionar a `SECTOR_ALIASES` se for variante; só estender `CANONICAL_SECTORS` se for bucket genuinamente novo.

## Ver também
- [[Library_Pipeline]] — books → chunks → methods (irmão tipográfico do Clippings RAG)
- [[Perpetuum_Engine]] — onde Bibliotheca é o 12º perpetuum
- [[Token_discipline]] — porque tudo é Ollama local
- [[Analysis_workflow]] — como Tutor entra na leitura de dossiers
- [[Bibliotheca/_Index]] — hub vivo (stats actualizados)
- [[CONSTITUTION]] — Phase DD ship notes
