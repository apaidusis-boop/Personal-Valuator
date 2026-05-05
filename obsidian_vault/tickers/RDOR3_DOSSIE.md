---
type: research_dossie
ticker: RDOR3
name: Rede D'Or
market: br
sector: Healthcare
is_holding: False
date: 2026-04-26
verdict: BUY
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, healthcare]
---

# 📑 RDOR3 — Rede D'Or

> Generated **2026-04-26** by `ii dossier RDOR3`. Cross-links: [[RDOR3]] · [[RDOR3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

RDOR3 negocia P/E 18.17 e P/B 4.41 com ROE 20.05% e DY excepcional de 11.03% (acima do floor 6%) com streak 6y. IC consensus BUY (high, 80%) — qualidade de líder hospitalar combinada com yield e ND/EBITDA controlado em 1.01× passa todos os critérios Graham excepto P/B. Achado-chave: DY 11% num healthcare é anómalo — provavelmente dividendo extraordinário pós-integração Sul América; validar que é recorrente antes de assumir como base DRIP.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.13  |  **BVPS**: 8.77
- **ROE**: 20.05%  |  **P/E**: 18.17  |  **P/B**: 4.41
- **DY**: 11.03%  |  **Streak div**: 6y  |  **Market cap**: R$ 85.26B
- **Last price**: BRL 38.71 (2026-04-24)  |  **YoY**: +25.2%

## 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[RDOR3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A RDOR3 é uma empresa de saúde que atende aos critérios clássicos de investimento de valor ajustados para a Selic alta, com um DY de 11.03%, ROE de 20.05% e dívida líquida/EBITDA de apenas 1.01x, além de ter mantido dividendos consistentes por seis anos.

**Key assumptions**:
1. A empresa continuará a gerar lucros acima da média do setor
2. Os níveis atuais de endividamento permanecerão estáveis ou diminuirão
3. O mercado de saúde no Brasil continuará crescendo e demandando serviços especializados oferecidos pela RDOR3
4. A empresa manterá seu histórico de pagamento de dividendos

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- Dividend streak interrompido
- P/B aumenta para mais de 6x
- Net Debt/EBITDA sobe acima de 3×

→ Vault: [[RDOR3]]

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

- **P/E = 18.17** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 18.17** passa.
- **P/B = 4.41** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **4.41** — verificar consistência com ROE.
- **DY = 11.03%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **11.03%** passa.
- **ROE = 20.05%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **20.05%** compounder-grade.
- **Graham Number ≈ R$ 20.50** vs preço **R$ 38.71** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 6y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **DY 11% pode ser não-recorrente** — provável evento extraordinário (M&A Sul América); base sustentável é provavelmente 4-6%. Trigger: dividendo trimestral próximo ano <60% do anualizado actual.
- 🟡 **Regulação operadoras de saúde / ANS** — pressão tarifária, judicialização e tetos podem comprimir margem. Trigger: notícia/release ANS sobre reajuste/limite (events table).
- 🟡 **Integração Sul América** — risco de execução do M&A; sinergias podem demorar. Trigger: gross margin YoY <-200bp em 2 trimestres.
- 🟡 **P/B 4.41 esticado** — único critério Graham falhado; pouca margem de segurança patrimonial. Trigger: `fundamentals.pb > 5.5` para alerta.
- 🟢 **Alavancagem baixa** — ND/EBITDA 1.01× dá flexibilidade financeira. Trigger: `fundamentals.net_debt_ebitda > 2.5` para alarme.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. IC BUY mas validar primeiro recorrência do DY 11% (pode ser one-off pós-Sul América). Entry weight prudente 4-5% como Tier-2 (líder healthcare, M&A risk). Pode chegar a 6-7% após confirmação de yield base sustentável >5%.

## 7. Tracking triggers (auto-monitoring)

- **DY normalization** — `fundamentals.dy < 5%` em release seguinte → confirma yield 11% foi one-off.
- **ROE drop** — `fundamentals.roe < 15%` por 2 trimestres → invalida pilar qualidade.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 2.5` → integração mais cara que esperado.
- **Regulatory hit** — `events` com kind='fato_relevante' + ANS/regulatório → review imediato.
- **Conviction drop** — `conviction_scores.composite_score < 65` → flag review.

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
*Generated by `ii dossier RDOR3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
