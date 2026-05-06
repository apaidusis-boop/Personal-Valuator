---
description: Debug any failure systematically — root cause first, no fixes without evidence
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If Phase 1 is not complete, you cannot propose fixes. Random patches waste time and mask root causes.

## When to use

ANY technical issue: test failures, bugs, unexpected output, build failures, DB query anomalies, fetcher errors, scoring engine surprises.

**Use especially when:**
- Under time pressure ("quick fix" is tempting)
- You've already tried one fix
- The issue is in a multi-component pipeline (fetcher → DB → scoring → report)

## The Four Phases

### Phase 1: Root Cause Investigation

Before any fix:

1. **Read error messages completely** — stack traces, line numbers, exit codes. They often contain the answer.

2. **Reproduce consistently**
   - Can you trigger it reliably?
   - If not reproducible, gather more data — don't guess.

3. **Check recent changes**
   ```bash
   git diff HEAD~3
   git log --oneline -10
   ```

4. **Add instrumentation at each boundary** (for multi-component issues)

   Example for the fetcher → DB → scoring pipeline:
   ```python
   # Fetcher boundary
   print(f"[FETCHER] raw result keys: {list(result.keys())}")

   # DB write boundary
   print(f"[DB] inserting fundamentals: ticker={ticker}, pe={pe}, dy={dy}")

   # Scoring boundary
   print(f"[SCORE] inputs: {inputs}")
   ```
   Run once to see WHERE it breaks, then investigate that layer.

5. **Trace data flow** — where does the bad value originate? Walk up the call stack.

### Phase 2: Pattern Analysis

1. Find working examples of the same pattern in the codebase (use Grep).
2. Read the reference implementation completely — don't skim.
3. List every difference between working and broken, however small.
4. Check dependencies: DB schema columns, config keys, env vars.

### Phase 3: Hypothesis and Testing

1. State a single, specific hypothesis: *"I think X is the root cause because Y."*
2. Make the **smallest possible change** to test it — one variable at a time.
3. If it works → Phase 4. If not → form a NEW hypothesis. Do NOT stack fixes.
4. If you don't understand something, say so. Don't pretend.

### Phase 4: Implementation

1. **Create a failing test** (or a minimal reproduction script) before fixing.
   - Use `pytest tests/` or a one-off `python -c "..."` to confirm failure.
   - Surgical: per CLAUDE.md principles, no drive-by refactors.

2. **Implement single fix** addressing the root cause. Nothing else.

3. **Verify**:
   ```bash
   pytest tests/ -v          # or the relevant test
   python scripts/daily_update.py --dry-run  # for pipeline issues
   ```

4. **If fix doesn't work** → return to Phase 1 with new information.

5. **If 3+ fixes have failed → STOP.** Question the architecture.
   - Each fix revealing a new problem elsewhere = architectural issue.
   - Discuss before attempting fix #4.

## Red Flags — return to Phase 1

- "Quick fix for now"
- "Just try changing X and see"
- "Probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- Attempting fix #4 after three failures

## Project-specific notes

- **In-house first**: diagnose with local tools (`sqlite3`, `python -m`, existing scripts in the catalog). Claude API is last resort.
- **Surgical changes**: each fix = one concern, one commit. No bundled refactors.
- **code_health perpetuum** (CH001-CH007) catches structural anti-patterns separately — don't conflate debugging with code health cleanup.
- **DB queries**: use `sqlite3 data/br_investments.db` or `data/us_investments.db` to inspect state directly.
- **Fetcher cascade**: check `config/sources_priority.yaml` and `fetchers/_fallback.py` logs before assuming the primary source is wrong.

## Quick reference

| Phase | Key activity | Done when |
|-------|-------------|-----------|
| 1. Root cause | Read errors, reproduce, instrument | Know WHAT and WHY |
| 2. Pattern | Find working examples, diff | Differences identified |
| 3. Hypothesis | Single theory, minimal test | Confirmed or new theory |
| 4. Implementation | Failing test → fix → verify | Tests pass, no regressions |

> Adapted from obra/superpowers/skills/systematic-debugging/SKILL.md — fetched 2026-05-06
