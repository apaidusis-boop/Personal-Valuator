---
type: sector
name: Consumer Staples
region: US+BR
tags: [sector, consumer_staples, moats, defensive, dividend]
related: ["[[Buffett_quality]]", "[[Moat_types]]", "[[Aristocrats_Kings]]", "[[Dividend_Safety]]"]
holdings_us: ["[[PG]]", "[[KO]]", "[[CL]]"]
holdings_br: ["[[ABEV3]]"]
peers_staples: [PG, KO, PEP, CL, CLX, CHD, HSY, KVUE, MDLZ, GIS, K, UL]
peers_br: [ABEV3, MDIA3, JBSS3, BRFS3, NTCO3]
---

# 🛒 Setor: Consumer Staples

## Por que é a spine de DRIP US

Consumer Staples US = **disproportionate share de Dividend Aristocrats/Kings**:
- PG (68y streak — king+), KO (62y), CL (61y), HRL (58y), PEP (52y), CLX (47y), CHD (28y).
- Defensive (demand inelástica em recessão), moats brand-based.
- **Slow-but-steady compounder**: EPS growth 4-8%/y + DY 2-4% + buyback → TSR 8-13%.

## Moat typology em staples

| Moat | Como funciona | Exemplo |
|---|---|---|
| **Brand premium pricing** | Consumer paga +30% vs private label | Tide (PG), Crest (PG), KO |
| **Shelf slotting + distribuição** | Pay-to-play space + logística massiva | MDLZ cookies, PEP snacks |
| **Route-to-market DSD** | Direct-store-delivery fleet difícil replicar | KO, PEP, ABEV3 |
| **Scale economies** | Margin structural via global buying power | UL, Nestlé |
| **R&D + formulation** | Decades of tweaks proprietary | CHD Arm&Hammer, CLX germs |
| **Licensing / contract** | Concessão distribution area | ABEV3 Pepsi BR |

## Threats estruturais (bear case)

### 1. Private label (store brands)
- Walmart Great Value, Costco Kirkland, Amazon Basics.
- Share US supermarket ~20% e crescendo 1-2pp/y.
- Elasticidade cresce em inflation high (2022-23: shoppers traded down).
- **Winners defensive**: brands com loyal base + innovation cadence (Tide, Diet Coke, Oreo).
- **Losers**: segmentos commoditized (bleach, paper towels subset).

### 2. DTC / Amazon disruption
- Dollar Shave Club (Unilever acquired $1B), Harry's, Billie.
- But: physical distribution dominance ainda vale. Amazon penetration CPG stall ~10-12%.

### 3. GLP-1 weight loss drugs (Ozempic/Wegovy)
- Analyst reports 2023-24 bearish snacks/fast food (MDLZ, HSY, PEP, MCD) — users eat 30% less.
- **Reality**: impact modest so far (<3% revenue), mas tail risk 5-10y.
- [[KO]] claimed immune via brand/occasion; snacks mais vulneráveis.

### 4. Health/wellness trends
- Sugar reduction (KO shift para Coke Zero, Diet Coke).
- Protein/functional mini-trend benefits CPG adaptable.
- Processed food narrative backlash.

### 5. Inflation / margin pressure
- 2022-23 CPG players recuperaram pricing.
- 2024-25 pricing power testado — volumes decline em alguns categories.

## US peer group canonical

| Empresa | Moat | Streak | Trait distintivo |
|---|---|---|---|
| [[PG]] | Brand premium 20+ | 68y | Mega-diversified, $80B revenue, best-in-class working capital |
| [[KO]] | Route-to-market + brand | 62y | Bottler partners system, syrup concentrate IP |
| PEP | DSD + brand portfolio | 52y | Snacks (Frito-Lay) > beverage share |
| [[CL]] | Oral care global + pet | 61y | Hill's pet food growth engine; emerging mkts heavy |
| [[CLX]] | Cleaning + bleach | 47y | Post-COVID normalisation painful but complete |
| CHD | Arm&Hammer + laundry + condoms | 28y | Ponto-R&D driven innovation cadence |
| HSY | Chocolate moat | 14y (streak) | GLP-1 overhang, cocoa input cost 2024 spike |
| KVUE | Johnson spin-off OTC | 2y (new) | Tylenol, Band-Aid, Listerine — rebuilding |
| HRL (Hormel) | Meat brands + Jennie-O + Skippy | 58y | Agri cost exposure |

## Brasil staples

- **[[ABEV3]]** — Ambev, dominance cerveja (68%+ share), Pepsi licence, ethanol Latam.
- **BRFS3** — Sadia + Perdigão, avicultura + suínos, export-focused.
- **JBSS3** — JBS, largest proteín mundo, export + China exposure.
- **MDIA3** — M. Dias Branco, biscoitos/pasta #1 Brasil.
- **NTCO3** — Natura&Co (beauty, descended The Body Shop sold, turnaround play).

BR staples **menos DRIP-friendly** que US:
- ABEV3 dividendo variable + special, não aristocrat pattern.
- BRFS3 ciclo cutthroat.
- JBSS3 lucro volátil (ciclos carne).

## Métricas-chave

| Métrica | Bom |
|---|---|
| Gross margin | ≥ 45% |
| Operating margin | ≥ 18% |
| Organic revenue growth | ≥ 3% (mature), ≥ 5% (emerging market exposure) |
| Volume vs price split | Balance — all-price is red flag |
| FCF conversion | ≥ 95% net income |
| Dividend payout | 50-65% |
| Streak | ≥ 25y for aristocrat |

## Valuation benchmarks

- P/E 20-25× para maduros (PG, KO, CL).
- P/E 15-20× para struggling (CLX pós-2020, KVUE inicial).
- EV/EBITDA 15-18× healthy mature.
- DY 2.5-3.5% para well-covered aristocrats.

## Tese actual (2026)

- Inflação cooling → CPG margin recovery phase.
- Volume elasticity teste — se price-only growth stall → multiple compression.
- GLP-1 overhang específico HSY/snacks.
- PG/CL/KO core DRIP holdings defensible ao ciclo economico.
- ABEV3 BR exposure — Selic cortes aumentam consumo discretionary leve beer.

## Red flags

- Volume decline > 3% por 2+ quarters sem explicação cyclical.
- Organic growth all-price, volume negativo cronicamente.
- FCF conversion < 80% por 2y (working capital deterioration).
- Dividend payout > 75% consistente (spark corte ciclo à frente).
- Streak broken (KVUE post-spin contagious memory) → revalidar moat.

## Ferramentas

```bash
ii verdict PG --narrate            # aristocrat framework
python scripts/research.py KO      # brand + route-to-market
ii peers CL                        # vs PG/CLX/CHD percentil
python -m scoring.dividend_safety PG --streak
```

---

> Ver [[Aristocrats_Kings]] (maioria deste sector). [[Moat_types]] — brand premium = Dorsey "intangibles". [[Buffett_quality]] (KO icónica Buffett pick).
