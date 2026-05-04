---
type: research_dossie
ticker: XP
name: XP Inc
market: us
sector: Financials
is_holding: True
date: 2026-04-26
verdict: HOLD
verdict_confidence: high
verdict_consensus_pct: 80.0
sources: [in-house DB, Synthetic IC, vault thesis]
tokens_claude_data_gather: 0
tags: [research, dossie, us, financials]
---

# 📑 XP — XP Inc

> Generated **2026-04-26** by `ii dossier XP`. Cross-links: [[XP]] · [[XP_IC_DEBATE]] · [[CONSTITUTION]]

## TL;DR

XP negoceia P/E 10.12, DY 0.91% e ROE 23.71% com YoY +23.7% — broker BR listado no NASDAQ, growth pick não DRIP. IC verdict **HOLD** (high confidence, 80% consensus); valuation barato reflecte ciclo Selic alta a comprimir trading volumes mas custódia AUM continua a escalar. Tese central: scale do BR retail broker + diversificação para banking/seguros, não yield — manter como growth, não aplicar scorecard DRIP.

## 1. Fundamentals snapshot

- **Período**: 2026-04-25
- **EPS**: 1.95  |  **BVPS**: 9.08
- **ROE**: 23.71%  |  **P/E**: 10.12  |  **P/B**: 2.17
- **DY**: 0.91%  |  **Streak div**: 8y  |  **Market cap**: USD 10.21B
- **Last price**: USD 19.74 (2026-04-26)  |  **YoY**: +23.7%

## 2. Synthetic IC

**🏛️ HOLD** (high confidence, 80.0% consensus)

→ Detalhe: [[XP_IC_DEBATE]]

## 3. Thesis

**Core thesis (2026-04-24)**: XP Inc é uma empresa sólida no setor financeiro com um histórico de crescimento sustentado e dividendos consistentes, o que a torna atrativa para investidores Buffett/Graham. Com um P/E de 10,41 vezes e um ROE de 23,71%, XP Inc oferece uma combinação equilibrada entre valor e crescimento. A empresa mantém um rendimento anual de dividendos de 8,91% e já estendeu seu streak de pagamentos por oito anos consecutivos, demonstrando sua capacidade de gerar lucros consistentes.

**Key assumptions**:
1. XP Inc continuará a expandir seus serviços financeiros digitais no Brasil.
2. A empresa manterá um crescimento sustentável em EPS nos próximos anos.
3. O ROE permanecerá acima dos 20% ao longo do tempo, refletindo eficiência operacional.
4. XP Inc continuará a aumentar

→ Vault: [[XP]]










## Tutor

> Leitura métrica-por-métrica vs filosofia (CLAUDE.md screen). Cada link abre [[Glossary/_Index|Glossary]] para fórmula + contraméricas.

- **P/E = 10.12** → [[Glossary/PE|porquê isto importa?]]. Buffett quality: P/E ≤ 20. **Actual 10.12** passa.
- **P/B = 2.17** → [[Glossary/PB|leitura completa]]. US: P/B ≤ 3. **2.17** OK.
- **DY = 0.91%** → [[Glossary/DY|leitura + contraméricas]]. US Buffett DRIP: DY ≥ 2.5%. **0.91%** fraco; verificar se é growth pick.
- **ROE = 23.71%** → [[Glossary/ROE|porque é a métrica chave Buffett]]. Buffett quality: ≥ 15%. **23.71%** compounder-grade.
- **Graham Number ≈ R$ 19.96** vs preço **R$ 19.74** → [[Glossary/Graham_Number|conceito]]. ✅ Tem margem de segurança Graham.
- **Streak div = 8y** → [[Glossary/Dividend_Streak|porque importa]]. Target US ≥ 10y; curto.

### Conceitos relacionados

- 🛡️ **Princípios fundacionais**: [[Glossary/Margin_of_Safety|margem de segurança]] (Graham) + [[Glossary/Moat|moat]] (Buffett). Sem ambos, qualquer screen é teatro.

## 4. Riscos identificados

- 🔴 **Ciclo Selic / take-rate** — receita ligada a volume de trading e net interest; Selic em pico comprime equities flow. Trigger: `macro_exports/SELIC_DAILY.csv` Selic > 14% por 6m + revenue YoY < 5%.
- 🟡 **Regulatório CVM** — pressão sobre rebates, kickbacks e suitability rules pode comprimir margens. Trigger: `events.source='cvm'` com kind='regulation' e summary contendo 'rebate' ou 'comissão'.
- 🟡 **Concorrência BTG / Itaú** — bancões a copiar modelo XP via plataformas próprias; perda de market share AUM. Trigger: AUM YoY growth < 10%.
- 🟢 **Listing US** — exposição USD ao earnings BRL gera FX translation noise; gerível. Trigger: USDBRL move > 10% num trimestre.

## 5. Position sizing

**Status atual**: holding (in portfolio)

**HOLD** — growth pick BR-broker listado em USD (cash USD permanece em US, regra de isolation). Não aplicar scorecard DRIP (DY 0.91% não qualifica e a intenção é capital appreciation via scale broker BR). Sizing prudente até 5-7% do US book; aumentar em deeps (P/E < 8) ou se Selic iniciar ciclo de corte (catalyst para volumes).

## 6. Tracking triggers (auto-monitoring)

- `fundamentals.pe > 15` → premium injustificado vs hist 8-12 broker BR.
- `fundamentals.roe < 18%` por 2 trimestres → operational deleverage do cycle.
- Earnings miss > 10% (revenue ou net income vs consensus) → `quarterly_history` YoY revenue < 5%.
- `macro_exports/SELIC_DAILY.csv` corte > 200bps em 12m → catalyst para volumes (signal de aumento).
- `conviction_scores.score < 55` → tese growth a degradar.

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
*Generated by `ii dossier XP` on 2026-04-26. 100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*
