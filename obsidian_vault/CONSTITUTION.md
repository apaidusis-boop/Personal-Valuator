---
type: constitution
tags: [constitution, master, history, governance]
created: 2026-04-25
last_updated: 2026-04-25
phases_done: [W, X, Y, Y.8, Z.0-Z.7, AA, FIX, AUTO, Z.Design (Helena s1-s4), CATALOG_FIX, BB (code_health), CC (Captain's Log), F (T0 cleanup), G (Thesis backfill + C.2 analyst tracking), H (Telegram brief), I (Wiki holdings B.2 closeout), J (Universe-wide thesis + bank BS schema), K (Autoresearch / Tavily wired), K.2 (Tavily 3-wire integration), K.3 (Tavily Skills + CLI), L (BACEN fetcher + W.11 Quant stack + IC universe-wide), U.0 (Unification Sweep — 3-layer brain formalised), W.6.1 (Pydantic structured outputs + typed Ollama wrapper)]
current_phase: FF — Calibration Loop (Blocos 1-3, 3 semanas). Triggered 2026-05-05 após external AI critique (4 attack vectors: calibration void, latent space echo chamber, decorator macro, L1 quicksand). Bloco 4 (Capital Deployment) DEFERRED como Phase GG, prerequisite ≥90 dias validated verdicts. Começa com Bloco 1.1: Decision Quality Engine + benchmark schema.
---

# 📜 The Constitution — Investment Intelligence Project

> **Documento mestre vivo.** Cada phase concluída adiciona uma secção "Changelog". Cada decisão estratégica entra na "Decision Log". Quando voltares ao projecto após pausa, **lê esta página primeiro**.

## 🚪 Voltamos — sintetizador de retomada

> **Quando o user diz "Voltamos" numa nova conversa**: lê esta secção primeiro. Tem tudo que precisas para continuar do ponto certo sem queimar tokens em re-audits.

**Última sessão**: 2026-05-05 — **Phase FF (Calibration Loop) iniciada**. Após external AI critique em 4 rondas (briefing → 15 surgical questions → improvement roadmap → 4 attack vectors), formalizou-se o que faltava no sistema: *closed-loop validation*. Bloco 4 do roadmap externo (Capital Deployment) **deferred como Phase GG** com prerequisite explícito de ≥90 dias de validated verdicts. Começa com Bloco 1.1: schema migration `verdict_history` (8 outcome columns + `verdict_engine_breakdown` table) + `analytics/decision_quality.py` com benchmark comparison (SPY US / BOVA11 BR / sector ETFs). **Bloqueador imediato**: prices de SPY/BOVA11 com zero rows nas DBs — primeiro fetch antes do calibration_curve produzir números. Briefing externo + replies + roadmap em `EXTERNAL_AI_BRIEFING*.md` no root.

**Contexto da decisão Phase FF**:
- Critique mais aguda recebida: "If you had to prove to a skeptic today that this system isn't just retrofitting data to validate your pre-existing Buffett/Graham biases, what specific empirical evidence from your SQLite L1 layer could you point to?"
- Resposta honesta hoje: nenhuma. Em 90 dias, com FF rodando, podemos apontar para calibration curve + hit rate por engine + sector tilt + anomalias L1.
- Princípio: validação **antes** de capital. Bloco 4 (deploy) sem Bloco 1 (calibrate) seria confirmation bias retrofit.

### ✅ Sessão 2026-04-28 noite — Phase W.6.1 (structured outputs)

### ✅ Sessão 2026-04-28 noite — Phase W.6.1 (structured outputs)

Continuação do Roadmap após o detour Stitch. Sprint W.6 dividido em sub-sprints; **W.6.1 = Instructor/Pydantic schemas** (1º entregável dos 5 do W.6 original).

**Ficheiros novos**:
- `agents/_schemas.py` — PersonaVerdict, ThesisDraft, HoldingWikiStub. Literal types nos enum fields, conint(1,10) na conviction, validators que toleram input messy (single string → list, casing tolerance).
- `agents/_llm.py::ollama_call_typed[T]` — pipeline ollama_call_json → schema.model_validate → instance | None. Caller decide retry.

**3 refactors**:
- `agents/synthetic_ic.py::ask_persona` — substituiu regex `{.*}` + sub trailing-comma + json.loads + dict["persona"]= chain por 4 linhas com `ollama_call_typed`. ~15 LoC removidas.
- `agents/thesis_synthesizer.py::synthesize` — substituiu json.loads + parsed.get(field, default) chain. Schema garante list shape para assumptions/triggers.
- `agents/holding_wiki_synthesizer.py::synthesize_wiki` — substituiu `requests.post(OLLAMA, ...)` direto (CH001 violation pré-existente) + json.loads. Eliminadas imports `requests` + `json`.

**Validação live (zero token Claude, qwen2.5:14b)**:
- KO Buffett (seed=42): BUY conviction 9 sizing large
- KO majority (n=3, seeds 42/137/314): 3/3 BUY conviction 9
- KO synthesize: 4 key_assumptions + 4 disconfirmation_triggers + intent populado

**Não fizemos** (deferred para W.6.2+): Instructor SDK no hot path (overhead OpenAI client > ganho — Ollama format=json + Pydantic já é 90% do valor); LangFuse self-host; promptfoo test suite; DSPy.

**Próximos sub-sprints W.6**:
- W.6.2 — promptfoo test suite (3 agents acima primeiro; 100% offline porque Ollama)
- W.6.3 — LangFuse self-host Docker (observability de prompts em prod)
- W.6.4 — DSPy piloto em risk_auditor (agent mais crítico; benchmark quality pre/pos)

### ✅ Sessão 2026-04-27 manhã — Workday Work (workday autónomo)

User saiu para o trabalho 8-9h ("Tudo que tens para fazer sozinho, pode prosseguir"). Foco em quick wins do midnight report + canonical refactors. Detalhe: [[Bibliotheca/Workday_Work_2026-04-27]].

**5 commits, 1998 LoC adicionados, 111 removidos, zero broken.**

**Highlights:**
- **REIT-aware dividend_safety** — O 25 RISK → 60 WATCH; PLD 35 RISK → 85 SAFE (FFO em vez de EPS no payout; ND/EBITDA softer thresholds para REITs).
- **Canonical `agents/_llm.py::ollama_call`** — refactored 5 modules (synthetic_ic, variant, thesis, earnings_prep, extract_insights). ~50 LoC saved.
- **Library `_common.py`** — chunk_text/file_hash/slugify shared across ingest.py + clippings_ingest.py.
- **Synthetic IC `--majority N=3`** — runs 3 seeds, majority verdict. Top-3 conviction unanimous BUY high (BBDC4/ITSA4/ACN).
- **MCRF11 → MCRE11** (Mauá Capital Real Estate) — Yahoo 404 fixed. MCCI11 (Papel) já cobria CRI side.
- **XPML11 corruption (issue #8)** — 3 corrupt rows deleted + new fetcher guards reject >50% intraday moves vs prior close.
- **Bibliotheca 33 alerts → 0** — bibliotheca_autofix backfilled 33 BR names; legacy section catalogued 13 orphans; K&A.yaml integrated as US universe extension.
- **code_health CH005-CH007** — 3 new checks (direct ollama URL, silent except, ad-hoc banner). 40 hits flagged.

### ✅ Sessão 2026-04-26 tarde — Phase L (BACEN + Quant + IC universe)

User saiu por 2h ("Pode atacar tudo. Força total"). Ataque concorrente em 3 frentes:

### ✅ Sessão 2026-04-26 tarde — Phase L (BACEN + Quant + IC universe)

User saiu por 2h ("Pode atacar tudo. Força total"). Ataque concorrente em 3 frentes:

**1. BACEN IF.Data fetcher** (`fetchers/bacen_ifdata_fetcher.py`):
- API Olinda OData → popular CET1, basel_ratio, RWA, NPL nos bancos
- Mapping crítico: Rel 5 (Capital) usa **Conglomerado Prudencial** + Tipo 1; Rel 8 (NPL) usa **Conglomerado Financeiro** + Tipo 2 (CodInst diferentes para o mesmo banco)
- BBDC4 + ITUB4 cobertos; BBAS3/SANB11 ainda pendentes (não estão em `library/ri/catalog.yaml`)
- Bug fix: `requests.get(params=)` substitui ` ` por `+` no $filter mas BACEN só aceita `%20`. Resolvido com `urllib.parse.quote(safe="")`
- Bug fix: DB lock contention via timeout=60 + retry exponencial 8x

**2. Phase W.11 Quant stack** (`analytics/quant_smoke.py`):
- Pkgs instalados: vectorbt, pyfolio-reloaded, alphalens-reloaded, empyrical
- Tearsheet: CAGR, Sharpe, Sortino, Calmar, MaxDD, correlation matrix
- HTML report Helena `ii_dark` standalone em `reports/quant_smoke_{br,us}_*.html`
- US: CAGR 18.3%, Sharpe 0.92, MDD -34%; BR: CAGR 6.6%, Sharpe 0.56, MDD -28% (winsorized)
- Winsorize 50% protege métricas contra data corruption (XPML11 case)

**3. Synthetic IC universe-wide** (`agents/synthetic_ic.py`):
- Flags novos: `--watchlist`, `--all`, `--skip-existing`, `--limit`
- 33 IC files antes → ~70+ no fim da sessão (em curso, ~3h Ollama qwen2.5:14b)
- Universo final esperado: ~180 tickers cobertos com 5-persona debate

**Material findings** (full timeline 2018-2025, 56/56 BACEN rows backfilled):
- **NPL gap ITUB4 vs BBDC4 quantificado**: 3.0pp (2018) → 5.8pp peak (2023-Q2) → 3.9pp (2024-Q4). ITUB4 absorveu o ciclo de cost-of-risk com 1/2 do impacto.
- **CET1 spread persistente** ~2pp em favor de ITUB4 (Q3 2025: 13.47% vs 11.39%).
- **Recovery assimétrica**: BBDC4 NPL -315bps desde peak vs ITUB4 -128bps — coerente com "ciclo a fechar mais agressivamente para o lado mais stressed".
- **Implicação rebalance**: data-driven support para reforçar ITUB4 sobre BBDC4. Não é "BBDC4 catch-up", é "ITUB4 num plano superior" desde 2018.
- **XPML11 data corruption descoberta** (3 dias com close ~R$1 quando deveria ser ~R$110, 14-16/Jan/2026). Issue Constitution #8 aberta.

### ✅ Sessão 2026-04-26 madrugada — closeout total Tier-2

Bulk thesis **completou 100% (184/184)**. Bank parser extension shipped (user/linter editou cvm_parser_bank.py adicionando 10 colunas + BACEN-target NULL columns; 50 rows populados com loan_book/pdd_reserve/coverage/CoR/E/A). Conviction score expanded universe-wide (33→184). Bug fix CRLF poison nos tickers (companies table tinha \r — strip aplicado em thesis perpetuum subjects()).

**Estado quantitativo final 26-04-2026:**
```
Thesis coverage:                 184/184 (100% universe)
conviction_scores:               184 total, 86 high (≥70)
bank_quarterly_history rows:     50 com novas BS columns populadas
code_health:                     178 subjects, 0 flags
Top-5 conviction:                BBDC4=92, ITSA4=90, ACN=87, JPM=83, PG=82
```

**Material findings:**
- BBDC4 NII trajetória clara: cost-of-risk peak Q4 2023 (5.14% YTD) → 2.9% Q3 2025 (ciclo a normalizar)
- BBDC4 coverage ratio comprimindo 9% → 6.3% (provisões a esgotar — sinal de qualidade improving OU complacência)
- 86 de 184 tickers em high-conviction zone (47%)

### 📊 Estado quantitativo (snapshot fim de sessão)

```
Holdings com thesis:               33/33 (100%)
Wiki/holdings/ coverage:           34/33 (10 stubs auto_draft:true)
Open watchlist_actions:            18 (era 98)
Active perpetuums:                 9/10 (library_signals frozen)
T2+ perpetuums:                    4 (vault, ri_freshness, content_quality, token_economy)
thesis perpetuum subjects:         184 (33 holdings + 151 watchlist)
Constitution open issues:          5 (eram 7)
predictions table eval cron:       wired (primeiros fechos Jul 2026)
paper_trade_close cron:            wired (primeiros fechos May 2026)
Telegram push cron:                wired (daily 23:30, --silent)
code_health:                       176 subjects, 0 flags ✓
```

### 🎯 Próxima ordem de prioridade (Tier-2)

1. **Variant_perception source-weighting** — predictions infra já está wired (G2). Integrar win_rate como peso em `agents/variant_perception.py::magnitude_calc()`. **Bloqueado** até primeiros predictions fecharem (~Jul/2026 quando horizons expirarem). Building infra agora seria dead code 3 meses.

2. **BACEN fetcher** para popular CET1/RWA/basel_ratio/npl_ratio (4 cols NULL hoje). Schema já existe (`bank_quarterly_history`); falta scrape do site BACEN ou 4-pillar reports. Pure code, ~2-3h.

3. **Synthetic IC para watchlist** (151 tickers × 5 personas × ~30s = ~6h Ollama). Geraria IC_DEBATE.md para todos os tickers com thesis, completando o 5-persona signal universe-wide. Risk: longo, supervisionado.

4. **Variant_perception para watchlist** (151 tickers, ~30min Ollama por batch). Mas só funciona se ticker tem analyst_insights — muitos watchlist não têm.

5. **Phase W gold skills** (precisam user input):
   - W.2/W.5/W.10: Tavily / Firecrawl / Bigdata MCP — **precisa API keys**
   - W.7: Google Calendar/Drive — **precisa OAuth no browser**
   - W.6: Observability (LangFuse/Instructor/DSPy) — pure infra
   - W.11: Quant stack (pyfolio/vectorbt/Alphalens) — pure infra

6. **Catalog expansion** — 36 BR tickers em universe.yaml mas NÃO em catalog.yaml (22 stocks + 14 FIIs). Auto-populator tem track-record 60% accuracy (AXIA7 fail). **Precisa user-supervised** validação de CVM codes.

7. **Watchlist deep wiki Phase B.3** — 50 priority watchlist names com thesis light. **Precisa user**: lista de prioridades.

8. **Review humana dos 10 wiki/holdings auto_draft** (não-urgente).

### 🚫 Que NÃO fazer (token economy)

- Não spawn sub-agents para audits — última sessão já fez audit completo (4 agents paralelos, ~150K tokens)
- Não re-ler Constitution inteiro — esta secção tem o essencial
- Não criar mais scripts de planeamento — execute direct
- Não duplicar Phase F/G/H/I work — já feito

### 🔧 Comandos canónicos para inspecionar estado

```bash
# Verificar bulk progress
tail -30 logs/thesis_bulk_*.log

# Quantos thesis valid agora
.venv/Scripts/python.exe -c "import sqlite3; c=sqlite3.connect('data/br_investments.db'); print(c.execute(\"SELECT COUNT(*) FROM perpetuum_health WHERE perpetuum_name='thesis' AND score>=0 AND run_date=(SELECT MAX(run_date) FROM perpetuum_health WHERE perpetuum_name='thesis')\").fetchone())"

# Open actions
.venv/Scripts/python.exe -c "import sqlite3; print(sum(sqlite3.connect(d).execute(\"SELECT COUNT(*) FROM watchlist_actions WHERE status='open'\").fetchone()[0] for d in ['data/br_investments.db','data/us_investments.db']))"

# Code health
.venv/Scripts/python.exe -c "from agents.perpetuum.code_health import CodeHealthPerpetuum; p=CodeHealthPerpetuum(); print(f'{sum(1 for _ in p.subjects())} subjects, {sum(1 for s in p.subjects() if 0<=p.score(s).score<100)} flags')"

# Captain's Log dashboard
scripts\launch_dashboard.bat   # browser → Captain's Log

# Manual Telegram brief
.venv/Scripts/python.exe scripts/captains_log_telegram.py --dry-run
```

### 💡 Hint para próxima sessão

Se o bulk completou e há nova thesis_health data, o **maior leverage** é #2 (variant_perception source-weighting) — é tudo backend, sem precisar do user, e fecha o loop de "we vs consensus" que está hoje a usar weights uniformes. ~30-60 min de trabalho.

---

## 🎯 Identity & Purpose

Sistema pessoal de inteligência de investimentos para **um investidor pessoa física** a operar em duas geografias:

- 🇧🇷 **Brasil (B3)** — 12 holdings (5 stocks + 5 FIIs + 2 ETFs)
- 🇺🇸 **EUA (NYSE/NASDAQ)** — 21 holdings

**Estratégia core**: DRIP (Dividend Reinvestment Plan) com filosofia Buffett/Graham — quality compounders + margem de segurança + dividendos consistentes.

**Horizon**: long-term (anos, não meses).

**User profile**: vibe coder. Comandos terminal são deslike; prefere ler resultados em Obsidian/HTML/dashboards. Decisões são tomadas com clareza visual + contexto.

## 🛡️ Os 7 não-negociáveis (constitutional rules)

> **Princípio de superfícies (2026-04-26)**: Terminal/CLI = **sala do chefe**
> (acção directa, raw, sem cerimónia). Obsidian + desktop app + reports HTML =
> **Escritório** (consumível, polido, narrável). Helena Design System aplica-se
> ao Escritório. CLI optimiza para velocidade, não estética.

1. **In-house first** — Tudo que rode localmente (SQL, Ollama, scripts) NÃO usa tokens Claude. Claude é último recurso. Esta é a meta-regra que governa todas as outras.

2. **Carteiras isoladas** — Dinheiro USD fica em US, BRL em BR. Nunca sugerir conversão entre contas.

3. **Paper-trade antes de real capital** — Qualquer signal novo (library methods, perpetuums) entra em `paper_trade_signals`. Real capital só após 30+ closed signals com win_rate >60%.

4. **Honest projections** — Em forward scenarios, evitar assumptions optimistas. Aplicar damper quando histórico >> Gordon.

5. **Tier-gated autonomy** — Perpetuums escalam T1→T2→T3→T4→T5 com base em estabilidade comprovada (30d sem false positives). User aprova promoção.

6. **Tickers blacklist** — Memória persistente:
   - **TEN**: 4 sinais cycle peak Apr 2026 → NUNCA adicionar
   - **GREK**: dividendos irregulares → NÃO aplicar lógica DRIP

7. **Verification before completion** *(2026-05-06, importado de obra/superpowers)* — Nenhuma claim de "done" sem evidência fresca: comando executado, output capturado, teste verificado. Aplica-se a perpetuum action_hints (T2+), implementações autónomas overnight/workday, e respostas a pedidos de status. Anti-padrão proibido: declarar trabalho concluído baseado em raciocínio sobre o que *deveria* funcionar. Operacionalização: cada commit autónomo precisa de 1 linha de evidência (test pass / sql query / dry-run output) no body.

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

#### Z.8 — Helena Design System (2026-04-25 noite)

Phase paralela após sprints 0-7: hire de **Helena Linha** (Head of Design) + sistema visual fechado.

| Sessão | Output | Artefactos |
|---|---|---|
| s1 | Plotly template `ii_dark` + dark CSS injection + sidebar brand | `scripts/_theme.py` (304 LOC) |
| s2 | Design System v1.0 (5 princípios + UX agentic patterns + 8 anti-padrões) + 5 componentes reutilizáveis + 8 `st.metric` → `kpi_tile()` (Portfolio + Verdict) | `obsidian_vault/skills/Design_System.md`, `scripts/_components.py` (163 LOC) |
| s3 | **14 `st.metric` raw → `kpi_tile()`** em 6 pages (Actions Queue, Perpetuum Health, Paper Signals, RI Timeline, YouTube, Screener). Tones semânticos: warning para coisas que pedem atenção, positive/negative para deltas YoY, accent para counts informacionais. `grep '\.metric('` agora devolve **0 matches** | `scripts/dashboard_app.py` |
| Continuous | `scripts/design_research.py` — weekly Sunday scout de novos design skills (GitHub + 5 RSS) | `obsidian_vault/skills/Design_Watch.md` |

**Princípio constitucional emergente**: "Engenheiros não escolhem cores." Toda nova UI passa por `_components.py`; `Tone Literal` torna paletas fora-do-design impossíveis em compile-time.

**Próximo gap conhecido**: `st.bar_chart` em YouTube usa azul default fora da paleta — refactor para `px.bar(template="ii_dark")`.

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
| 2026-04-25 | Helena Linha hired (Head of Design) — toda UI nova passa por design review | Sem cadeira dedicada, cada feature herdava estilo do engenheiro que a escreveu |
| 2026-04-25 | `_components.py` + `Tone Literal` como compile-time guard contra cores ad-hoc | "Engenheiros não escolhem cores"; paleta restrita é não-negociável |
| 2026-04-26 | Mega Helena (`agents/helena_mega.py`) ship — pipeline audit+curate+spike+report | User: "vamos fazer a mega Helena"; consolidar Helena num único orchestrator |
| 2026-04-26 | **Princípio de superfícies**: Terminal=sala-do-chefe, Obsidian/desktop=Escritório | User: "O terminal é a sala do chefe, o Obsidian é o Escritório" — cada superfície optimiza para o seu uso |
| 2026-04-26 | Path B (Tauri desktop app) escolhido para Phase Z UI | "O mais elaborado"; tecto 10/10, reusa 100% backend Python via FastAPI sidecar |
| 2026-04-26 | CLI `ii *` mantém-se intacto independentemente do Path B | Princípio das superfícies — Tauri é Escritório, não substitui sala-do-chefe |
| 2026-05-06 | Adoptar 4 slash commands externos (security-review + 3 superpowers) em `.claude/commands/` | Editorial value alto, custo zero (só invocados on demand); reforça verification-before-completion |
| 2026-05-06 | Adicionar CI workflows (`.github/workflows/test.yml` + `codeql.yml`) | Repo era zero-CI; pytest + CodeQL gatekeep main sem custo recorrente; complementa `code_health` perpetuum (CH at PR-time vs cron-time) |
| 2026-05-06 | DS010 + CH008 — skill files >500 lines warn (best practice Anthropic) | Progressive disclosure principle; Helena audit + code_health perpetuum cobrem cron + linter |
| 2026-05-06 | 7º não-negociável — "Verification before completion" | Importado de obra/superpowers; reforça anti-padrão LLM "I'm done sem evidência" que CLAUDE.md "Goal-driven execution" já apontava |
| 2026-05-06 | claude-mem (cross-session memory passive) — **skip** | Existing file-based memory mais auditável + git-backed; AGPL/PolyForm sub-deps adicionais |
| 2026-05-06 | gstack (Garry Tan agentic framework) — inspiração only | Mission Control já tem scaffold; cherry-pick é DESIGN_TASTE.md (preference journal lightweight) |

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

1. ~~**Watchlist BR auto-populator ~40% match errado**~~ ✅ RESOLVIDO 2026-04-26. Phase FIX corrigiu 5 (ITUB4, SUZB3, TTEN3, EQTL3, ENGI11); sessão 26/04 validou + corrigiu os restantes 10 (AXIA7 CVM 3328→2437; PGMN3 sector Consumer Staples→Healthcare; outros 8 confirmados correctos). Catálogo `library/ri/catalog.yaml` agora sem `auto_populated: true`.
2. ~~**RBRX11 não resolvido** no FII module.~~ ✅ RESOLVIDO. Verificado 2026-04-26: `fii_monthly` tem 24 rows para RBRX11 (AUTO_RUN_REPORT estava certo).
3. ~~**fii_monthly DY display em decimal vs %**~~ ✅ RESOLVIDO 2026-05-08. `library/ri/fii_filings.py::show()` agora multiplica `dy_mes_pct` e `rentabilidade_efetiva_mes_pct` por 100 antes de display (decimais armazenados, percentagens mostradas). Verificado live: BTLG11 mostra 0.659%/0.729%/etc em vez de 0.01.
4. **Frontend é tudo CLI** — user vibe-coder não consegue ler outputs facilmente. **PHASE Z proposed**: UI friendly layer.
5. ~~**ITRs 2019-2023 não baixados**~~ ✅ RESOLVIDO. Verificado 2026-04-26: `quarterly_history` tem 60 ITRs por ano de 2018-2025 (AUTO_RUN_REPORT estava certo, esta entry estava obsoleta).
6. ~~**Bank-specific schema** (BBDC4/ITUB4)~~ ✅ RESOLVIDO 2026-05-08 (verificação). `bank_quarterly_history` tem 30 colunas BACEN (cet1, basel, rwa, npl, nim_proxy, cost_to_income, etc); BBDC4 mais recente (2025-09-30) tem 29/30 populadas (só NPL null), ITUB4 26/30. `library/ri/cvm_parser_bank.py` (ds_conta-based, Phase L) já cobre o que esta issue pedia. Open: NPL ratio recency gap (último valor para BBDC4/ITUB4 é 2024-12-31; BACEN publica com lag).
7. **Quarterly_single para watchlist novos** — parcialmente resolvido 2026-05-08. `library/ri/catalog_autopopulate apply` adicionou POMO3+POMO4 (Marcopolo). PLPL3 fica MISS (CAD CVM não tem "PLANO E PLANO" exact match). Outros 13 watchlist non-FII non-bank (BBSE3, WIZC3, UNIP6, SEER3, SLCE3, TUPY3, EGIE3, VAMO3, KLBN4, PNVL3, SIMH3, GMAT3, TIMS3, VIVA3) **fora do scope** do autopopulate actual. Investigar porquê o autopopulate só validou 19 do total 67 watchlist.
8. ~~**XPML11 data corruption**~~ ✅ RESOLVIDO 2026-04-27 (Workday Work). 3 rows deletadas + log em events table. Fetcher guard `_is_suspicious_close` adicionado a yf_br_fetcher + yf_us_fetcher (rejeita >50% intraday move sem split na history). Future glitches handled durably.
9. ~~**BBAS3/SANB11 fora do BACEN map**~~ ✅ MAIORITARIAMENTE RESOLVIDO 2026-05-08 (verificação). `config/bank_codinst.yaml` já tem **BBDC4 + ITUB4 + ABCB4 + BBAS3 + BPAC11** (added 2026-04-26). BBAS3 tem 32 rows em `bank_quarterly_history` com CET1/Basel/RWA até 2025-12-31. Apenas **SANB11** continua sem entry — é watchlist-only (não detido), low priority. Adicionar requer descoberta manual de CodInst via IfDataCadastro endpoint.
10. **Longitudinal validation data — primeira amostra capturada** (Phase FF). 31 verdicts originais (2026-04-23) → 29 fechados em window de 11 dias com benchmark + sector cmp (Bloco 1.1 shipped 2026-05-05). Calibration curve US n=20: bin 60-80 hit rate 25%, bin 80-100 hit rate 100% (n=1). BR n=9: maioria HOLD com retornos modestos vs IBOV. **Ainda muito cedo** para validação real — janela de 11 dias é ruído, não signal. Próximo: window 30d em ~3 semanas, 90d em Aug/2026.
11. ~~**Benchmark prices ausentes**~~ ✅ RESOLVIDO 2026-05-05. SPY (501 rows) + BOVA11 (499 rows) + 11 sector ETFs US (XLK/XLV/XLF/XLE/XLI/XLY/XLP/XLB/XLRE/XLU/XLC, 501 rows cada) — todos com 2 anos de história. **TODO**: wire em `daily_run.bat` para refresh diário (hoje só foi backfill one-shot).
12. ~~**`WATCH` action no `verdict_history`**~~ ✅ RESOLVIDO 2026-05-08. Era doc drift: `verdict.py` linhas 276-282 produz **vocabulário 6-stance** desde sempre — `BUY` (not held + score≥7), `ADD` (held + score≥7), `WATCH` (not held + borderline 6-7), `HOLD` (held + borderline), `AVOID` (not held + score<4), `SELL` (held + score<4) — mais `SKIP` (not held + mid 4-6, "no opinion"). `analytics/decision_quality.py::_accuracy()` já tratava `WATCH`/`HOLD` como NEUTRAL e `BUY`/`ADD` como BULLISH (linhas 111-113). Apenas o Constitution listava 4 stances incorrectamente. Resolução: docstring de `decision_quality.py` actualizada para formalizar 6-stance + SKIP. SKIP fica intencionalmente sem accuracy (`None,None`) porque é ausência de veredito, não veredito calibrável. Os 10 rows WATCH (4 BR + 6 US) e 1 row SKIP (ABBV) ficam preservados.

## 📄 Reports gerados

```
PHASE_Y_REPORT.md       — Y v1 (manhã 25/04)
PHASE_Y8_REPORT.md      — Y.8 expansão (tarde 25/04)
MORNING_REPORT.md       — Overnight 24→25
```

Plus 26+ docs em `obsidian_vault/skills/` e 5 timelines em `obsidian_vault/tickers/*_RI.md`.

## 🔮 Phase U — Unification (em curso, 2026-04-26)

**Decisão arquitectural confirmada**: brain = 3 camadas, não 1 só.

```
L1 — VERDADE (SQLite + YAML)            ← scripts read/write, humano não toca
L2 — PROJECÇÃO (vault auto-gerada)       ← regenerable, frontmatter tipado
L3 — NARRATIVA (vault humano-escrita)    ← sagrado, scripts NÃO sobrescrevem
```

**Surfaces consolidadas (3 papéis claros, 0 sobreposição):**
- **CLI `ii`** = sala do chefe (acção raw)
- **Streamlit** = cara (projecção interactiva sobre L1)
- **Obsidian** = cérebro (L1 + L2 + L3, leitura profunda)

**Mortos formalizados**:
- React/Vite desktop → `_deprecated/desktop_2026-04-26/` (zombie processes killed, node_modules removidos)
- HTML reports estáticos → continuam mas não-prioritários

**Roadmap Phase U** (7 sprints curtos):

| Sprint | Nome | Status | O que entrega |
|---|---|---|---|
| **U.0** | Sweep + 3-layer formalisation | ✅ SHIPPED | Root limpo (PHASE/HANDOFF moves), React deprecated, `_LAYER.md` markers, `helena.css` snippet, `vault_autocommit.bat` |
| **U.1** | Home minimalista (Apple Newsroom-style) | pending | Streamlit Home: 1 KPI hero + Captain's Log + Ask box + 3 cards. Resto colapsa em "More". |
| **U.2** | Streamlit consolidation | pending | Páginas redundantes mortas, navegação plana ≤5, mobile breakpoints. |
| **U.3** | Ask box wired | pending | Text input → `library.rag ask` → markdown render + sources expandíveis. |
| **U.4** | Action loop visual | pending | T2 actions na Home (não enterradas). Approve/reject buttons → `perpetuum_action_run.py`. |
| **U.5** | Charts com identidade | pending | Helena Linha enforced em todos plotly. `chart_with_benchmark()` helper. |
| **U.6** | Telegram visual card | pending | matplotlib (Helena tokens) → PNG card diário. Push 08:00 cron. |
| **U.7** | Obsidian = cérebro | pending | Home.md vault redesenhada; Dataview upgrades; Charts embeds; Syncthing setup mobile. |

**Os 3 riscos mitigados (ver decisão U.0):**
1. Dataview die → script Python regenera blocos estáticos
2. Vault scaling → `_archive/YYYY/` policy via bibliotheca perpetuum
3. Bidirectional editing → header `<!-- AUTO -->` + perpetuum diff-detect

## 🏁 Phase FF — Calibration Loop (em curso, 2026-05-05)

**Trigger**: external AI critique em 4 rondas (`EXTERNAL_AI_BRIEFING*.md`). Crítica central: sistema produz outputs eloquentes (verdicts, dossiers, IC debates) mas **nunca foi validado contra a realidade**. Sem closed-loop, o sistema é "confirmation bias engine" potencial.

**Objetivo**: construir infraestrutura de closed-loop validation. **Não** deployar capital nesta phase.

**4 attack vectors absorvidos**:
1. **Calibration Void** — `verdict_history` é populada mas nunca cruzada com forward returns + benchmarks.
2. **Latent Space Echo Chamber** — Synthetic IC (5 personas) usa só Qwen 14B; mudar prompt não muda latent space.
3. **Decorator Macro Engine** — macro classifier observa mas hedge weight rígido a 10% torna-o ornamental.
4. **L1 Data Quicksand** — yfinance pode corromper retroactivamente; CVM bank parser via `ds_conta` é frágil.

**Roadmap (3 semanas, 15 dias)**:

| Bloco | Sprint | Status | Entrega |
|---|---|---|---|
| **1.1** | Decision Quality Engine + benchmark cmp | ✅ SHIPPED 2026-05-05 | `scripts/migrate_decision_quality.py` (+11 cols + `verdict_engine_breakdown` table). `analytics/decision_quality.py` (4 cmds: update/calibration/post-mortem/engine-attribution + reset-accuracy). Backfill: SPY+BOVA11+11 sector ETFs (~5500 rows, 2y). Wired no `daily_run.bat`. 29/31 verdicts fechados em window 11d (window real fica activo após 30d). |
| **1.2** | Verdict Engine Breakdown | ✅ SHIPPED 2026-05-05 | `scripts/verdict_history.py::record_verdict` agora popula 4 sub-engines (quality/valuation/momentum/narrative) com weight + per-engine verdict band. Backfill: 124 breakdown rows expandidas dos 31 verdicts existentes. **Finding empírico crítico** (n pequeno mas direccional): valuation engine BUY 0% hit US (n=3) / 16.7% BR (n=6) — primeiro sinal mensurável do "Buffett/Graham buy bias" que o external critique previu. |
| **2.1** | Synthetic IC Multi-Model (3 famílias) | ✅ SHIPPED 2026-05-05 | `agents/synthetic_ic.py` refactored — Buffett/Klarman→Qwen 32B, Druck/Dalio→Qwen 14B, Taleb→**Gemma 4 31B** (família diferente, llama3.3:70b não instalado). Helper `_resolve_model()` faz fallback gracioso para Qwen 14B se modelo preferido ausente. Schema fix: `_lower_size` validator agora extrai keyword (32B é verbose). Live test KO: 2 BUY (Buffett/Dalio) / 1 HOLD (Druck) / 2 AVOID (Taleb/Klarman) — diversidade epistemológica real. |
| **2.2** | L1 Anomaly Detector (Benford+MAD) | ✅ SHIPPED 2026-05-05 | Estendido `analytics/data_anomalies.py` com 2 novos detectores: (a) `detect_benford_violations` chi-square agregado em market_cap/shares_outstanding (3 metrics, n=72-107). Resultado: 0 violations — dados clean. (b) `detect_cross_sectional_outliers` MAD em log(P/E) por sector (threshold 3.5σ). Resultado: 7 outliers genuínos (BPAC11, PLTR, ABBV, BN, NFG, GPC, TSLA). Wired no `daily_run.bat`. |
| **3.1** | Provenance Tracking | pending | `provenance` table + fetcher patches |
| **3.2** | Tier Clarification | pending | T1-T5 → OBSERVE/PROPOSE/EXECUTE + `config/action_safety.yaml` (touches 12 perpetuums — pede user review antes) |
| **3.3** | yfinance SPOF Mitigation | partial | Benchmark fallback já parcialmente activo via `refresh_benchmarks.py`. Spot-check cron + cache TTL yaml ainda pending. |

**Bloco 4 deferred**: **Phase GG (Capital Deployment Engine)** — só arranca após ≥90 dias de Phase FF rodando + calibration curve estável + hit rate por engine claro. Tentar deployar antes seria retrofit.

**Critério "done" Phase FF**:
- Calibration curve com ≥30 observações fechadas
- Hit rate per-engine respondível
- Sector tilt da carteira recomendada vs benchmark mensurável
- Synthetic IC com 3 model families em produção
- Benford + MAD a correr como perpetuum T1
- Resposta concreta à pergunta "evidência empírica que não é confirmation bias?"

**Phase FF Decision Log**:

| Data | Decisão | Racional |
|---|---|---|
| 2026-05-05 | Bloco 4 (capital deploy) deferred → Phase GG, prereq ≥90d validated verdicts | Validar **antes** de capital. Tentar fazer ambos em 4 semanas seria confirmation bias retrofit |
| 2026-05-05 | IC multi-família = Qwen 32B + Qwen 14B + Llama 70B (não deterministic-as-persona) | Promover scoring engine a "persona" do IC seria circular — usamos engine para validar engine |
| 2026-05-05 | Benford check chi-square agregado, não per-ticker first-digit-9 flag | Implementação correcta: distribuição de primeiros dígitos numa amostra grande, não valor individual |
| 2026-05-05 | Cross-sectional outlier via MAD (Median Absolute Deviation), não z-score sobre PE raw | PE é heavy-tailed/lognormal; z-score com std populacional produz false positives em tech/biotech |
| 2026-05-05 | Estender `analytics/data_anomalies.py` (Benford+MAD) em vez de criar novo perpetuum dedicado | Já existe + scaffolding (PRICE_JUMP/STALE/FUND_STALE); adicionar 2 detectors é menos cruft |

## 📝 Changelog

| Data                              | Phase            | Mudança principal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Tokens Claude pipeline |     |
| --------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------: | --- |
| 2026-04-24 morning                | W                | Skills arsenal evaluated, baseline frozen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                      0 |     |
| 2026-04-24 afternoon              | X                | Perpetuum engine (3 perpetuums initial)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                      0 |     |
| 2026-04-24 evening                | X+Lib            | 4 books ingested, RAG built, 154 paper signals                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                      0 |     |
| 2026-04-24 night                  | Overnight        | 5 phases autónomas: thesis populate, methods, RAG batch                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                      0 |     |
| 2026-04-25 morning                | Y                | RI Knowledge Base v1 (CVM pipeline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                      0 |     |
| 2026-04-25 afternoon              | Y.8              | Single-Q view, DFP backfill, FII module, watchlist auto                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                      0 |     |
| **2026-04-25 evening**            | **Constitution** | **Este documento criado**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                      0 |     |
| 2026-04-25 late evening           | **AA**           | Critical Thinking Stack: Synthetic IC (5 personas), Variant Perception, Earnings Prep cockpit, Portfolio Stress, Decision Journal Intelligence                                                                                                                                                                                                                                                                                                                                                                                |                      0 |     |
| 2026-04-25 night                  | **FIX**          | Quick-fixes: 5 watchlist matches corrigidos manualmente; variant_perception substring bug ("trim" matchava "patrimonial") → word-boundary regex; bank schema BBDC4+ITUB4 (`cvm_parser_bank.py` ds_conta-based). +15 tickers em quarterly_history, +26 bank rows, 4→0 HIGH variance falsos                                                                                                                                                                                                                                     |                      0 |     |
| 2026-04-25 afternoon (autonomous) | **AUTO**         | **11 sprints autónomos** (user out 3h): ITRs 2019-2023 backfill (+292 quarterly rows), Synthetic IC × 33 holdings, vault timelines × 20 tickers, bank single-Q view, earnings prep 60d, perpetuum master full run (3,665 subjects scored), conviction scoring engine (composite 0-100), `library/ri/catalog.py` canonical accessor (eliminou bug recorrente "watchlist not in loop"), compare_releases→quarterly_single (sem YTD distortion), RBRX11 ingerido (5/5 FII holdings). Top conviction: ITSA4 90, ACN 86, BBDC4 76. |                      0 |     |
| 2026-04-25 evening                | **Z (UI)**       | Sprints Z.0-Z.7: 7 dashboard pages novas (Actions Queue, Ask Library, Perpetuum Health, Paper Signals, RI Timeline) + Home.md morning landing + `start_dashboard.bat` one-click launcher. ~440 LOC. |                      0 |     |
| 2026-04-25 night                  | **Z.8 Helena s1-s2** | Helena Linha hired (Head of Design). `_theme.py` (plotly `ii_dark` + dark CSS + brand sidebar). Design_System v1.0 + `_components.py` v1 (5 helpers). 8 `st.metric` raw → `kpi_tile()` (Portfolio + Verdict). `design_research.py` weekly scout. |                      0 |     |
| **2026-04-25 night**              | **Z.8 Helena s3** | **14 `st.metric` raw → `kpi_tile()`** em 6 pages (Actions Queue, Perpetuum Health, Paper Signals, RI Timeline, YouTube, Screener). Tones semânticos: warning para attention items, positive/negative para YoY, accent para counts. `grep '\.metric('` = 0 matches. Compile-time enforcement de paleta via `Tone Literal`. |                      0 |     |
| 2026-04-26 afternoon              | **L (BACEN+Quant+IC)** | **Phase L shipped autonomously (user out 2h).** (1) `fetchers/bacen_ifdata_fetcher.py` — Olinda OData → CET1/Basel/RWA/NPL, BBDC4+ITUB4 cobertos. URL-encoding bug fix + retry-on-lock 8×. (2) **W.11 Quant stack** — vectorbt/pyfolio-reloaded/alphalens-reloaded/empyrical instalados; `analytics/quant_smoke.py` produz tearsheet + HTML Helena. US Sharpe 0.92, BR Sharpe 0.56 (winsorized). (3) **Synthetic IC universe-wide** — flags `--watchlist`/`--all`/`--skip-existing`/`--limit`; 33 → ~70+ ICs (mid-run, ~3h Ollama). (4) **XPML11 data corruption descoberta** (issue #8). | 0 | |
| 2026-04-25 night                  | **Z.8 Helena s4**    | **Live launcher + Claude Design avaliação.** `scripts/launch_dashboard.bat` idempotente (detecta porta 8501; arranca minimizado com `--server.runOnSave true` para hot-reload em qualquer save). Desktop `.lnk` aponta a `.bat` versionado em git → atalho não fica obsoleto. `obsidian_vault/skills/Claude_Design_Integration.md`: research preview Anthropic Labs avaliada — web-only, sem API; workflow proposto = Helena prototipa em claude.ai (com Design_System como contexto) → handoff Claude Code → implementação Streamlit reusando `_components.py`. Política dura: nunca HTML directo para produção. |                      0 |     |
| 2026-04-25 (CATALOG_FIX)          | **CATALOG_FIX**  | Watchlist BR auto-populator validado: 10/10 tickers `auto_populated: false` agora; AXIA7 CVM 3328→2437 (subsidiária Nordeste→holding), PGMN3 sector Consumer Staples→Healthcare (rede farmácias). 6 RI URLs preenchidos (CPLE3/B3SA3/MULT3/RENT3/MOTV3/ALOS3/RDOR3 etc.). | 0 | |
| 2026-04-25 (BB)                   | **BB**           | 10º perpetuum `code_health` (170 subjects scan, AST/regex CH001-CH004). Apanhou 4 issues no caminho — corrigi: ri_freshness 5→20 subjects, cvm_codes.validate_catalog (root cause AXIA7 hidden), 2 dead CATALOG constants. T1 Observer. | 0 | |
| 2026-04-25 (CC)                   | **CC**           | Captain's Log unified Streamlit page (primeira nav). 6 secções: Pulse, Top Conviction, Decisions Pending, Committee Latest, Variant View, RI Material Changes, Alerts. Componentes novos: `story_card()`, `verdict_pill()`. Data layer puro `_captains_log.py`. | 0 | |
| **2026-04-25 (F — T0 cleanup)**   | **F**            | **F1** `paper_trade_close.py` (cron wired) — sem este, win_rate undefined eternamente. **F2** Engine `enabled` flag; library_signals FROZEN; content_quality+token_economy promovidos T2; vault threshold 50→30. **F3** Bulk-ignore 80 vault drift actions BR (98→18 open). **F4** Thesis perpetuum subjects 33→184 (companies UNION watchlist, 156 sentinels visíveis). | 0 | |
| 2026-04-25 (G)                    | **G**            | Holdings thesis 100% (28→33): `agents/thesis_synthesizer.py` Ollama Qwen 14B local com philosophy-aware prompt (BR/BR_BANK/FII/US/REIT/ETF). 5 holdings escritos: XPML11, GREK, GS, HD, O. Bug fix line-based parser (regex catastrophic backtracking pré-fix). `predictions_evaluate.py` shipped (counterpart paper_trade_close). Wiki Phase C.2 `Analyst_Tracking.md` documenta schema `predictions` que já existia. Constitution open issues #2 RBRX11 + #5 ITRs verified resolved. | 0 | |
| 2026-04-25 (H)                    | **H**            | Telegram morning brief: `scripts/captains_log_telegram.py` empacota Captain's Log em push compact (~1160 chars), wired em `daily_run.bat`. Mobile-friendly, semantic emojis (🟢🟡🔴 score, BUY/HOLD/AVOID). Underscore-escaping bug fix (Telegram Markdown). | 0 | |
| 2026-04-25 (I)                    | **I**            | Wiki holdings B.2 closeout: `agents/holding_wiki_synthesizer.py` gera `wiki/holdings/<TICKER>.md` AUTO-DRAFT marcado para 6 holdings ainda sem nota deep (ABBV, GS, PLTR, TSLA, XP, GREK). Reusa context layer + portfolio_positions data + philosophy-aware prompt. | 0 | |
| **2026-04-26 evening**            | **U.0 (Unification Sweep)** | **3-layer brain formalisado.** (1) `desktop/` (React app + Vite + FastAPI sidecar) → `_deprecated/desktop_2026-04-26/`; 2 zombie processes killed (Vite 1420 + FastAPI 8765); node_modules apagados. (2) Root limpo: 11 ficheiros (PHASE_*_REPORT, HANDOFF*, MORNING_REPORT*, AUTO_RUN_REPORT) → `reports/_phases/`. (3) `.gitignore` actualizado: `node_modules/`, `_deprecated/`. (4) `_LAYER.md` markers em 11 vault folders (3 L2 + 8 L3). (5) `obsidian_vault/.obsidian/snippets/helena.css` espelha `_theme.py` tokens (paleta + tipografia + tabelas + callouts + sidebar). (6) `scripts/vault_autocommit.bat` pronto (Scheduled Task pendente confirmação user). | 0 | |
| **2026-04-27 morning**            | **Workday Work** (autonomous) | 5 commits, ~120 min. (1) **REIT-aware dividend_safety**: O 25 RISK → 60 WATCH; PLD 35 RISK → 85 SAFE (FFO + softer ND/EBITDA). (2) **Canonical `agents/_llm.py::ollama_call`**: refactored 5 modules (synthetic_ic, variant, thesis, earnings_prep, extract_insights), ~50 LoC saved. (3) **`library/_common.py`**: chunk_text/file_hash/slugify shared (ingest + clippings dedup). (4) **Synthetic IC `--majority N=3`**: ask_persona_majority + CLI flag; top-3 conviction unanimous (BBDC4/ITSA4/ACN BUY high). (5) **Fetcher guards**: BR + US `_is_suspicious_close` rejects >50% intraday moves. **Issue #8 (XPML11) resolved** — 3 corrupt rows deleted. (6) **MCRF11 → MCRE11** (Yahoo 404 fix). (7) **Bibliotheca 33 → 0 alerts**: autofix 33 names; legacy section catalogues 13 BR orphans; K&A.yaml integrated as US universe extension. (8) **code_health CH005-CH007**: 3 new checks (direct ollama URL, silent except, ad-hoc banner). 40 hits flagged. Detalhe: [[Bibliotheca/Workday_Work_2026-04-27]]. | 0 | |
| **2026-05-05** | **FF — Calibration Loop initiated** | Phase FF formalised after 4 rounds of external AI critique. Roadmap em 3 blocos / 15 dias. Bloco 4 (Capital Deployment) deferred → Phase GG (prereq ≥90d validated verdicts). Bloco 1.1 em curso: schema migration `verdict_history` (+8 outcome columns + `verdict_engine_breakdown` table) + `analytics/decision_quality.py` com benchmark comparison. Open issues #10 (no longitudinal validation data) + #11 (benchmark prices ausentes — SPY/BOVA11 zero rows). Briefing externo + replies em `EXTERNAL_AI_BRIEFING*.md` no root. | 0 | |
| **2026-05-05 night** | **FF — Blocos 1.1, 1.2, 2.1, 2.2 SHIPPED** | Sessão autónoma extensa (5/7 sprints fechados). (1) **Migration + decision_quality.py** com `update`/`calibration`/`post-mortem`/`engine-attribution`/`reset-accuracy`. (2) **Benchmark backfill**: SPY + BOVA11 + 11 sector ETFs US (~5500 rows, 2y). Wired em `daily_run.bat` via `refresh_benchmarks.py`. Open issue #11 fechado. (3) **Engine breakdown**: 124 rows backfilled. **Finding empírico**: valuation BUY 0% hit US (n=3) — primeiro sinal mensurável de "Buffett/Graham buy bias" previsto pelo critique externo. (4) **Multi-família IC**: Buffett/Klarman→Qwen 32B, Druck/Dalio→Qwen 14B, Taleb→Gemma 31B (família Google ≠ Alibaba). Schema fix `_lower_size` validator. Live test KO: 5 personas / 3 verdicts distintos / 3 backends. (5) **Benford+MAD**: 0 Benford violations (clean data) + 7 cross-sectional outliers (BPAC11, PLTR, ABBV, TSLA, BN, NFG, GPC). (6) **WATCH/ADD/SKIP** vocabulary alignment em `_accuracy()`. Total 5 ficheiros novos, 4 ficheiros estendidos, ~700 LoC. Não-commitado. | 0 | |

## 🧭 Como usar este documento

1. **Voltei depois de dias** → lê secção "Estado actual" + "Open issues" + último entry do changelog
2. **Quero arrancar nova phase** → revê "Decision Log" para não repetir decisões
3. **Não sei o que mudou desde X** → "Changelog" tem timeline
4. **Não lembro onde está Y** → "Architecture Map" + "Comandos canónicos"
5. **User pergunta "ainda sigo a regra Z?"** → "7 não-negociáveis"

## 🔗 Cross-links principais

- [[Home|🏠 Home]]
- [[skills/_MOC|🧰 Skills MOC]]
- [[skills/Phase_X_Perpetuum_Engine|🔁 Perpetuum Engine]]
- [[skills/Phase_Y_Roadmap|🏗️ Phase Y Roadmap]]
- [[skills/Library_Books_and_Options|📚 Library + Options strategy]]
- [[skills/Design_System|🎨 Design System v1.0 (Helena)]]
- [[skills/Design_Watch|🔍 Design Watch (research weekly)]]
- [[skills/Claude_Design_Integration|🧪 Claude Design integration plan]]
- [[agents/personas/Helena Linha|👤 Helena Linha (Head of Design)]]
- [[skills/Session_2026-04-24_Final_State|🏆 Session 24/04 final]]
- [[wiki/Index|📚 Wiki Index]]

---
*A Constituição é viva. Cada commit grande adiciona linha ao Changelog + actualiza secção relevante.*
