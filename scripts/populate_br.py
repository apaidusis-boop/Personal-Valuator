"""Populador em lote do mercado BR.

Corre o pipeline completo (yfinance → Status Invest → scoring → valuation)
para todas as acções do universo BR (skip FIIs — critérios diferentes,
ficam para Sprint 2). Tolerante a falhas por ticker: se um falhar, regista
e continua os outros.

Uso:
    python scripts/populate_br.py
    python scripts/populate_br.py --only ITSA4 PRIO3
"""
from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fetchers import yfinance_fetcher, statusinvest_scraper, fii_statusinvest_scraper  # noqa: E402
from scoring import engine as scoring_engine  # noqa: E402
from scoring import valuation  # noqa: E402


def br_stock_tickers(include_watchlist: bool = True) -> list[str]:
    """Holdings BR (stocks) + watchlist BR stocks. FIIs ficam no motor próprio."""
    data = yaml.safe_load((ROOT / "config" / "universe.yaml").read_text(encoding="utf-8"))
    br = data.get("br", {}) or {}
    tickers: list[str] = []
    for entry in (br.get("holdings", {}) or {}).get("stocks", []) or []:
        tickers.append(entry["ticker"])
    if include_watchlist:
        wl = br.get("watchlist", {}) or {}
        if isinstance(wl, dict):
            for entry in wl.get("stocks", []) or []:
                tickers.append(entry["ticker"])
        elif isinstance(wl, list):
            for entry in wl:
                tickers.append(entry["ticker"])
    return tickers


def br_fii_tickers(include_watchlist: bool = True) -> list[str]:
    """Holdings BR (fiis) + watchlist BR fiis."""
    data = yaml.safe_load((ROOT / "config" / "universe.yaml").read_text(encoding="utf-8"))
    br = data.get("br", {}) or {}
    tickers: list[str] = []
    for entry in (br.get("holdings", {}) or {}).get("fiis", []) or []:
        tickers.append(entry["ticker"])
    if include_watchlist:
        wl = br.get("watchlist", {}) or {}
        for entry in (wl.get("fiis", []) or []) if isinstance(wl, dict) else []:
            tickers.append(entry["ticker"])
    return tickers


def _is_fii(ticker: str) -> bool:
    return ticker.endswith("11")


def process(ticker: str) -> tuple[str, bool, str]:
    # Apanha tanto Exception como SystemExit — alguns fetchers (p.ex.
    # yfinance_fetcher quando devolve histórico vazio) chamam sys.exit /
    # raise SystemExit, que não é subclasse de Exception. Sem isto o
    # loop de populate_br abortava no primeiro ticker problemático.
    try:
        if _is_fii(ticker):
            fii_statusinvest_scraper.run(ticker)
            scoring_engine.run(ticker, "br")
            # valuation DDM não se aplica a FIIs (modelo é outro — TODO Sprint 2)
            return ticker, True, "ok (fii)"
        yfinance_fetcher.run(ticker, market="br", period="10y")
        statusinvest_scraper.run(ticker)
        scoring_engine.run(ticker, "br")
        valuation.run(ticker, "br")
        return ticker, True, "ok"
    except KeyboardInterrupt:
        raise
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        return ticker, False, f"{type(exc).__name__}: {exc}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None,
                    help="subconjunto de tickers a processar")
    ap.add_argument("--fiis", action="store_true",
                    help="processar só FIIs do universo BR")
    ap.add_argument("--all", action="store_true",
                    help="processar stocks + FIIs do universo BR")
    args = ap.parse_args()

    if args.only:
        tickers = args.only
    elif args.fiis:
        tickers = br_fii_tickers()
    elif args.all:
        tickers = br_stock_tickers() + br_fii_tickers()
    else:
        tickers = br_stock_tickers()
    print(f"[populate] alvo: {tickers}")

    results = []
    for t in tickers:
        print(f"\n=== {t} ===")
        try:
            r = process(t)
        except KeyboardInterrupt:
            raise
        except (Exception, SystemExit):
            traceback.print_exc()
            r = (t, False, "unexpected")
        results.append(r)

    print("\n=== resumo ===")
    for t, ok, msg in results:
        mark = "[OK]" if ok else "[FAIL]"
        print(f"{mark} {t:6} - {msg}")

    failed = [t for t, ok, _ in results if not ok]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
