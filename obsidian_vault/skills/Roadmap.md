---
type: roadmap
tags: [skills, roadmap, phase_w, gold]
phase: W
tier_target: gold
status: planning
created: 2026-04-24
---

# 🗺️ Phase W Gold — Skills Arsenal & Full Professionalization

> **Contexto**: Phase V.2 concluída (agents + personas). Phase W **Gold** absorve skills externas + descobertas adicionais para elevar projecto ao máximo. Overkill autorizado pelo user.
>
> **Princípio**: [[../_MOC|in-house first]] continua meta-regra. Skills Gold entram quando resolvem dor quantificável. [[Metrics]] é quem mede o ganho.

---

## Sprint W.1 — Document Skills (PDF + XLSX) 🎯

**Dor**: subscriptions PDF + broker xlsx frágeis.
**Entregáveis**:
- [ ] Install PDF + XLSX skills em `~/.claude/skills/`
- [ ] Flag `--use-claude-pdf` em `fetchers/subscriptions/_pdf_extract.py` (opt-in)
- [ ] Migrar `scripts/import_portfolio.py` para XLSX skill fallback
- [ ] Benchmark Ollama vs Claude PDF: 1 Suno + 1 XP + 1 WSJ

**Critério**: benchmark commitado; PDFs complexos extraem corretamente.

---

## Sprint W.2 — Scraping + Harness MCPs 🕷️

**Dor**: Status Invest scraper frágil; Bigdata.com/Google Drive/Calendar já loaded mas sem uso.
**Entregáveis**:
- [ ] Playwright MCP em `.claude/mcp.json`
- [ ] Firecrawl (cloud ou Docker self-host)
- [ ] Tavily MCP integrado em `fetchers/news_fetch.py`
- [ ] **NEW**: Refactor `fii_statusinvest_scraper.py` → wrapper `status-invest` MCP (delete scraping)
- [ ] **NEW**: `fetchers/bigdata_fetcher.py` — Bigdata.com MCP para tearsheets + events (branding: "Bigdata.com", https://bigdata.com)
- [ ] **NEW**: Google Calendar auto-populate (earnings + ex-div events)
- [ ] **NEW**: Google Drive output folder `Investment Intelligence/` estruturado
- [ ] Novo `fetchers/investidor10_scraper.py` via Playwright (DY 10y histórico BR)

**Critério**: 1 ticker BR com DY 10y carregado; StatusInvest scraper deletado; Calendar tem ≥10 eventos.

---

## Sprint W.3 — Obsidian Automation 📓

**Dor**: 53 wiki + 184 ticker notes, 0% com evergreen status.
**Entregáveis**:
- [ ] Estudar skills kepano (MOC, evergreen, orphan detect)
- [ ] Frontmatter `status: seedling/budding/evergreen` aplicado aos 35 holdings
- [ ] Dataview query orphan detection → lista órfãs
- [ ] Refactor `Home.md` com 3-pane pattern
- [ ] Todos os 35 tickers com secção `## Thesis` (feed perpetuum)

**Critério**: 0 orphan notes; 35/35 tickers com thesis explícita (necessário para W.5).

---

## Sprint W.4 — Skill Creator + 4 skills custom 🛠️

**Meta-sprint** — criar skills próprios que qualquer Claude futuro usa.

**Entregáveis**:
- [x] **drip-analyst** piloto criado em `.claude/skills/drip-analyst/SKILL.md` ✅
- [ ] **panorama-ticker** — orquestra `ii panorama X --write` + narra PT
- [ ] **rebalance-advisor** — lê portfolio + targets + macro + sugere
- [ ] **macro-regime** — classifica BR+US + flaga sectors
- [ ] Testar cada skill com prompt real (abrir session fresh, validar trigger)

**Critério**: 4/4 skills disparam automaticamente em prompts típicos.

---

## Sprint W.5 — Autoresearch + Ad Perpetuum Validator 🔬 **HEART OF GOLD**

**Dor**: thesis é manual, actualizada ad-hoc. Capital em risco quando thesis quebra silenciosamente.

**Entregáveis (já scaffolded ✅)**:
- [x] Schema `thesis_health` migrado BR + US ✅
- [x] `agents/perpetuum_validator.py` scaffold ✅
- [ ] Integrar Tavily MCP para new_evidence search (W.2 prereq)
- [ ] Integrar `devils_advocate` + `risk_auditor` nos hooks
- [ ] Integrar `analytics/regime.py` para regime_shift detection
- [ ] Hook no cron 23:45 (após daily_update 23:30)
- [ ] Telegram alert template para decay
- [ ] Weekly review `agents/thesis_weekly_review.py` → markdown + PPTX
- [ ] **Decision**: GPT Researcher vs Karpathy autoresearch — 30d A/B test

**Critério**: 30 dias de runs consecutivos; ≥1 decay alert disparado corretamente.

---

## Sprint W.6 — Agent Observability + Optimization 🤖

**Dor**: 12 agents sem tests; prompts hand-written não optimized; parsing JSON frágil.

**Entregáveis**:
- [ ] **Instructor** — Pydantic output schemas para 13 agents (inclui perpetuum)
- [ ] **LangFuse self-host** (Docker) + wrap `agents/_llm.py`
- [ ] **promptfoo** test suite cobrindo 13 agents
- [ ] **Context7 MCP** para docs on-demand
- [ ] **DSPy piloto** em `risk_auditor` (agent mais crítico)
- [ ] Benchmark: quality score pré vs pós-DSPy

**Critério**: 100% agents com tests; DSPy ganho >15% no risk_auditor; LangFuse dashboard funcional.

---

## Sprint W.7 — Catalog Monitoring 👁️

**Entregável**: `agents/skill_scout.py` cron mensal.
**Critério**: primeiro report 2026-05-24 → `obsidian_vault/skills/_monthly_2026-05.md`.

---

## Sprint W.8 — Canvas + PPTX 🎨🎬 **(NEW Gold)**

**Dor**: briefings só texto; sem deliverable trimestral profissional.

**Entregáveis**:
- [ ] Canvas Design skill instalada
- [ ] Template `obsidian_vault/templates/daily_briefing_visual.md` (4 charts embedded)
- [ ] Canvas ticker deep-dive (piloto ACN)
- [ ] PPTX skill instalada
- [ ] Template `reports/templates/quarterly_template.pptx`
- [ ] Script `scripts/generate_quarterly_deck.py`
- [ ] Primeiro deck Q1 2026 entregue + upload Google Drive

**Critério**: Q1 2026 deck entregue; daily briefings com charts visuais.

---

## Sprint W.9 — Remotion weekly video 🎥 **(NEW Gold)**

**Prereq**: W.5 (thesis_health feed) + W.8 (canvas graphics).
**Entregáveis**:
- [ ] Projecto Remotion em `video/` folder
- [ ] Components: `<PortfolioTotal>`, `<SparklineTicker>`, `<ThesisHeatmap>`, `<RegimeDial>`
- [ ] TTS local (Coqui) OR ElevenLabs free tier
- [ ] Script `video/render_weekly.ts`
- [ ] Cron Sunday 20h
- [ ] Upload Google Drive + Telegram push

**Critério**: 4 semanas consecutivas de videos renderizados e entregues.

---

## Sprint W.10 — OpenBB peer integration 💎 **(NEW Gold)**

**Dor**: construímos muito wheel-reinvention em `analytics/`.
**Entregáveis**:
- [ ] `pip install openbb` em venv paralelo
- [ ] `fetchers/openbb_fetcher.py` wrapper básico
- [ ] A/B test: 5 BR + 5 US tickers vs brapi/yfinance
- [ ] Decision memo: quais 5 scripts nossos aposentamos
- [ ] Documentar em CLAUDE.md o novo pattern

**Critério**: memo decision entregue; ≥3 scripts aposentados em favor de OpenBB equivalents.

---

## Sprint W.11 — Quant stack pro 📈 **(NEW Gold)**

**Dor**: analytics custom, lento, métricas básicas.
**Entregáveis**:
- [ ] **pyfolio** tearsheet — `scripts/pyfolio_tearsheet.py`
- [ ] **empyrical** — `analytics/risk_metrics.py` (Sharpe, Sortino, Calmar, VaR, CVaR)
- [ ] **vectorbt** — refactor `analytics/backtest_yield.py` e `backtest_regime.py` (100x speedup)
- [ ] **Alphalens** — `analytics/factor_validation.py` valida scoring IP (IC coefficient)
- [ ] **Riskfolio-Lib** — `scripts/position_size.py --optimize hrp`

**Critério**: Alphalens prova scoring engine tem IC>0.05; backtests rodam <5s; pyfolio tearsheet quarterly.

---

## ⏭️ Ordem Gold de execução

```
W.1 (docs)           → quick wins, PDF + XLSX
W.2 (scraping+MCP)   → harness MCPs são low-hanging fruit massivo
W.4 (skill creator)  → fundação para skills custom
W.3 (obsidian)       → prereq para W.5 (thesis explícita)
W.5 (perpetuum) 🎯   → HEART OF GOLD, depende de W.2 + W.3
W.6 (observability)  → blindar antes de escalar
W.11 (quant stack)   → pyfolio + vectorbt + Alphalens
W.8 (canvas+pptx)    → deliverable layer
W.9 (video)          → last, needs W.5 + W.8
W.10 (openbb)        → opportunistic, pode mover mais cedo
W.7 (catalog)        → passivo, sempre on
```

**Estimativa total**: 5 meses (2026-04-24 → 2026-09-30 target Gold).

---

## 🎯 Done criteria — "Phase W Gold complete"

Ver [[Metrics#🚀 Commit point — Gold achieved]] para checklist completa.

Essencial:
- Perpetuum validator 30d consecutivos
- 35/35 tickers com thesis
- ≥12 skills Gold integradas
- ≥4 skills customizadas criadas + testadas
- Observability stack funcional
- 1 quarterly PPTX + 4 weekly videos
- Alphalens valida scoring IP
- In-house ratio ≥85% comprovado

---

## ❌ OUT-of-scope Phase W (explícito)

- Frontend rewrite React/Next
- Marketing/SEO/Brand skills
- Multi-agent framework migration
- Container sandboxing single-machine
