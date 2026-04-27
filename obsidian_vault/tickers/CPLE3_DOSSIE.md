---
type: research_dossie
ticker: CPLE3
name: Copel
market: br
sector: Utilities
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, utilities]
---

# 📑 CPLE3 — Copel

> Generated **2026-04-26** by `ii dossier CPLE3`. Cross-links: [[CPLE3]] · [[CPLE3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

CPLE3 negocia a P/E 18.43 e DY 4.97% com ROE moderado de 10.96%; preço subiu +57.3% YoY, comprimindo entry attractiveness. Synthetic IC veredicto **HOLD** (high confidence, 80% consenso) e composite conviction 68. Achado central: streak de dividendos de apenas 1 ano após a privatização — falta histórico para qualificar como DRIP, e a re-rating já consumiu o desconto pré-privatização.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.90  |  **BVPS**: 7.79
- **ROE**: 10.96%  |  **P/E**: 18.43  |  **P/B**: 2.13
- **DY**: 4.97%  |  **Streak div**: 1y  |  **Market cap**: R$ 49.27B
- **Last price**: BRL 16.59 (2026-04-24)  |  **YoY**: +57.3%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[CPLE3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: Copel, uma empresa de utilidade pública no Brasil, apresenta um P/E de 18.43 e um DY de 4.97%, com um ROE de 10.96%. Apesar do potencial valor, Copel não atende aos critérios rigorosos da filosofia investidora clássica ajustada à Selic alta.

**Key assumptions**:
1. A taxa Selic permanecerá estável ou cairá nos próximos anos
2. Copel manterá sua posição competitiva no mercado de energia elétrica e serviços relacionados
3. O fluxo de caixa operacional melhorará, permitindo um aumento sustentável dos dividendos em breve
4. A dívida líquida/EBITDA se aproximará do limite aceitável de 3x nos próximos trimestres

**Disconfirmation triggers**:
- ROE cai abaixo de 10% por dois quarters consecutivos
- Dividendos são cortados ou não aumentam após um período prolongado

→ Vault: [[CPLE3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **68** |
| Thesis health | 96 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 70 |






## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 18.43** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 18.43** passa.
- **P/B = 2.13** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.13** — verificar consistência com ROE.
- **DY = 4.97%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.97%** abaixo do floor — DRIP não-óbvio.
- **ROE = 10.96%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **10.96%** abaixo do critério.
- **Graham Number ≈ R$ 12.56** vs preço **R$ 16.59** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 1y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Dividend streak imaturo** — apenas 1 ano pós-privatização; tese DRIP não qualificada (mínimo 5y). Trigger: `fundamentals.dividend_streak_years` < 3 mantém-se como veto.
- 🟡 **Revisão tarifária ANEEL** — distribuição (Copel DIS) entra em ciclo de revisão; WACC regulatório pode contrair. Trigger: anúncio ANEEL com mudança de WACC base.
- 🟡 **DY abaixo do mínimo** — 4.97% < 6% requerido para utility BR. Trigger: `fundamentals.dy` permanecer < 6% por 4 trimestres.
- 🟡 **Hidrologia / Copel GeT** — geração hidrelétrica exposta a GSF. Trigger: ONS GSF < 0.85.
- 🟢 **Execução pós-privatização** — sinergias prometidas no IPO podem demorar; capex elevado pode pressionar FCF. Trigger: `fundamentals.net_debt_ebitda` > 3x.

## 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: P/E < 13 **e** DY ≥ 6% sustentado por 2 ITRs após maturação do streak (≥ 3y). Weight prudente 3-5% do book BR; só faz sentido como complemento defensivo se já tiver low exposure a utilities. Cash exclusivo BRL (BR isolation), sem deploy DRIP enquanto streak < 5y.

## 7. Tracking triggers (auto-monitoring)

- **DY ≥ 6%** — `fundamentals.dy` ≥ 6% sustentado 2 trimestres (qualifica para screen utility BR).
- **Streak amadurece** — `fundamentals.dividend_streak_years` ≥ 3 (parcial DRIP) ou ≥ 5 (full DRIP).
- **ROE deterioração** — `fundamentals.roe` < 10% por 2 trimestres consecutivos invalida tese.
- **P/E re-rating** — `fundamentals.pe` < 13 abre ponto de entrada técnico.
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 3x.

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
*Generated by `ii dossier CPLE3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
