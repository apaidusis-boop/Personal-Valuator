---
type: macro
name: CDI — Certificado de Depósito Interbancário
category: interest_rates
country: BR
source: BCB SGS série 12 (daily)
tags: [macro, cdi, brazil, interest_rates, fixed_income]
related: ["[[Selic]]", "[[BR_stocks_tax]]", "[[BR_FIIs_tax]]"]
---

# CDI — Taxa de Referência BR

## O que é

**CDI** (Certificado de Depósito Interbancário) = taxa média de empréstimo **entre bancos** durante 1 dia útil. É o **benchmark universal** de renda fixa no Brasil.

Produtos típicos "100% CDI", "120% CDI", "CDI + 2%" — todos rastreiam esta taxa.

## Cálculo

Publicada pela **B3** e **BCB SGS série 12**. Diária. Taxa efetiva anual (252 dias úteis):

$$
CDI_{ano} = (1 + CDI_{dia})^{252} - 1
$$

## Relação com [[Selic]]

$$
CDI \approx \text{Selic meta} - 0.10\%
$$

**Por quê ligeiramente abaixo**: bancos emprestam entre si com menos risco que BCB (colateral disponível), portanto taxa levemente inferior.

**Na prática**: usar CDI e Selic como **intercambiáveis** em análise (diferença é ~10bp).

## Onde aparece

### Produtos RF directos
| Produto | Remuneração típica |
|---|---|
| **Tesouro Selic / LFT** | 100% CDI (quase) |
| **CDB bancos AAA** (Caixa, Itaú) | 100-105% CDI |
| **CDB mid-bank** | 110-115% CDI (crédito risk) |
| **LCI / LCA** | 90-95% CDI (isento IR = effective ~115% CDI after-tax) |
| **Fundo DI** | ~95-98% CDI (taxas admin) |

### Derivados
- **Swap DI** — instrumento central de hedge de taxas no Brasil
- **DI Futuro** na B3 — usado para extrair curva de juros implícita

## Como benchmark

Um **fundo bom** de renda fixa deve retornar **100% CDI líquido** após taxas e impostos.

**Regra**:
- Investimento RF < 100% CDI líquido = **destrói valor** vs alternativa trivial (Tesouro Selic)
- > 110% CDI líquido = **alpha real** (mas geralmente implica risco crédito)

## Impacto em ações

Como proxy de Selic (ver [[Selic]]), CDI alto atrai capital para RF:
- **2019-2021 CDI ~2-6%**: equity boom, FIIs +20%, IBOV 100k→130k
- **2022-2026 CDI 13-14.75%**: equity lateral, FIIs caíram, investidor migra para CDB/LCA

**Historicamente**, ações precisam retornar > CDI + risco para competir. Ratio DY / CDI é key:
- DY 7% + CDI 14% → DY real **negativo** vs cash → pressão vendas
- DY 7% + CDI 5% → DY real positivo → demanda equity

## Tributação

CDB / Tesouro Selic / Fundos DI seguem **tabela regressiva IR**:
| Prazo | Alíquota |
|---|:-:|
| ≤ 180 dias | 22.5% |
| 181-360 dias | 20.0% |
| 361-720 dias | 17.5% |
| > 720 dias | **15.0%** |

**LCI / LCA / LIG**: **isentos IRPF** para pessoa física → effective premium vs CDB.

## Cross-currency comparison

CDI BR vs Fed funds US:
- 2024: CDI 11-12% vs Fed funds 4.5-5% → **spread 6-7pp** justifica carry trade (BRL + vs USD fluctua)
- Historicamente spread > 5pp atrai capital estrangeiro → fortalece real
- Quando spread < 3pp, BRL sofre (fluxo saída)

## No nosso sistema

- `data.series` tabela: series_id='CDI_DAILY'
- Usado como **benchmark** em `analytics/backtest_yield.py`
- Fetcher: `fetchers/bcb_fetcher.py`

## Data point actual

BCB última publicação (verificar real):
- **CDI 2026-04**: ~14.65% (acompanha Selic meta 14.75%)

Consultar: `data/macro_exports/CDI_DAILY.csv` ou `ii fx --rate` indirecto.

---

> **Fontes**: Banco Central do Brasil SGS 12; B3 índices; FGV CDI series; `fetchers/bcb_fetcher.py`.
