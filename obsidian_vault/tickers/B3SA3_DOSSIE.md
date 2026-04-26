---
type: research_dossie
ticker: B3SA3
name: B3
market: br
sector: Financials
is_holding: False
date: 2026-04-26
verdict: BUY
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, financials]
---

# 📑 B3SA3 — B3

> Generated **2026-04-26** by `ii dossier B3SA3`. Cross-links: [[B3SA3]] · [[B3SA3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

B3SA3 negocia a P/E 22.60 com DY 3.19% mas ROE excepcional de 25.59% e net_debt/EBITDA de apenas 0.16x — capital-light puro. Synthetic IC veredicto **BUY** (medium confidence, 60% consenso) e composite conviction 73 com 19 anos de streak de dividendos. Achado central: monopólio natural de exchange brasileira justifica P/B alto (5.48x); DY baixo é trade-off por capital-light, mas o factor decisivo é ADTV B3 — qualquer queda estrutural de volume colapsa earnings.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.84  |  **BVPS**: 3.46
- **ROE**: 25.59%  |  **P/E**: 22.60  |  **P/B**: 5.48
- **DY**: 3.19%  |  **Streak div**: 19y  |  **Market cap**: R$ 95.10B
- **Last price**: BRL 18.98 (2026-04-24)  |  **YoY**: +43.0%

## 2. Synthetic IC

**🏛️ BUY** (medium confidence, 60.0% consensus)

→ Detalhe: [[B3SA3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: B3SA3 é uma empresa financeira sólida com um histórico de pagamento de dividendos consistente por mais de uma década. Com um ROE elevado de 25,59% e uma relação dívida líquida/EBITDA extremamente baixa de apenas 0,16x, a empresa mantém-se como um valor atrativo apesar do P/E ligeiramente acima da média (22,87x) e P/B alto (5,48x).

**Key assumptions**:
1. A demanda por serviços financeiros continuará em crescimento no Brasil, beneficiando B3SA3.
2. B3SA3 manterá seu histórico de distribuição de dividendos acima dos 3%.
3. O cenário macroeconômico brasileiro não deteriorar-se-á significativamente nos próximos anos.
4. A empresa continuará a gerir efetivamente suas dívidas, mantendo o ROE acima do nível atual.

**Disconfirmation triggers**:
- ROE cair abaixo de

→ Vault: [[B3SA3]]

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

- **P/E = 22.60** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 22.60** fora do screen.
- **P/B = 5.48** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **5.48** — verificar consistência com ROE.
- **DY = 3.19%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **3.19%** abaixo do floor — DRIP não-óbvio.
- **ROE = 25.59%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **25.59%** compounder-grade.
- **Graham Number ≈ R$ 8.09** vs preço **R$ 18.98** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 19y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Volume B3 estrutural baixo** — Selic alta empurra capital para RF, contraindo ADTV equities. Trigger: ADTV B3 < R$15B/dia média trimestral (proxy via `events` macro ou snapshot externo).
- 🔴 **Fee compression regulatória** — CVM/B3 podem reduzir taxas para incentivar competição. Trigger: anúncio CVM/B3 de revisão de tabela tarifária (`events` kind=`fato_relevante`).
- 🟡 **P/B alto vulnerável a re-rating** — 5.48x deixa pouco buffer para erros operacionais. Trigger: `fundamentals.pb` > 6 sem aceleração de earnings.
- 🟡 **Concorrência (ATS / nova bolsa)** — entrada de ATS regulamentada poderia diluir monopólio. Trigger: aprovação CVM de ATS competitiva.
- 🟢 **DY sub-mínimo** — 3.19% < 6% típico do screen BR (mas justificado por capital-light). Trigger: `fundamentals.dy` < 2.5% por 4 trimestres.

## 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira. Entry trigger: P/E < 18 (recompressão de múltiplo) **ou** sinal de Selic em tendência de queda sustentada (rotação de RF para equities aumenta ADTV). Weight prudente 4-6% do book BR como quality-compounder (não DRIP). Cash exclusivo BRL (BR isolation); pode complementar ITUB4 sem dupla-contar exposure financials operacional.

## 7. Tracking triggers (auto-monitoring)

- **ADTV colapso** — ADTV B3 < R$15B/dia média trimestral (proxy macro).
- **ROE deterioração** — `fundamentals.roe` < 18% por 2 trimestres consecutivos.
- **P/E re-rating** — `fundamentals.pe` < 18 (entry técnico) ou > 30 (exit técnico).
- **Streak break** — `fundamentals.dividend_streak_years` regrida abaixo de 19.
- **Fato relevante regulatório** — `events WHERE source='cvm' AND kind LIKE '%fee%'` ou revisão de tabela tarifária.

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
*Generated by `ii dossier B3SA3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
