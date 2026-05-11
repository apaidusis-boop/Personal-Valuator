# ISAE4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://www.isacteep.com.br/ri/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=30.3700008392334
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.12099 · DY=0.053423080512531 · P/E=8.530899
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 27.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.isacteep.com.br/ri/ | ✅ | 27.4s | 15,107 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **1**
- Headers detectados (structure): **14**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Demonstrações das Subsidiárias](https://www.isacteep.com.br/pt/informacoes-financeiras/demonstracoes-das-subsidiarias)
- [Relatório Anual de Sustentabilidade](https://www.isacteep.com.br/pt/sustentabilidade/relatorio-anual-de-sustentabilidade)
- [Apresentação Divulgação de Resultados 1T26](https://www.isacteep.com.br/pt/documentos/6582-ISA-ENERGIA-Resultados-1T26-vfinal.pdf)
- [Release de Resultados - 1T26](https://www.isacteep.com.br/pt/documentos/6574-Earnings-Release-1T26.pdf)
- [Apresentação Divulgação de Resultados 2T25](https://www.isacteep.com.br/pt/documentos/6245-ISA-ENERGIA-Resultados-2T25.pdf)
- [Release de Resultados - 2T25](https://www.isacteep.com.br/pt/documentos/6235-Earnings-Release-2T25.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Apresentações & Teleconferências](https://www.isacteep.com.br/pt/divulgacao-ao-mercado/apresentacoes-teleconferencias)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=0.12099, DY=0.053423080512531 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
