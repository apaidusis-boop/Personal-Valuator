"""AgentState — JSON persistent state per agent in data/agents/<name>.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class AgentState:
    """Simple JSON-backed state for agents. Thread-unsafe but cron-safe."""

    def __init__(self, agent_name: str, root: Path):
        self.agent_name = agent_name
        self.path = root / "data" / "agents" / f"{agent_name}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {
                "agent": self.agent_name,
                "run_count": 0,
                "failed_count": 0,
                "last_run": None,
                "last_status": None,
                "last_error": None,
                "custom": {},
            }
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {"agent": self.agent_name, "run_count": 0, "failed_count": 0}

    def save(self) -> None:
        self.path.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")

    def record_run(self, status: str, error: str | None = None) -> None:
        self._data["run_count"] = self._data.get("run_count", 0) + 1
        self._data["last_run"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._data["last_status"] = status
        if status == "failed":
            self._data["failed_count"] = self._data.get("failed_count", 0) + 1
            self._data["last_error"] = error
        self.save()

    def get(self, key: str, default=None):
        return self._data.get("custom", {}).get(key, default)

    def set(self, key: str, value) -> None:
        self._data.setdefault("custom", {})[key] = value

    def as_dict(self) -> dict:
        return dict(self._data)

    def last_run_dt(self) -> datetime | None:
        lr = self._data.get("last_run")
        if not lr:
            return None
        try:
            return datetime.fromisoformat(lr)
        except ValueError:
            return None
