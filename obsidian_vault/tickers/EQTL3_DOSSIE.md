---
type: research_dossie
ticker: EQTL3
name: Equatorial
market: br
sector: Utilities
is_holding: False
date: 2026-04-26
verdict: AVOID
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, utilities]
---

# 📑 EQTL3 — Equatorial

> Generated **2026-04-26** by `ii dossier EQTL3`. Cross-links: [[EQTL3]] · [[EQTL3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

EQTL3 negocia a P/E esticado de 45.95 com DY apenas 5.18% e ROE fraco de 6.98%, apesar de streak impressionante de 18 anos. Synthetic IC veredicto **AVOID** (high confidence, 80% consenso) e composite conviction 65. Achado central: histórico de excelência em M&A de distribuidoras já não está reflectido em retorno actual sobre capital — múltiplos premium sem justificativa em ROE, classic value trap em utility growth.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.96  |  **BVPS**: 20.47
- **ROE**: 6.98%  |  **P/E**: 45.95  |  **P/B**: 2.16
- **DY**: 5.18%  |  **Streak div**: 18y  |  **Market cap**: R$ 55.50B
- **Last price**: BRL 44.11 (2026-04-24)  |  **YoY**: +24.4%

## 2. Synthetic IC

**🏛️ AVOID** (high confidence, 80.0% consensus)

→ Detalhe: [[EQTL3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A EQTL3 opera no setor de utilities e apresenta um histórico sólido de dividendos, com 18 anos ininterruptos. Apesar disso, a empresa não atende aos critérios estritos da filosofia de investimento value, especialmente em relação ao ROE (6.98%) e ao Dividend Yield (5.18%), que estão abaixo dos requisitos mínimos.

**Key assumptions**:
1. A taxa Selic permanecerá elevada por um período prolongado, mantendo o ambiente desafiador para empresas com baixos retornos sobre capital empregado e dividendos mais baixos
2. A empresa não será capaz de aumentar significativamente seu ROE nos próximos 12-24 meses
3. O Dividend Yield permanecerá abaixo dos 6% por um período prolongado, refletindo a política atual da companhia em relação aos dividendos e à alocação do capital
4

→ Vault: [[EQTL3]]

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

- **P/E = 45.95** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 45.95** fora do screen.
- **P/B = 2.16** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **2.16** — verificar consistência com ROE.
- **DY = 5.18%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **5.18%** abaixo do floor — DRIP não-óbvio.
- **ROE = 6.98%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **6.98%** abaixo do critério.
- **Graham Number ≈ R$ 21.03** vs preço **R$ 44.11** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 18y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **P/E premium injustificado** — 45.95 contra ROE 6.98% sinaliza overvaluation severa. Trigger: `fundamentals.pe` > 30 mantém-se enquanto `roe` < 10%.
- 🔴 **ROE estrutural baixo** — bem abaixo do mínimo 15% para utility BR. Trigger: `fundamentals.roe` < 10% por 4 trimestres consecutivos.
- 🟡 **DY abaixo do mínimo** — 5.18% < 6% requerido. Trigger: `fundamentals.dy` < 6% (já actual; manter sob watch).
- 🟡 **Revisão tarifária ANEEL** — múltiplas distribuidoras (CEMAR, CELPA, CEPISA, EQTL Goiás) entram em ciclos diferentes. Trigger: anúncio ANEEL de revisão tarifária com WACC reduzido.
- 🟡 **Capex M&A intensivo** — modelo de roll-up de distribuidoras requer alavancagem contínua. Trigger: `fundamentals.net_debt_ebitda` > 4x.

## 6. Position sizing

**Status atual**: watchlist

Watchlist apenas — não na carteira; veredicto **AVOID** torna entry trigger restritivo. Re-entry só se P/E < 18 **e** ROE recuperar para ≥ 12% **e** DY ≥ 6% (combinação simultânea). Weight prudente máximo 3-4% se as condições convergirem. Cash exclusivo BRL (BR isolation), sem deploy DRIP enquanto múltiplos forem premium.

## 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe` ≥ 12% por 2 trimestres consecutivos.
- **P/E re-rating** — `fundamentals.pe` < 18 (sai de zona AVOID).
- **DY ≥ 6%** — `fundamentals.dy` ≥ 6% sustentado 2 trimestres.
- **Streak preservado** — `fundamentals.dividend_streak_years` < 18 sinaliza corte (red flag imediato).
- **Leverage breach** — `fundamentals.net_debt_ebitda` > 4x.

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
*Generated by `ii dossier EQTL3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
