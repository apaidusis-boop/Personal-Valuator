"""Conviction Scoring Engine — composite quantitativo + qualitativo por holding.

Inspirado em "Conviction scoring engine — ranking quantitativo + qualitativo das posições" do AA cross-tab.

Compõe 5 sub-scores em 1 número 0-100:

1. THESIS_HEALTH (perpetuum_thesis) — qualidade actual da thesis
2. IC_CONSENSUS (synthetic_ic) — convergência das 5 personas (Buffett+Druck+Taleb+Klarman+Dalio)
3. VARIANT_EVIDENCE (variant_perception) — onde temos edge vs consensus analyst
4. DATA_COVERAGE (perpetuum_data) — completeness dos dados que sustentam a tese
5. PAPER_TRADE_TRACK (signals counts) — quantos methods reforçam (proxy quality)

Weights (configuráveis):
    thesis_health: 0.30
    ic_consensus:  0.25
    variant:       0.15
    data_coverage: 0.10
    paper_track:   0.20

Output: conviction_scores table + obsidian_vault/briefings/conviction_ranking_<DATE>.md

100% local. Pure SQL + filesystem. Zero LLM calls.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
BRIEFINGS_DIR = ROOT / "obsidian_vault" / "briefings"

WEIGHTS = {
    "thesis_health":  0.30,
    "ic_consensus":   0.25,
    "variant":        0.15,
    "data_coverage":  0.10,
    "paper_track":    0.20,
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS conviction_scores (
    ticker          TEXT NOT NULL,
    market          TEXT NOT NULL,
    run_date        TEXT NOT NULL,
    composite_score INTEGER NOT NULL,
    thesis_health   INTEGER,
    ic_consensus    INTEGER,
    variant         INTEGER,
    data_coverage   INTEGER,
    paper_track     INTEGER,
    details_json    TEXT,
    PRIMARY KEY (ticker, run_date)
);
CREATE INDEX IF NOT EXISTS idx_conv_score ON conviction_scores(composite_score);
"""


def ensure_schema() -> None:
    with sqlite3.connect(DBS["br"]) as c:
        c.executescript(SCHEMA)
        c.commit()


def _holdings() -> list[tuple[str, str]]:
    out = []
    for market, db in DBS.items():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            for r in c.execute(
                "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
            ):
                out.append((r[0], market))
    return out


def _universe_with_thesis() -> list[tuple[str, str]]:
    """All tickers (holdings + watchlist) com thesis valid (score >= 0).

    Strip CRLF de tickers para evitar poluição de subject_id.
    """
    out = []
    seen: set[tuple[str, str]] = set()
    with sqlite3.connect(DBS["br"]) as c:
        rows = c.execute("""
            SELECT subject_id FROM perpetuum_health
            WHERE perpetuum_name='thesis' AND score >= 0
              AND run_date=(SELECT MAX(run_date) FROM perpetuum_health WHERE perpetuum_name='thesis')
        """).fetchall()
    for (sid,) in rows:
        market, _, ticker = (sid or "").partition(":")
        ticker = ticker.strip()
        if not ticker or not market:
            continue
        key = (ticker, market)
        if key in seen:
            continue
        seen.add(key)
        out.append((ticker, market))
    return out


def _thesis_health(ticker: str, market: str) -> int | None:
    """Latest thesis score. Lê de perpetuum_health (canonical source).
    Returns None se sem score válido (sentinel -1 ou inexistente)."""
    try:
        with sqlite3.connect(DBS["br"]) as c:
            row = c.execute(
                "SELECT score FROM perpetuum_health "
                "WHERE perpetuum_name='thesis' AND subject_id=? "
                "AND score >= 0 ORDER BY run_date DESC LIMIT 1",
                (f"{market}:{ticker}",),
            ).fetchone()
            if row and row[0] >= 0:
                return row[0]
    except sqlite3.OperationalError:
        pass
    # Fallback to legacy thesis_health table (early holdings)
    try:
        with sqlite3.connect(DBS[market]) as c:
            row = c.execute(
                "SELECT thesis_score FROM thesis_health WHERE ticker=? "
                "AND thesis_score >= 0 ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            return row[0] if row else None
    except sqlite3.OperationalError:
        return None


def _ic_consensus(ticker: str) -> int | None:
    """Parse vault/<ticker>_IC_DEBATE.md frontmatter for consensus_pct + verdict."""
    p = TICKERS_DIR / f"{ticker}_IC_DEBATE.md"
    if not p.exists():
        return None
    content = p.read_text(encoding="utf-8", errors="ignore")
    # Parse frontmatter
    m = re.search(r"committee_verdict:\s*(\w+)", content)
    c = re.search(r"consensus_pct:\s*([\d.]+)", content)
    if not m or not c:
        return None
    verdict = m.group(1).upper()
    pct = float(c.group(1))
    # Score: BUY high consensus = 90+, HOLD = 50-70, AVOID/MIXED = lower
    if verdict == "BUY":
        return min(100, int(60 + pct * 0.4))   # 60 base + 0-40 from consensus
    elif verdict == "HOLD":
        return min(80, int(40 + pct * 0.3))    # 40 base + up to 30 (max 70)
    elif verdict == "AVOID":
        return max(10, int(40 - pct * 0.3))    # decreases with consensus
    elif verdict == "MIXED":
        return 50
    return 50


def _variant(ticker: str, market: str) -> int | None:
    """Read variant_perception markdown frontmatter."""
    p = TICKERS_DIR / f"{ticker}_VARIANT.md"
    if not p.exists():
        return None
    content = p.read_text(encoding="utf-8", errors="ignore")
    m_var = re.search(r"variance:\s*(\w+)", content)
    m_mag = re.search(r"magnitude:\s*(\d+)", content)
    if not m_mag:
        return None
    mag = int(m_mag.group(1))
    var = (m_var.group(1) if m_var else "").lower()
    # High-variance LONG = positive edge (good for conviction)
    # High-variance SHORT = potential mistake (bad for conviction)
    # Low/aligned = neutral edge
    if "high_variance_long" in var:
        return 90
    if "medium_variance_long" in var or "missing_upside" in var:
        return 70
    if "low_consensus_long" in var or "aligned_neutral" in var:
        return 60
    if "medium_variance_short" in var or "missing_downside" in var:
        return 40
    if "high_variance_short" in var:
        return 20
    return 50


def _data_coverage(ticker: str, market: str) -> int | None:
    """Read perpetuum_health latest data_coverage score."""
    try:
        with sqlite3.connect(DBS["br"]) as c:
            row = c.execute(
                "SELECT score FROM perpetuum_health "
                "WHERE perpetuum_name='data_coverage' AND subject_id=? "
                "ORDER BY run_date DESC LIMIT 1",
                (f"{market}:{ticker}",),
            ).fetchone()
            return row[0] if row and row[0] >= 0 else None
    except sqlite3.OperationalError:
        return None


def _paper_track(ticker: str, market: str) -> int:
    """Count distinct methods that fired paper_trade_signal for this ticker.
    More methods firing = more frameworks agree = higher conviction."""
    try:
        with sqlite3.connect(DBS[market]) as c:
            n = c.execute(
                "SELECT COUNT(DISTINCT method_id) FROM paper_trade_signals "
                "WHERE ticker=? AND status='open'",
                (ticker,),
            ).fetchone()[0]
        # Map: 0 methods = 30, 1=50, 2=70, 3+=90 (cap)
        return min(90, 30 + n * 20)
    except sqlite3.OperationalError:
        return 50


def compute_one(ticker: str, market: str) -> dict:
    th = _thesis_health(ticker, market)
    ic = _ic_consensus(ticker)
    vp = _variant(ticker, market)
    dc = _data_coverage(ticker, market)
    pt = _paper_track(ticker, market)

    components = {
        "thesis_health": th if th is not None else 50,
        "ic_consensus":  ic if ic is not None else 50,
        "variant":       vp if vp is not None else 50,
        "data_coverage": dc if dc is not None else 50,
        "paper_track":   pt,
    }

    composite = sum(components[k] * WEIGHTS[k] for k in WEIGHTS)
    return {
        "ticker": ticker,
        "market": market,
        "composite_score": int(round(composite)),
        **components,
        "missing": [k for k, v in {"thesis_health": th, "ic_consensus": ic,
                                     "variant": vp, "data_coverage": dc}.items() if v is None],
    }


def run(universe: bool = False) -> dict:
    ensure_schema()
    today = date.today().isoformat()
    results = []
    targets = _universe_with_thesis() if universe else _holdings()
    for ticker, market in targets:
        r = compute_one(ticker, market)
        results.append(r)
        # Persist
        with sqlite3.connect(DBS["br"]) as c:
            c.execute(
                """INSERT OR REPLACE INTO conviction_scores
                   (ticker, market, run_date, composite_score, thesis_health,
                    ic_consensus, variant, data_coverage, paper_track, details_json)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    r["ticker"], r["market"], today, r["composite_score"],
                    r["thesis_health"], r["ic_consensus"], r["variant"],
                    r["data_coverage"], r["paper_track"],
                    json.dumps({"missing": r["missing"]}),
                ),
            )
            c.commit()

    results.sort(key=lambda x: -x["composite_score"])
    return {"date": today, "results": results}


def write_markdown(report: dict) -> Path:
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    out = BRIEFINGS_DIR / f"conviction_ranking_{report['date']}.md"
    lines = [
        "---",
        "type: conviction_ranking",
        f"date: {report['date']}",
        "tags: [conviction, ranking, composite_score]",
        "---",
        "",
        f"# 🎯 Conviction Ranking — {report['date']}",
        "",
        "> Composite 0-100 score per holding, integrating 5 sub-signals:",
        "> - Thesis health (perpetuum_thesis) — 30%",
        "> - IC consensus (synthetic_ic 5-persona debate) — 25%",
        "> - Variant perception (vs analyst consensus) — 15%",
        "> - Data coverage (perpetuum_data) — 10%",
        "> - Paper trade track (# methods firing) — 20%",
        "",
        "## 🏆 Ranking",
        "",
        "| # | Ticker | Mkt | **Composite** | Thesis | IC | Variant | Data | Methods |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for i, r in enumerate(report["results"], 1):
        emoji = "🟢" if r["composite_score"] >= 70 else ("🟡" if r["composite_score"] >= 50 else "🔴")
        lines.append(
            f"| {i} | {r['ticker']} | {r['market'].upper()} | "
            f"**{emoji} {r['composite_score']}** | "
            f"{r['thesis_health']} | {r['ic_consensus']} | {r['variant']} | "
            f"{r['data_coverage']} | {r['paper_track']} |"
        )
    lines.append("")
    lines.append("## 🟢 High conviction (≥70)")
    high = [r for r in report["results"] if r["composite_score"] >= 70]
    for r in high:
        lines.append(f"- **{r['ticker']}** ({r['composite_score']}) — {r['market'].upper()}")
    if not high:
        lines.append("_(none)_")
    lines.append("")
    lines.append("## 🔴 Low conviction (<50) — review")
    low = [r for r in report["results"] if r["composite_score"] < 50]
    for r in low:
        miss = f" missing: {','.join(r['missing'])}" if r["missing"] else ""
        lines.append(f"- **{r['ticker']}** ({r['composite_score']}) — {r['market'].upper()}{miss}")
    if not low:
        lines.append("_(none — all positions ≥50)_")
    lines.append("")
    lines.append("## 📊 Decision framework")
    lines.append("")
    lines.append("- **≥80**: high conviction — consider adding on weakness")
    lines.append("- **70-79**: solid — hold + monitor")
    lines.append("- **50-69**: neutral — review thesis quarterly")
    lines.append("- **30-49**: weakening — consider trim")
    lines.append("- **<30**: thesis broken — exit candidate")
    lines.append("")
    lines.append("---")
    lines.append("*Auto-generated by `analytics/conviction_score.py`. 100% local SQL + filesystem. Zero LLM calls.*")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", action="store_true",
                    help="score all 184 tickers (holdings + watchlist com thesis); default só holdings")
    ap.add_argument("--top", type=int, default=10, help="top-N to print (default 10)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    report = run(universe=args.universe)
    out = write_markdown(report)
    print(f"=== Conviction scoring — {report['date']} ({'universe' if args.universe else 'holdings'}) ===")
    print(f"Tickers scored: {len(report['results'])}")
    print(f"Top-{args.top}:")
    for i, r in enumerate(report["results"][:args.top], 1):
        print(f"  {i:>2}. {r['market'].upper()}:{r['ticker']:<8} composite={r['composite_score']:>3}  "
              f"th={r['thesis_health']:>3} ic={r['ic_consensus']:>3} var={r['variant']:>3} "
              f"data={r['data_coverage']:>3} pt={r['paper_track']:>3}")
    print(f"\nReport: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
