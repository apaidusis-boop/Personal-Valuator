# ALOS3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://ri.allos.com.br/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **11**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=29.799999237060547
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.068569995 · DY=0.07605765295393907 · P/E=17.951807
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-10 | fato_relevante | cvm | Celebração de Memorando de Entendimento para constituição de Fundo de  Investime |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reestruturações societári |
| 2026-04-02 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Encerramento da Oferta Pú |
| 2026-03-19 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atribuição de Rating AAA. |
| 2026-03-12 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |

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
