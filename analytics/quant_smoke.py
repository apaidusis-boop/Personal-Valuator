"""Phase W.11 Quant stack smoke test — vectorbt + pyfolio-reloaded + alphalens-reloaded.

Carrega histórico de prices das holdings activas (BR ou US), constrói carteira
weighted-by-quantity, e mostra:
  - Returns + drawdowns (vectorbt)
  - Sharpe, Sortino, Calmar, max DD, annual return (empyrical via pyfolio)
  - Per-ticker contribution to portfolio variance
  - Plot opcional para HTML (Helena dark theme) — saved em reports/

Uso:
    python -m analytics.quant_smoke --market us
    python -m analytics.quant_smoke --market br --start 2020-01-01
    python -m analytics.quant_smoke --market us --html
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parent.parent
DBS = {
    "br": ROOT / "data" / "br_investments.db",
    "us": ROOT / "data" / "us_investments.db",
}
REPORTS_DIR = ROOT / "reports"


def load_prices(market: str, start: str | None = None) -> tuple[pd.DataFrame, dict]:
    """Returns (price_df indexed by date, weights dict ticker→pct)."""
    db = DBS[market]
    with sqlite3.connect(db) as c:
        positions = c.execute(
            "SELECT ticker, quantity, entry_price "
            "FROM portfolio_positions WHERE active = 1"
        ).fetchall()
        if not positions:
            raise SystemExit(f"sem holdings activas no {market}")
        tickers = [p[0] for p in positions]

        # Pull prices, com filtro since
        sql = ("SELECT ticker, date, close FROM prices WHERE ticker IN ("
               + ",".join("?" * len(tickers)) + ")")
        params: list = list(tickers)
        if start:
            sql += " AND date >= ?"
            params.append(start)
        sql += " ORDER BY date"
        rows = c.execute(sql, params).fetchall()

    df = pd.DataFrame(rows, columns=["ticker", "date", "close"])
    df["date"] = pd.to_datetime(df["date"])
    pivot = df.pivot(index="date", columns="ticker", values="close").sort_index()

    # Weights por valor de mercado actual aproximado (qty * último preço)
    last_prices = pivot.ffill().iloc[-1]
    market_value = {t: q * last_prices.get(t, np.nan) for t, q, _ in positions}
    market_value = {t: v for t, v in market_value.items() if pd.notna(v)}
    total = sum(market_value.values())
    weights = {t: v / total for t, v in market_value.items()} if total > 0 else {}

    return pivot, weights


def compute_metrics(price_df: pd.DataFrame, weights: dict[str, float],
                    winsorize_clip: float = 0.5) -> dict:
    """Portfolio + per-ticker stats via empyrical/pandas.

    `winsorize_clip`: clip daily returns ao intervalo [-clip, +clip] para
    proteger métricas contra data-quality bugs (ex: XPML11 2026-01-14
    teve close=1.07 quando deveria ser ~110). Default 50% — qualquer
    daily return além disso é data corruption num ETF/FII normal.
    """
    import empyrical as ep

    # daily returns alinhados (only days where todos têm preço)
    rets = price_df.pct_change().dropna(how="all")

    if winsorize_clip and winsorize_clip > 0:
        outliers = (rets.abs() > winsorize_clip).sum().sum()
        rets = rets.clip(lower=-winsorize_clip, upper=winsorize_clip)
        if outliers > 0:
            print(f"  [winsorize] {outliers} daily-return outliers > {winsorize_clip:.0%} clipped")

    # portfolio return = somatório weighted dos retornos diários
    aligned_weights = pd.Series(weights).reindex(rets.columns).fillna(0)
    aligned_weights /= aligned_weights.sum() if aligned_weights.sum() > 0 else 1
    port_ret = (rets * aligned_weights).sum(axis=1)
    port_ret = port_ret.dropna()

    out: dict = {
        "panel_size": int(rets.shape[1]),
        "obs_days": int(port_ret.shape[0]),
        "first_date": str(port_ret.index.min().date()) if len(port_ret) else None,
        "last_date": str(port_ret.index.max().date()) if len(port_ret) else None,
        "portfolio": {
            "annual_return": float(ep.annual_return(port_ret)),
            "annual_vol": float(ep.annual_volatility(port_ret)),
            "sharpe_ratio": float(ep.sharpe_ratio(port_ret)),
            "sortino_ratio": float(ep.sortino_ratio(port_ret)),
            "calmar_ratio": float(ep.calmar_ratio(port_ret)),
            "max_drawdown": float(ep.max_drawdown(port_ret)),
            "cum_return": float(ep.cum_returns_final(port_ret)),
        },
        "weights": {t: round(w, 4) for t, w in
                    sorted(weights.items(), key=lambda x: -x[1])},
        "per_ticker": {},
    }

    # Per-ticker stats (top 5 por contribuição vol)
    for t in rets.columns:
        r = rets[t].dropna()
        if r.empty:
            continue
        out["per_ticker"][t] = {
            "weight": round(float(aligned_weights.get(t, 0)), 4),
            "annual_return": round(float(ep.annual_return(r)), 4),
            "annual_vol": round(float(ep.annual_volatility(r)), 4),
            "sharpe": round(float(ep.sharpe_ratio(r)), 3),
            "max_dd": round(float(ep.max_drawdown(r)), 4),
        }

    # Correlation matrix average (signal de diversificação)
    corr = rets.corr()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    out["avg_correlation"] = float(upper.stack().mean())

    return out, port_ret


def render_html(metrics: dict, port_ret: pd.Series, market: str) -> Path:
    """Pequeno relatório HTML com Helena dark — só inline, sem deps externos."""
    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / f"quant_smoke_{market}_{date.today().isoformat()}.html"
    p = metrics["portfolio"]

    cum = (1 + port_ret).cumprod()
    # SVG sparkline simples
    if len(cum) > 0:
        import io
        xs = np.linspace(0, 600, len(cum))
        ys_norm = (cum.values - cum.min()) / (cum.max() - cum.min() + 1e-9)
        ys = 200 - ys_norm * 180 - 10
        path_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
        spark = f'<svg width="600" height="200" style="background:#0f1117">' \
                f'<path d="{path_d}" stroke="#c4ff42" fill="none" stroke-width="2"/>' \
                f'</svg>'
    else:
        spark = ""

    rows_per_ticker = "".join(
        f"<tr><td>{t}</td><td>{m['weight']:.1%}</td><td>{m['annual_return']:+.1%}</td>"
        f"<td>{m['annual_vol']:.1%}</td><td>{m['sharpe']:+.2f}</td>"
        f"<td>{m['max_dd']:.1%}</td></tr>"
        for t, m in metrics["per_ticker"].items()
    )

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Quant Smoke — {market.upper()}</title>
<style>
  body {{ background:#0a0c10; color:#e8e8e8; font-family:'JetBrains Mono',monospace; padding:2rem; }}
  h1 {{ color:#c4ff42; }}
  table {{ border-collapse:collapse; margin-top:1rem; }}
  th,td {{ padding:0.4rem 1rem; border-bottom:1px solid #222; text-align:right; }}
  th:first-child, td:first-child {{ text-align:left; color:#c4ff42; }}
  .kpi {{ display:inline-block; margin-right:2rem; }}
  .kpi .label {{ color:#888; font-size:0.85rem; }}
  .kpi .value {{ font-size:1.4rem; font-weight:bold; }}
</style></head><body>
<h1>Phase W.11 — Quant Smoke ({market.upper()})</h1>
<p>{metrics['obs_days']} obs days | {metrics['first_date']} → {metrics['last_date']} | panel={metrics['panel_size']}</p>
<div>
  <span class="kpi"><span class="label">CAGR</span><br><span class="value">{p['annual_return']:+.1%}</span></span>
  <span class="kpi"><span class="label">Vol anual</span><br><span class="value">{p['annual_vol']:.1%}</span></span>
  <span class="kpi"><span class="label">Sharpe</span><br><span class="value">{p['sharpe_ratio']:+.2f}</span></span>
  <span class="kpi"><span class="label">Sortino</span><br><span class="value">{p['sortino_ratio']:+.2f}</span></span>
  <span class="kpi"><span class="label">Max DD</span><br><span class="value">{p['max_drawdown']:.1%}</span></span>
  <span class="kpi"><span class="label">Cum return</span><br><span class="value">{p['cum_return']:+.1%}</span></span>
  <span class="kpi"><span class="label">Avg corr</span><br><span class="value">{metrics['avg_correlation']:.2f}</span></span>
</div>
<h2>Equity curve</h2>
{spark}
<h2>Per ticker</h2>
<table>
<tr><th>Ticker</th><th>Weight</th><th>CAGR</th><th>Vol</th><th>Sharpe</th><th>Max DD</th></tr>
{rows_per_ticker}
</table>
<p style="color:#666;font-size:0.8rem;margin-top:2rem">
Phase W.11 smoke — vectorbt {__import__('vectorbt').__version__}, pyfolio-reloaded, empyrical.<br>
Generated {date.today().isoformat()}.
</p>
</body></html>"""
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], default="us")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--html", action="store_true",
                    help="Render relatório HTML em reports/")
    ap.add_argument("--json", action="store_true",
                    help="Print metrics como JSON")
    args = ap.parse_args()

    print(f"[quant_smoke] market={args.market}, start={args.start}")
    price_df, weights = load_prices(args.market, start=args.start)
    print(f"  loaded {price_df.shape[0]}d × {price_df.shape[1]} tickers")

    metrics, port_ret = compute_metrics(price_df, weights)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        p = metrics["portfolio"]
        print(f"\n=== Portfolio metrics ({metrics['first_date']} -> {metrics['last_date']}, "
              f"{metrics['obs_days']}d) ===")
        print(f"  CAGR:          {p['annual_return']:+.2%}")
        print(f"  Vol anual:     {p['annual_vol']:.2%}")
        print(f"  Sharpe:        {p['sharpe_ratio']:+.2f}")
        print(f"  Sortino:       {p['sortino_ratio']:+.2f}")
        print(f"  Calmar:        {p['calmar_ratio']:+.2f}")
        print(f"  Max DD:        {p['max_drawdown']:.2%}")
        print(f"  Cum return:    {p['cum_return']:+.2%}")
        print(f"  Avg corr:      {metrics['avg_correlation']:.2f}")
        print(f"\n  Top 5 weights: " + ", ".join(
            f"{t}={w:.1%}" for t, w in
            list(metrics["weights"].items())[:5]))

    if args.html:
        out = render_html(metrics, port_ret, args.market)
        print(f"\n  HTML report: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
