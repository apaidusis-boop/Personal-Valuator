# XPLG11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Logística
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/xplg11/
- **Pilot rationale**: fii_heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=99.97000122070312
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=None · DY=0.09842952765676471 · P/E=19.756918
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 32.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.fiis.com.br/xplg11/ | ✅ | 32.7s | 12,150 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 30-04-2026 | Mais de 170 fundos imobiliários (FIIs) divulgam dividendos (30); veja valores |

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

### 1. 30-04-2026 — Mais de 170 fundos imobiliários (FIIs) divulgam dividendos (30); veja valores

URL: https://fiis.com.br/noticias/fundos-imobiliarios-fiis-podem-divulgar-dividendos-valores-hoje-30-04-2026-jj/
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

- 🚨 **30-04-2026** matched `dividend` → Dividend declaration: _Mais de 170 fundos imobiliários (FIIs) divulgam dividendos (30); veja valores_

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
