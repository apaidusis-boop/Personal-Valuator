# ITSA4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Holding
- **RI URLs scraped** (1):
  - https://ri.itausa.com.br/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=2485.0 · entry=7.79 · date=2026-05-07

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=13.5
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.17571 · DY=0.09273259259259259 · P/E=9.121621
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-14 | fato_relevante | cvm | Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea |
| 2026-03-25 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |
| 2026-03-17 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência - Resultados em F |
| 2026-03-16 | fato_relevante | cvm | Pagamento de Juros sobre capital próprio |
| 2026-02-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 0.1s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.itausa.com.br/ | ✅ | 0.1s | 16,468 |
- Filings extraídos do RI: **4**
- Eventos calendário: **5**
- Apresentações/releases: **5**
- Audio/video: **1**
- Headers detectados (structure): **34**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/05/2026 | Comunicado ao Mercado \| Itaúsa inte... |
| 14/04/2026 | Fato Relevante \| Ajustes Contábeis ... |
| 16/03/2026 | Fato Relevante \| Pagamento de Juros... |
| 13/02/2026 | Aviso aos Acionistas \| Pagamento da... |

### Próximos eventos (calendário RI)

| Data | Evento |
|---|---|
| 2026-05-11 | Divulgação de Resultados 1T26 |
| 2026-05-29 | Formulário de Referência 2026 |
| 2026-07-31 | Informe sobre o CBGC |
| 2026-08-10 | Divulgação de Resultados 2T26 |
| 2026-08-11 | Videoconferência de Resultados 1S26 |

### Apresentações / releases disponíveis (5 total, top 5)

- [Relato Integrado](https://ri.itausa.com.br/sobre-a-itausa/relato-integrado/)
- [Apresentações](https://ri.itausa.com.br/informacoes-financeiras/apresentacoes/)
- [Relatório da administração](https://api.mziq.com/mzfilemanager/v2/d/afd9200b-9b01-4d1c-bdd9-9b2c1e9b3b4d/617fc6ff-ee6c-c8ff-7290-afae3e396676?origin=2)
- [Demonstrações contábeis](https://api.mziq.com/mzfilemanager/v2/d/afd9200b-9b01-4d1c-bdd9-9b2c1e9b3b4d/33d70207-2e3e-abbe-f266-09ff99212fda?origin=2)
- [Relato Integrado – Old](https://ri.itausa.com.br/?page_id=700)

### Audio / Video disponível (markitdown pode ler)

- [Itaúsa Cast](https://api.mziq.com/mzfilemanager/v2/d/afd9200b-9b01-4d1c-bdd9-9b2c1e9b3b4d/e81c8931-e993-d9ff-f18b-a4bc354d446a?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 7 | 7 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 5 | + |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 05/05/2026 — Comunicado ao Mercado | Itaúsa inte...

URL: https://api.mziq.com/mzfilemanager/v2/d/afd9200b-9b01-4d1c-bdd9-9b2c1e9b3b4d/53152c25-63a3-2865-9dab-2e23bea550e9?origin=2
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
COMUNICADO AO MERCADO

ITAÚSA INTEGRA NOVAMENTE O ISE DA B3

ITAÚSA  S.A.  (B3:  ITSA3,  ITSA4)  comunica  aos  seus  acionistas  e  ao  mercado  em  geral  que  foi
selecionada, pela 19ª vez, para compor a carteira do Índice de Sustentabilidade Empresarial (“ISE”)
da B3 em sua edição 2025/2026.

O  ISE  reúne  empresas  com  os  melhores  desempenhos  em  dimensões  que  avaliam  a
sustentabilidade empresarial. A nova carteira reúne 69 companhias pertencentes a 38 setores.

A nossa participação no ISE reforça nosso compromisso com a busca constante pelas melhores
práticas de gestão e de sustentabilidade.

Apoiados  em  nossos  valores,  seguimos  avançando  com  disciplina,  visão  de  longo  prazo  e
responsabilidade,  fortalecendo  nosso  ecossistema  de  negócios,  apoiando  o  desenvolvimento  do
país e gerando valor sustentável para a sociedade, investidas e acionistas.

São Paulo (SP), 5 de maio de 2026.

ALFREDO EGYDIO SETUBAL
Diretor de Relações com Investidores


```

### 2. 13/02/2026 — Aviso aos Acionistas | Pagamento da...

URL: https://api.mziq.com/mzfilemanager/v2/d/afd9200b-9b01-4d1c-bdd9-9b2c1e9b3b4d/a0460087-9170-d4d7-4a78-fc44cb369e21?origin=2
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
AVISO AOS ACIONISTAS

PAGAMENTO DAS FRAÇÕES DE AÇÕES DECORRENTES DE BONIFICAÇÃO

ITAÚSA  S.A.  (“Companhia”)  (B3:  ITSA3,  ITSA4),  em  complemento  ao  Fato  Relevante
divulgado em 15.12.2025, comunica a seus acionistas que as frações de ações, resultantes
da  bonificação  aprovada  pelo  Conselho  de  Administração  em  reunião  realizada  naquela
data, foram agrupadas em números inteiros e vendidas na B3 S.A. – Brasil, Bolsa, Balcão
(“B3”), em leilão realizado em 12.02.2026.

Nesse  leilão,  foram  alienadas  308.119  ações  escriturais,  sem  valor  nominal,  sendo
líquidos  de
39.229 ordinárias  e  268.890  preferenciais,  apurando-se  os  valores
R$ 14,5675853631  para  cada  ação  ordinária  e  R$ 14,6575822169  para  cada  ação
preferencial.

Esses valores serão creditados aos acionistas em 25.02.2026, na proporção das frações
de ações de cada espécie a que fizeram jus na data-base de 18.12.2025, conforme segue:

a)

b)

para  os  acionistas  registrados  nos  livros  da  Companhia,  o  crédito  será  efetuado
diretamente pela Itaú Corretora de Valores S.A. na conta indicada pelo acionista; para
os acionistas com cadastro desatualizado, os valores serão mantidos à disposição na
Companhia; e,

para  os  demais  acionistas,  o  pagamento  será  efetuado  diretamente  à  B3,  que
repassará  os  valores  aos  acionistas  cadastrados  em  seus  registros,  por  intermédio
dos seus Agentes de Custódia.

São Paulo (SP), 13 de fevereiro de 2026.

ALFREDO EGYDIO SETUBAL
Diret
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 eventos críticos nos próximos 30 dias** — maior risco operacional/oportunidade
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- ⏰ **Earnings/release iminente**: 2026-05-11 — Divulgação de Resultados 1T26 (em ~1 dias). Re-scrape no dia + monitorizar Telegram.
- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=2485.0, entry=7.79. 2 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.17571, DY=0.09273259259259259 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
