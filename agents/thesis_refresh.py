"""ThesisRefreshAgent — Re-runs scripts/thesis_refresh.py on schedule.

Weekly sunday 22:00. Updates Live Snapshot block em todas thesis notes.
Também corre obsidian_bridge --refresh para actualizar tickers/.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent


class ThesisRefreshAgent(BaseAgent):
    name = "thesis_refresh"
    description = "Re-injecta Live Snapshot em wiki/holdings/ + refresh vault"
    default_schedule = "weekly:sun:22:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        errors: list[str] = []
        py = sys.executable

        # 1. Refresh thesis notes
        try:
            r = subprocess.run(
                [py, "-X", "utf8", str(root / "scripts" / "thesis_refresh.py")],
                capture_output=True, text=True, timeout=600, cwd=str(root),
                encoding="utf-8", errors="replace",
            )
            if r.returncode == 0:
                actions.append("thesis_refresh.py ran")
                for line in (r.stdout or "").splitlines()[-3:]:
                    actions.append(line.strip())
            else:
                errors.append(f"thesis_refresh exit {r.returncode}")
        except Exception as e:
            errors.append(f"thesis_refresh: {e}")

        # 2. Vault bridge full refresh
        try:
            r = subprocess.run(
                [py, "-X", "utf8", str(root / "scripts" / "obsidian_bridge.py")],
                capture_output=True, text=True, timeout=600, cwd=str(root),
                encoding="utf-8", errors="replace",
            )
            if r.returncode == 0:
                actions.append("obsidian_bridge refresh ok")
            else:
                errors.append(f"bridge exit {r.returncode}")
        except Exception as e:
            errors.append(f"bridge: {e}")

        status = "ok" if actions and not errors else ("failed" if errors else "no_action")
        return AgentResult(
            agent=self.name, status=status,
            summary=" · ".join(actions[:3]) if actions else " / ".join(errors[:2]),
            started_at="", finished_at="", duration_sec=0,
            actions=actions, errors=errors,
        )
