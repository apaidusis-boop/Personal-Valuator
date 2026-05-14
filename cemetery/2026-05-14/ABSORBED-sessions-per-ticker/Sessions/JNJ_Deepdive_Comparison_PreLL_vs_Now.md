---
type: comparison
tags: [comparison, deepdive, jnj, phase-ll]
date: 2026-05-13
ticker: JNJ
old_run: 2026-04-29T21:05
new_run: 2026-05-13T22:48
---

# JNJ Deepdive — Antes (Pre-LL) vs Agora (Pós-LL)

> Comparação directa do mesmo ticker (JNJ) em 2 momentos:
> - **Pre-LL**: 2026-04-29 21:05 (single-source yfinance; sem Moat; sem data_confidence)
> - **Pós-LL**: 2026-05-13 22:48 (multi-source cascade: FMP+SEC XBRL+Fundamentus; com Moat 8.75; data_confidence ON; pipeline simplificado)
>
> Phase LL foi shipped 2026-05-08 noite — esta é a primeira oportunidade real de ver o efeito num ticker individual.

## 📊 O que mudou (data)

| Métrica | Pre-LL (29/Abr) | Pós-LL (13/Mai) | Δ | Interpretação |
|---|---:|---:|---:|---|
| **Price** | $227.79 | $230.24 | +$2.45 (+1.1%) | drift normal em 2 sem |
| **Market cap** | $548.3B | $554.2B | +$5.9B | acompanha o preço |
| **P/E trailing** | 26.40 | 26.68 | +1.1% | nada relevante |
| **P/E forward** | 17.92 | 18.11 | +1.1% | nada relevante |
| **P/B** | 6.73 | 6.82 | +1.3% | nada relevante |
| **EV/EBITDA** | 16.93 | 16.69 | −1.4% | melhorou ligeiramente |
| **Upside (target mean)** | 10.8% | 9.6% | −1.2pp | preço subiu, target mean não |
| **Piotroski F** | 4/9 | 4/9 | = | quality estável |
| **Altman Z** | 4.44 (safe) | 4.33 (safe) | −2.5% | só por price↑ → X4↓ |
| **Beneish M** | −2.29 (clean) | −2.29 (clean) | = | annual untouched |
| **ROE / ROA / GM** | 26.4% / 8.4% / 68.0% | 26.4% / 8.4% / 68.0% | = | annual fundamentals stable |
| **Short signal** | low | low | = | nada novo |
| **Insider** | bullish (65 buys) | bullish (63 buys) | −2 | sem mudança material |
| **Analyst consensus** | BUY (24 analysts) | BUY (24 analysts) | = | sem revision |

### Conclusão data
**Nada relevante mudou no underlying business em 2 semanas.** Tudo o que diferiu foi price-driven drift. Isto é **um bom sinal** — significa que a thesis fundamental do JNJ é estável, não está em zone de revisão.

## 🆕 O que é NOVO no pipeline Pós-LL

| Capability | Pre-LL | Pós-LL | Nota |
|---|:---:|:---:|---|
| **Moat Score** (`scoring/moat.py`) | ❌ ausente | ✅ **8.75/10 STRONG** | 4 sub-scores: pricing 10/10, capital_eff 7/10, runway 8/10, scale 10/10 |
| **Multi-source fundamentals cascade** | só yfinance | yfinance + SEC XBRL + Fundamentus | upstream em `derive_fundamentals_from_filings.py` |
| **Data confidence (3-way voting)** | ❌ | ✅ `analytics/data_confidence.py` | upstream — flagga disputed quando 2 fontes diferem |
| **Fair Value v2 banda + 6-stance action** | single number | banda + BUY/HOLD/AVOID/TRIM | em `scoring/fair_value.py` v2 |
| **Macro overlay gate** | ❌ | ✅ 4º gate | `config/macro_sector_fit.yaml` |
| **Filing Reactor (Phase KK)** | ❌ | ✅ `auto_verdict_on_filing.py` | re-roda fair_value em cada filing novo |
| **Historian delta** | só último run | versionado | há 5 runs JNJ pre-LL para comparar |

### Detalhe do Moat (NOVO — só existe pós-LL)
JNJ scored 8.75/10:
- **Pricing power**: 10/10 (gross margin 69%, CV 0.9% — fortíssima estabilidade)
- **Capital efficiency**: 7/10 (ROIC mediana 13%, persistência 100%)
- **Reinvestment runway**: 8/10 (revenue CAGR 5.6%, FCF/NI 84%)
- **Scale durability**: 10/10 (op margin +11pp delta, shares −8.8% buyback)
- **Anos usados**: 4 (2022-2025)
- **Label**: STRONG

JNJ era classificado como holding sólida antes; agora **temos a métrica numérica** para suportar.

## 🔧 O que mudou no PROCESSO (não no output)

### Pre-LL workflow (Apr 29)
```
ii deepdive JNJ
  → Auditor [Piotroski + Altman + Beneish]
  → Scout [news + insider + short + consensus]
  → Historian [delta vs last run]
  → Strategist [Llama dossier 5k word — opcional]
  → reports/deepdive/JNJ_*.json
```

### Pós-LL workflow (May 13)
```
ii deepdive JNJ
  → Auditor [Piotroski + Altman + Beneish + MOAT 🆕]
  → Scout [news + insider + short + consensus]
  → Historian [delta vs last run]
  → Strategist [Llama dossier — opcional]
  → reports/deepdive/JNJ_*.json
  ↑
  upstream invisível: fundamentals já passou por
  derive_fundamentals_from_filings.py (CVM/SEC XBRL primary)
  + data_confidence.py (3-way voting)
  + macro_gate (sector_fit overlay)
```

### Resumo das simplificações
1. **Mesma CLI**, mesmo JSON output schema (1 extra field `audit.moat`) — **zero quebra de retro-compatibilidade**.
2. **Upstream invisível**: o utilizador não chama `derive_fundamentals_from_filings.py` directamente; corre no cron noite. CLI ficou igual.
3. **Mais robusto a 1 fonte partir**: se yfinance der número errado, SEC XBRL/Fundamentus puxam de volta via data_confidence.
4. **Moat adicional** dá 1 sinal extra de conviction sem aumentar tempo de execução (já tinha fundamentals em DB).
5. **--no-llm** para iteração rápida; **com LLM** quando queres o dossier polido.

## 🐛 Falhas detectadas (no Pre-LL, agora resolvidas)

Comparando, eis falhas claras do output Pre-LL:
1. **Sem Moat**: não tinhas como saber se a "qualidade" do JNJ era sólida ou frágil. Hoje 8.75/10 STRONG é uma âncora.
2. **Single-source**: se yfinance.info tivesse um bug (acontece — ver `data_quality_dy_cagr`), Pre-LL fingia que estava certo. Hoje data_confidence flagga.
3. **Sem fair_value v2 banda**: Pre-LL não tinha banda de incerteza nem action 6-stance.
4. **Sem macro gate**: Pre-LL não cruzava holding com regime macro (expansion/recession/late_cycle).

## ✂️ Recomendação para os outros 7 pre-LL deepdives

Ficaram em `reports/deepdive/`:
- `ACN_deepdive_20260505_0639.json`
- `JNJ_deepdive_20260429_2105.json` ⭐ **manter para este comparison**
- `JNJ_deepdive_20260429_2106.json` (duplicado)
- `JNJ_deepdive_20260429_2107.json` (duplicado)
- `JNJ_deepdive_20260505_1934.json`
- `KO_deepdive_20260505_1935.json`
- `XPML11_deepdive_20260507_2335.json`
- `XPML11_deepdive_20260507_2336.json` (duplicado)

**Acção**:
- ✅ Manter `JNJ_deepdive_20260429_2105.json` como referência histórica para este comparison.
- ✂️ Bury os 7 restantes (incluindo duplicados) — info Pre-LL é unreliable e os tickers (ACN/JNJ/KO/XPML11) podem ser refrescados com pipeline current.
- 🔄 Após bury, re-correr `ii deepdive` para ACN, KO, XPML11 (3 holdings) com pipeline pós-LL para ter baseline limpa.

## 🔗 Cross-references
- [[Manual_do_Sistema#C. Deepdive — ticker on-demand]]
- [[CONSTITUTION]] — Phase LL changelog (shipped 2026-05-08 noite, ~13 commits)
- Memory: [[fair_value_forward_audit_2026-05-11]] · [[moat_engine_shipped]]
- Cemetery: `cemetery/2026-05-13/` (onde os outros pre-LL deepdives vão)
