---
type: design_system
owner: helena_linha
version: v1.0
created: 2026-04-25
tags: [design, system, principles, helena]
---

# Investment Intelligence — Design System v1.0

> Helena Linha · 2026-04-25
> Esta nota é a constituição visual da casa. Toda página, briefing,
> componente e chart passa por aqui antes de existir.

## 5 princípios (não-negociáveis)

### 1 — Hierarquia tipográfica > cor

Tamanho, peso e espaço resolvem 80% do problema visual *antes* de inventar
uma cor nova. Quando vejo um chart com 5 séries pintadas em vermelho-amarelo-verde-azul-roxo, o autor está a tentar suprir falta de hierarquia com paleta. Cortar séries, agrupar em "outros", ou separar em dois charts.

**Aplicar quando**: reviewer abre um chart e os olhos não sabem onde pousar primeiro. Resposta nunca é "mais cor"; é "subir 2pt no que importa, baixar 2pt no resto".

### 2 — Paleta restrita, sempre

5 cores no inventário. Mais que isto não é design, é decoração.

| Token | Hex | Uso exclusivo |
|---|---|---|
| `--accent` | `#4f8df9` | Highlight primário, links, CTA, série principal |
| `--positive` | `#4ade80` | Ganhos, screen pass, fresh, healthy |
| `--negative` | `#f87171` | Perdas, distress, stale, broken |
| `--warning` | `#fbbf24` | Mid-tier, atenção, soft alert |
| `--amethyst` | `#a78bfa` | 5ª categoria em charts (raramente) |

Neutros: `--bg #0f1115`, `--surface #161a22`, `--surface-2 #1d2330`, `--border #222833`, `--text #e6e8eb`, `--muted #7a8290`.

**Regra dura**: se um componente novo precisa de uma cor que não está aqui, é a estrutura que está errada, não a paleta.

### 3 — Whitespace é informação, não preenchimento

Espaço diz "isto agrupa, aquilo separa". Não é desperdício; é semântica.

- Entre KPIs relacionados: 12-16px.
- Entre secções: 32-48px (margem dura).
- Padding interno de card: 14px 18px (vertical mais apertado que horizontal — lê melhor).
- Captions a 0.82rem (vs body 1rem) — bate hierarquia sem precisar de cor.

**Heurística**: se está apertado, comprime ainda mais um lado e abre o outro. Distribuição uniforme de margens é o sinal de quem não decidiu.

### 4 — Emojis só em badges semânticos

Permitido: ✅ ❌ ⚠️ 🟢 🟡 🔴 — quando carregam estado (pass/fail/warn).

Proibido: emojis em headings, captions, labels de coluna, page titles.

> "🎯 Actions Queue 🚀" é decoração; "Actions Queue" + badge ✅ ao lado de cada item é semântica.

**Razão**: emojis em headings competem com tipografia pela atenção e empilham visual debt. Em badges são funcionais (read in 50ms).

### 5 — Default dark, números sempre tabulares

O founder lê de noite. Dark é menos cansativo em sessões longas com tabelas densas.

Toda tabela e todo metric value usa `font-feature-settings: "tnum" 1` em ui-monospace. Sem isto, números como `1,234` e `5,678` desalinham vertical e o olho perde a leitura comparativa.

**Texto continua sans-serif** (system-ui). Só **números** em mono. Misturar mostra cuidado e separa "narrativa" de "data" sem precisar de border.

---

## Padrões UX para AI agentic

> Destilado de [Smashing — UX Patterns para AI agentic](https://smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/) e [Transparency Moments Part 1](https://smashingmagazine.com/2026/04/identifying-necessary-transparency-moments-agentic-ai-part1/). Aplicação directa à nossa Actions Queue, perpetuums T2-T5, e qualquer surface onde um agente da casa propõe acção autónoma ao founder.

### Os 3 momentos de transparência obrigatórios

Quando um agente da casa propõe ou executa algo, o founder *tem que* ver:

1. **Why** — qual o sinal/evidência. Nunca "Helena recomenda X". Sempre "Helena recomenda X *porque* Y".
2. **What** — exactamente o que vai acontecer. "Refazer o chart com paleta nova" ≠ "Re-renderizar 4 charts em obsidian_vault/markets/BR.md, sobrescrevendo PNGs existentes".
3. **Who paid** — qual perpetuum/agente disparou e em que tier de autonomia (T1=auto, T5=requer aprovação).

**Aplicação**: toda linha da Actions Queue mostra `proposed_by · tier · why_one_liner`. Toda notificação Telegram tem footer com agente + tier.

### Control patterns (Smashing #2)

Em ordem de blast radius:

| Acção | Padrão | Onde |
|---|---|---|
| Read-only (digest, score recompute) | T1 — silent, log only | perpetuums data_coverage, thesis |
| Local write (vault note, DB row) | T2 — propose, founder one-click approve | actions_queue |
| External write (Telegram push, email) | T3 — explicit consent per-action | notifiers |
| Money-adjacent (suggest trade) | T5 — never auto, always memo first | rebalance_advisor |

**Regra**: nunca subir um tier sem actualizar este quadro primeiro.

### Consent fatigue mitigation

Se o founder tem que aprovar 20 actions iguais, o sistema falhou — não a UX.

- **Bulk approve** quando 5+ actions partilham `kind`. "Aprovar todos os 12 trigger:price_drop?"
- **Standing rules** ("sempre aprovar `vault.update_freshness` para holdings").
- **Threshold defaults** — actions com `confidence ≥ 0.85` e `blast_radius == 'local'` saltam aprovação.

---

## Princípios de implementação

### Plotly

- Toda figura: `template="ii_dark"` (default em `scripts/_theme.py`). Nunca usar `plotly_white`, `plotly_dark` cru, ou colorscale rainbow.
- Categórico: `colorway=CATEGORICAL` (5 cores). Se precisas de mais, refactor; não alongues a paleta.
- Continuous: gradiente single-hue (`Blues_r` ou custom mono). Nunca `Viridis`/`Plasma` em portfolio data.
- Eixos: `gridcolor=border`, sem `zeroline`. Margins: `l=8 r=8 t=36 b=8`.

### Streamlit

- `inject_css()` é obrigatório no topo de toda page nova, *depois* de `st.set_page_config`.
- Não usar `st.metric` cru — passa pelo helper `kpi_tile()` em `_components.py`.
- Captions ≤ 8 palavras, factuais. "Saúde dos 9 perpetuums autónomos. Verde=funcional, vermelho=stale" → "Health · 9 perpetuums".
- Page titles em sentence case sem emoji ("Actions queue", não "🎯 Actions Queue 🚀").

### Vault notes (markdown)

- Frontmatter sempre presente, com `type`, `owner`, `tags`.
- H1 = título da nota. H2 = secção principal. H3 = subsecção. Não saltar níveis.
- Tabelas com headers em **Title Case** ("Ticker", "Sector", "Market value"). Não Lowercase, não UPPER.
- Callouts apenas para info crítica (`> [!warning]`, `> [!info]`). Diluído perde sinal.

### Charts em vault

- PNGs gerados via `analytics/charts.py` com template `ii_dark`. Nunca screenshot.
- Tamanho fixo: 1200×600 (16:8) para chart standalone, 1200×400 (3:1) para sparkline header.
- Ficam em `obsidian_vault/_assets/`, referência relativa.

---

## Componentes reutilizáveis

> Implementação em `scripts/_components.py`. Importar de lá; não copiar HTML inline em pages.

| Componente | Função | Uso |
|---|---|---|
| `kpi_tile(label, value, delta=None, footnote=None, tone="neutral")` | Card métrico com left-accent | Dashboards, briefings |
| `status_pill(text, tone)` | Badge inline (positive/negative/warning/neutral) | Tabelas, listas |
| `section_header(title, caption=None)` | H2 + caption opcional, espaçamento consistente | Início de cada secção |
| `agent_attribution(agent, tier, why)` | Footer "by Helena · T2 · because Y" | Actions, notifications |
| `divider(label=None)` | Separador horizontal com label opcional | Entre secções densas |

---

## Anti-padrões (apanhados em audits)

1. **Headers com emoji-prefix** ("🎯", "📊", "💼") — corte sumário.
2. **`st.metric` cru** — usar `kpi_tile()` para consistência.
3. **Charts com >5 séries** — refactor obrigatório (agrupar em "Outros" ou separar).
4. **Captions condescendentes** ("zero tokens Claude", "9 perpetuums autónomos") — info arquitectural não é label.
5. **Mistura de tom** — ou tudo PT-PT formal, ou tudo casual; não trocar mid-page.
6. **Tabelas com gradient verde-amarelo-vermelho em todas as células** — uso de cor é binário (pass/fail) ou axial (1 dimensão), nunca ornamental.
7. **Cores fora dos 5 tokens** — se inventaste hex, refactor.
8. **Approver flow sem `why`** — toda Actions Queue row precisa de one-liner de justificação.

---

## Versionamento

- v1.0 (2026-04-25) — esta nota. Princípios + UX patterns AI agentic + componentes catalogados.
- Próxima revisão: 2026-05-09 (após 2 weeks de uso real e Design_Watch acumulado).

## Changelog

- 2026-04-25 — first cut. Helena.

---

> **Ler também**: [[Helena Linha]] (persona) · [[Design_Watch]] (research weekly) · [[Claude_Design_Integration]] (Anthropic Labs prototyping fit) · [[CONSTITUTION]] (não-negociáveis da casa)
