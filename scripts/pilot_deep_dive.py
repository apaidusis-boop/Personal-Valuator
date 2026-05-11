"""Pilot Deep Dive — Phase MCP-5 validation.

For each pilot ticker:
  1. Snapshot DB state (events, fundamentals, prices, scores)
  2. Scrape RI homepage via portal_playwright + markitdown
  3. Parse filings list, calendar, presentations from RI markdown
  4. Detect novel filings (newer than DB or not in DB)
  5. Download top novel filings, extract via markitdown
  6. Compose dossier .md with before/after diff table
  7. Aggregate master report

Idempotent: re-runs use Playwright cache (24h). Each ticker is independent —
failures don't abort the run.

Output: obsidian_vault/Pilot_Deep_Dive_<DATE>/
  - _MASTER.md            global comparative report
  - <TICKER>.md           per-ticker dossier

Usage:
    python scripts/pilot_deep_dive.py                    # default pilot 5
    python scripts/pilot_deep_dive.py --tickers ITSA4    # one ticker
    python scripts/pilot_deep_dive.py --no-download      # skip filing downloads
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from library._md_extract import extract_text  # noqa: E402

TODAY = datetime.now().strftime("%Y-%m-%d")
# Allow override of output dir via env (overnight uses a different dir)
OUT_DIR_ENV = os.environ.get("PILOT_OUT_DIR")
OUT_DIR = (Path(OUT_DIR_ENV) if OUT_DIR_ENV
           else ROOT / "obsidian_vault" / f"Pilot_Deep_Dive_{TODAY}")
LOG_PATH = ROOT / "logs" / f"pilot_deep_dive_{TODAY}.log"
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")
RI_URLS_YAML = Path(os.environ.get("RI_URLS_YAML",
                                    str(ROOT / "config" / "ri_urls.yaml")))

# ---------------------------------------------------------------------------
# Pilot configuration
# ---------------------------------------------------------------------------

PILOT = [
    {"ticker": "ITSA4", "market": "br",
     "ri_urls": ["https://ri.itausa.com.br/"],
     "sector": "Holding",
     "rationale": "Baseline tested today (Mz Group provider)"},
    {"ticker": "BBDC4", "market": "br",
     "ri_urls": ["https://www.bradescori.com.br/",
                 "https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fatos-relevantes/"],
     "sector": "Bank",
     "rationale": "Bradesco own RI (different provider)"},
    {"ticker": "PRIO3", "market": "br",
     "ri_urls": ["https://ri.prio3.com.br/",
                 "https://ri.prio3.com.br/servicos-aos-investidores/comunicados-e-fatos-relevantes/"],
     "sector": "Oil & Gas",
     "rationale": "Commodity, Mz Group provider"},
    {"ticker": "JPM", "market": "us",
     "ri_urls": ["https://www.jpmorganchase.com/ir",
                 "https://www.jpmorganchase.com/ir/news",
                 "https://www.jpmorganchase.com/ir/quarterly-earnings"],
     "sector": "Bank",
     "rationale": "Large US corporate IR (multi-page)"},
    {"ticker": "JNJ", "market": "us",
     "ri_urls": ["https://www.investor.jnj.com/"],
     "sector": "Healthcare",
     "rationale": "Classic US dividend aristocrat IR"},
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


# ---------------------------------------------------------------------------
# DB snapshot (BEFORE state)
# ---------------------------------------------------------------------------

def db_path(market: str) -> Path:
    return ROOT / "data" / f"{market}_investments.db"


def snapshot_db(ticker: str, market: str) -> dict:
    """Capture current DB state for the ticker."""
    snap = {
        "events_count": 0,
        "events_recent": [],
        "fundamentals_latest": None,
        "prices_latest": None,
        "score_latest": None,
        "thesis_health": None,
        "portfolio_position": None,
        "deep_fundamentals_count": 0,
    }
    db = db_path(market)
    if not db.exists():
        return snap
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    try:
        # Events
        snap["events_count"] = c.execute(
            "SELECT COUNT(*) FROM events WHERE ticker=?", (ticker,)
        ).fetchone()[0]
        recent = c.execute(
            "SELECT event_date, kind, source, substr(summary,1,140) as summary "
            "FROM events WHERE ticker=? ORDER BY event_date DESC LIMIT 5",
            (ticker,),
        ).fetchall()
        snap["events_recent"] = [dict(r) for r in recent]

        # Fundamentals (last quarter)
        try:
            fund = c.execute(
                "SELECT period_end, eps, bvps, roe, pe, pb, dy, "
                "net_debt_ebitda, dividend_streak_years, is_aristocrat "
                "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            snap["fundamentals_latest"] = dict(fund) if fund else None
        except sqlite3.OperationalError:
            pass

        # Prices
        try:
            price = c.execute(
                "SELECT date, close, volume FROM prices "
                "WHERE ticker=? ORDER BY date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            snap["prices_latest"] = dict(price) if price else None
        except sqlite3.OperationalError:
            pass

        # Score
        try:
            score = c.execute(
                "SELECT run_date, score, passes_screen FROM scores "
                "WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            snap["score_latest"] = dict(score) if score else None
        except sqlite3.OperationalError:
            pass

        # Thesis health
        try:
            th = c.execute(
                "SELECT * FROM thesis_health WHERE ticker=? "
                "ORDER BY run_date DESC LIMIT 1",
                (ticker,),
            ).fetchone()
            snap["thesis_health"] = dict(th) if th else None
        except sqlite3.OperationalError:
            pass

        # Portfolio position
        try:
            pos = c.execute(
                "SELECT quantity, entry_price, entry_date FROM portfolio_positions "
                "WHERE ticker=? AND active=1 LIMIT 1",
                (ticker,),
            ).fetchone()
            snap["portfolio_position"] = dict(pos) if pos else None
        except sqlite3.OperationalError:
            pass

        # Deep fundamentals (annual rows)
        try:
            n = c.execute(
                "SELECT COUNT(*) FROM deep_fundamentals WHERE ticker=?",
                (ticker,),
            ).fetchone()[0]
            snap["deep_fundamentals_count"] = n
        except sqlite3.OperationalError:
            pass
    finally:
        c.close()
    return snap


# ---------------------------------------------------------------------------
# RI scrape
# ---------------------------------------------------------------------------

def scrape_ri(url: str, ticker: str, force_fresh: bool = False) -> dict:
    """Run portal_playwright as subprocess. Returns parsed result dict."""
    cmd = [
        PYTHON,
        str(ROOT / "fetchers" / "portal_playwright.py"),
        url, "--md",
    ]
    if force_fresh:
        cmd += ["--ttl", "0"]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        elapsed = time.time() - t0
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout 120s", "elapsed_s": 120}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "elapsed_s": time.time() - t0}

    if r.returncode != 0:
        return {"ok": False, "error": (r.stderr or "")[:400],
                "elapsed_s": elapsed}

    # portal_playwright prints a pretty-printed JSON object to stdout
    text = (r.stdout or "").strip()
    parsed = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # fall back: find last balanced { ... } block
        for start in range(len(text)):
            if text[start] == "{":
                try:
                    parsed = json.loads(text[start:])
                    break
                except json.JSONDecodeError:
                    continue
    if not parsed:
        return {"ok": False, "error": "no JSON in stdout",
                "elapsed_s": elapsed, "stdout_tail": text[-300:]}

    # Prefer Playwright's own elapsed_s (real network/render time);
    # fall back to subprocess time if Playwright didn't report it.
    parsed["subprocess_elapsed_s"] = elapsed
    if "elapsed_s" not in parsed:
        parsed["elapsed_s"] = elapsed
    parsed["ok"] = parsed.get("status") == 200
    return parsed


# ---------------------------------------------------------------------------
# RI content parser (heuristics — works on Mz Group RI; degrades gracefully)
# ---------------------------------------------------------------------------

DATE_PT_RE = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
DATE_ISO_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
DATE_DASH_RE = re.compile(r"\b(\d{2}-\d{2}-\d{4})\b")  # DD-MM-YYYY (Bradesco)
DATE_EN_RE = re.compile(
    r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+"
    r"\d{1,2},?\s+\d{4})\b", re.IGNORECASE,
)
# Match [title](url) or [title](url "tooltip"). Accept absolute (http/https)
# OR relative (/path). Negative lookbehind (?<!!) excludes images ![alt](url).
LINK_RE = re.compile(
    r"(?<!!)\[([^\]]+)\]"
    r"\(((?:https?://|/)[^)\s]+)"
    r"(?:\s+\"[^\"]*\")?\)"
)


def _absolutize(url: str, base: str) -> str:
    """Make relative URL absolute given base URL."""
    if url.startswith(("http://", "https://")):
        return url
    if not base:
        return url
    # Strip trailing path from base, keep scheme+host
    from urllib.parse import urlparse
    p = urlparse(base)
    return f"{p.scheme}://{p.netloc}{url}"
MD_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

_EN_MONTHS = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05",
    "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10",
    "nov": "11", "dec": "12",
}


def _any_date_match(text: str):
    """Find first date of any format. Returns (raw, iso) or (None, None)."""
    m = DATE_PT_RE.search(text)
    if m:
        return m.group(1), _to_iso(m.group(1))
    m = DATE_ISO_RE.search(text)
    if m:
        return m.group(1), m.group(1)
    m = DATE_DASH_RE.search(text)
    if m:
        return m.group(1), _dash_to_iso(m.group(1))
    m = DATE_EN_RE.search(text)
    if m:
        return m.group(1), _en_to_iso(m.group(1))
    return None, None


def _any_date_fullmatch(text: str):
    """Check if text is exactly a date. Return iso or None."""
    s = text.strip()
    if DATE_PT_RE.fullmatch(s):
        return _to_iso(s)
    if DATE_ISO_RE.fullmatch(s):
        return s
    if DATE_DASH_RE.fullmatch(s):
        return _dash_to_iso(s)
    if DATE_EN_RE.fullmatch(s):
        return _en_to_iso(s)
    return None


def _dash_to_iso(s: str) -> str:
    """'30-04-2026' -> '2026-04-30'. Assumes DD-MM-YYYY."""
    parts = s.split("-")
    if len(parts) != 3 or len(parts[2]) != 4:
        return s
    return f"{parts[2]}-{parts[1]}-{parts[0]}"


def _en_to_iso(s: str) -> str:
    """'May 19, 2026' -> '2026-05-19'."""
    s = s.replace(",", "").strip()
    parts = s.split()
    if len(parts) != 3:
        return s
    mon = parts[0][:3].lower()
    if mon not in _EN_MONTHS:
        return s
    day = parts[1].zfill(2)
    year = parts[2]
    return f"{year}-{_EN_MONTHS[mon]}-{day}"


SECTION_HINT_EVENTS = ("próximos eventos", "proximos eventos", "calendário",
                        "calendar", "agenda", "upcoming events")
SECTION_HINT_FILINGS = ("destaques", "fato relevante", "comunicado",
                         "avisos", "filings", "press releases", "news",
                         "investor news", "latest news")
SECTION_HINT_PRES = ("apresentaç", "presentation", "central de resultados",
                      "quarterly", "earnings")

NAV_SKIP_KEYWORDS = (
    "ver tudo", "saiba mais", "acesse aqui", "inscreva-se", "view all",
    "mapa do site", "fale com", "português", "english", "skip to",
    "cadastre-se", "termos", "termo de", "linkedin", "twitter", "facebook",
    "join our team", "search ", "back to",
)

# CTA-only link texts — title lives in a nearby heading (handled by 2nd pass).
# In first pass, these should not produce filing entries on their own.
CTA_LINK_TEXTS = {
    "learn more", "read more", "view document", "view more",
    "read the report", "read article", "view all", "view",
    "saiba mais", "ver mais", "leia mais", "acesse aqui",
}

FILING_TITLE_KEYWORDS = (
    "fato relevante", "comunicado", "aviso", "8-k", "10-k", "10-q",
    "press release", "release", "earnings", "form ", "annual report",
    "proxy", "dividend", "shareholder", "presents", "to present",
)


def parse_ri_content(md: str, base_url: str = "") -> dict:
    """Extract filings, events, presentations, headers from RI markdown.

    Robust to BR (Mz Group) and US layouts. For each link, looks at a
    proximity window (3 lines before/after) for date and section context.

    base_url is used to convert relative URLs (e.g. /ir/news/...) to absolute.
    """
    res = {
        "headers": [],
        "filings": [],
        "events": [],
        "presentations": [],
        "audio_video": [],
        "analyst_coverage_links": [],
        "raw_chars": len(md),
    }
    if not md:
        return res

    for m in MD_HEADER_RE.finditer(md):
        res["headers"].append({"level": len(m.group(1)), "text": m.group(2).strip()})

    lines = md.splitlines()
    n = len(lines)

    # Pre-compute section context per line index
    # walking forward, current section (latest H1/H2/H3 seen)
    line_section: list[str] = [""] * n
    current_section = ""
    for i, ln in enumerate(lines):
        m = re.match(r"^#{1,6}\s+(.+)$", ln)
        if m:
            current_section = m.group(1).strip().lower()
        line_section[i] = current_section

    def in_section(idx: int, hints: tuple) -> bool:
        s = line_section[idx]
        return any(h in s for h in hints)

    def proximity_date(idx: int, window: int = 3):
        """Search the current line first, then expand outward (1 line at a time)
        to a max +/- window. Returns (raw, iso) or (None, None).
        Same-line date always wins over neighbour-line date.
        """
        # 1) same line
        same = _any_date_match(lines[idx])
        if same[0]:
            return same
        # 2) expand symmetrically
        for w in range(1, window + 1):
            for j in (idx - w, idx + w):
                if 0 <= j < n:
                    res = _any_date_match(lines[j])
                    if res[0]:
                        return res
        return None, None

    # Iterate links
    seen_urls = set()
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        # Calendar events without link: under events section, line follows date
        if in_section(i, SECTION_HINT_EVENTS):
            iso_full = _any_date_fullmatch(stripped.lstrip("*- ").strip())
            if iso_full:
                # Look for next non-empty line (the event title)
                for j in range(i + 1, min(n, i + 4)):
                    nxt = lines[j].strip().lstrip("*- ").strip()
                    if not nxt:
                        continue
                    if (not LINK_RE.search(nxt) and
                        not nxt.startswith(("[", "!", "http", "(")) and
                        not _any_date_fullmatch(nxt)):
                        res["events"].append({
                            "date": iso_full[:10] if len(iso_full) == 10 else iso_full,
                            "iso_date": iso_full,
                            "title": nxt[:120],
                        })
                        break
                    break

        # Links — main extraction
        for lm in LINK_RE.finditer(stripped):
            title = lm.group(1).strip()
            url = _absolutize(lm.group(2).strip(), base_url)
            tlow = title.lower()
            ulow = url.lower()

            if url in seen_urls:
                continue
            # Skip nav/menu/pure UI
            if any(skip in tlow for skip in NAV_SKIP_KEYWORDS):
                continue
            # CTA-only links: defer to 2nd pass (title comes from heading)
            if tlow in CTA_LINK_TEXTS:
                continue
            if title in ("pt", "en", ""):
                continue
            if title.startswith("![") or len(title) < 3:
                continue

            # Find date in proximity (within 3 lines)
            raw_date, iso_date = proximity_date(i, window=3)

            # Determine category
            is_filing_section = in_section(i, SECTION_HINT_FILINGS)
            looks_filing = (iso_date and (
                is_filing_section
                or any(kw in tlow for kw in FILING_TITLE_KEYWORDS)
                # JPM news layout: title appears as H2/H3 above link, also contains keywords
            ))

            looks_audio_video = any(kw in tlow for kw in (
                "cast", "podcast", "videoconfer", "webcast", "teleconfer",
                "conference call",
            ))

            looks_presentation = (
                any(kw in tlow for kw in (
                    "apresenta", "presentation", "demonstra", "relat",
                    "supplement", "earnings presentation", "transcript",
                )) or
                any(kw in ulow for kw in (
                    "/apresentac", "/presentation", ".pptx",
                    "earnings-presentation", "presentation.pdf",
                ))
                or (".pdf" in ulow and any(kw in tlow for kw in (
                    "release", "earnings", "report", "results", "review",
                )))
            )

            looks_analyst = "analista" in tlow or "analyst" in tlow

            # Clean title (strip leftover markdown markers)
            clean_title = title
            for prefix in ("### ", "## ", "# ", "**"):
                if clean_title.startswith(prefix):
                    clean_title = clean_title[len(prefix):].strip()
            clean_title = clean_title.replace("**", "").strip()

            if looks_filing:
                res["filings"].append({
                    "date": raw_date, "iso_date": iso_date,
                    "title": clean_title, "url": url,
                })
                seen_urls.add(url)
            elif looks_audio_video:
                res["audio_video"].append({"title": clean_title, "url": url})
                seen_urls.add(url)
            elif looks_presentation:
                res["presentations"].append({"title": clean_title, "url": url})
                seen_urls.add(url)
            elif looks_analyst:
                res["analyst_coverage_links"].append({"title": title, "url": url})
                seen_urls.add(url)

    # JPM/JNJ pattern: H2/H3 title + date line + link line (3 separate)
    # Re-scan for groups of (heading, date, link) within 4 lines window
    for i, ln in enumerate(lines):
        m = re.match(r"^\s*\*?\s*#{2,4}\s+(.+)$", ln)
        if not m:
            continue
        candidate_title = m.group(1).strip()
        # Skip if title is just a section header
        if any(h in candidate_title.lower() for h in
               ("investor relations", "news & updates", "menu", "navigation")):
            continue
        # Look ahead 5 lines for date + link
        date_iso = None
        link_url = None
        for j in range(i + 1, min(n, i + 8)):
            nxt = lines[j].strip()
            if not date_iso:
                _, date_iso = _any_date_match(nxt)
            for lm in LINK_RE.finditer(nxt):
                t = lm.group(1).strip().lower()
                # CTA-style links count as the entry's link (do NOT skip them)
                raw_url = lm.group(2).strip()
                abs_url = _absolutize(raw_url, base_url)
                if t in ("learn more", "read more", "view document",
                         "view more", "read the report", "read article",
                         "view all", "view"):
                    link_url = abs_url
                    break
                # Skip pure nav menus (everything else)
                if any(skip in t for skip in NAV_SKIP_KEYWORDS):
                    continue
                if not link_url:
                    link_url = abs_url
            if date_iso and link_url:
                break
        if date_iso and link_url and link_url not in seen_urls:
            tlow = candidate_title.lower()
            looks_filing = any(kw in tlow for kw in FILING_TITLE_KEYWORDS)
            if looks_filing or in_section(i, SECTION_HINT_FILINGS):
                res["filings"].append({
                    "date": date_iso, "iso_date": date_iso,
                    "title": candidate_title, "url": link_url,
                })
                seen_urls.add(link_url)

    # Dedupe
    res["filings"] = _dedupe(res["filings"],
                             key=lambda x: (x.get("iso_date", x.get("date", "")),
                                            x["title"][:40]))
    res["events"] = _dedupe(res["events"],
                            key=lambda x: (x["date"], x["title"][:40]))
    res["presentations"] = _dedupe(res["presentations"], key=lambda x: x["url"])
    res["audio_video"] = _dedupe(res["audio_video"], key=lambda x: x["url"])
    return res


def _dedupe(items, key):
    seen = set()
    out = []
    for it in items:
        k = key(it)
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out


# ---------------------------------------------------------------------------
# Novelty detection
# ---------------------------------------------------------------------------

def _to_iso(s: str) -> str:
    """Convert dd/mm/yyyy or yyyy-mm-dd to ISO."""
    if not s:
        return ""
    if "/" in s:
        try:
            d, m, y = s.split("/")
            return f"{y}-{m}-{d}"
        except ValueError:
            return s
    return s


_STOPWORDS = {
    "fato", "relevante", "comunicado", "aviso", "mercado", "ao", "aos",
    "acionistas", "outros", "nao", "considerados", "fatos", "relevantes",
    "the", "of", "to", "and", "for", "press", "release", "form",
    "de", "da", "do", "das", "dos", "para", "com", "em", "na", "no",
    "uma", "um", "e", "ou", "que",
}


def _content_tokens(s: str) -> set:
    """Lowercase, strip punctuation, drop stopwords/short tokens.
    Returns set of meaningful content words.
    """
    if not s:
        return set()
    import unicodedata
    s = s.lower()
    # Strip accents via NFKD normalization
    s = "".join(c for c in unicodedata.normalize("NFKD", s)
                if not unicodedata.combining(c))
    for ch in "|·.,;:()[]{}\"'-_/\\":
        s = s.replace(ch, " ")
    toks = {t for t in s.split() if len(t) >= 4 and t not in _STOPWORDS}
    return toks


def detect_novel_filings(filings: list[dict], db_events: list[dict]) -> list[dict]:
    """Filings considered novel if NO DB event on the same date shares
    >=2 content tokens (or >=50% of the smaller set).
    Plus 'after max DB date' tag for high-confidence new ones.
    """
    if not filings:
        return []
    db_dates = [_to_iso(e.get("event_date", ""))
                for e in db_events if e.get("event_date")]
    db_dates = [d for d in db_dates if d]
    max_db = max(db_dates) if db_dates else "1900-01-01"
    # Build {iso_date: [token_set, ...]} from DB summaries
    db_tokens_by_date: dict[str, list[set]] = {}
    for e in db_events:
        iso = _to_iso(e.get("event_date", ""))
        if not iso:
            continue
        toks = _content_tokens(e.get("summary", ""))
        db_tokens_by_date.setdefault(iso, []).append(toks)
    novel = []
    for f in filings:
        iso = _to_iso(f["date"])
        if not iso or len(iso) != 10:
            continue
        ri_toks = _content_tokens(f["title"])
        # Match against any DB event on same date
        is_dup = False
        for db_toks in db_tokens_by_date.get(iso, []):
            if not db_toks or not ri_toks:
                continue
            shared = ri_toks & db_toks
            min_size = min(len(ri_toks), len(db_toks))
            if len(shared) >= 2 or (min_size >= 1 and len(shared) / min_size >= 0.5):
                is_dup = True
                break
        if is_dup:
            continue
        is_after = iso > max_db
        novel.append({**f, "iso_date": iso, "after_db_max": is_after})
    novel.sort(key=lambda x: x["iso_date"], reverse=True)
    return novel


# ---------------------------------------------------------------------------
# Filing download + extract
# ---------------------------------------------------------------------------

def download_filing(url: str, target: Path, timeout: int = 60) -> bool:
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0",
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(r.content)
        return True
    except Exception as e:  # noqa: BLE001
        _log({"event": "download_fail", "url": url[:120], "err": str(e)[:200]})
        return False


def extract_filing(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return extract_text(path, engine="markitdown")
    except Exception as e:  # noqa: BLE001
        _log({"event": "extract_fail", "path": str(path), "err": str(e)[:200]})
        return ""


# ---------------------------------------------------------------------------
# Dossier composer
# ---------------------------------------------------------------------------

def _esc_pipe(s) -> str:
    """Escape | in cell content so markdown table doesn't break."""
    return str(s).replace("|", "\\|").replace("\n", " ")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    line_h = "| " + " | ".join(_esc_pipe(h) for h in headers) + " |"
    line_sep = "|" + "|".join(["---"] * len(headers)) + "|"
    out = [line_h, line_sep]
    for r in rows:
        out.append("| " + " | ".join(_esc_pipe(c) for c in r) + " |")
    return "\n".join(out)


def compose_dossier(cfg: dict, before: dict, scrape: dict, parsed: dict,
                    novel: list[dict], extracted: list[dict]) -> str:
    ticker, market = cfg["ticker"], cfg["market"].upper()
    lines: list[str] = []

    lines.append(f"# {ticker} — Pilot Deep Dive ({TODAY})")
    lines.append("")
    lines.append(f"- **Market**: {market}")
    lines.append(f"- **Sector**: {cfg.get('sector', '-')}")
    urls = cfg.get("ri_urls") or [cfg.get("ri_url", "-")]
    lines.append(f"- **RI URLs scraped** ({len(urls)}):")
    for u in urls:
        lines.append(f"  - {u}")
    lines.append(f"- **Pilot rationale**: {cfg.get('rationale', '-')}")
    lines.append("")

    # ---- ANTES ----
    lines.append("## Antes (estado da DB)")
    lines.append("")
    pos = before.get("portfolio_position") or {}
    if pos:
        lines.append(f"**Posição activa**: qty={pos.get('quantity')} · "
                     f"entry={pos.get('entry_price')} · "
                     f"date={pos.get('entry_date')}")
    else:
        lines.append("**Posição activa**: (nenhuma — watchlist ou holding sem qty)")
    lines.append("")
    lines.append(f"- Total events na DB: **{before.get('events_count', 0)}**")
    lines.append(f"- deep_fundamentals (rows anuais): "
                 f"**{before.get('deep_fundamentals_count', 0)}**")
    pl = before.get("prices_latest") or {}
    fl = before.get("fundamentals_latest") or {}
    sc = before.get("score_latest") or {}
    th = before.get("thesis_health") or {}
    if pl:
        lines.append(f"- Última cotação DB: {pl.get('date')} → close="
                     f"{pl.get('close')}")
    if fl:
        lines.append(f"- Último fundamentals snapshot: period_end="
                     f"{fl.get('period_end')} · ROE={fl.get('roe')} · "
                     f"DY={fl.get('dy')} · P/E={fl.get('pe')}")
    if sc:
        lines.append(f"- Score (último run): score={sc.get('score')} · "
                     f"passes_screen={sc.get('passes_screen')}")
    if th:
        lines.append(f"- Thesis health: status={th.get('status', '-')} "
                     f"({th.get('reason', '-')[:120]})")
    lines.append("")
    lines.append("**Últimos 5 events em DB**:")
    lines.append("")
    if before.get("events_recent"):
        rows = [[e.get("event_date", "-"), e.get("kind", "-"),
                 e.get("source", "-"), (e.get("summary") or "-")[:80]]
                for e in before["events_recent"]]
        lines.append(md_table(["Data", "Kind", "Source", "Summary"], rows))
    else:
        lines.append("_(zero events em DB)_")
    lines.append("")

    # ---- AGORA ----
    lines.append("## Agora (RI scrape live)")
    lines.append("")
    if scrape.get("ok"):
        all_urls = scrape.get("all_urls", [])
        if all_urls:
            ok_count = sum(1 for u in all_urls if u.get("ok"))
            lines.append(f"- Scrape: ✅ **{ok_count}/{len(all_urls)} URLs OK** · "
                         f"total {scrape.get('elapsed_s', 0):.1f}s")
            lines.append("")
            rows = [[u["url"][:70], "✅" if u.get("ok") else "❌",
                     f"{u.get('elapsed_s', 0):.1f}s",
                     f"{u.get('md_chars', 0):,}" if u.get("md_chars") else "-"]
                    for u in all_urls]
            lines.append(md_table(["URL", "OK", "Time", "MD chars"], rows))
        else:
            lines.append(f"- Scrape: ✅ {scrape.get('elapsed_s', 0):.1f}s · "
                         f"HTML {scrape.get('html_chars', 0):,} chars · "
                         f"MD {scrape.get('md_chars', 0):,} chars")
    else:
        lines.append(f"- Scrape: ❌ FALHOU — {scrape.get('error', 'unknown')}")
        lines.append("")
        return "\n".join(lines)
    lines.append(f"- Filings extraídos do RI: **{len(parsed['filings'])}**")
    lines.append(f"- Eventos calendário: **{len(parsed['events'])}**")
    lines.append(f"- Apresentações/releases: **{len(parsed['presentations'])}**")
    lines.append(f"- Audio/video: **{len(parsed['audio_video'])}**")
    lines.append(f"- Headers detectados (structure): "
                 f"**{len(parsed['headers'])}**")
    lines.append("")

    # Filings list (top 10)
    lines.append("### Filings detectados no RI (top 10)")
    lines.append("")
    if parsed["filings"]:
        rows = [[f["date"], f["title"][:80]] for f in parsed["filings"][:10]]
        lines.append(md_table(["Data", "Título"], rows))
    else:
        lines.append("_(nenhum filing parseado — heuristic falhou ou layout diferente)_")
    lines.append("")

    # Calendar
    lines.append("### Próximos eventos (calendário RI)")
    lines.append("")
    if parsed["events"]:
        rows = [[e["date"], e["title"][:80]] for e in parsed["events"][:10]]
        lines.append(md_table(["Data", "Evento"], rows))
    else:
        lines.append("_(nenhum evento de calendário detectado)_")
    lines.append("")

    # Presentations (capped + count overflow note)
    if parsed["presentations"]:
        n_pres = len(parsed["presentations"])
        cap = 12
        lines.append(f"### Apresentações / releases disponíveis "
                     f"({n_pres} total, top {min(cap, n_pres)})")
        lines.append("")
        for p in parsed["presentations"][:cap]:
            lines.append(f"- [{p['title'][:80]}]({p['url']})")
        if n_pres > cap:
            lines.append(f"- _… e mais {n_pres - cap} no MD raw "
                         f"(`data/portal_cache/`)_")
        lines.append("")

    # Audio/video
    if parsed["audio_video"]:
        lines.append("### Audio / Video disponível (markitdown pode ler)")
        lines.append("")
        for a in parsed["audio_video"][:5]:
            lines.append(f"- [{a['title'][:80]}]({a['url']})")
        lines.append("")

    # ---- DIFF ----
    lines.append("## Diff: o que mudou (Antes → Agora)")
    lines.append("")
    diff_rows = [
        ["Filings na DB", str(before.get("events_count", 0)),
         f"{before.get('events_count', 0)} + {len(novel)} novos no RI",
         "+" if novel else "="],
        ["Próximos eventos conhecidos", "0",
         str(len(parsed["events"])),
         "+" if parsed["events"] else "="],
        ["Apresentações .pdf detectadas", "0",
         str(len(parsed["presentations"])),
         "+" if parsed["presentations"] else "="],
        ["Audio/video acessível",
         "0 (era cego)",
         str(len(parsed["audio_video"])),
         "+" if parsed["audio_video"] else "="],
        ["Cross-check fundamentals com RI",
         "Não disponível",
         "Possível (não automatizado ainda)",
         "+"],
    ]
    lines.append(md_table(["Dimensão", "Antes", "Agora", "Δ"], diff_rows))
    lines.append("")

    # ---- NOVOS FILINGS COM EXTRACT ----
    lines.append("## Filings novos detectados (não estavam na DB)")
    lines.append("")
    if not novel:
        lines.append("_(nenhum filing novo — DB está sincronizada com RI)_")
    else:
        lines.append(f"**{len(novel)} filings detectados como novos vs DB.**")
        lines.append("")
        for i, n in enumerate(novel[:5]):
            lines.append(f"### {i+1}. {n['date']} — {n['title']}")
            lines.append("")
            lines.append(f"URL: {n['url']}")
            after_db = "**SIM (após max DB date)**" if n.get("after_db_max") else "(título não match em DB)"
            lines.append(f"Após data máxima DB: {after_db}")
            lines.append("")
            # Extracted text if available
            ex = next((x for x in extracted if x["url"] == n["url"]), None)
            if ex and ex.get("text"):
                lines.append("**Extracção markitdown (preview 1500 chars):**")
                lines.append("")
                lines.append("```")
                lines.append(ex["text"][:1500])
                lines.append("```")
                lines.append("")
    lines.append("")

    # ---- SINAIS ----
    lines.append("## Sinais / observações")
    lines.append("")
    signals = []
    if novel:
        signals.append(f"- **{len(novel)} filings descobertos** que CVM/SEC monitor "
                       f"ainda não trouxe → vantagem informacional")
    if parsed["events"]:
        upcoming_30d = [e for e in parsed["events"]
                        if _to_iso(e["date"]) <= "2026-06-10"
                        and _to_iso(e["date"]) >= TODAY]
        if upcoming_30d:
            signals.append(f"- **{len(upcoming_30d)} eventos críticos nos próximos 30 dias** "
                           f"— maior risco operacional/oportunidade")
    if parsed["audio_video"]:
        signals.append(f"- **{len(parsed['audio_video'])} fontes audio/video** disponíveis "
                       f"(markitdown pode transcrever)")
    if parsed["presentations"]:
        signals.append(f"- **{len(parsed['presentations'])} apresentações .pdf** disponíveis "
                       f"para extracção fundamentals/tese")
    if not signals:
        signals.append("_(sem sinais accionáveis — RI sem novidades vs DB)_")
    for s in signals:
        lines.append(s)
    lines.append("")

    # ---- INTERPRETAÇÃO PARA A TESE ----
    lines.append("## Interpretação para a tese")
    lines.append("")
    interp_lines = _interpret_for_thesis(cfg, before, parsed, novel, extracted)
    if interp_lines:
        lines.extend(interp_lines)
    else:
        lines.append("_(sem sinais accionáveis materiais)_")
    lines.append("")

    # ---- PRÓXIMAS PERGUNTAS ----
    lines.append("## Próximas perguntas (research-on-gap)")
    lines.append("")
    lines.append("- Wirar `events` table com filings novos detectados?")
    lines.append("- Schedule re-scrape no dia/véspera de earnings?")
    lines.append("- Cross-check fundamentals do RI vs nossa DB (delta material?)")
    lines.append("")

    return "\n".join(lines)


def _interpret_for_thesis(cfg: dict, before: dict, parsed: dict,
                          novel: list[dict], extracted: list[dict]) -> list[str]:
    """Heuristic, conservative interpretation of new findings vs the existing
    holding/thesis. Looks for keyword patterns in titles/extracted text and
    flags severity (positive/neutral/concern). Hand-curated, not LLM."""
    out: list[str] = []
    ticker = cfg["ticker"]
    pos = before.get("portfolio_position") or {}
    is_holding = bool(pos)

    # Earnings imminent?
    today = TODAY
    upcoming = []
    for e in parsed.get("events", []):
        iso = e.get("iso_date") or _to_iso(e.get("date", ""))
        if iso and today <= iso[:10] <= "2026-06-10":
            t = e.get("title", "").lower()
            if any(kw in t for kw in ("resultados", "earnings", "divulga",
                                      "videoconfer", "earnings call")):
                upcoming.append(e)
    if upcoming:
        nearest = upcoming[0]
        days = "?"
        try:
            from datetime import datetime as _dt
            d = _dt.fromisoformat(nearest.get("iso_date") or
                                  _to_iso(nearest["date"]))
            now = _dt.fromisoformat(today)
            days = (d - now).days
        except Exception:
            pass
        out.append(f"- ⏰ **Earnings/release iminente**: {nearest['date']} "
                   f"— {nearest['title'][:80]} (em ~{days} dias). "
                   f"Re-scrape no dia + monitorizar Telegram.")

    # Concerning patterns in novel filings
    concern_keywords = {
        "esclarecimento": "Pedido CVM/B3 → empresa teve que explicar algo",
        "ofício": "Ofício CVM → questionamento regulatório",
        "ajuste contábil": "Ajuste contábil → revisão de DFs já auditadas",
        "reapresenta": "Reapresentação DFs → erro material anterior",
        "renúncia": "Renúncia executiva/conselho → governance signal",
        "alteração na diretoria": "Mudança executiva — checar continuidade",
        "incorporação": "M&A — diluição/sinergia trade-off",
        "reorganização societ": "Reorganização — risco execução",
        "guidance": "Update guidance — material para preço",
        "dividend": "Dividend declaration",
        "jcp": "JCP — payout signal positivo",
        "investor day": "Investor day — narrative shift potencial",
        "downgrade": "Rating downgrade — risco financeiro",
        "upgrade": "Rating upgrade — sinal positivo",
    }
    flagged = []
    for n in novel[:8]:  # only top-N novel
        tlow = n.get("title", "").lower()
        for kw, meaning in concern_keywords.items():
            if kw in tlow:
                flagged.append((n, kw, meaning))
                break
    for n, kw, meaning in flagged:
        out.append(f"- 🚨 **{n.get('iso_date', n.get('date'))}** "
                   f"matched `{kw}` → {meaning}: _{n['title'][:80]}_")

    # Audio/video count → DD opportunities
    if parsed.get("audio_video"):
        n_av = len(parsed["audio_video"])
        out.append(f"- 🎙️ **{n_av} fontes audio/video** disponíveis para "
                   f"transcrição — earnings call/podcast pode revelar "
                   f"detalhes não em release escrito.")

    # Positions impact
    if is_holding and novel:
        avg_qty = pos.get("quantity", 0)
        entry = pos.get("entry_price", 0)
        out.append(f"- 💼 **Posição activa**: qty={avg_qty}, entry={entry}. "
                   f"{len(novel)} filings novos → revisitar tese se houver "
                   f"signal material acima.")

    # Cross-check fundamentals from RI vs DB
    fl = before.get("fundamentals_latest") or {}
    if fl and parsed.get("presentations"):
        out.append(f"- 📊 **Cross-check fundamentals**: RI tem "
                   f"{len(parsed['presentations'])} releases/relatórios — "
                   f"podemos auditar se ROE={fl.get('roe')}, "
                   f"DY={fl.get('dy')} batem com último report oficial.")

    return out


# ---------------------------------------------------------------------------
# Master report
# ---------------------------------------------------------------------------

def compose_master(results: list[dict]) -> str:
    L = []
    L.append(f"# Pilot Deep Dive — Master Report ({TODAY})")
    L.append("")
    L.append("**Phase MCP-5 validation** — does our new Playwright + markitdown "
             "pipeline add real value over yesterday's CVM/SEC monitors?")
    L.append("")
    L.append(f"Pilot: **{len(results)} tickers** chosen for diversity "
             "(BR/US, sector, RI provider).")
    L.append("")

    # Summary stats
    ok = [r for r in results if r["scrape"].get("ok")]
    fail = [r for r in results if not r["scrape"].get("ok")]
    total_novel = sum(len(r.get("novel", [])) for r in results)
    total_events = sum(len(r["parsed"].get("events", [])) if r.get("parsed") else 0
                       for r in results)
    total_pres = sum(len(r["parsed"].get("presentations", [])) if r.get("parsed") else 0
                     for r in results)
    total_av = sum(len(r["parsed"].get("audio_video", [])) if r.get("parsed") else 0
                   for r in results)
    avg_time = (sum(r["scrape"].get("elapsed_s", 0) for r in results) /
                max(len(results), 1))

    L.append("## Sumário executivo")
    L.append("")
    L.append(f"- Scrapes bem-sucedidos: **{len(ok)}/{len(results)}**")
    if fail:
        L.append(f"- Scrapes falhados: {[r['cfg']['ticker'] for r in fail]}")
    L.append(f"- **Filings novos descobertos** (vs DB): **{total_novel}**")
    L.append(f"- **Eventos de calendário descobertos** (não tínhamos): **{total_events}**")
    L.append(f"- **Apresentações/releases acessíveis**: **{total_pres}**")
    L.append(f"- **Audio/video accessível** (era cego): **{total_av}**")
    L.append(f"- Tempo médio scrape Playwright: **{avg_time:.1f}s/ticker**")
    L.append(f"- Estimativa scaling 200 tickers: "
             f"**~{200 * avg_time / 60:.0f}min** (~{200 * avg_time / 3600:.1f}h)")
    L.append("")

    # Master comparative table
    L.append("## Tabela comparativa global")
    L.append("")
    rows = []
    for r in results:
        cfg = r["cfg"]
        before = r["before"]
        parsed = r.get("parsed") or {}
        novel = r.get("novel", [])
        scrape = r["scrape"]
        rows.append([
            cfg["ticker"],
            cfg["market"].upper(),
            cfg["sector"][:14],
            "✅" if scrape.get("ok") else "❌",
            f"{scrape.get('elapsed_s', 0):.1f}s",
            str(before.get("events_count", 0)),
            str(len(parsed.get("filings", []))),
            f"**{len(novel)}**" if novel else "0",
            str(len(parsed.get("events", []))),
            str(len(parsed.get("presentations", []))),
            str(len(parsed.get("audio_video", []))),
        ])
    L.append(md_table(
        ["Ticker", "Mkt", "Sector", "Scrape", "Time",
         "DB events", "RI filings", "Novel", "Events", "Pres.", "A/V"],
        rows,
    ))
    L.append("")

    # Per-ticker links
    L.append("## Dossiers individuais")
    L.append("")
    for r in results:
        t = r["cfg"]["ticker"]
        status = "✅" if r["scrape"].get("ok") else "❌"
        L.append(f"- {status} [[{t}]] — {r['cfg']['rationale']}")
    L.append("")

    # Aggregated novel filings
    L.append("## Todos os filings novos descobertos (cross-ticker)")
    L.append("")
    all_novel = []
    for r in results:
        for n in r.get("novel", []):
            all_novel.append({**n, "ticker": r["cfg"]["ticker"]})
    all_novel.sort(key=lambda x: x.get("iso_date", ""), reverse=True)
    if all_novel:
        rows = [[n["ticker"], n["iso_date"], n["title"][:80]]
                for n in all_novel[:20]]
        L.append(md_table(["Ticker", "Data", "Título"], rows))
    else:
        L.append("_(zero filings novos cross-ticker)_")
    L.append("")

    # Upcoming events cross-ticker
    L.append("## Próximos eventos cross-ticker (30 dias)")
    L.append("")
    all_events = []
    for r in results:
        if r.get("parsed"):
            for e in r["parsed"].get("events", []):
                iso = _to_iso(e["date"])
                if TODAY <= iso <= "2026-06-10":
                    all_events.append({"ticker": r["cfg"]["ticker"],
                                       "date": iso, "title": e["title"]})
    all_events.sort(key=lambda x: x["date"])
    if all_events:
        rows = [[e["ticker"], e["date"], e["title"][:80]] for e in all_events]
        L.append(md_table(["Ticker", "Data", "Evento"], rows))
    else:
        L.append("_(zero eventos calendário cross-ticker nos próximos 30d)_")
    L.append("")

    # Validation / scaling
    L.append("## Validação técnica & escalabilidade")
    L.append("")
    L.append("**Por ticker (tempo + estado)**:")
    L.append("")
    rows = [[r["cfg"]["ticker"],
             f"{r['scrape'].get('elapsed_s', 0):.1f}s",
             "OK" if r["scrape"].get("ok") else f"ERR: {r['scrape'].get('error', '?')[:60]}"]
            for r in results]
    L.append(md_table(["Ticker", "Time", "Status"], rows))
    L.append("")

    L.append("**Estimativas de escala**:")
    L.append(f"- 33 holdings (BR+US): ~{33 * avg_time / 60:.0f}min")
    L.append(f"- 100 watchlist Tier-A: ~{100 * avg_time / 60:.0f}min")
    L.append(f"- 200 universo completo: ~{200 * avg_time / 60:.0f}min")
    L.append("")

    # Recommendation
    L.append("## Recomendação")
    L.append("")
    if len(ok) == len(results):
        L.append("✅ **Pipeline validado em 100% dos tickers do pilot.** "
                 "Recomendação: escalar para holdings (33) overnight como "
                 "próximo passo. Watchlist Tier-A (100) viável para 2ª noite.")
    elif len(ok) >= 3:
        L.append(f"⚠️ **{len(fail)} de {len(results)} falharam.** "
                 "Recomendação: fix gotchas dos failures antes de escalar. "
                 "Tickers que funcionam podem ir para overnight.")
    else:
        L.append(f"❌ **Pipeline frágil ({len(ok)}/{len(results)} OK).** "
                 "Não escalar. Re-investigar parser e RI URL resolution.")
    L.append("")

    L.append("---")
    L.append(f"_Generated by `scripts/pilot_deep_dive.py` at "
             f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    L.append(f"_Logs: `logs/pilot_deep_dive_{TODAY}.log`_")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Per-ticker pipeline
# ---------------------------------------------------------------------------

def deep_dive_one(cfg: dict, no_download: bool = False,
                  force_fresh: bool = False,
                  deep: bool = False,
                  per_ticker_budget: int = 300) -> dict:
    ticker = cfg["ticker"]
    market = cfg["market"]
    urls = cfg.get("ri_urls") or [cfg.get("ri_url")]
    urls = [u for u in urls if u]
    _log({"event": "ticker_start", "ticker": ticker, "market": market,
          "urls_count": len(urls)})
    t0 = time.time()

    result = {"cfg": cfg}
    try:
        result["before"] = snapshot_db(ticker, market)
        _log({"event": "snapshot_done", "ticker": ticker,
              "events_count": result["before"]["events_count"]})

        # Scrape ALL urls, accumulate parsed results
        scrapes = []
        merged = {"headers": [], "filings": [], "events": [],
                  "presentations": [], "audio_video": [],
                  "analyst_coverage_links": [], "raw_chars": 0}
        any_ok = False
        for url in urls:
            sc = scrape_ri(url, ticker, force_fresh=force_fresh)
            sc["url"] = url
            scrapes.append(sc)
            _log({"event": "scrape_done", "ticker": ticker, "url": url[:80],
                  "ok": sc.get("ok"), "elapsed_s": sc.get("elapsed_s")})
            if sc.get("ok"):
                any_ok = True
                md_path = Path(sc.get("md_path", ""))
                md = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
                p = parse_ri_content(md, base_url=url)
                # Merge
                merged["raw_chars"] += p.get("raw_chars", 0)
                for key in ("headers", "filings", "events", "presentations",
                            "audio_video", "analyst_coverage_links"):
                    merged[key].extend(p.get(key, []))

        # Final dedupe across URLs
        merged["filings"] = _dedupe(merged["filings"],
                                     key=lambda x: (x.get("iso_date", x.get("date", "")),
                                                    x["title"][:40]))
        merged["events"] = _dedupe(merged["events"],
                                    key=lambda x: (x["date"], x["title"][:40]))
        merged["presentations"] = _dedupe(merged["presentations"],
                                           key=lambda x: x["url"])
        merged["audio_video"] = _dedupe(merged["audio_video"],
                                         key=lambda x: x["url"])

        # Use first OK scrape as reference for "scrape" field (timing/chars)
        primary = next((s for s in scrapes if s.get("ok")), scrapes[0] if scrapes else {})
        result["scrape"] = {
            **primary,
            "ok": any_ok,
            "all_urls": [{"url": s.get("url"), "ok": s.get("ok"),
                          "elapsed_s": s.get("elapsed_s"),
                          "md_chars": s.get("md_chars")} for s in scrapes],
            "elapsed_s": sum(s.get("elapsed_s", 0) for s in scrapes),
        }
        result["parsed"] = merged if any_ok else None

        if not any_ok:
            result["novel"] = []
            result["extracted"] = []
        else:
            _log({"event": "parse_done", "ticker": ticker,
                  "filings": len(merged["filings"]),
                  "events": len(merged["events"]),
                  "presentations": len(merged["presentations"]),
                  "audio_video": len(merged["audio_video"])})

            result["novel"] = detect_novel_filings(
                merged["filings"],
                _all_events(ticker, market),
            )
            _log({"event": "novelty_done", "ticker": ticker,
                  "novel_count": len(result["novel"])})

            extracted = []
            # Deep mode: extract ALL novel; otherwise top 3.
            cap = len(result["novel"]) if deep else 3
            if not no_download and result["novel"]:
                t_extract_start = time.time()
                for i, novel_item in enumerate(result["novel"][:cap]):
                    # Per-ticker time budget guard
                    if time.time() - t0 > per_ticker_budget:
                        _log({"event": "extract_budget_hit",
                              "ticker": ticker,
                              "extracted_so_far": len(extracted),
                              "remaining": cap - i})
                        break
                    iso = novel_item.get("iso_date") or "no-date"
                    fname = f"{ticker}_{iso}_{i}.pdf"
                    target = ROOT / "data" / "cvm_pdfs" / "_pilot" / fname
                    if download_filing(novel_item["url"], target):
                        text = extract_filing(target)
                        extracted.append({**novel_item, "text": text})
                        _log({"event": "extract_done", "ticker": ticker,
                              "url": novel_item["url"][:80],
                              "chars": len(text)})
            result["extracted"] = extracted

        # Compose & save dossier
        dossier = compose_dossier(
            cfg, result["before"], result["scrape"],
            result.get("parsed") or {"filings": [], "events": [],
                                      "presentations": [], "audio_video": [],
                                      "headers": [], "raw_chars": 0,
                                      "analyst_coverage_links": []},
            result.get("novel", []),
            result.get("extracted", []),
        )
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"{ticker}.md"
        out.write_text(dossier, encoding="utf-8")
        _log({"event": "dossier_saved", "ticker": ticker,
              "path": str(out.relative_to(ROOT))})

        result["elapsed_s"] = time.time() - t0
        result["status"] = "ok"
    except Exception as e:
        tb = traceback.format_exc()
        _log({"event": "ticker_fail", "ticker": ticker, "err": str(e)[:300],
              "tb": tb[:600]})
        result["status"] = "fail"
        result["error"] = str(e)
        result["elapsed_s"] = time.time() - t0
        # Best-effort dossier with error
        try:
            err_md = (f"# {ticker} — FAIL\n\nError: {e}\n\n```\n{tb}\n```")
            (OUT_DIR / f"{ticker}.md").write_text(err_md, encoding="utf-8")
        except Exception:
            pass
    return result


def _all_events(ticker: str, market: str) -> list[dict]:
    """Pull all events (not just recent 5) for accurate novelty detection."""
    db = db_path(market)
    if not db.exists():
        return []
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    try:
        rows = c.execute(
            "SELECT event_date, kind, source, summary FROM events WHERE ticker=?",
            (ticker,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        c.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_pilot_from_yaml(filter_mode: str = "all",
                          tickers: list[str] | None = None) -> list[dict]:
    """Load pilot config from config/ri_urls.yaml.

    filter_mode: 'all', 'holdings', 'failed_only'
    tickers: optional explicit list to use
    """
    import yaml
    if not RI_URLS_YAML.exists():
        return []
    with RI_URLS_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    pilot = []
    for ticker, cfg in data.items():
        if cfg.get("status") != "ok":
            continue
        if not cfg.get("ri_urls"):
            continue
        if tickers and ticker not in tickers:
            continue
        if filter_mode == "holdings" and not cfg.get("is_holding"):
            continue
        pilot.append({
            "ticker": ticker,
            "market": cfg["market"],
            "sector": cfg.get("sector", ""),
            "ri_urls": cfg["ri_urls"],
            "rationale": (f"{cfg.get('method', '?')} "
                          f"{'(holding)' if cfg.get('is_holding') else '(watchlist)'}"),
        })
    return pilot


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", nargs="*", default=None,
                    help="Override tickers (default = pilot 5 OR all from yaml)")
    ap.add_argument("--from-yaml", action="store_true",
                    help="Load tickers from config/ri_urls.yaml instead of "
                         "hardcoded PILOT list")
    ap.add_argument("--filter", default="all",
                    choices=["all", "holdings"],
                    help="When --from-yaml, filter to subset")
    ap.add_argument("--no-download", action="store_true",
                    help="Skip downloading novel filings")
    ap.add_argument("--deep", action="store_true",
                    help="Extract ALL novel filings (default: top 3)")
    ap.add_argument("--per-ticker-budget", type=int, default=300,
                    help="Max seconds per ticker (default 300=5min). "
                         "Hard cap to prevent overnight stalls.")
    ap.add_argument("--force-fresh", action="store_true",
                    help="Bust Playwright cache (TTL=0) — slower but real timing")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _log({"event": "run_start", "out_dir": str(OUT_DIR),
          "deep": args.deep, "from_yaml": args.from_yaml,
          "filter": args.filter})

    if args.from_yaml:
        pilot = load_pilot_from_yaml(args.filter, args.tickers)
        if not pilot:
            print("No tickers loaded from yaml — run ri_url_resolver.py first",
                  file=sys.stderr)
            sys.exit(1)
    else:
        pilot = PILOT
        if args.tickers:
            pilot = [c for c in PILOT if c["ticker"] in args.tickers]
            if not pilot:
                print(f"No matching tickers in PILOT for {args.tickers}",
                      file=sys.stderr)
                sys.exit(1)

    _log({"event": "pilot_loaded", "n": len(pilot)})

    results = []
    t_run_start = time.time()
    for i, cfg in enumerate(pilot):
        t_ticker = time.time()
        r = deep_dive_one(cfg, no_download=args.no_download,
                          force_fresh=args.force_fresh,
                          deep=args.deep,
                          per_ticker_budget=args.per_ticker_budget)
        results.append(r)
        elapsed_total = time.time() - t_run_start
        _log({"event": "ticker_progress",
              "i": i + 1, "n": len(pilot), "ticker": cfg["ticker"],
              "ticker_elapsed_s": round(time.time() - t_ticker, 1),
              "total_elapsed_min": round(elapsed_total / 60, 1)})

    master = compose_master(results)
    master_path = OUT_DIR / "_MASTER.md"
    master_path.write_text(master, encoding="utf-8")
    _log({"event": "run_done", "master": str(master_path.relative_to(ROOT)),
          "results": len(results),
          "ok": sum(1 for r in results if r.get("status") == "ok"),
          "total_elapsed_min": round((time.time() - t_run_start) / 60, 1)})

    print(f"\n=== DONE ===")
    print(f"Master: {master_path}")
    print(f"Per-ticker: {OUT_DIR}")


if __name__ == "__main__":
    main()
