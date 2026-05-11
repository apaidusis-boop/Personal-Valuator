---
type: research_dossie
ticker: PETR4
name: Petrobras
market: br
sector: Oil & Gas
is_holding: False
date: 2026-04-26
verdict: BUY
verdict_confidence: high
verdict_consensus_pct: 100.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, oil & gas]
---

# 📑 PETR4 — Petrobras

> Generated **2026-04-26** by `ii dossier PETR4`. Cross-links: [[PETR4]] · [[PETR4_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PETR4 negocia a P/E 6.16 e DY 6.76% com ROE excepcional de 28.18% e dívida líq./EBITDA confortável em 1.60x. Synthetic IC veredicto **BUY** com consenso unânime (100%) e composite conviction 73. Achado central: combinação rara de earnings yield ~16% + payout sustentável, mas o risco de governança política (dividendos extraordinários, intervenção em preços) continua a ser o factor que pode colapsar a tese overnight.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 7.65  |  **BVPS**: 32.26
- **ROE**: 28.18%  |  **P/E**: 6.16  |  **P/B**: 1.46
- **DY**: 6.76%  |  **Streak div**: 9y  |  **Market cap**: R$ 644.37B
- **Last price**: BRL 47.16 (2026-04-24)  |  **YoY**: +55.0%

## 2. Synthetic IC

**🏛️ BUY** (high confidence, 100.0% consensus)

→ Detalhe: [[PETR4_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A PETR4, com um P/E de 6.22 e um DY de 6.76%, oferece um valor atrativo para investidores em busca de retornos estáveis. A empresa atende aos critérios da filosofia value-investing ajustada à Selic alta, destacando-se pelo ROE de 28.18% e uma dívida líquida/EBITDA de 1.60.

**Key assumptions**:
1. A PETR4 manterá seu histórico de dividendos ininterrupto por mais dois anos
2. O preço da ação não subirá acima do Graham Number ajustado para o ambiente atual (22.5)
3. A empresa continuará gerando um ROE superior a 15%
4. As condições macroeconômicas globais não afetarão negativamente os lucros operacionais da PETR4

**Disconfirmation triggers**:
- ROE cair abaixo de 12% por dois trimestres consecutivos
- Dividendos serem cortados ou pausados
- A dívida líquida/EBI

→ Vault: [[PETR4]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **73** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 90 |

## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 6.16** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 6.16** passa.
- **P/B = 1.46** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.46** — verificar consistência com ROE.
- **DY = 6.76%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **6.76%** passa.
- **ROE = 28.18%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **28.18%** compounder-grade.
- **Graham Number ≈ R$ 74.52** vs preço **R$ 47.16** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 9y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Governança política** — interferência em pricing combustíveis ou redirecionamento de capex social compromete margens e payout. Trigger: anúncio de mudança em política de paridade de preços ou troca de CEO por indicação política.
- 🔴 **Brent estrutural baixo** — break-even de pre-sal e geração de FCF dependem de Brent ≥ $60. Trigger: Brent < $60/bbl por 2 trimestres consecutivos (`prices` proxy via correlated ETF ou macro).
- 🟡 **Dividendos extraordinários reset** — política actual de DY 6.76% pode ser cortada a qualquer assembleia. Trigger: payout TTM > 100% ou anúncio de revisão de política de dividendos (`fundamentals.dy` queda >2pp QoQ).
- 🟡 **Dívida líq./EBITDA degradação** — actual 1.60x; alavancagem para acquisitions ou capex E&P pode pressionar grau de investimento. Trigger: `fundamentals.net_debt_ebitda` > 2.5x.
- 🟢 **Royalties / nova MP** — mudança fiscal sobre exploração offshore. Trigger: aprovação de MP ou PL aumentando alíquota de royalties.

## 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: pullback técnico para P/E < 5.5 (proxy: ~R$ 40) **com** confirmação de manutenção da política actual de dividendos pós-AGE. Weight prudente 3-5% do book BR (cap em estatal cíclica), uso exclusivo de cash BRL (BR isolation). Posição vs ITSA4/BBAS3 deve respeitar concentração sectorial — não somar +10% em estatais.

## 7. Tracking triggers (auto-monitoring)

- **DY colapso** — `fundamentals.dy` < 5.0% (sinal de corte de payout ou rerating preço).
- **Leverage spike** — `fundamentals.net_debt_ebitda` > 2.5x (degradação balance sheet).
- **ROE deterioração** — `fundamentals.roe` < 15% por 2 trimestres consecutivos.
- **Streak break** — `fundamentals.dividend_streak_years` regrida (cancelamento de proventos).
- **Thesis health** — `scores.details_json::thesis_health` < 60 (Synthetic IC reset para HOLD/SELL).

## 8. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier PETR4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

## 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-10 20:39 UTC · yt=10 · analyst=6 · themes=5_

### 🎬 YouTube + Podcast (últimos 90d)

| Data | Fonte | Kind | Conf | Claim |
|---|---|---|---:|---|
| 2026-05-09 | Inter Invest | catalyst | 0.80 | A expectativa é de que a Petrobras abra em alta na segunda-feira, com potencial para atingir os R$50. |
| 2026-05-03 | Stock Pickers | valuation | 0.80 | A Petrobras se beneficia do atual cenário de alta nos preços do petróleo, que está distorcido em relação às expectativas iniciais. |
| 2026-05-02 | Empiricus Podcasts | catalyst | 0.90 | A subida contínua dos preços do petróleo pode ser um catalisador positivo para a Petrobras. |
| 2026-05-02 | Empiricus Podcasts | valuation | 0.80 | A Petrobras está sendo vista como um ativo que pode aguentar incertezas e tem potencial de valorização se o fluxo de investimento internaci… |
| 2026-04-22 | Virtual Asset | risk | 0.80 | A Petrobras reconhece que as tensões geopolíticas podem impactar negativamente seus resultados. |
| 2026-04-22 | Virtual Asset | risk | 0.80 | A Petrobras alerta que a adaptação à nova legislação tributária pode causar efeitos adversos nos resultados. |
| 2026-04-22 | Virtual Asset | guidance | 0.70 | A Petrobras confirmou a distribuição de R$8 bilhões em dividendos e reforçou a distribuição total de R$41,2 bilhões em 2025. |
| 2026-04-21 | Market Makers | operational | 0.80 | A Petrobras pode gerar um excedente de ordem de grandeza de 15 bilhões de dólares devido à variação do preço do petróleo. |
| 2026-04-21 | O Primo Rico | operational | 0.80 | A Petrobras passou a emitir debêntures, títulos de dívida privada, para financiamento em vez de depender dos bancos. |
| 2026-04-21 | Market Makers | valuation | 0.70 | A Petrobras é considerada razoavelmente barata em vários cenários diferentes. |

### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | SUNO | rating | neutral | 38.00 | [Suno Valor] PETR4 — peso 7.5%, rating Aguardar, PT R$38.0 |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PETR4 — peso 9.6%, setor Energy |
| 2026-04-24 | XP | rating | bull | — | [BTG Equity Brazil] PETR4 — peso 13.5% |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PETR4 — peso 4.1% |
| 2026-04-24 | XP | catalyst | neutral | — | A Petrobras reajustou em 55% o preço do querosene de aviação, gerando apreensão no setor aéreo. |
| 2026-04-14 | XP | rating | bull | 47.00 | [XP Top Dividendos] PETR4 — peso 10.0%, Compra, PT R$47.0, setor Energia |

### 🌐 Macro themes mencionados (últimos 90d)

| Data | Fonte | Tema | Stance | Resumo |
|---|---|---|---|---|
| 2026-05-09 | Inter Invest | oil_cycle | bearish | O analista menciona preocupação com a queda do preço da Petrobras seguindo o petróleo, sugerindo um possível… |
| 2026-05-09 | Inter Invest | semis_cycle | bearish | O analista menciona a Aura 33 como um papel com potencial de queda, sugerindo uma tendência bearish. |
| 2026-05-09 | Inter Invest | usdbrl | bearish | O analista sugere que a tendência do dólar é de queda, indicando um momento não ideal para exposição em BDRs. |
| 2026-05-03 | Stock Pickers | oil_cycle | bullish | A guerra no Irã está elevando os preços do petróleo, beneficiando empresas como a Petrobras. |
| 2026-05-03 | Stock Pickers | oil_cycle | bullish | O preço do petróleo está atualmente alto devido à guerra no Irã, distorcendo as expectativas dos especialista… |

