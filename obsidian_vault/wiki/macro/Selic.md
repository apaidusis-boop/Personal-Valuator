---
type: macro
name: Selic — Taxa Básica BR
category: interest_rates
country: BR
source: BCB SGS série 11 (daily), 432 (meta)
tags: [macro, selic, brazil, interest_rates, copom]
related: ["[[CDI]]", "[[IPCA]]", "[[USDBRL_PTAX]]", "[[Real_rates_history]]", "[[Selic_history]]", "[[Banks_BR]]"]
source_class: derived
confidence: 0.7
freshness_check: 2026-04-30
---

# Selic — Taxa Básica de Juros BR

## O que é

Taxa **overnight** à qual o Banco Central do Brasil (BCB) empresta a bancos e compra/vende títulos públicos no mercado aberto. É o **benchmark** de todo o custo do dinheiro no Brasil.

## Componentes

### Selic meta
Definida pelo **Copom** (Comité de Política Monetária do BCB) em reuniões a cada **45 dias**. É a meta-alvo da taxa overnight. Publicada em BCB série 432.

### Selic efectiva
Taxa **realmente** praticada no mercado diariamente. Geralmente ~5-10bp abaixo da meta. Publicada em BCB série 11.

## Copom — estrutura

- **8 reuniões/ano** normalmente
- **8 membros** votam (presidente + 7 diretores)
- Decisão por **maioria**; atas publicadas ~1 semana depois
- **Forward guidance** cada vez mais importante (2019+)

## Mandato

**Meta de inflação** (definida pelo CMN — Conselho Monetário Nacional, não BCB):
- Centro: 3.0% IPCA/ano (desde 2024; antes 3.25% / 3.5% / 4.5% dependendo do ano)
- Intervalo: ±1.5pp (flexibilidade)

BCB pode perder meta — mas se perder, precisa carta ao Ministro da Fazenda justificando.

## Relação com [[CDI]]

$$
CDI \approx \text{Selic meta} - 0.10\%
$$

CDI é taxa de empréstimo interbancário (DI), rastreia Selic quase 1:1. **Benchmark renda fixa no Brasil** (100% CDI = produto básico).

## Relação com renda fixa / ações

### Renda fixa
- **Selic sobe** → title públicos +, prefixados ↓, pós-fixados (Tesouro Selic / LFT / LFTB11) estáveis
- **Selic desce** → prefixados ↑ (ganho capital)

### Ações
**Selic alta** (como 2023-2026 em 13-14.75%):
- Risk-free alto → equity risk premium comprimido → multiples mais baixos
- Dinheiro "safe" em RF atrai capital
- **FIIs** particular sofrem (competição directa 8% CDI vs DY FII)
- **Bancos** beneficiam NIM (spreads alargados)

**Selic baixa** (como 2019-2021 em 2-4%):
- Boom equity (busca por yield)
- FIIs em alta
- Consumer cyclicals beneficiam (crédito barato)

## Histórico rápido (ver [[Selic_history]])

| Ano | Selic média | Contexto |
|---|:-:|---|
| 1999 | 26% | Regime flutuante início, crise LatAm |
| 2003 | 25% | Meta inflação adopted |
| 2010 | 10% | Lula II boom commodities |
| 2015 | 14% | Dilma crisis |
| 2020 | 2% | **LOW HISTÓRICO** COVID |
| 2022 | 13.75% | Pós-COVID tightening |
| 2024-2026 | 13-15% | Sticky inflation + fiscal concerns |

## Como consultar

### APIs
- **BCB SGS**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json`
- No nosso sistema: `fetchers/bcb_fetcher.py` puxa diariamente

### Dashboards
- BCB Copom schedule: `bcb.gov.br/controleinflacao/historicotaxasjuros`
- Nosso: `data/macro_exports/SELIC_META.csv`

## No nosso sistema

- `data.series` tabela: series_id='SELIC_META' + 'SELIC_DAILY'
- `analytics/regime.py`: Selic nivel é input do classificador (hawkish vs dovish)
- `scripts/research.py`: secção [7] Regime macro contextualiza

## Copom calendar 2026 (aprox)

Reuniões tipicamente Jan, Mar, Mai, Jun, Ago, Set, Nov, Dec. Verificar calendário actualizado em bcb.gov.br.

---

> **Fontes**: Banco Central do Brasil (bcb.gov.br); Copom minutes; BCB Relatório de Inflação trimestral; Valor Económico / Poder360 para análise; nosso fetcher `fetchers/bcb_fetcher.py`.
