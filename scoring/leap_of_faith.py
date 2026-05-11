"""Leap of Faith Engine — vitality-aware screen override.

Filosofia (user, 2026-05-09): a régua quantitativa pode barrar uma empresa
Premium por uma margem pequena (P/E 13 vs ≤12, DY 1.95% vs ≥2.5%). Para casos
em que a vitalidade da empresa nos próximos 20-30 anos é OVERWHELMING, faz
sentido permitir entrada com uma "leap of faith" — sempre documentada, com
observações explícitas, e revalidada periodicamente.

Este módulo NÃO faz override automático. Emite uma classificação estruturada:

  status                 quando
  ─────                  ──────
  PASS                   screen passou (régua OK, sem necessidade de vitality)
  PASS_WITH_VITALITY     screen passou, vitality OVERWHELMING (alta convicção)
  LEAP_OF_FAITH          screen falhou por *near miss* + vitality OVERWHELMING
  REJECTED_NEAR_MISS     screen falhou near miss mas vitality não suporta
  REJECTED_FAR_MISS      screen falhou e multiplos longe da régua (não é near miss)
  N/A                    sem dados suficientes para avaliar

"Near miss" = todos os critérios falhados estão dentro de 1.30x da régua
(ou 1/1.30x para critérios "higher is better"). Calibra o que conta como
"um pouco acima". Se uma régua é falhada por mais de 30%, é far miss e não
qualifica para vitality override — concordância com a intuição de "multiplos
bons mas régua um pouco acima".

Persistência: tabela leap_of_faith_log em data/<mkt>_investments.db.
Cada run grava um snapshot: status, screen_score, vitality, near_miss_max,
failed_rules, observations.

Uso:
    python -m scoring.leap_of_faith JPM
    python -m scoring.leap_of_faith JPM --persist
    python -m scoring.leap_of_faith --holdings  # roda em todos holdings
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scoring import engine as scoring_engine
from scoring import vitality as vitality_mod

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

DEFAULT_NEAR_MISS_THRESHOLD = 1.30  # 30% slack for "um pouco acima da régua"
NEAR_MISS_THRESHOLD = DEFAULT_NEAR_MISS_THRESHOLD

# Rules that are structurally distorted for some company types (e.g., P/B for
# brand-heavy companies like KO/JNJ where most value is intangible). When
# detected, they're flagged as "structural" and excluded from near-miss math.
INTANGIBLE_HEAVY_PB_EXEMPT = True  # opt-in, can disable with --strict-pb
INTANGIBLE_THRESHOLD = 0.10        # 10% of total assets being intangible/goodwill

SCHEMA = """
CREATE TABLE IF NOT EXISTS leap_of_faith_log (
    ticker            TEXT NOT NULL,
    market            TEXT NOT NULL,
    run_date          TEXT NOT NULL,
    status            TEXT NOT NULL,
    screen_score      REAL,
    screen_passes     INTEGER,
    failed_rules_json TEXT,
    near_miss         INTEGER,
    near_miss_max     REAL,
    vitality_overall  INTEGER,
    vitality_label    TEXT,
    vitality_json     TEXT,
    observations      TEXT,
    PRIMARY KEY (ticker, run_date)
);
"""


@dataclass
class LeapOfFaithVerdict:
    ticker: str
    market: str
    status: str = "N/A"
    screen_score: float | None = None
    screen_passes: bool = False
    failed_rules: list[dict] = field(default_factory=list)
    near_miss: bool = False
    near_miss_max: float | None = None
    vitality_overall: int | None = None
    vitality_label: str = "N/A"
    vitality_components: dict = field(default_factory=dict)
    observations: list[str] = field(default_factory=list)
    intangible_pct: float | None = None

    def headline(self) -> str:
        emoji = {
            "PASS": "✅",
            "PASS_WITH_VITALITY": "🌟",
            "LEAP_OF_FAITH": "🎯",
            "REJECTED_NEAR_MISS": "🟠",
            "REJECTED_FAR_MISS": "🔴",
            "N/A": "❔",
        }.get(self.status, "·")
        return f"{emoji} {self.status}"


# ─── Near-miss detection ──────────────────────────────────────────────────

# Rules where lower value is better (value/threshold > 1 = fail)
LOWER_IS_BETTER = {
    "graham_number",  # special: value compared with price; passes if price ≤ graham
    "pe", "price_to_book", "price_to_tangible_book",
    "net_debt_ebitda", "p_ffo", "efficiency_ratio",
}
# Rules where higher value is better (value/threshold < 1 = fail)
HIGHER_IS_BETTER = {
    "dividend_yield", "roe", "rotce", "cet1",
    "dividend_streak", "dividend_streak_post_gfc", "interest_coverage",
    "spread_selic_real", "vacancy",  # vacancy: < threshold (lower better) but stored as "verdict"
}


def _miss_ratio(rule_name: str, value, threshold) -> float | None:
    """Compute how far the failed rule is from threshold. >1 = failed by ratio."""
    if value is None or threshold is None or threshold == 0:
        return None
    try:
        v = float(value)
        t = float(threshold)
    except (TypeError, ValueError):
        return None

    # graham_number: passes if price <= graham. value=graham, threshold=price.
    # When fails, price > graham → miss = price/graham. We need to invert.
    if rule_name == "graham_number":
        if v <= 0:
            return None
        return t / v  # price / graham_number; >1 = paying premium over Graham

    if rule_name in LOWER_IS_BETTER:
        return v / t
    if rule_name in HIGHER_IS_BETTER:
        if v <= 0:
            return float("inf")
        return t / v
    # Default: treat as lower-is-better
    return v / t


def _is_structural_failure(rule: str, intangible_pct: float | None) -> bool:
    """Some rules are structurally inappropriate for certain company profiles.
    Returns True if this failure should NOT count toward near-miss math.

    Currently: P/B and P/TBV for brand-heavy companies (intangibles >10% of
    assets). Coca-Cola, J&J, PG, etc. carry brand value off-balance-sheet, so
    P/B is permanently elevated — the rule fails for the wrong reason.
    """
    if not INTANGIBLE_HEAVY_PB_EXEMPT:
        return False
    if intangible_pct is None or intangible_pct <= INTANGIBLE_THRESHOLD:
        return False
    return rule in ("pb", "price_to_book", "price_to_tangible_book")


def _detect_near_miss(details: dict, intangible_pct: float | None = None) -> tuple[bool, float | None, list[dict]]:
    """Returns (near_miss, max_miss_ratio, failed_rules_with_ratio)."""
    failed = []
    max_ratio = None
    for rule, det in details.items():
        if det.get("verdict") != "fail":
            continue
        ratio = _miss_ratio(rule, det.get("value"), det.get("threshold"))
        structural = _is_structural_failure(rule, intangible_pct)
        failed.append({
            "rule": rule,
            "value": det.get("value"),
            "threshold": det.get("threshold"),
            "miss_ratio": round(ratio, 3) if ratio is not None else None,
            "structural": structural,
        })
        # Structural failures don't count toward max miss
        if structural:
            continue
        if ratio is not None and (max_ratio is None or ratio > max_ratio):
            max_ratio = ratio

    non_structural = [f for f in failed if not f["structural"]]
    if not non_structural:
        # Only structural failures remain → screen effectively passes
        return True, max_ratio, failed
    if max_ratio is None:
        return False, None, failed
    return (max_ratio <= NEAR_MISS_THRESHOLD), max_ratio, failed


# ─── Snapshot loading (delegates to engine) ───────────────────────────────

def _run_screen(ticker: str, market: str) -> tuple[dict | None, float, bool, float | None]:
    """Execute the appropriate screen. Returns (details, score, passes, intangible_pct)."""
    db = DB_BR if market == "br" else DB_US
    is_fii = market == "br" and ticker.endswith("11") and not ticker.startswith("^")
    intangible_pct = None
    with sqlite3.connect(db) as conn:
        if is_fii:
            snap = scoring_engine.load_fii_snapshot(conn, ticker)
            if snap is None:
                return None, 0.0, False, None
            selic_real = scoring_engine._selic_real_bcb(conn)
            details = scoring_engine.score_br_fii(snap, selic_real=selic_real)
        else:
            snap = scoring_engine.load_snapshot(conn, ticker)
            if snap is None:
                return None, 0.0, False, None
            if market == "br" and scoring_engine._is_bank(snap):
                details = scoring_engine.score_br_bank(snap)
            elif market == "us" and scoring_engine._is_reit(snap):
                details = scoring_engine.score_us_reit(snap)
            elif market == "us" and scoring_engine._is_us_bank(snap):
                details = scoring_engine.score_us_bank(snap)
            else:
                details = (scoring_engine.score_br if market == "br" else scoring_engine.score_us)(snap)

        # Pull intangible_pct_assets for structural-failure detection
        try:
            row = conn.execute(
                "SELECT intangible_pct_assets FROM fundamentals WHERE ticker=? "
                "ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if row and row[0] is not None:
                intangible_pct = float(row[0])
        except sqlite3.OperationalError:
            pass

        score, passes = scoring_engine.aggregate(details)
    return details, score, passes, intangible_pct


# ─── Verdict orchestrator ─────────────────────────────────────────────────

def evaluate(ticker: str, market: str | None = None) -> LeapOfFaithVerdict:
    market = market or vitality_mod._detect_market(ticker)
    if market is None:
        v = LeapOfFaithVerdict(ticker=ticker, market="?")
        v.observations.append("ticker not found in any DB")
        return v

    verdict = LeapOfFaithVerdict(ticker=ticker, market=market)

    details, score, passes, intangible_pct = _run_screen(ticker, market)
    if details is None:
        verdict.observations.append("screen returned no data (snapshot missing)")
        return verdict

    verdict.screen_score = round(score, 4)
    verdict.screen_passes = passes
    verdict.intangible_pct = intangible_pct
    if intangible_pct is not None:
        verdict.observations.append(
            f"intangibles: {intangible_pct:.1%} of total assets"
            + (" → P/B exempted from near-miss math" if intangible_pct > INTANGIBLE_THRESHOLD else "")
        )

    near, ratio, failed = _detect_near_miss(details, intangible_pct=intangible_pct)
    verdict.failed_rules = failed
    verdict.near_miss = near
    verdict.near_miss_max = round(ratio, 3) if ratio is not None else None

    vit = vitality_mod.compute(ticker, market)
    verdict.vitality_overall = vit.overall
    verdict.vitality_label = vit.label
    verdict.vitality_components = {
        "scale_dominance":     vit.scale_dominance,
        "secular_tailwind":    vit.secular_tailwind,
        "capital_allocation":  vit.capital_allocation,
        "resilience_track":    vit.resilience_track,
        "earnings_durability": vit.earnings_durability,
    }

    # Status decision tree
    if passes and vit.label == "OVERWHELMING":
        verdict.status = "PASS_WITH_VITALITY"
        verdict.observations.append(
            "Screen + vitality alinhados — empresa Premium a preço justo. Alta convicção."
        )
    elif passes:
        verdict.status = "PASS"
        verdict.observations.append("Screen aprovado pelos critérios duros.")
    elif not failed:
        verdict.status = "N/A"
        verdict.observations.append("Screen sem falhas avaliáveis (todas n/a).")
    elif near and vit.label == "OVERWHELMING":
        verdict.status = "LEAP_OF_FAITH"
        rule_summary = ", ".join(
            f"{r['rule']} (miss {r['miss_ratio']}x)"
            for r in failed if r['miss_ratio'] is not None
        )
        verdict.observations.append(
            f"Régua falha por pouco ({rule_summary}); vitalidade {vit.overall}/100 "
            f"({vit.label}) suporta entrada com observação."
        )
        verdict.observations.append(
            "⚠️ LEAP OF FAITH: posição assumida com tese de Premium Company 20-30y. "
            "Revalidar trimestralmente. Sair se vitalidade cair abaixo de STRONG."
        )
    elif near and vit.label in ("STRONG", "NEUTRAL"):
        verdict.status = "REJECTED_NEAR_MISS"
        verdict.observations.append(
            f"Régua falhou por pouco mas vitalidade só {vit.label} ({vit.overall}/100) "
            "— não suporta leap of faith. Esperar entrada na régua."
        )
    elif not near:
        verdict.status = "REJECTED_FAR_MISS"
        miss_str = f"{ratio:.2f}x" if ratio is not None else "n/a"
        vit_str = f"{vit.overall}/100" if vit.overall is not None else "n/a"
        verdict.observations.append(
            f"Régua falhou com folga (max miss {miss_str}). Mesmo com vitalidade "
            f"{vit.label} ({vit_str}), o preço pago seria especulativo."
        )
    else:
        verdict.status = "N/A"
        verdict.observations.append("caso não classificado; revisar lógica.")

    return verdict


# ─── Persistence ──────────────────────────────────────────────────────────

def _ensure_schema(market: str) -> None:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)
        c.commit()


def persist(v: LeapOfFaithVerdict) -> None:
    _ensure_schema(v.market)
    db = DB_BR if v.market == "br" else DB_US
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO leap_of_faith_log
               (ticker, market, run_date, status, screen_score, screen_passes,
                failed_rules_json, near_miss, near_miss_max,
                vitality_overall, vitality_label, vitality_json, observations)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                v.ticker, v.market, date.today().isoformat(), v.status,
                v.screen_score, 1 if v.screen_passes else 0,
                json.dumps(v.failed_rules, ensure_ascii=False),
                1 if v.near_miss else 0,
                v.near_miss_max,
                v.vitality_overall, v.vitality_label,
                json.dumps(v.vitality_components, ensure_ascii=False),
                "\n".join(v.observations),
            ),
        )
        c.commit()


# ─── Plain-language explanations for the risk decision panel ──────────────

def _fmt_pct_premium(rule: str, value, threshold) -> str:
    """How much "above the rule" we'd be paying. Direction depends on rule."""
    try:
        v = float(value); t = float(threshold)
    except (TypeError, ValueError):
        return ""
    if rule == "graham_number" and v > 0:
        return f"prémio de {((t / v) - 1) * 100:.0f}% sobre o preço Graham"
    if rule in LOWER_IS_BETTER and t > 0:
        return f"prémio de {((v / t) - 1) * 100:.0f}% acima do tecto"
    if rule in HIGHER_IS_BETTER and v > 0 and t > 0:
        return f"compressão de {(1 - (v / t)) * 100:.0f}% abaixo do mínimo"
    return ""


def _explain_failure(rule: str, value, threshold, currency: str = "USD",
                     intangible_pct: float | None = None) -> str | None:
    """Plain-language description of what accepting this miss means.
    Returns a one-line string the investor reads before deciding."""
    cur_symbol = "R$" if currency.upper() == "BRL" else "$"
    try:
        v = float(value)
        t = float(threshold)
    except (TypeError, ValueError):
        return None

    rule = rule.lower()
    if rule == "pe":
        return f"P/E (preço/lucro): pagas {cur_symbol}{v:.2f} por cada {cur_symbol}1 de lucro anual (tecto: {cur_symbol}{t:.0f})."
    if rule in ("pb", "price_to_book"):
        base = f"P/B: pagas {v:.2f}× o valor patrimonial por acção (tecto: {t:.1f}×)."
        if intangible_pct is not None and intangible_pct > INTANGIBLE_THRESHOLD:
            base += f" Empresa brand-heavy (intangíveis {intangible_pct:.0%} dos activos) — P/B é estruturalmente alto."
        return base
    if rule == "price_to_tangible_book":
        return f"P/TBV: pagas {v:.2f}× o book tangível (sem goodwill nem intangíveis). Tecto: {t:.1f}×."
    if rule == "dividend_yield":
        return f"DY actual: {v*100:.2f}% ao ano (mínimo: {t*100:.1f}%). Tu recebes menos rendimento de partida."
    if rule == "roe":
        return f"ROE: empresa rende {v*100:.1f}% sobre o capital (mínimo: {t*100:.0f}%). Eficiência operacional abaixo do bar."
    if rule == "rotce":
        return f"ROTCE: empresa rende {v*100:.1f}% sobre capital tangível (mínimo: {t*100:.0f}%). Bar mais exigente que ROE."
    if rule == "net_debt_ebitda":
        return f"Dív. líq/EBITDA: empresa deve {v:.2f}× a sua geração de caixa anual (tecto: {t:.1f}×). Risco de alavancagem."
    if rule in ("dividend_streak", "dividend_streak_post_gfc"):
        return f"Histórico de dividendos: {int(v)} anos consecutivos (mínimo: {int(t)})."
    if rule == "graham_number":
        return f"Graham number: o tecto Graham (sqrt(22.5 × EPS × BVPS)) é {cur_symbol}{v:.2f} mas pagas {cur_symbol}{t:.2f} no preço actual."
    if rule == "p_ffo":
        return f"P/FFO: REIT a {v:.1f}× o FFO/share (tecto: {t:.0f}×). Comparável a P/E para REIT."
    if rule == "interest_coverage":
        return f"Interest coverage: {v:.1f}× (mínimo {t:.1f}×). Capacidade de pagar juros."
    if rule == "cet1":
        return f"CET1 ratio: {v*100:.1f}% (mínimo regulatório+buffer: {t*100:.0f}%). Solidez de capital."
    if rule == "efficiency_ratio":
        return f"Efficiency ratio: {v*100:.0f}% (tecto: {t*100:.0f}%). Quanto menor, mais eficiente."
    if rule == "vacancy":
        return f"Vacância física: {v*100:.1f}% (tecto: {t*100:.0f}%)."
    if rule == "spread_selic_real":
        return f"Spread DY vs SELIC real: {v*100:.2f}pp (mínimo: {t*100:.0f}pp). FII compete com renda fixa."
    if rule == "liquidity":
        return f"Liquidez diária: {cur_symbol}{v:,.0f} (mínimo: {cur_symbol}{t:,.0f}). Risco de saída."
    return None


def _print_risk_panel(v: LeapOfFaithVerdict, currency: str) -> None:
    """Detailed plain-language breakdown shown when high-vitality + rejection.
    Lets the user see the real numbers and make their own call."""
    print()
    print("  ─── Painel de Decisão de Risco ───")
    print(f"  A régua diz {v.headline()}. A vitalidade diz {v.vitality_label} ({v.vitality_overall}/100).")
    print()
    print("  Para entrar mesmo assim, terias que aceitar:")
    print()
    for r in v.failed_rules:
        if r.get("structural"):
            print(f"    · [estrutural] {r['rule']} — {_explain_failure(r['rule'], r['value'], r['threshold'], currency, v.intangible_pct) or 'sem tradução'}")
            print(f"      → ignorado (P/B é estruturalmente elevado para empresas brand-heavy)")
            continue
        explain = _explain_failure(r["rule"], r["value"], r["threshold"], currency, v.intangible_pct)
        prem = _fmt_pct_premium(r["rule"], r["value"], r["threshold"])
        if explain:
            print(f"    · {explain}")
            if prem:
                print(f"      → {prem}")

    print()
    print(f"  O que diz a vitalidade ({v.vitality_label}):")
    if v.vitality_components:
        labels = {
            "scale_dominance":     "Domínio de escala (peso 20%)",
            "secular_tailwind":    "Vento estrutural 30y (peso 15%)",
            "capital_allocation":  "Alocação de capital (peso 25%)",
            "resilience_track":    "Resiliência histórica (peso 25%)",
            "earnings_durability": "Durabilidade dos lucros (peso 15%)",
        }
        for k, val in v.vitality_components.items():
            label = labels.get(k, k)
            bar = "█" * (val // 10) if val is not None else ""
            print(f"    {label:<40} {val!s:>4}  {bar}")
    print()
    if v.vitality_label == "OVERWHELMING":
        print("  ⚖️  A tese de Premium Company a 20-30 anos é forte. Mas o preço actual")
        print("      pede um leap of faith. Tu decides:")
        print("        a) Espera correcção até a régua passar (disciplina pura)")
        print("        b) Entra com posição reduzida e marca como leap_of_faith")
        print("           (aceitas o prémio acima em troca de não esperar)")
    else:
        print(f"  ⚠️  Vitalidade só {v.vitality_label} — não há base sólida para leap of faith.")
        print("      Recomendado: esperar a régua ou abandonar a tese.")
    print("  ──────────────────────────────────")


# ─── CLI ──────────────────────────────────────────────────────────────────

def _ticker_currency(ticker: str, market: str) -> str:
    db = DB_BR if market == "br" else DB_US
    if not db.exists():
        return "USD" if market == "us" else "BRL"
    with sqlite3.connect(db) as c:
        row = c.execute("SELECT currency FROM companies WHERE ticker=?", (ticker,)).fetchone()
        if row and row[0]:
            return row[0].upper()
    return "USD" if market == "us" else "BRL"


def _print_verdict(v: LeapOfFaithVerdict) -> None:
    print(f"=== Leap of Faith — {v.ticker} ({v.market.upper()}) ===")
    print(f"  Status: {v.headline()}")
    if v.screen_score is not None:
        print(f"  Screen score: {v.screen_score:.0%}  passes: {v.screen_passes}")
    if v.failed_rules:
        print(f"  Failed rules ({len(v.failed_rules)}):")
        for r in v.failed_rules:
            ratio = f"miss {r['miss_ratio']}x" if r["miss_ratio"] is not None else "miss ?"
            print(f"    · {r['rule']:<30} value={r['value']!s:<12} threshold={r['threshold']!s:<12} {ratio}")
        if v.near_miss_max is not None:
            tag = "NEAR MISS" if v.near_miss else "FAR MISS"
            print(f"  → max miss {v.near_miss_max}x  [{tag} (threshold {NEAR_MISS_THRESHOLD}x)]")
    print(f"  Vitality: {v.vitality_overall}/100 ({v.vitality_label})")
    if v.vitality_components:
        for k, val in v.vitality_components.items():
            print(f"    · {k:<22} {val}")
    if v.observations:
        print()
        print("  Observations:")
        for obs in v.observations:
            print(f"    {obs}")

    # Risk decision panel — auto-shown when high vitality + screen rejection.
    # Lets the user see the actual numbers in plain language and decide.
    show_panel = (
        v.status in ("REJECTED_NEAR_MISS", "REJECTED_FAR_MISS")
        and v.vitality_overall is not None
        and v.vitality_overall >= 80
        and v.failed_rules
    )
    if show_panel:
        currency = _ticker_currency(v.ticker, v.market)
        _print_risk_panel(v, currency)


def _holdings(market: str) -> list[str]:
    db = DB_BR if market == "br" else DB_US
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        return [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        )]


def main() -> None:
    global NEAR_MISS_THRESHOLD, INTANGIBLE_HEAVY_PB_EXEMPT
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--holdings", action="store_true", help="Run for all active holdings (BR+US)")
    ap.add_argument("--persist", action="store_true", help="Write to leap_of_faith_log table")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--threshold", type=float, default=DEFAULT_NEAR_MISS_THRESHOLD,
                    help=f"Near-miss cutoff (default {DEFAULT_NEAR_MISS_THRESHOLD}). "
                         "Lower = stricter discipline; higher = more leap candidates.")
    ap.add_argument("--strict-pb", action="store_true",
                    help="Disable P/B exemption for intangible-heavy companies (KO/PG/JNJ).")
    args = ap.parse_args()
    NEAR_MISS_THRESHOLD = args.threshold
    if args.strict_pb:
        INTANGIBLE_HEAVY_PB_EXEMPT = False

    if args.holdings:
        all_results = []
        for mkt in ("br", "us"):
            for tk in _holdings(mkt):
                tk = tk.strip()
                if not tk:
                    continue
                v = evaluate(tk, mkt)
                all_results.append(v)
                if args.persist:
                    persist(v)
        # Group by status
        by_status: dict[str, list[LeapOfFaithVerdict]] = {}
        for v in all_results:
            by_status.setdefault(v.status, []).append(v)
        print(f"=== Leap of Faith — {len(all_results)} holdings ===")
        for status in ("PASS_WITH_VITALITY", "PASS", "LEAP_OF_FAITH",
                       "REJECTED_NEAR_MISS", "REJECTED_FAR_MISS", "N/A"):
            verdicts = by_status.get(status, [])
            if not verdicts:
                continue
            print(f"\n  [{status}]  {len(verdicts)} ticker(s)")
            for v in verdicts:
                vt = v.vitality_overall if v.vitality_overall is not None else "—"
                miss = f"miss {v.near_miss_max}x" if v.near_miss_max is not None else ""
                print(f"    {v.market.upper()}:{v.ticker:<8} vit={vt!s:<3} {miss}")
        return

    if not args.ticker:
        ap.error("provide TICKER or --holdings")

    v = evaluate(args.ticker.upper(), args.market)
    if args.persist:
        persist(v)
    if args.json:
        print(json.dumps(asdict(v), indent=2, ensure_ascii=False))
    else:
        _print_verdict(v)


if __name__ == "__main__":
    main()
