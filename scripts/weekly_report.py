"""Relatório semanal consolidado BR + US.

Gera reports/weekly_YYYY-MM-DD.html com visão de todo o universo:
  1. Dashboard de carteira (holdings) com scores e verdicts
  2. Watchlist screening (quem passa / não passa o filtro)
  3. Top oportunidades (score alto + BUY)
  4. Red flags e gaps de cobertura
  5. Eventos recentes (CVM + SEC, últimos 7 dias)

Não toca na rede. Só leitura das DBs.

Uso:
    python scripts/weekly_report.py
    python scripts/weekly_report.py --no-open
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.coverage_audit import run as coverage_run  # noqa: E402

ROOT = _ROOT
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORTS = ROOT / "reports"


# ---------- helpers ----------

def fmt_pct(x, nd=2):
    return f"{x*100:.{nd}f}%" if isinstance(x, (int, float)) else "—"

def fmt_num(x, nd=2):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_money(x, sym="R$", nd=2):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{sym} {fmt_num(x, nd)}"

def _days_ago(n: int) -> str:
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


# ---------- data loading ----------

def _load_tickers(conn: sqlite3.Connection) -> list[dict]:
    """Carrega todos os tickers com company info, latest price, score, valuation."""
    rows = conn.execute(
        "SELECT ticker, name, sector, is_holding, currency FROM companies ORDER BY ticker"
    ).fetchall()
    result = []
    for ticker, name, sector, is_holding, currency in rows:
        # Latest price
        price_row = conn.execute(
            "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()

        # Latest score
        score_row = conn.execute(
            "SELECT score, passes_screen, details_json, run_date FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()

        # Latest valuation
        val_row = conn.execute(
            "SELECT fair_value, entry_price, details_json FROM valuations WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()

        # Latest fundamentals
        fund_row = conn.execute(
            "SELECT dy, roe, pe, dividend_streak_years FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()

        # FII fundamentals fallback
        fii_row = None
        if fund_row is None:
            fii_row = conn.execute(
                "SELECT dy_12m, pvp, distribution_streak_months FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()

        # Recent events (7 days)
        recent_events = conn.execute(
            "SELECT COUNT(*) FROM events WHERE ticker=? AND event_date >= ?",
            (ticker, _days_ago(7)),
        ).fetchone()[0]

        verdict = None
        upside = None
        if val_row and val_row[2]:
            det = json.loads(val_row[2])
            verdict = det.get("outputs", {}).get("verdict")
            upside = det.get("outputs", {}).get("upside")

        entry = {
            "ticker": ticker,
            "name": name,
            "sector": sector or "—",
            "is_holding": bool(is_holding),
            "currency": currency,
            "price": price_row[0] if price_row else None,
            "price_date": price_row[1] if price_row else None,
            "score": score_row[0] if score_row else None,
            "passes_screen": bool(score_row[1]) if score_row else None,
            "score_date": score_row[3] if score_row else None,
            "fair_value": val_row[0] if val_row else None,
            "entry_price": val_row[1] if val_row else None,
            "verdict": verdict,
            "upside": upside,
            "dy": (fund_row[0] if fund_row else (fii_row[0] if fii_row else None)),
            "roe": fund_row[1] if fund_row else None,
            "pe": fund_row[2] if fund_row else None,
            "streak": (fund_row[3] if fund_row else
                       (fii_row[2] if fii_row else None)),
            "pvp": fii_row[1] if fii_row else None,
            "is_fii": ticker.endswith("11"),
            "recent_events": recent_events,
        }
        result.append(entry)
    return result


def _load_recent_events(conn: sqlite3.Connection, days: int = 7) -> list[dict]:
    cutoff = _days_ago(days)
    rows = conn.execute(
        """SELECT ticker, event_date, source, kind, summary
           FROM events WHERE event_date >= ? ORDER BY event_date DESC""",
        (cutoff,),
    ).fetchall()
    return [{"ticker": r[0], "date": r[1], "source": r[2],
             "kind": r[3], "summary": r[4]} for r in rows]


def load_all() -> dict:
    br_tickers = []
    br_events = []
    us_tickers = []
    us_events = []

    if DB_BR.exists():
        with sqlite3.connect(DB_BR) as conn:
            br_tickers = _load_tickers(conn)
            br_events = _load_recent_events(conn)

    if DB_US.exists():
        with sqlite3.connect(DB_US) as conn:
            us_tickers = _load_tickers(conn)
            us_events = _load_recent_events(conn)

    # Coverage audit
    br_coverage = coverage_run("br") if DB_BR.exists() else []
    us_coverage = coverage_run("us") if DB_US.exists() else []

    return {
        "br_tickers": br_tickers,
        "us_tickers": us_tickers,
        "br_events": br_events,
        "us_events": us_events,
        "br_coverage": br_coverage,
        "us_coverage": us_coverage,
    }


# ---------- HTML builder ----------

CSS = """
:root {
  --bg: #0f172a; --fg: #e2e8f0; --muted: #94a3b8;
  --card: #1e293b; --border: #334155;
  --accent: #3b82f6; --pass: #10b981; --fail: #ef4444; --na: #6b7280;
  --warn: #f59e0b; --buy: #10b981; --hold: #f59e0b; --sell: #ef4444;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8fafc; --fg: #0f172a; --muted: #64748b;
    --card: #ffffff; --border: #e2e8f0;
  }
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
  background: var(--bg); color: var(--fg);
  max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; line-height: 1.5;
}
h1 { font-size: 1.8rem; margin: 0 0 .25rem; }
h2 { font-size: 1.15rem; margin: 2rem 0 .75rem;
     padding-bottom: .3rem; border-bottom: 1px solid var(--border); }
h3 { font-size: 1rem; margin: 1.5rem 0 .5rem; color: var(--muted); }
.subtitle { color: var(--muted); margin-bottom: 2rem; font-size: .9rem; }
.card { background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; padding: 1rem 1.25rem; margin: .75rem 0; overflow-x: auto; }
.stats { display: flex; gap: 1.5rem; flex-wrap: wrap; margin: 1rem 0; }
.stat { text-align: center; }
.stat .val { font-size: 1.6rem; font-weight: 700; }
.stat .lbl { font-size: .75rem; color: var(--muted); text-transform: uppercase; }
table { width: 100%; border-collapse: collapse; font-size: .85rem; }
th, td { text-align: left; padding: .45rem .6rem; border-bottom: 1px solid var(--border); }
th { color: var(--muted); font-weight: 600; text-transform: uppercase;
  font-size: .7rem; letter-spacing: .04em; position: sticky; top: 0; background: var(--card); }
.badge { display: inline-block; padding: .1rem .45rem; border-radius: 4px;
  font-size: .75rem; font-weight: 600; }
.b-pass { background: #10b98122; color: var(--pass); }
.b-fail { background: #ef444422; color: var(--fail); }
.b-na { background: #6b728022; color: var(--na); }
.b-buy { background: #10b98122; color: var(--buy); }
.b-hold { background: #f59e0b22; color: var(--hold); }
.b-sell { background: #ef444422; color: var(--sell); }
.b-gap { background: #ef444422; color: var(--fail); }
.b-ok { background: #10b98122; color: var(--pass); }
.b-warn { background: #f59e0b22; color: var(--warn); }
.event { padding: .4rem 0; border-bottom: 1px dashed var(--border); font-size: .85rem; }
.event:last-child { border-bottom: none; }
.event .src { color: var(--muted); font-size: .75rem; }
.num-r { text-align: right; }
.muted { color: var(--muted); }
footer { color: var(--muted); font-size: .75rem; margin-top: 2rem;
  padding-top: .75rem; border-top: 1px solid var(--border); text-align: center; }
"""


def _ticker_row_html(t: dict) -> str:
    sym = "R$" if t["currency"] == "BRL" else "$"
    # Screen badge
    if t["passes_screen"] is True:
        screen = '<span class="badge b-pass">PASSA</span>'
    elif t["passes_screen"] is False:
        screen = '<span class="badge b-fail">FALHA</span>'
    else:
        screen = '<span class="badge b-na">—</span>'
    # Verdict badge
    if t["verdict"] == "BUY":
        verd = '<span class="badge b-buy">BUY</span>'
    elif t["verdict"] == "HOLD":
        verd = '<span class="badge b-hold">HOLD</span>'
    elif t["verdict"] == "OVERVALUED":
        verd = '<span class="badge b-sell">OVER</span>'
    else:
        verd = '<span class="muted">—</span>'

    score_str = f"{t['score']:.2f}" if t["score"] is not None else "—"
    price_str = fmt_money(t["price"], sym) if t["price"] else "—"
    fv_str = fmt_money(t["fair_value"], sym) if t["fair_value"] else "—"
    dy_str = fmt_pct(t["dy"]) if t["dy"] else "—"
    upside_str = fmt_pct(t["upside"]) if t["upside"] else "—"
    events_str = str(t["recent_events"]) if t["recent_events"] else ""

    return (
        f"<tr>"
        f"<td><strong>{t['ticker']}</strong></td>"
        f"<td>{t['name']}</td>"
        f"<td>{t['sector']}</td>"
        f"<td class='num-r'>{price_str}</td>"
        f"<td class='num-r'>{dy_str}</td>"
        f"<td class='num-r'>{score_str}</td>"
        f"<td>{screen}</td>"
        f"<td class='num-r'>{fv_str}</td>"
        f"<td class='num-r'>{upside_str}</td>"
        f"<td>{verd}</td>"
        f"<td class='num-r'>{events_str}</td>"
        f"</tr>"
    )


def _fii_row_html(t: dict) -> str:
    sym = "R$"
    if t["passes_screen"] is True:
        screen = '<span class="badge b-pass">PASSA</span>'
    elif t["passes_screen"] is False:
        screen = '<span class="badge b-fail">FALHA</span>'
    else:
        screen = '<span class="badge b-na">—</span>'

    score_str = f"{t['score']:.2f}" if t["score"] is not None else "—"
    price_str = fmt_money(t["price"], sym) if t["price"] else "—"
    dy_str = fmt_pct(t["dy"]) if t["dy"] else "—"
    pvp_str = fmt_num(t["pvp"]) if t["pvp"] else "—"
    streak_str = str(t["streak"]) if t["streak"] else "—"

    return (
        f"<tr>"
        f"<td><strong>{t['ticker']}</strong></td>"
        f"<td>{t['name']}</td>"
        f"<td>{t['sector']}</td>"
        f"<td class='num-r'>{price_str}</td>"
        f"<td class='num-r'>{dy_str}</td>"
        f"<td class='num-r'>{pvp_str}</td>"
        f"<td class='num-r'>{streak_str} m</td>"
        f"<td class='num-r'>{score_str}</td>"
        f"<td>{screen}</td>"
        f"</tr>"
    )


def _coverage_summary_html(coverage: list[dict]) -> str:
    if not coverage:
        return '<p class="muted">Sem dados.</p>'
    gaps = [c for c in coverage if c["missing"]]
    if not gaps:
        return '<p><span class="badge b-ok">100% cobertura</span> — todos os campos críticos preenchidos.</p>'
    rows = []
    for c in gaps:
        miss = ", ".join(c["missing"])
        rows.append(
            f'<tr><td><strong>{c["ticker"]}</strong></td>'
            f'<td>{c["type"]}</td>'
            f'<td><span class="badge b-gap">{len(c["missing"])} gaps</span></td>'
            f'<td class="muted">{miss}</td></tr>'
        )
    return (
        '<table><thead><tr><th>Ticker</th><th>Tipo</th><th>Gaps</th><th>Campos em falta</th></tr></thead><tbody>'
        + "\n".join(rows) + "</tbody></table>"
    )


def build_html(data: dict) -> str:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    br = data["br_tickers"]
    us = data["us_tickers"]
    br_holdings = [t for t in br if t["is_holding"] and not t["is_fii"]]
    br_watch = [t for t in br if not t["is_holding"] and not t["is_fii"]]
    br_fiis_hold = [t for t in br if t["is_holding"] and t["is_fii"]]
    br_fiis_watch = [t for t in br if not t["is_holding"] and t["is_fii"]]
    us_holdings = [t for t in us if t["is_holding"]]
    us_watch = [t for t in us if not t["is_holding"]]

    # Aggregate stats
    n_pass = sum(1 for t in br + us if t["passes_screen"])
    n_buy = sum(1 for t in br + us if t["verdict"] == "BUY")
    n_events = sum(t["recent_events"] for t in br + us)
    n_gaps = sum(1 for c in data["br_coverage"] + data["us_coverage"] if c["missing"])

    parts: list[str] = []
    parts.append(f"<h1>Weekly Report — {date_str}</h1>")
    parts.append(f'<div class="subtitle">Investment Intelligence · '
                 f'{len(br)} tickers BR + {len(us)} tickers US · '
                 f'Gerado {now.strftime("%H:%M")}</div>')

    # Summary stats
    parts.append('<div class="stats">')
    parts.append(f'<div class="stat"><div class="val">{len(br_holdings)}</div><div class="lbl">Holdings BR</div></div>')
    parts.append(f'<div class="stat"><div class="val">{len(br_fiis_hold)}</div><div class="lbl">FIIs</div></div>')
    parts.append(f'<div class="stat"><div class="val">{len(us_holdings)}</div><div class="lbl">Holdings US</div></div>')
    parts.append(f'<div class="stat"><div class="val" style="color:var(--pass)">{n_pass}</div><div class="lbl">Passam screen</div></div>')
    parts.append(f'<div class="stat"><div class="val" style="color:var(--buy)">{n_buy}</div><div class="lbl">BUY (DDM)</div></div>')
    parts.append(f'<div class="stat"><div class="val">{n_events}</div><div class="lbl">Eventos 7d</div></div>')
    if n_gaps:
        parts.append(f'<div class="stat"><div class="val" style="color:var(--fail)">{n_gaps}</div><div class="lbl">Gaps dados</div></div>')
    parts.append("</div>")

    # --- BR Holdings (stocks) ---
    _stock_table_header = ('<table><thead><tr><th>Ticker</th><th>Empresa</th><th>Sector</th>'
                           '<th>Preço</th><th>DY</th><th>Score</th><th>Screen</th>'
                           '<th>Fair Value</th><th>Upside</th><th>Verdict</th><th>Ev 7d</th></tr></thead><tbody>')

    if br_holdings:
        parts.append("<h2>Carteira BR — Acções</h2>")
        parts.append(f'<div class="card">{_stock_table_header}')
        for t in sorted(br_holdings, key=lambda x: x["ticker"]):
            parts.append(_ticker_row_html(t))
        parts.append("</tbody></table></div>")

    # --- BR Holdings (FIIs) ---
    _fii_table_header = ('<table><thead><tr><th>Ticker</th><th>FII</th><th>Segmento</th>'
                         '<th>Preço</th><th>DY 12m</th><th>P/VP</th><th>Streak</th>'
                         '<th>Score</th><th>Screen</th></tr></thead><tbody>')

    if br_fiis_hold:
        parts.append("<h2>Carteira BR — FIIs</h2>")
        parts.append(f'<div class="card">{_fii_table_header}')
        for t in sorted(br_fiis_hold, key=lambda x: x["ticker"]):
            parts.append(_fii_row_html(t))
        parts.append("</tbody></table></div>")

    # --- US Holdings ---
    if us_holdings:
        parts.append("<h2>Carteira US — Acções</h2>")
        parts.append(f'<div class="card">{_stock_table_header}')
        for t in sorted(us_holdings, key=lambda x: x["ticker"]):
            parts.append(_ticker_row_html(t))
        parts.append("</tbody></table></div>")

    # --- BR Watchlist (stocks) ---
    if br_watch:
        parts.append("<h2>Watchlist BR — Acções</h2>")
        parts.append(f'<div class="card">{_stock_table_header}')
        for t in sorted(br_watch, key=lambda x: -(x["score"] or 0)):
            parts.append(_ticker_row_html(t))
        parts.append("</tbody></table></div>")

    # --- BR Watchlist (FIIs) ---
    if br_fiis_watch:
        parts.append("<h2>Watchlist BR — FIIs</h2>")
        parts.append(f'<div class="card">{_fii_table_header}')
        for t in sorted(br_fiis_watch, key=lambda x: -(x["score"] or 0)):
            parts.append(_fii_row_html(t))
        parts.append("</tbody></table></div>")

    # --- US Watchlist ---
    if us_watch:
        parts.append("<h2>Watchlist US — Acções</h2>")
        parts.append(f'<div class="card">{_stock_table_header}')
        for t in sorted(us_watch, key=lambda x: -(x["score"] or 0)):
            parts.append(_ticker_row_html(t))
        parts.append("</tbody></table></div>")

    # --- Top Opportunities ---
    buys = [t for t in br + us if t["verdict"] == "BUY" and t["upside"] is not None]
    buys.sort(key=lambda x: -(x["upside"] or 0))
    if buys:
        parts.append("<h2>Top Oportunidades (BUY + maior upside)</h2>")
        parts.append(f'<div class="card">{_stock_table_header}')
        for t in buys[:10]:
            parts.append(_ticker_row_html(t))
        parts.append("</tbody></table></div>")

    # --- Recent Events ---
    all_events = data["br_events"] + data["us_events"]
    all_events.sort(key=lambda x: x["date"], reverse=True)
    if all_events:
        parts.append(f"<h2>Eventos recentes (últimos 7 dias) — {len(all_events)} eventos</h2>")
        parts.append('<div class="card">')
        for ev in all_events[:30]:
            summary = (ev["summary"] or "—").replace("|", "·")
            parts.append(
                f'<div class="event">'
                f'<strong>{ev["ticker"]}</strong> '
                f'<span class="src">[{ev["source"]}]</span> '
                f'{ev["date"]} — {ev["kind"]} — {summary}'
                f'</div>'
            )
        if len(all_events) > 30:
            parts.append(f'<p class="muted">... e mais {len(all_events) - 30} eventos.</p>')
        parts.append("</div>")

    # --- Coverage Gaps ---
    br_gaps = [c for c in data["br_coverage"] if c["missing"]]
    us_gaps = [c for c in data["us_coverage"] if c["missing"]]
    if br_gaps or us_gaps:
        parts.append("<h2>Gaps de Cobertura</h2>")
        if br_gaps:
            parts.append("<h3>BR</h3>")
            parts.append(f'<div class="card">{_coverage_summary_html(data["br_coverage"])}</div>')
        if us_gaps:
            parts.append("<h3>US</h3>")
            parts.append(f'<div class="card">{_coverage_summary_html(data["us_coverage"])}</div>')

    parts.append(
        '<footer>Personal Investment Intelligence · '
        'Fontes: yfinance, brapi.dev, Status Invest, CVM, SEC EDGAR, BCB · '
        'Scoring: Graham (BR) / Buffett (US) · Valuation: Gordon DDM · '
        'Este relatório é informativo e pessoal, não constitui recomendação de investimento.</footer>'
    )

    return (
        '<!doctype html><html lang="pt-br"><head><meta charset="utf-8">'
        f'<title>Weekly Report {date_str}</title>'
        f'<style>{CSS}</style></head><body>'
        + "\n".join(parts)
        + "</body></html>"
    )


# ---------- main ----------

def main() -> None:
    ap = argparse.ArgumentParser(description="Weekly consolidated report BR+US")
    ap.add_argument("--no-open", action="store_true",
                    help="Não abrir o browser automaticamente")
    args = ap.parse_args()

    REPORTS.mkdir(exist_ok=True)
    data = load_all()
    html = build_html(data)

    date_str = datetime.now().strftime("%Y-%m-%d")
    path = REPORTS / f"weekly_{date_str}.html"
    path.write_text(html, encoding="utf-8")
    print(f"[ok] {path}")

    if not args.no_open:
        try:
            webbrowser.open(str(path.resolve()))
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    main()
