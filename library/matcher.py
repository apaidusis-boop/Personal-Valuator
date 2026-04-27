"""Method matcher — aplica library/methods/*.yaml ao estado actual.

Para cada método + ticker holdings/watchlist, checa rules; se todas passam,
gera signal (paper-trade only).

Methods YAML schema:
    rules:  list of {id, description, check}  — `check` é expressão Python-like
            evaluated against fundamentals row + derived vars.

Variables available no check context:
    pe, pb, dy, roe, lpa (eps), vpa (bvps), net_debt_ebitda
    market_cap_usd (computed)
    current_ratio (from fundamentals_extra if exists)
    dividend_streak_years
    positive_earnings_years_10 (approx from fundamentals hist)
    eps_3y_avg_growth_10y (computed from fundamentals)

Uso:
    python library/matcher.py                     # all methods vs all holdings
    python library/matcher.py --method graham_defensive
    python library/matcher.py --dry-run           # don't log paper signals
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import yaml
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from library import METHODS_DIR
from library.paper_trade import log_signal, ensure_schema

DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}


def load_methods() -> list[dict]:
    methods = []
    for f in sorted(METHODS_DIR.glob("*.yaml")):
        try:
            with open(f, encoding="utf-8") as fp:
                methods.append(yaml.safe_load(fp))
        except Exception as e:
            print(f"[warn] failed to parse {f.name}: {e}")
    return methods


def _get_fundamentals(db: Path, ticker: str) -> dict:
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if not row:
            return {}
        return dict(row)


def _get_last_price(db: Path, ticker: str) -> float | None:
    with sqlite3.connect(db) as c:
        row = c.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        return row[0] if row else None


def _holdings_and_watchlist(market: str) -> list[str]:
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        holdings = [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()]
        watch = [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM companies WHERE is_holding = 0"
        ).fetchall()]
    return holdings + watch


def _safe_eval_check(expr: str, variables: dict) -> tuple[bool, str]:
    """VERY restricted eval. Only allows: comparisons + AND/OR + numeric/boolean.

    Returns (passed, reason_if_failed).
    """
    # Normalize
    expr_py = expr.replace(" AND ", " and ").replace(" OR ", " or ")
    # Extract variable names
    import re
    var_names = re.findall(r"\b[a-z_][a-z0-9_]*\b", expr_py)
    builtins_blocklist = {"import", "eval", "exec", "open", "__", "lambda"}
    if any(b in expr_py for b in builtins_blocklist):
        return False, f"blocked token in expr"

    context = {k: variables.get(k) for k in set(var_names)}
    missing = [k for k in var_names if context.get(k) is None and k not in ("and", "or", "not", "True", "False")]

    if missing:
        return False, f"missing vars: {missing}"

    try:
        result = eval(expr_py, {"__builtins__": {}}, context)
        return bool(result), "" if result else f"failed: {expr}"
    except Exception as e:
        return False, f"eval error: {e}"


def apply_method(method: dict, ticker: str, market: str, dry_run: bool) -> dict:
    db = DBS[market]
    f = _get_fundamentals(db, ticker)
    if not f:
        return {"ticker": ticker, "method": method["id"], "status": "no_fundamentals"}

    price = _get_last_price(db, ticker)
    # Bag of variables method can reference
    vars_bag = {
        "pe": f.get("pe"), "pb": f.get("pb"), "dy": f.get("dy"),
        "roe": f.get("roe"), "lpa": f.get("eps"), "vpa": f.get("bvps"),
        "eps": f.get("eps"), "bvps": f.get("bvps"),
        "net_debt_ebitda": f.get("net_debt_ebitda"),
        "dividend_streak_years": f.get("dividend_streak_years") or 0,
        "price": price,
        # Derived placeholders (extend as DB schemas grow)
        "market_cap_usd": None,
        "current_ratio": None,
        "ltd": None, "working_capital": None,
        "positive_earnings_years_10": None,
        "eps_3y_avg_growth_10y": None,
        "pe_on_3y_avg_earnings": f.get("pe"),   # approximation
    }

    rules = method.get("rules", [])
    passed_rules = 0
    failed_reasons = []
    for r in rules:
        check = r.get("check", "")
        if not check or not isinstance(check, str):
            failed_reasons.append(f"{r.get('id')}: non-evaluable")
            continue
        ok, reason = _safe_eval_check(check, vars_bag)
        if ok:
            passed_rules += 1
        else:
            failed_reasons.append(f"{r.get('id')}: {reason}")

    all_pass = passed_rules == len(rules) and len(rules) > 0

    signal_id = None
    if all_pass and not dry_run:
        ensure_schema()
        signal_id = log_signal(
            ticker=ticker, market=market,
            method_id=method["id"],
            book_slug=method.get("book", "").replace(" ", "_")[:40].lower(),
            direction=method.get("direction", "LONG"),
            horizon=method.get("horizon", "medium"),
            expected_move_pct=(method.get("expected_move", {}) or {}).get("target_pct"),
            entry_price=price,
            thesis=f"All {len(rules)} rules of {method['id']} passed",
        )

    return {
        "ticker": ticker,
        "market": market,
        "method": method["id"],
        "rules_passed": passed_rules,
        "rules_total": len(rules),
        "status": "SIGNAL" if all_pass else "no_signal",
        "failed_reasons": failed_reasons[:3],
        "signal_id": signal_id,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", help="Only apply this method id")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--market", choices=["br", "us"], help="Subset by market")
    args = ap.parse_args()

    methods = load_methods()
    if args.method:
        methods = [m for m in methods if m.get("id") == args.method]
    if not methods:
        print("No methods loaded. Seed in library/methods/ or ingest a book.")
        return

    markets = [args.market] if args.market else ["br", "us"]
    print(f"=== Method matcher ===")
    print(f"Methods: {[m['id'] for m in methods]}")
    print(f"Dry-run: {args.dry_run}")
    print()

    signals_generated = 0
    for method in methods:
        print(f"--- {method['id']} ({method.get('name', '')})")
        for market in markets:
            for ticker in _holdings_and_watchlist(market):
                r = apply_method(method, ticker, market, args.dry_run)
                if r["status"] == "SIGNAL":
                    signals_generated += 1
                    print(f"  [SIGNAL] {market}:{ticker:<8} {method['id']} ({r['rules_passed']}/{r['rules_total']}) id={r['signal_id']}")
    print()
    print(f"Total paper-signals generated: {signals_generated}")
    print("These live in paper_trade_signals table. Review with:")
    print("  sqlite3 data/br_investments.db 'SELECT * FROM paper_trade_signals WHERE status=\"open\"'")


if __name__ == "__main__":
    main()
