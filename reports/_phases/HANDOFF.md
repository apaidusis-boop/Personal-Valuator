# HANDOFF — investment-intelligence

Documento de passagem de contexto. Lê isto primeiro antes de continuar o
trabalho noutra ferramenta ou sessão. Filosofia, critérios e schema base
estão em **`CLAUDE.md`** — ler lá também.

Última actualização: **2026-04-17** (após a sessão de portfolio + DRIP + briefing).

---

## 1. Estado actual

Sistema passou de "scaffolding + piloto" a "plataforma viva com carteira
real carregada e análise one-shot". Tudo corre localmente; apenas fetchers
tocam na rede.

### Data layer
- **`data/br_investments.db`** e **`data/us_investments.db`** com schemas
  idênticos. Sincronizadas via `scripts/init_db.py`.
- Tabelas: `companies`, `prices`, `fundamentals`, `fii_fundamentals`,
  `scores`, `dividends`, `events`, `series` (+ metas), `portfolio_positions`
  (com `quantity` + `notes`), `fixed_income_positions` (novo — Tesouro +
  Deb + CRA + LCA).
- **Carteira real carregada** (2026-04-17): R$ 514.933 trackados
  (R$ 358.827 equity BR + R$ 156.106 renda fixa BR + USD 20.536 US
  equity). Resto (~R$ 12k: saldo + proventos) fica fora.

### Universe
- `config/universe.yaml` é a única fonte de truth para tickers.
- BR: 6 stocks holdings (VALE3, BBDC4, ITSA4, PRIO3, LFTB11, IVVB11)
  + 5 FIIs (XPML11, VGIR11, BTLG11, RBRX11, PVBI11) + watchlist Tier 1/2
  + FIIs Suno + research pool.
- US: 22 holdings (JPM Wealth export) + watchlist Dividend Aristocrats.

### Fetchers (rede, idempotentes)
- `brapi_fetcher.py` — BR fundamentals (EPS, BVPS, ROE, P/E, P/B, DY,
  histórico dividendos). Requer `BRAPI_TOKEN` em `.env`.
- `statusinvest_scraper.py` — fallback BR scraper.
- `yf_br_fetcher.py` — BR preços + dividendos via yfinance.
- `yf_us_fetcher.py` — US preços + fundamentals + dividendos + FFO/REIT.
- `fiis_fetcher.py`, `fii_statusinvest_scraper.py` — FIIs BR.
- `bcb_fetcher.py` — Selic, CDI, IPCA, USD/BRL PTAX via BCB SGS API.
- **`sec_edgar_fetcher.py`** (novo, Fase 2) — cross-validate streak de
  dividendos via Company Facts XBRL (us-gaap + ifrs-full). Auto-flag
  `is_aristocrat=1` para streak ≥ 25. Column `dividend_streak_source`
  regista origem.

### Monitors
- `cvm_monitor.py` + `cvm_pdf_extractor.py` — fatos relevantes BR.
- `sec_monitor.py` — 8-K / 10-K / 20-F / proxy / 6-K nas holdings US.

### Scoring
- `scoring/engine.py` — 5 motores:
  - `score_br` (Graham BR: Graham Number, DY≥6%, ROE≥15%, NetDebt/EBITDA<3, streak≥5)
  - `score_br_bank` (P/E≤10, P/B≤1.5, DY≥6%, ROE≥12%, streak≥5)
  - `score_br_fii` (DY 12m≥8%, P/VP≤1.05, vacância<15%, streak≥12m, ADTV>R$500k, spread sobre Selic real)
  - `score_us` (P/E≤20, P/B≤3, DY≥2.5%, ROE≥15%, aristocrat OR streak≥10)
  - `score_us_reit` (DY, streak, P/B, ND/EBITDA, P/FFO, interest coverage)
- Cada critério devolve `pass`/`fail`/`n/a`. Score = pass / applicable.

### Pipeline diário (`scripts/daily_run.bat`)
11 stages, corre end-to-end em ~5m26s:
1. BR daily_update (fetch + scoring)
2. CVM monitor (IPE)
3. CVM-PDF extractor (best-effort)
4. US daily_update (yf → **sec_edgar cross-validate** → scoring)
5. SEC monitor
6. US portfolio report
7. Weekly report
8. **Portfolio briefing** (novo)
9. Notify events (toasts CVM/SEC + screen transitions)
10. Macro CSV export
11. Log rotate

### Scripts de análise (one-shot, sem rede)
- **`scripts/analyze_ticker.py`** — deep-dive single-ticker (~0.2s):
  posição + price action + fundamentals + screen verdict + dividend
  history + eventos 90d + peers + DRIP forward + entry triggers.
- **`scripts/drip_projection.py`** — forward DRIP 5/10/15y com 3 cenários
  (conservador/base/optimista). Type-aware (fii / selic_etf / sp_etf /
  compounder / equity). Damper em hist explosivo vs Gordon.
- **`scripts/portfolio_report.py`** — briefing consolidado BR+US+RF
  (~0.3s): snapshot, eventos, holdings com screen, dividend calendar,
  DRIP forward, watchlist near-miss, macro, action items.
- **`scripts/import_portfolio.py`** — parser XP xlsx + JPM csv para
  popular `portfolio_positions` + `fixed_income_positions`.
- **`scripts/executive_report.py`** — HTML executivo BR Plotly.
- **`scripts/compare_ibov.py`**, **`compare_ticker_vs_macro.py`**,
  **`analyze_portfolio_csv.py`** — comparativos e legacy CSV.

## 2. Como (re)importar a carteira

Se o user exporta uma posição XP/JPM actualizada:
```bash
python scripts/import_portfolio.py \
  --br "C:\Users\paidu\Downloads\PosicaoDetalhada.xlsx" \
  --us "C:\Users\paidu\Downloads\positions.csv"
```
Idempotente: substitui os registos XP/JPM daquele dia. `--dry-run` para
conferir antes de gravar. Scripts `portfolio_report`, `drip_projection`,
`analyze_ticker` consomem automaticamente.

## 3. Assumptions em DRIP projection (importante!)

Ver `scripts/drip_projection.py::derive_scenarios`.

- **FII**: base = mediana(hist, IPCA 3.5%), floor 0%, cap 6%. Não decresce
  estruturalmente no Base.
- **SELIC ETF (LFTB11)**: md = SELIC meta × {0.65/0.80/1.00} por cenário.
- **S&P ETF (IVVB11)**: md = {6%/10%/14%} por cenário (US + FX).
- **Compounder / não-pagador**: md = price CAGR 5y histórico, cap 25%.
- **Equity com dividendo**: base = mediana(hist_g, Gordon=ROE×(1-payout)).
  **Damper**: quando hist > 2×Gordon e Gordon>0, clampa hist ao max(2×Gordon, 12%).
  Evita one-offs (ITSA4 reset 2020→2025) dominarem a projecção.
- Clamps finais: g ∈ [-3%, 18%] para equity.

O user prefere assumptions honesto-conservadoras. Se uma projecção 15y
depende de um múltiplo > 10×, verificar se o cenário Base está
efectivamente no "optimista-moderado".

## 4. Próximos passos documentados

Por ordem de ROI decrescente:

1. **`analytics/technical.py`** — DMA 50/200, distância de 52w-high/low,
   ATR. Para contexto de aporte, não trading signals.
2. **`scripts/compare_tickers.py`** — side-by-side entre tickers
   (ITUB4 vs BBDC4 vs BPAC11, por exemplo).
3. **Portfolio-level scoring** — diversificação, Sharpe histórico vs IBOV,
   concentração sectorial, overlap de holdings.
4. **Toast com briefing diário** — wrapper em notify_events.py que
   anexa o action items do briefing.
5. **`analytics/sector_rotation_us.py`** — 11 ETFs XL vs SPY.
6. **Fixed income forward** — projectar o value_atual de NTN-B / CRA /
   Deb ao longo do tempo (IPCA forward + duration).

## 5. Memória externa (`~/.claude/.../memory/`)

O Claude Code mantém memórias persistentes entre sessões:
- `portfolio_loaded.md` — a carteira do user vive em portfolio_positions.
- `feedback_honest_projections.md` — damping hist quando non-repeatable.
- `us_data_sources_catalog.md` — APIs US (parcialmente activado).
- `MEMORY.md` — índice.

## 6. Convenções críticas (de CLAUDE.md, repetidas aqui)

- Datas ISO 8601 (`YYYY-MM-DD`), UTC para timestamps.
- Moeda **nunca** convertida na DB — BRL em br, USD em us. FX só no
  relatório consolidado.
- Tickers BR **sem** sufixo `.SA` na DB.
- Fetchers independentes e idempotentes. Scoring engine **nunca** chama rede.
- Logs estruturados (1 linha JSON por evento) em `logs/`.
- `data/*.db`, `data/cvm_pdfs/`, `logs/`, `reports/` ficam commitados
  (decisão deliberada — permite reconstruir histórico). `.env`,
  `.venv/`, `data/sec_cache/` ficam em `.gitignore`.

## 7. Comandos cheat-sheet

```bash
# pipeline completo
scripts/daily_run.bat

# análises one-shot
python scripts/analyze_ticker.py <TICKER>
python scripts/analyze_ticker.py JNJ --md
python scripts/portfolio_report.py
python scripts/drip_projection.py --horizons 5,10,15,20

# import nova carteira
python scripts/import_portfolio.py --br "<path>.xlsx" --us "<path>.csv"

# reconstruir DBs (idempotente — não destrói dados)
python scripts/init_db.py

# scoring ad-hoc
python scoring/engine.py ITSA4             # BR default
python scoring/engine.py JNJ --market us

# inspecção DB
sqlite3 data/br_investments.db "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE active=1;"
```
