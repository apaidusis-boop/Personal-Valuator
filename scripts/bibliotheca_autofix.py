"""Bibliotheca autofix — safe one-shot librarian repairs.

Three fixes, all idempotent:

  1. SECTOR_NULL → backfill from `config/universe.yaml` when canonical truth
     exists there. Never overwrites an existing sector.
  2. ENCODING_BROKEN → repair latin1-mangled UTF-8 ("H?brido" → "Híbrido",
     "Log?stica" → "Logística"). Uses the alias map.
  3. NAME_GENERIC → if name == ticker AND universe.yaml has a real name,
     use the real name.

Hardcoded fallbacks for tickers NOT in universe.yaml but obviously
classifiable (ABCB4 = Banco ABC Brasil, BPAC11 = BTG Pactual). Keep this
list TINY — the right place for new mappings is universe.yaml itself, so
the perpetuum stays in sync.

Usage:
    python scripts/bibliotheca_autofix.py            # dry-run
    python scripts/bibliotheca_autofix.py --apply    # execute writes

Exit code 0 always (this is a maintenance utility, not a check).
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from library.sector_taxonomy import normalize, is_canonical

UNIVERSE = ROOT / "config" / "universe.yaml"
DBS = {
    "br": ROOT / "data" / "br_investments.db",
    "us": ROOT / "data" / "us_investments.db",
}

# Tickers that exist in the DB but are missing from universe.yaml. Keep this
# minimal — extend universe.yaml instead whenever possible.
HARDCODED_FALLBACKS: dict[str, dict[str, str]] = {
    "ABCB4":  {"name": "Banco ABC Brasil", "sector": "Banks"},
    "BPAC11": {"name": "BTG Pactual",      "sector": "Banks"},
}


def _walk_universe(market_root: dict) -> dict[str, dict]:
    """Flatten universe.yaml under one market into {ticker: {name, sector}}.

    universe.yaml has nested groups (holdings.stocks, holdings.fiis,
    watchlist.stocks, research_pool.stocks, etc.) — we walk all of them.
    """
    out: dict[str, dict] = {}

    def _visit(node):
        if isinstance(node, list):
            for item in node:
                _visit(item)
        elif isinstance(node, dict):
            ticker = node.get("ticker")
            if ticker and isinstance(ticker, str):
                # Use first occurrence (holdings beat watchlist beat research_pool
                # in YAML order — first writer wins is fine here).
                if ticker not in out:
                    sector = node.get("sector") or node.get("segment")
                    out[ticker] = {
                        "name": node.get("name"),
                        "sector": sector,
                    }
            else:
                for v in node.values():
                    _visit(v)

    _visit(market_root)
    return out


def _load_universe() -> dict[str, dict[str, dict]]:
    with open(UNIVERSE, encoding="utf-8") as f:
        u = yaml.safe_load(f)
    return {market: _walk_universe(u.get(market, {})) for market in DBS}


def _fixes_for_market(market: str, db: Path, universe: dict) -> list[tuple]:
    """Return list of (ticker, new_name, new_sector, reasons[]) needing write."""
    if not db.exists():
        return []

    out: list[tuple] = []
    with sqlite3.connect(db) as c:
        rows = c.execute(
            "SELECT ticker, name, sector FROM companies"
        ).fetchall()

    for ticker, cur_name, cur_sector in rows:
        reasons: list[str] = []
        new_name = cur_name
        new_sector = cur_sector

        u_entry = universe.get(ticker) or HARDCODED_FALLBACKS.get(ticker, {})
        u_name = u_entry.get("name")
        u_sector_raw = u_entry.get("sector")
        u_sector = normalize(u_sector_raw)

        # Fix 1: NULL sector -> backfill if we have a canonical answer.
        if cur_sector is None and u_sector and is_canonical(u_sector):
            new_sector = u_sector
            reasons.append(f"SECTOR_NULL -> {u_sector} (universe)")

        # Fix 2: non-canonical sector that maps to a canonical one (handles
        # mojibake too, since aliases include H?brido -> Hibrido).
        elif cur_sector and not is_canonical(cur_sector):
            normalized = normalize(cur_sector)
            if normalized and normalized != cur_sector and is_canonical(normalized):
                new_sector = normalized
                reasons.append(f"ALIAS: {cur_sector!r} -> {normalized!r}")

        # Fix 3: name == ticker and universe has a real name.
        if cur_name == ticker and u_name and u_name != ticker:
            new_name = u_name
            reasons.append(f"NAME_GENERIC -> {u_name!r}")

        if reasons:
            out.append((ticker, new_name, new_sector, reasons))

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true",
                        help="Execute writes (default: dry-run)")
    args = parser.parse_args()

    universe = _load_universe()
    total_fixes = 0
    total_skipped = 0

    for market, db in DBS.items():
        fixes = _fixes_for_market(market, db, universe.get(market, {}))
        if not fixes:
            print(f"[{market}] nothing to fix")
            continue

        print(f"[{market}] {len(fixes)} fixes:")
        for ticker, new_name, new_sector, reasons in fixes:
            print(f"  {ticker:<8} {' | '.join(reasons)}")
            total_fixes += 1

        if args.apply:
            with sqlite3.connect(db) as c:
                for ticker, new_name, new_sector, _ in fixes:
                    c.execute(
                        "UPDATE companies SET name=?, sector=? WHERE ticker=?",
                        (new_name, new_sector, ticker),
                    )
                c.commit()
            print(f"[{market}] applied {len(fixes)} writes")
        else:
            total_skipped += len(fixes)

    if not args.apply and total_fixes:
        print(f"\nDRY-RUN — {total_skipped} fixes pending. Re-run with --apply.")
    elif args.apply:
        print(f"\nApplied {total_fixes} fixes total.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
