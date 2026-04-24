"""obsidian_bridge — DB → Obsidian vault (markdown + Dataview frontmatter).

Exporta per-ticker notes e dashboards dinâmicos para um vault Obsidian.
Dataview plugin faz queries cross-note sobre os frontmatters YAML.

Default vault path: `./obsidian_vault/` (no root do projecto).
Override: env `OBSIDIAN_VAULT_PATH` ou flag `--vault <path>`.

Uso:
    python scripts/obsidian_bridge.py                    # export all holdings + watchlist
    python scripts/obsidian_bridge.py --ticker ACN       # só um ticker
    python scripts/obsidian_bridge.py --holdings-only
    python scripts/obsidian_bridge.py --refresh          # refresh_ticker primeiro
    python scripts/obsidian_bridge.py --vault ~/vaults/investimentos

Após primeira execução, abrir Obsidian → "Open folder as vault" → apontar para
 `obsidian_vault/`. Instalar plugins: **Dataview**, **Charts** (opcional).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _vault_path(override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    envp = os.environ.get("OBSIDIAN_VAULT_PATH")
    if envp:
        return Path(envp).expanduser().resolve()
    return ROOT / "obsidian_vault"


def _memory_notes_dir() -> Path:
    from scripts.notes_cli import NOTES_DIR
    return NOTES_DIR


def _yaml_val(v) -> str:
    """Escape YAML value. Round floats to 4 dp."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.4f}".rstrip("0").rstrip(".") or "0"
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\n", " ").replace("\"", "'")
    # quote se contém :, #, ou começa com char especial
    if any(c in s for c in ":#[]{},&*!|>%@`") or s.startswith(("-", "?")):
        return f'"{s}"'
    return s


def _slugify(s: str, maxlen: int = 60) -> str:
    """ASCII slug, lowercase, hyphens, truncated. Safe for filenames."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:maxlen].rstrip("-")


def _video_slug_name(video_id: str, published_at: str | None, channel: str | None, title: str | None) -> str:
    """Filename stem (sem .md) para uma nota de vídeo. Legível humanamente."""
    date_part = (published_at or "")[:10]
    ch = _slugify(channel or "", maxlen=25)
    ti = _slugify(title or video_id, maxlen=70)
    pieces = [p for p in (date_part, ch, ti) if p]
    stem = "_".join(pieces) if pieces else video_id
    return stem


def _frontmatter(data: dict) -> str:
    lines = ["---"]
    for k, v in data.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(_yaml_val(x) for x in v)}]")
        else:
            lines.append(f"{k}: {_yaml_val(v)}")
    lines.append("---\n")
    return "\n".join(lines)


def _fetch_ticker_data(ticker: str, market: str) -> dict:
    db = DB_BR if market == "br" else DB_US
    out: dict = {"ticker": ticker, "market": market}
    with sqlite3.connect(db) as c:
        row = c.execute(
            "SELECT name, sector, is_holding, currency FROM companies WHERE ticker=?",
            (ticker,),
        ).fetchone()
        if row:
            out["name"] = row[0]
            out["sector"] = row[1]
            out["is_holding"] = bool(row[2])
            out["currency"] = row[3]

        price_rows = c.execute(
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 2",
            (ticker,),
        ).fetchall()
        if price_rows:
            out["price"] = price_rows[0][1]
            out["price_date"] = price_rows[0][0]
            if len(price_rows) > 1 and price_rows[1][1]:
                out["change_1d_pct"] = round((price_rows[0][1] / price_rows[1][1] - 1) * 100, 2)

        # fundamentals latest
        f = c.execute(
            """SELECT period_end, pe, pb, dy, roe, eps, bvps, net_debt_ebitda,
                      dividend_streak_years, is_aristocrat
               FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if f:
            out["fund_period"] = f[0]
            out["pe"] = f[1]
            out["pb"] = f[2]
            out["dy_pct"] = round(f[3] * 100, 2) if f[3] else None
            out["roe_pct"] = round(f[4] * 100, 2) if f[4] else None
            out["eps"] = f[5]
            out["bvps"] = f[6]
            out["net_debt_ebitda"] = f[7]
            out["streak_years"] = f[8]
            out["aristocrat"] = bool(f[9]) if f[9] is not None else None

        # latest scores row
        s = c.execute(
            """SELECT run_date, score, passes_screen, details_json
               FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if s:
            out["screen_run"] = s[0]
            out["screen_score"] = s[1]
            out["screen_pass"] = bool(s[2])

        # portfolio position
        try:
            pos = c.execute(
                """SELECT quantity, entry_price FROM portfolio_positions
                   WHERE ticker=? AND active=1 LIMIT 1""",
                (ticker,),
            ).fetchone()
            if pos:
                out["position_qty"] = pos[0]
                out["entry_price"] = pos[1]
                if out.get("price") and pos[1]:
                    out["pnl_pct"] = round((out["price"] / pos[1] - 1) * 100, 2)
                    out["market_value"] = round(out["price"] * pos[0], 2)
        except sqlite3.OperationalError:
            pass

        # dividend events recent
        try:
            divs = c.execute(
                "SELECT ex_date, amount FROM dividends WHERE ticker=? ORDER BY ex_date DESC LIMIT 5",
                (ticker,),
            ).fetchall()
            out["recent_divs"] = [(r[0], r[1]) for r in divs]
        except sqlite3.OperationalError:
            out["recent_divs"] = []

        # events recent
        events = c.execute(
            "SELECT event_date, kind, summary FROM events WHERE ticker=? ORDER BY event_date DESC LIMIT 5",
            (ticker,),
        ).fetchall()
        out["recent_events"] = [(e[0], e[1], (e[2] or "")[:80]) for e in events]

        # YouTube insights recent
        try:
            yt = c.execute(
                """SELECT v.published_at, v.channel, i.kind, i.claim, i.confidence
                   FROM video_insights i LEFT JOIN videos v ON i.video_id=v.video_id
                   WHERE i.ticker=? ORDER BY COALESCE(v.published_at, i.created_at) DESC LIMIT 5""",
                (ticker,),
            ).fetchall()
            out["yt_insights"] = [(r[0] or "", r[1] or "", r[2], r[3][:180], r[4]) for r in yt]
        except sqlite3.OperationalError:
            out["yt_insights"] = []
    return out


def _scoring_extras(ticker: str) -> dict:
    """Call scoring modules to get Altman/Piotroski/DividendSafety."""
    out: dict = {}
    try:
        from scoring import altman
        a = altman.compute(ticker)
        if a:
            out["altman_z"] = round(getattr(a, "z", 0), 3)
            out["altman_zone"] = getattr(a, "zone", None)
    except Exception as e:  # noqa: BLE001
        out["altman_err"] = str(e)[:60]
    try:
        from scoring import piotroski
        p = piotroski.compute(ticker)
        if p:
            out["piotroski"] = getattr(p, "f_score", None)
            out["piotroski_max"] = 9
    except Exception as e:  # noqa: BLE001
        out["piotroski_err"] = str(e)[:60]
    try:
        from scoring import dividend_safety
        d = dividend_safety.compute(ticker)
        if d:
            out["div_safety"] = getattr(d, "total", getattr(d, "score", None))
            out["div_safety_verdict"] = getattr(d, "verdict", None)
    except Exception as e:  # noqa: BLE001
        out["div_safety_err"] = str(e)[:60]
    return out


def _load_user_notes(ticker: str) -> tuple[dict, str]:
    """Load optional user notes from memory/notes/<ticker>.md."""
    p = _memory_notes_dir() / f"{ticker}.md"
    if not p.exists():
        return {}, ""
    from scripts.notes_cli import _parse
    return _parse(p.read_text(encoding="utf-8"))


def _sector_slug(sector: str) -> str:
    if not sector:
        return "Uncategorized"
    return sector.replace("/", "_").replace(" ", "_")


def _compute_peers(ticker: str, market: str, limit: int = 5) -> list[str]:
    """Tickers no mesmo sector do mesmo market. Ordenados por market cap aprox
    (usando price*position_qty como proxy) ou alfabético como fallback."""
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        row = c.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
        if not row or not row[0]:
            return []
        sector = row[0]
        peers = c.execute(
            """SELECT c.ticker FROM companies c
               LEFT JOIN portfolio_positions p ON c.ticker=p.ticker AND p.active=1
               WHERE c.sector=? AND c.ticker<>?
               ORDER BY c.is_holding DESC, c.ticker ASC""",
            (sector, ticker),
        ).fetchall()
    return [p[0] for p in peers[:limit]]


def _price_series(ticker: str, market: str, days: int = 365) -> list[tuple[str, float]]:
    """Últimos N dias de close prices."""
    db = DB_BR if market == "br" else DB_US
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    with sqlite3.connect(db) as c:
        return list(c.execute(
            "SELECT date, close FROM prices WHERE ticker=? AND date>=? ORDER BY date ASC",
            (ticker, cutoff),
        ))


def _dividend_series(ticker: str, market: str, years: int = 10) -> list[tuple[int, float]]:
    """Anos × sum dividends."""
    db = DB_BR if market == "br" else DB_US
    cutoff_y = date.today().year - years
    with sqlite3.connect(db) as c:
        try:
            rows = list(c.execute(
                """SELECT substr(ex_date,1,4) AS y, SUM(amount) FROM dividends
                   WHERE ticker=? AND substr(ex_date,1,4) >= ? AND kind='cash'
                   GROUP BY y ORDER BY y""",
                (ticker, str(cutoff_y)),
            ))
        except sqlite3.OperationalError:
            rows = []
    return [(int(y), float(s)) for y, s in rows if y and s]


def _fundamentals_trend(ticker: str, market: str) -> list[tuple]:
    """Annual fundamentals trend: (period_end, pe, roe, dy)."""
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        try:
            return list(c.execute(
                """SELECT period_end, pe, roe, dy FROM fundamentals
                   WHERE ticker=? ORDER BY period_end ASC""",
                (ticker,),
            ))
        except sqlite3.OperationalError:
            return []


def _render_chart_block(
    chart_type: str, labels: list, series: list[dict],
    title: str = "", width: str = "80%",
) -> str:
    """Gera bloco Obsidian Charts plugin (YAML-inside-fence).
    Ver https://github.com/phibr0/obsidian-charts"""
    out = ["```chart", f"type: {chart_type}"]
    if title:
        out.append(f"title: \"{title}\"")
    out.append(f"labels: [{', '.join(repr(l) for l in labels)}]")
    out.append("series:")
    for s in series:
        out.append(f"  - title: {s['title']}")
        out.append(f"    data: {s['data']}")
    out.append(f"width: {width}")
    out.append("beginAtZero: false")
    out.append("fill: false")
    out.append("tension: 0.3")
    out.append("```")
    return "\n".join(out)


def _fetch_videos_for_ticker(ticker: str) -> list[tuple]:
    """Devolve [(video_id, published_at, channel, title)] para videos que mencionam ticker."""
    out: list[tuple] = []
    seen: set[str] = set()
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                for r in c.execute(
                    """SELECT DISTINCT v.video_id, v.published_at, v.channel, v.title
                       FROM videos v JOIN video_insights i ON v.video_id=i.video_id
                       WHERE i.ticker=?
                       ORDER BY v.published_at DESC, v.processed_at DESC""",
                    (ticker,),
                ):
                    if r[0] in seen:
                        continue
                    seen.add(r[0])
                    out.append(r)
            except sqlite3.OperationalError:
                pass
    return out


def _render_ticker_md(ticker: str, market: str) -> str:
    d = _fetch_ticker_data(ticker, market)
    extras = _scoring_extras(ticker)
    d.update(extras)
    notes_fm, notes_body = _load_user_notes(ticker)
    peers = _compute_peers(ticker, market)
    videos = _fetch_videos_for_ticker(ticker)
    sector_slug = _sector_slug(d.get("sector", ""))

    tags = [f"#{'holding' if d.get('is_holding') else 'watchlist'}", f"#{market}"]
    if d.get("sector"):
        tags.append(f"#{d['sector'].lower().replace(' ', '_')}")
    user_tags = notes_fm.get("tags", "")
    if user_tags:
        tags.extend(f"#{t.strip()}" for t in user_tags.split(",") if t.strip())

    fm_data = {
        "ticker": ticker,
        "name": d.get("name", ticker),
        "market": market,
        "sector": d.get("sector", "") or "",
        "is_holding": d.get("is_holding", False),
        "currency": d.get("currency", ""),
        "price": d.get("price"),
        "price_date": d.get("price_date", ""),
        "change_1d_pct": d.get("change_1d_pct"),
        "pe": d.get("pe"),
        "pb": d.get("pb"),
        "dy_pct": d.get("dy_pct"),
        "roe_pct": d.get("roe_pct"),
        "streak_years": d.get("streak_years"),
        "aristocrat": d.get("aristocrat"),
        "screen_score": d.get("screen_score"),
        "screen_pass": d.get("screen_pass"),
        "altman_z": d.get("altman_z"),
        "piotroski": d.get("piotroski"),
        "div_safety": d.get("div_safety"),
        "div_safety_verdict": d.get("div_safety_verdict"),
        "position_qty": d.get("position_qty"),
        "entry_price": d.get("entry_price"),
        "pnl_pct": d.get("pnl_pct"),
        "market_value": d.get("market_value"),
        "updated": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tags": [t.lstrip("#") for t in tags],
    }
    # Remove None
    fm_data = {k: v for k, v in fm_data.items() if v is not None and v != ""}

    out = [_frontmatter(fm_data)]
    out.append(f"# {ticker} — {d.get('name', '')}\n")
    out.append(" ".join(tags) + "\n")

    # Verdict (para holdings apenas — poupa tempo)
    if d.get("is_holding"):
        try:
            from scripts.verdict import compute_verdict, render_markdown
            v = compute_verdict(ticker)
            out.append(render_markdown(v))
            out.append("")
        except Exception as e:  # noqa: BLE001
            out.append(f"_(verdict indisponível: {e})_\n")

    # Links (Tier 1 + 2) — sector, market, peers
    out.append("## Links\n")
    market_upper = market.upper()
    out.append(f"- Sector: [[sectors/{sector_slug}|{d.get('sector', 'Uncategorized')}]]")
    out.append(f"- Market: [[markets/{market_upper}|{market_upper}]]")
    if peers:
        peer_links = " · ".join(f"[[{p}]]" for p in peers)
        out.append(f"- Peers: {peer_links}")
    if videos:
        vid_links = " · ".join(
            f"[[videos/{_video_slug_name(v[0], v[1], v[2], v[3])}|{(v[3] or v[0])[:40]}]]"
            for v in videos[:5]
        )
        out.append(f"- Vídeos: {vid_links}")
    out.append("")

    # Snapshot
    cur = d.get("currency") or ("R$" if market == "br" else "$")
    cur = "R$" if cur == "BRL" else ("$" if cur == "USD" else cur)
    out.append("## Snapshot\n")
    price_str = f"{d['price']:.2f}" if isinstance(d.get("price"), (int, float)) else "n/a"
    out.append(f"- **Preço**: {cur}{price_str}  ({d.get('price_date', '')})  ")
    if d.get("change_1d_pct") is not None:
        out[-1] += f"  _{d['change_1d_pct']:+.2f}% 1d_"
    out.append(f"- **Screen**: {d.get('screen_score', 'n/a')}  {'✓ PASS' if d.get('screen_pass') else '✗ fail'}")
    out.append(f"- **Altman Z**: {d.get('altman_z', 'n/a')} ({d.get('altman_zone','')})")
    out.append(f"- **Piotroski**: {d.get('piotroski', 'n/a')}/9")
    out.append(f"- **Div Safety**: {d.get('div_safety', 'n/a')}/100 ({d.get('div_safety_verdict','')})")
    if d.get("position_qty"):
        out.append(f"- **Posição**: {d['position_qty']} sh @ {cur}{d.get('entry_price','')}  →  P&L {d.get('pnl_pct','?')}%")
    out.append("")

    # Fundamentals
    out.append("## Fundamentals\n")
    out.append(f"- P/E: {d.get('pe','n/a')} | P/B: {d.get('pb','n/a')} | DY: {d.get('dy_pct','n/a')}%")
    out.append(f"- ROE: {d.get('roe_pct','n/a')}% | EPS: {d.get('eps','n/a')} | BVPS: {d.get('bvps','n/a')}")
    out.append(f"- Streak div: {d.get('streak_years','n/a')}y | Aristocrat: {d.get('aristocrat','n/a')}")
    out.append("")

    # User notes
    if notes_body and notes_body.strip():
        out.append("## Tese / Notas do investidor\n")
        out.append(notes_body.strip())
        out.append("")

    # Recent dividends
    if d.get("recent_divs"):
        out.append("## Dividendos recentes\n")
        for dt, amt in d["recent_divs"]:
            out.append(f"- {dt}: {cur}{amt:.4f}")
        out.append("")

    # SEC / CVM events
    if d.get("recent_events"):
        out.append("## Eventos (SEC/CVM)\n")
        for ev in d["recent_events"]:
            out.append(f"- **{ev[0]}** `{ev[1]}` — {ev[2]}")
        out.append("")

    # YouTube insights
    if d.get("yt_insights"):
        out.append("## YouTube insights\n")
        for dt, ch, kind, claim, conf in d["yt_insights"]:
            out.append(f"- `{dt or '??'}` **{ch}** — [{kind} conf={conf:.2f}] {claim}")
        out.append("")

    # Charts (requires plugin "Charts" — https://github.com/phibr0/obsidian-charts)
    price_rows = _price_series(ticker, market, days=365)
    if len(price_rows) >= 10:
        out.append("## 📈 Price history 1y\n")
        # down-sample para ~60 pontos
        step = max(1, len(price_rows) // 60)
        sampled = price_rows[::step]
        labels = [r[0] for r in sampled]
        data = [round(r[1], 2) for r in sampled]
        out.append(_render_chart_block(
            "line", labels, [{"title": ticker, "data": data}],
            title=f"{ticker} — 1y close",
        ))
        out.append("")

    div_rows = _dividend_series(ticker, market, years=10)
    if div_rows:
        out.append("## 💰 Dividendos anuais (10y)\n")
        labels = [str(y) for y, _ in div_rows]
        data = [round(s, 4) for _, s in div_rows]
        out.append(_render_chart_block(
            "bar", labels, [{"title": "Dividends", "data": data}],
            title=f"{ticker} — dividend history",
        ))
        out.append("")

    trend = _fundamentals_trend(ticker, market)
    if len(trend) >= 3:
        out.append("## 📊 Fundamentals trend\n")
        # Formato flexivel — pe e roe em escalas distintas; mostrar separados
        labels = [r[0] for r in trend]
        pes = [r[1] if r[1] is not None else 0 for r in trend]
        roes = [round((r[2] or 0) * 100, 2) for r in trend]
        dys = [round((r[3] or 0) * 100, 2) for r in trend]
        out.append(_render_chart_block(
            "line", labels,
            [{"title": "P/E", "data": pes}],
            title="P/E over time",
        ))
        out.append("")
        out.append(_render_chart_block(
            "line", labels,
            [
                {"title": "ROE %", "data": roes},
                {"title": "DY %", "data": dys},
            ],
            title="ROE & DY %",
        ))
        out.append("")

    out.append(f"\n---\n*Gerado por obsidian_bridge — {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}*\n")
    return "\n".join(out)


def _render_sector_page(sector: str, tickers_in_sector: list[tuple]) -> str:
    """tickers_in_sector: [(ticker, market, is_holding)]"""
    slug = _sector_slug(sector)
    fm = {"type": "sector", "name": sector, "count": len(tickers_in_sector), "tags": ["sector"]}
    out = [_frontmatter(fm), f"# 🏢 {sector}\n"]
    out.append(f"Total tickers: **{len(tickers_in_sector)}**")
    holdings = [t for t in tickers_in_sector if t[2]]
    if holdings:
        out.append(f"Holdings: **{len(holdings)}**\n")
    out.append("## Tabela live (Dataview)\n")
    out.append("```dataview")
    out.append("TABLE market, price, pnl_pct, screen_score, altman_z, piotroski")
    out.append('FROM "tickers"')
    out.append(f'WHERE sector = "{sector}"')
    out.append("SORT is_holding DESC, pnl_pct ASC")
    out.append("```\n")
    out.append("## Tickers neste sector\n")
    for tk, mk, is_h in sorted(tickers_in_sector, key=lambda x: (not x[2], x[0])):
        mark = "★ " if is_h else ""
        out.append(f"- {mark}[[{tk}]] _({mk})_")
    return "\n".join(out)


def _render_market_page(market: str, tickers_in_market: list[tuple]) -> str:
    fm = {"type": "market", "name": market, "tags": ["market"]}
    out = [_frontmatter(fm), f"# 🌐 Market: {market.upper()}\n"]
    out.append("## Holdings — P&L sorted\n")
    out.append("```dataview")
    out.append("TABLE sector, price, pnl_pct AS \"P&L %\", screen_score, altman_z, piotroski")
    out.append('FROM "tickers"')
    out.append(f'WHERE market = "{market}" AND is_holding = true')
    out.append("SORT pnl_pct ASC")
    out.append("```\n")
    out.append("## Watchlist screen passes\n")
    out.append("```dataview")
    out.append("TABLE sector, price, screen_score, dy_pct AS \"DY%\"")
    out.append('FROM "tickers"')
    out.append(f'WHERE market = "{market}" AND is_holding = false AND screen_pass = true')
    out.append("SORT screen_score DESC")
    out.append("```\n")
    out.append("## Por sector neste mercado\n")
    out.append("```dataview")
    out.append("TABLE length(rows) AS Total, sum(rows.is_holding) AS Holdings")
    out.append('FROM "tickers"')
    out.append(f'WHERE market = "{market}"')
    out.append("GROUP BY sector")
    out.append("SORT length(rows) DESC")
    out.append("```\n")
    return "\n".join(out)


def _render_video_page(video_id: str, market_hint: str = "br") -> str | None:
    """Busca metadata + insights em AMBAS as DBs e gera nota para o video."""
    meta = None
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                m = c.execute(
                    """SELECT video_id, url, title, channel, channel_id, published_at,
                              duration_sec, lang, status, tickers_seen
                       FROM videos WHERE video_id=?""",
                    (video_id,),
                ).fetchone()
                if m:
                    meta = m
                    break
            except sqlite3.OperationalError:
                pass
    if meta is None:
        return None

    insights: list[tuple] = []
    themes: list[tuple] = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                for r in c.execute(
                    "SELECT ticker, kind, claim, confidence FROM video_insights WHERE video_id=? ORDER BY confidence DESC",
                    (video_id,),
                ):
                    insights.append(r)
                for r in c.execute(
                    "SELECT theme, stance, summary, confidence FROM video_themes WHERE video_id=? ORDER BY confidence DESC",
                    (video_id,),
                ):
                    themes.append(r)
            except sqlite3.OperationalError:
                pass

    tickers_mentioned = sorted({i[0] for i in insights})
    fm = {
        "type": "video",
        "aliases": [meta[0]],
        "video_id": meta[0],
        "channel": meta[3] or "",
        "published_at": meta[5] or "",
        "duration_sec": meta[6] or 0,
        "lang": meta[7] or "",
        "status": meta[8] or "",
        "tickers_mentioned": tickers_mentioned,
        "tags": ["video", f"channel_{(meta[3] or 'unknown').lower().replace(' ', '_')}"],
    }
    out = [_frontmatter(fm)]
    out.append(f"# 🎬 {meta[2] or video_id}\n")
    out.append(f"**Canal**: {meta[3] or 'unknown'} | **Publicado**: {meta[5] or '?'} | **Duração**: {(meta[6] or 0)//60}min\n")
    out.append(f"**URL**: [{meta[1]}]({meta[1]})\n")

    out.append("## Tickers mencionados\n")
    if tickers_mentioned:
        out.append(" · ".join(f"[[{t}]]" for t in tickers_mentioned))
    else:
        out.append("_(nenhum)_")
    out.append("")

    if insights:
        out.append("## Insights extraídos\n")
        by_ticker: dict[str, list] = {}
        for ins in insights:
            by_ticker.setdefault(ins[0], []).append(ins)
        for tk, rows in by_ticker.items():
            out.append(f"### [[{tk}]]")
            for r in rows:
                out.append(f"- [{r[3]:.2f} {r[1]}] {r[2]}")
            out.append("")

    if themes:
        out.append("## Temas macro\n")
        for th in themes:
            stance = th[1] or ""
            out.append(f"- **{th[0]}** {stance} _(conf {th[3]:.2f})_ — {th[2]}")

    return "\n".join(out)


def _portfolio_live_snapshot() -> dict:
    """Snapshot vivo para a landing page (não depende de Dataview)."""
    from analytics.fx import fx_rate, total_portfolio_brl
    fx = total_portfolio_brl()
    holdings: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute("""
                SELECT p.ticker, p.quantity, p.entry_price, p.entry_date, p.notes,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS px,
                       (SELECT date FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS px_date,
                       c.name, c.sector, c.currency
                FROM portfolio_positions p LEFT JOIN companies c ON c.ticker=p.ticker
                WHERE p.active=1
                ORDER BY p.ticker
            """).fetchall()
            for r in rows:
                tk, qty, entry, entry_date, notes, px, px_date, name, sector, curr = r
                mv = (px or 0) * (qty or 0)
                cost = (entry or 0) * (qty or 0)
                pnl = ((px / entry - 1) * 100) if (px and entry) else None
                pnl_abs = mv - cost
                holdings.append({
                    "ticker": tk, "name": name or tk, "sector": sector or "—",
                    "market": market, "currency": curr or ("BRL" if market == "br" else "USD"),
                    "qty": qty, "entry_price": entry, "entry_date": entry_date,
                    "price": px, "price_date": px_date,
                    "market_value": mv, "cost": cost,
                    "pnl_pct": round(pnl, 2) if pnl is not None else None,
                    "pnl_abs": round(pnl_abs, 2),
                    "notes": notes or "",
                })
    return {"fx": fx, "holdings": holdings}


def _portfolio_evolution_series(days: int = 90) -> tuple[list[str], list[float], list[float], list[float]]:
    """Lê portfolio_snapshots em ambas DBs e agrega MV total BRL por data."""
    from collections import defaultdict
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {"br": 0.0, "us_brl": 0.0})
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            try:
                for d, mv_brl in c.execute(
                    """SELECT date, SUM(mv_brl) FROM portfolio_snapshots
                       WHERE date >= ? GROUP BY date""",
                    (cutoff,),
                ):
                    key = "br" if market == "br" else "us_brl"
                    totals[d][key] = float(mv_brl or 0)
            except sqlite3.OperationalError:
                pass
    dates = sorted(totals.keys())
    br_vals = [round(totals[d]["br"], 0) for d in dates]
    us_vals = [round(totals[d]["us_brl"], 0) for d in dates]
    total_vals = [round(totals[d]["br"] + totals[d]["us_brl"], 0) for d in dates]
    return dates, br_vals, us_vals, total_vals


def _render_my_portfolio_page() -> str:
    """THE landing page — snapshot actual + pointers."""
    snap = _portfolio_live_snapshot()
    fx = snap["fx"]
    holdings = snap["holdings"]
    today = date.today().isoformat()

    lines = ["---", "tags: [portfolio, landing]", "---"]
    lines.append(f"# 💼 Minha Carteira — {today}\n")
    lines.append(f"_Actualizado: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}_")
    lines.append(f"_Refresh: `ii obsidian --refresh --holdings-only`_\n")

    # Headline
    lines.append("## Totais consolidados\n")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---|---|")
    lines.append(f"| **Total BRL** | **R$ {fx['total_brl']:,.2f}** |")
    lines.append(f"| **Total USD** | ${fx['total_usd']:,.2f} |")
    lines.append(f"| BR equity | R$ {fx['br_mv_brl']:,.2f} ({fx['holdings_br']} holdings) |")
    lines.append(f"| US equity | ${fx['us_mv_usd']:,.2f} = R$ {fx['us_mv_brl']:,.2f} ({fx['holdings_us']} holdings) |")
    lines.append(f"| PTAX USDBRL | {fx['fx_ptax']:.4f} |\n")

    # Quick links
    lines.append("## 🔍 Explora\n")
    lines.append(f"- [[briefings/{today}|🌅 Morning Briefing hoje]]")
    lines.append("- [[Holdings|📋 Tabela completa de posições]]")
    lines.append("- [[Allocation|📊 Alocação (sector / market / quality)]]")
    lines.append("- [[Transactions|📜 Log de transacções]]")
    lines.append("- [[dashboards/Portfolio|📊 Dataview queries]]")
    lines.append("- [[markets/BR|🇧🇷 Market BR]]  ·  [[markets/US|🇺🇸 Market US]]\n")

    # Holdings compact
    lines.append("## Holdings (ranked por |P&L%|)\n")
    br = [h for h in holdings if h["market"] == "br"]
    us = [h for h in holdings if h["market"] == "us"]

    def _section(title: str, rows: list[dict], cur: str):
        lines.append(f"### {title}\n")
        lines.append("| Ticker | Qty | Entry | Now | MV | P&L % | P&L abs |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for h in sorted(rows, key=lambda x: -(x["pnl_pct"] or 0)):
            pnl_s = f"{h['pnl_pct']:+.2f}%" if h["pnl_pct"] is not None else "—"
            pnl_abs_s = f"{cur}{h['pnl_abs']:+,.0f}" if h["pnl_abs"] is not None else "—"
            lines.append(
                f"| [[{h['ticker']}]] | {h['qty']:g} | "
                f"{cur}{h['entry_price']:.2f} | {cur}{h['price'] or 0:.2f} | "
                f"{cur}{h['market_value']:,.0f} | {pnl_s} | {pnl_abs_s} |"
            )
        lines.append("")

    if br:
        _section(f"🇧🇷 BR ({len(br)} posições)", br, "R$ ")
    if us:
        _section(f"🇺🇸 US ({len(us)} posições)", us, "$ ")

    # Portfolio evolution chart (requires Charts plugin + portfolio_snapshots populated)
    dates, br_vals, us_vals, total_vals = _portfolio_evolution_series(90)
    if len(dates) >= 5:
        lines.append("## 📈 Evolução MV — 90d (BRL)\n")
        # down-sample to ~30 points if too dense
        step = max(1, len(dates) // 30)
        sd = dates[::step]
        lines.append(_render_chart_block(
            "line", sd,
            [
                {"title": "Total BRL", "data": total_vals[::step]},
                {"title": "BR", "data": br_vals[::step]},
                {"title": "US (BRL)", "data": us_vals[::step]},
            ],
            title="Market value consolidado",
            width="100%",
        ))
        lines.append("")

    lines.append("---")
    lines.append("*Fonte: DB `portfolio_positions` + `prices` últimos; FX via `analytics/fx.py`.*")
    lines.append("*Chart evolução requer plugin **Charts** + dados de `portfolio_snapshots`.*")
    return "\n".join(lines)


def _render_holdings_page() -> str:
    """Tabela unificada BR+US em BRL, sortable via Dataview."""
    snap = _portfolio_live_snapshot()
    fx = snap["fx"]
    holdings = snap["holdings"]
    rate = fx["fx_ptax"]
    today = date.today().isoformat()

    lines = ["---", "tags: [holdings, positions]", f"date: {today}", "---"]
    lines.append("# 📋 Holdings — todas posições activas\n")
    lines.append(f"_Total consolidado: **R$ {fx['total_brl']:,.2f}**  |  ${fx['total_usd']:,.2f}_\n")
    lines.append("Tabela completa em BRL (US convertido via PTAX actual).\n")

    lines.append("| Ticker | Mkt | Sector | Qty | Entry | Now | MV (BRL) | Weight | P&L % |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|")
    # Compute weights in BRL
    total_brl = fx["total_brl"] or 1
    rows_enriched = []
    for h in holdings:
        mv_brl = h["market_value"] * (rate if h["market"] == "us" else 1)
        rows_enriched.append({**h, "mv_brl": mv_brl, "weight_pct": mv_brl / total_brl * 100})
    rows_enriched.sort(key=lambda x: -x["mv_brl"])
    for h in rows_enriched:
        mkt_flag = "🇧🇷" if h["market"] == "br" else "🇺🇸"
        cur = "R$" if h["market"] == "br" else "$"
        pnl_s = f"{h['pnl_pct']:+.2f}%" if h["pnl_pct"] is not None else "—"
        lines.append(
            f"| [[{h['ticker']}]] | {mkt_flag} | {h['sector'] or '—'} | {h['qty']:g} | "
            f"{cur}{h['entry_price']:.2f} | {cur}{h['price'] or 0:.2f} | "
            f"R$ {h['mv_brl']:,.0f} | {h['weight_pct']:.1f}% | {pnl_s} |"
        )
    lines.append("")
    lines.append(f"\n**Totais**: R$ {fx['total_brl']:,.2f} (BR R$ {fx['br_mv_brl']:,.2f}  +  US R$ {fx['us_mv_brl']:,.2f})\n")

    lines.append("## Dataview live (via frontmatter dos tickers)\n")
    lines.append("```dataview")
    lines.append("TABLE market, sector, position_qty, entry_price, price, pnl_pct, market_value")
    lines.append('FROM "tickers"')
    lines.append("WHERE is_holding = true AND position_qty > 0")
    lines.append("SORT pnl_pct ASC")
    lines.append("```")
    return "\n".join(lines)


def _render_allocation_page() -> str:
    """Breakdowns by market, sector, quality."""
    snap = _portfolio_live_snapshot()
    fx = snap["fx"]
    rate = fx["fx_ptax"]
    holdings = snap["holdings"]
    total_brl = fx["total_brl"] or 1

    # Enrich com MV em BRL
    for h in holdings:
        h["mv_brl"] = h["market_value"] * (rate if h["market"] == "us" else 1)
        h["weight_pct"] = h["mv_brl"] / total_brl * 100

    lines = ["---", "tags: [allocation, portfolio]", "---"]
    lines.append("# 📊 Alocação\n")
    lines.append(f"_Total: **R$ {fx['total_brl']:,.2f}** |  PTAX: {fx['fx_ptax']:.4f}_\n")

    # By market
    lines.append("## Por mercado\n")
    lines.append("| Mercado | Holdings | MV (BRL) | % |")
    lines.append("|---|---:|---:|---:|")
    br_sum = sum(h["mv_brl"] for h in holdings if h["market"] == "br")
    us_sum = sum(h["mv_brl"] for h in holdings if h["market"] == "us")
    lines.append(f"| 🇧🇷 BR | {sum(1 for h in holdings if h['market']=='br')} | R$ {br_sum:,.0f} | {br_sum/total_brl*100:.1f}% |")
    lines.append(f"| 🇺🇸 US | {sum(1 for h in holdings if h['market']=='us')} | R$ {us_sum:,.0f} | {us_sum/total_brl*100:.1f}% |")
    lines.append("")

    # By sector
    lines.append("## Por sector\n")
    lines.append("| Sector | Holdings | MV (BRL) | % |")
    lines.append("|---|---:|---:|---:|")
    by_sector: dict[str, list] = {}
    for h in holdings:
        by_sector.setdefault(h["sector"] or "—", []).append(h)
    for sec, rows in sorted(by_sector.items(), key=lambda x: -sum(r["mv_brl"] for r in x[1])):
        mv = sum(r["mv_brl"] for r in rows)
        tickers_links = ", ".join(f"[[{r['ticker']}]]" for r in rows)
        lines.append(f"| [[sectors/{_sector_slug(sec)}|{sec}]] | {len(rows)} | R$ {mv:,.0f} | {mv/total_brl*100:.1f}% |")
    lines.append("")

    # Top 10 concentrations
    lines.append("## Top 10 concentrações\n")
    top10 = sorted(holdings, key=lambda x: -x["mv_brl"])[:10]
    lines.append("| # | Ticker | MV (BRL) | % | Cumulative % |")
    lines.append("|---:|---|---:|---:|---:|")
    cum = 0.0
    for i, h in enumerate(top10, 1):
        cum += h["weight_pct"]
        lines.append(f"| {i} | [[{h['ticker']}]] | R$ {h['mv_brl']:,.0f} | {h['weight_pct']:.1f}% | {cum:.1f}% |")
    lines.append("")

    # Dataview by quality (if frontmatter has altman/piotroski)
    lines.append("## Por quality bucket (Dataview)\n")
    lines.append("Altman Z ≥ 3 E Piotroski ≥ 6 = **Tier A**; Altman ≥ 1.8 E Piot ≥ 4 = **Tier B**; restante = **Tier C**.\n")
    lines.append("```dataview")
    lines.append("TABLE altman_z, piotroski, market_value, pnl_pct")
    lines.append('FROM "tickers"')
    lines.append("WHERE is_holding = true")
    lines.append("SORT altman_z DESC")
    lines.append("```")
    return "\n".join(lines)


def _render_transactions_page() -> str:
    """Log de entries + exits do portfolio_positions."""
    today = date.today().isoformat()
    lines = ["---", "tags: [transactions, log]", "---"]
    lines.append("# 📜 Log de transacções\n")
    lines.append(f"_Gerado: {today}. Fonte: `portfolio_positions` em ambas as DBs._\n")

    # Active entries
    active: list[tuple] = []
    exits: list[tuple] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            for r in c.execute("""
                SELECT ticker, quantity, entry_price, entry_date, notes
                FROM portfolio_positions WHERE active=1
                ORDER BY entry_date DESC, ticker
            """):
                active.append((market, *r))
            for r in c.execute("""
                SELECT ticker, quantity, entry_price, entry_date, exit_price, exit_date, notes
                FROM portfolio_positions WHERE active=0
                ORDER BY exit_date DESC, ticker
            """):
                exits.append((market, *r))

    lines.append(f"## Posições activas ({len(active)})\n")
    lines.append("| Data entry | Ticker | Mkt | Qty | Entry | Notes |")
    lines.append("|---|---|---|---:|---:|---|")
    for market, tk, qty, entry, ed, notes in active:
        cur = "R$" if market == "br" else "$"
        lines.append(f"| {ed or '—'} | [[{tk}]] | {market.upper()} | {qty:g} | {cur}{entry or 0:.2f} | {(notes or '')[:60]} |")
    lines.append("")

    if exits:
        lines.append(f"## Posições fechadas ({len(exits)})\n")
        lines.append("| Data exit | Ticker | Mkt | Qty | Entry | Exit | Δ% | Notes |")
        lines.append("|---|---|---|---:|---:|---:|---:|---|")
        for market, tk, qty, entry, ed, ep, xd, notes in exits:
            cur = "R$" if market == "br" else "$"
            delta = ((ep / entry - 1) * 100) if (entry and ep) else None
            d_s = f"{delta:+.2f}%" if delta is not None else "—"
            lines.append(f"| {xd or '—'} | [[{tk}]] | {market.upper()} | {qty:g} | {cur}{entry or 0:.2f} | {cur}{ep or 0:.2f} | {d_s} | {(notes or '')[:60]} |")
        lines.append("")
    else:
        lines.append("## Posições fechadas\n_(nenhuma registada)_\n")

    lines.append("## Adicionar transacção\n")
    lines.append("```bash")
    lines.append('ii tx buy ACN 2 176.50 "thesis turnaround after Q2 miss"')
    lines.append("ii tx sell TEN 35 38.76 \"distress signal converged\"")
    lines.append("```")
    lines.append("_(comando `ii tx` disponível no CLI)_")
    return "\n".join(lines)


def _render_portfolio_dashboard() -> str:
    return """---
tags: [dashboard, portfolio]
---
# 📊 Portfolio Dashboard (Dataview)

> Requer plugin **Dataview** habilitado. Para vista sem plugin, ver [[My Portfolio]].

## Holdings — live snapshot

```dataview
TABLE
  price AS "Preço",
  change_1d_pct AS "1d %",
  pnl_pct AS "P&L %",
  screen_score AS "Screen",
  altman_z AS "Altman",
  piotroski AS "Piot",
  div_safety AS "DivSaf"
FROM "tickers"
WHERE is_holding = true
SORT pnl_pct ASC
```

## Watchlist — screen passa

```dataview
TABLE
  price AS "Preço",
  pe AS "P/E",
  pb AS "P/B",
  dy_pct AS "DY%",
  screen_score AS "Screen",
  altman_z AS "Altman",
  piotroski AS "Piot"
FROM "tickers"
WHERE is_holding = false AND screen_pass = true
SORT screen_score DESC
```

## Screen falhas críticas (Altman < 3 ou Piotroski ≤ 3)

```dataview
TABLE altman_z, piotroski, screen_score, price
FROM "tickers"
WHERE (altman_z < 3 OR piotroski <= 3)
SORT altman_z ASC
```

## Quality high (Piotroski ≥ 7)

```dataview
TABLE piotroski, altman_z, pe, pb, dy_pct
FROM "tickers"
WHERE piotroski >= 7
SORT piotroski DESC
```

## Dividend stars (streak ≥ 15y)

```dataview
TABLE streak_years AS "Streak", dy_pct AS "DY%", div_safety AS "Safety", aristocrat
FROM "tickers"
WHERE streak_years >= 15
SORT streak_years DESC
```
"""


def _render_sector_dashboard() -> str:
    return """---
tags: [dashboard, sector]
---
# 🏢 Cobertura por Sector

```dataview
TABLE length(rows) AS "N", sum(rows.is_holding) AS "Holdings"
FROM "tickers"
GROUP BY sector
SORT length(rows) DESC
```

## Por mercado

```dataview
TABLE length(rows) AS "N", sum(rows.is_holding) AS "Holdings"
FROM "tickers"
GROUP BY market
```
"""


def _render_briefing_dashboard() -> str:
    return """---
tags: [dashboard, briefing]
---
# 📰 Daily Briefing

## Preço móveis — últimas 24h

```dataview
TABLE price, change_1d_pct AS "1d %", pnl_pct AS "P&L %"
FROM "tickers"
WHERE is_holding = true
SORT abs(change_1d_pct) DESC
LIMIT 20
```

## Holdings com eventos recentes (≤ 7d)

Manual ingest quando briefing correr. Ver ficheiro individual do ticker para eventos SEC/CVM.

## YouTube — últimos insights por canal

Ver `yt_digest.py --channel "X" --days 7` + importar manualmente.
"""


def _load_tickers_by_market() -> dict[str, list[str]]:
    out = {"br": [], "us": []}
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            for (t,) in c.execute("SELECT ticker FROM companies ORDER BY ticker"):
                out[market].append(t)
    return out


def export_vault(
    vault_path: Path,
    only_ticker: str | None = None,
    holdings_only: bool = False,
) -> dict:
    vault_path.mkdir(parents=True, exist_ok=True)
    tickers_dir = vault_path / "tickers"
    sectors_dir = vault_path / "sectors"
    markets_dir = vault_path / "markets"
    videos_dir = vault_path / "videos"
    for p in (tickers_dir, sectors_dir, markets_dir, videos_dir):
        p.mkdir(exist_ok=True)
    (vault_path / "dashboards").mkdir(exist_ok=True)

    written = 0
    skipped = 0

    # Tracking para sector/market/video aggregation
    sector_map: dict[str, list[tuple]] = {}  # sector -> [(ticker, market, is_holding)]
    market_map: dict[str, list[tuple]] = {"br": [], "us": []}
    all_video_ids: set[str] = set()

    def _process_ticker(t: str, mk: str) -> bool:
        nonlocal written, skipped
        try:
            md = _render_ticker_md(t, mk)
            (tickers_dir / f"{t}.md").write_text(md, encoding="utf-8")
            written += 1
            # collect for aggregates
            db = DB_BR if mk == "br" else DB_US
            with sqlite3.connect(db) as c:
                row = c.execute(
                    "SELECT sector, is_holding FROM companies WHERE ticker=?", (t,)
                ).fetchone()
                sector = (row[0] if row else None) or "Uncategorized"
                is_h = bool(row[1]) if row else False
                sector_map.setdefault(sector, []).append((t, mk, is_h))
                market_map[mk].append((t, mk, is_h))
                for vid in c.execute(
                    "SELECT DISTINCT video_id FROM video_insights WHERE ticker=?", (t,)
                ):
                    all_video_ids.add(vid[0])
            return True
        except Exception as e:  # noqa: BLE001
            print(f"  {t}: ERROR — {e}")
            skipped += 1
            return False

    if only_ticker:
        from scripts.refresh_ticker import _market_of
        mk = _market_of(only_ticker)
        _process_ticker(only_ticker, mk)
    else:
        for mk, tks in _load_tickers_by_market().items():
            for t in tks:
                if holdings_only:
                    db = DB_BR if mk == "br" else DB_US
                    with sqlite3.connect(db) as c:
                        r = c.execute(
                            "SELECT is_holding FROM companies WHERE ticker=?", (t,)
                        ).fetchone()
                    if not r or not r[0]:
                        skipped += 1
                        continue
                _process_ticker(t, mk)

    # Sector pages
    for sector, rows in sector_map.items():
        slug = _sector_slug(sector)
        (sectors_dir / f"{slug}.md").write_text(_render_sector_page(sector, rows), encoding="utf-8")

    # Market pages
    for mk, rows in market_map.items():
        if rows:
            (markets_dir / f"{mk.upper()}.md").write_text(_render_market_page(mk, rows), encoding="utf-8")

    # Video pages — filename legível humanamente; video_id preservado como alias.
    video_written = 0
    for vid in all_video_ids:
        md = _render_video_page(vid)
        if not md:
            continue
        # extrai published_at, channel, title do frontmatter escrito
        date_m = re.search(r"^published_at:\s*(.+)$", md, re.MULTILINE)
        chan_m = re.search(r"^channel:\s*(.+)$", md, re.MULTILINE)
        title_m = re.search(r"^#\s+🎬\s*(.+?)\s*$", md, re.MULTILINE)
        stem = _video_slug_name(
            vid,
            (date_m.group(1).strip().strip("\"'") if date_m else None),
            (chan_m.group(1).strip().strip("\"'") if chan_m else None),
            (title_m.group(1).strip() if title_m else None),
        )
        (videos_dir / f"{stem}.md").write_text(md, encoding="utf-8")
        video_written += 1

    # Dashboards
    (vault_path / "dashboards" / "Portfolio.md").write_text(_render_portfolio_dashboard(), encoding="utf-8")
    (vault_path / "dashboards" / "Sectors.md").write_text(_render_sector_dashboard(), encoding="utf-8")
    (vault_path / "dashboards" / "Briefing.md").write_text(_render_briefing_dashboard(), encoding="utf-8")

    # Top-level portfolio pages (não precisam Dataview)
    (vault_path / "My Portfolio.md").write_text(_render_my_portfolio_page(), encoding="utf-8")
    (vault_path / "Holdings.md").write_text(_render_holdings_page(), encoding="utf-8")
    (vault_path / "Allocation.md").write_text(_render_allocation_page(), encoding="utf-8")
    (vault_path / "Transactions.md").write_text(_render_transactions_page(), encoding="utf-8")

    # Index
    today_iso = date.today().isoformat()
    idx = [
        "# 🏠 Investment Intelligence Vault",
        "",
        f"_Export: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
        "## 🚀 Começa aqui",
        "- [[My Portfolio|💼 A minha carteira AGORA]] — overview + totals + holdings table",
        f"- [[briefings/{today_iso}|🌅 Morning Briefing de hoje]] — diff, moves, earnings",
        "- [[Holdings|📋 Holdings completo]] — tabela unificada BR+US em BRL",
        "- [[Allocation|📊 Alocação]] — por market/sector/concentração",
        "- [[TaxLots|📜 Tax Lots JPM]] — breakdown lote-a-lote + short/long term",
        "- [[Rebalance|🔄 Rebalance]] — drift vs target",
        "- [[Transactions|📜 Transacções]] — log entries/exits",
        "- [[wiki/Index|📚 Wiki — Finance Map]] — methods, macro, history (31 notas)",
        "",
        "## Dashboards (Dataview)",
        "- [[dashboards/Portfolio|📊 Portfolio Dashboard]]",
        "- [[dashboards/Sectors|🏢 Sectors agregado]]",
        "- [[dashboards/Briefing|📰 Daily Briefing layout]]",
        "",
        "## Markets",
        "- [[markets/BR|🇧🇷 Brazil]]",
        "- [[markets/US|🇺🇸 United States]]",
        "",
        "## Sectors",
    ]
    for sector in sorted(sector_map):
        slug = _sector_slug(sector)
        count = len(sector_map[sector])
        idx.append(f"- [[sectors/{slug}|{sector}]] ({count} tickers)")
    idx.extend([
        "",
        f"## Tickers — **{written}** exportados",
        "- Pasta: [[tickers/]]",
        "",
        f"## Videos YouTube — **{video_written}** ingeridos",
        "- Pasta: [[videos/]]",
        "",
        "## Graph View",
        "Ver ícone do canto superior esquerdo (3 bolas ligadas). Clusters emergem por sector + market + peers.",
        "",
        "## Plugins recomendados",
        "- **Dataview** ⭐ essencial (Community plugins → Browse → Dataview)",
        "- **Charts** — gráficos inline",
        "- **Templater** — snippets",
        "- **Calendar** — eventos datados",
    ])
    (vault_path / "Home.md").write_text("\n".join(idx), encoding="utf-8")

    return {
        "written": written, "skipped": skipped, "vault": str(vault_path),
        "sectors": len(sector_map), "markets": len([m for m in market_map.values() if m]),
        "videos": video_written,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vault", help="Override vault path (env OBSIDIAN_VAULT_PATH tb serve)")
    ap.add_argument("--ticker", help="Single ticker")
    ap.add_argument("--holdings-only", action="store_true")
    ap.add_argument("--refresh", action="store_true", help="Corre refresh_ticker antes")
    args = ap.parse_args()

    vp = _vault_path(args.vault)

    if args.refresh:
        print("Refreshing prices...")
        scope = "--all-holdings" if args.holdings_only or not args.ticker else args.ticker
        cmd = [sys.executable, str(ROOT / "scripts" / "refresh_ticker.py")]
        if args.ticker:
            cmd.append(args.ticker)
        else:
            cmd.append("--all-holdings")
        cmd.append("--quiet")
        subprocess.call(cmd)

    print(f"Exporting to: {vp}")
    stats = export_vault(vp, only_ticker=args.ticker, holdings_only=args.holdings_only)
    print(f"Wrote {stats['written']} ticker note(s). Skipped {stats['skipped']}.")
    print(f"Vault ready at: {stats['vault']}")
    print()
    print("Próximo passo:")
    print(f"  1. Abrir Obsidian → 'Open folder as vault' → apontar para {stats['vault']}")
    print("  2. Settings → Community plugins → Browse → install 'Dataview' → Enable")
    print("  3. Abrir dashboards/Portfolio.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
