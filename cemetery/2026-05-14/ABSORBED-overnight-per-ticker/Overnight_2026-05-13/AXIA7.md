# AXIA7 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (2):
  - https://ri.axiaenergia.com.br/
  - https://ri.light.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **33**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=55.09000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.07862 · DY=None · P/E=None
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Arquivamento do Form 20-F |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado - A |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reapresentação de BVD |
| 2026-04-01 | fato_relevante | cvm | Aprovação de Migração para o Novo Mercado |
| 2026-04-01 | fato_relevante | cvm | Deslistagem dos Americans Depositary Recepits - ADRs |

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
