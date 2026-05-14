"""Build obsidian_vault/_TICKERS_INDEX.md covering ALL tickers with a hub.

3 sections: 🇧🇷 BR · 🇺🇸 US Holdings/Watchlist · 🇺🇸 US Kings & Aristocrats / Research.
Each row: ticker link to hub + name + sector + posição (if holding) + verdict + score.
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import sqlite3
import yaml
import json
from pathlib import Path
from datetime import datetime

VAULT = Path("obsidian_vault")
HUBS = VAULT / "hubs"


def load_universe() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open("config/universe.yaml", "r", encoding="utf-8") as f:
        u = yaml.safe_load(f)
    for market in ("br", "us"):
        m = u.get(market, {})
        for bucket in ("holdings", "watchlist", "research_pool"):
            stack = [m.get(bucket, {})]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    stack.extend(cur.values())
                elif isinstance(cur, list):
                    for item in cur:
                        if isinstance(item, dict) and "ticker" in item:
                            tk = item["ticker"]
                            if tk not in out:
                                out[tk] = {
                                    "market": market, "bucket": bucket,
                                    "name": item.get("name", ""),
                                    "sector": item.get("sector") or item.get("segment", ""),
                                }
    if Path("config/kings_aristocrats.yaml").exists():
        with open("config/kings_aristocrats.yaml", "r", encoding="utf-8") as f:
            k = yaml.safe_load(f)
        for item in k.get("tickers", []):
            tk = item["ticker"]
            if tk not in out:
                out[tk] = {"market": "us", "bucket": "kings_aristocrats", "name": item.get("name", ""), "sector": item.get("sector", "")}
    return out


def load_db_meta(tk: str, market: str) -> dict:
    db = f"data/{market}_investments.db"
    out: dict = {}
    try:
        con = sqlite3.connect(db)
        row = con.execute("SELECT quantity, entry_price FROM portfolio_positions WHERE ticker=? AND active=1", (tk,)).fetchone()
        if row:
            out["qty"], out["entry"] = row
        row = con.execute("SELECT action, total_score, date FROM verdict_history WHERE ticker=? ORDER BY date DESC LIMIT 1", (tk,)).fetchone()
        if row:
            out["verdict"], out["score"], out["verdict_date"] = row
        con.close()
    except sqlite3.Error:
        pass
    dd = sorted(Path("reports/deepdive").glob(f"{tk}_deepdive_*.json"))
    if dd:
        out["deepdive_dt"] = datetime.fromtimestamp(dd[-1].stat().st_mtime).strftime("%Y-%m-%d")
    return out


def render_table(rows: list[tuple[str, dict, dict]]) -> str:
    """Render a markdown table for given rows."""
    lines = []
    lines.append("| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |")
    lines.append("|---|---|---|---:|---|---:|---|")
    for tk, meta, db in rows:
        qty = f"{db['qty']:.0f}" if db.get("qty") else "—"
        verdict = db.get("verdict", "—") or "—"
        score = f"{db['score']:.2f}" if db.get("score") is not None else "—"
        dd = db.get("deepdive_dt", "—")
        name = (meta.get("name") or "")[:30]
        sector = (meta.get("sector") or "")[:18]
        lines.append(f"| [[hubs/{tk}\\|{tk}]] | {name} | {sector} | {qty} | `{verdict}` | {score} | {dd} |")
    return "\n".join(lines)


def main() -> None:
    universe = load_universe()
    # Filter to those with a hub
    rows = []
    for tk, meta in universe.items():
        if not (HUBS / f"{tk}.md").exists():
            continue
        db = load_db_meta(tk, meta["market"])
        rows.append((tk, meta, db))
    rows.sort(key=lambda r: r[0])
    print(f"{len(rows)} tickers with hubs")

    by_section = {
        "br_holdings": [r for r in rows if r[1]["market"] == "br" and r[1]["bucket"] == "holdings"],
        "br_watchlist": [r for r in rows if r[1]["market"] == "br" and r[1]["bucket"] == "watchlist"],
        "br_research": [r for r in rows if r[1]["market"] == "br" and r[1]["bucket"] == "research_pool"],
        "us_holdings": [r for r in rows if r[1]["market"] == "us" and r[1]["bucket"] == "holdings"],
        "us_watchlist": [r for r in rows if r[1]["market"] == "us" and r[1]["bucket"] == "watchlist"],
        "us_research": [r for r in rows if r[1]["market"] == "us" and r[1]["bucket"] == "research_pool"],
        "us_kings": [r for r in rows if r[1]["market"] == "us" and r[1]["bucket"] == "kings_aristocrats"],
    }

    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append("---")
    lines.append("type: index")
    lines.append(f"generated: {today}")
    lines.append(f"total_hubs: {len(rows)}")
    lines.append("tags: [hub, master_index]")
    lines.append('parent: "[[CONSTITUTION_Pessoal]]"')
    lines.append("---")
    lines.append("")
    lines.append("# 🗂️ Tickers Index — porta única matinal")
    lines.append("")
    lines.append(f"> Cada ticker tem 1 hub consolidado em `obsidian_vault/hubs/<TK>.md` que ABSORVE todo o conteúdo histórico (panorama, dossier, story, council, IC debate, variant, RI, filings, overnights, drips, wiki, reviews). Ficheiros-fonte estão em `cemetery/2026-05-14/`.")
    lines.append("")
    lines.append(f"**{len(rows)} hubs** · gerado {today}")
    lines.append("")

    sections_meta = [
        ("br_holdings", "🇧🇷 Brasil · Holdings"),
        ("us_holdings", "🇺🇸 EUA · Holdings"),
        ("br_watchlist", "🇧🇷 Brasil · Watchlist"),
        ("us_watchlist", "🇺🇸 EUA · Watchlist"),
        ("br_research", "🇧🇷 Brasil · Research pool"),
        ("us_research", "🇺🇸 EUA · Research pool"),
        ("us_kings", "🇺🇸 EUA · Kings & Aristocrats"),
    ]
    for key, label in sections_meta:
        rows_section = by_section[key]
        if not rows_section:
            continue
        lines.append(f"## {label} ({len(rows_section)})")
        lines.append("")
        lines.append(render_table(rows_section))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Como usar")
    lines.append("1. **Manhã**: abre este índice → clica no ticker → hub mostra **Hoje** (1 linha de verdict + fundamentals) e **Histórico** (todo o conteúdo absorvido cronologicamente).")
    lines.append("2. **Refresh**: cada hub tem 5 comandos canónicos no fim.")
    lines.append("3. **Regenerar todos**: `python scripts/build_merged_hubs.py` + `python scripts/build_tickers_index.py`.")
    lines.append("")
    lines.append("_Gerado por `scripts/build_tickers_index.py`._")

    out = VAULT / "_TICKERS_INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} hubs across {sum(1 for k,_ in sections_meta if by_section[k])} sections)")


if __name__ == "__main__":
    main()
