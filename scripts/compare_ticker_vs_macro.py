"""CLI: comparar um ticker BR (total return) com séries macro/benchmark.

Devolve:
  - tabela de retornos na consola
  - CSV em reports/compare_<ticker>_<start>_<end>.csv
  - HTML interactivo Plotly em reports/compare_<ticker>_<start>_<end>.html

Uso:
    python scripts/compare_ticker_vs_macro.py ITSA4
    python scripts/compare_ticker_vs_macro.py ITSA4 --months 12
    python scripts/compare_ticker_vs_macro.py ITSA4 --specs ITSA4 SELIC_DAILY CDI_DAILY IBOV
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analytics.compare import compare, growth_pct  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--months", type=int, default=6)
    ap.add_argument("--specs", nargs="*", default=None,
                    help="override das séries a comparar (default: TICKER TICKER:price SELIC_DAILY CDI_DAILY)")
    ap.add_argument("--no-html", action="store_true")
    args = ap.parse_args()

    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=int(args.months * 30.5))
    start = start_dt.strftime("%Y-%m-%d")
    end = end_dt.strftime("%Y-%m-%d")

    specs = args.specs or [args.ticker, f"{args.ticker}:price", "SELIC_DAILY", "CDI_DAILY"]

    df = compare(specs, start=start, end=end)
    returns = growth_pct(df).round(2)

    print(f"\n=== {args.ticker} -- janela {args.months}m ({start} -> {end}) ===")
    print(f"{'série':<18}  retorno")
    print("-" * 30)
    for name, val in returns.items():
        print(f"{name:<18}  {val:>6.2f}%")
    print()

    out_dir = ROOT / "reports"
    out_dir.mkdir(exist_ok=True)
    tag = f"{args.ticker}_{start}_{end}"
    csv_path = out_dir / f"compare_{tag}.csv"
    df.to_csv(csv_path)
    print(f"CSV  → {csv_path.relative_to(ROOT)}")

    if not args.no_html:
        import plotly.graph_objects as go
        fig = go.Figure()
        for col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, mode="lines"))
        fig.update_layout(
            title=f"{args.ticker} vs macro — {args.months}m (base 100 em {start})",
            xaxis_title="data", yaxis_title="índice normalizado (100 = data-base)",
            hovermode="x unified", template="plotly_white",
        )
        html_path = out_dir / f"compare_{tag}.html"
        fig.write_html(str(html_path), include_plotlyjs="cdn")
        print(f"HTML → {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
