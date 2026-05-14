# B3SA3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ri.b3.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=17.59000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.26738 · DY=0.03444695820033037 · P/E=19.119566
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Conclusão de Venda de Par |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Cronograma de divulgação  |
| 2026-04-15 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - març |
| 2026-03-19 | fato_relevante | cvm | Alteração na Administração da B3 |
| 2026-03-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - feve |

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
