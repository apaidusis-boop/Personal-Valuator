"""agent_runner — cron entry point. Chamado a cada minuto.

Agenda Windows:
  schtasks /create /tn "ii-agent-runner" /tr "python \"C:\\path\\to\\agent_runner.py\"" ^
           /sc minute /mo 1

Ou Linux crontab:
  * * * * * cd /path && /usr/bin/python3 scripts/agent_runner.py >> logs/agent_runner.log 2>&1

Este script é MUITO leve — só verifica schedules e delega para agents/_runner.py.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from agents._runner import run_all_due  # noqa: E402


def main():
    started = datetime.now()
    print(f"[{started.isoformat(timespec='seconds')}] agent_runner tick")
    try:
        results = run_all_due(ROOT)
        if results:
            for r in results:
                icon = {"ok": "✅", "no_action": "·", "failed": "❌"}.get(r.status, "?")
                print(f"  {icon} {r.agent}: {r.summary[:100]}")
        else:
            print("  (no agents due)")
    except Exception as e:
        print(f"[runner] fatal: {type(e).__name__}: {e}")
        return 1
    dur = (datetime.now() - started).total_seconds()
    print(f"[{datetime.now().isoformat(timespec='seconds')}] tick done ({dur:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
