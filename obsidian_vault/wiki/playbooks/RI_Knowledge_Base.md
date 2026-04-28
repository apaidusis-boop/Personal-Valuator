---
type: playbook
name: RI Knowledge Base — CVM official filings → quarterly_history
tags: [playbook, ri, cvm, quarterly, bank_parser]
related: ["[[CVM_vs_SEC]]", "[[BR_Banks]]", "[[Perpetuum_Engine]]", "[[Token_discipline]]"]
---

# 🏛️ RI Knowledge Base — Phase Y, fonte oficial CVM

> Pipeline que transforma os ZIPs oficiais da CVM (`dados.cvm.gov.br`) em factos estruturados (`quarterly_history`, `bank_quarterly_history`) consumíveis pelo scoring engine, vault timelines e Captain's Log. **Zero scraping, zero LLM, zero tokens** — só `requests` + `csv` + `sqlite3`. Cumpre [[Token_discipline]].

## Princípio

**Filing oficial > release marketing > scraping**. CVM publica os mesmos CSVs anuais que alimentam o B3 — DRE/BPA/BPP/DFC linha-a-linha por empresa, com `cd_conta` + `ds_conta`. Ingestão é idempotente: re-runs custam zero (cache 30d para DFP/ITR, 1d para IPE).

> Distinto de `monitors/cvm_monitor.py` — esse lê só categorias **Fato Relevante / Comunicado** do IPE para a tabela `events`. Este playbook é sobre o **knowledge base estruturado** (DRE/BPA/BPP/DFC).

## Pipeline (5 fases)

```
CVM ZIP ──► extract CSVs ──► filter by CNPJ ──► cvm_dre/bpa/bpp/dfc ──► parser ──► quarterly_history
(dados.cvm)  (latin-1, ;)    (catalog.yaml)    (raw rows)             (cd_conta) (one row/qtr)
                                                                                      │
                                                                  ┌───────────────────┤
                                                                  │                   │
                                                              non-bank             bank
                                                              cvm_parser          cvm_parser_bank
                                                              (cd_conta)          (ds_conta!)
                                                                  │                   │
                                                              quarterly_         bank_quarterly_
                                                              history            history
                                                                  │                   │
                                                              quarterly_         bank_quarterly_
                                                              single             single
                                                              (YTD diff)         (YTD diff)
                                                                  │                   │
                                                                  └─► compare_releases ─► obsidian_vault/tickers/<TK>_RI.md
```

| # | Fase | Módulo | Output |
|---|---|---|---|
| 1 | Download ZIPs anuais | `library/ri/cvm_filings.py::download` | `library/ri/cache/<SOURCE>/<source>_cia_aberta_<year>.zip` |
| 2 | Ingest raw rows | `cvm_filings.py::ingest_dfp_or_itr` | `cvm_dre`, `cvm_bpa`, `cvm_bpp`, `cvm_dfc` |
| 3a | Parser non-bank | `library/ri/cvm_parser.py::build` | `quarterly_history` |
| 3b | Parser bank | `library/ri/cvm_parser_bank.py::build` | `bank_quarterly_history` |
| 4 | YTD → single-Q | `quarterly_single.py` + `bank_quarterly_single.py` | `quarterly_single`, `bank_quarterly_single` |
| 5 | Compare releases | `compare_releases.py` | JSON em `data/ri_compare/` + MD em `obsidian_vault/tickers/<TK>_RI.md` |

## YTD artifact (regra de ouro)

ITRs CVM são **acumulados year-to-date**, não single-quarter. `Q3 ITR = 9 meses YTD`, `DFP = 12 meses`. Para análise QoQ honesta:

- `Q1 single = ITR Q1` (já são 3 meses)
- `Q2 single = ITR Q2 − ITR Q1`
- `Q3 single = ITR Q3 − ITR Q2`
- `Q4 single = DFP − ITR Q3`

Métricas **flow** (revenue, ebit, net_income, fco, NII, fee_income, PDD) **subtraem**. Métricas **stock** (total_assets, equity, debt_total, loan_book, deposits) são snapshot — NÃO subtrair.

Implementado em `library/ri/quarterly_single.py` (non-bank) e `library/ri/bank_quarterly_single.py` (bank). Sempre que comparar QoQ, usar tabelas `*_single`, **nunca** `*_history`.

## Bank parser specificity (`cvm_parser_bank.py`)

### Por que `ds_conta` (descrição) e não `cd_conta` (código)?

Cada banco usa **códigos diferentes** para a mesma conta. Exemplos:

| Conta | Itaú (ITUB4) | Bradesco (BBDC4) |
|---|---|---|
| Patrimônio Líquido | `2.06` | `2.07` |
| Receitas de Intermediação | `3.01` | `3.01` ✅ (raros casos onde batem) |
| PDD/Perda Esperada | sub-código X | sub-código Y |

Se usássemos `cd_conta` como nas empresas operacionais, o parser falharia silenciosamente para qualquer banco que não fosse o "padrão". Solução: lookup por **substring case-insensitive de `ds_conta`** com tiebreaker (Consolidado > Individual; menor `LENGTH(ds_conta)` para preferir conta principal sobre sub-categorias tipo "Arrendamento" ou "Outros Créditos").

`BANK_DRE_ACCOUNTS_BY_DESC` (no módulo) tem listas ordenadas de patterns por métrica — primeira match wins. Empresas operacionais continuam a usar `cd_conta` em `cvm_parser.py` (estável entre tickers).

### Schema `bank_quarterly_history`

DRE bancária + BP relevantes + ratios derivados + colunas BACEN reservadas:

| Coluna | Origem | Notas |
|---|---|---|
| `nii` | DRE 3.03 (Resultado Bruto Intermediação) | Net Interest Income |
| `interest_income` | DRE 3.01 | |
| `interest_expense` | DRE 3.02 | negativo |
| `fee_income` | DRE 3.04.02 (variável) | Receitas de Prestação de Serviços |
| `personnel_expenses`, `admin_expenses`, `tax_expenses` | DRE 3.04.03/04/05 | opex bancário |
| `loan_loss_provisions` | DRE 3.04.01 | PDD expense (negativo) |
| `pretax_income`, `net_income` | DRE 3.05 / 3.07 ou 3.09 | |
| `total_assets`, `equity` | BPA `1` / BPP por descrição "patrimônio líquido" | |
| **`loan_book`** (Phase J) | BPA por descrição "operações de crédito" | gross loans |
| **`pdd_reserve`** (Phase J) | BPA por descrição "(-) provisão para perda esperada" | reserve, negativo |
| **`deposits`** (Phase J) | BPP por descrição "depósitos" | |
| `cost_to_income_ratio` | derived | `\|opex\| / (NII + fees)` |
| `pre_provision_profit` | derived | NII + fees − opex (antes de PDD/taxes) |
| `nim_proxy` | derived | NII / total_assets |
| **`coverage_ratio_bs`** (Phase J) | derived | `\|pdd_reserve\| / loan_book` |
| **`equity_to_assets`** (Phase J) | derived | leverage proxy |
| **`cost_of_risk_ytd`** (Phase J) | derived | `\|loan_loss_provisions\| / loan_book` (YTD basis) |
| **`cet1_ratio`** | reservada | NULL — fetcher BACEN futuro (Pillar III) |
| **`rwa`** | reservada | NULL — Risk-Weighted Assets |
| **`basel_ratio`** | reservada | NULL — Total capital / RWA |
| **`npl_ratio`** | reservada | NULL — Non-performing loans / loan_book |

As 4 colunas BACEN são target para futuro fetcher dedicado (BACEN Pillar III não vem nos CSVs CVM).

### Schema `quarterly_history` (non-bank)

23 colunas: `ticker`, `period_end`, `source` + DRE (revenue, gross_profit, ebit, pretax_income, net_income, equity_method) + BPA/BPP (total_assets, current_assets, current_liab, total_liab, equity, debt_st, debt_lt) + DFC (fco, fci, fcf_proxy) + computed (gross_margin, ebit_margin, net_margin, debt_total). PK `(ticker, period_end)`.

## Coverage state (2026-04-28)

Após backfill ITRs 2019-2023:

| Tabela | Rows | Tickers | Range |
|---|---|---|---|
| `quarterly_history` | **532** | 20 | 2018-Q1 → 2025-Q3 (~7 anos, 26-30 quarters/ticker) |
| `quarterly_single` | 532 | 20 | mirror com YTD-deltas |
| `bank_quarterly_history` | **151** | 5 (ABCB4, BBAS3, BBDC4, BPAC11, ITUB4 — verificado 2026-04-28) | 2018-Q1 → 2025-Q3 |
| `bank_quarterly_single` | **56** | 5 | mirror |
| `cvm_dre` / `cvm_bpa` / `cvm_bpp` / `cvm_dfc` (raw) | 38k / 81k / 132k / 61k | — | filter por catalog CNPJ |
| `cvm_ipe` (eventos) | 1055 | — | fatos relevantes + comunicados |

Baseline anterior era 5 stocks × 11 quarters; backfill adicionou +292 rows e +15 tickers. Bancos têm 56 single-Q rows com as novas BS columns (`loan_book`, `pdd_reserve`, etc.) populadas a partir de Phase J.

## Vault timelines auto-geradas

`library/ri/compare_releases.py` é o output layer. Para cada ticker:

- **JSON detalhado** em `data/ri_compare/<TK>_<period>.json` (qoq, yoy, material_flags).
- **Markdown timeline** em `obsidian_vault/tickers/<TK>_RI.md` com:
  - Frontmatter `type: ri_quarterly_comparison`
  - 🚨 Material changes section (auto-flag se ≥10% revenue, ≥20% ebit/net_income, ≥5pp margin, ≥25% debt, ≥30% FCO)
  - Tabelas QoQ + YoY
  - Trajetória 11Q (último ano + 2.5 anos)
  - Chart Dataview (`type: line`, Revenue + EBIT margin)

Material thresholds em `MATERIAL_CHG` dict no topo de `compare_releases.py`.

## Material findings registados (memo)

- **BBDC4** (Bradesco): NII **+16% YoY**, Net income **+31% YoY** → forte recovery. PDD +16-18% reflete sector credit cost rising.
- **ITUB4** (Itaú): NII **flat YoY** → estagnação. PDD ainda em alta.
- **VALE3**: deteriorating quality — YoY EBIT **−25%** (flagged via `compare_releases`).

São exemplos do tipo de finding que o pipeline torna trivial. Cross-check com [[Synthetic_IC]] / [[Variant_Perception]] antes de fazer trade.

## CVM code gotcha — subsidiary trap

**AXIA7 → código CVM correto é `2437`, NÃO `3328`** (que era subsidiária Nordeste, registrada separadamente). Confirmado pelo user 2026-04-26.

Pattern: holdings com múltiplos CNPJs (parent + sub) podem ter o sub registado como `cia_aberta` com nome parecido. Sempre validar `cad_cia_aberta.csv` (CVM CAD) com `python -m library.ri.cvm_codes lookup <TK>` antes de fixar `codigo_cvm` em `library/ri/catalog.yaml`. Se 0 rows aparecem em `quarterly_history` para um ticker, suspeitar subsidiary trap antes de assumir filing missing.

## ri_freshness perpetuum (9º perpetuum)

`agents/perpetuum/ri_freshness.py` é o **monitor** do pipeline (T2 desde Y.8.5). Subjects: cada stock do `library/ri/catalog.yaml` (holdings + watchlist; FIIs têm pipeline próprio em `fii_filings.py`).

Sinais (score 0-100, action_score_threshold=80):
1. `quarterly_history` latest period ≥ deadline esperado (Q1 +45d, Q2 +45d, Q3 +45d, DFP +120d) → −25 ou −50.
2. IPE events nos últimos 30 dias > 0 (proxy actividade RI) → +/−15.
3. Fato Relevante nos últimos 7 dias (sinal urgente, não score).
4. DFP latest year < ano corrente − 1 → −10.

Action_hint emite comando whitelisted: `python -m library.ri.cvm_filings ingest itr --year YYYY --all-catalog && python -m library.ri.cvm_parser build`. Ver [[Perpetuum_Engine]] para autonomy tiers e workflow approve/ignore.

## Comandos

| Caso | Comando |
|---|---|
| Listar fontes disponíveis | `python -m library.ri.cvm_filings sources` |
| Download ZIP DFP/ITR/IPE | `python -m library.ri.cvm_filings download {dfp\|itr\|ipe} --year 2025` |
| Ingest 1 ticker, 1 ano | `python -m library.ri.cvm_filings ingest itr --year 2025 --ticker VALE3` |
| Ingest catalog inteiro | `python -m library.ri.cvm_filings ingest dfp --year 2024 --all-catalog` |
| Build `quarterly_history` (non-bank) | `python -m library.ri.cvm_parser build` |
| Inspect ticker | `python -m library.ri.cvm_parser show VALE3` |
| Build `bank_quarterly_history` | `python -m library.ri.cvm_parser_bank build` |
| Inspect bank | `python -m library.ri.cvm_parser_bank show BBDC4` |
| Build single-Q (YTD diff) | `python -m library.ri.quarterly_single build` |
| Build bank single-Q | `python -m library.ri.bank_quarterly_single <TK>` |
| Compare releases (1 ticker) | `python -m library.ri.compare_releases <TK>` — itera todos os quarters disponíveis automaticamente (não há flag `--quarters`; verificado 2026-04-28) |
| Compare all catalog | `python -m library.ri.compare_releases --all-catalog` |
| Lookup CVM code | `python -m library.ri.cvm_codes lookup <TK>` |
| Validate catalog | `python -m library.ri.cvm_codes validate-catalog` |
| Refresh CAD cache | `python -m library.ri.cvm_codes refresh` |

Cron diário (23:30) corre o monitor `cvm_monitor.py` (IPE-only, eventos). Ingestão DFP/ITR é manual ou disparada por `ri_freshness` action_hint — ZIPs são grandes (40-200MB/ano) e raramente mudam.

## Limitações conhecidas

- **Bank schema só suporta tickers em `bank=true` no catalog**. Adicionar novo banco requer:
  1. Add entry em `library/ri/catalog.yaml` com `bank: true` (e `sector: Banks`).
  2. Verificar que padrões em `BANK_DRE_ACCOUNTS_BY_DESC` apanham o `ds_conta` desse banco — empresas tipo Banco do Brasil (BBAS3) ou BTG (BPAC11) podem ter wording subtilmente diferente. Adicionar pattern à lista (case-insensitive substring).
  3. Re-run `python -m library.ri.cvm_parser_bank build`.
  4. Inspect `python -m library.ri.cvm_parser_bank show <TK>` — se NII/PDD vêm 0 ou NULL, descobrir o `ds_conta` real via SQL: `SELECT DISTINCT ds_conta FROM cvm_dre WHERE ticker='X' ORDER BY ds_conta`.
- **BACEN columns NULL** (cet1_ratio, rwa, basel_ratio, npl_ratio) — fetcher BACEN dedicado pendente. Para já, esses ratios entram pelo `daily_update.py` via `yf_deep_fundamentals` quando disponíveis. Scoring engine (`score_br_bank`) tem fallback graceful.
- **Equivalência patrimonial** (`equity_method`, conta `3.04.06`) só é populada para holdings (ITSA4, IVVB11 não-aplicável). Útil para ITSA4 onde domina o lucro.
- **FIIs não entram aqui** — `library/ri/fii_filings.py` é pipeline paralelo (FII Mensal/Trimestral schemas próprios).
- **Latin-1 encoding** dos CSVs CVM é hardcoded em `_read_csv_in_zip` — se a CVM mudar para UTF-8 no futuro, mudar aqui.
- **Subsidiary trap** (ver AXIA7 acima) é detectável só por inspecção; nenhum guard automático no parser.

## Integrações

- **Scoring engine** (`scoring/engine.py::score_br_bank`, `score_br_company`) lê `quarterly_history` / `bank_quarterly_history` para os 5 critérios Graham/banks.
- **Captain's Log** (Phase CC) puxa material_flags de `compare_releases` JSON outputs.
- **Conviction score** (`analytics/conviction_score.py`) usa quarterly trends como input.
- **Synthetic IC** + **Variant Perception** (Phase AA) cross-reference `quarterly_single` vs analyst consensus / vídeos.
- **Trigger engine** consome `bank_quarterly_history.cost_of_risk_ytd` para flag de credit deterioration.

## Workflow recomendado

1. **Fim de período fiscal** (45d após quarter end) → `ri_freshness` perpetuum vai score < 80 e propor action. Approve via `python scripts/perpetuum_action_run.py <id>`.
2. **Após ingest** → sempre re-run `cvm_parser build` + `cvm_parser_bank build` (ambos idempotentes). Single-Q derivation precisa de duas linhas para Q2+ (Q2 needs Q1).
3. **Para análise** → consumir `quarterly_single` / `bank_quarterly_single` (YTD-corrected), nunca `*_history` directamente para QoQ.
4. **Material change detected** → `compare_releases <TK>` regenera vault MD; cross-check com [[Synthetic_IC]] antes de mudar tese.

## Ver também
- [[CVM_vs_SEC]] — porque CVM tem este formato e SEC não
- [[BR_Banks]] — playbook narrativo do scoring bancário BR
- [[Perpetuum_Engine]] — `ri_freshness` é um dos 12 perpetuums
- [[Token_discipline]] — porque pipeline é 100% local
- `library/ri/catalog.yaml` — fonte canónica de tickers + CNPJ + codigo_cvm
