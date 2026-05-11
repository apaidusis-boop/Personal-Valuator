"""Extension run after the 3 fixes of 2026-05-09 morning.

Mission: re-run engines with fixes applied + run multi_agent on holdings + watchlist.

Phases:
  1. backfill_br_intangibles  — yfinance balance sheet for BR universe
  2. recompute_fair_value     — rebuild with intangibles in inputs (full universe)
  3. recompute_dividend_safety — REIT-aware ROE fix takes effect
  4. multi_agent_holdings     — synthetic_ic on all holdings (US + BR)
  5. multi_agent_watchlist    — synthetic_ic on top-N watchlist (US + BR)
  6. final_report             — consolidated markdown deliverable

Calibration log: each phase records predicted vs actual elapsed time. The
calibration file lets us tune predictions over time so future "vou dormir
6h" promises are honest.

Outputs:
  logs/extend_2026-05-09.log
  obsidian_vault/Extension_Run_2026-05-09.md         live status
  obsidian_vault/Bibliotheca/Extension_Run_2026-05-09.md  final report
  data/calibration_2026-05-09.json                   predicted vs actual

Kill switch: STOP_EXTEND in repo root.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "extend_2026-05-09.log"
STATUS_FILE = ROOT / "obsidian_vault" / "Extension_Run_2026-05-09.md"
REPORT_FILE = ROOT / "obsidian_vault" / "Bibliotheca" / "Extension_Run_2026-05-09.md"
CALIB_FILE = ROOT / "data" / "calibration_2026-05-09.json"
KILL_FILE = ROOT / "STOP_EXTEND"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
_VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON = str(_VENV_PY) if _VENV_PY.exists() else sys.executable

for p in (LOG_FILE.parent, STATUS_FILE.parent, REPORT_FILE.parent, CALIB_FILE.parent):
    p.mkdir(parents=True, exist_ok=True)

# Predicted timings — refined from earlier observations. Used for calibration log.
PREDICTIONS = {
    "1.backfill_br_intangibles": 90,    # ~80 BR tickers @ 0.5s + yfinance latency
    "2.recompute_fair_value":   180,   # 190 tickers @ ~1s each
    "3.recompute_safety":        60,   # quick re-score
    "4.multi_agent_holdings":  2520,   # 33 holdings × 76s
    "5.multi_agent_watchlist": 5400,   # 70 watchlist × 76s (top picks only)
    "6.final_report":            30,
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def hms() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log(msg: str, phase: str | None = None) -> None:
    line = f"[{now_iso()}] {phase or '---'}: {msg}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode(), flush=True)
    if phase:
        try:
            with open(STATUS_FILE, "a", encoding="utf-8") as f:
                f.write(f"- {hms()} **{phase}** {msg}\n")
        except Exception:
            pass


def stop_requested() -> bool:
    return KILL_FILE.exists()


def run_cmd(cmd: str, phase: str, timeout: int = 1800):
    log(f"$ {cmd}", phase)
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
            env=env, cwd=str(ROOT),
        )
        log(f"  exit={r.returncode}  stdout={len(r.stdout or '')}b  stderr={len(r.stderr or '')}b", phase)
        if r.returncode != 0 and r.stderr:
            log(f"  stderr_head: {(r.stderr or '')[:500]}", phase)
        return r
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT after {timeout}s", phase)
        return None
    except Exception as e:
        log(f"  EXCEPTION: {e!r}", phase)
        return None


# ------------------- Calibration log helpers -------------------

_calib: list[dict] = []


def _record_calib(phase: str, predicted: int, actual: float, **extra) -> None:
    delta = actual - predicted
    pct = (delta / predicted * 100) if predicted else 0
    entry = {
        "phase": phase, "predicted_sec": predicted,
        "actual_sec": round(actual, 1), "delta_sec": round(delta, 1),
        "delta_pct": round(pct, 1), "ts": now_iso(), **extra,
    }
    _calib.append(entry)
    CALIB_FILE.write_text(json.dumps(_calib, indent=2), encoding="utf-8")
    sign = "+" if delta >= 0 else ""
    log(f"  ⏱ predicted={predicted}s actual={actual:.0f}s delta={sign}{delta:.0f}s ({sign}{pct:.0f}%)", phase)


# ------------------- Phases -------------------

def phase_1_backfill_br() -> None:
    p = "1.backfill_br_intangibles"
    if stop_requested(): return
    t0 = time.time()
    log("Backfilling intangibles for BR universe (yfinance .SA)", p)
    run_cmd(f'"{PYTHON}" scripts/backfill_intangibles.py --br-only --sleep 0.3', p, timeout=600)
    _record_calib(p, PREDICTIONS[p], time.time() - t0)


def phase_2_recompute_fv() -> None:
    p = "2.recompute_fair_value"
    if stop_requested(): return
    t0 = time.time()
    log("Recomputing fair_value for entire universe (with intangibles in inputs_json)", p)
    run_cmd(f'"{PYTHON}" -m scoring.fair_value --all --trigger "extend_2026-05-09"', p, timeout=1200)
    _record_calib(p, PREDICTIONS[p], time.time() - t0)


def phase_3_recompute_safety() -> None:
    p = "3.recompute_safety"
    if stop_requested(): return
    t0 = time.time()
    log("Recomputing dividend_safety (REIT-aware ROE branch)", p)
    run_cmd(f'"{PYTHON}" -m scoring.dividend_safety --all', p, timeout=300)
    _record_calib(p, PREDICTIONS[p], time.time() - t0)


def _holdings() -> list[tuple[str, str]]:
    out = []
    for mkt, db in (("us", DB_US), ("br", DB_BR)):
        if not db.exists(): continue
        with sqlite3.connect(db) as c:
            try:
                rows = c.execute("SELECT ticker FROM portfolio_positions WHERE active=1").fetchall()
            except Exception:
                rows = []
            for (tk,) in rows:
                out.append((tk, mkt))
    return out


def _watchlist_top(n_per_market: int = 35) -> list[tuple[str, str]]:
    """Top-N watchlist by safety score (already cross-screened)."""
    out = []
    for mkt, db in (("us", DB_US), ("br", DB_BR)):
        if not db.exists(): continue
        with sqlite3.connect(db) as c:
            try:
                rows = c.execute("""
                    SELECT s.ticker FROM scores s
                    LEFT JOIN portfolio_positions p ON s.ticker=p.ticker AND p.active=1
                    WHERE p.ticker IS NULL
                      AND s.run_date=(SELECT MAX(run_date) FROM scores s2 WHERE s2.ticker=s.ticker)
                    ORDER BY s.score DESC LIMIT ?
                """, (n_per_market,)).fetchall()
            except Exception:
                rows = []
            for (tk,) in rows:
                out.append((tk, mkt))
    return out


def phase_4_multi_agent_holdings() -> None:
    p = "4.multi_agent_holdings"
    if stop_requested(): return
    t0 = time.time()

    holdings = _holdings()
    log(f"Multi-agent on holdings: {len(holdings)} tickers", p)

    # Smoke test mandatory (per Postmortem 2026-05-09 lesson)
    if not holdings:
        log("  no holdings — skipping", p)
        _record_calib(p, PREDICTIONS[p], time.time() - t0, n_tickers=0)
        return

    smoke_tk, smoke_mkt = holdings[0]
    log(f"  SMOKE: {smoke_mkt}/{smoke_tk}", p)
    smoke_t0 = time.time()
    smoke_r = run_cmd(
        f'"{PYTHON}" -m agents.synthetic_ic {smoke_tk} --market {smoke_mkt}',
        p, timeout=240,
    )
    smoke_elapsed = time.time() - smoke_t0
    if smoke_r is None or smoke_r.returncode != 0:
        log(f"  SMOKE FAIL ({smoke_elapsed:.0f}s) — bailing phase 4", p)
        _record_calib(p, PREDICTIONS[p], time.time() - t0, smoke_failed=True)
        return
    fail_count = (smoke_r.stdout or "").count("FAIL (")
    log(f"  smoke OK in {smoke_elapsed:.0f}s, persona_fails={fail_count}", p)
    if fail_count >= 3:
        log("  ≥3 persona failures in smoke — bailing", p)
        _record_calib(p, PREDICTIONS[p], time.time() - t0, smoke_persona_fails=fail_count)
        return

    consec_fail = 0
    completed = 0
    for tk, mkt in holdings[1:]:  # smoke already covered holdings[0]
        if stop_requested():
            log("STOP_EXTEND — bailing", p)
            break
        log(f"  → {mkt}/{tk}", p)
        r = run_cmd(f'"{PYTHON}" -m agents.synthetic_ic {tk} --market {mkt}', p, timeout=240)
        if r is None or r.returncode != 0:
            consec_fail += 1
            if consec_fail >= 3:
                log("  3 consecutive failures — bailing phase 4", p)
                break
        else:
            consec_fail = 0
            completed += 1
        # Variant perception (cheap, sub-3s usually)
        run_cmd(f'"{PYTHON}" -m agents.variant_perception {tk} --market {mkt}', p, timeout=60)

    elapsed = time.time() - t0
    _record_calib(p, PREDICTIONS[p], elapsed, n_tickers=len(holdings), completed=completed + 1)


def phase_5_multi_agent_watchlist() -> None:
    p = "5.multi_agent_watchlist"
    if stop_requested(): return
    t0 = time.time()

    targets = _watchlist_top(n_per_market=35)  # 70 total cap
    log(f"Multi-agent on watchlist top-N: {len(targets)} tickers", p)

    if not targets:
        log("  no watchlist targets — skipping", p)
        _record_calib(p, PREDICTIONS[p], time.time() - t0, n_tickers=0)
        return

    consec_fail = 0
    completed = 0
    for tk, mkt in targets:
        if stop_requested():
            log("STOP_EXTEND — bailing", p)
            break
        log(f"  → {mkt}/{tk}", p)
        r = run_cmd(f'"{PYTHON}" -m agents.synthetic_ic {tk} --market {mkt}', p, timeout=240)
        if r is None or r.returncode != 0:
            consec_fail += 1
            if consec_fail >= 5:  # watchlist has more null-data variance, allow more before bail
                log("  5 consecutive failures — bailing phase 5", p)
                break
        else:
            consec_fail = 0
            completed += 1

    elapsed = time.time() - t0
    _record_calib(p, PREDICTIONS[p], elapsed, n_tickers=len(targets), completed=completed)


def phase_6_final_report() -> None:
    p = "6.final_report"
    t0 = time.time()
    log("Building final report", p)

    # Gather state
    state = {"computed_at": now_iso(), "phases_completed": len(_calib)}

    # fair_value confidence distribution
    for mkt, db in (("us", DB_US), ("br", DB_BR)):
        if not db.exists(): continue
        with sqlite3.connect(db) as c:
            rows = c.execute("""
                SELECT confidence_label, COUNT(*) FROM fair_value
                WHERE computed_at = (SELECT MAX(computed_at) FROM fair_value f2 WHERE f2.ticker = fair_value.ticker)
                GROUP BY confidence_label
            """).fetchall()
            state[f"{mkt}_fair_value_confidence"] = dict(rows)

    # safety distribution
    safety = {}
    try:
        safety_proc = subprocess.run(
            f'"{PYTHON}" -m scoring.dividend_safety --all',
            shell=True, capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="replace", cwd=str(ROOT),
        )
        for line in (safety_proc.stdout or "").splitlines():
            parts = line.split()
            if len(parts) >= 4 and parts[1] in ("br", "us") and parts[3] in ("SAFE", "WATCH", "RISK", "N/A"):
                safety[parts[0]] = (parts[3], parts[1])
    except Exception:
        pass
    state["safety_summary"] = safety

    # IC debates count
    debates_dir = ROOT / "obsidian_vault" / "tickers"
    if debates_dir.exists():
        state["ic_debates_total"] = len(list(debates_dir.glob("*_IC_DEBATE.md")))

    # Build markdown
    md = []
    md.append("# Extension Run 2026-05-09 — Final Report")
    md.append("")
    md.append(f"_Generated: {state['computed_at']}_")
    md.append("")
    md.append("## Mission recap")
    md.append("")
    md.append("3 fixes shipped earlier today, then this orchestrator extended:")
    md.append("- Recomputed fair_value for full universe (now with intangibles in inputs)")
    md.append("- Recomputed dividend_safety (REIT-aware ROE fix)")
    md.append("- synthetic_ic on holdings + watchlist top-N")
    md.append("")
    md.append("## Calibration: predicted vs actual")
    md.append("")
    md.append("| Phase | Predicted | Actual | Δ | Δ% |")
    md.append("|---|---:|---:|---:|---:|")
    for c in _calib:
        sign = "+" if c["delta_sec"] >= 0 else ""
        md.append(f"| {c['phase']} | {c['predicted_sec']}s | {c['actual_sec']:.0f}s | {sign}{c['delta_sec']:.0f}s | {sign}{c['delta_pct']:.0f}% |")
    if _calib:
        total_pred = sum(c['predicted_sec'] for c in _calib)
        total_actual = sum(c['actual_sec'] for c in _calib)
        total_delta = total_actual - total_pred
        sign = "+" if total_delta >= 0 else ""
        pct = (total_delta / total_pred * 100) if total_pred else 0
        md.append(f"| **TOTAL** | **{total_pred}s ({total_pred/60:.0f}min)** | **{total_actual:.0f}s ({total_actual/60:.0f}min)** | **{sign}{total_delta:.0f}s** | **{sign}{pct:.0f}%** |")
    md.append("")
    md.append("## Fair value confidence (after recompute)")
    md.append("")
    for mkt in ("us", "br"):
        d = state.get(f"{mkt}_fair_value_confidence", {})
        if d:
            md.append(f"- **{mkt.upper()}**: {d}")
    md.append("")
    md.append("## IC debates produced")
    md.append("")
    md.append(f"- Total IC_DEBATE.md files in vault: **{state.get('ic_debates_total', 0)}**")
    md.append(f"- Run output dir: `obsidian_vault/tickers/<TK>_IC_DEBATE.md`")
    md.append("")
    md.append("## How to use this run")
    md.append("")
    md.append("1. Compare any single dossier to its earlier version — does intangible context appear in fundamentals?")
    md.append("2. Re-ask 'should I add to KO/PG/JNJ?' — system can now cite intangible_pct_assets and warn re: brand-off-balance-sheet")
    md.append("3. Re-ask 'is O safe?' — dividend_safety should now show REIT-aware re-score (75 instead of 60)")
    md.append("4. Open A_FAZER.md to see what's still pending (CET1 parser, fair-zones engine, litigation flags, CVM upstream fix)")
    md.append("")
    md.append("## Files")
    md.append("")
    md.append(f"- Live status: `{STATUS_FILE.relative_to(ROOT)}`")
    md.append(f"- Log: `{LOG_FILE.relative_to(ROOT)}`")
    md.append(f"- Calibration: `{CALIB_FILE.relative_to(ROOT)}`")
    md.append("")

    REPORT_FILE.write_text("\n".join(md), encoding="utf-8")
    _record_calib(p, PREDICTIONS[p], time.time() - t0)
    log(f"  master report: {REPORT_FILE.relative_to(ROOT)}", p)


# ------------------- Main -------------------

def main() -> None:
    log("=== EXTENSION RUN 2026-05-09 START ===", "boot")
    log(f"Python: {PYTHON}", "boot")

    STATUS_FILE.write_text(
        f"# Extension Run 2026-05-09 — live status\n\n"
        f"_Started: {now_iso()}_\n\n"
        "Drop `STOP_EXTEND` in repo root to halt at next phase boundary.\n\n"
        "Predicted total: ~140min (~2.3h). Calibration log at end.\n\n"
        "## Progress\n\n",
        encoding="utf-8",
    )

    phases = [
        ("1.backfill_br_intangibles", phase_1_backfill_br),
        ("2.recompute_fair_value",   phase_2_recompute_fv),
        ("3.recompute_safety",       phase_3_recompute_safety),
        ("4.multi_agent_holdings",   phase_4_multi_agent_holdings),
        ("5.multi_agent_watchlist",  phase_5_multi_agent_watchlist),
        ("6.final_report",           phase_6_final_report),
    ]

    for name, fn in phases:
        if stop_requested():
            log(f"STOP_EXTEND detected — halting before {name}", "boot")
            break
        log(f">>> ENTERING {name}", "boot")
        try:
            fn()
        except Exception as e:
            log(f"  PHASE EXCEPTION ({name}): {e!r}", "boot")
        log(f"<<< EXITING {name}", "boot")

    log("=== EXTENSION RUN DONE ===", "boot")


if __name__ == "__main__":
    main()
