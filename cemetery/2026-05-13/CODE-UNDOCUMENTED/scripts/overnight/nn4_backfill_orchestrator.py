"""NN.4 · Backfill orchestrator — autonomous execution.

Reads `data_coverage_summary_2026-05-09.json`, categorises gaps, runs the
correct fetcher per ticker, captures per-ticker logs, re-runs coverage at
the end, writes a single MD report for the user to open after the gym.

Designed to be fire-and-forget: launch in background, walks through 127
tickers (8 prices + 119 fundamentals + a few partial), 60-90 min runtime.

Idempotent — every fetcher used is safe to re-run.

Output: obsidian_vault/Bibliotheca/NN4_Backfill_<DATE>.md
"""
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import time
import traceback
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
VAULT = ROOT / "obsidian_vault" / "Bibliotheca"
LOG = ROOT / "logs" / "nn4_backfill.log"

# Use the project venv that has yfinance + dependencies installed.
# Fall back to current sys.executable if .venv is missing.
_VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON = str(_VENV_PY) if _VENV_PY.exists() else sys.executable

DATE_TAG = date.today().isoformat()
AUDIT_JSON = VAULT / "data_coverage_summary_2026-05-09.json"
OUT_MD = VAULT / f"NN4_Backfill_{DATE_TAG}.md"

PER_TICKER_TIMEOUT = 90  # seconds — yfinance tail latency
TEN_YEARS_AGO = date(date.today().year - 10, date.today().month, date.today().day)


def log(msg: str) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ── Coverage probe (lightweight — same logic as audit, single ticker) ──

def coverage_for_ticker(market: str, ticker: str) -> dict:
    file = DB_BR if market == "br" else DB_US
    out = {"prices_total": 0, "fund_total": 0, "events_total": 0, "deep_rows": 0}
    try:
        c = sqlite3.connect(f"file:{file}?mode=ro", uri=True)
        out["prices_total"] = (c.execute(
            "SELECT COUNT(*) FROM prices WHERE ticker=? AND date >= ?",
            (ticker, TEN_YEARS_AGO.isoformat()),
        ).fetchone() or [0])[0]
        try:
            out["fund_total"] = (c.execute(
                "SELECT COUNT(*) FROM fundamentals WHERE ticker=? AND period_end >= ?",
                (ticker, TEN_YEARS_AGO.isoformat()),
            ).fetchone() or [0])[0]
        except sqlite3.OperationalError:
            pass
        try:
            out["events_total"] = (c.execute(
                "SELECT COUNT(*) FROM events WHERE ticker=? AND event_date >= ?",
                (ticker, TEN_YEARS_AGO.isoformat()),
            ).fetchone() or [0])[0]
        except sqlite3.OperationalError:
            pass
        try:
            out["deep_rows"] = (c.execute(
                "SELECT COUNT(*) FROM deep_fundamentals WHERE ticker=?",
                (ticker,),
            ).fetchone() or [0])[0]
        except sqlite3.OperationalError:
            pass
        c.close()
    except Exception as e:
        log(f"  coverage_for_ticker {market}:{ticker} ERROR: {e}")
    return out


# ── Fetcher runners ─────────────────────────────────────────────────

def run_market_fetcher(market: str, ticker: str) -> tuple[bool, str]:
    """Populates BOTH `prices` and `fundamentals` (quarterly) tables.
    This is the audit-aware fetcher — fundamentals_missing gaps are
    measured against the quarterly fundamentals table."""
    module = "fetchers.yf_br_fetcher" if market == "br" else "fetchers.yf_us_fetcher"
    cmd = [PYTHON, "-m", module, ticker, "--period", "max"]
    return _run(cmd)


def run_deep_fundamentals(ticker: str) -> tuple[bool, str]:
    """Populates `deep_fundamentals` (annual IS/BS/CF) — needed for
    Altman, Piotroski, ROIC, etc. Idempotent re-run."""
    cmd = [PYTHON, "-m", "fetchers.yf_deep_fundamentals", ticker]
    return _run(cmd)


def _run(cmd: list[str]) -> tuple[bool, str]:
    """Returns (ok, last_lines_of_stdout_stderr)."""
    try:
        r = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=PER_TICKER_TIMEOUT,
            encoding="utf-8",
            errors="replace",
        )
        out = (r.stdout or "") + (r.stderr or "")
        tail = "\n".join(out.strip().splitlines()[-3:]) if out.strip() else ""
        return r.returncode == 0, tail[:300]
    except subprocess.TimeoutExpired:
        return False, f"timeout after {PER_TICKER_TIMEOUT}s"
    except Exception as e:
        return False, f"exception: {e}"


# ── Main orchestrator ───────────────────────────────────────────────

def main():
    started = datetime.now()
    log(f"NN.4 BACKFILL START · output {OUT_MD}")

    if not AUDIT_JSON.exists():
        log(f"FATAL: audit JSON missing at {AUDIT_JSON}")
        sys.exit(1)

    summary = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))

    # Plan: bucket tickers by gap kind
    plan: dict[str, list[tuple[str, str]]] = {
        "prices_missing": [],
        "fundamentals_missing": [],
        "partial": [],
    }
    for market, tickers in summary.items():
        for tk, info in tickers.items():
            ov = info.get("overall", "")
            if "NO_PRICES" in ov:
                plan["prices_missing"].append((market, tk))
            elif "NO_FUNDAMENTALS" in ov:
                plan["fundamentals_missing"].append((market, tk))
            elif "PARTIAL" in ov:
                plan["partial"].append((market, tk))

    log(f"PLAN · prices_missing={len(plan['prices_missing'])} "
        f"fund_missing={len(plan['fundamentals_missing'])} "
        f"partial={len(plan['partial'])}")

    # Snapshot before
    before: dict[str, dict] = {}
    all_tickers = set(plan["prices_missing"] + plan["fundamentals_missing"] + plan["partial"])
    for market, tk in all_tickers:
        before[f"{market}:{tk}"] = coverage_for_ticker(market, tk)

    # ── Phase 1: prices_missing — market fetcher (prices + fundamentals) ───
    p1_results: list[dict] = []
    for i, (market, tk) in enumerate(plan["prices_missing"], 1):
        log(f"P1 [{i}/{len(plan['prices_missing'])}] market · {market}:{tk}")
        t0 = time.time()
        ok, tail = run_market_fetcher(market, tk)
        elapsed = time.time() - t0
        p1_results.append({"market": market, "ticker": tk, "ok": ok, "elapsed": round(elapsed, 1), "tail": tail})

    # ── Phase 2: fundamentals_missing — same market fetcher (audit-aware) ──
    # The `fundamentals` quarterly table is populated by yf_br/yf_us_fetcher.
    # Run deep too, so Altman/Piotroski/ROIC stay refreshed.
    p2_results: list[dict] = []
    for i, (market, tk) in enumerate(plan["fundamentals_missing"], 1):
        log(f"P2 [{i}/{len(plan['fundamentals_missing'])}] market+deep · {market}:{tk}")
        t0 = time.time()
        ok_m, tail_m = run_market_fetcher(market, tk)
        ok_d, tail_d = run_deep_fundamentals(tk)
        elapsed = time.time() - t0
        p2_results.append({
            "market": market, "ticker": tk,
            "ok": ok_m, "elapsed": round(elapsed, 1),
            "tail": f"market: {tail_m[:120]} · deep: {tail_d[:120]}",
        })

    # ── Phase 3: partial — same as P2 (market + deep) ─────────────
    p3_results: list[dict] = []
    for i, (market, tk) in enumerate(plan["partial"], 1):
        log(f"P3 [{i}/{len(plan['partial'])}] market+deep · {market}:{tk}")
        t0 = time.time()
        ok_m, tail_m = run_market_fetcher(market, tk)
        ok_d, tail_d = run_deep_fundamentals(tk)
        elapsed = time.time() - t0
        p3_results.append({
            "market": market, "ticker": tk,
            "ok": ok_m, "elapsed": round(elapsed, 1),
            "tail": f"market: {tail_m[:120]} · deep: {tail_d[:120]}",
        })

    # Snapshot after
    after: dict[str, dict] = {}
    for market, tk in all_tickers:
        after[f"{market}:{tk}"] = coverage_for_ticker(market, tk)

    finished = datetime.now()
    duration_min = round((finished - started).total_seconds() / 60, 1)

    # ── Write report ──────────────────────────────────────────────
    write_report(plan, p1_results, p2_results, p3_results, before, after, started, finished, duration_min)
    log(f"NN.4 BACKFILL DONE · duration={duration_min}min · report {OUT_MD}")


def write_report(plan, p1, p2, p3, before, after, started, finished, duration_min):
    lines: list[str] = []
    lines.append("---")
    lines.append("type: backfill_execution_log")
    lines.append(f"date: {DATE_TAG}")
    lines.append(f"sprint: NN.4")
    lines.append(f"started: {started.isoformat(timespec='seconds')}")
    lines.append(f"finished: {finished.isoformat(timespec='seconds')}")
    lines.append(f"duration_min: {duration_min}")
    lines.append("status: autonomous")
    lines.append("tags: [nn4, backfill, data_coverage, autonomous_execution]")
    lines.append("---")
    lines.append("")
    lines.append(f"# NN.4 · Backfill Execution · {DATE_TAG}")
    lines.append("")
    lines.append("> Orquestrador autónomo. User foi para academia, este ficheiro é o relatório.")
    lines.append("> Zero intervenção humana; todos os fetchers são idempotentes.")
    lines.append("")
    lines.append("## TL;DR")
    lines.append("")

    n_p1_ok = sum(1 for r in p1 if r["ok"])
    n_p2_ok = sum(1 for r in p2 if r["ok"])
    n_p3_ok = sum(1 for r in p3 if r["ok"])
    n_total_ok = n_p1_ok + n_p2_ok + n_p3_ok
    n_total = len(p1) + len(p2) + len(p3)
    lines.append(f"- Total tickers processados: **{n_total}**")
    lines.append(f"- Sucessos: **{n_total_ok}** ({n_total_ok / max(n_total, 1) * 100:.0f}%)")
    lines.append(f"- Falhas: **{n_total - n_total_ok}**")
    lines.append(f"- Duração: **{duration_min} min**")
    lines.append("")
    lines.append("## Plano executado")
    lines.append("")
    lines.append("| Fase | Categoria | Tickers | Fetcher |")
    lines.append("|---|---|---|---|")
    lines.append(f"| P1 | prices_missing | {len(plan['prices_missing'])} | yf_br_fetcher / yf_us_fetcher --period max |")
    lines.append(f"| P2 | fundamentals_missing | {len(plan['fundamentals_missing'])} | yf_deep_fundamentals |")
    lines.append(f"| P3 | partial | {len(plan['partial'])} | ambos |")
    lines.append("")

    # Per-phase tables
    for label, results in [("P1 · Prices", p1), ("P2 · Fundamentals", p2), ("P3 · Partial", p3)]:
        if not results:
            continue
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| # | Ticker | Mkt | OK | Δ prices | Δ fund | Δ deep | Tempo (s) | Tail |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(results, 1):
            key = f"{r['market']}:{r['ticker']}"
            b = before.get(key, {})
            a = after.get(key, {})
            d_prices = (a.get("prices_total") or 0) - (b.get("prices_total") or 0)
            d_fund = (a.get("fund_total") or 0) - (b.get("fund_total") or 0)
            d_deep = (a.get("deep_rows") or 0) - (b.get("deep_rows") or 0)
            ok_mark = "✅" if r["ok"] else "❌"
            tail_clean = (r["tail"] or "").replace("|", "\\|").replace("\n", " · ")[:80]
            lines.append(f"| {i} | {r['ticker']} | {r['market']} | {ok_mark} | "
                         f"{d_prices:+d} | {d_fund:+d} | {d_deep:+d} | {r['elapsed']} | {tail_clean} |")
        lines.append("")

    # Failures summary
    failures = [r for r in (p1 + p2 + p3) if not r["ok"]]
    if failures:
        lines.append("## Falhas detectadas")
        lines.append("")
        lines.append("Tickers que NÃO completaram (provavelmente delisted, ticker errado, ou yfinance rate-limit):")
        lines.append("")
        for r in failures[:30]:
            lines.append(f"- `{r['market']}:{r['ticker']}` — {r['tail'][:120]}")
        if len(failures) > 30:
            lines.append(f"- … e mais {len(failures) - 30}")
        lines.append("")

    # Coverage diff summary
    total_d_prices = sum((after[k].get("prices_total", 0) - before[k].get("prices_total", 0)) for k in before)
    total_d_fund = sum((after[k].get("fund_total", 0) - before[k].get("fund_total", 0)) for k in before)
    total_d_deep = sum((after[k].get("deep_rows", 0) - before[k].get("deep_rows", 0)) for k in before)
    lines.append("## Coverage diff (agregado)")
    lines.append("")
    lines.append(f"- Linhas `prices` adicionadas: **+{total_d_prices:,}**")
    lines.append(f"- Linhas `fundamentals` adicionadas: **+{total_d_fund:,}**")
    lines.append(f"- Linhas `deep_fundamentals` adicionadas: **+{total_d_deep:,}**")
    lines.append("")

    lines.append("## Próximos passos")
    lines.append("")
    lines.append("- [ ] Re-correr `python scripts/overnight/overnight_2026_05_09.py --block A` para gerar audit V2 com novos números")
    lines.append("- [ ] Refresh `/stocks` e `/desk` no browser — fundamentals devem aparecer agora")
    lines.append("- [ ] Para failures persistentes: confirmar ticker delisted ou ajustar manualmente em `config/universe.yaml`")
    lines.append("")
    lines.append(f"## Log completo")
    lines.append("")
    lines.append(f"`{LOG.relative_to(ROOT)}`")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
