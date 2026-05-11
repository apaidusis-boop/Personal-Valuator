# AAPL — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.apple.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=5.0 · entry=121.89000000000001 · date=2020-11-16

- Total events na DB: **160**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=293.32000732421875
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=1.4147099 · DY=0.004432019526588434 · P/E=35.467957
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-30 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-20 | 8-K | sec | 8-K \| 5.02 |
| 2026-02-24 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-01-30 | 10-Q | sec | 10-Q |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 20.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.apple.com/ | ✅ | 20.3s | 25,119 |
- Filings extraídos do RI: **2**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **1**
- Headers detectados (structure): **39**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| March 28, 2026 | View the press release |
| 2026-05-07 | How filmmakers are redefining the art form with MAMI Select: Filmed on iPhone |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Investor Relations](https://investor.apple.com/investor-relations/default.aspx)
- [Annual green bond impact report](https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf#page=89)

### Audio / Video disponível (markitdown pode ler)

- [Apple Podcasts](https://www.apple.com/apple-podcasts/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 160 | 160 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 2026-05-07 — How filmmakers are redefining the art form with MAMI Select: Filmed on iPhone

URL: https://www.apple.com/newsroom/2026/05/how-filmmakers-are-redefining-the-art-form-with-mami-select-filmed-on-iphone/
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
* [Apple](/)
* + [Store](/us/shop/goto/store)

  + [Mac](/mac/)

  + [iPad](/ipad/)

  + [iPhone](/iphone/)

  + [Watch](/watch/)

  + [Vision](/apple-vision-pro/)

  + [AirPods](/airpods/)

  + [TV & Home](/tv-home/)

  + [Entertainment](/entertainment/)

  + [Accessories](/us/shop/goto/buy_accessories)

  + [Support](https://support.apple.com/?cid=gn-ols-home-hp-tab)
* 0+

[ ]

[Newsroom](/newsroom/)

Open Newsroom navigation

Close Newsroom navigation

* [Apple Services](/newsroom/apple-services/)
* [Apple Stories](/newsroom/apple-stories/)

Search Newsroom
Close

##

##

opens in new window

[![
](/newsroom/videos/2026/autoplay/05/apple-mami-select-filmed-on-iphone-hero/posters/Apple-MAMI-Select-Filmed-on-iPhone-hero.jpg.large_2x.jpg)](/newsroom/videos/2026/autoplay/05/apple-mami-select-filmed-on-iphone-hero/large_2x.mp4)

apple stories

# Meet four emerging filmmakers redefining the art form with MAMI Select: Filmed on iPhone

This year’s slate of innovative shorts showcases how new tools are changing not just the way films are made, but which stories get told

[Download Video](/newsroom/videos/2026/autoplay/05/apple-mami-select-filmed-on-iphone-hero/downloads/Apple-MAMI-Select-Filmed-on-iPhone-hero.zip)

The four emerging filmmakers behind this year’s MAMI Select: Filmed on iPhone shorts harnessed iPhone 17 Pro Max — along with MacBook Pro with M5 and iPad Pro with M5 — to construct distinct cinematic languages.

creatives
May 7, 2026

In telling the stories of a clande
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=5.0, entry=121.89000000000001. 1 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=1.4147099, DY=0.004432019526588434 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
