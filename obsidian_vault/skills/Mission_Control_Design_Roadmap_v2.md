---
type: roadmap
status: in_progress
last_updated: 2026-05-08
supersedes:
  - skills/Mission_Control_Design_Roadmap.md (v1 Broadsheet — superseded by MC v5 JPM)
tags: [roadmap, design, v2, anti-slop, helena]
---

# 🎨 Mission Control Design Roadmap v2 — anti-slop, taste-first

> **Trigger**: 2026-05-08 user critique sobre os 3 componentes Phase LL Sprint 3
> (FairTrajectoryChart, ConsensusPanel, ReadyToBuyTile) — *"looks very bad"* /
> classic AI slop. Princípio v2: **design specs antes de código, sempre**.

> Substitui [[Mission_Control_Design_Roadmap]] (v1 Broadsheet, ~830 linhas, ~110
> sources). v1 entregou os tokens FT/WSJ que ainda usamos; mas a metodologia
> "ship-fast .tsx" produziu slop. v2 inverte a ordem.

---

## 🚪 Voltamos — sintetizador de retomada

> Quando o user disser "voltamos design" ou "AI slop": ler esta secção primeiro.

**Estado**: Phase LL data foundation completa (16/33 holdings cross_validated,
SEC XBRL US + CVM filings BR + Fundamentus + fiis.com.br + 4-gate fair_value +
consensus blender + 3 dashboard endpoints + 3 React components shipped).

**Problema**: os 3 React components (FairTrajectoryChart, ConsensusPanel,
ReadyToBuyTile) são funcionalmente correctos mas visualmente genéricos. Tabelas
densas, Recharts default, hierarquia plana, sem voz editorial — *"AI slop"*.

**Solução**: research deep + adoption tier 1 skills + spec-first redesign dos 3
componentes via `huashu-design`. Não delete — refazer com taste.

---

## 📊 Baseline (state of play 2026-05-08)

### Tokens já estabelecidos (`mission-control/app/globals.css`)
JPM-clean palette decidida em MC v5 (commit `4a4b2b6`, 2026-05-07):

```css
--jpm-canvas:  #F4F6F8   /* page bg, cool grey */
--jpm-card:    #FFFFFF   /* card bg */
--jpm-overlay: #EEF1F5   /* sub-bg, chips */
--jpm-ink:     #0F1B2D   /* primary text */
--jpm-ink-3:   #5A6577   /* labels, captions */
--jpm-blue:    #0F62D1   /* action / link (Chase blue) */
--jpm-gain:    #15A861   /* positive deltas */
--jpm-loss:    #E5142D   /* negative deltas */
--jpm-amber:   #C77700   /* HOLD / warning */
--jpm-border:  #E1E4EA   /* hairlines */
--jpm-grid:    #ECEFF3   /* chart gridlines */
```

Tipografia: **Inter** (sans), **Playfair Display** (display/h1), **JetBrains Mono** (data/numbers).

**Decisão v2**: tokens permanecem. v2 ataca *como* os componentes usam estes tokens — hierarquia, voz editorial, restraint, density tradeoffs.

### Skills instaladas (`~/.claude/skills/`)
- `designer-skills`
- `huashu-design` — 5 streams × 20 design philosophies, anti-AI-slop guardrails
- `hue` — meta-skill que gera novas design languages
- `ui-ux-pro-max-skill` — 67 UI styles, 161 palettes, 57 font pairings searchable

### Os 3 componentes a redesenhar (não delete — refazer)
1. **`components/fair-trajectory-chart.tsx`** — Recharts line chart 5y de our_fair + consensus + price. Header KPI + period tabs + footer. *Mais slop-y dos três (Recharts genérico).*
2. **`components/consensus-panel.tsx`** — tabela houses (Nossa/Suno/XP/BTG/WS) com mediana footer. *Tabela densa, sem narrative voice.*
3. **`components/ready-to-buy-tile.tsx`** — tabela home page com action pills + confidence badges. *Pills genéricas, hierarquia plana, decision não em destaque.*

---

## 🔬 Research streams (em curso 2026-05-08)

> 3 sub-agentes paralelos lançados; secções abaixo populam quando completarem.

### A. GitHub deep-dive — top 3 install order

> Detalhe completo em [[Design_Research_GitHub_DeepDive]] (310 linhas).
> Confidence: HIGH — agent leu SKILL.md + reference files de cada repo,
> não só READMEs. Drilou nos próprios componentes slop para grounding.

**Tier 1 — install esta semana**:

1. **`pbakaus/impeccable`** (26k ★) — *the runnable detector*. NÃO é um prompt overlay; é uma harness com `npx impeccable --json` (CI gate) + `npx impeccable live` (browser overlay injector). Flag 27 anti-patterns determinísticos. Lista *"absolute bans"* nomeia exactamente os nossos casos:
   - "the hero-metric template" = `ReadyToBuyTile`
   - "side-stripe borders >1px"
   - "identical card grids"
   - "glassmorphism-as-default"
   ```bash
   # Adoption command (Sprint MM.1)
   npm install --save-dev impeccable
   # Wire into mission-control package.json scripts:
   #   "design:audit": "npx impeccable --json"
   #   "design:live":  "npx impeccable live"
   ```

2. **`nexu-io/open-design`** (33k ★) — *the content bank*. README under-sells: na verdade são **97 skills + 142 brand-grade design systems** (counted via API). Sparse-checkout só do que precisamos:
   ```bash
   git clone --depth=1 --filter=blob:none --sparse https://github.com/nexu-io/open-design
   cd open-design
   git sparse-checkout set \
     skills/dashboard \
     skills/finance-report \
     skills/trading-analysis-dashboard-template \
     skills/critique \
     skills/tweaks \
     skills/dcf-valuation \
     design-systems/editorial \
     design-systems/clickhouse \
     design-systems/linear-app \
     design-systems/cohere
   ```
   Killer feature: `dashboard` skill regra **"inline SVG only, no JS chart libraries"**. `trading-analysis-dashboard-template` traz `template.html` com hover crosshair + click-to-focus floating chart + command palette — directo fix do default-Recharts smell em `FairTrajectoryChart`. Design system `editorial` é JPM-adjacent (Gelasio serif + Ubuntu Mono numerals, 8pt grid).

3. **`Leonxlnx/taste-skill --skill "redesign-existing-projects"`** (16k ★) — *the closest-match-to-our-situation skill*. Não somos greenfield; estamos a re-fazer. 6-step Fix Priority + AI-tells lista mais copy-ready dos 3 repos:
   - NO Inter (sole sans), NO `#000000`
   - NO purple/blue gradients, NO Lucide-default icons
   - NO 3-equal cards, NO emoji-as-icons
   - NO "John Doe" placeholders, NO `99.99%` round numbers

**Tier 2 — adoptar process patterns (não código)**:

4. **`KAOPU-XiaoPu/web-design`** (301 ★) — *spec-first-code-second*. Adoptar o pattern: 9-section DESIGN.md como entregável **antes** do .tsx. L1/L2/L3 motion tier ladder. 100-point quality red lines. Já replicámos parcialmente em `obsidian_vault/specs/{component}.spec.md`.

5. **`ConardLi/garden-skills/web-design-engineer`** (2.7k ★) — *placeholder discipline*: "a placeholder is more professional than a poorly drawn fake; missing data → ASK USER, never fabricate". Mais 3 React+Babel non-negotiables. Adoptar como Helena DS010-DS012.

**90-min spike plan** (Agent 1 already drafted): rebuild `fair-trajectory-chart.tsx` as inline SVG using open-design dashboard tokens, gated by `npx impeccable --json` before merge. Comandos exactos no doc.

### B. YouTube channel curation — 12 canais validados

> Detalhe em [[../../config/yt_design_channels.yaml|config/yt_design_channels.yaml]].
> Cada `channel_id` validado live via `curl https://www.youtube.com/@<handle>` +
> RSS feed cross-check 2026-05-08.

**Cadence + cost**: 3 weekly · 7 monthly · 2 quarterly = ~80 vídeos/mês para Whisper local. Free.

**Tier S — ingest first** (3 canais que falam directamente do nosso problema):

| Canal | skill_target | Why |
|---|---|---|
| **Malewicz** | `design.dashboard` | Já escreveu *"The End of Dashboards and Design Systems"* — exact contrarian voice contra o failure mode que critique-aste hoje |
| **Tailwind Labs** | `design.systems` | YT proxy do *Refactoring UI* (Wathan + Schoger) — canonical anti-AI-slop manual |
| **Financial Times** | `design.dataviz` | FT Chart Doctor + visual journalism. Já listado em `youtube_sources.yaml` para news; aqui re-tagged para dataviz |

**Tier 1 — ingest após Tier S**:

| Canal | skill_target | Cadence |
|---|---|---|
| Linear | `design.dashboard` | quarterly (talks at scale) |
| The Pudding | `design.dataviz` | monthly |
| Storytelling with Data (Knaflic) | `design.dataviz` | monthly |
| Observable | `design.dataviz` | monthly |
| Vercel | `design.systems` | monthly (Vercel Ship + WWW Conf) |
| Figma | `design.scout` | quarterly (Config talks) |
| Smashing Magazine | `design.scout` | monthly |
| Kevin Powell | `design.css` | weekly |
| Bramus | `design.css` | weekly (note: `@bramus`, NOT older "Bramus Van Damme") |

**Rejeitados** (15+ documentados no YAML para Helena scout não re-suggest):
`@adamwathan` (subsumed), `@AaronIker` (Dribbble only), `@uxtools` (newsletter > YT),
`@DesignCourse` (Figma-clicking tutorials — exactly the filter), Bloomberg Originals
(documentary not instruction), Femke van Schoonhoven (career not editorial UI),
`@TheStudio`/DesignBetter (defunct).

**Adoption command (Sprint MM.4)**:
```bash
# Tier S first (~30 vídeos)
ii yt ingest --channel-last UCMalewiczHype --count 10
ii yt ingest --channel-last UCOe-8z68tgw9ioqVvYM4ddQ --count 10  # Tailwind Labs
ii yt ingest --channel-last UCoUxsWakJucWg46KW5RsvPw --count 10  # FT

# Then Tier 1 batch
python scripts/yt_ingest_batch.py --config config/yt_design_channels.yaml --tier 1
```

### C. Web/pattern library — 28 sources, 15 anti-patterns named

> Detalhe completo em [[Design_Research_Web]] (430 linhas, 28 refs).

**Anti-AI-slop signature** (named publicly, deterministic):
> *"Purple-blue gradients + Inter-on-everything + 16px-rounded-cards + glassmorphism stack + Lucide three-up cards"* → AI slop.
> Sources: 925 Studios, The Adpharm, Slopless.design, CSS-Tricks slop critiques 2024-2026.

Bom: o nosso JPM theme já evita gradients e glassmorphism. Mau: *Inter-on-everything* aplica-se (precisa diferenciar via 3-font system: Inter body, Playfair display, JetBrains Mono data).

**Color palette extracted** (hex codes diretamente do source):

| Source | Hex | Use |
|---|---|---|
| FT Claret | `#990F3D` | secondary accent (could replace --jpm-loss for editorial weight) |
| FT Oxford Blue | `#0F5499` | similar to JPM Blue (#0F62D1) — blends |
| FT Paper | `#FFF1E0` | warm cream alternative to canvas grey |
| FT Mascarpone | `#F2DFCE` | warm card alternative |
| Bloomberg Amber | `#F39F41` | gold/HOLD accent (better than current `--jpm-amber #C77700`) |
| Bloomberg Mint | `#4AF6C3` | gain accent for terminals (too saturated for our use) |
| Stripe Downriver | `#0A2540` | navy ≈ identical to our JPM ink #0F1B2D — direction confirmed |
| Stripe Black Squeeze | `#F6F9FC` | canvas ≈ identical to our --jpm-canvas #F4F6F8 — direction confirmed |

**Proposed v5 token additions** (não substituir actuais — adicionar):
```css
/* Editorial register tokens — for narrative pages (dossiers, council) */
--ed-paper:        #FFF1E0;     /* warm canvas */
--ed-mascarpone:   #F2DFCE;     /* warm card */
--ed-claret:       #990F3D;     /* editorial secondary */
--ed-oxford:       #0F5499;     /* editorial primary */

/* Action tokens — replace current generic green pills with gold */
--action-gold:     #F39F41;     /* BUY / STRONG_BUY (was emerald) */
--action-gold-soft: #FCF1DD;    /* tinted background */
```

**3 chart-design patterns directly applicable**:

| Pattern | Source | Apply to |
|---|---|---|
| **Gray normal-range band** (Tufte) — shaded zone for "normal" values, line crosses out only when abnormal | Edward Tufte sparkline theory | `FairTrajectoryChart` — banda sombreada entre our_fair e consensus_fair |
| **Direct end-of-line labelling** | Datawrapper academy | `FairTrajectoryChart` — substituir Recharts Legend por inline labels no end of each line |
| **Right-aligned Y axis with WSJ Wong rule (1/2/5/10/20/50/100)** | Dona Wong — WSJ Guide to Information Graphics | `FairTrajectoryChart` Y axis — substituir tick-formatter actual |

**Typography rules** (5 font-pair stacks, full fallback chains):
1. *Editorial register* — Playfair Display 700 (h1) / Inter 400 (body) / JetBrains Mono 400 (data)
2. *Dashboard register* — Inter 600 (labels) / Inter 400 (body) / JetBrains Mono 500 (numbers, `font-feature-settings: "tnum"`)
3. *Data-viz register* — Inter 500 (chart labels) / JetBrains Mono 400 (axis ticks)
4. *Hero numbers* — Playfair Display 800 italic (1-2 large numbers per page)
5. *Footnote register* — Inter 400 small (10-11px) com `tracking-wider uppercase`

**THE single CSS line** que separa serious finance UI de amateur:
```css
:root, body {
  font-variant-numeric: tabular-nums lining-nums;
}
```

(Confirmar se já está em `globals.css` — provavelmente não.)

**Range plot pattern** (Datawrapper):
- `ConsensusPanel` actual = tabela. Slop.
- Range plot = horizontal stacked points + connecting line, mostrando dispersion visualmente.
- Datawrapper academy tem template directo: <https://academy.datawrapper.de/article/126-customizing-your-range-plot>

**"If only 5 things, do these"** (Agent 3 priority):
1. Add `font-variant-numeric: tabular-nums` globally
2. Gut FairTrajectoryChart per Tufte+FT+WSJ (inline SVG, gray range band, direct labels)
3. Recolor BUY pills Gold (#F39F41) not emerald
4. ConsensusPanel → Datawrapper range plot
5. Adopt 3-font system (Playfair Display + Inter + JetBrains Mono)

---

### D. Convergent recommendations — onde os 3 streams concordam

> Sinal mais forte do research: quando GitHub + YouTube + Web independentemente
> chegam à mesma recomendação. Estas têm prioridade na adopção.

| # | Recomendação | GitHub | YouTube | Web |
|---|---|---|---|---|
| 1 | **Spec-first methodology** (DESIGN.md antes de .tsx) | ✅ web-design | ✅ Malewicz "End of Dashboards" essay | ✅ Datawrapper docs philosophy |
| 2 | **Inline SVG > default Recharts** para dashboards | ✅ open-design `dashboard` skill | ✅ The Pudding tutorials | ✅ FT Chart Doctor patterns |
| 3 | **Range plot** para `ConsensusPanel` | ✅ open-design templates | ✅ Storytelling with Data | ✅ Datawrapper academy |
| 4 | **Tufte sparkline 5:1** + WSJ Wong Y-axis | — | ✅ Observable + Knaflic | ✅ Tufte sparkline theory |
| 5 | **"Hero metric / 3-equal cards" = slop trap** | ✅ impeccable absolute bans | ✅ Refactoring UI (via Tailwind Labs) | ✅ 925 Studios slop guide |
| 6 | **Anti-AI-slop é determinístico + named** | ✅ taste-skill AI-tells list | ✅ Malewicz/Refactoring UI | ✅ 925 Studios + Slopless.design |
| 7 | **JPM Navy ≈ Stripe Downriver** — direction OK | — | — | ✅ Stripe Elements color extraction |
| 8 | **`font-variant-numeric: tabular-nums`** mandatory | ✅ taste-skill | ✅ Bramus CSS | ✅ Datawrapper + Practical Typography |

**Tensão a resolver** (apenas 1):
- Agent 1 (taste-skill): "NO Inter as sole sans"
- Agent 3 (FT/Datawrapper): "Inter is fine — combined with Playfair + JetBrains"
- **Resolução**: o problema é Inter-em-tudo, não Inter per se. Nosso 3-font system Playfair/Inter/JetBrains evita o trope. Manter.

---

## 🎯 Adoption philosophy (v2 non-negotiables)

> Estas regras existem para evitar repetir o erro de hoje. Aplicam-se a **todo
> trabalho de UI futuro**, não só a este sprint.

1. **Spec antes de código** — adoptado de `KAOPU-XiaoPu/web-design`. Para cada componente novo: escrever spec markdown (purpose, hierarchy, density, anti-patterns) **antes** de qualquer .tsx. Spec é committed à parte e revista pelo user.

2. **3 directions paralelas, user escolhe** — adoptado de `huashu-design`. Nunca shipar 1 design. Sempre 3 (Pentagram info-arch / Field.io motion / Kenya Hara minimal ou outras 3 streams). 24 showcases. User vê side-by-side e escolhe.

3. **Anti-slop checklist** — adoptado de `Leonxlnx/taste-skill` (a confirmar quando agent 1 voltar). Lista de tropes a evitar (default Recharts, generic admin table, flat hierarchy, etc.) que são checadas antes de commit.

4. **Helena audit pré-commit** — DS001-009 já existe; adicionar regras anti-slop específicas como DS010+. Bloquear merge se falhar.

5. **Editorial voice obrigatória** — números têm hierarquia (lead number 32px+, supporting 14px); cards têm narrative (não só dados). Inspiração: FT By the Numbers, Economist Daily Chart, Apple Stocks app.

---

## 🗓️ Sprint plan (Phase MM — Anti-Slop Redesign)

### Sprint MM.1 — Skill installation + spec finalisation (~30min)

> **Pre-req**: ✅ research streams completas. ✅ specs current-state já em
> `obsidian_vault/specs/` (committed 2026-05-08).

```bash
# 1. Install tier-1 skills (all 3 in parallel):

cd C:/Users/paidu/investment-intelligence/mission-control
npm install --save-dev impeccable
# Add to package.json scripts:
#   "design:audit": "npx impeccable --json"
#   "design:live":  "npx impeccable live"

# 2. Sparse-checkout open-design content bank:
mkdir -p ~/.local/design-banks
cd ~/.local/design-banks
git clone --depth=1 --filter=blob:none --sparse \
  https://github.com/nexu-io/open-design
cd open-design
git sparse-checkout set \
  skills/dashboard \
  skills/finance-report \
  skills/trading-analysis-dashboard-template \
  skills/critique \
  skills/tweaks \
  skills/dcf-valuation \
  design-systems/editorial \
  design-systems/clickhouse \
  design-systems/linear-app

# 3. Install taste-skill (redesign-existing-projects subset):
# (instructions vary; check repo README for current command)

# 4. Add tabular-nums to globals.css NOW (the single highest-leverage CSS line):
# Edit mission-control/app/globals.css:
#   :root, body { font-variant-numeric: tabular-nums lining-nums; }

# 5. User review of the 3 specs (already committed):
#   - obsidian_vault/specs/fair_trajectory.spec.md
#   - obsidian_vault/specs/consensus_panel.spec.md
#   - obsidian_vault/specs/ready_to_buy.spec.md
# Confirmar Hierarchy intent + Success metrics matches user's mental model
# antes de Sprint MM.2.
```

### Sprint MM.2 — 3 design directions paralelas (~1-2d)

```
4. Para cada componente (3 specs × 3 directions = 9 mockups), invocar
   huashu-design com prompt structurado:

   "Design [component] per spec at obsidian_vault/specs/X.spec.md.
    Generate 3 directions side-by-side as standalone HTML:
    - Direction A: FT Chart Doctor (editorial financial — Tufte+Wong)
    - Direction B: Linear/Stripe (modern fintech — restraint+typography hierarchy)
    - Direction C: Bloomberg Terminal (data-density king — keyboard-first)
    Use design tokens from mission-control/app/globals.css.
    Apply: tabular-nums, gold BUY pills (#F39F41 not green),
    inline SVG charts (no Recharts), range plot for ConsensusPanel."

5. Mockups em HTML standalone em obsidian_vault/design/mockups/<component>/<direction>.html.
   User vê 9 layouts side-by-side e escolhe 1 por componente (3 picks).

6. Run impeccable detector pré-mockup-handoff:
   npx impeccable --json mockups/*.html
   Reject + iterate any direction failing >2 anti-patterns.
```

### Sprint MM.3 — Implementation + Helena audit (~1d)

```
7. Implementar direção escolhida em .tsx. Componentes actuais ficam até
   merge — feature flag se preciso.

8. Helena audit DS010+ (regras anti-slop):
   DS010: tabular-nums presente em :root
   DS011: BUY pills usam --action-gold (não emerald)
   DS012: charts são inline SVG OU Recharts customizado (não default)
   DS013: hero-metric template ban (no 3-equal cards)
   DS014: side-stripe borders ≤1px
   DS015: no purple/blue gradients
   DS016: no Lucide-default icons
   DS017: placeholder discipline (no fake data, no "John Doe")

9. CI gate:
   npm run design:audit  # impeccable --json — bloqueia merge se falhar

10. User aprova visual final.
```

### Sprint MM.4 — Continuous YouTube ingest (~30min wire, then async)

```
11. Tier-S ingest (~30 vídeos, ~1h Whisper local):
    ii yt ingest --channel-last UCMalewiczHype --count 10
    ii yt ingest --channel-last UCOe-8z68tgw9ioqVvYM4ddQ --count 10  # Tailwind Labs
    ii yt ingest --channel-last UCoUxsWakJucWg46KW5RsvPw --count 10  # FT

12. Tier 1 batch (cron weekly Sunday):
    python scripts/yt_ingest_batch.py \
      --config config/yt_design_channels.yaml --tier 1

13. Helena scout consulta semanalmente — promove vídeos altos sinal para
    obsidian_vault/skills/Design_Watch.md "videos · weekly highlights".
```

### Sprint MM.5 — `/research` grid + outras pages (~1-2d, deferred)

```
10. Após MM.1-3 validados, aplicar mesmo workflow ao /research grid e ao
    /alertas page (que também são tabelas potencialmente slop-y).
```

---

## 📦 Out of scope para v2

- Re-skin completo do site (manter MC v5 JPM theme)
- React Native / mobile app
- Re-arquitectar lib/db.ts ou API endpoints (Phase LL data foundation já validada)
- Substituir Recharts por outra biblioteca (avaliar caso a caso, nem todo chart é slop)

---

## 🔁 Manutenção

- **Helena Linha scout** corre semanalmente (cron Sunday 23:30 em `daily_run.bat`).
  Discoveries entram em `obsidian_vault/skills/Design_Watch.md`. Promovem para
  install-tier quando relevantes. v2 deve ler Design_Watch antes de adicionar
  novas skills.

- **Specs commitadas** vivem em `obsidian_vault/specs/<component>.spec.md`. São
  source of truth para regressões — qualquer .tsx que divergir do spec é bug.

- **3-direction archive** — todos os 9 mockups (3 components × 3 directions)
  preservados em `obsidian_vault/design/mockups/<component>/<direction>.html`.
  Mesmo os não-escolhidos. Para futuras decisões.

---

## ⚡ "If only 5 things, do these" (priority punch-list)

> Synthesised across all 3 research streams. Highest-leverage low-cost
> actions — execute these antes mesmo do Sprint MM.1 ser totalmente formal.

1. **Add `font-variant-numeric: tabular-nums lining-nums` to `:root` in `globals.css`** — the single CSS line that separates serious finance UI from amateur. 2 minutes. Affects every number on every page.

2. **Recolor BUY pills from emerald green to Bloomberg Amber `#F39F41`** — emerald is documented AI-slop signature. Edit `--jpm-gain` usage in Action pills only (not P/L deltas — those stay green/red). 10 minutes.

3. **Install `impeccable` + run `npx impeccable --json` on current build** — get the deterministic baseline of how many anti-patterns we're flagging today. 5 minutes setup, instant signal.

4. **Adoptar `KAOPU-XiaoPu/web-design` spec-first workflow as project rule** — already started (3 specs committed). Make it CLAUDE.md rule: "no .tsx for UI without spec.md committed first". Update CLAUDE.md once. Permanent process change.

5. **Sparse-checkout `open-design` skills `dashboard` + `trading-analysis-dashboard-template`** — these are working HTML templates with the inline-SVG-no-Recharts pattern. Reference for Sprint MM.2 mockups. 5 minutes setup.

Do these 5 = move from "AI slop" to "credible foundation" without redesigning anything yet. Sprint MM.2-3 then redesigns from this base.

---

## 📝 Changelog

- **2026-05-08 noite** — v2 synthesis completa. 3 research streams sintetizados.
  Top-3 install order definido (impeccable + open-design + taste-skill).
  YouTube curation pronto (12 canais Tier S/1). Web pattern library com 28 refs.
  Convergent recommendations table (8 cross-stream agreements).
  Sprint MM.1-5 com comandos concretos. "If only 5 things" priority list.

- **2026-05-08** — v2 created após user critique "AI slop". Skeleton committed;
  research streams (GitHub/YouTube/Web) running em paralelo.
