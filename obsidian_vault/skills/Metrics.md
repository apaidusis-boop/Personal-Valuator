---
type: metrics
tags: [metrics, kpi, before_after, phase_w]
baseline_date: 2026-04-24
target_gold_date: 2026-09-30
---

# 📏 Phase W Metrics — Before / After Quadro

> **Objetivo**: provar quantitativamente que Phase W Gold elevou o projeto. **Baseline hoje (2026-04-24)**, medições contínuas via `scripts/metrics_report.py`.

## 🎯 Como funciona

1. **Baseline** em 2026-04-24 (freeze state): `python scripts/metrics_baseline.py --freeze`
2. Baseline escrito em `data/metrics_baseline_2026-04-24.json`
3. **Tracking contínuo**: `scripts/metrics_report.py` roda diário, escreve em `metrics_history` table
4. **Weekly comparison** em `obsidian_vault/briefings/weekly_metrics_YYYY-WW.md`
5. **Monthly dashboard**: thesis_health + agent performance + token cost trends

---

## 📊 Quadro BEFORE / AFTER

### 🗂️ Data & Sources

| Métrica | Before (2026-04-24) | Target Gold (2026-09-30) | Measurement |
|---|---|---|---|
| Data sources activos | 8 (brapi, yfinance, FRED, SEC, CVM, StatusInvest scraper, subscriptions, YT) | **14** (+Investidor10, +Fundamentus, +OpenBB, +Bigdata.com MCP, +LSEG, +Tavily) | Count in `fetchers/_registry.py` |
| MCP servers integrados | 0 (harness-loaded mas não usados) | **6** (Bigdata.com, Status Invest, Playwright, Tavily, Firecrawl, Google Drive) | `.claude/mcp.json` + harness |
| Scraping scripts frágeis | 2 (StatusInvest, partes de news_fetch) | **0** (substituídos por MCP/Playwright) | LOC em `fetchers/*scraper*` |
| DY histórico 10y BR | ❌ não temos | ✅ 35 tickers | new `fundamentals.dy_history_json` |

### 🤖 Agents & LLM Ops

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Agents em production | 12 (Phase V) | **12 + perpetuum_validator = 13** | `agents/` count |
| Agents com tests promptfoo | **0** | **13 (100% coverage)** | `tests/prompts/` suite |
| Agent observability | prints + logs | **LangFuse traces 100%** | LangFuse dashboard |
| Prompt optimization | manual (hand-written) | **DSPy-optimized em 3 agents críticos** | `tests/prompts/dspy_eval_*.json` |
| Structured outputs | parse frágil | **Instructor+Pydantic 100%** | 0 parse errors em 30d |

### 🔬 Research Quality

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Research memo (`ii research X`) | template + 1-shot Claude | **deep mode com autoresearch multi-step** | avg # sources per memo |
| Sources per memo | ~3 (yfinance + CLAUDE.md + Ollama) | **≥10** (+ Tavily + Bigdata + subscriptions + Investidor10) | parse `data/research_cache/*.json` |
| Counter-arguments per memo | 0-1 (manual) | **≥3** (devils_advocate integrado) | devils_advocate output count |
| Thesis tracking | manual, mensal | **diário automatic** via perpetuum | thesis_health row count |
| Thesis health score | N/A | **0-100 per holding daily** | `thesis_health` table |

### 🧠 Skills Arsenal

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| External skills avaliadas | 0 | **33 documented** | `obsidian_vault/skills/SKL_*.md` count |
| Skills Gold integradas | 0 | **≥12 active** | installed in `~/.claude/skills/` |
| Skills customizadas criadas | 0 | **4** (drip-analyst, panorama-ticker, rebalance-advisor, macro-regime) | `.claude/skills/` count |
| Skills com test case | 0 | **4/4 tested** | dispatcher logs |

### 📊 Quant & Analytics

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Backtest engines | 2 custom (yield, regime) | **2 custom + vectorbt** (100x faster) | wall clock time |
| Backtest runtime (20y hist) | ~5 min | **<5 sec** (vectorbt) | `time python analytics/...` |
| Portfolio tearsheet | básico (portfolio_report.py) | **pyfolio full** (20 charts, institutional) | HTML tearsheet pages |
| Risk metrics | Sharpe manual | **empyrical** (Sharpe, Sortino, Calmar, VaR, CVaR, alpha, beta) | `analytics/risk_metrics.py` |
| Factor analysis | ❌ | ✅ **Alphalens** valida scoring IP | IC coefficient published |

### 📓 Obsidian Vault

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Wiki notes | 53 | **≥60** (+ skills 12 + métodos novos) | `wiki/` + `skills/` count |
| Ticker notes com thesis explícita | ~15/35 (43%) | **35/35 (100%)** | grep `## Thesis` in tickers/ |
| Orphan notes (0 backlinks) | unknown | **0** (kepano cleanup) | Dataview query |
| Evergreen status tagged | 0% | **100%** (seedling/budding/evergreen) | frontmatter count |
| Daily briefings auto-visual | ❌ | ✅ **Canvas charts embedded** | PNG count in briefings |

### 📦 Deliverables

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Weekly report format | Markdown | Markdown **+ pyfolio HTML** | file types in `reports/` |
| Quarterly deliverable | ❌ | ✅ **PPTX deck auto-generated** | `reports/quarterly_*.pptx` |
| Video recap | ❌ | ✅ **Weekly 60-90s MP4** (Remotion) | `reports/videos/*.mp4` |
| Google Drive backup | ❌ | ✅ **auto-upload all reports** | Drive API logs |
| Calendar integration | ❌ | ✅ **earnings + ex-div events** | Google Calendar events count |

### 💰 Cost & Tokens

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| Tokens Claude / week | unknown | **tracked + budget** | LangFuse cost dashboard |
| In-house ratio (Ollama/Claude) | ~70% est | **≥85%** (após autoresearch + Tavily cache) | LangFuse traces |
| Cache hit rate | 0% (no cache) | **≥60%** (research_cache + tavily_cache + pdf_cache) | cache stats |

### ⚡ Time-to-Insight

| Métrica | Before | Target Gold | Measurement |
|---|---|---|---|
| "Should I buy X?" → answer | ~5-10 min manual | **<30s** via drip-analyst skill | User logs |
| "Regime changed?" detection latency | N days | **≤1 day** (daily perpetuum) | alert timestamps |
| Thesis decay detection | weeks/months | **≤1 day** | Telegram alert count |
| New relevant news → surface | manual scan | **≤1h** (news_fetch + Tavily + classify) | event_date vs alert timestamp |

---

## 🎯 5 KPIs headline para dashboard

Top-level metrics que vão para weekly briefing:

1. **Thesis Health Portfolio Avg** (0-100) — média ponderada por peso na carteira
2. **In-house Ratio** (%) — Ollama calls / total LLM calls
3. **Research Depth Score** — avg sources per memo (target ≥10)
4. **Agent Test Coverage** — % agents com promptfoo passing
5. **Decay Alerts This Week** — # vezes perpetuum disparou alerta (signal quality)

---

## 📉 Leading indicators (sinais de problema ANTES de materializar)

O perpetuum validator + métricas dão **early warning**:

- **Thesis score drop ≥10 pts em 1 dia** → action item imediato
- **Regime shift detected** → rebalance avaliar em 7 dias
- **Contradiction count >3 em 30 dias para ticker X** → thesis may be broken, manual review
- **Decay alerts spike** (>5/week) → macro stress event
- **In-house ratio drops** (<80%) → investigação: algum workflow leak tokens?

---

## 🚀 Commit point — "Gold achieved"

Definimos "Gold achieved" quando **todas** estas true:

- [ ] Perpetuum validator roda 30 dias consecutivos sem crash
- [ ] 35/35 holdings têm thesis explícita no vault
- [ ] ≥12 skills Gold instaladas + funcionais
- [ ] ≥4 skills customizadas criadas e a disparar auto
- [ ] promptfoo test suite passa em 13/13 agents
- [ ] 1 quarterly PPTX deck entregue
- [ ] 1 weekly video recap entregue
- [ ] In-house ratio medido ≥85% em 30-day window
- [ ] Alphalens valida scoring engine com IC>0.05 (significance)

**Target**: 2026-09-30 (5 meses de execução Phase W).

---

## 📍 Baseline script

Ver `scripts/metrics_baseline.py` — corre **uma vez** hoje, captura snapshot pré-Phase-W.
Ver `scripts/metrics_report.py` — corre **diário** via cron, popula metrics_history.

## Links
- [[Roadmap]] — sprints W.1 → W.11
- [[_MOC]] — índice skills
- [[SKL_autoresearch_perpetuum]] — engine que gera thesis_health metrics
- [[SKL_observability_stack|LangFuse]] — fonte de token/cost metrics
