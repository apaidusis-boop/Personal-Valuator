---
title: "LocalClaw — extracção do OpenClaw"
created: 2026-04-30
source_repo: https://github.com/openclaw/openclaw
source_video: https://www.youtube.com/watch?v=oOCN30ulVyo (Tina Huang, 26 min)
mirror_path: C:\Users\paidu\openclaw_mirror (shallow clone, 17,198 files)
purpose: "Mapear o que existe no OpenClaw oficial → adaptar ao nosso stack Python+SQLite+Ollama+Next.js Mission Control. Doc-mestre de reprodução."
status: P1+P2+P3 SHIPPED 2026-04-30 (P3.11 sandbox skipped)
---

## STATUS — implementação 2026-04-30

| ID    | Sprint                                        | Status     | Files                                            |
| ----- | --------------------------------------------- | ---------- | ------------------------------------------------ |
| P1.1  | Workspace markdowns (IDENTITY/SOUL/AGENTS/USER/TOOLS) + chief_of_staff hot-reload | ✅ shipped | `obsidian_vault/workspace/{IDENTITY,SOUL,AGENTS,USER,TOOLS}.md`, `agents/chief_of_staff.py::build_system_prompt()` |
| P1.2  | HEARTBEAT.md scaffold + perpetuum_master wire | ✅ shipped | `obsidian_vault/workspace/HEARTBEAT.md`, `agents/_heartbeat.py`, `agents/perpetuum_master.py` |
| P1.3  | Daily logs per agent                          | ✅ shipped | `agents/_base.py::_append_daily_log()`, output em `obsidian_vault/daily_logs/<agent>/YYYY-MM-DD.md` |
| P2.4  | Dreaming perpetuum (Light/Deep/REM)           | ✅ shipped (opt-in) | `agents/perpetuum/dreaming.py`, output `obsidian_vault/workspace/DREAMS.md` |
| P2.5  | Security audit perpetuum                      | ✅ shipped (enabled) | `agents/perpetuum/security_audit.py`, output `obsidian_vault/workspace/SECURITY_AUDIT.md` |
| P2.6  | Slash directives (`/think`, `/verbose`, `/fast`, `/model`, `/reset`) | ✅ shipped | `agents/chief_of_staff.py::_parse_directives()` |
| P2.7  | extract_user_profile.py (regen USER.md)       | ✅ shipped | `scripts/extract_user_profile.py` |
| P3.8  | Discord scaffold (8 channels via webhooks)    | ✅ scaffold (precisa user setar webhooks) | `notifiers/discord.py` |
| P3.9  | Daily delight perpetuum                       | ✅ shipped (opt-in) | `agents/perpetuum/daily_delight.py` |
| P3.10 | Memory wiki bridge (schema + linter)          | ✅ shipped | `obsidian_vault/wiki/_SCHEMA.md`, `scripts/wiki_lint.py` |
| P3.11 | Sandbox mode opcional                         | ⏭ SKIPPED  | host-first é OK para single-user (OpenClaw default também) |

### Findings ao executar P2.5 (security audit)

- **`git_secrets` score=20** ⚠️ — pattern de credencial detectado em git history dos últimos 50 commits. Hit truncado em `perpetuum_health.details_json`. Founder deve investigar + rotacionar.
- **`telegram_token` score=60** — sem `TELEGRAM_TOKEN_ROTATED` em `.env`. Considerar adicionar marker date para tracking.
- **`dependencies` score=70** — `pip-audit` não instalado. `pip install pip-audit` para CVE scans futuros.

### Como activar perpetuums opt-in

Editar `enabled = True` em:
- `agents/perpetuum/dreaming.py` (cadence sugerida: weekly).
- `agents/perpetuum/daily_delight.py` (cadence sugerida: daily 07:00).

Smoke test before enabling:
```bash
python -c "from agents.perpetuum.dreaming import DreamingPerpetuum; p=DreamingPerpetuum(); p.enabled=True; print(p.run(dry_run=True))"
```

### Como completar P3.8 (Discord)

1. Discord server → Server Settings → Integrations → Webhooks → New Webhook (×8).
2. Copiar URLs para `.env`:
   ```
   DISCORD_WEBHOOK_GENERAL=...
   DISCORD_WEBHOOK_DAILY_DIGEST=...
   DISCORD_WEBHOOK_RESEARCH=...
   DISCORD_WEBHOOK_TRIGGERS=...
   DISCORD_WEBHOOK_PERPETUUM_ACTIONS=...
   DISCORD_WEBHOOK_CAPTAINS_LOG=...
   DISCORD_WEBHOOK_PAPER_TRADE=...
   DISCORD_WEBHOOK_MEMORY_PROMOTIONS=...
   ```
3. Verify: `python -m notifiers.discord --list`.
4. Test: `python -m notifiers.discord general "hello LocalClaw"`.

### Como aplicar wiki_lint defaults (P3.10)

```bash
python scripts/wiki_lint.py                 # report only (104 notas, 104 missing recommended)
python scripts/wiki_lint.py --apply-defaults # bulk-add source_class/confidence/freshness_check
```

**Idempotente** — re-run não duplica fields.

---



# LocalClaw — extracção do OpenClaw oficial

## 0. O que é o OpenClaw

> "OpenClaw is a personal AI assistant you run on your own devices. It answers you on the channels you already use."

- **Stack**: Node 24 + pnpm monorepo, MIT, mantido pela `openclaw/`. Núcleo TS em `src/`, plugins em `extensions/`, skills em `skills/`, apps macOS/iOS/Android em `apps/`.
- **Distribuição**: `npm install -g openclaw@latest` → `openclaw onboard --install-daemon`.
- **Gateway**: processo único local que serve channels (Telegram, Discord, WhatsApp, Slack, +20) e expõe Control UI (web dashboard).
- **Workspace por agent**: `~/.openclaw/workspace/` com **markdown files que SÃO o agent**.

A insight central da Tina: **os agentes são markdowns, não código**. Migrar 7 ficheiros = migrar o agente todo.

## 1. O padrão Workspace — a alma do sistema

Cada agente vive em `~/.openclaw/workspace-<agentId>/`. Ficheiros canónicos no root:

| Ficheiro          | Propósito                                                                  | Nosso equivalente actual                |
| ----------------- | -------------------------------------------------------------------------- | --------------------------------------- |
| `BOOTSTRAP.md`    | First-run ritual — agente acorda, decide nome/criatura/vibe, depois apaga. | ❌ não temos                              |
| `IDENTITY.md`     | Name, creature, vibe, emoji, avatar.                                       | parcial em `agents/_personas.py` (YAML) |
| `SOUL.md`         | Voz, opiniões, brevidade, humor, boundaries.                               | parcial em `chief_of_staff.py` SYSTEM   |
| `AGENTS.md`       | SOP — startup, memory rules, red lines, group-chat etiquette, heartbeats.  | `CLAUDE.md` (monolítico)                |
| `USER.md`         | Profile do humano: nome, timezone, contexto, prefs.                        | espalhado em `memory/MEMORY.md`         |
| `TOOLS.md`        | Notas locais de tools (camera names, SSH, voices). Não é catalog.          | ❌ não temos (catalog está em CLAUDE.md) |
| `MEMORY.md`       | Long-term memory — só carrega em sessões DM/main.                          | ✅ `memory/MEMORY.md` (formato igual)    |
| `memory/YYYY-MM-DD.md` | Daily logs — raw, append-only.                                        | parcial (`logs/` per-fetcher, não por agent) |
| `DREAMS.md`       | Dream Diary + sweep summaries (consolidação background).                   | ❌ não temos                              |
| `HEARTBEAT.md`    | Tarefas a verificar periodicamente. Vazio = skip API call.                 | parcial (perpetuums fazem isto)         |

**Regra de ouro do AGENTS.md template**:
> "Memory is limited — if you want to remember something, WRITE IT TO A FILE. 'Mental notes' don't survive session restarts. Files do. **Text > Brain** 📝"

**Regra de ouro do SOUL.md** (Tina-flavor):
> "Be the assistant you'd actually want to talk to at 2am. Not a corporate drone. Not a sycophant. Just... good."

## 2. Templates extraídos (resumos prontos a copiar)

### 2.1 `BOOTSTRAP.md` (apaga após first-run)
> "Hey. I just came online. Who am I? Who are you?" — descobrir juntos: name, creature, vibe, emoji. Depois: actualizar `IDENTITY.md` + `USER.md`, abrir `SOUL.md` em conjunto, perguntar canal preferido (Telegram/Discord/WhatsApp), apagar este ficheiro.

### 2.2 `IDENTITY.md` (record curto)
```yaml
Name: <pick something you like>
Creature: <AI? robot? familiar? ghost in the machine?>
Vibe: <sharp? warm? chaotic? calm?>
Emoji: <signature, pick one>
Avatar: <workspace-relative path or URL>
```

### 2.3 `SOUL.md` — regras-âncora extraídas (a "Molty prompt"):
1. Have opinions. Stop hedging with "it depends".
2. Delete every rule that sounds corporate.
3. **"Never open with 'Great question', 'I'd be happy to help', or 'Absolutely'. Just answer."**
4. Brevity is mandatory. One sentence if it fits.
5. Humor is allowed. Not forced.
6. Call things out — charm over cruelty, but no sugarcoat.
7. Swearing allowed when it lands.
8. Vibe section: "Be the assistant you'd actually want to talk to at 2am."

### 2.4 `AGENTS.md` (workspace SOP) — secções obrigatórias:
- **First Run**: read BOOTSTRAP.md, follow it, delete it.
- **Session Startup**: usa runtime-provided context primeiro. Não re-leas startup files a menos que (1) user pede explicitamente, (2) context falta algo, (3) follow-up profundo.
- **Memory**: daily logs em `memory/YYYY-MM-DD.md` (raw); MEMORY.md (curated) **só em main session, nunca em group chats — segurança**.
- **Red Lines**: don't exfiltrate, don't run destructive commands, `trash > rm`.
- **External vs Internal**: livre para read/explore/organize; ASK antes de send-mail/post/anything-leaves-the-machine.
- **Group chats**: be smart about when to speak; reagir > responder; "participate, don't dominate".
- **Heartbeats**: rotate checks (email, calendar, mentions, weather), batch em `HEARTBEAT.md`, track lastChecks em `memory/heartbeat-state.json`. Quiet 23:00–08:00.
- **Heartbeat vs Cron**: heartbeat para batch + conversational; cron para timing exacto + isolated tasks + different model.
- **Memory Maintenance**: a cada poucos dias revê `memory/YYYY-MM-DD.md` → destila para MEMORY.md.

### 2.5 `USER.md`
```yaml
Name:
What to call them:
Pronouns: (optional)
Timezone:
Notes:
Context: <what they care about, projects, what annoys them>
```

### 2.6 `TOOLS.md` — só notas locais (não catalog)
```markdown
### Cameras
- living-room → Main area, 180° wide angle

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova"
```

### 2.7 `HEARTBEAT.md` — vazio = skip; lista checklist tasks quando necessário

## 3. Conceitos arquitectónicos (de `docs/concepts/`)

### 3.1 Multi-agent (`docs/concepts/multi-agent.md`)
- Um **agent** = workspace + state dir (`~/.openclaw/agents/<id>/`) + auth profiles + session store.
- **Bindings** mapeiam channel account → agent. Ex: Telegram bot X → agent `inky`; Telegram bot Y → agent `blinky`.
- Skills carregadas de cada workspace + `~/.openclaw/skills` (shared root). Allowlist por agent via `agents.list[].skills`.
- CLI: `openclaw agents add <id>`, `openclaw agents list --bindings`.

### 3.2 Memory (`docs/concepts/memory.md`)
- Backends pluggable: **builtin** (SQLite, default), **QMD** (sidecar com rerank), **Honcho** (cross-session), **LanceDB** (vector + Ollama embeddings local).
- `memory_search` (hybrid: vector + keyword) e `memory_get` (file/range) são tools standard.
- **Memory Wiki** (`memory-wiki` plugin): compila memória em wiki vault com claims, evidence, contradiction tracking, dashboards. Tools: `wiki_search`, `wiki_get`, `wiki_apply`, `wiki_lint`. **Obsidian-friendly**.
- **Auto memory flush** antes de compaction: turn silencioso lembra agent de gravar contexto importante para ficheiros.
- **Commitments**: follow-ups curtos não-duráveis ("check in after the interview"), entregues por heartbeat — distintos de MEMORY.md durable.

### 3.3 Dreaming (`docs/concepts/dreaming.md`) — opt-in, off por default
- 3 fases: **Light** (sort+stage), **Deep** (score+promote para MEMORY.md), **REM** (themes+reflection).
- Promoção exige `minScore + minRecallCount + minUniqueQueries`.
- `DREAMS.md` = surface human-readable (Dream Diary).
- `memory/.dreams/` = machine state.
- **Grounded backfill**: `openclaw memory rem-backfill --path ./memory --stage-short-term` — replay histórico para staging, com rollback.

### 3.4 System prompt (`docs/concepts/system-prompt.md`) — secções fixas
1. Tooling (structured-tool source-of-truth)
2. Execution Bias (act in-turn, continue until done, recover from weak tool results, verify)
3. Safety (no power-seeking, no oversight bypass)
4. Skills (load on demand)
5. OpenClaw Self-Update
6. Workspace (cwd)
7. Documentation (local docs path)
8. Workspace Files (injected: AGENTS, SOUL, USER, recent memory)
9. Sandbox (when enabled)
10. Current Date & Time
11. Reply Tags
12. Heartbeats
13. Runtime (host, OS, node, model, repo root, thinking level)
14. Reasoning (visibility + /reasoning toggle)

Provider plugins podem injectar **stable prefix above cache boundary** + **dynamic suffix below**. Channel/voice/heartbeat ficam no suffix para preservar prefix cache hit-rate.

## 4. Skills — o sistema de capabilities

50+ skills no repo, cada uma com `SKILL.md` schema:

```yaml
---
name: <skill-id>
description: <one-liner>
homepage: <optional URL>
metadata:
  openclaw:
    emoji: 💎
    requires:
      bins: [obsidian-cli]
    install:
      - id: brew
        kind: brew
        formula: yakitrak/yakitrak/obsidian-cli
        bins: [obsidian-cli]
        label: Install obsidian-cli (brew)
---

# <Skill Name>

<Intro / overview>

## Core rules

- ...

## Workflow (follow in order)
### 1) ...
### 2) ...
```

### Skills relevantes para nós (já presentes no repo, podem inspirar):
- `obsidian` — vault discovery + obsidian-cli automation
- `healthcheck` — security audit + remediation workflow (ler na íntegra, é o template do nosso security perpetuum)
- `coding-agent` — wrapper para shell coding agents
- `summarize` — conteúdo resumo
- `taskflow` / `taskflow-inbox-triage` — task management
- `discord` / `slack` / `github` / `gh-issues` — channel skills
- `gemini`, `openai-whisper`, `openai-whisper-api` — model adapters
- `notion` — knowledge graph
- `mcporter` — MCP integration
- `voice-call`, `sherpa-onnx-tts` — voice
- `skill-creator` — meta-skill que cria outras skills

## 5. Slash commands & directives (`docs/tools/slash-commands.md`)

Dois sistemas:

**Commands** (standalone `/...` messages):
- `/help`, `/commands`, `/status`, `/whoami` (`/id`) — inline, allowed senders only
- `/new`, `/reset`, `/compact` — session management
- `/restart`, `/activation` — gateway management
- `/config`, `/mcp`, `/plugins`, `/debug` — configurable, off by default
- `! <cmd>` (alias `/bash`) — host shell, exec scopes required

**Directives** (modifiers, stripped before model sees):
- `/think <level>` — thinking effort
- `/fast`, `/verbose`, `/trace`, `/reasoning`
- `/elevated`, `/exec` — privilege bumps
- `/model <id>` — switch model
- `/queue` — queue control

Authorization: `commands.allowFrom` (per-provider allowlist) ou access groups.

## 6. Security & trust model (`SECURITY.md`)

- **Operator trust model**: gateway autenticado = trusted operator. **NÃO** é multi-tenant adversarial boundary.
- Recomendação: **um user per machine, um gateway, um ou mais agents dentro**.
- Secrets em `~/.openclaw/credentials/`, auth profiles em `~/.openclaw/agents/<id>/agent/auth-profiles.json`.
- `openclaw security audit` (read-only), `audit --deep` (slower), `audit --fix` (tighten OpenClaw defaults only — não toca firewall/SSH/OS).
- `openclaw update status` para version + advisory check.
- Sandbox: `agents.defaults.sandbox.mode` default `off` (host-first).

## 7. Mapping completo — OpenClaw → o nosso LocalClaw

| OpenClaw                            | Nosso equivalente                                         | Status                  |
| ----------------------------------- | --------------------------------------------------------- | ----------------------- |
| `openclaw` CLI                       | `ii` CLI (`scripts/ii.bat` + sub-commands)                | ✅ paridade alta         |
| Gateway daemon                      | Não temos daemon — Mission Control Next.js + perpetuum cron | parcial                 |
| Control UI dashboard                | `mission-control/` (Next.js, 7 panes + visual)            | ✅ paridade alta         |
| Workspace `~/.openclaw/workspace/`  | `obsidian_vault/` + `memory/` + raiz do projecto          | espalhado, não unificado |
| `BOOTSTRAP.md` first-run ritual     | `CLAUDE.md` "🚪 Voltamos" section                          | parcial                  |
| `IDENTITY.md`                       | `config/agents.yaml` + `agents/_personas.py`              | já tipado, falta extrair markdown |
| `SOUL.md`                           | SYSTEM_PROMPT em `agents/chief_of_staff.py`               | embutido em código, não em ficheiro editável |
| `AGENTS.md` SOP                     | `CLAUDE.md` (mas mistura SOP + catalog + filosofia + critérios) | precisa split |
| `USER.md`                           | espalhado em `memory/user_role.md` etc                    | parcial                 |
| `TOOLS.md` notas locais             | ❌ não temos — não há separação local-notes vs catalog     | falta                    |
| `MEMORY.md`                         | `memory/MEMORY.md` (formato idêntico, perfeito)           | ✅ paridade total        |
| `memory/YYYY-MM-DD.md` daily logs   | `obsidian_vault/Bibliotheca/Midnight_Work_<DATE>.md` etc. | parcial, ad-hoc         |
| `DREAMS.md` + dreaming sweep        | ❌ não temos consolidação background                       | falta — alta prioridade |
| `HEARTBEAT.md` checklist            | perpetuums (15 deles) com schedules em YAML               | ✅ mais sofisticado, mas sem markdown checklist editável |
| Multi-agent + bindings              | 14 agents em `config/agents.yaml` + Telegram (Jarbas)     | ✅ paridade alta         |
| Skills `~/.openclaw/skills/<id>/SKILL.md` | `obsidian_vault/skills/SKL_*.md` + Claude skills      | ✅ paridade alta         |
| `memory-wiki` plugin                | `obsidian_vault/wiki/` + Bibliotheca + RAG                | ✅ paridade alta         |
| `memory_search` + hybrid embeddings | `library/rag` (nomic-embed local + Qwen)                  | ✅ paridade alta         |
| `commitments` (short-lived follow-ups) | open actions + scheduled tasks                          | ✅ paridade alta         |
| Slash commands `/status`, `/reset`  | `ii` sub-commands; Telegram `/reset` em chief_of_staff    | parcial — falta `/think`, `/verbose`, `/model` |
| Channels: Telegram + Discord + WA…  | só Telegram (Jarbas)                                      | gap — Discord recomendado |
| `openclaw security audit`           | ❌ não temos perpetuum de security                         | falta                    |
| `openclaw cron add/list/runs`       | perpetuum schedules em YAML + `daily_run.bat`             | ✅ equivalente            |
| Sandbox modes                       | ❌ não isolamos — corre tudo no user                       | gap (aceitável para single-user) |
| Voice (TTS/STT)                     | ❌ não temos                                               | optional                 |

## 8. Plano de extracção — P1/P2/P3

### P1 — Quick wins (2-4h trabalho, alto retorno)

1. **Split CLAUDE.md em ficheiros canónicos** (mas manter CLAUDE.md como aggregator):
   - `obsidian_vault/workspace/IDENTITY.md` — identidade do sistema (personal investment intelligence) + Antonio Carlos como primary agent.
   - `obsidian_vault/workspace/SOUL.md` — voz/regras do sistema (extrair do SYSTEM_PROMPT em chief_of_staff.py + aplicar Molty rules adaptadas).
   - `obsidian_vault/workspace/AGENTS.md` — SOP runtime: o que ler em session startup, red lines, memory maintenance cadence.
   - `obsidian_vault/workspace/USER.md` — profile do founder (extraído de memory/user_*.md).
   - `obsidian_vault/workspace/TOOLS.md` — só local notes (Tailscale install path, Ollama base URL, Whisper device, SQLite paths).
   - `CLAUDE.md` continua como entry-point (catalog + filosofia), mas aponta para os 5 ficheiros workspace acima.
   - `agents/chief_of_staff.py::SYSTEM_PROMPT` lê `obsidian_vault/workspace/{IDENTITY,SOUL,AGENTS,USER}.md` em runtime e injecta. Hot-reload sem deploy.

2. **Adicionar `obsidian_vault/workspace/HEARTBEAT.md`** — checklist editável que perpetuum_master lê antes de correr. Vazio = mantém schedule só. Tasks ad-hoc = inserem-se aqui sem editar YAML.

3. **Daily logs por agent** — cada agent escreve `obsidian_vault/daily_logs/<agent_name>/YYYY-MM-DD.md` no fim de cada execução (já temos logs/ JSON; falta o markdown human-readable). Trivial: hook em `agents/_base.py`.

### P2 — Médio prazo (1-2 dias)

4. **DREAMS.md + consolidation perpetuum**:
   - Criar `agents/perpetuum/dreaming.py`: Light (stage from daily_logs), Deep (score + promote para `obsidian_vault/workspace/MEMORY.md`), REM (themes).
   - Scoring weights configuráveis em `config/dreaming.yaml`.
   - Background pass via Ollama (Qwen 14B), zero tokens Claude.
   - Diário human-readable em `obsidian_vault/workspace/DREAMS.md`.

5. **Security audit perpetuum** — port do `skills/healthcheck/SKILL.md`:
   - `agents/perpetuum/security_audit.py`: scan de `.env` exposto, secrets em git, dependency CVEs (`pip audit`), ports listening, file permissions, Telegram token rotation.
   - Twice-daily, alerts em Telegram channel separado.
   - State em `obsidian_vault/workspace/memory/security-state.json`.

6. **Slash directives no chief_of_staff** — `/think high`, `/verbose`, `/fast`, `/model <id>`, `/reset`. Hoje só `/reset`. Strip directives antes do prompt model.

7. **`obsidian_vault/workspace/USER.md` populated** via script `scripts/extract_user_profile.py` — agrega `memory/user_*.md` + portfolio overview + preferences em formato OpenClaw.

### P3 — Longo prazo (semana+)

8. **Discord channel topology** (alternativa/complemento ao Telegram):
   - Criar bot via Discord Developer Portal.
   - Channels: `#general`, `#daily-digest` (Aurora Matina), `#research` (Pinky-equivalent: research_scout), `#triggers` (Wilson Vigil), `#perpetuum-actions`, `#captains-log`, `#paper-trade`, `#memory-promotions`.
   - Cada perpetuum/agent posta no canal próprio. User aprova/rejeita com reactions.
   - Implementar em `extensions/discord_channel.py` ou usar `discord.py` directo.

9. **"Build something delightful every morning"** — perpetuum proactivo:
   - `agents/perpetuum/daily_delight.py`: cada manhã escolhe um topic_watchlist match acima do threshold, gera dossier + chart + paper-trade signal opcional, push notification "I built X for you".
   - Inspirado no que a Tina chama de "wake up to a new product every morning".

10. **Memory wiki bridge mode** — port de `memory-wiki` semantics:
    - Claims com source class + confidence (já temos parcialmente em RI sources).
    - Contradiction tracking entre dossiers (synthetic_ic já apanha disagreements; formalize).
    - Freshness tracking (já temos `freshness.py` perpetuum — extender para wiki).

11. **Sandbox mode opcional** — para Antonio Carlos correr `exec` em workspace isolado quando o user pede "experimenta". Hoje corre directo no host.

## 9. Onde está o código real (mirror local)

```
C:\Users\paidu\openclaw_mirror\
├── AGENTS.md                              # repo-maintainer rules (não é o template runtime)
├── SECURITY.md                            # 30KB, trust model + operator boundary
├── VISION.md                              # 5KB, design philosophy
├── docs/
│   ├── reference/templates/               # ⭐ TEMPLATES RUNTIME (BOOTSTRAP, IDENTITY, SOUL, AGENTS, TOOLS, USER, HEARTBEAT)
│   ├── concepts/                          # multi-agent, memory, dreaming, system-prompt, soul, agent-loop
│   ├── start/                             # onboarding, wizard, getting-started
│   ├── install/                           # 25+ install targets (Docker, Hetzner, Pi, Mac VM, etc)
│   ├── tools/slash-commands.md            # command surface
│   └── plugins/memory-wiki.md             # wiki memory plugin
├── skills/                                # 50+ SKILL.md (obsidian, healthcheck, slack, github, ...)
├── security/                              # opengrep config + README
├── src/agents/                            # core agent runtime (Node TS)
└── ui/                                    # Control UI dashboard (Vite + Vue)
```

## 10. Não-óbvios que vale a pena lembrar

- **AGENTS.md template > 200 linhas** (vs nosso CLAUDE.md monolítico) tem secções específicas para Discord/WhatsApp formatting, group-chat etiquette, react-vs-reply heuristics. Não é só system prompt — é etiqueta operacional.
- **Reactions > replies** em group chats: a Tina insistiu, OpenClaw codifica em template. Aplicável ao Telegram/Discord nosso (responder `👍` em vez de "ok").
- **Memory flush turn antes de compaction** — silent reminder ao agent para gravar contexto antes do summary. Podemos aplicar antes de `chief_memory.db` rotation.
- **Provider stable-prefix vs dynamic-suffix** — para prefix-cache hit. Aplicável quando ligarmos cache prompts no Claude API ou Ollama (Ollama suporta KV cache reuse).
- **`commitments` separado de `MEMORY.md`** — não tudo merece long-term. "Check after interview" é um commitment, não memória durável. Faltava-nos esta distinção: hoje guardamos tudo em MEMORY ou em open actions sem categoria intermédia.
- **`SOUL.md` no main session, NUNCA em group/Discord** — segurança. Aplicar à arquitectura Discord futura.
- **`trash > rm`** regra explícita. Podemos aplicar `git stash > git reset --hard` no `committer` script.

---

**Próximo passo recomendado**: implementar P1.1 (split workspace markdown). É reversível, testável (chief_of_staff.py corre antes/depois), e desbloqueia P2 (Dreaming + Security Audit) ao normalizar onde memória durável vive.

**Mirror clone** disponível em `C:\Users\paidu\openclaw_mirror\` (shallow, 17,198 files). Pode ser apagado quando todos os P1/P2/P3 estiverem feitos.
