# Investment Intelligence System — External AI Briefing

> **Audience**: An external AI agent (e.g. another Claude session, a GPT model, Gemini) being asked to give feedback on this system.
> **Goal**: After reading this once, you should have a complete enough mental model to ask sharp questions and challenge architectural decisions. The user (the system's owner) will answer your questions in a back-and-forth.
> **Owner**: A solo private investor in Portugal/Brazil ecosystem.
> **Date of snapshot**: 2026-05-05.

---

## 1. One-paragraph summary

This is a personal investment intelligence system for one human investor operating in two markets in parallel — **Brazil (B3)** and **US (NYSE/NASDAQ)** — with a long-term **DRIP** (dividend reinvestment) strategy and a **Buffett/Graham** philosophy (quality, margin of safety, dividends). It is **not** a trading system, not a robo-advisor, and not a SaaS product. It is a single-user "second brain" that ingests market data, public filings, books, YouTube analyst calls, and paid newsletters; runs them through a battery of local LLMs (Ollama) plus deterministic scoring engines; and surfaces decisions through a CLI, an Obsidian vault, a localhost Next.js dashboard, and a Telegram bot. The single most distinctive choice is **local-first**: a dedicated always-on PC with an RTX 5090 runs Qwen 2.5 14B/32B and Llama 3.3 70B for ~95% of cognitive work, so that the Claude API (and any paid LLM) is the **last** resort, not the first.

---

## 2. Who built this and how they work

- **Profile**: Solo private investor, software-literate but not a professional engineer. Treats this codebase as a personal "operating system for capital allocation".
- **Markets**: Real positions in both Brazil (B3 stocks, FIIs) and US (stocks, ETFs). Cash in BRL stays in BRL; cash in USD stays in USD. The system is hard-coded never to suggest converting between accounts.
- **Strategy**: DRIP-first (compounding via dividend reinvestment), with a smaller "growth" sleeve (e.g. XP Inc., Brookfield post-split) and a tactical hedge sleeve. No options, no leverage, no day-trading.
- **Hardware**: Always-on PC. Ryzen 9 9800X3D + RTX 5090. Ollama runs locally with Qwen 2.5 14B (default), Qwen 2.5 32B (heavier reasoning, e.g. the chief-of-staff agent), and Llama 3.3 70B (optional, only for the deepest dossier pass).
- **Working style**:
  - Operates the system in three modes: **interactive** (chat, CLI, dashboard), **workday autonomous** (~2h "I'll be away, run idempotent enrichment + cleanup"), and **midnight autonomous** (8–9h overnight backfills).
  - Strong preference for surgical changes over refactors. "If 200 lines can be 50, rewrite. Don't generalize for hypothetical futures."
  - Strong preference for terse, decision-grade output. The terminal is "the boss's room"; the Obsidian vault is "the office where things are polished".

---

## 3. The non-negotiable principles

These are the bedrock; the system is designed around them. Challenge them at your discretion.

1. **In-house first.** Anything that can run locally (SQL, Ollama, an existing Python script) must run locally. Claude / GPT / paid frontier models are the **last** resort. Tavily (web research) is the **only** paid external dependency that is accepted, and even that is rate-limited to 100/day, cached 7 days, and gated behind a fallback that returns gracefully when quota is hit. **Reason**: token economics + privacy + offline resilience + intellectual independence (the system shouldn't be a thin wrapper over a vendor).

2. **Two databases, never mixed.** `data/br_investments.db` and `data/us_investments.db` have *identical* schemas but live in separate files. Currency, timezone, and source authority are isolated. This costs duplication but eliminates an entire class of bugs.

3. **Universe lives in YAML, never in code.** `config/universe.yaml` is the single source of truth for "what tickers do we follow". Any Python file that hard-codes a ticker is a bug.

4. **Fetchers are independent and idempotent.** Each fetcher knows how to talk to *one* source. The scoring engine never makes a network call. Re-running any fetcher is safe.

5. **Three-layer brain.**
   - **L1** = SQLite (raw, machine-readable, authoritative).
   - **L2** = Obsidian vault auto-generated markdown (machine-derived, regenerable).
   - **L3** = Obsidian vault human-curated markdown (theses, decisions, journals — never overwritten by automation).
   This separation prevents the most common 2nd-brain failure mode: automation eating the human's notes.

6. **Terminal = chefe; Obsidian = escritório.** The CLI is for raw action, no ceremony. The vault and dashboards are for consumable, polished output. Pretty UIs do not replace the CLI; they sit on top of it.

7. **Every recommendation is auditable.** Each dossier has an evidence ledger (each metric tagged with source + URL + date). Each decision is versioned (`data/dossier_snapshots/`). Each AI-generated thesis is tagged `auto_draft: true` until a human accepts it.

---

## 4. Architecture: how a ticker actually becomes a verdict

This is the most useful section to internalize. Walk through how, say, **ACN (Accenture)** flows from raw web data to a recommendation.

### Step 1 — Universe declaration
ACN is listed in `config/universe.yaml` under the US watchlist with sector "IT Services" and `is_holding: true`.

### Step 2 — Fetch (idempotent, fallback-aware)
- Primary: `yfinance` (no auth) pulls price history, fundamentals, dividends.
- Fallback: Massive.com (ex-Polygon) for intraday and corporate actions.
- Filings: SEC EDGAR monitor pulls 8-K, 10-K, dividend declarations.
- Dispatch is declarative via `config/sources_priority.yaml`; orchestrated by `fetchers/_fallback.py::fetch_with_fallback(market, kind, ticker)`.
- Each fetch goes through a TTL cache (`data/api_cache.db`). Quality returned as a `FetchResult` enum: OK / WARNING / DEGRADED / CRITICAL with `age_hours`.

### Step 3 — Persist to SQLite (L1)
Tables touched: `companies`, `prices`, `fundamentals`, `events`, `deep_fundamentals`, `quarterly_history`. Schemas are identical between BR and US DBs.

### Step 4 — Run the scoring engines (deterministic, no LLM)
For ACN this means:
- **Buffett US screen**: P/E ≤ 20, P/B ≤ 3, DY ≥ 2.5%, ROE ≥ 15%, ≥10y dividend streak.
- **Moat score** (`scoring/moat.py`): 0–10 composite of pricing power (gross margin level + stability), capital efficiency (ROIC level + persistence), reinvestment runway (revenue CAGR + FCF/NI), scale durability (op-margin trend + buybacks). Banks, Holdings, REITs, FIIs are excluded by design.
- **Dividend safety**: 0–100 forward-looking score. REIT-aware (different formula).
- **Altman Z-Score**: distress flag (veto if too low).
- **Piotroski F-Score**: 0–9 quality score (veto if F ≤ 3).
- **Beneish M-Score**: 8 indices for accounting manipulation. Excludes banks/REITs.

These are pure Python, no network, fully reproducible.

### Step 5 — Run the strategy engines (LLM-optional)
Five engines in `strategies/`:
- **graham** (classic Graham number / value)
- **buffett** (quality)
- **drip** (dividend compounding payback)
- **macro** (regime overlay — see §6)
- **hedge** (tactical hedge proposal)

Each emits a `StrategyOutput { score: 0..1, verdict: BUY|HOLD|AVOID|N/A, rationale: dict }`. Run via `ii strategy <engine> <ticker>` or all-at-once via `ii allocate`.

### Step 6 — Combine into an allocation proposal
`ii allocate` runs all five engines in parallel, combines via fixed bucket weights (graham 25 / buffett 30 / drip 20 / macro 15 / hedge 10), applies a sectoral overlay, and emits `AllocationProposal { target weights, conflicts, hedge proposal }`.

### Step 7 — Synthetic IC debate (LLM, local)
`agents/synthetic_ic.py` runs 5 personas — **Buffett, Druckenmiller, Taleb, Klarman, Dalio** — against the ticker's evidence pack. They debate, vote, and emit a majority opinion with dissents. Each call is one Qwen 14B inference per persona (5 total). Tavily can be wired to inject 14-day recent news.

### Step 8 — Variant perception (LLM + web)
`agents/variant_perception.py` compares **our view** vs **analyst consensus** (pulled from subscriptions DB + Tavily web research). Emits a "we vs them" matrix with the spread.

### Step 9 — Council STORYT_3.0 dossier (LLM-heavy)
`agents/council/story.py` — the heaviest pipeline:
- Research Brief (analyst_insights + events + videos + Bibliotheca + Tavily)
- Peer Engine (real medians from the DB, not made-up)
- Evidence Ledger (each metric annotated with source + URL)
- Versioning (`data/dossier_snapshots/`)
- Delta Engine (auto-diff vs prior version)
- Specialists with named personas (Tião Galpão, Aderbaldo Cíclico, Hank Tier-One, Walter Triple-Net, Mariana Macro, Pedro Alocação, Charlie Compounder, Lourdes, Valentina) — 9 specialists + 2 cross-cutting roles.
- Smart cache (`agents/council/cache_policy.py`) skips the run if nothing material has changed (~95s saved/run).

End-to-end ~100s, ~20k characters with ~19 evidence entries.

### Step 10 — `ii deepdive`
The "V10 Personal Equity Valuator". 4 layers in parallel:
1. **Auditor** (Piotroski + Altman + Beneish + Moat)
2. **Scout** (yfinance: news, insider, short interest, consensus)
3. **Historian** (delta vs prior dossier)
4. **Strategist** (Llama 3.3 70B optional — 5k-word narrative)

Output: JSON in `reports/deepdive/` and optional Markdown in the vault.

### Step 11 — Human in the loop
The verdict (BUY / HOLD / AVOID) plus dossier surfaces in:
- The CLI (`ii verdict ACN`)
- The Mission Control dashboard (`/ticker/ACN` page with chart, fundamentals, position, action buttons)
- The Obsidian vault (`obsidian_vault/dossiers/ACN.md`)
- The Captain's Log Telegram push

Nothing buys/sells real shares. The system ends at a recommendation; the human places orders manually in the broker.

---

## 5. The 12 core systems

A flat list of what's actually in the repo, with depth where it matters.

### 5.1 Universe & databases
- `config/universe.yaml` — single source of truth, ~250 tickers across BR + US + watchlists.
- `data/br_investments.db` and `data/us_investments.db` — SQLite, identical schemas.
- Key tables: `companies`, `prices`, `fundamentals`, `deep_fundamentals` (extended), `quarterly_history` (CVM ITRs for BR, 10-Q for US), `bank_quarterly_history` (NII, PDD, fees, efficiency for banks BR), `events` (filings), `scores`, `strategy_runs`, `paper_trade_signals`, `analyst_reports`, `analyst_insights`, `chunks_index` (RAG embeddings), `agent_decisions` (governance audit), `portfolio_positions` (real holdings).

### 5.2 Fetchers
- `fetchers/yf_br_fetcher.py`, `fetchers/yf_us_fetcher.py` — primary.
- `fetchers/sec_edgar_fetcher.py` — US filings.
- `fetchers/massive_fetcher.py` — US fallback (ex-Polygon).
- `fetchers/bcb_fetcher.py` — Brazilian Central Bank macro series (Selic, CDI, IPCA, USDBRL).
- `fetchers/fred_fetcher.py` — US FRED (DGS10, etc.).
- `fetchers/fiis_fetcher.py` — Brazilian REIT specifics.
- `fetchers/yf_deep_fundamentals.py` — extended fundamentals (cashflow, balance sheet detail).
- `monitors/cvm_monitor.py`, `monitors/sec_monitor.py` — daily filing scrapers.
- `monitors/cvm_pdf_extractor.py` — downloads + parses CVM PDFs (pdfplumber).

### 5.3 Scoring engines (deterministic)
All in `scoring/`:
- `engine.py` — main entry. Per-market, per-sector logic (Graham BR non-financial, banks BR, banks US, Buffett US).
- `moat.py` — 0–10 composite (4 sub-scores).
- `dividend_safety.py` — 0–100 forward-looking, REIT-aware.
- `altman.py` — Z-Score distress.
- `piotroski.py` — F-Score 0–9 quality.
- `beneish.py` — M-Score accounting manipulation.

### 5.4 Strategy engines (5)
All in `strategies/`. Each is a class that takes a ticker and emits `StrategyOutput`. Run individually via `ii strategy <engine> <ticker>` or combined via `ii allocate`.

### 5.5 Macro classifier
`analytics/regime.py` classifies the current macro regime per market (BR + US) from interest-rate, inflation, yield-curve, and growth proxies. Emits one of: expansion / late_cycle / recession / recovery. Drives the `macro` strategy engine and the `hedge` engine (hedge OFF in expansion, 5% size in late_cycle, 10% in recession).

### 5.6 Perpetuums (12 autonomous loops)
A "perpetuum" is a long-running, idempotent agent that scans the system for signals and proposes actions. Inspired by background daemons but explicitly LLM-aware.

Each perpetuum has an **autonomy tier**:
- **T1 Observer** — surfaces signals, proposes nothing.
- **T2 Proposer** — proposes actions with verifiable `action_hint`. Human approves/rejects via `ii perpetuum-review`.
- **T3 Whitelisted Executor** — executes a narrow whitelist of safe actions (e.g. "regenerate this auto-draft wiki page").
- **T4** — broader execution, still bounded.
- **T5** — reserved, not in use.

The 12 active perpetuums:
1. **thesis** — keeps thesis coverage across the universe (currently 184/184 = 100%).
2. **vault** — vault sync drift detection.
3. **data_coverage** — finds missing fundamentals / dividend history / quarterly history.
4. **bibliotheca** — librarian-quality (sector backfill, name normalization, orphan detection).
5. **content_quality** — checks vault notes for staleness, broken links.
6. **methods** — extracts methods from books and matches against portfolio.
7. **token_economy** — tracks Claude/Tavily usage, alerts on outliers.
8. **library** — re-ingests new books / clippings.
9. **meta** — meta-perpetuum that checks the other perpetuums.
10. **ri_freshness** — CVM filings freshness per BR ticker.
11. **autoresearch** — top-30 conviction subjects get Tavily web-research weekly (cooldown 6 days).
12. **code_health** — scans the codebase for anti-patterns CH001–CH007 (e.g. "hard-coded ticker outside YAML").

Daily run: `daily_run.bat` at 23:30 (Windows scheduled task) → fetchers → strategy_runs → perpetuum_master → captains_log_telegram → log rotation.

### 5.7 Agents (named, LLM-driven)
Beyond perpetuums, named agents do specific reasoning tasks:
- **Antonio Carlos** (chief of staff) — `agents/chief_of_staff.py`. Tool-calling Qwen 2.5 32B with 16 tools: verdict, deepdive, position, regime, portfolio, IC, variant, web, etc. Conversational memory per `chat_id` in `data/chief_memory.db`. Reachable via Telegram (free-form) or CLI. Embedded in Mission Control as a 🐙 chat widget.
- **Synthetic IC** — 5 personas (Buffett, Druck, Taleb, Klarman, Dalio).
- **Variant Perception** — we vs analyst consensus.
- **Council STORYT_3.0** — full dossier pipeline with named specialists.
- **Holding Wiki Synthesizer** — generates `auto_draft: true` wiki stubs.
- **Earnings Prep** — pre-call briefs (Tavily-grounded for upcoming events).
- **Decision Journal Intel** — aggregates patterns across perpetuum decision logs.
- **Mega Auditor** — codebase cruft detector (8 categories). Audit-only T1; manual `--bury` to quarantine.
- **Helena Mega** — design-system auditor for the UI layer.

### 5.8 Bibliotheca (book → method → paper trade)
- `library/ingest.py` ingests PDFs → chunks.
- `library/extract_insights.py` uses Ollama to extract investing methods (e.g. "Magic Formula", "Net-Net", "Buffett quality screen").
- `library/matcher.py` matches methods against the universe → emits `paper_trade_signals` (long/short/screen, with entry conditions).
- `library/rag.py` builds an embedding index (nomic-embed local) and supports semantic search and Qwen-synth Q&A.
- **Discipline rule**: nothing turns into real capital until the method has 30+ closed paper signals with win-rate > 60%. Currently ~1300+ paper signals open, none yet validated. This is intentional friction.

### 5.9 RI / CVM pipeline
- `library/ri/cvm_parser.py` — non-bank Brazilian companies (DRE/BPA/BPP/DFC standard CVM account codes).
- `library/ri/cvm_parser_bank.py` — banks (BACEN schema, `ds_conta`-based because each bank uses different `cd_conta`).
- `library/ri/quarterly_single.py` — resolves the YTD artifact (Qn single = ITRn − ITRn-1).
- `library/ri/fii_filings.py` — FII monthly disclosures (NAV, DY, cotistas).
- `library/ri/catalog_autopopulate.py` — matches universe.yaml tickers against `cad_cia_aberta.csv` to auto-populate the catalog.

### 5.10 YouTube ingest pipeline
- `scripts/yt_ingest.py` — single video.
- `scripts/yt_ingest_batch.py` — channel batch.
- Whisper local for transcription.
- Ollama local for re-extraction (no Claude tokens).
- `scripts/yt_digest.py` — SQL-only digest (zero LLM calls).
- Captures Brazilian and US analyst calls / podcasts. Phase Q v2 added transcript cache + anti-broker prompt + validator rules.

### 5.11 Subscriptions ingest
- `fetchers/subscriptions/` — Suno (BR research house), XP (BR broker), WSJ, Finclass.
- Cookie-based scraping, exports to `analyst_reports` + `analyst_insights` tables.
- Surfaces in `ii panorama <ticker>` and the Captain's Log.

### 5.12 Front-ends (4 surfaces)
1. **CLI `ii`** — Click-based, ~80 sub-commands. Direct, zero ceremony. The "boss's room".
2. **Mission Control Next.js** — `cd mission-control && npm run dev` → `localhost:3000`. 7 panes: Home / Tasks / Content / Calendar / Projects / Memory / Docs / Team. Plus a `/visual` pixel-art Office (each agent as a sprite with live status) and a `/ticker/<TK>` deep page. Reads SQLite + vault directly (zero mock data). Webpack mode (better-sqlite3 incompatible with Turbopack).
3. **Obsidian vault** — `obsidian_vault/`. The "office". Wikis (holdings, sectors, playbooks, macro), dossiers, glossary, knowledge cards, Bibliotheca, Captain's Log, Constitution.
4. **Telegram bot Jarbas** (`@TheJarbas123_bot`) — daily push of Captain's Log + free-form chat with Antonio Carlos.

---

## 6. The autonomy model in detail

This is the most opinionated part of the system. External feedback here is especially valuable.

- **Cron-driven backbone.** Daily 23:30 scheduled task runs the full pipeline. The PC must be awake (not sleeping).
- **Workday autonomous mode.** When the user says "I'll be away 2h, do X", the agent is allowed to: enrichment, idempotent re-runs, vault writes (auto-draft only), commits with descriptive messages. **Forbidden**: writes to `data/`, force-push, exceeding Tavily quota.
- **Midnight autonomous mode.** 8–9h overnight. Same rules as workday but allowed to consume the full daily quota of paid services. Required deliverable: `obsidian_vault/Bibliotheca/Midnight_Work_<DATE>.md` with concrete metrics.
- **Constitution.** `obsidian_vault/CONSTITUTION.md` is the master vivendo doc: identity + 6 non-negotiables + architecture + phase history + decision log + open issues + changelog. **The first thing read when returning after a pause.** Has a "🚪 Voltamos" section at the top — when the user says "Voltamos" or a variant, the synthesis there is the entry point (no fresh audits, no re-exploration).
- **Decision journal.** Every non-trivial decision gets a row. Perpetuums are required to leave verifiable `action_hint`s. If the success criterion can't be measured, the action stays at T1.
- **Evidence ledger.** Every dossier appendix lists each metric with source + URL + as-of date. No hallucinated numbers.
- **Versioning of dossiers.** `data/dossier_snapshots/<TK>/<DATE>.json`. The Delta Engine auto-generates a diff vs prior on every refresh.
- **Smart cache.** Dossier fingerprinting; skip the LLM-heavy run if nothing material changed.

---

## 7. Tech stack

- **Languages**: Python 3.11+ (90% of the codebase), TypeScript/React (Mission Control), Bash (cron glue), some PowerShell.
- **DB**: SQLite (intentional — no Postgres, no warehouse).
- **LLM (local)**: Ollama. Models: `qwen2.5:14b` (default), `qwen2.5:32b` (heavy reasoning), `llama3.3:70b` (optional, ~40GB).
- **LLM (paid, gated)**: Claude API (last resort, never first), Tavily (web research, only paid external dep).
- **Embeddings**: `nomic-embed-text` local.
- **ASR**: Whisper local.
- **Front-end**: Next.js 14 (Mission Control), Streamlit (legacy `ii dashboard`).
- **Notifications**: Telegram Bot API, Windows Toast (`scripts/notify_events.py`).
- **Charting**: Recharts (Mission Control), matplotlib (Streamlit/CLI).
- **MCP servers wired**: `claude.ai Bigdata.com` (financial data), `Status Invest` (BR fundamentals), `Google Drive`, `Google Calendar` (calendar events), `Gmail`. Most are availability-gated on demand.
- **Testing**: pytest. ~7 typed-agents tests, ~60s, 100% offline (Ollama).
- **Versioning**: git. Heavy committing discipline (one commit per concern, descriptive messages).

---

## 8. Current state snapshot (2026-05-05)

**Coverage**:
- Universe: ~250 tickers (BR + US + watchlists)
- Real holdings: 33 positions across BR + US
- Thesis coverage: 184/184 = 100% of universe (mostly via Ollama-generated drafts; high-conviction ones manually curated)
- Conviction scores top: ITSA4=90, ACN=87, BBDC4=92, KO=87, JNJ=88
- Paper trade signals: ~1300+ open, 0 closed-and-validated yet
- CVM quarterly_history: 5 BR stocks fully populated × 11 quarters; bank schema BBDC4 + ITUB4 with 26 rows

**Recent shipped (last 2 weeks)**:
- **Moat Engine** (`scoring/moat.py`) — 0–10 composite, wired in `ii deepdive`. Calibrated: JNJ 8.75 / KO 8.5 / ACN 8.0 STRONG; PETR4 6.25 NEUTRAL.
- **Council STORYT_3.0** — full dossier pipeline with versioning, delta engine, smart cache.
- **Mission Control v3 broadsheet design** — sprint 1 shipped (FT/WSJ tokens, light/dark theme, 11 components refactored). Sprint 2 (page-by-page editorial pass) pending.
- **Tavily wired in 3 places**: variant_perception, earnings_prep, synthetic_ic.
- **Bank Quarterly schema** — BBDC4 + ITUB4 with NII/PDD/efficiency revealing material findings (BBDC4 NII +16% YoY, NI +31% recovery; ITUB4 NII flat).
- **Phase J** — universe thesis at 100%, bank balance-sheet extension (10 BS columns).
- **Antonio Carlos** chief-of-staff agent with 16 tools and conversational memory.

**Open issues / known weak spots**:
- Variant perception revealed bias in auto-populated theses (overnight runs). The fix path is "human review queue" but it's not yet built.
- Paper-trade validation pipeline has no ground-truth comparison engine yet — signals just sit in `paper_trade_signals.status='open'` indefinitely.
- yfinance is a single point of failure for 70% of fetches. Massive.com fallback exists for US but not BR.
- The 12 perpetuums occasionally produce conflicting actions (e.g. data_coverage proposes a fetch that bibliotheca then immediately marks as orphan). No formal conflict resolution layer.
- Mission Control is fast but has zero auth — only safe because it binds to localhost. Tailscale exposure is on the roadmap but not yet enabled.
- Decision quality is not yet measured. We have prediction logs and a `predictions_evaluate.py` cron, but no calibration curve, no Brier score, no ground-truth backtest of "what did we recommend BUY 6 months ago and how did it actually do".

---

## 9. Where external feedback is most valuable

These are the questions the user most wants challenged. Treat them as starting points, not a closed list.

### A. Calibration & overfitting
1. The scoring engines (Graham BR, Buffett US, bank-specific) use thresholds. Are they literal from the source books, or were they tuned on this user's universe? If tuned — with what holdout? How do we know they're not overfit to a regime that already passed (e.g. low-rate 2010s for the Buffett US screen)?
2. The Moat Engine is a 4-sub-score composite. Is the weighting (and the choice of those 4 sub-scores vs alternatives like distribution, switching costs, network effects) defensible, or just convenient given available data?
3. The macro regime classifier outputs one of 4 labels per market. Is a 4-state discrete classifier the right model, or should it be a continuous risk-on/risk-off score?

### B. Data robustness
4. yfinance is the primary source for ~70% of fetches. What's the failure mode when it breaks? Is there a ground-truth check (e.g. spot-check 5 random fundamentals against SEC EDGAR XBRL) that runs automatically?
5. The CVM bank parser uses `ds_conta` (description) instead of `cd_conta` (code) because each bank uses different codes. This is fragile to wording changes. Is there a more durable identifier strategy?
6. The Beneish M-Score and Piotroski F-Score require ~3 years of clean fundamentals. For tickers with thin history (newer listings, recent IPOs), the score returns N/A. Is "N/A" the right default, or should it return a noisy estimate with a confidence flag?

### C. The autonomy model
7. The 12 perpetuums each have their own logic. Is this the right granularity, or should they collapse into 3–4 with shared infrastructure?
8. The autonomy tier system (T1–T5) gates execution authority. But the boundary between T1 and T2 is fuzzy in practice — many perpetuums say "T1 observer" but emit `action_hint`s that look like T2 proposals. Is this drift acceptable or a smell?
9. Overnight autonomous mode runs 8–9h and is allowed to commit. What's the rollback strategy if a midnight run corrupts the vault? (Currently: git, but the user has to notice.)
10. The Constitution + decision journal + evidence ledger together form an audit trail. Is this enough, or should there be a separate "post-mortem" cadence (e.g. monthly: "of the BUY recommendations 90 days ago, how did they perform?")?

### D. Decision quality (the big one)
11. There is currently **no closed-loop evaluation** of recommendations. We have `predictions_evaluate.py` for analyst predictions, but not for our own. How would you build a calibration system that doesn't itself become a source of overfit (e.g. retraining the scoring engines on past hits)?
12. The Synthetic IC debate (5 personas) feels useful but has never been validated. Are the 5 voices producing genuinely different reasoning, or are they all just Qwen 14B with different system prompts producing 5 variants of the same output?
13. The Variant Perception agent compares "us vs analyst consensus". But "us" is itself a multi-engine output. What does it mean to disagree with consensus when our own internal engines disagree with each other?

### E. Architectural smells
14. Two SQLite DBs with identical schemas — is the duplication worth it, or should there be a single DB with a `market` column and a strict CHECK constraint?
15. The "in-house first" rule pushes 95% of work to local Qwen 14B. Are we leaving quality on the table for tasks where Claude/GPT-4 would be 5× better and the cost is negligible (e.g. one-shot dossier generation)?
16. The Bibliotheca has ~1300 open paper-trade signals and 0 closed-validated. At what point is the "30+ closed signals at 60% win rate before real capital" rule producing analysis paralysis vs intellectual honesty?
17. Mission Control + Streamlit + CLI + Telegram + Obsidian = 5 surfaces. Is this fragmenting attention, or is each genuinely earning its place?

### F. Strategy
18. The system is dogmatically DRIP + Buffett/Graham. In a regime where dividend stocks have underperformed (e.g. mega-cap growth dominance 2017–2023), the philosophy itself was the bottleneck, not the implementation. How would the system know if the philosophy is wrong, vs the implementation is suboptimal?
19. The sleeve split (DRIP core / growth tactical / hedge) has fixed bucket weights. Should those be dynamic based on regime or own-conviction? If yes, how without becoming a market-timer?
20. BR and US are run in strict isolation. But the user is one human with one portfolio total. Is the lack of a unified currency-translated view a feature (avoids meaningless apples-to-oranges) or a bug (no global allocation lens)?

---

## 10. Glossary of project-specific terms

- **DRIP** — Dividend Reinvestment Plan. Compounding via reinvested dividends.
- **DY** — Dividend Yield (annualized, trailing).
- **FII** — Fundo de Investimento Imobiliário. Brazilian REIT equivalent.
- **CDI / Selic** — Brazilian short-term interbank / policy rates.
- **CVM** — Comissão de Valores Mobiliários. Brazilian SEC.
- **ITR** — Informação Trimestral. Brazilian quarterly filing.
- **DRE / BPA / BPP / DFC** — Brazilian standard income statement / balance sheet / cash flow statement codes.
- **BACEN** — Banco Central do Brasil. Brazilian Fed.
- **Bibliotheca** — internal name for the books → methods → paper-trades pipeline.
- **Captain's Log** — daily Telegram + Streamlit page summarizing perpetuum signals + IC + variant + RI changes.
- **Constitution** — `obsidian_vault/CONSTITUTION.md`. Master living doc.
- **Council STORYT_3.0** — full dossier pipeline with named specialists.
- **Helena** — design-system auditor agent for the UI layer.
- **ii** — the CLI entry point (`ii panorama X`, `ii deepdive X`, `ii allocate`).
- **Jarbas** — Telegram bot handle (`@TheJarbas123_bot`).
- **L1 / L2 / L3** — the 3-layer brain (SQLite raw / vault auto / vault humano).
- **Mega Auditor** — codebase cruft detector. Audit-only T1.
- **Mission Control** — Next.js dashboard at localhost:3000.
- **Moat Score** — 0–10 composite of 4 sub-scores.
- **Panorama** — super-command aggregating verdict + peers + triggers + notes + videos + analyst views.
- **Perpetuum** — long-running idempotent autonomous agent.
- **Phase X / AA / DD / EE** etc. — chronological "shipping epochs". Each phase has a closing report.
- **STORYT_3.0** — naming for the council-driven dossier pipeline (vs prior STORYT 1/2).
- **Synthetic IC** — 5-persona Investment Committee debate.
- **T1 / T2 / T3 / T4 / T5** — autonomy tiers.
- **Tier C / Compounder** — internal classification of holdings (Compounder, DRIP, Tactical, Growth, Turnaround, Hedge).
- **Variant Perception** — we vs analyst consensus.
- **Verdict** — final aggregate output: BUY / HOLD / AVOID / N/A.

---

## 11. How to engage with this document

If you are an external AI agent reading this, the user wants:

1. **Sharp questions, not vague encouragement.** Pick 3–5 things from §9 that you think are most worth interrogating, and ask hard follow-ups.
2. **Don't summarize back what you read.** The user already knows the system. Your value is the *outside* view.
3. **Concrete attack vectors.** "Your Moat Engine has a survivorship bias because it depends on ≥3 years of fundamentals" is more useful than "consider edge cases".
4. **Comparisons welcome.** If you've seen a system solve a similar problem differently (e.g. how Bridgewater handles regime classification, how Renaissance handles fundamentals robustness, how Notion's second-brain users handle L2/L3 separation), name it. The user can read.
5. **Push back on the philosophy.** Especially questions in §9.F (Strategy). The user is open to being told the framework itself has a bug, not just the implementation.

The user will reply to your questions in plain language and may grant you read-access to specific files (CLAUDE.md, Constitution, specific scripts) on request. Ask for what you need.

---

*End of briefing. Total system: ~250 Python modules, ~12 perpetuums, ~16 named agents, 4 front-end surfaces, 2 SQLite DBs, 1 human.*
