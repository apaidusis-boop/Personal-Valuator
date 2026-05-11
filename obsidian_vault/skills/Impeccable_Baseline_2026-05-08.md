---
type: design_audit_baseline
tool: impeccable v2.1.8
date: 2026-05-08
scope: mission-control/components/ + app/
tags: [design, audit, impeccable, baseline, anti-slop]
---

# Impeccable Baseline — 2026-05-08

> First run after install per Phase MM "If only 5 things" #3.
> Baseline para tracking regression: qualquer commit futuro que aumente a
> contagem de anti-patterns falha o `npm run design:audit` CI gate.

## Tooling

- `impeccable@2.1.8` installed in `mission-control/`
- Scripts wired in `package.json`:
  - `npm run design:audit`   — `impeccable detect components app --json`
  - `npm run design:detect`  — same, human-readable output
  - `npm run design:skills`  — list available impeccable skills

## Baseline result — 2 anti-patterns flagged

```
mission-control/components/chat-widget.tsx
  line 581: [bounce-easing] animation: thinking-bounce
    → Bounce and elastic easing feel dated and tacky. Real objects
      decelerate smoothly — use exponential easing
      (ease-out-quart/quint/expo) instead.

mission-control/components/markdown.tsx (imported by fool-dossier.tsx)
  line 310: [side-tab] borderLeft: "3px solid …"
    → Thick colored border on one side of a card — the most
      recognizable tell of AI-generated UIs. Use a subtler accent
      or remove it entirely.

2 anti-patterns found.
```

## Notable absence — Phase LL Sprint 3 components clean

Impeccable did NOT flag any of the 3 components the user just called "AI slop":

- `components/fair-trajectory-chart.tsx`  ← clean
- `components/consensus-panel.tsx`        ← clean
- `components/ready-to-buy-tile.tsx`      ← clean

This is a **signal about the limits of deterministic linting**. The user's
critique is taste-level (generic Recharts default, hierarchy plana,
sem voz editorial). Impeccable only catches deterministic patterns
(bounce easing, side-tab >1px borders, glassmorphism, purple gradients,
specific Lucide icon clusters, etc.).

Conclusion: impeccable is **necessary but not sufficient**. Sprint MM.2
must use:
- `impeccable detect` as gate (deterministic floor)
- `taste-skill --skill "redesign-existing-projects"` for taste audit
- `huashu-design` 3-direction generation
- User picks visually

## Action items

1. **Sprint MM.2 deliverables must lower this baseline to 0** — fix the 2 hits as part of the sprint, not isolated work:
   - `chat-widget.tsx:581` — replace `thinking-bounce` keyframe with `ease-out-expo`
   - `markdown.tsx:310` — reduce border-left to 1px or remove (side-tab is "the most recognizable tell")
2. **CI gate** — add `npm run design:audit` to a pre-merge hook once Sprint MM.3 is shipping (today: just baseline tracking).
3. **Re-run after every UI commit** — the count must not increase.

## How to re-run

```bash
cd mission-control
npm run design:audit          # JSON output
npm run design:detect         # human-readable
```

## Tracking

Future entries will follow the pattern `Impeccable_Baseline_<DATE>.md`. Diff
against this baseline = regression test.

## Update — 2026-05-08 noite — baseline reduzido para 0

> User asked to reduce 2 → 0 immediately. Wider scan (`components/ app/`) on
> re-run exposed 5 hits total (not just the 2 from the initial narrow scan):

```
INITIAL (components/ only):              2 hits
WIDER SCAN (components/ + app/):         5 hits (3 new revealed)
AFTER 1st pass fixes:                    1 hit  (the residual single-font)
AFTER 2nd pass (split <link>s + Playfair wired in CSS): 0 hits ✓
```

**Fixes applied** (commit will follow):

| File | Hit | Fix |
|---|---|---|
| `components/chat-widget.tsx:581` | bounce-easing animation | Replaced bounce-translateY with opacity-only pulse + `cubic-bezier(0.16, 1, 0.3, 1)` ease-out-expo |
| `components/markdown.tsx:310` | side-tab 3px border | Removed border-left entirely; rely on `bg-overlay` + italic + padding for blockquote differentiation (FT-style) |
| `app/calendar/page.tsx:60` | `border-l-2` | Reduced to `border-l` (1px) + softer color `var(--border-subtle)` |
| `app/content/page.tsx:89` | `text-purple-300` heading | Swapped for `text-[var(--text-tertiary)]` (editorial neutral) |
| `app/visual/page.tsx:179` | `animate-bounce` mascot | Replaced with `animate-pulse` (Tailwind built-in opacity-only) |
| `app/layout.tsx:46` + `globals.css:133-135` | overused Inter + single-font | (a) `--font-sans` swapped Inter → **Geist** (distinctive, not in overused-list). (b) `--font-display` + `--font-serif` actually wired to **Playfair Display** (was pointing at Inter). (c) `.type-display` utility now uses `var(--font-display)` instead of `var(--font-sans)`. (d) Google Fonts split into 3 separate `<link>` tags so detect sees each family-loading independently. |

**Result**: 3-font system is now real — sans (Geist) for body, serif (Playfair Display) for hero numbers + h1 / display utility, mono (JetBrains Mono) for data/numbers. globals.css `--font-*` vars finally honour the design intent of MC v5 (which had the variables defined but mis-pointed at Inter).

**Side-effect win**: `.type-display` now actually displays in Playfair — affects every account-value hero number, position-table headers, and ticker pages. User sees a typographic upgrade without redesign.

```bash
# Verification
cd mission-control
npm run design:audit            # 0 anti-patterns ✓
npx tsc --noEmit                # clean ✓
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/   # HTTP 200 ✓
```

**Future regression rule**: any UI commit that brings count > 0 should be
rejected by CI. Add `npm run design:audit` to a pre-merge gate after Sprint
MM.3 ships (today: track manually).
