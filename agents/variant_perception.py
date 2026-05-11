"""Variant Perception scanner — onde a nossa thesis diverge do consenso analyst.

Inspirado em "Variant perception scanner" da lista do user.

Para cada holding com ## Thesis no vault E pelo menos 1 analyst_insight recente:
  1. Pull thesis stance (extracted via simple keywords: bullish/bearish/neutral)
  2. Pull analyst_insights consensus (last 90 days, by stance)
  3. Compute divergence score:
       - Thesis bullish + Analysts majority bear → high variance LONG (we see something market misses)
       - Thesis bullish + Analysts majority bull → low variance (consensus, no edge)
       - Thesis bearish + Analysts majority bull → high variance SHORT
  4. For high-variance positions, ask Ollama: "what specific divergence is most relevant"
  5. Output: obsidian_vault/tickers/<TICKER>_VARIANT.md

100% local. Edge identification = where you disagree with the crowd, with evidence.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"

MODEL = "qwen2.5:14b-instruct-q4_K_M"

BULLISH_HINTS = ["compounder", "long-term hold", "drip", "quality", "moat", "buffett", "buy",
                 "accumulate", "convicção", "convicted", "favorit", "winner", "best-in-class"]
BEARISH_HINTS = ["avoid", "trim", "exit", "sell", "broken", "deteriorat", "concern", "risk",
                 "sair", "reduzir", "vender", "preocup", "venda", "trim"]


def _classify_thesis_stance(thesis_text: str) -> str:
    """Stance classifier — looks ONLY at Core thesis paragraph (not triggers).

    The "Disconfirmation triggers" section contains bearish keywords by design
    (it lists when to exit). We must not count those — they are the inverse signal.
    """
    if not thesis_text:
        return "unknown"

    # Extract only the Core thesis paragraph + Intent
    import re
    core_match = re.search(r"\*\*Core thesis[^*]*\*\*:?\s*(.+?)(?=\n\n|\n\*\*|$)",
                           thesis_text, re.DOTALL)
    intent_match = re.search(r"\*\*Intent\*\*:?\s*(.+?)(?=\n|$)", thesis_text)

    pieces = []
    if core_match:
        pieces.append(core_match.group(1))
    if intent_match:
        pieces.append(intent_match.group(1))
    # If neither marker found, fall back to first 600 chars (likely the core)
    if not pieces:
        pieces.append(thesis_text[:600])

    t = "\n".join(pieces).lower()
    # Word-boundary match — "trim" must NOT match "patrimonial", "risk" must NOT match "asterisko"
    import re
    def _wb_count(word: str, text: str) -> int:
        return len(re.findall(r"\b" + re.escape(word) + r"\b", text))
    bull = sum(_wb_count(h, t) for h in BULLISH_HINTS)
    bear = sum(_wb_count(h, t) for h in BEARISH_HINTS)

    # Default-long bias: if user holds it, probably bullish unless Core says otherwise
    if bull > 0 and bear == 0:
        return "bullish"
    if bull > bear * 1.5:
        return "bullish"
    if bear > bull * 1.5:
        return "bearish"
    if bull == 0 and bear == 0:
        return "neutral"   # (was "unknown" — but if there IS a thesis, default neutral)
    return "neutral"


def _vault_thesis(ticker: str) -> str | None:
    """Thin wrapper — canonical impl lives in agents._common.read_vault_thesis.

    This module previously held the source-of-truth (bug-fix 2026-04-27 to
    cover numbered '## N. Thesis' in DOSSIE.md files). Migrated to shared
    module Phase Cleanup 2026-04-27 to deduplicate across synthetic_ic,
    earnings_prep, ab_qwen3_vs_14b.
    """
    from agents._common import read_vault_thesis
    return read_vault_thesis(ticker, max_chars=None)


def _source_weights(market: str, min_closed: int = 5) -> dict[str, float]:
    """Compute weight per source based on closed predictions' win_rate.

    Returns dict {source: weight}. Weight is win_rate when closed >= min_closed,
    else 0.5 (neutral fallback — source has no track record yet).

    Phase G wired predictions infra; first closures expected Jul 2026.
    Until then all weights = 0.5 → degrades to uniform weighting (no behaviour change).
    """
    db = DBS[market]
    if not db.exists():
        return {}
    weights: dict[str, float] = {}
    with sqlite3.connect(db) as c:
        rows = c.execute(
            """
            SELECT REPLACE(source, 'analyst:', '') AS src,
                   SUM(CASE WHEN outcome='win' THEN 1 ELSE 0 END) AS wins,
                   SUM(CASE WHEN outcome IN ('win','loss') THEN 1 ELSE 0 END) AS closed
            FROM predictions
            GROUP BY src
            """
        ).fetchall()
    for src, wins, closed in rows:
        if closed and closed >= min_closed:
            weights[src] = (wins or 0) / closed
        else:
            weights[src] = 0.5
    return weights


def _analyst_consensus(market: str, ticker: str, days: int = 90) -> dict:
    db = DBS[market]
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    counts = {"bull": 0, "bear": 0, "neutral": 0, "unspecified": 0}
    weighted = {"bull": 0.0, "bear": 0.0, "neutral": 0.0}
    weights_used: dict[str, float] = {}  # source → weight applied to its votes
    insights = []
    src_weights = _source_weights(market)
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """
            SELECT ai.stance, ai.claim, ai.kind, ai.price_target, ai.evidence_quote,
                   ai.created_at, ar.source
            FROM analyst_insights ai
            LEFT JOIN analyst_reports ar ON ai.report_id = ar.id
            WHERE ai.ticker = ? AND ai.created_at >= ?
            ORDER BY ai.created_at DESC LIMIT 30
            """,
            (ticker, cutoff),
        ).fetchall()
        for r in rows:
            stance = (r["stance"] or "").lower().strip()
            src = (r["source"] or "unknown").lower()
            w = src_weights.get(src, 0.5)
            weights_used[src] = w
            if stance in ("bull", "bullish", "buy"):
                counts["bull"] += 1
                weighted["bull"] += w
            elif stance in ("bear", "bearish", "sell"):
                counts["bear"] += 1
                weighted["bear"] += w
            elif stance in ("neutral", "hold"):
                counts["neutral"] += 1
                weighted["neutral"] += w
            else:
                counts["unspecified"] += 1
            d = dict(r)
            d["weight"] = w
            insights.append(d)
    n = sum(counts.values())
    if n == 0:
        return {"counts": counts, "n": 0, "insights": [], "consensus": "no_data",
                "weighted_consensus": "no_data", "source_weights": weights_used}
    # Unweighted consensus (legacy)
    n_specified = counts["bull"] + counts["bear"] + counts["neutral"]
    consensus = "no_data"
    if n_specified > 0:
        bull_pct = counts["bull"] / n_specified
        bear_pct = counts["bear"] / n_specified
        if bull_pct >= 0.6:
            consensus = "bullish"
        elif bear_pct >= 0.6:
            consensus = "bearish"
        else:
            consensus = "neutral"
    # Weighted consensus (sources weighted by predictions win_rate)
    w_total = weighted["bull"] + weighted["bear"] + weighted["neutral"]
    weighted_consensus = "no_data"
    weighted_bull_pct = 0.0
    if w_total > 0:
        weighted_bull_pct = weighted["bull"] / w_total
        weighted_bear_pct = weighted["bear"] / w_total
        if weighted_bull_pct >= 0.6:
            weighted_consensus = "bullish"
        elif weighted_bear_pct >= 0.6:
            weighted_consensus = "bearish"
        else:
            weighted_consensus = "neutral"
    return {
        "counts": counts,
        "n": n,
        "insights": insights,
        "consensus": consensus,
        "bull_pct": round(counts["bull"] / max(n_specified, 1) * 100, 1),
        "weighted_consensus": weighted_consensus,
        "weighted_bull_pct": round(weighted_bull_pct * 100, 1),
        "source_weights": weights_used,
    }


_TAVILY_BULL = ["upgrade", "buy", "outperform", "raise target", "strong buy",
                "raised price target", "bullish", "beat estimates", "earnings beat",
                "guidance raised", "raises guidance"]
_TAVILY_BEAR = ["downgrade", "sell", "underperform", "cut target", "lower target",
                "bearish", "miss estimates", "earnings miss", "guidance cut",
                "cuts guidance", "warns", "investigation", "lawsuit", "fraud"]


def _tavily_consensus(ticker: str, market: str) -> dict:
    """Pull web analyst calls/news via Tavily; classify by stance keywords.
    Returns {bull, bear, neutral} counts + top hits. Cache 7d via autoresearch.
    Cost: 1 Tavily call (cached on subsequent runs)."""
    try:
        from agents.autoresearch import search_ticker
        r = search_ticker(ticker, topic="downgrade", market=market, days_back=30)
    except Exception as e:
        return {"available": False, "error": str(e)}
    if r.error or not r.results:
        return {"available": False, "error": r.error, "n": 0,
                "counts": {"bull": 0, "bear": 0, "neutral": 0}}

    counts = {"bull": 0, "bear": 0, "neutral": 0}
    classified_hits: list[dict] = []
    for h in r.results:
        title_lc = (h.title or "").lower()
        content_lc = (h.content or "").lower()[:500]
        text = title_lc + " " + content_lc
        bull_hits = sum(1 for k in _TAVILY_BULL if k in text)
        bear_hits = sum(1 for k in _TAVILY_BEAR if k in text)
        if bull_hits > bear_hits:
            stance = "bull"
        elif bear_hits > bull_hits:
            stance = "bear"
        else:
            stance = "neutral"
        counts[stance] += 1
        classified_hits.append({
            "title": h.title[:120], "url": h.url, "stance": stance,
            "score": h.score, "published": h.published_date,
        })

    n = sum(counts.values())
    if n == 0:
        consensus_label = "no_data"
    else:
        bull_pct = counts["bull"] / n
        bear_pct = counts["bear"] / n
        if bull_pct >= 0.6:
            consensus_label = "bullish"
        elif bear_pct >= 0.6:
            consensus_label = "bearish"
        else:
            consensus_label = "neutral"
    return {
        "available": True,
        "cached": r.cached,
        "n": n,
        "counts": counts,
        "consensus": consensus_label,
        "bull_pct": round(counts["bull"] / max(n, 1) * 100, 1),
        "hits": classified_hits[:5],
    }


def compute_variance(thesis_stance: str, consensus: str) -> dict:
    """Return variance type + magnitude."""
    if thesis_stance == "unknown" or consensus == "no_data":
        return {"variance": "unmeasurable", "magnitude": 0,
                "interpretation": "missing thesis or no analyst data"}
    matrix = {
        ("bullish", "bullish"): ("low_consensus_long", 1, "consensus pick — no edge"),
        ("bullish", "bearish"): ("HIGH_VARIANCE_LONG", 5, "we see something market misses (or wrong)"),
        ("bullish", "neutral"): ("medium_variance_long", 2, "moderate edge"),
        ("bearish", "bullish"): ("HIGH_VARIANCE_SHORT", 5, "contrarian sell — strong conviction needed"),
        ("bearish", "bearish"): ("low_consensus_short", 1, "consensus avoid — overcrowded"),
        ("bearish", "neutral"): ("medium_variance_short", 2, "moderate caution edge"),
        ("neutral", "bullish"): ("missing_upside", 2, "we lack conviction; market does"),
        ("neutral", "bearish"): ("missing_downside", 2, "we lack conviction; market is negative"),
        ("neutral", "neutral"): ("aligned_neutral", 0, "no edge, no risk"),
    }
    label, mag, interp = matrix.get((thesis_stance, consensus), ("unknown", 0, ""))
    return {"variance": label, "magnitude": mag, "interpretation": interp}


def ask_specific_divergence(ticker: str, our_thesis: str, analyst_claims: list[str],
                            timeout: int = 90) -> str | None:
    if not analyst_claims:
        return None
    prompt = f"""Investidor pessoal tem esta thesis:

NOSSA THESIS ({ticker}):
{our_thesis[:1200]}

CONSENSO ANALYSTS (recente):
{chr(10).join(f'- {c[:200]}' for c in analyst_claims[:5])}

TAREFA: Identifica em 3 frases concisas (PT) onde a NOSSA thesis DIVERGE do consenso.
- Se concordamos: diz "alinhado" + razão.
- Se divergimos: diz EXACTAMENTE o ponto contestado + qual lado tem evidência mais robusta.

Reply só o texto da análise, sem JSON."""
    from agents._llm import ollama_call
    raw = ollama_call(
        prompt,
        model=MODEL,
        max_tokens=300,
        temperature=0.3,
        timeout=timeout,
    )
    if raw.startswith("[LLM FAILED"):
        return f"(error: {raw})"
    return raw[:1200]


def scan_ticker(ticker: str, market: str, verbose: bool = True,
                use_weighted: bool = True, use_tavily: bool = True) -> dict:
    thesis = _vault_thesis(ticker)
    thesis_stance = _classify_thesis_stance(thesis or "")
    cons = _analyst_consensus(market, ticker)
    # Prefer weighted consensus when available; falls back to raw if not.
    chosen_consensus = (cons.get("weighted_consensus") if use_weighted
                        else cons.get("consensus")) or cons.get("consensus", "no_data")

    # Tavily web consensus (Phase K) — complementa quando DB analyst coverage é fraca.
    # Gating: só chama Tavily quando DB tem < 3 insights (evita queimar quota desnecessariamente).
    tavily_data = {"available": False, "skipped": "use_tavily=False"}
    if use_tavily and cons["n"] < 3:
        tavily_data = _tavily_consensus(ticker, market)
        if tavily_data.get("available") and tavily_data.get("n", 0) >= 3:
            # Tavily preenche o gap — sobrepõe consensus quando DB é insufficient
            if chosen_consensus == "no_data":
                chosen_consensus = tavily_data["consensus"]

    variance = compute_variance(thesis_stance, chosen_consensus)
    # Track if weighted vs raw differ — useful signal of source-skew
    weight_skew = (cons.get("consensus") != cons.get("weighted_consensus")
                   and cons.get("weighted_consensus") not in (None, "no_data"))

    divergence_text = None
    if variance["magnitude"] >= 2 and cons["insights"]:
        claims = [i.get("claim", "") for i in cons["insights"][:5]]
        divergence_text = ask_specific_divergence(ticker, thesis or "", claims)

    result = {
        "ticker": ticker,
        "market": market,
        "thesis_stance": thesis_stance,
        "analyst_consensus": cons["consensus"],
        "weighted_consensus": cons.get("weighted_consensus", "no_data"),
        "analyst_n": cons["n"],
        "analyst_bull_pct": cons.get("bull_pct", 0),
        "weighted_bull_pct": cons.get("weighted_bull_pct", 0),
        "weight_skew": weight_skew,
        "source_weights": cons.get("source_weights", {}),
        "tavily": tavily_data,
        "variance": variance,
        "divergence_summary": divergence_text,
    }

    # Markdown
    if thesis or cons["n"] > 0:
        out = TICKERS_DIR / f"{ticker}_VARIANT.md"
        weighted_line = ""
        if cons.get("weighted_consensus") not in (None, "no_data"):
            weighted_line = (f"**Weighted consensus** (source win-rate weighted): "
                             f"{cons['weighted_consensus']} ({cons.get('weighted_bull_pct',0):.0f}% bull)  ")
        lines = [
            "---",
            f"type: variant_perception",
            f"ticker: {ticker}",
            f"market: {market}",
            f"date: {date.today().isoformat()}",
            f"variance: {variance['variance']}",
            f"magnitude: {variance['magnitude']}",
            f"weight_skew: {weight_skew}",
            "tags: [variant_perception, edge_detection]",
            "---",
            "",
            f"# 🎯 Variant Perception — {ticker}",
            "",
            f"**Our stance**: {thesis_stance}  ",
            f"**Analyst consensus** ({cons['n']} insights, last 90d): {cons['consensus']} ({cons.get('bull_pct',0):.0f}% bull)  ",
            *( [weighted_line] if weighted_line else [] ),
            f"**Variance type**: `{variance['variance']}` (magnitude {variance['magnitude']}/5)  ",
            f"**Interpretation**: {variance['interpretation']}",
            "",
        ]
        if variance["magnitude"] >= 4:
            lines.append("> 🚨 **HIGH VARIANCE — potential edge OR potential mistake**")
            lines.append("")
        if weight_skew:
            lines.append("> ⚖️ **Source weighting changed verdict** — raw vs win-rate-weighted consensus differ. Inspect source_weights.")
            lines.append("")
        if divergence_text:
            lines.append("## 🔍 Specific divergence analysis")
            lines.append("")
            lines.append(divergence_text)
            lines.append("")
        if cons["insights"]:
            lines.append("## 📰 Recent analyst insights")
            lines.append("")
            for ins in cons["insights"][:8]:
                stance = ins.get("stance") or "?"
                src = ins.get("source") or "?"
                w = ins.get("weight", 0.5)
                lines.append(f"- [{stance}] *{src} (w={w:.2f})* {ins.get('claim', '')[:150]}")
            lines.append("")
        # Phase K — Tavily web consensus (complementa DB analyst_insights)
        if tavily_data.get("available") and tavily_data.get("n", 0) > 0:
            lines.append("## 🌐 Tavily web consensus (last 30d)")
            lines.append("")
            counts = tavily_data["counts"]
            lines.append(f"**Web stance**: {tavily_data['consensus']} "
                         f"({counts['bull']} bull / {counts['bear']} bear / {counts['neutral']} neutral)  ")
            lines.append(f"**Cached**: {tavily_data.get('cached', False)}")
            lines.append("")
            for h in tavily_data["hits"][:5]:
                emoji = "🟢" if h["stance"] == "bull" else ("🔴" if h["stance"] == "bear" else "🟡")
                pub = f" ({h['published'][:10]})" if h.get("published") else ""
                lines.append(f"- {emoji} [{h['stance']}] [{h['title']}]({h['url']}){pub}")
            lines.append("")
        if cons.get("source_weights"):
            lines.append("## ⚖️ Source weights (predictions win-rate)")
            lines.append("")
            for src, w in sorted(cons["source_weights"].items(),
                                 key=lambda x: x[1], reverse=True):
                badge = "📊" if abs(w - 0.5) < 0.001 else ("✅" if w >= 0.55 else "⚠️")
                note = " *(no track record yet)*" if abs(w - 0.5) < 0.001 else ""
                lines.append(f"- {badge} `{src}` → {w:.2f}{note}")
            lines.append("")
        if thesis:
            lines.append("## 📜 Our thesis")
            lines.append("")
            lines.append(thesis[:800])
            lines.append("")
        lines.append("---")
        lines.append(f"*100% Ollama local. Variant perception scan.*")
        out.write_text("\n".join(lines), encoding="utf-8")

    if verbose:
        print(f"  {market.upper()}:{ticker:<8}  ours={thesis_stance:<10} consenso={cons['consensus']:<10}  "
              f"variance={variance['variance']:<22} mag={variance['magnitude']}")
    return result


def _holdings(market: str) -> list[str]:
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        return [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--all-holdings", action="store_true")
    ap.add_argument("--no-weighting", action="store_true",
                    help="Disable source-weighting (uniform consensus, legacy mode for A/B)")
    args = ap.parse_args()
    use_weighted = not args.no_weighting
    sys.stdout.reconfigure(encoding="utf-8")

    if args.all_holdings:
        results = []
        print(f"=== Variant Perception scan — all holdings (weighted={use_weighted}) ===")
        for market in ("br", "us"):
            for t in _holdings(market):
                results.append(scan_ticker(t, market, use_weighted=use_weighted))
        # summary
        high = [r for r in results if r["variance"]["magnitude"] >= 4]
        med = [r for r in results if r["variance"]["magnitude"] in (2, 3)]
        print(f"\n=== Summary ===")
        print(f"  HIGH variance ({len(high)}):")
        for r in high:
            print(f"    {r['market'].upper()}:{r['ticker']:<8} {r['variance']['variance']}")
        print(f"  Medium variance: {len(med)}")
        print(f"  Low/aligned: {len(results) - len(high) - len(med)}")
    elif args.ticker:
        market = args.market
        if not market:
            for m in ("br", "us"):
                if args.ticker.upper() in _holdings(m):
                    market = m; break
            market = market or "us"
        scan_ticker(args.ticker.upper(), market, use_weighted=use_weighted)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
