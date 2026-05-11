"""Política de cache centralizada.

Princípio: dados históricos são imutáveis. Uma vez buscados, ficam.
Apenas dados do período corrente (ou recém-fechados) são refrescados.

Funções de consulta: is_fresh(...) devolve True se o dado em DB já é
bom o suficiente para o contexto e NÃO precisa de re-fetch.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal


# ---------- políticas declarativas ----------

# TTL por tipo de dado, em dias. 0 = refresh sempre. None = imutável.
POLICY = {
    "price_past":               None,   # fechado, nunca muda
    "price_today":              1,      # refrescar no mesmo dia se re-corrermos
    "dividend_past_year":       None,   # ano fechado, imutável
    "dividend_current_year":    7,      # ano em curso, refrescar semanal
    "fundamental_snapshot":     1,      # snapshot do trimestre corrente, refrescar diário
    "statement_closed_year":    None,   # anos N-2 e anteriores imutáveis
    "statement_recent_year":    180,    # último ano fechado — revisões podem ocorrer até 6 meses
    "statement_current_period": 30,     # trimestre em curso, refrescar mensal
    "event_full_text":          None,   # PDF extraído uma vez, imutável
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_fresh(
    fetched_at: str | None,
    policy_key: str,
    *,
    now: datetime | None = None,
) -> bool:
    """Devolve True se os dados em DB ainda são bons sob a política indicada.

    Rule:
      - se nunca foi buscado → False (precisa buscar)
      - se política é None (imutável) e já foi buscado → True (nunca re-buscar)
      - caso contrário: True se idade < TTL
    """
    if fetched_at is None:
        return False
    ttl_days = POLICY.get(policy_key, 0)
    if ttl_days is None:
        return True  # imutável + já temos = fresh
    fetched = _parse_iso(fetched_at)
    if fetched is None:
        return False
    now = now or datetime.now(timezone.utc)
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    age = now - fetched
    return age < timedelta(days=ttl_days)


def statement_policy_for(period_end: str, period_type: Literal["annual", "quarterly"]) -> str:
    """Escolhe a chave de política correta para um statement, com base
    em quão antigo é o período."""
    try:
        pe = datetime.fromisoformat(period_end[:10])
    except ValueError:
        return "statement_current_period"
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    age_days = (now - pe).days
    if period_type == "annual":
        if age_days > 365 * 2:      # anos N-2 ou anteriores
            return "statement_closed_year"
        if age_days > 180:            # último ano fechado
            return "statement_recent_year"
        return "statement_current_period"
    # quarterly
    if age_days > 365:
        return "statement_closed_year"
    if age_days > 90:
        return "statement_recent_year"
    return "statement_current_period"


# ---------- formatters partilhados (display) ----------

def fmt_date_br(iso: str | None) -> str:
    """ISO YYYY-MM-DD → DD/MM/YYYY. Tolera None e strings parciais."""
    if not iso:
        return "—"
    s = str(iso)[:10]
    try:
        y, m, d = s.split("-")
        return f"{d}/{m}/{y}"
    except ValueError:
        return s


def parse_date_br(s: str) -> str:
    """DD/MM/YYYY → YYYY-MM-DD (ISO). Tolera já-ISO."""
    s = s.strip()
    if "/" in s:
        d, m, y = s.split("/")
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
    return s
