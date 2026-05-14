"""Overnight orchestrator — runs deep dive in 3 phases (holdings, US watchlist,
BR watchlist), then composes a unified morning report focused on:

  - $1.5k US cash deployment recommendations
  - Sell candidates framework
  - Top signals cross-ticker (CRITICAL flagged)
  - Validation table per ticker
  - Errors / coding issues found

Output: obsidian_vault/Overnight_<DATE+1>/_LEITURA_DA_MANHA.md + per-ticker dossiers.

Usage:
    python scripts/overnight_orchestrator.py                # full run
    python scripts/overnight_orchestrator.py --phase b      # one phase
    python scripts/overnight_orchestrator.py --skip-extract # skip PDF download
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Tomorrow's date — when the user wakes up
TOMORROW = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y-%m-%d")
OUT_DIR = ROOT / "obsidian_vault" / f"Overnight_{TOMORROW}"
LOG_PATH = ROOT / "logs" / f"overnight_{TOMORROW}.log"
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")
# Allow override via env (for smoke testing before real yaml is ready)
RI_URLS_YAML = Path(os.environ.get("RI_URLS_YAML",
                                    str(ROOT / "config" / "ri_urls.yaml")))

PHASES = ["holdings_br", "holdings_us", "watchlist_us", "watchlist_br"]


def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def load_yaml() -> dict:
    if not RI_URLS_YAML.exists():
        return {}
    with RI_URLS_YAML.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_phase_tickers(phase: str, urls_data: dict) -> list[str]:
    """Filter tickers by phase."""
    out = []
    for ticker, cfg in urls_data.items():
        if cfg.get("status") != "ok":
            continue
        market = cfg.get("market", "")
        is_holding = bool(cfg.get("is_holding", False))
        if phase == "holdings_br" and market == "br" and is_holding:
            out.append(ticker)
        elif phase == "holdings_us" and market == "us" and is_holding:
            out.append(ticker)
        elif phase == "watchlist_us" and market == "us" and not is_holding:
            out.append(ticker)
        elif phase == "watchlist_br" and market == "br" and not is_holding:
            out.append(ticker)
    return sorted(out)


def run_phase(phase: str, tickers: list[str], skip_extract: bool = False) -> dict:
    """Run pilot_deep_dive for a list of tickers. Output goes to OUT_DIR."""
    if not tickers:
        _log({"event": "phase_skip_empty", "phase": phase})
        return {"phase": phase, "n": 0, "elapsed_s": 0}
    _log({"event": "phase_start", "phase": phase, "n": len(tickers)})
    cmd = [
        PYTHON,
        str(ROOT / "scripts" / "pilot_deep_dive.py"),
        "--from-yaml", "--deep", "--force-fresh",
        "--per-ticker-budget", "300",
    ]
    if skip_extract:
        cmd.append("--no-download")
    cmd += ["--tickers"] + tickers

    env = os.environ.copy()
    env["PILOT_OUT_DIR"] = str(OUT_DIR)
    env["PYTHONIOENCODING"] = "utf-8"
    env["RI_URLS_YAML"] = str(RI_URLS_YAML)

    t0 = time.time()
    try:
        r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                           timeout=int(len(tickers) * 360))
        elapsed = time.time() - t0
    except subprocess.TimeoutExpired:
        _log({"event": "phase_timeout", "phase": phase})
        return {"phase": phase, "n": len(tickers), "elapsed_s": -1,
                "status": "timeout"}
    _log({"event": "phase_done", "phase": phase, "n": len(tickers),
          "elapsed_s": round(elapsed, 1),
          "rc": r.returncode})
    if r.returncode != 0:
        _log({"event": "phase_stderr", "phase": phase,
              "stderr": (r.stderr or "")[-500:]})
    return {"phase": phase, "n": len(tickers), "elapsed_s": round(elapsed, 1),
            "rc": r.returncode}


def collect_dossiers() -> dict:
    """Read all dossier .md files and parse top-level metrics for master."""
    docs = {}
    for md in OUT_DIR.glob("*.md"):
        if md.name.startswith("_"):
            continue
        ticker = md.stem
        text = md.read_text(encoding="utf-8")
        # Quick parse — count filings/events/signals
        novel_count = 0
        events_count = 0
        signals_count = 0
        critical_signal = ""
        if "filings detectados como novos vs DB" in text:
            import re as _re
            m = _re.search(r"\*\*(\d+)\s+filings detectados como novos",
                            text)
            if m:
                novel_count = int(m.group(1))
        for ln in text.splitlines():
            if "🚨" in ln and "matched" in ln:
                signals_count += 1
                if not critical_signal:
                    critical_signal = ln[:200]
        docs[ticker] = {
            "novel": novel_count,
            "signals": signals_count,
            "critical": critical_signal,
            "path": md.name,
        }
    return docs


def get_us_holdings_data() -> list[dict]:
    """For $1.5k decision: pull US holdings with prices, fundamentals, scores."""
    db = ROOT / "data" / "us_investments.db"
    if not db.exists():
        return []
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    out = []
    try:
        rows = c.execute("""
            SELECT c.ticker, c.name, c.sector,
                   p.quantity, p.entry_price, p.entry_date
            FROM companies c
            LEFT JOIN portfolio_positions p ON p.ticker = c.ticker
                AND p.active = 1
            WHERE c.is_holding = 1
            ORDER BY c.ticker
        """).fetchall()
        for r in rows:
            t = r["ticker"]
            d = dict(r)
            try:
                price = c.execute(
                    "SELECT date, close FROM prices WHERE ticker=? "
                    "ORDER BY date DESC LIMIT 1", (t,)
                ).fetchone()
                d["last_price_date"] = price["date"] if price else None
                d["last_price"] = price["close"] if price else None
            except sqlite3.OperationalError:
                d["last_price"] = None
            try:
                fund = c.execute(
                    "SELECT period_end, eps, bvps, roe, pe, pb, dy, "
                    "is_aristocrat, dividend_streak_years "
                    "FROM fundamentals WHERE ticker=? "
                    "ORDER BY period_end DESC LIMIT 1", (t,)
                ).fetchone()
                if fund:
                    for k, v in dict(fund).items():
                        d[f"f_{k}"] = v
            except sqlite3.OperationalError:
                pass
            try:
                sc = c.execute(
                    "SELECT score, passes_screen FROM scores WHERE ticker=? "
                    "ORDER BY run_date DESC LIMIT 1", (t,)
                ).fetchone()
                if sc:
                    d["score"] = sc["score"]
                    d["passes_screen"] = sc["passes_screen"]
            except sqlite3.OperationalError:
                pass
            out.append(d)
    finally:
        c.close()
    return out


def cash_allocation_section(dossiers: dict) -> str:
    """Recommend top picks for $1.5k US cash deployment."""
    holdings = get_us_holdings_data()
    L = []
    L.append("## 💰 Recomendação para $1,500 USD")
    L.append("")
    L.append("**Critério de ranking** (composto):")
    L.append("- Score nosso (0-1, mais alto = melhor)")
    L.append("- Passa screen Buffett (boolean)")
    L.append("- Aristocrat / dividend streak (boolean / years)")
    L.append("- DY actual (>2.5%)")
    L.append("- Sinais novos descobertos no overnight (filings novos / críticos)")
    L.append("- Profit/loss da posição actual (entry vs current)")
    L.append("")

    # Build scoring table
    rows = []
    for h in holdings:
        t = h["ticker"]
        score = h.get("score") or 0
        passes = h.get("passes_screen") or 0
        roe = h.get("f_roe") or 0
        dy = h.get("f_dy") or 0
        pe = h.get("f_pe") or 0
        is_arist = h.get("f_is_aristocrat") or 0
        streak = h.get("f_dividend_streak_years") or 0
        last_price = h.get("last_price")
        entry = h.get("entry_price")
        pl_pct = ""
        if last_price and entry:
            pl_pct = f"{((last_price / entry) - 1) * 100:+.1f}%"
        d_data = dossiers.get(t, {})
        novel = d_data.get("novel", 0)
        signals = d_data.get("signals", 0)
        # Composite ranking score
        comp = (
            (score * 30) +
            (10 if passes else 0) +
            (5 if is_arist else 0) +
            (min(streak / 50 * 5, 5) if streak else 0) +
            (max(0, (dy - 0.025)) * 100) +
            (max(0, (0.18 - (pe / 100))) * 30 if pe else 0) +
            (signals * 2) +
            (novel * 0.5)
        )
        rows.append({
            "ticker": t,
            "sector": (h.get("sector") or "-")[:14],
            "score": score,
            "passes": passes,
            "roe": roe,
            "dy": dy,
            "pe": pe,
            "is_arist": is_arist,
            "streak": streak,
            "novel": novel,
            "signals": signals,
            "pl_pct": pl_pct,
            "comp": comp,
            "last_price": last_price,
        })

    rows.sort(key=lambda r: r["comp"], reverse=True)

    L.append("### Top 8 candidatos para reinvestir (ranked)")
    L.append("")
    L.append("| # | Ticker | Sector | Score | Pass | ROE | DY | P/E | "
             "Aristocrat | Streak | Novel filings | Critical signals | "
             "P/L | Composite |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows[:8]):
        L.append(
            f"| {i+1} | **{r['ticker']}** | {r['sector']} | "
            f"{r['score']:.2f} | {'✅' if r['passes'] else '❌'} | "
            f"{r['roe']*100:.1f}% | {r['dy']*100:.2f}% | {r['pe']:.1f} | "
            f"{'✅' if r['is_arist'] else '-'} | {int(r['streak']) if r['streak'] else '-'} | "
            f"{r['novel']} | {r['signals']} | "
            f"{r['pl_pct']} | **{r['comp']:.1f}** |"
        )
    L.append("")

    # Allocation suggestion
    L.append("### Sugestão de alocação $1,500")
    L.append("")
    if rows:
        top3 = rows[:3]
        per_pos = 500
        L.append(f"**Distribuir entre os top 3** (~$500 por posição):")
        for r in top3:
            shares_estimate = (per_pos / r["last_price"]) if r["last_price"] else 0
            L.append(f"- **{r['ticker']}** (~{shares_estimate:.2f} shares @ ${r['last_price']:.2f}) — {r['sector']}")
        L.append("")
        L.append("**Alternativa concentrada** (top 1 só):")
        if rows[0]["last_price"]:
            shares = 1500 / rows[0]["last_price"]
            L.append(f"- **{rows[0]['ticker']}** (~{shares:.2f} shares @ ${rows[0]['last_price']:.2f})")
    L.append("")

    # Bottom 3 — sell candidates
    L.append("### Bottom 5 (candidatos a sell se quiseres realocar)")
    L.append("")
    L.append("| # | Ticker | Sector | Composite | Notes |")
    L.append("|---|---|---|---|---|")
    for i, r in enumerate(rows[-5:]):
        notes = []
        if not r["passes"]:
            notes.append("não passa screen")
        if r["score"] < 0.5:
            notes.append(f"score baixo ({r['score']:.2f})")
        if r["pl_pct"] and r["pl_pct"].startswith("-"):
            notes.append(f"underwater {r['pl_pct']}")
        L.append(f"| {len(rows)-5+i+1} | {r['ticker']} | {r['sector']} | "
                 f"{r['comp']:.1f} | {'; '.join(notes) or '-'} |")
    L.append("")

    L.append("> ⚠️ **Decisão final é tua.** Estes rankings são heurísticos "
             "(score nosso + filings novos + valuation simples). "
             "Verifica o dossier individual de cada ticker antes de operar.")
    L.append("")
    return "\n".join(L)


def critical_signals_section(dossiers: dict) -> str:
    """Cross-ticker critical signals from all dossiers."""
    L = []
    L.append("## 🚨 Sinais críticos descobertos no overnight")
    L.append("")
    flagged = [(t, d) for t, d in dossiers.items() if d.get("signals", 0) > 0]
    flagged.sort(key=lambda x: x[1]["signals"], reverse=True)
    if not flagged:
        L.append("_(nenhum sinal crítico flagged automaticamente)_")
        return "\n".join(L)
    L.append(f"**{len(flagged)} tickers com sinais flagged**:")
    L.append("")
    for t, d in flagged[:15]:
        L.append(f"### [[{t}]]")
        L.append(f"- {d['signals']} signals · {d['novel']} novel filings")
        if d.get("critical"):
            crit = d["critical"].lstrip("-").strip()
            L.append(f"- {crit[:240]}")
        L.append("")
    return "\n".join(L)


def compose_master_report(phase_results: list[dict],
                            dossiers: dict) -> str:
    L = []
    L.append(f"# Overnight Deep Dive — Manhã de {TOMORROW}")
    L.append("")
    L.append("> Bom dia. Este é o relatório consolidado da sessão "
             "overnight. Lê este ficheiro primeiro. Para detalhes por "
             "ticker, abre `[[ITSA4]]` etc.")
    L.append("")

    # Summary stats
    total_tickers = sum(p["n"] for p in phase_results)
    total_elapsed = sum(p["elapsed_s"] for p in phase_results
                        if p["elapsed_s"] > 0)
    total_novel = sum(d.get("novel", 0) for d in dossiers.values())
    total_signals = sum(d.get("signals", 0) for d in dossiers.values())

    L.append("## 📊 Estatísticas do overnight")
    L.append("")
    L.append(f"- **Tickers cobertos**: {total_tickers}")
    L.append(f"- **Dossiers gerados**: {len(dossiers)}")
    L.append(f"- **Filings novos descobertos**: {total_novel}")
    L.append(f"- **Sinais críticos auto-flagged**: {total_signals}")
    L.append(f"- **Tempo total de execução**: "
             f"{total_elapsed/60:.1f}min ({total_elapsed/3600:.1f}h)")
    L.append("")
    L.append("**Por phase**:")
    L.append("")
    L.append("| Phase | Tickers | Tempo (min) | Status |")
    L.append("|---|---|---|---|")
    for p in phase_results:
        st = ("OK" if p.get("rc") == 0 else
              "TIMEOUT" if p.get("status") == "timeout" else
              "ERROR")
        elapsed_min = (f"{p['elapsed_s']/60:.1f}"
                       if p["elapsed_s"] > 0 else "-")
        L.append(f"| {p['phase']} | {p['n']} | {elapsed_min} | {st} |")
    L.append("")

    # Cash allocation
    L.append(cash_allocation_section(dossiers))

    # Critical signals
    L.append(critical_signals_section(dossiers))

    # Per-ticker index
    L.append("## 📂 Index por ticker")
    L.append("")
    by_market: dict = {"BR": [], "US": []}
    urls_data = load_yaml()
    for t, d in sorted(dossiers.items()):
        market = (urls_data.get(t, {}).get("market") or "?").upper()
        is_h = urls_data.get(t, {}).get("is_holding", False)
        line = (f"- [[{t}]] — "
                f"{'**HOLDING**' if is_h else 'watchlist'} · "
                f"{d.get('novel', 0)} novel · "
                f"{d.get('signals', 0)} signals")
        by_market.setdefault(market, []).append(line)
    for mkt in ("BR", "US"):
        if by_market.get(mkt):
            L.append(f"### {mkt}")
            L.append("")
            L.extend(by_market[mkt])
            L.append("")

    # Errors / coding issues placeholder
    L.append("## 🐛 Erros e issues encontrados durante a sessão")
    L.append("")
    err_log = ROOT / "logs" / f"overnight_{TOMORROW}.log"
    if err_log.exists():
        text = err_log.read_text(encoding="utf-8", errors="replace")
        err_lines = [ln for ln in text.splitlines()
                     if any(kw in ln for kw in
                            ('"event": "ticker_fail"',
                             '"event": "extract_fail"',
                             '"event": "phase_timeout"',
                             '"event": "phase_stderr"'))]
        if err_lines:
            L.append(f"**{len(err_lines)} eventos de erro registados**:")
            L.append("")
            L.append("```json")
            L.extend(err_lines[:20])
            L.append("```")
            if len(err_lines) > 20:
                L.append(f"_... e mais {len(err_lines) - 20} no log._")
        else:
            L.append("_(nenhum erro de execução registado)_")
    L.append("")

    L.append("## 🔄 Como rodar de novo")
    L.append("")
    L.append("```powershell")
    L.append("# Re-run phase específica")
    L.append(".venv\\Scripts\\python.exe scripts/overnight_orchestrator.py --phase holdings_us")
    L.append("# Single ticker re-scrape")
    L.append(".venv\\Scripts\\python.exe scripts/pilot_deep_dive.py --tickers ITSA4 --force-fresh")
    L.append("```")
    L.append("")

    L.append("---")
    L.append(f"_Generated by `scripts/overnight_orchestrator.py` at "
             f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    L.append(f"_Logs: `logs/overnight_{TOMORROW}.log`_")

    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default=None,
                    choices=PHASES + ["all"])
    ap.add_argument("--skip-extract", action="store_true",
                    help="Skip PDF download/extract (faster, less depth)")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _log({"event": "orchestrator_start", "out": str(OUT_DIR),
          "phase": args.phase})

    urls_data = load_yaml()
    if not urls_data:
        _log({"event": "abort", "reason": "no ri_urls.yaml found"})
        print("ERROR: config/ri_urls.yaml not found. Run ri_url_resolver.py first.",
              file=sys.stderr)
        sys.exit(1)

    phases = PHASES if args.phase in (None, "all") else [args.phase]
    phase_results = []
    for phase in phases:
        tickers = get_phase_tickers(phase, urls_data)
        _log({"event": "phase_planned", "phase": phase, "n": len(tickers)})
        r = run_phase(phase, tickers, skip_extract=args.skip_extract)
        phase_results.append(r)

    # Compose master morning report
    dossiers = collect_dossiers()
    master = compose_master_report(phase_results, dossiers)
    out_path = OUT_DIR / "_LEITURA_DA_MANHA.md"
    out_path.write_text(master, encoding="utf-8")
    _log({"event": "master_saved", "path": str(out_path.relative_to(ROOT)),
          "dossiers": len(dossiers)})

    print(f"\n=== ORCHESTRATOR DONE ===")
    print(f"Output: {OUT_DIR}")
    print(f"Master: {out_path}")


if __name__ == "__main__":
    main()
