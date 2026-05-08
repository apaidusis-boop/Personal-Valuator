---
type: skill_scout_report
date: 2026-05-08
total: 19
active: 13
stable: 0
decay: 0
backlog: 3
skipped: 3
tags: [skill_scout, monthly, w_7]
---

# 🛰️ Skill Scout — 2026-05-08

Auditoria mensal de **19 skill notes** vs. actividade no codebase.
Active = touched ≤30d · Stable = 31–90d · Decay = >90d · Backlog = no impl found.

**Snapshot**: 🟢 13 active · 🟡 0 stable · 🔴 0 decay · ⏳ 3 backlog · ⚪ 3 skipped.

## ⏳ Backlog (no impl yet)

- [[SKL_openbb]] · sprint W.10 · tier Gold — status: backlog
- [[SKL_pptx]] · sprint W.8 · tier Gold — status: backlog
- [[SKL_remotion]] · sprint W.9 · tier Gold — status: backlog

## 🟢 Active (≤30d)

- [[SKL_obsidian_kepano]] · sprint W.3 · tier S — last touched 2026-05-04 (3d ago)
    - impl: `scripts/memory_cleanup.py`, `scripts/obsidian_bridge.py`
- [[SKL_playwright_mcp]] · sprint W.2 · tier S — last touched 2026-05-04 (3d ago)
    - impl: `fetchers/fii_statusinvest_scraper.py`, `scripts/obsidian_bridge.py`
- [[SKL_autoresearch_perpetuum]] · sprint W.5 · tier Gold — last touched 2026-04-27 (10d ago)
    - impl: `agents/devils_advocate.py`, `agents/meta_agent.py`, `agents/perpetuum_validator.py`, `agents/risk_auditor.py` (+3)
- [[SKL_canvas_design]] · sprint W.8 · tier Gold — last touched 2026-04-26 (11d ago)
    - impl: `scripts/weekly_report.py`
- [[SKL_firecrawl]] · sprint W.2 · tier S — last touched 2026-04-26 (11d ago)
    - impl: `monitors/cvm_monitor.py`, `monitors/sec_monitor.py`
- [[SKL_tavily]] · sprint W.2 · tier S — last touched 2026-04-26 (11d ago)
    - impl: `agents/research_scout.py`, `fetchers/news_fetch.py`, `scripts/research.py`
- [[SKL_tier_A]] · tier A — last touched 2026-04-26 (11d ago)
    - impl: `scripts/research.py`
- [[SKL_mcp_harness_arsenal]] · sprint W.2 · tier Gold — last touched 2026-04-23 (14d ago)
    - impl: `fetchers/earnings_calendar.py`, `fetchers/fii_statusinvest_scraper.py`
- [[SKL_quant_stack]] · sprint W.11 · tier Gold — last touched 2026-04-23 (14d ago)
    - impl: `analytics/backtest_yield.py`, `scripts/portfolio_report.py`, `scripts/position_size.py`
- [[SKL_skill_creator]] · sprint W.4 · tier S — last touched 2026-04-20 (17d ago)
    - impl: `scripts/drip_projection.py`
- [[SKL_observability_stack]] · sprint W.6 · tier Gold — last touched 2026-05-08 (0d ago)
    - impl: `agents/_base.py`, `agents/_llm.py`
- [[SKL_pdf_processing]] · sprint W.1 · tier S — last touched 2026-05-08 (0d ago)
    - impl: `fetchers/subscriptions/_pdf_extract.py`, `monitors/cvm_monitor.py`, `monitors/sec_monitor.py`
- [[SKL_xlsx]] · sprint W.1 · tier S — last touched 2026-05-08 (0d ago)
    - impl: `scripts/import_portfolio.py`, `scripts/import_taxlots.py`

## ⚪ Skipped (Tier B/C — informational)

- [[SKL_tier_B]] · tier B — last touched 2026-05-06 (2d ago)
    - impl: `agents/_runner.py`, `agents/helena/audit.py`, `agents/perpetuum/code_health.py`
- [[SKL_google_stitch]] · tier B — last touched 2026-04-26 (11d ago)
    - impl: `agents/helena_mega.py`, `scripts/_components.py`, `scripts/_theme.py`
- [[SKL_tier_C_and_catalogs]] · tier C — status: deferred
    - impl: `agents/skill_scout.py`

---

## 🔁 Manutenção

1. **Decay candidates**: abrir SKL note + git blame impl. Decidir `status: deprecated` no frontmatter ou re-investir.
2. **Backlog antigos** (>60d): demote para `tier_C` ou archive.
3. **Active sem decay tracking**: nada a fazer.

Gerado por `python -m agents.skill_scout` em 2026-05-08T14:08:46.
