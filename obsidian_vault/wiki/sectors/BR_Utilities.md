---
type: sector
name: BR Utilities
region: BR
tags: [sector, utilities, regulated, br]
related: ["[[Selic]]", "[[IPCA]]", "[[DDM_Gordon]]", "[[Dividend_Safety]]"]
holdings: ["[[EGIE3]]", "[[TAEE11]]", "[[ISAE4]]", "[[CMIG4]]", "[[CPLE3]]", "[[SAPR11]]"]
---

# ⚡ Setor: Utilities BR

## Mapa regulatório

Três sub-sectores **economicamente distintos**, apesar de "utility" ser tratado como um bloco:

| Sub-sector | Regulador | Receita | Risco |
|---|---|---|---|
| Geração | ANEEL + ONS | PPA contratado + spot | Hidrologia + inflação |
| Transmissão | ANEEL (RAP) | RAP indexada IPCA (revista 5y) | Zero demand risk — execution only |
| Distribuição | ANEEL (reajustes anuais) | Consumo × tarifa | Inadimplência + perdas técnicas |
| Saneamento | ARSESP/ARSPB | Tarifa + volume | Capex pesado, marco 2020 |

**Canonical**: [[TAEE11]] transmissão pura → menor risco. [[EGIE3]] geração com contratos longos → 2º menor risco. [[CMIG4]] / [[CPLE3]] mistos (dist + geração) → mais volatéis.

## Receita mechanics

### Transmissão (RAP)
- **RAP = Receita Anual Permitida** — contrato 30 anos com revisão a cada 5y.
- Indexada a **IPCA** (ou IGP-M legacy).
- **Zero exposição a demand/preço spot**.
- Score metric: DY + histórico sem cortes.

### Geração
- **PPA** (Power Purchase Agreement) — contratos bilaterais 5-20y, preço fixo IPCA-indexado.
- Exposição **Mercado Livre** (MWh spot) — preço volátil (R$ 50-800/MWh range).
- Hidrologia determina mix: chuva normal = PLD baixo = geração vende no PPA já contratado; seca = PLD alto mas se geradora falhou hidro precisa comprar no spot = destrói margem.
- **GSF** (Generation Scaling Factor) mutualisa risco hidro no SIN (2001/2015 rationing episodes).

### Distribuição
- **Revisão tarifária periódica (RTP)** a cada 4-5 anos.
- Entre revisões: reajuste anual (IGP-M → IPCA desde 2023).
- **Perdas técnicas + comerciais** (furto de luz no NE pode chegar 20%+ da energia distribuída).
- Capex intensivo para manter qualidade (DEC/FEC) — regulatório pune falha.

## Drivers macro

### [[Selic]] sensibilidade
- Utilities são bond proxies → Selic ↑ tende a pressionar preço das ações.
- Mas contratos IPCA-indexados protegem dividendo real.
- **Trade**: em ciclos de Selic alta, DY nominal sobe mecanicamente (preço cai, dividendo IPCA-linked sobe) — janela compra.

### [[IPCA]]
- Motor directo da RAP e PPAs.
- IPCA ↑ → RAP ↑ → dividendo ↑ (com lag 6m).

### Hidrologia / clima
- ONS publica nível reservatórios mensalmente.
- Reservatórios < 40% → risco de PLD spike + racionamento.
- **2001 apagão**, **2015 stress**, **2021 drought** — janelas históricas onde geradoras hidro sofreram.

### Câmbio
- Exposição **baixa** (inputs mostly BRL; algum CAPEX em EUR para equipamentos).

## Peer table (nossa universe)

| Ticker | Sub | Tese | Risco |
|---|---|---|---|
| [[TAEE11]] | Transmissão | RAP pura, DY alto, zero demand risk | Concentração alguns leilões |
| [[ISAE4]] | Transmissão | Ex-ISA CTEEP, mesma mecânica TAEE | Spin corporate em evolução |
| [[EGIE3]] | Geração | Hidro + eólica + térmica, mix robusto, moat operacional Engie | PLD se seca |
| [[CMIG4]] | Integrada (MG) | Dist + geração + gás, estatal MG | Política MG, tarifa social |
| [[CPLE3]] | Integrada (PR) | Privatizada 2023, tese turnaround | Execution risk reestruturação |
| [[ALUP11]] | Transmissão | Alupar, também pura transmissão | Menor escala vs TAEE |
| [[ENGI11]] | Energisa (Dist) | Dist consolidadora (NO/NE), concessões 30y | Capex heavy, inadimplência NE |

### Saneamento (subcategoria)
- [[SAPR11]] (Sanepar PR) — concessão 30y, receita tarifa + volume.
- [[CSMG3]] (Copasa MG) — estatal, política MG + marco 2020.

## Tese actual (2026)

- [[Selic]] cortes 2025-26 → revaluation utilities (bond proxy).
- [[IPCA]] 4-5% → protege dividendo real.
- Transmissão é a tese mais limpa para DRIP BR (TAEE, ISAE).
- Distribuição tem RTP a vir 2026-27 para vários players — risco/oportunidade.

## Red flags

- **Reservatórios < 40%** + geradora com GSF negativo → spot purchase destrói margem trimestral.
- **RTP desfavorável** (revisão WACC baixa) → impacta dividendo 4y à frente.
- Alavancagem > 3.5× ND/EBITDA em dist → vulnerável a ciclos.
- Interferência política em estatais (tarifa subsidy, payout forçado).

## Como usar no sistema

- Bancos BR usam `score_br_bank`; utilities usam `score_br` normal mas com **critério dividend_streak muito importante** (cortes de dividendo em utility = red flag grave).
- DY-pctl entry timing aplicado (Phase G backtest) — janelas de DY > p75 histórico são boas entries.

---

> Ver também: [[Dividend_Safety]], [[DDM_Gordon]] (utilities são o caso canónico Gordon), [[Selic_history]].
