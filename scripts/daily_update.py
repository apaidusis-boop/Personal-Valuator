"""Pipeline diário consolidado — BR.

Corre em sequência:
  1. BCB SGS (SELIC, CDI, IPCA, PTAX) — últimos 30 dias
  2. yfinance BR: preços + dividendos para todos os stocks e FIIs do universo
  3. fiis.com.br (+ fallback Status Invest) para fundamentals de FIIs
  4. recompute_fii_streaks — streaks a partir de dividends
  5. scoring BR: corre o engine contra toda a watchlist e persiste scores

Reporta sumário final com:
  - séries populadas
  - tickers OK/BAD
  - top N do ranking do dia

Não aborta num erro individual — colecciona e prossegue.

Uso:
    python scripts/daily_update.py             # default: tudo, 30 dias macro
    python scripts/daily_update.py --full      # fetch 5y histórico
    python scripts/daily_update.py --skip-fii  # só stocks
    python scripts/daily_update.py --only yf   # só fetcher yfinance
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402


def _section(label: str) -> None:
    print(f"\n{'=' * 60}\n== {label}\n{'=' * 60}")


def _load_universe() -> tuple[list[str], list[str]]:
    data = yaml.safe_load((ROOT / "config" / "universe.yaml").read_text(encoding="utf-8"))
    br = data.get("br", {})
    stocks: list[str] = []
    fiis: list[str] = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        g = br.get(bucket) or {}
        for e in (g.get("stocks") or []):
            stocks.append(e["ticker"])
        for e in (g.get("fiis") or []):
            fiis.append(e["ticker"])
    return stocks, fiis


def step_bcb(days: int) -> dict:
    _section(f"1/5  BCB SGS  (macro, {days}d)")
    from fetchers.bcb_fetcher import SGS_MAP, run
    ok = []; bad = []
    for sid in SGS_MAP:
        try:
            n = run(sid, days=days)
            ok.append((sid, n))
        except Exception as e:
            bad.append((sid, str(e)[:80]))
    return {"ok": ok, "bad": bad}


def step_yf(stocks: list[str], fiis: list[str], period: str, skip_fii: bool) -> dict:
    _section(f"2/5  yfinance BR  (period={period})")
    from fetchers.yf_br_fetcher import run
    targets = stocks + ([] if skip_fii else fiis)
    ok = []; bad = []
    for t in targets:
        try:
            r = run(t, period=period)
            ok.append((t, r["prices"], r["dividends"]))
        except Exception as e:
            bad.append((t, str(e)[:80]))
    return {"ok": ok, "bad": bad}


def step_fiis(fiis: list[str], skip_fii: bool) -> dict:
    _section("3/5  fiis.com.br + fallback Status Invest")
    if skip_fii:
        print("  (skip)")
        return {"ok": [], "bad": []}
    from fetchers.fiis_fetcher import run
    ok = []; bad = []
    for t in fiis:
        try:
            r = run(t, force=True)
            (ok if r else bad).append(t)
        except Exception as e:
            bad.append((t, str(e)[:80]))
    return {"ok": ok, "bad": bad}


def step_streaks(skip_fii: bool) -> dict:
    _section("4/5  recompute FII streaks")
    if skip_fii:
        print("  (skip)")
        return {}
    import scripts.recompute_fii_streaks as rs
    rs.main()
    return {}


def step_scoring(stocks: list[str], fiis: list[str], skip_fii: bool) -> dict:
    _section("5/5  scoring BR")
    from scoring.engine import run as score_run
    passed = []; failed = []; errors = []
    targets = stocks + ([] if skip_fii else fiis)
    for t in targets:
        try:
            r = score_run(t, "br")
            if r["passes_screen"]:
                passed.append((t, r["score"]))
            else:
                failed.append((t, r["score"]))
        except SystemExit as e:
            errors.append((t, str(e)[:80]))
        except Exception as e:
            errors.append((t, str(e)[:80]))
    return {"passed": passed, "failed": failed, "errors": errors}


def summary(results: dict, start_ts: float) -> None:
    dur = time.time() - start_ts
    _section(f"SUMÁRIO  ({dur:.1f}s)")

    bcb = results["bcb"]
    print(f"[BCB]       OK {len(bcb['ok'])}  BAD {len(bcb['bad'])}")
    for sid, n in bcb["ok"]:
        print(f"            {sid}: {n} rows")
    for sid, err in bcb["bad"]:
        print(f"            BAD {sid}: {err}")

    yf = results["yf"]
    print(f"[yfinance]  OK {len(yf['ok'])}  BAD {len(yf['bad'])}")
    for t, err in yf["bad"]:
        print(f"            BAD {t}: {err}")

    fi = results["fiis"]
    print(f"[fiis.com]  OK {len(fi['ok'])}  BAD {len(fi['bad'])}")
    for b in fi["bad"]:
        print(f"            BAD {b}")

    sc = results["scoring"]
    print(f"[scoring]   PASS {len(sc['passed'])}  FAIL {len(sc['failed'])}  ERR {len(sc['errors'])}")
    if sc["passed"]:
        print("  Passes screen:")
        for t, s in sorted(sc["passed"], key=lambda x: x[1], reverse=True):
            print(f"    {t}: score={s}")
    if sc["errors"]:
        print("  Errors:")
        for t, e in sc["errors"][:10]:
            print(f"    {t}: {e}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="fetch 5y histórico (default: 60 dias)")
    ap.add_argument("--macro-days", type=int, default=60)
    ap.add_argument("--skip-fii", action="store_true")
    ap.add_argument("--only", choices=["bcb", "yf", "fiis", "streaks", "scoring"],
                    help="correr apenas uma etapa")
    args = ap.parse_args()

    stocks, fiis = _load_universe()
    print(f"Universo: {len(stocks)} stocks, {len(fiis)} fiis")

    period = "5y" if args.full else "3mo"
    macro_days = 1850 if args.full else args.macro_days

    start = time.time()
    results: dict = {}

    def run_step(name, fn, *a):
        if args.only and args.only != name:
            return None
        return fn(*a)

    results["bcb"] = run_step("bcb", step_bcb, macro_days) or {"ok": [], "bad": []}
    results["yf"] = run_step("yf", step_yf, stocks, fiis, period, args.skip_fii) or {"ok": [], "bad": []}
    results["fiis"] = run_step("fiis", step_fiis, fiis, args.skip_fii) or {"ok": [], "bad": []}
    results["streaks"] = run_step("streaks", step_streaks, args.skip_fii) or {}
    results["scoring"] = run_step("scoring", step_scoring, stocks, fiis, args.skip_fii) or {"passed": [], "failed": [], "errors": []}

    summary(results, start)


if __name__ == "__main__":
    main()
