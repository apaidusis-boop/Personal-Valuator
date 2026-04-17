"""Deep-dive single-ticker — tudo o que o sistema sabe sobre um ticker.

Junta num único relatório (sem tocar na rede):
  - Identidade + status na carteira (holding + cost basis + P&L)
  - Price action (1d/YTD/1y/5y)
  - Fundamentals + screen verdict (usa scoring.engine)
  - Histórico de dividendos (por ano) + DY implícito
  - Eventos CVM (BR) ou SEC (US) nos últimos 90d
  - Peer comparison (outras holdings/watchlist do mesmo sector)
  - DRIP projection forward 5/10/15y (mesma lógica de drip_projection.py)

Corre em <3 segundos. Auto-detecta mercado.

Uso:
    python scripts/analyze_ticker.py ITSA4
    python scripts/analyze_ticker.py JNJ --market us
    python scripts/analyze_ticker.py BPAC11 --md
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORTS = ROOT / "reports"


def _detect_market(ticker: str) -> str:
    for db, mk in [(DB_BR, "br"), (DB_US, "us")]:
        with sqlite3.connect(db) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
            r = c.execute("SELECT 1 FROM prices WHERE ticker=? LIMIT 1", (ticker,)).fetchone()
            if r:
                return mk
    raise SystemExit(f"{ticker} não encontrado em nenhuma DB — corre yf_{'br' if 'SA' in ticker.upper() else 'us'}_fetcher.py {ticker}")


def _price_on_or_before(conn, ticker, target_date):
    r = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, target_date),
    ).fetchone()
    return r


def _section(title: str, out: list, char="═"):
    out.append("")
    out.append(char * 76)
    out.append(title)
    out.append(char * 76)


def analyze(ticker: str, market: str) -> str:
    db = DB_BR if market == "br" else DB_US
    ccy_sym = "R$" if market == "br" else "$"
    conn = sqlite3.connect(db)
    out: list[str] = []

    # === 1. Identidade ===
    comp = conn.execute(
        "SELECT ticker, name, sector, is_holding FROM companies WHERE ticker=?", (ticker,)
    ).fetchone()
    if not comp:
        raise SystemExit(f"{ticker} não está em companies")
    tk, name, sector, is_holding = comp

    _section(f"ANÁLISE {tk} — {name}", out)
    out.append(f"  Mercado : {market.upper()}")
    out.append(f"  Sector  : {sector or '-'}")
    out.append(f"  Status  : {'HOLDING' if is_holding else 'watchlist / universe'}")

    # === 2. Posição na carteira (se for holding real) ===
    pos_rows = conn.execute(
        "SELECT quantity, entry_price, entry_date FROM portfolio_positions "
        "WHERE ticker=? AND active=1 AND quantity>0", (tk,)
    ).fetchall()
    last_px = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (tk,)
    ).fetchone()
    px_today = last_px[1] if last_px else None
    if pos_rows and px_today:
        tot_qty = sum(r[0] for r in pos_rows)
        avg_cost = sum(r[0] * r[1] for r in pos_rows) / tot_qty
        mv = tot_qty * px_today
        cost = tot_qty * avg_cost
        pnl = mv - cost
        _section("POSIÇÃO NA CARTEIRA", out)
        out.append(f"  Quantidade  : {tot_qty:,.2f}")
        out.append(f"  Preço médio : {ccy_sym} {avg_cost:,.2f}")
        out.append(f"  Último preço: {ccy_sym} {px_today:,.2f}  ({last_px[0]})")
        out.append(f"  MV          : {ccy_sym} {mv:,.2f}")
        out.append(f"  P&L         : {ccy_sym} {pnl:+,.2f}  ({pnl/cost*100:+.2f}%)")

    # === 3. Price action ===
    if px_today:
        today = last_px[0]
        def ret(days):
            target = (datetime.fromisoformat(today) - timedelta(days=days)).date().isoformat()
            prev = _price_on_or_before(conn, tk, target)
            if not prev:
                return None, None
            return prev[0], (px_today / prev[1] - 1) * 100

        ytd_start = f"{today[:4]}-01-01"
        ytd_row = _price_on_or_before(conn, tk, ytd_start)
        ytd = (px_today / ytd_row[1] - 1) * 100 if ytd_row else None

        d1 = ret(1); d30 = ret(30); y1 = ret(365); y5 = ret(365*5)

        _section("PRICE ACTION", out)
        out.append(f"  Último   : {ccy_sym} {px_today:,.2f}  ({today})")
        if d1[1] is not None:  out.append(f"  1 dia    : {d1[1]:+6.2f}%")
        if d30[1] is not None: out.append(f"  30 dias  : {d30[1]:+6.2f}%")
        if ytd is not None:    out.append(f"  YTD      : {ytd:+6.2f}%")
        if y1[1] is not None:  out.append(f"  1 ano    : {y1[1]:+6.2f}%")
        if y5[1] is not None:  out.append(f"  5 anos   : {y5[1]:+6.2f}%  (CAGR {((1+y5[1]/100)**(1/5)-1)*100:.2f}%)")

    # === 4. Fundamentals + screen verdict ===
    fund = None
    try:
        fund = conn.execute(
            """SELECT period_end, eps, bvps, roe, pe, pb, dy, net_debt_ebitda,
                      dividend_streak_years, is_aristocrat, dividend_streak_source
               FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (tk,),
        ).fetchone()
    except sqlite3.OperationalError:
        pass

    if fund:
        _section("FUNDAMENTALS", out)
        period, eps, bvps, roe, pe, pb, dy, nde, streak, arist, src = fund
        out.append(f"  Período    : {period}")
        out.append(f"  P/E        : {pe if pe is not None else '-'}")
        out.append(f"  P/B        : {pb if pb is not None else '-'}")
        out.append(f"  DY         : {dy*100 if dy else 0:.2f}%")
        out.append(f"  ROE        : {roe*100 if roe else 0:.2f}%")
        out.append(f"  EPS / BVPS : {eps} / {bvps}")
        if nde is not None: out.append(f"  Div.liq/EBITDA : {nde:.2f}")
        if streak is not None:
            tag = " [ARISTOCRAT]" if arist else ""
            src_tag = f" (source: {src})" if src else ""
            out.append(f"  Streak div : {streak} anos{tag}{src_tag}")

    # Screen verdict — chama scoring.engine
    try:
        from scoring.engine import (
            load_snapshot, load_fii_snapshot,
            score_br, score_br_bank, score_br_fii,
            score_us, score_us_reit,
            _is_bank, _is_reit, _selic_real_bcb, aggregate,
            _is_fii_ticker,
        )
        # Fix: tickers ending in "11" podem ser UNITs bancárias (BPAC11, TAEE11,
        # SANB11), não FIIs. O discriminador real é se tem row em fii_fundamentals.
        has_fii_row = conn.execute(
            "SELECT 1 FROM fii_fundamentals WHERE ticker=? LIMIT 1", (tk,)
        ).fetchone() is not None
        is_fii = market == "br" and _is_fii_ticker(tk) and has_fii_row
        if is_fii:
            snap = load_fii_snapshot(conn, tk)
            details = score_br_fii(snap, selic_real=_selic_real_bcb(conn)) if snap else None
        else:
            snap = load_snapshot(conn, tk)
            if snap is None:
                details = None
            elif market == "br" and _is_bank(snap):
                details = score_br_bank(snap)
            elif market == "us" and _is_reit(snap):
                details = score_us_reit(snap)
            else:
                details = (score_br if market == "br" else score_us)(snap)
        if details:
            sc, passes = aggregate(details)
            _section(f"SCREEN VERDICT  —  {'✓ PASSA' if passes else '✗ falha'}  score={sc:.2f}", out)
            for crit, d in details.items():
                verdict = d["verdict"]
                sym_v = {"pass": "✓", "fail": "✗", "n/a": "○"}.get(verdict, "?")
                val = d.get("value"); th = d.get("threshold")
                reason = d.get("reason") or d.get("kind") or ""
                val_s = f"{val:.4f}" if isinstance(val, (int, float)) else str(val)
                th_s = f"{th:.4f}" if isinstance(th, (int, float)) else str(th)
                out.append(f"  {sym_v} {crit:<22} val={val_s:<12} thr={th_s:<10}  {reason}")
    except Exception as e:
        out.append(f"  [scoring error: {str(e)[:120]}]")

    # === 5. Dividend history ===
    divs_rows = conn.execute(
        "SELECT substr(ex_date,1,4) y, SUM(amount) FROM dividends WHERE ticker=? AND amount>0 "
        "GROUP BY 1 ORDER BY 1", (tk,)
    ).fetchall()
    if divs_rows:
        _section(f"DIVIDENDOS — {len(divs_rows)} anos de histórico", out)
        # últimos 10 anos
        for y, total in divs_rows[-10:]:
            # DY implícito: usa preço médio do ano (se temos)
            prices_year = conn.execute(
                "SELECT AVG(close) FROM prices WHERE ticker=? AND substr(date,1,4)=?", (tk, y)
            ).fetchone()
            avg_px = prices_year[0] if prices_year else None
            dy_implied = (total / avg_px * 100) if avg_px else 0
            out.append(f"  {y}  {ccy_sym} {total:>8.4f}/share  (avg px {ccy_sym}{avg_px or 0:>7.2f}, DY≈{dy_implied:>5.2f}%)")

    # === 6. Eventos (CVM/SEC) últimos 90d ===
    cutoff = (date.today() - timedelta(days=90)).isoformat()
    ev = conn.execute(
        "SELECT event_date, source, kind, substr(summary,1,80) FROM events "
        "WHERE ticker=? AND event_date>=? ORDER BY event_date DESC LIMIT 15",
        (tk, cutoff),
    ).fetchall()
    if ev:
        _section(f"EVENTOS últimos 90 dias  ({len(ev)} filings)", out)
        for d, src, kind, summ in ev:
            out.append(f"  {d}  {src:<4}  {kind:<20}  {summ or ''}")

    # === 7. Peer comparison (mesmo sector) ===
    if sector:
        peers = conn.execute(
            "SELECT c.ticker, c.name, c.is_holding, f.pe, f.pb, f.roe, f.dy, "
            "       f.dividend_streak_years "
            "FROM companies c LEFT JOIN fundamentals f ON f.ticker=c.ticker "
            "WHERE c.sector=? AND c.ticker != ? "
            "AND (f.period_end = (SELECT MAX(period_end) FROM fundamentals WHERE ticker=c.ticker)"
            "     OR f.period_end IS NULL) "
            "ORDER BY c.is_holding DESC, c.ticker", (sector, tk),
        ).fetchall()
        if peers:
            _section(f"PEERS no sector {sector!r}  ({len(peers)} tickers)", out)
            out.append(f"  {'Ticker':<8}{'Holding':<9}{'P/E':>7}{'P/B':>7}{'ROE':>8}{'DY':>8}{'Streak':>8}  Name")
            for pk, pn, ph, ppe, ppb, proe, pdy, ps in peers[:15]:
                out.append(
                    f"  {pk:<8}{'✓ sim' if ph else '':<9}"
                    f"{(ppe or 0):>7.2f}{(ppb or 0):>7.2f}{(proe or 0)*100:>7.1f}%{(pdy or 0)*100:>7.2f}%"
                    f"{(ps or '-')!s:>8}  {(pn or '')[:30]}"
                )

    # === 8. DRIP projection (se holding ou com dividendo) ===
    if pos_rows:
        try:
            from scripts.drip_projection import (
                derive_scenarios, _annual_divs_per_share, _ttm_div_per_share,
                _latest_fundamentals, project_drip,
            )
            tot_qty = sum(r[0] for r in pos_rows)
            ttm_dps = _ttm_div_per_share(conn, tk, date.today().isoformat())
            annual = _annual_divs_per_share(conn, tk)
            f2 = _latest_fundamentals(conn, tk)
            scen = derive_scenarios(tk, px_today, ttm_dps, annual, f2, conn, sector)
            _section(f"DRIP FORWARD (holding actual) — assumptions kind={scen['debug'].get('kind')}", out)
            out.append(f"  {'Horizonte':<12}{'Conservador':>18}{'Base':>18}{'Optimista':>18}")
            for h in (5, 10, 15):
                vals = {s: project_drip(tot_qty, px_today, ttm_dps,
                                         scen[s]["g"], scen[s]["md"], h)[3]
                        for s in ("conservador", "base", "optimista")}
                out.append(f"  {h}y           {ccy_sym} {vals['conservador']:>14,.0f}"
                          f"{ccy_sym} {vals['base']:>14,.0f}{ccy_sym} {vals['optimista']:>14,.0f}")
        except Exception as e:
            out.append(f"  [drip projection error: {str(e)[:120]}]")

    # === 9. Entry triggers (se não for holding mas tem fundamentals) ===
    if not is_holding and fund and px_today:
        _, eps, bvps, _, pe, pb, _, _, _, _, _ = fund
        _section("ENTRY TRIGGERS (preços que fariam passar critérios-chave)", out)
        if eps and bvps and eps > 0 and bvps > 0:
            import math
            gn = math.sqrt(22.5 * eps * bvps)
            out.append(f"  Graham Number   : {ccy_sym} {gn:>8.2f}  (actual: {ccy_sym} {px_today:,.2f}  diff: {((px_today/gn)-1)*100:+.1f}%)")
        if bvps and bvps > 0:
            target_pb15 = 1.5 * bvps
            target_pb3 = 3.0 * bvps
            out.append(f"  Preço p/ P/B≤1.5: {ccy_sym} {target_pb15:>8.2f}  (screen BR-banco)")
            out.append(f"  Preço p/ P/B≤3  : {ccy_sym} {target_pb3:>8.2f}  (screen US)")

    conn.close()
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"], help="override auto-detect")
    ap.add_argument("--md", action="store_true", help="grava em reports/analyze_<ticker>.md")
    args = ap.parse_args()

    tk = args.ticker.upper()
    market = args.market or _detect_market(tk)
    report = analyze(tk, market)
    print(report)

    if args.md:
        REPORTS.mkdir(exist_ok=True)
        fp = REPORTS / f"analyze_{tk.replace('-','_')}_{date.today().isoformat()}.md"
        fp.write_text(f"# Analyze {tk}  —  {date.today().isoformat()}\n\n```\n{report}\n```\n",
                      encoding="utf-8")
        print(f"\n[md] gravado em {fp}")


if __name__ == "__main__":
    main()
