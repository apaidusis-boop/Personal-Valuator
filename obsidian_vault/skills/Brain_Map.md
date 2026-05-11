---
type: integration_master
version: v1.0
audience: external_ai (Claude Design, design partners, future Claude Code sessions)
owner: helena_linha + founder
created: 2026-04-27
last_updated: 2026-04-27
purpose: feed an external AI everything it needs to redesign Investment Intelligence end-to-end, in one document.
tags: [brain_map, integration, claude_design, design, master, helena]
---

# 🧠 Mapa do Cérebro — Investment Intelligence

> **Para qualquer AI externa que abrir este ficheiro pela primeira vez:** lê este mapa inteiro antes de propor qualquer coisa visual. Foi destilado de ~600 ficheiros do projecto especificamente para te dar contexto suficiente para ofereceres design *coerente com a casa*, não design genérico.
>
> O objectivo não é repetir o que já existe. O objectivo é que entendas **quem somos, o que construímos, e que aspecto isso quer ter** — e depois proponhas uma solução que respeite o conjunto.
>
> Se preferires leitura curta antes da profunda: §1 + §3 + §8 + §11 (≈10 min). O resto é para iteração.

---

## 0 — Índice

- §1 [Quem está do outro lado](#1--quem-está-do-outro-lado-founder)
- §2 [O que é o produto](#2--o-que-é-o-produto)
- §3 [Os 6 não-negociáveis](#3--os-6-não-negociáveis-constitutional-rules)
- §4 [Arquitectura: 3-layer brain](#4--arquitectura--3-layer-brain)
- §5 [Surfaces e seu papel](#5--surfaces-e-seu-papel)
- §6 [Estado do projecto: phases history em 30 segundos](#6--estado-do-projecto-phases-history-em-30-segundos)
- §7 [Open issues que intersectam design](#7--open-issues-que-intersectam-design)
- §8 [Design system v2.0 — a constituição visual](#8--design-system-v20--a-constituição-visual)
- §9 [Componentes e implementação actual](#9--componentes-e-implementação-actual)
- §10 [Páginas que existem (e o que precisam virar)](#10--páginas-que-existem-e-o-que-precisam-virar)
- §11 [North Star — o que "bom design" significa aqui](#11--north-star--o-que-bom-design-significa-aqui)
- §12 [Briefs concretos para sessões de Claude Design](#12--briefs-concretos-para-sessões-de-claude-design)
- §13 [Reading map para AI: o que ler quando](#13--reading-map-para-ai-o-que-ler-quando)
- §14 [Glossário do projecto](#14--glossário-do-projecto)
- §15 [Cross-links (master index)](#15--cross-links-master-index)

---

## 1 — Quem está do outro lado (founder)

**Não é uma fintech. É uma pessoa real, sozinha, a gerir o seu próprio dinheiro.**

| Dimensão | Realidade |
|---|---|
| Profissão | Profissional liberal, **vibe-coder** (programa por interesse, não a tempo inteiro) |
| Línguas | PT-BR + PT-PT fluentes; inglês operacional. Prefere UI em PT. |
| Hábitos de leitura | Suno Notícias, JPM Research, WSJ, livros (Damodaran, Dalio). |
| Filosofia financeira | **DRIP + Buffett + Graham** — qualidade > velocidade, dividendos consistentes, horizonte de anos. |
| Mercados | 🇧🇷 B3 (12 holdings BR) + 🇺🇸 NYSE/NASDAQ (21 holdings US). |
| Estilo de uso | Lê de noite, com café. Sessões longas e contemplativas. **Não é day-trader**. |
| Estilo cognitivo | Decide com **clareza visual + contexto**, não com 50 botões. Aprecia profundidade narrativa. |
| Aversões | Dashboards SaaS gringos, decoração gratuita, condescendência ("zero tokens Claude" como caption). |

**Implicação para design**: a UI tem que **espelhar como ele pensa sobre os investimentos** (longo prazo, contemplativo, narrativo), não estar em conflito com isso. O modelo mental certo é "**leitor de carta privada de banco**", não "**operador de Bloomberg Terminal**".

A Helena Linha (Head of Design) já validou esta direcção em `proto_home_v1_c.html` (Hara/MUJI). Está aprovada.

---

## 2 — O que é o produto

Sistema **pessoal** de inteligência de investimento. **Single-user**, local-first, zero stakeholders externos.

### Cobertura quantitativa actual

| Dimensão | Estado |
|---|---:|
| Holdings totais | 33 (12 BR + 21 US) |
| Universe seguido | 184 tickers |
| Dossiers wiki | 184 ticker notes + 53 conceptual notes |
| Quarterly history (CVM oficial) | ~532 rows BR (7 anos) + 50 bank-specific rows |
| Books ingeridos (PDF → chunks → methods) | 4 (Damodaran + 3 Dalio) → 1.152 methods extraídos |
| Library RAG chunks | 1.704 (nomic-embed local) |
| Paper signals acumulados | ~1.334 (zero capital real envolvido) |
| Perpetuums autónomos | 12 activos (T1-T2) |
| Agents framework | 12 personas com clearance matrix |
| Tokens Claude pipeline | **~0** (Ollama Qwen 14B local faz tudo) |

### Capacidades principais (em uma frase cada)

- **Fetchers** — yfinance (BR + US), brapi, SEC EDGAR, FRED, BACEN IF.Data, Tavily web research, Massive.com (Polygon rebrand, recém-integrado).
- **Scoring** — engine único com critérios por mercado (Graham clássico BR não-financeiras, banco-specific BR, Buffett US, banco US ROTCE-based, REIT-aware FFO).
- **Analytics** — backtests yield + regime, regime classifier macro BR/US, quant smoke (vectorbt + pyfolio).
- **Library** — 16 YAML methods canónicos + 1.152 auto-extraídos, RAG queryable em PT, matcher contra portfolio.
- **Perpetuums** — 12 daemons que *escrevem propostas* (T2) ou *agem* (T3-T5) sobre dados/vault — não são cron jobs cegos, são auto-correctors com track record.
- **Agents** — 12 personas com clearance matrix, mas o user é sempre L0 Founder (decisão final).
- **Frontend (cara)** — Streamlit dashboard 9+ pages. **Esta é a parte com mais débito visual** — a razão principal deste exercício.
- **Frontend (cérebro)** — Obsidian vault 200+ notas, Dataview queries, Charts plugins.
- **Frontend (chefe)** — CLI `ii` 50+ comandos.
- **Notifiers** — Telegram bot @TheJarbas123_bot diário.

### O que **não é**:

❌ SaaS multi-tenant. ❌ Trading platform. ❌ Robo-advisor. ❌ Para venda. ❌ Para escala. ❌ "MVP". ❌ "Production-grade" no sentido enterprise — é production-grade no sentido *o user usa todos os dias*.

---

## 3 — Os 6 não-negociáveis (constitutional rules)

Estas são leis da casa. Qualquer proposta de design que viole uma delas **é descartada antes de discussão**.

1. **In-house first** — Tudo que rode localmente (SQL, Ollama, scripts) NÃO usa tokens Claude. Claude API é último recurso, não primeiro. *Implicação para design*: nada de "simplificar" propondo um chat-with-AI omnipresente que requer chamadas externas constantes.

2. **Carteiras isoladas** — Dinheiro USD fica em US, BRL em BR. **Nunca** sugerir conversão entre contas, nunca apresentar como pool único sem rótulo claro de moeda. *Implicação para design*: separação visual clara BR vs US em qualquer surface multi-mercado.

3. **Paper-trade antes de real capital** — Qualquer signal novo entra em `paper_trade_signals`. Real capital só após 30+ closed signals com win_rate >60%. *Implicação para design*: paper signals são **um cidadão visual de primeira classe**, não pop-up secundário.

4. **Honest projections** — Em forward scenarios, evitar assumptions optimistas. Aplicar damper quando histórico >> Gordon. *Implicação para design*: nunca mostrar "projected 2030 value" sem mostrar o intervalo conservador ao lado.

5. **Tier-gated autonomy** — Perpetuums escalam T1→T2→T3→T4→T5 com base em estabilidade comprovada. *Implicação para design*: toda Actions Queue mostra `proposed_by · tier · why`. Tier visível é não-negociável.

6. **Tickers blacklist persistente** — TEN: 4 sinais cycle peak Apr 2026 → NUNCA mostrar como "consider adding". GREK: dividendos irregulares → NÃO aplicar lógica DRIP/scorecard. *Implicação para design*: as tabelas têm que respeitar excepções por ticker, não tratar tudo uniformemente.

**Princípio meta** (2026-04-26): **"Engenheiros não escolhem cores."** Toda nova UI passa por `_components.py`. `Tone Literal` (Python typing) torna paletas fora-dos-tokens **impossíveis em compile-time**.

---

## 4 — Arquitectura: 3-layer brain

Decisão arquitectural canónica de 2026-04-26 (Phase U.0). O cérebro do sistema vive em **três camadas** com responsabilidades disjuntas:

```
┌─────────────────────────────────────────────────────────────┐
│ L1 — VERDADE                                                │
│   SQLite (data/br_investments.db, data/us_investments.db)   │
│   YAML (config/universe.yaml, library/ri/catalog.yaml)      │
│   Scripts read/write. O humano não toca.                    │
└─────────────────────────────────────────────────────────────┘
                            ↑
                   (regenerable, frontmatter tipado)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L2 — PROJECÇÃO                                              │
│   Vault auto-gerada (obsidian_vault/tickers/*_RI.md,        │
│   briefings/, dashboards/, sectors/)                        │
│   Scripts geram. Marcadores `_LAYER.md` em cada folder.     │
└─────────────────────────────────────────────────────────────┘
                            ↑
                  (humano escreve aqui — sagrado)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ L3 — NARRATIVA                                              │
│   Vault humano-escrita (wiki/, CONSTITUTION.md, teses,      │
│   decision logs, journals)                                  │
│   Scripts NÃO sobrescrevem. Backup git é o único guard.     │
└─────────────────────────────────────────────────────────────┘
```

Esta separação é **fundamental para design** porque cada camada quer um tratamento visual diferente:

- **L1 dados** ⇒ tabelas densas, mono, alinhamento tabular, mínimo cosmético.
- **L2 projecções** ⇒ documentos editoriais, lede sentence, charts integrados.
- **L3 narrativa** ⇒ markdown puro, tipografia serif, leitura longa.

Misturar os tratamentos (e.g. tabela L1 com dressing editorial L2) gera cognitive dissonance — é exactamente o "HTML bobo" que estamos a tentar deixar para trás.

---

## 5 — Surfaces e seu papel

**Princípio das superfícies** (decisão 2026-04-26): cada surface optimiza para o seu uso. Nunca tentar que uma surface faça o trabalho da outra.

| Surface | Papel | Optimiza para | Exemplo de coisa que NÃO faz |
|---|---|---|---|
| **CLI `ii`** | Sala do chefe | Velocidade, raw output, scriptabilidade. Sem cerimónia. | Não tem branding, paleta, charts. |
| **Streamlit** | Cara | Interactividade (filtros, drill-downs), visualização rica de L1. | Não é onde se *lê* longamente — é onde se *explora*. |
| **Obsidian** | Cérebro | Leitura profunda, escrita, knowledge graph (L1+L2+L3). | Não é interactivo (não há filtros server-side). |
| **HTML reports** | Deliverables | Quarterly briefings, weekly. Output one-shot, partilhável. | Não é onde se *trabalha* — é o que sai. |
| **Telegram (Jarbas)** | Push canal | Push diário matinal (~1160 chars), notificações de eventos. | Não é onde se *consulta* — é onde se é *avisado*. |

**Implicação dura**: Claude Design *não* deve propor unificar tudo numa única surface. Não há um "super-dashboard que faz tudo". O modelo mental certo é **"4 surfaces complementares, cada uma com excelência no seu lane"**.

O foco actual desta Phase U é o **Streamlit** (cara). É o elo mais fraco hoje.

---

## 6 — Estado do projecto: phases history em 30 segundos

Para AI externa: o sistema foi construído em phases nomeadas (W → U). O que importa é o estado actual, não a história, mas eis o destilado:

| Phase | Em uma linha | Status |
|---|---|---|
| **W** | Skills arsenal — 33 skills externas avaliadas, 7 Tier-S priorizadas. | ✅ |
| **X** | Perpetuum engine — 12 daemons autónomos com tier-gated autonomy T1-T5. | ✅ |
| **Y / Y.8** | RI Knowledge Base — pipeline directo CVM → DB normalizado, 5 stocks BR + 5 FIIs com 7 anos history. | ✅ |
| **Z** | UI friendly layer — Streamlit dashboard 9 pages (Captain's Log, Actions Queue, Perpetuum Health, Paper Signals, RI Timeline, etc.). | ✅ |
| **Z.8 Helena s1-s4** | Helena Linha hired (Head of Design). Design System v1.0 + plotly `ii_dark` + `_components.py` com `Tone Literal` compile-time guard. | ✅ |
| **AA** | Critical Thinking Stack — Synthetic IC (5 personas debate), Variant Perception, Earnings Prep, Portfolio Stress, Decision Journal. | ✅ |
| **F → I** | T0 cleanup + thesis backfill 100% (33/33 holdings) + Telegram brief + wiki holdings closeout. | ✅ |
| **J** | Universe-wide thesis (184/184) + bank balance sheet schema + conviction score expanded. | ✅ |
| **K / K.2 / K.3** | Tavily wired (autoresearch + 3-wire) + 8 Tavily skills + CLI. | ✅ |
| **L** | BACEN IF.Data fetcher + W.11 Quant stack (vectorbt/pyfolio) + Synthetic IC universe-wide. | ✅ |
| **U.0** | Unification sweep — 3-layer brain formalised, root cleanup, React desktop deprecated, helena.css snippet. | ✅ |
| **U.1** | Home minimalista (Apple Newsroom-style). Direcção aprovada (proto_home_v1_c.html — Hara/MUJI). | 🔄 implementação pendente |
| **U.2 → U.7** | Streamlit consolidation, Ask box, Action loop, Charts identidade, Telegram visual card, Obsidian cérebro. | ⏳ pending |

**O que isto significa para Claude Design**: o backend está sólido. O problema é puramente *experiencial*. Não há features para inventar — há **expressão visual** para encontrar.

---

## 7 — Open issues que intersectam design

Da Constitution, filtrado para o que importa visualmente:

1. **Frontend Streamlit ainda não casou com v2.0 editorial** — Helena Mega audit ainda regista 12 violações (5 hex literals fora dos tokens, 5 plotly templates crus, 2 captions >8 palavras). É o "HTML bobo" que o user quer eliminar.
2. **Pages redundantes em Streamlit** — 9 pages, várias com sobreposição (e.g. Captain's Log + Home + Actions Queue mostram conteúdo similar). Phase U.2 quer consolidar para ≤5 com nav plana.
3. **Mobile sem tratamento** — Streamlit responsive default é fraco. Phase U.2 quer breakpoints reais.
4. **Charts inconsistentes** — alguns ainda em `plotly_dark` cru, outros em `ii_dark`, alguns com paletas inventadas.
5. **Telegram push é texto** — Phase U.6 quer matplotlib (Helena tokens) → PNG card diário visual.

**O que NÃO é problema**:
- ✅ Backend (perpetuums, fetchers, scoring) está estável.
- ✅ Data quality (após XPML11 cleanup) está boa.
- ✅ Token economy (Ollama-first) está respeitada.
- ✅ Vault (cérebro) está bem organizado em 3-layer.

---

## 8 — Design system v2.0 — a constituição visual

**Direcção aprovada pelo founder em 2026-04-26 a partir de `proto_home_v1_c.html`.**

Filosofia: **Kenya Hara / MUJI / Editorial Banking**. **NÃO É DASHBOARD. É um documento.**

### Princípios não-negociáveis (v2.0)

1. **Voz humana sobre label/value.** A página abre com uma *lede sentence* completa, não com stat bar.
2. **Cream warm `#f4eee5`** é a tradição visual de relatórios financeiros impressos (Itaú PB, Pictet, Suno em alguns documentos). Não é "fashion choice".
3. **Source Serif 4** para títulos e body. **Mono SÓ em números**, em tamanho menor que o texto.
4. **1 accent terracotta `#b85c38`** usado com extrema disciplina (3 sítios por página máximo).
5. **Voz PT-BR completa**: "Início" não "Home", "Pergunta" não "Ask", "Frente ao IBOV" não "vs IBOV", "Cinco anos" não "5y".
6. **Datas formato pt-BR** (`02·04·2026` ou `02 de abril`).
7. **Espaço respira.** Margens generosas, vertical rhythm 48px+ entre secções.

### Paleta — 11 tokens

| Token | Hex | Uso |
|---|---|---|
| `paper` | `#f4eee5` | Background. Cream warm. |
| `paper-2` | `#ede5d8` | Alt bg (subtle alternation). |
| `ink` | `#2a2622` | Text default. Charcoal warm. |
| `ink-2` | `#4a423a` | Text secondary. |
| `muted` | `#786f64` | Labels, captions, metadata. |
| `rule` | `#d8d0c4` | Border principal. |
| `rule-soft` | `#e7e0d2` | Border subtil. |
| `clay` | `#b85c38` | **O accent.** Terracotta. Highlight 1 elemento por página. |
| `pos` | `#527a45` | Ganhos. Sage green (não verde-fluorescente). |
| `neg` | `#a0473d` | Perdas. Clay-red (consistente com accent family). |
| `warn` | `#a8763d` | Atenção. Amber-clay. |

**Mudança vs v1.0**: dark theme abandonado. Paleta agora é warm/cream para alinhar com tradição editorial financeira.

### Tipografia — 3 famílias com role explícito

| Família | Role | Onde |
|---|---|---|
| **Source Serif 4** | Títulos, body, lede, ticker names | Headlines (italic 700, optical-size 60), body (400, opsz 30), nav active (italic) |
| **Inter** | UI micro-labels, eyebrows | UPPERCASE 9-11px tracked .2em, table headers, captions |
| **IBM Plex Mono** | Números (apenas) | 13-14px (menor que body 15px), tabular-nums forced |

**Regra dura**: mono nunca domina. Os números *servem* o texto, não vice-versa.

### Spacing scale

- Vertical rhythm: **48px+** entre secções principais
- Inter-section: **32px**
- Within section: **18-24px**
- Margens main: **56-80px** horizontal (generosas)

### Chart conventions (v2.0)

- Background = `paper` (não brancos puros, não dark).
- Lines: 0.5-1.1px (thin, ink-line).
- 1 line highlighted em `clay`, restantes em `ink` muted (opacity 0.4).
- IBOV/index: dotted 0.5px em `muted`, opacity 0.5.
- Single horizontal grid line em base 100, `rule` width 0.6.
- Year markers: serif italic 11px, `muted`.
- Labels inline no fim das linhas (Tufte convention).

### Anti-padrões — proibidos (8)

1. ❌ Hero number gigante (sem 56px+ de números soltos).
2. ❌ Cards com `border-left: 2px accent`.
3. ❌ Emojis como hierarquia (em headings, captions, page titles).
4. ❌ Mistura de idiomas em UI strings.
5. ❌ Mono dominante em texto não-numérico.
6. ❌ Mais de 1 accent por página.
7. ❌ Voz de UI engineer ("Open Actions", "Last update", "zero tokens Claude").
8. ❌ Cores fora dos 11 tokens (qualquer hex inventado).

### Heurística geral

Se um componente novo precisa de uma cor que não está nos tokens, é a **estrutura** que está errada, não a paleta. Refactor primeiro.

> Para Claude Design: respeitar estes 7 princípios + 11 tokens + 3 fontes + 8 anti-padrões é a **condição mínima** para qualquer proposta sair daqui sem ser refeita. Não há "interpretação criativa" desta paleta.

---

## 9 — Componentes e implementação actual

### Componentes Helena (`scripts/_components.py`)

| Componente | Função | Status v2.0 |
|---|---|---|
| `kpi_tile(label, value, delta, footnote, tone)` | Card métrico com left-accent | ⚠️ v1.0 — refactor pendente para editorial |
| `status_pill(text, tone)` | Badge inline (positive/negative/warning/neutral) | ⚠️ v1.0 — clay/sage/amber |
| `section_header(title, caption)` | H2 + caption opcional | ⚠️ v1.0 — passar a serif italic |
| `agent_attribution(agent, tier, why)` | Footer "by Helena · T2 · because Y" | ✅ comportamento mantido |
| `divider(label)` | Separador horizontal | ⚠️ refactor para `rule` token |
| `story_card()` | Card narrativo (Captain's Log) | ⚠️ v1.0 — refactor para editorial |
| `verdict_pill()` | BUY/HOLD/AVOID rendering | ⚠️ v1.0 — refactor para clay/sage |

**Nota**: `_components.py` é o **único** sítio onde HTML/CSS de page existe. Pages em `scripts/dashboard_app.py` chamam helpers, não inline.

### Theme (`scripts/_theme.py`)

- Plotly template `ii_dark` (deprecated com v2.0 — ainda em uso até refactor).
- Editorial template ainda não escrito (esperado em `scripts/_editorial.py`).

### Vault CSS (`obsidian_vault/.obsidian/snippets/helena.css`)

Espelha tokens v1.0. **Refactor para v2.0 é gap conhecido**.

### Implicação para Claude Design

Quando propões uma page nova, pensa em **helpers reusáveis**, não em CSS inline. O output ideal é:
1. HTML standalone (para canvas review).
2. Lista dos helpers que precisam existir/ser refactored para a page funcionar.
3. Tokens novos *justificados* se precisar (mas a régua é: refactor estrutura primeiro, token novo depois).

---

## 10 — Páginas que existem (e o que precisam virar)

Estado actual do `scripts/dashboard_app.py` — 9 pages, em ordem da nav:

| # | Page actual | Função | Problema design | Direcção v2.0 |
|---|---|---|---|---|
| 1 | **Captain's Log** | Story cards: synthetic IC + variant + conviction + RI material changes + perpetuum alerts | Cards demasiado uniformes, sem hierarquia editorial | **Documento de manhã**. Lede sentence + 3-4 secções narrativas. Conviction como pull-quote. |
| 2 | **Home / Portfolio** | KPIs + holdings table + alocação | Stat bar dominante, dashboard-y | **Início** (PT-BR). Lede sentence ("A carteira encerra a semana em..."). Sidebar de carteiras + chart 5y + holdings table denso mas elegante. |
| 3 | **Actions Queue** | T2 perpetuum proposals para 1-click approve | Lista plana sem priorização visual | **Decisões pendentes**. Each action como mini-card editorial com `proposed_by · tier · why`. |
| 4 | **Perpetuum Health** | 12 daemons + scores + trends | Tabela sem narrativa | **Saúde dos automatismos**. Health summary + drill-down por perpetuum. |
| 5 | **Paper Signals** | 1.334 signals abertos + filtros | Densidade alta, mas sem hierarquia | **Sinais experimentais**. Group by convergence (3+ methods agree on same ticker). |
| 6 | **RI Timeline** | Quarterly history (CVM) + 4 plotly charts por ticker | Charts em template antigo | **Relatórios trimestrais**. Editorial: timeline serif + charts em paleta clay. |
| 7 | **Ask Library** | RAG via subprocess + history | UX de busca crua | **Pergunta**. Big text input + answer rendered as document, sources expandíveis. |
| 8 | **Screener** | Filter universe by criteria | Form + tabela | **Triagem**. Form editorial + result count em lede ("87 dos 184 passam"). |
| 9 | **YouTube** | 21 videos ingeridos + insights | Cards demasiado tile-y | **Vídeos**. Lista editorial + extract preview. |

**Phase U.2 pede consolidação para ≤5 nav**. Sugestão (não validada com user):
1. **Início** (Home + Captain's Log fundidos).
2. **Decisões** (Actions Queue + Paper Signals + Screener fundidos).
3. **Empresas** (RI Timeline + ticker pages + earnings prep).
4. **Pergunta** (Ask Library + YouTube + Bibliotheca search fundidos).
5. **Saúde** (Perpetuum Health + system status).

> Para Claude Design: esta consolidação é onde tu podes ajudar mais. Propor a IA a estrutura editorial das 5 e como secções colapsam dentro de cada uma sem perder funcionalidade.

---

## 11 — North Star — o que "bom design" significa aqui

Se tudo o que ficou acima cair, esta secção é a única que tens que respeitar.

### A imagem mental certa

> *"A página que mostro ao meu pai sem precisar de explicar."*

Não é Bloomberg. Não é Yahoo Finance. Não é Robinhood. Não é Notion. **É uma carta de banco privado, escrita à mão, em papel cremoso, que abro em silêncio com o café da manhã.**

### Os 5 testes para qualquer proposta visual

1. **Teste do pai**: alguém não-técnico abre a page. Em 10 segundos, percebe o que está a olhar?
2. **Teste do café**: o user lê de manhã, com café, em 5 minutos. Sai com clareza ou com mais ansiedade?
3. **Teste da identidade**: se eu apagasse o logo, ainda saberias que é deste produto? Ou parece um SaaS template B2B?
4. **Teste da paleta**: contaste cores? Mais que 3 numa página? Refactor.
5. **Teste do "porquê"**: cada elemento responde a uma pergunta que o user faria? Ou é decoração?

### Princípios de movimento

- **Lede sentence > stat bar.** Texto humano completo *antes* de números.
- **Whitespace é informação.** Não é desperdício; é semântica. Diz "isto agrupa, aquilo separa".
- **Mono serve o texto.** Os números são parágrafos com data, não headlines.
- **1 accent por página.** Clay terracotta marca o que importa hoje. O resto é ink.
- **Voz portuguesa autêntica.** "Frente ao IBOV", não "vs IBOV". "Cinco anos", não "5y".
- **Densidade quando justificada.** Tabelas densas são OK *se* a hierarquia tipográfica está respeitada e o user pode scan vertical.

### O que isto NÃO é

❌ Não é "modo simples" para principiantes — o user é sofisticado.
❌ Não é "minimalismo Apple" — é editorial banking, que tem mais texto e mais densidade que Apple Newsroom.
❌ Não é "skin design system" — não é mudar cor de botão; é mudar a *natureza do produto*.

---

## 12 — Briefs concretos para sessões de Claude Design

Para AI externa: cada um destes é um brief prontos-a-usar. Em sessão Claude Design:
1. Cola o `Brain_Map.md` inteiro (este ficheiro) como contexto inicial.
2. Cola o `Design_System_v2.md` para reforço dos tokens.
3. Cola **um** dos briefs abaixo.
4. Itera no canvas.
5. Export → `obsidian_vault/_assets/proto_<page>_v<n>_<variant>.html`.

### Brief A — Início (Home redesign integrado)

> Brief individual em [[Brief_Home_U1]]. TL;DR: redesenhar a Home/Início para Phase U.1 — fundir com Captain's Log, lede sentence + sidebar carteiras + chart 5y BR/US/IBOV + holdings table + decisões pendentes inline. Referência aprovada: `proto_home_v1_c.html`.

### Brief B — Empresa (página de ticker editorial)

> Cada um dos 184 tickers tem uma `tickers/<TICKER>_DOSSIE.md`. Hoje é Streamlit page com KPIs + chart + thesis + RI timeline + Synthetic IC quotes + paper signals. Refactor para layout estilo "FT/WSJ company profile": serif title, deck (sub-headline), pull-quotes da Synthetic IC, RI quarterly como timeline editorial, chart 5y em clay-ink. Anti-pattern: tile-grid de KPIs.

### Brief C — Decisões (Actions Queue + Paper Signals fundido)

> Hoje são 2 pages separadas. Actions Queue tem ~18 propostas T2 abertas (ex: "Reforçar BBDC4 — proposed by perpetuum.thesis · T2 · because conviction 92"). Paper Signals tem 1.334 sinais experimentais (ex: "BUY ITSA4 via Graham defensive @ R$11.20"). Refactor para uma Page única "Decisões pendentes" com hierarquia: (1) Decisões com peso real (T2 actions com convergência ≥3 methods) no topo, (2) Sinais experimentais agrupados por convergência abaixo, (3) Histórico fechado em accordion. Cada decision card mostra `proposed_by · tier · why` (3 momentos de transparência).

### Brief D — Pergunta (Ask Library editorial)

> Hoje é text input + subprocess RAG + answer dump. Refactor para "Pergunta ao acervo" — input grande estilo Google search 2005, mas com tipografia serif italic. Answer rendered como **documento** (não chat bubble) com sources expandíveis no fim, marcadas em superscript estilo academic. RAG queries cross-book em PT — preserva esta capacidade (não é só placeholder).

### Brief E — Telegram visual card (Phase U.6)

> Hoje Telegram push é texto markdown ~1160 chars (briefing). Refactor para **PNG card** gerado por matplotlib usando Helena tokens — cream background, serif title, números em mono, 1 chart sparkline 5y, lede sentence. Não pode exceder ~1200×900px (Telegram preview). Output: `reports/telegram/<date>.png`.

---

## 13 — Reading map para AI: o que ler quando

Por ordem de prioridade, *além* deste mapa:

### Para entender o tom (5 min)
- `obsidian_vault/CONSTITUTION.md` — secção "🚪 Voltamos" (topo)
- Este Brain_Map §1 + §11

### Para entender o design existente (15 min)
- `obsidian_vault/skills/Design_System_v2.md` — paleta + tipografia + anti-padrões
- `obsidian_vault/_assets/proto_home_v1_c.html` — protótipo aprovado (abrir em browser)
- `obsidian_vault/_assets/proto_home_v1_INDEX.md` — porque é que C ganhou vs A e B

### Para entender a arquitectura (30 min)
- `CLAUDE.md` — script catalog + critérios BR/US
- `obsidian_vault/CONSTITUTION.md` — phases history + decision log + open issues
- Este Brain_Map §4 + §5 + §6

### Para entender os perpetuums (15 min)
- `obsidian_vault/skills/Phase_X_Perpetuum_Engine.md`
- `obsidian_vault/agents/_information_levels.md` — clearance matrix

### Para entender Helena (10 min)
- `obsidian_vault/agents/personas/Helena Linha.md`
- `obsidian_vault/skills/Helena_Mega/00_MASTER.md`

### Para entender o que NÃO fazer (5 min)
- Este Brain_Map §3 (não-negociáveis) + §8 (anti-padrões) + §11 (testes)

### Se o user pede "tudo"
- Repo público: `https://github.com/apaidusis-boop/Personal-Valuator`
- Sub-paths recomendados (per `Claude_Design_Integration.md`):
  - `tree/main/scripts` — implementação Streamlit
  - `tree/main/obsidian_vault/skills` — design docs
  - `tree/main/obsidian_vault/.obsidian/snippets` — vault CSS

> **Importante**: nunca apontar Claude Design ao monorepo inteiro (`tree/main`). Lag e dilui contexto.

---

## 14 — Glossário do projecto

| Termo | Significado |
|---|---|
| **DRIP** | Dividend Reinvestment Plan — reinvestir dividendos em mais shares. |
| **Perpetuum** | Daemon autónomo que detecta/propõe/age sobre o sistema. T1=observer, T5=fully autonomous. |
| **T1-T5** | Tier de autonomia. T1=detecta+alerta. T2=propõe action para 1-click approve. T3=actua em sandbox. T4=produção com hard limits. T5=livre. |
| **Library method** | YAML em `library/methods/` com critério reusável (ex: Graham defensive). 16 canónicos + 1.152 auto-extraídos de livros. |
| **Paper signal** | Trade hipotético em `paper_trade_signals` table. Validação antes de capital real. |
| **L0 Founder** | O user. Decisão final sempre. Nenhum agent sobrepõe. |
| **L1/L2/L3** | 3-layer brain (verdade SQLite / projecção vault auto / narrativa vault humano). |
| **Helena Linha** | Persona Head of Design. Ownera Design System v2.0. |
| **Captain's Log** | Streamlit page primeira da nav — synthetic IC + variant + conviction + alerts. |
| **Synthetic IC** | 5 personas (Buffett+Druckenmiller+Taleb+Klarman+Dalio) debatem cada holding via Ollama Qwen 14B. |
| **Variant Perception** | "We vs analyst consensus" — onde a thesis nossa difere do consenso publicado. |
| **Conviction score** | 0-100 composite de fundamentals + thesis health + paper signals + variant. |
| **RI** | Relações com Investidores — pipeline CVM oficial → quarterly_history. |
| **Bibliotheca** | Sub-vault de clippings (Suno/XP/WSJ/JPM) + glossary + knowledge cards + research digest. |
| **K&A** | Kings & Aristocrats — 87 US tickers com dividend streak ≥10 anos. |
| **Helena Mega** | `agents/helena_mega.py` pipeline audit+curate+spike+report. |
| **proto_home_v1_c** | Protótipo Hara/MUJI aprovado pelo founder em 2026-04-26. Base de v2.0. |
| **HTML bobo** | Termo do user para o Streamlit actual que ainda não casou com v2.0 editorial. |

---

## 15 — Cross-links (master index)

### Documentos fundadores
- [[CONSTITUTION]] — master document vivo, ler primeiro ao voltar do projecto
- [[../../CLAUDE.md|CLAUDE.md]] — contrato projecto + script catalog
- [[Design_System_v2]] — constituição visual aprovada
- [[Design_System|Design_System v1.0 (deprecated)]] — referência histórica

### Design history
- [[../_assets/proto_home_v1_INDEX|3 protótipos: Tufte/Vignelli/Hara]] — porque escolhemos C
- [[../_assets/proto_home_v1_c|Protótipo aprovado (HTML)]]
- [[Helena_Mega/00_MASTER|Helena Mega master report]]
- [[Helena_Mega/01_Audit|Audit lint DS001-DS009]]
- [[Helena_Mega/02_Curation|Skills triados]]
- [[Helena_Mega/03_Spikes|4 paths de plataforma — A/B/C/D]]

### Personas e processos
- [[../agents/personas/Helena Linha|Helena Linha (Head of Design)]]
- [[../agents/_information_levels|Clearance matrix dos 12 agents]]
- [[Claude_Design_Integration|Workflow Claude Design]]
- [[Design_Watch|Design research scout (weekly)]]

### Roadmap activo
- [[Roadmap|Phase W roadmap mestre]]
- [[Phase_X_Perpetuum_Engine|Perpetuum architecture]]
- [[Phase_Y_Roadmap|RI Knowledge Base]]
- [[Brief_Home_U1|Brief U.1 — Home minimalista]]

### Wiki conceptual (53 notes)
- [[../wiki/Index|Wiki Index]] — sectors + macro + methods + playbooks

---

## 🌙 Notas de manutenção deste mapa

- **Quem actualiza**: Helena Linha + founder. Ninguém mais.
- **Quando**: depois de cada Phase fechada que mude design system OU surfaces.
- **Como detectar drift**: se a Constitution mudar uma decisão que afecte design, este mapa fica stale. Audit manual mensal sugerido.
- **Versionamento**: sempre a versão mais recente em-line (não fazer v2, v3 — só editar).
- **Audiência**: Claude Design (primário), Claude Code (secundário, durante handoff), futuros founders/heads (terciário).

---

> *"Não há resposta única. A escolha define o produto."* — Helena Linha, sobre os 3 protótipos
>
> *"NÃO É DASHBOARD. É um documento."* — Design System v2.0
>
> *"A página que mostro ao meu pai sem precisar de explicar."* — North Star
