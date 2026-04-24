---
type: sector
name: Pulp & Paper
region: BR+Global
tags: [sector, pulp, paper, commodity, cyclical, export]
related: ["[[Pulp_cycle]]", "[[USDBRL_PTAX]]", "[[DCF_simplified]]"]
holdings_br: ["[[SUZB3]]", "[[KLBN4]]"]
peers: [SUZB3, KLBN4, FIBR3 (merged), IP, WRK, PKG, UPM, STERV, MERC]
---

# 🌲 Setor: Pulp & Paper

## Produto espectro

| Tipo | O que é | Clientes | Cyclicality |
|---|---|---|---|
| **Pulp de fibra curta (BEKP — eucalipto)** | Celulose branqueada hardwood | Tissue, papéis escritório | Alta |
| **Pulp de fibra longa (NBSK — pinho)** | Softwood longa, resistência | Packaging, tissue premium | Alta |
| **Papel/papelão ondulado (corrugated)** | Caixas | E-commerce, industrial | Média |
| **Papel imprimir/escrever** | A4, livros | Editoras, escritório (secular decline) | Alta |
| **Papel tissue** | Toalha, papel higiénico | Varejo | Baixa |
| **Embalagem food-grade** | Cartões boreal | Alimentos | Baixa |

**Brasil leader mundial BEKP** — Eucalipto cresce em 7 anos vs 25 anos pinho no Hemisfério Norte → custo produção mais baixo do mundo.

## Players-chave

### Brasil (producer)
- [[SUZB3]] (Suzano) — #1 global BEKP, maior fabricante pulp mundo, $5B+ EBITDA peak.
- [[KLBN4]] (Klabin) — integrado papelão + pulp + sacos (Brasilcomércio focused).
- Bracell (privada), Eldorado (privada, sob litígio).
- Veracel (joint SUZB+Stora Enso).

### US/Canadá (paper-focused)
- International Paper (IP) — corrugated + pulp.
- WestRock (WRK) — corrugated (mergeada com Smurfit Kappa → Smurfit Westrock 2024).
- PackagingCorpAmerica (PKG).
- Domtar (privada pós-Paper Excellence).

### Nórdicos (integrated pulp+paper)
- UPM, Stora Enso, Metsä.
- Vantagem histórica em NBSK + integration downstream.

## Drivers de preço (BEKP)

### Demand
- **China ~60% da demanda mundial BEKP**. Spot prices em Xangai (tracks Europe -2/+3 semanas).
- Demografia: tissue growth 3-5%/y global, 8%/y emerging.
- E-commerce packaging: +5-10%/y growth.
- Paper scriptual decline: -3 a -5%/y (secular).

### Supply
- Capacity additions multi-year (mill new $2-3B, ramp 2-3y).
- **Brownfield expansions SUZB** (Cerrado 2024: +2.5Mt) → supply shock.
- Logistic: navio capesize + LNG + Suez/Panama bottlenecks.

### Preço histórico BEKP China (CFR)
- 2009: $450/t (crise)
- 2011: $850/t (peak)
- 2016: $430/t (bottom)
- 2018: $790/t (peak)
- 2020: $450/t (COVID)
- 2022: $850/t (peak)
- 2023-24: $500-650/t range
- 2025: rally $750+ tight supply

**Thumb rule**: $500 = soft landing; $700+ = boom; $900+ = peak; < $450 = stress (marginal producers negative cash).

## Economia SUZB3 (canonical)

- **Produção 10-11Mt/y BEKP** pós Cerrado.
- **Cash cost ~$170-200/t** (mais baixo mundo).
- **Breakeven** ~$350/t (all-in incluindo capex manutenção).
- **FCF @ $700/t** = EBITDA $5B → FCF $3B+ após capex.
- **FX leverage**: 100% receita USD, 80% custo BRL → USD↑ ou BRL↓ = margin windfall massive.

### SUZB3 vs KLBN4 positioning
- SUZB3 é **pure-play pulp** commodity + FX.
- KLBN4 é **mais estável** — 50% packaging (doméstico BRL, pricing power), 50% pulp export.
- KLBN4 DY mais consistente; SUZB3 DY spikes em peak.

## Análise normalised

**Nunca valuation em peak earnings**.
- SUZB3 peak: $5-6B EBITDA; trough: $2-3B.
- Mid-cycle: $3.5-4.5B.
- EV/EBITDA mid-cycle 5-7× para ciclos commodity BR.

## FX como driver dominante

- USD/BRL $1 movimentado = ~2-3% EBITDA impact SUZB3.
- PTAX a R$ 5.00 vs R$ 5.80 = diferença material.
- Hedge accounting: SUZB usa NDF (non-deliverable forwards) com dívida USD (natural hedge).
- **Inversão lógica**: BRL weak pode ser bom para SUZB3 mesmo com pulp price flat.

## Sustentabilidade

- Certificação FSC ~90% plantação brasileira.
- Carbon-negative claims (eucalipto sequestra > emit).
- EUDR (EU Deforestation Regulation 2024-25): impact low — BR já compliant ampliado.
- Water consumption mill criticizada; novas mills closed-loop reduziram 40%.

## Red flags

- Net debt / EBITDA > 3× em peak cycle → dilution risk (emissão) em próximo downturn.
- China stockpile building (indicator: Xangai port inventory) → preço cair soon.
- New supply > 5Mt/y next 24m combined → prolonged oversupply.
- Papel imprimir share > 30% portfolio (secular decline).

## Tese actual (2026)

- [[SUZB3]] Cerrado 2024 startup creates supply pressure mas tight shipping + China demand absorb.
- BEKP spot $750-800 → SUZB3 FCF robust.
- KLBN4 mais defensivo, papelão pricing recuperado pós-2023 destocking.
- FX BRL fraco (~R$ 5.80) é tailwind estrutural.
- **Risk**: China deflation deepening → paper demand fall.

## Métricas-chave

| Métrica | SUZB3 | KLBN4 |
|---|---|---|
| Cash cost / t | $170-200 | higher (smaller scale) |
| ND / EBITDA target | ≤ 2.5× | ≤ 3.0× |
| Payout | 25-40% peaks | 50-60% steady |
| Dividend streak | Irregular (special divs) | Consistent |
| FX leverage | 100% USD receita | 50% USD receita |

## Ferramentas

```bash
python scripts/research.py SUZB3    # memo + FX sensitivity
ii verdict KLBN4 --narrate          # packaging vs pulp mix
python scripts/compare_tickers.py SUZB3 KLBN4 UPM
```

---

> Ver [[Pulp_cycle]] para framework timing. [[USDBRL_PTAX]] — crucial SUZB3. [[DCF_simplified]] para normalised FCF.
