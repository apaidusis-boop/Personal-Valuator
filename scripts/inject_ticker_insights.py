"""inject_ticker_insights — adiciona/refresha secção `## Recent insights & mentions`
em cada `obsidian_vault/tickers/<TK>.md`.

Agrega 3 fontes do mesmo ticker:
  1. video_insights (YouTube + Podcast — mesma tabela, source distinguido por channel)
  2. analyst_insights (Suno/XP/WSJ/Finclass via subscriptions)
  3. video_themes (macro themes — informativo, não por ticker)

Idempotente: se a secção existir, substitui; se não existir, insere antes de
`## 📈 Live snapshot` (se houver) ou no fim do ficheiro.

Migra automaticamente a secção legada `## YouTube insights` para o novo formato.

Uso:
    python scripts/inject_ticker_insights.py                   # scan all tickers
    python scripts/inject_ticker_insights.py --ticker ITSA4    # 1 ticker
    python scripts/inject_ticker_insights.py --holdings-only   # só holdings
    python scripts/inject_ticker_insights.py --dry-run         # print sem write
    python scripts/inject_ticker_insights.py --max-yt 10 --max-analyst 8

Cron: wired em daily_run.bat após VAULT-EXPORT.
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

SECTION_HEAD = "## 🎙️ Recent insights & mentions"
LEGACY_HEAD = "## YouTube insights"

# Section is inserted just before this anchor if present (post-fundamentals,
# pre-live-snapshot makes sense visually).
ANCHOR_BEFORE = "## 📈 Live snapshot"

# Default windows — generous enough to surface stale-but-relevant takes.
DEFAULT_VIDEO_DAYS = 90
DEFAULT_ANALYST_DAYS = 120


def _market_db(market: str) -> Path:
    return DB_BR if (market or "br").lower() == "br" else DB_US


def _frontmatter(path: Path) -> dict:
    """Tiny YAML frontmatter parser."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def _fetch_video_insights(ticker: str, market: str, days: int, limit: int) -> list[dict]:
    db = _market_db(market)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    out = []
    try:
        with sqlite3.connect(db) as c:
            rows = c.execute(
                """
                SELECT v.published_at, v.channel, v.title,
                       i.kind, i.claim, i.confidence, i.evidence_quote
                FROM video_insights i
                LEFT JOIN videos v ON i.video_id = v.video_id
                WHERE i.ticker = ?
                  AND COALESCE(v.published_at, i.created_at) >= ?
                ORDER BY COALESCE(v.published_at, i.created_at) DESC,
                         i.confidence DESC
                LIMIT ?
                """,
                (ticker, cutoff, limit),
            ).fetchall()
    except sqlite3.OperationalError:
        return []
    for pub, ch, title, kind, claim, conf, ev in rows:
        out.append({
            "date": (pub or "")[:10],
            "channel": ch or "—",
            "title": title or "",
            "kind": kind,
            "claim": (claim or "").strip(),
            "confidence": conf or 0.0,
            "evidence": (ev or "").strip(),
        })
    return out


def _fetch_analyst_insights(ticker: str, market: str, days: int, limit: int) -> list[dict]:
    db = _market_db(market)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    out = []
    try:
        with sqlite3.connect(db) as c:
            rows = c.execute(
                """
                SELECT r.published_at, r.source, r.title,
                       ai.kind, ai.stance, ai.claim, ai.price_target, ai.confidence
                FROM analyst_insights ai
                JOIN analyst_reports r ON ai.report_id = r.id
                WHERE ai.ticker = ?
                  AND r.published_at >= ?
                ORDER BY r.published_at DESC,
                         ai.confidence DESC NULLS LAST
                LIMIT ?
                """,
                (ticker, cutoff, limit),
            ).fetchall()
    except sqlite3.OperationalError:
        return []
    for pub, src, title, kind, stance, claim, pt, conf in rows:
        out.append({
            "date": (pub or "")[:10],
            "source": (src or "—").upper(),
            "title": title or "",
            "kind": kind or "—",
            "stance": stance or "—",
            "claim": (claim or "").strip(),
            "price_target": pt,
            "confidence": conf,
        })
    return out


def _fetch_themes_for_ticker(ticker: str, market: str, days: int, limit: int) -> list[dict]:
    """Themes are per-video, not per-ticker. We surface themes from videos
    that ALSO mention this ticker."""
    db = _market_db(market)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    out = []
    try:
        with sqlite3.connect(db) as c:
            rows = c.execute(
                """
                SELECT DISTINCT v.published_at, v.channel, t.theme, t.stance,
                       t.summary, t.confidence
                FROM video_themes t
                JOIN videos v ON t.video_id = v.video_id
                JOIN video_insights i ON i.video_id = t.video_id
                WHERE i.ticker = ?
                  AND v.published_at >= ?
                ORDER BY v.published_at DESC LIMIT ?
                """,
                (ticker, cutoff, limit),
            ).fetchall()
    except sqlite3.OperationalError:
        return []
    for pub, ch, theme, stance, summary, conf in rows:
        out.append({
            "date": (pub or "")[:10],
            "channel": ch or "—",
            "theme": theme,
            "stance": stance or "—",
            "summary": (summary or "").strip(),
            "confidence": conf or 0.0,
        })
    return out


def _truncate(s: str, n: int) -> str:
    s = (s or "").replace("|", "\\|").replace("\n", " ").strip()
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


def build_section(ticker: str, market: str, max_yt: int, max_analyst: int,
                  max_themes: int, video_days: int, analyst_days: int) -> str:
    yt = _fetch_video_insights(ticker, market, video_days, max_yt)
    an = _fetch_analyst_insights(ticker, market, analyst_days, max_analyst)
    th = _fetch_themes_for_ticker(ticker, market, video_days, max_themes)

    if not yt and not an and not th:
        return ""  # nothing to inject — caller may strip legacy section

    lines: list[str] = [SECTION_HEAD, ""]
    lines.append(f"_Auto-gerado · {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
                 f"yt={len(yt)} · analyst={len(an)} · themes={len(th)}_")
    lines.append("")

    if yt:
        lines.append(f"### 🎬 YouTube + Podcast (últimos {video_days}d)")
        lines.append("")
        lines.append("| Data | Fonte | Kind | Conf | Claim |")
        lines.append("|---|---|---|---:|---|")
        for ins in yt:
            d = ins["date"] or "—"
            ch = _truncate(ins["channel"], 28)
            kind = ins["kind"] or "—"
            conf = f"{ins['confidence']:.2f}" if ins["confidence"] else "—"
            claim = _truncate(ins["claim"], 140)
            lines.append(f"| {d} | {ch} | {kind} | {conf} | {claim} |")
        lines.append("")

    if an:
        lines.append(f"### 📰 Analyst reports (últimos {analyst_days}d)")
        lines.append("")
        lines.append("| Data | Fonte | Kind | Stance | PT | Claim |")
        lines.append("|---|---|---|---|---:|---|")
        for ins in an:
            d = ins["date"] or "—"
            src = _truncate(ins["source"], 8)
            kind = ins["kind"] or "—"
            stance = ins["stance"] or "—"
            pt = f"{ins['price_target']:.2f}" if ins["price_target"] else "—"
            claim = _truncate(ins["claim"], 130)
            lines.append(f"| {d} | {src} | {kind} | {stance} | {pt} | {claim} |")
        lines.append("")

    if th:
        lines.append(f"### 🌐 Macro themes mencionados (últimos {video_days}d)")
        lines.append("")
        lines.append("| Data | Fonte | Tema | Stance | Resumo |")
        lines.append("|---|---|---|---|---|")
        for ins in th:
            d = ins["date"] or "—"
            ch = _truncate(ins["channel"], 28)
            theme = ins["theme"]
            stance = ins["stance"]
            summary = _truncate(ins["summary"], 110)
            lines.append(f"| {d} | {ch} | {theme} | {stance} | {summary} |")
        lines.append("")

    return "\n".join(lines)


def _strip_section(text: str, head: str) -> str:
    """Remove an existing section ('## ...') up to next '##' or EOF."""
    pattern = re.compile(
        r"^" + re.escape(head) + r".*?(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    return pattern.sub("", text)


def _insert_before_anchor(text: str, section: str, anchor: str) -> str:
    """Insert section just before the anchor heading. Falls back to end."""
    if not section:
        return text
    section = section.rstrip() + "\n\n"
    if anchor in text:
        return text.replace(anchor, section + anchor, 1)
    return text.rstrip() + "\n\n" + section


def update_ticker_file(path: Path, dry_run: bool, max_yt: int, max_analyst: int,
                       max_themes: int, video_days: int, analyst_days: int) -> tuple[bool, str]:
    fm = _frontmatter(path)
    ticker = fm.get("ticker") or path.stem
    market = (fm.get("market") or "").lower()
    if market not in ("br", "us"):
        return False, f"unknown market: {market!r}"

    new_section = build_section(ticker, market, max_yt, max_analyst, max_themes,
                                video_days, analyst_days)

    text = path.read_text(encoding="utf-8")
    new_text = text

    # Strip legacy + current sections (we always rewrite from DB).
    new_text = _strip_section(new_text, LEGACY_HEAD)
    new_text = _strip_section(new_text, SECTION_HEAD)

    # Collapse triple+ blank lines that the strip may have introduced.
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    if new_section:
        new_text = _insert_before_anchor(new_text, new_section, ANCHOR_BEFORE)

    if new_text == text:
        return False, "no change"

    if dry_run:
        return True, f"would update ({len(new_section)//1024}KB section)"

    path.write_text(new_text, encoding="utf-8")
    return True, f"updated ({len(new_section)} chars)"


def iter_targets(args) -> list[Path]:
    if args.ticker:
        p = TICKERS_DIR / f"{args.ticker}.md"
        if not p.exists():
            print(f"  [SKIP] {args.ticker}.md not found")
            return []
        return [p]

    paths = sorted(TICKERS_DIR.glob("*.md"))
    if args.holdings_only:
        kept = []
        for p in paths:
            fm = _frontmatter(p)
            if fm.get("is_holding"):
                kept.append(p)
        return kept
    return paths


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", default=None)
    p.add_argument("--holdings-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--max-yt", type=int, default=10)
    p.add_argument("--max-analyst", type=int, default=8)
    p.add_argument("--max-themes", type=int, default=5)
    p.add_argument("--video-days", type=int, default=DEFAULT_VIDEO_DAYS)
    p.add_argument("--analyst-days", type=int, default=DEFAULT_ANALYST_DAYS)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    if not TICKERS_DIR.exists():
        print(f"ERROR: {TICKERS_DIR} not found")
        return 2

    targets = iter_targets(args)
    if not targets:
        print("no ticker files matched")
        return 0

    n_changed = 0
    n_total = len(targets)
    for path in targets:
        try:
            changed, msg = update_ticker_file(
                path, args.dry_run,
                args.max_yt, args.max_analyst, args.max_themes,
                args.video_days, args.analyst_days,
            )
            if changed:
                n_changed += 1
                if not args.quiet:
                    print(f"  [WRITE] {path.stem:10s} — {msg}")
            elif not args.quiet and args.ticker:
                print(f"  [SKIP]  {path.stem:10s} — {msg}")
        except Exception as e:
            print(f"  [FAIL]  {path.stem:10s} — {type(e).__name__}: {e}")

    print(f"\nupdated {n_changed}/{n_total} ticker files"
          f"{' (dry-run)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
