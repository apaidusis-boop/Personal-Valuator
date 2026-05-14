# CPLE3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.copel.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=15.069999694824219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.10787 · DY=0.07051088397599298 · P/E=16.560438
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 08/ |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 02/ |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Arquivamento Relatório An |
| 2026-03-18 | fato_relevante | cvm | FR 01/26 - Copel vence leilão de reserva de capacidade com duas usinas hidrelétr |
| 2026-03-18 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação - Leilão de Reserva  |

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
