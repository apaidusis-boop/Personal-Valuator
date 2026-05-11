---
title: Mission Control Design Roadmap
phase: design-v3-broadsheet
created: 2026-05-05
status: in-progress
supersedes: Mission_Control_Design_v2.md
---

# Mission Control Design Roadmap — v3 "Broadsheet"

> Master document for the Mission Control redesign sprint and the
> research that informs it. Saved per user request 2026-05-05 before
> 8-hour break. Has three streams:
>
> 1. **Design log** — what shipped this session (v3 Broadsheet sprint)
> 2. **Design research** — frontend/palettes/hedge-fund visual references
> 3. **Watchlist research** — BR + US tickers, fresh angle per ticker
>
> All sources cited inline + consolidated at the end.

---

## TOC

1. [Voltamos](#voltamos)
2. [Sprint 1 — v3 Broadsheet ship log](#sprint-1--v3-broadsheet-ship-log)
3. [Open sprints — what's next](#open-sprints--whats-next)
4. [Design research](#design-research) (9 themes, ~80 sources)
5. [BR Watchlist research](#br-watchlist-research) (19 stocks + 16 FIIs)
6. [US Watchlist research](#us-watchlist-research) (6 candidates)
7. [Consolidated sources](#consolidated-sources)
8. [Closing — what to attack first when you're back](#closing--what-to-attack-first-when-youre-back)

**Doc stats**: ~830 lines, 41 ticker entries, ~110 unique source URLs.

---

## Voltamos

When you come back, the four open decisions are at [Open sprints](#open-sprints--whats-next).
The single highest-value next step is **Sprint 2 — page-by-page editorial pass** (Tasks, Council, Allocation, Ticker pages still inherit v2 spacing/cards).

Quick sanity check after landing:
```powershell
cd mission-control
npm run dev
# localhost:3000 — toggle dark/light bottom-left of sidebar
```

If colors look wrong or text not rendering serif, run `npm run build` to see if Tailwind v4 picked up the new tokens (it should — v4 is CSS-first).

---

## Sprint 1 — v3 Broadsheet ship log

**Date**: 2026-05-05
**Goal**: replace Linear/Vercel-style v2 (purple+cyan SaaS) with editorial broadsheet language inspired by **Financial Times** and **Wall Street Journal**.
**Build status**: ✓ `npm run build` clean, 20 routes, no TS regressions.

### Files changed (11 total)

| File | What changed |
|---|---|
| `app/globals.css` | Full token rewrite. Light theme = FT salmon (#FFF1E5). Dark theme = warm charcoal (#1B1916, deliberately not blue, not pure black). Serif (Source Serif 4 → Charter → Cambria → Georgia) for headlines, sans system stack for body, mono for numerics. Corners 0–2px (was 8px). New `.editorial`, `.rule-hard`, `.rule-soft`, `.serif`, `.drop-cap` utilities. Pills now thin uppercase (was chunky rounded). |
| `app/layout.tsx` | Wired `<ThemeInit />` into `<head>` so the data-theme is set BEFORE first paint (no FOUC). Added `suppressHydrationWarning` on `<html>`. |
| `components/theme-init.tsx` | NEW. Inline script reads `localStorage("mc-theme")`, defaults to dark, sets `data-theme` attr on root. |
| `components/theme-toggle.tsx` | NEW. Client-side button to flip theme + persist. Lives in sidebar footer. |
| `components/sidebar.tsx` | Editorial masthead "Mission / Control / est. 2026 · LocalClaw edition" replacing the gradient brand block. Icons removed (icons drift toward consumer SaaS). Width 224px → 192px. Active link uses left-rule (`border-l-2 border-[var(--accent-primary)]`) instead of bg color. |
| `components/ui/page-header.tsx` | Title now in `type-display` (serif). Subtitle is `type-byline` (italic). Hard rule (`.rule-hard`) under header — FT signature. |
| `components/ui/section.tsx` | Heading uppercase tracked + horizontal rule extending to action on the right (FT supplement style). |
| `components/ui/stat.tsx` | Removed `.card` wrapper. Now `border-t border-[var(--rule)] pt-3` — broadsheet stat block. Value in `type-display` mono tabular. |
| `components/chat-widget.tsx` | Trigger button changed from gradient orb to editorial pill: green dot · "antonio carlos" · ⌘K. Bubbles use `bg-overlay` + colored left-rule (was rgba purple/cyan glow). |
| `components/hedge-banner.tsx` | Replaced rgba red bg with `border-t-2` red rule + `bg-overlay`. Removed ⚑ flag char. |
| `components/action-button.tsx` | Tones now reference CSS tokens (was hardcoded purple-700/zinc-900 etc.). Editorial outline-only style. |

### Token palette reference

**Light (FT broadsheet)**
| Token | Value | Note |
|---|---|---|
| `--bg-canvas` | `#FFF1E5` | FT iconic salmon paper |
| `--bg-elevated` | `#FFFAF3` | Slightly lifted from canvas |
| `--bg-deep` | `#F2DEC2` | Sidebar/masthead |
| `--text-primary` | `#1A1815` | Warm black, not pure |
| `--accent-primary` | `#990F3D` | FT raspberry/claret |
| `--accent-glow` | `#1F3864` | WSJ deep navy (links) |
| `--gain` / `--verdict-buy` | `#006F3C` | FT green |
| `--loss` / `--verdict-avoid` | `#B22222` | Firebrick red (not vermillion) |

**Dark (FT/WSJ at night)**
| Token | Value | Note |
|---|---|---|
| `--bg-canvas` | `#1B1916` | Warm charcoal — not blue, not black |
| `--bg-elevated` | `#232018` | |
| `--bg-deep` | `#131210` | |
| `--text-primary` | `#F2EDE3` | Warm cream — NOT pure white |
| `--accent-primary` | `#E8957B` | Warm peach (analog of claret) |
| `--accent-glow` | `#95B0DD` | Soft navy at night |
| `--gain` | `#6FAE7E` | Muted forest |
| `--loss` | `#D97777` | Muted firebrick |

### Type scale
- `type-display` — 30px serif 600 (page titles)
- `type-h1` — 22px serif 600 (deck)
- `type-h2` — 16px serif 600 (sub)
- `type-h3` — 10px sans 700 uppercase 0.12em (eyebrow)
- `type-byline` — 12px sans italic
- `type-body` — 14px sans 1.55
- `type-mono` — 12px mono tabular

---

## Open sprints — what's next

> Decisions left for next session, in priority order. Each is sized
> for ~1–2 days of focused work.

### Sprint 2 — Page-by-page editorial pass *(highest leverage)*
The pages individuais (Tasks, Council, Allocation, Ticker, Memory, Content, Calendar, Team, Visual) still inherit v2 patterns: `card p-5`, `space-y-8`, `max-w-[1400px]`, occasional purple/cyan accent classes.

**What to do**:
- Replace `card p-5` containers with editorial alternatives:
  - Tables → flat with `rule-soft` row dividers, no card wrap
  - Cards-of-cards (e.g. Council grid) → keep card but flatten borders
- Bring `max-w-[1400px]` down to context — Tasks/Allocation can go full-width with denser table
- Replace remaining `pill-purple` / `pill-cyan` legacy with `pill-glow` (navy at light, soft-navy at dark)
- Strip `card-cyan` / `card-purple` gradient backgrounds — already done in tokens but components may still set inline styles
- Line-height + spacing tightening: `space-y-8` → `space-y-6` on density-heavy pages

**Verification**: open each page in light + dark, check no `rgba(139,92,246,...)` hardcoded values remain (`grep -r 'rgba(139,92'` in app+components).

### Sprint 3 — Top status bar (sticky global)
A single horizontal strip below the page header showing always-visible:
`NetWorth (BRL+USD aggregated) · Daily P&L · Macro Regime · Hedge ON/OFF · Time · API Health`.
Currently scattered (only on Home, hedge-banner is global).

**Rough plan**:
- New `components/status-bar.tsx` — server-rendered, reads from db.ts + vault.ts
- Refresh cadence: revalidate every 60s with `export const revalidate = 60` per page or use `next/router refresh()`
- Position: between `<HedgeBanner />` and `{children}` in `app/layout.tsx`
- Style: `border-y border-[var(--border-subtle)]`, mono numerics, dot-indicator for live

### Sprint 4 — Web font (Source Serif 4 via next/font)
Today the serif uses system stack (Charter on Mac, Cambria on Windows, Georgia fallback). Stack works but renders inconsistent across OSes.

Trade-off: `+30kb` self-hosted vs visual consistency. Recommend yes — for a "broadsheet" identity the headline weight matters, and `next/font` does subsetting.

```ts
// app/layout.tsx
import { Source_Serif_4 } from 'next/font/google';
const serif = Source_Serif_4({ subsets: ['latin'], variable: '--font-serif' });
// Apply: <html className={serif.variable}>
```

Plus update `:root --font-serif` to use `var(--font-serif)` first.

### Sprint 5 — Density audit (data-to-ink)
After Sprint 2, pass a measuring tape over each page:
- How many distinct numbers per viewport at 1440×900?
- WSJ benchmark: `~25-40 numbers visible per fold`
- Today (Home v3): ~12 numbers per fold
- Goal: 25+ on data-heavy pages, 8-12 on "narrative" pages (Briefing, Council dossier)

Tools: just measure. Bring `space-y-*` down where appropriate, increase row density in tables (`py-1` instead of `py-2`).

### Sprint 6 *(optional, later)* — Editorial illustrations
WSJ has the dotted-portrait byline. We could give each holding a procedural mark (e.g. ASCII sparkline of the price) inline in the masthead area of each ticker page. Low priority.

---

## Design research

> Web searches done 2026-05-05 during the 8-hour autonomous slot.
> All sources are listed inline; consolidated bibliography at the end.
> Themes: typography canon, hedge-fund visuals, anti-patterns,
> palettes, fonts, current trends.

### Theme 1 — The newspaper canon (FT, WSJ, Bloomberg)

**Financial Times**
- Typeface: **Financier** (Klim Type Foundry, Kris Sowersby, 2014). Two
  families: Financier Display (Perpetua-influenced) and Financier Text
  (Solus + Joanna influenced). Brief was "elegant, authoritative serif
  versatile for news + features, from broadsheet to mobile."
  Source: [Klim — Financier design notes](https://klim.co.nz/blog/financier-design-information/)
- Salmon paper background `#FFF1E5` is iconic and licenced to no one
  else — instantly recognisable.
- Design system: **Origami** (`@financial-times/o-typography`). Open
  source on GitHub. Provides type scale, vertical rhythm, font
  fallbacks, component primitives.
  Source: [GitHub Financial-Times/o-typography](https://github.com/Financial-Times/o-typography)
- FT's chart-type taxonomy (the "Visual Vocabulary"): authoritative
  rubric mapping data shape → chart choice. Worth borrowing for our
  ticker pages (price → line, allocation → bar, distributions →
  histogram, etc.)
  Source: [GitHub Financial-Times/chart-doctor](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md)

**Wall Street Journal**
- Typefaces (introduced for digital products in the 2016 redraw):
  - **Escrow** (Cyrus Highsmith, 2002, redrawn 2016) — Scotch serif for
    titles. "Escrow Banner Condensed" for big heads. Loud, authoritative.
  - **Exchange** (Tobias Frere-Jones, 2002) — Ionic slab for body.
    "Stability of Ionic slabs welded with Bell Gothic legibility."
  - **Retina** — for ultra-small numerics (originally designed by
    Frere-Jones for stock listings).
- Palette: "paper tones and inky hues" — drawn from the physical paper
  itself.
  Sources: [TypeNetwork — WSJ design chief on type & trustworthiness](https://typenetwork.com/articles/the-wall-street-journals-design-chief-talks-type-and-trustworthiness-after-launching-updated-app), [Matt Ström — WSJ Fonts: Escrow, Exchange & Retina](https://mattstromawn.com/writing/wsjfonts/), [WSJ Medium — design system collaboratively built](https://medium.com/the-wall-street-journal/how-we-collaboratively-built-a-new-design-system-daf4e95a2887)

**Bloomberg Terminal**
- Custom mono + proportional fonts by **Matthew Carter** (1980s onwards).
  Includes 1/64th fraction glyphs for finance.
- The interface is intentionally NOT redesigned much. *"Customer
  centricity ranks higher than aesthetic frivolity"* — religious
  consistency to satisfy users attached to the look.
- Modern: Chromium technology adopted to allow HTML5/CSS3 evolution
  WITHOUT breaking the visual contract.
  Sources: [Bloomberg LP — How Terminal UX designers conceal complexity](https://www.bloomberg.com/company/stories/how-bloomberg-terminal-ux-designers-conceal-complexity/), [@usgraphics on X — Bloomberg Terminal design philosophy](https://x.com/usgraphics/status/1617581416308695041), [UX Magazine — The Impossible Bloomberg Makeover](https://uxmag.com/articles/the-impossible-bloomberg-makeover)
- Bloomberg Green editorial — designed by Karlssonwilker — softens
  data with photography, climate focus.
  Source: [karlssonwilker — Bloomberg Green case study](https://karlssonwilker.com/case-study/bloomberg-green)

**Implication for Mission Control**
- Steal the typographic CANON from FT (serif headlines + sans body +
  mono numerics) — already done in v3 globals.css.
- Resist the urge to redesign every quarter — Bloomberg's stability
  is its identity. Once we settle v3, *don't* keep tweaking.
- Reference FT's Visual Vocabulary when adding new chart types.

### Theme 2 — Information density and the data-ink ratio

The fundamental design law for a hedge-fund cockpit is Tufte's, not
Material/Linear's. Five laws:

> 1. Above all else, show the data.
> 2. Maximize the data-ink ratio.
> 3. Erase non-data ink.
> 4. Erase redundant data-ink.
> 5. Revise and edit.

Source: [The Doublethink — Tufte's principles](https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/), [Holistics — Data-ink ratio explained](https://www.holistics.io/blog/data-ink-ratio/), [Plotly Medium — Maximizing data-ink ratio in dashboards](https://medium.com/plotly/maximizing-the-data-ink-ratio-in-dashboards-and-slide-deck-7887f7c1fab)

**The anti-pattern named by 2025 research**: "the data eyeball attack."
A B2B SaaS exec dashboard with **34 metrics** had executives spend 15
min/session just scanning. Working memory caps at **5–9 elements**.
Dashboards exceeding **12 KPIs** show **40% lower engagement**.

Source: [Pencil & Paper — Dashboard UX patterns](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards), [DesignRush — 9 dashboard design principles 2026](https://www.designrush.com/agency/ui-ux-design/dashboard/trends/dashboard-design-principles)

**Implication**:
- Home page should never exceed 9 distinct numbers above the fold.
  Today's v3 Home shows 4 stat blocks + 3 lists — already in budget.
- Tasks/Council/Allocation are *deep dives*, not overview — there
  density is OK. Per-page metric budget can be relaxed.
- Captain's Log style "story cards" (one finding per card) are the
  right approach for synthesis pages.

### Theme 3 — Linear/Vercel/SaaS commoditisation

The pattern v2 was built in (purple+cyan accents, soft borders, glass)
is by 2025 widely identified as the "every SaaS looks the same"
commoditisation. Critics name it "linear design" — direct, minimal,
but proven and indistinguishable.

> "The biggest change is that 2025 has significantly cut back on the
> amount of color, swapping the dull, monochrome blue with few bold
> colors for monochrome black/white with even fewer bold colors."

Source: [LogRocket — Linear design: the SaaS trend that's boring and bettering UI](https://blog.logrocket.com/ux-design/linear-design/), [Raw Studio — UX for SaaS in 2025](https://raw.studio/blog/ux-for-saas-in-2025-what-top-performing-dashboards-have-in-common/)

**Vercel/Linear approach**: dark backgrounds + monospace + terminal
aesthetics. Vercel uses CLI outputs as social proof and Core Web
Vitals as the hero visual. Brand-coherent but generic.

**Why "broadsheet" wins for us**: it's an underused visual language.
Almost no fintech is doing it. Stripe is mono-and-clean, Wealthsimple
is "calm confidence," Robinhood Legend is widgetized-modern. None of
those are broadsheet. We get differentiation for free.

### Theme 4 — Calm finance / editorial pastels (Wealthsimple precedent)

Wealthsimple is the example most often cited as "finance can feel
trustworthy without being cold." Soft pastels, editorial vibe, lots
of breathing space. The 2025 trend among personal finance apps is
"calm confidence" + clean layouts + adaptive themes.

Source: [Eleken — Fintech UI examples to build trust](https://www.eleken.co/blog-posts/trusted-fintech-ui-examples), [Goodface — Top 10 FinTech product interfaces](https://goodface.agency/insight/top-10-fintech-product-interface-designs/)

This validates the FT salmon light theme — it's *warmer* than typical
fintech navy-blue. Salmon at 100% saturation could feel too FT-derivative;
we use it scaled (`#FFF1E5` is FT's exact hex) and pair with restrained
editorial accents (claret, deep navy) — readable and warm without
caricature.

### Theme 5 — Dark mode in finance: warm charcoal beats blue-black

The 2025 dark-mode reference palette for premium finance:
- Background: `#1C1917` (warm charcoal)
- Accent: `#D4A574` (soft gold)
- Text: `#FAFAF9` (warm white)
- Subtle: `#A8A29E` (warm grey)

Source: [ColorHero — Dark mode palettes for modern websites](https://colorhero.io/blog/dark-mode-color-palettes-2025), [Phoenix Strategy Group — Best palettes for financial dashboards](https://www.phoenixstrategy.group/blog/best-color-palettes-for-financial-dashboards)

Our v3 dark theme is very close (`#1B1916` bg, `#F2EDE3` text, `#E8957B`
peach, `#95B0DD` soft navy). We diverge from the warm-gold-accent trend
because gold reads "luxury wealth management" — Bessemer/Goldman Private
Wealth — and we want editorial, not Private Wealth. Keep the peach +
soft navy.

### Theme 6 — Mono fonts for ticker data

The empirical 2025 leaderboard for finance/dashboard mono:

| Font | Strength | Why for finance |
|---|---|---|
| **Geist Mono** (Vercel) | Perfect x-height, clear punctuation | Open-source, designed for code+data |
| **Atkinson Hyperlegible Mono** | 1/l/I and 0/O deliberately shaped to differ | "Catastrophic if confused" use cases |
| **JetBrains Mono** *(current)* | Strong tabular figures, good ligatures | Already in our stack |
| Neue Montreal Mono | Modern, readable | Premium, not free |
| SUSE Mono | Sans-serif structure with strict mono | Production-ready 2024 release |

Source: [Pangram Pangram — Best monospace fonts 2025](https://pangrampangram.com/blogs/journal/best-monospace-fonts-2025), [Octet — 18 best monospace fonts](https://octet.design/journal/best-monospace-fonts/)

**Recommendation**: keep JetBrains Mono. It's industry-standard, free,
ligature-friendly. **But** consider switching to **Atkinson Hyperlegible
Mono** if a single 0/O confusion ever causes a real bug — it's
explicitly designed for that.

### Theme 7 — Serif typefaces that work on screen

The shortlist of serifs that hold up at 14px on dense data tables:

| Font | License | Note |
|---|---|---|
| **Source Serif 4** *(our v3 first choice)* | Open (SIL OFL) | Adobe + Google Fonts. 12 styles, **optical sizes**. |
| **Charter** | Free for non-commercial; bundled with macOS | Matthew Carter humanist. "Highly legible at low resolution" — designed for that. |
| **Tiempos Text** (Klim) | Commercial (~$249) | "Modern Plantin/Times update for editorial" |
| **Newsreader** | Open (Google Fonts) | Designed for variable optical sizes, news context |
| **Merriweather** | Open (Google Fonts) | Tall x-height, dense text-friendly |

Source: [Klim — Tiempos Text](https://klim.co.nz/fonts/tiempos-text/), [Adobe Fonts — Source Serif 4](https://fonts.adobe.com/fonts/source-serif-4), [John Jago — Source Serif and Charter: a tale of two typefaces](https://johnjago.com/fournier/), [Figma — 31 best serif fonts](https://www.figma.com/resource-library/best-serif-fonts/)

**Decision frame for Sprint 4**:
- If we want pixel-perfect cross-platform: **Source Serif 4 via next/font** (~30kb subset, free).
- If we want truly broadsheet-authentic: **Tiempos Text** but it's
  paid (~$249 for web). Defensible spend if "broadsheet" is the brand.
- For now (system stack), Charter on Mac and Cambria on Windows do a
  remarkable job — both designed for screen reading at low res.

### Theme 8 — Hedge-fund / wealth platforms as benchmarks

**Addepar** (family-office tier): emphasis on *aggregation across
institutions*. Single screen, real-time, customizable reporting. Light
mode by default. Visualization-heavy.
Source: [Addepar — Family Office Software](https://addepar.com/family-office-software)

**BlackRock Aladdin**: front+middle+back-office, eFront for private.
Whole-portfolio, includes risk analytics. Institutional, dark default.

**Robinhood Legend** (browser desktop): widgetized, modular, modern
"trader vibe." Validates the move to multi-window/customizable layout
even for retail.
Source: [Robinhood — New visual identity](https://newsroom.aboutrobinhood.com/a-new-visual-identity/)

**Wealthfront Dashboard redesign 2024**: net-worth projection as the
hero — orienting the user *toward the long term*. Validates our
DRIP/long-term framing.
Source: [Wealthfront — Introducing the new Dashboard](https://www.wealthfront.com/blog/introducing-new-dashboard/)

**What we steal**:
- **Aggregation** (Addepar) — already done; portfolio crosses BR+US.
- **Long-term hero** (Wealthfront) — Home should show net-worth chart
  big, with DRIP projection year-marker overlay. *Not yet done.*
- **Widgetized layout** (Robinhood Legend) — pages are static today;
  Sprint 5+ could allow per-user pinning.

**What we reject**:
- Aladdin's institutional rigour comes with institutional ugliness.
  We're a personal hedge fund — keep the editorial warmth.
- "Calm finance" pastels — too soft for our ambitions; broadsheet is
  more authoritative.

### Theme 9 — Layout patterns to consider for Sprint 2

| Pattern | Where it fits |
|---|---|
| **Three-column broadsheet** | Home page — left rail (status), centre column (briefing/council), right rail (open actions). FT.com uses this on its home. |
| **Sticky byline + drop cap** | Council dossier pages — open with a serif drop cap, then reading flow. |
| **Inline ticker pill on hover** | Anywhere a ticker is mentioned — small price + colour pill on hover. WSJ Markets does this. |
| **"Market data" tables with ruled rows, no zebra** | Allocation, Tasks list, Holdings — replace card-of-rows with FT-style ruled tables. |
| **Editorial breakouts** | Council / Strategy pages — pull-quote panels for key findings (like NYT longreads). |
| **Sparkline beside every ticker** | Tasks and Watchlist — 60-day sparkline inline with the ticker symbol, ~80×20px, mono colour. |

---

## BR Watchlist research

> 19 BR stocks + 16 BR FIIs from `config/universe.yaml > br > watchlist`,
> researched 2026-05-05 with one fresh-news web search per ticker.
> Each block: thesis snapshot + Q1 2026 (or latest) read + analyst
> target where available + what to watch. Sources cited inline.

### BR stocks — Tier 1 (XP + BTG consensus, 3+ houses)

#### PETR4 — Petrobras *(Oil & Gas)*
- **Q1 2026 read**: BTG estimates EBITDA ~US$13bn, dividends ~US$2.1bn (1.5% quarterly DY). Annual DY projected ~9% for 2026. Current cash dividend R$3.20/share, 6.52% trailing.
- **Tension**: CEO Magda Chambriard publicly guiding **Brent → US$70 by year-end 2026**. BTG's bull case uses **US$82**. The US$12/bbl gap is the entire EBITDA story.
- **What to watch**: extraordinary dividends if cash builds; capex discipline; political pressure on fuel pricing pre-2026 election lookback.
- **BTG ADR target**: **US$25** (raised this year).
- Sources: [Seu Dinheiro — BTG sees PETR4 strong quarter + ADR target US$25](https://www.seudinheiro.com/2026/empresas/petrobras-petr4-deve-entregar-trimestre-forte-e-dividendos-robustos-diz-btg-preco-alvo-do-adr-sobe-para-us-25-lvgb/), [Rio Times — Petrobras CEO sees Brent US$70 by year-end](https://www.riotimesonline.com/petrobras-oil-forecast-70-dollar-magda-chambriard-april/), [Simply Wall St — PETR4 dividend history](https://simplywall.st/stocks/br/energy/bovespa-petr4/petroleo-brasileiro-petrobras-shares/dividend)

#### AXIA7 — Axia Energia *(Utilities — ex-Eletrobras)*
- **Identity**: Axia is rebranded Eletrobras, privatised June 2022. AXIA7 is a **temporary class C preferred share** (606.8M new shares distributed free to shareholders, liquidated Dec 26 2025).
- **2026 transition**: April 1 EGM approved migration to **B3 Novo Mercado**, converting AXIA5/AXIA6 PNs into ON. AXIA7 (class C) **remains outside** the conversion, fate TBD.
- **What to watch**: timeline of AXIA7 unwind (one-time event when liquidity merges into ON shares); valuation re-rating post-Novo Mercado; capex discipline now no longer state-controlled.
- Sources: [Wikipedia — Axia Energia](https://pt.wikipedia.org/wiki/Axia_Energia), [Suno — Axia Novo Mercado approval](https://www.suno.com.br/noticias/acionistas-axia-energia-axia3-eletrobras-migracao-novo-mercado-go/), [Seu Dinheiro — AXIA6 Novo Mercado proposta](https://www.seudinheiro.com/2026/empresas/acionistas-querem-a-axia-energia-axia6-no-novo-mercado-acoes-sobem-apos-proposta-da-eletrica-veja-se-e-hora-de-comprar-miql/)

#### CPLE3 — Copel *(Utilities — privatised 2023)*
- **2026 dividend**: R$1.35bn approved, **R$0.4546/share gross**, payment 30 Jun 2026.
- **Q4 2025 read**: net income R$683M recurring, **+29.6% YoY**. Stock +23% YTD 2026, +58% LTM.
- **Drivers**: Safra calls it "dividends + growth" — rare combo in BR utilities.
- **What to watch**: continued capex efficiency post-privatisation; Paraná state government residual exposure; whether Selic-cuts cycle compresses the multiple.
- Sources: [Investidor10 — CPLE3 R$ bilhões dividendos 2026](https://investidor10.com.br/noticias/copel-cple3-pagara-dividendos-bilionarios-em-2026-veja-valor-por-acao-119968/), [Seu Dinheiro — Safra: dividendos e crescimento](https://www.seudinheiro.com/2026/empresas/dividendos-e-crescimento-a-eletrica-que-entrega-o-pacote-completo-segundo-safra-lvgb/), [Arevista — CPLE3 dispara 80%](https://arevista.com.br/investimentos/cple3-dispara-mais-de-80-ate-onde-vao-os-dividendos-da-copel/)

### BR stocks — Tier 2 (XP + BTG consensus, 2 houses)

#### ALOS3 — Allos *(Real Estate — Shopping)*
- **2026 guidance**: EBITDA R$2.17–2.24bn; dividends R$0.28–0.30/share; capex R$350–450M (cycle of lower investments).
- **Operacional**: occupancy 96.5% (+0.1pp YoY), SSR +5.7% Q4 25 (renewals beating inflation). 45 malls, 1.94M sqm GLA total / 1.27M sqm owned.
- **What to watch**: tier-3/4 city malls organic SSR; balance sheet capacity for opportunistic acquisitions; cycle-low capex creates dividend cushion.
- Sources: [PRNewswire — ALLOS 2Q25 SSR +7.7%](https://www.prnewswire.com/news-releases/allos-2q25-results-sss-7-1-ssr-7-7-and-ffops9-302529529.html), [Investcred — ALOS3 will triple monthly dividends](https://investcred.com.br/ultimas-noticias/allos-alos3-triplicara-dividendos-mensais-ate-2026-e-acoes-sobem-forte-apos-3o-tri/)

#### B3SA3 — B3 *(Financials — Exchange)*
- **Market cap**: R$87.8bn. Price ~R$17.63. **12M consensus target R$17.04** (low R$15, high R$22). Consensus rating **Buy** (6 buy / 8 hold / 0 sell, 14 analysts).
- **2026 narrative**: management projects double-digit growth, focus on **non-cyclical revenue** (digital options + data analytics).
- **What to watch**: ADTV recovery cycle; international cross-listings; BTG/XP target R$16.90 implies modest upside — basically a fair-value HOLD in current price.
- Sources: [Investing.com — B3SA3 forecast & analyst targets](https://www.investing.com/equities/bmfbovespa-on-nm-consensus-estimates), [Stock Analysis — B3SA3 market cap](https://stockanalysis.com/quote/bvmf/B3SA3/market-cap/)

#### ENGI11 — Energisa *(Utilities — Distribution)*
- **2026 capex**: R$7.09bn total, of which R$6.55bn for the 9 distributors. Largest investment plan in company history.
- **Tariff index switch**: from **IGP-M to IPCA** for Parcela B from 2026 cycle, materially better fit to consumer inflation.
- **ES Gás** subsidiary: ARSP-approved tariff cut −2.47% from Feb 1 (margin compression there).
- **What to watch**: how IPCA index transition affects realised tariffs vs IGP-M base; capex execution pace.
- Sources: [Análise de Ações — Energisa R$7.1bn capex 2026](https://www.analisedeacoes.com/noticias/energisa-engi11-projeta-investimentos-de-7-1-bilhoes-em-2026/), [AgoraMS — IPCA replacing IGP-M](https://www.agorams.com.br/com-ipca-no-lugar-do-igp-m-reajuste-da-tarifa-da-energisa-ms-muda-em-2026/), [Visno Invest — ES Gás tariff cut](https://visnoinvest.com.br/news/11507/energisa-engi3-engi4-engi11-arsp-homologa-reajuste-da-es-gas-com-reducao-media-de-247-a-partir-de-1o-de-fevereiro-de-2026)

#### ITUB4 — Itaú Unibanco *(Banks)*
- **Q4 2025**: net income R$12.3bn (managerial), **ROE 24.4%**, FY2025 R$46.8bn (+13.1% YoY).
- **2026 guidance**: implied 7–9% earnings growth (ciclo maduro de rentabilidade). Safra estimates **R$51.0bn** FY2026.
- **Dividends/JCP**: trailing 12M R$5.08/share = **8.10% DY**. Latest JCP R$3.85bn announced (R$0.349/share, paid by Aug 31).
- **What to watch**: NIM behaviour as Selic cycle plays out; credit normalisation; whether ROE sustains >24% (top of cycle).
- Sources: [Seu Dinheiro — ITUB4 R$3.85bn JCP](https://www.seudinheiro.com/2026/empresas/alem-dos-dividendos-itau-unibanco-itub4-anuncia-r-385-bilhoes-em-jcp-veja-valor-por-acao-e-quem-tem-direito-lvgb/), [O Especialista (Safra) — Itaú 4T25 análise](https://oespecialista.safra.com.br/itau-itub4-analise-4t25/), [Investidor10 — ITUB4 financial overview](https://investidor10.com.br/acoes/itub4/)

#### EQTL3 — Equatorial *(Utilities — Distribution + Sanitation)*
- **Strategic pivot**: prioritising **distribution + sewage**, exiting transmission. Sold transmission division to **CDPQ for R$9.4bn** — proceeds for deleveraging + Sabesp investment + dividend potential.
- **Sabesp stake**: 15% reference shareholder post-privatisation. Targets accelerated capex + management overhaul.
- **What to watch**: pace of Sabesp synergies; transmission auction abstention discipline; deleveraging progress.
- Sources: [Investing & Notícias — EQTL3 sells transmission to CDPQ](https://www.investimentosenoticias.com.br/noticias/mercado/equatorial-eqtl3-vende-divisao-de-transmissao-para-cdpq-por-r94-bilhoes-e-foca-em-novas-estrategias-apos-aquisicao-da-sabesp-sbsp3/), [Money Times — EQTL3 leva 15% Sabesp](https://www.moneytimes.com.br/sabesp-sbsp3-equatorial-eqtl3-leva-15-e-sera-o-investidor-referencia/), [Empiricus — Equatorial Day expansão Sabesp](https://www.empiricus.com.br/artigos/investimentos/equatorial-day-eqtl3-expansao-de-negocios-com-a-sabesp-sbsp3-caminha-e-geracao-de-valor-continua-diz-analista/)

#### MOTV3 — Motiva *(Industrials — ex-CCR, Highways)*
- **Q1 2026 (just released)**: **adjusted net income R$627M, +16.3% YoY**. Adjusted EBITDA R$2.24bn (+9.3%). Net revenue R$3.33bn (+5.7%). Highways segment EBITDA R$1.93bn **(+14.7%)**.
- **Identity note**: Q1 2026 marks 1-year anniversary of MOTV3 ticker (ex-CCR rebranding).
- **Drivers**: portfolio optimisation (new SP/PR highways + BR-163 contract renegotiation); traffic recovery in March 2026.
- **What to watch**: BB Investimentos rates **Buy** (mixed result framing); Banco do Brasil call out asset rotation as the recurring positive.
- Sources: [DiárioDoTransporte — Motiva 1T26 +16.3%](https://diariodotransporte.com.br/2026/05/03/motiva-tem-alta-de-163-no-lucro-liquido-ajustado-do-1t26-para-r-627-milhoes/), [Suno — BB resultado misto compra](https://www.suno.com.br/noticias/motiva-motv3-resultado-1t26-bb-investimentos-compra-go/), [InfoMoney — Motiva 1T26 R$627M](https://www.infomoney.com.br/mercados/motiva-motv3-resultados-primeiro-trimestre-2026/)

#### MULT3 — Multiplan *(Real Estate — Shopping)*
- **Q1 2026**: net income R$316.1M, **+35.1% YoY**, record for the period. SSR real growth **+3.0%** + RE sales bump.
- **2026 expansion**: ~13,000 sqm GLA additions across BH Shopping (Q2), BarraShopping (Q3), ParkShopping SP (Q4).
- **Analyst consensus**: 12M target **R$34.19** (11 analysts buy).
- **What to watch**: potential dividend bump (mgmt has indicated openness); cycle-low capex post-2026 deliveries.
- Sources: [BPMoney — MULT3 1T26 +35.1%](https://bpmoney.com.br/mercado/multiplan-mult3-lucra-r-3161-milhoes-no-1t26-alta-de-351-e-recorde-para-o-periodo/), [Money Times — MULT3 expansion plans + dividends](https://www.moneytimes.com.br/multiplan-mult3-preve-expansao-de-shoppings-em-2026-e-nao-descarta-elevar-dividendos-veja-planos-igdl/), [MarketScreener — MULT3 analyst consensus](https://www.marketscreener.com/quote/stock/MULTIPLAN-EMPREENDIMENTOS-6499840/consensus/)

#### PGMN3 — Pague Menos *(Consumer Staples — Pharmacy)*
- **Trailing 12M**: revenue R$14.91bn, net income R$260.9M.
- **Stock**: R$5.56, +76% LTM.
- **BTG resumed coverage with BUY**, target **R$9** (~50%+ upside). Trades below historical multiples.
- **GLP-1 driver**: ~9% of revenue today; could explain ~3pp of revenue growth in 2026.
- **What to watch**: margin recovery flowing to operating leverage; M&A optionality (CFO has hinted).
- Sources: [Seu Dinheiro — BTG buy on PGMN3 R$9](https://www.seudinheiro.com/2026/empresas/a-virada-da-pague-menos-pgmn3-o-que-esta-por-tras-da-recomendacao-de-compra-do-btg-pactual-lvgb/), [Investidor10 — PGMN3 financials](https://investidor10.com.br/acoes/pgmn3/), [Seu Dinheiro — PGMN3 50% lucro 3T25](https://www.seudinheiro.com/2025/bolsa-dolar/depois-de-salto-de-50-no-lucro-liquido-no-terceiro-trimestre-cfo-da-pague-menos-pgmn3-fala-como-a-rede-pode-mais-bdap/)

#### PLPL3 — Plano & Plano *(Consumer Disc. — Construction)*
- **2026 projections**: R$5.3bn launches (+18% vs 2025), net profit R$578M, **ROE 45%** — among highest in popular construction segment.
- **Q4 2025**: revenue R$1.08bn (+60% YoY), EBITDA R$191M (+51%), net profit R$144M (+39%).
- **MCMV positioning**: tier 1 + 2 in São Paulo. CFO has said preparing **3 years for tier 4** (R$500K cap), now active since May 2025.
- **What to watch**: BTG bull thesis sees +34% upside; tier 4 capture rate; stem of any government-policy reversal risk.
- Sources: [Money Times — PLPL3 MCMV faixa 1 velocidade](https://www.moneytimes.com.br/plano-plano-avanca-na-faixa-1-do-mcmv-onde-velocidade-de-vendas-surpreende-6/), [Seu Dinheiro — PLPL3 tier 4 estratégia + BTG +34%](https://www.seudinheiro.com/2026/empresas/construtora-queridinha-do-minha-casa-minha-vida-se-prepara-para-acelerar-em-2026-e-acao-deve-saltar-mais-de-34-segundo-o-btg-pactual-bdap/), [Nord Investimentos — PLPL3 4T25 recordes](https://www.nordinvestimentos.com.br/blog/plano-plano-resultados-4t25/)

#### POMO3 + POMO4 — Marcopolo *(Industrials — Bus bodies)*
- **Q1 2026**: net income R$265M (~+10% above expected), EBITDA R$304.8M (+16% operacional).
- **Export-led**: 2025 international sales **45.4% of revenue** (vs 36.3% in 2024). BR exports +31% to R$1.1bn.
- **2026 strategy**: Argentina + LatAm export push to offset BR domestic deceleration.
- **Margins**: adjusted EBITDA margin 19.0% Q4 25; FY 2025 EBITDA R$1.51bn / margin 16.6%.
- **What to watch**: domestic order book; FX tailwind erosion if BRL appreciates; biofuel/electric-bus product ramp.
- Sources: [InfoMoney — Marcopolo 1T26 R$265M](https://www.infomoney.com.br/mercados/marcopolo-pomo4-resultados-primeiro-trimestre-2026/), [XP — POMO4 4T25 rentabilidade sólida 2026](https://conteudos.xpi.com.br/acoes/relatorios/marcopolo-pomo4-rentabilidade-solida-com-indicacoes-positivas-para-2026e-resultados-do-4t25/), [CNPL — Marcopolo LatAm growth](https://www.cnpl.org.br/marcopolo-busca-crescimento-na-america-latina-para-enfrentar-desaceleracao-no-brasil/)

#### RAPT4 — Randoncorp *(Industrials — Trailers + heavy vehicles)*
- **Trigger event Jan 2026**: R$770M contract for railcars (Arauco + Rumo), shares +5.1% to +7.94% intraday.
- **Q3 2025**: profit −81% to R$23.1M — recovery story, not value-trap, but base is brutal.
- **Safra target**: **R$7.80** (+38% upside). Buy rating.
- **What to watch**: agri-cycle recovery (key end-market); high-rate environment relief; international expansion ("CEO wants ever-more international").
- Sources: [Seu Dinheiro — Randon Arauco/Rumo contract](https://www.seudinheiro.com/2026/empresas/randon-rapt4-salta-ate-8-apos-fechar-contrato-com-arauco-e-rumo-rail3-lvgb/), [InfoMoney — Randoncorp Q3 2025 −81%](https://www.infomoney.com.br/mercados/randoncorp-rapt4-resultados-terceiro-trimestre-2025/), [Acionista — RAPT4 megacontrato BUY](https://acionista.com.br/rapt4-disparou-apos-megacontrato-e-hora-de-comprar/)

#### RDOR3 — Rede D'Or *(Healthcare)*
- **Q4 2025**: net income R$1.2bn (+39.2% YoY), revenue >R$12bn (+double-digit), adjusted EBITDA margin >25%. **Stock fell despite beat** — expectations were too high.
- **Operational**: 79 hospitals (76 owned + 3 managed), 13,555 beds (+3.8%), occupancy 76.9%.
- **SulAmérica synergy**: 2022 acquisition flowing — captive insurance customers prioritising in-network = occupancy boost. ROIC steadily improving.
- **What to watch**: SulAmérica MLR (medical loss ratio) trends; pace of new hospital openings; whether dividends-extraordinary-pattern continues (R$8.12bn of proventos in 2025).
- Sources: [EBC — RDOR3 4T25 R$1.2bn lucro queda da ação](https://www.ebc.com/pt/forex/rdor3-resultados-4t25-lucro-sulamerica-queda-acoes), [Empiricus — SulAmérica beneficiários sólidos](https://www.empiricus.com.br/artigos/investimentos/rede-dor-sulamerica-apresenta-crescimento-solido-de-beneficiarios-e-reforca-tese-de-investimento-nas-acoes-rdor3-saiba-mais-capf/), [Genial — RDOR3 SULA11 incorporação](https://analisa.genialinvestimentos.com.br/acoes/rede-dor/rede-dor-incorpora-sulamerica-se-nao-comprar-a-solucao-e-ser-comprado-rdor3-sula11/)

#### RENT3 — Localiza *(Industrials — Car rental)*
- **Q4 2025**: net income R$939M (+12.1% YoY); 2026E net income ~R$1.0bn Q1 (+21% YoY); FY2026E ~R$4.2bn / FY2027E ~R$5.3bn.
- **Seminovos**: revenue +15% QoQ, volumes 78k units (record). EBITDA margin 2.5% (+80bps QoQ).
- **Headwind**: **Chinese-brand cars eroding residual values** of internal-combustion fleet. BTG sees +25% upside despite this.
- **Targets**: avg consensus R$59.25 (low R$50, high R$70).
- **What to watch**: depreciation policy adjustments; corporate fleet (Localiza is the de-facto BR fleet manager); rate-cycle tailwind on rental rates.
- Sources: [InfoMoney — RENT3 reporta resultados positivos](https://www.infomoney.com.br/mercados/localiza-rent3-reporta-resultados-positivos-e-analistas-reforcam-confianca-na-acao/), [Seu Dinheiro — RENT3 carros chineses BTG +25%](https://www.seudinheiro.com/2026/empresas/localiza-rent3-sofre-com-invasao-de-carros-chineses-mas-ha-esperancas-acao-pode-subir-ate-25-segundo-o-btg-kaes/), [XP — Localiza 1T26 prévia](https://conteudos.xpi.com.br/acoes/relatorios/localiza-rent3-previa-do-1t26-atualizacao-de-estimativas/)

#### SUZB3 — Suzano *(Materials — Pulp)*
- **Q1 2026**: weak. Stock under R$50 even as Ibov hits records.
- **Targets diverging widely**: Citi **R$72** (was R$70, BUY +23%). XP **R$66**. BofA **cut R$25 from target** = chunky downgrade. Avg consensus **R$68.68** (low R$55, high R$81).
- **Pulp pricing**: BHKP avg US$562/ton Q1 26. 2026 increases announced: +US$50/ton Asia, +US$200/ton elsewhere. Forward forecasts US$591 (Citi) / US$560 (XP). Diverging, like the targets.
- **What to watch**: realised vs announced price increases; China demand recovery; FX (BRL strength compresses USD-receivables).
- Sources: [Money Times — Citi raises SUZB3 target +23%](https://www.moneytimes.com.br/suzano-suzb3-citi-eleva-mais-uma-vez-preco-alvo-para-acao-por-operacional-mais-forte-e-melhora-para-celulose-pads/), [Suno — SUZB3 1T26 decepção](https://www.suno.com.br/noticias/suzano-suzb3-resultado-1t26-ebitda-celulose-mt/), [Seu Dinheiro — BofA cuts R$25 from SUZB3](https://www.seudinheiro.com/2026/empresas/suzano-suzb3-bofa-corta-r-25-do-preco-alvo-e-acoes-despencam-lvgb/), [InfoMoney — Suzano May price hikes](https://www.infomoney.com.br/mercados/suzano-elevara-celulose-na-europa-e-americas-em-maio-anuncio-e-agridoce-diz-bbi/)

#### TTEN3 — 3Tentos *(Consumer Staples — Agribusiness)*
- **2026E**: grain sourcing volumes **+13%**, processed volumes **+49%** (corn ethanol plant + soybean expansion). EPS growth 16% 2025→2027E.
- **Q3 2025**: EBITDA R$166M **−51%**, net income R$203M **−36%** YoY — crushing margin compression.
- **XP price target R$23.60** (BUY, +49.84% upside). XP framing: 9.2x 2026 P/E doesn't reflect quality.
- **Drivers**: B15 biodiesel mandate; canola processing higher-margin; fertilizer cycle.
- **What to watch**: crushing margin recovery (the entire bull thesis hinges on it); execution of corn ethanol plant ramp.
- Sources: [Investidor10 — XP elege TTEN3 favorita 50%](https://investidor10.com.br/noticias/xp-elege-3tentos-tten3-como-favorita-no-agro-com-potencial-alta-de-50-118011/), [Nord — TTEN3 projeções 2026](https://www.nordinvestimentos.com.br/blog/3tentos-tten3-projecoes-2026-meta-receita-2032/), [XP — 3T25 resultados positive but hard to interpret](https://conteudos.xpi.com.br/acoes/relatorios/3tentos-tten3-revisao-dos-resultados-do-3t25-positivo-porem-dificil-de-interpretar/)

### BR FIIs (Suno carteira recomendada)

#### Shopping

| Ticker | Quote (~May 26) | DY 12M | P/VP | Latest dividend | Notes |
|---|---|---|---|---|---|
| **PMLL11** *(Plural Malls)* | R$110.23 | 10.86% | 0.94 | R$1.00 (5/26) | 2026 perf strong; NAV R$121.22; mgmt Pátria-VBI. Suno target R$120 |
| **VISC11** *(Vinci Shopping)* | R$110.21 | 8.92% | n/a | R$0.81/mo Jun-Sep 25 | YTD +26.81%. Mandate: ≥95% earnings distributed. Suno target R$119 |

Sources: [Status Invest — PMLL11](https://statusinvest.com.br/fundos-imobiliarios/pmll11), [Investidor10 — PMLL11](https://investidor10.com.br/fiis/pmll11/), [Genial — VISC11](https://www.genialinvestimentos.com.br/onde-investir/renda-variavel/fiis/visc11/), [Investidor10 — VISC11](https://investidor10.com.br/fiis/visc11/)

#### Híbrido / Tijolo

| Ticker | Quote | DY 12M | P/VP | Latest div | Notes |
|---|---|---|---|---|---|
| **TRXF11** *(TRX Real Estate)* | ~R$93 | 13.03% | 0.91 | R$0.93 (4/26) | Hybrid: corporate + retail leased to large companies. Active mgmt. Suno target R$120 |
| **GARE11** *(Guardian Real Estate)* | ~R$8.5 | 11.99% | 0.88 | R$0.083/mo | 2026 guidance R$0.083–0.090. Logistics + essential retail. Suno target R$10.90 |
| **HGRU11** *(CSHG Renda Urbana → Pátria)* | R$129.05 | 9.39% | n/a | R$0.95 (4/15/26) | Urban income (commercial + residential leases). YTD +26.80%. Suno target R$140 |
| **MCRE11** *(Mauá Capital Real Estate)* | R$9.60 | trailing | n/a | R$0.11/mo | High-yield "tijolo" but **paper-fund-like** (multi-strategy CRI exposure). Suno target R$9.90 |
| **KNRI11** *(Kinea Renda Imobiliária)* | ~R$148 | 7.40% | **1.03** | R$1.10 (4/15/26) | Hybrid corporate + logistics + CRIs. Trades at NAV. Suno target R$164 (Aguardar) |

Sources: [Status Invest — TRXF11](https://statusinvest.com.br/fundos-imobiliarios/trxf11), [Investidor10 — GARE11](https://investidor10.com.br/fiis/gare11/), [InfoMoney — GARE11 2026 dividend guidance](https://www.infomoney.com.br/onde-investir/fii-gare11-mantera-patamar-de-dividendos-para-2026-gestor-responde-duvidas/), [Investidor10 — HGRU11](https://investidor10.com.br/fiis/hgru11/), [Status Invest — MCRE11](https://statusinvest.com.br/fundos-imobiliarios/mcre11), [Investidor10 — KNRI11](https://investidor10.com.br/fiis/knri11/)

#### Logística

| Ticker | Quote | DY 12M | P/VP | Latest div | Notes |
|---|---|---|---|---|---|
| **HGLG11** *(CSHG Logística → Pátria Log)* | R$156.40 | n/a | n/a | R$1.10/share | 2026 guidance R$1.10 H1 → potentially R$1.17 H2. >20 warehouses. Suno target R$162 |
| **BRCO11** *(Bresco Logística)* | R$118.10 | 8.34% | n/a | R$0.95 (raised from R$0.92) | YTD +27.37%. Vacancy 0.8% (was 11.3%). 14 warehouses, 591k sqm. Suno target R$129 |
| **XPLG11** *(XP Log)* | n/a | 9.80% | n/a | R$0.82/mo | Vacancy 8.7% (rising — 12.6k sqm returned in 2 assets). Cap rate ~9.7%. Suno target R$119 |

Sources: [Suno — HGLG11 2026 R$1.10–1.17 guidance](https://www.suno.com.br/noticias/hglg11-rendimentos-2026-projecoes/), [Suno — BRCO11 dividends raised](https://www.suno.com.br/noticias/brco11-dividendos-095-maio-2026/), [FundsExplorer — XPLG11 vacancy 8.7%](https://www.fundsexplorer.com.br/noticias/xplg11-dividendo-abril-2026), [Investidor10 — XPLG11](https://investidor10.com.br/fiis/xplg11/)

#### Papel / CRI

| Ticker | Quote | DY 12M | P/VP | Latest div | Notes |
|---|---|---|---|---|---|
| **RECR11** *(REC Recebíveis Imobiliários)* | R$83.71 | 13.10% | 0.94 | R$1.03 (4/15/26) | 92% in CRIs (R$2.25bn). YTD +3.55%. Adm fee 0.20%. Suno target R$95 |
| **KNCR11** *(Kinea Rendimentos)* | n/a | **13.73%** | **1.04** | R$1.15 (4/14/26) | CDI-linked; 77.7% CRIs at CDI+2.04%, 4y avg duration. Suno target R$106 |
| **VGIP11** *(Valora CRI Plus, IPCA-linked)* | R$80.56 | 13.74% | 0.88 | R$0.73 (Mar 26) | IPCA+5.6% net yield current; structurally IPCA+8.4% over 12M. Suno target R$82 |
| **MCCI11** *(Mauá Capital CRI)* | n/a | 12.18% | n/a | R$1.00/mo (8 consecutive months) | 2026 H1 guidance R$0.90–1.00. 92% target assets, 28 CRIs + 20 CRI funds. Suno target R$99 |
| **RBRY11** *(RBR CRI)* | n/a | **15.16%** | n/a | R$1.06 (4/17/26) | High-yield private CRI. Suno status "Aguardar" (highest yield = highest risk) |
| **VRTA11** *(Fator Verita)* | R$78.46 | 12.99% | 0.93 | R$0.85 (4/15/26) | Started YTD R$68.59 → R$78.46. Suno status "Aguardar" |

Sources: [Investidor10 — RECR11](https://investidor10.com.br/fiis/recr11/), [Investidor10 — KNCR11](https://investidor10.com.br/fiis/kncr11/), [Investidor10 — VGIP11](https://investidor10.com.br/fiis/vgip11/), [Suno — MCCI11 R$1.00 8 months](https://www.suno.com.br/noticias/mcci11-dividendo-1-real-yield-13-3-fev-2026/), [Investidor10 — RBRY11](https://investidor10.com.br/fiis/rbry11/), [Investidor10 — VRTA11](https://investidor10.com.br/fiis/vrta11/)

### BR watchlist — synthesis

**Macro context** (May 2026): Selic in cutting cycle, Brent volatile around US$70–82 (huge dispersion). FII papel still dominant from yield perspective (12–15% DY) but yields will compress as Selic falls — favoring tijolo/híbrido on duration. Tier-1 stocks (PETR4, AXIA7, CPLE3) all carry **structural events** (Brent dispersion, Novo Mercado migration, post-privatisation maturity).

**The single best risk-reward** in this watchlist (purely a research read, NOT a recommendation): **PGMN3** has the cleanest BTG bull case (+50%, BUY just resumed), GLP-1 tailwind that's structural, and trades below historicals. **CPLE3** is the safer "dividends + growth" combo. **PMLL11** is the cleanest FII tijolo opportunity at NAV discount.

**Highest tail-risk** in watchlist: **SUZB3** (BofA cut R$25 — major analyst capitulation; Citi still bull at R$72; consensus dispersion is the trade), **RAPT4** (recovery story off −81% Q3 2025 base — needs the cycle to turn), **TTEN3** (crushing margins recovery is the entire thesis).

---

## US Watchlist research

> 6 US tickers from `config/universe.yaml > us > watchlist`. Smaller
> than BR list because US holdings are already 22 deep — watchlist is
> "want-to-add" candidates. Each block: Q1 2026 (or latest) read +
> dividend/buyback profile + thesis driver. Sources cited inline.

#### V — Visa *(Financials — Payments)*
- **Q2 FY2026 (calendar Q1 2026)**: net revenue **$11.2bn (+17% YoY)**, GAAP EPS $3.14 / non-GAAP $3.31 (+20%). Payments volume **$3.7T (+9% constant FX)**, processed transactions 66bn (+9%).
- **Capital return**: quarterly dividend $0.670/share (paid 6/1/26). FY annual $2.68 = **0.82% yield**. Payout 25.1% TTM (very low). New **$20bn buyback authorization**.
- **Dividend growth**: 5y CAGR ~14.5%/15% — among the strongest in S&P 500 large-caps.
- **Thesis driver**: secular global cards growth + cross-border travel rebound + tap-to-pay penetration.
- **What to watch**: regulatory pressure (interchange caps in EU + UK); stablecoin disruption optics; cross-border take-rate sustainability.
- Sources: [Stock Titan — Visa Q2 2026 SEC 8-K](https://www.stocktitan.net/sec-filings/V/8-k-visa-inc-reports-material-event-e5b890a6c4d8.html), [Yahoo — Visa Q2 2026 highlights](https://finance.yahoo.com/markets/stocks/articles/visa-inc-v-q2-2026-071023801.html), [MarketBeat — V dividend history](https://www.marketbeat.com/stocks/NYSE/V/dividend/), [Tickeron — V dividend analysis](https://tickeron.com/dividends/V/)

#### MCD — McDonald's *(Consumer Disc. — QSR)*
- **2026 plan**: open **2,600 new restaurants** (~2,100 net of closures), maintain **45–47% operating margin**.
- **Comp sales**: Jefferies projects **US +4%, international +3.5%** for 2026. Q4 2025 adj. EPS $3.12 (vs $3.05 expected) on +6% global comps.
- **Q1 2026 risk**: management warned slowdown likely from January weather + tough comp base.
- **Dividend**: raised 5% to **$1.86/quarter** (paid Mar 17 26), annual $7.44 = **2.60% yield**.
- **Analyst targets**: Wall Street consensus moved to **$341** despite margin/traffic doubts emerging.
- **What to watch**: GLP-1 medications squeezing burger occasions (the bear thesis everyone watches); value menu uptake post-2024 overhaul; franchisee margin health amid wage inflation.
- Sources: [IBTimes — MCD 2026 outlook $341 BUY](https://www.ibtimes.com/mcdonalds-stock-2026-outlook-why-wall-street-sees-mcd-buy-341-target-3801979), [24/7 Wall St — MCD $341 target but cracks showing](https://247wallst.com/investing/2026/04/23/mcdonalds-price-target-hits-341-but-cracks-are-starting-to-show/), [MarketBeat — MCD dividend history](https://www.marketbeat.com/stocks/NYSE/MCD/dividend/), [RoboForex — MCD 2026 forecast](https://roboforex.com/beginners/analytics/forex-forecast/stocks/stocks-forecast-mcdonalds-mcd/)

#### PEP — PepsiCo *(Consumer Staples — Snacks + Beverages)*
- **Q1 2026**: organic revenue **+2.6%**, beat consensus. FY guidance reiterated: organic +2-4%, core constant-FX EPS +4-6%.
- **Frito-Lay turnaround**: NA food **first volume growth in 2+ years** after price cuts of up to **15%** on Lay's, Tostitos, Doritos, Cheetos in Feb. Pepsi expects double-digit shelf-space increase from Q2.
- **Dividend**: raised 4% (June 2026 payment), **54th consecutive year** = Dividend King.
- **Drag**: management explicitly called out "global volatile + uncertain" macro — Middle East war reference.
- **What to watch**: GLP-1 demand erosion on snacks (less-clear than for fast food but real); whether the price-cut strategy lifts category share without margin damage.
- Sources: [CNBC — PepsiCo Q1 2026 earnings](https://www.cnbc.com/2026/04/16/pepsico-pep-q1-2026-earnings.html), [Sure Dividend — PepsiCo Aristocrat focus](https://www.suredividend.com/dividend-aristocrats-pep/), [TIKR — PEP +5% YTD analysts $171](https://www.tikr.com/blog/pepsico-stock-is-up-5-in-2026-and-analysts-point-to-171-upside-ahead), [TheStreet — PEP raises dividend Aristocrat streak](https://www.thestreet.com/investing/stocks/pepsico-pep-stock-raises-dividend-again-to-extend-legendary-streak)

#### ABBV — AbbVie *(Healthcare — Pharma)*
- **Q1 2026**: revenue **$15.0bn (+12.4%)**, beat consensus. Guidance **raised**.
- **Skyrizi + Rinvoq combo** more than offset Humira: Skyrizi **$4.48bn (+30.9%)**, Rinvoq **$2.12bn (+23.3%)**. Humira **$688M (−38.6%)** post-biosimilar.
- **2026 guidance**: revenue ~**$67bn (+9.5%)**, adj EPS **$14.37–14.57**. Q1 raised the prior $14.08–14.28 range by $0.12.
- **Dividend**: 5.5% increase late 2025 = continuation of every-year-since-IPO streak (12 consecutive).
- **Pipeline**: Skyrizi sub-cutaneous induction for Crohn's submitted to FDA, decision expected later in 2026.
- **What to watch**: Skyrizi+Rinvoq peak; pipeline (Botox, neuroscience); whether the post-Humira growth profile re-rates the multiple.
- Sources: [PR Newswire — AbbVie Q1 2026 results](https://www.prnewswire.com/news-releases/abbvie-reports-first-quarter-2026-financial-results-302757172.html), [TIKR — AbbVie record $61bn revenue Skyrizi+Rinvoq peak Humira](https://www.tikr.com/blog/abbvie-posts-record-61b-revenue-as-skyrizi-and-rinvoq-surge-past-peak-humira-sales), [BigGo — ABBV Q1 2026 raises FY](https://finance.biggo.com/news/US_ABBV_2026-04-29), [Seeking Alpha — Strong 2026 outlook expect dividend increases](https://seekingalpha.com/article/4886675-abbvie-strong-2026-outlook-expect-dividend-increases)

#### MSFT — Microsoft *(Technology)*
- **Q3 FY2026 (Apr 29 26)**: revenue **$82.9bn (+18%)**, operating income **$38.4bn (+20%)**, net income **$31.8bn (+23%)** GAAP.
- **Azure**: **+40% (+39% constant FX)**, well above 37% Street consensus. **AI revenue run-rate $37bn (+123% YoY)**. M365 Copilot **>20M seats** (was 15M in Jan).
- **Capital return**: $10.2bn returned in dividends + buybacks Q3.
- **Capex**: ~**$190bn calendar 2026** (incl. ~$25bn from higher component pricing). Q3 already $31.9bn (+49% YoY) — but **below** the $34.9bn consensus, which markets read as conservative ramping.
- **What to watch**: Azure deceleration (40% can't continue forever); OpenAI commercial relationship restructuring; Copilot conversion metrics; whether $190bn capex breaks free cash flow trajectory.
- Sources: [Microsoft IR — FY26 Q3 press release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast), [CNBC — MSFT Q3 2026 earnings](https://www.cnbc.com/2026/04/29/microsoft-msft-q3-earnings-report-2026.html), [TradingKey — MSFT earnings deep dive Azure 40% capex](https://www.tradingkey.com/analysis/stocks/us-stocks/261840966-microsoft-earnings-azure-ai-revenue-capital-spending-stock-drop-tradingkey), [Microsoft News — Cloud + AI strength fuels Q3](https://news.microsoft.com/source/2026/04/29/microsoft-cloud-and-ai-strength-fuels-third-quarter-results/)

#### IBM — International Business Machines *(Technology)*
- **Q1 2026**: revenue **$15.9bn (+9.0%, +6.0% constant FX)**, net income $1.2bn, GAAP EPS $1.30 (vs $1.14 prior year). Op non-GAAP EPS **$1.91**.
- **Software/Red Hat**: software revenue **$7.1bn (+11%)**. Red Hat **+13% (return to double-digit)**. **OpenShift ARR > $2bn**.
- **Mainframe (Z)**: **+48% YoY** — old-tech-as-AI-substrate story (real-time inferencing).
- **Dividend**: raised to **$1.69/quarter**, **31st consecutive year** of increases (Aristocrat).
- **2026 guidance**: >5% constant FX revenue growth, +$1bn YoY free cash flow.
- **What to watch**: AI book-of-business sustaining (consultative + watsonx); software margin trajectory; whether Z+Red Hat combo survives the next mainframe replacement cycle.
- Sources: [IBM Newsroom — Q1 2026 results](https://newsroom.ibm.com/2026-04-22-IBM-RELEASES-FIRST-QUARTER-RESULTS), [Yahoo — IBM Q1 deep dive AI hybrid cloud growth](https://finance.yahoo.com/markets/stocks/articles/ibm-q1-deep-dive-ai-144523817.html), [TheStreet — IBM 27th consecutive dividend hike](https://www.thestreet.com/investing/stocks/ibm-stock-prepares-for-27th-consecutive-dividend-hike-ahead-of-q1-earnings), [Stock Titan — IBM Q1 2026 SEC 8-K](https://www.stocktitan.net/sec-filings/IBM/8-k-international-business-machines-corp-reports-material-event-ff8b866d9081.html)

### US watchlist — synthesis

**Macro context** (May 2026): mega-cap tech (MSFT) carrying the index on AI + capex; consumer staples (PEP, MCD) wrestling with GLP-1 narrative + price-elasticity recalibration; pharma (ABBV) executing the Humira-cliff playbook better than feared; payment networks (V) compounding at high teens despite regulatory pressure; mainframe + hybrid cloud (IBM) rediscovering enterprise pricing power.

**Cleanest add candidates** from this watchlist for our DRIP profile (compounders + dividend track record):
1. **V** — payout 25%, 14% dividend CAGR, secular tailwind. The DRIP poster child. Trades at premium but justifiably.
2. **ABBV** — 12-year dividend streak, post-Humira growth back to +9.5%, pipeline + immunology second leg = de-risked. Yield ~3.5% premium to V.
3. **PEP** — Dividend King (54y), modest upside but very low downside. Frito-Lay turnaround is the optionality.

**Watch-but-don't-add yet**:
- **MSFT** — already represented via concentration in AI thesis; capex cycle could make 2026-2027 a digestion year. Wait for cleaner entry.
- **MCD** — GLP-1 cracks emerging at the same time targets hit highs. Rare adverse divergence — let it sort out.
- **IBM** — old-tech-as-AI-substrate is a thesis I respect but the multi-decade record is uneven. 31y dividend streak is the sole reason it stays a watchlist candidate.

---

## Consolidated sources

> All web sources cited in this document, grouped by section. Each
> entry: title — date accessed (2026-05-05). Inline links above are
> the canonical references; this list is for audit/reproducibility.

### Design canon (Theme 1: FT, WSJ, Bloomberg)
- Klim Type Foundry — [Financier design notes](https://klim.co.nz/blog/financier-design-information/)
- Klim Type Foundry — [Tiempos Text](https://klim.co.nz/fonts/tiempos-text/)
- GitHub — [Financial-Times/o-typography](https://github.com/Financial-Times/o-typography)
- GitHub — [Financial-Times/chart-doctor (Visual Vocabulary)](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md)
- TypeNetwork — [WSJ design chief on type & trustworthiness](https://typenetwork.com/articles/the-wall-street-journals-design-chief-talks-type-and-trustworthiness-after-launching-updated-app)
- Matt Ström-Awn — [WSJ Fonts: Escrow, Exchange & Retina](https://mattstromawn.com/writing/wsjfonts/)
- WSJ Medium — [How we collaboratively built a new design system](https://medium.com/the-wall-street-journal/how-we-collaboratively-built-a-new-design-system-daf4e95a2887)
- Bloomberg LP — [How Terminal UX designers conceal complexity](https://www.bloomberg.com/company/stories/how-bloomberg-terminal-ux-designers-conceal-complexity/)
- @usgraphics on X — [Bloomberg Terminal design philosophy](https://x.com/usgraphics/status/1617581416308695041)
- UX Magazine — [The Impossible Bloomberg Makeover](https://uxmag.com/articles/the-impossible-bloomberg-makeover)
- Karlssonwilker — [Bloomberg Green case study](https://karlssonwilker.com/case-study/bloomberg-green)
- Pentagram — [Bloomberg LP work](https://www.pentagram.com/work/bloomberg-lp)
- Designers Institute NZ — [The Financial Times Redesign case study](https://designersinstitute.nz/case-study/the-financial-times-redesign/)
- García Media — [FT redesign for the digital age](https://garciamedia.com/blog/financial_times_a_classic_redesign_for_the_digital_age/)
- Klim Type Foundry — [Wikipedia entry](https://en.wikipedia.org/wiki/Klim_Type_Foundry)

### Data-ink ratio + density (Theme 2)
- The Doublethink — [Tufte's principles](https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/)
- Holistics — [Data-ink ratio explained](https://www.holistics.io/blog/data-ink-ratio/)
- Plotly Medium — [Maximizing data-ink ratio in dashboards](https://medium.com/plotly/maximizing-the-data-ink-ratio-in-dashboards-and-slide-deck-7887f7c1fab)
- The Data School — [What is the Data Ink Ratio?](https://www.thedataschool.co.uk/calvin-gao/what-is-the-data-ink-ratio/)
- Pencil & Paper — [Dashboard UX patterns](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards)
- DesignRush — [9 dashboard design principles 2026](https://www.designrush.com/agency/ui-ux-design/dashboard/trends/dashboard-design-principles)

### SaaS commoditisation + warm finance (Themes 3 + 4)
- LogRocket — [Linear design: SaaS trend that's boring and bettering UI](https://blog.logrocket.com/ux-design/linear-design/)
- Raw Studio — [UX for SaaS in 2025](https://raw.studio/blog/ux-for-saas-in-2025-what-top-performing-dashboards-have-in-common/)
- Eleken — [Fintech UI examples to build trust](https://www.eleken.co/blog-posts/trusted-fintech-ui-examples)
- Goodface — [Top 10 FinTech product interfaces](https://goodface.agency/insight/top-10-fintech-product-interface-designs/)

### Dark-mode palette + mono fonts (Themes 5 + 6)
- ColorHero — [Dark mode palettes for modern websites 2025](https://colorhero.io/blog/dark-mode-color-palettes-2025)
- Phoenix Strategy Group — [Best palettes for financial dashboards](https://www.phoenixstrategy.group/blog/best-color-palettes-for-financial-dashboards)
- Pangram Pangram — [Best monospace fonts 2025](https://pangrampangram.com/blogs/journal/best-monospace-fonts-2025)
- Octet Design — [18 best monospace fonts](https://octet.design/journal/best-monospace-fonts/)

### Serif typography (Theme 7)
- Adobe Fonts — [Source Serif 4](https://fonts.adobe.com/fonts/source-serif-4)
- Google Fonts — [Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4)
- John Jago — [Source Serif and Charter: a tale of two typefaces](https://johnjago.com/fournier/)
- Figma Resource Library — [31 best serif fonts](https://www.figma.com/resource-library/best-serif-fonts/)

### Wealth platforms (Theme 8)
- Addepar — [Family Office Software](https://addepar.com/family-office-software)
- Robinhood Newsroom — [New visual identity](https://newsroom.aboutrobinhood.com/a-new-visual-identity/)
- Wealthfront Blog — [Introducing the new Dashboard](https://www.wealthfront.com/blog/introducing-new-dashboard/)

### BR watchlist — Tier 1 stocks
- Seu Dinheiro — [PETR4 BTG strong quarter ADR target US$25](https://www.seudinheiro.com/2026/empresas/petrobras-petr4-deve-entregar-trimestre-forte-e-dividendos-robustos-diz-btg-preco-alvo-do-adr-sobe-para-us-25-lvgb/)
- Rio Times — [Petrobras CEO sees Brent US$70 by year-end](https://www.riotimesonline.com/petrobras-oil-forecast-70-dollar-magda-chambriard-april/)
- Simply Wall St — [PETR4 dividend history](https://simplywall.st/stocks/br/energy/bovespa-petr4/petroleo-brasileiro-petrobras-shares/dividend)
- Wikipedia — [Axia Energia](https://pt.wikipedia.org/wiki/Axia_Energia)
- Suno — [Axia Novo Mercado approval](https://www.suno.com.br/noticias/acionistas-axia-energia-axia3-eletrobras-migracao-novo-mercado-go/)
- Seu Dinheiro — [AXIA6 Novo Mercado proposta](https://www.seudinheiro.com/2026/empresas/acionistas-querem-a-axia-energia-axia6-no-novo-mercado-acoes-sobem-apos-proposta-da-eletrica-veja-se-e-hora-de-comprar-miql/)
- Investidor10 — [CPLE3 R$ bilhões dividendos 2026](https://investidor10.com.br/noticias/copel-cple3-pagara-dividendos-bilionarios-em-2026-veja-valor-por-acao-119968/)
- Seu Dinheiro — [Safra: dividendos e crescimento Copel](https://www.seudinheiro.com/2026/empresas/dividendos-e-crescimento-a-eletrica-que-entrega-o-pacote-completo-segundo-safra-lvgb/)
- Arevista — [CPLE3 dispara 80%](https://arevista.com.br/investimentos/cple3-dispara-mais-de-80-ate-onde-vao-os-dividendos-da-copel/)

### BR watchlist — Tier 2 stocks
- PRNewswire — [ALLOS 2Q25 SSR +7.7%](https://www.prnewswire.com/news-releases/allos-2q25-results-sss-7-1-ssr-7-7-and-ffops9-302529529.html)
- Investcred — [ALOS3 will triple monthly dividends](https://investcred.com.br/ultimas-noticias/allos-alos3-triplicara-dividendos-mensais-ate-2026-e-acoes-sobem-forte-apos-3o-tri/)
- Investing.com — [B3SA3 forecast & analyst targets](https://www.investing.com/equities/bmfbovespa-on-nm-consensus-estimates)
- Stock Analysis — [B3SA3 market cap](https://stockanalysis.com/quote/bvmf/B3SA3/market-cap/)
- Análise de Ações — [Energisa R$7.1bn capex 2026](https://www.analisedeacoes.com/noticias/energisa-engi11-projeta-investimentos-de-7-1-bilhoes-em-2026/)
- AgoraMS — [IPCA replacing IGP-M Energisa](https://www.agorams.com.br/com-ipca-no-lugar-do-igp-m-reajuste-da-tarifa-da-energisa-ms-muda-em-2026/)
- Visno Invest — [ES Gás tariff cut](https://visnoinvest.com.br/news/11507/energisa-engi3-engi4-engi11-arsp-homologa-reajuste-da-es-gas-com-reducao-media-de-247-a-partir-de-1o-de-fevereiro-de-2026)
- Seu Dinheiro — [ITUB4 R$3.85bn JCP](https://www.seudinheiro.com/2026/empresas/alem-dos-dividendos-itau-unibanco-itub4-anuncia-r-385-bilhoes-em-jcp-veja-valor-por-acao-e-quem-tem-direito-lvgb/)
- O Especialista (Safra) — [Itaú 4T25 análise](https://oespecialista.safra.com.br/itau-itub4-analise-4t25/)
- Investidor10 — [ITUB4 financial overview](https://investidor10.com.br/acoes/itub4/)
- Investing & Notícias — [EQTL3 sells transmission to CDPQ R$9.4bn](https://www.investimentosenoticias.com.br/noticias/mercado/equatorial-eqtl3-vende-divisao-de-transmissao-para-cdpq-por-r94-bilhoes-e-foca-em-novas-estrategias-apos-aquisicao-da-sabesp-sbsp3/)
- Money Times — [EQTL3 leva 15% Sabesp](https://www.moneytimes.com.br/sabesp-sbsp3-equatorial-eqtl3-leva-15-e-sera-o-investidor-referencia/)
- Empiricus — [Equatorial Day expansão Sabesp](https://www.empiricus.com.br/artigos/investimentos/equatorial-day-eqtl3-expansao-de-negocios-com-a-sabesp-sbsp3-caminha-e-geracao-de-valor-continua-diz-analista/)
- DiárioDoTransporte — [Motiva 1T26 +16.3%](https://diariodotransporte.com.br/2026/05/03/motiva-tem-alta-de-163-no-lucro-liquido-ajustado-do-1t26-para-r-627-milhoes/)
- Suno — [Motiva BB 1T26 mantém compra](https://www.suno.com.br/noticias/motiva-motv3-resultado-1t26-bb-investimentos-compra-go/)
- InfoMoney — [Motiva 1T26 R$627M](https://www.infomoney.com.br/mercados/motiva-motv3-resultados-primeiro-trimestre-2026/)
- BPMoney — [MULT3 1T26 +35.1%](https://bpmoney.com.br/mercado/multiplan-mult3-lucra-r-3161-milhoes-no-1t26-alta-de-351-e-recorde-para-o-periodo/)
- Money Times — [MULT3 expansion plans + dividends](https://www.moneytimes.com.br/multiplan-mult3-preve-expansao-de-shoppings-em-2026-e-nao-descarta-elevar-dividendos-veja-planos-igdl/)
- MarketScreener — [MULT3 analyst consensus](https://www.marketscreener.com/quote/stock/MULTIPLAN-EMPREENDIMENTOS-6499840/consensus/)
- Seu Dinheiro — [BTG buy on PGMN3 R$9](https://www.seudinheiro.com/2026/empresas/a-virada-da-pague-menos-pgmn3-o-que-esta-por-tras-da-recomendacao-de-compra-do-btg-pactual-lvgb/)
- Investidor10 — [PGMN3 financials](https://investidor10.com.br/acoes/pgmn3/)
- Money Times — [PLPL3 MCMV faixa 1 velocidade](https://www.moneytimes.com.br/plano-plano-avanca-na-faixa-1-do-mcmv-onde-velocidade-de-vendas-surpreende-6/)
- Seu Dinheiro — [PLPL3 tier 4 BTG +34%](https://www.seudinheiro.com/2026/empresas/construtora-queridinha-do-minha-casa-minha-vida-se-prepara-para-acelerar-em-2026-e-acao-deve-saltar-mais-de-34-segundo-o-btg-pactual-bdap/)
- Nord — [PLPL3 4T25 recordes](https://www.nordinvestimentos.com.br/blog/plano-plano-resultados-4t25/)
- InfoMoney — [Marcopolo 1T26 R$265M](https://www.infomoney.com.br/mercados/marcopolo-pomo4-resultados-primeiro-trimestre-2026/)
- XP — [POMO4 4T25 rentabilidade sólida 2026](https://conteudos.xpi.com.br/acoes/relatorios/marcopolo-pomo4-rentabilidade-solida-com-indicacoes-positivas-para-2026e-resultados-do-4t25/)
- CNPL — [Marcopolo LatAm growth](https://www.cnpl.org.br/marcopolo-busca-crescimento-na-america-latina-para-enfrentar-desaceleracao-no-brasil/)
- Seu Dinheiro — [Randon Arauco/Rumo contract](https://www.seudinheiro.com/2026/empresas/randon-rapt4-salta-ate-8-apos-fechar-contrato-com-arauco-e-rumo-rail3-lvgb/)
- InfoMoney — [Randoncorp Q3 2025 −81%](https://www.infomoney.com.br/mercados/randoncorp-rapt4-resultados-terceiro-trimestre-2025/)
- Acionista — [RAPT4 megacontrato BUY](https://acionista.com.br/rapt4-disparou-apos-megacontrato-e-hora-de-comprar/)
- EBC — [RDOR3 4T25 R$1.2bn lucro queda da ação](https://www.ebc.com/pt/forex/rdor3-resultados-4t25-lucro-sulamerica-queda-acoes)
- Empiricus — [SulAmérica beneficiários sólidos](https://www.empiricus.com.br/artigos/investimentos/rede-dor-sulamerica-apresenta-crescimento-solido-de-beneficiarios-e-reforca-tese-de-investimento-nas-acoes-rdor3-saiba-mais-capf/)
- Genial — [RDOR3 SULA11 incorporação](https://analisa.genialinvestimentos.com.br/acoes/rede-dor/rede-dor-incorpora-sulamerica-se-nao-comprar-a-solucao-e-ser-comprado-rdor3-sula11/)
- InfoMoney — [RENT3 reporta resultados positivos](https://www.infomoney.com.br/mercados/localiza-rent3-reporta-resultados-positivos-e-analistas-reforcam-confianca-na-acao/)
- Seu Dinheiro — [RENT3 carros chineses BTG +25%](https://www.seudinheiro.com/2026/empresas/localiza-rent3-sofre-com-invasao-de-carros-chineses-mas-ha-esperancas-acao-pode-subir-ate-25-segundo-o-btg-kaes/)
- XP — [Localiza 1T26 prévia](https://conteudos.xpi.com.br/acoes/relatorios/localiza-rent3-previa-do-1t26-atualizacao-de-estimativas/)
- Money Times — [Citi raises SUZB3 target +23%](https://www.moneytimes.com.br/suzano-suzb3-citi-eleva-mais-uma-vez-preco-alvo-para-acao-por-operacional-mais-forte-e-melhora-para-celulose-pads/)
- Suno — [SUZB3 1T26 decepção](https://www.suno.com.br/noticias/suzano-suzb3-resultado-1t26-ebitda-celulose-mt/)
- Seu Dinheiro — [BofA cuts R$25 from SUZB3](https://www.seudinheiro.com/2026/empresas/suzano-suzb3-bofa-corta-r-25-do-preco-alvo-e-acoes-despencam-lvgb/)
- InfoMoney — [Suzano May price hikes](https://www.infomoney.com.br/mercados/suzano-elevara-celulose-na-europa-e-americas-em-maio-anuncio-e-agridoce-diz-bbi/)
- Investidor10 — [XP elege TTEN3 favorita 50%](https://investidor10.com.br/noticias/xp-elege-3tentos-tten3-como-favorita-no-agro-com-potencial-alta-de-50-118011/)
- Nord — [TTEN3 projeções 2026](https://www.nordinvestimentos.com.br/blog/3tentos-tten3-projecoes-2026-meta-receita-2032/)
- XP — [TTEN3 3T25 positive but hard to interpret](https://conteudos.xpi.com.br/acoes/relatorios/3tentos-tten3-revisao-dos-resultados-do-3t25-positivo-porem-dificil-de-interpretar/)

### BR watchlist — FIIs
- Status Invest — [PMLL11](https://statusinvest.com.br/fundos-imobiliarios/pmll11)
- Investidor10 — [PMLL11](https://investidor10.com.br/fiis/pmll11/)
- Genial — [VISC11](https://www.genialinvestimentos.com.br/onde-investir/renda-variavel/fiis/visc11/)
- Investidor10 — [VISC11](https://investidor10.com.br/fiis/visc11/)
- Status Invest — [TRXF11](https://statusinvest.com.br/fundos-imobiliarios/trxf11)
- Investidor10 — [GARE11](https://investidor10.com.br/fiis/gare11/)
- InfoMoney — [GARE11 2026 dividend guidance](https://www.infomoney.com.br/onde-investir/fii-gare11-mantera-patamar-de-dividendos-para-2026-gestor-responde-duvidas/)
- Investidor10 — [HGRU11](https://investidor10.com.br/fiis/hgru11/)
- Status Invest — [MCRE11](https://statusinvest.com.br/fundos-imobiliarios/mcre11)
- Investidor10 — [KNRI11](https://investidor10.com.br/fiis/knri11/)
- Suno — [HGLG11 2026 R$1.10–1.17 guidance](https://www.suno.com.br/noticias/hglg11-rendimentos-2026-projecoes/)
- Suno — [BRCO11 dividends raised](https://www.suno.com.br/noticias/brco11-dividendos-095-maio-2026/)
- FundsExplorer — [XPLG11 vacancy 8.7%](https://www.fundsexplorer.com.br/noticias/xplg11-dividendo-abril-2026)
- Investidor10 — [XPLG11](https://investidor10.com.br/fiis/xplg11/)
- Investidor10 — [RECR11](https://investidor10.com.br/fiis/recr11/)
- Investidor10 — [KNCR11](https://investidor10.com.br/fiis/kncr11/)
- Investidor10 — [VGIP11](https://investidor10.com.br/fiis/vgip11/)
- Suno — [MCCI11 R$1.00 8 months](https://www.suno.com.br/noticias/mcci11-dividendo-1-real-yield-13-3-fev-2026/)
- Investidor10 — [RBRY11](https://investidor10.com.br/fiis/rbry11/)
- Investidor10 — [VRTA11](https://investidor10.com.br/fiis/vrta11/)

### US watchlist
- Stock Titan — [Visa Q2 2026 SEC 8-K](https://www.stocktitan.net/sec-filings/V/8-k-visa-inc-reports-material-event-e5b890a6c4d8.html)
- Yahoo — [Visa Q2 2026 highlights](https://finance.yahoo.com/markets/stocks/articles/visa-inc-v-q2-2026-071023801.html)
- MarketBeat — [V dividend history](https://www.marketbeat.com/stocks/NYSE/V/dividend/)
- Tickeron — [V dividend analysis](https://tickeron.com/dividends/V/)
- IBTimes — [MCD 2026 outlook $341](https://www.ibtimes.com/mcdonalds-stock-2026-outlook-why-wall-street-sees-mcd-buy-341-target-3801979)
- 24/7 Wall St — [MCD $341 target but cracks showing](https://247wallst.com/investing/2026/04/23/mcdonalds-price-target-hits-341-but-cracks-are-starting-to-show/)
- MarketBeat — [MCD dividend history](https://www.marketbeat.com/stocks/NYSE/MCD/dividend/)
- RoboForex — [MCD 2026 forecast](https://roboforex.com/beginners/analytics/forex-forecast/stocks/stocks-forecast-mcdonalds-mcd/)
- CNBC — [PepsiCo Q1 2026 earnings](https://www.cnbc.com/2026/04/16/pepsico-pep-q1-2026-earnings.html)
- Sure Dividend — [PepsiCo Aristocrat](https://www.suredividend.com/dividend-aristocrats-pep/)
- TIKR — [PEP +5% YTD analysts $171](https://www.tikr.com/blog/pepsico-stock-is-up-5-in-2026-and-analysts-point-to-171-upside-ahead)
- TheStreet — [PEP raises dividend](https://www.thestreet.com/investing/stocks/pepsico-pep-stock-raises-dividend-again-to-extend-legendary-streak)
- PR Newswire — [AbbVie Q1 2026 results](https://www.prnewswire.com/news-releases/abbvie-reports-first-quarter-2026-financial-results-302757172.html)
- TIKR — [AbbVie record $61bn revenue](https://www.tikr.com/blog/abbvie-posts-record-61b-revenue-as-skyrizi-and-rinvoq-surge-past-peak-humira-sales)
- BigGo — [ABBV Q1 2026 raises FY](https://finance.biggo.com/news/US_ABBV_2026-04-29)
- Seeking Alpha — [Strong 2026 outlook expect dividend increases](https://seekingalpha.com/article/4886675-abbvie-strong-2026-outlook-expect-dividend-increases)
- Microsoft IR — [FY26 Q3 press release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast)
- CNBC — [MSFT Q3 2026 earnings](https://www.cnbc.com/2026/04/29/microsoft-msft-q3-earnings-report-2026.html)
- TradingKey — [MSFT earnings deep dive Azure 40%](https://www.tradingkey.com/analysis/stocks/us-stocks/261840966-microsoft-earnings-azure-ai-revenue-capital-spending-stock-drop-tradingkey)
- Microsoft News — [Cloud + AI strength fuels Q3](https://news.microsoft.com/source/2026/04/29/microsoft-cloud-and-ai-strength-fuels-third-quarter-results/)
- IBM Newsroom — [Q1 2026 results](https://newsroom.ibm.com/2026-04-22-IBM-RELEASES-FIRST-QUARTER-RESULTS)
- Yahoo — [IBM Q1 deep dive AI hybrid cloud](https://finance.yahoo.com/markets/stocks/articles/ibm-q1-deep-dive-ai-144523817.html)
- TheStreet — [IBM 27th consecutive dividend hike](https://www.thestreet.com/investing/stocks/ibm-stock-prepares-for-27th-consecutive-dividend-hike-ahead-of-q1-earnings)
- Stock Titan — [IBM Q1 2026 SEC 8-K](https://www.stocktitan.net/sec-filings/IBM/8-k-international-business-machines-corp-reports-material-event-ff8b866d9081.html)

---

## Closing — what to attack first when you're back

Top of the queue:

1. **Open mission-control in browser, toggle dark/light** — verify v3 actually feels FT/WSJ-coded and not "Linear with serif headlines."
2. **Sprint 2** if visual feels right — page-by-page editorial pass (Tasks, Council, Allocation, Ticker). The remaining `card p-5` and `pill-purple/cyan` patterns will dilute the broadsheet identity if left.
3. **Sprint 3** (status bar) before Sprint 4 (web font) — the global status strip is **functional value**, the web font is **polish**. Function first.
4. **Watchlist deep-dives**: PGMN3, CPLE3, PMLL11 are the three I'd queue for `ii deepdive` first based on the synthesis above. ABBV and V are the two cleanest US adds for our DRIP profile.

If anything looks like it didn't survive the night (stale data, broken links, misread numbers), grep for the ticker in this doc and triangulate against the actual primary source — most of the financial data was extracted from secondary aggregators (Investidor10, StatusInvest, etc.), so primary IR pages are the canonical truth.




