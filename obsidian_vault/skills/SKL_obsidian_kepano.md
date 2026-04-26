---
type: skill
tier: S
skill_name: obsidian-skills
source: kepano/obsidian-skills
status: backlog
sprint: W.3
tags: [skill, tier_s, obsidian, pkm, vault]
---

# 📓 Obsidian Skills (kepano)

**Repo**: https://github.com/kepano/obsidian-skills
**Autor**: Steph Ango (kepano), CEO Obsidian
**Fit**: 🎯 **Altíssimo** — nosso vault tem 53 wiki + 35 tickers + 20 sectors. Falta disciplina PKM canónica.

## O que faz
Coleção de skills que ensinam Claude a trabalhar com um vault Obsidian seguindo patterns testados: MOC (Maps of Content), evergreen notes, atomic notes, PARA, Johnny Decimal. Inclui templates e convenções de naming.

## Onde integra
- **Refactor `Home.md`**: hoje é lista extensa; kepano sugere 3-pane (Start / Explore / Workflows)
- **Refactor `wiki/Index.md`**: promover MOC pattern real (vs apenas index tabular)
- **Ticker notes**: adicionar campo `status: seedling / budding / evergreen` no frontmatter → filtrar em Dataview
- **Notas órfãs**: kepano tem script para detectar, adaptar em `scripts/memory_cleanup.py --vault`
- **Daily notes**: vault já tem `2026-04-23.md` solto — formalizar pattern de daily + templates

## Sprint W.3 — entregáveis concretos
1. Ler os 5-10 skills do kepano em detalhe (cada um é uma convention)
2. Aplicar **1 convention por vez**, medir adesão:
   - evergreen status em tickers/ (quais 35 estão realmente maduros?)
   - MOC real em wiki/ (Index.md → _MOC.md hub com queries Dataview)
   - naming: `YYYY-MM-DD` strict em briefings/
3. Atualizar `scripts/obsidian_bridge.py` para respeitar novas conventions

## O que NÃO fazer
- **Migration big-bang**: 53 wiki + 35 tickers = semanas se re-escrever tudo. Aplicar a novos + migrar os antigos on-touch
- **Copiar kepano 1:1**: ele é PKM pessoal; nosso vault é ferramental investment. Filtrar.

## Blockers
Nenhum. Sprint de leitura + aplicação gradual.
