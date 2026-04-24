---
type: sector
name: Oil & Gas
region: Global
tags: [sector, oil, energy, cyclical, commodity]
related: ["[[Brent_WTI]]", "[[DCF_simplified]]", "[[Dividend_Safety]]", "[[Oil_cycle]]"]
holdings_br: ["[[PETR4]]"]
holdings_us: ["[[CVX]]"]
peers_us: [XOM, CVX, COP, OXY, EOG, HES, TTE, SHEL, BP]
peers_br: [PETR4, PRIO3, RECV3, BRAV3]
---

# 🛢 Setor: Oil & Gas

## Stack vertical

| Segmento | Fluxo | Preço driver | Margin volatility |
|---|---|---|---|
| **Upstream** (E&P) | Extrai | Brent/WTI spot | Extrema |
| **Midstream** | Transporta/armazena | Tarifa volumétrica | Baixa (toll road) |
| **Downstream** (refino) | Refina + varejo | Crack spread | Alta (contracíclico parcial) |
| **Integrado (major)** | Up+Mid+Down | Mix | Média (natural hedge) |

Majors integrados: [[XOM]], [[CVX]], Shell, BP, TotalEnergies, [[PETR4]].
US E&P puro: COP, OXY, EOG, HES, PXD (adquirida), CTRA, DVN, CHK.
BR E&P independente: PRIO3, RECV3, BRAV3 (ex-3R).

## O ciclo canónico

### Fase 1 — Discovery / boom (ex: 2003-2008, 2021-2022)
- Brent > $80, incentivo a capex.
- Rigs activos ↑ rapidamente (Baker Hughes rig count).
- Supply cresce lagged 12-18m.
- FCF yield compressed por reinvestimento.

### Fase 2 — Oversupply / correção (2014-2016, 2020, 2023)
- Supply cresce > demand → estoques ↑ → preço ↓.
- Breakeven pressured: shale US $35-45/bbl, Brazilian pré-sal $20-30/bbl, Saudi land $10-15/bbl.
- **Rig count colapsa**, capex slash.

### Fase 3 — Discipline / consolidation (2017-2019, 2023-presente)
- Majors focam FCF + dividend + buyback em vez de reinvest.
- M&A: Exxon+Pioneer ($60B, 2023), Chevron+Hess ($53B, 2023), Occidental+CrownRock (2024).
- CAPEX disciplined ≤ 50% FCF → dividend + buyback sobem.

### Fase 4 — Supply response delayed (presente 2026)
- Underinvest 2015-2020 prepara shortage 2025-2028.
- OPEC+ spare capacity crucial (Saudi, UAE).
- Geopolítica: Russia war, Iran sanctions, Venezuelan reprieve modulam.

## Brent drivers

### Demand
- China PMI / manufacturing (40% demand marginal).
- Global GDP growth (elasticidade 0.8).
- EV penetration — começa a morder demand LEVE (carros) mas jet/marine/petchem imunes décadas.

### Supply
- OPEC+ production quotas (Saudi voluntário cut 1Mbd 2023-24).
- US shale (produção breakeven $45-55 atual).
- Brazilian pré-sal growth (PETR4 aim 3.3-3.9Mbd 2028).
- Venezuelan + Iran (geopolítica).

### Geopolítica eventos
- Hamas-Israel war 2023 → risk premium.
- Russia SPR drawdown 2022 agora revertendo.
- Strait of Hormuz threats (Iran).

## Métricas-chave upstream

| Métrica | Bom |
|---|---|
| Breakeven / bbl | < $40 (tier 1) |
| Reserves replacement ratio | ≥ 100% |
| Debt / EBITDA | ≤ 1.5× peak cycle |
| Free cash flow yield @ $70 Brent | ≥ 10% |
| Dividend + buyback / cash flow | 50-70% |
| Decline rate (shale) | 30-40% year-1 |

## Majors vs E&P puro — para DRIP

### Majors integrados ([[CVX]], [[XOM]]) — aristocrats
- **Resilience** via refino/química/midstream.
- Dividend aristocrat (XOM 40y+, CVX 35y+).
- Mesmo em Brent $30 mantiveram dividendo (2020) — streak intacta.
- Capex disciplina post-2016 — CEO memo Chevron explicito "capital discipline over barrel growth".
- **Drawback**: cap growth is slow (produção flat-up 1-3%/y).

### E&P puro (COP, EOG, OXY)
- **Direct play** no crude price.
- Dividendos variáveis (COP tem base + variable; EOG base + special).
- Risk Brent crash pode suspender variable dividend.
- Upside mais alto em Brent rally.

### PETR4 caso especial
- Quasi-estatal → risco intervenção (paridade importação, dividend policy).
- Mas dividend 2022-23 foi o maior cash yield mundial (DY 30%+).
- Política interferiu 2023-24 (Prates management, payout ajustado).
- Pré-sal baixo breakeven (< $30) = ativo mundial classe.

### PRIO3
- E&P independente BR (Polvo, Tubarão Martelo, Frade + new fields).
- Break-even ~$20-25 (brownfield revitalization).
- **Growth play**, não DRIP — capex heavy.

## Tese actual (2026-04)

- Brent ~$75-85 range, OPEC+ holding discipline.
- Majors em "cash return" mode → atractive DRIP.
- [[CVX]] + Hess deal agrega portfolio Guyana (growth orgânico).
- Risk supply-side (Russia/Iran) mantém premium ~$10/bbl.
- [[TEN]] signal (ver memory `ten_distress_signal.md`) sugere cycle peak em drybulk/tanker shipping — **não** aplica directamente a oil E&P, mas correlação de sentiment em transport cabe vigilância.

## Red flags

- Debt/EBITDA > 2× + Brent caindo = dividend em risco.
- Reserve replacement < 80% por 2+ anos = depleção mask.
- Capex > FCF cronicamente = boom-bust incoming.
- Dividend declarado antes capex committed = accounting trick.
- Quasi-estatal (PETR4, PEMEX, Saudi Aramco) — risco interferência.

## Ferramentas

```bash
ii verdict CVX --narrate                 # aristocrat + mix analysis
python scripts/research.py PETR4         # memo com DY + payout + política
ii peers CVX                             # vs XOM/COP/OXY percentil
python -m scoring.altman PETR4           # distress check
```

---

> Ver [[Brent_WTI]] para benchmarks. [[Dividend_Safety]] score com payout volatility. [[Oil_cycle]] framework cyclical.
