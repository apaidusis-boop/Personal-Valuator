"""Seed Tier-A US watchlist (Kings/Aristocrats ∩ KNOWN URLs).

Lets Phase C start before full discovery completes.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ri_url_resolver import KNOWN

K_PATH = ROOT / "config" / "kings_aristocrats.yaml"
OUT = ROOT / "config" / "ri_urls_tier_a_us.yaml"


def main():
    if not K_PATH.exists():
        print(f"missing {K_PATH}")
        return
    data = yaml.safe_load(K_PATH.read_text(encoding="utf-8")) or {}
    # Structure is {meta:..., tickers: [{ticker, name, kind, ...}, ...]}
    raw = data.get("tickers", [])
    us_tickers = []
    for entry in raw:
        if isinstance(entry, dict) and "ticker" in entry:
            us_tickers.append(entry["ticker"])
    us_tickers = sorted(set(us_tickers))
    print(f"Found {len(us_tickers)} US Kings/Aristocrats tickers")

    out_data = {}
    matched = 0
    for t in sorted(us_tickers):
        t = str(t).upper()
        if t in KNOWN:
            out_data[t] = {
                "market": "us", "sector": "", "name": "",
                "is_holding": False,
                "ri_urls": KNOWN[t], "method": "known", "status": "ok",
            }
            matched += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(out_data, f, sort_keys=True,
                       allow_unicode=True, default_flow_style=False)
    print(f"matched {matched} / {len(us_tickers)} → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
