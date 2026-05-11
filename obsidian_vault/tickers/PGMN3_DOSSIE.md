---
type: research_dossie
ticker: PGMN3
name: Pague Menos
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

# 📑 PGMN3 — Pague Menos

> Generated **2026-04-26** by `ii dossier PGMN3`. Cross-links: [[PGMN3]] · [[PGMN3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PGMN3 negocia P/E 13.57 e P/B 1.22 (perto do livro) com DY 4.50% e ROE 8.97% — abaixo do critério Graham (DY 6%, ROE 15%). IC consensus HOLD com confiança máxima (100%) — ninguém diverge: empresa em fase de turnaround com fundamentos médios. Achado-chave: subida de +66.2% YoY já reprecificou a tese contrarian; entrada nova precisa de prova de melhoria de margem retalho ou expansão da clínica.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.42  |  **BVPS**: 4.68
- **ROE**: 8.97%  |  **P/E**: 13.57  |  **P/B**: 1.22
- **DY**: 4.50%  |  **Streak div**: 3y  |  **Market cap**: R$ 4.30B
- **Last price**: BRL 5.70 (2026-04-24)  |  **YoY**: +66.2%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 100.0% consensus)

→ Detalhe: [[PGMN3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: A PGMN3, uma empresa do setor de Consumer Staples, apresenta um valuation atrativo com P/E de 13.57 e P/B de 1.22, embora não atenda aos critérios rigorosos da filosofia value-investimento ajustada à Selic alta (Graham clássico). A empresa tem uma taxa de dividendos de 4.50% e um ROE de 8.97%, indicando potencial para melhorias em eficiência operacional.

**Key assumptions**:
1. A PGMN3 manterá sua posição no mercado brasileiro, mantendo margens estáveis
2. O cenário macroeconômico do Brasil continuará a suportar o consumo de bens essenciais
3. A empresa aumentará seus esforços para melhorar seu ROE e reduzir sua dívida líquida/EBITDA
4. Os dividendos continuarão sendo pagos, mesmo com a atual crise econômica

**Disconfirmation triggers**:
- ROE cai abaixo de

→ Vault: [[PGMN3]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **67** |
| Thesis health | 92 |
| IC consensus | 50 |
| Variant perception | 50 |
| Data coverage | 50 |
| Paper track | 70 |

## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 13.57** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 13.57** passa.
- **P/B = 1.22** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.22** — verificar consistência com ROE.
- **DY = 4.50%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **4.50%** abaixo do floor — DRIP não-óbvio.
- **ROE = 8.97%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **8.97%** abaixo do critério.
- **Graham Number ≈ R$ 6.65** vs preço **R$ 5.70** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 3y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Margem retalho farma sob pressão** — sector altamente competitivo (RaiaDrogasil, Pague Menos, redes regionais); ROE 8.97% reflecte essa compressão. Trigger: `fundamentals.roe < 7%` em 2 trimestres.
- 🟡 **Streak div curta (3y)** — sem track record para sustentar tese DRIP. Trigger: dividendo trimestral abaixo da média móvel 4Q.
- 🟡 **Competição RD/Drogasil** — peer maior tem economias de escala; risco de perda de share. Trigger: gross margin YoY <-100bp em release.
- 🟡 **Reprecificação esticada** — +66% YoY pode ter consumido upside; reversão rápida possível. Trigger: `prices.close` queda >-15% em 30d.
- 🟢 **Valuation moderado** — P/B 1.22 dá floor parcial; risco de mark-down limitado. Trigger: `fundamentals.pb > 1.8` para alerta.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR (caixa BRL only). Entry trigger: ROE recovery >12% em 2 trimestres OU pullback significativo (>-20%) que recoloque DY próximo a 6%. Weight prudente 2-3% como Tier-2 (mid-cap consumer staples, tese turnaround não consolidada).

## 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → confirma turnaround.
- **DY upgrade** — `fundamentals.dy > 6%` → entra critério Graham.
- **Margin compression** — `fundamentals.eps` YoY <-15% → sector pressure confirmada.
- **Pullback técnico** — `prices.close` queda >-20% em 60d com fundamentos intactos → entry zone.
- **Thesis health** — `conviction_scores.composite_score < 55` → flag review.

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
*Generated by `ii dossier PGMN3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

## 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-10 20:39 UTC · yt=0 · analyst=8 · themes=0_

### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | rating | bull | 8.50 | Recomendação de compra para PGMN3 com preço-alvo de R$8,5/ação até o final de 2026. |
| 2026-04-24 | XP | thesis | bull | — | A produtividade das lojas da PGMN deve melhorar continuamente até atingir ~R$965 mil por loja no final de 2026. |
| 2026-04-24 | XP | numerical | neutral | — | O valuation atual é atrativo, negociado a ~10,5x P/L 2026. |
| 2026-04-24 | XP | catalyst | bull | — | Os genéricos de semaglutida devem começar a ser vendidos no segundo semestre de 2026, com um mercado endereçável que pode surpree… |
| 2026-04-24 | XP | numerical | bull | — | O GLP-1 deve responder por cerca de ~1/3 do crescimento da PGMN em 2026. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] PGMN3 — peso 9.6%, setor Consumer Staples |
| 2026-04-24 | XP | rating | bull | — | [BTG Value] PGMN3 — peso 1.8% |
| 2026-04-24 | XP | catalyst | bull | — | A PGMN deve se beneficiar da tendência estrutural de GLP-1, com aceleração prevista à frente. |

