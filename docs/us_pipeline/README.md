# US Pipeline — Playbook e Referências

Esta pasta contém **tudo o que foi reunido durante a fase BR** para servir
como ponto de partida quando se atacar o lado US do `investment-intelligence`.

Neste momento (Abr 2026) o pipeline US **não está implementado**. Só há:
- `fetchers/yfinance_fetcher.py` (existente, nunca corrido em batch)
- `scoring/engine.py score_us()` (critérios Buffett, testável assim que houver DB populada)
- `data/us_investments.db` (schema aplicado, vazio)

## Índice

- [`README.md`](README.md) — este ficheiro
- [`api_catalog.md`](api_catalog.md) — catálogo completo de APIs US (gratuitas + pagas)
- [`patterns_to_port.md`](patterns_to_port.md) — padrões de arquitetura a replicar
- [`modules_to_port.md`](modules_to_port.md) — mapa ficheiro-a-ficheiro do que aproveitar
- [`vendor/skill-financial-analyst/`](vendor/skill-financial-analyst/) — repo inteiro clonado,
  MIT-licensed, fonte primária das ideias

## Porque esta pasta existe

Durante a fase BR descobrimos o repo público
[`geogons/skill-financial-analyst`](https://github.com/geogons/skill-financial-analyst)
— uma Claude Skill profissional para análise financeira US. Está licenciado MIT,
tem ~7.8K linhas de Python, 14 módulos, cobertura de 14+ APIs US com fallback chains.

Em vez de reinventar, quando chegar a altura do US:
1. Portamos o que encaixa na nossa filosofia Graham/Buffett/DRIP
2. Descartamos o que é swing-trading-centric (entries/exits próximos, sentiment social)
3. Mantemos a estrutura SQLite + scoring pass/fail/n/a + HTML Plotly

## Como usar quando chegar a altura

1. Ler [`api_catalog.md`](api_catalog.md) e escolher 2–3 APIs para arranque
   (sugestão: yfinance + SEC EDGAR + Finnhub free)
2. Criar contas gratuitas, colocar tokens em `.env`
3. Ler [`patterns_to_port.md`](patterns_to_port.md) para perceber as decisões
   arquiteturais deles
4. Ler [`modules_to_port.md`](modules_to_port.md) para saber que ficheiros
   copiar-adaptar e para onde
5. Para cada módulo portado, incluir a atribuição MIT no header do ficheiro
   derivado (exemplo em `vendor/skill-financial-analyst/LICENSE`)

## Licença dos ficheiros vendored

O repo `vendor/skill-financial-analyst/` está sob **MIT License**, copyright
(c) 2026 Contributors. A licença completa está em
`vendor/skill-financial-analyst/LICENSE`. Qualquer código derivado deste
ponto de partida tem de preservar a nota de copyright conforme exigido
pela MIT.

## O que NÃO está aqui

- Código adaptado para BR (esse vive em `fetchers/`, `analytics/`, etc.)
- Decisões sobre o universo US (quando for a altura, `config/universe.yaml`
  ganhará uma secção `us:` análoga à `br:`)
- Tokens ou secrets (`.env` continua fora do git)
