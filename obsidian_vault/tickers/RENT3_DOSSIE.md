---
type: research_dossie
ticker: RENT3
name: Localiza
market: br
sector: Industrials
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, industrials]
---

# 📑 RENT3 — Localiza

> Generated **2026-04-26** by `ii dossier RENT3`. Cross-links: [[RENT3]] · [[RENT3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

RENT3 negocia P/E elevado de 28.01 e P/B 2.11 com ROE apenas 7.21% (abaixo dos 15% requeridos), DY 4.18% e streak excepcional de 20 anos. IC consensus HOLD (medium, 60%) — divergência reflecte trade-off entre track record DRIP impecável e ROE actualmente comprimido pelo ciclo de juros (custo de carry da frota). Achado-chave: Localiza é classic compounder de longo prazo mas a janela actual (Selic alta + CAPEX renovação frota) pressiona ROE; entrada deve esperar ROE >12%.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.76  |  **BVPS**: 23.32
- **ROE**: 7.21%  |  **P/E**: 28.01  |  **P/B**: 2.11
- **DY**: 4.18%  |  **Streak div**: 20y  |  **Market cap**: R$ 51.98B
- **Last price**: BRL 49.29 (2026-04-24)  |  **YoY**: +18.5%

## 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[RENT3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A RENT3 é uma empresa de capital intensivo no setor industrial com um histórico robusto de pagamento de dividendos por mais de duas décadas. Apesar do P/E alto e ROE abaixo da meta, a relação P/B está dentro de limites aceitáveis e o DY oferece atratividade para investidores em busca de renda.

**Key assumptions**:
1. A empresa mantém seu histórico de dividendos por mais dois anos consecutivos
2. O ROE se recupera acima dos 15% nos próximos quatro trimestres
3. A relação dívida líquida/EBITDA permanece abaixo de 3× no próximo ano
4. A Selic mantém-se estável ou em queda, facilitando a gestão da dívida

**Disconfirmation triggers**:
- ROE cai abaixo de 7% por dois trimestres consecutivos
- Dividendos não são pagos nos próximos dois trimestres
- A relação dívida

→ Vault: [[RENT3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **65** |
| Thesis health | 100 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 50 |












## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 28.01** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 28.01** fora do screen.
- **P/B = 2.11** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.11** — verificar consistência com ROE.
- **DY = 4.18%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.18%** abaixo do floor — DRIP não-óbvio.
- **ROE = 7.21%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **7.21%** abaixo do critério.
- **Graham Number ≈ R$ 30.39** vs preço **R$ 49.29** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 20y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **ROE comprimido pelo ciclo** — 7.21% vs floor 15%; carry de frota com Selic alta e CAPEX renovação destroem retorno. Trigger: `fundamentals.roe < 6%` em release seguinte → erosão estrutural.
- 🟡 **CAPEX frota intensivo** — modelo capital-intensive amplifica sensibilidade a juros e preços de carros. Trigger: dívida líquida YoY >+25% em 2 trimestres.
- 🟡 **Ciclo automotivo / preço de carros usados** — desvalorização da frota afecta resultado. Trigger: receita de seminovos YoY <-15% em release.
- 🟡 **P/E 28 esticado para ROE 7%** — múltiplo precifica recuperação de margem; risco se demora. Trigger: `fundamentals.pe > 35` para alerta de overvaluation.
- 🟢 **Streak 20y impecável** — track record DRIP class A; risco de corte muito baixo. Trigger: dividendo zero em qualquer trimestre = sinal estrutural grave.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada. Compounder de qualidade mas valuation actual desfavorável (P/E 28 / ROE 7%). Entry trigger: ROE recovery >12% em 2 trimestres OU pullback que normalize P/E <20×. Weight prudente 4-5% como Tier-2 pela qualidade do business e streak DRIP.

## 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → entry zone activa.
- **PE compression** — `fundamentals.pe < 18` → valuation razoável.
- **Selic shock** — `macro.selic_meta` delta >+50bp → CAPEX/refinancing pressure agrava.
- **DY drop** — `fundamentals.dy < 3%` → afasta-se do critério renda.
- **Conviction drop** — `conviction_scores.composite_score < 55` → flag review.

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
*Generated by `ii dossier RENT3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
