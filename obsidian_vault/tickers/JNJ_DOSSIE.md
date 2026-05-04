---
type: research_dossie
ticker: JNJ
name: Johnson & Johnson
market: us
sector: Healthcare
is_holding: True
date: 2026-04-26
verdict: MIXED
verdict_confidence: low
verdict_consensus_pct: 40.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, healthcare]
---

# 📑 JNJ — Johnson & Johnson

> Generated **2026-04-26** by `ii dossier JNJ`. Cross-links: [[JNJ]] · [[JNJ_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

JNJ negoceia a P/E 26.4 com DY 2.29% e ROE robusto de 26.4%, mas o IC fica MIXED (40% consenso, baixa confiança) — múltiplo esticado vs histórico Buffett. Achado-chave: **Dividend King com 65 anos consecutivos de aumentos**, qualidade defensiva inquestionável, mas valuation premium pede paciência antes de novos reforços. YoY +47.2% reflecte rotação defensiva — risco de mean-reversion no múltiplo.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 8.62  |  **BVPS**: 33.87
- **ROE**: 26.42%  |  **P/E**: 26.39  |  **P/B**: 6.72
- **DY**: 2.29%  |  **Streak div**: 65y  |  **Market cap**: USD 547.64B
- **Last price**: USD 227.50 (2026-04-26)  |  **YoY**: +47.2%

## 2. Synthetic IC

**🏛️ MIXED** (low confidence, 40.0% consensus)

→ Detalhe: [[JNJ_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: Johnson & Johnson é uma excelente posição de longo prazo para um investidor Buffett/Graham, comprovada por seu sólido histórico de dividendos e crescimento sustentável. A empresa mantém uma renda anualizada de 2,3% (DY), um P/E razoável de 20,5 vezes o lucro por ação (EPS) de $11,03, e uma relação Patrimônio Líquido/Patrimônio Bruto (PB) de 6,7. Com uma tradição inigualável de aumentos de dividendos consecutivos por 65 anos como Dividend Aristocrat, Johnson & Johnson demonstra consistência financeira e gerenciamento robusto.

**Key assumptions**:
1. A empresa continuará a crescer seus dividendos anualmente.
2. O P/E da empresa permanecerá dentro de um intervalo razoável entre 18-23 vezes EPS.
3. A relação Patrimônio Líquido/Patrimônio Bruto (PB) não ultrapassa

→ Vault: [[JNJ]]










## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 26.39** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 26.39** esticado vs critério.
- **P/B = 6.72** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **6.72** esticado.
- **DY = 2.29%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **2.29%** fraco; verificar se é growth pick.
- **ROE = 26.42%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **26.42%** compounder-grade.
- **Graham Number ≈ R$ 81.05** vs preço **R$ 227.50** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 65y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**. Eligível [[Glossary/Aristocrat|Aristocrat]] se ≥ 25y.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🟡 **Pipeline replacement (Stelara biosimilars)** — Stelara perde exclusividade 2025+, biosimilars vão erodir margens Innovative Medicine. Trigger: `fundamentals.eps` YoY < -5% por 2 trimestres consecutivos.
- 🟡 **Talc litigation overhang** — provisões cobrem mas verdicts adversos podem reabrir liability. Trigger: `events` table novo settlement > USD 1B.
- 🟡 **Valuation stretch** — P/E 26.4 acima da média histórica 18-22 e do screen US (≤20). Trigger: `fundamentals.pe > 28` por 2 quarters.
- 🟢 **Pricing power MedTech** — sector com tailwind demográfico mas concorrência (MDT, ABT) intensa.

## 5. Position sizing

**Status atual**: holding (in portfolio)

**Manter DRIP ligado** — Dividend King clássico para o sleeve defensivo US. Não acelerar reforços com P/E 26+ acima da banda histórica; aguardar dips para -10% para adicionar. USD permanece em conta US (isolamento de moeda).

## 6. Tracking triggers (auto-monitoring)

- **ROE quebra** — `fundamentals.roe < 0.15` por 2 trimestres → reavaliar economic moat.
- **PE overstretch** — `fundamentals.pe > 30` → trim candidate, valuation desligada do fundamental.
- **DY break aristocrat streak** — qualquer corte ou freeze do dividendo em `dividend feed` → tese DRIP comprometida.
- **Earnings miss material** — `events.kind='earnings'` com surprise < -10% → atualizar thesis.
- **Conviction drop** — `conviction_scores.composite_score < 60` → revisar e considerar reduce.

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
*Generated by `ii dossier JNJ` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
