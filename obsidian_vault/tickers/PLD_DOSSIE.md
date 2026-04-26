---
type: research_dossie
ticker: PLD
name: Prologis
market: us
sector: REIT
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, reit]
---

# 📑 PLD — Prologis

> Generated **2026-04-26** by `ii dossier PLD`. Cross-links: [[PLD]] · [[PLD_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PLD cota P/E 39.80 (GAAP REIT, normal), DY 2.89% e streak 30y — REIT logístico líder global, beneficiário estrutural do e-commerce. IC verdict **HOLD** (medium confidence, 60% consensus); YoY +39.0% reflecte re-rating após o sell-off de 2024 induzido por cap rates altos. DRIP candidate sólido (REIT mandatory payout + 30y streak), manter para reinvestimento mas atento ao spread cap rate vs 10y treasury.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 3.57  |  **BVPS**: 57.18
- **ROE**: 6.84%  |  **P/E**: 39.80  |  **P/B**: 2.49
- **DY**: 2.89%  |  **Streak div**: 30y  |  **Market cap**: USD 132.47B
- **Last price**: USD 142.10 (2026-04-26)  |  **YoY**: +39.0%

## 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[PLD_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: Prologis, uma empresa de REIT com um histórico inegável de dividendos crescentes por 30 anos consecutivos e uma taxa de dividend yield de 2.89%, é apropriada para investidores Buffett/Graham em busca de rendimentos sustentáveis e crescimento de capital a longo prazo. Com um preço/lucro (PE) de 39.9775, que ainda se encontra dentro do intervalo aceitável para empresas com uma história consistente de dividendos, Prologis oferece segurança através da sua robusta relação dívida/EBITDA de 5.21 e um retorno sobre o patrimônio líquido (ROE) de 6.84%. A empresa mantém-se como uma posição sólida para investidores que buscam dividendos crescentes e valorização do ativo.

**Key assumptions**:
1. Prologis continuará a aumentar seus dividendos anualmente, refletindo sua re

→ Vault: [[PLD]]




## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 39.80** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 39.80** esticado vs critério.
- **P/B = 2.49** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **2.49** OK.
- **DY = 2.89%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **2.89%** OK.
- **ROE = 6.84%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **6.84%** abaixo do critério.
- **Graham Number ≈ R$ 67.77** vs preço **R$ 142.10** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 30y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

### Conceitos relacionados

- 💰 **Status DRIP-friendly** (US holding com DY ≥ 2.5%) — ver [[Glossary/DRIP]] para mecanismo + [[Glossary/Aristocrat]] para membership formal.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Cap rate spread vs 10y** — REITs sofrem quando spread cap-rate vs UST 10y comprime; atualmente apertado. Trigger: `macro_exports/DGS10` > 4.7% por 6m + cap rate < 5%.
- 🟡 **E-commerce capex slowdown** — Amazon e clientes top a desacelerar warehouse leasing após overbuild 2021-22. Trigger: occupancy < 95% ou guidance leasing growth YoY < 5%.
- 🟡 **Vacancy spec / build-to-suit pipeline** — desenvolvimento spec exposto a deterioração demand. Trigger: vacancy spec > 8% ou starts YoY < -20%.
- 🟢 **Streak 30y robusto** — política de dividendo REIT-mandated; quebra seria evento de tail. Trigger: `fundamentals.dy < 2.3%` ou anúncio de freeze em 8-K.

## 5. Position sizing

**Status atual**: holding (in portfolio)

**HOLD com bias DRIP** — REIT industrial líder qualifica como DRIP candidate (DY 2.89% + streak 30y); USD permanece em US (isolation rule). Após +39% YoY parte do re-rating já feito, evitar adds agressivos a estes níveis. Sizing prudente até 5-7% do US book; preferir adds em pull-backs (DY > 3.3% ou cap-rate spread > 250bps).

## 6. Tracking triggers (auto-monitoring)

- `fundamentals.dy < 2.3%` → quebra screen US (DY ≥ 2.5%).
- Cap rate spread vs 10y < 100bps (FRED DGS10 + REIT cap rate) → REIT pricing esticado.
- Occupancy < 95% por 2 trimestres → demand structural a quebrar.
- AFFO/share YoY < 3% por 2 trimestres → growth da DPU comprimido.
- `conviction_scores.score < 60` → tese DRIP REIT a degradar.

## 7. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier PLD` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
