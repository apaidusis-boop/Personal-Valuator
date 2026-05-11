---
name: perpetuum-review
description: Use this skill when the user wants to review open perpetuum
  actions (proposed by T2+ perpetuums) and approve/reject them individually.
  Triggers on phrases like "revisar ações", "o que o perpetuum propôs",
  "aprovar ação X", "ignore Y", "que sugestões tenho", "perpetuum review",
  "list pending actions", "show me open actions". Lists actions created by
  data_coverage, vault, or thesis perpetuums with status=open and walks the
  user through approve/reject/defer. Uses scripts/perpetuum_action_run.py
  for execution (only whitelisted commands run automatically).
---

# Perpetuum Review Skill

UX for T2 autonomy tier — user reviews what perpetuums have proposed
and decides per-action what to do. Respects safety: only whitelisted
commands execute automatically.

## When to trigger

- "Revisar ações perpetuum"
- "Que sugestões o sistema tem?"
- "Perpetuum review"
- "Aprovar X" / "Approve action 23"
- "Ignorar Y" / "Reject action 42"
- "O que está pendente"

Do NOT trigger for:
- Ticker-specific questions (use panorama-ticker)
- Running perpetuum itself (just run `python agents/perpetuum_master.py`)

## Workflow

### Step 1 — List open actions

```bash
python scripts/perpetuum_action_run.py list-open
```

Output shows table with: ID, market, perpetuum kind, score, ticker/subject, action_hint preview.

### Step 2 — For each action, present choice

For each open action, show the user:
- **Subject** + **score** (e.g., "br:IVVB11 — score 33/100")
- **Why flagged** (from flags in snapshot)
- **Proposed action** (the command or hint)
- **Risk level** (auto from action type):
  - Whitelisted command → "SAFE_AUTO" (can run via skill)
  - Non-command hint (e.g. "REVIEW + add context") → "MANUAL_REVIEW"
  - Destructive → "BLOCKED" (never auto)

### Step 3 — User decides (per action)

Valid decisions:
- **"approve 23"** → runs `python scripts/perpetuum_action_run.py 23` (only if whitelisted)
- **"approve all safe"** → bulk approve all whitelisted (ask confirm once if >3)
- **"ignore 42"** → marks status='ignored' via action_cli.py
- **"defer 42"** → leaves open (no-op, will re-surface next review)
- **"note 42 '<text>'"** → adds context note, leaves open

### Step 4 — After execution

Show delta:
- Exit code of each approved command
- Fresh perpetuum score (re-run `python agents/perpetuum_master.py --only <perpetuum>`)
- Proves the action fixed the problem (score should go up)

## Example interaction

User: "Revisar ações perpetuum"

Skill internal:
1. `python scripts/perpetuum_action_run.py list-open`
2. Parse table → 33 open actions from data_coverage (scores 33-66)
3. Group by perpetuum, show top 5 per group
4. Narrate:

```
Temos 33 ações abertas do perpetuum data_coverage (fundamentals incompletos).

### Top prioritárias (score mais baixo):

**ID 47** — br:IVVB11 — score 33/100
- Flags: 4 sinais em falta (fundamentals stale, sem dy_history, sem streak, ...)
- Proposto: `python fetchers/yf_deep_fundamentals.py IVVB11`
- Risk: SAFE_AUTO ✅

**ID 48** — br:KLBN11 — score 33/100
- Flags: 4 sinais em falta (mesmo padrão)
- Proposto: `python fetchers/yf_deep_fundamentals.py KLBN11`
- Risk: SAFE_AUTO ✅

**ID 49** — br:LFTB11 — score 33/100
- ...

### Opções
- `approve 47` — corre agora (safe)
- `approve all safe` — corre os 3 de score 33
- `ignore 47 "reason"` — marca ignored
- `defer 47` — volta a ver amanhã
```

User: "approve all safe"

Skill: confirms, runs each, reports results, suggests re-running perpetuum to see score go up.

## Critical rules

- **NEVER auto-run non-whitelisted commands** — the script refuses, but skill reinforces visually
- **ALWAYS show the command** before approve — transparency
- **Vault perpetuum hints are MANUAL_REVIEW** (not executable) — never auto-run
- **Thesis perpetuum hints are MANUAL_REVIEW** — require human judgment
- **Data_coverage is the only T2 perpetuum today** — other promotions need explicit tier change
- **Show delta after**: re-running the perpetuum proves the fix worked

## Files reference

- `scripts/perpetuum_action_run.py` — main runner with whitelist
- `agents/perpetuum/_actions.py` — list_open_by_perpetuum helper
- `scripts/action_cli.py` — legacy CLI (still works for ignore/note)
- `obsidian_vault/skills/Phase_X_Perpetuum_Engine.md` — full design
- watchlist_actions table — actions storage (shared with trigger system)
