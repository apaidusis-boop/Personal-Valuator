---
type: macro
name: IPCA — Inflação oficial BR
category: inflation
country: BR
source: IBGE (mensal)
tags: [macro, ipca, inflation, brazil]
related: ["[[Selic]]", "[[USDBRL_PTAX]]", "[[IGP_M]]", "[[BR_inflation_history]]"]
---

# IPCA — Índice de Preços ao Consumidor Amplo

## O que é

Índice oficial de inflação do Brasil. Medido pelo **IBGE** mensalmente. É a **meta perseguida pelo BCB** em política monetária.

## Metodologia

### Coleta
- Universo: famílias com **renda 1-40 salários mínimos** em 10 regiões metropolitanas (SP, RJ, BH, Salvador, Fortaleza, Recife, POA, Curitiba, DF, Goiânia) + Rio Branco
- ~10.000 empresas visitadas mensalmente
- ~500.000 preços coletados
- Período: entre dias 1 e 30 de cada mês (ref. mês anterior)
- Publicação: meados do mês seguinte (10-15)

### Ponderações
Grupos (ponderação aprox 2024):
- **Alimentação e bebidas** 19%
- **Transportes** 19%
- **Habitação** 15%
- **Saúde e cuidados pessoais** 13%
- **Despesas pessoais** 11%
- **Educação** 7%
- **Vestuário** 5%
- **Comunicação** 5%
- **Artigos de residência** 4%

## Componentes úteis em análise

### Núcleo (core IPCA)
BCB calcula vários "núcleos" excluindo itens voláteis:
- **IPCA EX-3**: exclui alimentos no domicílio + energia/combustíveis + monitorados
- **MS (média aparada)**: tira os 40% mais extremos (20% cada lado)
- **DP (dupla ponderação)**: remove volatility statisticamente

**Serviços** core = **sticky inflation** (mais relevante para BCB).

### Monitorados (preços administrados)
Gasolina, energia elétrica, transporte público, planos de saúde — reguladores definem. Representa ~25% do IPCA.

## Meta de inflação

Definida pelo **CMN** (Conselho Monetário):
| Ano | Meta | Realizado |
|---|:-:|:-:|
| 2020 | 4.00% | 4.52% |
| 2021 | 3.75% | **10.06%** (pós-COVID choc commodities) |
| 2022 | 3.50% | 5.79% |
| 2023 | 3.25% | 4.62% |
| 2024 | 3.00% | ~4.5% (miss) |
| 2025 | 3.00% | ~4.0%? |
| 2026 | 3.00% | expectativa ~4% (ainda above target) |

**Banda ±1.5pp**. Se IPCA > 4.5% (centro 3 + 1.5), BCB deve carta ao Ministro Fazenda explicando.

## Efeito em ações

### Setores beneficiados inflação alta
- **Banks** (JPM/BR): NIM alarga em ciclo hike
- **Utilities** com reajuste IPCA (TAEE11, ISAE4 — contratos indexados)
- **Real estate / FII logística** (contratos com IPCA + spread)
- **Commodity exporters** (BR real desvaloriza → receita USD fica sob pressão mas ainda positiva)

### Setores sacrificados
- **Consumer discretionary** (MGLU3, VIIA3) — consumidor squeezed
- **Construção civil** (MRVE3): juros alto mata demanda + custos sobe
- **Small caps** alavancadas

## IPCA vs IGP-M

**IGP-M** (FGV — Índice Geral de Preços do Mercado):
- Pondera **atacado** (mais sensível a câmbio), **construção**, **consumidor**
- Usado em **aluguel** tradicionalmente (contratos típicos "IGP-M + X%")
- Volatilidade MUITO maior (23% em 2021!)

**IPCA** é mais estável, reflecte consumidor final puro.

## Como interpretar números mensais

**IPCA mensal** (mês a mês):
- 0.2-0.4% = baixo (anualizado 2.5-5%)
- 0.5-0.7% = fair (anualizado 6-9%)
- > 0.8%/mês = hot (anualizado > 10%) — BCB reaccionário

**IPCA 12m** (mais usado para meta):
- Trajetória suave; inflação sticky leva meses a descer.

**Expectativa Focus** (BCB):
- Mercado expectativa 1/2/3 anos à frente publicada semanalmente (`focus.bcb.gov.br`)
- Útil para prever próximos movimentos Copom

## Impacto nos nossos holdings

| Ticker | Sensibilidade IPCA |
|---|---|
| [[BBDC4]], [[ITSA4]] | Positivo (NIM alarga) |
| [[VALE3]] | Neutro (exporta commodity em USD) |
| [[TAEE11]], [[ISAE4]] | Positivo (reajuste contratos) |
| [[PETR4]] | Complexo (hedge fuels vs preços domésticos) |
| [[XPML11]] | Negativo (vacância up, contract reset) |

## No nosso sistema

- `data.series` tabela: series_id='IPCA_MONTHLY' (mensal)
- Fetcher: `fetchers/bcb_fetcher.py`
- Usado em `analytics/regime.py` para classificar regime BR

---

> **Fontes**: IBGE (ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html); BCB Focus Report; FGV IBRE; nosso fetcher `fetchers/bcb_fetcher.py`.
