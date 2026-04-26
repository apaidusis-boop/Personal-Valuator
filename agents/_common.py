"""Shared lightweight utilities — para evitar duplicação cross-module.

Convenções:
  - Sem dependências externas além de stdlib + Path.
  - Nada aqui pode tocar a rede ou DBs (helpers puros).
  - Adicionar aqui APENAS funções já duplicadas em ≥2 sítios.

Política anti-duplicação (Phase Cleanup 2026-04-27): este módulo é o
"home" preferido para utilitários de baixo nível partilhados por
agents/ + scripts/. Para formatação user-facing PT-BR, ver `analytics.format`.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"


# ─────────────────────────────────────────────────────────────────────────────
# Slugs (filename-safe)
# ─────────────────────────────────────────────────────────────────────────────

def slugify(s: str, maxlen: int = 60) -> str:
    """ASCII-safe slug: lowercase, hyphens, truncated. Safe for filenames.

    Canonical version unificada (substitui duplicates em obsidian_bridge.py +
    vault_clean_video_names.py — Phase Cleanup 2026-04-27).

    >>> slugify("Hello World!")
    'hello-world'
    >>> slugify("Café com Leite", maxlen=10)
    'cafe-com-l'
    >>> slugify("")
    ''
    """
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:maxlen].rstrip("-")


# ─────────────────────────────────────────────────────────────────────────────
# Vault thesis reading
# ─────────────────────────────────────────────────────────────────────────────

def read_vault_thesis(ticker: str, max_chars: int | None = 1500) -> str | None:
    """Find ## Thesis content. Tries DOSSIER first (numbered: '## N. Thesis'),
    then plain wiki ticker note ('## Thesis').

    Canonical version (substitui _vault_thesis duplicates em synthetic_ic.py,
    earnings_prep.py, ab_qwen3_vs_14b.py — variant_perception.py mantém local
    porque já era a versão mais completa, mas pode migrar para cá).

    Args:
      ticker: símbolo (ex: 'ITSA4', 'ACN')
      max_chars: corte máximo (None = sem corte). Default 1500.

    Returns:
      Texto da thesis (limpo de footers '→ Vault:'), ou None se não encontrada.
    """
    candidates = [
        (TICKERS_DIR / f"{ticker}_DOSSIE.md", True),   # check numbered ## N. Thesis
        (TICKERS_DIR / f"{ticker}.md", False),          # legacy: plain ## Thesis
    ]
    for p, numbered in candidates:
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        if numbered:
            # Match "## 3. Thesis" or any number
            m = re.search(r"\n## \d+\.\s*Thesis\s*\n", content)
            if not m:
                # try plain too (some dossiers may not be numbered)
                if "## Thesis" not in content:
                    continue
                after = content.split("## Thesis", 1)[1]
            else:
                after = content[m.end():]
        else:
            if "## Thesis" not in content:
                continue
            after = content.split("## Thesis", 1)[1]
        # cut at next ## section
        end = after.find("\n## ")
        thesis = (after[:end] if end > 0 else after).strip()
        # also cut if we hit "→ Vault:" footer from dossier render
        if "\n→ Vault:" in thesis:
            thesis = thesis.split("\n→ Vault:", 1)[0].strip()
        if thesis:
            return thesis[:max_chars] if max_chars else thesis
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline section helper
# ─────────────────────────────────────────────────────────────────────────────

def section(label: str) -> None:
    """Print a section banner. Usado por scripts de pipeline (daily_update.*)."""
    print(f"\n{'=' * 60}\n== {label}\n{'=' * 60}")
