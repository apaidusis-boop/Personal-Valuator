"""Envia Windows Toast para eventos prioritários recentes.

Lê de br_investments.db + us_investments.db. Filtra:
  - CVM fatos relevantes de HOLDINGS, últimas N horas
  - SEC 8-K com itens prioritários (1.01, 2.01, 3.03, 5.02, 8.01) de HOLDINGS

Idempotente: mantém um ficheiro `data/notify_state.json` com os IDs de
eventos já notificados. Não repete.

Uso:
    python scripts/notify_events.py              # default: últimas 48h
    python scripts/notify_events.py --hours 24   # janela personalizada
    python scripts/notify_events.py --dry-run    # só imprime, não envia toast
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
STATE_PATH = ROOT / "data" / "notify_state.json"

PRIORITY_8K_ITEMS = ("1.01", "2.01", "3.03", "5.02", "8.01")


def _load_state() -> set[str]:
    if not STATE_PATH.exists():
        return set()
    try:
        return set(json.loads(STATE_PATH.read_text(encoding="utf-8")).get("seen", []))
    except Exception:
        return set()


def _save_state(seen: set[str]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"seen": sorted(seen)}), encoding="utf-8")


def collect_events(hours: int) -> list[dict]:
    """Retorna eventos de HOLDINGS dos últimos N horas que são alta prioridade."""
    since = (date.today() - timedelta(days=max(1, hours // 24 + 1))).isoformat()
    events: list[dict] = []

    # BR: fatos relevantes de holdings
    with sqlite3.connect(DB_BR) as c:
        for eid, tk, d, summ, url in c.execute(
            """SELECT e.id, e.ticker, e.event_date, e.summary, e.url
               FROM events e JOIN companies c ON e.ticker=c.ticker
               WHERE e.source='cvm' AND e.kind='fato_relevante'
                 AND c.is_holding=1 AND e.event_date >= ?
               ORDER BY e.event_date DESC""",
            (since,),
        ).fetchall():
            events.append({
                "id": f"br-{eid}",
                "ticker": tk, "date": d,
                "title": f"Fato Relevante — {tk}",
                "body": (summ or "")[:150],
                "url": url,
                "priority": "high",
            })

    # US: 8-K prioritários de holdings
    with sqlite3.connect(DB_US) as c:
        rows = c.execute(
            """SELECT e.id, e.ticker, e.event_date, e.summary, e.url
               FROM events e JOIN companies c ON e.ticker=c.ticker
               WHERE e.source='sec' AND e.kind='8-K'
                 AND c.is_holding=1 AND e.event_date >= ?
               ORDER BY e.event_date DESC""",
            (since,),
        ).fetchall()
        for eid, tk, d, summ, url in rows:
            if not summ:
                continue
            if not any(it in summ for it in PRIORITY_8K_ITEMS):
                continue
            events.append({
                "id": f"us-{eid}",
                "ticker": tk, "date": d,
                "title": f"8-K — {tk}",
                "body": summ.replace("8-K | ", "")[:150],
                "url": url,
                "priority": "high",
            })

    return events


def send_toast(ev: dict) -> None:
    from win11toast import toast
    kwargs = {
        "title": ev["title"],
        "body": f"{ev['date']}  {ev['body']}",
        "app_id": "Investment Intelligence",
        "duration": "long",
    }
    if ev.get("url"):
        kwargs["on_click"] = ev["url"]
        kwargs["button"] = {
            "activationType": "protocol",
            "arguments": ev["url"],
            "content": "Abrir",
        }
    toast(**kwargs)


def run(hours: int = 48, dry_run: bool = False) -> int:
    seen = _load_state()
    evs = collect_events(hours)
    new = [e for e in evs if e["id"] not in seen]

    print(f"[notify] eventos janela: {len(evs)}  |  já vistos: {len(evs) - len(new)}  |  novos: {len(new)}")
    for e in new:
        print(f"  - {e['ticker']} {e['date']} | {e['title']}: {e['body'][:60]}")
        if not dry_run:
            try:
                send_toast(e)
            except Exception as ex:
                print(f"    [WARN] toast failed: {ex}")
        seen.add(e["id"])

    if not dry_run and new:
        _save_state(seen)
    return len(new)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=48)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    run(hours=args.hours, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
