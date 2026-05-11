---
type: component_spec
component: ReadyToBuyTile
status: current_state_documented
last_updated: 2026-05-08
tags: [spec, design, anti-slop, mm-sprint-1]
---

# Spec — ReadyToBuyTile

> Phase MM.1. Estado actual após critique "AI slop" 2026-05-08.

## Purpose

A frase exacta do user no início da phase:
*"What I need is in my dashboard on the main page. Look at the moment and say,
this stock is a buy. I should add right now."*

Componente da home page que dá **resposta one-glance**: dos 33 holdings + watchlist,
quais é que estão em BUY zone agora — preço abaixo do nosso fair, confidence
não-disputada, sem distress vetoes. Mostra topN ordenados por upside.

Esta é a peça **acção** do dashboard. Não é uma tabela de explorar — é uma
lista curta, opinionated, "podes adicionar agora a estes 3-6 nomes".

## Current implementation

`mission-control/components/ready-to-buy-tile.tsx` (consume `/api/ready-to-buy`).

```
┌──────────────────────────────────────────────────────────────────┐
│ Ready to buy   BR · ação BUY+ · confiança não-disputada    ...→  │
├──────────────────────────────────────────────────────────────────┤
│ Ticker     Ação        Preço     our_fair    Upside    Conf.     │
│ ──────────────────────────────────                                │
│ O REIT     STRONG_BUY  $ 64.01   $ 72.40    +13.1%    ✓ verified │
│ XP FIN     BUY         $ 19.57   $ 21.25    +8.6%     single src │
│ PVBI11 ... BUY         R$ 75.50  R$ 80.89   +7.1%     single src │
└──────────────────────────────────────────────────────────────────┘
```

## Data shape

```ts
GET /api/ready-to-buy?market={br|us}&limit=6
→ {
    rows: [{
      market, ticker, name, sector,
      current_price, our_fair, fair_price,
      action, confidence_label,
      our_upside_pct, upside_pct,
      computed_at
    }, ...],
    n
  }
```

Filtro: `action ∈ {BUY, STRONG_BUY}` AND `confidence_label != 'disputed'`.
Sort: `our_upside_pct desc`.

## Known issues / slop traps observed

1. **Tabela 6-column horizontal** — typical admin dashboard. Cada row é um ticker mas não há **diferenciação entre STRONG_BUY (acção urgente) e BUY (acção tranquila)**. Visualmente quase iguais.

2. **Pills de acção genéricas** — "STRONG_BUY" solid green, "BUY" outlined green. Mesmo tamanho que outros elementos da row. Devia ser **lead element** — se a acção é o ponto, devia dominar a row.

3. **Confidence badge à direita esquecida** — "✓ verified" vs "single source" é signal crítico (verified = age agora, single = espera mais data). Mas está no canto direito small text — invisível.

4. **Upside number isolated** — "+13.1%" é o ranking signal. Mas vem entre our_fair (referência) e Conf (signal). Devia ser destacado.

5. **Falta hierarquia entre os 3-6 rows** — todos têm peso igual. Mas o top-1 (highest upside, cross_validated) é qualitativamente diferente do bottom (single_source low upside). Top-1 devia ter hero treatment, restantes lista compacta.

6. **Sem narrative voice** — onde está *"hoje, 3 holdings estão em BUY zone — O com REIT recovery thesis, XP com upside contrarian, PVBI11 turnaround"*? Pure data, no voice.

7. **Sector text uppercase tiny** — informação útil (REIT, FIN, FII) mas tipográficamente engolida. Sector influencia a tese (REIT = rate-cut thesis; FII = NAV thesis); devia ser visível.

8. **"ver universe →" link no header** — implica navegação para algo (que existe? `/research`?) mas o user provavelmente quer drill-in para um row específico, não para o universe. Hierarquia de actions confusa.

## Hierarchy intent

| Nível | Elemento | Peso visual ideal |
|---|---|---|
| **Hero** (top action) | Top-1 ticker — STRONG_BUY com upside e confidence cross_validated | Big card, dominant area, lead number |
| **Primary** (queue) | 2-5 outros tickers BUY-ranked | Compact stack, scannable in 3-5s |
| **Secondary** (context) | Sector + thesis snippet (1 linha) per row | Visible but second |
| **Tertiary** (status) | Confidence + price/fair detail | Hover/expand or right-aligned small |

## Density tradeoffs

- **Home page real estate** — tile compete com Top positions, Asset allocation, Markets/Calendar/Watchlist. Devia ser **focal point**, não peer.
- **Mobile**: 6-column tabela quebra. Devia colapsar para card stack vertical com hero+queue.
- **N=0 case** — *"hoje nenhum holding em BUY zone"* é IMPORTANTE comunicar (não vazio sad-face italic). Devia ter call-to-action: "watchlist ranked by proximity to BUY zone" ou similar.

## Anti-patterns

- ❌ 6-column equal-weight table na home page
- ❌ Action pills do mesmo size que sector text
- ❌ Empty state com italic genérica
- ❌ Confidence label como afterthought à direita
- ❌ Upside number sem destaque
- ❌ "Ready to buy" header genérico em uppercase
- ❌ Sem thesis snippet — pure metrics

## Success metrics

- [ ] Olhar 1 segundo: leio "O é o top BUY agora, +13% upside cross_validated" — decisão preliminar
- [ ] Olhar 5 segundos: vejo os outros 2-5 candidates e seus contextos sectoriais
- [ ] Olhar 30 segundos: clico no top-1 → /ticker/O com toda a triangulação
- [ ] N=0 caso: componente comunica "mercado overpriced" + sugere proximity-watchlist
- [ ] Mobile: stack vertical funciona, hero card destaca

## References to reach for

- Apple News editor's picks (hero card + secondary list)
- Stripe "you might want to" cards
- Linear's prioritization views (top item visually distinct)
- Notion database hero rows
- *(mais refs concretas quando agent 3 — Web research — completar)*
