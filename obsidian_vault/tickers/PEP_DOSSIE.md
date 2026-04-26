---
type: research_dossie
ticker: PEP
name: PepsiCo
market: us
sector: Consumer Staples
is_holding: False
date: 2026-04-26
verdict: BUY
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, consumer staples]
---

# 📑 PEP — PepsiCo

> Generated **2026-04-26** by `ii dossier PEP`. Cross-links: [[PEP]] · [[PEP_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

PepsiCo transaciona a P/E 24.40 com DY 3.66% e Dividend King de 55y — DY claramente acima do screen US (≥2.5%) embora P/E ligeiramente alto. IC Synthetic verdica BUY (60% consenso, medium confidence), o único BUY no grupo de watchlist. Achado-chave: ROE 43.88% combinado com YoY +14.9% sugere que a janela de entry óptima já passou parcialmente, mas DY sustentado e Aristocrat status mantêm-na qualificada para core DRIP.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 6.37  |  **BVPS**: 15.63
- **ROE**: 43.88%  |  **P/E**: 24.40  |  **P/B**: 9.94
- **DY**: 3.66%  |  **Streak div**: 55y  |  **Market cap**: USD 212.48B
- **Last price**: USD 155.44 (2026-04-24)  |  **YoY**: +14.9%

## 2. Synthetic IC

**🏛️ BUY** (medium confidence, 60.0% consensus)

→ Detalhe: [[PEP_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-26)**: PepsiCo, como um Dividend Aristocrat com 55 anos de histórico contínuo de dividendos e ROE de 43.88%, oferece valor duradouro em Consumer Staples. Apesar de não atender aos critérios estritos do valuation da filosofia (P/E > 20, P/B > 3), a empresa mantém um DY sólido de 3.66% e uma posição financeira robusta com Net Debt/EBITDA de 2.24.

**Key assumptions**:
1. A PepsiCo continuará a expandir suas operações globais, impulsionando o crescimento sustentável
2. O setor de Consumer Staples permanecerá resiliente em tempos econômicos incertos
3. PepsiCo manterá seu histórico consistente de dividendos e potencialmente aumentará o dividendo anualmente
4. A empresa continuará a gerir efetivamente suas dívidas, mantendo uma posição financeira sólida

**Disconfirmation

→ Vault: [[PEP]]




## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 24.40** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 24.40** esticado vs critério.
- **P/B = 9.94** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **9.94** esticado.
- **DY = 3.66%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **3.66%** OK.
- **ROE = 43.88%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **43.88%** compounder-grade.
- **Graham Number ≈ R$ 47.33** vs preço **R$ 155.44** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 55y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Volume decline persistente** — Frito-Lay e Beverages com volumes negativos enquanto pricing sustenta receita. Trigger: volume growth YoY negativo por 3 quarters em earnings transcripts (yt_digest).
- 🟡 **GLP-1 staples impact** — snacks/beverages açucarados em risco estrutural. Trigger: revenue growth YoY < 2% sustained.
- 🟡 **FX EM headwind** — exposição LatAm/Europa significativa (~40% revenue). Trigger: DXY > 110 sustained AND organic vs reported gap > 400bps.
- 🟡 **Pricing power vs private label** — trade-down acelera em recessão; Walmart/Costco apertam shelf. Trigger: gross margin contracts > 150bps YoY.
- 🟢 **Múltiplo elevado pós-rally +14.9%** — entry premium reduz margem de segurança. Trigger: P/E > 26 sustained sem earnings re-acceleration.

## 5. Position sizing

**Status atual**: watchlist

Watchlist com IC BUY — single best candidate do grupo. Considerar entry inicial 3-5% da sleeve US se P/E recuar para ≤22 (DY já passa screen com 3.66%); rally YoY +14.9% sugere esperar pullback antes de starter position. Dividend King 55y é core DRIP US qualificado. Cash USD permanece em US (BR/US isolation).

## 6. Tracking triggers (auto-monitoring)

- `fundamentals.pe < 22 AND fundamentals.dy > 3.5%` — entry condition watchlist (DY já dá pass; falta P/E).
- `fundamentals.roe < 25%` por 2Q — quality compression alerta thesis.
- `fundamentals.net_debt_ebitda > 3.0` — disconfirmation (actual 2.24).
- `events WHERE kind='earnings' AND summary LIKE '%volume%negative%'` por 3Q — volume thesis break.
- `scores.score > 75` AND screen passes — promover para entry.

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
*Generated by `ii dossier PEP` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
