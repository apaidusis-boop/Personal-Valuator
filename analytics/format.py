"""Helpers de formatação para a camada de apresentação.

DB guarda tudo em ISO 8601 (YYYY-MM-DD) — convenção trancada em CLAUDE.md.
Estes helpers existem apenas para converter à vista do utilizador em PT-BR:
datas como dd/mm/yyyy.

Regras:
  - `br_date(iso)` aceita 'YYYY-MM-DD' ou prefixo maior ('2026-04-19T17:28:44Z');
     devolve 'dd/mm/yyyy'. Se input for None/'' ou inválido, devolve '—'.
  - `br_datetime(iso)` para timestamps — inclui hora 'dd/mm/yyyy HH:MM'.
  - Ambos tolerantes a None para simplificar o uso em f-strings.
"""
from __future__ import annotations

from datetime import date, datetime


def br_date(iso: str | date | datetime | None) -> str:
    """'2026-04-19' -> '19/04/2026'. Input vazio/inválido -> '—'."""
    if iso is None or iso == "":
        return "—"
    if isinstance(iso, datetime):
        return iso.strftime("%d/%m/%Y")
    if isinstance(iso, date):
        return iso.strftime("%d/%m/%Y")
    s = str(iso)
    # aceita '2026-04-19' ou '2026-04-19T...' ou '2026-04-19 ...'
    if len(s) < 10:
        return "—"
    try:
        d = date.fromisoformat(s[:10])
    except ValueError:
        return "—"
    return d.strftime("%d/%m/%Y")


def br_datetime(iso: str | datetime | None) -> str:
    """'2026-04-19T17:28:44Z' -> '19/04/2026 17:28'. Input inválido -> '—'."""
    if iso is None or iso == "":
        return "—"
    if isinstance(iso, datetime):
        return iso.strftime("%d/%m/%Y %H:%M")
    s = str(iso).replace("Z", "+00:00")
    # fallback para só-data
    if "T" not in s and " " not in s:
        return br_date(s)
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return br_date(s)
    return dt.strftime("%d/%m/%Y %H:%M")
