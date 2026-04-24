"""Ulisses Navegador — Head of Research.

Procura informação EXTERNA que as subscriptions não cobriram:
  - CVM fatos relevantes novos (via monitors/cvm_monitor.py)
  - SEC filings 8-K/10-K recentes (via monitors/sec_monitor.py)
  - News scan (via fetchers/news_fetch.py)

Para cada fonte, detecta o que é novo desde last_run (persistido em state),
faz triagem pró-holdings, e regista tudo em `events` table.

Schedule: daily 08:30 (depois do morning_briefing 07:00, antes de pregão BR 10:00).
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from ._base import AgentContext, AgentResult, BaseAgent
from ._personas import format_signature
from ._state import AgentState


class ResearchScoutAgent(BaseAgent):
    name = "research_scout"
    description = "Scout externo: CVM + SEC + news. Traz o que subscriptions não cobrem."
    default_schedule = "daily:08:30"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        errors: list[str] = []
        sources = ctx.config.get("sources", ["cvm", "sec", "news"])
        state = AgentState(self.name, root=root)
        py = sys.executable

        totals: dict[str, int] = {}

        # CVM monitor (BR fatos relevantes)
        if "cvm" in sources:
            try:
                out = self._run_script(root, py, "monitors/cvm_monitor.py")
                n = self._parse_count(out, "CVM")
                totals["cvm"] = n
                if n:
                    actions.append(f"CVM: {n} fatos novos")
            except Exception as e:
                errors.append(f"cvm: {type(e).__name__}: {e}")

        # SEC monitor (US filings)
        if "sec" in sources:
            try:
                out = self._run_script(root, py, "monitors/sec_monitor.py")
                n = self._parse_count(out, "SEC")
                totals["sec"] = n
                if n:
                    actions.append(f"SEC: {n} filings novos")
            except Exception as e:
                errors.append(f"sec: {type(e).__name__}: {e}")

        # News fetch
        if "news" in sources:
            try:
                out = self._run_script(root, py, "fetchers/news_fetch.py", ["--classify"])
                n = self._parse_count(out, "news")
                totals["news"] = n
                if n:
                    actions.append(f"news: {n} artigos novos")
            except Exception as e:
                errors.append(f"news: {type(e).__name__}: {e}")

        total_new = sum(totals.values())
        state.set("last_totals", totals)
        state.save()

        status = "ok" if total_new > 0 else ("failed" if errors else "no_action")
        summary = (
            f"{format_signature(self.name)}: {total_new} sinais externos novos "
            f"({', '.join(f'{k}={v}' for k, v in totals.items())})"
        )
        return AgentResult(
            agent=self.name, status=status, summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions, errors=errors, data={"totals": totals},
        )

    def _run_script(self, root, py, script_rel_path, extra_args=None):
        args = [py, "-X", "utf8", str(root / script_rel_path)] + (extra_args or [])
        r = subprocess.run(
            args, capture_output=True, text=True, timeout=300,
            cwd=str(root), encoding="utf-8", errors="replace",
        )
        return (r.stdout or "") + "\n" + (r.stderr or "")

    def _parse_count(self, out: str, hint: str) -> int:
        """Tenta extrair número de 'N new' ou 'N fatos' do output."""
        patterns = [
            rf"(\d+)\s+new",
            rf"(\d+)\s+fatos",
            rf"(\d+)\s+filings",
            rf"(\d+)\s+artigos",
            rf"(\d+)\s+rows?\s+inserted",
        ]
        total = 0
        for p in patterns:
            for m in re.finditer(p, out, re.IGNORECASE):
                total += int(m.group(1))
        return total
