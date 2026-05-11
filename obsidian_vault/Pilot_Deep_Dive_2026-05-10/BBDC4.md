# BBDC4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Bank
- **RI URLs scraped** (2):
  - https://www.bradescori.com.br/
  - https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fatos-relevantes/
- **Pilot rationale**: Bradesco own RI (different provider)

## Antes (estado da DB)

**Posição activa**: qty=1837.0 · entry=16.1 · date=2026-05-07

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=18.59000015258789
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.13366 · DY=0.08201430809497631 · P/E=8.852382
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

- Scrape: ✅ **2/2 URLs OK** · total 0.1s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.bradescori.com.br/ | ✅ | 0.1s | 16,520 |
| https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fat | ✅ | 0.1s | 24,720 |
- Filings extraídos do RI: **27**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **2**
- Headers detectados (structure): **4**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 06-05-2026 | Bradesco 1T26 - Press Release |
| 06-05-2026 | Resultados e Videoconferência 1T26 |
| 30-04-2026 | Comunicado ao Mercado - Publicação ... |
| 30-04-2026 | Comunicado ao Mercado - Fechamento ... |
| 29-04-2026 | Convite para Videoconferência de Re... |
| 16-04-2026 | Agenda da Divulgação de Resultados ... |
| 30-04-2026 | Comunicado ao Mercado - Fechamento da Consolidação dos Negócios de Saúde – Homol |
| 29-04-2026 | Convite para Videoconferência de Resultados 1T26 |
| 16-04-2026 | Agenda da Divulgação de Resultados 1T26 |
| 15-04-2026 | Esclarecimentos sobre Questionamentos da CVM/B3 - Ofício nº 152/2026/CVM/SEP/GEA |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Relatório Integrado e ESG](https://www.bradescori.com.br/o-bradesco/relatorio-integrado-e-esg/)
- [Relatórios e Planilhas](https://www.bradescori.com.br/informacoes-ao-mercado/relatorios-e-planilhas/relatorios/)
- [Apresentações](https://www.bradescori.com.br/informacoes-ao-mercado/apresentacoes/)
- [Bradesco 1T26 - Relatório de Anális...](https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/7cb24c7c-e2f1-eb15-8222-620ba0d80519?origin=2)
- [Bradesco 1T26 - Apresentação de Res...](https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/2a3c3776-7c17-55d6-0c6a-2a9a0b306272?origin=2)
- [Relatório ESG 2025](https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/a87ae47b-e0c3-27c7-8d51-2ce5233e7716?origin=2)

### Audio / Video disponível (markitdown pode ler)

- [Assista ao replay da Videoconferência de Resultados do 1T26](https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/964c0bf2-e893-fc9c-a943-05e6ac002467?origin=2)
- [Assista ao replay da Videoconferência de Resultados do 1T26 da Bradsaúde](https://www.youtube.com/live/mKdUCECdup8)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 15 | 15 + 27 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**27 filings detectados como novos vs DB.**

### 1. 31-03-2026 — Comunicado ao Mercado - Mapa Final de Votação Resumido (AGE 31.3.26)

URL: https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/b1d3459b-0487-7b03-dbaf-10d3015be3e9?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
Banco Bradesco S.A. Mapa final de
Companhia Aberta votação resumido
CNPJ no 60.746.948/0001-12 (Boletim de Voto a Distância)
Assembleia Geral Extraordinária de 31.3.2026
O Banco Bradesco S.A., nos termos da Resolução CVM no 81/22, divulga o
“Mapa final de votação resumido” consolidando os votos proferidos a
distância e aqueles computados durante a assembleia por seus acionistas,
com as indicações do total de aprovações, rejeições e abstenções para
cada uma das matérias examinadas, discutidas e votadas na Assembleia
Geral Extraordinária realizada nesta data, às 16h.
Cidade de Deus, Osasco, SP, 31 de março de 2026
Banco Bradesco S.A.
André Costa Carvalho
Diretor de Relações com Investidores

Mapa  final de votação resumido
Empresa:                                      00001 - BANCO BRADESCO S.A.
Cód. Assembleia B3:
Tipo Assembleia:                        ASSEMBLEIA GERAL EXTRAORDINÁRIA
Data da Assembleia:                31/03/2026                            Hora da Assembleia: 16:00
Perído de Votação:
Até: 27/03/2026
27/02/2026
VOTO DA DELIBERAÇÃO E QUANTIDADE
| CÓDIGO DA  |     |     | DE AÇÕES |     |
| ---------- | --- | --- | -------- | --- |
DELIBERAÇÃO (BOLETIM  DESCRIÇÃO DA DELIBERAÇÃO
| DE VOTO A DISTÂNCIA) |     | APROVAR  | REJEITAR  |     |
| -------------------- | --- | -------- | --------- | --- |
ABSTER-SE
|     |     | (SIM) | (NÃO) |     |
| --- | --- | ----- | ----- | --- |
Deliberação
“Protocolo e Justificação de Cisão Parcial da Bradseg Participações S.A. com
```

### 2. 30-04-2026 — Comunicado ao Mercado - Publicação ...

URL: https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/879c8e73-af0b-09ac-c3fc-f19bcbd378c8?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
Banco Bradesco S.A.
Companhia Aberta
CNPJ no 60.746.948/0001-12

Comunicado ao Mercado

Publicação dos Relatórios Integrado e ESG de 2025

O  Banco  Bradesco  S.A.  (“Bradesco”)  (B3:  BBDC3,  BBDC4;  NYSE:  BBD,  BBDO;  e  Latibex:

XBBDC) comunica aos seus acionistas e ao mercado em geral que publicou, nesta data, os

Relatórios Integrado e ESG referentes a 2025, arquivando-os também na CVM.

Em conjunto, os documentos compartilham informações importantes do Bradesco sobre

governança,  estratégia,  modelo  de  gestão  de  riscos  e  oportunidades,  os  principais

resultados  financeiros  alcançados  no  exercício,  além  do  desempenho  em  indicadores

ambientais, sociais e climáticos.

Os relatórios podem ser acessados no website de Relações com Investidores do Bradesco

- banco.bradesco/ri.

Cidade de Deus, Osasco, SP, 30 de abril de 2026.

Banco Bradesco S.A.

André Costa Carvalho
Diretor de Relações com Investidores

Página 1 de 1


```

### 3. 30-04-2026 — Comunicado ao Mercado - Fechamento ...

URL: https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/7f09c21b-5007-40fe-d302-8f9809f86483?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
Banco Bradesco S.A.
Companhia Aberta

o
 60.746.948/0001-12
CNPJ n

Comunicado ao Mercado

Fechamento da Consolidação dos Negócios de Saúde – Homologação da
Incorporação de Ações

O  Banco  Bradesco  S.A.  (“Bradesco”),  em  continuidade  às  divulgações  anteriores
relativas  à  consolidação  dos  negócios  de  saúde  da  Organização  Bradesco  na
Bradsaúde  S.A.  (atual  denominação  da  Odontoprev  S.A.)  (“Bradsaúde”),  comunica
aos seus acionistas e ao mercado em geral que:

(i)  na  presente  data,  foi  homologada  e  consumada  a  incorporação  das  ações  de
emissão da Bradesco Gestão de Saúde S.A. (“BGS”) pela Bradsaúde (“Incorporação
de Ações”), com a confirmação da relação de troca previamente estabelecida, sem
ajustes.

Com a consumação da Incorporação de Ações, a BGS passou a ser subsidiária integral
da Bradsaúde, e a participação do Bradesco no capital social da Bradsaúde passou a
representar  91,35%  do  capital  total  e  votante  (sem  levar  em  conta  eventuais
exercícios do direito de retirada por acionistas dissidentes da Bradsaúde, cujo prazo
se encerrará em 7 de maio de 2026); e

(ii)  conforme  anteriormente  divulgado,  será  realizada,  em  1º  de  maio  de  2026,  a
assembleia geral extraordinária da Mediservice Operadora de Planos de Saúde S.A.
(“Mediservice”),  na  qual  será  aprovada  a  contribuição  da  carteira  de  planos
odontológicos  e  demais  ativos  e  passivos  operacionais  da  Bradsaúde  para  a
Mediservice,  a  qual  se  tornou,  
```

### 4. 30-04-2026 — Comunicado ao Mercado - Fechamento da Consolidação dos Negócios de Saúde – Homologação da Incorporação de Ações

URL: https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/7f09c21b-5007-40fe-d302-8f9809f86483?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
Banco Bradesco S.A.
Companhia Aberta

o
 60.746.948/0001-12
CNPJ n

Comunicado ao Mercado

Fechamento da Consolidação dos Negócios de Saúde – Homologação da
Incorporação de Ações

O  Banco  Bradesco  S.A.  (“Bradesco”),  em  continuidade  às  divulgações  anteriores
relativas  à  consolidação  dos  negócios  de  saúde  da  Organização  Bradesco  na
Bradsaúde  S.A.  (atual  denominação  da  Odontoprev  S.A.)  (“Bradsaúde”),  comunica
aos seus acionistas e ao mercado em geral que:

(i)  na  presente  data,  foi  homologada  e  consumada  a  incorporação  das  ações  de
emissão da Bradesco Gestão de Saúde S.A. (“BGS”) pela Bradsaúde (“Incorporação
de Ações”), com a confirmação da relação de troca previamente estabelecida, sem
ajustes.

Com a consumação da Incorporação de Ações, a BGS passou a ser subsidiária integral
da Bradsaúde, e a participação do Bradesco no capital social da Bradsaúde passou a
representar  91,35%  do  capital  total  e  votante  (sem  levar  em  conta  eventuais
exercícios do direito de retirada por acionistas dissidentes da Bradsaúde, cujo prazo
se encerrará em 7 de maio de 2026); e

(ii)  conforme  anteriormente  divulgado,  será  realizada,  em  1º  de  maio  de  2026,  a
assembleia geral extraordinária da Mediservice Operadora de Planos de Saúde S.A.
(“Mediservice”),  na  qual  será  aprovada  a  contribuição  da  carteira  de  planos
odontológicos  e  demais  ativos  e  passivos  operacionais  da  Bradsaúde  para  a
Mediservice,  a  qual  se  tornou,  
```

### 5. 30-03-2026 — Comunicado ao Mercado - Mapa Sintético Consolidado de Votação (AGE 31.3.26)

URL: https://api.mziq.com/mzfilemanager/v2/d/80f2e993-0a30-421a-9470-a4d5c8ad5e9f/ca79e0f2-cd45-83b9-8182-edbd8e6cfc2d?origin=2
Após data máxima DB: **SIM (após max DB date)**


## Sinais / observações

- **27 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **30-04-2026** matched `incorporação` → M&A — diluição/sinergia trade-off: _Comunicado ao Mercado - Fechamento da Consolidação dos Negócios de Saúde – Homol_
- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=1837.0, entry=16.1. 27 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=0.13366, DY=0.08201430809497631 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
