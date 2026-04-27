"""Synthetic Investment Committee — multi-personality debate via Ollama local.

Inspirado em "Expert synthetic panel" da lista de ideias do user.

Cada persona é um investidor lendário com framework próprio:
  - Buffett: quality + moat + simplicity + long horizon
  - Druckenmiller: macro + concentration + asymmetric bets
  - Taleb: tail risk + barbell + skin in the game
  - Klarman: margin of safety + opportunistic + cash patience
  - Dalio (extra): debt cycle + diversification + balance

Workflow:
  1. Pull ticker context (fundamentals + RI timeline + thesis health + 4 quarters)
  2. Para cada persona, prompt Ollama com persona's framework
  3. Cada persona devolve: verdict (BUY/HOLD/AVOID), 2-3 razões, 1 risk
  4. Synthesizer agrega: convergência + divergência + final committee verdict
  5. Output em obsidian_vault/tickers/<TICKER>_IC_DEBATE.md

100% Ollama local. Zero Claude tokens.

Uso:
    python -m agents.synthetic_ic ITSA4
    python -m agents.synthetic_ic --all-holdings
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"

MODEL = "qwen2.5:14b-instruct-q4_K_M"


PERSONAS = {
    "buffett": {
        "name": "Warren Buffett",
        "framework": """Você é Warren Buffett. Avalia investimentos com este framework:
- Compre business excelente a preço justo (qualidade > barato)
- Moat duradouro (brand, switching costs, network effects, cost advantage)
- Management honesto e capaz (skin in the game)
- ROIC alto e estável > 15%
- Geração de cash livre crescente
- Horizonte: forever
- Evita: turnarounds, IPOs, complexity, leverage cíclica
- Crucial: "É melhor estar aproximadamente certo do que precisamente errado"
""",
    },
    "druckenmiller": {
        "name": "Stan Druckenmiller",
        "framework": """Você é Stan Druckenmiller. Framework:
- Macro liquidity é o motor #1 — quando central banks aliviam, longa equities/risk
- Concentre quando convicção forte (5-10 positions max)
- Bet asymmetric — risk small for big upside; cut losers fast
- Olha 6-18 meses à frente, não trailing
- Currency, rates, commodities cross-asset signals
- Avalia: liquidity regime + earnings power + market positioning
- "É um sport de batting avg + slugging — winners têm que pagar a conta dos losers"
""",
    },
    "taleb": {
        "name": "Nassim Taleb",
        "framework": """Você é Nassim Taleb. Framework:
- Tail risk + black swans são tudo o que importa long-term
- Barbell strategy: 80% ultra-safe + 20% extremely speculative
- Procura ANTI-fragility — beneficia de volatilidade
- Skin in the game obrigatório (avoid management sem skin)
- Hidden risks: leverage, fragility, opacity, complex derivatives
- Survival > optimization
- Quase sempre: AVOID overvalued growth + AVOID leveraged turnarounds
- Valoriza: convex payoffs, optionality, redundancy
""",
    },
    "klarman": {
        "name": "Seth Klarman",
        "framework": """Você é Seth Klarman. Framework:
- Margin of safety: comprar com desconto significativo do valor intrínseco (≥30%)
- Cash é position em si quando não há valor
- Opportunistic: special situations, distressed, spinoffs, complexity
- Avoid leverage NA carteira E nas empresas
- Bottoms-up valuation rigorous
- Patient capital — multi-year holding period esperado
- "Risk is permanent loss of capital, not volatility"
""",
    },
    "dalio": {
        "name": "Ray Dalio",
        "framework": """Você é Ray Dalio. Framework:
- Big debt cycles drivam tudo — onde estamos no ciclo?
- Diversification across asset classes que perform em diferentes regimes
- All-Weather: equities + bonds + commodities + gold em proporção
- Avoid: bubbles (4 critérios), late cycle leverage, single-country concentration
- Look at debt/GDP, capital flows, currency, central bank stance
- Country power index — geopolitical lens
- "Pain + Reflection = Progress"
""",
    },
}


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


def _quarterly_history(market: str, ticker: str, n: int = 6) -> list[dict]:
    db = DBS[market]
    try:
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute(
                "SELECT period_end, revenue, ebit, net_income, ebit_margin, "
                "net_margin, debt_total, fcf_proxy, fco "
                "FROM quarterly_single WHERE ticker=? ORDER BY period_end DESC LIMIT ?",
                (ticker, n),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.OperationalError:
        return []


def _thesis_health(market: str, ticker: str) -> dict | None:
    db = DBS[market]
    try:
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            row = c.execute(
                "SELECT thesis_score, contradictions, risk_flags, regime_shift, details_json "
                "FROM thesis_health WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            return dict(row) if row else None
    except sqlite3.OperationalError:
        return None


def _vault_thesis(ticker: str) -> str | None:
    """Thin wrapper around the canonical reader (Phase Cleanup 2026-04-27).

    Note: this now also reads from <TICKER>_DOSSIE.md (numbered '## N. Thesis')
    in addition to legacy '## Thesis' wiki notes. Behaviour bonus from
    centralisation — was previously missing dossier-resident theses (Phase G+).
    """
    from agents._common import read_vault_thesis
    return read_vault_thesis(ticker, max_chars=1500)


def _tavily_recent_news(ticker: str, market: str, max_hits: int = 4) -> list[dict]:
    """Pull recent material news (14d) via Tavily for IC personas reagirem.
    Phase K wire (2026-04-26). 1 call por ticker; cache 7d. Same news passa
    para todas 5 personas (não multiplica calls)."""
    try:
        from agents.autoresearch import search_ticker
        r = search_ticker(ticker, topic="news", market=market, days_back=14)
    except Exception:
        return []
    if r.error or not r.results:
        return []
    return [{"title": h.title[:120], "score": h.score,
             "published": h.published_date, "content": h.content[:300]}
            for h in r.results[:max_hits]]


def build_context(ticker: str, market: str, use_tavily: bool = True) -> str:
    f = _fundamentals(market, ticker)
    qh = _quarterly_history(market, ticker)
    th = _thesis_health(market, ticker)
    th_text = _vault_thesis(ticker)
    news = _tavily_recent_news(ticker, market) if use_tavily else []

    lines = [f"TICKER: {market.upper()}:{ticker}"]

    if f:
        lines.append("\nFUNDAMENTALS LATEST:")
        for k in ("pe", "pb", "dy", "roe", "net_debt_ebitda", "market_cap_usd", "current_ratio", "beta_levered"):
            v = f.get(k)
            if v is not None:
                if "margin" in k or k in ("dy", "roe"):
                    lines.append(f"  {k}: {v*100:.2f}%" if abs(v) < 5 else f"  {k}: {v}")
                elif k == "market_cap_usd":
                    lines.append(f"  {k}: ${v/1e9:.1f}B")
                else:
                    lines.append(f"  {k}: {v}")

    if qh:
        lines.append("\nQUARTERLY TRAJECTORY (single-Q, R$ bi):")
        for r in qh:
            rev = (r['revenue'] or 0)/1e6
            ebit = (r['ebit'] or 0)/1e6
            ni = (r['net_income'] or 0)/1e6
            em = (r['ebit_margin'] or 0)*100
            dbt = (r['debt_total'] or 0)/1e6
            fcf = (r['fcf_proxy'] or 0)/1e6
            lines.append(f"  {r['period_end']}: rev={rev:.1f} ebit={ebit:.1f} ni={ni:.1f} em%={em:.1f} debt={dbt:.0f} fcf={fcf:.1f}")

    if th:
        lines.append(f"\nTHESIS HEALTH: score={th['thesis_score']}/100  contradictions={th['contradictions']}  risk_flags={th['risk_flags']}  regime_shift={th['regime_shift']}")

    if th_text:
        lines.append(f"\nVAULT THESIS:\n{th_text[:800]}")

    # Phase K — Tavily recent news para personas reagirem a eventos materiais
    if news:
        lines.append("\nRECENT MATERIAL NEWS (last 14d via Tavily):")
        for n in news:
            pub = f" [{n['published'][:10]}]" if n.get("published") else ""
            lines.append(f"  - {n['title']}{pub}")
            if n.get("content"):
                lines.append(f"    {n['content'][:200]}")

    return "\n".join(lines)


def ask_persona(
    persona_key: str,
    ticker: str,
    context: str,
    timeout: int = 120,
    *,
    seed: int | None = 42,
) -> dict:
    persona = PERSONAS[persona_key]
    prompt = f"""{persona['framework']}

CONTEXT:
{context}

TASK: Avalia este ticker pelo teu framework. Responde como {persona['name']} faria. Output ESTRUTURADO em JSON apenas (sem markdown):

{{
  "verdict": "BUY" | "HOLD" | "AVOID",
  "conviction": 1-10,
  "rationale": ["razão 1 (max 25 palavras)", "razão 2", "razão 3"],
  "key_risk": "o ÚNICO risk que importa para mim (max 30 palavras)",
  "would_size": "small | medium | large | none — proporção típica do meu book"
}}

Reply JSON ONLY."""

    from agents._llm import ollama_call
    raw = ollama_call(
        prompt,
        model=MODEL,
        max_tokens=500,
        temperature=0.15,
        seed=seed,
        timeout=timeout,
    )
    if raw.startswith("[LLM FAILED"):
        return {"_error": raw}
    import re as _re
    m = _re.search(r"\{.*\}", raw, _re.DOTALL)
    if not m:
        return {"_error": "no_json", "raw": raw[:300]}
    text = m.group(0)
    text = _re.sub(r",\s*}", "}", text)
    text = _re.sub(r",\s*]", "]", text)
    try:
        data = json.loads(text)
        data["persona"] = persona["name"]
        return data
    except json.JSONDecodeError as e:
        return {"_error": str(e), "raw": raw[:500]}


def ask_persona_majority(
    persona_key: str,
    ticker: str,
    context: str,
    timeout: int = 120,
    n: int = 3,
) -> dict:
    """Run ask_persona N times with different seeds, take majority verdict.
    Reduces single-run variance. N=3 is the sweet spot (3× cost, fixes most flips).
    Conviction = mean of conviction scores from runs that match the majority verdict.
    Returns shape compatible with ask_persona (single dict).
    """
    SEEDS = [42, 137, 314, 271, 1729][:max(1, n)]
    runs = []
    for s in SEEDS:
        d = ask_persona(persona_key, ticker, context, timeout=timeout, seed=s)
        if "_error" not in d and d.get("verdict"):
            runs.append(d)
    if not runs:
        return {"_error": "all_runs_failed", "persona": PERSONAS[persona_key]["name"],
                "majority_runs_attempted": n}
    verdicts = [r["verdict"].upper() for r in runs]
    counts = {v: verdicts.count(v) for v in set(verdicts)}
    winner = max(counts, key=counts.get)
    winners = [r for r in runs if r["verdict"].upper() == winner]
    # Conviction: mean of winning runs (rounded to int)
    convictions = [r.get("conviction", 5) for r in winners
                   if isinstance(r.get("conviction"), (int, float))]
    avg_conv = round(sum(convictions) / len(convictions)) if convictions else 5
    base = winners[0].copy()
    base["conviction"] = avg_conv
    base["majority_n"] = len(runs)
    base["majority_winner_count"] = counts[winner]
    base["majority_distribution"] = counts
    # Note rationale only from first winner — full set in details if needed.
    return base


def synthesize(ticker: str, debates: list[dict]) -> dict:
    """Aggregate verdicts + find consensus/dissent."""
    valid = [d for d in debates if "_error" not in d and d.get("verdict")]
    if not valid:
        return {"committee_verdict": "NO_CONSENSUS", "reason": "all personas failed"}

    counts = {"BUY": 0, "HOLD": 0, "AVOID": 0}
    convictions = {"BUY": [], "HOLD": [], "AVOID": []}
    for d in valid:
        v = d.get("verdict", "HOLD").upper()
        if v in counts:
            counts[v] += 1
            convictions[v].append(d.get("conviction", 5))

    n = sum(counts.values())
    majority = max(counts.items(), key=lambda x: x[1])
    consensus_pct = majority[1] / n if n else 0

    if consensus_pct >= 0.6:
        verdict = majority[0]
        confidence = "high" if consensus_pct >= 0.8 else "medium"
    else:
        verdict = "MIXED"
        confidence = "low"

    avg_conv = sum(convictions[majority[0]]) / max(len(convictions[majority[0]]), 1)

    return {
        "committee_verdict": verdict,
        "confidence": confidence,
        "consensus_pct": round(consensus_pct * 100, 0),
        "votes": counts,
        "avg_conviction_majority": round(avg_conv, 1),
        "panel_size": n,
        "panel_failed": len(debates) - n,
    }


def write_markdown(ticker: str, market: str, context: str, debates: list[dict],
                   summary: dict) -> Path:
    out_path = TICKERS_DIR / f"{ticker}_IC_DEBATE.md"
    lines = [
        "---",
        f"type: synthetic_ic_debate",
        f"ticker: {ticker}",
        f"market: {market}",
        f"date: {date.today().isoformat()}",
        f"committee_verdict: {summary['committee_verdict']}",
        f"confidence: {summary.get('confidence', '?')}",
        f"consensus_pct: {summary.get('consensus_pct', 0)}",
        "tags: [synthetic_ic, debate, multi_persona]",
        "---",
        "",
        f"# 🏛️ Synthetic IC Debate — {ticker}",
        "",
        f"**Committee verdict**: **{summary['committee_verdict']}** ({summary.get('confidence', '?')} confidence, "
        f"{summary.get('consensus_pct', 0):.0f}% consensus)  ",
        f"**Votes**: BUY={summary.get('votes',{}).get('BUY',0)} | HOLD={summary.get('votes',{}).get('HOLD',0)} | AVOID={summary.get('votes',{}).get('AVOID',0)}  ",
        f"**Avg conviction majority**: {summary.get('avg_conviction_majority', 0):.1f}/10  ",
        f"**Panel**: {summary.get('panel_size', 0)} personas (failed: {summary.get('panel_failed', 0)})",
        "",
        "## 🗣️ Each persona's verdict",
        "",
    ]

    for d in debates:
        if "_error" in d:
            lines.append(f"### ❌ {d.get('persona', '?')}\n_(failed: {d['_error']})_\n")
            continue
        emoji = {"BUY": "🟢", "HOLD": "🟡", "AVOID": "🔴"}.get(d.get("verdict", ""), "⚪")
        lines.append(f"### {emoji} {d.get('persona', '?')} — **{d.get('verdict', '?')}** (conv {d.get('conviction', '?')}/10, size: {d.get('would_size', '?')})")
        lines.append("")
        lines.append("**Rationale**:")
        for r in (d.get("rationale") or []):
            lines.append(f"- {r}")
        if d.get("key_risk"):
            lines.append(f"\n**Key risk**: {d['key_risk']}")
        lines.append("")

    lines.append("## 📊 Context provided")
    lines.append("")
    lines.append("```")
    lines.append(context[:2000])
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append(f"*100% Ollama local ({MODEL}). Zero Claude tokens. {len(PERSONAS)} personas debated.*")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def run_debate(ticker: str, market: str, verbose: bool = True, *, majority: int = 1) -> dict:
    if verbose:
        print(f"\n=== Synthetic IC: {market.upper()}:{ticker} ===")
    context = build_context(ticker, market)
    debates = []
    t0 = time.time()
    for key in PERSONAS:
        if verbose:
            tag = f" (majority N={majority})" if majority > 1 else ""
            print(f"  asking {PERSONAS[key]['name']}{tag}...", end=" ", flush=True)
        if majority > 1:
            d = ask_persona_majority(key, ticker, context, n=majority)
        else:
            d = ask_persona(key, ticker, context)
        debates.append(d)
        if verbose:
            if "_error" in d:
                print(f"FAIL ({d['_error']})")
            else:
                m_tag = ""
                if "majority_winner_count" in d:
                    m_tag = f" [{d['majority_winner_count']}/{d['majority_n']}]"
                print(f"{d.get('verdict','?')} (conv {d.get('conviction','?')}){m_tag}")
    summary = synthesize(ticker, debates)
    md_path = write_markdown(ticker, market, context, debates, summary)
    elapsed = time.time() - t0
    if verbose:
        print(f"  -> committee: {summary['committee_verdict']} ({summary.get('confidence','?')})  saved: {md_path.relative_to(ROOT)}  ({elapsed:.1f}s)")
    return {"ticker": ticker, "market": market, **summary, "elapsed_sec": elapsed}


def _holdings(market: str) -> list[str]:
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        return [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()]


def _watchlist(market: str) -> list[str]:
    """Tickers em companies (excl. holdings) — usa is_holding=0 ou NOT IN portfolio_positions."""
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        return [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM companies "
            "WHERE COALESCE(is_holding, 0) = 0"
        ).fetchall()]


def _existing_ic_tickers() -> set[str]:
    """Tickers que já têm IC_DEBATE.md — para skip resumability."""
    return {p.name.replace("_IC_DEBATE.md", "")
            for p in TICKERS_DIR.glob("*_IC_DEBATE.md")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--market", choices=["br", "us"], default=None)
    ap.add_argument("--all-holdings", action="store_true")
    ap.add_argument("--watchlist", action="store_true",
                    help="Run debate para todo o watchlist (companies is_holding=0)")
    ap.add_argument("--all", action="store_true",
                    help="Holdings + watchlist (universe-wide)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Pula tickers que já têm <TICKER>_IC_DEBATE.md")
    ap.add_argument("--limit", type=int, default=None,
                    help="Máximo de tickers a processar nesta run")
    ap.add_argument("--majority", type=int, default=1,
                    help="Run cada persona N vezes com seeds diferentes; "
                         "verdict por maioria. N=3 fixa flips ~85%% por 3× custo.")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.all_holdings or args.watchlist or args.all:
        targets: list[tuple[str, str]] = []
        for market in ("br", "us"):
            if args.all_holdings or args.all:
                for t in _holdings(market):
                    targets.append((t, market))
            if args.watchlist or args.all:
                for t in _watchlist(market):
                    targets.append((t, market))
        # dedup mantendo ordem
        seen: set[tuple[str, str]] = set()
        deduped: list[tuple[str, str]] = []
        for tup in targets:
            if tup not in seen:
                seen.add(tup)
                deduped.append(tup)
        targets = deduped
        if args.skip_existing:
            existing = _existing_ic_tickers()
            targets = [(t, m) for t, m in targets if t not in existing]
            print(f"[skip-existing] {len(existing)} já existem; restam {len(targets)} a processar")
        if args.limit:
            targets = targets[: args.limit]
        results = []
        for t, market in targets:
            try:
                results.append(run_debate(t, market, majority=args.majority))
            except Exception as e:
                print(f"  !! {market}:{t} crashed: {e}")
        # summary
        print(f"\n=== Summary {len(results)} tickers debated ===")
        for r in results:
            print(f"  {r['market'].upper()}:{r['ticker']:<8} -> {r['committee_verdict']:<10} ({r.get('confidence','?')})  {r.get('consensus_pct',0):.0f}%")
    elif args.ticker:
        # detect market
        market = args.market
        if not market:
            for m in ("br", "us"):
                if args.ticker.upper() in _holdings(m):
                    market = m
                    break
            market = market or "us"
        run_debate(args.ticker.upper(), market, majority=args.majority)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
