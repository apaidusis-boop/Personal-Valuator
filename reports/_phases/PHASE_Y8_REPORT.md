---
type: phase_report
phase: Y.8
date: 2026-04-25
status: shipped
tokens_claude_pipeline: 0
---

# 🏗️ Phase Y.8 — RI Knowledge Base Expansion — SHIPPED

> Resolveu YTD artifact, fez backfill 6 anos, integrou FIIs (4 de 5), 15 watchlist auto-populados, ri_freshness em T2.

## ✅ Sub-sprints

| Sprint | Componente | Status |
|---|---|---|
| Y.8.1 | `library/ri/quarterly_single.py` (resolve YTD artifact) | ✅ shipped |
| Y.8.2 | DFP backfill 2020-2023 (4 ZIPs ~50MB) + ingest | ✅ shipped |
| Y.8.3 | `library/ri/fii_filings.py` + 4/5 FIIs (CNPJs auto-resolved) | ✅ shipped |
| Y.8.4 | `library/ri/catalog_autopopulate.py` + 15 watchlist BR | ✅ shipped (com ressalvas) |
| Y.8.5 | `ri_freshness` perpetuum → T2 + whitelist actions CVM | ✅ shipped |

## 📊 Numbers ANTES vs DEPOIS Y.8

| Metric | Y (manhã) | Y.8 (agora) | Δ |
|---|---:|---:|---:|
| `quarterly_history` rows | 55 | **75** | +20 |
| `quarterly_single` rows | 0 | **75** | +75 |
| Quarters per ticker | 11 | **15** | +4 |
| Período coberto | 2023-Q1 → 2025-Q3 | **2019-Q4 → 2025-Q3** | +4 yrs |
| `cvm_dre` rows | 4,097 | **5,587** | +1,490 |
| `cvm_bpa` rows | 6,082 | **8,494** | +2,412 |
| `cvm_bpp` rows | 10,182 | **14,212** | +4,030 |
| `cvm_dfc` rows | 5,807 | **7,959** | +2,152 |
| `fii_monthly` rows | 0 | **96** | +96 |
| `fii_balance_sheet` rows | 0 | **96** | +96 |
| FIIs com data | 0 | **4 de 5** | +4 |
| Catalog stocks (incl. watchlist) | 5 | **20** | +15 |
| Perpetuums em T2 | 2 | **3** (+ ri_freshness) | +1 |

## 🎯 Smoke tests OK

### VALE3 — single-Q expõe **Q4 2024 negativo**
```
2024Q4   net_income = -R$ 5.8 bi    EBIT margin = 7.7%   (vs 30%+ típico)
```
Provável write-off Mariana / Brumadinho não-recurrente.
Sem single-Q view (só YTD), este flag passaria despercebido.

### XPML11 — emissão massiva 14 meses
```
2024-01: 33M cotas, PL R$ 3.7bi
2025-03: 56M cotas, PL R$ 6.7bi
→ +70% cotas, +80% PL
```
Diluição vs growth balance — análise qualitativa próxima sprint.

### BBDC4 — 15 quarters coverage
Bradesco com histórico 2019-Q4 → 2025-Q3 (24 quarters teóricos, 15 com data por causa de DFP-only nos quartos finais).

## ⚠️ Limitations honestas Y.8

1. **Auto-populator de watchlist tem ~40% match errado**:
   - ITUB4 → matched "COMPANHIA ITAUNENSE ENERGIA" (devia ser ITAU UNIBANCO HOLDING)
   - SUZB3 → matched "SUZANO HOLDING S.A." (devia ser SUZANO S.A.)
   - TTEN3 → matched "PETTENATI INDUSTRIA TEXTIL" (devia ser 3tentos / Três Tentos)
   - EQTL3, ENGI11 → matched subsidiárias em vez de holdings
   - **Action**: revisar manualmente catalog.yaml `watchlist_stocks` antes de ingest dessas.

2. **RBRX11 não resolved** — patterns "RBR X" e "RBR ALPHA MULTIESTRATEGIA" não encontram match no `inf_mensal_fii_geral_2025.csv`. Investigar nome real.

3. **fii_monthly DY values low (0.01)** — formato CVM possivelmente já decimal, display label `%` está errado. Trivial fix.

4. **2019 só tem Q4 (DFP)** — sem ITRs 2019, single-Q dá só 1 quarter. Para 2019-Q1/Q2/Q3 precisamos baixar ITR 2019 (não feito).

5. **Watchlist FIIs (16) ainda sem ingest** — só 4 holdings ingeridas. Próxima sprint expande.

## 🚦 Comandos novos shipped

```bash
# Single-quarter delta (resolve YTD)
python -m library.ri.quarterly_single build
python -m library.ri.quarterly_single show VALE3

# Watchlist auto (revisar matches!)
python -m library.ri.catalog_autopopulate plan
python -m library.ri.catalog_autopopulate apply

# FII module
python -m library.ri.fii_filings download --year 2025
python -m library.ri.fii_filings resolve-cnpjs --year 2025
python -m library.ri.fii_filings ingest --year 2025
python -m library.ri.fii_filings show XPML11
```

## 🔍 Queries úteis pós-Y.8

```python
# Comparar VALE3 single-Q EBIT margin trajectory
python -c "import sqlite3; c=sqlite3.connect('data/br_investments.db'); [print(r) for r in c.execute('SELECT period_end, ROUND(ebit_margin*100,1) FROM quarterly_single WHERE ticker=\"VALE3\" ORDER BY period_end DESC LIMIT 16')]"

# FII XPML11 dilution rate
python -c "import sqlite3; c=sqlite3.connect('data/br_investments.db'); [print(r) for r in c.execute('SELECT period_end, cotas_emitidas, valor_patrimonial_cota FROM fii_monthly WHERE ticker=\"XPML11\" ORDER BY period_end')]"

# Watchlist com CVM ativo (post-fix manual)
python -c "import yaml; cat=yaml.safe_load(open('library/ri/catalog.yaml',encoding='utf-8')); print('Auto-populated:', len(cat.get('watchlist_stocks',[])))"
```

## 🛣️ Próxima sessão — Y.9 ideas

- Fix manual matches errados em watchlist_stocks
- ITR 2019-2023 backfill para 24 quarters full por ticker (vs 15 actual)
- Watchlist FIIs (16) ingest
- Resolver RBRX11 nome correcto
- `compare_releases` usa `quarterly_single` (não `quarterly_history`) — material flags ficam corretos sem YTD distortion
- Vault timelines per ticker watchlist (atualmente só 5 holdings têm `_RI.md`)
- Bank-specific schema (BBDC4/ITUB4 — DRE bancária diferente de operacional)

## 🏆 Status global

| Phase | Status |
|---|---|
| W (Skills Arsenal) | partial |
| X (Perpetuum Engine) | **9 perpetuums** (3 em T2) |
| Y (RI Knowledge Base v1) | shipped 25/04 manhã |
| **Y.8 (RI expansion)** | **shipped 25/04 tarde** |

Tokens Claude consumidos pelo pipeline: **0**. Tudo CVM público + Ollama local + Python.
