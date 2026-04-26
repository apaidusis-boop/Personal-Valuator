---
type: skill_group
tier: B
status: backlog
sprints: [revisit_Q3]
tags: [skill, tier_b, nice_to_have]
---

# 🥉 Tier B — Nice-to-have

Skills com valor potencial mas não resolvem dor imediata. **Revisitar trimestralmente.**

---

## Superpowers (obra/superpowers)
**Repo**: https://github.com/obra/superpowers
**O que faz**: coleção de general Claude Code enhancements (commands, hooks, workflows).
**Fit**: médio. Alguns commands podem ser úteis (ex: auto-commit patterns).
**Decisão**: **cherry-pick** — ler README, importar 1-2 commands que fitam. Não adoptar bulk.

---

## Context Optimization (muratcankoylan)
**Repo**: https://github.com/muratcankoylan/agent-... (URL truncada)
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
**Fit**: baixo. Temos Streamlit (`ii dashboard`).
**Quando faria sentido**: se quisermos um dashboard static HTML sem Streamlit deps.
**Decisão**: **skip**, revisitar se Streamlit começar a pesar.

---

## Frontend Design (Anthropic skill)
**Repo**: https://github.com/anthropics/skills (subfolder)
**O que faz**: skill para design system / UI components.
**Fit**: baixo. Streamlit não precisa design system custom.
**Quando faria sentido**: se migrarmos dashboard para Next.js/React.
**Decisão**: **skip**.

---

## 📊 Resumo Tier B

| Skill | Adopt? | Quando revisitar |
|---|---|---|
| Superpowers | Cherry-pick | Next session |
| Context Optimization | Leitura inspiração | Quando agent bloat |
| n8n | Skip | Se multi-SaaS integration |
| claude-squad | Skip | Se `agents/` insuficiente |
| Doc Co-Authoring | Skip | Nunca (não fit) |
| Web Artifacts | Skip | Se ditch Streamlit |
| Frontend Design | Skip | Se rewrite dashboard em React |
