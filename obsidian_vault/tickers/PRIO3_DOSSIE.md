---
type: research_dossie
ticker: PRIO3
name: PetroRio
market: br
sector: Oil & Gas
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, oil & gas]
---

# 📑 PRIO3 — PetroRio

> Generated **2026-04-26** by `ii dossier PRIO3`. Cross-links: [[PRIO3]] · [[PRIO3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PRIO3 negocia a P/E 22.61 e P/B 1.97 com ROE de apenas 8.71% — múltiplos esticados para uma E&P cíclica e ROE abaixo do critério Buffett (15%). DY n/a (streak de apenas 1 ano), portanto não é tese DRIP. IC HOLD (high confidence, 80% consensus) — composite conviction 70 sustenta-se mais por thesis health (96) do que por fundamentals; rally YoY +79.6% deixa pouca margem de segurança a este preço.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.77  |  **BVPS**: 31.83
- **ROE**: 8.71%  |  **P/E**: 22.61  |  **P/B**: 1.97
- **DY**: n/a  |  **Streak div**: 1y  |  **Market cap**: R$ 50.72B
- **Last price**: BRL 62.63 (2026-04-26)  |  **YoY**: +79.6%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[PRIO3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: A PRIO3, uma empresa do setor de petróleo e gás no Brasil, apresenta um perfil atraente para investidores Buffett/Graham em busca de valor a longo prazo. Com um preço/lucro (P/E) de 22,64 e um patrimônio líquido/patrimônio (P/B) de 1,97, a empresa está negociada abaixo da média histórica, oferecendo uma margem de segurança significativa. A PRIO3 tem um retorno sobre o patrimônio (ROE) de 8,71%, indicando eficiência operacional e potencial para crescimento sustentado. Além disso, a empresa possui uma relação dívida bruta/EBITDA de 3,12, sugerindo que está bem posicionada financeiramente para enfrentar desafios econômicos.

**Key assumptions**:
1. A PRIO3 manterá seu ROE acima de 8% nos próximos anos.
2. O preço/lucro (P/E) da empresa não excederá 25 no curto pr

→ Vault: [[PRIO3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **70** |
| Thesis health | 96 |
| IC consensus | 64 |
| Variant perception | 70 |
| Data coverage | 50 |
| Paper track | 50 |










## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 22.61** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 22.61** fora do screen.
- **P/B = 1.97** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.97** — verificar consistência com ROE.
- **ROE = 8.71%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **8.71%** abaixo do critério.
- **Graham Number ≈ R$ 44.54** vs preço **R$ 62.63** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 1y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Ciclo de petróleo (commodity)** — receita e EBITDA dependem do Brent; cycle peak risk após +79.6% YoY. Trigger: `prices` Brent < 70 USD/barril sustentado 30d.
- 🔴 **ROE estrutural baixo** — 8.71% está abaixo do critério Buffett (15%) e do mínimo BR não-financeiro. Trigger: `fundamentals.roe < 0.08` no próximo trimestre.
- 🟡 **Múltiplo esticado vs ROE** — P/E 22.61 com ROE single-digit implica preço a sustentar perpetual growth. Trigger: `fundamentals.pe > 25` AND `roe < 0.10`.
- 🟡 **Dívida elevada** — net_debt/EBITDA 3.12 já no limite (critério < 3×). Trigger: `fundamentals.net_debt_ebitda > 3.5`.
- 🟢 **Data coverage fraco (50)** — falta histórico de DY/streak; conviction depende muito da thesis health. Trigger: gap > 90 dias em `fundamentals` updates.

## 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold** posição actual sem reforçar a este preço — rally YoY +79.6% + P/E 22.6 + ROE 8.7% deixam pouca margem de segurança. PRIO3 é commodity-cíclico (não DRIP), pelo que peso sugerido <5% da sleeve BR; cash em BRL fica em BR (não converter). Considerar trim parcial se Brent ceder abaixo de 70 USD ou se P/E ultrapassar 25 com ROE estagnado; reforço só se voltar para P/E < 15 com Brent estabilizado.

## 7. Tracking triggers (auto-monitoring)

- **ROE deteriora** — `SELECT roe FROM fundamentals WHERE ticker='PRIO3' ORDER BY period_end DESC LIMIT 1` < 0.08
- **Dívida sobe** — `SELECT net_debt_ebitda FROM fundamentals WHERE ticker='PRIO3'` > 3.5
- **P/E expande sem ROE** — `fundamentals.pe > 25 AND fundamentals.roe < 0.10`
- **Thesis health degrada** — `SELECT thesis_health FROM conviction_scores WHERE ticker='PRIO3'` < 60
- **Drawdown técnico** — `prices.close` < 0.80 × max(close últimos 90d) sustentado 5 dias

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
*Generated by `ii dossier PRIO3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
