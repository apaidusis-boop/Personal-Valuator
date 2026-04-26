"""Daily Research Digest — relatório de actividade da Bibliotheca + research.

Saída: `obsidian_vault/Bibliotheca/Research_Digest_YYYY-MM-DD.md` — vista
única do que aconteceu nas últimas 24h:

  1. Clippings novos ingested  (Investopedia / Suno / Motley Fool / etc.)
  2. Tavily web searches       (perpetuum autoresearch + dossier wires)
  3. Methods extraídos          (library/methods/*.yaml novos)
  4. Books processados          (library/books/ + chunks)
  5. Perpetuum runs             (today's sweep)
  6. Coverage gaps surfaced     (tickers sem thesis, banks sem BACEN, etc.)
  7. Bibliotheca alerts         (BIB001-004 do librarian perpetuum)
  8. RAG ask-ready topics       (sample queries para o utilizador testar)

Idempotente: re-running mesmo dia sobrescreve.

Uso:
    python scripts/research_digest.py            # hoje
    python scripts/research_digest.py --days 7   # window 7d
    python scripts/research_digest.py --since YYYY-MM-DD
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT/"data"/"br_investments.db", "us": ROOT/"data"/"us_investments.db"}
CLIPPINGS_DIR = ROOT / "obsidian_vault" / "Clippings"
BIBLIO_DIR = ROOT / "obsidian_vault" / "Bibliotheca"
METHODS_DIR = ROOT / "library" / "methods"
BOOKS_DIR = ROOT / "library" / "books"
CHUNKS_INDEX = ROOT / "library" / "chunks_index.db"
TAVILY_CACHE = ROOT / "data" / "tavily_cache"


def _files_modified_since(directory: Path, cutoff_ts: float, suffix: str = ".md") -> list[Path]:
    if not directory.exists():
        return []
    out = []
    for p in directory.glob(f"*{suffix}"):
        if p.stem.startswith("_"):
            continue
        try:
            if p.stat().st_mtime >= cutoff_ts:
                out.append(p)
        except OSError:
            pass
    return sorted(out, key=lambda p: -p.stat().st_mtime)


def _pull_clipping_meta(p: Path) -> dict:
    """Quick frontmatter scan."""
    text = p.read_text(encoding="utf-8", errors="ignore")[:1500]
    if not text.startswith("---"):
        return {"title": p.stem, "source": "", "author": ""}
    fm = text.split("---", 2)[1]
    out = {"title": p.stem, "source": "", "author": ""}
    for line in fm.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            if k in ("title", "source", "author", "published"):
                out[k] = v.strip().strip('"').strip("'")
    return out


def _format_url(s: str, max_len: int = 50) -> str:
    if not s:
        return ""
    s = s.replace("https://", "").replace("http://", "")
    if len(s) > max_len:
        return s[:max_len-3] + "..."
    return s


def _scan_tavily_cache(cutoff_ts: float) -> list[dict]:
    """Return list of recent Tavily cache entries with query + URL count."""
    out = []
    if not TAVILY_CACHE.exists():
        return out
    for p in TAVILY_CACHE.glob("*.json"):
        try:
            if p.stat().st_mtime < cutoff_ts:
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            q = data.get("query", "?")
            results = data.get("results", []) or data.get("response", {}).get("results", [])
            ans = (data.get("answer") or "")[:80]
            out.append({"query": q, "n_urls": len(results), "answer_preview": ans,
                        "ts": p.stat().st_mtime})
        except Exception:
            pass
    return sorted(out, key=lambda d: -d["ts"])


def _perpetuum_runs_today(today: str) -> list[tuple]:
    db = DBS["br"]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        try:
            return c.execute(
                "SELECT perpetuum_name, subjects_count, alerts_count, summary "
                "FROM perpetuum_run_log WHERE run_date=? "
                "ORDER BY perpetuum_name", (today,)
            ).fetchall()
        except sqlite3.OperationalError:
            return []


def _clipping_chunk_stats() -> tuple[int, int]:
    if not CHUNKS_INDEX.exists():
        return 0, 0
    with sqlite3.connect(CHUNKS_INDEX) as c:
        n = c.execute("SELECT COUNT(*) FROM chunk_index WHERE book_slug LIKE 'clip_%'").fetchone()[0]
        d = c.execute("SELECT COUNT(DISTINCT book_slug) FROM chunk_index WHERE book_slug LIKE 'clip_%'").fetchone()[0]
        return n, d


def _bibliotheca_alerts(today: str) -> list[tuple]:
    """Return list of (subject_id, score, flags, action_hint) for BIB alerts today."""
    db = DBS["br"]
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        try:
            rows = c.execute(
                "SELECT subject_id, score, details_json, action_hint "
                "FROM perpetuum_health WHERE perpetuum_name='bibliotheca' "
                "AND run_date=? AND score < 100 "
                "ORDER BY score, subject_id LIMIT 25", (today,)
            ).fetchall()
            return rows
        except sqlite3.OperationalError:
            return []


def _coverage_gaps() -> list[str]:
    out = []
    with sqlite3.connect(DBS["br"]) as c:
        # Bank without Basel
        bank_t = {r[0] for r in c.execute("SELECT ticker FROM companies WHERE sector='Banks'").fetchall()}
        bank_basel = {r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM bank_quarterly_history WHERE basel_ratio IS NOT NULL"
        ).fetchall()}
        missing_bacen = sorted(bank_t - bank_basel)
        if missing_bacen:
            out.append(f"Banks sem BACEN: {missing_bacen} → `ii dossier {missing_bacen[0]}` (auto-bootstrap)")

        # Holdings sem fundamentals
        try:
            rows = c.execute(
                "SELECT c.ticker FROM companies c LEFT JOIN fundamentals f "
                "ON c.ticker=f.ticker WHERE c.is_holding=1 AND f.ticker IS NULL"
            ).fetchall()
            if rows:
                out.append(f"Holdings BR sem fundamentals: {[r[0] for r in rows]}")
        except sqlite3.OperationalError:
            pass

        # Conviction stale (older than 7d)
        try:
            n = c.execute(
                "SELECT COUNT(DISTINCT ticker) FROM conviction_scores "
                "WHERE run_date < date('now','-7 days')"
            ).fetchone()[0]
            if n > 0:
                out.append(f"Conviction stale (>7d): {n} tickers")
        except sqlite3.OperationalError:
            pass
    return out


def _new_methods_since(cutoff_ts: float) -> list[Path]:
    if not METHODS_DIR.exists():
        return []
    return sorted([p for p in METHODS_DIR.glob("*.yaml")
                   if p.stat().st_mtime >= cutoff_ts],
                  key=lambda p: -p.stat().st_mtime)


def _new_books_since(cutoff_ts: float) -> list[Path]:
    if not BOOKS_DIR.exists():
        return []
    return sorted([p for p in BOOKS_DIR.glob("*")
                   if p.is_file() and p.stat().st_mtime >= cutoff_ts],
                  key=lambda p: -p.stat().st_mtime)


def _suggested_rag_topics() -> list[str]:
    """Returns hand-curated topics that the user can ask via `ii vault` or RAG."""
    return [
        "como o Buffett define moat?",
        "qual o critério Graham para uma acção barata?",
        "quando reinvestir dividendos via DRIP vs receber em cash?",
        "quais sinais antecedem uma crise de dívida (Dalio)?",
        "como avaliar margem de segurança em bancos?",
        "diferença entre value e growth investing na prática?",
    ]


def render_digest(target_date: str, days: int) -> str:
    cutoff_ts = (datetime.fromisoformat(target_date) - timedelta(days=days-1)).timestamp()
    cutoff_dt = datetime.fromtimestamp(cutoff_ts).strftime("%Y-%m-%d %H:%M")

    new_clips = _files_modified_since(CLIPPINGS_DIR, cutoff_ts)
    tavily = _scan_tavily_cache(cutoff_ts)
    perp_runs = _perpetuum_runs_today(target_date)
    n_clip_chunks, n_clip_distinct = _clipping_chunk_stats()
    biblio_alerts = _bibliotheca_alerts(target_date)
    gaps = _coverage_gaps()
    new_methods = _new_methods_since(cutoff_ts)
    new_books = _new_books_since(cutoff_ts)
    rag_topics = _suggested_rag_topics()

    lines: list[str] = []

    # Frontmatter
    lines += [
        "---",
        "type: research_digest",
        f"date: {target_date}",
        f"window_days: {days}",
        f"cutoff: {cutoff_dt}",
        f"clippings_added: {len(new_clips)}",
        f"tavily_searches: {len(tavily)}",
        f"methods_added: {len(new_methods)}",
        f"books_added: {len(new_books)}",
        f"clip_rag_chunks_total: {n_clip_chunks}",
        f"clip_rag_distinct_total: {n_clip_distinct}",
        "tags: [bibliotheca, research_digest, daily]",
        "---",
        "",
        f"# 📚 Research Digest — {target_date}",
        "",
        f"> Janela: últimos **{days}d** (desde {cutoff_dt}). "
        "Cross-links: [[CONSTITUTION]] · [[Bibliotheca/_Index]]",
        "",
        "## TL;DR",
        "",
        f"- Clippings novos: **{len(new_clips)}**",
        f"- Tavily web searches: **{len(tavily)}**",
        f"- Methods extraídos: **{len(new_methods)}**",
        f"- Books processados: **{len(new_books)}**",
        f"- Perpetuum runs hoje: **{len(perp_runs)}**",
        f"- Bibliotheca catálogo (RAG cumulativo): **{n_clip_distinct} clips / {n_clip_chunks} chunks**",
        "",
    ]

    # 1. Clippings novos
    lines += ["## 1. Clippings novos", ""]
    if not new_clips:
        lines += ["_(nenhum clipping novo na janela)_", ""]
    else:
        lines += ["| Título | Fonte | Autor |",
                  "|---|---|---|"]
        for p in new_clips[:30]:
            m = _pull_clipping_meta(p)
            title = m["title"][:60]
            src = _format_url(m.get("source", ""))
            author = m.get("author", "").replace("[[", "").replace("]]", "")[:30]
            lines.append(f"| [[Clippings/{p.stem}\\|{title}]] | {src} | {author} |")
        if len(new_clips) > 30:
            lines.append(f"\n_(+{len(new_clips)-30} mais)_")
        lines.append("")

    # 2. Tavily web searches
    lines += ["## 2. Tavily web searches", ""]
    if not tavily:
        lines += ["_(nenhuma chamada Tavily na janela)_", ""]
    else:
        lines += ["| Query | URLs | Answer preview |",
                  "|---|---|---|"]
        for t in tavily[:25]:
            q = t["query"][:60].replace("|", "\\|")
            urls = t["n_urls"]
            ans = t.get("answer_preview", "").replace("|", "\\|").replace("\n", " ")[:80]
            lines.append(f"| {q} | {urls} | {ans} |")
        if len(tavily) > 25:
            lines.append(f"\n_(+{len(tavily)-25} mais — total cache size: {len(list(TAVILY_CACHE.glob('*.json'))) if TAVILY_CACHE.exists() else 0})_")
        lines.append("")

    # 3. Methods extracted
    lines += ["## 3. Methods registered", ""]
    if not new_methods:
        lines += ["_(nenhum método novo na janela — total disponível: "
                  f"{len(list(METHODS_DIR.glob('*.yaml'))) if METHODS_DIR.exists() else 0})_", ""]
    else:
        for p in new_methods[:20]:
            lines.append(f"- `{p.name}`")
        if len(new_methods) > 20:
            lines.append(f"\n_(+{len(new_methods)-20} mais)_")
        lines.append("")

    # 4. Books
    lines += ["## 4. Books processados", ""]
    if not new_books:
        lines += [f"_(nenhum book novo — total: {len(list(BOOKS_DIR.glob('*'))) if BOOKS_DIR.exists() else 0})_", ""]
    else:
        for p in new_books:
            sz = p.stat().st_size / 1024 / 1024
            lines.append(f"- `{p.name}` ({sz:.1f} MB)")
        lines.append("")

    # 5. Perpetuum runs
    lines += ["## 5. Perpetuum runs hoje", "",
              "| Name | Subjects | Alerts | Summary |", "|---|---|---|---|"]
    if not perp_runs:
        lines.append("| _(nenhum)_ | — | — | — |")
    else:
        for name, subj, alerts, summ in perp_runs:
            summ = (summ or "")[:60].replace("|", "\\|")
            lines.append(f"| {name} | {subj} | {alerts} | {summ} |")
    lines.append("")

    # 6. Coverage gaps
    lines += ["## 6. Coverage gaps surfaced", ""]
    if not gaps:
        lines += ["_(nenhum gap material detectado)_", ""]
    else:
        for g in gaps:
            lines.append(f"- ▸ {g}")
        lines.append("")

    # 7. Bibliotheca alerts
    lines += ["## 7. Bibliotheca alerts (BIB001-004)", ""]
    if not biblio_alerts:
        lines += ["_(nenhum alert hoje)_", ""]
    else:
        lines += ["| Subject | Score | Flags | Action |", "|---|---|---|---|"]
        for sid, score, dj, hint in biblio_alerts[:25]:
            try:
                d = json.loads(dj or "{}")
                flags = ",".join(d.get("flags", []))[:40]
            except Exception:
                flags = "?"
            hint = (hint or "")[:60]
            lines.append(f"| {sid} | {score} | {flags} | {hint} |")
        lines.append("")

    # 8. Suggested RAG topics
    lines += ["## 8. RAG ready-to-ask",
              "",
              "Tópicos prontos para `ii vault` ou `python -m library.rag ask`:",
              ""]
    for q in rag_topics:
        lines.append(f"- `python -m library.rag ask \"{q}\" --k 6`")
    lines.append("")

    lines += ["---",
              f"*Gerado por `scripts/research_digest.py` em {datetime.now().strftime('%Y-%m-%d %H:%M')}*"]

    return "\n".join(lines) + "\n"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1, help="Window in days (default 1)")
    ap.add_argument("--since", help="Override target date (YYYY-MM-DD); default today")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    target = args.since or date.today().isoformat()
    BIBLIO_DIR.mkdir(parents=True, exist_ok=True)

    md = render_digest(target, args.days)
    out_path = BIBLIO_DIR / f"Research_Digest_{target}.md"
    out_path.write_text(md, encoding="utf-8")

    if not args.quiet:
        print(f"[digest] {out_path.relative_to(ROOT)}")
        print(f"  size: {len(md):,} chars / {md.count(chr(10)):,} lines")
        # quick top-line metrics
        for line in md.splitlines():
            if line.startswith("- ") and "**" in line:
                print(f"  {line.lstrip('- ')}")


if __name__ == "__main__":
    main()
