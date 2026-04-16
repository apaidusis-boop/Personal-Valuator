"""Gera gráficos interactivos de macro (SELIC, CDI, IPCA, PTAX, spread real).

Output:
  reports/macro_YYYY-MM-DD.html  — Plotly interactivo com tema Fallout

Charts:
  1. SELIC anual histórica (bar) + destaques mín/máx
  2. IPCA anual em quintis (stacked bar colorido por quintil)
  3. SELIC real (SELIC − IPCA) vs tempo (line)
  4. PTAX USDBRL histórico (line log scale)

Uso:
    python scripts/macro_chart.py
    python scripts/macro_chart.py --since 1995
"""
from __future__ import annotations

import argparse
import sqlite3
from collections import defaultdict
from datetime import date
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "br_investments.db"
REPORTS = ROOT / "reports"

# Fallout terminal palette
BG = "#000000"
FG = "#20ff20"
ACCENT = "#39ff14"
DIM = "#155515"
RED = "#ff4040"
AMBER = "#ffb000"


def load_selic_annual(conn: sqlite3.Connection, since: int) -> list[tuple[int, float]]:
    """Anualiza SELIC_DAILY composta por ano."""
    rows = conn.execute(
        "SELECT date, value FROM series WHERE series_id='SELIC_DAILY' ORDER BY date"
    ).fetchall()
    yearly: dict[int, list[float]] = defaultdict(list)
    for d, v in rows:
        y = int(d[:4])
        if y >= since:
            yearly[y].append(v)
    out = []
    for y in sorted(yearly):
        daily_avg = sum(yearly[y]) / len(yearly[y])
        out.append((y, (1 + daily_avg) ** 252 - 1))
    return out


def load_ipca_annual(conn: sqlite3.Connection, since: int) -> list[tuple[int, float]]:
    """Compõe IPCA mensal em anual."""
    rows = conn.execute(
        "SELECT date, value FROM series WHERE series_id='IPCA_MONTHLY' ORDER BY date"
    ).fetchall()
    buckets: dict[int, list[float]] = defaultdict(list)
    for d, v in rows:
        y = int(d[:4])
        if y >= since:
            buckets[y].append(v)
    out = []
    for y in sorted(buckets):
        if len(buckets[y]) < 12:
            continue
        factor = 1.0
        for m in buckets[y]:
            factor *= (1 + m)
        out.append((y, factor - 1))
    return out


def quintile_colors(values: list[float]) -> list[str]:
    """Assign colour por quintil. Verde claro = baixa, vermelho = alta."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    palette = ["#60ff60", "#90ff40", "#ffd000", "#ff8800", "#ff2020"]
    thresholds = [sorted_vals[(i + 1) * n // 5 - 1] for i in range(5)]
    out = []
    for v in values:
        for i, th in enumerate(thresholds):
            if v <= th:
                out.append(palette[i])
                break
        else:
            out.append(palette[-1])
    return out


def load_ptax_monthly(conn: sqlite3.Connection, since: int) -> list[tuple[str, float]]:
    rows = conn.execute(
        "SELECT date, value FROM series WHERE series_id='USDBRL_PTAX' ORDER BY date"
    ).fetchall()
    # último valor de cada mês
    monthly: dict[str, tuple[str, float]] = {}
    for d, v in rows:
        if int(d[:4]) < since:
            continue
        ym = d[:7]
        monthly[ym] = (d, v)
    return [(ym, v) for ym, (_, v) in sorted(monthly.items())]


def build_figure(selic, ipca, ptax) -> go.Figure:
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=(
            ">SELIC ANUALIZADA (% a.a.)",
            ">IPCA ANUAL COM QUINTIS",
            ">SELIC REAL (SELIC - IPCA)",
            ">PTAX USD/BRL (log)",
        ),
        vertical_spacing=0.08,
        row_heights=[0.25, 0.25, 0.25, 0.25],
    )

    # 1. SELIC bar
    years = [y for y, _ in selic]
    vals = [v * 100 for _, v in selic]
    max_y, max_v = max(selic, key=lambda x: x[1])
    min_y, min_v = min(selic, key=lambda x: x[1])
    colors = [RED if v == max_v else AMBER if v == min_v else FG for _, v in selic]
    fig.add_trace(
        go.Bar(x=years, y=vals, marker_color=colors,
               text=[f"{v:.1f}%" for v in vals],
               textposition="outside", textfont=dict(color=FG, size=9),
               hovertemplate="%{x}<br>SELIC %{y:.2f}%<extra></extra>",
               showlegend=False),
        row=1, col=1,
    )

    # 2. IPCA com quintis
    iyears = [y for y, _ in ipca]
    ivals = [v * 100 for _, v in ipca]
    qcolors = quintile_colors([v for _, v in ipca])
    fig.add_trace(
        go.Bar(x=iyears, y=ivals, marker_color=qcolors,
               text=[f"{v:.1f}%" for v in ivals],
               textposition="outside", textfont=dict(color=FG, size=9),
               hovertemplate="%{x}<br>IPCA %{y:.2f}%<extra></extra>",
               showlegend=False),
        row=2, col=1,
    )

    # 3. SELIC real (diferença)
    ipca_map = dict(ipca)
    real_years = []
    real_vals = []
    for y, s in selic:
        if y in ipca_map:
            real_years.append(y)
            real_vals.append((s - ipca_map[y]) * 100)
    fig.add_trace(
        go.Scatter(x=real_years, y=real_vals, mode="lines+markers",
                   line=dict(color=ACCENT, width=2),
                   marker=dict(size=6, color=ACCENT),
                   hovertemplate="%{x}<br>Real %{y:.2f}%<extra></extra>",
                   showlegend=False),
        row=3, col=1,
    )
    fig.add_hline(y=0, line_dash="dash", line_color=DIM, row=3, col=1)

    # 4. PTAX line
    pdates = [ym + "-01" for ym, _ in ptax]
    pvals = [v for _, v in ptax]
    fig.add_trace(
        go.Scatter(x=pdates, y=pvals, mode="lines",
                   line=dict(color=FG, width=1.5),
                   hovertemplate="%{x}<br>USD/BRL %{y:.2f}<extra></extra>",
                   showlegend=False),
        row=4, col=1,
    )
    fig.update_yaxes(type="log", row=4, col=1)

    # Theme
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color=FG, family="Consolas, Courier New, monospace", size=11),
        height=1100,
        margin=dict(l=60, r=30, t=80, b=40),
        title=dict(
            text=">MACRO DASHBOARD BR // ROBCO TERMLINK",
            font=dict(color=ACCENT, size=16),
            x=0.01,
        ),
    )
    fig.update_xaxes(gridcolor=DIM, zerolinecolor=DIM, color=FG)
    fig.update_yaxes(gridcolor=DIM, zerolinecolor=DIM, color=FG)
    for ann in fig["layout"]["annotations"]:
        ann["font"] = dict(color=ACCENT, size=12, family="Consolas")
        ann["x"] = 0.01
        ann["xanchor"] = "left"
    return fig


def wrap_html(fig_html: str, today: str, since: int) -> str:
    return f"""<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<title>Macro Dashboard BR — {today}</title>
<style>
  body {{
    background: #000;
    color: #20ff20;
    font-family: Consolas, "Courier New", monospace;
    margin: 0;
    padding: 20px;
    text-shadow: 0 0 2px #20ff20;
  }}
  header {{
    border-bottom: 1px solid #155;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }}
  h1 {{
    color: #39ff14;
    font-size: 18px;
    margin: 0 0 4px 0;
    text-shadow: 0 0 5px #39ff14;
  }}
  .meta {{
    font-size: 11px;
    color: #60aa60;
  }}
  .chart {{
    margin: 16px 0;
  }}
  footer {{
    margin-top: 20px;
    font-size: 11px;
    color: #60aa60;
    border-top: 1px solid #155;
    padding-top: 8px;
  }}
</style>
</head>
<body>
<header>
  <h1>&gt; MACRO DASHBOARD BR // ROBCO TERMLINK</h1>
  <div class="meta">DATA ESTELAR: {today} &nbsp;|&nbsp; JANELA: {since}-{today[:4]} &nbsp;|&nbsp; FONTE: BCB SGS (11, 432, 433, 1)</div>
</header>
<div class="chart">{fig_html}</div>
<footer>
  &gt; END OF TRANSMISSION. &nbsp;|&nbsp; CHARTS INTERACTIVOS: hover para valores, double-click para zoom-reset.
</footer>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=int, default=1995,
                    help="ano inicial (default 1995 = pós-Plano Real)")
    args = ap.parse_args()

    with sqlite3.connect(DB) as conn:
        selic = load_selic_annual(conn, args.since)
        ipca = load_ipca_annual(conn, args.since)
        ptax = load_ptax_monthly(conn, args.since)

    fig = build_figure(selic, ipca, ptax)
    today = date.today().isoformat()
    out = REPORTS / f"macro_{today}.html"
    REPORTS.mkdir(parents=True, exist_ok=True)
    fig_html = fig.to_html(include_plotlyjs="cdn", full_html=False,
                           config={"displaylogo": False})
    out.write_text(wrap_html(fig_html, today, args.since), encoding="utf-8")
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()
