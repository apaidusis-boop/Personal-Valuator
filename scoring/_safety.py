"""scoring._safety — per-sector safety margin lookup + triplet emission.

Reads `config/safety_margins.yaml`. Resolves margin for (market, sector,
ticker) with this precedence:

    1. ticker_overrides.<market>.<TICKER>
    2. <market>.<sector>
    3. defaults

Returns either a float pct (e.g. 18.0) or None (not applicable / explicit
opt-out via null in YAML).

Triplet builder (`build_triplet`) takes consensus_fair + price + margin and
returns the (buy_below, hold_low, hold_high, sell_above, action) tuple used
across fair_value engine + dossier writer.

Action vocab matches the 6-stance verdict (Phase FF Bloco 3.1 close):
    STRONG_BUY  : price ≤ buy_below × 0.90  (10% under our_fair → very rare)
    BUY         : buy_below × 0.90 < price ≤ buy_below
    HOLD        : buy_below < price ≤ hold_high  (between our_fair and consensus)
    TRIM        : hold_high < price ≤ sell_above  (overvalued vs consensus)
    SELL        : price > sell_above
    N/A         : margin is None (ETF / tactical / opt-out)
"""
from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "safety_margins.yaml"


@functools.lru_cache(maxsize=1)
def _load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"defaults": {"safety_margin_pct": 25.0, "overvaluation_pct": 15.0},
                "br": {}, "us": {}, "ticker_overrides": {}}
    with CONFIG_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def reload_config() -> None:
    """Drop the cached config (useful in tests / live edits)."""
    _load_config.cache_clear()


def resolve_margin(market: str, sector: str | None, ticker: str | None = None) -> float | None:
    """Return safety_margin_pct (e.g. 18.0) or None if explicitly opted out.

    Falls back to defaults.safety_margin_pct if sector unknown.
    """
    cfg = _load_config()
    market = market.lower()

    if ticker:
        override = (cfg.get("ticker_overrides", {}) or {}).get(market, {}).get(ticker.upper())
        if override is not None:
            return override.get("safety_margin_pct")

    sector_map = cfg.get(market, {}) or {}
    if sector and sector in sector_map:
        entry = sector_map[sector]
        if entry is None:
            return None
        return entry.get("safety_margin_pct")

    return (cfg.get("defaults", {}) or {}).get("safety_margin_pct", 25.0)


def overvaluation_pct() -> float:
    return float((_load_config().get("defaults", {}) or {}).get("overvaluation_pct", 15.0))


def build_triplet(consensus_fair: float, price: float, margin_pct: float | None) -> dict:
    """Compute (our_fair, buy_below, hold_low, hold_high, sell_above, action).

    `margin_pct` None -> action "N/A" and triplet collapses to consensus only.
    """
    if margin_pct is None:
        return {
            "our_fair": None, "buy_below": None,
            "hold_low": None, "hold_high": None,
            "sell_above": None,
            "action": "N/A",
            "margin_pct": None,
            "consensus_fair": round(consensus_fair, 4),
            "price": round(price, 4),
        }

    margin = float(margin_pct) / 100.0
    over = overvaluation_pct() / 100.0
    our_fair = consensus_fair * (1.0 - margin)
    sell_above = consensus_fair * (1.0 + over)

    if price <= our_fair * 0.90:
        action = "STRONG_BUY"
    elif price <= our_fair:
        action = "BUY"
    elif price <= consensus_fair:
        action = "HOLD"
    elif price <= sell_above:
        action = "TRIM"
    else:
        action = "SELL"

    return {
        "consensus_fair": round(consensus_fair, 4),
        "our_fair": round(our_fair, 4),
        "buy_below": round(our_fair, 4),
        "hold_low": round(our_fair, 4),
        "hold_high": round(consensus_fair, 4),
        "sell_above": round(sell_above, 4),
        "price": round(price, 4),
        "action": action,
        "margin_pct": float(margin_pct),
    }
