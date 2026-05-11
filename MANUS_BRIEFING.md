# Mission Control — Briefing para Manus

> Briefing completo do projecto para geração de design draft da web app "Mission Control".
> Criado em 2026-05-06.

---

## 1. Contexto do utilizador e do projecto

Investidor pessoa física operando em dois mercados: **Brasil (B3)** e **EUA (NYSE/NASDAQ)**.
Estratégia de longo prazo **DRIP** (reinvestimento de dividendos) com filosofia **Buffett/Graham** — qualidade, margem de segurança, dividendos consistentes. ~30 posições activas entre os dois mercados.

O sistema chama-se **investment-intelligence** — um OS pessoal de análise, scoring, agentes autónomos e tomada de decisão. A **Mission Control** é o front-end web desse sistema: o lugar onde o utilizador vê tudo, toma decisões e interage com os agentes de IA.

---

## 2. Stack técnica actual

| Camada | Tecnologia |
|---|---|
| Front-end | Next.js (App Router) + TypeScript + Tailwind v4 |
| Base de dados | SQLite local lida directamente via `better-sqlite3` (sem API server) |
| Agente principal | Python + Qwen 2.5 32B local (Ollama) |
| Execução | `localhost:3000`, Windows 11, RTX 5090, sempre ligado |
| Dados de mercado | yfinance (sem auth) + SEC EDGAR + CVM (BR) |

> A app **nunca** envia dados para a cloud. É 100% local.

O `App.tsx` partilhado pelo utilizador (React + Wouter + ThemeProvider, Vite-based) é o **taste/scaffolding** que o Manus pode usar como ponto de partida. Não é necessário Next.js — qualquer React moderno serve.

---

## 3. Páginas existentes (20 rotas)

| Rota | Propósito |
|---|---|
| `/` | Home — dashboard principal |
| `/portfolio` | Todas as posições agrupadas por classe |
| `/tasks` | Fila de open actions dos agentes |
| `/allocation` | Proposta de alocação dos 5 engines |
| `/council` | Sumário do Conselho de Analistas sintético |
| `/council/[ticker]` | Dossier completo de um ticker no Council |
| `/ticker/[ticker]` | Página de ticker: preço, posição, fundamentals, verdict |
| `/strategy/[ticker]` | Detalhe dos 5 engines de estratégia |
| `/content` | Topic Watchlist (10 temas scored 0-100) |
| `/memory` | 3 tabs: Daily / Long-term / Chats activos |
| `/calendar` | Calendário de eventos (ex-dates dividendos, earnings) |
| `/team` | Org chart dos 14 agentes com status live/idle/alert |
| `/visual` | Visual Office pixel-art com os agentes |
| `/docs` | Documentação do sistema |
| `/projects` | Gestão de projects/sprints |

---

## 4. Design language — "Broadsheet" v3

### Filosofia

> **"Terminal = sala do chefe (acção, raw, sem cerimónia). Mission Control = escritório (consumível, polido)."**

Não é um SaaS de startups. É uma sala de operações de um gestor privado sério.
Referências visuais: **Financial Times**, **Wall Street Journal**, **The Economist**.
Inspiração de produto: densidade editorial, não gamification.

### Paleta — Light (FT Broadsheet)

| Token | Hex | Uso |
|---|---|---|
| `--bg-canvas` | `#FFF1E5` | Fundo principal — salmão icónico do FT |
| `--bg-elevated` | `#FFFAF3` | Cards ligeiramente levantados |
| `--bg-overlay` | `#F5E6D2` | Hover states |
| `--bg-deep` | `#F2DEC2` | Sidebar, masthead |
| `--text-primary` | `#1A1815` | Texto — preto quente, não puro |
| `--text-secondary` | `#4A4540` | Texto secundário |
| `--text-tertiary` | `#6B6359` | Labels, meta |
| `--accent-primary` | `#990F3D` | Claret FT — acento principal, active states |
| `--accent-glow` | `#1F3864` | Azul marinho WSJ — links |
| `--verdict-buy` | `#006F3C` | Verde FT — BUY |
| `--verdict-hold` | `#B3741F` | Âmbar — HOLD |
| `--verdict-avoid` | `#B22222` | Firebrick — AVOID |
| `--gain` | `#006F3C` | P&L positivo |
| `--loss` | `#B22222` | P&L negativo |
| `--rule` | `#1A1A1A` | Linha editorial dura (sob títulos) |
| `--border-subtle` | `#E5D6BE` | Bordas suaves |

### Paleta — Dark (FT/WSJ à noite) — DEFAULT

| Token | Hex | Uso |
|---|---|---|
| `--bg-canvas` | `#1B1916` | Carvão quente — não azul, não preto puro |
| `--bg-elevated` | `#232018` | Cards |
| `--bg-overlay` | `#2D2922` | Hover |
| `--bg-deep` | `#131210` | Sidebar |
| `--text-primary` | `#F2EDE3` | Creme quente — não branco puro |
| `--text-secondary` | `#BFB7A8` | Texto secundário |
| `--text-tertiary` | `#8A8275` | Labels |
| `--accent-primary` | `#E8957B` | Pêssego quente (análogo ao claret) |
| `--accent-glow` | `#95B0DD` | Azul suave noturno — links |
| `--verdict-buy` | `#6FAE7E` | Verde floresta suave |
| `--verdict-hold` | `#D4A55A` | Âmbar suave |
| `--verdict-avoid` | `#D97777` | Vermelho suave |
| `--gain` | `#6FAE7E` | P&L positivo |
| `--loss` | `#D97777` | P&L negativo |
| `--rule` | `#BFB7A8` | Linha editorial em fundo escuro |

### Tipografia

| Família | Stack | Uso |
|---|---|---|
| Serif | `"Source Serif 4", Charter, Cambria, Georgia, serif` | Títulos, display, masthead |
| Sans | `-apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif` | Corpo de texto, labels |
| Mono | `"JetBrains Mono", "SF Mono", Menlo, Consolas, monospace` | Números, tickers, valores financeiros, código |

**Regra dos números**: todos os valores financeiros (preços, P&L, percentagens, patrimônio) usam a fonte mono com `font-variant-numeric: tabular-nums` para alinhamento perfeito.

### Forma e espaço

- **Border-radius**: 0–2px. Cantos vivos. Zero arredondamento excessivo.
- **Cards**: borda fina, sem sombra exagerada. `border-t` ou `border-l` como accent em vez de bg colorido.
- **Regras horizontais**: `border-t-2` ou `border-b-2` sob títulos de secção — assinatura FT.
- **Pills/badges**: thin, uppercase, tracked. Sem excesso de cor. Ex: `BR` | `US` | `BUY` | `HOLD`.
- **Ícones**: usar com muita contenção. Preferir símbolos tipográficos (◇ ▤ ⚑ ⚖) a icon libraries cheias.
- **Espaçamento**: denso mas respirado. Escala 4px base.

### O que EVITAR

- Gradientes coloridos (zero)
- Cores neon / glow effects
- Border-radius > 4px em elementos de dados
- Ícones coloridos tipo dashboard SaaS
- Sombras exageradas
- Animações distratoras em dados financeiros
- Verde/vermelho saturado em excesso (usa as variantes suaves acima)

---

## 5. Dados disponíveis (SQLite local)

Duas bases: `br_investments.db` (Brasil) e `us_investments.db` (EUA). Schema idêntico.

### Tabelas principais

**`portfolio_positions`**
```
ticker TEXT, quantity REAL, entry_price REAL, current_price REAL,
market_value REAL, cost_basis REAL, asset_class TEXT,
market TEXT (br/us), active INTEGER
```

**`companies`**
```
ticker TEXT, name TEXT, sector TEXT, is_holding INTEGER (1=carteira, 0=watchlist),
currency TEXT
```

**`prices`** — série temporal diária
```
ticker TEXT, date TEXT, close REAL, volume INTEGER
PK (ticker, date)
```

**`fundamentals`** — snapshot trimestral
```
ticker TEXT, period_end TEXT,
eps REAL, bvps REAL, roe REAL,
pe REAL, pb REAL, dy REAL,           -- dividend yield
net_debt_ebitda REAL,
dividend_streak_years INTEGER,
is_aristocrat INTEGER,
market_cap REAL, fcf_ttm REAL,
ev_ebitda REAL, pe_forward REAL
PK (ticker, period_end)
```

**`scores`** — output do motor de scoring
```
ticker TEXT, run_date TEXT,
score REAL,                           -- 0.0 a 1.0
passes_screen INTEGER,                -- bool
details_json TEXT                     -- JSON com breakdown por critério
```

**`events`** — fatos relevantes / filings
```
ticker TEXT, event_date TEXT,
source TEXT (cvm/sec),
kind TEXT (8-K/10-K/dividend/fato_relevante),
url TEXT, summary TEXT
```

**`open_actions`** — triggers abertos dos agentes
```
id INTEGER, market TEXT, ticker TEXT,
kind TEXT,                            -- price_drop/div_cut/thesis_alert/etc
description TEXT, created_at TEXT, status TEXT
```

**`conviction_scores`** — score 0-100 por ticker
```
ticker TEXT, score INTEGER,
breakdown_json TEXT                   -- factores: thesis/IC/screen/quality
```

**`thesis_health`**
```
ticker TEXT, status TEXT (healthy/warning/stale),
last_checked TEXT, notes TEXT
```

**`verdict_history`** — histórico de veredictos para calibração
```
ticker TEXT, run_date TEXT,
verdict TEXT (BUY/HOLD/AVOID),
engine_breakdown JSON
```

---

## 6. Os Agentes — o "time" que trabalha para o utilizador

O sistema tem 14+ agentes autónomos. Os mais visíveis no front-end:

| Agente | Papel | Status |
|---|---|---|
| **Antonio Carlos** | Chief of Staff — chat widget, executa scripts, responde perguntas | live 24/7 |
| **Aurora** | Gera briefing matinal às 07:00 BRT | diário |
| **Perpetuum Master** | Corre 12 perpetuums diários (thesis, vault, data coverage...) | diário |
| **Council** | 9 personas sintéticas (Buffett/Dalio/Klarman/Taleb/Grantham/etc) debatem cada ticker | on-demand |
| **Bibliotheca** | Ingestão de livros de investimento + RAG local | semanal |
| **Jarbas** | Bot Telegram — notificações e comandos por mensagem | live |
| **Helena** | Design system linter + audit | on-demand |

**Antonio Carlos** é o mais importante para o front-end: reside no chat widget, tem memória conversacional, usa tool-calling com 16 ferramentas do sistema.

---

## 7. Referência de produto — Valoria AI

A estrutura visual e de UX da Mission Control é inspirada directamente no **Valoria AI** (plataforma BR de análise de investimentos). O screenshot de referência mostra:

- Header global com search + date range + notifications
- Sidebar esquerda com grupos de navegação (ANÁLISE / CARTEIRA / INTELIGÊNCIA)
- Dashboard em 3 zonas: KPIs → análise central + right rail → bottom row
- Zona central: gráfico de Valor Justo + painel de Recomendação com Confluência de Métodos
- Bottom: Diversificação (donut) + Shortlist/Top Picks + Alertas

**A nossa vantagem sobre o Valoria:**
- Council de 9 personas sintéticas (Buffett/Dalio/Klarman/Taleb/etc)
- Antonio Carlos (chat que executa scripts reais)
- Pipeline 100% local (zero cloud, zero dados enviados)
- DRIP projection + conviction scoring próprio

**Mapeamento Valoria → Mission Control:**

| Valoria | Mission Control | Fonte de dados |
|---|---|---|
| Carteira Total (R$ 2,48 mi) | Patrimônio BR + US | `/api/portfolio/summary` |
| Valor Justo Médio | Graham Number médio das holdings | `sqrt(22.5 × eps × bvps)` — computado client-side |
| Potencial de Upside | `(graham_number - price) / price × 100` | `/api/ticker/:ticker` |
| Rating Médio (4.2) | Média de `score × 10` | `/api/conviction` |
| Comparativo de Valor Justo (chart) | Preço vs Graham Number histórico | `/api/prices` + `fundamentals` |
| Recomendação: COMPRA | Council stance: BUY/HOLD/AVOID | `/api/council` |
| Confluência dos Métodos (8.7/10) | 5 engines: graham/buffett/drip/macro/hedge | `/api/strategy/:ticker` |
| Diversificação da Carteira (donut) | Posições por `group_label` | `/api/portfolio/positions` |
| Shortlist – Top Picks | Tickers ordenados por conviction score | `/api/conviction` |
| Fatos Relevantes | Events CVM/SEC | `/api/briefing` + events table |
| Alertas | Open actions dos agentes | `/api/actions` |

---

## 8. Layout global

### Header (fixo, topo, altura 56px)

```
[Logo: "MC"] [Search: "Buscar tickers, executar comandos..." ⌘K] [----] [Date: 01/05 – 31/05] [🔔 3] [👤]
```

- **Logo**: "MC" em serif bold ou "Mission Control" compacto
- **Search bar** (centro, larga): ao activar → abre o Antonio Carlos (chat + busca de tickers)
- **Date range**: período de análise activo (afecta gráficos + council filter)
- **🔔**: badge com count de open actions
- **👤**: avatar + nome + logout

### Sidebar esquerda (fixa, 200px, fundo `--bg-deep`)

```
HOJE
  Dashboard
  Actions [badge count]

ANÁLISE
  Portfolio
  Ticker
  Comparador

CONSELHO
  Council
  Allocation

INTELIGÊNCIA
  Briefing
  Content
  Memory

SISTEMA
  Calendar
  Team

─────────────────
● antonio carlos · live
[toggle dark/light]  v3
```

- Labels de grupo em uppercase tracking (`font-mono text-xs text-tertiary`)
- Items sem ícones (Valoria usa ícones — nós usamos texto puro, editorial)
- Active state: borda-esquerda 2px `--accent-primary`
- Footer: dot verde pulsante "antonio carlos · live" + theme toggle

---

## 9. Páginas — especificação Valoria-inspired

### 9.1 Home Dashboard (`/`)

Layout em **3 zonas verticais** + **right rail**.

```
┌────────────────────────────────────────────────────────┬──────────────┐
│  [KPI 1]  [KPI 2]  [KPI 3]  [KPI 4]                   │              │
├────────────────────────────────────┬───────────────────┤  DESTAQUES   │
│                                    │                   │  DIÁRIOS     │
│   GRÁFICO — Evolução / Valor Justo │  RECOMENDAÇÃO     │              │
│   (chart Recharts, linha)          │  + CONFLUÊNCIA    │  (briefing   │
│                                    │                   │  + events    │
│                                    │                   │  feed)       │
├───────────────┬────────────────────┴───────────────────┤              │
│ DIVERSIFICAÇÃO│   SHORTLIST — TOP PICKS                │              │
│ (donut chart) │   (tabela 6 linhas conviction)         │  ALERTAS     │
│               │                                        │  (actions)   │
└───────────────┴────────────────────────────────────────┴──────────────┘
```

#### Zona 1 — 4 KPI Cards

| Card | Valor | Delta | Fonte |
|---|---|---|---|
| **Patrimônio BR** | `br.market_value_plus_rf` em BRL | `br.pnl_pct` % vs custo | `/api/portfolio/summary` |
| **Portfolio US** | `us.market_value` em USD | `us.pnl_pct` % vs custo | `/api/portfolio/summary` |
| **Upside Médio** | média de `(current_unit/entry_unit - 1) × 100` das holdings | vs mês anterior (se disponível) | `/api/portfolio/positions` |
| **Rating Médio** | média de `score × 10` das holdings com score | texto "Bom" / "Atenção" / "Risco" | `/api/conviction` |

Cada card: label uppercase small + valor grande mono + delta colorido + vs referência.

---

#### Zona 2 — Análise central (2 colunas)

**Col esquerda (65%) — Gráfico:**

Tabs: `Carteira` · `Ticker em destaque`

- **Tab Carteira**: linha de P&L total cumulativo (soma de todas as posições) ao longo do tempo. Linha tracejada horizontal = custo total. Período selector: 1M · 3M · 6M · 12M · Tudo.

- **Tab Ticker em destaque** (default = top conviction da carteira):
  - Linha azul: preço actual (365d) via `/api/prices/:ticker`
  - Linha tracejada amarela: **Graham Number** computado a partir dos fundamentals
    ```
    graham_number = Math.sqrt(22.5 × fundamentals.eps × fundamentals.bvps)
    ```
  - Linha tracejada laranja: preço médio de entrada (`position.entry_price`)
  - Legenda: "Preço" · "Valor Justo (Graham)" · "Custo"

**Col direita (35%) — Recomendação:**

Para o ticker em destaque:

```
┌─────────────────────────────┐
│  ↑  COMPRA                  │  ← big pill, verde escuro
│                             │
│  Potencial de Upside        │
│  24.7%                      │  ← (graham_number - price) / price
│                             │
│  Preço Actual   R$ 13,66    │
│  Valor Justo    R$ 17,02    │  ← Graham Number
│                             │
│  Confluência dos Engines    │
│  ████████░░  8.0 / 10       │  ← barra colorida
│  graham ✓  buffett ✓        │
│  drip ✓    macro ✓  hedge ✗ │
└─────────────────────────────┘
```

**Cálculo da Confluência (X/10):**
```typescript
// Para cada engine em /api/strategy/:ticker
const pts = runs.reduce((acc, r) => {
  if (r.verdict === 'BUY')  return acc + 2;
  if (r.verdict === 'HOLD') return acc + 1;
  return acc;  // AVOID = 0
}, 0);
const score = (pts / (runs.length * 2)) * 10;  // normalizado 0-10
```

---

#### Zona 2.5 — Right Rail (300px, fixo à direita)

**Destaques Diários:**
- 5 linhas do briefing matinal (strip frontmatter, mostrar apenas parágrafos de texto)
- Link "ver briefing completo →"

**Fatos Recentes:**
- Últimos 5 events (CVM/SEC) da tabela `events`
- Formato: `PETR4 · há 1h · Comunicado sobre distribuição de dividendos [NOVO]`
- Cor de destaque se evento de holding activa

**Alertas:**
- 3 open actions mais urgentes
- Botões approve/ignore inline
- Link "ver todos os alertas →"

---

#### Zona 3 — Bottom Row (3 colunas)

**Col 1 — Diversificação da Carteira:**

Donut chart (Recharts PieChart) com `group_label` das posições:
- Ações BR (azul escuro)
- US Equities (azul)
- FIIs (verde)
- Tesouro Direto (dourado)
- Outros RF (cinza)

Legenda ao lado: `● Ações 28% · ● FIIs 15% · ...`

Fonte: `/api/portfolio/positions` → agrupa por `group_label` → soma `current_value`

---

**Col 2 — Shortlist / Top Picks:**

Tabela de 6 linhas, ordenada por conviction score DESC.

```
Ativo         Preço Actual  Valor Justo  Recom.   Upside
ITSA4         R$ 13,66      R$ 17,02     COMPRA   +24.7%
BBDC4         R$ 19,19      R$ 22,40     COMPRA   +16.7%
VALE3         R$ 78,39      R$ 91,20     COMPRA   +16.3%
...
```

- Fonte tickers: `/api/conviction?market=br` sorted by score DESC
- Preço: `last_price.close` via `/api/ticker/:ticker`
- Valor Justo: `sqrt(22.5 × eps × bvps)` dos fundamentals
- Recom.: stance do council ou verdict do engine com maior score
- Upside: `(valor_justo - preco) / preco × 100`

Botão: "Ver shortlist completa →" → `/portfolio`

---

**Col 3 — Alertas:**

(já descrito no right rail — aqui mostrar a versão expandida com 5 items)

---

### 9.2 Portfolio (`/portfolio`)

**Header com 4 stats** (mini KPI row):
Patrimônio BR | Portfolio US | n posições BR | n posições US

**Tabs horizontais:**
`Tudo` · `Ações BR` · `FIIs` · `US Equities` · `Renda Fixa`

**Por cada grupo (header collapsible):**
```
▸ Ações BR                R$ 312.450    +18.4%    60.2% da carteira BR
  ticker | nome | qtd | p.médio | p.atual | MV | P&L R$ | P&L %
```

Tabela:
- Ticker: link mono → `/ticker/:ticker`
- Nome: sans, truncated
- Qtd: mono tabular right-align
- P. Médio: mono right-align
- P. Actual: mono right-align
- MV: mono right-align bold
- P&L R$: mono colorido (gain/loss)
- P&L %: mono colorido + badge

Renda Fixa: sem P. Actual; mostrar `taxa` + `vencimento` em vez de P&L

Rodapé: totais por mercado. BRL e USD **nunca** somados.

---

### 9.3 Ticker Page (`/ticker/:ticker`)

Layout idêntico ao Valoria ticker view:

**Header:**
```
Itaúsa [ITSA4] [BR] · Holding
R$ 13,66  ▼ -0.44%  hoje
```

**Main (2 colunas, como o dashboard):**

*Left — Gráfico "Comparativo de Valor Justo":*
- 3 linhas: Preço Actual (azul) · Graham Number (amarelo tracejado) · Custo de Entrada (laranja tracejado)
- Período: 1M · 3M · 6M · 12M · Tudo
- Fonte: `/api/prices/:ticker` + `fundamentals.eps` + `fundamentals.bvps`

*Right — Recomendação:*
- Pill COMPRA/HOLD/EVITAR (do council stance)
- Upside % (graham vs preço)
- Preço Actual + Valor Justo
- Confluência X/10 (5 engines com ticks)
- Posição: qtd · p.médio · MV · P&L

**Grid fundamentals (8 métricas, abaixo do chart):**
```
PE: 9.2    PB: 1.7    DY: 8.99%    ROE: 17.6%
N.D/EBITDA: 4.0    Div Streak: 20a    Mkt Cap: R$153B    EV/EBITDA: 105x
```
Cada métrica: label pequeno + valor mono grande + dot colorido (verde=ok / âmbar=warn / vermelho=fail vs threshold)

**5 Action Buttons (row):**
`Deepdive` · `Council` · `Tese` · `Nota` · `Refresh`

---

### 9.4 Council (`/council`)

**Header:** data do último run + BUY N · HOLD N · AVOID N · N/A N

**Filtros:** stance (pill toggle) · market (BR/US) · busca por ticker

**Tabela:**
```
Ticker  Sector       Stance   Conf.   Dissensos  Flags  Data
ACN     Technology   BUY      high    1          1      30/04
ABBV    Healthcare   HOLD     medium  2          2      30/04
```
- Stance: pill colorida (verde/âmbar/vermelho)
- Click → `/council/:ticker` (dossier completo com markdown do STORY + debate das personas)

---

### 9.5 Tasks / Actions (`/tasks`)

**Header:** count open · filtros por market e kind

**Lista de cards:**
```
┌─ price_drop ──────────────────────────────────────────┐
│  VALE3 [BR]  price_drop                  há 2h        │
│  VALE3 caiu 8.3% em 2 sessões                         │
│  [✓ Approve]  [✗ Ignore]  [→ Deepdive]               │
└───────────────────────────────────────────────────────┘
```
Borda-esquerda colorida por kind:
- `price_drop` → `--loss` (vermelho suave)
- `div_cut` → `--verdict-avoid`
- `thesis_alert` → `--accent-primary`
- `screen_pass` → `--verdict-buy`
- `earnings_react` → `--accent-glow`

---

## 10. Chat Widget — Antonio Carlos

Em **todas as páginas**, bottom-right. É também o que abre ao pressionar ⌘K no search bar.

**Estado fechado:**
```
● antonio carlos  ⌘K
```
Pill editorial com dot verde pulsante. Não é bolha de chat.

**Estado aberto (slide-up, 420px × 65vh):**
- Header: "antonio carlos" + [×]
- Histórico: bolhas user (direita, `--bg-overlay`) + agent (esquerda, borda-left `--accent-primary`)
- Typing indicator: 3 dots animados quando aguarda resposta (5-30s normal)
- Input + send

**Comportamento:**
- `chat_id` = `"dashboard"` ou `"ticker-ITSA4"` (muda por página)
- Agent tem memória por `chat_id` via `/api/chat`
- Pode citar tickers linkáveis: clicar em `ITSA4` no chat → navega para `/ticker/ITSA4`

---

## 10. O que este produto É e NÃO É

### É
- Painel de controlo de um gestor individual sério
- Ferramenta de decisão apoiada por IA **local** (zero cloud, zero dados enviados para fora)
- Jornalismo financeiro pessoal — FT/WSJ no tom
- Orientado à acção: cada página responde "o que devo fazer agora?"
- Desktop-first (1440px+ largura óptima)

### Não é
- App de trading (sem compra/venda directa)
- Robinhood / Revolut (zero gamification, zero verde/vermelho saturado)
- Dashboard de KPIs de SaaS (sem icon cards coloridos)
- Bloomberg Terminal (não queremos complexidade assustadora)
- App mobile (não é prioridade)

---

## 11. Referências visuais consolidadas

| Referência | O que pegar |
|---|---|
| **Financial Times** | Paleta salmão, regras horizontais, serif headlines, densidade editorial |
| **Wall Street Journal** | Monocromático quase, hierarquia clara, tabelas densas |
| **The Economist** | Headlines directas, zero decoração desnecessária, opiniões fortes |
| **Linear** | Densidade nas tabelas de tasks (não a estética purple SaaS) |
| **Notion** | Hierarquia de conteúdo limpa, sans body |
| **Seeking Alpha** | Simplificação de charts de preço |

---

## 12. API Backend — já implementada e a correr

O backend Express está implementado e funcional. O Manus **não precisa de criar nenhum servidor** — só fazer `fetch()` para os endpoints abaixo.

### Como arrancar

```bash
cd mission-control
npm run api        # inicia em http://localhost:3001
npm run api:watch  # com hot-reload
```

### Vite config — proxy obrigatório

```typescript
// vite.config.ts
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:3001'
    }
  }
}
```

Com o proxy activo, o frontend faz `fetch('/api/...')` e o Vite encaminha para o Express. Sem CORS, sem URL hardcoded.

---

### Referência completa de endpoints

#### `GET /api/health`
```json
{
  "status": "ok",
  "ts": "2026-05-06T18:43:10.437Z",
  "ii_root": "C:\\Users\\paidu\\investment-intelligence",
  "dbs": { "br": true, "us": true }
}
```

---

#### `GET /api/portfolio/summary`
Patrimônio total por mercado. Usar na Home para os 4 stat blocks.
```json
{
  "br": {
    "market_value": 518771.47,
    "market_value_plus_rf": 679743.07,
    "cost": 464241.64,
    "pnl_abs": 54529.83,
    "pnl_pct": 11.75,
    "rf_total": 160971.60,
    "n_positions": 26
  },
  "us": {
    "market_value": 22616.16,
    "cost": 17712.17,
    "pnl_abs": 4903.99,
    "pnl_pct": 27.69,
    "n_positions": 21
  }
}
```

---

#### `GET /api/portfolio/positions`
Array de todas as posições. Usar na página Portfolio.

Cada item:
```json
{
  "id": "br_ITSA4",
  "market": "br",
  "asset_class": "equity",
  "group_label": "Ações",
  "ticker": "ITSA4",
  "name": "Itaúsa",
  "sector": "Holding",
  "quantity": 2485,
  "entry_unit": 7.79,
  "current_unit": 13.66,
  "cost_basis": 19359.15,
  "current_value": 33954.10,
  "pnl_abs": 14594.95,
  "pnl_pct": 75.39,
  "maturity_date": null,
  "rate": null,
  "weight_pct": 6.54
}
```

`group_label` possíveis: `"Ações"` · `"US Equities"` · `"FIIs"` · `"ETFs"` · `"Tesouro Direto"` · `"Debêntures"` · `"CRAs"` · `"LCAs"` · `"Fundos"`

`asset_class` possíveis: `equity` · `fii` · `etf` · `tesouro` · `debenture` · `cra` · `lca` · `fundo`

---

#### `GET /api/actions?limit=20`
Open actions dos agentes. Usar na Home (top 5) e na página Tasks.
```json
[
  {
    "id": 42,
    "market": "br",
    "ticker": "VALE3",
    "kind": "price_drop",
    "description": "VALE3 caiu 8.3% em 2 sessões — abaixo do threshold de -7%",
    "created_at": "2026-05-05T14:22:00",
    "status": "open"
  }
]
```

`kind` possíveis: `price_drop` · `div_cut` · `thesis_alert` · `screen_pass` · `earnings_react`

#### `PATCH /api/actions/:id?market=br`
Resolver ou ignorar uma action.
```json
// request body
{ "status": "resolved" }   // ou "ignored"

// response
{ "ok": true }
```

---

#### `GET /api/council?limit=200&market=br`
Output do Conselho. Usar na Home (snapshot) e na página Council.
```json
{
  "summary": {
    "date": "2026-04-30",
    "total": 14,
    "buy": 9,
    "hold": 3,
    "avoid": 0,
    "needs_data": 2
  },
  "entries": [
    {
      "ticker": "ACN",
      "market": "us",
      "stance": "BUY",
      "confidence": "high",
      "dissent_count": 1,
      "flag_count": 1,
      "date": "2026-04-30",
      "sector": "Technology",
      "is_holding": true,
      "margin_of_safety": 0.18,
      "elapsed_sec": 52,
      "seats": ["Buffett", "Dalio", "Klarman", "Taleb", "Druckenmiller"]
    }
  ]
}
```

`stance` possíveis: `"BUY"` · `"HOLD"` · `"AVOID"` · `"NEEDS_DATA"` · `"UNKNOWN"`

#### `GET /api/council/:ticker`
Dossier completo de um ticker. Usar na página `/council/[ticker]`.
```json
{
  "entry": { /* CouncilEntry completo */ },
  "body": "# ACN — Investment Story\n\n...",
  "council_md": "## Council Debate\n\n..."
}
```

---

#### `GET /api/ticker/:ticker?market=br`
Tudo sobre um ticker. Usar na página `/ticker/[ticker]`.
```json
{
  "ticker": "ITSA4",
  "market": "br",
  "company": {
    "ticker": "ITSA4",
    "name": "Itaúsa",
    "sector": "Holding",
    "is_holding": 1,
    "currency": "BRL"
  },
  "fundamentals": {
    "period_end": "2026-05-05",
    "eps": 1.48,
    "bvps": 7.917,
    "roe": 0.17571,
    "pe": 9.23,
    "pb": 1.725,
    "dy": 0.0899,
    "net_debt_ebitda": 4.03,
    "dividend_streak_years": 20,
    "pe_forward": 7.10,
    "market_cap": 153146998784,
    "ev_ebitda": 105.72
  },
  "score": {
    "run_date": "2026-05-05",
    "score": 0.82,
    "passes_screen": 1,
    "details": { "dy": true, "roe": true, "pb": false }
  },
  "position": {
    "quantity": 2485,
    "entry_price": 7.79,
    "active": 1
  },
  "last_price": {
    "date": "2026-05-05",
    "close": 13.66,
    "volume": 24064600
  }
}
```

**Nota**: `dy`, `roe`, `pb` estão em decimais (0.0899 = 8.99%). Multiplicar por 100 para mostrar como percentagem.

**Auto-detect market**: se omitir `?market=`, o servidor detecta automaticamente (verifica BR primeiro, depois US).

---

#### `GET /api/prices/:ticker?market=br&days=365`
Série temporal de preços. Usar nos charts de linha.
```json
[
  { "date": "2026-04-29", "close": 13.66, "volume": 24356600 },
  { "date": "2026-04-30", "close": 13.92, "volume": 31950600 },
  { "date": "2026-05-04", "close": 13.60, "volume": 20967300 },
  { "date": "2026-05-05", "close": 13.66, "volume": 24064600 }
]
```

---

#### `GET /api/dividends?days=45`
Próximos dividendos. Usar na Home e na página Calendar.
```json
[
  {
    "market": "us",
    "ticker": "JNJ",
    "ex_date": "2026-05-20",
    "amount": 1.24
  }
]
```

---

#### `GET /api/briefing`
Briefing matinal gerado pelo agente Aurora.
```json
{
  "content": "---\ntags: [dashboard, briefing]\n---\n# Daily Briefing\n\n...",
  "mtime": "2026-04-28T18:40:45.218Z"
}
```

`content` é Markdown. Fazer strip do frontmatter (`---`) antes de mostrar. `mtime` é ISO 8601.

---

#### `GET /api/agents`
Status de todos os agentes. Usar na Home e na página Team.
```json
{
  "morning_briefing": {
    "name": "morning_briefing",
    "last_status": "ok",
    "last_run": "2026-04-28T07:00:00+00:00",
    "consecutive_failures": 0,
    "run_count": 12,
    "failed_count": 0,
    "last_summary": "Briefing gerado com 8 secções"
  }
}
```

`last_status` possíveis: `"ok"` · `"failed"` · `"no_action"` · `null`

#### `GET /api/agents/personas`
Perfis completos dos agentes (nome, título, bio, departamento).

#### `GET /api/agents/departments`
Agentes agrupados por departamento.

---

#### `GET /api/strategy/:ticker?market=us`
Runs dos 5 engines de estratégia para um ticker.
```json
[
  { "ticker": "ACN", "engine": "buffett", "verdict": "HOLD", "score": 0.67, "run_ts": "2026-05-04" },
  { "ticker": "ACN", "engine": "drip",    "verdict": "HOLD", "score": 0.95, "run_ts": "2026-05-04" },
  { "ticker": "ACN", "engine": "hedge",   "verdict": "HOLD", "score": 1.00, "run_ts": "2026-05-04" },
  { "ticker": "ACN", "engine": "macro",   "verdict": "BUY",  "score": 1.00, "run_ts": "2026-05-04" }
]
```

Engines possíveis: `graham` · `buffett` · `drip` · `macro` · `hedge`

---

#### `GET /api/allocation/br` ou `/api/allocation/us`
Proposta de alocação mais recente (gerada pelo overnight backfill).
```json
{
  "market": "br",
  "date": "2026-05-04",
  "target_weights": { "ITSA4": 0.08, "BBDC4": 0.07 },
  "bucket_weights": { "graham": 0.25, "buffett": 0.30, "drip": 0.20, "macro": 0.15, "hedge": 0.10 },
  "conflicts": [],
  "notes": ["Macro overlay: expansion — hedge size 0%"]
}
```

---

#### `GET /api/conviction?market=br`
Conviction scores 0-100 para todos os tickers.
```json
[
  { "market": "br", "ticker": "ITSA4", "score": 90, "breakdown": {} },
  { "market": "br", "ticker": "BBDC4", "score": 76, "breakdown": {} }
]
```

---

#### `GET /api/topics`
Topic Watchlist scored. Usar na página Content.
```json
{
  "computed_at": "2026-05-05T09:00:00",
  "topics": [
    {
      "id": "br_banks",
      "name": "Bancos BR",
      "score": 82,
      "tier": "make_now",
      "tickers": ["BBDC4", "ITUB4", "BBAS3"],
      "holdings_hit": ["BBDC4"],
      "open_triggers": 2
    }
  ]
}
```

`tier` possíveis: `"make_now"` · `"rising"` · `"watch"` · `"background"`

---

#### `GET /api/memory/auto?limit=100`
Memórias automáticas do Claude (tipo user/feedback/project/reference).

#### `GET /api/memory/daily?limit=60`
Research digests e entradas diárias do vault.

---

#### `POST /api/chat`
Envia mensagem para o Antonio Carlos (Fiel Escudeiro). Pode demorar 5-30s.
```json
// request
{ "message": "qual o verdict de ITSA4?", "chat_id": "web-session-abc123" }

// response (sucesso)
{ "reply": "ITSA4 está com conviction 90/100...", "chat_id": "web-session-abc123" }

// response (erro)
{ "error": "escudeiro exited 1", "stderr": "..." }
```

`chat_id` é livre — usar para separar sessões de diferentes páginas ou utilizadores. O agente mantém memória por `chat_id`.

---

### Padrão de fetch recomendado

```typescript
// lib/api.ts
const API = '';  // string vazia — o proxy Vite trata de /api/*

export async function fetchSummary() {
  const r = await fetch(`${API}/api/portfolio/summary`);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export async function fetchPositions() {
  return fetch(`${API}/api/portfolio/positions`).then(r => r.json());
}

export async function fetchTicker(ticker: string, market?: 'br' | 'us') {
  const q = market ? `?market=${market}` : '';
  return fetch(`${API}/api/ticker/${ticker}${q}`).then(r => r.json());
}

export async function fetchPrices(ticker: string, market: 'br' | 'us', days = 365) {
  return fetch(`${API}/api/prices/${ticker}?market=${market}&days=${days}`).then(r => r.json());
}

export async function sendChat(message: string, chatId = 'default') {
  const r = await fetch(`${API}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, chat_id: chatId }),
  });
  return r.json();
}
```

---

### Notas de formatação

| Campo | Como mostrar |
|---|---|
| `dy`, `roe`, `pb`, `pe` | São decimais — `dy * 100` → `"8.99%"` |
| `market_cap` | Em BRL/USD — dividir por `1e9` para `"R$ 153B"` |
| `close` (preços) | Float com 2 casas — `close.toFixed(2)` |
| `pnl_pct` | Já em % — `pnl_pct.toFixed(1) + "%"` |
| `mtime` (briefing) | ISO 8601 — usar `new Date(mtime).toLocaleDateString('pt-BR')` |
| `last_run` (agents) | ISO 8601 — mostrar como "há X min" com date-fns ou similar |
| `score` (scores) | 0.0 a 1.0 — `score * 100` para mostrar como 0-100 |
| `content` (briefing) | Markdown — strip do bloco `---...---` antes de renderizar |

---

## 13. Entregável esperado do Manus

Construir o frontend **React + Vite + Wouter + TailwindCSS** da Mission Control com layout inspirado no **Valoria AI** — mas com os nossos dados e os nossos agentes.

---

### Stack

```
React 19 + TypeScript
Vite 6 (build tool, com proxy /api → localhost:3001)
Wouter (routing leve — já no App.tsx dado)
TailwindCSS v4
Recharts (PieChart + LineChart)
```

---

### Páginas obrigatórias (5)

| Rota | Página | Fonte principal |
|---|---|---|
| `/` | Home Dashboard (layout Valoria 3 zonas) | `/api/portfolio/summary` + `/api/council` + `/api/conviction` + `/api/actions` + `/api/briefing` |
| `/portfolio` | Portfolio com tabs por classe + tabela P&L | `/api/portfolio/positions` |
| `/ticker/:ticker` | Ticker detail com gráfico Valor Justo | `/api/ticker/:ticker` + `/api/prices/:ticker` + `/api/strategy/:ticker` |
| `/council` | Council table com filtros | `/api/council` |
| `/tasks` | Actions queue com approve/ignore | `/api/actions` + `PATCH /api/actions/:id` |

---

### Componentes obrigatórios

| Componente | Descrição |
|---|---|
| `<AppShell>` | Header global + Sidebar + main outlet + ChatWidget |
| `<Header>` | Search bar ⌘K + date range + notification bell + avatar |
| `<Sidebar>` | 5 grupos (HOJE/ANÁLISE/CONSELHO/INTELIGÊNCIA/SISTEMA) + footer AC status |
| `<KpiCard>` | label + valor mono grande + delta colorido + sub-label |
| `<ValorJustoChart>` | Recharts LineChart 3 linhas: preço / Graham Number / custo entrada |
| `<RecomendacaoPanel>` | Pill COMPRA/HOLD/EVITAR + upside % + preço vs valor justo + confluência bar |
| `<ConfluenciaBar>` | 5 engines como score X/10 com ticks individuais |
| `<DiversificacaoDonut>` | Recharts PieChart por group_label + legenda |
| `<TopPicksTable>` | 6 linhas: ticker + preço + valor justo + recom + upside |
| `<AlertasFeed>` | 3-5 open actions com approve/ignore inline |
| `<PortfolioTable>` | Tabela por grupo collapsible, tudo mono tabular |
| `<StancePill>` | BUY/HOLD/AVOID/NEEDS_DATA em cores token |
| `<ChatWidget>` | Pill `● antonio carlos ⌘K` + slide-up panel + `POST /api/chat` |

---

### Cálculos client-side (sem nova rota API)

```typescript
// Valor Justo (Graham Number) — computar em cada ticker
function grahamNumber(eps: number, bvps: number): number {
  if (eps <= 0 || bvps <= 0) return 0;
  return Math.sqrt(22.5 * eps * bvps);
}

// Upside potencial
function upside(price: number, fairValue: number): number {
  return ((fairValue - price) / price) * 100;
}

// Confluência dos engines (0–10)
function confluencia(runs: StrategyRun[]): number {
  if (!runs.length) return 0;
  const pts = runs.reduce((acc, r) => {
    if (r.verdict === 'BUY')  return acc + 2;
    if (r.verdict === 'HOLD') return acc + 1;
    return acc;
  }, 0);
  return (pts / (runs.length * 2)) * 10;
}

// Rating Médio da carteira (0–10)
function ratingMedio(positions: Position[], convictions: ConvictionScore[]): number {
  const map = Object.fromEntries(convictions.map(c => [c.ticker, c.score]));
  const scores = positions.map(p => map[p.ticker]).filter(Boolean);
  return scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length / 10 : 0;
}
```

---

### Design system (resumo — paleta completa na Secção 4)

**Dark mode default** (obrigatório):

```css
--bg-canvas:    #1B1916   /* carvão quente — NOT pure black, NOT blue */
--bg-elevated:  #232018   /* cards */
--bg-deep:      #131210   /* sidebar */
--text-primary: #F2EDE3   /* creme quente — NOT pure white */
--accent:       #E8957B   /* pêssego */
--verdict-buy:  #6FAE7E   /* verde floresta */
--verdict-hold: #D4A55A   /* âmbar */
--verdict-avoid:#D97777   /* vermelho suave */
```

**Tipografia:**
- Títulos de secção + masthead: serif (Georgia / Source Serif 4)
- Body: system sans
- **Todos os números financeiros**: `font-mono` + `tabular-nums` (obrigatório)

**Forma:**
- Border-radius: 0–2px (cantos vivos, não arredondados)
- Cards: `border border-[--border-subtle]` sem sombra
- Regras horizontais `border-b-2` sob títulos (assinatura FT)
- Zero gradientes, zero neon, zero ícones coloridos

---

### Arquitectura de dados

```
SQLite  ──►  Express API  ──►  Vite proxy  ──►  React
             :3001              /api/*             fetch('/api/...')
             (PRONTO)           (config)           (a construir)
```

O backend está 100% implementado e testado com dados reais.
O Manus só constrói o **frontend**.
