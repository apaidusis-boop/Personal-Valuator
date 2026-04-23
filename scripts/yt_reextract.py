"""yt_reextract — re-corre router/extract/validate sobre transcripts cached.

Zero rede, zero GPU (Whisper). Só LLM local (Ollama) + SQL. Custo por
vídeo: o mesmo do extractor original.

Usos:
    python scripts/yt_reextract.py --all               # todos os videos com transcript
    python scripts/yt_reextract.py --video eM1acX1fYb4 # um vídeo
    python scripts/yt_reextract.py --channel "Virtual Asset"
    python scripts/yt_reextract.py --all --dry-run     # simular
    python scripts/yt_reextract.py --all --skip-themes # só tickers (mais rápido)

Utilidade: validar fixes de aliases/validator sem re-transcrever. Muito
mais barato que re-correr o pipeline completo.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from youtube.extractor import extract_for_theme, extract_for_ticker
from youtube.models import ExtractorOutput
from youtube.persistence import (
    clear_video_facts,
    list_cached_video_ids,
    load_cached_transcript,
    persist,
)
from youtube.router import load_aliases, route
from youtube.validator import DEFAULT_CONFIDENCE_THRESHOLD, validate

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def _setup_logging(verbose: bool) -> None:
    handlers = [
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "yt_ingest.log", encoding="utf-8"),
    ]
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=handlers,
    )


def _process_one(
    video_id: str,
    aliases: dict,
    confidence_threshold: float,
    skip_themes: bool,
    dry_run: bool,
) -> dict:
    cached = load_cached_transcript(video_id)
    if cached is None:
        return {"video_id": video_id, "status": "no_transcript_cached"}

    meta, lang, chunks, full_text = cached
    ro = route(chunks, aliases)

    if len(ro.tickers_matched) == 0 and len(ro.themes_matched) < 2:
        if not dry_run:
            persist(meta=meta, lang=lang, status="skipped_no_relevance",
                    insights=[], themes=[], aliases=aliases,
                    transcript_text=full_text, transcript_chunks=chunks)
        return {
            "video_id": video_id, "status": "skipped_no_relevance",
            "tickers": ro.tickers_matched, "themes": ro.themes_matched,
        }

    aggregated = ExtractorOutput()
    for ticker, windows in ro.ticker_windows.items():
        text = "\n\n---\n\n".join(w.text for w in windows)
        out = extract_for_ticker(ticker, text)
        aggregated.insights.extend(out.insights)
    if not skip_themes:
        for theme, windows in ro.theme_windows.items():
            text = "\n\n---\n\n".join(w.text for w in windows)
            out = extract_for_theme(theme, text)
            aggregated.themes.extend(out.themes)

    kept_ins, kept_themes, vstats = validate(
        aggregated, full_text, aliases=aliases,
        confidence_threshold=confidence_threshold,
    )

    if dry_run:
        return {
            "video_id": video_id, "status": "dry_run",
            "tickers": ro.tickers_matched, "themes": ro.themes_matched,
            "kept_insights": len(kept_ins), "kept_themes": len(kept_themes),
            "validator": vstats,
        }

    cleared = clear_video_facts(video_id)
    pstats = persist(
        meta=meta, lang=lang, status="completed",
        insights=kept_ins, themes=kept_themes, aliases=aliases,
        transcript_text=full_text, transcript_chunks=chunks,
    )
    return {
        "video_id": video_id, "status": "completed",
        "tickers": ro.tickers_matched, "themes": ro.themes_matched,
        "kept_insights": len(kept_ins), "kept_themes": len(kept_themes),
        "validator": vstats, "cleared": cleared, "persist": pstats,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--video", help="Single video_id")
    g.add_argument("--channel", help="All cached videos from this channel")
    ap.add_argument("--confidence-threshold", type=float, default=DEFAULT_CONFIDENCE_THRESHOLD)
    ap.add_argument("--skip-themes", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    _setup_logging(args.verbose)

    aliases = load_aliases()

    if args.video:
        video_ids = [args.video]
    elif args.channel:
        video_ids = list_cached_video_ids(channel=args.channel)
    else:
        video_ids = list_cached_video_ids()

    if not video_ids:
        print("Nenhum vídeo cached. Corre primeiro yt_ingest.py.", flush=True)
        return 1

    print(f"Processing {len(video_ids)} video(s). dry_run={args.dry_run} skip_themes={args.skip_themes}", flush=True)
    t0 = datetime.now(UTC)
    summary = []
    for i, vid in enumerate(video_ids, 1):
        tt = datetime.now(UTC)
        print(f"\n[{i}/{len(video_ids)}] {vid}", flush=True)
        res = _process_one(vid, aliases, args.confidence_threshold, args.skip_themes, args.dry_run)
        dt = (datetime.now(UTC) - tt).total_seconds()
        res["elapsed_sec"] = round(dt, 1)
        summary.append(res)
        print(json.dumps({k: v for k, v in res.items() if k != "validator"}, ensure_ascii=False), flush=True)

    total = (datetime.now(UTC) - t0).total_seconds()
    print(f"\n=== DONE {len(video_ids)} videos in {total:.1f}s ===", flush=True)
    ki = sum(r.get("kept_insights", 0) for r in summary)
    kt = sum(r.get("kept_themes", 0) for r in summary)
    print(f"Totals: insights_kept={ki} themes_kept={kt}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
