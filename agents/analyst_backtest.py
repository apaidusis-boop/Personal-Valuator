"""Aristóteles Backtest — Head of Performance.

Fecha o loop de aprendizagem. Para cada prediction (analyst_insight com
price_target OU stance bull/bear) registada em `predictions` table:

  - Se prediction foi há ≥ horizon_days (30/90/180), evaluate:
      - bull: preço subiu > stance_threshold? → correct
      - bear: preço caiu > stance_threshold? → correct
      - price_target: actual preço atingiu? → correct
  - Agrega accuracy por source (XP / Fool / WSJ / YouTube channel)
  - Escreve ranking em obsidian_vault/agents/_performance_ranking.md
  - Sugere weight adjustments (source credibility)

Também **popula** a predictions table quando não está (backfill inicial) —
corre através de analyst_insights dos últimos 180 dias com price_target
ou stance forte.

Schedule: weekly Friday 20:00.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent
from ._personas import format_signature


class AnalystBacktestAgent(BaseAgent):
    name = "analyst_backtest"
    description = "Mede accuracy de predictions vs real moves; ranking de sources"
    default_schedule = "weekly:fri:20:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        horizons = ctx.config.get("horizons_days", [30, 90, 180])
        threshold = float(ctx.config.get("stance_threshold", 0.02))

        backfilled = 0
        evaluated = 0
        rankings_by_source: dict[str, dict] = {}

        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row

                # 1. Backfill: criar predictions rows a partir de insights recentes
                backfilled += self._backfill_from_insights(c, days=180)

                # 2. Evaluate predictions pending cujo horizon passou
                for h in horizons:
                    evaluated += self._evaluate_horizon(c, h, threshold)

                # 3. Agrega accuracy por source
                rows = c.execute("""
                    SELECT source,
                           COUNT(*) AS total,
                           SUM(CASE WHEN outcome='correct' THEN 1 ELSE 0 END) AS correct,
                           SUM(CASE WHEN outcome='wrong'   THEN 1 ELSE 0 END) AS wrong,
                           AVG(confidence) AS avg_conf
                    FROM predictions
                    WHERE evaluated_at IS NOT NULL
                    GROUP BY source
                """).fetchall()
                for r in rows:
                    total = r["total"] or 0
                    correct = r["correct"] or 0
                    rankings_by_source.setdefault(r["source"], {
                        "total": 0, "correct": 0, "wrong": 0, "avg_conf": 0
                    })
                    agg = rankings_by_source[r["source"]]
                    agg["total"] += total
                    agg["correct"] += correct
                    agg["wrong"] += (r["wrong"] or 0)
                    if r["avg_conf"]:
                        agg["avg_conf"] = (agg["avg_conf"] + r["avg_conf"]) / 2

                c.commit()

        # 4. Write performance ranking to vault
        if not ctx.dry_run:
            self._write_ranking(root, rankings_by_source)

        if backfilled:
            actions.append(f"backfilled {backfilled} predictions from insights")
        if evaluated:
            actions.append(f"evaluated {evaluated} predictions (horizons={horizons})")
        if rankings_by_source:
            actions.append(f"ranking updated — {len(rankings_by_source)} sources tracked")

        return AgentResult(
            agent=self.name,
            status="ok" if actions else "no_action",
            summary=(
                f"{format_signature(self.name)}: {backfilled} backfilled, "
                f"{evaluated} evaluated, {len(rankings_by_source)} sources ranked."
            ),
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data={"rankings": rankings_by_source, "backfilled": backfilled, "evaluated": evaluated},
        )

    # ─── Backfill predictions from insights ─────────────────────────────
    def _backfill_from_insights(self, c: sqlite3.Connection, days: int) -> int:
        """Para cada analyst_insight com stance forte OU price_target, insere
        row em predictions se ainda não existe."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")
        insights = c.execute("""
            SELECT i.id, i.ticker, i.stance, i.price_target, i.confidence, i.claim,
                   r.source, r.published_at
            FROM analyst_insights i
            JOIN analyst_reports r ON r.id = i.report_id
            WHERE i.ticker IS NOT NULL
              AND r.published_at >= ?
              AND (i.stance IN ('bull', 'bear') OR i.price_target IS NOT NULL)
        """, (cutoff,)).fetchall()

        new = 0
        for row in insights:
            # Check se já existe prediction para (source_ref=insight_id)
            source_ref = f"insight:{row['id']}"
            existing = c.execute(
                "SELECT 1 FROM predictions WHERE source_ref = ? LIMIT 1",
                (source_ref,),
            ).fetchone()
            if existing:
                continue

            # Preço at prediction (published_at)
            pub_date = row["published_at"][:10]
            price_row = c.execute("""
                SELECT close FROM prices WHERE ticker=? AND date<=?
                ORDER BY date DESC LIMIT 1
            """, (row["ticker"], pub_date)).fetchone()
            price_at_pred = price_row[0] if price_row else None
            if not price_at_pred:
                continue

            c.execute("""
                INSERT INTO predictions
                    (source, source_ref, ticker, prediction_date, price_at_pred,
                     predicted_stance, price_target, horizon_days, confidence,
                     claim, outcome)
                VALUES (?, ?, ?, ?, ?, ?, ?, 90, ?, ?, 'pending')
            """, (
                f"analyst:{row['source']}",
                source_ref,
                row["ticker"],
                pub_date,
                price_at_pred,
                row["stance"] or "neutral",
                row["price_target"],
                row["confidence"] or 0.5,
                (row["claim"] or "")[:500],
            ))
            new += 1
        return new

    # ─── Evaluate predictions ───────────────────────────────────────────
    def _evaluate_horizon(self, c: sqlite3.Connection, horizon_days: int, threshold: float) -> int:
        """Marca outcome em predictions cujo horizon passou."""
        cutoff_date = (datetime.now().date() - timedelta(days=horizon_days)).isoformat()
        pending = c.execute("""
            SELECT id, ticker, prediction_date, price_at_pred, predicted_stance,
                   price_target, horizon_days
            FROM predictions
            WHERE outcome = 'pending'
              AND horizon_days = ?
              AND prediction_date <= ?
        """, (horizon_days, cutoff_date)).fetchall()

        updated = 0
        for p in pending:
            eval_date = (
                datetime.fromisoformat(p[2]).date() + timedelta(days=horizon_days)
            ).isoformat()
            price_row = c.execute("""
                SELECT close FROM prices WHERE ticker=? AND date<=?
                ORDER BY date DESC LIMIT 1
            """, (p[1], eval_date)).fetchone()
            if not price_row or not price_row[0]:
                continue
            price_eval = price_row[0]
            price_pred = p[3]
            change = (price_eval - price_pred) / price_pred

            stance = p[4]
            target = p[5]

            # Prioridade: price_target se existe
            if target and target > 0:
                outcome = "correct" if (
                    (stance == "bull" and price_eval >= target) or
                    (stance == "bear" and price_eval <= target)
                ) else "wrong"
            else:
                if stance == "bull":
                    outcome = "correct" if change >= threshold else (
                        "wrong" if change <= -threshold else "neutral"
                    )
                elif stance == "bear":
                    outcome = "correct" if change <= -threshold else (
                        "wrong" if change >= threshold else "neutral"
                    )
                else:
                    outcome = "neutral"

            c.execute("""
                UPDATE predictions
                SET evaluated_at = ?, price_at_eval = ?, outcome = ?
                WHERE id = ?
            """, (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                price_eval, outcome, p[0],
            ))
            updated += 1
        return updated

    # ─── Write ranking to vault ─────────────────────────────────────────
    def _write_ranking(self, root: Path, rankings: dict) -> None:
        vault = root / "obsidian_vault" / "agents"
        vault.mkdir(parents=True, exist_ok=True)
        path = vault / "_performance_ranking.md"

        rows = []
        for source, agg in rankings.items():
            total = agg["total"]
            correct = agg["correct"]
            accuracy = (correct / total) if total > 0 else 0
            rows.append((source, total, correct, agg["wrong"], accuracy, agg["avg_conf"]))
        rows.sort(key=lambda x: -x[4])  # sort by accuracy desc

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "---",
            "type: agent_performance_ranking",
            f"updated: {now}",
            "tags: [agent, performance, backtest, ranking]",
            "---",
            "",
            "# 📊 Source Credibility Ranking",
            "",
            f"_Por {format_signature('analyst_backtest')} · última run {now}_",
            "",
            "## Accuracy por source",
            "",
            "| Source | Total | Correct | Wrong | Accuracy | Avg Confidence |",
            "|---|---|---|---|---|---|",
        ]
        for src, total, correct, wrong, acc, conf in rows:
            lines.append(
                f"| {src} | {total} | {correct} | {wrong} | "
                f"**{acc*100:.1f}%** | {conf:.2f} |"
            )
        lines += [
            "",
            "## Interpretação",
            "",
            "- **Accuracy > 60%**: source credível — manter peso default.",
            "- **Accuracy 40-60%**: coin-flip — ponderar insights com `confidence × 0.7`.",
            "- **Accuracy < 40%**: source contrarian (flip signal) ou ruído — review manual.",
            "",
            "## Policy (proposed)",
            "",
            "`portfolio_matcher` usa este ranking para ponderar insights quando",
            "computa relevance_score de cada insight vs holding.",
        ]
        path.write_text("\n".join(lines), encoding="utf-8")
