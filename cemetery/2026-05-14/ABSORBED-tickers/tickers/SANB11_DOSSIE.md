---
type: research_dossie
ticker: SANB11
name: Santander BR
market: br
sector: Banks
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, BACEN IF.Data, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, banks]
---

# 📑 SANB11 — Santander BR

> Generated **2026-04-26** by `ii dossier SANB11`. Cross-links: [[SANB11]] · [[SANB11_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

<!-- TODO_CLAUDE_TLDR: 3 frases sobre SANB11 a partir das tabelas abaixo. Citar PE, DY, IC verdict, e o achado mais importante. -->

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 2.05  |  **BVPS**: 33.51
- **ROE**: 10.52%  |  **P/E**: 14.51  |  **P/B**: 0.89
- **DY**: 7.78%  |  **Streak div**: 17y  |  **Market cap**: R$ 140.10B
- **Last price**: BRL 29.68 (2026-04-24)  |  **YoY**: +5.7%

## 2. Screen — BR Banks (CLAUDE.md)

| Critério | Threshold | Valor | OK? |
|---|---|---|---|
| P/E ≤ 10 | ≤ 10 | **14.51** | ❌ |
| P/B ≤ 1.5 | ≤ 1.5 | **0.89** | ✅ |
| DY ≥ 6% | ≥ 6% | **7.78%** | ✅ |
| ROE ≥ 12% | ≥ 12% | **10.52%** | ❌ |
| Streak div ≥ 5y | ≥ 5 | **17y** | ✅ |

→ **3/5 critérios** passam.

## 3. Peer comparison

### Fundamentals

| Métrica | SANB11 | ABCB4 | BBDC4 | ITUB4 |
|---|---|---|---|---|
| Market cap | R$ 140.10B | R$ 6.52B | R$ 210.57B | R$ 489.02B |
| P/E | 14.51 | 4.73 | 9.35 | 11.06 |
| P/B | 0.89 | 0.90 | 1.18 | 2.39 |
| ROE | 10.52% | 15.46% | 13.75% | 21.01% |
| DY | 7.78% | 10.30% | 7.56% | 7.68% |
| Streak div | 17y | 16y | 19y | 19y |
| YoY price | +5.7% | +21.0% | +48.9% | +31.5% |

### BACEN regulatório (latest non-NULL)

| Métrica | SANB11 | ABCB4 | BBDC4 | ITUB4 |
|---|---|---|---|---|
| Período | n/a | 2025-09-30 | 2025-09-30 | 2025-09-30 |
| Basel | n/a | 16.71% | 15.85% | 16.40% |
| CET1 | n/a | 11.88% | 11.39% | 13.47% |
| NPL E-H | n/a | n/a | n/a | n/a |

## 4. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[SANB11_IC_DEBATE]]

## 5. Thesis

**Core thesis (2026-04-25)**: A Santander BR (SANB11) é uma instituição financeira com um sólido histórico de dividendos, oferecendo um DY anualizado de 7.78% e operando com um P/B abaixo de 1.0, indicativo de desconto em relação ao patrimônio líquido, sugerindo margem de segurança para investidores.

**Key assumptions**:
1. A empresa mantém uma consistente política de dividendos por pelo menos mais 17 anos consecutivos
2. O P/B continuarão a refletir um desconto substancial em relação ao valor do patrimônio líquido, indicando continuidade da atual avaliação baixa
3. A rentabilidade sobre o capital próprio (ROE) se mantém acima de 10% para sustentar dividendos robustos
4. O mercado financeiro reconhece a solidez e consistência operacional do banco, pressionando o P/B para níveis mais eleva

→ Vault: [[SANB11]]

## 6. Conviction breakdown

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

- **P/E = 14.51** → [[Glossary/PE|porquê isto importa?]]. Bancos BR têm spread alto e múltiplos comprimidos — target ≤ 10. **Actual 14.51** NÃO passa.
- **P/B = 0.89** → [[Glossary/PB|leitura completa]]. Bancos: P/B ≤ 1.5 = margem sobre equity. **0.89** OK.
- **DY = 7.78%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **7.78%** passa.
- **ROE = 10.52%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Bancos BR (Selic alta): target ≥ 12%. **10.52%** fraco.
- **Streak div = 17y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.
- **Basel = 16.71%** → [[Glossary/Basel_Ratio|capital regulatório]]. Tier **premium** (mín BCB ~10.5%; saudável ≥14%; premium ≥16%).
- **CET1 = 11.88%** → [[Glossary/CET1|capital high-quality]]. Tier **saudável** (≥11% médio peer BR; ≥13% leadership tipo ITUB4).

## 7. Riscos identificados

<!-- TODO_CLAUDE_RISKS: 3-5 riscos prioritizados, baseados em IC + thesis + peer compare. Severidade 🟢🟡🔴. Cite trigger condition específica. -->

## 8. Position sizing

**Status atual**: watchlist

<!-- TODO_CLAUDE_SIZING: guidance breve para entrada/aumento/redução. Considerar BR/US isolation, market cap, weight prudente, DRIP/cash deploy. -->

## 9. Tracking triggers (auto-monitoring)

<!-- TODO_CLAUDE_TRIGGERS: 3-5 condições mensuráveis em SQL/data que indicariam re-avaliação. Ex: 'NPL > 4%', 'DY < 5.5%', 'thesis_health score < 60'. Citar tabela/coluna a monitorar. -->

## 10. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| BACEN backfill | Olinda OData | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier SANB11` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

## 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-13 20:46 UTC · yt=0 · analyst=1 · themes=0_

### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-14 | XP | rating | bull | 44.00 | [XP Top Dividendos] SANB11 — peso 5.0%, Compra, PT R$44.0, setor Bancos |

