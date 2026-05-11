"""Pipeline diário US.

Corre em sequência:
  1. yf_us_fetcher para cada ticker em us.holdings + us.watchlist
  2. sec_edgar_fetcher — cross-validation do streak + flag is_aristocrat
  3. scoring US (critérios Buffett) contra todo o universo

Reporta sumário final (OK/BAD + passes screen).
Não aborta num erro individual.

Uso:
    python scripts/daily_update_us.py               # default: 3mo
    python scripts/daily_update_us.py --full        # 5y
    python scripts/daily_update_us.py --only yf     # só 1 etapa
    python scripts/daily_update_us.py --skip-sec    # salta SEC EDGAR
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from agents._common import section as _section  # noqa: E402  shared banner


def _load_universe() -> list[str]:
    data = yaml.safe_load((ROOT / "config" / "universe.yaml").read_text(encoding="utf-8"))
    us = data.get("us", {})
    tickers: list[str] = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        g = us.get(bucket) or {}
        for e in (g.get("stocks") or []):
            tickers.append(e["ticker"])
    ka_path = ROOT / "config" / "kings_aristocrats.yaml"
    if ka_path.exists():
        ka = yaml.safe_load(ka_path.read_text(encoding="utf-8")) or {}
        seen = set(tickers)
        for e in (ka.get("tickers") or []):
            t = e.get("ticker")
            if t and t not in seen:
                tickers.append(t)
                seen.add(t)
    return tickers


def step_yf(tickers: list[str], period: str) -> dict:
    _section(f"1/3  yfinance US  (period={period})")
    from fetchers.yf_us_fetcher import run
    ok = []; bad = []
    for t in tickers:
        try:
            r = run(t, period=period)
            ok.append((t, r["prices"], r["dividends"]))
        except Exception as e:
            bad.append((t, str(e)[:80]))
    return {"ok": ok, "bad": bad}


def step_sec(tickers: list[str]) -> dict:
    _section("2/3  SEC EDGAR — cross-validate streak + is_aristocrat")
    from fetchers.sec_edgar_fetcher import run_all as sec_run
    results = sec_run(tickers, dry_run=False)
    ok = [r for r in results if r["status"] == "ok"]
    aristocrats = [r for r in ok if r.get("is_aristocrat")]
    return {"results": results, "aristocrats": aristocrats}


def step_scoring(tickers: list[str]) -> dict:
    _section("3/3  scoring US")
    from scoring.engine import run as score_run
    passed = []; failed = []; errors = []
    for t in tickers:
        try:
            r = score_run(t, "us")
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
    _section(f"SUMÁRIO US  ({dur:.1f}s)")

    yf = results["yf"]
    print(f"[yfinance]  OK {len(yf['ok'])}  BAD {len(yf['bad'])}")
    for t, err in yf["bad"]:
        print(f"            BAD {t}: {err}")

    sec = results.get("sec")
    if sec:
        arists = [r["ticker"] for r in sec["aristocrats"]]
        print(f"[sec_edgar] processados {len(sec['results'])}  aristocrats {len(arists)}: "
              f"{', '.join(arists[:12])}{'...' if len(arists) > 12 else ''}")

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
    ap.add_argument("--full", action="store_true", help="fetch 5y histórico (default: 3mo)")
    ap.add_argument("--only", choices=["yf", "sec", "scoring"], help="correr apenas uma etapa")
    ap.add_argument("--skip-sec", action="store_true", help="salta cross-validation SEC")
    args = ap.parse_args()

    tickers = _load_universe()
    print(f"Universo US: {len(tickers)} tickers")

    period = "5y" if args.full else "3mo"
    start = time.time()
    results: dict = {}

    def run_step(name, fn, *a):
        if args.only and args.only != name:
            return None
        return fn(*a)

    results["yf"] = run_step("yf", step_yf, tickers, period) or {"ok": [], "bad": []}
    if not args.skip_sec:
        results["sec"] = run_step("sec", step_sec, tickers) or {"results": [], "aristocrats": []}
    results["scoring"] = run_step("scoring", step_scoring, tickers) or {"passed": [], "failed": [], "errors": []}

    summary(results, start)


if __name__ == "__main__":
    main()
