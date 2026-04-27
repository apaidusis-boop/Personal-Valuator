"""Compare quarterly releases — diff Q-o-Q + YoY + 4Q TTM.

Para cada ticker:
  - latest period vs prior period (Q-o-Q sequencial)
  - latest period vs same period last year (YoY)
  - latest 4Q sum vs prior 4Q sum (TTM rolling)

Output:
  - JSON detalhado em data/ri_compare/<ticker>_<period>.json
  - Markdown report em obsidian_vault/tickers/<ticker>_RI.md
  - Material change flags (>10% revenue chg, >20% margin chg, >25% debt chg, >30% FCF)

Uso:
    python -m library.ri.compare_releases <ticker>
    python -m library.ri.compare_releases --all-catalog
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"
OUT_JSON = ROOT / "data" / "ri_compare"
OUT_VAULT = ROOT / "obsidian_vault" / "tickers"

OUT_JSON.mkdir(parents=True, exist_ok=True)

MATERIAL_CHG = {
    "revenue":       0.10,
    "ebit":          0.20,
    "net_income":    0.20,
    "ebit_margin":   0.05,    # absolute pp change
    "net_margin":    0.05,
    "debt_total":    0.25,
    "fco":           0.30,
}


def _load_periods(ticker: str) -> list[dict]:
    """Use quarterly_single (single-Q) — resolves YTD ITR artifact.
    Falls back to quarterly_history if single-Q empty (older tickers).
    """
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT * FROM quarterly_single
            WHERE ticker=? ORDER BY period_end DESC
        """, (ticker,)).fetchall()
        if not rows:
            rows = c.execute("""
                SELECT * FROM quarterly_history
                WHERE ticker=? ORDER BY period_end DESC
            """, (ticker,)).fetchall()
    return [dict(r) for r in rows]


def _pct_chg(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or b == 0:
        return None
    return (a - b) / abs(b)


def _abs_chg(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return a - b


def _is_material(metric: str, chg: float | None) -> bool:
    if chg is None:
        return False
    th = MATERIAL_CHG.get(metric, 0.20)
    return abs(chg) >= th


def compare(ticker: str) -> dict:
    periods = _load_periods(ticker)
    if len(periods) < 2:
        return {"ticker": ticker, "error": f"need >=2 periods, got {len(periods)}"}

    latest = periods[0]
    prior = periods[1]

    # Find YoY comparable (same MM-DD, prior year)
    latest_period = latest["period_end"]
    yoy = None
    for p in periods[1:]:
        # Match same month+day
        if p["period_end"][5:] == latest_period[5:]:
            yoy = p
            break

    def diff(curr: dict, comp: dict | None, label: str) -> dict:
        if not comp:
            return {"label": label, "comparable_period": None, "metrics": {}}
        d = {"label": label, "comparable_period": comp["period_end"], "metrics": {}}
        for m in ("revenue", "ebit", "net_income", "debt_total", "fco", "fcf_proxy"):
            d["metrics"][m] = {
                "current": curr.get(m),
                "comparable": comp.get(m),
                "pct_chg": _pct_chg(curr.get(m), comp.get(m)),
                "material": _is_material(m, _pct_chg(curr.get(m), comp.get(m))),
            }
        for m in ("gross_margin", "ebit_margin", "net_margin"):
            d["metrics"][m] = {
                "current": curr.get(m),
                "comparable": comp.get(m),
                "abs_chg_pp": _abs_chg(curr.get(m), comp.get(m)),
                "material": _is_material(m, _abs_chg(curr.get(m), comp.get(m))),
            }
        return d

    result = {
        "ticker": ticker,
        "latest_period": latest_period,
        "qoq": diff(latest, prior, "Q-o-Q"),
        "yoy": diff(latest, yoy, "YoY"),
        "material_flags": [],
    }

    for cmp_kind in ("qoq", "yoy"):
        for m, d in result[cmp_kind]["metrics"].items():
            if d.get("material"):
                chg = d.get("pct_chg") or d.get("abs_chg_pp")
                kind_label = "%" if "pct_chg" in d else "pp"
                if chg is not None:
                    result["material_flags"].append({
                        "comparison": cmp_kind.upper(),
                        "metric": m,
                        "change": f"{chg*100:+.1f}{kind_label}" if kind_label == "%" else f"{chg*100:+.1f}pp",
                    })

    return result


def to_markdown(report: dict, periods: list[dict]) -> str:
    ticker = report["ticker"]
    lines = [
        "---",
        f"type: ri_quarterly_comparison",
        f"ticker: {ticker}",
        f"latest_period: {report['latest_period']}",
        "tags: [ri, quarterly, comparison]",
        "---",
        "",
        f"# {ticker} — RI Quarterly Compare",
        "",
        f"**Latest period**: {report['latest_period']}  ",
        f"**Q-o-Q vs**: {report['qoq']['comparable_period']}  ",
        f"**YoY vs**: {report['yoy']['comparable_period']}  ",
        "",
    ]

    if report["material_flags"]:
        lines.append("## 🚨 Material changes")
        lines.append("")
        for f in report["material_flags"]:
            emoji = "⬆️" if "+" in f["change"] else "⬇️"
            lines.append(f"- {emoji} **{f['comparison']}** `{f['metric']}`: **{f['change']}**")
        lines.append("")
    else:
        lines.append("## ✅ No material changes flagged")
        lines.append("")

    # Diff tables
    for cmp_kind in ("qoq", "yoy"):
        d = report[cmp_kind]
        if not d["comparable_period"]:
            continue
        lines.append(f"## {d['label']} ({report['latest_period']} vs {d['comparable_period']})")
        lines.append("")
        lines.append("| Metric | Current | Prior | Change |")
        lines.append("|---|---:|---:|---:|")
        for m, x in d["metrics"].items():
            cur = x.get("current")
            comp = x.get("comparable")
            chg = x.get("pct_chg") or x.get("abs_chg_pp")
            if cur is None and comp is None:
                continue
            if "margin" in m:
                cur_s = f"{cur*100:.1f}%" if cur is not None else "—"
                comp_s = f"{comp*100:.1f}%" if comp is not None else "—"
                chg_s = f"{chg*100:+.1f}pp" if chg is not None else "—"
            else:
                cur_s = f"R$ {cur/1e6:,.1f} mi" if cur is not None else "—"
                comp_s = f"R$ {comp/1e6:,.1f} mi" if comp is not None else "—"
                chg_s = f"{chg*100:+.1f}%" if chg is not None else "—"
            lines.append(f"| `{m}` | {cur_s} | {comp_s} | {chg_s} |")
        lines.append("")

    # Trajetória 11Q
    lines.append("## 📊 Trajetória 11Q")
    lines.append("")
    lines.append("| Period | Source | Revenue (R$bi) | EBIT margin | Net margin | Debt (R$bi) | FCO (R$bi) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for p in periods[:11]:
        rev = (p['revenue'] or 0) / 1e6
        em = (p['ebit_margin'] or 0) * 100
        nm = (p['net_margin'] or 0) * 100
        dbt = (p['debt_total'] or 0) / 1e6
        fco = (p['fco'] or 0) / 1e6
        src = p.get('source') or p.get('derived_from') or '?'
        lines.append(f"| {p['period_end']} | {src} | {rev:,.1f} | {em:.1f}% | {nm:.1f}% | {dbt:,.0f} | {fco:,.0f} |")
    lines.append("")

    # Dataview chart hint
    lines.append("## Chart: Revenue + EBIT margin trend")
    lines.append("")
    lines.append("```chart")
    lines.append("type: line")
    lines.append('title: "Revenue (R$bi) + EBIT margin %"')
    chart_periods = list(reversed(periods[:11]))
    labels = [p["period_end"] for p in chart_periods]
    revenues = [round((p['revenue'] or 0) / 1e6, 1) for p in chart_periods]
    ebit_margins = [round((p['ebit_margin'] or 0) * 100, 1) for p in chart_periods]
    lines.append(f"labels: {labels}")
    lines.append("series:")
    lines.append(f"  - title: Revenue")
    lines.append(f"    data: {revenues}")
    lines.append(f"  - title: EBIT margin %")
    lines.append(f"    data: {ebit_margins}")
    lines.append("width: 90%")
    lines.append("beginAtZero: false")
    lines.append("tension: 0.3")
    lines.append("```")
    lines.append("")
    lines.append(f"---")
    lines.append(f"*Auto-generated by `library.ri.compare_releases` from CVM official data.*")
    return "\n".join(lines)


def write_outputs(ticker: str, report: dict, periods: list[dict]) -> tuple[Path, Path]:
    json_path = OUT_JSON / f"{ticker}_{report['latest_period']}.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    md_path = OUT_VAULT / f"{ticker}_RI.md"
    md_path.write_text(to_markdown(report, periods), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--all-catalog", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.all_catalog:
        from library.ri.catalog import all_tickers as _all_tickers
        tickers = _all_tickers(include_watchlist=True, include_fiis=False)
    elif args.ticker:
        tickers = [args.ticker.upper()]
    else:
        ap.print_help(); return

    summary = []
    for t in tickers:
        report = compare(t)
        if "error" in report:
            print(f"  {t}: {report['error']}")
            continue
        periods = _load_periods(t)
        json_p, md_p = write_outputs(t, report, periods)
        flags = len(report["material_flags"])
        print(f"  {t}: latest={report['latest_period']} material_flags={flags}")
        for f in report["material_flags"][:5]:
            print(f"    - [{f['comparison']}] {f['metric']}: {f['change']}")
        summary.append({"ticker": t, "flags": flags, "md": str(md_p.relative_to(ROOT))})

    print(f"\nGenerated {len(summary)} reports.")


if __name__ == "__main__":
    main()
