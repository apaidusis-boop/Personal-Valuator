---
type: skills_moc
tags: [skills, moc, phase_w, gold]
updated: 2026-04-24
tier_target: gold
---

# 🏆 Skills Arsenal — Gold Tier MOC

> **Phase W Gold** — 33 skills avaliadas + descobertas adicionais. Promovemos a "overkill is fine" por pedido explícito do user.
> Filosofia: [[../_MOC|in-house first]] mantida — cada skill entra pela dor concreta que resolve. Mas agora pushamos ceiling para **profissional máximo**.

🗺️ **Começar aqui**: [[Roadmap]] — plano Gold W.1 → W.11
📏 **Medir progresso**: [[Metrics]] — quadro BEFORE/AFTER + KPIs
🎯 **Heart of Gold**: [[SKL_autoresearch_perpetuum]] — engine de validação contínua

---

## 🏆 Gold Tier — integrar tudo

### Document & Visual (W.1, W.8, W.9)
- [[SKL_pdf_processing]] 📄 — PDFs Suno/XP/WSJ complexos (opt-in vs Ollama)
- [[SKL_xlsx]] 📊 — portfolio XP/JPM imports resilientes a layout changes
- [[SKL_canvas_design]] 🎨 — briefings visuais + charts em Obsidian Canvas
- [[SKL_pptx]] 🎬 — quarterly deck auto-gerado + annual review
- [[SKL_remotion]] 🎥 — weekly video recap (60-90s MP4, TTS narrated)
- [[SKL_google_stitch]] 🪡 — vibe design tool (Tier B observe-only; valida Helena Linha sem substituir)

### Scraping & Data (W.2)
- [[SKL_playwright_mcp]] 🎭 — Investidor10, brokers, sites JS-heavy
- [[SKL_firecrawl]] 🔥 — CVM, SEC, markdown clean output
- [[SKL_tavily]] 🔍 — search qualificada para news + research
- [[SKL_mcp_harness_arsenal]] 🎁 — **CRÍTICO**: Bigdata.com + Status Invest + Google Drive + Gmail + Calendar já loaded no harness (untapped!)

### Vault & PKM (W.3)
- [[SKL_obsidian_kepano]] 📓 — MOC, evergreen status, orphan detection

### Research & Autonomy (W.5)
- [[SKL_autoresearch_perpetuum]] 🔬 — **heart of Gold**: ad perpetuum validator com thesis_health tracking diário

### Skill Creation (W.4) — meta-tool
- [[SKL_skill_creator]] 🛠️ — criar skills custom (drip-analyst, panorama, rebalance, macro-regime)

### Agent Ops & Observability (W.6)
- [[SKL_observability_stack]] 🔭 — LangFuse traces + DSPy optimization + Instructor structured outputs

### Quant (W.11)
- [[SKL_quant_stack]] 📈 — pyfolio tearsheets, empyrical risk, vectorbt backtest, Alphalens factor validation, Riskfolio-Lib optimization

### Platform peer (W.10)
- [[SKL_openbb]] 💎 — open source investment research platform como peer layer

### Tier A — avaliar sprint-a-sprint (ainda relevante mas não full-Gold)
- [[SKL_tier_A]] — Task Master, promptfoo, Context7, Codebase Memory, GPT Researcher alternatives

---

## 📦 Imported plugin skills (2026-05-13)

Absorção de **17 plugins** de marketplace → `.claude/skills/` (locais, invocáveis) + `obsidian_vault/skills/imported/` (pointer docs).

- **Total**: 111 skills + 48 commands + 4 agents
- **Motivo**: Independência de marketplace (FSI plugins hooks partidos em 2026-05-13)
- **Re-absorver**: `python scripts/absorb_plugins.py`
- **Manifest**: `data/absorbed_plugins.json`
- **Índice completo**: [[imported/_INDEX]]

Mais relevantes ao projecto investing:
- [[imported/equity-research/_]] — catalysts/screen/morning-note/thesis (sobrepõe `ii brief`, `ii decide`)
- [[imported/financial-analysis/_]] — DCF/LBO/3-statement/comps (sobrepõe `fair_value.py`, `compare_tickers.py`)
- [[imported/earnings-reviewer/_]] — earnings updates (sobrepõe `ii react`, `earnings_prep.py`)
- [[imported/wealth-management/_]] — rebalance/TLH (sobrepõe `ii rebalance`)
- [[imported/superpowers/_]] — eng meta-skills (systematic-debugging, writing-plans, TDD)

---

## 🚫 Skip explícito (documentado para não re-avaliar)

- [[SKL_tier_B]] — Superpowers (cherry-pick), n8n, claude-squad, Doc Co-Authoring, Web Artifacts, Frontend Design (Streamlit suficiente)
- [[SKL_tier_C_and_catalogs]] — gstack (não é SaaS), Marketing/SEO/Brand (não é produto), Langflow (overkill fora de escopo), container-use + Ghost OS (single-machine overkill)

**Nota**: "overkill is fine" do user aplica-se a skills que resolvem dor concreta; skills em escopo diferente (Marketing, SEO) continuam skip.

---

## 📚 Catálogos — monitorizar mensalmente (W.7)

Agent `agents/skill_scout.py` passivo. Ver [[SKL_tier_C_and_catalogs#Catálogos]]:
- Official Anthropic Skills Repo
- Awesome Claude Skills
- SkillsMP + SkillHub
- MAGI Archive

---

## 🎯 Skills customizadas a criar (W.4)

Project-scoped em `.claude/skills/`:

1. ✅ **drip-analyst** — criada como piloto (ver `.claude/skills/drip-analyst/SKILL.md`)
2. ⏳ **panorama-ticker** — orquestra `ii panorama X --write` + narra PT
3. ⏳ **rebalance-advisor** — lê `portfolio_positions` + targets + macro regime
4. ⏳ **macro-regime** — classifica BR+US + flaga sectors em alerta

---

## 🔗 Cross-links

- Phase anterior: [[../agents/_MOC|Agents layer (Phase V)]]
- Histórico fases: [[../_MOC#Phases]]
- Baseline frozen: `data/metrics_baseline_2026-04-24.json`
- Heart of Gold DB: `thesis_health` table (migrated 2026-04-24)
- Regra meta: **[[../_MOC|in-house first]]** governa adoção de qualquer skill external

## 📊 Estado actual (2026-04-24)

- ✅ 19 notas criadas em `obsidian_vault/skills/`
- ✅ Metrics baseline frozen
- ✅ `thesis_health` tabela migrada em BR + US
- ✅ `agents/perpetuum_validator.py` scaffold
- ✅ `.claude/skills/drip-analyst/SKILL.md` piloto
- ✅ `scripts/metrics_report.py` tracking contínuo
- ⏳ Sprints W.1 → W.11 pendentes execução
