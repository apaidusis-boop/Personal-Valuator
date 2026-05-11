---
type: roadmap
tags: [skills, roadmap, phase_w, gold]
phase: W
tier_target: gold
status: in_progress
created: 2026-04-24
updated: 2026-04-28
---

# 🗺️ Phase W Gold — Skills Arsenal & Full Professionalization

> **Doc canónico vivo** = [[../CONSTITUTION]] (phases history + decision log).
> Este Roadmap rastreia o **plano original Phase W**. Marca sprints shipped à medida que avançamos. Phases adjacentes (Y/AA/FIX/L/U) vivem na Constitution.
>
> **Princípio**: [[../_MOC|in-house first]] meta-regra. Skills Gold entram quando resolvem dor quantificável.
> **Coding principles**: [Karpathy guidelines](https://github.com/forrestchang/andrej-karpathy-skills) adoptadas no `CLAUDE.md` raiz (2026-04-28) — Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution.

---

## 📊 Snapshot — 2026-04-28

| Sprint | Estado | Onde |
|---|---|---|
| W.1 Document Skills (PDF/XLSX) | ⏳ pending | quick win |
| W.2 Scraping + Harness MCPs | 🟡 partial | Tavily ✅ K.2; Bigdata.com listada; Playwright/Calendar/investidor10 pendentes |
| W.3 Obsidian Automation | ✅ **done** | wiki holdings 34/34 (Phase I); thesis 184/184 (Phase J); bibliotheca autofix (DD) |
| W.4 Skill Creator + 4 custom | ✅ **done** | drip-analyst + panorama-ticker + rebalance-advisor + macro-regime registadas |
| W.5 Autoresearch + Perpetuum 🎯 | ✅ **done (heart of gold)** | 11 perpetuums activos; Tavily 3-wired (K.2); autoresearch perpetuum (K) |
| W.6 Observability | 🟡 W.6.1+W.6.2 done | W.6.3/4 pendentes |
| W.7 Catalog Monitoring | ⏳ pending | passivo, baixo esforço |
| W.8 Canvas + PPTX | ⏳ pending | quarterly deck deliverable |
| W.9 Remotion video | ⏳ pending | needs W.5 ✅ + W.8 |
| W.10 OpenBB peer | ⏳ pending | opportunistic |
| W.11 Quant stack | ✅ **done** | Phase L — vectorbt + pyfolio + alphalens + empyrical smoke OK |

**Done**: 5/11 sprints (W.3, W.4, W.5, W.6.1, W.11) + Heart of Gold ✅.
**Próximo recomendado**: W.6.2 (promptfoo offline test suite) — natural continuação de W.6.1; alinhado com Karpathy "goal-driven".

---

## ✅ Sprints shipped (detalhes)

### W.3 — Obsidian Automation 📓 (Phase I + J + DD)

- Wiki holdings 34/34 (incluindo 10 stubs `auto_draft:true` via `agents/holding_wiki_synthesizer.py`)
- Thesis universe-wide 184/184 via `agents/perpetuum/thesis.py` + `agents/thesis_synthesizer.py` (Ollama Qwen 14B)
- Bibliotheca autofix (Phase DD): BR sectors NULL 17→0, 35 fixes nomes, 94 orphans surfaced

### W.4 — Skills custom (4/4)

Registadas em `.claude/skills/`:
- `drip-analyst` — piloto
- `panorama-ticker` — orquestra `ii panorama X --write`
- `rebalance-advisor` — portfolio + targets + macro
- `macro-regime` — classifica BR+US

### W.5 — Heart of Gold ✅

11 perpetuums activos: thesis, vault, data_coverage, code_health, bibliotheca, ri_freshness, autoresearch, content_quality, token_economy, library_signals (frozen), meta. Tavily 3-wired em variant_perception/earnings_prep/synthetic_ic (Phase K.2).

### W.6.1 — Pydantic typed outputs (2026-04-28)

`agents/_schemas.py` (PersonaVerdict / ThesisDraft / HoldingWikiStub) + `agents/_llm.py::ollama_call_typed[T]`. Refactored synthetic_ic + thesis_synthesizer + holding_wiki_synthesizer (eliminados manual `json.loads` + 3 violations CH001). Validation: Literal types + conint(1,10).

### W.11 — Quant stack pro 📈 (Phase L)

`analytics/quant_smoke.py` com vectorbt + pyfolio-reloaded + alphalens-reloaded + empyrical. CAGR, Sharpe, Sortino, Calmar, MaxDD computados; HTML report Helena `ii_dark` standalone. US: CAGR 18.3%, Sharpe 0.92. BR: CAGR 6.6%, Sharpe 0.56 (winsorized 50%).

---

## ⏳ Sprints pendentes (detalhes)

### W.6.2 — pytest offline test suite ✅ **DONE 2026-04-28**

**Dor**: 3 agents typed (W.6.1) sem coverage automatizada — regressão silenciosa possível.

**Decisão tooling**: **pytest** sobre promptfoo (Karpathy "Simplicity first"). Projecto 100% Python; promptfoo traria Node.js + custom Ollama provider; ~50 LoC vs ~200.

**Shipped**:
- [x] `tests/test_typed_outputs.py` — 7 tests cobrindo PersonaVerdict + ThesisDraft + HoldingWikiStub
- [x] Assertions: schema válido + Literal fields no domínio + conviction range + non-empty content + seed reproducibility
- [x] `pytestmark = skipif(not _ollama_up())` — skip gracioso se Ollama down
- [x] CLAUDE.md catalog: `pytest tests/ -v`
- [x] Critério atingido: 7/7 pass em **59.5s**, 100% offline, zero Claude tokens

**Tests**:
1. `test_persona_verdict_schema_valid` — domínio Literal + conviction 1-10 + would_size enum
2. `test_persona_verdict_buffett_likes_ko` — sanity: KO-Buffett não AVOID
3. `test_persona_verdict_seed_reproducible` — same seed → same verdict
4. `test_thesis_draft_schema_valid` — assumptions/triggers non-empty
5. `test_thesis_draft_assumptions_are_strings` — type integrity de listas
6. `test_holding_wiki_stub_schema_valid` — todos os campos required preenchidos
7. `test_holding_wiki_stub_lists_are_strings` — type integrity de listas

### W.6.3 — LangFuse self-host

**Dor**: prompts não tracked em prod; debug pos-mortem é grep nos logs.
**Entregáveis**:
- [ ] Docker compose LangFuse self-host
- [ ] Wrap `agents/_llm.py::ollama_call` com decorator de trace
- [ ] Dashboard local `http://localhost:3000` com últimas 100 chamadas

### W.6.4 — DSPy piloto em risk_auditor

**Dor**: prompt risk_auditor hand-tuned; sem benchmark de quality.
**Entregáveis**:
- [ ] Trainset: 20 cases manuais (ticker, situação, expected risk_call)
- [ ] DSPy MIPRO ou BootstrapFewShot
- [ ] Benchmark pré vs pós DSPy
- [ ] Decisão go/no-go para outros agents

### W.1 — Document Skills (PDF + XLSX)

**Dor**: subscriptions PDF Suno/XP/WSJ frágeis quando layout muda.
**Entregáveis**:
- [ ] Install PDF + XLSX skills em `~/.claude/skills/`
- [ ] Flag `--use-claude-pdf` em `fetchers/subscriptions/_pdf_extract.py` (opt-in)
- [ ] Migrar `scripts/import_portfolio.py` para XLSX skill fallback
- [ ] Benchmark Ollama vs Claude PDF: 1 Suno + 1 XP + 1 WSJ

### W.2 — Scraping + Harness MCPs (parcial)

**Já feito**: Tavily MCP + autoresearch (K, K.2, K.3) + Bigdata.com listada.

**Pendente**:
- [ ] Playwright MCP em `.claude/mcp.json`
- [ ] Firecrawl Docker self-host (decisão: cloud já avaliada SKL_firecrawl)
- [ ] `fetchers/bigdata_fetcher.py` — wrapper Bigdata.com MCP para tearsheets + events (branding: "Bigdata.com")
- [ ] Google Calendar auto-populate (earnings + ex-div)
- [ ] Google Drive folder estruturado `Investment Intelligence/`
- [ ] `fetchers/investidor10_scraper.py` via Playwright (DY 10y BR)

### W.7 — Catalog Monitoring (passivo)

`agents/skill_scout.py` cron mensal. Primeiro report: `obsidian_vault/skills/_monthly_2026-05.md`.

### W.8 — Canvas + PPTX

- Canvas Design skill instalada
- Templates: `templates/daily_briefing_visual.md` (4 charts), `reports/templates/quarterly_template.pptx`
- `scripts/generate_quarterly_deck.py`
- Primeiro deck Q1 2026 + upload Google Drive

### W.9 — Remotion weekly video

Pré-req: W.5 ✅ + W.8.
- Projecto Remotion em `video/`
- Components: `<PortfolioTotal>`, `<SparklineTicker>`, `<ThesisHeatmap>`, `<RegimeDial>`
- TTS Coqui local OR ElevenLabs free
- Cron Sunday 20h + upload Drive + Telegram push

### W.10 — OpenBB peer integration

- `pip install openbb` em venv paralelo
- A/B test 5 BR + 5 US tickers vs brapi/yfinance
- Decision memo: quais scripts aposentamos
- Documentar pattern em CLAUDE.md

---

## 🚧 Phase U — Unification (current canonical)

Per Constitution: `current_phase: U — Unification (Sprints U.0–U.7). U.0 SHIPPED.`

**U.0 done** (2026-04-26):
- 3-layer brain formalisado (L1 SQLite / L2 vault auto / L3 vault humano)
- React desktop deprecated
- `helena.css` unifica Streamlit ↔ Obsidian
- 11 `_LAYER.md` markers + root limpo + vault auto-commit script

**U.1–U.7**: a definir/expandir conforme avançamos. **U.1 Home minimalista** é o próximo provável.

---

## ⏭️ Ordem actualizada de execução (2026-04-28)

```
W.6.2 (promptfoo offline)  → blindar W.6.1 com tests; baseline para W.6.3
W.6.3 (LangFuse)           → observability prod; baseline trace de prompts
W.6.4 (DSPy risk_auditor)  → quality gain mensurável
W.1   (PDF/XLSX skills)    → quick win opt-in (não rompe nada)
W.7   (skill_scout cron)   → 1 cron, baixo risco
U.1   (Home minimalista)   → UI canonical Helena style
W.8   (Canvas + PPTX)      → deliverable layer (quarterly)
W.9   (Remotion video)     → after W.8
W.2   (Playwright/Bigdata) → opportunistic
W.10  (OpenBB)             → opportunistic
```

**Estimativa restante**: 3-4 meses para Gold complete (target 2026-08-31).

---

## 🎯 Done criteria — "Phase W Gold complete"

- ✅ Perpetuum validator 30d consecutivos (heart of gold shipping)
- ✅ 35/35 tickers com thesis (na verdade 184/184 universe — superado)
- ✅ ≥12 skills Gold integradas
- ✅ ≥4 skills customizadas criadas + testadas
- 🟡 Observability stack funcional (W.6.1 done; promptfoo + LangFuse pendentes)
- ⏳ 1 quarterly PPTX + 4 weekly videos
- ✅ Alphalens valida scoring IP (Phase L smoke OK)
- ✅ In-house ratio ≥85% comprovado

---

## ❌ OUT-of-scope Phase W (explícito)

- Frontend rewrite React/Next (deprecated em U.0)
- Marketing/SEO/Brand skills
- Multi-agent framework migration
- Container sandboxing single-machine
- Pinecone / Lovable / Zapier (avaliados 2026-04-28; nosso stack já cobre)
