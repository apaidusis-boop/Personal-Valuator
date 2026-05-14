# POMO3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.marcopolo.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.920000076293945
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.30973 · DY=0.1594748290258507 · P/E=5.92
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-15 | fato_relevante | cvm | Pagamento de Juros Sobre o Capital Próprio |
| 2026-03-24 | fato_relevante | cvm | Alteração dos portais de publicação |
| 2026-03-03 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-02-27 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação de Resultados 4T25 e |
| 2026-02-17 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |

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
