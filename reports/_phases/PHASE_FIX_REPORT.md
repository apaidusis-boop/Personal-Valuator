---
type: phase_report
phase: FIX (sprint quick-fixes)
date: 2026-04-25
status: shipped
tokens_claude_pipeline: 0
---

# 🔧 Phase FIX — Quick-Fixes — SHIPPED

> 3 hot spots de qualidade resolvidos numa sessão. **Zero tokens Claude.**

## ✅ Fixes shipped

| # | Issue | Status | Impact |
|---|---|---|---|
| FIX.1 | Watchlist matches errados (5 tickers) | ✅ | ITUB4/SUZB3/TTEN3/EQTL3/ENGI11 corrigidos. **+15 tickers em quarterly_history (5→20).** |
| FIX.2 | Variant perception classifier bug | ✅ | "trim" matchava "patrimonial". Word-boundary regex. **HIGH variance falsos: 4→0.** |
| FIX.3 | Bank schema BBDC4/ITUB4 (BACEN) | ✅ | `cvm_parser_bank.py` + `bank_quarterly_history` table. **26 quarter-rows bancárias** (15 BBDC4 + 11 ITUB4). |

## 📊 Deltas mensuráveis

| Metric | Antes FIX | Depois FIX | Δ |
|---|---:|---:|---:|
| `quarterly_history` rows | 75 | 240 | +165 (3.2×) |
| Tickers com data CVM | 5 | 20 | +15 |
| `bank_quarterly_history` rows | 0 | 26 | NEW |
| Variant_perception HIGH variance falsos | 4 | 0 | -4 |
| Watchlist matches incorrect | 5 | 0 | -5 |

## 🎯 Material findings expostos pelos novos dados bancários

### BBDC4 (Bradesco) — forte recovery 2025
| Métrica | 2024 Q3 YTD | 2025 Q3 YTD | Δ YoY |
|---|---:|---:|---:|
| NII | R$ 49.0 bi | R$ 56.8 bi | **+16%** |
| Fee income | R$ 21.0 bi | R$ 23.0 bi | +9% |
| PDD (provision) | -R$ 18.4 bi | -R$ 21.7 bi | +18% (cost rising) |
| Net income | R$ 13.3 bi | **R$ 17.4 bi** | **+31%** |
| C/I ratio | 39-40% | 36-37% | improving |

→ **BBDC4 thesis materialmente mais bullish que ao ir dormir ontem.** Bradesco está em recovery clara — NII +16%, margens e net income subindo. PDD sobe mas em proporção menor que receita.

### ITUB4 (Itaú) — estagnação NII, eficiência compensa
| Métrica | 2024 Q3 YTD | 2025 Q3 YTD | Δ YoY |
|---|---:|---:|---:|
| NII | R$ 103.3 bi | R$ 102.9 bi | **flat** (-0.4%) |
| Fees | R$ 34.8 bi | R$ 34.4 bi | flat |
| PDD | -R$ 21.5 bi | -R$ 24.9 bi | +16% (rising) |
| Net income | R$ 31.0 bi | R$ 33.7 bi | +9% |
| C/I ratio | 45.1% | 43.1% | -2pp (improving) |

→ **ITUB4 sem crescimento receita** (NII e fees flat). Bottom line cresce só via efficiency e gestão fiscal. **Watch**: se PDD continuar a subir, o algorithm de "earn through cost-cuts" tem ceiling. ITUB4 thesis: review na próxima earnings (próxima ITR Q4 + DFP).

### Sector signal (ambos bancos)
- **PDD cresce dois-dígitos** em 2025 vs 2024 — sinal de **stress crediticio setorial** macro BR
- Ambos C/I < 45% — eficiência operacional alta (defesa em ambiente difícil)
- ITUB4 vs BBDC4: BBDC4 com momentum maior agora (mais convergência reflows)

## 🚦 Comandos novos shipped

```bash
# Bank schema parser (descrição-based, BBDC4 + ITUB4 + futuro BPAC11)
python -m library.ri.cvm_parser_bank build
python -m library.ri.cvm_parser_bank show BBDC4
python -m library.ri.cvm_parser_bank show ITUB4

# Watchlist novos tickers já em pipeline normal (após FIX.1):
python -m library.ri.cvm_parser show ITUB4
python -m library.ri.compare_releases ITUB4    # auto-gera vault timeline
```

## 🐛 Bugs corrigidos (silentes mas críticos)

1. **`variant_perception._classify_thesis_stance`**:
   - Bug: `if "trim" in text.lower()` matched `"patrimonial"` (substring)
   - Fix: word-boundary regex `\btrim\b`
   - Impact: 4 holdings falsamente flagados como HIGH VARIANCE SHORT
   - Aplicado **só** ao Core thesis paragraph (não Disconfirmation triggers, que sempre contêm bearish keywords by design)

2. **`cvm_filings.load_catalog_codes`**:
   - Bug: só lia `stocks` section, ignorava `watchlist_stocks` adicionada em Y.8
   - Fix: concat both buckets
   - Impact: 15 watchlist tickers começaram a ingerir CVM data

3. **Catalog matches** (5 tickers):
   - Bug: auto-populator usou substring match → ITUB4 → Itaúnense Energia (wrong); SUZB3 → Suzano Holding (wrong); etc.
   - Fix: lookup manual com CNPJ + cad_cia_aberta validation
   - Impact: dados ingeridos agora são **das empresas corretas**

## ⚠️ Limitations residuais (Y.9 future)

1. **Bank parser**: ainda assume DRE-based metrics. Não cobre Basel III ratios (CET1, RWA) que viriam dos relatórios prudenciais BACEN (não CVM).
2. **Total assets/equity** mostrando "3" e "2" trillion — display unit inconsistente (cosmético).
3. **ITRs YTD artifact** — `quarterly_single` resolveu para companhias normais; bank schema ainda não tem versão single-Q (próxima sessão se quiseres).
4. **Watchlist FIIs (16)** — ainda não no pipeline (só holdings 5).
5. **DFPs 2020-2023 backfilled** mas ITRs 2020-2023 não — para 24Q full por ticker (vs 15 actuais), baixar ITRs 2020-2023.

## 🪞 Auto-crítica (lessons learned)

**Bug pattern identificado**: substring matching em texto livre é frágil em PT (palavras compostas como "patrimonial", "intermediação"). Word-boundary é defensivo padrão.

**Auto-populator anti-pattern**: substring no `cvm_name` do universe.yaml é insuficiente quando há ambiguidade (ITUB4 = "Itaú Unibanco Holding" vs várias subs Itaú). Resolução manual com CNPJ é safer mas não-escalável. Para Y.10+: usar B3 listing API que mapeia ticker → ISIN → CNPJ official.

**Bank schema anti-pattern**: cada banco usa cd_conta diferente. Lookup por descrição é mais robusto mas precisa pattern library curado. Adicionar novos bancos = adicionar patterns.

## 🏆 Status pós-FIX

| Phase | Status |
|---|---|
| W (Skills Arsenal) | partial |
| X (Perpetuum Engine) | 9 perpetuums + Synthetic IC + variant_perception + earnings_prep + portfolio_stress |
| Y/Y.8 (RI Knowledge Base) | shipped |
| AA (Critical Thinking Stack) | shipped |
| **FIX (Quick-fixes)** | **shipped 2026-04-25 noite** |
| Z (UI Friendly Layer) | handoff pronto, pendente |

## 📋 Recomendação próxima sessão

**Phase Z (UI Friendly Layer)** agora faz sentido — dados estão limpos:
- 20 tickers com 11-15 quarters de history estruturada
- 2 bancos com schema próprio (cost-to-income, NII trajectory)
- Variant perception sem falsos positivos
- Catalog 100% validado contra CVM oficial

UI sobre dados ruins = noise amplificado. UI sobre dados limpos = leverage real.

Tokens Claude no pipeline FIX: **0**.
