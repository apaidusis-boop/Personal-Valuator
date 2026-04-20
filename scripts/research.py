"""Research CLI unificado — deep-dive em 1 ticker.

Produz um memorando estruturado em português (BR) ou inglês técnico (US),
combinando TODAS as camadas determinísticas que já temos no sistema:

  1. Identificação: ticker, nome, sector, preço, market cap
  2. Screen verdict (scoring.engine) — Buffett/Graham sector-aware
  3. Altman Z-Score (scoring.altman) — distress predictor
  4. Piotroski F-Score (scoring.piotroski) — quality composite
  5. Dividend safety (scoring.dividend_safety) — forward-looking 0-100
  6. DY vs own history (analytics.dy_percentile) — entry-timing
  7. DRIP base scenario (scripts.drip_projection) — TR forward
  8. Thesis qualitativa (scripts.thesis_manager) — ticker/sector/macro
  9. Regime macro (analytics.regime) — contexto descritivo
 10. Posição actual (portfolio_positions) — MV, P&L, posição relativa

Regras determinísticas para o veredito final:
  • Altman Z < 1.81  →  AVOID (veto estrutural de distress)
  • Piotroski F ≤ 3  →  AVOID (veto estrutural de qualidade degradada)
  • Screen score < 0.4 →  AVOID
  • Screen ≥ 0.8 AND Altman SAFE AND Piotroski ≥ 5  →  BUY
  • Resto  →  HOLD (ou "WATCH" se não for posição)

Fetchers invocados automaticamente se a deep_fundamentals estiver vazia.

Zero rede se dados já estão persistidos. 1-2 chamadas yfinance se não.

CLI:
    python scripts/research.py JNJ
    python scripts/research.py ITSA4 --market br
    python scripts/research.py PRIO3 --md   # grava em reports/research_PRIO3_YYYY-MM-DD.md
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORTS = ROOT / "reports"


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        with sqlite3.connect(_db(mk)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


def _has_deep_fundamentals(ticker: str, market: str) -> bool:
    with sqlite3.connect(_db(market)) as c:
        r = c.execute(
            "SELECT COUNT(*) FROM deep_fundamentals "
            "WHERE ticker=? AND period_type='annual' AND total_assets IS NOT NULL",
            (ticker,),
        ).fetchone()
    return r[0] >= 2


def _ensure_deep_fundamentals(ticker: str, market: str) -> bool:
    """Se não há histórico, pulls via fetcher. Devolve True se agora há dados."""
    if _has_deep_fundamentals(ticker, market):
        return True
    from fetchers.yf_deep_fundamentals import fetch_and_persist
    n = fetch_and_persist(ticker, market)
    return n > 0 and _has_deep_fundamentals(ticker, market)


def _company_info(ticker: str, market: str) -> dict:
    with sqlite3.connect(_db(market)) as c:
        r = c.execute(
            "SELECT name, sector, is_holding, currency FROM companies WHERE ticker=?",
            (ticker,),
        ).fetchone()
        px_row = c.execute(
            "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        pos_row = c.execute(
            "SELECT quantity, entry_price FROM portfolio_positions "
            "WHERE ticker=? AND active=1 ORDER BY entry_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
    if not r:
        return {}
    name, sector, is_holding, ccy = r
    last_px, last_px_date = (px_row if px_row else (None, None))
    qty, entry_px = (pos_row if pos_row else (None, None))
    return {
        "ticker": ticker, "name": name, "sector": sector,
        "is_holding": bool(is_holding), "currency": ccy,
        "last_px": last_px, "last_px_date": last_px_date,
        "quantity": qty, "entry_price": entry_px,
        "mv": (qty * last_px) if qty and last_px else None,
        "cost": (qty * entry_px) if qty and entry_px else None,
    }


def _screen(ticker: str, market: str) -> tuple[float | None, bool, dict]:
    try:
        from scoring.engine import (
            load_snapshot, load_fii_snapshot,
            score_br, score_br_bank, score_br_fii,
            score_us, score_us_reit,
            _is_bank, _is_reit, _is_fii_ticker, _selic_real_bcb, aggregate,
        )
        is_fii = market == "br" and _is_fii_ticker(ticker)
        with sqlite3.connect(_db(market)) as conn:
            if is_fii:
                snap = load_fii_snapshot(conn, ticker)
                if not snap:
                    return None, False, {}
                details = score_br_fii(snap, selic_real=_selic_real_bcb(conn))
            else:
                snap = load_snapshot(conn, ticker)
                if not snap:
                    return None, False, {}
                if market == "br" and _is_bank(snap):
                    details = score_br_bank(snap)
                elif market == "us" and _is_reit(snap):
                    details = score_us_reit(snap)
                else:
                    details = (score_br if market == "br" else score_us)(snap)
        score, passes = aggregate(details)
        return score, passes, details
    except Exception as e:
        return None, False, {"error": str(e)}


def _safety(ticker: str, market: str) -> dict | None:
    try:
        from scoring.dividend_safety import compute as safety_compute
        s = safety_compute(ticker, market)
        if s is None:
            return None
        return {"total": s.total, "verdict": s.verdict, "components": getattr(s, "components", None)}
    except Exception:
        return None


def _dy_pctl(ticker: str, market: str) -> dict | None:
    try:
        from analytics.dy_percentile import compute as dy_compute
        with sqlite3.connect(_db(market)) as c:
            r = dy_compute(c, ticker)
        if not r:
            return None
        return {"dy_now_pct": r.dy_now_pct, "percentile": r.percentile,
                "obs": r.obs, "label": r.label}
    except Exception:
        return None


def _drip_base(ticker: str, market: str, last_px: float | None, sector: str | None) -> dict | None:
    if not last_px:
        return None
    try:
        from scripts.drip_projection import (
            _ttm_div_per_share, _annual_divs_per_share, _latest_fundamentals,
            derive_scenarios, project_drip,
        )
        as_of = date.today().isoformat()
        with sqlite3.connect(_db(market)) as conn:
            ttm = _ttm_div_per_share(conn, ticker, as_of)
            annual = _annual_divs_per_share(conn, ticker)
            fund = _latest_fundamentals(conn, ticker)
            scen = derive_scenarios(ticker, last_px, ttm, annual, fund, conn, sector)
        base = scen["base"]
        current_yield = ttm / last_px if last_px else 0
        tr_fwd = current_yield + base["g"] + base["md"]
        return {
            "ttm_div_ps": ttm,
            "current_yield": current_yield,
            "g_base": base["g"],
            "md_base": base["md"],
            "tr_fwd_base": tr_fwd,
            "kind": scen["debug"].get("kind"),
        }
    except Exception:
        return None


def _thesis(ticker: str, market: str) -> dict | None:
    try:
        from scripts.thesis_manager import get_full_context
        ctx = get_full_context(ticker, market)
        return ctx if ctx else None
    except Exception:
        return None


def _regime(market: str) -> dict | None:
    try:
        from analytics.regime import classify
        r = classify(market)
        return {"regime": r.regime, "confidence": r.confidence, "note": r.notes[0] if r.notes else ""}
    except Exception:
        return None


def _altman(ticker: str, market: str):
    from scoring.altman import compute as altman_compute
    return altman_compute(ticker, market)


def _piotroski(ticker: str, market: str):
    from scoring.piotroski import compute as piotroski_compute
    return piotroski_compute(ticker, market)


# --- verdict engine ---------------------------------------------------------

def _final_verdict(*, screen_score, screen_passes, altman, piotroski,
                   safety, dy_pctl, is_holding) -> tuple[str, list[str], int]:
    """Aplica regras determinísticas. Devolve (verdict, reasons, confidence_pct)."""
    reasons = []
    # vetos estruturais (hard floors)
    if altman.applicable and altman.is_distress:
        reasons.append(f"Altman Z={altman.z:.2f} < 1.81 (distress zone) → veto estrutural")
        return "AVOID", reasons, 85
    if piotroski.applicable and piotroski.is_weak:
        reasons.append(f"Piotroski F={piotroski.f_score}/9 ≤ 3 (quality degradada) → veto estrutural")
        return "AVOID", reasons, 80

    if screen_score is None:
        reasons.append("screen score indisponível — não há dados suficientes")
        return "WATCH", reasons, 30

    if screen_score < 0.4:
        reasons.append(f"screen score {screen_score:.2f} < 0.40 (insuficiente em ≥3 critérios)")
        return "AVOID", reasons, 70

    # quality composite para BUY
    qual_signals_strong = (
        screen_score >= 0.8 and
        (not altman.applicable or altman.is_safe) and
        (not piotroski.applicable or piotroski.f_score >= 5)
    )
    if qual_signals_strong:
        if safety and safety["total"] < 50:
            reasons.append(f"screen forte {screen_score:.2f} + Altman safe + F≥5, mas safety {safety['total']:.0f}/100 fraco")
            return "HOLD", reasons, 55
        reasons.append(f"screen {screen_score:.2f} + Altman/Piotroski confirmam qualidade")
        if dy_pctl and dy_pctl["label"] == "CHEAP":
            reasons.append(f"DY P{dy_pctl['percentile']:.0f} (CHEAP vs 10y) → entry timing favorável")
            conf = 80
        elif dy_pctl and dy_pctl["label"] == "EXPENSIVE":
            reasons.append(f"DY P{dy_pctl['percentile']:.0f} (EXPENSIVE vs 10y) → qualidade OK mas preço elevado")
            return "HOLD", reasons, 60
        else:
            conf = 70
        return "BUY", reasons, conf

    # zona cinzenta: passa-mas-não-brilha
    if screen_passes:
        reasons.append(f"screen passa ({screen_score:.2f}) mas sem confirmação forte em Altman/Piotroski/safety")
    else:
        reasons.append(f"screen quase ({screen_score:.2f}); 1+ critério em falta")
    return "HOLD", reasons, 50


# --- rendering --------------------------------------------------------------

def build_memo(ticker: str, market: str) -> str:
    out: list[str] = []
    P = out.append
    ci = _company_info(ticker, market)
    if not ci:
        return f"[erro] {ticker} não encontrado em {market}."
    sym = "R$" if ci["currency"] == "BRL" else "$"
    today = date.today().isoformat()

    # fetch on-demand
    has_deep = _ensure_deep_fundamentals(ticker, market)

    screen_score, screen_passes, screen_details = _screen(ticker, market)
    altman = _altman(ticker, market)
    piotroski = _piotroski(ticker, market)
    safety = _safety(ticker, market)
    dy_pctl = _dy_pctl(ticker, market)
    drip = _drip_base(ticker, market, ci["last_px"], ci["sector"])
    thesis = _thesis(ticker, market)
    regime = _regime(market)

    verdict, reasons, conf = _final_verdict(
        screen_score=screen_score, screen_passes=screen_passes,
        altman=altman, piotroski=piotroski, safety=safety,
        dy_pctl=dy_pctl, is_holding=ci["is_holding"],
    )

    P("=" * 78)
    P(f"  RESEARCH MEMO — {ticker}  ({ci['name']})")
    P(f"  Gerado: {today}   Mercado: {market.upper()}   Sector: {ci['sector'] or '-'}")
    P("=" * 78)

    # veredito upfront
    verdict_glyph = {"BUY": "✓ BUY", "HOLD": "◦ HOLD", "AVOID": "✗ AVOID", "WATCH": "? WATCH"}[verdict]
    P("")
    P(f"  VEREDITO: {verdict_glyph}   Confiança: {conf}%")
    for r in reasons:
        P(f"    • {r}")
    if ci["is_holding"]:
        P(f"    • POSIÇÃO ACTUAL: {ci['quantity']:.4f} shares @ {sym}{ci['entry_price']:.2f}  "
          f"MV {sym}{ci['mv']:,.0f}  P&L {sym}{(ci['mv']-ci['cost']):+,.0f} "
          f"({(ci['mv']/ci['cost']-1)*100:+.1f}%)")
    P("")

    # quadro financeiro
    P("[1] IDENTIFICAÇÃO & PREÇO")
    P("-" * 78)
    P(f"  Preço actual ............: {sym}{ci['last_px']:.2f}  ({ci['last_px_date']})")
    if drip:
        P(f"  DY t12m .................: {drip['current_yield']*100:.2f}%  "
          f"(div t12m {sym}{drip['ttm_div_ps']:.4f}/share)")
    if dy_pctl:
        P(f"  DY vs own 10y ...........: P{dy_pctl['percentile']:.0f}  [{dy_pctl['label']}]  "
          f"({dy_pctl['obs']} obs mensais) — entry-timing, NÃO stock-picker")

    # screen
    P("")
    P("[2] SCREEN VERDICT (Buffett/Graham sector-aware)")
    P("-" * 78)
    if screen_score is None:
        P("  Indisponível (ver 'error' em scoring.engine).")
    else:
        tag = "✓ PASSA" if screen_passes else ("≈ NEAR" if screen_score >= 0.6 else "✗ FAIL")
        P(f"  Score composto ..........: {screen_score:.2f}  →  {tag}")
        if isinstance(screen_details, dict):
            for k, v in screen_details.items():
                if not isinstance(v, dict):
                    continue
                val = v.get("value")
                thr = v.get("threshold")
                vd = v.get("verdict")
                if val is None:
                    continue
                vd_glyph = {"pass": "✓", "fail": "✗", "na": "·"}.get(vd, "?")
                # formato de valor depende do critério
                if isinstance(val, (int, float)):
                    val_s = f"{val:.3f}" if abs(val) < 10 else f"{val:.1f}"
                    thr_s = f"{thr}" if thr is not None else "-"
                else:
                    val_s = str(val)
                    thr_s = str(thr) if thr is not None else "-"
                P(f"    {vd_glyph}  {k:<22} {val_s:>10}  (threshold {thr_s})")

    # Altman + Piotroski
    P("")
    P("[3] QUALITY COMPOSITE (Altman + Piotroski)")
    P("-" * 78)
    if altman.applicable:
        z_tag = {"safe": "✓ SAFE", "grey": "◦ GREY", "distress": "✗ DISTRESS"}[altman.zone]
        P(f"  Altman Z-Score ..........: {altman.z:+.3f}  →  {z_tag}  (confiança {altman.confidence})")
        P(f"    X1 WC/TA={altman.x1:+.3f}  X2 RE/TA={altman.x2:+.3f}  X3 EBIT/TA={altman.x3:+.3f}  "
          f"X4 MC/TL={altman.x4:+.3f}  X5 Rev/TA={altman.x5:+.3f}")
    else:
        P(f"  Altman Z-Score ..........: N/A  ({altman.reason_if_not_applicable})")
    if piotroski.applicable:
        f_tag = {"STRONG": "✓ STRONG", "NEUTRAL": "◦ NEUTRAL", "WEAK": "✗ WEAK"}[piotroski.label]
        P(f"  Piotroski F-Score .......: {piotroski.f_score}/9  →  {f_tag}  "
          f"({piotroski.period_t} vs {piotroski.period_t_minus_1})")
        passed = [k for k, v in piotroski.criteria.items() if v]
        failed = [k for k, v in piotroski.criteria.items() if not v]
        P(f"    passou: {', '.join(passed) or '—'}")
        P(f"    falhou: {', '.join(failed) or '—'}")
    else:
        P(f"  Piotroski F-Score .......: N/A  ({piotroski.reason_if_not_applicable})")

    # safety
    P("")
    P("[4] DIVIDEND SAFETY")
    P("-" * 78)
    if safety:
        P(f"  Safety score ............: {safety['total']:.0f}/100  →  {safety['verdict']}")
    else:
        P("  Indisponível.")

    # DRIP forward
    P("")
    P("[5] DRIP FORWARD — cenário Base (apenas contexto, não forecast)")
    P("-" * 78)
    if drip:
        P(f"  g (div growth base) .....: {drip['g_base']*100:+.2f}%/y")
        P(f"  md (multiple drift) .....: {drip['md_base']*100:+.2f}%/y")
        P(f"  TR fwd base (DY+g+md) ...: {drip['tr_fwd_base']*100:+.2f}%/y")
        P(f"  kind ....................: {drip['kind']}")
    else:
        P("  Indisponível.")

    # thesis + regime context
    if thesis:
        P("")
        P("[6] TESE QUALITATIVA (thesis_manager)")
        P("-" * 78)
        tt = thesis.get("ticker")
        if tt:
            P(f"  Tese ticker: {tt.get('summary', '—')}")
            if tt.get("risks"):
                P(f"  Riscos:    {tt['risks'] if isinstance(tt['risks'], str) else ', '.join(tt['risks'])}")
            if tt.get("thesis_type"):
                P(f"  Tipo tese: {tt['thesis_type']}")
        st = thesis.get("sector")
        if st and st.get("summary"):
            P(f"  Sector:    {st['summary'][:120]}")
        mc = thesis.get("macros")
        if mc:
            # get_full_context devolve lista de dicts (cada um já resolvido)
            for m in mc:
                if not m:
                    continue
                key = m.get("key") or m.get("name") or "?"
                summ = m.get("summary")
                if summ:
                    P(f"  Macro [{key}]: {summ[:100]}")

    if regime:
        P("")
        P("[7] REGIME MACRO")
        P("-" * 78)
        P(f"  {market.upper()}: {regime['regime']} (conf {regime['confidence']}) — {regime['note']}")
        P(f"  NOTA: classifier é descritivo, não timing signal (ver Phase H null).")

    # closing
    P("")
    P("=" * 78)
    P(f"  Fontes: {'deep_fundamentals' if has_deep else 'deep_fundamentals PARCIAL'}, "
      f"scores, prices, dividends, series (FRED/BCB), thesis_book, dy_percentile")
    P(f"  Memo determinístico — sem LLM. Regras em scripts/research.py::_final_verdict.")
    P("=" * 78)

    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--md", action="store_true", help="Grava reports/research_TICKER_YYYY-MM-DD.md")
    args = ap.parse_args()

    ticker = args.ticker.upper()
    market = args.market or _detect_market(ticker)
    if not market:
        print(f"[erro] {ticker} não encontrado em nenhuma DB. Adiciona em config/universe.yaml.")
        return

    memo = build_memo(ticker, market)
    print(memo)

    if args.md:
        REPORTS.mkdir(exist_ok=True)
        fp = REPORTS / f"research_{ticker}_{date.today().isoformat()}.md"
        fp.write_text(f"# Research Memo — {ticker} {date.today().isoformat()}\n\n```\n{memo}\n```\n",
                      encoding="utf-8")
        print(f"\n[md] gravado em {fp}")


if __name__ == "__main__":
    main()
