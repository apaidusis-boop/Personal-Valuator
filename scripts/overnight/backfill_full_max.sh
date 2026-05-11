#!/bin/bash
# Overnight full price backfill — period=max for all BR + US tickers
# Idempotent. Logs each ticker outcome.
set -u

PYEXE=".venv/Scripts/python.exe"
TS=$(date +%Y%m%d_%H%M%S)
LOG="logs/overnight/full_backfill_${TS}.log"
mkdir -p logs/overnight

echo "=== FULL BACKFILL START: $(date) ===" | tee -a "$LOG"

br_count=0
br_ok=0
br_fail=0
echo "" | tee -a "$LOG"
echo "--- BR (period=max) ---" | tee -a "$LOG"
while IFS= read -r raw_t; do
  # Strip CR (Windows CRLF txt files cause `read` to keep trailing \r in $t)
  t="${raw_t%$'\r'}"
  [ -z "$t" ] && continue
  br_count=$((br_count+1))
  if "$PYEXE" fetchers/yf_br_fetcher.py "$t" --period max >> "$LOG" 2>&1; then
    br_ok=$((br_ok+1))
  else
    br_fail=$((br_fail+1))
    echo "[BR FAIL] $t" | tee -a "$LOG"
  fi
done < logs/overnight/br_tickers.txt
echo "[BR SUMMARY] total=$br_count ok=$br_ok fail=$br_fail" | tee -a "$LOG"

us_count=0
us_ok=0
us_fail=0
echo "" | tee -a "$LOG"
echo "--- US (period=max) ---" | tee -a "$LOG"
while IFS= read -r raw_t; do
  # Strip CR (Windows CRLF txt files cause `read` to keep trailing \r in $t)
  t="${raw_t%$'\r'}"
  [ -z "$t" ] && continue
  us_count=$((us_count+1))
  if "$PYEXE" fetchers/yf_us_fetcher.py "$t" --period max >> "$LOG" 2>&1; then
    us_ok=$((us_ok+1))
  else
    us_fail=$((us_fail+1))
    echo "[US FAIL] $t" | tee -a "$LOG"
  fi
done < logs/overnight/us_tickers.txt
echo "[US SUMMARY] total=$us_count ok=$us_ok fail=$us_fail" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== FULL BACKFILL END: $(date) ===" | tee -a "$LOG"
