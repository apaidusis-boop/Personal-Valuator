---
type: research_dossie
ticker: ITSA4
name: Itaúsa
market: br
sector: Holding
is_holding: True
date: 2026-04-26
verdict: BUY
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, br, holding]
---

# 📑 ITSA4 — Itaúsa

> Generated **2026-04-26** by `ii dossier ITSA4`. Cross-links: [[ITSA4]] · [[ITSA4_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

ITSA4 negocia P/E 9.61, DY 8.63% e ROE consolidado 17.57% com streak de 20 anos — múltiplos compatíveis com critério Buffett/Graham. IC BUY (high confidence, 80% consensus); composite conviction 90 (top-3 da carteira). Tese central: holding discount play sobre ITUB4 — exposição barata ao banco #1 BR sem comprar ITUB4 a P/B 2.39, com payout estável + capital allocator disciplinado (Villela).

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.48  |  **BVPS**: 7.92
- **ROE**: 17.57%  |  **P/E**: 9.61  |  **P/B**: 1.80
- **DY**: 8.63%  |  **Streak div**: 20y  |  **Market cap**: R$ 159.43B
- **Last price**: BRL 14.22 (2026-04-26)  |  **YoY**: +37.2%

## 2. Synthetic IC

**🏛️ BUY** (high confidence, 80.0% consensus)

→ Detalhe: [[ITSA4_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: ITSA4 é holding do Itaú Unibanco com desconto
persistente vs NAV (~15-20%). Capital allocator disciplinado (Rodolfo Villela),
payout policy estável. ROE consolidado ~17% via ITUB + participações (Alpargatas, Dexco, Aegea).
DY actual 8.91% alinhado com Selic de mercado. Margin of safety vem do desconto
holding + quality do Itaú como banco #1 BR.

**Key assumptions**:
1. Itaú mantém ROE ≥15% (core driver, ~85% do NAV)
2. Desconto holding não supera 25% (ponto de TRIM se chegar lá)
3. Payout ≥90% do lucro recorrente
4. Capital allocation continua disciplinada (Villela)

**Disconfirmation triggers**:
- Itaú ROE < 12% em 2 quarters consecutivos
- Desconto NAV > 25% sem catalisador
- Mudança gestão Itaúsa / Villela sair
- Payout < 70% sem expansão clara

**Intent**:

→ Vault: [[ITSA4]]

## 4. Conviction breakdown

| Component | Score |
|---|---|
| **Composite** | **90** |
| Thesis health | 100 |
| IC consensus | 92 |
| Variant perception | 60 |
| Data coverage | 100 |
| Paper track | 90 |












## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 9.61** → [[Glossary/PE|porquê isto importa?]]. Graham (BR equity): P/E ≤ 22.5 (em conjunto com P/B). **Actual 9.61** passa.
- **P/B = 1.80** → [[Glossary/PB|leitura completa]]. BR equity: usado dentro do Graham. **1.80** — verificar consistência com ROE.
- **DY = 8.63%** → [[Glossary/DY|leitura + contraméricas]]. BR DRIP: DY ≥ 6%. **8.63%** passa.
- **ROE = 17.57%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **17.57%** compounder-grade.
- **Graham Number ≈ R$ 16.24** vs preço **R$ 14.22** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 20y** → [[Glossary/Dividend_Streak|porque importa]]. Target BR ≥ 5y; **passa**.

### Conceitos relacionados

- 💰 **Status DRIP-friendly** (BR holding com DY ≥ 6%) — reinvestimento mensal/quarterly compõe.
- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 5. Riscos identificados

- 🔴 **Concentração no Itaú (~85% NAV)** — qualquer choque ITUB4 propaga-se directamente. Trigger: ITUB4 ROE < 15% em 2 quarters (per disconfirmation trigger da thesis).
- 🟡 **Desconto holding alarga** — desconto >25% sem catalisador é sinal SELL na própria thesis. Trigger: monitor `(NAV - market_cap) / NAV > 0.25` 90d.
- 🟡 **Variant perception apenas 60** — consenso de mercado já reflectiu boa parte da tese; pouco edge informacional. Trigger: variant_perception score < 50.
- 🟡 **Risco de gestão** — saída de Villela mudaria capital allocation. Trigger: news/filings com mudança de management.
- 🟢 **Payout reduction** — payout < 70% sem expansão é trigger explícito. Trigger: `fundamentals.dy < 0.06` próximo trimestre.

## 6. Position sizing

**Status atual**: holding (in portfolio)

**Hold-to-add** — conviction 90, IC BUY, screen forte e tese DRIP genuína (streak 20y, DY 8.63%). Reinvestir dividendos via DRIP automático faz total sentido. Cash em BRL fica em BR (não converter); considerar acréscimo em pullbacks (DY > 9% ou desconto NAV > 20%) mas atenção à concentração bancária combinada com BBDC4 — ambos puxam exposição ao sector financeiro BR. Manter peso entre 8-12% da sleeve BR. Trim só se ITUB4 ROE colapsar abaixo de 12% sustentado.

## 7. Tracking triggers (auto-monitoring)

- **ITUB4 ROE colapsa** — `SELECT roe FROM fundamentals WHERE ticker='ITUB4' ORDER BY period_end DESC LIMIT 2` < 0.15 em 2 quarters
- **Itaúsa ROE consolidado** — `fundamentals.roe < 0.13` no próximo trimestre
- **Desconto NAV alarga** — monitor `(NAV - market_cap) / NAV > 0.25` 90d (requer NAV calc cross-holdings)
- **DY trap** — `fundamentals.dy < 0.06` (sinal payout reduction)
- **P/B premium** — `fundamentals.pb > 2.0 AND fundamentals.roe < 0.15`
- **Thesis health degrada** — `SELECT thesis_health FROM conviction_scores WHERE ticker='ITSA4'` < 70

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
*Generated by `ii dossier ITSA4` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
