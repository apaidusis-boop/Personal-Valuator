"""CLI para gerir watchlist_actions (decision journal aberto pelos triggers).

Fecha o loop: triggers abrem rows `open`; o user usa este CLI para as marcar
`resolved` (agi) ou `ignored` (vi e decidi não actuar), com nota contextual.

Uso:
    python scripts/action_cli.py                    # list open (default)
    python scripts/action_cli.py list --all         # inclui resolved/ignored
    python scripts/action_cli.py list --ticker JNJ
    python scripts/action_cli.py resolve 3 --note "comprei 10 @ 234.50"
    python scripts/action_cli.py ignore 4 --note "wait Q earnings"
    python scripts/action_cli.py note 2 "price reviewed, maintaining position"

Zero rede. Apenas toca watchlist_actions. A descoberta em qual DB está a action
(BR vs US) é automática (tenta BR primeiro, depois US).
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _dbs():
    return [(DB_BR, "br"), (DB_US, "us")]


def _parse_ref(ref: str) -> tuple[str | None, int]:
    """Aceita 'br/3', 'us/7' ou '3'. Devolve (market|None, id)."""
    if "/" in ref:
        mkt, num = ref.split("/", 1)
        return (mkt, int(num))
    return (None, int(ref))


def _find_action(action_id: int, market: str | None = None) -> tuple[Path, str] | None:
    matches: list[tuple[Path, str]] = []
    for db, mkt in _dbs():
        if market and mkt != market:
            continue
        with sqlite3.connect(db) as conn:
            r = conn.execute(
                "SELECT 1 FROM watchlist_actions WHERE id=?", (action_id,)
            ).fetchone()
            if r:
                matches.append((db, mkt))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(
            f"ambíguo: id={action_id} existe em várias DBs "
            f"({','.join(m for _, m in matches)}). Use prefixo 'mkt/id' (ex: br/{action_id})."
        )
    return None


def _fetch_all(*, status_filter: str | None, ticker_filter: str | None,
               kind_filter: str | None) -> list[dict]:
    out: list[dict] = []
    for db, mkt in _dbs():
        with sqlite3.connect(db) as conn:
            sql = ("SELECT id, ticker, kind, trigger_id, action_hint, status, "
                   "opened_at, resolved_at, trigger_snapshot_json, notes "
                   "FROM watchlist_actions WHERE 1=1")
            params: list = []
            if status_filter:
                sql += " AND status = ?"; params.append(status_filter)
            if ticker_filter:
                sql += " AND ticker = ?"; params.append(ticker_filter.upper())
            if kind_filter:
                sql += " AND kind = ?"; params.append(kind_filter)
            sql += " ORDER BY opened_at DESC"
            for r in conn.execute(sql, params).fetchall():
                out.append({
                    "id": r[0], "ticker": r[1], "kind": r[2], "trigger_id": r[3],
                    "action_hint": r[4], "status": r[5], "opened_at": r[6],
                    "resolved_at": r[7],
                    "snapshot": json.loads(r[8]) if r[8] else {},
                    "notes": r[9], "market": mkt,
                })
    return out


def _summarize_snapshot(kind: str, snap: dict) -> str:
    """Uma linha curta com o essencial do snapshot para display."""
    if kind == "price_drop_from_high":
        return (f"drop {snap.get('drop_pct','?')}% vs high {snap.get('lookback_days','?')}d "
                f"(price {snap.get('price','?')} ← {snap.get('high_lookback','?')})")
    if kind == "dy_above_pct":
        return f"DY {snap.get('dy_pct','?')}% ≥ {snap.get('threshold_pct','?')}%"
    if kind == "dy_percentile_vs_own_history":
        return (f"DY {snap.get('dy_now_pct','?')}% ≥ P{snap.get('percentile','?')} "
                f"hist {snap.get('dy_threshold_pct','?')}% ({snap.get('lookback_years','?')}y)")
    return json.dumps(snap, ensure_ascii=False)[:80]


def cmd_list(args: argparse.Namespace) -> int:
    rows = _fetch_all(
        status_filter=None if args.all else "open",
        ticker_filter=args.ticker,
        kind_filter=args.kind,
    )
    if not rows:
        print("[nenhuma action]")
        return 0
    print(f"\n{'REF':<8}  {'TICKER':<7}  {'STATUS':<9}  "
          f"{'HINT':<7}  {'OPENED':<12}  DETALHE")
    print("-" * 92)
    for r in rows:
        opened_short = (r["opened_at"] or "")[:10]
        detail = _summarize_snapshot(r["kind"], r["snapshot"])
        ref = f"{r['market']}/{r['id']}"
        print(f"{ref:<8}  {r['ticker']:<7}  {r['status']:<9}  "
              f"{(r['action_hint'] or '-'):<7}  {opened_short:<12}  {detail}")
        if r["notes"]:
            print(f"           note: {r['notes']}")
    print("-" * 90)
    print(f"{len(rows)} action(s)"
          + ("" if args.all else " open (use --all p/ histórico completo)"))
    return 0


def _update(ref: str, *, new_status: str | None, note: str | None,
            market_hint: str | None = None) -> int:
    mkt, aid = _parse_ref(ref)
    if mkt is None and market_hint:
        mkt = market_hint
    try:
        found = _find_action(aid, market=mkt)
    except ValueError as e:
        print(f"[erro] {e}")
        return 1
    if not found:
        print(f"[erro] action #{ref} não existe")
        return 1
    db, _mkt = found
    now_iso = datetime.now(UTC).replace(microsecond=0).isoformat()
    with sqlite3.connect(db) as conn:
        # SQLite não suporta E'\n'; usar char(10). Append com separador só se já há notes.
        if new_status and note:
            conn.execute(
                """UPDATE watchlist_actions
                   SET status=?, resolved_at=?,
                       notes=CASE WHEN notes IS NULL OR notes='' THEN ?
                                  ELSE notes || char(10) || ? END
                   WHERE id=?""",
                (new_status, now_iso, note, note, aid),
            )
        elif new_status:
            conn.execute(
                "UPDATE watchlist_actions SET status=?, resolved_at=? WHERE id=?",
                (new_status, now_iso, aid),
            )
        elif note:
            conn.execute(
                """UPDATE watchlist_actions
                   SET notes=CASE WHEN notes IS NULL OR notes='' THEN ?
                                  ELSE notes || char(10) || ? END
                   WHERE id=?""",
                (note, note, aid),
            )
        conn.commit()
    verb = new_status or "noted"
    print(f"[ok] action {ref} -> {verb}" + (f" (note: {note})" if note else ""))
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    return _update(args.ref, new_status="resolved",
                   note=args.note, market_hint=args.market)


def cmd_ignore(args: argparse.Namespace) -> int:
    return _update(args.ref, new_status="ignored",
                   note=args.note, market_hint=args.market)


def cmd_note(args: argparse.Namespace) -> int:
    return _update(args.ref, new_status=None,
                   note=args.text, market_hint=args.market)


def main() -> None:
    ap = argparse.ArgumentParser(prog="action_cli")
    sub = ap.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="Lista actions (open por default)")
    p_list.add_argument("--all", action="store_true", help="Inclui resolved+ignored")
    p_list.add_argument("--ticker", help="Filtra por ticker")
    p_list.add_argument("--kind", help="Filtra por kind")
    p_list.set_defaults(func=cmd_list)

    p_res = sub.add_parser("resolve", help="Marca como resolvida (agi)")
    p_res.add_argument("ref", help="Ref da action: 'br/1' ou 'us/1' (ou '1' com --market)")
    p_res.add_argument("--market", choices=["br", "us"],
                       help="Desambigua quando ref é só número")
    p_res.add_argument("--note", default="", help="Contexto (ex: 'comprei 10 @ 234.50')")
    p_res.set_defaults(func=cmd_resolve)

    p_ign = sub.add_parser("ignore", help="Marca como ignorada (vi, decidi não actuar)")
    p_ign.add_argument("ref")
    p_ign.add_argument("--market", choices=["br", "us"])
    p_ign.add_argument("--note", default="", help="Razão")
    p_ign.set_defaults(func=cmd_ignore)

    p_nt = sub.add_parser("note", help="Adiciona nota sem mudar status")
    p_nt.add_argument("ref")
    p_nt.add_argument("text")
    p_nt.add_argument("--market", choices=["br", "us"])
    p_nt.set_defaults(func=cmd_note)

    # default = list
    args = ap.parse_args()
    if args.cmd is None:
        ap_list = argparse.Namespace(all=False, ticker=None, kind=None)
        cmd_list(ap_list)
        return
    args.func(args)


if __name__ == "__main__":
    main()
