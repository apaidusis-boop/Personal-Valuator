---
type: bibliotheca_index
date: 2026-04-26
tags: [bibliotheca, index]
---

# 📚 Bibliotheca — Índice

> Hub de tudo que entra no sistema vindo de fora: **clippings web, books, papers, métodos extraídos, research diário, glossário**. Tudo embedded localmente (Ollama nomic-embed) → searchable via `ii vault` ou `python -m library.rag`.

## Daily Research Digests

Cada dia gera um snapshot de actividade automático. Lê primeiro o de hoje:

- [[Bibliotheca/Research_Digest_2026-04-26]] — relatório mais recente
- _(digests mais antigos: ver `obsidian_vault/Bibliotheca/Research_Digest_*.md`)_

**Como gerar manualmente**: `python scripts/research_digest.py [--days N]`

## Catálogo de Conhecimento

### Clippings (24 documents, 245 chunks embedded)

Origens:
- **Investopedia** — definições, conceitos, frameworks (DRIP, P/E, value investing, moat, etc.)
- **Suno Research** — teses BR (AXIA6, SLCE3, WIZC3), Carteira Dividendos, MacroLab
- **Motley Fool** — premium reports (AI-proof, Bubble hedge, Hollywood revolution, Space race)
- **JPM/Chase** — markets overview, research portal
- **13F filings** — Berkshire Hathaway tracking

Browse: `obsidian_vault/Clippings/` directory

### Books (4 livros, 1704 chunks)

- Dalio: *Changing World Order*, *Big Debt Crises*, *Country Power Index*
- Damodaran: *Investment Valuation 3rd Edition*

Browse: `library/books/` (PDF originais), `library/chunks/` (text chunks), `library/methods/` (regras extraídas)

### Methods extraídos (17+)

YAML files com regras mecânicas extraídas dos books via Ollama. Cada método tem trigger condition + scoring + paper signal generation.

Browse: `library/methods/*.yaml`

## Glossary (16 entradas — Tutor)

Cada métrica usada nos dossiers tem entrada própria com:
- Fórmula
- Leitura (good/bad)
- Thresholds BR vs US (do CLAUDE.md)
- **Contraméricas** (quando o sinal falha — onde está a alpha)
- Fontes (links para Clippings)

→ [[Glossary/_Index]]

**Como usar**: hover sobre `[[Glossary/PE]]` em qualquer dossier para preview Obsidian nativo.

## Como expandir

### Novos clippings
1. Salvar via Obsidian Web Clipper para `obsidian_vault/Clippings/`
2. `python -m library.clippings_ingest --rag-build` (embed novos)
3. `python scripts/research_digest.py` regenera digest

### Novos books
1. Drop PDF/EPUB em `library/books/`
2. `python -m library.ingest` → chunks
3. `python -m library.rag build` → embeddings
4. `python -m library.extract_insights --book <slug>` → methods YAML

### Novas Glossary entries
1. Editar `scripts/build_glossary.py` `ENTRIES` dict
2. `python scripts/build_glossary.py --backlinks`

### Tavily web research (autonomo)
- Perpetuum `autoresearch` corre diariamente via `daily_run.bat`
- Cache em `data/tavily_cache/` (avoid re-fetch 7d)
- Rate-limit: 100/dia, 50/hora (TAVILY_API_KEY em `.env`)
- Forçar manual: `python -m agents.perpetuum.autoresearch`

## Queries prontas (RAG semântico local)

```bash
# Pergunta direta com Qwen 14B + cita chunks
python -m library.rag ask "como o Buffett define moat?" --k 6
python -m library.rag ask "quando reinvestir DRIP vs receber cash?" --k 6
python -m library.rag ask "qual o critério Graham para barato?" --k 6
python -m library.rag ask "sinais antecedem crise dívida (Dalio)?" --k 8

# Search pura (chunks sem síntese)
python -m library.rag query "margem de segurança" --k 5
```

Ou via wrapper: `ii vault "pergunta em PT"` (mesma RAG + vault context).

## Stats (atualizado 2026-04-27)

| Asset | Count | Onde |
|---|---:|---|
| Clippings | 24 | `obsidian_vault/Clippings/` |
| Books | 4 | `library/books/` |
| Methods | 17 | `library/methods/*.yaml` |
| Glossary entries | **29** | `obsidian_vault/Glossary/` ([[Glossary/_Index|_Index]]) |
| Knowledge Cards | **12** | `obsidian_vault/Bibliotheca/Knowledge/` ([[Bibliotheca/Knowledge/_Index|_Index]]) |
| Total RAG chunks | 1949 | `library/chunks_index.db` (Ollama nomic-embed) |
| Tavily cache | 101 entries | `data/tavily_cache/` (TTL 7d) |
| Daily Research Digests | 2026-04-26 + ... | `obsidian_vault/Bibliotheca/Research_Digest_*.md` |
| Cleanup reports (one-time) | 4 | `obsidian_vault/Bibliotheca/Cleanup_*.md` |
| Test reports (one-time) | 1 | [[Bibliotheca/Test_Run_2026-04-26]] |
| Midnight Work reports | 1 | [[Bibliotheca/Midnight_Work_2026-04-27]] |
| Workday Work reports | 1 | [[Bibliotheca/Workday_Work_2026-04-27]] |
| Night Shift reports | 1 | [[Bibliotheca/Night_Shift_2026-04-27]] |

## Pipeline daily (cron 23:30)

```
[CLIPPINGS-INGEST]  novos clippings → RAG (Ollama embed)
[GLOSSARY]          rebuild entries + index (idempotente)
[TUTOR]             re-inject ## Tutor section em todos os DOSSIE.md
[KNOWLEDGE-CARDS]   skip-if-exists; gera só novas perguntas
[RESEARCH-DIGEST]   gera Research_Digest_<DATE>.md
```

Plus: synthetic_ic + variant_perception + earnings_prep corem manualmente / weekly.

---
*Auto-build via [[Bibliotheca/_Index]]. Última actualização: 2026-04-27 (midnight work).*
