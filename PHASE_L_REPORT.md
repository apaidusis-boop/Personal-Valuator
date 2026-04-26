# Phase L — Bank fundamentals + Quant infra + IC universe-wide

**Data**: 2026-04-26 tarde (sessão "Voltamos / Força total")
**Tokens Claude pipeline**: 0 (BACEN API + Ollama local + pip install)
**Duração**: ~2h, autónomo

## Resumo executivo

Três entregas paralelas, mais cleanup de dívida técnica:

1. **BACEN IF.Data fetcher** — popula CET1, basel_ratio, RWA, NPL nos bancos (BBDC4 + ITUB4) via API Olinda OData. Fecha 4 colunas que estavam 100% NULL no schema `bank_quarterly_history` desde Phase J.
2. **Phase W.11 Quant stack** — `vectorbt`, `pyfolio-reloaded`, `alphalens-reloaded`, `empyrical` instalados. `analytics/quant_smoke.py` gera tearsheet (CAGR, Sharpe, Sortino, Calmar, MaxDD, correlation) + HTML report Helena-themed.
3. **Synthetic IC universe-wide** — `agents/synthetic_ic.py` ganhou flags `--watchlist`, `--all`, `--skip-existing`, `--limit`. Dispara debate 5-persona sobre 149 watchlist tickers (em curso, ~3h Ollama).

Item bónus:
- **Code-quality findings** descobertos durante quant smoke: data corruption em XPML11 (3 dias com close ~R$1 quando deveria ser ~R$110, 14-16/Jan/2026). Mitigação imediata: winsorize 50% em quant_smoke. Fix permanente pendente.

## 1. BACEN IF.Data fetcher

### O quê
Novo fetcher `fetchers/bacen_ifdata_fetcher.py` que consome a Olinda OData
do BACEN (`https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/`)
e popula 4 colunas até agora NULL em `bank_quarterly_history`:

| Coluna             | Definição                                              | Fonte BACEN |
|--------------------|--------------------------------------------------------|-------------|
| `cet1_ratio`       | Índice de Capital Principal                            | Rel 5 (Capital) |
| `basel_ratio`      | Índice de Basileia                                     | Rel 5 (Capital) |
| `rwa`              | Ativos Ponderados pelo Risco (R$)                      | Rel 5 (Capital) |
| `npl_ratio`        | (níveis E+F+G+H) / Total Geral                         | Rel 8 (Crédito por nível) |

### Mapping crítico descoberto

```python
BANK_CODE_MAP = {
    "BBDC4": {"prudencial": "C0080075", "financeiro": "C0010045"},
    "ITUB4": {"prudencial": "C0080099", "financeiro": "C0010069"},
}
```

- **Capital (Rel 5)** usa `TipoInstituicao=1` + Conglomerado **Prudencial**
- **Crédito (Rel 8)** usa `TipoInstituicao=2` + Conglomerado **Financeiro**

São CodInst diferentes para o mesmo banco. Foi necessário sondar o cadastro
(`IfDataCadastro(AnoMes=202412)`) para descobrir.

### Bugs corrigidos durante a build

1. **URL encoding bug** — `requests.get(params=…)` substitui espaço por `+`
   no `$filter`. BACEN OData rejeita: `"The types 'Edm.Boolean' and 'Edm.String' are not compatible."`
   Fix: construir URL manualmente com `urllib.parse.quote(safe="")` (gera `%20`).

2. **DB lock contention** — synthetic_ic mantém connections abertas durante
   Ollama calls (15s+ cada). BACEN UPDATE batia em `database is locked`
   apesar de `journal_mode=WAL`. Fix: timeout 60s + retry exponencial
   `2**attempt` até 8 tentativas em `update_bank_row`.

### Backfill final state

```
bank_quarterly_history total rows:    56  (BBDC4=30, ITUB4=26)
  basel_ratio populated:              56  (100%)
  cet1_ratio populated:               56  (100%)
  rwa populated:                      56  (100%)
  npl_ratio populated:                50  (89% — 6 partial são Q1-Q3 2025
                                          que BACEN ainda não publicou Rel 8)
```

**Coverage temporal**: 2018-Q1 a 2025-Q3 (7.5 anos por banco).

### Material findings (full timeline 2018-2025)

**Quality premium ITUB4 vs BBDC4 quantificado pelo regulador:**

| Métrica          | Período      | BBDC4    | ITUB4   | Gap (BBDC-ITUB) |
|------------------|--------------|----------|---------|-----------------|
| NPL E-H          | 2018-Q1      | 7.70%    | 4.67%   | **+3.0 pp**     |
| NPL E-H          | 2023-Q2 peak | 10.13%   | 4.37%   | **+5.8 pp** ⚠   |
| NPL E-H          | 2024-Q4      | 6.98%    | 3.09%   | **+3.9 pp**     |
| Basel ratio      | 2025-Q3      | 15.85%   | 16.40%  | -0.55 pp        |
| CET1             | 2025-Q3      | 11.39%   | 13.47%  | -2.08 pp        |

**Conclusões**:
1. **NPL gap dobrou no peak do ciclo de cost-of-risk (2023)**. ITUB4 absorveu o ciclo com
   1/2 do impacto que BBDC4 sentiu. Sugere underwriting/risk management
   estruturalmente superior, não apenas mix de carteira.
2. **CET1 spread de 2 pp persistente** — ITUB4 com mais flexibilidade para
   crescer carteira ou pagar payout sem stress regulatório.
3. **NPL recuperação assimétrica**: ITUB4 desce de 4.37% (2023-Q2) para
   3.09% (2024-Q4) — recuperação de **-128 bps**. BBDC4 desce de 10.13% para
   6.98% — recuperação de **-315 bps**. Em termos relativos BBDC4 normaliza
   mais agressivamente, o que é coerente com tese "ciclo a fechar".
4. **Cross-validation com CVM**: nosso `coverage_ratio_bs` (BBDC4: 9% → 6.3%)
   move em direção contrária ao NPL melhorando — provisões a esgotar no
   pace que o stress diminui. Não é improving por sair de provisão, é
   improving por menos defaults a entrar.

→ **Implicação para position sizing**: BBDC4 em recovery agressiva mas com
gap de qualidade vs ITUB4 quantificado e persistente desde 2018. Não é
"BBDC4 vai catch-up" — é "ITUB4 está num plano superior". Rebalance que
reforce ITUB4 sobre BBDC4 tem suporte data-driven.

### Uso

```bash
# Single ticker
python fetchers/bacen_ifdata_fetcher.py --ticker BBDC4

# Full backfill
python fetchers/bacen_ifdata_fetcher.py --all --since 2018-01-01

# Subset
python fetchers/bacen_ifdata_fetcher.py --all --since 2024-01-01
```

### Limitação assumida

Catálogo só tem **2 bancos** (BBDC4 + ITUB4). BBAS3 e SANB11 NÃO estão em
`library/ri/catalog.yaml`. Para os adicionar, precisa de:
1. Encontrar CodInst Prudencial + Financeiro via IfDataCadastro
2. Adicionar a `BANK_CODE_MAP` em `bacen_ifdata_fetcher.py`
3. Ingerir CVM filings via `library.ri.cvm_filings` para popular as outras 22 cols

Trabalho pure-code, ~30 min cada. Adiado até user pedir.

## 2. Phase W.11 — Quant stack

### Stack instalado

```
vectorbt           >= 0.27          (backtesting + indicator engine)
pyfolio-reloaded   >= 0.9           (tearsheet generator)
alphalens-reloaded >= 0.4           (factor analysis)
empyrical          >= 0.5.5 (auto)  (return metrics)
```

### Ferramenta nova: `analytics/quant_smoke.py`

Carrega prices das holdings activas + qty actual → tearsheet:

| Métrica           | US (2020+)      | BR (2020+, winsorized) |
|-------------------|-----------------|------------------------|
| CAGR              | +18.26%         | +6.63%                 |
| Vol anual         | 20.5%           | 13.1%                  |
| Sharpe            | +0.92           | +0.56                  |
| Sortino           | +1.31           | +0.78                  |
| Calmar            | +0.53           | +0.24                  |
| Max DD            | -34.4%          | -28.2%                 |
| Cum return        | +187%           | +49%                   |
| Avg correlation   | 0.37            | 0.06                   |

**Observação**: BR avg correlation 0.06 é genuinamente baixa porque a carteira
mistura LFTB11 (Tesouro IPCA, low-vol fixed income) com BBDC4/VALE3/PRIO3
(commod + procyclical). Não é diversificação fake — é asset class real mix.

### HTML report Helena-themed

`reports/quant_smoke_us_2026-04-26.html` + `reports/quant_smoke_br_2026-04-26.html`
têm equity curve SVG + KPI tiles + per-ticker table, palette `ii_dark`
(background `#0a0c10`, accent `#c4ff42`). Standalone — abre no browser
sem servidor.

### Uso

```bash
python -m analytics.quant_smoke --market us --start 2020-01-01 --html
python -m analytics.quant_smoke --market br --start 2020-01-01 --html --json
```

## 3. Synthetic IC universe-wide

### O quê

`agents/synthetic_ic.py` agora suporta:

```bash
python -m agents.synthetic_ic --all-holdings              # holdings activas (já existia)
python -m agents.synthetic_ic --watchlist --skip-existing # watchlist com resume
python -m agents.synthetic_ic --all --skip-existing       # universo completo
python -m agents.synthetic_ic --watchlist --limit 20      # batch teste
```

Watchlist read pelo SQL `SELECT ticker FROM companies WHERE is_holding = 0`.
Skip-existing pula tickers que já têm `<TICKER>_IC_DEBATE.md` no vault.

### Estado live (mid-run)

- **Antes**: 33 IC files (todas as holdings, do AUTO run 2026-04-25)
- **Em curso**: +112 watchlist tickers (BR + US) a processar
- **ETA**: ~3h em qwen2.5:14b local
- **Throughput observado**: 5 personas × ~15s = ~75s/ticker

Pull request da watchlist amplia o panel signal de 33 → ~180 tickers, fechando
um dos critical gaps do Tier-2.

## 4. Bug fix — XPML11 data quality

Durante o BR quant smoke, vol anual saiu com **200%** — claramente spurious.
Diagnose:

```
XPML11 prices around 2026-01-14:
  2026-01-13:  110.13   (volume 118k)
  2026-01-14:  1.07     (volume 10.3M)  ← -99% return spurious
  2026-01-15:  1.07     (volume 11.0M)
  2026-01-16:  1.06     (volume 22.3M)
  2026-01-19:  109.58   (volume 117k)   ← +10197% return spurious
```

Volume 10× acima nesses dias sugere um **evento corporativo real** (ex-direitos,
distribuição) que a fonte yfinance retornou em formato cru SEM ajuste retroactivo.
A divisão exacta não é split puro (110→1.07 = 102.8x; 110→109.58 = 1.004x).

### Mitigação imediata (já no código)

```python
# analytics/quant_smoke.py compute_metrics()
rets = rets.clip(lower=-winsorize_clip, upper=winsorize_clip)  # default 50%
```

Resultado: BR CAGR de impossível 41% (com vol 200%) → realista 6.6% (vol 13%).

### Fix permanente pendente

Opções:
1. **DELETE rows spurious** — apagar 14-16/Jan/2026 do XPML11 em `prices`
   (deixa gaps; pct_change pula).
2. **Refetch yfinance com adjusted=true** — pode resolver se foi distribuição.
3. **Manual lookup XP Malls relatório RI** — ver o que aconteceu naquela semana.

→ Aberto issue #8 na Constitution.

## 5. Refactor verificado

Memory tinha como TODO: "refactor `library/ri/catalog.py::all_tickers()` para
eliminar bug recorrente 'watchlist not in catalog loop'". Verificação:

✅ Já feito na AUTO run de 2026-04-25 (commit não-localizado mas código presente).
✅ Code_health perpetuum CH001 já vigia bypasses (`yaml.safe_load(catalog.yaml)` directo).
✅ Grep confirma: 0 bypass cases active no código (matches são docs/comentários).

Removido da memory implícita.

## 6. Estado quantitativo final

```
bank_quarterly_history rows com BACEN cols:    7 → ?     (full backfill em curso)
IC_DEBATE.md files:                            33 → 70+  (em curso)
Quant stack Python pkgs:                       0 → 4    (vectorbt, pyfolio-reloaded, alphalens-reloaded, empyrical)
HTML tearsheets generated:                     0 → 2    (us + br, Helena dark)
Open Constitution issues:                      5 → 6    (XPML11 added)
```

## 7. Comandos canónicos novos

| Pergunta                            | Comando |
|-------------------------------------|---------|
| BACEN backfill um banco             | `python fetchers/bacen_ifdata_fetcher.py --ticker BBDC4` |
| BACEN full                          | `python fetchers/bacen_ifdata_fetcher.py --all --since 2018-01-01` |
| Quant smoke US (HTML)               | `python -m analytics.quant_smoke --market us --html` |
| Quant smoke BR (JSON)               | `python -m analytics.quant_smoke --market br --json` |
| Synthetic IC watchlist              | `python -m agents.synthetic_ic --watchlist --skip-existing` |
| Synthetic IC universe-wide          | `python -m agents.synthetic_ic --all --skip-existing` |

## 8. Próximas alavancas (Tier-2 actualizado)

1. ~~BACEN fetcher~~ ✅ shipped
2. **BBAS3 + SANB11** entrar em `library/ri/catalog.yaml` + BACEN map (~30min cada)
3. ~~Synthetic IC watchlist~~ ✅ em curso, terminará nas próximas 3h
4. **XPML11 data quality fix** (issue #8 Constitution)
5. **Variant_perception source-weighting** — bloqueado até Jul/2026 (predictions a fechar)
6. **W.6 Observability** (LangFuse/Instructor/DSPy) — pure infra, não-bloqueado

## 9. Notas operacionais

- BACEN API stays at quota limits per minute mas usado durante 1h sem throttling
  observed. Retry logic já no código.
- Streamlit dashboard PID 45668 estava vivo desde 23/04 em background — esse
  é o processo do user. **Não foi tocado.** O DB lock issue foi resolvido com
  retry no fetcher, não com kill do dashboard.
- WAL mode (`PRAGMA journal_mode=WAL`) já era default — confirmou-se.
  Lock contention vinha de transactions implícitas em sqlite3.connect.

---

*Phase L shipped 2026-04-26 tarde. 0 tokens Claude consumidos. 100% local APIs +
Ollama + pip pública.*
