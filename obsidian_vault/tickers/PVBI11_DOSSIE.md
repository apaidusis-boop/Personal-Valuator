---
type: research_dossie
ticker: PVBI11
name: VBI Prime Properties
market: br
sector: Corporativo
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, corporativo]
---

# 📑 PVBI11 — VBI Prime Properties

> Generated **2026-04-26** by `ii dossier PVBI11`. Cross-links: [[PVBI11]] · [[PVBI11_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PVBI11 é FII Corporativo (VBI Prime, lajes Faria Lima/SP) com **DY 5.95%** abaixo do piso típico FII, mas streak de 7y (mais longo do bolso) e P/E 8.42 baixo. **Synthetic IC: HOLD** (high confidence, 80% consensus) com composite **conviction 75** — o mais alto entre os FIIs do bolso. **Achado-chave: tese contrarian deliberada (turnaround) — Tier C no scoring por DY baixo, mas hold pela vacância em re-absorção do prédio FL; NÃO sugerir venda.**

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 9.38  |  **BVPS**: n/a
- **ROE**: n/a  |  **P/E**: 8.42  |  **P/B**: n/a
- **DY**: 5.95%  |  **Streak div**: 7y  |  **Market cap**: R$ 2.14B
- **Last price**: BRL 79.00 (2026-04-26)  |  **YoY**: +1.4%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[PVBI11_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: PVBI11 é uma ação atrativa para investidores de longo prazo que buscam dividendos sustentáveis e crescimento acionário. Com um P/E de 8,33 e uma taxa de dividendos de 6%, a empresa oferece valor comparável ao mercado brasileiro e demonstra consistência no pagamento de dividendos por sete anos consecutivos. A posição atual com preço de entrada de R$79,04 e market cap de US$426 milhões sugere uma base sólida para investidores Buffett/Graham que buscam empresas estabelecidas com retornos atrativos.

**Key assumptions**:
1. PVBI11 continuará a pagar dividendos consistentemente nos próximos anos.
2. A empresa manterá sua margem de lucro e crescimento acionário em linha com as médias históricas.
3. O mercado brasileiro continuará a valorizar empresas com baixo múlti

→ Vault: [[PVBI11]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **75** |
| Thesis health | 100 |
| IC consensus | 64 |
| Variant perception | 70 |
| Data coverage | 83 |
| Paper track | 50 |













## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **DY = 5.95%** → [[Glossary/DY|leitura + contraméricas]]. FIIs: target DY ≥ 8%. **5.95%** baixo para FII; verificar reset/cycle.
- **Streak div = 7y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

## 5. Riscos identificados

- 🔴 **Vacância prédio FL (Faria Lima) prolongada** — eixo da tese turnaround; se re-absorção falhar, distribuição estagna. Trigger: relatório gerencial reportando vacância prédio FL > 30% por 3 trimestres consecutivos.
- 🟡 **DY 5.95% abaixo do piso FII** — caro vs peers; só justificável se prêmio de qualidade (Faria Lima A+) materializar. Trigger: `fundamentals.dy < 0.055` por 2 meses sem progresso de leasing.
- 🟡 **Re-pricing de cap-rate em laje corporativa** — Selic alta + WFH residual pressionam valuation. Trigger: `pb > 1.0` enquanto vacância > 20%.
- 🟢 **Streak 7y** — risco baixo, mas observar. Trigger: distribuição mensal cair > 10% MoM.
- 🟢 **Concentração single-asset** — Faria Lima é prêmio mas single-tenant risk. Trigger: notícia de saída de inquilino âncora.

## 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold** — turnaround thesis explícita do user; **NÃO sugerir venda apesar do Tier C no scoring DRIP** (memory rule). Composite conviction 75 valida hold. Cap em **5-8% do bolso BR de FIIs**. **Não fazer add agressivo** enquanto vacância FL não baixar; reinvestir distribuição mensal em outros FIIs do bolso (XPML11/VGIR11) é aceitável até gatilho de leasing-up. BRL doméstico, sem conversão US→BR. Trim só se vacância prédio FL deteriorar materialmente (> 30% por 3 quarters).

## 7. Tracking triggers (auto-monitoring)

- **Vacância prédio FL prolongada** — relatório gerencial trimestral com vacância > 30% por 3 quarters → tese turnaround rota.
- **DY abaixo do piso** — `fundamentals.dy < 0.055` por 2 meses → revisar.
- **Distribuição mensal cai** — `events.kind='dividend' AND amount < (avg ult 6m × 0.85)` → investigar relatório.
- **Streak quebrado** — `fundamentals.dividend_streak_years < 7` → tese de stability rota.
- **Conviction degrada** — `conviction.composite < 65` → re-avaliar permanência (não sair só por scoring DRIP, é turnaround).

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
*Generated by `ii dossier PVBI11` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
