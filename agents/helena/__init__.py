"""agents.helena — Mega Helena design intelligence package.

Subpackages:
  audit   — design system linter (scans Streamlit + Plotly code for violations)
  curate  — community skill go/no-go evaluator (vs in-house arsenal)
  spike   — feasibility sketches for the 4 platform paths (A/B/C/D)
  report  — master consolidator (writes design.lint_mega/00_MASTER.md)

Orchestrated by agents.helena_mega.MegaHelenaAgent.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAULT_OUT = ROOT / "obsidian_vault" / "skills" / "design.lint_mega"
VAULT_OUT.mkdir(parents=True, exist_ok=True)
