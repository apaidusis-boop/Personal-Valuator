---
type: skill_curation
updated: 2026-04-25
owner: helena_linha
tags: [skills, curation, helena, mega]
---

# 02 — Skill curation

> Helena Mega · run **2026-04-25** · 39 candidatos avaliados · **4** install / **16** consider / **19** skip

## Princípio

Excesso de skills = AI slop. Cada install adiciona context que disputa atenção; 5 skills bem usadas > 30 instaladas. Critério hard:

1. **Preenche um gap real** que o arsenal in-house não cobre
2. **Manutenção activa** (commit em ≤180 dias)
3. **Não duplica** capability já existente
4. **Domain fit** — investment intelligence, design, ou developer workflow

## Arsenal in-house (referência)

Capabilities que já temos — **não recomendar duplicados**:

| Capability | Onde |
|---|---|
| YouTube ingestion local | `scripts/yt_ingest.py` (Phase Q v2) |
| RAG semantic search | `library/rag` (nomic-embed local + Qwen) |
| Knowledge graph | `obsidian_vault` + `library/ingest` |
| Method extraction (Buffett/Druck/…) | `library/extract_insights` |
| Synthetic IC debate | `agents/synthetic_ic.py` |
| Telegram push | `notifiers/telegram.py` + Jarbas bot |
| Design System v1.0 | `obsidian_vault/skills/Design_System.md` |
| Design tokens / CSS | `scripts/_theme.py` |
| Reusable components | `scripts/_components.py` |
| Hi-fi prototyping | `huashu-design` skill |
| Style/palette/typography DB | `ui-ux-pro-max-skill` |
| Design language generator | `hue` skill |
| Figma toolkit | `figma:figma-*` skills |
| Perpetuum / autonomy | `agents/perpetuum_master.py` (Phase X) |

## INSTALL (4)

_Instalar (ou já instalado e em uso). Preenche gap real._

| Skill | Categoria | Fit | Razão |
|---|---|---:|---|
| **[hue (dominikmartn)](https://github.com/dominikmartn/hue)** | design | 100 | Already in ~/.claude/skills/. Confirm it's the latest version. Generates design language skills from references. |
| **[huashu-design](https://github.com/alchaincyf/huashu-design)** | design | 100 | Already installed. Hi-fi prototyping + 5 streams × 20 philosophies + video export. Underused — should be Helena's go-to for protótipos. |
| **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** | design | 100 | Already installed. 67 UI styles + 161 palettes + 57 font pairs. Use as reference DB when picking variants for new pages. |
| **[designer-skills (julianoczkowski)](https://github.com/julianoczkowski/designer-skills)** | design | 88 | 7 skills mapping a real design process (research → wireframe → high-fi → handoff). Helena flow currently jumps from brief to code; this gives her the missing intermediate stages. |

## CONSIDER (16)

_30-min spike antes de decidir. Risco de duplicar ou ser overhead._

| Skill | Categoria | Fit | Razão |
|---|---|---:|---|
| **[CCHooks (GowayLee)](github GowayLee/CCHooks)** | hooks | 72 | Python equivalent of johnlindquist. Better fit for our stack; could trigger `python -m agents.helena.audit` on PreToolUse Edit/Write to scripts/. |
| **[Skill Seekers (yusufkaraaslan)](https://github.com/yusufkaraaslan/Skill_Seekers)** | dev | 68 | Auto-generates a skill from any docs site/PDF. Concrete use: feed it Bigdata.com docs + yfinance docs + brapi.dev docs to get 3 lookup skills. 1h test before committing. |
| **[awesome-claude-skills (BehiSecc)](https://github.com/BehiSecc/awesome-claude-skills)** | catalog | 60 | Curated index. Use as discovery, not install. Re-scan monthly via Helena scout. |
| **[interface-design (Dammyjay93)](https://github.com/Dammyjay93/interface-design)** | design | 58 | Scope claims 'interface design'. Need to read SKILL.md before deciding — risk of overlap with huashu-design prototyping mode. |
| **[OneDrive/Claude/Skills/design-system](C:/Users/paidu/OneDrive/Claude/Skills/design-system)** | design | 55 | Local copy with components/layouts/showcase/themes/tokens. Audit overlap with our Helena Design System v1.0 — keep best. |
| **[Snyk — Top Claude Skills for Finance/Quant](https://snyk.io/pt-BR/articles/top-claude-skills-finance-quantitative-developers/)** | finance | 55 | Article (not a skill repo). Triage 2-3 specific skills it recommends; install only if they touch DCF, screener or risk. |
| **[Systematic Debugging Skill](superpowers (obra))** | dev | 55 | Forces root-cause analysis vs random fixes. Aligned with founder's preference (memory: 'feedback_inhouse_first'). |
| **[awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills)** | catalog | 55 | Second curated index. Cross-reference with BehiSecc's. |
| **[awesome-claude-code (hesreallyhim)](https://github.com/hesreallyhim/awesome-claude-code)** | catalog | 55 | Hooks-focused index. Use when we decide on hook strategy. |
| **[OneDrive/Claude/Skills/theme-factory](C:/Users/paidu/OneDrive/Claude/Skills/theme-factory)** | design | 50 | Has theme-showcase.pdf — read it; if useful, integrate as reference for Path B (Tauri) theme rollout. |
| **[CC Notify (desktop notifications)](awesome-claude-code (hesreallyhim))** | hooks | 48 | Desktop notification on completion. Overlaps with our Telegram push (notifiers/telegram.py); could complement it for in-front-of-PC sessions. |
| **[Web Asset Generator (icons, OG, PWA)](awesome-claude-skills (BehiSecc) / travisvn)** | productivity | 45 | If we go Path B (Tauri) or Path C (Next.js), need favicon, icons, OG tags. Install only when we commit to a path with web/web-app surface. |
| **[johnlindquist/claude-hooks](https://github.com/johnlindquist/claude-hooks)** | hooks | 42 | TypeScript hook framework. Useful if we want to enforce Helena audit on save. But adds a TS dependency to a Python project — evaluate cost/benefit. |
| **[Webapp Testing with Playwright](awesome-claude-skills (BehiSecc))** | dev | 42 | E2E testing. Becomes relevant if we go Path B (Tauri) or Path C (Next.js); already have SKL_playwright_mcp.md noted. |
| **[OneDrive/Claude/Skills/Front Design (frontend-design.md)](C:/Users/paidu/OneDrive/Claude/Skills/Front  Design)** | design | 40 | Single .md skill. Open and audit before deciding. |
| **[Claudio (Christopher Toth — sound effects)](github Christopher Toth Claudio)** | hooks | 35 | OS-native sounds on Claude events. Cosmetic but mildly useful for long perpetuum runs (overnight). |

### Duplicações detectadas (consider)

- **interface-design (Dammyjay93)** ↔ huashu-design app prototyping mode covers similar ground.
- **OneDrive/Claude/Skills/design-system** ↔ Helena Design_System.md v1.0
- **OneDrive/Claude/Skills/theme-factory** ↔ scripts/_theme.py defines our tokens already
- **CC Notify (desktop notifications)** ↔ notifiers/telegram.py
- **Webapp Testing with Playwright** ↔ obsidian_vault/skills/SKL_playwright_mcp.md (already evaluated)

## SKIP (19)

_Não instalar — duplica capability existente, fora de scope, ou abandonware._

| Skill | Categoria | Fit | Razão |
|---|---|---:|---|
| **[Superpowers (obra)](https://github.com/obra/superpowers)** | dev | 22 | Brainstorming + TDD enforcement + execution planning. Overkill for a 1-dev personal project; we already have perpetuums for structured work. |
| **[CFO Connect — Claude for Finance Teams](https://www.cfoconnect.eu/resources/event-recaps/claude-for-finance-teams/)** | finance | 20 | Talk recap, not code. Extract 2-3 patterns into vault if any stand out, no install needed. |
| **[Brainstorming Skill](superpowers (obra))** | research | 20 | Structured brainstorming. We have agents/synthetic_ic.py (Buffett+Druck+Taleb+Klarman+Dalio debate) which is more domain-specific. |
| **[Test-Driven Development Skill](superpowers (obra) / awesome-claude-skills)** | dev | 20 | TDD enforcement. Personal project; tests exist where they matter (analytics, scoring), not blanket. |
| **[Superpowers Lab (obra)](https://github.com/obra/superpowers-lab)** | dev | 18 | Bleeding-edge fork of Superpowers. Same reason to skip. |
| **[fcakyon Code Quality Hooks](awesome-claude-code (hesreallyhim))** | hooks | 18 | Linting + TDD enforcement collection. Too generic; we'd want Helena audit specifically on UI files, not blanket TDD. |
| **[Finishing a Development Branch Skill](awesome-claude-skills (BehiSecc))** | dev | 18 | PR cleanup workflow. We use small commits + manual PR; minor friction not worth a skill. |
| **[Tapestry (knowledge graph from PDFs)](awesome-claude-skills (BehiSecc))** | research | 15 | Builds knowledge graphs from PDFs. We already have library/rag (nomic-embed local) + Obsidian vault + library/ingest pipeline. |
| **[Content Research Writer (citations)](awesome-claude-skills (BehiSecc))** | research | 15 | Adds citations + iterates. Not a writing-heavy workflow here; founder writes own theses, agents generate structured memos. |
| **[bartolli TypeScript Quality Hooks](awesome-claude-code (hesreallyhim))** | hooks | 15 | TypeScript-specific. Out of scope unless we go Path B (Tauri) or Path C (Next.js); revisit then. |
| **[Git Worktrees Skill](awesome-claude-skills (BehiSecc))** | dev | 15 | Multi-branch worktrees. Solo dev on main most of the time. |
| **[EPUB / PDF Analyzer](awesome-claude-skills (BehiSecc))** | research | 12 | Summarizes/queries ebooks. We have library/extract_insights (Ollama local) — similar with Buffett/Klarman/Druckenmiller playbook lens. |
| **[YouTube Transcript / Article Extractor](awesome-claude-skills (BehiSecc))** | research | 10 | Claude-side YouTube ingestion. We have scripts/yt_ingest.py v2 (Phase Q) — local Whisper + Ollama, zero tokens. |
| **[codeinbox/claude-code-discord](https://github.com/codeinbox/claude-code-discord)** | hooks | 10 | Discord/Slack notification. We already use Telegram (Phase V Jarbas bot). |
| **[Pypict (combinatorial testing)](awesome-claude-skills (BehiSecc))** | dev | 10 | Generates QA test matrices. Heavy infra for personal scope. |
| **[Invoice / File Organizer](awesome-claude-skills (BehiSecc))** | productivity | 5 | Organizes receipts/invoices. Out of scope for investment intelligence project. |
| **[claude-code-hooks-sdk (beyondcode)](github beyondcode/claude-code-hooks-sdk)** | hooks | 5 | PHP/Laravel-style. Not our stack. |
| **[ffuf_claude_skill](awesome-claude-skills (BehiSecc))** | security | 2 | Security fuzzing. Out of scope for investment intelligence. |
| **[Defense-in-Depth Skill](awesome-claude-skills (BehiSecc))** | security | 2 | Multi-layer security. Out of scope. |

### Duplicações detectadas (skip)

- **Superpowers (obra)** ↔ agents/perpetuum_master.py + Plan mode
- **Brainstorming Skill** ↔ agents/synthetic_ic.py
- **Superpowers Lab (obra)** ↔ agents/perpetuum_master.py
- **Tapestry (knowledge graph from PDFs)** ↔ library/rag, library/ingest, obsidian_vault
- **EPUB / PDF Analyzer** ↔ library/ingest + library/extract_insights
- **YouTube Transcript / Article Extractor** ↔ scripts/yt_ingest.py, scripts/yt_reextract.py, scripts/yt_digest.py
- **codeinbox/claude-code-discord** ↔ notifiers/telegram.py + Jarbas bot

## Próximas acções (proposta Helena)

1. **Confirmar in-place** — `huashu-design`, `hue`, `ui-ux-pro-max-skill` estão em `~/.claude/skills/`. Helena começa a usá-los activamente em todo prototype novo (ver `Claude_Design_Integration.md`).
2. **Instalar `julianoczkowski/designer-skills`** — adiciona o process (research → wireframe → high-fi → handoff) que a casa não tem.
3. **30-min spikes (em paralelo, baixo custo)**:
   - `Dammyjay93/interface-design` — abrir SKILL.md, comparar com huashu-design
   - OneDrive/{design-system, theme-factory, Front Design} — auditar conteúdo, promover o útil para `obsidian_vault/skills/`
   - `Skill_Seekers` — 1 teste real: gerar skill a partir de docs `brapi.dev`
   - `CCHooks` (Python) — wire `python -m agents.helena.audit` em PreToolUse hook
4. **Adiar até decidir Path A/B/C/D**:
   - Web Asset Generator (só relevante se houver web surface)
   - Playwright skills (só relevante para Path B/C)
   - bartolli TS hooks (só relevante para Path B/C)
5. **Definitivamente não instalar** — todos os SKIP acima. Razões na tabela.

## Cross-links

- [[Design_Watch]] — re-scan semanal automático de novos repos
- [[Claude_Design_Integration]] — Anthropic Labs prototyping flow
- [[Helena Linha]] — owner
