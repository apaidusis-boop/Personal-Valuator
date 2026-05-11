"""analytics.fair_value_forward — EXPERIMENTAL quality-aware forward fair value.

Opção B do plano de fusão (sessão 2026-05-11, ver
`obsidian_vault/Sessions/FairValue_Forward_Audit_2026-05-11.md`).

**NÃO está wired no engine nem no daily_run.** Corre stand-alone, emite um
relatório no vault, e fica como leitura *lado-a-lado* do `scoring.fair_value`
conservador — o `our_fair` persistido continua a ser o teto Buffett-Graham; este
módulo só mostra o que um DCF conservador que *dá crédito ao prémio de qualidade*
diz. Promover (Opção A) só depois de decisão explícita do user.

Método (honest-conservative — memory `feedback_honest_projections`):

  Non-bank, non-REIT (DCF 2-estágios sobre owner earnings):
    owner_earnings = min( mediana(FCF, 3y), mediana(net_income, 3y) )   # conservador
    g1 = clamp( CAGR(net_income, ~5y), 0.02, 0.10 )                     # se <0 ou NaN -> 0.04
    fade linear g1 -> g2 ao longo de 10y; terminal Gordon a g2
    r = discount rate por bucket de risco (staples/health 8.5%, disc/ind/tech/fin 9.5%, energy/mat 10.5%)
    g2 = 0.025 (0.030 p/ asset managers)
    sanity cap: forward_fair = min(dcf_per_share, owner_earnings_per_share * 25)

  Banco (no whitelist `scoring.fair_value._US_BANK_TICKERS`):
    forward_fair = mediana(EPS, 3y) * MULT  (MULT = 14 p/ JPM/BAC/WFC tier, senão 13)
    — substitui o EPS*12 do engine (que usa o *screen ceiling* como fair value)

  REIT:
    forward_fair = AFFO_per_share * P_AFFO  (AFFO de _AFFO_OVERRIDE; P_AFFO=16 default)
    — marcado low_confidence (precisa de calibração de AFFO/sector)

Blend opcional com consenso de analistas (yfinance `targetMeanPrice`, se yfinance
instalado — só o `.venv` tem): blended = 0.6*forward_fair + 0.4*analyst_pt.

Uso:
    python -m analytics.fair_value_forward                  # US holdings + os 8 nomeados
    python -m analytics.fair_value_forward --ticker ACN
    python -m analytics.fair_value_forward --no-analyst     # sem fetch yfinance
    python -m analytics.fair_value_forward --all-us         # todo o universo US
"""
from __future__ import annotations

import argparse
import sqlite3
import statistics
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_US = ROOT / "data" / "us_investments.db"
OUT_DIR = ROOT / "obsidian_vault" / "Bibliotheca"

# Discount rate by sector risk bucket
_R_BUCKETS = {
    "Consumer Staples": 0.085, "Healthcare": 0.085, "Utilities": 0.085,
    "Consumer Disc.": 0.095, "Industrials": 0.095, "Technology": 0.095,
    "Communication": 0.095, "Financials": 0.095,
    "Materials": 0.105, "Energy": 0.105,
}
_DEFAULT_R = 0.095
_ASSET_MGR_TICKERS = frozenset({"BLK", "BX", "KKR", "APO", "TROW", "BEN", "IVZ"})

# REIT AFFO/share estimates (FY just-reported / current run-rate). Hand-maintained;
# the engine's bvps*2 has no AFFO basis. Update when REITs report.
_AFFO_OVERRIDE = {
    "O":   4.22,    # Realty Income — 2025 run-rate
    "PLD": 5.56,    # Prologis — Core FFO/AFFO ~ 2024
}
_P_AFFO_DEFAULT = 16.0

# Tickers where the DCF/multiple read is structurally weak (holdcos, ETFs, distressed)
_LOW_CONF_TICKERS = frozenset({"BN", "BRK-B", "BRK.B", "GREK", "TEN"})
# Skip the DCF entirely for these and emit only a flag:
_FOREIGN_REPORTERS = frozenset({"TSM", "XP"})          # report in non-USD; DCF not comparable to USD price
_GROWTH_PICKS = frozenset({"NU", "PLTR", "TSLA"})       # >20%/yr growers — DCF with a 10% growth cap is meaningless; growth pick, not DRIP
_SKIP_DCF = frozenset({"BN", "BRK-B", "BRK.B", "GREK"})  # holdcos / ETF — earnings-per-share economics don't map to a simple DCF here

# The 8 compounders the user asked about (always included even if not holdings)
_FOCUS = ["KO", "PG", "JNJ", "JPM", "BLK", "O", "ACN", "HD"]


def _conn():
    return sqlite3.connect(DB_US)


def _company(c, ticker):
    r = c.execute("SELECT name, sector, is_holding FROM companies WHERE ticker=?", (ticker,)).fetchone()
    return {"name": r[0], "sector": r[1] or "", "is_holding": bool(r[2])} if r else None


def _price(c, ticker):
    r = c.execute("SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)).fetchone()
    return r[0] if r else None


def _engine_row(c, ticker):
    r = c.execute(
        """SELECT method, fair_price, our_fair, sell_above, action, confidence_label
           FROM fair_value WHERE ticker=? ORDER BY computed_at DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    return {"method": r[0], "fair_price": r[1], "our_fair": r[2], "sell_above": r[3],
            "action": r[4], "confidence": r[5]}


def _annual_series(c, ticker):
    """Latest-first list of dicts from deep_fundamentals (annual)."""
    rows = c.execute(
        """SELECT period_end, total_revenue, net_income, free_cash_flow,
                  diluted_avg_shares, shares_outstanding
           FROM deep_fundamentals WHERE ticker=? AND period_type='annual'
           ORDER BY period_end DESC LIMIT 6""",
        (ticker,),
    ).fetchall()
    out = []
    for r in rows:
        out.append({
            "period_end": r[0], "revenue": r[1], "net_income": r[2],
            "fcf": r[3], "shares": r[4] or r[5],
        })
    return out


def _cagr(values_old_to_new):
    """CAGR from first to last positive value. None if not computable."""
    vals = [v for v in values_old_to_new if v is not None]
    if len(vals) < 2 or vals[0] <= 0 or vals[-1] <= 0:
        return None
    n = len(vals) - 1
    return (vals[-1] / vals[0]) ** (1.0 / n) - 1.0


def _two_stage_dcf(oe0, g1, r, g2, years=10):
    """PV of owner earnings: explicit `years` with g linearly fading g1->g2, then Gordon terminal."""
    pv = 0.0
    last = oe0
    for t in range(1, years + 1):
        c = oe0
        for k in range(1, t + 1):
            g = g1 + (g2 - g1) * (k - 1) / (years - 1)
            c *= (1.0 + g)
        last = c
        pv += c / (1.0 + r) ** t
    term = last * (1.0 + g2) / (r - g2)
    pv += term / (1.0 + r) ** years
    return pv


def _is_bank(ticker):
    try:
        from scoring.fair_value import _US_BANK_TICKERS
        return ticker.upper() in _US_BANK_TICKERS
    except Exception:
        return ticker.upper() in {"JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC"}


def _analyst_pt(ticker):
    """yfinance targetMeanPrice + numberOfAnalystOpinions. None if yfinance missing/fails."""
    try:
        import yfinance as yf
    except ImportError:
        return None
    try:
        info = yf.Ticker(ticker).info
        pt = info.get("targetMeanPrice")
        n = info.get("numberOfAnalystOpinions")
        fwd_eps = info.get("forwardEps")
        if pt and pt > 0:
            return {"pt": float(pt), "n": int(n) if n else None, "fwd_eps": fwd_eps}
    except Exception:
        return None
    return None


def _bare(ticker, co, price, eng, method, low_conf, notes):
    """A result row with no forward number — just the engine read + a flag."""
    return {
        "ticker": ticker, "name": co["name"], "sector": co["sector"], "is_holding": co["is_holding"],
        "price": price, "engine": eng, "method": method,
        "forward_fair": None, "impl_multiple": None, "analyst": None, "blended": None,
        "upside_fwd_pct": None, "upside_blend_pct": None,
        "action_fwd": "—", "action_blend": "—",
        "low_conf": low_conf, "notes": notes,
        "g1": None, "r": None, "g2": None, "oe_ps": None,
    }


def _action_vs(price, fair):
    """Distinct vocab so it doesn't get confused with the engine's BUY/HOLD/SELL."""
    if fair is None or fair <= 0 or price is None:
        return "—"
    ratio = price / fair
    if ratio <= 0.90:
        return "ADD"
    if ratio <= 1.05:
        return "FAIR"
    if ratio <= 1.20:
        return "RICH"
    return "EXPENSIVE"


def compute(ticker: str) -> dict | None:
    ticker = ticker.upper()
    with _conn() as c:
        co = _company(c, ticker)
        if not co:
            return None
        price = _price(c, ticker)
        eng = _engine_row(c, ticker)
        series = _annual_series(c, ticker)

    sector = co["sector"]
    notes: list[str] = []
    low_conf = ticker in _LOW_CONF_TICKERS

    forward_fair = None
    method = None
    impl_multiple = None
    g1 = r = g2 = oe_ps = None

    # Early-out: tickers where this method doesn't apply — emit a flag, not a number.
    if ticker in _FOREIGN_REPORTERS:
        return _bare(ticker, co, price, eng, "skip_foreign_ccy", True,
                     ["reporta em moeda ≠ USD — owner earnings de deep_fundamentals não comparáveis ao preço em USD; usar valuation nativa"])
    if ticker in _GROWTH_PICKS:
        return _bare(ticker, co, price, eng, "skip_growth_pick", True,
                     ["growth pick (>20%/ano) — DCF com cap de crescimento 8% não tem sentido; valorizar por outra lente (memory user_investment_intents)"])
    if ticker in _SKIP_DCF:
        return _bare(ticker, co, price, eng, "skip_holdco_etf", True,
                     ["holdco / ETF — economia por ação não mapeia para um DCF simples; ver dossiê / NAV"])

    analyst = _analyst_pt(ticker)   # {pt, n, fwd_eps} or None

    if _is_bank(ticker):
        method = "bank_pe_normalized"
        eps_hist = []
        for row in series[:3]:
            if row["net_income"] and row["shares"] and row["shares"] > 0:
                eps_hist.append(row["net_income"] / row["shares"])
        if eps_hist:
            eps_norm = statistics.median(eps_hist)
            mult = 14.0 if ticker in {"JPM", "BAC", "WFC"} else 13.0
            forward_fair = eps_norm * mult
            impl_multiple = mult
            notes.append(f"EPS norm. (mediana 3y) = {eps_norm:.2f}; multiple {mult:.0f}× (engine usa {eng['method'] if eng else '?'} = ×12, que é o *screen ceiling*)")
        else:
            notes.append("sem EPS histórico suficiente")
    elif "REIT" in sector.upper():
        method = "reit_p_affo"
        low_conf = True
        affo = _AFFO_OVERRIDE.get(ticker)
        if affo:
            forward_fair = affo * _P_AFFO_DEFAULT
            impl_multiple = _P_AFFO_DEFAULT
            notes.append(f"AFFO/share ≈ {affo:.2f} (hand-maintained); P/AFFO {_P_AFFO_DEFAULT:.0f}× (engine usa BVPS×2, sem base AFFO). Calibrar P/AFFO por sub-sector.")
        else:
            notes.append("sem AFFO override — precisa de input externo")
    else:
        method = "owner_earnings_dcf2"
        ni_hist = [row["net_income"] for row in series[:3] if row["net_income"] is not None and row["net_income"] > 0]
        fcf_hist = [row["fcf"] for row in series[:3] if row["fcf"] is not None and row["fcf"] > 0]
        shares = next((row["shares"] for row in series if row["shares"] and row["shares"] > 0), None)
        # Owner-earnings base / share: prefer the street's forward EPS (already strips
        # acquisition amort / one-off charges — closer to economic earnings for
        # acquisitive compounders like BLK/ACN/JNJ than GAAP NI). Fall back to
        # 3y-median NI haircut by cash conversion (floored 85%, capped 100%).
        oe_base_src = None
        if analyst and analyst.get("fwd_eps") and analyst["fwd_eps"] > 0:
            oe_ps = float(analyst["fwd_eps"])
            oe_base_src = f"forward EPS consenso ≈ {oe_ps:.2f}"
        elif ni_hist and shares:
            med_ni = statistics.median(ni_hist)
            med_fcf = statistics.median(fcf_hist) if fcf_hist else med_ni
            conv = max(0.85, min(1.0, med_fcf / med_ni)) if med_ni else 0.85
            oe_ps = (med_ni * conv) / shares
            oe_base_src = f"mediana NI 3y × conversão de caixa {conv:.0%} ≈ {oe_ps:.2f}/sh"
            if conv == 0.85 and (med_fcf / med_ni) < 0.85:
                notes.append(f"conversão de caixa 3y baixa ({med_fcf/med_ni:.0%}) — owner earnings floored a 85% do lucro (dip de FCF tratado como temporário)")
        if oe_ps:
            # growth: CAGR of NI over available years, capped by sector (defensives slower)
            ni_chrono = [row["net_income"] for row in reversed(series) if row["net_income"] is not None]
            g_hist = _cagr(ni_chrono)
            g_cap = 0.06 if sector in ("Consumer Staples", "Healthcare", "Utilities") else 0.08
            if g_hist is None or g_hist < 0:
                g1 = 0.04
                notes.append("CAGR histórico de lucro negativo/indisponível (charges one-off / ciclo?) → g1=4% por defeito conservador")
            else:
                g1 = max(0.02, min(g_hist, g_cap))
                if g_hist > g_cap:
                    notes.append(f"CAGR histórico {g_hist:.1%} cortado para o cap sectorial de {g_cap:.0%}")
            r = _R_BUCKETS.get(sector, _DEFAULT_R)
            g2 = 0.030 if ticker in _ASSET_MGR_TICKERS else 0.025
            dcf_ps = _two_stage_dcf(oe_ps, g1, r, g2)
            # Sanity band on owner earnings: wide-moat names rarely de-rate below ~16×
            # absent a crisis, and we won't pay above ~25×. Clamp the DCF into the band.
            lo, hi = oe_ps * 16.0, oe_ps * 25.0
            forward_fair = max(lo, min(dcf_ps, hi))
            impl_multiple = forward_fair / oe_ps
            if dcf_ps > hi:
                notes.append("DCF acima de 25× owner earnings — limitado ao topo da banda de sanidade")
            elif dcf_ps < lo:
                notes.append("DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise)")
            notes.append(f"base = {oe_base_src}; g1={g1:.1%} fade→{g2:.1%}; desconto r={r:.1%}; banda 16-25× OE")
        else:
            notes.append("sem forward EPS nem NI/shares suficientes para o DCF")

    # analyst blend (weight 60% forward fair / 40% street price target)
    blended = forward_fair
    if forward_fair and analyst:
        blended = 0.6 * forward_fair + 0.4 * analyst["pt"]

    upside_fwd = (forward_fair / price - 1.0) * 100.0 if (forward_fair and price) else None
    upside_blend = (blended / price - 1.0) * 100.0 if (blended and price) else None

    return {
        "ticker": ticker, "name": co["name"], "sector": sector, "is_holding": co["is_holding"],
        "price": price, "engine": eng, "method": method,
        "forward_fair": forward_fair, "impl_multiple": impl_multiple,
        "analyst": analyst, "blended": blended,
        "upside_fwd_pct": upside_fwd, "upside_blend_pct": upside_blend,
        "action_fwd": _action_vs(price, forward_fair),
        "action_blend": _action_vs(price, blended),
        "low_conf": low_conf, "notes": notes,
        "g1": g1, "r": r, "g2": g2, "oe_ps": oe_ps,
    }


def _holdings_us() -> list[str]:
    with _conn() as c:
        rows = c.execute("SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1").fetchall()
    return sorted({r[0] for r in rows})


def _universe_us() -> list[str]:
    with _conn() as c:
        rows = c.execute("SELECT ticker FROM companies").fetchall()
    return sorted({r[0] for r in rows})


def _fmt(x, dp=2, prefix="$"):
    return f"{prefix}{x:,.{dp}f}" if x is not None else "—"


def _fmt_pct(x):
    return f"{x:+.1f}%" if x is not None else "—"


def write_report(results: list[dict]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = OUT_DIR / f"FairValue_Forward_{today}.md"
    lines: list[str] = []
    lines.append(f"# Fair Value Forward — leitura quality-aware (US)  ·  {today}")
    lines.append("")
    lines.append("> **EXPERIMENTAL** — `analytics.fair_value_forward`. NÃO está no engine nem no daily_run.")
    lines.append("> Mostra o que um DCF conservador que *dá crédito ao prémio de qualidade* diz, lado a lado")
    lines.append("> com o teto Buffett-Graham (`our_fair`) que continua a ser o número oficial persistido.")
    lines.append("> Método em `analytics/fair_value_forward.py` (docstring). Decisão A/B de fusão pendente —")
    lines.append("> ver [[Sessions/FairValue_Forward_Audit_2026-05-11]] e [[Bibliotheca/Manual_de_Direcao]].")
    lines.append("")
    lines.append("| Ticker | Sector | Preço | Engine `our_fair` / action | **Forward fair** (impl. mult.) | Margem | Analistas PT (n) | **Leitura fwd** |")
    lines.append("|---|---|---|---|---|---|---|---|")
    # focus first, then the rest
    focus = [r for r in results if r["ticker"] in _FOCUS]
    rest = [r for r in results if r["ticker"] not in _FOCUS]
    for r in focus + rest:
        eng = r["engine"]
        eng_s = f"{_fmt(eng['our_fair'])} / {eng['action']}" if eng else "—"
        mult_s = f" ({r['impl_multiple']:.1f}×)" if r["impl_multiple"] else ""
        an = r["analyst"]
        an_s = f"{_fmt(an['pt'])} ({an['n']})" if an else "—"
        lc = " ⚠️" if r["low_conf"] else ""
        star = "★" if r["is_holding"] else " "
        # Margem = upside vs forward fair (positivo = preço abaixo do forward fair).
        # The headline action is the *pure forward* read (conservador); if the street
        # PT is materially more bullish/bearish than forward fair, annotate.
        action_h = r["action_fwd"]
        flag = ""
        if an and r["forward_fair"]:
            pt_ratio = an["pt"] / r["forward_fair"]
            if pt_ratio >= 1.12:
                flag = " · *street mais bull (PT ≫ fwd)*"
            elif pt_ratio <= 0.92:
                flag = " · *street mais bear (PT ≪ fwd)*"
        lines.append(
            f"| {star} **{r['ticker']}** | {r['sector']} | {_fmt(r['price'])} | {eng_s} | "
            f"{_fmt(r['forward_fair'])}{mult_s}{lc} | {_fmt_pct(r['upside_fwd_pct'])} | {an_s} | "
            f"**{action_h}**{flag} |"
        )
    lines.append("")
    lines.append("`Margem` = quanto o forward fair está acima(+)/abaixo(−) do preço atual. Vocab `Leitura fwd` (sobre o **forward fair puro**, não misturado com o PT dos analistas): **ADD** = preço ≤ 90% do forward fair (margem ≥ ~10%) · **FAIR** = ±5% · **RICH** = 5-20% acima · **EXPENSIVE** = >20% acima. ⚠️ = baixa confiança (holdco/ETF/REIT sem AFFO calibrado/distressed). O PT dos analistas é mostrado só como referência — *não* entra na leitura (disciplina: não confiar no número que adoramos).")
    lines.append("")
    lines.append("## Notas por ticker")
    lines.append("")
    for r in focus + rest:
        if not r["notes"]:
            continue
        lines.append(f"- **{r['ticker']}** — " + " · ".join(r["notes"]))
    lines.append("")
    lines.append("## Como ler isto vs o engine")
    lines.append("")
    lines.append("- `our_fair` (engine) = teto Buffett-Graham menos margem de segurança — **disciplina de preço**, deliberadamente exigente. Grita 'múltiplo rico' cedo.")
    lines.append("- `Forward fair` (este módulo) = DCF 2-estágios sobre owner earnings (conservador: g cortado, fade para 2,5-3%, desconto 8,5-9,5%, teto 25× OE) — **dá crédito ao prémio de qualidade** de um negócio de fosso largo e ROIC durável.")
    lines.append("- A verdade está entre os dois. Quando o engine diz SELL e o forward diz FAIR, a leitura humana é 'não está barato mas SELL é exagero' (KO/JNJ). Quando ambos dizem ADD/cheap, é sinal forte (ACN).")
    lines.append("- Bancos: o forward usa EPS normalizado × 13-14× (best-in-class), não o ×12 do screen ceiling. REITs: P/AFFO, não BVPS×2 — mas precisa de AFFO calibrado por sub-sector.")
    lines.append("")
    lines.append(f"_Gerado por `python -m analytics.fair_value_forward` em {today}. Fontes: `data/us_investments.db` (deep_fundamentals annual, fair_value, prices) + yfinance analyst targets (se disponível)._")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ticker", help="single ticker")
    g.add_argument("--all-us", action="store_true", help="todo o universo US")
    ap.add_argument("--no-analyst", action="store_true", help="não fazer fetch yfinance de price targets")
    ap.add_argument("--no-report", action="store_true", help="só imprime, não escreve o md")
    args = ap.parse_args()

    if args.no_analyst:
        global _analyst_pt
        _analyst_pt = lambda t: None  # noqa: E731

    if args.ticker:
        targets = [args.ticker.upper()]
    elif args.all_us:
        targets = _universe_us()
    else:
        targets = sorted(set(_holdings_us()) | set(_FOCUS))

    results = []
    for tk in targets:
        try:
            r = compute(tk)
            if r is None:
                print(f"  {tk}: not found")
                continue
            results.append(r)
            fwd = r["forward_fair"]
            print(
                f"  {tk:<8} {r['method']:<22} fwd={_fmt(fwd):>12} "
                f"price={_fmt(r['price']):>12}  {r['action_fwd']:<10}"
                f"  (engine our_fair={_fmt(r['engine']['our_fair']) if r['engine'] else '—'} / {r['engine']['action'] if r['engine'] else '—'})"
            )
        except Exception as e:  # noqa: BLE001
            print(f"  {tk}: error — {type(e).__name__}: {e}")

    if results and not args.no_report:
        path = write_report(results)
        print(f"\nReport: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
