"""Backfill `companies.strategy_tag` para todos os tickers (BR + US).

Usa `agents.council.philosophy.compute()` (deterministic, zero LLM) para
classificar cada ticker num primary lens: Value / Growth / Dividend(DRIP) /
Buffett(Quality) / Macro. Persiste o tag em `companies.strategy_tag` para
poder ser lido instantaneamente em panorama / Mission Control / dashboards
sem re-correr o engine.

Idempotente — overwrites o tag em cada run.

Uso:
    python scripts/backfill_strategy_tag.py
    python scripts/backfill_strategy_tag.py --market br
    python scripts/backfill_strategy_tag.py --ticker JNJ      # só um
    python scripts/backfill_strategy_tag.py --schema-only

Schema: assume que coluna `strategy_tag TEXT` já existe em `companies`.
Se faltar (ex: DB nova), corre ALTER idempotente no boot.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.council.philosophy import compute as compute_philosophy

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
LOG_PATH = ROOT / "logs" / "backfill_strategy_tag.log"


def ensure_schema(conn: sqlite3.Connection) -> bool:
    """Adiciona strategy_tag se faltar. Devolve True se foi adicionado agora."""
    try:
        conn.execute("ALTER TABLE companies ADD COLUMN strategy_tag TEXT")
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            return False
        raise


def _build_dossier(ticker: str, conn: sqlite3.Connection, market: str) -> dict | None:
    """Monta dossier minimal a partir do snapshot mais recente em fundamentals."""
    conn.row_factory = sqlite3.Row
    company = conn.execute(
        "SELECT name, sector, is_holding FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not company:
        return None
    fund = conn.execute(
        """SELECT pe, pb, dy, roe, net_debt_ebitda, dividend_streak_years,
                  is_aristocrat, market_cap, fcf_ttm
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    fund_dict = dict(fund) if fund else {}
    return {
        "ticker": ticker,
        "market": market,
        "sector": company["sector"] or "",
        "is_holding": bool(company["is_holding"]),
        "fundamentals": fund_dict,
        "quality_scores": {},
    }


def _format_tag(scores) -> str:
    """Converte PhilosophyScores no tag persistido.

    Format: 'Buffett (10/12)' ou 'Buffett (10/12) | Dividend (8/12)'.
    Se nenhum lens >=4 (threshold em philosophy.py), devolve 'N/A'.
    """
    if not scores.primary:
        return "N/A"
    if scores.secondary:
        return f"{scores.primary} | {scores.secondary}"
    return scores.primary


def _primary_lens(scores) -> str:
    """Apenas a label do primary (sem score) — para distribuição."""
    if not scores.primary:
        return "N/A"
    return scores.primary.split(" (")[0]


def backfill_db(db_path: Path, market: str, only_ticker: str | None,
                log_fp) -> tuple[int, Counter]:
    """Backfill numa DB. Devolve (n_processados, distribuição_de_primary)."""
    if not db_path.exists():
        return 0, Counter()
    counts: Counter = Counter()
    n = 0
    with sqlite3.connect(db_path) as conn:
        ensure_schema(conn)
        if only_ticker:
            tickers = [only_ticker] if conn.execute(
                "SELECT 1 FROM companies WHERE ticker=?", (only_ticker,)
            ).fetchone() else []
        else:
            tickers = [r[0] for r in conn.execute(
                "SELECT ticker FROM companies ORDER BY ticker"
            ).fetchall()]
        for ticker in tickers:
            try:
                dossier = _build_dossier(ticker, conn, market)
                if not dossier:
                    continue
                scores = compute_philosophy(dossier)
                tag = _format_tag(scores)
                conn.execute(
                    "UPDATE companies SET strategy_tag=? WHERE ticker=?",
                    (tag, ticker),
                )
                counts[_primary_lens(scores)] += 1
                n += 1
                log_fp.write(json.dumps({
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "market": market,
                    "ticker": ticker,
                    "tag": tag,
                    "value": scores.value,
                    "growth": scores.growth,
                    "dividend": scores.dividend,
                    "buffett": scores.buffett,
                }, ensure_ascii=False) + "\n")
            except Exception as e:
                log_fp.write(json.dumps({
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "market": market,
                    "ticker": ticker,
                    "error": str(e),
                }, ensure_ascii=False) + "\n")
        conn.commit()
    return n, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--market", choices=["br", "us", "both"], default="both")
    ap.add_argument("--ticker", help="só um ticker (ignora --market filter)")
    ap.add_argument("--schema-only", action="store_true",
                    help="só corre ALTER TABLE, sem backfill")
    args = ap.parse_args()

    if args.schema_only:
        for db in (DB_BR, DB_US):
            if db.exists():
                with sqlite3.connect(db) as c:
                    added = ensure_schema(c)
                    print(f"{db.name}: {'ADDED' if added else 'already exists'}")
        return

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    grand_counts: Counter = Counter()
    with open(LOG_PATH, "a", encoding="utf-8") as log_fp:
        log_fp.write(json.dumps({
            "ts": datetime.now().isoformat(timespec="seconds"),
            "event": "run_start",
            "market": args.market,
            "ticker": args.ticker,
        }) + "\n")
        targets: list[tuple[Path, str]] = []
        if args.market in ("br", "both"):
            targets.append((DB_BR, "br"))
        if args.market in ("us", "both"):
            targets.append((DB_US, "us"))

        for db, mkt in targets:
            n, counts = backfill_db(db, mkt, args.ticker, log_fp)
            total += n
            grand_counts.update(counts)
            dist = ", ".join(f"{k}: {v}" for k, v in counts.most_common())
            print(f"{mkt.upper()}: {n} tickers tagged — {dist or '(nenhum)'}")

        log_fp.write(json.dumps({
            "ts": datetime.now().isoformat(timespec="seconds"),
            "event": "run_end",
            "total": total,
            "distribution": dict(grand_counts),
        }) + "\n")

    print(f"\nTOTAL: {total} tickers tagged")
    print("Distribuição global:")
    for lens, n in grand_counts.most_common():
        print(f"  {lens}: {n}")


if __name__ == "__main__":
    main()
