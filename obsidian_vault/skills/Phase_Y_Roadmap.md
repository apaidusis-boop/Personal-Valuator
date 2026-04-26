---
phase: Y
title: RI Knowledge Base
status: in-progress
started: 2026-04-25
sprints: 8  # Y.0–Y.7
---

# 🗺️ Phase Y — RI Knowledge Base

> **Objectivo**: transformar a infra existente de monitorização CVM em uma **knowledge base estruturada de RI (Relações com Investidores)** — capaz de indexar, pesquisar e responder perguntas sobre documentos formais (DFP, ITR, FRE, IPE) e materiais de RI (releases trimestrais, presentations, calls) das empresas e FIIs que sigo.

> **Por quê agora?** Já tenho `cvm_monitor` (fatos relevantes), `subscriptions` (broker reports), `library` (livros). Falta a camada **primary-source RI** — directamente da empresa. Para uma estratégia DRIP/Buffett-Graham, ler os filings originais é a maior margem de segurança contra noise de analistas.

> **Filosofia (não-negociável)**: in-house first. Toda a ingestão, parsing e indexação é local (CVM dados abertos + RI websites + Ollama). Claude API só entra para sintetizar quando explicitamente pedido.

---

## Scope

### IN scope
- Catálogo curado de tickers BR (stocks + FIIs) → CVM codes + CNPJ + RI URL
- Download e cache de filings CVM (DFP, ITR, FRE, IPE, FCA, cad_fii)
- Parse estruturado de DFP/ITR (XBRL + CSV) para histórico de DREs/BPs
- Scraping respeitoso de páginas RI (releases trimestrais, apresentações)
- Indexação RAG sobre o corpus RI (re-uso de `library/rag.py`)
- CLI: `ii ri <ticker>` (resumo), `ii ri ask "pergunta"` (RAG)
- Integração com `verdict` engine (RI evidence influencia score)

### OUT of scope (deferido)
- Tickers US (10-K já está em `sec_edgar_fetcher`; SEC equivale ao CVM)
- Conference call transcripts (Phase Y.7+ se houver demanda)
- OCR de PDFs digitalizados antigos
- Tradução automática EN↔PT

---

## Architecture

```
library/ri/
├── __init__.py
├── catalog.yaml              # ticker → CVM code, CNPJ, RI URL, filings
├── cvm_codes.py              # POC + helper para resolver/validar codigo_cvm
├── cvm_filings.py            # download+cache DFP/ITR/FRE/IPE
├── cvm_parser.py             # XBRL/CSV → linhas estruturadas (DRE, BP, DFC)
├── ri_scraper.py             # scrape ri.<empresa>.com.br (releases, apresentações)
├── indexer.py                # corpus RI → chunks → embeddings (Ollama nomic)
├── cli.py                    # ii ri <ticker>, ii ri ask "..."
└── cache/                    # ZIPs CVM, PDFs RI, parsed CSVs
    ├── cvm/                  # ipe_cia_aberta_2026.zip etc.
    ├── ri_pdfs/              # apresentações trimestrais
    └── parsed/               # CSVs normalizados pós-parse
```

### Database tables (br_investments.db)

```sql
CREATE TABLE ri_documents (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker          TEXT NOT NULL,
  source          TEXT NOT NULL,          -- 'cvm_dfp', 'cvm_itr', 'cvm_fre', 'cvm_ipe', 'ri_release', 'ri_presentation'
  doc_date        TEXT NOT NULL,          -- ISO date
  period_end      TEXT,                   -- quarter/annual end (DFP/ITR)
  title           TEXT,
  url             TEXT,
  local_path      TEXT,                   -- caminho cache local
  hash            TEXT,                   -- sha256 pra deduplicação
  ingested_at     TEXT NOT NULL,
  UNIQUE(ticker, source, hash)
);

CREATE TABLE ri_chunks (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  document_id     INTEGER NOT NULL REFERENCES ri_documents(id),
  chunk_idx       INTEGER NOT NULL,
  text            TEXT NOT NULL,
  embedding       BLOB                    -- nomic-embed-text via Ollama
);

CREATE INDEX idx_ri_documents_ticker ON ri_documents(ticker, source, doc_date);
CREATE INDEX idx_ri_chunks_doc ON ri_chunks(document_id);
```

---

## Sprints

### Y.0 — Roadmap formal *(esta sessão)*
- [x] Este documento (`Phase_Y_Roadmap.md`)
- [x] Scope, architecture, sprint plan validados

### Y.1 — Skeleton + catálogo manual *(esta sessão)*
- [x] `library/ri/__init__.py`
- [x] `library/ri/catalog.yaml` — 5 stocks holdings + 5 FIIs holdings, com CVM codes + CNPJ curados manualmente
- [x] `library/ri/cvm_codes.py` — POC: download cad_cia_aberta.csv + lookup
- [x] Test funcional: 1 ticker resolvido contra dados oficiais CVM

### Y.2 — DFP/ITR ingestion *(próxima sessão)*
- [ ] `cvm_filings.py download dfp --year 2025` baixa todos os ZIPs DFP
- [ ] Schema `ri_documents` + `ri_chunks` migration
- [ ] Indexador básico DFP → tabela `ri_documents`
- [ ] Smoke test: VALE3 DFP 2024 ingerido + queryável via SQL

### Y.3 — Parser XBRL/CSV
- [ ] `cvm_parser.py`: DRE, BPA, BPP, DFC normalizados em CSV
- [ ] Histórico ≥ 5 anos por ticker em DBs (`fundamentals_history` extended)
- [ ] Comparação cross-period: revenue growth, margin trend
- [ ] Plug em `analytics.screen_trend` para signal de quality drift baseado em DFP raw

### Y.4 — IPE deep (fato relevante full-text)
- [ ] `cvm_filings.py download ipe --year 2026` (já temos resumos via cvm_monitor; agora full PDFs)
- [ ] PDF → text extraction (pdfplumber, sem OCR por agora)
- [ ] Re-uso `library/rag.py` para indexar full text dos fatos relevantes
- [ ] CLI: `ii ri events <ticker>` lista IPE com texto resumido por Ollama

### Y.5 — RI scraping (release trimestral + apresentações)
- [ ] `ri_scraper.py` — política `cache_policy.py` (24h TTL, robots.txt respeitado)
- [ ] Scrape estruturado de ri.vale.com.br, ri.itausa.com.br, etc.
- [ ] PDFs trimestrais → cache local + parse
- [ ] FIIs: informe mensal + relatório gerencial (mensal/trimestral)

### Y.6 — RAG sobre corpus RI
- [ ] `indexer.py` chunks + embeddings (re-uso `library/rag.py` infra)
- [ ] CLI: `ii ri ask "como evoluiu o capex da Vale 2020-2025?"`
- [ ] Citações: cada answer aponta para `ri_documents.id`
- [ ] Smoke test: 5 perguntas-chave por ticker holding

### Y.7 — Integração verdict + agent
- [ ] `verdict` engine consulta RI signals (margin trend, capex trajectory)
- [ ] Novo agent `agents/ri_watcher.py` — perpetuum diário
- [ ] Telegram push quando filing relevante (DFP/ITR novo, IPE de holding)
- [ ] Obsidian: cada ticker tem secção "RI Recent" auto-populada

---

## Out-of-band items / risks

- **CVM rate limit**: dados.cvm.gov.br não tem rate limit conhecido, mas vamos respeitar `User-Agent` identificável (já feito em `cvm_monitor`)
- **Tamanho do corpus**: DFP/ITR de 5 anos × 30 empresas pode ser ~50GB raw. Plano: parse-and-discard — guardamos só CSVs normalizados pós-parse + chunks indexados
- **PDFs scaneados**: alguns DFPs antigos (<2010) podem ser imagem. Phase Y.4 ignora-os (deferido para OCR phase).
- **FIIs CVM dataset**: estrutura diferente das companhias abertas — dataset `FII/DOC` separado, formato distinto. Y.2 trata stocks; FIIs entram em Y.5+ via informe mensal.

---

## Sucesso (definição)

**A Phase Y está completa quando:**
1. Os 5 stocks + 5 FIIs holdings têm catálogo CVM validado (Y.1) ✅
2. Histórico ≥ 5 anos de DFPs ingerido por ticker holding (Y.2-Y.3)
3. Última DRE / BP queryável por SQL em <10ms
4. RAG responde "qual o EBITDA margin da PRIO em 2024 vs 2023" com citação ao filing original
5. `ii ri <ticker>` mostra: últimos 4 trimestres, último fato relevante, link RI direto
6. Cron diário detecta novo filing CVM em <24h

---

## Links e referências

- CVM Dados Abertos: https://dados.cvm.gov.br/
- IPE: `https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_<YYYY>.zip`
- DFP: `https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/`
- ITR: `https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/`
- FRE: `https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/`
- FCA: `https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv`
- FII cadastro: `https://dados.cvm.gov.br/dados/FII/CAD/DADOS/cad_fii.csv`
- Memória relacionada: [[phase_x_perpetuum_engine]], [[us_data_sources_catalog]] (mirror US)
