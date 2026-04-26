---
type: skill_group
tier: C
status: deferred
tags: [skill, tier_c, skip, catalogs]
---

# 🗑️ Tier C — Skip (não fit para investment-intelligence)

Skills boas por mérito próprio mas fora do escopo deste projeto. **Documentadas aqui para não re-avaliar em sessões futuras.**

---

## Skills skip

### gstack (Garry Tan)
**Repo**: https://github.com/garrytan/gstack
**O que é**: startup tech stack template (Next.js + auth + billing + ...).
**Por que skip**: não estamos a construir SaaS. Investment-intelligence é ferramental pessoal.

### PPTX (Anthropic skill)
**Repo**: anthropics/skills
**Por que skip**: não geramos apresentações. Reports → markdown + Obsidian.

### Remotion
**Repo**: https://github.com/remotion-dev/remotion
**O que é**: programmatic video rendering em React.
**Por que skip**: não geramos vídeos. Se um dia quisermos auto-gerar "weekly portfolio recap" em vídeo, voltar aqui.

### Canvas Design (Anthropic skill)
**Por que skip**: não fazemos design work.

### Marketing Skills (Corey Haines)
**Repo**: https://github.com/coreyhaines31/marketing-...
**Por que skip**: não é produto comercial. Sem marketing.

### Claude SEO (AgriciDaniel)
**Repo**: https://github.com/AgriciDaniel/claude-seo
**Por que skip**: vault é pessoal, não público. Sem SEO.

### Brand Guidelines (Anthropic skill)
**Por que skip**: não temos brand. Investment-intelligence é tooling, não produto.

### Langflow
**Repo**: https://github.com/langflow-ai/langflow
**O que é**: visual LLM workflow builder.
**Por que skip**: overkill para nosso uso. `agents/` framework + scripts Python cobrem. Langflow faria sentido se quiséssemos expor workflows a non-devs.

### container-use (Dagger)
**Repo**: https://github.com/dagger/container-use
**O que é**: sandbox containerizado para agents.
**Por que skip**: uso pessoal single-machine. Sandboxing é overhead sem ganho real. Revisitar se executar código não-confiável.

### Ghost OS (ghostwright)
**Repo**: https://github.com/ghostwright/ghost-os
**O que é**: agent OS / framework experimental.
**Por que skip**: `agents/` framework já funciona. Ghost OS é alpha e overkill.

### Figma skills (loaded mas não relevantes)
**O que são**: skills para Figma design automation (figma-use, figma-generate-library, figma-implement-design, etc.).
**Por que skip**: investment-intelligence não tem design deliverables em Figma. Skills estão loaded no harness mas nunca vão disparar aqui.

---

# 📚 Catálogos — monitorizar mensalmente

Para descobrir skills novas que apareçam após esta avaliação (2026-04-24).

### Official Anthropic Skills Repo
**URL**: https://github.com/anthropics/skills
**O que é**: repo canónico. Todos os `document-skills/*` vêm daqui.
**Monitorizar**: novos commits ao `main` branch.

### Awesome Claude Skills
**URL**: https://github.com/travisvn/awesome-claude-skills (URL base, pattern awesome-*)
**O que é**: community-curated list.
**Monitorizar**: releases do README.

### SkillsMP
**URL**: https://skillsmp.com
**O que é**: skill marketplace (commercial).
**Monitorizar**: secção free + top-downloaded.

### SkillHub
**URL**: https://skillhub.club
**O que é**: outro marketplace.
**Monitorizar**: categoria finance/research.

### MAGI Archive (tom-doerr)
**URL**: https://tom-doerr.github.io/repo_posts/
**O que é**: curated repo posts, não especificamente skills mas vale watch.
**Monitorizar**: weekly.

---

## Sprint W.7 — Catalog Monitoring Agent

Plano para automatizar este monitoring:
- Novo agent `agents/skill_scout.py`
- Cron mensal (dia 1 de cada mês)
- Scrape diffs vs baseline mensal anterior
- Output → `obsidian_vault/skills/_monthly_YYYY-MM.md`
- Se skill nova tem >80% fit score (heurística), Telegram alert

---

## ✅ Ficheiros desta secção

- [[_MOC]] — índice completo skills
- [[Roadmap]] — Phase W plano
- [[SKL_pdf_processing]] [[SKL_xlsx]] [[SKL_obsidian_kepano]] [[SKL_playwright_mcp]] [[SKL_tavily]] [[SKL_firecrawl]] [[SKL_skill_creator]] — Tier S
- [[SKL_tier_A]] — research + agent ops
- [[SKL_tier_B]] — nice-to-have
- **Este ficheiro** — Tier C skip + catalogs
