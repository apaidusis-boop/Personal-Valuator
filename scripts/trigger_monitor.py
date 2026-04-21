"""Avalia triggers declarativos de config/triggers.yaml e abre rows em
`watchlist_actions` quando disparam.

Zero rede: consome apenas `prices`, `dividends`, `companies`, `fundamentals`
das DBs BR/US. O pipeline diário já populou tudo antes de este script correr.

Idempotente por dia: o índice parcial `ux_wa_open_daily` garante que o mesmo
(ticker, kind, trigger_id) não abre duas rows no mesmo dia enquanto
a primeira estiver `open`. Resolver a row (user marca resolved/ignored) libera
para re-abrir no dia seguinte se a condição persistir.

Log JSON (1 linha por hit + 1 linha `summary`) em logs/trigger_monitor_YYYY-MM-DD.log.

Uso:
    python scripts/trigger_monitor.py
    python scripts/trigger_monitor.py --dry-run
    python scripts/trigger_monitor.py --market us
    python scripts/trigger_monitor.py --config config/triggers.yaml
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from statistics import quantiles
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
CFG_PATH = ROOT / "config" / "triggers.yaml"
LOG_DIR = ROOT / "logs"


def _log(logf, payload: dict) -> None:
    logf.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def _db_for(market: str) -> Path:
    if market == "br":
        return DB_BR
    if market == "us":
        return DB_US
    raise ValueError(f"market inválido: {market!r}")


def _latest_price(conn: sqlite3.Connection, ticker: str) -> tuple[str, float] | None:
    row = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return (row[0], row[1]) if row else None


def _max_price_since(conn: sqlite3.Connection, ticker: str, since: str) -> float | None:
    row = conn.execute(
        "SELECT MAX(close) FROM prices WHERE ticker=? AND date>=?",
        (ticker, since),
    ).fetchone()
    return row[0] if row and row[0] is not None else None


def _trailing_div_sum(conn: sqlite3.Connection, ticker: str, anchor: str, months: int = 12) -> float:
    """Soma de dividendos (inclui JCP/rendimento) nos últimos `months` meses até anchor."""
    anchor_dt = datetime.fromisoformat(anchor).date()
    since = (anchor_dt - timedelta(days=int(months * 30.5))).isoformat()
    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM dividends WHERE ticker=? AND ex_date<=? AND ex_date>?",
        (ticker, anchor, since),
    ).fetchone()
    return float(row[0]) if row else 0.0


def _dy_history_series(
    conn: sqlite3.Connection, ticker: str, lookback_years: int
) -> list[float]:
    """Série mensal de DY trailing-12m para os últimos `lookback_years` anos.

    Para cada mês-fim, calcula sum(divs últimos 12m)/preço-fim. Usado para
    percentile histórico. Retorna lista de DYs em % (ex: [3.1, 3.2, ...]).
    """
    end_row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker=?", (ticker,)
    ).fetchone()
    if not end_row or not end_row[0]:
        return []
    end_dt = datetime.fromisoformat(end_row[0]).date()
    start_dt = date(end_dt.year - lookback_years, end_dt.month, 1)

    cur = start_dt
    out: list[float] = []
    while cur <= end_dt:
        next_month = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)
        month_end = (next_month - timedelta(days=1)).isoformat()
        pr = conn.execute(
            "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
            (ticker, month_end),
        ).fetchone()
        if pr and pr[0] and pr[0] > 0:
            divs = _trailing_div_sum(conn, ticker, month_end, months=12)
            if divs > 0:
                out.append(100.0 * divs / pr[0])
        cur = next_month
    return out


def _percentile(values: list[float], pct: float) -> float | None:
    """Percentile simples por interpolação linear. pct ∈ [0,100]."""
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    k = (len(xs) - 1) * (pct / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    frac = k - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


# --- Evaluators: cada kind recebe (conn, trigger_cfg) e devolve dict com
#     {fired: bool, snapshot: dict} -----------------------------------------

def _eval_price_drop_from_high(conn: sqlite3.Connection, t: dict) -> dict:
    ticker = t["ticker"]
    lookback = int(t.get("lookback_days", 90))
    threshold = float(t["threshold_pct"])  # espera-se negativo (ex: -10)
    latest = _latest_price(conn, ticker)
    if not latest:
        return {"fired": False, "snapshot": {"reason": "no_price"}}
    d_latest, p_latest = latest
    since = (datetime.fromisoformat(d_latest).date() - timedelta(days=lookback)).isoformat()
    high = _max_price_since(conn, ticker, since)
    if high is None or high <= 0:
        return {"fired": False, "snapshot": {"reason": "no_high"}}
    drop_pct = (p_latest - high) / high * 100.0
    fired = drop_pct <= threshold
    return {
        "fired": fired,
        "snapshot": {
            "price": round(p_latest, 4),
            "price_date": d_latest,
            "high_lookback": round(high, 4),
            "lookback_days": lookback,
            "drop_pct": round(drop_pct, 2),
            "threshold_pct": threshold,
        },
    }


def _eval_dy_above_pct(conn: sqlite3.Connection, t: dict) -> dict:
    ticker = t["ticker"]
    threshold = float(t["threshold_pct"])
    latest = _latest_price(conn, ticker)
    if not latest:
        return {"fired": False, "snapshot": {"reason": "no_price"}}
    d_latest, p_latest = latest
    div_t12 = _trailing_div_sum(conn, ticker, d_latest, months=12)
    if p_latest <= 0:
        return {"fired": False, "snapshot": {"reason": "zero_price"}}
    dy_pct = 100.0 * div_t12 / p_latest
    fired = dy_pct >= threshold
    return {
        "fired": fired,
        "snapshot": {
            "price": round(p_latest, 4),
            "price_date": d_latest,
            "div_t12": round(div_t12, 4),
            "dy_pct": round(dy_pct, 3),
            "threshold_pct": threshold,
        },
    }


def _eval_dy_percentile(conn: sqlite3.Connection, t: dict) -> dict:
    ticker = t["ticker"]
    pct = float(t.get("percentile", 75))
    lookback = int(t.get("lookback_years", 10))
    min_years = int(t.get("min_years", 5))
    hist = _dy_history_series(conn, ticker, lookback)
    # exige dados mensais suficientes (≈12 obs/ano)
    if len(hist) < min_years * 12:
        return {"fired": False, "snapshot": {"reason": "insufficient_history", "obs": len(hist)}}
    threshold_dy = _percentile(hist, pct)
    latest = _latest_price(conn, ticker)
    if not latest or threshold_dy is None:
        return {"fired": False, "snapshot": {"reason": "no_price"}}
    d_latest, p_latest = latest
    div_t12 = _trailing_div_sum(conn, ticker, d_latest, months=12)
    if p_latest <= 0:
        return {"fired": False, "snapshot": {"reason": "zero_price"}}
    dy_now = 100.0 * div_t12 / p_latest
    fired = dy_now >= threshold_dy
    return {
        "fired": fired,
        "snapshot": {
            "price": round(p_latest, 4),
            "price_date": d_latest,
            "dy_now_pct": round(dy_now, 3),
            "dy_threshold_pct": round(threshold_dy, 3),
            "percentile": pct,
            "lookback_years": lookback,
            "obs": len(hist),
        },
    }


def _eval_altman_distress(conn: sqlite3.Connection, t: dict) -> dict:
    """Dispara quando Altman Z-Score cai abaixo de 1.81 (distress zone).

    Usa scoring.altman.compute (lê deep_fundamentals). Skips tickers em
    sectores excluídos (Banks, REITs, FIIs) — retorna fired=False com reason.
    """
    from scoring.altman import compute as altman_compute

    ticker = t["ticker"]
    market = t["market"]
    threshold = float(t.get("threshold_z", 1.81))
    score = altman_compute(ticker, market)
    if not score.applicable:
        return {"fired": False, "snapshot": {
            "reason": "not_applicable",
            "detail": score.reason_if_not_applicable,
        }}
    if score.z is None:
        return {"fired": False, "snapshot": {"reason": "no_z_score"}}
    fired = score.z < threshold
    return {
        "fired": fired,
        "snapshot": {
            "z_score": round(score.z, 3),
            "zone": score.zone,
            "threshold_z": threshold,
            "period_end": score.period_end,
            "confidence": score.confidence,
        },
    }


def _eval_piotroski_weak(conn: sqlite3.Connection, t: dict) -> dict:
    """Dispara quando Piotroski F-Score ≤ 3 (quality red flag)."""
    from scoring.piotroski import compute as piotroski_compute

    ticker = t["ticker"]
    market = t["market"]
    threshold = int(t.get("threshold_f", 3))
    score = piotroski_compute(ticker, market)
    if not score.applicable:
        return {"fired": False, "snapshot": {
            "reason": "not_applicable",
            "detail": score.reason_if_not_applicable,
        }}
    if score.f_score is None:
        return {"fired": False, "snapshot": {"reason": "no_f_score"}}
    fired = score.f_score <= threshold
    return {
        "fired": fired,
        "snapshot": {
            "f_score": score.f_score,
            "label": score.label,
            "threshold_f": threshold,
            "period_t": score.period_t,
            "period_t_minus_1": score.period_t_minus_1,
        },
    }


EVALUATORS = {
    "price_drop_from_high": _eval_price_drop_from_high,
    "dy_above_pct": _eval_dy_above_pct,
    "dy_percentile_vs_own_history": _eval_dy_percentile,
    "altman_distress": _eval_altman_distress,
    "piotroski_weak": _eval_piotroski_weak,
}


def _expand_scoped_triggers(triggers: list[dict]) -> list[dict]:
    """Expande triggers com `scope: all_holdings` para 1 trigger por holding activa.

    Scope resolve-se consultando portfolio_positions em cada DB. Permite
    declarar um veto global (ex: `altman_distress` em todas as holdings)
    sem replicar a entry por ticker.

    O trigger_id original fica inalterado mas a expansão adiciona sufixo
    `/<ticker>` para garantir dedupe único por ticker no dia.
    """
    expanded: list[dict] = []
    for t in triggers:
        scope = t.get("scope")
        if not scope:
            expanded.append(t)
            continue
        if scope != "all_holdings":
            # scope desconhecido — deixa passar para o loop apanhar como erro
            expanded.append(t)
            continue
        markets = [t["market"]] if t.get("market") in ("br", "us") else ["br", "us"]
        for mk in markets:
            with sqlite3.connect(_db_for(mk)) as conn:
                tickers = [row[0] for row in conn.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions "
                    "WHERE active=1 ORDER BY ticker"
                )]
            for ticker in tickers:
                child = dict(t)
                child["ticker"] = ticker
                child["market"] = mk
                child.pop("scope", None)
                child["id"] = f"{t['id']}/{ticker}"
                expanded.append(child)
    return expanded


def _insert_action(
    conn: sqlite3.Connection,
    *,
    ticker: str,
    market: str,
    kind: str,
    trigger_id: str | None,
    action_hint: str | None,
    snapshot: dict,
    note: str | None,
    now_iso: str,
) -> bool:
    """Abre uma row open. Retorna True se inseriu, False se já existia (dedupe diário)."""
    try:
        conn.execute(
            """INSERT INTO watchlist_actions
                 (ticker, market, kind, trigger_id, action_hint,
                  trigger_snapshot_json, status, opened_at, notes)
               VALUES (?,?,?,?,?,?, 'open', ?, ?)""",
            (ticker, market, kind, trigger_id, action_hint,
             json.dumps(snapshot, ensure_ascii=False), now_iso, note),
        )
        return True
    except sqlite3.IntegrityError:
        # índice único parcial: já existe open para este (ticker,kind,trigger_id) hoje
        return False


def run(*, cfg_path: Path, market_filter: str | None, dry_run: bool) -> int:
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    triggers = cfg.get("triggers") or []
    triggers = _expand_scoped_triggers(triggers)
    if market_filter:
        triggers = [t for t in triggers if t.get("market") == market_filter]

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"trigger_monitor_{date.today().isoformat()}.log"
    now_iso = datetime.now(UTC).replace(microsecond=0).isoformat()

    # agrupa triggers por market para abrir 1 connection por DB
    by_market: dict[str, list[dict]] = {}
    for t in triggers:
        by_market.setdefault(t["market"], []).append(t)

    fired = 0
    inserted = 0
    skipped = 0
    errors = 0

    with open(log_path, "a", encoding="utf-8") as logf:
        for market, tlist in by_market.items():
            db = _db_for(market)
            with sqlite3.connect(db) as conn:
                for t in tlist:
                    kind = t.get("kind")
                    ticker = t.get("ticker")
                    tid = t.get("id")
                    evaluator = EVALUATORS.get(kind)
                    if evaluator is None:
                        _log(logf, {
                            "ts": now_iso, "level": "error",
                            "trigger_id": tid, "ticker": ticker, "market": market,
                            "kind": kind, "error": "unknown_kind",
                        })
                        errors += 1
                        continue
                    try:
                        result = evaluator(conn, t)
                    except Exception as exc:
                        _log(logf, {
                            "ts": now_iso, "level": "error",
                            "trigger_id": tid, "ticker": ticker, "market": market,
                            "kind": kind, "error": f"{type(exc).__name__}: {exc}",
                        })
                        errors += 1
                        continue

                    snap = result["snapshot"]
                    if not result["fired"]:
                        _log(logf, {
                            "ts": now_iso, "level": "info", "event": "not_fired",
                            "trigger_id": tid, "ticker": ticker, "market": market,
                            "kind": kind, "snapshot": snap,
                        })
                        continue

                    fired += 1
                    if dry_run:
                        _log(logf, {
                            "ts": now_iso, "level": "info", "event": "fired_dry",
                            "trigger_id": tid, "ticker": ticker, "market": market,
                            "kind": kind, "action_hint": t.get("action_hint"),
                            "snapshot": snap, "note": t.get("note"),
                        })
                        continue

                    ok = _insert_action(
                        conn,
                        ticker=ticker, market=market, kind=kind,
                        trigger_id=tid, action_hint=t.get("action_hint"),
                        snapshot=snap, note=t.get("note"), now_iso=now_iso,
                    )
                    if ok:
                        inserted += 1
                        _log(logf, {
                            "ts": now_iso, "level": "info", "event": "action_opened",
                            "trigger_id": tid, "ticker": ticker, "market": market,
                            "kind": kind, "action_hint": t.get("action_hint"),
                            "snapshot": snap, "note": t.get("note"),
                        })
                    else:
                        skipped += 1
                        _log(logf, {
                            "ts": now_iso, "level": "info", "event": "deduped_open_today",
                            "trigger_id": tid, "ticker": ticker, "market": market, "kind": kind,
                        })
                conn.commit()

        _log(logf, {
            "ts": now_iso, "level": "info", "event": "summary",
            "total_triggers": len(triggers), "fired": fired,
            "inserted": inserted, "deduped": skipped, "errors": errors,
            "dry_run": dry_run,
        })

    print(
        f"[trigger_monitor] triggers={len(triggers)} fired={fired} "
        f"inserted={inserted} deduped={skipped} errors={errors} "
        f"{'DRY' if dry_run else ''}".strip()
    )
    print(f"[trigger_monitor] log: {log_path}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=CFG_PATH)
    ap.add_argument("--market", choices=["br", "us"], default=None,
                    help="Filtra triggers por mercado (default: todos)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Avalia e loga mas NÃO grava em watchlist_actions")
    args = ap.parse_args()
    run(cfg_path=args.config, market_filter=args.market, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
