"""Ad Perpetuum Validator — Heart of Phase W Gold.

Corre diariamente (23:45 após daily_update 23:30). Para cada holding:
  1. Pull thesis (obsidian_vault/tickers/<X>.md secção ## Thesis)
  2. Check fundamentals drift (fundamentals table delta vs baseline)
  3. Count risk_auditor rule hits (R1-R5 deterministic rules)
  4. Check regime shift (analytics/regime.classify vs anchor)
  5. Compute thesis_score 0-100
  6. INSERT thesis_health
  7. If drop ≥ 10 vs last run → flag (would Telegram in prod)

Score formula:
    score = 100
    score -= contradictions * 5   (data-driven signals against thesis)
    score -= regime_shift    * 15 (macro context changed)
    score -= devils_flags    * 3  (qualitative devils advocate)
    score -= risk_flags      * 4  (R1-R5 hits from risk_auditor)
    score += min(pro_evidence, 10)
    score = clamp(0, 100)

Tiers:
    90-100  intact       (no action)
    70-89   minor erosion (watch)
    50-69   material drift (revisit this week)
    30-49   broken       (rebalance/exit)
     0-29   preservation  (exit now)
"""
from __future__ import annotations

import json
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"

# Dynamic import — avoid hard import-time dependency; agents run standalone
try:
    from agents._base import AgentContext, AgentResult, BaseAgent
    HAS_BASE = True
except Exception:
    HAS_BASE = False


@dataclass
class ThesisHealth:
    ticker: str
    thesis_score: int
    new_evidence: int = 0
    contradictions: int = 0
    regime_shift: int = 0
    devils_flags: int = 0
    risk_flags: int = 0
    details: dict = field(default_factory=dict)


def _pull_thesis(ticker: str) -> str | None:
    """Extract thesis-equivalent content from the ticker vault note.

    Vault template evolved 2026-05: "## Thesis" was replaced by structured
    "## 🎯 Verdict" (auto-generated dossier) plus optional "## Tese / Notas
    do investidor" (manual notes). Probe in priority order:
      1. ## Tese / Notas do investidor  (manual investor commitment)
      2. ## Tese                         (any case, partial match)
      3. ## Thesis                       (legacy template, backwards compat)
      4. ## 🎯 Verdict                   (system-generated thesis-equivalent)
    """
    path = TICKERS_DIR / f"{ticker}.md"
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8", errors="ignore")
    for marker in ("## Tese", "## Thesis", "## 🎯 Verdict"):
        if marker not in content:
            continue
        after = content.split(marker, 1)[1]
        next_h2 = after.find("\n## ")
        body = (after[:next_h2].strip() if next_h2 > 0 else after.strip())
        if body:
            return body[:500]
    return None


def _count_risk_rules(db: Path, ticker: str) -> tuple[int, list[str]]:
    """Aplica subset das R1-R5 do risk_auditor (rule-based, zero LLM).

    Devolve (flag_count, reasons). Usa SQL puro, zero chamadas externas.
    """
    flags: list[str] = []
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row

        # R1. P/E expansion: actual PE > 1.4x historical avg
        row_pe = c.execute(
            "SELECT pe FROM fundamentals WHERE ticker=? AND pe > 0 ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        row_pe_hist = c.execute(
            "SELECT AVG(pe) FROM fundamentals WHERE ticker=? AND pe > 0 AND pe < 200",
            (ticker,)
        ).fetchone()
        if row_pe and row_pe[0] and row_pe_hist and row_pe_hist[0]:
            if row_pe[0] / row_pe_hist[0] >= 1.4:
                flags.append(f"R1 P/E +{((row_pe[0]/row_pe_hist[0])-1)*100:.0f}% vs hist")

        # R2/R3. Drawdown from 52w high
        row_price = c.execute(
            "SELECT MAX(close), (SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1) "
            "FROM prices WHERE ticker=? AND date >= date('now','-365 days')",
            (ticker, ticker)
        ).fetchone()
        if row_price and row_price[0] and row_price[1]:
            dd = (row_price[1] - row_price[0]) / row_price[0]
            if dd <= -0.30:
                flags.append(f"R3 DD {dd*100:.0f}% from 52w")
            elif dd <= -0.20:
                flags.append(f"R2 DD {dd*100:.0f}% from 52w")

        # R4. YoY price > +60% (euphoria)
        row_yoy = c.execute(
            "SELECT close FROM prices WHERE ticker=? AND date >= date('now','-365 days') "
            "ORDER BY date LIMIT 1",
            (ticker,)
        ).fetchone()
        row_last = c.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        if row_yoy and row_last and row_yoy[0] and row_last[0]:
            yoy = (row_last[0] - row_yoy[0]) / row_yoy[0]
            if yoy > 0.60:
                flags.append(f"R4 YoY +{yoy*100:.0f}%")

        # R5. DY current < 50% of historical avg
        row_dy = c.execute(
            "SELECT dy FROM fundamentals WHERE ticker=? AND dy > 0 ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        row_dy_hist = c.execute(
            "SELECT AVG(dy) FROM fundamentals WHERE ticker=? AND dy > 0",
            (ticker,)
        ).fetchone()
        if row_dy and row_dy[0] and row_dy_hist and row_dy_hist[0]:
            if row_dy[0] < 0.5 * row_dy_hist[0]:
                flags.append(f"R5 DY compressed {row_dy[0]:.1f}% vs avg {row_dy_hist[0]:.1f}%")

    return len(flags), flags


def _regime_shift_detect(market: str, prev_regime: str | None) -> tuple[int, str]:
    """Classifica regime hoje e compara com prev_regime."""
    try:
        from analytics.regime import classify
        r = classify(market)
        current = r.regime
        if prev_regime and prev_regime != current:
            return 1, current
        return 0, current
    except Exception as e:
        return 0, f"error:{e}"


def _last_run_details(db: Path, ticker: str, before: str) -> tuple[int | None, dict]:
    with sqlite3.connect(db) as c:
        row = c.execute(
            "SELECT thesis_score, details_json FROM thesis_health "
            "WHERE ticker=? AND run_date < ? ORDER BY run_date DESC LIMIT 1",
            (ticker, before)
        ).fetchone()
    if not row:
        return None, {}
    try:
        details = json.loads(row[1]) if row[1] else {}
    except Exception:
        details = {}
    return row[0], details


def _contradictions_from_fundamentals(db: Path, ticker: str) -> tuple[int, list[str]]:
    """Detecta contradictions a partir de trend negativo nos fundamentals.

    Contradictions = sinais data-driven que contradizem uma thesis típica:
      - ROE trend negativo em 2 quarters
      - DY compressed vs anterior quarter
      - Net debt/EBITDA a subir rápido
    """
    contras: list[str] = []
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT period_end, roe, dy, net_debt_ebitda FROM fundamentals "
            "WHERE ticker=? ORDER BY period_end DESC LIMIT 3",
            (ticker,)
        ).fetchall()

        if len(rows) >= 2:
            cur, prev = rows[0], rows[1]
            if cur["roe"] and prev["roe"] and cur["roe"] < prev["roe"] * 0.85:
                contras.append(f"ROE drop {prev['roe']:.1f} → {cur['roe']:.1f}")
            if cur["dy"] and prev["dy"] and cur["dy"] < prev["dy"] * 0.8:
                contras.append(f"DY compress {prev['dy']:.1f} → {cur['dy']:.1f}")
            if (cur["net_debt_ebitda"] and prev["net_debt_ebitda"]
                    and cur["net_debt_ebitda"] > prev["net_debt_ebitda"] * 1.5
                    and cur["net_debt_ebitda"] > 2.0):
                contras.append(f"NetDebt/EBITDA spike {prev['net_debt_ebitda']:.2f} → {cur['net_debt_ebitda']:.2f}")
    return len(contras), contras


def score_ticker(ticker: str, market: str) -> ThesisHealth:
    db = DBS[market]
    thesis = _pull_thesis(ticker)

    if not thesis:
        return ThesisHealth(
            ticker=ticker,
            thesis_score=-1,  # sentinel: no thesis to validate
            details={"reason": "no_thesis_in_vault"},
        )

    prev_score, prev_details = _last_run_details(db, ticker, date.today().isoformat())
    prev_regime = prev_details.get("regime")

    contras, contra_reasons = _contradictions_from_fundamentals(db, ticker)
    risk_flags, risk_reasons = _count_risk_rules(db, ticker)
    regime_shift, current_regime = _regime_shift_detect(market, prev_regime)

    # Devils flags: placeholder — fully wired in W.5 with agents.devils_advocate
    devils_flags, devils_reasons = 0, []

    # Pro evidence: placeholder — W.5 com Tavily search
    pro_evidence = 0

    score = 100
    score -= contras * 5
    score -= regime_shift * 15
    score -= devils_flags * 3
    score -= risk_flags * 4
    score += min(pro_evidence, 10)
    score = max(0, min(100, score))

    return ThesisHealth(
        ticker=ticker,
        thesis_score=score,
        new_evidence=contras + pro_evidence,
        contradictions=contras,
        regime_shift=regime_shift,
        devils_flags=devils_flags,
        risk_flags=risk_flags,
        details={
            "thesis_preview": thesis[:150],
            "regime": current_regime,
            "prev_regime": prev_regime,
            "contradiction_reasons": contra_reasons,
            "risk_reasons": risk_reasons,
            "devils_reasons": devils_reasons,
            "prev_score": prev_score,
        },
    )


def _holdings(market: str) -> list[str]:
    db = DBS[market]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        rows = c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()
    return [r[0] for r in rows]


def _persist(health: ThesisHealth, market: str, run_date: str) -> None:
    db = DBS[market]
    with sqlite3.connect(db) as c:
        c.execute(
            """
            INSERT OR REPLACE INTO thesis_health
                (ticker, run_date, thesis_score, new_evidence, contradictions,
                 regime_shift, devils_flags, risk_flags, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                health.ticker, run_date,
                health.thesis_score, health.new_evidence, health.contradictions,
                health.regime_shift, health.devils_flags, health.risk_flags,
                json.dumps(health.details, ensure_ascii=False),
            ),
        )
        c.commit()


def run(run_date: str | None = None, markets: list[str] | None = None) -> dict:
    """Executa uma run completa. Devolve summary dict.

    Retorna:
        {"processed": N, "alerts": N, "results": [{ticker, market, score}], "errors": [...]}
    """
    run_date = run_date or date.today().isoformat()
    markets = markets or ["br", "us"]
    results = []
    errors: list[str] = []
    alerts = 0

    for market in markets:
        for ticker in _holdings(market):
            try:
                health = score_ticker(ticker, market)
                _persist(health, market, run_date)

                prev = health.details.get("prev_score")
                drop = (prev - health.thesis_score) if (prev is not None and health.thesis_score >= 0) else None
                if drop is not None and drop >= 10:
                    alerts += 1

                results.append({
                    "ticker": ticker,
                    "market": market,
                    "score": health.thesis_score,
                    "contras": health.contradictions,
                    "risk": health.risk_flags,
                    "regime_shift": health.regime_shift,
                    "drop": drop,
                })
            except Exception as e:
                errors.append(f"{market}:{ticker}: {type(e).__name__}: {e}")

    return {
        "run_date": run_date,
        "processed": len(results),
        "alerts": alerts,
        "results": results,
        "errors": errors,
    }


if HAS_BASE:
    class PerpetuumValidator(BaseAgent):
        name = "perpetuum_validator"
        description = "Ad perpetuum thesis validator — scores 0-100 daily per holding"
        default_schedule = "daily:23:45"

        def execute_impl(self, ctx: AgentContext) -> AgentResult:
            summary = run()
            return AgentResult(
                agent=self.name,
                status="ok" if not summary["errors"] else "partial",
                summary=f"Validated {summary['processed']} holdings, {summary['alerts']} decay alerts",
                started_at="",  # filled by BaseAgent.execute wrapper
                finished_at="",
                duration_sec=0.0,
                data=summary,
                errors=summary["errors"],
                actions=[f"thesis_health rows: {summary['processed']}"],
            )


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], help="Só um mercado (default: ambos)")
    ap.add_argument("--date", help="ISO date for run (default: today)")
    args = ap.parse_args()

    markets = [args.market] if args.market else ["br", "us"]
    summary = run(run_date=args.date, markets=markets)

    print(f"=== Perpetuum Validator — {summary['run_date']} ===")
    print(f"Processed: {summary['processed']} holdings")
    print(f"Alerts (decay >= 10pts): {summary['alerts']}")
    if summary["errors"]:
        print(f"Errors: {len(summary['errors'])}")
        for e in summary["errors"][:5]:
            print(f"  - {e}")
    print()
    print("Top-10 by thesis_score (ascending — worst first):")
    sorted_r = sorted(summary["results"], key=lambda r: r["score"])
    for r in sorted_r[:10]:
        drop_str = f"Δ{r['drop']:+d}" if r["drop"] is not None else "new"
        print(f"  {r['market']}:{r['ticker']:<8} score={r['score']:>3} "
              f"contras={r['contras']} risk={r['risk']} regime={r['regime_shift']} {drop_str}")
