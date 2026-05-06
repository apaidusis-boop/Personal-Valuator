---
type: research_dossie
ticker: VALE3
name: Vale
market: br
sector: Mining
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, mining]
---

# 📑 VALE3 — Vale

> Generated **2026-04-26** by `ii dossier VALE3`. Cross-links: [[VALE3]] · [[VALE3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

VALE3 negocia P/E 31.0 com ROE de apenas 5.87% e DY 6.38% sustentado por streak de 18 anos — múltiplo esticado para um ROE single-digit. IC HOLD (high confidence, 80% consensus); composite conviction 75. Achado material da Phase Y RI: deteriorating quality YoY com EBIT -25%, exigindo monitorização próxima do ciclo de minério após rally YoY +59.5%.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.77  |  **BVPS**: 43.17
- **ROE**: 5.87%  |  **P/E**: 31.00  |  **P/B**: 1.99
- **DY**: 6.38%  |  **Streak div**: 18y  |  **Market cap**: R$ 366.62B
- **Last price**: BRL 85.87 (2026-04-26)  |  **YoY**: +59.5%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[VALE3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: A Vale S.A. (VALE3) é uma excelente posição de longo prazo para um investidor do tipo Buffett/Graham, dada sua sólida geração de caixa e consistência em dividendos. Com um payout ratio sustentável de 50%, a empresa tem mantido um histórico de 18 anos consecutivos de pagamentos de dividendos, oferecendo uma renda estável aos acionistas. A relação P/E de 31,15 é ligeiramente elevada em comparação com o setor, mas compensada pelo baixo múltiplo P/B de 1,99 e um ROE de 5,87%, indicando que a empresa está gerindo bem seus ativos. A relação dívida EBITDA de 0,97 sugere uma posição financeira sólida.

**Key assumptions**:
1. O preço do minério de ferro permanecerá acima dos níveis mínimos históricos.
2. A Vale continuará a manter um payout ratio sustentável entre 50%

→ Vault: [[VALE3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **75** |
| Thesis health | 100 |
| IC consensus | 64 |
| Variant perception | 60 |
| Data coverage | 100 |
| Paper track | 50 |












## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 31.00** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 31.00** fora do screen.
- **P/B = 1.99** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.99** — verificar consistência com ROE.
- **DY = 6.38%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **6.38%** passa.
- **ROE = 5.87%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **5.87%** abaixo do critério.
- **Graham Number ≈ R$ 51.87** vs preço **R$ 85.87** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Deteriorating quality (Phase Y RI)** — YoY EBIT -25% sinaliza compressão de margens; ROE caiu para 5.87%. Trigger: `quarterly_history` EBIT YoY < -10% no próximo Q.
- 🔴 **Ciclo do minério de ferro** — receita ultra-correlacionada com preço China spot. Trigger: minério < 80 USD/t sustentado 30d.
- 🟡 **Múltiplo esticado** — P/E 31 com ROE 5.87% implica re-rating só justificável se margens normalizarem. Trigger: `fundamentals.pe > 35` AND `roe < 0.07`.
- 🟡 **Risco regulatório/ESG (Brumadinho/Mariana)** — passivos ambientais e fiscais residuais. Trigger: novo provisionamento >R$5B em earnings.
- 🟢 **Yield trap risk** — DY 6.38% pode comprimir se payout 50% encolhe com lucros. Trigger: `fundamentals.dy < 0.04` próximo trimestre.

## 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold** sem reforçar a este nível — combinação YoY +59.5% + EBIT -25% YoY + P/E 31 com ROE 5.87% sinaliza ciclo perto do topo. VALE3 é commodity-cyclical (não DRIP puro apesar do streak de 18 anos), pelo que peso prudente <7% da sleeve BR. Cash em BRL fica em BR (não converter); considerar trim parcial se EBIT continuar a deteriorar dois trimestres seguidos ou se minério cair abaixo de 80 USD/t. Reforço só com P/E < 8 e estabilização da margem operacional.

## 7. Tracking triggers (auto-monitoring)

- **EBIT YoY duplo digit drop** — `SELECT ebit FROM quarterly_history WHERE ticker='VALE3' ORDER BY period_end DESC LIMIT 5` — comparar Q vs Q-4 < -10%
- **ROE colapsa abaixo de 5%** — `SELECT roe FROM fundamentals WHERE ticker='VALE3' ORDER BY period_end DESC LIMIT 1` < 0.05
- **DY corta abaixo de 4%** — `fundamentals.dy < 0.04` (sinal de payout reduction)
- **P/E expande sem ROE** — `fundamentals.pe > 35 AND fundamentals.roe < 0.07`
- **Thesis health degrada** — `SELECT thesis_health FROM conviction_scores WHERE ticker='VALE3'` < 60

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
*Generated by `ii dossier VALE3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
