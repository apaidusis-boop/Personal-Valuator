# RDOR3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://ri.rededorsaoluiz.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **5**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=35.970001220703125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.19188 · DY=0.11873116083026136 · P/E=17.128572
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-16 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-23 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Distribuição de Juros Sob |
| 2026-03-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Habilitação Medicina |
| 2026-02-26 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação da Teleconferência d |
| 2026-01-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Fechamento do Acordo Atlâ |

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
