# BBDC4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (2):
  - https://www.bradescori.com.br/
  - https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fatos-relevantes/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1837.0 · entry=16.1 · date=2026-05-07

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=18.09000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.13366 · DY=0.08428114909561732 · P/E=8.614286
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Fechamento da Consolidaçã |
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Publicação dos Relatórios |
| 2026-04-15 | comunicado | cvm | Esclarecimentos sobre questionamentos da CVM/B3 \| Notícia Divulgada na Mídia |
| 2026-04-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre a Reorg |
| 2026-03-25 | fato_relevante | cvm | Pagamento de Juros sobre o Capital Próprio Intermediários |

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
