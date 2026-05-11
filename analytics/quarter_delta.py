"""quarter_delta — compare last 2 quarters of filings; emit structured deltas
+ PT narrative for the filing-driven dossier.

Sources:
  BR non-bank: quarterly_single (resolves YTD artifact for ITRs/DFP)
  BR bank:     bank_quarterly_history (NII/PDD/efficiency native; pretax/equity)
  US:         not yet wired (needs SEC EDGAR XBRL parser); returns None.

Delta forms emitted per metric:
  abs    — absolute change (latest − prior)
  pct    — relative change (abs / |prior| × 100)
  yoy    — relative change vs same quarter prior year (when available)

Narrative shape (Portuguese, mobile-friendly bullets):
  Receita 70.4B vs 65.3B (+7.7% QoQ, +34.0% YoY)
  EBIT 15.3B (+0.7% QoQ); margem 21.7% vs 22.4%
  Lucro líquido 5.6B (-9.4% QoQ, +12.6% YoY)
  Dívida líquida −2.1% QoQ; equity +2.2%

Used by:
  scripts/auto_verdict_on_filing — embeds in `<TK>_FILING_<DATE>.md` dossier

CLI:
    python -m analytics.quarter_delta BBDC4
    python -m analytics.quarter_delta ITSA4 --json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _is_bank(c: sqlite3.Connection, ticker: str) -> bool:
    r = c.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
    if not r or not r[0]:
        return False
    s = r[0].strip().lower()
    return any(tok in s for tok in ("bank", "banks", "banco", "bancos"))


def _abs_pct(latest: float | None, prior: float | None) -> dict:
    if latest is None or prior is None:
        return {"abs": None, "pct": None}
    abs_d = latest - prior
    if prior == 0:
        return {"abs": round(abs_d, 4), "pct": None}
    pct_d = (abs_d / abs(prior)) * 100.0
    return {"abs": round(abs_d, 4), "pct": round(pct_d, 2)}


def _bank_deltas(c: sqlite3.Connection, ticker: str) -> dict | None:
    rows = c.execute(
        """SELECT period_end, nii, fee_income, loan_loss_provisions, pretax_income,
                  net_income, total_assets, equity, cost_to_income_ratio, npl_ratio,
                  loan_book, pdd_reserve, cet1_ratio
           FROM bank_quarterly_history WHERE ticker=? ORDER BY period_end DESC LIMIT 5""",
        (ticker,),
    ).fetchall()
    if len(rows) < 2:
        return None
    cols = ["period_end", "nii", "fee_income", "pdd_loss", "pretax_income",
            "net_income", "total_assets", "equity", "cost_to_income", "npl_ratio",
            "loan_book", "pdd_reserve", "cet1_ratio"]
    by_idx = [dict(zip(cols, r, strict=True)) for r in rows]
    latest, prior = by_idx[0], by_idx[1]
    yoy = next((r for r in by_idx[2:] if r["period_end"][:4] != latest["period_end"][:4]
                and r["period_end"][5:7] == latest["period_end"][5:7]), None)

    def trio(metric: str) -> dict:
        d = {"latest": latest.get(metric), "prior": prior.get(metric)}
        d.update({"qoq_" + k: v for k, v in _abs_pct(latest.get(metric), prior.get(metric)).items()})
        if yoy:
            d.update({"yoy_" + k: v for k, v in _abs_pct(latest.get(metric), yoy.get(metric)).items()})
        return d

    return {
        "kind": "bank",
        "latest_period": latest["period_end"],
        "prior_period": prior["period_end"],
        "yoy_period": yoy["period_end"] if yoy else None,
        "metrics": {
            "nii": trio("nii"),
            "fee_income": trio("fee_income"),
            "pdd_loss": trio("pdd_loss"),
            "pretax_income": trio("pretax_income"),
            "net_income": trio("net_income"),
            "total_assets": trio("total_assets"),
            "equity": trio("equity"),
            "loan_book": trio("loan_book"),
            "pdd_reserve": trio("pdd_reserve"),
            "cost_to_income": trio("cost_to_income"),
            "npl_ratio": trio("npl_ratio"),
            "cet1_ratio": trio("cet1_ratio"),
        },
    }


def _ops_deltas(c: sqlite3.Connection, ticker: str) -> dict | None:
    rows = c.execute(
        """SELECT period_end, revenue, gross_profit, ebit, net_income, equity,
                  debt_total, fcf_proxy, gross_margin, ebit_margin, net_margin
           FROM quarterly_single WHERE ticker=? ORDER BY period_end DESC LIMIT 5""",
        (ticker,),
    ).fetchall()
    if len(rows) < 2:
        return None
    cols = ["period_end", "revenue", "gross_profit", "ebit", "net_income",
            "equity", "debt_total", "fcf_proxy", "gross_margin", "ebit_margin",
            "net_margin"]
    by_idx = [dict(zip(cols, r, strict=True)) for r in rows]
    latest, prior = by_idx[0], by_idx[1]
    yoy = next((r for r in by_idx[2:] if r["period_end"][:4] != latest["period_end"][:4]
                and r["period_end"][5:7] == latest["period_end"][5:7]), None)

    def trio(metric: str) -> dict:
        d = {"latest": latest.get(metric), "prior": prior.get(metric)}
        d.update({"qoq_" + k: v for k, v in _abs_pct(latest.get(metric), prior.get(metric)).items()})
        if yoy:
            d.update({"yoy_" + k: v for k, v in _abs_pct(latest.get(metric), yoy.get(metric)).items()})
        return d

    return {
        "kind": "ops",
        "latest_period": latest["period_end"],
        "prior_period": prior["period_end"],
        "yoy_period": yoy["period_end"] if yoy else None,
        "metrics": {
            "revenue": trio("revenue"),
            "gross_profit": trio("gross_profit"),
            "ebit": trio("ebit"),
            "net_income": trio("net_income"),
            "equity": trio("equity"),
            "debt_total": trio("debt_total"),
            "fcf_proxy": trio("fcf_proxy"),
            "gross_margin": trio("gross_margin"),
            "ebit_margin": trio("ebit_margin"),
            "net_margin": trio("net_margin"),
        },
    }


def compute(ticker: str, market: str = "br") -> dict | None:
    """Returns {kind: 'bank'|'ops', latest_period, prior_period, metrics:{...}}.

    None when there's no parser coverage (US today) or insufficient history.
    """
    if market != "br":
        return None
    db = DB_BR
    with sqlite3.connect(db) as c:
        if _is_bank(c, ticker):
            d = _bank_deltas(c, ticker)
            if d:
                return d
        return _ops_deltas(c, ticker)


# --- Narrative ---

_PT_NUMS = ("k", "M", "B", "T")


def _abbrev(value: float | None, *, in_thousands: bool = True) -> str:
    """Format BRL values for narrative. quarterly_single stores in thousand BRL,
    so default in_thousands=True multiplies × 1000 to get raw BRL before abbrev.
    Result e.g.: 70.4B, 12.5M, R$5.5B."""
    if value is None:
        return "—"
    v = value * 1000.0 if in_thousands else float(value)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v < 1e3:
        return f"{sign}{v:.0f}"
    for unit, scale in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if v >= scale:
            return f"{sign}{v/scale:.1f}{unit}"
    return f"{sign}{v:.0f}"


def _pct_str(pct: float | None) -> str:
    if pct is None:
        return "—"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}%"


def render_narrative(delta: dict) -> str:
    """PT narrative (markdown bullets) for the filing dossier."""
    if not delta:
        return "_(sem deltas computáveis — histórico insuficiente)_"

    m = delta["metrics"]
    latest, prior = delta["latest_period"], delta["prior_period"]
    yoy = delta.get("yoy_period")
    head = f"**Filing período**: `{latest}` vs prior `{prior}`"
    if yoy:
        head += f" | YoY: `{yoy}`"

    lines = [head, ""]

    if delta["kind"] == "bank":
        # Bank narrative — focus on NII, PDD, efficiency
        lines.append("**P&L**")
        nii = m["nii"]; lines.append(
            f"- NII {_abbrev(nii['latest'])} ({_pct_str(nii.get('qoq_pct'))} QoQ"
            + (f", {_pct_str(nii.get('yoy_pct'))} YoY)" if yoy else ")"))
        pdd = m["pdd_loss"]; lines.append(
            f"- PDD {_abbrev(pdd['latest'])} ({_pct_str(pdd.get('qoq_pct'))} QoQ)"
            + (f" — sinal de risco crescente" if (pdd.get('qoq_pct') or 0) > 10 else "")
        )
        ni = m["net_income"]; lines.append(
            f"- Lucro líquido {_abbrev(ni['latest'])} ({_pct_str(ni.get('qoq_pct'))} QoQ"
            + (f", {_pct_str(ni.get('yoy_pct'))} YoY)" if yoy else ")"))
        ci = m["cost_to_income"]
        if ci.get("latest") is not None:
            lines.append(f"- Eficiência {ci['latest']*100:.1f}% (vs {ci['prior']*100:.1f}% prior)"
                         if isinstance(ci.get("latest"), (int, float)) and ci["latest"] < 1
                         else f"- Eficiência {ci['latest']:.1f} (vs {ci['prior']:.1f} prior)")
        lines.append("")
        lines.append("**BS / risco**")
        lb = m["loan_book"]
        if lb.get("latest"):
            lines.append(f"- Carteira de crédito {_abbrev(lb['latest'])} ({_pct_str(lb.get('qoq_pct'))} QoQ)")
        npl = m["npl_ratio"]
        if npl.get("latest") is not None:
            lines.append(f"- NPL {npl['latest']*100:.2f}% (vs {(npl.get('prior') or 0)*100:.2f}% prior)"
                         if isinstance(npl.get("latest"), (int, float)) and npl["latest"] < 1
                         else f"- NPL {npl['latest']:.2f} (vs {npl.get('prior')} prior)")
        cet1 = m["cet1_ratio"]
        if cet1.get("latest") is not None:
            # CET1 stored as fraction (0.114 = 11.4%); upscale to pct.
            cur, prior = cet1["latest"] * 100, (cet1.get("prior") or 0) * 100
            lines.append(f"- CET1 {cur:.2f}% (vs {prior:.2f}% prior)")
        eq = m["equity"]
        lines.append(f"- Equity {_abbrev(eq['latest'])} ({_pct_str(eq.get('qoq_pct'))} QoQ)")
    else:
        # Operating company narrative — revenue, ebit, fcf, debt
        lines.append("**P&L**")
        rev = m["revenue"]; lines.append(
            f"- Receita {_abbrev(rev['latest'])} ({_pct_str(rev.get('qoq_pct'))} QoQ"
            + (f", {_pct_str(rev.get('yoy_pct'))} YoY)" if yoy else ")"))
        ebit = m["ebit"]; lines.append(
            f"- EBIT {_abbrev(ebit['latest'])} ({_pct_str(ebit.get('qoq_pct'))} QoQ)")
        em = m["ebit_margin"]
        if em.get("latest") is not None and em.get("prior") is not None:
            lines.append(f"- Margem EBIT {em['latest']*100:.1f}% vs {em['prior']*100:.1f}% prior"
                         if abs(em['latest']) < 1 else f"- Margem EBIT {em['latest']:.1f} vs {em['prior']:.1f} prior")
        ni = m["net_income"]; lines.append(
            f"- Lucro líquido {_abbrev(ni['latest'])} ({_pct_str(ni.get('qoq_pct'))} QoQ"
            + (f", {_pct_str(ni.get('yoy_pct'))} YoY)" if yoy else ")"))
        lines.append("")
        lines.append("**BS / cash**")
        eq = m["equity"]; lines.append(
            f"- Equity {_abbrev(eq['latest'])} ({_pct_str(eq.get('qoq_pct'))} QoQ)")
        debt = m["debt_total"]
        if debt.get("latest"):
            lines.append(f"- Dívida total {_abbrev(debt['latest'])} ({_pct_str(debt.get('qoq_pct'))} QoQ)")
        fcf = m["fcf_proxy"]
        if fcf.get("latest"):
            lines.append(f"- FCF proxy {_abbrev(fcf['latest'])} ({_pct_str(fcf.get('qoq_pct'))} QoQ)")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    d = compute(args.ticker.upper(), market=args.market)
    if d is None:
        print(f"{args.ticker}: no quarter delta (missing source / insufficient history)")
        return 1

    if args.json:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(render_narrative(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
