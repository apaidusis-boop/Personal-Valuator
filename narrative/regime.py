"""Classificação do regime macro (4 dimensões independentes).

Consome `series` já populada por fetchers/bcb_fetcher.py (BR) e equivalente US
(FRED, a implementar). NÃO chama rede. Escreve em `macro_regime`.

Dimensões (cada uma é uma função pura de séries numéricas):

    rate_regime    : 'tightening' | 'easing' | 'hold'
    growth_regime  : 'expansion' | 'slowdown' | 'recession' | 'recovery'
    fx_regime      : 'strong_local' | 'weak_local' | 'neutral'
    risk_regime    : 'risk_on' | 'risk_off' | 'neutral'

Regras são heurísticas conservadoras — preferir 'hold'/'neutral' quando sinal
ambíguo. Toda a sensibilidade está em `BR_CONFIG` (magic numbers ficam em
config, não em lógica).

BR: lookback limitado a 2010-01-01 para evitar quebras estruturais (era
Selic 14%→2%→13% em 5 anos distorce qualquer análise longa).
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"

BR_LOOKBACK_START = "2010-01-01"

RateRegime = Literal["tightening", "easing", "hold"]
GrowthRegime = Literal["expansion", "slowdown", "recession", "recovery"]
FxRegime = Literal["strong_local", "weak_local", "neutral"]
RiskRegime = Literal["risk_on", "risk_off", "neutral"]


@dataclass(frozen=True)
class MacroRegime:
    date: str
    market: str
    rate: RateRegime
    growth: GrowthRegime
    fx: FxRegime
    risk: RiskRegime
    details: dict


# ---------------------------------------------------------------------------
# Configuração BR — magic numbers todos aqui para ser fácil calibrar.
# ---------------------------------------------------------------------------
BR_CONFIG = {
    # rate_regime: delta da meta Selic em 90 dias corridos
    "rate": {
        "series": "SELIC_META",        # % a.a.
        "lookback_days": 90,
        "tightening_threshold_pp": 0.5,    # +0.5pp em 90d → tightening
        "easing_threshold_pp": -0.5,
    },
    # growth_regime: IPCA YoY como proxy inverso (alta inflação ≈ slowdown
    # via aperto monetário). Proxy pobre mas único sem IBC-Br implementado.
    # TODO: substituir por IBC-Br + desemprego quando IBGE fetcher existir.
    "growth": {
        "series": "IPCA_MONTHLY",      # % a.m.
        "yoy_high_pct": 6.0,           # IPCA YoY > 6% → slowdown (aperto)
        "yoy_low_pct":  3.0,           # IPCA YoY < 3% → recovery/expansion
    },
    # fx_regime: USDBRL vs média móvel 200 dias
    "fx": {
        "series": "USDBRL_PTAX",
        "ma_window": 200,
        "weak_local_threshold": 0.05,   # preço > MA*(1+0.05) → BRL fraco
        "strong_local_threshold": -0.05,
    },
    # risk_regime: ainda sem VIX na DB BR → neutral por defeito.
    # TODO: adicionar ^VIX via yfinance_fetcher quando viável.
    "risk": {
        "default": "neutral",
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_series(conn: sqlite3.Connection, series_id: str, since: str) -> list[tuple[str, float]]:
    rows = conn.execute(
        "SELECT date, value FROM series WHERE series_id=? AND date >= ? ORDER BY date",
        (series_id, since),
    ).fetchall()
    return [(r[0], r[1]) for r in rows]


def _pct_change_pp(latest: float, earlier: float) -> float:
    """Ambos em % a.a. — devolve delta em pontos percentuais."""
    return latest - earlier


def _classify_rate_br(series: list[tuple[str, float]], date: str) -> tuple[RateRegime, dict]:
    cfg = BR_CONFIG["rate"]
    cutoff_date = (datetime.fromisoformat(date) - timedelta(days=cfg["lookback_days"])).date().isoformat()
    window = [(d, v) for d, v in series if d <= date]
    if len(window) < 2:
        return "hold", {"reason": "insufficient_data"}
    latest = window[-1]
    earlier = next((p for p in reversed(window) if p[0] <= cutoff_date), window[0])
    delta = _pct_change_pp(latest[1], earlier[1])
    details = {"latest_value": latest[1], "earlier_value": earlier[1], "delta_pp": round(delta, 3)}
    if delta >= cfg["tightening_threshold_pp"]:
        return "tightening", details
    if delta <= cfg["easing_threshold_pp"]:
        return "easing", details
    return "hold", details


def _ipca_yoy(series: list[tuple[str, float]], date: str) -> float | None:
    """Composto dos 12 meses anteriores a `date` (IPCA vem em % a.m.)."""
    recent = [(d, v) for d, v in series if d <= date][-12:]
    if len(recent) < 12:
        return None
    compound = 1.0
    for _, v in recent:
        compound *= 1.0 + v / 100.0
    return (compound - 1.0) * 100.0


def _classify_growth_br(series: list[tuple[str, float]], date: str) -> tuple[GrowthRegime, dict]:
    cfg = BR_CONFIG["growth"]
    yoy = _ipca_yoy(series, date)
    if yoy is None:
        return "expansion", {"reason": "insufficient_data", "assumption": "default_expansion"}
    details = {"ipca_yoy_pct": round(yoy, 2)}
    if yoy > cfg["yoy_high_pct"]:
        return "slowdown", details
    if yoy < cfg["yoy_low_pct"]:
        return "expansion", details
    return "expansion", details  # banda intermédia = expansion por conservadorismo


def _classify_fx_br(series: list[tuple[str, float]], date: str) -> tuple[FxRegime, dict]:
    cfg = BR_CONFIG["fx"]
    window = [(d, v) for d, v in series if d <= date]
    if len(window) < cfg["ma_window"]:
        return "neutral", {"reason": "insufficient_data"}
    tail = window[-cfg["ma_window"]:]
    ma = sum(v for _, v in tail) / cfg["ma_window"]
    latest = window[-1][1]
    deviation = (latest - ma) / ma
    details = {"usdbrl": round(latest, 4), "ma200": round(ma, 4), "deviation": round(deviation, 4)}
    if deviation > cfg["weak_local_threshold"]:
        return "weak_local", details
    if deviation < cfg["strong_local_threshold"]:
        return "strong_local", details
    return "neutral", details


def _classify_risk_br(date: str) -> tuple[RiskRegime, dict]:
    # Placeholder — sem VIX na DB BR ainda.
    return BR_CONFIG["risk"]["default"], {"reason": "vix_not_available"}


def classify_br(db_path: Path = DB_BR, since: str | None = None) -> int:
    """Recomputa `macro_regime` para market='br' desde `since` (default:
    BR_LOOKBACK_START). Idempotente — UPSERT por (date, market).

    Devolve nº de linhas escritas/actualizadas.
    """
    since_date = since or BR_LOOKBACK_START
    with sqlite3.connect(db_path) as conn:
        selic = _load_series(conn, BR_CONFIG["rate"]["series"], since_date)
        ipca = _load_series(conn, BR_CONFIG["growth"]["series"], since_date)
        usdbrl = _load_series(conn, BR_CONFIG["fx"]["series"], since_date)

        # Usamos o eixo temporal do USDBRL (daily, mais completo) como grelha.
        dates = sorted({d for d, _ in usdbrl if d >= since_date})

        rows = []
        for date in dates:
            rate, rate_d = _classify_rate_br(selic, date)
            growth, growth_d = _classify_growth_br(ipca, date)
            fx, fx_d = _classify_fx_br(usdbrl, date)
            risk, risk_d = _classify_risk_br(date)
            details = {"rate": rate_d, "growth": growth_d, "fx": fx_d, "risk": risk_d}
            rows.append((date, "br", rate, growth, fx, risk, json.dumps(details, ensure_ascii=False)))

        conn.executemany(
            """INSERT INTO macro_regime
                 (date, market, rate_regime, growth_regime, fx_regime, risk_regime, details_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(date, market) DO UPDATE SET
                 rate_regime=excluded.rate_regime,
                 growth_regime=excluded.growth_regime,
                 fx_regime=excluded.fx_regime,
                 risk_regime=excluded.risk_regime,
                 details_json=excluded.details_json""",
            rows,
        )
        conn.commit()
    return len(rows)


def classify_us(db_path: Path, since: str | None = None) -> int:
    """TODO: requer FRED fetcher (FEDFUNDS, CPI, DXY, VIX)."""
    raise NotImplementedError("US regime requer FRED series ainda não populadas")


def current(db_path: Path, market: str) -> MacroRegime | None:
    """Devolve o regime mais recente para o mercado indicado."""
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """SELECT date, market, rate_regime, growth_regime, fx_regime,
                      risk_regime, details_json
                 FROM macro_regime WHERE market=? ORDER BY date DESC LIMIT 1""",
            (market,),
        ).fetchone()
    if not row:
        return None
    return MacroRegime(
        date=row[0], market=row[1], rate=row[2], growth=row[3],
        fx=row[4], risk=row[5], details=json.loads(row[6] or "{}"),
    )


if __name__ == "__main__":
    n = classify_br()
    print(f"[regime] classified {n} days for BR")
    cur = current(DB_BR, "br")
    if cur:
        print(f"[regime] latest {cur.date}: rate={cur.rate} growth={cur.growth} fx={cur.fx} risk={cur.risk}")
