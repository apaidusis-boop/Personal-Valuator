#!/usr/bin/env python
"""
Midnight Work 2026-05-09 — Data Fortification Night

Mission: prove how firm our data is. NO new recommendations tonight.
Tomorrow's test: same questions as today — do answers come from DB rows
or from extrapolation? Tonight we want to push that needle.

Phases:
  1. inventory     — nullable critical fields per ticker × column
  2a. dividends    — yfinance 25y div history + CAGR computations
  2b. macro        — FRED 30y + BCB 20y
  2c. sec_cvm      — SEC EDGAR + CVM DFP/ITR + PDF extractor
  3. engines       — recompute scoring, fair_value, dividend_safety
  4. perpetuums    — run T1 observers (all 10)
  5. multi_agent   — synthetic_ic + variant_perception (Ollama, in-house)
  6. provenance    — audit per-field source coverage
  7. master_report — consolidated markdown deliverable

Outputs:
  logs/midnight_2026-05-09.log
  obsidian_vault/Midnight_Work_2026-05-09.md          live status
  obsidian_vault/Bibliotheca/Midnight_Work_2026-05-09.md  final report
  data/midnight_inventory_2026-05-09.json
  data/provenance_scorecard_2026-05-09.json

Kill switch: create file STOP_MIDNIGHT in repo root to halt at next phase boundary.
"""

import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "midnight_2026-05-09.log"
STATUS_FILE = ROOT / "obsidian_vault" / "Midnight_Work_2026-05-09.md"
REPORT_FILE = ROOT / "obsidian_vault" / "Bibliotheca" / "Midnight_Work_2026-05-09.md"
INVENTORY_FILE = ROOT / "data" / "midnight_inventory_2026-05-09.json"
PROV_FILE = ROOT / "data" / "provenance_scorecard_2026-05-09.json"
KILL_FILE = ROOT / "STOP_MIDNIGHT"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
_VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON = str(_VENV_PY) if _VENV_PY.exists() else sys.executable

for p in (LOG_FILE.parent, STATUS_FILE.parent, REPORT_FILE.parent, INVENTORY_FILE.parent):
    p.mkdir(parents=True, exist_ok=True)


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def hms():
    return datetime.now().strftime("%H:%M:%S")


def log(msg, phase=None):
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


def stop_requested():
    return KILL_FILE.exists()


def run_cmd(cmd, phase, timeout=900):
    log(f"$ {cmd}", phase)
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        r = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=str(ROOT),
        )
        log(f"  exit={r.returncode}  stdout_len={len(r.stdout or '')}  stderr_len={len(r.stderr or '')}", phase)
        if r.returncode != 0 and r.stderr:
            log(f"  stderr_head: {(r.stderr or '')[:600]}", phase)
        return r
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT after {timeout}s", phase)
        return None
    except Exception as e:
        log(f"  EXCEPTION: {e!r}", phase)
        return None


# ------------------- Phase 1 — inventory -------------------


def phase_inventory():
    phase = "1.inventory"
    log("Scanning DBs for nullable critical fields and stale rows", phase)

    critical_fund = ["pe", "pb", "dy", "roe", "eps", "bvps", "dividend_streak_years"]
    inventory = {"us": {}, "br": {}, "computed_at": now_iso()}

    for market, db in [("us", DB_US), ("br", DB_BR)]:
        if not db.exists():
            inventory[market] = {"error": "db_not_found"}
            continue
        con = sqlite3.connect(db)
        try:
            tickers = [r[0] for r in con.execute("SELECT DISTINCT ticker FROM companies").fetchall()]
        except Exception:
            tickers = []
        market_inv = {
            "tickers_total": len(tickers),
            "gaps_per_field": {},
            "tickers_no_recent_div": [],
            "tickers_no_recent_fund": [],
            "tickers_no_fundamentals_at_all": [],
        }
        for col in critical_fund:
            try:
                n_null = con.execute(f"SELECT COUNT(DISTINCT ticker) FROM fundamentals WHERE {col} IS NULL").fetchone()[0]
            except Exception:
                n_null = -1
            market_inv["gaps_per_field"][col] = n_null
        stale_div_cutoff = (datetime.now() - timedelta(days=180)).date().isoformat()
        stale_fund_cutoff = (datetime.now() - timedelta(days=120)).date().isoformat()
        for tk in tickers:
            try:
                r = con.execute("SELECT MAX(ex_date) FROM dividends WHERE ticker=?", (tk,)).fetchone()
            except Exception:
                r = None
            if not r or not r[0] or r[0] < stale_div_cutoff:
                market_inv["tickers_no_recent_div"].append(tk)
            try:
                r = con.execute("SELECT MAX(period_end) FROM fundamentals WHERE ticker=?", (tk,)).fetchone()
            except Exception:
                r = None
            if not r or not r[0]:
                market_inv["tickers_no_fundamentals_at_all"].append(tk)
            elif r[0] < stale_fund_cutoff:
                market_inv["tickers_no_recent_fund"].append(tk)
        inventory[market] = market_inv
        con.close()

    INVENTORY_FILE.write_text(json.dumps(inventory, indent=2, default=str), encoding="utf-8")
    for m in ("us", "br"):
        i = inventory.get(m, {})
        log(
            f"  {m.upper()}: tickers={i.get('tickers_total')} stale_fund={len(i.get('tickers_no_recent_fund', []))} "
            f"stale_div={len(i.get('tickers_no_recent_div', []))} no_fund={len(i.get('tickers_no_fundamentals_at_all', []))}",
            phase,
        )
    log(f"  written: {INVENTORY_FILE.relative_to(ROOT)}", phase)


# ------------------- Phase 2a — dividends -------------------


def phase_dividends():
    phase = "2a.dividends"
    if stop_requested():
        return
    log("Backfilling dividend history (yfinance deep fundamentals + holdings)", phase)
    fetcher = ROOT / "fetchers" / "yf_deep_fundamentals.py"
    if fetcher.exists():
        run_cmd(f'"{PYTHON}" "{fetcher}" --holdings', phase, timeout=1500)
    else:
        log("  yf_deep_fundamentals.py not found — skipping", phase)

    log("Computing CAGR (5y/10y/25y) per ticker — inline", phase)
    cagrs = {}
    for market, db in [("us", DB_US), ("br", DB_BR)]:
        if not db.exists():
            continue
        con = sqlite3.connect(db)
        try:
            tickers = [r[0] for r in con.execute("SELECT DISTINCT ticker FROM dividends").fetchall()]
        except Exception:
            tickers = []
        for tk in tickers:
            try:
                rows = con.execute(
                    "SELECT strftime('%Y', ex_date) AS y, SUM(amount) FROM dividends WHERE ticker=? GROUP BY y ORDER BY y",
                    (tk,),
                ).fetchall()
            except Exception:
                rows = []
            years = {int(y): float(a) for y, a in rows if y and a}
            if len(years) < 3:
                continue
            yrs_sorted = sorted(years.keys())
            # ANCHOR FIX: use the most recent COMPLETE year as anchor.
            # Current year is partial (we are mid-year), comparing partial-year
            # totals to full-year totals produces fake negative CAGRs.
            this_year = datetime.now().year
            anchor_year = yrs_sorted[-1]
            if anchor_year >= this_year:
                # current year is partial — drop it
                anchor_year = anchor_year - 1
                # also confirm anchor year exists in data
                while anchor_year not in years and anchor_year > yrs_sorted[0]:
                    anchor_year -= 1
            entry = {
                "market": market,
                "years_count": len(years),
                "anchor_year": anchor_year,
                "current_year_partial": yrs_sorted[-1] >= this_year,
            }
            for span in (5, 10, 25):
                yr_old = anchor_year - span
                if (
                    yr_old in years
                    and years.get(yr_old, 0) > 0
                    and years.get(anchor_year, 0) > 0
                ):
                    cagr = (years[anchor_year] / years[yr_old]) ** (1 / span) - 1
                    entry[f"cagr_{span}y_pct"] = round(cagr * 100, 2)
                else:
                    entry[f"cagr_{span}y_pct"] = None
            entry["anchor_amount"] = round(years.get(anchor_year, 0), 4)
            cagrs[tk] = entry
        con.close()
    out = ROOT / "data" / "dividend_cagrs_2026-05-09.json"
    out.write_text(json.dumps(cagrs, indent=2), encoding="utf-8")
    log(f"  CAGRs computed for {len(cagrs)} tickers — {out.relative_to(ROOT)}", phase)


# ------------------- Phase 2b — macro -------------------


def phase_macro():
    phase = "2b.macro"
    if stop_requested():
        return
    log("Backfilling macro history (FRED + BCB)", phase)
    fred = ROOT / "fetchers" / "fred_fetcher.py"
    if fred.exists():
        run_cmd(f'"{PYTHON}" "{fred}"', phase, timeout=600)
    bcb_export = ROOT / "scripts" / "export_macro_csv.py"
    if bcb_export.exists():
        run_cmd(f'"{PYTHON}" "{bcb_export}"', phase, timeout=300)
    log("  Macro phase done", phase)


# ------------------- Phase 2c — sec / cvm -------------------


def phase_sec_cvm():
    phase = "2c.sec_cvm"
    if stop_requested():
        return
    log("Running SEC monitor for US universe", phase)
    run_cmd(f'"{PYTHON}" -m monitors.sec_monitor', phase, timeout=2400)
    if stop_requested():
        return
    log("Running CVM monitor for BR universe", phase)
    run_cmd(f'"{PYTHON}" -m monitors.cvm_monitor', phase, timeout=2400)
    if stop_requested():
        return
    log("Extracting CVM PDFs for pending events", phase)
    pdf_ext = ROOT / "monitors" / "cvm_pdf_extractor.py"
    if pdf_ext.exists():
        run_cmd(f'"{PYTHON}" "{pdf_ext}" --limit 200', phase, timeout=2400)


# ------------------- Phase 3 — engines -------------------


def phase_engines():
    phase = "3.engines"
    if stop_requested():
        return
    log("Recomputing dividend_safety for all", phase)
    run_cmd(f'"{PYTHON}" -m scoring.dividend_safety --all', phase, timeout=600)
    if stop_requested():
        return
    log("Running daily_update.py (BR side)", phase)
    daily_br = ROOT / "scripts" / "daily_update.py"
    if daily_br.exists():
        run_cmd(f'"{PYTHON}" "{daily_br}"', phase, timeout=2400)
    if stop_requested():
        return
    log("Running daily_update_us.py (US side)", phase)
    daily_us = ROOT / "scripts" / "daily_update_us.py"
    if daily_us.exists():
        run_cmd(f'"{PYTHON}" "{daily_us}"', phase, timeout=2400)


# ------------------- Phase 4 — perpetuums -------------------


def phase_perpetuums():
    phase = "4.perpetuums"
    if stop_requested():
        return
    log("Running perpetuum_master (all T1 observers)", phase)
    pm = ROOT / "agents" / "perpetuum_master.py"
    if pm.exists():
        run_cmd(f'"{PYTHON}" "{pm}"', phase, timeout=3600)
    else:
        log("  perpetuum_master.py not found — skipping", phase)


# ------------------- Phase 5 — multi-agent validation -------------------


def phase_multi_agent():
    phase = "5.multi_agent"
    if stop_requested():
        return
    log("Multi-agent validation chain (synthetic_ic + variant_perception)", phase)

    # holdings only — these are LLM (Ollama) and slow
    holdings = []
    for market, db in [("us", DB_US), ("br", DB_BR)]:
        if not db.exists():
            continue
        con = sqlite3.connect(db)
        try:
            for r in con.execute("SELECT ticker FROM portfolio_positions WHERE active=1").fetchall():
                holdings.append((r[0], market))
        except Exception:
            pass
        con.close()
    log(f"  holdings to validate: {len(holdings)}", phase)

    if not holdings:
        log("  no holdings — skipping phase", phase)
        return

    # MANDATORY SMOKE TEST — added 2026-05-09 after phase 5 lost 7.5h to undetected
    # Ollama CPU mode + broken model. Run 1 ticker first, verify <300s and zero
    # _error in output. Without this, never detach a multi-agent phase overnight.
    smoke_tk, smoke_mkt = holdings[0]
    log(f"  SMOKE TEST: running 1 ticker ({smoke_mkt}/{smoke_tk}) before iterating all", phase)
    smoke_t0 = time.time()
    smoke_r = run_cmd(
        f'"{PYTHON}" -m agents.synthetic_ic {smoke_tk} --market {smoke_mkt}',
        phase,
        timeout=300,
    )
    smoke_elapsed = time.time() - smoke_t0
    if smoke_r is None or smoke_r.returncode != 0:
        log(f"  SMOKE FAIL ({smoke_elapsed:.0f}s) — bailing out of phase 5 entirely", phase)
        return
    smoke_failed_personas = (smoke_r.stdout or "").count("FAIL (")
    log(f"  smoke OK ({smoke_elapsed:.0f}s, failed personas={smoke_failed_personas})", phase)
    if smoke_failed_personas >= 3:
        log(f"  >=3 personas failed in smoke — bailing", phase)
        return

    consecutive_failures = 0
    for tk, mkt in holdings:
        if stop_requested():
            log("STOP requested — bailing out of multi_agent phase", phase)
            break
        log(f"  → {mkt}/{tk} synthetic_ic", phase)
        # No --majority 3: 3× cost not justified for overnight observer mode.
        # Single run per persona; majority is reserved for explicit decision moments.
        r = run_cmd(f'"{PYTHON}" -m agents.synthetic_ic {tk} --market {mkt}', phase, timeout=300)
        if r is None or r.returncode != 0:
            consecutive_failures += 1
            if consecutive_failures >= 3:
                log(f"  3 consecutive ticker failures — bailing out of phase 5", phase)
                break
        else:
            consecutive_failures = 0
        if stop_requested():
            break
        log(f"  → {mkt}/{tk} variant_perception", phase)
        run_cmd(f'"{PYTHON}" -m agents.variant_perception {tk} --market {mkt}', phase, timeout=120)


# ------------------- Phase 6 — provenance audit -------------------


def phase_provenance():
    phase = "6.provenance"
    if stop_requested():
        return
    log("Auditing provenance: source coverage per field", phase)
    audit = {"us": {}, "br": {}, "computed_at": now_iso()}

    for market, db in [("us", DB_US), ("br", DB_BR)]:
        if not db.exists():
            audit[market] = {"error": "db_not_found"}
            continue
        con = sqlite3.connect(db)
        market_audit = {}

        try:
            rows = con.execute(
                """
                SELECT confidence_label, COUNT(*) FROM fair_value
                WHERE computed_at = (
                    SELECT MAX(computed_at) FROM fair_value f2 WHERE f2.ticker = fair_value.ticker
                )
                GROUP BY confidence_label
                """
            ).fetchall()
            market_audit["fair_value_confidence"] = {(k or "null"): v for k, v in rows}
        except Exception as e:
            market_audit["fair_value_confidence"] = f"err:{e}"

        try:
            n_prov = con.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
            market_audit["provenance_rows"] = n_prov
        except Exception:
            market_audit["provenance_rows"] = "no_table"

        try:
            rows = con.execute("SELECT confidence_label, COUNT(*) FROM data_confidence GROUP BY confidence_label").fetchall()
            market_audit["data_confidence"] = {(k or "null"): v for k, v in rows}
        except Exception:
            market_audit["data_confidence"] = "no_table"

        critical = ["pe", "pb", "dy", "roe", "eps", "bvps", "dividend_streak_years"]
        nulls = {}
        nonnulls = {}
        for c in critical:
            try:
                n_total = con.execute("SELECT COUNT(*) FROM fundamentals").fetchone()[0]
                n_nonnull = con.execute(f"SELECT COUNT(*) FROM fundamentals WHERE {c} IS NOT NULL").fetchone()[0]
                nonnulls[c] = n_nonnull
                nulls[c] = n_total - n_nonnull
            except Exception:
                nulls[c] = -1
                nonnulls[c] = -1
        market_audit["fundamental_nulls"] = nulls
        market_audit["fundamental_nonnulls"] = nonnulls

        # event coverage
        try:
            n_events = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            n_events_recent = con.execute(
                "SELECT COUNT(*) FROM events WHERE event_date >= date('now','-90 day')"
            ).fetchone()[0]
            market_audit["events_total"] = n_events
            market_audit["events_last_90d"] = n_events_recent
        except Exception:
            market_audit["events_total"] = -1

        # dividends streak length distribution
        try:
            rows = con.execute(
                "SELECT dividend_streak_years FROM fundamentals WHERE dividend_streak_years IS NOT NULL"
            ).fetchall()
            streaks = [r[0] for r in rows if r[0] is not None]
            if streaks:
                market_audit["streak_stats"] = {
                    "min": min(streaks),
                    "max": max(streaks),
                    "median": sorted(streaks)[len(streaks) // 2],
                    "n_25plus": sum(1 for s in streaks if s >= 25),
                }
        except Exception:
            pass

        audit[market] = market_audit
        con.close()

    PROV_FILE.write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    log(f"  scorecard: {PROV_FILE.relative_to(ROOT)}", phase)
    for m in ("us", "br"):
        ma = audit.get(m, {})
        if isinstance(ma, dict):
            log(f"  {m.upper()} fair_value_confidence: {ma.get('fair_value_confidence')}", phase)


# ------------------- Phase 7 — master report -------------------


def phase_master_report():
    phase = "7.report"
    log("Building master report", phase)

    inv = json.loads(INVENTORY_FILE.read_text(encoding="utf-8")) if INVENTORY_FILE.exists() else {}
    prov = json.loads(PROV_FILE.read_text(encoding="utf-8")) if PROV_FILE.exists() else {}
    cagr_file = ROOT / "data" / "dividend_cagrs_2026-05-09.json"
    cagrs = json.loads(cagr_file.read_text(encoding="utf-8")) if cagr_file.exists() else {}

    md = []
    md.append("# Midnight Work 2026-05-09 — Data Fortification Report")
    md.append("")
    md.append(f"_Generated: {now_iso()}_")
    md.append("")
    md.append("## Mission recap")
    md.append("")
    md.append(
        "Fortify data quality, audit provenance, prove firmness — **no new recommendations**. "
        "Tomorrow re-test: same questions as today, do answers cite DB rows or extrapolate?"
    )
    md.append("")
    md.append("## Phase results — quick scan")
    md.append("")
    md.append(f"- Live log: `{LOG_FILE.relative_to(ROOT)}`")
    md.append(f"- Live status: `{STATUS_FILE.relative_to(ROOT)}`")
    md.append(f"- Inventory snapshot: `{INVENTORY_FILE.relative_to(ROOT)}`")
    md.append(f"- Provenance scorecard: `{PROV_FILE.relative_to(ROOT)}`")
    md.append(f"- Dividend CAGRs: `{cagr_file.relative_to(ROOT) if cagr_file.exists() else 'not generated'}`")
    md.append("")
    md.append("## Inventory snapshot (start of night)")
    md.append("")
    for market in ("us", "br"):
        i = inv.get(market, {})
        if not isinstance(i, dict):
            continue
        md.append(f"### {market.upper()}")
        md.append("")
        md.append(f"- Tickers known: **{i.get('tickers_total', '?')}**")
        md.append(f"- Tickers with no fundamentals at all: **{len(i.get('tickers_no_fundamentals_at_all', []))}**")
        md.append(f"- Tickers with stale fundamentals (>120d): **{len(i.get('tickers_no_recent_fund', []))}**")
        md.append(f"- Tickers with stale dividend history (>180d): **{len(i.get('tickers_no_recent_div', []))}**")
        gaps = i.get("gaps_per_field", {})
        if gaps:
            md.append("- Fundamentals nulls per field:")
            for k, v in gaps.items():
                md.append(f"  - `{k}`: {v} tickers null")
        md.append("")

    md.append("## Provenance scorecard (end of night)")
    md.append("")
    for market in ("us", "br"):
        p = prov.get(market, {})
        if not isinstance(p, dict):
            continue
        md.append(f"### {market.upper()}")
        md.append("")
        fvc = p.get("fair_value_confidence")
        if fvc:
            md.append(f"- fair_value confidence distribution: `{fvc}`")
        dc = p.get("data_confidence")
        if dc:
            md.append(f"- data_confidence distribution: `{dc}`")
        prv = p.get("provenance_rows")
        if prv is not None:
            md.append(f"- provenance table rows: `{prv}`")
        nn = p.get("fundamental_nonnulls", {})
        if nn:
            md.append("- fundamentals non-null counts:")
            for k, v in nn.items():
                md.append(f"  - `{k}`: {v}")
        ev = p.get("events_total")
        if ev is not None:
            md.append(f"- events total: {ev}  (last 90d: {p.get('events_last_90d')})")
        ss = p.get("streak_stats")
        if ss:
            md.append(f"- dividend streak stats: median={ss.get('median')}y max={ss.get('max')}y count_>=25y={ss.get('n_25plus')}")
        md.append("")

    md.append("## Dividend CAGRs (computed from DB, NOT extrapolated)")
    md.append("")
    md.append("| Ticker | Mkt | 5y CAGR | 10y CAGR | 25y CAGR | yrs in DB |")
    md.append("|---|---|---:|---:|---:|---:|")
    for tk in sorted(cagrs):
        e = cagrs[tk]
        c5 = e.get("cagr_5y_pct")
        c10 = e.get("cagr_10y_pct")
        c25 = e.get("cagr_25y_pct")
        yrs = e.get("years_count")
        c5s = f"{c5:+.1f}%" if c5 is not None else "—"
        c10s = f"{c10:+.1f}%" if c10 is not None else "—"
        c25s = f"{c25:+.1f}%" if c25 is not None else "—"
        md.append(f"| {tk} | {e.get('market', '?')} | {c5s} | {c10s} | {c25s} | {yrs} |")
    md.append("")

    md.append("## How to consume tomorrow")
    md.append("")
    md.append("1. Read THIS file (`Bibliotheca/Midnight_Work_2026-05-09.md`) — executive summary")
    md.append("2. Read live status (`Midnight_Work_2026-05-09.md`) — chronological progress for any failures")
    md.append("3. Re-ask yesterday's questions (PG/JNJ/KO bands; JPM deep dive; \"onde investir $1.5k\"). Each numerical claim should now cite a DB source or be flagged `extrapolation:true`.")
    md.append("4. Compare CAGR table above with my earlier extrapolations: \"PG 5–7%/yr\", \"JPM ~10%/yr\". Real numbers are above.")
    md.append("5. Items NOT closed tonight (engineering follow-ups for design conversation tomorrow):")
    md.append("   - CET1/Tier 1/leverage parser for US banks")
    md.append("   - Brand/intangible premium estimator for staples")
    md.append("   - Litigation overhang flags (10-K Item 3 parsing)")
    md.append("   - Fair-value intermediate \"add zones\" engine")
    md.append("   - REIT-aware dividend safety calibration audit (O still WATCH 60)")
    md.append("")

    REPORT_FILE.write_text("\n".join(md), encoding="utf-8")
    log(f"  master report: {REPORT_FILE.relative_to(ROOT)}", phase)


# ------------------- Main -------------------


def main():
    log("=== MIDNIGHT WORK 2026-05-09 START ===", "boot")
    log(f"Python: {PYTHON}", "boot")
    log(f"Repo:   {ROOT}", "boot")

    STATUS_FILE.write_text(
        f"# Midnight Work 2026-05-09 — live status\n\n_Started: {now_iso()}_\n\n"
        "Drop `STOP_MIDNIGHT` in repo root to halt at next phase boundary.\n\n"
        "## Progress\n\n",
        encoding="utf-8",
    )

    phases = [
        ("inventory", phase_inventory),
        ("dividends", phase_dividends),
        ("macro", phase_macro),
        ("sec_cvm", phase_sec_cvm),
        ("engines", phase_engines),
        ("perpetuums", phase_perpetuums),
        ("multi_agent", phase_multi_agent),
        ("provenance", phase_provenance),
        ("master_report", phase_master_report),
    ]

    for name, fn in phases:
        if stop_requested():
            log(f"STOP_MIDNIGHT detected — halting before phase '{name}'", "boot")
            break
        t0 = time.time()
        log(f">>> ENTERING PHASE: {name}", "boot")
        try:
            fn()
        except Exception as e:
            log(f"  PHASE EXCEPTION ({name}): {e!r}", "boot")
        elapsed = time.time() - t0
        log(f"<<< EXITING PHASE: {name}  ({elapsed:.0f}s elapsed)", "boot")

    log("=== MIDNIGHT WORK 2026-05-09 DONE ===", "boot")


if __name__ == "__main__":
    main()
