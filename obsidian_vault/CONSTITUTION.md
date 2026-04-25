---
type: constitution
tags: [constitution, master, history, governance]
created: 2026-04-25
last_updated: 2026-04-25
phases_done: [W, X, Y, Y.8]
current_phase: Z (UI Friendly Layer)
---

# 📜 The Constitution — Investment Intelligence Project

> **Documento mestre vivo.** Cada phase concluída adiciona uma secção "Changelog". Cada decisão estratégica entra na "Decision Log". Quando voltares ao projecto após pausa, **lê esta página primeiro**.

## 🎯 Identity & Purpose

Sistema pessoal de inteligência de investimentos para **um investidor pessoa física** a operar em duas geografias:

- 🇧🇷 **Brasil (B3)** — 12 holdings (5 stocks + 5 FIIs + 2 ETFs)
- 🇺🇸 **EUA (NYSE/NASDAQ)** — 21 holdings

**Estratégia core**: DRIP (Dividend Reinvestment Plan) com filosofia Buffett/Graham — quality compounders + margem de segurança + dividendos consistentes.

**Horizon**: long-term (anos, não meses).

**User profile**: vibe coder. Comandos terminal são deslike; prefere ler resultados em Obsidian/HTML/dashboards. Decisões são tomadas com clareza visual + contexto.

## 🛡️ Os 6 não-negociáveis (constitutional rules)

1. **In-house first** — Tudo que rode localmente (SQL, Ollama, scripts) NÃO usa tokens Claude. Claude é último recurso. Esta é a meta-regra que governa todas as outras.

2. **Carteiras isoladas** — Dinheiro USD fica em US, BRL em BR. Nunca sugerir conversão entre contas.

3. **Paper-trade antes de real capital** — Qualquer signal novo (library methods, perpetuums) entra em `paper_trade_signals`. Real capital só após 30+ closed signals com win_rate >60%.

4. **Honest projections** — Em forward scenarios, evitar assumptions optimistas. Aplicar damper quando histórico >> Gordon.

5. **Tier-gated autonomy** — Perpetuums escalam T1→T2→T3→T4→T5 com base em estabilidade comprovada (30d sem false positives). User aprova promoção.

6. **Tickers blacklist** — Memória persistente:
   - **TEN**: 4 sinais cycle peak Apr 2026 → NUNCA adicionar
   - **GREK**: dividendos irregulares → NÃO aplicar lógica DRIP

## 🗺️ Architecture Map

```
investment-intelligence/
├── CLAUDE.md                           # Contrato projecto + script catalog
├── CONSTITUTION.md                     # ESTE documento (link via vault)
├── config/
│   └── universe.yaml                   # ÚNICA fonte de verdade dos tickers
├── data/
│   ├── br_investments.db               # SQLite BR — schema canónico
│   ├── us_investments.db               # SQLite US — mesmo schema
│   ├── overnight/                      # Logs de runs autónomos
│   ├── ri_compare/                     # Comparações trimestrais JSON
│   └── statusinvest_cache/             # MCP cache
├── fetchers/                           # 1 fetcher por fonte
├── scoring/                            # Engine de critérios
├── analytics/                          # Backtests + regime classifier
├── agents/
│   ├── perpetuum/                      # ⭐ 9 perpetuums activos (Phase X)
│   └── *.py                            # 12 agents framework V
├── library/                            # ⭐ Knowledge base (Phase X+Y)
│   ├── books/                          # 4 PDFs ingeridos (Damodaran, 3 Dalio)
│   ├── chunks/                         # 1704 text chunks
│   ├── insights/                       # JSON estruturado por book
│   ├── methods/                        # 16 YAML methods (Graham, Dalio, Damodaran)
│   ├── chunks_index.db                 # RAG embeddings (nomic-embed)
│   └── ri/                             # ⭐ RI knowledge base (Phase Y)
│       ├── catalog.yaml                # 5 stocks + 5 FIIs + 15 watchlist
│       ├── cache/                      # ZIPs CVM oficiais
│       └── *.py                        # cvm_filings, cvm_parser, fii_filings, etc.
├── scripts/                            # CLI + utility
│   ├── overnight/                      # Orchestrators autónomos
│   └── ii (CLI unificado)
└── obsidian_vault/                     # ⭐ Frontend humano
    ├── Home.md                         # Hub principal
    ├── CONSTITUTION.md                 # ← este doc
    ├── tickers/                        # 184 ticker notes (35 holdings + 149 watchlist)
    ├── briefings/                      # Daily morning briefings
    ├── skills/                         # Phase W/X/Y design docs
    ├── wiki/                           # 53 conceptual notes
    └── agents/                         # Agent status notes
```

## 📚 Phases History

### ✅ Phase V (concluída antes desta série) — Agent framework
Foundational. 12 agents inicialmente. Frase "agent framework + persona company".

### ✅ Phase W — Skills Arsenal (2026-04-24)
Avaliou 33 skills externas (vídeo YouTube referência). Output:
- Roadmap em `obsidian_vault/skills/Roadmap.md` (11 sprints W.1-W.11)
- 26+ notas em `obsidian_vault/skills/`
- 5 skills custom criadas em `.claude/skills/`: drip-analyst, panorama-ticker, rebalance-advisor, macro-regime, perpetuum-review
- Metrics baseline frozen
- Scaffolding inicial do Perpetuum Engine

### ✅ Phase X — Perpetuum Engine (2026-04-24 → 2026-04-25)
Generalização do `perpetuum_validator` em pattern arquitectural com plugin architecture.

**9 perpetuums activos**:
| # | Nome | Tier | Subjects | Função |
|---|---|---|---:|---|
| 1 | thesis | T1 | 33 | Valida thesis explícita por holding |
| 2 | vault | T2 | 376 | Saúde de notas (orphans, stale, broken links) |
| 3 | data_coverage | T2 | 33 | Completeness de dados por holding |
| 4 | content_quality | T1 | 18 | Signal-to-noise de briefings |
| 5 | method_discovery | T1 | 8 | Staleness dos critérios + autoresearch queries |
| 6 | token_economy | T1 | 117 | Procura waste de Claude tokens, propõe Ollama |
| 7 | library_signals | T1 | 1092 | Aplica YAML methods × portfolio |
| 8 | ri_freshness | **T2** | 5 | Monitor staleness de filings CVM |
| 9 | meta | T1 | 7 | Auto-audit dos outros perpetuums |

**Total**: 1684+ subjects scored/dia.

**Autonomy tiers**:
- **T1 Observer**: detecta + alerta
- **T2 Proposer**: escreve action em `watchlist_actions` para 1-click approve
- **T3 Sandboxed**: actua em worktree isolado
- **T4 Guarded**: produção com hard limits
- **T5 Autonomous**: livre com sample audits

### ✅ Phase X (extras) — Library + RAG (2026-04-24)
Pipeline books → methods → matcher → paper signals.

**4 livros ingeridos** (1,628 chunks processados, 100% Ollama):
| Livro | Methods | Heuristics | Concepts |
|---|---:|---:|---:|
| Damodaran Investment Valuation 3rd ed | **910** | 1,869 | 2,191 |
| Dalio Big Debt Crises | 232 | 846 | 1,119 |
| Dalio CWO Charts | 7 | 47 | 114 |
| Dalio CWO Power Index | 3 | 26 | 45 |
| **TOTAL** | **1,152** | **2,788** | **3,469** |

**RAG**: 1,704 chunks indexed via nomic-embed-text local. Queryable em PT cross-book.

**16 YAML methods** activos: Graham defensive, Dalio All Weather, Dalio bubble 4-criteria, Dalio capital flow, Damodaran implied ERP, Damodaran unlevered beta, + 10 auto-generated do Damodaran.

**Paper signals**: ~932 acumulados (392 BR + 540 US). Zero capital real envolvido.

### ✅ Phase Y — RI Knowledge Base v1 (2026-04-25 manhã)
Pipeline directo CVM → DB normalizado.

- `library/ri/catalog.yaml` — 5 stocks + 5 FIIs catalogados com CVM codes
- `library/ri/cvm_filings.py` — DFP/ITR/IPE downloader
- `library/ri/cvm_parser.py` — DRE/BPA/BPP/DFC → quarterly_history
- `library/ri/compare_releases.py` — Q-o-Q + YoY + material flags
- `agents/perpetuum/ri_freshness.py` — 9º perpetuum
- `obsidian_vault/tickers/{X}_RI.md` — 5 timelines auto-gerados

**Material finding**: VALE3 YoY EBIT -25.4%, EBIT margin -10pp, debt +27.6%, FCF -68.2% → quality deterioration confirmado.

### ✅ Phase Y.8 — RI Expansion (2026-04-25 tarde)
- `quarterly_single` view (resolve YTD artifact dos ITRs)
- DFP backfill 2020-2023 → 6 anos coverage
- `fii_filings.py` + 4/5 FIIs ingeridos (96 monthly observations)
- 15 watchlist BR auto-populados (com ~40% match errado — needs review)
- ri_freshness promoted T1 → T2

**Material finding**: VALE3 single-Q expõe **Q4 2024 net income NEGATIVO (-R$ 5.8 bi)** + EBIT margin 7.7% (vs 30%+ típico). Provavelmente write-off Mariana/Brumadinho. Sem single-Q view, escondido pelo YTD.

### 🔄 Phase Z — UI Friendly Layer (2026-04-25, em curso)
Eliminar comandos terminal do flow normal. Backend não muda; só wrapping.

**Decisão arquitectural**: Opção D (mix), pesada em Streamlit.
- Streamlit = interactive (approve, ask library, screener, deep dive)
- Obsidian + Dataview + Charts = read flow normal
- (Futuro) HTML/Jinja2 = deliverables weekly/quarterly

**Sprints concluídos** (Z.0–Z.7, ~1h):
| # | Sprint | Output |
|---|---|---|
| Z.0 | Roadmap doc | `PHASE_Z_ROADMAP.md` |
| Z.1 | T2 Actions queue page | Streamlit "🎯 Actions Queue" — approve/ignore/note via UI |
| Z.2 | Ask Library page | Streamlit "📚 Ask Library" — RAG via subprocess + history |
| Z.3 | Perpetuum Health dashboard | Streamlit "🩺 Perpetuum Health" — summary + trend chart + drill-down |
| Z.4 | Paper Signals viewer | Streamlit "📈 Paper Signals" — filtros + convergence detection |
| Z.5 | RI Timeline page | Streamlit "📊 RI Timeline" — quarterly history + 4 plotly charts |
| Z.6 | Home.md morning landing | Dataview queries (decisões, holdings, screen passers) + dashboard URL |
| Z.7 | One-click launcher | `start_dashboard.bat` + `scripts/create_desktop_shortcut.ps1` |

**Total dashboard pages**: 9 (era 5). Total LOC adicionados: ~440.

**Critério sucesso**: 0 comandos terminal no morning flow. Validar resolvendo os 20 triggers abertos via UI Z.1.

## 🧠 Decision Log

| Data | Decisão | Racional |
|---|---|---|
| 2026-04-24 | Skills Arsenal limited a Tier S inicialmente; depois "all Gold" autorizado | User pediu "overkill is fine" |
| 2026-04-24 | Perpetuum como pattern arquitectural, não feature única | User: "processos em perpétuo autoconhecimento" |
| 2026-04-24 | Library/methods são paper-only — NÃO sugerir trades reais até 30+ closed signals | Risco asimétrico de option plays untested |
| 2026-04-24 | Books: focar Graham/Dalio/Damodaran (não options trading) | Alinhado com DRIP/value philosophy |
| 2026-04-25 | Autonomy tiered (T1-T5) — perpetuums sobem só com track record | Safety; user confirma promoção |
| 2026-04-25 | RI primary source = CVM oficial (não scrape RI sites) | Estável, deterministic, free |
| 2026-04-25 | Frontend cliquetó (Streamlit + Obsidian) prioritário sobre CLI | User vibe-coder; ler > digitar |
| 2026-04-25 | Phase Z = expand Streamlit (não rewrite React/Next) | 80% scaffold já existe; single-user local |
| 2026-04-25 | Streamlit UI chama scripts existentes via subprocess | Não duplicar lógica; CLI continua canónico |

## 🔁 Estado actual dos perpetuums (live)

```
Total subjects scored/dia: 1,684+
Total perpetuum_health rows:  3,508+
Open T2 actions:              6 (vault REVIEW + data_coverage fetch)
Paper signals OPEN:           932
Tickers BR com thesis:        28/35 (vs 2 antes overnight)
Tickers BR com RI timeline:   5/5 holdings stocks
```

## 📊 Library + RI Knowledge

```
quarterly_history:   75 rows (15Q × 5 stocks, 2019Q4-2025Q3)
quarterly_single:    75 rows (single-Q derived)
cvm_dre/bpa/bpp/dfc: ~36k rows totais
cvm_ipe:             1,055 fatos relevantes
fii_monthly:         96 (24m × 4 FIIs)
fii_balance_sheet:   96
RAG chunks indexed:  1,704
YAML methods:        16
Paper signals:       932
Books processed:     4 (1,628 chunks → 1,152 methods extracted)
```

## 🎯 Comandos canónicos (que CLAUDE.md catalogue conhece)

```bash
# Daily run completo
python agents/perpetuum_master.py

# Review T2 actions
python scripts/perpetuum_action_run.py list-open
python scripts/perpetuum_action_run.py <id>          # approve specific

# RI deep dive single ticker
python -m library.ri.cvm_parser show VALE3
python -m library.ri.quarterly_single show VALE3

# RAG questions cross-book
python -m library.rag ask "pergunta em PT" --k 8

# Generate vault timelines
python -m library.ri.compare_releases --all-catalog

# Add new book
cp livro.pdf library/books/
python -m library.ingest && python -m library.extract_insights --book <slug> --max 100
```

## 🚧 Open issues / known limitations

1. **Watchlist BR auto-populator ~40% match errado** (ITUB4, SUZB3, TTEN3, EQTL3, ENGI11) — user precisa revisar manualmente.
2. **RBRX11 não resolvido** no FII module.
3. **fii_monthly DY display em decimal vs %** — bug cosmético.
4. **Frontend é tudo CLI** — user vibe-coder não consegue ler outputs facilmente. **PHASE Z proposed**: UI friendly layer.
5. **ITRs 2019-2023 não baixados** (só DFPs). Para 24Q full coverage por ticker, baixar.
6. **Bank-specific schema** (BBDC4/ITUB4) — DRE bancária diferente; parser actual genérico funciona mas ignora detalhes BACEN.
7. **Quarterly_single para watchlist novos** — só ingere 5 holdings principais; novos 15 watchlist precisam ingest específico.

## 📄 Reports gerados

```
PHASE_Y_REPORT.md       — Y v1 (manhã 25/04)
PHASE_Y8_REPORT.md      — Y.8 expansão (tarde 25/04)
MORNING_REPORT.md       — Overnight 24→25
```

Plus 26+ docs em `obsidian_vault/skills/` e 5 timelines em `obsidian_vault/tickers/*_RI.md`.

## 🔮 Próxima fase proposta — Phase Z (UI Friendly Layer)

User explicitamente pediu (sessão 25/04 final):
> "Eu sou bem leigo em comandos. Quero abrir documentos, de maneira user-friendly, seja em HTML, seja no Obsidian, sem pulls/cats/python commands. Backend pode ser tudo isso, frontend tem que ser friendly."

**Direcções possíveis**:
- Aproveitar **Streamlit dashboard** (`ii dashboard`) já existente — expandir
- Static HTML reports auto-gerados (Jinja2 + cron)
- Obsidian dashboards via Dataview queries pré-escritas
- Skills do Tier S Phase W: Frontend Design + Canvas Design + Web Artifacts Builder
- Templated daily/weekly reports renderizados em HTML

→ Hand-off prompt em `HANDOFF_PHASE_Z_UI.md` (criado em paralelo).

## 📝 Changelog

| Data                   | Phase            | Mudança principal                                       | Tokens Claude pipeline |
| ---------------------- | ---------------- | ------------------------------------------------------- | ---------------------: |
| 2026-04-24 morning     | W                | Skills arsenal evaluated, baseline frozen               |                      0 |
| 2026-04-24 afternoon   | X                | Perpetuum engine (3 perpetuums initial)                 |                      0 |
| 2026-04-24 evening     | X+Lib            | 4 books ingested, RAG built, 154 paper signals          |                      0 |
| 2026-04-24 night       | Overnight        | 5 phases autónomas: thesis populate, methods, RAG batch |                      0 |
| 2026-04-25 morning     | Y                | RI Knowledge Base v1 (CVM pipeline)                     |                      0 |
| 2026-04-25 afternoon   | Y.8              | Single-Q view, DFP backfill, FII module, watchlist auto |                      0 |
| **2026-04-25 evening** | **Constitution** | **Este documento criado**                               |                      0 |

## 🧭 Como usar este documento

1. **Voltei depois de dias** → lê secção "Estado actual" + "Open issues" + último entry do changelog
2. **Quero arrancar nova phase** → revê "Decision Log" para não repetir decisões
3. **Não sei o que mudou desde X** → "Changelog" tem timeline
4. **Não lembro onde está Y** → "Architecture Map" + "Comandos canónicos"
5. **User pergunta "ainda sigo a regra Z?"** → "6 não-negociáveis"

## 🔗 Cross-links principais

- [[Home|🏠 Home]]
- [[skills/_MOC|🧰 Skills MOC]]
- [[skills/Phase_X_Perpetuum_Engine|🔁 Perpetuum Engine]]
- [[skills/Phase_Y_Roadmap|🏗️ Phase Y Roadmap]]
- [[skills/Library_Books_and_Options|📚 Library + Options strategy]]
- [[skills/Session_2026-04-24_Final_State|🏆 Session 24/04 final]]
- [[wiki/Index|📚 Wiki Index]]

---
*A Constituição é viva. Cada commit grande adiciona linha ao Changelog + actualiza secção relevante.*
