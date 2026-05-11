# Design Research — Web Reference Pack for Mission Control v5

> Generated 2026-05-08. Targeted research to fix three components flagged as
> "very bad / classic AI slop": **FairTrajectoryChart**, **ConsensusPanel**,
> **ReadyToBuyTile**. Project tone is JPM-inspired (Navy/Graphite/Gold/Ivory)
> with WSJ-style chart discipline.
>
> Bias: extract concrete patterns (specific hex values, font sizes, layout
> rules) over abstract design philosophy. Anchored on editorial finance
> (FT/WSJ/Bloomberg/Economist) and modern fintech product (Stripe/Linear/Fey).

---

## § Sources visited (canonical reference table)

| # | Source | What they do well | URL |
|---|---|---|---|
| 1 | FT Chart Doctor / Visual Vocabulary | Categorical taxonomy of chart types; line-chart guidance "axes don't always start at zero"; range plots for ranking | https://github.com/Financial-Times/chart-doctor |
| 2 | FT graphics-style-guide | Editorial discipline: graphics must induce thought about substance, not methodology | https://github.com/Financial-Times/graphics-style-guide |
| 3 | FT o-colors npm package | Canonical FT color tokens (claret, oxford, slate, mascarpone, paper) | https://www.npmjs.com/package/@financial-times/o-colors |
| 4 | FT brand pink #FFF1E0 | Salmon/bisque page background — instantly recognisable, low-contrast for serious reading | https://www.brandcolorcode.com/financial-times |
| 5 | WSJ Guide to Information Graphics (Dona Wong) | Y-axis natural increments (1/2/5/10/20/50/100); type describes, never decorates | https://www.ataccama.com/blog/top-10-takeaways-from-wsj-guide-to-information-graphics |
| 6 | WSJ Fonts (Escrow / Exchange / Retina) | Three-font system: Escrow display serif, Exchange text serif (slab + Bell Gothic DNA), Retina UI sans optimised for tiny sizes | https://mattstromawn.com/writing/wsjfonts/ |
| 7 | Bloomberg Terminal color accessibility post | Amber as base (#F39F41), blue/red reserved for semantic deltas, density-first | https://www.bloomberg.com/ux/2021/10/14/designing-the-terminal-for-color-accessibility/ |
| 8 | Bloomberg color palette ref | #000000 / #F39F41 amber / #FF433D red / #0068FF blue / #4AF6C3 mint | https://www.color-hex.com/color-palette/111776 |
| 9 | Stripe Elements Appearance API | Token contract: `colorPrimary` `colorBackground` `colorText` `colorDanger` `borderRadius` `fontFamily` | https://docs.stripe.com/elements/appearance-api |
| 10 | Stripe accessible color systems | LCH-style perceptual uniformity; "any two colors at least 5 levels apart pass WCAG"; #0A2540 / #F6F9FC / #635BFF brand | https://stripe.com/blog/accessible-color-systems |
| 11 | Linear redesign part II | LCH color space; reduced 98 theme vars to 3 (base/accent/contrast); Inter Display headings + Inter body; alignment is felt not seen | https://linear.app/now/how-we-redesigned-the-linear-ui |
| 12 | Robinhood design story | White background market-open / black market-closed; bold typography for hierarchy; red-green semantic only | https://medium.com/canvs/robinhood-5-reasons-the-stock-trading-app-has-cracked-application-design-2e2c727f0735 |
| 13 | Fey app (now Wealthsimple) | "Masterfully-crafted pocket watch" — every interaction, animation, color choice obsessed-over | https://nicelydone.club/apps/fey |
| 14 | Datawrapper — fonts for data viz | Recommend Roboto/Lato/Source Sans Pro (all ship lining + tabular figs); min 12px; avoid thin weights; bold only for titles | https://www.datawrapper.de/blog/fonts-for-data-visualization/ |
| 15 | Datawrapper — text in data viz | Annotations near elements; left-align text; never center; use color/weight for hierarchy not size alone | https://www.datawrapper.de/blog/text-in-data-visualizations |
| 16 | Datawrapper — y-axis fixes | Custom ticks (e.g. only 2015/2020/2025); right-align Y when chart benefits | https://blog.datawrapper.de/fix-my-chart-y-axis/ |
| 17 | Datawrapper — line chart customizing | Multi-line direct labelling > legend; thick lines for foreground series, thin grey for context | https://academy.datawrapper.de/article/47-customizing-your-line-chart |
| 18 | Datawrapper — range plot academy | Dot+line range plot for showing min/max/median across categories — prime model for ConsensusPanel | https://academy.datawrapper.de/article/126-customizing-your-range-plot |
| 19 | Tufte — sparkline theory & practice | Word-sized graphics; 5:1 aspect ratio for financial; gray normal-range bands; rightmost point highlighted in red/blue | https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/ |
| 20 | Tufte — data-ink ratio | Maximize data-ink, erase non-data-ink, erase redundant data-ink — applies to grids, tooltips, legends | https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/ |
| 21 | Cole Knaflic — Storytelling with Data | Annotation explains the "why"; title carries the message; visual hierarchy via color saturation not size | https://wuyaheng.github.io/Takeaways-from-Storytelling-with-Data/ |
| 22 | Stephen Few — Information Dashboard Design | 10/80/10 hierarchy (10% strategic, 80% operational, 10% drilldown); context + comparison required | https://public.magendanz.com/Temp/Information%20Dashboard%20Design.pdf |
| 23 | font-variant-numeric: tabular-nums | OpenType `tnum` aligns digit columns; `lnum` lining figures; both required for serious finance UI | https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric |
| 24 | Söhne / Klim Type Foundry usage | Stripe's commissioned sans — Akzidenz-Grotesk DNA filtered through Helvetica; "the most-copied fintech typeface" | https://typ.io/fonts/sohne |
| 25 | "AI slop" critique (925 Studios) | Telltale slop: purple gradients, Inter-on-everything, 16px rounded cards everywhere, gradient blobs, three-up icon grids | https://www.925studios.co/blog/ai-slop-web-design-guide |
| 26 | Okabe-Ito / Paul Tol palettes | Color-blind safe categorical: blue + orange is the safest 2-hue pair; max 8 distinguishable colors | https://thenode.biologists.com/data-visualization-with-flying-colors/research/ |
| 27 | Datawrapper — colors for vis style guides | Keep palette < 8 hues; use one accent + neutrals + sparing red/green for semantic | https://www.datawrapper.de/blog/colors-for-data-vis-style-guides |
| 28 | Visible Alpha consensus product | Bottom-up consensus from analyst models; comparison tables identify anomalies → ConsensusPanel must surface dispersion not just median | https://visiblealpha.com/products/corporate-insights/ |

---

## § FairTrajectoryChart — 5 references with adoption notes

Current: default Recharts, thin line, generic tooltip, period tabs at top, KPI strip with arrows.

| # | Reference | What to copy | Concrete adoption note |
|---|---|---|---|
| 1 | **FT line chart pattern** (Visual Vocabulary §line) | Direct labelling of lines at the right end (no legend); thicker line for primary series, hairline for context series | Drop the Recharts `<Legend>`. Render labels at `x = lastPoint.x + 4px`, color-matched to line. our_fair gets primary weight (1.5px), fair_price gets secondary (1px), current_price = filled circle marker only at the latest date. |
| 2 | **Tufte sparkline aspect** (financial 5:1) | Wide-and-short ratio for time series; gray normal-range band | Set chart container `aspect-ratio: 5/1` (or min 4:1). Add a faint band (`rgba(grey, 0.08)`) between min/max of our_fair across the period as a "fair range" backdrop — instantly conveys that the line is anchored, not floating. |
| 3 | **Robinhood "market open / closed" ambient color** | Subtle background tint signals state without UI chrome | Tint the chart background a *very* faint Ivory `#FAF8F2` (FT-adjacent) when the trajectory is BUY-rated, faint Graphite when AVOID. Zero borders. Replaces the period-tab visual weight at top. |
| 4 | **Datawrapper line-chart axis treatment** (right-align Y, custom ticks) | Right-align Y axis; show 4-5 ticks max with chosen years (e.g. 2021/23/25/27); no horizontal grid | Set `tickCount={4}`, `orientation="right"`, `axisLine={false}`, `tickLine={false}`. Pure typographic axis — numeric labels float to the right of the plot area in JetBrains Mono with `tabular-nums`. |
| 5 | **WSJ "natural increments"** (Wong, p.49) | Y-axis ticks must be 1/2/5/10/20/50/100/etc — never $13.42 / $26.84 / $40.26 | Round Y-domain UP to nearest natural increment. e.g. price range $42–$87 → ticks at $40/$50/$60/$70/$80/$90. Don't trust Recharts default; write a `niceTicks(min, max)` helper. |

**Concrete CSS/JSX deltas to apply**:
```css
.trajectory-chart { aspect-ratio: 5 / 1.2; background: var(--ivory-faint); }
.trajectory-chart .recharts-cartesian-grid { display: none; }
.trajectory-chart text { font: 11px/1 'JetBrains Mono', monospace; font-feature-settings: 'tnum' 1, 'lnum' 1; fill: var(--graphite-60); }
.trajectory-chart .our-fair-line { stroke: var(--navy); stroke-width: 1.5; }
.trajectory-chart .consensus-line { stroke: var(--graphite-40); stroke-width: 1; stroke-dasharray: 0; }
.trajectory-chart .price-marker { fill: var(--gold); r: 4; }
```

Kill list for this component: KPI arrow strip (move to caption sentence under chart), period tabs at top (replace with hairline buttons aligned right of chart title), grid lines (gone), tooltip box (replace with crosshair + floating value at line end), method-name footer (move to small caps `‹ method ›` after caption).

---

## § ConsensusPanel — 5 references with adoption notes

Current: 4-col table (Source / Target / Stance / Idade), our_fair row highlighted, footer with median/weighted/dispersion/upside.

| # | Reference | What to copy | Concrete adoption note |
|---|---|---|---|
| 1 | **Datawrapper range plot** (academy/article/126) | Each row gets a horizontal strip showing target on a price axis — visual position > numeric column | Replace `Target` column with a 200px-wide micro-strip per row: background = sector low/high range, dot = that broker's target, x-position scaled to `(target − min) / (max − min)`. Numeric value sits to the right of the strip in tabular mono. |
| 2 | **FT slope/range table** (Chart Doctor "comparing magnitude") | Show median as a vertical reference line across all rows, not as a separate footer | Render `median` as a 1px Gold vertical rule that crosses every row at the same x-position. our_fair's dot becomes a Navy diamond instead of a circle to differentiate without needing a `bg-overlay`. |
| 3 | **Tufte "small multiples" stacking** | Same scale + same chart type repeated for instant pattern recognition | Each row's micro-strip uses the SAME x-domain (locked to all-broker min/max). Reader's eye sweeps top-to-bottom and instantly sees who's bullish/bearish — table becomes a dot plot disguised as a list. |
| 4 | **Bloomberg amber-on-black semantic restraint** | Color reserved for delta meaning, not row identity | Drop the `bg-overlay` highlight on our_fair row. Instead: our_fair label gets a `‹nossa›` mono prefix in Gold and the diamond marker. All other rows: pure Graphite. Stance column: only colored when `STRONG_BUY` (Gold dot) or `SELL` (red text) — `BUY/HOLD/NEUTRAL` stays neutral. |
| 5 | **Stripe Elements appearance tokens** | Single set of tokens (colorBackground/colorText/colorPrimary) applied consistently | Define `--consensus-row-h: 28px; --consensus-divider: rgba(0,0,0,0.06);` and use 1px hairline dividers ONLY between rows — no card border, no zebra stripe, no background. Stripe's `Black Squeeze #F6F9FC` or our Ivory does the job. |

**Footer redesign**: replace 4-stat strip with a single sentence in editorial style:
> *Median target $58.40 • our_fair $54.20 • 9 estimates dispersion 12% • upside +4.2% from $52.10*
>
> Set as `font: 13px/1.5 'Inter', sans-serif; color: var(--graphite-70); font-feature-settings: 'tnum';` — single line, no boxes.

Kill list: per-cell padding boxes, age-column (move to a tiny `· 14d` mono suffix on each row), the "highlight overlay row" treatment.

---

## § ReadyToBuyTile — 5 references with adoption notes

Current: simple striped table, action pills (STRONG_BUY solid green / BUY outlined), columns Ticker/Action/Price/our_fair/Upside/Confidence.

| # | Reference | What to copy | Concrete adoption note |
|---|---|---|---|
| 1 | **Linear table density + alignment** | Tighter row height (28-32px), no zebra stripe, hover-only emphasis | `row-height: 28px;` + `border-bottom: 1px solid rgba(0,0,0,0.04);` between rows. NO background alternation. Hover: `background: var(--gold-tint-04)` only. Inter Display 11px for ticker, JetBrains Mono 12px for numerics. |
| 2 | **WSJ market table treatment** | Right-align all numerics with tabular-nums; ticker bold left-aligned; no per-cell borders | `td.numeric { text-align: right; font: 12px 'JetBrains Mono'; font-variant-numeric: tabular-nums; }`. Ticker column gets Inter Display 600 weight. Action column squeezed to fit. |
| 3 | **Robinhood semantic color** (red/green only for direction) | Color reserved for up/down; brand color reserved for action affordance | Upside column: `color: var(--green-700)` if positive, `var(--graphite-70)` if neutral, `var(--red-600)` if negative. Action pill: STRONG_BUY = Gold solid (no green), BUY = Gold outline. Removes the generic-fintech "green pill" look. |
| 4 | **Stephen Few — context for KPI** | Every metric needs comparison context to mean anything | Confidence column: instead of "78%" alone, render as a 40px-wide horizontal progress strip + value. Reader sees the bar fill against an implicit 100% — Few's "without context, you can't tell good from bad". |
| 5 | **FT salmon-page hierarchy** | Tile lives on a tinted background that signals editorial vs raw data | Wrap the tile in `background: var(--ivory) /* #FAF8F2 */; border: none; padding: 24px 0;` with a Playfair Display "Ready to buy" title at 22px and a thin Gold rule under the title. The tile reads like a curated section, not a database export. |

**Action pill redesign**:
```css
.pill-strong-buy {
  background: var(--gold-700); /* JPM gold #B8860B-adjacent */
  color: var(--ivory);
  font: 600 10px/1.6 'Inter', sans-serif;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 2px; /* 2px not 12px — slop tax */
}
.pill-buy {
  background: transparent;
  color: var(--gold-700);
  border: 1px solid var(--gold-700);
  /* same other props */
}
```

Kill list: zebra striping, generic green for BUY (use brand Gold), 12px+ rounded pills (2px max), per-row dividers heavier than 1px, the word "Confidence" as a column header (use `Conv` or icon).

---

## § Typography rules — 5 concrete pairings to try

| Slot | Font (primary) | Fallback chain | Size / Weight | Notes |
|---|---|---|---|---|
| 1. Editorial headline (page H1, tile title) | **Playfair Display** | `'Playfair Display', 'Tiempos Headline', Georgia, serif` | 32px / 700 — H1; 22px / 600 — tile title | Already in app. Keep; restrict to first H on each page only. Anything sub-section uses Inter Display. |
| 2. UI sans (labels, body, table headers) | **Inter** + **Inter Display** for headers ≥ 18px | `'Inter', 'Söhne', system-ui, sans-serif` | 13px/1.5 body; 11px/1.2 table headers; 22px/600 panel title | Per Linear: Inter for body, Inter Display for expressive headers. Body color `--graphite-80`, headers `--graphite-100`. |
| 3. Numeric / tabular (all financial values) | **JetBrains Mono** | `'JetBrains Mono', 'IBM Plex Mono', 'SF Mono', monospace` | 12px/1.4 in tables; 14px/1.4 in KPI strips | MUST set `font-variant-numeric: tabular-nums lining-nums;` on the column or container. Without `tnum`, columns wobble. |
| 4. Caption / method footer / annotation | **Inter** small caps | `'Inter', sans-serif` | 10px/1.4 weight 500, `letter-spacing: 0.06em; text-transform: uppercase;` | Replaces the boxy `‹ method: filings_grounded ›` with a typographic caption. Color `--graphite-60`. |
| 5. Inline mono accent (tickers, file paths) | **JetBrains Mono** | `'JetBrains Mono', monospace` | 11px/1 weight 500 | Use for the 4-letter ticker symbol in tables, on tooltips, and in the editorial captions ("our_fair $58.40 · ACN +4.2%"). Anchors the eye. |

**Universal CSS reset for finance UI**:
```css
:root { --tabular: 'tnum' 1, 'lnum' 1, 'ss01' 1; }
table, .num, .price, .pct, .ratio { font-feature-settings: var(--tabular); }
table { font-variant-numeric: tabular-nums lining-nums; }
```

---

## § Color palette ideas — extracted hex codes

### From FT (editorial-finance reference)
| Token | Hex | Use |
|---|---|---|
| FT paper (salmon) | `#FFF1E0` | Page-level wash for serious editorial sections; very low saturation lets numbers pop |
| FT claret | `#990F3D` | Reserved for negative deltas / SELL accents (replaces generic red) |
| FT oxford | `#0F5499` | Trust / positive editorial — pairs well with our Navy |
| FT slate | `#262A33` | Body text on light backgrounds — slightly warmer than pure black |
| FT mascarpone | `#F2DFCE` | Subtle row tint alternative to zebra |
| FT teal | `#0D7680` | Categorical accent #2 in multi-series charts |

### From Bloomberg (data-density reference)
| Token | Hex | Use |
|---|---|---|
| Black | `#000000` | True black for max-density terminals only — NOT our Ivory home |
| Amber base | `#F39F41` | Inspiration only — we'd map this to our Gold accent |
| Bloomberg blue | `#0068FF` | Positive delta semantic |
| Bloomberg red | `#FF433D` | Negative delta semantic |
| Bloomberg mint | `#4AF6C3` | Highlight / hover; only ever as 1-2px accent |

### From Stripe (modern fintech reference)
| Token | Hex | Use |
|---|---|---|
| Downriver navy | `#0A2540` | Almost identical to our JPM Navy — confirms direction |
| Black Squeeze | `#F6F9FC` | Near-white card surface — alternative to our Ivory for pure-data contexts |
| Cornflower | `#635BFF` | Stripe's brand purple — DO NOT ADOPT (purple is the AI-slop tell) |
| Stripe primary CTA | `#0570DE` | Saturated blue for primary action — we'd use Gold instead to differentiate |
| Stripe text | `#30313D` | Warm near-black for body — softer than pure black |

### Suggested Mission Control v5 palette (synthesized)
| Token | Hex | Role |
|---|---|---|
| `--navy-900` | `#0A2540` | Primary brand (Stripe-validated) |
| `--navy-700` | `#1A3A5C` | Hover / depth |
| `--gold-700` | `#B07D2B` | Action color (replaces all green BUY pills) |
| `--gold-400` | `#D4A85A` | Tints for STRONG_BUY accents |
| `--gold-tint-04` | `#B07D2B0A` | 4%-alpha hover wash |
| `--graphite-100` | `#1F2328` | Headers (warmer than #000) |
| `--graphite-80` | `#3A4048` | Body text |
| `--graphite-60` | `#6B7280` | Captions, muted labels |
| `--graphite-40` | `#A0A8B0` | Hairline / context-series chart lines |
| `--ivory` | `#FAF8F2` | Page wash on editorial sections |
| `--ivory-faint` | `#FDFCF6` | Chart background tint |
| `--green-700` | `#0D7C4A` | Positive delta only (NOT for affordances) |
| `--red-600` | `#990F3D` | Negative delta (FT claret) |
| `--divider` | `rgba(15,30,45,0.06)` | All horizontal rules between rows |

Rule: any hue NOT in this list does not appear in the UI. Period.

---

## § 3 chart-design patterns from Tufte / Datawrapper directly applicable

### Pattern A — Gray normal-range band behind the line (Tufte sparklines)
For FairTrajectoryChart: render a faint `rgba(31,35,40,0.06)` filled band between (min our_fair, max our_fair) across the period. The line then "lives" within the band, signalling its anchor visually without a single label. Found in Tufte's medical glucose example — when the data point falls outside the band, the eye catches it instantly.

Implementation: add a `<ReferenceArea y1={ourFairMin} y2={ourFairMax} fill="rgba(31,35,40,0.06)" stroke="none" />` as the first child of the Recharts cartesian area.

### Pattern B — Direct labelling > legend (Datawrapper line-chart academy)
Eliminate the `<Legend>` component entirely. At the right edge of each line, render a small text label at `y = lastPoint.y, x = lastPoint.x + 6px`, weight 500, color-matched. The eye traces the line to the label without a legend round-trip. Datawrapper says this works because "place words explaining elements as close to those elements as possible". Effect: removes ~40px of vertical legend space and forces the chart to read like an editorial line, not a chart.

### Pattern C — Right-aligned Y axis with sparse natural ticks (Datawrapper + WSJ Wong)
Move Y-axis to right side (where the eye lands at end of line scan), show 4 ticks max at natural increments (1/2/5/10/20/50/100), strip axis line and tick lines, set tick text in JetBrains Mono with tabular-nums. The chart shifts from "engineering plot" to "newspaper graphic" with no other change. WSJ does this on every multi-period equity chart; it's the single highest-leverage move.

---

## § Anti-patterns observed — slop traps to avoid

Distilled from 925 Studios "AI Slop Web Design Guide", The Adpharm critique, and Slopless.design:

1. **Purple-blue gradients anywhere**. The `#635BFF → #4F46E5` Stripe-Vercel gradient is the single biggest tell. Mission Control uses zero gradients (Gold accent is solid, never gradient).
2. **16px everywhere border radius**. Slop default. Use 2px on pills, 4px on cards, 0px on tables. Anything 12px+ rounded-corner reads "AI generated".
3. **Three-up icon card grid for "features"**. Three identical glass-morphism cards with Lucide icons + 14px regular subtext = instant slop. Replace with editorial paragraph + inline metric callouts.
4. **Inter on absolutely everything**. Inter is correct for UI but boring as the only voice. Mix in Playfair Display for editorial moments, JetBrains Mono for numerics. Three-font system creates rhythm.
5. **Generic emerald-green BUY pills**. `bg-green-500 text-white rounded-xl px-3 py-1` is the Tailwind default that makes every BUY button look identical across every fintech ever. Use Gold instead — instant differentiation.
6. **Drop-shadow + glassmorphism + rounded-card stack**. `shadow-md backdrop-blur-sm rounded-2xl border` is the AI-slop signature. We use one hairline divider and zero shadows. Hierarchy via spacing + typography.
7. **Bento-box with random AI-illustration accents**. Hero asset is data, not decoration. No Midjourney abstract blobs.
8. **KPI cards with up/down arrow icons + delta percentage**. Trope. Replace with sentence: *"Up 4.2% from $52.10"* with the number set in JetBrains Mono.
9. **Recharts default tooltip box**. White rounded box with shadow appearing on hover is a Recharts/AI tell. Replace with a thin vertical crosshair line + value floating at the line's right edge.
10. **Zebra-striped tables**. Per Anthony Hobday + A List Apart — when row count is small (< 8) zebra adds noise without aiding scanning. Use 1px hairline dividers at 6% alpha instead.
11. **"Animated gradient blob" hero**. The hero of a serious investing tool is a number, not a generative animation.
12. **All-caps SaaS pills with `letter-spacing: 0.1em` on every label**. Reserve uppercase for true small-caps captions (≤11px), never on body labels.
13. **Centered text-blocks across wide containers**. Editorial finance is left-aligned, ragged-right. Center-aligned wide blocks read marketing-page, not Bloomberg.
14. **Soft pastel "chart palettes"** (#A78BFA / #F472B6 / #34D399 grouped). These map to no semantic meaning and are color-blind hostile. Use Okabe-Ito or our 3-hue palette.
15. **Generic "Confidence: 78%" with bar**. Slop unless the bar is contextual against a comparable baseline (peer median, historical own-average). Add the comparison or remove the bar.

---

## § If only 5 things, do these

In priority order for fastest visible "this isn't AI slop" win:

1. **Set `font-variant-numeric: tabular-nums lining-nums;` globally on every table cell, KPI value, chart axis, and tooltip number.** One CSS line. Single biggest "this is a serious finance product" signal you can ship today. Without it, columns wobble and the whole UI reads amateur.

2. **Kill all chart grids, tooltips boxes, and legends in FairTrajectoryChart.** Replace with: faint Ivory background, gray normal-range band behind the line (Tufte), direct end-of-line labels (Datawrapper), right-aligned Y-axis with 4 natural ticks (WSJ). The chart goes from "default Recharts" to "FT graphic" with zero new components.

3. **Recolor every BUY/STRONG_BUY pill from green to Gold (`#B07D2B`).** Generic emerald is the AI-slop tell. Gold is brand. Two-line CSS change. Side benefit: red/green stays reserved for direction (up/down deltas) per Robinhood + Bloomberg semantic discipline.

4. **Replace the ConsensusPanel `Target` column with a Datawrapper-style range plot.** Each row = a horizontal micro-strip with a dot positioned at the broker's target on a shared price axis, plus the numeric value to the right. Median = single Gold vertical rule across all rows. The component goes from "table" to "ranking visualization" — Visible Alpha-grade.

5. **Adopt the 3-font system everywhere: Playfair Display (display) + Inter / Inter Display (UI) + JetBrains Mono (numerics).** Forces rhythm, kills the "Inter on everything" slop signature. Combine with the palette restriction (Navy/Gold/Graphite/Ivory + 2 semantic deltas) and the visual identity locks in.

---

## Sources

- [FT Chart Doctor (GitHub)](https://github.com/Financial-Times/chart-doctor)
- [FT graphics-style-guide](https://github.com/Financial-Times/graphics-style-guide)
- [@financial-times/o-colors](https://www.npmjs.com/package/@financial-times/o-colors)
- [Why the Financial Times is pink (Quartz)](https://qz.com/462285/why-the-financial-times-is-pink)
- [WSJ Guide to Information Graphics — 10 Takeaways (Ataccama)](https://www.ataccama.com/blog/top-10-takeaways-from-wsj-guide-to-information-graphics)
- [WSJ Fonts: Escrow, Exchange & Retina (Matt Ström-Awn)](https://mattstromawn.com/writing/wsjfonts/)
- [Bloomberg — Designing the Terminal for Color Accessibility](https://www.bloomberg.com/ux/2021/10/14/designing-the-terminal-for-color-accessibility/)
- [Bloomberg color palette (color-hex)](https://www.color-hex.com/color-palette/111776)
- [Stripe Elements Appearance API](https://docs.stripe.com/elements/appearance-api)
- [Stripe — Designing Accessible Color Systems](https://stripe.com/blog/accessible-color-systems)
- [Linear — How we redesigned the Linear UI (Part II)](https://linear.app/now/how-we-redesigned-the-linear-ui)
- [Robinhood design story (Canvs / Medium)](https://medium.com/canvs/robinhood-5-reasons-the-stock-trading-app-has-cracked-application-design-2e2c727f0735)
- [Fey app UI screens (Nicely Done)](https://nicelydone.club/apps/fey)
- [Datawrapper — Fonts for data visualization](https://www.datawrapper.de/blog/fonts-for-data-visualization/)
- [Datawrapper — Text in data visualizations](https://www.datawrapper.de/blog/text-in-data-visualizations)
- [Datawrapper — Fix my chart: the y-axis](https://blog.datawrapper.de/fix-my-chart-y-axis/)
- [Datawrapper Academy — Customizing your line chart](https://academy.datawrapper.de/article/47-customizing-your-line-chart)
- [Datawrapper Academy — Customizing your range plot](https://academy.datawrapper.de/article/126-customizing-your-range-plot)
- [Tufte — Sparkline theory and practice](https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/)
- [Tufte's Principles (Doublethink)](https://thedoublethink.com/tuftes-principles-for-visualizing-quantitative-information/)
- [Storytelling with Data takeaways (Wuyaheng)](https://wuyaheng.github.io/Takeaways-from-Storytelling-with-Data/)
- [Stephen Few — Information Dashboard Design (PDF)](https://public.magendanz.com/Temp/Information%20Dashboard%20Design.pdf)
- [MDN — font-variant-numeric](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric)
- [Söhne in action (Typ.io)](https://typ.io/fonts/sohne)
- [925 Studios — AI Slop Web Design Guide (2026)](https://www.925studios.co/blog/ai-slop-web-design-guide)
- [Color-blind-friendly palettes (TheNode/Biologists)](https://thenode.biologists.com/data-visualization-with-flying-colors/research/)
- [Datawrapper — Colors for data vis style guides](https://www.datawrapper.de/blog/colors-for-data-vis-style-guides)
- [Visible Alpha — Corporate Insights](https://visiblealpha.com/products/corporate-insights/)
