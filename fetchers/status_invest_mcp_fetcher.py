"""Status Invest MCP fetcher — substitui o scraper HTML frágil.

Usa MCP `status-invest` já loaded no harness Claude Code. Output rico:
  - Price + 52w range + 12m variation
  - Full valuation (DY, P/L, P/VP, PEG, EV/EBITDA, LPA, VPA, ...)
  - Debt ratios (Dív líq/PL, Dív líq/EBITDA)
  - Efficiency margins (Bruta, EBITDA, EBIT, Líquida)
  - Profitability (ROE, ROA, ROIC)
  - Growth (CAGR receitas 5y, CAGR lucros 5y)

Substitui:
  fetchers/fii_statusinvest_scraper.py  (HTML scraping, frágil)

Uso (outside Claude harness, with MCP proxy):
    # Quando este fetcher for chamado, o assistant orquestra a call MCP
    # e escreve output em `data/statusinvest_cache/<ticker>.json`

Uso dentro de script Python normal:
    from fetchers.status_invest_mcp_fetcher import parse_mcp_payload, upsert_fundamentals
    parsed = parse_mcp_payload(payload_json)
    upsert_fundamentals(parsed, market='br')

Porque o cache externo? MCPs são orquestrados pelo assistant (não chamáveis via
requests.post directo). Pattern: o perpetuum_validator pede ao assistant um
refresh via cron/hook, assistant popula o cache JSON, fetcher lê e grava DB.
"""
from __future__ import annotations

import json
import sqlite3
import unicodedata
from datetime import date
from pathlib import Path


def _norm(s: str) -> str:
    """Normaliza unicode (NFC) e casefold para comparação robusta."""
    return unicodedata.normalize("NFC", s).casefold()

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "data" / "statusinvest_cache"
BR_DB = ROOT / "data" / "br_investments.db"


def _indicator(block: list[dict], group_title: str, indicator_title: str) -> float | None:
    """Extrai valor de `indicators[group].values[indicator]`. Unicode-safe."""
    gt_norm = _norm(group_title)
    it_norm = _norm(indicator_title)
    for grp in block:
        if _norm(grp.get("title", "")) == gt_norm:
            for item in grp.get("values", []):
                if _norm(item.get("title", "")) == it_norm:
                    v = item.get("value")
                    return float(v) if v is not None else None
    return None


def parse_mcp_payload(payload: dict) -> dict:
    """Converte output do MCP status-invest para nosso schema interno."""
    resume = payload.get("resume", {})
    indicators = payload.get("indicators", [])

    return {
        "ticker": payload["stock"],
        "fetched_at": date.today().isoformat(),
        "url": payload.get("url"),
        "price": resume.get("price", {}).get("value"),
        "price_variation_today_pct": resume.get("price", {}).get("variation"),
        "week52_low": resume.get("min52weeks", {}).get("value"),
        "week52_high": resume.get("max52weeks", {}).get("value"),
        "valuation_12m_pct": resume.get("valuation12Months", {}).get("value"),

        # Valuation
        "dy": _indicator(indicators, "indicadoresDeValuation", "D.Y"),
        "pe": _indicator(indicators, "indicadoresDeValuation", "P/L"),
        "pb": _indicator(indicators, "indicadoresDeValuation", "P/VP"),
        "peg": _indicator(indicators, "indicadoresDeValuation", "PEG Ratio"),
        "ev_ebitda": _indicator(indicators, "indicadoresDeValuation", "EV/EBITDA"),
        "ev_ebit": _indicator(indicators, "indicadoresDeValuation", "EV/EBIT"),
        "lpa": _indicator(indicators, "indicadoresDeValuation", "LPA"),
        "vpa": _indicator(indicators, "indicadoresDeValuation", "VPA"),

        # Debt
        "net_debt_equity": _indicator(indicators, "indicadoresDeEndividamento", "Dív. líquida/PL"),
        "net_debt_ebitda": _indicator(indicators, "indicadoresDeEndividamento", "Dív. líquida/EBITDA"),
        "net_debt_ebit": _indicator(indicators, "indicadoresDeEndividamento", "Dív. líquida/EBIT"),
        "current_ratio": _indicator(indicators, "indicadoresDeEndividamento", "Liq. corrente"),

        # Margins
        "gross_margin": _indicator(indicators, "indicadoresDeEficiência", "M. Bruta"),
        "ebitda_margin": _indicator(indicators, "indicadoresDeEficiência", "M. EBITDA"),
        "ebit_margin": _indicator(indicators, "indicadoresDeEficiência", "M. EBIT"),
        "net_margin": _indicator(indicators, "indicadoresDeEficiência", "M. Líquida"),

        # Profitability
        "roe": _indicator(indicators, "indicadoresDeRentabilidade", "ROE"),
        "roa": _indicator(indicators, "indicadoresDeRentabilidade", "ROA"),
        "roic": _indicator(indicators, "indicadoresDeRentabilidade", "ROIC"),

        # Growth
        "cagr_revenue_5y": _indicator(indicators, "indicadoresDeCrescimento", "CAGR Receitas 5 anos"),
        "cagr_profit_5y": _indicator(indicators, "indicadoresDeCrescimento", "CAGR Lucros 5 anos"),
    }


def cache_payload(payload: dict) -> Path:
    """Persist raw MCP payload to cache (for replay/debug)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ticker = payload["stock"]
    out = CACHE_DIR / f"{ticker}_{date.today().isoformat()}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def upsert_fundamentals(parsed: dict, market: str = "br") -> None:
    """Grava em `fundamentals` table. Usa period_end = today para snapshot current."""
    db = BR_DB if market == "br" else ROOT / "data" / "us_investments.db"
    if not db.exists():
        raise FileNotFoundError(f"DB not found: {db}")

    period_end = parsed["fetched_at"]
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO fundamentals
                (ticker, period_end, eps, bvps, roe, pe, pb, dy, net_debt_ebitda)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                parsed["ticker"],
                period_end,
                parsed.get("lpa"),
                parsed.get("vpa"),
                parsed.get("roe"),
                parsed.get("pe"),
                parsed.get("pb"),
                parsed.get("dy"),
                parsed.get("net_debt_ebitda"),
            ),
        )
        conn.commit()


def passes_graham_br(parsed: dict) -> tuple[bool, list[str]]:
    """Aplica critério BR empresas operacionais do CLAUDE.md."""
    failures = []
    dy = parsed.get("dy") or 0
    roe = parsed.get("roe") or 0
    nde = parsed.get("net_debt_ebitda")
    lpa, vpa = parsed.get("lpa") or 0, parsed.get("vpa") or 0
    price = parsed.get("price") or 0

    if dy < 6.0:
        failures.append(f"DY {dy:.2f}% < 6%")
    if roe < 15.0:
        failures.append(f"ROE {roe:.2f}% < 15%")
    if nde is not None and nde >= 3.0:
        failures.append(f"Dív liq/EBITDA {nde:.2f} >= 3")

    if lpa > 0 and vpa > 0 and price > 0:
        graham_number = (22.5 * lpa * vpa) ** 0.5
        if graham_number < price:
            failures.append(f"Graham {graham_number:.2f} < preço {price:.2f}")

    return (len(failures) == 0, failures)


def passes_graham_br_bank(parsed: dict) -> tuple[bool, list[str]]:
    """Critério BR bancos do CLAUDE.md (Graham Number + Dív/EBITDA not applicable)."""
    failures = []
    pe = parsed.get("pe") or 0
    pb = parsed.get("pb") or 0
    dy = parsed.get("dy") or 0
    roe = parsed.get("roe") or 0

    if pe > 10:
        failures.append(f"P/E {pe:.2f} > 10")
    if pb > 1.5:
        failures.append(f"P/B {pb:.2f} > 1.5")
    if dy < 6.0:
        failures.append(f"DY {dy:.2f}% < 6%")
    if roe < 12.0:
        failures.append(f"ROE {roe:.2f}% < 12%")

    return (len(failures) == 0, failures)


if __name__ == "__main__":
    print("Status Invest MCP fetcher — library, not CLI.")
    print("Call via assistant MCP orchestration or import into agents.")
    print()
    print("Example:")
    print("  >>> from fetchers.status_invest_mcp_fetcher import parse_mcp_payload, passes_graham_br")
    print("  >>> payload = {...}  # from mcp__status-invest__get-indicadores")
    print("  >>> parsed = parse_mcp_payload(payload)")
    print("  >>> ok, reasons = passes_graham_br(parsed)")
