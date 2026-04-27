"""Auto-populate catalog.yaml watchlist section from universe.yaml + cad_cia_aberta.csv.

Strategy:
  1. Read config/universe.yaml — collect BR watchlist stock tickers
  2. For each ticker, lookup CVM record by name pattern + cross-validate
  3. Update library/ri/catalog.yaml with `watchlist_stocks` section
  4. Output validation summary

Smart matching:
  - First try by cvm_name (substring) in DENOM_SOCIAL
  - Filter to SIT='ATIVO' (skip cancelled)
  - If multiple matches, prefer Categoria A (formal cia aberta)
  - Manual review still recommended for ambiguous

Uso:
    python -m library.ri.catalog_autopopulate plan      # dry-run, show matches
    python -m library.ri.catalog_autopopulate apply     # write to catalog.yaml
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
UNIVERSE = ROOT / "config" / "universe.yaml"
CATALOG = ROOT / "library" / "ri" / "catalog.yaml"
CAD = ROOT / "library" / "ri" / "cache" / "cad_cia_aberta.csv"


def _read_cad() -> list[dict]:
    if not CAD.exists():
        # try fetch
        from library.ri.cvm_codes import fetch_cad
        fetch_cad()
    with open(CAD, encoding="latin-1", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _normalize(s: str) -> str:
    """Lowercase, strip accents, only ASCII alphanumeric."""
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", s or "")
    only_ascii = nfkd.encode("ASCII", "ignore").decode().lower()
    return "".join(c for c in only_ascii if c.isalnum())


def find_cvm_match(cad_rows: list[dict], cvm_name_hint: str | None,
                   ticker: str) -> dict | None:
    """Find best match: by cvm_name first, then by ticker root."""
    candidates = [r for r in cad_rows if r.get("SIT") == "ATIVO"]

    # Try cvm_name first
    if cvm_name_hint:
        hint_norm = _normalize(cvm_name_hint)
        hits = [r for r in candidates if hint_norm in _normalize(r.get("DENOM_SOCIAL", ""))]
        if hits:
            # Prefer Categoria A
            cat_a = [r for r in hits if r.get("CATEG_REG") == "Categoria A"]
            if cat_a:
                return cat_a[0]
            return hits[0]

    # Fallback: ticker root (drop trailing digits)
    root = ticker.rstrip("0123456789").rstrip().upper()
    if len(root) >= 3:
        root_norm = _normalize(root)
        hits = [r for r in candidates if root_norm in _normalize(r.get("DENOM_SOCIAL", ""))]
        if hits:
            cat_a = [r for r in hits if r.get("CATEG_REG") == "Categoria A"]
            if cat_a:
                return cat_a[0]
            return hits[0]
    return None


def plan() -> dict:
    sys.stdout.reconfigure(encoding="utf-8")
    universe = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    br_watch = universe.get("br", {}).get("watchlist", {}).get("stocks", [])
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))

    # Existing tickers in catalog (skip duplicates)
    existing = set()
    for entry in catalog.get("stocks", []) + catalog.get("watchlist_stocks", []):
        existing.add(entry["ticker"])

    cad_rows = _read_cad()
    plan_entries = []
    print(f"=== Plan: {len(br_watch)} watchlist stocks to validate ===\n")

    for u in br_watch:
        ticker = u["ticker"]
        if ticker in existing:
            print(f"  SKIP {ticker:<8} (already in catalog)")
            continue
        cvm_hint = u.get("cvm_name")
        match = find_cvm_match(cad_rows, cvm_hint, ticker)
        if not match:
            print(f"  MISS {ticker:<8} hint={cvm_hint!r:<25} (no CAD row found)")
            continue
        cvm_code = match.get("CD_CVM")
        cnpj = match.get("CNPJ_CIA")
        denom = match.get("DENOM_SOCIAL", "")[:50]
        print(f"  OK   {ticker:<8} cvm={cvm_code:<8} cnpj={cnpj}  {denom}")
        plan_entries.append({
            "ticker": ticker,
            "name": u.get("name", denom),
            "cnpj": cnpj,
            "codigo_cvm": int(cvm_code) if cvm_code else None,
            "ri_url": "TODO",          # manual fill later
            "filings": ["DFP", "ITR", "FRE", "IPE", "FCA"],
            "sector": u.get("sector"),
            "auto_populated": True,
            "notes": f"Auto-populated 2026-04-25 via universe.yaml ↔ cad_cia_aberta.csv. "
                     f"CVM denom: {denom}. RI URL needs manual curation.",
        })

    print(f"\n=== Summary ===")
    print(f"To add: {len(plan_entries)}")
    print(f"Already in catalog: {sum(1 for u in br_watch if u['ticker'] in existing)}")
    return {"entries": plan_entries, "catalog": catalog}


def apply() -> None:
    p = plan()
    catalog = p["catalog"]
    if not p["entries"]:
        print("\nNothing to add.")
        return
    catalog.setdefault("watchlist_stocks", []).extend(p["entries"])
    # Re-write
    yaml_text = yaml.dump(catalog, sort_keys=False, allow_unicode=True, default_flow_style=False)
    CATALOG.write_text(yaml_text, encoding="utf-8")
    print(f"\nApplied: catalog.yaml now has {len(catalog['watchlist_stocks'])} watchlist_stocks entries")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "apply"])
    args = ap.parse_args()
    if args.cmd == "plan":
        plan()
    else:
        apply()


if __name__ == "__main__":
    main()
