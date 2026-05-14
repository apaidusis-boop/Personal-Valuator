# EZTC3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://ri.eztec.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=13.420000076293945
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.10949001 · DY=0.08296378492327612 · P/E=6.71
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.eztec.com.br/ | ✅ | 12.8s | 66,906 |
- Filings extraídos do RI: **2**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **0**
- Headers detectados (structure): **37**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 07/05/2026 | Conselho de Administração - Ata (Reporte trimestral de atividades do CA; Aprovaç |
| 07/05/2026 | Comunicado ao Mercado - Comunicado de Lançamento GranResort Reserva São Caetano  |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Relatórios e Arquivamentos CVM](https://ri.eztec.com.br/arquivamentos-cvm/)
- [Relatórios de ESG](https://ri.eztec.com.br/governanca-compliance/#section-1)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 07/05/2026 — Conselho de Administração - Ata (Reporte trimestral de atividades do CA; Aprovação do Relatório de Administração; Deliberação dos Dividendos Intermediários)

URL: https://api.mziq.com/mzfilemanager/v2/d/653fada3-cbcd-4015-9a94-2149f610a321/1163c0aa-22df-8517-b8a8-39922e9de8a0?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
EZ TEC EMPREENDIMENTOS E PARTICIPAÇÕES S.A.
CNPJ 08.312.229/0001-73
NIRE 35300334345
Companhia Aberta

ATA DA REUNIÃO DO CONSELHO DE ADMINISTRAÇÃO
REALIZADA EM 07 DE MAIO DE 2026

DATA, HORA E LOCAL: Em 07 de maio de 2026, às 10h00 horas, na sede social da Ez Tec
Empreendimentos e Participações S.A. (“Companhia”), situada na Avenida República do
Líbano, nº 1921, Ibirapuera, 04.501-002, na cidade de São Paulo, estado de São Paulo.

CONVOCAÇÃO  E  PRESENÇA:  Dispensada  a  convocação,  nos  termos  do  art.  16,  §4º  do
Estatuto Social da Companhia, tendo em vista a presença da totalidade dos membros do
Conselho de Administração, conforme lista de presença ao final da presente ata.

MESA: Presidente: Flávio Ernesto Zarzur; e Secretário: Roberto Mounir Maalouli.

ORDEM DO DIA: (i) tomar ciência sobre o reporte trimestral das atividades realizadas pelo
Comitê  de  Auditoria  da  Companhia;  (ii) deliberar  sobre  a  aprovação  do  Relatório  da
Administração,  das  Informações  Financeiras  Trimestrais  e  do  relatório  dos  auditores
independentes, referentes ao período de três meses compreendido entre 1º de janeiro e 31
de março de 2026; e (iii) deliberar sobre a declaração de dividendos intermediários, com
base no saldo da reserva de lucros estatutária denominada “Reserva de Expansão”, indicado
nas  Informações  Financeiras  Trimestrais  da  Companhia  na  data-base  de 31  de  março  de
2026.

DELIBERAÇÕES: Instalada a reunião, foi realizado o reporte das atividades do Comi
```

### 2. 07/05/2026 — Comunicado ao Mercado - Comunicado de Lançamento GranResort Reserva São Caetano - 1ª Fase

URL: https://api.mziq.com/mzfilemanager/v2/d/653fada3-cbcd-4015-9a94-2149f610a321/5099e0cc-d7ce-94ec-bfe3-87ef231faf6c?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
Lançamento

1ª Fase: Torres Bonaire e Curaçao

VGV %Eztec: R$ 457 milhões

Padrão: Médio

%Eztec: 100%

Região: São Caetano

Unidades: 497

Área Privativa: 43.332 m²

A Eztec apresenta seu mais novo lançamento, o
GrandResort Reserva São Caetano. Com
unidades de 68 m² a 134 m² e arquitetura
assinada pelo MCAA Arquitetos, o projeto é o
terceiro lançamento do complexo Reserva São
Caetano e oferece diversas experiências de lazer,
como piscina de 50 metros, parque aquático
infantil, quadras de tênis e areia, áreas wellness,
salões de festas, espaços gourmet e diversas
opções de entretenimento para toda a família. Em
um endereço privilegiado, o Grand Reserva esta
localizado à poucos minutos do ParkShopping
São Caetano e do Parque Chico Mendes, unindo
conforto, conveniência e qualidade de vida em
uma proposta única de moradia.

.

Perspectiva ilustrada da Fachada

Perspectiva ilustrada da Piscina

Perspectiva ilustrada do Family Space

Com 47 anos de história, a Eztec é uma das empresas com maior lucratividade entre as empresas de capital aberto
do setor de incorporação e construção no Brasil. Com seu modelo de negócio totalmente integrado, a Companhia
já lançou 198 empreendimentos, totalizando mais de 5,8 milhões de metros quadrados de área construída e em
construção e 48.503 unidades.

A Eztec S.A. integra o Novo Mercado da B3 e é negociada com o código EZTC3.

Para mais informações adicionais,
favor entrar em contato:

Relações com Investidores - Eztec S.A.
(11) 5056-8313 | ri@ez
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-05-07** matched `dividend` → Dividend declaration: _Conselho de Administração - Ata (Reporte trimestral de atividades do CA; Aprovaç_
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.10949001, DY=0.08296378492327612 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
