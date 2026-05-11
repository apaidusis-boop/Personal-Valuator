"""Downloader + extractor de PDFs de fatos relevantes da CVM.

Para cada linha em events onde source='cvm' e full_text é NULL:
  1. baixa o PDF do Link_Download para data/cvm_pdfs/<id>.pdf
  2. extrai o texto com pdfplumber
  3. guarda full_text + pdf_path na linha

Idempotente: eventos já processados são saltados. Tolerante a falhas por
evento (continua os outros).

Uso:
    python monitors/cvm_pdf_extractor.py                # todos pendentes
    python monitors/cvm_pdf_extractor.py --ticker ITSA4 # só ITSA4
    python monitors/cvm_pdf_extractor.py --limit 5      # só 5 eventos
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber
import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
PDF_DIR = ROOT / "data" / "cvm_pdfs"
LOG_DIR = ROOT / "logs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "cvm_pdf_extractor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def download_pdf(url: str, target: Path, attempts: int = 3, base_timeout: int = 45) -> None:
    """Download com retry exponencial. CVM RAD é conhecido por timeouts/SSL
    transitórios. Aumenta timeout a cada tentativa."""
    import time as _t
    last_exc: Exception | None = None
    for i in range(attempts):
        timeout = base_timeout * (i + 1)
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                snippet = r.content[:200].decode("latin-1", errors="replace")
                raise RuntimeError(f"resposta não é PDF (começa com: {snippet!r})")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(r.content)
            return
        except Exception as e:  # noqa: BLE001
            last_exc = e
            if i < attempts - 1:
                _t.sleep(2 ** i * 3)  # 3s, 6s, 12s
    raise last_exc or RuntimeError("download failed")


def extract_text(pdf_path: Path, engine: str = "pdfplumber") -> str:
    """Extract CVM PDF text. engine in {pdfplumber, markitdown, auto}.

    pdfplumber is the legacy default (fast, reliable on CVM layouts).
    markitdown produces structured Markdown (tables/headers preserved) —
    useful when full_text downstream feeds Qwen/Ollama for IR analysis.
    auto: markitdown first, pdfplumber fallback if markitdown errors.
    """
    if engine in ("markitdown", "auto"):
        try:
            from library._md_extract import extract_text as _md_extract
            text = _md_extract(pdf_path, engine=engine)
            if text:
                return text
        except Exception:
            pass
        # fall through to pdfplumber on any failure
    chunks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            chunks.append(txt)
    # normalização simples: colapsa whitespace excessivo preservando parágrafos
    full = "\n\n".join(c.strip() for c in chunks if c.strip())
    lines = [ln.rstrip() for ln in full.splitlines()]
    return "\n".join(lines).strip()


def process_event(conn: sqlite3.Connection, row: sqlite3.Row, engine: str = "pdfplumber") -> tuple[bool, str]:
    event_id, ticker, url = row["id"], row["ticker"], row["url"]
    if not url:
        return False, "sem url"
    pdf_path = PDF_DIR / f"{event_id}.pdf"
    try:
        if not pdf_path.exists():
            download_pdf(url, pdf_path)
        text = extract_text(pdf_path, engine=engine)
        if not text:
            return False, "PDF sem texto extraível"
        conn.execute(
            "UPDATE events SET full_text=?, pdf_path=? WHERE id=?",
            (text, str(pdf_path.relative_to(ROOT)), event_id),
        )
        return True, f"{len(text)} chars"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


_NET_FAIL_MARKERS = ("SSLError", "ConnectionError", "Timeout", "URLError",
                      "ProxyError", "ReadTimeout", "ConnectTimeout")


def _looks_like_network_failure(msg: str) -> bool:
    return any(marker in msg for marker in _NET_FAIL_MARKERS)


def run(ticker: str | None = None, limit: int | None = None, engine: str = "pdfplumber") -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    # Circuit breaker pre-check: if cvm endpoint already tripped from prior runs,
    # abort with exit-friendly message instead of burning 4min per event.
    try:
        from agents._health import _is_tripped, record as _hb_record
        tripped, why = _is_tripped("cvm")
        if tripped:
            _log({"event": "extract_skipped",
                  "reason": f"cvm circuit breaker tripped: {why}"})
            return
    except ImportError:
        _hb_record = None

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        query = (
            "SELECT id, ticker, event_date, kind, url FROM events "
            "WHERE source='cvm' AND (full_text IS NULL OR full_text='')"
        )
        params: list = []
        if ticker:
            query += " AND ticker=?"
            params.append(ticker)
        query += " ORDER BY event_date DESC"
        if limit:
            query += f" LIMIT {int(limit)}"
        pending = conn.execute(query, params).fetchall()

        _log({"event": "extract_start", "pending": len(pending)})

        ok_count = 0
        fail_count = 0
        consecutive_net_fails = 0
        for row in pending:
            ok, msg = process_event(conn, row, engine=engine)
            _log({
                "event": "extract_result",
                "event_id": row["id"],
                "ticker": row["ticker"],
                "date": row["event_date"],
                "kind": row["kind"],
                "ok": ok,
                "msg": msg,
            })
            if ok:
                ok_count += 1
                consecutive_net_fails = 0
                if _hb_record:
                    _hb_record("cvm", "ok")
                conn.commit()
            else:
                fail_count += 1
                if _looks_like_network_failure(msg):
                    consecutive_net_fails += 1
                    if _hb_record:
                        _hb_record("cvm", "fail", msg[:200])
                    # 3 consecutive network fails = endpoint is down, bail out.
                    # Saves ~4min × remaining events of pointless retries.
                    if consecutive_net_fails >= 3:
                        _log({"event": "extract_aborted",
                              "reason": "3 consecutive network failures — circuit tripped",
                              "remaining": len(pending) - (ok_count + fail_count)})
                        break
                else:
                    consecutive_net_fails = 0
            time.sleep(0.5)  # gentileza com o servidor CVM

        _log({"event": "extract_done", "ok": ok_count, "fail": fail_count})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--engine", default="pdfplumber",
                    choices=["pdfplumber", "markitdown", "auto"],
                    help="PDF extraction engine. markitdown = structured MD; "
                         "auto = markitdown→pdfplumber fallback.")
    args = ap.parse_args()
    run(args.ticker, args.limit, engine=args.engine)


if __name__ == "__main__":
    main()
