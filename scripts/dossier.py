"""ii dossier <TICKER> — gera dossiê de research em segundos.

Pipeline:
  1. Detect market + class (bank / equity / FII / ETF)
  2. Pull all in-house data (single JOIN-ish query across DB)
  3. SE banco AND not in BANK_CODE_MAP: lookup IfDataCadastro + append yaml
  4. SE banco: kickoff BACEN backfill paralelo (skip-cached)
  5. Render markdown skeleton com TODO_CLAUDE marcadores
  6. Write to obsidian_vault/tickers/<TICKER>_DOSSIE.md

Uso:
  ii dossier ABCB4              # cached: ~5s
  ii dossier BBAS3              # banco novo: ~90s
  ii dossier KO                 # equity US: ~1s
  ii dossier ABCB4 --refresh    # re-fetch BACEN
  ii dossier --list             # lista dossiers existentes

0 tokens Claude durante data-gather. Synth narrativa via TODO_CLAUDE markers
que Claude (ou user) preenche depois com Edit. Re-runs ~0.5-1k tokens.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from dataclasses import asdict, is_dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
DOSSIE_DIR = ROOT / "obsidian_vault" / "dossiers"
CODINST_YAML = ROOT / "config" / "bank_codinst.yaml"


# ─────────────────────────────────────────────────────────────────────────────
# Detection helpers
# ─────────────────────────────────────────────────────────────────────────────

def detect_market(ticker: str) -> str | None:
    """Procura ticker em ambas as DBs. None se não existir."""
    for mkt, db in DBS.items():
        if not db.exists():
            continue
        with sqlite3.connect(db, timeout=10) as c:
            row = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if row:
                return mkt
    return None


def detect_class(ticker: str, sector: str | None, market: str) -> str:
    """bank / fii / etf / equity"""
    if sector and sector.strip().lower() in ("banks", "bancos"):
        return "bank"
    # FII BR: termina em '11' e mercado=br (mas nem todos 11 são FII; usar sector se possível)
    if market == "br" and ticker.endswith("11"):
        # ETFs BR também podem terminar em 11 (ex: IVVB11)
        if (sector or "").lower() in ("etf", "fundo imob", "fii", "real estate"):
            return "fii"
        # heurística: se sector vazio e ends "11", default fii
        if not sector or sector.strip().lower() in ("none", "uncategorized", ""):
            return "fii"
    if (sector or "").lower() in ("etf",):
        return "etf"
    return "equity"


# ─────────────────────────────────────────────────────────────────────────────
# BACEN auto-bootstrap
# ─────────────────────────────────────────────────────────────────────────────

def lookup_bank_codinst(name_hint: str) -> dict[str, str] | None:
    """Sondar IfDataCadastro pelo nome. Returns {prudencial, financeiro, name} ou None.

    Lógica: do cadastro, escolher o conglomerado prudencial cujo NomeInstituicao
    contém `name_hint` (case-insensitive). Para crédito, picar o conglomerado
    financeiro do mesmo grupo.
    """
    name_q = name_hint.upper().strip()
    # AnoMes recente para que CodConglomerado* esteja preenchido
    anomes = 202506
    filter_q = quote(f"contains(NomeInstituicao,'{name_q}')", safe="")
    url = (f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/"
           f"IfDataCadastro(AnoMes={anomes})?$format=json&$filter={filter_q}")
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        rows = r.json().get("value", [])
    except Exception as e:
        print(f"  [bacen] cadastro lookup failed: {e}", file=sys.stderr)
        return None

    # Pick: prefer entry that IS the prudential conglomerate (CodInst starts with C0080)
    prudencial = None
    financeiro = None
    name_full = None
    for v in rows:
        cod = v.get("CodInst") or ""
        if cod.startswith("C0080") and not prudencial:
            prudencial = cod
            name_full = v.get("NomeInstituicao")
        elif cod.startswith("C0010") and not financeiro:
            financeiro = cod

    # Fallback: usar CodConglomerado* da primeira entry banco múltiplo
    if not (prudencial and financeiro):
        for v in rows:
            seg = (v.get("SegmentoTb") or "")
            if "Banco" in seg:
                if not prudencial:
                    prudencial = v.get("CodConglomeradoPrudencial")
                if not financeiro:
                    financeiro = v.get("CodConglomeradoFinanceiro")
                if not name_full:
                    name_full = v.get("NomeInstituicao")
                if prudencial and financeiro:
                    break

    if not (prudencial and financeiro):
        return None
    return {"prudencial": prudencial, "financeiro": financeiro,
            "name": name_full or name_hint}


def append_bank_codinst(ticker: str, codes: dict[str, str]) -> None:
    """Appende ao config/bank_codinst.yaml + cria skeleton rows na DB."""
    import yaml
    raw = {}
    if CODINST_YAML.exists():
        raw = yaml.safe_load(CODINST_YAML.read_text(encoding="utf-8")) or {}
    raw[ticker] = {
        "prudencial": codes["prudencial"],
        "financeiro": codes["financeiro"],
        "name": codes.get("name", ticker),
        "added_at": date.today().isoformat(),
    }
    CODINST_YAML.write_text(
        yaml.safe_dump(raw, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )

    # Criar skeleton rows para o ticker em bank_quarterly_history
    from calendar import monthrange
    today = date.today()
    periods = []
    for y in range(2018, today.year + 1):
        for m in (3, 6, 9, 12):
            if y == today.year and m > today.month - 2:
                break
            day = monthrange(y, m)[1]
            periods.append(f"{y}-{m:02d}-{day:02d}")
    with sqlite3.connect(DBS["br"], timeout=30) as c:
        n0 = c.execute("SELECT COUNT(*) FROM bank_quarterly_history WHERE ticker=?",
                       (ticker,)).fetchone()[0]
        for p in periods:
            c.execute("INSERT OR IGNORE INTO bank_quarterly_history "
                      "(ticker, period_end, source) VALUES (?, ?, ?)",
                      (ticker, p, "bacen_ifdata"))
        c.commit()
        n1 = c.execute("SELECT COUNT(*) FROM bank_quarterly_history WHERE ticker=?",
                       (ticker,)).fetchone()[0]
        print(f"  [setup] {ticker}: skeleton rows {n0} -> {n1} (+{n1-n0})")


def ensure_bacen_bank(ticker: str, name: str) -> bool:
    """Garante que o banco está no map. Returns True se está pronto para fetch."""
    # Lazy import — requer module reload em mesmo processo
    sys.path.insert(0, str(ROOT))
    from fetchers import bacen_ifdata_fetcher as bif
    if ticker in bif.BANK_CODE_MAP:
        return True
    print(f"  [setup] {ticker} não está em BANK_CODE_MAP — sondar BACEN cadastro...")
    codes = lookup_bank_codinst(name)
    if not codes:
        print(f"  [setup] BACEN cadastro não retornou match para '{name}'")
        return False
    print(f"  [setup] found: prudencial={codes['prudencial']} financeiro={codes['financeiro']}")
    append_bank_codinst(ticker, codes)
    # reload module to pick up new yaml
    bif.BANK_CODE_MAP = bif._load_bank_code_map()
    return ticker in bif.BANK_CODE_MAP


def run_bacen_backfill(ticker: str, since: str = "2018-01-01") -> dict:
    """Corre BACEN fetcher para o ticker. Returns stats."""
    sys.path.insert(0, str(ROOT))
    from fetchers import bacen_ifdata_fetcher as bif
    return bif.fetch_ticker(ticker, since=since, max_workers=5,
                            skip_cached=True, verbose=False)


# ─────────────────────────────────────────────────────────────────────────────
# Quality scores (Piotroski / Altman / Beneish)
# ─────────────────────────────────────────────────────────────────────────────

def _score_to_dict(score) -> dict:
    if score is None:
        return {}
    if is_dataclass(score):
        return {k: v for k, v in asdict(score).items()
                if v is not None and v != []}
    if hasattr(score, "__dict__"):
        return {k: v for k, v in score.__dict__.items()
                if not k.startswith("_") and v is not None}
    return {"raw": str(score)}


def pull_quality_scores(ticker: str, market: str) -> dict:
    """Compute Piotroski + Altman + Beneish in parallel. Returns dict with raw scores."""
    import concurrent.futures
    from scoring import altman, piotroski, beneish
    out: dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        f_p = ex.submit(piotroski.compute, ticker, market)
        f_a = ex.submit(altman.compute, ticker, market)
        f_b = ex.submit(beneish.compute, ticker, market)
        try:
            out["piotroski"] = _score_to_dict(f_p.result(timeout=20))
        except Exception as e:
            out["piotroski"] = {"error": f"{type(e).__name__}: {e}"}
        try:
            out["altman"] = _score_to_dict(f_a.result(timeout=20))
        except Exception as e:
            out["altman"] = {"error": f"{type(e).__name__}: {e}"}
        try:
            out["beneish"] = _score_to_dict(f_b.result(timeout=20))
        except Exception as e:
            out["beneish"] = {"error": f"{type(e).__name__}: {e}"}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Sector benchmark (peer_engine)
# ─────────────────────────────────────────────────────────────────────────────

def pull_sector_benchmark(ticker: str, market: str, sector: str | None) -> dict | None:
    """Peer sector medians (P/E, P/B, DY, ROE, ND/EBITDA, FCF Yield)."""
    if not sector:
        return None
    try:
        from agents.council.peer_engine import compute_sector_benchmark, compute_ticker_fcf_yield
    except Exception:
        return None
    bench = compute_sector_benchmark(ticker, market, sector)
    fcf_yield = compute_ticker_fcf_yield(ticker, market)
    return {
        "sector": bench.sector,
        "n_peers": bench.n_peers,
        "peers_used": bench.peers_used,
        "source": bench.source,
        "median_pe": bench.median_pe,
        "median_pb": bench.median_pb,
        "median_dy": bench.median_dy,
        "median_roe": bench.median_roe,
        "median_nde": bench.median_nde,
        "median_fcf_yield": bench.median_fcf_yield,
        "ticker_fcf_yield": fcf_yield,
        "_obj": bench,  # keep for render_comparison_table call
    }


# ─────────────────────────────────────────────────────────────────────────────
# Fair value DCF (valuation)
# ─────────────────────────────────────────────────────────────────────────────

def pull_fair_value(ticker: str, market: str, current_price: float | None) -> dict | None:
    """3-scenario DCF + margin of safety. Skip for banks (FCF model doesn't fit)."""
    try:
        from agents.council.valuation import (
            fetch_annual_evolution, compute_dcf, get_shares_outstanding,
        )
    except Exception:
        return None
    ev = fetch_annual_evolution(ticker, market, n=5)
    if not ev:
        return None
    shares = get_shares_outstanding(ticker, market)
    dcf = compute_dcf(ev, current_price, shares, market=market)
    return {
        "pessimistic": dcf.pessimistic_value,
        "base": dcf.base_value,
        "optimistic": dcf.optimistic_value,
        "wacc": dcf.base_wacc,
        "margin_of_safety_pct": dcf.margin_of_safety_pct,
        "current_price": dcf.current_price,
        "annual_evolution": [
            {"period_end": r.period_end, "total_revenue": r.revenue, "ebit": r.ebit,
             "net_income": r.net_income, "free_cash_flow": r.fcf,
             "ebit_margin": r.ebit_margin, "net_margin": r.net_margin}
            for r in ev
        ],
        "_dcf_obj": dcf,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Philosophy classification (Buffett / Graham / DRIP / Growth tag)
# ─────────────────────────────────────────────────────────────────────────────

def pull_philosophy(ticker: str, dossier_dict: dict, ev: list[dict] | None,
                    dcf: dict | None) -> dict | None:
    """Classify the stock into Value/Growth/Dividend/Buffett buckets."""
    try:
        from agents.council.philosophy import compute as compute_philo
    except Exception:
        return None
    scores = compute_philo(dossier_dict, annual_evolution=ev, dcf=dcf)
    return {
        "primary": scores.primary,
        "secondary": scores.secondary,
        "value": scores.value,
        "growth": scores.growth,
        "dividend": scores.dividend,
        "buffett": scores.buffett,
        "macro_exposure": scores.macro_exposure,
        "macro_dependency": scores.macro_dependency,
        "breakdown": scores.breakdown,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Competitors — top N peers in same sector with multiples (non-bank flow)
# ─────────────────────────────────────────────────────────────────────────────

def pull_competitors(ticker: str, market: str, sector: str | None, n: int = 5) -> list[dict]:
    """Return top N peers by market cap in same sector, with their multiples + price."""
    if not sector:
        return []
    db = DBS[market]
    if not db.exists():
        return []
    out: list[dict] = []
    with sqlite3.connect(db, timeout=15) as c:
        c.row_factory = sqlite3.Row
        try:
            rows = c.execute("""
                SELECT c.ticker, c.name, f.pe, f.pb, f.dy, f.roe, f.net_debt_ebitda,
                       f.market_cap, f.dividend_streak_years
                FROM companies c
                JOIN fundamentals f ON f.ticker = c.ticker
                WHERE c.sector = ?
                  AND c.ticker != ?
                  AND f.period_end = (
                      SELECT MAX(period_end) FROM fundamentals WHERE ticker = c.ticker
                  )
                ORDER BY f.market_cap DESC NULLS LAST
                LIMIT ?
            """, (sector, ticker, n)).fetchall()
        except sqlite3.OperationalError:
            return []
        for r in rows:
            d = dict(r)
            # latest price + YoY
            p = c.execute("SELECT close, date FROM prices WHERE ticker=? "
                          "ORDER BY date DESC LIMIT 1", (d["ticker"],)).fetchone()
            if p:
                d["price"] = p[0]
                d["price_date"] = p[1]
                yr = c.execute(
                    "SELECT close FROM prices WHERE ticker=? AND date <= "
                    "date((SELECT MAX(date) FROM prices WHERE ticker=?),'-365 days') "
                    "ORDER BY date DESC LIMIT 1",
                    (d["ticker"], d["ticker"])).fetchone()
                if yr and yr[0]:
                    d["yoy_pct"] = (p[0] - yr[0]) / yr[0] * 100
            out.append(d)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Verdict (BUY/HOLD/AVOID) — light read of pre-computed scores table
# ─────────────────────────────────────────────────────────────────────────────

def pull_verdict_light(ticker: str, market: str) -> dict | None:
    """Read latest verdict from scores table. Avoid running the full verdict.py
    subprocess — too slow for a dossier."""
    db = DBS[market]
    if not db.exists():
        return None
    with sqlite3.connect(db, timeout=10) as c:
        c.row_factory = sqlite3.Row
        try:
            row = c.execute(
                "SELECT run_date, score, passes_screen, details_json "
                "FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,)).fetchone()
        except sqlite3.OperationalError:
            return None
        if not row:
            return None
        out = {"run_date": row["run_date"], "screen_score": row["score"],
               "passes_screen": bool(row["passes_screen"])}
        if row["details_json"]:
            try:
                out["details"] = json.loads(row["details_json"])
            except Exception:
                pass
        return out


# ─────────────────────────────────────────────────────────────────────────────
# In-house data pull
# ─────────────────────────────────────────────────────────────────────────────

def pull_data(ticker: str, market: str) -> dict:
    """Single big bag of all in-house signals for the ticker."""
    db = DBS[market]
    out: dict = {"ticker": ticker, "market": market, "as_of": date.today().isoformat()}

    with sqlite3.connect(db, timeout=15) as c:
        # companies
        row = c.execute("SELECT name, sector, is_holding, currency FROM companies "
                        "WHERE ticker=?", (ticker,)).fetchone()
        out["company"] = dict(zip(("name", "sector", "is_holding", "currency"), row)) if row else {}

        # fundamentals (latest)
        f = c.execute(
            "SELECT period_end, eps, bvps, roe, pe, pb, dy, "
            "dividend_streak_years, market_cap, net_debt_ebitda, "
            "is_aristocrat "
            "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        if f:
            out["fundamentals"] = dict(zip(
                ("period_end", "eps", "bvps", "roe", "pe", "pb", "dy",
                 "div_streak", "market_cap", "net_debt_ebitda",
                 "is_aristocrat"), f))
            # Add canonical key alias for philosophy.compute()
            out["fundamentals"]["dividend_streak_years"] = out["fundamentals"]["div_streak"]

        # latest price
        p = c.execute("SELECT date, close FROM prices WHERE ticker=? "
                      "ORDER BY date DESC LIMIT 1", (ticker,)).fetchone()
        if p:
            out["last_price"] = {"date": p[0], "close": p[1]}
            # 1y ago
            yr = c.execute(
                "SELECT close FROM prices WHERE ticker=? AND date <= "
                "date((SELECT MAX(date) FROM prices WHERE ticker=?), '-365 days') "
                "ORDER BY date DESC LIMIT 1", (ticker, ticker)).fetchone()
            if yr:
                out["yoy_pct"] = (p[1] - yr[0]) / yr[0] * 100

        # conviction (br only — schema)
        try:
            cv = c.execute(
                "SELECT composite_score, thesis_health, ic_consensus, variant, "
                "data_coverage, paper_track FROM conviction_scores "
                "WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,)
            ).fetchone()
            if cv:
                out["conviction"] = dict(zip(
                    ("composite", "thesis", "ic", "variant", "data_cov", "paper"), cv))
        except sqlite3.OperationalError:
            pass

        # BACEN regulatory (banks só)
        bacen = c.execute(
            "SELECT period_end, basel_ratio, cet1_ratio, npl_ratio "
            "FROM bank_quarterly_history WHERE ticker=? AND basel_ratio IS NOT NULL "
            "ORDER BY period_end", (ticker,)
        ).fetchall() if market == "br" else []
        if bacen:
            out["bacen"] = [
                {"period": p, "basel": b, "cet1": c1, "npl": n}
                for p, b, c1, n in bacen
            ]

    # IC + thesis from vault files
    ic_path = TICKERS_DIR / f"{ticker}_IC_DEBATE.md"
    if ic_path.exists():
        text = ic_path.read_text(encoding="utf-8", errors="ignore")
        out["ic"] = {"path": ic_path.name, "raw": text}
        # parse frontmatter quick
        for line in text.splitlines()[:15]:
            if line.startswith("committee_verdict:"):
                out["ic"]["verdict"] = line.split(":", 1)[1].strip()
            elif line.startswith("confidence:"):
                out["ic"]["confidence"] = line.split(":", 1)[1].strip()
            elif line.startswith("consensus_pct:"):
                try:
                    out["ic"]["consensus_pct"] = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

    vault_path = TICKERS_DIR / f"{ticker}.md"
    if vault_path.exists():
        text = vault_path.read_text(encoding="utf-8", errors="ignore")
        out["vault"] = {"path": vault_path.name}
        # Extract Thesis section (between '## Thesis' and next '##')
        if "## Thesis" in text:
            start = text.index("## Thesis")
            after = text[start:]
            end = after.find("\n## ", 5)
            out["vault"]["thesis"] = (after[:end] if end > 0 else after).strip()

    # Fallback thesis: extrair do IC_DEBATE context se vault não tem
    if not (out.get("vault") or {}).get("thesis") and out.get("ic", {}).get("raw"):
        ic_text = out["ic"]["raw"]
        if "VAULT THESIS:" in ic_text:
            after = ic_text.split("VAULT THESIS:", 1)[1]
            # cortar no próximo header all-caps tipo "RECENT MATERIAL NEWS:" ou triple backtick
            for marker in ["RECENT MATERIAL NEWS", "FUNDAMENTALS LATEST", "```", "\n---"]:
                if marker in after:
                    after = after.split(marker, 1)[0]
            out.setdefault("vault", {})["thesis"] = "## Thesis\n\n" + after.strip()

    return out


# ─────────────────────────────────────────────────────────────────────────────
# Peer compare (banks)
# ─────────────────────────────────────────────────────────────────────────────

def pull_bank_peers(ticker: str, peer_tickers: list[str]) -> dict:
    """Fundamentals + BACEN snapshot para ticker + peers."""
    db = DBS["br"]
    out: dict = {}
    all_t = [ticker] + [p for p in peer_tickers if p != ticker]
    with sqlite3.connect(db, timeout=15) as c:
        for t in all_t:
            entry: dict = {}
            f = c.execute(
                "SELECT eps, bvps, roe, pe, pb, dy, dividend_streak_years, market_cap "
                "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (t,)
            ).fetchone()
            if f:
                entry["fund"] = dict(zip(
                    ("eps", "bvps", "roe", "pe", "pb", "dy", "div_streak", "market_cap"), f))
            # latest price + YoY
            p = c.execute("SELECT close, date FROM prices WHERE ticker=? "
                          "ORDER BY date DESC LIMIT 1", (t,)).fetchone()
            if p:
                entry["price"] = {"close": p[0], "date": p[1]}
                yr = c.execute(
                    "SELECT close FROM prices WHERE ticker=? AND date <= "
                    "date((SELECT MAX(date) FROM prices WHERE ticker=?),'-365 days') "
                    "ORDER BY date DESC LIMIT 1", (t, t)).fetchone()
                if yr:
                    entry["price"]["yoy_pct"] = (p[0] - yr[0]) / yr[0] * 100
            # BACEN latest non-NULL
            b = c.execute(
                "SELECT period_end, basel_ratio, cet1_ratio, npl_ratio "
                "FROM bank_quarterly_history WHERE ticker=? AND basel_ratio IS NOT NULL "
                "ORDER BY period_end DESC LIMIT 1", (t,)).fetchone()
            if b:
                entry["bacen_latest"] = dict(zip(
                    ("period", "basel", "cet1", "npl"), b))
            # BACEN ciclo: peak NPL e Q4 anterior
            bacen_q4_2024 = c.execute(
                "SELECT basel_ratio, cet1_ratio, npl_ratio FROM bank_quarterly_history "
                "WHERE ticker=? AND period_end='2024-12-31'", (t,)).fetchone()
            if bacen_q4_2024:
                entry["bacen_2024_q4"] = dict(zip(
                    ("basel", "cet1", "npl"), bacen_q4_2024))
            out[t] = entry
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Render
# ─────────────────────────────────────────────────────────────────────────────

def _fmt_pct(v: float | None, decimals: int = 2) -> str:
    if v is None:
        return "n/a"
    return f"{v*100:.{decimals}f}%"


def _fmt_money(v: float | None, scale: str = "B", currency: str = "R$") -> str:
    if v is None:
        return "n/a"
    if scale == "B":
        return f"{currency} {v/1e9:.2f}B"
    return f"{currency} {v:.2f}"


def _fmt_num(v: float | None, decimals: int = 2) -> str:
    if v is None:
        return "n/a"
    return f"{v:.{decimals}f}"


def render_dossier(data: dict, peers: dict | None = None) -> str:
    t = data["ticker"]
    mkt = data["market"]
    co = data.get("company") or {}
    fund = data.get("fundamentals") or {}
    ic = data.get("ic") or {}
    bacen = data.get("bacen") or []
    philo = data.get("philosophy") or {}
    is_bank = (co.get("sector") or "").lower() == "banks"
    currency = co.get("currency") or ("BRL" if mkt == "br" else "USD")

    lines: list[str] = []

    # Frontmatter + header
    lines += [
        "---",
        "type: research_dossie",
        f"ticker: {t}",
        f"name: {co.get('name', t)}",
        f"market: {mkt}",
        f"sector: {co.get('sector') or 'Uncategorized'}",
        f"is_holding: {bool(co.get('is_holding'))}",
        f"date: {data['as_of']}",
        f"verdict: {ic.get('verdict','TODO')}",
        f"verdict_confidence: {ic.get('confidence','n/a')}",
        f"verdict_consensus_pct: {ic.get('consensus_pct','n/a')}",
        f"strategy_primary: {philo.get('primary') or 'n/a'}",
        f"strategy_secondary: {philo.get('secondary') or 'n/a'}",
        "sources: [in-house DB, BACEN IF.Data, Synthetic IC, vault thesis]" if is_bank
        else "sources: [in-house DB, Synthetic IC, vault thesis]",
        "tokens_claude_data_gather: 0",
        f"tags: [research, dossie, {mkt}, {'banks' if is_bank else co.get('sector','equity').lower()}]",
        "---",
        "",
        f"# 📑 {t} — {co.get('name', t)}",
        "",
        (f"_Strategy: **{philo['primary']}**"
         + (f"  ·  Secondary: {philo['secondary']}" if philo.get("secondary") else "")
         + "_") if philo.get("primary") else "_(strategy: not classified)_",
        "",
        f"> Generated **{data['as_of']}** by `ii dossier {t}`. "
        f"Cross-links: [[{t}]] · "
        + (f"[[{t}_IC_DEBATE]]" if ic else "_(no IC yet)_")
        + " · [[CONSTITUTION]]",
        "",
        "## TL;DR",
        "",
        f"<!-- TODO_CLAUDE_TLDR: 3 frases sobre {t} a partir das tabelas abaixo. "
        f"Citar PE, DY, IC verdict, e o achado mais importante. -->",
        "",
    ]

    # ─── Sequential numbered sections ───────────────────────────
    sections: list[list[str]] = []

    # Fundamentals
    if fund:
        cur_sym = "R$" if currency == "BRL" else "USD"
        body = [
            f"- **Período**: {fund.get('period_end','n/a')}",
            f"- **EPS**: {_fmt_num(fund.get('eps'))}  |  "
            f"**BVPS**: {_fmt_num(fund.get('bvps'))}",
            f"- **ROE**: {_fmt_pct(fund.get('roe'))}  |  "
            f"**P/E**: {_fmt_num(fund.get('pe'))}  |  "
            f"**P/B**: {_fmt_num(fund.get('pb'))}",
            f"- **DY**: {_fmt_pct(fund.get('dy'))}  |  "
            f"**Streak div**: {int(fund['div_streak']) if fund.get('div_streak') else 'n/a'}y  |  "
            f"**Market cap**: {_fmt_money(fund.get('market_cap'), currency=cur_sym)}",
        ]
        last = data.get("last_price") or {}
        if last:
            body.append(f"- **Last price**: {currency} {last.get('close'):.2f} ({last.get('date')})  "
                        f"|  **YoY**: {data.get('yoy_pct',0):+.1f}%")
        sections.append(["Fundamentals snapshot", *body])

    # ── Strategy classification (philosophy) ──
    philo = data.get("philosophy") or {}
    if philo.get("primary"):
        body = [
            f"**Primary**: {philo['primary']}"
            + (f"  ·  **Secondary**: {philo['secondary']}" if philo.get("secondary") else ""),
            "",
            f"| Lente | Score | Sinais |",
            "|---|---|---|",
        ]
        for lens_key, lens_label in [("value", "Value (Graham)"), ("growth", "Growth"),
                                     ("dividend", "Dividend/DRIP"),
                                     ("buffett", "Buffett/Quality")]:
            score = philo.get(lens_key) or 0
            reasons = (philo.get("breakdown") or {}).get(lens_key) or []
            reason_str = " · ".join(reasons[:3]) if reasons else "—"
            body.append(f"| {lens_label} | **{score}/12** | {reason_str} |")
        macro = (philo.get("macro_exposure") or 0) + (philo.get("macro_dependency") or 0)
        body.append(
            f"| Macro (Exp/Dep) | {philo.get('macro_exposure', 0)}/6 + "
            f"{philo.get('macro_dependency', 0)}/6 = {macro}/12 | — |"
        )
        sections.append(["Strategy classification", *body])

    # ── Quality scores (Piotroski / Altman / Beneish) ──
    qs = data.get("quality_scores") or {}
    if qs:
        body = ["| Score | Valor | Interpretação |", "|---|---|---|"]
        # Piotroski
        pio = qs.get("piotroski") or {}
        if "f_score" in pio or "score" in pio:
            v = pio.get("f_score", pio.get("score"))
            interp = "✅ Strong (≥7)" if v and v >= 7 else \
                     "🟡 Mid (4-6)" if v and v >= 4 else \
                     "🔴 Weak (≤3)" if v is not None else "n/a"
            body.append(f"| Piotroski F-Score | **{v}/9** | {interp} |")
        elif pio.get("error"):
            body.append(f"| Piotroski F-Score | error | {pio['error'][:60]} |")
        # Altman
        alt = qs.get("altman") or {}
        z = alt.get("z") or alt.get("z_score") or alt.get("score")
        if z is not None:
            interp = "✅ Safe (>2.99)" if z > 2.99 else \
                     "🟡 Grey (1.81-2.99)" if z >= 1.81 else "🔴 Distress (<1.81)"
            body.append(f"| Altman Z-Score | **{z:+.2f}** | {interp} |")
        elif alt.get("error"):
            body.append(f"| Altman Z-Score | error | {alt['error'][:60]} |")
        # Beneish
        ben = qs.get("beneish") or {}
        m = ben.get("m") or ben.get("m_score")
        if m is not None:
            zone = ben.get("zone")
            interp = f"✅ {zone}" if zone == "clean" else \
                     f"🟡 {zone}" if zone == "grey" else \
                     f"🔴 {zone}" if zone else ""
            body.append(f"| Beneish M-Score | **{m:+.2f}** | {interp} |")
        elif ben.get("error"):
            body.append(f"| Beneish M-Score | error | {ben['error'][:60]} |")
        if len(body) > 2:
            sections.append(["Quality scores (auditor)", *body])

    # ── Multiples vs Sector benchmark ──
    sb = data.get("sector_benchmark")
    if sb and (sb.get("median_pe") or sb.get("median_dy") or sb.get("median_roe")):
        ticker_metrics = {
            "pe": fund.get("pe"),
            "pb": fund.get("pb"),
            "dy": fund.get("dy"),
            "roe": fund.get("roe"),
            "net_debt_ebitda": (data.get("fundamentals") or {}).get("net_debt_ebitda"),
            "fcf_yield": sb.get("ticker_fcf_yield"),
        }
        body = [sb["_obj"].render_comparison_table(t, ticker_metrics), ""]
        if sb.get("n_peers", 0) > 0:
            body.append(
                f"_Peer set ({sb['source']}): {sb['n_peers']} tickers — "
                f"{', '.join(sb.get('peers_used', [])[:8])}_"
            )
        else:
            body.append(f"_Source: {sb['source']} (DB n/a, fallback published medianas)._")
        sections.append([f"Multiples vs Sector ({sb['sector']})", *body])

    # Screen pass (banks BR)
    if is_bank and mkt == "br":
        body = ["| Critério | Threshold | Valor | OK? |",
                "|---|---|---|---|"]
        checks = [
            ("P/E ≤ 10", "≤ 10", fund.get("pe"), lambda v: v is not None and v <= 10),
            ("P/B ≤ 1.5", "≤ 1.5", fund.get("pb"), lambda v: v is not None and v <= 1.5),
            ("DY ≥ 6%", "≥ 6%", fund.get("dy"), lambda v: v is not None and v >= 0.06),
            ("ROE ≥ 12%", "≥ 12%", fund.get("roe"), lambda v: v is not None and v >= 0.12),
            ("Streak div ≥ 5y", "≥ 5", fund.get("div_streak"),
             lambda v: v is not None and v >= 5),
        ]
        for label, thresh, val, ok_fn in checks:
            if val is None:
                fmt = "n/a"
            elif "%" in label:
                fmt = _fmt_pct(val)
            elif "Streak" in label:
                fmt = f"{int(val)}y"
            else:
                fmt = _fmt_num(val)
            ok = "✅" if ok_fn(val) else ("❌" if val is not None else "?")
            body.append(f"| {label} | {thresh} | **{fmt}** | {ok} |")
        passes = sum(1 for _, _, v, fn in checks if v is not None and fn(v))
        body += ["", f"→ **{passes}/5 critérios** passam."]
        sections.append(["Screen — BR Banks (CLAUDE.md)", *body])

    # Peer comparison (banks)
    if is_bank and peers and mkt == "br":
        body = ["### Fundamentals", "",
                "| Métrica | " + " | ".join(peers.keys()) + " |",
                "|---|" + "---|" * len(peers)]
        rows_def = [
            ("Market cap", lambda f: _fmt_money(f.get("market_cap"), currency="R$")),
            ("P/E", lambda f: _fmt_num(f.get("pe"))),
            ("P/B", lambda f: _fmt_num(f.get("pb"))),
            ("ROE", lambda f: _fmt_pct(f.get("roe"))),
            ("DY", lambda f: _fmt_pct(f.get("dy"))),
            ("Streak div",
             lambda f: f"{int(f['div_streak'])}y" if f.get("div_streak") else "n/a"),
        ]
        for label, fn in rows_def:
            body.append(
                f"| {label} | "
                + " | ".join(fn(peers[tk].get("fund") or {}) for tk in peers)
                + " |"
            )
        body.append(
            "| YoY price | "
            + " | ".join(
                f"{(peers[tk].get('price') or {}).get('yoy_pct',0):+.1f}%"
                if (peers[tk].get('price') or {}).get('yoy_pct') is not None
                else "n/a"
                for tk in peers)
            + " |"
        )
        body += ["", "### BACEN regulatório (latest non-NULL)", "",
                 "| Métrica | " + " | ".join(peers.keys()) + " |",
                 "|---|" + "---|" * len(peers)]
        for label, key in [("Período", "period"), ("Basel", "basel"),
                           ("CET1", "cet1"), ("NPL E-H", "npl")]:
            row = f"| {label} |"
            for tk in peers:
                bl = peers[tk].get("bacen_latest") or {}
                v = bl.get(key)
                if v is None:
                    row += " n/a |"
                elif key == "period":
                    row += f" {v} |"
                else:
                    row += f" {_fmt_pct(v)} |"
            body.append(row)
        sections.append(["Peer comparison", *body])

    # BACEN timeline
    if is_bank and bacen:
        body = ["| Período | Basel | CET1 | NPL E-H |",
                "|---|---|---|---|"]
        for r in bacen:
            body.append(
                f"| {r['period']} | {_fmt_pct(r['basel'])} | "
                f"{_fmt_pct(r['cet1'])} | "
                f"{_fmt_pct(r['npl']) if r['npl'] else 'pending'} |"
            )
        body += ["",
                 "<!-- TODO_CLAUDE_BACEN_INSIGHT: 3-4 bullets sobre tendência "
                 "Basel/NPL + comparação peer. Identificar peak ciclo + recovery. -->"]
        sections.append(["BACEN timeline — capital + crédito", *body])

    # ── Fair value DCF + upside ──
    fv = data.get("fair_value")
    if fv and fv.get("base") is not None:
        cur_sym = "R$" if currency == "BRL" else "$"
        body = [
            "| Cenário | Crescimento 5y | Perpetuidade | Valor por acção |",
            "|---|---|---|---|",
            f"| Pessimista | 5% a.a. | 3% | {cur_sym} {fv['pessimistic']:.2f} |",
            f"| **Base** | **8% a.a.** | **4%** | **{cur_sym} {fv['base']:.2f}** |",
            f"| Optimista | 11% a.a. | 5% | {cur_sym} {fv['optimistic']:.2f} |",
        ]
        cp = fv.get("current_price")
        mos = fv.get("margin_of_safety_pct")
        if cp and mos is not None:
            tag = "✅ MoS > 25%" if mos > 0.25 else \
                  "🟡 MoS 0-25%" if mos > 0 else "🔴 Sobre-precificado"
            body += ["", (f"**Preço actual**: {cur_sym} {cp:.2f}  ·  "
                          f"**Margem de segurança**: {mos*100:+.0f}%  ·  "
                          f"**WACC**: {fv['wacc']*100:.0f}%  ·  {tag}")]
            upside_pct = (fv["base"] - cp) / cp * 100 if cp > 0 else None
            if upside_pct is not None:
                body.append(f"**Upside vs base**: {upside_pct:+.1f}%")
        sections.append(["Fair value (3-cenário DCF)", *body])
    elif (data.get("fundamentals") or {}).get("pe") and not is_bank:
        # No annual evolution data — show graham number proxy if possible
        eps = (data.get("fundamentals") or {}).get("eps")
        bvps = (data.get("fundamentals") or {}).get("bvps")
        if eps and bvps and eps > 0 and bvps > 0:
            import math
            graham = math.sqrt(22.5 * eps * bvps)
            cp = (data.get("last_price") or {}).get("close")
            cur_sym = "R$" if currency == "BRL" else "$"
            body = [
                f"_(DCF skipped — annual FCF data not available)_",
                "",
                f"**Graham Number** (sqrt(22.5 × EPS × BVPS)): {cur_sym} {graham:.2f}",
            ]
            if cp and cp > 0:
                mos = (graham - cp) / cp
                body.append(
                    f"**Preço actual**: {cur_sym} {cp:.2f}  ·  "
                    f"**Graham MoS**: {mos*100:+.0f}%"
                )
            sections.append(["Fair value (Graham proxy)", *body])

    # ── Competitors (top 5 by mkt cap, same sector) — non-bank ──
    comps = data.get("competitors") or []
    if comps:
        cur_sym = "R$" if currency == "BRL" else "$"
        body = [
            "| Ticker | Nome | Mkt Cap | P/E | P/B | DY | ROE | ND/EBITDA | Streak |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        # Anchor row first (the ticker itself)
        anchor_mc = fund.get("market_cap")
        anchor_streak = fund.get("div_streak")
        body.append(
            f"| **{t}** | _este_ | "
            f"{_fmt_money(anchor_mc, currency=cur_sym) if anchor_mc else 'n/a'} | "
            f"{_fmt_num(fund.get('pe'))} | {_fmt_num(fund.get('pb'))} | "
            f"{_fmt_pct(fund.get('dy'))} | {_fmt_pct(fund.get('roe'))} | "
            f"{_fmt_num((data.get('fundamentals') or {}).get('net_debt_ebitda'))} | "
            f"{int(anchor_streak) if anchor_streak else 'n/a'}y |"
        )
        for c in comps:
            name = (c.get("name") or "")[:22]
            mc_s = _fmt_money(c.get("market_cap"), currency=cur_sym) if c.get("market_cap") else "n/a"
            streak_s = f"{int(c['dividend_streak_years'])}y" if c.get("dividend_streak_years") else "n/a"
            body.append(
                f"| [[{c['ticker']}]] | {name} | {mc_s} | "
                f"{_fmt_num(c.get('pe'))} | {_fmt_num(c.get('pb'))} | "
                f"{_fmt_pct(c.get('dy'))} | {_fmt_pct(c.get('roe'))} | "
                f"{_fmt_num(c.get('net_debt_ebitda'))} | {streak_s} |"
            )
        sections.append([f"Competitors ({(co.get('sector') or 'sector')}, top 5 by mkt cap)", *body])

    # Synthetic IC
    if ic:
        sections.append(["Synthetic IC",
                         f"**🏛️ {ic.get('verdict','?')}** "
                         f"({ic.get('confidence','?')} confidence, "
                         f"{ic.get('consensus_pct','?')}% consensus)",
                         "",
                         f"→ Detalhe: [[{t}_IC_DEBATE]]"])
    else:
        sections.append(["Synthetic IC",
                         f"_(IC ainda não gerado para {t}. Execute "
                         f"`python -m agents.synthetic_ic {t}` "
                         "para popular antes do dossier ser refinado.)_"])

    # Thesis
    thesis = (data.get("vault") or {}).get("thesis")
    if thesis:
        clean = thesis.replace("## Thesis", "").strip()
        sections.append(["Thesis", clean, "", f"→ Vault: [[{t}]]"])

    # Conviction
    conv = data.get("conviction")
    if conv:
        sections.append(["Conviction breakdown",
                         "| Component | Score |",
                         "|---|---|",
                         f"| **Composite** | **{conv.get('composite','?')}** |",
                         f"| Thesis health | {conv.get('thesis','?')} |",
                         f"| IC consensus | {conv.get('ic','?')} |",
                         f"| Variant perception | {conv.get('variant','?')} |",
                         f"| Data coverage | {conv.get('data_cov','?')} |",
                         f"| Paper track | {conv.get('paper','?')} |"])

    # Risks
    sections.append(["Riscos identificados",
                     "<!-- TODO_CLAUDE_RISKS: 3-5 riscos prioritizados, baseados em IC + thesis "
                     "+ peer compare. Severidade 🟢🟡🔴. Cite trigger condition específica. -->"])

    # Position sizing
    is_holding = co.get("is_holding")
    sections.append(["Position sizing",
                     f"**Status atual**: {'holding (in portfolio)' if is_holding else 'watchlist'}",
                     "",
                     "<!-- TODO_CLAUDE_SIZING: guidance breve para entrada/aumento/redução. "
                     "Considerar BR/US isolation, market cap, weight prudente, DRIP/cash deploy. -->"])

    # Tracking triggers
    sections.append(["Tracking triggers (auto-monitoring)",
                     "<!-- TODO_CLAUDE_TRIGGERS: 3-5 condições mensuráveis em SQL/data "
                     "que indicariam re-avaliação. Ex: 'NPL > 4%', 'DY < 5.5%', "
                     "'thesis_health score < 60'. Citar tabela/coluna a monitorar. -->"])

    # Compute trail
    bacen_row = ("| BACEN backfill | Olinda OData | 0 |" if is_bank
                 else "| IC + thesis (cached) | Ollama prior session | 0 |")
    sections.append(["Compute trail",
                     "| Stage | Tool | Tokens Claude |",
                     "|---|---|---|",
                     "| Recon DB | sqlite3 | 0 |",
                     "| Vault read | filesystem | 0 |",
                     bacen_row,
                     "| Skeleton render | Python f-string | 0 |",
                     "| TODO_CLAUDE narrativa | Claude (subsequent edit) | ~600-1000 |",
                     "",
                     "→ Re-run desta dossier (refresh): ~0.5s + 0 tokens (data layer só) ou "
                     "~600 tokens (re-fill narrativa)."])

    # Stitch sections com numbering correto
    for i, section in enumerate(sections, start=1):
        title, *body = section
        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.extend(body)
        lines.append("")

    lines += [
        "---",
        f"*Generated by `ii dossier {t}` on {data['as_of']}. "
        f"100% in-house data. Fill TODO_CLAUDE_* markers para narrativa final.*",
    ]

    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def run_dossier(ticker: str, refresh: bool = False, peers: list[str] | None = None,
                quiet: bool = False) -> Path:
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.time()
    ticker = ticker.upper().strip()

    # 1. Detect
    market = detect_market(ticker)
    if not market:
        raise SystemExit(f"ticker {ticker!r} não encontrado em nenhuma DB. "
                         f"Adicionar ao universe.yaml + correr daily_update primeiro.")
    if not quiet:
        print(f"[dossier] {ticker} (market={market})")

    # 2. Pull data
    data = pull_data(ticker, market)
    company = data.get("company") or {}
    sector = company.get("sector")
    cls = detect_class(ticker, sector, market)
    if not quiet:
        print(f"  class={cls}, sector={sector}")

    # 3. If bank, ensure BACEN + backfill
    peers_data = None
    if cls == "bank" and market == "br":
        ok = ensure_bacen_bank(ticker, company.get("name") or ticker)
        if ok:
            stats = run_bacen_backfill(ticker)
            if not quiet:
                print(f"  [bacen] updated={stats['periods_updated']} "
                      f"cached={stats.get('periods_skipped',0)} "
                      f"partial={stats['periods_partial']} of {stats['periods_total']}")
            # Re-pull para incluir BACEN data atualizada
            data = pull_data(ticker, market)
        else:
            if not quiet:
                print(f"  [bacen] skipped — não conseguiu mapear CodInst")

        # peer compare default: ABCB4/BBDC4/ITUB4 sempre, plus target se diferente
        default_peers = ["ABCB4", "BBDC4", "ITUB4"]
        chosen = peers or default_peers
        if ticker not in chosen:
            chosen = [ticker] + chosen
        peers_data = pull_bank_peers(ticker, chosen)

    # 3a. Quality scores (Piotroski / Altman / Beneish)
    if not quiet:
        print("  [pull] quality scores...")
    data["quality_scores"] = pull_quality_scores(ticker, market)

    # 3b. Sector benchmark (peer medians)
    if not quiet:
        print("  [pull] sector benchmark...")
    data["sector_benchmark"] = pull_sector_benchmark(ticker, market, sector)

    # 3c. Fair value DCF (skip banks — FCF model doesn't fit)
    if cls != "bank":
        if not quiet:
            print("  [pull] fair value DCF...")
        last_price = (data.get("last_price") or {}).get("close")
        data["fair_value"] = pull_fair_value(ticker, market, last_price)
    else:
        data["fair_value"] = None

    # 3d. Philosophy classification (Buffett/Graham/DRIP/Growth)
    fund = data.get("fundamentals") or {}
    co_dict = data.get("company") or {}
    philo_input = {
        "fundamentals": fund,
        "quality_scores": data.get("quality_scores") or {},
        "sector": sector,
        "market": market,
        "is_holding": bool(co_dict.get("is_holding")),
    }
    ev_for_philo = (data.get("fair_value") or {}).get("annual_evolution")
    data["philosophy"] = pull_philosophy(ticker, philo_input, ev_for_philo, data.get("fair_value"))

    # 3e. Competitors (non-bank flow — banks already get peer compare hardcoded)
    if cls != "bank":
        if not quiet:
            print("  [pull] competitors...")
        data["competitors"] = pull_competitors(ticker, market, sector, n=5)
    else:
        data["competitors"] = []

    # 3f. Verdict light (from scores table)
    data["verdict_light"] = pull_verdict_light(ticker, market)

    # 4. Render
    md = render_dossier(data, peers=peers_data)

    # 5. Write
    out_path = TICKERS_DIR / f"{ticker}_DOSSIE.md"
    out_path.write_text(md, encoding="utf-8")

    elapsed = time.time() - t0
    if not quiet:
        print(f"  [done] {out_path.relative_to(ROOT)}  ({elapsed:.1f}s)")
        todo_count = md.count("TODO_CLAUDE_")
        if todo_count:
            print(f"  [next] {todo_count} TODO_CLAUDE_* markers — "
                  f"Claude/user fill via Edit para narrativa final")
    return out_path


def list_dossiers() -> None:
    paths = sorted(TICKERS_DIR.glob("*_DOSSIE.md"))
    print(f"{len(paths)} dossiers existentes:")
    for p in paths:
        ticker = p.name.replace("_DOSSIE.md", "")
        print(f"  {ticker}: {p.relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate research dossier for ticker.")
    ap.add_argument("ticker", nargs="?", help="Ticker symbol (e.g. ABCB4, KO)")
    ap.add_argument("--refresh", action="store_true",
                    help="Force re-fetch BACEN (skip cache)")
    ap.add_argument("--peers", help="Comma-separated peer tickers (default: trio bancos)")
    ap.add_argument("--list", action="store_true",
                    help="Lista dossiers existentes")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.list:
        list_dossiers()
        return
    if not args.ticker:
        ap.error("indicar ticker ou --list")

    peers = [p.strip().upper() for p in args.peers.split(",")] if args.peers else None
    run_dossier(args.ticker, refresh=args.refresh, peers=peers, quiet=args.quiet)


if __name__ == "__main__":
    main()
