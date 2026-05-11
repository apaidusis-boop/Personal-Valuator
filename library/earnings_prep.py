"""Earnings Prep Cockpit — pre-call memo automático para próximos earnings.

Inspirado em "Autonomous earnings prep bot" da lista do user.

Para cada ticker em earnings_calendar com earnings_date <= 30d à frente:
  1. Pull last 4-6 quarters de quarterly_single (ou yf_deep_fundamentals para US)
  2. Pull thesis_health latest + thesis text from vault
  3. Pull recent IPE events / news / analyst_insights (last 30d)
  4. Compute key questions:
     - Margin trend (improving/compressing)
     - Guidance/expectations vs consensus
     - Risk flags
  5. Ollama gera "Pre-call brief": 5-10 bullets + 5 questions to listen for + watch metrics
  6. Output: obsidian_vault/briefings/earnings_prep_<TICKER>_<DATE>.md

100% local. Generated 7d before earnings_date.

Uso:
    python -m library.earnings_prep --upcoming 30      # all next 30 days
    python -m library.earnings_prep --ticker AAPL
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
BRIEFINGS_DIR = ROOT / "obsidian_vault" / "briefings"

MODEL = "qwen2.5:14b-instruct-q4_K_M"

PREP_PROMPT = """És analista preparando-se para uma earnings call.

CONTEXT:
{context}

TASK: Gera "Pre-call Brief" estruturado em PORTUGUÊS:

## 🔥 Top 3 things to watch
- métrica/comentário 1 (max 30 palavras, com número-alvo se possível)
- métrica 2
- métrica 3

## ❓ Specific questions to listen for management
1. Pergunta concreta sobre área X (max 20 palavras)
2. Pergunta sobre área Y
3. Pergunta sobre área Z
4. Pergunta sobre area W
5. Pergunta sobre area V

## 📊 Trajectory check (vs trend)
- O que precisa CONFIRMAR no call (continuar trend Y)
- O que precisa MUDAR (revertir trend Z)

## 🚨 Red flags potenciais
- Sinal vermelho 1 (margin/debt/guidance/segment)
- Sinal vermelho 2

## 🎯 Decision framework
- BUY MORE if: condição quantitativa
- HOLD if: condição
- TRIM if: condição

Responde SÓ o markdown estruturado, sem prefácio."""


def _fundamentals(market: str, ticker: str) -> dict:
    db = DBS[market]
    if not db.exists():
        return {}
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        return dict(row) if row else {}


def _quarterly_single(market: str, ticker: str, n: int = 6) -> list[dict]:
    db = DBS[market]
    try:
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute(
                "SELECT period_end, fiscal_quarter, revenue, ebit, net_income, "
                "ebit_margin, net_margin, fco, fcf_proxy, debt_total "
                "FROM quarterly_single WHERE ticker=? ORDER BY period_end DESC LIMIT ?",
                (ticker, n),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.OperationalError:
        return []


def _thesis_health(market: str, ticker: str) -> dict | None:
    try:
        with sqlite3.connect(DBS[market]) as c:
            c.row_factory = sqlite3.Row
            row = c.execute(
                "SELECT * FROM thesis_health WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            return dict(row) if row else None
    except sqlite3.OperationalError:
        return None


def _recent_analyst_insights(market: str, ticker: str, days: int = 60) -> list[dict]:
    try:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        with sqlite3.connect(DBS[market]) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute(
                "SELECT stance, claim, kind, evidence_quote, created_at FROM analyst_insights "
                "WHERE ticker=? AND created_at >= ? ORDER BY created_at DESC LIMIT 10",
                (ticker, cutoff),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.OperationalError:
        return []


def _vault_thesis(ticker: str) -> str | None:
    p = TICKERS_DIR / f"{ticker}.md"
    if not p.exists():
        return None
    content = p.read_text(encoding="utf-8", errors="ignore")
    if "## Thesis" not in content:
        return None
    after = content.split("## Thesis", 1)[1]
    end = after.find("\n## ")
    return (after[:end].strip() if end > 0 else after.strip())[:1200]


def _tavily_pre_call_research(ticker: str, market: str) -> dict:
    """Pull pre-call analyst expectations + last quarter call notes via Tavily.
    Phase K wire (2026-04-26). 2 calls per ticker per prep run; cache 7d
    (re-runs em mesma earnings = 0 calls)."""
    out = {"available": False, "guidance_hits": [], "earnings_hits": []}
    try:
        from agents.autoresearch import search_ticker
    except Exception:
        return out
    g = search_ticker(ticker, topic="guidance", market=market, days_back=60)
    e = search_ticker(ticker, topic="earnings", market=market, days_back=90)
    if g.error and e.error:
        return out
    out["available"] = True
    if not g.error:
        out["guidance_answer"] = g.answer or ""
        out["guidance_hits"] = [
            {"title": h.title[:100], "url": h.url, "content": h.content[:300]}
            for h in g.results[:3]
        ]
    if not e.error:
        out["earnings_answer"] = e.answer or ""
        out["earnings_hits"] = [
            {"title": h.title[:100], "url": h.url, "content": h.content[:300]}
            for h in e.results[:3]
        ]
    out["cached"] = g.cached and e.cached
    return out


def build_context(ticker: str, market: str, earnings_date: str,
                   use_tavily: bool = True) -> str:
    f = _fundamentals(market, ticker)
    qs = _quarterly_single(market, ticker)
    th = _thesis_health(market, ticker)
    ai = _recent_analyst_insights(market, ticker)
    thesis = _vault_thesis(ticker)
    tavily = _tavily_pre_call_research(ticker, market) if use_tavily else {"available": False}

    lines = [
        f"TICKER: {market.upper()}:{ticker}",
        f"EARNINGS DATE: {earnings_date}",
    ]
    if f:
        lines.append("\nFUNDAMENTALS:")
        for k in ("pe", "pb", "dy", "roe", "net_debt_ebitda", "market_cap_usd", "current_ratio"):
            v = f.get(k)
            if v is not None:
                if k in ("dy", "roe") or "margin" in k:
                    lines.append(f"  {k}: {v*100:.2f}%" if abs(v) < 5 else f"  {k}: {v}")
                elif k == "market_cap_usd":
                    lines.append(f"  {k}: ${v/1e9:.1f}B")
                else:
                    lines.append(f"  {k}: {v}")
    if qs:
        lines.append("\nQUARTERLY TRAJECTORY (single-Q, R$ bi se BR):")
        for r in qs:
            rev = (r['revenue'] or 0)/1e6
            ebit = (r['ebit'] or 0)/1e6
            em = (r['ebit_margin'] or 0)*100
            ni = (r['net_income'] or 0)/1e6
            fcf = (r['fcf_proxy'] or 0)/1e6
            lines.append(f"  {r['period_end']} ({r['fiscal_quarter']}): rev={rev:.1f} ebit={ebit:.1f} ni={ni:.1f} em%={em:.1f} fcf={fcf:.1f}")
    if th:
        lines.append(f"\nTHESIS HEALTH: {th['thesis_score']}/100 (contras={th['contradictions']}, risk_flags={th['risk_flags']})")
    if ai:
        lines.append("\nANALYST INSIGHTS (last 60d):")
        for a in ai[:5]:
            stance = a.get("stance") or "?"
            lines.append(f"  [{stance}] {a.get('claim','')[:140]}")
    if thesis:
        lines.append(f"\nOUR THESIS:\n{thesis}")
    # Phase K — Tavily pre-call research (analyst expectations + last quarter notes)
    if tavily.get("available"):
        if tavily.get("earnings_answer"):
            lines.append(f"\nWEB EARNINGS CONTEXT (Tavily synth, last 90d):")
            lines.append(f"  {tavily['earnings_answer'][:600]}")
        if tavily.get("guidance_answer"):
            lines.append(f"\nWEB GUIDANCE CONTEXT (Tavily synth, last 60d):")
            lines.append(f"  {tavily['guidance_answer'][:600]}")
        if tavily.get("earnings_hits"):
            lines.append(f"\nWEB EARNINGS HEADLINES:")
            for h in tavily["earnings_hits"][:3]:
                lines.append(f"  - {h['title']}")
        if tavily.get("guidance_hits"):
            lines.append(f"\nWEB GUIDANCE HEADLINES:")
            for h in tavily["guidance_hits"][:3]:
                lines.append(f"  - {h['title']}")
    return "\n".join(lines)


def gen_prep_brief(context: str, timeout: int = 180) -> str | None:
    prompt = PREP_PROMPT.replace("{context}", context[:4000])
    from agents._llm import ollama_call
    raw = ollama_call(
        prompt,
        model=MODEL,
        max_tokens=1200,
        temperature=0.3,
        timeout=timeout,
    )
    if raw.startswith("[LLM FAILED"):
        return f"(error: {raw})"
    return raw


def upcoming_earnings(days_ahead: int = 30) -> list[dict]:
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=days_ahead)).isoformat()
    out = []
    for market, db in DBS.items():
        if not db.exists():
            continue
        try:
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                rows = c.execute(
                    "SELECT ticker, earnings_date FROM earnings_calendar "
                    "WHERE earnings_date >= ? AND earnings_date <= ? "
                    "ORDER BY earnings_date",
                    (today, cutoff),
                ).fetchall()
                for r in rows:
                    out.append({"ticker": r["ticker"], "earnings_date": r["earnings_date"], "market": market})
        except sqlite3.OperationalError:
            continue
    return out


def prep_one(ticker: str, market: str, earnings_date: str, verbose: bool = True) -> Path | None:
    if verbose:
        print(f"  preparing {market.upper()}:{ticker} (earnings {earnings_date})...", end=" ", flush=True)
    context = build_context(ticker, market, earnings_date)
    t0 = time.time()
    brief = gen_prep_brief(context)
    elapsed = time.time() - t0
    if not brief or brief.startswith("(error"):
        if verbose:
            print(f"FAIL ({brief})")
        return None

    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    out = BRIEFINGS_DIR / f"earnings_prep_{ticker}_{earnings_date}.md"
    md = [
        "---",
        f"type: earnings_prep_brief",
        f"ticker: {ticker}",
        f"market: {market}",
        f"earnings_date: {earnings_date}",
        f"generated: {date.today().isoformat()}",
        "tags: [earnings, prep, brief]",
        "---",
        "",
        f"# 📞 Earnings Prep — {ticker} ({earnings_date})",
        "",
        f"_Auto-generated {(date.fromisoformat(earnings_date) - date.today()).days} days before call. 100% Ollama local._",
        "",
        brief,
        "",
        "---",
        "## 📊 Context provided to LLM",
        "",
        "```",
        context[:2500],
        "```",
    ]
    out.write_text("\n".join(md), encoding="utf-8")
    if verbose:
        print(f"OK ({elapsed:.1f}s) -> {out.name}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upcoming", type=int, default=0, help="Generate for all upcoming N days")
    ap.add_argument("--ticker")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--date", help="Custom earnings date if not in calendar")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.upcoming:
        upcoming = upcoming_earnings(args.upcoming)
        print(f"=== Earnings prep — {len(upcoming)} upcoming events (next {args.upcoming}d) ===")
        for u in upcoming:
            prep_one(u["ticker"], u["market"], u["earnings_date"])
        print(f"\nDone. Briefs saved to obsidian_vault/briefings/")
    elif args.ticker:
        market = args.market or "us"
        edate = args.date or date.today().isoformat()
        prep_one(args.ticker.upper(), market, edate)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
