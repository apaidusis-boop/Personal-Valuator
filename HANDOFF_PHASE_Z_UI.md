# 📋 HAND-OFF — Nova conversa Phase Z (UI Friendly Layer)

> **Como usar**: copia tudo abaixo a partir da linha "BEGIN PROMPT" e cola numa conversa Claude Code nova (`cd C:\Users\paidu\investment-intelligence` antes). É self-contained.

---

## BEGIN PROMPT ⬇️ copia daqui

Olá. Sou um investidor pessoa física a operar BR (B3) + US (NYSE/NASDAQ) com filosofia DRIP/Buffett-Graham. **Sou vibe-coder leigo em comandos**. Estou a abrir uma conversa nova focada em criar a **camada UI friendly** do meu sistema (Phase Z).

## 1) Lê primeiro estes 3 documentos para entrares no contexto

```
obsidian_vault/CONSTITUTION.md      # master doc — TUDO sobre o projecto
PHASE_Y8_REPORT.md                  # último report técnico (RI Knowledge Base)
CLAUDE.md                           # script catalog + filosofia
```

Resumo curto enquanto não lês:
- **Sistema com 9 perpetuums autónomos** que correm SQL/Ollama/Python local diariamente, geram signals, escrevem em SQLite + vault Obsidian.
- **1,152 methods** extraídos de Damodaran + 3 Dalio (RAG local com nomic-embed + Qwen 14B). Zero tokens Claude no pipeline.
- **CVM data ingerida** — 6 anos de DRE/BPA/BPP/DFC para 5 stocks BR + 96 monthly observations de 4 FIIs.
- **932 paper signals open** baseado nos 16 YAML methods.
- **35 holdings** (12 BR + 21 US) + watchlist.

## 2) O problema (porquê esta phase existe)

Tudo o que o sistema produz hoje vive em:
- SQLite tables (preciso de Python ou sqlite3 para ler)
- Markdown notes em obsidian_vault/ (lê-se OK no Obsidian app)
- Stdout de scripts CLI (`python -m library.ri.cvm_parser show VALE3`)

**Eu não consigo (ou não gosto) de digitar**:
- `python -c "import sqlite3..."`
- `cat obsidian_vault/tickers/VALE3_RI.md`
- `python -m library.rag ask "..."`

**O que quero**:
- Abrir um browser (ou Obsidian) e ver tudo bonito, navegável, com charts
- Fazer perguntas em português via input text e ler resposta formatada
- Aprovar actions T2 com clique
- Ver health score por ticker em dashboard visual
- Botão "regenerate report" que corre os scripts no background
- Nada de comandos terminal no flow normal de uso

## 3) O que JÁ existe (não construas do zero)

- **Streamlit dashboard** em `scripts/dashboard_app.py` (`ii dashboard` → localhost:8501) — está OK mas pouco usado
- **Obsidian vault** rico (CONSTITUTION.md, 184 ticker notes, 26 skill docs, briefings, wiki)
- **Obsidian Dataview plugin** instalado (queries SQL-like sobre frontmatter)
- **Obsidian Charts plugin** instalado (line/bar charts em ```chart blocks)
- **5 vault timelines** auto-gerados em `obsidian_vault/tickers/{X}_RI.md` com chart embed
- **CLI `ii`** super-comando unificado (mas ainda CLI)

## 4) O que está em mente (skills mapeadas Phase W mas não executadas)

Em [[obsidian_vault/skills/_MOC|skills/_MOC.md]] tenho avaliações de 33 skills externas. Para Phase Z relevantes:

- **Frontend Design** (Anthropic) — tier B no roadmap mas pode subir
- **Canvas Design** (Anthropic) — gerar SVG/PNG charts annotated
- **Web Artifacts Builder** (Anthropic) — mini-apps web stand-alone
- **Remotion** — auto video weekly recap (overkill mas autorizado)
- **PPTX skill** — quarterly deck

Já tinha decidido aproveitar Streamlit (não rewrite em React/Next).

## 5) O que quero construir nesta sessão

Discutamos primeiro a abordagem. Algumas hipóteses para escolher:

**Opção A — Expand Streamlit dashboard** (low-effort, leverage existente)
- Mais páginas: RI Timeline, Paper Signals, Perpetuum Health, T2 Actions queue
- Botões "approve/reject action"
- Embedded charts plotly
- "Ask the library" input → roda RAG no background

**Opção B — Static HTML reports** (rendered files, super portable)
- Jinja2 templates → output em `reports/html/`
- Auto-refresh via cron
- Open com double-click
- Versão print-friendly por ticker / por perpetuum / quarterly

**Opção C — Obsidian-native dashboards** (zero novo tooling)
- Aproveita Dataview + Charts + Bases plugins
- Cada ticker tem dashboard com queries automáticas
- Master dashboard agrega tudo
- Limitação: queries são limitadas a frontmatter/file structure

**Opção D — Mix** (provavelmente o certo)
- Obsidian para docs + read flow normal
- Streamlit para interactive (ask library, approve actions)
- Static HTML para weekly/quarterly deliverables

## 6) Workflow ideal (visão pessoal)

```
Manhã:
  1. Abro Obsidian
  2. Vejo Home.md → vê briefing + alerts
  3. Click ticker → vejo timeline + thesis health
  4. Se houver T2 action → click "approve" no Streamlit
  5. Se quiser entender algo → "Ask Library" input box

Semana:
  - Receber automaticamente weekly HTML report no email/folder
  - Ver video recap 60s no fim de domingo (Remotion overkill, mas...)
```

## 7) Constraints rígidos

- **Backend continua 100% local** (Ollama/SQLite/Python). Frontend pode ser Streamlit/HTML.
- **Zero tokens Claude no pipeline** — frontend pode usar Claude API se ABSOLUTAMENTE necessário, mas default Ollama.
- **Não rewrite o backend** — só wrappar o que existe.
- **Cada feature nova** entra na Constitution changelog.
- **Tudo respeita os 6 não-negociáveis** (ver Constitution).

## 8) O que peço primeiro

1. Lê os 3 docs do passo 1
2. Inspecciona `scripts/dashboard_app.py` (Streamlit existente)
3. Inspecciona 1-2 ticker notes (`obsidian_vault/tickers/VALE3_RI.md` por exemplo) para veres o estilo actual
4. Propõe um **roadmap concreto Phase Z** com sprints (Z.0, Z.1, ...) tipo o que fizemos antes
5. Recomenda uma das Opções A-D (ou outra) com tradeoffs honestos
6. Identifica 3-5 skills concretas (do Tier S/A) a integrar
7. **Execute Z.0** (scope freeze + decisão arquitetural) ainda nesta sessão

## 9) Estilo de trabalho preferido

- Direto, sem narração excessiva
- Auto mode acceptable — execute, mostra resultados, pergunta apenas em ambiguidade real
- Background jobs para tudo que demora >2 min
- Reports + commit com changelog updates
- Português PT como default

## 10) Memória persistente

Tenho memória em `~/.claude/projects/C--Users-paidu-investment-intelligence/memory/`. Lê `MEMORY.md` para os pointers. **CRÍTICO**: respeita as memórias `feedback_inhouse_first`, `carteiras_isoladas`, `ten_distress_signal`, `grek_irregular_dividends`, `feedback_honest_projections`.

---

Pronto. Quando terminares de ler os 3 docs, propõe o roadmap Z e arrancamos. Vamos.

## END PROMPT ⬆️ copia até aqui
