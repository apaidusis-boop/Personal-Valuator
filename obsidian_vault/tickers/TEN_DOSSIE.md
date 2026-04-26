---
type: research_dossie
ticker: TEN
name: Tsakos Energy Navig.
market: us
sector: Energy
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, energy]
---

# 📑 TEN — Tsakos Energy Navig.

> Generated **2026-04-26** by `ii dossier TEN`. Cross-links: [[TEN]] · [[TEN_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

TEN negoceia a P/E 8.82 com DY 1.53% e P/B 0.63 — métricas ópticamente "baratas" mas IC HOLD com 60% consenso esconde sinal crítico. Achado-chave: 🚨 **4 sinais de distress convergentes em Abril 2026 cycle peak (memo SELL pendente)** — YoY +132.6% típico de topo de ciclo tanker, NAV em queda e tanker rates rolling over. Posição em revisão para reduce/exit; **NÃO adicionar em nenhum cenário**.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 4.45  |  **BVPS**: 62.48
- **ROE**: 9.09%  |  **P/E**: 8.82  |  **P/B**: 0.63
- **DY**: 1.53%  |  **Streak div**: 24y  |  **Market cap**: USD 1.18B
- **Last price**: USD 39.27 (2026-04-26)  |  **YoY**: +132.6%

## 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[TEN_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: Tsakos Energy Navigation é uma posição atraente para investidores de longo prazo que buscam dividendos sustentáveis e crescimento acionário. A empresa apresenta um P/E baixo de 8,64x, indicando que o mercado está avaliando suas ações abaixo do valor intrínseco. Além disso, seu ROE de 9,09% sugere uma eficiência operacional sólida e lucratividade elevada. A empresa tem um histórico consistente de dividendos por 24 anos consecutivos, com um yield atual de 1,56%, o que é atraente para investidores em busca de renda regular.

**Key assumptions**:
1. O setor de energia continuará a apresentar condições favoráveis para empresas como Tsakos Energy Navigation.
2. A empresa manterá seu ROE acima de 9% nos próximos anos, refletindo sua eficiência operacional e gestão só

→ Vault: [[TEN]]

## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 8.82** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 8.82** passa.
- **P/B = 0.63** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **0.63** OK.
- **DY = 1.53%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **1.53%** fraco; verificar se é growth pick.
- **ROE = 9.09%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **9.09%** abaixo do critério.
- **Graham Number ≈ R$ 79.09** vs preço **R$ 39.27** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 24y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Cycle peak em Abril 2026** — 4 sinais convergentes: YoY +132% (típico topo), tanker rates rolling over, NAV em queda, comparáveis sector contracting. Trigger: TCE rates Suezmax/Aframax YoY < 0.
- 🔴 **Earnings YoY rollover** — shipping é hyper-cyclical; quando EPS YoY vira negativo o múltiplo expande contra. Trigger: `fundamentals.eps` YoY < 0.
- 🔴 **Capital allocation (newbuild orders no peak)** — ordens em peak comprimem returns no down-cycle seguinte. Trigger: capex > FCF por 2 quarters.
- 🟡 **NAV decline** — P/B 0.63 já sinaliza desconto vs equity, mas NAV está a comprimir. Trigger: BVPS YoY < -5%.
- 🟡 **Dividend irregular (shipping)** — 24y streak nominal mas amounts voláteis; corte é provável no down-cycle.

## 5. Position sizing

**Status atual**: holding (in portfolio)

🚨 **Reduce / Exit candidate** — memo SELL pendente do user. **NÃO adicionar em nenhum cenário**, inclusive DRIP. Avaliar saída faseada para realizar ganhos +132% YoY antes do rollover do ciclo. USD recebido fica em conta US para realocar a outro nome do screen.

## 6. Tracking triggers (auto-monitoring)

- **EPS YoY rollover** — `fundamentals.eps` YoY < 0 → confirma fim de cycle peak; accelerate exit.
- **Tanker rates roll** — TCE Suezmax/Aframax YoY < 0 (macro feed) → cycle break confirmed.
- **NAV decline** — `fundamentals.bvps` YoY < -5% → P/B 0.63 vai expandir contra.
- **Dividend cut** — qualquer corte ou freeze do dividendo → tese perfurada definitivamente.
- **Conviction drop** — `conviction_scores.composite_score < 50` → exit imediato.

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
*Generated by `ii dossier TEN` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
