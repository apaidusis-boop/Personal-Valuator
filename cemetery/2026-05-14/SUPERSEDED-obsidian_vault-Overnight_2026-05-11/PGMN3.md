# PGMN3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://ri.paguemenos.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **9**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=5.099999904632568
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.089729995 · DY=0.050297647999364224 · P/E=10.408163
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

- Scrape: ✅ **1/1 URLs OK** · total 11.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.paguemenos.com.br/ | ✅ | 11.3s | 15,335 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **2**
- Headers detectados (structure): **11**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Apresentações](https://ri.paguemenos.com.br/informacoes-aos-investidores/apresentacoes/)
- [Apresentação 1T26](https://api.mziq.com/mzfilemanager/v2/d/2cf06553-5bc1-44cd-b75f-6f3cd49d155d/74f4a63a-172f-bdbf-2572-73ecd713b704?origin=2)
- [Apresentação 4T25](https://api.mziq.com/mzfilemanager/v2/d/2cf06553-5bc1-44cd-b75f-6f3cd49d155d/6a6a2a49-a022-33ea-0031-bfaa23a1925a?origin=2)
- [Apresentação 3T25](https://api.mziq.com/mzfilemanager/v2/d/2cf06553-5bc1-44cd-b75f-6f3cd49d155d/9bdd199c-15d4-da15-6681-0df5c384ec79?origin=1)
- [Apresentação 2T25](https://api.mziq.com/mzfilemanager/v2/d/2cf06553-5bc1-44cd-b75f-6f3cd49d155d/ed38bc91-b7b6-f76a-76ee-9cd236b2cc71?origin=1)

### Audio / Video disponível (markitdown pode ler)

- [Videoconferência 4T25](https://drive.google.com/file/d/18CLdRWpVeAlRgC5_r9TEwY2IrXqPt99C/view)
- [Videoconferência 3T25](https://api.mziq.com/mzfilemanager/v2/d/2cf06553-5bc1-44cd-b75f-6f3cd49d155d/ff604eb7-30c7-a21f-f064-475a0765223d?origin=1)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 9 | 9 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.089729995, DY=0.050297647999364224 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
