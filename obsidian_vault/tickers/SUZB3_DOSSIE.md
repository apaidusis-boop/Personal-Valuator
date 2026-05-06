---
type: research_dossie
ticker: SUZB3
name: Suzano
market: br
sector: Materials
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, materials]
---

# 📑 SUZB3 — Suzano

> Generated **2026-04-26** by `ii dossier SUZB3`. Cross-links: [[SUZB3]] · [[SUZB3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

SUZB3 negocia P/E baixíssimo de 4.22 e P/B 1.29 com ROE robusto de 35.19%, mas DY apenas 2.45% e streak curta de 4y. IC consensus HOLD (medium, 60%) — divergência típica de cíclica de commodity: lucros actuais elevados (FX favorável + preço BHKP) com risco evidente de mean-reversion. Achado-chave: P/E 4 num ROE 35% é o mercado a precificar pico de ciclo da celulose; entrada exige convicção sobre cenário USD/BRL e demanda China — não tese DRIP.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 10.82  |  **BVPS**: 35.45
- **ROE**: 35.19%  |  **P/E**: 4.22  |  **P/B**: 1.29
- **DY**: 2.45%  |  **Streak div**: 4y  |  **Market cap**: R$ 56.42B
- **Last price**: BRL 45.64 (2026-04-24)  |  **YoY**: -12.7%

## 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[SUZB3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A Suzano (SUZB3) é uma empresa de materiais com um P/E baixo de 4.22, indicando que o preço da ação está abaixo do valor intrínseco comparado à sua lucratividade. Apesar de ter um ROE robusto de 35.19%, a empresa não atende aos critérios de dividend yield e Net Debt/EBITDA estabelecidos na filosofia de investimento.

**Key assumptions**:
1. A demanda por papelão ondulado continuará crescendo, mantendo os preços das commodities em níveis elevados
2. O cenário macroeconômico brasileiro permitirá que a empresa reduza sua dívida líquida de forma sustentável
3. Os dividendos continuarão sendo pagos e o histórico de pagamento será estendido para mais de 5 anos
4. A Selic permanecerá em níveis elevados, mantendo a atratividade das ações com P/E baixo

**Disconfirmati

→ Vault: [[SUZB3]]

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

- **P/E = 4.22** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 4.22** passa.
- **P/B = 1.29** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.29** — verificar consistência com ROE.
- **DY = 2.45%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **2.45%** abaixo do floor — DRIP não-óbvio.
- **ROE = 35.19%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **35.19%** compounder-grade.
- **Graham Number ≈ R$ 92.90** vs preço **R$ 45.64** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 4y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Preço BHKP / ciclo celulose** — receita altamente sensível a preço FOB China; queda de 20% destrói lucro. Trigger: BHKP spot China YoY <-15% (vault commodity note ou release).
- 🔴 **Exposição USD/BRL** — receita exportadora; BRL forte comprime EBITDA mesmo com volume estável. Trigger: `macro.usdbrl` <5.0 sustentado.
- 🟡 **Demanda China** — papel/celulose dependente de consumo asiático; risco macro chinês. Trigger: imports China celulose YoY <-10%.
- 🟡 **Streak curta + DY baixo** — 4y de pagamento e DY 2.45% afastam-se totalmente do critério DRIP. Trigger: `fundamentals.dy < 2%` consolida desqualificação.
- 🟢 **Custo cash competitivo** — Suzano é low-cost producer global; floor parcial em ciclos baixos. Trigger: gross margin YoY <-500bp em 2 trimestres → competitividade erodida.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Tese só faz sentido como tactical (cycle play / FX hedge), não como DRIP. Entry trigger: pullback >-25% combinado com BHKP a recuperar OU USD/BRL >5.5 sustentado. Weight prudente 2-3% como Tier-3 (cíclica de commodity).

## 7. Tracking triggers (auto-monitoring)

- **ROE mean-revert** — `fundamentals.roe < 18%` em release → tese de pico confirmada.
- **FX shock** — `macro.usdbrl` < 5.0 sustentado >60d → comprime EBITDA exportador.
- **PE inflation** — `fundamentals.pe > 12` → mercado já reprecificou ciclo, downside.
- **Leverage spike** — `fundamentals.net_debt_ebitda > 3.5` → risco financeiro com lucro a normalizar.
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
*Generated by `ii dossier SUZB3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
