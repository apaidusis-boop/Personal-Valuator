---
title: Mission Control — Design v2
date: 2026-05-04
status: IMPLEMENTING
author: claude (overnight session)
references:
  - "Linear (linear.app) — sidebar restraint + breadcrumbs"
  - "Bloomberg Terminal — info density without clutter"
  - "Notion — typographic hierarchy + monospace counterpoint"
  - "Robinhood — semantic color minimalism"
  - "Tina Huang's Mission Control screenshots (existing reference)"
---

# Mission Control v2 — Design Memo

**Pedido do user**: o front-end actual está *"muito pobrinho, datas aleatórias, não tem conexão"*. Quer **minimalista, clean, profissional** — escala Linear/Bloomberg/Notion.

Este memo é a base de design (filosofia, tokens, IA, page-by-page) para a refactor da Mission Control. Audit detalhado está em `data/_overnight_audit_2026-05-04.md` (95+ problemas mapeados).

---

## 1. Filosofia (3 regras)

### 1.1 **Density without clutter**
Bloomberg-grade information density. Cada pixel carrega significado. Mas: hierarquia tipográfica clara, cores semânticas, white space deliberado.

### 1.2 **Connected, not isolated**
Cada página é parte de um workflow. Breadcrumbs, contextual links, "see also" sections. User nunca chega a um dead-end.

### 1.3 **Show your data freshness**
Cada secção mostra quando foi actualizada. "há 3h" / "há 2 dias" / "stale ⚠". User confia porque vê.

---

## 2. Design Tokens

### 2.1 Cores (semânticas, não decorativas)

```css
/* Foundation */
--bg-canvas:       #0a0a14;   /* page background */
--bg-elevated:     #0f0f1f;   /* card / panel */
--bg-overlay:      #15152e;   /* hover / input */
--border-subtle:   #1a1a3a;   /* default border */
--border-strong:   #2a2a55;   /* emphasized border */

/* Text */
--text-primary:    #e8e8f0;   /* default */
--text-secondary:  #a0a0b8;   /* labels, secondary */
--text-tertiary:   #5a5a78;   /* muted, captions */
--text-disabled:   #303048;

/* Accent — primary brand (rare use) */
--accent-primary:  #8b5cf6;   /* purple — tactical / nav active only */
--accent-glow:     #06b6d4;   /* cyan — links / focus rings */

/* Semantic — verdicts (consistent everywhere) */
--verdict-buy:     #22c55e;   /* green */
--verdict-hold:    #f59e0b;   /* amber */
--verdict-avoid:   #ef4444;   /* red */
--verdict-na:      #71717a;   /* zinc */

/* Semantic — financial */
--gain:            #22c55e;
--loss:            #ef4444;
--neutral:         #71717a;

/* Semantic — markets (subtle, not loud) */
--mkt-br:          #fbbf24;   /* yellow tint, B3 */
--mkt-us:          #3b82f6;   /* blue tint, NYSE/NASDAQ */

/* Semantic — quality flags (data layer) */
--qual-ok:         #22c55e;
--qual-warning:    #f59e0b;
--qual-degraded:   #f97316;   /* orange */
--qual-critical:   #ef4444;
```

**Regras de uso**:
- Nada de `text-zinc-300` ad-hoc. Tudo via vars.
- Verdicts (BUY/HOLD/AVOID) **sempre** com a mesma cor cross-page.
- Purple = nav active only. Não decoração.
- Cyan = focus ring + link hover. Não decoração.

### 2.2 Tipografia (escala clara)

```css
/* Display — page hero numbers (rare) */
--type-display:    32px / 1.1 / 600 / -0.02em;

/* Headings */
--type-h1:         24px / 1.2 / 600 / -0.01em;
--type-h2:         18px / 1.3 / 600 / 0;
--type-h3:         14px / 1.4 / 600 / 0.02em / uppercase;

/* Body */
--type-body:       14px / 1.5 / 400 / 0;
--type-body-sm:    13px / 1.5 / 400 / 0;
--type-caption:    12px / 1.4 / 400 / 0;

/* Mono (numbers, tickers, dates, code) */
--type-mono:       13px / 1.4 / 500 / 0;
--type-mono-sm:    11px / 1.4 / 500 / 0.04em;

/* Family */
--font-sans:       "Inter", system-ui, sans-serif;
--font-mono:       "JetBrains Mono", "SF Mono", Menlo, monospace;
```

**Regras**:
- Nunca >5 sizes numa única página.
- Numbers → mono. Sempre. Tabular numerals.
- H3 = uppercase + letter-spacing (label-style).

### 2.3 Spacing (8pt grid)

```css
--space-1:  4px;
--space-2:  8px;
--space-3:  12px;
--space-4:  16px;
--space-5:  20px;
--space-6:  24px;
--space-8:  32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

**Regras**: padding interno de cards = `--space-4` ou `--space-6`. Section gaps = `--space-8`.

### 2.4 Radius

```css
--radius-sm: 4px;   /* pills, badges */
--radius:    8px;   /* cards, inputs */
--radius-lg: 12px;  /* panels */
```

### 2.5 Motion (subtle)

```css
--motion-fast:   120ms ease-out;
--motion:        180ms ease-out;
--motion-slow:   320ms cubic-bezier(0.16, 1, 0.3, 1);
```

**Regras**: nada de bounce gratuito. Animations only on user action (hover, focus, expand). Status dots têm pulse, mas controlado.

### 2.6 Iconografia

**Decisão**: monospace symbols (◉ ◯ ◐ ▲ ▼ ⚑ ✓ ✗ →), **não emoji**.

| Symbol | Meaning |
|---|---|
| ◉ | active / live / present |
| ◯ | empty / off / absent |
| ◐ | partial / loading |
| ▲ ▼ | trend up/down |
| ⚑ | flag / alert |
| → | navigate / drill in |
| ✓ ✗ | pass / fail |
| ◇ | item / pending |
| ⌘ ⏎ | keyboard cues |

**Sidebar nav icons**: keep current unicode set — coerência interna do projecto. Mudar só os caóticos (emoji ☀, 💸, 📈, 🐙).

---

## 3. Information Architecture

### 3.1 Páginas — propósito 1-line

| Path | Propósito (1 frase) | Persona |
|---|---|---|
| `/` | "Dashboard hoje: portfolio + actions + briefing matinal" | Quotidian glance |
| `/allocation` | "Alocação alvo combinada (5 engines × 2 mkts)" | Strategy planning |
| `/strategy/[tk]` | "Por que este ticker tem este peso? 5 engines explicam" | Drill-down |
| `/ticker/[tk]` | "Ficha técnica: preço + fundamentals + posição + tese" | Deep research |
| `/council` | "Conselho sintético: BUY/HOLD/AVOID por ticker" | Conviction calibration |
| `/council/[tk]` | "Dossier completo: storytelling + dissent + size" | Decision support |
| `/tasks` | "Triggers em aberto — actions a aprovar" | Workflow |
| `/calendar` | "Cronograma agentes + ex-divs + earnings" | Operational |
| `/content` | "Topic watchlist + research digests + knowledge cards" | Reading |
| `/memory` | "Daily logs + auto-memory + chat history" | Audit |
| `/team` | "Org chart agentes" | Awareness |
| `/visual` | "Office pixel-art (delight)" | Polish |
| `/docs` | "Dossier catalog" | Archive |

### 3.2 Sidebar — refactor

**Remover** Visual da nav principal (mover para footer/easter-egg).
**Adicionar** Ticker (universal access — search-driven).

Grupos:
```
TODAY
  ◇ Home
  ▤ Tasks

DECIDE
  ▲ Allocation
  ⚖ Council

RESEARCH
  ❖ Content
  ✶ Memory
  ≡ Docs

SYSTEM
  ▦ Calendar
  ◉ Team
```

`/ticker/X` e `/strategy/X` são páginas dinâmicas — não no sidebar. Acesso via:
- Search global (cmd+k) — futuro
- Por agora: link em todas as listagens

### 3.3 Breadcrumb global

Nova `<Breadcrumb />` no topo de cada layout child:
```
Allocation › US › ACN
```
Cada segmento clicável. Reduz "lost in nav".

### 3.4 Connection map (key links)

```
Home ─────┬─→ /tasks (action item)
          ├─→ /allocation (portfolio composition)
          ├─→ /ticker/X (drill from holdings table)
          └─→ /council/X (drill from council snippet)

Allocation ─→ /strategy/X (per-ticker engine breakdown)
            ←─ Strategy → /ticker/X (price + fundamentals)

Council ──→ /council/X (full dossier)
          → /ticker/X (price/fundamentals link)
          ←─ /ticker → /council (related dossier)

Tasks ───→ /ticker/X (context on triggered ticker)
```

---

## 4. Layout Primitives

### 4.1 `<PageHeader>`
- breadcrumb
- title (h1)
- subtitle (optional)
- actions (right side, optional)
- freshness pill ("updated 2h ago")

### 4.2 `<Card>`
- Default padding `--space-6`
- Border `--border-subtle`
- Optional header (title + actions row)
- Optional footer (link / CTA)

### 4.3 `<Stat>`
- label (uppercase mono)
- value (display or h1, mono if number)
- delta (optional, ▲/▼ color-semantic)
- caption (optional, tertiary text)

### 4.4 `<Pill>`
Variants: `verdict-buy`, `verdict-hold`, `verdict-avoid`, `mkt-br`, `mkt-us`, `qual-ok`, `qual-warning`, neutral.

### 4.5 `<Section>`
- h3 label (uppercase)
- optional right-side meta (count, date)
- content slot

### 4.6 `<EmptyState>`
- icon (◯)
- title (1 line)
- description (1-2 lines, no terminal commands)
- action button (optional)

### 4.7 `<Freshness>`
Standalone pill: "◉ live" | "2h ago" | "stale 3d ago ⚠"

### 4.8 `<HedgeBanner>`
Already exists. Refactor to use design tokens + add "why" tooltip.

---

## 5. Date / Number Formatting

Helper `lib/format.ts`:

```typescript
formatDate(iso, mode):
  'relative'  → "há 3 dias", "há 2h", "agora mesmo"
  'short'     → "28 abr"
  'medium'    → "28 abr 2026"
  'iso'       → "2026-04-28"
  'datetime'  → "28 abr · 14:30"

formatCurrency(value, currency):
  → "R$ 12.345,67" or "$12,345.67" (locale aware)

formatPercent(value, digits=1):
  → "12.5%" (always with sign for deltas: "+2.3%")

formatNumber(value, opts):
  compact: "1.2M", "456k"
  signed: "+12.5", "-3.1"

formatTickerSize(market, ticker):
  // pads to 6 chars for tabular alignment
```

**Aplicação**: TODAS as datas no app passam por `formatDate(iso, 'relative')` por default. ISO só em tooltips.

---

## 6. Page-by-Page Redesign

### 6.1 `/` Home (re-pensada)

**Estrutura nova**:

```
┌─ HedgeBanner (se hedge active) ────────────────────────────────────┐
│                                                                    │
│  Mission Control                            Briefing 2h ago ◉       │
│  ────────────────────────────────────────────────────────────────  │
│                                                                    │
│  [Portfolio BR]    [Portfolio US]   [Open Actions]   [Council]    │
│   R$ 123,456        $45,678          12 pending      8 today      │
│   +12.5% YTD        -3.2% YTD        →               2 AVOID ⚑    │
│                                                                    │
│  ─── BRIEFING MATINAL ────────────────────────── Aurora · 07:00 ── │
│  (markdown rendering, max 500 words, "see full →")                 │
│                                                                    │
│  ─── ACTIONS (4 priority) ─────────────────────────── view all →── │
│  ┌─ ITSA4 · price drop −12% ───────────── 2h ago ──[approve][skip]┐│
│  ┌─ JNJ · earnings beat ──────────────── 5h ago ──[approve][skip]┐│
│  ...                                                                │
│                                                                    │
│  ─── COUNCIL TODAY ─────────────────── 8 reviewed · 2026-05-04 ── │
│  AVOID (2)  ⚑ flagged (3)  ─→  view council                       │
│                                                                    │
│  ─── DIVIDENDS · NEXT 14 DAYS ────────────────────────────────── │
│  KO  · 06 mai · $0.485 · yield 3.2%                                │
│  ...                                                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

Diferenças do actual:
- Stats em 4 colunas (não 3) → adiciona "Council today"
- Briefing com freshness pill
- Actions com **botões reais** (approve/skip) — task #1 do P1
- Sections com ⏵→ "view all" semântica clara
- Datas relativas everywhere

### 6.2 `/allocation` (refactor)

**Mantém estrutura atual** (estava bem). Mudanças:
- HedgeBanner movido para layout (já está)
- Bucket weights pills com tokens (purple muted, não saturated)
- Conflicts: cada conflict mostra **severidade** (low/med/high) por contagem de engines em desacordo
- "Last allocation: 14h ago ◉" pill no header
- Empty state amigável

### 6.3 `/strategy/[ticker]` (refactor)

- Breadcrumb: `Allocation › US › ACN`
- Top: composite score line ("Buffett 0.6 · DRIP 0.9 · Macro 1.0 · Hedge HOLD")
- Cards expansíveis ainda — mas **summary visible** (top 2-3 reasons in plain text)
- Footer link "view ticker page →" mais prominente

### 6.4 `/ticker/[ticker]` (re-pensada — major)

**4 quadrants**:

```
┌─ HEADER ───────────────────────────────────────────────────────────┐
│  ACN · Accenture                          $328.50  ▲ +2.1% today    │
│  Communication Services · US                                       │
│  Breadcrumb: Home › ACN                                             │
└────────────────────────────────────────────────────────────────────┘

┌─ POSITION ──────────────────┐  ┌─ SCREEN ───────────────────────┐
│  Quantity:  20.5            │  │  Buffett · 0.85 · BUY            │
│  Avg cost:  $245.00         │  │  ✓ PE 18 (≤20)                  │
│  Market val: $6,734         │  │  ✓ ROE 22%                       │
│  PnL:        +34.1%          │  │  ✗ DY 0.9% (<2.5%)              │
│  YoC:        2.8%            │  │  ✓ Aristocrat                    │
│  vs IBOV:    +12pp          │  │  ROIC 28% (Buffett bar 15%)     │
│                             │  │  ─→ full strategy breakdown      │
└─────────────────────────────┘  └────────────────────────────────┘

┌─ PRICE 365D ──────────────────────────────────────────────────────┐
│  (chart with high/low/avg overlay)                                │
└───────────────────────────────────────────────────────────────────┘

┌─ FUNDAMENTALS Q1 2026 ───────┐  ┌─ COUNCIL · 2026-05-01 ─────────┐
│  PE      18.2                │  │  Stance:  HOLD ⚑                 │
│  PB      6.8                 │  │  Flags:   3                      │
│  DY      0.9%                │  │  Dissent: 2                      │
│  ROE     22%                 │  │  ─→ full dossier                  │
│  ROIC    28%                 │  │                                   │
│  ND/EBITDA 0.8x              │  │  Last position note:              │
│  Filed: 28 abr (Q1 26)       │  │  "Compounding intact, fair price" │
└──────────────────────────────┘  └───────────────────────────────────┘

[Pending Actions on this ticker]  ←  if any, with approve/skip buttons
```

### 6.5 `/council` (refactor)

- Filter chips no topo: `All · BUY · HOLD · AVOID · Flagged`
- Datas relativas
- Cards mostram **first dissent topic** (não só count)
- "Last run: 2h ago" pill

### 6.6 `/tasks` (refactor — fix CRITICAL)

- **Render `<TaskRowActions>`** — fix da issue #1
- Filter chips: market, kind
- Sort options
- Datas relativas
- Empty state amigável

### 6.7 `/memory` (refactor)

- Tabs maiores, com count badges
- Datas relativas
- Long-term memories: card grid, color por type (legend visible)
- Chat list: alias de chat_id (substring) + last activity relative

### 6.8 `/calendar` (refactor)

- Schedules human-readable ("daily 09:30" → "every day at 9:30 AM")
- Dividends sorted by date, com yield context
- Empty state se nada nos próximos 14d

### 6.9 `/content` (refactor)

- Topics com tendência (▲/▼ vs last week)
- Tier colors com escala lógica (red=avoid → orange=watch → green=opportunity)
  - Wait, isso colide com BUY=green. Vou usar: tier = neutral palette (purple-cyan-grey-graphite)
- Knowledge cards: parse frontmatter properly

### 6.10 `/team` (refactor)

- Bio com max 100 chars + "..."
- Schedule humanizado
- Status dots com tooltip do que significa

### 6.11 `/visual` (delight, low priority)

Mantém. Rever só os emoji collisions.

### 6.12 `/docs` (refactor)

- Cards clicáveis → `/ticker/[tk]` (não só link textual)
- Empty state amigável

---

## 7. Implementação — Ordem

1. **Foundation** (tokens + helpers + primitives)
   - `globals.css` com CSS vars novos
   - `lib/format.ts` com date/number helpers
   - `components/ui/*` — Card, Stat, Pill, PageHeader, Section, Pill, EmptyState, Freshness, Breadcrumb

2. **Layout** (sidebar + breadcrumb + chat)
   - Sidebar com grupos TODAY/DECIDE/RESEARCH/SYSTEM
   - Breadcrumb dinâmico
   - HedgeBanner refactored

3. **Critical fixes** (P1)
   - `<TaskRowActions>` rendered em /tasks
   - `/ticker/[X]` discoverable

4. **Page redesigns** (em ordem de impacto)
   - /              (hub central)
   - /allocation    (decision)
   - /strategy/[X]  (drill)
   - /ticker/[X]    (drill — biggest refactor)
   - /tasks         (fix critical)
   - /council       (filters)
   - /memory        (datas + grouping)
   - /content, /calendar, /team, /docs (polish)

5. **Antonio Carlos chat upgrade**
   - Slash shortcuts: `/allocate`, `/hedge`, `/strategy ACN`, `/why ACN`
   - Visual polish (consistent with tokens)

6. **Build + smoke + commit + push**

---

## 8. Não-objectivos (skip explicitamente)

- Mobile-first burger menu (deferred — user usa desktop)
- Cmd+K global search (futuro — não há infra)
- Real-time websockets (overkill — page reload OK)
- Theme switcher light mode (dark only por design)
- i18n (PT/EN — keep PT primary, EN labels OK)

---

## 9. Métricas de sucesso (post-implement)

- ✓ Cada página: 1 herói + máx 4 secções
- ✓ Cada data: humanizada (relative or short)
- ✓ Cada empty state: sem comando Python visível
- ✓ Cada link/CTA: discoverable < 1s
- ✓ npm run build verde
- ✓ npm run dev: 200 em todas as rotas
- ✓ Smoke test: clicar em 5 paths chave (Home → Action → Ticker → Council → Strategy → Allocation)

---

## 10. Decisões abertas (validar manhã)

1. **Visual page** — manter ou esconder? (Mantém, mover para footer link.)
2. **Cmd+K search** — implementar agora ou skip? (Skip, defer.)
3. **Light mode** — opcional ou never? (Never. Dark only.)
4. **Mobile** — invest now ou after? (After. Desktop primary.)
5. **i18n** — PT primary com EN labels (status quo)? Sim.

---

Pronto para implementar.
