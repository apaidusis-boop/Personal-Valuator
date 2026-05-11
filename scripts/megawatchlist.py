"""MegaWatchlist — vista unificada dos 108+ tickers BR+US com todas as métricas.

Junta:
  - Identidade        (companies + kings_aristocrats.yaml)
  - Preço + histórico (prices + analytics.metrics)
  - Valuation         (fundamentals: pe, pb, pe_forward, ev_ebitda)
  - Dividendos        (dy, streak, cagr_5y, frequency, next_ex_date)
  - Qualidade         (roe, altman, piotroski cached)
  - Screen            (scores.score, passes_screen)
  - Carteira          (portfolio_positions: qty, mv, % port, p&l)

Uso:
    python scripts/megawatchlist.py                            # tudo, table
    python scripts/megawatchlist.py --market us                # só US
    python scripts/megawatchlist.py --format markdown          # para reports/
    python scripts/megawatchlist.py --only holdings,watchlist  # filtra kind
    python scripts/megawatchlist.py --sort drawdown_52w        # ordenar
    python scripts/megawatchlist.py --only-pass                # só screen PASS
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analytics.metrics import compute_all as metrics_all  # noqa: E402

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
KA = ROOT / "config" / "kings_aristocrats.yaml"
REPORTS = ROOT / "reports"


# ---------------------------------------------------------------------------
# loaders
# ---------------------------------------------------------------------------

def _load_ka_map() -> dict[str, str]:
    if not KA.exists():
        return {}
    data = yaml.safe_load(KA.read_text(encoding="utf-8")) or {}
    return {e["ticker"]: e.get("kind", "") for e in (data.get("tickers") or [])}


def _latest_fundamentals(conn: sqlite3.Connection, ticker: str) -> dict | None:
    r = conn.execute(
        """SELECT pe, pb, dy, roe, net_debt_ebitda, dividend_streak_years,
                  is_aristocrat, pe_forward, ev_ebitda, market_cap,
                  fcf_ttm, shares_outstanding, next_ex_date, next_earnings_date
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    keys = ["pe", "pb", "dy", "roe", "net_debt_ebitda", "streak",
            "is_aristocrat", "pe_forward", "ev_ebitda", "market_cap",
            "fcf_ttm", "shares_out", "next_ex", "next_earnings"]
    return dict(zip(keys, r))


def _latest_price(conn: sqlite3.Connection, ticker: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)
    ).fetchone()
    return r[0] if r else None


def _latest_score(conn: sqlite3.Connection, ticker: str) -> tuple[float | None, bool]:
    r = conn.execute(
        "SELECT score, passes_screen FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if not r:
        return None, False
    return r[0], bool(r[1])


def _position(conn: sqlite3.Connection, ticker: str) -> dict | None:
    r = conn.execute(
        """SELECT quantity, entry_price FROM portfolio_positions
           WHERE ticker=? AND active=1""",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    qty, entry = r
    return {"qty": qty, "entry_price": entry}


def _sector_and_name(conn: sqlite3.Connection, ticker: str) -> tuple[str, str, bool]:
    r = conn.execute(
        "SELECT name, sector, is_holding FROM companies WHERE ticker=?", (ticker,)
    ).fetchone()
    if not r:
        return ticker, "?", False
    return r[0] or ticker, r[1] or "?", bool(r[2])


# ---------------------------------------------------------------------------
# row assembly
# ---------------------------------------------------------------------------

@dataclass
class Row:
    ticker: str
    market: str
    name: str
    sector: str
    kind: str                   # holding / watchlist / king / aristocrat / king_aristocrat
    price: float | None
    mcap_b: float | None        # market cap em bilhões
    pe: float | None
    pe_fwd: float | None
    pb: float | None
    ev_ebitda: float | None
    dy_pct: float | None        # %
    dy_5y_avg_pct: float | None
    roe_pct: float | None       # %
    nd_ebitda: float | None
    streak: int | None
    div_cagr_5y: float | None
    div_freq: str
    screen: float | None
    passes: bool
    drawdown_52w: float | None
    drawdown_5y: float | None
    ytd: float | None
    yoy: float | None
    next_ex: str | None
    next_earn: str | None
    qty: float | None
    mv: float | None
    port_pct: float | None
    pnl_pct: float | None

    @property
    def kind_badge(self) -> str:
        if self.kind == "holding":
            return "⭐ HOLD"
        if self.kind == "king_aristocrat":
            return "K+A"
        if self.kind == "king":
            return "KING"
        if self.kind == "aristocrat":
            return "ARIST"
        if self.kind == "watchlist":
            return "WATCH"
        return "?"


def _build_row(conn: sqlite3.Connection, ticker: str, market: str,
               ka_map: dict[str, str], total_port_mv: float) -> Row:
    name, sector, is_holding = _sector_and_name(conn, ticker)
    f = _latest_fundamentals(conn, ticker) or {}
    price = _latest_price(conn, ticker)
    score, passes = _latest_score(conn, ticker)
    pos = _position(conn, ticker)
    m = metrics_all(conn, ticker)

    kind = "holding" if is_holding else ka_map.get(ticker, "watchlist")

    mv = None; port_pct = None; pnl_pct = None
    if pos and price:
        mv = (pos["qty"] or 0) * price
        if total_port_mv > 0:
            port_pct = 100.0 * mv / total_port_mv
        if pos["entry_price"] and pos["entry_price"] > 0:
            pnl_pct = 100.0 * (price - pos["entry_price"]) / pos["entry_price"]

    mcap = f.get("market_cap")
    mcap_b = mcap / 1e9 if mcap else None
    dy = f.get("dy")
    roe = f.get("roe")

    return Row(
        ticker=ticker, market=market, name=name, sector=sector, kind=kind,
        price=price, mcap_b=mcap_b,
        pe=f.get("pe"), pe_fwd=f.get("pe_forward"), pb=f.get("pb"),
        ev_ebitda=f.get("ev_ebitda"),
        dy_pct=dy * 100 if dy else None,
        dy_5y_avg_pct=m.dy_5y_avg_pct,
        roe_pct=roe * 100 if roe else None,
        nd_ebitda=f.get("net_debt_ebitda"),
        streak=f.get("streak"),
        div_cagr_5y=m.div_cagr_5y_pct,
        div_freq=m.div_frequency,
        screen=score, passes=passes,
        drawdown_52w=m.drawdown_52w, drawdown_5y=m.drawdown_5y,
        ytd=m.ytd, yoy=m.yoy,
        next_ex=f.get("next_ex"), next_earn=f.get("next_earnings"),
        qty=pos["qty"] if pos else None,
        mv=mv, port_pct=port_pct, pnl_pct=pnl_pct,
    )


def _load_market(market: str, ka_map: dict[str, str]) -> list[Row]:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as conn:
        # total portfolio MV para % port
        total_rows = conn.execute(
            """SELECT p.ticker, p.quantity FROM portfolio_positions p
               WHERE p.active=1"""
        ).fetchall()
        total_mv = 0.0
        for t, q in total_rows:
            p = _latest_price(conn, t)
            if p and q:
                total_mv += p * q

        tickers = [r[0] for r in conn.execute(
            "SELECT ticker FROM companies ORDER BY is_holding DESC, ticker"
        ).fetchall()]
        rows = [_build_row(conn, t, market, ka_map if market == "us" else {}, total_mv)
                for t in tickers]
    return rows


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------

def _fmt(v, kind: str = "f", prec: int = 1) -> str:
    if v is None:
        return "—"
    if kind == "pct":
        return f"{v:+.{prec}f}%"
    if kind == "money":
        return f"{v:,.2f}"
    if kind == "b":
        return f"{v:.1f}B"
    return f"{v:.{prec}f}"


def render_table(rows: list[Row], max_rows: int = None) -> str:
    hdr = ("TICKER MK  SECT             KIND   PRICE    P/E P/Efwd   P/B  EV/E  DY%  5yA  ROE% ND/E STK CAGR FREQ     SCR PASS  DD52w  YoY   %PF   P&L%")
    sep = "-" * len(hdr)
    lines = [hdr, sep]
    n_shown = 0
    for r in rows:
        if max_rows and n_shown >= max_rows:
            break
        price_s = f"{r.price:,.2f}" if r.price else "—"
        sect = (r.sector or "?")[:14]
        line = (
            f"{r.ticker:6s} {r.market:2s}  {sect:<16s} {r.kind_badge:<6s} "
            f"{price_s:>7s} "
            f"{_fmt(r.pe, 'f', 1):>6s} "
            f"{_fmt(r.pe_fwd, 'f', 1):>6s} "
            f"{_fmt(r.pb, 'f', 1):>5s} "
            f"{_fmt(r.ev_ebitda, 'f', 1):>5s} "
            f"{_fmt(r.dy_pct, 'f', 2):>5s} "
            f"{_fmt(r.dy_5y_avg_pct, 'f', 1):>4s} "
            f"{_fmt(r.roe_pct, 'f', 1):>5s} "
            f"{_fmt(r.nd_ebitda, 'f', 1):>4s} "
            f"{str(r.streak) if r.streak else '—':>3s} "
            f"{_fmt(r.div_cagr_5y, 'f', 1):>4s} "
            f"{r.div_freq[:8]:<8s} "
            f"{_fmt(r.screen, 'f', 2):>4s} "
            f"{'Y' if r.passes else 'N':>4s} "
            f"{_fmt(r.drawdown_52w, 'f', 1):>6s} "
            f"{_fmt(r.yoy, 'f', 1):>5s} "
            f"{_fmt(r.port_pct, 'f', 1):>5s} "
            f"{_fmt(r.pnl_pct, 'f', 1):>5s}"
        )
        lines.append(line)
        n_shown += 1
    return "\n".join(lines)


def render_markdown(rows: list[Row]) -> str:
    out = [
        f"# MegaWatchlist — {date.today().isoformat()}",
        "",
        f"{len(rows)} tickers. Ordenados por holdings → score desc → ticker.",
        "",
        "| Ticker | Mkt | Sector | Kind | Price | P/E | P/Efwd | P/B | DY% | DY-5y | ROE% | STK | CAGR | Freq | Scr | Pass | DD52w | YoY | %PF | P&L% |",
        "|--------|-----|--------|------|------:|----:|-------:|----:|----:|------:|-----:|---:|-----:|-----:|----:|:----:|------:|----:|----:|----:|",
    ]
    for r in rows:
        price_s = f"{r.price:,.2f}" if r.price else "—"
        out.append(
            f"| {r.ticker} | {r.market} | {r.sector} | {r.kind_badge} | "
            f"{price_s} | {_fmt(r.pe, 'f', 1)} | {_fmt(r.pe_fwd, 'f', 1)} | "
            f"{_fmt(r.pb, 'f', 1)} | {_fmt(r.dy_pct, 'f', 2)} | "
            f"{_fmt(r.dy_5y_avg_pct, 'f', 1)} | {_fmt(r.roe_pct, 'f', 1)} | "
            f"{r.streak or '—'} | {_fmt(r.div_cagr_5y, 'f', 1)} | {r.div_freq} | "
            f"{_fmt(r.screen, 'f', 2)} | {'✅' if r.passes else '—'} | "
            f"{_fmt(r.drawdown_52w, 'f', 1)} | {_fmt(r.yoy, 'f', 1)} | "
            f"{_fmt(r.port_pct, 'f', 1)} | {_fmt(r.pnl_pct, 'f', 1)} |"
        )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# sorting / filtering
# ---------------------------------------------------------------------------

def _sort_key(row: Row, sort_by: str):
    # holdings sempre primeiro, depois por sort_by desc (tratando None como pior)
    val = getattr(row, sort_by, None)
    is_holding = 1 if row.kind == "holding" else 0
    sort_val = -1e18 if val is None else val
    return (-is_holding, -sort_val, row.ticker)


def _apply_filters(rows: list[Row], args) -> list[Row]:
    out = rows
    if args.only:
        kinds = set(k.strip() for k in args.only.split(","))
        out = [r for r in out if r.kind in kinds or (r.kind == "holding" and "holdings" in kinds)]
    if args.only_pass:
        out = [r for r in out if r.passes]
    if args.only_holdings:
        out = [r for r in out if r.kind == "holding"]
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us", "all"], default="all")
    ap.add_argument("--format", choices=["table", "markdown", "json"], default="table")
    ap.add_argument("--sort", default="screen",
                    help="campo para ordenar desc (ex: screen, drawdown_52w, dy_pct)")
    ap.add_argument("--only", help="filtrar por kind (csv): holding,king,aristocrat,...")
    ap.add_argument("--only-pass", action="store_true", help="apenas screen PASS")
    ap.add_argument("--only-holdings", action="store_true", help="apenas posições reais")
    ap.add_argument("--output", help="ficheiro para escrever (default stdout)")
    ap.add_argument("--max-rows", type=int, help="limite de linhas na table view")
    args = ap.parse_args()

    ka_map = _load_ka_map()
    rows: list[Row] = []
    if args.market in ("br", "all"):
        rows.extend(_load_market("br", ka_map))
    if args.market in ("us", "all"):
        rows.extend(_load_market("us", ka_map))

    rows = _apply_filters(rows, args)
    rows.sort(key=lambda r: _sort_key(r, args.sort))

    if args.format == "markdown":
        content = render_markdown(rows)
    elif args.format == "json":
        import json
        content = json.dumps([asdict(r) for r in rows], ensure_ascii=False, indent=2)
    else:
        content = render_table(rows, max_rows=args.max_rows)

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = REPORTS / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"[mwl] escrito: {out_path}")
    else:
        print(content)
    print(f"\n[mwl] {len(rows)} rows · market={args.market} · sort={args.sort}")


if __name__ == "__main__":
    main()
