---
type: macro
name: USDBRL PTAX — Câmbio oficial
category: currency
country: BR
source: BCB SGS série 1 (daily)
tags: [macro, usdbrl, ptax, forex, brazil]
related: ["[[Selic]]", "[[IPCA]]", "[[Brazilian_inflation_hist]]", "[[Fed_funds]]"]
---

# USDBRL PTAX — Câmbio oficial USD/BRL

## O que é

**PTAX** = taxa de câmbio de **referência** oficial do Banco Central, calculada a partir de consultas a dealers authorizados às 16:00 (horário BR).

Publicada em **BCB SGS série 1** ao fim do dia.

## Cálculo (PTAX final = D0 close)

1. BCB consulta 4 dealers em **4 momentos do dia** (10h, 11h, 13h, 15h + final 16h)
2. Em cada momento: remove extremos (20% maior, 20% menor) → calcula **média aritmética**
3. PTAX **venda** = média dos preços venda; **compra** = média dos compra

**Spread típico** ~5 basis points.

Usado como referência em:
- Fundos FICFIM multimoeda
- Contratos importação/exportação
- Declaração IR (valor de referência)
- ETFs cambiais (IVVB11 tracking CDI + PTAX)

## Regime cambial BR

### Pré-1999: cambial fixo / banda
Diversos regimes (crawling peg, banda cambial) — crises recorrentes.

### **Janeiro 1999: flutuação suja**
Armínio Fraga (BCB) abandona banda. Real passou de 1.20 → 1.70 em 1 mês.

### Pós-1999: float com intervenção
- BCB intervém **esporadicamente** em stress (leilões de dólar)
- Core: deixar flutuar
- Política fiscal + Selic são âncoras

## Drivers do USD/BRL

### 1. Differential de juros ([[Selic]] vs [[Fed_funds]])
- Selic 14% - Fed funds 5% = **carry 9pp** → atrai capital estrangeiro → BRL forte
- Carry < 3pp = BRL frágil

### 2. Preços de commodities
- Boom commodity 2003-2011 → BRL 4.0 → 1.55 (USD collapse)
- Bear commodity 2014-2016 → BRL 2.2 → 4.2
- BR é grande exportador de minério + soja + petróleo

### 3. Risco fiscal BR
- Dívida/PIB trajectória: ascendente = BRL vulnerable
- Meta fiscal credível = BRL estável
- 2024-2026: ruído fiscal constante → BRL em 5-5.5 range

### 4. Dólar global (DXY)
USD vs basket (EUR, JPY, GBP, CAD, SEK, CHF). DXY up → BRL sofre mesmo se fundamentals BR OK (risk-off global).

## Faixas históricas

| Ano | USDBRL médio | Contexto |
|---|:-:|---|
| 1999 | 1.80 | Flutuação nova |
| 2002 | 2.95 | Crise Lula eleição |
| 2003-2008 | 2.0-2.5 | Boom commodities |
| 2008 | 2.40 | Crise LB collapse |
| 2011 | 1.55 | **BRL forte peak** |
| 2015-2016 | 3.9 | Dilma impeachment |
| 2020 | 5.6 | COVID crash |
| 2024 | 5.2 | Fiscal concerns |
| 2026 | 4.96 (actual) | Moderação com IOF + Copom hawkish |

## Impacto em ações

### Empresas BENEFICIÁRIAS de BRL fraco
Receita USD, custo BRL:
- **VALE3** (minério exportado em USD)
- **SUZB3, KLBN4** (celulose USD)
- **PETR4** (petróleo commodity USD)
- **EMBR3** (aeronaves em USD)

### Empresas PREJUDICADAS por BRL fraco
Custo USD, receita BRL:
- **BR Distribuidora, Raízen** (combustíveis importados)
- **Tech BR** (servidores, licenças em USD)
- **Consumer** dependente de insumos importados

## Como investir hedging câmbio

### Dollar-up exposure (BRL fraco = gain)
- **IVVB11**: S&P500 em BRL — dual exposure (market US + USD/BRL)
- **Dólar futuro** na B3
- **Tesouro PTAX** (título indexado à PTAX)
- **Stocks exporters** BR (VALE3, SUZB3)

### Dollar-down (BRL forte = gain)
- **Shorts/ETFs inversos** (raros em BR)
- **Importers / consumer internals** (MGLU3, LREN3)
- **Bonds BR prefixados** com spread interno

## No nosso sistema

- `data.series` tabela: series_id='USDBRL_PTAX'
- `analytics/fx.py::fx_rate(date)` — lookup por data
- `analytics/fx.py::total_portfolio_brl()` — consolida BR + US em BRL
- Usado em `obsidian_bridge.py` para MV consolidado

## Dato actual

Última PTAX (verificar sistema): **~4.96** (Abril 2026).

`ii fx --rate` ou `ii fx --total` para ver estado atual.

---

> **Fontes**: Banco Central do Brasil PTAX (bcb.gov.br/estabilidadefinanceira/historicocotacoes); Ministério da Fazenda boletim semanal; XP/Itau research on BRL; nosso `fetchers/bcb_fetcher.py`.
