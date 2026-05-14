# RAPT4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.randoncorp.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.25
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=-0.0129700005 · DY=None · P/E=None
- Score (último run): score=0.3333 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Mar/20 |
| 2026-03-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Fev/20 |
| 2026-03-13 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Videoconferência de  |
| 2026-03-12 | fato_relevante | cvm | Guidance 2026 - Projeções |
| 2026-02-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Divulgação Receita Jan/20 |

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
