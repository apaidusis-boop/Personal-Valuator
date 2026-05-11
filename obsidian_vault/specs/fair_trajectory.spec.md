---
type: component_spec
component: FairTrajectoryChart
status: current_state_documented
last_updated: 2026-05-08
tags: [spec, design, anti-slop, mm-sprint-1]
---

# Spec — FairTrajectoryChart

> Phase MM.1. Documenta o **estado actual** do componente após critique
> "AI slop" 2026-05-08. Input para o Sprint MM.2 (3 design directions paralelas).

## Purpose (o que tenta comunicar)

Mostrar a **trajectória de longo prazo** do nosso fair value para um ticker —
a frase do user no início desta phase: *"5 anos atrás ITSA4 era R$10, agora
é R$15. O meu preço médio é R$8. Tenho confiança para adicionar mais."*

Três séries simultâneas:
1. **`our_fair`** (linha sólida accent) — o nosso preço justo conservador (filings + safety margin per-sector)
2. **`fair_price`** (linha tracejada muted) — o consensus Buffett/Graham raw
3. **`current_price`** (linha cor de mercado) — preço actual diário

A leitura ideal: *"o nosso fair tem subido em compounding consistente; o preço
às vezes sobe acima, às vezes abaixo; nas vezes que o preço cai abaixo do nosso
fair → BUY zone."*

## Current implementation

`mission-control/components/fair-trajectory-chart.tsx` (consume `/api/fair-trajectory/[ticker]`).

```
┌──────────────────────────────────────────────────────┐
│ FAIR VALUE · trajectória 5Y          [1Y 3Y 5Y ALL]  │  ← header KPI
│ R$ 12.99  our_fair  consensus R$ 16.66  HOLD [cv]    │
│ ▲ our_fair +28%  · price +15%  5Y                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│   [Recharts LineChart com 3 lines + Legend]          │  ← chart
│   • our_fair (solid accent var(--accent-glow))       │
│   • consensus (dashed muted var(--text-tertiary))    │
│   • price (market color var(--mkt-br/us))            │
│                                                      │
├──────────────────────────────────────────────────────┤
│ n 16 fv computes · método graham_number ·            │  ← footer
│ últ. trigger phase_ll_full_v3                        │
└──────────────────────────────────────────────────────┘
```

## Data shape

```ts
GET /api/fair-trajectory/{ticker}?days=1825&include_price=true
→ {
    ticker, market, name, sector,
    n_trajectory: 16,    // sparse (one per fair_value compute, ~daily)
    n_prices: 251,       // dense (every trading day)
    latest: { date, action, confidence, our_fair, fair_price, ... },
    trajectory: [{date, our_fair, fair_price, action, confidence, trigger}, ...],
    prices: [{date, close}, ...]
  }
```

Component faz forward-fill de `our_fair` + `fair_price` (sparse) para a linha
ser contínua; preço é dense já.

## Known issues / slop traps observed

1. **Recharts default look** — XAxis tick formatting é PT (jan/fev/mar) mas o resto é Recharts sem customização real. Tooltip é o default Recharts shape. Cursor é dashed line. Tudo isso grita "AI dashboard genérico".

2. **Hierarquia plana entre as 3 linhas** — todas têm peso visual similar; user precisa de ler legenda para perceber qual é qual. Devia haver clear primary (our_fair, decisão), secondary (price, contexto), tertiary (consensus, referência).

3. **Header KPI strip é WSJ-like mas em vão** — copiei o pattern do PriceChart sem perguntar se faz sentido para fair value (não faz; fair não tem "abertura/fecho"; KPI strip implica price action que não é o ponto).

4. **Period tabs no canto direito** — pattern correcto mas no contexto errado. Para fair value história 5y, raramente o user quer 1Y. Default deveria ser 5Y, e tabs até 10Y / DESDE-COMEÇO.

5. **Legend Recharts native** — texto pequeno acima do chart, irrelevante para o que importa. Devia haver mini-legend inline com as labels (estilo FT *"our fair · consensus · price"* abaixo do chart com bullet do mesmo cor).

6. **Footer técnico ("n 16 fv computes · método graham_number")** — info de debug em produção. Útil para mim, mas user não decide nada com isso.

7. **No annotation markers** — quando há filing_dossier trigger, é momento importante (qualidade da empresa mudou). Devia ter um marker no chart na data do filing. Tufte: small multiples + annotation > pure line.

## Hierarchy intent (o que devia ter peso visual)

| Nível | Elemento | Peso visual ideal |
|---|---|---|
| **Primary** (decisão) | Banda BUY (price ≤ our_fair) — a área onde "comprar agora" | Highlight bg ou shaded zone |
| **Secondary** (story) | Trajectória `our_fair` ao longo dos 5y | Linha sólida espessa |
| **Tertiary** (current state) | Onde está o preço hoje vs banda | Marker grande no end-of-line |
| **Quaternary** (context) | Consensus + filings markers | Dashed line + dots |

## Density tradeoffs

- **Mobile-first**: chart funcional em 375px? Hoje provavelmente quebra (3 lines + legend + period tabs).
- **Contexto na app**: aparece no `/ticker/<TK>` page **abaixo** do FairValueStrip e **acima** do PriceChart. É a peça narrative da página — devia ter espaço para respirar (300-400px height, não 240).

## Anti-patterns explicitamente a evitar

- ❌ Recharts default tooltip
- ❌ Legend em cima do chart com texto pequeno e bullets coloridos genéricos
- ❌ KPI strip que não fala (header copiado do PriceChart)
- ❌ Footer técnico ("n 16 fv computes")
- ❌ 3 linhas com peso visual igual
- ❌ Period tabs com 1M / 3M / 6M (não fazem sentido para fair value 5y)
- ❌ Right-aligned Y axis com format(0) integers (perde casas decimais relevantes para FII NAV)

## Success metrics (anti-slop checklist)

- [ ] Olhando o componente 1 segundo, leio "ITSA4 está em BUY zone agora" ou "está em HOLD" — ação imediata
- [ ] Olhando 5 segundos, vejo a trajectória multi-anual e percebo se o nosso fair está a compor consistentemente
- [ ] Olhando 30 segundos, posso ler annotation markers e dar conta de filings importantes que mudaram nosso fair
- [ ] Mostraria este componente a um analista FT/WSJ sem ter vergonha — não parece template

## References to reach for (Sprint MM.2 deve adicionar mais)

- FT equity research charts (multi-line price + target overlay)
- Apple Stocks app multi-day comparison
- The Pudding long-form data journalism
- Datawrapper charts (range plots, confidence bands)
- *(mais refs concretas quando agent 3 — Web research — completar)*
