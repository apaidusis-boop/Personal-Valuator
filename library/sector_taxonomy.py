"""Canonical sector taxonomy + normalization.

Single source of truth for the sector vocabulary used in the `companies`
table (BR + US DBs) and Obsidian sector notes. The Bibliotheca perpetuum
(`agents.perpetuum.bibliotheca`) consults this map to decide whether a
ticker is well-classified or needs a librarian action.

Why a fixed taxonomy: without one, every fetcher / analyst report invents
its own ("Insurance Broker", "Chemicals", "Education", "Agribusiness"),
and the vault sector index fragments. Sector sprawl breaks the
`obsidian_vault/sectors/<X>.md` Dataview queries.
"""
from __future__ import annotations

# Canonical set — anything not in here is "non-canonical" and the
# Bibliotheca will propose the mapped equivalent (or flag for human review
# if no mapping exists).
CANONICAL_SECTORS: frozenset[str] = frozenset({
    # Operating sectors (BR + US)
    "Banks",
    "Financials",
    "Insurance",
    "Healthcare",
    "Technology",
    "Communication",
    "Consumer Disc.",
    "Consumer Staples",
    "Energy",
    "Oil & Gas",
    "Industrials",
    "Materials",
    "Mining",
    "Utilities",
    "Telecom",
    "Real Estate",
    "Holding",
    # FII / property (BR-specific buckets)
    "REIT",
    "Shopping",
    "Logística",
    "Híbrido",
    "Papel (CRI)",
    "Corporativo",
    # ETFs
    "ETF",
    "ETF-RF",
    "ETF-US",
})

# Normalization map: non-canonical → canonical.
# Lower-case keys; lookup is case-insensitive.
SECTOR_ALIASES: dict[str, str] = {
    # Insurance variants
    "insurance broker": "Insurance",
    "seguros": "Insurance",

    # Materials / chemicals
    "chemicals": "Materials",
    "química": "Materials",
    "quimica": "Materials",
    "paper & pulp": "Materials",
    "papel e celulose": "Materials",

    # Consumer
    "education": "Consumer Disc.",
    "educação": "Consumer Disc.",
    "educacao": "Consumer Disc.",
    "agribusiness": "Consumer Staples",
    "agronegócio": "Consumer Staples",
    "agronegocio": "Consumer Staples",
    "retail": "Consumer Disc.",
    "consumer discretionary": "Consumer Disc.",
    "consumer cyclical": "Consumer Disc.",
    "consumer defensive": "Consumer Staples",

    # Tech / comms
    "information technology": "Technology",
    "communication services": "Communication",
    "media": "Communication",

    # Energy / oil
    "oil and gas": "Oil & Gas",
    "oil&gas": "Oil & Gas",

    # Real estate
    "real estate management": "Real Estate",
    "real estate investment trust": "REIT",

    # FII mojibake (latin1-mangled UTF-8 from old fetcher writes)
    "h?brido": "Híbrido",
    "h�brido": "Híbrido",
    "log?stica": "Logística",
    "log�stica": "Logística",

    # Common yfinance.info.sector strings
    "financial services": "Financials",
    "basic materials": "Materials",
}


def normalize(raw: str | None) -> str | None:
    """Map any sector string to a canonical bucket.

    Returns None if input is None/empty (caller decides whether NULL is OK).
    Returns the canonical name if a match exists.
    Returns the *original* string (un-normalized) if no mapping is known —
    Bibliotheca will then surface it as a `SECTOR_NONCANONICAL` flag so a
    human can decide whether to extend the alias map.
    """
    if not raw:
        return None
    raw_clean = raw.strip()
    if raw_clean in CANONICAL_SECTORS:
        return raw_clean
    mapped = SECTOR_ALIASES.get(raw_clean.lower())
    if mapped:
        return mapped
    return raw_clean


def is_canonical(sector: str | None) -> bool:
    return sector is not None and sector in CANONICAL_SECTORS


def is_known_alias(sector: str | None) -> bool:
    if not sector:
        return False
    return sector.strip().lower() in SECTOR_ALIASES


__all__ = [
    "CANONICAL_SECTORS",
    "SECTOR_ALIASES",
    "normalize",
    "is_canonical",
    "is_known_alias",
]
