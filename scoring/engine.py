"""Motor de scoring — nunca toca na rede.

Lê de data/br_investments.db (ou us_investments.db), aplica os critérios
do mercado correspondente e escreve em scores.

Cada critério devolve um veredicto de 3 estados:
    pass  — cumpre o threshold
    fail  — não cumpre
    n/a   — não aplicável ou dados em falta

passes_screen = True sse todos os critérios aplicáveis (!= n/a) são pass.
score         = nº de pass / nº de critérios aplicáveis (0.0–1.0).

Formato de scores.details_json (conforme HANDOFF §4.3):
    {
      "graham_number":   {"value": 13.2, "threshold": 14.83, "verdict": "fail"},
      "dividend_yield":  {"value": 0.0854, "threshold": 0.06, "verdict": "pass"},
      ...
    }

Uso:
    python scoring/engine.py              # scores ITSA4 (piloto)
    python scoring/engine.py PRIO3        # outro ticker BR
    python scoring/engine.py --market us  # modo US (quando houver dados)
"""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


# ---------- helpers de veredicto ----------

def _v(value, threshold, verdict: str, **extra) -> dict:
    d = {"value": value, "threshold": threshold, "verdict": verdict}
    d.update(extra)
    return d


def _na(threshold, reason: str, value=None) -> dict:
    return {"value": value, "threshold": threshold, "verdict": "n/a", "reason": reason}


# ---------- acesso a dados (só leitura) ----------

def load_snapshot(conn: sqlite3.Connection, ticker: str) -> dict | None:
    """Devolve o estado mais recente de um ticker: company + fundamentals + último preço."""
    co = conn.execute(
        "SELECT ticker, name, sector, is_holding, currency FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not co:
        return None

    # Tenta carregar campos REIT (só existem na DB US); cai em SELECT antigo para BR.
    try:
        fund = conn.execute(
            """SELECT period_end, eps, bvps, roe, pe, pb, dy,
                      net_debt_ebitda, dividend_streak_years, is_aristocrat,
                      ffo_per_share, interest_coverage, debt_to_assets
               FROM fundamentals WHERE ticker=?
               ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        has_reit_cols = True
    except sqlite3.OperationalError:
        fund = conn.execute(
            """SELECT period_end, eps, bvps, roe, pe, pb, dy,
                      net_debt_ebitda, dividend_streak_years, is_aristocrat
               FROM fundamentals WHERE ticker=?
               ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        has_reit_cols = False

    price = conn.execute(
        "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()

    fundamentals = None
    if fund:
        fundamentals = {
            "period_end": fund[0], "eps": fund[1], "bvps": fund[2], "roe": fund[3],
            "pe": fund[4], "pb": fund[5], "dy": fund[6],
            "net_debt_ebitda": fund[7], "dividend_streak_years": fund[8],
            "is_aristocrat": bool(fund[9]) if fund[9] is not None else None,
        }
        if has_reit_cols:
            fundamentals.update({
                "ffo_per_share": fund[10],
                "interest_coverage": fund[11],
                "debt_to_assets": fund[12],
            })

    return {
        "ticker": co[0],
        "name": co[1],
        "sector": co[2] or "",
        "is_in_portfolio": bool(co[3]),
        "currency": co[4],
        "fundamentals": fundamentals,
        "price": {"close": price[0], "date": price[1]} if price else None,
    }


# ---------- critérios BR ----------

def _is_holding_company(snap: dict) -> bool:
    """Itaúsa, Bradespar, etc. — sector == 'Holding' em universe.yaml."""
    return snap.get("sector", "").strip().lower() == "holding"


def _is_bank(snap: dict) -> bool:
    """Bancos comerciais — Graham Number e Dív/EBITDA não se aplicam
    (estrutura de capital e receita totalmente diferentes)."""
    return snap.get("sector", "").strip().lower() == "banks"


def _is_reit(snap: dict) -> bool:
    """REITs — GAAP deprecia imóveis de forma não-económica, distorcendo
    EPS/ROE. Usa-se FFO, P/FFO, AFFO payout, interest coverage em vez."""
    sector = snap.get("sector", "").strip().lower()
    return sector == "reit" or "reit" in sector


def score_br(snap: dict) -> dict:
    """Aplica os 5 critérios BR. Devolve details conforme HANDOFF §4.3."""
    f = snap.get("fundamentals") or {}
    p = snap.get("price") or {}
    price = p.get("close")
    eps = f.get("eps")
    bvps = f.get("bvps")

    # 1. Graham Number. Compara-se com o preço actual: passa se preço ≤ Graham.
    if eps is None or bvps is None or eps <= 0 or bvps <= 0:
        graham = _na(price, "EPS/BVPS em falta ou não positivos")
    elif price is None:
        graham = _na(None, "sem preço actual na DB")
    else:
        gn = math.sqrt(22.5 * eps * bvps)
        graham = _v(round(gn, 4), price, "pass" if price <= gn else "fail")

    # 2. DY ≥ 6%
    dy = f.get("dy")
    if dy is None:
        dividend_yield = _na(0.06, "DY em falta")
    else:
        dividend_yield = _v(dy, 0.06, "pass" if dy >= 0.06 else "fail")

    # 3. ROE ≥ 15%
    roe = f.get("roe")
    if roe is None:
        roe_v = _na(0.15, "ROE em falta")
    else:
        roe_v = _v(roe, 0.15, "pass" if roe >= 0.15 else "fail")

    # 4. Dív. líquida / EBITDA < 3. Para holdings o indicador é
    # conceptualmente estranho (EBITDA vem sobretudo de equiv. patrimonial),
    # por isso marca-se n/a — ver HANDOFF §3.
    nde = f.get("net_debt_ebitda")
    if _is_holding_company(snap):
        net_debt_ebitda = _na(3.0, "holding company (EBITDA de equivalência patrimonial)", value=nde)
    elif nde is None:
        net_debt_ebitda = _na(3.0, "Dív. líq/EBITDA em falta")
    else:
        net_debt_ebitda = _v(nde, 3.0, "pass" if nde < 3.0 else "fail")

    # 5. Dividend streak ≥ 5 anos
    streak = f.get("dividend_streak_years")
    if streak is None:
        dividend_streak = _na(5, "histórico de dividendos em falta")
    else:
        dividend_streak = _v(streak, 5, "pass" if streak >= 5 else "fail")

    return {
        "graham_number":   graham,
        "dividend_yield":  dividend_yield,
        "roe":             roe_v,
        "net_debt_ebitda": net_debt_ebitda,
        "dividend_streak": dividend_streak,
    }


# ---------- critérios BR banco ----------

def score_br_bank(snap: dict) -> dict:
    """Screen para bancos BR. Substitui Graham Number e Dív/EBITDA por
    P/E e P/B, e relaxa ROE para 12% (realidade pós-Selic alta)."""
    f = snap.get("fundamentals") or {}

    pe = f.get("pe")
    pe_v = _na(10, "P/E em falta") if pe is None else _v(pe, 10, "pass" if pe <= 10 else "fail")

    pb = f.get("pb")
    pb_v = _na(1.5, "P/B em falta") if pb is None else _v(pb, 1.5, "pass" if pb <= 1.5 else "fail")

    dy = f.get("dy")
    dy_v = _na(0.06, "DY em falta") if dy is None else _v(dy, 0.06, "pass" if dy >= 0.06 else "fail")

    roe = f.get("roe")
    roe_v = _na(0.12, "ROE em falta") if roe is None else _v(roe, 0.12, "pass" if roe >= 0.12 else "fail")

    streak = f.get("dividend_streak_years")
    streak_v = _na(5, "histórico de dividendos em falta") if streak is None else _v(streak, 5, "pass" if streak >= 5 else "fail")

    return {
        "pe":               pe_v,
        "price_to_book":    pb_v,
        "dividend_yield":   dy_v,
        "roe":              roe_v,
        "dividend_streak":  streak_v,
    }


# ---------- critérios BR FII ----------

def load_fii_snapshot(conn: sqlite3.Connection, ticker: str) -> dict | None:
    co = conn.execute(
        "SELECT ticker, name, sector, is_holding, currency FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not co:
        return None
    fund = conn.execute(
        """SELECT period_end, price, vpa, pvp, dy_12m,
                  avg_monthly_rendimento_24m, physical_vacancy,
                  distribution_streak_months, adtv_daily, segment_anbima
           FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    return {
        "ticker": co[0], "name": co[1], "segment": co[2],
        "is_in_portfolio": bool(co[3]),
        "fundamentals": {
            "period_end": fund[0], "price": fund[1], "vpa": fund[2],
            "pvp": fund[3], "dy_12m": fund[4],
            "avg_monthly_rendimento_24m": fund[5],
            "physical_vacancy": fund[6],
            "distribution_streak_months": fund[7],
            "adtv_daily": fund[8],
            "segment_anbima": fund[9],
        } if fund else None,
    }


def _selic_real_bcb(conn: sqlite3.Connection) -> float | None:
    """SELIC real = SELIC meta anualizada − IPCA 12m acumulado.
    Proxy para NTN-B (Baroni/Suno usam este indicador em análises de FII).
    Retorna em fracção (ex: 0.085 = 8,5%)."""
    selic = conn.execute(
        "SELECT value FROM series WHERE series_id='SELIC_META' ORDER BY date DESC LIMIT 1"
    ).fetchone()
    if not selic:
        return None
    selic_nominal = selic[0] / 100.0 if selic[0] > 1 else selic[0]

    # IPCA 12m: produto composto dos últimos 12 valores mensais
    ipca = conn.execute(
        "SELECT value FROM series WHERE series_id='IPCA_MONTHLY' ORDER BY date DESC LIMIT 12"
    ).fetchall()
    if len(ipca) < 12:
        return None
    factor = 1.0
    for (v,) in ipca:
        factor *= (1 + v)
    ipca_12m = factor - 1
    return selic_nominal - ipca_12m


def _is_papel_fii(segment_anbima: str | None) -> bool:
    if not segment_anbima:
        return False
    s = segment_anbima.lower()
    return any(k in s for k in ("títulos", "cri", "papel", "papéis", "papeis"))


def score_br_fii(snap: dict, selic_real: float | None = None) -> dict:
    """Screen para FIIs BR. 6 critérios.
    Papel (CRI) isenta vacância física como n/a.
    Critério 6 usa SELIC real (proxy de NTN-B) vindo do caller."""
    f = snap.get("fundamentals") or {}
    is_papel = _is_papel_fii(f.get("segment_anbima"))

    # 1. DY 12m ≥ 8%
    dy = f.get("dy_12m")
    dy_v = _na(0.08, "DY 12m em falta") if dy is None else _v(dy, 0.08, "pass" if dy >= 0.08 else "fail")

    # 2. P/VP ≤ 1,05
    pvp = f.get("pvp")
    pvp_v = _na(1.05, "P/VP em falta") if pvp is None else _v(pvp, 1.05, "pass" if pvp <= 1.05 else "fail")

    # 3. Vacância física < 15% (só tijolo)
    if is_papel:
        vacancy_v = _na(0.15, "FII de papel — vacância não aplicável")
    else:
        vac = f.get("physical_vacancy")
        vacancy_v = _na(0.15, "vacância física em falta") if vac is None else _v(vac, 0.15, "pass" if vac < 0.15 else "fail")

    # 4. Streak de distribuição ≥ 12 meses
    streak = f.get("distribution_streak_months")
    streak_v = _na(12, "histórico de distribuição em falta") if streak is None else _v(streak, 12, "pass" if streak >= 12 else "fail")

    # 5. Liquidez diária > R$ 500k
    adtv = f.get("adtv_daily")
    adtv_v = _na(500_000, "liquidez em falta") if adtv is None else _v(adtv, 500_000, "pass" if adtv > 500_000 else "fail")

    # 6. Spread DY sobre SELIC real ≥ 0 (FII pelo menos bate risk-free real)
    # Proxy de NTN-B 10y: ideal seria NTN-B (benchmark Baroni com 3% spread),
    # mas sem fetcher Tesouro Direto usamos SELIC - IPCA 12m. Como Selic nominal
    # costuma ser > NTN-B 10y em curva invertida, o threshold é relaxado (0%).
    if selic_real is None or dy is None:
        spread_v = _na(0.0, "SELIC real ou DY em falta")
    else:
        spread = dy - selic_real
        spread_v = _v(round(spread, 4), 0.0, "pass" if spread >= 0.0 else "fail",
                      dy=dy, selic_real=round(selic_real, 4),
                      proxy="SELIC-IPCA (NTN-B mais fiel na Fase 2)")

    return {
        "dividend_yield":      dy_v,
        "price_to_book":       pvp_v,
        "vacancy":             vacancy_v,
        "distribution_streak": streak_v,
        "liquidity":           adtv_v,
        "spread_selic_real":   spread_v,
    }


# ---------- critérios US REIT ----------

def score_us_reit(snap: dict) -> dict:
    """Screen para REITs US. Substitui P/E/ROE (distorcidos por GAAP) por
    P/FFO e interest coverage. P/B como proxy de P/NAV."""
    f = snap.get("fundamentals") or {}
    p = snap.get("price") or {}
    price = p.get("close")

    dy = f.get("dy")
    dy_v = _na(0.03, "DY em falta") if dy is None else _v(dy, 0.03, "pass" if dy >= 0.03 else "fail")

    streak = f.get("dividend_streak_years")
    arist = f.get("is_aristocrat")
    if arist:
        streak_v = _v(True, 10, "pass", kind="aristocrat")
    elif streak is None:
        streak_v = _na(10, "streak em falta")
    else:
        streak_v = _v(streak, 10, "pass" if streak >= 10 else "fail", kind="streak")

    pb = f.get("pb")
    pb_v = _na(1.5, "P/B (proxy NAV) em falta") if pb is None else _v(pb, 1.5, "pass" if pb <= 1.5 else "fail")

    nde = f.get("net_debt_ebitda")
    nde_v = _na(6.0, "Net Debt/EBITDA em falta") if nde is None else _v(nde, 6.0, "pass" if nde <= 6.0 else "fail")

    ffo = f.get("ffo_per_share")
    if ffo is None or price is None or ffo <= 0:
        p_ffo_v = _na(18, "FFO/share ou preço em falta ou FFO≤0")
    else:
        p_ffo = price / ffo
        p_ffo_v = _v(round(p_ffo, 2), 18, "pass" if p_ffo <= 18 else "fail",
                     ffo_per_share=round(ffo, 2))

    ic = f.get("interest_coverage")
    ic_v = _na(2.5, "interest coverage em falta") if ic is None else _v(ic, 2.5, "pass" if ic >= 2.5 else "fail")

    return {
        "dividend_yield":    dy_v,
        "dividend_streak":   streak_v,
        "price_to_book":     pb_v,
        "net_debt_ebitda":   nde_v,
        "p_ffo":             p_ffo_v,
        "interest_coverage": ic_v,
    }


# ---------- critérios US ----------

def score_us(snap: dict) -> dict:
    f = snap.get("fundamentals") or {}

    pe = f.get("pe")
    pe_v = _na(20, "P/E em falta") if pe is None else _v(pe, 20, "pass" if pe <= 20 else "fail")

    pb = f.get("pb")
    pb_v = _na(3, "P/B em falta") if pb is None else _v(pb, 3, "pass" if pb <= 3 else "fail")

    dy = f.get("dy")
    dy_v = _na(0.025, "DY em falta") if dy is None else _v(dy, 0.025, "pass" if dy >= 0.025 else "fail")

    roe = f.get("roe")
    roe_v = _na(0.15, "ROE em falta") if roe is None else _v(roe, 0.15, "pass" if roe >= 0.15 else "fail")

    # Aristocrat OU ≥ 10 anos consecutivos
    arist = f.get("is_aristocrat")
    streak = f.get("dividend_streak_years")
    if arist is None and streak is None:
        aristocrat = _na(10, "histórico de dividendos em falta")
    elif arist:
        aristocrat = _v(True, 10, "pass", kind="aristocrat")
    elif streak is not None:
        aristocrat = _v(streak, 10, "pass" if streak >= 10 else "fail", kind="streak")
    else:
        aristocrat = _v(False, 10, "fail", kind="aristocrat")

    return {
        "pe": pe_v,
        "pb": pb_v,
        "dividend_yield": dy_v,
        "roe": roe_v,
        "aristocrat": aristocrat,
    }


# ---------- agregação ----------

def aggregate(details: dict) -> tuple[float, bool]:
    verdicts = [c["verdict"] for c in details.values()]
    applicable = [v for v in verdicts if v != "n/a"]
    if not applicable:
        return 0.0, False
    passes = sum(1 for v in applicable if v == "pass")
    score = passes / len(applicable)
    passes_screen = all(v == "pass" for v in applicable)
    return round(score, 4), passes_screen


# ---------- persistência ----------

def persist_score(conn: sqlite3.Connection, ticker: str, score: float,
                  passes_screen: bool, details: dict) -> str:
    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO scores (ticker, run_date, score, passes_screen, details_json)
           VALUES (?,?,?,?,?)
           ON CONFLICT(ticker, run_date) DO UPDATE SET
             score=excluded.score,
             passes_screen=excluded.passes_screen,
             details_json=excluded.details_json""",
        (ticker, run_date, score, 1 if passes_screen else 0, json.dumps(details, ensure_ascii=False)),
    )
    return run_date


# ---------- CLI ----------

def _is_fii_ticker(ticker: str) -> bool:
    return ticker.endswith("11") and not ticker.startswith("^")


def run(ticker: str, market: str) -> dict[str, Any]:
    db = DB_BR if market == "br" else DB_US
    is_fii = market == "br" and _is_fii_ticker(ticker)
    with sqlite3.connect(db) as conn:
        if is_fii:
            snap = load_fii_snapshot(conn, ticker)
            if snap is None:
                raise SystemExit(f"{ticker} não encontrado em {db.name}")
            selic_real = _selic_real_bcb(conn)
            details = score_br_fii(snap, selic_real=selic_real)
        else:
            snap = load_snapshot(conn, ticker)
            if snap is None:
                raise SystemExit(f"{ticker} não encontrado em {db.name}")
            if market == "br" and _is_bank(snap):
                details = score_br_bank(snap)
            elif market == "us" and _is_reit(snap):
                details = score_us_reit(snap)
            else:
                details = (score_br if market == "br" else score_us)(snap)
        score, passes = aggregate(details)
        run_date = persist_score(conn, ticker, score, passes, details)
        conn.commit()

    result = {
        "ticker": ticker,
        "market": market,
        "run_date": run_date,
        "score": score,
        "passes_screen": passes,
        "details": details,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    args = ap.parse_args()
    run(args.ticker, args.market)


if __name__ == "__main__":
    main()
