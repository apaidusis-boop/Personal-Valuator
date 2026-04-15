# Mapa Ficheiro-a-Ficheiro: O Que Portar

Cada linha desta tabela mapeia **um módulo do repo vendored** para **onde
encaixa (ou não) no nosso stack**. Usar como checklist quando se arrancar o
US pipeline.

Origem: `vendor/skill-financial-analyst/scripts/`. Todos os ficheiros estão
sob MIT License — qualquer ficheiro derivado deve incluir atribuição no
header.

## Tabela de portabilidade

| Ficheiro (origem) | Linhas | Destino no nosso stack | Prioridade | Esforço | Nota |
|---|---|---|---|---|---|
| `api_config.py` | ~200 | `fetchers/api_config_us.py` | **ALTA** | 30min | Catálogo de endpoints + rate limits. Adapta directo. |
| `api_caller.py` | 117 | `fetchers/_resilient.py` | **ALTA** | 45min | Resilient fetch helper. Usa imediatamente em fetchers BR existentes também. |
| `data_cache.py` | 783 | Confirmar se `fetchers/cache_policy.py` basta; senão estender | MÉDIA | 1h review | O nosso é mais simples. Portar só se precisares de TTLs diferenciados. |
| `data_fetchers.py` | ? | `fetchers/yfinance_us_fetcher.py` + `fetchers/sec_edgar_fetcher.py` (novos) | **ALTA** | 2h | Separar em dois fetchers independentes. Lógica yfinance é quase copy-paste do nosso `yf_br_fetcher.py`. |
| `scoring.py` | 846 | Parcial — só o `calculate_confidence()` e padrão composite | MÉDIA | 1h | O nosso scoring é melhor (pass/fail/n/a). Só portar o pattern de confidence. |
| `technical_analysis.py` | 459 | `analytics/technical.py` (novo) | MÉDIA | 1.5h | Portar SMA, EMA, RSI, MACD, ATR, Bollinger em pandas puro (dropar dependência `pandas-ta`). |
| `entry_exit.py` | 448 | `analytics/entry_exit.py` (novo) | MÉDIA | 1.5h | Adaptar para DRIP: entries baseados em Graham Number, não em ATR. |
| `sector_rotation.py` | 415 | `analytics/sector_rotation_us.py` (novo) | BAIXA | 1h | Para US é directo (11 XL ETFs). Para BR requer trabalho extra, não portar agora. |
| `rss_feeds.py` | 170 | `fetchers/rss_fetcher.py` (novo, US only) | BAIXA | 45min | 20 feeds US. Para BR precisaria catálogo próprio (Valor, InfoMoney, Seu Dinheiro, ...). |
| `macro_calendar.py` | 408 | `analytics/calendar.py` (novo) | BAIXA | 1h | Útil mas não crítico para MVP. |
| `usage_tracker.py` | ~200 | Skip a menos que uses APIs com quotas apertadas | BAIXA | — | Só relevante se meteres Alpha Vantage (25 req/dia). |
| `run_daily_scanner.py` | ? | **Não portar** | — | — | Swing-trading, não alinha com DRIP. |
| `run_deep_dive.py` | ? | Inspirar `scripts/analyze_ticker_us.py` (novo) | MÉDIA | 1h | A estrutura do output (secções, ordenação) é boa referência. Não copiar — inspirar. |
| `run_portfolio_review.py` | ? | **Não portar** | — | — | Output markdown print, incompatível com HTML Plotly. |

## Ordem de ataque sugerida (quando arrancar US)

**Fase 1 — MVP (2–3h):**
1. `fetchers/_resilient.py` (portar `api_caller.py`)
2. `fetchers/yfinance_us_fetcher.py` (análogo do `yf_br_fetcher.py`)
3. `scripts/daily_update.py` — adicionar step US
4. Popular watchlist US seed (10 Dividend Aristocrats: KO, JNJ, PG, MMM, CAT, PEP, MCD, WMT, MSFT, XOM)
5. Correr `scoring/engine.py <TICKER> --market us` contra cada um

**Fase 2 — SEC EDGAR como ground truth (2h):**
6. `fetchers/sec_edgar_fetcher.py` — Company Facts JSON para extrair histórico
   de dividendos canónico (> confiável que yfinance para streaks longos)
7. Cruzar com `is_aristocrat` flag no `universe.yaml`

**Fase 3 — Analytics US (3–4h):**
8. `analytics/technical.py` — SMA/EMA/RSI/MACD/ATR em pandas puro
9. `analytics/entry_exit.py` adaptado a DRIP
10. `scripts/analyze_ticker.py` — gera relatório HTML Plotly single-ticker
    (funciona para BR ou US, argumento `--market`)

**Fase 4 — Context (opcional):**
11. `analytics/sector_rotation_us.py` — 11 ETFs vs SPY
12. `analytics/calendar.py` — FOMC + earnings

Total estimado: **~10h** para um pipeline US ao nível do que temos hoje no BR.

## Atribuição MIT

Qualquer ficheiro derivado de `vendor/skill-financial-analyst/` deve ter
no topo:

```python
"""<descrição do ficheiro>.

Derivado de scripts/<ficheiro>.py do projecto geogons/skill-financial-analyst
(github.com/geogons/skill-financial-analyst), MIT License, copyright (c)
2026 Contributors.

Adaptado para DRIP/Buffett/Graham filosofia e integração SQLite.
"""
```

Isto cumpre a cláusula de preservação de copyright da MIT sem burocracia.

## Ficheiros que **nem vale** abrir

- `setup.sh` — é específico da estrutura de Claude Skill deles
- `tests/` — testes unitários dos módulos deles, não nossos
- `QUICKSTART.md`, `README.md` — úteis como leitura, não como código
- `references/` — documentação interna deles, overlap com o que já temos
