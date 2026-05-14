# EQTL3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.equatorialenergia.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **24**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=41.52000045776367
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.06985 · DY=0.03813326065857366 · P/E=43.25
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Resultado sobre proposta  |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Release Operacional - 1t2 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reajuste Tarifário - Equa |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-15 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional 4T25 |

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
