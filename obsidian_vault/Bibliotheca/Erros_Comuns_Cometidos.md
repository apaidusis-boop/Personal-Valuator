---
type: living-document
tags: [meta, retrospective, lessons, mistakes, process]
created: 2026-05-13
audience: o chefe + o sistema (memória durável de padrões a evitar)
related: ["[[Manual_de_Direcao]]", "[[CONSTITUTION]]"]
status: aberto · adiciona entradas à medida que surgirem
---

# Erros Comuns Cometidos

> Log vivo dos padrões em que tropeço repetidamente. Cada entrada tem **regra** (o que fazer em vez), **porquê** (a razão por que estraga), **como aplicar** (gatilhos e cascade preferida), e **incidente fundador** (quando o chefe corrigiu).
> Quando uma entrada se tornar reflexo automático (sem reincidência), marca-se como *internalizada* (não se apaga — fica como prova).

---

## #1 — yfinance NÃO é a melhor ferramenta para acções americanas

**Regra**: Para acções US, **yfinance é último recurso**, não primeiro. A ordem certa é:

1. **Dados já em DB** (`us_investments.db.fundamentals` / `prices` / `dividends`) — já curados pelos nossos guards (`guards.fundamentals` em `config/sources_priority.yaml`). Se está fresco (TTL respeitado), usar.
2. **FMP** — `fmp_client.py` + `claude.ai FMP MCP` (27 tools). Fundamentals, DCF, key metrics, analyst estimates. Cobertura US é o que foi feito para.
3. **SEC EDGAR** — `fetchers/sec_edgar_fetcher.py` + `monitors/sec_monitor.py`. Ground truth para dividend streaks (10-K Cash Flow), insider trades (Form 4), filings 8-K/10-K. **Canónico**.
4. **Massive.com** (ex-Polygon) — `fetchers/massive_fetcher.py`. Intraday, options, snapshots. Já wired com `MASSIVE_API_KEY`.
5. **Finnhub** (free tier 60/min) — analyst ratings, price targets, earnings calendar, insider transactions. Em `us_data_sources_catalog.md` mas ainda não wired — wire-it-up antes de re-bater na pedra.
6. **Bigdata.com MCP** — entity tearsheets, search, sentiment. Para context qualitativo.
7. **Exa neural search** — recall semântico para news/research. Já wired (`fetchers/exa_fetcher.py`).
8. **yfinance** — apenas para preço histórico simples (gratuito, longo histórico) ou como último fallback. **NUNCA como única fonte para fundamentals US.**

**Why:** yfinance tem bugs sistemáticos demonstrados e recorrentes:
- DY absurdos (AAPL 38%, V 85%, AMP 145%, LLY 73%) — mis-adjustment de splits ou fields errados. Ver [[memory/data_quality_dy_cagr]].
- Streak de dividendos via `t.dividends` é frágil (LLY veio 107 anos — artefacto óbvio).
- `info` dict não é estável (campos mudam silenciosamente entre versões).
- Sem ground truth de filings (não cobre 10-K/10-Q/8-K detalhe).
- Sem analyst consensus fiável (campos truncados).
- Free + no-auth = sem SLA, sem garantia de continuidade.

**Os USA têm infra-estrutura própria de mercado, regulada e auditável (SEC EDGAR, FMP, exchanges com APIs). Usar yfinance é desperdiçar isso e arriscar dados errados em decisões que envolvem dinheiro real.**

**How to apply:**
- Antes de qualquer script novo que precise de dados US, perguntar: *"qual a fonte canónica para este campo?"* — escolher da cascade acima.
- Em scripts existentes que ainda usam `yf.Ticker(X).info` directo para US fundamentals: marcar como dívida técnica e migrar.
- Em screens/research memos ad-hoc: **não usar yfinance live** — usar `ii fetch us fundamentals X --quality` (cascade respeitada) ou ler `us_investments.db` directo.
- Quando um valor parece absurdo (DY 145%, P/E 1000, streak 107y): **assumir bug** e cross-checar com SEC EDGAR ou FMP antes de citar.

**Incidente fundador (recorrentes — já é a Nª vez)**:
- 2026-04-21 — DY absurdos AAPL/V/XP/ABEV3 expostos; corrigida a regra computar DY internamente ([[memory/data_quality_dy_cagr]]).
- 2026-05-11 — fair_value_forward usa yfinance live para forward EPS; user pediu para ler `analyst_consensus` da DB em vez disso.
- **2026-05-13 — SWS Buffett+DRIP screening usou `yfinance` live para P/E fwd, DY, ROE, streak em 41 tickers. AMP veio com DY 145%, LLY com 107 anos de streak. Chefe disse "NOVAMENTE, o yfinance não é a melhor ferramenta para acções americanas. Anote isso em Erros Comuns Cometidos."**

**Status**: não internalizado. Reincidência recorrente. Próximo passo: ver §"Acções de reparação" abaixo.

**Acções de reparação queued**:
1. Mudar `config/sources_priority.yaml` US fundamentals: `fmp` primeiro, `sec_edgar` segundo (para streaks/filings), `yf_deep` terceiro, `yfinance` último.
2. Re-correr o screening SWS Buffett+DRIP com FMP MCP + SEC EDGAR; comparar deltas vs o memo de hoje.
3. Auditar todos os scripts em `scripts/` que usem `import yfinance` para US e marcar para migração.
4. Adicionar guard no `fetchers/_fallback.py`: para `market=us, kind=fundamentals`, log WARN se cair em yfinance.

---

## Próximas entradas (placeholder)

> Adicionar aqui à medida que o chefe identificar mais padrões repetentes.

---

## Como usar este documento

- **Antes de começar trabalho US**: ler #1 antes de escrever qualquer fetcher/script.
- **Em review de processos**: usar este doc como checklist de "estes erros já não podem aparecer".
- **Quando um erro é cometido**: adicionar entrada nova OU incrementar "incidente fundador" da entrada existente (não criar duplicada).
- **Quando um erro é internalizado**: mover para o final do doc na secção *Internalizados* (manter histórico, libertar atenção).
