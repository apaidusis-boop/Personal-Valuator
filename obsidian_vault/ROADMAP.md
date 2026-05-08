---
type: roadmap
status: canonical
last_updated: 2026-05-08
supersedes:
  - skills/Roadmap.md (Phase W detail kept for reference)
  - skills/Phase_Y_Roadmap.md (mostly shipped)
  - skills/Mission_Control_Design_Roadmap.md (v3 superseded by v5 JPM)
  - Roadmap_Always_On_Workforce.md (EE shipped today; rest queued here)
tags: [roadmap, master, canonical, governance]
---

# 🗺️ Master Roadmap — Investment Intelligence

> **Documento canónico único.** Substitui os 4 roadmaps fragmentados que existiam até 2026-05-08.
> Para o estado vivo + decision log + open issues, ver **[[CONSTITUTION]]**.
> Para skills detail (W.1-W.11), ver [[skills/Roadmap]].
>
> **Estrutura**:
> 1. [[#📊 Snapshot 2026-05-08]] — onde estamos hoje
> 2. [[#✅ Shipped — phases history]] — cronologia, mais recentes primeiro
> 3. [[#🎯 Queue — what's next]] — pendências priorizadas
> 4. [[#❌ Deprecated / superseded]] — limpeza
>
> Phase letters cyclados (EE, FF reusadas em contextos diferentes) são distinguidos por **data** + **descritor**.

---

## 📊 Snapshot 2026-05-08

**Status global**: sistema é maduro. 128 commits desde 2026-04-20. Closed-loop validation infra completa (Phase FF). Tiered scheduler shipped (Phase EE-AOW). Mission Control v6.1 com /calibration, /decisions, /perpetuums pages live.

**Aguardando**:
- ≥90 dias de validated verdicts → destrava Phase GG (Capital Deployment Engine). Estamos a ~13d in (window real Aug/2026).
- User registar `schtasks` para hourly + q4h tiers (commands em [[skills/Phase_EE_Tiered_Scheduler]]).
- User decidir PC sleep policy (recomendação: `powercfg standby-timeout-ac 0`).

**Open issues** vivem em [[CONSTITUTION#open-issues]]. Active count: pequeno (Phase FF closeout fechou a maioria).

---

## ✅ Shipped — phases history

### Maio 2026

| Data | Phase / Sprint | Resumo |
|---|---|---|
| **2026-05-08** | **Phase EE-AOW** Tiered Scheduler | `agents/_lock.py` + `hourly_run.bat` + `q4h_run.bat` + `daily_run.bat` refactor. Scheduler 3-tier com PID lockfiles. SEC inserted 7 events em smoke test. Doc: [[skills/Phase_EE_Tiered_Scheduler]]. Commit `ec40283`. |
| **2026-05-08** | **Phase FF CLOSED** | Calibration Loop fechado. Blocos 1.1/1.2/2.1/2.2/3.1/3.2/3.3/4.1 todos shipped. Bonus: `decision_journal_intel` windowing fix. Commit `8059b98`. |
| **2026-05-07/08** | **MC v6.1** /perpetuums | Health dashboard + Helena audit refresh. Commit `6336cdf`. |
| **2026-05-07/08** | **MC v6** /calibration + /decisions | Phase FF visibility pages. Commit `b4d939c`. |
| **2026-05-07** | **MC v5** JPM redesign | Side-sheet + Fool dossier + alerts/events/research/filings. Commit `4a4b2b6`. **Supersedes** MC v3 Broadsheet. |
| **2026-05-07** | Voice IO + Fiel Escudeiro | Antonio Carlos replacement. Commit `55ce87e`. |
| **2026-05-07** | FMP integration | Layer 1 FMPClient + Layer 2 MCP (27 tools). Commit `442e2cc`. |
| **2026-05-07** | Dividends + filings + fair value | + auto-verdict on filing. Commit `f35e8d2`. |
| **2026-05-05/06** | **Phase FF Blocos 3.1/3.2/3.3/4.1** | Provenance, tier action_safety, cross-source spot-check, sector tilt. Commits `22519cf`, `222ba8c`, `353e830`, `f0c87ce`, `27f84c4`. |
| **2026-05-05** | **Phase FF Blocos 1.1/1.2/2.1/2.2** | Decision Quality + engine breakdown + multi-family IC + Benford+MAD. Commits `b0295ce`, `0b751bb`, `8880d85`, `d43fac3`. |
| **2026-05-05** | MC v3 Broadsheet | FT/WSJ tokens. **Superseded** 2 dias depois por v5 JPM. Commit `16a0753`. |
| **2026-05-05** | Moat engine | `scoring/moat.py` 0-10 composite. JNJ 8.75 / KO 8.5 / ACN 8.0 STRONG. Commit `e86d914`. |

### Abril 2026 (intensification window)

| Data | Phase / Sprint | Resumo |
|---|---|---|
| **2026-04-30** | Night Shift 30/30 holdings | Council STORYT_3.0 dossiers. Commit `0d6a7d2` (era). |
| **2026-04-29** | **Phase EE-LocalClaw** bundle | LocalClaw P1-P4 + DeepDive V10 + Council + Topic Watchlist + Night Shift + Mission Control Next.js. **Diferente do AOW EE de hoje** — coincidência de letras. Commit `f928987`. |
| **2026-04-28** | **Phase W.6.1 + W.6.2** | Pydantic typed outputs + pytest offline suite. 7/7 tests pass em 60s. Commit `fb70501`. |
| **2026-04-28** | Cemetery (quarantine) | 13 items + 6 one-shots burial. Commits `3e2dba5`, `b830225`. |
| **2026-04-27 evening** | Mega Helena | Audit + curate + spike + master report pipeline. Commit `8e84df3`. |
| **2026-04-27 noon** | Path B Sprints 1-3 | FastAPI sidecar + Vite/React + operations surface. **Deprecated** em U.0 (substituído pelo MC Next.js). Commits `ed477af`, `d364ab7`, `8b39b0a`. |
| **2026-04-27 morning** | **Phase L** | BACEN IF.Data fetcher + W.11 Quant stack + IC universe-wide. Commits `7aeffbd`, `e20acfa`. |
| **2026-04-26 night** | **Phase BB / CC / DD / F** | code_health (BB), Captain's Log (CC), Bibliotheca autofix (DD), T0 cleanup (F). |
| **2026-04-26 evening** | **Phase U.0** Unification Sweep | 3-layer brain (L1/L2/L3). React desktop deprecated. helena.css unifica. Commit `b68c0a9`. |
| **2026-04-26** | **Phase J / I / H / G** | Universe-wide thesis (184/184), wiki holdings closeout, Telegram brief, holdings thesis backfill. |
| **2026-04-26** | **Phase K / K.2 / K.3** | Tavily wired (autoresearch + 3 modules). Skills + CLI installed. |
| **2026-04-25 night** | **Phase FIX + AUTO** | 11 sprints autonomous (ITRs backfill, IC × 33 holdings, vault timelines, conviction score, etc). |
| **2026-04-25 evening** | **Phase Z / Z.Design** | UI Friendly Layer (7 dashboard pages) + Helena Linha (s1-s4). |
| **2026-04-25 evening** | **Constitution criada** | `obsidian_vault/CONSTITUTION.md` master doc. |
| **2026-04-25 afternoon** | **Phase Y.0-Y.8** | RI Knowledge Base — CVM ingest + bank parser + quarterly_history. |
| **2026-04-25** | **Phase AA** Critical Thinking | Synthetic IC + Variant Perception + Earnings Prep + Portfolio Stress + Decision Journal Intelligence. |
| **2026-04-24 night** | **Phase X** Perpetuum Engine | 8→11 perpetuums (thesis/vault/data/content/methods/tokens/library/meta/+...). |
| **2026-04-24** | **Phase W** Skills Arsenal | 33 skills evaluated; 6/11 sprints shipped (W.3, W.4, W.5, W.6.1, W.6.2, W.11). |
| **2026-04-24** | Library + Paper Trade | Books → methods → matcher → 154 paper signals. |
| **2026-04-24** | **Phase V / V.1 / V.2** | Agents framework + RiskAuditor/DevilsAdvocate/MetaAgent + 12 funcionários sintéticos. |
| **2026-04-23/24** | **Phase U.1-U.7** | Subscriptions adapters (XP/Suno/WSJ) + Playwright + login flows + bridge enrichment. |
| **2026-04-23** | **Phases Q+R+S** | YouTube pipeline + Verdict Engine + Obsidian vault + Streamlit + tax lots. |
| **2026-04-22** | **Wiki Phase A + B.1/C.1/D/E** | 53 foundation notes (sectors, cycles, tax, playbooks). |
| **2026-04-22** | **Phase P** data quality + TEN distress | DY/CAGR computed locally; TEN sell memo. |
| **2026-04-22** | **Phase O** universe re-score | $3k triggers + BR dividend compounders. |
| **2026-04-22** | **Phase N** MegaWatchlist v1 | Fundamentals extra + metrics + unified view. |
| **2026-04-22** | **Phase M** Kings/Aristocrats | 87 tickers + loaders + $3k memo. |
| **2026-04-21** | **Phase L** verdict limpo | Intent layer + ETF N/A + ROE fallback. |
| **2026-04-21** | **Phase K** quality vetoes | Scoring → triggers → journal → reports. |
| **2026-04-21** | **Phase I + J** | Altman + Piotroski + unified research CLI. |
| **2026-04-20** | **Phase H** regime overlay backtest | REJECTED (−2%/y US/BR). |
| **2026-04-20** | **Phase G** DY-pctl entry timing | Closes Phase F loop. |

### Pre-2026-04-20 (pre-Constitution era)
Phases F (and earlier) shipped antes do Constitution ser criado. Detalhe não consolidado aqui — ver `git log` ou Constitution Changelog.

---

## 🎯 Queue — what's next

> Ordenado por **valor / esforço**. Cada item tem effort estimate + done criteria 1-line.

### Tier 1 — High value, low/medium effort (next 1-4 weeks)

| Prioridade | Phase | Effort | Done quando |
|---|---|---|---|
| **1** | **User register schtasks** (Phase EE pending) | 5min user action | hourly + q4h tasks visíveis em `schtasks /Query` |
| **2** | **Phase HH-AOW** Budget & Health | 1-2d | Tavily quota allocation + `_health.py` + circuit breaker |
| **3** | **Phase II-AOW** Stream Layer Mini (news RSS hourly) | 1d | News fetch hourly com classifier |
| **4** | **W.1** PDF/XLSX Document Skills | 1-2d | Suno/XP PDF extraction via skill |
| **5** | **W.6.3** LangFuse self-host | 1d | Docker compose + decorator no `ollama_call` |
| **6** | **W.7** skill_scout cron mensal | 0.5d | `agents/skill_scout.py` + monthly report |
| **7** | **U.1** Home minimalista (deprecated React, MC v6.1 cobre) | 0d | ✅ already covered by MC v6.1 |

### Tier 2 — Medium value, medium effort (1-3 months)

| Prioridade | Phase | Effort | Done quando |
|---|---|---|---|
| 8 | **Phase JJ-AOW** Reactive Engine | 2-3d | `event_queue` + react_8k/react_fato handlers |
| 9 | **W.6.4** DSPy piloto risk_auditor | 2d | Trainset + benchmark pre/post |
| 10 | **W.2 (rest)** Playwright + Bigdata fetcher | 2d | `bigdata_fetcher.py` + Calendar/investidor10 |
| 11 | **Phase II-Live Workforce Page** | 1d | MC page mostrando schtasks + locks + Tavily quota |
| 12 | **W.8** Canvas + PPTX quarterly deck | 2-3d | Q1 2026 deck primeiro |
| 13 | **W.10** OpenBB peer integration | 1-2d | A/B 5 BR + 5 US tickers |

### Tier 3 — Aguarda dados / opportunistic

| Prioridade | Phase | Bloqueador | Done quando |
|---|---|---|---|
| 14 | **Phase GG** Capital Deployment Engine | ≥90d validated verdicts | Calibration curve estável; hit rate per-engine claro |
| 15 | **W.9** Remotion weekly video | depende W.5 ✅ + W.8 | Cron Sunday 20h + upload Drive + Telegram |
| 16 | **Phase JJ-AOW Tuning** | depende GG + EE estabilizar | Severity calibrada + Telegram inline buttons |

### Tier 4 — Low priority / explicit defer

- **Phase T** Pip-Boy TUI — deferred, não iniciar sem sinal explícito
- React desktop rewrite — deprecated em U.0, NÃO restart
- Marketing/SEO/Brand skills — out of scope

---

## ❌ Deprecated / superseded

| Doc | Status | Substituído por |
|---|---|---|
| `desktop/` (React + Vite + FastAPI) | DEPRECATED 2026-04-26 | Mission Control Next.js (`mission-control/`) |
| `obsidian_vault/skills/Mission_Control_Design_Roadmap.md` (v3 Broadsheet) | SUPERSEDED 2026-05-07 | MC v5 JPM redesign |
| `obsidian_vault/skills/Phase_Y_Roadmap.md` | MOSTLY SHIPPED | Constitution Y.0-Y.8 entries |
| `Roadmap_Always_On_Workforce.md` (Phase EE proposed) | SHIPPED 2026-05-08 | This doc + [[skills/Phase_EE_Tiered_Scheduler]] |
| `Roadmap_Always_On_Workforce.md` (FF/GG/HH/II/JJ) | LETTERS REUSED | This doc rebadgeia como AOW.FF, AOW.GG, etc para evitar conflito com Phase FF Calibration |
| `obsidian_vault/skills/Roadmap.md` (Phase W) | LIVING | Detail kept; high-level state replicado aqui |
| `HANDOFF_PHASE_Z_UI.md` (root) | DEPRECATED 2026-04-26 | Z shipped (Z.0-Z.7) |

---

## 🧭 Como usar este doc

1. **"O que vamos atacar?"** → Tier 1 queue, ordem 1-7.
2. **"O que já fizemos?"** → § Shipped, cronológico mais recente primeiro.
3. **"Posso esquecer este roadmap antigo?"** → § Deprecated. Ver substituto.
4. **"Como sei se uma phase fechou?"** → Constitution `phases_done` frontmatter + Changelog.
5. **"Onde está a decisão de fazer X?"** → Constitution Decision Log (não duplicado aqui).

## 🔁 Manutenção

- Este doc actualiza-se manualmente quando uma phase entra/sai do queue.
- Constitution actualiza-se a cada commit grande (Changelog).
- Quando há conflito entre os dois, **Constitution wins** (é a fonte de verdade temporal).
- Quando este doc fica desactualizado >7 dias, fazer audit `git log` vs queue + corrigir.
