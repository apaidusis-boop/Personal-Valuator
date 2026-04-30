---
type: sector
name: Semiconductors
region: US+Global
tags: [sector, semiconductors, tech, cyclical, growth]
related: ["[[Buffett_quality]]", "[[Moat_types]]", "[[Semi_cycle]]", "[[FCF_yield]]"]
peers_us: [NVDA, AMD, TSM, INTC, AVGO, MU, AMAT, LRCX, KLAC, ASML, QCOM]
source_class: derived
confidence: 0.7
freshness_check: 2026-04-30
---

# 🔌 Setor: Semicondutores

## Stack da indústria

### Design puro (fabless)
Desenha chip, não fabrica. Depende de foundries.
- [[NVDA]] — GPU/AI (monopólio CUDA).
- [[AMD]] — CPU/GPU (concorrente Intel + NVDA).
- [[QCOM]] — mobile SoC (Snapdragon, modem).
- Broadcom [[AVGO]] — hybrid (design + VMware software).

### Foundry (fabricação pura)
Fabrica chip para fabless.
- [[TSM]] (TSMC) — 55%+ world foundry share, líder 3nm/2nm.
- Samsung Foundry — #2, lagging em nodes avançados.
- GlobalFoundries (GFS) — mature nodes.
- Intel Foundry Services (nascent, IFS initiative).

### IDM (integrated device manufacturer) — fabless+foundry combinado
- [[INTC]] — CPU x86 dominant erosão → foundry turnaround play.
- Samsung Electronics — memory + logic foundry.
- Micron [[MU]] — memory DRAM+NAND only.
- SK Hynix — memory.
- Texas Instruments [[TXN]] — analog.

### Equipment (semi cap)
Faz as máquinas.
- [[ASML]] — EUV lithography **monopólio** (1 fabricante globally).
- Applied Materials AMAT, Lam Research LRCX, KLA KLAC, Tokyo Electron.

### EDA (design software)
- Synopsys [[SNPS]], Cadence [[CDNS]], Siemens EDA — tooling moat massivo.

## Moat ranking (subjective)

| Empresa | Moat | Tipo |
|---|---|---|
| ASML | 🏰🏰🏰🏰🏰 | Monopólio EUV |
| TSMC | 🏰🏰🏰🏰 | Process node lead, capex $30B+/y |
| NVDA | 🏰🏰🏰🏰 | CUDA ecosystem + silicon |
| Synopsys/Cadence | 🏰🏰🏰🏰 | EDA tool switching cost |
| Broadcom | 🏰🏰🏰 | Sticky custom silicon + VMware |
| AMD | 🏰🏰 | Zen architecture, datacenter share |
| Intel | 🏰🏰 (erosion) | x86 legacy + foundry aspiration |
| Micron | 🏰 | Commodity memory (brutal cycles) |

## O ciclo semi (~3-4y)

### Fase 1 — Shortage / boom
- Fabs ao limite capacity → lead times 6-12m.
- Capex anunciado massively → TSMC 2020-22 $100B+ cumulative.
- Sellers dictate pricing — AVG ASP ↑.
- **Exemplo**: 2020-2022 pandemic-era shortage.

### Fase 2 — Capacity chegando
- Novas fabs coming online (2 anos após announcement).
- Demand normaliza post-bubble.
- Inventários nos clientes built-up.
- **Exemplo**: 2H 2022-2023.

### Fase 3 — Oversupply / correção
- Inventários altos clientes → ordem de chips despenca.
- ASP caem, utilization cai.
- Memory primeira (DRAM/NAND) — Micron, SK, Samsung sofrem.
- **Exemplo**: 2023 (Micron perdeu 30% revenue).

### Fase 4 — Consolidação / recovery
- Fabs mothball projects, capex slash.
- Leaner supply → demand recovers → next shortage setup.
- **Exemplo**: 2024 recovery → 2025 AI-driven super-cycle.

## AI supercycle (2023-presente)

- [[NVDA]] 80%+ datacenter GPU share, margins bruto 75%+.
- ASML EUV order book backlog multi-year.
- TSMC N3/N2 fully booked 2025-2027 (AI customers).
- Memory (HBM3/HBM4 stack on logic) → Hynix/Micron beneficiam.
- Winners claros: NVDA, ASML, TSM, AVGO (custom silicon Meta/Google), HBM memory.
- Losers relativos: INTC (perdendo datacenter share), pure CPU plays.

**Risk**: AI capex sustainability. Hyperscaler capex cresceu $200B+ em 2024 — se training demand stutter, primeira ronda inventory pile acima NVDA.

## Taiwan risk

TSMC é **~92% logic leading-edge production** mundial.
- Geopolítica China-Taiwan = supply chain single point of failure.
- US CHIPS Act $52B → TSM Arizona, Intel Ohio, Samsung Texas — diversificação multi-anos.
- **Ainda**: disruption real Taiwan = mercado global de chips -70% nearshore.

## Capital intensity

Semi é **the most capital intensive industry após energy**.
- Fab 3nm custa $20-30B. 2nm vai $30-40B.
- Depreciação brutal → FCF negativo em expansion years.
- **TSMC capex/revenue** historically 30-40%. Compare ACN ~3%.

## Valuation nuance

| Metric | Aplicação |
|---|---|
| P/E | Útil em steady-state, distorced em shortage (peak earnings) |
| P/S | Útil para growth (NVDA, ASML) |
| EV/EBITDA | Melhor em IDM (captura depreciation) |
| FCF yield normalised | Key — FCF em peak vs trough |
| ROIC ex-cash | TSMC historical 20-25%; NVDA 40%+ recente |

**Trap comum**: compre em peak P/E baixo (earnings inflados) → cycle turns → P/E balloon as earnings crash. Sempre usar **normalised earnings** em semi.

## Dividend profile

- **AVGO**: aristocrat-track, alto payout (~45%), DY ~1-2% + buyback.
- **TXN**: analog aristocrat, 20+ years consistent raises.
- **QCOM**: steady dividend + buyback.
- **NVDA**: minimal dividend (mas massive buyback).
- **TSM**: ~2% DY, steady.
- **INTC**: **cortou** 2023 — distressed recovery.

Semi is **NOT a DRIP core** genericamente — só specific names (AVGO, TXN, QCOM).

## Red flags

- Inventory days > 120 sector-wide → correction imminent.
- ASP declining + capex increasing → double whammy.
- Customer concentration (NVDA revenue 40%+ top-3 hyperscalers).
- Geopolítica escalation China-Taiwan.
- Capex / revenue > 40% + FCF negative > 2y.

## Tese actual (2026)

- AI infra build-out mid-cycle. NVDA margins em peak (sustentabilidade?).
- ASML trade tem EUV backlog 2027+ (limited supply).
- Memory (MU, Hynix) em up-cycle HBM.
- INTC foundry turnaround tese high-variance.
- Consumer electronics (smartphone, PC) tepid.

## Ferramentas

```bash
ii verdict NVDA --narrate         # AI exposure assessment
ii peers TSM                      # vs foundry peers
python scripts/research.py AVGO   # dividend aristocrat track
```

---

> Ver [[Semi_cycle]] para timing framework. [[Buffett_quality]] para moat ranking. [[Moat_types]] — ASML exemplo de "monopólio regulamentado de facto".
