"""yt_ingest — ingere um vídeo do YouTube, extrai factos estruturados.

Pipeline:
  URL → yt-dlp (áudio) → faster-whisper (transcript em RAM) →
  router (aliases.yaml) → ollama Qwen2.5 (JSON) →
  validator (evidence substring + dedup + confidence) →
  persist (videos/video_insights/video_themes em BR+US DBs) →
  cleanup (apaga áudio).

Uso:
    python scripts/yt_ingest.py <url>
    python scripts/yt_ingest.py <url> --dry-run
    python scripts/yt_ingest.py <url> --verbose

Zero tokens Claude. Zero bloat em disco (só factos + metadata).
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Windows console default é cp1252 — força UTF-8 para evitar crashes com
# caracteres PT (ç, á, R$, €) em prints de insights/themes.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def _ensure_runtime_paths() -> None:
    """Injecta ffmpeg + CUDA DLLs no PATH se o terminal não os tiver.

    O Claude Code / shells persistentes podem ter o PATH desactualizado.
    Este helper faz introspecção de locais conhecidos para não depender
    do user ter de reabrir o terminal antes de cada run.
    """
    extras: list[str] = []

    # ffmpeg via winget
    winget_ff = Path(os.environ.get("LOCALAPPDATA", "")) / (
        r"Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    )
    if winget_ff.exists():
        for sub in winget_ff.glob("ffmpeg-*/bin"):
            extras.append(str(sub))
            break

    # CUDA DLLs bundled via pip (nvidia-cublas-cu12, nvidia-cudnn-cu12)
    try:
        import nvidia  # noqa: F401
        nvidia_root = Path(sys.modules["nvidia"].__path__[0])
        for sub in ("cublas/bin", "cudnn/bin", "cuda_nvrtc/bin"):
            p = nvidia_root / sub
            if p.exists():
                extras.append(str(p))
    except ImportError:
        pass

    if extras:
        current = os.environ.get("PATH", "")
        prefix = os.pathsep.join(extras)
        if prefix not in current:
            os.environ["PATH"] = prefix + os.pathsep + current
        # Windows LoadLibrary não honra PATH para DLLs pip-installed;
        # usar os.add_dll_directory (Python 3.8+) para ctranslate2.
        if hasattr(os, "add_dll_directory"):
            for p in extras:
                try:
                    os.add_dll_directory(p)
                except (OSError, FileNotFoundError):
                    pass


_ensure_runtime_paths()

from youtube.cleanup import remove_audio
from youtube.downloader import download
from youtube.extractor import extract_for_theme, extract_for_ticker
from youtube.models import ExtractorOutput
from youtube.persistence import (
    clear_video_facts,
    load_cached_transcript,
    persist,
)
from youtube.router import load_aliases, route
from youtube.transcriber import transcribe
from youtube.validator import DEFAULT_CONFIDENCE_THRESHOLD, validate

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def _extract_video_id(url: str) -> str | None:
    """Parse video_id do URL sem rede. Aceita youtube.com/watch?v=..., youtu.be/..., etc."""
    import re
    from urllib.parse import parse_qs, urlparse
    try:
        p = urlparse(url)
    except Exception:  # noqa: BLE001
        return None
    if p.hostname and "youtu.be" in p.hostname:
        return p.path.lstrip("/").split("/")[0] or None
    if p.hostname and "youtube.com" in p.hostname:
        qs = parse_qs(p.query)
        if "v" in qs:
            return qs["v"][0]
        m = re.match(r"/(?:embed|shorts)/([^/?#]+)", p.path)
        if m:
            return m.group(1)
    return None


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "yt_ingest.log", encoding="utf-8"),
    ]
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=handlers,
    )


def _banner(msg: str) -> None:
    print(f"\n=== {msg} ===", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", nargs="?", default=None,
                    help="YouTube URL (skip if --audio-file)")
    ap.add_argument(
        "--audio-file",
        default=None,
        help="Caminho para MP3/M4A já descarregado. Skip phase 1 (download). "
             "Usado por pod_poll.py para reaproveitar a engine Whisper+Ollama.",
    )
    ap.add_argument(
        "--source-id",
        default=None,
        help="ID sintético quando --audio-file (ex: WSJ-whats-news-2026-05-08).",
    )
    ap.add_argument(
        "--source-channel",
        default=None,
        help="Nome do canal/show quando --audio-file (ex: 'WSJ — What\\'s News').",
    )
    ap.add_argument(
        "--source-title",
        default=None,
        help="Título do episódio/vídeo quando --audio-file.",
    )
    ap.add_argument(
        "--source-pubdate",
        default=None,
        help="ISO date do episódio quando --audio-file.",
    )
    ap.add_argument(
        "--source-url",
        default=None,
        help="URL canónico do episódio (RSS enclosure ou show page) quando --audio-file.",
    )
    ap.add_argument(
        "--confidence-threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"Min confidence to persist (default {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Run pipeline but do not persist to DB",
    )
    ap.add_argument(
        "--skip-themes",
        action="store_true",
        help="Skip theme extraction (ticker insights only)",
    )
    ap.add_argument(
        "--verbose", "-v",
        action="store_true",
    )
    ap.add_argument(
        "--force-retranscribe",
        action="store_true",
        help="Ignorar transcript cached, re-transcrever (usa rede + GPU).",
    )
    ap.add_argument(
        "--skip-if-has-facts",
        action="store_true",
        help="Se o vídeo já tem insights/themes persistidos, skip inteiramente.",
    )
    args = ap.parse_args()

    if not args.url and not args.audio_file:
        ap.error("either url OR --audio-file must be provided")
    if args.audio_file and not args.source_id:
        ap.error("--audio-file requires --source-id (used as video_id)")

    _setup_logging(args.verbose)
    log = logging.getLogger("yt_ingest")
    t0 = datetime.now(UTC)

    # --- Branch: --audio-file (podcast / external audio) vs URL (YouTube) ---
    audio_file_mode = bool(args.audio_file)
    cached = None
    audio_path = None
    from_cache = False

    if audio_file_mode:
        from youtube.models import VideoMetadata
        meta = VideoMetadata(
            video_id=args.source_id,
            url=args.source_url or f"audio-file://{args.source_id}",
            title=args.source_title or args.source_id,
            channel=args.source_channel or "external",
            published_at=args.source_pubdate,
        )
        # External audio path also caches by video_id, so re-runs skip download.
        if not args.force_retranscribe:
            cached = load_cached_transcript(args.source_id)
        if cached:
            from_cache = True
            meta, lang, chunks, full_text = cached
            _banner("1/6 Cached transcript found — skip transcribe")
            print(f"video_id={meta.video_id} chars={len(full_text)} chunks={len(chunks)} — zero GPU", flush=True)
        else:
            _banner("1/6 Audio file given — skip download")
            audio_path = Path(args.audio_file)
            if not audio_path.exists():
                print(f"ERROR: audio file not found: {audio_path}", flush=True)
                return 2
            print(f"audio: {audio_path.name} ({audio_path.stat().st_size // 1024}KB) — '{meta.title}' ({meta.channel})", flush=True)
    else:
        # --- Try cache-first: extrair video_id do URL + checar DB antes de descarregar ---
        video_id = _extract_video_id(args.url)
        if video_id and not args.force_retranscribe:
            cached = load_cached_transcript(video_id)
        from_cache = cached is not None

        if from_cache:
            meta, lang, chunks, full_text = cached
            _banner("1/6 Cached transcript found — skip download/transcribe")
            print(f"video_id={meta.video_id} chars={len(full_text)} chunks={len(chunks)} — zero rede/GPU", flush=True)

            if args.skip_if_has_facts:
                import sqlite3
                from youtube.persistence import DB_BR
                with sqlite3.connect(DB_BR) as conn:
                    n = conn.execute(
                        "SELECT COUNT(*) FROM video_insights WHERE video_id=?",
                        (meta.video_id,),
                    ).fetchone()[0]
                if n > 0:
                    print(f"SKIPPED: already has {n} insights (--skip-if-has-facts)", flush=True)
                    return 0
        else:
            _banner("1/6 Download")
            dl = download(args.url)
            if not dl.ok:
                log.error("download failed: %s", dl.error)
                print(f"ERROR: download failed — {dl.error}", flush=True)
                return 2
            print(f"video: {dl.metadata.title!r} ({dl.metadata.duration_sec}s) — {dl.metadata.channel}", flush=True)
            meta = dl.metadata
            audio_path = dl.audio_path

    try:
        if not from_cache:
            _banner("2/6 Transcrever (Whisper)")
            tr = transcribe(audio_path)
            print(f"lang={tr.lang} duration={tr.duration_sec:.0f}s chunks={len(tr.chunks)} chars={len(tr.full_text)}", flush=True)
            chunks = tr.chunks
            full_text = tr.full_text
            lang = tr.lang

        _banner("3/6 Router (aliases)")
        aliases = load_aliases()
        ro = route(chunks, aliases)
        print(f"tickers matched: {ro.tickers_matched or '(none)'}", flush=True)
        print(f"themes matched:  {ro.themes_matched or '(none)'}", flush=True)

        # Short-circuit: 0 tickers E <2 themes → não vale a pena LLM
        if len(ro.tickers_matched) == 0 and len(ro.themes_matched) < 2:
            print("SKIPPED: low relevance (0 tickers, <2 themes) — skipping extractor", flush=True)
            if not args.dry_run:
                persist(
                    meta=meta, lang=lang, status="skipped_no_relevance",
                    insights=[], themes=[], aliases=aliases,
                    transcript_text=full_text,
                    transcript_chunks=chunks,
                )
            return 0

        # Re-extract path: limpa factos prévios do vídeo (idempotência forte)
        if from_cache:
            cleared = clear_video_facts(meta.video_id)
            print(f"cleared prior facts: {cleared}", flush=True)

        _banner("4/6 Extract (Ollama)")
        aggregated = ExtractorOutput()
        for ticker, windows in ro.ticker_windows.items():
            text = "\n\n---\n\n".join(w.text for w in windows)
            out = extract_for_ticker(ticker, text)
            n = len(out.insights)
            print(f"  {ticker:<8s} → {n} insights (raw)", flush=True)
            aggregated.insights.extend(out.insights)
        if not args.skip_themes:
            for theme, windows in ro.theme_windows.items():
                text = "\n\n---\n\n".join(w.text for w in windows)
                out = extract_for_theme(theme, text)
                n = len(out.themes)
                print(f"  theme:{theme:<24s} → {n} themes (raw)", flush=True)
                aggregated.themes.extend(out.themes)

        _banner("5/6 Validate")
        kept_ins, kept_themes, stats = validate(
            aggregated, full_text,
            aliases=aliases,
            confidence_threshold=args.confidence_threshold,
        )
        print(json.dumps(stats, indent=2), flush=True)

        _banner("6/6 Persist")
        if args.dry_run:
            print("DRY-RUN — no DB writes. Would persist:", flush=True)
            for ins in kept_ins:
                print(f"  [{ins.ticker}] {ins.kind} ({ins.confidence:.2f}): {ins.claim}", flush=True)
            for th in kept_themes:
                print(f"  [{th.theme}] {th.stance} ({th.confidence:.2f}): {th.summary}", flush=True)
        else:
            pstats = persist(
                meta=meta, lang=lang, status="completed",
                insights=kept_ins, themes=kept_themes, aliases=aliases,
                transcript_text=full_text,
                transcript_chunks=chunks,
            )
            print(json.dumps(pstats, indent=2), flush=True)
    finally:
        if audio_path is not None:
            remove_audio(audio_path)

    dt = (datetime.now(UTC) - t0).total_seconds()
    print(f"\nDone in {dt:.1f}s.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
