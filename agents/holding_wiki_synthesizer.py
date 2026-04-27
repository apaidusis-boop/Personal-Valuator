"""holding_wiki_synthesizer — gera wiki/holdings/<TICKER>.md stubs via Ollama.

Phase I (2026-04-25). Closeout B.2: 6 holdings sem deep wiki note (ABBV,
GS, PLTR, TSLA, XP, GREK). Distinct from `thesis_synthesizer` (which writes
the `## Thesis` section em ticker notes auto-geradas).

Output marcado AUTO-DRAFT no frontmatter + topo do ficheiro — user revê + refina.

100% Ollama local. Zero Claude tokens.

Uso:
  python -m agents.holding_wiki_synthesizer ABBV
  python -m agents.holding_wiki_synthesizer ABBV GS PLTR TSLA XP GREK
  python -m agents.holding_wiki_synthesizer --missing  # auto-pick os que faltam
  python -m agents.holding_wiki_synthesizer --dry-run ABBV
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.thesis_synthesizer import (
    _build_context, _resolve_market, _select_philosophy, _fundamentals,
    SPECIAL_INTENT, OLLAMA, MODEL,
)

WIKI_HOLDINGS = ROOT / "obsidian_vault" / "wiki" / "holdings"
DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}

# Holdings que devem ter wiki/holdings/<TICKER>.md
EXPECTED_BY_USER = {"ABBV", "GS", "PLTR", "TSLA", "XP", "GREK"}


def _portfolio_data(market: str, ticker: str) -> dict:
    db = DBS[market]
    if not db.exists():
        return {}
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        r = c.execute(
            "SELECT quantity, entry_price, entry_date, notes "
            "FROM portfolio_positions WHERE ticker=? AND active=1",
            (ticker,),
        ).fetchone()
    return dict(r) if r else {}


def synthesize_wiki(ticker: str, market: str | None = None,
                    timeout: int = 180) -> dict | None:
    market = market or _resolve_market(ticker)
    fund = _fundamentals(market, ticker)
    if not fund:
        return {"error": f"no fundamentals row for {ticker}"}

    portfolio = _portfolio_data(market, ticker)
    context = _build_context(ticker, market)
    philosophy = _select_philosophy(ticker, market, fund)
    today = date.today().isoformat()
    special_note = SPECIAL_INTENT.get(ticker, "")

    portfolio_line = ""
    if portfolio.get("quantity"):
        portfolio_line = f"POSITION: {portfolio['quantity']} shares @ {portfolio['entry_price']} entry ({portfolio.get('entry_date', '?')})"

    prompt = f"""Você é um analyst sénior buy-side a escrever uma nota de research
profunda para uma holding na carteira de um value-investor PT-BR.

{philosophy}

CONTEXT (factual, do nosso DB):
{context}
{portfolio_line}

{f'NOTA ESPECIAL: {special_note}' if special_note else ''}

TAREFA: Gera o conteúdo estruturado para wiki/holdings/{ticker}.md.
Usa SÓ números do context — não inventes. Se um critério da filosofia falhar,
diz isso explicitamente. Português PT-BR claro, frases curtas.

Output JSON apenas (sem markdown wrapper):

{{
  "intent_one_liner": "1 frase: DRIP core / Compounder / Tactical / Growth — porquê",
  "business_snapshot": "2-3 frases. Que negócio é, geografia, tipo de receita, scale.",
  "why_we_hold": [
    "razão 1 (1 frase, factual)",
    "razão 2",
    "razão 3",
    "razão 4"
  ],
  "moat": "2-3 frases. Source de vantagem competitiva sustentável.",
  "current_state": "2-3 frases. Onde a empresa está em 2026, métricas chave do context.",
  "invalidation_triggers": [
    "trigger 1 quantitativo",
    "trigger 2",
    "trigger 3",
    "trigger 4"
  ],
  "sizing_drip_intent": "1-2 frases sobre sizing target + intent (DRIP / trim / accumulate)"
}}
"""

    try:
        resp = requests.post(
            OLLAMA,
            json={"model": MODEL, "prompt": prompt, "stream": False,
                  "format": "json", "options": {"temperature": 0.4}},
            timeout=timeout,
        )
        resp.raise_for_status()
    except Exception as e:
        return {"error": f"ollama_call_failed: {e}"}

    raw = resp.json().get("response", "")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "non-json", "raw": raw[:300]}

    return {
        "ticker": ticker, "market": market, "date": today,
        "name": fund.get("name", ticker),
        "sector": fund.get("sector", ""),
        "fundamentals": {
            "pe": fund.get("pe"), "pb": fund.get("pb"),
            "dy": fund.get("dy"), "roe": fund.get("roe"),
            "streak": fund.get("dividend_streak_years"),
            "aristocrat": fund.get("is_aristocrat"),
        },
        "portfolio": portfolio,
        **parsed,
    }


def format_wiki_md(d: dict) -> str:
    """Render dict → wiki/holdings markdown."""
    why = "\n".join(f"{i+1}. {r}" for i, r in enumerate(d.get("why_we_hold", [])))
    triggers = "\n".join(f"- [ ] {t}" for t in d.get("invalidation_triggers", []))

    intent_tag = "DRIP_core"
    intent_lower = (d.get("intent_one_liner") or "").lower()
    if "tactical" in intent_lower:
        intent_tag = "tactical"
    elif "growth" in intent_lower:
        intent_tag = "growth"
    elif "compounder" in intent_lower:
        intent_tag = "compounder"
    elif "value" in intent_lower or "turnaround" in intent_lower:
        intent_tag = "value_turnaround"

    f = d.get("fundamentals") or {}
    fund_line = []
    if f.get("pe") is not None:
        fund_line.append(f"P/E {f['pe']:.1f}")
    if f.get("pb") is not None:
        fund_line.append(f"P/B {f['pb']:.1f}")
    if f.get("dy") is not None:
        fund_line.append(f"DY {f['dy']*100:.1f}%")
    if f.get("roe") is not None:
        fund_line.append(f"ROE {f['roe']*100:.1f}%")
    if f.get("streak"):
        fund_line.append(f"Streak {f['streak']}y")
    fund_summary = " · ".join(fund_line) if fund_line else "(sem fundamentals)"

    portfolio = d.get("portfolio") or {}
    portfolio_line = ""
    if portfolio.get("quantity"):
        portfolio_line = (
            f"- Posição actual: {portfolio['quantity']} shares "
            f"@ {portfolio.get('entry_price', '?')} entry "
            f"({portfolio.get('entry_date', '?')})"
        )

    return f"""---
type: holding_thesis
ticker: {d['ticker']}
market: {d['market']}
sector: {d.get('sector', '')}
intent: {intent_tag}
auto_draft: true
draft_date: {d['date']}
tags: [holding, thesis, {d['market']}, auto_draft]
related: []
---

> ⚠️ **AUTO-DRAFT** ({d['date']}) — gerado por `holding_wiki_synthesizer.py` via
> Ollama Qwen 14B local. Refinar com tese pessoal + memória de contexto que o
> LLM não tem acesso (entry rationale, lições passadas, sizing decisions).
> Após review humana, remover `auto_draft: true` e este aviso.

# 🎯 Thesis: [[{d['ticker']}]] — {d.get('name', d['ticker'])}

> {d.get('intent_one_liner', '')}

## Intent
**{intent_tag.replace('_', ' ').title()}** — {d.get('intent_one_liner', '')}

## Business snapshot
{d.get('business_snapshot', '')}

**Fundamentals**: {fund_summary}

## Por que detemos

{why}

## Moat

{d.get('moat', '')}

## Current state ({d['date'][:7]})

{d.get('current_state', '')}

## Invalidation triggers

{triggers}

## Sizing + DRIP

{d.get('sizing_drip_intent', '')}
{portfolio_line}

---
*AUTO-DRAFT por `holding_wiki_synthesizer.py` · Ollama Qwen 14B local · {d['date']}*
"""


def write_wiki(ticker: str, content: str, dry_run: bool = False) -> str:
    """Write to wiki/holdings/<TICKER>.md. Returns 'written' | 'exists' | 'error'."""
    p = WIKI_HOLDINGS / f"{ticker}.md"
    if p.exists():
        return "exists"
    if dry_run:
        return "written"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return "written"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--missing", action="store_true",
                    help="auto-pick holdings sem wiki/holdings/<TICKER>.md")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.missing:
        existing = {p.stem for p in WIKI_HOLDINGS.glob("*.md") if not p.name.startswith("_")}
        # Get all current holdings from DB
        all_holdings: list[tuple[str, str]] = []
        for market, db in DBS.items():
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ).fetchall()
            for (t,) in rows:
                if t not in existing:
                    all_holdings.append((market, t))
        tickers_list = all_holdings
    else:
        tickers_list = [(_resolve_market(t), t) for t in args.tickers]

    if not tickers_list:
        print("No tickers to process. Use --missing or pass tickers.")
        return

    print(f"Generating {len(tickers_list)} wiki holding stub(s):")
    for mkt, t in tickers_list:
        print(f"  {mkt}:{t}")
    print()

    summary = {"written": 0, "exists": 0, "error": 0}
    for mkt, t in tickers_list:
        print(f"[{t}] Calling Qwen 14B...", flush=True)
        result = synthesize_wiki(t, mkt)
        if not result or result.get("error"):
            print(f"  ERROR: {result.get('error') if result else 'none'}")
            summary["error"] += 1
            continue
        content = format_wiki_md(result)
        status = write_wiki(t, content, dry_run=args.dry_run)
        summary[status] += 1
        print(f"  → {status}{' (dry-run)' if args.dry_run else ''}")

    print()
    print("=== Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
