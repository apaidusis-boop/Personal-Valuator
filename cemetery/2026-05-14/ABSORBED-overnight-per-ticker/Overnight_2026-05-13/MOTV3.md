# MOTV3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.motiva.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=15.449999809265137
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.20401 · DY=0.02507482231602866 · P/E=10.510203
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-29 | fato_relevante | cvm | ABERTURA DO 4º PROGRAMA DE RECOMPRA DE AÇÕES |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-27 | fato_relevante | cvm | Intenção de Alienação de Participação Acionária - Grupo Mover. |
| 2026-04-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Movimentação Mensal - Mar |

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
