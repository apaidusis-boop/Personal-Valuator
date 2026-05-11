"""Seed BR watchlist yaml from KNOWN URLs + FII heuristic."""
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ri_url_resolver import KNOWN, ETF_TICKERS, fii_url

OUT = ROOT / "config" / "ri_urls_br_watchlist.yaml"


def main():
    out_data = {}
    db = ROOT / "data" / "br_investments.db"
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    try:
        for r in c.execute(
            "SELECT ticker, name, sector FROM companies "
            "WHERE is_holding=0 ORDER BY ticker"
        ).fetchall():
            t = r["ticker"]
            if t in ETF_TICKERS:
                continue
            if t in KNOWN:
                out_data[t] = {
                    "market": "br", "sector": r["sector"] or "",
                    "name": r["name"] or "", "is_holding": False,
                    "ri_urls": KNOWN[t], "method": "known", "status": "ok",
                }
            elif t.endswith("11"):
                out_data[t] = {
                    "market": "br", "sector": r["sector"] or "",
                    "name": r["name"] or "", "is_holding": False,
                    "ri_urls": [fii_url(t)],
                    "method": "fii_heuristic", "status": "ok",
                }
    finally:
        c.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(out_data, f, sort_keys=True,
                       allow_unicode=True, default_flow_style=False)
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(out_data)} BR watchlist tickers")


if __name__ == "__main__":
    main()
