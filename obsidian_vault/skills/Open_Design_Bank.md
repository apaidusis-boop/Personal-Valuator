---
type: skill_reference
location: external_repo
date: 2026-05-08
tags: [design, skills, open-design, sparse-checkout, bank]
---

# Open-Design Bank — local sparse-checkout pointer

> Phase MM "If only 5 things" #5. The `nexu-io/open-design` repo (33k★)
> has 97 skills + 142 design systems — too much to clone fully. Sparse-
> checkout subset relevant to financial dashboard work, kept locally
> outside the project repo so it doesn't pollute git.

## Path

```
~/.local/design-banks/open-design/
```

## What's in the local checkout

### `skills/`

| Skill | Purpose |
|---|---|
| `dashboard` | "inline SVG only, no JS chart libraries" rule + dashboard layout patterns |
| `finance-report` | report layout templates (dossier-grade) |
| `trading-analysis-dashboard-template` | working `template.html` w/ hover crosshair + click-to-focus floating chart + command palette — **direct fix candidate for FairTrajectoryChart** |
| `critique` | self-critique skill — invoke for design review pre-merge |
| `tweaks` | design-tweak collection (small fixes to common slop) |
| `dcf-valuation` | DCF-specific layout (relevant for Sprint MM.5 if we add a DCF page) |

### `design-systems/`

| System | Use case |
|---|---|
| `editorial` | Gelasio serif + Ubuntu Mono numerals + 8pt grid — JPM-adjacent register |
| `clickhouse` | Database-product UI register (reference for our /portfolio table density) |
| `linear-app` | Modern fintech SaaS (reference for /research grid) |
| `cohere` | Editorial AI register (reference for /council / dossier pages) |

## How to read these in Sprint MM.2

```bash
# Read a skill's instructions
cat ~/.local/design-banks/open-design/skills/dashboard/SKILL.md

# Read the trading-analysis template HTML
cat ~/.local/design-banks/open-design/skills/trading-analysis-dashboard-template/template.html

# Browse a design system
ls ~/.local/design-banks/open-design/design-systems/editorial/
```

## How to update

```bash
cd ~/.local/design-banks/open-design
git pull --depth=1
# Sparse-checkout settings persist; new files arrive only for the included paths.
```

## How to add more skills/systems later

```bash
cd ~/.local/design-banks/open-design
git sparse-checkout add skills/<new-skill-name>
git sparse-checkout add design-systems/<new-system-name>
git pull --depth=1
```

## Why outside project repo

- Avoid polluting git diffs / `daily_run.bat` cycles
- Reference material, not source code we ship
- Can be re-cloned if disk lost (it's a public repo)
- Helena scout already tracks this in `Design_Watch.md` install-tier

## Setup history

- Cloned 2026-05-08 with `--depth=1 --filter=blob:none --sparse`
- Sparse subset applied via `git sparse-checkout set` (10 paths)
- 38 files total (clone is ~few hundred KB)
