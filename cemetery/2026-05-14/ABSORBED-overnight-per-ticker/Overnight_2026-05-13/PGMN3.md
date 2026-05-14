# PGMN3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://ri.paguemenos.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **9**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=5.019999980926514
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.089729995 · DY=0.051099203381402385 · P/E=10.244898
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-03-23 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional (PT/EN |
| 2026-03-18 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-16 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-10 | fato_relevante | cvm | Aprovação do Preço por Ação no âmbito da Oferta Pública de Distribuição Primária |
| 2026-03-03 | fato_relevante | cvm | Oferta Pública de Distribuição Primária e Secundária de Ações Ordinárias de Emis |

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
