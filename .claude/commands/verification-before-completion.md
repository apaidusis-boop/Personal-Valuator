---
description: Verify work with fresh evidence before claiming done — no completion without proof
---

# Verification Before Completion

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Claiming work is complete without running verification is dishonesty, not efficiency.
Violating the letter of this rule is violating the spirit of it.

## The Gate Function

Before any success claim or expression of satisfaction:

1. **Identify** — what command proves this claim?
2. **Run** — execute the full command fresh, in this message
3. **Read** — full output, exit code, failure count
4. **Verify** — does output confirm the claim?
   - NO → state actual status with evidence
   - YES → state claim WITH evidence quoted
5. **Only then** — make the claim

Skipping any step = asserting without evidence.

## Common failure patterns

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | `pytest` output: 0 failures | "Should pass", previous run |
| Script runs clean | Exit 0 + expected output | "Looks correct" |
| DB populated | `sqlite3` query returning rows | "Inserted successfully" |
| Scoring correct | Score value printed and matches threshold | "Logic looks right" |
| Fetcher working | Actual fetched data printed | No errors in logs |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Phase complete | Line-by-line checklist vs requirements | Tests passing |

## Red Flags — STOP

- Using "should", "probably", "seems to", "looks like"
- Expressing satisfaction before verification ("Done!", "Great!", "All set!")
- About to commit without running the verification command first
- Trusting a sub-agent's success report without independent check
- Relying on partial verification ("linter passed" ≠ "tests pass")
- "Just this once" under time pressure

## Verification commands for this project

```bash
# Tests
pytest tests/ -v

# Specific script dry-run
python scripts/daily_update.py --dry-run
python scripts/weekly_report.py --dry-run

# DB state
sqlite3 data/br_investments.db "SELECT count(*) FROM fundamentals WHERE period_end >= date('now','-90 days')"
sqlite3 data/us_investments.db "SELECT ticker, score, passes_screen FROM scores ORDER BY run_date DESC LIMIT 10"

# Scoring engine
python scoring/engine.py ITSA4 --market br
python scoring/engine.py JNJ --market us

# Fetcher check
python fetchers/yfinance_fetcher.py --ticker AAPL --dry-run 2>&1 | tail -5

# Perpetuum open actions
python scripts/perpetuum_action_run.py list-open

# Data anomalies
python analytics/data_anomalies.py
```

## Rationalization prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence is not evidence |
| "Linter passed" | Linter does not run tests |
| "Agent said success" | Verify independently |
| "Just this once" | No exceptions |
| "Different words, rule doesn't apply" | Spirit over letter |

## Regression test pattern (TDD red-green)

```
Write test → Run (must FAIL) → Implement fix → Run (must PASS)
```

"I've written a regression test" without confirming the red-green cycle is not verification.

## When to apply

**Always before:**
- Any completion/success claim or positive status statement
- Committing, creating a PR, or pushing
- Moving to the next task or phase
- Delegating to a sub-agent (verify their output afterwards)
- Reporting a phase as "done" to the user

> Adapted from obra/superpowers/skills/verification-before-completion/SKILL.md — fetched 2026-05-06
