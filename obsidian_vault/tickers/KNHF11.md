---
ticker: KNHF11
name: Kinea Hedge Fund FII
market: br
sector: Híbrido
segment_anbima: "Híbrido / Hedge Fund Imobiliário"
manager: Kinea (Itaú Unibanco group)
is_holding: false
currency: BRL
price: 98.39
price_date: 2026-05-07
dy_12m: 12.15
distros_12m_count: 12
distro_cv: 0.014
yoy_price_pct: 24.6
market_cap_brl_m: 1935
last_monthly_rendimento: 1.00
research_status: initial_scaffold
created: "2026-05-08"
tags: [watchlist, br, híbrido, kinea, research_candidate]
related: ["[[RBRX11]]", "[[KNCR11]]", "[[KNRI11]]", "[[sectors/Híbrido|Híbrido]]"]
---

# KNHF11 — Kinea Hedge Fund FII

#watchlist #br #híbrido #kinea

> **Status**: research scaffold inicial (2026-05-08). Adicionado ao universe.yaml
> watchlist; pipeline daily ainda não correu. Sem score, sem council debate ainda.
> Dados deste ficheiro vêm de yfinance live + Carta do Gestor 12-2025 + WebSearch.

## Contexto da inclusão

Considerado como **alternativa ao [[RBRX11]]** após preocupações do user com a
[[rbrx11_patria_acquisition|aquisição da divisão FIIs da RBR pela Pátria
em Dez/2025]] e o sinal de saída líquida persistente (cotistas -10% Jun→Dez/25).
KNHF11 é gerido pela Kinea (gestora independente, parte Itaú Unibanco), com
estrutura de hedge fund imobiliário multi-estratégia.

## Snapshot (yfinance live, 2026-05-07)

- **Preço**: R$ 98,39
- **Market cap**: R$ 1.935 M
- **YoY price**: +24,6%
- **Distros últimos 12m**: 12 × ~R$ 1,00 = **R$ 11,95/cota**
- **DY 12m computado**: 12,15%
- **Estabilidade distros (CV)**: 0,014 (ultra-estável; <0,05 = excepcional)
- **Liquidez**: ~2× a do RBRX11

## Mandate e estratégia (Carta do Gestor, Dez/2025)

> "Gerar retorno absoluto, resultante de renda recorrente e ganhos de capital,
> a partir de gestão activa multidisciplinar com carteira composta por diferentes
> activos do setor imobiliário."

Diferentes equipas Kinea contribuem ao fundo. Universo de busca: **CRI, FII,
Tijolo, Acções e Projectos de Desenvolvimento**.

## Composição do portfólio (Dez/2025)

| Classe | % |
|---|---:|
| CRI (recebíveis imobiliários) | 62,2% |
| Imóveis (tijolo) | 31,7% |
| Cotas de FII | 16,3% |
| (soma > 100% — pode incluir alavancagem ou caixa negativo) |  |

Carteira **transparente** — três classes distintas auditáveis, cada uma com mandate
declarado. Contraste com o "multiestratégia" mais opaco do RBRX11.

## Postura táctica recente (Dez/2025)

- Gestor reduziu posição em FIIs de 18,1% → 17,2%, **realizando lucros em CRI/Logística**
  que se valorizaram em Dezembro.
- Aumentou caixa para "iniciar 2026 com proteção e novas oportunidades".
- Tese de cautela: alta de Dezembro vista como **fluxo, não fundamentos**.
- Preocupação explícita com cenário fiscal e eleições BR 2026.

Esta postura activa, declarada, e discricionária é uma vantagem qualitativa
sobre fundos passivos ou opacos.

## Distribuições recentes (yfinance)

| Mês ref. | Distros (R$/cota) |
|---|---:|
| 2026-04 | 1,00 |
| 2026-03 | 1,00 |
| 2026-02 | 1,00 |
| 2026-01 | 1,00 |
| 2025-12 | 1,00 |
| 2025-11 | 1,00 |
| 2025-10 | 1,00 |
| 2025-09 | 1,00 |
| 2025-08 | 1,00 |
| 2025-07 | 1,00 |
| 2025-06 | 1,00 |
| 2025-05 | 0,95 |

Padrão: R$ 1,00/mês desde Jun/2025, após bump up de R$ 0,95.

## Comparação directa vs [[RBRX11]]

| Dimensão | RBRX11 | KNHF11 |
|---|---|---|
| Gestora | RBR / Pátria *(em integração M&A)* | Kinea (Itaú, estável) |
| Risco mudança ticker/regulamento 2026 | Sim (Pátria sinalizou consolidação) | Não |
| Composição declarada | "multiestratégia" opaco | 62% CRI + 32% Tijolo + 16% FII |
| DY 12m | 12,48% | 12,15% |
| Estabilidade distros CV | 0,020 | 0,014 |
| YoY price | +18,8% | +24,6% |
| Market cap | R$ 989M | R$ 1.935M |
| Streak distros | 5y | ~2,5y (FII mais novo, IPO ~mid-2023) |
| Cotistas trend (CVM) | **−9,99% em 6m** 🔴 | n/a (não temos CVM ingerido) |

## Lacunas conhecidas

- [ ] Sem `prices` no DB (corrigido após próximo daily_update.py)
- [ ] Sem `fii_monthly` ingerido (pendente — ver `library/ri/fii_filings.py`)
- [ ] Sem `fii_fundamentals` (computado após preços disponíveis)
- [ ] Sem score do nosso engine (`scoring/engine.py::score_fii`)
- [ ] Sem council debate (corre após dados disponíveis)
- [ ] Vacância física/financeira: irrelevante para hedge fund (carteira de papel/outros)

## Open actions

- [ ] Trigger `knhf11_cotistas_drop_5_6m` aguarda fii_monthly populado para
      poder avaliar (signal seria valioso para detectar deterioração simétrica
      à do RBRX11).
- [ ] Após `daily_update.py` correr e popular preço/dividendos, re-correr
      `python scoring/engine.py KNHF11 --market br` para gerar score formal.
- [ ] Após score, invocar `python -m agents.council.story KNHF11` para council
      formal (Lourdes Aluguel + Mariana Macro + Valentina Prudente + Pedro Alocação).
- [ ] Comparar relatório gerencial Mar/2026 (mais recente) para confirmar
      postura defensiva descrita em Dez/2025.

## Sources

- [Kinea — KNHF11 página oficial](https://www.kinea.com.br/fundos/fundo-imobiliario-kinea-hedge-fund-knhf11/)
- [Carta do Gestor — Dezembro 2025](https://www.kinea.com.br/wp-content/uploads/2026/01/KNHF_Carta-do-Gestor_12-2025.pdf)
- [Relatório Gerencial 31/Dez/2025 — BrFiis](https://brfiis.com.br/fundos/KNHF11/documentos/2026-jan-13/relatorio-gerencial-1081276)
- [Status Invest — KNHF11](https://statusinvest.com.br/fundos-imobiliarios/knhf11)
- yfinance (KNHF11.SA) — preço e dividendos snapshot 2026-05-07

---
*Created 2026-05-08 — sessão "test do sistema FII RBRX11 vs KNHF11".
Será regenerado pelo `obsidian_bridge` após pipeline daily incluir KNHF11.*
