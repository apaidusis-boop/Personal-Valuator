"""Noé Arquivista — Data Steward.

Semanalmente (sáb 03:00) limpa o que já não presta:

  1. Archive analyst_reports > N dias (default 180) sem insights persistidos
  2. Dedup analyst_reports com mesmo source+source_id (raça condition caught)
  3. Archive watchlist_actions resolved > 90 dias em tabela _archive
  4. Remove log files > 90 dias em logs/agents/
  5. VACUUM em ambas DBs (compacta)

Schedule: weekly:sat:03:00 (quando ninguém usa).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent
from ._personas import format_signature


class DataJanitorAgent(BaseAgent):
    name = "data_janitor"
    description = "DB cleanup + log rotation + VACUUM semanal"
    default_schedule = "weekly:sat:03:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        cfg = ctx.config
        actions: list[str] = []
        totals: dict[str, int] = {}

        archive_days = cfg.get("archive_older_than_days", 180)
        do_dedup = cfg.get("dedup_reports", True)
        do_vacuum = cfg.get("vacuum", True)

        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                # 1. Archive old reports
                if not ctx.dry_run:
                    n = self._archive_old_reports(c, archive_days)
                    totals[f"{db_name}_archived_reports"] = n
                    if n:
                        actions.append(f"{db_name}: archived {n} old reports")

                # 2. Dedup reports
                if do_dedup and not ctx.dry_run:
                    n = self._dedup_reports(c)
                    totals[f"{db_name}_deduped"] = n
                    if n:
                        actions.append(f"{db_name}: deduped {n} duplicate reports")

                # 3. Archive resolved watchlist_actions
                if not ctx.dry_run:
                    n = self._archive_resolved_actions(c)
                    totals[f"{db_name}_archived_actions"] = n
                    if n:
                        actions.append(f"{db_name}: archived {n} resolved actions")

                c.commit()

                # 4. VACUUM (outside transaction)
                if do_vacuum and not ctx.dry_run:
                    try:
                        c.execute("VACUUM")
                        actions.append(f"{db_name}: VACUUM ok")
                    except sqlite3.OperationalError as e:
                        actions.append(f"{db_name}: VACUUM skipped ({e})")

        # 5. Log rotation
        if not ctx.dry_run:
            n = self._rotate_logs(root, days=90)
            if n:
                actions.append(f"removed {n} old log files")
                totals["old_logs_removed"] = n

        return AgentResult(
            agent=self.name,
            status="ok" if actions else "no_action",
            summary=(
                f"{format_signature(self.name)}: "
                f"{sum(totals.values())} items cleaned across DBs and logs."
            ),
            started_at="", finished_at="", duration_sec=0,
            actions=actions, data={"totals": totals},
        )

    # ─── Helpers ─────────────────────────────────────────────────────────

    def _archive_old_reports(self, c: sqlite3.Connection, days: int) -> int:
        """Move analyst_reports > N dias sem insights para _archive table."""
        cutoff = (datetime.now().date() - timedelta(days=days)).isoformat()
        # Ensure archive table
        c.execute("""
            CREATE TABLE IF NOT EXISTS analyst_reports_archive AS
            SELECT * FROM analyst_reports WHERE 0
        """)
        rows = c.execute("""
            SELECT r.* FROM analyst_reports r
            LEFT JOIN analyst_insights i ON i.report_id = r.id
            WHERE r.published_at < ? AND i.id IS NULL
        """, (cutoff,)).fetchall()
        if not rows:
            return 0
        cols = [d[0] for d in c.execute("PRAGMA table_info(analyst_reports)").fetchall()]
        # Copy to archive
        placeholders = ",".join("?" for _ in cols)
        c.executemany(
            f"INSERT INTO analyst_reports_archive ({','.join(cols)}) VALUES ({placeholders})",
            rows,
        )
        c.execute("""
            DELETE FROM analyst_reports
            WHERE id IN (
                SELECT r.id FROM analyst_reports r
                LEFT JOIN analyst_insights i ON i.report_id = r.id
                WHERE r.published_at < ? AND i.id IS NULL
            )
        """, (cutoff,))
        return len(rows)

    def _dedup_reports(self, c: sqlite3.Connection) -> int:
        """Remove duplicate analyst_reports com mesmo (source, source_id), keeping oldest id."""
        try:
            dups = c.execute("""
                SELECT source, source_id, COUNT(*) - 1 AS extra
                FROM analyst_reports
                GROUP BY source, source_id HAVING COUNT(*) > 1
            """).fetchall()
            total_extra = sum(r[2] for r in dups)
            if not total_extra:
                return 0
            c.execute("""
                DELETE FROM analyst_reports
                WHERE id NOT IN (
                    SELECT MIN(id) FROM analyst_reports GROUP BY source, source_id
                )
            """)
            return total_extra
        except sqlite3.OperationalError:
            return 0

    def _archive_resolved_actions(self, c: sqlite3.Connection) -> int:
        """Move resolved watchlist_actions > 90d para _archive."""
        cutoff = (datetime.now().date() - timedelta(days=90)).isoformat()
        try:
            c.execute("""
                CREATE TABLE IF NOT EXISTS watchlist_actions_archive AS
                SELECT * FROM watchlist_actions WHERE 0
            """)
            rows = c.execute("""
                SELECT * FROM watchlist_actions
                WHERE status IN ('resolved', 'ignored')
                  AND COALESCE(resolved_at, created_at) < ?
            """, (cutoff,)).fetchall()
            if not rows:
                return 0
            cols = [d[0] for d in c.execute("PRAGMA table_info(watchlist_actions)").fetchall()]
            placeholders = ",".join("?" for _ in cols)
            c.executemany(
                f"INSERT INTO watchlist_actions_archive ({','.join(cols)}) VALUES ({placeholders})",
                rows,
            )
            c.execute("""
                DELETE FROM watchlist_actions
                WHERE status IN ('resolved', 'ignored')
                  AND COALESCE(resolved_at, created_at) < ?
            """, (cutoff,))
            return len(rows)
        except sqlite3.OperationalError:
            return 0

    def _rotate_logs(self, root: Path, days: int) -> int:
        log_dir = root / "logs" / "agents"
        if not log_dir.exists():
            return 0
        cutoff_ts = (datetime.now() - timedelta(days=days)).timestamp()
        removed = 0
        for f in log_dir.glob("*.log*"):
            try:
                if f.stat().st_mtime < cutoff_ts:
                    f.unlink()
                    removed += 1
            except Exception:
                pass
        return removed
