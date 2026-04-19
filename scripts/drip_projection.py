"""Projecção DRIP forward — BR + US, usando portfolio_positions.

Lê a carteira real de ambas as DBs, deriva parâmetros de crescimento de
dividendo por ticker a partir dos dados já persistidos (TTM yield, CAGR
histórico, ROE × retenção quando disponível) e projecta o valor final
em 5/10/15 anos com 3 cenários (Conservador / Base / Optimista).

Não faz network — usa apenas DB local.

Uso:
    python scripts/drip_projection.py                # relatório consolidado
    python scripts/drip_projection.py --horizons 5,10,15,20
    python scripts/drip_projection.py --md           # grava markdown em reports/
    python scripts/drip_projection.py --only br      # só BR
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORTS = ROOT / "reports"


def _last_close(conn: sqlite3.Connection, ticker: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return r[0] if r else None


def _ttm_div_per_share(conn: sqlite3.Connection, ticker: str, as_of: str) -> float:
    cutoff = (date.fromisoformat(as_of) - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM dividends "
        "WHERE ticker=? AND ex_date>=? AND amount>0",
        (ticker, cutoff),
    ).fetchone()
    return r[0] or 0.0


def _annual_divs_per_share(conn: sqlite3.Connection, ticker: str) -> dict[int, float]:
    rows = conn.execute(
        "SELECT substr(ex_date,1,4), SUM(amount) FROM dividends "
        "WHERE ticker=? AND amount>0 GROUP BY 1 ORDER BY 1",
        (ticker,),
    ).fetchall()
    return {int(y): v for y, v in rows if y and y.isdigit()}


def _cagr(first: float, last: float, years: int) -> float | None:
    if first <= 0 or last <= 0 or years <= 0:
        return None
    return (last / first) ** (1 / years) - 1


def _latest_fundamentals(conn: sqlite3.Connection, ticker: str) -> dict:
    try:
        r = conn.execute(
            "SELECT eps, roe, dy, pe, pb, dividend_streak_years, is_aristocrat "
            "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
    except sqlite3.OperationalError:
        return {}
    if not r:
        return {}
    keys = ["eps", "roe", "dy", "pe", "pb", "streak", "aristocrat"]
    return dict(zip(keys, r))


FII_TICKER_SUFFIX = "11"
SELIC_CASH_TICKERS = {"LFTB11"}  # Tesouro Selic ETFs
SP_PROXY_TICKERS = {"IVVB11"}    # S&P 500 via ETF BRL


def _price_cagr(conn: sqlite3.Connection, ticker: str, years: int) -> float | None:
    rows = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date", (ticker,)
    ).fetchall()
    if len(rows) < 60:
        return None
    # pega primeiro ponto de ~N anos atrás e mais recente
    from datetime import datetime
    last_date = datetime.fromisoformat(rows[-1][0])
    target = last_date.replace(year=last_date.year - years)
    target_iso = target.isoformat()
    first = None
    for d, c in rows:
        if d >= target_iso:
            first = (d, c)
            break
    if not first:
        first = rows[0]
    last = rows[-1]
    yrs = (datetime.fromisoformat(last[0]) - datetime.fromisoformat(first[0])).days / 365.25
    return _cagr(first[1], last[1], max(yrs, 1))


def _classify(ticker: str, fund: dict, sector: str | None) -> str:
    """Devolve 'fii', 'selic_etf', 'sp_etf', 'compounder' (não-pagador),
    ou 'equity' (caso default)."""
    if ticker in SELIC_CASH_TICKERS:
        return "selic_etf"
    if ticker in SP_PROXY_TICKERS:
        return "sp_etf"
    if ticker.endswith(FII_TICKER_SUFFIX) and ticker not in SELIC_CASH_TICKERS | SP_PROXY_TICKERS:
        # todos os tickers com "11" no BR que não são ETF-RF ou ETF-US
        if (sector or "").startswith("ETF"):
            return "sp_etf" if "US" in sector else "selic_etf"
        return "fii"
    return "equity"


def derive_scenarios(ticker: str, last_price: float, ttm_div_ps: float,
                     annual_divs: dict[int, float], fund: dict,
                     conn: sqlite3.Connection, sector: str | None = None) -> dict:
    """3 cenários baseados no tipo de activo:
      - fii        : DY alto estável; g próximo de zero (papel) ou IPCA-link (tijolo)
      - selic_etf  : TR = SELIC (~14.75%/ano), proxy via price_growth
      - sp_etf     : TR = S&P long-term average (~10% USD, acresce FX)
      - compounder : não paga div; usa price CAGR histórico
      - equity     : Gordon + CAGR histórico do dividendo"""
    kind = _classify(ticker, fund, sector)
    debug = {"kind": kind, "streak": fund.get("streak")}

    if kind == "fii":
        # FII: distribuição ligada a IPCA (tijolo) ou CDI-IPCA (papel).
        # Hist 4y pode ser negativo em períodos pós-corte de juros ou defaults
        # de CRI — isso é *cíclico*, não estrutural. Forward-looking, o anchor
        # é IPCA (~3-4%). Blend 50/50 entre hist e IPCA proxy.
        years = sorted(annual_divs.keys())
        hist_g = None
        if len(years) >= 5:
            window = years[-4:]
            first, last = annual_divs[window[0]], annual_divs[window[-1]]
            hist_g = _cagr(first, last, len(window) - 1)
        ipca_anchor = 0.035  # IPCA 12m proxy (verifica em series se quiseres)
        if hist_g is not None:
            base_g = 0.5 * hist_g + 0.5 * ipca_anchor
        else:
            base_g = ipca_anchor
        base_g = max(0.0, min(base_g, 0.06))  # floor em 0 (sem decline real), cap 6%
        debug["hist_g"] = hist_g
        debug["ipca_anchor"] = ipca_anchor
        return {
            "conservador": {"g": max(0.0, base_g * 0.5),  "md": -0.01},
            "base":        {"g": base_g,                   "md": 0.0},
            "optimista":   {"g": min(0.08, base_g * 1.5), "md": 0.01},
            "debug": debug,
        }

    if kind == "selic_etf":
        # Tesouro Selic: TR ≈ SELIC meta. Procura em series, senão 14.75%.
        selic = conn.execute(
            "SELECT value FROM series WHERE series_id='SELIC_META' ORDER BY date DESC LIMIT 1"
        ).fetchone()
        selic_pct = (selic[0] / 100.0) if selic else 0.1475
        debug["selic_meta"] = selic_pct
        # Modela como price_growth puro (TR embutido no price)
        return {
            "conservador": {"g": 0.0, "md": selic_pct * 0.65},  # SELIC cai para ~10%
            "base":        {"g": 0.0, "md": selic_pct * 0.80},  # SELIC normaliza ~12%
            "optimista":   {"g": 0.0, "md": selic_pct},          # SELIC mantém
            "debug": debug,
        }

    if kind == "sp_etf":
        # S&P 500 via IVVB11: TR histórico 10% USD; FX drift ~3-5%/ano BRL
        return {
            "conservador": {"g": 0.0, "md": 0.06},   # S&P 7% USD, FX 0%
            "base":        {"g": 0.0, "md": 0.10},   # S&P 10% USD, FX flat
            "optimista":   {"g": 0.0, "md": 0.14},   # S&P 10% USD + FX +4%
            "debug": debug,
        }

    if kind == "compounder" or (ttm_div_ps == 0 and last_price > 0):
        # Não paga div. Usa price CAGR 5y como TR. Se sem história, assume 8%.
        pcagr = _price_cagr(conn, ticker, 5)
        base_md = pcagr if pcagr is not None else 0.08
        base_md = max(-0.05, min(base_md, 0.25))
        debug["price_cagr_5y"] = pcagr
        return {
            "conservador": {"g": 0.0, "md": base_md * 0.5},
            "base":        {"g": 0.0, "md": base_md},
            "optimista":   {"g": 0.0, "md": min(0.30, base_md * 1.3)},
            "debug": debug,
        }

    # --- equity com dividendo: Gordon + CAGR histórico ---
    years = sorted(annual_divs.keys())
    hist_g_5y = None
    if len(years) >= 6:
        window = years[-6:-1]
        first, last = annual_divs[window[0]], annual_divs[window[-1]]
        hist_g_5y = _cagr(first, last, 4)
    elif len(years) >= 3:
        first, last = annual_divs[years[0]], annual_divs[years[-1]]
        hist_g_5y = _cagr(first, last, len(years) - 1)

    gordon_g = None
    if fund.get("eps") and fund["eps"] > 0 and ttm_div_ps > 0 and fund.get("roe"):
        payout = min(max(ttm_div_ps / fund["eps"], 0.0), 1.0)
        gordon_g = fund["roe"] * (1 - payout)

    # Damper para hist "explosivo": quando o CAGR histórico do dividendo está
    # muito acima do Gordon sustentável, tipicamente reflecte um reset de
    # política de distribuição (one-off), não crescimento orgânico repetível.
    # Capamos ao max(2× gordon, 12%) quando ambos os sinais existem.
    hist_g_raw = hist_g_5y
    capped = False
    if hist_g_5y is not None and gordon_g is not None and gordon_g > 0:
        cap = max(2 * gordon_g, 0.12)
        if hist_g_5y > cap:
            hist_g_5y = cap
            capped = True

    signals = [g for g in (hist_g_5y, gordon_g) if g is not None and g > -0.5]
    base_g = median(signals) if signals else (ttm_div_ps / last_price if last_price else 0.04)
    base_g = max(-0.03, min(base_g, 0.18))

    is_quality = bool(fund.get("aristocrat")) or (fund.get("streak") or 0) >= 15
    debug.update({"hist_g_5y": hist_g_5y, "hist_g_raw": hist_g_raw,
                  "gordon_g": gordon_g, "is_quality": is_quality, "capped": capped})

    return {
        "conservador": {"g": max(-0.03, base_g * 0.6), "md": -0.01 if is_quality else -0.02},
        "base":        {"g": base_g,                    "md": 0.0},
        "optimista":   {"g": min(0.22, base_g * 1.35), "md": 0.01},
        "debug": debug,
    }


def project_drip(shares: float, price: float, div_ps: float,
                 g: float, md: float, years: int) -> tuple[float, float, float, float]:
    """Simulação ano-a-ano. Devolve (final_shares, final_price, total_divs, final_mv)."""
    sh, px, d = shares, price, div_ps
    total_divs = 0.0
    price_growth = g + md
    for _ in range(years):
        px *= (1 + price_growth)
        d *= (1 + g)
        gross = sh * d
        total_divs += gross
        if px > 0:
            sh += gross / px
    return sh, px, total_divs, sh * px


def payback_milestones(shares0: float, price0: float, div_ps0: float,
                       g: float, md: float, cost_basis: float,
                       max_years: int = 40) -> dict:
    """Calcula 3 marcos de payback para um cenário.

    - cash_payback_y   : anos até Σ cash_divs (sem reinvestir) ≥ cost_basis
    - share_double_y   : anos até shares (com DRIP) ≥ 2× shares iniciais
    - wealth_double_y  : anos até market value (com DRIP) ≥ 2× cost_basis
    """
    sh, px, d = shares0, price0, div_ps0
    cash_cum = 0.0
    marks: dict[str, int | None] = {
        "cash_payback_y": None,
        "share_double_y": None,
        "wealth_double_y": None,
    }
    price_growth = g + md
    for yr in range(1, max_years + 1):
        px *= (1 + price_growth)
        d *= (1 + g)
        cash_cum += shares0 * d          # cash path: só shares originais, sem reinvest
        if px > 0:
            sh += (sh * d) / px          # DRIP reinvest
        if marks["cash_payback_y"] is None and cash_cum >= cost_basis:
            marks["cash_payback_y"] = yr
        if marks["share_double_y"] is None and sh >= 2 * shares0:
            marks["share_double_y"] = yr
        if marks["wealth_double_y"] is None and sh * px >= 2 * cost_basis:
            marks["wealth_double_y"] = yr
        if all(marks.values()) and yr >= 5:
            break
    return marks


def analyze_market(db_path: Path, ccy: str, horizons: list[int], as_of: str) -> dict:
    conn = sqlite3.connect(db_path)
    positions = conn.execute(
        "SELECT ticker, quantity, entry_price FROM portfolio_positions "
        "WHERE active=1 AND quantity > 0 ORDER BY ticker"
    ).fetchall()

    per_ticker = []
    for ticker, qty, entry_px in positions:
        last_px = _last_close(conn, ticker)
        if not last_px:
            continue
        ttm_dps = _ttm_div_per_share(conn, ticker, as_of)
        annual = _annual_divs_per_share(conn, ticker)
        fund = _latest_fundamentals(conn, ticker)
        sector = conn.execute(
            "SELECT sector FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        sector = sector[0] if sector else None
        scenarios = derive_scenarios(ticker, last_px, ttm_dps, annual, fund, conn, sector)

        results = {}
        for sc_name in ("conservador", "base", "optimista"):
            sc = scenarios[sc_name]
            results[sc_name] = {
                h: project_drip(qty, last_px, ttm_dps, sc["g"], sc["md"], h)
                for h in horizons
            }

        per_ticker.append({
            "ticker": ticker, "qty": qty, "entry_price": entry_px,
            "last_price": last_px, "ttm_div_ps": ttm_dps,
            "mv_now": qty * last_px,
            "cost": qty * (entry_px or 0),
            "current_yield": ttm_dps / last_px if last_px else 0,
            "scenarios": scenarios,
            "results": results,
            "fund": fund,
        })
    conn.close()

    # agregados por horizonte × cenário
    total_mv_now = sum(p["mv_now"] for p in per_ticker)
    agg: dict = {}
    for h in horizons:
        agg[h] = {}
        for sc in ("conservador", "base", "optimista"):
            total_mv = sum(p["results"][sc][h][3] for p in per_ticker)
            total_divs = sum(p["results"][sc][h][2] for p in per_ticker)
            # valor shares iniciais em h anos (sem DRIP)
            total_orig = sum(
                p["qty"] * p["results"][sc][h][1] / max(1e-9, p["last_price"]) * p["last_price"] * 0
                + p["qty"] * p["results"][sc][h][1] / (p["last_price"] * (1 + p["scenarios"][sc]["g"] + p["scenarios"][sc]["md"]) ** h) * p["results"][sc][h][1]
                for p in per_ticker
            )
            # recalcular limpo: valor das shares iniciais = qty * final_price
            value_original = 0.0
            for p in per_ticker:
                final_px = p["results"][sc][h][1]
                value_original += p["qty"] * final_px
            value_drip = total_mv - value_original
            agg[h][sc] = {
                "mv": total_mv,
                "divs_bruto": total_divs,
                "value_original": value_original,
                "value_drip": value_drip,
                "cagr": (total_mv / total_mv_now) ** (1 / h) - 1 if total_mv_now else 0,
            }

    return {
        "ccy": ccy,
        "positions": per_ticker,
        "aggregate": agg,
        "total_mv_now": total_mv_now,
    }


def fmt_money(v: float, sym: str = "R$") -> str:
    return f"{sym} {v:>12,.2f}"


def print_report(markets: list[dict], horizons: list[int], fx_brl_usd: float) -> str:
    out = []
    P = out.append

    for m in markets:
        sym = "R$" if m["ccy"] == "BRL" else "US$"
        P(f"\n{'='*88}")
        P(f"CARTEIRA {m['ccy']} — MV actual {fmt_money(m['total_mv_now'], sym)}  ({len(m['positions'])} posições)")
        P(f"{'='*88}")

        # Assumptions por ticker
        P(f"\nAssumptions (kind = tipo de activo; g = div growth, md = price/multiple drift):")
        P(f"{'Ticker':<8}{'Kind':<10}{'MV':>14}{'DY':>8}{'g-base':>9}{'md-base':>10}{'TR-base':>9}")
        for p in m["positions"]:
            s = p["scenarios"]
            kind = s["debug"].get("kind", "?")
            gb = s["base"]["g"]; mb = s["base"]["md"]
            tr = p["current_yield"] + gb + mb
            P(f"{p['ticker']:<8}{kind:<10}{fmt_money(p['mv_now'], sym):>14}"
              f"{p['current_yield']*100:>7.2f}%"
              f"{gb*100:>+8.2f}%{mb*100:>+9.2f}%{tr*100:>+8.2f}%")

        # Aggregate por horizonte × cenário
        P(f"\nProjecção DRIP — valor de mercado final ({sym}):")
        P(f"{'Horizonte':<12}{'Conservador':>18}{'Base':>18}{'Optimista':>18}{'CAGR range':>18}")
        for h in horizons:
            a = m["aggregate"][h]
            cag_range = f"{a['conservador']['cagr']*100:.1f}% → {a['optimista']['cagr']*100:.1f}%"
            P(f"{h}y          "
              f"{sym} {a['conservador']['mv']:>14,.0f}"
              f"{sym} {a['base']['mv']:>14,.0f}"
              f"{sym} {a['optimista']['mv']:>14,.0f}"
              f"{cag_range:>18}")

        # Decomposição 15y/Base (ou último horizonte)
        h_final = horizons[-1]
        a_base = m["aggregate"][h_final]["base"]
        pct_drip = a_base["value_drip"] / a_base["mv"] * 100 if a_base["mv"] else 0
        P(f"\n{h_final}y / Base — decomposição:")
        P(f"  Patrimônio final           : {fmt_money(a_base['mv'], sym)}")
        P(f"  Das shares iniciais        : {fmt_money(a_base['value_original'], sym)}  ({100-pct_drip:.1f}%)")
        P(f"  Das shares compradas DRIP  : {fmt_money(a_base['value_drip'], sym)}  ({pct_drip:.1f}%)  ← efeito DRIP")
        P(f"  Dividendos brutos 15y      : {fmt_money(a_base['divs_bruto'], sym)}")

    # Consolidado global (converte US para BRL)
    br = next((m for m in markets if m["ccy"] == "BRL"), None)
    us = next((m for m in markets if m["ccy"] == "USD"), None)
    if br and us:
        P(f"\n{'='*88}")
        P(f"CONSOLIDADO GLOBAL (PTAX atual {fx_brl_usd:.4f}, assumida constante)")
        P(f"{'='*88}")
        mv_now_total = br["total_mv_now"] + us["total_mv_now"] * fx_brl_usd
        P(f"MV actual: R$ {mv_now_total:,.2f}  (BR R$ {br['total_mv_now']:,.0f} + US R$ {us['total_mv_now']*fx_brl_usd:,.0f})")
        P(f"\n{'Horizonte':<12}{'Conservador':>18}{'Base':>18}{'Optimista':>18}")
        for h in horizons:
            c = br["aggregate"][h]["conservador"]["mv"] + us["aggregate"][h]["conservador"]["mv"] * fx_brl_usd
            b = br["aggregate"][h]["base"]["mv"]       + us["aggregate"][h]["base"]["mv"] * fx_brl_usd
            o = br["aggregate"][h]["optimista"]["mv"]  + us["aggregate"][h]["optimista"]["mv"] * fx_brl_usd
            P(f"{h}y          R$ {c:>14,.0f}R$ {b:>14,.0f}R$ {o:>14,.0f}")

    return "\n".join(out)


def analyze_single_ticker(ticker: str, *, qty_override: float | None = None,
                          entry_override: float | None = None,
                          horizons: list[int] | None = None,
                          as_of: str | None = None) -> dict | None:
    """Retorna dict com tudo o que o single-ticker report precisa, ou None se não existir.

    Tenta ambas as DBs (BR primeiro, depois US). Se --qty/--entry são passados,
    sobrepõem a posição da carteira (útil para scenarios hipotéticos).
    """
    as_of = as_of or date.today().isoformat()
    horizons = horizons or [5, 10, 15]
    for db_path, ccy in [(DB_BR, "BRL"), (DB_US, "USD")]:
        conn = sqlite3.connect(db_path)
        last_px = _last_close(conn, ticker)
        if not last_px:
            conn.close()
            continue
        # qty/entry: override tem precedência; senão portfolio_positions; senão qty=0
        pos = conn.execute(
            "SELECT quantity, entry_price FROM portfolio_positions "
            "WHERE ticker=? AND active=1 ORDER BY entry_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        qty = qty_override if qty_override is not None else (pos[0] if pos else 0)
        entry_px = entry_override if entry_override is not None else (pos[1] if pos else last_px)

        ttm_dps = _ttm_div_per_share(conn, ticker, as_of)
        annual = _annual_divs_per_share(conn, ticker)
        fund = _latest_fundamentals(conn, ticker)
        sec_row = conn.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
        sector = sec_row[0] if sec_row else None
        scenarios = derive_scenarios(ticker, last_px, ttm_dps, annual, fund, conn, sector)
        conn.close()

        cost_basis = qty * entry_px if qty and entry_px else 0.0
        paybacks = {}
        trajectories = {}
        for sc_name in ("conservador", "base", "optimista"):
            sc = scenarios[sc_name]
            paybacks[sc_name] = payback_milestones(
                qty, last_px, ttm_dps, sc["g"], sc["md"], cost_basis
            ) if cost_basis > 0 else None
            trajectories[sc_name] = {
                h: project_drip(qty, last_px, ttm_dps, sc["g"], sc["md"], h)
                for h in horizons
            }
        return {
            "ticker": ticker, "ccy": ccy, "qty": qty, "entry_price": entry_px,
            "cost_basis": cost_basis, "last_price": last_px,
            "mv_now": qty * last_px, "ttm_div_ps": ttm_dps,
            "current_yield": ttm_dps / last_px if last_px else 0,
            "scenarios": scenarios, "paybacks": paybacks, "trajectories": trajectories,
            "horizons": horizons, "fund": fund,
        }
    return None


def print_single_ticker(data: dict, payback_mode: bool) -> str:
    sym = "R$" if data["ccy"] == "BRL" else "US$"
    out: list[str] = []
    P = out.append
    P("")
    P("/" + "=" * 76 + "\\")
    from analytics.format import br_date
    P(f"|   DRIP SCENARIO — {data['ticker']:<12}    moeda {data['ccy']}      data {br_date(date.today().isoformat())}".ljust(77) + "|")
    P("\\" + "=" * 76 + "/")
    P("")
    P("  POSICAO")
    P("  " + "-" * 60)
    P(f"  Shares..............: {data['qty']:>14,.0f}".replace(",", "."))
    P(f"  Entry price.........: {sym} {data['entry_price']:>11,.2f}")
    P(f"  Cost basis..........: {sym} {data['cost_basis']:>11,.2f}")
    P(f"  Price now...........: {sym} {data['last_price']:>11,.2f}")
    unrl = (data["last_price"]/data["entry_price"]-1)*100 if data["entry_price"] else 0
    P(f"  Market value now....: {sym} {data['mv_now']:>11,.2f}  [{unrl:+.1f}% nao-realizado]")
    P(f"  DY t12m.............: {data['current_yield']*100:.2f}%  (R$/US$ {data['ttm_div_ps']:.4f}/share)")
    P("")
    kind = data["scenarios"]["debug"].get("kind", "?")
    dbg = data["scenarios"]["debug"]
    P(f"  kind={kind}  "
      + "  ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}"
                  for k, v in dbg.items() if k != "kind" and v is not None))
    P("")

    P("  ASSUMPTIONS POR CENARIO")
    P("  " + "-" * 74)
    P("  | SCENARIO     |   g_div/y   |   md/y    |  TR (DY+g+md)  |")
    P("  " + "-" * 74)
    for sc_name in ("conservador", "base", "optimista"):
        sc = data["scenarios"][sc_name]
        tr = data["current_yield"] + sc["g"] + sc["md"]
        P(f"  | {sc_name:<12} |  {sc['g']*100:>+6.2f}%  |  {sc['md']*100:>+6.2f}% |  {tr*100:>+6.2f}%       |")
    P("  " + "-" * 74)
    P("")

    if payback_mode and data["cost_basis"] > 0:
        P("  PAYBACK MILESTONES (anos)")
        P("  " + "-" * 74)
        P("  | SCENARIO     | CASH payback | DRIP 2x shares | DRIP 2x wealth |")
        P("  " + "-" * 74)
        for sc_name in ("conservador", "base", "optimista"):
            pb = data["paybacks"][sc_name] or {}
            f = lambda k: str(pb.get(k) or ">40")
            P(f"  | {sc_name:<12} |   {f('cash_payback_y'):>4}       |     {f('share_double_y'):>4}       |     {f('wealth_double_y'):>4}       |")
        P("  " + "-" * 74)
        P("")
        P("  Cash payback    : sem reinvest, Sigma divs recebidos = cost_basis")
        P("  DRIP 2x shares  : com reinvest, shares_t >= 2 x shares_0")
        P("  DRIP 2x wealth  : com reinvest, value_t >= 2 x cost_basis")
        P("")

    P("  PROJECCAO DRIP — valor final de mercado por horizonte")
    P("  " + "-" * 74)
    hdr = "  | HORZ  | " + " | ".join(f"{sc:<12}" for sc in ("conservador","base","optimista")) + " |"
    P(hdr)
    P("  " + "-" * 74)
    for h in data["horizons"]:
        cells = []
        for sc_name in ("conservador", "base", "optimista"):
            _, _, _, mv = data["trajectories"][sc_name][h]
            cells.append(f"{sym} {mv:>10,.0f}")
        P(f"  | {h:>3}y  | " + " | ".join(cells) + " |")
    P("  " + "-" * 74)
    return "\n".join(out)


def _ptax() -> float:
    conn = sqlite3.connect(DB_BR)
    r = conn.execute(
        "SELECT value FROM series WHERE series_id='USDBRL_PTAX' ORDER BY date DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return r[0] if r else 5.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizons", default="5,10,15",
                    help="CSV de horizontes em anos, ex: 5,10,15,20")
    ap.add_argument("--md", action="store_true", help="Grava em reports/drip_projection_YYYY-MM-DD.md")
    ap.add_argument("--only", choices=["br", "us"], help="Só um mercado")
    ap.add_argument("--ticker", help="Modo single-ticker: foca só neste símbolo")
    ap.add_argument("--qty", type=float, help="Override de quantidade (só com --ticker)")
    ap.add_argument("--entry", type=float, help="Override de preço de entrada (só com --ticker)")
    ap.add_argument("--payback", action="store_true",
                    help="Com --ticker: mostra marcos de payback (cash/2xSH/2xV)")
    args = ap.parse_args()

    horizons = [int(x) for x in args.horizons.split(",")]
    as_of = date.today().isoformat()

    if args.ticker:
        data = analyze_single_ticker(
            args.ticker.upper(),
            qty_override=args.qty, entry_override=args.entry,
            horizons=horizons, as_of=as_of,
        )
        if not data:
            print(f"[erro] ticker '{args.ticker}' sem dados de preço em nenhuma DB.")
            return
        report = print_single_ticker(data, payback_mode=args.payback)
        print(report)
        if args.md:
            REPORTS.mkdir(exist_ok=True)
            fp = REPORTS / f"drip_{args.ticker.upper()}_{as_of}.md"
            fp.write_text(f"# DRIP — {args.ticker.upper()} {as_of}\n\n```\n{report}\n```\n", encoding="utf-8")
            print(f"\n[md] gravado em {fp}")
        return

    markets: list[dict] = []
    if args.only != "us":
        markets.append(analyze_market(DB_BR, "BRL", horizons, as_of))
    if args.only != "br":
        markets.append(analyze_market(DB_US, "USD", horizons, as_of))

    fx = _ptax()
    report = print_report(markets, horizons, fx)
    print(report)

    if args.md:
        REPORTS.mkdir(exist_ok=True)
        fp = REPORTS / f"drip_projection_{as_of}.md"
        fp.write_text(f"# DRIP Projection — {as_of}\n\n```\n{report}\n```\n", encoding="utf-8")
        print(f"\n[md] gravado em {fp}")


if __name__ == "__main__":
    main()
