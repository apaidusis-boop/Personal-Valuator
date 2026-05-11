"""Relatório HTML do portfolio US — scoring Buffett + total return + concentração.

Lê:
  - config/universe.yaml (secção us.holdings)
  - data/us_investments.db (prices, dividends, fundamentals, scores)
  - C:/Users/paidu/Downloads/positions (1).csv (quantities + cost basis)

Produz:
  reports/us_portfolio_YYYY-MM-DD.html

Tabelas:
  1. Sumário agregado (total MV, cost, P&L, yield efectivo, coverage do screen)
  2. Posições ordenadas por score composto
  3. Screen Buffett por ticker (verdict de cada critério, coverage)
  4. Gainers/Losers desde aquisição

Gráficos Plotly:
  - Alocação por sector (pie)
  - Concentração por ticker (bar)
  - P&L absoluto por posição (bar, cor condicional)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "data" / "us_investments.db"
UNIVERSE = ROOT / "config" / "universe.yaml"


def load_holdings_from_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, thousands=",", encoding="utf-8-sig")
    df = df[df["Asset Class"].isin(["Equity", "Alternative Assets"])].copy()
    for col in ["Quantity", "Price", "Value", "Cost",
                "Unrealized G/L Amt.", "Unrealized Gain/Loss (%)",
                "Est. Annual Income"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # normalizar ticker BRKB → BRK-B (schema universe usa BRK-B, yfinance BRK-B)
    df["Ticker"] = df["Ticker"].replace({"BRKB": "BRK-B"})
    return df[["Ticker", "Description", "Quantity", "Price", "Value", "Cost",
               "Unrealized G/L Amt.", "Unrealized Gain/Loss (%)",
               "Est. Annual Income"]].rename(columns={
        "Ticker": "ticker", "Description": "description",
        "Quantity": "qty", "Price": "price", "Value": "mv", "Cost": "cost",
        "Unrealized G/L Amt.": "pnl", "Unrealized Gain/Loss (%)": "pnl_pct",
        "Est. Annual Income": "income_est",
    })


def load_sectors() -> dict[str, str]:
    d = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    us = d.get("us", {}) or {}
    out: dict[str, str] = {}
    for bucket in ("holdings", "watchlist"):
        for entries in (us.get(bucket) or {}).values():
            for e in (entries or []):
                out[e["ticker"]] = e.get("sector") or "Other"
    return out


def load_screen_results(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with sqlite3.connect(DB) as conn:
        for t in tickers:
            row = conn.execute(
                """SELECT score, passes_screen, details_json FROM scores
                   WHERE ticker=? ORDER BY run_date DESC LIMIT 1""",
                (t,),
            ).fetchone()
            if not row:
                continue
            out[t] = {
                "score": row[0],
                "passes_screen": bool(row[1]),
                "details": json.loads(row[2]) if row[2] else {},
            }
    return out


def load_fundamentals(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with sqlite3.connect(DB) as conn:
        for t in tickers:
            row = conn.execute(
                """SELECT pe, pb, dy, roe, dividend_streak_years, net_debt_ebitda
                   FROM fundamentals WHERE ticker=?
                   ORDER BY period_end DESC LIMIT 1""",
                (t,),
            ).fetchone()
            if row:
                out[t] = {
                    "pe": row[0], "pb": row[1], "dy": row[2],
                    "roe": row[3], "streak": row[4], "nde": row[5],
                }
    return out


def _verdict_emoji(v: str) -> str:
    return {"pass": "✅", "fail": "❌", "n/a": "⚪"}.get(v, "?")


def _fmt(v, pct=False, dash="—"):
    if v is None or (isinstance(v, float) and v != v):
        return dash
    if pct:
        return f"{v * 100:.2f}%" if abs(v) < 1 else f"{v:.2f}%"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def build_html(port: pd.DataFrame, sectors: dict, screens: dict, funds: dict) -> str:
    import plotly.graph_objects as go
    from plotly.offline import plot

    port = port.copy()
    port["sector"] = port["ticker"].map(sectors).fillna("Other")
    port["score"] = port["ticker"].map(lambda t: screens.get(t, {}).get("score"))
    port["passes"] = port["ticker"].map(lambda t: screens.get(t, {}).get("passes_screen", False))
    port = port.sort_values("mv", ascending=False)

    total_mv = port["mv"].sum()
    total_cost = port["cost"].sum()
    total_pnl = port["pnl"].sum()
    total_income = port["income_est"].sum()
    yield_eff = (total_income / total_mv * 100) if total_mv else 0.0
    n_scored = sum(1 for t in port["ticker"] if t in screens)
    n_pass = sum(1 for t in port["ticker"] if screens.get(t, {}).get("passes_screen"))

    # ---- Pie: alocação por sector ----
    sec_agg = port.groupby("sector")["mv"].sum().sort_values(ascending=False)
    pie = go.Figure(data=[go.Pie(
        labels=sec_agg.index.tolist(), values=sec_agg.values.tolist(),
        hole=0.4, textinfo="label+percent",
    )])
    pie.update_layout(title="Alocação por Sector", template="plotly_white", height=400)

    # ---- Bar: MV por ticker ----
    bar_mv = go.Figure(data=[go.Bar(
        x=port["ticker"], y=port["mv"],
        text=[f"${v:,.0f}" for v in port["mv"]], textposition="outside",
        marker_color="#2E86AB",
    )])
    bar_mv.update_layout(title="Market Value por Posição", template="plotly_white",
                         height=400, yaxis_title="USD")

    # ---- Bar: P&L por ticker ----
    colors = ["#28a745" if v >= 0 else "#dc3545" for v in port["pnl"]]
    bar_pnl = go.Figure(data=[go.Bar(
        x=port["ticker"], y=port["pnl"], marker_color=colors,
        text=[f"{v:+.0f}" for v in port["pnl"]], textposition="outside",
    )])
    bar_pnl.update_layout(title="P&L Não Realizado (USD)", template="plotly_white",
                          height=400, yaxis_title="USD")

    pie_div = plot(pie, output_type="div", include_plotlyjs=False)
    bar_mv_div = plot(bar_mv, output_type="div", include_plotlyjs=False)
    bar_pnl_div = plot(bar_pnl, output_type="div", include_plotlyjs=False)

    # ---- Tabela de posições ----
    pos_rows = []
    for _, r in port.iterrows():
        t = r["ticker"]
        sc = screens.get(t, {})
        score = sc.get("score")
        passes = sc.get("passes_screen")
        fnd = funds.get(t, {})
        badge = (
            '<span class="pass">PASS</span>' if passes is True else
            '<span class="fail">FAIL</span>' if passes is False else
            '<span class="na">n/a</span>'
        )
        score_s = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
        pnl_cls = "gain" if r["pnl"] >= 0 else "loss"
        pos_rows.append(f"""
        <tr>
          <td><b>{t}</b></td>
          <td>{r['sector']}</td>
          <td>{r['description'][:35]}</td>
          <td class="num">{r['qty']:.4f}</td>
          <td class="num">${r['mv']:,.2f}</td>
          <td class="num">${r['cost']:,.2f}</td>
          <td class="num {pnl_cls}">{r['pnl']:+,.2f}</td>
          <td class="num {pnl_cls}">{r['pnl_pct']:+.2f}%</td>
          <td class="num">{_fmt(fnd.get('pe'))}</td>
          <td class="num">{_fmt(fnd.get('pb'))}</td>
          <td class="num">{_fmt(fnd.get('dy'), pct=True)}</td>
          <td class="num">{_fmt(fnd.get('roe'), pct=True)}</td>
          <td class="num">{_fmt(fnd.get('streak'))}</td>
          <td class="num">{score_s}</td>
          <td>{badge}</td>
        </tr>""")

    pos_table = "\n".join(pos_rows)

    # ---- Tabela de screen detalhado ----
    screen_rows = []
    for t in port["ticker"]:
        if t not in screens:
            continue
        d = screens[t]["details"]
        cells = "".join(
            f"<td title='{c.get('reason','')}'>{_verdict_emoji(c['verdict'])}</td>"
            for name, c in d.items()
        )
        headers_once = [name for name in d.keys()]
        screen_rows.append((t, cells, headers_once, screens[t]["score"]))

    if screen_rows:
        header_cols = "".join(f"<th>{h.replace('_', ' ')}</th>" for h in screen_rows[0][2])
        screen_table = f"""
        <table class="screen">
          <thead>
            <tr><th>ticker</th>{header_cols}<th>score</th></tr>
          </thead>
          <tbody>
            {''.join(f"<tr><td><b>{t}</b></td>{cells}<td class='num'>{s:.2f}</td></tr>"
                     for t, cells, _, s in screen_rows)}
          </tbody>
        </table>"""
    else:
        screen_table = "<p>(sem screens)</p>"

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <title>US Portfolio Report — {datetime.now():%Y-%m-%d}</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    body {{ font-family: -apple-system, system-ui, Segoe UI, sans-serif;
           max-width: 1400px; margin: 2em auto; padding: 0 1em; color: #1d1d1f; }}
    h1, h2 {{ color: #0b2545; }}
    h1 {{ border-bottom: 3px solid #0b2545; padding-bottom: 0.3em; }}
    .kpis {{ display: flex; gap: 1em; flex-wrap: wrap; margin: 1em 0 2em; }}
    .kpi {{ flex: 1; min-width: 180px; background: #f5f7fa; padding: 1em;
           border-radius: 8px; border-left: 4px solid #0b2545; }}
    .kpi .label {{ font-size: 0.85em; color: #666; text-transform: uppercase;
                  letter-spacing: 0.5px; }}
    .kpi .value {{ font-size: 1.6em; font-weight: 600; margin-top: 0.3em; }}
    .kpi .sub {{ font-size: 0.85em; color: #888; margin-top: 0.2em; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1em 0;
             font-size: 0.88em; }}
    th {{ background: #0b2545; color: white; padding: 0.6em 0.5em;
         text-align: left; font-weight: 500; }}
    td {{ padding: 0.5em; border-bottom: 1px solid #eee; }}
    td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    tr:hover {{ background: #f9fafb; }}
    .gain {{ color: #28a745; font-weight: 600; }}
    .loss {{ color: #dc3545; font-weight: 600; }}
    .pass {{ background: #28a745; color: white; padding: 2px 8px;
            border-radius: 4px; font-size: 0.78em; font-weight: 600; }}
    .fail {{ background: #dc3545; color: white; padding: 2px 8px;
            border-radius: 4px; font-size: 0.78em; font-weight: 600; }}
    .na   {{ background: #adb5bd; color: white; padding: 2px 8px;
            border-radius: 4px; font-size: 0.78em; font-weight: 600; }}
    .screen td {{ text-align: center; font-size: 1.2em; padding: 0.4em; }}
    .note {{ background: #fff3cd; border-left: 4px solid #ffc107;
            padding: 0.8em 1em; margin: 1em 0; border-radius: 4px;
            font-size: 0.9em; }}
    .footer {{ color: #999; font-size: 0.8em; margin-top: 3em;
              text-align: center; padding: 1em 0; border-top: 1px solid #eee; }}
  </style>
</head>
<body>

<h1>US Portfolio Report</h1>
<p style="color:#666">Gerado em {datetime.now():%Y-%m-%d %H:%M}. Fonte de holdings: export J.P. Morgan Securities.
Scoring Buffett: <code>scoring/engine.py score_us()</code>. Fundamentals: yfinance <code>.info</code>.</p>

<div class="kpis">
  <div class="kpi">
    <div class="label">Market Value</div>
    <div class="value">${total_mv:,.0f}</div>
    <div class="sub">{len(port)} posições</div>
  </div>
  <div class="kpi">
    <div class="label">Cost Basis</div>
    <div class="value">${total_cost:,.0f}</div>
  </div>
  <div class="kpi">
    <div class="label">P&amp;L Não Realizado</div>
    <div class="value {'gain' if total_pnl >= 0 else 'loss'}">{total_pnl:+,.0f}</div>
    <div class="sub">{total_pnl / total_cost * 100:+.2f}%</div>
  </div>
  <div class="kpi">
    <div class="label">Yield Efectivo</div>
    <div class="value">{yield_eff:.2f}%</div>
    <div class="sub">${total_income:,.0f}/ano est.</div>
  </div>
  <div class="kpi">
    <div class="label">Screen Buffett</div>
    <div class="value">{n_pass} / {n_scored}</div>
    <div class="sub">passam de {n_scored} scoradas</div>
  </div>
</div>

<div class="note">
  <b>Como ler o screen Buffett.</b> Critérios: P/E ≤ 20, P/B ≤ 3, DY ≥ 2.5%,
  ROE ≥ 15%, Aristocrat <i>ou</i> ≥ 10 anos de streak. Cada critério tem
  verdict <b>pass / fail / n/a</b>. O score é a fração de pass sobre o total
  de critérios aplicáveis (excluindo n/a). Passa o screen = <b>todos</b> os
  critérios aplicáveis são pass.
</div>

{pie_div}

{bar_mv_div}

{bar_pnl_div}

<h2>Posições</h2>
<table>
  <thead>
    <tr>
      <th>ticker</th><th>sector</th><th>nome</th>
      <th>qty</th><th>mv</th><th>cost</th><th>pnl</th><th>pnl%</th>
      <th>P/E</th><th>P/B</th><th>DY</th><th>ROE</th><th>streak</th>
      <th>score</th><th>verdict</th>
    </tr>
  </thead>
  <tbody>
    {pos_table}
  </tbody>
</table>

<h2>Screen Buffett — detalhe por critério</h2>
{screen_table}

<div class="footer">
  Personal-Valuator · investment-intelligence · Claude Code generated
</div>

</body>
</html>"""
    return html


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="C:/Users/paidu/Downloads/positions (1).csv")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    port = load_holdings_from_csv(Path(args.csv))
    sectors = load_sectors()
    tickers = port["ticker"].dropna().unique().tolist()
    screens = load_screen_results(tickers)
    funds = load_fundamentals(tickers)

    html = build_html(port, sectors, screens, funds)

    out = Path(args.out) if args.out else (
        ROOT / "reports" / f"us_portfolio_{datetime.now():%Y-%m-%d}.html"
    )
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Relatório: {out.relative_to(ROOT)}")
    print(f"Posições: {len(port)}  |  Scoradas: {len(screens)}  |  Passam: "
          f"{sum(1 for t in tickers if screens.get(t, {}).get('passes_screen'))}")


if __name__ == "__main__":
    main()
