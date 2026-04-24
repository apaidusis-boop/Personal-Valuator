"""panorama — super-command: agrega TUDO sobre um ticker num só markdown.

Corre inhouse (zero tokens Claude). Combina outputs de:
  - verdict (BUY/HOLD/SELL + narrativa)
  - scoring (screen + Altman + Piotroski + Dividend Safety)
  - peers (percentil vs sector)
  - triggers abertos (action_cli list --ticker)
  - notes (notes_cli show)
  - video insights (últimos 3)
  - analyst insights (subscriptions, últimos 90d)
  - wiki links (sector + cycle relevantes)

Uso:
    python scripts/panorama.py X
    python scripts/panorama.py X --write          # grava em tickers/<X>.md (Obsidian)
    python scripts/panorama.py X --md             # imprime markdown, não gravado
    ii panorama X                                  # via CLI

Design: acumula tudo num `sections` dict e renderiza tail. Falhas em secções
individuais são isoladas (não bloqueiam o resto).
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
PY = sys.executable


def _run_script(script_path: str, args: list[str], timeout: int = 60) -> str:
    """Corre um script em subprocess e devolve stdout. Isolado — erros não matam panorama."""
    try:
        r = subprocess.run(
            [PY, "-X", "utf8", str(ROOT / script_path), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return r.stdout.strip() or f"(sem output — rc={r.returncode})"
    except subprocess.TimeoutExpired:
        return "(timeout)"
    except Exception as e:
        return f"(erro: {e})"


def _run_module(module: str, args: list[str], timeout: int = 60) -> str:
    try:
        r = subprocess.run(
            [PY, "-X", "utf8", "-m", module, *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return r.stdout.strip() or f"(sem output — rc={r.returncode})"
    except Exception as e:
        return f"(erro: {e})"


def _detect_market(ticker: str) -> str:
    with sqlite3.connect(DB_BR) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
            return "br"
    with sqlite3.connect(DB_US) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
            return "us"
    return "us"  # fallback


def _snapshot_from_db(ticker: str, market: str) -> dict:
    db = DB_BR if market == "br" else DB_US
    out: dict = {"ticker": ticker, "market": market}
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT name, sector, is_holding, currency FROM companies WHERE ticker=?",
            (ticker,),
        ).fetchone()
        if row:
            out.update(dict(row))
        p = c.execute(
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if p:
            out["price"] = p["close"]
            out["price_date"] = p["date"]
        pos = c.execute(
            "SELECT quantity, entry_price, entry_date FROM portfolio_positions WHERE ticker=? AND active=1 LIMIT 1",
            (ticker,),
        ).fetchone()
        if pos:
            out["position"] = dict(pos)
        f = c.execute(
            """SELECT period_end, pe, pb, dy, roe, net_debt_ebitda,
                      dividend_streak_years, is_aristocrat
               FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if f:
            out["fund"] = dict(f)
        # últimos video insights
        try:
            vids = c.execute(
                """SELECT v.title, v.channel, v.published_at, i.kind, i.claim, i.confidence
                   FROM video_insights i JOIN videos v ON i.video_id=v.video_id
                   WHERE i.ticker=? ORDER BY v.published_at DESC, i.confidence DESC LIMIT 5""",
                (ticker,),
            ).fetchall()
            out["video_insights"] = [dict(v) for v in vids]
        except sqlite3.OperationalError:
            out["video_insights"] = []
        # triggers abertos
        try:
            trig = c.execute(
                """SELECT kind, action_hint, note, created_at
                   FROM watchlist_actions WHERE ticker=? AND status='open'
                   ORDER BY created_at DESC""",
                (ticker,),
            ).fetchall()
            out["open_triggers"] = [dict(t) for t in trig]
        except sqlite3.OperationalError:
            out["open_triggers"] = []
    return out


def _analyst_insights(ticker: str, days: int = 90) -> list[dict]:
    cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()
    items: list[dict] = []
    for db in (DB_BR, DB_US):
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            try:
                rows = c.execute(
                    """SELECT r.source, r.published_at, r.title,
                              i.kind, i.claim, i.stance, i.price_target, i.confidence
                       FROM analyst_insights i JOIN analyst_reports r ON i.report_id=r.id
                       WHERE i.ticker=? AND r.published_at >= ?
                       ORDER BY r.published_at DESC, i.confidence DESC LIMIT 10""",
                    (ticker, cutoff),
                ).fetchall()
                items.extend(dict(r) for r in rows)
            except sqlite3.OperationalError:
                pass
    return items


def _notes_for_ticker(ticker: str) -> str:
    notes_dir = Path(os.environ.get(
        "II_NOTES_DIR",
        r"C:\Users\paidu\.claude\projects\C--Users-paidu-investment-intelligence\memory\notes",
    ))
    p = notes_dir / f"{ticker}.md"
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def _wiki_sector_link(sector: str | None, market: str) -> str | None:
    """Mapeia sector name → wiki note path se existir."""
    if not sector:
        return None
    mapping = {
        "Banks": "BR_Banks" if market == "br" else None,
        "Financials": "BR_Banks" if market == "br" else None,
        "Utilities": "BR_Utilities" if market == "br" else None,
        "REIT": "BR_FIIs_vs_US_REITs",
        "Real Estate": "BR_FIIs_vs_US_REITs",
        "FII": "BR_FIIs_vs_US_REITs",
        "Technology": "Semiconductors_cycle",
        "Oil & Gas": "Oil_and_Gas_cycle",
        "Energy": "Oil_and_Gas_cycle",
        "Materials": "Pulp_and_Paper_cycle",
        "Consumer Staples": "Consumer_Staples_moats",
        "IT Services": "Consulting_IT_Services",
        "Information Technology": "Consulting_IT_Services",
    }
    return mapping.get(sector)


def _wiki_cycle_link(sector: str | None) -> str | None:
    if not sector:
        return None
    mapping = {
        "Oil & Gas": "Oil_cycle", "Energy": "Oil_cycle",
        "Technology": "Semi_cycle",
        "Materials": "Pulp_cycle",
        "REIT": "Real_estate_cycle", "Real Estate": "Real_estate_cycle",
        "FII": "Real_estate_cycle",
    }
    return mapping.get(sector)


def render_panorama(ticker: str) -> str:
    ticker = ticker.upper()
    market = _detect_market(ticker)
    snap = _snapshot_from_db(ticker, market)
    notes = _notes_for_ticker(ticker)
    analyst = _analyst_insights(ticker, days=90)

    out: list[str] = []
    out.append(f"---")
    out.append(f"type: panorama")
    out.append(f"ticker: {ticker}")
    out.append(f"market: {market}")
    out.append(f"generated_at: {datetime.now().isoformat(timespec='seconds')}")
    out.append(f"---\n")
    out.append(f"# 🎯 Panorama — {ticker}")
    out.append(f"_{snap.get('name') or ticker}  ·  {snap.get('sector','?')}  ·  Mercado: {market.upper()}_\n")

    # Snapshot
    out.append("## 📸 Snapshot")
    cur = "R$" if market == "br" else "$"
    price = snap.get("price")
    price_str = f"{cur}{price:.2f} ({snap.get('price_date','?')})" if price else "n/a"
    out.append(f"- **Preço**: {price_str}")
    if snap.get("position"):
        pos = snap["position"]
        out.append(f"- **Posição**: {pos['quantity']} @ {cur}{pos['entry_price']:.2f} (entry {pos['entry_date']})")
    else:
        out.append("- **Posição**: (não holding)")
    if snap.get("fund"):
        f = snap["fund"]
        bits = []
        if f.get("pe") is not None: bits.append(f"P/E {f['pe']:.1f}")
        if f.get("pb") is not None: bits.append(f"P/B {f['pb']:.2f}")
        if f.get("dy") is not None: bits.append(f"DY {f['dy']*100:.2f}%")
        if f.get("roe") is not None: bits.append(f"ROE {f['roe']*100:.1f}%")
        if f.get("net_debt_ebitda") is not None: bits.append(f"ND/EBITDA {f['net_debt_ebitda']:.2f}×")
        if f.get("dividend_streak_years"): bits.append(f"Streak {f['dividend_streak_years']}y")
        if f.get("is_aristocrat"): bits.append("Aristocrat ✓")
        out.append(f"- **Fundamentals**: {' · '.join(bits)}")
    out.append("")

    # Verdict — executado live
    out.append("## ⚖ Verdict")
    verdict_out = _run_script("scripts/verdict.py", [ticker], timeout=30)
    out.append("```")
    out.append(verdict_out[:2000])
    out.append("```\n")

    # Screen + quality scores
    out.append("## 🔬 Quality scores")
    out.append("```")
    out.append(_run_module("scoring.altman", [ticker], timeout=20)[:600])
    out.append("")
    out.append(_run_module("scoring.piotroski", [ticker], timeout=20)[:600])
    out.append("")
    out.append(_run_module("scoring.dividend_safety", [ticker], timeout=20)[:600])
    out.append("```\n")

    # Peers
    out.append("## 📊 Peers")
    peers_out = _run_script("scripts/peer_compare.py", [ticker], timeout=30)
    out.append("```")
    out.append(peers_out[:1500])
    out.append("```\n")

    # Triggers abertos
    if snap.get("open_triggers"):
        out.append("## ⚡ Triggers abertos")
        for t in snap["open_triggers"]:
            out.append(f"- [{t['kind']}] {t['action_hint']} — {t.get('note','') or ''}")
        out.append("")

    # Analyst views (subscriptions)
    if analyst:
        out.append(f"## 📰 Analyst views ({len(analyst)} insights, últimos 90d)")
        for a in analyst:
            stance = f" [{a['stance']}]" if a['stance'] else ""
            pt = f" PT={a['price_target']}" if a['price_target'] else ""
            out.append(f"- `{a['published_at']}` **{a['source']}** {a['kind']}{stance}{pt}")
            out.append(f"  > {a['claim'][:250]}")
        out.append("")

    # Video insights
    if snap.get("video_insights"):
        out.append(f"## 🎬 YouTube insights (top 5)")
        for v in snap["video_insights"]:
            out.append(f"- `{v['published_at']}` **{v['channel']}** [{v['kind']}, {v['confidence']:.2f}]")
            out.append(f"  > {v['claim'][:250]}")
        out.append("")

    # User notes
    if notes:
        out.append("## 📝 Tuas notas")
        out.append(notes[:2000])
        out.append("")

    # Wiki context links
    sector = snap.get("sector")
    wiki_sec = _wiki_sector_link(sector, market)
    wiki_cyc = _wiki_cycle_link(sector)
    links = []
    if wiki_sec: links.append(f"[[wiki/sectors/{wiki_sec}|{wiki_sec}]]")
    if wiki_cyc: links.append(f"[[wiki/cycles/{wiki_cyc}|{wiki_cyc}]]")
    links.append("[[wiki/playbooks/Buy_checklist|Buy checklist]]")
    links.append("[[wiki/playbooks/Sell_triggers|Sell triggers]]")
    out.append("## 🔗 Wiki context")
    out.append(" · ".join(links))
    out.append("")

    out.append("---")
    out.append(f"*Panorama gerado por `ii panorama {ticker}` — 0 tokens Claude.*")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ticker")
    ap.add_argument("--write", action="store_true", help="grava em vault tickers/<X>.md")
    ap.add_argument("--md", action="store_true", help="imprime markdown (default)")
    args = ap.parse_args()
    md = render_panorama(args.ticker)
    if args.write:
        vault = Path(os.environ.get("OBSIDIAN_VAULT_PATH", ROOT / "obsidian_vault"))
        target = vault / "tickers" / f"{args.ticker.upper()}_panorama.md"
        target.write_text(md, encoding="utf-8")
        print(f"✓ {target}")
    else:
        print(md)


if __name__ == "__main__":
    main()
