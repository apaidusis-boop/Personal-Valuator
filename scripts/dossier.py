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
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
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
            "dividend_streak_years, market_cap "
            "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,)
        ).fetchone()
        if f:
            out["fundamentals"] = dict(zip(
                ("period_end", "eps", "bvps", "roe", "pe", "pb", "dy",
                 "div_streak", "market_cap"), f))

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
        "sources: [in-house DB, BACEN IF.Data, Synthetic IC, vault thesis]" if is_bank
        else "sources: [in-house DB, Synthetic IC, vault thesis]",
        "tokens_claude_data_gather: 0",
        f"tags: [research, dossie, {mkt}, {'banks' if is_bank else co.get('sector','equity').lower()}]",
        "---",
        "",
        f"# 📑 {t} — {co.get('name', t)}",
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
