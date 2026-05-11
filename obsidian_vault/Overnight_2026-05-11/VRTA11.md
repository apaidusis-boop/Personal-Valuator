# VRTA11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Papel (CRI)
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/vrta11/
- **Pilot rationale**: fii_heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=77.11000061035156
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.081949994 · DY=0.13227856204465793 · P/E=11.450846
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 32.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.fiis.com.br/vrta11/ | ✅ | 32.8s | 11,703 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 2023-09-28 | VRTA11 e VRTM11 divulgam novos dividendos; yield supera 1% |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 2023-09-28 — VRTA11 e VRTM11 divulgam novos dividendos; yield supera 1%

URL: https://fiis.com.br/noticias/fundo-imobiliario-vrta11-vrtm11-divulgam-novos-dividendos-yield/
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[![Logo Fiis](https://fiis.com.br/wp-content/themes/fiis/resources/images/logo-fiis.svg)](https://fiis.com.br)

menu mobile
      [ ]

* [Notícias](/noticias)
* [Artigos](/artigos)
* FiisFiis[ ]
  + [Atualizações](/atualizacoes)
  + [Lista de Fiis](https://fiis.com.br/lista-de-fundos-imobiliarios/)
  + [Resumo](/resumo)
  + [Lupa de FIIs](/lupa-de-fiis)
  + [Rendimentos](/rendimentos)
  + [Assembleias](/calendario-de-assembleias)
  + [Fundos do IFIX](/ifix)
  + [Glossário](/glossario)
* GratuitoGratuito[ ]
  + [Suno One](https://lp.suno.com.br/suno-one/?utm_source=fiis.com.br&utm_medium=topbar&utm_campaign=_SNC55C1611B_)
  + [Siga o grupo Suno](https://www.suno.com.br/newsletters-suno/?utm_source=fiis.com.br&utm_medium=topbar&utm_campaign=_SNC55C1611B_)
  + [E-book Investindo em Fiis](https://lp.fiis.com.br/ebook-manual-do-investidor-em-fiis/?utm_source=fiis.com.br&utm_medium=topbar&utm_campaign=_SNC55C1611B_)
  + [Planilha de controle de gastos](https://lp.suno.com.br/planilha-controle-gastos/?utm_source=fiis.com.br&utm_medium=topbar&utm_campaign=_SNC55C1611B_)
  + [Grupo de whatsapp](https://lp.fiis.com.br/whatsapp-fiis/?utm_source=fiis.com.br&utm_medium=topbar&utm_campaign=_SNC55C1611B_)
* AproveiteAproveite[ ]
  + [Carteira Suno](https://lp.suno.com.br/nossas-assinaturas/suno-fundos-imobiliarios/?utm_source=Afiliado&utm_medium=Fiis.com.br&utm_campaign=_SNCDC1C07F7_)
  + [Consultoria Suno](https://lp.suno.com.br/ao/servico-especializado-aw/?utm_source=fiis.com.br&utm_mediu
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional

## Interpretação para a tese

- 🚨 **2023-09-28** matched `dividend` → Dividend declaration: _VRTA11 e VRTM11 divulgam novos dividendos; yield supera 1%_

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
