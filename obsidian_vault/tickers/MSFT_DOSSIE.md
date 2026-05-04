---
type: research_dossie
ticker: MSFT
name: Microsoft
market: us
sector: Technology
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, technology]
---

# 📑 MSFT — Microsoft

> Generated **2026-04-26** by `ii dossier MSFT`. Cross-links: [[MSFT]] · [[MSFT_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

Microsoft transaciona a P/E 26.59 com DY apenas 0.82% e streak de 24y — falha screen US tanto em P/E (≤20) como em DY (≥2.5%). IC Synthetic verdica HOLD com high confidence (80% consenso, o mais robusto do grupo watchlist). Achado-chave: thesis é compounder/growth, não DRIP — entry justifica-se por moat (Azure + M365 + GitHub Copilot) e ROE 34.39% sustentado, não por yield; AI capex cycle é o swing variable.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 15.97  |  **BVPS**: 52.62
- **ROE**: 34.39%  |  **P/E**: 26.59  |  **P/B**: 8.07
- **DY**: 0.82%  |  **Streak div**: 24y  |  **Market cap**: USD 3155.94B
- **Last price**: USD 424.62 (2026-04-24)  |  **YoY**: +9.6%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[MSFT_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-26)**: Microsoft é líder em tecnologia com forte ROE de 34.39%, embora apresente um P/E de 26.61 e um P/B de 8.07, que excedem os critérios da filosofia value-investor. A empresa mantém uma sólida tradição de dividendos por 24 anos consecutivos.

**Key assumptions**:
1. Microsoft continuará a expandir suas margens e lucratividade
2. A demanda por soluções em nuvem e inteligência artificial permanecerá robusta
3. A empresa manterá sua política de dividendos estável e crescente
4. O mercado reconhecerá o valor intrínseco da Microsoft, reavaliando suas métricas financeiras

**Disconfirmation triggers**:
- ROE cai abaixo de 15% por dois trimestres consecutivos
- P/E ultrapassa 30 por três trimestres seguidos
- A empresa reduz ou congela o dividendo após 24 anos de pagame

→ Vault: [[MSFT]]










## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 26.59** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 26.59** esticado vs critério.
- **P/B = 8.07** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **8.07** esticado.
- **DY = 0.82%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.82%** fraco; verificar se é growth pick.
- **ROE = 34.39%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **34.39%** compounder-grade.
- **Graham Number ≈ R$ 137.51** vs preço **R$ 424.62** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 24y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Azure growth deceleration** — segmento sustenta múltiplo; queda abaixo de 25% YoY constant currency é red flag. Trigger: revenue growth Azure YoY < 25% por 2Q em earnings transcripts (yt_digest).
- 🔴 **AI capex returns inadequados** — $80B+/ano capex requer ROIC>WACC; risco de overinvestment. Trigger: capex/revenue > 30% AND operating margin contracts > 200bps.
- 🟡 **OpenAI relationship complexity** — equity stake + IP rights + competitive overlap; qualquer ruptura é evento material. Trigger: events com kind='strategic' AND summary LIKE '%OpenAI%'.
- 🟡 **Antitrust EU/UK/FTC** — Activision deal sob scrutiny; bundling Teams já levou a unbundling forçado. Trigger: events com kind='regulatory' AND ticker='MSFT'.
- 🟢 **Múltiplo elevado vs screen** — DY 0.82% confirma entry não é DRIP. Trigger: P/E > 30 sustained reabre disconfirmation thesis.

## 5. Position sizing

**Status atual**: watchlist

Watchlist — não é trade signal. Considerar entry inicial 3-5% da sleeve US apenas se P/E recuar para ≤22 com Azure growth ainda > 25% YoY (compounder thesis intact). DY 0.82% deixa MSFT fora do core DRIP — entry seria por compounder/quality, não por yield. Cash USD permanece em US (BR/US isolation); não converter BRL.

## 6. Tracking triggers (auto-monitoring)

- `fundamentals.pe < 22` — entry condition compounder (DY screen ignorado dado thesis).
- `fundamentals.roe < 25%` por 2Q — quality compression alerta thesis.
- `events WHERE kind='earnings' AND summary LIKE '%Azure%' AND growth_pct < 25` por 2Q — disconfirmation core.
- `events WHERE kind='regulatory' AND ticker='MSFT'` — antitrust EU/FTC tracking.
- `scores.score > 75` AND macro 10y < 4% — promover de watchlist a entry.

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
*Generated by `ii dossier MSFT` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
