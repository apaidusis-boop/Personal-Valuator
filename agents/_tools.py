"""Tool registry for Antonio Carlos (Chief of Staff).

Each tool is a small function: receives kwargs from the LLM, returns a JSON-
serializable dict. Tools wrap existing scripts/agents — direct imports where
fast and clean, subprocess where the script's own argparse plumbing is
worth reusing.

Design:
- Tools are intentionally thin. They never print, never write to vault, never
  mutate DB (read-only by default). Side effects go in tools prefixed `do_`.
- Schemas use OpenAI/Ollama function-calling JSON schema format.
- All tools tolerant: on failure return `{"error": "<msg>"}` so the model can
  decide to retry, fall back, or surface to the user.
"""
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
PY = sys.executable


def _db_for(market: str) -> Path:
    return DB_BR if (market or "").lower() == "br" else DB_US


def _detect_market(ticker: str) -> str:
    """Cheap market detection: query both DBs."""
    if not ticker:
        return "us"
    t = ticker.upper().replace(".SA", "")
    for market, db in (("br", DB_BR), ("us", DB_US)):
        try:
            with sqlite3.connect(db) as c:
                if c.execute("SELECT 1 FROM companies WHERE ticker=?", (t,)).fetchone():
                    return market
        except sqlite3.OperationalError:
            pass
    # Heuristic: BR tickers end in digit
    return "br" if t and t[-1].isdigit() else "us"


def _run_script(script: str, args: list[str], timeout: int = 90) -> str:
    try:
        r = subprocess.run(
            [PY, "-X", "utf8", str(ROOT / script), *args],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace", cwd=str(ROOT),
        )
        return (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return f"(timeout: {script} after {timeout}s)"
    except Exception as e:
        return f"(error: {type(e).__name__}: {e})"


# ─── Tool implementations ─────────────────────────────────────────────────

def get_ticker_verdict(ticker: str) -> dict:
    """Compute aggregate buy/hold/sell verdict with score breakdown."""
    try:
        from scripts.verdict import compute_verdict
        v = compute_verdict(ticker.upper().replace(".SA", ""))
        return {
            "ticker": v.ticker,
            "market": v.market,
            "action": v.action,
            "total_score": round(v.total_score, 2),
            "confidence_pct": v.confidence_pct,
            "scores": {
                "quality": round(v.quality_score, 2),
                "valuation": round(v.valuation_score, 2),
                "momentum": round(v.momentum_score, 2),
                "narrative": round(v.narrative_score, 2),
            },
            "reasons": v.reasons[:5],
            "momentum_detail": v.momentum_detail,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def get_ticker_position(ticker: str) -> dict:
    """Current position, P&L, dividends 12m, yield-on-cost."""
    t = ticker.upper().replace(".SA", "")
    market = _detect_market(t)
    db = _db_for(market)
    try:
        with sqlite3.connect(db) as c:
            cur = c.cursor()
            cr = cur.execute(
                "SELECT name, sector, is_holding FROM companies WHERE ticker=?", (t,)
            ).fetchone()
            if not cr:
                return {"error": f"ticker {t} not found"}
            name, sector, is_holding = cr
            price_row = cur.execute(
                "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (t,)
            ).fetchone()
            price, price_date = (price_row or (None, None))
            pos_row = cur.execute(
                "SELECT quantity, entry_price, entry_date FROM portfolio_positions "
                "WHERE ticker=? AND active=1", (t,)
            ).fetchone()
            divs_12m = 0.0
            n_pay = 0
            cutoff = (date.today() - timedelta(days=365)).isoformat()
            try:
                drow = cur.execute(
                    "SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM dividends "
                    "WHERE ticker=? AND ex_date >= ?", (t, cutoff)
                ).fetchone()
                divs_12m, n_pay = drow or (0.0, 0)
            except sqlite3.OperationalError:
                pass

        out: dict[str, Any] = {
            "ticker": t, "name": name, "sector": sector, "market": market,
            "price": price, "price_date": price_date,
            "is_holding": bool(is_holding),
        }
        if pos_row:
            qty, entry, edate = pos_row
            out["position"] = {
                "quantity": qty,
                "entry_price": entry,
                "entry_date": edate,
                "cost_total": round(qty * entry, 2),
                "market_value": round(qty * price, 2) if price else None,
                "pnl_pct": round((price/entry - 1) * 100, 2) if price and entry else None,
                "pnl_abs": round(qty * (price - entry), 2) if price else None,
            }
            if divs_12m and entry:
                out["position"]["dividends_12m_per_share"] = round(divs_12m, 4)
                out["position"]["dividends_12m_total"] = round(divs_12m * qty, 2)
                out["position"]["yield_on_cost_pct"] = round((divs_12m / entry) * 100, 2)
                out["position"]["payments_12m"] = n_pay
        else:
            out["position"] = None
        return out
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def list_portfolio(market: str = "all") -> dict:
    """List active positions in BR, US, or both. Includes total cost basis."""
    out: dict = {"br": [], "us": [], "totals": {}}
    targets = (("br", DB_BR), ("us", DB_US)) if market == "all" else \
              ((market.lower(), _db_for(market)),)
    for mkt, db in targets:
        try:
            with sqlite3.connect(db) as c:
                rows = c.execute(
                    "SELECT pp.ticker, pp.quantity, pp.entry_price, "
                    "  (SELECT close FROM prices WHERE ticker=pp.ticker ORDER BY date DESC LIMIT 1) AS px, "
                    "  c.name, c.sector "
                    "FROM portfolio_positions pp LEFT JOIN companies c ON c.ticker=pp.ticker "
                    "WHERE pp.active=1 ORDER BY pp.ticker"
                ).fetchall()
            cost = 0.0
            mv = 0.0
            for tk, q, ep, px, name, sector in rows:
                cost += q * ep
                if px:
                    mv += q * px
                out[mkt].append({
                    "ticker": tk, "name": name, "sector": sector,
                    "quantity": q, "entry_price": ep, "price": px,
                    "cost": round(q * ep, 2),
                    "market_value": round(q * px, 2) if px else None,
                    "pnl_pct": round((px/ep - 1) * 100, 2) if px and ep else None,
                })
            out["totals"][mkt] = {
                "n_positions": len(rows),
                "cost": round(cost, 2),
                "market_value": round(mv, 2) if mv else None,
                "pnl_abs": round(mv - cost, 2) if mv else None,
                "pnl_pct": round((mv/cost - 1) * 100, 2) if cost and mv else None,
            }
        except sqlite3.OperationalError as e:
            out["totals"][mkt] = {"error": str(e)}
    return out


def get_macro_regime(market: str = "br") -> dict:
    """Current macro regime (rate cycle, inflation, growth) for BR or US."""
    try:
        from analytics.regime import classify
        r = classify(market.lower())
        from dataclasses import asdict, is_dataclass
        if is_dataclass(r):
            return {"market": market.lower(), **asdict(r)}
        if hasattr(r, "__dict__"):
            return {"market": market.lower(),
                    **{k: v for k, v in r.__dict__.items() if not k.startswith("_")}}
        return {"market": market.lower(), "regime": str(r)}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def query_sql(market: str, sql: str) -> dict:
    """Read-only SELECT query against br/us DB. Auto-LIMIT 50 rows."""
    sql_clean = sql.strip().rstrip(";")
    if not sql_clean.lower().startswith("select"):
        return {"error": "only SELECT statements allowed"}
    forbidden = ["insert", "update", "delete", "drop", "alter", "attach", "pragma write"]
    if any(f in sql_clean.lower() for f in forbidden):
        return {"error": "modifying statements not allowed"}
    if "limit" not in sql_clean.lower():
        sql_clean += " LIMIT 50"
    db = _db_for(market)
    try:
        with sqlite3.connect(db) as c:
            cur = c.execute(sql_clean)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        return {
            "market": market.lower(),
            "rows_returned": len(rows),
            "columns": cols,
            "rows": [dict(zip(cols, r)) for r in rows[:50]],
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def list_open_triggers(ticker: str | None = None) -> dict:
    """Open watchlist actions / triggers. Optionally filter by ticker."""
    out: dict = {"br": [], "us": []}
    for mkt, db in (("br", DB_BR), ("us", DB_US)):
        try:
            with sqlite3.connect(db) as c:
                if ticker:
                    rows = c.execute(
                        "SELECT id, ticker, kind, payload_json, created_at FROM watchlist_actions "
                        "WHERE status='open' AND ticker=? ORDER BY created_at DESC LIMIT 20",
                        (ticker.upper().replace(".SA", ""),)
                    ).fetchall()
                else:
                    rows = c.execute(
                        "SELECT id, ticker, kind, payload_json, created_at FROM watchlist_actions "
                        "WHERE status='open' ORDER BY created_at DESC LIMIT 20"
                    ).fetchall()
            for rid, tk, kind, pj, ts in rows:
                try:
                    pl = json.loads(pj) if pj else {}
                except Exception:
                    pl = {}
                out[mkt].append({
                    "id": rid, "ticker": tk, "kind": kind,
                    "description": pl.get("description") or pl.get("threshold") or str(pl)[:80],
                    "created_at": ts,
                })
        except sqlite3.OperationalError:
            pass
    return out


def get_perpetuum_status() -> dict:
    """Health snapshot of all agents/perpetuums."""
    sd = ROOT / "data" / "agents"
    if not sd.exists():
        return {"error": "no agents state dir"}
    out: dict = {"agents": []}
    for f in sorted(sd.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
            out["agents"].append({
                "name": s.get("agent") or f.stem,
                "last_status": s.get("last_status"),
                "last_run": s.get("last_run"),
                "consecutive_failures": s.get("consecutive_failures", 0),
                "run_count": s.get("run_count", 0),
            })
        except Exception:
            continue
    return out


def get_briefing() -> dict:
    """Latest morning briefing markdown content."""
    p = ROOT / "obsidian_vault" / "dashboards" / "Briefing.md"
    if not p.exists():
        return {"error": "no briefing yet — run morning_briefing"}
    text = p.read_text(encoding="utf-8")
    return {"markdown": text[:5000], "path": str(p), "length": len(text)}


def get_synthetic_ic(ticker: str) -> dict:
    """5-persona Investment Committee debate (Buffett/Druck/Taleb/Klarman/Dalio)."""
    out = _run_script("agents/synthetic_ic.py", [ticker.upper()], timeout=240)
    return {"ticker": ticker.upper(), "output": out[:3000]}


def get_variant_perception(ticker: str) -> dict:
    """Our view vs analyst consensus — variant perception."""
    out = _run_script("-m agents.variant_perception".split(), [ticker.upper()], timeout=120)
    if not out or "error" in out.lower()[:200]:
        try:
            r = subprocess.run(
                [PY, "-m", "agents.variant_perception", ticker.upper()],
                capture_output=True, text=True, timeout=120,
                cwd=str(ROOT), encoding="utf-8", errors="replace",
            )
            out = (r.stdout or "").strip()
        except Exception as e:
            out = f"(error: {e})"
    return {"ticker": ticker.upper(), "output": out[:3000]}


def get_drip_projection(ticker: str, horizons: str = "5,10,15") -> dict:
    """Dividend reinvestment projection for ticker over multiple horizons."""
    out = _run_script("scripts/drip_projection.py",
                      ["--ticker", ticker.upper(), "--horizons", horizons], timeout=60)
    return {"ticker": ticker.upper(), "horizons": horizons, "output": out[:2500]}


def compare_tickers_tool(tickers: str, vs: str = "SPY") -> dict:
    """Compare multiple tickers side-by-side. tickers = 'JNJ,PG,KO'."""
    tk_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    args = tk_list + ["--vs", vs]
    out = _run_script("scripts/compare_tickers.py", args, timeout=90)
    return {"tickers": tk_list, "benchmark": vs, "output": out[:3000]}


def web_research(topic: str, ticker: str | None = None) -> dict:
    """Web research via Tavily (cached, 7d). Returns synthesized answer."""
    try:
        from agents.autoresearch import research_topic
        result = research_topic(topic, ticker=ticker)
        if isinstance(result, dict):
            return {
                "topic": topic, "ticker": ticker,
                "answer": (result.get("answer") or "")[:2500],
                "sources": [s.get("url") for s in (result.get("sources") or [])[:5]],
            }
        return {"topic": topic, "answer": str(result)[:2500]}
    except ImportError:
        return {"error": "autoresearch not available"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def get_dividend_calendar(ticker: str | None = None, days: int = 30) -> dict:
    """Upcoming ex-dividend dates within N days."""
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    today = date.today().isoformat()
    out: dict = {"br": [], "us": []}
    for mkt, db in (("br", DB_BR), ("us", DB_US)):
        try:
            with sqlite3.connect(db) as c:
                if ticker:
                    rows = c.execute(
                        "SELECT ticker, ex_date, amount FROM dividends "
                        "WHERE ticker=? AND ex_date BETWEEN ? AND ? "
                        "ORDER BY ex_date", (ticker.upper(), today, cutoff)
                    ).fetchall()
                else:
                    rows = c.execute(
                        "SELECT ticker, ex_date, amount FROM dividends "
                        "WHERE ex_date BETWEEN ? AND ? "
                        "ORDER BY ex_date LIMIT 30", (today, cutoff)
                    ).fetchall()
            for tk, ed, amt in rows:
                out[mkt].append({"ticker": tk, "ex_date": ed, "amount": amt})
        except sqlite3.OperationalError:
            pass
    return out


def get_ticker_deepdive(ticker: str, with_dossier: bool = False) -> dict:
    """Run the full deepdive (Piotroski + Altman + Beneish + Scout + optional
    Strategist dossier). Slow (3+ min with dossier). Returns structured summary."""
    args = [ticker.upper()]
    if not with_dossier:
        args.append("--no-llm")
    out = _run_script("scripts/deepdive.py", args, timeout=420 if with_dossier else 90)
    # Read latest JSON written
    try:
        json_dir = ROOT / "reports" / "deepdive"
        if json_dir.exists():
            latest = max(json_dir.glob(f"{ticker.upper()}_deepdive_*.json"),
                         key=lambda p: p.stat().st_mtime, default=None)
            if latest:
                data = json.loads(latest.read_text(encoding="utf-8"))
                # Trim dossier if present (very large)
                if data.get("dossier") and len(data["dossier"]) > 1500:
                    data["dossier_excerpt"] = data["dossier"][:1500] + "…[truncated]"
                    data["dossier_full_path"] = str(latest)
                    del data["dossier"]
                # Trim scout news
                if (data.get("scout") or {}).get("news"):
                    data["scout"]["news"] = data["scout"]["news"][:3]
                return data
    except Exception:
        pass
    return {"ticker": ticker.upper(), "output": out[:2500],
            "note": "JSON not parsed — see stdout"}


def add_note(ticker: str, text: str, tags: str = "") -> dict:
    """Append a note for a ticker. Persisted to vault + DB. Side-effect tool."""
    args = ["add", ticker.upper(), text]
    if tags:
        args += ["--tags", tags]
    out = _run_script("scripts/notes_cli.py", args, timeout=30)
    return {"ticker": ticker.upper(), "note": text[:200], "result": out[:500]}


# ─── Tool registry ────────────────────────────────────────────────────────

TOOLS: dict[str, Callable] = {
    "get_ticker_verdict":      get_ticker_verdict,
    "get_ticker_deepdive":     get_ticker_deepdive,
    "get_ticker_position":     get_ticker_position,
    "list_portfolio":          list_portfolio,
    "get_macro_regime":        get_macro_regime,
    "query_sql":               query_sql,
    "list_open_triggers":      list_open_triggers,
    "get_perpetuum_status":    get_perpetuum_status,
    "get_briefing":            get_briefing,
    "get_synthetic_ic":        get_synthetic_ic,
    "get_variant_perception":  get_variant_perception,
    "get_drip_projection":     get_drip_projection,
    "compare_tickers":         compare_tickers_tool,
    "web_research":            web_research,
    "get_dividend_calendar":   get_dividend_calendar,
    "add_note":                add_note,
}


def tool_schemas() -> list[dict]:
    """OpenAI/Ollama function-calling schemas for all registered tools."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_ticker_verdict",
                "description": (
                    "Aggregate buy/hold/sell/watch verdict for a ticker — combines quality "
                    "(Altman+Piotroski+DivSafety), valuation (screen+DY pct), momentum (1d/30d/YTD), "
                    "and narrative scores. Use for 'o que fazer com X', 'comprar X?', 'vale a pena X'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string", "description": "Ticker (e.g. ITSA4, AAPL)"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_ticker_deepdive",
                "description": (
                    "ELITE deep-dive analysis: Piotroski F-Score + Altman Z + Beneish M + "
                    "yfinance scout (insider/short/consensus/news) + optional 5k-word LLM dossier. "
                    "SLOW (~90s without dossier, ~3-5min with). Use only when user asks for "
                    "'análise profunda', 'dossier', 'deepdive', 'avaliação completa'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "with_dossier": {
                            "type": "boolean", "default": False,
                            "description": "True = also generate the 5k-word strategist dossier (slow)."
                        },
                    },
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_ticker_position",
                "description": (
                    "Current portfolio position in a single ticker: quantity, entry price, P&L, "
                    "dividends paid 12m, yield-on-cost. Use for 'minha posição em X', 'quanto tenho de X'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_portfolio",
                "description": (
                    "List ALL active positions across BR/US with totals. Use for 'minha carteira', "
                    "'meu portfolio', 'quanto tenho investido'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"market": {"type": "string", "enum": ["br", "us", "all"], "default": "all"}},
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_macro_regime",
                "description": (
                    "Current macro regime classification (rate cycle, inflation, growth) for BR or US. "
                    "Use for 'em que regime estamos', 'macro BR', 'Fed vai cortar', 'risk-on?'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"market": {"type": "string", "enum": ["br", "us"], "default": "br"}},
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "query_sql",
                "description": (
                    "Read-only SELECT against the BR or US SQLite DB. Tables include companies, prices, "
                    "fundamentals, scores, dividends, portfolio_positions, watchlist_actions, "
                    "thesis_health, quarterly_history, events. Use only when other tools don't fit. "
                    "Always include LIMIT."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "market": {"type": "string", "enum": ["br", "us"]},
                        "sql": {"type": "string"},
                    },
                    "required": ["market", "sql"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_open_triggers",
                "description": (
                    "Open watchlist triggers / alerts (price levels, fundamental thresholds). "
                    "Use for 'alertas abertos', 'triggers', 'quando comprar'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string", "description": "Optional filter"}},
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_perpetuum_status",
                "description": (
                    "Health of all 12 perpetuums + agents (last run, status, failures). Use for "
                    "'como estão os agents', 'system health', 'os perpetuums correram'."
                ),
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_briefing",
                "description": (
                    "Latest morning briefing markdown. Use for 'briefing', 'o que aconteceu hoje', "
                    "'resumo do dia'."
                ),
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_synthetic_ic",
                "description": (
                    "5-persona investment committee debate (Buffett, Druckenmiller, Taleb, Klarman, "
                    "Dalio) on a ticker. Slow (~3min). Use for deep contrarian view, 'qual o IC pensa', "
                    "'debate sobre X'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_variant_perception",
                "description": (
                    "Compare our internal view vs analyst consensus — flags where we disagree. "
                    "Use for 'estamos certos sobre X', 'consenso vs nós', 'vai contra mercado'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_drip_projection",
                "description": (
                    "Dividend reinvestment plan projection — value, shares, dividends over horizons. "
                    "Use for 'em quantos anos dobro shares de X', 'projecção DRIP X', 'payback divs'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "horizons": {"type": "string", "default": "5,10,15"},
                    },
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "compare_tickers",
                "description": (
                    "Side-by-side comparison of multiple tickers. Use for 'compara X com Y', "
                    "'X vs Y', 'qual melhor: X ou Y'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tickers": {"type": "string", "description": "Comma-separated tickers"},
                        "vs": {"type": "string", "default": "SPY"},
                    },
                    "required": ["tickers"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "web_research",
                "description": (
                    "Web search + LLM synthesis via Tavily (cached). Use for fresh news, qualitative "
                    "context, or anything not in DB. Costs API quota — only when other tools cannot answer."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "ticker": {"type": "string", "description": "Optional ticker context"},
                    },
                    "required": ["topic"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_dividend_calendar",
                "description": (
                    "Upcoming ex-dividend dates within N days. Use for 'próximos dividendos', "
                    "'quando recebo X', 'agenda de proventos'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Optional filter"},
                        "days": {"type": "integer", "default": 30},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "add_note",
                "description": (
                    "Persist a note about a ticker to the vault + DB. SIDE EFFECT — use only when "
                    "user explicitly asks 'anota', 'lembra-te disto', 'guarda essa observação'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "text": {"type": "string"},
                        "tags": {"type": "string", "description": "Comma-separated, optional"},
                    },
                    "required": ["ticker", "text"],
                },
            },
        },
    ]


def execute_tool(name: str, arguments: dict) -> dict:
    """Run a registered tool. Always returns a dict (never raises)."""
    fn = TOOLS.get(name)
    if not fn:
        return {"error": f"unknown tool: {name}"}
    try:
        return fn(**(arguments or {}))
    except TypeError as e:
        return {"error": f"bad arguments for {name}: {e}"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
