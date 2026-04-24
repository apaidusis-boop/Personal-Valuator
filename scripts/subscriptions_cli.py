"""subscriptions_cli — orchestrator para adapters de subscription.

Comandos (via `ii subs <cmd>`):
    ii subs setup                            # cria dirs + imprime instruções
    ii subs test [--source suno|xp|wsj|all]  # valida cookies
    ii subs fetch [--source X] [--days 7]    # discover + download
    ii subs extract [--source X] [--limit N] # Ollama extract pendente
    ii subs query <TICKER> [--days 90]       # views sobre ticker
    ii subs latest [--source X] [--days 7]   # reports recentes

Zero tokens Claude em toda a pipeline.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from fetchers.subscriptions import SessionManager, PlaywrightSession  # noqa: E402
from fetchers.subscriptions.suno import SunoAdapter  # noqa: E402
from fetchers.subscriptions.xp import XPAdapter  # noqa: E402
from fetchers.subscriptions.wsj import WSJAdapter  # noqa: E402
from fetchers.subscriptions.finclass import FinclassAdapter  # noqa: E402
from fetchers.subscriptions.fool import FoolAdapter  # noqa: E402

SUBS_DIR = ROOT / "data" / "subscriptions"
COOKIES_DIR = SUBS_DIR / "cookies"
PDF_DIR = SUBS_DIR / "pdfs"
HTML_DIR = SUBS_DIR / "html"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

ADAPTERS = {
    "suno": SunoAdapter,
    "xp": XPAdapter,
    "wsj": WSJAdapter,
    "fool": FoolAdapter,
    "finclass": FinclassAdapter,
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _get_db(source: str) -> Path:
    # Suno/XP/Finclass → BR. WSJ/Fool → US.
    return DB_US if source in ("wsj", "fool") else DB_BR


def _make_adapter(source: str, *, force_playwright: bool = False, headless: bool | None = None):
    """Constrói adapter com a session certa.

    Sites que precisam de browser real (WAF/SPA/JWT) usam PlaywrightSession.
    Sites que funcionam com requests+cookies ficam com SessionManager.

    `headless` override: se None, usa default por site (XP=False; outros=True).
    """
    cls = ADAPTERS[source]
    # Default: XP/Suno/Finclass → Playwright; Fool/WSJ → requests
    playwright_sources = {"suno", "xp", "finclass"}
    use_pw = force_playwright or source in playwright_sources
    # WAF-heavy sites requerem headful (Imperva bloqueia headless)
    headless_by_source = {"xp": False, "suno": True, "finclass": True}
    effective_headless = headless if headless is not None else headless_by_source.get(source, True)
    if use_pw:
        try:
            session = PlaywrightSession(source, COOKIES_DIR, headless=effective_headless)
        except RuntimeError as e:
            print(f"[{source}] Playwright unavailable, falling back to requests: {e}")
            session = SessionManager(source, COOKIES_DIR)
    else:
        session = SessionManager(source, COOKIES_DIR)
    html_sources = {"wsj", "fool"}
    storage = (HTML_DIR if source in html_sources else PDF_DIR) / source
    return cls(session, storage)


def cmd_setup(_args):
    for d in (COOKIES_DIR, PDF_DIR, HTML_DIR):
        d.mkdir(parents=True, exist_ok=True)
    print(f"✓ dirs criados em {SUBS_DIR}")
    print("\nPara cada site:")
    print("  1. Login no browser.")
    print("  2. Cookie-Editor → Export → JSON.")
    print(f"  3. Guarda em {COOKIES_DIR / '<source>.json'}")
    print("\nSources disponíveis:", ", ".join(ADAPTERS.keys()))
    print("Próximo: ii subs test --source suno")


def cmd_login(args):
    """Abre browser VISÍVEL para login manual. Session persiste em profile_dir.

    Usa-se para sites onde Cookie-Editor não captura auth (SPA JWT em
    localStorage: Suno member, Finclass). Login uma vez, depois Playwright
    reusa persistent context.

    Features:
    - Poll automático de localStorage/cookies; avisa quando login detectado.
    - Captura state.json explícito (session_state.json) — backup em caso de
      Chromium não flush.
    - Termina quando user fecha a janela OU pressiona Ctrl+C.
    """
    import time
    src = args.source
    if src not in ADAPTERS:
        print(f"source '{src}' desconhecido")
        return
    print(f"[{src}] abrindo browser para login manual...")
    session = PlaywrightSession(src, COOKIES_DIR, headless=False, rate_limit_sec=0)
    urls = {
        "suno": "https://investidor.suno.com.br/",
        "finclass": "https://app.finclass.com/",
        "xp": "https://conteudos.xpi.com.br/",
        "wsj": "https://www.wsj.com/",
        "fool": "https://www.fool.com/",
    }
    # Markers específicos por site para detectar logged-in
    login_markers = {
        "suno": ["cognitoidentityserviceprovider", "accesstoken", "idtoken"],
        "finclass": ["auth", "token", "jwt"],
        "xp": ["user", "customer"],
    }
    browser_closed = False
    login_detected = False
    last_storage_snapshot: dict = {}
    try:
        session.get(urls.get(src, "about:blank"), timeout=60)
        print("\n▶ Browser aberto. Faz login manualmente.")
        print("▶ IMPORTANTE: espera até veres o DASHBOARD com os teus dados.")
        print("▶ Quando fechares a janela, session é guardada automaticamente.")
        print(f"▶ Profile dir: {session.profile_dir}\n")
        markers = login_markers.get(src, [])
        state_file = session.profile_dir / "session_state.json"
        tick = 0
        while True:
            time.sleep(3)
            tick += 1
            try:
                pages = session._ctx.pages if session._ctx else []
                if not pages:
                    browser_closed = True
                    break
                page = pages[0]
                page.evaluate("() => true")
                # Poll localStorage para detectar login
                if not login_detected and markers:
                    try:
                        keys = page.evaluate("() => Object.keys(localStorage)")
                        keys_lc = [k.lower() for k in keys]
                        if any(any(m in k for m in markers) for k in keys_lc):
                            login_detected = True
                            print(f"✓ login detectado ({len(keys)} localStorage keys)")
                            # Dump storage_state para backup — funciona mesmo se Chromium falhar flush
                            try:
                                session._ctx.storage_state(path=str(state_file))
                                print(f"✓ state snapshot: {state_file.name}")
                            except Exception as e:
                                print(f"  (state dump failed: {e})")
                    except Exception:
                        pass
                # Snapshot periódico a cada 30s mesmo sem marker detection
                if tick % 10 == 0 and login_detected:
                    try:
                        session._ctx.storage_state(path=str(state_file))
                    except Exception:
                        pass
            except Exception:
                browser_closed = True
                break
    except KeyboardInterrupt:
        print("\n[!] interrompido")
    finally:
        if not browser_closed:
            # Save state antes de close
            try:
                state_file = session.profile_dir / "session_state.json"
                session._ctx.storage_state(path=str(state_file))
            except Exception:
                pass
            session.close()
    if login_detected:
        print(f"✓ session com login persistida para {src}.")
    else:
        print(f"⚠ login NÃO foi detectado (nenhum marker encontrado em localStorage).")
        print(f"  Verifica se chegaste ao dashboard antes de fechar.")
    print(f"  Próximo: `ii subs test --source {src}`")


def cmd_test(args):
    sources = list(ADAPTERS) if args.source == "all" else [args.source]
    for src in sources:
        adapter = None
        try:
            adapter = _make_adapter(src)
            ok, msg = adapter.test_access()
            print(f"[{src:<10}] {msg}")
        except FileNotFoundError as e:
            print(f"[{src:<10}] ✗ {e}")
        except Exception as e:
            print(f"[{src:<10}] ✗ error: {e}")
        finally:
            # fechar Playwright sessions para não contaminar próxima iteração
            if adapter is not None and hasattr(adapter.session, "close"):
                try:
                    adapter.session.close()
                except Exception:
                    pass


def cmd_fetch(args):
    sources = list(ADAPTERS) if args.source == "all" else [args.source]
    total_new = 0
    for src in sources:
        if src == "finclass":
            print(f"[{src}] skip (SPA skeleton — requer Playwright)")
            continue
        try:
            adapter = _make_adapter(src)
        except FileNotFoundError as e:
            print(f"[{src}] skip — {e}")
            continue
        print(f"[{src}] discover (last {args.days}d) ...")
        db = _get_db(src)
        new = 0
        try:
          with sqlite3.connect(db) as c:
            for report in adapter.discover(since_days=args.days):
                # dedup check
                row = c.execute(
                    "SELECT id FROM analyst_reports WHERE source=? AND source_id=?",
                    (report.source, report.source_id),
                ).fetchone()
                if row:
                    continue
                # fetch full content
                try:
                    report = adapter.fetch_one(report)
                except Exception as e:
                    print(f"  [{src}] fetch failed {report.source_id[:8]}: {e}")
                    continue
                c.execute(
                    """INSERT INTO analyst_reports
                       (source, source_id, url, title, author, published_at, fetched_at,
                        content_type, local_path, raw_text, language, tags_json, extract_status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')""",
                    (
                        report.source, report.source_id, report.url, report.title,
                        report.author, report.published_at, _now_iso(),
                        report.content_type,
                        str(report.local_path) if report.local_path else None,
                        report.raw_text,
                        report.language,
                        json.dumps(report.tags),
                    ),
                )
                new += 1
                print(f"  + {report.published_at} {report.title[:70]}")
            c.commit()
        finally:
            if hasattr(adapter.session, "close"):
                try:
                    adapter.session.close()
                except Exception:
                    pass
        print(f"[{src}] {new} new reports")
        total_new += new
    print(f"\ntotal: {total_new} new reports")


def cmd_extract(args):
    from fetchers.subscriptions._pdf_extract import (
        extract_pdf_text, extract_html_text, extract_insights,
    )

    # universe de tickers para hint do prompt
    ticker_universe = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            for r in c.execute("SELECT ticker FROM companies"):
                ticker_universe.append(r[0])

    sources = list(ADAPTERS) if args.source == "all" else [args.source]
    total = 0
    for src in sources:
        db = _get_db(src)
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            q = """SELECT id, source_id, title, content_type, local_path, raw_text, published_at
                   FROM analyst_reports
                   WHERE source=? AND extract_status='pending'
                   ORDER BY published_at DESC
                   LIMIT ?"""
            rows = list(c.execute(q, (src, args.limit)))
            print(f"[{src}] {len(rows)} reports pending extract")
            for row in rows:
                rid = row["id"]
                text = row["raw_text"] or ""
                if row["content_type"] == "pdf" and row["local_path"]:
                    try:
                        text = extract_pdf_text(Path(row["local_path"]))
                    except Exception as e:
                        print(f"  ✗ {row['source_id'][:8]} pdf extract failed: {e}")
                        c.execute(
                            "UPDATE analyst_reports SET extract_status='failed' WHERE id=?",
                            (rid,),
                        )
                        continue
                if not text or len(text) < 200:
                    c.execute(
                        "UPDATE analyst_reports SET extract_status='skipped' WHERE id=?",
                        (rid,),
                    )
                    continue
                print(f"  … {row['published_at']} {row['title'][:60]}")
                result = extract_insights(text, ticker_universe=ticker_universe)
                if "error" in result:
                    print(f"    ✗ {result['error']}")
                    c.execute(
                        "UPDATE analyst_reports SET extract_status='failed' WHERE id=?",
                        (rid,),
                    )
                    continue
                summary = result.get("summary", "")[:1000]
                tags = result.get("tags", [])
                insights = result.get("insights", [])
                c.execute(
                    """UPDATE analyst_reports
                       SET summary=?, tags_json=?, extracted_at=?, extract_status='done'
                       WHERE id=?""",
                    (summary, json.dumps(tags), _now_iso(), rid),
                )
                for ins in insights:
                    c.execute(
                        """INSERT INTO analyst_insights
                           (report_id, ticker, kind, claim, stance, price_target,
                            confidence, evidence_quote, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            rid,
                            ins.get("ticker"),
                            ins.get("kind", "thesis"),
                            ins.get("claim", "")[:500],
                            ins.get("stance"),
                            ins.get("price_target"),
                            float(ins.get("confidence", 0.5)),
                            (ins.get("evidence_quote") or "")[:500],
                            _now_iso(),
                        ),
                    )
                total += 1
                c.commit()
    print(f"\n✓ {total} reports extracted")


def cmd_query(args):
    ticker = args.ticker.upper()
    cutoff = (datetime.now() - timedelta(days=args.days)).date().isoformat()
    print(f"Analyst views on {ticker} (last {args.days}d):\n")
    total = 0
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = list(c.execute(
                """SELECT r.source, r.published_at, r.title, r.url,
                          i.kind, i.claim, i.stance, i.price_target, i.confidence
                   FROM analyst_insights i JOIN analyst_reports r ON i.report_id=r.id
                   WHERE i.ticker=? AND r.published_at >= ?
                   ORDER BY r.published_at DESC, i.confidence DESC""",
                (ticker, cutoff),
            ))
            for row in rows:
                stance = f" [{row['stance']}]" if row['stance'] else ""
                pt = f" PT={row['price_target']}" if row['price_target'] else ""
                print(f"{row['published_at']} [{row['source']}] {row['kind']}{stance}{pt}")
                print(f"  {row['claim']}")
                print(f"  → {row['title'][:80]}")
                print()
                total += 1
    if total == 0:
        print("(nenhum insight ainda; correr `ii subs fetch && ii subs extract` primeiro)")
    else:
        print(f"{total} insights total.")


def cmd_latest(args):
    cutoff = (datetime.now() - timedelta(days=args.days)).date().isoformat()
    sources = list(ADAPTERS) if args.source == "all" else [args.source]
    for src in sources:
        db = _get_db(src)
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = list(c.execute(
                """SELECT published_at, title, url, summary, extract_status
                   FROM analyst_reports
                   WHERE source=? AND published_at >= ?
                   ORDER BY published_at DESC LIMIT 20""",
                (src, cutoff),
            ))
        if not rows:
            continue
        print(f"\n=== {src} ({len(rows)} reports, last {args.days}d) ===")
        for r in rows:
            status = "✓" if r["extract_status"] == "done" else "…"
            print(f"  {status} {r['published_at']}  {r['title'][:80]}")
            if r["summary"]:
                print(f"      {r['summary'][:160]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("setup")

    lp2 = sub.add_parser("login")
    lp2.add_argument("--source", required=True, choices=list(ADAPTERS))

    tp = sub.add_parser("test")
    tp.add_argument("--source", default="all", choices=["all", *ADAPTERS])

    fp = sub.add_parser("fetch")
    fp.add_argument("--source", default="all", choices=["all", *ADAPTERS])
    fp.add_argument("--days", type=int, default=7)

    ep = sub.add_parser("extract")
    ep.add_argument("--source", default="all", choices=["all", *ADAPTERS])
    ep.add_argument("--limit", type=int, default=20)

    qp = sub.add_parser("query")
    qp.add_argument("ticker")
    qp.add_argument("--days", type=int, default=90)

    lp = sub.add_parser("latest")
    lp.add_argument("--source", default="all", choices=["all", *ADAPTERS])
    lp.add_argument("--days", type=int, default=7)

    args = ap.parse_args()
    {
        "setup": cmd_setup,
        "login": cmd_login,
        "test": cmd_test,
        "fetch": cmd_fetch,
        "extract": cmd_extract,
        "query": cmd_query,
        "latest": cmd_latest,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
