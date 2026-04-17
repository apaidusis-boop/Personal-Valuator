"""Pipeline diário do módulo de narrativa.

Ordem das fases (cada uma idempotente):

    1. scrapers      → narrative_items (raw, classified_at=NULL)
    2. classifier    → narrative_items (preenche sector/tese/direção)
    3. aggregator    → sector_sentiment (rolling 7/30/90d)
    4. regime        → macro_regime (4D)
    5. base_rates    → sector_base_rates  (correr semanalmente, não diário)
    6. rules.decide_universe → log de Decisions (relatório)

Uso:
    python scripts/narrative_update.py             # pipeline completo
    python scripts/narrative_update.py --skip-base-rates
    python scripts/narrative_update.py --only scrape,classify
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "config"

DB_BR = DATA_DIR / "br_investments.db"
DB_US = DATA_DIR / "us_investments.db"


def main() -> None:
    raise NotImplementedError(
        "Pipeline ainda não implementado — ver narrative/* para os stubs."
    )


if __name__ == "__main__":
    main()
