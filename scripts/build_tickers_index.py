"""Build obsidian_vault/_TICKERS_INDEX.md - top-level table of all 33 holding hubs.

One row per ticker with: handle/sector, currency, position size,
latest verdict, last deepdive timestamp, link to hub.
"""
from __future__ import annotations
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import sqlite3
import json
from pathlib import Path
from datetime import datetime

VAULT = Path("obsidian_vault")
HUBS = VAULT / "hubs"


def holdings_rows() -> list[dict]:
    rows: list[dict] = []
    for market, db in [("br", "data/br_investments.db"), ("us", "data/us_investments.db")]:
        con = sqlite3.connect(db)
        for tk, qty, entry in con.execute(
            "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE active=1 ORDER BY ticker"
        ):
            comp = con.execute("SELECT name, sector FROM companies WHERE ticker=?", (tk,)).fetchone() or ("", "")
            verdict = con.execute(
                "SELECT action, total_score, date FROM verdict_history WHERE ticker=? ORDER BY date DESC LIMIT 1",
                (tk,),
            ).fetchone() or (None, None, None)
            # Latest deepdive JSON timestamp
            dd_files = sorted(Path("reports/deepdive").glob(f"{tk}_deepdive_*.json"))
            dd_dt = ""
            if dd_files:
                dd_dt = datetime.fromtimestamp(dd_files[-1].stat().st_mtime).strftime("%Y-%m-%d")
            rows.append({
                "market": market,
                "ticker": tk,
                "name": comp[0],
                "sector": comp[1] or "",
                "qty": qty,
                "entry": entry,
                "verdict": verdict[0] or "—",
                "score": verdict[1],
                "verdict_date": verdict[2] or "",
                "deepdive_dt": dd_dt,
            })
        con.close()
    return rows


def render(rows: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append("---")
    lines.append("type: index")
    lines.append(f"generated: {today}")
    lines.append("tags: [hub, master_index, holdings]")
    lines.append('parent: "[[CONSTITUTION_Pessoal]]"')
    lines.append('related: "[[_LEITURA_DA_MANHA]]"')
    lines.append("---")
    lines.append("")
    lines.append("# 🗂️ Tickers Index — porta de entrada matinal")
    lines.append("")
    lines.append("> Um link por holding. Clica para abrir o **hub consolidado** do ticker (panorama, histórico cronológico, todos os artefactos). Substitui o atropelo de DOSSIE / STORY / COUNCIL / FILING / OVERNIGHT espalhados.")
    lines.append("")
    lines.append("**Filosofia**: cada nome é uma porta. Atrás dela está tudo (e ordenado).")
    lines.append("")

    # ─── BR ─────────────────────────────────────────────
    br = [r for r in rows if r["market"] == "br"]
    us = [r for r in rows if r["market"] == "us"]

    lines.append(f"## 🇧🇷 Brasil ({len(br)})")
    lines.append("")
    lines.append("| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |")
    lines.append("|---|---|---|---:|---|---:|---|")
    for r in br:
        qty = f"{r['qty']:.0f}" if r["qty"] else "—"
        score = f"{r['score']:.2f}" if r["score"] is not None else "—"
        lines.append(
            f"| [[hubs/{r['ticker']}\\|{r['ticker']}]] | {r['name']} | {r['sector']} | {qty} | `{r['verdict']}` | {score} | {r['deepdive_dt'] or '—'} |"
        )
    lines.append("")

    lines.append(f"## 🇺🇸 EUA ({len(us)})")
    lines.append("")
    lines.append("| Ticker | Nome | Sector | Posição | Verdict | Score | Último deepdive |")
    lines.append("|---|---|---|---:|---|---:|---|")
    for r in us:
        qty = f"{r['qty']:.0f}" if r["qty"] else "—"
        score = f"{r['score']:.2f}" if r["score"] is not None else "—"
        lines.append(
            f"| [[hubs/{r['ticker']}\\|{r['ticker']}]] | {r['name']} | {r['sector']} | {qty} | `{r['verdict']}` | {score} | {r['deepdive_dt'] or '—'} |"
        )
    lines.append("")

    # ─── meta ───────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## Como usar")
    lines.append("")
    lines.append("1. **Manhã**: abre este índice → clica no ticker que queres rever → hub mostra **Hoje** (1 linha de verdict) e **Histórico** (jornal cronológico).")
    lines.append("2. **Refresh**: cada hub tem um bloco `bash` com os 5 comandos canónicos (`ii panorama`, `ii deepdive`, `ii verdict`, `ii fv`, `fair_value_forward`).")
    lines.append("3. **Regenerar tudo**: `python scripts/build_ticker_hubs.py` reescreve os 33 hubs. `python scripts/build_tickers_index.py` reescreve este índice.")
    lines.append("")
    lines.append("## Hubs disponíveis (filesystem)")
    lines.append("")
    for r in sorted(rows, key=lambda x: x["ticker"]):
        lines.append(f"- [[hubs/{r['ticker']}]] · `{r['market'].upper()}` · `{r['sector']}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Gerado por `scripts/build_tickers_index.py`._")
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = holdings_rows()
    out = VAULT / "_TICKERS_INDEX.md"
    out.write_text(render(rows), encoding="utf-8")
    print(f"Wrote {out} with {len(rows)} holdings")


if __name__ == "__main__":
    main()
