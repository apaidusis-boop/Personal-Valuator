"""auto_verdict_on_content — flag verdict mismatch from new content.

Pattern: cron-friendly hook, complementa `auto_verdict_on_filing` (que
reage a CVM/SEC filings). Aqui reagimos a CONTEÚDO — quando ≥2 fontes
profissionais (analyst_reports + YouTube + Podcast) das últimas 24h
contradizem o verdict actual de um ticker.

Trigger criteria (todos têm de bater):
  1. Verdict actual existe (verdict_history row recente).
  2. ≥2 insights distintos (de fontes diferentes) com stance/kind oposto
     ao verdict actual.
  3. Confidence média ≥0.70 nos insights opostos.

Action stance ↔ insight stance gap matrix:
  BUY_*   ↔  thesis_bear|risk(high conf)|valuation(stance=bear)  → DISAGREE
  AVOID|SELL  ↔  thesis_bull|catalyst|guidance(stance=bull)      → DISAGREE
  HOLD ↔ qualquer extremo (≥3 fontes mesmo lado)                 → DISAGREE

Output:
  - obsidian_vault/dossiers/<TK>_CONTENT_TRIGGER_<DATE>.md (one per ticker/day)
  - verdict_delta row com triggered_by="content:multi"
  - watchlist_actions row (kind="content_trigger") para surfacing em MC /alerts

Idempotência:
  - dossier path é determinístico (TK + date) — overwrite OK.
  - watchlist_actions tem unique key (ticker, kind, created_date) — skip.

Uso:
    python scripts/auto_verdict_on_content.py
    python scripts/auto_verdict_on_content.py --hours 48 --min-sources 2
    python scripts/auto_verdict_on_content.py --ticker BBDC4
    python scripts/auto_verdict_on_content.py --dry-run
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
DOSSIER_DIR = ROOT / "obsidian_vault" / "dossiers"
LOG_FILE = ROOT / "logs" / "auto_verdict_content.log"

# Insight kinds → polarity (-1=bear, 0=neutral, +1=bull)
KIND_POLARITY = {
    "thesis_bull": +1, "catalyst": +1, "guidance": +0.5, "operational": +0.3,
    "thesis_bear": -1, "risk": -0.7, "balance_sheet": -0.4,
    "valuation": 0.0,  # depends on stance/PT — handled separately
    "dividend": +0.4, "management": 0.0, "capex": -0.2,
}

# Verdict action → polarity
ACTION_POLARITY = {
    "BUY": +1, "STRONG_BUY": +1, "BUY_GROWTH": +0.7, "ACCUMULATE": +0.7,
    "HOLD": 0.0, "WATCH": 0.0, "NEUTRAL": 0.0,
    "AVOID": -0.7, "REDUCE": -0.7, "SELL": -1, "STRONG_SELL": -1,
}

# Trigger threshold: how much disagreement is needed
DISAGREEMENT_THRESHOLD = 0.8  # |verdict_polarity - insights_polarity| >= 0.8
MIN_SOURCES = 2
MIN_AVG_CONFIDENCE = 0.70


def _log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(UTC).isoformat(timespec='seconds')} {msg}\n")


def _ensure_schema(db: Path) -> None:
    """verdict_delta is created here; watchlist_actions is owned by trigger_monitor
    (canonical schema with market, trigger_id, opened_at, notes)."""
    with sqlite3.connect(db) as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS verdict_delta (
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            prior_action TEXT,
            new_action TEXT NOT NULL,
            prior_score REAL,
            new_score REAL,
            triggered_by TEXT,
            triggered_url TEXT,
            computed_at TEXT NOT NULL,
            PRIMARY KEY (ticker, date, triggered_by)
        );
        """)


def _current_verdict(market: str, ticker: str) -> dict | None:
    db = DB_BR if market == "br" else DB_US
    try:
        with sqlite3.connect(db) as c:
            r = c.execute(
                """SELECT action, total_score, date FROM verdict_history
                   WHERE ticker=? ORDER BY date DESC LIMIT 1""",
                (ticker,),
            ).fetchone()
    except sqlite3.OperationalError:
        return None
    return {"action": r[0], "score": r[1], "date": r[2]} if r else None


def _new_insights(market: str, hours: int, ticker_filter: str | None = None) -> dict:
    """Devolve dict {ticker: [insights...]} dos last N hours."""
    db = DB_BR if market == "br" else DB_US
    cutoff = (datetime.now(UTC) - timedelta(hours=hours)).date().isoformat()
    by_ticker: dict[str, list[dict]] = defaultdict(list)

    if not db.exists():
        return by_ticker

    try:
        with sqlite3.connect(db) as c:
            # Video insights (YouTube + Podcast)
            params = [cutoff]
            extra = ""
            if ticker_filter:
                extra = " AND i.ticker=?"
                params.append(ticker_filter)
            for row in c.execute(f"""
                SELECT i.ticker, i.kind, i.claim, i.confidence, v.channel, v.published_at
                FROM video_insights i
                LEFT JOIN videos v ON i.video_id = v.video_id
                WHERE COALESCE(v.published_at, i.created_at) >= ?{extra}
            """, params).fetchall():
                tk, kind, claim, conf, ch, pub = row
                by_ticker[tk].append({
                    "source_type": "video",
                    "source": ch or "?",
                    "kind": kind, "stance": None,
                    "claim": claim, "confidence": conf or 0.0,
                    "date": (pub or cutoff)[:10],
                })

            # Analyst insights (subscriptions)
            params = [cutoff]
            extra = ""
            if ticker_filter:
                extra = " AND ai.ticker=?"
                params.append(ticker_filter)
            for row in c.execute(f"""
                SELECT ai.ticker, ai.kind, ai.claim, ai.stance, ai.confidence,
                       r.source, r.published_at
                FROM analyst_insights ai
                JOIN analyst_reports r ON ai.report_id = r.id
                WHERE r.published_at >= ?{extra}
            """, params).fetchall():
                tk, kind, claim, stance, conf, src, pub = row
                by_ticker[tk].append({
                    "source_type": "analyst",
                    "source": (src or "?").upper(),
                    "kind": kind, "stance": stance,
                    "claim": claim, "confidence": conf or 0.65,
                    "date": (pub or cutoff)[:10],
                })
    except sqlite3.OperationalError:
        return by_ticker
    return by_ticker


def _polarity(insight: dict) -> float:
    """Map a single insight to [-1, +1] polarity."""
    stance = (insight.get("stance") or "").lower()
    if stance in ("bullish", "bull", "positive"):
        return +0.8
    if stance in ("bearish", "bear", "negative"):
        return -0.8
    kind_pol = KIND_POLARITY.get(insight.get("kind"), 0.0)
    return kind_pol


def _aggregate_polarity(insights: list[dict]) -> tuple[float, float, int]:
    """Returns (weighted_polarity, avg_confidence, n_distinct_sources)."""
    if not insights:
        return 0.0, 0.0, 0
    total_w = 0.0
    weighted = 0.0
    confs = []
    sources = set()
    for ins in insights:
        conf = float(ins.get("confidence") or 0.5)
        pol = _polarity(ins)
        weighted += pol * conf
        total_w += conf
        confs.append(conf)
        sources.add(ins["source"])
    return (weighted / total_w if total_w else 0.0,
            sum(confs) / len(confs),
            len(sources))


def evaluate_ticker(market: str, ticker: str, insights: list[dict],
                    min_sources: int, threshold: float, min_conf: float) -> dict | None:
    """If ticker has disagreement → return decision dict; else None."""
    if not insights:
        return None
    verdict = _current_verdict(market, ticker)
    if not verdict:
        return None  # no baseline to disagree with

    pol_v = ACTION_POLARITY.get((verdict.get("action") or "").upper(), 0.0)

    # Filter to insights with non-zero polarity (signal)
    signal_ins = [i for i in insights if abs(_polarity(i)) >= 0.3]
    if not signal_ins:
        return None

    pol_i, avg_conf, n_src = _aggregate_polarity(signal_ins)
    gap = abs(pol_v - pol_i)

    if n_src < min_sources:
        return None
    if avg_conf < min_conf:
        return None
    if gap < threshold:
        return None

    direction = "MORE_BEARISH" if pol_i < pol_v else "MORE_BULLISH"
    return {
        "ticker": ticker, "market": market,
        "verdict": verdict, "verdict_polarity": pol_v,
        "insights_polarity": pol_i, "gap": gap, "direction": direction,
        "n_sources": n_src, "avg_confidence": avg_conf,
        "n_insights": len(signal_ins), "insights": signal_ins,
    }


def _write_dossier(decision: dict) -> Path:
    DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).date().isoformat()
    out = DOSSIER_DIR / f"{decision['ticker']}_CONTENT_TRIGGER_{today}.md"

    v = decision["verdict"]
    direction_label = {"MORE_BEARISH": "🔴 mais bearish", "MORE_BULLISH": "🟢 mais bullish"}[decision["direction"]]

    lines = [
        f"---",
        f"type: content_trigger",
        f"ticker: {decision['ticker']}",
        f"market: {decision['market']}",
        f"date: {today}",
        f"direction: {decision['direction']}",
        f"gap: {decision['gap']:.2f}",
        f"n_sources: {decision['n_sources']}",
        f"avg_confidence: {decision['avg_confidence']:.2f}",
        f"verdict_actual: {v['action']}",
        f"verdict_score: {v['score']}",
        f"---",
        "",
        f"# {decision['ticker']} — Content Trigger {today}",
        "",
        f"## 🚨 Disagreement detectado",
        "",
        f"O verdict actual `{v['action']}` (score {v['score']}, polaridade "
        f"{decision['verdict_polarity']:+.2f}) contradiz o consenso recente "
        f"de {decision['n_sources']} fontes profissionais.",
        "",
        f"- **Direcção do conflito**: {direction_label}",
        f"- **Gap de polaridade**: `{decision['gap']:.2f}` "
        f"(threshold {DISAGREEMENT_THRESHOLD})",
        f"- **Confiança média insights**: {decision['avg_confidence']:.2f}",
        f"- **Insights opostos**: {decision['n_insights']} (de {decision['n_sources']} fontes distintas)",
        "",
        f"## 🎙️ Insights opostos (últimas 24h)",
        "",
        "| Fonte | Tipo | Kind | Conf | Claim |",
        "|---|---|---|---:|---|",
    ]

    for ins in sorted(decision["insights"], key=lambda i: -i["confidence"])[:15]:
        src = ins["source"][:25].replace("|", "\\|")
        st = ins["source_type"][:8]
        kind = ins["kind"] or "?"
        conf = f"{ins['confidence']:.2f}"
        claim = (ins["claim"] or "")[:140].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {src} | {st} | {kind} | {conf} | {claim} |")

    lines.extend([
        "",
        "## 📊 Recomendação",
        "",
        "**Status**: REVIEW — não acção automática.",
        "",
        "Sugestão de fluxo:",
        f"1. Lê os insights opostos acima e o verdict actual em `tickers/{decision['ticker']}.md`.",
        "2. Se concordas com o consenso recente → `ii decide " + decision['ticker'] + "` para re-rodar engines.",
        "3. Se discordas (e tens conviction) → `ii actions ignore " + decision['ticker'] + " --note 'reason'`.",
        "4. Se quiseres mais sinal antes de decidir → adiciona pergunta a Antonio Carlos via Telegram.",
        "",
        f"## Cross-links",
        "",
        f"- [[tickers/{decision['ticker']}|Ticker page]]",
        f"- [[CONSTITUTION#decision-log]]",
        f"- Triggered by `auto_verdict_on_content.py` em {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
    ])

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def _persist_action(market: str, decision: dict) -> bool:
    """Inserts watchlist_actions row se ainda não existe para hoje.
    Schema canónico vem de trigger_monitor (market, trigger_id, opened_at, notes)."""
    db = DB_BR if market == "br" else DB_US
    today = datetime.now(UTC).date().isoformat()
    note = (f"{decision['direction']} consensus from {decision['n_sources']} sources "
            f"(gap={decision['gap']:.2f}, conf={decision['avg_confidence']:.2f}). "
            f"Verdict actual: {decision['verdict']['action']}.")
    trigger_id = f"content:{decision['ticker']}:{today}"
    with sqlite3.connect(db) as c:
        existing = c.execute(
            """SELECT id FROM watchlist_actions
               WHERE ticker=? AND kind='content_trigger'
                 AND substr(opened_at,1,10)=?
                 AND status='open'""",
            (decision["ticker"], today),
        ).fetchone()
        if existing:
            return False
        c.execute(
            """INSERT INTO watchlist_actions
               (ticker, market, kind, trigger_id, action_hint,
                trigger_snapshot_json, status, opened_at, notes)
               VALUES (?, ?, 'content_trigger', ?, ?, ?, 'open', ?, ?)""",
            (decision["ticker"], market, trigger_id,
             "review" if decision["direction"] == "MORE_BEARISH" else "buy_review",
             None,  # snapshot json — could fill with decision dict later
             datetime.now(UTC).isoformat(timespec="seconds"),
             note),
        )
        c.commit()
    return True


def _persist_delta(market: str, decision: dict) -> None:
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    today = datetime.now(UTC).date().isoformat()
    v = decision["verdict"]
    new_action_proposed = {
        "MORE_BEARISH": "REVIEW_BEARISH",
        "MORE_BULLISH": "REVIEW_BULLISH",
    }[decision["direction"]]
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO verdict_delta
               (ticker, date, prior_action, new_action, prior_score, new_score,
                triggered_by, triggered_url, computed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (decision["ticker"], today, v["action"], new_action_proposed,
             v["score"], None,
             f"content:{decision['n_sources']}_sources",
             None,
             datetime.now(UTC).isoformat(timespec="seconds")),
        )
        c.commit()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--hours", type=int, default=24)
    p.add_argument("--min-sources", type=int, default=MIN_SOURCES)
    p.add_argument("--threshold", type=float, default=DISAGREEMENT_THRESHOLD)
    p.add_argument("--min-confidence", type=float, default=MIN_AVG_CONFIDENCE)
    p.add_argument("--ticker", default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    n_triggered = 0
    n_evaluated = 0
    written: list[Path] = []

    for market in ("br", "us"):
        by_ticker = _new_insights(market, args.hours, args.ticker)
        for ticker, insights in by_ticker.items():
            n_evaluated += 1
            decision = evaluate_ticker(
                market, ticker, insights,
                args.min_sources, args.threshold, args.min_confidence,
            )
            if not decision:
                continue
            n_triggered += 1
            _log(f"TRIGGER {market}/{ticker} dir={decision['direction']} "
                 f"gap={decision['gap']:.2f} n_src={decision['n_sources']} "
                 f"conf={decision['avg_confidence']:.2f}")

            if args.dry_run:
                if not args.quiet:
                    print(f"  [DRY] {ticker:8s} {decision['direction']:13s} "
                          f"gap={decision['gap']:.2f} sources={decision['n_sources']} "
                          f"conf={decision['avg_confidence']:.2f}")
                continue

            try:
                path = _write_dossier(decision)
                written.append(path)
                inserted = _persist_action(market, decision)
                _persist_delta(market, decision)
                if not args.quiet:
                    insert_msg = "+watchlist" if inserted else "(skip dup watchlist)"
                    print(f"  [WRITE] {ticker:8s} {decision['direction']:13s} → "
                          f"{path.name} {insert_msg}")
            except Exception as e:
                _log(f"FAIL {ticker}: {type(e).__name__}: {e}")
                if not args.quiet:
                    print(f"  [FAIL]  {ticker} — {type(e).__name__}: {e}")

    print(f"\nevaluated {n_evaluated} tickers, triggered {n_triggered}, "
          f"wrote {len(written)} dossiers"
          f"{' (dry-run)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
