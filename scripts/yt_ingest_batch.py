"""yt_ingest_batch — corre yt_ingest.py sobre uma lista de video_ids ou URLs.

Ganha de bater o pipeline de forma sequencial num único processo Python,
reaproveitando o carregamento de modelos (Whisper + Ollama warm cache).
Default: skip se o vídeo já tem insights/themes persistidos.

Usos:
    python scripts/yt_ingest_batch.py --ids DPYjtKsW7Ek,eM1acX1fYb4
    python scripts/yt_ingest_batch.py --file urls.txt
    python scripts/yt_ingest_batch.py --channel-last UCJ6q8DczoyLFcFcGs4CrdXQ --count 14
    python scripts/yt_ingest_batch.py --ids a,b,c --force
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
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

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def _channel_last(channel_id: str, count: int) -> list[str]:
    """yt-dlp --flat-playlist para top N video_ids do canal."""
    yt_dlp = str(ROOT / ".venv" / "Scripts" / "yt-dlp.exe")
    if not Path(yt_dlp).exists():
        yt_dlp = "yt-dlp"
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    cmd = [yt_dlp, "--flat-playlist", "--playlist-end", str(count),
           "--print", "%(id)s", url]
    out = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _already_has_facts(video_id: str) -> bool:
    import sqlite3
    from youtube.persistence import DB_BR, DB_US
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            n = c.execute(
                "SELECT COUNT(*) FROM video_insights WHERE video_id=?", (video_id,)
            ).fetchone()[0]
            if n > 0:
                return True
    return False


def _run_one(video_id: str, force_retranscribe: bool, skip_if_has_facts: bool) -> dict:
    """Spawn fresh subprocess per video.

    Motivo: faster-whisper CUDA mantém GPU memory até GC destruir o WhisperModel,
    e o GC Python não corre entre chamadas in-process. Ollama 32B precisa ~20GB
    livres e falha silentemente (OOM no CUDA server) se Whisper segurar VRAM.
    Subprocess isola → Windows limpa GPU quando o processo sai.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = [sys.executable, str(ROOT / "scripts" / "yt_ingest.py"), url]
    if force_retranscribe:
        cmd.append("--force-retranscribe")
    if skip_if_has_facts:
        cmd.append("--skip-if-has-facts")
    rc = subprocess.call(cmd)
    return {"video_id": video_id, "rc": rc}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ids", help="Comma-separated video_ids")
    g.add_argument("--file", help="File with one URL/ID per line")
    g.add_argument("--channel-last", help="Channel id; fetches latest N")
    ap.add_argument("--count", type=int, default=14, help="Used with --channel-last")
    ap.add_argument("--force", action="store_true", help="Re-transcribe even if cached")
    ap.add_argument("--force-extract", action="store_true",
                    help="Re-run extractor even if facts already persisted")
    args = ap.parse_args()

    handlers = [
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "yt_ingest.log", encoding="utf-8"),
    ]
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s",
                        handlers=handlers)

    if args.ids:
        video_ids = [s.strip() for s in args.ids.split(",") if s.strip()]
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            raw = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
        video_ids = []
        for r in raw:
            if r.startswith("http"):
                from scripts.yt_ingest import _extract_video_id
                vid = _extract_video_id(r)
                if vid:
                    video_ids.append(vid)
            else:
                video_ids.append(r)
    else:
        video_ids = _channel_last(args.channel_last, args.count)

    t0 = datetime.now(UTC)
    print(f"Batch: {len(video_ids)} videos. force_retranscribe={args.force} force_extract={args.force_extract}", flush=True)

    results = []
    for i, vid in enumerate(video_ids, 1):
        tt = datetime.now(UTC)
        if not args.force_extract and _already_has_facts(vid) and not args.force:
            print(f"\n[{i}/{len(video_ids)}] {vid} — skip (já tem insights)", flush=True)
            results.append({"video_id": vid, "status": "skipped_has_facts"})
            continue
        print(f"\n[{i}/{len(video_ids)}] {vid}", flush=True)
        try:
            r = _run_one(vid, args.force, skip_if_has_facts=not args.force_extract)
            r["elapsed_sec"] = round((datetime.now(UTC) - tt).total_seconds(), 1)
            results.append(r)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR: {e}", flush=True)
            results.append({"video_id": vid, "status": "error", "error": str(e)})

    dt = (datetime.now(UTC) - t0).total_seconds()
    print(f"\n=== DONE {len(video_ids)} videos in {dt/60:.1f}min ===", flush=True)
    print(json.dumps(results, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
