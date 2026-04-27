"""Natural-language dispatcher — interpreta perguntas livres do founder.

Pipeline:
  1. LLM (Ollama 14B) extrai `{ticker, intent, market}` em JSON.
  2. Para intents conhecidas (price, entry, panorama, triggers, brief) → rota
     determinística: corre script local + formata.
  3. Fallback (intent='unknown' ou sem match): reúne contexto do ticker (preço,
     screen, verdict, posição) e pede ao LLM para responder em PT-BR livre.

Zero tokens Claude. Tudo Ollama local.

Exemplo:
    from agents._nl_dispatch import handle
    reply = handle("qual preço de entrada de ITSA4?")
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents._llm import llm_summarise, extract_json

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
PY = sys.executable


# ─── Intent extraction ────────────────────────────────────────────────────

INTENT_SYSTEM = """Tu és um classificador de intenções para um sistema de investimentos pessoal.
Recebes uma pergunta em PT-BR sobre mercados (BR: B3 / US: NYSE/NASDAQ) e devolves JSON.

Intents possíveis:
- "price"      — utilizador pergunta preço actual de um ticker
- "entry"      — preço de compra alvo, margem de segurança, "comprar a quanto"
- "panorama"   — análise geral / resumo / "o que achas", "vale a pena"
- "verdict"    — BUY/HOLD/SELL, recomendação
- "triggers"   — alertas, sinais abertos, "quando disparar"
- "status"     — saúde dos agents, system health
- "brief"      — briefing matinal, o que aconteceu hoje
- "position"   — posição específica EM UM ticker ("minha posição em X", "quanto tenho de X", "P&L de X")
- "portfolio"  — VISÃO GERAL da carteira inteira (sem ticker mencionado: "minha carteira", "meu portfolio")
- "unknown"    — nenhuma das anteriores

IMPORTANTE: se a pergunta menciona um ticker específico E fala de posição/quantity/quanto tenho → intent="position" (NÃO "portfolio").
"portfolio" é SÓ quando o utilizador pede overview sem ticker nenhum.

Devolve APENAS um JSON válido no formato:
{"ticker": "ITSA4", "intent": "entry", "market": "br"}

Se não houver ticker, usa null. Market: "br" para tickers B3 (4-6 chars + número, ex ITSA4, BBAS3, PETR4, HGLG11), "us" para tickers NASDAQ/NYSE (ex AAPL, JNJ, MSFT), "auto" se ambíguo."""


def classify(text: str) -> dict:
    """Extract intent/ticker from free text via Ollama. Never raises."""
    prompt = f"Pergunta: {text}\n\nJSON:"
    resp = llm_summarise(
        prompt,
        system=INTENT_SYSTEM,
        prefer="ollama",
        max_tokens=120,
        temperature=0.1,
    )
    parsed = extract_json(resp) or {}
    # Normalize
    ticker = parsed.get("ticker")
    if ticker:
        ticker = str(ticker).upper().strip().replace(".SA", "")
    return {
        "ticker": ticker,
        "intent": (parsed.get("intent") or "unknown").lower(),
        "market": (parsed.get("market") or "auto").lower(),
    }


# ─── Market detection ─────────────────────────────────────────────────────

def detect_market(ticker: str) -> Optional[str]:
    """Descobre BR/US consultando DB companies. None se não existir."""
    if not ticker:
        return None
    try:
        with sqlite3.connect(DB_BR) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return "br"
        with sqlite3.connect(DB_US) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return "us"
    except Exception:
        pass
    # Heuristic fallback: tickers BR têm dígito no fim
    if re.search(r"\d$", ticker):
        return "br"
    return "us"


def _db_for(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


# ─── Context gathering ────────────────────────────────────────────────────

def gather_ticker_context(ticker: str, market: Optional[str] = None) -> dict:
    """Reúne dados chave do ticker: preço, fundamentals, screen, posição, verdict."""
    market = market or detect_market(ticker)
    ctx: dict = {"ticker": ticker, "market": market}
    if not market:
        return ctx
    db = _db_for(market)
    try:
        with sqlite3.connect(db) as c:
            # Preço + data
            row = c.execute(
                "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if row:
                ctx["price"] = row[0]
                ctx["price_date"] = row[1]
            # Fundamentals
            fcols = [r[1] for r in c.execute("PRAGMA table_info(fundamentals)")]
            frow = c.execute(
                "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if frow:
                fund = dict(zip(fcols, frow))
                ctx["fundamentals"] = {
                    k: fund.get(k)
                    for k in ("eps", "bvps", "roe", "pe", "pb", "dy", "net_debt_ebitda",
                             "dividend_streak_years", "is_aristocrat", "pe_forward")
                    if fund.get(k) is not None
                }
            # Scoring
            srow = c.execute(
                "SELECT score, passes_screen, details_json, run_date FROM scores "
                "WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            if srow:
                try:
                    details = json.loads(srow[2]) if srow[2] else {}
                except Exception:
                    details = {}
                ctx["screen"] = {
                    "score": srow[0],
                    "passes": bool(srow[1]),
                    "run_date": srow[3],
                    "details": details,
                }
            # Posição actual
            try:
                prow = c.execute(
                    "SELECT quantity, entry_price, entry_date FROM portfolio_positions "
                    "WHERE ticker=? AND active=1",
                    (ticker,),
                ).fetchone()
                if prow:
                    ctx["position"] = {
                        "quantity": prow[0],
                        "entry_price": prow[1],
                        "entry_date": prow[2],
                    }
            except sqlite3.OperationalError:
                pass
            # Graham Number como proxy de preço-alvo de entrada (BR)
            if market == "br" and ctx.get("fundamentals"):
                eps = ctx["fundamentals"].get("eps")
                bvps = ctx["fundamentals"].get("bvps")
                if eps and bvps and eps > 0 and bvps > 0:
                    import math
                    ctx["graham_number"] = round(math.sqrt(22.5 * eps * bvps), 2)
            # Company name + sector
            try:
                cr = c.execute(
                    "SELECT name, sector, is_holding FROM companies WHERE ticker=?",
                    (ticker,),
                ).fetchone()
                if cr:
                    ctx["name"] = cr[0]
                    ctx["sector"] = cr[1]
                    ctx["is_holding"] = bool(cr[2])
            except sqlite3.OperationalError:
                pass
    except Exception as e:
        ctx["_error"] = str(e)
    return ctx


def _format_context_md(ctx: dict) -> str:
    """Renderiza contexto em markdown conciso para o LLM (ou resposta directa)."""
    lines = []
    name = ctx.get("name") or ctx.get("ticker")
    sector = ctx.get("sector") or "-"
    market = (ctx.get("market") or "?").upper()
    cur = "R$" if ctx.get("market") == "br" else "US$"
    lines.append(f"**{ctx.get('ticker')}** — {name} · {sector} · {market}")
    if ctx.get("price") is not None:
        lines.append(f"Preço: {cur}{ctx['price']:.2f} ({ctx.get('price_date')})")
    if f := ctx.get("fundamentals"):
        parts = []
        if f.get("pe"): parts.append(f"P/E {f['pe']:.1f}")
        if f.get("pb"): parts.append(f"P/B {f['pb']:.2f}")
        if f.get("dy"): parts.append(f"DY {f['dy']*100:.1f}%")
        if f.get("roe"): parts.append(f"ROE {f['roe']*100:.1f}%")
        if f.get("dividend_streak_years"): parts.append(f"Streak {f['dividend_streak_years']}y")
        if parts:
            lines.append("Fundamentals: " + " · ".join(parts))
    if ctx.get("graham_number"):
        lines.append(f"Graham Number (preço-alvo Graham): {cur}{ctx['graham_number']:.2f}")
    if s := ctx.get("screen"):
        verdict = "✓ passa" if s["passes"] else "✗ falha"
        lines.append(f"Screen: {verdict} (score {s['score']:.2f}, {s['run_date']})")
        for k, v in (s.get("details") or {}).items():
            if isinstance(v, dict):
                val = v.get("value")
                ver = v.get("verdict")
                if val is not None and ver:
                    lines.append(f"  · {k}: {val} → {ver}")
    if p := ctx.get("position"):
        lines.append(f"Posição: {p['quantity']} @ {cur}{p['entry_price']:.2f} (desde {p['entry_date']})")
        if ctx.get("price"):
            pnl = (ctx["price"] / p["entry_price"] - 1) * 100
            lines.append(f"P&L não-realizado: {pnl:+.1f}%")
    elif ctx.get("is_holding") is False:
        lines.append("Posição: (watchlist, sem posição)")
    return "\n".join(lines)


# ─── Intent handlers ──────────────────────────────────────────────────────

# ─── Telegram-first formatters ────────────────────────────────────────────

_DIV = "━━━━━━━━━━━━━━━━━━━"
_ACTION_ICON = {
    "BUY": "🟢", "ADD": "🟢", "WATCH": "🟡",
    "HOLD": "🟠", "SELL": "🔴", "AVOID": "⛔", "SKIP": "⚪",
}


def _bar(score: float, width: int = 10) -> str:
    filled = max(0, min(width, int(round(score / 10 * width))))
    return "▓" * filled + "░" * (width - filled)


def _br_date(iso: str) -> str:
    """2026-04-24 → 24/04"""
    try:
        return f"{iso[8:10]}/{iso[5:7]}"
    except Exception:
        return iso or ""


def _format_verdict_telegram(v, ctx: dict) -> str:
    """Renderiza um Verdict como bloco Telegram compacto e legível."""
    cur = "R$" if v.market == "br" else "US$"
    name = ctx.get("name") or v.ticker
    sector = ctx.get("sector")
    header_tail = f" · {name}" + (f" ({sector})" if sector else "")
    icon = _ACTION_ICON.get(v.action, "·")

    lines = [f"📊 *{v.ticker}*{header_tail}", _DIV]

    price = ctx.get("price")
    if price is not None:
        lines.append(f"💰 *{cur}{price:.2f}*  _{_br_date(ctx.get('price_date',''))}_")
    lines.append(f"{icon} *{v.action}*  ·  {v.total_score:.1f}/10  _(conf {v.confidence_pct}%)_")
    lines.append("")

    lines.append(f"`Quality    {_bar(v.quality_score)}  {v.quality_score:.1f}`")
    lines.append(f"`Valuation  {_bar(v.valuation_score)}  {v.valuation_score:.1f}`")
    lines.append(f"`Momentum   {_bar(v.momentum_score)}  {v.momentum_score:.1f}`")
    lines.append(f"`Narrativa  {_bar(v.narrative_score)}  {v.narrative_score:.1f}`")

    if v.reasons:
        lines.append("")
        lines.append("⚠ *Razões*")
        for r in v.reasons[:4]:
            lines.append(f"• {r}")

    # Momentum stats (1d / 30d / YTD)
    mom = v.momentum_detail or {}
    m_parts = []
    if (c1 := mom.get("change_1d_pct")) is not None:
        m_parts.append(f"1d {c1:+.1f}%")
    if (c30 := mom.get("change_30d_pct")) is not None:
        m_parts.append(f"30d {c30:+.1f}%")
    if (cytd := mom.get("ytd_pct")) is not None:
        m_parts.append(f"YTD {cytd:+.1f}%")
    if m_parts:
        lines.append("")
        lines.append("📈 " + " · ".join(m_parts))

    # Posição / watchlist
    p = ctx.get("position")
    if p:
        pnl = (price / p["entry_price"] - 1) * 100 if price else 0
        pnl_icon = "🟢" if pnl > 0 else ("🔴" if pnl < 0 else "·")
        lines.append(f"📍 Posição: {p['quantity']} @ {cur}{p['entry_price']:.2f}  {pnl_icon} {pnl:+.1f}%")
    elif ctx.get("is_holding") is False:
        lines.append("📍 Watchlist (sem posição)")

    return "\n".join(lines)


def _reply_price(ticker: str, market: str) -> str:
    ctx = gather_ticker_context(ticker, market)
    if not ctx.get("price"):
        return f"Sem preço para {ticker} na DB."
    cur = "R$" if market == "br" else "US$"
    name = ctx.get("name") or ticker
    lines = [
        f"💰 *{ticker}* · {name}",
        _DIV,
        f"*{cur}{ctx['price']:.2f}*  _{_br_date(ctx.get('price_date',''))}_",
    ]
    if p := ctx.get("position"):
        pnl = (ctx["price"] / p["entry_price"] - 1) * 100
        pnl_icon = "🟢" if pnl > 0 else ("🔴" if pnl < 0 else "·")
        lines.append(f"📍 {p['quantity']} @ {cur}{p['entry_price']:.2f}  {pnl_icon} *{pnl:+.1f}%*")
    return "\n".join(lines)


def _reply_entry(ticker: str, market: str) -> str:
    """Preço de entrada alvo — Graham + screen + triggers + posição actual."""
    ctx = gather_ticker_context(ticker, market)
    if not ctx.get("ticker") or not ctx.get("price"):
        return f"Sem dados para {ticker}."
    cur = "R$" if market == "br" else "US$"
    price = ctx["price"]
    name = ctx.get("name") or ticker
    lines = [
        f"🎯 *{ticker}* · preço de entrada",
        _DIV,
        f"Actual: *{cur}{price:.2f}*  _{_br_date(ctx.get('price_date',''))}_",
    ]
    graham = ctx.get("graham_number")
    if graham:
        margin = (graham / price - 1) * 100
        icon = "🟢" if price <= graham else "🔴"
        status = "compra" if price <= graham else "caro"
        lines.append(f"Alvo Graham: {cur}{graham:.2f}  {icon} {margin:+.1f}% ({status})")

    s = ctx.get("screen") or {}
    if s:
        icon = "🟢" if s.get("passes") else "🔴"
        lines.append(f"Screen: {icon} {'passa' if s.get('passes') else 'falha'}  _(score {s.get('score',0):.2f})_")

    # Triggers
    db = _db_for(market)
    try:
        with sqlite3.connect(db) as c:
            trows = c.execute(
                "SELECT kind, payload_json FROM watchlist_actions "
                "WHERE ticker=? AND status='open' ORDER BY created_at DESC LIMIT 3",
                (ticker,),
            ).fetchall()
            if trows:
                lines.append("")
                lines.append("🔔 *Triggers abertos*")
                for kind, pj in trows:
                    try:
                        pl = json.loads(pj) if pj else {}
                    except Exception:
                        pl = {}
                    desc = pl.get("description") or pl.get("threshold") or str(pl)[:60]
                    lines.append(f"• {kind}: {desc}")
    except sqlite3.OperationalError:
        pass

    p = ctx.get("position")
    if p:
        pnl = (price / p["entry_price"] - 1) * 100
        pnl_icon = "🟢" if pnl > 0 else ("🔴" if pnl < 0 else "·")
        lines.append("")
        lines.append(f"📍 *Minha posição*: {p['quantity']} @ {cur}{p['entry_price']:.2f}  {pnl_icon} {pnl:+.1f}%")
    elif ctx.get("is_holding") is False:
        lines.append("")
        lines.append("📍 Watchlist (sem posição)")

    return "\n".join(lines)


def _run_script(script: str, args: list[str], timeout: int = 120) -> str:
    try:
        r = subprocess.run(
            [PY, "-X", "utf8", str(ROOT / script), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace", cwd=str(ROOT),
        )
        return (r.stdout or "").strip()
    except Exception as e:
        return f"(erro: {type(e).__name__}: {e})"


def _reply_verdict(ticker: str, market: str) -> str:
    """Verdict compacto Telegram — importa compute_verdict directamente."""
    try:
        from scripts.verdict import compute_verdict
        v = compute_verdict(ticker)
    except Exception as e:
        return f"⚠ Verdict falhou para {ticker}: {type(e).__name__}: {e}"
    ctx = gather_ticker_context(ticker, v.market)
    return _format_verdict_telegram(v, ctx)


def _reply_panorama(ticker: str, market: str) -> str:
    """Panorama = Verdict + triggers + posição — tudo compacto."""
    return _reply_verdict(ticker, market)


def _reply_triggers(ticker: Optional[str]) -> str:
    args = ["list"]
    if ticker:
        args += ["--ticker", ticker]
    out = _run_script("scripts/action_cli.py", args, timeout=30)
    return f"🔔 *Triggers abertos*\n\n```\n{out[:3500]}\n```" if out else "Sem triggers abertos."


def _reply_brief() -> str:
    path = ROOT / "obsidian_vault" / "dashboards" / "Briefing.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        return f"☀️ *Briefing* (último gerado)\n\n{text[:3500]}"
    return "Sem briefing recente. Corre `/run morning_briefing`."


def _reply_position(ticker: str, market: str) -> str:
    """Posição individual num ticker: qty, avg cost, P&L, proventos 12m, YoC."""
    ctx = gather_ticker_context(ticker, market)
    if not ctx.get("ticker"):
        return f"Não conheço {ticker}."
    cur = "R$" if market == "br" else "US$"
    name = ctx.get("name") or ticker
    price = ctx.get("price")
    p = ctx.get("position")

    if not p:
        lines = [
            f"📍 *{ticker}* · {name}",
            _DIV,
            "_Sem posição activa (watchlist)._",
        ]
        if price:
            lines.append(f"Preço actual: {cur}{price:.2f}  _{_br_date(ctx.get('price_date',''))}_")
        return "\n".join(lines)

    qty = p["quantity"]
    entry = p["entry_price"]
    cost_total = qty * entry
    mkt_value = qty * price if price else 0
    pnl_pct = (price / entry - 1) * 100 if price else 0
    pnl_abs = mkt_value - cost_total
    pnl_icon = "🟢" if pnl_pct > 0 else ("🔴" if pnl_pct < 0 else "·")

    lines = [
        f"📍 *{ticker}* · {name}",
        _DIV,
        f"Preço: *{cur}{price:.2f}*  _{_br_date(ctx.get('price_date',''))}_" if price else "Sem preço",
        f"Quantidade: *{qty:g}* @ {cur}{entry:.2f}",
        f"Valor investido: {cur}{cost_total:,.2f}",
    ]
    if price:
        lines.append(f"Valor de mercado: *{cur}{mkt_value:,.2f}*")
        lines.append(f"P&L: {pnl_icon} *{cur}{pnl_abs:+,.2f}*  ({pnl_pct:+.1f}%)")
    lines.append(f"Entry date: _{p.get('entry_date') or '?'}_")

    # Dividendos últimos 12m × quantity → YoC
    db = _db_for(market)
    try:
        with sqlite3.connect(db) as c:
            from datetime import date, timedelta
            cutoff = (date.today() - timedelta(days=365)).isoformat()
            row = c.execute(
                "SELECT SUM(amount), COUNT(*) FROM dividends "
                "WHERE ticker=? AND ex_date >= ?",
                (ticker, cutoff),
            ).fetchone()
            div_per_share_12m = row[0] if row and row[0] else 0
            n_div = row[1] if row else 0
            if div_per_share_12m > 0:
                div_received = div_per_share_12m * qty
                yoc = (div_per_share_12m / entry) * 100 if entry > 0 else 0
                lines.append("")
                lines.append(f"💸 Proventos 12m: *{cur}{div_received:,.2f}*  ({n_div} pagamentos)")
                lines.append(f"Yield on Cost: *{yoc:.2f}%*")
    except Exception:
        pass

    # Verdict action rápido
    try:
        from scripts.verdict import compute_verdict
        v = compute_verdict(ticker)
        icon = _ACTION_ICON.get(v.action, "·")
        lines.append("")
        lines.append(f"{icon} Verdict: *{v.action}*  ·  {v.total_score:.1f}/10")
    except Exception:
        pass

    return "\n".join(lines)


def _reply_portfolio() -> str:
    lines = ["💼 *Portfolio*", ""]
    for mkt, db in (("BR", DB_BR), ("US", DB_US)):
        try:
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    "SELECT ticker, quantity, entry_price FROM portfolio_positions "
                    "WHERE active=1 ORDER BY ticker"
                ).fetchall()
                if rows:
                    lines.append(f"*{mkt}*")
                    for t, q, ep in rows:
                        lines.append(f"  {t}: {q} @ {ep:.2f}")
                    lines.append("")
        except sqlite3.OperationalError:
            pass
    return "\n".join(lines)


def _reply_free(text: str, ticker: Optional[str], market: Optional[str]) -> str:
    """Última linha de defesa: LLM responde livre com contexto (se tiver ticker)."""
    context = ""
    if ticker:
        ctx = gather_ticker_context(ticker, market)
        context = _format_context_md(ctx)
    system = (
        "Tu és o Jarbas, assistente pessoal de investimentos. Respondes em PT-BR, "
        "conciso (max 250 palavras), factual, sem inventar números. Se não tens "
        "dados, dizes 'sem dados' em vez de especular. Usa Markdown simples."
    )
    prompt = (
        f"Contexto actual do sistema:\n{context}\n\n"
        f"Pergunta do founder: {text}\n\n"
        f"Resposta (max 250 palavras, factual):"
    ) if context else (
        f"Pergunta do founder: {text}\n\n"
        f"Nota: não identifiquei ticker na pergunta. Responde no geral, "
        f"ou pede clarificação se precisa de ticker.\n\n"
        f"Resposta:"
    )
    reply = llm_summarise(prompt, system=system, prefer="ollama", max_tokens=500, temperature=0.3)
    return reply or "Sem resposta do LLM local."


# ─── Public entry point ──────────────────────────────────────────────────

def handle(text: str) -> str:
    """Processa texto livre e devolve resposta pronta para Telegram."""
    text = (text or "").strip()
    if not text:
        return "Pergunta vazia."
    intent_obj = classify(text)
    ticker = intent_obj.get("ticker")
    intent = intent_obj.get("intent")
    market = intent_obj.get("market") or "auto"
    if market == "auto" and ticker:
        market = detect_market(ticker) or "us"

    try:
        if intent == "price" and ticker:
            return _reply_price(ticker, market)
        if intent == "entry" and ticker:
            return _reply_entry(ticker, market)
        if intent == "verdict" and ticker:
            return _reply_verdict(ticker, market)
        if intent == "panorama" and ticker:
            return _reply_panorama(ticker, market)
        if intent == "triggers":
            return _reply_triggers(ticker)
        if intent == "brief":
            return _reply_brief()
        if intent == "position" and ticker:
            return _reply_position(ticker, market)
        if intent == "portfolio":
            # Se tem ticker, user quer SÓ essa posição, não carteira toda.
            if ticker:
                return _reply_position(ticker, market)
            return _reply_portfolio()
        # fallback
        return _reply_free(text, ticker, market)
    except Exception as e:
        return f"❌ erro ao processar: {type(e).__name__}: {e}"


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "qual preço de entrada de ITSA4?"
    print(handle(q))
