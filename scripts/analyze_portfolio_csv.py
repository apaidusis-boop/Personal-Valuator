"""Analyser de CSV de portfólio exportado pela corretora (formato J.P. Morgan).

Lê o CSV, ignora rodapés/notas, sumariza por asset class e produz:
  - total market value, cost basis, P&L absoluto e percentual
  - breakdown por asset class e por asset strategy
  - posições ordenadas por market value
  - top gainers / losers
  - concentração (top N % do portfolio)
  - income estimado anual + yield efectivo da carteira

Uso:
    python scripts/analyze_portfolio_csv.py "C:/path/to/positions.csv"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

KEEP = [
    "Asset Class", "Asset Strategy", "Description", "Ticker",
    "Quantity", "Price", "Value", "Cost",
    "Unrealized G/L Amt.", "Unrealized Gain/Loss (%)",
    "Est. Annual Income",
]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, thousands=",", encoding="utf-8-sig")
    # descartar rodapés: linhas onde Asset Class é "FOOTNOTES" ou letras soltas
    df = df[df["Ticker"].notna() | df["Asset Class"].isin(
        ["Equity", "Fixed Income & Cash", "Alternative Assets"]
    )]
    df = df[df["Asset Class"].isin(
        ["Equity", "Fixed Income & Cash", "Alternative Assets"]
    )].copy()
    # normalizar
    for col in ["Quantity", "Price", "Value", "Cost",
                "Unrealized G/L Amt.", "Unrealized Gain/Loss (%)",
                "Est. Annual Income"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[KEEP].reset_index(drop=True)


def _fmt_usd(v: float) -> str:
    sign = "-" if v < 0 else ""
    return f"{sign}${abs(v):>12,.2f}"


def _fmt_pct(v: float) -> str:
    return f"{v:>+7.2f}%" if pd.notna(v) else "     --"


def print_header(title: str) -> None:
    print(f"\n{'=' * 78}\n  {title}\n{'=' * 78}")


def totals(df: pd.DataFrame) -> dict:
    equity = df[df["Asset Class"] == "Equity"]
    alts = df[df["Asset Class"] == "Alternative Assets"]
    cash = df[df["Asset Class"] == "Fixed Income & Cash"]
    invested = equity["Value"].sum() + alts["Value"].sum()
    cash_net = cash["Value"].sum()
    total = invested + cash_net
    cost = equity["Cost"].sum() + alts["Cost"].sum()
    pnl = equity["Unrealized G/L Amt."].sum() + alts["Unrealized G/L Amt."].sum()
    income = df["Est. Annual Income"].sum(skipna=True)
    return {
        "total": total, "invested": invested, "cash_net": cash_net,
        "cost_basis": cost, "pnl": pnl,
        "pnl_pct": (pnl / cost * 100) if cost else 0.0,
        "est_annual_income": income,
        "effective_yield": (income / invested * 100) if invested else 0.0,
    }


def print_summary(df: pd.DataFrame, t: dict) -> None:
    print_header("PORTFOLIO — SUMÁRIO")
    print(f"  Valor total:           {_fmt_usd(t['total'])}")
    print(f"  Investido (equity+alt):{_fmt_usd(t['invested'])}")
    print(f"  Cash líquido:          {_fmt_usd(t['cash_net'])}  "
          f"({t['cash_net'] / t['total'] * 100:+.1f}% do total)")
    print(f"  Cost basis:            {_fmt_usd(t['cost_basis'])}")
    print(f"  P&L não realizado:     {_fmt_usd(t['pnl'])}  "
          f"({t['pnl_pct']:+.2f}%)")
    print(f"  Income anual estimado: {_fmt_usd(t['est_annual_income'])}")
    print(f"  Yield efectivo:        {t['effective_yield']:.2f}%")


def print_by_class(df: pd.DataFrame) -> None:
    print_header("BREAKDOWN por Asset Class")
    g = df.groupby("Asset Class").agg(
        n=("Ticker", "count"),
        value=("Value", "sum"),
        cost=("Cost", "sum"),
        pnl=("Unrealized G/L Amt.", "sum"),
    ).sort_values("value", ascending=False)
    total_inv = g.loc[g.index != "Fixed Income & Cash", "value"].sum()
    print(f"  {'class':<22} {'n':>3} {'value':>15} {'cost':>15} {'pnl':>13} {'% inv':>7}")
    print(f"  {'-'*22} {'-'*3} {'-'*15} {'-'*15} {'-'*13} {'-'*7}")
    for cls, row in g.iterrows():
        pct = (row["value"] / total_inv * 100) if cls != "Fixed Income & Cash" else None
        pct_s = f"{pct:>6.1f}%" if pct is not None else "   cash"
        print(f"  {cls:<22} {int(row['n']):>3} {_fmt_usd(row['value'])} "
              f"{_fmt_usd(row['cost'])} {_fmt_usd(row['pnl'])} {pct_s}")


def print_by_strategy(df: pd.DataFrame) -> None:
    print_header("BREAKDOWN por Strategy")
    g = df[df["Asset Class"] != "Fixed Income & Cash"].groupby("Asset Strategy").agg(
        n=("Ticker", "count"),
        value=("Value", "sum"),
        pnl=("Unrealized G/L Amt.", "sum"),
    ).sort_values("value", ascending=False)
    total = g["value"].sum()
    print(f"  {'strategy':<32} {'n':>3} {'value':>15} {'pnl':>13} {'% inv':>7}")
    print(f"  {'-'*32} {'-'*3} {'-'*15} {'-'*13} {'-'*7}")
    for strat, row in g.iterrows():
        pct = row["value"] / total * 100
        print(f"  {strat[:32]:<32} {int(row['n']):>3} {_fmt_usd(row['value'])} "
              f"{_fmt_usd(row['pnl'])} {pct:>6.1f}%")


def print_positions(df: pd.DataFrame) -> None:
    print_header("POSIÇÕES (por market value)")
    eq = df[df["Asset Class"] != "Fixed Income & Cash"].sort_values("Value", ascending=False)
    total = eq["Value"].sum()
    print(f"  {'#':>2} {'ticker':<6} {'qty':>10} {'price':>10} {'value':>13} "
          f"{'cost':>13} {'pnl%':>8} {'%pf':>6}")
    print(f"  {'-'*2} {'-'*6} {'-'*10} {'-'*10} {'-'*13} {'-'*13} {'-'*8} {'-'*6}")
    for i, (_, r) in enumerate(eq.iterrows(), 1):
        pct_pf = r["Value"] / total * 100
        print(f"  {i:>2} {str(r['Ticker']):<6} {r['Quantity']:>10.4f} "
              f"{r['Price']:>10.2f} {_fmt_usd(r['Value'])} {_fmt_usd(r['Cost'])} "
              f"{_fmt_pct(r['Unrealized Gain/Loss (%)'])} {pct_pf:>5.1f}%")


def print_top_movers(df: pd.DataFrame) -> None:
    eq = df[(df["Asset Class"] != "Fixed Income & Cash") &
            df["Unrealized Gain/Loss (%)"].notna()].copy()
    top = eq.nlargest(5, "Unrealized Gain/Loss (%)")
    bot = eq.nsmallest(5, "Unrealized Gain/Loss (%)")

    print_header("TOP 5 GAINERS  /  TOP 5 LOSERS")
    print("  GAINERS")
    for _, r in top.iterrows():
        print(f"    {str(r['Ticker']):<6} {_fmt_pct(r['Unrealized Gain/Loss (%)'])}  "
              f"{_fmt_usd(r['Unrealized G/L Amt.'])}  ({str(r['Description'])[:40]})")
    print("  LOSERS")
    for _, r in bot.iterrows():
        print(f"    {str(r['Ticker']):<6} {_fmt_pct(r['Unrealized Gain/Loss (%)'])}  "
              f"{_fmt_usd(r['Unrealized G/L Amt.'])}  ({str(r['Description'])[:40]})")


def print_concentration(df: pd.DataFrame) -> None:
    eq = df[df["Asset Class"] != "Fixed Income & Cash"].sort_values("Value", ascending=False)
    total = eq["Value"].sum()
    print_header("CONCENTRAÇÃO")
    for k in [1, 3, 5, 10]:
        pct = eq.head(k)["Value"].sum() / total * 100
        tickers = ", ".join(eq.head(k)["Ticker"].astype(str).tolist())
        print(f"  Top {k:>2}: {pct:>5.1f}%  ({tickers})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="path to positions CSV")
    args = ap.parse_args()

    path = Path(args.csv)
    if not path.exists():
        sys.exit(f"não encontrado: {path}")

    df = load(path)
    t = totals(df)

    print_summary(df, t)
    print_by_class(df)
    print_by_strategy(df)
    print_positions(df)
    print_top_movers(df)
    print_concentration(df)


if __name__ == "__main__":
    main()
