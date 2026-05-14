---
type: midnight_work_report
date: 2026-05-06
session: external-repos-import
duration_h: ~2 (compressed)
tokens_economy: heavy parallel Sonnet sub-agents (6 research + 4 implementation)
commits: 6
tags: [midnight-work, import, adaptation, governance, ci, slash-commands]
---

# 🌙 Midnight Work — 2026-05-06: External repos import + adaptation

> User dropped 6 external repos with directive: "TUDO O QUE FOR ÚTIL, IMPORTE E ADAPTE. VOLTO EM 8 HORAS, LEMBRE-SE DE ECONOMIZAR TOKENS E USAR OUTROS MODELOS." Token economy enforced via 10 Sonnet sub-agents (6 research, 4 implementation); Opus only for cross-cutting synthesis (Constitution, SKL_tier_B, DESIGN_TASTE, this report).

## TL;DR — final disposition table

| Repo | Posture | Implementation | Commit |
|---|---|---|---|
| `obra/superpowers` | Cherry-pick (5 patterns) | 4 slash cmds + DS010 + rule 7 | dffb5e9 + cfc408b + 92a3b89 |
| `anthropics/skills/frontend-design` | Partial adopt | DS010 spatial + DESIGN_TASTE colour weight | cfc408b + 6ddc4fb |
| `github/features/code-review` | Partial setup | test.yml + codeql.yml | d576c9d |
| `anthropics/claude-code-security-review` | Partial adopt | slash cmd + SKIP_PATTERNS seed | dffb5e9 + 0c6305d |
| `thedotmack/claude-mem` | **Skip** | none (file-based memory more auditable) | — |
| `garrytan/gstack` | Inspiration only | DESIGN_TASTE.md (no tooling) | 6ddc4fb |

## Phase summary

### Phase 1 — Parallel research (Sonnet × 6)

Spawned 6 sub-agents in parallel, one per repo. Each devolved a structured report (under 600 words) with: what it is, top adoption candidates, hard mismatches, recommended posture. Total wall-clock ~140s (longest agent: superpowers 137s).

**Token economy**: research delegated entirely to Sonnet; Opus synthesis ~6k tokens reading reports + deciding adaptation list.

### Phase 2 — Parallel implementation (Sonnet × 4)

Spawned 4 sub-agents in parallel for mechanical work:

1. **CI workflows** → `.github/workflows/test.yml` + `codeql.yml`
2. **Slash commands** → 4 files in `.claude/commands/`
3. **Helena DS010** → `agents/helena/audit.py` edit + sanity check
4. **code_health CH008** → `agents/perpetuum/code_health.py` edit + sanity check

Total wall-clock ~200s (longest: slash commands fetched + adapted 4 upstream files).

### Phase 3 — Manual edits (Opus, cross-cutting)

- `obsidian_vault/CONSTITUTION.md` — added 7th rule + 6 decision-log entries.
- `obsidian_vault/skills/SKL_tier_B.md` — full re-evaluation table with 🔁 markers.
- `mission-control/DESIGN_TASTE.md` — new preference journal (gstack pattern, no tooling).

### Phase 4 — Commits + verification

6 commits, 1 per concern (CLAUDE.md "1 commit por preocupação"). Each commit body has 1-line evidence per the new 7th non-negotiable rule.

**Final pytest run**: 49 passed in 64.39s. Zero regressions.

## Concrete metrics

```
Files created:    11
  .github/workflows/test.yml
  .github/workflows/codeql.yml
  .claude/commands/security-review.md
  .claude/commands/systematic-debugging.md
  .claude/commands/verification-before-completion.md
  .claude/commands/writing-plans.md
  mission-control/DESIGN_TASTE.md
  obsidian_vault/Bibliotheca/Midnight_Work_2026-05-06.md (this file)
  + 3 updated/edited files

Files edited:     5
  agents/helena/audit.py                                    (+89 −0)
  agents/perpetuum/code_health.py                           (+69 −0)
  obsidian_vault/CONSTITUTION.md                            (+12 −2)
  obsidian_vault/skills/SKL_tier_B.md                       (rewrite, +83 −28)
  obsidian_vault/skills/Helena_Mega/01_Audit.md             (auto-regen)

Total LoC added:  ~850
Sonnet agents:    10 (6 research + 4 implementation)
Opus tokens:      ~25k (synthesis + Constitution edits + this report)
Sonnet tokens:    ~280k (delegated, 11x cheaper per token than Opus)

Git commits:      6
  d576c9d  CI workflows (test.yml + codeql.yml)
  dffb5e9  Slash commands (4 from anthropics + obra/superpowers)
  cfc408b  Helena DS010 (skill files >500 lines warn)
  0c6305d  code_health CH008 + SKIP_PATTERNS seed
  92a3b89  Constitution rule 7 + Tier B re-eval
  6ddc4fb  DESIGN_TASTE.md (gstack-inspired, no tooling)
```

## What fired (smoke test results)

**Helena DS010**: 1 hit — `obsidian_vault/skills/Mission_Control_Design_Roadmap.md` @ 672 body lines. Legit candidate for split via reference files (per Anthropic best practice).

**code_health CH008**: 14 hits — biggest offenders:
- `scripts/dashboard_app.py` 1203 lines
- `scripts/obsidian_bridge.py` 1164 lines
- `scripts/dossier.py` 928 lines
- `scripts/build_glossary.py` 924 lines
- `scripts/research.py` ~750 lines (estimated)

These are real maintainability hits. **Documenting them is enough** — a 14-file refactor is a future sprint, not this session. Rule of thumb baked into Constitution: surfacing > fixing in autonomous mode.

## Surprising findings (memory candidates)

1. **Anthropic security-review tool's 18 hard-exclusion list** — its real intellectual value isn't the AI scanner (which costs Opus tokens), it's the *calibrated noise filter*. The 18 categories that are explicitly NOT findings (DoS, rate-limit, weak crypto without exploit context, missing CSRF on read-only endpoints, etc.) are the kind of taxonomic discipline that takes years to develop. Worth more than the scanner itself.

2. **claude-mem licensing trap** — repo is AGPL-3.0 but sub-components are PolyForm Noncommercial. Easy miss; would have constrained future commercial work. Decision was to skip on architecture grounds, but licensing was the second nail.

3. **gstack is not a UI lib** — Garry Tan's repo despite his designer background is a Claude Code skills collection, zero CSS/components. Mission Control already covers what gstack-the-UI would offer; the only borrow is the *taste journal pattern*.

4. **Frontend-design "skip" decision (2026-04-24) was right at the time** — but Mission Control migration to Next.js (Phase EE.3, 2026-04-29) flipped the trigger. Lesson: Tier B re-evaluation cadence (quarterly) was approximately right; weekly might catch faster pivots, but quarterly is sufficient for taste-level decisions.

5. **Repo had ZERO CI** until tonight. Helena audit + code_health perpetuum are cron-time gates; pytest + CodeQL are now PR-time gates. The two complement, not duplicate.

## Open follow-ups (next sprint)

- [ ] User: enable branch protection on `main` via GitHub UI (test.yml + codeql.yml as required checks). Cannot be done via CLI without a personal token + admin scopes.
- [ ] DS010 hit on Mission_Control_Design_Roadmap.md — split into `roadmap-overview.md` + `roadmap-references/themes.md` + `.../bookmarks.md` (following Anthropic progressive-disclosure pattern). Open issue, not blocking.
- [ ] CH008 14 hits — flag dashboard_app.py + obsidian_bridge.py as priority refactor candidates next sprint. They each pre-date the rule by months; acceptable to defer.
- [ ] `Design_System.md` doesn't yet have the dominant-colour + accent-weight guideline as written prose (it's documented in DESIGN_TASTE.md instead). Reconsider whether to duplicate or whether DESIGN_TASTE is the right home.
- [ ] CH001-CH007 don't yet *consume* SKIP_PATTERNS — it's seeded only. Next code_health refactor sprint should wire it.

## Method notes (for future midnight sessions)

**What worked**:
- Single round of parallel Sonnet research before committing to plan. Could have started implementing earlier and wasted tokens on dead ends.
- Sonnet for mechanical "fetch + write" + Sonnet for clear-spec edits (DS010, CH008) was well-calibrated; both delivered with sanity-check evidence inline.
- Decision-log entries IN the Constitution + SKL_tier_B make this self-auditable later — no need for me to remember what was decided when.

**What I'd tweak next time**:
- Could have run pytest BEFORE the Helena/code_health agents started, as a baseline. As it happens, they didn't break anything, but I had to take it on trust until the final run.
- The 10-agent token economy was deliberate — but could have been more aggressive: writing the Midnight Work report itself in a Sonnet agent would have saved another ~3k Opus tokens. Trade-off: Opus has full session context which makes the report more accurate; Sonnet would need a long prompt to catch up.

## Sources cited

- `obra/superpowers` — github.com/obra/superpowers (Apache-2 / MIT depending on subdir)
- `anthropics/claude-code-security-review` — github.com/anthropics/claude-code-security-review
- `anthropics/skills/frontend-design` — github.com/anthropics/skills/tree/main/skills/frontend-design
- `github/features/code-review` — marketing page, GitHub features
- `thedotmack/claude-mem` — github.com/thedotmack/claude-mem (AGPL-3.0 + PolyForm Noncommercial)
- `garrytan/gstack` — github.com/garrytan/gstack

> Constitution rule 7 evidence — every claim of completion in this report has a referenced commit hash, a sanity-check output, or a "skipped + why" rationale. No "should-work" statements without evidence.
