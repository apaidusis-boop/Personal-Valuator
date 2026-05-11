---
type: design_brief
phase: U.1
sprint: home_redesign
audience: claude_design (Anthropic Labs)
prereq_reading: [[Brain_Map]] + [[Design_System_v2]] + [[../_assets/proto_home_v1_c|proto_home_v1_c.html]]
owner: helena_linha
status: ready_for_session
created: 2026-04-27
tags: [brief, design, home, claude_design, U1]
---

# Brief — Início (Home redesign integrado · Phase U.1)

> Este brief é para uma sessão de Claude Design. Antes de o usar:
> 1. Cola o `Brain_Map.md` inteiro (contexto integrado).
> 2. Cola o `Design_System_v2.md` (paleta + tipografia).
> 3. Cola este brief.
> 4. Itera no canvas.

## TL;DR

Refazer a Home do dashboard Streamlit para implementar a direcção Hara/MUJI editorial v2.0 aprovada em `proto_home_v1_c.html`. **Fundir Captain's Log dentro da Home** — não há valor em ter 2 pages que mostram conteúdo similar. Saída: `proto_inicio_v2_<variant>.html` para review, depois handoff a Claude Code para implementação Streamlit reusando `_components.py` (com refactor para v2.0).

## Contexto curto (em uma frase)

A Home actual é dashboard-y (KPIs em tile-grid, stat bar dominante, voz de UI engineer). A direcção aprovada é **editorial banking** — abrir com lede sentence completa, não com números soltos.

## Objectivo da sessão

Produzir 2 variantes HTML da nova Início, com este conteúdo concreto e respeitando v2.0:

### Conteúdo obrigatório da página

1. **Lede sentence** (abertura — 1 frase única):
   > *"A carteira encerra a semana em R$ 287.432, com +1,24% em sete pregões, distribuída por 33 posições entre Brasil e Estados Unidos."*
   > (mock — valor real vem de SQLite L1 em runtime)

2. **Captain's Log inline** (3-4 cards narrativos curtos, fundidos da page actual):
   - **Decisão pendente em destaque** — uma T2 action com mais peso (ex: "Reforçar BBDC4 — proposta da thesis · porque conviction subiu de 88 para 92").
   - **Variant Perception destacada** — 1 holding onde a tese da casa diverge do consenso analista (1 frase).
   - **RI material change** — se algum holding teve filing CVM/SEC nas últimas 72h com flag material.
   - **Synthetic IC quote** — 1 pull-quote de uma das 5 personas (Buffett/Druck/Taleb/Klarman/Dalio) sobre um holding, em formato editorial italic.

3. **Sidebar de carteiras** (à esquerda, fixa):
   - "Carteiras" (eyebrow)
   - 3 grupos: 🇧🇷 Brasil (12 posições, R$ X), 🇺🇸 EUA (21 posições, US$ Y), Total em BRL (R$ Z)
   - Lista clicável de "Carteiras Recomendadas" (XP Top Div, BTG PS, Suno) — tracking dos 3 analistas que o user lê.

4. **Chart hero** (centro/direita):
   - Performance 5 anos (não "5y") em base 100.
   - 3 séries: portfolio BR, portfolio US, IBOV (dotted reference).
   - Labels inline no fim das linhas. **Sem legenda em caixa**.
   - 1 série em `clay`, restantes em `ink` muted.

5. **Holdings table** (densa mas elegante, abaixo do chart):
   - 33 rows. Sem paginação visível.
   - Colunas: Ativo (serif), Sector (small caps), MV em moeda, % portfolio, DY 12m, Conviction (0-100 em mono pequeno), Stale flag (badge clay se RI > 90 dias).
   - Sem zebra striping. Sem cores ornamentais.
   - Tabular nums forced.

6. **Decisões pendentes inline** (rodapé inferior — não secção separada):
   - Lista compacta de Actions Queue T2 abertas. Cada uma: `• proposed_by · tier · why_one_liner` em serif italic.
   - Link "Ver todas (18)" para nav `/decisoes`.

### Conteúdo proibido nesta page

- ❌ Tile-grid de KPIs (12 tiles `kpi_tile()` em row).
- ❌ Stat bar tipo Robinhood (% Day, % Week, % YTD em row).
- ❌ Page title "🏠 Home" — usar **"Início"** em italic serif (sem emoji).
- ❌ Mais de 3 usos do accent `clay`.
- ❌ Captions condescendentes ("9 perpetuums autónomos", "zero tokens Claude").
- ❌ "Last updated 14:32" — datas formato `27 de abril, 14:32`.

## Variantes a produzir

### Variante 1 — "Início serena"
Mais próxima do `proto_home_v1_c.html` original. Densidade média. Mais whitespace. Foco em legibilidade contemplativa.

### Variante 2 — "Início densa"
Mesmas regras v2.0 mas comprimida verticalmente. Mais informação acima do fold. Útil em dias de muita actividade (várias decisões pendentes + várias material changes).

> A escolha entre serena/densa pode ser **per-user-preference toggle** futuro. Mas hoje, propor as 2 versões de tokens-respeitam-100% para o user escolher uma como default.

## Respeitar (não-negociáveis v2.0)

Recapitulação dos 7 princípios + 8 anti-padrões está em `Design_System_v2.md`. Resumo dos 5 mais críticos para esta page:

1. ✅ **Voz humana > stat bar** — abre com lede sentence.
2. ✅ **Cream `#f4eee5`** background. Texto `ink #2a2622`. **Sem dark mode.**
3. ✅ **3 fontes** — Source Serif 4 (títulos, body, lede), Inter (eyebrows, micro-labels UPPERCASE), IBM Plex Mono (números apenas, menor que body).
4. ✅ **1 accent `clay #b85c38`** — usado em 3 sítios apenas (sugestão: chart line principal + 1 KPI delta importante + 1 link "ver todas").
5. ✅ **Voz PT-BR**: "Início", "Decisões pendentes", "Frente ao IBOV", "Cinco anos", "27 de abril", "Pergunta ao acervo", nunca "Home/Actions/vs/5y/Apr 27/Ask".

## Output esperado (entregables da sessão)

1. **`proto_inicio_v2_serena.html`** — variante 1 standalone, viewable em browser.
2. **`proto_inicio_v2_densa.html`** — variante 2 standalone.
3. **Notas de implementação** (opcional — texto dentro do canvas):
   - Quais helpers do `_components.py` precisam refactor para esta page funcionar.
   - Tokens novos *justificados* (se algum) — mas régua: refactor estrutura primeiro.
   - Mapping aproximado: cada secção do HTML ⇒ widget Streamlit ou helper.

Guardar exports em:
```
C:\Users\paidu\investment-intelligence\obsidian_vault\_assets\
  └─ proto_inicio_v2_serena.html
  └─ proto_inicio_v2_densa.html
  └─ proto_inicio_v2_serena.png  (screenshot)
  └─ proto_inicio_v2_densa.png   (screenshot)
```

## Próximo passo após esta sessão

1. **User escolhe** uma das duas variantes (serena/densa) como default.
2. **Helena review** — confirma 0 violações DS001-DS009 (Helena Mega audit).
3. **Handoff a Claude Code** (esta CLI) com prompt:
   > "Helena aprovou `proto_inicio_v2_<choice>.html`. Implementa como nova `Início` em `scripts/dashboard_app.py`, refactorando `_components.py` para v2.0 (kpi_tile, story_card, verdict_pill, section_header). Cria `scripts/_editorial.py` com `inject_editorial_css()`, `EDITORIAL_TEMPLATE` (Plotly), `lede()`, `eyebrow()`, `section_h()`. Anti-padrões DS001-DS009 banidos."
4. **Após implementação**: deprecar Captain's Log page (já dentro da Home) ou simplificar (fica como drill-down "Captain's Log completo").

## Cross-links

- [[Brain_Map]] — contexto integrado (lê primeiro)
- [[Design_System_v2]] — tokens + tipografia + anti-padrões
- [[../_assets/proto_home_v1_c|Proto C aprovado em 26-04]] — referência visual
- [[../_assets/proto_home_v1_INDEX]] — porque C ganhou
- [[Claude_Design_Integration]] — workflow geral Claude Design

---

> *"A página que mostro ao meu pai sem precisar de explicar."* — North Star
