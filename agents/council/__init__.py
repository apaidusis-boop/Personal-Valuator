"""STORYT_2.0 Council — pre-publication multi-agent debate.

Inserts a deliberation layer between Classification (STORYT_1 Camada 5) and
Narrative (Camada 6). Three voices argue across two rounds before the
narrative engine ships a dossier:

  - Sector Specialist: defends method-correct framing for the asset's Modo
  - Risk Officer:      Pre-Mortem rigour, distress flags, gating conditions
  - Portfolio Officer: fit vs current portfolio, sizing, correlation

Output:
  - CouncilSynthesis (consensus + preserved dissent + pre-publication flags)
  - Markdown transcript at obsidian_vault/dossiers/<TICKER>_COUNCIL.md
  - JSON sidecar for programmatic consumption

Modo A-BR prototype. Banks/Commodities/REITs follow if the prototype proves
out vs the existing single-pass pipeline (synthetic_ic + variant_perception
chained sequentially after dossier).

100% Ollama local. Zero Claude tokens. (CLAUDE.md feedback_inhouse_first.md.)
"""
from agents.council.coordinator import run_council
from agents.council.dossier import CouncilDossier, build_dossier

__all__ = ["run_council", "CouncilDossier", "build_dossier"]
