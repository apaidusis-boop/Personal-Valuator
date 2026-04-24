---
type: wiki_section_index
name: Holdings thesis — section index
tags: [wiki_index, holdings]
---

# 🎯 Holdings — Thesis Deep-dives

> Uma tese canónica por holding. Complementa `tickers/<X>.md` (auto-gerado pelo bridge com fundamentals) com o **"porquê detemos"**: intent, moat, invalidation, sizing, peer comparison.

## Convenções

Cada nota tem `type: holding_thesis` + frontmatter:
- `ticker` — símbolo
- `intent` — **DRIP_core** · **DRIP_cyclical** · **DRIP_hedge** · **DRIP_income** · **Compounder** · **Growth** · **Tactical_contrarian** · **EXIT_PENDING**
- `related` — wiki links (sector, cycle, playbooks)

## BR holdings (5 com thesis deep)

| Ticker | Intent | Sector |
|---|---|---|
| [[ITSA4]] | DRIP core | Holding (Itaú via holdco) |
| [[BBDC4]] | DRIP core | Banks (Bradesco deep-value) |
| [[PRIO3]] | Compounder | Oil & Gas (E&P growth) |
| [[VALE3]] | DRIP cyclical | Mining (ferro + USD) |
| [[PVBI11]] | Tactical contrarian | FII corporativo turnaround |
| [[BTLG11]] | DRIP core | FII logística |
| [[VGIR11]] | DRIP hedge | FII papel CRI (anti-Selic) |
| [[XPML11]] | DRIP cyclical | FII shopping |

## US holdings (core quality)

| Ticker | Intent | Notes |
|---|---|---|
| [[JNJ]] | DRIP core | Dividend King 62y, pharma + MedTech |
| [[KO]] | DRIP core | Dividend King 62y, brand moat |
| [[PG]] | DRIP core | Dividend King 68y, longest streak S&P |
| [[JPM]] | DRIP core | Best-in-class US bank |
| [[BLK]] | Compounder | Asset manager + Aladdin moat |
| [[BN]] | Growth | Brookfield holdco post-split 2023 |
| [[BRK-B]] | Compounder | Berkshire, buy-and-die |
| [[ACN]] | Compounder | Consulting + AI services |
| [[O]] | DRIP income | Monthly dividend REIT |
| [[TSM]] | Compounder | Foundry #1 + Taiwan risk |
| [[AAPL]] | Compounder | Ecosystem + services |
| [[PLD]] | DRIP income | Industrial logistics REIT |
| [[HD]] | DRIP core | Home improvement, Pro channel |
| [[NU]] | Growth | BR fintech listed US |
| [[TEN]] | **EXIT_PENDING** | ⚠️ Shipping peak — SELL memo |

## Holdings sem thesis note ainda (pending)

BR: —

US: ABBV · BRK-A (via B) · GREK (tactical memory doc only) · GS · PLTR · TSLA · XP

Estas podem não precisar thesis completa — memo curto `notes_cli` suffice. Ou criar em sessão posterior se a tese merecer wiki-level depth.

## Como usar

- **Quando reforçar / trimar uma posição** → ler thesis primeiro (confirma invalidation não foi tocada)
- **Quando Selic / Fed / macro muda** → revisitar secção "Current state" + "Invalidation triggers"
- **Quando adicionar novo holding** → criar nova nota seguindo template desta secção

## Template recomendado

```yaml
---
type: holding_thesis
ticker: <X>
market: br|us
sector: <sector>
intent: <DRIP_core|Compounder|Growth|...>
tags: [holding, thesis, <market>, ...]
related: [<wiki sector>, <wiki cycle>, <playbooks>]
---
```

Secções padrão:
- Intent
- Business snapshot
- Por que detemos (3-5 razões)
- Moat (com weak points)
- Current state (2026-XX-XX)
- Invalidation triggers (checklist)
- Sizing + expected path
- Peer comparison
- Related

## Related wiki

- [[wiki/Index|Wiki — Finance Map]]
- [[wiki/playbooks/Buy_checklist]]
- [[wiki/playbooks/Sell_triggers]]
- [[wiki/playbooks/Rebalance_cadence]]
