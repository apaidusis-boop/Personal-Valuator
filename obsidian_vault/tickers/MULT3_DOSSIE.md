---
type: research_dossie
ticker: MULT3
name: Multiplan
market: br
sector: Real Estate
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, real estate]
---

# 📑 MULT3 — Multiplan

> Generated **2026-04-26** by `ii dossier MULT3`. Cross-links: [[MULT3]] · [[MULT3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

MULT3 negocia P/E 14.23 e P/B 2.54 com ROE 19.11% e streak excepcional de 18 anos, mas DY 3.31% fica abaixo do floor 6%. IC consensus HOLD (high, 80%) reflecte qualidade de operador líder de malls com track record longo, contrabalançada por valuation premium e yield baixo. Achado-chave: peer leader vs ALOS3 — ROE quase 3× superior (19% vs 7%), justificando P/B premium, mas o yield é metade.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.30  |  **BVPS**: 12.87
- **ROE**: 19.11%  |  **P/E**: 14.23  |  **P/B**: 2.54
- **DY**: 3.31%  |  **Streak div**: 18y  |  **Market cap**: R$ 16.05B
- **Last price**: BRL 32.73 (2026-04-24)  |  **YoY**: +30.1%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MULT3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: MULT3 é um fundo imobiliário focado em ativos de tijolo, com forte histórico de dividendos e ROE acima da média. Apesar do P/B estar ligeiramente alto (2.54), o DY de 3.31% ainda oferece uma vantagem relativa ao mercado brasileiro, embora esteja abaixo da faixa ideal para FIIs de 8-12%.

**Key assumptions**:
1. O P/VP manterá-se em um nível sustentável e não subirá acima do patamar atual
2. A taxa de vacância permanecerá estável ou diminuirá nos próximos trimestres, mantendo a geração de renda
3. Os ativos imobiliários continuarão gerando retornos superiores à média do setor, apoiados pelo ROE de 19.11%
4. A dívida líquida/EBITDA se manterá em um nível administrável (2.64), sem pressões significativas para aumentar

**Disconfirmation triggers**:
- ROE cai abai

→ Vault: [[MULT3]]

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

- **P/E = 14.23** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 14.23** passa.
- **P/B = 2.54** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.54** — verificar consistência com ROE.
- **DY = 3.31%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **3.31%** abaixo do floor — DRIP não-óbvio.
- **ROE = 19.11%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **19.11%** compounder-grade.
- **Graham Number ≈ R$ 25.81** vs preço **R$ 32.73** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🟡 **Valuation premium** — P/B 2.54× é o dobro de ALOS3; pouco margem de segurança. Trigger: `fundamentals.pb > 3.0` invalida ponto de entrada.
- 🟡 **Yield abaixo do critério** — DY 3.31% vs floor 6% impossibilita classificação como DRIP defensivo. Trigger: `fundamentals.dy < 3%` consolida desqualificação.
- 🟡 **Vacância em malls premium** — exposição a consumo discricionário e juros altos pode pressionar NOI. Trigger: NOI YoY <-3% em 2 trimestres consecutivos (release).
- 🟢 **ND/EBITDA controlado** — 2.64× dentro do limite, baixa pressão financeira; risco baixo. Trigger: `fundamentals.net_debt_ebitda > 3.5` para alarme.
- 🟡 **Compressão por juros** — yield baixo perde competitividade vs NTN-B em ciclo Selic alta. Trigger: `macro.selic_meta` delta >+50bp.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Entry trigger: pullback que leve P/B <2.0× combinado com DY ≥4.5%, ou tese reframe como compounder de qualidade em vez de DRIP. Weight prudente 3-5% como Tier-2 (mall premium, exposição cíclica).

## 7. Tracking triggers (auto-monitoring)

- **Valuation pullback** — `fundamentals.pb < 2.0` → reabrir tese de entrada.
- **DY upgrade** — `fundamentals.dy > 4.5%` → começa a competir com peers/NTN-B.
- **ROE drop** — `fundamentals.roe < 12%` → perda do diferencial vs ALOS3.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 3.0` → alerta de pressão financeira.
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
*Generated by `ii dossier MULT3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
