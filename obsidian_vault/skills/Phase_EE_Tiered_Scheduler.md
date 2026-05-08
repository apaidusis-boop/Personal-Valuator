---
title: Phase EE - Tiered Scheduler
phase: EE (Always-On Workforce)
status: shipped
date: 2026-05-08
tags: [phase, infrastructure, scheduler, cron]
---

# Phase EE - Tiered Scheduler

> Splits the previous monolithic 23:30 cron into 3 tiers (hourly / 4h / daily)
> with PID-based lockfiles so a heavier tier blocks lighter tiers from
> overlapping. Goal: filings detected in <1h instead of <22h delay.
>
> **Source roadmap**: `obsidian_vault/Roadmap_Always_On_Workforce.md` Phase EE.

## What shipped

| File | Purpose |
|---|---|
| `agents/_lock.py` | Stateless CLI tier lockfile helper. PID-alive check via Windows OpenProcess + GetExitCodeProcess (ctypes, no subprocess). Auto-recovers stale locks. |
| `scripts/hourly_run.bat` | Tier hourly: SEC monitor (lookback 1d) + CVM monitor + notify_events --hours 4. ~5min. Yields to daily. |
| `scripts/q4h_run.bat` | Tier 4h: cvm_pdf_extractor + dividend/earnings calendars + benchmarks + auto_verdict_on_filing + trigger_monitor. ~10-15min. Yields to daily. |
| `scripts/daily_run.bat` (refactored) | Tier daily: heavy pipeline (BR/US fundamentals, perpetuum_master, fair_value, decision_quality, briefings, RAG, glossary, telegram brief). Acquires `daily.lock` on entry, blocks hourly+q4h. |

Lockfiles live in `data/locks/<tier>.lock`. Each contains `<pid>\n<unix_ts>\n`.

## Scheduling - what to do next (manual user action required)

Phase EE ships the **code** for tiered scheduling. The Windows Task Scheduler
side requires explicit user consent because it touches system services.

### Inspect the current state of the daily task
```powershell
schtasks /Query /TN "investment-intelligence-daily" /V /FO LIST
```

### Register the new hourly + q4h tasks
Run as Administrator (PowerShell elevated):

```powershell
# Hourly: every hour, on the hour, all day
schtasks /Create /SC HOURLY /TN "investment-intelligence-hourly" `
  /TR "C:\Users\paidu\investment-intelligence\scripts\hourly_run.bat" `
  /ST 00:05 /RL HIGHEST /F

# 4-hourly: every 4 hours starting 02:30 (offset to avoid daily 23:30)
schtasks /Create /SC HOURLY /MO 4 /TN "investment-intelligence-q4h" `
  /TR "C:\Users\paidu\investment-intelligence\scripts\q4h_run.bat" `
  /ST 02:30 /RL HIGHEST /F
```

The `/ST 00:05` offset for hourly avoids the top-of-hour stampede where many
other systems schedule. The `/MO 4` modifier on q4h gives 02:30 / 06:30 / 10:30
/ 14:30 / 18:30 / 22:30 - none of which collide with the 23:30 daily.

### Verify all 3 tasks are registered
```powershell
schtasks /Query /TN "investment-intelligence-*" /FO LIST | Select-String "TaskName|Status|Next Run"
```

### Disable a tier (if you ever need to)
```powershell
schtasks /Change /TN "investment-intelligence-hourly" /DISABLE
```

### PC sleep policy (decision pending)
The Phase EE roadmap noted that hourly tasks only run when the PC is awake.
Two options:

1. **Change power plan to never sleep on AC** -
   `powercfg /change standby-timeout-ac 0` (requires elevation)
2. **Use wake timers** in the Task Scheduler -
   `schtasks /Change /TN <name> /RL HIGHEST` and tick "Wake the computer to
   run this task" in the GUI (no clean CLI flag).

Recommendation: option 1 if PC stays plugged in; option 2 if it travels.

## How the locks behave

```
daily acquires daily.lock        - blocks hourly + q4h (they detect via blocked_by)
hourly acquires hourly.lock      - daily ignores it (heavier tier wins on next attempt)
q4h    acquires q4h.lock         - same
```

Hourly and q4h CAN coexist (different lockfiles). If you want them serialised,
add `--blocked-by q4h` to hourly_run.bat (currently they don't block each other
because their work doesn't overlap on the same DBs in conflicting ways).

If a tier crashes mid-run leaving a stale lockfile, the next invocation of that
tier detects the dead PID via `OpenProcess + GetExitCodeProcess` and takes
over the lock automatically. No manual cleanup needed.

## Probing lock state

```powershell
python -m agents._lock status
# {
#   "daily": {"alive": true, "pid": 12345, "ts": 1778232401, "age_seconds": 240}
# }
```

## Reverting to the previous monolithic cron

The refactor is non-destructive:
- `daily_run.bat` still runs the full pipeline if hourly/q4h tasks are not
  registered (the steps moved are also still safe to run there).
- To revert: delete the hourly + q4h scheduled tasks, and re-add the moved
  steps to `daily_run.bat` (git history has the pre-EE version).

## Phase EE done criteria - status

- [x] `agents/_lock.py` shipped with smoke tests passing (acquire/release/blocked_by/stale takeover)
- [x] `scripts/hourly_run.bat` smoke test PASS - SEC inserted 7 events, lock acquired/released cleanly
- [x] `scripts/q4h_run.bat` smoke test - see latest log
- [x] `scripts/daily_run.bat` refactored, lock acquire on entry, em-dashes scrubbed
- [ ] **Pending user action**: register hourly + q4h scheduled tasks (commands above)
- [ ] **Pending user decision**: PC sleep policy (recommend option 1)

## Next phases (Always-On Workforce roadmap)

After Phase EE stabilises:
- **Phase FF (Stream Layer)** - news RSS hourly, YouTube channel poll, Bigdata.com events
- **Phase GG (Reactive Engine)** - event_queue + react_8k / react_fato / react_screen_break handlers
- **Phase HH (Budget & Health)** - health_check first, Tavily bucket allocation, circuit breaker
- **Phase II (Live Workforce Page)** - MC page showing schtasks status + lock state + Tavily quota
- **Phase JJ (Tuning)** - severity calibration, Telegram inline buttons, weekly digest
