---
title: Overnight session — Mission Control v2 redesign
date: 2026-05-05
type: morning_report
session: 2026-05-04 → 05 overnight
status: COMPLETE
---

# 🌅 Bom dia. O Mission Control foi todo refeito durante a noite.

> "Esses front end está muito pobrinho, as coisas não estão otimizadas, datas aleatórias, não tem conexão." — tu, ontem à noite.

Recebi o pedido. Pensei muito antes de mexer em código (o memo está em `obsidian_vault/skills/Mission_Control_Design_v2.md`). Depois implementei.

---

## TL;DR

- **2 commits** novos pushed para origin (`d95c2b0` Mission Control v2 + tudo o que o precede)
- **14/14 rotas** com 200 OK em dev server
- **npm run build** verde
- **95+ problemas** identificados no audit, **maioria resolvida**
- **Tudo connectado** — breadcrumbs, links contextuais, dates humanizadas, empty states amigáveis

Para ver: `cd C:\Users\paidu\investment-intelligence\mission-control && npm run dev`, abrir <http://localhost:3000>.

---

## O que mudou — em uma palavra cada

| Categoria | Antes | Agora |
|---|---|---|
| **Cores** | Cyan/purple/green/red/yellow/magenta sem regra | Tokens semânticos: verdict (BUY/HOLD/AVOID), market (BR/US), quality, accent |
| **Tipografia** | 6+ tamanhos misturados ad-hoc | 9 escalas definidas (display/h1/h2/h3/body/body-sm/caption/mono/mono-sm) |
| **Spacing** | Aleatório (p-3, p-4, p-5...) | Grid 8pt (--space-1 a --space-16) |
| **Datas** | "2026-04-28" cru | "há 3 dias" + tooltip com data exacta |
| **Iconografia** | 🐙 ☀ 💸 📈 🟢 🟡 🔴 ⚪ caóticos | Mono symbols (◉ ◯ ◐ ▲ ▼ ⚑ ✓ ✗ →) |
| **Empty states** | "Corre `python scripts/foo.py`" | "Nenhum X disponível ainda" + acção sugerida |
| **Navegação** | Pages isoladas | Breadcrumbs + connections + ⌘K chat |
| **Cards** | Bordas saturadas, gradientes vivos | Bordas subtis, hover discreto |
| **Status** | Verde/vermelho sem texto | Pills semânticas com label |

---

## Foundation construída

### `app/globals.css` — design tokens v2
- **Surfaces**: `--bg-canvas`, `--bg-elevated`, `--bg-overlay`, `--bg-deep`
- **Borders**: `--border-subtle`, `--border-strong`
- **Text**: 4 níveis (`primary` / `secondary` / `tertiary` / `disabled`)
- **Verdicts**: BUY/HOLD/AVOID/N/A — uma cor por verdict, igual em **todas** as páginas
- **Markets**: subtle BR (yellow) / US (blue)
- **Quality**: ok / warning / degraded / critical (alinhado com `FetchResult`)
- **Spacing**: 4-64px em grid 8pt
- **Motion**: 120/180/320ms com easing curves

### `lib/format.ts` — formatadores únicos para tudo
```ts
formatDate(iso, "relative")  → "há 3 dias"
formatDate(iso, "short")     → "28 abr"
formatCurrency(value, "BRL") → "R$ 12.345,67"
formatPercent(0.123, 1)      → "12.3%"
formatPercent(0.05, 1, {fromFraction: true}) → "5.0%"
humanizeSchedule("daily 09:30") → "every day · 09:30"
isStale(date, 24) → boolean (>24h?)
```

### `components/ui/` — 5 primitives
- `<PageHeader>` — breadcrumb + title + subtitle + freshness pill + actions
- `<Section>` — label + meta + right-side action ("view all →")
- `<Stat>` — label + display value + delta arrow (color-aware) + caption + icon
- `<Pill>` — 9 variants semantic (no more inline tailwind soup)
- `<EmptyState>` — icon + title + description + action

---

## Pages — antes vs depois

### `/` Home
- 4 stat cards em vez de 3 (adicionei "Council Today")
- Briefing card com freshness real (mtime do ficheiro, não hardcoded)
- **Action priority** com `<TaskRowActions>` inline (approve/skip/deepdive)
- Dividendos table com relative dates
- Agents list com relative timestamps
- Council snapshot redesenhado

### `/allocation`
- Header com breadcrumb + freshness do JSON
- Bucket pills (graham 25 · buffett 30 · drip 20 · macro 15 · hedge 10)
- Macro tilt context inline (regime + tilt-up + tilt-down sectors)
- Hedge banner inline (só aparece quando active)
- Top-15 weights table com bar viz
- Conflicts grid com engine pills coloridas

### `/strategy/[ticker]`
- Breadcrumb: `Allocation › US › ACN`
- Cards expansíveis com summary visível (verdict pill + score /100 + weight)
- Rationale renderizado:
  - **graham/buffett/drip**: tabela de critérios com ✓/✗ + value + threshold
  - **macro/hedge**: flat key/value
- Footer com link `/ticker/{tk}` prominente

### `/ticker/[ticker]`
- Hero com display price + delta arrow + market pill
- **Council strip** card (clickable → council story)
- Price chart 365d
- 3 quadrants: Position / Fundamentals / Screen
- Strategy breakdown row com pills das 5 engines

### `/tasks`
- `<TaskRowActions>` rendered (approve/skip/deepdive)
- Cards com market pill + ticker link + relative date
- Empty state amigável

### `/council`
- Counts em 5 boxes (total · buy · hold · avoid · n/a)
- Sections por stance (avoid first — risk-first)
- Cards com seats info + dissent/flag pills
- Earlier runs table com sticky header

### `/memory`
- Tabs maiores, hover state claro
- Daily entries com relative date + abs date + word count

### `/calendar`
- 4-column schedule grid (daily/weekly/every/manual)
- Schedules **humanizados** ("every day · 09:30" em vez de "daily 09:30")
- Dividendos em table proper com sticky header

### `/content`
- Tier pills tokenizadas (consistent com resto)
- Digests com preview limpo
- Knowledge cards clickable

### `/team`
- Founder + Chief feature cards
- Departments com run/fail counters
- Schedules humanizados

### `/projects`
- Status glyphs (✓ ◐ ◯ ·) em vez de só cor
- Phases com relative date inline

### `/docs`
- Dossiers clickable → `/ticker/{tk}`
- ScoreBox tokenizado (F/Z/M)

### `/visual`
- PageHeader integrado, rest preservado (era OK)

---

## Antonio Carlos chat — upgrade

### Antes
- Botão 🐙 fixo bottom-right
- Aceita texto livre
- Sem shortcuts

### Agora
- **⌘K / Ctrl+K** abre/fecha
- **Esc** fecha
- **6 slash commands**:
  - `/allocate` → ver proposta de alocação
  - `/hedge` → estado do hedge tactical
  - `/strategy ACN` → engines de um ticker
  - `/why JNJ` → drivers do verdict
  - `/position ITSA4` → minha posição actual
  - `/regime` → regime macro BR + US
- **Autocomplete** com `Tab` (mostra suggestions strip enquanto escreves /)
- Empty state lista os shortcuts como botões clicáveis
- Visual polish — token-driven, gradient mark refinado, bubbles suaves

---

## Critical fixes (P1)

✅ **`<TaskRowActions>` rendered** — actions aparecem no Home E na página `/tasks` (antes só em `/tasks` e mesmo lá era sub-óptimo)
✅ **Datas formatadas** — todas via `formatDate()` (relative por default, com tooltip ISO)
✅ **Empty states amigáveis** — zero comandos Python expostos
✅ **Navegação connectada**:
  - Home → /tasks → /ticker → /council → /strategy → /allocation
  - Dossiers → /ticker
  - Council/X → /ticker/X (e vice-versa)
  - Allocation conflicts → /strategy/X com market preserved
✅ **Breadcrumbs** em todas as páginas profundas
✅ **Freshness pills** mostram quando dados foram actualizados (e ⚑ se stale)

---

## O que NÃO mudou (intencional)

- **Mobile burger menu** — diferido (usas desktop primário)
- **Cmd+K global search** — não há infra ainda; chat widget tem ⌘K mas é só toggle
- **Light mode** — never (dark é a estética)
- **i18n PT/EN labels** — manteve PT primário com EN labels onde já estavam
- **Visual page** — manteve pixel-art (delight, baixa prioridade)

---

## Como testar agora

```powershell
cd C:\Users\paidu\investment-intelligence\mission-control
npm run dev
# http://localhost:3000
```

Roteiro sugerido (5 min):
1. **Home** → vê os 4 stats (PnL real com cores), o action card com botões approve/skip
2. **/allocation** → vê os bucket pills, hedge OFF (estamos em expansion), top weights
3. Clica em **AAPL** na tabela → `/strategy/AAPL` com engines breakdown
4. Clica em **ticker page →** → `/ticker/AAPL` com hero, position, fundamentals
5. **⌘K** abre chat → escreve `/al` (autocomplete sugere `/allocate`)

---

## Próximas direcções (escolhe quando voltares)

1. **Search global Cmd+K** — autocompletar tickers, ir directo a /ticker/X
2. **Real-time price ticker** — mini barra no topo com tickers em movimento
3. **Skill/Strategy badges no Home** — em cada holding mostrar verdict de cada engine
4. **Quick actions row no Home** — buttons para correr `ii overnight`, `ii brief`, etc
5. **Loading states / spinners** — skeleton screens para charts
6. **Mobile responsive** — burger sidebar em <768px
7. **Cron schedule do `ii overnight` 23:30** — nightly auto-backfill via Windows Task Scheduler

---

## Memo design completo

`obsidian_vault/skills/Mission_Control_Design_v2.md` — filosofia, design tokens, IA, decisões, plano de execução. **Lê se queres entender as decisões.**

---

## Stack final do session

```
d95c2b0  Mission Control v2: design tokens + primitives + 13 page redesigns ← novo
f1df2ab  Overnight backfill + Mission Control: Allocation/Strategy + Hedge banner
b40e076  Agent governance: agent_call + 6 role specialists + decisions DB
27b4323  strategies/ package: 5-engine multi-philosophy framework
2da3338  stage ITR zips for LFS migration
ec3ad76  ignore data/api_cache.db
```

Tudo pushed para `origin/main`.

Bom dia. ☕
