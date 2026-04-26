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

## Stats

| Asset | Count |
|---|---:|
| Clippings | 24 |
| Books | 4 |
| Methods | 17 |
| Glossary entries | 16 |
| Total RAG chunks | 1949 |
| Tavily cache | 101 entries |

---
*Auto-build via [[Bibliotheca/_Index]]. Última actualização: 2026-04-26.*
