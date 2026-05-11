"""Patch config/ri_urls.yaml with manually-validated URLs for tickers
that failed discovery.

Edit MANUAL_PATCH below with new mappings, then run.
"""
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT / "config" / "ri_urls.yaml"

# Manually mapped URLs (validated 2026-05-10 via _tmp_probe_urls.py).
MANUAL_PATCH: dict[str, list[str]] = {
    # BR mid-caps confirmed working:
    "ABCB4":  ["https://ri.abcbrasil.com.br/"],
    "BRKM5":  ["https://www.braskem-ri.com.br/"],
    "ENGI11": ["https://ri.energisa.com.br/"],
    "EZTC3":  ["https://ri.eztec.com.br/"],
    "GMAT3":  ["https://ri.grupomateus.com.br/"],
    "ISAE4":  ["https://www.isacteep.com.br/ri/"],
    "PGMN3":  ["https://ri.paguemenos.com.br/"],
    "PLPL3":  ["https://ri.planoeplano.com.br/"],
    # Still need investigation: ALOS3 (403), ALUP11 (SSL), BRBI11,
    # PNVL3 (DNS), AURA33 (SSL), AXIA7
}


def probe(url: str, timeout: int = 8) -> tuple[bool, int]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0",
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout,
                         allow_redirects=True, stream=True)
        r.close()
        return r.status_code < 400, r.status_code
    except Exception:
        return False, 0


def main():
    if not YAML.exists():
        print(f"ERROR: {YAML} not found")
        sys.exit(1)
    if not MANUAL_PATCH:
        print("No manual patches in MANUAL_PATCH. Edit script first.")
        return
    with YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    patched = 0
    for ticker, urls in MANUAL_PATCH.items():
        # Probe each URL
        valid = []
        for u in urls:
            ok, code = probe(u)
            print(f"  {ticker}: {u} → HTTP {code} {'✅' if ok else '❌'}")
            if ok:
                valid.append(u)
        if not valid:
            print(f"  {ticker}: no valid URLs, skipping patch")
            continue
        if ticker not in data:
            data[ticker] = {"market": "br", "is_holding": False,
                            "ri_urls": valid, "method": "manual",
                            "status": "ok"}
        else:
            data[ticker]["ri_urls"] = valid
            data[ticker]["method"] = "manual"
            data[ticker]["status"] = "ok"
        patched += 1
    with YAML.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True,
                       default_flow_style=False)
    print(f"\nPatched {patched} tickers in {YAML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
