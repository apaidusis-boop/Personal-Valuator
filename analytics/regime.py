"""Classificador de regime macro — rule-based, zero aprendizado.

Responde: "em que fase do ciclo macro estamos?". Output: expansion | late_cycle
| recession | recovery. Os screens ganham contexto — p.ex. em late_cycle
devemos ser mais cautelosos com alavancagem; em recovery, estar longo.

Fontes: tabela `series` (BCB + FRED).

Sinais usados (e os thresholds são pragmáticos, não optimizados):
  BR:
    - Selic meta (nível + direcção últimos 6m)
    - IPCA YoY (níveis recentes vs meta 3%)
    - IBOV price trend 6m

  US:
    - FRED_T10Y2Y (curva invertida = recession risk)
    - FRED_FEDFUNDS (nível + direcção 12m — fed cutting/hiking)
    - FRED_UNRATE (tendência 6m — empilha labor market)
    - FRED_VIX (stress gauge)

Heurística agregada (inspired Ray Dalio's big cycle):
  expansion   : gov cortou juros recentemente, unemployment baixo, curva positiva
  late_cycle  : gov a subir juros há 12m+, curva plana/invertendo, VIX elevado
  recession   : curva invertida há 3m+, unemployment a subir, VIX spike
  recovery    : vindo de recession, fed a cortar, unemployment a cair

CLI:
    python -m analytics.regime                 # BR + US
    python -m analytics.regime --market us
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


@dataclass
class Regime:
    market: str
    regime: str                       # expansion | late_cycle | recession | recovery | unknown
    confidence: str                   # high | medium | low
    signals: dict[str, str | float] = field(default_factory=dict)   # raw readings
    notes: list[str] = field(default_factory=list)


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _series_value_at(conn: sqlite3.Connection, series_id: str,
                     at_iso: str | None = None) -> float | None:
    at_iso = at_iso or date.today().isoformat()
    r = conn.execute(
        "SELECT value FROM series WHERE series_id=? AND date<=? ORDER BY date DESC LIMIT 1",
        (series_id, at_iso),
    ).fetchone()
    return r[0] if r else None


def _series_trend(conn: sqlite3.Connection, series_id: str, months: int) -> float | None:
    """Diferença (valor_hoje - valor_há_N_meses). Em unidades da série."""
    today = date.today()
    target = (today - timedelta(days=months * 30)).isoformat()
    now_v = _series_value_at(conn, series_id)
    past_v = _series_value_at(conn, series_id, target)
    if now_v is None or past_v is None:
        return None
    return now_v - past_v


def _price_trend(conn: sqlite3.Connection, ticker: str, months: int) -> float | None:
    """Retorno % do ticker nos últimos N meses. Usa prices table."""
    today = date.today().isoformat()
    target = (date.today() - timedelta(days=months * 30)).isoformat()
    p_now = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, today),
    ).fetchone()
    p_past = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date<=? ORDER BY date DESC LIMIT 1",
        (ticker, target),
    ).fetchone()
    if not p_now or not p_past or not p_past[0]:
        return None
    return (p_now[0] / p_past[0] - 1) * 100


# --- classifiers ------------------------------------------------------------

def classify_br() -> Regime:
    r = Regime(market="br", regime="unknown", confidence="low")
    with sqlite3.connect(DB_BR) as conn:
        selic_now = _series_value_at(conn, "SELIC_META")
        selic_trend_6m = _series_trend(conn, "SELIC_META", 6)
        ipca_last = _series_value_at(conn, "IPCA_MONTHLY")
        ibov_trend_6m = _price_trend(conn, "^BVSP", 6)

    r.signals = {
        "selic_meta": round(selic_now, 2) if selic_now is not None else None,
        "selic_trend_6m": round(selic_trend_6m, 2) if selic_trend_6m is not None else None,
        "ipca_last_month": round(ipca_last * 100, 2) if ipca_last is not None else None,
        "ibov_6m_pct": round(ibov_trend_6m, 2) if ibov_trend_6m is not None else None,
    }

    # Regras heurísticas para BR
    if selic_now is None:
        r.notes.append("sem dados Selic")
        return r

    selic_high = selic_now >= 12.0                 # Selic alta: restritivo
    selic_cutting = (selic_trend_6m or 0) < -0.5   # a cortar nos últimos 6m
    selic_hiking = (selic_trend_6m or 0) > 0.5     # a subir
    ibov_weak = (ibov_trend_6m or 0) < -5
    ibov_strong = (ibov_trend_6m or 0) > 10

    if selic_high and selic_hiking and ibov_weak:
        r.regime, r.confidence = "late_cycle", "medium"
        r.notes.append("Selic alta + a subir + IBOV fraco = ambiente restritivo")
    elif selic_high and selic_cutting and ibov_strong:
        r.regime, r.confidence = "recovery", "medium"
        r.notes.append("Selic ainda alta mas a cortar + IBOV forte = easing cycle")
    elif selic_cutting and (ibov_trend_6m or 0) > 0:
        r.regime, r.confidence = "expansion", "medium"
        r.notes.append("Selic em queda + IBOV positivo = expansão")
    elif selic_hiking:
        r.regime, r.confidence = "late_cycle", "medium"
        r.notes.append("Selic a subir = restrição a caminho")
    else:
        r.regime, r.confidence = "expansion", "low"
        r.notes.append("sinais mistos — default expansion")
    return r


def classify_us() -> Regime:
    r = Regime(market="us", regime="unknown", confidence="low")
    with sqlite3.connect(DB_US) as conn:
        t10y2y = _series_value_at(conn, "FRED_T10Y2Y")
        fedfunds = _series_value_at(conn, "FRED_FEDFUNDS")
        fedfunds_trend_12m = _series_trend(conn, "FRED_FEDFUNDS", 12)
        unrate = _series_value_at(conn, "FRED_UNRATE")
        unrate_trend_6m = _series_trend(conn, "FRED_UNRATE", 6)
        vix = _series_value_at(conn, "FRED_VIX")
        cpi_yoy = _series_value_at(conn, "FRED_CPI_YOY")

    r.signals = {
        "t10y2y_spread_pp": round(t10y2y, 2) if t10y2y is not None else None,
        "fed_funds_pct": round(fedfunds, 2) if fedfunds is not None else None,
        "fed_trend_12m_pp": round(fedfunds_trend_12m, 2) if fedfunds_trend_12m is not None else None,
        "unemployment_pct": round(unrate, 2) if unrate is not None else None,
        "unrate_trend_6m_pp": round(unrate_trend_6m, 2) if unrate_trend_6m is not None else None,
        "vix": round(vix, 2) if vix is not None else None,
        "cpi_yoy_pct": round(cpi_yoy, 2) if cpi_yoy is not None else None,
    }

    if t10y2y is None or fedfunds is None:
        r.notes.append("sem dados FRED chave")
        return r

    curve_inverted = t10y2y < 0
    fed_cutting = (fedfunds_trend_12m or 0) < -0.5
    fed_hiking = (fedfunds_trend_12m or 0) > 0.5
    unemployment_rising = (unrate_trend_6m or 0) > 0.3
    unemployment_falling = (unrate_trend_6m or 0) < -0.3
    vix_high = (vix or 0) > 25
    inflation_hot = (cpi_yoy or 0) > 3.5

    # Priority order of rules
    if curve_inverted and unemployment_rising and vix_high:
        r.regime, r.confidence = "recession", "high"
        r.notes.append("curva invertida + unemployment a subir + VIX elevado")
    elif curve_inverted and fed_hiking:
        r.regime, r.confidence = "late_cycle", "high"
        r.notes.append("curva invertida + Fed a apertar = late cycle clássico")
    elif fed_cutting and unemployment_falling:
        r.regime, r.confidence = "expansion", "high"
        r.notes.append("Fed a cortar + labor forte = expansion")
    elif fed_cutting and unemployment_rising:
        r.regime, r.confidence = "recovery", "medium"
        r.notes.append("Fed a cortar + unemployment ainda a subir = early recovery")
    elif fed_hiking and inflation_hot:
        r.regime, r.confidence = "late_cycle", "medium"
        r.notes.append("Fed hiking + inflação alta = restrição")
    elif not curve_inverted and not unemployment_rising:
        r.regime, r.confidence = "expansion", "medium"
        r.notes.append("curva normal + labor estável = expansion")
    else:
        r.regime, r.confidence = "late_cycle", "low"
        r.notes.append("sinais mistos — default cauteloso")
    return r


def classify(market: str) -> Regime:
    if market == "br":
        return classify_br()
    return classify_us()


# --- CLI --------------------------------------------------------------------

def _print(r: Regime) -> None:
    emoji = {"expansion": "📈", "late_cycle": "⚠", "recession": "📉",
             "recovery": "🌱", "unknown": "?"}.get(r.regime, "?")
    conf_bars = {"high": "▓▓▓", "medium": "▓▓░", "low": "▓░░"}[r.confidence]
    print(f"\n{emoji} REGIME {r.market.upper()}: {r.regime.upper()}  "
          f"[confidence {r.confidence} {conf_bars}]")
    print("  signals:")
    for k, v in r.signals.items():
        v_disp = "—" if v is None else str(v)
        print(f"    {k:<25} {v_disp}")
    if r.notes:
        print("  notes:")
        for n in r.notes:
            print(f"    • {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", choices=["br", "us"], help="Só um mercado")
    args = ap.parse_args()
    markets = [args.market] if args.market else ["br", "us"]
    for m in markets:
        _print(classify(m))


if __name__ == "__main__":
    main()
