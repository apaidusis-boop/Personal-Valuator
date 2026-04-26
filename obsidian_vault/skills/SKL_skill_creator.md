---
type: skill
tier: S
skill_name: skill-creator
source: anthropics/skills
status: backlog
sprint: W.4
tags: [skill, tier_s, meta, skill_creator]
---

# 🛠️ Skill Creator (Anthropic)

**Repo**: https://github.com/anthropics/skills (subfolder `skill-creator`)
**Fit**: 🎯 **Crítico** — meta-skill. Sem isto, skills customizadas nossas ficam ad-hoc.

## O que faz
Skill oficial que ensina Claude a criar **outras skills**: frontmatter correcto, descrição que dispara bem, estrutura `SKILL.md + files/`, testing pattern. Output é um skill pronto para `~/.claude/skills/`.

## Por que é o mais importante para nós
Temos pelo menos **4 workflows** que seriam skills óbvias:
1. `drip-analyst` — sempre que user pergunta "quanto rende X em DRIP", aplica `scripts/drip_projection.py` + lógica do `CLAUDE.md`
2. `panorama-ticker` — orquestra `ii panorama X` + narra em PT com tone do user
3. `rebalance-advisor` — lê `portfolio_positions` + targets + macro regime + sugere trades
4. `macro-regime` — classifica BR+US regime + flaga sectors em alerta

Se criarmos estas skills, **qualquer Claude session futura** usa-as automaticamente sem o user pedir explicitamente. Ganho composto.

## Sprint W.4 — plano
1. Instalar skill-creator em `~/.claude/skills/`
2. Criar `drip-analyst` skill (caso piloto — mais bem definido):
   - SKILL.md: quando disparar, input esperado, output formato
   - files/: reference `CLAUDE.md` critérios BR/US, linka `scripts/drip_projection.py`
3. Testar: abrir Claude session, perguntar "quanto me rende TFC em 10y DRIP?" → skill dispara sozinho
4. Iterar nos outros 3 skills seguindo o mesmo pattern
5. Decidir local: `.claude/skills/` (project-scoped, versiona em git) vs `~/.claude/skills/` (global)
   - **Recomendação**: project-scoped (versionar, ser explícito)

## Template esperado
```markdown
---
name: drip-analyst
description: Use this skill when the user asks about DRIP projection for a ticker
  they hold or watch (BR or US market). Applies Buffett/Graham criteria from
  CLAUDE.md and invokes scripts/drip_projection.py.
---

# DRIP Analyst

[Instruções + referências a ficheiros]
```

## Riscos
- **Skill bloat**: criar 20 skills → overlap + confusão sobre qual dispara. Começar com 4 e consolidar.
- **Description quality**: se descrição fraca, skill nunca dispara. Test-driven: afirmar prompts que DEVEM disparar e prompts que NÃO devem.

## Blockers
Nenhum. Pode começar assim que anthropics/skills repo for clonado.

## Links
- [[Roadmap]] — Sprint W.4 tem este skill como fundação
- [[SKL_pdf_processing]] — usar pattern semelhante para integrar Claude PDF skill condicionalmente
