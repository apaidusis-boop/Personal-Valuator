"""Portfolio report — briefing pessoal consolidado BR + US.

Sintetiza em < 1 segundo tudo o que o sistema sabe sobre a carteira real
que vive em portfolio_positions nas duas DBs:

  1. Snapshot financeiro consolidado (MV, P&L, alocação)
  2. Holdings com screen verdict + P&L unrealizado
  3. Eventos CVM/SEC dos últimos 7 dias tocando holdings
  4. Dividend calendar — pagamentos dos últimos 30d e esperados próximos
  5. DRIP forward 5/10/15y (Base, usa drip_projection.derive_scenarios)
  6. Watchlist near-miss (1 critério da aprovação)
  7. Macro context (Selic/IPCA/USD-BRL)
  8. Action items — síntese dos pontos anteriores

Uso:
    python scripts/portfolio_report.py          # stdout
    python scripts/portfolio_report.py --md     # grava em reports/
    python scripts/portfolio_report.py --days 14  # janela de eventos
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
REPORTS = ROOT / "reports"


def _get_ptax() -> float:
    with sqlite3.connect(DB_BR) as c:
        r = c.execute(
            "SELECT value FROM series WHERE series_id='USDBRL_PTAX' ORDER BY date DESC LIMIT 1"
        ).fetchone()
    return r[0] if r else 5.0


def _cash_balance(conn: sqlite3.Connection) -> tuple[float, list[tuple]]:
    """Devolve (total, lista de movimentações) da tabela cash_balance."""
    try:
        rows = conn.execute(
            "SELECT date, amount, currency, source, related_ticker, notes "
            "FROM cash_balance ORDER BY date DESC LIMIT 20"
        ).fetchall()
    except sqlite3.OperationalError:
        return 0.0, []
    total = sum(r[1] for r in rows)
    return total, rows


def _realized_pnl(conn: sqlite3.Connection) -> list[tuple]:
    """Posições fechadas: ticker, entry_price, exit_price, qty, realized_pnl, exit_date."""
    try:
        rows = conn.execute(
            "SELECT ticker, quantity, entry_price, exit_price, exit_date "
            "FROM portfolio_positions WHERE active=0 AND exit_price IS NOT NULL "
            "ORDER BY exit_date DESC"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    out = []
    for t, q, ep, xp, xd in rows:
        pnl = (xp - ep) * q
        pct = (xp / ep - 1) * 100 if ep else 0
        out.append((t, q, ep, xp, xd, pnl, pct))
    return out


def _fixed_income(conn: sqlite3.Connection) -> list[dict]:
    try:
        rows = conn.execute(
            "SELECT name, kind, indexador, spread_taxa, cdi_pct, maturity_date, "
            "       valor_atual, valor_aplicado, entry_date "
            "FROM fixed_income_positions ORDER BY valor_atual DESC"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    out = []
    for name, kind, idx, spread, cdi_pct, mat, atual, aplic, ent in rows:
        out.append({
            "name": name, "kind": kind, "indexador": idx,
            "spread": spread, "cdi_pct": cdi_pct,
            "maturity": mat, "entry_date": ent,
            "valor_atual": atual or 0, "valor_aplicado": aplic or 0,
            "pnl": (atual or 0) - (aplic or 0),
        })
    return out


def _holdings_with_mv(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT pp.ticker, pp.quantity, pp.entry_price,
               (SELECT close FROM prices p WHERE p.ticker=pp.ticker ORDER BY date DESC LIMIT 1) last_px,
               co.name, co.sector
        FROM portfolio_positions pp
        LEFT JOIN companies co ON co.ticker=pp.ticker
        WHERE pp.active=1 AND pp.quantity > 0
    """).fetchall()
    out = []
    for t, q, ep, lp, nm, sec in rows:
        q = q or 0; ep = ep or 0; lp = lp or ep
        mv = q * lp
        cost = q * ep
        out.append({
            "ticker": t, "name": nm or t, "sector": sec or "",
            "quantity": q, "cost": cost, "mv": mv,
            "last_px": lp, "entry_px": ep,
            "pnl": mv - cost, "pnl_pct": (mv/cost - 1)*100 if cost else 0,
        })
    return sorted(out, key=lambda x: -x["mv"])


def _screen_verdict(conn: sqlite3.Connection, ticker: str, market: str) -> tuple[float, bool, dict]:
    from scoring.engine import (
        load_snapshot, load_fii_snapshot,
        score_br, score_br_bank, score_br_fii,
        score_us, score_us_reit,
        _is_bank, _is_reit, _selic_real_bcb, aggregate, _is_fii_ticker,
    )
    has_fii = conn.execute(
        "SELECT 1 FROM fii_fundamentals WHERE ticker=? LIMIT 1", (ticker,)
    ).fetchone() is not None
    if market == "br" and _is_fii_ticker(ticker) and has_fii:
        snap = load_fii_snapshot(conn, ticker)
        if snap:
            details = score_br_fii(snap, selic_real=_selic_real_bcb(conn))
        else:
            return 0.0, False, {}
    else:
        snap = load_snapshot(conn, ticker)
        if snap is None:
            return 0.0, False, {}
        if market == "br" and _is_bank(snap):
            details = score_br_bank(snap)
        elif market == "us" and _is_reit(snap):
            details = score_us_reit(snap)
        else:
            details = (score_br if market == "br" else score_us)(snap)
    score, passes = aggregate(details)
    return score, passes, details


def _ttm_income(conn: sqlite3.Connection, ticker: str, qty: float) -> float:
    cutoff = (date.today() - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM dividends "
        "WHERE ticker=? AND ex_date>=? AND amount>0", (ticker, cutoff),
    ).fetchone()
    return (r[0] or 0) * qty


def _recent_events(conn: sqlite3.Connection, tickers: list[str], days: int) -> list[tuple]:
    if not tickers:
        return []
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    q = f"""SELECT event_date, ticker, source, kind, substr(summary,1,75)
            FROM events
            WHERE ticker IN ({','.join('?'*len(tickers))}) AND event_date >= ?
            ORDER BY event_date DESC"""
    return conn.execute(q, (*tickers, cutoff)).fetchall()


def _near_miss_watchlist(conn: sqlite3.Connection, market: str) -> list[tuple]:
    """Tickers não-holding onde o scoring mais recente tem score >= 0.6 e falha
    só 1 critério. Candidatos realistas a entrar no radar de entrada."""
    rows = conn.execute("""
        SELECT s.ticker, s.score, s.details_json, c.sector
        FROM scores s JOIN companies c ON c.ticker=s.ticker
        WHERE c.is_holding = 0
          AND s.run_date = (SELECT MAX(run_date) FROM scores WHERE ticker=s.ticker)
          AND s.score >= 0.60
        ORDER BY s.score DESC LIMIT 15
    """).fetchall()
    out = []
    import json
    for t, sc, js, sec in rows:
        try:
            d = json.loads(js or "{}")
        except json.JSONDecodeError:
            continue
        fails = [k for k, v in d.items() if v.get("verdict") == "fail"]
        if len(fails) == 1:
            out.append((t, sc, fails[0], sec))
    return out


def _upcoming_dividends(conn: sqlite3.Connection, tickers: list[str]) -> list[tuple]:
    """Pagamentos marcados nos próximos 45d a partir de events com kind='dividend'
    ou linhas em dividends com pay_date futura."""
    if not tickers:
        return []
    today = date.today().isoformat()
    future = (date.today() + timedelta(days=45)).isoformat()
    q = f"""SELECT ex_date, pay_date, ticker, amount
            FROM dividends
            WHERE ticker IN ({','.join('?'*len(tickers))})
              AND (pay_date BETWEEN ? AND ? OR (pay_date IS NULL AND ex_date BETWEEN ? AND ?))
            ORDER BY COALESCE(pay_date, ex_date)"""
    return conn.execute(q, (*tickers, today, future, today, future)).fetchall()


def _open_actions(conn: sqlite3.Connection, market: str) -> list[dict]:
    """Retorna todas as watchlist_actions com status='open'. Mais recentes primeiro."""
    import json as _json
    rows = conn.execute(
        """SELECT id, ticker, kind, trigger_id, action_hint, opened_at,
                  trigger_snapshot_json, notes
           FROM watchlist_actions WHERE status='open' ORDER BY opened_at DESC"""
    ).fetchall()
    out = []
    today = date.today().isoformat()
    for r in rows:
        snap = _json.loads(r[6]) if r[6] else {}
        out.append({
            "id": r[0], "ticker": r[1], "kind": r[2], "trigger_id": r[3],
            "action_hint": r[4] or "-", "opened_at": r[5],
            "is_today": (r[5] or "")[:10] == today,
            "snapshot": snap, "notes": r[7], "market": market,
        })
    return out


def _summarize_action_snapshot(kind: str, snap: dict) -> str:
    """Uma linha ultra-curta. Fallback para JSON dump se kind desconhecido."""
    if kind == "price_drop_from_high":
        return f"drop {snap.get('drop_pct','?')}% (price {snap.get('price','?')})"
    if kind == "dy_above_pct":
        return f"DY {snap.get('dy_pct','?')}% ≥ {snap.get('threshold_pct','?')}%"
    if kind == "dy_percentile_vs_own_history":
        return (f"DY {snap.get('dy_now_pct','?')}% ≥ P{snap.get('percentile','?')} "
                f"({snap.get('dy_threshold_pct','?')}%)")
    return "—"


def _drip_forward(conn, holding, horizons, sector):
    """Usa drip_projection.derive_scenarios para projectar um holding."""
    from scripts.drip_projection import (
        derive_scenarios, _annual_divs_per_share, _ttm_div_per_share,
        _latest_fundamentals, project_drip,
    )
    tk = holding["ticker"]
    px = holding["last_px"]
    ttm = _ttm_div_per_share(conn, tk, date.today().isoformat())
    annual = _annual_divs_per_share(conn, tk)
    fund = _latest_fundamentals(conn, tk)
    scen = derive_scenarios(tk, px, ttm, annual, fund, conn, sector)
    return {
        h: project_drip(holding["quantity"], px, ttm,
                        scen["base"]["g"], scen["base"]["md"], h)[3]
        for h in horizons
    }, scen


def build_report(days: int = 7) -> str:
    out: list[str] = []
    P = out.append
    today_iso = date.today().isoformat()
    ptax = _get_ptax()

    # === Conecta BR e US ===
    conn_br = sqlite3.connect(DB_BR)
    conn_us = sqlite3.connect(DB_US)

    h_br = _holdings_with_mv(conn_br)
    h_us = _holdings_with_mv(conn_us)
    fi_br = _fixed_income(conn_br)
    cash_br_total, cash_br_mvs = _cash_balance(conn_br)
    cash_us_total, cash_us_mvs = _cash_balance(conn_us)
    closed_br = _realized_pnl(conn_br)
    closed_us = _realized_pnl(conn_us)
    mv_br = sum(h["mv"] for h in h_br)
    mv_us = sum(h["mv"] for h in h_us)
    mv_fi = sum(f["valor_atual"] for f in fi_br)
    cost_br = sum(h["cost"] for h in h_br)
    cost_us = sum(h["cost"] for h in h_us)
    cost_fi = sum(f["valor_aplicado"] for f in fi_br)

    P("╔" + "═"*72 + "╗")
    P(f"║  PORTFOLIO BRIEFING  —  {today_iso}" + " " * 40 + "║")
    P("╚" + "═"*72 + "╝")

    # === 1. Snapshot consolidado ===
    P("\n[1] SNAPSHOT CONSOLIDADO")
    P(f"  BR equity    MV R$ {mv_br:>12,.2f}   P&L R$ {mv_br-cost_br:>+11,.2f} ({(mv_br/cost_br-1)*100 if cost_br else 0:+5.1f}%)   "
      f"{len(h_br):>2} holdings")
    P(f"  BR renda fx  MV R$ {mv_fi:>12,.2f}   P&L R$ {mv_fi-cost_fi:>+11,.2f} ({(mv_fi/cost_fi-1)*100 if cost_fi else 0:+5.1f}%)   "
      f"{len(fi_br):>2} títulos")
    P(f"  US equity    MV $  {mv_us:>12,.2f}   P&L $  {mv_us-cost_us:>+11,.2f} ({(mv_us/cost_us-1)*100 if cost_us else 0:+5.1f}%)   "
      f"{len(h_us):>2} holdings")
    if cash_br_total or cash_us_total:
        cash_lines = []
        if cash_br_total:
            cash_lines.append(f"R$ {cash_br_total:,.2f}")
        if cash_us_total:
            cash_lines.append(f"$ {cash_us_total:,.2f}")
        P(f"  CASH livre   {'  '.join(cash_lines)}  (realocar ou aguardar entrada)")
    cash_brl_equiv = cash_br_total + cash_us_total * ptax
    total_brl = mv_br + mv_fi + mv_us * ptax + cash_brl_equiv
    cost_total_brl = cost_br + cost_fi + cost_us * ptax
    P(f"  TOTAL        MV R$ {total_brl:>12,.2f} (PTAX {ptax:.4f})   P&L R$ {total_brl-cost_total_brl:>+11,.2f} "
      f"({(total_brl/cost_total_brl-1)*100:+5.1f}%)")
    P(f"  Allocation   BR-equity={mv_br/total_brl*100:.1f}%  BR-RF={mv_fi/total_brl*100:.1f}%  "
      f"US-equity={mv_us*ptax/total_brl*100:.1f}%")

    # === 2. Eventos recentes (holdings) ===
    tickers_br = [h["ticker"] for h in h_br]
    tickers_us = [h["ticker"] for h in h_us]
    ev_br = _recent_events(conn_br, tickers_br, days)
    ev_us = _recent_events(conn_us, tickers_us, days)
    if ev_br or ev_us:
        P(f"\n[2] EVENTOS holdings últimos {days}d  —  {len(ev_br)+len(ev_us)} filings")
        for d, t, src, kind, summ in (ev_br + ev_us)[:15]:
            P(f"  {d}  {t:<8} {src:<4} {kind:<20}  {summ or ''}")
    else:
        P(f"\n[2] EVENTOS — nada nos últimos {days}d a tocar holdings")

    # === 3. Holdings — screen + P&L ===
    for h_list, conn, label, sym in [(h_br, conn_br, "BR", "R$"), (h_us, conn_us, "US", "$")]:
        mk = "br" if label == "BR" else "us"
        P(f"\n[3.{label}] HOLDINGS  —  {len(h_list)} posições")
        P(f"  {'Ticker':<8}{'Screen':>8}{'MV':>14}{'P&L':>12}{'DY':>7}{'Streak':>7}  Sector")
        for h in h_list:
            score, passes, _ = _screen_verdict(conn, h["ticker"], mk)
            sym_v = "✓" if passes else ("≈" if score >= 0.6 else "✗")
            ttm_inc = _ttm_income(conn, h["ticker"], h["quantity"])
            dy_eff = ttm_inc / h["mv"] if h["mv"] else 0
            fund_row = conn.execute(
                "SELECT dividend_streak_years, is_aristocrat FROM fundamentals "
                "WHERE ticker=? ORDER BY period_end DESC LIMIT 1", (h["ticker"],)
            ).fetchone()
            streak, arist = (fund_row or (None, None))
            streak_tag = f"{streak}a" + ("★" if arist else "") if streak is not None else "-"
            P(f"  {h['ticker']:<8}{sym_v}{score:>6.2f}  {sym} {h['mv']:>10,.0f}"
              f"  {sym}{h['pnl']:>+9,.0f}{dy_eff*100:>6.2f}%{streak_tag:>7}  {h['sector']}")

    # === 4. Dividend calendar ===
    upc_br = _upcoming_dividends(conn_br, tickers_br)
    upc_us = _upcoming_dividends(conn_us, tickers_us)
    if upc_br or upc_us:
        P(f"\n[4] DIVIDEND CALENDAR — pagamentos próximos 45d")
        for ex, pay, t, amt in upc_br[:10]:
            P(f"  ex {ex}  pay {pay or '-':<10}  {t:<8}  R$ {amt:.4f}/share")
        for ex, pay, t, amt in upc_us[:10]:
            P(f"  ex {ex}  pay {pay or '-':<10}  {t:<8}  $ {amt:.4f}/share")
    else:
        P("\n[4] DIVIDEND CALENDAR — sem datas confirmadas nos próximos 45d")

    # === 5. DRIP projection consolidado (Base) ===
    P(f"\n[5] DRIP FORWARD — projecção Base, sem aportes (horizons 5/10/15y)")
    horizons = [5, 10, 15]
    tot_mv_h = {h: 0.0 for h in horizons}
    for holding in h_br:
        vals, _ = _drip_forward(conn_br, holding, horizons, holding["sector"])
        for h in horizons:
            tot_mv_h[h] += vals[h]
    tot_mv_us_h = {h: 0.0 for h in horizons}
    for holding in h_us:
        vals, _ = _drip_forward(conn_us, holding, horizons, holding["sector"])
        for h in horizons:
            tot_mv_us_h[h] += vals[h]

    P(f"  {'Horizonte':<10}{'BR (R$)':>18}{'US ($)':>16}{'Total BRL':>18}{'CAGR':>9}")
    for h in horizons:
        cons_total = tot_mv_h[h] + tot_mv_us_h[h] * ptax
        cagr = (cons_total / total_brl) ** (1/h) - 1 if total_brl else 0
        P(f"  {h}y       R$ {tot_mv_h[h]:>14,.0f}  $ {tot_mv_us_h[h]:>12,.0f}  "
          f"R$ {cons_total:>14,.0f}{cagr*100:>7.2f}%")

    # === 6. Near-miss watchlist ===
    nm_br = _near_miss_watchlist(conn_br, "br")
    nm_us = _near_miss_watchlist(conn_us, "us")
    if nm_br or nm_us:
        P(f"\n[6] WATCHLIST NEAR-MISS — 1 critério a faltar")
        for t, sc, fail, sec in nm_br[:8]:
            P(f"  BR  {t:<8}  score {sc:.2f}  falha: {fail:<22}  sector: {sec}")
        for t, sc, fail, sec in nm_us[:8]:
            P(f"  US  {t:<8}  score {sc:.2f}  falha: {fail:<22}  sector: {sec}")

    # === 7. Macro context ===
    macro = conn_br.execute("""
        SELECT series_id, date, value FROM series
        WHERE series_id IN ('SELIC_META', 'IPCA_MONTHLY', 'USDBRL_PTAX', 'CDI_DAILY')
        AND (series_id, date) IN (
            SELECT series_id, MAX(date) FROM series GROUP BY series_id
        )
        ORDER BY series_id
    """).fetchall()
    if macro:
        P(f"\n[7] MACRO")
        for sid, d, v in macro:
            label = {"SELIC_META": "Selic meta (a.a.)", "IPCA_MONTHLY": "IPCA mensal",
                     "USDBRL_PTAX": "PTAX USD/BRL", "CDI_DAILY": "CDI diário (fator)"}.get(sid, sid)
            fmt = f"{v:.2f}%" if sid == "SELIC_META" else (f"R$ {v:.4f}" if sid=="USDBRL_PTAX" else f"{v*100:.2f}%")
            P(f"  {label:<22}: {fmt:<10}  ({d})")

    # === Posições fechadas / P&L realizado ===
    all_closed = [(*r, "BR", "R$") for r in closed_br] + [(*r, "US", "$") for r in closed_us]
    if all_closed:
        P(f"\n[R] POSIÇÕES FECHADAS — P&L realizado  ({len(all_closed)} vendas)")
        P(f"  {'Data':<12}{'Ticker':<8}{'Qty':>8}{'Entry':>10}{'Exit':>10}{'Realized':>14}{'%':>7}")
        for t, q, ep, xp, xd, pnl, pct, mkt, sym in all_closed:
            P(f"  {xd:<12}{t:<8}{q:>8.2f}  {sym}{ep:>7.2f}  {sym}{xp:>7.2f}  {sym}{pnl:>+10,.2f}{pct:>+7.1f}%")
        P(f"\n  Cash flows recentes:")
        for d, amt, ccy, src, tk, nt in (cash_br_mvs + cash_us_mvs)[:10]:
            sym = "R$" if ccy == "BRL" else "$"
            P(f"    {d}  {sym} {amt:>+10,.2f}  {src:<16}  {tk or '':<8}  {(nt or '')[:55]}")

    # === 9. Renda Fixa detalhe ===
    if fi_br:
        P(f"\n[9] RENDA FIXA — {len(fi_br)} títulos  (MV R$ {mv_fi:,.0f})")
        P(f"  {'Nome':<32}{'Kind':<10}{'Taxa':<16}{'Venc':<12}{'Aplicado':>12}{'Atual':>12}")
        from datetime import date as _date
        today_d = _date.today()
        for f in fi_br:
            if f["spread"]:
                taxa = f"{f['indexador']}+{f['spread']*100:.2f}%"
            elif f["cdi_pct"]:
                taxa = f"{f['cdi_pct']*100:.1f}% CDI"
            else:
                taxa = f["indexador"] or "?"
            # anos até vencimento
            mat = f["maturity"]
            yrs_tag = ""
            if mat:
                try:
                    mat_d = _date.fromisoformat(mat)
                    yrs = (mat_d - today_d).days / 365.25
                    yrs_tag = f" ({yrs:.1f}y)"
                except ValueError:
                    pass
            P(f"  {f['name'][:31]:<32}{f['kind']:<10}{taxa:<16}{(mat or '-')+yrs_tag:<12}"
              f"R$ {f['valor_aplicado']:>8,.0f}R$ {f['valor_atual']:>8,.0f}")

    # === [T] Triggers/red-flags da tese activados ===
    try:
        from scripts.thesis_manager import check_trigger_activation, load_theses
        # thesis alerts usam janela maior (30d) porque triggers estruturais
        # tipicamente saem em filings mais esparsos que eventos diários
        alerts = check_trigger_activation(30)
        theses = load_theses()
        if alerts:
            P(f"\n[T] THESIS ALERTS — triggers/red-flags em eventos 30d ({len(alerts)})")
            for a in alerts[:10]:
                bullet = "⚠" if (a["flag_hits"] or a["is_critical"]) else "✓"
                hits = a["flag_hits"] or a["trigger_hits"]
                hit_tag = f" [{','.join(hits[:2])}]" if hits else (" [critical]" if a["is_critical"] else "")
                P(f"  {bullet} {a['market'].upper()} {a['ticker']:<7} {a['date']}  "
                  f"intent={a['thesis_intent']:<11}  {a['kind']}{hit_tag}")
                P(f"      {(a['summary'] or '')[:75]}")
    except Exception as e:
        P(f"\n[T] thesis_manager error: {str(e)[:100]}")

    # === 7b. Open watchlist actions (trigger-driven decision journal) ===
    actions_br = _open_actions(conn_br, "br")
    actions_us = _open_actions(conn_us, "us")
    all_actions = actions_br + actions_us
    if all_actions:
        new_today = sum(1 for a in all_actions if a["is_today"])
        tag = f" — {new_today} NOVO(S) HOJE" if new_today else ""
        P(f"\n[A] OPEN TRIGGERS / DECISION JOURNAL ({len(all_actions)}){tag}")
        for a in all_actions[:15]:
            age = (date.today() - date.fromisoformat((a["opened_at"] or "")[:10])).days
            age_s = "today" if age == 0 else f"{age}d ago"
            bullet = "🆕" if a["is_today"] else " •"
            detail = _summarize_action_snapshot(a["kind"], a["snapshot"])
            P(f"  {bullet} {a['market']}/{a['id']:<3} {a['ticker']:<7} "
              f"[{a['action_hint']:<6}] {detail:<44} {age_s}")
        P(f"  resolve: python scripts/action_cli.py resolve <ref> --note '...'")

    # === 8. Action items ===
    P(f"\n[8] ACTION ITEMS")
    # — eventos prioritários
    crit_ev = [(d, t, k, s) for d, t, s2, k, s in (ev_br + ev_us)
               if k == "8-K" and s and ("2.02" in s or "5.02" in s)]
    if crit_ev:
        P(f"  • {len(crit_ev)} filings 8-K críticos (earnings/executive changes) — revisar")
    # — underperformers
    down = [h for h in h_br+h_us if h["pnl_pct"] < -10]
    if down:
        P(f"  • Underperformers (< −10%): " + ", ".join(
            f"{h['ticker']} ({h['pnl_pct']:+.0f}%)" for h in down))
    # — near-miss candidates
    if nm_br or nm_us:
        P(f"  • {len(nm_br)+len(nm_us)} near-miss no screen (potencial promote a holding)")
    # — screens failing among holdings (distingue falha real vs tese deliberada vs sem dados)
    fails = []
    no_data = []
    try:
        from scripts.thesis_manager import load_theses as _lt
        _theses = _lt()
    except Exception:
        _theses = {"br": {}, "us": {}}

    for h_list, conn, mk in [(h_br, conn_br, "br"), (h_us, conn_us, "us")]:
        for h in h_list:
            # Skip tickers com intent non-DRIP (growth, turnaround, etc.)
            th = _theses.get(mk, {}).get(h["ticker"])
            if th and th.get("intent") in ("GROWTH", "TURNAROUND", "WIND_DOWN", "COMPOUNDER", "ETF"):
                continue
            sc, passes, details = _screen_verdict(conn, h["ticker"], mk)
            if not details:
                continue
            verdicts = [d["verdict"] for d in details.values()]
            applicable = [v for v in verdicts if v != "n/a"]
            if not applicable:
                no_data.append(h["ticker"])
            elif not passes and sc < 0.4 and len([v for v in applicable if v=="fail"]) >= 2:
                fails.append(f"{h['ticker']} ({sc:.2f})")
    if fails:
        P(f"  • Holdings DRIP com screen fraco (≥2 critérios fail, score<0.40): " + ", ".join(fails[:10]))
    if no_data:
        P(f"  • Holdings sem fundamentals (ETFs/novos): " + ", ".join(no_data[:10]))

    conn_br.close(); conn_us.close()
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="Janela de eventos (dias)")
    ap.add_argument("--md", action="store_true", help="Grava em reports/portfolio_briefing_YYYY-MM-DD.md")
    args = ap.parse_args()

    report = build_report(days=args.days)
    print(report)

    if args.md:
        REPORTS.mkdir(exist_ok=True)
        fp = REPORTS / f"portfolio_briefing_{date.today().isoformat()}.md"
        fp.write_text(f"# Portfolio Briefing — {date.today().isoformat()}\n\n```\n{report}\n```\n",
                      encoding="utf-8")
        print(f"\n[md] gravado em {fp}")


if __name__ == "__main__":
    main()
