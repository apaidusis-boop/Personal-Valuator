---
type: research_dossie
ticker: MOTV3
name: Motiva
market: br
sector: Industrials
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, industrials]
---

# 📑 MOTV3 — Motiva

> Generated **2026-04-26** by `ii dossier MOTV3`. Cross-links: [[MOTV3]] · [[MOTV3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

MOTV3 negocia P/E 11.37 e P/B 2.10 com ROE forte de 20.78%, mas DY de apenas 2.35% e streak curta de 2y deixam-na fora do critério Graham clássico (DY ≥6%). IC consensus HOLD com high confidence (80%) — qualidade operacional reconhecida, mas não compensa o yield baixo num portefólio orientado a renda. Achado-chave: ND/EBITDA 3.55× já acima do limite 3× combinado com market cap R$33B sugere que o equity story aqui é growth-via-concessões, não DRIP defensivo.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.45  |  **BVPS**: 7.85
- **ROE**: 20.78%  |  **P/E**: 11.37  |  **P/B**: 2.10
- **DY**: 2.35%  |  **Streak div**: 2y  |  **Market cap**: R$ 33.14B
- **Last price**: BRL 16.48 (2026-04-24)  |  **YoY**: +26.1%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MOTV3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A MOTV3 opera no setor industrial brasileiro, com um P/E de 11.36 e um ROE de 20.78%, indicando potencial valorização a longo prazo. No entanto, o dividend yield de apenas 1.98% e uma relação dívida líquida/EBITDA acima do limite ideal (3.55 vs 3x) sugerem cautela.

**Key assumptions**:
1. Mantendo-se a tendência atual de crescimento dos lucros, o ROE se manterá acima de 15% nos próximos anos
2. A empresa conseguirá reduzir sua dívida líquida/EBITDA para abaixo de 3x nos próximos dois anos
3. O dividend yield aumentará significativamente em decorrência de políticas de distribuição mais agressivas ou melhora na rentabilidade operacional
4. A empresa continuará a pagar dividendos ininterruptamente, mantendo o histórico de cinco anos

**Disconfirmation triggers**

→ Vault: [[MOTV3]]

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

- **P/E = 11.37** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 11.37** passa.
- **P/B = 2.10** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.10** — verificar consistência com ROE.
- **DY = 2.35%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **2.35%** abaixo do floor — DRIP não-óbvio.
- **ROE = 20.78%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **20.78%** compounder-grade.
- **Graham Number ≈ R$ 16.00** vs preço **R$ 16.48** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 2y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Alavancagem acima do limite** — ND/EBITDA 3.55× vs floor 3.0×; concessões CAPEX-intensive amplificam risco em ciclo de juros alto. Trigger: `fundamentals.net_debt_ebitda > 3.8` em qualquer release.
- 🟡 **Yield insuficiente para tese DRIP** — 2.35% vs floor 6%; tese só faz sentido como growth/total-return, não para reinvestimento de dividendos. Trigger: `fundamentals.dy < 2%` consolida desqualificação.
- 🟡 **Risco regulatório/concessão** — fim de prazos de concessão, repactuações tarifárias e ambiente político. Trigger: notícia/release sobre quebra ou renegociação contratual (events table).
- 🟡 **Streak curta (2y)** — sem histórico para qualificar como dividendeira fiável; possível corte em ciclo down. Trigger: dividendo trimestral abaixo da média móvel 4Q.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR (caixa BRL only). Entry só faz sentido se reframe como growth/compounder — não DRIP. Trigger: ND/EBITDA cair sustentadamente <3× e DY subir >4%. Weight prudente 3-4% como Tier-2 (industrial cíclico/concessões).

## 7. Tracking triggers (auto-monitoring)

- **Deleverage success** — `fundamentals.net_debt_ebitda < 3.0` por 2 trimestres → reabrir tese.
- **ROE drop** — `fundamentals.roe < 15%` → invalidação do pilar de qualidade.
- **DY upgrade** — `fundamentals.dy > 4%` → começa a fazer sentido para income.
- **Selic shock** — `macro.selic_meta` delta >+50bp → CAPEX/refinancing pressure.
- **Thesis health** — `conviction_scores.composite_score < 60` → flag review.

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
*Generated by `ii dossier MOTV3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
