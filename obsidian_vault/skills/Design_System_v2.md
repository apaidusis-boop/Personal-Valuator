---
type: design_system
version: v2.0
owner: helena_linha
philosophy: kenya_hara_muji
created: 2026-04-26
supersedes: Design_System.md (v1.0)
tags: [design, system, helena, hara, editorial]
---

# Design System v2.0 — Editorial / Hara / Banca Privada

> Helena Linha · 2026-04-26
> Substitui v1.0 após aprovação do utilizador no protótipo `proto_home_v1_c.html`.
> Filosofia: **NÃO É DASHBOARD. É um documento.**

## Princípios (NÃO-NEGOCIÁVEIS)

1. **Voz humana sobre label/value**. A página abre com uma *lede sentence* completa, não com stat bar.
2. **Cream warm `#f4eee5`** é a tradição visual de relatórios financeiros impressos (Itaú PB, Pictet, Suno em alguns documentos). Não é "fashion choice".
3. **Source Serif 4** para títulos e body. Mono SÓ em números, em tamanho menor que o texto.
4. **1 accent terracotta `#b85c38`** usado com extrema disciplina (3 sítios por página max).
5. **Voz PT-BR completa**: "Início" não "Home", "Pergunta" não "Ask", "Frente ao IBOV" não "vs IBOV", "Cinco anos" não "5y".
6. **Datas formato pt-BR** (`02·04·2026` ou `02 de abril`).
7. **Espaço respira**. Margens generosas, vertical rhythm 48px+ entre secções.

## Paleta — 11 tokens (extensão justificada vs v1.0)

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

**Diferença vs v1.0**: dark theme abandonado. Paleta agora é warm/cream para alinhar com tradição editorial financeira.

## Tipografia

3 famílias com role explícito:

| Família | Role | Onde |
|---|---|---|
| **Source Serif 4** | Títulos, body, lede, ticker names | Headlines (italic 700, optical-size 60), body (400, opsz 30), nav active (italic) |
| **Inter** | UI micro-labels, eyebrows | UPPERCASE 9-11px tracked .2em, table headers, captions |
| **IBM Plex Mono** | Números | 13-14px (menor que body 15px), tabular-nums forced |

**Regra**: mono nunca domina. Os números servem o texto, não vice-versa.

## Spacing scale

- Vertical rhythm: **48px+** entre secções principais
- Inter-section: **32px**
- Within section: **18-24px**
- Margens main: **56-80px** horizontal (generosas)

## Chart conventions

- Bg = `paper` (não brancos puros, não dark)
- Lines: 0.5-1.1px (thin, ink-line)
- 1 line highlighted em `clay`, restantes em `ink` muted (opacity 0.4)
- IBOV/index: dotted 0.5px em `muted`, opacity 0.5
- Single horizontal grid line em base 100, `rule` width 0.6
- Year markers: serif italic 11px, `muted`
- Labels inline no fim das linhas (Tufte convention), serif italic ou mono pequeno

## Componentes (helpers em `scripts/_editorial.py`)

| Helper | Substitui |
|---|---|
| `inject_editorial_css()` | `_terminal.inject_terminal_css()` |
| `EDITORIAL_TEMPLATE` (Plotly) | `TERMINAL_TEMPLATE` |
| `lede(text)` | A lede sentence opening |
| `eyebrow(label)` | Pequena uppercase tracked |
| `hl(text)` | Big italic serif headline |
| `deck(text)` | Sub-headline em serif body |
| `section_h(title, deck)` | Section eyebrow + title |
| `quiet_stat(label, value, tone)` | Item da quiet stat grid |

## Anti-padrões — proibidos

❌ Hero number gigante (sem 56px+ de números soltos)
❌ Cards com `border-left:2px accent`
❌ Emojis como hierarquia
❌ Mistura de idiomas em UI strings
❌ Mono dominante em texto não-numérico
❌ Mais de 1 accent por página
❌ Voz de UI engineer ("Open Actions", "Last update")

## Cross-links
- [[../_assets/proto_home_v1_c|Protótipo C — Hara]]
- [[../_assets/proto_home_v1_INDEX|Index dos 3 protótipos]]
- [[Design_System|v1.0 deprecated]]
