---
type: folder_readme
purpose: design_assets_landing
owner: helena_linha
tags: [assets, design, prototypes, claude_design]
---

# `_assets/` — Design prototypes & visual exports

> Landing folder para HTML prototypes, screenshots, mockups, brand assets, e qualquer output de Claude Design / huashu-design / outras ferramentas de design.

## Convenção de nomes

```
proto_<page>_v<n>_<variant>.html        # standalone HTML viewable em browser
proto_<page>_v<n>_<variant>.png         # screenshot mesma proto, pra preview no vault
proto_<page>_v<n>_INDEX.md              # index quando há múltiplas variantes (a/b/c)
brand_<asset>.{svg|png}                 # logos, marcas, ícones
chart_<topic>_<date>.png                # PNG de chart standalone (se gerado fora do dashboard live)
```

**Exemplos actuais**:
- `proto_home_v1_a.html` — Tufte/Pentagram (rejeitado)
- `proto_home_v1_b.html` — Vignelli/Unimark (rejeitado)
- `proto_home_v1_c.html` — Hara/MUJI (✅ aprovado, base de Design_System v2.0)
- `proto_home_v1_INDEX.md` — análise comparativa das 3 direcções

## Política

1. **Source of truth do design não vive aqui** — vive em `obsidian_vault/skills/Design_System_v2.md` e em `scripts/_components.py` + `_editorial.py`. Esta folder é o *whiteboard*.
2. **HTML aqui nunca vai directamente para produção** — sempre passa por handoff a Claude Code, que respeita `_components.py` e tokens.
3. **Versionamento manual** — `v1`, `v2`, `v3`. Quando uma é aprovada como direcção, marca-a no nome ou no `INDEX.md`. Não apagar variantes rejeitadas (referência histórica).
4. **Brand spec sempre injectado em sessões Claude Design** — `Design_System_v2.md` cola-se como contexto inicial. Caso contrário, ferramentas externas inventam cores fora da paleta.

## Workflow típico

1. Brief escrito em `obsidian_vault/skills/Brief_<page>_<phase>.md`.
2. Sessão Claude Design — cola Brain_Map + Design_System_v2 + brief, itera no canvas.
3. Export → guarda HTML + PNG aqui com nome convencionado.
4. Helena review — confirma 0 violações DS001-DS009.
5. Handoff Claude Code — implementação Streamlit reusando `_components.py`.
6. Após implementação Streamlit: prototypes ficam aqui como referência histórica.

## Cross-links

- [[../skills/Brain_Map|🧠 Mapa do Cérebro]] — contexto integrado para AI externa
- [[../skills/Design_System_v2|Design System v2.0]] — paleta + tipografia + anti-padrões
- [[../skills/Claude_Design_Integration|Workflow Claude Design]]
- [[../skills/Brief_Home_U1|Brief — Início U.1]] — próxima sessão
