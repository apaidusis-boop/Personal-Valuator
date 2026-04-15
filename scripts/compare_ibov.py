"""Comparativo de performance acumulada vs Ibovespa.

Usa yfinance (histórico longo, gratuito) e gera um HTML standalone
em reports/compare_<ticker>_vs_ibov_<period>.html, abrindo-o no browser.

Ambas as séries são normalizadas a base 100 no primeiro ponto,
incluindo dividendos (auto_adjust=True). Também considera o Total
Return para o ticker individual, o que é mais justo com uma acção
pagadora de dividendos como ITSA4.

Uso:
    python scripts/compare_ibov.py                    # ITSA4, 10y, mensal
    python scripts/compare_ibov.py PRIO3 --period 5y
    python scripts/compare_ibov.py ITSA4 --period max --interval 1wk
"""
from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

import plotly.graph_objects as go
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

IBOV_TICKER = "^BVSP"


def _yf_ticker(ticker: str, market: str) -> str:
    if market == "br" and not ticker.endswith(".SA") and not ticker.startswith("^"):
        return f"{ticker}.SA"
    return ticker


def fetch_series(tickers: list[str], period: str, interval: str):
    return yf.download(
        tickers, period=period, interval=interval,
        auto_adjust=True, progress=False, group_by="ticker",
    )


def extract_close(df, ticker: str):
    """Aceita o DataFrame multi-ticker do yfinance e devolve (dates, closes)."""
    if (ticker, "Close") in df.columns:
        s = df[(ticker, "Close")].dropna()
    elif ticker in df.columns.get_level_values(0):
        s = df[ticker]["Close"].dropna()
    else:
        s = df["Close"].dropna() if "Close" in df.columns else df[ticker].dropna()
    return list(s.index.strftime("%Y-%m-%d")), [float(x) for x in s.values]


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    base = values[0]
    return [v / base * 100 for v in values]


def build_html(ticker: str, period: str, interval: str) -> Path:
    yticker = _yf_ticker(ticker, "br")
    df = fetch_series([yticker, IBOV_TICKER], period=period, interval=interval)

    t_dates, t_close = extract_close(df, yticker)
    i_dates, i_close = extract_close(df, IBOV_TICKER)
    t_norm = normalize(t_close)
    i_norm = normalize(i_close)

    # métricas resumo
    def total_ret(v):
        return (v[-1] / v[0] - 1) if len(v) >= 2 else 0.0

    def ann_ret(v, n_bars, per_year):
        if len(v) < 2: return 0.0
        years = max(1e-9, n_bars / per_year)
        return (v[-1] / v[0]) ** (1 / years) - 1

    per_year = {"1d": 252, "1wk": 52, "1mo": 12}.get(interval, 12)
    t_tot = total_ret(t_close); i_tot = total_ret(i_close)
    t_ann = ann_ret(t_close, len(t_close), per_year)
    i_ann = ann_ret(i_close, len(i_close), per_year)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_dates, y=t_norm, name=ticker,
        line=dict(color="#10b981", width=2.5),
        hovertemplate="%{x}<br>" + ticker + ": %{y:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=i_dates, y=i_norm, name="Ibovespa",
        line=dict(color="#64748b", width=2, dash="dot"),
        hovertemplate="%{x}<br>IBOV: %{y:.1f}<extra></extra>",
    ))
    fig.add_hline(y=100, line=dict(color="#94a3b8", width=1),
                  annotation_text="base 100", annotation_position="right")
    fig.update_layout(
        title=f"{ticker} vs Ibovespa — retorno acumulado ({period}, {interval}, total return)",
        xaxis_title="Data",
        yaxis_title="Índice (base 100)",
        template="plotly_white",
        height=560,
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(l=50, r=30, t=70, b=40),
    )

    summary = f"""
    <div class="summary">
      <div class="cell"><div class="k">{ticker}</div>
        <div class="v">{t_tot*100:+.1f}%</div>
        <div class="s">total · {t_ann*100:+.1f}% a.a.</div></div>
      <div class="cell"><div class="k">Ibovespa</div>
        <div class="v">{i_tot*100:+.1f}%</div>
        <div class="s">total · {i_ann*100:+.1f}% a.a.</div></div>
      <div class="cell"><div class="k">Alpha</div>
        <div class="v">{(t_tot - i_tot)*100:+.1f} pp</div>
        <div class="s">vs IBOV · {(t_ann - i_ann)*100:+.1f} pp a.a.</div></div>
    </div>
    """

    css = """
    :root { color-scheme: light dark;
      --bg:#f8fafc; --fg:#0f172a; --muted:#64748b;
      --card:#ffffff; --border:#e2e8f0; }
    @media (prefers-color-scheme: dark) {
      :root { --bg:#0f172a; --fg:#e2e8f0; --muted:#94a3b8;
              --card:#1e293b; --border:#334155; }
    }
    * { box-sizing: border-box; }
    body { font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
      background: var(--bg); color: var(--fg);
      max-width: 1080px; margin: 0 auto; padding: 2rem 1.5rem; line-height: 1.5; }
    h1 { font-size: 1.6rem; margin: 0 0 .25rem; }
    .subtitle { color: var(--muted); margin-bottom: 1.5rem; }
    .card { background: var(--card); border: 1px solid var(--border);
      border-radius: 10px; padding: 1rem 1.25rem; margin: 1rem 0; }
    .summary { display: grid; gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin: 1rem 0; }
    .cell { background: var(--card); border: 1px solid var(--border);
      border-radius: 10px; padding: .9rem 1.1rem; }
    .cell .k { color: var(--muted); font-size: .75rem; text-transform: uppercase;
      letter-spacing: .05em; }
    .cell .v { font-size: 1.6rem; font-weight: 700; margin: .1rem 0; }
    .cell .s { color: var(--muted); font-size: .82rem; }
    footer { color: var(--muted); font-size: .8rem; text-align: center;
      margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }
    """

    body = f"""
    <h1>{ticker} vs Ibovespa</h1>
    <div class="subtitle">Período: <strong>{period}</strong> · Intervalo: <strong>{interval}</strong>
      · Total return (dividendos reinvestidos) · Fonte: Yahoo Finance</div>
    {summary}
    <div class="card">{fig.to_html(include_plotlyjs='cdn', full_html=False)}</div>
    <footer>Base 100 no primeiro ponto da série. Ambas as séries ajustadas para dividendos e splits.</footer>
    """

    html = f'<!doctype html><html lang="pt-br"><head><meta charset="utf-8">' \
           f'<title>{ticker} vs IBOV</title><style>{css}</style></head><body>{body}</body></html>'

    REPORTS.mkdir(exist_ok=True)
    out = REPORTS / f"compare_{ticker.lower()}_vs_ibov_{period}.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--period", default="10y",
                    help="1y, 2y, 5y, 10y, max (default 10y)")
    ap.add_argument("--interval", default="1mo",
                    help="1d, 1wk, 1mo (default 1mo)")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    out = build_html(args.ticker, args.period, args.interval)
    print(f"[ok] {out}")
    if not args.no_open:
        webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
