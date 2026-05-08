---
type: research_dossie
ticker: BN
name: Brookfield Corp
market: us
sector: Financials
is_holding: True
date: 2026-04-26
verdict: AVOID
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, financials]
---

# 📑 BN — Brookfield Corp

> Generated **2026-04-26** by `ii dossier BN`. Cross-links: [[BN]] · [[BN_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

BN cota P/E 92.82, DY 0.55% e ROE 1.95% (depressed por accounting GAAP que mascara fluxos do alternative asset platform) — POST-SPLIT 2023, tracking de shares ajustado. IC verdict **AVOID** (high confidence, 80% consensus); YoY +28.1% mas múltiplos GAAP enganadores — tese real é NAV-discount play sobre asset management franchise (BAM + private RE + infra). Manter como growth/holding NAV-arb, NÃO aplicar scorecard DRIP (DY 0.55% irrelevante e earnings GAAP não são proxy).

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 0.49  |  **BVPS**: 19.51
- **ROE**: 1.95%  |  **P/E**: 92.82  |  **P/B**: 2.33
- **DY**: 0.55%  |  **Streak div**: 40y  |  **Market cap**: USD 101.74B
- **Last price**: USD 45.48 (2026-04-26)  |  **YoY**: +28.1%

## 2. Synthetic IC

**🏛️ AVOID** (high confidence, 80.0% consensus)

→ Detalhe: [[BN_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: Brookfield Corp é uma excelente posição long-term para um investidor Buffett/Graham devido à sua consistência em dividendos, com 40 anos de crescimento contínuo e status de Dividend Aristocrat. Apesar do múltiplo P/E elevado (94.78), a empresa mantém um sólido ROE de 1.95% e uma relação patrimônio líquido/Patrimônio Líquido (P/B) de 2.38, indicando que o valor intrínseco pode estar subestimado em relação ao seu crescimento futuro. A empresa também possui um sólido coeficiente de endividamento EBITDA de 8.27 e uma razão corrente de 1.265, sugerindo capacidade financeira robusta.

**Key assumptions**:
1. Brookfield Corp continuará a aumentar seus dividendos por pelo menos mais cinco anos.
2. A empresa manterá um ROE acima de 1% nos próximos três anos.
3. O múlti

→ Vault: [[BN]]













## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 92.82** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 92.82** esticado vs critério.
- **P/B = 2.33** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **2.33** OK.
- **DY = 0.55%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.55%** fraco; verificar se é growth pick.
- **ROE = 1.95%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **1.95%** abaixo do critério.
- **Graham Number ≈ R$ 14.67** vs preço **R$ 45.48** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 40y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Real estate writedowns** — exposição commercial RE (escritórios LA / NY) ainda a marcar para baixo; NAV pode contrair. Trigger: `events.kind = '8-K'` com summary contendo 'impairment' ou 'writedown'.
- 🔴 **Holding NAV discount** — BN cota a discount sobre soma NAV das partes; discount pode persistir/alargar se mercado descrer da capacidade de monetizar private assets. Trigger: NAV/share ratio (10-K) > 1.4x preço.
- 🟡 **IC verdict AVOID (80% consensus)** — sinais de cautela do synthetic IC convergem; revisitar thesis vs valuation. Trigger: `conviction_scores.score < 50`.
- 🟡 **Post-split 2023 tracking** — número de shares pós-split deve ser confirmado em portfolio_positions (memória do user). Trigger: SQL audit `portfolio_positions` quantity vs broker statement YE2023.

## 5. Position sizing

**Status atual**: holding (in portfolio)

**HOLD com cautela** — NAV-discount play; AVOID do IC sugere não aumentar a estes níveis. Posição growth/holding (USD permanece em US, isolation rule); NÃO aplicar scorecard DRIP. Sizing máximo 4-5% do US book dado verdict AVOID; considerar trim se NAV discount fechar significativamente sem catalyst de monetização.

## 6. Tracking triggers (auto-monitoring)

- `events.kind = '8-K'` com 'impairment' / 'writedown' / 'real estate' → NAV pressure imediata.
- `conviction_scores.score < 50` → IC AVOID a consolidar; trim signal.
- DAM (Distributable Asset Management) earnings YoY < 5% → franchise growth a quebrar.
- `fundamentals.pe` GAAP > 100 ou prejuízo GAAP — irrelevante mas monitorar; usar DAM/share como proxy.
- `prices.close` drawdown > 25% vs ATH e NAV discount > 35% → re-avaliar entry, NÃO aumentar sem confirmação de catalyst.

## 7. Compute trail

| Stage | Tool | Tokens Claude |
|---|---|---|
| Recon DB | sqlite3 | 0 |
| Vault read | filesystem | 0 |
| IC + thesis (cached) | Ollama prior session | 0 |
| Skeleton render | Python f-string | 0 |
| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |

→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou ~600 tokens (re-fill narrativa).

---
*Generated by `ii dossier BN` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
