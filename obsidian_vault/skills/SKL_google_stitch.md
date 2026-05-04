---
type: skill_assessment
tier: B
status: evaluated
source_video: https://www.youtube.com/watch?v=sjL61D3oybY
video_id: sjL61D3oybY
video_channel: Wanderloots
video_duration_min: 21
ingested: 2026-04-28
owner: helena_linha
tags: [skill, design, stitch, google, mcp, vibe_design, phase_z, phase_u]
---

# 🎨 SKL · Google Stitch + Vibe Design

> Avaliação após ingestão do vídeo "Vibe Design First THEN Build Apps" (Wanderloots, 21min). Pipeline `yt_ingest.py` correctamente devolveu 0 insights de investimento — vídeo é puro design tooling. Esta nota captura a aplicabilidade ao **Escritório** (Phase Z/U + Helena Linha).

## TL;DR

- **Stitch** = ferramenta Google AI gratuita de design UI/UX com canvas infinito, exporta `design.md` (markdown blueprint) + HTML.
- **Conceito-chave**: "Vibe Design First, THEN Vibe Code." Design phase explícita antes de codar — fecha o gap entre o que imaginas e o que o LLM implementa.
- **MCP Server nativo** — Stitch tem MCP que liga bidirectionalmente a Claude Code / Antigravity / Cursor. Permite `pull` de mudanças no design para o coding agent e vice-versa.
- **Validação arquitectural, não inovação para nós**: Helena Linha já existe exactamente porque "engenheiros não escolhem cores". `Design_System.md` + `_components.py` + Tone Literal **são** o nosso `design.md`. O vídeo confirma a tese.

## O que o vídeo apresenta

### Conceitos
1. **Vibe Design vs Vibe Coding** — Design phase é primeira; LLM codifica errado se a visualização do humano está vaga.
2. **`design.md` como blueprint portátil** — markdown único que armazena colors, typography, spacing rules, component definitions. Qualquer agent que leia, constrói consistente.
3. **Bi-directional vs one-way export** — Google AI Studio é one-way push (perde-se sync depois); MCP é round-trip.

### Stitch features
- Modos: Gemini Flash (HTML quick), Gemini Pro (complex), **Redesign** (Nano Banana, screenshot→design), **ID8** (problem→plan), **Live** (chat real-time).
- **URL color extraction** — paste URL, extrai paleta + typography. Útil para herdar branding existente.
- **Instant prototype** — costura todas as screens em preview clicável; mobile/tablet/desktop responsive.
- **Imagine new screen** — agent sugere screen baseada no contexto, gera + integra na navegação.

### Export targets
- **Google AI Studio** (one-way, ~5min para 1 page; sufoca em 5+ pages).
- **MCP** (Antigravity, Claude Code, Cursor) — bi-directional, permite ciclo design↔code.
- Figma, Jules, ZIP, clipboard.

## Aplicabilidade ao projecto

### ✅ Onde encaixa hoje

| Phase | Como Stitch ajuda | Custo |
|---|---|---|
| **U.1 Home minimalista** | Mockup Apple-Newsroom-style em Stitch antes de implementar em Streamlit. 30min spike risk-free. | 0 (Stitch grátis) |
| **U.6 Telegram visual card** | Mockup do daily push card (matplotlib output PNG) — Stitch gera referência visual primeiro. | 0 |
| **Mega Helena spike** | 5ª path nos 4-path spikes existentes (`agents/helena_mega.py`). Output em `obsidian_vault/skills/Helena_Mega/03_Spikes/stitch.md`. | 0 |
| **W.2 MCP harness arsenal** | Stitch MCP é candidato para integrar (`.claude/mcp.json`). Mas só DEPOIS de Playwright/Firecrawl/Bigdata wired — esses dão dado de investimento, Stitch dá design. | priority B |

### ❌ Onde NÃO encaixa

- **L1 (verdade SQLite/YAML)** — irrelevante.
- **CLI `ii *`** — Constitution: terminal = sala-do-chefe, optimiza velocidade não estética. Stitch é Escritório-only.
- **Dados sensíveis (portfolio, theses)** — Stitch é cloud Google. Constitution não-negociável #1 (in-house first) impede feed de portfolio/theses para Stitch. **Apenas mockups visuais genéricos** podem ir.
- **Substituir Helena Linha** — `_components.py` + `Tone Literal` em compile-time são moat anti-AI-slop que Stitch não dá. Stitch gera HTML/CSS sem garantia de paleta restrita.

## Mapping `design.md` (Stitch) ↔ `Design_System.md` (Helena)

| Stitch `design.md` campo | Equivalente nosso |
|---|---|
| Colors palette | `scripts/_theme.py::COLORS` + `helena.css` tokens |
| Typography rules | `helena.css` font stack + `_components.py` text helpers |
| Component definitions | `scripts/_components.py` (`kpi_tile`, `story_card`, `verdict_pill`, etc.) |
| Spacing rules | helena.css gap tokens |
| Overall vibe/tone | `obsidian_vault/skills/Design_System.md` v1/v2 (5 princípios + 8 anti-padrões) |

**Conclusão**: temos paridade estrutural completa. Se um dia migrarmos para Stitch como source-of-truth, conversão é mecânica.

## Recomendações concretas (auto mode action items)

1. **Não instalar Stitch MCP agora**. Razões: (a) Tavily/Bigdata.com ainda não totalmente wired, ROI investimento > UI; (b) bidirectional MCP só vale a pena se o user adoptar Stitch como ferramenta diária — hoje Helena Linha ad-hoc é suficiente.

2. **Sim explorar Stitch para U.1 Home spike**. Custo zero, Apple-Newsroom-style é o sweet spot do Stitch. Output: 1 mockup PNG em `obsidian_vault/skills/Mockups/Home_U1_stitch.png`.

3. **Adicionar entry em Design_Watch.md** — Stitch entra na lista de ferramentas observadas, não na lista instaladas.

4. **Testar `design.md` como formato canónico** — exportar nosso `Design_System.md` para o formato Stitch `design.md` e ver se Stitch consegue construir um mockup respeitando a nossa paleta. Se sim, validamos roundtrip.

5. **Skip os outros tools mencionados** — Antigravity, Google AI Studio. Claude Code já é o coding agent; não duplicar.

## Anti-recomendações

- **NÃO migrar Streamlit para output do Stitch**. Stitch produz HTML/JSX. Nosso stack é Python+Streamlit por razão (subprocess para CLI canónica, deploy local). Refactor seria semanas com zero ganho de função.
- **NÃO usar Stitch para wire-frame de dashboards de dados reais**. Cloud Google = data egress. Use só para shells/layouts genéricos.
- **NÃO comprar narrativa "vibe code é gap de design"** ao pé da letra. Para nós o gap maior é **dados/critérios**, não UI. UI é polish phase, dados é core.

## Cross-links

- [[Design_System]] — DS principles atuais
- [[Design_System_v2]] — evolução
- [[Brain_Map]] — onde UI encaixa
- [[Helena_Mega/00_MASTER]] — pipeline existente de spikes
- [[../CONSTITUTION#🛡️ Os 6 não-negociáveis]] — in-house first regra

## Source

- **Vídeo**: [Wanderloots — Vibe Design First THEN Build Apps](https://www.youtube.com/watch?v=sjL61D3oybY) (2026, 21min, EN)
- **Transcript local**: `data/yt_transcript_sjL61D3oybY.txt` (25,907 chars)
- **DB row**: `videos.video_id='sjL61D3oybY'` em `data/us_investments.db`
- **Ingest log**: insights=0 themes=0 (correcto — vídeo é design, não investment)
