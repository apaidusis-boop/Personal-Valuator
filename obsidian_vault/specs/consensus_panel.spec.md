---
type: component_spec
component: ConsensusPanel
status: current_state_documented
last_updated: 2026-05-08
tags: [spec, design, anti-slop, mm-sprint-1]
---

# Spec — ConsensusPanel

> Phase MM.1. Estado actual após critique "AI slop" 2026-05-08.

## Purpose

A frase exacta do user no início da phase:
*"BTG diz que o fair price é 15. XP diz 17. Para nós pode ser 14.50 ou 16.
Quero ver isto numa tabela e perceber a triangulação."*

Mostrar **multi-house consensus** — o nosso fair vs as casas brasileiras (Suno,
XP, BTG) vs Wall Street consensus (FMP) — agregar numa mediana/ponderada e dar
narrativa: *"Nossa diz 13, Suno diz 11.5 — mediana 12.25 — preço actual 13.30
está acima de ambos: HOLD."*

Esta é a peça **Mister Market** (à la Graham) do dashboard. Comparar nossa
view com o mercado, não para seguir, mas para confirmar/contrastar.

## Current implementation

`mission-control/components/consensus-panel.tsx` (consume `/api/consensus/[ticker]`).

```
┌──────────────────────────────────────────────────────┐
│ CONSENSO FAIR PRICE · 2 fontes      preço actual ... │  ← header
├──────────────────────────────────────────────────────┤
│ Fonte         Target    Stance    Idade              │
│ ─────────────────────────────────                    │  ← table
│ Nossa         R$ 12.99   —        hoje    ◀ highlight│
│ Suno          R$ 11.50   NEUTRAL  14d                │
│ ═════════════════════════════════                    │
│ Mediana       R$ 12.25   ponderada R$ 12.34  -7.9%   │  ← footer row
├──────────────────────────────────────────────────────┤
│ dispersão 8.6% · mediana/média R$ 12.25 / R$ 12.25   │  ← provenance
│ extract_targets re-pass para puxar BTG/XP PTs em...  │
└──────────────────────────────────────────────────────┘
```

## Data shape

```ts
GET /api/consensus/{ticker}
→ {
    ticker, market,
    our_fair, consensus_fair, current_price,
    n_sources: 2,                              // includes our_fair
    houses: [
      {source: "our_fair", target, recency_days, stance, confidence},
      {source: "suno", target, recency_days, stance, confidence, published_at},
      ...
    ],
    blended: { median, mean, weighted },
    dispersion: 0.086,                         // sigma/mu
    upside_blended_pct: -7.93
  }
```

## Known issues / slop traps observed

1. **Tabela genérica admin-style** — 4 colunas equal-weight, header em uppercase tracking-wider, rows com border-bottom. Look de SaaS dashboard padrão. **Falta voz editorial.**

2. **"Nossa" highlight é sutil demais** — bg-overlay + accent text não chega. A nossa view é a **âncora** da decisão; devia ser graficamente distinta (card-within-card? lateral border accent? lead-row treatment?).

3. **Stance pills (NEUTRAL/BULL/BEAR)** — texto small uppercase sem contextualização. Bull do BTG e Bull da Suno não têm o mesmo peso (track record diferente per house — Phase G `predictions_evaluate.py` tem isto). Devia surfacing isso.

4. **Footer row com mediana é graficamente similar às data rows** — aumenta border-top mas não muda layout. A mediana é o **takeaway** — devia ser hero number.

5. **"upside -7.9% vs preço"** — número crítico enterrado num cell na footer row, mesmo tamanho que os outros numbers. Devia ser hero também.

6. **n_sources baixo (1-2 hoje)** — quando só nossa view existe, o componente devia comunicar isso explicitamente em vez de fingir que "consenso de 1 fonte" é informativo. Hoje mostra dispersão 0%, mediana = nossa = sem info adicional.

7. **Nenhuma narrative** — falta a frase que fecha. *"Houses 11.50–12.99 → mediana 12.25 → preço 13.30 +8% acima da mediana → HOLD/TRIM zone."* Tudo está nos numbers mas não há ninguém a dizer o que significa.

## Hierarchy intent

| Nível | Elemento | Peso visual ideal |
|---|---|---|
| **Hero** (the answer) | Mediana + upside vs preço | XX-large number, dominant card area |
| **Primary** (the inputs) | Lista das casas com targets | Horizontal stack ou tabela com voz |
| **Secondary** (the anchor) | Nossa view (our_fair) com confidence stamp | Visual distinct — sidecard ou lead row |
| **Tertiary** (the trust signal) | Dispersão + n_sources + recência média | Small caption |
| **Quaternary** (provenance) | Stance per source, links para reports | Hover/expand |

## Density tradeoffs

- **2-3 sources comum** (ITSA4, BBDC4) — tabela 2-row é desproporcional, devia ser inline horizontal.
- **3+ sources com PT extraction** (futuro pós-extract_targets re-pass) — tabela faz sentido.
- **1 source só** (most US holdings hoje) — devia colapsar para apenas o card "Nossa" sem overhead.

Component devia adaptar o layout ao n_sources, não forçar tabela sempre.

## Anti-patterns

- ❌ Tabela 4-col equal-weight quando n_sources < 3
- ❌ Mediana enterrada em footer row
- ❌ Stance pills sem track-record context
- ❌ Italic "extract_targets re-pass" hint em produção (debug noise)
- ❌ "Nossa" linha apenas com bg-overlay (sutil demais)
- ❌ Linkless source names — cada source devia linkar para o report (analyst_reports.url)

## Success metrics

- [ ] Olhar 1 segundo: leio "consensus diz 12.25, preço está em 13.30, +8% above" → HOLD entendido
- [ ] Olhar 5 segundos: vejo as fontes, percebo que Suno é mais conservador que nós
- [ ] Olhar 30 segundos: clico em "Suno" → vou para o report onde a casa explica thesis
- [ ] N=1 caso (só our_fair): componente colapsa graciosamente, comunica "ainda só temos nossa view"

## References to reach for

- Bloomberg Terminal Ratings pane
- Visible Alpha / FactSet consensus tables
- FT "By the Numbers" sidebars
- Editorial Economist comparisons
- *(mais refs concretas quando agent 3 — Web research — completar)*
