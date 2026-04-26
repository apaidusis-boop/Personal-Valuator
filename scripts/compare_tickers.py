"""Compare side-by-side 2-N tickers (BR ou US ou mix) contra um benchmark.

Reusa lógica existente:
  - scoring.engine          — verdict de screen (pass/fail) e score
  - scoring.dividend_safety — safety score 0-100
  - scripts.drip_projection — derive_scenarios para TR base/optimista

Uso:
    python scripts/compare_tickers.py JNJ PG KO
    python scripts/compare_tickers.py JNJ PG KO --vs SPY
    python scripts/compare_tickers.py ITSA4 BBDC4 ITUB4 --vs IBOV
    python scripts/compare_tickers.py VALE3 PRIO3 JNJ        # cross-market OK

Zero rede. Só lê as DBs.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analytics.dy_percentile import compute as dy_pctl_compute   # noqa: E402
from scoring.dividend_safety import compute as safety_compute   # noqa: E402
from scripts.drip_projection import _annual_divs_per_share, _latest_fundamentals, _ttm_div_per_share, derive_scenarios

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _db(mkt: str) -> Path:
    return DB_BR if mkt == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mkt in ("br", "us"):
        with sqlite3.connect(_db(mkt)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mkt
    return None


def _dy_percentile_now(conn: sqlite3.Connection, ticker: str, lookback_years: int = 10) -> tuple[float, float, int] | None:
    """Devolve (dy_now_pct, percentile_actual, obs) usando série mensal t12m.

    Thin wrapper sobre analytics.dy_percentile.compute para back-compat tabular.
    """
    r = dy_pctl_compute(conn, ticker, lookback_years=lookback_years, min_obs=1)
    if r is None:
        return None
    return (r.dy_now_pct, r.percentile, r.obs)


def _total_return(conn: sqlite3.Connection, ticker: str, years: int) -> float | None:
    """Total return anualizado aproximado: price CAGR + média DY no período."""
    rows = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date", (ticker,)
    ).fetchall()
    if len(rows) < 60:
        return None
    from datetime import datetime
    last_dt = datetime.fromisoformat(rows[-1][0])
    target = last_dt.replace(year=last_dt.year - years).isoformat()
    first = next(((d, c) for d, c in rows if d >= target), rows[0])
    last = rows[-1]
    yrs = (datetime.fromisoformat(last[0]) - datetime.fromisoformat(first[0])).days / 365.25
    if yrs < 1 or first[1] <= 0:
        return None
    price_cagr = (last[1] / first[1]) ** (1 / yrs) - 1

    # média de DY anual no período
    since = target
    divs = conn.execute(
        "SELECT substr(ex_date,1,4) AS yr, SUM(amount) FROM dividends "
        "WHERE ticker=? AND ex_date>=? GROUP BY yr",
        (ticker, since),
    ).fetchall()
    total_divs = sum(v for _, v in divs if v)
    # dy_avg = total_divs / (preço médio × anos aprox)
    avg_px = (first[1] + last[1]) / 2
    dy_avg = (total_divs / yrs) / avg_px if avg_px else 0
    return price_cagr + dy_avg


def _div_cagr(conn: sqlite3.Connection, ticker: str, years: int = 5) -> float | None:
    rows = conn.execute(
        "SELECT substr(ex_date,1,4) y, SUM(amount) FROM dividends "
        "WHERE ticker=? AND amount>0 GROUP BY y ORDER BY y",
        (ticker,),
    ).fetchall()
    if len(rows) < years + 1:
        return None
    complete = [(int(y), v) for y, v in rows if y and y.isdigit()]
    # usa últimos `years+1` anos completos, ignorando o ano corrente
    today_y = date.today().year
    past = [(y, v) for y, v in complete if y < today_y]
    if len(past) < years + 1:
        return None
    first_y, first_v = past[-years-1]
    last_y, last_v = past[-1]
    if first_v <= 0 or last_v <= 0:
        return None
    return (last_v / first_v) ** (1 / (last_y - first_y)) - 1


def _screen_verdict(conn: sqlite3.Connection, ticker: str, market: str) -> tuple[float | None, bool | None]:
    r = conn.execute(
        "SELECT score, passes_screen FROM scores WHERE ticker=? "
        "ORDER BY run_date DESC LIMIT 1", (ticker,),
    ).fetchone()
    if not r:
        return (None, None)
    return (float(r[0]), bool(r[1]))


def collect(ticker: str) -> dict:
    ticker = ticker.upper()
    mkt = _detect_market(ticker)
    if not mkt:
        return {"ticker": ticker, "market": None, "error": "not_found"}
    with sqlite3.connect(_db(mkt)) as conn:
        last_row = conn.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)
        ).fetchone()
        last_px = last_row[0] if last_row else None
        fund = _latest_fundamentals(conn, ticker)
        ttm = _ttm_div_per_share(conn, ticker, date.today().isoformat())
        annual = _annual_divs_per_share(conn, ticker)
        sec_row = conn.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
        sector = sec_row[0] if sec_row else None

        scen = derive_scenarios(ticker, last_px, ttm, annual, fund, conn, sector) if last_px else {}
        tr_5y = _total_return(conn, ticker, 5)
        tr_10y = _total_return(conn, ticker, 10)
        dcagr_5y = _div_cagr(conn, ticker, 5)
        dy_pct = _dy_percentile_now(conn, ticker)
        score, passes = _screen_verdict(conn, ticker, mkt)

    safety = safety_compute(ticker, mkt)

    current_yield = ttm / last_px if last_px else 0
    tr_base = None
    if scen and scen.get("base"):
        tr_base = current_yield + scen["base"]["g"] + scen["base"]["md"]

    return {
        "ticker": ticker, "market": mkt, "sector": sector, "last_px": last_px,
        "ttm_div_ps": ttm, "current_yield": current_yield,
        "eps": fund.get("eps"), "roe": fund.get("roe"),
        "pe": fund.get("pe"), "pb": fund.get("pb"),
        "streak": fund.get("streak"), "aristocrat": fund.get("aristocrat"),
        "nd_ebitda": fund.get("net_debt_ebitda"),
        "screen_score": score, "screen_passes": passes,
        "safety_score": safety.total if safety else None,
        "safety_verdict": safety.verdict if safety else None,
        "tr_5y": tr_5y, "tr_10y": tr_10y,
        "dcagr_5y": dcagr_5y,
        "dy_percentile": dy_pct,
        "tr_base_forward": tr_base,
        "scen_kind": scen.get("debug", {}).get("kind") if scen else None,
    }


def _fmt_pct(v: float | None, decimals: int = 2) -> str:
    if v is None: return "    —"
    return f"{v*100:>+{6+decimals}.{decimals}f}%"


def _fmt_num(v, fmt: str = ">7.2f", suffix: str = "") -> str:
    if v is None: return "    —"
    return f"{v:{fmt}}{suffix}"


def print_table(rows: list[dict], benchmark: dict | None) -> None:
    # Header + rows
    cols = [
        ("TICKER",       lambda r: f"{r['ticker']}"),
        ("MKT",          lambda r: r["market"] or "?"),
        ("KIND",         lambda r: r.get("scen_kind") or "-"),
        ("PRICE",        lambda r: _fmt_num(r["last_px"])),
        ("DY t12m",      lambda r: _fmt_pct(r["current_yield"])),
        ("DY_PCTL",      lambda r: _fmt_num(r["dy_percentile"][1] if r["dy_percentile"] else None, ">5.0f", "%")),
        ("P/E",          lambda r: _fmt_num(r["pe"])),
        ("P/B",          lambda r: _fmt_num(r["pb"])),
        ("ROE",          lambda r: _fmt_pct(r["roe"] if r["roe"] is None or abs(r["roe"]) > 1.5 else r["roe"]*100) if False else (f"{r['roe']*100:>+6.1f}%" if r["roe"] and abs(r["roe"]) <= 1.5 else (f"{r['roe']:>+6.1f}%" if r["roe"] is not None else "    —"))),
        ("ND/EB",        lambda r: _fmt_num(r["nd_ebitda"])),
        ("STREAK",       lambda r: f"{r['streak']:>3}y" if r["streak"] else "  —"),
        ("SCR",          lambda r: (f"{r['screen_score']:>.2f}" + ("P" if r["screen_passes"] else "F")) if r["screen_score"] is not None else "  —"),
        ("SAFE",         lambda r: (f"{r['safety_score']:>4.0f}/{r['safety_verdict'][:3]}") if r["safety_score"] is not None else "  —"),
        ("div_CAGR 5y",  lambda r: _fmt_pct(r["dcagr_5y"])),
        ("TR 5y",        lambda r: _fmt_pct(r["tr_5y"])),
        ("TR 10y",       lambda r: _fmt_pct(r["tr_10y"])),
        ("TR fwd base",  lambda r: _fmt_pct(r["tr_base_forward"])),
    ]

    widths = [max(len(name), max(len(fn(r)) for r in rows)) for name, fn in cols]

    def _row(cells: list[str]) -> str:
        return "  ".join(c.rjust(w) if i>0 else c.ljust(w) for i, (c, w) in enumerate(zip(cells, widths)))

    header = _row([c[0] for c in cols])
    print()
    print(header)
    print("-" * len(header))
    for r in rows:
        print(_row([fn(r) for _, fn in cols]))
    if benchmark:
        print("-" * len(header))
        print(_row([fn(benchmark) for _, fn in cols]))
    print()


def _index_row(series_id: str, label: str) -> dict | None:
    """Faz uma 'linha fake' para índice (IBOV, SPY...). Usa tabela prices ou series."""
    # tenta como ticker em prices primeiro
    for mkt in ("us", "br"):
        with sqlite3.connect(_db(mkt)) as conn:
            r = conn.execute(
                "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (series_id,)
            ).fetchone()
            if r:
                # tem dados como ticker
                data = collect(series_id)
                data["ticker"] = label
                return data
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="+", help="2+ tickers para comparar")
    ap.add_argument("--vs", help="Benchmark (ex: SPY, IBOV). Opcional.")
    args = ap.parse_args()

    if len(args.tickers) < 2:
        ap.error("pelo menos 2 tickers")

    rows = [collect(t) for t in args.tickers]
    errors = [r for r in rows if r.get("error")]
    for r in errors:
        print(f"[warn] {r['ticker']}: {r['error']}")
    rows = [r for r in rows if not r.get("error")]
    if not rows:
        print("[erro] nenhum ticker válido.")
        return

    bench = _index_row(args.vs.upper(), args.vs.upper()) if args.vs else None

    print_table(rows, bench)
    # summary text com "winners" per metric
    print("WINNERS (entre os tickers, não benchmark):")
    def _best(key, reverse=True):
        vals = [(r["ticker"], r.get(key)) for r in rows if r.get(key) is not None]
        if not vals: return None
        return sorted(vals, key=lambda x: x[1], reverse=reverse)[0]

    picks = {
        "DY mais alto":         _best("current_yield", reverse=True),
        "DY percentile alto":   _best("dy_percentile", reverse=True),  # tuple; custom
        "ROE":                  _best("roe", reverse=True),
        "ND/EB (menor)":        _best("nd_ebitda", reverse=False),
        "Safety score":         _best("safety_score", reverse=True),
        "Screen score":         _best("screen_score", reverse=True),
        "Div CAGR 5y":          _best("dcagr_5y", reverse=True),
        "Total return 5y":      _best("tr_5y", reverse=True),
        "TR forward base":      _best("tr_base_forward", reverse=True),
    }
    for label, pick in picks.items():
        if not pick: continue
        name, val = pick
        if isinstance(val, tuple): val = val[1]   # dy_percentile
        if isinstance(val, float) and abs(val) < 1:
            val_s = f"{val*100:+.2f}%"
        else:
            val_s = f"{val:.2f}"
        print(f"  - {label:<22}: {name} ({val_s})")


if __name__ == "__main__":
    main()
