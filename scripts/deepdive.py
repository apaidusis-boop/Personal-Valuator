"""ii deepdive — Personal Equity Valuator pipeline (Phase EE.2 / V10 blueprint).

Orquestra 4 camadas para um único ticker:

  Camada 1 — AUDITOR  (paralelo)
    - Piotroski F-Score (scoring.piotroski.compute)
    - Altman Z-Score    (scoring.altman.compute)
    - Beneish M-Score   (scoring.beneish.compute)
    - Existing screen score (scoring.engine)

  Camada 2 — SCOUT   (paralelo com Auditor)
    - Notícias, insider, short interest, consensus (yfinance live)

  Camada 3 — HISTORIAN
    - Delta vs análise anterior (mesmo ticker, scores.run_date)

  Camada 4 — STRATEGIST  (Ollama, opcional)
    - Dossier 5k+ palavras com bear/bull cases, DuPont, valuation multinível
    - Default: qwen2.5:32b (rápido). --model llama3.3:70b para dossier "elite".

Output:
  - JSON em reports/deepdive/<TICKER>_<YYYYMMDD_HHMM>.json
  - Markdown Obsidian em obsidian_vault/dossiers/<TICKER>.md  (--save-obsidian)
  - Print compacto no terminal

Uso:
    python scripts/deepdive.py PRIO3
    python scripts/deepdive.py JNJ --no-llm
    python scripts/deepdive.py ITSA4 --save-obsidian --model qwen2.5:32b-instruct-q4_K_M
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import sqlite3
import sys
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scoring import altman, piotroski, beneish, moat

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
OBSIDIAN_DIR = ROOT / "obsidian_vault" / "dossiers"
REPORTS_DIR = ROOT / "reports" / "deepdive"

DEFAULT_MODEL = "qwen2.5:32b-instruct-q4_K_M"
ELITE_MODEL = "llama3.3:70b"  # Phase EE.4 — pull when ready (~40GB)


def _autodetect_model() -> str:
    """Prefer the elite 70B model if installed; fall back to 32B chief model."""
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        names = [m.get("name", "") for m in (r.json().get("models") or [])]
        for elite in (ELITE_MODEL, "qwen2.5:72b-instruct-q4_K_M", "qwen2.5:72b"):
            if any(elite in n for n in names):
                return elite
    except Exception:
        pass
    return DEFAULT_MODEL


# ─── Auditor (3 quality scores in parallel) ───────────────────────────────

def _auditor(ticker: str, market: str | None) -> dict:
    """Run all 4 scoring modules in parallel. Returns dict ready for JSON serialization."""
    out: dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        f_p = ex.submit(piotroski.compute, ticker, market)
        f_a = ex.submit(altman.compute, ticker, market)
        f_b = ex.submit(beneish.compute, ticker, market)
        f_m = ex.submit(moat.compute, ticker, market)
        out["piotroski"] = _score_to_dict(f_p.result())
        out["altman"] = _score_to_dict(f_a.result())
        out["beneish"] = _score_to_dict(f_b.result())
        m_score = f_m.result()
        out["moat"] = _score_to_dict(m_score)
        out["moat"]["label"] = m_score.label  # @property, lost by asdict()
    return out


def _score_to_dict(score) -> dict:
    if is_dataclass(score):
        return {k: v for k, v in asdict(score).items() if v is not None and v != []}
    if hasattr(score, "__dict__"):
        return {k: v for k, v in score.__dict__.items() if not k.startswith("_") and v is not None}
    return {"raw": str(score)}


# ─── Scout (yfinance qualitative) ─────────────────────────────────────────

def _scout(ticker: str, market: str | None) -> dict:
    """News + insider + short interest + analyst consensus via yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance not available"}

    yf_ticker = ticker
    if market == "br" and "." not in ticker:
        from scoring.beneish import BR_ADR_TICKERS
        if ticker not in BR_ADR_TICKERS:
            yf_ticker = f"{ticker}.SA"

    try:
        tk = yf.Ticker(yf_ticker)
        info = tk.info or {}
    except Exception as e:
        return {"error": f"yfinance fetch: {type(e).__name__}: {e}"}

    out: dict = {}

    # News
    try:
        raw_news = (tk.news or [])[:8]
        out["news"] = []
        for item in raw_news:
            content = item.get("content", item)
            out["news"].append({
                "title": content.get("title") or item.get("title", ""),
                "published": str(content.get("pubDate") or item.get("providerPublishTime", "")),
            })
    except Exception:
        out["news"] = []

    # Short interest
    pct = info.get("shortPercentOfFloat")
    if pct is not None:
        pct_d = round(pct * 100, 2)
        if pct_d < 5:
            sig = "low"
        elif pct_d < 15:
            sig = "moderate"
        else:
            sig = "elevated"
        out["short_interest"] = {
            "shares_short": info.get("sharesShort"),
            "pct_of_float": pct_d,
            "days_to_cover": info.get("shortRatio"),
            "signal": sig,
        }

    # Insider
    out["insider"] = {
        "insider_pct": info.get("heldPercentInsiders"),
        "institution_pct": info.get("heldPercentInstitutions"),
    }
    try:
        txn = tk.insider_transactions
        if txn is not None and not txn.empty:
            shares_col = next((c for c in txn.columns if "share" in c.lower()), None)
            if shares_col:
                buys = int((txn[shares_col].fillna(0) > 0).sum())
                sells = int((txn[shares_col].fillna(0) < 0).sum())
                out["insider"]["recent_buys"] = buys
                out["insider"]["recent_sells"] = sells
                out["insider"]["signal"] = (
                    "bullish" if buys > sells else
                    "bearish" if sells > buys else "neutral"
                )
    except Exception:
        pass

    # Analyst consensus
    price = info.get("currentPrice") or info.get("previousClose") or 0
    mean = info.get("targetMeanPrice")
    if mean and price:
        upside = round((mean - price) / price * 100, 1)
    else:
        upside = None
    rec = (info.get("recommendationKey") or "n/a").upper().replace("_", " ")
    out["analyst_consensus"] = {
        "recommendation": rec,
        "num_analysts": info.get("numberOfAnalystOpinions", 0),
        "target_mean": mean,
        "target_high": info.get("targetHighPrice"),
        "target_low": info.get("targetLowPrice"),
        "current_price": price,
        "upside_pct": upside,
    }

    # Multiples + profitability + balance snapshot
    out["multiples"] = {
        "pe_trailing": info.get("trailingPE"),
        "pe_forward": info.get("forwardPE"),
        "pb": info.get("priceToBook"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "ps": info.get("priceToSalesTrailing12Months"),
        "peg": info.get("pegRatio"),
        "div_yield": (round(info.get("dividendYield", 0) * 100, 2)
                      if info.get("dividendYield") else None),
        "fcf_yield": (round(info.get("freeCashflow") / info.get("marketCap") * 100, 2)
                      if info.get("freeCashflow") and info.get("marketCap") else None),
    }
    out["profitability"] = {
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        "gross_margin": info.get("grossMargins"),
        "net_margin": info.get("profitMargins"),
    }
    out["meta"] = {
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "price": price,
    }
    return out


# ─── Historian (delta vs anterior) ────────────────────────────────────────

def _historian(ticker: str, market: str | None,
               current_audit: dict, current_scout: dict) -> str:
    """Produce delta narrative comparing today's run to most recent prior run."""
    if not market:
        return "[Historian] sem mercado detectado — sem histórico."
    db = DB_BR if market == "br" else DB_US
    try:
        with sqlite3.connect(db) as c:
            row = c.execute(
                "SELECT details_json, run_date FROM scores WHERE ticker=? "
                "ORDER BY run_date DESC LIMIT 1",
                (ticker,)
            ).fetchone()
    except sqlite3.OperationalError:
        return "[Historian] tabela scores indisponível."
    if not row:
        return f"[Historian] primeira análise registada para {ticker}."

    prev_json, prev_date = row
    try:
        prev = json.loads(prev_json) if prev_json else {}
    except Exception:
        prev = {}

    lines = [f"Delta Report — {ticker} | hoje vs run anterior ({prev_date})"]

    cur_p = (current_audit.get("piotroski") or {}).get("score")
    cur_a = (current_audit.get("altman") or {}).get("z")
    cur_b = (current_audit.get("beneish") or {}).get("m")
    cur_price = (current_scout.get("meta") or {}).get("price")

    prev_p = prev.get("piotroski_score") or prev.get("piotroski")
    prev_a = prev.get("altman_z") or prev.get("altman")
    prev_price = prev.get("price")

    def _line(label, cur, prv, fmt="{:+.2f}"):
        if cur is None or prv is None:
            return
        try:
            a = "▲" if cur > prv else "▼" if cur < prv else "→"
            lines.append(f"  {label}: {fmt.format(prv)} → {fmt.format(cur)} {a}")
        except Exception:
            pass

    _line("Piotroski", cur_p, prev_p, fmt="{:.0f}/9")
    _line("Altman Z", cur_a, prev_a, fmt="{:+.2f}")
    if cur_b is not None:
        lines.append(f"  Beneish M: {cur_b:+.2f} (novo — não comparável)")
    _line("Preço", cur_price, prev_price, fmt="{:.2f}")
    return "\n".join(lines)


# ─── Strategist (Ollama dossier) ──────────────────────────────────────────

STRATEGIST_PROMPT_HEAD = """Tu és um analista de equity sénior, 20 anos de experiência em value investing
(Graham, Buffett, Klarman, Dalio). Mandato: DESTRUIR a tese antes de aprovar.
Optimismo sem dados é proibido. Falas PT-BR.

REGRA ANTI-VIÉS: se Piotroski < 5, o Bear Case deve ter o DOBRO do tamanho do Bull Case.
REGRA DE OURO: nunca recomendar BUY se EY < taxa livre de risco local sem
justificativa de crescimento excepcional.
"""


def _strategist(audit: dict, scout: dict, delta: str, model: str) -> str:
    """Generate 5k-word dossier via Ollama. Returns markdown."""
    from agents._llm import ollama_call

    p_score = ((audit.get("piotroski") or {}).get("f_score") or (audit.get("piotroski") or {}).get("score"))
    a_z = (audit.get("altman") or {}).get("z")
    b_m = (audit.get("beneish") or {}).get("m")
    moat_obj = audit.get("moat") or {}
    moat_overall = moat_obj.get("overall")
    moat_label = moat_obj.get("label", "N/A")

    meta = scout.get("meta") or {}
    mults = scout.get("multiples") or {}
    prof = scout.get("profitability") or {}
    cons = scout.get("analyst_consensus") or {}
    short = scout.get("short_interest") or {}
    ins = scout.get("insider") or {}

    user_prompt = f"""DADOS QUANTITATIVOS — {meta.get('name')} ({meta.get('country','?')})
Setor: {meta.get('sector')} | Indústria: {meta.get('industry')}
Preço: {meta.get('price')} {meta.get('currency','')} | Market Cap: {meta.get('market_cap')}

QUALITY SCORES
  Piotroski F-Score : {p_score}/9
  Altman Z-Score    : {a_z}  ({(audit.get('altman') or {}).get('zone')})
  Beneish M-Score   : {b_m}  ({(audit.get('beneish') or {}).get('zone')})
  Moat Score        : {moat_overall}/10  ({moat_label})
    pricing_power   : {moat_obj.get('pricing_power')}/10
    capital_eff     : {moat_obj.get('capital_efficiency')}/10
    reinvest_runway : {moat_obj.get('reinvestment_runway')}/10
    scale_durability: {moat_obj.get('scale_durability')}/10

MÚLTIPLOS
  P/E TTM: {mults.get('pe_trailing')} | P/E Fwd: {mults.get('pe_forward')}
  P/B: {mults.get('pb')} | EV/EBITDA: {mults.get('ev_ebitda')}
  FCF Yield: {mults.get('fcf_yield')}% | Div Yield: {mults.get('div_yield')}%

RENTABILIDADE
  ROE: {prof.get('roe')} | ROA: {prof.get('roa')}
  Margem Líquida: {prof.get('net_margin')} | Margem Bruta: {prof.get('gross_margin')}

DADOS QUALITATIVOS (Scout)
  Insider: {ins.get('signal','n/a')} (compras: {ins.get('recent_buys')} / vendas: {ins.get('recent_sells')})
  Short interest: {short.get('signal','n/a')} ({short.get('pct_of_float','?')}% float)
  Consensus: {cons.get('recommendation','n/a')} / {cons.get('num_analysts',0)} analistas
  Upside médio: {cons.get('upside_pct','?')}%

DELTA REPORT
{delta}

ROTEIRO OBRIGATÓRIO (markdown PT-BR, ~3000 palavras):

# 1. Executive Summary
   - Rating: COMPRAR / ACUMULAR EM QUEDA / MANTER / EVITAR
   - Preço justo estimado e upside/downside %
   - Risk Score 1-10 (1=baixo, 10=altíssimo)
   - Se Beneish é RISK ou Altman DISTRESS → alerta vermelho aqui

# 2. O Negócio
   - Modelo de receita, fontes de caixa
   - Moat (Network Effect / Switching Costs / Intangibles / Cost Adv) 1-5 cada

# 3. Decomposição DuPont
   - ROE = Margem × Giro × Alavancagem
   - Identificar a alavanca dominante

# 4. Valuation Multinível
   - Graham Number se aplicável
   - DCF com 3 cenários: Bear / Base / Bull
   - EV/EBITDA vs mediana setor

# 5. Bear Case (mais agressivo se Piotroski < 5)
   - 3 maiores riscos com prob × impacto
   - Cenário de -40%: o que aconteceria?

# 6. Bull Case
   - Catalisadores específicos com prazo
   - O que precisa acontecer para o preço dobrar em 3 anos?

# 7. Classificação Lynch
   - Slow / Stalwart / Fast / Cyclical / Turnaround / Asset Play
   - 2-3 argumentos objectivos

# 8. Veredicto Final
   - Decisão com 3 critérios mensuráveis
   - Position sizing: núcleo / satélite / especulativo / evitar

Responde APENAS o markdown do dossier. Sem preâmbulo.
"""
    return ollama_call(
        user_prompt,
        system=STRATEGIST_PROMPT_HEAD,
        model=model,
        max_tokens=6000,
        temperature=0.3,
        timeout=600,
    )


# ─── Persistência ─────────────────────────────────────────────────────────

def _save_json(ticker: str, output: dict) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = REPORTS_DIR / f"{ticker}_deepdive_{ts}.json"
    path.write_text(json.dumps(output, indent=2, default=str), encoding="utf-8")
    return path


def _save_obsidian(ticker: str, output: dict) -> Path:
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    audit = output["audit"]
    scout = output["scout"]
    meta = scout.get("meta") or {}
    p = audit.get("piotroski") or {}
    a = audit.get("altman") or {}
    b = audit.get("beneish") or {}
    m = audit.get("moat") or {}
    mults = scout.get("multiples") or {}
    prof = scout.get("profitability") or {}

    fm = ["---",
          f"ticker: {ticker}",
          f"date: {date.today().isoformat()}",
          f"price: {meta.get('price')}",
          f"sector: \"{meta.get('sector','')}\"",
          f"country: \"{meta.get('country','')}\"",
          f"piotroski: {p.get('score')}",
          f"altman_z: {a.get('z')}",
          f"beneish_m: {b.get('m')}",
          f"moat_score: {m.get('overall')}",
          f"moat_label: \"{m.get('label','N/A')}\"",
          f"pe_trailing: {mults.get('pe_trailing')}",
          f"pb: {mults.get('pb')}",
          f"ev_ebitda: {mults.get('ev_ebitda')}",
          f"div_yield: {mults.get('div_yield')}",
          f"roe: {prof.get('roe')}",
          "tags: [equity, deepdive, dossier]",
          "---",
          ""]

    title = f"# [[{ticker}]] — Dossier Deepdive ({date.today().isoformat()})"
    summary_table = (
        f"| Score | Valor | Zona |\n"
        f"|---|---|---|\n"
        f"| Piotroski | {(p.get('f_score') or p.get('score','-'))}/9 | {p.get('zone','-')} |\n"
        f"| Altman Z | {a.get('z','-')} | {a.get('zone','-')} |\n"
        f"| Beneish M | {b.get('m','-')} | {b.get('zone','-')} |\n"
        f"| Moat | {m.get('overall','-')}/10 | {m.get('label','-')} |\n"
    )
    body = output.get("dossier", "*(dossier não gerado — flag --no-llm ou erro LLM)*")

    content = "\n".join(fm) + "\n".join([
        title, "",
        f"> Sector: {meta.get('sector','?')} · Country: {meta.get('country','?')} · "
        f"Price: {meta.get('price','?')} {meta.get('currency','')}",
        "",
        "## Quality Scores", "", summary_table, "",
        "## Delta Report", "", "```", output.get("delta", ""), "```", "",
        "## Strategist Dossier", "", body, "",
        "---",
        f"*Generated by `ii deepdive {ticker}` em {datetime.now().isoformat(timespec='seconds')}.*",
    ])

    path = OBSIDIAN_DIR / f"{ticker}.md"
    path.write_text(content, encoding="utf-8")
    return path


# ─── Main pipeline ────────────────────────────────────────────────────────

def deepdive(ticker: str, *, use_llm: bool = True, save_obsidian: bool = False,
             model: str = DEFAULT_MODEL, market: str | None = None) -> dict:
    """Run the full 4-layer deepdive. Returns dict + writes JSON (always) + .md (optional)."""
    ticker = ticker.upper().replace(".SA", "")
    sep = "═" * 60
    print(f"\n{sep}\n  ii deepdive — {ticker}\n  {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{sep}\n")

    # Auto-detect market if not provided
    if not market:
        from scoring.altman import _detect_market
        market = _detect_market(ticker)

    # Layer 1+2: Auditor + Scout in parallel
    print("⚡ [1+2] Auditor (3 scores) + Scout (yfinance) em paralelo…")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_aud = ex.submit(_auditor, ticker, market)
        f_sct = ex.submit(_scout, ticker, market)
        audit = f_aud.result()
        scout = f_sct.result()

    p = audit.get("piotroski", {})
    a = audit.get("altman", {})
    b = audit.get("beneish", {})
    m = audit.get("moat", {})
    print(f"  ✓ Auditor  | Piotroski: {(p.get('f_score') or p.get('score','-'))}/9 ({p.get('zone','-')}) | "
          f"Altman: {a.get('z','-')} ({a.get('zone','-')}) | "
          f"Beneish: {b.get('m','-')} ({b.get('zone','-')}) | "
          f"Moat: {m.get('overall','-')}/10 ({m.get('label','-')})")
    cons = scout.get("analyst_consensus", {})
    print(f"  ✓ Scout    | Consensus: {cons.get('recommendation','-')} "
          f"({cons.get('num_analysts',0)} analistas, upside {cons.get('upside_pct','?')}%)")

    # Layer 3: Historian
    print("\n📚 [3] Historian — delta vs run anterior…")
    delta = _historian(ticker, market, audit, scout)
    for line in delta.split("\n")[:5]:
        print(f"  {line}")

    # Layer 4: Strategist
    dossier = ""
    if use_llm:
        print(f"\n🧠 [4] Strategist via {model} — pode demorar 1-3 min…")
        dossier = _strategist(audit, scout, delta, model)
        wc = len(dossier.split())
        print(f"  ✓ Dossier {wc:,} palavras")
    else:
        dossier = "_(dossier desactivado via --no-llm)_"
        print("\n  [4] LLM desactivado — só audit+scout+delta.")

    output = {
        "ticker": ticker,
        "market": market,
        "timestamp": datetime.now().isoformat(),
        "audit": audit,
        "scout": scout,
        "delta": delta,
        "dossier": dossier,
        "model": model if use_llm else None,
    }

    json_path = _save_json(ticker, output)
    print(f"\n💾 [Output] {json_path}")
    if save_obsidian:
        md_path = _save_obsidian(ticker, output)
        print(f"📝 [Obsidian] {md_path}")

    print(f"\n{sep}\n")
    return output


# ─── CLI ──────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        description="ii deepdive — Personal Equity Valuator (V10 / Phase EE.2)"
    )
    ap.add_argument("ticker")
    ap.add_argument("--no-llm", action="store_true", help="skip strategist dossier")
    ap.add_argument("--save-obsidian", action="store_true",
                    help="write dossier to obsidian_vault/dossiers/<TICKER>.md")
    ap.add_argument("--model", default=None,
                    help=f"Ollama model. Auto: prefer {ELITE_MODEL} if installed, "
                         f"else {DEFAULT_MODEL}. Override with --model qwen2.5:32b-instruct-q4_K_M.")
    ap.add_argument("--market", choices=["br", "us"])
    args = ap.parse_args()

    try:
        model = args.model or _autodetect_model()
        deepdive(args.ticker, use_llm=not args.no_llm,
                 save_obsidian=args.save_obsidian,
                 model=model, market=args.market)
        return 0
    except KeyboardInterrupt:
        print("\nInterrompido.")
        return 130
    except Exception as e:
        print(f"\n[ERRO FATAL] {type(e).__name__}: {e}")
        import traceback; traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
