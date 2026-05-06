---
type: skill_group
tier: B
status: actively_curated
last_review: 2026-05-06
sprints: [revisit_quarterly]
tags: [skill, tier_b, nice_to_have, decision_log]
---

# 🥉 Tier B — Nice-to-have

Skills com valor potencial mas não resolvem dor imediata. **Revisitar trimestralmente.**

> **Última re-avaliação 2026-05-06**: 6 repos auditados em paralelo (Sonnet sub-agents). Re-avaliações marcadas com 🔁. Decisões persistidas em [[../CONSTITUTION#🧠 Decision Log]].

---

## Superpowers (obra/superpowers) 🔁
**Repo**: https://github.com/obra/superpowers
**O que faz**: coleção de SKILL.md prompts para Claude Code (debugging, planning, TDD, brainstorming, verification). Plugin que injecta via SessionStart hook.
**Decisão prévia (2026-04-24)**: cherry-pick 1-2 commands.
**Re-avaliação 2026-05-06**: **CHERRY-PICKED 5 patterns** (não wholesale install — SessionStart hook conflita com CLAUDE.md/Constitution authority chain).
- `systematic-debugging` → `.claude/commands/systematic-debugging.md` (4-phase protocol).
- `verification-before-completion` → 7º não-negociável + `.claude/commands/verification-before-completion.md`.
- `writing-plans` → `.claude/commands/writing-plans.md` (formato canónico p/ T3+ action_hints).
- `anthropic-best-practices.md` → DS010 + CH008 (skill files <500 linhas).
- `brainstorming` → memorando p/ futuro `[BRAINSTORM]` mode em `ii decide`.
- **Skip**: `using-git-worktrees` (bash-Unix), `dispatching-parallel-agents` (Claude API tokens), `test-driven-development` (data-pipeline code não fit).

---

## Context Optimization (muratcankoylan)
**Repo**: https://github.com/muratcankoylan/agent-... (URL truncada na fonte original)
**O que faz**: técnicas de redução de tokens em agent contexts.
**Fit**: médio. Nossos agents (Phase V) já usam `[[in-house first]]` pattern.
**Decisão**: ler para inspiração; adoptar patterns quando tivermos bloat real.

---

## n8n (workflow automation)
**Repo**: https://github.com/n8n-io/n8n
**O que faz**: visual workflow builder (tipo Zapier self-host) para orquestrar APIs.
**Fit**: baixo-médio. Já temos `scripts/` + scheduled tasks (`_schtasks_*.bat`).
**Quando faria sentido**: se user quer fluxos cross-service (Gmail alert → Telegram → SQL log) sem escrever Python.
**Decisão**: **skip for now**. Nossos schedule tasks + Python CLI cobrem 100% do que precisamos.
**Revisitar se**: user começar a pedir integrações com 3+ serviços externos SaaS.

---

## claude-squad (multi-agent)
**Repo**: https://github.com/smtg-ai/claude-squad
**O que faz**: orquestra múltiplos Claude agents em paralelo (tipo tmux para AI).
**Fit**: baixo. **Nosso `agents/` framework (Phase V) já resolve isto.**
**Decisão**: **skip**. Ler para ver se há patterns de orquestração que valem migrar para `agents/_runner.py`.

---

## Doc Co-Authoring (Anthropic skill)
**Repo**: https://github.com/anthropics/skills (subfolder)
**O que faz**: colaboração em docs (Google Docs-like).
**Fit**: muito baixo. Não fazemos docs colaborativos.
**Decisão**: **skip**.

---

## Web Artifacts Builder (Anthropic skill)
**Repo**: https://github.com/anthropics/skills (subfolder)
**O que faz**: gera artefactos web (mini-apps, dashboards) interactively.
**Fit**: baixo. Temos Mission Control Next.js (`localhost:3000`) que já cobre o use-case.
**Decisão**: **skip**, revisitar se precisarmos de artefactos descartáveis (one-off chart, demo).

---

## Frontend Design (Anthropic skill) 🔁
**Repo**: https://github.com/anthropics/skills/tree/main/skills/frontend-design
**O que faz**: prompt creative-direction para gerações UI one-shot (HTML/CSS/JS, React).
**Decisão prévia (2026-04-24)**: skip ("Streamlit não precisa design system custom").
**Re-avaliação 2026-05-06**: trigger atingido — **Mission Control Next.js é primary front-end** desde Phase EE; Streamlit phasing out. **PARTIAL ADOPT**:
- DS010 spatial-composition heuristic + skill-length linter (já implementados em `agents/helena/audit.py`).
- Dominant-colour + accent-weight guideline a documentar em `Design_System.md` (TODO próximo sprint).
- "Unforgettable one thing" framing como sprint-2 review checklist (memo em [[Mission_Control_Design_Roadmap]]).
- **Não copy**: tudo que conflita com Helena (DS001-009 já cobrem tokens, motion, dataviz, contracts).

---

## claude-mem (thedotmack/claude-mem) 🆕
**Repo**: https://github.com/thedotmack/claude-mem
**O que faz**: session-persistence layer (Node/Bun daemon + SQLite + Chroma vector). Captura tool-use observations passivamente, injecta context via SessionStart hook. Web UI :37777.
**Fit**: parcial — endereça gap "auto observation capture" mas existing system é mais auditável.
**Decisão (2026-05-06)**: **SKIP**. Existing memory file-based + MEMORY.md indexed + git-backed = mais auditável e curated. Sem decay/conflict-resolution upstream. AGPL + PolyForm Noncommercial em sub-deps adicional reason. **Pattern reusable**: replicar PostToolUse hook no `.claude/settings.json` se quisermos Stop-trigger.

---

## gstack (garrytan/gstack) 🆕
**Repo**: https://github.com/garrytan/gstack
**O que faz**: 23 skills + 8 power tools p/ Claude Code (sprint workflow think→plan→build→review→test→ship→reflect; design-taste decay model; /guard scope fence). Não é UI lib.
**Fit**: zero direct — Mission Control já tem scaffold. Cherry-picks lightweight only.
**Decisão (2026-05-06)**: **INSPIRAÇÃO ONLY**.
- `mission-control/DESIGN_TASTE.md` — preference journal v3 Broadsheet (lightweight, sem tooling).
- `/guard` scope fence convention — já alinhado com CLAUDE.md "Surgical changes" (sem novo file).
- Feed-forward planning doc pattern — convention CLAUDE.md (sem novo file).

---

## GitHub Code Review (features page) 🆕
**URL**: https://github.com/features/code-review
**O que faz**: marketing page de PR primitives + branch protection. Não é repo.
**Fit**: solo-developer adoptable items existem.
**Decisão (2026-05-06)**: **PARTIAL SETUP**.
- ✅ `.github/workflows/test.yml` (pytest, push+PR, weekly fallback p/ requirements UTF-16).
- ✅ `.github/workflows/codeql.yml` (Python static analysis, push+PR+weekly cron).
- TODO (manual user action via GitHub UI): branch protection on `main` requiring tests pass.
- **Skip**: Copilot Code Review (no subscription); team-facing features (review requests, granular permissions).

---

## claude-code-security-review (anthropics) 🆕
**Repo**: https://github.com/anthropics/claude-code-security-review
**O que faz**: GitHub Action + slash command + eval framework. 18 hard-exclusion rules para reduzir noise.
**Fit**: parcial — slash command form é zero-cost (só invocado on demand).
**Decisão (2026-05-06)**: **PARTIAL ADOPT**.
- ✅ `.claude/commands/security-review.md` — copiada (free, manual invoke).
- ✅ `agents/perpetuum/code_health.py::SKIP_PATTERNS` — 18 exclusões seeded como const (CH001-007 podem usar futuramente).
- **Skip**: GitHub Action mode (recurring Opus API cost, solo repo, no audience for PR comments).

---

## 📊 Resumo Tier B (post-2026-05-06)

| Skill | Decisão | Implementação | Próxima revisão |
|---|---|---|---|
| Superpowers | Cherry-pick (5 patterns) | ✅ slash cmds + DS010 + rule 7 | Quando novo skill upstream |
| Context Optimization | Inspiração | — | Quando agent bloat |
| n8n | Skip | — | Multi-SaaS demand |
| claude-squad | Skip | — | Se `agents/` insuficiente |
| Doc Co-Authoring | Skip | — | Nunca (no fit) |
| Web Artifacts | Skip | — | Mission Control replaceável |
| Frontend Design | Partial | ✅ DS010 + Design_System updates | v3 Broadsheet sprint 2 |
| claude-mem | Skip | — | Re-avaliar se existing memory bloat |
| gstack | Inspiração | DESIGN_TASTE.md only | Mission Control v4 |
| GitHub Code Review | Partial | ✅ test.yml + codeql.yml | User aplica branch protection UI |
| claude-code-security-review | Partial | ✅ slash cmd + SKIP_PATTERNS | CH integration sprint |
