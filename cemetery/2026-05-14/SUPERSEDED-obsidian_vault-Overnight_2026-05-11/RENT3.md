# RENT3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.localiza.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **14**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=49.880001068115234
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.07211 · DY=0.041282196389451825 · P/E=24.09662
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-28 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Juros sobre o capital pró |
| 2026-03-25 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-24 | fato_relevante | cvm | Juros sobre o Capital Próprio |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 13.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.localiza.com/ | ✅ | 13.6s | 54,970 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **42**
- Audio/video: **36**
- Headers detectados (structure): **90**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (42 total, top 12)

- [Apresentações](https://ri.localiza.com/informacoes-aos-acionistas/apresentacoes-e-teleconferencias/)
- [Apresentação de Resultados](https://mz-filemanager.s3.amazonaws.com/08f327aa-e610-4d9d-b683-8ff0f7caae07/1t17/c4eab503ed291445c963c3418d525cf85fa344391d9b4b611b8f5d2248c7f663/download__da_apresentacao.pdf)
- [Release de Resultados](https://mz-filemanager.s3.amazonaws.com/08f327aa-e610-4d9d-b683-8ff0f7caae07/1t17/673722ae66696b0df5668d1d38d2cd32ba9389ac32ff5c5acc710edca216afca/earnings_release_1t17.pdf)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/b588eef5-90e3-92ff-04d9-4fd4d20656ba?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/1b4a1685-04e8-d704-8144-43a341cff1a7?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/883be988-ba9f-fe9f-427c-47f310f3fcd4?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/78494ca0-b24d-8423-ac34-3843ff15a708?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/d624b4c8-5633-4040-813a-f4f6388f187e?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/c6a06103-ef0d-2cc8-1678-b59d6e92e3ab?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/9240cc70-b2cf-78c0-f716-4016648add50?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/9c3faefd-7745-aef2-7f5a-03192c0bda7d?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/23dca5f8-5fe9-1e78-13b7-e3282937bf44?origin=2)
- _… e mais 30 no MD raw (`data/portal_cache/`)_

### Audio / Video disponível (markitdown pode ler)

- [Comunicado ao Mercado - Webcast 1T26](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/874c7dfc-be8a-8aed-9606-cda9be317bc9?origin=2)
- [Teleconferência](https://mz-filemanager.s3.amazonaws.com/08f327aa-e610-4d9d-b683-8ff0f7caae07/1t17/c3d20105d337952e48f3be31b6daa8959542864b10e14225af46f28cd7689104/download_do_audio.mp3)
- [Teleconferência](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/911386b5-62c1-5ca5-a309-4eabe7f613b0?origin=2)
- [Teleconferência](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/29b6255c-2e57-d800-a8e2-0ea09486393c?origin=2)
- [Teleconferência](https://api.mziq.com/mzfilemanager/v2/d/08f327aa-e610-4d9d-b683-8ff0f7caae07/d211fdb1-b06c-ac95-4f5b-20105c281bca?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 14 | 14 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 42 | + |
| Audio/video acessível | 0 (era cego) | 36 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **36 fontes audio/video** disponíveis (markitdown pode transcrever)
- **42 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **36 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 42 releases/relatórios — podemos auditar se ROE=0.07211, DY=0.041282196389451825 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
