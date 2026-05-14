# BRKM5 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://www.braskem-ri.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=8.989999771118164
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=None · DY=None · P/E=None
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.5s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.braskem-ri.com.br/ | ✅ | 12.5s | 99,616 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **2**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/05/2026 | Ver + |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Relatórios Anuais](https://www.braskem-ri.com.br/divulgacoes-documentos/relatorios-anuais/)

### Audio / Video disponível (markitdown pode ler)

- [Apresentações e Teleconferências](https://www.braskem-ri.com.br/divulgacoes-documentos/apresentacoes-e-teleconferencias/)
- [Vídeos e Podcasts](https://www.braskem-ri.com.br/servicos-aos-investidores/videos-podcasts/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 05/05/2026 — Ver +

URL: https://www.braskem-ri.com.br/divulgacoes-documentos/avisos-comunicados-ao-mercado-e-fatos-relevantes/
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[![](https://cdn-sites-assets.mziq.com/wp-content/uploads/sites/900/2021/11/BRASKEM-PREFERENCIAL-NEGATIVA-RGB-TRANSP-1.png)](https://www.braskem-ri.com.br)
Relações com Investidores

* A+
  A-
* Contraste
* [Acessibilidade](/acessibilidade/)
* + [Institucional](https://www.braskem.com.br)
* + [Português](https://www.braskem-ri.com.br/divulgacoes-documentos/avisos-comunicados-ao-mercado-e-fatos-relevantes/)
  + [English](https://www.braskem-ri.com.br/en/divulgacoes-documentos/notices-and-material-facts/)

* [Institucional](https://www.braskem.com.br)

* A+
  A-
* Contraste
* [Acessibilidade](/acessibilidade/)
* + [Institucional](https://www.braskem.com.br)

* A Companhia
  + [Perfil](https://www.braskem-ri.com.br/a-companhia/perfil/)
  + [Histórico](https://www.braskem-ri.com.br/a-companhia/historico/)
  + [O Setor Petroquímico](https://www.braskem-ri.com.br/a-companhia/o-setor-petroquimico/)
  + [Por que investir na Braskem?](https://www.braskem-ri.com.br/a-companhia/por-que-investir-na-braskem/)
  + [Estrutura Societária](https://www.braskem-ri.com.br/a-companhia/estrutura-societaria/)
  + [Conselhos e Diretoria](https://www.braskem-ri.com.br/a-companhia/conselhos-e-diretoria/)
  + [Estatutos e Políticas](https://www.braskem-ri.com.br/a-companhia/estatutos-e-politicas/)
* ESG
  + [Visão Geral](https://www.braskem-ri.com.br/esg/visao-geral/)
    - [Ambiental](https://www.braskem-ri.com.br/esg/visao-geral/ambiental/)
    - [Social](https://www.braskem-ri.com.br/esg/visao-geral
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=None, DY=None batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
