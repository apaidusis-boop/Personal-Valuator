---
description: Write a concrete, step-by-step implementation plan before touching code
---

# Writing Plans

## When to use

Before writing code for any multi-step task where:
- The spec covers more than one file or component
- The task will take more than ~15 minutes
- Multiple concerns could be bundled (which violates "Surgical changes")

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

## Pre-flight checks

1. **Script catalog check first** (per CLAUDE.md anti-queima-tokens policy):
   Before designing anything new, scan the catalog in CLAUDE.md. If an existing script can be extended with a flag, do that — do not create a new script.

2. **Scope check**: If the spec covers multiple independent subsystems, split into separate plans. Each plan should produce working, testable software on its own.

## Plan location

Save to: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Plan document header

Every plan must start with:

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Files touched:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/test_file.py`

---
```

## File structure decisions

Before defining tasks, declare which files are created or modified and what each is responsible for.

- Each file should have one clear responsibility (per CLAUDE.md Simplicity first principle).
- Files that change together should live together.
- Follow existing project patterns — do not restructure adjacent files as a side-effect.
- Prefer extending an existing script with a flag over creating a new one.

## Task granularity

Each task = one action (2-5 minutes). Separate steps for:

- Write the failing test
- Run it to confirm it fails
- Implement minimal code
- Run tests to confirm pass
- Commit (one concern per commit)

## Task structure template

````markdown
### Task N: [Component Name]

**Files:**
- Modify: `exact/path/file.py`
- Test: `tests/exact/path/test_file.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function_under_test(input_value)
    assert result == expected_value
```

- [ ] **Step 2: Run test — confirm FAIL**

```bash
pytest tests/exact/path/test_file.py::test_specific_behavior -v
```
Expected: `FAILED` with `<reason>`

- [ ] **Step 3: Implement minimal fix**

```python
def function_under_test(input_value):
    return expected_value
```

- [ ] **Step 4: Run test — confirm PASS**

```bash
pytest tests/exact/path/test_file.py::test_specific_behavior -v
```
Expected: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add tests/exact/path/test_file.py exact/path/file.py
git commit -m "feat: <one-line criterion of done>"
```
````

## No placeholders

These are plan failures — never write them:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" without showing the code
- "Write tests for the above" without the actual test code
- "Similar to Task N" — repeat the code; tasks may be read out of order
- Steps describing what to do without showing how

## Project conventions to bake in

- **In-house first**: default to Ollama local LLMs (`python -m agents._agent <role>`), not Claude API.
- **Surgical changes**: each commit = one concern. No drive-by refactors in the same commit.
- **DB writes**: BR in `data/br_investments.db`, US in `data/us_investments.db`. Never cross-write.
- **Tickers**: stored without `.SA` suffix in DB; fetchers add it when calling external APIs.
- **Dates**: ISO 8601 in DB; `br_date()` helper for display.
- **code_health perpetuum** (CH001-CH007) will scan the result — write clean code upfront.

## Self-review before handoff

After writing the complete plan:

1. **Spec coverage** — every requirement maps to a task. List any gaps.
2. **Placeholder scan** — search for patterns from "No placeholders" above. Fix them.
3. **Type/name consistency** — function names and method signatures match across tasks.

Fix issues inline. Then offer execution:

> "Plan saved to `docs/superpowers/plans/<filename>.md`. Ready to execute task-by-task — confirm to start."

> Adapted from obra/superpowers/skills/writing-plans/SKILL.md — fetched 2026-05-06
