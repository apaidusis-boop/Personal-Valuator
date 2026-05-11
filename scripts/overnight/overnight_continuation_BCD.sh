#!/usr/bin/env bash
# Overnight continuation 2026-05-09:
# Tavily quota was exhausted at start; Block A and partial D ran.
# This script sleeps until ~02:30 local (after UTC midnight reset)
# and then runs B + C + D-rerun.
#
# Launched in background by Claude after Block A finished.
# PC must stay awake (memory rule: cron 23:30 daily — already on).

set -e

cd "$(dirname "$0")/../.."
echo "[$(date -Iseconds)] continuation: sleeping ~3h30m until ~02:30 local for Tavily reset" \
    | tee -a logs/overnight_2026-05-09.log

# 12600 = 3h30m. Tavily resets at UTC midnight; with London BST (UTC+1 in Apr–Oct, +0 in winter)
# this puts us safely past reset.
sleep 12600

echo "[$(date -Iseconds)] continuation: starting Block B" | tee -a logs/overnight_2026-05-09.log
python scripts/overnight/overnight_2026_05_09.py --block B 2>&1 | tee -a logs/overnight_2026-05-09.log

echo "[$(date -Iseconds)] continuation: starting Block C" | tee -a logs/overnight_2026-05-09.log
python scripts/overnight/overnight_2026_05_09.py --block C 2>&1 | tee -a logs/overnight_2026-05-09.log

echo "[$(date -Iseconds)] continuation: re-running Block D with full data" | tee -a logs/overnight_2026-05-09.log
python scripts/overnight/overnight_2026_05_09.py --block D 2>&1 | tee -a logs/overnight_2026-05-09.log

echo "[$(date -Iseconds)] continuation: ALL DONE" | tee -a logs/overnight_2026-05-09.log
