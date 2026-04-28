"""thesis_synthesizer — gera ## Thesis section para ticker notes via Ollama local.

Phase G (2026-04-26). Substitui placeholder/missing thesis com Core/Assumptions/
Triggers/Intent estruturado, derivado de fundamentals + quarterly_history +
synthetic_ic_debate + variant_perception se existirem.

100% Ollama local (Qwen 14B). Zero Claude tokens.

Filosofia injectada no prompt:
  - Buffett/Graham: quality > price, margem de segurança, dividendos consistentes
  - DRIP focus: long horizon, compounders preferidos
  - BR/US criteria diferentes (CLAUDE.md tem regras explícitas)
  - Special tickers: GREK = tactical (irregular divs), FIIs = framework próprio

Uso:
    python -m agents.thesis_synthesizer GREK              # 1 ticker
    python -m agents.thesis_synthesizer GREK GS HD        # vários
    python -m agents.thesis_synthesizer --holdings-missing # all holdings score=-1
    python -m agents.thesis_synthesizer --dry-run GREK    # preview, no write
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"

MODEL = "qwen2.5:14b-instruct-q4_K_M"

# Tickers com regras específicas que o user tem em memória persistente
SPECIAL_INTENT = {
    "GREK": "Tactical (NÃO DRIP — dividendos semianuais irregulares; reclassificado tactical 2026-04)",
    "BN":   "Compounder pós-split 2023 (não growth pura)",
    "XP":   "Growth (não DRIP)",
}


def _resolve_market(ticker: str) -> str:
    """Determine BR vs US by querying companies table."""
    for market, db in DBS.items():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return market
    return "us"  # default


def _fundamentals(market: str, ticker: str) -> dict:
    db = DBS[market]
    if not db.exists():
        return {}
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,)).fetchone()
        deep = c.execute(
            "SELECT * FROM deep_fundamentals WHERE ticker=? LIMIT 1",
            (ticker,)).fetchone()
        comp = c.execute(
            "SELECT name, sector, currency FROM companies WHERE ticker=?",
            (ticker,)).fetchone()
    out: dict = {}
    if row:
        out.update({k: row[k] for k in row.keys()})
    if deep:
        out.update({f"deep_{k}": deep[k] for k in deep.keys() if k not in ("ticker",)})
    if comp:
        out["name"] = comp["name"]
        out["sector"] = comp["sector"]
        out["currency"] = comp["currency"]
    return out


def _read_section(ticker: str, suffix: str, max_chars: int = 1500) -> str:
    p = TICKERS_DIR / f"{ticker}{suffix}.md"
    if not p.exists():
        return ""
    text = p.read_text(encoding="utf-8", errors="ignore")
    return text[:max_chars]


def _build_context(ticker: str, market: str) -> str:
    f = _fundamentals(market, ticker)
    lines = [f"TICKER: {market.upper()}:{ticker}"]
    if f.get("name"):
        lines.append(f"NAME: {f['name']}")
    if f.get("sector"):
        lines.append(f"SECTOR: {f['sector']}")

    metrics = []
    for k, label in [("pe", "P/E"), ("pb", "P/B"), ("dy", "DY"),
                     ("roe", "ROE"), ("net_debt_ebitda", "Net Debt/EBITDA"),
                     ("dividend_streak_years", "Dividend streak (yrs)"),
                     ("is_aristocrat", "Aristocrat")]:
        v = f.get(k)
        if v is None:
            continue
        if k in ("dy", "roe") and isinstance(v, float) and abs(v) < 5:
            metrics.append(f"  {label}: {v * 100:.2f}%")
        elif k == "is_aristocrat":
            metrics.append(f"  {label}: {'YES' if v else 'NO'}")
        else:
            metrics.append(f"  {label}: {v}")
    if metrics:
        lines.append("\nFUNDAMENTALS LATEST:")
        lines.extend(metrics)

    # Deep fundamentals (current_ratio, mkt cap, beta if available)
    deep_metrics = []
    for k in ("deep_current_ratio", "deep_market_cap_usd", "deep_beta_levered",
             "deep_long_term_debt", "deep_working_capital"):
        v = f.get(k)
        if v is None:
            continue
        clean = k.replace("deep_", "")
        if clean == "market_cap_usd":
            deep_metrics.append(f"  Market cap (USD): ${v / 1e9:.1f}B")
        else:
            deep_metrics.append(f"  {clean}: {v}")
    if deep_metrics:
        lines.append("\nDEEP FUNDAMENTALS:")
        lines.extend(deep_metrics)

    # IC debate snapshot if exists (committee verdict + consensus)
    ic_text = _read_section(ticker, "_IC_DEBATE", 800)
    if ic_text:
        # Extract just the committee_verdict line + consensus
        m = re.search(r"committee_verdict:\s*(\w+)", ic_text)
        m2 = re.search(r"consensus_pct:\s*([\d.]+)", ic_text)
        if m:
            lines.append(f"\nIC COMMITTEE VERDICT: {m.group(1)}"
                         + (f" ({m2.group(1)}% consensus)" if m2 else ""))

    # Variant view snapshot
    var_text = _read_section(ticker, "_VARIANT", 600)
    if var_text:
        m = re.search(r"variance:\s*(\w+)", var_text)
        m2 = re.search(r"magnitude:\s*(\d+)", var_text)
        if m:
            lines.append(f"VARIANT vs CONSENSUS: {m.group(1)}"
                         + (f" magnitude {m2.group(1)}/5" if m2 else ""))

    return "\n".join(lines)


# Investor philosophy + market criteria injected into every prompt
PHILOSOPHY_BR_NONFINANCIAL = """
**Filosofia (Brasil, não-financeiras — Graham clássico ajustado a Selic alta)**:
- Graham Number ≤ 22.5 (sqrt(22.5 × EPS × BVPS) ≥ preço)
- Dividend Yield ≥ 6%
- ROE ≥ 15%
- Dívida líquida / EBITDA < 3×
- Histórico de dividendos ≥ 5 anos ininterrupto
"""

PHILOSOPHY_BR_BANK = """
**Filosofia (Brasil, bancos)**:
- P/E ≤ 10, P/B ≤ 1.5, DY ≥ 6%, ROE ≥ 12%, dividend streak ≥ 5y
- Graham Number e Dív/EBITDA NÃO se aplicam (estrutura de capital diferente)
"""

PHILOSOPHY_US = """
**Filosofia (EUA — Buffett, qualidade sobre preço)**:
- P/E ≤ 20, P/B ≤ 3, DY ≥ 2.5%, ROE ≥ 15%
- Dividend Aristocrat OU mínimo 10y consecutivos de dividendos
- Long horizon (anos, não meses); DRIP é o default
"""

PHILOSOPHY_FII = """
**Filosofia (FIIs — Real Estate Funds Brasil)**:
- DY mensal recorrente é o motor; tipicamente 8-12% anualizado
- P/VP < 1.0 = desconto sobre patrimônio líquido (margem segurança)
- Vacancy rate, contratos atípicos, carteira diversificada
- Categoria: Tijolo (shoppings, lajes, logística) | Papel (CRI) | Híbrido
"""

PHILOSOPHY_REIT = """
**Filosofia (REITs / monthly dividend)**:
- AFFO yield, payout ratio sustainable, debt/EBITDA controlado
- Lease structure, tenant concentration, occupancy
- O / Realty Income é o monthly dividend benchmark
"""

PHILOSOPHY_ETF = """
**Filosofia (ETFs)**:
- Tactical / sleeve allocation, NÃO DRIP individual
- Expense ratio, tracking error, liquidity, currency exposure
- Eventos (rebalance) podem mover dividendos significativamente
"""


def _select_philosophy(ticker: str, market: str, fund: dict) -> str:
    sector = (fund.get("sector") or "").lower()
    if sector == "etf" or "etf" in (fund.get("name") or "").lower():
        return PHILOSOPHY_ETF
    if "reit" in sector:
        return PHILOSOPHY_REIT
    if market == "br":
        if "shopping" in sector or "real estate" in sector or ticker.endswith("11"):
            return PHILOSOPHY_FII
        if "bank" in sector or sector == "banks":
            return PHILOSOPHY_BR_BANK
        return PHILOSOPHY_BR_NONFINANCIAL
    return PHILOSOPHY_US


def synthesize(ticker: str, market: str | None = None,
               timeout: int = 180) -> dict | None:
    market = market or _resolve_market(ticker)
    fund = _fundamentals(market, ticker)
    if not fund:
        return {"error": f"no fundamentals row for {ticker}"}

    context = _build_context(ticker, market)
    philosophy = _select_philosophy(ticker, market, fund)
    today = date.today().isoformat()
    special_note = SPECIAL_INTENT.get(ticker, "")

    prompt = f"""Você é um analyst sénior buy-side a escrever a thesis de uma posição
para um value-investor pessoa física. Português PT-BR.

{philosophy}

CONTEXT (factual, do nosso DB local + IC debate + variant scan):
{context}

{f'NOTA ESPECIAL: {special_note}' if special_note else ''}

TAREFA: Escreve a Thesis estruturada para este ticker. Usa SÓ os números do
context — não inventes. Se algum critério da filosofia falhar (ex: ROE < 15%
para US), diz isso explicitamente. Os disconfirmation triggers DEVEM ser
quantitativos e específicos (não vagos).

Output JSON apenas (sem markdown, sem comentários):

{{
  "core_thesis": "2-4 frases. O que é o business e qual o caso bull/value-add. Inclui métricas chave do context.",
  "key_assumptions": [
    "assumption 1 — específica, falsificável",
    "assumption 2",
    "assumption 3",
    "assumption 4"
  ],
  "disconfirmation_triggers": [
    "trigger 1 — quantitativo (ex: 'ROE cai abaixo de 12% por 2 quarters consecutivos')",
    "trigger 2",
    "trigger 3",
    "trigger 4"
  ],
  "intent": "DRIP compounder | Growth | Tactical | Value/turnaround | etc — uma linha"
}}
"""

    from agents._llm import ollama_call_typed
    from agents._schemas import ThesisDraft

    td = ollama_call_typed(
        prompt,
        ThesisDraft,
        model=MODEL,
        max_tokens=800,
        temperature=0.4,
        timeout=timeout,
    )
    if td is None:
        return {"error": "ollama_or_validation_failed"}

    return {
        "ticker": ticker, "market": market, "date": today,
        "core_thesis": td.core_thesis,
        "key_assumptions": td.key_assumptions,
        "disconfirmation_triggers": td.disconfirmation_triggers,
        "intent": td.intent,
    }


def format_thesis_md(t: dict) -> str:
    """Output o ## Thesis section em markdown (no leading indent)."""
    assumptions = "\n".join(f"{i+1}. {a}" for i, a in enumerate(t["key_assumptions"]))
    triggers = "\n".join(f"- {tr}" for tr in t["disconfirmation_triggers"])
    intent_clean = (t["intent"] or "").split("|")[0].strip()  # drop alt branches
    return (
        f"\n**Core thesis ({t['date']})**: {t['core_thesis']}\n\n"
        f"**Key assumptions**:\n{assumptions}\n\n"
        f"**Disconfirmation triggers**:\n{triggers}\n\n"
        f"**Intent**: {intent_clean}\n\n"
        f"---\n*Gerado por thesis_synthesizer · Ollama Qwen 14B local*\n"
    )


def insert_thesis(ticker: str, thesis_md: str, dry_run: bool = False) -> str:
    """Insere ## Thesis após ## 🎯 Verdict (ou no início se Verdict não existir).
    Returns status: "written" | "exists" | "no_note".

    Implementação line-by-line (sem regex) para evitar catastrophic backtracking
    em ticker notes longos.
    """
    p = TICKERS_DIR / f"{ticker}.md"
    if not p.exists():
        return "no_note"
    text = p.read_text(encoding="utf-8")
    if "## Thesis" in text:
        return "exists"

    section = "\n## Thesis\n" + thesis_md.rstrip() + "\n"

    lines = text.split("\n")
    insert_at: int | None = None
    in_verdict = False

    for i, line in enumerate(lines):
        if line.startswith("## "):
            if in_verdict:
                # End of Verdict section reached; insert here
                insert_at = i
                break
            if "Verdict" in line or "verdict" in line.lower():
                in_verdict = True
                continue
            # First non-Verdict ## section — insert here as fallback
            if insert_at is None and not in_verdict:
                insert_at = i
                break

    if insert_at is None:
        # No ## section at all → append at end
        new_text = text.rstrip() + "\n" + section
    else:
        new_text = "\n".join(lines[:insert_at]) + "\n" + section + "\n".join(lines[insert_at:])

    if not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return "written"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", help="ticker symbols (or use --holdings-missing)")
    ap.add_argument("--market", choices=["br", "us"], help="force market (rare)")
    ap.add_argument("--holdings-missing", action="store_true",
                    help="select all holdings with thesis_health score=-1")
    ap.add_argument("--watchlist-missing", action="store_true",
                    help="select ALL universe tickers (holdings+watchlist) with thesis_health score=-1")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--print-thesis", action="store_true",
                    help="print generated thesis md (default: only on dry-run)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    tickers: list[tuple[str, str]] = []
    if args.holdings_missing or args.watchlist_missing:
        with sqlite3.connect(DBS["br"]) as c:
            rows = c.execute("""
                SELECT subject_id FROM perpetuum_health
                WHERE perpetuum_name='thesis' AND score=-1
                  AND run_date=(SELECT MAX(run_date) FROM perpetuum_health WHERE perpetuum_name='thesis')
            """).fetchall()
        all_no_thesis = [r[0] for r in rows]
        if args.holdings_missing:
            # filter to holdings only
            holds_set: set[tuple[str, str]] = set()
            for market, db in DBS.items():
                if not db.exists():
                    continue
                with sqlite3.connect(db) as c:
                    for (t,) in c.execute(
                        "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                    ).fetchall():
                        holds_set.add((market, t))
            for sid in all_no_thesis:
                mkt, _, t = sid.partition(":")
                if (mkt, t) in holds_set and (mkt, t) not in tickers:
                    tickers.append((mkt, t))
        else:  # watchlist_missing — full universe with score=-1
            seen = set()
            for sid in all_no_thesis:
                mkt, _, t = sid.partition(":")
                if (mkt, t) not in seen:
                    seen.add((mkt, t))
                    tickers.append((mkt, t))
    else:
        for t in args.tickers:
            mkt = args.market or _resolve_market(t)
            tickers.append((mkt, t))

    if not tickers:
        print("No tickers to process. Use --holdings-missing or pass tickers.")
        return

    print(f"Synthesizing thesis for {len(tickers)} ticker(s):")
    for mkt, t in tickers:
        print(f"  {mkt}:{t}")
    print()

    summary = {"written": 0, "exists": 0, "no_note": 0, "error": 0, "skipped": 0}
    for mkt, t in tickers:
        # Pre-check: skip Ollama call entirely if ticker already has ## Thesis
        # (idempotent re-run shouldn't re-pay Ollama tax). Only checks vault.
        note_path = TICKERS_DIR / f"{t}.md"
        if note_path.exists():
            try:
                if "## Thesis" in note_path.read_text(encoding="utf-8"):
                    summary["skipped"] += 1
                    print(f"[{t}] skip — already has ## Thesis")
                    continue
            except Exception:
                pass

        print(f"[{t}] Calling Qwen 14B...")
        result = synthesize(t, mkt)
        if not result or result.get("error"):
            print(f"  ERROR: {result.get('error') if result else 'none'}")
            summary["error"] += 1
            continue
        thesis_md = format_thesis_md(result)
        if args.dry_run or args.print_thesis:
            print("  ---generated---")
            for line in thesis_md.split("\n"):
                print(f"    {line}")
            print("  ---/generated---")
        status = insert_thesis(t, thesis_md, dry_run=args.dry_run)
        summary[status] += 1
        print(f"  → {status}{' (dry-run)' if args.dry_run else ''}")
        print()

    print("=== Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
