"""SubscriptionFetchAgent — weekly ingest de novos reports Fool/XP/WSJ.

Monday 09:00. Corre `ii subs fetch --source <X>` para cada fonte em config.
Não corre extract (watchdog faz isso continuamente).
"""
from __future__ import annotations

import subprocess
import sys

from ._base import AgentContext, AgentResult, BaseAgent


class SubscriptionFetchAgent(BaseAgent):
    name = "subscription_fetch"
    description = "Weekly fetch novos reports de Fool/XP/WSJ"
    default_schedule = "weekly:mon:09:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        errors: list[str] = []
        py = sys.executable
        sources = self.config.get("sources", ["fool", "xp", "wsj"])
        days = self.config.get("days", 7)
        total_new = 0
        for src in sources:
            try:
                r = subprocess.run(
                    [py, "-X", "utf8", str(root / "scripts" / "subscriptions_cli.py"),
                     "fetch", "--source", src, "--days", str(days)],
                    capture_output=True, text=True, timeout=1800, cwd=str(root),
                    encoding="utf-8", errors="replace",
                )
                import re
                for line in (r.stdout or "").splitlines():
                    m = re.search(rf"\[{src}\]\s+(\d+)\s+new", line)
                    if m:
                        n = int(m.group(1))
                        total_new += n
                        actions.append(f"{src}: {n} new reports")
                        break
            except Exception as e:
                errors.append(f"{src}: {type(e).__name__}: {e}")
        status = "ok" if total_new > 0 else ("failed" if errors else "no_action")
        summary = f"fetched {total_new} new reports ({len(sources)} sources)"
        return AgentResult(
            agent=self.name, status=status, summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions, errors=errors, data={"total_new": total_new},
        )
