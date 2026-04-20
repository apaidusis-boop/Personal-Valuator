"""Altman Z-Score — predictor de distress financeiro.

Fórmula clássica (Altman 1968, empresas industriais cotadas):

    Z = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5

  X1 = Working Capital / Total Assets       (liquidez)
  X2 = Retained Earnings / Total Assets     (lucros acumulados ao longo do tempo)
  X3 = EBIT / Total Assets                  (rentabilidade operacional)
  X4 = Market Cap / Total Liabilities       (margem de segurança de equity)
  X5 = Revenue / Total Assets               (eficiência de activos)

Interpretação:
  Z > 2.99   → safe zone
  1.81 ≤ Z ≤ 2.99  → grey zone (monitor)
  Z < 1.81   → distress zone (veto forte de BUY)

Fontes de dados: tabela deep_fundamentals (fetched via fetchers/yf_deep_fundamentals.py).

Aplicabilidade: não se aplica a bancos (Banks) e FIIs/REITs (rácios têm
significado diferente). Para esses, retorna applicable=False.

CLI:
    python -m scoring.altman JNJ
    python -m scoring.altman ITSA4 --market br
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# Sectores onde Altman clássico NÃO se aplica
EXCLUDED_SECTORS = {"Banks", "Financials", "REIT", "FII", "Shopping", "Logística",
                    "Papel (CRI)", "Híbrido", "Corporativo", "ETF-RF", "ETF-US"}


@dataclass
class AltmanScore:
    ticker: str
    applicable: bool
    reason_if_not_applicable: str | None = None
    z: float | None = None
    zone: str | None = None          # 'safe' | 'grey' | 'distress'
    confidence: str | None = None    # 'high' | 'medium' | 'low'
    x1: float | None = None
    x2: float | None = None
    x3: float | None = None
    x4: float | None = None
    x5: float | None = None
    period_end: str | None = None
    notes: list[str] | None = None

    @property
    def is_distress(self) -> bool:
        return self.applicable and self.z is not None and self.z < 1.81

    @property
    def is_safe(self) -> bool:
        return self.applicable and self.z is not None and self.z > 2.99


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        with sqlite3.connect(_db(mk)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


def compute(ticker: str, market: str | None = None) -> AltmanScore:
    """Calcula Z-Score para um ticker. Auto-detecta mercado se não passado."""
    notes: list[str] = []
    market = market or _detect_market(ticker)
    if market is None:
        return AltmanScore(ticker=ticker, applicable=False,
                           reason_if_not_applicable="ticker não encontrado em nenhuma DB")

    with sqlite3.connect(_db(market)) as conn:
        sec_row = conn.execute(
            "SELECT sector FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        sector = sec_row[0] if sec_row else None
        if sector in EXCLUDED_SECTORS:
            return AltmanScore(
                ticker=ticker, applicable=False,
                reason_if_not_applicable=f"Altman não se aplica a sector '{sector}'",
            )

        # Pega o período anual mais recente COMPLETO (com total_assets não-None)
        row = conn.execute(
            """SELECT period_end, total_assets, working_capital, retained_earnings,
                      ebit, total_revenue, total_liabilities, stockholders_equity,
                      net_income, market_cap_at_fetch
               FROM deep_fundamentals
               WHERE ticker=? AND period_type='annual' AND total_assets IS NOT NULL
               ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
    if not row:
        return AltmanScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable="sem deep_fundamentals — roda fetchers/yf_deep_fundamentals.py",
        )
    (period_end, ta, wc, re_, ebit, rev, tl, eq, ni, mc) = row

    # Required não-nulos
    missing = [name for name, v in {
        "total_assets": ta, "working_capital": wc, "ebit": ebit,
        "total_revenue": rev, "total_liabilities": tl,
    }.items() if v is None]
    if missing:
        return AltmanScore(
            ticker=ticker, applicable=False,
            reason_if_not_applicable=f"campos em falta: {','.join(missing)}",
        )

    confidence = "high"

    # Fallback X2: se retained_earnings missing, usar stockholders_equity como proxy
    # (stockholders_equity inclui RE + paid-in capital → overstates X2, marcar low)
    if re_ is None:
        if eq is not None:
            re_ = eq
            notes.append("X2 usa stockholders_equity (retained_earnings missing) — conservative proxy")
            confidence = "medium"
        else:
            return AltmanScore(
                ticker=ticker, applicable=False,
                reason_if_not_applicable="retained_earnings e stockholders_equity ambos missing",
            )

    # Fallback X4: se market_cap não preenchido nesta row, vai buscar o mais recente da mesma ticker
    if mc is None or mc <= 0:
        with sqlite3.connect(_db(market)) as conn:
            mc_row = conn.execute(
                "SELECT market_cap_at_fetch FROM deep_fundamentals "
                "WHERE ticker=? AND market_cap_at_fetch IS NOT NULL "
                "ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
        if mc_row:
            mc = mc_row[0]
        else:
            return AltmanScore(
                ticker=ticker, applicable=False,
                reason_if_not_applicable="market_cap não disponível em nenhum período",
            )

    x1 = wc / ta
    x2 = re_ / ta
    x3 = ebit / ta
    x4 = mc / tl if tl > 0 else 0
    x5 = rev / ta

    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5

    if z > 2.99:
        zone = "safe"
    elif z >= 1.81:
        zone = "grey"
    else:
        zone = "distress"

    return AltmanScore(
        ticker=ticker, applicable=True,
        z=z, zone=zone, confidence=confidence,
        x1=x1, x2=x2, x3=x3, x4=x4, x5=x5,
        period_end=period_end, notes=notes,
    )


def _print(score: AltmanScore) -> None:
    print(f"\nAltman Z-Score — {score.ticker}")
    print("=" * 60)
    if not score.applicable:
        print(f"  NÃO APLICÁVEL: {score.reason_if_not_applicable}")
        return
    print(f"  Período: {score.period_end}   Confiança: {score.confidence}")
    print(f"  Z = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5")
    print(f"      X1 (WC/TA)   = {score.x1:+.4f}")
    print(f"      X2 (RE/TA)   = {score.x2:+.4f}")
    print(f"      X3 (EBIT/TA) = {score.x3:+.4f}")
    print(f"      X4 (MC/TL)   = {score.x4:+.4f}")
    print(f"      X5 (Rev/TA)  = {score.x5:+.4f}")
    zone_tag = {"safe": "✓ SAFE", "grey": "◦ GREY", "distress": "✗ DISTRESS"}[score.zone]
    print(f"  Z = {score.z:+.3f}  →  {zone_tag}")
    if score.is_distress:
        print(f"  ⚠ Z < 1.81 → veto forte sobre BUY (ver scoring/engine.py rule R5)")
    if score.notes:
        for n in score.notes:
            print(f"  note: {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    args = ap.parse_args()
    score = compute(args.ticker.upper(), args.market)
    _print(score)


if __name__ == "__main__":
    main()
