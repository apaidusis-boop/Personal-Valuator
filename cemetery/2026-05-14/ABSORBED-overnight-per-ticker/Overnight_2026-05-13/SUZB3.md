# SUZB3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://ri.suzano.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **11**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=43.130001068115234
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.26295 · DY=0.025994411598306812 · P/E=4.6931453
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação de Resultados 1T26 |
| 2026-04-02 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| L |
| 2026-03-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| 1 |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Termo de Emissão (CPR-F) |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aprovação da 2° Oferta pú |

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
