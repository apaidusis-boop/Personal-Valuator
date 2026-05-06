---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(git show:*), Bash(git remote show:*), Read, Glob, Grep
description: Security review of branch changes — high-confidence vulns only, no noise
---

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:
```
!`git status`
```

FILES MODIFIED:
```
!`git diff --name-only origin/HEAD...`
```

COMMITS:
```
!`git log --no-decorate origin/HEAD...`
```

DIFF CONTENT:
```
!`git diff --merge-base origin/HEAD`
```

## Objective

Identify **HIGH-CONFIDENCE** security vulnerabilities introduced by this branch only.
Not a general code review — focus on what is *newly added* here.

**Minimum confidence to report: 8/10.** Better to miss a theoretical issue than flood with noise.

## Project context

- Python codebase; SQLite (br_investments.db / us_investments.db); yfinance + Ollama local LLMs.
- Secrets live in `.env` (never committed). `MASSIVE_API_KEY`, `TAVILY_API_KEY`, `TELEGRAM_TOKEN`.
- Fetchers call external APIs; monitors scrape CVM/SEC EDGAR; scoring engine is offline.
- No web server, no auth layer — single-user personal tool. Attack surface = local scripts + env vars + any subprocess calls.

## Categories to examine

**Input validation**
- SQL injection via unsanitized ticker/query strings passed to SQLite
- Command injection in `subprocess` calls or `os.system`
- Path traversal in file write operations (e.g. log paths, vault exports)

**Secrets management**
- Hardcoded API keys, tokens, or passwords in new code
- Secrets logged to `logs/` (structured JSON — check what fields are emitted)
- New `.env` reads that might be inadvertently written to DB or vault

**Injection & code execution**
- `pickle` / `eval` / `yaml.load` (unsafe loader) in new deserialization code
- Template injection if any Jinja2 or f-string HTML output is added

**Data exposure**
- PII or credential data written to `reports/` or `obsidian_vault/` (world-readable directories)
- Debug output that exposes internal state over Telegram push

## Hard exclusions (do NOT report)

1. DoS / resource exhaustion / rate limiting
2. Credentials stored on disk if already `.gitignore`-d and `.env`-protected
3. Memory safety issues (Python is memory-safe)
4. Theoretical regex-DOS
5. Outdated library versions (managed separately)
6. Missing audit logs
7. Race conditions without a concrete attack path in a single-user local tool
8. Environment variable injection (single-user local tool — env vars are trusted)
9. Findings in `*.ipynb` or `tests/` files unless attack path is concrete
10. Log spoofing / logging non-PII data

## Precedents

- UUIDs are unguessable — no need to flag as predictable.
- Ticker strings from `config/universe.yaml` are trusted input — not user-controlled at runtime.
- Ollama model calls are local; no network exfiltration surface there.
- Telegram push sends to a known `chat_id` from `.env` — not exploitable by third parties.

## Methodology

**Phase 1 — Repository context** (use Grep/Glob/Read, no Bash writes):
- Identify existing sanitization patterns (e.g. parameterized SQL queries).
- Understand how external input enters the system (yfinance responses, CVM scrapes, SEC EDGAR data).

**Phase 2 — Comparative analysis**:
- Compare new code against existing secure patterns.
- Flag deviations: raw string interpolation into SQL where parameterized queries are used elsewhere.

**Phase 3 — Vulnerability assessment**:
- Trace data flow from external sources to sensitive operations.
- Look for subprocess calls, `eval`, pickle, path construction from external data.

## Output format

Report findings in Markdown. For each finding:

```
## Vuln N: <Category>: `file.py:LINE`

- **Severity:** High | Medium
- **Confidence:** X/10
- **Description:** ...
- **Exploit scenario:** ...
- **Recommendation:** ...
```

Severity:
- **High**: Directly exploitable → RCE, credential leak, data breach
- **Medium**: Requires specific conditions but meaningful impact

If no findings meet the 8/10 threshold, output: `No high-confidence vulnerabilities found.`

Your final reply must contain the Markdown report and nothing else. Do not write to any files.

> Adapted from anthropics/claude-code-security-review/.claude/commands/security-review.md — fetched 2026-05-06
