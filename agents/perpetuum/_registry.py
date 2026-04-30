"""Registry de perpetuums. Adicionar aqui para ficar disponível via master runner."""
from __future__ import annotations

from ._engine import BasePerpetuum
from .thesis import ThesisPerpetuum
from .vault_health import VaultHealthPerpetuum
from .data_coverage import DataCoveragePerpetuum
from .content_quality import ContentQualityPerpetuum
from .method_discovery import MethodDiscoveryPerpetuum
from .token_economy import TokenEconomyPerpetuum
from .library_signals import LibrarySignalsPerpetuum
from .ri_freshness import RIFreshnessPerpetuum
from .code_health import CodeHealthPerpetuum
from .autoresearch import AutoresearchPerpetuum
from .bibliotheca import BibliothecaPerpetuum
from .dreaming import DreamingPerpetuum
from .security_audit import SecurityAuditPerpetuum
from .daily_delight import DailyDelightPerpetuum
from .meta import MetaPerpetuum


def _build() -> dict[str, BasePerpetuum]:
    # Order matters: meta roda POR ÚLTIMO (precisa dos outros já escritos)
    instances = [
        ThesisPerpetuum(),
        VaultHealthPerpetuum(),
        DataCoveragePerpetuum(),
        ContentQualityPerpetuum(),
        MethodDiscoveryPerpetuum(),
        TokenEconomyPerpetuum(),
        LibrarySignalsPerpetuum(),
        RIFreshnessPerpetuum(),
        CodeHealthPerpetuum(),
        AutoresearchPerpetuum(),
        BibliothecaPerpetuum(),
        DreamingPerpetuum(),     # opt-in; consolidates daily_logs → DREAMS.md
        SecurityAuditPerpetuum(), # read-only host hygiene; writes SECURITY_AUDIT.md
        DailyDelightPerpetuum(),  # opt-in; morning topic-of-the-day build
        MetaPerpetuum(),         # always last
    ]
    return {p.name: p for p in instances}


_REGISTRY: dict[str, BasePerpetuum] | None = None


def get_all() -> dict[str, BasePerpetuum]:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build()
    return _REGISTRY


def get_by_name(name: str) -> BasePerpetuum | None:
    return get_all().get(name)
