# SUZB3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://ri.suzano.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **11**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=43.70000076293945
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.26295 · DY=0.025655354243169746 · P/E=4.755169
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação de Resultados 1T26 |
| 2026-04-02 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| L |
| 2026-03-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado \| 1 |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Termo de Emissão (CPR-F) |
| 2026-03-09 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aprovação da 2° Oferta pú |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 15.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.suzano.com.br/ | ✅ | 15.4s | 15,029 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **1**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 2026-04-30 | Releases de Resultados(opens in new window) |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Relatórios e Eventos](https://ri.suzano.com.br/Portuguese/ESG/Relatorios-e-Eventos/default.aspx)
- [Apresentações](https://ri.suzano.com.br/Portuguese/Informacoes-Aos-Investidores/Apresentacoes/default.aspx)
- [Acesse o Relatório aqui](https://ri.suzano.com.br//s201.q4cdn.com/761980458/files/doc_downloads/2026/03/RS2025_POR_Vfinal.pdf)
- [Demonstrações Financeiras(opens in new window)](https://s201.q4cdn.com/761980458/files/doc_news/2026/04/1T26/DF/DFP-ITR-PT.pdf)
- [Apresentação de Resultados(opens in new window)](https://s201.q4cdn.com/761980458/files/doc_news/2026/04/1T26/Apresentacao/Apresenta%C3%A7%C3%A3o-de-Resultados-1T26_PORT-v4.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://s201.q4cdn.com/761980458/files/doc_news/2026/04/1T26/Audio/suzano_1q26_por-1.mp3)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 11 | 11 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 2026-04-30 — Releases de Resultados(opens in new window)

URL: https://s201.q4cdn.com/761980458/files/doc_news/2026/04/1T26/Release/Release-de-Resultados_1T26_PT-2026-04-30-16-27.pdf
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
RESULTADOS
1T26
Sólido desempenho operacional e preços mais elevados de celulose.
EBITDA impactado por BRL mais forte.
São Paulo, 29 de abril de 2026. Suzano S.A. (B3: SUZB3 | NYSE: SUZ), uma das maiores produtoras de
celulose e integradas de papel do mundo, anuncia hoje os resultados consolidados do 1º trimestre de
2026 (1T26).
DESTAQUES
• Vendas de celulose de 2.835 mil t (+7% vs. 1T25).
Vendas de papel1 de 378 mil t (-3% vs. 1T25).
•
• EBITDA Ajustado2 e Geração de caixa operacional3: R$ 4,6 bilhões e R$ 2,5 bilhões, respectivamente.
• EBITDA Ajustado2/t de celulose em R$ 1.431/t (-11% vs. 1T25).
• EBITDA Ajustado2/t de papel em R$ 1.385/t (-12% vs. 1T25).
• Preço médio líquido de celulose – mercado externo: US$ 562/t (+1% vs. 1T25).
Preço médio líquido de papel1 de R$ 6.933/t (-8% vs. 1T25).
•
• Custo caixa de produção de celulose sem paradas de R$ 802/t (-7% vs. 1T25).
• Alavancagem em 3,3x em US$ e 3,2x em R$.
• Free Cash Flow Yield ("FCF Yield" - UDM) de 13,6% (-4,9 p.p. vs. 1T25).
• ROIC ("Return on Invested Capital" - UDM) de 10,1% (-3,7 p.p. vs. 1T25).
Dados Financeiros Consolidados
|     | 1T26 | 4T25 | Δ Q-o-Q | 1T25 | Δ Y-o-Y | UDM 1T26 |
| --- | ---- | ---- | ------- | ---- | ------- | -------- |
(R$ milhões)
| Receita Líquida         | 10.968 | 13.114 | -16%    | 11.553 | -5%    | 49.531 |
| ----------------------- | ------ | ------ | ------- | ------ | ------ | ------ |
| EBITDA Ajustado2        | 4.580  | 5.583  | -18%    | 4.866  | -6%    | 21.451 |
| Margem
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.26295, DY=0.025655354243169746 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
