---
type: research_dossie
ticker: ALOS3
name: Allos
market: br
sector: Real Estate
is_holding: False
date: 2026-04-26
verdict: HOLD
verdict_confidence: medium
verdict_consensus_pct: 60.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, real estate]
---

# 📑 ALOS3 — Allos

> Generated **2026-04-26** by `ii dossier ALOS3`. Cross-links: [[ALOS3]] · [[ALOS3_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

ALOS3 negocia a P/E 19.27 e P/B 1.20 com DY 7.17% (acima do floor 6%) e streak 6y, mas ROE 6.74% fica muito abaixo do exigido (15%). IC consensus HOLD (60%, medium) reflecte o trade-off: yield decente e P/B perto de 1× dão margem de segurança, mas a rentabilidade do equity é fraca para um operador de malls. Achado-chave: yield FII-like a 7%+ depois de subida de +49.9% YoY sugere que o mercado já reprecificou a tese de queda de juros — entrada nova exige confirmação de NOI/ABL.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.64  |  **BVPS**: 26.34
- **ROE**: 6.74%  |  **P/E**: 19.27  |  **P/B**: 1.20
- **DY**: 7.17%  |  **Streak div**: 6y  |  **Market cap**: R$ 15.78B
- **Last price**: BRL 31.61 (2026-04-24)  |  **YoY**: +49.9%

## 2. Synthetic IC

**🏛️ HOLD** (medium confidence, 60.0% consensus)

→ Detalhe: [[ALOS3_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-25)**: ALOS3 é um fundo imobiliário focado em ativos de tijolo, com um DY anualizado de 7.17%, ligeiramente abaixo da faixa ideal de 8-12% para FIIs no Brasil. Apresenta uma relação P/B de 1.20x, oferecendo margem de segurança considerável em comparação com a média do setor e um histórico consistente de pagamentos de dividendos por seis anos consecutivos.

**Key assumptions**:
1. Dividendos continuarão sendo pagos consistentemente nos próximos três anos
2. Taxa de vacância permanecerá estável ou diminuirá, mantendo a receita operacional
3. Net Debt/EBITDA se manterá abaixo dos 3.0x para garantir liquidez e capacidade de refinanciamento
4. A categoria tijolo (shoppings, lajes, logística) continuará sendo atrativa em termos de demanda imobiliária

**Disconfirmation tri

→ Vault: [[ALOS3]]

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

- **P/E = 19.27** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 19.27** passa.
- **P/B = 1.20** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.20** — verificar consistência com ROE.
- **DY = 7.17%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **7.17%** passa.
- **ROE = 6.74%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **6.74%** abaixo do critério.
- **Graham Number ≈ R$ 31.18** vs preço **R$ 31.61** → [[Glossary/Graham_Number|conceito]]. ❌ Acima do tecto Graham.
- **Streak div = 6y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **ROE estruturalmente baixo** — 6.74% vs critério 15%; sustenta tese de que valuation a 1.2× P/B já é fair value. Trigger: `fundamentals.roe < 8%` em 2 trimestres consecutivos.
- 🟡 **Vacância em malls** — ciclo macro (juros, consumo) pressiona ABL ocupada e renovação de aluguel. Trigger: NOI YoY negativo nos releases trimestrais (vault releases note).
- 🟡 **Compressão de valuation por juros** — DY 7.17% compete directamente com NTN-B; corte da Selic é tailwind, mas alta surpresa é veneno. Trigger: `macro.selic_meta` subir >25bp vs assumption.
- 🟡 **Streak div curto (6y)** — não atinge floor histórico de aristocratas; risco de corte se NOI cair. Trigger: dividendo trimestral abaixo dos últimos 4Q médios.

## 6. Position sizing

**Status atual**: watchlist

Watchlist BR isolada (não consumir caixa USD). Entry trigger: ROE >12% em 2 trimestres consecutivos OU pullback que leve P/B < 1.0× com DY ainda ≥7%. Weight prudente 3-5% como Tier-2 (real estate cíclico, não DRIP defensivo).

## 7. Tracking triggers (auto-monitoring)

- **ROE recovery** — `fundamentals.roe > 12%` por 2 trimestres → reavaliar BUY.
- **DY floor break** — `fundamentals.dy < 6%` → tese DRIP enfraquece.
- **P/B inflation** — `fundamentals.pb > 1.6` → margem de segurança evaporou.
- **Selic shock** — `macro.selic_meta` delta >+50bp vs último snapshot → revalidar valuation.
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
*Generated by `ii dossier ALOS3` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*

## 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-10 20:39 UTC · yt=0 · analyst=8 · themes=0_

### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | numerical | — | — | A concessão da Autopista Litoral Sul se estende até 2033. |
| 2026-04-24 | XP | rating | bull | — | [BTG Portfolio Dividendos] ALOS3 — peso 9.6%, setor Real Estate |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados a refinanciamentos, passivos intragrupo e investimentos programados. |
| 2026-04-24 | XP | thesis | bull | — | A Oncoclínicas apresenta um modelo de negócios integrado com crescimento sustentável nos últimos anos. |
| 2026-04-24 | XP | sector_view | neutral | — | O setor de tratamento do câncer tem fundamentos sólidos de longo prazo, impulsionado pelo envelhecimento da população e avanços n… |
| 2026-04-24 | XP | thesis | neutral | — | A concessão da Autopista Litoral Sul é madura e geradora de caixa, mas apresenta pontos de atenção relacionados à rentabilidade e… |
| 2026-04-24 | XP | risk | bear | — | Há riscos regulatórios e métricas de crédito da Arteris que podem impactar a Autopista Litoral Sul. |
| 2026-04-24 | XP | risk | bear | — | A empresa enfrenta riscos relacionados à continuidade operacional e descumprimento de covenants. |

