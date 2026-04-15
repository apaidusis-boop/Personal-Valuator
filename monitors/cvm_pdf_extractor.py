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


def download_pdf(url: str, target: Path) -> None:
    r = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
    r.raise_for_status()
    # CVM às vezes devolve HTML de erro com status 200 — sanity check
    if not r.content.startswith(b"%PDF"):
        snippet = r.content[:200].decode("latin-1", errors="replace")
        raise RuntimeError(f"resposta não é PDF (começa com: {snippet!r})")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(r.content)


def extract_text(pdf_path: Path) -> str:
    chunks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            chunks.append(txt)
    # normalização simples: colapsa whitespace excessivo preservando parágrafos
    full = "\n\n".join(c.strip() for c in chunks if c.strip())
    lines = [ln.rstrip() for ln in full.splitlines()]
    return "\n".join(lines).strip()


def process_event(conn: sqlite3.Connection, row: sqlite3.Row) -> tuple[bool, str]:
    event_id, ticker, url = row["id"], row["ticker"], row["url"]
    if not url:
        return False, "sem url"
    pdf_path = PDF_DIR / f"{event_id}.pdf"
    try:
        if not pdf_path.exists():
            download_pdf(url, pdf_path)
        text = extract_text(pdf_path)
        if not text:
            return False, "PDF sem texto extraível"
        conn.execute(
            "UPDATE events SET full_text=?, pdf_path=? WHERE id=?",
            (text, str(pdf_path.relative_to(ROOT)), event_id),
        )
        return True, f"{len(text)} chars"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def run(ticker: str | None = None, limit: int | None = None) -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
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
        for row in pending:
            ok, msg = process_event(conn, row)
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
                conn.commit()
            else:
                fail_count += 1
            time.sleep(0.5)  # gentileza com o servidor CVM

        _log({"event": "extract_done", "ok": ok_count, "fail": fail_count})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    run(args.ticker, args.limit)


if __name__ == "__main__":
    main()
