---
type: research_dossie
ticker: VGIR11
name: Valora CRI
market: br
sector: Papel (CRI)
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, papel (cri)]
---

# 📑 VGIR11 — Valora CRI

> Generated **2026-04-26** by `ii dossier VGIR11`. Cross-links: [[VGIR11]] · [[VGIR11_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

VGIR11 é FII Papel/CRI (Valora) com **DY 15.63%** — top yield do bolso FII — streak 5y, market cap R$ 1.13B. **Synthetic IC: HOLD** (high confidence, 80% consensus) com composite **conviction 69**, thesis health 100. Achado-chave: yield estratosférico reflecte spread CRI sobre Selic (cenário macro alta de juros) — sustentado enquanto Selic não despencar; DRIP-friendly mas vigiar default rate dos CRIs subjacentes.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: n/a  |  **BVPS**: n/a
- **ROE**: n/a  |  **P/E**: n/a  |  **P/B**: n/a
- **DY**: 15.63%  |  **Streak div**: 5y  |  **Market cap**: R$ 1.13B
- **Last price**: BRL 9.79 (2026-04-26)  |  **YoY**: +5.8%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[VGIR11_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: A VGIR11 é uma excelente opção de investimento a longo prazo para um investidor Buffett/Graham, comprovada por seu histórico de cinco anos de dividendos consecutivos e um yield de 15,61%, que supera significativamente os rendimentos do mercado. Com uma capitalização de mercado de R$225 milhões e uma posição atual na carteira de R$17.369,28, a empresa oferece segurança através da consistência em dividendos e valorização patrimonial.

**Key assumptions**:
1. A VGIR11 manterá seu histórico de pagamentos de dividendos por mais cinco anos.
2. O preço atual do ativo (R$9,78) continuará a ser sustentável em relação ao mercado.
3. A empresa continuará a gerar lucros suficientes para cobrir seus dividendos e reinvestimentos.
4. A economia brasileira manterá um crescime

→ Vault: [[VGIR11]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **69** |
| Thesis health | 100 |
| IC consensus | 64 |
| Variant perception | 60 |
| Data coverage | 83 |
| Paper track | 30 |

## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **DY = 15.63%** → [[Glossary/DY|leitura + contraméricas]]. FIIs: target DY ≥ 8%. **15.63%** OK. ⚠️ DY > 15% frequentemente sinaliza **distress**, não oportunidade.
- **Streak div = 5y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.

## 5. Riscos identificados

- 🔴 **Default em CRIs subjacentes** — risco principal de papel; PDD sobe em ciclo Selic alta + recessão imobiliária. Trigger: relatório gerencial reportando CRI vencido > 3% do portfolio.
- 🟡 **Reset de IPCA / CDI nos CRIs** — distribuição segue indexador; queda de Selic ou desinflação corta DY. Trigger: `Selic < 11%` cumulativo OU `IPCA acumulado < 4%`.
- 🟡 **DY 15.63% é insustentável fora de regime de juros altos** — yield reflecte CDI+spread; reversão macro = reversão DY rápida. Trigger: `fundamentals.dy < 0.12` por 2 meses.
- 🟢 **Concentração emissor CRI** — risco se 1-2 emissores grandes defaultarem. Trigger: relatório gerencial reportando top-5 emissores > 50% do portfolio.
- 🟢 **Streak quebrado** — Trigger: distribuição mensal cair > 20% MoM sem ajuste de indexador.

## 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold** posição (user_pick); IC HOLD high confidence reforça. Cap em **5-8% do bolso BR de FIIs** dado risco CRI; não concentrar bloco Papel acima de 15% (combinar com outros CRIs diversifica). DRIP mensal mantém composto; **add com moderação** se DY > 15% e relatório gerencial limpo (default < 1%). BRL doméstico, sem conversão US→BR. **Honest projection**: distribuição actual NÃO é garantida em cenário de Selic em queda.

## 7. Tracking triggers (auto-monitoring)

- **DY abaixo do piso CRI** — `fundamentals.dy < 0.12` por 2 meses → reset de indexadores; revisar tese.
- **Selic em queda forte** — macro check `Selic < 11%` → spread CRI comprime, prep para DY drop.
- **Distribuição mensal cai** — `events.kind='dividend' AND amount < (avg ult 6m × 0.80)` → investigar relatório.
- **Default rate up** — relatório gerencial mensal com CRI vencido > 3% → considerar trim.
- **Conviction degrada** — `conviction.composite < 60` → re-avaliar.

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
*Generated by `ii dossier VGIR11` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
