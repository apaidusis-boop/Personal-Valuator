# MULT3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://www.multri.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=31.010000228881836
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.20018 · DY=0.03493205391824209 · P/E=12.554656
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Data de eficácia da capit |
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência de Resultados - 1 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Participação de executivo |
| 2026-04-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Alienação de Participação |
| 2026-04-07 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Reunião Pública Multiplan 2026 -  |

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
