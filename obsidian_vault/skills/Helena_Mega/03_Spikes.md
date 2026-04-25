---
type: platform_spikes
updated: 2026-04-25
owner: helena_linha
tags: [platform, spikes, helena, mega, architecture]
---

# 03 — Platform spikes (4 paths)

> Helena Mega · run **2026-04-25** · 4 caminhos avaliados.

## Critério de decisão

Para cada path: **stack**, **o que reusa do código actual**, **passos de migração concretos**, **estrutura de pastas final**, **comando de build**, **custo weekly**, **limitações honestas**, **veredicto**.

## Sumário

| Path | Título | Tecto | Semanas | Veredicto rápido |
|---|---|---|---:|---|
| **A** | Streamlit perfectionism | Tasteful internal tool (8/10) | 1 | Cheapest viable. Hits a real ceiling at 8/10. Pick if budget < 1 sprint.… |
| **B** | Tauri desktop app  (RECOMMENDED) | Native product feel (10/10) | 3-4 | Highest ceiling. Reuses 100% of Python backend. Sells like a real product. 3-4 weeks hones… |
| **C** | Next.js + FastAPI (web app, PWA) | Real web product (9/10) | 3-4 | Same backend reuse as B. Wins on mobile + accessibility from anywhere. Loses on 'feels lik… |
| **D** | Obsidian-native + static HTML reports | Polished knowledge worker setup (8/10 in different dimension) | 1-2 | Cheapest path with high aesthetic ceiling. Different shape than B/C — doesn't try to be a … |

## Path A — Streamlit perfectionism

**Tecto**: Tasteful internal tool (8/10)  · **Custo**: 1 semanas  · 
**Build**: `streamlit run scripts/dashboard_app.py  (no build step)`

### Stack

- Streamlit 1.x (current)
- Plotly + ii_dark template
- scripts/_theme.py + scripts/_components.py (existing)
- Custom CSS injection (existing)

### O que se reusa do código actual

- 100% backend (SQLite, fetchers, scoring, agents) — zero changes
- All current pages (Portfolio, Ticker, Triggers, Screener, etc.)
- Helena Design System v1.0 (already in place)

### Passos de migração

- Run `python -m agents.helena.audit` → fix every error in the report
- Refactor `dashboard_app.py` lines 247, 229, 232, 273 (audit findings)
- Replace 5× `template='plotly_white'` with `ii_dark` (DS005 hits)
- Replace 5× hex literals out of palette (DS006 hits) with COLORS[…]
- Tighten 2× section_caption with >8 words (DS008 hits)
- Add `hide_streamlit_branding` CSS (footer 'Made with Streamlit', menu hamburger)
- Add custom 404/error templates
- Test in 720p / 1080p / 1440p viewports — accept narrowest as canonical

### Estrutura de pastas

```
scripts/
  _theme.py             ← already exists
  _components.py        ← already exists
  dashboard_app.py      ← refactor in place
  pages/
    portfolio.py        ← extract from monolith
    ticker.py
    youtube.py
    triggers.py
    screener.py
```

### Build

```bash
streamlit run scripts/dashboard_app.py  (no build step)
```

### Custo weekly

Zero infra. Existing cron at 23:30 already updates data.

### Limitações

- Streamlit chrome leaks (sidebar widgets aesthetic, `st.button` look)
- No fluid mobile — sidebar collapses but feels desktop-first
- Cannot ship as `.exe` / `.app` / `.pwa`
- Slider/dropdown styling only customizable to a point

### Veredicto

Cheapest viable. Hits a real ceiling at 8/10. Pick if budget < 1 sprint.

## Path B — Tauri desktop app  (RECOMMENDED)

**Tecto**: Native product feel (10/10)  · **Custo**: 3-4 semanas  · 
**Build**: `Dev:  cd desktop && pnpm tauri dev`

### Stack

- Tauri 2.x (Rust shell + system WebView)
- Frontend: React 18 + Vite + TypeScript
- Design tokens: translate scripts/_theme.py → src/tokens.css
- Backend sidecar: FastAPI (Python) bundled via PyInstaller
- Charts: Plotly.js (mirror ii_dark template) OR ECharts / Recharts
- State: TanStack Query (React Query) + Zustand for local UI state

### O que se reusa do código actual

- 100% Python backend (SQLite, fetchers, scoring, agents) — exposed via FastAPI
- All scoring logic, perpetuums, library, paper signals — unchanged
- Helena Design System v1.0 — translated to CSS custom properties + Tailwind config
- Plotly templates → mirror in JS (`scripts/_theme.py` becomes `src/lib/plotly_theme.ts`)

### Passos de migração

- **Sprint 1 — scaffold:**
  - • `cargo install tauri-cli`; `pnpm create tauri-app`
  - • Create `desktop/` directory at repo root
  - • FastAPI backend: `desktop/backend/main.py` exposing /api/positions, /api/verdict/{ticker}, …
  - • Translate `scripts/_theme.py` COLORS → `desktop/src/tokens.css` :root vars
- **Sprint 2 — core pages (Portfolio + Ticker + Triggers):**
  - • React routes + Helena components (`<KPITile/>`, `<StatusPill/>`, `<SectionHeader/>`)
  - • Plotly.js charts using ii_dark template ported to TS
  - • TanStack Query hooks against FastAPI endpoints
- **Sprint 3 — remaining pages + polish:**
  - • YouTube / Screener / Perpetuum Health / Actions Queue
  - • Tauri native menu, system tray, notifications (replace Telegram for in-front-of-PC)
  - • Sidecar packaging: PyInstaller bundle FastAPI as `helena-backend.exe`
  - • `tauri build` produces `helena.exe` installer (~30MB)
- **Sprint 4 — hardening + ship:**
  - • E2E tests (Playwright)
  - • Auto-update via Tauri updater (if we want)
  - • Sign + notarize (optional for personal use)

### Estrutura de pastas

```
investment-intelligence/
  desktop/                              ← NEW
    backend/
      main.py            FastAPI app (`uvicorn main:app`)
      routers/
        positions.py     /api/positions, /api/snapshot
        ticker.py        /api/ticker/{symbol}, /api/verdict/{symbol}
        triggers.py
        agents.py        /api/agents/run/{name}
    src/
      tokens.css         ← from scripts/_theme.py COLORS
      lib/
        plotly_theme.ts  ← mirror of ii_dark
        api.ts           ← TanStack Query client
      components/
        KPITile.tsx      ← mirror of scripts/_components.py
        StatusPill.tsx
        SectionHeader.tsx
        AgentAttribution.tsx
      routes/
        Portfolio.tsx
        Ticker.tsx
        Triggers.tsx
        …
      App.tsx
      main.tsx
    src-tauri/
      tauri.conf.json    ← bundle, sidecar, icon
      Cargo.toml
      src/main.rs        ← spawn FastAPI sidecar on app start
    package.json
    pnpm-lock.yaml

  scripts/                             ← existing, untouched
  agents/                              ← existing, untouched
  data/                                ← existing, untouched
```

### Build

```bash
Dev:  cd desktop && pnpm tauri dev
Prod: cd desktop && pnpm tauri build  → emits desktop/src-tauri/target/release/bundle/msi/*.msi
```

### Custo weekly

Zero infra (local). Tauri auto-update server optional (~$0).

### Limitações

- Adds Rust + Node toolchain to dev environment
- PyInstaller sidecar bloats install (~120MB total) but acceptable
- Plotly.js theme port requires manual sync if ii_dark changes
- No mobile (Tauri Mobile is beta; desktop-first)

### Veredicto

Highest ceiling. Reuses 100% of Python backend. Sells like a real product. 3-4 weeks honest. Pick if 'top quality' is the brief.

## Path C — Next.js + FastAPI (web app, PWA)

**Tecto**: Real web product (9/10)  · **Custo**: 3-4 semanas  · 
**Build**: `Dev:  cd web && pnpm dev   (and `uvicorn backend.main:app --reload`)`

### Stack

- Next.js 14 (App Router) + TypeScript
- Tailwind CSS + Helena tokens
- FastAPI backend (Python)
- Charts: Recharts or Plotly.js
- Deploy: localhost:3000 + Caddy reverse proxy → optional Tailscale
- PWA: next-pwa for installable mobile experience

### O que se reusa do código actual

- 100% Python backend exposed via FastAPI (same as Path B)
- Helena Design System v1.0 → Tailwind config

### Passos de migração

- Same as Path B but no Tauri shell — runs in browser
- PWA manifest enables 'Add to Home Screen' on mobile
- Self-host on Mac Mini / Windows always-on box, expose via Tailscale

### Estrutura de pastas

```
investment-intelligence/
  web/                                ← NEW
    app/                              Next.js App Router
      portfolio/page.tsx
      ticker/[symbol]/page.tsx
      …
    components/                       Helena components in TSX
    lib/api.ts                        TanStack Query client
    public/manifest.json              PWA
    next.config.js
    tailwind.config.ts                ← from scripts/_theme.py
  backend/                            ← shares Path B FastAPI
```

### Build

```bash
Dev:  cd web && pnpm dev   (and `uvicorn backend.main:app --reload`)
Prod: cd web && pnpm build && pnpm start  (or `vercel deploy`)
```

### Custo weekly

Zero if self-hosted. Optional Vercel free tier.

### Limitações

- Browser chrome (URL bar, refresh, etc.) — not 100% native feel
- Network dependency unless PWA service worker caches aggressively
- Deploy story is more friction (Caddy / Tailscale) vs Tauri's installer

### Veredicto

Same backend reuse as B. Wins on mobile + accessibility from anywhere. Loses on 'feels like an app'. Pick if cross-device > native polish.

## Path D — Obsidian-native + static HTML reports

**Tecto**: Polished knowledge worker setup (8/10 in different dimension)  · **Custo**: 1-2 semanas  · 
**Build**: `python scripts/render_report.py --week 2026-W17  → reports/*.html`

### Stack

- Obsidian (existing) + community plugins (Charts, Dataview, Templater)
- Static HTML generator: Jinja2 + Helena CSS tokens (single-file output)
- scripts/obsidian_bridge.py (existing) — extend for richer outputs
- Streamlit kept ONLY for power-user interactive drill-down

### O que se reusa do código actual

- Everything backend (zero change)
- Streamlit for interactive screener / triggers (not the 'platform face')
- Obsidian becomes the canonical reading surface

### Passos de migração

- **Sprint 1 — Obsidian polish:**
  - • Install Kepano theme + Style Settings plugin
  - • Apply Helena tokens via Obsidian CSS snippet (`obsidian.css`)
  - • Wire Charts plugin to read from `data/*.db` via Dataview JS
- **Sprint 2 — Static HTML pipeline:**
  - • `scripts/render_report.py` — Jinja2 template, Helena tokens
  - • Outputs: `reports/weekly_YYYY-MM-DD.html` (single file, embedded CSS,     inline Plotly via plotly-CDN)
  - • Investor letter / quarterly review = HTML files (shareable, printable)

### Estrutura de pastas

```
investment-intelligence/
  obsidian_vault/
    .obsidian/snippets/
      helena-tokens.css       ← NEW
      helena-typography.css   ← NEW
    dashboards/
      My Portfolio.md         ← existing, polish
      Holdings.md
      …
  reports/
    weekly_2026-04-25.html    ← single-file artifact
    quarterly_Q1_2026.html
  scripts/
    render_report.py          ← NEW (Jinja2)
    obsidian_bridge.py        ← extend
```

### Build

```bash
python scripts/render_report.py --week 2026-W17  → reports/*.html
```

### Custo weekly

Zero. No new infra.

### Limitações

- No 'single dashboard' — split between Obsidian (reading) + Streamlit (drill) + reports
- Live data requires either Obsidian Dataview JS or refresh script
- Won't sell as 'a platform' — it's a knowledge worker rig

### Veredicto

Cheapest path with high aesthetic ceiling. Different shape than B/C — doesn't try to be a product, leans into 'investor's desk' metaphor. Pick if you want polish in 1-2 weeks and accept the hybrid surface.

## Recomendação Helena

Founder pediu **'top quality, mega Helena'**. Pelo critério dele, Path B (Tauri) é o fit:

1. Dá tecto 10/10 (sente-se a produto, não a script + CSS).
2. Reusa 100% do backend Python (zero re-escrita de fetchers/scoring/agents).
3. Helena Design System v1.0 traduz-se 1:1 para CSS tokens.
4. Claude Design (Anthropic Labs) entra como prototyping per `Claude_Design_Integration.md` — output HTML cola com nosso React.
5. 3-4 semanas honestas é razoável para um vibe-coder com auto mode.

**Plano B se 4 semanas é demasiado**: combinar Path A (1 sprint Streamlit perfeccionismo, fix dos errors do audit) + Path D (Obsidian polish + reports HTML). Total 2-3 semanas para intermediate ceiling 8/10 sem stack nova.

## Decisão pendente do founder

- [ ] **Path B (Tauri) começa já?** — Helena Mega cria branch `phase-z-tauri`, Sprint 1 scaffold em ~3 dias.
- [ ] **Path A+D fallback?** — 1 sprint cada, ship antes de duas semanas.
- [ ] **Outra combinação**? Documentar aqui.

## Cross-links

- [[01_Audit]] — violações actuais (input para Path A)
- [[02_Curation]] — skills relevantes para cada path
- [[Claude_Design_Integration]] — prototyping flow comum a todos paths
- [[Design_System]] — fonte dos tokens
