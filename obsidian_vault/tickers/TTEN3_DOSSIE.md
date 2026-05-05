---
type: research_dossie
ticker: TTEN3
name: 3Tentos
market: br
sector: Consumer Staples
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 100.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, consumer staples]
---

# 📑 TTEN3 — 3Tentos

> Generated **2026-04-26** by `ii dossier TTEN3`. Cross-links: [[TTEN3]] · [[TTEN3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

TTEN3 negocia P/E 9.52 e P/B 1.63 com ROE 18.49% e streak 5y, mas DY 1.19% fica muito abaixo do floor 6%. IC consensus HOLD com confiança máxima (100%) — agro novo (Suno target 16.80) com qualidade operacional comprovada mas reinveste em vez de distribuir. Achado-chave: ND/EBITDA 2.99× já no limite e queda -9.3% YoY mostram que ciclo grão (soja/milho) começa a pressionar — entrada exige espera por estabilização ou pullback maior.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.61  |  **BVPS**: 9.40
- **ROE**: 18.49%  |  **P/E**: 9.52  |  **P/B**: 1.63
- **DY**: 1.19%  |  **Streak div**: 5y  |  **Market cap**: R$ 7.66B
- **Last price**: BRL 15.32 (2026-04-24)  |  **YoY**: -9.3%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 100.0% consensus)

→ Detalhe: [[TTEN3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: TTEN3, uma empresa do setor de Consumer Staples, apresenta um perfil defensivo com fundamentos sólidos, incluindo ROE de 18.49% e uma relação dívida líquida/EBITDA próxima ao limite aceitável (2.995). No entanto, o dividend yield atual de 1.19% está abaixo do critério mínimo da filosofia de investimento de 6%, limitando a atratividade como um valor seguro para um value-investor.

**Key assumptions**:
1. A empresa mantém seu histórico de pagamento de dividendos por pelo menos mais dois anos
2. O ROE permanece acima de 15% nos próximos trimestres
3. A relação dívida líquida/EBITDA se estabiliza ou melhora para valores abaixo de 3×
4. A empresa aumenta seu dividend yield para pelo menos 6%

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres

→ Vault: [[TTEN3]]

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

- **P/E = 9.52** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 9.52** passa.
- **P/B = 1.63** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.63** — verificar consistência com ROE.
- **DY = 1.19%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **1.19%** abaixo do floor — DRIP não-óbvio.
- **ROE = 18.49%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **18.49%** compounder-grade.
- **Graham Number ≈ R$ 18.45** vs preço **R$ 15.32** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 5y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Preço de grãos (soja/milho)** — modelo agro depende de margens insumos×grãos; queda de preço comprime ambos os lados. Trigger: soja CME YoY <-15% sustentado.
- 🟡 **ND/EBITDA no limite** — 2.99× a 1bp do floor; qualquer choque de EBITDA cruza a fronteira. Trigger: `fundamentals.net_debt_ebitda > 3.2`.
- 🟡 **DY incompatível com tese DRIP** — 1.19% indica reinvestimento agressivo (growth), não renda. Trigger: `fundamentals.dy < 1%` consolida desqualificação.
- 🟡 **Competição agro / climático** — safra negativa ou pragas afectam volume e margem. Trigger: revisão receita guidance no release.
- 🟢 **ROE robusto** — 18.49% acima do floor 15% confirma qualidade operacional. Trigger: `fundamentals.roe < 12%` para alarme.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Tese growth/agro (Suno target 16.80 vs preço 15.32, upside ~10%), não DRIP. Entry trigger: deleverage para ND/EBITDA <2.5× OU pullback >-15% combinado com soja a estabilizar. Weight prudente 2-3% como Tier-2 (mid-cap agro novo, ciclo commodity).

## 7. Tracking triggers (auto-monitoring)

- **Deleverage** — `fundamentals.net_debt_ebitda < 2.5` → entrada mais segura.
- **ROE drop** — `fundamentals.roe < 12%` por 2 trimestres → invalida pilar qualidade.
- **Suno target alcançado** — `prices.close > 16.80` → reduzir/sair (target Suno).
- **PE inflation** — `fundamentals.pe > 14` → margem de segurança evapora.
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
*Generated by `ii dossier TTEN3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
