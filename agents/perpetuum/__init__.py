"""Perpetuum Engine — generalized self-improvement loops.

Architectural pattern: each perpetuum has same contract
    baseline → observe → score → detect drift → alert / action hint

Each subject (ticker, vault note, data source, briefing, method) gets a
health score 0-100 tracked over time. When score drops, system emits
signal. Gradually accumulates self-knowledge — today it flags, tomorrow
it proposes, eventually it acts.

Perpetuums actived:
  - thesis        — ticker thesis validation (was agents/perpetuum_validator.py)
  - vault         — vault note health (orphans, stale, backlinks)
  - data_coverage — data completeness per holding/source

Add new perpetuum:
    1. Create agents/perpetuum/<name>.py inheriting from BasePerpetuum
    2. Register in agents/perpetuum/_registry.py REGISTRY list
    3. Run via `python agents/perpetuum_master.py --only <name>`

Design principles:
  - Idempotent: re-run same day = overwrites same row (PRIMARY KEY)
  - Cheap: all scoring uses SQL + local files. LLM calls are opt-in.
  - Observable: every run writes to perpetuum_run_log + perpetuum_health
  - Autonomy-tiered: perpetuums declare their current tier (T1..T5)
"""
from ._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject
from ._registry import get_all, get_by_name

__all__ = ["BasePerpetuum", "PerpetuumResult", "PerpetuumSubject",
           "get_all", "get_by_name"]
