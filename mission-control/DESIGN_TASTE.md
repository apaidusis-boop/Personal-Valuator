---
type: design_taste_journal
tags: [design, taste, mission-control, broadsheet, journal]
created: 2026-05-06
updated: 2026-05-06
inspired_by: gstack/design-taste-update (decay model removed — manual curation here)
---

# 🎨 Mission Control — Design Taste Journal

> **Purpose**: a lightweight preference journal recording UI decisions that have been **approved + ratified** by the founder. Reference at the start of every UI sprint to prevent drift.
>
> Pattern borrowed (without tooling) from `garrytan/gstack`'s `/design-taste-update` skill — there it is a 5%/week-decay model fed by build cycles. Here it's curated by hand: each entry is a deliberate ratification, no auto-decay.

---

## 🟣 v3 Broadsheet (current direction)

Approved 2026-05-05. Reference: [[../obsidian_vault/skills/Mission_Control_Design_Roadmap]] + memory entry `design_v3_broadsheet_roadmap.md`. Sprint 1 shipped (FT/WSJ tokens + light/dark + 11 components refactored).

### Typography
- **Display / hero**: serif (FT-style). Only on top-of-fold; no body serif.
- **Body**: system sans (`-apple-system`, `Segoe UI`, etc.). Default 14px, line-height 1.55.
- **Tabular numbers**: `font-variant-numeric: tabular-nums` on every price/percentage cell — non-negotiable.
- **Anti-drift**: never introduce a third typeface. If a third is needed, it replaces sans, not augments.

### Colour
- **Dark theme palette**: `#0f1115` (background), `#1a1d24` (surface 1), `#252a33` (surface 2), `#e8eaed` (text high), `#9aa0a6` (text mid), `#5f6368` (text low).
- **Accent (purple)**: `#7c5cff` — primary action, brand mark, hover states. **≤20% of coloured surfaces.**
- **Accent (cyan)**: `#5ce0ff` — data positives, fresh signals, info banners. **≤10%.**
- **Semantic**: green `#4ade80` (BUY/up), red `#f87171` (AVOID/down), amber `#fbbf24` (HOLD/warn).
- **Borrowed from anthropic/skills frontend-design (2026-05-06)**: *dominant colour + sharp accent outperform timid evenly-distributed palettes*. v3 enforces this — neutral surfaces dominate, accent is a punctuation, not a fill.
- **Anti-drift**: no gradient mesh on KPI cards (reads as decorative); gradients OK on hero only.

### Spacing
- **Grid**: 8pt. Components use multiples (8, 16, 24, 40, 64).
- **Rhythm**: vertical rhythm 24px between major sections; 16px within section; 8px within compound widget.
- **Anti-drift**: never use 6, 10, 14, 18, 20px. They feel arbitrary because they are arbitrary.

### Layout
- **Asymmetric splits encouraged**: `grid-template-columns: 2fr 1fr` over `1fr 1fr` for any pane that has a primary + secondary signal. Equal splits are the default-of-no-thought.
- **Borrowed from anthropic/skills frontend-design (2026-05-06)**: spatial composition is intentional; absence of proportion is a violation. DS010 (Helena audit) flags pages with all-equal columns.

### Motion
- **One orchestrated entrance** per page, max 600ms total, staggered children.
- **No scattered hover micro-interactions** — six bouncy hover effects feel cheap. One thoughtful focus state beats six.
- **Anti-drift**: motion budget is per-page, not per-component.

### Density
- Tables: 36px row height (compact-readable). 28px (compact-dense) reserved for screens shown to power users only.
- Cards: never less than 16px padding.

---

## 🚫 Rejected directions (don't re-litigate)

| Direction | Rejected on | Why |
|---|---|---|
| Light theme as default | 2026-04-29 | User preference dark-first; light is alternate |
| Glassmorphism / backdrop-blur on cards | 2026-04-29 | Tries-too-hard; reads as 2020 stylesheet |
| Animated KPI counters (0 → value) | 2026-05-01 | Looks juvenile; user wants Bloomberg Terminal not crypto-bro |
| Pie charts | 2026-04-26 (DS004) | Banned in Helena; never read accurately at small sizes |
| Emoji in section headings | 2026-04-26 (DS003) | Banned in Helena Escritório; OK in vault prose |

---

## 🔁 Update protocol

When a UI decision is ratified (commit lands + founder accepts):

1. Edit this file. Add the decision under the correct section.
2. If it conflicts with a "Rejected" entry, move that entry to a new "Reverted Rejections" sub-section with reason.
3. Reference this file at the top of every Mission Control PR description so design context travels with code.

---

## Source attributions

- Pattern: `garrytan/gstack` `/design-taste-update` (decay journal). Decay omitted — we re-litigate by hand.
- Palette + spatial heuristics: `anthropics/skills/frontend-design` (cherry-picked 2026-05-06).
- Token system + 9 DS rules: Helena Linha [[../obsidian_vault/skills/Design_System]].
- Sprint cadence: project's own [[../obsidian_vault/skills/Mission_Control_Design_Roadmap]].
