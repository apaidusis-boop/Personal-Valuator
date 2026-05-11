"""Seed config/ri_urls_holdings.yaml from KNOWN mappings + DB holdings.

Faster than full discovery — covers all holdings we have URLs for, without
waiting for discovery to finish probing watchlist failures.
"""
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ri_url_resolver import KNOWN, ETF_TICKERS, fii_url

OUT = ROOT / "config" / "ri_urls_holdings.yaml"


def main():
    out_data = {}
    for db_rel, market in [
        ("data/br_investments.db", "br"),
        ("data/us_investments.db", "us"),
    ]:
        c = sqlite3.connect(ROOT / db_rel)
        c.row_factory = sqlite3.Row
        try:
            for r in c.execute(
                "SELECT ticker, name, sector FROM companies "
                "WHERE is_holding=1 ORDER BY ticker"
            ).fetchall():
                t = r["ticker"]
                if t in ETF_TICKERS:
                    out_data[t] = {
                        "market": market, "sector": r["sector"] or "",
                        "name": r["name"] or "", "is_holding": True,
                        "ri_urls": [], "method": "etf",
                        "status": "skipped",
                        "notes": "ETF — no corporate RI",
                    }
                    continue
                if t in KNOWN:
                    out_data[t] = {
                        "market": market, "sector": r["sector"] or "",
                        "name": r["name"] or "", "is_holding": True,
                        "ri_urls": KNOWN[t], "method": "known",
                        "status": "ok",
                    }
                    continue
                # FII heuristic
                if market == "br" and t.endswith("11"):
                    out_data[t] = {
                        "market": market, "sector": r["sector"] or "",
                        "name": r["name"] or "", "is_holding": True,
                        "ri_urls": [fii_url(t)],
                        "method": "fii_heuristic", "status": "ok",
                    }
                    continue
                # No KNOWN, no FII pattern → mark needs discovery
                out_data[t] = {
                    "market": market, "sector": r["sector"] or "",
                    "name": r["name"] or "", "is_holding": True,
                    "ri_urls": [], "method": "unknown",
                    "status": "failed",
                    "notes": "needs heuristic discovery",
                }
        finally:
            c.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(out_data, f, sort_keys=True,
                       allow_unicode=True, default_flow_style=False)
    ok = sum(1 for c in out_data.values() if c["status"] == "ok")
    fail = sum(1 for c in out_data.values() if c["status"] == "failed")
    skip = sum(1 for c in out_data.values() if c["status"] == "skipped")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  ok: {ok}, failed: {fail}, skipped: {skip}, total: {len(out_data)}")


if __name__ == "__main__":
    main()
