#!/usr/bin/env bash
# Batch dossier generation for all holdings + watchlist (BR + US).
# Skeletons only — TODO_CLAUDE narrative is filled in subsequent step.
set -u
cd "$(dirname "$0")/.."

TICKERS=(
  # BR holdings stocks
  PRIO3 VALE3 BBDC4 ITSA4
  # BR holdings FIIs
  XPML11 RBRX11 BTLG11 VGIR11 PVBI11
  # BR watchlist stocks
  PETR4 AXIA7 CPLE3 ALOS3 B3SA3 ENGI11 ITUB4 EQTL3 MOTV3 MULT3
  PGMN3 PLPL3 RAPT4 RDOR3 RENT3 SUZB3 TTEN3
  # BR watchlist FIIs
  PMLL11 TRXF11 GARE11 VISC11 RECR11 HGRU11 HGLG11 MCRF11 KNCR11 VGIP11
  BRCO11 MCCI11 XPLG11 KNRI11 RBRY11 VRTA11
  # US holdings
  JNJ JPM BLK O TSM PG TEN AAPL TSLA GS KO BRK-B XP GREK HD BN PLD PLTR TFC NU ACN TTD
  # US watchlist
  V MCD PEP ABBV MSFT
)

TOTAL=${#TICKERS[@]}
i=0
ok=0
fail=0
for t in "${TICKERS[@]}"; do
  i=$((i+1))
  printf "[%2d/%d] %s ... " "$i" "$TOTAL" "$t"
  if python -m scripts.dossier "$t" --quiet 2>>logs/dossier_batch.err; then
    ok=$((ok+1))
    echo "ok"
  else
    fail=$((fail+1))
    echo "FAIL"
  fi
done

echo ""
echo "[summary] $ok ok, $fail failed (of $TOTAL)"
