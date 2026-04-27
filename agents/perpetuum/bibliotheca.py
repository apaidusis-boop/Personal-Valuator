"""Bibliotheca Perpetuum — proactive librarian for the companies catalog.

USER REQUEST (2026-04-26): "vejo que existem várias coisas sem suas devidas
categorias. Precisamos que a Bibliotheca seja mais pró-activa em buscar coisas
e tudo sem categoria e melhores práticas bibliotecárias."

Counterpart to `data_coverage` (which scores HOLDINGS coverage). Bibliotheca
audits the *catalog itself* — every row in `companies`, holding or not — for
librarian-quality issues: missing sector, non-canonical sector, generic name
(name == ticker), and orphan rows (in DB but not in universe.yaml).

Subjects: every (market, ticker) row in either DB.

Signals (each = -25 pts, min score 0):
  BIB001 SECTOR_NULL          — companies.sector IS NULL
  BIB002 SECTOR_NONCANONICAL  — sector not in CANONICAL_SECTORS and not in alias map
  BIB003 NAME_GENERIC         — name == ticker (placeholder from auto-onboard)
  BIB004 ORPHAN               — in DB, NOT in universe.yaml, NOT a holding

Action hint: `python scripts/bibliotheca_autofix.py --apply` covers the
mechanical fixes. ORPHAN rows surface for human triage (delete vs add to
universe.yaml).

T1 Observer. Auto-fix lives in scripts/bibliotheca_autofix.py — kept separate
so the perpetuum stays read-only and idempotent.

Zero LLM. Pure SQL + YAML.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject
from library.sector_taxonomy import is_canonical, is_known_alias

UNIVERSE = ROOT / "config" / "universe.yaml"
KINGS_ARISTOCRATS = ROOT / "config" / "kings_aristocrats.yaml"  # auto-loaded for US screen
DBS = {
    "br": ROOT / "data" / "br_investments.db",
    "us": ROOT / "data" / "us_investments.db",
}

PENALTY = 25  # 4 signals → 0..100 in 25-pt steps


def _walk_universe(market_root: dict) -> set[str]:
    """Flatten universe.yaml under one market and return the set of tickers."""
    out: set[str] = set()

    def _visit(node):
        if isinstance(node, list):
            for item in node:
                _visit(item)
        elif isinstance(node, dict):
            t = node.get("ticker")
            if t and isinstance(t, str):
                out.add(t)
            else:
                for v in node.values():
                    _visit(v)

    _visit(market_root)
    return out


_UNIVERSE_CACHE: dict[str, set[str]] | None = None


def _universe_tickers() -> dict[str, set[str]]:
    global _UNIVERSE_CACHE
    if _UNIVERSE_CACHE is None:
        with open(UNIVERSE, encoding="utf-8") as f:
            u = yaml.safe_load(f)
        cache = {m: _walk_universe(u.get(m, {})) for m in DBS}
        # Treat config/kings_aristocrats.yaml as a US universe extension —
        # those tickers are auto-loaded by yf_us_fetcher for screening, so
        # they aren't orphans even though they live outside universe.yaml.
        if KINGS_ARISTOCRATS.exists():
            with open(KINGS_ARISTOCRATS, encoding="utf-8") as f:
                ka = yaml.safe_load(f) or {}
            cache["us"] |= _walk_universe(ka)
        _UNIVERSE_CACHE = cache
    return _UNIVERSE_CACHE


class BibliothecaPerpetuum(BasePerpetuum):
    name = "bibliotheca"
    description = "Catálogo: sector tagging, naming, orphan detection (librarian-quality)"
    autonomy_tier = "T1"  # Observer; promote to T2 once autofix is trusted in cron
    drop_alert_threshold = 25

    def subjects(self) -> list[PerpetuumSubject]:
        out: list[PerpetuumSubject] = []
        for market, db in DBS.items():
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    "SELECT ticker, name, sector, is_holding FROM companies"
                ).fetchall()
            for ticker, name, sector, is_holding in rows:
                out.append(PerpetuumSubject(
                    id=f"{market}:{ticker}",
                    label=ticker,
                    metadata={
                        "market": market,
                        "ticker": ticker,
                        "name": name,
                        "sector": sector,
                        "is_holding": bool(is_holding),
                    },
                ))
        return out

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        m = subject.metadata
        ticker = m["ticker"]
        name = m["name"]
        sector = m["sector"]
        is_holding = m["is_holding"]
        market = m["market"]

        flags: list[str] = []
        action_hints: list[str] = []

        # BIB001 — NULL sector
        if sector is None:
            flags.append("BIB001 SECTOR_NULL")
            action_hints.append("python scripts/bibliotheca_autofix.py --apply")

        # BIB002 — non-canonical & no known alias to canonical
        elif not is_canonical(sector) and not is_known_alias(sector):
            flags.append(f"BIB002 SECTOR_NONCANONICAL ({sector!r})")
            action_hints.append(
                f"add alias for {sector!r} in library/sector_taxonomy.py "
                "or change sector in universe.yaml"
            )

        # BIB003 — placeholder name
        if name == ticker:
            flags.append("BIB003 NAME_GENERIC (name==ticker)")
            action_hints.append(
                f"add real name for {ticker} in config/universe.yaml, "
                "then run scripts/bibliotheca_autofix.py --apply"
            )

        # BIB004 — orphan (in DB but not in universe.yaml AND not a holding)
        # Holdings legitimately may be auto-onboarded from positions import,
        # so we don't penalize them. Non-holding orphans are the librarian's
        # cleanup pile.
        universe = _universe_tickers().get(market, set())
        if ticker not in universe and not is_holding:
            flags.append("BIB004 ORPHAN (not in universe.yaml, not holding)")
            action_hints.append(
                f"add {ticker} to config/universe.yaml watchlist or "
                f"DELETE FROM companies WHERE ticker='{ticker}'"
            )

        score = max(0, 100 - PENALTY * len(flags))
        action_hint = "; ".join(dict.fromkeys(action_hints)) if action_hints else None

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "market": market,
                "ticker": ticker,
                "name": name,
                "sector": sector,
                "is_holding": is_holding,
                "flags": flags,
            },
            action_hint=action_hint,
        )
