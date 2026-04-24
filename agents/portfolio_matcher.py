"""Clara Fit — Portfolio Analyst.

Para cada analyst_insight novo (última hora) com ticker:
  - Classifica como HOLDING / WATCHLIST / MACRO / NOISE
  - Atribui relevance_score (0-1) baseado em:
      weight_source (do ranking de Aristóteles) × confidence × position_size_pct
  - Se relevance > 0.7 E é holding → cria watchlist_action com action_hint='REVIEW'

Schedule: every:30m — barato, incremental.
"""
from __future__ import annotations

import sqlite3
import json
from datetime import datetime, timedelta, timezone

from ._base import AgentContext, AgentResult, BaseAgent
from ._personas import format_signature


class PortfolioMatcherAgent(BaseAgent):
    name = "portfolio_matcher"
    description = "Mapeia insights recentes → holdings/watchlist com relevance score"
    default_schedule = "every:30m"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        hours = ctx.config.get("lookback_hours", 6)
        actions: list[str] = []
        stats = {"holdings": 0, "watchlist": 0, "macro": 0, "noise": 0, "high_relevance": 0}

        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row

                # Load source weights (from Aristóteles ranking)
                weights = self._load_source_weights(c)
                # Load holdings + watchlist
                holdings = {r[0]: r[1] for r in c.execute(
                    "SELECT ticker, quantity * (SELECT close FROM prices WHERE ticker=companies.ticker ORDER BY date DESC LIMIT 1) "
                    "FROM companies LEFT JOIN portfolio_positions USING (ticker) "
                    "WHERE is_holding=1 AND active=1"
                ).fetchall() if r[0]}
                total_mv = sum(holdings.values()) or 1

                watchlist = {r[0] for r in c.execute(
                    "SELECT ticker FROM companies WHERE is_holding=0"
                ).fetchall()}

                # Recent insights
                cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat(timespec="seconds")
                insights = c.execute("""
                    SELECT i.id, i.ticker, i.stance, i.claim, i.confidence, r.source
                    FROM analyst_insights i
                    JOIN analyst_reports r ON r.id = i.report_id
                    WHERE i.created_at >= ?
                """, (cutoff,)).fetchall()

                for ins in insights:
                    ticker = ins["ticker"]
                    if not ticker:
                        stats["macro"] += 1
                        continue

                    # Classify
                    if ticker in holdings:
                        category = "holdings"
                        pos_weight = holdings[ticker] / total_mv
                    elif ticker in watchlist:
                        category = "watchlist"
                        pos_weight = 0.3  # baseline
                    else:
                        stats["noise"] += 1
                        continue
                    stats[category] += 1

                    # Relevance
                    source_credibility = weights.get(f"analyst:{ins['source']}", 0.5)
                    conf = ins["confidence"] or 0.5
                    relevance = source_credibility * conf * min(pos_weight * 5, 1.0)

                    if relevance >= 0.7 and category == "holdings":
                        stats["high_relevance"] += 1
                        # Dedupe: 1 action per ticker per day
                        existing = c.execute("""
                            SELECT 1 FROM watchlist_actions
                            WHERE ticker=? AND kind='portfolio_matcher_high_rel'
                              AND status='open' AND created_at >= date('now', '-1 days')
                        """, (ticker,)).fetchone()
                        if not existing:
                            c.execute("""
                                INSERT INTO watchlist_actions
                                    (ticker, kind, action_hint, note, status, created_at)
                                VALUES (?, 'portfolio_matcher_high_rel', 'REVIEW', ?, 'open', ?)
                            """, (
                                ticker,
                                f"[Clara Fit] {ins['source']} insight ({ins['stance'] or 'neutral'}, "
                                f"conf={conf:.2f}, rel={relevance:.2f}): {(ins['claim'] or '')[:200]}",
                                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            ))
                            actions.append(f"high-rel REVIEW {ticker} (rel={relevance:.2f})")

                c.commit()

        status = "ok" if actions else "no_action"
        return AgentResult(
            agent=self.name, status=status,
            summary=(
                f"{format_signature(self.name)}: {stats['holdings']} holdings + "
                f"{stats['watchlist']} watchlist + {stats['macro']} macro + "
                f"{stats['noise']} noise. {stats['high_relevance']} high-rel flagged."
            ),
            started_at="", finished_at="", duration_sec=0,
            actions=actions, data={"stats": stats},
        )

    def _load_source_weights(self, c: sqlite3.Connection) -> dict[str, float]:
        """Read per-source accuracy → return weight in [0.3, 1.0]."""
        weights = {}
        try:
            rows = c.execute("""
                SELECT source,
                       SUM(CASE WHEN outcome='correct' THEN 1.0 ELSE 0 END) /
                       NULLIF(COUNT(*), 0) AS acc
                FROM predictions WHERE evaluated_at IS NOT NULL
                GROUP BY source HAVING COUNT(*) >= 5
            """).fetchall()
            for src, acc in rows:
                if acc is not None:
                    # clamp [0.3, 1.0]
                    weights[src] = max(0.3, min(1.0, acc * 1.5))
        except sqlite3.OperationalError:
            pass
        return weights
