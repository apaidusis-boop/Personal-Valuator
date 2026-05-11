# Design Research — GitHub Deep Dive (Anti-Slop Patterns)

> Purpose: extract concrete patterns from 5 community Skills repos that fix the AI-slop pattern user identified in `FairTrajectoryChart`, `ConsensusPanel`, `ReadyToBuyTile`. Distillation, not transcription. Date: 2026-05-08.

---

## Context: what we are fixing

The 3 shipped components are textbook AI-slop tells:

- `fair-trajectory-chart.tsx` — **default Recharts** (`LineChart`, default Tooltip, default Legend, default axis ticks). Zero typographic hierarchy. No editorial voice. No domain framing ("conservative target" vs "consensus ceiling" is buried in a code comment, not the UI).
- `consensus-panel.tsx` — generic table consensus panel.
- `ready-to-buy-tile.tsx` — emoji checkmarks (`✓ verified`, `✗ disputed`), pill action badges with `var(--gain)` backgrounds, "tile" framing, `bg-overlay` cards.

This is the slop fingerprint these 5 repos exist to catch.

---

## 1. Leonxlnx/taste-skill

- **Stars / Push / Lang**: 16,214 / 2026-05-06 / Shell
- **What it actually does**: A bundle of 11 portable Agent Skills (`SKILL.md` files) that ship as a shell-installable package. Each skill is a strict prompt overlay that **rewrites the model's frontend defaults** — bans Inter, bans purple/blue gradients, bans 3-equal-card grids, mandates state coverage (loading/empty/error), enforces font/spacing/motion rules with metric thresholds. Three numeric "dials" (`DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`) act as global state for the prompt logic.
- **Key files**:
  - `skills/taste-skill/SKILL.md` — main all-rounder, 10 sections + final pre-flight checklist
  - `skills/redesign-skill/SKILL.md` — **the most relevant skill for our case** (existing project audit, not greenfield); 6-step Fix Priority
  - `skills/gpt-tasteskill/SKILL.md` — stricter variant: AIDA structure, 2-line Hero rule, gapless bento, banned meta-labels ("SECTION 01")
  - `skills/minimalist-skill/SKILL.md` — Notion/Linear editorial register
  - `skill.sh` + `skills/llms.txt` — install discovery for `npx skills add`
- **5 extractable patterns**:
  1. **The Forbidden List** is a deliverable, not a vibe. Each skill ships a literal "AI Tells (Forbidden Patterns)" section the model checks against pre-output: NO Inter, NO `#000000`, NO purple/blue gradients, NO oversized H1s, NO 3-equal cards, NO "John Doe", NO `99.99%`/`50%` round numbers, NO "Elevate"/"Seamless"/"Unleash" copy, NO Lucide-default icons, NO custom mouse cursors.
  2. **Numeric dials at the top of the prompt** (`DESIGN_VARIANCE: 8`, `MOTION_INTENSITY: 6`, `VISUAL_DENSITY: 4`) are referenced inside conditional rules later (`if DENSITY > 7 then BAN cards, use border-t/divide-y`). Turns a vibe into a switch the model can't ignore.
  3. **Anti-Center Bias rule for hero/data-display** — banned when variance > 4. Forces split-screen, asymmetric whitespace, or zigzag instead of the centered hero/centered tile.
  4. **Mandatory state coverage** — Loading skeletons matching layout shape (no spinners), composed Empty States, inline Error States, and `:active { -translate-y-[1px] }` tactile feedback. LLMs default to "static success" only.
  5. **Bento 2.0 spec** for dashboards: white cards on `#f9fafb`, `rounded-[2.5rem]`, **labels OUTSIDE and BELOW cards**, diffusion shadow `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`, perpetual micro-interactions per card with spring `stiffness:100, damping:20`.
- **Adoption fit (0-10)**:
  - `FairTrajectoryChart`: **9** — `redesign-skill` directly applies. Dial `VISUAL_DENSITY: 8` triggers "border-t/divide-y instead of cards", monospace numbers (`tabular-nums`), tinted shadows, ban Inter.
  - `ConsensusPanel`: **9** — same. Plus "NO 3-Column Card Layouts" rule kills the obvious slop reflex; mandates state coverage.
  - `ReadyToBuyTile`: **10** — emoji ban is explicit (`NEVER use emojis in code, markup, text content, or alt text. Replace with high-quality icons (Radix, Phosphor) or clean SVG primitives.`); pill-badge "New/Beta" ban is explicit; "Generic card look" callout is explicit.
- **Install**:
  ```bash
  npx skills add https://github.com/Leonxlnx/taste-skill --skill "redesign-existing-projects"
  npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
  ```

---

## 2. pbakaus/impeccable

- **Stars / Push / Lang**: 26,208 / 2026-05-04 / JavaScript
- **What it actually does**: A full **command-driven design harness** (23 sub-commands: `craft`, `shape`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `distill`, `harden`, `delight`, `colorize`, `typeset`, `layout`, `clarify`, `live`, etc.). Loads project-specific `PRODUCT.md` + `DESIGN.md` context before any design action via mandatory `IMPECCABLE_PREFLIGHT` gate. Ships an **automated detector**: `npx impeccable --json [target]` flags 27 specific anti-patterns; `npx impeccable live` injects an in-browser overlay that highlights findings on the live page. Includes 35 reference docs covering specific situations (`cognitive-load.md`, `personas.md`, `heuristics-scoring.md`, `motion-design.md`).
- **Key files**:
  - `skill/SKILL.md` — preflight gates, register selection (brand vs product), shared design laws, command routing
  - `DESIGN.md` (root) — full design system spec for impeccable's own site; shows the **OKLCH-only rule**, "warm-paper-not-white", "italic-is-voice", "1.6 leading rule"
  - `skill/reference/critique.md` — runs **two independent sub-agent assessments** (LLM + deterministic) so they can't anchor to each other; outputs Nielsen 10-heuristic score + persona red flags + P0-P3 issue list
  - `skill/reference/audit.md` — 5-dimension technical audit (a11y, perf, theming, responsive, anti-patterns) scored 0-4 each
  - `skill/reference/polish.md` — Design System Discovery → drift classification (missing token / one-off implementation / conceptual misalignment)
  - `skill/reference/bolder.md` — fixes "boring/generic" by amplifying hierarchy; explicit "WARNING - AI SLOP TRAP: bold means distinctive, not 'more effects'"
  - `skill/reference/typography.md` — vertical rhythm = line-height; modular scale ≥1.25; system fonts underrated
- **5 extractable patterns**:
  1. **Brand vs Product register** — the same skill behaves differently if it identifies the surface as a marketing page (design IS the product, push) vs a dashboard (design SERVES the product, restraint). Decision is one of: cue in task → surface in focus → `register:` field in PRODUCT.md. We are pure **product** register.
  2. **The AI Slop Test** has a category-reflex check at two altitudes: *first-order* ("could someone guess theme+palette from category alone? finance → navy + gold = fail") and *second-order* ("can someone guess from category-plus-anti-references? fintech-not-navy-and-gold → terminal-dark-mode = fail"). Both must NOT be obvious.
  3. **Absolute bans (match-and-refuse)**: side-stripe borders >1px (we have these in alerts), gradient text via `background-clip: text`, glassmorphism as default, **the hero-metric template** (big number + small label + supporting stats + gradient accent — exactly our `ReadyToBuyTile`), identical card grids, modals as first thought.
  4. **OKLCH-only color rule** + tinted neutrals (chroma 0.005-0.01 nudges every "neutral" toward the brand hue). Pure `#000`/`#fff` banned. Strategy axis: Restrained / Committed / Full palette / Drenched — pick before picking colors.
  5. **Two-isolated-assessments critique pattern** — LLM review + deterministic CLI scan + browser overlay, run independently in different tabs (no anchoring). Synthesis labels P0-P3, ties each to a fix command. Replicable in our verdict/critique flows.
- **Adoption fit (0-10)**:
  - `FairTrajectoryChart`: **8** — typeset.md (vertical rhythm), motion-design.md (ease-out-quart, no bounce), polish.md (drift classification: missing token vs one-off vs conceptual). Critique command would catch the default Recharts as "drift from DESIGN.md".
  - `ConsensusPanel`: **9** — distill, layout, harden references directly apply. Cognitive load 8-item check would flag a dense generic table.
  - `ReadyToBuyTile`: **10** — explicitly banned: "the hero-metric template" + side-stripe borders + identical card grids. `bolder` reference says "stronger hierarchy, clearer weight contrast, one sharper accent" instead of effects.
- **Install**:
  ```bash
  # As Claude Code skill:
  cp -r .impeccable/skills/impeccable .claude/skills/
  # Or use the npx CLI:
  npx impeccable --json mission-control/components/ready-to-buy-tile.tsx
  npx impeccable live  # then inject detect.js into localhost:3000
  ```

---

## 3. KAOPU-XiaoPu/web-design

- **Stars / Push / Lang**: 302 / 2026-04-16 / Python
- **What it actually does**: One single SKILL with a strict **2-phase workflow**: Phase A (gather requirements: URL/screenshot/PRD/keywords) → Phase B (output a **DESIGN.md** spec file as a DELIVERABLE that user confirms) → Phase C (only then write code). Includes Playwright-based competitor crawler script that extracts color tokens + viewport screenshots + motion audit. Ships 58 pre-built brand design systems (Linear/Stripe/Apple/etc.) cached as `.md` files for offline use.
- **Key files**:
  - `SKILL.md` (root) — full Phase A/B/C workflow, "首页爆点原则" (homepage hook principle), L1/L2/L3 interaction tier system, **100-point quality red lines**
  - `references/design-md-template.md` — the 9-section DESIGN.md template (Visual Theme / Color / Typography / Components / Layout / Depth / Animation / Do's-Don'ts / Responsive)
  - `references/quality-checklist.md` — final audit checklist
  - `references/design-systems/INDEX.md` — 58 brand cards
  - `scripts/crawl_website.py` — Playwright crawler with viewport screenshots + token extraction
- **5 extractable patterns**:
  1. **Spec-first, code-second**. DESIGN.md is the deliverable — a 9-section file (Color tokens with RGB helper values, font `@import` URLs, components with **all** states default/hover/active/focus/disabled, motion tier L1/L2/L3, Do's and Don'ts ≥8 with ≥5 Don'ts). Code only after user confirms the spec. Halts the "model just writes JSX" reflex.
  2. **L1/L2/L3 interaction tiers** — explicit ladder. L1 = static + soft hover; L2 = scroll reveal + parallax + nav state changes; L3 = pin/scrub + cursor effects + transitions. Every component declares its tier and all L2+ MUST include `prefers-reduced-motion` fallback. Forces the model to commit to a level instead of mixing.
  3. **The 100-point Quality Red Lines** — hard `IF-fail-THEN-not-shipped` checks: zero hardcoded hex values (CSS variables only), every interactive element has hover+focus state, NO solid-color image placeholders, all images have real source (Unsplash seed/Picsum/user asset), L2+ has signature animations from a curated library (≥1 each: text-hero, text-section, body, element-level, component, background).
  4. **Competitor extraction loop** — when user says "make it like Linear", the script first looks up the cached `design-systems/linear.md`; if missing, runs Playwright crawler that captures viewport screenshots + extracts CSS tokens + motion audit. Avoids the model hallucinating Linear's design from training data.
  5. **Chinese-page typography rules** (relevant for our PT-BR vault content): line-height ≥1.7, letter-spacing 0.02em, body ≥15-16px, Latin-and-CJK font-family chain.
- **Adoption fit (0-10)**:
  - `FairTrajectoryChart`: **7** — DESIGN.md spec discipline forces explicit chart-color-tokens, axis-typography rules, tooltip-copy rules in spec FIRST. The 100-point list catches "default Recharts tooltip" instantly.
  - `ConsensusPanel`: **8** — table-component spec (with all states) is one of the 9 mandatory sections.
  - `ReadyToBuyTile`: **6** — less direct (oriented toward landing pages), but Do's-and-Don'ts list with ≥5 Don'ts mandate is useful for "tile" anti-pattern.
- **Install**:
  ```bash
  # Copy the SKILL.md + references/ into .claude/skills/web-design/
  curl -L https://github.com/KAOPU-XiaoPu/web-design/archive/main.tar.gz | tar xz -C /tmp
  mkdir -p .claude/skills/web-design
  cp -r /tmp/web-design-main/{SKILL.md,references,scripts} .claude/skills/web-design/
  ```

---

## 4. nexu-io/open-design

- **Stars / Push / Lang**: 33,772 / 2026-05-08 / TypeScript
- **What it actually does**: Local-first alternative to Anthropic's Claude Design. **97 skills** (we miscounted — the README says 19 categories but the skills/ folder has 97 dirs) and **142 brand-grade design systems** (counted via API). Each skill emits a single self-contained HTML file with inline CSS/JS, scoped via `data-od-id` for comment mode, with a strict P0/P1/P2 checklist per skill. Skills relevant to us: `finance-report`, `dashboard`, `trading-analysis-dashboard-template`, `dcf-valuation`, `ib-pitch-book`, `critique`, `tweaks`, `live-dashboard`, `live-artifact`, `pm-spec`, `wireframe-sketch`, `pricing-page`.
- **Key files**:
  - `skills/finance-report/SKILL.md` — quarterly report template (masthead + KPI strip + revenue chart + P&L table + outlook); rule: **"every number ties to a labelled chart or table; deltas show direction and percentage; accent colour used at most twice"**
  - `skills/dashboard/SKILL.md` — admin/analytics single-screen layout; **"Accent used at most twice (sidebar active + one chart highlight)"**, **"inline SVG only, no JS chart libraries"** (kills Recharts default reflex)
  - `skills/trading-analysis-dashboard-template/SKILL.md` + `references/checklist.md` — Wall-Street terminal: dense panels + light/dark + live/demo modes + chart hover crosshair + click-to-focus + command palette `/`. P0 checklist: at least 2 charts have axis labels + units + legends; placeholder values are honest (`—`).
  - `skills/critique/SKILL.md` — **5-dimension expert review** (Philosophy / Visual Hierarchy / Detail Execution / Functionality / Innovation, each 0-10) outputs HTML radar chart + Keep/Fix/Quick-wins lists. Hard rules: every score has cited evidence (class name / line / page); no average above 8 without scrutiny.
  - `skills/dcf-valuation/SKILL.md` — every input row labelled `sourced` / `derived` / `user-provided` / `assumption`; sensitivity matrix mandatory; terminal-value-as-%-of-EV check
  - `skills/tweaks/SKILL.md` — wraps any artifact with side panel of live `--accent` / `--scale` / `--density` / `--mode` / `--motion` knobs persisted to `localStorage`. Curated swatches only, no free color picker
  - `design-systems/editorial/DESIGN.md` — Gelasio serif + Ubuntu Mono numerals, 8pt grid, single-color-meaning rule (one color = one semantic). 142 such systems available.
- **5 extractable patterns**:
  1. **"Accent at most twice" rule** — finance-report and dashboard both enforce this. Our `ReadyToBuyTile` uses gain/loss/secondary in 5+ places; cut to 2.
  2. **"Inline SVG charts only, no JS libraries"** for dashboards — directly kills the default-Recharts smell. Ten-line `<polyline>` line-chart + N `<rect>` bars beats default Recharts visual quality every time because every glyph is intentional.
  3. **Honest placeholders rule** — "placeholder values are honest (`—` if unknown), no fabricated marketing claims, no `99.99%` round numbers". DCF skill formalizes it: each row tagged `sourced`/`derived`/`assumption`. Map directly to our `confidence_label: "single_source" | "cross_validated" | "disputed"`.
  4. **5-dim critique with cited evidence** is replicable. We already have `ii deepdive` and synthetic_ic; adding a `ii design-critique <component-path>` that radars Philosophy/Hierarchy/Detail/Function/Innovation would close the loop **before** the user sees the slop.
  5. **142-design-system bank** — when picking a register for Mission Control, instead of inventing tokens, copy from `design-systems/editorial/DESIGN.md` (already a JPM-adjacent feel: serif headings + tabular-num data) or `design-systems/dashboard`, `cohere`, `linear-app`, `clickhouse`, `arc`. They are MIT-licensed pre-built spec files.
- **Adoption fit (0-10)**:
  - `FairTrajectoryChart`: **10** — `dashboard` skill literally says "inline SVG charts, no JS libs, accent twice max, axis labels + units + legends mandatory". `trading-analysis-dashboard-template` ships a working hover-crosshair + click-to-focus implementation we can lift wholesale.
  - `ConsensusPanel`: **10** — `finance-report` SKILL is exactly this format (P&L table + KPI strip + outlook). `critique` skill scores our component on 5 dims with evidence.
  - `ReadyToBuyTile`: **9** — `finance-report` + `dashboard` rules ("accent twice max", honest placeholders, KPI strip layout). `dcf-valuation` source-tagging is a perfect map for our `confidence_label`.
- **Install**:
  ```bash
  # Sparse-checkout just the skills we need (saves 134 MB):
  git clone --filter=blob:none --no-checkout https://github.com/nexu-io/open-design.git /tmp/od
  cd /tmp/od && git sparse-checkout init --cone && \
    git sparse-checkout set skills/dashboard skills/finance-report \
      skills/trading-analysis-dashboard-template skills/critique skills/tweaks \
      skills/dcf-valuation design-systems/editorial design-systems/dashboard \
      design-systems/linear-app design-systems/clickhouse
  git checkout
  cp -r skills/{dashboard,finance-report,critique,tweaks} \
    "C:/Users/paidu/investment-intelligence/.claude/skills/"
  ```

---

## 5. ConardLi/garden-skills

- **Stars / Push / Lang**: 2,707 / 2026-05-07 / CSS
- **What it actually does**: Smaller curated collection (4 skills total): `web-design-engineer`, `gpt-image-2`, `kb-retriever`, `web-video-presentation`. Strongest piece is `web-design-engineer/SKILL.md` (22.6 KB) — a dense workflow doc that emphasizes **"Stunning, not functional"** as the bar, declares design system in markdown BEFORE writing code, ships a **v0 draft early** with placeholders, and includes very practical React+Babel inline-JSX rules (3 hard non-negotiables). Less broad than open-design but the prose is sharper.
- **Key files**:
  - `skills/web-design-engineer/SKILL.md` — 6-step workflow, design-system declaration, v0 draft pattern, React+Babel hard rules, AI cliché list, placeholder philosophy, output-type guidelines (prototype/deck/dashboard/animation), Tweaks panel pattern
  - `skills/web-design-engineer/references/` — advanced patterns (device frames, slide engine, animation timeline)
- **5 extractable patterns**:
  1. **"Code ≫ Screenshots"** — when the user provides both a codebase and a screenshot, invest effort in reading the source code and extracting tokens, not in guessing from the image. Direct counsel for our case: the slop fix starts by re-reading the components, not re-rendering them.
  2. **v0 draft with explicit assumptions+placeholders** before full build. *"A v0 with assumptions and placeholders is more valuable than a perfect v1 that took 3x the time — if the direction is wrong, the latter has to be scrapped entirely."* Maps to the user's "very bad" feedback: we shipped v1 without v0 confirmation.
  3. **Declare design system in markdown FIRST, get user confirmation, THEN code**:
     ```markdown
     - Color palette: [primary / secondary / neutral / accent]
     - Typography: [heading font / body font / code font]
     - Spacing system: [base unit and multiples]
     - Border-radius strategy: [large / small / sharp]
     - Shadow hierarchy: [elevation 1–5]
     - Motion style: [easing curves / duration / trigger]
     ```
  4. **Placeholder philosophy** — *"a placeholder is more professional than a poorly drawn fake"*. Missing icon → `[icon]` square + label. Missing data → ASK USER, **never fabricate**. Missing logo → brand name in text + simple geometric shape. A placeholder signals "real material needed"; a fake signals "I cut corners".
  5. **No-emoji rule** + AI-slop list: gradient backgrounds (especially purple-pink-blue), rounded cards with colored left-border accent, complex SVG illustrations, gradient buttons + large-radius cards combo, overused fonts (Inter/Roboto/Arial/Fraunces/system-ui), data-slop (meaningless stats/icons spam), fabricated logo walls.
- **Adoption fit (0-10)**:
  - `FairTrajectoryChart`: **7** — strong on "code first, screenshots second" + design-system-declaration-first; less specific on chart anti-patterns than open-design.
  - `ConsensusPanel`: **7** — same strengths, less concrete checklist.
  - `ReadyToBuyTile`: **9** — "no-emoji default" + "rounded cards with colored left-border accent" + "data-slop" all describe the tile exactly. Placeholder philosophy applies to disputed/missing-data states.
- **Install**:
  ```bash
  npm install -g @conardli/garden-skills  # if published; otherwise:
  curl -L https://github.com/ConardLi/garden-skills/archive/main.tar.gz | tar xz -C /tmp
  cp -r /tmp/garden-skills-main/skills/web-design-engineer .claude/skills/
  ```

---

## Top 3 recommendations (install first)

### 1. **Install `pbakaus/impeccable` first** — it's a harness, not just a prompt

It gives us a **runnable detector** (`npx impeccable --json` and `npx impeccable live` browser overlay) that surfaces 27 specific anti-patterns deterministically. Skills/prompts that just sit in a SKILL.md require the model to remember to apply them; impeccable's CLI scan runs against any HTML/JSX file and exits nonzero on findings. This means we can wire it into `daily_run.bat` and CI as a gate, not just hope.

```bash
cd C:\Users\paidu\investment-intelligence\mission-control
npm install --save-dev impeccable
npx impeccable --json components/ready-to-buy-tile.tsx components/fair-trajectory-chart.tsx components/consensus-panel.tsx > ../obsidian_vault/Bibliotheca/Impeccable_Audit_2026-05-08.json
npx impeccable live &
# Then open localhost:3000 and inject the overlay (see critique.md step 5)
```

Also copy `skill/SKILL.md` and the 5 most relevant references (`critique.md`, `audit.md`, `polish.md`, `bolder.md`, `typography.md`) into `.claude/skills/impeccable/` so Claude can invoke `/impeccable critique components/ready-to-buy-tile.tsx` in-session.

### 2. **Install `nexu-io/open-design`'s 4 dashboard-relevant skills via sparse-checkout**

Specifically: `dashboard`, `finance-report`, `trading-analysis-dashboard-template`, `critique`. Plus copy `design-systems/editorial/DESIGN.md` as our register starting point (it's already JPM-ish: Gelasio serif + Ubuntu Mono for numerals + 8pt grid + #111111 primary). The `dashboard` skill's **"inline SVG only, no JS chart libs"** rule + the `trading-analysis-dashboard-template`'s working `assets/template.html` (with hover crosshair + click-to-focus floating chart + command palette) are the direct fix for the default-Recharts FairTrajectoryChart problem.

```bash
# Sparse checkout (~5MB instead of full 134MB):
git clone --filter=blob:none --sparse https://github.com/nexu-io/open-design.git /tmp/od
cd /tmp/od
git sparse-checkout set skills/dashboard skills/finance-report skills/trading-analysis-dashboard-template skills/critique skills/tweaks design-systems/editorial design-systems/clickhouse design-systems/linear-app design-systems/cohere
mkdir -p C:\Users\paidu\investment-intelligence\.claude\skills\open-design
cp -r skills/dashboard skills/finance-report skills/trading-analysis-dashboard-template skills/critique skills/tweaks C:\Users\paidu\investment-intelligence\.claude\skills\open-design\
cp -r design-systems C:\Users\paidu\investment-intelligence\obsidian_vault\skills\open-design-systems
```

### 3. **Install `Leonxlnx/taste-skill`'s `redesign-existing-projects` skill**

This is the targeted-redesign variant — its 6-step Fix Priority is exactly our situation (existing component, can't rewrite from scratch, must work with Tailwind already in place):

> Fix in this order: 1) Font swap → 2) Color cleanup → 3) Hover/active states → 4) Layout/spacing → 5) Replace generic components → 6) Loading/empty/error states → 7) Polish typography scale.

The detailed Audit checklist hits all three of our components: "Generic card look (border + shadow + white background)" / "More than one accent color" / "Pill-shaped New/Beta badges" / "Numbers in proportional font" / "All-caps subheaders everywhere" / "Mathematical alignment that looks optically wrong" / "Buttons not bottom-aligned in card groups".

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "redesign-existing-projects"
# Then in next session: "use the redesign-existing-projects skill to audit and fix
# mission-control/components/ready-to-buy-tile.tsx"
```

---

## Concrete next-step commands (post-install)

```bash
# 1. Run impeccable detector on the 3 slop components and dump JSON
cd mission-control
npx impeccable --json components/ready-to-buy-tile.tsx components/fair-trajectory-chart.tsx components/consensus-panel.tsx | tee ../obsidian_vault/Bibliotheca/Impeccable_2026-05-08.json

# 2. Live-inject the impeccable overlay on localhost:3000
npx impeccable live &
# (then in a Claude Code session): "inject http://localhost:<port>/detect.js and read the [impeccable] console messages for the home page, ticker page, and alerts page"

# 3. Run open-design's 5-dim critique on each component (would-be CLI):
# Currently no CLI; invoke as in-conversation skill:
#   /critique components/ready-to-buy-tile.tsx
#   /critique components/fair-trajectory-chart.tsx
#   /critique components/consensus-panel.tsx

# 4. Replace fair-trajectory-chart.tsx default Recharts with inline SVG line+area
#    using the open-design/dashboard skill template; commit as separate spike:
git checkout -b spike/inline-svg-trajectory
# (then in session): "redesign components/fair-trajectory-chart.tsx using the
# open-design dashboard skill — inline SVG only, no Recharts, accent at most
# twice, axis labels + units + legend mandatory; preserve the API contract"

# 5. Adopt design-systems/editorial as the new register baseline (serif + mono numerals)
#    by copying its DESIGN.md into mission-control/DESIGN.md and refactoring
#    components/ready-to-buy-tile.tsx to use its tokens; v0 draft first.
```

---

## Closing notes

- **All 5 repos are MIT/Apache-licensed** — safe to copy SKILL.md content into `.claude/skills/` directly. Keep upstream attribution in a NOTICE comment at the top of each copied file.
- The **three biggest patterns** that cut across all 5 repos and apply to our slop:
  1. **Spec-first / DESIGN.md before code** (web-design + impeccable + garden-skills + open-design's design-systems) — we have a `DESIGN.md` philosophy in vault but no machine-readable token spec.
  2. **The Forbidden List as a literal artifact** (taste-skill + impeccable + garden-skills) — emoji bans, font bans, hero-metric-template bans, side-stripe-border bans, gradient-text bans. Copy verbatim into our `obsidian_vault/skills/Anti_Slop_Forbidden.md`.
  3. **Run two separate critiques + cite evidence per finding** (impeccable + open-design/critique) — kills the model anchoring its critique to the design it just wrote.
- After the 3 installs above, we can do a 90-minute spike to rebuild `fair-trajectory-chart.tsx` from inline SVG + open-design dashboard tokens + impeccable typography rules, and use `/critique` + `npx impeccable --json` to gate the result before merge.
