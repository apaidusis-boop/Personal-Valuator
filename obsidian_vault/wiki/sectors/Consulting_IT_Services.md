---
type: sector
name: Consulting & IT Services
region: US+BR
tags: [sector, consulting, it_services, technology]
related: ["[[Buffett_quality]]", "[[Moat_types]]", "[[ROIC_interpretation]]", "[[FCF_yield]]"]
holdings: ["[[ACN]]"]
peers_us: [ACN, IBM, CTSH, EPAM, GLOB, INFY, WIT, TCS]
---

# 💼 Setor: Consulting & IT Services

## Business model

Três linhas de receita — mix determina qualidade:

| Linha | Margem | Cyclicality | Moat |
|---|---|---|---|
| **Strategy consulting** | 25-35% | Média | Relationship + brand |
| **IT implementation** | 10-18% | Alta | SAP/Oracle/Salesforce certs |
| **Managed services** | 15-25% | Baixa (recorrente) | Lock-in + switching cost |

**Thesis core**: mix shift → managed services = recurring revenue = stable margin.

## Peer economics (canonical)

| Empresa | Mix dominante | Margem oper | ROIC | Growth |
|---|---|---|---|---|
| **[[ACN]]** | Strategy + implementação + managed | 14-15% | 25-30% | 6-10%/y |
| IBM | Hybrid cloud + consulting (post-Kyndryl) | 10-12% | 8-12% | 0-3%/y |
| TCS | Offshore implementação massa | 25-27% | 30-40% | 4-8%/y |
| Infosys (INFY) | Offshore + digital | 20-22% | 25-30% | 5-9%/y |
| Cognizant (CTSH) | Digital + healthcare heavy | 14-16% | 15-20% | 2-6%/y |
| EPAM | Digital engineering premium | 14-18% | 18-22% | -5% a +15% (volátil) |

**Insight**: margem ACN (~14%) parece baixa vs TCS/INFY (25%+). A razão é **mix**: ACN tem 40% strategy (alta margem) mas 60% implementation/managed global (salários EUR/USD). TCS é 80%+ offshore India (salários INR) — margem bruta estrutural + 10pp.

## Drivers macro

### 1. GDP + IT spend
- Gartner IT spend growth previsto trimestralmente. Correlação 0.6-0.7 com receita Big 3.
- 2023-24: slowdown discretionary (strategy) mas managed services defensivo.
- 2026 forward: AI reinventing services line (GenAI = dev productivity 20-40%).

### 2. FX
- ACN: 60% receita USD, 25% EUR, 15% outras → FX headwind EUR/USD impactou 2023.
- TCS/INFY: receita USD mas custo INR → USD forte = margin windfall.

### 3. Bookings lag
- Bookings (contract signings) vem 2-4 trimestres antes da revenue.
- **Book-to-bill ratio** > 1.0 = growth forward; < 1.0 = shrink.
- Watch: strategy bookings declinam primeiro em slowdown.

## AI / GenAI impact

**Thesis duelo**:
- **Bear**: GenAI torna dev 30% mais productive → horas faturadas ↓ → revenue ↓.
- **Bull**: clientes precisam de **AI transformation** (data engineering, model ops, governance) — nova linha receita.
- **Realidade em 2025-26**: ACN reporta bookings AI > $3B cumulative. Net — pressure sobre classic dev but AI services > compensam.

Quem ganha:
- Empresas com **brand** (ACN, Deloitte, McKinsey-private) conseguem cobrar AI transformation premium.
- Empresas com **offshore scale** (TCS, INFY) conseguem retreinar em GenAI rapidamente.
- Empresas com **legacy outsourcing** (Kyndryl, antigas IBM) perdem — comoditizado.

## Mid-cycle vs late-cycle

- Consulting NÃO é zero-cycle. Em recessão, strategy é o primeiro corte.
- Managed services é contracíclico parcialmente (outsourcing para cut costs).
- **Historical**: ACN revenue caiu -1% em 2009; caiu 0% em 2020 COVID. Muito mais defensivo que média mas não imune.

## Métricas-chave

| Métrica | Bom |
|---|---|
| Utilization (bench) | 88-92% |
| Attrition (annual turnover) | ≤ 15% (ACN); ≤ 18% (TCS) |
| Bookings / Revenue TTM | ≥ 1.05 |
| Operating margin | ≥ 14% (Big 3) |
| ROIC | ≥ 25% |
| FCF conversion | ≥ 100% net income |
| Dividend streak | ≥ 10y (ACN aristocrat-track) |

## Tese ACN actual (2026)

- **Pros**: ROIC 27%, dividend streak consistente (desde IPO 2001), managed services ~50% mix, AI bookings momentum.
- **Cons**: EUR exposure 25%, strategy bookings soft 2023-24, GenAI cannibalization inside own services (clients DIY).
- **Peer premium**: ACN trades at 25-30× P/E vs TCS 25× vs IBM 20× — premium justificado por mix + growth?

Ver memória `user_investment_intents.md` — ACN é intent-compounder (não DRIP puro).

## Red flags

- Bookings < revenue TTM por 3+ quarters → shrink incoming.
- Attrition > 20% → cost to replace + skill gap.
- Utilization < 85% → excess bench = margin drag.
- Big client concentration (> 10% receita) → 1 perda devastadora.
- GenAI spending > revenue growth (capex sem ROI).

## Ferramentas

```bash
python scripts/research.py ACN            # memo PT + FCF + FY outlook
python scripts/research.py ACN --intraday # com preço live
ii verdict ACN --narrate                  # Verdict BUY/HOLD/SELL + rationale
ii peers ACN                              # percentil vs CTSH/IBM/EPAM
```

---

> Ver [[Buffett_quality]] (ACN exemplo — quality over deep value). [[ROIC_interpretation]] para entender por que ACN 27% é extraordinário.
