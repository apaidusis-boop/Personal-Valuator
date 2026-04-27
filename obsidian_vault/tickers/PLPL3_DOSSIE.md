---
type: research_dossie
ticker: PLPL3
name: Plano & Plano
market: br
sector: Consumer Disc.
is_holding: False
date: 2026-04-26
verdict: BUY
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, consumer disc.]
---

# 📑 PLPL3 — Plano & Plano

> Generated **2026-04-26** by `ii dossier PLPL3`. Cross-links: [[PLPL3]] · [[PLPL3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PLPL3 negocia P/E baixíssimo de 6.52 com ROE excepcional de 41.08% e DY 4.20%, streak 5y. IC consensus BUY (high, 80%) — único caso BUY desta watchlist, alicerçado em valuation baratíssimo combinado com rentabilidade extraordinária. Achado-chave: ROE 41% num P/E 6.5 sugere mercado descontando ciclo MCMV (Minha Casa Minha Vida) e juros como estrutura, não como pico — o risco maior está fora da DRE actual.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.80  |  **BVPS**: 5.04
- **ROE**: 41.08%  |  **P/E**: 6.52  |  **P/B**: 2.33
- **DY**: 4.20%  |  **Streak div**: 5y  |  **Market cap**: R$ 2.38B
- **Last price**: BRL 11.74 (2026-04-24)  |  **YoY**: -1.7%

## 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[PLPL3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A PLPL3 é uma empresa de consumo discrecional com um valuation atrativo, apresentando um P/E de 6.52 e um ROE de 41.08%. Apesar do dividend yield estar abaixo da meta de 6%, a empresa mantém um histórico ininterrupto de pagamento de dividendos por cinco anos e possui uma baixa relação dívida líquida/EBITDA.

**Key assumptions**:
1. PLPL3 manterá seu ROE acima dos 15% nos próximos trimestres
2. A empresa continuará a pagar dividendos com um yield próximo ao atual por pelo menos mais dois anos
3. O P/B da PLPL3 permanecerá estável ou diminuirá, mantendo o valuation atrativo
4. A relação dívida líquida/EBITDA não aumentará significativamente

**Disconfirmation triggers**:
- ROE cair abaixo de 15% por dois trimestres consecutivos
- Dividend yield cair para menos d

→ Vault: [[PLPL3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **72** |
| Thesis health | 96 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 90 |






## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 6.52** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 6.52** passa.
- **P/B = 2.33** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.33** — verificar consistência com ROE.
- **DY = 4.20%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.20%** abaixo do floor — DRIP não-óbvio.
- **ROE = 41.08%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **41.08%** compounder-grade.
- **Graham Number ≈ R$ 14.29** vs preço **R$ 11.74** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 5y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Dependência MCMV / política habitacional** — corte de orçamento federal ou redesenho do programa pode evaporar pipeline. Trigger: notícia/release sobre alteração MCMV (events table, source=cvm).
- 🔴 **Juros financiando habitação popular** — Selic alta encarece TR/financiamento e reduz takeup. Trigger: `macro.selic_meta` delta >+50bp combinada com lançamentos -20% YoY.
- 🟡 **ROE insustentável (41%)** — provável pico de ciclo; mean-reversion para 20-25% reduzirá lucros. Trigger: `fundamentals.roe < 25%` em release trimestral.
- 🟡 **Competição local pricing** — players regionais e MRV/Cury podem comprimir margem. Trigger: gross margin YoY <-200bp.
- 🟢 **Valuation com margem de segurança** — P/E 6.52 já desconta cenário pessimista; downside parcialmente protegido. Trigger: `fundamentals.pe > 12` para alerta de overpricing.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. IC BUY mas exige tese tactical, não DRIP — ROE 41% não sobrevive ao ciclo seguinte. Entry weight prudente 2-3% como Tier-2 com stop em ROE <20% ou MCMV cut. Não exceder 4% dado risco político concentrado.

## 7. Tracking triggers (auto-monitoring)

- **ROE mean-revert** — `fundamentals.roe < 20%` por 2 trimestres → tese de pico confirmada, exit.
- **MCMV cut** — `events.summary` contendo "MCMV" + corte/suspensão → reavaliar imediatamente.
- **Selic shock** — `macro.selic_meta` delta >+75bp → financiamento pressionado.
- **DY drop** — `fundamentals.dy < 3%` → sinaliza retenção de capital ou queda de lucro.
- **Conviction drop** — `conviction_scores.composite_score < 60` → flag review.

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
*Generated by `ii dossier PLPL3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
