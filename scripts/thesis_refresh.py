"""thesis_refresh — injeta/atualiza "Live snapshot" em wiki/holdings/*.md.

Para cada thesis note em `obsidian_vault/wiki/holdings/<X>.md`, computa
metrics via `analytics.metrics.compute_all` e injecta o bloco markdown
entre marcadores idempotentes. Re-run substitui o bloco.

Fonte de métricas: analytics/metrics.py (drawdowns, CAGR, vol, Sharpe,
DY avg, div CAGR, streak, P/E vs own avg).

Uso:
    python scripts/thesis_refresh.py                    # all holdings
    python scripts/thesis_refresh.py --ticker VALE3     # single
    ii refresh-thesis                                   # via CLI
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from analytics.metrics import compute_all, render_markdown_snapshot  # noqa: E402

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

BEGIN_MARKER = "<!-- LIVE_SNAPSHOT:BEGIN -->"
END_MARKER = "<!-- LIVE_SNAPSHOT:END -->"


def _detect_market(ticker: str) -> str:
    with sqlite3.connect(DB_BR) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
            return "br"
    with sqlite3.connect(DB_US) as c:
        if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
            return "us"
    return "us"


def _inject_snapshot(text: str, snapshot_md: str) -> str:
    """Injecta ou substitui bloco entre BEGIN/END markers.
    Se markers não existem, insere ANTES de "## Related" (ou no final do ficheiro)."""
    stamp = f"_Atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    block = f"{BEGIN_MARKER}\n{stamp}{snapshot_md}\n{END_MARKER}"

    pattern = re.compile(
        re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text)

    # inserir antes de "## Related" se existe
    related_idx = text.find("\n## Related")
    if related_idx >= 0:
        return text[:related_idx] + "\n\n" + block + "\n" + text[related_idx:]

    # inserir antes de "## Memory refs"
    mem_idx = text.find("\n## Memory refs")
    if mem_idx >= 0:
        return text[:mem_idx] + "\n\n" + block + "\n" + text[mem_idx:]

    # fallback: no final
    return text.rstrip() + "\n\n" + block + "\n"


def refresh_one(holdings_dir: Path, ticker: str) -> tuple[bool, str]:
    path = holdings_dir / f"{ticker}.md"
    if not path.exists():
        return (False, f"no thesis note ({path.name})")
    market = _detect_market(ticker)
    db = DB_BR if market == "br" else DB_US
    if not db.exists():
        return (False, f"db {db.name} missing")
    with sqlite3.connect(db) as c:
        m = compute_all(c, ticker)
    snapshot = render_markdown_snapshot(m)
    old = path.read_text(encoding="utf-8")
    new = _inject_snapshot(old, snapshot)
    if new == old:
        return (False, "no change")
    path.write_text(new, encoding="utf-8")
    return (True, "refreshed")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ticker", help="refresh single ticker; default = all")
    ap.add_argument("--vault", help="override vault path")
    args = ap.parse_args()

    vault = Path(args.vault) if args.vault else ROOT / "obsidian_vault"
    holdings_dir = vault / "wiki" / "holdings"
    if not holdings_dir.is_dir():
        print(f"[!] holdings dir not found: {holdings_dir}")
        return 1

    if args.ticker:
        tickers = [args.ticker.upper()]
    else:
        # all thesis notes (skip _README)
        tickers = sorted(
            p.stem for p in holdings_dir.glob("*.md")
            if not p.stem.startswith("_")
        )

    refreshed, skipped = 0, 0
    for t in tickers:
        ok, msg = refresh_one(holdings_dir, t)
        icon = "✓" if ok else "·"
        print(f"  {icon} {t:<8} {msg}")
        if ok:
            refreshed += 1
        else:
            skipped += 1
    print(f"\n{refreshed} refreshed, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
