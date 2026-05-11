"""RI URL discovery — name-driven heuristics + content verification.

For each (ticker, market, sector, name) we build candidate RI URLs from the
*company name* (not the ticker — the ticker rarely maps to the IR domain) and
probe each. A candidate only wins if it (a) returns HTTP 200 with an HTML body
and (b) the page actually mentions the company (name token present) — this
rejects parked domains, "404" landing pages, and the fiis.com.br generic
"fundo não encontrado" page that previously passed as a false positive.

Resolution order per ticker:
  1. ETF       → skipped (no corporate RI)
  2. FII       → fiis.com.br/<ticker>/  (only if the ticker is actually a FII;
                 verified by fund-name presence)
  3. KNOWN     → curated mapping; still verified, mismatch is flagged not dropped
  4. heuristic → name-derived candidate URLs, first *verified* one wins
  5. failed    → left for the Tavily fallback (--max-tavily) or a later pass

Output: config/ri_urls.yaml
    <ticker>:
      market: br|us
      sector: ...
      name: <company name>
      is_holding: bool
      ri_urls: [url, ...]
      method: etf|fii_heuristic|known|heuristic|tavily|unknown
      status: ok|failed|skipped
      verified: true|false|null
      notes: ...
      last_resolved: ISO8601

Usage:
    python scripts/ri_url_resolver.py [--tickers T ...] [--only-failed]
                                      [--max-tavily N] [--no-verify]
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT_PATH = ROOT / "config" / "ri_urls.yaml"
UNIVERSE_PATH = ROOT / "config" / "universe.yaml"
LOG_PATH = ROOT / "logs" / "ri_url_resolver.log"

# Known explicit mappings (override heuristics). Still verified at resolve time.
KNOWN: dict[str, list[str]] = {
    # BR — validated in pilot
    "ITSA4": ["https://ri.itausa.com.br/"],
    "BBDC4": [
        "https://www.bradescori.com.br/",
        "https://www.bradescori.com.br/informacoes-ao-mercado/comunicados-e-fatos-relevantes/",
    ],
    "PRIO3": [
        "https://ri.prio3.com.br/",
        "https://ri.prio3.com.br/servicos-aos-investidores/comunicados-e-fatos-relevantes/",
    ],
    "PETR4": ["https://www.investidorpetrobras.com.br/"],
    "VALE3": ["https://vale.com/pt/investidores"],
    "ITUB4": ["https://www.itau.com.br/relacoes-com-investidores/"],
    "ABEV3": ["https://ri.ambev.com.br/"],
    "WEGE3": ["https://ri.weg.net/"],
    "SUZB3": ["https://ri.suzano.com.br/"],
    "KLBN11": ["https://ri.klabin.com.br/"],
    "BBSE3": ["https://www.bbseguridaderi.com.br/"],
    "BBAS3": ["https://ri.bb.com.br/"],
    "JBSS3": ["https://ri.jbs.com.br/"],
    "MGLU3": ["https://ri.magazineluiza.com.br/"],
    "RENT3": ["https://ri.localiza.com/"],
    "RDOR3": ["https://ri.rededorsaoluiz.com.br/"],
    "TAEE11": ["https://ri.taesa.com.br/"],
    "EGIE3": ["https://ri.engie.com.br/"],
    "BPAC11": ["https://ri.btgpactual.com/"],
    "B3SA3": ["https://ri.b3.com.br/"],
    "UNIP6": ["https://ri.unipar.com/"],
    "UNIP3": ["https://ri.unipar.com/"],
    "TUPY3": ["https://ri.tupy.com.br/"],
    "AXIA7": ["https://ri.axiaenergia.com.br/", "https://ri.light.com.br/"],
    "HGLG11": ["https://www.fiis.com.br/hglg11/"],
    "KNRI11": ["https://www.fiis.com.br/knri11/"],
    "EQTL3": ["https://ri.equatorialenergia.com.br/"],
    "CMIG4": ["https://ri.cemig.com.br/"],
    "CPLE3": ["https://ri.copel.com/"],
    "CPLE6": ["https://ri.copel.com/"],
    "CSAN3": ["https://ri.cosan.com.br/"],
    "GGBR4": ["https://ri.gerdau.com/"],
    "USIM5": ["https://ri.usiminas.com/"],
    "EMBR3": ["https://ri.embraer.com.br/"],
    "TIMS3": ["https://ri.tim.com.br/"],
    "VIVT3": ["https://ri.telefonica.com.br/"],
    "ELET3": ["https://ri.eletrobras.com/"],
    "RAIZ4": ["https://ri.raizen.com.br/"],
    "ASAI3": ["https://ri.assai.com.br/"],
    "PCAR3": ["https://www.gpari.com.br/"],
    "SBSP3": ["https://ri.sabesp.com.br/"],
    "FLRY3": ["https://ri.fleury.com.br/"],
    "LREN3": ["https://ri.lojasrenner.com.br/"],
    "VIVA3": ["https://ri.vivara.com.br/"],
    "POMO4": ["https://ri.marcopolo.com.br/"],
    "POMO3": ["https://ri.marcopolo.com.br/"],
    "AURA33": ["https://ri.auraminerals.com/"],
    "MOTV3": ["https://ri.motiva.com.br/"],
    "GMAT3": ["https://ri.grupomateus.com.br/"],
    "CSMG3": ["https://ri.copasa.com.br/"],
    "GRND3": ["https://ri.grendene.com.br/"],
    "PSSA3": ["https://ri.portoseguro.com.br/"],
    "PGMN3": ["https://ri.paguemenos.com.br/"],
    "PLPL3": ["https://ri.planoeplano.com.br/"],
    "EZTC3": ["https://ri.eztec.com.br/"],
    "MULT3": ["https://www.multri.com.br/"],
    "BRKM5": ["https://www.braskem-ri.com.br/"],
    "KLBN4": ["https://ri.klabin.com.br/"],
    # US — major holdings + watchlist
    "JPM": [
        "https://www.jpmorganchase.com/ir",
        "https://www.jpmorganchase.com/ir/quarterly-earnings",
    ],
    "JNJ": ["https://www.investor.jnj.com/"],
    "KO": ["https://investors.coca-colacompany.com/"],
    "PG": ["https://www.pginvestor.com/"],
    "BLK": ["https://ir.blackrock.com/"],
    "BN": ["https://bn.brookfield.com/"],
    "GS": ["https://www.goldmansachs.com/investor-relations/"],
    "BRK-B": ["https://www.berkshirehathaway.com/"],
    "AAPL": ["https://investor.apple.com/"],
    "ACN": ["https://investor.accenture.com/"],
    "MSFT": ["https://www.microsoft.com/en-us/investor"],
    "GOOGL": ["https://abc.xyz/investor/"],
    "AMZN": ["https://ir.aboutamazon.com/"],
    "META": ["https://investor.atmeta.com/"],
    "NVDA": ["https://investor.nvidia.com/"],
    "TSLA": ["https://ir.tesla.com/"],
    "PLTR": ["https://investors.palantir.com/"],
    "TSM": ["https://investor.tsmc.com/english"],
    "TTD": ["https://investors.thetradedesk.com/"],
    "HD": ["https://ir.homedepot.com/"],
    # TEN = Tsakos Energy Navigation Ltd (NYSE: TEN). IR site:
    "TEN": ["https://www.tenn.gr/", "https://www.tsakosenergynavigation.com/"],
    "NU": ["https://investors.nu/"],
    "TFC": ["https://ir.truist.com/"],
    "XP": ["https://investors.xpinc.com/"],
    "O": ["https://www.realtyincome.com/investors"],
    "PLD": ["https://ir.prologis.com/"],
    "MA": ["https://investor.mastercard.com/"],
    "V": ["https://investor.visa.com/"],
    "WMT": ["https://stock.walmart.com/"],
    "HON": ["https://investor.honeywell.com/"],
    "CAT": ["https://www.caterpillar.com/en/investors.html"],
    "MMM": ["https://investors.3m.com/"],
    "PFE": ["https://investors.pfizer.com/"],
    "MRK": ["https://www.merck.com/investor-relations/"],
    "ABBV": ["https://investors.abbvie.com/"],
    "LLY": ["https://investor.lilly.com/"],
    "UNH": ["https://www.unitedhealthgroup.com/investors.html"],
    "CVS": ["https://investors.cvshealth.com/"],
    "WBA": ["https://investor.walgreensbootsalliance.com/"],
    "MCD": ["https://corporate.mcdonalds.com/corpmcd/investors.html"],
    "SBUX": ["https://investor.starbucks.com/"],
    "NKE": ["https://investors.nike.com/"],
    "DIS": ["https://thewaltdisneycompany.com/investor-relations/"],
    "T": ["https://investors.att.com/"],
    "VZ": ["https://www.verizon.com/about/investors/"],
    "TMUS": ["https://investor.t-mobile.com/"],
    "INTC": ["https://www.intc.com/"],
    "CSCO": ["https://investor.cisco.com/"],
    "AMD": ["https://ir.amd.com/"],
    "QCOM": ["https://investor.qualcomm.com/"],
    "ORCL": ["https://investor.oracle.com/"],
    "ADBE": ["https://www.adobe.com/investor-relations.html"],
    "CRM": ["https://investor.salesforce.com/"],
    "NFLX": ["https://ir.netflix.net/"],
    "PYPL": ["https://investor.pypl.com/"],
    "ROKU": ["https://investor.roku.com/"],
    "BABA": ["https://www.alibabagroup.com/en/ir/home"],
    "CVX": ["https://www.chevron.com/investors"],
    "XOM": ["https://investor.exxonmobil.com/"],
    "SYY": ["https://investors.sysco.com/"],
    "AOS": ["https://investor.aosmith.com/"],
    # US Dividend Kings / Aristocrats — IR domains the ticker/name heuristics miss
    "ADM": ["https://investors.adm.com/"],
    "ADP": ["https://investors.adp.com/"],
    "ITW": ["https://investor.itw.com/"],
    "BDX": ["https://investors.bd.com/"],
    "MDT": ["https://investorrelations.medtronic.com/"],
    "MKC": ["https://ir.mccormick.com/"],
    "PNR": ["https://investors.pentair.com/"],
    "SWK": ["https://www.stanleyblackanddecker.com/investors"],
    "TROW": ["https://investors.troweprice.com/"],
    "LEG": ["https://investors.leggett.com/"],
    "ED": ["https://investor.conedison.com/"],
    "TDS": ["https://investors.tdsinc.com/"],
    "TNC": ["https://investors.tennantco.com/"],
    "ABM": ["https://investor.abm.com/"],
    "FDS": ["https://investor.factset.com/"],
    "WST": ["https://investors.westpharma.com/"],
    "SHW": ["https://investors.sherwin-williams.com/"],
    "ES": ["https://investors.eversource.com/"],
    "CL": ["https://investor.colgatepalmolive.com/"],
    "CLX": ["https://investors.thecloroxcompany.com/"],
    "APD": ["https://investors.airproducts.com/"],
    "KMB": ["https://investor.kimberly-clark.com/"],
    "ABT": ["https://www.abbottinvestor.com/"],
    "UVV": ["https://www.universalcorp.com/investor-relations/"],
    "GPC": ["https://investor.genpt.com/"],
    "BRO": ["https://investor.bbrown.com/"],
    "BF-B": ["https://investors.brown-forman.com/"],
    "AWR": ["https://ir.aswater.com/"],
    "ERIE": ["https://www.erie.com/about-erie/investor-relations"],
    "CWT": ["https://ir.calwatergroup.com/"],
    "GRC": ["https://investors.gormanrupp.com/"],
    "GWW": ["https://invest.grainger.com/"],
    "FRT": ["https://investors.federalrealty.com/"],
    "TR": ["https://www.tootsie.com/about/investor-relations"],
    "SCL": ["https://www.stepan.com/content/stepan-dot-com/en/investors.html"],
    "MSEX": ["https://www.middlesexwater.com/category/investors/"],
    "IBM": ["https://www.ibm.com/investor"],
    "BKH": ["https://investors.blackhillscorp.com/"],
    "CBSH": ["https://investor.commercebancshares.com/"],
    "BRO": ["https://investor.bbrown.com/"],
    # BR — name slug doesn't yield the real RI domain
    "ABCB4": ["https://ri.abcbrasil.com.br/"],
    "WIZC3": ["https://ri.wizsolucoes.com.br/", "https://ri.wizco.com.br/"],
    "AWR": ["https://ir.americanstateswater.com/", "https://www.aswater.com/investors"],
}

# ETFs / index trackers — no corporate RI.
ETF_TICKERS = {
    "LFTB11", "IVVB11", "GREK", "ARKK", "BOVA11", "IVV", "SPY", "QQQ",
    "VTI", "VOO", "BOVA11", "SMAL11", "DIVO11", "FIND11",
    "BTLG12",  # residual/old class, no live RI page of its own
}

# Sector / segment strings that indicate a FII (real-estate fund).
FII_SEGMENTS = {
    "logística", "logistica", "híbrido", "hibrido", "papel (cri)", "papel",
    "tijolo", "shopping", "corporativo", "renda urbana", "fii", "fof",
    "fundo imobiliário", "fundos imobiliários", "agências", "agencias",
    "hospitalar", "lajes corporativas", "galpões", "residencial",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

# Markers that mean "this is not a real page" — checked only in <title> and the
# first few KB of HTML (a bare "not found" anywhere in 120KB of markup is far too
# common to use as a signal).
PARKED_MARKERS = (
    "domain for sale", "buy this domain", "this domain is for sale",
    "domínio à venda", "this domain may be for sale", "hugedomains",
    "página não encontrada", "pagina nao encontrada",
    "page not found", "404 not found", "error 404 -", "http 404",
    "site temporarily unavailable", "this site can't be reached",
    "fundo não encontrado", "fundo nao encontrado",
    "ação não encontrada", "acao nao encontrada", "ativo não encontrado",
    "nenhum resultado encontrado", "under construction", "em construção",
    "godaddy.com", "default web site page",
)

# Tokens too generic to *alone* confirm a company identity (used as name slug
# parts but won't count as a unique verification signal on their own).
_STOP_TOKENS = {
    "sa", "saa", "ltda", "inc", "corp", "corporation", "company", "companies",
    "co", "ltd", "limited", "plc", "ag", "gmbh", "nv", "the", "and", "of",
    "group", "grupo", "holding", "holdings", "participações", "participacoes",
    "pn", "on", "unit", "units", "fii", "cri", "fof", "fundo", "fundos",
    "imobiliário", "imobiliario", "imobiliarios", "imob", "brasil", "brazil",
    "companhia", "etf", "ishares", "investimentos", "investments", "banco", "bank",
}

# Words that appear in many company names but identify nothing on their own.
# A *single* one of these matching a page is not enough to verify it.
_GENERIC_TOKENS = {
    "data", "energy", "energia", "capital", "financial", "finance", "services",
    "service", "industries", "industrial", "international", "global", "national",
    "technologies", "technology", "systems", "system", "solutions", "brands",
    "partners", "products", "product", "materials", "resources", "electric",
    "motors", "foods", "food", "power", "trust", "realty", "water", "gas", "oil",
    "oils", "insurance", "health", "healthcare", "media", "communications",
    "entertainment", "first", "united", "general", "southern", "northern",
    "eastern", "western", "central", "pacific", "atlantic", "american",
    "automatic", "natural", "standard", "commercial", "consolidated", "associates",
    "stores", "store", "retail", "hotels", "resorts", "airlines", "express",
    "logistics", "logística", "logistica", "transport", "transportation",
    "mining", "steel", "chemical", "chemicals", "petroleum", "beverages",
    "brewing", "tobacco", "apparel", "footwear", "tools", "tool", "works",
    "safety", "aviation", "aerospace", "defense", "semiconductor", "semiconductors",
    "software", "internet", "networks", "network", "wireless", "mobile",
    "telecom", "telecommunications", "real", "estate", "shopping", "centers",
    "center", "properties", "renda", "urbana", "papel", "fator", "verita",
    "black", "white", "blue", "green", "red", "gold", "silver", "diamond",
    "illinois", "texas", "california", "carolina", "dakota", "ohio", "valley",
}


def _is_distinctive(tok: str) -> bool:
    """A token strong enough to verify a company on its own."""
    return len(tok) >= 5 and not tok.isdigit() and tok not in _GENERIC_TOKENS


def _log(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


# --------------------------------------------------------------------------
# name / slug helpers
# --------------------------------------------------------------------------
def _strip_suffixes(s: str) -> str:
    s = s.strip().lower()
    for suf in (" sa", " s.a.", " s.a", " s/a", " ltda", " holding", " holdings",
                " inc", " inc.", " corp", " corporation", " co", " co.", " ltd",
                " limited", " plc", " ag", " gmbh", " nv", " group", " grupo",
                " participações", " participacoes", " pn", " on", " unit", " units",
                " fii", " cri"):
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
    return s


def slug_from_name(name: str) -> str:
    """'Banco ABC Brasil' -> 'bancoabcbrasil'."""
    if not name:
        return ""
    return re.sub(r"[^a-z0-9]+", "", _strip_suffixes(name))


def first_word_slug(name: str) -> str:
    """First significant word of the name -> slug. 'Pague Menos' -> 'paguemenos'?
    No — first word only: 'pague'. Useful for ri.<firstword>.com.br patterns."""
    s = _strip_suffixes(name)
    parts = [p for p in re.split(r"[^a-z0-9]+", s) if p]
    return parts[0] if parts else ""


def name_tokens(name: str) -> list[str]:
    """Significant lowercase tokens used to confirm a page belongs to a company."""
    s = _strip_suffixes(name)
    toks = [t for t in re.split(r"[^a-z0-9]+", s) if len(t) >= 3]
    return [t for t in toks if t not in _STOP_TOKENS]


# --------------------------------------------------------------------------
# fetch + verify
# --------------------------------------------------------------------------
def fetch_text(url: str, timeout: int = 12) -> tuple[int, str, str]:
    """GET url → (status_code, html_text[:120k], final_hostname).

    status 0 on exception. Retries once with verify=False on SSL error
    (some RI sites have cert mismatches).
    """
    from urllib.parse import urlparse
    for verify in (True, False):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout,
                             allow_redirects=True, verify=verify)
            host = (urlparse(r.url).hostname or "").lower()
            ctype = r.headers.get("content-type", "").lower()
            if "html" not in ctype and "text" not in ctype and ctype:
                return r.status_code, "", host
            return r.status_code, (r.text or "")[:120_000], host
        except requests.exceptions.SSLError:
            continue  # retry with verify=False
        except Exception:
            return 0, "", ""
    return 0, "", ""


def _looks_parked(low_html: str) -> str | None:
    """Return the matched marker if the page head/title looks parked/404, else None."""
    head = low_html[:5000]
    m = re.search(r"<title[^>]*>(.*?)</title>", low_html[:20000], re.S)
    title = (m.group(1) if m else "")
    for mk in PARKED_MARKERS:
        if mk in title or mk in head:
            return mk
    # bare "page not found" / "404" if it dominates a tiny page
    if len(low_html) < 3000 and ("not found" in low_html or " 404 " in low_html):
        return "tiny 404-ish page"
    return None


def verify_page(url: str, name: str, ticker: str) -> tuple[bool, str]:
    """Is this URL plausibly the real IR page for `name` / `ticker`?

    A candidate passes only if it returns HTML 200 AND the page carries a
    *distinctive* signal of the company:
      - the full-name slug appears, OR
      - a distinctive name token (≥5 chars, not a generic business word), OR
      - ≥2 name tokens of any kind, OR
      - the ticker appears AND the resolved hostname is ticker-derived.
    A single generic token ("data", "energy", "global"…) is NOT enough — that
    is what let ADP → automatic.com and ADM → archer.com slip through before.
    """
    code, txt, host = fetch_text(url)
    if code == 0:
        return False, "fetch failed (timeout/conn/SSL)"
    if code >= 400:
        return False, f"HTTP {code}"
    if not txt or not txt.strip():
        return False, f"HTTP {code} but empty/non-HTML body"
    low = txt.lower()
    parked = _looks_parked(low)
    if parked:
        return False, f"parked/error page ('{parked}')"

    toks = name_tokens(name)
    flat = low.replace(" ", "")
    slug = slug_from_name(name)
    tkl = ticker.lower().replace("-", "").replace(".", "")

    if slug and len(slug) >= 5 and slug in flat:
        return True, f"verified: full-name slug '{slug}' present"
    distinct = [t for t in toks if _is_distinctive(t) and t in low]
    if distinct:
        return True, f"verified: distinctive token '{distinct[0]}'"
    generic_hits = [t for t in toks if t in low]
    if len(generic_hits) >= 2:
        return True, f"verified: name tokens {generic_hits[:3]}"
    if tkl and len(tkl) >= 2 and tkl in (host or "") and tkl in low:
        return True, f"weak-verified: ticker '{ticker}' in host+page"
    if not toks:
        return True, "accepted: HTTP 200, no distinctive name tokens to check"
    return False, (f"insufficient signal (tokens {toks[:4]}; "
                   f"distinct={distinct}; generic_hits={generic_hits}; host={host})")


# --------------------------------------------------------------------------
# candidate builders
# --------------------------------------------------------------------------
def _dedup(cands: list[str]) -> list[str]:
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _br_patterns(slug: str) -> list[str]:
    return [
        f"https://ri.{slug}.com.br/",
        f"https://www.{slug}ri.com.br/",
        f"https://ri.{slug}.com/",
        f"https://www.{slug}.com.br/ri/",
        f"https://www.{slug}.com.br/relacoes-com-investidores/",
        f"https://{slug}.com.br/ri/",
    ]


def _us_patterns(slug: str) -> list[str]:
    return [
        f"https://investors.{slug}.com/",
        f"https://investor.{slug}.com/",
        f"https://ir.{slug}.com/",
        f"https://www.{slug}.com/investors",
        f"https://www.{slug}.com/investor-relations",
        f"https://www.{slug}.com/investors/",
        f"https://www.{slug}.com/ir",
    ]


def br_candidates(ticker: str, name: str) -> list[str]:
    # Order matters: most-specific first. full-name slug → ticker base → first
    # word of the name (last — it collides easily with unrelated domains).
    full = slug_from_name(name)
    fw = first_word_slug(name)
    base = ticker[:-1].lower() if ticker[-1:].isdigit() else ticker.lower()
    cands: list[str] = []
    if full:
        cands += _br_patterns(full)
    cands += [f"https://ri.{base}.com.br/", f"https://www.{base}ri.com.br/",
              f"https://ri.{ticker.lower()}.com.br/"]
    if fw and fw != full:
        cands += _br_patterns(fw)
    return _dedup(cands)


def us_candidates(ticker: str, name: str) -> list[str]:
    full = slug_from_name(name)
    fw = first_word_slug(name)
    tk = ticker.lower().replace("-", "").replace(".", "")
    cands: list[str] = []
    if full:
        cands += _us_patterns(full)
    cands += [f"https://investors.{tk}.com/", f"https://investor.{tk}.com/",
              f"https://ir.{tk}.com/"]
    if fw and fw != full:
        cands += _us_patterns(fw)
    return _dedup(cands)


# --------------------------------------------------------------------------
# universe loading
# --------------------------------------------------------------------------
def _walk_universe_collect(node, fii: set, etf: set):
    if isinstance(node, dict):
        # heuristic: a node is a leaf entry if it has a ticker
        # group keys 'fiis' / 'etfs' tell us the kind
        for k, v in node.items():
            if k == "fiis" and isinstance(v, list):
                for e in v:
                    if isinstance(e, dict) and e.get("ticker"):
                        fii.add(e["ticker"])
            elif k == "etfs" and isinstance(v, list):
                for e in v:
                    if isinstance(e, dict) and e.get("ticker"):
                        etf.add(e["ticker"])
            else:
                _walk_universe_collect(v, fii, etf)
    elif isinstance(node, list):
        for v in node:
            _walk_universe_collect(v, fii, etf)


def load_fii_etf_sets() -> tuple[set, set]:
    fii: set = set()
    etf: set = set(ETF_TICKERS)
    if UNIVERSE_PATH.exists():
        try:
            u = yaml.safe_load(UNIVERSE_PATH.read_text(encoding="utf-8")) or {}
            _walk_universe_collect(u, fii, etf)
        except Exception:
            pass
    return fii, etf


# Standard GICS-ish sectors a "11" ticker can legitimately have *without* being
# a FII (units like ENGI11=Utilities, BPAC11=Banks, KLBN11=Materials).
_NON_FII_SECTORS = {
    "banks", "financials", "financial", "utilities", "materials", "industrials",
    "energy", "oil & gas", "oil and gas", "mining", "technology",
    "information technology", "health care", "healthcare", "consumer staples",
    "consumer discretionary", "consumer disc.", "communication services",
    "communications", "insurance", "telecommunications", "benchmark",
    "etf-rf", "etf-us", "etf-eq", "real estate",  # RE *companies* don't end in 11
}


def is_fii(ticker: str, sector: str, fii_set: set) -> bool:
    """A BR ticker ending in '11' is a FII unless it's an ETF or a unit of a
    standard-sector company. (Sector strings in the DB are sometimes mojibake'd,
    so we test against the *exclusion* list rather than a FII-segment list.)"""
    if ticker in fii_set:
        return True
    if not ticker.endswith("11"):
        return False
    s = (sector or "").strip().lower()
    if s and s in FII_SEGMENTS:
        return True
    if s and s in _NON_FII_SECTORS:
        return False
    # unknown / mojibake'd sector that isn't clearly a standard one → assume FII
    return True


def load_universe() -> list[dict]:
    """All tickers from companies tables, with name + sector + is_holding.
    Falls back to existing ri_urls.yaml names if the DB name is missing."""
    existing = {}
    if OUT_PATH.exists():
        try:
            existing = yaml.safe_load(OUT_PATH.read_text(encoding="utf-8")) or {}
        except Exception:
            existing = {}
    rows: list[dict] = []
    seen: set = set()
    for db_path, market in [
        (ROOT / "data" / "br_investments.db", "br"),
        (ROOT / "data" / "us_investments.db", "us"),
    ]:
        if not db_path.exists():
            continue
        c = sqlite3.connect(db_path)
        c.row_factory = sqlite3.Row
        try:
            for r in c.execute(
                "SELECT ticker, name, sector, is_holding FROM companies "
                "ORDER BY is_holding DESC, ticker"
            ).fetchall():
                t = r["ticker"]
                if t in seen:
                    continue
                seen.add(t)
                nm = r["name"] or ""
                if not nm or nm == t:
                    nm = (existing.get(t, {}) or {}).get("name") or nm
                rows.append({
                    "ticker": t, "market": market, "name": nm,
                    "sector": r["sector"] or "", "is_holding": bool(r["is_holding"]),
                })
        finally:
            c.close()
    # any ticker only present in the yaml (shouldn't happen now, but be safe)
    for t, c in (existing or {}).items():
        if t not in seen and isinstance(c, dict):
            rows.append({
                "ticker": t, "market": c.get("market", "us"),
                "name": c.get("name", ""), "sector": c.get("sector", ""),
                "is_holding": bool(c.get("is_holding")),
            })
    return rows


# --------------------------------------------------------------------------
# resolution
# --------------------------------------------------------------------------
def resolve_one(ticker: str, market: str, name: str, sector: str,
                fii_set: set, etf_set: set, verify: bool = True) -> dict:
    out = {
        "market": market, "sector": sector, "name": name,
        "ri_urls": [], "method": "unknown", "status": "failed",
        "verified": None, "notes": "",
        "last_resolved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # 1. ETF — skip
    if ticker in etf_set:
        out.update(status="skipped", method="etf", notes="ETF / index tracker — no corporate RI")
        return out

    # 2. FII — fiis.com.br (only for real FIIs; verified by fund-name presence)
    if market == "br" and ticker.endswith("11") and is_fii(ticker, sector, fii_set):
        url = f"https://www.fiis.com.br/{ticker.lower()}/"
        if not verify:
            out.update(ri_urls=[url], method="fii_heuristic", status="ok",
                       notes="fiis.com.br (unverified)")
            return out
        ok, why = verify_page(url, name, ticker)
        if ok:
            out.update(ri_urls=[url], method="fii_heuristic", status="ok",
                       verified=True, notes=f"fiis.com.br — {why}")
            return out
        out["notes"] = f"fiis.com.br rejected — {why}; "
        # fall through to generic heuristics (some FIIs have own RI sites)

    # 3. KNOWN — curated; verified but never dropped on mismatch
    if ticker in KNOWN:
        urls = list(KNOWN[ticker])
        out.update(ri_urls=urls, method="known", status="ok")
        if verify:
            ok, why = verify_page(urls[0], name, ticker)
            out["verified"] = bool(ok)
            out["notes"] = (out["notes"] + (f"known — {why}" if ok else
                            f"known — UNVERIFIED ({why}); kept anyway, review")).strip()
        else:
            out["notes"] = (out["notes"] + "known (unverified)").strip()
        return out

    # 4. Heuristic candidates derived from the company name
    cands = (br_candidates(ticker, name) if market == "br"
             else us_candidates(ticker, name))
    tried = 0
    for cand in cands:
        tried += 1
        if verify:
            ok, why = verify_page(cand, name, ticker)
            if ok:
                out.update(ri_urls=[cand], method="heuristic", status="ok",
                           verified=True, notes=(out["notes"] + f"name-heuristic — {why}").strip())
                return out
        else:
            # cheap probe only
            try:
                r = requests.get(cand, headers=HEADERS, timeout=6,
                                 allow_redirects=True, stream=True)
                r.close()
                if r.status_code < 400:
                    out.update(ri_urls=[cand], method="heuristic", status="ok",
                               notes=(out["notes"] + f"HTTP {r.status_code} (unverified)").strip())
                    return out
            except Exception:
                pass
        time.sleep(0.15)

    out["notes"] = (out["notes"] + f"all {tried} name-heuristic candidates failed; Tavily defer").strip()
    return out


# --------------------------------------------------------------------------
# Tavily fallback (optional, quota-limited)
# --------------------------------------------------------------------------
def tavily_resolve(name: str, ticker: str, market: str) -> tuple[str, str] | None:
    """Search '<name> investor relations official site' via Tavily, return
    (best_url, note) of the first result whose page verifies, else None.

    Uses agents.autoresearch.search (cached 7d, rate-limited 100/day 50/h).
    """
    try:
        from agents.autoresearch import search as tavily_search  # type: ignore
    except Exception:
        return None
    geo = "relações com investidores site oficial" if market == "br" else "investor relations official site"
    q = f"{name} ({ticker}) {geo}"
    try:
        res = tavily_search(q, max_results=8)
    except Exception:
        return None
    if getattr(res, "error", None):
        return None
    from urllib.parse import urlparse
    _AGG = ("wikipedia.", "bloomberg.com", "reuters.com", "marketwatch.",
            "yahoo.com", "finance.yahoo", "investing.com", "tradingview.",
            "tipranks.", "stockanalysis.", "wsj.com", "fool.com", "seekingalpha.",
            "alphaspread.", "quartr.com", "statusinvest.com", "fundsexplorer.",
            "investidor10.", "advfn.com", "simplywall.st", "barchart.com",
            "morningstar.", "marketbeat.", "macrotrends.", "wisesheets.",
            "gurufocus.", "stockopine.", "moomoo.com", "webull.com",
            "finviz.com", "zacks.com", "nasdaq.com", "investorshub.",
            "linkedin.com", "facebook.com", "twitter.com", "youtube.com",
            "sec.gov", "annualreports.com", "stocktitan.", "benzinga.com")
    ntoks = [t for t in name_tokens(name) if len(t) >= 4]
    tkl = ticker.lower().replace("-", "").replace(".", "")
    for hit in (getattr(res, "results", None) or []):
        url = getattr(hit, "url", "") or ""
        if not url:
            continue
        host = (urlparse(url).hostname or "").lower()
        if not host or any(a in host for a in _AGG):
            continue
        # the company's *own* IR site has a name token (or the ticker) in its
        # hostname — an aggregator that merely mentions the company does not.
        if not (any(t in host for t in ntoks) or (len(tkl) >= 3 and tkl in host)):
            continue
        ok, why = verify_page(url, name, ticker)
        if ok:
            return url, f"tavily — {why}"
    return None


# --------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", nargs="*", default=None,
                    help="Subset of tickers to (re)resolve (default = all)")
    ap.add_argument("--only-failed", action="store_true",
                    help="Only (re)resolve tickers currently status=failed in ri_urls.yaml")
    ap.add_argument("--max-tavily", type=int, default=0,
                    help="Max Tavily searches as fallback for still-failed tickers")
    ap.add_argument("--no-verify", action="store_true",
                    help="Skip content verification (HTTP-200 probe only) — faster, less accurate")
    args = ap.parse_args()
    verify = not args.no_verify

    fii_set, etf_set = load_fii_etf_sets()
    universe = load_universe()

    existing: dict = {}
    if OUT_PATH.exists():
        try:
            existing = yaml.safe_load(OUT_PATH.read_text(encoding="utf-8")) or {}
        except Exception:
            existing = {}

    if args.tickers:
        wanted = set(args.tickers)
        universe = [r for r in universe if r["ticker"] in wanted]
    elif args.only_failed:
        bad = {t for t, c in existing.items()
               if isinstance(c, dict) and c.get("status") == "failed"}
        universe = [r for r in universe if r["ticker"] in bad]

    _log({"event": "discovery_start", "n": len(universe), "verify": verify})

    out = dict(existing)  # merge: keep entries we don't touch
    ok = fail = skip = tavily_used = 0

    for r in universe:
        t = r["ticker"]
        try:
            res = resolve_one(t, r["market"], r["name"], r["sector"],
                              fii_set, etf_set, verify=verify)
            res["is_holding"] = r["is_holding"]
            # Tavily fallback for still-failed
            if res["status"] == "failed" and tavily_used < args.max_tavily:
                tavily_used += 1
                hit = tavily_resolve(r["name"], t, r["market"])
                if hit:
                    url, why = hit
                    res.update(ri_urls=[url], method="tavily", status="ok",
                               verified=True, notes=why)
            out[t] = res
            if res["status"] == "ok":
                ok += 1
            elif res["status"] == "skipped":
                skip += 1
            else:
                fail += 1
            _log({"event": "resolved", "ticker": t, "name": r["name"],
                  "status": res["status"], "method": res["method"],
                  "verified": res.get("verified"),
                  "url": (res["ri_urls"][0] if res["ri_urls"] else None),
                  "notes": res["notes"]})
        except Exception as e:  # noqa: BLE001
            out[t] = {**(existing.get(t, {})), "market": r["market"],
                      "method": "error", "status": "failed", "notes": str(e)[:200],
                      "last_resolved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
            fail += 1
            _log({"event": "error", "ticker": t, "err": str(e)[:200]})

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump({k: out[k] for k in sorted(out)}, f,
                       sort_keys=False, allow_unicode=True, default_flow_style=False, width=120)

    _log({"event": "discovery_done", "ok": ok, "fail": fail, "skip": skip,
          "tavily_used": tavily_used, "out": str(OUT_PATH.relative_to(ROOT))})
    print(f"\n=== DONE ===  processed {len(universe)} | ok={ok} failed={fail} "
          f"skipped={skip} tavily_used={tavily_used}\noutput: {OUT_PATH}")


if __name__ == "__main__":
    main()
