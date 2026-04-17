"""Thesis Manager — CRUD e surfacing de teses por ticker.

Orquestra o config/theses.yaml e deixa o sistema responder a "qual é a
tese deste ticker?", "que teses precisam de review?", "que triggers
foram activados?". Serve de integração entre:

  - dados quantitativos (prices, dividends, events, fundamentals)
  - contexto qualitativo (thesis statements, triggers, red_flags)
  - surfacing em relatórios (portfolio_report, analyze_ticker)

Uso:
    python scripts/thesis_manager.py                 # lista todas as teses
    python scripts/thesis_manager.py ITSA4           # detalhe de um ticker
    python scripts/thesis_manager.py --review        # teses que precisam review
    python scripts/thesis_manager.py --triggers      # triggers activados em eventos recentes
    python scripts/thesis_manager.py --no-thesis     # holdings sem tese
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
THESES_FILE = ROOT / "config" / "theses.yaml"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def load_theses() -> dict:
    if not THESES_FILE.exists():
        return {"br": {}, "us": {}}
    return yaml.safe_load(THESES_FILE.read_text(encoding="utf-8")) or {"br": {}, "us": {}}


def save_theses(data: dict) -> None:
    THESES_FILE.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )


def get_thesis(ticker: str, market: str | None = None) -> dict | None:
    data = load_theses()
    if market:
        return data.get(market, {}).get(ticker)
    for mk in ("br", "us"):
        if ticker in data.get(mk, {}):
            return data[mk][ticker]
    return None


def get_sector(sector_key: str) -> dict | None:
    data = load_theses()
    return (data.get("sectors") or {}).get(sector_key)


def get_macro(macro_key: str) -> dict | None:
    data = load_theses()
    return (data.get("macro_themes") or {}).get(macro_key)


def get_full_context(ticker: str, market: str | None = None) -> dict:
    """Devolve tese completa de um ticker: ticker + sector + macros (herança)."""
    th = get_thesis(ticker, market)
    if not th:
        return {}
    out = {"ticker": th}
    if th.get("sector"):
        out["sector"] = get_sector(th["sector"])
    if th.get("macro"):
        out["macros"] = [get_macro(m) for m in th["macro"] if get_macro(m)]
    return out


def find_by_sector(sector_key: str) -> list[tuple[str, str, dict]]:
    """Devolve todos os tickers em uma tese sectorial. (market, ticker, thesis)"""
    data = load_theses()
    out = []
    for mk in ("br", "us"):
        for t, th in (data.get(mk, {}) or {}).items():
            if th.get("sector") == sector_key:
                out.append((mk, t, th))
    return out


def find_by_macro(macro_key: str) -> dict[str, list[tuple[str, str]]]:
    """Devolve tickers afectados por um tema macro. Divide por affects_positive/negative
    olhando directamente no macro_theme + via ticker.macro field."""
    data = load_theses()
    macro = (data.get("macro_themes") or {}).get(macro_key) or {}
    out = {"positive": [], "negative": [], "mentioned": []}

    # do ponto de vista do macro (affects_positive/negative fields)
    for t in macro.get("affects_positive", []):
        mk = "br" if t in (data.get("br", {}) or {}) else "us"
        out["positive"].append((mk, t))
    for t in macro.get("affects_negative", []):
        mk = "br" if t in (data.get("br", {}) or {}) else "us"
        out["negative"].append((mk, t))

    # do ponto de vista dos tickers (macro: [...] field)
    for mk in ("br", "us"):
        for t, th in (data.get(mk, {}) or {}).items():
            if macro_key in (th.get("macro") or []):
                out["mentioned"].append((mk, t))
    return out


def list_holdings_by_market() -> dict[str, list[str]]:
    out = {"br": [], "us": []}
    for db, mk in [(DB_BR, "br"), (DB_US, "us")]:
        with sqlite3.connect(db) as c:
            rows = c.execute(
                "SELECT ticker FROM portfolio_positions WHERE active=1 AND quantity>0"
            ).fetchall()
            out[mk] = [r[0] for r in rows]
    return out


def find_missing_theses() -> list[tuple[str, str]]:
    """Holdings reais que não têm tese em theses.yaml."""
    theses = load_theses()
    holdings = list_holdings_by_market()
    missing = []
    for mk, tickers in holdings.items():
        for t in tickers:
            if t not in theses.get(mk, {}):
                missing.append((mk, t))
    return missing


def theses_needing_review(days_threshold: int = 90) -> list[tuple[str, str, dict]]:
    """Teses cuja last_review é mais antiga que N dias."""
    theses = load_theses()
    cutoff = date.today() - timedelta(days=days_threshold)
    out = []
    for mk in ("br", "us"):
        for t, thesis in (theses.get(mk, {}) or {}).items():
            last = thesis.get("last_review")
            if last is None:
                out.append((mk, t, thesis))
                continue
            try:
                last_d = last if isinstance(last, date) else date.fromisoformat(str(last))
                if last_d < cutoff:
                    out.append((mk, t, thesis))
            except ValueError:
                out.append((mk, t, thesis))
    return out


def check_trigger_activation(days_lookback: int = 30) -> list[dict]:
    """Percorre todas as teses e verifica se algum trigger/red_flag foi
    materializado por um evento recente (CVM/SEC filings, dividend cuts,
    big price moves).

    Versão 1 — simple keyword match nos summaries de events + sinais de
    dividend history. Evolui na fase News/RI.
    """
    theses = load_theses()
    alerts = []
    since = (date.today() - timedelta(days=days_lookback)).isoformat()

    for mk, db in [("br", DB_BR), ("us", DB_US)]:
        with sqlite3.connect(db) as c:
            for t, th in (theses.get(mk, {}) or {}).items():
                # eventos recentes do ticker
                events = c.execute(
                    """SELECT event_date, kind, summary FROM events
                       WHERE ticker=? AND event_date>=?
                       ORDER BY event_date DESC""",
                    (t, since),
                ).fetchall()
                if not events:
                    continue

                # keywords derivadas dos triggers/red_flags
                trigger_kw = []
                for tr in (th.get("triggers") or []):
                    trigger_kw.extend([w.lower() for w in tr.split() if len(w) > 4])
                flag_kw = []
                for rf in (th.get("red_flags") or []):
                    flag_kw.extend([w.lower() for w in rf.split() if len(w) > 4])

                for d, kind, summ in events:
                    s = (summ or "").lower()
                    matched_trigger = [kw for kw in trigger_kw if kw in s]
                    matched_flag = [kw for kw in flag_kw if kw in s]
                    # Alerta automático para items estruturais
                    is_critical = (
                        kind == "8-K" and any(it in (summ or "")
                                              for it in ("5.02", "3.01", "1.01", "2.01"))
                    )
                    if matched_trigger or matched_flag or is_critical:
                        alerts.append({
                            "market": mk,
                            "ticker": t,
                            "date": d,
                            "kind": kind,
                            "summary": summ,
                            "trigger_hits": matched_trigger,
                            "flag_hits": matched_flag,
                            "is_critical": is_critical,
                            "thesis_intent": th.get("intent"),
                        })
    return alerts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", help="Detalhe de um ticker")
    ap.add_argument("--review", action="store_true",
                    help="Teses que precisam review (>90d)")
    ap.add_argument("--review-days", type=int, default=90)
    ap.add_argument("--triggers", action="store_true",
                    help="Triggers activados em eventos recentes")
    ap.add_argument("--trigger-days", type=int, default=30)
    ap.add_argument("--no-thesis", action="store_true",
                    help="Holdings sem tese documentada")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--sector", metavar="KEY",
                    help="Mostra tese sectorial e tickers afectados (ex: br.fii_papel)")
    ap.add_argument("--macro", metavar="KEY",
                    help="Mostra tema macro e tickers afectados (ex: selic_alta_br)")
    ap.add_argument("--sectors-list", action="store_true",
                    help="Lista todos os sectors e macro themes")
    args = ap.parse_args()

    if args.sectors_list:
        data = load_theses()
        print(f"\n### MACRO THEMES ({len(data.get('macro_themes', {}))})")
        for k, m in (data.get("macro_themes") or {}).items():
            n_pos = len(m.get("affects_positive", []))
            n_neg = len(m.get("affects_negative", []))
            print(f"  {k:<28} {m.get('name','')[:50]}  (+{n_pos}/-{n_neg})")
        print(f"\n### SECTORS ({len(data.get('sectors', {}))})")
        for k, s in (data.get("sectors") or {}).items():
            print(f"  {k:<28} {s.get('name','')[:40]:<40}  tickers: {', '.join(s.get('tickers', []))}")
        return

    if args.sector:
        s = get_sector(args.sector)
        if not s:
            print(f"Sector {args.sector!r} não existe. Lista com --sectors-list")
            return
        print(f"\n╔{'═'*68}╗")
        print(f"║  SECTOR — {s.get('name', args.sector):<56}║")
        print(f"╚{'═'*68}╝")
        print(f"\nTese:\n  {s.get('thesis', '')}")
        if s.get("macro_exposure"):
            print(f"\nMacro exposure: {', '.join(s['macro_exposure'])}")
        print(f"\nDrivers (confirmação):")
        for d in s.get("drivers", []):
            print(f"  ✓ {d}")
        print(f"\nRisks (abre conversa):")
        for r in s.get("risks", []):
            print(f"  ⚠ {r}")
        affected = find_by_sector(args.sector)
        print(f"\nTickers neste sector ({len(affected)}):")
        for mk, t, th in affected:
            print(f"  {mk.upper()} {t:<8}  intent={th.get('intent', '-'):<12}  {(th.get('thesis') or '')[:60]}")
        return

    if args.macro:
        m = get_macro(args.macro)
        if not m:
            print(f"Macro theme {args.macro!r} não existe. Lista com --sectors-list")
            return
        print(f"\n╔{'═'*68}╗")
        print(f"║  MACRO — {m.get('name', args.macro):<57}║")
        print(f"╚{'═'*68}╝")
        print(f"\nTese:\n  {m.get('thesis', '')}")
        print(f"\nDrivers positivos (confirmação):")
        for d in m.get("drivers_positivos", []):
            print(f"  ✓ {d}")
        print(f"\nDrivers negativos (invalidação):")
        for d in m.get("drivers_negativos", []):
            print(f"  ✗ {d}")
        affected = find_by_macro(args.macro)
        print(f"\nAffected positive: {', '.join(f'{mk.upper()}.{t}' for mk,t in affected['positive'])}")
        print(f"Affected negative: {', '.join(f'{mk.upper()}.{t}' for mk,t in affected['negative'])}")
        print(f"Tickers que linkam este macro: {', '.join(f'{mk.upper()}.{t}' for mk,t in affected['mentioned'])}")
        return

    if args.ticker:
        th = get_thesis(args.ticker.upper(), args.market)
        if not th:
            print(f"Sem tese documentada para {args.ticker}")
            return
        print(f"╔{'═'*68}╗")
        print(f"║  TESE — {args.ticker.upper():<56}║")
        print(f"╚{'═'*68}╝")
        print(f"\nIntent     : {th.get('intent', '-')}")
        print(f"Sector     : {th.get('sector', '-')}")
        print(f"Macro      : {', '.join(th.get('macro', [])) or '-'}")
        print(f"Last review: {th.get('last_review', '-')}")
        print(f"\n### CAMADA TICKER")
        print(f"Tese:\n  {th.get('thesis', '(vazia)')}")
        if th.get("why_hold"):
            print(f"\nWhy hold:\n  {th['why_hold']}")
        if th.get("triggers"):
            print(f"\nTriggers (ticker):")
            for tr in th["triggers"]:
                print(f"  ✓ {tr}")
        if th.get("red_flags"):
            print(f"\nRed flags (ticker):")
            for rf in th["red_flags"]:
                print(f"  ⚠ {rf}")

        # Sector herança
        if th.get("sector"):
            s = get_sector(th["sector"])
            if s:
                print(f"\n### CAMADA SECTOR — {s.get('name', th['sector'])}")
                print(f"Tese:\n  {s.get('thesis', '')}")
                if s.get("drivers"):
                    print(f"\nDrivers sectoriais:")
                    for d in s["drivers"][:4]:
                        print(f"  ✓ {d}")
                if s.get("risks"):
                    print(f"\nRisks sectoriais:")
                    for r in s["risks"][:4]:
                        print(f"  ⚠ {r}")

        # Macro herança
        for mk in (th.get("macro") or []):
            m = get_macro(mk)
            if m:
                print(f"\n### CAMADA MACRO — {m.get('name', mk)}")
                print(f"Tese:\n  {m.get('thesis', '')}")

        if th.get("target_weight") is not None:
            print(f"\nTarget weight: {th['target_weight']}%")
        if th.get("ri_url"):
            print(f"\nRI: {th['ri_url']}")
        if th.get("source"):
            print(f"Source: {', '.join(th['source']) if isinstance(th['source'], list) else th['source']}")
        return

    if args.review:
        out = theses_needing_review(args.review_days)
        print(f"Teses a precisar review (>{args.review_days}d): {len(out)}")
        for mk, t, th in out:
            print(f"  {mk.upper():<3} {t:<8}  last_review={th.get('last_review', 'NUNCA')}  [{th.get('intent')}]")
        return

    if args.triggers:
        alerts = check_trigger_activation(args.trigger_days)
        print(f"Alerts de triggers/red-flags em eventos últimos {args.trigger_days}d: {len(alerts)}")
        for a in alerts:
            bullet = "⚠" if a["flag_hits"] or a["is_critical"] else "✓"
            hits = a["flag_hits"] or a["trigger_hits"]
            hit_str = f" [{','.join(hits[:3])}]" if hits else (" [critical 8-K]" if a["is_critical"] else "")
            print(f"  {bullet} {a['market'].upper()} {a['ticker']:<7} {a['date']}  {a['kind']:<10}{hit_str}")
            print(f"      intent={a['thesis_intent']}  summary={(a['summary'] or '')[:70]}")
        return

    if args.no_thesis:
        missing = find_missing_theses()
        print(f"Holdings sem tese documentada: {len(missing)}")
        for mk, t in missing:
            print(f"  {mk.upper():<3} {t}")
        return

    # Default: sumário de todas as teses
    theses = load_theses()
    for mk in ("br", "us"):
        print(f"\n{'='*72}")
        print(f"TESES {mk.upper()}  ({len(theses.get(mk, {}))} tickers)")
        print(f"{'='*72}")
        for t, th in (theses.get(mk, {}) or {}).items():
            intent = th.get("intent", "-")
            last = th.get("last_review", "?")
            print(f"  {t:<8} [{intent:<11}] review {last}  — {(th.get('thesis') or '')[:75]}")


if __name__ == "__main__":
    main()
