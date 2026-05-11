"""Detecta degradação / melhoria do screen score ao longo do tempo.

Complementa os triggers (que vigiam preço/yield). Enquanto os triggers dizem
"o momento é bom para entrar", este módulo responde "a qualidade continua lá?".

Usa apenas a tabela `scores` que tem (ticker, run_date, score, passes_screen).
Funciona graceful com história curta — em runs iniciais não marca alerts,
mas à medida que o histórico cresce passa a detectar padrões.

Sinais emitidos:
  - transition_fail   : passes_screen foi 1→0 na run mais recente (alerta de tese)
  - transition_pass   : passes_screen foi 0→1 (promote candidate)
  - score_degrading   : score caiu >= 0.20 vs mediana das 5 runs anteriores
  - score_improving   : score subiu >= 0.20 vs mediana
  - stable            : sem mudança significativa

CLI:
    python -m analytics.screen_trend                 # varre BR + US
    python -m analytics.screen_trend --market br
    python -m analytics.screen_trend --ticker JNJ
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

DEGRADATION_DELTA = 0.20     # score drop vs baseline para flag
BASELINE_WINDOW = 5          # nº de runs anteriores usadas como baseline


@dataclass
class TrendSignal:
    ticker: str
    market: str
    signal: str                    # transition_fail | transition_pass | score_degrading | ...
    latest_run: str
    latest_score: float
    latest_passes: bool
    baseline_score: float | None   # mediana das runs anteriores (None se história insuficiente)
    prev_passes: bool | None
    history_len: int               # quantas runs há para este ticker
    is_holding: bool


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _fetch_history(conn: sqlite3.Connection, ticker: str) -> list[tuple[str, float, int]]:
    """Devolve (run_date, score, passes_screen) mais recente primeiro."""
    return conn.execute(
        "SELECT run_date, score, passes_screen FROM scores "
        "WHERE ticker=? ORDER BY run_date DESC",
        (ticker,),
    ).fetchall()


def _classify(history: list[tuple[str, float, int]]) -> tuple[str, float | None, bool | None]:
    """Retorna (signal, baseline_score, prev_passes)."""
    if not history:
        return ("no_data", None, None)
    latest_date, latest_score, latest_passes = history[0]
    # baseline: mediana das `BASELINE_WINDOW` runs anteriores (índices 1..N)
    baseline_slice = history[1:1 + BASELINE_WINDOW]
    if not baseline_slice:
        return ("first_run", None, None)

    baseline_score = median(s for _, s, _ in baseline_slice)
    prev_passes = bool(baseline_slice[0][2])

    if bool(latest_passes) != prev_passes:
        return ("transition_fail" if not latest_passes else "transition_pass",
                baseline_score, prev_passes)
    delta = latest_score - baseline_score
    if delta <= -DEGRADATION_DELTA:
        return ("score_degrading", baseline_score, prev_passes)
    if delta >= DEGRADATION_DELTA:
        return ("score_improving", baseline_score, prev_passes)
    return ("stable", baseline_score, prev_passes)


def scan(market: str, *, ticker_filter: str | None = None) -> list[TrendSignal]:
    out: list[TrendSignal] = []
    with sqlite3.connect(_db(market)) as conn:
        q = "SELECT ticker, is_holding FROM companies"
        params: tuple = ()
        if ticker_filter:
            q += " WHERE ticker=?"
            params = (ticker_filter.upper(),)
        for ticker, is_holding in conn.execute(q, params).fetchall():
            hist = _fetch_history(conn, ticker)
            if not hist:
                continue
            sig, baseline, prev_p = _classify(hist)
            out.append(TrendSignal(
                ticker=ticker, market=market,
                signal=sig, latest_run=hist[0][0],
                latest_score=float(hist[0][1]),
                latest_passes=bool(hist[0][2]),
                baseline_score=baseline,
                prev_passes=prev_p,
                history_len=len(hist),
                is_holding=bool(is_holding),
            ))
    return out


def notable(signals: list[TrendSignal]) -> list[TrendSignal]:
    """Subset que merece atenção: transições + degradação em holdings."""
    priority = {"transition_fail": 0, "transition_pass": 1,
                "score_degrading": 2, "score_improving": 3}
    return sorted(
        [s for s in signals if s.signal in priority],
        key=lambda s: (priority[s.signal], not s.is_holding, s.ticker),
    )


def _print(signals: list[TrendSignal]) -> None:
    if not signals:
        print("[nenhum sinal — todos stable ou história insuficiente]")
        return
    print(f"\n{'MKT':<3} {'TICKER':<7} {'SIGNAL':<18} {'SCORE':>6} "
          f"{'BASELINE':>9} {'PASS':>5} {'RUNS':>5} {'HOLD':>5}")
    print("-" * 72)
    for s in signals:
        base = f"{s.baseline_score:.2f}" if s.baseline_score is not None else "  —"
        prev = "—" if s.prev_passes is None else ("Y" if s.prev_passes else "N")
        pass_disp = "Y" if s.latest_passes else "N"
        hold = "Y" if s.is_holding else "-"
        print(f"{s.market:<3} {s.ticker:<7} {s.signal:<18} "
              f"{s.latest_score:>6.2f} {base:>9} "
              f"{prev}→{pass_disp:<3} {s.history_len:>5} {hold:>5}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], help="Filtra por mercado")
    ap.add_argument("--ticker", help="Só este ticker")
    ap.add_argument("--all", action="store_true",
                    help="Mostra também stable/first_run/no_data")
    args = ap.parse_args()

    markets = [args.market] if args.market else ["br", "us"]
    all_signals: list[TrendSignal] = []
    for mkt in markets:
        all_signals.extend(scan(mkt, ticker_filter=args.ticker))

    if args.all:
        _print(sorted(all_signals, key=lambda s: (s.market, s.ticker)))
    else:
        _print(notable(all_signals))


if __name__ == "__main__":
    main()
