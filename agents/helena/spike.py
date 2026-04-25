"""spike — feasibility sketches for the 4 platform paths.

Path A — Streamlit perfectionism (current floor + 1 sprint)
Path B — Tauri desktop app (Rust shell + WebView + React)        ← recommended
Path C — Next.js + FastAPI (web app, PWA-capable)
Path D — Obsidian-native + static HTML reports (hybrid)

Each spike documents: stack, file tree, build commands, what we keep
from current code, migration steps, weekly cost, ceiling.

Run:
    python -m agents.helena.spike
"""
from __future__ import annotations

import argparse
from datetime import date

from . import VAULT_OUT, ROOT


PATHS = {
    "A": {
        "title": "Streamlit perfectionism",
        "ceiling": "Tasteful internal tool (8/10)",
        "weeks": "1",
        "stack": [
            "Streamlit 1.x (current)",
            "Plotly + ii_dark template",
            "scripts/_theme.py + scripts/_components.py (existing)",
            "Custom CSS injection (existing)",
        ],
        "what_keep": [
            "100% backend (SQLite, fetchers, scoring, agents) — zero changes",
            "All current pages (Portfolio, Ticker, Triggers, Screener, etc.)",
            "Helena Design System v1.0 (already in place)",
        ],
        "migration": [
            "Run `python -m agents.helena.audit` → fix every error in the report",
            "Refactor `dashboard_app.py` lines 247, 229, 232, 273 (audit findings)",
            "Replace 5× `template='plotly_white'` with `ii_dark` (DS005 hits)",
            "Replace 5× hex literals out of palette (DS006 hits) with COLORS[…]",
            "Tighten 2× section_caption with >8 words (DS008 hits)",
            "Add `hide_streamlit_branding` CSS (footer 'Made with Streamlit', menu hamburger)",
            "Add custom 404/error templates",
            "Test in 720p / 1080p / 1440p viewports — accept narrowest as canonical",
        ],
        "structure": """\
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
""",
        "build": "streamlit run scripts/dashboard_app.py  (no build step)",
        "weekly_cost": "Zero infra. Existing cron at 23:30 already updates data.",
        "limitations": [
            "Streamlit chrome leaks (sidebar widgets aesthetic, `st.button` look)",
            "No fluid mobile — sidebar collapses but feels desktop-first",
            "Cannot ship as `.exe` / `.app` / `.pwa`",
            "Slider/dropdown styling only customizable to a point",
        ],
        "verdict": "Cheapest viable. Hits a real ceiling at 8/10. Pick if budget < 1 sprint.",
    },

    "B": {
        "title": "Tauri desktop app  (RECOMMENDED)",
        "ceiling": "Native product feel (10/10)",
        "weeks": "3-4",
        "stack": [
            "Tauri 2.x (Rust shell + system WebView)",
            "Frontend: React 18 + Vite + TypeScript",
            "Design tokens: translate scripts/_theme.py → src/tokens.css",
            "Backend sidecar: FastAPI (Python) bundled via PyInstaller",
            "Charts: Plotly.js (mirror ii_dark template) OR ECharts / Recharts",
            "State: TanStack Query (React Query) + Zustand for local UI state",
        ],
        "what_keep": [
            "100% Python backend (SQLite, fetchers, scoring, agents) — exposed via FastAPI",
            "All scoring logic, perpetuums, library, paper signals — unchanged",
            "Helena Design System v1.0 — translated to CSS custom properties + Tailwind config",
            "Plotly templates → mirror in JS (`scripts/_theme.py` becomes `src/lib/plotly_theme.ts`)",
        ],
        "migration": [
            "Sprint 1 — scaffold:",
            "  • `cargo install tauri-cli`; `pnpm create tauri-app`",
            "  • Create `desktop/` directory at repo root",
            "  • FastAPI backend: `desktop/backend/main.py` exposing /api/positions, /api/verdict/{ticker}, …",
            "  • Translate `scripts/_theme.py` COLORS → `desktop/src/tokens.css` :root vars",
            "Sprint 2 — core pages (Portfolio + Ticker + Triggers):",
            "  • React routes + Helena components (`<KPITile/>`, `<StatusPill/>`, `<SectionHeader/>`)",
            "  • Plotly.js charts using ii_dark template ported to TS",
            "  • TanStack Query hooks against FastAPI endpoints",
            "Sprint 3 — remaining pages + polish:",
            "  • YouTube / Screener / Perpetuum Health / Actions Queue",
            "  • Tauri native menu, system tray, notifications (replace Telegram for in-front-of-PC)",
            "  • Sidecar packaging: PyInstaller bundle FastAPI as `helena-backend.exe`",
            "  • `tauri build` produces `helena.exe` installer (~30MB)",
            "Sprint 4 — hardening + ship:",
            "  • E2E tests (Playwright)",
            "  • Auto-update via Tauri updater (if we want)",
            "  • Sign + notarize (optional for personal use)",
        ],
        "structure": """\
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
""",
        "build": (
            "Dev:  cd desktop && pnpm tauri dev\n"
            "Prod: cd desktop && pnpm tauri build  → emits desktop/src-tauri/target/release/bundle/msi/*.msi"
        ),
        "weekly_cost": "Zero infra (local). Tauri auto-update server optional (~$0).",
        "limitations": [
            "Adds Rust + Node toolchain to dev environment",
            "PyInstaller sidecar bloats install (~120MB total) but acceptable",
            "Plotly.js theme port requires manual sync if ii_dark changes",
            "No mobile (Tauri Mobile is beta; desktop-first)",
        ],
        "verdict": (
            "Highest ceiling. Reuses 100% of Python backend. Sells like a real product. "
            "3-4 weeks honest. Pick if 'top quality' is the brief."
        ),
    },

    "C": {
        "title": "Next.js + FastAPI (web app, PWA)",
        "ceiling": "Real web product (9/10)",
        "weeks": "3-4",
        "stack": [
            "Next.js 14 (App Router) + TypeScript",
            "Tailwind CSS + Helena tokens",
            "FastAPI backend (Python)",
            "Charts: Recharts or Plotly.js",
            "Deploy: localhost:3000 + Caddy reverse proxy → optional Tailscale",
            "PWA: next-pwa for installable mobile experience",
        ],
        "what_keep": [
            "100% Python backend exposed via FastAPI (same as Path B)",
            "Helena Design System v1.0 → Tailwind config",
        ],
        "migration": [
            "Same as Path B but no Tauri shell — runs in browser",
            "PWA manifest enables 'Add to Home Screen' on mobile",
            "Self-host on Mac Mini / Windows always-on box, expose via Tailscale",
        ],
        "structure": """\
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
""",
        "build": (
            "Dev:  cd web && pnpm dev   (and `uvicorn backend.main:app --reload`)\n"
            "Prod: cd web && pnpm build && pnpm start  (or `vercel deploy`)"
        ),
        "weekly_cost": "Zero if self-hosted. Optional Vercel free tier.",
        "limitations": [
            "Browser chrome (URL bar, refresh, etc.) — not 100% native feel",
            "Network dependency unless PWA service worker caches aggressively",
            "Deploy story is more friction (Caddy / Tailscale) vs Tauri's installer",
        ],
        "verdict": (
            "Same backend reuse as B. Wins on mobile + accessibility from anywhere. "
            "Loses on 'feels like an app'. Pick if cross-device > native polish."
        ),
    },

    "D": {
        "title": "Obsidian-native + static HTML reports",
        "ceiling": "Polished knowledge worker setup (8/10 in different dimension)",
        "weeks": "1-2",
        "stack": [
            "Obsidian (existing) + community plugins (Charts, Dataview, Templater)",
            "Static HTML generator: Jinja2 + Helena CSS tokens (single-file output)",
            "scripts/obsidian_bridge.py (existing) — extend for richer outputs",
            "Streamlit kept ONLY for power-user interactive drill-down",
        ],
        "what_keep": [
            "Everything backend (zero change)",
            "Streamlit for interactive screener / triggers (not the 'platform face')",
            "Obsidian becomes the canonical reading surface",
        ],
        "migration": [
            "Sprint 1 — Obsidian polish:",
            "  • Install Kepano theme + Style Settings plugin",
            "  • Apply Helena tokens via Obsidian CSS snippet (`obsidian.css`)",
            "  • Wire Charts plugin to read from `data/*.db` via Dataview JS",
            "Sprint 2 — Static HTML pipeline:",
            "  • `scripts/render_report.py` — Jinja2 template, Helena tokens",
            "  • Outputs: `reports/weekly_YYYY-MM-DD.html` (single file, embedded CSS, "
            "    inline Plotly via plotly-CDN)",
            "  • Investor letter / quarterly review = HTML files (shareable, printable)",
        ],
        "structure": """\
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
""",
        "build": "python scripts/render_report.py --week 2026-W17  → reports/*.html",
        "weekly_cost": "Zero. No new infra.",
        "limitations": [
            "No 'single dashboard' — split between Obsidian (reading) + Streamlit (drill) + reports",
            "Live data requires either Obsidian Dataview JS or refresh script",
            "Won't sell as 'a platform' — it's a knowledge worker rig",
        ],
        "verdict": (
            "Cheapest path with high aesthetic ceiling. Different shape than B/C — "
            "doesn't try to be a product, leans into 'investor's desk' metaphor. "
            "Pick if you want polish in 1-2 weeks and accept the hybrid surface."
        ),
    },
}


def render_md() -> str:
    today = date.today().isoformat()
    out = [
        "---",
        "type: platform_spikes",
        f"updated: {today}",
        "owner: helena_linha",
        "tags: [platform, spikes, helena, mega, architecture]",
        "---",
        "",
        "# 03 — Platform spikes (4 paths)",
        "",
        f"> Helena Mega · run **{today}** · 4 caminhos avaliados.",
        "",
        "## Critério de decisão",
        "",
        "Para cada path: **stack**, **o que reusa do código actual**, **passos de "
        "migração concretos**, **estrutura de pastas final**, **comando de build**, "
        "**custo weekly**, **limitações honestas**, **veredicto**.",
        "",
        "## Sumário",
        "",
        "| Path | Título | Tecto | Semanas | Veredicto rápido |",
        "|---|---|---|---:|---|",
    ]
    for k, p in PATHS.items():
        out.append(
            f"| **{k}** | {p['title']} | {p['ceiling']} | {p['weeks']} | "
            f"{p['verdict'][:90]}… |"
        )
    out.append("")

    for k, p in PATHS.items():
        out += [
            f"## Path {k} — {p['title']}",
            "",
            f"**Tecto**: {p['ceiling']}  · **Custo**: {p['weeks']} semanas  · ",
            f"**Build**: `{p['build'].splitlines()[0]}`",
            "",
            "### Stack",
            "",
        ]
        for s in p["stack"]:
            out.append(f"- {s}")
        out += ["", "### O que se reusa do código actual", ""]
        for s in p["what_keep"]:
            out.append(f"- {s}")
        out += ["", "### Passos de migração", ""]
        for s in p["migration"]:
            if s.startswith("  "):
                out.append(f"  - {s.strip()}")
            elif s.endswith(":"):
                out.append(f"- **{s}**")
            else:
                out.append(f"- {s}")
        out += ["", "### Estrutura de pastas", "", "```", p["structure"].rstrip(), "```", ""]
        out += [f"### Build", "", "```bash", p["build"], "```", ""]
        out += [f"### Custo weekly", "", p["weekly_cost"], ""]
        out += [f"### Limitações", ""]
        for s in p["limitations"]:
            out.append(f"- {s}")
        out += ["", f"### Veredicto", "", p["verdict"], ""]

    out += [
        "## Recomendação Helena",
        "",
        "Founder pediu **'top quality, mega Helena'**. Pelo critério dele, Path B (Tauri) é o fit:",
        "",
        "1. Dá tecto 10/10 (sente-se a produto, não a script + CSS).",
        "2. Reusa 100% do backend Python (zero re-escrita de fetchers/scoring/agents).",
        "3. Helena Design System v1.0 traduz-se 1:1 para CSS tokens.",
        "4. Claude Design (Anthropic Labs) entra como prototyping per `Claude_Design_Integration.md` — output HTML cola com nosso React.",
        "5. 3-4 semanas honestas é razoável para um vibe-coder com auto mode.",
        "",
        "**Plano B se 4 semanas é demasiado**: combinar Path A (1 sprint Streamlit perfeccionismo, "
        "fix dos errors do audit) + Path D (Obsidian polish + reports HTML). Total 2-3 semanas para "
        "intermediate ceiling 8/10 sem stack nova.",
        "",
        "## Decisão pendente do founder",
        "",
        "- [ ] **Path B (Tauri) começa já?** — Helena Mega cria branch `phase-z-tauri`, Sprint 1 scaffold em ~3 dias.",
        "- [ ] **Path A+D fallback?** — 1 sprint cada, ship antes de duas semanas.",
        "- [ ] **Outra combinação**? Documentar aqui.",
        "",
        "## Cross-links",
        "",
        "- [[01_Audit]] — violações actuais (input para Path A)",
        "- [[02_Curation]] — skills relevantes para cada path",
        "- [[Claude_Design_Integration]] — prototyping flow comum a todos paths",
        "- [[Design_System]] — fonte dos tokens",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    import sys
    ap = argparse.ArgumentParser(description="Helena platform spikes")
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()

    md = render_md()

    if args.print:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        sys.stdout.write(md + "\n")
        return 0

    out_path = VAULT_OUT / "03_Spikes.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)} · 4 paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
