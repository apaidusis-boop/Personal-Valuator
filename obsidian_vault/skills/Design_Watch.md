---
type: design_watch
updated: 2026-04-25
owner: helena_linha
tags: [design, watch, research, helena]
---

# Design Watch — Helena Linha continuous scout

> Auto-refreshed weekly. Last run: **2026-04-25**. Total finds: **6** (5 install / 1 consider).

## Currently installed (`~/.claude/skills/`)

- `huashu-design`
- `hue`
- `ui-ux-pro-max-skill`

## New: install tier

Stars ≥1000, design-relevant description, pushed in window.

| Repo | Stars | Pushed | Description |
|---|---:|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 21832 | 2026-04-25 | The design language that makes your AI harness better at design. |
| [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 16060 | 2026-04-24 | Turn Claude Code into a full game dev studio — 49 AI agents, 72 workflow skills, and a complete coordination system mirr |
| [OpenCoworkAI/open-codesign](https://github.com/OpenCoworkAI/open-codesign) | 2246 | 2026-04-24 | Open-source Claude Design alternative. One-click import your Claude Code / Codex API key. Prompt → prototype / slides /  |
| [KAOPU-XiaoPu/web-design](https://github.com/KAOPU-XiaoPu/web-design) | 187 | 2026-04-16 | A Claude Code SKILL for designing beautiful, consistent web pages — spec first, code second. |
| [likaku/Mck-ppt-design-skill](https://github.com/likaku/Mck-ppt-design-skill) | 109 | 2026-04-21 | Consulting firm-style PowerPoint design system for AI agents. 70 layout patterns, flat design, python-pptx. 麦麸风格PPT设计系统。 |

## New: consider tier

Stars ≥100 (or ≥5 with strong design keyword). Helena triages.

| Repo | Stars | Pushed | Description |
|---|---:|---|---|
| [AgriciDaniel/skill-forge](https://github.com/AgriciDaniel/skill-forge) | 48 | 2026-04-10 | Ultimate Claude Code skill creator — design, scaffold, build, review, evolve, and publish production |

## Helena's recommendation this week

**Top pick**: [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable) (21k stars, pushed today). Tagline: "the design language that makes your AI harness better at design". É exactamente a categoria do `hue` mas com 45× mais stars e tracking activo. **Próxima instalação que proponho** — re-avaliar na próxima semana com teste A/B contra hue.

**Watch**: [`KAOPU-XiaoPu/web-design`](https://github.com/KAOPU-XiaoPu/web-design) (187 stars) — "spec first, code second" ressoa com a regra "design review pré-merge" que estabeleci. Pequeno o suficiente para inspeccionar antes de instalar.

**Defer**: [`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios) (16k) — fora de scope (game dev, não investing). [`OpenCoworkAI/open-codesign`](https://github.com/OpenCoworkAI/open-codesign) (2.2k) — alternative harness, heavy install.

**Curiosidade**: [`likaku/Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) (109) — McKinsey-style PPT design system com python-pptx. Útil se a Vitória decidir fazer quarterly deck. Bookmark, não instalar agora.

## Notes

- Source: GitHub search API. Queries in `scripts/design_research.py::SEARCH_QUERIES`.
- Adicionar repo à blacklist: editar `KNOWN` no script.
- Rate limit 60/h sem token; 5000/h com `GITHUB_TOKEN`.
- Log: `logs/design_research.log`