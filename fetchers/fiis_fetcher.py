"""Fetcher primário de FIIs via fiis.com.br.

Fonte primária para métricas de FIIs. Status Invest (fii_statusinvest_scraper.py)
fica como fallback/complemento para campos ausentes.

Persiste em fii_fundamentals. Idempotente. Cache-aware.

Campos extraídos directamente:
  - price, vpa, pvp
  - dy_12m (reportado pela fonte)
  - last_monthly_rendimento
  - adtv_daily (liquidez média diária, em BRL)
  - segment_anbima, management_type

Campos derivados:
  - distribution_streak_months: meses consecutivos de distribuição
    computados a partir do histórico rendido na página.

Campos ainda n/a (sourcing futuro, provavelmente relatórios CVM):
  - physical_vacancy, financial_vacancy
  - avg_monthly_rendimento_24m (pode vir via Status Invest fallback)

Uso:
    python fetchers/fiis_fetcher.py XPML11
    python fetchers/fiis_fetcher.py XPML11 --force
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests
import yaml

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from fetchers.cache_policy import is_fresh, now_iso  # noqa: E402

ROOT = _ROOT
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

BASE = "https://fiis.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

# ---------- parsing helpers ----------

_INDICATOR_RE = re.compile(
    r'<div class="indicators__box">\s*<p>(?P<val>.*?)</p>\s*<p>(?P<label>[^<]+)</p>\s*</div>',
    re.S,
)
_ADMIN_RE = re.compile(
    r'<p>\s*<span>(?P<label>[^<]+)</span>\s*<b>(?P<val>[^<]+)</b>\s*</p>',
    re.S,
)
_PRICE_RE = re.compile(
    r'<span class="value">([^<]+)</span>\s*<div class="change">.*?Cota\S+?o atual de',
    re.S,
)
_DIV_BLOCK_MARKER = "yieldChart__table__bloco--rendimento"
_TABLE_CELL_RE = re.compile(r'<div class="table__linha">\s*([^<]*?)\s*</div>', re.S)


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "fiis_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _br_num(s: str | None) -> float | None:
    """Converte número BR com suporte a prefixo R$, sufixo %, M, B, K."""
    if s is None:
        return None
    s = unescape(s).strip()
    if s in {"", "-", "n/a", "N/A", "--"}:
        return None
    s = s.replace("R$", "").strip()
    mult = 1.0
    m = re.match(r"^(.+?)\s*([KkMmBb])\s*$", s)
    if m:
        s = m.group(1)
        suf = m.group(2).upper()
        mult = {"K": 1e3, "M": 1e6, "B": 1e9}[suf]
    pct = s.endswith("%")
    s = s.replace("%", "").strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        return None
    if pct:
        v /= 100
    return v * mult


def _parse_br_date(s: str) -> str | None:
    """`18.03.2026` ou `18/03/2026` → `2026-03-18`."""
    s = s.strip()
    m = re.match(r"^(\d{2})[./](\d{2})[./](\d{4})$", s)
    if not m:
        return None
    d, mo, y = m.groups()
    return f"{y}-{mo}-{d}"


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def _extract_indicators(html: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _INDICATOR_RE.finditer(html):
        label = unescape(re.sub(r"\s+", " ", m.group("label")).strip())
        raw = m.group("val")
        is_pct = "<small>%</small>" in raw or ">%<" in raw
        text = unescape(re.sub(r"\s+", " ", _strip_tags(raw)).strip())
        if is_pct and not text.endswith("%"):
            text += "%"
        out[label] = text
    return out


def _extract_admin(html: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _ADMIN_RE.finditer(html):
        label = unescape(re.sub(r"\s+", " ", m.group("label")).strip())
        val = unescape(re.sub(r"\s+", " ", m.group("val")).strip())
        out.setdefault(label, val)
    return out


def _extract_price(html: str) -> float | None:
    m = _PRICE_RE.search(html)
    return _br_num(m.group(1)) if m else None


def _extract_dividend_history(html: str) -> list[dict]:
    rows: list[dict] = []
    pos = 0
    while True:
        idx = html.find(_DIV_BLOCK_MARKER, pos)
        if idx < 0:
            break
        window = html[idx:idx + 1500]
        cells = [c.strip() for c in _TABLE_CELL_RE.findall(window)[:6]]
        pos = idx + len(_DIV_BLOCK_MARKER)
        if len(cells) < 6:
            continue
        kind, base, pay, close, dy, rev = cells
        base_iso = _parse_br_date(base)
        if not base_iso:
            continue
        rows.append({
            "kind": unescape(kind),
            "base_date": base_iso,
            "payment_date": _parse_br_date(pay),
            "close": _br_num(close),
            "yield": _br_num(dy),
            "revenue": _br_num(rev),
        })
    # dedupe by base_date keeping first occurrence
    seen: set[str] = set()
    uniq: list[dict] = []
    for r in rows:
        if r["base_date"] in seen:
            continue
        seen.add(r["base_date"])
        uniq.append(r)
    return sorted(uniq, key=lambda r: r["base_date"], reverse=True)


def compute_streak_months(dividends: list[dict]) -> int:
    """Meses consecutivos de distribuição, contados do mais recente para trás.

    Cada `base_date` é reduzido a `YYYY-MM`; um gap > 1 mês quebra o streak.
    """
    if not dividends:
        return 0
    months = sorted({d["base_date"][:7] for d in dividends}, reverse=True)
    streak = 1
    for i in range(1, len(months)):
        y1, m1 = map(int, months[i - 1].split("-"))
        y2, m2 = map(int, months[i].split("-"))
        if (y1 - y2) * 12 + (m1 - m2) == 1:
            streak += 1
        else:
            break
    return streak


# ---------- universe / DB ----------

def load_fii_entry(ticker: str) -> dict | None:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    br = data.get("br", {}) or {}
    pools: list[dict] = []
    pools.extend((br.get("holdings") or {}).get("fiis", []) or [])
    pools.extend((br.get("watchlist") or {}).get("fiis", []) or [])
    for entry in pools:
        if entry["ticker"] == ticker:
            return entry
    return None


def upsert_company(conn: sqlite3.Connection, entry: dict) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, ?, 'BRL')
           ON CONFLICT(ticker) DO UPDATE SET
             name=excluded.name, sector=excluded.sector, is_holding=excluded.is_holding""",
        (
            entry["ticker"],
            entry["name"],
            entry.get("segment") or entry.get("sector"),
            1 if entry.get("is_holding") else 0,
        ),
    )


def upsert_fii_fundamentals(conn: sqlite3.Connection, ticker: str, fields: dict) -> str:
    period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO fii_fundamentals
             (ticker, period_end, price, vpa, pvp, dy_12m,
              last_monthly_rendimento, avg_monthly_rendimento_24m,
              physical_vacancy, financial_vacancy, adtv_daily,
              distribution_streak_months, segment_anbima, management_type,
              source, fetched_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             price=excluded.price, vpa=excluded.vpa, pvp=excluded.pvp,
             dy_12m=excluded.dy_12m,
             last_monthly_rendimento=excluded.last_monthly_rendimento,
             avg_monthly_rendimento_24m=COALESCE(excluded.avg_monthly_rendimento_24m, fii_fundamentals.avg_monthly_rendimento_24m),
             adtv_daily=excluded.adtv_daily,
             distribution_streak_months=excluded.distribution_streak_months,
             segment_anbima=excluded.segment_anbima,
             management_type=excluded.management_type,
             source=excluded.source,
             fetched_at=excluded.fetched_at""",
        (
            ticker, period,
            fields.get("price"), fields.get("vpa"), fields.get("pvp"),
            fields.get("dy_12m"),
            fields.get("last_monthly_rendimento"),
            fields.get("avg_monthly_rendimento_24m"),
            None, None,  # vacancy — sourcing futuro
            fields.get("adtv_daily"),
            fields.get("distribution_streak_months"),
            fields.get("segment_anbima"), fields.get("management_type"),
            "fiis.com.br", now_iso(),
        ),
    )
    return period


# ---------- orchestration ----------

def fetch_html(ticker: str) -> tuple[int, str]:
    url = f"{BASE}/{ticker.lower()}/"
    r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
    return r.status_code, r.text


def parse_page(html: str) -> dict:
    indic = _extract_indicators(html)
    admin = _extract_admin(html)
    price = _extract_price(html)
    divs = _extract_dividend_history(html)

    vpa = _br_num(indic.get("Val. Patrimonial p/Cota"))
    pvp = _br_num(indic.get("P/VP"))
    dy_12m = _br_num(indic.get("Dividend Yield"))
    last_rend = _br_num(indic.get("Último Rendimento"))
    adtv = _br_num(indic.get("Liquidez média diária"))

    segment = admin.get("Segmento ANBIMA") or admin.get("Segmento")
    mgmt = admin.get("Tipo de Gestão")

    # fallback: derive price from pvp * vpa if primary extractor missed
    if price is None and pvp and vpa:
        price = round(pvp * vpa, 2)

    return {
        "price": price,
        "vpa": vpa,
        "pvp": pvp,
        "dy_12m": dy_12m,
        "last_monthly_rendimento": last_rend,
        "adtv_daily": adtv,
        "avg_monthly_rendimento_24m": None,  # preenchido por fallback SI
        "segment_anbima": segment,
        "management_type": mgmt,
        "distribution_streak_months": compute_streak_months(divs),
        "_dividend_count": len(divs),
    }


def _fetch_from_statusinvest(ticker: str) -> dict | None:
    """Fallback: usa fii_statusinvest_scraper para extrair métricas quando
    fiis.com.br falhar. Devolve dict compatível com upsert_fii_fundamentals."""
    try:
        from fetchers.fii_statusinvest_scraper import fetch_indicators, parse_fii
    except Exception as e:
        _log({"event": "fii_fallback_import_error", "ticker": ticker, "error": str(e)})
        return None
    try:
        pairs = fetch_indicators(ticker)
    except Exception as e:
        _log({"event": "fii_fallback_http_error", "ticker": ticker, "error": str(e)})
        return None
    si = parse_fii(pairs)
    if si.get("price") is None and si.get("vpa") is None:
        return None
    return {
        "price": si.get("price"),
        "vpa": si.get("vpa"),
        "pvp": si.get("pvp"),
        "dy_12m": si.get("dy_12m"),
        "last_monthly_rendimento": None,
        "adtv_daily": None,
        "avg_monthly_rendimento_24m": si.get("avg_monthly_rendimento_24m"),
        "segment_anbima": si.get("segment_anbima"),
        "management_type": None,
        "distribution_streak_months": None,
        "_dividend_count": 0,
        "_source": "statusinvest",
    }


def _persist(ticker: str, entry: dict, fields: dict, source: str) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        upsert_company(conn, entry)
        period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        conn.execute(
            """INSERT INTO fii_fundamentals
                 (ticker, period_end, price, vpa, pvp, dy_12m,
                  last_monthly_rendimento, avg_monthly_rendimento_24m,
                  physical_vacancy, financial_vacancy, adtv_daily,
                  distribution_streak_months, segment_anbima, management_type,
                  source, fetched_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(ticker, period_end) DO UPDATE SET
                 price=excluded.price, vpa=excluded.vpa, pvp=excluded.pvp,
                 dy_12m=excluded.dy_12m,
                 last_monthly_rendimento=COALESCE(excluded.last_monthly_rendimento, fii_fundamentals.last_monthly_rendimento),
                 avg_monthly_rendimento_24m=COALESCE(excluded.avg_monthly_rendimento_24m, fii_fundamentals.avg_monthly_rendimento_24m),
                 adtv_daily=COALESCE(excluded.adtv_daily, fii_fundamentals.adtv_daily),
                 distribution_streak_months=COALESCE(excluded.distribution_streak_months, fii_fundamentals.distribution_streak_months),
                 segment_anbima=excluded.segment_anbima,
                 management_type=COALESCE(excluded.management_type, fii_fundamentals.management_type),
                 source=excluded.source,
                 fetched_at=excluded.fetched_at""",
            (
                ticker, period,
                fields.get("price"), fields.get("vpa"), fields.get("pvp"),
                fields.get("dy_12m"),
                fields.get("last_monthly_rendimento"),
                fields.get("avg_monthly_rendimento_24m"),
                None, None,
                fields.get("adtv_daily"),
                fields.get("distribution_streak_months"),
                fields.get("segment_anbima"), fields.get("management_type"),
                source, now_iso(),
            ),
        )
        conn.commit()
    return period


def run(ticker: str, force: bool = False) -> dict | None:
    entry = load_fii_entry(ticker)
    if entry is None:
        raise SystemExit(f"{ticker} não é um FII conhecido em universe.yaml")

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT fetched_at, source FROM fii_fundamentals WHERE ticker=? "
            "ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
    if not force and row and is_fresh(row[0], "fundamental_snapshot"):
        _log({"event": "fii_fetch_skip_fresh", "ticker": ticker, "fetched_at": row[0], "source": row[1]})
        return None

    _log({"event": "fii_fetch_start", "ticker": ticker})
    fields: dict | None = None
    source = "fiis.com.br"

    status, html = fetch_html(ticker)
    if status == 200:
        candidate = parse_page(html)
        # detectar redirect implícito (página de notícia sem indicadores)
        if candidate["price"] is not None or candidate["vpa"] is not None:
            fields = candidate
        else:
            _log({"event": "fii_fetch_parse_empty_primary", "ticker": ticker})
    else:
        _log({"event": "fii_fetch_primary_http", "ticker": ticker, "status": status})

    if fields is None:
        _log({"event": "fii_fetch_fallback_statusinvest", "ticker": ticker})
        fb = _fetch_from_statusinvest(ticker)
        if fb is not None:
            fields = fb
            source = "statusinvest"

    if fields is None:
        _log({"event": "fii_fetch_failed", "ticker": ticker})
        return None

    period = _persist(ticker, entry, fields, source)
    log_fields = {k: v for k, v in fields.items() if not k.startswith("_")}
    _log({
        "event": "fii_fetched",
        "ticker": ticker,
        "period": period,
        "source": source,
        "dividends_parsed": fields.get("_dividend_count", 0),
        "fields": log_fields,
    })
    return fields


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="XPML11")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    run(args.ticker.upper(), force=args.force)


if __name__ == "__main__":
    main()
