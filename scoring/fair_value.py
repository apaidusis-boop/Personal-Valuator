"""fair_value — compute consensus + our_fair (safety-margin) target prices.

Methods (per market × sector) — produces the *consensus* fair (Buffett/Graham
canonical reading):

  BR non-bank, non-FII  — Graham Number = sqrt(22.5 × EPS × BVPS)
  BR bank               — min(EPS × 10, BVPS × 1.5)   (both screen ceilings)
  US non-bank, non-REIT — min(EPS × 20, BVPS × 3)     (Buffett ceiling)
  US bank               — EPS × 12                     (mid-cycle multiple)
  US REIT               — BVPS × 2                     (proxy; AFFO/FFO later)
  BR FII                — VPA (NAV anchor)

The consensus is then narrowed by `scoring._safety.build_triplet()` into
(our_fair, buy_below, hold_low, hold_high, sell_above, action) using a
per-sector safety margin (config/safety_margins.yaml). Philosophy: 1-2%
*more* conservative than the canonical Buffett/Graham margin.

History: every `compute → persist` writes a NEW row keyed by
(ticker, method, computed_at) where computed_at is an ISO **timestamp**.
Same-day re-runs no longer overwrite; the full trajectory is queryable.
Mission Control's existing `MAX(computed_at)` query keeps surfacing the
latest correctly.

Confidence: each row carries `confidence_label` ∈ {cross_validated,
single_source, disputed} via `analytics.data_confidence`. Disputed inputs
still emit a number but flagged so the orchestrator / dossier can warn.

Uso:
    python -m scoring.fair_value ACN
    python -m scoring.fair_value --all
    python -m scoring.fair_value --holdings        (default)
    python -m scoring.fair_value --upside           (just print, no compute)
    python -m scoring.fair_value ACN --history     (print all rows for ticker)
"""
from __future__ import annotations

import argparse
import math
import sqlite3
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS fair_value (
    ticker          TEXT NOT NULL,
    method          TEXT NOT NULL,
    fair_price      REAL,
    current_price   REAL,
    upside_pct      REAL,
    eps             REAL,
    bvps            REAL,
    sector          TEXT,
    inputs_json     TEXT,
    computed_at     TEXT NOT NULL,
    PRIMARY KEY (ticker, method, computed_at)
);
CREATE INDEX IF NOT EXISTS idx_fv_ticker ON fair_value(ticker);
"""

# Columns added in v2 (2026-05-08). ALTER TABLE applied lazily via _ensure_v2_columns.
# Kept additive so existing INSERT OR REPLACE callers (none) don't break.
V2_COLUMNS = [
    ("our_fair",          "REAL"),
    ("buy_below",         "REAL"),
    ("hold_low",          "REAL"),
    ("hold_high",         "REAL"),
    ("sell_above",        "REAL"),
    ("action",            "TEXT"),
    ("margin_pct",        "REAL"),
    ("our_upside_pct",    "REAL"),
    ("confidence_label",  "TEXT"),
    ("confidence_score",  "REAL"),
    ("trigger",           "TEXT"),
]

# Sector keys (lowercase) that are FIIs / REITs / Banks
_BANK_TOKENS = {"bank", "banks", "banco", "bancos"}
_FII_SECTORS = {
    "logística", "logistica", "shopping", "papel (cri)", "híbrido", "hibrido",
    "corporativo", "tijolo", "residencial", "agro", "fundo de fundos", "ffii",
}
_REIT_TOKENS = {"reit", "reits"}

# US bank ticker whitelist — catches JPM/BAC/WFC etc when companies.sector is
# "Financials" rather than "Banks". Mirrors scoring/engine.py::_US_BANK_TICKERS.
# Without this, fair_value defaults JPM to buffett_ceiling (BVPS×3 = $392) instead
# of us_bank_pe12 (EPS×12 = $254). Both produce a number; the bank multiple is
# the right reading. Phase 2026-05-09 fix.
_US_BANK_TICKERS = frozenset({
    "JPM", "BAC", "WFC", "C", "GS", "MS",
    "USB", "PNC", "TFC", "BK", "NTRS", "STT",
    "CFG", "RF", "KEY", "FITB", "MTB", "HBAN", "CMA",
    "CBSH", "WAL", "ZION",
    "COF", "DFS", "AXP",
})

# Fallback whitelist for the intangible gate. The measured trigger
# (intangible_pct_assets >= 0.25 or tangible_book_value < 0) depends on
# scripts/backfill_intangibles.py having populated those columns — but the
# daily fundamentals refresh inserts fresh rows *without* them, so between
# backfills the gate silently stops firing (this is exactly how KO/PG/JNJ
# regressed back to SELL/TRIM on 2026-05-10 despite the 2026-05-09 fix).
# These are the canonical "brand equity off the balance sheet / buybacks
# crushed BVPS" names where min(EPS×20, BVPS×3) and the SELL signal are
# unreliable. Belt-and-suspenders, mirrors _US_BANK_TICKERS. Only ever
# downgrades SELL/TRIM→HOLD (conservative direction).
_HIGH_INTANGIBLE_TICKERS = frozenset({
    "KO", "PEP", "PG", "CL", "KMB", "MDLZ", "KHC", "GIS", "HSY", "K", "SJM",
    "MO", "PM", "MCD", "SBUX", "YUM", "NKE", "EL", "CLX", "CHD",
    "JNJ", "ABT", "MMM", "HON",
    "V", "MA", "ACN", "IBM", "HD", "LOW",
})


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)
        _ensure_v2_columns(c)


def _ensure_v2_columns(c: sqlite3.Connection) -> None:
    """Lazily add v2 columns. Idempotent: ignores 'duplicate column' errors."""
    existing = {r[1] for r in c.execute("PRAGMA table_info(fair_value)").fetchall()}
    for name, ctype in V2_COLUMNS:
        if name in existing:
            continue
        try:
            c.execute(f"ALTER TABLE fair_value ADD COLUMN {name} {ctype}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                raise
    c.commit()


def _is_bank(sector: str | None, ticker: str | None = None, market: str | None = None) -> bool:
    """Bank detection. US: ticker whitelist + sector token. BR: sector token only.
    Mirrors scoring/engine.py::_is_us_bank so the two paths converge on the same
    name (JPM was the canonical mismatch — Financials sector meant fair_value
    used Buffett ceiling instead of EPS × 12 bank multiple)."""
    if market == "us" and ticker and ticker.upper() in _US_BANK_TICKERS:
        return True
    if not sector:
        return False
    s = sector.strip().lower()
    return any(tok in s for tok in _BANK_TOKENS)


def _is_fii(sector: str | None) -> bool:
    if not sector:
        return False
    return sector.strip().lower() in _FII_SECTORS


def _is_reit(sector: str | None) -> bool:
    if not sector:
        return False
    s = sector.strip().lower()
    return any(tok in s for tok in _REIT_TOKENS)


def _latest_price(c: sqlite3.Connection, ticker: str) -> float | None:
    r = c.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return r[0] if r else None


def _latest_fundamentals(c: sqlite3.Connection, ticker: str) -> dict | None:
    """Latest fundamentals snapshot. Prefers filings-derived (CVM/SEC) over
    yfinance — Phase LL Sprint 1.2 — because yfinance has documented bugs
    in BR coverage (PRIO3 ROE 9.7% yf vs 38.4% filings; BBDC4 EPS R$2.13 yf
    vs R$4.09 filings; the dual-share-class issue for BR banks).

    Fallback chain:
      1. fundamentals_from_filings   (CVM ITR/DFP, SEC XBRL when wired)
      2. fundamentals                (yfinance — last resort)

    Phase LL Sub-task B: when data_confidence flags `cvm_outlier_eps` (2-vs-1
    pattern: yf+Fundamentus agree, CVM disagrees), swap to median(yf, scraped)
    so the fair-value compute itself uses the consensus rather than the
    likely-buggy CVM number. This catches cases like VALE3 where our parser
    under-counted Q4'24 settlement loss.

    Stamps `inputs.source` so dossier can show provenance.
    """
    # Step 1: try filings first
    filings_row = None
    try:
        fr = c.execute(
            """SELECT period_end, eps_ttm, bvps, roe_ttm, source, computed_at
               FROM fundamentals_from_filings WHERE ticker=?
               ORDER BY computed_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if fr and fr[1] is not None and fr[2] is not None:
            filings_row = {
                "period_end": fr[0],
                "eps": fr[1], "bvps": fr[2], "roe": fr[3],
                "pe": None, "pb": None, "dy": None,
                "_source": fr[4],
                "_provenance": "filings",
                "_computed_at": fr[5],
            }
    except sqlite3.OperationalError:
        pass

    # Step 2: yfinance fundamentals
    yf_row = None
    # Detect optional intangible columns (added 2026-05-09)
    avail_cols = {col[1] for col in c.execute("PRAGMA table_info(fundamentals)").fetchall()}
    has_intangibles = "intangible_pct_assets" in avail_cols
    cols = "period_end, eps, bvps, roe, pe, pb, dy"
    if has_intangibles:
        cols += ", intangible_pct_assets, goodwill, other_intangibles, tangible_book_value"
    r = c.execute(
        f"""SELECT {cols}
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    if r:
        yf_row = {
            "period_end": r[0], "eps": r[1], "bvps": r[2],
            "roe": r[3], "pe": r[4], "pb": r[5], "dy": r[6],
            "_source": "yfinance",
            "_provenance": "yfinance_fallback",
        }
        if has_intangibles and len(r) > 7:
            yf_row["intangible_pct_assets"] = r[7]
            yf_row["goodwill"] = r[8]
            yf_row["other_intangibles"] = r[9]
            yf_row["tangible_book_value"] = r[10]

    # Step 3: outlier override — if filings is the outlier, swap to median(yf, scraped)
    if filings_row is not None:
        try:
            outlier = c.execute(
                """SELECT detail_json FROM data_confidence WHERE ticker=?
                   ORDER BY computed_at DESC LIMIT 1""",
                (ticker,),
            ).fetchone()
            if outlier and outlier[0]:
                import json as _json
                detail = _json.loads(outlier[0])
                if detail.get("outlier_signal") == "cvm_outlier_eps":
                    # Pull scraped EPS to compute median
                    sr = None
                    try:
                        sr = c.execute(
                            """SELECT eps, bvps FROM fundamentals_scraped
                               WHERE ticker=? AND source='fundamentus'
                               ORDER BY scraped_at DESC LIMIT 1""",
                            (ticker,),
                        ).fetchone()
                    except sqlite3.OperationalError:
                        pass
                    candidates_eps = [v for v in (
                        yf_row.get("eps") if yf_row else None,
                        sr[0] if sr else None,
                    ) if v is not None]
                    candidates_bvps = [v for v in (
                        yf_row.get("bvps") if yf_row else None,
                        sr[1] if sr else None,
                    ) if v is not None]
                    if candidates_eps and candidates_bvps:
                        # Use median (= average of 2 here) as the consensus
                        med_eps = sum(candidates_eps) / len(candidates_eps)
                        med_bvps = sum(candidates_bvps) / len(candidates_bvps)
                        return {
                            "period_end": filings_row["period_end"],
                            "eps": med_eps, "bvps": med_bvps,
                            "roe": yf_row.get("roe") if yf_row else None,
                            "pe": None, "pb": None, "dy": None,
                            "_source": "outlier_median_yf_scraped",
                            "_provenance": "outlier_override",
                            "_outlier_filings_eps": filings_row["eps"],
                        }
        except Exception:
            pass

    # Merge intangibles into whichever row wins (filings preferred over yfinance,
    # but intangibles always come from yfinance balance sheet — not in CVM/SEC
    # extracts). Phase 2026-05-09: enrichment for staples brand-equity context.
    chosen = filings_row if filings_row is not None else yf_row
    if chosen is not None and yf_row is not None:
        for k in ("intangible_pct_assets", "goodwill", "other_intangibles", "tangible_book_value"):
            if yf_row.get(k) is not None and k not in chosen:
                chosen[k] = yf_row[k]
    return chosen


def _company(c: sqlite3.Connection, ticker: str) -> dict | None:
    r = c.execute(
        "SELECT ticker, name, sector, is_holding FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not r:
        return None
    return {"ticker": r[0], "name": r[1], "sector": r[2], "is_holding": bool(r[3])}


def compute(ticker: str, market: str) -> dict | None:
    """Returns {method, fair_price, current_price, upside_pct, eps, bvps, sector, inputs}.
    Returns None if data insufficient."""
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        co = _company(c, ticker)
        if not co:
            return None
        f = _latest_fundamentals(c, ticker)
        price = _latest_price(c, ticker)

    sector = co.get("sector") or ""
    eps = (f or {}).get("eps")
    bvps = (f or {}).get("bvps")
    roe = (f or {}).get("roe")
    streak = (f or {}).get("streak")
    if streak is None:
        # ROE/streak come from a thinner schema in some BR rows; do a one-off
        # lookup to fundamentals to avoid an N/A on the modern-compounder gate.
        try:
            with sqlite3.connect(db) as _c:
                _r = _c.execute(
                    "SELECT roe, dividend_streak_years FROM fundamentals "
                    "WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                    (ticker,),
                ).fetchone()
                if _r:
                    if roe is None: roe = _r[0]
                    if streak is None: streak = _r[1]
        except sqlite3.OperationalError:
            pass
    provenance = (f or {}).get("_provenance", "unknown")
    fund_source = (f or {}).get("_source", "unknown")

    method = None
    fair = None
    inputs = {"eps": eps, "bvps": bvps,
              "fundamentals_source": fund_source,
              "fundamentals_provenance": provenance}

    # Surface intangible context for dossiers + LLM reasoning. Doesn't change
    # the canonical Buffett/Graham fair_price; just enriches the audit trail.
    # See scripts/backfill_intangibles.py docstring for rationale.
    ipa = (f or {}).get("intangible_pct_assets")
    tbv = (f or {}).get("tangible_book_value")
    if ipa is not None:
        inputs["intangible_pct_assets"] = ipa
        inputs["goodwill"] = (f or {}).get("goodwill")
        inputs["other_intangibles"] = (f or {}).get("other_intangibles")
        inputs["tangible_book_value"] = tbv
    # Intangible warning fires on:
    #   1. measured  — intangible_pct_assets >= 0.25 (threshold lowered 2026-05-09
    #      from 0.40 to catch KO at 26.7%), OR negative tangible_book_value (PG/JNJ/HD
    #      canonical case — equity is mostly goodwill+intangibles), OR
    #   2. fallback  — ticker is in _HIGH_INTANGIBLE_TICKERS and the columns are
    #      stale/missing (daily fundamentals refresh doesn't populate them).
    # The gate downstream only downgrades SELL/TRIM→HOLD and STRONG_BUY→BUY
    # (conservative direction), so a slightly generous trigger is low-risk.
    measured_hi = (ipa is not None and ipa >= 0.25) or (tbv is not None and tbv < 0)
    fallback_hi = (
        ipa is None and tbv is None
        and market == "us" and ticker.upper() in _HIGH_INTANGIBLE_TICKERS
    )
    if measured_hi or fallback_hi:
        inputs["intangible_warning"] = (
            "high_intangibles_brand_off_balance — Buffett ceiling on BVPS "
            "unreliable for this name; consider tangible_book_value carefully"
        )
        if fallback_hi:
            inputs["intangible_warning_source"] = "ticker_fallback_list"

    if market == "br":
        if _is_fii(sector):
            # FII fair value = NAV (VPA). Read fii_fundamentals if available.
            with sqlite3.connect(db) as c:
                r = c.execute(
                    "SELECT vpa FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                    (ticker,),
                ).fetchone()
            vpa = r[0] if r else None
            if vpa and vpa > 0:
                method, fair = "fii_nav", float(vpa)
                inputs = {"vpa": vpa}
        elif _is_bank(sector, ticker, market):
            if eps and bvps and eps > 0 and bvps > 0:
                method = "br_bank_mult"
                fair = min(eps * 10.0, bvps * 1.5)
        else:
            if eps and bvps and eps > 0 and bvps > 0:
                method = "graham_number"
                fair = math.sqrt(22.5 * eps * bvps)
    else:  # us
        if _is_reit(sector):
            if bvps and bvps > 0:
                method, fair = "reit_pb_proxy", bvps * 2.0
        elif _is_bank(sector, ticker, market):
            if eps and eps > 0:
                method, fair = "us_bank_pe12", eps * 12.0
        else:
            # Modern compounder check: high-ROE + long-streak names (AAPL/MSFT/V/HD)
            # have BVPS deceptively low because of buybacks + organic brand value
            # off-balance. The bvps×3 leg of Buffett ceiling dominates min() and
            # produces nonsense (AAPL fair $22 vs price $293). When ROE ≥ 25%
            # AND streak ≥ 10y, drop the bvps leg — keep eps×20 (still the Buffett
            # P/E discipline) without penalizing organic compounders. Phase 2026-05-09.
            modern_compounder = (
                eps and eps > 0 and bvps and bvps > 0
                and roe is not None
                and (roe if abs(roe) > 1.5 else roe * 100) >= 25  # 25% threshold; normalize to %
                and streak is not None and int(streak or 0) >= 10
            )
            if modern_compounder:
                method = "modern_compounder_pe20"
                fair = eps * 20.0
                inputs["modern_compounder_reason"] = (
                    f"ROE={(roe if abs(roe) > 1.5 else roe * 100):.1f}% streak={streak}y "
                    "→ buffett_ceiling bvps×3 leg dropped (compounder bias)"
                )
            elif eps and bvps and eps > 0 and bvps > 0:
                method = "buffett_ceiling"
                fair = min(eps * 20.0, bvps * 3.0)

    if method is None or fair is None or price is None or price <= 0:
        return None

    # Consensus upside (vs Buffett/Graham raw fair)
    upside = (fair / price - 1.0) * 100.0

    # Apply per-sector safety margin -> our_fair + action triplet
    from scoring._safety import build_triplet, resolve_margin
    margin_pct = resolve_margin(market, sector or None, ticker)
    triplet = build_triplet(consensus_fair=fair, price=price, margin_pct=margin_pct)
    our_upside = None
    if triplet["our_fair"] is not None:
        our_upside = (triplet["our_fair"] / price - 1.0) * 100.0

    # Confidence label (BR uses CVM cross-check; US is single-source today).
    confidence = _confidence_for(market, ticker)

    # Phase LL Sprint 1.4 — confidence as GATE.
    raw_action = triplet["action"]
    gated_action = raw_action
    gate_reasons: list[str] = []

    # Confidence gate (sources disagree -> dampen conviction)
    if raw_action and confidence.get("label") == "disputed":
        if raw_action in ("STRONG_BUY", "BUY"):
            gated_action = "HOLD"
            gate_reasons.append(f"confidence=disputed downgraded {raw_action}→HOLD")
    elif raw_action and confidence.get("label") == "single_source":
        if raw_action == "STRONG_BUY":
            gated_action = "BUY"
            gate_reasons.append("confidence=single_source downgraded STRONG_BUY→BUY")

    # Phase 2026-05-09 — intangible_warning gate.
    # When intangible_pct_assets >= 0.40, Buffett ceiling = sqrt(22.5 × EPS × BVPS)
    # / min(EPS × 20, BVPS × 3) is biased LOW because brand value is
    # off-balance-sheet. The SELL signal becomes unreliable — PG/JNJ/KO are
    # the canonical false-SELL cases (tangible BV negative for PG/JNJ; the
    # ceiling fires SELL on exactly the names Buffett owns in real life).
    #
    # Treatment:
    #   SELL / TRIM      → HOLD  (downside signal can't be trusted)
    #   STRONG_BUY       → BUY   (upside signal valid but ceiling is conservative;
    #                             dampen conviction since the anchor itself is shaky)
    #   confidence_label → downgraded one notch so dossier surfaces caveat
    if "intangible_warning" in inputs:
        ipa_pct = (ipa or 0.0)
        tbv_neg = "tbv<0" if (tbv is not None and tbv < 0) else f"ipa={ipa_pct:.0%}"
        if gated_action in ("SELL", "TRIM"):
            gate_reasons.append(
                f"intangibles_{tbv_neg} — Buffett ceiling unreliable, {gated_action}→HOLD"
            )
            gated_action = "HOLD"
        elif gated_action == "STRONG_BUY":
            gate_reasons.append(
                f"intangibles_{tbv_neg} — ceiling biased low, STRONG_BUY→BUY"
            )
            gated_action = "BUY"
        # Downgrade confidence one notch
        if confidence.get("label") == "cross_validated":
            confidence = dict(confidence)
            confidence["label"] = "single_source"
            if confidence.get("score") is not None:
                confidence["score"] = round(confidence["score"] * 0.6, 3)
            inputs["confidence_downgraded_by_intangibles"] = True

    # Phase LL Sprint 1.6 — distress vetoes via Altman + Piotroski.
    # Even if price screams BUY, distress signals override. TEN was the
    # canonical false-positive (memory ten_distress_signal flagged 4
    # distress signals but buffett_ceiling formula said BUY).
    # Stays inside the 6-stance vocab (Phase FF Bloco 3.1):
    #   altman_distress  → SELL  (don't hold a distressed name regardless of price)
    #   piotroski_weak   → HOLD  (downgrade BUY signals to wait-and-see)
    distress = _check_distress_vetoes(market, ticker, sector)
    if distress["altman_distress"]:
        if gated_action in ("STRONG_BUY", "BUY", "HOLD", "TRIM"):
            gate_reasons.append(
                f"altman_distress Z={distress['z']} forced {gated_action}→SELL"
            )
            gated_action = "SELL"
    elif distress["piotroski_weak"]:
        if gated_action in ("STRONG_BUY", "BUY"):
            gate_reasons.append(
                f"piotroski_weak F={distress['f']} forced {gated_action}→HOLD"
            )
            gated_action = "HOLD"

    # Phase LL.2 — macro overlay.
    # Consult regime + sector fit. Two effects:
    #   hard_hold  → force HOLD even on STRONG_BUY (cyclical at peak)
    #   downgrade  → STRONG_BUY → BUY → HOLD (one notch less aggressive)
    #   reinforce  → no action change but logged for dossier narrative
    macro = _check_macro_overlay(market, sector)
    if macro.get("action_adjust") == "hard_hold":
        if gated_action in ("STRONG_BUY", "BUY"):
            gate_reasons.append(
                f"macro_hard_hold {macro['reason']} forced {gated_action}→HOLD"
            )
            gated_action = "HOLD"
    elif macro.get("action_adjust") == "downgrade":
        downgrade_map = {"STRONG_BUY": "BUY", "BUY": "HOLD"}
        if gated_action in downgrade_map:
            new_action = downgrade_map[gated_action]
            gate_reasons.append(
                f"macro_downgrade {macro['reason']} forced {gated_action}→{new_action}"
            )
            gated_action = new_action
    elif macro.get("action_adjust") == "reinforce":
        gate_reasons.append(f"macro_reinforce {macro['reason']} (no change, dossier note)")

    triplet["action"] = gated_action
    inputs["action_pre_gate"] = raw_action
    inputs["action_post_gate"] = gated_action
    inputs["gate_reason"] = " | ".join(gate_reasons) if gate_reasons else "no_gate_applied"
    if distress.get("z") is not None:
        inputs["altman_z"] = distress["z"]
    if distress.get("f") is not None:
        inputs["piotroski_f"] = distress["f"]
    if macro.get("regime"):
        inputs["macro_regime"] = macro["regime"]
        inputs["macro_action_adjust"] = macro["action_adjust"]

    return {
        "ticker": ticker, "market": market, "sector": sector,
        "method": method,
        "fair_price": round(fair, 4),          # consensus
        "current_price": round(price, 4),
        "upside_pct": round(upside, 2),         # vs consensus
        "eps": eps, "bvps": bvps,
        "inputs": inputs,
        # v2 fields
        "our_fair": triplet["our_fair"],
        "buy_below": triplet["buy_below"],
        "hold_low": triplet["hold_low"],
        "hold_high": triplet["hold_high"],
        "sell_above": triplet["sell_above"],
        "action": triplet["action"],
        "margin_pct": triplet["margin_pct"],
        "our_upside_pct": round(our_upside, 2) if our_upside is not None else None,
        "confidence_label": confidence["label"],
        "confidence_score": confidence["score"],
        "confidence_detail": confidence.get("detail"),
    }


def _check_macro_overlay(market: str, sector: str | None) -> dict:
    """Phase LL.2 — consult `analytics.regime` and `config/macro_sector_fit.yaml`
    to determine if the current macro phase warrants action adjustment.

    Returns dict with keys: regime, action_adjust, reason. action_adjust:
      'downgrade'   - downgrade STRONG_BUY/BUY by one step
      'hard_hold'   - force HOLD regardless of price (cyclical at peak)
      'reinforce'   - log-only, no action change but dossier explains
      'no_change'   - default; nothing surfaced
    """
    out = {"regime": None, "action_adjust": "no_change", "reason": None}
    if not sector:
        return out
    try:
        from analytics.regime import classify
        r = classify(market)
        if not r or not r.regime:
            return out
        out["regime"] = r.regime
    except Exception:
        return out

    # Load fit map
    try:
        import yaml as _yaml
        cfg_path = ROOT / "config" / "macro_sector_fit.yaml"
        if not cfg_path.exists():
            return out
        cfg = _yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return out

    market_map = cfg.get(market, {}) or {}
    # Sector lookup is exact match — sector strings come from companies.sector
    sector_rules = market_map.get(sector)
    if not sector_rules:
        return out
    adjust = sector_rules.get(out["regime"], "no_change")
    out["action_adjust"] = adjust
    out["reason"] = f"{market}/{sector}/{out['regime']}={adjust}"
    return out


def _check_distress_vetoes(market: str, ticker: str, sector: str | None) -> dict:
    """Run Altman Z-Score + Piotroski F-Score and return veto signals.

    Returns dict with keys: altman_distress (bool), piotroski_weak (bool),
    z (float|None), f (int|None). Both engines exclude FIIs/REITs/Banks
    where the metrics don't apply, so banks like BBDC4 won't be vetoed
    by Altman even if Z would be technically computed.
    """
    out = {"altman_distress": False, "piotroski_weak": False, "z": None, "f": None}
    # Skip when ratios don't apply
    s = (sector or "").lower()
    skip = any(tok in s for tok in ("bank", "banks", "banco", "bancos", "reit", "reits"))
    skip = skip or _is_fii(sector or "")
    if skip:
        return out
    try:
        from scoring.altman import compute as altman_compute
        a = altman_compute(ticker, market)
        if a and getattr(a, "applicable", False) and a.z is not None:
            out["z"] = round(a.z, 2)
            out["altman_distress"] = a.is_distress
    except Exception:
        pass
    try:
        from scoring.piotroski import compute as piotroski_compute
        p = piotroski_compute(ticker, market)
        if p and getattr(p, "applicable", False) and p.f_score is not None:
            out["f"] = p.f_score
            out["piotroski_weak"] = p.is_weak
    except Exception:
        pass
    return out


def _confidence_for(market: str, ticker: str) -> dict:
    """Lookup confidence from `analytics.data_confidence` if available; else
    default to 'single_source'. Lazy import to avoid hard dep at engine load."""
    try:
        from analytics.data_confidence import latest_label
        row = latest_label(market, ticker)
        if row:
            return row
    except Exception:
        pass
    return {"label": "single_source", "score": None, "detail": None}


def persist(result: dict, *, trigger: str | None = None) -> None:
    """Append-only persist. Uses ISO timestamp (not date) so same-day re-runs
    each get their own row — full history queryable via ORDER BY computed_at.
    `trigger` is optional context (e.g. "manual", "filing:BBDC4:2026-05-08",
    "cron:daily") for downstream filtering.
    """
    market = result["market"]
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    now_iso = datetime.now(UTC).isoformat(timespec="seconds")
    import json as _json
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT INTO fair_value
                 (ticker, method, fair_price, current_price, upside_pct,
                  eps, bvps, sector, inputs_json, computed_at,
                  our_fair, buy_below, hold_low, hold_high, sell_above,
                  action, margin_pct, our_upside_pct,
                  confidence_label, confidence_score, trigger)
               VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?, ?,?,?)""",
            (
                result["ticker"], result["method"], result["fair_price"],
                result["current_price"], result["upside_pct"],
                result.get("eps"), result.get("bvps"), result.get("sector"),
                _json.dumps(result.get("inputs") or {}, ensure_ascii=False),
                now_iso,
                result.get("our_fair"), result.get("buy_below"),
                result.get("hold_low"), result.get("hold_high"),
                result.get("sell_above"),
                result.get("action"), result.get("margin_pct"),
                result.get("our_upside_pct"),
                result.get("confidence_label"), result.get("confidence_score"),
                trigger or "manual",
            ),
        )
        c.commit()


def history(ticker: str, market: str, *, limit: int = 50) -> list[dict]:
    """Return historical fair_value rows for ticker, oldest→newest."""
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    with sqlite3.connect(db) as c:
        rows = c.execute(
            """SELECT computed_at, method, fair_price, our_fair, current_price,
                      action, confidence_label, trigger
               FROM fair_value WHERE ticker=?
               ORDER BY computed_at DESC LIMIT ?""",
            (ticker, limit),
        ).fetchall()
    out = [
        {"computed_at": r[0], "method": r[1], "fair_price": r[2], "our_fair": r[3],
         "current_price": r[4], "action": r[5], "confidence_label": r[6],
         "trigger": r[7]}
        for r in rows
    ]
    out.reverse()  # oldest first
    return out


def _load_tickers(scope: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if scope == "holdings":
                rows = c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ).fetchall()
            else:
                rows = c.execute("SELECT ticker FROM companies").fetchall()
            for (t,) in rows:
                out.append((t, market))
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=False)
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--upside", action="store_true",
                    help="apenas listar último fair value persistido")
    ap.add_argument("--history", action="store_true",
                    help="(com --ticker) imprime trajectória histórica do ticker")
    ap.add_argument("--trigger", default="manual",
                    help="contexto persistido em fair_value.trigger (ex: 'filing:BBDC4:2026-05-08')")
    args = ap.parse_args()

    if args.ticker and args.history:
        tk = args.ticker.upper()
        for market, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                if not c.execute("SELECT 1 FROM companies WHERE ticker=?", (tk,)).fetchone():
                    continue
            print(f"\n=== {tk} fair value history ({market.upper()}) ===")
            for h in history(tk, market, limit=200):
                print(
                    f"  {h['computed_at']:<25} {h['method']:<18} "
                    f"fair={h['fair_price']:>9.2f} our={h['our_fair'] or 0:>9.2f} "
                    f"price={h['current_price']:>9.2f} {h['action'] or 'N/A':<11} "
                    f"[{h['confidence_label'] or '-'}] trig={h['trigger']}"
                )
            return 0
        print(f"{tk}: not found")
        return 1

    if args.upside:
        for market, db in (("br", DB_BR), ("us", DB_US)):
            _ensure_schema(db)
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    """SELECT fv.ticker, fv.method, fv.fair_price, fv.current_price,
                              fv.upside_pct, fv.computed_at, c.is_holding
                       FROM fair_value fv LEFT JOIN companies c ON c.ticker=fv.ticker
                       WHERE fv.computed_at = (
                         SELECT MAX(computed_at) FROM fair_value f2
                         WHERE f2.ticker=fv.ticker AND f2.method=fv.method
                       )
                       ORDER BY fv.upside_pct DESC""",
                ).fetchall()
            if rows:
                print(f"\n=== {market.upper()} fair value (most recent) ===")
                for tk, m, fair, cur, up, dt, h in rows:
                    mark = "★" if h else " "
                    print(f"  {mark} {tk:<8} {m:<18} fair={fair:>10.2f}  cur={cur:>10.2f}  upside={up:>+6.1f}%  ({dt})")
        return 0

    if args.ticker:
        tk = args.ticker.upper()
        # detect market
        market = None
        for m, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                if c.execute("SELECT 1 FROM companies WHERE ticker=?", (tk,)).fetchone():
                    market = m
                    break
        if not market:
            print(f"{tk}: not found")
            return 1
        targets = [(tk, market)]
    elif args.all:
        targets = _load_tickers("universe")
    else:
        targets = _load_tickers("holdings")

    print(f"Computing fair value for {len(targets)} ticker(s)...")
    ok = skipped = 0
    for tk, market in targets:
        try:
            r = compute(tk, market)
            if r is None:
                skipped += 1
                continue
            persist(r, trigger=args.trigger)
            ok += 1
            our = r.get("our_fair")
            our_str = f"{our:>10.2f}" if our is not None else "       N/A"
            act = r.get("action") or "—"
            conf = (r.get("confidence_label") or "-")[:6]
            print(
                f"  {tk:<8} {r['method']:<18} fair={r['fair_price']:>10.2f}"
                f"  our={our_str}  cur={r['current_price']:>10.2f}"
                f"  {act:<11}  [{conf}]"
            )
        except Exception as e:  # noqa: BLE001
            print(f"  {tk}: error — {e}")
            skipped += 1
    print(f"\nPersisted {ok} | skipped {skipped} (insufficient data).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
