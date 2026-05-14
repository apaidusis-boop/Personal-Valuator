# PETR4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Oil & Gas
- **RI URLs scraped** (1):
  - https://www.investidorpetrobras.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **49**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=46.43000030517578
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.28176 · DY=0.06804753347476936 · P/E=6.174202
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Petrobras antecipa início |
| 2026-04-30 | fato_relevante | cvm | Relatório de Produção e Vendas 1T26 |
| 2026-04-28 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Investor Tour 2026 |
| 2026-04-27 | fato_relevante | cvm | Petrobras amplia presença na Bacia de Campos com a aquisição de parte do ring-fe |
| 2026-04-23 | fato_relevante | cvm | Petrobras assina novo Acordo de Acionistas da Braskem |

## Agora (RI scrape live)

- Scrape: ❌ FALHOU — Traceback (most recent call last):
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 233, in <module>
    main()
    ~~~~^^
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 220, in main
    result = fetch(
        args.url,
    ...<5 lines>...
        headless=not args.no_headless,
    )
  File "C:\Users\paidu\investment-intellig
